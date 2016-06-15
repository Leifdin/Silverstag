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
("cms_switch_modes", mnf_scale_picture|mnf_disable_all_keys,
		"I shouldn't see this.  This should automatically be hidden by a new presentation.",
		"none",
		[
			# Wipe clean HUB_OBJECTS
			(try_for_range, ":slot", 0, 400),
				(troop_set_slot, HUB_OBJECTS, ":slot", 0),
			(try_end),
			
			(try_begin),
				####### MODE : GENERAL INFORMATION #######
				(eq, "$cms_display", CMS_MODE_MAIN),
				(change_screen_return),
				# (start_presentation, "prsnt_hub_general_info"),
				(jump_to_menu, "mnu_companion_settings"),
			
			(else_try),
				####### MODE : PARTY ROLES #######
				(eq, "$cms_display", CMS_MODE_PARTY_ROLES),
				(change_screen_return),
				(start_presentation, "prsnt_cms_party_roles"),
				
			(else_try),
				####### MODE : SHOPPING LIST #######
				(eq, "$cms_display", CMS_MODE_SHOPPING_LIST),
				(change_screen_return),
				(start_presentation, "prsnt_shopping_list_of_food"),
				
			(try_end),
			],
		[
			("continue",[], "Leave...",	[(jump_to_menu, "mnu_camp"),]),
			
		]),
		
