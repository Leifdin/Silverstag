# Quest Pack 2 (1.0) by Windyplains

from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from module_quests import *
from module_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################



simple_triggers = [
	
	# QUEST PULSE (DAILY): 
	(24,
		[
			## QUEST: A Noble Opportunity ##
			(try_begin),
				(check_quest_active, "qst_trade_noble_opportunity"),
				(quest_slot_eq, "qst_trade_noble_opportunity", slot_quest_current_state, qp2_opportunity_provided_loan),
				(call_script, "script_common_quest_change_slot", "qst_trade_noble_opportunity", slot_quest_days_remaining_for_repayment, -1),
				(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_update),
				# Determine if payment wait period is up and if so figure out if the lord can repay the player.
				(try_begin),
					(quest_slot_ge, "qst_trade_noble_opportunity", slot_quest_days_remaining_for_repayment, 1), # <= 0 days
					(quest_get_slot, ":failure_chance", "qst_trade_noble_opportunity", slot_quest_payment_failure_chance),
					(store_sub, ":success_threshold", 100, ":failure_chance"),
					(store_random_in_range, ":roll", 0, 100),
					(try_begin),
						(lt, ":roll", ":success_threshold"), # Lord will repay.
						(call_script, "script_common_quest_change_slot", "qst_trade_noble_opportunity", slot_quest_lord_will_repay_loan, 1),
					(try_end),
					(call_script, "script_common_quest_change_state", "qst_trade_noble_opportunity", qp2_opportunity_lord_ready_to_repay),
					# Notify player via popup message.
					(quest_get_slot, ":troop_no", "qst_trade_noble_opportunity", slot_quest_giver_troop),
					(str_store_troop_name, s21, ":troop_no"),
					(quest_get_slot, ":center_no", "qst_trade_noble_opportunity", slot_quest_target_center),
					(str_store_party_name, s22, ":center_no"),
					(dialog_box, "@A folded letter bearing the seal of {s21} has arrived.^^'I wish to speak with you the next time you are in the vicinity of {s22} regarding our financial arrangement.'", "@A Messenger Arrives"),
					(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_update),
				(try_end),
			(try_end),
			
			## TRADE RIVAL: Daily upgrade of each active trade rival's proficiency.
			(try_for_range, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
				(troop_slot_eq, ":troop_no", slot_rival_status, qp2_rival_status_active),
				(call_script, "script_qp2_trs_add_proficiency_to_rival", ":troop_no", qp2_trs_proficiency_gain_per_day),
			(try_end),
		]
	),
	
	# QUEST PULSE (4 HOURS): 
	(4,
		[
			## QUEST: Fortune Favors the Bold ##
			(try_begin),
				(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
				(quest_get_slot, ":party_no", "qst_floris_trade_fortune_favors_bold", slot_quest_target_party),
				(neg|party_is_active, ":party_no"),
				(call_script, "script_qp2_spawn_bandit_party"),
			(try_end),
		]
	),
	
	# TRIGGER: Rival Movement AI
	# Goal #1 - Move the Rival's towards their destination.
	# Goal #2 - If no quest is active then choose a new destination to travel to so they can generate money via trading.
	(3,
		[
			# Daily upgrade of each active trade rival's proficiency.
			(try_for_range, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
				(troop_slot_eq, ":troop_no", slot_rival_status, qp2_rival_status_active),
				(troop_get_slot, ":x_loc", ":troop_no", slot_rival_x_loc),
				(troop_get_slot, ":y_loc", ":troop_no", slot_rival_y_loc),
				(troop_get_slot, ":destination", ":troop_no", slot_rival_destination),
				(party_get_position, pos1, ":destination"),
				(position_get_x, ":dest_x", pos1),
				(position_get_y, ":dest_y", pos1),
				(store_sub, ":diff_x", ":dest_x", ":x_loc"),
				(store_sub, ":diff_y", ":dest_y", ":y_loc"),
				(store_random_in_range, ":random_movement", 0, 75),
				(troop_get_slot, ":proficiency", ":troop_no", slot_rival_proficiency),
				(store_div, ":upper_limit", ":proficiency", 4),
				(store_div, ":lower_limit", ":proficiency", 10),
				(try_for_range, ":unused", 0, 4),
					(store_random_in_range, ":roll", ":lower_limit", ":upper_limit"),
					(val_add, ":random_movement", ":roll"),
				(try_end),
				# Update X position.
				(try_begin),
					(ge, ":diff_x", 0),
					(ge, ":diff_x", 100),
					(val_add, ":x_loc", 100),
					(val_add, ":x_loc", ":random_movement"),
					(val_min, ":x_loc", ":dest_x"),
				(else_try),
					(ge, ":diff_x", 0),
					(assign, ":x_loc", ":dest_x"),
				(else_try),
					(lt, ":diff_x", 0),
					(val_sub, ":x_loc", 100),
					(val_sub, ":x_loc", ":random_movement"),
					(val_max, ":x_loc", ":dest_x"),
				(try_end),
				# Update Y position.
				(try_begin),
					(ge, ":diff_y", 0),
					(ge, ":diff_y", 100),
					(val_add, ":y_loc", 100),
					(val_add, ":y_loc", ":random_movement"),
					(val_min, ":y_loc", ":dest_y"),
				(else_try),
					(ge, ":diff_y", 0),
					(assign, ":y_loc", ":dest_y"),
				(else_try),
					(lt, ":diff_y", 0),
					(val_sub, ":y_loc", 100),
					(val_sub, ":y_loc", ":random_movement"),
					(val_max, ":y_loc", ":dest_y"),
				(try_end),
				# See if you're close enough as is.
				(position_set_x, pos2, ":x_loc"),
				(position_set_y, pos2, ":y_loc"),
				(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
				(try_begin),
					(lt, ":distance", 3),
					(neg|troop_slot_eq, ":troop_no", slot_rival_location, ":destination"),
					(assign, ":x_loc", ":dest_x"),
					(assign, ":y_loc", ":dest_y"),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_location, ":destination"),
					(call_script, "script_qp2_trs_rival_town_functions", ":troop_no"),
					(ge, DEBUG_QUEST_PACK_2, 1),
					(str_store_party_name, s31, ":destination"),
					(str_store_troop_name, s32, ":troop_no"),
					(display_message, "@DEBUG (TRS): {s32} has arrived at {s31}.", gpu_debug),
				(try_end),
				(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_x_loc, ":x_loc"),
				(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_y_loc, ":y_loc"),
				
				### DIAGNOSTIC ###
				(ge, DEBUG_QUEST_PACK_2, 1),
				(str_store_troop_name, s31, ":troop_no"),
				(assign, reg31, ":x_loc"),
				(assign, reg32, ":y_loc"),
				(str_store_party_name, s32, ":destination"),
				(party_get_position, pos1, ":destination"),
				(assign, ":closest_center", -1),
				(assign, ":closest_distance", 10000),
				(try_for_range, ":center_no", centers_begin, centers_end),
					(position_set_x, pos2, ":x_loc"),
					(position_set_y, pos2, ":y_loc"),
					(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
					(lt, ":distance", ":closest_distance"),
					(assign, ":closest_center", ":center_no"),
					(assign, ":closest_distance", ":distance"),
				(try_end),
				(str_store_party_name, s33, ":closest_center"),
				(assign, reg33, ":closest_distance"),
				(display_message, "@DEBUG (TRS): {s31} is headed to {s32}.  Location @ ({reg31},{reg32}) nearest {s33} by {reg33}m.", gpu_debug),
			(try_end),
			
			(try_for_range, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
				(troop_slot_eq, ":troop_no", slot_rival_status, qp2_rival_status_active),
				(call_script, "script_cf_qp2_rival_has_no_quest", ":troop_no"),
				(troop_slot_eq, ":troop_no", slot_rival_destination_set, 0),
				# Choose a random center a given distance away.
				(store_sub, ":upper_limit", centers_end, 5),
				(store_random_in_range, ":seed", centers_begin, ":upper_limit"),
				(try_for_range, ":center_no", ":seed", centers_end),
					(troop_get_slot, ":current_center", ":troop_no", slot_rival_location),
					(store_distance_to_party_from_party, ":distance", ":current_center", ":center_no"),
					(lt, ":distance", 25),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_destination, ":center_no"),
					(call_script, "script_qp2_trs_set_value", ":troop_no", slot_rival_destination_set, 1), # So we won't keep picking centers.
					(break_loop),
				(try_end),
			(try_end),
		]
	),
	
	# TRIGGER: AI Quest Progress
	# Check for active quest on each rival.
	# If a quest is active -> check to upgrade quest stage (progress).
	# If a quest failed to update -> improve trigger chance slightly.
	(3,
		[
			(try_for_range, ":quest_no", qp2_quests_begin, qp2_quests_end),
				(check_quest_active, ":quest_no"),
				
				# Insert blocks to prevent quests not using the rival system from getting through.
				# (neq, ":quest_no", "qst_trade_bargain"), # Doesn't exist yet.
					
				# Determine slot for value that sets if a rival is participating in the quest or not.
				(store_sub, ":quest_offset", ":quest_no", qp2_quests_begin),
				(val_mul, ":quest_offset", 10),
				(store_add, ":slot_rival_quest_status", ":quest_offset", slot_rival_quest_shortage_status),
				
				# Determine slot # for value that stores the rival's current progress in the quest.
				(store_sub, ":slot_offset", slot_rival_quest_shortage_stage, slot_rival_quest_shortage_status),
				(store_add, ":slot_rival_quest_stage", ":slot_rival_quest_status", ":slot_offset"),
				
				# Determine slot # for value that stores the rival's chance of upgrading status.
				(store_sub, ":slot_offset", slot_rival_quest_shortage_trigger_chance, slot_rival_quest_shortage_status),
				(store_add, ":slot_rival_trigger_chance", ":slot_rival_quest_status", ":slot_offset"),
				
				# Cycle through all of the rivals.
				(try_for_range, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
					(troop_slot_eq, ":troop_no", slot_rival_status, qp2_rival_status_active),          # Rival is active.
					(troop_slot_eq, ":troop_no", ":slot_rival_quest_status", qp2_rival_status_active), # Rival is participating in this quest.
					(troop_get_slot, ":trigger_chance", ":troop_no", ":slot_rival_trigger_chance"),
					(store_random_in_range, ":chance", 0, 100),
					(try_begin),
						(lt, ":chance", ":trigger_chance"),
						(call_script, "script_qp2_trs_change_value", ":troop_no", ":slot_rival_quest_stage", 1),
						# Debug notification
						(try_begin),
							(ge, DEBUG_QUEST_PACK_2, 1),
							(quest_get_slot, reg1, ":quest_no", slot_quest_unique_name),
							(str_store_string, s31, reg1),
							(str_store_troop_name, s32, ":troop_no"),
							(troop_get_slot, reg31, ":troop_no", ":slot_rival_quest_stage"),
							(display_message, "@DEBUG (TRS): Rival '{s32}' has upgraded quest '{s31}' to stage {reg31}.", gpu_debug),
						(try_end),
						# Check if the rival just won.
						(troop_get_slot, ":stage_current", ":troop_no", ":slot_rival_quest_stage"),
						(quest_get_slot, ":stage_final",   ":quest_no", slot_quest_final_stage),
						(try_begin),
							(eq, ":stage_current", ":stage_final"),
							(call_script, "script_qp2_trs_record_victory_for_rival", ":quest_no", ":troop_no"), # Rival wins, player fails.
						(else_try),
							# else -> figure out new trigger chance.
							(troop_get_slot, ":stage", ":troop_no", ":slot_rival_quest_stage"),
							(store_add, ":slot_quest_trigger", ":stage", slot_quest_stage_1_trigger_chance),
							(val_sub, ":slot_quest_trigger", 1),
							(quest_get_slot, ":trigger_chance", ":quest_no", ":slot_quest_trigger"),
							(call_script, "script_qp2_trs_set_value", ":troop_no", ":slot_rival_trigger_chance", ":trigger_chance"),
						(try_end),
					(else_try),
						# Improve the trigger chance.
						(ge, ":trigger_chance", 1), # I don't want it improving if I set it to 0 intentionally in the quest script.
						(call_script, "script_qp2_trs_change_value", ":troop_no", ":slot_rival_trigger_chance", 2),
					(try_end),
				(try_end),
				
			(try_end),
		]
	),
	
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