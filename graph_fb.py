import urllib.parse
import urllib.request
import json
import re
import os
import sys

# Search with FB Graph API
# Returns 'data' field of the returned JSON
def search(query, token):
    base_url = 'https://graph.facebook.com/v2.0/search?'
    search_type = 'place'
    p = {'access_token' : token,
         'q'            : query,
         'type'         : search_type,
        } 
    parameters = urllib.parse.urlencode(p)
    search_result = make_request(base_url + parameters)
    return search_result['data']


# Make http request and return parsed JSON
def make_request(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    content = json.loads(response.read().decode('utf-8'))
    return content


# Get JSON of a specific page, access token required
def get_page(page_id, token):
    base_url = 'https://graph.facebook.com/v2.0/'
    p = {'access_token' : token,
        }
    parameters = urllib.parse.urlencode(p)
    page_content = make_request(base_url + page_id + '?' + parameters)
    return page_content


# Get the html content of a given page
# By default, the 'About' ('info') tab is fetched
def get_raw_page(link, section='info'):
    raw_page = urllib.request.urlopen(urllib.request.Request(link + '?sk=' + section))
    return raw_page.read().decode('utf-8')


# Use regex to pattern match email address
# If there are multiple email addresses, the first one is returned.
def extract_email(html):
    match = re.search(r'mailto:([\w.-]+)(&#064;|&#64;|&#x40;|@)([\w.-]+)', html)
    if match:
        return match.group(1)+'@'+match.group(3)
    else: 
        match = re.search(r'([\w.-]+)(&#064;|&#64;|&#x40;|@)([\w.-]+)', html)
        if match:
            return match.group(1)+'@'+match.group(3)
    return ''


# Read the configuration file and return the access token
# If conf file does not exist, call generate_app_access_token to genearte
# a new access token
def get_access_token():
    try:
        with open('conf/access_token.conf', 'r') as conf:
            token = conf.read()
            if token.slitlines()[0] == '':
                raise IOError
            return token.splitlines()[0] 
    except IOError:
        print("Error: access_token not found. Generating new token.")
        generate_app_access_token()
        with open('conf/access_token.conf', 'r') as conf:
            return conf.read().splitlines()[0]

# Read the conf file to get app id and secret to generate accesss token
def generate_app_access_token():
    try:
        with open('conf/app_id_secret.conf', 'r') as app:
            credentials = app.read().splitlines()
    except IOError:
        print("Error: conf/app_id_secret.conf not found. Terminate now.")
        sys.exit(0)

    appid = credentials[0]
    secret = credentials[1]
    p = {'client_id' : appid,
         'client_secret' : secret,
         'grant_type' : 'client_credentials',
        }
    base_url = 'https://graph.facebook.com/oauth/access_token?'
    parameters = urllib.parse.urlencode(p)
    req = urllib.request.Request(base_url + parameters)
    response = urllib.request.urlopen(req)
    match = re.search('access_token=(.+)', response.read().decode('utf-8'))
    if match:
        token = match.group(1)
    with open('conf/access_token.conf', 'w') as f:
        f.write(token)
