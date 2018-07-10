import httplib, urllib, json
from functools import reduce

# The base URL for every Connect API request
connection = httplib.HTTPSConnection('connect.squareup.com')

# Obtains all of the business's location IDs. Each location has its own collection of inventory, payments, etc.
def get_location_ids(request_headers):
	request_path = '/v1/me/locations'
	connection.request('GET', request_path, '', request_headers)
	response = connection.getresponse()

	# Transform the JSON array of locations into a Python list
	locations = json.loads(response.read())

	location_ids = []
	for location in locations:
		location_ids.append(location['id'])
	print(location_ids[0])
	return location_ids  # JUST FOR DEVELOPMENT


# Returns a dict {item_id -> [payment_obect], ...} of all ids specified in ITEM_ID_TO_ITEM_NAME_MAP
def get_payments_by_item_id(location_ids, time_range, request_headers, ITEM_ID_TO_ITEM_NAME_MAP):
	item_id_to_paymennts_map = {}
	parameters = urllib.urlencode(time_range)

	for location_id in location_ids:
		print 'Downloading Inventory for location with ID ' + location_id + '...'
		inventory_path = '/v1/' + location_id + '/payments?' + parameters
		connection.request('GET', inventory_path, '', request_headers)
		payments = json.loads(connection.getresponse().read())

		for payment in payments:
			for item_detail in payment['itemizations']:
				item_id = item_detail['item_detail'].get('item_id', False)
				# Some payments did not specify a product (item), and we want only the subset specified in ITEM_ID_TO_ITEM_NAME_MAP
				if item_id and ITEM_ID_TO_ITEM_NAME_MAP.get(item_id, False):
					if item_id_to_paymennts_map.get(item_id, False):
						item_id_to_paymennts_map[item_id].append(item_detail)
					else:
						item_id_to_paymennts_map[item_id] = [item_detail]
	return item_id_to_paymennts_map


def get_inventory_changes(begin_time, end_time, access_token, ITEM_ID_TO_ITEM_NAME_MAP):
	time_range = {'begin_time': begin_time, 'end_time': end_time}
	request_headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
	payments_by_item_id = get_payments_by_item_id(get_location_ids(request_headers), time_range, request_headers, ITEM_ID_TO_ITEM_NAME_MAP)
	print('ITEMS SOLD:')
	inventory_changes = []
	for item_id, payments_array in payments_by_item_id.iteritems():
		# sanity check: print each payment:
		for payment in payments_array:
			print(str(payment['name']) + ': ' + str(payment['quantity']))
		total_for_item = reduce(lambda sum, payment: sum + float(payment['quantity']), payments_array, 0)
		print('TOTAL for ' + str(payment['name']) + ': ' + str(total_for_item))
		print('_______________________')
		inventory_changes.append({
			'item_id': item_id,
			'quantity_sold': total_for_item,
			'name': ITEM_ID_TO_ITEM_NAME_MAP[item_id]
		})
	connection.close()
	return inventory_changes
