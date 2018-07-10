from square_integration import get_inventory_changes
from pprint import pprint
import os

begin_time = '2017-11-01T00:00:00-08:00'
end_time = '2018-02-01T00:00:00-08:00'
access_token = os.environ['SQUARE_ACCESS_TOKEN']
ITEM_ID_TO_ITEM_NAME_MAP = {
	'CIRMY5XHPTZQIQZD5JZLU64C': 'Maya Mountain, Belize 70%',
	'GHOBJZ27X2T544KMMPYI2JRW': 'Mantuano, Venezuela 70%',
	'7G662Y2EY3QEM6YMV3RDGNOQ': 'Piura Blanco, Peru 70%',
}

inventory_changes = get_inventory_changes(begin_time, end_time, access_token, ITEM_ID_TO_ITEM_NAME_MAP)
pprint(inventory_changes)

