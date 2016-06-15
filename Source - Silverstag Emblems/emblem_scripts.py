# Companion Management System (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	
###########################################################################################################################
#####                                          PLAYER EMBLEM OPTIONS HUB                                              #####
###########################################################################################################################

# script_pep_create_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate this code for each window.
("pep_create_mode_switching_buttons",
    [
		### COMMON ELEMENTS ###
		(assign, "$gpu_storage", EMBLEM_OBJECTS),
		(assign, "$gpu_data",    EMBLEM_OBJECTS),
		
		# Text Labels
		(str_store_string, s21, "@Player Emblem Options"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, pep1_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", pep1_obj_main_title, 150),
		
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, pep1_obj_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", pep1_obj_main_title2, 150),
		
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		## CURRENT EMBLEMS AVAILABLE
		(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
		(try_begin),
			(ge, reg1, 1),
			(store_sub, reg21, reg1, 1),
			(str_store_string, s21, "@You currently have {reg1} emblem{reg21?s:}."),
		(else_try),
			(str_store_string, s21, "@You do not currently have any emblems."),
		(try_end),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 635, 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		# Setup an initial false value for objects so if they don't get loaded they aren't 0's.
		(try_for_range, ":slot_no", 0, 50),
			(store_add, ":value", ":slot_no", 1234),
			(troop_set_slot, EMBLEM_OBJECTS, ":slot_no", ":value"),
		(try_end),
		
		## CONTAINERS ##
		(call_script, "script_gpu_container_heading", 50, 80, 175, 505, pep1_obj_container_1),
			
			## BUTTONS ##
			(assign, ":x_buttons", 0), # 90 
			(assign, ":y_button_step", 55),
			(assign, ":pos_y", 420),
			
			(str_store_string, s21, "@Emblem Info "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", pep1_obj_button_emblem_info), ### EMBLEM INFO ###
			
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@Character Resets "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", pep1_obj_button_character_resets), ### CHARACTER RESETS ###
			
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@Development "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", pep1_obj_button_statistics), ### CHARACTER STATS ###
			
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@Miscellaneous "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", pep1_obj_button_misc_options), ### MISC OPTIONS ###
			
			(try_begin),
				(ge, BETA_TESTING_MODE, 1),
				(val_sub, ":pos_y", ":y_button_step"),
				(str_store_string, s21, "@Debugging "),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", pep1_obj_button_debugging), ### DEBUGGING OPTIONS ###
			(try_end),
			
		(set_container_overlay, -1),
		(call_script, "script_gpu_create_mesh", "mesh_button_up", 55, 35, 350, 500),
		(str_store_string, s21, "@Done"),
		(call_script, "script_gpu_create_button", "str_hub_s21", 65, 40, pep1_obj_button_done),
	]),
	
# script_pep_handle_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate the code to handle their functionality for each window.
("pep_handle_mode_switching_buttons",
    [
		(store_script_param, ":object", 1),
		(store_script_param, ":value", 2),
		(assign, reg1, ":value"), # So it won't be whined about.
		
		### COMMON ELEMENTS ###
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep1_obj_button_done, ":object"),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_reports"),
			
		(else_try), ####### BUTTON : EMBLEM INFORMATION #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep1_obj_button_emblem_info, ":object"),
			(assign, "$pep_mode", PEP_MODE_INFORMATIONAL),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_player_emblem_switch_modes"),
			
		(else_try), ####### BUTTON : CHARACTER RESETS #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep1_obj_button_character_resets, ":object"),
			(assign, "$pep_mode", PEP_MODE_CHARACTER_RESET),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_player_emblem_switch_modes"),
			
		(else_try), ####### BUTTON : CHARACTER STATISTICS #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep1_obj_button_statistics, ":object"),
			(assign, "$pep_mode", PEP_MODE_STATISTICS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_player_emblem_switch_modes"),
			
		(else_try), ####### BUTTON : MISC OPTIONS #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep1_obj_button_misc_options, ":object"),
			(assign, "$pep_mode", PEP_MODE_MISC),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_player_emblem_switch_modes"),
			
		(else_try), ####### BUTTON : DEBUGGING #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep1_obj_button_debugging, ":object"),
			(assign, "$pep_mode", PEP_MODE_DEBUGGING),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_player_emblem_switch_modes"),
			
		(try_end),
	]),
	
