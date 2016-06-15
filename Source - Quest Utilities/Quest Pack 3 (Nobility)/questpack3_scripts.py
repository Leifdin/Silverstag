# Quest Pack 3 (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_triggers import *
from module_quests import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contains the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [
##############################################################################################################################################
############                                                COMMON QUEST SCRIPTS                                                   ###########
##############################################################################################################################################

# # script_qp3_start_quest
# # INPUT: arg1 = quest_no, arg2 = giver_troop_no, s2 = description_text
# # OUTPUT: none
# ("qp3_start_quest",
  # [(store_script_param, ":quest_no", 1),
	# (store_script_param, ":giver_troop_no", 2),
	
	# #(quest_set_slot, ":quest_no", slot_quest_giver_troop, ":giver_troop_no"),
	
	# (try_begin),
	  # (eq, ":giver_troop_no", -1),
	  # (str_store_string, s63, "str_qp3_quest_title"),
	# (else_try),
	  # (is_between, ":giver_troop_no", active_npcs_begin, active_npcs_end),
	  # (str_store_troop_name_link, s62, ":giver_troop_no"),
	  # (str_store_string, s63, "@Given by: {s62}"),
	# (else_try),
	  # (str_store_troop_name, s62, ":giver_troop_no"),
	  # (str_store_string, s63, "@Given by: {s62}"),
	# (try_end),
	# (store_current_hours, ":cur_hours"),
	# (str_store_date, s60, ":cur_hours"),
	# (str_store_string, s60, "@Given on: {s60}"),
	# (add_quest_note_from_sreg, ":quest_no", 0, s60, 0),
	# (add_quest_note_from_sreg, ":quest_no", 1, s63, 0),
	# (add_quest_note_from_sreg, ":quest_no", 2, s61, 0),
	
	# (try_begin),
	  # (quest_slot_ge, ":quest_no", slot_quest_expiration_days, 1),
	  # (quest_get_slot, reg20, ":quest_no", slot_quest_expiration_days),
	  # (add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg20} days to finish this quest.", 0),
	# (try_end),
	
	# (start_quest, ":quest_no", ":giver_troop_no"),
	
	# (display_message, "str_quest_log_updated"),
	# ]),
	
# script_cf_qp3_ignore_failures
# These quests are not intended to trigger humanitarian companions complaining so they are added to the module_scripts exception list.
("cf_qp3_ignore_failures",
  [
		(store_script_param, ":quest_no", 1),
		
		(neq, ":quest_no", "qst_summoned_to_hall"),
		# (neq, ":quest_no", "qst_patrol_for_bandits"), # Nah, they should get mad about this one.
		(neq, ":quest_no", "qst_mercs_for_hire"),
		# (neq, ":quest_no", "qst_destroy_the_lair"), # Nah, they should get mad about this one.
		# (neq, ":quest_no", "qst_escort_to_mine"), # Nah, they should get mad about this one.
	]),
	
# script_qp3_track_town_entry
# Any functions that should occur upon town entry should happen here.
("qp3_track_town_entry",
  [
		#(store_script_param, ":center_no", 1),
		
		# Mercenary parties should attempt to sell prisoners and find new recruits.
		(try_begin),
			(check_quest_active, "qst_mercs_for_hire"),
			(quest_get_slot, ":merc_party", "qst_mercs_for_hire", slot_quest_target_party),
			(party_is_active, ":merc_party"),
			(call_script, "script_qp3_quest_mercenary_function", mercs_sell_prisoners),
			# (call_script, "script_qp3_quest_mercenary_function", mercs_recruit_troops), # Disabled because they're constantly hiring a full party at the moment.
		(try_end),
	]),
	
# script_qp3_check_failure_conditions
# Check if any quests should have failed from "script_abort_quest" due to expiration.  Messages are disabled if one of these quests trigger and are automatically re-enabled further down.
# This is to prevent multiple "Quest Failed" messages showing up.
# INPUT: none
# OUTPUT: none
("qp3_check_failure_conditions",
  [
		(store_script_param, ":quest_no", 1),
		
		(try_begin),
			(eq, ":quest_no", "qst_summoned_to_hall"),
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_fail),
			(set_show_messages, 0),
		(else_try),
			(eq, ":quest_no", "qst_patrol_for_bandits"),
			(call_script, "script_qp3_quest_patrol_for_bandits", floris_quest_fail),
			(set_show_messages, 0),
		(else_try),
			(eq, ":quest_no", "qst_mercs_for_hire"),
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_fail),
			(set_show_messages, 0),
		(else_try),
			(eq, ":quest_no", "qst_destroy_the_lair"),
			(call_script, "script_qp3_quest_destroy_the_lair", floris_quest_fail),
			(set_show_messages, 0),
		(else_try),
			## QUEST [ qst_escort_to_mine ] ##
			(eq, ":quest_no", "qst_escort_to_mine"),
			(call_script, "script_qp3_quest_escort_to_mine", floris_quest_fail),
		(try_end),
		
	]),
	
# script_cf_qp3_debug_initiate_quest
# Allows a debugging menu to manually initiate any quest from this quest pack.
# This is to prevent multiple "Quest Failed" messages showing up.
# INPUT: quest_no
# OUTPUT: none
("cf_qp3_debug_initiate_quest",
  [
		(store_script_param, ":quest_no", 1),
		(change_screen_map),
		(call_script, "script_cf_qus_player_owns_walled_center"),
		(quest_set_slot, "qst_summoned_to_hall", slot_quest_giver_center, reg1),
		(assign, "$current_town", reg1),
			
		(try_begin),
			## QUEST [ qst_summoned_to_hall ] ##
			(eq, ":quest_no", "qst_summoned_to_hall"),
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_begin),
		(else_try),
			## QUEST [ qst_patrol_for_bandits ] ##
			(eq, ":quest_no", "qst_patrol_for_bandits"),
			(call_script, "script_qp3_quest_patrol_for_bandits", floris_quest_begin),
		(else_try),
			## QUEST [ qst_mercs_for_hire ] ##
			(eq, ":quest_no", "qst_mercs_for_hire"),
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_begin),
		(else_try),
			## QUEST [ qst_destroy_the_lair ] ##
			(eq, ":quest_no", "qst_destroy_the_lair"),
			(store_add, ":bandit_templates_end", "pt_sea_raiders", 1),
			(assign, ":closest_template", -1),
			(try_for_range, ":bandit_template", "pt_steppe_bandits", ":bandit_templates_end"),
				(eq, ":closest_template", -1),
				(party_template_get_slot, ":bandit_lair", ":bandit_template", slot_party_template_lair_party),
				(call_script, "script_cf_qus_party_close_to_center", "$current_town", ":bandit_lair", 25),
				(assign, ":closest_template", ":bandit_template"),
			(try_end),
			(neq, ":closest_template", -1),
			(party_template_get_slot, ":bandit_lair", ":closest_template", slot_party_template_lair_party),
			(quest_set_slot, ":quest_no", slot_quest_target_party, ":bandit_lair"),
			(call_script, "script_qp3_quest_destroy_the_lair", floris_quest_begin),
		(else_try),
			## QUEST [ qst_escort_to_mine ] ##
			(eq, ":quest_no", "qst_escort_to_mine"),
			(call_script, "script_qp3_quest_escort_to_mine", floris_quest_begin),
		(else_try),
			## DEFAULT ERROR ##
			(str_store_quest_name, s21, ":quest_no"),
			(display_message, "@Manual quest intiation of quest '{s21}' failed."),
		(try_end),
	]),
	
