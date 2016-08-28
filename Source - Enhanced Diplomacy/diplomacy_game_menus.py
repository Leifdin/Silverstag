# Enhanced Diplomacy (1.0) by Windyplains

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

("diplomacy_alt_morale_report",0,
	"{s1}",
	"none",
	[
		(call_script, "script_diplomacy_get_player_party_morale_values"),
		(assign, ":target_morale", reg0),
		
		### PARTY SIZE ###
		(assign, reg1, "$g_player_party_morale_modifier_party_size"),
		(try_begin),
			(gt, reg1, 0),
			(str_store_string, s2, "@{!} +"),
		(else_try),
			(str_store_string, s2, "str_space"),
		(try_end),
		
		### LEADERSHIP SKILL ###
		(assign, reg2, "$g_player_party_morale_modifier_leadership"),
		(try_begin),
			(gt, reg2, 0),
			(str_store_string, s3, "@{!} +"),
		(else_try),
			(str_store_string, s3, "str_space"),
		(try_end),
		
		### NO FOOD PENALTY ###
		(try_begin),
			(gt, "$g_player_party_morale_modifier_no_food", 0),
			(assign, reg7, "$g_player_party_morale_modifier_no_food"),
			(str_store_string, s5, "@^No food:  -{reg7}"),
		(else_try),
			(str_store_string, s5, "str_space"),
		(try_end),
		
		### FOOD SUPPLIES ###
		(assign, reg3, "$g_player_party_morale_modifier_food"),
		(try_begin),
			(gt, reg3, 0),
			(str_store_string, s4, "@{!} +"),
		(else_try),
			(str_store_string, s4, "str_space"),
		(try_end),
		
		### WAGE DEBT ###
		(try_begin),
			(gt, "$g_player_party_morale_modifier_debt", 0),
			(assign, reg6, "$g_player_party_morale_modifier_debt"),
			(str_store_string, s6, "@^Wage debt:  -{reg6}"),
		(else_try),
			(str_store_string, s6, "str_space"),
		(try_end),

		### PARTY UNITY ###
		(assign, reg10, "$party_unity"),
		(try_begin),
			(gt, reg10, 0),
			(str_store_string, s10, "@{!} +"),
		(else_try),
			(str_store_string, s10, "str_space"),
		(try_end),
		
		### TROOP EFFECT: BONUS_INSPIRING ###
		(assign, reg11, "$morale_modifier_inspiring"),
		(try_begin),
			(gt, reg11, 0),
			(str_store_string, s11, "@{!} +"),
		(else_try),
			(str_store_string, s11, "str_space"),
		(try_end),
		
		### TROOP EFFECT: BONUS_DRILL_SARGEANT ###
		(assign, reg11, "$morale_modifier_drill_sargeant"),
		(try_begin),
			(gt, reg11, 0),
			(str_store_string, s12, "@{!} -"),
		(else_try),
			(str_store_string, s12, "str_space"),
		(try_end),
		
		### RECENT CHANGES ###
		(party_get_morale, reg5, "p_main_party"),
		(store_sub, reg4, reg5, ":target_morale"),
		(try_begin),
			(gt, reg4, 0),
			(str_store_string, s7, "@{!} +"),
		(else_try),
			(str_store_string, s7, "str_space"),
		(try_end),

		(assign, reg6, 0),
		
		### OUTPUT STRING ###
		(str_store_string, s1, "str_diplomacy_party_morale_report"),
		
		### MORALE FOR SPECIFIC KINGDOM TROOPS ###
		(try_for_range, ":kingdom_no", npc_kingdoms_begin, npc_kingdoms_end),
			(faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),
			(val_div, ":faction_morale", 100),
			(neq, ":faction_morale", 0),
			(assign, reg6, ":faction_morale"),
			(str_store_faction_name, s9, ":kingdom_no"),
			(str_store_string, s1, "str_s1extra_morale_for_s9_troops__reg6_"),
		(try_end),        
	],
	[
		("continue",[],"Continue...",
			[
				(jump_to_menu, "mnu_party_reports"),
			]),
	]),
  
