# Quest Pack 2 (1.0) by Windyplains

from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from module_constants import *

game_menus = [
# General DEBUG menu for this quest pack.
("qp2_debug_menu",mnf_disable_all_keys,
	"From here you can manually initiate or end quests as needed for testing.",
	"none",
	[
	],
	[
		("qp2_rival_debug_display", [], "Trade Rival Display", 
			[
				(assign, "$rival_troop", qp2_trade_rivals_begin),
				(start_presentation, "prsnt_qp2_debug_rival_status"),
			]),
		
		("qp2_quest_pack_reboot", [], "Reboot Quest Pack 2", 
			[
				(call_script, "script_qp2_quest_floris_trade_shortage", floris_quest_cancel),
				(call_script, "script_qp2_quest_floris_trade_surplus", floris_quest_cancel),
				(call_script, "script_qp2_quest_floris_trade_fortune_favors_the_bold", floris_quest_cancel),
				
				(call_script, "script_qp2_game_start"),
			]),
		
		("qp2_force_trade_shortage", 
			[
				(str_store_string, s20, "@Trade Shortage"),
				(try_begin),
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(str_store_string, s21, "@Initiate: {s20}"),
				(else_try),
					(check_quest_active, "qst_floris_trade_shortage"),
					(str_store_string, s21, "@Cancel: {s20}"),
				(else_try),
					(str_store_string, s21, "@Quest '{s20}' blocked due to active quests."),
					(disable_menu_option),
				(try_end),
			]
			, "{s21}", 
			[
				(try_begin),
					## Force Initate ##
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(call_script, "script_qp2_check_for_trade_quests", "qst_floris_trade_shortage"),
				(else_try),
					## Cancel Active Quest ##
					(check_quest_active, "qst_floris_trade_shortage"),
					(call_script, "script_qp2_quest_floris_trade_shortage", floris_quest_cancel),
				(try_end),
			]),
		
		("qp2_force_trade_surplus", 
			[
				(str_store_string, s20, "@Trade Surplus"),
				(try_begin),
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(str_store_string, s21, "@Initiate: {s20}"),
				(else_try),
					(check_quest_active, "qst_floris_trade_surplus"),
					(str_store_string, s21, "@Cancel: {s20}"),
				(else_try),
					(str_store_string, s21, "@Quest '{s20}' blocked due to active quests."),
					(disable_menu_option),
				(try_end),
			]
			, "{s21}", 
			[
				(try_begin),
					## Force Initate ##
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(call_script, "script_qp2_check_for_trade_quests", "qst_floris_trade_surplus"),
				(else_try),
					## Cancel Active Quest ##
					(check_quest_active, "qst_floris_trade_surplus"),
					(call_script, "script_qp2_quest_floris_trade_surplus", floris_quest_cancel),
				(try_end),
			]),
		
		("qp2_force_trade_fortune", 
			[
				(str_store_string, s20, "@Fortune Favors the Bold"),
				(try_begin),
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(str_store_string, s21, "@Initiate: {s20}"),
				(else_try),
					(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
					(str_store_string, s21, "@Cancel: {s20}"),
				(else_try),
					(str_store_string, s21, "@Quest '{s20}' blocked due to active quests."),
					(disable_menu_option),
				(try_end),
			]
			, "{s21}", 
			[
				(try_begin),
					## Force Initate ##
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(call_script, "script_qp2_check_for_trade_quests", "qst_floris_trade_fortune_favors_bold"),
				(else_try),
					## Cancel Active Quest ##
					(check_quest_active, "qst_floris_trade_fortune_favors_bold"),
					(call_script, "script_qp2_quest_floris_trade_fortune_favors_the_bold", floris_quest_cancel),
				(try_end),
			]),
		
		("qp2_force_trade_noble_opportunity", 
			[
				(str_store_string, s20, "@A Noble Opportunity"),
				(try_begin),
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(str_store_string, s21, "@Initiate: {s20}"),
				(else_try),
					(check_quest_active, "qst_trade_noble_opportunity"),
					(str_store_string, s21, "@Cancel: {s20}"),
				(else_try),
					(str_store_string, s21, "@Quest '{s20}' blocked due to active quests."),
					(disable_menu_option),
				(try_end),
			]
			, "{s21}", 
			[
				(try_begin),
					## Force Initate ##
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(call_script, "script_qp2_check_for_trade_quests", "qst_trade_noble_opportunity"),
				(else_try),
					## Cancel Active Quest ##
					(check_quest_active, "qst_trade_noble_opportunity"),
					(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_cancel),
				(try_end),
			]),
		
		("qp2_force_trade_noble_opportunity", 
			[
				(str_store_string, s20, "@The Discount Enterprise"),
				(try_begin),
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(str_store_string, s21, "@Initiate: {s20}"),
				(else_try),
					(check_quest_active, "qst_trade_discount_enterprise"),
					(str_store_string, s21, "@Cancel: {s20}"),
				(else_try),
					(str_store_string, s21, "@Quest '{s20}' blocked due to active quests."),
					(disable_menu_option),
				(try_end),
			]
			, "{s21}", 
			[
				(try_begin),
					## Force Initate ##
					(call_script, "script_cf_qp2_check_no_active_qp2_quests"),
					(call_script, "script_qp2_check_for_trade_quests", "qst_trade_discount_enterprise"),
				(else_try),
					## Cancel Active Quest ##
					(check_quest_active, "qst_trade_discount_enterprise"),
					(call_script, "script_qp2_quest_trade_discount_enterprise", floris_quest_cancel),
				(try_end),
			]),
		
		("continue", [], "Return to camp",	[(jump_to_menu, "mnu_camp"),]),
	]),
 ]

trade_quest_initiation = [
	#(call_script, "script_qp2_check_for_trade_quests", 0), # Floris 2.6 : Quest Pack 2 Initialization - Windyplains
]

trade_quest_rival_in_tavern = [
# (try_for_range, ":trade_rival", qp2_trade_rivals_begin, qp2_trade_rivals_end),
	# (troop_slot_eq, ":trade_rival", slot_rival_location, "$current_town"),
	# (troop_slot_eq, ":trade_rival", slot_rival_status, qp2_rival_status_active),
	# (eq, "$qp2_block_trade_quests", 0), # Hide rivals if the player isn't using the system.
	# (store_random_in_range, ":roll", 0, 100),
	# (lt, ":roll", 35),
	# (set_visitor, ":cur_entry", ":trade_rival"),
	# (val_add, ":cur_entry", 1),
# (try_end),
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
	
	# splice this into camp menu to call the tournament options menu
    find_index = find_object(orig_game_menus, "camp")
    orig_game_menus[find_index][5].insert(0,
            ("qp2_debugging",[(ge, DEBUG_QUEST_PACK_2, 1),],"Quest Pack 2 Debugging Menus", [(jump_to_menu, "mnu_qp2_debug_menu")]),
          )
	
	
# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "game_menus"
        orig_game_menus = var_set[var_name_1]
        modmerge_game_menus(orig_game_menus)
        # HOOK: Attempts to initiate trade quests when local prices are assessed in the marketplace.
        find_i = list_find_first_match_i( orig_game_menus, "town_trade_assessment" )
        codeblock = GameMenuWrapper(orig_game_menus[find_i]).GetOpBlock()
        line_i = codeblock.GetLength() - 2
        codeblock.InsertBefore(line_i, trade_quest_initiation)
        # HOOK: Inserts a trade rival (35% chance) into the tavern scene if they're within the town.
        find_i = list_find_first_match_i( orig_game_menus, "town" )
        menuoption = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOption("town_tavern")
        codeblock = menuoption.GetConsequenceBlock()
        line_i = codeblock.GetLength() - 2
        codeblock.InsertBefore(line_i, trade_quest_rival_in_tavern)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)