# script_qp3_debug_abort_quest
# Allows a debugging menu to manually fail any quest from this quest pack.
# This is to prevent multiple "Quest Failed" messages showing up.
# INPUT: quest_no
# OUTPUT: none
("qp3_debug_abort_quest",
  [
		(store_script_param, ":quest_no", 1),
		
		(change_screen_map),
		(try_begin),
			(eq, ":quest_no", "qst_summoned_to_hall"),
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_fail),
		(else_try),
			(eq, ":quest_no", "qst_patrol_for_bandits"),
			(call_script, "script_qp3_quest_patrol_for_bandits", floris_quest_fail),
		(else_try),
			(eq, ":quest_no", "qst_mercs_for_hire"),
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_fail),
		(else_try),
			(eq, ":quest_no", "qst_destroy_the_lair"),
			(call_script, "script_qp3_quest_destroy_the_lair", floris_quest_fail),
		(else_try),
			(eq, ":quest_no", "qst_escort_to_mine"),
			(call_script, "script_qp3_quest_escort_to_mine", floris_quest_fail),
		(else_try),
			## DEFAULT ERROR ##
			(str_store_quest_name, s21, ":quest_no"),
			(display_message, "@Manual quest abort of quest '{s21}' failed."),
		(try_end),
	]),
	
# script_qp3_enter_court
# Injects characters into your castle hall as needed.
# INPUT: none
# OUTPUT: none
("qp3_enter_court",
  [
		#(store_script_param, ":center_no", 1),
		(store_script_param, ":cur_pos",   2),
		
		### CASTLE STEWARD ###
		# (try_begin),
			# (check_quest_active, "qst_summoned_to_hall"),
			# (set_visitor, ":cur_pos", qp3_actor_minister),
			# (val_add,":cur_pos", 1),
		# (else_try),
			# (check_quest_active, "qst_mercs_for_hire"),
			# (quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_begun),
			# (set_visitor, ":cur_pos", qp3_actor_minister),
			# (val_add,":cur_pos", 1),
		# (try_end),
		
		### MERCENARY LEADER ###
		(try_begin),
			(check_quest_active, "qst_mercs_for_hire"),
			(set_visitor, ":cur_pos", qp3_actor_mercenary_leader),
			(val_add,":cur_pos", 1),
		(try_end),
		
		(assign, reg1, ":cur_pos"),
	]),

# script_qp3_game_start
# Contains all initialization scripts needed for Quest Pack 3.
# INPUT:  none
# OUTPUT: none
("qp3_game_start",
  [
		# (call_script, "script_give_center_to_lord", "p_town_16",  "trp_player", 0),
		# (call_script, "script_give_center_to_lord", "p_castle_20",  "trp_player", 0),
		# (call_script, "script_give_center_to_lord", "p_castle_26",  "trp_player", 0),
		# (troop_add_gold, "trp_player", 50000),
		# (try_for_range, ":troop_no", companions_begin, companions_end),
			# (call_script, "script_recruit_troop_as_companion", ":troop_no"),
		# (try_end),
	]),

# script_qp3_event_player_defeated_enemy_party
# Grabs information from the main script "event_player_defeated_enemy_party" which is called whenever a fight ends between two parties.
# INPUT:  none
# OUTPUT: none
("qp3_event_player_defeated_enemy_party",
  [

		(assign, ":party_enemies", "p_total_enemy_casualties"),
		
		### QUEST DATA ( patrol_for_bandits ) ###
		(try_begin),
			(check_quest_active, "qst_patrol_for_bandits"),   # We want to see how many bandits were on the other team.
			(quest_slot_eq, "qst_patrol_for_bandits", slot_quest_current_state, qp3_patrol_bandits_begun),
			(quest_get_slot, ":center_no", "qst_patrol_for_bandits", slot_quest_giver_center),
			(quest_get_slot, ":radius", "qst_patrol_for_bandits", slot_quest_town_radius),
			(call_script, "script_cf_qus_party_close_to_center", "p_main_party", ":center_no", ":radius"), # Only counts if we're near home.
			
			# get number of stacks of enemy party
			(party_get_num_companion_stacks, ":stack_limit", ":party_enemies"),
			(quest_get_slot, ":count_bandits", "qst_patrol_for_bandits", slot_quest_current_tally),
			(try_for_range, ":stack_no", 0, ":stack_limit"),
				(party_stack_get_troop_id, ":troop_no", ":party_enemies", ":stack_no"),
				#(party_stack_get_num_wounded, ":count_wounded", ":party_enemies", ":stack_no"),
				(party_stack_get_size, ":count_wounded", ":party_enemies", ":stack_no"),
				(ge, ":count_wounded", 1),
				(is_between, ":troop_no", qp3_bandits_begin, qp3_bandits_end),
				(val_add, ":count_bandits", ":count_wounded"),
				(ge, DEBUG_QUEST_PACK_3, 1),
				(assign, reg1, ":count_wounded"),
				(str_store_troop_name, s1, ":troop_no"),
				(display_message, "@DEBUG (QP3): {reg1} bandits [ {s1} ] from party [ total_enemy_casualties ] added to tally.", gpu_debug),
			(try_end),
			(quest_set_slot, "qst_patrol_for_bandits", slot_quest_current_tally, ":count_bandits"),
			(call_script, "script_qp3_quest_patrol_for_bandits", floris_quest_update),
			# Let the player know what's going on.
			(quest_get_slot, reg31, "qst_patrol_for_bandits", slot_quest_current_tally),
			(quest_get_slot, reg32, "qst_patrol_for_bandits", slot_quest_target_amount),
			(str_store_party_name, s13, ":center_no"),
			(display_message, "@You have slain {reg31} of the requested {reg32} bandits around {s13}."),
			########
			
			# Check if we have enough to successfully finish the quest.
			(quest_get_slot, ":amount_needed", "qst_patrol_for_bandits", slot_quest_target_amount),
			(quest_get_slot, ":amount_current", "qst_patrol_for_bandits", slot_quest_current_tally),
			(ge, ":amount_current", ":amount_needed"),
			(call_script, "script_common_quest_change_state", "qst_patrol_for_bandits", qp3_patrol_bandits_complete),
			(call_script, "script_qp3_quest_patrol_for_bandits", floris_quest_succeed),
		(try_end),
	]),
	
########################################################################################################################################################
####################                                             COMMON NOBILITY QUESTS                                             ####################
########################################################################################################################################################
# script_qp3_quest_summoned_to_hall
# Gating quest for all quests where the player is requested to come back to one of their owned centers to deal with a problem.
# INPUT: none
# OUTPUT: none
("qp3_quest_summoned_to_hall",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_summoned_to_hall"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp3_summoned_title"),
		(str_store_string, s41, ":quest_title"),
		(quest_get_slot, ":giver_center", ":quest_no", slot_quest_giver_center),
		
		# Quest Stages
		# qp3_summoned_inactive                     = 0
		# qp3_summoned_summoned_to_fief             = 1
		# qp3_summoned_problem_explained            = 2

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, ":giver_center"),
			(str_store_string, s61,       "str_qp3_summoned_quest_text"), # Needs: s13 (giver center)
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",               qp3_summoned_summoned_to_fief),
			(party_get_slot, ":castle_steward", "$current_town", slot_center_steward),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     ":castle_steward"),
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,                   -1), # Assigned prior to quest beginning.
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 20),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          5),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  5),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp3_quest_title"),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(quest_set_slot, "qst_summoned_to_hall", slot_quest_current_state, qp3_summoned_inactive),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(quest_set_slot, "qst_summoned_to_hall", slot_quest_current_state, qp3_summoned_inactive),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", -2),
			
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


