# Quest Pack 4 (1.0) by Windyplains

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

# script_qp4_start_quest
# INPUT: arg1 = quest_no, arg2 = giver_troop_no, s2 = description_text
# OUTPUT: none
("qp4_start_quest",
  [(store_script_param, ":quest_no", 1),
	(store_script_param, ":giver_troop_no", 2),
	
	(quest_set_slot, ":quest_no", slot_quest_giver_troop, ":giver_troop_no"),
	
	(try_begin),
	  (eq, ":giver_troop_no", -1),
	  (str_store_string, s63, "str_qp4_quest_title"),
	(else_try),
	  (is_between, ":giver_troop_no", active_npcs_begin, active_npcs_end),
	  (str_store_troop_name_link, s62, ":giver_troop_no"),
	  (str_store_string, s63, "@Given by: {s62}"),
	(else_try),
	  (str_store_troop_name, s62, ":giver_troop_no"),
	  (str_store_string, s63, "@Given by: {s62}"),
	(try_end),
	(store_current_hours, ":cur_hours"),
	(str_store_date, s60, ":cur_hours"),
	(str_store_string, s60, "@Given on: {s60}"),
	(add_quest_note_from_sreg, ":quest_no", 0, s60, 0),
	(add_quest_note_from_sreg, ":quest_no", 1, s63, 0),
	(add_quest_note_from_sreg, ":quest_no", 2, s61, 0),
	
	(try_begin),
	  (quest_slot_ge, ":quest_no", slot_quest_expiration_days, 1),
	  (quest_get_slot, reg20, ":quest_no", slot_quest_expiration_days),
	  (add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg20} days to finish this quest.", 0),
	(try_end),
	
	(start_quest, ":quest_no", ":giver_troop_no"),
	
	(display_message, "str_quest_log_updated"),
	]),
	
# script_cf_qp4_ignore_failures
# These quests are not intended to trigger humanitarian companions complaining so they are added to the module_scripts exception list.
# INPUT: none
# OUTPUT: none
("cf_qp4_ignore_failures",
  [
		(store_script_param, ":quest_no", 1),
		
		# Odval Story Line
		(neq, ":quest_no", "qst_odval_intro"),
		(neq, ":quest_no", "qst_odval_redemption"),
		(neq, ":quest_no", "qst_odval_return_to_tulbuk"),
		(neq, ":quest_no", "qst_odval_accept_the_challenge"),
		(neq, ":quest_no", "qst_odval_saving_face"),
		# Edwyn Story Line
		(neq, ":quest_no", "qst_edwyn_intro"),
		(neq, ":quest_no", "qst_edwyn_revenge"),
		(neq, ":quest_no", "qst_edwyn_first_knight"),
		(neq, ":quest_no", "qst_edwyn_second_knight"),
		(neq, ":quest_no", "qst_edwyn_third_knight"),
		
	]),
	
# script_qp4_add_storyline_characters
# Used by questpack4_mission_templates to see if a story line character needs to spawn in a scene.
# INPUT: none
# OUTPUT: none
("qp4_add_storyline_characters",
  [
		(assign, reg41, -1),
		(assign, reg42, -1),
		(assign, reg43, -1),
		(assign, reg44, -1),
		(assign, reg45, -1),
		(assign, reg46, -1),
		(assign, reg47, -1),
		(assign, reg48, -1),
		(assign, ":extra_companions", 0),
		
		# Clean out previous storyline characters.
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(troop_set_slot, ":troop_no", slot_troop_add_to_scene, 0),
		(try_end),
		
		##### ODVAL STORY ARC : BEGIN #####
		(try_begin),
			# If Odval_redemption is active then Odval always appears in home town scene.
			(check_quest_active, "qst_odval_redemption"),
			(eq, "$current_town", qp4_odval_home_town),
			(troop_set_slot, NPC_Odval, slot_troop_add_to_scene, 1),
			(check_quest_active, "qst_odval_return_to_tulbuk"),
			(troop_get_slot, ":troop_friend", NPC_Odval, slot_troop_personalitymatch_object),
			(is_between, ":troop_friend", companions_begin, companions_end),
			(troop_set_slot, ":troop_friend", slot_troop_add_to_scene, 1),
		(try_end),
		##### ODVAL STORY ARC : END #####
		
		##### EDWYN STORY ARC : BEGIN #####
		(try_begin),
			# If Odval_redemption is active then Odval always appears in home town scene.
			(check_quest_active, "qst_edwyn_revenge"),
			(party_get_slot, ":type", "$current_town", slot_party_type),
			(assign, ":pass", 0),
			(try_begin),
				(this_or_next|eq, ":type", spt_town),
				(eq, ":type", spt_village),
				(assign, ":pass", 1),
			(try_end),
			(try_begin),
				(eq, ":type", spt_bandit_lair),
				(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_current_state, qp4_edwyn_first_entered_lair),
				(assign, ":pass", 1),
			(try_end),
			(try_begin),
				(check_quest_active, "qst_edwyn_second_knight"),
				(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_arrived_in_town),
				(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance, "$current_town"),
				(assign, ":extra_companions", 4),
				(assign, ":pass", 1),
			(try_end),
			(try_begin),
				(check_quest_active, "qst_edwyn_third_knight"),
				(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_planning_to_kill_knight),
				(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_stage_2_trigger_chance, "$current_town"),
				(assign, ":pass", 0),
			(try_end),
			(eq, ":pass", 1),
			(troop_set_slot, NPC_Edwyn, slot_troop_add_to_scene, 1),
		(try_end),
		##### EDWYN STORY ARC : END #####
		
		# Extra companions requested
		(try_begin),
			(ge, ":extra_companions", 1),
			(assign, ":companions", 0),
			(party_get_num_companion_stacks, ":stack_limit", "p_main_party"),
			(try_for_range, ":stack_no", 1, ":stack_limit"),
				(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
				(troop_is_hero, ":troop_no"),
				(val_add, ":companions", 1),
				(le, ":companions", ":extra_companions"),
				(troop_set_slot, ":troop_no", slot_troop_add_to_scene, 1),
			(try_end),
		(try_end),
		
		# Setup the companions to add.
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(main_party_has_troop, ":troop_no"),
			(troop_slot_eq, ":troop_no", slot_troop_add_to_scene, 1),
			(try_begin),
				(eq, reg41, -1),
				(assign, reg41, ":troop_no"),
			(else_try),
				(eq, reg42, -1),
				(assign, reg42, ":troop_no"),
			(else_try),
				(eq, reg43, -1),
				(assign, reg43, ":troop_no"),
			(else_try),
				(eq, reg44, -1),
				(assign, reg44, ":troop_no"),
			(else_try),
				(eq, reg45, -1),
				(assign, reg45, ":troop_no"),
			(else_try),
				(eq, reg46, -1),
				(assign, reg46, ":troop_no"),
			(else_try),
				(eq, reg47, -1),
				(assign, reg47, ":troop_no"),
			(else_try),
				(eq, reg48, -1),
				(assign, reg48, ":troop_no"),
			(else_try),
				(display_message, "@ERROR - Too many story characters required to load them all."),
			(try_end),
			(troop_set_slot, ":troop_no", slot_troop_add_to_scene, 0),
			(ge, DEBUG_QUEST_PACK_4, 2),
			(str_store_troop_name, s31, ":troop_no"),
			(display_message, "@DEBUG (QP4): '{s31}' designated as a story character."),
		(try_end),
	]),
	
# script_qp4_track_town_entry
# Checks when the player enters a town using script "music_set_situation_with_culture" called in menu "town" to update quest stages as needed.
# INPUT: item_id
# OUTPUT: none
("qp4_track_town_entry",
  [
		(store_script_param, ":center_no", 1),
		
		# Store the time player arrived in town in hours.
		(store_current_hours, ":hours"),
		(party_set_slot, "p_main_party", slot_party_time_in_field, ":hours"),
		
		#### QUEST: EDWYN SECOND KNIGHT ### - Update quest stage if correct town entered.
		(try_begin),
			(check_quest_active, "qst_edwyn_second_knight"),
			(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_just_missed_him),
			(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance, ":center_no"),
			(call_script, "script_common_quest_change_state", "qst_edwyn_second_knight", qp4_edwyn_second_arrived_in_town),
			(call_script, "script_qp4_quest_edwyn_second_knight", floris_quest_update),
		(try_end),
	]),
	
# script_qp4_arrive_in_village
# INPUT: center_no
# OUTPUT: none
("qp4_arrive_in_village",
	[
		(store_script_param, ":center_no", 1),
		
		#### QUEST: EDWYN THIRD KNIGHT ### - Update quest stage if correct village entered.
		(try_begin),
			(check_quest_active, "qst_edwyn_third_knight"),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_not_here_check_nearby_village),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_stage_2_trigger_chance, ":center_no"),
			(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_arrival_in_village),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
		(try_end),
	]),
	 
