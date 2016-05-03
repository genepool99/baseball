#!/usr/bin/env python 

import requests
import json

##
# Pull basic sabersim.com data from the API.
# Use the Oauth 2.0 token to access their endpoint.
# Not sure if this violates their TOS so use at your own risk!
##
def getData():
    email = "your@email.com"
    password = "somepassword"
    with requests.Session() as s:
        login_data = {'email':email, 'password':password}
        p = s.post('https://www.sabersim.com/auth/login', data=login_data)  # post to the auth server to get token
        return_data = json.loads(p.text)      
        # change this endpoint to get different sabersim data (like a different date)
        endpoint = "https://baseball-sim.appspot.com/_ah/api/mlb/v1/player/projection/list?date=2016-05-02&type=basic"
        headers = {"Authorization":"Bearer " + return_data['token']}
        r = s.get(endpoint, headers=headers)
        return r.text
   
print getData() 
