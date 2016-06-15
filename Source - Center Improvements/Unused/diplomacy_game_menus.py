# Companion Management System (1.0) by Windyplains

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
# General configuration menu for equipment mods.
	("companion_settings",mnf_disable_all_keys,
		"{s1}", # From here you can access features related to your equipment or that of your companions.
		"none",
		[
			#(set_background_mesh, "mesh_companion_menu"),
			(str_clear, s1),
			(assign, reg11, 0),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				(val_add, reg11, 1),
			(try_end),
		],
		[
			("cms_relationship_matrix", 
				[
					(try_begin),
						(lt, reg11, 1),
						(disable_menu_option),
					(try_end),
				], "View companion relationships.", 
				[
					(assign, "$return_menu", "mnu_companion_settings"),
					(start_presentation, "prsnt_relation_matrix"),
				]),
			
			("cms_assign_role", 
				[
					(try_begin),
						(lt, reg11, 1),
						(disable_menu_option),
					(try_end),
				], "Assign party roles.", 
				[
					(assign, "$return_menu", "mnu_companion_settings"),
					(start_presentation, "prsnt_cms_party_roles"),
				]),
			
			("cms_equip_companion", 
				[
					(try_begin),
						(lt, reg11, 1),
						(disable_menu_option),
					(try_end),
				], "Access a companion's inventory.", 
				[
					(assign, "$return_menu", "mnu_companion_settings"),
					(jump_to_menu, "mnu_cms_access_companion_inventory"),
				]),
			
			("dws_config_panel", [], "Change dynamic weapon settings.",	
				[
					(call_script, "script_dws_jump_to_troop_settings", 0, "trp_player"),
				]),
				
			("als_config_panel", 
				[
					(try_begin),
						(lt, reg11, 1),
						(disable_menu_option),
					(try_end),
				], "Change autoloot settings.",	
				[
					(change_screen_return),
					(party_get_num_companions, reg1, "p_main_party"),
					(party_get_num_companion_stacks, ":stacks", "p_main_party"),
					(assign, "$als_troop", -1),
					(assign, ":menu_item_count", 0),
					(try_for_range, ":stack_no", 0, ":stacks"),
						(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
						(this_or_next|is_between, ":troop_no", companions_begin, companions_end),
						(is_between, ":troop_no", pretenders_begin, pretenders_end),
						(eq, "$als_troop", -1),
						(assign, "$als_troop", ":troop_no"),
						(val_add, ":menu_item_count", 1),
					(try_end),
					
					# Setup default character as first companion.
					(troop_set_slot, ALS_OBJECTS, als_val_menu_selected_character, 0),
					
					# Initialize settings.
					(call_script, "script_als_initialize_troop_settings"),
					(start_presentation, "prsnt_als_settings"),
				]),
				
			# ("als_confirm_panel", [], "Access autoloot menu.",	
				# [
					# (assign, "$return_menu", "mnu_companion_settings"),
					# (jump_to_menu, "mnu_manage_loot_pool"),
				# ]),
				
			("continue", [], "Continue...",	[(jump_to_menu, "mnu_camp"),]),
		]),

###########################################################################################################################
#####                                             DYNAMIC WEAPON SYSTEM                                               #####
###########################################################################################################################
		
	# Out of settings update menu.
	("update_dws_settings",mnf_disable_all_keys,
		"Dynamic Weapon Sets^Companions with outdated settings:", # It appears the following party members are missing items from their assigned dynamic weapon sets.  Please click on the party member below to update their settings.
		"none",
		[
			(menu_clear_items, "mnu_update_dws_settings"),
			(try_begin),
				(troop_slot_eq, "trp_player", slot_troop_dws_out_of_date, 1),
				(str_store_troop_name, s21, "trp_player"),
				(menu_add_item, "mnu_update_dws_settings", "@{s21}", -1, "script_dws_jump_to_troop_settings", "trp_player"),
			(try_end),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(troop_slot_eq, ":troop_no", slot_troop_dws_out_of_date, 1),
				(str_store_troop_name, s21, ":troop_no"),
				(menu_add_item, "mnu_update_dws_settings", "@{s21}", -1, "script_dws_jump_to_troop_settings", ":troop_no"),
			(try_end),
			(menu_add_item, "mnu_update_dws_settings", "@Return to Map", -1, "script_cms_exit_to_map", 0),
			# (set_background_mesh, "mesh_companion_menu"),
			# (str_clear, s1),
		],
		[]),
		
	# Access a companion's inventory.
	("cms_access_companion_inventory",mnf_disable_all_keys,
		"{s1}", # From here you can access the inventory of any companion within your party.  This is primarily to support lending them weapons beyond their normal equipment for purposes of the dynamic weapon sets.
		"none",
		[
			(menu_clear_items, "mnu_cms_access_companion_inventory"),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				(str_store_troop_name, s21, ":troop_no"),
				(try_begin),
					(eq, ":troop_no", "$cms_role_storekeeper"),
					(str_store_string, s22, "@ (Storekeeper)"),
				(else_try),
					(eq, ":troop_no", "$cms_role_quartermaster"),
					(str_store_string, s22, "@ (Quartermaster)"),
				(else_try),
					(eq, ":troop_no", "$cms_role_jailer"),
					(str_store_string, s22, "@ (Gaoler)"),
				(else_try),
					(str_clear, s22),
				(try_end),
				(menu_add_item, "mnu_cms_access_companion_inventory", "@Edit {s21}'s Inventory{s22}", -1, "script_cms_access_companion_inventory", ":troop_no"),
			(try_end),
			(menu_add_item, "mnu_cms_access_companion_inventory", "@Return to Previous Menu", -1, "script_cms_exit_to_previous_menu", 0),
			(menu_add_item, "mnu_cms_access_companion_inventory", "@Return to Map", -1, "script_cms_exit_to_map", 0),
			# (set_background_mesh, "mesh_companion_menu"),
			(str_clear, s1),
		],
		[]),
		
###########################################################################################################################
#####                                               AUTOLOOT SYSTEM                                                   #####
###########################################################################################################################
  ("manage_loot_pool",
    0,
    "Item pool currently has {reg20} of {reg21} items in it.",
    "none",
    [
		(assign, "$pool_troop", "trp_temp_troop"),
		(assign, "$alc_troop", "trp_player"),
		(assign, "$next_looting_troop", "trp_player"),
		(assign, reg20, 0),
		(assign, reg21, 0),
		(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
		(try_for_range, ":i_slot", 0, ":inv_cap"),
			(troop_get_inventory_slot, ":item_id", "$pool_troop", ":i_slot"),
			(ge, ":item_id", 0),
			(val_add, reg20, 1),
			(item_get_value, ":value", ":item_id"),
			(ge, ":value", 200),
			(val_add, reg21, 1),
		(try_end),
		(assign, reg21, ":inv_cap"),
		(str_clear, s41), # Clean out the list that stores what everyone took.
    ],
    [
		("auto_loot",
			[
				#(eq, "$inventory_menu_offset",0),
				(store_free_inventory_capacity, ":space", "$pool_troop"),
				(try_begin),
					(lt, reg20, 1), # Is there anything even in the pool.
					(disable_menu_option),
					(str_store_string, s21, "@No items are currently available for upgrading."),
				(else_try),
					(lt, ":space", 10),
					(disable_menu_option),
					(str_store_string, s21, "@Insufficient inventory space for auto-upgrade."),
				(else_try),
					# Default success output.
					(str_store_string, s21, "@Let your heroes select gear from the item pool."),
				(try_end),
			],
			"{s21}", 
			[
				(call_script, "script_als_party_begin_autolooting"),
				#(start_presentation, "prsnt_auto_loot_checklist"),
			]),
	  
		("als_config_panel", 
			[
				(assign, ":count", 0),
				(try_for_range, ":troop_no", companions_begin, companions_end),
					(main_party_has_troop, ":troop_no"),
					(val_add, ":count", 1),
				(try_end),
				(try_begin),
					(lt, ":count", 1),
					(disable_menu_option),
				(try_end),
			], "Change companion autoloot settings",	
			[
				(change_screen_return),
				(party_get_num_companions, reg1, "p_main_party"),
				(party_get_num_companion_stacks, ":stacks", "p_main_party"),
				(assign, "$als_troop", -1),
				(assign, ":menu_item_count", 0),
				(try_for_range, ":stack_no", 0, ":stacks"),
					(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
					(this_or_next|is_between, ":troop_no", companions_begin, companions_end),
					(is_between, ":troop_no", pretenders_begin, pretenders_end),
					(eq, "$als_troop", -1),
					(assign, "$als_troop", ":troop_no"),
					(val_add, ":menu_item_count", 1),
				(try_end),
				
				# Setup default character as first companion.
				(troop_set_slot, ALS_OBJECTS, als_val_menu_selected_character, 0),
				
				# Initialize settings.
				(call_script, "script_als_initialize_troop_settings"),
				(start_presentation, "prsnt_als_settings"),
			]),
			
		("loot", [], "Access the item pool.", [(change_screen_loot, "$pool_troop")]),
		
		("als_collect_all", 
			[
				(ge, reg20, 1), # Are there any items in the pool available to pick up?
				(ge, reg21, 1), # Are any above the value threshold for picking up?
				
			], "Collect valuable items and leave.",	
			[
				(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
				
				# QUARTERMASTER: Have quartermaster pick up valuable loot or trade goods that are not food.
				(assign, ":value_threshold", 100),
				(try_begin),
					(neq, "$cms_role_quartermaster", "trp_player"),
					(assign, ":value_threshold", 50),
				(try_end),
				(try_for_range, ":i_slot", 0, ":inv_cap"),
					(troop_get_inventory_slot, ":item_no", "$pool_troop", ":i_slot"),
					(ge, ":item_no", 0),
					(item_get_value, ":value", ":item_no"),
					(assign, ":pick_up", 0),
					(try_begin),
						(ge, ":value", ":value_threshold"),
						(assign, ":pick_up", 1),
					(else_try),
						(is_between, ":item_no", trade_goods_begin, trade_goods_end),
						(neg|is_between, ":item_no", food_begin, food_end),
						(assign, ":pick_up", 1),
					(try_end),
					(eq, ":pick_up", 1),
					(call_script, "script_cf_cms_store_pool_item_to_empty_inventory_slot", "$pool_troop", "$cms_role_quartermaster", ":i_slot"),
					(str_store_item_name, s21, ":item_no"),
					(str_store_troop_name, s22, "$cms_role_quartermaster"),
					(try_begin),
						(eq, "$cms_role_quartermaster", "trp_player"),
						(str_store_string, s22, "@You"),
					(try_end),
					(display_message, "@{s22} picked up a {s21} from the item pool.", gpu_green),
				(try_end),
				
				# STOREKEEPER: Have storekeeper pick up any food available.
				# (party_get_slot, ":troop_no", "p_main_party", slot_party_role_chef), # 
				(assign, ":troop_no", "$cms_role_storekeeper"),
				(try_begin),
					(neq, ":troop_no", "trp_player"),
					(try_for_range, ":i_slot", 0, ":inv_cap"),
						(troop_get_inventory_slot, ":item_no", "$pool_troop", ":i_slot"),
						(ge, ":item_no", 0),
						(is_between, ":item_no", food_begin, food_end),
						(troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":i_slot"),
						(neq, ":imod", imod_rotten),
						(call_script, "script_cf_cms_store_pool_item_to_empty_inventory_slot", "$pool_troop", ":troop_no", ":i_slot"),
						(str_store_item_name, s21, ":item_no"),
						(str_store_troop_name, s22, ":troop_no"),
						(display_message, "@{s22} found some {s21} to add to the party stores."),
					(try_end),
				(try_end),
				(jump_to_menu, "$return_menu"),
			]),
			
		("auto_loot_leave", [],
			"Leave items behind.",
			[
			  (assign, "$alc_troop", "trp_player"),
			  (jump_to_menu, "$return_menu"),
			]),
	]),
	
	("als_jump_to_next_looter",
    0,
    "Your companions have all taken what they can so you may return to the autolooting menu at this time.  Be sure to take any items from the item pool that you wish to retain.^^{s41}",
    "none",
    [
		(call_script, "script_als_party_begin_autolooting"),
		(try_begin),
			(neq, "$next_looting_troop", "$alc_troop"),
			(jump_to_menu, "mnu_manage_loot_pool"),
		(try_end),
    ],
    [
		("als_autoreturn_leave", [],
			"Return to Autoloot Menu",
			[
			  (jump_to_menu, "mnu_manage_loot_pool"),
			]),
	]),
	
	("als_jump_to_presentation",
    0,
    "Your companions have all taken what they can so you may return to the autolooting menu at this time.  Be sure to take any items from the item pool that you wish to retain.^^{s41}",
    "none",
    [
		(start_presentation, reg51),
    ],
    [
		("als_autoreturn_leave", [],
			"Return to Autoloot Menu",
			[
			  (jump_to_menu, "mnu_manage_loot_pool"),
			]),
	]),
	
###########################################################################################################################
#####                                                 PARTY ROLES                                                     #####
###########################################################################################################################
  ## WINDYPLAINS+ ## - Allow auto-buy of food.
  (
    "trade_auto_buy_food_begin",0,
    "You will buy food according to the shopping list of foods automatically. Do you want to continue?^^You can view and configure the shopping list here.",
    "none", [],
  [
    ("continue",[],"Continue...",
    [
      (call_script, "script_auto_buy_food"), ## CC 1.322: this line replaces the following lines.
      (jump_to_menu, "$g_next_menu"),
      ]),
      
    ("change_shopping_list_of_food",[],"Configure the shopping list of foods.",[(start_presentation, "prsnt_shopping_list_of_food"),]),
    ("go_back",[],"Go back",[(jump_to_menu, "$g_next_menu")]),
   ]),
  ## WINDYPLAINS- ##
  
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
	
	# splice this into CAMP menu to access the main companion management system menu.
    find_index = find_object(orig_game_menus, "camp")
    orig_game_menus[find_index][5].insert(1,
            ("camp_equipment_settings",[],"Companion Management", [(jump_to_menu, "mnu_companion_settings")]),
          )
	
	# splice this into TOWN_TRADE (marketplace) menu to add an option for configuring your purchasing of food.
    find_index = find_object(orig_game_menus, "town_trade")
    orig_game_menus[find_index][5].insert(0,
            ("auto_buy_food",[], "Have your storekeeper purchase food automatically.", [(assign, "$g_next_menu", "mnu_town"), (jump_to_menu,"mnu_trade_auto_buy_food_begin"), ]),
          )
		  
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
		# HOOK: (STOREKEEPER): Town exit detection to buy food.
        find_i = list_find_first_match_i( orig_game_menus, "town" )
        menuoption = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOption("town_leave")
        codeblock = menuoption.GetConsequenceBlock()
        codeblock.InsertBefore(0, [(try_begin), (eq, "$g_buy_foods_when_leaving", 1), (call_script, "script_auto_buy_food"), (try_end),])
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)