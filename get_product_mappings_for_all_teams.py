import os


# TO DO: map all square items <-> products/process combos
def get_product_mappings_for_all_teams():
	alabama_team_products = {
		'CIRMY5XHPTZQIQZD5JZLU64C': {'square_name': 'Maya Mountain, Belize 70%', 'polymer_process_id': 15, 'polymer_product_id': 32},
		'GHOBJZ27X2T544KMMPYI2JRW': {'square_name': 'Mantuano, Venezuela 70%', 'polymer_process_id': 15, 'polymer_product_id': 6},
		'7G662Y2EY3QEM6YMV3RDGNOQ': {'square_name': 'Piura Blanco, Peru 70%', 'polymer_process_id': 15, 'polymer_product_id': 14},
	}

	valencia_team_products = {
		'WIPH2BKIUQPYPX7OWQ7FGUE': {'square_name': 'Anamalai, India 70%', 'polymer_process_id': 34, 'polymer_product_id': 187},
	}

	polymer_teams = {
		'alabama': { 'polymer_team_id': 1, 'team_products': alabama_team_products, 'access_token': os.environ['SQUARE_ACCESS_TOKEN']},
		'valencia': {'polymer_team_id': 1, 'team_products': valencia_team_products, 'access_token': os.environ['SQUARE_ACCESS_TOKEN']},
	}

	return polymer_teams