("diplomacy_recruit_volunteers",0,
    "{s18}",
    "none",
    [
		(party_get_slot, ":volunteer_troop", "$current_town", slot_center_volunteer_troop_type),
		(party_get_slot, ":volunteer_amount", "$current_town", slot_center_volunteer_troop_amount),
		(party_get_free_companions_capacity, ":free_capacity", "p_main_party"),
		(store_troop_gold, ":gold", "trp_player"),
		## WINDYPLAINS+ ## - Enhanced Diplomacy - Relation & prosperity hit when recruits are taken during "Mandatory Conscription".
		(try_begin),
			# Check if decree is active and this is a fief in our kingdom.
			(store_faction_of_party, ":faction_no", "$current_town"),
			(eq, ":faction_no", "$players_kingdom"),
			(faction_slot_eq, "$players_kingdom", slot_faction_decree_conscription, 1), # Decree is active.
			# Double number of volunteers available.
			(val_mul, ":volunteer_amount", diplomacy_conscription_troop_multiplier),
			(assign, ":troop_cost", 0),
			(str_store_string, s21, "@conscript"),
		(else_try),
			(assign, ":troop_cost", 10),
			(str_store_string, s21, "@volunteer"),
		(try_end),
		(val_min, ":volunteer_amount", ":free_capacity"),
		(store_troop_gold, ":gold", "trp_player"),
		(store_div, ":gold_capacity", ":gold", ":troop_cost"), #10 denars per man
		(assign, ":party_capacity", ":free_capacity"),
		(val_min, ":party_capacity", ":gold_capacity"),
		(try_begin),
			(gt, ":party_capacity", 0),
			(val_min, ":volunteer_amount", ":party_capacity"),
		(try_end),
		(assign, reg5, ":volunteer_amount"),
		(assign, reg7, 0),
		(try_begin),
			(gt, ":volunteer_amount", ":gold_capacity"),
			(assign, reg7, 1), #not enough money
		(try_end),
		(store_mul, reg6, ":volunteer_amount", ":troop_cost"),#10 denars per man
		(str_store_troop_name_by_count, s3, ":volunteer_troop", ":volunteer_amount"),
		(try_begin),
			(eq, ":volunteer_amount", 0),
			(faction_slot_eq, "$players_kingdom", slot_faction_decree_conscription, 0), # Decree is inactive.
			(str_store_string, s18, "@No one here seems to be willing to join your party."),
		(else_try),
			(eq, ":volunteer_amount", 0),
			(faction_slot_eq, "$players_kingdom", slot_faction_decree_conscription, 1), # Decree is active.
			(str_store_string, s18, "@There is no one currently available to conscript."),
		(else_try),
			(faction_slot_eq, "$players_kingdom", slot_faction_decree_conscription, 0), # Decree is inactive.
			(str_store_string, s18, "@{reg5?One:reg5} {s3} {reg5?volunteers:volunteer} to follow you."),
			(set_background_mesh, "mesh_pic_recruits"),
		(else_try),
			(faction_slot_eq, "$players_kingdom", slot_faction_decree_conscription, 1), # Decree is active.
			(str_store_string, s18, "@{reg5?One:reg5} {s3} {reg5?conscript is:conscripts are} available to follow you."),
			(set_background_mesh, "mesh_pic_recruits"),
		(try_end),
		## WINDYPLAINS- ##
    ],
    [
		("continue_not_enough_gold",
			[
				(eq, reg7, 1),
			],
			"I don't have enough money...",
			[
				(jump_to_menu,"mnu_village"),
			]),

		("continue",
			[
				(eq, reg7, 0),
				(eq, reg5, 0),
			], #noone willing to join                   
			"Continue...",
			[
				(party_set_slot, "$current_town", slot_center_volunteer_troop_amount, -1),
				(jump_to_menu,"mnu_village"),
			]),

		("recruit_them",
			[
				(eq, reg7, 0),
				(gt, reg5, 0),
			],
			"Recruit them ({reg6} denars).",
			[
				(call_script, "script_village_recruit_volunteers_recruit"),
								
				(jump_to_menu,"mnu_village"),
			]),

		("forget_it",
			[
				(eq, reg7, 0),
				(gt, reg5, 0),
			],
			"Forget it.",
			[
				(jump_to_menu,"mnu_village"),
			]),
    ],),
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
