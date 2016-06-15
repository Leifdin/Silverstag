# Quest Pack 5 (1.0) by Windyplains

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

# script_cf_qp6_ignore_failures
# PURPOSE: These quests are not intended to trigger humanitarian companions complaining so they are added to the module_scripts exception list.
("cf_qp6_ignore_failures",
  [
		#(store_script_param, ":quest_no", 1),
		
		## NOTE: The quests that are commented out are included to show they were intentionally ommitted so as to cause objection.
		# (neq, ":quest_no", "qst_qp6_expanding_your_talents"),
		# (neq, ":quest_no", "qst_qp6_storekeeper_assignment"),
	]),
	
	
##############################################################################################################################################
############                                                   QUEST SCRIPTS                                                       ###########
##############################################################################################################################################

# script_qp6_quest_expanding_your_talents
# PURPOSE: Handles all quest specific actions for quest "qp6_expanding_your_talents".
("qp6_quest_expanding_your_talents",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_qp6_expanding_your_talents"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp6_q1_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Active states
		# QP6_QUEST_INACTIVE                              = 0
		# QP6_EYT_BEGUN                                   = 1
		# QP6_EYT_COMPLETED                               = 2
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            QP6_EYT_BEGUN),
			
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,          "trp_player"),              # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,                   "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_target_center,                  "$current_town"), # Already established.
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),               # No expiration.
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			# (quest_set_slot, ":quest_no", slot_quest_temp_slot,   PREVIOUSLY ASSIGNED), # We're tracking which level assignment the quest is for here.
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			
			(str_store_string, s61, "@You have reached the level necessary to assign a new ability.  This can be done by:\
									^ * Visiting the 'reports' menu.\
									^ * Going to the 'View Personal Reports' sub-menu.\
									^ * Selecting 'View Character Abilities'.\
									^ * Selecting an ability from the list on the right side.\
									^ * Clicking the 'Assign' button for an open slot."),
			# Clear out any old quest notes.
			(str_clear, s1),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", "trp_player", "str_qp6_q1_title"),
			
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
	