# script_emblem_reset_troop_attributes
# PURPOSE: Handles resetting a troop's attributes back to 4 and refunding everything above that as unspent points.
# EXAMPLE: (call_script, "script_emblem_reset_troop_attributes", ":troop_no"), # emblem_scripts.py
("emblem_reset_troop_attributes",
    [
		(store_script_param, ":troop_no", 1),
		
		# Get unspent points.
		(troop_get_attribute_points, ":unspent", ":troop_no"),
		# Strength
		(store_attribute_level, ":value", ":troop_no", ca_strength),
		(val_sub, ":value", 4),
		(troop_set_attribute, ":troop_no", ca_strength, 4),
		(val_add, ":unspent", ":value"),
		# Agility
		(store_attribute_level, ":value", ":troop_no", ca_agility),
		(val_sub, ":value", 4),
		(troop_set_attribute, ":troop_no", ca_agility, 4),
		(val_add, ":unspent", ":value"),
		# # Intelligence
		# (store_attribute_level, ":value", ":troop_no", ca_intelligence),
		# (val_sub, ":value", 4),
		# (troop_set_attribute, ":troop_no", ca_intelligence, 4),
		# (val_add, ":unspent", ":value"),
		# Charisma
		(store_attribute_level, ":value", ":troop_no", ca_charisma),
		(val_sub, ":value", 4),
		(troop_set_attribute, ":troop_no", ca_charisma, 4),
		(val_add, ":unspent", ":value"),
		# Set total unspent points.
		(troop_set_attribute_points, ":troop_no", ":unspent"),
		# Handle notification.
		(try_begin),
			(main_party_has_troop, ":troop_no"),
			(troop_get_type, reg1, ":troop_no"),
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(str_store_string, s1, "@You have"),
				(str_store_string, s3, "@your"),
			(else_try),
				(str_store_troop_name, s2, ":troop_no"),
				(str_store_string, s1, "@{s2} has"),
				(str_store_string, s3, "@{reg1?her:his}"),
			(try_end),
			(display_message, "@{s1} reset all of {s3} attribute points.", gpu_green),
		(try_end),
	]),
	
# script_emblem_reset_troop_skills
# PURPOSE: Handles resetting a troop's skills & INT back to 0 and refunding everything above that as unspent points.
# EXAMPLE: (call_script, "script_emblem_reset_troop_skills", ":troop_no"), # emblem_scripts.py
("emblem_reset_troop_skills",
    [
		(store_script_param, ":troop_no", 1),
		
		## ATTRIBUTES:
		# Get unspent points.
		(troop_get_attribute_points, ":unspent_attributes", ":troop_no"),
		# Intelligence
		(store_attribute_level, ":INT", ":troop_no", ca_intelligence),
		(val_sub, ":INT", 4),
		(troop_set_attribute, ":troop_no", ca_intelligence, 4),
		(val_add, ":unspent_attributes", ":INT"),
		
		## SKILLS:
		# Get unspent points.
		(troop_get_skill_points, ":unspent_skills", ":troop_no"),
		(val_sub, ":unspent_skills", ":INT"), # Done to remove extra skills granted by intelligence.
		# Cycle through skills and refund any spent points.
		(try_for_range, ":skill_no", 0, 42),
			(store_skill_level, ":value_before", ":skill_no", ":troop_no"),
			(troop_set_skill, ":troop_no", ":skill_no", 0),
			(store_skill_level, ":value_after", ":skill_no", ":troop_no"),
			# Account for encumbrance penalties that might be in effect.
			(try_begin),
				(eq, "$enable_encumbrance", 1),
				(this_or_next|eq, ":troop_no", "trp_player"),
				(is_between, ":troop_no", companions_begin, companions_end),
				(call_script, "script_cf_ce_skill_affected_by_encumbrance", ":skill_no"), # combat_scripts.py
				(call_script, "script_ce_get_troop_encumbrance", ":troop_no", ":skill_no"), # combat_scripts.py
				(val_add, ":value_before", reg3),
			(try_end),
			(store_sub, ":value", ":value_before", ":value_after"),
			(val_add, ":unspent_skills", ":value"),
			### DIAGNOSTIC+ ###
			# (str_store_skill_name, s31, ":skill_no"),
			# (assign, reg31, ":skill_no"),
			# (assign, reg32, ":value_before"),
			# (assign, reg33, ":unspent_skills"),
			# (assign, reg34, ":value_after"),
			# (display_message, "@DEBUG: {s31} #{reg31} changed from {reg32} to {reg34}.  Unspent Skills = {reg33}.", gpu_debug),
			### DIAGNOSTIC- ###
		(try_end),
		# Set total unspent points.
		(troop_set_skill_points, ":troop_no", ":unspent_skills"),
		# Handle notification.
		(try_begin),
			(main_party_has_troop, ":troop_no"),
			(troop_get_type, reg1, ":troop_no"),
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(str_store_string, s1, "@You have"),
				(str_store_string, s3, "@your"),
				(str_store_string, s4, "@have"),
			(else_try),
				(str_store_troop_name, s2, ":troop_no"),
				(str_store_string, s1, "@{s2} has"),
				(str_store_string, s3, "@{reg1?her:his}"),
				(str_store_string, s4, "@has"),
			(try_end),
			(assign, reg2, ":unspent_skills"),
			(assign, reg3, ":unspent_attributes"),
			(display_message, "@{s1} reset {s3} intelligence and {s4} been refunded {reg3} attribute points.", gpu_green),
			(display_message, "@{s1} reset all of {s3} skills and {s4} been refunded {reg2} skill points.", gpu_green),
		(try_end),
	]),
	
