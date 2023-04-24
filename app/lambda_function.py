
 

from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import SoupStrainer as strainer
import requests
import lxml
import json
import numpy as np
import re



def main_function(url_from_lambda):


    def create_soup(url):
        page = requests.get(url)
        only_item_cells = strainer("a", href=True)
        soup = BeautifulSoup(page.content, "lxml", parse_only=only_item_cells)
        return soup

    def find_title_create_soup(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.title.text , soup.select_one('[data-automation="advertiser-name"]').text


    


    
    def all_indexes_of_substring(string):
        indexes = []
        for match in re.finditer(r'-', string):
            indexes.append(match.start())
        return indexes


    #Platform Engineer - AWS Cloud Job in North Sydney, Sydney NSW - SEEK
    def create_jobsearch_url():
        string = str(jobTitle)
        title_string = string[0:string.index(" Job")].strip()
        title_string += " "+ str(advertiser_name).strip()
        title_string = title_string.replace('-', '+').replace(' ', '-')+"-jobs"
        location_string = string[string.index("in "):string.index(" - SEEK")].strip().replace(',', '').replace('-', '+').replace(' ', '-')
        if location_string.count("-")>2:
            indexes = all_indexes_of_substring(location_string)
            location_string = "in"+location_string[indexes[len(indexes)-2]:]
        return "https://www.seek.com.au/"+title_string+"/"+location_string
        

    def find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def find_Job_ID(job_url):
        return find_between(job_url,"job/","?")
    

    def does_job_exist(JobID,url):
        page = requests.get(url)
        only_item_cells = strainer('article',{"data-job-id" : str(JobID)}) #data-job-id="66089824"
        soup = BeautifulSoup(page.content, 'html.parser', parse_only=only_item_cells)
        return soup.text != ""


    def generate_query_url(min,max,url):
        print(url + "?salaryrange="+str(min)+"-"+str(max)+"&salarytype=annual") #dleete after 
        return url + "?salaryrange="+str(min)+"-"+str(max)+"&salarytype=annual"



    

    def check_for_min_value(value,url): #return equal, too small, too high
        if does_job_exist(global_JobID,generate_query_url(0,value,global_this_company_jobs_url))==False:
            return "too small"
        if does_job_exist(global_JobID,generate_query_url(0,value-1000,global_this_company_jobs_url))==True:
            return "too high"
        return "equal"

    def check_for_max_value(value,url): #return equal, too small, too high
        if does_job_exist(global_JobID,generate_query_url(value,350000,global_this_company_jobs_url))== False:
            return "too high"
        if does_job_exist(global_JobID,generate_query_url(value+1000,350000,global_this_company_jobs_url))==True:
            return "too small"
        return "equal" 

    def lowvalue_binary_search(arr, low, high, url):
    
        # Check base case
        if high >= low:
    
            mid = (high + low) // 2
    
            # If element is present at the middle itself
            if check_for_min_value(arr[mid],url)  == "equal":
                return mid
    
            # If element is smaller than mid, then it can only
            # be present in left subarray
            elif check_for_min_value(arr[mid],url)  == "too high":
                return lowvalue_binary_search(arr, low, mid - 1, url)
    
            # Else the element can only be present in right subarray
            else:
                return lowvalue_binary_search(arr, mid + 1, high, url)
    
        else:
            # Element is not present in the array
            return -1
    

    # Returns index of x in arr if present, else -1
    def highvalue_binary_search(arr, low, high, url):
    
        # Check base case
        if high >= low:
    
            mid = (high + low) // 2
    
            # If element is present at the middle itself
            if check_for_max_value(arr[mid],url)  == "equal":
                return mid
    
            # If element is smaller than mid, then it can only
            # be present in left subarray
            elif check_for_max_value(arr[mid],url)  == "too high":
                return highvalue_binary_search(arr, low, mid - 1, url)
    
            # Else the element can only be present in right subarray
            else:
                return highvalue_binary_search(arr, mid + 1, high, url)
    
        else:
            # Element is not present in the array
            return -1

    job_url = url_from_lambda

    job_url_soup = create_soup(job_url)
    jobTitle, advertiser_name = find_title_create_soup(job_url)
    global_JobID = find_Job_ID(job_url)

    global_job_ID_search_string = "href=\"/job/"+ global_JobID
    global_this_company_jobs_url = create_jobsearch_url()

    low_arr = np.arange(1, 350000, 1000)
    result = lowvalue_binary_search(low_arr, 0, len(low_arr)-1, job_url)
    

    high_arr = np.arange(low_arr[result], 350000, 1000)

    high_result_index = highvalue_binary_search(high_arr, 0, len(high_arr)-1, job_url)

    output_salary_range = "The Role: " + str(jobTitle)+ "is paying aroung the $" + str(low_arr[result]) + "- $" +str(high_arr[high_result_index])
    return output_salary_range





def lambda_handler(event, context):
    print("event is")
    print(event)
    job_url = "https://www.seek.com.au/job/"+str(event['queryStringParameters']['id'])+"?"
    body = main_function(job_url)
    print("returning the body as")
    print(body)
    statusCode = 200
    return {
        'statusCode': statusCode,
        'body': json.dumps(body),
        "headers":{
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin" : '*'
        }
    }
