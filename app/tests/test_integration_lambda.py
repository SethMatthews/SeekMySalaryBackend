import sys
import os
 
# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent)
 
# now we can import the module in the parent
# directory.

import lambda_function
import unittest
import json


class LambdaFunctionIntegrationTests(unittest.TestCase):
    def test_findsalary_should_return_successfully(self):
        sample_event = {'version': '2.0', 'routeKey': 'GET /get-salary', 'rawPath': '/get-salary', 'rawQueryString': 'id=66986610', 'headers': {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', 'content-length': '0', 'host': 'l7nvlry05d.execute-api.us-east-1.amazonaws.com', 'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate', 'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 'x-amzn-trace-id': 'Root=1-6445f440-73da9be157133431206ddc3e', 'x-forwarded-for': '202.153.220.224', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'queryStringParameters': {'id': '66986610'}, 'requestContext': {'accountId': '524870747371', 'apiId': 'l7nvlry05d', 'domainName': 'l7nvlry05d.execute-api.us-east-1.amazonaws.com', 'domainPrefix': 'l7nvlry05d', 'http': {'method': 'GET', 'path': '/get-salary', 'protocol': 'HTTP/1.1', 'sourceIp': '202.153.220.224', 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}, 'requestId': 'D3MaDhVtIAMEVww=', 'routeKey': 'GET /get-salary', 'stage': '$default', 'time': '24/Apr/2023:03:15:12 +0000', 'timeEpoch': 1682306112073}, 'isBase64Encoded': False}
        result = lambda_function.lambda_handler(sample_event,0)
        expected_result = {
            'statusCode': 200,
            'body': json.dumps("The Role: Solution Architect Job in Melbourne VIC - SEEKis paying aroung the $150001- $199001"),
            "headers":{
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin" : '*'
            }
        }
        self.assertEqual(result,expected_result)

if __name__ == '__main__':
    unittest.main()