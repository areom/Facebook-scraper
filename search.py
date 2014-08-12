import argparse
import graph_fb 
import csv
import os
from subprocess import Popen

argparser = argparse.ArgumentParser()
group = argparser.add_mutually_exclusive_group()
argparser.add_argument("-q", help="Your query.", required=True)
argparser.add_argument("-f", help="Specify a CSV file as output.")
argparser.add_argument("-v", help="Silence mode.", default=False, action='store_true')

args = argparser.parse_args()

query = args.q
outfile = args.f
verbose = args.v

if os.name == 'nt':
    win_set_encode = Popen('win_encode.bat')
    stdout, stderr = p.communicate()

access_token = graph_fb.get_access_token()
search_result = graph_fb.search(query=query, token=access_token)

id_list = []
for place in search_result:
    id_list.append(place['id'])

with open('conf/fields.conf', 'r') as f:
    fields = f.read().splitlines()
    location_fields = {'city', 'state', 'country', 'street', 'zip', 'latitude', 'longitude'}

if outfile is not None:
    csvfile = open(outfile, 'w', encoding='utf8')
    csvwriter = csv.writer(csvfile, dialect='excel')

for place_id in id_list:
    page = graph_fb.get_page(place_id, token=access_token)
    result = []
    for field in fields:
        if field == 'email':
            html = graph_fb.get_raw_page(page.get('link', ''))
            result.append(graph_fb.extract_email(html))
        elif field in location_fields:
            result.append(page.get('location', {}).get('field', ''))
        else:
            result.append(page.get(field, ''))
        
    if outfile is not None:
        csvwriter.writerow(result)
        if verbose:
            print(result)
            print()

if outfile is not None:
    csvfile.close()