# #script_qp2_spawn_bandit_party
# #INPUT:  none
# #OUTPUT: none
# ("qp2_spawn_bandit_party",
    # [
		# (set_spawn_radius, 2),
        # (spawn_around_party, "p_main_party", "pt_raider_party"),
        # (assign, ":bandit_party", reg0),
        # (party_set_slot, ":bandit_party", slot_party_commander_party, -1), #we need this because 0 is player's party!
        # (party_set_faction, ":bandit_party", "fac_outlaws"),
        # (party_set_ai_behavior, ":bandit_party", ai_bhvr_attack_party),
        # (party_clear, ":bandit_party"),
		# (store_character_level, ":tally", "trp_player"),
		# (try_for_range, ":unused", 0, 7),
			# (store_random_in_range, ":roll", 0, 4),
			# (val_add, ":tally", ":roll"),
		# (try_end),
		# (party_add_members, ":bandit_party", qp2_fortune_bandit_troop, ":tally"),
    # ]),
	
# # script_cf_qp2_parties_that_wont_join_battles
# # The following parties will be ignored when directed to join a nearby battle.
# # INPUT:  item_id
# # OUTPUT: none
# ("cf_qp2_parties_that_wont_join_battles",
  # [
		# (store_script_param, ":party_no", 1),
		
		# # QUEST: Fortune Favors the Bold
		# # (this_or_next|neg|check_quest_active, "qst_floris_trade_fortune_favors_bold"),
		# # (neg|quest_slot_eq, "qst_floris_trade_fortune_favors_bold", slot_quest_target_party, ":party_no"), ##
		
		# # Merchant Rivals in the field
		# (party_stack_get_troop_id, ":troop_no", ":party_no", 0),
		# (neg|is_between, ":troop_no", qp2_trade_rivals_begin, qp2_trade_rivals_end),
		
	# ]),

# script_qp4_game_start
# Contains all initialization scripts needed for Quest Pack 4.
# INPUT:  none
# OUTPUT: none
("qp4_game_start",
  [
		# Setup initial pre-define for $quest_reactions
		#(assign, "$quest_reactions", QUEST_REACTIONS_HIGH),
		#(troop_raise_skill, "trp_player", "skl_persuasion", 4),
		
		# Define the story arc quests for each companion after setting all of them to -1 as a default.
		(try_for_range, ":troop_no", companions_begin, companions_end),
			(troop_set_slot, ":troop_no", slot_troop_story_arc_quest, -1),
		(try_end),
		(troop_set_slot, NPC_Odval, slot_troop_story_arc_quest, "qst_odval_redemption"),
		
		(try_begin),
			(ge, DEBUG_QUEST_PACK_4, 1),
			(display_message, "@DEBUG (QP4): Quest Pack 4 initialized.  Story lines set."),
		(try_end),
	]),

