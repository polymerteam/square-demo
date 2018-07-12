import json
import grequests
from threading import RLock
from pprint import pprint
mutex = RLock()

# GLOBALS
downloaded_data_array = []

# Store data, using a mutex lock to prevent race conditions
def getAuthorJSON(response, *args, **kwargs):
	mutex.acquire()
	try:
		downloaded_data_array.append(json.loads(response.content))
		if response.status_code is not 200:
			pprint(response.content)
			raise Exception("ASYNC DOWNLOAD failed with status %d: %s" % (response.status_code, response.url))
		print "FINISHED DOWNLOADING FROM: " + response.url
	finally:
		mutex.release()


def exception_handler(request, exception):
	raise Exception(exception)


# Main function
def fetch_urls_async(urls_to_fetch, headers):
	unsent_requests = []
	for url in urls_to_fetch:
		unsent_requests.append(grequests.get(url, hooks={'response': getAuthorJSON}, headers=headers))
	# NOTE FOR FUTURE IMPROVEMENTS: Square Connect V1 throws a 429 if more than size=4 requests are made in a burst
	# This is fine if you have <= 4 urls (stores, in our case), but not optimal for LOTS of stores.
	# Dandelion's 8 stores take 4 seconds to run the entire script on my laptop.
	grequests.map(unsent_requests, exception_handler=exception_handler, size=4)  # actually make requests
	return downloaded_data_array