# script_qp3_quest_patrol_for_bandits
# Handles all quest specific actions for quest "patrol_for_bandits".
# INPUT: none
# OUTPUT: none
("qp3_quest_patrol_for_bandits",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_patrol_for_bandits"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp3_patrol_bandits_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp3_patrol_bandits_inactive                     = 0
		# qp3_patrol_bandits_begun                        = 1
		# qp3_patrol_bandits_complete                     = 2
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, "$current_town"),
			(assign, reg11, 50),
			(str_store_string, s61,       "str_qp3_patrol_bandits_quest_text"), # Needs: s13 (giver center), reg11 (# bandits)
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",               qp3_patrol_bandits_begun),
			(party_get_slot, ":castle_steward", "$current_town", slot_center_steward),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     ":castle_steward"),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 20),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          20),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  20),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   50),
			(quest_set_slot, ":quest_no", slot_quest_current_tally,                   0),
			# Determine applicable radius.
			(party_get_position, pos0 , "$current_town"),
            (assign, ":end",10),
            (try_for_range, ":counter", 1, ":end"),
               (map_get_water_position_around_position, pos1, pos0, ":counter"),
               (assign, ":end",":counter"),
            (try_end),
			(try_begin),
				(lt, ":counter", 5),
				(quest_set_slot, ":quest_no", slot_quest_town_radius,                  40),
			(else_try),
				(quest_set_slot, ":quest_no", slot_quest_town_radius,                  25),
			(try_end),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp3_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(try_begin),
				(eq, ":quest_stage", qp3_patrol_bandits_begun),
				(quest_get_slot, reg21, ":quest_no", slot_quest_current_tally),
				(try_begin),
					(ge, reg21, 2),
					(str_store_string, s21, "@{reg21} bandits"),
				(else_try),
					(str_store_string, s21, "@1 bandit"),
				(try_end),
				(quest_get_slot, reg22, ":quest_no", slot_quest_target_amount),
				(str_store_string, s65, "@You have eliminated {s21} of {reg22} bandits required."),
				(assign, ":note_slot", 3),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			#(display_message, "str_quest_log_updated"), # Very spammy on this quest if left.
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", 400),
			(assign, ":town_relation", 1),
			(assign, ":faction_relation", 0),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", 1),
				(val_add, ":faction_relation", 1),
				(val_add, ":reward_xp", 300),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", 1),
				(val_add, ":faction_relation", 2),
				(val_add, ":reward_xp", 300),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			# Change faction reputation.
			(store_faction_of_party, ":faction_no", ":quest_center"),
			(call_script, "script_change_player_relation_with_faction", ":faction_no", ":faction_relation"),
			## SILVERSTAG EMBLEMS+ ##
			(call_script, "script_cf_emblem_quest_reward_check", 1), # emblem_scripts.py
			## SILVERSTAG EMBLEMS- ##
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Consequences
			(assign, ":town_relation", -1),
			(assign, ":faction_relation", 0),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", -1),
				(val_add, ":faction_relation", -1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", -1),
				(val_add, ":faction_relation", -2),
			(try_end),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			# Change faction reputation.
			(store_faction_of_party, ":faction_no", ":quest_center"),
			(call_script, "script_change_player_relation_with_faction", ":faction_no", ":faction_relation"),
			
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
	
# script_qp3_quest_mercs_for_hire
# Handles all quest specific actions for quest "mercs_for_hire".
# INPUT: none
# OUTPUT: none
("qp3_quest_mercs_for_hire",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_mercs_for_hire"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp3_mercs_for_hire_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp3_mercs_for_hire_inactive                     = 0
		# qp3_mercs_for_hire_begun                        = 1
		# qp3_mercs_for_hire_active_contract              = 2 # Decision made to reject or accept.
		# qp3_mercs_for_hire_contract_due                 = 3 # Triggers map conversation with leader.  Depending on decision stage continues to 4 or 5.
		# qp3_mercs_for_hire_agree_to_renew               = 4 # When contract expires the stage is reset to 2 & duration refreshed.
		# qp3_mercs_for_hire_refused_to_renew             = 5 # When contract expires the stage is continued to 6.
		# qp3_mercs_for_hire_contract_ended               = 6 # Mercenary party leaves.

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, "$current_town"),
			(str_store_string, s61,       "str_qp3_mercs_for_hire_quest_text"),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",               qp3_mercs_for_hire_begun),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     qp3_actor_mercenary_leader),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  30),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_current_tally,                   0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp3_quest_title"),
			# Name the mercenary leader
			(store_random_in_range, ":leader_name", "str_qp3_merc_hero_name_1", "str_qp3_merc_hero_title_1"),
			(troop_set_name, qp3_actor_mercenary_leader, ":leader_name"),
			(store_random_in_range, ":leader_title", "str_qp3_merc_hero_title_1", "str_qp3_merc_band_name_1"),
			(quest_set_slot, ":quest_no", slot_quest_merc_leader_title, ":leader_title"),
			# Name the mercenary company.
			(store_random_in_range, ":band_name", "str_qp3_merc_band_name_1", "str_qp3_merc_band_name_end"),
			(quest_set_slot, ":quest_no", slot_quest_merc_band_name, ":band_name"),
			# Generate army size.
			(store_character_level, ":level"),
			(store_skill_level, ":roll_limit", "skl_leadership", "trp_player"),
			(val_max, ":roll_limit", 3),
			(assign, ":band_size", ":level"),
			(val_div, ":level", 2),
			(try_for_range, ":unused", 0, ":level"),
				(store_random_in_range, ":roll", 1, ":roll_limit"),
				(val_add, ":band_size", ":roll"),
			(try_end),
			(val_min, ":band_size", 100), # Cap at 100 tops.
			(quest_set_slot, ":quest_no", slot_quest_merc_band_ideal_size, ":band_size"),
			# Generate requested contract amount.
			(store_mul, ":contract_price", ":band_size", 15),
			(quest_set_slot, ":quest_no", slot_quest_target_amount, ":contract_price"), # Contract payment.
			(quest_set_slot, ":quest_no", slot_quest_merc_contract_debt, 0),
			# Determine faction flavor
			(try_begin),
				(this_or_next|eq, ":band_name", "str_qp3_merc_band_name_1"),
				(eq, ":band_name", "str_qp3_merc_band_name_9"),
				(assign, ":culture", "fac_culture_1"), # Swadia
			(else_try),
				(eq, ":band_name", "str_qp3_merc_band_name_7"),
				(assign, ":culture", "fac_culture_2"), # Vaegirs
			(else_try),
				(this_or_next|eq, ":band_name", "str_qp3_merc_band_name_5"),
				(eq, ":band_name", "str_qp3_merc_band_name_6"),
				(assign, ":culture", "fac_culture_3"), # Khergits
			(else_try),
				(this_or_next|eq, ":band_name", "str_qp3_merc_band_name_2"),
				(eq, ":band_name", "str_qp3_merc_band_name_8"),
				(assign, ":culture", "fac_culture_4"), # Nord
			(else_try),
				(eq, ":band_name", "str_qp3_merc_band_name_3"),
				(assign, ":culture", "fac_culture_5"), # Rhodok
			(else_try),
				(this_or_next|eq, ":band_name", "str_qp3_merc_band_name_10"),
				(eq, ":band_name", "str_qp3_merc_band_name_11"),
				(assign, ":culture", "fac_culture_6"), # Sarranid
			(else_try),
				### DEFAULT CULTURE ### - Based upon the initiating town.
				(store_faction_of_party, ":faction_no", "$current_town"),
				(faction_get_slot, ":culture", ":faction_no", slot_faction_culture),
			(try_end),
			(quest_set_slot, ":quest_no", slot_quest_merc_culture, ":culture"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(quest_get_slot, ":quest_giver", ":quest_no", slot_quest_giver_troop),
			(str_store_troop_name, s14, ":quest_giver"),
			(try_begin),
				(eq, ":quest_stage", qp3_mercs_for_hire_active_contract),
				(str_store_string, s65, "@You have agreed to a contract of payment with {s14} so they will follow your party's lead."),
				(assign, ":note_slot", 3),
				(str_clear, s1),
				(add_quest_note_from_sreg, ":quest_no", 4, s1, 0), # Clear out any contract renewal information.
			# (else_try),
				# (eq, ":quest_stage", qp3_mercs_for_hire_agree_to_renew),
				# (str_store_string, s65, "@You have agreed to renew your contract with {s14} once it expires."),
				# (assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp3_mercs_for_hire_refused_to_renew),
				(str_store_string, s65, "@You have decided against rewnewing your contract with {s14} so his group will leave once it expires."),
				(assign, ":note_slot", 4),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(try_begin),
			  (quest_slot_ge, ":quest_no", slot_quest_expiration_days, 1),
			  (quest_get_slot, reg20, ":quest_no", slot_quest_expiration_days),
			  (add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg20} days remaining on the current contract.", 0),
			(try_end),
			#(display_message, "str_quest_log_updated"),
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(cancel_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Consequences
			
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			(call_script, "script_qp3_quest_mercenary_function", mercs_destroy_party),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),

# script_qp3_quest_mercenary_function
# Handles numerous actions associated with the mercenary group for quest "mercs_for_hire".
# INPUT: none
# OUTPUT: none
("qp3_quest_mercenary_function",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_mercs_for_hire"),
		# Get specific string data.
		(quest_get_slot, ":quest_title", ":quest_no", slot_quest_unique_name),
		(str_store_string, s41, ":quest_title"),
		
		# Functions
		# mercs_generate_party          = 0
		# mercs_upgrade_troops          = 1
		# mercs_recruit_troops          = 2
		# mercs_generate_contract_cost  = 3
		# mercs_set_behavior_to_follow  = 4
		# mercs_destroy_party           = 5
		# mercs_remove_non_mercenaries  = 6
		# mercs_contract_renew          = 7
		# mercs_contract_end            = 8
		# mercs_payment_due             = 9
		# mercs_join_combat             = 10
		# mercs_sell_prisoners          = 11

		# Define tier 1-5 troops for initializing city center.
		(quest_get_slot, ":culture", ":quest_no", slot_quest_merc_culture),
		(faction_get_slot, ":tier_1", ":culture",  slot_faction_tier_1_troop),
		(faction_get_slot, ":tier_2", ":culture",  slot_faction_tier_2_troop),
		(faction_get_slot, ":tier_3", ":culture",  slot_faction_tier_3_troop),
		(faction_get_slot, ":tier_4", ":culture",  slot_faction_tier_4_troop),
		(faction_get_slot, ":tier_5", ":culture",  slot_faction_tier_5_troop),
		
		(try_begin),
			##### MERCS GENERATE PARTY #####
			(eq, ":function", mercs_generate_party),
			# Determine ideal size.
			(quest_get_slot, ":ideal_size", ":quest_no", slot_quest_merc_band_ideal_size),
			# Create the party
			(set_spawn_radius, 1),
			(spawn_around_party, "p_main_party", "pt_patrol_party"),
			(assign, ":merc_party", reg0),
			(quest_set_slot, ":quest_no", slot_quest_target_party, ":merc_party"),
			# Add troop leader
			(party_add_leader, ":merc_party", qp3_actor_mercenary_leader),
			(troop_set_skill, qp3_actor_mercenary_leader, "skl_pathfinding", 10),
			#(troop_raise_skill, qp3_actor_mercenary_leader, "skl_pathfinding", 10),
			(store_sub, ":troops_left", ":ideal_size", 1),
			(try_begin),
				# Add TIER 1 members
				(ge, ":troops_left", 1),
				(store_mul, ":tier_1_troops", ":troops_left", 60),
				(val_div, ":tier_1_troops", 100),
				(party_add_members, ":merc_party", ":tier_1", ":tier_1_troops"),
				(val_sub, ":troops_left", ":tier_1_troops"),
				# Add TIER 2 members
				(ge, ":troops_left", 1),
				(store_mul, ":tier_2_troops", ":troops_left", 60),
				(val_div, ":tier_2_troops", 100),
				(party_add_members, ":merc_party", ":tier_2", ":tier_2_troops"),
				(val_sub, ":troops_left", ":tier_2_troops"),
				# Add TIER 3 members
				(ge, ":troops_left", 1),
				(store_mul, ":tier_3_troops", ":troops_left", 60),
				(val_div, ":tier_3_troops", 100),
				(party_add_members, ":merc_party", ":tier_3", ":tier_3_troops"),
				(val_sub, ":troops_left", ":tier_3_troops"),
				# Add TIER 4 members
				(ge, ":troops_left", 1),
				(store_mul, ":tier_4_troops", ":troops_left", 60),
				(val_div, ":tier_4_troops", 100),
				(party_add_members, ":merc_party", ":tier_4", ":tier_4_troops"),
				(val_sub, ":troops_left", ":tier_4_troops"),
				# Add TIER 5 members
				(ge, ":troops_left", 1),
				(store_mul, ":tier_5_troops", ":troops_left", 60),
				(val_div, ":tier_5_troops", 100),
				(party_add_members, ":merc_party", ":tier_5", ":tier_5_troops"),
				(val_sub, ":troops_left", ":tier_5_troops"),
				# Add remaining numbers to TIER 1 members
				(ge, ":troops_left", 1),
				(party_add_members, ":merc_party", ":tier_1", ":troops_left"),
			(try_end),
			#(store_faction_of_party, ":faction_no", "p_main_party"),
			(party_set_faction, ":merc_party", "$players_kingdom"),
			# Name the band.
			(quest_get_slot, ":band_name", ":quest_no", slot_quest_merc_band_name),
			(party_set_name, ":merc_party", ":band_name"),
			
		(else_try),
			##### MERCS UPGRADE TROOPS #####
			(eq, ":function", mercs_upgrade_troops),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(party_is_active, ":merc_party"),
			(party_get_num_companion_stacks, ":stack_limit", ":merc_party"),
			# Upgrade 33% of each stack.
			(try_for_range, ":stack_no", 0, ":stack_limit"),
				(party_stack_get_troop_id, ":troop_no", ":merc_party", ":stack_no"),
				(neg|troop_is_hero, ":troop_no"),
				# Make sure this is someone we want in the party.
				(this_or_next|eq, ":troop_no", ":tier_1"),
				(this_or_next|eq, ":troop_no", ":tier_2"),
				(this_or_next|eq, ":troop_no", ":tier_3"),
				(this_or_next|eq, ":troop_no", ":tier_4"),
				(eq, ":troop_no", ":tier_5"),
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
				(party_stack_get_size, ":stack_size", ":merc_party", ":stack_no"),
				(store_mul, ":upgrade_count", ":stack_size", 33),
				(val_div, ":upgrade_count", 100),
				# Add new troops.
				(party_add_members, ":merc_party", ":upgrade_troop", ":upgrade_count"),
				# Remove old troops.
				(party_remove_members, ":merc_party", ":troop_no", ":upgrade_count"),
				# Improve army size.
				(quest_get_slot, ":band_size", ":quest_no", slot_quest_merc_band_ideal_size),
				(val_add, ":band_size", 8),
				(val_min, ":band_size", 100),
				(quest_set_slot, ":quest_no", slot_quest_merc_band_ideal_size, ":band_size"),
				
				### DIAGNOSTIC ###
				(ge, DEBUG_QUEST_AI, 1),
				(str_store_troop_name, s31, ":troop_no"),
				(str_store_troop_name, s32, ":upgrade_troop"),
				(assign, reg31, ":upgrade_count"),
				(display_message, "@DEBUG (Merc AI): Upgraded {reg31} '{s31}' -> '{s32}' in mercenary party.", gpu_debug),
			(try_end),
			
		(else_try),
			##### MERCS RECRUIT TROOPS #####
			(eq, ":function", mercs_recruit_troops),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(party_is_active, ":merc_party"),
			(quest_get_slot, ":ideal_size", ":quest_no", slot_quest_merc_band_ideal_size),
			(assign, ":party_size", 0),
			(party_count_members_of_type, ":members", ":merc_party", qp3_actor_mercenary_leader),
			(val_add, ":party_size", ":members"),
			(party_count_members_of_type, ":members", ":merc_party", ":tier_1"),
			(val_add, ":party_size", ":members"),
			(party_count_members_of_type, ":members", ":merc_party", ":tier_2"),
			(val_add, ":party_size", ":members"),
			(party_count_members_of_type, ":members", ":merc_party", ":tier_3"),
			(val_add, ":party_size", ":members"),
			(party_count_members_of_type, ":members", ":merc_party", ":tier_4"),
			(val_add, ":party_size", ":members"),
			(party_count_members_of_type, ":members", ":merc_party", ":tier_5"),
			(val_add, ":party_size", ":members"),
			(try_begin),
				(lt, ":party_size", ":ideal_size"),
				(store_sub, ":recruit_count", ":ideal_size", ":party_size"),
				(party_get_slot, ":limit_by_funds", ":merc_party", slot_party_wealth),
				(val_div, ":limit_by_funds", 5),
				(val_min, ":recruit_count", ":limit_by_funds"),
				(party_add_members, ":merc_party", ":tier_1", ":recruit_count"),
				### DIAGNOSTIC ###
				(ge, DEBUG_QUEST_AI, 1),
				(assign, reg31, ":recruit_count"),
				(display_message, "@DEBUG (Merc AI): Recruited {reg31} new members to mercenary party.", gpu_debug),
			(else_try),
				### DIAGNOSTIC ###
				(ge, DEBUG_QUEST_AI, 1),
				(assign, reg31, ":party_size"),
				(assign, reg32, ":ideal_size"),
				(display_message, "@DEBUG (Merc AI): Mercenary party did not recruit new members.  Compliment {reg31} / {reg32}", gpu_debug),
			(try_end),
			
		(else_try),
			##### MERCS GENERATE CONTRACT COST #####
			(eq, ":function", mercs_generate_contract_cost),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(party_is_active, ":merc_party"),
			(party_get_num_companion_stacks, ":stack_limit", ":merc_party"),
			(assign, ":total_cost", 50),
			(try_for_range, ":stack_no", 0, ":stack_limit"),
				(party_stack_get_troop_id, ":troop_no", ":merc_party", ":stack_no"),
				(neg|troop_is_hero, ":troop_no"), # Ignore the leader.
				(try_begin),
					(eq, ":troop_no", ":tier_1"),
					(assign, ":troop_cost", 5),
				(else_try),
					(eq, ":troop_no", ":tier_2"),
					(assign, ":troop_cost", 10),
				(else_try),
					(eq, ":troop_no", ":tier_3"),
					(assign, ":troop_cost", 15),
				(else_try),
					(eq, ":troop_no", ":tier_4"),
					(assign, ":troop_cost", 30),
				(else_try),
					(eq, ":troop_no", ":tier_5"),
					(assign, ":troop_cost", 60),
				(else_try),
					(assign, ":troop_cost", 25),
				(try_end),
				(party_stack_get_size, ":stack_size", ":merc_party", ":stack_no"),
				(val_mul, ":troop_cost", ":stack_size"),
				(val_add, ":total_cost", ":troop_cost"),
				### DIAGNOSTIC ###
				(ge, DEBUG_QUEST_AI, 1),
				(str_store_troop_name, s31, ":troop_no"),
				(assign, reg31, ":troop_cost"),
				(assign, reg32, ":total_cost"),
				(assign, reg33, ":stack_size"),
				(display_message, "@DEBUG (Merc AI): {reg33} '{s31}' raised contract price by {reg31} to {reg32}.", gpu_debug),
			(try_end),
			(quest_set_slot, ":quest_no", slot_quest_target_amount, ":total_cost"),
			
		(else_try),
			##### MERCS SET BEHAVIOR TO FOLLOW #####
			(eq, ":function", mercs_set_behavior_to_follow),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(party_is_active, ":merc_party"),
			(party_set_ai_object, ":merc_party", "p_main_party"),
			(party_set_ai_behavior, ":merc_party", ai_bhvr_escort_party),  # Try ai_bhvr_driven_by_party if that doesn't work.  
			(party_set_slot, ":merc_party", slot_party_ai_state, spai_accompanying_army),
			#(party_set_slot, ":merc_party", slot_party_type, spt_kingdom_hero_party),
			(party_set_slot, ":merc_party", slot_party_ai_object, "trp_player"),
			(party_set_helpfulness, ":merc_party", 500),
			
		(else_try),
			##### MERCS DESTROY PARTY #####
			(eq, ":function", mercs_destroy_party),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(try_begin),
				(party_is_active, ":merc_party"),
				(neq, ":merc_party", 0),
				(remove_party, ":merc_party"),
			(try_end),
			
		(else_try),
			##### MERCS REMOVE NON-MERCENARIES #####
			(eq, ":function", mercs_remove_non_mercenaries),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(party_is_active, ":merc_party"),
			# Remove any non-mercenary troops from the party.
			(party_get_num_companion_stacks, ":stack_limit", ":merc_party"),
			(try_for_range_backwards, ":stack_no", 0, ":stack_limit"),
				(party_stack_get_troop_id, ":troop_no", ":merc_party", ":stack_no"),
				(neg|troop_is_hero, ":troop_no"), # Don't want to lose the leader.
				(neq, ":troop_no", ":tier_1"),
				(neq, ":troop_no", ":tier_2"),
				(neq, ":troop_no", ":tier_3"),
				(neq, ":troop_no", ":tier_4"),
				(neq, ":troop_no", ":tier_5"),
				(party_stack_get_size, ":stack_size", ":merc_party", ":stack_no"),
				(party_remove_members, ":merc_party", ":troop_no", ":stack_size"),
				### DIAGNOSTIC ###
				(ge, DEBUG_QUEST_AI, 1),
				(str_store_troop_name, s31, ":troop_no"),
				(assign, reg31, ":stack_size"),
				(display_message, "@DEBUG (Merc AI): Removed {reg31} '{s31}' from mercenary party.", gpu_debug),
			(try_end),
			
		(else_try),
			##### MERCS RENEW CONTRACT #####
			(eq, ":function", mercs_contract_renew),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days, 30),
			(add_quest_note_from_sreg, ":quest_no", 7, "@You have 30 days remaining on the current contract.", 0),
			(call_script, "script_common_quest_change_state", ":quest_no", qp3_mercs_for_hire_active_contract),
			
		(else_try),
			##### MERCS END CONTRACT #####
			(eq, ":function", mercs_contract_end),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_succeed),
			
		(else_try),
			##### MERCS JOIN COMBAT #####
			(eq, ":function", mercs_join_combat),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(try_begin),
				(party_is_active, ":merc_party"),
				(eq, ":merc_party", reg41),
				(check_quest_active, "qst_mercs_for_hire"),
				(store_distance_to_party_from_party, ":distance", ":merc_party", "p_main_party"),
				(lt, ":distance", 5),
				(party_quick_attach_to_current_battle, ":merc_party", 0), #attach as friend
				(neg|is_between, "$g_encountered_party", centers_begin, centers_end),
				(try_begin),
					(store_faction_of_party, ":faction_check", "$g_encountered_party"),
					(neq, ":faction_check", "$players_kingdom"), # We don't really want our mercenaries joining battle with us displayed if we're talking to a friend.
					(str_store_party_name, s1, ":merc_party"),
					(display_message, "str_s1_joined_battle_friend"),
				(try_end),
				# (ge, DEBUG_QUEST_AI, 1),
				# (display_message, "@DEBUG (Merc AI): Mercenary party has been forced to join the player.", gpu_debug),
			(else_try),
				(eq, ":merc_party", reg41),
				(check_quest_active, "qst_mercs_for_hire"),
				(ge, DEBUG_QUEST_AI, 1),
				(display_message, "@DEBUG (Merc AI): Mercenary party did not join because they are too far away.", gpu_debug),
			(try_end),
			
		(else_try),
			##### MERCS PAYMENT DUE #####
			(eq, ":function", mercs_payment_due),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(quest_get_slot, ":contract_cost", "qst_mercs_for_hire", slot_quest_target_amount),
			# Figure out how much cash the player has.
			(store_troop_gold, ":gold", "trp_player"),
			# Remove his cash.
			(assign, reg20, 0), # Mercenary party should remain.
			(try_begin),
				### Player can afford his contract payment and any debt built up ###
				(quest_get_slot, ":contract_debt", "qst_mercs_for_hire", slot_quest_merc_contract_debt),
				(store_add, ":total_cost", ":contract_cost", ":contract_debt"),
				(ge, ":gold", ":total_cost"),
				(troop_remove_gold, "trp_player", ":total_cost"),
				(assign, reg31, ":total_cost"),
				(party_get_slot, ":wealth", ":merc_party", slot_party_wealth),
				(val_add, ":wealth", reg31),
				(party_set_slot, ":merc_party", slot_party_wealth, ":wealth"),
				(display_message, "@You have paid your mercenaries their weekly wage of {reg31} denars.", gpu_green),
				(try_begin),
					(ge, ":contract_debt", 1),
					(display_message, "@You have paid off your remaining debt owed to the mercenaries.", gpu_light_blue),
				(try_end),
			(else_try),
				### Player can afford his contract payment and some of his debt ###
				(quest_get_slot, ":contract_debt", "qst_mercs_for_hire", slot_quest_merc_contract_debt),
				(store_add, ":total_cost", ":contract_cost", ":contract_debt"),
				(ge, ":gold", ":contract_cost"),
				(store_sub, ":apply_to_debt", ":gold", ":contract_cost"),
				(store_add, ":total_cost", ":contract_cost", ":apply_to_debt"),
				(val_sub, ":contract_debt", ":apply_to_debt"),
				(quest_set_slot, "qst_mercs_for_hire", slot_quest_merc_contract_debt, ":contract_debt"),
				(troop_remove_gold, "trp_player", ":total_cost"),
				(assign, reg31, ":total_cost"),
				(assign, reg32, ":apply_to_debt"),
				(party_get_slot, ":wealth", ":merc_party", slot_party_wealth),
				(val_add, ":wealth", reg31),
				(party_set_slot, ":merc_party", slot_party_wealth, ":wealth"),
				(display_message, "@You have paid your mercenaries their weekly wage of {reg31} denars.", gpu_green),
				(display_message, "@You have paid off {reg32} denars of your debt owed to the mercenaries.", gpu_light_blue),
			(else_try),
				### Player can afford his contract payment only. ###
				(ge, ":gold", ":contract_cost"),
				(this_or_next|quest_slot_ge, "qst_mercs_for_hire", slot_quest_expiration_days, 7),
				(quest_slot_eq, "qst_mercs_for_hire", slot_quest_merc_contract_debt, 0),
				(troop_remove_gold, "trp_player", ":contract_cost"),
				(assign, reg31, ":contract_cost"),
				(party_get_slot, ":wealth", ":merc_party", slot_party_wealth),
				(val_add, ":wealth", reg31),
				(party_set_slot, ":merc_party", slot_party_wealth, ":wealth"),
				(display_message, "@You have paid your mercenaries their weekly wage of {reg31} denars.", gpu_green),
			(else_try),
				### Player can afford half of his contract payment so they'll stay, but expect the rest by contract end. ###
				(store_div, ":half_payment", ":contract_cost", 2),
				(ge, ":gold", ":half_payment"),
				(this_or_next|quest_slot_ge, "qst_mercs_for_hire", slot_quest_expiration_days, 1),
				(quest_slot_eq, "qst_mercs_for_hire", slot_quest_merc_contract_debt, 0),
				(troop_remove_gold, "trp_player", ":half_payment"),
				(quest_get_slot, ":contract_debt", "qst_mercs_for_hire", slot_quest_merc_contract_debt),
				(val_add, ":contract_debt", ":half_payment"), # half of the original wage goes to debt.
				(quest_set_slot, "qst_mercs_for_hire", slot_quest_merc_contract_debt, ":contract_debt"),
				(assign, reg31, ":half_payment"),
				(party_get_slot, ":wealth", ":merc_party", slot_party_wealth),
				(val_add, ":wealth", reg31),
				(party_set_slot, ":merc_party", slot_party_wealth, ":wealth"),
				(display_message, "@You have paid your mercenaries {reg31} denars which is only half of their wage.", gpu_red),
				(display_message, "@They will expect the rest of their wages by contract end or will abandon you.", gpu_light_blue),
			(else_try),
				### Player can't even afford a half payment.  If debt is 0 they'll wait, but if not they leave. ###
				(store_div, ":half_payment", ":contract_cost", 2),
				(neg|ge, ":gold", ":half_payment"),
				(quest_slot_ge, "qst_mercs_for_hire", slot_quest_expiration_days, 1),
				(quest_get_slot, ":contract_debt", "qst_mercs_for_hire", slot_quest_merc_contract_debt),
				(le, ":contract_debt", 0),
				(val_add, ":contract_debt", ":contract_cost"), # half of the original wage goes to debt.
				(quest_set_slot, "qst_mercs_for_hire", slot_quest_merc_contract_debt, ":contract_debt"),
				(assign, reg31, ":contract_cost"),
				(display_message, "@You were unable to pay even half your mercenaries wage of {reg31} so it is added to debt.", gpu_red),
				(display_message, "@They will expect the rest of their wages by contract end or will abandon you.", gpu_red),
			(else_try),
				# Default - Mercenaries should leave.
				(assign, reg20, 1), # Mercenary party should leave.
			(try_end),
			
		(else_try),
			##### MERCS SELL PRISONERS #####
			(eq, ":function", mercs_sell_prisoners),
			(quest_get_slot, ":merc_party", ":quest_no", slot_quest_target_party),
			(assign, ":center_no", "$current_town"),
			# Check on how many prisoners we have available for sale.
			(party_get_num_prisoners, ":prisoner_count", ":merc_party"),
			(party_get_num_prisoner_stacks, ":stack_limit", ":merc_party"),
			(try_begin),
				(ge, ":stack_limit", 1), # They need to have something worth selling.
				(is_between, ":center_no", towns_begin, towns_end),
				# Is a ransom broker available?
				(party_get_slot, ":ransom_broker", "$current_town", slot_center_ransom_broker),
				(gt, ":ransom_broker", 0),
				# Sell prisoners.
				(assign, ":earnings", 0),
				(try_for_range, ":stack_no", 0, ":stack_limit"),
					(party_prisoner_stack_get_troop_id, ":troop_no", ":merc_party", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"), # Prevent companions, lords & player from being taken.
					(party_prisoner_stack_get_size, ":troop_count", ":merc_party", ":stack_no"),
					(call_script, "script_game_get_prisoner_price", ":troop_no"),
					(assign, ":troop_value", reg0),
					(store_mul, ":stack_value", ":troop_value", ":troop_count"),
					(val_add, ":earnings", ":stack_value"),
				(try_end),
				# Remove the prisoners from the mercenary party.
				(assign, "$g_move_heroes", 0),
				(call_script, "script_party_remove_all_prisoners", ":merc_party"),
				# Store the mercenary party's earnings for later recruitment purposes.
				(party_get_slot, ":wealth", ":merc_party", slot_party_wealth),
				(val_add, ":wealth", ":earnings"),
				(party_set_slot, ":merc_party", slot_party_wealth, ":wealth"),
				### DIAGNOSTIC ###
				(try_begin),
					(ge, DEBUG_QUEST_AI, 1),
					(str_store_party_name, s31, ":merc_party"),
					(str_store_party_name, s32, ":center_no"),
					(assign, reg31, ":earnings"),
					(assign, reg32, ":prisoner_count"),
					(display_message, "@DEBUG (Merc AI): {s31} offloads {reg32} prisoners in {s32} for {reg31} denars.", gpu_debug),
				(try_end),
			(try_end),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "@ERROR - Mercenaries '{s41}' - Failed to update on function {reg31}.", qp_error_color),
		(try_end),
	]),
	