########################################################################################################################################################
####################                                                ODVAL STORY LINE                                                ####################
########################################################################################################################################################
# script_qp4_quest_odval_intro
# Handles all quest specific actions for quest "odval_intro".
# INPUT: none
# OUTPUT: none
("qp4_quest_odval_intro",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_odval_intro"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_odval_home_town),
		(str_store_troop_name, s14, NPC_Odval),
		(troop_get_type, reg3, NPC_Odval),
		(assign, ":quest_title", "str_qp4_odval_intro_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp4_odval_intro_inactive                        = 0
		# qp4_odval_intro_story_heard                     = 1
		# qp4_odval_intro_agreed_to_help                  = 2  # Quest Success
		# qp4_odval_intro_refused_to_help                 = 3  # Quest Failure
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_odval_home_town),
			(str_store_string, s61,       "str_qp4_odval_intro_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_odval_intro_inactive),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Odval),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_odval_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 5),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_odval_intro_story_heard),
				(str_store_string, s65, "@You have listened to {s14}'s story now you must decide if you will help {reg3?her:him} or not."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_odval_intro_agreed_to_help),
				(str_store_string, s65, "@You have agreed to help {s14} clear {reg3?her:his} name."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_odval_intro_refused_to_help),
				(str_store_string, s65, "@You have refused to help {s14} clear {reg3?her:his} name."),
				(assign, ":note_slot", 4),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			#(display_message, "str_quest_log_updated"),
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(add_xp_as_reward, 100),
			# Odval joins the party for free.
			(neg|main_party_has_troop, NPC_Odval),  # Make sure NPC isn't already in the party.
			(hero_can_join, "p_main_party"),        # Does the party have space?
			# (party_add_members, "p_main_party", NPC_Odval, 1),
			# (troop_set_slot, NPC_Odval, slot_troop_occupation, slto_player_companion),
			# (str_store_troop_name, s14, NPC_Odval),
			# (display_message, "@{s14} has joined your party."),
			(call_script, "script_recruit_troop_as_companion", NPC_Odval),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(troop_set_slot, NPC_Odval, slot_troop_intro_quest_complete, floris_story_arc_failed),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp4_quest_odval_redemption
# Handles all quest specific actions for quest "odval_redemption".
# INPUT: none
# OUTPUT: none
("qp4_quest_odval_redemption",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_odval_redemption"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_odval_home_town),
		(str_store_troop_name, s14, NPC_Odval),
		(troop_get_type, reg3, NPC_Odval),
		(assign, ":quest_title", "str_qp4_odval_redemption_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp4_odval_redemption_inactive                   = 0
		# qp4_odval_redemption_return_to_tulbuk_done      = 1
		# qp4_odval_redemption_accept_the_challenge_done  = 2
		# qp4_odval_redemption_saving_face_done           = 3
		# qp4_odval_redemption_success                    = 4 # Quest Success
		# qp4_odval_redemption_failure                    = 5 # Quest Failure
		# qp4_odval_redemption_success_via_bribe          = 6 # Quest Success
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_odval_home_town),
			(str_store_string, s61,       "str_qp4_odval_redemption_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_odval_redemption_inactive),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Odval),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_odval_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_odval_redemption_return_to_tulbuk_done),
				(str_store_string, s65, "@Part I Complete - You have met with the village elder in {s13}."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_odval_redemption_accept_the_challenge_done),
				(str_store_string, s65, "@Part II Complete - You have faced down {s14}'s accusers in martial combat."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_odval_redemption_saving_face_done),
				(str_store_string, s65, "@Part III Complete - You have faced {s14} in personal combat."),
				(assign, ":note_slot", 5),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(quest_set_slot, ":quest_no", slot_quest_current_state, qp4_odval_redemption_success),
			# Rewards
			(assign, ":reward_xp", 4000),
			(assign, ":reward_relation", 10),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", 3000),
				(val_add, ":reward_relation", 10),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", 3000),
				(val_add, ":reward_relation", 5),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Odval, ":reward_relation"),
			(add_xp_to_troop, ":reward_xp", NPC_Odval),
			(troop_set_slot, NPC_Odval, slot_troop_intro_quest_complete, floris_story_arc_success_lite), # Default value.
			(add_quest_note_from_sreg, ":quest_no", 7, "@You have successfully completed this quest.", 0),
			(try_begin),
				# Set Odval as a permanent companion member.
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(troop_set_slot, NPC_Odval, slot_troop_intro_quest_complete, floris_story_arc_successful),
			(try_end),
			## SILVERSTAG EMBLEMS+ ##
			(call_script, "script_emblem_award_to_player", 5), # emblem_scripts.py
			## SILVERSTAG EMBLEMS- ##
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(quest_set_slot, ":quest_no", slot_quest_current_state, qp4_odval_redemption_failure),
			(troop_set_slot, NPC_Odval, slot_troop_intro_quest_complete, floris_story_arc_failed),
			(add_quest_note_from_sreg, ":quest_no", 7, "@You have failed to redeem {s14} in the eyes of {reg3?her:his} kin.", 0),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			##### QUEST STORY ARC CONDITIONAL FAILURE #####
			(eq, ":function", floris_quest_story_arc_check),

			# Figure out how many quests were completed vs. successfully completed.
			(assign, ":quests_succeeded", 0),
			(assign, ":quests_completed", 0),
			(try_begin),
				(check_quest_succeeded, "qst_odval_return_to_tulbuk"),
				(val_add, ":quests_succeeded", 1),
			(try_end),
			(try_begin),
				(check_quest_finished, "qst_odval_return_to_tulbuk"),
				(val_add, ":quests_completed", 1),
			(try_end),
			(try_begin),
				(check_quest_succeeded, "qst_odval_accept_the_challenge"),
				(val_add, ":quests_succeeded", 1),
			(try_end),
			(try_begin),
				(check_quest_finished, "qst_odval_accept_the_challenge"),
				(val_add, ":quests_completed", 1),
			(try_end),
			(try_begin),
				(check_quest_succeeded, "qst_odval_saving_face"),
				(val_add, ":quests_succeeded", 1),
			(try_end),
			(try_begin),
				(check_quest_finished, "qst_odval_saving_face"),
				(val_add, ":quests_completed", 1),
			(try_end),
			
			# Check if minimum successful quest requirements are met.
			(try_begin),
				(assign, ":failure", 0),
				# 1 Quest Completed.
				(ge, ":quests_completed", 1),
				(assign, ":failure", 1),                          # 1 quest done, 1 quest uncertain.
				(ge, ":quests_succeeded", 1),
				(assign, ":failure", 0),                          # 1 quest done, 1 done successfully.
				# 2 Quests Completed.
				(ge, ":quests_completed", 2),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM), # 2 successful quests required.
				(assign, ":failure", 1),                          # 2 quest done, 1 done successfully, 1 quest uncertain.
				(ge, ":quests_succeeded", 2),
				(assign, ":failure", 0),                          # 2 quest done, 2 done successfully.
				# 3 Quests Completed.
				(ge, ":quests_completed", 3),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),   # 3 successful quests required.
				(assign, ":failure", 1),                          # 3 quests done, 2 done successfully, 1 quest uncertain.
				(ge, ":quests_succeeded", 3),
				(assign, ":failure", 0),                          # 3 quests done, 3 done successfully.
			(try_end),
			(try_begin),
				(eq, ":failure", 1),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(display_message, "@{s14}'s story arc meets the conditions to fail."),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(assign, reg20, ":quests_succeeded"),
				(assign, reg21, ":quests_completed"),
				(display_message, "@DEBUG (QP4): {reg20} successful quests of {reg21} quests completed."),
			(try_end),
			(assign, reg1, ":failure"),
			
		(else_try),
			##### QUEST RESET DURATION #####
			(eq, ":function", floris_quest_reset_duration),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days, 30),
			(try_begin),
				(check_quest_finished, "qst_odval_accept_the_challenge"),
				(quest_set_slot, ":quest_no", slot_quest_expiration_days, 5),
			(try_end),
			(quest_get_slot, reg20, ":quest_no", slot_quest_expiration_days),
			(add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg20} days to finish this quest.", 0),
		
		(else_try),
			##### QUEST STORYLINE FAILURE CONSEQUENCES #####
			(eq, ":function", floris_quest_storyline_failure),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Odval leaves the party and becomes a bandit.
			(display_message, "@{s14} has left the party.", qp_error_color),
			(party_remove_members, "p_main_party", NPC_Odval, 1),
			(troop_set_slot, NPC_Odval, slot_troop_occupation, 0),
			# Setup bandit spawn trigger.
			# trp_steppe_bandit_hero should be replaced as Odval and activated as needed.
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp4_quest_odval_return_to_tulbuk
# Handles all quest specific actions for quest "odval_return_to_tulbuk".
# INPUT: none
# OUTPUT: none
("qp4_quest_odval_return_to_tulbuk",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_odval_return_to_tulbuk"),
		(assign, ":quest_title", "str_qp4_odval_return_to_tulbuk_title"),
		(str_store_string, s41, ":quest_title"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_odval_home_town),
		(str_store_troop_name, s14, NPC_Odval),
		(troop_get_type, reg3, NPC_Odval),
		
		# Quest Stages
		# qp4_odval_return_to_tulbuk_inactive             = 0
		# qp4_odval_return_to_tulbuk_odval_joined_party   = 1
		# qp4_odval_return_to_tulbuk_accepted_challenge   = 2
		# qp4_odval_return_to_tulbuk_refused_challenge    = 3
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_odval_home_town),
			(str_store_string, s61,       "str_qp4_odval_return_to_tulbuk_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_odval_return_to_tulbuk_odval_joined_party),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Odval),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_odval_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_odval_return_to_tulbuk_accepted_challenge),
				(str_store_string, s65, "@You have met with the village elder in {s14}'s home town.  After a confrontation with two other townsfolk {s14} demanded the right of contest to defeat {reg3?her:his} challengers with you as {reg3?her:his} companion.  You have agreed to help {reg3?her:him} in this matter."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_odval_return_to_tulbuk_refused_challenge),
				(str_store_string, s65, "@You have met with the village elder in {s14}'s home town.  After a confrontation with two other townsfolk {s14} demanded the right of contest to defeat {reg3?her:his} challengers with you as {reg3?her:his} companion, but you refused to take part in the match."),
				(assign, ":note_slot", 3),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", qp4_companion_subquest_low_xp_reward),
			(assign, ":reward_relation", qp4_companion_subquest_low_relation_reward),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", qp4_companion_subquest_med_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_med_relation_reward),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", qp4_companion_subquest_high_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_high_relation_reward),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Odval, ":reward_relation"),
			(add_xp_to_troop, ":reward_xp", NPC_Odval),
			# Reset duration on main story arc
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_reset_duration),
			# Move main story arc along.
			(quest_set_slot, "qst_odval_redemption", slot_quest_current_state, qp4_odval_redemption_return_to_tulbuk_done),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_update),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Move main story arc along.
			(quest_set_slot, "qst_odval_redemption", slot_quest_current_state, qp4_odval_redemption_return_to_tulbuk_done),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_update),
			# Check conditions for story arc failure.
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_story_arc_check),
			(try_begin),
				(eq, reg1, 1), # Failed Story Arc
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_fail),
			(else_try),
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_succeed),
			(try_end),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp4_quest_odval_accept_the_challenge
# Handles all quest specific actions for quest "odval_accept_the_challenge".
# INPUT: none
# OUTPUT: none
("qp4_quest_odval_accept_the_challenge",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_odval_accept_the_challenge"),
		(assign, ":quest_title", "str_qp4_odval_accept_the_challenge_title"),
		(str_store_string, s41, ":quest_title"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_odval_home_town),
		(str_store_troop_name, s14, NPC_Odval),
		(troop_get_type, reg3, NPC_Odval),
		
		# Quest Stages
		# qp4_odval_accept_the_challenge_inactive             = 0
		# qp4_odval_accept_the_challenge_challenge_accepted   = 1
		# qp4_odval_accept_the_challenge_challenge_begun      = 2
		# qp4_odval_accept_the_challenge_challenge_won        = 3
		# qp4_odval_accept_the_challenge_challenge_lost       = 4 # Quest Failure
		# qp4_odval_accept_the_challenge_challenge_complete   = 5 # Quest Success
		# qp4_odval_accept_the_challenge_odval_fell           = 6
		# qp4_odval_accept_the_challenge_odval_fell_not_okay  = 7 # Quest Failure
		# qp4_odval_accept_the_challenge_odval_fell_but_okay  = 8 # Quest Success, but Arc doesn't continue.
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_odval_home_town),
			(str_store_string, s61,       "str_qp4_odval_accept_the_challenge_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_odval_accept_the_challenge_challenge_accepted),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Odval),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_odval_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_odval_accept_the_challenge_challenge_begun),
				(str_store_string, s65, "@You and {s14} have returned to face {reg3?her:his} accusers in a contest of arms."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_odval_accept_the_challenge_challenge_won),
				(str_store_string, s65, "@You have emerged victorious against {reg3?her:his} accusers and should now speak with the village elder."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_odval_accept_the_challenge_challenge_lost),
				(str_store_string, s65, "@{s14} has failed to beat {reg3?her:his} accusers and has been exiled from {s13}.  Due to {reg3?her:his} willingness to face judgement {reg3?she:he} has been spared {reg3?her:his} life."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_odval_accept_the_challenge_odval_fell_not_okay),
				(str_store_string, s65, "@{s14} was knocked out during the contest making a poor performance of {reg?her:his} ability.  The village elder views this as proof {reg3?she:he} would not have been able to win without cheating."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp4_odval_accept_the_challenge_odval_fell_but_okay),
				(str_store_string, s65, "@{s14} was knocked out during the contest making a poor performance of {reg?her:his} ability.  The elder has listened to your arguements and feels she has sufficiently cleared her name."),
				(assign, ":note_slot", 5),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", qp4_companion_subquest_low_xp_reward),
			(assign, ":reward_relation", qp4_companion_subquest_low_relation_reward),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", qp4_companion_subquest_med_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_med_relation_reward),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", qp4_companion_subquest_high_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_high_relation_reward),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Odval, ":reward_relation"),
			(add_xp_to_troop, ":reward_xp", NPC_Odval),
			# Reset duration on main story arc
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_reset_duration),
			# Move main story arc along.
			(quest_set_slot, "qst_odval_redemption", slot_quest_current_state, qp4_odval_redemption_accept_the_challenge_done),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_update),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Move main story arc along.
			(quest_set_slot, "qst_odval_redemption", slot_quest_current_state, qp4_odval_redemption_accept_the_challenge_done),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_update),
			# Check conditions for story arc failure.
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_story_arc_check),
			(try_begin),
				(eq, reg1, 1), # Failed Story Arc
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_fail),
			(else_try),
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_succeed),
			(try_end),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp4_quest_odval_saving_face