# script_qp6_storekeeper_assignment
# PURPOSE: Handles all quest specific actions for quest "qst_qp6_storekeeper_assignment".
("qp6_storekeeper_assignment",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_qp6_storekeeper_assignment"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp6_q1_title"),
		(str_store_string, s41, ":quest_title"),
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            QP6_QUEST_INACTIVE), # Stage is unnecessary.
			
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     "trp_player"),
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,                   "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_target_center,                  "$current_town"), # Already established.
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),               # No expiration.
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          0), # Enabling Storekeeper Purchasing option.
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          0), # Assigning an eligible companion.
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          0), # Visit the Shopping List.
			(quest_set_slot, ":quest_no", slot_quest_stage_4_trigger_chance,          0), # Visit the mod options page.
			
			(str_store_string, s61, "@You have not yet assigned a companion to the Storekeeper role.  You can do this by:\
									^ * Visiting the 'camp' menu.\
									^ * Going to the 'Companion Management' sub-menu.\
									^ * Selecting 'Assign Party Roles'.\
									^ * Check the box for 'Enable Storekeeper Purchasing'.\
									^ * At the Storekeeper menu select an eligible companion.\
									^ * Click the 'Shopping List' button to setup purchasing.\
									^ * Visit the 'Change Game Settings' page to setup a\
									^   'Minimum Cash to Maintain' value that suits you."),
									
			## Setup quest stage objectives.
			(str_store_string, s1, "@Objecive - Enable the Storekeeper purchasing option."),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0), # Enabling Storekeeper Purchasing option.
			(str_store_string, s1, "@Objective - Assign an eligible companion as your Storekeeper."),
			(add_quest_note_from_sreg, ":quest_no", 4, s1, 0), # Assigning an eligible companion.
			(str_store_string, s1, "@Objective - Visit the shopping list to setup purchasing limits."),
			(add_quest_note_from_sreg, ":quest_no", 5, s1, 0), # Visit the Shopping List.
			(str_store_string, s1, "@Objective - Setup a 'Minimum Cash to Maintain' setting on the mod options page."),
			(add_quest_note_from_sreg, ":quest_no", 6, s1, 0), # Visit the mod options page.
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", "trp_player", "str_qp6_q1_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			(assign, ":notify_of_update", 1),
			
			## SLOT 3 - Enabling Storekeeper Purchasing option.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_1_trigger_chance, 1),
				(str_store_string, s65, "@You have enabled your Storekeeper to automatically purchase food. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 3, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
			## SLOT 4 - Assigning an eligible companion.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_2_trigger_chance, 1),
				(str_store_string, s65, "@You have assigned an eligible companion as your Storekeeper. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 4, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
			## SLOT 5 - Visit the Shopping List.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_3_trigger_chance, 1),
				(str_store_string, s65, "@You have setup a shopping list for what your companion should buy. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 5, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
			## SLOT 6 - Visit the mod options page.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_4_trigger_chance, 1),
				(str_store_string, s65, "@You have setup a minimum cash value below which your Storekeeper will not buy food. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 6, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_4_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
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
			##### QUEST VICTORY CONDITIONS #####
			(eq, ":function", floris_quest_victory_condition),
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_1_trigger_chance, 2),
				(quest_slot_eq, ":quest_no", slot_quest_stage_2_trigger_chance, 2),
				(quest_slot_eq, ":quest_no", slot_quest_stage_3_trigger_chance, 2),
				(quest_slot_eq, ":quest_no", slot_quest_stage_4_trigger_chance, 2),
				(call_script, "script_qp6_storekeeper_assignment", floris_quest_succeed),
			(try_end),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp6_quartermaster_assignment
# PURPOSE: Handles all quest specific actions for quest "qst_qp6_quartermaster_assignment".
("qp6_quartermaster_assignment",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_qp6_quartermaster_assignment"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp6_q1_title"),
		(str_store_string, s41, ":quest_title"),
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            QP6_QUEST_INACTIVE), # Stage is unnecessary.
			
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     "trp_player"),
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,                   "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_target_center,                  "$current_town"), # Already established.
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),               # No expiration.
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          0), # Enabling Quartermaster Selling option.
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          0), # Assigning an eligible companion.
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          0), # Visit the mod options page.
			
			(str_store_string, s61, "@You have not yet assigned a companion to the Quartermaster role.  You can do this by:\
									^ * Visiting the 'camp' menu.\
									^ * Going to the 'Companion Management' sub-menu.\
									^ * Selecting 'Assign Party Roles'.\
									^ * Check the box for 'Enable Quartermaster Auto-Sell'.\
									^ * At the Quartermaster menu select an eligible companion.\
									^ * Visit the 'Change Game Settings' page to setup a\
									^   'Minimum Value for Pickup' setting that suits you."),
									
			## Setup quest stage objectives.
			(str_store_string, s1, "@Objecive - Enable the Quartermaster auto-selling option."),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0), # Enabling Quartermaster Purchasing option.
			(str_store_string, s1, "@Objective - Assign an eligible companion as your Quartermaster."),
			(add_quest_note_from_sreg, ":quest_no", 4, s1, 0), # Assigning an eligible companion.
			(str_store_string, s1, "@Objective - Setup a 'Minimum Value for Pickup' setting on the mod options page."),
			(add_quest_note_from_sreg, ":quest_no", 5, s1, 0), # Visit the mod options page.
			(str_clear, s1),
			(add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", "trp_player", "str_qp6_q1_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			(assign, ":notify_of_update", 1),
			
			## SLOT 3 - Enabling Quartermaster Auto-Sell option.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_1_trigger_chance, 1),
				(str_store_string, s65, "@You have enabled your Quartermaster to automatically sell battlefield loot. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 3, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
			## SLOT 4 - Assigning an eligible companion.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_2_trigger_chance, 1),
				(str_store_string, s65, "@You have assigned an eligible companion as your Quartermaster. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 4, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
			## SLOT 5 - Visit the mod options page.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_3_trigger_chance, 1),
				(str_store_string, s65, "@You have setup a minimum item value below which your Quartermaster will not loot it. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 5, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
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
			##### QUEST VICTORY CONDITIONS #####
			(eq, ":function", floris_quest_victory_condition),
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_1_trigger_chance, 2),
				(quest_slot_eq, ":quest_no", slot_quest_stage_2_trigger_chance, 2),
				(quest_slot_eq, ":quest_no", slot_quest_stage_3_trigger_chance, 2),
				(call_script, "script_qp6_quartermaster_assignment", floris_quest_succeed),
			(try_end),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp6_jailer_assignment
# PURPOSE: Handles all quest specific actions for quest "qst_qp6_jailer_assignment".
("qp6_jailer_assignment",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_qp6_jailer_assignment"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp6_q1_title"),
		(str_store_string, s41, ":quest_title"),
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            QP6_QUEST_INACTIVE), # Stage is unnecessary.
			
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     "trp_player"),
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,                   "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_target_center,                  "$current_town"), # Already established.
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),               # No expiration.
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          0), # Assigning an eligible companion.
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          0), # Setup operating mode.
			
			(str_store_string, s61, "@You have not yet assigned a companion to the Gaoler role.  You can do this by:\
									^ * Visiting the 'camp' menu.\
									^ * Going to the 'Companion Management' sub-menu.\
									^ * Selecting 'Assign Party Roles'.\
									^ * At the Gaoler menu select an eligible companion.\
									^ * Visit the 'Change Game Settings' page to setup a\
									^   'Party Gaoler Mode' setting that suits you."),
									
			## Setup quest stage objectives.
			(str_store_string, s1, "@Objective - Assign an eligible companion as your Quartermaster."),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0), # Assigning an eligible companion.
			(str_store_string, s1, "@Objective - Setup a 'Party Gaoler Mode' setting on the mod options page."),
			(add_quest_note_from_sreg, ":quest_no", 4, s1, 0), # Setup operating mode.
			(str_clear, s1),
			(add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", "trp_player", "str_qp6_q1_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			(assign, ":notify_of_update", 1),
			
			## SLOT 3 - Assigning an eligible companion.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_1_trigger_chance, 1),
				(str_store_string, s65, "@You have assigned an eligible companion as your Gaoler. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 3, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
			## SLOT 4 - Visit the mod options page.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_2_trigger_chance, 1),
				(str_store_string, s65, "@You have selected a 'Party Gaoler Mode' setting. (Completed)"),
				(str_store_string, s64, "@{s64}{s65}"),
				(add_quest_note_from_sreg, ":quest_no", 4, s64, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance, 2), # So it doesn't update again.
			(try_end),
			
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
			##### QUEST VICTORY CONDITIONS #####
			(eq, ":function", floris_quest_victory_condition),
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_stage_1_trigger_chance, 2),
				(quest_slot_eq, ":quest_no", slot_quest_stage_2_trigger_chance, 2),
				(call_script, "script_qp6_jailer_assignment", floris_quest_succeed),
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
	# # HOOK: Inserts a script that tracks village entry.
	# [SD_OP_BLOCK_INSERT, "update_center_recon_notes", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		# [(call_script, "script_qp5_arrive_in_village", ":center_no"),], 1],
	# # HOOK: Inserts the initializing scripts in game start as needed.
	# [SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		# [(call_script, "script_qp5_game_start"),], 1],
	# HOOK: Inserts the names of quests I do not want humanitarian companions to object to failing.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"), 0, 
		[(call_script, "script_cf_qp6_ignore_failures", ":quest_no"),], 1],
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