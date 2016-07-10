# Companion Management System (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *
from header_terrain_types import * # Needed for the Troop Ability (Hunting)

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	
###########################################################################################################################
#####                                                COMMON SCRIPTS                                                   #####
###########################################################################################################################

# script_cf_dws_item_in_a_weapon_set
# Reports back if an item is part of a DWS group or not.
# Input: troop #, item #
# Output: none
("cf_dws_item_in_a_weapon_set",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":item_no", 2),
		
		(assign, ":continue", 0),
		(try_for_range, ":slot_no", slot_troop_dws_sets_begin, slot_troop_dws_sets_end),
			(troop_slot_eq, ":troop_no", ":slot_no", ":item_no"),
			(neg|troop_slot_eq, ":troop_no", ":slot_no", -1), # Filter out empty slots.
			(assign, ":continue", 1),
			### DIAGNOSTIC ###
			# (ge, DEBUG_ALS, 1),
			# (assign, reg31, ":slot_no"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (str_store_item_name, s32, ":item_no"),
			# (display_message, "@DEBUG (DWS): {s31} is trying to upgrade {s32} from slot {reg31}."),
		(try_end),
		(eq, ":continue", 1),
	]),
	
# script_cf_cms_store_pool_item_to_empty_inventory_slot
# Moves an item from one location in a troop's inventory to another while retaining its quality modifier.
# Input: none
# Output: none
("cf_cms_store_pool_item_to_empty_inventory_slot",
    [
		(store_script_param, ":troop_pool", 1),
		(store_script_param, ":troop_dest", 2),
		(store_script_param, ":slot_to_empty", 3),
		
		(troop_get_inventory_slot, ":item_to_store", ":troop_pool", ":slot_to_empty"),
		(ge, ":item_to_store", 1), # Valid Item
		(troop_get_inventory_capacity, ":inv_cap", ":troop_pool"),
		(assign, ":continue", 1),
		(try_for_range, ":inv_slot", 10, ":inv_cap"),
			(eq, ":continue", 1),
			(troop_get_inventory_slot, ":item_in_inventory", ":troop_dest", ":inv_slot"),
			(lt, ":item_in_inventory", 1), # Invalid Item
			(troop_set_inventory_slot, ":troop_dest", ":inv_slot", ":item_to_store"),
			(troop_get_inventory_slot_modifier, ":imod", ":troop_pool", ":slot_to_empty"),
			(troop_set_inventory_slot_modifier, ":troop_dest", ":inv_slot", ":imod"),
			(try_begin),
				(is_between, ":item_to_store", food_begin, food_end),
				(troop_inventory_slot_get_item_amount, ":amount", ":troop_pool", ":slot_to_empty"),
				(troop_inventory_slot_set_item_amount, ":troop_dest", ":inv_slot", ":amount"),
			(try_end),
			(troop_set_inventory_slot, ":troop_pool", ":slot_to_empty", -1),
			(assign, ":continue", 0),
			(ge, DEBUG_ALS, 1),
			(str_store_item_name, s32, ":item_to_store"),
			(assign, reg31, ":imod"),
			(assign, reg32, ":slot_to_empty"),
			(assign, reg33, ":inv_slot"),
			(display_message, "@DEBUG (CMS): {s32} (IMOD: {reg31}) from slot {reg32} to {reg33}."),
		(try_end),
	]),
	
	
###########################################################################################################################
#####                                             DYNAMIC WEAPON SYSTEM                                               #####
###########################################################################################################################

# script_dws_jump_to_troop_settings
# Opens the dws settings panel for the selected "out of date settings" troop.
# Input: none
# Output: none
("dws_jump_to_troop_settings",
    [
		#(store_script_param, ":menu_no", 1),
		(store_script_param, ":troop_no", 2),
		
		(change_screen_return),
		# Setup default character as player.
		(assign, "$dws_troop", ":troop_no"),
		
		# Figure out who the menu should be set to.
		(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
		(assign, ":hero_slot", -1),
        (try_for_range, ":stack_num", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":troop_id", "p_main_party", ":stack_num"),
			(troop_is_hero, ":troop_id"),
			(val_add, ":hero_slot", 1),
			(eq, ":troop_id", ":troop_no"),
			(troop_set_slot, DWS_OBJECTS, dws_val_menu_selected_character, ":hero_slot"),
        (try_end),
		
		# Prevent carrying items from one character to the next.
		(troop_set_slot, DWS_OBJECTS, dws_val_selected_item, -1),
		
		# Initialize troop set information.
		(try_for_range, ":old_slot", slot_troop_battlefield_set_1, slot_troop_dws_enabled),
			(store_sub, ":offset", ":old_slot", slot_troop_battlefield_set_1),
			(store_add, ":new_slot", ":offset", dws_val_battlefield_set_1),
			(troop_get_slot, ":item_no", "$dws_troop", ":old_slot"),
			(troop_set_slot, DWS_OBJECTS, ":new_slot", ":item_no"),
		(try_end),
		
		(troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
		(start_presentation, "prsnt_dws_settings"),
	]),

# script_cms_exit_to_map
# Exits to the map from any dynamically generated DWS menus.
# Input: none
# Output: none
("cms_exit_to_map",
    [
		#(store_script_param, ":menu_no", 1),
		#(store_script_param, ":troop_no", 2),
		
		(change_screen_map),
	]),
	
# script_cms_access_companion_inventory
# Access an equipment trading screen for your companions.
("cms_access_companion_inventory",
    [
		#(store_script_param, ":menu_no", 1),
		(store_script_param, ":troop_no", 2),
		
		(change_screen_loot, ":troop_no"),
	]),
	
# script_cms_exit_to_previous_menu
# Return to the previous menu this menu was accessed from.
("cms_exit_to_previous_menu",
    [
		# (store_script_param, ":menu_no", 1),
		# (store_script_param, ":troop_no", 2),
		
		(try_begin),
			# Prevent nested "return to previous menu" options from being stuck.
			(eq, "$return_menu", "mnu_cms_book_reading"),
			(assign, "$return_menu", "mnu_companion_settings"),
		(else_try),
			# Prevent nested "return to previous menu" options from being stuck.
			(eq, "$return_menu", "mnu_cms_companion_reading"),
			(assign, "$return_menu", "mnu_cms_book_reading"),
		(try_end),
		(jump_to_menu, "$return_menu"),
	]),
	
# script_cms_companion_reading
# PURPOSE: Switch from a list of companions to a specific menu about one companion's reading list.
("cms_companion_reading",
    [
		#(store_script_param, ":menu_no", 1),
		(store_script_param, ":troop_no", 2),
		
		(assign, "$temp", ":troop_no"),
		(assign, "$return_menu", "mnu_cms_book_reading"),
		(jump_to_menu, "mnu_cms_companion_reading"),
	]),
	
# script_cms_switch_companion_reading
# PURPOSE: Change the currently read book by a companion.
("cms_switch_companion_reading",
    [
		#(store_script_param, ":menu_no", 1),
		(store_script_param, ":item_no", 2),
		
		(assign, ":troop_no", "$temp"),
		(troop_get_slot, ":current_book", ":troop_no", slot_troop_reading_book),
		(str_store_item_name, s21, ":item_no"),
		(str_store_troop_name, s22, ":troop_no"),
		(str_store_item_name, s23, ":current_book"),
		
		(try_begin),
			## BOOK HAS ALREADY BEEN READ.
			(store_sub, ":companion_no", ":troop_no", companions_begin),
			(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
			(item_slot_ge, ":item_no", ":book_read_slot", 1000),
			(display_message, "@{s22} has already read {s21}.", gpu_red),
		(else_try),
			## COMPANION HAS INSUFFICIENT INTELLIGENCE.
			(item_get_slot, ":int_req", ":item_no", slot_item_intelligence_requirement),
			(store_attribute_level, ":intelligence", ":troop_no", ca_intelligence),
			(lt, ":intelligence", ":int_req"),
			(display_message, "@{s22} has insufficient knowledge to understand what is written in {s21}.", gpu_red),
		(else_try),
			## BOOK IS AVAILABLE TO READ, BEGIN READING.
			(neg|troop_slot_eq, ":troop_no", slot_troop_reading_book, ":item_no"),
			(call_script, "script_change_troop_reading_book", ":troop_no", ":item_no"),
		(else_try),
			## DEFAULT ACTION REMOVE THE BOOK.
			(call_script, "script_change_troop_reading_book", ":troop_no", REMOVE_BOOK),
		(try_end),
		(assign, "$return_menu", "mnu_cms_companion_reading"),
		(jump_to_menu, "mnu_cms_companion_reading"),
	]),
	
# script_change_troop_reading_book
# PURPOSE: This handles functions of starting, stopping or completing the reading of a book by a companion.
("change_troop_reading_book",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":item_no", 2),
		
		(str_store_troop_name, s21, ":troop_no"),
		(str_store_item_name, s22, ":item_no"),
		
		(try_begin),
			(is_between, ":item_no", readable_books_begin, readable_books_end),
			(troop_set_slot, ":troop_no", slot_troop_reading_book, ":item_no"),
			(display_message, "@{s21} has started reading {s22}.", gpu_green),
		(else_try),
			(eq, ":item_no", REMOVE_BOOK),
			# (is_between, ":item_no", readable_books_begin, reference_books_end),
			(troop_set_slot, ":troop_no", slot_troop_reading_book, 0),
			(troop_get_type, reg21, ":troop_no"),
			(display_message, "@{s21} has stopped reading {reg21?her:his} current book."), #  {s22}."),
		(else_try),
			(eq, ":item_no", COMPLETED_BOOK),
			(troop_get_slot, ":item_no", ":troop_no", slot_troop_reading_book),
			(troop_set_slot, ":troop_no", slot_troop_reading_book, 0),
			(try_begin),
				# Determine the bonus type.
				(troop_get_type, reg21, ":troop_no"),
				(str_store_item_name, s22, ":item_no"),
				(str_store_string, s20, "@{s21} has completed reading '{s22}'"),
				(try_begin),
					(neg|troop_slot_eq, ":troop_no", slot_troop_advisor_station, 0),
					(troop_get_slot, ":center_no", ":troop_no", slot_troop_advisor_station),
					(str_store_party_name, s23, ":center_no"),
					(str_store_string, s20, "@{s20} while stationed in {s23}"),
				(try_end),
				
				(try_begin),
					(eq, ":item_no", "itm_book_tactics"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} tactics skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_persuasion"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} persuasion skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_leadership"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} leadership skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_intelligence"),
					(troop_raise_attribute, ":troop_no", ca_intelligence, 1),
					(str_store_string, s20, "@{s20} and {reg21?her:his} intelligence has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_trade"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} trade skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_weapon_mastery"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} weapon master skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_engineering"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} engineer skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_tracking"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} tracking skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_training"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} training skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_firstaid"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} first-aid skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_prison_management"),
					(str_store_string, s20, "@{s20} and {reg21?her:his} prisoner management skill has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_repair_bonus"),
					(str_store_string, s20, "@{s20} and {reg21?she:he} has become more adept at making repairs cheaper."),
				(else_try),
					(eq, ":item_no", "itm_book_charisma"),
					(troop_raise_attribute, ":troop_no", ca_charisma, 1),
					(str_store_string, s20, "@{s20} and {reg21?her:his} charisma has increased by 1."),
				(else_try),
					(eq, ":item_no", "itm_book_tax_reduction"),
					(str_store_string, s2, "@{s20} and {reg21?she:he} has become more adept at handling finances."),
				(else_try),
					(eq, ":item_no", "itm_book_cunning_rule"),
					(str_store_string, s2, "@{s20} and {reg21?she:he} has gained insight into becoming a more cunning leader."),
				(else_try),
					(eq, ":item_no", "itm_book_prosperity_1"),
					(str_store_string, s2, "@{s20} and {reg21?she:he} has gained insight land stewardship."),
				(else_try),
					(eq, ":item_no", "itm_book_prof75_sword"),
					(try_begin),
						(store_proficiency_level, ":proficiency", ":troop_no", wpt_one_handed_weapon),
						(lt, ":proficiency", 75),
						(troop_set_proficiency, ":troop_no", wpt_one_handed_weapon, 75),
						(str_store_string, s2, "@{s20} and {reg21?she:he} has finally figured out how to use the pointy end."),
					(else_try),
						(str_store_string, s2, "@{s20} and {reg21?she:he} found the book a little too basic to learn much from."),
					(try_end),
				(else_try),
					(eq, ":item_no", "itm_book_prof75_crossbow"),
					(try_begin),
						(store_proficiency_level, ":proficiency", ":troop_no", wpt_crossbow),
						(lt, ":proficiency", 75),
						(troop_set_proficiency, ":troop_no", wpt_crossbow, 75),
						(str_store_string, s2, "@{s20} and {reg21?she:he} has finally figured out how these infernal contraptions work."),
					(else_try),
						(str_store_string, s2, "@{s20} and {reg21?she:he} found the book a little too basic to learn much from."),
					(try_end),
				(else_try),
					(eq, ":item_no", "itm_book_escape_chance"),
					(str_store_string, s2, "@{s20} and {reg21?she:he} has learned how to better corner {reg21?his:her} enemies."),
				(try_end),
				
				# Bonus Experience for finishing a book.
				(try_begin),
					(store_character_level, ":level_bonus", ":troop_no"),
					(val_mul, ":level_bonus", 40),
					(val_max, ":level_bonus", 250),
					(add_xp_to_troop, ":level_bonus", ":troop_no"),
					(assign, reg22, ":level_bonus"),
					(display_message, "@{s21} has received {reg22} experience for completing {s22}.", gpu_green),
				(try_end),
				
				# Notify the player.
				(try_begin),
					(eq, "$enable_popups", 1),
					(dialog_box, "@{s20}", "@Book Completion"),
				(else_try),
					(display_message, "@{s20}", gpu_green),
				(try_end),
			(try_end),
			
		(else_try),
			(neq, ":item_no", 0), # Incase there wasn't a book found.
			(troop_set_slot, ":troop_no", slot_troop_reading_book, 0),
			(assign, reg31, ":item_no"),
			(display_message, "@ERROR (books) - {s21} assigned to read an INVALID BOOK (#{reg31}).", gpu_red),
		(try_end),
	]),
	
# script_cf_cms_troop_has_read_book
# PURPOSE: Check if the given troop has read the given book and fail to pass the script if not.
("cf_cms_troop_has_read_book",
	[
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":book_no", 2),
		
		# Setup variables for considering companions.
		(try_begin),
			(is_between, ":troop_no", companions_begin, companions_end),
			(store_sub, ":companion_no", ":troop_no", companions_begin),
			(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
		(else_try),
			(assign, ":book_read_slot", -1),
		(try_end),
		
		(assign, ":pass", 0),
		(try_begin),
			(item_slot_eq, ":book_no", slot_item_book_read, 1), # Book has been read by the player.
			(eq, ":troop_no", "trp_player"),
			(assign, ":pass", 1),
		(else_try),
			(item_slot_ge, ":book_no", ":book_read_slot", 1000), # Companion has read this book.
			(is_between, ":troop_no", companions_begin, companions_end),
			(assign, ":pass", 1),
		(try_end),
		(eq, ":pass", 1),
	]),
	
###########################################################################################################################
#####                                               AUTOLOOT SYSTEM                                                   #####
###########################################################################################################################

# script_als_autoloot_redirect
# Sets up a common method of handling weapon menu selections in the autoloot settings presentation.
# Input: none
# Output: none
("als_autoloot_redirect",
    [
		(store_script_param, "$return_menu", 1),
		(assign, "$autoloot_mode", ALS_MODE_BATTLEFIELD_LOOT),
		(jump_to_menu, "mnu_manage_loot_pool"),
	]),

# script_als_handle_weapon_menu_selection
# Sets up a common method of handling weapon menu selections in the autoloot settings presentation.
# Input: none
# Output: none
("als_handle_weapon_menu_selection",
    [
		(store_script_param, ":item_slot", 1),
		(store_script_param, ":value", 2),
		
		(store_add, ":value_slot", als_val_menu_slot_0, ":item_slot"),
		(troop_set_slot, ALS_OBJECTS, ":value_slot", ":value"),
		(try_begin),
			(ge, DEBUG_ALS, 1),
			(store_add, ":string_slot", "str_als_label_slot_1", ":item_slot"),
			(str_store_string, s31, ":string_slot"),
			(assign, reg31, ":value"),
			(display_message, "@DEBUG (ALS): Menu '{s31}' set to option {reg31}."),
		(try_end),
	]),

# script_als_handle_damage_type_menu_selection
# Sets up a common method of handling weapon damage type menu selections in the autoloot settings presentation.
# Input: none
# Output: none
("als_handle_damage_type_menu_selection",
    [
		(store_script_param, ":item_slot", 1),
		(store_script_param, ":value", 2),
		
		(store_add, ":value_slot", als_val_menu_weapon_type_0, ":item_slot"),
		(troop_set_slot, ALS_OBJECTS, ":value_slot", ":value"),
		(try_begin),
			(ge, DEBUG_ALS, 1),
			(store_add, ":string_slot", "str_als_label_slot_1", ":item_slot"),
			(str_store_string, s31, ":string_slot"),
			(assign, reg31, ":value"),
			(display_message, "@DEBUG (ALS): Damage type for menu '{s31}' set to option {reg31}."),
		(try_end),
	]),
	
# script_als_save_troop_settings
# Runs through the settings made on the autoloot configuration screen and saves them for that troop.
# Input: none
# Output: none
("als_save_troop_settings",
    [
		(store_script_param, ":troop_no", 1),
		
		### MENU SETTINGS ###
		(try_for_range, ":value_slot", als_val_menu_slot_0, als_val_menu_slot_9),
			(store_sub, ":offset", ":value_slot", als_val_menu_slot_0),
			(store_add, ":troop_slot", slot_troop_upgrade_weapon_1, ":offset"),
			(troop_get_slot, reg1, ALS_OBJECTS, ":value_slot"),
			(troop_set_slot, ":troop_no", ":troop_slot", reg1),
			(ge, DEBUG_ALS, 3),
			(str_store_troop_name, s31, ":troop_no"),
			(store_add, ":string_no", "str_als_label_slot_1", ":offset"),
			(str_store_string, s32, ":string_no"),
			(assign, reg31, reg1),
			(assign, reg32, ":troop_slot"),
			(assign, reg33, ":value_slot"),
			(display_message, "@DEBUG (ALS): {s32} set to {reg31}.  Moved from slot {reg33} of ALS_OBJECTS -> {reg32} of {s31}."),
		(try_end),
		# Weapon 1 Type
		(troop_get_slot, reg1, ALS_OBJECTS, als_val_menu_weapon_type_0),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1_type, reg1),
		# Weapon 2 Type
		(troop_get_slot, reg1, ALS_OBJECTS, als_val_menu_weapon_type_1),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2_type, reg1),
		# Weapon 3 Type
		(troop_get_slot, reg1, ALS_OBJECTS, als_val_menu_weapon_type_2),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3_type, reg1),
		# Weapon 4 Type
		(troop_get_slot, reg1, ALS_OBJECTS, als_val_menu_weapon_type_3),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4_type, reg1),
		# Weight Limit
		(troop_get_slot, reg1, ALS_OBJECTS, als_val_menu_weight_limit),
		(troop_set_slot, ":troop_no", slot_troop_weight_limit, reg1),
		
		### CHECKBOX SETTINGS ###
		# Enable Autoloot
		(troop_get_slot, reg1, ALS_OBJECTS, als_val_checkbox_enable),
		(troop_set_slot, ":troop_no", slot_troop_enable_autolooting, reg1),
		# Do not break weapon sets.
		(troop_get_slot, reg1, ALS_OBJECTS, als_val_checkbox_no_break_sets),
		(troop_set_slot, ":troop_no", slot_troop_prevent_breaking_sets, reg1),
		# Retain heraldic equipment.
		(troop_get_slot, reg1, ALS_OBJECTS, als_val_checkbox_heraldic_items),
		(troop_set_slot, ":troop_no", slot_troop_retain_heraldic_items, reg1),
		
		(try_begin),
			(eq, ":troop_no", "$als_troop"),
			(str_store_troop_name, s21, ":troop_no"),
			(display_message, "@Equipment set configuration for {s21} accepted."),
		(try_end),
	]),
	
