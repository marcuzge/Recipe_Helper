"""
webserver.py

File that is the central location of code for your webserver.
"""

import re
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json

from flask import Flask, render_template, request, session
import requests
import os
import sqlite3
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
# Create application, and point static path (where static resources like images, css, and js files are stored) to the
# "static folder"
app = Flask(__name__,static_url_path="/static")
app.secret_key = "super secret key"
GoogleMaps(app, key="") #fill-in
GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

def get_connection():
    return sqlite3.connect('users.db')

def create_links_table():
    conn = get_connection()

    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (name text, password text, email text PRIMARY KEY, question text, answer text )")
    c.execute("CREATE TABLE IF NOT EXISTS likes (id text, email text, name text )")
    conn.commit()
    conn.close()
app = Flask(__name__,static_url_path="/static")
GoogleMaps(app, key="") #fill-in

app.config.from_object(__name__)
app.secret_key = "super secret key"
# Session(app)
create_links_table()
search_engine_api= "https://project-teamx-api.herokuapp.com/" #subject to change 
def get_top_search():

    return_top5searches = requests.get(search_engine_api+"hotsearches")
    recipe_data = return_top5searches.json()
    return recipe_data
def post_search(food):
    data = {'recipe':food}
    requests.post(search_engine_api+"postsearches",data=json.dumps(data),headers={'Content-Type':'application/json'})
    return
@app.route('/')
def index_page():
    """
    If someone goes to the root of your website (i.e. http://localhost:5000/), run this function. The string that this
    returns will be sent to the browser
    """
    return render_template("index.html", data = get_top_search()) # Render the template located in "templates/index.html"

@app.route('/index')
def index():

    return render_template("index.html",data = get_top_search()) 


@app.route('/results', methods=['GET'])
def results():
    searchInput = request.args.get("searchInput")
    choice = request.args.get("choice")
    post_search(searchInput)
    params = {
        'q': searchInput, # doesn't work if switched to searchInput
        'app_id': '8d20f746', #add api_id
        'app_key': '', #add app_key
        'from': '0',
        'to': '24'
    }

    res = requests.get('https://api.edamam.com/search', params=params).json()


    return render_template("results.html", contents = res['hits'])
def isInLikeList(id):
    if 'email' not in session.keys() or session['email'] == None:
        return False
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, email  FROM likes WHERE email = ? and id = ?;",[session['email'], id])
    likes = c.fetchall()
    return len(likes)>0

@app.route('/recipe/<id>', methods=['GET'])
def show(id):

    # url = 'http://www.edamam.com/ontologies/edamam.owl%23recipe_' + id
    session['id'] = id;
    param = {
        'q': id, 
        'app_id': '8d20f746', #add api_id
        'app_key': '', #add a
    }
  
    dish = requests.get('https://api.edamam.com/search', params=param).json()

    return render_template("show.html", dish=dish['hits'][0]['recipe'], id = id , like= isInLikeList(id))


@app.route('/sign_up', methods=['GET'])
def show_sign():
    return render_template("sign_up.html")

def valid(name,email,password,question,answer):
    if name == None or email == None or password == None or question == None or answer ==None:
        return False
    if len(name) ==0 or len(email) ==0 or len(password)==0 or len(question) ==0 or len(answer) ==0:
        return False
    return True
