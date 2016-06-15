# Custom Commissioned Items by Windyplains

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
	
	# mnu_cci_switch_modes
	("cci_switch_modes", mnf_scale_picture|mnf_disable_all_keys,
		"I shouldn't see this.  This should automatically be hidden by a new presentation.",
		"none",
		[
			# Wipe clean CCI_OBJECTS
			(try_for_range, ":slot", 0, 400),
				(troop_set_slot, CCI_OBJECTS, ":slot", 0),
			(try_end),
			
			(try_begin),
				####### MODE : COMMISSION AN ITEM #######
				(eq, "$cci_mode", CCI_MODE_COMMISSION_ITEM),
				(assign, "$temp", 0),
				(troop_set_slot, CCI_OBJECTS, cci_val_selected_imod, imod_plain),
				(troop_set_slot, CCI_OBJECTS, cci_val_checkbox_modifiers_begin, 1),
				(change_screen_return),
				(start_presentation, "prsnt_commission_requests"),
			
			(else_try),
				####### MODE : LIST ALL COMMISSIONS #######
				(eq, "$cci_mode", CCI_MODE_LIST_ALL_COMMISSIONS),
				(change_screen_return),
				(start_presentation, "prsnt_all_commissions"),
			
			(else_try),
				####### MODE : ARTISAN CRAFTER #######
				(eq, "$cci_mode", CCI_MODE_ARTISAN_INFO),
				(change_screen_return),
				(start_presentation, "prsnt_artisan_blacksmith"),
			
			(else_try),
				####### MODE : REPAIR ITEMS #######
				(eq, "$cci_mode", CCI_MODE_REPAIR_ITEMS),
				(call_script, "script_cci_get_artisan_id", "$current_town"),
				(assign, "$cci_mode", CCI_STARTING_SCREEN),
				(change_screen_loot, reg1),
				
			(else_try),
				####### MODE : EVENT LOG #######
				(eq, "$cci_mode", CCI_MODE_EVENT_LOG),
				(troop_set_slot, CCI_OBJECTS, cci4_val_display_setting, 0), # Display current location only.
				(change_screen_return),
				(start_presentation, "prsnt_cci_event_log"),
			
			(else_try),
				####### MODE : EMBLEM OPTIONS #######
				(eq, "$cci_mode", CCI_MODE_EMBLEM_OPTIONS),
				(change_screen_return),
				(start_presentation, "prsnt_cci_emblem_options"),
			
			# (else_try),
				# ####### MODE : GARRISON REORDERING #######
				# (eq, "$grt_mode", GARRISON_MODE_REORDER),
				# (change_screen_return),
				# (start_presentation, "prsnt_garrison_reordering"),
			
			# (else_try),
				# ####### MODE : CURRENT QUEUE #######
				# (eq, "$grt_mode", GARRISON_MODE_QUEUE),
				# (change_screen_return),
				# (start_presentation, "prsnt_garrison_queue"),
			
			# (else_try),
				# ####### MODE : INSPECT TROOP #######
				# (eq, "$grt_mode", GARRISON_MODE_TROOP_INFO),
				# (change_screen_return),
				# (assign, "$g_presentation_next_presentation", "prsnt_garrison_recruitment"),
				# (start_presentation, "prsnt_troop_note"),
			
			(try_end),
			],
		[
			("continue",[], "Leave...",	[(jump_to_menu, "mnu_town"),]),
			
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