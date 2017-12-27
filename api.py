from flask import Flask, render_template, request
import sqlite3
import requests
import json

def get_connection():
	return sqlite3.connect('searches.db')

def create_links_table():
	conn = get_connection()
	c = conn.cursor()

	c.execute('CREATE TABLE IF NOT EXISTS searches (recipe TEXT);')
	c.execute('INSERT INTO searches (recipe) VALUES (?);', ["chicken"])
	conn.commit()
	conn.close()

app = Flask(__name__,static_url_path="/static")
create_links_table()


@app.route('/postsearches', methods = ['POST'])
def Post_searches():
	request_data = request.get_json()
	recipe = request_data['recipe']
	conn = get_connection()
	c = conn.cursor()
	c.execute('INSERT INTO searches (recipe) VALUES (?);', [recipe])
	print(recipe+" inserted")
	conn.commit()
	result = {"message":"success"}
	return json.dumps(result)

@app.route('/hotsearches', methods = ['GET'])
def Get_top5searches():

	conn = get_connection()
	c = conn.cursor()

	c.execute("SELECT recipe, COUNT (*) count FROM searches GROUP BY recipe ORDER BY count desc LIMIT 4;")

	recipes = c.fetchall()
	request_recipes = list()
	# for recipe in recipes:
	# 	request_recipes = dict()
	for i in range (0,len(recipes)):
		request_recipe = recipes[i]
		request_recipes.append(request_recipe)

	return json.dumps(request_recipes)