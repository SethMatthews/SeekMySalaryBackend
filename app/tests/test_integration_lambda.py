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
        sample_event = {'version': '2.0', 'routeKey': 'GET /find/salary', 'rawPath': '/find/salary', 'rawQueryString': 'id=67188663', 'headers': {'accept': '*/*', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8', 'content-length': '0', 'host': 'uoacbc7l29.execute-api.us-east-1.amazonaws.com', 'origin': 'http://127.0.0.1:5500', 'referer': 'http://127.0.0.1:5500/', 'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36', 'x-amzn-trace-id': 'Root=1-6462b25f-7dca4dfc0be99b8f42ada634', 'x-forwarded-for': '180.150.37.204', 'x-forwarded-port': '443', 'x-forwarded-proto': 'https'}, 'queryStringParameters': {'id': '67188663'}, 'requestContext': {'accountId': '524870747371', 'apiId': 'uoacbc7l29', 'domainName': 'uoacbc7l29.execute-api.us-east-1.amazonaws.com', 'domainPrefix': 'uoacbc7l29', 'http': {'method': 'GET', 'path': '/find/salary', 'protocol': 'HTTP/1.1', 'sourceIp': '180.150.37.204', 'userAgent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'}, 'requestId': 'E_DPBi9ToAMEYMQ=', 'routeKey': 'GET /find/salary', 'stage': '$default', 'time': '15/May/2023:22:29:51 +0000', 'timeEpoch': 1684189791884}, 'isBase64Encoded': False}

        result = lambda_function.lambda_handler(sample_event,0)
        expected_result = {
            'statusCode': 200,
            'body': json.dumps("The Role: React Engineer Job in Melbourne VIC - SEEK is paying around the $120001 - $199001"),
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
        }
        self.assertEqual(result,expected_result)

if __name__ == '__main__':
    unittest.main()