# Handles all quest specific actions for quest "odval_saving_face".
# INPUT: none
# OUTPUT: none
("qp4_quest_odval_saving_face",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_odval_saving_face"),
		(assign, ":quest_title", "str_qp4_odval_saving_face_title"),
		(str_store_string, s41, ":quest_title"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_odval_home_town),
		(str_store_troop_name, s14, NPC_Odval),
		(troop_get_type, reg3, NPC_Odval),
		
		# Quest Stages
		# qp4_odval_saving_face_inactive                  = 0
		# qp4_odval_saving_face_challenge_accepted        = 1
		# qp4_odval_saving_face_challenge_begun           = 2
		# qp4_odval_saving_face_challenge_won             = 3 # Quest failure.
		# qp4_odval_saving_face_challenge_lost            = 4 # Quest success.
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_odval_home_town),
			(str_store_string, s61,       "str_qp4_odval_saving_face_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_odval_saving_face_challenge_accepted),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Odval),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_odval_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 5),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_odval_saving_face_challenge_accepted),
				(str_store_string, s65, "@You and {s14} have returned to prove {s14}'s worth in martial combat."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_odval_saving_face_challenge_won),
				(str_store_string, s65, "@You have emerged victorious in the contest proving {s14} was not the warrior {reg3?she:he} claimed to be.  While {reg3?her:his} accusers were beaten many will likely feel {reg3?she:he} should have been exiled."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_odval_saving_face_challenge_lost),
				(str_store_string, s65, "@You have fallen to {s14} in combat allowing {reg3?her:him} to prove {reg3?her:his} worth before {reg3?her:his} people and clear {reg3?her:his} reputation."),
				(assign, ":note_slot", 4),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
	
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", qp4_companion_subquest_low_xp_reward),
			(assign, ":reward_relation", qp4_companion_subquest_low_relation_reward),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", qp4_companion_subquest_med_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_med_relation_reward),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", qp4_companion_subquest_high_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_high_relation_reward),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Odval, ":reward_relation"),
			(add_xp_to_troop, ":reward_xp", NPC_Odval),
			# Reset duration on main story arc
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_reset_duration),
			# Move main story arc along.
			(quest_set_slot, "qst_odval_redemption", slot_quest_current_state, qp4_odval_redemption_saving_face_done),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_update),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Move main story arc along.
			(quest_set_slot, "qst_odval_redemption", slot_quest_current_state, qp4_odval_redemption_saving_face_done),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_update),
			# Check conditions for story arc failure.
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_story_arc_check),
			(try_begin),
				(eq, reg1, 1), # Failed Story Arc
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_fail),
			(else_try),
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_succeed),
			(try_end),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
		
# script_qp4_odval_store_final_comment_to_s2
# Figure out a good information source for to use in dialogs then store it to s2.
# INPUT: none
# OUTPUT: s2 (epilogue comment)
("qp4_odval_store_final_comment_to_s2",
  [
		(assign, ":relation_hit", 0),
		(str_clear, s2),
		(str_store_party_name, s13, qp4_odval_home_town),
		(str_store_troop_name, s14, NPC_Odval),
		
		(try_begin),
			##### SUCCESS COMMENTS #####
			(check_quest_succeeded, "qst_odval_redemption"),
			(try_begin),
				# (3/3) You let Odval win the final duel.
				(check_quest_succeeded, "qst_odval_saving_face"),
				(str_store_string, s2, "str_qp4_redemp_success_odval_won_duel"),
				
			(else_try),
				# (2/3) You defeated Odval in the final duel.
				(check_quest_failed, "qst_odval_saving_face"),
				(str_store_string, s2, "str_qp4_redemp_success_odval_lost_duel"),
				(assign, ":relation_hit", -5),
				
			(else_try),
				# (2/3) You and Odval won, but you didn't agree to accept the duel.
				(check_quest_succeeded, "qst_odval_accept_the_challenge"),
				(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_complete),
				(str_store_string, s2, "str_qp4_redemp_success_player_refused_duel"),
				
			(else_try),
				# (2/3) You and Odval won, she was knocked out and it is okay.
				(check_quest_succeeded, "qst_odval_accept_the_challenge"),
				(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_odval_fell_but_okay),
				(str_store_string, s2, "str_qp4_redemp_success_odval_wounded_but_okay"),
				(assign, ":relation_hit", -5),
				
			(else_try),
				# (1/3) You and Odval lost the challenge.
				(check_quest_failed, "qst_odval_accept_the_challenge"),
				(str_store_string, s2, "str_qp4_redemp_success_player_lost_challenge"),
			(try_end),
			
		(else_try),
			##### FAILURE COMMENTS #####
			(check_quest_failed, "qst_odval_redemption"),
			(try_begin),
				# (2/3) You defeated Odval in the final duel.
				(check_quest_failed, "qst_odval_saving_face"),
				(str_store_string, s2, "str_qp4_redemp_failure_odval_lost_duel"),
				(assign, ":relation_hit", -40),
				
			(else_try),
				# (2/3) You and Odval won, but you didn't agree to accept the duel.
				(check_quest_succeeded, "qst_odval_accept_the_challenge"),
				(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_complete),
				(str_store_string, s2, "str_qp4_redemp_failure_player_refused_duel"),
				(assign, ":relation_hit", -20),
				
			(else_try),
				# (2/3) You and Odval won, she was knocked out and it is okay.
				(check_quest_succeeded, "qst_odval_accept_the_challenge"),
				(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_odval_fell_but_okay),
				(str_store_string, s2, "str_qp4_redemp_failure_odval_wounded_not_okay"),
				(assign, ":relation_hit", 0),
				
			(else_try),
				# (1/3) You and Odval won, she was knocked out and it is not okay.
				(check_quest_succeeded, "qst_odval_accept_the_challenge"),
				(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_odval_fell_not_okay),
				(str_store_string, s2, "str_qp4_redemp_failure_odval_wounded_not_okay"),
				(assign, ":relation_hit", 0),
				
			(else_try),
				# (1/3) You and Odval lost the challenge.
				(check_quest_failed, "qst_odval_accept_the_challenge"),
				(str_store_string, s2, "str_qp4_redemp_failure_player_lost_challenge"),
				#(str_store_string, s2, "@I cannot believe those horse-faced farmers beat us back there!  I can never go back to {s13} unless I want to find myself tied to a stake and stoned within an inch of my life as an example.  A fine mess your help made of all of this!  I will find my own way from here on out."),
				(assign, ":relation_hit", -20),
				
			(else_try),
				# (0/3) You refused to stand with Odval in the challenge.
				(check_quest_failed, "qst_odval_return_to_tulbuk"),
				(str_store_string, s2, "str_qp4_redemp_failure_player_refused_challenge"),
				(assign, ":relation_hit", -40),
			(try_end),
			
		(else_try),
			##### COMMENT ERROR #####
			(str_store_party_name, s13, qp4_odval_home_town),
			(assign, reg30, "$quest_reactions"),
			(quest_get_slot, reg31, "qst_odval_return_to_tulbuk", slot_quest_current_state),
			(quest_get_slot, reg32, "qst_odval_accept_the_challenge", slot_quest_current_state),
			(quest_get_slot, reg33, "qst_odval_saving_face", slot_quest_current_state),
			(str_store_string, s2, "@STORY ARC QUEST COMMENT ERROR: {s13}^This should not be seen.^Quest Reaction: {reg30}^^Quest Stages:^Return To Tulbuk @ {reg31}^Accept the Challenge @ {reg32}^Saving Face @ {reg33}^^Please send a screenshot of this dialog to the Floris Team."),
		(try_end),
		(assign, reg52, ":relation_hit"),
	]),

########################################################################################################################################################
####################                                                ODVAL STORY LINE                                                ####################
########################################################################################################################################################

