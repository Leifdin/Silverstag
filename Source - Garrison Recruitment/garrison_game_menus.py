# Garrison Recruitment & Training by Windyplains

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
	
	# mnu_garrison_switch_modes
	("garrison_switch_modes", mnf_scale_picture|mnf_disable_all_keys,
		"I shouldn't see this.  This should automatically be hidden by a new presentation.",
		"none",
		[
			# Wipe clean GRT_OBJECTS
			(try_for_range, ":slot", 0, 400),
				(troop_set_slot, GRT_OBJECTS, ":slot", 0),
			(try_end),
			
			(try_begin),
				####### MODE : GARRISON INFORMATION #######
				(eq, "$grt_mode", HUB_MODE_GENERAL),
				(change_screen_return),
				(start_presentation, "prsnt_garrison_general"),
			
			(else_try),
				####### MODE : GARRISON RECRUITMENT #######
				(eq, "$grt_mode", GARRISON_MODE_RECRUITMENT),
				(change_screen_return),
				(start_presentation, "prsnt_garrison_recruitment"),
			
			(else_try),
				####### MODE : GARRISON TRAINING #######
				(eq, "$grt_mode", GARRISON_MODE_TRAINING),
				(change_screen_return),
				(start_presentation, "prsnt_garrison_training"),
			
			(else_try),
				####### MODE : GARRISON REORDERING #######
				(eq, "$grt_mode", GARRISON_MODE_REORDER),
				(change_screen_return),
				(start_presentation, "prsnt_garrison_reordering"),
			
			(else_try),
				####### MODE : CURRENT QUEUE #######
				(eq, "$grt_mode", GARRISON_MODE_QUEUE),
				(change_screen_return),
				(start_presentation, "prsnt_garrison_queue"),
			
			(else_try),
				####### MODE : INSPECT TROOP #######
				(eq, "$grt_mode", GARRISON_MODE_TROOP_INFO),
				(change_screen_return),
				(assign, "$g_presentation_next_presentation", "prsnt_garrison_recruitment"),
				(start_presentation, "prsnt_troop_note"),
			
			(else_try),
				####### MODE : EMBLEM OPTIONS #######
				(eq, "$grt_mode", GARRISON_MODE_EMBLEM_OPTIONS),
				(change_screen_return),
				(start_presentation, "prsnt_garrison_emblem_options"),
			
			(try_end),
			],
		[
			("continue",[], "Leave...",	[(jump_to_menu, "mnu_town"),]),
			
		]),
 ]

# camp_addon = [

	# ("camp_equipment_settings",
		# [
			# (ge, DEBUG_GARRISON, 2),
		# ],"Garrison Queue Testing", 
		# [
			# (call_script, "script_grt_clear_center_queue", "p_town_1"),
			# (jump_to_menu, "mnu_queue_testing"),
		# ]),
	
# ]
 
 
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
	
	# splice this into camp menu to call the mod options presentation
	# find_i = list_find_first_match_i( orig_game_menus, "camp" )
	# menuoptions = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOptions()
	# find_i = list_find_first_match_i(menuoptions, "camp_action")		
	# OpBlockWrapper(menuoptions).InsertAfter(find_i, camp_addon)		

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
	try:
		var_name_1 = "game_menus"
		orig_game_menus = var_set[var_name_1]
		modmerge_game_menus(orig_game_menus)
		# HOOK: Town entry detection.
		find_i = list_find_first_match_i( orig_game_menus, "town" )
		codeblock = GameMenuWrapper(orig_game_menus[find_i]).GetOpBlock()
		codeblock.InsertBefore(0, [(call_script, "script_cms_town_entry"),])
		try:
			# HOOK: (STOREKEEPER): Town exit detection to buy food.
			find_i = list_find_first_match_i( orig_game_menus, "town" )
			menuoption = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOption("town_leave")
			codeblock = menuoption.GetConsequenceBlock()
			codeblock.InsertBefore(0, [(try_begin), (eq, "$cms_enable_auto_buying", 1), (call_script, "script_auto_buy_food"), (try_end),])
		except KeyError:
			errstring = "CMS Hook Failure: game_menus -> 'town_leave' for auto buying of food."
			raise ValueError(errstring)
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)