from square_integration import get_inventory_changes
from make_polymer_adjustments import make_polymer_adjustments
from pprint import pprint
import os

# Sample Usage for Alabama
begin_time = '2017-12-01T00:00:00-08:00'
end_time = '2017-12-05T00:00:00-08:00'
access_token = os.environ['SQUARE_ACCESS_TOKEN']
alabama_team_products = {
	'CIRMY5XHPTZQIQZD5JZLU64C': {'square_name': 'Maya Mountain, Belize 70%', 'polymer_process_id': 18, 'polymer_product_id': 32},
	'GHOBJZ27X2T544KMMPYI2JRW': {'square_name': 'Mantuano, Venezuela 70%', 'polymer_process_id': 18, 'polymer_product_id': 6},
	'7G662Y2EY3QEM6YMV3RDGNOQ': {'square_name': 'Piura Blanco, Peru 70%', 'polymer_process_id': 18, 'polymer_product_id': 14},
}

polymer_teams = {
	'alabama': alabama_team_products,
}

for polymer_team, team_products in polymer_teams.iteritems():
	try:
		print('Requesting inventory data from Square for %s' % polymer_team)
		inventory_changes = get_inventory_changes(begin_time, end_time, access_token, team_products)
		pprint(inventory_changes)
		print('Requesting Polymer inventory adjustments for %s' % polymer_team)
		make_polymer_adjustments(inventory_changes['adjustments'])
	except Exception as e:
		print('Fetching Inventory data from square terminated due to exception:')
		print(e)
		raise




