This conf/ directory contains 3 configuration files:
1. app_id_secret.conf
2. access_token.conf
3. fields.conf

app_id_secret.conf contains the app ID and secret of your Facebook app, the first line being the app ID and the second being thesecret.

access_token.conf contains the access token assigned by Facebook. If this file is missing, app_id_secret.conf will be used to generate a new access_token. Therefore, at least one of the two files must be present for the program to run properly.

fields.conf covers all the fields that will be scraped from Facebook and saved. Each field should be one separate line.

Available fields:
id
about
email
category
checkins
description
likes
link
city
country
latitude
longitude
street
zip
name
phone
public_transit
username
website
founded
