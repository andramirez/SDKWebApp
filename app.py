import flask, random, os, tweepy, json, requests

app = flask.Flask(__name__)

@app.route('/')



def index():
#****************************************************GITHUB****************************************
    phrases = ['nature', 'beauty', 'animals']
    phrase = random.choice(phrases)
    #search url to bring up certain images based on query
    search_url="https://api.gettyimages.com:443/v3/search/images?exclude_nudity=true&file_types=jpg&minimum_size=large&orientations=Horizontal&sort_order=best_match&number_of_people=none&phrase=" + phrase
    
    # search_url = "https://api.gettyimages.com:443/v3/search/images?phrase=star%20trek%20the%20original%20series"
    #api key
    # key = os.getenv("getty_key")
    headers1 = {'Api-Key': '42hg9wahfqwvspm4dwa2vs7g'}
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
    
    #keys and access token
    con_key = "qit0BAiTrTwmBsJ3AOpQnenGZ"
    sec_con_key = "reVX2c8hiJhT8rY5bXVMV0lrrtXyjHcLonYynmtHJECAMB5KIY"
    acc_token = "824355548501987328-slJGgxFlWbfetxRZdN3iutYTA21tg7v"
    acc_token_sec = "8L8HuqrVJY9ZM9ezb8R2NaCw2kmEBTJRHO82Js98JCnrp"
    
    users = ['experiencedquot', 'QuotesDetail', '_Famouss_Quotes', 'quotedefamous', 'motivational', 'philosophy_muse']
    user = random.choice(users)
    
    #tweepy config
    auth = tweepy.OAuthHandler(con_key, sec_con_key)
    auth.set_access_token(acc_token, acc_token_sec)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    tweets = api.user_timeline( 
                                screen_name=user,
                                count = 200,
                                lang = "en")
    tweet1 = random.choice(tweets)
    while "https" in tweet1.text:
        tweet1 = random.choice(tweets)
        
    return flask.render_template("index.html", text = tweet1.text, author = user, image = image1) ## sends tweet and image to html page via flask
    
    
app.run(
    port = int(os.getenv('PORT',8080)),
    host = os.getenv('IP','0.0.0.0'),
    debug = True
)