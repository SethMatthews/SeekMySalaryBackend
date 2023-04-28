from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import SoupStrainer as strainer
import requests
import lxml
import json
import numpy as np




def create_soup(url_for_soup):
    '''Returns BeautifulSoup Object for the given url_for_soup parameter'''
    page = requests.get(url_for_soup)
    filtered_page = strainer("a", href=True)
    soup = BeautifulSoup(page.content, "lxml", parse_only=filtered_page)
    return soup

def find_title_and_advertiser_name(url_of_job_advert):
    '''Returns the job's title as a string and job's advertiser name as a string, for the given url of the job'''
    page = requests.get(url_of_job_advert)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.title.text , soup.select_one('[data-automation="advertiser-name"]').text

def all_indexes_of_hyphen_in_string(string):
    '''Returns an array containing all the indexes of the hypen character of a given string'''
    indexes = []
    for index in string:
        if index == "-":
            indexes.append(index)
    return indexes


#Platform Engineer - AWS Cloud Job in North Sydney, Sydney NSW - SEEK
def create_jobsearch_url(job_title, advertiser_name):
    '''Returns a url which will will produce a Seek search in which the job should be present with no salary filters'''
    string = str(job_title)
    title_string = string[0:string.index(" Job")].strip()
    title_string += " "+ str(advertiser_name).strip()
    title_string = title_string.replace('-', '+').replace(' ', '-')+"-jobs"
    location_string = string[string.index("in "):string.index(" - SEEK")].strip().replace(',', '').replace('-', '+').replace(' ', '-')
    if location_string.count("-")>2:    #this checks for location edge case when more parts of typical location is specified
        indexes = all_indexes_of_hyphen_in_string(location_string)
        location_string = "in"+location_string[indexes[len(indexes)-2]:]
    return f"https://www.seek.com.au/{title_string}/{location_string}"
    

def is_job_id_in_search(job_id,url_to_search):
    '''Returns True if the job id is present in the Seek search of the given url parameter'''
    page = requests.get(url_to_search)
    filtered_page = strainer('article',{"data-job-id" : str(job_id)}) #data-job-id="66089824"
    soup = BeautifulSoup(page.content, 'html.parser', parse_only= filtered_page)
    return soup.text != ""


def generate_query_url(min_salary,max_salary,url_to_adapt):
    print(url_to_adapt + "?salaryrange="+str(min_salary)+"-"+str(max_salary)+"&salarytype=annual") #delete after 
    return f"{url_to_adapt}?salaryrange={min_salary}-{max_salary}&salarytype=annual"



def check_for_min_value(value,job_search_results_url,job_id): #return equal, too small, too high
    if is_job_id_in_search(job_id,generate_query_url(0,value,job_search_results_url))==False:
        return "too small"
    if is_job_id_in_search(job_id,generate_query_url(0,value-1000,job_search_results_url))==True:
        return "too high"
    return "equal"

def check_for_max_value(value,job_search_results_url, job_id): #return equal, too small, too high
    if is_job_id_in_search(job_id,generate_query_url(value,350000,job_search_results_url))== False:
        return "too high"
    if is_job_id_in_search(job_id,generate_query_url(value+1000,350000,job_search_results_url))==True:
        return "too small"
    return "equal" 

def lowvalue_binary_search(arr, low, high, url,job_id, job_search_results_url):
    if high >= low:
        mid = (high + low) // 2

        # If element is present at the middle itself
        if check_for_min_value(arr[mid],job_search_results_url,job_id)  == "equal":
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif check_for_min_value(arr[mid],job_search_results_url, job_id)  == "too high":
            return lowvalue_binary_search(arr, low, mid - 1, url,job_id, job_search_results_url)

        # Else the element can only be present in right subarray
        else:
            return lowvalue_binary_search(arr, mid + 1, high, url, job_id, job_search_results_url)

    else:
        # Element is not present in the array
        return -1


# Returns index of x in arr if present, else -1
def highvalue_binary_search(arr, low, high, url, job_id, job_search_results_url):

    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if check_for_max_value(arr[mid],job_search_results_url, job_id)  == "equal":
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif check_for_max_value(arr[mid],job_search_results_url, job_id)  == "too high":
            return highvalue_binary_search(arr, low, mid - 1, url, job_id, job_search_results_url)

        # Else the element can only be present in right subarray
        else:
            return highvalue_binary_search(arr, mid + 1, high, url, job_id, job_search_results_url)

    else:
        # Element is not present in the array
        return -1





def lambda_handler(event, context):

    print("event is")
    print(event)
    job_url = "https://www.seek.com.au/job/"+str(event['queryStringParameters']['id'])+"?"  

    job_url_soup = create_soup(job_url)
    job_title, advertiser_name = find_title_and_advertiser_name(job_url)

    job_id = str(event['queryStringParameters']['id'])
    #global_job_ID_search_string = "href=\"/job/"+ job_id
    job_search_results_url = create_jobsearch_url(job_title, advertiser_name)

    low_arr = np.arange(1, 350000, 1000)
    result = lowvalue_binary_search(low_arr, 0, len(low_arr)-1, job_url,job_id, job_search_results_url)


    high_arr = np.arange(low_arr[result], 350000, 1000)

    high_result_index = highvalue_binary_search(high_arr, 0, len(high_arr)-1, job_url, job_id, job_search_results_url)

    output_salary_range = "The Role: " + str(job_title)+ "is paying aroung the $" + str(low_arr[result]) + "- $" +str(high_arr[high_result_index])



    print("returning the body as")
    print(output_salary_range)
    statusCode = 200
    return {
        'statusCode': statusCode,
        'body': json.dumps(output_salary_range),
        "headers":{
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin" : '*'
        }
    }