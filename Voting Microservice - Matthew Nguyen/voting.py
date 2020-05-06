import flask_api
import json
from flask import Flask, request, abort
from flask_api import status, exceptions
from flask_redis import Redis
from pprint import pprint

app = flask_api.FlaskAPI(__name__)
r = Redis(app)

# Home Page. Lists all keys. Shows all hashes in the allposts set.
# Sample curl request: curl -X GET http://localhost:5000/
@app.route('/', methods=['GET'])
def all_posts():
	return r.keys(), status.HTTP_200_OK

# Create a post in order to upvote/downvote it
# Sample curl request: curl -X POST http://localhost:5000/create -d "title=example_title&community=example_community&text=example_text"
@app.route('/create', methods=['GET', 'POST'])
def create_post():
	if request.method == 'GET':
		return list(r.smembers("allposts")), status.HTTP_200_OK
	elif request.method == 'POST':
		postid = r.incr("next_post_id")
		post_props = {
                        "post_id":"{}".format(postid),
                        "title":request.data["title"],
                        "community":request.data["community"],
                        "text":request.data["text"],
                        "upvote_count":0,
                        "downvote_count": 0,
                        "score": 0
                        }
		r.sadd("allposts","post{}".format(postid))
		r.hmset("post{}".format(postid), post_props)
		return {}, status.HTTP_201_CREATED

# Filters posts based on query parameters
# Sample curl request: curl -X GET 'http://localhost:5000/search?title=example_title&community=example_community&text=example_text'
@app.route('/search', methods=['GET'])
def post_filter():
	foundPosts = set()
	numberOfPosts = r.scard("allposts")
	for x in range(numberOfPosts):
		if (r.hget("post{}".format(x+1),"title").decode() == request.args.get("title") or \
		r.hget("post{}".format(x+1),"community").decode() == request.args.get("community") or \
		r.hget("post{}".format(x+1),"text").decode() == request.args.get("text")):
			foundPosts.add("post{}".format(x+1))
			
	if len(foundPosts) > 0:
		return list(foundPosts), status.HTTP_200_OK
	else:
		return "Post(s) not found", status.HTTP_404_NOT_FOUND

# List n top-scoring posts to any community
# Sample curl request: curl -X GET http://localhost:5000/top/1
@app.route('/top/<int:n>', methods=['GET'])
def return_top_n(n):
        return r.sort("allposts", start=0, num=n, by="*->score", desc=True), status.HTTP_200_OK\

# Report the number of upvotes and downvotes for a post using post id
# Sample curl request: curl -X GET http://localhost:5000/total/1
@app.route('/total/<int:id>', methods=['GET'])
def report_total(id):
	if (r.hgetall("post{}".format(id)) == {}):
		return "Post does not exist", status.HTTP_404_NOT_FOUND
	else:
		total_upvotes = r.hget("post{}".format(id),"upvote_count")
		total_downvotes = r.hget("post{}".format(id), "downvote_count")
		return {"upvote_total": total_upvotes, "downvote_total": total_downvotes}, status.HTTP_200_OK

# Upvote a post based on post ID
# Sample curl request: curl -X PUT http://localhost:5000/upvote/1
@app.route('/upvote/<int:id>', methods=['GET','PUT'])
def upvote(id):
	if request.method == 'GET':
		return r.hgetall("post{}".format(id)), status.HTTP_200_OK
	elif request.method == 'PUT':
		if (r.hgetall("post{}".format(id)) == {}):
			return "Post does not exist", status.HTTP_404_NOT_FOUND
		else:
			r.hincrby("post{}".format(id),"upvote_count", 1)
			r.hincrby("post{}".format(id),"score", 1)
			return {"upvote_count": r.hget("post{}".format(id),"upvote_count")}, status.HTTP_200_OK
	
# Downvote a post based on post ID
# Sample curl request: curl -X PUT http://localhost:5000/downvote/1
@app.route('/downvote/<int:id>', methods=['GET','PUT'])
def downvote(id):
	if request.method == 'GET':
		return r.hgetall("post{}".format(id)), status.HTTP_200_OK
	elif request.method == 'PUT':
		if (r.hgetall("post{}".format(id)) == {}):
			return "Post does not exist", status.HTTP_404_NOT_FOUND
		else:
			r.hincrby("post{}".format(id),"downvote_count", 1)
			r.hincrby("post{}".format(id),"score", -1)
			return {"downvote_count": r.hget("post{}".format(id),"downvote_count")}, status.HTTP_200_OK
