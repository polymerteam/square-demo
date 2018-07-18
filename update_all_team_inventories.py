from get_product_mappings_for_all_teams import get_product_mappings_for_all_teams
from get_square_changes import get_square_changes
from make_polymer_adjustments import make_polymer_adjustments, get_last_square_sync_times
from pprint import pprint
import arrow


# Runs a square fetch of payment data for the time period specified for each Polymer team specified.
# Makes necessary adjustments to Polymer's database, then saves (exclusive) end_time for use as begin_time (inclusive)
# for the next time a Square sync is run.
# If any exception thrown, aborts that team's Square sync, and continues on to the remaining teams.


last_square_sync_times = get_last_square_sync_times()

for polymer_team, team_data in get_product_mappings_for_all_teams().iteritems():
	try:
		begin_time = last_square_sync_times[team_data['polymer_team_id']]  # '2018-01-01T00:00:00Z'
		end_time = arrow.utcnow().isoformat() # '2018-02-02T00:00:00Z'
		print('Begin time: ' + begin_time)
		print('end time:' + str(end_time))

		print('Requesting inventory data from Square for %s__________________________' % polymer_team)
		inventory_changes = get_square_changes(begin_time, end_time, team_data['access_token'], team_data['team_products'], team_data['polymer_team_id'])
		pprint(inventory_changes)

		print('\n')
		print('Requesting Polymer inventory adjustments for %s__________________________' % polymer_team)
		if inventory_changes['last_synced_with_square_at'] is not None:
			make_polymer_adjustments(inventory_changes)
		print('\n\n\n')

	except Exception as e:
		print('Updating inventory based on Square transactions terminated due to an exception:')
		print(e)
		# raise  # FOR DEBUG ONLY
