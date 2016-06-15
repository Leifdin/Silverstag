# Quest Pack 2 (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_triggers import *
from module_quests import *
from header_troops import *       # Required by script_qp2_calculate_troop_trading_power

####################################################################################################################
# scripts is a list of script records.
# Each script record contains the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

# ADDING A NEW QUEST:
#  - Add initiation to script "qp2_hook_assessment_initiations".
#  - Add failure condition to script "qp2_check_failure_conditions".
#  - Consider adding to ignore list for humanitarians in script "cf_qp2_ignore_failures".
#  - A new quest script for handling updates needs to be generated.

scripts = [
# script_qp2_game_start
# Contains all initialization scrips needed for Quest Pack 2.
("qp2_game_start",
  [
		# Reset active quests for debugging purposes.
		(try_for_range, ":quest_no", qp2_quests_begin, qp2_quests_end),
			(check_quest_active, ":quest_no"),
			(fail_quest, ":quest_no"),
		(try_end),
		
		# Reset all rivals.
		(try_for_range, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
			(try_for_range, ":slot_no", 200, 400),
				(troop_set_slot, ":troop_no", ":slot_no", 0),
			(try_end),
			(call_script, "script_qp2_trs_initialize_rival", ":troop_no"),
		(try_end),
		
		# Set blocking global.
		(assign, "$qp2_block_trade_quests", 0),
	]),
	
# script_qp2_check_failure_conditions
# Check if any quests should have failed from "script_abort_quest" due to expiration.  Messages are disabled if one of these quests trigger and are automatically re-enabled further down.
# This is to prevent multiple "Quest Failed" messages showing up.
("qp2_check_failure_conditions",
  [
		(store_script_param, ":quest_no", 1),
		
		(try_begin),
			## QUEST: TRADE SHORTAGE ##
			(eq, ":quest_no", "qst_floris_trade_shortage"),
			(call_script, "script_qp2_quest_floris_trade_shortage", floris_quest_fail),
			(set_show_messages, 0),
		(else_try),
			## QUEST: TRADE SURPLUS ##
			(eq, ":quest_no", "qst_floris_trade_surplus"),
			(call_script, "script_qp2_quest_floris_trade_surplus", floris_quest_fail),
			(set_show_messages, 0),
		(else_try),
			## QUEST: FORTUNE FAVORS THE BOLD ##
			(eq, ":quest_no", "qst_floris_trade_fortune_favors_bold"),
			(call_script, "script_qp2_quest_floris_trade_fortune_favors_the_bold", floris_quest_fail),
			(set_show_messages, 0),
		(try_end),
		
	]),

# script_cf_qp2_ignore_failures
# PURPOSE: These quests are not intended to trigger humanitarian companions complaining so they are added to the module_scripts exception list.
("cf_qp2_ignore_failures",
  [
		(store_script_param, ":quest_no", 1),
		
		(neq, ":quest_no", "qst_floris_trade_shortage"),
		(neq, ":quest_no", "qst_floris_trade_surplus"),
		#(neq, ":quest_no", "qst_floris_trade_bargain"),
		(neq, ":quest_no", "qst_floris_trade_fortune_favors_bold"),
		(neq, ":quest_no", "qst_trade_noble_opportunity"),
		(neq, ":quest_no", "qst_trade_discount_enterprise"),
		
	]),
	
# script_cf_qp2_check_no_active_qp2_quests
# PURPOSE: Fail if any of the specified quests are active.
("cf_qp2_check_no_active_qp2_quests",
  [
		# List quests here that should prevent the beginning of a new trade quest.
		(neg|check_quest_active, "qst_floris_trade_surplus"),
		(neg|check_quest_active, "qst_floris_trade_shortage"),
		(neg|check_quest_active, "qst_floris_trade_fortune_favors_bold"),
		
		(this_or_next|neg|check_quest_active, "qst_trade_noble_opportunity"),
		(quest_slot_ge, "qst_trade_noble_opportunity", slot_quest_current_state, qp2_opportunity_provided_loan), # For when we're just waiting to hear back for payment.
		
		(neg|check_quest_active, "qst_trade_discount_enterprise"),
	]),
	
# script_qp2_check_for_trade_quests
# PURPOSE: Determine if a new trade quest should be initiated while assessing local prices in the town market.
("qp2_check_for_trade_quests",
    [
	    (store_script_param, ":quest_override", 1),
		
		# Determine if a quest will be given at all based on current quests.
		(assign, ":block_quest", 1),
		(try_begin),
			# General global option set so that it doesn't block trade quests.
			(eq, "$qp2_block_trade_quests", 0),
			# List quests here that should prevent the beginning of a new trade quest.
			(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
			# qst_floris_trade_bargain - intentionally omitted.  I want this to be able to combine with trade shortage/surplus quests.
			(assign, ":block_quest", 0), # Don't block a new quest beginning.
		(try_end),
		
		# Determine type of quest to give.
		# If one quest isn't available it should try to assign a different quest.
		(assign, ":quest_selection", -1),
		(try_begin),
			(this_or_next|eq, ":block_quest", 0),
			(is_between, ":quest_override", qp2_quests_begin, qp2_quests_end),
			(store_character_level, ":level", "trp_player"),
			
			(try_begin), ### QUEST: FORTUNE FAVORS THE BOLD ###
				(assign, ":quest_no", "qst_floris_trade_fortune_favors_bold"),
				(store_random_in_range, ":roll", 0, 100),
				(this_or_next|lt, ":roll", 10),
				(eq, ":quest_override", ":quest_no"),
				##
				(quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|ge, ":level", 8),
				(eq, ":quest_override", ":quest_no"),
				##
				(assign, ":quest_selection", ":quest_no"),
				(assign, ":quest_script", "script_qp2_quest_floris_trade_fortune_favors_the_bold"),
				(assign, ":slot_rival_quest_status", slot_rival_quest_fortune_status),
				
			(else_try), ### QUEST: TRADE SURPLUS ###
				(assign, ":quest_no", "qst_floris_trade_surplus"),
				(store_random_in_range, ":roll", 0, 100),
				(this_or_next|lt, ":roll", 40),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|ge, ":level", 1),
				(eq, ":quest_override", ":quest_no"),
				##
				(assign, ":quest_selection", ":quest_no"),
				(assign, ":quest_script", "script_qp2_quest_floris_trade_surplus"),
				(assign, ":slot_rival_quest_status", slot_rival_quest_surplus_status),
				
			(else_try), ### QUEST: TRADE SHORTAGE ###
				(assign, ":quest_no", "qst_floris_trade_shortage"),
				(store_random_in_range, ":roll", 0, 100),
				(this_or_next|lt, ":roll", 40),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|ge, ":level", 1),
				(eq, ":quest_override", ":quest_no"),
				##
				(assign, ":quest_selection", ":quest_no"),
				(assign, ":quest_script", "script_qp2_quest_floris_trade_shortage"),
				(assign, ":slot_rival_quest_status", slot_rival_quest_shortage_status),
				
			(else_try), ### QUEST: TRADE NOBLE OPPORTUNITY ###
				(assign, ":quest_no", "qst_trade_noble_opportunity"),
				(store_random_in_range, ":roll", 0, 100),
				(this_or_next|lt, ":roll", 25),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|ge, ":level", 8),
				(eq, ":quest_override", ":quest_no"),
				##
				(assign, ":quest_selection", ":quest_no"),
				(assign, ":quest_script", "script_qp2_quest_trade_noble_opportunity"),
				(assign, ":slot_rival_quest_status", slot_rival_quest_opportunity_status),
				
			(else_try), ### QUEST: TRADE DISCOUNT ENTERPRISE ###
				(assign, ":quest_no", "qst_trade_discount_enterprise"),
				(store_random_in_range, ":roll", 0, 100),
				(this_or_next|lt, ":roll", 15),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(eq, ":quest_override", ":quest_no"),
				##
				(this_or_next|ge, ":level", 8),
				(eq, ":quest_override", ":quest_no"),
				##
				(assign, ":quest_selection", ":quest_no"),
				(assign, ":quest_script", "script_qp2_quest_trade_discount_enterprise"),
				(assign, ":slot_rival_quest_status", slot_rival_quest_discount_ent_status),
				
			(try_end),
		(try_end),
		
		# Initiate the quest.  Text to output needs to be stored in s3 (output of menu "town_trade_assessment").
		(try_begin),
			(this_or_next|eq, ":block_quest", 0), #  1 would have blocked if any other specified trade quest was active.
			(is_between, ":quest_override", qp2_quests_begin, qp2_quests_end),
			
			(ge, ":quest_selection", 0),          # -1 would have blocked if no valid quest was available.
			
			### INITIATE QUEST SCRIPT ###
			(call_script, ":quest_script", floris_quest_begin),
			
			### TRADE RIVAL SYSTEM INITIATION ###
			# ":slot_rival_quest_status" is determined above now.
			
			# Determine slot # for value that stores the rival's current progress in the quest.
			(store_sub, ":slot_offset", slot_rival_quest_shortage_stage, slot_rival_quest_shortage_status),
			(store_add, ":slot_rival_quest_stage", ":slot_rival_quest_status", ":slot_offset"),

			# Determine slot # for value that stores the rival's chance of upgrading status.
			(store_sub, ":slot_offset", slot_rival_quest_shortage_trigger_chance, slot_rival_quest_shortage_status),
			(store_add, ":slot_rival_trigger_chance", ":slot_rival_quest_status", ":slot_offset"),

			# Cycle through all of the rivals to activate the quest.
			(try_for_range, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
				# Qualify the rival's status.
				(troop_slot_eq, ":troop_no", slot_rival_status, qp2_rival_status_active),
				# Activate the quest.
				(call_script, "script_qp2_trs_set_value", ":troop_no", ":slot_rival_quest_status", 1),
				# Set the initial stage.
				(call_script, "script_qp2_trs_set_value", ":troop_no", ":slot_rival_quest_stage", 1),
				# Setup the initial trigger chance.  (Based on how far away they are from target location)
				(quest_get_slot, ":target_center", ":quest_selection", slot_quest_target_center),
				(troop_get_slot, ":current_location", ":troop_no", slot_rival_location),
				(store_distance_to_party_from_party, ":distance", ":current_location", ":target_center"),
				(store_sub, ":difficulty", 40, ":distance"),
				(call_script, "script_qp2_trs_set_value", ":troop_no", ":slot_rival_trigger_chance", ":difficulty"),
				# Set our rival's destination.
				(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_destination, ":target_center"),
			(try_end),
			
		(try_end),
		
		# BUGFIX - Nothing uses reg2, but something is overwriting it within my quest scripts.  This messes up the value for mnu_trade_assessment's text.
		(call_script, "script_get_max_skill_of_player_party", "skl_trade"),
		(assign, reg2, reg0),
    ]),
	
# script_qp2_quest_floris_trade_shortage
# PURPOSE: Handles all quest specific actions for quest "floris_trade_shortage".
("qp2_quest_floris_trade_shortage",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_floris_trade_shortage"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp2_shortage_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp2_shortage_inactive                           = 0
		# qp2_shortage_discovery                          = 1
		# qp2_shortage_picked_up_commodity                = 2
		# qp2_shortage_arrived_in_target_center           = 3
		# qp2_shortage_sold_items_to_town                 = 4
		# qp2_shortage_sold_items_to_merchant             = 5
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            qp2_shortage_discovery),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     -1),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 qp2_shortage_expiration),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          qp2_shortage_cooldown),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  qp2_shortage_cooldown),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   0),
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity,               0),
			(quest_set_slot, ":quest_no", slot_quest_target_center,                   0),
			(quest_set_slot, ":quest_no", slot_quest_secondary_commodity,             0),
			(quest_set_slot, ":quest_no", slot_quest_final_stage,                     qp2_shortage_sold_items_to_town),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_low,            5),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_medium,         5),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_high,           10),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          20), # qp2_shortage_discovery
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          20), # qp2_shortage_picked_up_commodity
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          20), # qp2_shortage_arrived_in_target_center
			(quest_set_slot, ":quest_no", slot_quest_stage_4_trigger_chance,          0),  # qp2_shortage_sold_items_to_town
			(quest_set_slot, ":quest_no", slot_quest_stage_5_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_6_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_7_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_8_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_9_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0),
			
			# Determine target center.
			(assign, ":end_cond", 26),
			(assign, ":center_no", -1),
			(assign, ":center_current", "$current_town"),
			(try_for_range, ":unused", 0, ":end_cond"),
				(store_random_in_range, ":center_no_pick", towns_begin, towns_end),
				(neq, ":center_no_pick", ":center_current"),
				(store_distance_to_party_from_party, ":distance", ":center_no_pick", ":center_current"),
				(is_between, ":distance", 50, 100),
				(assign, ":center_no", ":center_no_pick"),
				(assign, ":end_cond", 0), # Break loop
			(try_end),
			(try_begin),
				(neg|is_between, ":center_no", towns_begin, towns_end), # Filter
				(store_random_in_range, ":center_no", towns_begin, towns_end),
			(try_end),
			(quest_set_slot, ":quest_no", slot_quest_target_center, ":center_no"),
			# Pick the primary commodity.
			(call_script, "script_qp2_determine_best_surplus_item_for_center", ":center_no", -1),
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity, reg1),
			(str_store_item_name, s14, reg1),
			# Setup quest text.
			(str_store_party_name_link, s13, ":center_no"),
			(str_store_string, s61, "str_qp2_shortage_of_s14_in_s13_initiation"), # Needs: s13 (target center), s14 (trade good)
			(str_store_string, s3, "@^You hear of a great shortage of {s14} in the town of {s13}.^{s3}"),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp2_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(quest_get_slot, ":primary_item", ":quest_no", slot_quest_primary_commodity),
			(str_store_item_name, s53, ":primary_item"),
			(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
			(str_store_party_name, s51, ":target_center"),
			(try_begin),
				(eq, ":quest_stage", qp2_shortage_picked_up_commodity),
				(str_store_string, s65, "@You have acquired some {s53}.  Make haste for {s51} before the advantage is ruined by a competitor."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp2_shortage_arrived_in_target_center),
				(str_store_string, s65, "@You have arrived in the town of {s51}.  Deliver your supplies to the local goods merchant before your rivals do so."),
				(assign, ":note_slot", 4),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", 200),
			(assign, ":reward_town_rep", 0),
			(assign, ":reward_town_prosperity", 0),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", 150),
				(val_add, ":reward_town_rep", 1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", 150),
				(val_add, ":reward_town_rep", 1),
				(val_add, ":reward_town_prosperity", 1),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Change town reputation.
			(call_script, "script_change_player_relation_with_center", "$current_town", ":reward_town_rep"),
			# Improve town prosperity.
			(call_script, "script_change_center_prosperity", "$current_town", ":reward_town_prosperity"),
			# Trade Rival System Update
			(call_script, "script_qp2_trs_record_victory_for_rival", "trp_player", ":quest_no"),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp2_quest_floris_trade_surplus
# PURPOSE: Handles all quest specific actions for quest "floris_trade_surplus".
("qp2_quest_floris_trade_surplus",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_floris_trade_surplus"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp2_surplus_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp2_surplus_inactive                            = 0
		# qp2_surplus_discovery                           = 1
		# qp2_surplus_arrived_in_target_center            = 2
		# qp2_surplus_picked_up_commodity                 = 3
		# qp2_surplus_sold_items_to_town                  = 4

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            qp2_surplus_discovery),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     -1),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          1),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  1),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   0),
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity,               0),
			(quest_set_slot, ":quest_no", slot_quest_target_center,                   0),
			(quest_set_slot, ":quest_no", slot_quest_secondary_commodity,             0),
			(quest_set_slot, ":quest_no", slot_quest_final_stage,                     qp2_surplus_sold_items_to_town),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_low,            5),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_medium,         5),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_high,           10),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          20), # qp2_surplus_discovery
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          0),  # qp2_surplus_arrived_in_target_center
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          20), # qp2_surplus_picked_up_commodity
			(quest_set_slot, ":quest_no", slot_quest_stage_4_trigger_chance,          20), # qp2_surplus_sold_items_to_town
			(quest_set_slot, ":quest_no", slot_quest_stage_5_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_6_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_7_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_8_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_9_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0),
			
			# Determine target center.
			(assign, ":end_cond", 26),
			(assign, ":center_no", -1),
			(assign, ":center_current", "$current_town"),
			(try_for_range, ":unused", 0, ":end_cond"),
				(store_random_in_range, ":center_no_pick", towns_begin, towns_end),
				(neq, ":center_no_pick", ":center_current"),
				(store_distance_to_party_from_party, ":distance", ":center_no_pick", ":center_current"),
				(is_between, ":distance", 40, 100),
				(assign, ":center_no", ":center_no_pick"),
				(assign, ":end_cond", 0), # Break loop
			(try_end),
			(try_begin),
				(neg|is_between, ":center_no", towns_begin, towns_end), # Filter
				(store_random_in_range, ":center_no", towns_begin, towns_end),
			(try_end),
			(quest_set_slot, ":quest_no", slot_quest_target_center, ":center_no"),
			# Pick the primary commodity.
			(store_random_in_range, reg1, qp2_trade_goods_begin, qp2_trade_goods_end),
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity, reg1),
			(str_store_item_name, s14, reg1),
			# Setup quest text.
			(str_store_party_name_link, s13, ":center_no"),
			(str_store_string, s61, "str_qp2_surplus_of_s14_in_s13_initiation"), # Needs: s13 (target center), s14 (trade good)
			(str_store_string, s3, "@^You hear of a great surplus of {s14} in the town of {s13}.^{s3}"),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp2_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(quest_get_slot, ":primary_item", ":quest_no", slot_quest_primary_commodity),
			(str_store_item_name, s53, ":primary_item"),
			(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
			(str_store_party_name, s51, ":target_center"),
			(try_begin),
				(eq, ":quest_stage", qp2_surplus_picked_up_commodity),
				(str_store_string, s65, "@You have picked up some {s53} from {s51}.  Now export it to another town to finish the quest."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp2_surplus_arrived_in_target_center),
				(str_store_string, s65, "@You have arrived in the town of {s51}.  The local goods merchant will be looking for a ready buyer."),
				(assign, ":note_slot", 4),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", 100),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", 100),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", 100),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Reward the winning rival for the trade rival system.
			(call_script, "script_qp2_trs_record_victory_for_rival", "trp_player", ":quest_no"),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp2_quest_floris_trade_fortune_favors_the_bold
