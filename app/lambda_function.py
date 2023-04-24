
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import SoupStrainer as strainer
import requests
import lxml
import json
import numpy as np



def main_function(url_from_lambda):

    print(" url from lambda is ")
    print(url_from_lambda)

    job_url = url_from_lambda

    def create_soup(url):
        page = requests.get(url)
        only_item_cells = strainer("a", href=True)
        soup = BeautifulSoup(page.content, "lxml", parse_only=only_item_cells)
        return soup

    def find_title_create_soup(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.title.text , soup.select_one('[data-automation="advertiser-name"]').text


    job_url_soup = create_soup(job_url)
    jobTitle, advertiser_name = find_title_create_soup(job_url)


    import re
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
    global_JobID = find_Job_ID(job_url)



    global_job_ID_search_string = "href=\"/job/"+ global_JobID

    def does_job_exist(JobID,url):
        page = requests.get(url)
        only_item_cells = strainer('article',{"data-job-id" : str(JobID)}) #data-job-id="66089824"
        soup = BeautifulSoup(page.content, 'html.parser', parse_only=only_item_cells)
        return soup.text != ""


    def generate_query_url(min,max,url):
        print(url + "?salaryrange="+str(min)+"-"+str(max)+"&salarytype=annual") #dleete after 
        return url + "?salaryrange="+str(min)+"-"+str(max)+"&salarytype=annual"



    global_this_company_jobs_url = create_jobsearch_url()

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



#lambda_event_sample = {'version': '2.0', 'routeKey': 'GET /get-salary', 'rawPath': '/get-salary', 'rawQueryString': 'id=62289047', 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', 'content-length': '0', 'host': 'l7nvlry05d.execute-api.us-east-1.amazonaws.com', 'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36', 'x-amzn-trace-id': 'Root=1-6426644b-15e6a0017ad5ee953d3c10a2', 'x-forwarded-for': '122.199.44.88', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'queryStringParameters': {'id': '62289047'}, 'requestContext': {'accountId': '524870747371', 'apiId': 'l7nvlry05d', 'domainName': 'l7nvlry05d.execute-api.us-east-1.amazonaws.com', 'domainPrefix': 'l7nvlry05d', 'http': {'method': 'GET', 'path': '/get-salary', 'protocol': 'HTTP/1.1', 'sourceIp': '122.199.44.88', 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}, 'requestId': 'CoSb4jGUoAMEVow=', 'routeKey': 'GET /get-salary', 'stage': '$default', 'time': '31/Mar/2023:04:40:43 +0000', 'timeEpoch': 1680237643746}, 'isBase64Encoded': False}
#lambda_handler(lambda_event_sample,"lamnda event context filler")