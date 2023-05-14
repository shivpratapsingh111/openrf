# Author: Shiv Pratap Singh [Kirosci]--[Github]

import re
import urllib.parse
import argparse
import requests
from termcolor import colored


def replace_url_in_query_params(url, replace_url, replace_all):
    # decode the input URL if it is url encoded
    decoded_url = urllib.parse.unquote(url)

    # replace the URL in query parameters
    if replace_all:
        # Replace all parameter values with the replace URL
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(decoded_url).query)
        for key in query_params:
            query_params[key] = [replace_url]
        modified_query = urllib.parse.urlencode(query_params, doseq=True)
        modified_url = re.sub(r'\?.*', '?' + modified_query, decoded_url)
    else:
        # Replace only the URL in query parameters
        modified_url = re.sub(r'((?:^|&)[^&=]*?=)https?://[^&]*', r'\1' + replace_url, decoded_url)
    
    return modified_url

def make_request(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        if 200 <= status_code < 300:
            colored_status = colored(status_code, 'green')
        elif 300 <= status_code < 400:
            colored_status = colored(status_code, 'blue')
        elif 400 <= status_code < 500:
            colored_status = colored(status_code, 'red')
        elif 500 <= status_code < 600:
            colored_status = colored(status_code, 'yellow')
        else:
            colored_status = str(status_code)
        return colored_status
    except requests.exceptions.RequestException as e:
        return str(e)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Usage: python3 openrf.py -f urls.txt -u https://serverurl/ -A -o output.txt')
    parser.add_argument('-f', '--file', type=str, required=True, help='Specify file containing URLs')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL for replacing the vlaues, For operedirect or ssrf\nBurp Collborator, postbin,etc')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output file to save results')
    parser.add_argument('-A', '--replace-all', action='store_true', help='Replace values of all parameters in the url with given url\n Without -A it will only replace the parameters having any url as value')
    parser.add_argument('-R', '--request', action='store_true', help='Make request to each modified URL and print the status code')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        urls = f.readlines()

    with open(args.output, 'w') as f:
        for url in urls:
            updated_url = replace_url_in_query_params(url.strip(), args.url, args.replace_all)
            f.write(updated_url + '\n')
            print(updated_url)
            if args.request:
                response = make_request(updated_url)
                print(f"Status Code: {response}")
