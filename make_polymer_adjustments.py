from pprint import pprint


def make_polymer_adjustments(adjustments):
	for adjustment in adjustments:
		pprint(adjustment)


def update_begin_time(most_recent_time):
	print ('DB request to update begin_time:' + most_recent_time)


def get_begin_time(polymer_team_id):
	return '2017-12-01T00:00:00-08:00'