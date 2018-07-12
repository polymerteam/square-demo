import urllib
from functools import reduce
from fetch_urls_async import fetch_urls_async
import dateutil.parser
from pprint import pprint


# Obtains all of the business's location IDs. Each location has its own collection of inventory, payments, etc.
def get_location_payment_urls(request_headers, time_range):
	# Get a list of all location ids (only one GET request, but use same helper for consistency)
	locations_url = 'https://connect.squareup.com/v1/me/locations'
	locations = fetch_urls_async([locations_url], request_headers)[0]

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
			created_at = payment.get('created_at', False)  # store to use for finding most recent item
			if not created_at:
				continue  # payments includes one object of store meta info, which we skip
			for item_detail in payment.get('itemizations', []):
				item_id = item_detail['item_detail'].get('item_id', False)
				# Some payments did not specify a product (item), and we want only the subset specified in ITEM_ID_TO_ITEM_NAME_MAP
				if item_id and ITEM_ID_TO_ITEM_NAME_MAP.get(item_id, False):
					item_detail['created_at'] = created_at
					if item_id_to_payments_map.get(item_id, False):
						item_id_to_payments_map[item_id].append(item_detail)
					else:
						item_id_to_payments_map[item_id] = [item_detail]
	return item_id_to_payments_map

def get_most_recent_payment(payments_array):
	return max(payments_array, key=lambda p: dateutil.parser.parse(p['created_at']))

def get_inventory_changes(begin_time, end_time, access_token, ITEM_ID_TO_ITEM_NAME_MAP):
	# Request payments made from begin_time (inclusive) to end_time (exclusive), sorted chronologically
	time_range = {'begin_time': begin_time, 'end_time': end_time, 'order': 'ASC'}
	request_headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
	payments_by_item_id = get_payments_by_item_id(time_range, request_headers, ITEM_ID_TO_ITEM_NAME_MAP)

	print('ITEMS SOLD:')
	inventory_changes = []
	most_recents_payments_for_each_item = []
	for item_id, payments_array in payments_by_item_id.iteritems():
		most_recents_payments_for_each_item.append(get_most_recent_payment(payments_array))
		# sanity check: print each payment:
		for payment in payments_array:
			print(str(payment['name']) + ': ' + str(payment['quantity']) + ', ' + str(payment['created_at']))

		total_for_item = reduce(lambda sum, payment: sum + float(payment['quantity']), payments_array, 0)
		print('TOTAL for ' + str(payment['name']) + ': ' + str(total_for_item))
		print('_______________________')
		inventory_changes.append({
			'item_id': item_id,
			'quantity_sold': total_for_item,
			'info': ITEM_ID_TO_ITEM_NAME_MAP[item_id]
		})

	print('MOST RECENT OF ALL: ' + get_most_recent_payment(most_recents_payments_for_each_item)['created_at'])
	return inventory_changes

