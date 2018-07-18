# square-demo
Run the main script, `update_all_team_inventories.py`, to sync all listed teams' Polymer inventory with Square (teams and their respective products listed in `get_product_mappings_for_all_teams.py`).
### Backend: 
https://github.com/polymerteam/wafflecone/pull/211

### General Flow
* To setup, we retrieve the `last_synced_with_square_at` times for all teams.
* Next, for each team, fetch payments made in Square over the a time interval between the last update (which we retrieved) and the present moment (which gets stored as the last update time in the POST request to Polymer later). 
* Next, we retrieve the payments which match the specified product ids and format them into Adjustment objects.
* Finally, a POST request to Polymer then creates the necessary Adjustments and updates the last udpate time.

Requires `SQUARE_ACCESS_TOKEN` in local envinronment variables for each team. We just have one for Valencia and Alabama right now, since they share a Square account.

### Notes:
* the products on Square and Dandelion have yet to be fully mapped.
* Square limits 200 payments per request, meaning if a payment happens every 30 seconds, you shouldn't go more than ~1.5 hours without re-syncing. You may need to use the commented out, more than 1.5 hour date ranges to test large, aggregate results.