########################################################################################################################################################
####################                                                EDWYN STORY LINE                                                ####################
########################################################################################################################################################
# script_qp4_quest_edwyn_intro
# Handles all quest specific actions for quest "edwyn_intro".
# INPUT: none
# OUTPUT: none
("qp4_quest_edwyn_intro",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_edwyn_intro"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_edwyn_home_town),
		(str_store_troop_name, s14, NPC_Edwyn),
		(troop_get_type, reg3, NPC_Edwyn),
		(assign, ":quest_title", "str_qp4_edwyn_intro_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp4_edwyn_intro_inactive                        = 0
		# qp4_edwyn_intro_story_heard                     = 1
		# qp4_edwyn_intro_agreed_to_help                  = 2   # Quest Success
		# qp4_edwyn_intro_refused_to_help                 = 3   # Quest Failure
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_edwyn_home_town),
			(str_store_string, s61,       "str_qp4_edwyn_intro_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_edwyn_intro_inactive),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Edwyn),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_edwyn_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 5),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_edwyn_intro_story_heard),
				(str_store_string, s65, "@You have listened to {s14}'s story now you must decide if you will help {reg3?her:him} or not."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_intro_agreed_to_help),
				(str_store_string, s65, "@You have agreed to help {s14} clear {reg3?her:his} name."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_intro_refused_to_help),
				(str_store_string, s65, "@You have refused to help {s14} clear {reg3?her:his} name."),
				(assign, ":note_slot", 4),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			#(display_message, "str_quest_log_updated"),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(add_xp_as_reward, 100),
			# Odval joins the party for free.
			(neg|main_party_has_troop, NPC_Edwyn),  # Make sure NPC isn't already in the party.
			(hero_can_join, "p_main_party"),        # Does the party have space?
			(party_add_members, "p_main_party", NPC_Edwyn, 1),
			(troop_set_slot, NPC_Edwyn, slot_troop_occupation, slto_player_companion),
			(str_store_troop_name, s14, NPC_Edwyn),
			(display_message, "@{s14} has joined your party."),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(troop_set_slot, NPC_Edwyn, slot_troop_intro_quest_complete, floris_story_arc_failed),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),

# script_qp4_quest_edwyn_revenge
# Handles all quest specific actions for quest "edwyn_revenge".
# INPUT: none
# OUTPUT: none
("qp4_quest_edwyn_revenge",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_edwyn_revenge"),
		(assign, ":quest_title", "str_qp4_edwyn_revenge_title"),
		(str_store_string, s41, ":quest_title"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_edwyn_home_town),
		(str_store_troop_name, s14, NPC_Edwyn),
		(troop_get_type, reg3, NPC_Edwyn),
		
		# Quest Stages
		# qp4_edwyn_revenge_inactive                      = 0
		# qp4_edwyn_revenge_begun                         = 1
		# qp4_edwyn_revenge_one_knight_done               = 2
		# qp4_edwyn_revenge_two_knights_done              = 3
		# qp4_edwyn_revenge_three_knights_done            = 4
		# qp4_edwyn_revenge_success                       = 5   # Quest Success
		# qp4_edwyn_revenge_failure                       = 6   # Quest Failure

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_edwyn_home_town),
			(str_store_string, s61,       "str_qp4_edwyn_revenge_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_edwyn_revenge_begun),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Edwyn),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_edwyn_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 90),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			# Add the subquests to the main story quest notes.
			(add_quest_note_from_sreg, ":quest_no", 3, "@Help Edwyn kill Sir Tenry.", 0),
			(add_quest_note_from_sreg, ":quest_no", 4, "@Help Edwyn kill Sir Henric.", 0),
			(add_quest_note_from_sreg, ":quest_no", 5, "@Help Edwyn kill Sir Gerrin.", 0),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(try_begin),
				(check_quest_succeeded, "qst_edwyn_first_knight"),
				(neg|check_quest_finished, "qst_edwyn_first_knight"),
				(complete_quest, "qst_edwyn_first_knight"),
				(str_store_party_name_link, s12, "$current_town"),
				(str_store_string, s65, "@Sir Tenry - In {s12}, you learned that Sir Tenry had been exiled from the band of knights and turned bandit.  You successfully tracked him to their lair and assassinated him."),
				(assign, ":note_slot", 3),
			(else_try),
				(check_quest_failed, "qst_edwyn_first_knight"),
				(neg|check_quest_finished, "qst_edwyn_first_knight"),
				(complete_quest, "qst_edwyn_first_knight"),
				(str_store_string, s65, "@Sir Tenry - You learned that Sir Tenry had been exiled from the band of knights and turned bandit.  You attacked him at his lair, but failed to eliminate him."),
				(assign, ":note_slot", 3),
			(else_try),
				(check_quest_succeeded, "qst_edwyn_second_knight"),
				(neg|check_quest_finished, "qst_edwyn_second_knight"),
				(complete_quest, "qst_edwyn_second_knight"),
				(quest_get_slot, ":target_center", "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance),
				(str_store_party_name_link, s17, ":target_center"),
				(str_store_string, s65, "@Sir Henric - After tracing his path over the last month, you found Sir Henric in the town of {s17} before putting an end to him."),
				(assign, ":note_slot", 4),
			(else_try),
				(check_quest_failed, "qst_edwyn_second_knight"),
				(neg|check_quest_finished, "qst_edwyn_second_knight"),
				(complete_quest, "qst_edwyn_second_knight"),
				(quest_get_slot, ":target_center", "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance),
				(str_store_party_name_link, s17, ":target_center"),
				(str_store_string, s65, "@Sir Henric - You tracked Sir Henric to the town of {s17}, but were unable to kill him."),
				(assign, ":note_slot", 4),
			(else_try),
				(check_quest_succeeded, "qst_edwyn_third_knight"),
				(neg|check_quest_finished, "qst_edwyn_third_knight"),
				(complete_quest, "qst_edwyn_third_knight"),
				(quest_get_slot, ":target_center", "qst_edwyn_third_knight", slot_quest_stage_2_trigger_chance),
				(try_begin),
					(str_clear, s18),
					(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_convinced_edwyn_to_spare_knight),
					(str_store_string, s18, "@  After listening to the elder's pleas that the town would be in danger if Sir Gerrin was killed you and {s14} have agreed it is for the best to let him live."),
				(else_try),
					(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_knight_is_slain),
					(str_store_string, s18, "@  Upon the knight's next visit to the town you and your allies confronted his party and left him slain."),
				(try_end),
				(str_store_party_name_link, s17, ":target_center"),
				(str_store_string, s65, "@Sir Gerrin - Rumors of a knight matching Sir Gerrin's description has led you to the village of {s17} where you find that he and his companions have been extorting supplies from the village.{s18}"),
				(assign, ":note_slot", 5),
			(else_try),
				(check_quest_failed, "qst_edwyn_third_knight"),
				(neg|check_quest_finished, "qst_edwyn_third_knight"),
				(complete_quest, "qst_edwyn_third_knight"),
				(quest_get_slot, ":target_center", "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance),
				(try_begin),
					(str_clear, s18),
					(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_allowed_knight_to_live),
					(str_store_string, s18, "@  After listening to the elder's pleas that the town would be in danger if Sir Gerrin was killed you have agreed it is for the best to let him live.  {s14} disagrees and intends to go after him alone."),
				(else_try),
					(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_knight_lives_on),
					(str_store_string, s18, "@  You and your allies attacked Sir Gerrin's party unsuccessfully resulting in the knight escaping."),
				(else_try),
					(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_knight_is_slain),
					(str_store_string, s18, "@  You and your allies attacked Sir Gerrin's party killing him in the process, but failed to protect the villagers as promised."),
				(try_end),
				(str_store_party_name_link, s17, ":target_center"),
				(str_store_string, s65, "@Sir Gerrin - Rumors of a knight matching Sir Gerrin's description has led you to the village of {s17} where you find that he and his companions have been extorting supplies from the village.{s18}"),
				(assign, ":note_slot", 5),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(quest_set_slot, ":quest_no", slot_quest_current_state, qp4_edwyn_revenge_success),
			# Rewards
			(assign, ":reward_xp", 4000),
			(assign, ":reward_relation", 10),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", 3000),
				(val_add, ":reward_relation", 10),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", 3000),
				(val_add, ":reward_relation", 5),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Edwyn, ":reward_relation"),
			(add_xp_to_troop, ":reward_xp", NPC_Edwyn),
			(troop_set_slot, NPC_Edwyn, slot_troop_intro_quest_complete, floris_story_arc_success_lite), # Default value.
			(add_quest_note_from_sreg, ":quest_no", 7, "@You have successfully completed this quest.", 0),
			(try_begin),
				# Set companion as a permanent member.
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(troop_set_slot, NPC_Edwyn, slot_troop_intro_quest_complete, floris_story_arc_successful),
			(try_end),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(quest_set_slot, ":quest_no", slot_quest_current_state, qp4_edwyn_revenge_failure),
			(troop_set_slot, NPC_Edwyn, slot_troop_intro_quest_complete, floris_story_arc_failed),
			(add_quest_note_from_sreg, ":quest_no", 7, "@You have failed to help {s14} avenge {reg3?her:his} family.", 0),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			##### QUEST STORY ARC CONDITIONAL FAILURE #####
			(eq, ":function", floris_quest_story_arc_check),

			# Figure out how many quests were completed vs. successfully completed.
			(assign, ":quests_succeeded", 0),
			(assign, ":quests_completed", 0),
			(try_begin),
				(check_quest_succeeded, "qst_edwyn_first_knight"),
				(val_add, ":quests_succeeded", 1),
			(try_end),
			(try_begin),
				(check_quest_finished, "qst_edwyn_first_knight"),
				(val_add, ":quests_completed", 1),
			(try_end),
			(try_begin),
				(check_quest_succeeded, "qst_edwyn_second_knight"),
				(val_add, ":quests_succeeded", 1),
			(try_end),
			(try_begin),
				(check_quest_finished, "qst_edwyn_second_knight"),
				(val_add, ":quests_completed", 1),
			(try_end),
			(try_begin),
				(check_quest_succeeded, "qst_edwyn_third_knight"),
				(val_add, ":quests_succeeded", 1),
			(try_end),
			(try_begin),
				(check_quest_finished, "qst_edwyn_third_knight"),
				(val_add, ":quests_completed", 1),
			(try_end),
			
			# Check if minimum successful quest requirements are met.
			(try_begin),
				(assign, ":failure", 0),
				# 1 Quest Completed.
				(ge, ":quests_completed", 1),
				(assign, ":failure", 1),                          # 1 quest done, 1 quest uncertain.
				(ge, ":quests_succeeded", 1),
				(assign, ":failure", 0),                          # 1 quest done, 1 done successfully.
				# 2 Quests Completed.
				(ge, ":quests_completed", 2),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM), # 2 successful quests required.
				(assign, ":failure", 1),                          # 2 quest done, 1 done successfully, 1 quest uncertain.
				(ge, ":quests_succeeded", 2),
				(assign, ":failure", 0),                          # 2 quest done, 2 done successfully.
				# 3 Quests Completed.
				(ge, ":quests_completed", 3),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),   # 3 successful quests required.
				(assign, ":failure", 1),                          # 3 quests done, 2 done successfully, 1 quest uncertain.
				(ge, ":quests_succeeded", 3),
				(assign, ":failure", 0),                          # 3 quests done, 3 done successfully.
			(try_end),
			(try_begin),
				(eq, ":failure", 1),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(display_message, "@{s14}'s story arc meets the conditions to fail."),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(assign, reg20, ":quests_succeeded"),
				(assign, reg21, ":quests_completed"),
				(display_message, "@DEBUG (QP4): {reg20} successful quests of {reg21} quests completed."),
			(try_end),
			(assign, reg1, ":failure"),
			
		# (else_try),
			# ##### QUEST RESET DURATION #####
			# (eq, ":function", floris_quest_reset_duration),
			# (quest_set_slot, ":quest_no", slot_quest_expiration_days, 30),
			# # (try_begin),
				# # (check_quest_finished, "qst_odval_accept_the_challenge"),
				# # (quest_set_slot, ":quest_no", slot_quest_expiration_days, 5),
			# # (try_end),
			# (quest_get_slot, reg20, ":quest_no", slot_quest_expiration_days),
			# (add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg20} days to finish this quest.", 0),
		
		(else_try),
			##### QUEST STORYLINE FAILURE CONSEQUENCES #####
			(eq, ":function", floris_quest_storyline_failure),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Edwyn leaves the party and dies in the attempt if the failed quest the third_knight, otherwise lives.
			(display_message, "@{s14} has left the party.", qp_error_color),
			(party_remove_members, "p_main_party", NPC_Edwyn, 1),
			(troop_set_slot, NPC_Edwyn, slot_troop_occupation, 0),
			# Clean up quests from the log.
			(store_add, ":upper_limit", "qst_edwyn_third_knight", 1),
			(try_for_range, ":quest_to_remove", "qst_edwyn_first_knight", ":upper_limit"),
				(try_begin),
					(this_or_next|check_quest_succeeded, ":quest_to_remove"),
					(check_quest_failed, ":quest_to_remove"),
					(complete_quest, ":quest_to_remove"),
				(else_try),
					(check_quest_active, ":quest_to_remove"),
					(cancel_quest, ":quest_to_remove"),
				(try_end),
			(try_end),
			# Determine Edwyn's fate.
			# Edwyn will die attempting to finish the quest on his own.
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp4_quest_edwyn_first_knight
# Handles all quest specific actions for quest "edwyn_first_knight".
# INPUT: none
# OUTPUT: none
("qp4_quest_edwyn_first_knight",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_edwyn_first_knight"),
		(assign, ":quest_title", "str_qp4_edwyn_first_knight_title"),
		(str_store_string, s41, ":quest_title"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_edwyn_home_town),
		(str_store_troop_name, s14, NPC_Edwyn),
		(troop_get_type, reg3, NPC_Edwyn),
		
		# Quest Stages
		# qp4_edwyn_first_inactive                        = 0
		# qp4_edwyn_first_begun                           = 1
		# qp4_edwyn_first_learn_about_knight              = 2
		# qp4_edwyn_first_learn_of_lair_location          = 3
		# qp4_edwyn_first_found_lair_on_map               = 4
		# qp4_edwyn_first_entered_lair                    = 5
		# qp4_edwyn_first_conversation                    = 6
		# qp4_edwyn_first_knight_is_slain                 = 7   # Quest Success
		# qp4_edwyn_first_knight_lives_on                 = 8   # Quest Failure
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_edwyn_home_town),
			(str_store_string, s61,       "str_qp4_edwyn_first_knight_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_edwyn_first_begun),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Edwyn),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_edwyn_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 90),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Find a first town.
			(call_script, "script_qus_select_random_center", center_is_town, 30, 100, "p_main_party"),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance, reg1),
			(assign, ":first_town", reg1),
			# Find a second town.
			(call_script, "script_qus_select_random_center", center_is_any, 5, 15, ":first_town"),
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance, reg1),
			# Find a bandit lair.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_edwyn_first_learn_about_knight),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_1_trigger_chance),
				(str_store_party_name_link, s15, ":center_no"),
				(str_store_string, s65, "@You learn that Sir Tenry was exiled from the knight order for disloyalty and has become a bandit.  The person you spoke with wasn't sure of his exact location, but believed he traveled to the lands near {s15}."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_first_learn_of_lair_location),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_2_trigger_chance),
				(str_store_party_name_link, s16, ":center_no"),
				(party_get_slot, reg5, ":center_no", slot_party_type),
				(assign, reg4, 0),
				(try_begin),
					(eq, reg5, spt_village),
					(assign, reg4, 1),
				(try_end),
				(str_store_string, s65, "@You've learned of a bandit lair nearby to the {reg4?village:town} of {s16} that may be where Sir Tenry is hiding out."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_first_found_lair_on_map),
				(str_store_string, s65, "@You have found the location of the bandit lair."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_first_entered_lair),
				(str_store_string, s65, "@You found the location of Sir Tenry's lair and entered to find the exiled knight."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_first_knight_is_slain),
				(str_store_string, s65, "@After dispatching his fellow bandits you and {s14} put Sir Tenry to the sword leaving his corpse to rot."),
				(assign, ":note_slot", 6),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_first_knight_lives_on),
				(str_store_string, s65, "@Your company attempted to defeat the bandits, but Sir Tenry was able to escape your trap and disappear into the wilderness."),
				(assign, ":note_slot", 6),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			# Rewards
			(assign, ":reward_xp", qp4_companion_subquest_low_xp_reward),
			(assign, ":reward_relation", qp4_companion_subquest_low_relation_reward),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", qp4_companion_subquest_med_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_med_relation_reward),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", qp4_companion_subquest_high_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_high_relation_reward),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Edwyn, ":reward_relation"),
			(add_xp_to_troop, ":reward_xp", NPC_Edwyn),
			# Reset duration on main story arc
			#(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_reset_duration),
			# Move main story arc along.
			(quest_get_slot, ":stage", "qst_edwyn_revenge", slot_quest_current_state),
			(val_add, ":stage", 1),
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_current_state, ":stage"),
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_update),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			# Move main story arc along.
			(quest_get_slot, ":stage", "qst_edwyn_revenge", slot_quest_current_state),
			(val_add, ":stage", 1),
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_current_state, ":stage"),
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_update),
			# Check conditions for story arc failure.
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_story_arc_check),
			(try_begin),
				(eq, reg1, 1), # Failed Story Arc
				(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_fail),
			(else_try),
				(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_succeed),
			(try_end),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp4_quest_edwyn_second_knight
