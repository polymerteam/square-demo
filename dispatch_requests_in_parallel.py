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
		status_code = response.status_code
		if status_code is not 200 and status_code is not 201:  # GET and POST status codes
			pprint(response.content)
			raise Exception("ASYNC DOWNLOAD failed with status %d: %s" % (response.status_code, response.url))
		print "COMPLETED REQUEST TO: " + response.url
	finally:
		mutex.release()


def exception_handler(request, exception):
	raise Exception(exception)


# Main function
def dispatch_requests_in_parallel(urls_to_fetch, headers, method='GET', data=None):
	unsent_requests = []
	for url in urls_to_fetch:
		if method == 'GET':
			unsent_requests.append(grequests.get(url, hooks={'response': getAuthorJSON}, headers=headers))
		elif method == 'POST':
			unsent_requests.append(grequests.post(url, hooks={'response': getAuthorJSON}, headers=headers, data=data))
	# NOTE FOR FUTURE IMPROVEMENTS: Square Connect V1 throws a 429 for size > number_of_requests_at_once.
	# This is fine if you have urls_to_fetch <= number_of_requests_at_once (each url is a 'locations', in our case).
	# Dandelion for example, has 8 'locations' on square.
	number_of_requests_at_once = 3
	# Actually make requests, holds at line until all threads finish:
	grequests.map(unsent_requests, exception_handler=exception_handler, size=number_of_requests_at_once)
	return downloaded_data_array
