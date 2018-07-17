from dispatch_requests_in_parallel import dispatch_requests_in_parallel
from pprint import pprint
import json

POLYMER_SQUARE_ENDPOINT = 'http://0.0.0.0:8000/ics/v11/adjustments/square/'
HEADERS = {'Content-type': 'application/json'}


def make_polymer_adjustments(adjustments):
	pprint(adjustments)
	# dispatch_requests_in_parallel([POLYMER_SQUARE_ENDPOINT], HEADERS, 'POST', json.dumps(adjustments))


def get_last_square_sync_times():
	url = POLYMER_SQUARE_ENDPOINT + 'update-times/'
	team_update_times = dispatch_requests_in_parallel([url], HEADERS, 'GET')[0]

	last_square_sync_times = {}
	for team_update_time in team_update_times:
		last_square_sync_times[team_update_time['id']] = team_update_time['last_synced_with_square_at']
	return last_square_sync_times




def update_begin_time(most_recent_time):
	print ('DB request to update begin_time:' + most_recent_time)


def get_begin_time(polymer_team_id):
	return '2017-12-01T00:00:00-08:00'