# script_als_initialize_troop_settings
# Runs through the settings made on the autoloot configuration screen and initializes them for that troop.
# Input: none
# Output: none
("als_initialize_troop_settings",
    [
		# Initialize troop set information.
		(try_for_range, ":slot", 0, 9),
			(troop_get_inventory_slot, ":item_no", "$als_troop", ":slot"),
			(store_add, ":new_slot", ":slot", als_val_slot_0),
			(try_begin),
				(ge, ":item_no", 1),
				(troop_set_slot, ALS_OBJECTS, ":new_slot", ":item_no"),
				(str_store_item_name, s31, ":item_no"),
			(else_try),
				(str_store_string, s31, "@Empty Slot"),
				(troop_set_slot, ALS_OBJECTS, ":new_slot", -1),
			(try_end),
			(ge, DEBUG_ALS, 3),
			(assign, reg32, ":slot"),
			(assign, reg33, ":new_slot"),
			(display_message, "@DEBUG (ALS): Storing inventory slot #{reg32} [ {s31} ] into presentation slot #{reg33}."),
		(try_end),
		
		# Initalize troop setting information
		(try_for_range, ":troop_slot", slot_troop_upgrade_weapon_1, slot_troop_enable_autolooting),
			(store_sub, ":offset", ":troop_slot", slot_troop_upgrade_weapon_1),
			(store_add, ":value_slot", als_val_menu_slot_0, ":offset"),
			(troop_get_slot, reg1, "$als_troop", ":troop_slot"),
			(troop_set_slot, ALS_OBJECTS, ":value_slot", reg1),
			(ge, DEBUG_ALS, 3),
			(str_store_troop_name, s31, "$als_troop"),
			(store_add, ":string_no", "str_als_label_slot_1", ":offset"),
			(str_store_string, s32, ":string_no"),
			(assign, reg31, reg1),
			(assign, reg32, ":troop_slot"),
			(assign, reg33, ":value_slot"),
			(display_message, "@DEBUG (ALS): {s32} set to {reg31}.  Moved from slot {reg32} of {s31} -> {reg33} of ALS_OBJECTS."),
		(try_end),
		# Weapon 1 Type
		(troop_get_slot, reg1, "$als_troop", slot_troop_upgrade_weapon_1_type),
		(troop_set_slot, ALS_OBJECTS, als_val_menu_weapon_type_0, reg1),
		# Weapon 2 Type
		(troop_get_slot, reg1, "$als_troop", slot_troop_upgrade_weapon_2_type),
		(troop_set_slot, ALS_OBJECTS, als_val_menu_weapon_type_1, reg1),
		# Weapon 3 Type
		(troop_get_slot, reg1, "$als_troop", slot_troop_upgrade_weapon_3_type),
		(troop_set_slot, ALS_OBJECTS, als_val_menu_weapon_type_2, reg1),
		# Weapon 4 Type
		(troop_get_slot, reg1, "$als_troop", slot_troop_upgrade_weapon_4_type),
		(troop_set_slot, ALS_OBJECTS, als_val_menu_weapon_type_3, reg1),
		# Weight Limit
		(troop_get_slot, reg1, "$als_troop", slot_troop_weight_limit),
		(troop_set_slot, ALS_OBJECTS, als_val_menu_weight_limit, reg1),
		
		# Enable Autoloot
		(troop_get_slot, reg1, "$als_troop", slot_troop_enable_autolooting),
		(troop_set_slot, ALS_OBJECTS, als_val_checkbox_enable, reg1),
		# Do not break weapon sets.
		(troop_get_slot, reg1, "$als_troop", slot_troop_prevent_breaking_sets),
		(troop_set_slot, ALS_OBJECTS, als_val_checkbox_no_break_sets, reg1),
		# Retain heraldic equipment.
		(troop_get_slot, reg1, "$als_troop", slot_troop_retain_heraldic_items),
		(troop_set_slot, ALS_OBJECTS, als_val_checkbox_heraldic_items, reg1),
	]),
	
# script_als_party_begin_autolooting
# Cycles through the party finding qualified companions ready to upgrade items then attempts to find what they will upgrade to.
# Input: none
# Output: none
("als_party_begin_autolooting",
    [
		(party_get_num_companion_stacks, ":stack_limit", "p_main_party"),
		(assign, ":grab_next", 0),
		(try_for_range, ":stack_no", 0, ":stack_limit"),
			(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
			(try_begin),
				(eq, ":troop_no", "$alc_troop"),
				(assign, ":grab_next", 1),
			(try_end),
			(try_begin),
				### DIAGNOSTIC ###
				(ge, DEBUG_ALS, 2),
				(assign, reg31, ":grab_next"),
				(assign, reg32, ":stack_no"),
				(str_store_troop_name, s31, ":troop_no"),
				(str_store_troop_name, s32, "$alc_troop"),
				(str_store_troop_name, s33, "$next_looting_troop"),
				(display_message, "@DEBUG (ALS): stack #{reg32}, troop: {s31}, $alc_troop: {s32}, $next_looter: {s33}, grab_next: {reg31}."),
			(try_end),
			(is_between, ":troop_no", companions_begin, companions_end),
			(troop_slot_eq, ":troop_no", slot_troop_enable_autolooting, 1),
			(neq, ":troop_no", "$alc_troop"),
			(eq, ":grab_next", 1),
			(assign, "$next_looting_troop", ":troop_no"),
			(assign, ":stack_no", ":stack_limit"),
			(assign, ":grab_next", 0),
		(try_end),
		
		# Troop Qualified
		(try_begin),
			(neq, "$next_looting_troop", "$alc_troop"),
			(call_script, "script_als_troop_begin_autolooting", "$next_looting_troop"),
		(else_try),
			(display_message, "@Picking through the spoils, your companions have found nothing else worth using.", gpu_light_blue),
		(try_end),
	]),
	
# script_als_troop_begin_autolooting
# Determines what the skills of the looting troop are and what items would be best for them based on their settings.
# Input:  Companion (troop #)
# Output: none
("als_troop_begin_autolooting",
    [
		(store_script_param, ":troop_no", 1),
		
		(try_for_range, ":slot", 0, 50),
			(troop_set_slot, ALS_TRADE_CONFIRM, ":slot", -1),
			(troop_set_slot, ALS_OLD_ITEM, ":slot", -1),
			(troop_set_slot, ALS_NEW_ITEM, ":slot", -1),
			(troop_set_slot, ALS_LOOTER, ":slot", -1),
		(try_end),
		
		(assign, ":storage_slot", 0),
		
		(try_for_range, ":equipment_slot", 0, 9),
			# Verify we want to upgrade this equipment slot on this troop.
			(store_add, ":setting_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
			(neg|troop_slot_eq, ":troop_no", ":setting_slot", 0), # Troop wants to upgrade.
			(troop_slot_ge, ":troop_no", ":setting_slot", 1), # Troop wants to upgrade.
			
			### DIAGNOSTIC+ ###
			# ek_item_0 = 0
			# ek_item_1 = 1
			# ek_item_2 = 2
			# ek_item_3 = 3
			# ek_head   = 4
			# ek_body   = 5
			# ek_foot   = 6
			# ek_gloves = 7
			# ek_horse  = 8
			
			(try_begin),
				(ge, DEBUG_ALS, 1),
				(assign, reg31, ":equipment_slot"),
				(try_begin),
					(eq, ":equipment_slot", ek_item_0),
					(str_store_string, s31, "@Weapon Slot #1"),
				(else_try),
					(eq, ":equipment_slot", ek_item_1),
					(str_store_string, s31, "@Weapon Slot #2"),
				(else_try),
					(eq, ":equipment_slot", ek_item_2),
					(str_store_string, s31, "@Weapon Slot #3"),
				(else_try),
					(eq, ":equipment_slot", ek_item_3),
					(str_store_string, s31, "@Weapon Slot #4"),
				(else_try),
					(eq, ":equipment_slot", ek_head),
					(str_store_string, s31, "@Head"),
				(else_try),
					(eq, ":equipment_slot", ek_body),
					(str_store_string, s31, "@Body"),
				(else_try),
					(eq, ":equipment_slot", ek_foot),
					(str_store_string, s31, "@Foot"),
				(else_try),
					(eq, ":equipment_slot", ek_gloves),
					(str_store_string, s31, "@Gloves"),
				(else_try),
					(eq, ":equipment_slot", ek_horse),
					(str_store_string, s31, "@Mount"),
				(else_try),
					(str_store_string, s31, "@Undefined"),
				(try_end),
				(display_message, "@DEBUG (ALS): NOW SEARCHING FOR SLOT [ {s31} ]:", gpu_debug),
			(try_end),
			### DIAGNOSTIC- ###
			
			# See what the character is currently using there.
			(troop_get_inventory_slot, ":item_equipped", ":troop_no", ":equipment_slot"),
			(try_begin),
				(ge, ":item_equipped", 1), # A valid item exists here.
				(troop_get_inventory_slot_modifier, ":imod_equipped", ":troop_no", ":equipment_slot"),
				(call_script, "script_als_get_item_rating", ":troop_no", ":item_equipped", ":imod_equipped"),
				(assign, ":score_equipped", reg1),
				# If this current item doesn't fit our settings it should have its rating cut in half to make exchanging it easier.
				(call_script, "script_als_troop_can_use_item", ":troop_no", ":item_equipped", ":imod_equipped", ":equipment_slot"),
				(try_begin),
					(eq, reg1, 0),
					(val_div, ":score_equipped", 2),
				(try_end),
				(assign, ":item_best", ":item_equipped"),
				(assign, ":slot_best", ":equipment_slot"),
				(assign, ":score_best", ":score_equipped"),
			(else_try),
				## Nothing equipped there ##
				(assign, ":item_best", -1),
				(assign, ":slot_best", -1),
				(assign, ":score_best", -1),
			(try_end),
			
			# Cycle through the pool looking for something better.
			(troop_get_inventory_capacity, ":inv_cap", "$pool_troop"),
			(try_for_range, ":i_slot", 0, ":inv_cap"),
				(troop_get_inventory_slot, ":item_loot", "$pool_troop", ":i_slot"),
				(ge, ":item_loot", 1),
				(assign, ":continue", 1),
				(try_begin),
					(eq, "$pool_troop", "trp_player"),
					# Player inventory search so prevent certain items from being taken.
					(assign, ":continue", 0),
					(ge, ":i_slot", 9), # Don't steal the player's actual equipped items.
					(assign, ":continue", 1),
					(call_script, "script_cf_dws_item_in_a_weapon_set", "trp_player", ":item_loot"), # Don't steal a player's backup DWS item.
					(assign, ":continue", 0),
				(try_end),
				(eq, ":continue", 1),
				(troop_get_inventory_slot_modifier, ":imod_loot", "$pool_troop", ":i_slot"),
				(call_script, "script_als_troop_can_use_item", ":troop_no", ":item_loot", ":imod_loot", ":equipment_slot"), # i_slot
				(eq, reg1, 1), # The item can be used by this troop.
				(call_script, "script_als_get_item_rating", ":troop_no", ":item_loot", ":imod_loot"),
				(gt, reg1, ":score_best"),
				(assign, ":item_score", reg1),
				(item_get_type, ":item_type", ":item_loot"),
				
				(assign, ":continue", 0),

				(try_begin),
					(eq, ":item_type", itp_type_one_handed_wpn),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_one_hand),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_two_handed_wpn),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_two_hand),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_polearm),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(this_or_next|troop_slot_eq, ":troop_no", ":upgrade_slot", als_polearm),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_lance),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_arrows),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_arrows),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_bolts),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_bolts),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_bow),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(this_or_next|troop_slot_eq, ":troop_no", ":upgrade_slot", als_bow_mounted),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_bow_unmounted),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_crossbow),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(this_or_next|troop_slot_eq, ":troop_no", ":upgrade_slot", als_crossbow_mounted),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_crossbow_unmounted),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_thrown),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_throwing),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_shield),
					(is_between, ":equipment_slot", 0, 4),
					(store_add, ":upgrade_slot", slot_troop_upgrade_weapon_1, ":equipment_slot"),
					(this_or_next|troop_slot_eq, ":troop_no", ":upgrade_slot", als_shield_mounted),
					(troop_slot_eq, ":troop_no", ":upgrade_slot", als_shield_unmounted),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_head_armor),
					(eq, ":equipment_slot", ek_head),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_body_armor),
					(eq, ":equipment_slot", ek_body),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_foot_armor),
					(eq, ":equipment_slot", ek_foot),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_hand_armor),
					(eq, ":equipment_slot", ek_gloves),
					(assign, ":continue", 1),
				(else_try),
					(eq, ":item_type", itp_type_horse),
					(eq, ":equipment_slot", ek_horse),
					(assign, ":continue", 1),
				(try_end),
				
				# Make sure that the item we want to use isn't already selected for another slot.
				(eq, ":continue", 1),
				(try_for_range, ":upgrade_slots", 0, 9),
					(troop_slot_eq, ALS_NEW_ITEM, ":upgrade_slots", ":i_slot"),
					(assign, ":continue", 0),
					(ge, DEBUG_ALS, 1),
					(str_store_item_name, s31, ":item_loot"),
					(assign, reg31, ":i_slot"),
					(display_message, "@Item '{s31}' in slot {reg31} blocked from continuing because it has already been previously selected."),
				(try_end),
				
				(eq, ":continue", 1),
				(try_begin),
					(ge, DEBUG_ALS, 2),
					(store_add, ":string_no", "str_als_label_slot_1", ":equipment_slot"),
					(store_add, ":item_type_string", "str_alc_itp_type_horse", ":item_type"),
					(val_sub, ":item_type_string", 1),
					(str_store_item_name, s21, ":item_loot"),
					(str_store_string, s22, ":string_no"),
					(str_store_string, s23, ":item_type_string"),
					(display_message, "@DEBUG (ALS): Item '{s21}' is type [{s23}] vs. slot [{s22}]."),
				(try_end),
				
				(assign, ":item_best", ":item_loot"),
				(assign, ":slot_best", ":i_slot"),
				(assign, ":score_best", ":item_score"),
			(try_end),
			
			# Assuming a better item has been found store it for presentation display.
			(neq, ":item_best", ":item_equipped"),
			(troop_set_slot, ALS_TRADE_CONFIRM, ":storage_slot", 1),
			(troop_set_slot, ALS_OLD_ITEM, ":storage_slot", ":equipment_slot"),
			(troop_set_slot, ALS_NEW_ITEM, ":storage_slot", ":slot_best"),
			(troop_set_slot, ALS_LOOTER, ":storage_slot", ":troop_no"),
			(try_begin),
				(ge, DEBUG_ALS, 2),
				(assign, reg21, ":storage_slot"),
				(try_begin),
					(ge, ":item_equipped", 1),
					(str_store_item_name, s21, ":item_equipped"),
				(else_try),
					(str_store_string, s21, "@Empty Slot"),
				(try_end),
				(str_store_item_name, s22, ":item_best"),
				(display_message, "@DEBUG (ALS): Storage #{reg21} holds {s21} -> {s22} upgrade request."),
			(try_end),
			(val_add, ":storage_slot", 1),
		(try_end),
		
		# See how many upgrades are available.
		(assign, ":count", 0),
		(try_for_range, ":slot", 0, 15),
			(neg|troop_slot_eq, ALS_TRADE_CONFIRM, ":slot", -1),
			(val_add, ":count", 1),
		(try_end),
		
		(try_begin),
			(ge, ":count", 1),
			(eq, "$pool_troop", "trp_player"),
			(assign, "$alc_troop", ":troop_no"),
			# Ditch ALS presentation and start ALC presentation.
			(presentation_set_duration, 0),
			(assign, reg51, "prsnt_auto_loot_checklist"),
			(jump_to_menu, "mnu_als_jump_to_presentation"),
		(else_try),
			(ge, ":count", 1),
			(assign, "$alc_troop", ":troop_no"),
			(start_presentation, "prsnt_auto_loot_checklist"),
		(else_try),
			(eq, "$pool_troop", "trp_player"),
			(str_store_troop_name, s21, ":troop_no"),
			(display_message, "@{s21} found nothing to upgrade to in your inventory."),
		(else_try),
			(assign, "$alc_troop", ":troop_no"),
			(call_script, "script_als_party_begin_autolooting"),
		(try_end),
		
	]),
	