# script_emblem_reset_troop_proficiencies
# PURPOSE: Handles resetting a troop's proficiencies back to 25 and refunding everything above that as unspent points.
# EXAMPLE: (call_script, "script_emblem_reset_troop_proficiencies", ":troop_no"), # emblem_scripts.py
("emblem_reset_troop_proficiencies",
    [
		(store_script_param, ":troop_no", 1),
		
		# Get unspent points.
		(troop_get_proficiency_points, ":unspent", ":troop_no"),
		
		# One Handed
		(store_proficiency_level, ":value", ":troop_no", wpt_one_handed_weapon),
		(troop_set_proficiency, ":troop_no", wpt_one_handed_weapon, 25),
		(try_begin),
			(ge, ":value", 100), # 2 points for every 1 proficiency in this range.
			(store_sub, ":refunded_points", ":value", 100),
			(val_mul, ":refunded_points", 2),
			(val_div, ":refunded_points", 1),
			(assign, ":value", 99),
			(val_add, ":unspent", ":refunded_points"),
		(try_end),
		(try_begin),
			(ge, ":value", 75), # 5 points for every 3 proficiency in this range.
			(store_sub, ":refunded_points", ":value", 75),
			(val_mul, ":refunded_points", 5),
			(val_div, ":refunded_points", 3),
			(assign, ":value", 74),
			(val_add, ":unspent", ":refunded_points"),
		(try_end),
		(try_begin),
			(ge, ":value", 50), # 1 points for every 1 proficiency in this range.
			(store_sub, ":refunded_points", ":value", 25),
			(val_add, ":unspent", ":refunded_points"),
		(try_end),
		
		
		# Set total unspent points.
		(troop_set_proficiency_points, ":troop_no", ":unspent"),
		# Handle notification.
		(try_begin),
			(main_party_has_troop, ":troop_no"),
			(troop_get_type, reg1, ":troop_no"),
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(str_store_string, s1, "@You have"),
				(str_store_string, s3, "@your"),
				(str_store_string, s4, "@have"),
			(else_try),
				(str_store_troop_name, s2, ":troop_no"),
				(str_store_string, s1, "@{s2} has"),
				(str_store_string, s3, "@{reg1?her:his}"),
				(str_store_string, s4, "@has"),
			(try_end),
			(assign, reg2, ":unspent"),
			(display_message, "@{s1} reset all of {s3} weapon proficiencies and {s4} been refunded {reg2} points.", gpu_green),
		(try_end),
	]),
	
	
###########################################################################################################################
#####                                               EMBLEM HANDLING                                                   #####
###########################################################################################################################

