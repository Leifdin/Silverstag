# Enhanced Diplomacy (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *
from header_parties import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	

# script_diplomacy_initialize
# Sets initial conditions for the enhanced diplomacy system.
("diplomacy_initialize",
	[
		# Initialize faction policies.
		(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
			(call_script, "script_diplomacy_reset_policy_defaults", ":kingdom_no"),
		(try_end),
		(call_script, "script_diplomacy_reset_policy_defaults", "fac_no_faction"), # Initialize the "no faction" faction to prevent issues in the early game.
		
		# Swadia Policies
		(assign, ":kingdom_no", "fac_kingdom_1"),
		(faction_set_slot, ":kingdom_no", slot_faction_policy_culture_focus,  POLICY_STAGE_RIGHT_1), # Militant 1
		(faction_set_slot, ":kingdom_no", slot_faction_policy_border_control, POLICY_STAGE_LEFT_1),  # Open 1
		(faction_set_slot, ":kingdom_no", slot_faction_policy_slavery,        POLICY_STAGE_NEUTRAL), # Neutral
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_PRESENTATION),
		(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_FACTION),
		
		# Vaegir Policies
		(assign, ":kingdom_no", "fac_kingdom_2"),
		(faction_set_slot, ":kingdom_no", slot_faction_policy_culture_focus,  POLICY_STAGE_LEFT_2),  # Trade 2
		(faction_set_slot, ":kingdom_no", slot_faction_policy_border_control, POLICY_STAGE_LEFT_2),  # Open 2
		(faction_set_slot, ":kingdom_no", slot_faction_policy_slavery,        POLICY_STAGE_LEFT_1),  # Banned 1
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_PRESENTATION),
		(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_FACTION),
		
		# Khergit Policies
		(assign, ":kingdom_no", "fac_kingdom_3"),
		(faction_set_slot, ":kingdom_no", slot_faction_policy_culture_focus,  POLICY_STAGE_RIGHT_1), # Militant 1
		(faction_set_slot, ":kingdom_no", slot_faction_policy_border_control, POLICY_STAGE_RIGHT_2), # Sealed 2
		(faction_set_slot, ":kingdom_no", slot_faction_policy_slavery,        POLICY_STAGE_RIGHT_2), # Accepted 2
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_PRESENTATION),
		(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_FACTION),
		
		# Nord Policies
		(assign, ":kingdom_no", "fac_kingdom_4"),
		(faction_set_slot, ":kingdom_no", slot_faction_policy_culture_focus,  POLICY_STAGE_RIGHT_2), # Militant 2
		(faction_set_slot, ":kingdom_no", slot_faction_policy_border_control, POLICY_STAGE_RIGHT_1), # Sealed 1
		(faction_set_slot, ":kingdom_no", slot_faction_policy_slavery,        POLICY_STAGE_RIGHT_1), # Accepted 1
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_PRESENTATION),
		(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_FACTION),
		
		# Rhodok Policies
		(assign, ":kingdom_no", "fac_kingdom_5"),
		(faction_set_slot, ":kingdom_no", slot_faction_policy_culture_focus,  POLICY_STAGE_NEUTRAL), # Neutral
		(faction_set_slot, ":kingdom_no", slot_faction_policy_border_control, POLICY_STAGE_RIGHT_1), # Sealed 1
		(faction_set_slot, ":kingdom_no", slot_faction_policy_slavery,        POLICY_STAGE_LEFT_2),  # Banned 2
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_PRESENTATION),
		(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_FACTION),
		
		# Sarranid Policies
		(assign, ":kingdom_no", "fac_kingdom_6"),
		(faction_set_slot, ":kingdom_no", slot_faction_policy_culture_focus,  POLICY_STAGE_LEFT_1),  # Trade 1
		(faction_set_slot, ":kingdom_no", slot_faction_policy_border_control, POLICY_STAGE_NEUTRAL), # Neutral
		(faction_set_slot, ":kingdom_no", slot_faction_policy_slavery,        POLICY_STAGE_RIGHT_2), # Accepted 2
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_PRESENTATION),
		(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
		(call_script, "script_diplomacy_sync_faction_data", ":kingdom_no", STORE_TO_FACTION),
		
		# Initialize default mod settings.
		# (assign, "$diplomacy_filter_enabled", 1),        # Disabled by default.
		# (assign, "$diplomacy_use_alt_morale", 1),        # Default to alternate morale system.
		
		# Setup default upgrade data. (OUTDATED)
		# (try_for_range, ":troop_no", 1, "trp_end_of_troops"),
			# (neg|troop_is_hero, ":troop_no"),
			# (call_script, "script_diplomacy_initialize_troop_upgrade_options", ":troop_no"),
		# (try_end),
		
	]),  
	
###########################################################################################################################
#####                                             REVISED MORALE SYSTEM                                               #####
###########################################################################################################################

