# Quest Pack 3 (1.0) by Windyplains

from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *

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

# General DEBUG menu for this quest pack.
("qp3_debug_menu",mnf_disable_all_keys,
	"From here you can manually initiate or end quests as needed for testing.",
	"none",
	[
	],
	[
		("qp3_debugger_initiate", [], "Manually initiate quests", 
			[
				(jump_to_menu, "mnu_qp3_debug_initiate_quest"),
			]),
		
		("qp3_debugger_abort", [], "Manually abort quests", 
			[
				(jump_to_menu, "mnu_qp3_debug_abort_quest"),
			]),
		
		("continue", [], "Return to camp",	[(jump_to_menu, "mnu_camp"),]),
	]),

# DEBUG MENU: Initiate Quest.
("qp3_debug_initiate_quest",mnf_disable_all_keys,
	"It appears the following party members are missing items from their assigned dynamic weapon sets.  Please click on the party member below to update their settings.",
	"none",
	[
		(menu_clear_items, "mnu_qp3_debug_initiate_quest"),
		(try_for_range, ":quest_no", qp3_quests_begin, qp3_quests_end),
			(neg|check_quest_active, ":quest_no"),
			(str_store_quest_name, s21, ":quest_no"),
			(menu_add_item, "mnu_qp3_debug_initiate_quest", "@{s21}", -1, "script_cf_qp3_debug_initiate_quest", ":quest_no"),
		(try_end),
		(menu_add_item, "mnu_qp3_debug_initiate_quest", "@Return to Map", -1, "script_qus_exit_to_map", 0),
	],
	[]),

# DEBUG MENU: Abort Quest.
("qp3_debug_abort_quest",mnf_disable_all_keys,
	"It appears the following party members are missing items from their assigned dynamic weapon sets.  Please click on the party member below to update their settings.",
	"none",
	[
		(menu_clear_items, "mnu_qp3_debug_abort_quest"),
		(try_for_range, ":quest_no", qp3_quests_begin, qp3_quests_end),
			(check_quest_active, ":quest_no"),
			(str_store_quest_name, s21, ":quest_no"),
			(menu_add_item, "mnu_qp3_debug_abort_quest", "@{s21}", -1, "script_qp3_debug_abort_quest", ":quest_no"),
		(try_end),
		(menu_add_item, "mnu_qp3_debug_abort_quest", "@Return to Map", -1, "script_qus_exit_to_map", 0),
	],
	[]),

 ]

# hook_assessment_quest_initiation = [
	# (call_script, "script_qp2_hook_assessment_initiations"), # Floris 2.6 : Quest Pack 2 Initialization - Windyplains
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
    find_index = find_object(orig_game_menus, "camp")
    orig_game_menus[find_index][5].insert(0,
            ("qp3_debugging",[(ge, DEBUG_QUEST_PACK_3, 1),],"Quest Pack 3 Debugging Menus", [(jump_to_menu, "mnu_qp3_debug_menu")]),
          )
		  
# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
	try:
		var_name_1 = "game_menus"
		orig_game_menus = var_set[var_name_1]
		modmerge_game_menus(orig_game_menus)
		# Inside menu "bandit_lair" -> menu option "leave_victory" consequence block -> Add insertion for "qst_destroy_the_lair" above [ (assign, "$g_leave_encounter", 0), ].
		find_i = list_find_first_match_i( orig_game_menus, "bandit_lair" )
		menu = GameMenuWrapper(orig_game_menus[find_i])
		menuoptions = menu.GetMenuOptions()
		submenu_index = list_find_first_containing_i(menuoptions, "leave_victory")
		submenu = GameMenuOptionWrapper(menuoptions[submenu_index])
		submenu.GetConsequenceBlock().InsertBefore(0,[ (call_script, "script_qp3_quest_destroy_the_lair", floris_quest_victory_condition), ])
        # codeblock = GameMenuWrapper(orig_game_menus[find_i]).GetOpBlock()
        # line_i = codeblock.GetLength() - 2
        # codeblock.InsertBefore(line_i, hook_assessment_quest_initiation)
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)