# PURPOSE: Handles all quest specific actions for quest "floris_trade_surplus".
("qp2_quest_floris_trade_fortune_favors_the_bold",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_floris_trade_fortune_favors_bold"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp2_fortune_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp2_fortune_inactive                            = 0
		# qp2_fortune_arrived_in_primary_center           = 1
		# qp2_fortune_purchased_commodity_in_primary_town = 2
		# qp2_fortune_arrived_in_second_center            = 3
		# qp2_fortune_purchased_commodity_in_second_town  = 4
		# qp2_fortune_completed_route                     = 5

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            qp2_fortune_purchased_commodity_in_primary_town),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     -1),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 60),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          15),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  15),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   0),
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity,               0),
			(quest_set_slot, ":quest_no", slot_quest_target_center,                   0),
			(quest_set_slot, ":quest_no", slot_quest_secondary_commodity,             0),
			(quest_set_slot, ":quest_no", slot_quest_final_stage,                     qp2_fortune_completed_route),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_low,            10),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_medium,         10),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_high,           20),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          0), # qp2_fortune_arrived_in_primary_center
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          0), # qp2_fortune_purchased_commodity_in_primary_town
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          0), # qp2_fortune_arrived_in_second_center
			(quest_set_slot, ":quest_no", slot_quest_stage_4_trigger_chance,          0), # qp2_fortune_purchased_commodity_in_second_town
			(quest_set_slot, ":quest_no", slot_quest_stage_5_trigger_chance,          0), # qp2_fortune_completed_route
			(quest_set_slot, ":quest_no", slot_quest_stage_6_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_7_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_8_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_9_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0),
			
			# Determine target center.
			(assign, ":end_cond", 26),
			(assign, ":center_no", -1),
			(assign, ":center_current", "$current_town"),
			(try_for_range, ":unused", 0, ":end_cond"),
				(store_random_in_range, ":center_no_pick", towns_begin, towns_end),
				(neq, ":center_no_pick", ":center_current"),
				(store_distance_to_party_from_party, ":distance", ":center_no_pick", ":center_current"),
				(is_between, ":distance", 40, 100),
				(assign, ":center_no", ":center_no_pick"),
				(assign, ":end_cond", 0), # Break loop
			(try_end),
			(try_begin),
				(neg|is_between, ":center_no", towns_begin, towns_end), # Filter
				(store_random_in_range, ":center_no", towns_begin, towns_end),
			(try_end),
			(quest_set_slot, ":quest_no", slot_quest_target_center, ":center_no"),
			
			# Pick the primary commodity.
			(call_script, "script_qp2_determine_best_surplus_item_for_center", "$current_town", -1),
			(assign, ":primary_item", reg1),
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity, ":primary_item"),
			(str_store_item_name, s14, ":primary_item"),
			
			# Pick the secondary commodity (if needed).
			(call_script, "script_qp2_determine_best_surplus_item_for_center", ":center_no", ":primary_item"),
			(assign, ":secondary_item", reg1),
			(quest_set_slot, ":quest_no", slot_quest_secondary_commodity, ":secondary_item"),
			(str_store_item_name, s15, ":secondary_item"),
			
			# Setup quest text.
			(str_store_party_name_link, s13, ":center_no"),
			(str_store_string, s61, "str_qp2_fortune_s14_for_s13_and_bring_back_s15_initiation"), # Needs: s13 (target center), s14 (trade good)
			(str_store_string, s3, "@^Word is that the town of {s13} is in need of {s14} and needs someone to transport {s15} back here, but banditry has blocked most caravans.^{s3}"),
			
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp2_quest_title"),
			
			# Special case to initiate the trade route "fortune favors the bold"
			(try_begin),
				(eq, ":quest_no", "qst_floris_trade_fortune_favors_bold"),
				(call_script, "script_qp2_track_town_entry", "$current_town"),
			(try_end),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(quest_get_slot, ":primary_item", ":quest_no", slot_quest_primary_commodity),
			(str_store_item_name, s53, ":primary_item"),
			(quest_get_slot, ":secondary_item", ":quest_no", slot_quest_secondary_commodity),
			(str_store_item_name, s54, ":secondary_item"),
			(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
			(str_store_party_name, s51, ":target_center"),
			(quest_get_slot, ":giver_center", ":quest_no", slot_quest_giver_center),
			(str_store_party_name, s52, ":giver_center"),
			(try_begin),
				(eq, ":quest_stage", qp2_fortune_arrived_in_second_center),
				(str_store_string, s65, "@You have arrived in the town of {s52}.  Pick up some {s53} from the local goods merchant for shipment to {s51}."),
				(assign, ":note_slot", 3),
				(str_clear, s66),
				(add_quest_note_from_sreg, ":quest_no", 4, s66, 0),
				(add_quest_note_from_sreg, ":quest_no", 5, s66, 0),
				(add_quest_note_from_sreg, ":quest_no", 6, s66, 0),
			(else_try),
				(eq, ":quest_stage", qp2_fortune_purchased_commodity_in_second_town),
				(quest_get_slot, ":cycles", "qst_floris_trade_fortune_favors_bold", slot_quest_target_amount),
				(store_add, ":string_no", ":cycles", "str_qp2_fortune_1st"),
				(val_sub, ":string_no", 1),
				(str_store_string, s67, ":string_no"),
				(str_store_string, s65, "@You have acquired some {s53}.  The local goods merchant has asked that you bring it to {s51}, but be wary of the bandits.  This will be your {s67} journey along this route."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp2_fortune_arrived_in_primary_center),
				(str_store_string, s65, "@You have arrived in the town of {s51}.  Pick up some {s54} from the local goods merchant for shipment to {s52}."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp2_fortune_purchased_commodity_in_primary_town),
				(str_store_string, s65, "@You have acquired some {s54}.  The local goods merchant has asked that you bring it to {s52}, but be wary of the bandits."),
				(assign, ":note_slot", 6),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", 500),
			(assign, ":reward_town_rep", 1),
			(assign, ":reward_town_prosperity", 0),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", 500),
				(val_add, ":reward_town_rep", 1),
				(val_add, ":reward_town_prosperity", 1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", 500),
				(val_add, ":reward_town_rep", 1),
				(val_add, ":reward_town_prosperity", 1),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Grant relationship gain with the primary town.
			(quest_get_slot, ":center_no", "qst_floris_trade_fortune_favors_bold", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":center_no", ":reward_town_rep"),
			# Grant prosperity gain for the primary town.
			(call_script, "script_change_center_prosperity", ":center_no", ":reward_town_prosperity"),
			# Grant relationship gain with the secondary town.
			(quest_get_slot, ":center_no", "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":center_no", ":reward_town_rep"),
			# Grant prosperity gain for the secondary town.
			(call_script, "script_change_center_prosperity", ":center_no", ":reward_town_prosperity"),
			# Reward the winning rival for the trade rival system.
			(call_script, "script_qp2_trs_record_victory_for_rival", "trp_player", ":quest_no"),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp2_quest_trade_noble_opportunity
# PURPOSE: Handles all quest specific actions for quest "trade_noble_opportunity".
("qp2_quest_trade_noble_opportunity",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_trade_noble_opportunity"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp2_opportunity_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp2_opportunity_inactive                        = 0
		# qp2_opportunity_begun                           = 1  # You've learned he needs a loan.
		# qp2_opportunity_discussed_with_lord             = 2  # You mentioned his need while speaking with him.
		# qp2_opportunity_provided_loan                   = 3  # You've invested.  Now you need to wait until he's ready to repay the loan.
		# qp2_opportunity_lord_ready_to_repay             = 4  # You've received word (upon entering a town) he's ready to repay you.
		# qp2_opportunity_received_payment                = 5  # You've received payment.

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            qp2_shortage_discovery),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     -1),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          15),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  15),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   0),
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity,               0),
			(quest_set_slot, ":quest_no", slot_quest_target_center,                   0),
			(quest_set_slot, ":quest_no", slot_quest_secondary_commodity,             0),
			(quest_set_slot, ":quest_no", slot_quest_final_stage,                     qp2_opportunity_provided_loan),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_low,            5),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_medium,         5),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_high,           10),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          20), # qp2_opportunity_begun
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          20), # qp2_opportunity_discussed_with_lord
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          20), # qp2_opportunity_provided_loan
			(quest_set_slot, ":quest_no", slot_quest_stage_4_trigger_chance,          20), # qp2_opportunity_lord_ready_to_repay
			(quest_set_slot, ":quest_no", slot_quest_stage_5_trigger_chance,          20), # qp2_opportunity_received_payment
			(quest_set_slot, ":quest_no", slot_quest_stage_6_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_payment_return,                  200),
			(quest_set_slot, ":quest_no", slot_quest_payment_failure_chance,          20),
			(quest_set_slot, ":quest_no", slot_quest_lord_will_repay_loan,            0), # Holds info on if the lord will repay or not.
			(quest_set_slot, ":quest_no", slot_quest_days_remaining_for_repayment,    30), # Days left to count until repayment option.
			
			# Determine lord who wants a loan.  Get giver center based on lord's largest fief.
			(assign, ":lord_in_need", -1),
			(assign, ":lord_wealth", 500000),
			(assign, ":home_center", -1),
			(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
				(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
				(assign, ":fief_owned", -1),
				(try_for_range, ":center_no", centers_begin, centers_end),
					(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
					(store_distance_to_party_from_party, ":distance", ":center_no", "p_main_party"),
					(lt, ":distance", 30),
					(try_begin),
						(party_slot_eq, ":center_no", slot_party_type, spt_town),
						(assign, ":fief_owned", ":center_no"),
					(else_try),
						(party_slot_eq, ":center_no", slot_party_type, spt_castle),
						(this_or_next|eq, ":fief_owned", -1),
						(neg|party_slot_eq, ":fief_owned", slot_party_type, spt_town),
						(assign, ":fief_owned", ":center_no"),
					(else_try),
						(party_slot_eq, ":center_no", slot_party_type, spt_village),
						(this_or_next|eq, ":fief_owned", -1),
						(this_or_next|neg|party_slot_eq, ":fief_owned", slot_party_type, spt_town),
						(neg|party_slot_eq, ":fief_owned", slot_party_type, spt_castle),
						(assign, ":fief_owned", ":center_no"),
					(try_end),
				(try_end),
				(is_between, ":fief_owned", centers_begin, centers_end), # Rule out landless lords.
				(troop_get_slot, ":wealth", ":troop_no", slot_troop_wealth),
				(lt, ":wealth", ":lord_wealth"),
				(neq, ":home_center", "$current_town"), # Prevent this from being too easy.
				(neq, ":lord_in_need", "trp_player"),   # Let's not try to loan ourselves money.
				(assign, ":lord_in_need", ":troop_no"),
				(assign, ":lord_wealth", ":wealth"),
				(assign, ":home_center", ":fief_owned"),
			(try_end),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop, ":lord_in_need"),
			(quest_set_slot, ":quest_no", slot_quest_target_center, ":home_center"),
			# Determine the size of the loan.
			(store_character_level, ":level", "trp_player"),
			(store_mul, ":loan_amount", ":level", 100),
			(val_sub, ":level", 15),
			(val_max, ":level", 0),
			(store_mul, ":loan_excess", ":level", 250),
			(val_add, ":loan_amount", ":loan_excess"),
			(val_add, ":loan_amount", 5000),
			(val_clamp, ":loan_amount", 5000, 12000),
			(quest_set_slot, ":quest_no", slot_quest_target_amount, ":loan_amount"),
			# Setup payment failure chance & return based on quest difficulty.
			(try_begin),
				(eq, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(quest_set_slot, ":quest_no", slot_quest_payment_return, 320),
				(quest_set_slot, ":quest_no", slot_quest_payment_failure_chance, 40),
				
			(else_try),
				(eq, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(quest_set_slot, ":quest_no", slot_quest_payment_return, 260),
				(quest_set_slot, ":quest_no", slot_quest_payment_failure_chance, 30),
			(try_end),
			# Setup quest text.
			(str_store_party_name_link, s13, ":home_center"),
			(str_store_troop_name_link, s14, ":lord_in_need"),
			(str_store_party_name_link, s15, "$current_town"),
			(troop_get_type, reg21, ":lord_in_need"),
			(str_store_string, s61, "@Word in {s15} is that {s14}, {reg21?Lady:Lord} of {s13}, is planning a new campaign and is looking for an investor to help fund the effort.  Getting involved in politics can be quite dangerous, but even more profitable and can curry favors for the future.  Certainly other merchants of wealth will have learned of this opportunity as well so you will need to hurry to {s13}."),
			(str_store_string, s3, "@^You heard rumor that {s14}, {reg21?Lady:Lord} of {s13}, is looking for an investor to fund {reg21?her:his} latest ambition.  Getting involved in politics is dangerous, but potentially quite profitable.^{s3}"),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp2_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Special information needed.
			(quest_get_slot, ":troop_no", ":quest_no", slot_quest_giver_troop),
			(str_store_troop_name_link, s21, ":troop_no"),
			(troop_get_type, reg21, ":troop_no"),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(str_store_party_name_link, s22, ":center_no"),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(assign, ":notify_of_update", 0),
			(try_begin),
				(eq, ":quest_stage", qp2_opportunity_discussed_with_lord),
				(str_store_string, s65, "@After listening to {s21}'s request for financial support you have decided it is too risky."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp2_opportunity_provided_loan),
				(quest_slot_eq, ":quest_no", slot_quest_days_remaining_for_repayment, 30),
				(str_store_string, s65, "@You have agreed to lend {s21} the money {reg21?she:he} needed for a potential return of three times your investment.  You must wait one month for repayment."),
				(assign, ":note_slot", 3),
				(assign, ":notify_of_update", 1),
			(else_try),
				(eq, ":quest_stage", qp2_opportunity_lord_ready_to_repay),
				(str_store_string, s65, "@Word from {s21} has arrived requesting that you visit with {reg21?her:him} in {s22}."),
				(assign, ":note_slot", 4),
				(assign, ":notify_of_update", 1),
			(else_try),
				(eq, ":quest_stage", qp2_opportunity_provided_loan),
				(neg|quest_slot_eq, ":quest_no", slot_quest_days_remaining_for_repayment, 30),
				(quest_get_slot, reg22, ":quest_no", slot_quest_days_remaining_for_repayment),
				(store_sub, reg23, reg22, 1),
				(str_store_string, s65, "@You must wait another {reg22} day{reg23?s:} to hear from {s21}."),
				(str_clear, s64),
				(assign, ":note_slot", 7),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64}{s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(try_begin),
				(eq, ":notify_of_update", 1),
				(display_message, "str_quest_log_updated", gpu_light_blue),
			(try_end),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(quest_get_slot, ":loan_amount", ":quest_no", slot_quest_target_amount),
			(store_div, ":faction_relation", ":loan_amount", 3000),
			(store_div, ":lord_relation", ":loan_amount", 1300),
			(try_begin),
				(eq, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(assign, ":reward_xp", 800),
				(val_clamp, ":faction_relation", 3, 6),
				(val_clamp, ":lord_relation", 5, 10),
			(else_try),
				(eq, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(assign, ":reward_xp", 600),
				(val_clamp, ":faction_relation", 2, 4),
				(val_clamp, ":lord_relation", 3, 7),
			(else_try),
				(eq, "$quest_reactions", QUEST_REACTIONS_LOW),
				(assign, ":reward_xp", 400),
				(val_clamp, ":faction_relation", 1, 3),
				(val_clamp, ":lord_relation", 2, 4),
			(try_end),
			# Award the player experience.
			(add_xp_to_troop, ":reward_xp", "trp_player"),
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_lord_will_repay_loan, 2), # Half payment.
				(assign, ":lord_relation", 2),
				(assign, ":faction_relation", 1),
			(try_end),
			# Award lord relation gain.
			(quest_get_slot, ":troop_no", ":quest_no", slot_quest_giver_troop),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":lord_relation"),
			# Award faction relation gain.
			(store_faction_of_troop, ":faction_no", ":troop_no"),
			(call_script, "script_change_player_relation_with_faction", ":faction_no", ":faction_relation"),
			# Award payment and remove gold from lord wealth.
			(try_begin),
				(neg|quest_slot_eq, ":quest_no", slot_quest_lord_will_repay_loan, 0),
				(quest_get_slot, ":return_factor", ":quest_no", slot_quest_payment_return),
				(val_mul, ":loan_amount", ":return_factor"),
				(val_div, ":loan_amount", 100),
				(troop_add_gold, "trp_player", ":loan_amount"),
				(troop_get_slot, ":wealth", ":troop_no", slot_troop_wealth),
				(val_sub, ":wealth", ":loan_amount"),
				(troop_set_slot, ":troop_no", slot_troop_wealth, ":wealth"),
			(try_end),
			# Trade Rival System Update
			(call_script, "script_qp2_trs_record_victory_for_rival", "trp_player", ":quest_no"),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp2_quest_trade_discount_enterprise
# PURPOSE: Handles all quest specific actions for quest "trade_noble_opportunity".
("qp2_quest_trade_discount_enterprise",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_trade_discount_enterprise"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp2_discount_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp2_discount_inactive                           = 0
		# qp2_discount_discovered                         = 1
		# qp2_discount_spoken_with_guildmaster            = 2
		# qp2_discount_purchased                          = 3
		# qp2_discount_declined                           = 4

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            qp2_discount_discovered),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     -1),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  30),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   0),
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity,               0),
			(quest_set_slot, ":quest_no", slot_quest_target_center,                   0),
			(quest_set_slot, ":quest_no", slot_quest_secondary_commodity,             0),
			(quest_set_slot, ":quest_no", slot_quest_final_stage,                     qp2_discount_purchased),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_low,            5),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_medium,         5),
			(quest_set_slot, ":quest_no", slot_quest_proficiency_gain_high,           10),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          20), # qp2_discount_discovered
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          75), # qp2_discount_spoken_with_guildmaster
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          75), # qp2_discount_purchased
			(quest_set_slot, ":quest_no", slot_quest_stage_4_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_5_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_6_trigger_chance,          0),
			(quest_set_slot, ":quest_no", slot_quest_stage_7_trigger_chance,          0),
			# (quest_set_slot, ":quest_no", slot_quest_enterprise_discount,             0),
			# (quest_set_slot, ":quest_no", slot_quest_enterprise_item,                 0),
			# (quest_set_slot, ":quest_no", slot_quest_enterprise_name,                 0),
			# Pick a suitable destination center.
			(try_for_range, ":attempts", 0, 100),
				(try_begin),
					(lt, ":attempts", 10),
					(call_script, "script_qus_select_random_center", center_is_town, 20, 60, "$current_town"),
				(else_try),
					(lt, ":attempts", 50),
					(call_script, "script_qus_select_random_center", center_is_town, 10, 90, "$current_town"),
				(else_try),
					(store_random_in_range, ":center_no", towns_begin, towns_end),
				(try_end),
				(assign, ":center_no", reg1),
				# Ensure player doesn't already have an enterprise here.
				(party_slot_eq, "$g_encountered_party", slot_center_player_enterprise, 0),
				# Try to pick a location not hostile to the player's faction. (unless we're running out of options)
				(store_faction_of_party, ":faction_no", ":center_no"),
				(store_relation, ":relation", "$players_kingdom", ":faction_no"),
				(this_or_next|ge, ":relation", -10),
				(ge, ":attempts", 50),
				(assign, ":best_center", ":center_no"),
				(break_loop), # WSE
			(try_end),
			(assign, ":center_no", ":best_center"),
			# Determine best enterprise.
			(store_troop_gold, ":gold", "trp_player"),
			(call_script, "script_qp2_determine_most_profitable_enterprise_for_center", ":center_no", ":gold"),
			(assign, ":trade_good", reg1),
			(try_begin),
				(lt, ":trade_good", 1), # Nothing met the requirements.
				(assign, ":trade_good", "itm_leatherwork"), ## Floris Naming Difference
			(try_end),
			(quest_set_slot, ":quest_no", slot_quest_enterprise_item, ":trade_good"),
			(call_script, "script_get_enterprise_name", ":trade_good"),
			(str_store_string, s14, reg0),
			(quest_set_slot, ":quest_no", slot_quest_enterprise_name, reg0),
			# Determine discount.
			(store_mul, ":discount", "$quest_reactions", 8),
			(val_add, ":discount", 16), # Sets us up for 24%, 32% or 40% discounts based on difficulty.
			(quest_set_slot, ":quest_no", slot_quest_enterprise_discount, ":discount"),
			# Setup quest text.
			(str_store_party_name_link, s13, ":center_no"),
			(str_store_string, s61, "@You have learned from one of your merchant contacts that an acquiantance of his in {s13} has been trying to sell his {s14} and is willing to do so at a considerable discount.  Interested parties should consult with the local guildmaster there."),
			(str_store_string, s3, "@^One of your merchant mentioned that an old friend of his in {s13} has been trying to sell his {s14} unsuccessfully and is offering a considerable discount.^{s3}"),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp2_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Special information needed.
			
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(assign, ":notify_of_update", 0),
			(try_begin),
				(eq, ":quest_stage", qp2_opportunity_discussed_with_lord),
				(str_store_string, s65, "@Placeholder text.  This needs to be updated."),
				(assign, ":note_slot", 3),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64}{s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(try_begin),
				(eq, ":notify_of_update", 1),
				(display_message, "str_quest_log_updated", gpu_light_blue),
			(try_end),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			# Award the player experience.
			#(add_xp_to_troop, ":reward_xp", "trp_player"),
			# Trade Rival System Update
			(call_script, "script_qp2_trs_record_victory_for_rival", "trp_player", ":quest_no"),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp2_alter_item_price
# PURPOSE: Alters the price modifier on an item based upon current quests in progress.
("qp2_alter_item_price",
  [
		(store_script_param, ":center_no",     1),
		(store_script_param, ":item_no",       2),
		(store_script_param, ":transaction",   3),
		
		(assign, ":penalty", reg0), # Should be populated from script_get_trade_penalty or script_dplmc_get_trade_penalty depending on which is used.
		(assign, ":price_shift", 0),
		
		(try_begin),
			(is_between, ":center_no", centers_begin, centers_end),
			(neg|is_between, ":center_no", castles_begin, castles_end),
			
			# Determine the competency of our best trader.
			(call_script, "script_get_max_skill_of_player_party", "skl_trade"), # Stores skill level (reg0) & trader's troop_id (reg1)
			(call_script, "script_qp2_calculate_troop_trading_power", reg1),
			(assign, ":trading_power", reg1),
			
			# Market center is valid, check if it should be altered.
			(try_begin),
				### QUEST: TRADE SURPLUS ###
				(check_quest_active, "qst_floris_trade_surplus"),
				(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_target_center, ":center_no"),
				(quest_slot_ge, "qst_floris_trade_surplus", slot_quest_current_state, qp2_surplus_arrived_in_target_center),
				(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_primary_commodity, ":item_no"),
				
				(try_begin),
					(val_add, ":price_shift", 33), # -15
					(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
					(val_add, ":price_shift", 33), # -10
					(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
					(val_add, ":price_shift", 34), # -10
				(try_end),
				
				(val_mul, ":price_shift", ":trading_power"),
				(val_div, ":price_shift", -100), # Negative to flip the sign back to negative.
				
				(try_begin),
					(neq, ":transaction", qp2_buying_an_item),
					(val_mul, ":price_shift", -3),  # If there is a surplus then they won't want to pay much for that commodity.
					(val_div, ":price_shift", 2),
				(try_end),
				
			(else_try),
				### QUEST: TRADE SHORTAGE ###
				(check_quest_active, "qst_floris_trade_shortage"),
				(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_target_center, ":center_no"),
				(quest_slot_ge, "qst_floris_trade_shortage", slot_quest_current_state, qp2_shortage_discovery),
				(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_primary_commodity, ":item_no"),
				
				(try_begin),
					(val_add, ":price_shift", 33), # -15
					(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
					(val_add, ":price_shift", 33), # -10
					(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
					(val_add, ":price_shift", 34), # -10
				(try_end),
				
				(val_mul, ":price_shift", ":trading_power"),
				(val_div, ":price_shift", -100), # Negative to flip the sign back to negative.
				(try_begin),
					(neq, ":transaction", qp2_selling_an_item),
					(val_mul, ":price_shift", -3),  # If there is a shortage then they won't want to part with a commodity easily.
					(val_div, ":price_shift", 2),
				(try_end),
				
			(else_try),
				### QUEST: FORTUNE FAVORS THE BOLD ###
				(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
				(assign, ":pass", 0),
				(try_begin), # @ secondary center BUYING primary center item.
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, ":center_no"),
					(this_or_next|quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_second_center),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_second_town),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_primary_commodity, ":item_no"),
					(assign, ":pass", 1),
					(assign, ":transaction_check", qp2_buying_an_item),
				(else_try), # @ primary center BUYING secondary center item.
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_center, ":center_no"),
					(this_or_next|quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_primary_center),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_primary_town),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_secondary_commodity, ":item_no"),
					(assign, ":pass", 1),
					(assign, ":transaction_check", qp2_buying_an_item),
				(else_try), # @ primary center SELLING primary center item.
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_center, ":center_no"),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_primary_center),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_primary_commodity, ":item_no"),
					(assign, ":pass", 1),
					(assign, ":transaction_check", qp2_selling_an_item),
				(else_try), # @ secondary center SELLING secondary center item.
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, ":center_no"),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_second_center),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_secondary_commodity, ":item_no"),
					(assign, ":pass", 1),
					(assign, ":transaction_check", qp2_selling_an_item),
				(try_end),
				(eq, ":pass", 1),
				
				(try_begin),
					(val_add, ":price_shift", 33), # -15
					(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
					(val_add, ":price_shift", 33), # -10
					(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
					(val_add, ":price_shift", 34), # -10
				(try_end),
				
				(val_mul, ":price_shift", ":trading_power"),
				(val_div, ":price_shift", -100), # Negative to flip the sign back to negative.
				(try_begin),
					(neq, ":transaction", ":transaction_check"),
					(val_mul, ":price_shift", -3),  # If there is a shortage then they won't want to part with a commodity easily.
					(val_div, ":price_shift", 2),
				(try_end),
				
			(try_end),
			
		(try_end),
		
		(try_begin),
			(key_is_down, key_space),
			(assign, ":price_shift", 0),
		(try_end),
				
		(store_add, reg0, ":penalty", ":price_shift"),
	]),
	
