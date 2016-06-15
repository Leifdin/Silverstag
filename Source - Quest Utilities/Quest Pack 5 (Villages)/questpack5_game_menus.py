# Quest Pack 5 (1.0) by Windyplains

from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_sounds import * # To support sf_looping actions.

from module_constants import *

####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#  
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The consequences are executed for the menu option that has been selected by the player.
#
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################

game_menus = [
	##### QUEST: CRAFTSMANS_KNOWLEDGE : BEGIN #####
	# PURPOSE: This menu will cover informing the player that a worker has been injured. (Stage 2)
	("qp5_craftsmans_knowledge",0,
		"Work Interruption^^All work on the {s0} comes to a halt as a loud crash is heard at the worksite.  {s22} to investigate, a number of your men are standing around {reg24?the body of :}{reg22?:one of your }{s21}{reg22?:s}.  It seems {reg21?she:he} {s23}",
		"none",
		[
			#(call_script, "script_change_party_morale", "p_main_party", -2),
			
			# Determine who the engineer is in the party.
			(quest_get_slot, ":engineer", "qst_qp5_craftsmans_knowledge", slot_quest_object_troop),
			(try_begin),
				(is_between, ":engineer", companions_begin, companions_end),
				(str_store_troop_name, s20, ":engineer"),
				(str_store_string, s22, "@You and {s20} hurry over"),
			(else_try),
				(str_store_string, s22, "@You head over"),
			(try_end),
			
			(party_get_num_companion_stacks, ":stack_limit", "p_main_party"),
			(store_sub, ":last_stack", ":stack_limit", 1),
			(try_for_range, ":stack_no", 1, ":stack_limit"),
				(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
				(neq, ":troop_no", ":engineer"),
				(neq, ":troop_no", "trp_player"), # shouldn't be possible anyway, but just in case.
				(store_random_in_range, ":roll", 0, 100),
				(this_or_next|lt, ":roll", 15),
				(eq, ":stack_no", ":last_stack"),
				(assign, ":injured_troop", ":troop_no"),
				(troop_get_type, reg21, ":injured_troop"),
				(str_store_troop_name, s21, ":injured_troop"),
				(assign, reg22, 0),
				(troop_is_hero, ":injured_troop"),
				(assign, reg22, 1),
				(break_loop),
			(try_end),
			
			# Determine extent of injury or death.
			(try_begin),
				### INJURY ###
				(store_random_in_range, ":roll", 0, 100),
				(this_or_next|lt, ":roll", 65),
				(troop_is_hero, ":injured_troop"),
				(assign, reg24, 0), # Tracks injury vs. death.
				# Pick a description.
				(store_random_in_range, ":string_no", "str_qp5_ck_injury_1", "str_qp5_ck_injury_end"),
				(str_store_string, s23, ":string_no"),
				# Injury the character.
				(try_begin),
					(troop_is_hero, ":injured_troop"),
					(store_troop_health, ":health", ":injured_troop"),
					(val_sub, ":health", 35),
					(val_max, ":health", 5),
					(troop_set_health, ":injured_troop", ":health"),
				(else_try),
					(party_wound_members, "p_main_party", ":injured_troop", 1),
				(try_end),
				
			(else_try),
				### DEATH ###
				(assign, reg24, 1), # Tracks injury vs. death.
				# Pick a description.
				(store_random_in_range, ":string_no", "str_qp5_ck_death_1", "str_qp5_ck_death_end"),
				(str_store_string, s23, ":string_no"),
				# Kill the character.
				(party_remove_members, "p_main_party", ":injured_troop", 1),
			(try_end),
			
			(quest_get_slot, ":building_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount),
			(party_get_slot, ":improvement_no", "$current_town", ":building_slot"),
			(call_script, "script_get_improvement_details", ":improvement_no"),
			
		],
		[
			("worker_injury_ignore", [], "Tell everyone to get back to work.",
				[
					(rest_for_hours_interactive, qp5_ck_pause_period * 1, 5, 0), #rest while not attackable
					(assign, "$g_town_visit_after_rest", 1),
					(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_target_state, 1), # Start building.
					(call_script, "script_change_party_morale", "p_main_party", -2),
					(change_screen_return),
				]),
			  
			("worker_injury_stop_work", 
				[
					(quest_get_slot, ":giver_troop", "qst_qp5_craftsmans_knowledge", slot_quest_giver_troop),
					(str_store_troop_name, s21, ":giver_troop"),
				], "Tell everyone to stop work while you go speak with {s21}.",
				[
					(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_worker_injury),
					(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
					(jump_to_menu, "mnu_village"),
				]),
		]),
	
	# PURPOSE: This menu pops up after working on the project for a little while when no incidents occur. (Stage 1 or 4)
	("qp5_craftsmans_knowledge_progress",0,
		"{reg21?Construction:{s20}'s} Report^^Work on the {s0} continues without incident.  {s21}^^{s22}",
		"none",
		[
			# Determine who the engineer is in the party.
			(quest_get_slot, ":engineer", "qst_qp5_craftsmans_knowledge", qst_qp5_craftsmans_knowledge),
			(str_store_troop_name, s20, ":engineer"),
			(store_add, reg21, ":engineer", 1), # Switch who is displayed.
			
			# Determine the improvement we're constructing.
			(quest_get_slot, ":building_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount),
			(party_get_slot, ":improvement_no", "$current_town", ":building_slot"),
			(call_script, "script_get_improvement_details", ":improvement_no"),
			
			# Figure out our time progress.
			(quest_get_slot, ":progress", "qst_qp5_craftsmans_knowledge", slot_quest_object_state),
			(store_div, ":quest_progress", ":progress", 100),
			(call_script, "script_building_slot_get_days_to_complete", "$current_town", ":building_slot"),
			(assign, ":days_left", reg1),
			
			(store_sub, reg22, ":days_left", ":quest_progress"),
			(store_sub, reg23, reg22, 1), # Plural check
			(try_begin),
				(eq, reg22, 0),
				(str_store_string, s21, "@{reg21?You estimate:{s20} reports} that construction right on schedule."),
			(else_try),
				(ge, reg22, 1),
				(str_store_string, s21, "@{reg21?You estimate:{s20} reports} that construction is roughly {reg22} day{reg23?s:} ahead of schedule."),
			(else_try),
				(lt, reg22, 0),
				(val_mul, reg22, -1), # Get rid of our negative.
				(str_store_string, s21, "@{reg21?You estimate:{s20} reports} that construction is roughly {reg22} day{reg23?s:} behind schedule."),
			(try_end),
			
			# Report how much time is left to continue construction.
			(assign, reg24, ":days_left"),
			(store_sub, reg25, reg24, 1),
			(str_store_string, s22, "@You have {reg24} day{reg25?s:} left to complete construction."),
			
			## Diagnostic
			# (assign, reg32, ":quest_progress"),
			# (str_store_string, s22, "@{s22}^DEBUG: You have {reg32} days of work left."),
		],
		[
			("work_continue", 
				[
					(quest_get_slot, ":building_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount),
					(party_get_slot, ":improvement_no", "$current_town", ":building_slot"),
					(try_begin),
						(eq, ":improvement_no", slot_center_has_crops_of_grain),
						(str_store_string, s29, "@Continue planting the fields."),
					(else_try),
						(str_store_string, s29, "@Continue on with the project."),
					(try_end),
				]
				, "{s29}",
				[
					(rest_for_hours_interactive, qp5_ck_pause_period * 1, 5, 0), #rest while not attackable
					(assign, "$g_town_visit_after_rest", 1),
					(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_target_state, 1), # Start building.
					(change_screen_return),
				]),
			  
			("use_townsfolk_only", 
				[
					(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_convince_value, 1),
				], "Stop having your men help with the project.",
				[
					(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_convince_value, 0),
					(jump_to_menu, "mnu_qp5_craftsmans_knowledge_progress"),
				]),
			  
			("use_soldiers_too", 
				[
					(neg|quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_convince_value, 1),
				], "Start using your own men to help with the project.",
				[
					(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_convince_value, 1),
					(jump_to_menu, "mnu_qp5_craftsmans_knowledge_progress"),
				]),
			  
			("work_stop", [], "Leave the worksite.",
				[
					(jump_to_menu, "mnu_village"),
				]),
		]),
	##### QUEST: CRAFTSMANS_KNOWLEDGE : END #####
 ]

from util_common import *
from util_wrappers import *

def modmerge_game_menus(orig_game_menus, check_duplicates = False):
	if( not check_duplicates ):
		orig_game_menus.extend(game_menus) # Use this only if there are no replacements (i.e. no duplicated item names)
		
		# QUEST: A CRAFTSMANS KNOWLEDGE (village)
		find_index = find_object(orig_game_menus, "village")
		orig_game_menus[find_index][5].insert(3,
			("qp5_q1_building_improvement",[
				(stop_all_sounds, 0),
				(party_slot_eq, "$current_town", slot_village_infested_by_bandits, 0),
				(party_slot_eq, "$current_town", slot_village_state, svs_normal),
				(check_quest_active, "qst_qp5_craftsmans_knowledge"),
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_center, "$current_town"),
				(this_or_next|quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_begun),
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_supplies_restored),
				(quest_get_slot, ":building_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount),
				(call_script, "script_building_slot_get_days_to_complete", "$current_town", ":building_slot"),
				(ge, reg1, 0),
				(assign, ":improvement", reg2),
				(call_script, "script_get_improvement_details", ":improvement"),
				(str_store_party_name, s13, "$current_town"),
				(try_begin),
					(eq, ":improvement", slot_center_has_crops_of_grain),
					(str_store_string, s29, "@Continue planting the fields."),
				(else_try),
					(str_store_string, s29, "@Continue work on the {s0}."),
				(try_end),
				],"{s29}", 
				[
					(rest_for_hours_interactive, qp5_ck_pause_period * 1, 5, 0), #rest while not attackable
					(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_target_state, 1), # Start building.
					(assign, "$g_town_visit_after_rest", 1),
					(change_screen_return),
					
				]),
			  )
		
		# QUEST: SENDING AID (village)
		find_index = find_object(orig_game_menus, "village")
		orig_game_menus[find_index][5].insert(3,
			("qp5_q2_deliver_supplies",
				[
					(party_slot_eq, "$current_town", slot_village_state, svs_looted),
					(check_quest_active, "qst_qp5_sending_aid"),
					(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_target_center, "$current_town"),
					(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_begun),
					# Name the village elder.
					(store_sub, ":center_offset", "$current_town", villages_begin),
					(store_add, ":mayor", ":center_offset", "trp_village_1_elder"),
					(str_store_troop_name, s21, ":mayor"),
				]
				,"Search for {s21} to deliver the supplies.", 
				[
					(party_get_slot, ":village_scene", "$current_town", slot_castle_exterior),
					(modify_visitors_at_site,":village_scene"),
					(reset_visitors),
					(party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
					(set_visitor, 11, ":village_elder_troop"),
					(set_jump_mission,"mt_village_center"),
					(jump_to_scene,":village_scene"),           
					(change_screen_map_conversation, ":village_elder_troop"),
				]),
			  )
	else:
	# Use the following loop to replace existing entries with same id
		for i in range (0,len(game_menus)-1):
			find_index = find_object(orig_game_menus, game_menus[i][0]); # find_object is from header_common.py
			if( find_index == -1 ):
				orig_game_menus.append(game_menus[i])
			else:
				orig_game_menus[find_index] = game_menus[i]
			
# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "game_menus"
        orig_game_menus = var_set[var_name_1]
        modmerge_game_menus(orig_game_menus)
        # find_i = list_find_first_match_i( orig_game_menus, "town_trade_assessment" )  
        # codeblock = GameMenuWrapper(orig_game_menus[find_i]).GetOpBlock()
        # line_i = codeblock.GetLength() - 2
        # codeblock.InsertBefore(line_i, hook_assessment_quest_initiation)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)