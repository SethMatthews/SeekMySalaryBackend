from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import SoupStrainer as strainer
import requests
import json
import numpy as np


def find_title_and_advertiser_name(url_to_request):
    '''Returns the job's title as a string and job's advertiser name as a string, for the given url of the job'''
    page_request = requests.get(url_to_request)
    soup = BeautifulSoup(page_request.content, "html.parser")
    return soup.title.text , soup.select_one('[data-automation="advertiser-name"]').text

def all_indexes_of_hyphen_in_string(string):
    '''Returns an array containing all the indexes of the hypen character of a given string'''
    indexes = []
    for index in range(len(string)):
        if string[index] == "-":
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
    return f"{url_to_adapt}?salaryrange={min_salary}-{max_salary}&salarytype=annual"



def check_for_min_value(salary_to_check,job_search_results_url,job_id): 
    '''Checks if given salary_to_check is equal, smaller, or higher than minimum salary of job specified'''
    if is_job_id_in_search(job_id,generate_query_url(0,salary_to_check+1,job_search_results_url))==False:
        return "too small"
    if is_job_id_in_search(job_id,generate_query_url(0,salary_to_check-1,job_search_results_url))==True:
        return "too high"
    return "equal"

def check_for_max_value(salary_to_check,job_search_results_url, job_id): #return equal, too small, too high
    '''Checks if given salary_to_check is equal, smaller, or higher than maximum salary of job specified'''
    if is_job_id_in_search(job_id,generate_query_url(salary_to_check-1,350000,job_search_results_url))== False:
        return "too high"
    if is_job_id_in_search(job_id,generate_query_url(salary_to_check+1,350000,job_search_results_url))==True:
        return "too small"
    return "equal" 

def min_salary_binary_search(arr, low, high, url,job_id, job_search_results_url):
    '''A recursive binary search to find the minimum salary limit of the job_id specified'''
    if high >= low:
        mid = (high + low) // 2
        isThisMinValue = check_for_min_value(arr[mid],job_search_results_url,job_id)
        if isThisMinValue  == "equal":
            return mid
        elif isThisMinValue  == "too high":
            return min_salary_binary_search(arr, low, mid - 1, url,job_id, job_search_results_url)
        else:
            return min_salary_binary_search(arr, mid + 1, high, url, job_id, job_search_results_url)
    else:
        return -1

def max_salary_binary_search(arr, low, high, url, job_id, job_search_results_url):
    "A recursive binary search to find the maximum salary limit of the job_id specified"
    if high >= low:
        mid = (high + low) // 2
        isThisMaxValue = check_for_max_value(arr[mid],job_search_results_url, job_id)
        if isThisMaxValue  == "equal":
            return mid
        elif isThisMaxValue  == "too high":
            return max_salary_binary_search(arr, low, mid - 1, url, job_id, job_search_results_url)
        else:
            return max_salary_binary_search(arr, mid + 1, high, url, job_id, job_search_results_url)
    else:
        return -1


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



def format_job_title(job_description_string):
    job_title = job_description_string[0:job_description_string.index(" Job")].strip()
    return job_title

def format_job_location(job_description_string):
    job_location = job_description_string[job_description_string.index("in ")+3:job_description_string.index(" - SEEK")].strip()
    return job_location





def lambda_handler(event, context):
    print("Event is ")
    print(event)

    job_id = str(event['queryStringParameters']['id'])
    job_url = f"https://www.seek.com.au/job/{job_id}?"  

    job_description_string, advertiser_name = find_title_and_advertiser_name(job_url)

    job_search_results_url = create_jobsearch_url(job_description_string, advertiser_name)

    array_min_salary_binary_search = np.arange(0, 350000, 1000)
    result_index_array_min_salary = min_salary_binary_search(array_min_salary_binary_search, 0, len(array_min_salary_binary_search)-1, job_url,job_id, job_search_results_url)
    
    array_max_salary_binary_search = np.arange(array_min_salary_binary_search[result_index_array_min_salary], 350000, 1000)
    result_index_array_max_salary = max_salary_binary_search(array_max_salary_binary_search, 0, len(array_max_salary_binary_search)-1, job_url, job_id, job_search_results_url)

    minimum_salary_of_job = str(array_min_salary_binary_search[result_index_array_min_salary])
    maximum_salary_of_job = str(array_max_salary_binary_search[result_index_array_max_salary])

    #output_salary_range = f"The Role: {job_description_string} is paying around the ${minimum_salary_of_job} - ${maximum_salary_of_job}"

    response_json = {
        "jobTitle":format_job_title(job_description_string),
        "jobCompany":advertiser_name,
        "jobLocation":format_job_location(job_description_string),
        "minSalary":minimum_salary_of_job,
        "maxSalary":maximum_salary_of_job
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response_json),
        # "headers":{
        #     "Content-Type": "application/json",
        #     "Access-Control-Allow-Origin" : "http://127.0.0.1:5500/"
        # }
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
        }

# Lambda must be configured with Python 3.9 runtime


# Setting up CICD with AWS Codepipeline and Lambda
# https://www.youtube.com/watch?v=AmHZxULclLQ&t=592s&ab_channel=FelixYu