# script_als_troop_can_use_item
# Qualifies whether an item can be used by this troop based on his attributes, skills and current settings or not.
# Input:  Companion (troop #), Item (item #), Item Modifier, Equipment Slot
# Output: reg1 (0 - No, 1 - Yes)
("als_troop_can_use_item",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":item_no", 2),
		#(store_script_param, ":imod", 3),
		(store_script_param, ":equip_slot", 4),
		
		(item_get_type, ":item_type", ":item_no"),
		(item_get_difficulty, ":item_difficulty", ":item_no"),
		(set_fixed_point_multiplier, 100),
		(item_get_weight, ":item_weight", ":item_no"),
		
		(try_begin),
			(is_between, ":equip_slot", 0, 4),
			# Since it is a weapon then find out what kind of weapon the troop wants.
			(store_add, ":weapon_type", slot_troop_upgrade_weapon_1, ":equip_slot"),
			(store_add, ":type_slot", slot_troop_upgrade_weapon_1_type, ":equip_slot"),
			(troop_get_slot, ":desired_weapon_type", ":troop_no", ":weapon_type"),
			(troop_get_slot, ":desired_damage_type", ":troop_no", ":type_slot"),
			(assign, reg31, ":equip_slot"),
			# Now see if that is what we're comparing against.
			(item_get_swing_damage_type, ":swing_type", ":item_no"),
			(val_add, ":swing_type", 1),
			(item_get_thrust_damage_type, ":thrust_type", ":item_no"),
			(val_add, ":thrust_type", 1),
		(try_end),
		
		# Get troop skill & attribute requirements.
		(store_attribute_level, ":char_strength", ":troop_no", ca_strength),
		(store_skill_level, ":char_power_draw", "skl_power_draw", ":troop_no"),
		(store_skill_level, ":char_power_throw", "skl_power_throw", ":troop_no"),
		(store_skill_level, ":char_shield", "skl_shield", ":troop_no"),
		(store_skill_level, ":char_riding", "skl_riding", ":troop_no"),
		
		(assign, ":usable", 0),
		(str_clear, s51),
		(try_begin),
			### ONE HANDED WEAPONS ### - Requires strength.
			(eq, ":item_type", itp_type_one_handed_wpn),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(eq, ":desired_weapon_type", als_one_hand),
			# Check weapon damage type.
			(str_store_string, s51, "@Undesired damage type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_damage_type", ":swing_type"),
			(eq, ":desired_damage_type", 0), # Any type is okay.
			# See if player meets the pre-requisite attribute or skill.
			(str_store_string, s51, "@Inadequate STR : Slot {reg31}"), ## DIAGNOSTIC ##
			(ge, ":char_strength", ":item_difficulty"),
			(assign, ":usable", 1),
		(else_try),
			### TWO HANDED WEAPONS ### - Requires strength.
			(eq, ":item_type", itp_type_two_handed_wpn),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(eq, ":desired_weapon_type", als_two_hand),
			# Check weapon damage type.
			(str_store_string, s51, "@Undesired damage type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_damage_type", ":swing_type"),
			(eq, ":desired_damage_type", 0), # Any type is okay.
			# See if player meets the pre-requisite attribute or skill.
			(str_store_string, s51, "@Inadequate STR : Slot {reg31}"), ## DIAGNOSTIC ##
			(ge, ":char_strength", ":item_difficulty"),
			(assign, ":usable", 1),
		(else_try),
			### POLEARM WEAPONS ### - Requires strength.
			(eq, ":item_type", itp_type_polearm),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_polearm),
			(eq, ":desired_weapon_type", als_lance),
			# Make sure the polearm is a lance if that is specified.
			(str_store_string, s51, "@Not a lance : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_polearm),
			(item_has_property, ":item_no", itp_couchable),
			# Check weapon damage type.
			(str_store_string, s51, "@Undesired damage type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_damage_type", ":swing_type"),
			(eq, ":desired_damage_type", 0), # Any type is okay.
			# See if player meets the pre-requisite attribute or skill.
			(str_store_string, s51, "@Inadequate STR : Slot {reg31}"), ## DIAGNOSTIC ##
			(ge, ":char_strength", ":item_difficulty"),
			(assign, ":usable", 1),
		(else_try),
			### CROSSBOWS ### - Requires strength.
			(eq, ":item_type", itp_type_crossbow),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_crossbow_mounted),
			(eq, ":desired_weapon_type", als_crossbow_unmounted),
			# Check if the item can be used on a mount if mounted weapon type is desired.
			(str_store_string, s51, "@Not usable mounted : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_crossbow_unmounted),
			(neg|item_has_property, ":item_no", itp_cant_use_on_horseback),
			(str_store_string, s51, "@Not reloadable mounted : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_crossbow_unmounted),
			(neg|item_has_property, ":item_no", itp_cant_reload_on_horseback),
			# Check weapon damage type.
			(str_store_string, s51, "@Undesired damage type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_damage_type", ":thrust_type"),
			(eq, ":desired_damage_type", 0), # Any type is okay.
			# See if player meets the pre-requisite attribute or skill.
			(str_store_string, s51, "@Inadequate STR : Slot {reg31}"), ## DIAGNOSTIC ##
			(ge, ":char_strength", ":item_difficulty"),
			(assign, ":usable", 1),
		(else_try),
			### BOWS ### - Requires power draw.
			(eq, ":item_type", itp_type_bow),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_bow_mounted),
			(eq, ":desired_weapon_type", als_bow_unmounted),
			# Check if the item can be used on a mount if mounted weapon type is desired.
			(str_store_string, s51, "@Not usable mounted : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_bow_unmounted),
			(neg|item_has_property, ":item_no", itp_cant_use_on_horseback),
			(str_store_string, s51, "@Not reloadable mounted : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_bow_unmounted),
			(neg|item_has_property, ":item_no", itp_cant_reload_on_horseback),
			# Check weapon damage type.
			(str_store_string, s51, "@Undesired damage type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_damage_type", ":thrust_type"),
			(eq, ":desired_damage_type", 0), # Any type is okay.
			# See if player meets the pre-requisite attribute or skill.
			(str_store_string, s51, "@Inadequate Power Draw : Slot {reg31}"), ## DIAGNOSTIC ##
			(ge, ":char_power_draw", ":item_difficulty"),
			(assign, ":usable", 1),
		(else_try),
			### THROWN ITEMS ### - Requires power throw.
			(eq, ":item_type", itp_type_thrown),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(eq, ":desired_weapon_type", als_throwing),
			# Check weapon damage type.
			(str_store_string, s51, "@Undesired damage type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_damage_type", ":thrust_type"),
			(eq, ":desired_damage_type", 0), # Any type is okay.
			# See if player meets the pre-requisite attribute or skill.
			(str_store_string, s51, "@Inadequate Power Throw : Slot {reg31}"), ## DIAGNOSTIC ##
			(ge, ":char_power_throw", ":item_difficulty"),
			(assign, ":usable", 1),
		(else_try),
			### SHIELDS ### - Requires shield.
			(eq, ":item_type", itp_type_shield),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_shield_mounted),
			(eq, ":desired_weapon_type", als_shield_unmounted),
			# Check if the item can be used on a mount if mounted weapon type is desired.
			(str_store_string, s51, "@Not usable mounted : Slot {reg31}"), ## DIAGNOSTIC ##
			(this_or_next|eq, ":desired_weapon_type", als_shield_unmounted),
			(neg|item_has_property, ":item_no", itp_cant_use_on_horseback),
			(str_store_string, s51, "@Inadequate Shield Skill : Slot {reg31}"), ## DIAGNOSTIC ##
			(ge, ":char_shield", ":item_difficulty"),
			(assign, ":usable", 1),
		(else_try),
			### MOUNTS ### - Requires riding.
			(eq, ":item_type", itp_type_horse),
			(str_store_string, s51, "@We're not looking for mounts."), ## DIAGNOSTIC ##
			(eq, ":equip_slot", ek_horse), # We're looking for armor.
			(str_store_string, s51, "@Mounts are not being upgraded"), ## DIAGNOSTIC ##
			(troop_slot_ge, ":troop_no", slot_troop_upgrade_mount, 1), # We're upgrading horses.
			(str_store_string, s51, "@Inadequate Riding Skill"), ## DIAGNOSTIC ##
			(ge, ":char_riding", ":item_difficulty"),
			(assign, ":usable", 1),
		(else_try),
			### ARMOR (head) ### - Requires strength.
			(eq, ":item_type", itp_type_head_armor),
			(str_store_string, s51, "@We're not looking for head armor."), ## DIAGNOSTIC ##
			(eq, ":equip_slot", ek_head), # We're looking for armor.
			(str_store_string, s51, "@Head armor not being upgraded"), ## DIAGNOSTIC ##
			(troop_slot_eq, ":troop_no", slot_troop_upgrade_helm, 1), # We're upgrading head armor.
			(str_store_string, s51, "@Strength requirement too high"), ## DIAGNOSTIC ##
			(ge, ":char_strength", ":item_difficulty"),
			# Ensure this item isn't too encumbering.  If troop set to ignore armor restrictions the neg checks should pass through.
			(str_store_string, s51, "@Weight exceeds light armor restriction"), ## DIAGNOSTIC ##
			(this_or_next|lt, ":item_weight", als_head_armor_light),
			(neg|troop_slot_eq, ":troop_no", slot_troop_weight_limit, als_limit_armor_light),
			(str_store_string, s51, "@Weight exceeds medium armor restriction"), ## DIAGNOSTIC ##
			(this_or_next|lt, ":item_weight", als_head_armor_medium),
			(neg|troop_slot_eq, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
			(assign, ":usable", 1),
		(else_try),
			### ARMOR (body) ### - Requires strength.
			(eq, ":item_type", itp_type_body_armor),
			(str_store_string, s51, "@We're not looking for body armor."), ## DIAGNOSTIC ##
			(eq, ":equip_slot", ek_body), # We're looking for armor.
			(str_store_string, s51, "@Body armor not being upgraded"), ## DIAGNOSTIC ##
			(troop_slot_eq, ":troop_no", slot_troop_upgrade_armor, 1), # We're upgrading body armor.
			(str_store_string, s51, "@Strength requirement too high"), ## DIAGNOSTIC ##
			(ge, ":char_strength", ":item_difficulty"),
			# Ensure this item isn't too encumbering.  If troop set to ignore armor restrictions the neg checks should pass through.
			(str_store_string, s51, "@Weight exceeds light armor restriction"), ## DIAGNOSTIC ##
			(this_or_next|lt, ":item_weight", als_body_armor_light),
			(neg|troop_slot_eq, ":troop_no", slot_troop_weight_limit, als_limit_armor_light),
			(str_store_string, s51, "@Weight exceeds medium armor restriction"), ## DIAGNOSTIC ##
			(this_or_next|lt, ":item_weight", als_body_armor_medium),
			(neg|troop_slot_eq, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
			(assign, ":usable", 1),
		(else_try),
			### ARMOR (legs) ### - Requires strength.
			(eq, ":item_type", itp_type_foot_armor),
			(str_store_string, s51, "@We're not looking for leg armor."), ## DIAGNOSTIC ##
			(eq, ":equip_slot", ek_foot), # We're looking for armor.
			(str_store_string, s51, "@Leg armor not being upgraded"), ## DIAGNOSTIC ##
			(troop_slot_eq, ":troop_no", slot_troop_upgrade_boots, 1), # We're upgrading leg armor.
			(str_store_string, s51, "@Strength requirement too high"), ## DIAGNOSTIC ##
			(ge, ":char_strength", ":item_difficulty"),
			# Ensure this item isn't too encumbering.  If troop set to ignore armor restrictions the neg checks should pass through.
			(str_store_string, s51, "@Weight exceeds light armor restriction"), ## DIAGNOSTIC ##
			(this_or_next|lt, ":item_weight", als_foot_armor_light),
			(neg|troop_slot_eq, ":troop_no", slot_troop_weight_limit, als_limit_armor_light),
			(str_store_string, s51, "@Weight exceeds medium armor restriction"), ## DIAGNOSTIC ##
			(this_or_next|lt, ":item_weight", als_foot_armor_medium),
			(neg|troop_slot_eq, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
			(assign, ":usable", 1),
		(else_try),
			### ARMOR (hands) ### - Requires strength.
			(eq, ":item_type", itp_type_hand_armor),
			(str_store_string, s51, "@We're not looking for hand armor."), ## DIAGNOSTIC ##
			(eq, ":equip_slot", ek_gloves), # We're looking for armor.
			(str_store_string, s51, "@Hand armor not being upgraded"), ## DIAGNOSTIC ##
			(troop_slot_eq, ":troop_no", slot_troop_upgrade_gloves, 1), # We're upgrading hand armor.
			(str_store_string, s51, "@Strength requirement too high"), ## DIAGNOSTIC ##
			(ge, ":char_strength", ":item_difficulty"),
			# Ensure this item isn't too encumbering.  If troop set to ignore armor restrictions the neg checks should pass through.
			(str_store_string, s51, "@Weight exceeds light armor restriction"), ## DIAGNOSTIC ##
			(this_or_next|lt, ":item_weight", als_hand_armor_light),
			(neg|troop_slot_eq, ":troop_no", slot_troop_weight_limit, als_limit_armor_light),
			(str_store_string, s51, "@Weight exceeds medium armor restriction"), ## DIAGNOSTIC ##
			(this_or_next|lt, ":item_weight", als_hand_armor_medium),
			(neg|troop_slot_eq, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
			(assign, ":usable", 1),
		(else_try),
			### BOLTS ### - No requirement.
			(eq, ":item_type", itp_type_bolts),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(eq, ":desired_weapon_type", als_bolts),
			(assign, ":usable", 1),
		(else_try),
			### ARROWS ### - No requirement.
			(eq, ":item_type", itp_type_arrows),
			# Ensure the item we are looking at is the correct type.
			(str_store_string, s51, "@We're not looking for weapons."), ## DIAGNOSTIC ##
			(is_between, ":equip_slot", 0, 4), # We're looking for weapons.
			(str_store_string, s51, "@Undesired item type : Slot {reg31}"), ## DIAGNOSTIC ##
			(eq, ":desired_weapon_type", als_arrows),
			(assign, ":usable", 1),
		(try_end),
		
		(try_begin),
			(eq, ":usable", 1),
			(str_store_string, s51, "@Usable"), ## DIAGNOSTIC ##
		(try_end),
		
		### DIAGNOSTIC ###
		(try_begin),
			(ge, DEBUG_ALS, 1),
			(this_or_next|eq, ":usable", 1), ### TESTING LIMITATION ###
			(ge, DEBUG_ALS, 2),
			(neq, "$debug_als_usable_item", ":item_no"),
			(str_store_item_name, s21, ":item_no"),
			(str_store_troop_name, s22, ":troop_no"),
			(assign, reg21, ":usable"),
			(try_begin),
				(eq, ":usable", 1),
				(str_clear, s31),
			(else_try),
				(str_store_string, s31, "@  {s51}"),
			(try_end),
			(display_message, "@Item '{s21}' is {reg21?usable:not usable} by {s22}.{s31}"),
			(assign, "$debug_als_usable_item", ":item_no"),
		(try_end),
		
		(assign, reg1, ":usable"),
	]),
	
# script_als_get_item_rating
# Based upon the item requested and the modifiers on it this will return a score for that item.
# Input:  Companion (troop #), Item (item #), Item Modifier
# Output: reg1 (rating score)
("als_get_item_rating",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":item_no", 2),
		(store_script_param, ":imod", 3),
		
		(try_begin),
			(ge, ":item_no", 1),
			(item_get_type, ":item_type", ":item_no"),
		(else_try),
			(assign, ":item_type", -1),
		(try_end),
		
		(assign, ":rating", 0),
		
		# Get basic score of item.
		(try_begin),
			### MELEE WEAPONS ###
			(this_or_next|eq, ":item_type", itp_type_one_handed_wpn),
			(this_or_next|eq, ":item_type", itp_type_two_handed_wpn),
			(eq, ":item_type", itp_type_polearm),
			# Item is definitely a MELEE weapon.
			(call_script, "script_cms_get_melee_weapon_ratings", ":item_no", ":imod", 0),
			(assign, ":rating", reg1),
			
		(else_try),
			### RANGED WEAPONS ###
			(this_or_next|eq, ":item_type", itp_type_bow),
			(this_or_next|eq, ":item_type", itp_type_crossbow),
			(eq, ":item_type", itp_type_thrown),
			# Item is definitely a RANGED weapon.
			(call_script, "script_cms_get_ranged_weapon_ratings", ":item_no", ":imod", 0),
			(assign, ":rating", reg1),
		
		(else_try),
			### AMMUNITION ###
			(this_or_next|eq, ":item_type", itp_type_arrows),
			(eq, ":item_type", itp_type_bolts),
			# Item is definitely AMMUNITION.
			(call_script, "script_cms_get_ammo_ratings", ":item_no", ":imod", 0),
			(assign, ":rating", reg1),
		
		(else_try),
			### ARMOR ###
			(this_or_next|eq, ":item_type", itp_type_head_armor),
			(this_or_next|eq, ":item_type", itp_type_body_armor),
			(this_or_next|eq, ":item_type", itp_type_foot_armor),
			(eq, ":item_type", itp_type_hand_armor),
			# Item is definitely ARMOR.
			(call_script, "script_cms_get_armor_ratings", ":item_no", ":imod", 0, ":troop_no"),
			(assign, ":rating", reg1),
		
		(else_try),
			### SHIELD ###
			(eq, ":item_type", itp_type_shield),
			# Item is definitely a SHIELD.
			(call_script, "script_cms_get_shield_ratings", ":item_no", ":imod", 0, ":troop_no"),
			(assign, ":rating", reg1),
		
		(else_try),
			### MOUNTS ###
			(eq, ":item_type", itp_type_horse),
			# Item is definitely a MOUNT.
			(call_script, "script_cms_get_mount_ratings", ":item_no", ":imod", 0, ":troop_no"),
			(assign, ":rating", reg1),
		
		(try_end),
		
		(assign, reg1, ":rating"),
	]),
	
# script_cms_get_mount_ratings
# PURPOSE: Determines the autoloot rating of a mount item.
# EXAMPLE: (call_script, "script_cms_get_mount_ratings", ":item_no", ":imod", 0, ":troop_no"),
  ("cms_get_mount_ratings",
    [
		(store_script_param, ":item_no", 1),
		(store_script_param, ":imod", 2),
		(store_script_param, ":slot", 3),
		(store_script_param, ":troop_no", 4),
		
		# Item is definitely a MOUNT.
		(item_get_body_armor, ":horse_armor", ":item_no"),
		(item_get_horse_speed, ":horse_speed", ":item_no"),
		(item_get_horse_maneuver, ":horse_maneuver", ":item_no"),
		(item_get_hit_points, ":horse_health", ":item_no"),
		
		# Implement modifier value improvements.
		(try_begin),
			(eq, ":imod", imod_cracked),
			(val_add, ":horse_health", -46),
			(val_add, ":horse_armor", -4),
		(else_try),
			(eq, ":imod", imod_rusty),
			(val_add, ":horse_armor", -3),
		(else_try),
			(eq, ":imod", imod_battered),
			(val_add, ":horse_health", -26),
			(val_add, ":horse_armor", -2),
		(else_try),
			(eq, ":imod", imod_crude),
			(val_add, ":horse_armor", -1),
		(else_try),
			(eq, ":imod", imod_heavy),
			(val_add, ":horse_health", 10),
			(val_add, ":horse_armor", 3),
		(else_try),
			(eq, ":imod", imod_tattered),
			(val_add, ":horse_armor", -3),
		(else_try),
			(eq, ":imod", imod_ragged),
			(val_add, ":horse_armor", -2),
		(else_try),
			(eq, ":imod", imod_sturdy),
			(val_add, ":horse_armor", 1),
		(else_try),
			(eq, ":imod", imod_thick),
			(val_add, ":horse_health", 47),
			(val_add, ":horse_armor", 2),
		(else_try),
			(eq, ":imod", imod_hardened),
			(val_add, ":horse_armor", 3),
		(else_try),
			(eq, ":imod", imod_reinforced),
			(val_add, ":horse_health", 83),
			(val_add, ":horse_armor", 4),
		(else_try),
			(eq, ":imod", imod_lordly),
			(val_add, ":horse_health", 155),
			(val_add, ":horse_armor", 6),
		(else_try),
			(eq, ":imod", imod_lame),
			(val_add, ":horse_speed", -10),
			(val_add, ":horse_maneuver", -5),
		(else_try),
			(eq, ":imod", imod_swaybacked),
			(val_add, ":horse_speed", -4),
			(val_add, ":horse_maneuver", -2),
		(else_try),
			(eq, ":imod", imod_stubborn),
			(val_add, ":horse_health", 5),
		(else_try),
			(eq, ":imod", imod_spirited),
			(val_add, ":horse_speed", 2),
			(val_add, ":horse_maneuver", 1),
		(else_try),
			(eq, ":imod", imod_champion),
			(val_add, ":horse_speed", 4),
			(val_add, ":horse_maneuver", 2),
		(try_end),
		
		# Set some baseline values to compare against.
		(assign, ":baseline_health",   MOUNT_BASELINE_HEALTH),
		(assign, ":baseline_speed",    MOUNT_BASELINE_SPEED),
		(assign, ":baseline_maneuver", MOUNT_BASELINE_MANEUVER),
		(assign, ":baseline_armor",    MOUNT_BASELINE_ARMOR),
		
		# Now convert raw data to baseline % values.
		# Health
		(store_mul, ":score_health", ":horse_health", 100),
		(val_div, ":score_health", ":baseline_health"),
		# Speed
		(store_mul, ":score_speed", ":horse_speed", 100),
		(val_div, ":score_speed", ":baseline_speed"),
		# Maneuver
		(store_mul, ":score_maneuver", ":horse_maneuver", 100),
		(val_div, ":score_maneuver", ":baseline_maneuver"),
		# Armor
		(store_mul, ":score_armor", ":horse_armor", 100),
		(val_div, ":score_armor", ":baseline_armor"),
		
		# Lets find out what kind of mount upgrade this troop wants.
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_upgrade_mount, als_mount_fastest),
			(val_mul, ":score_speed", 2),
			(val_mul, ":score_maneuver", 2),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_upgrade_mount, als_mount_resilient),
			(val_mul, ":score_armor", 2),
			(val_mul, ":score_health", 2),
		(try_end),
		
		# Combine everything to get our item's rating.
		(assign, ":rating", ":score_speed"),
		(val_add, ":rating", ":score_maneuver"),
		(val_add, ":rating", ":score_armor"),
		(val_add, ":rating", ":score_health"),
		
		# Bonus rating given to heraldic items.
		(try_begin),
			(call_script, "script_cf_als_item_is_heraldic", ":item_no"),
			(troop_slot_eq, ":troop_no", slot_troop_retain_heraldic_items, 1),    # We are specifically interested in heraldic items.
			(val_add, ":rating", 1000),
		(try_end),
		
		# Diagnostic
		(try_begin),
			(ge, DEBUG_ALS, 2),
			(neq, "$debug_als_item_rated", ":item_no"),
			(str_store_item_name, s21, ":item_no"),
			(assign, reg21, ":score_speed"),
			(assign, reg22, ":score_maneuver"),
			(assign, reg23, ":score_health"),
			(assign, reg24, ":score_armor"),
			(assign, reg25, ":rating"),
			(display_message, "@Item '{s21}': {reg21}% speed + {reg22}% maneuver + {reg23}% health + {reg24}% armor = {reg25} Rating"),
			(assign, "$debug_als_item_rated", ":item_no"),
		(try_end),
		
		(try_begin),
			## COMBINED RATINGS
			(eq, ":slot", 0),
			(assign, reg1, ":rating"),
		(else_try),
			## ARMOR
			(eq, ":slot", 1),
			(assign, reg1, ":score_armor"),
		(else_try),
			## SPEED
			(eq, ":slot", 2),
			(assign, reg1, ":score_speed"),
		(else_try),
			## MANEUVER
			(eq, ":slot", 3),
			(assign, reg1, ":score_maneuver"),
		(else_try),
			## HEALTH
			(eq, ":slot", 4),
			(assign, reg1, ":score_health"),
		(try_end),
	]),
	
