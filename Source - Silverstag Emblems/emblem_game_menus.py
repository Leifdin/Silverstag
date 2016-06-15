# Silverstag Emblems by Windyplains

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
	
	# Presentation modes controlled by $pep_mode
	# PEP_MODE_INFORMATIONAL               = 0   # Describe the emblem system in game.
	# PEP_MODE_CHARACTER_RESET             = 1   # Resets for abilities, attributes, skills, proficiencies and all of the above.
	# PEP_MODE_STATISTICS                  = 2   # Add +1 skill, attribute or +10 proficiency.
	# PEP_MODE_MISC                        = 3   # Instantly finish a book
	# PEP_MODE_DEBUGGING                   = 4   # Add or remove emblems.
	
	# mnu_garrison_switch_modes
	("player_emblem_switch_modes", mnf_scale_picture|mnf_disable_all_keys,
		"I shouldn't see this.  This should automatically be hidden by a new presentation.",
		"none",
		[
			# Wipe clean GRT_OBJECTS
			(try_for_range, ":slot", 0, 400),
				(troop_set_slot, EMBLEM_OBJECTS, ":slot", 0),
			(try_end),
			
			(try_begin),
				####### MODE : EMBLEM INFORMATION #######
				(eq, "$pep_mode", PEP_MODE_INFORMATIONAL),
				(change_screen_return),
				(start_presentation, "prsnt_pep_emblem_info"),
			
			(else_try),
				####### MODE : CHARACTER RESETS #######
				(eq, "$pep_mode", PEP_MODE_CHARACTER_RESET),
				(change_screen_return),
				(start_presentation, "prsnt_pep_character_resets"),
			
			(else_try),
				####### MODE : CHARACTER STATISTICS #######
				(eq, "$pep_mode", PEP_MODE_STATISTICS),
				(change_screen_return),
				(start_presentation, "prsnt_pep_character_development"),
			
			(else_try),
				####### MODE : MISC OPTIONS #######
				(eq, "$pep_mode", PEP_MODE_MISC),
				(change_screen_return),
				(start_presentation, "prsnt_pep_misc_options"),
			
			(else_try),
				####### MODE : EMBLEM DEBUGGING #######
				(eq, "$pep_mode", PEP_MODE_DEBUGGING),
				(change_screen_return),
				(start_presentation, "prsnt_pep_debugging"),
			
			(try_end),
			],
		[
			("continue",[], "Leave...",	[(jump_to_menu, "mnu_reports"),]),
			
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
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)