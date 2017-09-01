#! python 3.6
# fetch the potw from nasa's web site

"""
TODO to make the script work :
Complete the variables in the main function 

api_key = Your nasa's api access keys
path = the path of the folder you want to save the picture to

To post to slack, you must insert your webhook in the "post_payload" function
if you want to disable the slack posting just comment the call in the main function.

"""
# imports

import os
from urllib.request import urlopen
import time
import json
import requests

# subroutines


def get_json(url):
    response = urlopen(url)
    return json.load(response)


def fetch_url(url, path):
    make_dir(path)
    print("Checking folder path ...")
    print("Getting img's URL ...")
    decoded = get_json(url)
    pic_url = decoded["url"]
    r = requests.get(pic_url)
    print("Img's fetched ... Writting !")
    name = str(time.time()) + ".png"
    print("Switching directory for saving ...")
    os.chdir(path)
    with open(name, 'wb') as f:
        f.write(r.content)
    print("New img has been written to " + path + " It's called : " + name)


def make_dir(dirPath):
    #create dir if it doesn't already exist
    if(os.path.isdir(dirPath)):
        pass
    else:
        os.makedir(dirPath)


def create_payload(json_data):
    payload = {'text': json_data["title"] + "\n" + json_data["url"] + "\n" + json_data["date"]}
    return payload


def post_payload(payload):
    if payload != {}:
        webhook_url = "Insert_Here_Your_Slack_Webhook" #TODO
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is : %s' % (response.status_code, response.text))
            return False
        else:
            return True


def to_slack(url):
    my_payload = create_payload(get_json(url))
    status = post_payload(my_payload)
    if status:
        print("payload posted")
    else:
        print("it ain't working")

# main
if __name__ == "__main__":
    api_key = "Insert_Here_Your_Nasa_Api_Key" #TODO
    path = r"Insert_Here_The_path_of_the_folder_where_you_want_to_save_the_pictures" #TODO
    url = "https://api.nasa.gov/planetary/apod" + "?api_key=" + api_key
    fetch_url(url, path)
    to_slack(url) # To comment if you want to disable slack posting
    exit(0)