# script_cms_get_shield_ratings
# PURPOSE: Determines the autoloot rating of a shield item.
# EXAMPLE: (call_script, "script_cms_get_shield_ratings", ":item_no", ":imod", 0, ":troop_no"),
  ("cms_get_shield_ratings",
    [
		(store_script_param, ":item_no", 1),
		(store_script_param, ":imod", 2),
		(store_script_param, ":slot", 3),
		(store_script_param, ":troop_no", 4),
		
		# Item is definitely a SHIELD.
		(item_get_body_armor, ":shield_resist", ":item_no"),
		(item_get_shield_width, ":shield_width", ":item_no"),
		(item_get_shield_height, ":shield_height", ":item_no"),
		(item_get_hit_points, ":shield_health", ":item_no"),
		
		# If height = 0 due to a round shield make it equal the same value as width.
		(try_begin),
			(lt, ":shield_height", 1),
			(assign, ":shield_height", ":shield_width"),
		(try_end),
		
		# Implement modifier value improvements.
		(try_begin),
			(eq, ":imod", imod_cracked),
			(val_add, ":shield_health", -46),
			(val_add, ":shield_resist", -4),
		(else_try),
			(eq, ":imod", imod_battered),
			(val_add, ":shield_health", -26),
			(val_add, ":shield_resist", -2),
		(else_try),
			(eq, ":imod", imod_crude),
			(val_add, ":shield_resist", -1),
		(else_try),
			(eq, ":imod", imod_ragged),
			(val_add, ":shield_resist", -2),
		(else_try),
			(this_or_next|eq, ":imod", imod_rusty),
			(eq, ":imod", imod_tattered),
			(val_add, ":shield_resist", -3),
		(else_try),
			(eq, ":imod", imod_heavy),
			(val_add, ":shield_health", 10),
			(val_add, ":shield_resist", 3),
		(else_try),
			(eq, ":imod", imod_heavy),
			(val_add, ":shield_health", 10),
			(val_add, ":shield_resist", 3),
		(else_try),
			(eq, ":imod", imod_sturdy),
			(val_add, ":shield_resist", 1),
		(else_try),
			(eq, ":imod", imod_reinforced),
			(val_add, ":shield_health", 83),
			(val_add, ":shield_resist", 4),
		(else_try),
			(eq, ":imod", imod_lordly),
			(val_add, ":shield_health", 155),
			(val_add, ":shield_resist", 6),
		(else_try),
			(eq, ":imod", imod_stubborn),
			(val_add, ":shield_health", 5),
		(try_end),
		
		# Set some baseline values to compare against.
		(assign, ":baseline_health", SHIELD_BASELINE_HEALTH),
		(assign, ":baseline_resist", SHIELD_BASELINE_RESIST),
		(assign, ":baseline_width",  SHIELD_BASELINE_WIDTH),
		(assign, ":baseline_height", SHIELD_BASELINE_HEIGHT),
		
		# Now convert raw data to baseline % values.
		# Health
		(store_mul, ":score_health", ":shield_health", 100),
		(val_div, ":score_health", ":baseline_health"),
		# Resist
		(store_mul, ":score_resist", ":shield_resist", 100),
		(val_div, ":score_resist", ":baseline_resist"),
		# Width
		(store_mul, ":score_width", ":shield_width", 100),
		(val_div, ":score_width", ":baseline_width"),
		(val_div, ":score_width", 2),
		# Height
		(store_mul, ":score_height", ":shield_height", 100),
		(val_div, ":score_height", ":baseline_height"),
		(val_div, ":score_height", 2),
		
		# Combine everything to get our item's rating.
		(assign, ":rating", ":score_width"),
		(val_add, ":rating", ":score_height"),
		(val_add, ":rating", ":score_health"),
		(val_add, ":rating", ":score_resist"),
		
		# Check for heraldic bonus.
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_retain_heraldic_items, 1),
			(call_script, "script_cf_als_item_is_heraldic", ":item_no"),
			(store_div, ":heraldic_bonus", ":rating", 2),
			(val_add, ":rating", ":heraldic_bonus"),
		(try_end),
		
		# Diagnostic
		(try_begin),
			(ge, DEBUG_ALS, 2),
			(neq, "$debug_als_item_rated", ":item_no"),
			(str_store_item_name, s21, ":item_no"),
			(assign, reg21, ":score_width"),
			(assign, reg22, ":score_height"),
			(assign, reg23, ":score_health"),
			(assign, reg24, ":score_resist"),
			(assign, reg25, ":rating"),
			(display_message, "@Item '{s21}': {reg21}% width + {reg22}% height + {reg23}% health + {reg24}% resist = {reg25} Rating"),
			(assign, "$debug_als_item_rated", ":item_no"),
		(try_end),
		
		(try_begin),
			## COMBINED RATINGS
			(eq, ":slot", 0),
			(assign, reg1, ":rating"),
		(else_try),
			## HEALTH
			(eq, ":slot", 1),
			(assign, reg1, ":score_health"),
		(else_try),
			## RESIST
			(eq, ":slot", 2),
			(assign, reg1, ":score_resist"),
		(else_try),
			## WIDTH
			(eq, ":slot", 3),
			(assign, reg1, ":score_width"),
		(else_try),
			## HEIGHT
			(eq, ":slot", 4),
			(assign, reg1, ":score_height"),
		(try_end),
	]),
	
# script_cms_get_armor_ratings
# PURPOSE: Determines the autoloot rating of a armor item.
# EXAMPLE: (call_script, "script_cms_get_armor_ratings", ":item_no", ":imod", 0, ":troop_no"),
  ("cms_get_armor_ratings",
    [
		(store_script_param, ":item_no", 1),
		(store_script_param, ":imod", 2),
		(store_script_param, ":slot", 3),
		(store_script_param, ":troop_no", 4),
		
		# Item is definitely ARMOR.
		(item_get_head_armor, ":armor_head", ":item_no"),
		(item_get_body_armor, ":armor_body", ":item_no"),
		(item_get_leg_armor, ":armor_legs", ":item_no"),
		
		# Implement modifier value improvements.
		(assign, ":armor_bonus", 0),
		(try_begin),
			(eq, ":imod", imod_cracked),
			(val_add, ":armor_bonus", -4),
		(else_try),
			(this_or_next|eq, ":imod", imod_rusty),
			(eq, ":imod", imod_tattered),
			(val_add, ":armor_bonus", -3),
		(else_try),
			(this_or_next|eq, ":imod", imod_ragged),
			(eq, ":imod", imod_battered),
			(val_add, ":armor_bonus", -2),
		(else_try),
			(eq, ":imod", imod_crude),
			(val_add, ":armor_bonus", -1),
		(else_try),
			(eq, ":imod", imod_sturdy),
			(val_add, ":armor_bonus", 1),
		(else_try),
			(eq, ":imod", imod_thick),
			(val_add, ":armor_bonus", 2),
		(else_try),
			(this_or_next|eq, ":imod", imod_hardened),
			(eq, ":imod", imod_heavy),
			(val_add, ":armor_bonus", 3),
		(else_try),
			(eq, ":imod", imod_reinforced),
			(val_add, ":armor_bonus", 4),
		(else_try),
			(eq, ":imod", imod_lordly),
			(val_add, ":armor_bonus", 6),
		(try_end),
		
		# Add bonus intelligently based upon armor type.
		(item_get_type, ":item_type", ":item_no"),
		(try_begin), ## Head
			(eq, ":item_type", itp_type_head_armor),
			(val_add, ":armor_head", ":armor_bonus"),
		(else_try), ## Body / Hand
			(this_or_next|eq, ":item_type", itp_type_body_armor),
			(eq, ":item_type", itp_type_hand_armor),
			(val_add, ":armor_body", ":armor_bonus"),
		(else_try), ## Feet
			(eq, ":item_type", itp_type_foot_armor),
			(val_add, ":armor_legs", ":armor_bonus"),
		(try_end),
		
		# (val_add, ":armor_head", ":armor_bonus"),
		# (val_add, ":armor_body", ":armor_bonus"),
		# (val_add, ":armor_legs", ":armor_bonus"),
		
		# Set things back to 0 at a minimum in case their modifier knocked it lower.
		(val_max, ":armor_head", 0),
		(val_max, ":armor_body", 0),
		(val_max, ":armor_legs", 0),
		
		# Set some baseline values to compare against.
		(assign, ":baseline_head", ARMOR_BASELINE_HEAD),
		(assign, ":baseline_body", ARMOR_BASELINE_BODY),
		(assign, ":baseline_legs", ARMOR_BASELINE_LEGS),
		
		# Now convert raw data to baseline % values.
		# Head
		(store_mul, ":score_head", ":armor_head", 100),
		(val_div, ":score_head", ":baseline_head"),
		# Body
		(store_mul, ":score_body", ":armor_body", 100),
		(val_div, ":score_body", ":baseline_body"),
		# Legs
		(store_mul, ":score_legs", ":armor_legs", 100),
		(val_div, ":score_legs", ":baseline_legs"),
		
		# Combine everything to get our item's rating.
		(assign, ":rating", ":score_head"),
		(val_add, ":rating", ":score_body"),
		(val_add, ":rating", ":score_legs"),
		
		# Check for heraldic bonus.
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_retain_heraldic_items, 1),
			(call_script, "script_cf_als_item_is_heraldic", ":item_no"),
			(store_div, ":heraldic_bonus", ":rating", 2),
			(val_add, ":rating", ":heraldic_bonus"),
		(try_end),
		
		# Diagnostic
		(try_begin),
			(ge, DEBUG_ALS, 2),
			(neq, "$debug_als_item_rated", ":item_no"),
			(str_store_item_name, s21, ":item_no"),
			(assign, reg21, ":score_head"),
			(assign, reg22, ":score_body"),
			(assign, reg23, ":score_legs"),
			(assign, reg25, ":rating"),
			(display_message, "@Item '{s21}': {reg21}% head + {reg22}% body + {reg23}% legs = {reg25} Rating"),
			(assign, "$debug_als_item_rated", ":item_no"),
		(try_end),
		
		(try_begin),
			## COMBINED RATINGS
			(eq, ":slot", 0),
			(assign, reg1, ":rating"),
		(else_try),
			## HEAD
			(eq, ":slot", 1),
			(assign, reg1, ":score_head"),
		(else_try),
			## BODY
			(eq, ":slot", 2),
			(assign, reg1, ":score_body"),
		(else_try),
			## LEGS
			(eq, ":slot", 3),
			(assign, reg1, ":score_legs"),
		(try_end),
	]),
	
# script_cms_get_ammo_ratings
# PURPOSE: Determines the autoloot rating of a armor item.
# EXAMPLE: (call_script, "script_cms_get_ammo_ratings", ":item_no", ":imod", 0),
  ("cms_get_ammo_ratings",
    [
		(store_script_param, ":item_no", 1),
		(store_script_param, ":imod", 2),
		(store_script_param, ":slot", 3),
		
		# Item is definitely AMMUNITION.
		(item_get_thrust_damage, ":thrust_damage", ":item_no"),
		(item_get_max_ammo, ":ammo", ":item_no"),
		
		# Implement modifier value improvements.
		(try_begin),
			(eq, ":imod", imod_large_bag),
			(val_add, ":ammo", 6),
		(try_end),
		
		# Set some baseline values to compare against.
		(assign, ":baseline_damage", AMMO_BASELINE_DAMAGE),
		(assign, ":baseline_ammo",   AMMO_BASELINE_AMMO),
		
		# Now convert raw data to baseline % values.
		# Damage
		(store_mul, ":score_damage", ":thrust_damage", 100),
		(val_div, ":score_damage", ":baseline_damage"),
		# Ammunition
		(store_mul, ":score_ammo", ":ammo", 100),
		(val_div, ":score_ammo", ":baseline_ammo"),
		
		# Combine everything to get our item's rating.
		(assign, ":rating", ":score_damage"),
		(val_add, ":rating", ":score_ammo"),
		
		# Diagnostic
		(try_begin),
			(ge, DEBUG_ALS, 2),
			(neq, "$debug_als_item_rated", ":item_no"),
			(str_store_item_name, s21, ":item_no"),
			(assign, reg21, ":score_damage"),
			(assign, reg22, ":score_ammo"),
			(assign, reg25, ":rating"),
			(display_message, "@Item '{s21}': {reg21}% damage + {reg22}% ammo = {reg25} Rating"),
			(assign, "$debug_als_item_rated", ":item_no"),
		(try_end),
		
		(try_begin),
			## COMBINED RATINGS
			(eq, ":slot", 0),
			(assign, reg1, ":rating"),
		(else_try),
			## DAMAGE
			(eq, ":slot", 1),
			(assign, reg1, ":score_damage"),
		(else_try),
			## AMMO COUNT
			(eq, ":slot", 2),
			(assign, reg1, ":score_ammo"),
		(try_end),
	]),
	
# script_cms_get_ranged_weapon_ratings
# PURPOSE: Determines the autoloot rating of a armor item.
# EXAMPLE: (call_script, "script_cms_get_ranged_weapon_ratings", ":item_no", ":imod", 0),
  ("cms_get_ranged_weapon_ratings",
    [
		(store_script_param, ":item_no", 1),
		(store_script_param, ":imod", 2),
		(store_script_param, ":slot", 3),
		
		# Item is definitely a RANGED weapon.
		(item_get_thrust_damage, ":weapon_damage", ":item_no"),
		(item_get_thrust_damage_type, ":ranged_type", ":item_no"),
		(item_get_accuracy, ":ranged_accuracy", ":item_no"),
		(item_get_speed_rating, ":weapon_speed", ":item_no"),
		
		# Give accuracy some value if it is not being set by the mod.
		(try_begin),
			(eq, ":ranged_accuracy", 0),
			(assign, ":ranged_accuracy", 100),
		(try_end),
		
		# Implement modifier value improvements.
		(try_begin),
			(eq, ":imod", imod_cracked),
			(val_add, ":weapon_damage", -5),
		(else_try),
			(eq, ":imod", imod_rusty),
			(val_add, ":weapon_damage", -3),
		(else_try),
			(eq, ":imod", imod_bent),
			(val_add, ":weapon_damage", -3),
			(val_add, ":weapon_speed", -3),
		(else_try),
			(eq, ":imod", imod_chipped),
			(val_add, ":weapon_damage", 2), # -1
		(else_try),
			(eq, ":imod", imod_crude),
			(val_add, ":weapon_damage", -2),
		(else_try),
			(eq, ":imod", imod_fine),
			(val_add, ":weapon_damage", 1),
		(else_try),
			(eq, ":imod", imod_tempered),
			(val_add, ":weapon_damage", 4),
		(else_try),
			(eq, ":imod", imod_balanced),
			(val_add, ":weapon_damage", 3),
			(val_add, ":weapon_speed", 3),
		(else_try),
			(eq, ":imod", imod_masterwork),
			(val_add, ":weapon_damage", 5),
			(val_add, ":weapon_speed", 1),
		(else_try),
			(eq, ":imod", imod_heavy),
			(val_add, ":weapon_damage", 2),
			(val_add, ":weapon_speed", -2),
		(try_end),
		
		# Set some baseline values to compare against.
		(assign, ":baseline_damage",   RANGED_BASELINE_DAMAGE),
		(assign, ":baseline_accuracy", RANGED_BASELINE_ACCURACY),
		(assign, ":baseline_speed",    RANGED_BASELINE_SPEED),
		
		# Now convert raw data to baseline % values.
		# Damage
		(store_mul, ":score_damage", ":weapon_damage", 100),
		(val_div, ":score_damage", ":baseline_damage"),
		# Speed
		(store_mul, ":score_speed", ":weapon_speed", 100),
		(val_div, ":score_speed", ":baseline_speed"),
		# Accuracy
		(store_mul, ":score_accuracy", ":ranged_accuracy", 100),
		(val_div, ":score_accuracy", ":baseline_accuracy"),
		# Type
		(try_begin),
			(eq, ":ranged_type", cut),
			(assign, ":score_type", 50),
		(else_try),
			(eq, ":ranged_type", pierce),
			(assign, ":score_type", 150),
		(else_try),
			(eq, ":ranged_type", blunt),
			(assign, ":score_type", 100),
		(try_end),
		
		# Combine everything to get our item's rating.
		(assign, ":rating", ":score_damage"),
		(val_add, ":rating", ":score_type"),
		(val_add, ":rating", ":score_speed"),
		(val_add, ":rating", ":score_accuracy"),
		
		# Diagnostic
		(try_begin),
			(ge, DEBUG_ALS, 1),
			(neq, "$debug_als_item_rated", ":item_no"),
			(str_store_item_name, s21, ":item_no"),
			(assign, reg21, ":score_damage"),
			(assign, reg22, ":score_type"),
			(assign, reg23, ":score_speed"),
			(assign, reg24, ":score_accuracy"),
			(assign, reg25, ":rating"),
			(display_message, "@Item '{s21}': {reg21}% damage + {reg22}% type + {reg23}% speed + {reg24}% accuracy = {reg25} Rating"),
			(assign, "$debug_als_item_rated", ":item_no"),
		(try_end),
		
		(try_begin),
			## COMBINED RATINGS
			(eq, ":slot", 0),
			(assign, reg1, ":rating"),
		(else_try),
			## DAMAGE
			(eq, ":slot", 1),
			(assign, reg1, ":score_damage"),
		(else_try),
			## ACCURACY
			(eq, ":slot", 2),
			(assign, reg1, ":score_accuracy"),
		(else_try),
			## SPEED
			(eq, ":slot", 3),
			(assign, reg1, ":score_speed"),
		(else_try),
			## DAMAGE TYPE
			(eq, ":slot", 4),
			(assign, reg1, ":score_type"),
		(try_end),
	]),
	
