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
	# NOTE FOR FUTURE IMPROVEMENTS: Square Connect V1 throws a 429 for size > number_of_requests_at_once.
	# This is fine if you have urls_to_fetch <= number_of_requests_at_once (each url is a 'locations', in our case).
	# Dandelion for example, has 8 'locations' on square.
	number_of_requests_at_once = 3
	# Actually make requests, holds at line until all threads finish:
	grequests.map(unsent_requests, exception_handler=exception_handler, size=number_of_requests_at_once)
	return downloaded_data_array