# script_qp2_calculate_troop_trading_power
# PURPOSE: Based on the input of a troop ID returns the trading competency of that troop to reg1.
("qp2_calculate_troop_trading_power",
  [
		(store_script_param, ":troop_no", 1),
		
		# Trade contribution = Trade Skill *2 for levels 1-3, *3 for levels 4-7, and *4 for levels 8-10.
		(store_skill_level, ":skill_trade", "skl_persuasion", ":troop_no"),
		(try_begin),
			(ge, ":skill_trade", 8),
			(store_sub, ":trade_bonus", ":skill_trade", 7),
			(val_mul, ":trade_bonus", 4),
			(val_add, ":trade_bonus", 18),
		(else_try),
			(ge, ":skill_trade", 4),
			(store_sub, ":trade_bonus", ":skill_trade", 3),
			(val_mul, ":trade_bonus", 3),
			(val_add, ":trade_bonus", 6),
		(else_try),
			(store_mul, ":trade_bonus", ":skill_trade", 2),
		(try_end),
		# Persuasion contribution = Persuasion Skill *1 for levels 1-3, *2 for levels 4-7, and *3 for levels 8-10.
		(store_skill_level, ":skill_persuasion", "skl_persuasion", ":troop_no"),
		(try_begin),
			(ge, ":skill_persuasion", 8),
			(store_sub, ":persuasion_bonus", ":skill_persuasion", 7),
			(val_mul, ":persuasion_bonus", 4),
			(val_add, ":persuasion_bonus", 18),
		(else_try),
			(ge, ":skill_persuasion", 4),
			(store_sub, ":persuasion_bonus", ":skill_persuasion", 3),
			(val_mul, ":persuasion_bonus", 3),
			(val_add, ":persuasion_bonus", 6),
		(else_try),
			(store_mul, ":persuasion_bonus", ":skill_persuasion", 2),
		(try_end),
		# Intelligence contribution = INT - 10
		(store_attribute_level, ":intelligence", ":troop_no", ca_intelligence),
		(val_sub, ":intelligence", 10),
		(val_max, ":intelligence", 0),
		
		# Put everything together.
		(assign, ":trading_power", 25),
		(val_add, ":trading_power", ":trade_bonus"),
		(val_add, ":trading_power", ":persuasion_bonus"),
		(val_add, ":trading_power", ":intelligence"),

		(assign, reg1, ":trading_power"),
	]),