# General configuration menu for equipment mods.
	("companion_settings",mnf_disable_all_keys,
		"{s1}", # From here you can access features related to your equipment or that of your companions.
		"none",
		[
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
			
			("cms_setup_reading", 
				[
					(try_begin),
						(lt, reg11, 1),
						(disable_menu_option),
					(try_end),
				], "Setup a companion's reading.", 
				[
					(assign, "$return_menu", "mnu_companion_settings"),
					(jump_to_menu, "mnu_cms_book_reading"),
				]),
			
			("dws_config_panel", 
				[
					(eq, 1, 0), ## DWS DISABLE ##
				], "Change dynamic weapon settings.",	
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
					(assign, "$autoloot_mode", ALS_MODE_PLAYER_SEARCH),
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
				
			("action_export_import",[],"Export or import companion history.",
				[
					(assign, "$g_player_troop", "trp_player"),
					(jump_to_menu, "mnu_export_import_npcs"),
				]),
			
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
			(eq, 1, 0), ## DWS DISABLE ##
		],
		[]),
		
	# Access a companion's inventory.
	("cms_access_companion_inventory",mnf_disable_all_keys,
		"{s1}", # From here you can access the inventory of any companion within your party.  This is primarily to support lending them weapons beyond their normal equipment for purposes of the dynamic weapon sets.
		"none",
		[
			(menu_clear_items, "mnu_cms_access_companion_inventory"),
			(assign, ":companion_count", 0),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				(this_or_next|lt, ":companion_count", 11), # Done to prevent reaching 16 companions which blocks the return menu item and forces you to crash the game.
				(this_or_next|eq, ":troop_no", "$cms_role_storekeeper"),
				(this_or_next|eq, ":troop_no", "$cms_role_quartermaster"),
				(eq, ":troop_no", "$cms_role_jailer"),
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
				(val_add, ":companion_count", 1),
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
		(assign, "$autoloot_mode", ALS_MODE_BATTLEFIELD_LOOT),
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
					(is_between, ":troop_no", companions_begin, companions_end),
					# (this_or_next|is_between, ":troop_no", companions_begin, companions_end),
					# (is_between, ":troop_no", pretenders_begin, pretenders_end),
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
				
				# STOREKEEPER: Have storekeeper pick up any food available.
				# (party_get_slot, ":troop_no", "p_main_party", slot_party_role_chef), # 
				(assign, ":troop_no", "$cms_role_storekeeper"),
				(call_script, "script_cms_verify_party_role_filled", ROLE_STOREKEEPER),
				(try_begin),
					(neq, ":troop_no", "trp_player"),
					(assign, ":total_items", 0),
					(try_for_range, ":i_slot", 0, ":inv_cap"),
						(troop_get_inventory_slot, ":item_no", "$pool_troop", ":i_slot"),
						(ge, ":item_no", 0),
						(is_between, ":item_no", food_begin, food_end),
						(troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":i_slot"),
						(neq, ":imod", imod_rotten),
						(call_script, "script_cf_cms_store_pool_item_to_empty_inventory_slot", "$pool_troop", ":troop_no", ":i_slot"),
						(try_begin),
							(eq, "$cms_report_mode", CMS_REPORTS_DETAILED),
							(str_store_item_name, s21, ":item_no"),
							(str_store_troop_name, s22, ":troop_no"),
							(display_message, "@{s22} found some {s21} to add to the party stores."),
						(try_end),
					(try_end),
					# Report Summary Info
					(try_begin),
						(ge, ":total_items", 1),
						(eq, "$cms_report_mode", CMS_REPORTS_SUMMARY),
						(str_store_troop_name, s21, ":troop_no"),
						(assign, reg21, ":total_items"),
						(store_sub, reg23, reg21, 1),
						(display_message, "@{s21} collected {reg21} food store{reg23?s:}.", gpu_green),
					(try_end),
				(try_end),
				
				# QUARTERMASTER: Have quartermaster pick up valuable loot or trade goods that are not food.
				(call_script, "script_cms_verify_party_role_filled", ROLE_QUARTERMASTER),
				(assign, ":total_items", 0),
				(assign, ":total_value", 0),
				(try_for_range, ":i_slot", 0, ":inv_cap"),
					(troop_get_inventory_slot, ":item_no", "$pool_troop", ":i_slot"),
					(ge, ":item_no", 0),
					(item_get_value, ":value", ":item_no"),
					(assign, ":pick_up", 0),
					(try_begin),
						(ge, ":value", "$cms_minimum_pickup_value"),
						# (neg|is_between, ":item_no", food_begin, food_end),
						(assign, ":pick_up", 1),
					(else_try),
						(is_between, ":item_no", trade_goods_begin, trade_goods_end),
						(neg|is_between, ":item_no", food_begin, food_end),
						(assign, ":pick_up", 1),
					(try_end),
					(eq, ":pick_up", 1),
					## Determine value of item for summary view.
					(troop_get_inventory_slot_modifier, ":item_modifier", "$pool_troop", ":i_slot"),
					(call_script, "script_cms_get_item_value_with_imod", ":item_no", ":item_modifier", CMS_AUTO_SELLING),
					(assign, ":item_value", reg0),
					(val_div, ":item_value", 100),
					(call_script, "script_game_get_item_sell_price_factor", ":item_no"),
					(assign, ":sell_price_factor", reg0),
					(val_mul, ":item_value", ":sell_price_factor"),
					(val_div, ":item_value", 100),
					(val_max, ":item_value",1),
					## Store the item to the Quartermaster's inventory.
					(call_script, "script_cf_cms_store_pool_item_to_empty_inventory_slot", "$pool_troop", "$cms_role_quartermaster", ":i_slot"),
					(val_add, ":total_items", 1),
					(val_add, ":total_value", ":item_value"),
					(str_store_item_name, s21, ":item_no"),
					(str_store_troop_name, s22, "$cms_role_quartermaster"),
					(try_begin),
						(eq, "$cms_role_quartermaster", "trp_player"),
						(str_store_string, s22, "@You"),
					(try_end),
					(try_begin),
						(eq, "$cms_report_mode", CMS_REPORTS_DETAILED),
						(display_message, "@{s22} picked up a {s21} from the item pool.", gpu_green),
					(try_end),
				(try_end),
				# Report Summary Info
				(try_begin),
					(ge, ":total_items", 1),
					(eq, "$cms_report_mode", CMS_REPORTS_SUMMARY),
					(str_store_troop_name, s21, "$cms_role_quartermaster"),
					(assign, reg21, ":total_items"),
					(assign, reg22, ":total_value"),
					(store_sub, reg23, reg21, 1),
					(store_sub, reg24, reg22, 1),
					(display_message, "@{s21} collected {reg21} item{reg23?s:} valuing {reg22} denar{reg24?s:}.", gpu_green),
				(try_end),
				
				(try_begin),
					(eq, "$return_menu", "mnu_village_loot_complete"),
					(change_screen_return),
				(else_try),
					(jump_to_menu, "$return_menu"),
				(try_end),
			]),
			
		("auto_loot_leave", [],
			"Leave items behind.",
			[
			  (assign, "$alc_troop", "trp_player"),
			  (try_begin),
				(eq, "$return_menu", "mnu_village_loot_complete"),
				(change_screen_return),
			  (else_try),
				(jump_to_menu, "$return_menu"),
			  (try_end),
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
    "none", 
	[],
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
  
###########################################################################################################################
#####                                            COMPANION BOOK READING                                               #####
###########################################################################################################################
		
	# Out of settings update menu.
	("cms_book_reading",mnf_disable_all_keys,
		"Companion Book Reading^The following companions have readable books in their inventory:", # It appears the following party members are missing items from their assigned dynamic weapon sets.  Please click on the party member below to update their settings.
		"none",
		[
			(menu_clear_items, "mnu_cms_book_reading"),
			(assign, ":companion_count", 0),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				(assign, ":book_total", 0),
				(try_for_range, ":item_no", readable_books_begin, readable_books_end),
					(store_item_kind_count, ":book_count", ":item_no", ":troop_no"),
					(val_add, ":book_total", ":book_count"),
				(try_end),
				(ge, ":book_total", 1),
				(lt, ":companion_count", 13), # Done to prevent reaching 16 companions which blocks the return menu item and forces you to crash the game.
				(str_store_troop_name, s21, ":troop_no"),
				(val_add, ":companion_count", 1),
				# Get the book information.
				(try_begin),
					(troop_get_slot, ":item_no", ":troop_no", slot_troop_reading_book),
					(is_between, ":item_no", readable_books_begin, readable_books_end),
					(store_sub, ":companion_no", ":troop_no", companions_begin),
					(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
					(item_get_slot, reg21, ":item_no", ":book_read_slot"),
					(val_div, reg21, 10),
					(str_store_item_name, s22, ":item_no"),
					(str_store_string, s23, "@ - {s22} ({reg21}%)"),
				(else_try),
					(str_store_string, s23, "@ - Nothing"),
				(try_end),
				(menu_add_item, "mnu_cms_book_reading", "@{s21}'s Reading{s23}", -1, "script_cms_companion_reading", ":troop_no"),
			(try_end),
			(menu_add_item, "mnu_cms_book_reading", "@Return to Previous Menu", -1, "script_cms_exit_to_previous_menu", 0),
			(menu_add_item, "mnu_cms_book_reading", "@Return to Map", -1, "script_cms_exit_to_map", 0),
		],
		[]),
		
	# Out of settings update menu.
	("cms_companion_reading",mnf_disable_all_keys,
		"Companion Book Reading^^This companion has the following books to choose from.  Only one book may be selected for reading at a time and only readable books will be listed below.", # It appears the following party members are missing items from their assigned dynamic weapon sets.  Please click on the party member below to update their settings.
		"none",
		[
			(menu_clear_items, "mnu_cms_companion_reading"),
			(assign, ":troop_no", "$temp"),
			## SILVERSTAG EMBLEMS+ ##
			(try_begin),
				(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
				(ge, reg1, EMBLEM_COST_FINISH_BOOK_COMPANION),
				# Troop is reading a valid book.
				(troop_get_slot, ":item_no", ":troop_no", slot_troop_reading_book),
				(is_between, ":item_no", readable_books_begin, readable_books_end),
				# Troop has not yet finished this book.
				(store_sub, ":companion_no", ":troop_no", companions_begin),
				(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
				(item_get_slot, ":progress", ":item_no", ":book_read_slot"),
				(is_between, ":progress", 0, 1000),
				(assign, reg21, EMBLEM_COST_FINISH_BOOK_COMPANION),
				(store_sub, reg22, reg21, 1),
				(str_store_item_name, s21, ":item_no"),
				(menu_add_item, "mnu_cms_companion_reading", "@Instantly finish {s21} ({reg21} emblem{reg22?s:})", -1, "script_emblem_instantly_complete_reading_companion", 0),
			(try_end),
			## SILVERSTAG EMBLEMS- ##
			(try_for_range, ":item_no", readable_books_begin, readable_books_end),
				(store_item_kind_count, ":book_count", ":item_no", ":troop_no"),
				(ge, ":book_count", 1),
				(str_store_item_name, s21, ":item_no"),
				(str_store_string, s23, "@Read"),
				(store_sub, ":companion_no", ":troop_no", companions_begin),
				(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
				(try_begin),
					(item_slot_ge, ":item_no", ":book_read_slot", 1000),
					(str_store_string, s22, "@ (already read)"),
				(else_try),
					(troop_slot_eq, ":troop_no", slot_troop_reading_book, ":item_no"),
					(item_get_slot, reg21, ":item_no", ":book_read_slot"),
					(val_div, reg21, 10),
					(str_store_string, s22, "@ ({reg21}% read)"),
					(str_store_string, s23, "@Stop Reading"),
				(else_try),
					(item_slot_ge, ":item_no", ":book_read_slot", 1),
					(item_get_slot, reg21, ":item_no", ":book_read_slot"),
					(val_div, reg21, 10),
					(str_store_string, s22, "@ ({reg21}% read)"),
				(else_try),
					(str_clear, s22),
				(try_end),
				(menu_add_item, "mnu_cms_companion_reading", "@{s23}: {s21} {s22}", -1, "script_cms_switch_companion_reading", ":item_no"),
			(try_end),
			(menu_add_item, "mnu_cms_companion_reading", "@Return to Previous Menu", -1, "script_cms_exit_to_previous_menu", 0),
			(menu_add_item, "mnu_cms_companion_reading", "@Return to Map", -1, "script_cms_exit_to_map", 0),
		],
		[]),
		
###########################################################################################################################
#####                                          COMPANION IMPORT / EXPORT                                              #####
###########################################################################################################################

	## WINDYPLAINS+ ## - Import/Export of NPCs - Credit: Custom Commander
  ("export_import_npcs", mnf_enable_hot_keys,
   "Please choose a character, then press the C key to view and export or import the chosen character history.^^You choose {reg0?{s0}:none}.",
   "none",
    [
      (assign, reg0, "$g_player_troop"),
      (str_store_troop_name, s0, "$g_player_troop"),
    ],
    [
      ("export_import_back",[],"Go back",
        [
          (assign, "$g_player_troop", "trp_player"),
          (set_player_troop, "$g_player_troop"),
          (jump_to_menu, "mnu_companion_settings"),
        ]
      ),
    ]+[("export_import_npc"+str(x+1),
        [
          (store_add, ":dest_npc", "trp_npc1", x),
          (str_store_troop_name, s0, ":dest_npc"),
        ], "{s0}",
        [
          (store_add, ":dest_npc", "trp_npc1", x),
          (assign, "$g_player_troop", ":dest_npc"),
          (set_player_troop, "$g_player_troop"),
        ]) for x in range(0, 8)]+[
      ("export_import_next",[],"Next page", [(jump_to_menu, "mnu_export_import_npcs_2")]),
    ]
  ),

  ("export_import_npcs_2", mnf_enable_hot_keys,
    "Please choose a character, then press the C key to view and export or import the chosen character history.^^You choose {reg0?{s0}:none}.",
    "none",
     [
       (assign, reg0, "$g_player_troop"),
       (str_store_troop_name, s0, "$g_player_troop"),
     ],
    [
      ("export_import_prev",[],"Previous page", [(jump_to_menu, "mnu_export_import_npcs")]),
    ]+[("export_import_npc"+str(x+1),
      [
        (store_add, ":dest_npc", "trp_npc1", x),
        (str_store_troop_name, s0, ":dest_npc"),
      ], "{s0}",
      [
        (store_add, ":dest_npc", "trp_npc1", x),
        (assign, "$g_player_troop", ":dest_npc"),
        (set_player_troop, "$g_player_troop"),
      ]) for x in range(8, 17)] #Silverstag - for new companions; was 8, 17
  ),
	## WINDYPLAINS- ##
 ]

camp_addon = [

	("camp_equipment_settings",[],"Companion Management", 
		[
			(assign, "$cms_display", CMS_MODE_MAIN),
			(jump_to_menu, "mnu_companion_settings"),
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
	
	# splice this into CAMP menu to access the main companion management system menu.
    # find_index = find_object(orig_game_menus, "camp")
    # orig_game_menus[find_index][5].insert(1,
            # ("camp_equipment_settings",[],"Companion Management", [(jump_to_menu, "mnu_companion_settings")]),
          # )
	# splice this into camp menu to call the mod options presentation
	find_i = list_find_first_match_i( orig_game_menus, "camp" )
	menuoptions = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOptions()
	find_i = list_find_first_match_i(menuoptions, "camp_action")		
	OpBlockWrapper(menuoptions).InsertAfter(find_i, camp_addon)		

	# splice this into TOWN_TRADE (marketplace) menu to add an option for configuring your purchasing of food.
	find_index = find_object(orig_game_menus, "town_trade")
	orig_game_menus[find_index][5].insert(6,
		("auto_buy_food",[(eq, 1, 0),], "Have your storekeeper purchase food automatically.", [(assign, "$g_next_menu", "mnu_town"), (jump_to_menu,"mnu_trade_auto_buy_food_begin"), ]),)

	# splice this into TOWN_TRADE (marketplace) menu to jump to a menu for accessing companion inventories.
	find_index = find_object(orig_game_menus, "town_trade")
	orig_game_menus[find_index][5].insert(7,
		("companion_inventories",
			[
				(assign, reg11, 0),
				(try_for_range, ":troop_no", companions_begin, companions_end),
					(main_party_has_troop, ":troop_no"),
					(val_add, reg11, 1),
				(try_end),
				(ge, reg11, 1),
			], "Check companion inventories.", [(assign, "$return_menu", "mnu_town_trade"), (jump_to_menu,"mnu_cms_access_companion_inventory"), ]),)
		  
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