# script_diplomacy_get_player_party_morale_values
# Provides alternative method of party morale control.
# Output: reg0 = player_party_morale_target
("diplomacy_get_player_party_morale_values",
	[
		### BASE VALUE ###
		(assign, ":new_morale", 0),
		(try_begin),
			(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
			(faction_get_slot, ":faction_morale_bonus", "$players_kingdom", slot_faction_party_morale_adjust),
		(else_try),
			(assign, ":faction_morale_bonus", 0),
		(try_end),
		(val_add, ":new_morale", ":faction_morale_bonus"),
		
		### PARTY SIZE ###
		# The larger your party the more beneficial this is to morale.  Safety in numbers and all that.
		(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
		(assign, ":troop_count", 0),
		(try_for_range, ":i_stack", 1, ":num_stacks"),
			(party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
			(val_add, ":troop_count", ":stack_size"),
		(try_end),
		(store_div, ":troops_size_to_morale", ":troop_count", morale_party_size_factor),
		(val_max, ":troops_size_to_morale", 0),
		(val_clamp, ":troops_size_to_morale", morale_min_party_size, morale_max_party_size),
		(assign, "$g_player_party_morale_modifier_party_size", ":troops_size_to_morale"),
		(val_add, ":new_morale", "$g_player_party_morale_modifier_party_size"),
		
		### TROOP EFFECT: INPSIRING ###
		(call_script, "script_ce_inspiring_get_party_bonus", "p_main_party"),
		(val_add, ":new_morale", reg0), # Inspiring bonus

		### TROOP EFFECT: DRILL_SARGEANT ###
		(call_script, "script_ce_drill_sargeant_get_party_penalty", "p_main_party"),
		(val_sub, ":new_morale", reg0), # Drill Sargeant Penalty
		
		### LEADERSHIP SKILL ### : 0 to +40/60 morale.
		(store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),
		(try_begin),
			(eq, "$players_kingdom", "fac_player_supporters_faction"),
			(faction_get_slot, ":cur_faction_king", "$players_kingdom", slot_faction_leader),
			(eq, ":cur_faction_king", "trp_player"),
			(store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", morale_king_leadership_bonus), # Was 15 natively.
		(else_try),  
			(store_mul, "$g_player_party_morale_modifier_leadership", ":player_leadership", morale_basic_leadership_bonus), # Was 12 natively.
		(try_end),
		
		### TROOP EFFECT: RALLYING FIGURE ###
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", "trp_player", BONUS_RALLYING_FIGURE),
			(store_mul, ":rallying_bonus", ":player_leadership", 2),
			(val_add, "$g_player_party_morale_modifier_leadership", ":rallying_bonus"),
		(try_end),
		(val_add, ":new_morale", "$g_player_party_morale_modifier_leadership"),
		
		### DAYS ON THE MARCH ### : -50 to 0 morale. (global value is a positive integer)
		# (val_sub, ":new_morale", "$days_on_the_march"), # Days on the march gets factored in.
		### BATTLE WEARINESS ### : -50 to +15 morale.
		(val_add, ":new_morale", "$morale_battle_weary"), # Battle Weariness gets factored in.
		
		### PARTY UNITY ### : -60 to +60 morale.
		# Favors smaller parties, but is far less impacting on large parties with a similar background.
		# Determine combined leadership score for player & companions.
		(store_skill_level, ":party_leadership_score", "skl_leadership", "trp_player"),
		(try_for_range, ":companion_no", companions_begin, companions_end),
			(main_party_has_troop, ":companion_no"),
			(store_skill_level, ":leadership", "skl_leadership", ":companion_no"),
			(val_add, ":party_leadership_score", ":leadership"),
		(try_end),
		(val_mul, ":party_leadership_score", 3),
		# Figure out how many of each type of troop the player party has.
		(assign, ":faction_troops", 0),
		(assign, ":non_faction_troops", 0),
		(assign, ":mercenary_troops", 0),
		(assign, ":companion_troops", 0),
		(party_get_num_companion_stacks, ":stack_count","p_main_party"),
		(try_for_range, ":stack_no", 1, ":stack_count"),
			(party_stack_get_troop_id, ":troop_no","p_main_party",":stack_no"),
			(party_stack_get_size, ":stack_size","p_main_party",":stack_no"),
			(store_faction_of_troop, ":faction_no", ":troop_no"),
			##
			(faction_get_slot, ":troop_culture", ":faction_no",  slot_faction_culture),
			(faction_get_slot, ":player_culture", "$players_kingdom",  slot_faction_culture),
			## Determine Troop Type
			(try_begin),
				(is_between, ":troop_no", companions_begin, companions_end),
				(assign, ":treat_as_type", 1),
			(else_try),
				(faction_slot_eq, "$players_kingdom", slot_faction_culture, "fac_culture_player"),
				(is_between, ":troop_no", player_troops_begin, player_troops_end),
				(eq, ":troop_culture", "fac_culture_player"),
				(assign, ":treat_as_type", 2),
			(else_try),
				(neg|faction_slot_eq, "$players_kingdom", slot_faction_culture, "fac_culture_player"),
				(eq, ":troop_culture", ":player_culture"),
				(neg|is_between, ":troop_no", player_troops_begin, player_troops_end),
				(assign, ":treat_as_type", 2),
			(else_try),
				(is_between, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
				(assign, ":treat_as_type", 4),
			(else_try),
				(assign, ":treat_as_type", 3),
			(try_end),
			
			(try_begin),
				## TROOP ABILITY: BONUS_DEDICATED
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_DEDICATED), # combat_scripts.py - ability constants in combat_constants.py
				(val_sub, ":treat_as_type", 1),
				(val_max, ":treat_as_type", 1),
			(try_end),
			
			(try_begin),
				(eq, ":treat_as_type", 1),
				(val_add, ":companion_troops", ":stack_size"),
			(else_try),
				(eq, ":treat_as_type", 2),
				(val_add, ":faction_troops", ":stack_size"),
			(else_try),
				(eq, ":treat_as_type", 4),
				(val_add, ":mercenary_troops", ":stack_size"),
			(else_try),
				(val_add, ":non_faction_troops", ":stack_size"),
			(try_end),
			
		(try_end),
		
		# Determine unity based on faction troops.
		(try_begin),
			(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
			(faction_get_slot, reg1, "$players_kingdom", slot_faction_unity_top_faction),
			(faction_get_slot, reg2, "$players_kingdom", slot_faction_unity_bottom_faction),
		(else_try),
			## DEFAULT: -1 for every 3 faction troops.
			(assign, reg1, 1),
			(assign, reg2, 3),
		(try_end),
		(val_max, reg2, 1), # Prevent Div/0 errors.
		(val_mul, ":faction_troops", reg1),
		(val_div, ":faction_troops", reg2),
		
		# Determine unity based on non-faction troops.
		(try_begin),
			(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
			(faction_get_slot, reg1, "$players_kingdom", slot_faction_unity_top_nonfaction),
			(faction_get_slot, reg2, "$players_kingdom", slot_faction_unity_bottom_nonfaction),
		(else_try),
			## DEFAULT: -1 for every 1 non-faction troops.
			(assign, reg1, 1),
			(assign, reg2, 1),
		(try_end),
		(val_max, reg2, 1), # Prevent Div/0 errors.
		(val_mul, ":non_faction_troops", reg1),
		(val_div, ":non_faction_troops", reg2),
		
		# Determine unity based on mercenary troops.
		(try_begin),
			(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
			(faction_get_slot, reg1, "$players_kingdom", slot_faction_unity_top_mercs),
			(faction_get_slot, reg2, "$players_kingdom", slot_faction_unity_bottom_mercs),
		(else_try),
			## DEFAULT: -2 for every 1 non-faction troops.
			(assign, reg1, 2),
			(assign, reg2, 1),
		(try_end),
		(val_max, reg2, 1), # Prevent Div/0 errors.
		(val_mul, ":mercenary_troops", reg1),
		(val_div, ":mercenary_troops", reg2),
		
		# Create unity value.
		(assign, "$party_unity", ":party_leadership_score"),
		(val_sub, "$party_unity", ":faction_troops"),
		(val_sub, "$party_unity", ":non_faction_troops"),
		(val_sub, "$party_unity", ":mercenary_troops"),
		(val_clamp, "$party_unity", morale_min_party_unity, morale_max_party_unity),
		(val_add, ":new_morale", "$party_unity"), # Depending on party composition and companion leaderships this could be good or bad.
		
		### FOOD SUPPLIES ###
		(assign, "$g_player_party_morale_modifier_food", 0),
		# Determine cumulative morale bonuses of all food in stock.
		(try_for_range, ":cur_edible", food_begin, food_end),      
			(call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
			(item_get_slot, ":food_bonus", ":cur_edible", slot_item_food_bonus),
			(val_add, "$g_player_party_morale_modifier_food", ":food_bonus"),
		(try_end),
		## TROOP EFFECT: BONUS_CHEF
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", "$cms_role_storekeeper", BONUS_CHEF),
			(store_skill_level, ":trade_bonus", "skl_trade", "$cms_role_storekeeper"),
			(ge, ":trade_bonus", 1),
			(val_mul, ":trade_bonus", 25),
			(store_mul, ":chef_bonus", "$g_player_party_morale_modifier_food", ":trade_bonus"),
			(val_div, ":chef_bonus", 1000),
			(try_begin), ### DIAGNOSTIC+ ###
				(ge, DEBUG_TROOP_ABILITIES, 1),
				(assign, reg31, "$g_player_party_morale_modifier_food"),
				(store_add, reg32, "$g_player_party_morale_modifier_food", ":chef_bonus"),
				(store_skill_level, reg33, "skl_trade", "$cms_role_storekeeper"),
				(str_store_troop_name, s31, "$cms_role_storekeeper"),
				(display_message, "@DEBUG (Abilities): {s31}'s TRADE skill ({reg33}) improves food morale bonus from {reg31} to {reg32}. (CHEF)", gpu_debug),
			(try_end), ### DIAGNOSTIC- ###
			(val_add, "$g_player_party_morale_modifier_food", ":chef_bonus"),
		(try_end),
		# Determine how many days the food you have will last your party.  This favors smaller parties.
		
		(val_add, ":new_morale", "$g_player_party_morale_modifier_food"),
		
		# Factor in if the party has no food.
		(try_begin),
			(eq, "$g_player_party_morale_modifier_food", 0),
			(assign, "$g_player_party_morale_modifier_no_food", 30),
			(val_sub, ":new_morale", "$g_player_party_morale_modifier_no_food"),
		(else_try),
			(assign, "$g_player_party_morale_modifier_no_food", 0),
		(try_end),
		
		### WAGE DEBT ###
		(assign, "$g_player_party_morale_modifier_debt", 0),
		(try_begin),
			(gt, "$g_player_debt_to_party_members", 0),
			(call_script, "script_calculate_player_faction_wage"),
			(assign, ":total_wages", reg0),
			(store_mul, "$g_player_party_morale_modifier_debt", "$g_player_debt_to_party_members", 10),
			(val_max, ":total_wages", 1),
			(val_div, "$g_player_party_morale_modifier_debt", ":total_wages"),
			(val_clamp, "$g_player_party_morale_modifier_debt", 1, 31),
			(val_sub, ":new_morale", "$g_player_party_morale_modifier_debt"),
		(try_end),
		
		# Return Morale Value
		(val_clamp, ":new_morale", 0, 100),
		(assign, reg0, ":new_morale"),
	]),

# script_diplomacy_clear_morale_log
# PURPOSE: Completely empty the morale log for save game resets.  This is only applicable to the player party.
# EXAMPLE: (call_script, "script_diplomacy_clear_morale_log"), # diplomacy_scripts.py
("diplomacy_clear_morale_log",
	[
		(assign, "$morale_log_entries", 0),
		(try_for_range, ":slot_no", 0, 450),
			(troop_set_slot, PMR_LOG_DATE, ":slot_no", 0),
			(troop_set_slot, PMR_LOG_REASON, ":slot_no", 0),
			(troop_set_slot, PMR_LOG_CHANGE, ":slot_no", 0),
			(troop_set_slot, PMR_LOG_MORALE, ":slot_no", 0),
			(troop_set_slot, PMR_LOG_IDEAL, ":slot_no", 0),
		(try_end),
		
		(try_begin),
			(ge, BETA_TESTING_MODE, 2),
			(display_message, "@DEBUG (Morale Log): All entries deleted.", gpu_debug),
		(try_end),
	]),
	
# script_diplomacy_add_morale_log_entry
# PURPOSE: Store an additional entry into the party morale log.  This is only applicable to the player party.
# EXAMPLE: (call_script, "script_diplomacy_add_morale_log_entry", PMR_UNDEFINED, ":change"),
("diplomacy_add_morale_log_entry",
	[
		(store_script_param, ":reasoning", 1),
		(store_script_param, ":change", 2),
		
		## Update morale log total entries and reset count if needed.
		(val_add, "$morale_log_entries", 1),
		(try_begin),
			(ge, "$morale_log_entries", 450),
			(assign, "$morale_log_entries", 1),
		(try_end),
		
		## Store current time.
		(store_current_hours, ":hours"),
		(troop_set_slot, PMR_LOG_DATE, "$morale_log_entries", ":hours"),
		## Store the reasoning.
		(troop_set_slot, PMR_LOG_REASON, "$morale_log_entries", ":reasoning"),
		## Store the amount changed.
		(troop_set_slot, PMR_LOG_CHANGE, "$morale_log_entries", ":change"),
		## Store the REAL morale.
		(party_get_morale, ":morale_real", "p_main_party"),
		(troop_set_slot, PMR_LOG_MORALE, "$morale_log_entries", ":morale_real"),
		## Store the IDEAL morale.
		(call_script, "script_diplomacy_get_player_party_morale_values"),
		(troop_set_slot, PMR_LOG_IDEAL, "$morale_log_entries", reg0),
		
		(try_begin),
			(ge, BETA_TESTING_MODE, 2),
			(assign, reg31, "$morale_log_entries"),
			(display_message, "@DEBUG (Morale Log): Entry #{reg31} added.", gpu_debug),
		(try_end),
	]),

# script_diplomacy_get_morale_log_entry
# PURPOSE: Retrieves a specific entry from a given entry type & number.  This is only applicable to the player party.
# EXAMPLE: (call_script, "script_diplomacy_get_morale_log_entry", ":entry_no", PMR_LOG_DATE, ":reg_no"),
("diplomacy_get_morale_log_entry",
	[
		(store_script_param, ":entry_no", 1),
		(store_script_param, ":entry_type", 2),
		(store_script_param, ":reg_no", 3),
		
		(assign, ":value", 0),
		(try_begin),
			(is_between, ":entry_no", 0, 451),
			(try_begin),
				(this_or_next|eq, ":entry_type", PMR_LOG_DATE),
				(this_or_next|eq, ":entry_type", PMR_LOG_REASON),
				(this_or_next|eq, ":entry_type", PMR_LOG_CHANGE),
				(this_or_next|eq, ":entry_type", PMR_LOG_MORALE),
				(eq, ":entry_type", PMR_LOG_IDEAL),
				(troop_get_slot, ":value", ":entry_type", ":entry_no"),
			(else_try),
				(assign, reg31, ":entry_type"),
				(display_message, "@ERROR - Morale Log - Unrecognized entry type requested. (#{reg31})", gpu_red),
			(try_end),
		(else_try),
			(assign, reg31, ":entry_no"),
			(display_message, "@ERROR - Morale Log - Entry outside of range requested. (#{reg31})", gpu_red),
		(try_end),
		(register_set, ":reg_no", ":value"),
	]),
	
# script_diplomacy_get_battle_weariness_factor
# PURPOSE: Retrieves a specific battle weariness factor based on requested input and stores it in the requested register.
# EXAMPLE: (call_script, "script_diplomacy_get_battle_weariness_factor", WEARINESS_PENALTY, ":reg_no"),
("diplomacy_get_battle_weariness_factor",
	[
		(store_script_param, ":factor", 1),
		(store_script_param, ":reg_no", 2),
		
		# WEARINESS_PENALTY             = 1  # Returns how much ideal morale is lost per battle.
		# WEARINESS_RECOVERY_RATE       = 2  # Returns how much you should recover per 4 hours.
		# WEARINESS_RECOVERY_LIMIT      = 3  # Returns the maximum recovery rate you can achieve.
		
		(assign, ":value", 0),
		(try_begin),
			(eq, ":factor", WEARINESS_PENALTY),
			# Set initial baseline value.
			(assign, ":value", morale_weariness_penalty),
			# Apply faction penalties.
			(faction_get_slot, ":bw_penalty", "$players_kingdom", slot_faction_weariness_battle_penalty),
			(val_add, ":value", ":bw_penalty"),
			
		(else_try),
			(eq, ":factor", WEARINESS_RECOVERY_RATE),
			# Get the time since the last battle.
			(store_current_hours, ":hours"),
			(store_sub, ":value", ":hours", "$morale_time_last_battle"),
			# Get improvement rate maximum.
			(assign, ":upper_limit", morale_weariness_recovery_max),
			(faction_get_slot, ":faction_limit", "$players_kingdom", slot_faction_weariness_recovery_max),
			(val_add, ":upper_limit", ":faction_limit"),
			# Get raw rate of recovery.
			(assign, ":hour_spacing", morale_weariness_hour_spacing),
			(faction_get_slot, ":faction_spacing", "$players_kingdom", slot_faction_weariness_recovery_rate),
			(val_add, ":hour_spacing", ":faction_spacing"),
			# Get final rate.
			(val_div, ":value", ":hour_spacing"),
			(val_clamp, ":value", 0, ":upper_limit"),
			
		(else_try),
			(eq, ":factor", WEARINESS_RECOVERY_LIMIT),
			# Get improvement rate maximum.
			(assign, ":value", morale_weariness_recovery_max),
			(faction_get_slot, ":faction_limit", "$players_kingdom", slot_faction_weariness_recovery_max),
			(val_add, ":value", ":faction_limit"),
			(val_sub, ":value", 1), # Since a clamped upper limit is 1 higher than desired.
			
		(else_try),
			(eq, ":factor", WEARINESS_RECOVERY_SPACING),
			# Get raw rate of recovery.
			(assign, ":value", morale_weariness_hour_spacing),
			(faction_get_slot, ":faction_spacing", "$players_kingdom", slot_faction_weariness_recovery_rate),
			(val_add, ":value", ":faction_spacing"),
			
		(else_try),
			(assign, reg31, ":factor"),
			(display_message, "@ERROR - Battle Weariness - Unexpected information type requested. (#{reg31})", gpu_red),
		(try_end),
		
		(register_set, ":reg_no", ":value"),
	]),
	
# script_diplomacy_player_loots_village_consequences
# PURPOSE: Applies penalties to raiding a peaceful village.
# EXAMPLE: (call_script, "script_diplomacy_player_loots_village_consequences", ":center_no"),
("diplomacy_player_loots_village_consequences",
	[
		(store_script_param, ":center_no", 1),
		
		(store_faction_of_party, ":faction_no", ":center_no"),
		(store_relation, ":relation", "$players_kingdom", ":faction_no"),
		(try_begin),
			(ge, ":relation", 0),
			(assign, reg40, ":relation"),
			(try_begin),
				## VASSAL PROVOKES WAR - Angers current king.
				(call_script, "script_cf_qus_player_is_vassal", 1),
				# Anger current ruler.
				(faction_get_slot, ":troop_king", "$players_kingdom", slot_faction_leader),
				(call_script, "script_change_player_relation_with_troop", ":troop_king", -12, 1),
				# Increase player controversy.
				(troop_get_slot, ":controversy",  "trp_player", slot_troop_controversy),
				(val_add, ":controversy", 200),
				(troop_set_slot,  "trp_player", slot_troop_controversy, ":controversy"),
			(else_try),
				## KING PROVOKES WAR
				(call_script, "script_cf_qus_player_is_king", 1),
				(display_message, "@DEBUG: Testing provocation as king", gpu_debug),
				(call_script, "script_diplomacy_start_war_between_kingdoms", ":faction_no", "$players_kingdom", 1),
			(else_try),
				## UNAFFILIATED ANGERS FACTION
				(call_script, "script_change_player_relation_with_faction", ":faction_no", -5),
				(display_message, "@DEBUG: Testing provocation as commoner", gpu_debug),
			(try_end),
		(try_end),
	]),
	
###########################################################################################################################
#####                                                ADVISOR SYSTEM                                                   #####
###########################################################################################################################

# script_diplomacy_store_steward_advice_to_s0
# This figures out what a castle steward should recommend upon initial greeting.
("diplomacy_store_steward_advice_to_s0",
	[
		# LOGIC PROCESS:
			# Determine state of current garrison.
			# Determine state of current construction.
			# If garrison < 300 then
				# Recommend recruitment of more men.
			# If construction slot is open then
				# Look to repairs first.
				# Look to new construction next.
			# If a war advisor is not appointed then recommend one be appointed.
		
		# LOGIC: Determine state of current garrison.
		(assign, ":logic_garrison_is_undermanned", 1),
		(try_begin),
			(party_get_num_companions, ":garrison_count", "$current_town"),
			(party_get_slot, ":center_type", "$current_town", slot_party_type),
			(try_begin),
				(eq, ":center_type", spt_town),
				(assign, ":minimum_amount", 300),
			(else_try),
				(eq, ":center_type", spt_castle),
				(assign, ":minimum_amount", 150),
			(else_try),
				(assign, ":minimum_amount", 0),
			(try_end),
			(ge, ":garrison_count", ":minimum_amount"),
			(assign, ":logic_garrison_is_undermanned", 0),
		(try_end),
		
		# LOGIC: Determine if any buildings are near collapse.
		(assign, ":logic_building_near_destruction", 0),
		(assign, ":data_improvement_needing_repair", -1),
		(try_for_range, ":current_count", native_improvements_begin, center_improvements_end),
			(store_sub, ":counter", ":current_count", native_improvements_begin),
			(call_script, "script_cf_improvement_get_priority_for_ai", ":counter"),
			(assign, ":improvement", reg1),
			
			# Prevent the need for two loops, but make sure we only affect improvement slots.
			(this_or_next|is_between, ":improvement", native_improvements_begin, native_improvements_end),
			(is_between, ":improvement", center_improvements_begin, center_improvements_end),
			
			# Is this improvement damaged?
			(party_slot_ge, "$current_town", ":improvement", cis_damaged_60_percent),
			
			# Is it already being fixed?
			(neg|party_slot_eq, "$current_town", slot_center_current_improvement_1, ":improvement"),
			(neg|party_slot_eq, "$current_town", slot_center_current_improvement_2, ":improvement"),
			(neg|party_slot_eq, "$current_town", slot_center_current_improvement_3, ":improvement"),
				
			(assign, ":data_improvement_needing_repair", ":improvement"),
			(assign, ":logic_building_near_destruction", 1),
			(break_loop),
		(try_end),
		
		# LOGIC: Determine if improvements can be built here and find which is the priority.
		(assign, ":logic_improvement_available_to_build", 0),
		(assign, ":data_improvement_to_build", -1),
		(try_for_range, ":current_count", native_improvements_begin, center_improvements_end),
			(store_sub, ":counter", ":current_count", native_improvements_begin),
			(call_script, "script_cf_improvement_get_priority_for_ai", ":counter"),
			(assign, ":improvement", reg1),
			
			# Prevent the need for two loops, but make sure we only affect improvement slots.
			(this_or_next|is_between, ":improvement", native_improvements_begin, native_improvements_end),
			(is_between, ":improvement", center_improvements_begin, center_improvements_end),
			
			# Can this improvement be built here?
			(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement"),
			
			(assign, ":data_improvement_to_build", ":improvement"),
			(assign, ":logic_improvement_available_to_build", 1),
			(break_loop),
		(try_end),
		
		# LOGIC: Determine state of current construction.
		(assign, ":logic_building_slot_available", 0),
		(try_begin),
			(this_or_next|party_slot_eq, "$current_town", slot_center_current_improvement_1, 0),
			(this_or_next|party_slot_eq, "$current_town", slot_center_current_improvement_2, 0),
			(party_slot_eq, "$current_town", slot_center_current_improvement_3, 0),
			(assign, ":logic_building_slot_available", 1),
		(try_end),
		
		# LOGIC CYCLE & PRIORITY
		(try_begin),
			## A BUILDING IS NEAR DESTRUCTION, BUT WE HAVE NO AVAILABLE BUILDING SLOTS ## -> Recommend canceling an improvement.
			(eq, ":logic_building_near_destruction", 1), 
			(eq, ":logic_building_slot_available", 0),
			(call_script, "script_get_improvement_details", ":data_improvement_needing_repair"),
			(str_store_string, s0, "@Our {s0} has been damaged in a recent attack and is nearing collapse, but we currently lack the manpower to go after repairing it due to our other projects.  I believe we should halt our efforts on one of these projects and redirect our efforts to repair."),
			(eq, DEBUG_DIPLOMACY, 0), # Advisor advice.  Must be 0.
			
		(else_try),
			## A BUILDING IS NEAR DESTRUCTION ## -> Recommend repairing an improvement.
			(eq, ":logic_garrison_is_undermanned", 0),
			(eq, ":logic_building_near_destruction", 1), 
			(eq, ":logic_building_slot_available", 1),
			(call_script, "script_get_improvement_details", ":data_improvement_needing_repair"),
			(str_store_string, s0, "@During a recent siege our {s0} was severely damaged and requires immediate repair.  I believe we need to direct our efforts towards repair of this situation as soon as possible."),
			(eq, DEBUG_DIPLOMACY, 0), # Advisor advice.  Must be 0.
			
		(else_try),
			## GARRISON IS UNDERMANNED, BUT A BUILDING IS NEAR DESTRUCTION ## -> Recommend repairing an improvement.
			(eq, ":logic_garrison_is_undermanned", 1),
			(eq, ":logic_building_near_destruction", 1),
			(eq, ":logic_building_slot_available", 1),
			(call_script, "script_get_improvement_details", ":data_improvement_needing_repair"),
			(str_store_string, s0, "@While I would be more comfortable if the garrison was better stocked we have more immediate concerns to deal with.  Our {s0} was damaged in a recent attack and is nearing collapse.  We need to direct our efforts to repairing this situation as soon as possible."),
			(eq, DEBUG_DIPLOMACY, 0), # Advisor advice.  Must be 0.
			
		(else_try),
			## GARRISON IS UNDERMANNED, NO BUILDINGS NEARING DESTRUCTION ## -> Recommend improving the garrison.
			(eq, ":logic_garrison_is_undermanned", 1),
			(str_store_string, s0, "@I am concerned that our garrison lacks the resources to properly defend the castle if we come under attack.  We need to consider hiring more recruits to man the walls or our enemies will see us as an easy target."),
			(eq, DEBUG_DIPLOMACY, 0), # Advisor advice.  Must be 0.
			
		(else_try),
			## TRY BUILDING SOMETHING NEW ## -> Recommending building an improvement.
			(eq, ":logic_improvement_available_to_build", 1),
			(eq, ":logic_building_slot_available", 1),
			(call_script, "script_get_improvement_details", ":data_improvement_to_build"),
			(str_store_string, s0, "@While most of our pressing needs are met, I think we could benefit from the production of {s2}."),
			(eq, DEBUG_DIPLOMACY, 0), # Advisor advice.  Must be 0.
			
		(else_try),
			## DEFAULT RESPONSE - NORMAL ##
			(eq, DEBUG_DIPLOMACY, 0), # Advisor advice.  Must be 0.
			(str_store_string, s0, "@All is as it should be here, sire, and I see no immediate matters of pressing concern."),
			
		(else_try),
			## DEFAULT RESPONSE - DIAGNOSTIC ##
			(ge, DEBUG_DIPLOMACY, 1), # Advisor advice.  Must be 1.
			(str_store_string, s33, s0),
			(assign, reg31, ":logic_building_slot_available"),
			(assign, reg32, ":logic_garrison_is_undermanned"),
			(assign, reg33, ":logic_building_near_destruction"),
			(assign, reg34, ":logic_improvement_available_to_build"),
			(assign, reg35, ":data_improvement_to_build"),
			(assign, reg36, ":data_improvement_needing_repair"),
			(assign, reg37, ":garrison_count"),
			(try_begin),
				(this_or_next|is_between, ":data_improvement_to_build", native_improvements_begin, native_improvements_end),
				(is_between, ":data_improvement_to_build", center_improvements_begin, center_improvements_end),
				(call_script, "script_get_improvement_details", ":data_improvement_to_build"),
				(str_store_string, s31, s0),
			(try_end),
			(try_begin),
				(this_or_next|is_between, ":data_improvement_needing_repair", native_improvements_begin, native_improvements_end),
				(is_between, ":data_improvement_needing_repair", center_improvements_begin, center_improvements_end),
				(call_script, "script_get_improvement_details", ":data_improvement_needing_repair"),
				(str_store_string, s32, s0),
			(try_end),
			(str_store_string, s0, "@DIANOSTIC RESPONSE:^^Garrison is {reg32?:NOT} undermanned @ {reg37} men.^Repair {reg33?IS:is NOT} needed{reg33? for: {s32}:.}^{reg34?{s31} is available to build:Nothing is available to build}.^There {reg31?IS:is NOT} a space available to build something.^^Recommendation: {s33}"),
			
		(try_end),
	]),  
   
# script_diplomacy_order_all_patrols_of_center
# Provides a shortcut for sending an order to each valid patrol that is attached to a given center #.
("diplomacy_order_all_patrols_of_center",
	[
		(store_script_param, ":center_no", 1),
		(store_script_param, ":order", 2),
		
		(try_for_range, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
			(assign, ":slot_to_use", ":slot_no"),
			# Special consideration for PATROL_DISBAND because it shuffles patrols upward as each is disbanded.
			(try_begin),
				(eq, ":order", PATROL_DISBAND),
				(assign, ":slot_to_use", slot_center_patrols_begin),
			(try_end),
			(party_get_slot, ":party_no", ":center_no", ":slot_to_use"),
			(ge, ":party_no", 1), # Prevent 0's accidentally reaching the player's party.
			(party_is_active, ":party_no"),
			(call_script, "script_diplomacy_patrol_functions", ":party_no", ":order"),
		(try_end),
	]),
	
# script_diplomacy_determine_patrol_size
# This ties in the faction diplomacy alterations to how large a patrol size should be so it is done in one unique place.
("diplomacy_determine_patrol_size",
	[
		(store_script_param, ":party_no", 1), # Could be the patrol party or its home center.
		(store_script_param, ":base_size", 2),
		
		(store_faction_of_party, ":faction_no", ":party_no"),
		
		(try_begin),
			(eq, ":base_size", patrol_size_small),
			(assign, ":troop_count", 15),
		(else_try),
			(eq, ":base_size", patrol_size_medium),
			(assign, ":troop_count", 30),
		(else_try),
			(eq, ":base_size", patrol_size_large),
			(assign, ":troop_count", 45),
		(else_try),
			(assign, ":troop_count", 0),
			(assign, reg31, ":base_size"),
			(display_message, "@ERROR (diplomacy_scripts) - Invalid patrol size used in 'diplomacy_determine_patrol_size'. [{reg31}]", gpu_red),
		(try_end),
		
		## CAPTAIN OF THE GUARD: BONUS_ADMINISTRATOR
		## TROOP EFFECT: Increases the size of regional patrols from this center by 4 per point of Leadership.
		(try_begin),
			(is_between, ":party_no", walled_centers_begin, walled_centers_end),
			(party_get_slot, ":advisor_no", ":party_no", slot_center_advisor_war),
			(is_between, ":advisor_no", companions_begin, companions_end),
			(call_script, "script_cf_ce_troop_has_ability", ":advisor_no", BONUS_ADMINISTRATOR), # combat_scripts.py - ability constants in combat_constants.py
			(store_skill_level, ":leadership_bonus", "skl_leadership", ":advisor_no"),
			(val_mul, ":leadership_bonus", 5),
			(val_add, ":troop_count", ":leadership_bonus"),
		(try_end),
		
		## Faction Setting - Patrol Size
		(try_begin),
			(faction_get_slot, ":faction_change", ":faction_no", slot_faction_patrol_size_adjust),
			(neq, ":faction_change", 0),
			(store_mul, ":extra_troops", ":troop_count", ":faction_change"),
			(val_div, ":extra_troops", 100),
			(val_add, ":troop_count", ":extra_troops"),
		(try_end),
		
		(assign, reg1, ":troop_count"),
		(val_clamp, reg1, 5, 81),
	]),
	
# script_diplomacy_patrol_functions
# If a castle that an advisor is stationed at is lost then the advisor is setup to rejoin the companions that move around the map.
("diplomacy_patrol_functions",
	[
		(store_script_param, ":party_no", 1),
		(store_script_param, ":function", 2),
		
		# PATROL_GENERATE               = 0
		# PATROL_DISBAND                = 1
		# PATROL_UPGRADE_TROOPS         = 2
		# PATROL_RECRUIT_TROOPS         = 3
		# PATROL_DETERMINE_COST         = 4
		# PATROL_PAYMENT_DUE            = 5
		# PATROL_DETERMINE_PATROL_NO    = 6
		# PATROL_JOIN_COMBAT            = 7
		# PATROL_OFFLOAD_PRISONERS      = 8
		# PATROL_REPORT_STATUS          = 9
		# PATROL_GET_SUMMARY            = 10
		# PATROL_TRIM_EXTRAS            = 11
		# PATROL_RESET_AI_THINKING      = 12
		# PATROL_ACCOMPANY_OWNER        = 13
		# PATROL_DUMP_PRISONERS         = 14
		# PATROL_RESET_CENTER_SLOTS     = 15
		
		(try_begin),
			(this_or_next|party_is_active, ":party_no"),
			(this_or_next|eq, ":function", PATROL_GENERATE),            # No active party should exist when this is called.
			(this_or_next|eq, ":function", PATROL_DETERMINE_PATROL_NO), # This function has an error catch for invalid parties.
			(this_or_next|eq, ":function", PATROL_DISBAND),             # This needs to clear out invalid parties.
			(eq, ":function", PATROL_GET_SUMMARY), 
			# Fitler for bad party_no input.
			(ge, ":party_no", 1),
			### DIAGNOSTIC : BEGIN ###
			# (assign, reg31, ":party_no"),
			# (assign, reg32, ":function"),
			# (display_message, "@Attempt: party #{reg31}, function {reg32}.", gpu_debug),
			### DIAGNOSTIC : END ###
			
			# Define tier 1-5 troops for initializing city center.
			(assign, ":culture", -1),
			(try_begin),
				(eq, ":function", PATROL_GENERATE),
				# The party is being generated to it doesn't have a party # yet to check for culture.  In this case we'll use the spawning city's info that is passed via the ":party_no" parameter.
				(store_faction_of_party, ":faction_no", ":party_no"),
				(faction_get_slot, ":culture", ":faction_no", slot_faction_culture),
			(else_try),
				# Every other case there should be a valid party # to use even if it isn't active.
				(party_is_active, ":party_no"),
				(neg|is_between, ":party_no", walled_centers_begin, walled_centers_end), # Prevent PATROL_GET_SUMMARY & PATROL_DETERMINE_COST from using a center # to get this far and pick up a bogus culture #.
				(party_get_slot, ":culture", ":party_no", slot_party_patrol_culture),
			(try_end),
			(try_begin),
				(ge, ":culture", 0),
				(faction_get_slot, ":tier_1", ":culture",  slot_faction_tier_1_troop),
				(faction_get_slot, ":tier_2", ":culture",  slot_faction_tier_2_troop),
				(faction_get_slot, ":tier_3", ":culture",  slot_faction_tier_3_troop),
				(faction_get_slot, ":tier_4", ":culture",  slot_faction_tier_4_troop),
				(faction_get_slot, ":tier_5", ":culture",  slot_faction_tier_5_troop),
			(try_end),
			
			(try_begin),
				##### PATROL GENERATE #####
				(eq, ":function", PATROL_GENERATE),
				(assign, ":center_no", ":party_no"),
				# Determine which patrol slot to use.  If 1 is taken, move to 2, etc.
				(assign, ":center_patrol_slot", -1),
				(try_for_range, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
					(eq, ":center_patrol_slot", -1),
					(party_slot_eq, ":center_no", ":slot_no", 0),
					(assign, ":center_patrol_slot", ":slot_no"),
				(try_end),
				(assign, ":pass", 1),
				(try_begin),
					(eq, ":center_patrol_slot", -1),
					# Failure to create new patrol due to size.
				(else_try),
					# Pull data from about size ($temp) & training ($temp_2).
					(assign, ":patrol_size", "$temp"),
					(assign, ":patrol_training", "$temp_2"),
					# Spawn patrol party.
					(set_spawn_radius, 1),
					(spawn_around_party, "p_main_party", "pt_patrol_party"),
					(assign, ":patrol_party", reg0),
					# Stamp "slot_party_patrol_home" with originating center_no.
					(party_set_slot, ":patrol_party", slot_party_patrol_home, ":center_no"),            # Track which center the patrol came from via its party slot.
					(party_set_slot, ":center_no", ":center_patrol_slot", ":patrol_party"),             # Track which party the center has out via its center slot.
					(party_set_slot, ":patrol_party", slot_party_patrol_size, ":patrol_size"),          # Track how large our patrol should be.
					(party_set_slot, ":patrol_party", slot_party_patrol_training, ":patrol_training"),  # Keep track of what kind of tier of soldier our patrols should be.
					(party_set_slot, ":patrol_party", slot_party_patrol_culture, ":culture"),           # Track which culture of troops this party should use.
					# Determine proper size of patrol.
					(call_script, "script_diplomacy_determine_patrol_size", ":center_no", ":patrol_size"),
					(assign, ":troop_count", reg1),
					# Determine upgrade chances.
					(assign, ":tier_1_chance", 0),
					(assign, ":tier_2_chance", 0),
					(assign, ":tier_3_chance", 0),
					(assign, ":tier_4_chance", 0),
					(assign, ":tier_5_chance", 0),
					(try_begin),
						(eq, ":patrol_training", patrol_training_poor),
						(assign, ":tier_1_chance", 60),
						(assign, ":tier_2_chance", 40),
						(assign, ":tier_3_chance", 20),
					(else_try),
						(eq, ":patrol_training", patrol_training_average),
						(assign, ":tier_1_chance", 15),
						(assign, ":tier_2_chance", 35),
						(assign, ":tier_3_chance", 35),
						(assign, ":tier_4_chance", 15),
					(else_try),
						(eq, ":patrol_training", patrol_training_good),
						(assign, ":tier_2_chance", 25),
						(assign, ":tier_3_chance", 40),
						(assign, ":tier_4_chance", 30),
						(assign, ":tier_5_chance", 5),
					(else_try),
						(eq, ":patrol_training", patrol_training_elite),
						(assign, ":tier_3_chance", 40),
						(assign, ":tier_4_chance", 35),
						(assign, ":tier_5_chance", 25),
					(else_try),
						(assign, reg31, ":patrol_training"),
						(display_message, "@ERROR (diplomacy_scripts) - Patrol attempted to spawn with no TRAINING setting. [{reg31}]", gpu_red),
					(try_end),
					# Fill party with specified troops.
					(try_begin),
						# Add TIER 1 members
						(ge, ":tier_1_chance", 1),
						(store_mul, ":tier_1_troops", ":troop_count", ":tier_1_chance"),
						(val_div, ":tier_1_troops", 100),
						(party_add_members, ":patrol_party", ":tier_1", ":tier_1_troops"),
					(try_end),
					(try_begin),
						# Add TIER 2 members
						(ge, ":tier_2_chance", 1),
						(store_mul, ":tier_2_troops", ":troop_count", ":tier_2_chance"),
						(val_div, ":tier_2_troops", 100),
						(party_add_members, ":patrol_party", ":tier_2", ":tier_2_troops"),
					(try_end),
					(try_begin),
						# Add TIER 3 members
						(ge, ":tier_3_chance", 1),
						(store_mul, ":tier_3_troops", ":troop_count", ":tier_3_chance"),
						(val_div, ":tier_3_troops", 100),
						(party_add_members, ":patrol_party", ":tier_3", ":tier_3_troops"),
					(try_end),
					(try_begin),
						# Add TIER 4 members
						(ge, ":tier_4_chance", 1),
						(store_mul, ":tier_4_troops", ":troop_count", ":tier_4_chance"),
						(val_div, ":tier_4_troops", 100),
						(party_add_members, ":patrol_party", ":tier_4", ":tier_4_troops"),
					(try_end),
					(try_begin),
						# Add TIER 5 members
						(ge, ":tier_5_chance", 1),
						(store_mul, ":tier_5_troops", ":troop_count", ":tier_5_chance"),
						(val_div, ":tier_5_troops", 100),
						(party_add_members, ":patrol_party", ":tier_5", ":tier_5_troops"),
					(try_end),
					# Name party as a "Patrol from {city}".
					(str_store_party_name, s21, ":center_no"),
					(str_store_string, s22, "@Patrol from {s21}"),
					(party_set_name, ":patrol_party", s22),
					# Setup party's faction.
					(store_faction_of_party, ":faction_no", ":center_no"),
					(party_set_faction, ":patrol_party", ":faction_no"),
					# Setup AI for the party.
					(party_set_ai_object, ":patrol_party", ":center_no"),
					(party_set_ai_behavior, ":patrol_party", ai_bhvr_patrol_location),
					(party_set_slot, ":patrol_party", slot_party_ai_state, spai_patrolling_around_center),
					(party_set_ai_patrol_radius, ":patrol_party", 6),
					(party_set_slot, ":patrol_party", slot_party_type, spt_patrol),
					(party_set_slot, ":patrol_party", slot_party_ai_object, ":center_no"),
					(party_set_helpfulness, ":patrol_party", 500),
					# Report action to the player if he owns the town.
					(try_begin),
						(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
						(display_message, "@{s21} has comissioned a new patrol party.", gpu_green),
					(try_end),
				(else_try),
					### DEBUG - Patrol failed to spawn. ###
					(assign, ":pass", 0),
				(try_end),
				(eq, ":pass", 1),
				
			(else_try),
				##### PATROL_DISBAND #####
				(eq, ":function", PATROL_DISBAND),
				# Ensure there are no AI lords within the party's prisoners.  If so release them.
				# Clean out the associated party's center slot. (set to 0)
				(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DETERMINE_PATROL_NO),
				(try_begin),
					(is_between, reg2, walled_centers_begin, walled_centers_end),
					(assign, ":patrol_no", reg1),
					(store_add, ":slot_no", slot_center_patrols_begin, ":patrol_no"),
					(val_sub, ":slot_no", 1), # Since we added 1 in the above script we need to remove 1 here.
					(assign, ":center_no", reg2),
					(party_set_slot, ":center_no", ":slot_no", 0),
					# Despawn the party.
					(try_begin),
						(str_store_string, s22, "@ due to defeat."),
						(party_is_active, ":party_no"),
						(str_clear, s22),
						(remove_party, ":party_no"),
					(try_end),
					# Report action to the player if he owns the town.
					(str_store_party_name, s31, ":center_no"),
					(assign, reg31, ":patrol_no"),
					(try_begin),
						(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
						(display_message, "@Patrol #{reg31} from {s31} has been disbanded{s22}.", gpu_red),
					(else_try),
						(ge, DEBUG_DIPLOMACY_PATROLS, 1),
						(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
						(str_store_troop_name, s32, ":troop_no"),
						(display_message, "@DEBUG (patrols): Patrol #{reg31} from {s31} has been disbanded.  Town owned by {s32}.", gpu_debug),
					(try_end),
					# Shuffle patrols upward in slots.
					(try_for_range, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
						(party_slot_eq, ":center_no", ":slot_no", 0), # No party in current slot.
						(store_add, ":next_slot", ":slot_no", 1),
						(neq, ":next_slot", slot_center_patrols_end), # This should prevent us from trying to grab information out of bounds.
						(party_slot_ge, ":center_no", ":next_slot", 1), # Valid party.
						(party_get_slot, ":temp_party", ":center_no", ":next_slot"),
						(party_set_slot, ":center_no", ":slot_no", ":temp_party"),
						(party_set_slot, ":center_no", ":next_slot", 0),
						(ge, DEBUG_DIPLOMACY_PATROLS, 1),
						(assign, reg31, ":slot_no"),
						(assign, reg32, ":next_slot"),
						(assign, reg33, ":temp_party"),
						(str_store_party_name, s31, ":center_no"),
						(display_message, "@DEBUG (patrols): Patrol [Party #{reg33}] in {s31} moved from slot {reg32} to slot {reg31}.", gpu_debug),
					(try_end),
				(try_end),
				
			(else_try),
				##### PATROL UPGRADE TROOPS #####
				(eq, ":function", PATROL_UPGRADE_TROOPS),
				(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_TRIM_EXTRAS), # Clear out troops that don't belong there.
				(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
				(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DETERMINE_PATROL_NO),
				(assign, ":patrol_no", reg1),
				(try_begin),
					(party_is_active, ":party_no"),
					(party_get_num_companion_stacks, ":stack_limit", ":party_no"),
					# Upgrade 20% of each stack.
					(try_for_range, ":stack_no", 0, ":stack_limit"),
						(party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
						(neg|troop_is_hero, ":troop_no"),
						# Make sure this is someone we want in the party.
						(this_or_next|eq, ":troop_no", ":tier_1"),
						(this_or_next|eq, ":troop_no", ":tier_2"),
						(this_or_next|eq, ":troop_no", ":tier_3"),
						(eq, ":troop_no", ":tier_4"),
						# Determine upgrade path.
						(assign, ":upgrade_troop", -1),
						(try_begin),
							(eq, ":troop_no", ":tier_1"),
							(assign, ":upgrade_troop", ":tier_2"),
						(else_try),
							(eq, ":troop_no", ":tier_2"),
							(assign, ":upgrade_troop", ":tier_3"),
						(else_try),
							(eq, ":troop_no", ":tier_3"),
							(assign, ":upgrade_troop", ":tier_4"),
						(else_try),
							(eq, ":troop_no", ":tier_4"),
							(assign, ":upgrade_troop", ":tier_5"),
						(try_end),
						(ge, ":upgrade_troop", 0),
						# Figure out how many to upgrade.
						(party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
						(store_mul, ":upgrade_count", ":stack_size", 20),
						(val_div, ":upgrade_count", 100),
						# Add new troops.
						(party_add_members, ":party_no", ":upgrade_troop", ":upgrade_count"),
						# Remove old troops.
						(party_remove_members, ":party_no", ":troop_no", ":upgrade_count"),
						### DIAGNOSTIC ###
						(ge, DEBUG_DIPLOMACY_PATROLS, 1),
						(ge, ":upgrade_count", 1),
						(str_store_troop_name, s31, ":troop_no"),
						(str_store_troop_name, s32, ":upgrade_troop"),
						(str_store_party_name, s33, ":center_no"),
						(assign, reg31, ":upgrade_count"),
						(assign, reg32, ":patrol_no"),
						(display_message, "@DEBUG (patrols): Upgraded {reg31} '{s31}' -> '{s32}' in patrol #{reg32} from {s33}.", gpu_debug),
					(try_end),
					
				(else_try),
					(ge, DEBUG_DIPLOMACY_PATROLS, 1),
					(str_store_party_name, s31, ":center_no"),
					(assign, reg31, ":patrol_no"),
					(display_message, "@DEBUG (patrols): Patrol #{reg31} from {s31} did not UPGRADE due to being flagged INACTIVE.", gpu_debug),
				(try_end),
				
			(else_try),
				##### PATROL RECRUIT TROOPS #####
				(eq, ":function", PATROL_RECRUIT_TROOPS),
				(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_TRIM_EXTRAS), # Clear out troops that don't belong there.
				(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
				(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DETERMINE_PATROL_NO),
				(assign, ":patrol_no", reg1),
				(try_begin),
					(party_is_active, ":party_no"),
					# (store_faction_of_party, ":faction_no", ":party_no"),
					(party_get_slot, ":patrol_size", ":party_no", slot_party_patrol_size),
					(call_script, "script_diplomacy_determine_patrol_size", ":party_no", ":patrol_size"),
					(assign, ":ideal_size", reg1),
					(assign, ":party_size", 0),
					(party_count_members_of_type, ":members", ":party_no", ":tier_1"),
					(val_add, ":party_size", ":members"),
					(party_count_members_of_type, ":members", ":party_no", ":tier_2"),
					(val_add, ":party_size", ":members"),
					(party_count_members_of_type, ":members", ":party_no", ":tier_3"),
					(val_add, ":party_size", ":members"),
					(party_count_members_of_type, ":members", ":party_no", ":tier_4"),
					(val_add, ":party_size", ":members"),
					(party_count_members_of_type, ":members", ":party_no", ":tier_5"),
					(val_add, ":party_size", ":members"),
					(try_begin),
						(lt, ":party_size", ":ideal_size"),
						# Determine how many new recruits to add.  Limit maximum to 3 per attempt.
						(store_sub, ":recruit_count", ":ideal_size", ":party_size"),
						(val_min, ":recruit_count", 3),
						# Determine how seasoned these recruits should be based upon the kind of patrol we've hired.
						(party_get_slot, ":patrol_training", ":party_no", slot_party_patrol_training),
						(try_begin),
							(eq, ":patrol_training", patrol_training_poor),
							(assign, ":recruit_tier", ":tier_1"),
						(else_try),
							(eq, ":patrol_training", patrol_training_average),
							(assign, ":recruit_tier", ":tier_2"),
						(else_try),
							(eq, ":patrol_training", patrol_training_good),
							(assign, ":recruit_tier", ":tier_2"),
						(else_try),
							(eq, ":patrol_training", patrol_training_elite),
							(assign, ":recruit_tier", ":tier_3"),
						(try_end),
						(party_add_members, ":party_no", ":recruit_tier", ":recruit_count"),
						(ge, DEBUG_DIPLOMACY_PATROLS, 1),
						(assign, reg31, ":party_size"),
						(assign, reg32, ":ideal_size"),
						(assign, reg33, ":recruit_count"),
						(assign, reg34, ":patrol_training"),
						(assign, reg35, ":patrol_no"),
						(str_store_party_name, s31, ":center_no"),
						(str_store_troop_name, s32, ":recruit_tier"),
						(display_message, "@DEBUG (patrols): Patrol #{reg35} from {s31} recruits {reg33} {s32}.  +{reg33} gain in {reg31} / {reg32} party.", gpu_debug),
					(try_end),
					
				(else_try),
					(ge, DEBUG_DIPLOMACY_PATROLS, 1),
					(str_store_party_name, s31, ":center_no"),
					(assign, reg31, ":patrol_no"),
					(display_message, "@DEBUG (patrols): Patrol #{reg31} from {s31} did not RECRUIT due to being flagged INACTIVE.", gpu_debug),
				(try_end),
				
			(else_try),
				##### PATROL_DETERMINE_COST #####
				(eq, ":function", PATROL_DETERMINE_COST),
				(try_begin),
					(neg|is_between, ":party_no", walled_centers_begin, walled_centers_end),
					(party_get_slot, ":patrol_size", ":party_no", slot_party_patrol_size),
					(party_get_slot, ":patrol_training", ":party_no", slot_party_patrol_training),
					(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
				(else_try),
					(assign, ":center_no", ":party_no"),
					(assign, ":patrol_size", "$temp"),
					(assign, ":patrol_training", "$temp_2"),
				(try_end),
				(store_faction_of_party, ":faction_no", ":center_no"),
				(call_script, "script_diplomacy_determine_patrol_size", ":center_no", ":patrol_size"),
				(store_mul, ":cost", reg1, ":patrol_training"),
				(val_mul, ":cost", 15),
				# Tie in the troop wage discount from kingdom management.
				(try_begin),
					(faction_get_slot, ":wage_discount", ":faction_no", slot_faction_troop_wages),
					(val_mul, ":wage_discount", 2),
					(store_mul, ":discount", ":cost", ":wage_discount"),
					(val_div, ":discount", 100),
					(val_add, ":cost", ":discount"),
				(try_end),
				## CASTLE STEWARD: BONUS_EFFICIENT
				## TROOP EFFECT: Reduces the cost of regional patrols from this center by efficient_patrol_discount% per point of Leadership.
				(try_begin),
					(is_between, ":center_no", walled_centers_begin, walled_centers_end),
					(party_get_slot, ":advisor_no", ":center_no", slot_center_steward),
					(is_between, ":advisor_no", companions_begin, companions_end),
					(call_script, "script_cf_ce_troop_has_ability", ":advisor_no", BONUS_EFFICIENT), # combat_scripts.py - ability constants in combat_constants.py
					(store_skill_level, ":leadership_bonus", "skl_leadership", ":advisor_no"),
					(val_mul, ":leadership_bonus", efficient_patrol_discount),
					(store_mul, ":discount", ":cost", ":leadership_bonus"),
					(val_div, ":discount", 100),
					(assign, reg31, ":cost"),
					(val_sub, ":cost", ":discount"),
					(assign, reg32, ":cost"),
					(assign, reg33, ":discount"),
					(assign, reg34, ":leadership_bonus"),
					(str_store_party_name, s31, ":center_no"),
					(str_store_troop_name, s32, ":advisor_no"),
					(display_message, "@DEBUG (Eff): {s31}'s patrol cost reduced from {reg31} to {reg32} (-{reg33} denars) due to {s32}'s leadership bonus (-{reg34}%).", gpu_debug),
				(try_end),
				(assign, reg1, ":cost"),
				(assign, reg62, ":cost"), # For later use in PATROL_PAYMENT_DUE
				(try_begin),
					(neg|is_between, ":party_no", walled_centers_begin, walled_centers_end),
					(party_set_slot, ":party_no", slot_party_patrol_upkeep, reg1),
				(try_end),
				
			(else_try),
				##### PATROL_PAYMENT_DUE #####
				(eq, ":function", PATROL_PAYMENT_DUE),
				(party_get_slot, ":upkeep", ":party_no", slot_party_patrol_upkeep),
				(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
				(try_begin),
					# Player owns the fief the patrol comes from.
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(store_troop_gold, ":gold", "trp_player"),
					(try_begin),
						# Player can afford to pay the upkeep.
						# (call_script, "script_cf_diplomacy_treasury_verify_funds", ":upkeep", ":center_no", FUND_FROM_EITHER, TREASURY_FUNDS_AVAILABLE),
						(ge, ":gold", ":upkeep"),
						(try_begin),
							(ge, DEBUG_DIPLOMACY_PATROLS, 1),
							(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DETERMINE_PATROL_NO),
							(assign, reg33, reg1),
							(assign, reg31, ":gold"),
							(assign, reg32, ":upkeep"),
							(str_store_party_name, s31, ":center_no"),
							(display_message, "@DEBUG (Patrols): Patrol #{reg33} from {s31} draws payment of {reg32}.", gpu_debug),
						(try_end),
						(assign, reg1, ":upkeep"),
					(else_try),
						# Player can't pay for the patrol so it gets disbanded.
						(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DISBAND),
						(assign, reg1, 0),
					(try_end),
					
				(else_try),
					## AI PAYMENT ##
					(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
					(troop_get_slot, ":wealth", ":troop_no", slot_troop_wealth),
					(try_begin),
						(ge, ":wealth", ":upkeep"),
						(val_sub, ":wealth", ":upkeep"),
						(troop_set_slot, ":troop_no", slot_troop_wealth, ":wealth"),
					(else_try),
						(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DISBAND),
					(try_end),
					
				(try_end),
				
			(else_try),
				##### PATROL_DETERMINE_PATROL_NO #####
				(eq, ":function", PATROL_DETERMINE_PATROL_NO),
				(try_begin),
					## Valid party is available to determine center. ##
					(party_is_active, ":party_no"),
					(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
					(is_between, ":center_no", walled_centers_begin, walled_centers_end), # Potential bug trap.
					(assign, reg2, -1), # Feedback the patrol wasn't found.
					(try_for_range, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
						(party_slot_eq, ":center_no", ":slot_no", ":party_no"),
						(store_sub, reg1, ":slot_no", slot_center_patrols_begin),
						(val_add, reg1, 1),
						(assign, reg2, ":center_no"),
						(break_loop),
					(try_end),
				(else_try),
					## No valid party exists to determine the center.  Check them all. ##
					(assign, reg2, -1),
					(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
						(try_for_range, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
							(party_slot_eq, ":walled_center", ":slot_no", ":party_no"),
							(store_sub, reg1, ":slot_no", slot_center_patrols_begin),
							(val_add, reg1, 1),
							(assign, reg2, ":walled_center"),
							(break_loop),
						(try_end),
						(is_between, reg2, walled_centers_begin, walled_centers_end),
						(break_loop),
					(try_end),
				(try_end),
				
			(else_try),
				##### PATROL_JOIN_COMBAT #####
				(eq, ":function", PATROL_JOIN_COMBAT),
				(try_begin),
					(party_is_active, ":party_no"),
					(party_slot_eq, ":party_no", slot_party_type, spt_patrol),
					(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
					(is_between, ":center_no", walled_centers_begin, walled_centers_end), # This makes sure the next line is even relevent.
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DETERMINE_PATROL_NO),
					(assign, ":patrol_no", reg1),
					(try_begin),
						(store_distance_to_party_from_party, ":distance", ":party_no", "p_main_party"),
						(lt, ":distance", 5),
						(party_quick_attach_to_current_battle, ":party_no", 0), #attach as friend
						(neg|is_between, "$g_encountered_party", centers_begin, centers_end),
						(try_begin),
							(store_faction_of_party, ":faction_check", "$g_encountered_party"),
							(neq, ":faction_check", "$players_kingdom"), # We don't really want our patrols joining battle with us displayed if we're talking to a friend.
							(str_store_party_name, s1, ":party_no"),
							(display_message, "str_s1_joined_battle_friend"),
						(try_end),
						(ge, DEBUG_DIPLOMACY_PATROLS, 1),
						(str_store_party_name, s31, ":center_no"),
						(assign, reg31, ":patrol_no"),
						(display_message, "@DEBUG (patrols): Patrol #{reg31} of {s31} has been forced to join the player.", gpu_debug),
					(else_try),
						(ge, DEBUG_DIPLOMACY_PATROLS, 2),
						(str_store_party_name, s31, ":center_no"),
						(assign, reg31, ":patrol_no"),
						(display_message, "@DEBUG (patrols): Patrol #{reg31} of {s31} did not join because they are too far away.", gpu_debug),
					(try_end),
				(try_end),
				
			(else_try),
				##### PATROL_OFFLOAD_PRISONERS #####
				(eq, ":function", PATROL_OFFLOAD_PRISONERS),
				# Figure out how many prisoners we can accept transfered.
				(party_get_num_prisoners, ":available_prisoners", ":party_no"),
				(party_get_free_prisoners_capacity, ":capacity", "p_main_party"),
				(val_min, ":available_prisoners", ":capacity"),
				(assign, ":limit", ":available_prisoners"),
				(assign, "$g_move_heroes", 1),
				# Transfer the prisoners.
				(party_get_num_prisoner_stacks, ":num_stacks", ":party_no"),
				(try_for_range, ":stack_no", 0, ":num_stacks"),
					(ge, ":limit", 1),
					(party_prisoner_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
					(this_or_next|neg|troop_is_hero, ":troop_no"),
					(eq, "$g_move_heroes", 1),
					(party_prisoner_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
					(val_min, ":stack_size", ":limit"),
					(val_sub, ":limit", ":stack_size"),
					(party_add_prisoners, "p_main_party", ":troop_no", ":stack_size"),
				(try_end),
				(call_script, "script_party_remove_all_prisoners", ":party_no"),
				
			(else_try),
				##### PATROL_REPORT_STATUS #####
				(eq, ":function", PATROL_REPORT_STATUS),
				(str_clear, s21),
				(str_store_party_name, s22, "$current_town"),
				# Determine which party this is.
				(assign, reg21, 0),
				(try_for_range, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
					(party_slot_eq, "$current_town", ":slot_no", ":party_no"),
					(store_sub, reg21, ":slot_no", slot_center_patrols_begin),
					(val_add, reg21, 1), # So we don't start with party #0.
					(break_loop),
				(try_end),
				(str_store_string, s21, "@Patrol #{reg21} from {s22}:"),
				(str_store_string, s21, "@{s21}^-----------------------------------------------------------"),
				(try_begin),
					(party_is_active, ":party_no"),
					# Determine the nearest fief to our patrol.
					(assign, ":nearest_fief", -1),
					(assign, ":nearest_distance", 10000),
					(try_for_range, ":center_no", centers_begin, centers_end),
						(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
						(lt, ":distance", ":nearest_distance"),
						(assign, ":nearest_fief", ":center_no"),
						(assign, ":nearest_distance", ":distance"),
					(try_end),
					(str_store_party_name, s22, ":nearest_fief"),
					(str_store_string, s21, "@{s21}^They are patrolling near {s22}."),
					# Determine the general health of the patrol.
					(party_get_num_companion_stacks, ":stack_count", ":party_no"),
					(assign, ":total_wounded", 0),
					(assign, ":total_count", 0),
					(try_for_range, ":stack_no", 0, ":stack_count"),
						(party_stack_get_num_wounded, ":wounded", ":party_no", ":stack_no"),
						(party_stack_get_size, ":count", ":party_no", ":stack_no"),
						(val_add, ":total_wounded", ":wounded"),
						(val_add, ":total_count", ":count"),
					(try_end),
					(store_mul, ":health", ":total_wounded", 100),
					(val_max, ":total_count", 1), # Prevent Div/0 errors.
					(val_div, ":health", ":total_count"),
					(try_begin),
						(lt, ":health", 15),
						(str_store_string, s22, "@Their captain reports the men are well"),
					(else_try),
						(lt, ":health", 35),
						(str_store_string, s22, "@Their captain reports a number of injuries have been sustained"),
					(else_try),
						(lt, ":health", 65),
						(str_store_string, s22, "@Their captain fears for the condition of his men"),
					(else_try),
						(str_store_string, s22, "@The men are in a sorry state of health"),
					(try_end),
					(str_store_string, s21, "@{s21}  {s22}"),
					# Show reinforcement request status.
					(try_begin),
						(lt, ":total_count", 8),
						(str_store_string, s21, "@{s21} and requests immediate reinforcements."),
					(else_try),
						(lt, ":total_count", 16),
						(str_store_string, s21, "@{s21}, but he could use a few more soldiers to keep the area clear."),
					(else_try),
						(lt, ":total_count", 25),
						(str_store_string, s21, "@{s21}, though he could always use more soldiers if they can be spared."),
					(else_try),
						(str_store_string, s21, "@{s21} and doesn't need any help in the area."),
					(try_end),
					# Determine the status of prisoners.
					(party_get_num_prisoners, ":prisoner_count", ":party_no"),
					(try_begin),
						(ge, ":prisoner_count", 20),
						(str_store_string, s22, "@Following a battle in the area, they've captured a large number of prisoners."),
					(else_try),
						(ge, ":prisoner_count", 10),
						(str_store_string, s22, "@It seems they've captured several prisoners in a recent skirmish."),
					(else_try),
						(str_store_string, s22, "@They also are holding a few prisoners."),
					(try_end),
					(try_begin),
						(ge, ":prisoner_count", 1),
						(str_store_string, s21, "@{s21}  {s22}"),
					(try_end),
					
				(else_try),
					### Party is inactive ###
					(str_store_string, s21, "@I have not heard from them in some time."),
				(try_end),
				
			(else_try),
				##### PATROL_GET_SUMMARY #####
				(eq, ":function", PATROL_GET_SUMMARY),
				(try_begin),
					(neg|is_between, ":party_no", walled_centers_begin, walled_centers_end),
					(party_get_slot, ":patrol_size", ":party_no", slot_party_patrol_size),
					(party_get_slot, ":patrol_training", ":party_no", slot_party_patrol_training),
					(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
				(else_try),
					(assign, ":center_no", ":party_no"),
					(assign, ":patrol_size", "$temp"),
					(assign, ":patrol_training", "$temp_2"),
				(try_end),
				# (store_faction_of_party, ":faction_no", ":party_no"),
				(call_script, "script_diplomacy_determine_patrol_size", ":party_no", ":patrol_size"),
				(assign, reg40, reg1),
				(try_begin),
					(eq, ":patrol_size", patrol_size_small),
					(str_store_string, s41, "@small squad ({reg40})"),
				(else_try),
					(eq, ":patrol_size", patrol_size_medium),
					(str_store_string, s41, "@medium party ({reg40})"),
				(else_try),
					(eq, ":patrol_size", patrol_size_large),
					(str_store_string, s41, "@large warband ({reg40})"),
				(try_end),
				(try_begin),
					(eq, ":patrol_training", patrol_training_poor),
					(str_store_string, s42, "@mostly recruits"),
				(else_try),
					(eq, ":patrol_training", patrol_training_average),
					(str_store_string, s42, "@average soldiers"),
				(else_try),
					(eq, ":patrol_training", patrol_training_good),
					(str_store_string, s42, "@good soldiers"),
				(else_try),
					(eq, ":patrol_training", patrol_training_elite),
					(str_store_string, s42, "@elite veterans"),
				(try_end),
				(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DETERMINE_COST),
				(assign, reg21, reg1),
				(str_store_string, s21, s41),
				(str_store_string, s22, s42),
				
			(else_try),
				##### PATROL_TRIM_EXTRAS #####
				(eq, ":function", PATROL_TRIM_EXTRAS),
				(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
				(try_begin),
					(party_is_active, ":party_no"),
					# Remove any non-faction troops from the party.
					(party_get_num_companion_stacks, ":stack_limit", ":party_no"),
					(try_for_range_backwards, ":stack_no", 0, ":stack_limit"),
						(party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
						(neg|troop_is_hero, ":troop_no"), # Don't want to lose the leader.
						(neq, ":troop_no", ":tier_1"),
						(neq, ":troop_no", ":tier_2"),
						(neq, ":troop_no", ":tier_3"),
						(neq, ":troop_no", ":tier_4"),
						(neq, ":troop_no", ":tier_5"),
						(party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
						(party_remove_members, ":party_no", ":troop_no", ":stack_size"),
						### DIAGNOSTIC ###
						(ge, DEBUG_DIPLOMACY_PATROLS, 1),
						(str_store_troop_name, s31, ":troop_no"),
						(assign, reg31, ":stack_size"),
						(display_message, "@DEBUG (patrols): Removed {reg31} '{s31}' from patrol party.", gpu_debug),
					(try_end),
				(else_try),
					(ge, DEBUG_DIPLOMACY_PATROLS, 1),
					(str_store_party_name, s31, ":center_no"),
					(assign, reg31, ":patrol_no"),
					(display_message, "@DEBUG (patrols): Patrol #{reg31} from {s31} did not trim members due to being flagged INACTIVE.", gpu_debug),
				(try_end),
			
			(else_try),
				##### PATROL_RESET_AI_THINKING #####
				(eq, ":function", PATROL_RESET_AI_THINKING),
				# Setup AI for the party.
				(party_is_active, ":party_no"),
				(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
				(party_set_ai_object, ":party_no", ":center_no"),
				(party_set_ai_behavior, ":party_no", ai_bhvr_patrol_location),
				(party_set_slot, ":party_no", slot_party_ai_state, spai_patrolling_around_center),
				(party_set_ai_patrol_radius, ":party_no", 6),
				(party_set_slot, ":party_no", slot_party_type, spt_patrol),
				(party_set_slot, ":party_no", slot_party_ai_object, ":center_no"),
				(party_set_helpfulness, ":party_no", 500),
				
			(else_try),
				##### PATROL_ACCOMPANY_OWNER #####
				(eq, ":function", PATROL_ACCOMPANY_OWNER),
				# Setup AI for the party.
				(party_is_active, ":party_no"),
				(party_get_slot, ":center_no", ":party_no", slot_party_patrol_home),
				(party_set_ai_object, ":party_no", "p_main_party"),
				(party_set_ai_behavior, ":party_no", ai_bhvr_escort_party),
				(party_set_slot, ":party_no", slot_party_ai_state, spai_accompanying_army),
				(party_set_slot, ":party_no", slot_party_ai_object, "p_main_party"),
				(party_set_helpfulness, ":party_no", 500),
				
			(else_try),
				##### PATROL_DUMP_PRISONERS #####
				(eq, ":function", PATROL_DUMP_PRISONERS),
				# Figure out how many prisoners we can accept transfered.
				(party_get_num_prisoners, ":available_prisoners", ":party_no"),
				(try_begin),
					(ge, ":available_prisoners", 1),
					(assign, "$g_move_heroes", 0), # Do not dump hero prisoners.
					(call_script, "script_party_remove_all_prisoners", ":party_no"),
				(try_end),
			
			(else_try),
				##### PATROL_RESET_CENTER_SLOTS #####
				(eq, ":function", PATROL_RESET_CENTER_SLOTS),
				(assign, ":center_no", ":party_no"),
				# Cycle through each patrol of a center and clean them out if they're not active.
				(is_between, ":center_no", walled_centers_begin, walled_centers_end),
				(try_for_range_backwards, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
					(party_get_slot, ":patrol_no", ":center_no", ":slot_no"),
					(ge, ":patrol_no", 1),
					(neg|party_is_active, ":patrol_no"),
					(call_script, "script_diplomacy_patrol_functions", ":patrol_no", PATROL_DISBAND),
				(try_end),
			
			(else_try),
				(assign, reg31, ":function"),
				(str_store_party_name, s31, ":center_no"),
				(display_message, "@ERROR - {s31} Patrol - Failed to update on function {reg31}.", qp_error_color),
			(try_end),
		
		# (else_try),
			# ### PATROL IS NOT ACTIVE ###
			# (call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DISBAND),
		(try_end),
	]),
	
# script_diplomacy_get_recruitment_score
# Calculates the recruitment rating for a given center to add recruits each "recruitment phase".
("diplomacy_get_recruitment_score",
	[
		(store_script_param_1, ":center_no"),
		
		(assign, ":rating", 0),
		(assign, ":pass", 1), # Assume the script will work.
		
		(try_for_range, ":slot", 0, 10),
			(store_add, ":primary_register", 30, ":slot"),
			(store_add, ":secondary_register", 40, ":slot"),
			(register_set, ":primary_register", 0),
			(register_set, ":secondary_register", 0),
		(try_end),
		
		(store_faction_of_party, ":faction_no", ":center_no"),
		(store_relation, ":faction_relation", "$players_kingdom", ":faction_no"),
		
		# Determine if the center is in a state to be contributing currently.
		(try_begin),
			### VILLAGES ###
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(this_or_next|party_slot_eq, ":center_no", slot_village_state, svs_being_raided),
			(this_or_next|party_slot_eq, ":center_no", slot_village_state, svs_looted),
			(party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
			(assign, ":pass", 0),
		(try_end),
		
		# If this is a village then determine if we own both village and castle/town it is bound to.
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
			(party_get_slot, ":owner_target", ":bound_center", slot_town_lord),
			(this_or_next|party_slot_eq, ":center_no", slot_town_lord, ":owner_target"),
			(party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
			(assign, ":village_owned_by_garrison_owner", 1),
		(else_try),
			(assign, ":village_owned_by_garrison_owner", 0),
		(try_end),
		
		# Determine the type of center we're dealing with.
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(assign, ":center_multiplier", 5),
			(str_store_string, s31, "@town"),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(assign, ":center_multiplier", 3),
			(str_store_string, s31, "@castle"),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(assign, ":center_multiplier", 2),
			(str_store_string, s31, "@village"),
		(else_try),
			(party_get_slot, reg1, ":center_no", slot_party_type),
			(display_message, "@ERROR (diplomacy): Recruitment request made of a party that is not a fief.", gpu_debug),
			(assign, ":center_multiplier", 0),
			(str_store_string, s31, "@unidentified"),
			(assign, ":pass", 0),
		(try_end),
		#(val_add, ":rating", ":center_type"),
		
		# Factor in the settlement's prosperity.
		(party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
		(assign, reg42, ":prosperity"), ## Diagnostic ##
		# (val_div, ":prosperity", 2),
		# (val_sub, ":prosperity", 20),
		# (val_clamp, ":prosperity", 0, 41),
		(val_sub, ":prosperity", 40),
		(val_mul, ":prosperity", 4),
		(val_clamp, ":prosperity", -20, 151),
		(val_mul, ":prosperity", ":center_multiplier"),
		(val_add, ":rating", ":prosperity"),
		
		# Factor in the settlement's distance from a potential target center. (Villages Only)
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			#(party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
			(store_distance_to_party_from_party, ":distance", ":bound_center", ":center_no"),
			(assign, reg43, ":distance"), ## Diagnostic ##
			(val_mul, ":distance", -2),
			(val_add, ":distance", 20),
			(val_clamp, ":distance", -30, 31),
			(val_mul, ":distance", ":center_multiplier"),
			(val_add, ":rating", ":distance"),
		(else_try),
			(assign, ":distance", 0),
		(try_end),
		
		# Factor in the Captain of the Guard attributes.
		(try_begin),
			# Ensure a Captain of the Guard is assigned to this center or its bound center if also owned by player.
			(assign, ":troop_no", -1),
			(try_begin),
				(is_between, ":center_no", walled_centers_begin, walled_centers_end),
				(party_get_slot, ":troop_no", ":center_no", slot_center_advisor_war),
			(else_try),
				(eq, ":village_owned_by_garrison_owner", 1),
				(party_get_slot, ":troop_no", ":bound_center", slot_center_advisor_war),
			(try_end),
			(is_between, ":troop_no", companions_begin, companions_end),
			(str_store_troop_name, s32, ":troop_no"), # Done for diagnostic reasons below.
			# Check renown of the advisor.
			(troop_get_slot, ":captain_renown", ":troop_no", slot_troop_renown),
			(assign, reg45, ":captain_renown"), ## Diagnostic ##
			(val_div, ":captain_renown", 3),
			(val_clamp, ":captain_renown", 0, 126),
			(val_mul, ":captain_renown", ":center_multiplier"),
			(val_add, ":rating", ":captain_renown"),
			# Check persuasion of the advisor.
			(store_skill_level, ":persuasion", "skl_persuasion", ":troop_no"),
			(assign, reg44, ":persuasion"), ## Diagnostic ##
			(val_mul, ":persuasion", 6),
			(val_clamp, ":persuasion", 0, 61),
			(val_mul, ":persuasion", ":center_multiplier"),
			(val_add, ":rating", ":persuasion"),
		(else_try),
			(assign, ":persuasion", 0),
			(assign, ":captain_renown", 0),
			(str_store_string, s32, "@unassigned"),
		(try_end),
		
		# Factor in the fief owner's renown.
		# Logic - This should only be beneficial if the target recruitment center owns the source recruitment center OR it is unassigned.
		(try_begin),
			# Castles & towns automatically get a pass since they aren't bound elsewhere.
			#(is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			# Make sure someone owns this fief.
			(this_or_next|is_between, ":town_lord", active_npcs_begin, active_npcs_end),
			(eq, ":town_lord", "trp_player"),
			(str_store_troop_name, s33, ":town_lord"), # Done for diagnostic reasons below.
			(troop_get_slot, ":lord_renown", ":town_lord", slot_troop_renown),
			(assign, reg46, ":lord_renown"), ## Diagnostic ##
			(val_div, ":lord_renown", 5),
			(val_clamp, ":lord_renown", 0, 201),
			(val_mul, ":lord_renown", ":center_multiplier"),
			(val_add, ":rating", ":lord_renown"),
		# (else_try),
			# (party_slot_eq, ":center_no", slot_party_type, spt_village),
			# # Since this is a village it only gets this benefit if its owner matches (or it is unassigned) that of the target castle or town.
			# (eq, ":village_owned_by_garrison_owner", 1),
			# # Since we now have the lord info for the target center and it either matches or we don't have a valid troop for this center let's use the target one.
			# (str_store_troop_name, s33, ":owner_target"), # Done for diagnostic reasons below.
			# (troop_get_slot, ":lord_renown", ":owner_target", slot_troop_renown),
			# (assign, reg46, ":lord_renown"), ## Diagnostic ##
			# (val_div, ":lord_renown", 5),
			# (val_clamp, ":lord_renown", 0, 201),
			# (val_mul, ":lord_renown", ":center_multiplier"),
			# (val_add, ":rating", ":lord_renown"),
		(else_try),
			(assign, ":lord_renown", 0),
			(str_store_string, s33, "@no lord"),
		(try_end),
		
		# Enhanced Diplomacy - Factor in recruitment influence at villages.
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(faction_get_slot, ":recruitment", ":faction_no", slot_faction_village_recruits),
			(assign, reg47, ":recruitment"), ## Diagnostic ##
			(val_mul, ":recruitment", 25),
			(val_clamp, ":recruitment", -100, 151),
			(val_mul, ":recruitment", ":center_multiplier"),
			(val_add, ":rating", ":recruitment"),
		(else_try),
			(assign, ":recruitment", 0),
		(try_end),
		
		# Factor in game difficulty.
		(try_begin),
			(this_or_next|eq, ":faction_no", "$players_kingdom"),
			(ge, ":faction_relation", 0), # if this center would be friendly then count it as an ally.
			(assign, ":difficulty_factor", -25),
		(else_try),
			(assign, ":difficulty_factor", 75),
		(try_end),
		(store_mul, ":difficulty", "$mod_difficulty", ":difficulty_factor"),
		(val_add, ":rating", ":difficulty"),
		(assign, reg38, ":difficulty"),
		
		# Factor in the mandatory conscription decree.
		(try_begin),
			(eq, "$diplomacy_force_recruit_enabled", 1), # Make sure we're even using this game option.
			(store_faction_of_party, ":faction_no", ":center_no"),
			(faction_slot_eq, ":faction_no", slot_faction_decree_conscription, 1), # Ensure conscription decree is active.
			(store_mul, ":conscription_bonus", ":rating", 3),
			(store_mul, ":conscription_limit", 350, ":center_multiplier"),
			(val_max, ":conscription_bonus", ":conscription_limit"),
			(try_begin),
				(ge, ":conscription_bonus", ":conscription_limit"),
				(assign, reg39, ":conscription_limit"),
			(else_try),
				(assign, reg39, ":conscription_bonus"),
			(try_end),
			(val_add, ":rating", reg39), # ":conscription_bonus"),
			# Sequence the penalties for having this active.
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(eq, "$diplomacy_apply_conscription_penalties", 1),
			(call_script, "script_change_player_relation_with_center", ":center_no", -3),
			(call_script, "script_change_center_prosperity", ":center_no", -3),
		(try_end),
		
		# Now finally check if we're keeping this rating at all.
		(try_begin),
			(eq, ":pass", 1),
			(try_begin),
				## DIAGNOSTICS ##
				(str_store_party_name, s30, ":center_no"),
				(assign, reg30, ":rating"),
				(assign, reg31, ":center_multiplier"),
				# s31 already holds a description of the center type.
				(assign, reg32, ":prosperity"),
				(assign, reg33, ":distance"),
				(assign, reg34, ":persuasion"),
				(assign, reg35, ":captain_renown"),
				# s32 already holds name of the Captain of the Guard.
				(assign, reg36, ":lord_renown"),
				# s33 already holds name of the town lord.
				(assign, reg37, ":recruitment"),
				(assign, reg38, ":difficulty"),
				(ge, DEBUG_DIPLOMACY, 1),
				(display_message, "@DEBUG (recruitment): {s30} received a recruitment rating of {reg30}.", gpu_debug),
				(ge, DEBUG_DIPLOMACY, 2),
				(display_message, "@DEBUG: All ratings multiplied by {reg31} due to being a {s31}.", gpu_debug),
				(try_begin), (neq, reg32, 0), (display_message, "@DEBUG: {reg32} due to a prosperity rating of {reg42}.", gpu_debug), (try_end),
				(try_begin), (neq, reg33, 0), (display_message, "@DEBUG: {reg33} due to a distance of {reg43}. (villages only)", gpu_debug), (try_end),
				(try_begin), (neq, reg34, 0), (display_message, "@DEBUG: {reg34} due to {s32}'s persuasion score of {reg44}.", gpu_debug), (try_end),
				(try_begin), (neq, reg35, 0), (display_message, "@DEBUG: {reg35} due to {s32}'s renown score of {reg45}.", gpu_debug), (try_end),
				(try_begin), (neq, reg36, 0), (display_message, "@DEBUG: {reg36} due to {s33}'s renown score of {reg46}.", gpu_debug), (try_end),
				(try_begin), (neq, reg37, 0), (display_message, "@DEBUG: {reg37} due to the faction's recruitment setting of {reg47}. (villages only)", gpu_debug), (try_end),
				(try_begin), (neq, reg38, 0), (display_message, "@DEBUG: {reg38} due to the game's difficulty setting.", gpu_debug), (try_end),
				(try_begin), (neq, reg39, 0), (display_message, "@DEBUG: {reg39} due to mandatory conscription. (villages only)", gpu_debug), (try_end),
				
			(try_end),
			# Output.
			(assign, reg1, ":rating"),
		(else_try),
			(assign, reg1, 0),
		(try_end),
	]),
	
# # script_diplomacy_describe_troop_to_s2
# # PURPOSE: Create a small descriptive line for a troop to show what types of attacks it has.
# ("diplomacy_describe_troop_to_s2",
	# [
		# (store_script_param_1, ":troop_no"),
		
		# (str_clear, s2),
		# (try_begin),
			# (troop_is_guarantee_ranged, ":troop_no"),
			# (assign, ":ranged", 1),
		# (else_try),
			# (assign, ":ranged", 0),
		# (try_end),
		# (try_begin),
			# (troop_is_guarantee_horse, ":troop_no"),
			# (assign, ":mounted", 1),
		# (else_try),
			# (troop_is_mounted, ":troop_no"),
			# (assign, ":mounted", 2),
		# (else_try),
			# (assign, ":mounted", 0),
		# (try_end),
		# (try_begin),
			# (eq, ":mounted", 1),
			# (eq, ":ranged", 1),
			# (str_store_string, s2, "@Mounted & Ranged Attack"),
		# (else_try),
			# (eq, ":mounted", 2),
			# (eq, ":ranged", 1),
			# (str_store_string, s2, "@Possibly Mounted & Ranged Attack"),
		# (else_try),
			# (eq, ":mounted", 1),
			# (str_store_string, s2, "@Mounted"),
		# (else_try),
			# (eq, ":mounted", 2),
			# (str_store_string, s2, "@Possibly Mounted"),
		# (else_try),
			# (eq, ":ranged", 1),
			# (str_store_string, s2, "@Ranged Attack"),
		# (else_try),
			# (str_store_string, s2, "@Melee on Foot"),
		# (try_end),
	# ]),
	
# script_diplomacy_determine_troop_tier
# PURPOSE: For a given troop ID determine how many tiers up in the upgrade system it is.
("diplomacy_determine_troop_tier",
	[
		(store_script_param, ":troop_no", 1),
		
		(troop_get_slot, reg1, ":troop_no", slot_troop_tier),
		
		# (assign, ":jumps", 1),
		# (assign, ":focus_troop", ":troop_no"),
		# (try_for_range, ":unused", 0, 10),
			# # To save on loop sizes we're going to take a sampling of the troop list and see if our upgrade troops are nearby first.
			# (store_sub, ":lower_limit", ":focus_troop", 20),
			# (store_add, ":upper_limit", ":focus_troop", 20),
			# (val_clamp, ":lower_limit", 1, "trp_end_of_troops"),
			# (val_clamp, ":upper_limit", 1, "trp_end_of_troops"),
			
			# # Cycle through our sampling for someone that upgrades to this troop type.
			# (assign, ":found_a_match", 0),
			# (try_for_range, ":sample_troop", ":lower_limit", ":upper_limit"),
				# (troop_get_upgrade_troop, ":path_1", ":sample_troop", 0),
				# (troop_get_upgrade_troop, ":path_2", ":sample_troop", 1),
				# # Check if this troop upgrades into the one we want.  Most troops should fail this set of checks.
				# (this_or_next|eq, ":path_1", ":focus_troop"),
				# (eq, ":path_2", ":focus_troop"),
				# # Make sure if this is a tier 1 faction troop we don't count bandits that lead to it.
				# (assign, ":pass", 1),
				# (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
					# (faction_get_slot, ":culture_no", ":kingdom_no"),
					# (faction_slot_eq, ":culture_no", slot_faction_tier_1_troop, ":focus_troop"),
					# (assign, ":pass", 0),
				# (try_end),
				# (eq, ":pass", 1),
				# # This is a valid troop so let's shift our focus to it.
				# (assign, ":focus_troop", ":sample_troop"),
				# (val_add, ":jumps", 1),
				# (assign, ":found_a_match", 1),
				# (break_loop),
			# (try_end),
			
			# # In the event that we failed to find a match in our smaller loop then we'll have to try a larger one.
			# (eq, ":found_a_match", 0),
			# (try_for_range, ":sample_troop", 1, "trp_end_of_troops"),
				# (troop_get_upgrade_troop, ":path_1", ":sample_troop", 0),
				# (troop_get_upgrade_troop, ":path_2", ":sample_troop", 1),
				# # Check if this troop upgrades into the one we want.  Most troops should fail this set of checks.
				# (this_or_next|eq, ":path_1", ":focus_troop"),
				# (eq, ":path_2", ":focus_troop"),
				# # Make sure if this is a tier 1 faction troop we don't count bandits that lead to it.
				# (assign, ":pass", 1),
				# (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
					# (faction_get_slot, ":culture_no", ":kingdom_no", slot_faction_culture),
					# (faction_slot_eq, ":culture_no", slot_faction_tier_1_troop, ":focus_troop"),
					# (assign, ":pass", 0),
				# (try_end),
				# (eq, ":pass", 1),
				# # This is a valid troop so let's shift our focus to it.
				# (assign, ":focus_troop", ":sample_troop"),
				# (val_add, ":jumps", 1),
				# (assign, ":found_a_match", 1),
				# (break_loop),
			# (try_end),
			
			# # If we still haven't found a match then it is time to stop looking for this troop's starting point as this troop is a tier 1.
			# (eq, ":found_a_match", 0),
			# (break_loop),
		# (try_end),
		
		# (assign, reg1, ":jumps"),
	]),
	
# # script_diplomacy_initialize_troop_upgrade_options
# # PURPOSE: Sets the initial training options for a given troop.  This is intended to be used at game start to setup every troop in the game's options or to reboot an individual troop's options.
# ("diplomacy_initialize_troop_upgrade_options",
	# [
		# (store_script_param, ":troop_no", 1),
		
		# # Determine how many upgrade paths this troop has available.
		# (troop_get_upgrade_troop, ":path_1", ":troop_no", 0),
		# (troop_get_upgrade_troop, ":path_2", ":troop_no", 1),
		# (assign, ":count", 0),
		# (try_begin),
			# (neq, ":path_1", 0),
			# (val_add, ":count", 1),
		# (try_end),
		# (try_begin),
			# (neq, ":path_2", 0),
			# (val_add, ":count", 1),
		# (try_end),
		
		# # Determine the split each path should get based on the number of paths.
		# (try_begin),
			# (ge, ":count", 3),
			# (assign, ":chance", 0),
			# (str_store_troop_name, s31, ":troop_no"),
			# (display_message, "@ERROR - Troop {s31} has more than two upgrade paths."),
		# (else_try),
			# (eq, ":count", 2),
			# (assign, ":chance", 50),
		# (else_try),
			# (eq, ":count", 1),
			# (assign, ":chance", 100),
		# (else_try),
			# (eq, ":count", 0),
			# (assign, ":chance", 0),
		# (else_try),
			# (assign, ":chance", 100), # Should not ever be possible give the above options, but just in case.
		# (try_end),
		
		# # Now assign each upgrade path it's given chance.
		# (try_begin),
			# (neq, ":path_1", 0),
			# (troop_set_slot, ":troop_no", slot_troop_upgrade_chance_1, ":chance"),
		# (try_end),
		# (try_begin),
			# (neq, ":path_2", 0),
			# (troop_set_slot, ":troop_no", slot_troop_upgrade_chance_2, ":chance"),
		# (try_end),
		
		# (try_begin),
			# (ge, DEBUG_DIPLOMACY, 2),
			# (assign, reg31, ":chance"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (display_message, "@DEBUG (diplomacy): Upgrade chances for {s31} has been reset to {reg31}%.", gpu_debug),
		# (try_end),
	# ]),
	
# script_diplomacy_advisors_flee_the_castle
# If a castle that an advisor is stationed at is lost then the advisor is setup to rejoin the companions that move around the map.
("diplomacy_advisors_flee_the_castle",
	[
		(store_script_param_1, ":center_no"),
		
		(try_begin),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(try_for_range, ":advisor_slot", advisors_begin, advisors_end),
				(call_script, "script_diplomacy_remove_advisor", ":center_no", ":advisor_slot", ADVISOR_FLEES),
			(try_end),
		(try_end),
	]),
	
# script_diplomacy_reset_adviser_slots
# Cycles through every castle & town and if a companion is currently set to an adviser role updates their slots properly.
("diplomacy_reset_adviser_slots",
	[
		# Initialize every companion's current status to 0.
		(try_for_range, ":troop_no", companions_begin, companions_end),
			(troop_set_slot, ":troop_no", slot_troop_advisor_station, 0),
			(troop_set_slot, ":troop_no", slot_troop_advisor_role, 0),
		(try_end),
		
		# Cycle through each castle & town and search for current advisers.
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(try_for_range, ":advisor_slot", advisors_begin, advisors_end),
				(party_get_slot, ":troop_no", ":center_no", ":advisor_slot"),
				(is_between, ":troop_no", companions_begin, companions_end),
				(troop_set_slot, ":troop_no", slot_troop_advisor_station, ":center_no"),
				(troop_set_slot, ":troop_no", slot_troop_advisor_role, ":advisor_slot"),
				(ge, DEBUG_DIPLOMACY, 1), # Advisor detected.
				(str_store_troop_name, s21, ":troop_no"),
				(str_store_party_name, s22, ":center_no"),
				# Name the position.
				(store_sub, ":advisor_no", ":advisor_slot", advisors_begin),
				(store_add, ":string_no", ":advisor_no", "str_diplomacy_advisor_steward"),
				(str_store_string, s23, ":string_no"),
				(display_message, "@{s21} is detected serving as {s23} in {s22}.", gpu_debug),
			(try_end),
		(try_end),
	]),
	
# script_diplomacy_remove_advisor
# PURPOSE: Remove a companion advisor from a given center.
# EXAMPLE: (call_script, "script_diplomacy_remove_advisor", ":center_no", ":advisor_no", ADVISOR_BEGIN_RETURN_MISSION),
("diplomacy_remove_advisor",
	[
		(store_script_param, ":center_no", 1),
		(store_script_param, ":advisor_slot", 2),
		(store_script_param, ":return_to_party", 3),
		
		# Remove any currently assigned advisor.
		(party_get_slot, ":troop_no", ":center_no", ":advisor_slot"),
		
		(try_begin),
			(is_between, ":troop_no", companions_begin, companions_end),
			# Decide if the companion is being returned to the player party or not.
			(try_begin),
				### ADVISOR_FLEES ###
				(eq, ":return_to_party", ADVISOR_FLEES),
				(is_between, ":troop_no", companions_begin, companions_end),
				#(party_set_slot, ":center_no", ":advisor_slot", -1),
				(troop_set_slot, ":troop_no", slot_troop_days_on_mission, 0),
				(troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive),
				(troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
				
				(try_begin),
					(this_or_next|ge, DEBUG_DIPLOMACY, 1),
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(str_store_troop_name, s41, ":troop_no"),
					(str_store_party_name, s42, ":center_no"),
					(try_begin),
						(party_slot_eq, ":center_no", slot_party_type, spt_town),
						(troop_set_slot, ":troop_no", slot_troop_cur_center, ":center_no"), # Start them at their last known location for the rotation.
						(str_store_string, s23, "@{s41} has escaped from the castle in {s42} and gone into hiding within the town."),
					(else_try),
						(call_script, "script_qus_select_random_center", center_is_town, 1, 35, ":center_no"),
						(assign, ":target_center", reg1),
						(troop_set_slot, ":troop_no", slot_troop_cur_center, ":target_center"), # Find a nearby town to start over in.
						(str_store_string, s23, "@{s41} has fled from {s42} and gone into hiding."),
					(try_end),
					(display_message, "@{s23}", gpu_debug),
				(try_end),
				
			(else_try),
				### ADVISOR_RETURNS_TO_PARTY ###
				(eq, ":return_to_party", ADVISOR_RETURNS_TO_PARTY),
				(is_between, ":troop_no", companions_begin, companions_end),
				(party_add_members, "p_main_party", ":troop_no", 1),
				(str_store_troop_name, s21, ":troop_no"),
				(display_message, "@{s21} has rejoined your party.", gpu_green),
				
			(else_try),
				### ADVISOR_RETURN_IF_NEARBY ###
				(eq, ":return_to_party", ADVISOR_RETURN_IF_NEARBY),
				(is_between, ":troop_no", companions_begin, companions_end),
				(try_begin),
					(eq, "$g_encountered_party", ":center_no"),
					(call_script, "script_diplomacy_remove_advisor", ":center_no", ":advisor_slot", ADVISOR_RETURNS_TO_PARTY),
				(else_try),
					(call_script, "script_diplomacy_remove_advisor", ":center_no", ":advisor_slot", ADVISOR_FLEES),
				(try_end),
				
			(else_try),
				### ADVISOR_BEGIN_RETURN_MISSION ###
				(eq, ":return_to_party", ADVISOR_BEGIN_RETURN_MISSION),
				(is_between, ":troop_no", companions_begin, companions_end),
				(store_distance_to_party_from_party, ":distance", ":center_no", "p_main_party"),
				(val_clamp, ":distance", 1, 15),
				(troop_set_slot, ":troop_no", slot_troop_days_on_mission, ":distance"),
				(troop_set_slot, ":troop_no", slot_troop_current_mission, npc_mission_rejoin_when_possible),
				(troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
				(try_begin),
					# (this_or_next|ge, DEBUG_DIPLOMACY, 1),
					# (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(str_store_troop_name, s21, ":troop_no"),
					(str_store_party_name, s22, ":center_no"),
					(assign, reg21, ":distance"),
					(display_message, "@{s21} has left {s22} and should rejoin the party in {reg21} days.", gpu_green),
				(try_end),
				
			(else_try),
				### ERROR ###
				(str_store_troop_name, s31, ":troop_no"),
				(str_store_party_name, s32, ":center_no"),
				(assign, reg31, ":return_to_party"),
				(display_message, "@ERROR (advisors) - Invalid 'return to party' setting [{reg31}] when removing {s31} from {s32}.", gpu_red),
			(try_end),
			
			# Clean out advisor slots.
			(party_set_slot, ":center_no", ":advisor_slot", 0),
			(troop_set_slot, ":troop_no", slot_troop_advisor_station, 0),
			(troop_set_slot, ":troop_no", slot_troop_advisor_role, 0),
			
			## ADVISOR SPECIFICS ##
			(try_begin),
				### ADVISOR: CASTLE STEWARD ###
				(eq, ":advisor_slot", slot_center_steward),
				(neq, ":return_to_party", ADVISOR_RETURN_IF_NEARBY), # Since this will have already processed.
				# Cancel any active Quest Pack 3 quests.
				(try_for_range, ":quest_no", qp3_quests_begin, qp3_quests_end),
					(check_quest_active, ":quest_no"),
					(neq, ":quest_no", "qst_mercs_for_hire"), # No need for canceling this.
					(str_store_quest_name, s21, ":quest_no"),
					(cancel_quest, ":quest_no"),
					(display_message, "@Quest '{s21}' canceled due to the quest originator being removed."),
				(try_end),
				
			(else_try),
				### ADVISOR: CAPTAIN OF THE GUARD ###
				(eq, ":advisor_slot", slot_center_advisor_war),
				(neq, ":return_to_party", ADVISOR_RETURN_IF_NEARBY), # Since this will have already processed.
				# Disband any active patrols from this center.
				(call_script, "script_diplomacy_order_all_patrols_of_center", ":center_no", PATROL_DISBAND),
				# Disable any active garrison recruiting.
				(party_set_slot, ":center_no", slot_center_recruiting, 0),
				# Disable active upgrading in this center.
				(party_set_slot, ":center_no", slot_center_upgrade_garrison, 0),
				# Remove treasury income.
				(party_set_slot, ":center_no", slot_center_income_to_treasury, 0),
				
			(try_end),
		(try_end),
	]),
	
###########################################################################################################################
#####                                                MESSAGE FILTER                                                   #####
###########################################################################################################################

# script_cf_diplomacy_message_filter
# Replaces the native script for changing right to rule to provide more information and color highlighting.
("cf_diplomacy_message_filter",
	[
		(store_script_param, ":side_a", 1), # good side of the conflict
		(store_script_param, ":context_a", 2),
		(store_script_param, ":side_b", 3), # bad side of the conflict
		(store_script_param, ":context_b", 4),
		
		(assign, ":display", 0),
		(try_begin),
			### CENTERS : GOOD ###
			(eq, ":context_a", context_center),
			(ge, ":side_a", 0),
			(store_faction_of_party, ":faction_no", ":side_a"),
			(eq, ":faction_no", "$players_kingdom"),
			(assign, ":display", 1),
			(assign, ":color", gpu_green),
		(else_try),
			### CENTERS : BAD ###
			(eq, ":context_b", context_center),
			(ge, ":side_b", 0),
			(store_faction_of_party, ":faction_no", ":side_b"),
			(eq, ":faction_no", "$players_kingdom"),
			(assign, ":display", 1),
			(assign, ":color", gpu_red),
		(else_try),
			### PARTY : GOOD ###
			(eq, ":context_a", context_party),
			(ge, ":side_a", 0),
			(store_faction_of_party, ":faction_no", ":side_a"),
			(eq, ":faction_no", "$players_kingdom"),
			(assign, ":display", 1),
			(assign, ":color", gpu_green),
		(else_try),
			### PARTY : BAD ###
			(eq, ":context_b", context_party),
			(ge, ":side_b", 0),
			(store_faction_of_party, ":faction_no", ":side_b"),
			(eq, ":faction_no", "$players_kingdom"),
			(assign, ":display", 1),
			(assign, ":color", gpu_red),
		(else_try),
			### TROOP : GOOD ###
			(eq, ":context_a", context_troop),
			(ge, ":side_a", 0),
			(store_faction_of_troop, ":faction_no", ":side_a"),
			(eq, ":faction_no", "$players_kingdom"),
			(assign, ":display", 1),
			(assign, ":color", gpu_green),
		(else_try),
			### TROOP : BAD ###
			(eq, ":context_b", context_troop),
			(ge, ":side_b", 0),
			(store_faction_of_troop, ":faction_no", ":side_b"),
			(eq, ":faction_no", "$players_kingdom"),
			(assign, ":display", 1),
			(assign, ":color", gpu_red),
		(else_try),
			### FACTION : GOOD ###
			(eq, ":context_a", context_faction),
			(ge, ":side_a", 0),
			(eq, ":side_a", "$players_kingdom"),
			(assign, ":display", 1),
			(assign, ":color", gpu_green),
		(else_try),
			### FACTION : BAD ###
			(eq, ":context_b", context_faction),
			(ge, ":side_b", 0),
			(eq, ":side_b", "$players_kingdom"),
			(assign, ":display", 1),
			(assign, ":color", gpu_red),
		(else_try),
			(eq, "$diplomacy_filter_enabled", 0),
			(assign, ":display", 1),
			(assign, ":color", gpu_white),
		(try_end),
		(assign, reg1, ":color"),
		(eq, ":display", 1), ## CONDITIONAL BREAK ##
	]),  
   	
###########################################################################################################################
#####                                              DISPLAY RECOLORING                                                 #####
###########################################################################################################################

# script_change_player_right_to_rule
# Replaces the native script for changing right to rule to provide more information and color highlighting.
("change_player_right_to_rule",
	[
		(store_script_param_1, ":right_to_rule_dif"),
		
		(assign, ":initial_value", "$player_right_to_rule"),
		(val_add, "$player_right_to_rule", ":right_to_rule_dif"),
		(val_clamp, "$player_right_to_rule", 0, 100),
		(try_begin),
			(neq, "$player_right_to_rule", ":initial_value"),
			(assign, reg21, "$player_right_to_rule"),
			(store_sub, reg22, "$player_right_to_rule", ":initial_value"),
			(try_begin),
				(gt, ":right_to_rule_dif", 0),
				(display_message, "@Your right to rule has risen to {reg21}. (+{reg22})", gpu_green),
			(else_try),
				(lt, ":right_to_rule_dif", 0),
				(display_message, "@Your right to rule has lowered to {reg21}. ({reg22})", gpu_red),
			(try_end),
		(try_end),
	]),  
   
# script_change_player_honor
# Replaces the native script for changing honor to provide more information and color highlighting.
("change_player_honor",
    [
		(store_script_param_1, ":honor_dif"),
		
		(val_add, "$player_honor", ":honor_dif"),
		(assign, reg21, ":honor_dif"),
		(try_begin),
			(gt, ":honor_dif", 0),
			(display_message, "@You gain {reg21} honour.", gpu_green),
		(else_try),
			(lt, ":honor_dif", 0),
			#(val_mul, ":honor_dif", -1),
			(display_message, "@You lose {reg21} honour.", gpu_red),
		(try_end),
	]),
	
###########################################################################################################################
#####                                           EXPANDED PRISONER DIALOG                                              #####
###########################################################################################################################

# script_diplomacy_rate_kingdom_strength
# Compares various aspects of the kingdom's power and returns a rating via reg1.
("diplomacy_rate_kingdom_strength",
    [
		(store_script_param_1, ":faction_no"),
		
		### COMPARE STRENGTH OF KINGDOM ###
		# Compare number of walled centers.  (15 points for towns, 10 points for castles)
		(assign, ":rating_centers", 0),
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(store_faction_of_party, ":center_faction", ":center_no"),
			(eq, ":center_faction", ":faction_no"),
			(val_add, ":rating_centers", 15),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(val_add, ":rating_centers", 10),
		(try_end),
		
		# Compare number of vassals.  (7 points for free vassal, 4 point for imprisoned one)
		(assign, ":rating_vassals", 0),
		(try_for_range, ":vassal_no", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":vassal_faction", ":vassal_no"),
			(eq, ":vassal_faction", ":faction_no"),
			(val_add, ":rating_vassals", 4),
			(troop_slot_eq, ":vassal_no", slot_troop_prisoner_of_party, -1), # Not a prisoner.
			(val_add, ":rating_vassals", 7),
		(try_end),
		
		# Compare average relation of vassals with liege. (-30 to +100 from average of relations)
		(assign, ":rating_relation", 0),
		(assign, ":number_of_vassals", 0), 
		(try_for_range, ":vassal_no", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":vassal_faction", ":vassal_no"),
			(eq, ":vassal_faction", ":faction_no"),
			(neg|faction_slot_eq, ":faction_no", slot_faction_leader, ":vassal_no"), # Don't count the king.
			(val_add, ":number_of_vassals", 1),
			(faction_get_slot, ":liege", ":faction_no", slot_faction_leader),
			(call_script, "script_troop_get_relation_with_troop", ":vassal_no", ":liege"),
			(val_add, ":rating_relation", reg0),
		(try_end),
		(val_max, ":number_of_vassals", 1), # Prevent Div/0 errors.
		(val_div, ":rating_relation", ":number_of_vassals"),
		
		# Consider number of active wars. (-25 for each active war)
		(assign, ":number_of_wars", 0),
		(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
			(faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
			(store_relation, ":relation", ":kingdom_no", ":faction_no"),
			(lt, ":relation", 0),
			(val_add, ":number_of_wars", 1),
		(try_end),
		(store_mul, ":rating_wars", ":number_of_wars", -25),
		
		(assign, ":rating_total", 0),
		(val_add, ":rating_total", ":rating_centers"),
		(val_add, ":rating_total", ":rating_vassals"),
		(val_add, ":rating_total", ":rating_relation"),
		(val_add, ":rating_total", ":rating_wars"),
		
		### DIAGNOSTIC ###
		#(str_store_faction_name, s31, ":faction_no"),
		(assign, reg31, ":rating_total"),
		(assign, reg32, ":rating_centers"),
		(assign, reg33, ":rating_vassals"),
		(assign, reg34, ":rating_relation"),
		(assign, reg35, ":rating_wars"),
		#(display_message, "@Faction: [{s31}] = {reg31} rating = +{reg32} centers +{reg33} vassals +{reg34} relation + {reg35} wars."),
		
		(assign, reg1, ":rating_total"),
	]),
	
# script_diplomacy_change_troop_faction
# Input: arg1 = troop_no, arg2 = faction
("diplomacy_change_troop_faction",
    [
      (store_script_param_1, ":troop_no"),
      (store_script_param_2, ":faction_no"),
      (try_begin),
        #Reactivating inactive or defeated faction
        (is_between, ":faction_no", kingdoms_begin, kingdoms_end),
        (neg|faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (faction_set_slot, ":faction_no", slot_faction_state, sfs_active),
        #(call_script, "script_store_average_center_value_per_faction"),
      (try_end),

	  #Political ramifications
	  (store_faction_of_troop, ":orig_faction", ":troop_no"),
	  
	  #remove if he is marshal
	  (try_begin),
		(faction_slot_eq, ":orig_faction", slot_faction_marshall, ":troop_no"),
        (call_script, "script_check_and_finish_active_army_quests_for_faction", ":orig_faction"),       

		#No current issue on the agenda
		(try_begin),
			(faction_slot_eq, ":orig_faction", slot_faction_political_issue, 0),
		
			(faction_set_slot, ":orig_faction", slot_faction_political_issue, 1), #Appointment of marshal
			(store_current_hours, ":hours"),
			(val_max, ":hours", 0),
			(faction_set_slot, ":orig_faction", slot_faction_political_issue_time, ":hours"), #Appointment of marshal
			(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
				(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
				(eq, ":active_npc_faction", ":orig_faction"),
				(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
			(try_end),		
			(try_begin),
				(eq, "$players_kingdom", ":orig_faction"),
				(troop_set_slot, "trp_player", slot_troop_stance_on_faction_issue, -1),
			(try_end),		
		(try_end),
		
        (try_begin),
		  (troop_get_slot, ":old_marshall_party", ":troop_no", slot_troop_leaded_party),
          (party_is_active, ":old_marshall_party"),
          (party_set_marshall, ":old_marshall_party", 0),
        (try_end),  

		(faction_set_slot, ":orig_faction", slot_faction_marshall, -1),
	  (try_end),
	  #Removal as marshal ends
	  
	  #Other political ramifications
	  (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
	  (try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":active_npc", slot_troop_stance_on_faction_issue, ":troop_no"),
		(troop_set_slot, ":active_npc", slot_troop_stance_on_faction_issue, -1),
	  (try_end),
	  #Political ramifications end
	  
	  
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed in normal faction change"), 
		(try_end),
	  
      (troop_set_faction, ":troop_no", ":faction_no"),
      (troop_set_slot, ":troop_no", slot_troop_recruitment_random, 0),
      (troop_set_slot, ":troop_no", slot_lord_recruitment_argument, 0),
      (troop_set_slot, ":troop_no", slot_lord_recruitment_candidate, 0),
      (troop_set_slot, ":troop_no", slot_troop_promised_fief, 0),

      #Give new title
      (call_script, "script_troop_set_title_according_to_faction", ":troop_no", ":faction_no"),
      
      (try_begin),
        (this_or_next|eq, ":faction_no", "$players_kingdom"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
        (call_script, "script_check_concilio_calradi_achievement"),
      (try_end),

	  #Takes walled centers and dependent villages with him
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
        (party_set_faction, ":center_no", ":faction_no"),
        (try_for_range, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
          (party_set_faction, ":village_no", ":faction_no"),
          (party_get_slot, ":farmer_party_no", ":village_no", slot_village_farmer_party),
          (try_begin),
            (gt, ":farmer_party_no", 0),
            (party_is_active, ":farmer_party_no"),
            (party_set_faction, ":farmer_party_no", ":faction_no"),
          (try_end),
          (try_begin),
            (party_get_slot, ":old_town_lord", ":village_no", slot_town_lord),
            (neq, ":old_town_lord", ":troop_no"),
            #(party_set_slot, ":village_no", slot_town_lord, stl_unassigned), # Every lord is being moved so don't unassign this.
          (try_end),
        (try_end),
      (try_end),
	  
	  #Dependant kingdom ladies switch faction
	  (try_for_range, ":kingdom_lady", kingdom_ladies_begin, kingdom_ladies_end),
		(call_script, "script_get_kingdom_lady_social_determinants", ":kingdom_lady"),
		(assign, ":closest_male_relative", reg0),
		(assign, ":new_center", reg1),
		
		(eq, ":closest_male_relative", ":troop_no"),
		
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":kingdom_lady"),
			(display_message, "@{!}DEBUG - {s4} faction changed by guardian moving"), 
		(try_end),
		
		(troop_set_faction, ":kingdom_lady", ":faction_no"),
		(troop_slot_eq, ":kingdom_lady", slot_troop_prisoner_of_party, -1),
		(troop_set_slot, ":kingdom_lady", slot_troop_cur_center, ":new_center"),
	  (try_end),
	  
	  #Remove his control over villages under another fortress
      (try_for_range, ":village_no", villages_begin, villages_end),
        (party_slot_eq, ":village_no", slot_town_lord, ":troop_no"),
        (store_faction_of_party, ":village_faction", ":village_no"),
        (try_begin),
          (neq, ":village_faction", ":faction_no"),
          (party_set_slot, ":village_no", slot_town_lord, stl_unassigned),
        (try_end),
      (try_end),
	  
	  #Free prisoners
      (try_begin),
        (troop_get_slot, ":leaded_party", ":troop_no", slot_troop_leaded_party),
        (gt, ":leaded_party", 0),
        (party_set_faction, ":leaded_party", ":faction_no"),
        (party_get_num_prisoner_stacks, ":num_stacks", ":leaded_party"),
        (try_for_range_backwards, ":troop_iterator", 0, ":num_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_troop_id", ":leaded_party", ":troop_iterator"),
          (store_troop_faction, ":cur_faction", ":cur_troop_id"),
          (troop_is_hero, ":cur_troop_id"),
          (eq, ":cur_faction", ":faction_no"),
          (call_script, "script_remove_troop_from_prison", ":cur_troop_id"),
          (party_remove_prisoners, ":leaded_party", ":cur_troop_id", 1),
        (try_end),
      (try_end),
	  
	  #Annull all quests of which the lord is giver
	  (try_for_range, ":quest", all_quests_begin, all_quests_end),
		(check_quest_active, ":quest"),
		(quest_slot_eq, ":quest", slot_quest_giver_troop, ":troop_no"),
		
		(str_store_troop_name, s4, ":troop_no"),
		(try_begin),
		  (eq, "$cheat_mode", 1),
  		  (display_message, "str_s4_changing_sides_aborts_quest"),
        (try_end),
		(call_script, "script_abort_quest", ":quest", 0),
	  (try_end),
	  
	  #Boot all lords out of centers whose faction has changed
	  (try_for_range, ":lord_to_move", active_npcs_begin, active_npcs_end),
		(troop_get_slot, ":lord_led_party", ":lord_to_move", slot_troop_leaded_party),
	    (party_is_active, ":lord_led_party"),
		(party_get_attached_to, ":led_party_attached", ":lord_led_party"),
		(is_between, ":led_party_attached", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":led_party_faction", ":lord_led_party"),
		(store_faction_of_party, ":attached_party_faction", ":led_party_attached"),
		(neq, ":led_party_faction", ":attached_party_faction"),
		
		(party_detach, ":lord_led_party"),
	  (try_end),
	  
	  #Increase relation with lord in new faction by 5
	  #Or, if player kingdom, make inactive pending confirmation
	  (faction_get_slot, ":faction_liege", ":faction_no", slot_faction_leader),
	  (try_begin),
		(eq, ":faction_liege", "trp_player"),
		(neq, ":troop_no", "$g_talk_troop"),
	    (troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive), #POSSIBLE REASON 1
	  (else_try),
		(is_between, ":faction_liege", active_npcs_begin, active_npcs_end),
		(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
		(call_script, "script_troop_change_relation_with_troop", ":faction_liege", ":troop_no", 5),
		(val_add, "$total_indictment_changes", 5),
	  (try_end),
	  
	  #Break courtship relations
	  (try_begin),
	  	(troop_slot_ge, ":troop_no", slot_troop_spouse, 0),
		#Already married, do nothing
	  (else_try),
		(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
	    (try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
			(troop_get_slot, ":courted_lady", ":troop_no", ":love_interest_slot"),
			(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":courted_lady", ":troop_no"),
	    (try_end),
		(call_script, "script_assign_troop_love_interests", ":troop_no"),
	  (else_try),	
		(is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
			(try_for_range, ":love_interest_slot", slot_troop_love_interest_1, slot_troop_love_interests_end),
				(troop_slot_eq, ":active_npc", ":love_interest_slot", ":troop_no"),
				(call_script, "script_courtship_event_lady_break_relation_with_suitor", ":troop_no", ":active_npc"),
			(try_end),
		(try_end),
	  (try_end),
	  
	  #Stop raidings/sieges of new faction's fief if there is any
	  (troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
	  (try_for_range, ":center_no", centers_begin, centers_end),
	    (party_slot_eq, ":center_no", slot_party_type, spt_village),
	    (party_get_slot, ":raided_by", ":center_no", slot_village_raided_by),	    
	    (eq, ":raided_by", ":troop_party"),
	    (party_set_slot, ":center_no", slot_village_raided_by, -1),
	    (try_begin),
	      (party_slot_eq, ":center_no", slot_village_state, svs_being_raided),	      
	      (party_set_slot, ":center_no", slot_village_state, svs_normal),
	      (party_set_extra_text, ":center_no", "str_empty_string"),
	    (try_end),
	  (else_try),  	    
	    (party_get_slot, ":besieged_by", ":center_no", slot_center_is_besieged_by),
	    (eq, ":besieged_by", ":troop_party"),
	    (party_set_slot, ":center_no", slot_center_is_besieged_by, -1),
	    (try_begin),	    
	      (party_slot_eq, ":center_no", slot_village_state, svs_under_siege),	      
	      (party_set_slot, ":center_no", slot_village_state, svs_normal),
	      (party_set_extra_text, ":center_no", "str_empty_string"),
	    (try_end),
	  (try_end),
	  	  
      (call_script, "script_update_all_notes"),

      (call_script, "script_update_village_market_towns"),
      (assign, "$g_recalculate_ais", 1),
      ]),
	  
###########################################################################################################################
#####                                          KINGDOM MANAGEMENT SYSTEM                                              #####
###########################################################################################################################

# script_diplomacy_reset_policy_defaults
# Sets the initial default policy, decree and data values for a generic faction.
("diplomacy_reset_policy_defaults",
	[
		(store_script_param_1, ":faction_no"),
		
		### DOMESTIC POLICIES ###
		(try_for_range, ":slot", diplomacy_policies_begin, diplomacy_policies_end),
			(faction_set_slot, ":faction_no", ":slot", POLICY_STAGE_NEUTRAL),
		(try_end),
		
		### ROYAL DECREES ###
		(try_for_range, ":slot", diplomacy_decrees_begin, diplomacy_decrees_end),
			(faction_set_slot, ":faction_no", ":slot", 0),
		(try_end),
		
		### POLICY DATA ###
		# Initially set them all to 0.
		(try_for_range, ":slot", diplomacy_policy_data_begin, diplomacy_policy_data_end),
			(faction_set_slot, ":faction_no", ":slot", 0),
		(try_end),
		# Now set specific values to their defaults.
		(faction_set_slot, ":faction_no", slot_faction_desertion_factor, 4),
		(faction_set_slot, ":faction_no", slot_faction_desertion_threshold, 32),
		(faction_set_slot, ":faction_no", slot_faction_unity_top_faction, 1),
		(faction_set_slot, ":faction_no", slot_faction_unity_bottom_faction, 3),
		(faction_set_slot, ":faction_no", slot_faction_unity_top_nonfaction, 1),
		(faction_set_slot, ":faction_no", slot_faction_unity_bottom_nonfaction, 1),
		(faction_set_slot, ":faction_no", slot_faction_unity_top_mercs, 2),
		(faction_set_slot, ":faction_no", slot_faction_unity_bottom_mercs, 1),
		(faction_set_slot, ":faction_no", slot_faction_march_unrest, 2),
		(faction_set_slot, ":faction_no", kms_val_data_slaver_availability, diplomacy_default_slaver_availability),
	]),  
	
# script_diplomacy_calculate_policy_data_values
# Figures out what a specific policy's data value should be based upon all inputs.
("diplomacy_calculate_policy_data_values",
	[
		(store_script_param, ":tooltip_scope", 1),
		
		# TOOLTIP_DIPLOMACY_SUMMARY            = 1
		# TOOLTIP_POLICY_CULTURAL_FOCUS        = 2
		# TOOLTIP_POLICY_MILITARY_DIVERSITY    = 3
		# TOOLTIP_POLICY_BORDER_CONTROLS       = 4
		# TOOLTIP_POLICY_SLAVERY               = 5
		# TOOLTIP_POLICY_TROOP_DESERTION       = 6
		# TOOLTIP_DECREE_CONSCRIPTION          = 7
		# TOOLTIP_DECREE_CODE_OF_LAW_COMMON    = 8
		# TOOLTIP_DECREE_CODE_OF_LAW_NOBLE     = 9
		# TOOLTIP_DECREE_WAR_TAXATION          = 10
		# TOOLTIP_DECREE_SANITATION            = 11
		# TOOLTIP_DECREE_RECONSTRUCTION        = 12
		# TOOLTIP_DECREE_PUBLIC_EXECUTIONS     = 13

		# Get policy values.
		(troop_get_slot, ":policy_focus",           KMS_OBJECTS, kms_val_policy_culture_focus),
		(troop_get_slot, ":policy_diversity",       KMS_OBJECTS, kms_val_policy_mil_diversity),
		(troop_get_slot, ":policy_borders",         KMS_OBJECTS, kms_val_policy_border_control),
		(troop_get_slot, ":policy_slavery",         KMS_OBJECTS, kms_val_policy_slavery),
		(troop_get_slot, ":policy_desertion",       KMS_OBJECTS, kms_val_policy_desertion),
		# Get decree values.
		(troop_get_slot, ":decree_conscription",    KMS_OBJECTS, kms_val_decree_conscription),
		(troop_get_slot, ":decree_common_laws",     KMS_OBJECTS, kms_val_decree_laws_commons),
		(troop_get_slot, ":decree_noble_laws",      KMS_OBJECTS, kms_val_decree_laws_nobles),
		(troop_get_slot, ":decree_war_taxes",       KMS_OBJECTS, kms_val_decree_war_taxes),
		(troop_get_slot, ":decree_sanitation",      KMS_OBJECTS, kms_val_decree_sanitation),
		(troop_get_slot, ":decree_reconstruction",  KMS_OBJECTS, kms_val_decree_reconstruction),
		(troop_get_slot, ":decree_executions",      KMS_OBJECTS, kms_val_decree_executions),
		
		# Initialize data variables.
		(assign, ":data_village_recruits", 0),
		(assign, ":data_desertion_factor", 4),
		(assign, ":data_desertion_threshold", 32),
		(assign, ":data_unity_top_faction", 1),
		(assign, ":data_unity_bot_faction", 3),
		(assign, ":data_unity_top_nonfaction", 1),
		(assign, ":data_unity_bot_nonfaction", 1),
		(assign, ":data_unity_top_mercs", 2),
		(assign, ":data_unity_bot_mercs", 1),
		(assign, ":data_center_income", 0),
		(assign, ":data_army_size", 0),
		(assign, ":data_patrol_size", 0),
		(assign, ":data_raw_material_cost", 0),
		(assign, ":data_price_of_slaves", 0),
		(assign, ":data_chance_of_slavers", diplomacy_default_slaver_availability),
		(assign, ":data_party_morale", 0),
		(assign, ":data_improvement_time", 0),
		(assign, ":data_village_troop_tier", 0),
		(assign, ":data_castle_troop_tier", 0),
		(assign, ":data_labor_discount", 0),
		(assign, ":data_troop_wages", 0),
		(assign, ":data_improvement_cost", 0),
		(assign, ":data_march_unrest", 2),
		(assign, ":data_march_tolerance", 0),
		(assign, ":data_prosperity_ideal", 0),
		(assign, ":data_center_tariffs", 0),
		(assign, ":data_prosperity_real", 0),
		(assign, ":data_prosperity_recovery", 0),
		(assign, ":data_fief_relation", 0),
		(assign, ":data_lrep_martial", 0),
		(assign, ":data_lrep_quarrelsome", 0),
		(assign, ":data_lrep_selfrighteous", 0),
		(assign, ":data_lrep_debauched", 0),
		(assign, ":data_lrep_goodnatured", 0),
		(assign, ":data_lrep_upstanding", 0),
		(assign, ":data_lrep_roguish", 0),
		(assign, ":data_lrep_benefactor", 0),
		(assign, ":data_lrep_custodian", 0),
		(assign, ":data_bandit_infest", 0),
		(assign, ":data_right_to_rule", 0),
		(assign, ":data_bw_penalty", 0),
		(assign, ":data_bw_recover_max", 0),
		(assign, ":data_bw_recover_rate", 0),
		(assign, ":data_fief_recruit_factor", 0),
		
		### POLICY: DESERTION ###
		(try_begin),
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			(eq, ":tooltip_scope", TOOLTIP_POLICY_TROOP_DESERTION),
			(try_begin),
				(eq, ":policy_desertion", POLICY_STAGE_LEFT_2), # Accepted
				(val_add, ":data_village_recruits",      6),
				(assign, ":data_desertion_factor",       2),
				(assign, ":data_desertion_threshold",   44),
				(val_add, ":data_bandit_infest",        -2),
				(val_add, ":data_fief_relation",        15),
				(val_add, ":data_lrep_martial",        -10),
				(val_add, ":data_lrep_quarrelsome",     -5),
				(val_add, ":data_lrep_selfrighteous",   -5),
				(val_add, ":data_lrep_goodnatured",     10),
				(val_add, ":data_lrep_upstanding",      10),
				(val_add, ":data_lrep_roguish",          5),
				(val_add, ":data_lrep_benefactor",      10),
				(val_add, ":data_lrep_custodian",        5),
			(else_try),
				(eq, ":policy_desertion", POLICY_STAGE_LEFT_1), 
				(val_add, ":data_village_recruits",      3),
				(assign, ":data_desertion_factor",       3),
				(assign, ":data_desertion_threshold",   38),
				(val_add, ":data_bandit_infest",        -1),
				(val_add, ":data_fief_relation",         5),
				(val_add, ":data_lrep_martial",         -5),
				(val_add, ":data_lrep_goodnatured",      5),
				(val_add, ":data_lrep_upstanding",       5),
				(val_add, ":data_lrep_benefactor",       5),
			(else_try),
				(eq, ":policy_desertion", POLICY_STAGE_NEUTRAL),
				(val_add, ":data_village_recruits",      0),
				(assign, ":data_desertion_factor",       4),
				(assign, ":data_desertion_threshold",   32),
				(val_add, ":data_bandit_infest",         0),
				(val_add, ":data_fief_relation",         0),
			(else_try),
				(eq, ":policy_desertion", POLICY_STAGE_RIGHT_1),
				(val_add, ":data_village_recruits",     -2),
				(assign, ":data_desertion_factor",       5),
				(assign, ":data_desertion_threshold",   26),
				(val_add, ":data_bandit_infest",         1),
				(val_add, ":data_fief_relation",        -2),
				(val_add, ":data_lrep_quarrelsome",      5),
				(val_add, ":data_lrep_selfrighteous",    5),
				(val_add, ":data_lrep_upstanding",      -5),
			(else_try),
				(eq, ":policy_desertion", POLICY_STAGE_RIGHT_2), # Hunted
				(val_add, ":data_village_recruits",     -4),
				(assign, ":data_desertion_factor",       6),
				(assign, ":data_desertion_threshold",   20),
				(val_add, ":data_bandit_infest",         3),
				(val_add, ":data_fief_relation",        -6),
				(val_add, ":data_lrep_martial",          5),
				(val_add, ":data_lrep_quarrelsome",     10),
				(val_add, ":data_lrep_selfrighteous",   10),
				(val_add, ":data_lrep_goodnatured",     -5),
				(val_add, ":data_lrep_upstanding",      -5),
				(val_add, ":data_lrep_roguish",         -5),
				(val_add, ":data_lrep_custodian",       -5),
			(else_try),
				(assign, reg31, ":policy_desertion"),
				(display_message, "@ERROR (KMS): Invalid policy [ desertion ] value ({reg31}) at script 'diplomacy_calculate_policy_data_values'", gpu_red),
			(try_end),
		(try_end),
		
		### POLICY: CULTURAL FOCUS ###
		(try_begin),
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			(eq, ":tooltip_scope", TOOLTIP_POLICY_CULTURAL_FOCUS),
			(try_begin),
				(eq, ":policy_focus", POLICY_STAGE_LEFT_2), # Trade
				(val_add, ":data_troop_wages",         16),
				(val_add, ":data_center_income",       24),
				(val_add, ":data_improvement_cost",   -16),
				(val_add, ":data_march_unrest",         1), # Mark for removal.
				(val_add, ":data_march_tolerance",      0), # Mark for removal.
				(val_add, ":data_army_size",          -12),
				(val_add, ":data_village_troop_tier",   0),
				(val_add, ":data_prosperity_ideal",     6),
				(val_add, ":data_improvement_time",   -20),
				(val_add, ":data_castle_troop_tier",    0),
				(val_add, ":data_raw_material_cost",   -8),
				(val_add, ":data_bw_penalty",          -2),
				(val_add, ":data_bw_recover_max",      -1),
				(val_add, ":data_bw_recover_rate",      4),
				(val_add, ":data_lrep_martial",       -10),
				(val_add, ":data_lrep_quarrelsome",    -5),
				(val_add, ":data_lrep_selfrighteous",   5),
				(val_add, ":data_lrep_debauched",      10),
				(val_add, ":data_lrep_goodnatured",     5),
				(val_add, ":data_lrep_upstanding",      5),
				(val_add, ":data_lrep_benefactor",     -5),
				(val_add, ":data_lrep_custodian",      15),
			(else_try),
				(eq, ":policy_focus", POLICY_STAGE_LEFT_1), 
				(val_add, ":data_troop_wages",          8),
				(val_add, ":data_center_income",       12),
				(val_add, ":data_improvement_cost",    -8),
				(val_add, ":data_march_unrest",         1),
				(val_add, ":data_march_tolerance",      0),
				(val_add, ":data_army_size",           -6),
				(val_add, ":data_village_troop_tier",   0),
				(val_add, ":data_prosperity_ideal",     3),
				(val_add, ":data_improvement_time",   -10),
				(val_add, ":data_castle_troop_tier",    0),
				(val_add, ":data_raw_material_cost",   -4),
				(val_add, ":data_bw_penalty",          -1),
				(val_add, ":data_bw_recover_max",      -1),
				(val_add, ":data_bw_recover_rate",      2),
				(val_add, ":data_lrep_martial",        -5),
				(val_add, ":data_lrep_debauched",       5),
				(val_add, ":data_lrep_custodian",       5),
			(else_try),
				(eq, ":policy_focus", POLICY_STAGE_NEUTRAL),
				(val_add, ":data_troop_wages",          0),
				(val_add, ":data_center_income",        0),
				(val_add, ":data_improvement_cost",     0),
				(val_add, ":data_march_unrest",         0),
				(val_add, ":data_march_tolerance",      0),
				(val_add, ":data_army_size",            0),
				(val_add, ":data_village_troop_tier",   0),
				(val_add, ":data_prosperity_ideal",     0),
				(val_add, ":data_improvement_time",     0),
				(val_add, ":data_castle_troop_tier",    0),
				(val_add, ":data_raw_material_cost",    0),
				(val_add, ":data_bw_penalty",           0),
				(val_add, ":data_bw_recover_max",       0),
				(val_add, ":data_bw_recover_rate",      0),
			(else_try),
				(eq, ":policy_focus", POLICY_STAGE_RIGHT_1),
				(val_add, ":data_troop_wages",         -8),
				(val_add, ":data_center_income",       -8),
				(val_add, ":data_improvement_cost",     8),
				(val_add, ":data_march_unrest",        -1),
				(val_add, ":data_march_tolerance",      5),
				(val_add, ":data_army_size",            8),
				(val_add, ":data_village_troop_tier",   1),
				(val_add, ":data_prosperity_ideal",    -3),
				(val_add, ":data_improvement_time",     5),
				(val_add, ":data_castle_troop_tier",    0),
				(val_add, ":data_raw_material_cost",    0),
				(val_add, ":data_bw_penalty",           1),
				(val_add, ":data_bw_recover_max",       1),
				(val_add, ":data_bw_recover_rate",     -2),
				(val_add, ":data_lrep_martial",         5),
				(val_add, ":data_lrep_quarrelsome",     5),
				(val_add, ":data_lrep_custodian",      -5),
			(else_try),
				(eq, ":policy_focus", POLICY_STAGE_RIGHT_2), # Military
				(val_add, ":data_troop_wages",        -16),
				(val_add, ":data_center_income",      -16),
				(val_add, ":data_improvement_cost",    16),
				(val_add, ":data_march_unrest",        -1),
				(val_add, ":data_march_tolerance",     10),
				(val_add, ":data_army_size",           16),
				(val_add, ":data_village_troop_tier",   2),
				(val_add, ":data_prosperity_ideal",    -6),
				(val_add, ":data_improvement_time",    10),
				(val_add, ":data_castle_troop_tier",    1),
				(val_add, ":data_raw_material_cost",    0),
				(val_add, ":data_bw_penalty",           2),
				(val_add, ":data_bw_recover_max",       1),
				(val_add, ":data_bw_recover_rate",     -4),
				(val_add, ":data_lrep_martial",        15),
				(val_add, ":data_lrep_quarrelsome",    10),
				(val_add, ":data_lrep_selfrighteous",   5),
				(val_add, ":data_lrep_goodnatured",    -5),
				(val_add, ":data_lrep_upstanding",     -5),
				(val_add, ":data_lrep_benefactor",      5),
				(val_add, ":data_lrep_debauched",      -5),
				(val_add, ":data_lrep_custodian",     -15),
			(else_try),
				(assign, reg31, ":policy_focus"),
				(display_message, "@ERROR (KMS): Invalid policy [ cultural focus ] value ({reg31}) at script 'diplomacy_calculate_policy_data_values'", gpu_red),
			(try_end),
		(try_end),
		
		### POLICY: BORDERS ###
		(try_begin),
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			(eq, ":tooltip_scope", TOOLTIP_POLICY_BORDER_CONTROLS),
			(try_begin),
				(eq, ":policy_borders", POLICY_STAGE_LEFT_2), # Open Borders
				(val_add, ":data_center_tariffs",      16),
				(val_add, ":data_army_size",          -20),
				(val_add, ":data_patrol_size",        -30),
				(val_add, ":data_raw_material_cost",  -15),
				(val_add, ":data_lrep_martial",       -10),
				(val_add, ":data_lrep_quarrelsome",    -5),
				(val_add, ":data_lrep_debauched",       5),
				(val_add, ":data_lrep_benefactor",      5),
				(val_add, ":data_lrep_custodian",      10),
			(else_try),
				(eq, ":policy_borders", POLICY_STAGE_LEFT_1), 
				(val_add, ":data_center_tariffs",       8),
				(val_add, ":data_army_size",          -10),
				(val_add, ":data_patrol_size",        -15),
				(val_add, ":data_raw_material_cost",   -8),
				(val_add, ":data_lrep_martial",        -5),
				(val_add, ":data_lrep_custodian",       5),
			(else_try),
				(eq, ":policy_borders", POLICY_STAGE_NEUTRAL),
				(val_add, ":data_center_tariffs",       0),
				(val_add, ":data_army_size",            0),
				(val_add, ":data_patrol_size",          0),
				(val_add, ":data_raw_material_cost",    0),
			(else_try),
				(eq, ":policy_borders", POLICY_STAGE_RIGHT_1),
				(val_add, ":data_center_tariffs",      -8),
				(val_add, ":data_army_size",           10),
				(val_add, ":data_patrol_size",         25),
				(val_add, ":data_raw_material_cost",    4),
				(val_add, ":data_lrep_martial",         5),
				(val_add, ":data_lrep_custodian",      -5),
			(else_try),
				(eq, ":policy_borders", POLICY_STAGE_RIGHT_2), # Sealed Borders
				(val_add, ":data_center_tariffs",     -16),
				(val_add, ":data_army_size",           20),
				(val_add, ":data_patrol_size",         50),
				(val_add, ":data_raw_material_cost",    8),
				(val_add, ":data_lrep_martial",        10),
				(val_add, ":data_lrep_quarrelsome",    -5),
				(val_add, ":data_lrep_debauched",      -5),
				(val_add, ":data_lrep_benefactor",     -5),
				(val_add, ":data_lrep_custodian",     -10),
			(else_try),
				(assign, reg31, ":policy_borders"),
				(display_message, "@ERROR (KMS): Invalid policy [ border control ] value ({reg31}) at script 'diplomacy_calculate_policy_data_values'", gpu_red),
			(try_end),
		(try_end),
		
		### POLICY: SLAVERY ###
		(try_begin),
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			(eq, ":tooltip_scope", TOOLTIP_POLICY_SLAVERY),
			(try_begin),
				(eq, ":policy_slavery", POLICY_STAGE_LEFT_2), # Banned
				(val_add, ":data_price_of_slaves",     60),
				(val_add, ":data_chance_of_slavers",  -15),
				(val_add, ":data_center_income",      -12),
				(val_add, ":data_party_morale",        -8),
				(val_add, ":data_improvement_time",     0),
				(val_add, ":data_village_troop_tier",   2),
				(val_add, ":data_castle_troop_tier",    1),
				(val_add, ":data_labor_discount",       0),
				(val_add, ":data_fief_recruit_factor",  0),
				(val_add, ":data_lrep_martial",        -5),
				(val_add, ":data_lrep_quarrelsome",    -5),
				(val_add, ":data_lrep_debauched",     -15),
				(val_add, ":data_lrep_goodnatured",    15),
				(val_add, ":data_lrep_upstanding",     15),
				(val_add, ":data_lrep_roguish",       -10),
				(val_add, ":data_lrep_benefactor",      5),
				(val_add, ":data_lrep_custodian",     -10),
			(else_try),
				(eq, ":policy_slavery", POLICY_STAGE_LEFT_1), 
				(val_add, ":data_price_of_slaves",     30),
				(val_add, ":data_chance_of_slavers",  -10),
				(val_add, ":data_center_income",       -6),
				(val_add, ":data_party_morale",        -4),
				(val_add, ":data_improvement_time",     0),
				(val_add, ":data_village_troop_tier",   1),
				(val_add, ":data_castle_troop_tier",    0),
				(val_add, ":data_labor_discount",       0),
				(val_add, ":data_fief_recruit_factor",  0),
				(val_add, ":data_lrep_debauched",      -5),
				(val_add, ":data_lrep_goodnatured",     5),
				(val_add, ":data_lrep_upstanding",      5),
				(val_add, ":data_lrep_roguish",        -5),
				(val_add, ":data_lrep_custodian",      -5),
			(else_try),
				(eq, ":policy_slavery", POLICY_STAGE_NEUTRAL),
				(val_add, ":data_price_of_slaves",      0),
				(val_add, ":data_chance_of_slavers",    0),
				(val_add, ":data_center_income",        0),
				(val_add, ":data_party_morale",         0),
				(val_add, ":data_improvement_time",     0),
				(val_add, ":data_village_troop_tier",   0),
				(val_add, ":data_castle_troop_tier",    0),
				(val_add, ":data_labor_discount",       0),
				(val_add, ":data_fief_recruit_factor",  0),
			(else_try),
				(eq, ":policy_slavery", POLICY_STAGE_RIGHT_1),
				(val_add, ":data_price_of_slaves",    -15),
				(val_add, ":data_chance_of_slavers",   25),
				(val_add, ":data_center_income",        8),
				(val_add, ":data_party_morale",         7),
				(val_add, ":data_improvement_time",   -10),
				(val_add, ":data_village_troop_tier",   0),
				(val_add, ":data_castle_troop_tier",    0),
				(val_add, ":data_labor_discount",     -20),
				(val_add, ":data_fief_recruit_factor",  1),
				(val_add, ":data_lrep_martial",         5),
				(val_add, ":data_lrep_debauched",      10),
				(val_add, ":data_lrep_goodnatured",    -5),
				(val_add, ":data_lrep_upstanding",     -5),
				(val_add, ":data_lrep_roguish",         5),
				(val_add, ":data_lrep_custodian",       5),
			(else_try),
				(eq, ":policy_slavery", POLICY_STAGE_RIGHT_2), # Accepted
				(val_add, ":data_price_of_slaves",    -30),
				(val_add, ":data_chance_of_slavers",   80),
				(val_add, ":data_center_income",       16),
				(val_add, ":data_party_morale",        15),
				(val_add, ":data_improvement_time",   -20),
				(val_add, ":data_village_troop_tier",   0),
				(val_add, ":data_castle_troop_tier",   -1),
				(val_add, ":data_labor_discount",     -50),
				(val_add, ":data_fief_recruit_factor",  2),
				(val_add, ":data_lrep_martial",        10),
				(val_add, ":data_lrep_quarrelsome",    -5),
				(val_add, ":data_lrep_selfrighteous",   5),
				(val_add, ":data_lrep_debauched",      15),
				(val_add, ":data_lrep_goodnatured",   -10),
				(val_add, ":data_lrep_upstanding",    -10),
				(val_add, ":data_lrep_roguish",        10),
				(val_add, ":data_lrep_benefactor",     -5),
				(val_add, ":data_lrep_custodian",      10),
			(else_try),
				(assign, reg31, ":policy_slavery"),
				(display_message, "@ERROR (KMS): Invalid policy [ slavery ] value ({reg31}) at script 'diplomacy_calculate_policy_data_values'", gpu_red),
			(try_end),
		(try_end),
		
		### POLICY: MILITARY DIVERSITY ###
		(try_begin),
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			(eq, ":tooltip_scope", TOOLTIP_POLICY_MILITARY_DIVERSITY),
			(try_begin),
				(eq, ":policy_diversity", POLICY_STAGE_LEFT_2), # Diverse
				(val_add, ":data_village_recruits",    -3),
				(assign, ":data_unity_top_faction",     1),
				(assign, ":data_unity_bot_faction",     2),
				(assign, ":data_unity_top_nonfaction",  1),
				(assign, ":data_unity_bot_nonfaction",  2),
				(assign, ":data_unity_top_mercs",       1),
				(assign, ":data_unity_bot_mercs",       2),
				(val_add, ":data_lrep_martial",        10),
				(val_add, ":data_lrep_quarrelsome",    -5),
				(val_add, ":data_lrep_selfrighteous",  -5),
			(else_try),
				(eq, ":policy_diversity", POLICY_STAGE_LEFT_1), 
				(val_add, ":data_village_recruits",    -1),
				(assign, ":data_unity_top_faction",     1),
				(assign, ":data_unity_bot_faction",     2),
				(assign, ":data_unity_top_nonfaction",  1),
				(assign, ":data_unity_bot_nonfaction",  2),
				(assign, ":data_unity_top_mercs",       1),
				(assign, ":data_unity_bot_mercs",       1),
				(val_add, ":data_lrep_martial",         5),
				(val_add, ":data_lrep_quarrelsome",    -5),
			(else_try),
				(eq, ":policy_diversity", POLICY_STAGE_NEUTRAL),
				(val_add, ":data_village_recruits",     0),
				(assign, ":data_unity_top_faction",     1),
				(assign, ":data_unity_bot_faction",     3),
				(assign, ":data_unity_top_nonfaction",  1),
				(assign, ":data_unity_bot_nonfaction",  1),
				(assign, ":data_unity_top_mercs",       2),
				(assign, ":data_unity_bot_mercs",       1),
			(else_try),
				(eq, ":policy_diversity", POLICY_STAGE_RIGHT_1),
				(val_add, ":data_village_recruits",     1),
				(assign, ":data_unity_top_faction",     1),
				(assign, ":data_unity_bot_faction",     5),
				(assign, ":data_unity_top_nonfaction",  2),
				(assign, ":data_unity_bot_nonfaction",  1),
				(assign, ":data_unity_top_mercs",       3),
				(assign, ":data_unity_bot_mercs",       1),
				(val_add, ":data_lrep_martial",         5),
			(else_try),
				(eq, ":policy_diversity", POLICY_STAGE_RIGHT_2), # Rigid
				(val_add, ":data_village_recruits",     3),
				(assign, ":data_unity_top_faction",     1),
				(assign, ":data_unity_bot_faction",     8),
				(assign, ":data_unity_top_nonfaction",  3),
				(assign, ":data_unity_bot_nonfaction",  1),
				(assign, ":data_unity_top_mercs",       4),
				(assign, ":data_unity_bot_mercs",       1),
				(val_add, ":data_lrep_martial",         5),
				(val_add, ":data_lrep_quarrelsome",    -5),
				(val_add, ":data_lrep_selfrighteous",   5),
			(else_try),
				(assign, reg31, ":policy_diversity"),
				(display_message, "@ERROR (KMS): Invalid policy [ military diversity ] value ({reg31}) at script 'diplomacy_calculate_policy_data_values'", gpu_red),
			(try_end),
		(try_end),
		
		## DECREE: CODE OF LAW (COMMON) ##
		(try_begin),
			# Are we looking at the main summary tooltip?
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_CODE_OF_LAW_COMMON),
			(eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			# Are we looking at this effect as a tooltip.
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_CODE_OF_LAW_COMMON),
			(eq, ":decree_common_laws", 1), # Active
			# Game Effects
			(val_add, ":data_prosperity_ideal",       4),
			(val_add, ":data_center_income",         -8),
			(val_add, ":data_lrep_upstanding",        5),
			(val_add, ":data_lrep_benefactor",        5),
			(val_add, ":data_right_to_rule",          5),
		(try_end),
		
		## DECREE: CODE OF LAW (NOBILITY) ##
		(try_begin),
			# Are we looking at the main summary tooltip?
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_CODE_OF_LAW_NOBLE),
			(eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			# Are we looking at this effect as a tooltip.
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_CODE_OF_LAW_NOBLE),
			(eq, ":decree_noble_laws", 1), # Active
			# Game Effects
			(val_add, ":data_prosperity_ideal",       4),
			(val_add, ":data_fief_relation",         15),
			(val_add, ":data_lrep_debauched",       -15),
			(val_add, ":data_lrep_goodnatured",      10),
			(val_add, ":data_lrep_upstanding",       15),
			(val_add, ":data_lrep_benefactor",       10),
			(val_add, ":data_lrep_roguish",         -10),
			(val_add, ":data_lrep_quarrelsome",     -10),
			(val_add, ":data_lrep_selfrighteous",   -10),
			(val_add, ":data_right_to_rule",          5),
		(try_end),
		
		## DECREE: WAR TAXATION ##
		(try_begin),
			# Are we looking at the main summary tooltip?
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_WAR_TAXATION),
			(eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			# Are we looking at this effect as a tooltip.
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_WAR_TAXATION),
			(eq, ":decree_war_taxes", 1), # Active
			# Game Effects
			(val_add, ":data_prosperity_real",       -4),
			(val_add, ":data_center_income",         75),
			(val_add, ":data_lrep_custodian",       -15),
			(val_add, ":data_lrep_benefactor",      -15),
			(val_add, ":data_lrep_martial",          15),
			(val_add, ":data_fief_relation",       -100),
		(try_end),
		
		## DECREE: SANITATION STANDARDS ##
		(try_begin),
			# Are we looking at the main summary tooltip?
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_SANITATION),
			(eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			# Are we looking at this effect as a tooltip.
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_SANITATION),
			(eq, ":decree_sanitation", 1), # Active
			# Game Effects
			(val_add, ":data_prosperity_ideal",       2),
			(val_add, ":data_fief_relation",          5),
			(val_add, ":data_center_income",         -5),
			(val_add, ":data_lrep_benefactor",        5),
		(try_end),
		
		## DECREE: PERIOD OF RECONSTRUCTION ##
		(try_begin),
			# Are we looking at the main summary tooltip?
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_RECONSTRUCTION),
			(eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			# Are we looking at this effect as a tooltip.
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_RECONSTRUCTION),
			(eq, ":decree_reconstruction", 1), # Active
			# Game Effects
			(val_add, ":data_center_income",       -100),
			(val_add, ":data_prosperity_recovery",  200),
			(val_add, ":data_fief_relation",        100),
			(val_add, ":data_lrep_benefactor",       10),
			(val_add, ":data_lrep_martial",         -15),
		(try_end),
		
		## DECREE: PUBLIC EXECUTIONS ##
		(try_begin),
			# Are we looking at the main summary tooltip?
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_PUBLIC_EXECUTIONS),
			(eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			# Are we looking at this effect as a tooltip.
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_PUBLIC_EXECUTIONS),
			(eq, ":decree_executions", 1), # Active
			# Game Effects
			(val_add, ":data_bandit_infest",         -2),
			(val_add, ":data_fief_relation",        -15),
			(val_add, ":data_lrep_quarrelsome",       5),
			(val_add, ":data_lrep_benefactor",      -10),
			(val_add, ":data_lrep_martial",           5),
		(try_end),
		
		## DECREE: CONSCRIPTION ##
		(try_begin),
			# Are we looking at the main summary tooltip?
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_CONSCRIPTION),
			(eq, ":tooltip_scope", TOOLTIP_DIPLOMACY_SUMMARY),
			# Are we looking at this effect as a tooltip.
			(this_or_next|eq, ":tooltip_scope", TOOLTIP_DECREE_CONSCRIPTION),
			(eq, ":decree_conscription", 1), # Active
			# Game Effects
			(val_mul, ":data_village_recruits",       4), # Special effect.
			(val_add, ":data_lrep_martial",          10),
		(try_end),
		
		# Store output
		(troop_set_slot, KMS_OBJECTS, kms_val_data_village_recruits,            ":data_village_recruits"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_desertion_factor,            ":data_desertion_factor"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_desertion_threshold,         ":data_desertion_threshold"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_unity_top_faction,           ":data_unity_top_faction"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_unity_bot_faction,           ":data_unity_bot_faction"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_unity_top_nonfaction,        ":data_unity_top_nonfaction"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_unity_bot_nonfaction,        ":data_unity_bot_nonfaction"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_unity_top_mercs,             ":data_unity_top_mercs"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_unity_bot_mercs,             ":data_unity_bot_mercs"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_center_income,               ":data_center_income"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_army_size_adjust,            ":data_army_size"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_patrol_size,                 ":data_patrol_size"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_raw_material_discount,       ":data_raw_material_cost"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_price_of_slaves,             ":data_price_of_slaves"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_slaver_availability,         ":data_chance_of_slavers"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_party_morale,                ":data_party_morale"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_improvement_time,            ":data_improvement_time"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_village_recruit_tier,        ":data_village_troop_tier"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_castle_recruit_tier,         ":data_castle_troop_tier"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_labor_discount,              ":data_labor_discount"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_troop_wages,                 ":data_troop_wages"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_improvement_cost,            ":data_improvement_cost"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_march_unrest,                ":data_march_unrest"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_march_tolerance,             ":data_march_tolerance"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_prosperity_ideal,            ":data_prosperity_ideal"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_center_tariffs,              ":data_center_tariffs"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_prosperity_real,             ":data_prosperity_real"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_prosperity_recovery,         ":data_prosperity_recovery"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_fief_relation,               ":data_fief_relation"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_martial_relation,       ":data_lrep_martial"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_quarrelsome_relation,   ":data_lrep_quarrelsome"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_selfrighteous_relation, ":data_lrep_selfrighteous"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_debauched_relation,     ":data_lrep_debauched"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_goodnatured_relation,   ":data_lrep_goodnatured"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_upstanding_relation,    ":data_lrep_upstanding"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_roguish_relation,       ":data_lrep_roguish"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_benefactor_relation,    ":data_lrep_benefactor"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_lrep_custodian_relation,     ":data_lrep_custodian"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_bandit_infest_chance,        ":data_bandit_infest"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_right_to_rule,               ":data_right_to_rule"),
		# v0.16 additions (Battle Weariness)
		(troop_set_slot, KMS_OBJECTS, kms_val_data_weariness_battle_penalty,    ":data_bw_penalty"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_weariness_recovery_max,      ":data_bw_recover_max"),
		(troop_set_slot, KMS_OBJECTS, kms_val_data_weariness_recovery_rate,     ":data_bw_recover_rate"),	
		# v0.24 additions (Slavery Policy)
		(troop_set_slot, KMS_OBJECTS, kms_val_data_center_recruitment_factor,   ":data_fief_recruit_factor"),
		
	]), 
	
# script_diplomacy_create_policy_slider
# Receives the faction, policy & new setting to adjust data slots.
("diplomacy_create_policy_slider",
	[
		(store_script_param, ":pos_x", 1),
		(store_script_param, ":pos_y", 2),
		(store_script_param, ":slot_obj_slider", 3),
		(store_script_param, ":string_policy_label", 4),
		(store_script_param, ":string_policy_desc", 5),
		
		(store_add, ":slot_obj_label", ":slot_obj_slider", 1),
		(store_add, ":slot_obj_left_desc", ":slot_obj_slider", 2),
		(store_add, ":slot_obj_right_desc", ":slot_obj_slider", 3),
		
		### OBJECT: LABEL ###
		(call_script, "script_gpu_create_text_label", ":string_policy_label", ":pos_x", ":pos_y", ":slot_obj_label", gpu_center),
		# (overlay_set_color, reg1, gpu_blue),
		(call_script, "script_gpu_resize_object", ":slot_obj_label", 90),
		(val_sub, ":pos_y", 35),
		(store_add, ":pos_x_slider", ":pos_x", 35), # 10
		
		### OBJECT : SLIDER ###
		(create_slider_overlay, reg1, POLICY_STAGE_LEFT_2, POLICY_STAGE_RIGHT_2),
		(assign, ":obj_slider", reg1),
		(position_set_x, pos1, ":pos_x_slider"),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, ":obj_slider", pos1),
		(troop_set_slot, KMS_OBJECTS, ":slot_obj_slider", ":obj_slider"),
		(call_script, "script_gpu_resize_object", ":slot_obj_slider", 75),
		
		### OBJECT: LEFT BOUNDARY ###
		(val_sub, ":pos_y", 10),
		(store_add, ":pos_x_left", ":pos_x", -75),
		(call_script, "script_gpu_create_text_label", ":string_policy_desc", ":pos_x_left", ":pos_y", ":slot_obj_left_desc", gpu_center),
		(overlay_set_color, reg1, gpu_gray),
		(call_script, "script_gpu_resize_object", ":slot_obj_left_desc", 75),
		
		### OBJECT: RIGHT BOUNDARY ###
		(store_add, ":pos_x_right", ":pos_x", 75),
		(store_sub, ":string_count", POLICY_STAGE_RIGHT_2, POLICY_STAGE_LEFT_2),
		(store_add, ":string_end", ":string_policy_desc", ":string_count"),
		(call_script, "script_gpu_create_text_label", ":string_end", ":pos_x_right", ":pos_y", ":slot_obj_right_desc", gpu_center),
		(overlay_set_color, reg1, gpu_gray),
		(call_script, "script_gpu_resize_object", ":slot_obj_right_desc", 75),
		
	]), 
	
# script_diplomacy_sync_faction_data
# Stores all faction diplomacy data into KMS_OBJECT value slots or takes them from it.
("diplomacy_sync_faction_data",
	[
		(store_script_param, ":faction_no", 1),
		(store_script_param, ":function", 2),
		
		(troop_set_slot, KMS_OBJECTS, kms_val_faction_no, ":faction_no"),
		
		(store_sub, ":limit", diplomacy_policy_data_end, diplomacy_policies_begin),
		(try_for_range, ":offset", 0, ":limit"),
			(store_add, ":faction_slot", diplomacy_policies_begin, ":offset"),
			(store_add, ":storage_slot", kms_val_policies_begin, ":offset"),
			(try_begin),
				(eq, ":function", STORE_TO_PRESENTATION), # 0
				(faction_get_slot, reg1, ":faction_no", ":faction_slot"),
				(troop_get_slot, ":old_value", KMS_OBJECTS, ":storage_slot"),
				(troop_set_slot, KMS_OBJECTS, ":storage_slot", reg1),
			(else_try),
				(eq, ":function", STORE_TO_FACTION), # 1
				(troop_get_slot, reg1, KMS_OBJECTS, ":storage_slot"),
				(faction_get_slot, ":old_value", ":faction_no", ":faction_slot"),
				(faction_set_slot, ":faction_no", ":faction_slot", reg1),
			(else_try),
				### ERROR ###
				(assign, reg31, ":function"),
				(display_message, "@ERROR (KMS): Invalid function #{reg31} at script 'diplomacy_sync_faction_data'.", gpu_red),
			(try_end),
			### DIAGNOSTIC ###
			(ge, DEBUG_DIPLOMACY, 2), # Kingdom management presentation data transfer.  Relevant slots only (verbose)
			(this_or_next|is_between, ":faction_slot", diplomacy_policies_begin, diplomacy_policies_end),
			(this_or_next|is_between, ":faction_slot", diplomacy_decrees_begin, diplomacy_decrees_end),
			(this_or_next|is_between, ":faction_slot", diplomacy_policy_data_begin, diplomacy_policy_data_end),
			(ge, DEBUG_DIPLOMACY, 3), # Kingdom management presentation data transfer.  Every slot (very verbose)
			(assign, reg31, ":faction_slot"),
			(assign, reg32, ":storage_slot"),
			(assign, reg33, reg1),
			(assign, reg34, ":function"),
			(assign, reg35, ":old_value"),
			(str_store_faction_name, s31, ":faction_no"),
			(str_store_string, s32, "@Slot #{reg34?{reg32} of KMS_OBJECTS:{reg31} of {s31}}"), # Source
			(str_store_string, s33, "@slot #{reg34?{reg31} of {s31}:{reg32} of KMS_OBJECTS}"), # Target
			(display_message, "@DEBUG (KMS): {s32} [{reg33}] -> {s33} [{reg35}].", gpu_debug),
		(try_end),
	]),
	
# script_diplomacy_write_benefit_line_to_s1
# Fill {s1} with a single line of text describing the effect of a given benefit.
("diplomacy_write_benefit_line_to_s1",
	[
		(store_script_param, ":benefit", 1),
		
		(str_clear, s1),
		(try_begin),
			### VILLAGE RECRUITS ###
			(eq, ":benefit", kms_val_data_village_recruits),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_village_recruits"),
			
		(else_try),
			### DESERTION FACTOR ###
			(eq, ":benefit", kms_val_data_desertion_factor),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(eq, ":data", 2),
				(str_store_string, s2, "@significantly more"),
			(else_try),
				(eq, ":data", 3),
				(str_store_string, s2, "@more"),
			(else_try),
				(eq, ":data", 5),
				(str_store_string, s2, "@less"),
			(else_try),
				(eq, ":data", 6),
				(str_store_string, s2, "@significantly less"),
			(else_try),
				(str_store_string, s2, "@no more or less"),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_desertion_factor"),
			(try_begin),
				(eq, ":data", 4),
				(str_store_string, s1, "@Soldiers are no more or less likely to desert."),
			(try_end),
			
		(else_try),
			### DESERTION THRESHOLD ###
			(eq, ":benefit", kms_val_data_desertion_threshold),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(assign, reg1, ":data"),
			(str_store_string, s1, "str_kms_data_type_desertion_threshold"),
			
		(else_try),
			### TROOP UNITY: FACTION ###
			(eq, ":benefit", kms_val_data_unity_top_faction),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(troop_get_slot, ":bottom", KMS_OBJECTS, kms_val_data_unity_bot_faction),
			(assign, reg1, ":data"),
			(assign, reg2, ":bottom"),
			(store_sub, reg3, reg2, 1),
			(str_store_string, s1, "str_kms_data_type_unity_faction"),
			
		(else_try),
			### TROOP UNITY: NON-FACTION ###
			(eq, ":benefit", kms_val_data_unity_top_nonfaction),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(troop_get_slot, ":bottom", KMS_OBJECTS, kms_val_data_unity_bot_nonfaction),
			(assign, reg1, ":data"),
			(assign, reg2, ":bottom"),
			(store_sub, reg3, reg2, 1),
			(str_store_string, s1, "str_kms_data_type_unity_nonfaction"),
			
		(else_try),
			### TROOP UNITY: MERCENARIES ###
			(eq, ":benefit", kms_val_data_unity_top_mercs),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(troop_get_slot, ":bottom", KMS_OBJECTS, kms_val_data_unity_bot_mercs),
			(assign, reg1, ":data"),
			(assign, reg2, ":bottom"),
			(store_sub, reg3, reg2, 1),
			(str_store_string, s1, "str_kms_data_type_unity_mercs"),
			
		(else_try),
			### CENTER INCOME ###
			(eq, ":benefit", kms_val_data_center_income),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_center_income"),
			
		(else_try),
			### CENTER TARIFFS ###
			(eq, ":benefit", kms_val_data_center_tariffs),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_center_tariffs"),
			
		(else_try),
			### ARMY SIZE ###
			(eq, ":benefit", kms_val_data_army_size_adjust),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_army_size"),
			
		(else_try),
			### PATROL SIZE ###
			(eq, ":benefit", kms_val_data_patrol_size),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_patrol_size"),
			
		(else_try),
			### RAW MATERIAL DISCOUNT ###
			(eq, ":benefit", kms_val_data_raw_material_discount),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_raw_material_discount"),
			
		(else_try),
			### LABOR DISCOUNT ###
			(eq, ":benefit", kms_val_data_labor_discount),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_labor_discount"),
			
		(else_try),
			### TROOP WAGES ###
			(eq, ":benefit", kms_val_data_troop_wages),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_troop_wages"),
			
		(else_try),
			### IDEAL PROSPERITY ###
			(eq, ":benefit", kms_val_data_prosperity_ideal),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_prosperity_ideal"),
			
		(else_try),
			### PRICE OF SLAVES ###
			(eq, ":benefit", kms_val_data_price_of_slaves),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_price_of_slaves"),
			
		(else_try),
			### AVAILABILITY OF SLAVERS ###
			(eq, ":benefit", kms_val_data_slaver_availability),
			(troop_get_slot, reg1, KMS_OBJECTS, ":benefit"),
			(str_store_string, s1, "str_kms_data_type_slaver_availability"),
			
		(else_try),
			### PARTY MORALE ###
			(eq, ":benefit", kms_val_data_party_morale),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_party_morale"),
			
		(else_try),
			### IMPROVEMENT COST ###
			(eq, ":benefit", kms_val_data_improvement_cost),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_improvement_cost"),
			
		(else_try),
			### IMPROVEMENT TIME ###
			(eq, ":benefit", kms_val_data_improvement_time),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_improvement_time"),
			
		(else_try),
			### VILLAGE RECRUITMENT TIER ###
			(eq, ":benefit", kms_val_data_village_recruit_tier),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(store_sub, reg3, reg1, 1),
			(str_store_string, s1, "str_kms_data_type_village_recruit_tier"),
			
		(else_try),
			### CASTLE RECRUITMENT TIER ###
			(eq, ":benefit", kms_val_data_castle_recruit_tier),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(store_sub, reg3, reg1, 1),
			(str_store_string, s1, "str_kms_data_type_castle_recruit_tier"),
			
		(else_try),
			### BATTLE WEARINESS - PENALTY PER BATTLE ###
			(eq, ":benefit", kms_val_data_weariness_battle_penalty),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_weariness_penalty"),
			
		(else_try),
			### BATTLE WEARINESS - RECOVERY RATE ###
			(eq, ":benefit", kms_val_data_weariness_recovery_rate),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(eq, ":data", -4),
				(assign, reg1, 33),
				(assign, reg2, 0),
			(else_try),
				(eq, ":data", -2),
				(assign, reg1, 14),
				(assign, reg2, 0),
			(else_try),
				(eq, ":data", 0),
				(assign, reg1, 0),
				(assign, reg2, 0),
			(else_try),
				(eq, ":data", 2),
				(assign, reg1, 12),
				(assign, reg2, 1),
			(else_try),
				(eq, ":data", 4),
				(assign, reg1, 25),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_weariness_recovery_rate"),
			
		(else_try),
			### BATTLE WEARINESS - RECOVERY LIMIT ###
			(eq, ":benefit", kms_val_data_weariness_recovery_max),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_weariness_recovery_limit"),
			
		## WINDYPLAINS+ ## - MARK FOR DELETION.  Obsolete with Battle Weariness addition.
		(else_try),
			### MARCH UNREST ###
			(eq, ":benefit", kms_val_data_march_unrest),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(assign, reg1, ":data"),
			(str_store_string, s1, "str_kms_data_type_march_unrest"),
			
		(else_try),
			### MARCH TOLERANCE ###
			(eq, ":benefit", kms_val_data_march_tolerance),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(assign, reg1, ":data"),
			(store_sub, reg2, reg1, 1),
			(str_store_string, s1, "str_kms_data_type_march_tolerance"),
		## WINDYPLAINS- ##
		
		(else_try),
			### PROSPERITY REAL ###
			(eq, ":benefit", kms_val_data_prosperity_real),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_prosperity_real"),
			
		(else_try),
			### PROSPERITY RECOVERY ###
			(eq, ":benefit", kms_val_data_prosperity_recovery),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_prosperity_recovery"),
			
		(else_try),
			### NOBLE RELATION: MARTIAL ###
			(eq, ":benefit", kms_val_data_lrep_martial_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_martial_relation"),
			
		(else_try),
			### NOBLE RELATION: QUARRELSOME ###
			(eq, ":benefit", kms_val_data_lrep_quarrelsome_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_quarrelsome_relation"),
			
		(else_try),
			### NOBLE RELATION: SELF-RIGHTEOUS ###
			(eq, ":benefit", kms_val_data_lrep_selfrighteous_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_selfrighteous_relation"),
			
		(else_try),
			### NOBLE RELATION: CUNNING ###
			(eq, ":benefit", kms_val_data_lrep_cunning_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_cunning_relation"),
			
		(else_try),
			### NOBLE RELATION: DEBAUCHED ###
			(eq, ":benefit", kms_val_data_lrep_debauched_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_debauched_relation"),
			
		(else_try),
			### NOBLE RELATION: GOODNATURED ###
			(eq, ":benefit", kms_val_data_lrep_goodnatured_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_goodnatured_relation"),
			
		(else_try),
			### NOBLE RELATION: UPSTANDING ###
			(eq, ":benefit", kms_val_data_lrep_upstanding_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_upstanding_relation"),
			
		(else_try),
			### NOBLE RELATION: ROGUISH ###
			(eq, ":benefit", kms_val_data_lrep_roguish_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_roguish_relation"),
			
		(else_try),
			### NOBLE RELATION: BENEFACTOR ###
			(eq, ":benefit", kms_val_data_lrep_benefactor_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_benefactor_relation"),
			
		(else_try),
			### NOBLE RELATION: CUSTODIAN ###
			(eq, ":benefit", kms_val_data_lrep_custodian_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_lrep_custodian_relation"),
			
		(else_try),
			### FIEF RELATION ###
			(eq, ":benefit", kms_val_data_fief_relation),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_fief_relation"),
			
		(else_try),
			### BANDIT INFESTATION ###
			(eq, ":benefit", kms_val_data_bandit_infest_chance),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_bandit_infestation"),
			
		(else_try),
			### RIGHT TO RULE ###
			(eq, ":benefit", kms_val_data_right_to_rule),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(str_store_string, s1, "str_kms_data_type_right_to_rule"),
			
		(else_try),
			### CENTER RECRUITMENT FACTOR ###
			(eq, ":benefit", kms_val_data_center_recruitment_factor),
			(troop_get_slot, ":data", KMS_OBJECTS, ":benefit"),
			(try_begin),
				(ge, ":data", 0),
				(assign, reg1, ":data"),
				(assign, reg2, 0),
			(else_try),
				(store_mul, ":double_positive", ":data", -2),
				(store_add, reg1, ":data", ":double_positive"),
				(assign, reg2, 1),
			(try_end),
			(val_mul, reg1, 15),
			(str_store_string, s1, "@Peasants available in fiefs are {reg2?reduced:increased} by {reg1}%."),
			# (str_store_string, s1, "@The number of peasant recruits available in fiefs is {reg2?reduced:increased} by {reg1}%."),
			
		### DATA TYPES SHOULD BE LISTED BEFORE THIS POINT ###
		(else_try),
			### ERROR ###
			(assign, reg31, ":benefit"),
			(display_message, "@ERROR (KMS): Invalid data slot #{reg31} requested at script 'diplomacy_write_benefit_line_to_s1'.", gpu_red),
			(str_store_string, s1, "@ERROR: Invalid data slot #{reg31} requested."),
		(try_end),
	]),

# script_diplomacy_create_tooltip
# Gathers information necessary to update the main & secondary description blocks in presentation "diplomacy_kingdom_management"
("diplomacy_create_tooltip",
	[
		(store_script_param, ":tooltip_type", 1),
		
		(call_script, "script_diplomacy_calculate_policy_data_values", ":tooltip_type"),
		
		### TITLE BLOCK ###
		(str_clear, s40),
		
		# Determine start & end description string points & main title value.
		(try_begin),
			(eq, ":tooltip_type", TOOLTIP_DIPLOMACY_SUMMARY),
			(assign, ":string_title", "str_kms_summary_label"),
			(assign, ":string_begin", "str_kms_summary_long_desc_1"),
			(store_add, ":string_end", "str_kms_summary_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_POLICY_CULTURAL_FOCUS),
			(assign, ":string_title", "str_kms_sfp_focus_label"),
			(assign, ":string_begin", "str_kms_sfp_focus_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_focus_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_POLICY_MILITARY_DIVERSITY),
			(assign, ":string_title", "str_kms_sfp_diversity_label"),
			(assign, ":string_begin", "str_kms_sfp_diversity_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_diversity_long_desc_7", 1),
			
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_POLICY_BORDER_CONTROLS),
			(assign, ":string_title", "str_kms_sfp_borders_label"),
			(assign, ":string_begin", "str_kms_sfp_borders_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_borders_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_POLICY_SLAVERY),
			(assign, ":string_title", "str_kms_sfp_slavery_label"),
			(assign, ":string_begin", "str_kms_sfp_slavery_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_slavery_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_POLICY_TROOP_DESERTION),
			(assign, ":string_title", "str_kms_sfp_desertion_label"),
			(assign, ":string_begin", "str_kms_sfp_desertion_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_desertion_long_desc_7", 1),
			
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_DECREE_CONSCRIPTION),
			(assign, ":string_title", "str_kms_sfd_conscription_label"),
			(assign, ":string_begin", "str_kms_sfp_conscription_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_conscription_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_DECREE_CODE_OF_LAW_COMMON),
			(assign, ":string_title", "str_kms_sfd_code_of_law_common_label"),
			(assign, ":string_begin", "str_kms_sfp_commonlaw_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_commonlaw_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_DECREE_CODE_OF_LAW_NOBLE),
			(assign, ":string_title", "str_kms_sfd_code_of_law_noble_label"),
			(assign, ":string_begin", "str_kms_sfp_noblelaw_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_noblelaw_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_DECREE_WAR_TAXATION),
			(assign, ":string_title", "str_kms_sfd_war_taxation_label"),
			(assign, ":string_begin", "str_kms_sfp_wartaxes_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_wartaxes_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_DECREE_SANITATION),
			(assign, ":string_title", "str_kms_sfd_sanitation_label"),
			(assign, ":string_begin", "str_kms_sfp_sanitation_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_sanitation_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_DECREE_RECONSTRUCTION),
			(assign, ":string_title", "str_kms_sfd_reconstruction_label"),
			(assign, ":string_begin", "str_kms_sfp_reconstruction_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_reconstruction_long_desc_7", 1),
		(else_try),
			(eq, ":tooltip_type", TOOLTIP_DECREE_PUBLIC_EXECUTIONS),
			(assign, ":string_title", "str_kms_sfd_executions_label"),
			(assign, ":string_begin", "str_kms_sfp_executions_long_desc_1"),
			(store_add, ":string_end", "str_kms_sfp_executions_long_desc_7", 1),
		(try_end),
		
		# Main Title
		(str_store_string, s40, ":string_title"),
		(troop_get_slot, ":tooltip_obj", KMS_OBJECTS, kms_obj_title_tooltip),
		(overlay_set_text, ":tooltip_obj", "@{s40}"),
		
		
		### PRIMARY BLOCK ###
		(str_clear, s40),
		# Description Block
		(try_for_range, ":string_no", ":string_begin", ":string_end"),
			(str_store_string, s41, ":string_no"),
			(str_store_string, s40, "@{s40}^{s41}"),
		(try_end),
		# Update primary overlay object with {s40}.
		(troop_get_slot, ":tooltip_obj", KMS_OBJECTS, kms_obj_primary_tooltip),
		(overlay_set_text, ":tooltip_obj", "@{s40}"),
		
		### SECONDARY BLOCK ###
		# Initialize
		(str_store_string, s40, "@^"),
		
		# Determine data points to display.
		(try_begin),
			### MAIN SUMMARY ###
			(eq, ":tooltip_type", TOOLTIP_DIPLOMACY_SUMMARY),
			# Economy / Enterprises / Improvements
			(str_store_string, s40, "@{s40}^^Economy, Improvements & Enterprises:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_income),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_tariffs),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_ideal),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_real),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_recovery),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_improvement_cost),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_improvement_time),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_labor_discount),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_raw_material_discount),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_price_of_slaves),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_slaver_availability),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			
			# Security / Troops
			(str_store_string, s40, "@{s40}^^Security & Troops:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_troop_wages),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_army_size_adjust),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_patrol_size),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_village_recruits),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_recruitment_factor),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_village_recruit_tier),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_castle_recruit_tier),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_bandit_infest_chance),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			
			# Relations
			(str_store_string, s40, "@{s40}^^Politics:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_fief_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_martial_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_quarrelsome_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_selfrighteous_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_cunning_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_debauched_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_goodnatured_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_upstanding_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_roguish_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_benefactor_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_custodian_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_right_to_rule),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			
			# Morale Changers
			(str_store_string, s40, "@{s40}^^Kingdom & Party Morale:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_party_morale),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_desertion_factor),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_desertion_threshold),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_unity_top_faction),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_unity_top_nonfaction),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_unity_top_mercs),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_weariness_battle_penalty),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_weariness_recovery_max),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_weariness_recovery_rate),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			
		(else_try),
			### POLICY: CULTURAL FOCUS ###
			(eq, ":tooltip_type", TOOLTIP_POLICY_CULTURAL_FOCUS),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_income),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_ideal),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_improvement_cost),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_improvement_time),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_raw_material_discount),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_troop_wages),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_army_size_adjust),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_village_recruit_tier),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_castle_recruit_tier),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			# (call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_march_unrest),
			# (str_store_string, s40, "str_diplomacy_data_benefit_line"),
			# (call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_march_tolerance),
			# (str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_weariness_battle_penalty),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_weariness_recovery_max),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_weariness_recovery_rate),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(assign, ":blanks", 25),
			
		(else_try),
			### POLICY: MILITARY DIVERSITY ###
			(eq, ":tooltip_type", TOOLTIP_POLICY_MILITARY_DIVERSITY),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_village_recruits),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_unity_top_faction),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_unity_top_nonfaction),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_unity_top_mercs),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(assign, ":blanks", 33),
			
		(else_try),
			### POLICY: BORDER CONTROL ###
			(eq, ":tooltip_type", TOOLTIP_POLICY_BORDER_CONTROLS),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_tariffs),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_raw_material_discount),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_army_size_adjust),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_patrol_size),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(assign, ":blanks", 33),
			
		(else_try),
			### POLICY: SLAVERY ###
			(eq, ":tooltip_type", TOOLTIP_POLICY_SLAVERY),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_price_of_slaves),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_slaver_availability),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_income),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_labor_discount),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_improvement_time),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_recruitment_factor),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_village_recruit_tier),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_castle_recruit_tier),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_party_morale),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(assign, ":blanks", 28),
			
		(else_try),
			### POLICY: TROOP DESERTION ###
			(eq, ":tooltip_type", TOOLTIP_POLICY_TROOP_DESERTION),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_fief_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_village_recruits),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_desertion_factor),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_desertion_threshold),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_bandit_infest_chance),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(assign, ":blanks", 32),
			
		(else_try),
			### DECREE: MANDATORY CONSCRIPTION ###
			(eq, ":tooltip_type", TOOLTIP_DECREE_CONSCRIPTION),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(str_store_string, s40, "@{s40}^* Number of recruits available is quadrupled."),
			(str_store_string, s40, "@{s40}^* Fief relation is reduced by 3 during each recruitment."),
			(str_store_string, s40, "@{s40}^* Fief prosperity is reduced by 3 during each recruitment."),
			(assign, ":blanks", 34),
			
		(else_try),
			### DECREE: CODE OF LAW FOR COMMONERS ###
			(eq, ":tooltip_type", TOOLTIP_DECREE_CODE_OF_LAW_COMMON),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_income),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_ideal),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_right_to_rule),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(assign, ":blanks", 34),
			
		(else_try),
			### DECREE: CODE OF LAW FOR NOBLES ###
			(eq, ":tooltip_type", TOOLTIP_DECREE_CODE_OF_LAW_NOBLE),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_ideal),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_right_to_rule),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(str_store_string, s40, "@{s40}^^Note: This decree requires that 'Code of Law (Commons)' ^be in effect."),
			(assign, ":blanks", 32),
			
		(else_try),
			### DECREE: WAR TAXATION ###
			(eq, ":tooltip_type", TOOLTIP_DECREE_WAR_TAXATION),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_real),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_fief_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_recovery),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(str_store_string, s40, "@{s40}^^Note: This decree may not be in effect at the same^time as 'Period of Reconstruction'."),
			(assign, ":blanks", 31),
			
		(else_try),
			### DECREE: SANITATION STANDARDS ###
			(eq, ":tooltip_type", TOOLTIP_DECREE_SANITATION),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_income),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_ideal),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(assign, ":blanks", 35),
			
		(else_try),
			### DECREE: PERIOD OF RECONSTRUCTION ###
			(eq, ":tooltip_type", TOOLTIP_DECREE_RECONSTRUCTION),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_center_income),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_ideal),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_prosperity_recovery),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_fief_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(str_store_string, s40, "@{s40}^^Note: This decree may not be in effect at the same^time as 'War Taxation'."),
			(assign, ":blanks", 30),
			
		(else_try),
			### DECREE: PUBLIC EXECUTIONS ###
			(eq, ":tooltip_type", TOOLTIP_DECREE_PUBLIC_EXECUTIONS),
			(str_store_string, s40, "@{s40}^^Game Effects:^"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_fief_relation),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_bandit_infest_chance),
			(str_store_string, s40, "str_diplomacy_data_benefit_line"),
			(assign, ":blanks", 35),
			
		(try_end),
		
		(try_begin),
			(neq, ":tooltip_type", TOOLTIP_DIPLOMACY_SUMMARY),
			(str_store_string, s40, "@{s40}^^Noble Reactions:^"),
			(assign, ":nobles_affected", 10),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_martial_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_quarrelsome_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_selfrighteous_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_cunning_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_debauched_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_goodnatured_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_upstanding_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_roguish_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_benefactor_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			(try_begin),
				(call_script, "script_diplomacy_write_benefit_line_to_s1", kms_val_data_lrep_custodian_relation),
				(neq, reg1, 0),
				(str_store_string, s40, "str_diplomacy_data_benefit_line"),
				(val_sub, ":nobles_affected", 1),
			(try_end),
			
			(val_add, ":blanks", ":nobles_affected"),
			(ge, ":blanks", 1),
			# Blank spaces inserted at bottom to make scrolling setup look proper.
			(try_for_range, ":unused", 0, ":blanks"),
				(str_store_string, s40, "@{s40}^"),
			(try_end),
		(try_end),
		
		## TODO: Update secondary overlay object with {s40}.
		(troop_get_slot, ":tooltip_obj", KMS_OBJECTS, kms_obj_secondary_tooltip),
		(overlay_set_text, ":tooltip_obj", "@{s40}"),
	]),
	
# script_diplomacy_convert_percent_to_direct_change
# Receives a % chance and returns back how much something should change by.
# Example: -130% supplied.  Turned into 130.  Minimum change becomes 1 with a 30% chance of becoming a 2.  Final change value returned is -1 to -2.
("diplomacy_convert_percent_to_direct_change",
	[
		(store_script_param_1, ":chance"),
		
		(try_begin),
			(ge, ":chance", 0),
			(assign, ":sign", 1),
		(else_try),
			(assign, ":sign", -1),
		(try_end),
		(val_mul, ":chance", ":sign"), # Remove - sign for now.
		
		(store_div, ":change", ":chance", 100),
		(store_mod, ":random_threshold", ":chance", 100),
		(store_random_in_range, ":roll", 0, 100),
		(try_begin),
			(lt, ":roll", ":random_threshold"),
			(val_add, ":change", 1),
		(try_end),
		
		(store_mul, reg1, ":change", ":sign"), # Put the (-) sign back if applicable.
	]),  
	
###########################################################################################################################
#####                                                 MISC SCRIPTS                                                    #####
###########################################################################################################################
# script_post_combat_relation_changes
# This script gets inserted in the add_log_event script to catch any allied heroes you fight alongside.  This includes companions.
("post_combat_relation_changes",
	[
		(store_script_param_1, ":troop_no"),
		
		(store_faction_of_troop, ":faction_no", ":troop_no"),
		(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
		(assign, ":relation", reg0),
		
		(try_begin),
			# Capture non-party heroes.
			(neg|main_party_has_troop, ":troop_no"),
			(assign, ":relation_boost", 1),
			(try_begin),
				(faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"), # Kings like you helping out.
				(val_add, ":relation_boost", 1),
			(else_try),
				(faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"), # Marshalls appreciate your support.
				(val_add, ":relation_boost", 1),
			(try_end),
			
			# If relation with player is poor then may not get any relation gain.
			(try_begin),
				(lt, ":relation", 0),
				(val_mul, ":relation", -3),
				(store_random_in_range, ":roll", 0, 100),
				(ge, ":roll", ":relation"),
				(val_sub, ":relation_boost", 1),
			(try_end),
			
			(store_add, ":cap", ":relation", ":relation_boost"),
			(lt, ":cap", 50),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_boost", 0),
		(else_try),
			# Party companions only gain relation if they were not wounded in the fight.
			(neg|troop_is_wounded, ":troop_no"),
			(store_add, ":cap", ":relation", ":relation_boost"),
			(lt, ":cap", 50),
			(set_show_messages, 0),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", 1, 0),
			(set_show_messages, 1),
		(try_end),
		
	]),   

# script_cf_diplomacy_treasury_verify_funds
# PURPOSE: Make a universal script for handling if the player has enough funds available for something to make it easier when I add a treasury.
# EXAMPLE: (call_script, "script_cf_diplomacy_treasury_verify_funds", ":funds_required", ":center_no", ":primary_source", ":condition_requested"), # diplomacy_scripts.py
("cf_diplomacy_treasury_verify_funds",
	[
		(store_script_param, ":funds_required", 1),
		(store_script_param, ":center_no", 2),
		(store_script_param, ":primary_source", 3),
		(store_script_param, ":condition_requested", 4),
		
		(store_troop_gold, ":player_gold", "trp_player"),
		(try_begin),
			(is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(party_get_slot, ":treasury_funds", ":center_no", slot_center_treasury),
		(else_try),
			(assign, ":treasury_funds", 0),
		(try_end),
		(store_add, ":total_funds", ":player_gold", ":treasury_funds"),
		
		(assign, ":pass", 0),
		(try_begin),
			(eq, ":condition_requested", TREASURY_FUNDS_AVAILABLE),
			(try_begin),
				(eq, ":primary_source", FUND_FROM_TREASURY),
				(assign, reg1, ":treasury_funds"), # Stored for fail checks.
				(ge, ":treasury_funds", ":funds_required"),
				(str_store_string, s31, "@Treasury"),
				(try_begin),
					(neg|is_between, ":center_no", walled_centers_begin, walled_centers_end),
					(str_store_party_name, s32, ":center_no"),
					(display_message, "@ERROR (diplomacy) - Fund request from a treasury that doesn't exist.  Invalid keep = {s32}.", gpu_debug),
				(try_end),
				(assign, ":pass", 1),
			(else_try),
				(eq, ":primary_source", FUND_FROM_PLAYER),
				(assign, reg1, ":player_gold"), # Stored for fail checks.
				(ge, ":player_gold", ":funds_required"),
				(str_store_string, s31, "@Player funds"),
				(assign, ":pass", 1),
			(else_try),
				(eq, ":primary_source", FUND_FROM_EITHER),
				(assign, reg1, ":total_funds"), # Stored for fail checks.
				(ge, ":total_funds", ":funds_required"),
				(str_store_string, s31, "@Total funds"),
				(assign, ":pass", 1),
			(try_end),
			
		(else_try),
			(eq, ":condition_requested", TREASURY_FUNDS_INSUFFICIENT),
			(try_begin),
				(eq, ":primary_source", FUND_FROM_TREASURY),
				(assign, reg1, ":treasury_funds"), # Stored for fail checks.
				(lt, ":treasury_funds", ":funds_required"),
				(str_store_string, s31, "@Treasury"),
				(try_begin),
					(neg|is_between, ":center_no", walled_centers_begin, walled_centers_end),
					(str_store_party_name, s32, ":center_no"),
					(display_message, "@ERROR (diplomacy) - Fund request from a treasury that doesn't exist.  Invalid keep = {s32}.", gpu_debug),
				(try_end),
				(assign, ":pass", 1),
			(else_try),
				(eq, ":primary_source", FUND_FROM_PLAYER),
				(assign, reg1, ":player_gold"), # Stored for fail checks.
				(lt, ":player_gold", ":funds_required"),
				(str_store_string, s31, "@Player funds"),
				(assign, ":pass", 1),
			(else_try),
				(eq, ":primary_source", FUND_FROM_EITHER),
				(assign, reg1, ":total_funds"), # Stored for fail checks.
				(lt, ":total_funds", ":funds_required"),
				(str_store_string, s31, "@Total funds"),
				(assign, ":pass", 1),
			(try_end),
			
		(else_try),
			(ge, DEBUG_TREASURY, 1),
			(assign, reg31, ":condition_requested"),
			(assign, reg32, ":funds_required"),
			(display_message, "@DEBUG (diplomacy): {s31} {reg31?<:>=} {reg32} denars.  Condition failed.", gpu_debug),
		(try_end),
		(eq, ":pass", 1),
	]),
	
# script_diplomacy_treasury_withdraw_funds
# PURPOSE: Set a universal script for handling removal of player funds.  This is done so that a treasury can be factored in where appropriate.
("diplomacy_treasury_withdraw_funds",
	[
		(store_script_param, ":funds_required", 1),
		(store_script_param, ":center_no", 2),
		(store_script_param, ":primary_source", 3),
		
		(store_troop_gold, ":player_gold", "trp_player"),
		(try_begin),
			(is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(party_get_slot, ":treasury_funds", ":center_no", slot_center_treasury),
		(else_try),
			(assign, ":treasury_funds", 0),
		(try_end),
		(assign, ":play_sound", 0),
		
		(try_begin),
			(this_or_next|eq, ":primary_source", FUND_FROM_TREASURY),
			(eq, ":primary_source", FUND_FROM_TREASURY_TO_PLAYER),
			(val_sub, ":treasury_funds", ":funds_required"),
			(party_set_slot, ":center_no", slot_center_treasury, ":treasury_funds"),
			(try_begin),
				(ge, DEBUG_TREASURY, 1),
				(str_store_party_name, s31, ":center_no"),
				(assign, reg31, ":funds_required"),
				(assign, reg32, ":treasury_funds"),
				(display_message, "@DEBUG (diplomacy): Treasury in {s31} has been reduced by {reg31} denars to {reg32} denars.", gpu_debug),
			(try_end),
			(try_begin),
				(eq, ":primary_source", FUND_FROM_TREASURY_TO_PLAYER),
				(call_script, "script_troop_add_gold", "trp_player", ":funds_required"), # Give the gold back to the player.
			(try_end),
			
		(else_try),
			(eq, ":primary_source", FUND_FROM_PLAYER),
			(troop_remove_gold, "trp_player", ":funds_required"),
			(assign, ":play_sound", 1),
			
		(else_try),
			# First attempt to have the player fund this entirely.
			(eq, ":primary_source", FUND_FROM_EITHER),
			(ge, ":player_gold", ":funds_required"),
			(troop_remove_gold, "trp_player", ":funds_required"),
			(assign, ":play_sound", 1),
			
		(else_try),
			# Second attempt to split the difference 50/50.
			(eq, ":primary_source", FUND_FROM_EITHER),
			(store_div, ":half_cost", ":funds_required", 2),
			(ge, ":player_gold", ":half_cost"),
			(troop_remove_gold, "trp_player", ":half_cost"),
			(assign, ":play_sound", 1),
			(val_sub, ":treasury_funds", ":half_cost"),
			(party_set_slot, ":center_no", slot_center_treasury, ":treasury_funds"),
			(try_begin),
				(ge, DEBUG_TREASURY, 1),
				(str_store_party_name, s31, ":center_no"),
				(assign, reg31, ":half_cost"),
				(assign, reg32, ":treasury_funds"),
				(display_message, "@DEBUG (diplomacy): Treasury in {s31} has been reduced by {reg31} denars to {reg32} denars.", gpu_debug),
			(try_end),
			
		(else_try),
			# Finally take everything from the player you can and then deplete the treasury.
			(eq, ":primary_source", FUND_FROM_EITHER),
			(assign, ":taken_from_player", ":funds_required"),
			(val_min, ":taken_from_player", ":player_gold"),
			(troop_remove_gold, "trp_player", ":taken_from_player"),
			(assign, ":play_sound", 1),
			(val_sub, ":funds_required", ":taken_from_player"),
			(val_sub, ":treasury_funds", ":funds_required"),
			(party_set_slot, ":center_no", slot_center_treasury, ":treasury_funds"),
			(try_begin),
				(ge, DEBUG_TREASURY, 1),
				(str_store_party_name, s31, ":center_no"),
				(assign, reg31, ":funds_required"),
				(assign, reg32, ":treasury_funds"),
				(display_message, "@DEBUG (diplomacy): Treasury in {s31} has been reduced by {reg31} denars to {reg32} denars.", gpu_debug),
			(try_end),
			
		(try_end),
		
		(try_begin),
			(eq, ":play_sound", 1),
			(play_sound, "snd_money_received"),
		(try_end),
	]),
	
# script_diplomacy_treasury_deposit_funds
# PURPOSE: Set a universal script for handling deposit of player gold into a treasury.
("diplomacy_treasury_deposit_funds",
	[
		(store_script_param, ":funds_deposited", 1),
		(store_script_param, ":center_no", 2),
		
		# Get our current treasury values.
		(party_get_slot, ":treasury_funds", ":center_no", slot_center_treasury),
		(try_begin),
			(neg|is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(display_message, "@ERROR (diplomacy) - A deposit attempt was made at an invalid treasury.", gpu_debug),
		(try_end),
		
		# Verify we have enough gold to make the deposit.
		(store_troop_gold, ":player_gold", "trp_player"),
		(val_min, ":funds_deposited", ":player_gold"),
		
		# Make the payment.
		(troop_remove_gold, "trp_player", ":funds_deposited"),
		(val_add, ":treasury_funds", ":funds_deposited"),
		(party_set_slot, ":center_no", slot_center_treasury, ":treasury_funds"),
		
		# Diagnostic
		(try_begin),
			(ge, DEBUG_TREASURY, 1),
			(str_store_party_name, s31, ":center_no"),
			(assign, reg31, ":funds_deposited"),
			(assign, reg32, ":treasury_funds"),
			(display_message, "@DEBUG (diplomacy): Treasury in {s31} has been increased by {reg31} denars to {reg32} denars.", gpu_debug),
		(try_end),
	]),
	
# script_diplomacy_store_player_title_to_s66
# PURPOSE: Develop a universal script for handling the way a player should be referred to.
("diplomacy_store_player_title_to_s66",
	[
		(store_script_param, ":speaker", 1),
		(store_script_param, ":capitalize", 2),
		(assign, reg1, ":speaker"), # Prevent the compiler from complaining.
		
		(str_clear, s66),
		
		(assign, reg22, ":capitalize"),
		
		(call_script, "script_kmt_set_custom_noble_title_for_troop", "trp_player", "$players_kingdom", KMT_TITLE_FUNCTION_STORE),
		(str_store_troop_name, s0, "trp_player"),
		(try_begin),
			(faction_slot_eq, "$players_kingdom", slot_faction_title_style, 1), # Title After Name
			(str_store_string, s66, "@{reg22?:, }{s0} {s4}"),
		(else_try),
			(str_store_string, s66, "@{reg22?:, }{s4} {s0}"), # Title Before Name
		(try_end),
		
		# Capture companions speaking to the player from within the party while the player has no valid title.
		(try_begin),
			(str_is_empty, s4),
			(troop_get_type, reg23, "trp_player"),
			(str_store_string, s66, "@{reg22?:, }{reg22?My:my} {reg23?Lady:Lord}"),
		(try_end),
	]),
	
# script_diplomacy_set_party_intel_level
# PURPOSE: Change the level of intelligence on a location or party.
# EXAMPLE: (call_script, "script_diplomacy_set_party_intel_level", ":center_no", ":change", ":show_report"),
("diplomacy_set_party_intel_level",
	[
		(store_script_param, ":center_no", 1),
		(store_script_param, ":change", 2),
		(store_script_param, ":show_report", 3),
		
		# Get our current treasury values.
		(party_get_slot, ":intel", ":center_no", slot_center_intelligence),
		(assign, ":display_info", 0),
		(try_begin),
			(lt, ":intel", 10),
			(assign, ":display_info", 1),
		(try_end),
		(val_add, ":intel", ":change"),
		
		# Special case to allow for val_min settings.
		(try_begin),
			(lt, ":show_report", 0),
			(store_mul, ":new_minimum", ":show_report", -1),
			(val_max, ":intel", ":new_minimum"),
		(try_end),
		
		(val_clamp, ":intel", 0, 11),
		(party_set_slot, ":center_no", slot_center_intelligence, ":intel"),
		
		
		(try_begin),
			(eq, ":show_report", 1),
			(neq, ":change", 0),
			(try_begin),
				(ge, ":change", 1),
				(assign, ":color", gpu_green),
				(str_store_string, s2, "@+"),
			(else_try),
				(lt, ":change", 0),
				(assign, ":color", gpu_red),
				(str_clear, s2),
			(else_try),
				(assign, ":color", gpu_black),
				(str_store_string, s2, "@+"),
			(try_end),
			(str_store_party_name, s1, ":center_no"),
			(assign, reg1, ":change"),
			(assign, reg3, ":intel"),
			(eq, ":display_info", 1),
			(display_message, "@Your level of knowledge about {s1} has increased to {reg3}. ({s2}{reg1})", ":color"),
		(try_end),
	]),
	
# script_diplomacy_change_player_relation_with_family
# PURPOSE: For each +1 relation boost a family member receives there is a chance that it is passed on to all other family members.
# EXAMPLE: (call_script, "script_diplomacy_change_player_relation_with_family", ":troop_no", ":change"),
("diplomacy_change_player_relation_with_family",
	[
		(store_script_param, ":troop_base", 1),
		(store_script_param, ":change", 2),
		
		(try_for_range, ":troop_no", companions_begin, kingdom_ladies_end),
			(call_script, "script_troop_get_family_relation_to_troop", ":troop_no", ":troop_base"),
			(assign, ":relation_strength", reg0),
			(ge, ":relation_strength", 1),
			(store_mul, ":chance", ":relation_strength", 3),
			(val_max, ":chance", 15),
			### DIAGNOSTIC+ ###
			# (str_store_troop_name, s31, ":troop_base"),
			# (str_store_troop_name, s32, ":troop_no"),
			# (assign, reg31, ":relation_strength"),
			# (assign, reg32, ":chance"),
			# (display_message, "@{s32} is a {s11} to {s31}, strength {reg31} = {reg32}% chance.", gpu_debug),
			### DIAGNOSTIC- ###
			(assign, ":relation_passed_on", 0),
			(try_for_range, ":unused", 0, ":change"),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", ":chance"),
				(val_add, ":relation_passed_on", 1),
			(try_end),
			(ge, ":relation_passed_on", 1),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_passed_on", 0),
		(try_end),
	]),
]


from util_wrappers import *
from util_scripts import *

scripts_directives = [
	#rename scripts to "insert" switch scripts (see end of scripts[])  
	[SD_RENAME, "change_player_right_to_rule" , "change_player_right_to_rule_orig"],
	[SD_RENAME, "change_player_honor" , "change_player_honor_orig"],
	
	# HOOK: Give +1 relation automatically for each ally hero present at a fight the player helped in.
	[SD_OP_BLOCK_INSERT, "add_log_entry", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (troop_set_slot, ":hero", slot_troop_present_at_event, "$num_log_entries"), 0, 
		[(call_script, "script_post_combat_relation_changes", ":hero", 1),], 1],
	
	# HOOK: Inserts the initializing scripts in game start as needed.
	[SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_diplomacy_initialize"),], 1],
	
	# HOOK: Inserts the ideal prosperity changes.
	[SD_OP_BLOCK_INSERT, "get_center_ideal_prosperity", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (val_max, ":ideal", 0), 0, 
		[
			# (call_script, "script_diplomacy_prosperity_changes", ":center_no"),
			# (val_add, ":ideal", reg1),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(faction_get_slot, ":prosperity_ideal", ":faction_no", slot_faction_prosperity_ideal),
			(val_add, ":ideal", ":prosperity_ideal"),
		], 1],
	
	# HOOK: Inserts a script that forces patrol companies to join the player in battle.
	[SD_OP_BLOCK_INSERT, "let_nearby_parties_join_current_battle", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (try_end), 0, 
		[
			(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_JOIN_COMBAT),
		], 1],
		
] # scripts_rename
                
def modmerge_scripts(orig_scripts):
	# process script directives first
	process_script_directives(orig_scripts, scripts_directives)
	# add remaining scripts
	add_scripts(orig_scripts, scripts, True)
	
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "scripts"
        orig_scripts = var_set[var_name_1]
    
        
		# START do your own stuff to do merging
		
        modmerge_scripts(orig_scripts)

		# END do your own stuff
        
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
