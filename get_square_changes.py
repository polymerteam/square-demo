from dispatch_requests_in_parallel import dispatch_requests_in_parallel
import urllib
from functools import reduce
import dateutil.parser
from pprint import pprint
import pickle


# Obtains all of the business's location IDs. Each location has its own collection of inventory, payments, etc.
def get_location_payment_urls(request_headers, time_range):
	# Get a list of all location ids (only one GET request, but use same helper for consistency)
	locations_url = 'https://connect.squareup.com/v1/me/locations'
	locations = dispatch_requests_in_parallel([locations_url], request_headers)[0]

	# Format a payments urls for each location
	location_payment_urls = []
	parameters = urllib.urlencode(time_range)
	for location in locations:
		inventory_path = 'https://connect.squareup.com/v1/' + location['id'] + '/payments?' + parameters
		location_payment_urls.append(inventory_path)
	return location_payment_urls


def get_datetime_object(payment):
	return dateutil.parser.parse(payment['created_at'])


# Remove potential duplicate values from the list of payments, and sorts old-new
# The official Square sample script does this with API data, so we do, too.
def get_sorted_unique_payments(all_location_payments):
	seen_payment_ids = set()
	unique_payments = []
	payments = reduce(lambda sum, payments: sum + payments, all_location_payments, [])

	for payment in payments:
		# Filter duplicates or the store-info object that come with each store's payments
		if payment['id'] in seen_payment_ids or payment.get('created_at', None) is None:
			continue
		seen_payment_ids.add(payment['id'])
		unique_payments.append(payment)
	return sorted(unique_payments, key=get_datetime_object)


# Returns a dict {item_id -> [payment_object], ...} of all ids specified in team_products
def get_payments_by_item_id(time_range, request_headers, team_products):
	item_id_to_payments_map = {}

	# Download all payment from each location asynchronously, get unique ones
	# location_payment_urls = get_location_payment_urls(request_headers, time_range)
	# all_location_payments = dispatch_requests_in_parallel(location_payment_urls, request_headers)
	# def save_obj(obj):
	# 	with open('moc_db.txt', 'wb') as f:
	# 		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
	# save_obj(all_location_payments)
	def load_obj():
		with open('moc_db.txt', 'rb') as f:
			return pickle.load(f)
	all_location_payments = load_obj()
	sorted_unique_payments = get_sorted_unique_payments(all_location_payments)

	# Parse all payments and group relevant group by item_id (product type)
	for payment in sorted_unique_payments:
		created_at = payment.get('created_at', False)  # store to use for finding most recent item
		if not created_at:
			continue  # payments includes one object of store meta info, which we skip
		for item_detail in payment.get('itemizations', []):
			item_id = item_detail['item_detail'].get('item_id', False)
			# Some payments did not specify a product (item), and we want only the subset specified in team_products
			if item_id and team_products.get(item_id, False):
				item_detail['created_at'] = created_at
				if item_id_to_payments_map.get(item_id, False):
					item_id_to_payments_map[item_id].append(item_detail)
				else:
					item_id_to_payments_map[item_id] = [item_detail]
	return item_id_to_payments_map


def get_most_recent_payment(payments_array):
	return max(payments_array, key=get_datetime_object)


def get_adjustment_explenation(square_name, most_recent_change):
	date_display_str = dateutil.parser.parse(most_recent_change).strftime('%c')
	return 'This adjustment was made automatically based on sales of "%s" on Square on or before %s.' % (square_name, date_display_str)


def get_square_changes(begin_time, end_time, access_token, team_products):
	# Request payments made from begin_time (inclusive) to end_time (exclusive), sorted chronologically
	time_range = {'begin_time': begin_time, 'end_time': end_time, 'order': 'ASC'}
	request_headers = {'Authorization': 'Bearer ' + access_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
	payments_by_item_id = get_payments_by_item_id(time_range, request_headers, team_products)

	adjustments = []
	most_recents_payment_for_each_item = []
	for item_id, payments_array in payments_by_item_id.iteritems():
		# Stash the most recent payment for this item, which we'll use to determine the most recent for ALL items
		most_recents_payment_for_each_item.append(payments_array[-1])  # because it's sorted oldest-newest
		total_amount_for_item = reduce(lambda sum, payment: sum + float(payment['quantity']), payments_array, 0)
		info = team_products[item_id]
		most_recent_change = get_most_recent_payment(most_recents_payment_for_each_item)['created_at']
		adjustments.append({
			'userprofile': 1,
			'process_type': info['polymer_process_id'],
			'product_type': info['polymer_product_id'],
			'amount': total_amount_for_item,
			'explanation': get_adjustment_explenation(info['square_name'], most_recent_change),
		})
	return {
		'adjustments': adjustments,
		'most_recent_change': most_recent_change,
	}
