# Center Improvements (1.0) by Windyplains

from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from module_constants import *

game_menus = [
###########################################################################################################################
#####                                               COMMON MENU CODE                                                  #####
###########################################################################################################################

	("cancel_construction_confirm", 0, "{s23} Management^^{s21}^^What do you wish to cancel construction of?", "none",
		[
			# Menu code begins.
			#(assign, ":num_improvements", 0),
			 (str_clear, s18),
			 (try_begin),
			   (party_slot_eq, "$g_encountered_party", slot_party_type, spt_village),
			   (str_store_string, s17, "@village"),
			   (str_store_string, s20, "@The villagers"),
			 (else_try),
			   (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town),
			   (str_store_string, s17, "@town"),
			   (str_store_string, s20, "@The townsfolk"),
			 (else_try),
			   (str_store_string, s17, "@castle"),
			   (str_store_string, s20, "@The townsfolk"),
			 (try_end),
			 (str_store_party_name, s23, "$g_encountered_party"),
			 
			# # Check for buildings that are constructed.
			# (try_for_range, ":improvement_no", native_improvements_begin, center_improvements_end),
				# # Prevent the need for two loops, but make sure we only affect improvement slots.
				# (this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
				# (is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
				# (party_slot_ge, "$g_encountered_party", ":improvement_no", cis_built),
				# (val_add,  ":num_improvements", 1),
				# (call_script, "script_get_improvement_details", ":improvement_no"),
				# (try_begin),
					# (eq,  ":num_improvements", 1),
					# (str_store_string, s18, "@{!}{s0}"),
				# (else_try),
					# (str_store_string, s18, "@{!}{s18}, {s0}"),
				# (try_end),
				# # Assess damage to structure.
				# (try_begin),
					# (str_clear, s22),
					# (party_slot_ge, "$g_encountered_party", ":improvement_no", cis_damaged_20_percent),
					# (str_store_string, s22, "@ (minorly damaged)"),
					# (party_slot_ge, "$g_encountered_party", ":improvement_no", cis_damaged_40_percent),
					# (str_store_string, s22, "@ (moderately damaged)"),
					# (party_slot_ge, "$g_encountered_party", ":improvement_no", cis_damaged_60_percent),
					# (str_store_string, s22, "@ (heavily damaged)"),
					# (party_slot_ge, "$g_encountered_party", ":improvement_no", cis_damaged_80_percent),
					# (str_store_string, s22, "@ (total ruins)"),
				# (try_end),
				# (str_store_string, s18, "@{!}{s18}{s22}"),
			# (try_end),
			 
			 # (try_begin),
			   # (eq,  ":num_improvements", 0),
			   # (str_store_string, s19, "@The {s17} has no improvements."),
			 # (else_try),
			   # (str_store_string, s19, "@The {s17} has the following improvements:^{s18}."),
			 # (try_end),
			 
			 (try_begin),
				(str_clear, s21),
				(this_or_next|party_slot_ge, "$g_encountered_party", slot_center_current_improvement_1, 1),
				(this_or_next|party_slot_ge, "$g_encountered_party", slot_center_current_improvement_2, 1),
				(party_slot_ge, "$g_encountered_party", slot_center_current_improvement_3, 1),
				
				 (str_store_string, s21, "@{s20} are currently working on:"),
				 (try_for_range, ":improvement_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
					 (try_begin),
					   (party_get_slot, ":cur_improvement", "$g_encountered_party", ":improvement_slot"),
					   (gt, ":cur_improvement", 0),
					   (call_script, "script_get_improvement_details", ":cur_improvement"),
					   (str_store_string, s7, s0),
					   (store_current_hours, ":cur_hours"),
					   (store_add, ":end_time_slot", ":improvement_slot", 3),
					   (party_get_slot, ":finish_time", "$g_encountered_party", ":end_time_slot"),
					   (val_sub, ":finish_time", ":cur_hours"),
					   (store_div, reg8, ":finish_time", 24),
					   (val_max, reg8, 1),
					   (store_sub, reg9, reg8, 1),
					   (try_begin),
							(party_slot_ge, "$g_encountered_party", ":cur_improvement", cis_built),
							(assign, reg21, 1),
					   (else_try),
							(assign, reg21, 0),
					   (try_end),
					   (str_store_string, s21, "@{s21}^{reg21?Repairing the:Building a} {s7} needing another {reg8} day{reg9?s:} to complete."),
					 (try_end),
				 (try_end),
			 (try_end),
		],
		[
			("cancel_que_1",
				[(party_slot_ge, "$g_encountered_party", slot_center_current_improvement_1, 1),
				(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_1),
				(call_script, "script_get_improvement_details", ":improvement"),
				],
				"Cancel work on the {s0}.",
				[
					(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_1),
					(call_script, "script_get_improvement_details", ":improvement"),
					(party_set_slot, "$g_encountered_party", slot_center_current_improvement_1, 0),
					# Reset ending time record.
					(store_sub, ":offset", slot_center_improvement_end_hour_1, slot_center_current_improvement_1),
					(store_add, ":end_hour_slot", slot_center_current_improvement_1, ":offset"),
					(party_set_slot, "$g_encountered_party", ":end_hour_slot", 0),
					# Reset starting time record.
					(store_sub, ":offset", slot_center_improvement_start_hour_1, slot_center_current_improvement_1),
					(store_add, ":end_hour_slot", slot_center_current_improvement_1, ":offset"),
					(party_set_slot, "$g_encountered_party", ":end_hour_slot", 0),
					# Notify the player.
					(str_store_party_name, s21, "$g_encountered_party"),
					(display_message, "@Work on the {s0} in {s21} has been stopped."),
					(jump_to_menu, "mnu_center_manage"),
				]),
			
			 ("cancel_que_2",
				[(party_slot_ge, "$g_encountered_party", slot_center_current_improvement_2, 1),
				(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_2),
				(call_script, "script_get_improvement_details", ":improvement"),
				],
				"Cancel work on the {s0}.",
				[
					(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_2),
					(call_script, "script_get_improvement_details", ":improvement"),
					(party_set_slot, "$g_encountered_party", slot_center_current_improvement_2, 0),
					# Reset ending time record.
					(store_sub, ":offset", slot_center_improvement_end_hour_1, slot_center_current_improvement_1),
					(store_add, ":end_hour_slot", slot_center_current_improvement_2, ":offset"),
					(party_set_slot, "$g_encountered_party", ":end_hour_slot", 0),
					# Reset starting time record.
					(store_sub, ":offset", slot_center_improvement_start_hour_1, slot_center_current_improvement_1),
					(store_add, ":end_hour_slot", slot_center_current_improvement_2, ":offset"),
					(party_set_slot, "$g_encountered_party", ":end_hour_slot", 0),
					# Notify the player.
					(str_store_party_name, s21, "$g_encountered_party"),
					(display_message, "@Work on the {s0} in {s21} has been stopped."),
					(jump_to_menu, "mnu_center_manage"),
				]),
			
			 ("cancel_que_3",
				[(party_slot_ge, "$g_encountered_party", slot_center_current_improvement_3, 1),
				(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_3),
				(call_script, "script_get_improvement_details", ":improvement"),
				],
				"Cancel work on the {s0}.",
				[
					(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_3),
					(call_script, "script_get_improvement_details", ":improvement"),
					(party_set_slot, "$g_encountered_party", slot_center_current_improvement_3, 0),
					# Reset ending time record.
					(store_sub, ":offset", slot_center_improvement_end_hour_1, slot_center_current_improvement_1),
					(store_add, ":end_hour_slot", slot_center_current_improvement_3, ":offset"),
					(party_set_slot, "$g_encountered_party", ":end_hour_slot", 0),
					# Reset starting time record.
					(store_sub, ":offset", slot_center_improvement_start_hour_1, slot_center_current_improvement_1),
					(store_add, ":end_hour_slot", slot_center_current_improvement_3, ":offset"),
					(party_set_slot, "$g_encountered_party", ":end_hour_slot", 0),
					# Notify the player.
					(str_store_party_name, s21, "$g_encountered_party"),
					(display_message, "@Work on the {s0} in {s21} has been stopped."),
					(jump_to_menu, "mnu_center_manage"),
				]),
			
			("cancel_construction_no", [], "Continue working on current projects.",
				[
					(jump_to_menu, "mnu_center_manage"),
				]),
			
		]),
  
 ]


from util_common import *
from util_wrappers import *

def modmerge_game_menus(orig_game_menus, check_duplicates = False):
    if( not check_duplicates ):
        orig_game_menus.extend(game_menus) # Use this only if there are no replacements (i.e. no duplicated item names)
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
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)