from dispatch_requests_in_parallel import dispatch_requests_in_parallel
import json
import requests

POLYMER_SQUARE_ENDPOINT = 'http://0.0.0.0:8000/ics/v11/adjustments/square/'
HEADERS = {'Content-type': 'application/json'}


def make_polymer_adjustments(inventory_changes):
	dispatch_requests_in_parallel([POLYMER_SQUARE_ENDPOINT], HEADERS, 'POST', json.dumps(inventory_changes))


def get_last_square_sync_times():
	url = POLYMER_SQUARE_ENDPOINT + 'update-times/'
	team_update_times = requests.get(url).json()

	last_square_sync_times = {}
	for team_update_time in team_update_times:
		last_square_sync_times[team_update_time['id']] = team_update_time['last_synced_with_square_at']
	return last_square_sync_times
