from dispatch_requests_in_parallel import dispatch_requests_in_parallel
from pprint import pprint
import json

def make_polymer_adjustments(adjustments):
	for adjustment in adjustments:
		pprint(adjustment)
		adjustment_url = 'https://eszlr18ifi.execute-api.us-west-1.amazonaws.com/staging/ics/v11/adjustments/'
		headers = {'Content-type' : 'application/json'}
		dispatch_requests_in_parallel([adjustment_url], headers, 'POST', json.dumps(adjustment))


def update_begin_time(most_recent_time):
	print ('DB request to update begin_time:' + most_recent_time)


def get_begin_time(polymer_team_id):
	return '2017-12-01T00:00:00-08:00'