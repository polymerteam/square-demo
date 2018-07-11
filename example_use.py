from square_integration import get_inventory_changes
from pprint import pprint
import os

# Sample Usage for Alabama
begin_time = '2017-11-01T00:00:00-08:00'
end_time = '2018-02-01T00:00:00-08:00'
access_token = os.environ['SQUARE_ACCESS_TOKEN']
ITEM_ID_TO_ITEM_NAME_MAP = {
	'CIRMY5XHPTZQIQZD5JZLU64C': {'square_name': 'Maya Mountain, Belize 70%', 'polymer_process_type_id': 18, 'polymer_product_type_id': 32},
	'GHOBJZ27X2T544KMMPYI2JRW': {'square_name': 'Mantuano, Venezuela 70%', 'polymer_process_type_id': 18, 'polymer_product_type_id': 6},
	'7G662Y2EY3QEM6YMV3RDGNOQ': {'square_name': 'Piura Blanco, Peru 70%', 'polymer_process_type_id': 18, 'polymer_product_type_id': 14},
}

try:
	inventory_changes = get_inventory_changes(begin_time, end_time, access_token, ITEM_ID_TO_ITEM_NAME_MAP)
	pprint(inventory_changes)
except Exception as e:
	print('Fetching Inventory data from square terminated due to exception:')
	print(e)