# script_cms_get_melee_weapon_ratings
# PURPOSE: Determines the autoloot rating of a armor item.
# EXAMPLE: (call_script, "script_cms_get_melee_weapon_ratings", ":item_no", ":imod", 0),
  ("cms_get_melee_weapon_ratings",
    [
		(store_script_param, ":item_no", 1),
		(store_script_param, ":imod", 2),
		(store_script_param, ":slot", 3),
		
		# Item is definitely a MELEE weapon.
		(item_get_swing_damage, ":weapon_damage", ":item_no"),
		(item_get_swing_damage_type, ":melee_type", ":item_no"),
		(item_get_weapon_length, ":weapon_reach", ":item_no"),
		(item_get_speed_rating, ":weapon_speed", ":item_no"),
		
		# Implement modifier value improvements.
		(try_begin),
			(eq, ":imod", imod_cracked),
			(val_add, ":weapon_damage", -5),
		(else_try),
			(eq, ":imod", imod_rusty),
			(val_add, ":weapon_damage", -3),
		(else_try),
			(eq, ":imod", imod_bent),
			(val_add, ":weapon_damage", -3),
			(val_add, ":weapon_speed", -3),
		(else_try),
			(eq, ":imod", imod_chipped),
			(val_add, ":weapon_damage", 2), # -1
		(else_try),
			(eq, ":imod", imod_crude),
			(val_add, ":weapon_damage", -2),
		(else_try),
			(eq, ":imod", imod_fine),
			(val_add, ":weapon_damage", 1),
		(else_try),
			(eq, ":imod", imod_tempered),
			(val_add, ":weapon_damage", 4),
		(else_try),
			(eq, ":imod", imod_balanced),
			(val_add, ":weapon_damage", 3),
			(val_add, ":weapon_speed", 3),
		(else_try),
			(eq, ":imod", imod_masterwork),
			(val_add, ":weapon_damage", 5),
			(val_add, ":weapon_speed", 1),
		(else_try),
			(eq, ":imod", imod_heavy),
			(val_add, ":weapon_damage", 2),
			(val_add, ":weapon_speed", -2),
		(try_end),
		
		# Set some baseline values to compare against.
		(assign, ":baseline_damage", MELEE_BASELINE_DAMAGE),
		(assign, ":baseline_reach",  MELEE_BASELINE_REACH),
		(assign, ":baseline_speed",  MELEE_BASELINE_SPEED),
		
		# Now convert raw data to baseline % values.
		# Damage
		(store_mul, ":score_damage", ":weapon_damage", 100),
		(val_div, ":score_damage", ":baseline_damage"),
		# Reach
		(store_mul, ":score_reach", ":weapon_reach", 100),
		(val_div, ":score_reach", ":baseline_reach"),
		# Speed
		(store_mul, ":score_speed", ":weapon_speed", 100),
		(val_div, ":score_speed", ":baseline_speed"),
		# Type
		(try_begin),
			(eq, ":melee_type", cut),
			(assign, ":score_type", 75),
		(else_try),
			(eq, ":melee_type", pierce),
			(assign, ":score_type", 125),
		(else_try),
			(eq, ":melee_type", blunt),
			(assign, ":score_type", 135),
		(try_end),
		
		# Apply special modifiers if available.
		(assign, ":score_special", 0),
		(try_begin),
			(item_has_property, ":item_no", itp_can_knock_down),
			(val_add, ":score_special", 25),
			(eq, 1, 0),
		(else_try),
			(item_has_property, ":item_no", itp_unbalanced),
			(val_add, ":score_special", -25),
			(eq, 1, 0),
		(else_try),
			(item_has_property, ":item_no", itp_crush_through),
			(val_add, ":score_special", 25),
			(eq, 1, 0),
		(else_try),
			(item_has_property, ":item_no", itp_couchable),
			(val_add, ":score_special", 40),
			(eq, 1, 0),
		(else_try),
			(item_has_property, ":item_no", itp_can_penetrate_shield),
			(val_add, ":score_special", 40),
			(eq, 1, 0),
		(else_try),
			(item_has_property, ":item_no", itp_bonus_against_shield),
			(val_add, ":score_special", 25),
			(eq, 1, 0),
		(else_try),
			(item_has_property, ":item_no", itp_penalty_with_shield),
			(val_add, ":score_special", -25),
			(eq, 1, 0),
		(else_try),
			(is_between, ":item_no", "itm_pitch_fork", "itm_pike"), #lower rating for spears
			(val_add, ":score_special", -80),
			(eq, 1, 0),
		(try_end),
		
		# Combine everything to get our item's rating.
		(assign, ":rating", ":score_damage"),
		(val_add, ":rating", ":score_speed"),
		(val_add, ":rating", ":score_reach"),
		(val_add, ":rating", ":score_type"),
		(val_add, ":rating", ":score_special"),
		
		# Diagnostic
		(try_begin),
			(ge, DEBUG_ALS, 2),
			(neq, "$debug_als_item_rated", ":item_no"),
			(str_store_item_name, s21, ":item_no"),
			(assign, reg21, ":score_damage"),
			(assign, reg22, ":score_type"),
			(assign, reg23, ":score_reach"),
			(assign, reg24, ":score_speed"),
			(assign, reg25, ":rating"),
			(assign, reg26, ":score_special"),
			(display_message, "@Item '{s21}': {reg21}% damage + {reg22}% type + {reg23}% reach + {reg24}% speed = {reg25} Rating"),
			(assign, "$debug_als_item_rated", ":item_no"),
		(try_end),
		
		(try_begin),
			## COMBINED RATINGS
			(eq, ":slot", 0),
			(assign, reg1, ":rating"),
		(else_try),
			## DAMAGE
			(eq, ":slot", 1),
			(assign, reg1, ":score_damage"),
		(else_try),
			## SPEED
			(eq, ":slot", 2),
			(assign, reg1, ":score_speed"),
		(else_try),
			## LENGTH
			(eq, ":slot", 3),
			(assign, reg1, ":score_reach"),
		(else_try),
			## DAMAGE TYPE
			(eq, ":slot", 4),
			(assign, reg1, ":score_type"),
		(try_end),
	]),
	
	
# script_als_execute_upgrade_checklist
# Cycles through the list of upgrades and executes any approved ones.
# Input: none
# Output: none
("als_execute_upgrade_checklist",
    [
		(try_for_range, ":storage_slot", 0, 9),
			(troop_slot_eq, ALS_TRADE_CONFIRM, ":storage_slot", 1),
			# Figure out who wants this upgrade.
			(troop_get_slot, ":troop_no", ALS_LOOTER, ":storage_slot"),
			# Get the old item information.
			(troop_get_slot, ":slot_old", ALS_OLD_ITEM, ":storage_slot"),
			(troop_get_inventory_slot, ":item_old", ":troop_no", ":slot_old"),
			(troop_get_inventory_slot_modifier, ":imod_old", ":troop_no", ":slot_old"),
			# Get the new item information.
			(troop_get_slot, ":slot_new", ALS_NEW_ITEM, ":storage_slot"),
			(troop_get_inventory_slot, ":item_new", "$pool_troop", ":slot_new"),
			(troop_get_inventory_slot_modifier, ":imod_new", "$pool_troop", ":slot_new"),
			# Switch the items.
			(troop_set_inventory_slot, ":troop_no", ":slot_old", ":item_new"),
			(troop_set_inventory_slot_modifier, ":troop_no", ":slot_old", ":imod_new"),
			(troop_set_inventory_slot, "$pool_troop", ":slot_new", ":item_old"),
			(troop_set_inventory_slot_modifier, "$pool_troop", ":slot_new", ":imod_old"),
			# Player output
			(str_store_troop_name, s21, ":troop_no"),
			(try_begin),
				(ge, ":item_old", 1),
				(str_store_item_name, s22, ":item_old"),
			(else_try),
				(str_store_string, s22, "@Empty Slot"),
			(try_end),
			(str_store_item_name, s23, ":item_new"),
			(troop_get_type, reg21, ":troop_no"),
			#(display_message, "@{s21} has replaced {reg21?her:his} {s22} with {s23}."),
			(str_store_string, s41, "@{s21} has replaced {reg21?her:his} {s22} with {s23}.^{s41}"),
			### DIAGNOSTIC ###
			(ge, DEBUG_ALS, 2),
			(assign, reg31, ":slot_old"),
			(assign, reg32, ":slot_new"),
			(display_message, "@ITEM SWITCH:", gpu_green),
			(display_message, "@Item [ {s23} ] placed in slot #{reg31} of {s21}."),
			(display_message, "@Item [ {s22} ] placed in slot #{reg32} of pool."),
		(try_end),
	]),
	
# script_cf_als_item_is_heraldic
# Reports back if an item is heraldic or not.
# Input: item #
# Output: none
("cf_als_item_is_heraldic",
    [
		(store_script_param, ":item_no", 1),
		
		## NATIVE DEFINITIONS ##
		# Armor
		(this_or_next|is_between, ":item_no", "itm_heraldic_mail_with_surcoat", "itm_white_highlander_shirt"),
		# Shields
		(is_between, ":item_no", "itm_old_round_shield", "itm_blue_company_round_shield"),
		
		## FLORIS DEFINITIONS ##
		
	]),

# script_als_set_companion_presets
# Sets up initial autoloot settings for each companion.
("als_set_companion_presets",
    [
		### COMPANION PRESETS ###
		(try_for_range, ":troop_no", companions_begin, companions_end),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_helm, als_find_upgrade),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_armor, als_find_upgrade),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_boots, als_find_upgrade),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_gloves, als_find_upgrade),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_mount, als_mount_best),
			(troop_set_slot, ":troop_no", slot_troop_enable_autolooting, 1),
			(troop_set_slot, ":troop_no", slot_troop_retain_heraldic_items, 1),
			(troop_set_slot, ":troop_no", slot_troop_prevent_breaking_sets, 1),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1_type, 0),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2_type, 0),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3_type, 0),
			(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4_type, 0),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_any),
		(try_end),
		## NPC1 - Borcha
		(assign, ":troop_no", "trp_npc1"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_two_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_throwing),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_throwing),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_throwing),
		## NPC2 - Marnid
		(assign, ":troop_no", "trp_npc2"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
		(try_end),
		## NPC3 - Ymira
		(assign, ":troop_no", "trp_npc3"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
		(try_end),
		## NPC4 - Rolf
		(assign, ":troop_no", "trp_npc4"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		## NPC5 - Baheshtur
		(assign, ":troop_no", "trp_npc5"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_bow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_arrows),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_two_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_arrows),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_mount, als_mount_fastest),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_light),
		(try_end),
		## NPC6 - Firentis
		(assign, ":troop_no", "trp_npc6"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		## NPC7 - Deshavi
		(assign, ":troop_no", "trp_npc7"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_bow_unmounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_arrows),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_polearm),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_arrows),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_mount, als_mount_fastest),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_light),
		(try_end),
		## NPC8 - Matheld
		(assign, ":troop_no", "trp_npc8"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_two_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_throwing),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_throwing),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_throwing),
		## NPC9 - Alayen
		(assign, ":troop_no", "trp_npc9"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		## NPC10 - Bunduk
		(assign, ":troop_no", "trp_npc10"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
		(try_end),
		## NPC11 - Katrin
		(assign, ":troop_no", "trp_npc11"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
		(try_end),
		## NPC12 - Jeremus
		(assign, ":troop_no", "trp_npc12"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_polearm),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_bolts),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
		(try_end),
		## NPC13 - Nizar
		(assign, ":troop_no", "trp_npc13"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_bow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_arrows),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
		(try_end),
		## NPC14 - Lezalit
		(assign, ":troop_no", "trp_npc14"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		## NPC15 - Artimenner
		(assign, ":troop_no", "trp_npc15"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_crossbow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_bolts),
		## NPC16 - Klethi
		(assign, ":troop_no", "trp_npc16"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_one_hand),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_shield_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_throwing),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_throwing),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_medium),
		(try_end),
		## NPC17 - Nissa
		(assign, ":troop_no", "trp_npc17"),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_1, als_bow_mounted),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_2, als_arrows),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_3, als_polearm),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_weapon_4, als_arrows),
		(troop_set_slot, ":troop_no", slot_troop_upgrade_mount, als_mount_fastest),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(troop_set_slot, ":troop_no", slot_troop_weight_limit, als_limit_armor_light),
		(try_end),
		
		
		# # VALUES FOR UPGRADE MENUS
		# als_keep_current                       = 0
		# # Armor
		# als_find_upgrade                       = 1 # Used by armor & mounts.
		# # Mounts
		# als_mount_fastest                      = 1
		# als_mount_resilient                    = 2
		# als_mount_best                         = 3
		# # Weapons
		# als_shield_mounted                     = 1 # Used by weapons.
		# als_shield_unmounted                   = 2
		# als_one_hand                           = 3
		# als_two_hand                           = 4
		# als_polearm                            = 5
		# als_lance                              = 6
		# als_arrows                             = 7
		# als_bow_mounted                        = 8
		# als_bow_unmounted                      = 9
		# als_bolts                              = 10
		# als_crossbow_mounted                   = 11
		# als_crossbow_unmounted                 = 12
		# als_throwing                           = 13

		
	]),
###########################################################################################################################
#####                                                 PARTY ROLES                                                     #####
###########################################################################################################################

# script_cms_strip_companion_from_any_role
# PURPOSE: Simple script for taking a given companion and ensuring they have their role properly removed (if any are applicable).
("cms_strip_companion_from_any_role",
    [
		(store_script_param, ":troop_no", 1),
		
		(try_begin),
			(eq, "$cms_role_storekeeper", ":troop_no"),
			(assign, "$cms_role_storekeeper", "trp_player"),
			(call_script, "script_cms_turnover_stores", "$cms_role_storekeeper", ":troop_no", ROLE_STOREKEEPER),
		(else_try),
			(eq, "$cms_role_quartermaster", ":troop_no"),
			(assign, "$cms_role_quartermaster", "trp_player"),
			(call_script, "script_cms_turnover_stores", "$cms_role_quartermaster", ":troop_no", ROLE_QUARTERMASTER),
		(else_try),
			(eq, "$cms_role_jailer", ":troop_no"),
			(assign, "$cms_role_jailer", "trp_player"),
			(call_script, "script_cms_turnover_stores", "$cms_role_jailer", ":troop_no", ROLE_JAILER),
		(try_end),
	]),
	
# script_cms_replace_troop_with_troop_in_role
# Reassigns new troop to a companion role.
("cms_replace_troop_with_troop_in_role",
    [
		(store_script_param, ":old_person", 1),
		(store_script_param, ":new_person", 2),
		(store_script_param, ":role_id", 3),
		
		(try_begin),
			(eq, ":role_id", ROLE_STOREKEEPER),
			(neq, ":old_person", ":new_person"),
			(assign, "$cms_role_storekeeper", ":new_person"),
			(call_script, "script_cms_turnover_stores", ":new_person", ":old_person", ":role_id"),
			(str_store_troop_name, s21, ":new_person"),
			(str_store_troop_name, s22, ":old_person"),
			(troop_get_type, reg21, ":old_person"),
			(display_message, "@{s22} has been relieved as your party's storekeeper.", gpu_light_blue),
			(display_message, "@{s22} has turned over {reg21?her:his} food stores to {s21}."),
			
		(else_try),
			(eq, ":role_id", ROLE_JAILER),
			(neq, ":old_person", ":new_person"),
			(assign, "$cms_role_jailer", ":new_person"),
			(str_store_troop_name, s21, ":new_person"),
			(str_store_troop_name, s22, ":old_person"),
			(display_message, "@{s22} has been relieved as your party's jailer.", gpu_light_blue),
			(display_message, "@{s21} has assumed the role as party gaoler."),
			
		(else_try),
			(eq, ":role_id", ROLE_QUARTERMASTER),
			(neq, ":old_person", ":new_person"),
			(assign, "$cms_role_quartermaster", ":new_person"),
			(call_script, "script_cms_turnover_stores", ":new_person", ":old_person", ":role_id"),
			(str_store_troop_name, s21, ":new_person"),
			(str_store_troop_name, s22, ":old_person"),
			(troop_get_type, reg21, ":old_person"),
			(display_message, "@{s22} has been relieved as your party's quartermaster.", gpu_light_blue),
			(display_message, "@{s22} has turned over {reg21?her:his} stored items to {s21}."),
			
		(else_try),
			(eq, ":old_person", ":new_person"),
			
		(else_try),
			(display_message, "@ERROR (CMS): Unrecognized role requested for turnover.", gpu_debug),
		(try_end),
    ]),
	
# script_cf_player_has_item_without_modifier (replaces native script)
  # Input: arg1 = item_id, arg2 = modifier
  # Output: none (can_fail)
  ("cf_player_has_item_without_modifier",
    [
      (store_script_param, ":item_id", 1),
      (store_script_param, ":modifier", 2),
	  #(party_get_slot, ":troop_no", "p_main_party", slot_party_role_chef), # 
	  (assign, ":troop_no", "$cms_role_storekeeper"),
	  (try_begin),
		(lt, ":troop_no", 1),
		(assign, ":troop_no", "trp_player"),
	  (try_end),
      #checking if any of the meat is not rotten
      (assign, ":has_without_modifier", 0),
      (troop_get_inventory_capacity, ":inv_size", ":troop_no"),
      (try_for_range, ":i_slot", 0, ":inv_size"),
        (troop_get_inventory_slot, ":cur_item", ":troop_no", ":i_slot"),
        (eq, ":cur_item", ":item_id"),
        (troop_get_inventory_slot_modifier, ":cur_modifier", ":troop_no", ":i_slot"),
        (neq, ":cur_modifier", ":modifier"),
        (assign, ":has_without_modifier", 1),
        (assign, ":inv_size", 0), #break
      (try_end),
      (eq, ":has_without_modifier", 1),
  ]),
  
# script_consume_food (replaces native script)
# Input: arg1: order of the food to be consumed
# Output: none
("consume_food",
    [
		(store_script_param, ":selected_food", 1),
		#(party_get_slot, ":troop_no", "p_main_party", slot_party_role_chef), # 
		(assign, ":troop_no", "$cms_role_storekeeper"),
		(troop_get_inventory_capacity, ":capacity", ":troop_no"),
		(try_for_range, ":cur_slot", 0, ":capacity"),
		  (troop_get_inventory_slot, ":cur_item", ":troop_no", ":cur_slot"),
		  (is_between, ":cur_item", food_begin, food_end),
		  (troop_get_inventory_slot_modifier, ":item_modifier", ":troop_no", ":cur_slot"),
		  (neq, ":item_modifier", imod_rotten),
		  (item_slot_eq, ":cur_item", slot_item_is_checked, 0),
		  (item_set_slot, ":cur_item", slot_item_is_checked, 1),
		  (val_sub, ":selected_food", 1),
		  (lt, ":selected_food", 0),
		  (assign, ":capacity", 0),
		  (troop_inventory_slot_get_item_amount, ":cur_amount", ":troop_no", ":cur_slot"),
		  (val_sub, ":cur_amount", 1),
		  (troop_inventory_slot_set_item_amount, ":troop_no", ":cur_slot", ":cur_amount"),
		(try_end),
		
		# Gain Storekeeper experience based on food consumption.
		(try_begin),
			(neq, "$cms_role_storekeeper", "trp_player"),
			(store_character_level, ":level_penalty", "$cms_role_storekeeper"),
			(val_mul, ":level_penalty", 4),
			(val_min, ":level_penalty", 100),
			(store_random_in_range, ":roll", 0, 100),
			(gt, ":roll", ":level_penalty"),
			(assign, ":xp_gain", 1),
			## TROOP EFFFECT: BONUS_QUICK_STUDY
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", "$cms_role_storekeeper", BONUS_QUICK_STUDY),
				(store_attribute_level, ":quick_study_bonus", "$cms_role_storekeeper", ca_intelligence),
				(val_div, ":quick_study_bonus", 2),
				(store_random_in_range, ":qs_roll", 0, 100),
				(lt, ":qs_roll", ":quick_study_bonus"),
				(val_add, ":xp_gain", 1),
			(try_end),
			(add_xp_to_troop, ":xp_gain", "$cms_role_storekeeper"), # Storekeepers have a chance of gaining 1xp per item eaten with a penalty that scales with level.
			(ge, DEBUG_ROLE, 1),
			(str_store_troop_name, s21, "$cms_role_storekeeper"),
			(assign, reg31, ":xp_gain"),
			(display_message, "@DEBUG (Storekeeper): {s21} gained {reg31} experience due to food consumption."),
		(try_end),
    ]),
	