# Handles all quest specific actions for quest "edwyn_second_knight".
# INPUT: none
# OUTPUT: none
("qp4_quest_edwyn_second_knight",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_edwyn_second_knight"),
		(assign, ":quest_title", "str_qp4_edwyn_second_knight_title"),
		(str_store_string, s41, ":quest_title"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_edwyn_home_town),
		(str_store_troop_name, s14, NPC_Edwyn),
		(troop_get_type, reg3, NPC_Edwyn),
		
		# Quest Stages
		# qp4_edwyn_second_inactive                       = 0
		# qp4_edwyn_second_begun                          = 1
		# qp4_edwyn_second_learn_of_location              = 2
		# qp4_edwyn_second_just_missed_him                = 3
		# qp4_edwyn_second_arrived_in_town                = 4
		# qp4_edwyn_second_knight_confrontation           = 5
		# qp4_edwyn_second_knight_is_slain                = 6   # Quest Success
		# qp4_edwyn_second_knight_lives_on                = 7   # Quest Failure

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_edwyn_home_town),
			(str_store_string, s61,       "str_qp4_edwyn_second_knight_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_edwyn_second_begun),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Edwyn),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_edwyn_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 90),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Find a first town.
			(call_script, "script_qus_select_random_center", center_is_town, 30, 100, "p_main_party"),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance, reg1),
			(assign, ":starting_point", reg1),
			# Find a second town.
			(call_script, "script_qus_select_random_center", center_is_town, 25, 50, ":starting_point"),
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance, reg1),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_edwyn_second_learn_of_location),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_1_trigger_chance),
				(str_store_party_name_link, s15, ":center_no"),
				(str_store_string, s65, "@Asking around you've learned that Sir Henric passed through here a month ago on his way to {s15}."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_second_just_missed_him),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_1_trigger_chance),
				(str_store_party_name_link, s15, ":center_no"),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_2_trigger_chance),
				(str_store_party_name_link, s16, ":center_no"),
				(str_store_string, s65, "@It seems you've just missed Sir Henric in {s15} by a couple of weeks.  You learn he is believed to have been headed towards {s16}."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_second_arrived_in_town),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_2_trigger_chance),
				(str_store_party_name_link, s16, ":center_no"),
				(str_store_string, s65, "@You have arrived in {s16} where folks claim to have recently seen the wayward knight walking the streets."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_second_knight_is_slain),
				(str_store_string, s65, "@After a bloody battle in the streets you've slain Sir Henric and left him behind in the street."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_second_knight_lives_on),
				(str_store_string, s65, "@You and your allies attempted to defeat Sir Henric, but he was able to best your group and escape the scene."),
				(assign, ":note_slot", 5),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			# Rewards
			(assign, ":reward_xp", qp4_companion_subquest_low_xp_reward),
			(assign, ":reward_relation", qp4_companion_subquest_low_relation_reward),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", qp4_companion_subquest_med_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_med_relation_reward),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", qp4_companion_subquest_high_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_high_relation_reward),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Edwyn, ":reward_relation"),
			(add_xp_to_troop, ":reward_xp", NPC_Edwyn),
			# Reset duration on main story arc
			#(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_reset_duration),
			# Move main story arc along.
			(quest_get_slot, ":stage", "qst_edwyn_revenge", slot_quest_current_state),
			(val_add, ":stage", 1),
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_current_state, ":stage"),
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_update),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			# Move main story arc along.
			(quest_get_slot, ":stage", "qst_edwyn_revenge", slot_quest_current_state),
			(val_add, ":stage", 1),
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_current_state, ":stage"),
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_update),
			# Check conditions for story arc failure.
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_story_arc_check),
			(try_begin),
				(eq, reg1, 1), # Failed Story Arc
				(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_fail),
			(else_try),
				(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_succeed),
			(try_end),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp4_quest_edwyn_third_knight
