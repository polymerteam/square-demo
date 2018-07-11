import json
import grequests 
from threading import RLock
mutex = RLock()

# GLOBALS
downloaded_data_array = []

# Store data, using a mutex lock to prevent race conditions
def getAuthorJSON(response, *args, **kwargs):
	mutex.acquire()
	try:
		downloaded_data_array.append(json.loads(response.content))
		print "DONE: " + response.url
	finally:
		mutex.release()


def exception_handler(request, exception):
	print "ERROR: request failed: " + request.url + "<<<<<<<"
	print ("Request error: {0}".format(exception))


# Main function
def fetch_urls_async(urls_to_fetch, headers):
	unsent_requests = []
	for url in urls_to_fetch:
		unsent_requests.append(grequests.get(url, hooks={'response': getAuthorJSON}, headers=headers))
	# All urls have finished downloading after this line
	grequests.map(unsent_requests, exception_handler=exception_handler)  # actually make requests
	return downloaded_data_array
