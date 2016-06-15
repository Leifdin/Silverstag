# Quest Pack 7 by Windyplains

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

# script_cf_qp7_ignore_failures
# These quests are not intended to trigger humanitarian companions complaining so they are added to the module_scripts exception list.
("cf_qp7_ignore_failures",
  [
		(store_script_param, ":quest_no", 1),
		
		(neq, ":quest_no", "qst_qp7_freemans_return"),
	]),
	
##############################################################################################################################################
############                                                   QUEST SCRIPTS                                                       ###########
##############################################################################################################################################

# script_qp7_quest_freemans_return
# PURPOSE: Handles all quest specific actions for quest "qst_qp7_freemans_return".
("qp7_quest_freemans_return",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_qp7_freemans_return"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp7_q1_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Active states
		# QP7_QUEST_INACTIVE                              = 0
		# QP7_AFR_BEGUN                                   = 1
		# QP7_AFR_COMPLETED                               = 2
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            QP7_AFR_BEGUN),
			
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,          "trp_player"),              # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,                   "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_target_center,                  "$current_town"), # Already established.
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),               # No expiration.
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_temp_slot,                       0),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			(quest_set_slot, ":quest_no", slot_quest_object_troop,                    "trp_freed_fugitive"),
			# Name the target village.
			(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
			(str_store_party_name_link, s11, ":target_center"),
			# Name the Nervous Man.
			(quest_get_slot, ":quest_target_dna", "qst_hunt_down_fugitive", slot_quest_target_dna),
			(call_script, "script_get_name_from_dna_to_s50", ":quest_target_dna"),
			(str_store_string, s12, s50),
			(str_store_string, s61, "@You have agreed to escort {s12} back to his home village of {s11}."),
			# Clear out any old quest notes.
			(str_clear, s1),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", "trp_player", "str_qp7_q1_title"),
			
		# (else_try),
			# ##### QUEST UPDATE #####
			# (eq, ":function", floris_quest_update),
			# # Get the date stamp.
			# (store_current_hours, ":cur_hours"),
			# (str_store_date, s64, ":cur_hours"),
			# (str_store_string, s64, "@[{s64}]: "),
			# # Special information needed.
			# (quest_get_slot, ":giver_troop", ":quest_no", slot_quest_giver_troop),
			# # Improvement
			# (quest_get_slot, ":target_village", ":quest_no", slot_quest_target_center),
			# (quest_get_slot, ":center_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount), # The center upgrade spot was hidden here.
			# (party_get_slot, ":improvement", ":target_village", ":center_slot"),
			# (call_script, "script_get_improvement_details", ":improvement"),
			# (str_store_string, s22, s0),
			# (str_store_troop_name, s21, ":giver_troop"),
			# (quest_get_slot, ":item_no", ":quest_no", slot_quest_primary_commodity),
			# (try_begin),
				# (ge, ":item_no", 1),
				# (str_store_item_name, s23, ":item_no"),
			# (try_end),
			# # Update quest notes as required.
			# (quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			# (assign, ":notify_of_update", 1),
			# (try_begin),
				# (eq, ":quest_stage", qp5_ck_worker_injury),
				# (str_store_string, s65, "@One of your men has been harmed during construction and you've had all work stopped until you speak to {s21}."),
				# (assign, ":note_slot", 3),
			# (else_try),
				# (eq, ":quest_stage", qp5_ck_begun),
				# (str_store_string, s65, "@Work on {s22} has resumed."),
				# (assign, ":note_slot", 3),
			# (else_try),
				# (eq, ":quest_stage", qp5_ck_supplies_being_obtained_by_villagers),
				# (str_store_string, s65, "@Work on the {s22} has stopped due to a shortage of {s23}.  You have had several villagers sent to acquire more."),
				# (assign, ":note_slot", 4),
				# (assign, ":notify_of_update", 0),
			# (else_try),
				# (eq, ":quest_stage", qp5_ck_supplies_being_obtained_by_player),
				# (quest_get_slot, ":target_center", ":quest_no", slot_quest_target_party),
				# (str_store_party_name_link, s24, ":target_center"),
				# (str_store_string, s65, "@Work on the {s22} has stopped due to a shortage of {s23} and you have chosen to travel to {s24} to acquire more."),
				# (assign, ":note_slot", 4),
			# (else_try),
				# (eq, ":quest_stage", qp5_ck_supplies_restored),
				# (str_store_string, s65, "@The shortage of {s23} has been resolved and work is now able to resume."),
				# (assign, ":note_slot", 4),
			# (else_try),
				# (eq, ":quest_stage", qp5_ck_work_completed),
				# (str_store_string, s65, "@The {s22} has been completed.  You should seek out {s21} to inform him."),
				# (assign, ":note_slot", 5),
			# (else_try),
				# (eq, ":quest_stage", qp5_ck_quest_failed),
				# (str_store_string, s65, "@You have failed to complete the {s22} in time.  You should seek out {s21} to inform him."),
				# (assign, ":note_slot", 5),
			# (else_try),
				# # Default error on failure to update note.
				# (display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			# (try_end),
			# # Update quest note.
			# (str_store_string, s64, "@{s64}{s65}"),
			# (add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			# (try_begin),
				# (eq, ":notify_of_update", 1),
				# (display_message, "str_quest_log_updated", gpu_light_blue),
			# (try_end),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", 250),
			(assign, ":town_relation", 2),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":town_relation", 1),
				(val_add, ":reward_xp", 100),
				(call_script, "script_change_player_honor", 1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":town_relation", 2),
				(val_add, ":reward_xp", 100),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Change town reputation.
			(quest_get_slot, ":quest_center", ":quest_no", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":town_relation"),
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
	

]

from util_wrappers import *
from util_scripts import *

scripts_directives = [
	# # HOOK: Inserts a script that tracks village entry.
	# [SD_OP_BLOCK_INSERT, "update_center_recon_notes", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		# [(call_script, "script_qp5_arrive_in_village", ":center_no"),], 1],
	# # HOOK: Inserts the initializing scripts in game start as needed.
	# [SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		# [(call_script, "script_qp5_game_start"),], 1],
	# HOOK: Inserts the names of quests I do not want humanitarian companions to object to failing.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"), 0, 
		[(call_script, "script_cf_qp7_ignore_failures", ":quest_no"),], 1],
	# # HOOK: Captures when a player enters town.
	# [SD_OP_BLOCK_INSERT, "game_event_party_encounter", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), 0, 
		# [(call_script, "script_qp5_track_town_entry", "$g_encountered_party"),], 1],
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