# Handles all quest specific actions for quest "edwyn_third_knight".
# INPUT: none
# OUTPUT: none
("qp4_quest_edwyn_third_knight",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_edwyn_third_knight"),
		(assign, ":quest_title", "str_qp4_edwyn_third_knight_title"),
		(str_store_string, s41, ":quest_title"),
		# Get specific string data.
		(str_store_party_name, s13, qp4_edwyn_home_town),
		(str_store_troop_name, s14, NPC_Edwyn),
		(troop_get_type, reg3, NPC_Edwyn),
		
		# Quest Stages
		# qp4_edwyn_third_inactive                        = 0
		# qp4_edwyn_third_begun                           = 1
		# qp4_edwyn_third_last_seen_location              = 2
		# qp4_edwyn_third_not_here_check_nearby_village   = 3
		# qp4_edwyn_third_arrival_in_village              = 4
		# qp4_edwyn_third_learned_story_from_elder        = 5
		# qp4_edwyn_third_allowed_knight_to_live          = 6   # Quest Failure, good for village.
		# qp4_edwyn_third_convinced_edwyn_to_spare_knight = 7   # Quest Success, good for village.
		# qp4_edwyn_third_planning_to_kill_knight         = 8
		# qp4_edwyn_third_knight_is_slain                 = 9   # Quest Success, but bad for village.
		# qp4_edwyn_third_knight_lives_on                 = 10  # Quest Failure

		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, qp4_edwyn_home_town),
			(str_store_string, s61,       "str_qp4_edwyn_third_knight_quest_text"),
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_edwyn_third_begun),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     NPC_Edwyn),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    qp4_edwyn_home_town),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 90),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance,         0), # used to track if expiration warnings have been made.
			# Find a first town.
			(call_script, "script_qus_select_random_center", center_is_town, 45, 100, "p_main_party"),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance, reg1),
			(assign, ":starting_point", reg1),
			# Find a second town.
			(call_script, "script_qus_select_random_center", center_is_village, 5, 15, ":starting_point"),
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance, reg1),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_qp4_start_quest", ":quest_no", -1),
			
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
				(eq, ":quest_stage", qp4_edwyn_third_last_seen_location),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_1_trigger_chance),
				(str_store_party_name_link, s15, ":center_no"),
				(str_store_string, s65, "@No one here seems to know of the location of a Sir Gerrin, but someone heard his name when they passed through {s15} last."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_third_not_here_check_nearby_village),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_1_trigger_chance),
				(str_store_party_name_link, s15, ":center_no"),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_2_trigger_chance),
				(str_store_party_name_link, s16, ":center_no"),
				(str_store_string, s65, "@Checking around in the town of {s15} you hear of a band of knights that are regularly seen in the village of {s16}."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_third_arrival_in_village),
				(quest_get_slot, ":center_no", ":quest_no", slot_quest_stage_2_trigger_chance),
				(str_store_party_name_link, s16, ":center_no"),
				(str_store_string, s65, "@You have arrived in the village of {s16}, but there doesn't appear to be any trace of Sir Gerrin.  You should speak to the village elder."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_third_learned_story_from_elder),
				(str_store_string, s65, "@The village elder of {s16} tells you that Sir Gerrin and his knights make regular visits to the town to extort supplies for their band.  He pleads with you not to kill the knights as it would be blamed upon his village."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_third_allowed_knight_to_live),
				(str_store_string, s65, "@You decided for the good of the village to let Sir Gerrin live, but {s14} has felt betrayed by this decision and intends to go after him alone."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_third_convinced_edwyn_to_spare_knight),
				(str_store_string, s65, "@You and {s14} have decided for the good of the village to let Sir Gerrin live.  You've successfully convinced {reg3?her:him} that you couldn't leave the village at the mercy of the knights' wrath."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_third_planning_to_kill_knight),
				(str_store_string, s65, "@Regardless of the situation in the village, you and {s14} plan to hunt down Sir Gerrin and eliminate him."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_third_knight_is_slain),
				(str_store_string, s65, "@Sir Gerrin and his knights have been eliminated."),
				(assign, ":note_slot", 6),
			(else_try),
				(eq, ":quest_stage", qp4_edwyn_third_knight_lives_on),
				(str_store_string, s65, "@You failed to kill Sir Gerrin and allowed him to leave the village alive."),
				(assign, ":note_slot", 6),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_qp4_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			# Rewards
			(assign, ":reward_xp", qp4_companion_subquest_low_xp_reward),
			(assign, ":reward_relation", qp4_companion_subquest_low_relation_reward),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", qp4_companion_subquest_med_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_med_relation_reward),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", qp4_companion_subquest_high_xp_reward),
				(val_add, ":reward_relation", qp4_companion_subquest_high_relation_reward),
			(try_end),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Edwyn, ":reward_relation"),
			(add_xp_to_troop, ":reward_xp", NPC_Edwyn),
			# Reset duration on main story arc
			#(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_reset_duration),
			# Move main story arc along.
			(quest_get_slot, ":stage", "qst_edwyn_revenge", slot_quest_current_state),
			(val_add, ":stage", 1),
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_current_state, ":stage"),
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_update),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			# Move main story arc along.
			(quest_get_slot, ":stage", "qst_edwyn_revenge", slot_quest_current_state),
			(val_add, ":stage", 1),
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_current_state, ":stage"),
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_update),
			# Check conditions for story arc failure.
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_story_arc_check),
			(try_begin),
				(eq, reg1, 1), # Failed Story Arc
				(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_fail),
			(else_try),
				(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_succeed),
			(try_end),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_qp4_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp4_store_informant_to_s2
