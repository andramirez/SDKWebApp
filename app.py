# Name: Andrea Ramirez
# Title: app.py (Project 1)
# Description: This project is a Web App that uses the following toolchains: Getty Images, 
#               Flask, c9, Github, Twitter, and Heroku to create a web page that dynamically 
#               produces images (from Getty images) and quotes (from twitter) that are connected
#               by an overall theme. 
# Date: 02/06/17

# Github repo: https://github.com/CSUMB-SP17-CST438/andramirez
# C9 Workspace: https://ide.c9.io/drearam3/andramirez
# Heroku Site: https://arcane-cove-98216.herokuapp.com/


import flask, random, os, tweepy, json, requests

app = flask.Flask(__name__)

@app.route('/')

def index():
#****************************************************GITHUB****************************************
    phrases = ['Stephen%20King', 'JK%20Rowling', 'william%20Shakespear', 'Aldous%20Huxley', 'dr%20seuss']
    
    phrase = random.choice(phrases)
    #search url to bring up certain images based on query
    search_url="https://api.gettyimages.com:443/v3/search/images?exclude_nudity=true&file_types=jpg&minimum_size=large&orientations=Horizontal&sort_order=best_match&phrase=" + phrase

    #getty api key
    headers1 = {'Api-Key': os.getenv("getty_key")}

    #result of image search
    result = requests.get(search_url, headers=headers1)
    #result in json to get page ID
    data = result.json()
    #randomizing what image is displayed
    num = random.randint(0,(len(data[u'images'])-1))
    #getting ID num from json text
    data = data[u'images'][num]
    data = data[u'id']
    #link to image
    image1 = "http://media.gettyimages.com/photos/-id" + data

#****************************************************************************************************      
    
    #twitter API keys and tokens
    con_key = os.getenv("twitterkey")
    sec_con_key = os.getenv("twitterkey_sec")
    acc_token = os.getenv("twitter_token")
    acc_token_sec = os.getenv("twitter_token_sec")
    
    #twitter user names chosen by getty image search phrase
    if 'Stephen%20King' in phrase: 
        users = ['S_KingQuotes', 'SKing_Quotes']
        user = random.choice(users)
    if 'JK%20Rowling' in phrase:
        user = 'jkrowlingquotes'
    if 'william%20Shakespear' in phrase:
        users = ['DailyShakes', 'Wwm_Shakespeare']
        user = random.choice(users)
    if 'Aldous%20Huxley' in phrase: 
        user = 'AHuxleyQuote'
    if 'dr%20seuss' in phrase:
        users = ['makelifesimmple', 'DrSeussQuotes__', 'DrSeuss_Quotes']
        user = random.choice(users)
        
    
    #tweepy config
    auth = tweepy.OAuthHandler(con_key, sec_con_key)
    auth.set_access_token(acc_token, acc_token_sec)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    #REST API
    tweets = api.user_timeline( 
                                screen_name=user,
                                count = 200,
                                lang = "en")
    tweet1 = random.choice(tweets) # choose random tweets

    while "http" in tweet1.text: #checks to make sure that tweet doesn't have an image
        tweet1 = random.choice(tweets) # choose random tweets
    
    url = user + "/status/"+ tweet1.id_str
    
    #template returned to html page    
    return flask.render_template("index.html", text = tweet1.text, author = user, link = url, image = image1) ## sends tweet and image to html page via flask
    
##Flask run app    
app.run(
    port = int(os.getenv('PORT',8080)),
    host = os.getenv('IP','0.0.0.0'),
)