# script_qp3_quest_destroy_the_lair
# Handles all quest specific actions for quest "destroy_their_lair".
# INPUT: none
# OUTPUT: none
("qp3_quest_destroy_the_lair",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_destroy_the_lair"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp3_destroy_the_lair_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp3_destroy_the_lair_inactive                   = 0
		# qp3_destroy_the_lair_begun                      = 1
		# qp3_destroy_the_lair_found_it                   = 2
		# qp3_destroy_the_lair_end                        = 3
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, "$current_town"),
			(str_store_string, s61,       "str_qp3_destroy_the_lair_quest_text"), # Needs: s13 (giver center)
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",               qp3_destroy_the_lair_begun),
			(party_get_slot, ":castle_steward", "$current_town", slot_center_steward),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     ":castle_steward"),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          20),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  20),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   1),
			(quest_set_slot, ":quest_no", slot_quest_current_tally,                   0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp3_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(try_begin),
				(eq, ":quest_stage", qp3_destroy_the_lair_found_it),
				(str_store_string, s65, "@You have located the bandits lair."),
				(assign, ":note_slot", 3),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			#(display_message, "str_quest_log_updated"), # Very spammy on this quest if left.
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", 400),
			(assign, ":town_relation", 1),
			(assign, ":faction_relation", 0),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", 1),
				(val_add, ":faction_relation", 1),
				(val_add, ":reward_xp", 300),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", 1),
				(val_add, ":faction_relation", 2),
				(val_add, ":reward_xp", 300),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			# Change faction reputation.
			(store_faction_of_party, ":faction_no", ":quest_center"),
			(call_script, "script_change_player_relation_with_faction", ":faction_no", ":faction_relation"),
			## SILVERSTAG EMBLEMS+ ##
			(call_script, "script_cf_emblem_quest_reward_check", 1), # emblem_scripts.py
			## SILVERSTAG EMBLEMS- ##
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Consequences
			(assign, ":town_relation", -1),
			(assign, ":faction_relation", 0),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", -1),
				(val_add, ":faction_relation", -1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", -1),
				(val_add, ":faction_relation", -2),
			(try_end),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			# Change faction reputation.
			(store_faction_of_party, ":faction_no", ":quest_center"),
			(call_script, "script_change_player_relation_with_faction", ":faction_no", ":faction_relation"),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			##### QUEST CHECK VICTORY CONDITIONS #####
			(eq, ":function", floris_quest_victory_condition),
			(try_begin),
			  (check_quest_active, ":quest_no"),
			  (quest_slot_eq, ":quest_no", slot_quest_target_party, "$g_encountered_party"),
			  (call_script, "script_qp3_quest_destroy_the_lair", floris_quest_succeed),
			(try_end),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp3_quest_escort_to_mine
# Handles all quest specific actions for quest "escort_to_mine".
# INPUT: none
# OUTPUT: none
("qp3_quest_escort_to_mine",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_escort_to_mine"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp3_escort_to_mine_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp3_escort_to_mine_inactive                     = 0
		# qp3_escort_to_mine_begun                        = 1
		# qp3_escort_to_mine_slaves_delivered             = 2
		# qp3_escort_to_mine_money_returned               = 3
		# qp3_escort_to_mine_slaves_lost                  = 4
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, "$current_town"),
			(str_store_string, s61,       "str_qp3_escort_to_mine_quest_text"), # Needs: s13 (giver center)
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",               qp3_escort_to_mine_begun),
			(party_get_slot, ":castle_steward", "$current_town", slot_center_steward),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     ":castle_steward"),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_target_center,                   "p_salt_mine"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			# (quest_set_slot, ":quest_no", slot_quest_target_amount,                   40), # Setup later.
			(quest_set_slot, ":quest_no", slot_quest_current_tally,                   0),
			##### PRISONERS GENERATE PARTY #####
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_create, 0, "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_target_party, reg51),
			(assign, ":caravan", reg51),
			(assign, "$g_move_heroes", 0),
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_generate_escort_cost, ":caravan", "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount, reg51), # Player contract payment.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_load_from_center, ":caravan", "$current_town"),     # Move prisoners from town to new party.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_direct_to_destination, ":caravan", "p_salt_mine"),  # Set party AI
			## Activate the quest. ##
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp3_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
			(str_store_party_name_link, s14, ":target_center"),
			(try_begin),
				(eq, ":quest_stage", qp3_escort_to_mine_slaves_delivered),
				(str_store_string, s65, "@Your prisoner caravan has arrived at {s14}.  Now you must ensure the guards make it back with the payment."),
				(assign, ":note_slot", 3),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			#(display_message, "str_quest_log_updated"), # Very spammy on this quest if left.
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(quest_get_slot, ":payment", ":quest_no", slot_quest_target_amount),
			(assign, ":reward_xp", 400),
			(assign, ":town_relation", 1),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", 1),
				(val_add, ":reward_xp", 300),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", 1),
				(val_add, ":reward_xp", 300),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			# Award contract payment
			(call_script, "script_troop_add_gold", "trp_player", ":payment"),
			## SILVERSTAG EMBLEMS+ ##
			(call_script, "script_cf_emblem_quest_reward_check", 2), # emblem_scripts.py
			## SILVERSTAG EMBLEMS- ##
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Consequences
			(assign, ":town_relation", -1),
			(assign, ":faction_relation", 0),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", -1),
				(val_add, ":faction_relation", -1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", -1),
				(val_add, ":faction_relation", -2),
			(try_end),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			##### QUEST CHECK FAILURE CONDITIONS #####
			(eq, ":function", floris_quest_failure_condition),
			(try_begin),
			  (check_quest_active, ":quest_no"),
			  (quest_get_slot, ":party_no", ":quest_no", slot_quest_target_party),
			  (neg|party_is_active, ":party_no"),
			  (quest_slot_eq, ":quest_no", slot_quest_current_state, qp3_escort_to_mine_begun),
			  (display_message, "@The prisoners you were to escort have been slain.", qp_error_color),
			  (call_script, "script_qp3_quest_escort_to_mine", floris_quest_fail),
			(try_end),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp3_quest_escort_captive_lord_to_king
# Handles all quest specific actions for quest "the_bargaining_chip".
# INPUT: none
# OUTPUT: none
("qp3_quest_escort_captive_lord_to_king",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_escort_to_mine"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp3_escort_to_mine_title"),
		(str_store_string, s41, ":quest_title"),
		
		# (enable_party, "p_salt_mine"),
		
		# Quest Stages
		# qp3_escort_to_mine_inactive                     = 0
		# qp3_escort_to_mine_begun                        = 1
		# qp3_escort_to_mine_slaves_delivered             = 2
		# qp3_escort_to_mine_money_returned               = 3
		# qp3_escort_to_mine_slaves_lost                  = 4
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, "$current_town"),
			(str_store_string, s61,       "str_qp3_escort_to_mine_quest_text"), # Needs: s13 (giver center)
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",               qp3_escort_to_mine_begun),
			(party_get_slot, ":castle_steward", "$current_town", slot_center_steward),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     ":castle_steward"),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_target_center,                   "p_salt_mine"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			# (quest_set_slot, ":quest_no", slot_quest_target_amount,                   40), # Setup later.
			(quest_set_slot, ":quest_no", slot_quest_current_tally,                   0),
			##### PRISONERS GENERATE PARTY #####
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_create, 0, "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_target_party, reg51),
			(assign, ":caravan", reg51),
			(assign, "$g_move_heroes", 0),
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_generate_escort_cost, ":caravan", "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount, reg51), # Player contract payment.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_load_from_center, ":caravan", "$current_town"),     # Move prisoners from town to new party.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_direct_to_destination, ":caravan", "p_salt_mine"),  # Set party AI
			## Activate the quest. ##
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp3_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
			(str_store_party_name_link, s14, ":target_center"),
			(try_begin),
				(eq, ":quest_stage", qp3_escort_to_mine_slaves_delivered),
				(str_store_string, s65, "@Your prisoner caravan has arrived at {s14}.  Now you must ensure the guards make it back with the payment."),
				(assign, ":note_slot", 3),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			#(display_message, "str_quest_log_updated"), # Very spammy on this quest if left.
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(quest_get_slot, ":payment", ":quest_no", slot_quest_target_amount),
			(assign, ":reward_xp", 400),
			(assign, ":town_relation", 1),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", 1),
				(val_add, ":reward_xp", 300),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", 1),
				(val_add, ":reward_xp", 300),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			# Award contract payment
			(call_script, "script_troop_add_gold", "trp_player", ":payment"),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Consequences
			(assign, ":town_relation", -1),
			(assign, ":faction_relation", 0),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", -1),
				(val_add, ":faction_relation", -1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", -1),
				(val_add, ":faction_relation", -2),
			(try_end),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			##### QUEST CHECK FAILURE CONDITIONS #####
			(eq, ":function", floris_quest_failure_condition),
			(try_begin),
			  (check_quest_active, ":quest_no"),
			  (quest_get_slot, ":party_no", ":quest_no", slot_quest_target_party),
			  (neg|party_is_active, ":party_no"),
			  (quest_slot_eq, ":quest_no", slot_quest_current_state, qp3_escort_to_mine_begun),
			  (display_message, "@The prisoners you were escorting have been slain.", qp_error_color),
			  (call_script, "script_qp3_quest_escort_to_mine", floris_quest_fail),
			(try_end),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
]

