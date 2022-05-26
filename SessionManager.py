import time
import re

#from flask import session

sessions = {}

def is_a_coward(session_id):
    try:
        if(sessions[session_id]):
          return sessions[session_id]["cowardlyness"]
    except:
        sessions[session_id] = {"cowardlyness" : "Never visted", "name" : ""}
        return sessions[session_id]["cowardlyness"]

    
    

def set_cowardice(session_id, response):
    sessions[session_id] = {"cowardlyness" : response, "name" : ""}
    



def has_set_name(session_id):
    if(sessions[session_id]["name"]):
        return True
    return False




def set_name(session_id, name):
    sessions[session_id]["name"] = name