# Figure out a good information source for to use in dialogs then store it to s2.
# INPUT: none
# OUTPUT: none
("qp4_store_informant_to_s2",
  [
		(store_random_in_range, reg2, 0, 3),
		(try_begin),	
			(eq, reg2, 0), 
			(str_store_string, s2, "@tavern keeper"),
		(else_try),		
			(eq, reg2, 1), 
			(str_store_string, s2, "@guard"),
		(else_try),		
			(eq, reg2, 2), 
			(str_store_string, s2, "@storekeeper"),
		(try_end),		
	]),
	
# script_qp4_edwyn_store_final_comment_to_s2
# Figure out a good information source for to use in dialogs then store it to s2.
# INPUT: none
# OUTPUT: s2 (epilogue comment)
("qp4_edwyn_store_final_comment_to_s2",
  [
		(assign, ":relation_hit", 0),
		# Check status of "EDWYN FIRST KNIGHT"
		(try_begin),
			(check_quest_succeeded, "qst_edwyn_first_knight"),
			(assign, ":first_knight_good", 1),
		(else_try),
			(assign, ":first_knight_good", 0),
			(val_add, ":relation_hit", 10),
		(try_end),
		
		# Check status of "EDWYN SECOND KNIGHT"
		(try_begin),
			(check_quest_succeeded, "qst_edwyn_second_knight"),
			(assign, ":second_knight_good", 1),
		(else_try),
			(assign, ":second_knight_good", 0),
			(val_add, ":relation_hit", 10),
		(try_end),
		
		# Check status of "EDWYN THIRD KNIGHT"
		(try_begin),
			(check_quest_succeeded, "qst_edwyn_third_knight"),
			(assign, ":third_knight_good", 1),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_convinced_edwyn_to_spare_knight),
			(assign, ":third_knight_good", 2),
		(else_try),
			(assign, ":third_knight_good", 0),
			(val_add, ":relation_hit", 10),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_allowed_knight_to_live),
			(assign, ":third_knight_good", -1),
			(val_add, ":relation_hit", 10),
		(try_end),
		
		(str_clear, s3), # General comment on revenge quest.
		(str_clear, s4), # Comment about Sir Tenry's quest.
		(str_clear, s5), # Comment about Sir Henric's quest.
		(str_clear, s6), # Comment about Sir Gerrin's quest.
		
		(try_begin),
			##### SUCCESS COMMENTS #####
			(check_quest_succeeded, "qst_edwyn_revenge"),
			(str_store_string, s3, "@M'{Lord/Lady} {playername}, I have to admit that I was not entirely sure you'd see it through, but you sure proved your word to me."),
			# EDWYN_FIRST_KNIGHT
			(try_begin),
				(eq, ":first_knight_good", 1),
				(str_store_string, s4, "@  Figures that Sir Tenry would have become a rogue, but we gave him what all rogues deserve, didn't we?"),
			(try_end),
			# EDWYN_SECOND_KNIGHT
			(try_begin),
				(eq, ":second_knight_good", 1),
				(quest_get_slot, reg13, "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance),
				(str_store_party_name, s13, reg13),
				(str_store_string, s5, "@  And that was a great brawl we had back in {s13}."),
			(try_end),
			# EDWYN_THIRD_KNIGHT
			(try_begin),
				(eq, ":third_knight_good", 1),
				(quest_get_slot, reg13, "qst_edwyn_third_knight", slot_quest_stage_2_trigger_chance),
				(str_store_party_name, s13, reg13),
				(str_store_string, s6, "@  Not to mention driving those bastards out of {s13}!"),
			(else_try),
				(eq, ":third_knight_good", 2),
				(str_store_string, s6, "@  I am not sure how I feel about letting Sir Gerrin escape, but it wouldn't have been right setting those villagers up to take the fall."),
			(try_end),
			(str_store_string, s2, "@{s3}{s4}{s5}{s6}  Just wanted you to know that you've found a loyal friend in me."),
			
		(else_try),
			##### FAILURE COMMENTS #####
			(check_quest_failed, "qst_edwyn_revenge"),
			(str_store_string, s3, "@M'{Lord/Lady} {playername}, you convinced me to follow you on the road with the promise of helping me put an end to those bastards that killed my family, but that didn't happen, did it?"),
			# EDWYN_FIRST_KNIGHT
			(try_begin),
				(eq, ":first_knight_good", 0),
				(str_store_string, s4, "@  You let that damned rogue, Tenry, escape."),
			(try_end),
			# EDWYN_SECOND_KNIGHT
			(try_begin),
				(eq, ":second_knight_good", 0),
				(quest_get_slot, reg13, "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance),
				(str_store_party_name, s13, reg13),
				(str_store_string, s5, "@  Back in {s13} we had Henric cornered, but we ran because of a few guards?."),
			(try_end),
			# EDWYN_THIRD_KNIGHT
			(try_begin),
				(quest_get_slot, reg13, "qst_edwyn_third_knight", slot_quest_stage_2_trigger_chance),
				(str_store_party_name, s13, reg13),
				(eq, ":third_knight_good", 0),
				(str_store_string, s6, "@  We even failed to drive Gerrin's order out of {s13}!"),
			(else_try),
				(eq, ":third_knight_good", -1),
				(str_store_string, s6, "@  Worst of all you betrayed me in {s13}."),
			(try_end),
			(str_store_string, s2, "@{s3}{s4}{s5}{s6}  I'm done supporting your aims as you sure didn't help mine."),
			
		(else_try),
			##### COMMENT ERROR #####
			(assign, reg3, ":first_knight_good"),
			(str_store_string, s4, "@Sir Tenry's Quest = {reg3?Success:Failure}"),
			(assign, reg3, ":second_knight_good"),
			(str_store_string, s5, "@Sir Henric's Quest = {reg3?Success:Failure}"),
			(try_begin),
				(ge, ":third_knight_good", 1),
				(str_store_string, s6, "@Sir Gerrin's Quest = Success"),
			(else_try),
				(str_store_string, s6, "@Sir Gerrin's Quest = Failure"),
			(try_end),
			(str_store_string, s2, "@This is an error comment that should not be seen.^^CONDITIONS:^{s4}^{s5}^{s6}^^Please send a screenshot of this dialog to the Floris Team."),
		(try_end),
		(assign, reg52, ":relation_hit"),
	]),
########################################################################################################################################################
####################                                                EDWYN STORY LINE                                                ####################
########################################################################################################################################################
]

from util_wrappers import *
from util_scripts import *

scripts_directives = [
	# HOOK: Inserts a script that tracks village entry.
	[SD_OP_BLOCK_INSERT, "update_center_recon_notes", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp4_arrive_in_village", ":center_no"),], 1],
	# HOOK: Inserts the initializing scripts in game start as needed.
	[SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp4_game_start"),], 1],
	# HOOK: Inserts the names of quests I do not want humanitarian companions to object to failing.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"), 0, 
		[(call_script, "script_cf_qp4_ignore_failures", ":quest_no"),], 1],
	# HOOK: Captures when a player enters town.
	[SD_OP_BLOCK_INSERT, "game_event_party_encounter", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), 0, 
		[(call_script, "script_qp4_track_town_entry", "$g_encountered_party"),], 1],
	# HOOK: Prevent loyal companions from complaining about fellow party members.
	[SD_OP_BLOCK_INSERT, "post_battle_personality_clash_check", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (troop_get_slot, ":other_npc", ":npc", slot_troop_personalityclash2_object), 0, 
		[(neg|troop_slot_eq, ":npc", slot_troop_intro_quest_complete, 1),], 1],
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