# script_qp2_track_when_items_are_bought
# PURPOSE: Checks when items are bought in the game and updates quest stages as needed.
("qp2_track_when_items_are_bought",
  [
		(store_script_param, ":item_no", 1),
		(try_begin),
			##### QUEST: TRADE SURPLUS #####
			(check_quest_active, "qst_floris_trade_surplus"),
			(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_target_center, "$current_town"),
			(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_primary_commodity, ":item_no"),
			(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_current_state, qp2_surplus_arrived_in_target_center),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_surplus", qp2_surplus_picked_up_commodity),
			(call_script, "script_qp2_quest_floris_trade_surplus", floris_quest_update),
			(ge, DEBUG_QUEST_PACK_2, 1),
			(display_message, "@Quest Progress: 'Trade Surplus' advanced to 'picked up commodity' stage.", gpu_green),
		(else_try),
			##### QUEST: TRADE SHORTAGE #####
			(check_quest_active, "qst_floris_trade_shortage"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_primary_commodity, ":item_no"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_current_state, qp2_shortage_discovery),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_shortage", qp2_shortage_picked_up_commodity),
			(call_script, "script_qp2_quest_floris_trade_shortage", floris_quest_update),
			(ge, DEBUG_QUEST_PACK_2, 1),
			(display_message, "@Quest Progress: 'Trade Shortage' advanced to 'picked up commodity' stage.", gpu_green),
		(else_try),
			##### QUEST: FORTUNE FAVORS THE BOLD ##### @ PRIMARY TOWN
			(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_center, "$current_town"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_secondary_commodity, ":item_no"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_primary_center),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_fortune_favors_bold", qp2_fortune_purchased_commodity_in_primary_town),
			(call_script, "script_qp2_quest_floris_trade_fortune_favors_the_bold", floris_quest_update),
			(ge, DEBUG_QUEST_PACK_2, 1),
			(display_message, "@Quest Progress: 'Trade Fortune' advanced to 'picked up commodity' in 'primary town' stage.", gpu_green),
		(else_try),
			##### QUEST: FORTUNE FAVORS THE BOLD ##### @ SECONDARY TOWN
			(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, "$current_town"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_primary_commodity, ":item_no"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_second_center),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_fortune_favors_bold", qp2_fortune_purchased_commodity_in_second_town),
			(call_script, "script_qp2_quest_floris_trade_fortune_favors_the_bold", floris_quest_update),
			(ge, DEBUG_QUEST_PACK_2, 1),
			(display_message, "@Quest Progress: 'Trade Fortune' advanced to 'picked up commodity' in 'primary town' stage.", gpu_green),
		(try_end),
	]),
	