from util_wrappers import *
from util_scripts import *

scripts_directives = [
	# HOOK: Inserts a script that tracks village entry.
	# [SD_OP_BLOCK_INSERT, "update_center_recon_notes", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		# [(call_script, "script_qp4_arrive_in_village", ":center_no"),], 1],
		
	# HOOK: Insert failure condition checks for quests that need them.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (try_begin), 0, 
		[(call_script, "script_qp3_check_failure_conditions", ":quest_no"),], 1],
		
	# HOOK: Inserts a script that forces hired mercenary companies to join the player in battle.
	[SD_OP_BLOCK_INSERT, "let_nearby_parties_join_current_battle", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (try_end), 0, 
		[
			(assign, reg41, ":party_no"),
			(call_script, "script_qp3_quest_mercenary_function", mercs_join_combat),
		], 1],
		
	# HOOK: Inserts a script that tracks village entry.
	[SD_OP_BLOCK_INSERT, "enter_court", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (assign, ":cur_pos", 16), 0, 
		[
			(call_script, "script_qp3_enter_court", ":center_no", ":cur_pos"),
			(assign, ":cur_pos", reg1),
		], 1],
		
	# HOOK: Inserts script into game_event_battle_end to check on types of enemies killed.
	[SD_OP_BLOCK_INSERT, "event_player_defeated_enemy_party", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp3_event_player_defeated_enemy_party"),], 1],
		
	# HOOK: Inserts the initializing scripts in game start as needed.
	[SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp3_game_start"),], 1],
		
	# HOOK: Inserts the names of quests I do not want humanitarian companions to object to failing.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"), 0, 
		[(call_script, "script_cf_qp3_ignore_failures", ":quest_no"),], 1],
		
	# HOOK: Captures when a player enters town.
	[SD_OP_BLOCK_INSERT, "game_event_party_encounter", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), 0, 
		[(call_script, "script_qp3_track_town_entry", "$g_encountered_party"),], 1],
		
	# HOOK: Prevent spawned bandits from joining nearby battles.
	# [SD_OP_BLOCK_INSERT, "let_nearby_parties_join_current_battle", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (neg|quest_slot_eq, "qst_troublesome_bandits", slot_quest_target_party, ":party_no"), 0, 
		# [(call_script, "script_cf_qp2_parties_that_wont_join_battles", ":party_no"),], 1],

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