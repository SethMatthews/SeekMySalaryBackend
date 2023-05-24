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
        sample_event = {'version': '2.0', 'routeKey': 'GET /find/salary', 'rawPath': '/find/salary', 'rawQueryString': 'id=67219280', 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', 'content-length': '0', 'host': 'uoacbc7l29.execute-api.us-east-1.amazonaws.com', 'origin': 'https://seekmysalary.com', 'referer': 'https://seekmysalary.com/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1', 'x-amzn-trace-id': 'Root=1-646d81fe-56d860a1690d6cc502e11d71', 'x-forwarded-for': '180.150.37.204', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'queryStringParameters': {'id': '67219280'}, 'requestContext': {'accountId': '524870747371', 'apiId': 'uoacbc7l29', 'domainName': 'uoacbc7l29.execute-api.us-east-1.amazonaws.com', 'domainPrefix': 'uoacbc7l29', 'http': {'method': 'GET', 'path': '/find/salary', 'protocol': 'HTTP/1.1', 'sourceIp': '180.150.37.204', 'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}, 'requestId': 'FaE_vjtHoAMEJqw=', 'routeKey': 'GET /find/salary', 'stage': '$default', 'time': '24/May/2023:03:18:22 +0000', 'timeEpoch': 1684898302001}, 'isBase64Encoded': False}

        result = lambda_function.lambda_handler(sample_event,0)

        response_json = {
        "jobTitle":"Software Engineer (.Net, TypeScript)",
        "jobCompany":"Inlogik Pty Ltd",
        "jobLocation":"Melbourne VIC",
        "minSalary":str(100000),
        "maxSalary":str(200000)
    }
        
        expected_result = {
            'statusCode': 200,
            'body': json.dumps(response_json),
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }
        self.assertEqual(result,expected_result)

if __name__ == '__main__':
    unittest.main()