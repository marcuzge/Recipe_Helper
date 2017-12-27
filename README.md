# LEARNING.MD

## Deployed Application :https://final-project-temx.herokuapp.com/
## Deployed API : https://project-teamx-api.herokuapp.com/hotsearches
## routes available for app functions
* /index
* /
#### Both are home page which can view top searchs, searchs for recipes and direct to login/sign up
* /results
#### Seach for a recipe or an ingredient and display all the related search offering customer for future selection
* /recipe/<id>
#### View a particular recipe with detailed information including nutrition, ingredients, steps and picture. Also can access to nearby restaurant  offering the dish and shop on Amazon now to get ingredients ready for cooking.
* /sign_up
* /login
* /logout
* /account
#### View all the liked dishes 
* /like/{{id}}/{{name}}
#### Added a dish to user’s list 
* /unlike/{{id}}
#### Do the reverse -- delete from the user’s saved list 
* /search
#### Search nearby resturants 
## routes available for search metric API (Extra Credit)
* /postsearches
#### post a search to store as a metric
* /hotsearches
#### retrieve the top 5 searches
## A description of what your project does and the functionality that it provides
Our project can let users search recipes and return the steps, ingredients, nutrition. Users can signup and login to like this dish. Users can click the ingredients whick link to Amazon and buy these ingredients. If users don’t want to cook, they can get a list of nearby restaurants that provide this dish. These restaurants will be displayed on google map.
## A list of at least ten different web technologies that you used in your web application and where they are used
* Use Python Flask to build webserver and API.
* Use webserver to hit edamam Recipe API, Yelp API and GoogleMap API for GET request and POST request.
* Use Python SQLite package to Connect server to database.
* Use Python Google_map package to generate google map and display it on webpage.
* Use Python oauthlib2 package to configure the client_id and client_secrete to get the yelp api key.
* Load jQuery stick sidebar
* Build our own api to keep tracking search hits
* Use Amazon Prime Now to shop for fresh ingredients and save us from the grocery trip
* Use git to collaborate on different features, putting up pull requests for review and merges.
* Use jQeury for animation and a javascript library scrolly for scrolling in a single page
