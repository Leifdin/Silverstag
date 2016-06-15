from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *

from module_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################



simple_triggers = [
	# (0,
		# [
			# # (map_free),
			# # (key_clicked, key_h),
			# # (call_script, "script_cf_qus_party_within_range_of_kingdom", "p_main_party"),
			# # (try_for_parties, ":party_no"),
				# # (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
				# # (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
				# # # (party_get_slot, ":troop_no", ":party_no", slot_town_lord),
				# # (store_troop_faction, ":faction_no", ":troop_no"),
				# # (eq, ":faction_no", "fac_kingdom_1"),
				# # (call_script, "script_cf_qus_player_within_range_of_kingdom", ":party_no"),
			# # (try_end),
		# ]

	# ),
	
	# (300,
		# [
			# #(map_free),
			# #(this_or_next|ge, DEBUG_QUEST_PACK_1, 1),
			# #(this_or_next|ge, DEBUG_QUEST_PACK_2, 1),
			# # (this_or_next|ge, DEBUG_QUEST_PACK_3, 1),
			# # (ge, DEBUG_QUEST_PACK_4, 1),
			# #(display_message, "@DEBUG (Quest Util): Parties around the player forced to ignore the player."),
			# #(call_script, "script_set_parties_around_player_ignore_player", 10, 1), # range, hours
		# ]

	# ),
	
	(24,
		[
			(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
				## SPAWN PRISONER CARAVANS IF NEEDED ##
				(try_begin),
					(party_get_num_prisoners, ":prisoner_count", ":center_no"),
					(ge, ":prisoner_count", 75),
					(neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), # Players should handle this themselves via quest or dialog.
					##### GENERATE PRISONER CARAVAN #####
					(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_create, 0, ":center_no"),
					(assign, ":caravan", reg51),
					(assign, "$g_move_heroes", 0), # Prevent heroes from being transfered.
					(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_generate_escort_cost, ":caravan", ":center_no"),    # Since no player escort is available figure out escort price.
					(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_add_escort_troops, ":caravan", reg51),              # Add in extra escort troops.
					(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_load_from_center, ":caravan", ":center_no"),        # Move prisoners from town to new party.
					(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_direct_to_destination, ":caravan", "p_salt_mine"),  # Set party AI
				(try_end),
				
				## UNLOAD WEALTH TO TOWN LORD IF AVAILABLE ##
				(try_begin),
					(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
					(ge, ":town_lord", 1), # Exclude player on purpose.  He'll receive it via weekly budget.
					(party_get_slot, ":treasury", ":center_no", slot_party_wealth),
					(ge, ":treasury", 1),
					# (troop_get_slot, ":lord_party", ":town_lord", slot_troop_leaded_party),
					# (store_distance_to_party_from_party, ":distance", ":lord_party", ":center_no"),
					# (lt, ":distance", 5),
					(troop_get_slot, ":cash_on_hand", ":town_lord", slot_troop_wealth),
					(val_add, ":cash_on_hand", ":treasury"),
					(troop_set_slot, ":town_lord", slot_troop_wealth, ":cash_on_hand"),
					(party_set_slot, ":center_no", slot_party_wealth, 0),
					(ge, DEBUG_QUEST_AI, 2),
					(str_store_troop_name, s31, ":town_lord"),
					(str_store_party_name, s32, ":center_no"),
					(assign, reg31, ":treasury"),
					(assign, reg32, ":cash_on_hand"),
					(display_message, "@DEBUG (Caravan AI): {s31} receives {reg31} denars from prisoners sold from {s32} raising his wealth to {reg32} denars."),
				(try_end),
			(try_end),
		]

	),
	
	## TRIGGER - Award Noble Recruits Event
	(1,
		[
			(map_free),
			(neq, "$award_nobles_reasoning", 0), # This should hold a string value if a valid award is pending.
			(try_begin),
				### TOURNAMENT WINS ###
				(eq, "$award_nobles_reasoning", "str_noble_joins_due_to_tournament"),
				(store_random_in_range, ":recruits", 1, 3),
				(call_script, "script_common_change_veteran_recruits_in_party", "$tpe_tournament_last_location", "trp_player", ":recruits", "$award_nobles_reasoning"),
			(else_try),
				### WEEKLY RIGHT TO RULE TRIGGER ###
				(eq, "$award_nobles_reasoning", "str_noble_joins_due_to_rtr"),
				(call_script, "script_cf_qus_player_owns_walled_center"), # questutil_scripts.py  - Returns center via reg1.
				(store_div, ":recruits", "$player_right_to_rule", 15),
				(val_clamp, ":recruits", 2, 7),
				(call_script, "script_common_change_veteran_recruits_in_party", reg1, "trp_player", ":recruits", "$award_nobles_reasoning"),
			(else_try),
				### SUCCESSFUL SIEGE TRIGGER ###
				(eq, "$award_nobles_reasoning", "str_noble_joins_due_to_siege"),
				(str_store_party_name, s21, "$current_town"),
				(call_script, "script_common_change_veteran_recruits_in_party", "$current_town", "trp_player", 4, "$award_nobles_reasoning"),
			(try_end),
			(assign, "$award_nobles_reasoning", 0),
		]),
]


# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "simple_triggers"
        orig_simple_triggers = var_set[var_name_1]
        orig_simple_triggers.extend(simple_triggers)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)