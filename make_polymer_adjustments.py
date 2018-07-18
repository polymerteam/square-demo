from make_request import make_request
import json

POLYMER_DB = 'http://0.0.0.0:8000'
POLYMER_SQUARE_ENDPOINT = POLYMER_DB + '/ics/v11/adjustments/square/'  # get: last update times, post: adjustments
HEADERS = {'Content-type': 'application/json'}


def make_polymer_adjustments(inventory_changes):
	make_request(POLYMER_SQUARE_ENDPOINT, HEADERS, 'POST', json.dumps(inventory_changes))


def get_last_square_sync_times():
	url = POLYMER_SQUARE_ENDPOINT + 'update-times/'
	team_update_times = make_request(url)

	last_square_sync_times = {}
	for team_update_time in team_update_times:
		last_square_sync_times[team_update_time['id']] = team_update_time['last_synced_with_square_at']
	return last_square_sync_times
