from flask import Flask 
import requests
from feedgen.feed import FeedGenerator

app = Flask(__name__)

@app.route('/<string:community>/<int:amount>')
def ParticularRecent(amount,community):
	newRoute = '/api/v1.0/resources/collections/recent' + '/' + community + '/' +amount
	getStuff = requests.get(newRoute)

	jsonDict = getStuff.json()

	fg = FeedGenerator()
	fg.id('http://127.0.0.1:5000/<string:community>')
	fg.title('25 recent post for particular community')
	fg.language('en')

	counter = 0

	while (counter<amount):
		fe = fg.add_entry()
		fe.id(jsonDict['postID'][counter])
		fe.title(jsonDict['title'][counter])
		fe.author(jsonDict['username'][counter])
		fe.description(jsonDict['text'][counter])
		fe.link(jsonDict['url'][counter])
		counter+=1

	 
	results = fg.rss_str(pretty=True)
	return results
	