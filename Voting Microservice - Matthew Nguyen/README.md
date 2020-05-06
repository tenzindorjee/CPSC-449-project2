# 449Project2
Voting microservice implemented using flaskapi and Redis by Matthew Nguyen

<b>Run these beforehand</b>:

sudo apt update

sudo apt install --yes redis python3-hiredis

pip3 install Flask

pip3 install Flask-API

pip3 install --user Flask-and-Redis



<b>Run with</b>:

flask run

<b>To clear the db, run</b>:

redis-cli

flushdb



<b>Endpoints</b>: 

http://localhost:5000/ - home page. View all posts

/total/&lt;int:id&gt; - Report the number of upvotes and downvotes for a post using post #

/create - create a post. requires title, community, text

/upvote/&lt;int:id&gt; - Upvote a post based on post #

/downvote/&lt;int:id&gt; - Downvote a post based on post #

/top/&lt;int:n&gt; - List n top-scoring posts to any community

/search/?&lt;queryparameter1&gt;&&lt;queryparameter2&gt;&... - Filters posts based on query parameters
