# Companion Management System (1.0) by Windyplains

from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from module_constants import *

game_menus = [

	# mnu_hub_switch_modes
	("hub_switch_modes", mnf_scale_picture|mnf_disable_all_keys,
		"I shouldn't see this.  This should automatically be hidden by a new presentation.",
		"none",
		[
			# Wipe clean HUB_OBJECTS
			(try_for_range, ":slot", 0, 400),
				(troop_set_slot, HUB_OBJECTS, ":slot", 0),
			(try_end),
			
			(try_begin),
				####### MODE : GENERAL INFORMATION #######
				(eq, "$hub_mode", HUB_MODE_GENERAL),
				(change_screen_return),
				(start_presentation, "prsnt_hub_general_info"),
			
			(else_try),
				####### MODE : FINANCES #######
				(eq, "$hub_mode", HUB_MODE_FINANCES),
				(change_screen_return),
				(start_presentation, "prsnt_hub_finances"),
			
			(else_try),
				####### MODE : IMPROVEMENTS #######
				(eq, "$hub_mode", HUB_MODE_IMPROVEMENTS),
				(change_screen_return),
				(start_presentation, "prsnt_hub_improvements"),
			
			(else_try),
				####### MODE : RECRUITMENT #######
				(eq, "$hub_mode", HUB_MODE_RECRUITMENT),
				(change_screen_return),
				(start_presentation, "prsnt_hub_recruitment"),
			
			(else_try),
				####### MODE : ADVISORS #######
				(eq, "$hub_mode", HUB_MODE_ADVISORS),
				(change_screen_return),
				(start_presentation, "prsnt_hub_advisors"),
			
			(else_try),
				####### MODE : GARRISON #######
				(eq, "$hub_mode", HUB_MODE_GARRISON),
				(change_screen_return),
				(assign, "$grt_mode", GARRISON_MODE_GENERAL),
				(presentation_set_duration, 0),
				(jump_to_menu, "mnu_garrison_switch_modes"),
			
			(else_try),
				####### MODE : QUESTS #######
				(eq, "$hub_mode", HUB_MODE_QUESTS),
				(change_screen_return),
				(start_presentation, "prsnt_hub_quests"),
			
			(else_try),
				####### MODE : TROOP INSPECTION #######
				(eq, "$hub_mode", HUB_MODE_TROOP_INFO),
				(change_screen_return),
				(start_presentation, "prsnt_troop_note"),
			
			(else_try),
				####### MODE : COMMISSIONS #######
				(eq, "$hub_mode", HUB_MODE_COMMISSIONS),
				(change_screen_return),
				(assign, "$cci_mode", CCI_STARTING_SCREEN),
				(presentation_set_duration, 0),
				(jump_to_menu, "mnu_cci_switch_modes"),
			
			(else_try),
				####### MODE : COMMISSIONS #######
				(eq, "$hub_mode", HUB_MODE_REALM_AFFAIRS),
				(change_screen_return),
				(assign, "$kmt_mode", KMT_STARTING_SCREEN),
				(presentation_set_duration, 0),
				(jump_to_menu, "mnu_kmt_switch_modes"),
			
			(try_end),
			],
		[
			("continue",[], "Leave...",	[(jump_to_menu, "mnu_town"),]),
			
		]),
		
	("hub_recruitment_testing", mnf_scale_picture|mnf_disable_all_keys,
		"CENTER RECRUITMENT DATA:^^{s23}^{s21}^{s22}^^{s29}",
		"none",
		[
			
			## CENTER CULTURE
			(party_get_slot, ":center_culture", "$current_town", slot_center_culture),
			(str_store_faction_name, s23, ":center_culture"),
			(str_store_string, s23, "@Center Culture is {s23}."),
			
			## CENTER RELATION
			(party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
			(assign, reg21, ":center_relation"),
			(try_begin),
				(ge, ":center_relation", 5),
				(str_store_string, s21, "@Center Relation {reg21} greater than or equal to 5.  PASS"),
			(else_try),
				(str_store_string, s21, "@Center Relation {reg21} less than 5.  FAILED"),
			(try_end),
			
			## FACTION CHECKS
			(store_faction_of_party, ":faction_no", "$current_town"),
			(store_relation, ":faction_relation", ":faction_no", "fac_player_faction"),
			(str_store_faction_name, s1, ":faction_no"),
			(try_begin),
				(eq, ":faction_no", "$players_kingdom"),
				(str_store_string, s22, "@Center Faction = {s1} ($players_kingdom).  PASS"),
			(else_try),
				(eq, ":faction_no", "$supported_pretender_old_faction"),
				(str_store_string, s22, "@Center Faction = {s1} ($supported_pretender_old_faction).  PASS"),
			(else_try),
				(eq, "$players_kingdom", 0),
				(str_store_string, s22, "@Center Faction = The player is factionless.  PASS"),
			(else_try),
				(ge, ":faction_relation", 0),
				(str_store_string, s22, "@Center Faction is friendly with 'fac_player_faction'.  PASS"),
			(else_try),
				(str_store_string, s22, "@Center Faction [{s1}] = FAILED"),
			(try_end),
			
			## RECRUITABLE CHECK ##
			(try_begin),
				(this_or_next|ge, ":center_relation", 5),
				(this_or_next|eq, ":faction_no", "$players_kingdom"),
				(this_or_next|ge, ":faction_relation", 0),
				(this_or_next|eq, ":faction_no", "$supported_pretender_old_faction"),
				(eq, "$players_kingdom", 0),
				(str_store_string, s29, "@General troops are recruitable here."),
			(else_try),
				(str_store_string, s29, "@General troops are NOT recruitable here."),
			(try_end),
		],
		[
			("continue",[], "Return...",	[(change_screen_return),]),
			("continue",[], "Leave...",	[(jump_to_menu, "mnu_town"),]),
			
		]),
 ]

hub_hook_village = [

	("hub_main",
		[
			(try_begin),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
				(str_store_string, s21, "@Manage this village."),
			(else_try),
				(str_store_string, s21, "@Gather information & recruit volunteers"),
			(try_end),
		]
		,"{s21}", 
		[
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(start_presentation, "prsnt_hub_general_info"),
		]),
	
]
 
hub_hook_town = [

	("hub_main",
		[
			(try_begin),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
				(assign, reg0, 1),
				(try_begin),
					(party_slot_eq, "$current_town", slot_party_type, spt_castle),
					(assign, reg0, 0),
				(try_end),
				(str_store_string, s21, "@Manage this {reg0?town:castle}."),
			(else_try),
				(str_store_string, s21, "@Gather information & recruit volunteers"),
			(try_end),
		]
		,"{s21}", 
		[
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(start_presentation, "prsnt_hub_general_info"),
		]),
	
	("hub_testing",
		[
			(ge, DEBUG_RECRUITMENT, 1),
		]
		,"Test recruitment requirements here.", 
		[
			(jump_to_menu, "mnu_hub_recruitment_testing"),
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
	
	# splice this into "town" menu to call the center management hub.
	find_i = list_find_first_match_i( orig_game_menus, "town" )
	menuoptions = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOptions()
	find_i = list_find_first_match_i(menuoptions, "walled_center_manage")		
	OpBlockWrapper(menuoptions).InsertAfter(find_i, hub_hook_town)		
	
	# splice this into "village" menu to call the center management hub.
	find_i = list_find_first_match_i( orig_game_menus, "village" )
	menuoptions = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOptions()
	find_i = list_find_first_match_i(menuoptions, "village_manage")		
	OpBlockWrapper(menuoptions).InsertAfter(find_i, hub_hook_village)		
	
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