# script_qp2_track_when_items_are_sold
# PURPOSE: Checks when items are sold in the game and updates quest stages as needed.
("qp2_track_when_items_are_sold",
  [
		(store_script_param, ":item_no", 1),
		(try_begin),
			##### QUEST: TRADE SURPLUS #####
			(check_quest_active, "qst_floris_trade_surplus"),
			(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_primary_commodity, ":item_no"),
			(neg|quest_slot_eq, "qst_floris_trade_surplus", slot_quest_target_center, "$current_town"),
			(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_current_state, qp2_surplus_picked_up_commodity),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_surplus", qp2_surplus_sold_items_to_town),
		(else_try),
			##### QUEST: TRADE SHORTAGE #####
			(check_quest_active, "qst_floris_trade_shortage"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_target_center, "$current_town"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_primary_commodity, ":item_no"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_current_state, qp2_shortage_arrived_in_target_center),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_shortage", qp2_shortage_sold_items_to_town),
		(else_try),
			##### QUEST: FORTUNE FAVORS THE BOLD ##### @ SECONDARY TOWN
			(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, "$current_town"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_secondary_commodity, ":item_no"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_second_town),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_fortune_favors_bold", qp2_fortune_completed_route),
		(try_end),
	]),
	
# script_qp2_increase_merchant_stock
# PURPOSE: Checks to see if a merchant has enough of a given item upon entry into town and adds more if not.
("qp2_increase_merchant_stock",
  [
		(store_script_param, ":quest_no", 1),
		(store_script_param, ":minimum", 2),
		
		# Make sure the goods merchant has enough of the trade goods in his inventory to call it a 'surplus'.
		(store_sub, ":troop_merchant", "$current_town", towns_begin),
		(val_add, ":troop_merchant", "trp_town_1_merchant"),
		
		(try_begin),
			(eq, ":quest_no", "qst_floris_trade_fortune_favors_bold"),
			(quest_slot_eq, ":quest_no", slot_quest_target_center, "$current_town"),
			(quest_get_slot, ":item_no", ":quest_no", slot_quest_secondary_commodity),
		(else_try),
			(eq, ":quest_no", "qst_floris_trade_fortune_favors_bold"),
			(quest_slot_eq, ":quest_no", slot_quest_giver_center, "$current_town"),
			(quest_get_slot, ":item_no", ":quest_no", slot_quest_primary_commodity),
		(else_try),
			(quest_slot_eq, ":quest_no", slot_quest_target_center, "$current_town"),
			(quest_get_slot, ":item_no", ":quest_no", slot_quest_primary_commodity),
		(try_end),
		(store_item_kind_count, ":item_count", ":item_no", ":troop_merchant"),
		(try_begin),
			(lt, ":item_count", ":minimum"),
			(store_sub, ":add_count", ":minimum", ":item_count"),
			(ge, ":add_count", 1),
			(troop_add_items, ":troop_merchant", ":item_no", ":add_count"),
		(else_try),
			(assign, ":add_count", 0),
		(try_end),
		(try_begin),
			(this_or_next|ge, DEBUG_QUEST_PACK_2, 1),
			(ge, DEBUG_QUEST_PACK_5, 1),
			(ge, ":add_count", 1),
			(assign, reg31, ":add_count"),
			(str_store_item_name, s31, ":item_no"),
			(display_message, "@DEBUG (QP2/5): Added {reg31} {s31} to merchant's inventory.", gpu_debug),
		(try_end),
	]),
	
# script_qp2_determine_best_surplus_item_for_center
# PURPOSE: Based on a specific town checks the local goods merchant to see what the best trade good would be to call a surplus as opposed to random choice.
#          Stores surplus item ID to reg1.
("qp2_determine_best_surplus_item_for_center",
  [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":prohibited_item", 2),
		
		# Make sure the goods merchant has enough of the trade goods in his inventory to call it a 'surplus'.
		(store_sub, ":troop_merchant", ":center_no", towns_begin),
		(val_add, ":troop_merchant", "trp_town_1_merchant"),
		(assign, ":item_no_surplus", -1),
		(assign, ":item_count_surplus", -1),
		(try_for_range, ":item_no_current", qp2_trade_goods_begin, qp2_trade_goods_end),
			(store_item_kind_count, ":item_count_current", ":item_no_current", ":troop_merchant"),
			(store_item_value, ":item_value_current", ":item_no_current"),
			(try_begin),
				(is_between, ":item_no_surplus", qp2_trade_goods_begin, qp2_trade_goods_end),
				(store_item_value, ":item_value_surplus", ":item_no_surplus"),
				(store_item_kind_count, ":item_count_surplus", ":item_no_surplus", ":troop_merchant"),
			(try_end),
			(ge, ":item_count_current", ":item_count_surplus"),
			(this_or_next|gt, ":item_count_current", ":item_count_surplus"),
			(ge, ":item_value_current", ":item_value_surplus"),
			(this_or_next|neq, ":item_no_current", ":prohibited_item"),
			(eq, ":prohibited_item", -1),
			
			# (assign, reg21, ":item_count_current"),
			# (str_store_item_name, s31, ":item_no_current"),
			# (str_store_party_name, s32, ":center_no"),
			# (display_message, "@DEBUG (QP2): Found {reg21} {s31} in {s32}.", gpu_debug),
			
			(assign, ":item_no_surplus", ":item_no_current"), # Use this as the new best surplus item.
			#(assign, ":item_count_surplus", ":item_count_current"),
		(try_end),
		(try_begin),
			(is_between, ":item_no_surplus", qp2_trade_goods_begin, qp2_trade_goods_end),
			(assign, reg1, ":item_no_surplus"),
			(try_begin),
				(ge, DEBUG_QUEST_PACK_2, 1),
				(store_item_kind_count, reg21, ":item_no_surplus", ":troop_merchant"),
				(str_store_item_name, s31, ":item_no_surplus"),
				(str_store_party_name, s32, ":center_no"),
				(display_message, "@DEBUG (QP2): Discovered {reg21} {s31} in {s32}.", gpu_debug),
			(try_end),
		(else_try),
			(display_message, "@ERROR! -> Quest cound not determine best surplus item.", gpu_red),
			(assign, reg1, qp2_trade_goods_begin),
		(try_end),
		
	]),
	
