from get_product_mappings_for_all_teams import get_product_mappings_for_all_teams
from get_square_changes import get_square_changes
from make_polymer_adjustments import make_polymer_adjustments, get_last_square_sync_times
from pprint import pprint
from datetime import datetime, timedelta
import dateutil.parser
import arrow


# Runs a square fetch of payment data for the time period specified for each Polymer team specified.
# Makes necessary adjustments to Polymer's database, then updates begin_time to the most recent
# payment made + 1 second, which serves as the (inclusive) lower-bound for its next execution.


last_square_sync_times = get_last_square_sync_times()

for polymer_team, team_data in get_product_mappings_for_all_teams().iteritems():
	try:
		begin_time = last_square_sync_times[team_data['polymer_team_id']]  # '2018-03-27T01:50:16Z'
		end_time = arrow.utcnow().isoformat() # '2018-03-27T05:50:16Z'  #'2018-07-18T01:21:21.554316+00:00'
		print('Begin time: ' + begin_time)
		print('end time:' + str(end_time))
		print('Requesting inventory data from Square for %s__________________________' % polymer_team)
		inventory_changes = get_square_changes(begin_time, end_time, team_data['access_token'], team_data['team_products'], team_data['polymer_team_id'])
		pprint(inventory_changes)
		print('\n\n')
		print('Requesting Polymer inventory adjustments for %s__________________________' % polymer_team)
		if inventory_changes['last_synced_with_square_at'] is not None:
			make_polymer_adjustments(inventory_changes)

	except Exception as e:
		print('Updating inventory based on Square transactions terminated due to an exception:')
		print(e)
		raise
