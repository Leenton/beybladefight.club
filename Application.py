from flask import Flask, render_template, url_for, redirect, request, session
import SessionManager
import secrets
from datetime import datetime
import os
import random

app = Flask(__name__)

app.config['SECRET_KEY'] = "684a2c31fa1f159e791fbd0d01e4214c58b1ba170543bd7085dd61c934hg7180"
tournament_day = 1654014157 

def session_check():
    try:
        temp = session["SessionID"]
        del temp
    except:
        session["SessionID"] = secrets.token_hex(64)

#Log the IP addresses of the people who visit the site. 

def log_ip(ip):
    file_object = open('iplog.txt', 'a')
    file_object.write((ip + "\n"))
    file_object.close()

#Log the names of people who sign up to the tournament. 

def log_participant(name):
    file_object = open('participant.txt', 'a')
    file_object.write((name + "\n"))
    file_object.close()




@app.route("/",  methods=["GET","POST"])
def home():
    session_check()
    log_ip(request.remote_addr)

    #If the date of the tournament has passed, return a message saying you missed this event

    if(datetime.utcnow() > datetime.fromtimestamp(tournament_day)):
        return "You missed this event, loser."



    #If it is a post request we know it's some one either clicking yes they will come or no they wont. Based on their response set what their cowardince is.

    if request.method == "POST":
        try:
            if(request.form["Response"] == "I will"):
                SessionManager.set_cowardice(session["SessionID"], "No")
            else:
                SessionManager.set_cowardice(session["SessionID"], "Yes")
                return redirect('https://letmegooglethat.com/?q=How+do+I+stop+being+a+coward%3F',code=302)
        except:
            return "This is for fun and games, don't try to break this shit mate."
        
  

    #Return a different page based on what type of coward someone is.

    if(SessionManager.is_a_coward(session["SessionID"]) == "Yes"):
        return "Cowards are not allowed here"
    elif(SessionManager.is_a_coward(session["SessionID"]) == "Never visted"):
        return render_template("home.html")
    return redirect(url_for("rules"))




@app.route("/rules",  methods=["GET","POST"])
def rules():
    log_ip(request.remote_addr)
    session_check()

    gifs = os.listdir(".//static//gifs")
    gif = gifs[random.randint(0,(len(gifs)) - 1)]

    #Handle post requests, if a post is sent it's someone setting a name, names must be less than 257 charcters. Else drop the request to set a name.

    if request.method == "POST":
        try:
            print(request.form["name"])
            
            if(len(request.form["name"]) < 257):
                SessionManager.set_name(session["SessionID"], request.form["name"])
                log_participant(request.form["name"])
            else:
                return render_template("rules.html", state="Your name is too long, shorten it a bit mate, this site has TOP notch security, don't think you can enter some bullshit to try and break it.", gif=gif) 
        except:
            return "This is for fun and games, don't break this shit mate."

    
    #Render the page based on what what type of person has tried to visit the page. 

    if(SessionManager.is_a_coward(session["SessionID"]) == "Yes"):
        return "Cowards are not allowed here"
    elif(SessionManager.is_a_coward(session["SessionID"]) == "Never visted"):
        gifs = os.listdir(".//static//gifs")
        print(gifs)
        gif = gifs[random.randint(0,(len(gifs)) - 1)]
        return render_template("rules.html", state="not registered", gif=gif)
    if(SessionManager.has_set_name(session["SessionID"])):
        return render_template("rules.html", state="registered")
    return render_template("rules.html", state="not registered", gif=gif) 
    


#A link to the PNG with the bracekts  

@app.route("/bracket",  methods=["GET"])
def bracket():
    return "LINK TO BRACKET"

#Legaly required privacy page

@app.route("/privacy",  methods=['GET'])
def privacy():
    log_ip((request.remote_addr))
    return "We log your IP address and sell it to the Russians for Yu Gi Oh cards. Your names we sell to somalian priates for 5% discounts at Thai Hut.\nIn actually we store your IP adress and name so we know who you are so we can add you to the tournament bracket, if you wish to be removed from our database and be forgotten please send an email to leenton.chinyanga@futurenet.com who will delete any refrences to yourself from all locations."

if __name__ == "__main__":
    app.run(use_reloader=False, host= '0.0.0.0', debug=True)