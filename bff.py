from flask import Flask
import requests
from feedgen.feed import FeedGenerator

app = Flask(__name__)

@app.route('/<string:community>/<int:amount>')
def ParticularRecent(amount,community):
	# newRoute = '127.0.0.1:5000/api/v1.0/resources/collections/recent?community=' + community + '&amount=' +str(amount)
	newRoute = 'http://127.0.0.1:5000/api/v1.0/resources/collections/recent?community=CSUF&amount=15'
	
	response = requests.get(newRoute)
	jsonDict = response.json()
	
	fg = FeedGenerator()
	fg.id('http://127.0.0.1:5100/<string:community>')
	fg.link(href='http://127.0.0.1:5100/<string:community>', rel='alternate')
	fg.title('25 recent post for particular community')
	fg.language('en')
	fg.description('printing the top 25 recent post for a particular community!')

	counter = 0
	for post in jsonDict:
		fe = fg.add_entry()
		fe.title(post['title'])
		# fe.author(post['username'])
		# fe.description(post['text'])
		counter += 1

	
	results = fg.rss_str(pretty=True)
	
	return results
	