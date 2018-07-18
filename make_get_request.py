import requests

def make_get_request(url, headers={}):
	res = requests.get(url, headers=headers)
	if res.status_code != requests.codes.ok:
		raise Exception("Get request failed with status %d: %s" % (res.status_code, res.text))
	else:
		print "COMPLETED REQUEST TO: " + url
		return res.json()