# script_emblem_award_to_player
# PURPOSE: Adds the specificed number of emblems to the player's inventory.
# EXAMPLE: (call_script, "script_emblem_award_to_player", ":quantity"), # emblem_scripts.py
("emblem_award_to_player",
    [
		(store_script_param, ":emblems_awarded", 1),
		
		# Add awarded emblems from player's inventory.
		(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
		(assign, ":emblems_carried", reg1),
		
		(try_begin),
			(ge, ":emblems_carried", EMBLEM_MAX_QUANTITY),
			(display_message, "@WARNING - Emblems have not been awarded as you are carrying the maximum amount.", gpu_red),
		(else_try),
			(store_add, ":combined", ":emblems_carried", ":emblems_awarded"),
			(gt, ":combined", EMBLEM_MAX_QUANTITY),
			(display_message, "@WARNING - Emblems will only be partially awarded as you will reach the maximum amount.", gpu_red),
		(try_end),
		
		# Determine limit to award.
		(store_sub, ":max_amount", EMBLEM_MAX_QUANTITY, ":emblems_carried"),
		(assign, ":emblems_to_award", ":emblems_awarded"),
		(val_min, ":emblems_to_award", ":max_amount"),
		
		(try_begin),
			## LOGIC - No emblems carried, add item to inventory & set amount to quantity awarded.
			(lt, ":emblems_carried", 1),
			(try_begin),
				# Find an open slot in the player's inventory for this stack.
				(troop_get_inventory_capacity, ":inventory_capacity", "trp_player"),
				(assign, ":free_slot", -1),
				(try_for_range, ":inv_slot", 10, ":inventory_capacity"),
					(troop_get_inventory_slot, ":item_no", "trp_player", ":inv_slot"),
					(lt, ":item_no", 1),
					(assign, ":free_slot", ":inv_slot"),
					(break_loop),
				(try_end),
				
				# If no free slot can be found then store in overflow.
				(try_begin),
					(neg|is_between, ":free_slot", 10, ":inventory_capacity"),
					(display_message, "@WARNING - No free inventory space available to store awarded emblems.  Stored in overflow.", gpu_red),
					(val_add, "$emblem_overflow", ":emblems_to_award"),
				(try_end),
				(is_between, ":free_slot", 10, ":inventory_capacity"),
				
				# Assign stack to player inventory.
				(troop_set_inventory_slot, "trp_player", ":free_slot", SILVERSTAG_EMBLEM),
				(troop_inventory_slot_set_item_amount, "trp_player", ":free_slot", ":emblems_to_award"),
				
				# Display award.
				(assign, reg31, ":emblems_to_award"),
				(store_sub, reg32, reg31, 1),
				(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
				(assign, reg33, reg1),
				(assign, reg34, EMBLEM_MAX_QUANTITY),
				(display_message, "@You have been awarded {reg31} emblem{reg32?s:}. ({reg33} / {reg34})", gpu_green),
				
				### METRICS+ ### - EMBLEMS EARNED
				(troop_get_slot, ":earned", METRICS_DATA, metrics_emblems_total_earned),
				(val_add, ":earned", ":emblems_to_award"),
				(troop_set_slot, METRICS_DATA, metrics_emblems_total_earned, ":earned"),
				(try_begin),
					(eq, "$enable_metrics", 1),
					(troop_get_slot, reg31, METRICS_DATA, metrics_emblems_total_earned),
					(store_sub, reg32, reg31, 1),
					(display_message, "@METRIC (Emblems): You have earned a total of {reg31} emblem{reg32?s:}.", gpu_debug),
				(try_end),
				### METRICS- ###
			(try_end),
			
		(else_try),
			## LOGIC - Emblems are currently carried.  Find that item and improve it's quantity by the amount awarded.
			
			(try_begin),
				# Find the current stack the player has.
				(assign, ":emblem_slot", -1),
				(troop_get_inventory_capacity, ":inventory_capacity", "trp_player"),
				(try_for_range, ":inv_slot", 10, ":inventory_capacity"),
					(troop_get_inventory_slot, ":item_no", "trp_player", ":inv_slot"),
					(eq, ":item_no", SILVERSTAG_EMBLEM),
					(assign, ":emblem_slot", ":inv_slot"),
					(break_loop),
				(try_end),
				(is_between, ":emblem_slot", 10, ":inventory_capacity"),
				
				# Update that stack by the awarded amounts.
				(troop_inventory_slot_get_item_amount, ":emblem_count", "trp_player", ":emblem_slot"),
				(val_add, ":emblem_count", ":emblems_to_award"),
				(val_min, ":emblem_count", EMBLEM_MAX_QUANTITY),
				(troop_inventory_slot_set_item_amount, "trp_player", ":emblem_slot", ":emblem_count"),
				
				# Display award.
				(assign, reg31, ":emblems_to_award"),
				(store_sub, reg32, reg31, 1),
				(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
				(assign, reg33, reg1),
				(assign, reg34, EMBLEM_MAX_QUANTITY),
				(display_message, "@You have been awarded {reg31} emblem{reg32?s:}. ({reg33} / {reg34})", gpu_green),
				
				### METRICS+ ### - EMBLEMS EARNED
				(troop_get_slot, ":earned", METRICS_DATA, metrics_emblems_total_earned),
				(val_add, ":earned", ":emblems_to_award"),
				(troop_set_slot, METRICS_DATA, metrics_emblems_total_earned, ":earned"),
				(try_begin),
					(eq, "$enable_metrics", 1),
					(troop_get_slot, reg31, METRICS_DATA, metrics_emblems_total_earned),
					(store_sub, reg32, reg31, 1),
					(display_message, "@METRIC (Emblems): You have earned a total of {reg31} emblem{reg32?s:}.", gpu_debug),
				(try_end),
				### METRICS- ###
			(try_end),
			
		(try_end),
	]),
	
# script_emblem_get_current_quantity
# PURPOSE: Serves as a utility script to find out how many emblems a player currently has as store_item_kind_count will just return # of stacks.
# EXAMPLE: (call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
("emblem_get_current_quantity",
    [
		(store_item_kind_count, ":emblems_carried", SILVERSTAG_EMBLEM, "trp_player"),
		(assign, reg1, 0),
		
		(try_begin),
			(lt, ":emblems_carried", 1),
			(assign, reg1, 0),
		(else_try),
			(assign, ":emblem_slot", -1),
			(troop_get_inventory_capacity, ":inventory_capacity", "trp_player"),
			(try_for_range, ":inv_slot", 10, ":inventory_capacity"),
				(troop_get_inventory_slot, ":item_no", "trp_player", ":inv_slot"),
				(eq, ":item_no", SILVERSTAG_EMBLEM),
				(assign, ":emblem_slot", ":inv_slot"),
				(break_loop),
			(try_end),
			(is_between, ":emblem_slot", 10, ":inventory_capacity"),
			(troop_inventory_slot_get_item_amount, reg1, "trp_player", ":emblem_slot"),
		(try_end),
		
	]),
	
# script_cf_emblem_spend_emblems
# PURPOSE: Remove emblems from the player inventory if sufficient quantity exists.  This serves as a gate to whether an emblem service can be purchased.
# EXAMPLE: (call_script, "script_cf_emblem_spend_emblems", ":quantity"), # emblem_scripts.py
("cf_emblem_spend_emblems",
    [
		(store_script_param, ":quantity", 1),
		
		(assign, ":pass", 0),
		
		# Add awarded emblems from player's inventory.
		(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
		(assign, ":emblems_carried", reg1),
		
		(try_begin),
			(ge, ":emblems_carried", ":quantity"),
			## LOGIC - Emblems are currently carried.  Find that item and improve it's quantity by the amount awarded.
			(try_begin),
				# Find the current stack the player has.
				(assign, ":emblem_slot", -1),
				(troop_get_inventory_capacity, ":inventory_capacity", "trp_player"),
				(try_for_range, ":inv_slot", 10, ":inventory_capacity"),
					(troop_get_inventory_slot, ":item_no", "trp_player", ":inv_slot"),
					(eq, ":item_no", SILVERSTAG_EMBLEM),
					(assign, ":emblem_slot", ":inv_slot"),
					(break_loop),
				(try_end),
				(is_between, ":emblem_slot", 10, ":inventory_capacity"),
				
				# Update that stack by the awarded amounts.
				(troop_inventory_slot_get_item_amount, ":emblem_count", "trp_player", ":emblem_slot"),
				(val_sub, ":emblem_count", ":quantity"),
				(troop_inventory_slot_set_item_amount, "trp_player", ":emblem_slot", ":emblem_count"),
				
				# Display award.
				(assign, reg31, ":quantity"),
				(store_sub, reg32, reg31, 1),
				(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
				(assign, reg33, reg1),
				(assign, reg34, EMBLEM_MAX_QUANTITY),
				(display_message, "@You have used {reg31} emblem{reg32?s:}. ({reg33} / {reg34})", gpu_debug),
				
				### METRICS+ ### - EMBLEMS SPENT
				(troop_get_slot, ":spent", METRICS_DATA, metrics_emblems_total_spent),
				(val_add, ":spent", ":quantity"),
				(troop_set_slot, METRICS_DATA, metrics_emblems_total_spent, ":spent"),
				(try_begin),
					(eq, "$enable_metrics", 1),
					(troop_get_slot, reg31, METRICS_DATA, metrics_emblems_total_spent),
					(store_sub, reg32, reg31, 1),
					(display_message, "@METRIC (Emblems): You have spent a total of {reg31} emblem{reg32?s:}.", gpu_debug),
				(try_end),
				### METRICS- ###
			(try_end),
			(assign, ":pass", 1),
			
		(else_try),
			(display_message, "@You have insufficient emblems for this purpose.", gpu_red),
			(assign, ":pass", 0),
		(try_end),
		(eq, ":pass", 1),
	]),
	

# script_cf_emblem_quest_reward_check
# EXAMPLE: (call_script, "script_cf_emblem_quest_reward_check", ":quantity"), # emblem_scripts.py
("cf_emblem_quest_reward_check",
    [
		(store_script_param, ":quantity", 1),
		
		(val_max, ":quantity", 1),
		
		# Setup DC.
		(try_begin),
			(assign, ":DC", 10),
			(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
			(val_add, ":DC", 40),
			(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
			(val_add, ":DC", 50),
		(try_end),
		
		(try_begin),
			(ge, ":quantity", 2),
			(store_mul, ":limited_quantity", ":quantity", ":DC"),
			(val_div, ":limited_quantity", 100),
			(ge, ":limited_quantity", 1),
			(call_script, "script_emblem_award_to_player", ":limited_quantity"), # emblem_scripts.py
		(else_try),
			(store_random_in_range, ":roll", 0, 100),
			(lt, ":roll", ":DC"),
			(call_script, "script_emblem_award_to_player", 1), # emblem_scripts.py
		(try_end),
	]),
	
	
# script_emblem_instantly_complete_reading_companion
# EXAMPLE: (call_script, "script_emblem_instantly_complete_reading_companion"), # emblem_scripts.py
("emblem_instantly_complete_reading_companion",
    [
		(assign, ":troop_no", "$temp"),
		
		(try_begin),
			# Get the companion's current reading book.
			(troop_get_slot, ":item_no", ":troop_no", slot_troop_reading_book),
			(is_between, ":item_no", readable_books_begin, readable_books_end),
			# Spend Emblems.
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_FINISH_BOOK_COMPANION),
			# Set progress to 1000. (completed)
			(store_sub, ":companion_no", ":troop_no", companions_begin),
			(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
			(item_set_slot, ":item_no", ":book_read_slot", 999),
			(change_screen_map),
			(rest_for_hours_interactive, 2, 5, 0),
		(else_try),
			(jump_to_menu, "mnu_cms_companion_reading"),
		(try_end),
	]),
	
	
# script_cf_emblem_spend_emblems
# EXAMPLE: (call_script, "script_cf_emblem_spend_emblems", ":quantity"), # emblem_scripts.py
# ("emblem_instantly_complete_reading_companion",
    # [
		# (store_script_param, ":quantity", 1),
		
	# ]),
	
# script_emblem_remove_from_merchants
# PURPOSE: Searches the inventories of each merchant in a center to immediately remove emblems from them.
# EXAMPLE: (call_script, "script_emblem_remove_from_merchants", ":center_no"), # emblem_scripts.py
("emblem_remove_from_merchants",
    [
		(store_script_param, ":center_no", 1),
		
		(try_begin),
			(is_between, ":center_no", towns_begin, towns_end),
			(call_script, "script_emblem_remove_emblems_from_town_merchant", ":center_no", armor_merchants_begin),
			(call_script, "script_emblem_remove_emblems_from_town_merchant", ":center_no", weapon_merchants_begin),
			(call_script, "script_emblem_remove_emblems_from_town_merchant", ":center_no", tavernkeepers_begin),
			(call_script, "script_emblem_remove_emblems_from_town_merchant", ":center_no", goods_merchants_begin),
			(call_script, "script_emblem_remove_emblems_from_town_merchant", ":center_no", horse_merchants_begin),
		(try_end),
	]),
	
# script_emblem_remove_emblems_from_town_merchant
# PURPOSE: Searches the inventories of each merchant in a center to immediately remove emblems from them.
# EXAMPLE: (call_script, "script_emblem_remove_emblems_from_town_merchant", ":center_no", ":merchant_type"), # emblem_scripts.py
("emblem_remove_emblems_from_town_merchant",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":merchant_type", 2),
		
		(try_begin),
			# Quality filters.
			
			# Determine Our Town Offset.
			(store_sub, ":offset", ":center_no", towns_begin),
			(store_add, ":merchant", ":merchant_type", ":offset"),
			
			(store_item_kind_count, ":emblems_carried", SILVERSTAG_EMBLEM, ":merchant"),
			(ge, ":emblems_carried", 1),
			
			(troop_get_inventory_capacity, ":inventory_capacity", ":merchant"),
			(try_for_range, ":inv_slot", 0, ":inventory_capacity"),
				(troop_get_inventory_slot, ":item_no", ":merchant", ":inv_slot"),
				(eq, ":item_no", SILVERSTAG_EMBLEM),
				(troop_set_inventory_slot, ":merchant", ":inv_slot", -1),
				(val_sub, ":emblems_carried", 1),
				
				### DIAGNOSTIC+ ###
				(try_begin),
					(ge, BETA_TESTING_MODE, 1),
					(assign, reg30, ":inv_slot"),
					(str_store_troop_name, s31, ":merchant"),
					(assign, reg31, ":merchant"),
					(str_store_party_name, s32, ":center_no"),
					(display_message, "@DEBUG (emblem): Emblem removed from {s31} (#{reg31}) from slot #{reg30} in {s32}.", gpu_debug),
				(try_end),
				### DIAGNOSTIC- ###
				
				(neg|gt, ":emblems_carried", 0),
				(break_loop),
			(try_end),
			
		(try_end),
	]),
	
# script_emblem_add_option_header
# PURPOSE: Serves as a utility script to find out how many emblems a player currently has as store_item_kind_count will just return # of stacks.
# EXAMPLE: (call_script, "script_emblem_add_option_header", ":title", ":pos_y", ":button_storage", ":emblem_cost"), # emblem_scripts.py
("emblem_add_option_header",
    [
		(store_script_param, ":title", 1),
		(store_script_param, ":pos_y", 2),
		(store_script_param, ":button_storage", 3),
		(store_script_param, ":emblem_cost", 4),
		
		(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
		(assign, ":emblems_available", reg1),
		
		## OBJ - TEXT - OPTION TITLE
		(call_script, "script_gpu_create_text_label", ":title", 305, ":pos_y", 0, gpu_center),
		(call_script, "script_gpu_create_text_label", ":title", 305, ":pos_y", 0, gpu_center),
		
		## OBJ - BUTTON - OPTION SPENDING BUTTON
		(try_begin),
			(ge, ":emblems_available", ":emblem_cost"),
			(str_store_string, s21, "@Buy"),
			(store_sub, ":pos_y_temp", ":pos_y", 57),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 590, ":pos_y_temp", ":button_storage"),
		(try_end),
		
		## OBJ - TEXT - OPTION COST
		(assign, reg21, ":emblem_cost"),
		(str_store_string, s21, "@{reg21}"),
		(store_sub, ":pos_y_temp", ":pos_y", 27),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 60, ":pos_y_temp", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 110),
		
		## OBJ - TEXT - OPTION COST
		(store_sub, reg22, ":emblem_cost", 1),
		(str_store_string, s21, "@Emblem{reg22?s:}"),
		(val_sub, ":pos_y_temp", 20),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 60, ":pos_y_temp", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
			
	]),
]


from util_wrappers import *
from util_scripts import *

def modmerge_scripts(orig_scripts):
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