def exist(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? ;",[email])
    links = c.fetchall()
    return len(links) != 0

@app.route('/sign_up', methods=['POST'])
def sign_up():
    name = request.form.get("username").strip()
    email = request.form.get("email").strip()

    password = request.form.get("password").strip()
    question = request.form.get("question")
    answer = request.form.get("answer").strip()
    if not valid(name,email,password,question,answer):
        return render_template("sign_up.html", notification = "not enough information")
    if exist(email):
        return render_template("sign_up.html", notification = "email is use")
    conn = get_connection()
    c = conn.cursor()
    c.execute( "INSERT INTO users (name, password, email, question, answer)VALUES(?,?,?,?,?);", [name, password,email,question,answer])
    session['user']=name
    session['email']=email
    conn.commit()
    conn.close()
    return render_template("index.html")
@app.route('/login', methods=['GET'])
def show_login():
    session['user']=None
    session['email']=None
    return render_template("login.html")
def get_user(email,password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT password, name  FROM users WHERE email = ? ;",[email])
    links = c.fetchall()
    if len(links) == 0:
        return None
    if password == links[0][0]:
     
        return links[0][1]
    return None
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("email").strip()
    password = request.form.get("password").strip()
    user = get_user(email,password);
    if user == None:
        return render_template("login.html",notification="invalid combination")

    session['user']=user
    session['email']=email

    return render_template("index.html", notification="Welcome Back, "+user)
@app.route('/logout', methods=['GET'])
def logout():
    session['user']=None
    session['email']=None
    return render_template("index.html")

def getLikes(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM likes WHERE email = ?;",[email])
    likes = c.fetchall()
    return likes

@app.route('/account',methods=['GET'])
def view_account():
    if session['user'] == None:
        return render_template("login.html")
    lists = getLikes(session['email'])
    return render_template("account.html", likes = lists)

def add_like(email,id,name):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, email  FROM likes WHERE email = ? and id = ?;",[email, id])
    likes = c.fetchall()
    if len(likes)>0:
        return
    c.execute( "INSERT INTO likes (email, id, name)VALUES(?,?,?);", [email,id, name])
    conn.commit()
    conn.close()

@app.route('/like/<id>/<name>',methods=['GET'])
def like(id,name):
    if session['user'] == None:
        return render_template("login.html")
    add_like(session['email'],id,name)
    return show(id)
    
def dis_like(email,id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM likes WHERE email = ? and id = ?;",[email, id])
    conn.commit()
    conn.close()

@app.route('/unlike/<id>',methods=['GET'])
def unlike(id):
    if session['user'] == None:
        return render_template("login.html")
    dis_like(session['email'],id)
    return show(id)


@app.route('/search', methods = ["GET","POST"])
def search_res():
#get the value of the form from previous webpage
    food_name = request.form.get("searchfood")


#Fill app key details from Yelp
    client_id = 'B5riMw77DRaQxQigXFy9yA'
    client_secret = '' #fill-in
#Authenticate and get access token
    client = BackendApplicationClient(client_id=client_id)
    yelp = OAuth2Session(client=client)
    token = yelp.fetch_token(token_url='https://api.yelp.com/oauth2/token', client_id=client_id, client_secret=client_secret)
#Construct custom Authentication header
#Can use a better way to access the token string from returned unicode JSON. This is quick and dirty

    tokenstring = str(token)
    json_acceptable_string = tokenstring.replace("'", "\"")
    d = json.loads(json_acceptable_string)
    
    authhead = "Bearer " + d['access_token']
    head = {'Authorization': authhead}
    markers = []
    r = requests.post('https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBaOUgQxXFWx8Eoefb3thEBki23folImKk')
    if r.status_code == requests.codes.ok:
        current_location = r.json()['location']


    params = {'latlng': str(current_location['lat'])+','+str(current_location['lng'])}
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res =req.json()
    result = res['results'][0]


    for address_component in result['address_components']:
        if address_component['types'][0] == "locality":
            current_city = address_component['long_name']
        if address_component['types'][0] == "administrative_area_level_1":
            current_state = address_component['long_name']



#Call needed yelp endpoint with custom header using requests module
    # r = requests.get("https://api.yelp.com/v3/businesses/search?term=mapotofu&location=berkeley", headers= head)
    r = requests.get("https://api.yelp.com/v3/businesses/search?"+ "term="+ str(food_name) +"&location=" + str(current_city), headers= head)

    datas = r.json()
    return_data = list()


    i=1
    for data in datas["businesses"]:
        data_dict = dict()
        data_dict['index'] = i
        data_dict["name"] = data["name"]
        data_dict["rating"] = data["rating"]
        data_dict["location"] = data["location"]
        data_dict["display_phone"] = data["display_phone"]
        data_dict["image_url"] = data["image_url"]
        data_dict["review_count"] = data["review_count"]
        data_dict["categories"] = data["categories"]
        data_dict["coordinates"] = data["coordinates"]
        data_dict["url"] = data["url"]
        #why there is a keyError in price
        if "price" in data.keys():
            data_dict["price"] = data["price"]

        marker = {
            'icon': 'http://maps.google.com/mapfiles/kml/paddle/'+str(i)+'.png',
            'lat': data_dict['coordinates']['latitude'],
            'lng': data_dict['coordinates']['longitude'],
        }
        markers.append(marker)
        i=i+1

        return_data.append(data_dict)

    
    mymap = Map(
        identifier="view-side",
        lat = current_location['lat'],
        lng = current_location['lng'],
        markers= markers,
        style=(
            "height:400px;"
            "width:400px;"
            "float:right;"
        ),
        fit_markers_to_bounds = True,
        zoom = 11)
    return render_template("Restaurants_Nearby.html",mymap = mymap, restaurants = return_data, food_name=food_name)





