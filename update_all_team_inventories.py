from get_product_mappings_for_all_teams import get_product_mappings_for_all_teams
from get_square_changes import get_square_changes
from make_polymer_adjustments import make_polymer_adjustments, update_begin_time, get_begin_time
from pprint import pprint
from datetime import datetime


# Runs a square fetch of payment data for the time period specified for each Polymer team specified.
# Makes necessary adjustments to Polymer's database, then updates begin_time to the most recent
# payment made + 1 second, which serves as the (inclusive) lower-bound for its next execution.


for polymer_team, team_data in get_product_mappings_for_all_teams().iteritems():
	try:
		begin_time = get_begin_time(team_data['polymer_team_id'])  # retrieve from DB
		end_time = '2017-12-05T00:00:00-08:00'  # datetime.utcnow()

		print('Requesting inventory data from Square for %s__________________________' % polymer_team)
		inventory_changes = get_square_changes(begin_time, end_time, team_data['access_token'], team_data['team_products'])
		pprint(inventory_changes)
		print('\n\n')
		print('Requesting Polymer inventory adjustments for %s__________________________' % polymer_team)
		make_polymer_adjustments(inventory_changes['adjustments'])
		update_begin_time(inventory_changes['most_recent_change'])

	except Exception as e:
		print('Updating inventory based on Square transactions terminated due to an exception:')
		print(e)
		raise
