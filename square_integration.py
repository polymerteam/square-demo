import httplib, urllib, json
from functools import reduce
from fetch_urls_async import fetch_urls_async

# The base URL for every Connect API request
connection = httplib.HTTPSConnection('connect.squareup.com')


# Obtains all of the business's location IDs. Each location has its own collection of inventory, payments, etc.
def get_location_payment_urls(request_headers, time_range):
	# Get a list of all location ids
	request_path = '/v1/me/locations'
	connection.request('GET', request_path, '', request_headers)
	response = connection.getresponse()
	# Transform the JSON array of locations into a Python list
	locations = json.loads(response.read())

	# Format a payments urls for each location
	location_payment_urls = []
	parameters = urllib.urlencode(time_range)
	for location in locations:
		inventory_path = 'https://connect.squareup.com/v1/' + location['id'] + '/payments?' + parameters
		location_payment_urls.append(inventory_path)
	return location_payment_urls


# Returns a dict {item_id -> [payment_obect], ...} of all ids specified in ITEM_ID_TO_ITEM_NAME_MAP
def get_payments_by_item_id(time_range, request_headers, ITEM_ID_TO_ITEM_NAME_MAP):
	item_id_to_payments_map = {}

	# Download all payment from each location asynchronously
	location_payment_urls = get_location_payment_urls(request_headers, time_range)
	all_location_payments = fetch_urls_async(location_payment_urls, request_headers)

	# Parse all payments and group relavent group by item_id (product type)
	for payments in all_location_payments:
		for payment in payments:
			print (payment['itemizations'])
			for item_detail in payment['itemizations']:
				item_id = item_detail['item_detail'].get('item_id', False)
				# Some payments did not specify a product (item), and we want only the subset specified in ITEM_ID_TO_ITEM_NAME_MAP
				if item_id and ITEM_ID_TO_ITEM_NAME_MAP.get(item_id, False):
					if item_id_to_payments_map.get(item_id, False):
						item_id_to_payments_map[item_id].append(item_detail)
					else:
						item_id_to_payments_map[item_id] = [item_detail]
	return item_id_to_payments_map


def get_inventory_changes(begin_time, end_time, access_token, ITEM_ID_TO_ITEM_NAME_MAP):
	time_range = {'begin_time': begin_time, 'end_time': end_time}
	request_headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
	payments_by_item_id = get_payments_by_item_id(time_range, request_headers, ITEM_ID_TO_ITEM_NAME_MAP)

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
			'info': ITEM_ID_TO_ITEM_NAME_MAP[item_id]
		})
	connection.close()
	return inventory_changes
