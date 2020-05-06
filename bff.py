from flask import Flask
import requests
from feedgen.feed import FeedGenerator

app = Flask(__name__)

@app.route('/<string:community>/<int:amount>')
def ParticularRecent(amount,community):
	newRoute = 'http://127.0.0.1:5000/api/v1.0/resources/collections/recent?community=' + community + '&amount=' +str(amount)
	
	response = requests.get(newRoute)
	jsonDict = response.json()
	
	fg = FeedGenerator()
	fg.id('http://127.0.0.1:5100/<string:community>')
	fg.link(href='http://127.0.0.1:5100/<string:community>', rel='alternate')
	fg.title('25 recent post for particular community')
	fg.language('en')
	fg.description('printing the top 25 recent post for a particular community!')

	for post in jsonDict:
	
		fe = fg.add_entry()
		fe.title(post['title'])
		fe.author( {'name':post['username'],'email':'john@example.de'})
		fe.id(post['community'])
		
	results = fg.rss_str(pretty=True)
	return results

@app.route('/any/<int:amount>')
def any(amount):
	newRoute = 'http://127.0.0.1:5000/api/v1.0/resources/collections/any?amount='+ str(amount)
	response1 = requests.get(newRoute)
	jsonDict1 = response1.json()

	fg = FeedGenerator()
	fg.id('http://127.0.0.1:5100/any/<int:amount>')
	fg.link(href='http://127.0.0.1:5100/any/<int:amount>', rel='alternate')
	fg.title('25 recent post for any community')
	fg.language('en')
	fg.description('printing the top 25 recent post for any community!')

	for post in jsonDict1:
		fe = fg.add_entry()
		fe.title(post['title'])
		fe.author( {'name':post['username'],'email':'john@example.de'})
		fe.id(post['community'])
	
	results = fg.rss_str(pretty=True)
	return results


	
