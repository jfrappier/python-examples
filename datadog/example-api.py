# Query Datadog API for count of hits on URL based on redirect file/JSON
import shutil
import json
import requests
import os
import time

# Getnerate time right now in EPOCH format, subtract 30 days (in milliseconds)
right_now = int(time.time() * 1000)
back_then = (right_now - 2592000000)

# Todo - prompt for HTTP code - current hard coded as 308 for redirect
# May be useful to get destination address has HTTP 200 to compare traffic and
# traffic from the old URL

# Requires environment variable to be set to these keys
# Todo - get from HVS? Would still require HCP service principal keys to be set
DD_API_KEY = os.getenv('DD_API_KEY')
DD_APP_KEY = os.getenv('DD_APP_KEY')

# Define the URL
url = "https://api.datadoghq.com/api/v2/logs/analytics/aggregate"

# Define the headers
headers = {
    "Content-Type": "application/json",
    "DD-API-KEY": DD_API_KEY,
    "DD-APPLICATION-KEY": DD_APP_KEY
}

# Initialize a session
session = requests.Session()
session.headers.update(headers)

# Get copy of current redirect and build data
# Update your source/destination. Could probably get right from tutorials repo
# in raw format
shutil.copyfile('/source/path/redirects.json', '/destination/path/redirects.json')

file = open('redirects.json')
redirects = json.load(file)

for redirect in redirects:
    source = redirect["source"]
    destination = redirect["destination"]
    permanent = redirect["permanent"]

    # Define the data payload
    data = {
        "compute": [
            {
                "metric": "count",
                "aggregation": "count",
                "type": "total"
            }
        ],
        "filter": {
            "query": ""+source+" GET 308",
            "from": back_then,
            "to": right_now,
            "indexes": ["*"]
        },
        "group_by": []
    }

    if "vault/" in source:
        print("Source: " + source)
        #print(f"Destination: {destination}")
        #print(f"data: {data}")
        #print(f"header: {headers}")
        #print(json.dumps(data))
        # Make the POST request
        try:
            response = session.post(url, json=data, timeout=30)
            response.raise_for_status()  # Raise an exception for HTTP errors
            print("Response JSON:", response.json())
        except requests.exceptions.Timeout:
            print("Request timed out")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Close the session
session.close()