# script_qp2_track_town_entry
# PURPOSE: Checks when the player enters a town using script "music_set_situation_with_culture" called in menu "town" to update quest stages as needed.
("qp2_track_town_entry",
  [
		(store_script_param, ":center_no", 1),
		(store_troop_gold, reg50, "trp_player"),
		(try_begin),
			##### QUEST: TRADE SURPLUS #####
			(check_quest_active, "qst_floris_trade_surplus"),
			(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_target_center, ":center_no"),
			(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_current_state, qp2_surplus_discovery),
			(call_script, "script_qp2_increase_merchant_stock", "qst_floris_trade_surplus", 3),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_surplus", qp2_surplus_arrived_in_target_center),
			(call_script, "script_qp2_quest_floris_trade_surplus", floris_quest_update),
			
		(else_try),
			##### QUEST: TRADE SURPLUS #####
			(check_quest_active, "qst_floris_trade_surplus"),
			(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_current_state, qp2_surplus_sold_items_to_town),
			(call_script, "script_qp2_quest_floris_trade_surplus", floris_quest_succeed),
			
		(else_try),
			##### QUEST: TRADE SHORTAGE #####
			(check_quest_active, "qst_floris_trade_shortage"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_target_center, ":center_no"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_current_state, qp2_shortage_picked_up_commodity),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_shortage", qp2_shortage_arrived_in_target_center),
			(call_script, "script_qp2_quest_floris_trade_shortage", floris_quest_update),
			
		(else_try),
			##### QUEST: TRADE SHORTAGE #####
			(check_quest_active, "qst_floris_trade_shortage"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_target_center, ":center_no"),
			(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_current_state, qp2_shortage_sold_items_to_town),
			(call_script, "script_qp2_quest_floris_trade_shortage", floris_quest_succeed),
			
		(else_try),
			##### QUEST: TRADE FORTUNE ##### @ Primary Town
			(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_center, ":center_no"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_second_town),
			(call_script, "script_qp2_increase_merchant_stock", "qst_floris_trade_fortune_favors_bold", 2),
			(call_script, "script_common_quest_change_state", "qst_floris_trade_fortune_favors_bold", qp2_fortune_arrived_in_primary_center),
			(call_script, "script_qp2_quest_floris_trade_fortune_favors_the_bold", floris_quest_update),
			
		(else_try),
			##### QUEST: TRADE FORTUNE ##### @ Secondary Town
			(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, ":center_no"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_primary_town),
			(try_begin),
				(neg|quest_slot_ge, "qst_floris_trade_fortune_favors_bold", slot_quest_target_amount, 4),
				(call_script, "script_common_quest_change_slot", "qst_floris_trade_fortune_favors_bold", slot_quest_target_amount, 1),
				# Continue the cycle.
				(call_script, "script_common_quest_change_state", "qst_floris_trade_fortune_favors_bold", qp2_fortune_arrived_in_second_center),
				(call_script, "script_qp2_increase_merchant_stock", "qst_floris_trade_fortune_favors_bold", 2),
				(call_script, "script_qp2_quest_floris_trade_fortune_favors_the_bold", floris_quest_update),
			(else_try),
				# Break the cycle.
				(call_script, "script_common_quest_change_state", "qst_floris_trade_fortune_favors_bold", qp2_fortune_completed_route),
			(try_end),
			
		(else_try),
			##### QUEST: TRADE FORTUNE ##### @ Broken Cycle
			(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, ":center_no"),
			(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_completed_route),
			(call_script, "qst_floris_trade_fortune_favors_bold", floris_quest_succeed),
		(try_end),
	]),
	
# script_qp2_trs_record_victory_for_rival
# PURPOSE: Set a rival as having completed a quest.
#          Cause the player and all other rivals to fail the quest due to being too slow.
#          Store previous quest information for every rival and then clean out quest info.
#          Assign winning rival the rewards for being first.
("qp2_trs_record_victory_for_rival",
  [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":quest_no", 2),
		
		# Switch out trp_player for the trade rival file for the player.
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(assign, ":troop_no", "trp_trade_rival_p"),
		(try_end),
		
		(try_begin),
			##### QUEST: TRADE SURPLUS #####
			(eq, ":quest_no", "qst_floris_trade_surplus"),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(store_sub, ":faction_slot", ":faction_no", kingdoms_begin),
			(val_add, ":faction_slot", slot_rival_relation_fac_player),
			(call_script, "script_qp2_trs_change_value", ":troop_no", ":faction_slot", 2),
			(assign, ":quest_slot_begin", slot_rival_quest_surplus_status),
			# Determine proficiency award
			(call_script, "script_qp2_trs_determine_proficiency_gain", ":quest_no"),
			(assign, ":primary_gain", reg1),
			(assign, ":secondary_gain", reg2),
			(ge, DEBUG_QUEST_PACK_2, 1),
			(display_message, "@Quest Progress: 'Trade Surplus' advanced to 'sold items to town' stage.", gpu_green),
		(else_try),
			##### QUEST: TRADE SHORTAGE #####
			(eq, ":quest_no", "qst_floris_trade_shortage"),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(store_sub, ":faction_slot", ":faction_no", kingdoms_begin),
			(val_add, ":faction_slot", slot_rival_relation_fac_player),
			(call_script, "script_qp2_trs_change_value", ":troop_no", ":faction_slot", 4),
			(assign, ":quest_slot_begin", slot_rival_quest_shortage_status),
			# Determine proficiency award
			(call_script, "script_qp2_trs_determine_proficiency_gain", ":quest_no"),
			(assign, ":primary_gain", reg1),
			(assign, ":secondary_gain", reg2),
			(ge, DEBUG_QUEST_PACK_2, 1),
			(display_message, "@Quest Progress: 'Trade Shortage' advanced to 'sold items to town' stage.", gpu_green),
		(else_try),
			##### QUEST: TRADE FORTUNE FAVORS THE BOLD #####
			(eq, ":quest_no", "qst_floris_trade_fortune_favors_bold"),
			# Primary Center
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(store_sub, ":faction_slot", ":faction_no", kingdoms_begin),
			(val_add, ":faction_slot", slot_rival_relation_fac_player),
			(call_script, "script_qp2_trs_change_value", ":troop_no", ":faction_slot", 10),
			# Secondary Center
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_giver_center),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(store_sub, ":faction_slot", ":faction_no", kingdoms_begin),
			(val_add, ":faction_slot", slot_rival_relation_fac_player),
			(call_script, "script_qp2_trs_change_value", ":troop_no", ":faction_slot", 10),
			(assign, ":quest_slot_begin", slot_rival_quest_fortune_status),
			# Determine proficiency award
			(call_script, "script_qp2_trs_determine_proficiency_gain", ":quest_no"),
			(assign, ":primary_gain", reg1),
			(assign, ":secondary_gain", reg2),
			(ge, DEBUG_QUEST_PACK_2, 1),
			(display_message, "@Quest Progress: 'Trade Fortune' advanced to 'sold items to town' stage.", gpu_green),
		(try_end),
		
		# Award Proficiency Gains
		(try_for_range, ":troop_rival", qp2_trade_rivals_begin, qp2_trade_rivals_end),
			(try_begin),
				(eq, ":troop_rival", ":troop_no"),
				(call_script, "script_qp2_trs_add_proficiency_to_rival", ":troop_rival", ":primary_gain"),
			(else_try),
				(call_script, "script_qp2_trs_add_proficiency_to_rival", ":troop_rival", ":secondary_gain"),
			(try_end),
		(try_end),
			
		# Update the "last attempted quest" information.
		(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
		(try_for_range, ":troop_rival", qp2_trade_rivals_begin, qp2_trade_rivals_end),
			(call_script, "script_qp2_trs_set_value", ":troop_rival", slot_rival_last_quest_attempted,   ":quest_no"),
			(call_script, "script_qp2_trs_set_value", ":troop_rival", slot_rival_last_quest_winner,      ":troop_no"),
			(call_script, "script_qp2_trs_set_value", ":troop_rival", slot_rival_last_quest_destination, ":center_no"),
			(call_script, "script_qp2_trs_set_value", ":troop_rival", slot_rival_last_quest_focus,       0),
			(call_script, "script_qp2_trs_set_value", ":troop_rival", slot_rival_last_quest_commentary,  0),
			# Cleanup the quest that just ended.
			(store_add, ":quest_slot_end", ":quest_slot_begin", 10),
			(try_for_range, ":quest_slot", ":quest_slot_begin", ":quest_slot_end"),
				(call_script, "script_qp2_trs_set_value", ":troop_rival", ":quest_slot", 0),
			(try_end),
		(try_end),
		
		# If player was not the winner then he needs to fail the quest.
		(try_begin),
			# Make sure the player didn't win the quest.
			(neq, ":troop_no", "trp_player"),
			(neq, ":troop_no", "trp_trade_rival_p"),
			(check_quest_active, ":quest_no"), # Error filter
			# Fail the quest.
			(call_script, "script_qp2_quest_floris_trade_shortage", floris_quest_fail),
			(str_store_troop_name, s31, ":troop_no"),
			(str_store_quest_name, s32, ":quest_no"),
			(display_message, "@{s31} has completed quest '{s32}' before you.", gpu_red),
		(try_end),
		
	]),

# script_qp2_trs_change_value
# PURPOSE: Changes a trade rival character's given slot by a given value.
("qp2_trs_change_value",
  [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":slot_no",  2),
		(store_script_param, ":value",    3),
		#(store_script_param, ":display",  4),
		
		# Switch out trp_player for the trade rival file for the player.
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(assign, ":troop_no", "trp_trade_rival_p"),
		(try_end),
		
		(troop_get_slot, ":temp_value", ":troop_no", ":slot_no"),
		(val_add, ":temp_value", ":value"),
		(troop_set_slot, ":troop_no", ":slot_no", ":temp_value"),
		(try_begin),
			(ge, DEBUG_QUEST_PACK_2, 1),
			#(ge, ":display", 0),
			(str_store_troop_name, s31, ":troop_no"),
			(assign, reg31, ":slot_no"),
			(assign, reg32, ":value"),
			(assign, reg33, ":temp_value"),
			(try_begin),
				(ge, ":value", 1),
				(str_store_string, s32, "@increased by +{reg32} to"),
			(else_try),
				(lt, ":value", 0),
				(str_store_string, s32, "@reduced by {reg32} to"),
			(else_try),
				(str_store_string, s32, "@remained unchanged at"),
			(try_end),
			(try_begin),
				(is_between, ":slot_no", slot_rival_data_begin, slot_rival_data_end),
				(store_sub, ":offset", ":slot_no", slot_rival_data_begin),
				(store_add, ":string_no", ":offset", "str_qp2_rival_slot_200"),
				(str_store_string, s33, ":string_no"),
			(else_try),
				(str_store_string, s33, "@UNRECOGNIZED SLOT"),
				(assign, ":string_no", 0),
			(try_end),
			(str_store_string, s38, ":string_no"),
			(str_store_string, s39, "str_qp2_rival_data_unused"),
			(this_or_next|ge, DEBUG_QUEST_PACK_2, 2),
			(neg|str_equals, s38, s39),
			(display_message, "@DEBUG (TRS): Rival '{s31}' {s33} [{reg31}] {s32} {reg33}.", gpu_debug),
		(try_end),
	]),
	
# script_qp2_trs_set_value
# PURPOSE: Changes a trade rival character's given slot to a given value.
("qp2_trs_set_value",
  [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":slot_no",  2),
		(store_script_param, ":value",    3),
		#(store_script_param, ":display",  4),
		
		# Switch out trp_player for the trade rival file for the player.
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(assign, ":troop_no", "trp_trade_rival_p"),
		(try_end),
		
		(troop_set_slot, ":troop_no", ":slot_no", ":value"),
		(try_begin),
			(ge, DEBUG_QUEST_PACK_2, 1),
			#(ge, ":display", 0),
			(str_store_troop_name, s31, ":troop_no"),
			(assign, reg31, ":slot_no"),
			(assign, reg32, ":value"),
			(try_begin),
				(is_between, ":slot_no", slot_rival_data_begin, slot_rival_data_end),
				(store_sub, ":offset", ":slot_no", slot_rival_data_begin),
				(store_add, ":string_no", ":offset", "str_qp2_rival_slot_200"),
				(str_store_string, s32, ":string_no"),
			(else_try),
				(str_store_string, s32, "@UNRECOGNIZED SLOT"),
				(assign, ":string_no", 0),
			(try_end),
			(str_store_string, s38, ":string_no"),
			(str_store_string, s39, "str_qp2_rival_data_unused"),
			(this_or_next|ge, DEBUG_QUEST_PACK_2, 2),
			(neg|str_equals, s38, s39),
			(display_message, "@DEBUG (TRS): Rival '{s31}' {s32} [{reg31}] set to {reg32}.", gpu_debug),
		(try_end),
	]),
	