# script_calculate_days_of_food_remaining
# PURPOSE: Determines how much food your party has, what the party's consumption rate is and how many days of food you have remaining.
# EXAMPLE: (call_script, "script_calculate_days_of_food_remaining"), # reg0 (# of men), reg1 (food available), reg2 (days left)
("calculate_days_of_food_remaining",
    [
		## Troop Effect (BONUS_HUNTER) - Reduce the amount of food needed.
		(assign, ":num_men", 0),
		(assign, ":hunting_chance", 0),
		(assign, ":total_hunters", 0),
		(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
		(try_for_range, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
			(val_add, ":num_men", ":stack_size"),
			#
			(party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
			(call_script, "script_cf_ce_troop_has_ability", ":stack_troop", BONUS_HUNTER),
			(val_add, ":total_hunters", 1),
			(try_begin),
				(this_or_next|is_between, ":stack_troop", companions_begin, companions_end),
				(eq, ":stack_troop", "trp_player"),
				(store_skill_level, ":tracking", "skl_tracking", ":stack_troop"),
				(val_max, ":tracking", 1),
				(val_mul, ":tracking", 3),
				(val_add, ":hunting_chance", ":tracking"),
			(else_try),
				(val_add, ":hunting_chance", ":stack_size"),
			(try_end),
		(try_end),
		
		# Hunting Effect
		(try_begin),
			(ge, ":total_hunters", 1),
			(party_get_current_terrain, ":terrain", "p_main_party"),
			(try_begin),
				## Abundant Hunting
				(this_or_next|eq, ":terrain", rt_water),
				(this_or_next|eq, ":terrain", rt_plain),
				(this_or_next|eq, ":terrain", rt_bridge),
				(this_or_next|eq, ":terrain", rt_river),
				(eq, ":terrain", rt_forest),
				(val_mul, ":hunting_chance", 3),
				(val_add, ":hunting_chance", 20),
				(val_clamp, ":hunting_chance", 0, 100),
				(str_store_string, s31, "@an abundant"),
			(else_try),
				## Sparse Hunting
				(this_or_next|eq, ":terrain", rt_mountain),
				(this_or_next|eq, ":terrain", rt_snow),
				(this_or_next|eq, ":terrain", rt_desert),
				(eq, ":terrain", rt_desert_forest),
				(val_mul, ":hunting_chance", 1),
				(val_clamp, ":hunting_chance", 0, 35),
				(str_store_string, s31, "@a sparse"),
			(else_try),
				## Default = Moderate Hunting
				(val_mul, ":hunting_chance", 2),
				(val_add, ":hunting_chance", 10),
				(val_clamp, ":hunting_chance", 0, 60),
				(str_store_string, s31, "@a moderate"),
			(try_end),
			(store_random_in_range, ":hunt_attempt", 0, 100),
			(store_mul, ":hunting_bonus", ":total_hunters", 6),
			
			## DIAGNOSTIC+ ##
			# (assign, reg31, ":hunting_chance"),
			# (assign, reg32, ":total_hunters"),
			# (assign, reg33, ":hunting_bonus"),
			# (assign, reg34, ":num_men"),
			# (display_message, "@DEBUG (Abilities): {reg32} Hunters in {s31} area had a {reg31}% chance of reducing people to feed by {reg33}. ({reg34} total)", gpu_debug),
			## DIAGNOSTIC- ##
			
			(lt, ":hunt_attempt", ":hunting_chance"),
			(val_sub, ":num_men", ":hunting_bonus"),
			(val_max, ":num_men", 1),
		(try_end),
		
		## Troop Effect (BONUS_CHEF) - Alter how many troops X amount of food can feed.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", "$cms_role_storekeeper", BONUS_CHEF),
			(assign, ":chef_effect", 29),
		(else_try),
			(assign, ":chef_effect", 33),
		(try_end),
		(val_mul, ":num_men", ":chef_effect"),
		(val_div, ":num_men", 100),
		(val_max, ":num_men", 1),
		
		## SECTION - Count how much food the Storekeeper has available.
		(assign, ":troop_no", "$cms_role_storekeeper"),
		(troop_get_inventory_capacity, ":capacity", ":troop_no"),
		(assign, ":food_carried", 0),
		(try_for_range, ":slot_no", 0, ":capacity"),
		  (troop_get_inventory_slot, ":item_no", ":troop_no", ":slot_no"),
		  (is_between, ":item_no", food_begin, food_end),
		  (troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":slot_no"),
		  (neq, ":imod", imod_rotten),
		  (troop_inventory_slot_get_item_amount, ":amount", ":troop_no", ":slot_no"),
		  (val_add, ":food_carried", ":amount"),
		(try_end),
		
		(assign, reg0, ":num_men"),      # Effective number of men eating.
		(assign, reg1, ":food_carried"), # Available food carried by the Storekeeper.
		(store_div, reg2, ":food_carried", ":num_men"), # Days of food remaining.
		# (display_message, "@DEBUG: {reg0} men to feed, {reg1} food available, {reg2} days remaining.", gpu_debug),
    ]),
	
# script_cms_turnover_stores
# Input: new storekeeper, old storekeeper, role # (constant from cms_constants)
# Output: none
("cms_turnover_stores",
    [
		(store_script_param, ":new_person", 1),
		(store_script_param, ":old_person", 2),
		(store_script_param, ":role_id", 3),
		
		(troop_get_inventory_capacity, ":capacity", ":old_person"),
		(try_begin),
			(eq, ":role_id", ROLE_STOREKEEPER),
			(try_for_range, ":i_slot", 9, ":capacity"),
			  (troop_get_inventory_slot, ":item_no", ":old_person", ":i_slot"),
			  (is_between, ":item_no", food_begin, food_end),
			  (call_script, "script_cf_cms_store_pool_item_to_empty_inventory_slot", ":old_person", ":new_person", ":i_slot"),
			(try_end),
		(else_try),
			(eq, ":role_id", ROLE_QUARTERMASTER),
			(try_for_range, ":i_slot", 9, ":capacity"),
			  (troop_get_inventory_slot, ":item_no", ":old_person", ":i_slot"),
			  (neg|is_between, ":item_no", food_begin, food_end),
			  (neg|troop_slot_eq, ":old_person", slot_troop_reading_book, ":item_no"),
			  (neq, ":item_no", SILVERSTAG_EMBLEM), # Prevent trading emblems.
			  (call_script, "script_cf_cms_store_pool_item_to_empty_inventory_slot", ":old_person", ":new_person", ":i_slot"),
			(try_end),
		(try_end),
    ]),

# script_cms_verify_party_role_filled
# PURPOSE: A single place to check if a role is filled and if not replace that role with the player.
("cms_verify_party_role_filled",
    [
		(store_script_param, ":role_id", 1),
		
		(try_begin),
			(eq, ":role_id", ROLE_STOREKEEPER),
			(neq, "$cms_role_storekeeper", "trp_player"),
			(try_begin),
				(neg|main_party_has_troop, "$cms_role_storekeeper"),
				(assign, "$cms_role_storekeeper", "trp_player"),
			(try_end),
			
		(else_try),
			(eq, ":role_id", ROLE_QUARTERMASTER),
			(neq, "$cms_role_quartermaster", "trp_player"),
			(try_begin),
				(neg|main_party_has_troop, "$cms_role_quartermaster"),
				(assign, "$cms_role_quartermaster", "trp_player"),
			(try_end),
			
		(else_try),
			(eq, ":role_id", ROLE_JAILER),
			(neq, "$cms_role_jailer", "trp_player"),
			(try_begin),
				(neg|main_party_has_troop, "$cms_role_jailer"),
				(assign, "$cms_role_jailer", "trp_player"),
			(try_end),
			
		(try_end),
    ]),
	
# script_cf_cms_check_if_qualified_for_role
# PURPOSE: A single location to verify if a perspective troop is qualified to fit a given companion role.
# EXAMPLE: (call_script, "script_cf_cms_check_if_qualified_for_role", ":troop_no", ROLE_STOREKEEPER / ROLE_QUARTERMASTER / ROLE_JAILER), # cms_scripts.py
("cf_cms_check_if_qualified_for_role",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":role_id", 2),
		
		(assign, ":qualified", 0),
		(store_skill_level, ":skill_trade", "skl_trade", ":troop_no"),
		(store_skill_level, ":skill_inventory_management", "skl_inventory_management", ":troop_no"),
		(store_skill_level, ":skill_prisoner_management", "skl_prisoner_management", ":troop_no"),
		(str_store_troop_name, s20, ":troop_no"),
		
		(try_begin),
			(eq, ":role_id", ROLE_STOREKEEPER),
			(str_store_string, s21, "@{s20} has insufficient skill in inventory management.  Requires 3+."),
			(ge, ":skill_inventory_management", 3),
			(str_store_string, s21, "@{s20} is qualified to serve as your storekeeper."),
			(assign, ":qualified", 1),
		(else_try),
			(eq, ":role_id", ROLE_QUARTERMASTER),
			(str_store_string, s21, "@{s20} has insufficient skill in trading.  Requires 3+."),
			(ge, ":skill_trade", 3),
			(str_store_string, s21, "@{s20} has insufficient skill in inventory management.  Requires 3+."),
			(ge, ":skill_inventory_management", 3),
			(str_store_string, s21, "@{s20} is qualified to serve as your quartermaster."),
			(assign, ":qualified", 1),
		(else_try),
			(eq, ":role_id", ROLE_JAILER),
			(str_store_string, s21, "@{s20} has insufficient skill in prisoner management.  Requires 2+."),
			(ge, ":skill_prisoner_management", 2),
			(str_store_string, s21, "@{s20} is qualified to serve as your gaoler."),
			# TODO: Must check to see if new gaoler can handle current prisoner limitations.
			(assign, ":qualified", 1),
		(try_end),
		
		# Ensure member isn't filling in a role already.
		(try_begin),
			(eq, "$cms_role_storekeeper", ":troop_no"),
			(str_store_string, s21, "@{s20} is already serving as your storekeeper."),
			(assign, ":qualified", 0),
		(else_try),
			(eq, "$cms_role_quartermaster", ":troop_no"),
			(str_store_string, s21, "@{s20} is already serving as your quartermaster."),
			(assign, ":qualified", 0),
		(else_try),
			(eq, "$cms_role_jailer", ":troop_no"),
			(str_store_string, s21, "@{s20} is already serving as your jailer."),
			(assign, ":qualified", 0),
		(try_end),
		
		# If this is the player we're switching to then automatically succeed.
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(assign, ":qualified", 1),
		(try_end),
		
		(try_begin),
			(eq, ":qualified", 0),
			(display_message, "@{s21}", gpu_red),
		(try_end),
		
		(eq, ":qualified", 1), ## CONDITIONAL BREAK ##
    ]),
	
# script_cms_town_entry (hooks into the consequence block of town "menu"
# PURPOSE: Check for party role related functions upon entering a town.
# EXAMPLE: (call_script, "script_cms_town_entry"), # cms_scripts.py
("cms_town_entry",
    [
		### QUARTERMASTER: SALE OF GOODS ###
		(try_begin),
			# Is a quartermaster assigned and present?
			(this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_town),
			(party_slot_eq, "$current_town", slot_party_type, spt_village),
			(neq, "$cms_role_quartermaster", "trp_player"),
			(is_between, "$cms_role_quartermaster", companions_begin, companions_end),
			(main_party_has_troop, "$cms_role_quartermaster"),
			# Are we allowing auto-selling to occur?
			(eq, "$cms_enable_auto_selling", 1),
			
			(try_begin),
				(is_between, "$current_town", towns_begin, towns_end),
				(party_get_slot, ":town_weaponsmith", "$current_town", slot_town_weaponsmith),
				(party_get_slot, ":town_armorer", "$current_town", slot_town_armorer),
				(party_get_slot, ":town_horse_merchant", "$current_town", slot_town_horse_merchant),
				(party_get_slot, ":town_merchant", "$current_town", slot_town_merchant),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
			(try_end),
			
			(assign, ":troop_no", "$cms_role_quartermaster"),
			
			(store_free_inventory_capacity, ":begin_space", ":troop_no"),
			(store_troop_gold, ":begin_gold", ":troop_no"),
			(try_begin),
				(is_between, "$current_town", towns_begin, towns_end),
				(call_script, "script_cms_auto_sell", ":troop_no", ":town_weaponsmith"),
				(call_script, "script_cms_auto_sell", ":troop_no", ":town_armorer"),
				(call_script, "script_cms_auto_sell", ":troop_no", ":town_horse_merchant"),
				(call_script, "script_cms_auto_sell", ":troop_no", ":town_merchant"),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(call_script, "script_cms_auto_sell", ":troop_no", ":merchant_troop"),
			(try_end),
			(store_free_inventory_capacity, ":end_space", ":troop_no"),
			(store_troop_gold, ":end_gold", ":troop_no"),
			(neq, ":end_gold", ":begin_gold"),
			(store_sub, ":gained_gold", ":end_gold", ":begin_gold"),
			(set_show_messages, 0),
			(troop_remove_gold, ":troop_no", ":gained_gold"),
			(store_mul, ":quartermaster_payment", ":gained_gold", 15),
			(val_div, ":quartermaster_payment", 100),
			(store_sub, ":net_gain", ":gained_gold", ":quartermaster_payment"),
			(troop_add_gold, "trp_player", ":net_gain"),
			(set_show_messages, 1),
			(store_sub, reg21, ":end_space", ":begin_space"),
			(assign, reg22, ":gained_gold"),
			(store_sub, reg23, reg21, 1),
			(store_sub, reg24, reg22, 1),
			(assign, reg25, ":quartermaster_payment"),
			(store_sub, reg26, reg25, 1),
			(troop_get_type, reg27, ":troop_no"),
			(assign, reg28, ":net_gain"),
			(store_sub, reg29, reg28, 1),
			(str_store_troop_name, s21, ":troop_no"),
			(display_message, "@{s21} has sold {reg21} {reg23?items:item} and earned {reg22} {reg24?denars:denar}.", gpu_green),
			(display_message, "@{s21} takes {reg27?her:his} cut of {reg25} {reg26?denars:denar} gives you {reg28} {reg29?denars:denar}."),
			(val_div, ":quartermaster_payment", 3),
			(add_xp_to_troop, ":quartermaster_payment", "$cms_role_quartermaster"), # Quartermasters gain 5% of the sale price as experience.
			
			## TROOP EFFFECT: BONUS_QUICK_STUDY
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", "$cms_role_quartermaster", BONUS_QUICK_STUDY),
				(store_attribute_level, ":quick_study_bonus", "$cms_role_quartermaster", ca_intelligence),
				(val_div, ":quick_study_bonus", 2),
				(store_mul, ":quick_study_xp", ":gained_gold", ":quick_study_bonus"),
				(val_div, ":quick_study_xp", 100),
				(assign, reg11, ":quick_study_xp"),
				(display_message, "@{s21} earns an additional {reg11} experience. (Quick Study)"),
				(add_xp_to_troop, ":quick_study_xp", "$cms_role_quartermaster"), # Quick study companions gain 1% per 2 INT extra as experience.
			(try_end),
			
			## DISPLAY WHAT COULDN'T BE SOLD.
			(try_begin),
				(troop_get_inventory_capacity, ":capacity", "$cms_role_quartermaster"),
				(assign, ":earnings", 0),
				(assign, ":total_items", 0),
				(try_for_range, ":i_slot", 9, ":capacity"),
					(troop_get_inventory_slot, ":item_no", "$cms_role_quartermaster", ":i_slot"),
					(ge, ":item_no", 1), # Valid item.
					(assign, ":continue", 1),
					(try_begin),
						(call_script, "script_cf_dws_item_in_a_weapon_set", "$cms_role_quartermaster", ":item_no"), # Prevent sale of weapon set gear.
						(assign, ":continue", 0),
					(else_try),
						(item_get_type, ":item_type", ":item_no"), # Prevent sale of books or mentioning them.
						(eq, ":item_type", itp_type_book),
						(assign, ":continue", 0),
					(try_end),
					(eq, ":continue", 1),
					(val_add, ":total_items", 1),
					(troop_get_inventory_slot_modifier, ":item_modifier", "$cms_role_quartermaster", ":i_slot"),
					(call_script, "script_cms_get_item_value_with_imod", ":item_no", ":item_modifier", CMS_AUTO_SELLING),
					(assign, ":item_value", reg0),
					(val_div, ":item_value", 100),
					(call_script, "script_game_get_item_sell_price_factor", ":item_no"),
					(assign, ":sell_price_factor", reg0),
					(val_mul, ":item_value", ":sell_price_factor"),
					(val_div, ":item_value", 100),
					(val_max, ":item_value",1),
					
					(val_add, ":earnings", ":item_value"),
				(try_end),
				(ge, ":total_items", 1),
				(assign, reg21, ":earnings"),
				(store_sub, reg24, reg21, 1),
				(assign, reg22, ":total_items"),
				(store_sub, reg23, reg22, 1),
				(str_store_troop_name, s21, "$cms_role_quartermaster"),
				(display_message, "@{s21} was unable to sell {reg22} item{reg23?s:} worth {reg21} denar{reg24?s:}.", gpu_red),
			(try_end),
		(try_end),
		
		### JAILER: SALE OF PRISONERS ###
		(try_begin),
			(is_between, "$current_town", towns_begin, towns_end),
			# Is a ransom broker available? (if applicable)
			(try_begin),
				(party_get_slot, ":ransom_broker", "$current_town", slot_center_ransom_broker),
				(gt, ":ransom_broker", 0),
			(else_try),
				## WINDYPLAINS+ ## - Troop Effect (BONUS_USEFUL_CONTACTS) - Allows prisoner sale even if no broker is available.
				(is_between, "$cms_role_jailer", companions_begin, companions_end), # Companion only effect.
				(main_party_has_troop, "$cms_role_jailer"),
				(call_script, "script_cf_ce_troop_has_ability", "$cms_role_jailer", BONUS_USEFUL_CONTACTS),
				# (party_get_num_prisoner_stacks, ":stack_limit", "p_main_party"),
				# (gt, ":stack_limit", 0),
				# (str_store_troop_name, s21, "$cms_role_jailer"),
				# (display_message, "@{s21}'s manages to find someone to offload prisoners to even though no broker is present.", gpu_green),
				(assign, ":ransom_broker", ransom_brokers_begin), # Just to assign one to move on.
			(try_end),
			(gt, ":ransom_broker", 0),
			(assign, "$cms_last_town_with_slaver", "$current_town"),
			# Is a jailer assigned and present?
			(neq, "$cms_role_jailer", "trp_player"),
			(is_between, "$cms_role_jailer", companions_begin, companions_end),
			(main_party_has_troop, "$cms_role_jailer"),
			# Check jailer mode.
			(this_or_next|eq, "$cms_mode_jailer", CMS_JAILER_SELL_ONLY),
			(eq, "$cms_mode_jailer", CMS_JAILER_STORE_AND_SELL),
			# Sell prisoners.
			(assign, "$g_talk_troop", ":ransom_broker"), # Done to prevent all prisoners being worth 50 denars each.
			(party_get_num_prisoner_stacks, ":stack_limit", "p_main_party"),
			(gt, ":stack_limit", 0),
			(assign, "$g_move_heroes", 0),
			(try_begin),
				## See if quest "raise_troops" is active and make sure we don't sell our quest troop type.
				(check_quest_active, "qst_capture_prisoners"),
				(quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
				(store_troop_count_prisoners, reg24, ":quest_target_troop", "p_main_party"),
				(gt, reg24, 0),
				(call_script, "script_determine_value_of_party_prisoners_except", "p_main_party", ":quest_target_troop"),
				(assign, ":cash", reg1),
				(assign, ":prisoners", reg2),
				(call_script, "script_party_remove_all_prisoners_except", "p_main_party", ":quest_target_troop"),
			(else_try),
				## Default Response ##
				(call_script, "script_determine_value_of_party_prisoners_except", "p_main_party", -1),
				(assign, ":cash", reg1),
				(assign, ":prisoners", reg2),
				(call_script, "script_party_remove_all_prisoners_except", "p_main_party", -1),
				# (call_script, "script_party_remove_all_prisoners", "p_main_party"),
			(try_end),
			# Calculate jailer's cut.
			(gt, ":cash", 0), # Prevent this script from telling us about this if the party only contains hero prisoners.
			(assign, reg21, ":cash"),
			(store_mul, ":jailer_payment", ":cash", 15),
			(val_div, ":jailer_payment", 100),
			(val_sub, ":cash", ":jailer_payment"),
			(set_show_messages, 0),
			(call_script, "script_troop_add_gold", "trp_player", ":cash"),
			(set_show_messages, 1),
			(assign, reg22, ":jailer_payment"),
			(assign, reg23, ":prisoners"),
			(str_store_troop_name, s21, "$cms_role_jailer"),
			(troop_get_type, reg24, "$cms_role_jailer"),
			(store_sub, reg25, reg22, 1),
			(store_sub, reg26, reg23, 1),
			(store_sub, reg27, reg21, 1),
			(assign, reg28, ":cash"),
			(store_sub, reg29, reg28, 1),
			(display_message, "@{s21} has sold {reg23} {reg26?prisoners:prisoner} and earned {reg21} {reg27?denars:denar}.", gpu_green),
			(display_message, "@{s21} takes {reg24?her:his} cut of {reg22} {reg25?denars:denar} gives you {reg28} {reg29?denars:denar}."),
			(add_xp_to_troop, ":jailer_payment", "$cms_role_jailer"), # Jailers gain 15% of the sale price as experience.
			
			## TROOP EFFFECT: BONUS_QUICK_STUDY
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", "$cms_role_jailer", BONUS_QUICK_STUDY),
				(store_attribute_level, ":quick_study_bonus", "$cms_role_jailer", ca_intelligence),
				(val_div, ":quick_study_bonus", 2),
				(store_mul, ":quick_study_xp", ":cash", ":quick_study_bonus"),
				(val_div, ":quick_study_xp", 100),
				(assign, reg11, ":quick_study_xp"),
				(display_message, "@{s21} earns an additional {reg11} experience. (Quick Study)"),
				(add_xp_to_troop, ":quick_study_xp", "$cms_role_jailer"), # Quick study companions gain 1% per 2 INT extra as experience.
			(try_end),
		(else_try),
			### JAILER: STORAGE OF PRISONERS ###
			# Is a jailer assigned and present?
			(neq, "$cms_role_jailer", "trp_player"),
			(is_between, "$cms_role_jailer", companions_begin, companions_end),
			(main_party_has_troop, "$cms_role_jailer"),
			# Check jailer mode.
			(this_or_next|eq, "$cms_mode_jailer", CMS_JAILER_STORE_ONLY),
			(eq, "$cms_mode_jailer", CMS_JAILER_STORE_AND_SELL),
			# Do we own this center and does it have a prison?
			(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
			(this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_town),
			(party_slot_eq, "$current_town", slot_party_type, spt_castle),
			# Transfer prisoners.
			(party_get_num_prisoners, ":prisoner_count_before", "p_main_party"),
			(gt, ":prisoner_count_before", 0),
			(assign, "$g_move_heroes", 0),
			(call_script, "script_party_prisoners_add_party_prisoners", "$current_town", "p_main_party"),  # Move prisoners from player party to center.
			(call_script, "script_party_remove_all_prisoners", "p_main_party"),
			(party_get_num_prisoners, ":prisoner_count_after", "p_main_party"),
			(store_sub, ":prisoners_transferred", ":prisoner_count_before", ":prisoner_count_after"),
			(ge, ":prisoners_transferred", 1),
			(assign, reg21, ":prisoners_transferred"),
			(store_sub, reg22, ":prisoners_transferred", 1),
			(str_store_troop_name, s21, "$cms_role_jailer"),
			(str_store_party_name, s22, "$current_town"),
			(display_message, "@{s21} has transferred {reg21} prisoner{reg22?s:} to {s22}.", gpu_green),
		(try_end),
    ]),
	
# script_cms_offload_prisoners
("cms_offload_prisoners",
    [
		### JAILER: SALE OF PRISONERS ###
		# Is a ransom broker available?
		# (try_begin),
			# (is_between, "$current_town", towns_begin, towns_end),
			# (party_get_slot, ":ransom_broker", "$current_town", slot_center_ransom_broker),
			# (gt, ":ransom_broker", 0),
			# (assign, "$cms_last_town_with_slaver", "$current_town"),
		# (else_try),
			# (assign, ":ransom_broker", "trp_ransom_broker_1"),
		# (try_end),
		
		(try_begin),
			# TODO: Put in a global option to prevent auto-sale.
			# Sell prisoners.
			(assign, "$g_talk_troop", "trp_ransom_broker_1"), # Done to prevent all prisoners being worth 50 denars each.
			(party_get_num_prisoner_stacks, ":stack_limit", "p_main_party"),
			(gt, ":stack_limit", 0),
			(assign, "$g_move_heroes", 0),
			(call_script, "script_determine_value_of_party_prisoners_except", "p_main_party", -1),
			(assign, ":cash", reg1),
			(assign, ":prisoners", reg2),
			(call_script, "script_party_remove_all_prisoners_except", "p_main_party", -1),
			# Calculate jailer's cut.
			(gt, ":cash", 0), # Prevent this script from telling us about this if the party only contains hero prisoners.
			(assign, reg21, ":cash"),
			(store_sub, reg27, reg21, 1),
			(assign, reg23, ":prisoners"),
			(store_sub, reg26, reg23, 1),
			(try_begin),
				(eq, "$cms_role_jailer", "trp_player"),
				(set_show_messages, 0),
				(call_script, "script_troop_add_gold", "trp_player", ":cash"),
				(set_show_messages, 1),
				(display_message, "@You have sold {reg23} {reg26?prisoners:prisoner} and earned {reg21} {reg27?denars:denar}.", gpu_green),
			(else_try),
				(is_between, "$cms_role_jailer", companions_begin, companions_end),
				(store_mul, ":jailer_payment", ":cash", 15),
				(val_div, ":jailer_payment", 100),
				(val_sub, ":cash", ":jailer_payment"),
				(set_show_messages, 0),
				(call_script, "script_troop_add_gold", "trp_player", ":cash"),
				(set_show_messages, 1),
				(assign, reg22, ":jailer_payment"),
				(str_store_troop_name, s21, "$cms_role_jailer"),
				(troop_get_type, reg24, "$cms_role_jailer"),
				(store_sub, reg25, reg22, 1),
				(assign, reg28, ":cash"),
				(store_sub, reg29, reg28, 1),
				(display_message, "@{s21} has sold {reg23} {reg26?prisoners:prisoner} and earned {reg21} {reg27?denars:denar}.", gpu_green),
				(display_message, "@{s21} takes {reg24?her:his} cut of {reg22} {reg25?denars:denar} gives you {reg28} {reg29?denars:denar}."),
				(add_xp_to_troop, ":jailer_payment", "$cms_role_jailer"), # Jailers gain 15% of the sale price as experience.
			(try_end),
			
		(else_try),
			### JAILER: STORAGE OF PRISONERS ###
			# Ensure we are not trying to give prisoners to the salt mine.  This place is designed to make prisoners disappear.
			(neq, "$g_encountered_party", "p_salt_mine"),
			# Is a jailer assigned and present?
			(neq, "$cms_role_jailer", "trp_player"),
			(is_between, "$cms_role_jailer", companions_begin, companions_end),
			(main_party_has_troop, "$cms_role_jailer"),
			# Do we own this center and does it have a prison?
			(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
			(this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_town),
			(party_slot_eq, "$current_town", slot_party_type, spt_castle),
			# Transfer prisoners.
			(party_get_num_prisoners, ":prisoner_count", "p_main_party"),
			(gt, ":prisoner_count", 0),
			(assign, "$g_move_heroes", 1),
			(call_script, "script_party_prisoners_add_party_prisoners", "$current_town", "p_main_party"),  # Move prisoners from player party to center.
			(call_script, "script_party_remove_all_prisoners", "p_main_party"),
			(assign, "$g_move_heroes", 0), # Just to be safe.
			(assign, reg21, ":prisoner_count"),
			(store_sub, reg22, ":prisoner_count", 1),
			(str_store_troop_name, s21, "$cms_role_jailer"),
			(str_store_party_name, s22, "$current_town"),
			(display_message, "@{s21} has transferred {reg21} prisoner{reg22?s:} to {s22}.", gpu_green),
		(try_end),
    ]),
	
# script_party_remove_all_prisoners_except
# INPUT:
# param1: Party-id from which  prisoners will be removed.
# param2: Troop-id you don't want removed.
# "$g_move_heroes" : controls if heroes will also be removed.
("party_remove_all_prisoners_except",
    [
      (store_script_param, ":party", 1),
      (store_script_param, ":troop_no", 2),
	  
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop",":party",":stack_no"),
        (this_or_next|neg|troop_is_hero, ":stack_troop"),
        (eq, "$g_move_heroes", 1),
		(neq, ":stack_troop", ":troop_no"),
		(call_script, "script_cf_common_troop_needed_for_quest", ":stack_troop"), # questutil_scripts.py
        (party_prisoner_stack_get_size, ":stack_size",":party",":stack_no"),
        (party_remove_prisoners, ":party", ":stack_troop", ":stack_size"),
      (try_end),
  ]),
  
# script_determine_value_of_party_prisoners_except
# "$g_move_heroes"		controls if heroes will also be removed.
# ":troop_to_ignore"	This troop is ignored in the counting process.  Done for quest & party role purposes.  Set to -1 to disregard it.
("determine_value_of_party_prisoners_except",
    [
		(store_script_param, ":party_no", 1),
		(store_script_param, ":troop_to_ignore", 2),

		(party_get_num_prisoner_stacks, ":stack_limit", ":party_no"),
		(assign, ":cash", 0),
		(assign, ":prisoners", 0),
		(try_begin),
			(gt, ":stack_limit", 0),
			(try_for_range, ":stack_no", 0, ":stack_limit"),
				(party_prisoner_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
				(neg|troop_is_hero, ":troop_no"), # Prevent companions, lords & player from being counted.
				(neq, ":troop_no", ":troop_to_ignore"),
				(call_script, "script_cf_common_troop_needed_for_quest", ":troop_no"), # questutil_scripts.py
				(party_prisoner_stack_get_size, ":troop_count", ":party_no", ":stack_no"),
				(call_script, "script_game_get_prisoner_price", ":troop_no"),
				(assign, ":troop_value", reg0),
				(store_mul, ":stack_value", ":troop_value", ":troop_count"),
				(val_add, ":cash", ":stack_value"),
				(val_add, ":prisoners", ":troop_count"),
			(try_end),
		(try_end),
		(assign, reg1, ":cash"),
		(assign, reg2, ":prisoners"),
  ]),
  
# script_cms_get_item_value_with_imod
# Credit: Custom Commander (rubik)
# PURPOSE: Returns the sell price based on the item's money value and its imod
# EXAMPLE: (call_script, "script_cms_get_item_value_with_imod", ":item", ":imod", CMS_AUTO_SELLING),
("cms_get_item_value_with_imod",
	[
	(store_script_param, ":item", 1),
	(store_script_param, ":imod", 2),
	(store_script_param, ":function", 3),
	
	(store_item_value, ":score", ":item"),
	(try_begin),
		(eq, ":imod", imod_plain),
		(assign, ":imod_multiplier", 100),
	(else_try),
		(eq, ":imod", imod_cracked),
		(assign, ":imod_multiplier", 50),
	(else_try),
		(eq, ":imod", imod_rusty),
		(assign, ":imod_multiplier", 55),
	(else_try),
		(eq, ":imod", imod_bent),
		(assign, ":imod_multiplier", 65),
	(else_try),
		(eq, ":imod", imod_chipped),
		(assign, ":imod_multiplier", 72),
	(else_try),
		(eq, ":imod", imod_battered),
		(assign, ":imod_multiplier", 75),
	(else_try),
		(eq, ":imod", imod_poor),
		(assign, ":imod_multiplier", 80),
	(else_try),
		(eq, ":imod", imod_crude),
		(assign, ":imod_multiplier", 83),
	(else_try),
		(eq, ":imod", imod_old),
		(assign, ":imod_multiplier", 86),
	(else_try),
		(eq, ":imod", imod_cheap),
		(assign, ":imod_multiplier", 90),
	(else_try),
		(eq, ":imod", imod_fine),
		(assign, ":imod_multiplier", 190),
	(else_try),
		(eq, ":imod", imod_well_made),
		(assign, ":imod_multiplier", 250),
	(else_try),
		(eq, ":imod", imod_sharp),
		(assign, ":imod_multiplier", 160),
	(else_try),
		(eq, ":imod", imod_balanced),
		(assign, ":imod_multiplier", 350),
	(else_try),
		(eq, ":imod", imod_tempered),
		(assign, ":imod_multiplier", 670),
	(else_try),
		(eq, ":imod", imod_deadly),
		(assign, ":imod_multiplier", 850),
	(else_try),
		(eq, ":imod", imod_exquisite),
		(assign, ":imod_multiplier", 1450),
	(else_try),
		(eq, ":imod", imod_masterwork),
		(assign, ":imod_multiplier", 1750),
	(else_try),
		(eq, ":imod", imod_heavy),
		(assign, ":imod_multiplier", 190),
	(else_try),
		(eq, ":imod", imod_strong),
		(assign, ":imod_multiplier", 490),
	(else_try),
		(eq, ":imod", imod_powerful),
		(assign, ":imod_multiplier", 320),
	(else_try),
		(eq, ":imod", imod_tattered),
		(assign, ":imod_multiplier", 50),
	(else_try),
		(eq, ":imod", imod_ragged),
		(assign, ":imod_multiplier", 70),
	(else_try),
		(eq, ":imod", imod_rough),
		(assign, ":imod_multiplier", 60),
	(else_try),
		(eq, ":imod", imod_sturdy),
		(assign, ":imod_multiplier", 170),
	(else_try),
		(eq, ":imod", imod_thick),
		(assign, ":imod_multiplier", 260),
	(else_try),
		(eq, ":imod", imod_hardened),
		(assign, ":imod_multiplier", 390),
	(else_try),
		(eq, ":imod", imod_reinforced),
		(assign, ":imod_multiplier", 650),
	(else_try),
		(eq, ":imod", imod_superb),
		(assign, ":imod_multiplier", 250),
	(else_try),
		(eq, ":imod", imod_lordly),
		(assign, ":imod_multiplier", 1150),
	(else_try),
		(eq, ":imod", imod_lame),
		(assign, ":imod_multiplier", 40),
	(else_try),
		(eq, ":imod", imod_swaybacked),
		(assign, ":imod_multiplier", 60),
	(else_try),
		(eq, ":imod", imod_stubborn),
		(assign, ":imod_multiplier", 90),
	(else_try),
		(eq, ":imod", imod_timid),
		(assign, ":imod_multiplier", 180),
	(else_try),
		(eq, ":imod", imod_meek),
		(assign, ":imod_multiplier", 180),
	(else_try),
		(eq, ":imod", imod_spirited),
		(assign, ":imod_multiplier", 650),
	(else_try),
		(eq, ":imod", imod_champion),
		(assign, ":imod_multiplier", 1450),
	(else_try),
		(eq, ":imod", imod_fresh),
		(assign, ":imod_multiplier", 100),
	(else_try),
		(eq, ":imod", imod_day_old),
		(assign, ":imod_multiplier", 100),
	(else_try),
		(eq, ":imod", imod_two_day_old),
		(assign, ":imod_multiplier", 90),
	(else_try),
		(eq, ":imod", imod_smelling),
		(assign, ":imod_multiplier", 40),
	(else_try),
		(eq, ":imod", imod_rotten),
		(assign, ":imod_multiplier", 5),
	(else_try),
		(eq, ":imod", imod_large_bag),
		(assign, ":imod_multiplier", 190),
	(try_end),
	(val_mul, ":score", ":imod_multiplier"),
	
	## TROOP EFFECT: CARGOMASTER
	(try_begin),
		(eq, ":function", CMS_AUTO_SELLING),
		(call_script, "script_cf_ce_troop_has_ability", "$cms_role_quartermaster", BONUS_CARGOMASTER), # combat_scripts.py - ability constants in combat_constants.py
		(store_skill_level, ":skill", "skl_persuasion", "$cms_role_quartermaster"),
		(val_mul, ":skill", 3),
		(store_mul, ":cargomaster_bonus", ":score", ":skill"),
		(val_div, ":cargomaster_bonus", 100),
		# (try_begin), ### DIAGNOSTIC+ ###
			# # (ge, DEBUG_TROOP_ABILITIES, 1),
			# (assign, reg31, ":score"),
			# (val_div, reg31, 100),
			# (store_add, reg32, ":score", ":cargomaster_bonus"),
			# (val_div, reg32, 100),
			# (store_skill_level, reg33, "skl_persuasion", "$cms_role_quartermaster"),
			# (str_store_troop_name, s31, "$cms_role_quartermaster"),
			# (str_store_item_name, s32, ":item"),
			# (display_message, "@DEBUG (Abilities): {s31}'s PERSUASION skill ({reg33}) raises the price of {s32} from {reg31} to {reg32} denars. (CARGOMASTER)", gpu_debug),
		# (try_end), ### DIAGNOSTIC- ###
		(val_add, ":score", ":cargomaster_bonus"),
	(try_end),
	
	## TROOP EFFECT: USEFUL_CONTACTS
	#  Effect: Reduces the cost of food goods by 4% per point of trade.
	(try_begin),
		(eq, ":function", CMS_AUTO_BUYING),
		(is_between, ":item", food_begin, food_end),
		(call_script, "script_cf_ce_troop_has_ability", "$cms_role_storekeeper", BONUS_USEFUL_CONTACTS), # combat_scripts.py - ability constants in combat_constants.py
		(store_skill_level, ":skill", "skl_trade", "$cms_role_storekeeper"),
		(val_mul, ":skill", 4),
		(store_mul, ":price_discount", ":score", ":skill"),
		(val_div, ":price_discount", 100),
		(val_add, "$cms_useful_contact_food_discount", ":price_discount"),
		# (try_begin), ### DIAGNOSTIC+ ###
			# (ge, DEBUG_TROOP_ABILITIES, 1),
			# (assign, reg31, ":score"),
			# (val_div, reg31, 100),
			# (store_sub, reg32, ":score", ":price_discount"),
			# (val_div, reg32, 100),
			# (store_skill_level, reg33, "skl_trade", "$cms_role_storekeeper"),
			# (str_store_troop_name, s31, "$cms_role_storekeeper"),
			# (str_store_item_name, s32, ":item"),
			# (display_message, "@DEBUG (Abilities): {s31}'s TRADE skill ({reg33}) lowers the price of {s32} from {reg31} to {reg32} denars. (USEFUL CONTACTS)", gpu_debug),
		# (try_end), ### DIAGNOSTIC- ###
		(val_sub, ":score", ":price_discount"),
	(try_end),
	
	(assign, reg0, ":score"),
	]),
	
# script_cms_auto_sell
# PURPOSE: Attempt to sell any random junk in the customer's inventory to the merchant as long as they have available funds to buy it.
# EXAMPLE: (call_script, "script_cms_auto_sell", ":customer", ":merchant"),
("cms_auto_sell", 
	[
		(store_script_param_1, ":customer"),
		(store_script_param_2, ":merchant"),
		
		(store_free_inventory_capacity, ":space", ":merchant"),
		(troop_sort_inventory, ":customer"),
		
		(troop_get_inventory_capacity, ":inv_cap", ":customer"),
		(try_for_range_backwards, ":i_slot", 10, ":inv_cap"),
			(troop_get_inventory_slot, ":item_no", ":customer", ":i_slot"),
			(troop_get_inventory_slot_modifier, ":imod", ":customer", ":i_slot"),
			(gt, ":item_no", -1),
			(assign, ":continue", 1),
			(try_begin),
				(call_script, "script_cf_dws_item_in_a_weapon_set", ":customer", ":item_no"), # Prevent sale of weapon set gear.
				(assign, ":continue", 0),
			(else_try),
				# We don't want storekeepers selling books they're supposed to be reading.
				(item_get_type, ":item_type", ":item_no"),
				(eq, ":item_type", itp_type_book),
				(assign, ":continue", 0),
			(try_end),
			(eq, ":continue", 1),
			
			(call_script, "script_cms_get_item_value_with_imod", ":item_no", ":imod", CMS_AUTO_SELLING),
			(assign, ":score", reg0),
			(val_div, ":score", 100),
			(call_script, "script_game_get_item_sell_price_factor", ":item_no"),
			(assign, ":sell_price_factor", reg0),
			(val_mul, ":score", ":sell_price_factor"),
			(val_div, ":score", 100),
			(val_max, ":score",1),
		  
			(store_troop_gold, ":m_gold", ":merchant"),
			(try_begin),
				## WINDYPLAINS+ ## - Troop Effect (BONUS_USEFUL_CONTACTS) - Allows prisoner sale even if no broker is available.
				(is_between, "$cms_role_quartermaster", companions_begin, companions_end), # Companion only effect.
				(call_script, "script_cf_ce_troop_has_ability", "$cms_role_quartermaster", BONUS_USEFUL_CONTACTS),
				(assign, ":useful_contact", 1), # Tracks if sales should be allowed past the merchant's cash amount.
			(else_try),
				(assign, ":useful_contact", 0), 
			(try_end),
			(assign, ":total_excess", 0), # Used to store how much extra cash the player is allowed to spend.
			
			(try_begin),
				## TROOP EFFECT: CARGOMASTER
				(call_script, "script_cf_ce_troop_has_ability", "$cms_role_quartermaster", BONUS_CARGOMASTER), # combat_scripts.py - ability constants in combat_constants.py
				(store_skill_level, ":skill_trade", "skl_trade", "$cms_role_quartermaster"),
				(val_mul, ":skill_trade", 5),
				(store_mul, ":merchant_gold_modified", ":m_gold", ":skill_trade"),
				(val_div, ":merchant_gold_modified", 100),
				# (try_begin), ### DIAGNOSTIC+ ###
					# (ge, DEBUG_TROOP_ABILITIES, 1),
					# (assign, reg31, ":m_gold"),
					# (store_add, reg32, ":m_gold", ":merchant_gold_modified"),
					# (store_skill_level, reg33, "skl_trade", "$cms_role_quartermaster"),
					# (str_store_troop_name, s31, "$cms_role_quartermaster"),
					# (display_message, "@DEBUG (Abilities): {s31}'s TRADE skill ({reg33}) raises the merchant's cash from {reg31} to {reg32} denars. (CARGOMASTER)", gpu_debug),
				# (try_end), ### DIAGNOSTIC- ###
				(val_add, ":merchant_gold_modified", ":m_gold"),
			(else_try),
				(assign, ":merchant_gold_modified", ":m_gold"),
			(try_end),
			(assign, ":merchant_cost", ":score"),
			(try_begin),
				(is_between, ":score", ":m_gold", ":merchant_gold_modified"),
				(assign, ":merchant_cost", ":m_gold"),
			(try_end),
			
			## CONDITIONAL BREAKS TO PREVENT SALE ##
			(gt, ":space", 0),                                # Merchant has room to hold the new item.
			(this_or_next|eq, ":useful_contact", 1),          # The party Quartermaster has the USEFUL CONTACTS ability.
			(lt, ":score", ":merchant_gold_modified"),        # Merchant has enough cash to afford the new item.
			
			## BONUS_USEFUL_CONTACTS - Tallying the effects of this benefit.
			(try_begin),
				(eq, ":useful_contact", 1),
				(gt, ":score", ":merchant_gold_modified"),    # This item is worth more than the merchant can afford.
				(store_sub, ":excess", ":score", ":merchant_gold_modified"),
				(val_add, ":total_excess", ":excess"),
			(else_try),
				(assign, ":excess", 0), # For display purposes below.
			(try_end),
			
			### DIAGNOSTIC+ ###
			# (assign, reg31, ":score"),  # Actual item price.
			# (store_troop_gold, reg32, ":merchant"), # Actual merchant gold. (Simulates ":m_gold")
			# (assign, reg33, ":merchant_gold_modified"), # Enhanced merchant gold due to CARGOMASTER.
			# (store_free_inventory_capacity, reg34, ":merchant"),  # Available merchant inventory space.
			# (store_troop_gold, reg35, ":customer"),
			# (store_free_inventory_capacity, reg36, ":customer"),
			# (str_store_item_name, s31, ":item_no"),
			# (str_store_troop_name, s32, ":merchant"),
			# (str_store_troop_name, s33, ":customer"),
			# (display_message, "@DEBUG (Auto-Sell): Item [{s31}], Value {reg31}.", gpu_debug),
			# (display_message, "@DEBUG (Auto-Sell): Merchant [{s32}], {reg32} gold ({reg33}), {reg34} space", gpu_debug),
			# (display_message, "@DEBUG (Auto-Sell): Customer [{s33}], {reg35} gold, {reg36} space", gpu_debug),
			# (try_begin),
				# (eq, ":useful_contact", 1),
				# (display_message, "@DEBUG (Auto-Sell): SALE OCCURRED.  Merchant gold N/A (USEFUL CONTACTS)", gpu_debug),
			# (else_try),
				# (display_message, "@DEBUG (Auto-Sell): SALE OCCURRED.", gpu_debug),
			# (try_end),
			### DIAGNOSTIC- ###
			
			(troop_add_item, ":merchant", ":item_no", ":imod"),
			(val_sub, ":space", 1),
			(troop_set_inventory_slot, ":customer", ":i_slot", -1),
			(troop_remove_gold, ":merchant", ":merchant_cost"),
			(troop_add_gold, ":customer", ":score"),
			
			### DIAGNOSTIC+ ###
			# (assign, reg31, ":score"),  # Actual item price.
			# (store_troop_gold, reg32, ":merchant"), # Actual merchant gold. (Simulates ":m_gold")
			# (assign, reg33, ":merchant_gold_modified"), # Enhanced merchant gold due to CARGOMASTER.
			# (store_free_inventory_capacity, reg34, ":merchant"),  # Available merchant inventory space.
			# (store_troop_gold, reg35, ":customer"),
			# (store_free_inventory_capacity, reg36, ":customer"),
			# (str_store_item_name, s31, ":item_no"),
			# (str_store_troop_name, s32, ":merchant"),
			# (str_store_troop_name, s33, ":customer"),
			# (display_message, "@DEBUG (Auto-Sell): Merchant [{s32}], {reg32} gold, {reg34} space", gpu_debug),
			# (display_message, "@DEBUG (Auto-Sell): Customer [{s33}], {reg35} gold, {reg36} space", gpu_debug),
			# (try_begin),
				# (ge, ":total_excess", 1),
				# (assign, reg31, ":excess"),
				# (assign, reg32, ":total_excess"),
				# (display_message, "@DEBUG (Auto-Sell): USEFUL CONTACT - Item excess {reg31} denars, Total excess {reg32} denars.", gpu_debug),
			# (try_end),
			# (display_message, "@DEBUG (Auto-Sell): --------------- BREAK BETWEEN ITEMS ----------------", gpu_debug),
			### DIAGNOSTIC- ###
		(try_end), # Inventory Loop
	]),
	
("auto_buy_food", [
	(try_begin),
	  (is_between, "$current_town", towns_begin, towns_end),
	  (party_get_slot, ":merchant_troop", "$current_town", slot_town_merchant),
	(else_try),
	  (is_between, "$current_town", villages_begin, villages_end),
	  (party_get_slot, ":merchant_troop", "$current_town", slot_town_elder),
	(else_try),
	  (assign, ":merchant_troop", -1),
	(try_end),
	##
	
	(try_begin),
		(ge, ":merchant_troop", 1),
		(eq, "$cms_enable_auto_buying", 1),
		(try_begin),
			(neg|main_party_has_troop, "$cms_role_storekeeper"),
			(str_store_troop_name, s21, "$cms_role_storekeeper"),
			(display_message, "@Warning: Your storekeeper, {s21}, is no longer in the party and will need to be reassigned to purchase food.", gpu_red),
		(try_end),
		(main_party_has_troop, "$cms_role_storekeeper"),
		(assign, "$cms_useful_contact_food_discount", 0),
		(store_troop_gold, ":begin_gold", "trp_player"),
		(store_free_inventory_capacity, ":begin_space", "$cms_role_storekeeper"),
		(troop_get_inventory_capacity, ":inv_cap", ":merchant_troop"),
		(set_show_messages, 0),
		(try_for_range, ":i_slot", 10, ":inv_cap"),
		  (troop_get_inventory_slot, ":item", ":merchant_troop", ":i_slot"),
		  (gt, ":item", -1),
		  (is_between, ":item", food_begin, food_end),
		  (troop_inventory_slot_get_item_amount, ":amount", ":merchant_troop", ":i_slot"),
		  (troop_inventory_slot_get_item_max_amount, ":max_amount", ":merchant_troop", ":i_slot"),
		  (eq, ":amount", ":max_amount"),
		  (item_get_slot, ":food_portion", ":item", slot_item_food_portion),
		  (store_item_kind_count, ":food_count", ":item", "$cms_role_storekeeper"),
		  (lt, ":food_count", ":food_portion"),
		  (store_free_inventory_capacity, ":free_inv_cap", "$cms_role_storekeeper"),
		  (gt, ":free_inv_cap", 0),
		  
		  (troop_get_inventory_slot_modifier, ":imod", ":merchant_troop", ":i_slot"),
		  (call_script, "script_cms_get_item_value_with_imod", ":item", ":imod", CMS_AUTO_BUYING),
		  (assign, ":score", reg0),
		  (val_div, ":score", 100),
		  (call_script, "script_game_get_item_buy_price_factor", ":item"),
		  (assign, ":buy_price_factor", reg0),
		  # (store_item_value,":score",":item"),
		  (val_mul, ":score", ":buy_price_factor"),
		  (val_div, ":score", 100),
		  (val_max, ":score",1),
		  (store_troop_gold, ":player_gold", "trp_player"),
		  ## WINDYPLAINS+ ## - Auto-buying minimum cash block.
		  (val_sub, ":player_gold", "$cms_minimum_cash_block"),
		  ## WINDYPLAINS- ##
		  (ge, ":player_gold", ":score"),
		  
		  (troop_add_item, "$cms_role_storekeeper", ":item"),
		  (troop_set_inventory_slot, ":merchant_troop", ":i_slot", -1),
		  (troop_remove_gold, "trp_player", ":score"),
		  (troop_add_gold, ":merchant_troop", ":score"),
		(try_end),
		(set_show_messages, 1),
		(store_troop_gold, ":end_gold", "trp_player"),
		(store_free_inventory_capacity, ":end_space", "$cms_role_storekeeper"),
		(try_begin),
		  (neq, ":end_gold", ":begin_gold"),
		  (store_sub, reg1, ":begin_gold", ":end_gold"),
		  (store_sub, reg2, ":begin_space", ":end_space"),
		  (store_sub, reg3, reg1, 1),
		  (store_sub, reg4, reg2, 1),
		  (str_store_troop_name, s21, "$cms_role_storekeeper"),
		  (try_begin),
			(eq, "$cms_role_storekeeper", "trp_player"),
			(str_store_string, s21, "@You have"),
		  (else_try),
			(str_store_string, s21, "@{s21} has"),
		  (try_end),
		  (display_message, "@{s21} purchased {reg2} {reg4?kinds:kind} of food costing you {reg1} {reg3?denars:denar}."),
		(try_end),
		
		# sell rotten food
		(store_troop_gold, ":begin_gold", "trp_player"),
		(store_free_inventory_capacity, ":begin_space", "$cms_role_storekeeper"),
		(troop_get_inventory_capacity, ":inv_cap", "$cms_role_storekeeper"),
		(set_show_messages, 0),
		(try_for_range, ":i_slot", 10, ":inv_cap"),
		  (troop_get_inventory_slot, ":item", "$cms_role_storekeeper", ":i_slot"),
		  (gt, ":item", -1),
		  (is_between, ":item", food_begin, food_end),
		  (troop_get_inventory_slot_modifier, ":imod", "$cms_role_storekeeper", ":i_slot"),
		  (eq, ":imod", imod_rotten),
		  (store_free_inventory_capacity, ":free_inv_cap", ":merchant_troop"),
		  (gt, ":free_inv_cap", 0),
		  
		  (call_script, "script_cms_get_item_value_with_imod", ":item", ":imod", CMS_AUTO_SELLING),
		  (assign, ":score", reg0),
		  (val_div, ":score", 100),
		  (call_script, "script_game_get_item_sell_price_factor", ":item"),
		  (assign, ":sell_price_factor", reg0),
		  (val_mul, ":score", ":sell_price_factor"),
		  (troop_inventory_slot_get_item_amount, ":amount", "$cms_role_storekeeper", ":i_slot"),
		  (troop_inventory_slot_get_item_max_amount, ":max_amount", "$cms_role_storekeeper", ":i_slot"),
		  (val_mul, ":score", ":amount"),
		  (val_div, ":score", ":max_amount"),
		  (val_div, ":score", 100),
		  (val_max, ":score",1),
		  (store_troop_gold, ":merchant_gold", ":merchant_troop"),
		  (ge, ":merchant_gold", ":score"),
		  
		  #(troop_add_item, ":merchant_troop", ":item", ":imod"),
		  (troop_set_inventory_slot, "$cms_role_storekeeper", ":i_slot", -1),
		  (troop_remove_gold, ":merchant_troop", ":score"),
		  (troop_add_gold, "trp_player", ":score"),
		(try_end),
		(set_show_messages, 1),
		(store_troop_gold, ":end_gold", "trp_player"),
		(store_free_inventory_capacity, ":end_space", "$cms_role_storekeeper"),
		(try_begin),
		  (neq, ":end_gold", ":begin_gold"),
		  (store_sub, reg1, ":end_gold", ":begin_gold"),
		  (store_sub, reg2, ":end_space", ":begin_space"),
		  (store_sub, reg3, reg1, 1),
		  (store_sub, reg4, reg2, 1),
		  (str_store_troop_name, s21, "$cms_role_storekeeper"),
		  (try_begin),
			(eq, "$cms_role_storekeeper", "trp_player"),
			(str_store_string, s21, "@You have"),
		  (else_try),
			(str_store_string, s21, "@{s21} has"),
		  (try_end),
		  (display_message, "@{s21} sold {reg2} {reg4?kinds:kind} of rotten food and gained {reg1} {reg3?denars:denar}."),
		(try_end),
		
		## TROOP EFFECT: BONUS_USEFUL_CONTACTS
		(try_begin),
			(ge, "$cms_useful_contact_food_discount", 1),
			(store_div, reg21, "$cms_useful_contact_food_discount", 100),
			(store_sub, reg22, reg21, 1),
			(troop_get_type, reg23, "$cms_role_storekeeper"),
			(str_store_troop_name, s21, "$cms_role_storekeeper"),
			(display_message, "@{s21}'s useful contacts helped {reg23?her:him} save {reg21} denar{reg22?s:}.", gpu_green),
			(assign, "$cms_useful_contact_food_discount", 0),
		(try_end),
	(try_end),
]),

# script_cf_cms_storekeeper_has_x_of_y_item
# Verifies that your storekeeper has X of Y item #.  If the storekeeper fails to have it then it will check your inventory (provided you were not the storekeeper).
# Outside of kit usage: This is used by the "Center Improvements" kit.
("cf_cms_storekeeper_has_x_of_y_item",
    [
		(store_script_param, ":requested_amount", 1),
		(store_script_param, ":requested_item", 2),
		(store_script_param, ":remove_items", 3), # 0 - just check if you have it, 1 - remove the item.
		
		(try_begin),
			### CHECK STOREKEEPER INVENTORY ###
			# Is a storekeeper assigned and present?
			(neq, "$cms_role_storekeeper", "trp_player"),
			(is_between, "$cms_role_storekeeper", companions_begin, companions_end),
			(main_party_has_troop, "$cms_role_storekeeper"),
			# Initialize variables.
			(assign, ":troop_no", "$cms_role_storekeeper"),
			(assign, ":found", 0),
			# Search for item.
			(troop_get_inventory_capacity, ":capacity", ":troop_no"),
			(try_for_range, ":inventory_slot", 9, ":capacity"),
				(troop_get_inventory_slot, ":item_no", ":troop_no", ":inventory_slot"),
				(eq, ":item_no", ":requested_item"),
				(troop_inventory_slot_get_item_amount, ":current_amount", ":troop_no", ":inventory_slot"),
				(troop_inventory_slot_get_item_max_amount, ":max_amount", ":troop_no", ":inventory_slot"),
				(ge, ":current_amount", ":max_amount"),
				(val_add, ":found", 1),
			(try_end),
			(ge, ":found", ":requested_amount"),
			(assign, ":continue", 1),
			
		(else_try),
			### CHECK PLAYER INVENTORY ###
			(this_or_next|lt, ":found", ":requested_amount"),
			(eq, "$cms_role_storekeeper", "trp_player"),
			(assign, ":troop_no", "trp_player"),
			(assign, ":found", 0),
			# Search for item.
			(troop_get_inventory_capacity, ":capacity", ":troop_no"),
			(try_for_range, ":inventory_slot", 9, ":capacity"),
				(troop_get_inventory_slot, ":item_no", ":troop_no", ":inventory_slot"),
				(eq, ":item_no", ":requested_item"),
				(troop_inventory_slot_get_item_amount, ":current_amount", ":troop_no", ":inventory_slot"),
				(troop_inventory_slot_get_item_max_amount, ":max_amount", ":troop_no", ":inventory_slot"),
				(ge, ":current_amount", ":max_amount"),
				(val_add, ":found", 1),
			(try_end),
			(ge, ":found", ":requested_amount"),
			(assign, ":continue", 1),
			
		(else_try),
			# No one has enough of this item.  Fail the check.
			(assign, ":continue", 0),
		(try_end),
		
		(eq, ":continue", 1),  ## CONDITIONAL BREAK ##
		
		# Remove the requested items if ":remove_items" = 1
		(try_begin),
			(eq, ":remove_items", 1),
			# Search for item.
			(troop_get_inventory_capacity, ":capacity", ":troop_no"),
			(try_for_range, ":inventory_slot", 9, ":capacity"),
				(gt, ":requested_amount", 0),
				(troop_get_inventory_slot, ":item_no", ":troop_no", ":inventory_slot"),
				(eq, ":item_no", ":requested_item"),
				(troop_inventory_slot_get_item_amount, ":current_amount", ":troop_no", ":inventory_slot"),
				(troop_inventory_slot_get_item_max_amount, ":max_amount", ":troop_no", ":inventory_slot"),
				(ge, ":current_amount", ":max_amount"),
				(str_store_item_name, s21, ":item_no"),
				(str_store_troop_name, s22, ":troop_no"),
				(troop_set_inventory_slot, ":troop_no", ":inventory_slot", -1),
				(display_message, "@{s22} has lost 1 {s21}."),
				(val_sub, ":requested_amount", 1),
			(try_end),
		(try_end),
		
	]),
]


from util_wrappers import *
from util_scripts import *

scripts_directives = [
	#rename scripts to "insert" switch scripts (see end of scripts[])  
	[SD_RENAME, "consume_food" , "consume_food_orig"],                                               # Replaced for using the storekeeper role.
	[SD_RENAME, "cf_player_has_item_without_modifier" , "cf_player_has_item_without_modifier_orig"], # Replaced for using the storekeeper role.
	
	# HOOK: Alters native script to allow player selected jailer's prisoner management skill to function.
	[SD_OP_BLOCK_INSERT, "game_get_party_prisoner_limit", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (assign, ":troop_no", "trp_player"), 0, 
		[(assign, ":troop_no", "$cms_role_jailer"),], 1],
	
] # scripts_rename
                
def modmerge_scripts(orig_scripts):
	# process script directives first
	process_script_directives(orig_scripts, scripts_directives)
	# add remaining scripts
	add_scripts(orig_scripts, scripts, True)
	
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "scripts"
        orig_scripts = var_set[var_name_1]
    
        
		# START do your own stuff to do merging
		
        modmerge_scripts(orig_scripts)

		# END do your own stuff
        
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
