class SalarySearchJobObject:
    def __init__(self):
        self.jobId = ""
        self.jobTitle = ""
        self.advertiserName = ""
        self.jobUrl = ""
        self.jobSoup = ""
        self.salaryRange = ""

    def get_jobId(self):
        return self.jobId
    
    def set_jobId(self,jobId):
        self.jobId = jobId
    
    def get_jobTitle(self):
        return self.jobTitle
    
    def set_jobTitle(self,jobTitle):
        self.jobTitle = jobTitle
    
    def get_advertiserName(self):
        return self.advertiserName
    
    def set_advertiserName(self,advertiserName):
        self.advertiserName = advertiserName
    
    def get_jobUrl(self):
        return self.jobUrl
    
    def set_jobUrl(self,jobUrl):
        self.jobUrl = jobUrl

    def get_jobSoup(self):
        return self.jobSoup
    
    def set_jobSoup(self,jobSoup):
        self.jobSoup = jobSoup


    def get_salaryRange(self):
        return self.salaryRange
    
    def set_salaryRange(self,salaryRange):
        self.salaryRange = salaryRange







'''
job_url = "https://www.seek.com.au/job/"+str(event['queryStringParameters']['id'])+"?"

    job_url_soup = create_soup(job_url)
    jobTitle, advertiser_name = find_title_create_soup(job_url)
    global_JobID = find_Job_ID(job_url)

    global_job_ID_search_string = "href=\"/job/"+ global_JobID
    global_this_company_jobs_url = create_jobsearch_url(jobTitle,advertiser_name)

    low_arr = np.arange(1, 350000, 1000)
    result = lowvalue_binary_search(low_arr, 0, len(low_arr)-1, job_url,global_JobID)
    

    high_arr = np.arange(low_arr[result], 350000, 1000)

    high_result_index = highvalue_binary_search(high_arr, 0, len(high_arr)-1, job_url,global_JobID)

    output_salary_range = "The Role: " + str(jobTitle)+ "is paying aroung the $" + str(low_arr[result]) + "- $" +str(high_arr[high_result_index])

'''