# script_qp2_trs_add_proficiency_to_rival
# PURPOSE: Attempts to raise the proficiency of a rival by a given amount altered by the level penalty.
("qp2_trs_add_proficiency_to_rival",
  [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":prof_gain", 2),
		
		# Switch out trp_player for the trade rival file for the player.
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(assign, ":troop_no", "trp_trade_rival_p"),
		(try_end),
		
		(try_begin),
			# Determine the current proficiency for the rival.
			(troop_get_slot, ":prof_current", ":troop_no", slot_rival_proficiency),
			# Determine the current level penalty for the rival.
			(store_div, ":penalty", ":prof_current", qp2_trs_proficiency_per_level_ratio), # prof / 100 = level
			(val_mul, ":penalty", qp2_trs_proficiency_penalty_per_level),
			# Determine amount of penalty.
			(store_mul, ":prof_penalty", ":prof_gain", ":penalty"),
			(val_max, ":prof_penalty", 1), # Prevent Div/0 errors.
			(val_div, ":prof_penalty", 100),
			# Determine final proficiency gain.
			(store_sub, ":prof_gain_actual", ":prof_gain", ":prof_penalty"),
			(val_max, ":prof_gain_actual", 1), # You are supposed to gain something at least.
			
			(call_script, "script_qp2_trs_change_value", ":troop_no", slot_rival_proficiency, ":prof_gain_actual"),
		(try_end),
	]),
	
# script_qp2_trs_determine_proficiency_gain
# PURPOSE: Based upon the quest reaction setting this will determine how much raw proficiency a rival should gain.
#          reg1 - Stores the proficiency gain for the winning rival.
#          reg2 - Stores the proficiency gain for other rivals.
("qp2_trs_determine_proficiency_gain",
  [
		(store_script_param, ":quest_no", 1),
		
		(assign, reg1, 0),
		(try_begin),
			(quest_get_slot, reg2, ":quest_no", slot_quest_proficiency_gain_low),
			(assign, reg1, reg2),
			(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
			(quest_get_slot, reg2, ":quest_no", slot_quest_proficiency_gain_medium),
			(val_add, reg1, reg2),
			(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
			(quest_get_slot, reg2, ":quest_no", slot_quest_proficiency_gain_high),
			(val_add, reg1, reg2),
		(try_end),
		
		(store_div, reg2, reg1, 10),
	]),
	
# script_qp2_alter_purchase_price_drift
# PURPOSE: Reduces the upward drift in prices when an item is bought in the giver center during a surplus quest.
("qp2_alter_purchase_price_drift",
  [
		(store_script_param, ":item_no", 1),

		(try_begin),
			(assign, ":pass", 0),
			(try_begin),
				##### QUEST: TRADE SURPLUS #####
				(check_quest_active, "qst_floris_trade_surplus"),
				(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_target_center, "$current_town"),
				(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_primary_commodity, ":item_no"),
				(this_or_next|quest_slot_eq, "qst_floris_trade_surplus", slot_quest_current_state, qp2_surplus_arrived_in_target_center),
				(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_current_state, qp2_surplus_picked_up_commodity),
				(assign, ":pass", 1),
			(else_try),
				##### QUEST: FORTUNE FAVORS THE BOLD ##### @ Primary Center
				(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_center, "$current_town"),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_primary_commodity, ":item_no"),
				(this_or_next|quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_primary_center),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_primary_town),
				(assign, ":pass", 1),
			(else_try),
				##### QUEST: FORTUNE FAVORS THE BOLD ##### @ Secondary Center
				(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, "$current_town"),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_secondary_commodity, ":item_no"),
				(this_or_next|quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_second_center),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_second_town),
				(assign, ":pass", 1),
			(try_end),
			(eq, ":pass", 1), # Pass condition.
			(is_between, ":item_no", qp2_trade_goods_begin, trade_goods_end),
			(store_sub, ":item_slot_no", ":item_no", qp2_trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(party_get_slot, reg21, "$g_encountered_party", ":item_slot_no"),
			(val_add, reg21, 20),
			(ge, DEBUG_QUEST_PACK_2, 2),
			(display_message, "@DEBUG (QP2): Purchase price drift reduced due to active quest.", gpu_debug),
		(try_end),
			
		# (store_troop_gold, reg51, "trp_player"),
		# (store_sub, reg52, reg50, reg51), # negative value indicates buying from merchant.
		# (try_begin),
			# (ge, reg52, 0),
			# (display_message, "@You have received {reg52} denars on your sales."),
		# (else_try),
			# (lt, reg52, 0),
			# (display_message, "@You have spent {reg52} denars on your purchase."),
		# (try_end),
	]),
	
# script_qp2_alter_sale_price_drift
# PURPOSE: Reduces the upward drift in prices when an item is sold to the target center during a shortage quest.
("qp2_alter_sale_price_drift",
  [
		(store_script_param, ":item_no", 1),
		
		(try_begin),
			(assign, ":pass", 0),
			(try_begin),
				##### QUEST: TRADE SHORTAGE #####
				(check_quest_active, "qst_floris_trade_shortage"),
				(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_target_center, "$current_town"),
				(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_primary_commodity, ":item_no"),
				(this_or_next|quest_slot_eq, "qst_floris_trade_shortage", slot_quest_current_state, qp2_shortage_arrived_in_target_center),
				(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_current_state, qp2_shortage_sold_items_to_town),
				(assign, ":pass", 1),
			(else_try),
				##### QUEST: FORTUNE FAVORS THE BOLD ##### @ Primary Center
				(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_center, "$current_town"),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_primary_commodity, ":item_no"),
				(this_or_next|quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_primary_center),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_primary_town),
				(assign, ":pass", 1),
			(else_try),
				##### QUEST: FORTUNE FAVORS THE BOLD ##### @ Secondary Center
				(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, "$current_town"),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_secondary_commodity, ":item_no"),
				(this_or_next|quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_arrived_in_second_center),
				(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_current_state, qp2_fortune_purchased_commodity_in_second_town),
				(assign, ":pass", 1),
			(try_end),
			(eq, ":pass", 1), # Pass condition.
			(is_between, ":item_no", qp2_trade_goods_begin, trade_goods_end),
			(store_sub, ":item_slot_no", ":item_no", qp2_trade_goods_begin),
			(val_sub, ":item_slot_no", slot_town_trade_good_prices_begin),
			(party_get_slot, reg21, "$g_encountered_party", ":item_slot_no"),
			(val_add, reg21, 20),
			(ge, DEBUG_QUEST_PACK_2, 2),
			(display_message, "@DEBUG (QP2): Sale price drift reduced due to shortage quest active.", gpu_debug),
		(try_end),
		# (store_troop_gold, reg51, "trp_player"),
		# (store_sub, reg52, reg50, reg51), # negative value indicates buying from merchant.
		# (try_begin),
			# (ge, reg52, 0),
			# (display_message, "@You have received {reg52} denars on your sales."),
		# (else_try),
			# (lt, reg52, 0),
			# (display_message, "@You have spent {reg52} denars on your purchase."),
		# (try_end),
	]),
	
# script_qp2_spawn_bandit_party
# PURPOSE: Spawn a bandit party near the player's location, populate it with a level scaled number of bandits and attack the player.
# Bandit Party Size = [ (LEVEL/6)+3 ] * [ range (LEVEL/8)+1 to (LEVEL/3)+2 ]
# Character level   	= 	1	5	10	15	20	25	30	35	40	
# Average party size 	=	3	4	12	20	30	45	60	68	90
("qp2_spawn_bandit_party",
    [
		(set_spawn_radius, 2),
        (spawn_around_party, "p_main_party", "pt_raider_party"),
        (assign, ":bandit_party", reg0),
        (party_set_slot, ":bandit_party", slot_party_commander_party, -1), #we need this because 0 is player's party!
        (party_set_faction, ":bandit_party", "fac_outlaws"),
        (party_set_ai_behavior, ":bandit_party", ai_bhvr_attack_party),
        (party_clear, ":bandit_party"),
		(store_character_level, ":level", "trp_player"),
		(store_div, ":upper_limit", ":level", 3), # Upper = level/3 + 2
		(val_add, ":upper_limit", 2),
		(store_div, ":lower_limit", ":level", 8),
		(val_add, ":lower_limit", 1),
		(store_div, ":number_of_rolls", ":level", 6),
		(val_add, ":number_of_rolls", 3),
		(assign, ":bandit_count", 0),
		(try_for_range, ":unused", 0, ":number_of_rolls"), # [ (LEVEL/6)+3 ] * [ range (LEVEL/8)+1 to (LEVEL/3)+2 ]
			(store_random_in_range, ":roll", ":lower_limit", ":upper_limit"),
			(val_add, ":bandit_count", ":roll"),
		(try_end),
		(party_add_members, ":bandit_party", qp2_fortune_bandit_troop, ":bandit_count"),
		(quest_set_slot, "qst_floris_trade_fortune_favors_bold", slot_quest_target_party, ":bandit_party"),
    ]),
	
# script_cf_qp2_parties_that_wont_join_battles
# PURPOSE: The following parties will be ignored when directed to join a nearby battle.
("cf_qp2_parties_that_wont_join_battles",
  [
		(store_script_param, ":party_no", 1),
		
		# QUEST: Fortune Favors the Bold
		(this_or_next|neg|check_quest_active, "qst_floris_trade_fortune_favors_bold"),
		(neg|quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_party, ":party_no"), ##
		
		# Merchant Rivals in the field
		(party_stack_get_troop_id, ":troop_no", ":party_no", 0),
		(neg|is_between, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
		
	]),
	
# script_qp2_trs_initialize_rival
# PURPOSE: Sets the initial values for a trade rival.
("qp2_trs_initialize_rival",
  [
		(store_script_param, ":troop_no", 1),
		
		# Create Name
		# Activate status.
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_status,  1),
		# Reset Proficiency
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_proficiency,  qp2_trs_proficiency_per_level_ratio),
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_trade_skill,  50),
		# Generate home town & faction
		(store_random_in_range, ":center_no", centers_begin, centers_end),
		(store_faction_of_party, ":faction_home", ":center_no"),
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_home_region, ":faction_home"),
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_location, ":center_no"),
		# Set initial location and set destination.
		(party_get_position, pos1, ":center_no"),
		(position_get_x, ":x_pos", pos1),
		(position_get_y, ":y_pos", pos1),
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_x_loc, ":x_pos"),
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_y_loc, ":y_pos"),
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_destination, ":center_no"),
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_destination_set, 0),
		# Reset wealth
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_current_wealth, 2000),
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_accumulated_wealth, 2000),
		# Set relations with factions
		(try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
			(store_relation, ":relation", ":faction_home", ":faction_no"),
			(try_begin),
				(lt, ":relation", 0),
				(val_div, ":relation", 2),
			(try_end),
			(store_random_in_range, ":random_bonus", -5, 6),
			(val_add, ":relation", ":random_bonus"),
			(store_sub, ":faction_slot", ":faction_no", kingdoms_begin),
			(val_add, ":faction_slot", slot_rival_relation_fac_player),
			(call_script, "script_qp2_trs_set_value", ":troop_no", ":faction_slot", ":relation"),
		(try_end),
		# Set relations with individuals
		(try_for_range, ":relation_slot", slot_rival_relation_player, slot_rival_individual_relations_end),
			(store_random_in_range, ":relation", -5, 6),
			(call_script, "script_qp2_trs_set_value", ":troop_no", ":relation_slot", ":relation"),
		(try_end),
	]),
	
