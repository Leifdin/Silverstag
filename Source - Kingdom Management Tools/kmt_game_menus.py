# Kingdom Management Tools (1.0) by Windyplains

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
	
	# mnu_kmt_switch_modes
	("kmt_switch_modes", mnf_scale_picture|mnf_disable_all_keys,
		"I shouldn't see this.  This should automatically be hidden by a new presentation.",
		"none",
		[
			# Wipe clean KMT_OBJECTS
			(try_for_range, ":slot", 0, 400),
				(troop_set_slot, KMT_OBJECTS, ":slot", 0),
			(try_end),
			
			(try_begin),
				####### MODE : GENERAL INFO #######
				(eq, "$kmt_mode", KMT_MODE_GENERAL_INFO),
				(change_screen_return),
				(start_presentation, "prsnt_kmt_general_info"),
			
			(else_try),
				####### MODE : FIEF ELECTIONS #######
				(eq, "$kmt_mode", KMT_MODE_FIEF_ELECTIONS),
				(change_screen_return),
				(start_presentation, "prsnt_kmt_fief_elections"),
			
			(else_try),
				####### MODE : FIEF EXCHANGE #######
				(eq, "$kmt_mode", KMT_MODE_FIEF_EXCHANGE),
				(change_screen_return),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_menu_lord_left, 0),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_menu_lord_right, 1),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_lord_left, "trp_player"),
				# Attempt to find another lord in the player's faction.
				(assign, ":selected_lord", -1),
				(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
					(eq, ":selected_lord", -1),
					(store_troop_faction, ":faction_no", ":troop_no"),
					(eq, ":faction_no", "$players_kingdom"),
					(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
					(assign, ":selected_lord", ":troop_no"),
				(try_end),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_label_forced_loss, 0),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_right_label_forced_loss, 0),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_rating, 0),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_right_rating, 0),
				(try_begin),
					(is_between, ":selected_lord", active_npcs_begin, active_npcs_end),
					(troop_set_slot, KMT_OBJECTS, kmt3_val_lord_right, ":selected_lord"),
					(start_presentation, "prsnt_kmt_fief_exchange"),
				(else_try),
					(display_message, "@Warning - You must have at least one vassal within your faction in order to trade.", gpu_red),
				(try_end),
				
			(else_try),
				####### MODE : VASSAL GIFTS #######
				(eq, "$kmt_mode", KMT_MODE_VASSAL_GIFTS),
				(change_screen_return),
				(start_presentation, "prsnt_kmt_vassal_gifts"),
			
			(else_try),
				####### MODE : VASSAL TITLES #######
				(eq, "$kmt_mode", KMT_MODE_VASSAL_TITLES),
				(change_screen_return),
				(store_sub, ":offset", "$players_kingdom", kingdoms_begin),
				(troop_set_slot, KMT_OBJECTS, kmt5_val_faction_selector, ":offset"),
				(troop_set_slot, KMT_OBJECTS, kmt5_val_selected_faction, "$players_kingdom"),
				(start_presentation, "prsnt_kmt_vassal_titles"),
			
			(else_try),
				####### MODE : VASSAL PRISONERS #######
				(eq, "$kmt_mode", KMT_MODE_VASSAL_PRISONERS),
				(change_screen_return),
				(start_presentation, "prsnt_kmt_vassal_prisoners"),
			
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