# script_qp2_trs_rival_town_functions
# PURPOSE: Checks if there is any business for the rival to attend to in town.
("qp2_trs_rival_town_functions",
    [
	    (store_script_param, ":troop_no", 1),
		
		(troop_get_slot, ":center_no", ":troop_no", slot_rival_location),
		(troop_get_slot, ":proficiency", ":troop_no", slot_rival_proficiency),
		(try_begin),
			(is_between, ":center_no", centers_begin, centers_end),
			(troop_slot_eq, ":troop_no", slot_rival_status, qp2_rival_status_active),
			
			### QUEST: TRADE SHORTAGE ###
			(try_begin),
				(troop_slot_eq, ":troop_no", slot_rival_quest_shortage_status, 1), # Quest is active.
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_rival_quest_shortage_stage, qp2_shortage_arrived_in_target_center),
					(quest_slot_eq, "qst_floris_trade_shortage", slot_quest_target_center, ":center_no"),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_quest_shortage_stage, qp2_shortage_sold_items_to_town),
				(try_end),
			(try_end),
			
			### QUEST: TRADE SURPLUS ###
			(try_begin),
				(troop_slot_eq, ":troop_no", slot_rival_quest_surplus_status, 1), # Quest is active.
				(try_begin),
					(troop_slot_eq, ":troop_no", slot_rival_quest_surplus_stage, qp2_surplus_arrived_in_target_center),
					(quest_slot_eq, "qst_floris_trade_surplus", slot_quest_target_center, ":center_no"),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_quest_surplus_stage, qp2_surplus_picked_up_commodity),
				(try_end),
			(try_end),
			
			### QUEST: FORTUNE FAVORS THE BOLD ###
			(try_begin),
				(troop_slot_eq, ":troop_no", slot_rival_quest_fortune_status, 1), # Quest is active.
				(try_begin), # Primary Center
					(troop_slot_eq, ":troop_no", slot_rival_quest_fortune_stage, qp2_fortune_arrived_in_primary_center),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_center, ":center_no"),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_quest_fortune_stage, qp2_fortune_purchased_commodity_in_primary_town),
					# Send the rival towards the next town.
					(quest_get_slot, ":destination", "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_destination, ":destination"),
					(call_script, "script_qp2_trs_change_value", ":troop_no", slot_rival_quest_fortune_cycle_count, 1),
					# Check if rival finished the quest.
					(try_begin),
						(troop_slot_ge, ":troop_no", slot_rival_quest_fortune_cycle_count, 4),
						(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_quest_fortune_stage, qp2_fortune_completed_route),
						(call_script, "script_qp2_trs_record_victory_for_rival", "qst_floris_trade_fortune_favors_bold", ":troop_no"), # Rival wins, player fails.
					(try_end),
				(else_try), # Secondary Center
					(troop_slot_eq, ":troop_no", slot_rival_quest_fortune_stage, qp2_fortune_arrived_in_second_center),
					(quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center, ":center_no"),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_quest_fortune_stage, qp2_fortune_purchased_commodity_in_second_town),
					# Send the rival towards the next town.
					(quest_get_slot, ":destination", "qst_floris_trade_fortune_favors_bold", slot_quest_target_center),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_destination, ":destination"),
				(try_end),
			(try_end),
			
			# Rival does random business based upon his proficiency.
			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(store_random_in_range, ":profit", -250, 500),
				(store_div, ":proficiency_bonus", ":proficiency", 8),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(store_random_in_range, ":profit", -175, 350),
				(store_div, ":proficiency_bonus", ":proficiency", 14),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
				(store_random_in_range, ":profit", -50, 120),
				(store_div, ":proficiency_bonus", ":proficiency", 25),
			(try_end),
			(val_add, ":profit", ":proficiency_bonus"),
			(val_clamp, ":profit", -500, 2000),
			(call_script, "script_qp2_trs_change_value", ":troop_no", slot_rival_current_wealth, ":profit"),
			(call_script, "script_qp2_trs_change_value", ":troop_no", slot_rival_accumulated_wealth, ":profit"),
			
			# Random chance rival's relation with the faction improves.
			(try_begin),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", 40),
				(store_faction_of_party, ":faction_no", ":center_no"),
				(store_sub, ":faction_slot", ":faction_no", kingdoms_begin),
				(val_add, ":faction_slot", trs_obj_rival_relation_fac_player),
				(call_script, "script_qp2_trs_set_value", ":troop_no", ":faction_slot", 1),
			(try_end),
			
			# Random chance rival's proficency improves by 2.
			(try_begin),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", 15),
				(call_script, "script_qp2_trs_add_proficiency_to_rival", ":troop_no", 2),
			(try_end),
		(try_end),
		
		# Reset our destination locking slot.
		(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_destination_set, 0), # So this rival will pick a new direction.
    ]),
	
# script_cf_qp2_rival_has_no_quest
# PURPOSE: Ensures the specified rival has no active trade quest.
("cf_qp2_rival_has_no_quest",
    [
	    (store_script_param, ":troop_no", 1),
		
		(is_between, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
		(troop_slot_eq, ":troop_no", slot_rival_quest_shortage_status, 0),
		(troop_slot_eq, ":troop_no", slot_rival_quest_surplus_status, 0),
		# Trade Bargain quest is N/A.
		(troop_slot_eq, ":troop_no", slot_rival_quest_fortune_status, 0),
    ]),
	
# script_qp2_determine_most_profitable_enterprise_for_center
# PURPOSE: Finds the most profitable enterprise for a center based upon center cost vs. weekly profit, but under a given price limit.
("qp2_determine_most_profitable_enterprise_for_center",
    [
	    (store_script_param, ":center_no", 1),
		(store_script_param, ":price_limit", 2),
		
		(assign, ":array", "trp_temp_array_a"),
		## Floris Naming Difference+ ##
		(troop_set_slot, ":array", 1, "itm_bread"),
		(troop_set_slot, ":array", 2, "itm_ale"),
		(troop_set_slot, ":array", 3, "itm_leatherwork"),
		(troop_set_slot, ":array", 4, "itm_wine"),
		(troop_set_slot, ":array", 5, "itm_oil"),
		(troop_set_slot, ":array", 6, "itm_tools"),
		(troop_set_slot, ":array", 7, "itm_velvet"),
		(troop_set_slot, ":array", 8, "itm_wool_cloth"),
		(troop_set_slot, ":array", 9, "itm_linen"),
		## Floris Naming Difference- ##
		
		(assign, ":best_return", 0),
		(assign, ":best_profit", 0),
		(assign, ":item_produced", -1),
		
		(try_for_range, ":slot", 1, 10),
			(troop_get_slot, ":item_no", ":array", ":slot"),
			# Determine cost of building the enterprise and that it is below our budget limit.
			(item_get_slot, ":building_cost", ":item_no", slot_item_enterprise_building_cost),
			(le, ":price_limit", ":building_cost"),
			
			# Calculate the weekly profit for the enterprise.
			(call_script, "script_process_player_enterprise", ":item_no", ":center_no"),
			(assign, ":weekly_profit", reg0), #reg0: Profit per cycle
			(ge, ":weekly_profit", 1),
			
			# Compare profit vs. cost for a return of investment rating.
			(store_div, ":return_rating", ":building_cost", ":weekly_profit"), # Lower rating # is better.
			
			# Store the best enterprise.
			(try_begin),
				(eq, ":return_rating", ":best_return"),
				(gt, ":weekly_profit", ":best_profit"),
				(assign, ":best_return", ":return_rating"),
				(assign, ":best_profit", ":weekly_profit"),
				(assign, ":item_produced", ":item_no"),
			(else_try),
				(lt, ":return_rating", ":best_return"),
				(assign, ":best_return", ":return_rating"),
				(assign, ":best_profit", ":weekly_profit"),
				(assign, ":item_produced", ":item_no"),
			(try_end),
			
			(ge, DEBUG_QUEST_PACK_2, 1),
			(call_script, "script_get_enterprise_name", ":item_no"),
			(str_store_string, s31, reg0),
			(str_store_item_name, s32, ":item_no"),
			(assign, reg31, ":return_rating"),
			(assign, reg32, ":weekly_profit"),
			(assign, reg33, ":building_cost"),
			(display_message, "@DEBUG (QP2): {s31} producing {s32}.  Rating [{reg31}] = {reg33} denars cost / {reg32} denars profit.", gpu_debug),
		(try_end),
		(assign, reg1, ":item_produced"),
    ]),
		
]

from util_wrappers import *
from util_scripts import *

scripts_directives = [
	# HOOK: Inserts the initializing scripts in game start as needed.
	[SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp2_game_start"),], 1],
	# HOOK: Inserts the names of quests I do not want humanitarian companions to object to failing.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"), 0, 
		[(call_script, "script_cf_qp2_ignore_failures", ":quest_no"),], 1],
	# HOOK: Changes the price of buying trade goods if appropriate based on the current quest.
	[SD_OP_BLOCK_INSERT, "game_get_item_buy_price_factor", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (store_add, ":penalty_factor", 100, ":trade_penalty"), 0, 
		[(call_script, "script_qp2_alter_item_price", "$g_encountered_party", ":item_kind_id", qp2_buying_an_item), (assign, ":trade_penalty", reg0),], 1],
	# HOOK: Changes the price of selling trade goods if appropriate based on the current quest.
	[SD_OP_BLOCK_INSERT, "game_get_item_sell_price_factor", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (store_add, ":penalty_divisor", 100, ":trade_penalty"), 0, 
		[(call_script, "script_qp2_alter_item_price", "$g_encountered_party", ":item_kind_id", qp2_selling_an_item), (assign, ":trade_penalty", reg0),], 1],
	# HOOK: Checks when an item is bought in game.
	[SD_OP_BLOCK_INSERT, "game_event_buy_item", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp2_track_when_items_are_bought", ":item_kind_id"),], 1],
	# HOOK: Checks when an item is sold in game.
	[SD_OP_BLOCK_INSERT, "game_event_sell_item", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp2_track_when_items_are_sold", ":item_kind_id"),], 1],
	# HOOK: Captures when a player enters town.
	[SD_OP_BLOCK_INSERT, "music_set_situation_with_culture", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (music_set_culture, ":culture"), 0, 
		[(call_script, "script_qp2_track_town_entry", "$g_encountered_party"),], 1],
	# HOOK: Checks when an item is bought in game and limits the drift in price during a surplus.
	[SD_OP_BLOCK_INSERT, "game_event_buy_item", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (val_min, ":multiplier", maximum_price_factor), 0, 
		[(assign, reg21, ":multiplier"), (call_script, "script_qp2_alter_purchase_price_drift", ":item_kind_id"), (assign, ":multiplier", reg21),], 1],
	# HOOK: Checks when an item is sold in game and limits the drift in price during a shortage.
	[SD_OP_BLOCK_INSERT, "game_event_sell_item", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (val_max, ":multiplier", minimum_price_factor), 0, 
		[(assign, reg21, ":multiplier"), (call_script, "script_qp2_alter_sale_price_drift", ":item_kind_id"), (assign, ":multiplier", reg21),], 1],
	# HOOK: Prevent spawned bandits from joining nearby battles.
	[SD_OP_BLOCK_INSERT, "let_nearby_parties_join_current_battle", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (neg|quest_slot_eq, "qst_troublesome_bandits", slot_quest_target_party, ":party_no"), 0, 
		[(call_script, "script_cf_qp2_parties_that_wont_join_battles", ":party_no"),], 1],
	# HOOK: Insert failure condition checks for quests that need them.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (try_begin), 0, 
		[(call_script, "script_qp2_check_failure_conditions", ":quest_no"),], 1],
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