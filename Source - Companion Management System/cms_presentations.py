# Companion Management System (1.0) by Windyplains

from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
from header_items import *   # Added for Show all Items presentation.
from module_items import *   # Added for Show all Items presentation.
import string

####################################################################################################################
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################

presentations = [
###########################################################################################################################
#####                                             DYNAMIC WEAPON SYSTEM                                               #####
###########################################################################################################################
# This preference panel will set what kinds of equipment the player wishes allowed in each city's specific tournaments.
  ("dws_settings", 0, mesh_load_window, [
    (ti_on_presentation_load,
    [
		(set_fixed_point_multiplier, 1000),
		 
		(assign, "$gpu_storage", DWS_OBJECTS),
		(assign, "$gpu_data",    DWS_OBJECTS),
		
		# Button Definitions
		(call_script, "script_gpu_create_game_button", "str_cms_accept", 885, 30, dws_obj_button_accept),
		(call_script, "script_gpu_create_game_button", "str_cms_cancel", 695, 30, dws_obj_button_cancel),
		(call_script, "script_gpu_create_game_button", "str_dws_test", 505, 30, dws_obj_test),
		
		(call_script, "script_gpu_draw_line", 852, 40, 73, 650, gpu_brown), # Brown background
		(call_script, "script_gpu_draw_line", 852, 2, 73, 690, gpu_black), # - Header
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_black), # - Footer
		(call_script, "script_gpu_draw_line", 2, 40, 73, 650, gpu_black), # | Left border
		(call_script, "script_gpu_draw_line", 2, 40, 923, 650, gpu_black), # | Right border
		
		# Text Labels
		(call_script, "script_gpu_create_text_label", "str_dws_main_title", 500, 665, dws_obj_label_main_title, gpu_center_with_outline), # 680
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", dws_obj_label_main_title, 150),
		(call_script, "script_gpu_create_text_label", "str_dws_inventory_title", 455, 620, 0, gpu_center),
		(call_script, "script_gpu_create_text_label", "str_dws_battlefield_title", 795, 620, 0, gpu_center),
		(call_script, "script_gpu_create_text_label", "str_dws_siege_title", 795, 470, 0, gpu_center),
		(call_script, "script_gpu_create_text_label", "str_dws_selected_title", 795, 320, 0, gpu_center),
		
		# Create Character Portrait
		(call_script, "script_gpu_create_portrait", "$dws_troop", 70, 465, 500, dws_obj_portrait_selected_troop),
		
		# CHARACTER MENU BEGIN
		(position_set_x, pos1, 190),
        (position_set_y, pos1, 425),
		
		(troop_get_slot, ":selected_profile", DWS_OBJECTS, dws_val_menu_selected_character),
		(create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
		(troop_set_slot, DWS_OBJECTS, dws_obj_menu_selected_character, reg1),
		(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
		(assign, ":hero_slot", 0),
        (try_for_range, ":stack_num", 0, ":num_stacks"),
			(store_add, ":slot_pick", dws_val_menu_troop_1, ":hero_slot"),
			(party_stack_get_troop_id,":troop_no","p_main_party",":stack_num"),
			(troop_is_hero, ":troop_no"),
			(str_clear, s1),
			(str_store_troop_name, s1, ":troop_no"),
			(troop_set_slot, DWS_OBJECTS, ":slot_pick", ":troop_no"),
			(try_begin),
				(ge, DEBUG_DWS, 2),
				(assign, reg31, ":slot_pick"),
				(display_message, "@DEBUG (DWS): Added '{s1}' to character chooser menu.  Slot #{reg31}"),
			(try_end),
			(val_add, ":hero_slot", 1),
			(overlay_add_item, reg1, "@{s1}"),
        (try_end),
		(overlay_set_val, reg1, ":selected_profile"),
		(call_script, "script_gpu_resize_object", dws_obj_menu_selected_character, 75),
		# CHARACTER MENU END
		
		# ITEM MESH
		# script_gpu_create_mesh         - mesh_id, pos_x, pos_y, size_x, size_y
		(assign, ":left_margin", 290),
		(assign, ":pos_x", ":left_margin"),
		(assign, ":pos_y", 515),
		(assign, ":slot_no", 0),
		(assign, ":box_size", 80),
		(store_mul, ":limit_x", ":box_size", 4),
		(val_add, ":limit_x", ":pos_x"),
		(troop_get_inventory_capacity, ":inv_cap", "$dws_troop"),
		(try_for_range, ":inv_slot", 0, ":inv_cap"),
			(troop_get_inventory_slot, ":item_no", "$dws_troop", ":inv_slot"),
			(ge, ":item_no", 1), # Valid Item
			(item_get_type, ":item_type", ":item_no"),
			(this_or_next|eq, ":item_type", itp_type_one_handed_wpn),
            (this_or_next|eq, ":item_type", itp_type_two_handed_wpn),
            (this_or_next|eq, ":item_type", itp_type_polearm),
            (this_or_next|eq, ":item_type", itp_type_shield),
            (this_or_next|eq, ":item_type", itp_type_arrows),
            (this_or_next|eq, ":item_type", itp_type_bolts),
            (this_or_next|eq, ":item_type", itp_type_bow),
            (this_or_next|eq, ":item_type", itp_type_crossbow),
            (this_or_next|eq, ":item_type", itp_type_thrown),
            (this_or_next|eq, ":item_type", itp_type_pistol),
            (this_or_next|eq, ":item_type", itp_type_musket),
            (eq, ":item_type", itp_type_bullets),
			(lt, ":slot_no", 8),
			### ITEM PASSES AND SHOULD BE SHOWN ###
			(call_script, "script_gpu_create_mesh", "mesh_inv_slot", ":pos_x", ":pos_y", 800, 800),
			(call_script, "script_gpu_create_mesh", "mesh_mp_inventory_choose", ":pos_x", ":pos_y", 640, 640),
			(troop_set_slot, "trp_temp_array_a", ":slot_no", reg1),
			(troop_set_slot, "trp_temp_array_b", ":slot_no", -1),
			(troop_set_slot, "trp_temp_array_c", ":slot_no", -1),
			(ge, ":item_no", 1), # Valid Item
			(store_add, ":pos_x_item", ":pos_x", 40),
			(store_add, ":pos_y_item", ":pos_y", 40),
			(call_script, "script_gpu_create_item_mesh", ":item_no", ":pos_x_item", ":pos_y_item", 800),
			(troop_set_slot, "trp_temp_array_b", ":slot_no", reg1),
			(troop_set_slot, "trp_temp_array_c", ":slot_no", ":inv_slot"), # ":item_no"),
            (val_add, ":slot_no", 1),
			(try_begin),
				(val_add, ":pos_x", ":box_size"),
				(ge, ":pos_x", ":limit_x"),
				(assign, ":pos_x", ":left_margin"),
				(val_sub, ":pos_y", ":box_size"),
			(try_end),
		(try_end),
		
		# Finish out the inventory box.
		(try_for_range, ":empty_slot", ":slot_no", 24),
			(call_script, "script_gpu_create_mesh", "mesh_inv_slot", ":pos_x", ":pos_y", 800, 800),
			(call_script, "script_gpu_create_mesh", "mesh_mp_inventory_choose", ":pos_x", ":pos_y", 640, 640),
			(troop_set_slot, "trp_temp_array_a", ":empty_slot", -1),
			(troop_set_slot, "trp_temp_array_b", ":empty_slot", -1),
			(troop_set_slot, "trp_temp_array_c", ":empty_slot", -1),
			(try_begin),
				(val_add, ":pos_x", ":box_size"),
				(ge, ":pos_x", ":limit_x"),
				(assign, ":pos_x", ":left_margin"),
				(val_sub, ":pos_y", ":box_size"),
			(try_end),
		(try_end),
		
		### DISPLAY BATTLEFIELD & SIEGE EQUIPMENT SLOTS ###
		(assign, ":left_margin", 635),
		(assign, ":pos_x", ":left_margin"),
		(assign, ":pos_y", 515),
		(try_for_range, ":pick_slot", 0, 8),
			(store_add, ":troop_slot", ":pick_slot", dws_val_battlefield_set_1),
			(store_add, ":storage_slot", ":pick_slot", 50),
			(troop_get_slot, ":item_no", DWS_OBJECTS, ":troop_slot"),
			(call_script, "script_gpu_create_mesh", "mesh_inv_slot", ":pos_x", ":pos_y", 800, 800),
			(call_script, "script_gpu_create_mesh", "mesh_mp_inventory_choose", ":pos_x", ":pos_y", 640, 640),
			(troop_set_slot, "trp_temp_array_a", ":storage_slot", reg1),
			(troop_set_slot, "trp_temp_array_b", ":storage_slot", -1),
			(troop_set_slot, "trp_temp_array_c", ":storage_slot", -1),
			# script_gpu_create_item_mesh    - item_id, pos_x, pos_y, size
			(store_add, ":pos_x_item", ":pos_x", 40),
			(store_add, ":pos_y_item", ":pos_y", 40),
			(try_begin),
				(val_add, ":pos_x", ":box_size"),
				(eq, ":pick_slot", 3),
				(assign, ":pos_x", ":left_margin"),
				(val_sub, ":pos_y", 150),
			(try_end),
			
			(ge, ":item_no", 1), # Valid Item
			(call_script, "script_gpu_create_item_mesh", ":item_no", ":pos_x_item", ":pos_y_item", 800),
			(troop_set_slot, "trp_temp_array_b", ":storage_slot", reg1),
			(troop_set_slot, "trp_temp_array_c", ":storage_slot", ":item_no"),
          
		(try_end),
		
		# Create Selected Item Spot
		(assign, ":pos_x", 755),
		(assign, ":pos_y", 215),
		(call_script, "script_gpu_create_mesh", "mesh_inv_slot", ":pos_x", ":pos_y", 800, 800),
		(call_script, "script_gpu_create_mesh", "mesh_mp_inventory_choose", ":pos_x", ":pos_y", 640, 640),
		(try_begin),
			(troop_get_slot, ":item_no", DWS_OBJECTS, dws_val_selected_item),
			(ge, ":item_no", 1),
			(store_add, ":pos_x_item", ":pos_x", 40),
			(store_add, ":pos_y_item", ":pos_y", 40),
			(call_script, "script_gpu_create_item_mesh", ":item_no", ":pos_x_item", ":pos_y_item", 800),
		(try_end),
		
		### CHECKBOX OPTIONS ###
		# Enable Checkbox #
		(troop_get_slot, ":setting", "$dws_troop", slot_troop_dws_enabled),
		(troop_set_slot, DWS_OBJECTS, dws_val_checkbox_enable, ":setting"),
		(call_script, "script_gpu_create_checkbox", 45, 380, "str_dws_checkbox_enable", dws_obj_checkbox_enable, dws_val_checkbox_enable),
		
		# All or Nothing Checkbox #
		(troop_get_slot, ":setting", "$dws_troop", slot_troop_dws_all_or_nothing),
		(troop_set_slot, DWS_OBJECTS, dws_val_checkbox_all_or_nothing, ":setting"),
		(call_script, "script_gpu_create_checkbox", 45, 350, "str_dws_checkbox_all_or_nothing", dws_obj_checkbox_all_or_nothing, dws_val_checkbox_all_or_nothing),
		
		# Report Activity Checkbox #
		(troop_set_slot, DWS_OBJECTS, dws_val_checkbox_report, "$dws_report_activity"),
		(call_script, "script_gpu_create_checkbox", 45, 320, "str_dws_checkbox_report", dws_obj_checkbox_report, dws_val_checkbox_report),
		
		(presentation_set_duration, 999999),
    ]),
	
	(ti_on_presentation_mouse_enter_leave,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":enter_leave"),
			
			(try_begin),
				(eq, ":enter_leave", 0),
				(try_for_range, ":slot_no", 0, 58),
					(troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
					
					(try_begin),
						(ge, ":slot_no", 50),
						(troop_get_slot, ":item_no", "trp_temp_array_c", ":slot_no"),
						(troop_get_slot, ":target_obj", "trp_temp_array_b", ":slot_no"),
						(ge, ":item_no", 1),
						(overlay_get_position, pos0, ":target_obj"),
						(show_item_details, ":item_no", pos0, 100),
					(else_try),
						(lt, ":slot_no", 50),
						(troop_get_slot, ":inv_slot", "trp_temp_array_c", ":slot_no"),
						(troop_get_inventory_slot, ":item_no", "$dws_troop", ":inv_slot"),
						(troop_get_inventory_slot_modifier, ":imod", "$dws_troop", ":inv_slot"),
						(troop_get_slot, ":target_obj", "trp_temp_array_b", ":slot_no"),
						(ge, ":item_no", 1),
						(overlay_get_position, pos0, ":target_obj"),
						(show_item_details_with_modifier, ":item_no", ":imod", pos0, 100),
					(try_end),
					(ge, ":item_no", 1),
					(assign, "$g_current_opened_item_details", ":slot_no"),
				(try_end),
			(else_try),
				(try_for_range, ":slot_no", 0, 58),
					(troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
					(try_begin),
						(eq, "$g_current_opened_item_details", ":slot_no"),
						(close_item_details),
					(try_end),
				(try_end),
			(try_end),
		]),
	
    (ti_on_presentation_mouse_press,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":mouse_button"),
			
			(try_begin),
				##################################
				##### INVENTORY ITEM CLICKED #####
				##################################
				## Locate the item that was clicked
				(eq, ":mouse_button", 0), # Left Button
				(assign, ":found", 0),
				(try_for_range, ":temp_slot", 0, 24),
					(eq, ":found", 0),
					#(this_or_next|troop_slot_eq, "trp_temp_array_a", ":temp_slot", ":object"),
					(troop_slot_eq, "trp_temp_array_a", ":temp_slot", ":object"),
					(troop_get_slot, ":inv_slot", "trp_temp_array_c", ":temp_slot"),
					(troop_get_inventory_slot, ":item_no", "$dws_troop", ":inv_slot"),
					(ge, ":item_no", 1),
					(assign, ":found", 1),
					#(troop_get_slot, ":item_no", "trp_temp_array_c", ":temp_slot"),
				(try_end),
				(eq, ":found", 1),
				
				# (str_store_item_name, s21, ":item_no"),
				# (display_message, "@You picked item {s21}."),
				(troop_set_slot, DWS_OBJECTS, dws_val_selected_item, ":item_no"),
				(start_presentation, "prsnt_dws_settings"),
				
			(else_try),
				######################################
				##### EQUIPMENT SET SLOT CLICKED #####
				######################################
				(eq, ":mouse_button", 0), # Left Button adds the item.
				(assign, ":found", 0),
				(try_for_range, ":temp_slot", 50, 58),
					(eq, ":found", 0),
					(troop_slot_eq, "trp_temp_array_a", ":temp_slot", ":object"),
					(troop_get_slot, ":item_no", DWS_OBJECTS, dws_val_selected_item),
					(ge, ":item_no", 1),
					(assign, ":found", ":temp_slot"),
				(try_end),
				(ge, ":found", 1),
				
				## Figure out how many the troop has of this item.
				(troop_get_inventory_capacity, ":capacity", "$dws_troop"),
				(assign, ":count_available", 0),
				(try_for_range, ":inv_slot", 0, ":capacity"),
					(troop_get_inventory_slot, ":item_check", "$dws_troop", ":inv_slot"),
					(eq, ":item_check", ":item_no"),
					(val_add, ":count_available", 1),
				(try_end),
				
				## Determine how many of the item the troop is trying to gear in a given set.
				(store_sub, ":pick_slot", ":found", 50),
				(store_add, ":troop_slot", ":pick_slot", dws_val_battlefield_set_1),
				(assign, ":count_already_have", 0),
				(try_begin),
					# Battlefield Set
					(is_between, ":troop_slot", dws_val_battlefield_set_1, dws_val_siege_set_1),
					(try_for_range, ":slot_no", dws_val_battlefield_set_1, dws_val_siege_set_1),
						(troop_slot_eq, DWS_OBJECTS, ":slot_no", ":item_no"),
						(neq, ":slot_no", ":troop_slot"), # Don't count the item if it is the same spot being replaced.
						(val_add, ":count_already_have", 1),
					(try_end),
				(else_try),
					# Siege Set
					(is_between, ":troop_slot", dws_val_siege_set_1, dws_end_of_sets),
					(try_for_range, ":slot_no", dws_val_siege_set_1, dws_end_of_sets),
						(troop_slot_eq, DWS_OBJECTS, ":slot_no", ":item_no"),
						(neq, ":slot_no", ":troop_slot"), # Don't count the item if it is the same spot being replaced.
						(val_add, ":count_already_have", 1),
					(try_end),
				(try_end),
				(try_begin),
					(gt, ":count_available", ":count_already_have"),
					(troop_set_slot, DWS_OBJECTS, ":troop_slot", ":item_no"),
					(troop_set_slot, DWS_OBJECTS, dws_val_selected_item, -1),
					(start_presentation, "prsnt_dws_settings"),
				(else_try),
					(str_store_item_name, s21, ":item_no"),
					(display_message, "@This set already contains {s21} and you don't have enough extras to add another."),
				(try_end),
				
			(else_try),
				######################################
				##### EQUIPMENT SET SLOT CLICKED #####
				######################################
				(eq, ":mouse_button", 1), # Right Button clears the item.
				(assign, ":found", 0),
				(try_for_range, ":temp_slot", 50, 58),
					(eq, ":found", 0),
					(troop_slot_eq, "trp_temp_array_a", ":temp_slot", ":object"),
					(assign, ":found", ":temp_slot"),
				(try_end),
				(ge, ":found", 1),
				(store_sub, ":pick_slot", ":found", 50),
				(store_add, ":troop_slot", ":pick_slot", dws_val_battlefield_set_1),
				(troop_set_slot, DWS_OBJECTS, ":troop_slot", -1),
				(start_presentation, "prsnt_dws_settings"),
			(try_end),
		]),
	
	(ti_on_presentation_event_state_change,
    [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(try_begin),
			##### ACCEPT CHANGES BUTTON #####
			(troop_slot_eq, DWS_OBJECTS, dws_obj_button_accept, ":object"),
			# Copy troop set information to actual troop slots.
			(try_for_range, ":old_slot", dws_val_battlefield_set_1, dws_end_of_sets), 
				(store_sub, ":offset", ":old_slot", dws_val_battlefield_set_1),
				(store_add, ":new_slot", ":offset", slot_troop_battlefield_set_1),
				(troop_get_slot, ":item_no", DWS_OBJECTS, ":old_slot"),
				(troop_set_slot, "$dws_troop", ":new_slot", ":item_no"),
			(try_end),
			(str_store_troop_name, s21, "$dws_troop"),
			(display_message, "@Equipment set configuration for {s21} accepted."),
			
		(else_try),
			##### EXIT BUTTON #####
			(troop_slot_eq, DWS_OBJECTS, dws_obj_button_cancel, ":object"),
			(presentation_set_duration, 0),
			
		(else_try), 
			####### CHARACTER SELECTOR #######
			(troop_slot_eq, DWS_OBJECTS, dws_obj_menu_selected_character, ":object"),
			(troop_set_slot, DWS_OBJECTS, dws_val_menu_selected_character, ":value"),
			(store_add, ":troop_pick", dws_val_menu_troop_1, ":value"),
			(troop_get_slot, "$dws_troop", DWS_OBJECTS, ":troop_pick"),
			# Prevent carrying items from one character to the next.
			(troop_set_slot, DWS_OBJECTS, dws_val_selected_item, -1),
			# Initialize troop set information.
			(try_for_range, ":old_slot", slot_troop_battlefield_set_1, slot_troop_dws_enabled),
				(store_sub, ":offset", ":old_slot", slot_troop_battlefield_set_1),
				(store_add, ":new_slot", ":offset", dws_val_battlefield_set_1),
				(troop_get_slot, ":item_no", "$dws_troop", ":old_slot"),
				(troop_set_slot, DWS_OBJECTS, ":new_slot", ":item_no"),
			(try_end),
			(start_presentation, "prsnt_dws_settings"),
			
		(else_try), 
			####### SHOW OBJECT LIST #######
			(troop_slot_eq, DWS_OBJECTS, dws_obj_test, ":object"),
			(try_for_range, ":slot", 0, 58),
				(assign, reg20, ":slot"),
				(troop_get_slot, reg21, "trp_temp_array_a", ":slot"),
				(troop_get_slot, reg22, "trp_temp_array_b", ":slot"),
				(troop_get_slot, reg23, "trp_temp_array_c", ":slot"),
				(ge, reg21, 1),
				(display_message, "@[#{reg20}]: {reg21}, {reg22}, [Item: {reg23}]"),
			(try_end),
			
		(else_try),
			##### ENABLE DWS CHECKBOX #####
			(troop_slot_eq, DWS_OBJECTS, dws_obj_checkbox_enable, ":object"),
			(troop_set_slot, DWS_OBJECTS, dws_val_checkbox_enable, ":value"),
			(troop_set_slot, "$dws_troop", slot_troop_dws_enabled, ":value"),
			(ge, DEBUG_DWS, 1),
			(assign, reg31, ":value"),
			(display_message, "@DEBUG (DWS): Dynamic switching set to {reg31}. [{reg31?Enabled:Disabled}]"),
			
		(else_try),
			##### ENFORCE ALL OR NOTHING CHECKBOX #####
			(troop_slot_eq, DWS_OBJECTS, dws_obj_checkbox_all_or_nothing, ":object"),
			(troop_set_slot, DWS_OBJECTS, dws_val_checkbox_all_or_nothing, ":value"),
			(troop_set_slot, "$dws_troop", slot_troop_dws_all_or_nothing, ":value"),
			(ge, DEBUG_DWS, 1),
			(assign, reg31, ":value"),
			(display_message, "@DEBUG (DWS): 'All or Nothing' enforcement set to {reg31}. [{reg31?Enabled:Disabled}]"),
			
		(else_try),
			##### REPORT ACTIVITY CHECKBOX #####
			(troop_slot_eq, DWS_OBJECTS, dws_obj_checkbox_report, ":object"),
			(troop_set_slot, DWS_OBJECTS, dws_val_checkbox_report, ":value"),
			(assign, "$dws_report_activity", ":value"),
			(ge, DEBUG_DWS, 1),
			(assign, reg31, ":value"),
			(display_message, "@DEBUG (DWS): DWS Activity reporting to {reg31}. [{reg31?Enabled:Disabled}]"),
			
		
		(try_end),
		
	]),
  ]),
  
###########################################################################################################################
#####                                               AUTOLOOT SYSTEM                                                   #####
###########################################################################################################################
# This preference panel will set what kinds of equipment the player wishes allowed in each city's specific tournaments.
  ("als_settings", 0, mesh_load_window, [
    (ti_on_presentation_load,
    [
		(set_fixed_point_multiplier, 1000),
		
		(assign, "$gpu_storage", ALS_OBJECTS),
		(assign, "$gpu_data",    ALS_OBJECTS),
		
		# Button Definitions
		(call_script, "script_gpu_create_game_button", "str_cms_accept", 885, 30, als_obj_button_accept),
		(call_script, "script_gpu_create_game_button", "str_cms_cancel", 695, 30, als_obj_button_cancel),
		(try_begin),
			(eq, "$autoloot_mode", ALS_MODE_PLAYER_SEARCH),
			(call_script, "script_gpu_create_game_button", "str_als_label_search", 505, 30, als_obj_inventory_search),
		(try_end),
		(call_script, "script_gpu_create_game_button", "str_als_label_copy", 315, 30, als_obj_copy_settings_to_all),
		#(call_script, "script_gpu_create_game_button", "str_als_label_actual_gear", 125, 30, als_obj_equipment_page),
		
		# (call_script, "script_gpu_draw_line", 950, 2, 25, 655, gpu_gray), # horizontal line underneath title.
		# (call_script, "script_gpu_draw_line", 950, 2, 25, 655, gpu_gray), # horizontal line underneath title.
		
		# (call_script, "script_gpu_draw_line", 852, 40, 73, 650, gpu_brown), # Brown background
		# (call_script, "script_gpu_draw_line", 852, 2, 73, 690, gpu_black), # - Header
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		# (call_script, "script_gpu_draw_line", 2, 40, 73, 650, gpu_black), # | Left border
		# (call_script, "script_gpu_draw_line", 2, 40, 923, 650, gpu_black), # | Right border
		
		# Text Labels
		(str_store_troop_name, s21, "$als_troop"),
		(call_script, "script_gpu_create_text_label", "str_als_main_title", 500, 665, als_obj_label_main_title, gpu_center),
		(call_script, "script_gpu_resize_object", als_obj_label_main_title, 150),
		(call_script, "script_gpu_create_text_label", "str_als_main_title", 500, 665, als_obj_label_main_title, gpu_center),
		# (call_script, "script_gpu_create_text_label", "str_als_main_title", 500, 665, als_obj_label_main_title, gpu_center_with_outline),
		# (overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", als_obj_label_main_title, 150),
		#(call_script, "script_gpu_create_text_label", "str_dws_inventory_title", 455, 620, 0, gpu_center),
		
		# Create Character Portrait
		(call_script, "script_gpu_create_portrait", "$als_troop", 70, 465, 500, als_obj_portrait_selected_troop),
		
		# CHARACTER MENU BEGIN
		(position_set_x, pos1, 190),
        (position_set_y, pos1, 425),
		
		(troop_get_slot, ":selected_profile", ALS_OBJECTS, als_val_menu_selected_character),
		(create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
		(troop_set_slot, ALS_OBJECTS, als_obj_menu_selected_character, reg1),
		(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
		(assign, ":hero_slot", 0),
        (try_for_range, ":stack_num", 0, ":num_stacks"),
			(store_add, ":slot_pick", als_val_menu_troop_1, ":hero_slot"),
			(party_stack_get_troop_id,":troop_no","p_main_party",":stack_num"),
			(troop_is_hero, ":troop_no"),
			(neq, ":troop_no", "trp_player"),
			(is_between, ":troop_no", companions_begin, companions_end),
			(str_clear, s1),
			(str_store_troop_name, s1, ":troop_no"),
			(troop_set_slot, ALS_OBJECTS, ":slot_pick", ":troop_no"),
			(try_begin),
				(ge, DEBUG_ALS, 2),
				(assign, reg31, ":slot_pick"),
				(display_message, "@DEBUG (ALS): Added '{s1}' to character chooser menu.  Slot #{reg31}"),
			(try_end),
			(val_add, ":hero_slot", 1),
			(overlay_add_item, reg1, "@{s1}"),
        (try_end),
		(overlay_set_val, reg1, ":selected_profile"),
		(call_script, "script_gpu_resize_object", als_obj_menu_selected_character, 75),
		# CHARACTER MENU END
		
		# Character skills & attributes used as prerequisites
		(assign, ":margin_left", 40),
		(assign, ":margin_center_left", 160),
		(assign, ":margin_center_right", 195),
		(assign, ":margin_right", 315),
		(assign, ":font_size", 75),
		(assign, ":pos_y", 260),
		(assign, ":pos_y_step", 25),
		(store_add, ":margin_center", ":margin_left", ":margin_right"),
		(val_div, ":margin_center", 2),
		(call_script, "script_gpu_create_text_label", "str_als_label_abilities", ":margin_center", ":pos_y", 0, gpu_center),
		(call_script, "script_gpu_create_text_label", "str_als_label_abilities", ":margin_center", ":pos_y", 0, gpu_center),
		# (call_script, "script_gpu_create_text_label", "str_als_label_abilities", ":margin_center", ":pos_y", 0, gpu_center_with_outline),
		# (overlay_set_color, reg1, gpu_white),
		(val_sub, ":pos_y", 15),
		(store_sub, ":length", ":margin_right", ":margin_left"),
		(val_add, ":length", 3),
		(call_script, "script_gpu_draw_line", ":length", 2, ":margin_left", ":pos_y", gpu_black),
		(val_sub, ":pos_y", 20),
		## STRENGTH ##
		(call_script, "script_gpu_create_text_label", "str_als_label_strength", ":margin_left", ":pos_y", als_obj_label_strength, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_strength, ":font_size"),
		(store_attribute_level, reg21, "$als_troop", ca_strength),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_center_left", ":pos_y", als_obj_label_strength, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_strength, ":font_size"),
		## ONE HANDED PROFICIENCY ##
		(call_script, "script_gpu_create_text_label", "str_als_label_onehand", ":margin_center_right", ":pos_y", als_obj_label_onehand, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_onehand, ":font_size"),
		(store_proficiency_level, reg21, "$als_troop", wpt_one_handed_weapon),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_right", ":pos_y", als_obj_label_onehand, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_onehand, ":font_size"),
		##
		(val_sub, ":pos_y", ":pos_y_step"),
		## POWER DRAW ##
		(call_script, "script_gpu_create_text_label", "str_als_label_powerdraw", ":margin_left", ":pos_y", als_obj_label_powerdraw, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_powerdraw, ":font_size"),
		(store_skill_level, reg21, "skl_power_draw", "$als_troop"),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_center_left", ":pos_y", als_obj_label_powerdraw, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_powerdraw, ":font_size"),
		## TWO HANDED PROFICIENCY ##
		(call_script, "script_gpu_create_text_label", "str_als_label_twohand", ":margin_center_right", ":pos_y", als_obj_label_twohand, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_twohand, ":font_size"),
		(store_proficiency_level, reg21, "$als_troop", wpt_two_handed_weapon),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_right", ":pos_y", als_obj_label_twohand, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_twohand, ":font_size"),
		##
		(val_sub, ":pos_y", ":pos_y_step"),
		## POWER THROW ##
		(call_script, "script_gpu_create_text_label", "str_als_label_powerthrow", ":margin_left", ":pos_y", als_obj_label_powerthrow, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_powerthrow, ":font_size"),
		(store_skill_level, reg21, "skl_power_throw", "$als_troop"),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_center_left", ":pos_y", als_obj_label_powerthrow, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_powerthrow, ":font_size"),
		## POLEARM PROFICIENCY ##
		(call_script, "script_gpu_create_text_label", "str_als_label_polearm", ":margin_center_right", ":pos_y", als_obj_label_polearm, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_polearm, ":font_size"),
		(store_proficiency_level, reg21, "$als_troop", wpt_polearm),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_right", ":pos_y", als_obj_label_polearm, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_polearm, ":font_size"),
		##
		(val_sub, ":pos_y", ":pos_y_step"),
		## SHIELD ##
		(call_script, "script_gpu_create_text_label", "str_als_label_shield", ":margin_left", ":pos_y", als_obj_label_shield, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_shield, ":font_size"),
		(store_skill_level, reg21, "skl_shield", "$als_troop"),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_center_left", ":pos_y", als_obj_label_shield, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_shield, ":font_size"),
		## ARCHERY PROFICIENCY ##
		(call_script, "script_gpu_create_text_label", "str_als_label_archery", ":margin_center_right", ":pos_y", als_obj_label_archery, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_archery, ":font_size"),
		(store_proficiency_level, reg21, "$als_troop", wpt_archery),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_right", ":pos_y", als_obj_label_archery, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_archery, ":font_size"),
		##
		(val_sub, ":pos_y", ":pos_y_step"),
		## RIDING ##
		(call_script, "script_gpu_create_text_label", "str_als_label_riding", ":margin_left", ":pos_y", als_obj_label_riding, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_riding, ":font_size"),
		(store_skill_level, reg21, "skl_riding", "$als_troop"),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_center_left", ":pos_y", als_obj_label_riding, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_riding, ":font_size"),
		## CROSSBOW PROFICIENCY ##
		(call_script, "script_gpu_create_text_label", "str_als_label_crossbow", ":margin_center_right", ":pos_y", als_obj_label_crossbow, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_crossbow, ":font_size"),
		(store_proficiency_level, reg21, "$als_troop", wpt_crossbow),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_right", ":pos_y", als_obj_label_crossbow, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_crossbow, ":font_size"),
		##
		(val_sub, ":pos_y", ":pos_y_step"),
		## HORSE ARCHERY ##
		(call_script, "script_gpu_create_text_label", "str_als_label_horsearchery", ":margin_left", ":pos_y", als_obj_label_horsearchery, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_horsearchery, ":font_size"),
		(store_skill_level, reg21, "skl_horse_archery", "$als_troop"),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_center_left", ":pos_y", als_obj_label_horsearchery, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_horsearchery, ":font_size"),
		## THROWING PROFICIENCY ##
		(call_script, "script_gpu_create_text_label", "str_als_label_thrown", ":margin_center_right", ":pos_y", als_obj_label_thrown, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_thrown, ":font_size"),
		(store_proficiency_level, reg21, "$als_troop", wpt_throwing),
		(set_fixed_point_multiplier, 1000), # Necessary as encumbrance shifts this value to 100.
		(call_script, "script_gpu_create_text_label", "str_als_label_r21", ":margin_right", ":pos_y", als_obj_label_thrown, gpu_right),
		(call_script, "script_gpu_resize_object", als_obj_label_thrown, ":font_size"),
		##
		
		### DISPLAY EQUIPMENT SLOTS ###
		(assign, ":left_margin", 350),
		(assign, ":upper_margin", 515),
		(assign, ":pos_x", ":left_margin"),
		(assign, ":pos_y", ":upper_margin"),
		(assign, ":box_size", 80),
		(try_for_range, ":pick_slot", 0, 9),
			(store_add, ":troop_slot", ":pick_slot", als_val_slot_0),
			(store_add, ":storage_slot", ":pick_slot", 0),
			(troop_get_slot, ":item_no", ALS_OBJECTS, ":troop_slot"),
			# Create inventory box for the item.
			(call_script, "script_gpu_create_mesh", "mesh_inv_slot", ":pos_x", ":pos_y", 800, 800),
			# (call_script, "script_gpu_create_mesh", "mesh_mp_inventory_choose", ":pos_x", ":pos_y", 640, 640),
			(troop_set_slot, "trp_temp_array_a", ":storage_slot", reg1),
			(troop_set_slot, "trp_temp_array_b", ":storage_slot", -1),
			(troop_set_slot, "trp_temp_array_c", ":storage_slot", -1),
			# script_gpu_create_item_mesh    - item_id, pos_x, pos_y, size
			
			# Create text label for the inventory slot.
			(try_begin),
				(lt, ":pick_slot", 4),
				(store_add, ":pos_x_item", ":pos_x", 95),
				(store_add, ":pos_y_item", ":pos_y", 70),
			(else_try),
				(store_add, ":pos_x_item", ":pos_x", 95),
				(store_add, ":pos_y_item", ":pos_y", 60),
			(try_end),
			(store_add, ":string_slot", ":pick_slot", "str_als_label_slot_1"),
			(call_script, "script_gpu_create_text_label", ":string_slot", ":pos_x_item", ":pos_y_item", 0, gpu_left),
			
			# Create image of the item itself.
			(store_add, ":pos_x_item", ":pos_x", 40),
			(store_add, ":pos_y_item", ":pos_y", 40),
			(try_begin),
				(ge, ":item_no", 1), # Valid Item
				(call_script, "script_gpu_create_item_mesh", ":item_no", ":pos_x_item", ":pos_y_item", 800),
				(troop_set_slot, "trp_temp_array_b", ":storage_slot", reg1),
				(troop_set_slot, "trp_temp_array_c", ":storage_slot", ":item_no"),
			(try_end),
			
			# Create upgrade menu.
			(try_begin),
				(lt, ":pick_slot", 4),
				(store_add, ":pos_x_item", ":pos_x", 215),  (position_set_x, pos1, ":pos_x_item"),
				(store_add, ":pos_y_item", ":pos_y",  30),  (position_set_y, pos1, ":pos_y_item"),
			(else_try),
				(store_add, ":pos_x_item", ":pos_x", 215),  (position_set_x, pos1, ":pos_x_item"),
				(store_add, ":pos_y_item", ":pos_y",  15),  (position_set_y, pos1, ":pos_y_item"),
			(try_end),
			(store_add, ":value_slot", ":pick_slot", als_val_menu_slot_0),
			(store_add, ":menu_slot", ":pick_slot", als_obj_menu_slot_0),
			(troop_get_slot, ":choice", ALS_OBJECTS, ":value_slot"),
			(create_combo_button_overlay, reg1),
			(overlay_set_position, reg1, pos1),
			(troop_set_slot, ALS_OBJECTS, ":menu_slot", reg1),
			(try_begin),
				### WEAPON MENUS ### - More complex because weapon types are added.
				(lt, ":pick_slot", 4),
				(overlay_add_item, reg1, "@Keep Current"),
				(overlay_add_item, reg1, "@Shield (mounted)"),
				(overlay_add_item, reg1, "@Shield (infantry)"),
				(overlay_add_item, reg1, "@One Handed Weapon"),
				(overlay_add_item, reg1, "@Two Handed Weapon"),
				(overlay_add_item, reg1, "@Polearm"),
				(overlay_add_item, reg1, "@Polearm (Lance)"),
				(overlay_add_item, reg1, "@Arrows"),
				(overlay_add_item, reg1, "@Bow (mounted)"),
				(overlay_add_item, reg1, "@Bow (infantry)"),
				(overlay_add_item, reg1, "@Crossbow Bolts"),
				(overlay_add_item, reg1, "@Crossbow (mounted)"),
				(overlay_add_item, reg1, "@Crossbow (infantry)"),
				(overlay_add_item, reg1, "@Thrown Weapon"),
			(else_try),
				### MOUNT MENU ### - Slightly more complex.
				(eq, ":pick_slot", 8),
				(overlay_add_item, reg1, "@Keep Current"),
				(overlay_add_item, reg1, "@Find Fastest Mount"),
				(overlay_add_item, reg1, "@Find Most Resilient Mount"),
				(overlay_add_item, reg1, "@Find Best Overall Mount"),
			(else_try),
				### SIMPLE MENUS ### - Simple Keep Current / Find Upgrade options
				(overlay_add_item, reg1, "@Keep Current"),
				(overlay_add_item, reg1, "@Find Upgrade"),
			(try_end),
			(overlay_set_val, reg1, ":choice"),
			(call_script, "script_gpu_resize_object", ":menu_slot", 75),
			
			# Create upgrade menu.
			(try_begin),
				(lt, ":pick_slot", 4),
				(store_add, ":pos_x_item", ":pos_x", 215),  (position_set_x, pos1, ":pos_x_item"),
				(store_add, ":pos_y_item", ":pos_y",  0),  (position_set_y, pos1, ":pos_y_item"),
				(store_add, ":value_slot", ":pick_slot", als_val_menu_weapon_type_0),
				(store_add, ":menu_slot", ":pick_slot", als_obj_menu_weapon_type_0),
				(troop_get_slot, ":choice", ALS_OBJECTS, ":value_slot"),
				(create_combo_button_overlay, reg1),
				(overlay_set_position, reg1, pos1),
				(troop_set_slot, ALS_OBJECTS, ":menu_slot", reg1),
				(overlay_add_item, reg1, "@Any Damage Type"),
				(overlay_add_item, reg1, "@Cutting Damage"),
				(overlay_add_item, reg1, "@Piercing Damage"),
				(overlay_add_item, reg1, "@Blunt Damage"),
				(overlay_set_val, reg1, ":choice"),
				(call_script, "script_gpu_resize_object", ":menu_slot", 75),
			(try_end),
			
			# Shift to the next box.
			(assign, ":horizontal shift", 305),
			(store_add, ":vertical_shift", ":box_size", 25),
			(try_begin),
				(val_sub, ":pos_y", ":vertical_shift"),
				(try_begin),
					(eq, ":pick_slot", 1),
					(assign, ":pos_y", ":upper_margin"),
					(val_add, ":pos_x", ":horizontal shift"),
				(else_try),
					(eq, ":pick_slot", 3),
					(assign, ":pos_x", ":left_margin"),
				(else_try),
					(eq, ":pick_slot", 5),
					(val_add, ":pos_x", ":horizontal shift"),
					(val_add, ":pos_y", ":vertical_shift"),
					(val_add, ":pos_y", ":vertical_shift"),
				(try_end),
				# (try_begin),
					# (eq, ":pick_slot", 3),
					# (assign, ":pos_y", ":upper_margin"),
					# (val_add, ":pos_x", 305),
				# (else_try),
					# (eq, ":pick_slot", 8),
					# (assign, ":pos_x", ":left_margin"),
				# (try_end),
			(try_end),
			
		(try_end),
		
		### CHECKBOX OPTIONS ###
		# "Enable Autolooting" Checkbox #
		(troop_get_slot, ":setting", "$als_troop", slot_troop_enable_autolooting),
		(troop_set_slot, ALS_OBJECTS, als_val_checkbox_enable, ":setting"),
		(call_script, "script_gpu_create_checkbox", 45, 380, "str_als_checkbox_enable", als_obj_checkbox_enable, als_val_checkbox_enable),
		
		# "Do not break weapon sets" Checkbox #
		(troop_get_slot, ":setting", "$als_troop", slot_troop_prevent_breaking_sets),
		(troop_set_slot, ALS_OBJECTS, als_val_checkbox_no_break_sets, ":setting"),
		(call_script, "script_gpu_create_checkbox", 45, 350, "str_als_checkbox_breaking_sets", als_obj_checkbox_no_break_sets, als_val_checkbox_no_break_sets),
		
		# "Use only heraldic armor & shields" Checkbox #
		(troop_get_slot, ":setting", "$als_troop", slot_troop_retain_heraldic_items),
		(troop_set_slot, ALS_OBJECTS, als_val_checkbox_heraldic_items, ":setting"),
		(call_script, "script_gpu_create_checkbox", 45, 320, "str_als_checkbox_heralic", als_obj_checkbox_heraldic_items, als_val_checkbox_heraldic_items),
		
		### WEIGHT LIMIT MENU ###
		(call_script, "script_gpu_create_text_label", "str_als_label_weight_limit", 40, 302, als_obj_label_weight_limit, gpu_left),
		(call_script, "script_gpu_resize_object", als_obj_label_weight_limit, 75),
		(position_set_x, pos1, 260),
		(position_set_y, pos1, 287),
		(troop_get_slot, ":choice", ALS_OBJECTS, als_val_menu_weight_limit),
		(create_combo_button_overlay, reg1),
		(overlay_set_position, reg1, pos1),
		(troop_set_slot, ALS_OBJECTS, als_obj_menu_weight_limit, reg1),
		(overlay_add_item, reg1, "@No Armor Restriction"),
		(overlay_add_item, reg1, "@Light Armor"),
		(overlay_add_item, reg1, "@Medium Armor"),
		(overlay_set_val, reg1, ":choice"),
		(call_script, "script_gpu_resize_object", als_obj_menu_weight_limit, 75),
		
		(presentation_set_duration, 999999),
    ]),
	
	(ti_on_presentation_mouse_enter_leave,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":enter_leave"),
			
			(try_begin),
				(ge, DEBUG_ALS, 1),
				(show_object_details_overlay, 1),
			(try_end),
			
			(try_begin),
				(eq, ":enter_leave", 0),
				(try_for_range, ":slot_no", 0, 9),
					(troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
					(troop_get_slot, ":item_no", "trp_temp_array_c", ":slot_no"),
					(troop_get_slot, ":target_obj", "trp_temp_array_b", ":slot_no"),
					(ge, ":item_no", 1),
					(troop_get_inventory_slot_modifier, ":imod", "$als_troop", ":slot_no"),
					(overlay_get_position, pos0, ":target_obj"),
					#(show_item_details, ":item_no", pos0, 100),
					(show_item_details_with_modifier, ":item_no", ":imod", pos0, 100),
					(assign, "$g_current_opened_item_details", ":slot_no"),
					# (call_script, "script_als_get_item_rating", "$als_troop", ":item_no", 0),
					# (call_script, "script_als_troop_can_use_item", "$als_troop", ":item_no", 0, ":slot_no"), 
				(try_end),
			(else_try),
				(try_for_range, ":slot_no", 0, 9),
					(troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
					(try_begin),
						(eq, "$g_current_opened_item_details", ":slot_no"),
						(close_item_details),
					(try_end),
				(try_end),
			(try_end),
		]),
	
	(ti_on_presentation_event_state_change,
    [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(try_begin),
			##### ACCEPT CHANGES BUTTON #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_button_accept, ":object"),
			(call_script, "script_als_save_troop_settings", "$als_troop"),
			
		(else_try),
			##### EXIT BUTTON #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_button_cancel, ":object"),
			# Clean out ALS_OBJECTS
			(try_for_range, ":slot", 0, 300),
				(troop_set_slot, ALS_OBJECTS, ":slot", 0),
			(try_end),
			(presentation_set_duration, 0),
			(try_begin),
				# (eq, "$pool_troop", "trp_player"),
				(eq, "$autoloot_mode", ALS_MODE_PLAYER_SEARCH),
				(jump_to_menu, "mnu_companion_settings"),
			(else_try),
				(eq, "$autoloot_mode", ALS_MODE_BATTLEFIELD_LOOT),
				(jump_to_menu, "mnu_manage_loot_pool"),
			(else_try),
				(jump_to_menu, "$return_menu"),
			(try_end),
			
		(else_try), 
			####### CHARACTER SELECTOR #######
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_selected_character, ":object"),
			(troop_set_slot, ALS_OBJECTS, als_val_menu_selected_character, ":value"),
			(store_add, ":troop_pick", als_val_menu_troop_1, ":value"),
			(troop_get_slot, "$als_troop", ALS_OBJECTS, ":troop_pick"),
			# Initialize troop set information.
			(call_script, "script_als_initialize_troop_settings"),
			(start_presentation, "prsnt_als_settings"),
			
		(else_try),
			####### PLAYER INVENTORY SEARCH BUTTON #######
			(troop_slot_eq, ALS_OBJECTS, als_obj_inventory_search, ":object"),
			(assign, "$pool_troop", "trp_player"),
			(str_clear, s41), # Clean out the "what they took" from previous searches.
			(call_script, "script_als_troop_begin_autolooting", "$als_troop"),
			
		(else_try),
			####### COPY SETTINGS TO ALL BUTTON #######
			(troop_slot_eq, ALS_OBJECTS, als_obj_copy_settings_to_all, ":object"),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(call_script, "script_als_save_troop_settings", ":troop_no"),
			(try_end),
			(try_for_range, ":troop_no", pretenders_begin, pretenders_end),
				(call_script, "script_als_save_troop_settings", ":troop_no"),
			(try_end),
			(display_message, "@Current configuration copied to all companions and pretenders."),
		
		(else_try),
			####### WEIGHT RESTRICTION MENU #######
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_weight_limit, ":object"),
			(troop_set_slot, ALS_OBJECTS, als_val_menu_weight_limit, ":value"),
			
		(else_try),
			##### ITEM SLOT 0 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_0, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 0, ":value"),
			
		(else_try),
			##### ITEM SLOT 1 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_1, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 1, ":value"),
			
		(else_try),
			##### ITEM SLOT 2 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_2, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 2, ":value"),
			
		(else_try),
			##### ITEM SLOT 3 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_3, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 3, ":value"),
			
		(else_try),
			##### ITEM SLOT 4 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_4, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 4, ":value"),
			
		(else_try),
			##### ITEM SLOT 5 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_5, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 5, ":value"),
			
		(else_try),
			##### ITEM SLOT 6 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_6, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 6, ":value"),
			
		(else_try),
			##### ITEM SLOT 7 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_7, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 7, ":value"),
			
		(else_try),
			##### ITEM SLOT 8 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_slot_8, ":object"),
			(call_script, "script_als_handle_weapon_menu_selection", 8, ":value"),
			
		(else_try),
			##### WEAPON TYPE 0 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_weapon_type_0, ":object"),
			(call_script, "script_als_handle_damage_type_menu_selection", 0, ":value"),
			
		(else_try),
			##### WEAPON TYPE 1 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_weapon_type_1, ":object"),
			(call_script, "script_als_handle_damage_type_menu_selection", 1, ":value"),
			
		(else_try),
			##### WEAPON TYPE 2 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_weapon_type_2, ":object"),
			(call_script, "script_als_handle_damage_type_menu_selection", 2, ":value"),
			
		(else_try),
			##### WEAPON TYPE 3 - MENU #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_menu_weapon_type_3, ":object"),
			(call_script, "script_als_handle_damage_type_menu_selection", 3, ":value"),
			
		(else_try),
			##### ENABLE DWS CHECKBOX #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_checkbox_enable, ":object"),
			(troop_set_slot, ALS_OBJECTS, als_val_checkbox_enable, ":value"),
			#(troop_set_slot, "$als_troop", slot_troop_enable_autolooting, ":value"),
			(ge, DEBUG_ALS, 1),
			(assign, reg31, ":value"),
			(display_message, "@DEBUG (ALS): Autolooting set to {reg31}. [{reg31?Enabled:Disabled}]"),
			
		(else_try),
			##### DON'T BREAK SETS CHECKBOX #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_checkbox_no_break_sets, ":object"),
			(troop_set_slot, ALS_OBJECTS, als_val_checkbox_no_break_sets, ":value"),
			#(troop_set_slot, "$als_troop", slot_troop_prevent_breaking_sets, ":value"),
			(ge, DEBUG_ALS, 1),
			(assign, reg31, ":value"),
			(display_message, "@DEBUG (ALS): 'Do not break sets' enforcement set to {reg31}. [{reg31?Enabled:Disabled}]"),
			
		(else_try),
			##### KEEP HERALDIC ARMOR CHECKBOX #####
			(troop_slot_eq, ALS_OBJECTS, als_obj_checkbox_heraldic_items, ":object"),
			(troop_set_slot, ALS_OBJECTS, als_val_checkbox_heraldic_items, ":value"),
			#(troop_set_slot, "$als_troop", slot_troop_retain_heraldic_items, ":value"),
			(ge, DEBUG_ALS, 1),
			(assign, reg31, ":value"),
			(display_message, "@DEBUG (ALS): 'Keep heraldic armor' set to {reg31}. [{reg31?Enabled:Disabled}]"),
			
		(else_try), 
			####### SHOW OBJECT LIST #######
			(troop_slot_eq, ALS_OBJECTS, als_obj_test, ":object"),
			(try_for_range, ":slot", 0, 9),
				(assign, reg20, ":slot"),
				(troop_get_slot, reg21, "trp_temp_array_a", ":slot"),
				(troop_get_slot, reg22, "trp_temp_array_b", ":slot"),
				(troop_get_slot, reg23, "trp_temp_array_c", ":slot"),
				(store_add, ":string_no", "str_als_label_slot_1", ":slot"),
				(str_store_string, s21, ":string_no"),
				(ge, reg21, 1),
				(display_message, "@[#{reg20} / {s21}]: {reg21}, {reg22}, [Item: {reg23}]"),
			(try_end),
			
			
		(try_end),
		
	]),
  ]),
  
# This preference panel will set what kinds of equipment the player wishes allowed in each city's specific tournaments.
  ("auto_loot_checklist", 0, mesh_load_window, [
    (ti_on_presentation_load,
    [
		(set_fixed_point_multiplier, 1000),
		
		(assign, "$gpu_storage", ALS_OBJECTS),
		(assign, "$gpu_data",    ALS_TRADE_CONFIRM),
		
		# Assign margins
		(assign, ":font_size", 75),
		(assign, ":pos_x_checkboxes", 70),
		(assign, ":pos_x_slot", 120),
		(assign, ":pos_x_old", 220),
		(assign, ":pos_x_new", 415),
		(assign, ":pos_x_comments", 630),
		(assign, ":pos_y_titles", 620),
		
		# Button Definitions
		(call_script, "script_gpu_create_game_button", "str_alc_confirm", 885, 30, alc_obj_button_accept),
		(call_script, "script_gpu_create_game_button", "str_alc_skip", 695, 30, alc_obj_button_cancel),
		
		# Create Character Portrait
		(call_script, "script_gpu_create_portrait", "$alc_troop", 70, 500, 500, alc_obj_portrait_selected_troop),
		(str_store_troop_name, s21, "$alc_troop"),
		(call_script, "script_gpu_create_text_label", "str_cms_s21", 140, 475, alc_obj_label_main_title, gpu_center),
		
		# Text Labels
		(call_script, "script_gpu_create_text_label", "str_alc_main_title", 500, 680, alc_obj_label_main_title, gpu_center),
		(call_script, "script_gpu_resize_object", alc_obj_label_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_alc_main_title", 500, 680, alc_obj_label_main_title, gpu_center),
		(call_script, "script_gpu_resize_object", alc_obj_label_main_title, 150),
		
		# Scrolling "what they took" list.
		(call_script, "script_gpu_container_heading", 300, 475, 650, 185, alc_obj_label_upgrade_text_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			(call_script, "script_gpu_create_text_label", "str_alc_label_s41", 0, 0, alc_obj_label_upgrade_text, gpu_left),
			(call_script, "script_gpu_resize_object", alc_obj_label_upgrade_text, ":font_size"),
		################ CONTAINER END ################	
		(set_container_overlay, -1),
		
		### HEADER ###
		(call_script, "script_gpu_draw_line", 950, 30, 25, 425, gpu_brown), # Brown header
		(overlay_set_alpha, reg1, 0xCC),
		(assign, ":pos_y", 455),
		(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_black),
		(store_sub, ":pos_y_titles", ":pos_y", 13),
		
		(call_script, "script_gpu_create_text_label", "str_alc_header_approval", ":pos_x_checkboxes", ":pos_y_titles", alc_obj_label_approve, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", alc_obj_label_approve, ":font_size"),
		
		(call_script, "script_gpu_create_text_label", "str_alc_header_slot", ":pos_x_slot", ":pos_y_titles", alc_obj_label_slot, gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", alc_obj_label_slot, ":font_size"),
		
		(call_script, "script_gpu_create_text_label", "str_alc_header_old", ":pos_x_old", ":pos_y_titles", alc_obj_label_old, gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", alc_obj_label_old, ":font_size"),
		
		(call_script, "script_gpu_create_text_label", "str_alc_header_new",      ":pos_x_new",        ":pos_y_titles", alc_obj_label_new,     gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", alc_obj_label_new, ":font_size"),
		
		(call_script, "script_gpu_create_text_label", "str_alc_header_special",  ":pos_x_comments",   ":pos_y_titles", alc_obj_label_comment, gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", alc_obj_label_comment, ":font_size"),
		
		(val_sub, ":pos_y", 30),
		(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_black),
		
		### FOOTER ###
		(call_script, "script_gpu_draw_line", 950, 30, 25, 85, gpu_brown), # Brown footer
		(overlay_set_alpha, reg1, 0xCC),
		(assign, ":pos_y", 115),
		(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_black),
		#(store_sub, ":pos_y_titles", ":pos_y", 3),
		
		(call_script, "script_gpu_create_text_label", "str_alc_sub_title", 500, ":pos_y", alc_obj_label_sub_title, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", alc_obj_label_sub_title, 75),
		
		(val_sub, ":pos_y", 30),
		(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_black),
		
		### SIDE BORDERS ###
		(call_script, "script_gpu_draw_line", 2, 370, 25, 85, gpu_black), # left border
		(call_script, "script_gpu_draw_line", 2, 370, 973, 85, gpu_black), # right border
		
		# (call_script, "script_gpu_container_heading", 0, 115, 1000, 485, alc_obj_main_container), # Scrolling container
		# ############### CONTAINER BEGIN ###############
		(assign, ":pos_y", 400),
		(try_for_range, ":storage_slot", 0, 15),
			(troop_slot_ge, ALS_TRADE_CONFIRM, ":storage_slot", 0), # An upgrade option is available.
			(lt, ":storage_slot", 9), # Temporary.
			
			# Approval checkbox.
			(store_add, ":pos_y_checkbox", ":pos_y", -15),
			(store_add, ":pos_x", ":pos_x_checkboxes", -10),
			(store_add, ":obj_slot", alc_obj_approval_checkboxes_begin, ":storage_slot"),
			(call_script, "script_gpu_create_checkbox", ":pos_x", ":pos_y_checkbox", "str_cms_blank", ":obj_slot", ":storage_slot"),
			#(call_script, "script_gpu_resize_object", ":obj_slot", ":font_size"),
			
			# What slot is being upgraded.
			(store_add, ":pos_x", ":pos_x_slot", 5),
			(troop_get_slot, ":item_slot", ALS_OLD_ITEM, ":storage_slot"),
			(store_add, ":obj_slot", alc_obj_slot_labels, ":storage_slot"),
			(store_add, ":string_slot", "str_als_label_slot_1", ":item_slot"),
			(call_script, "script_gpu_create_text_label", ":string_slot", ":pos_x", ":pos_y", ":obj_slot", gpu_left),
			(call_script, "script_gpu_resize_object", ":obj_slot", ":font_size"),
			
			# The current item the troop has.
			(store_add, ":pos_x", ":pos_x_old", 5),
			(store_add, ":obj_slot", alc_obj_old_item_labels, ":storage_slot"),
			(troop_get_slot, ":item_slot", ALS_OLD_ITEM, ":storage_slot"),
			(troop_get_inventory_slot, ":item_old", "$alc_troop", ":item_slot"),
			(try_begin),
				(ge, ":item_old", 1),
				(troop_get_inventory_slot_modifier, ":imod", "$alc_troop", ":item_slot"),
				(call_script, "script_als_get_item_rating", "$alc_troop", ":item_old", ":imod"),
				(str_store_item_name, s21, ":item_old"),
				(str_store_string, s21, "@{s21} ({reg1})"),
			(else_try),
				(str_store_string, s21, "@Empty (0)"),
			(try_end),
			(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x", ":pos_y", ":obj_slot", gpu_left),
			(call_script, "script_gpu_resize_object", ":obj_slot", ":font_size"),
			
			# The best item available to upgrade to for this troop.
			(store_add, ":pos_x", ":pos_x_new", 5),
			(store_add, ":obj_slot", alc_obj_new_item_labels, ":storage_slot"),
			(troop_get_slot, ":item_slot", ALS_NEW_ITEM, ":storage_slot"),
			(troop_get_inventory_slot, ":item_new", "$pool_troop", ":item_slot"),
			(troop_get_inventory_slot_modifier, ":imod", "$pool_troop", ":item_slot"),
			(call_script, "script_als_get_item_rating", "$alc_troop", ":item_new", ":imod"),
			(str_store_item_name, s21, ":item_new"),
			(str_store_string, s21, "@{s21} ({reg1})"),
			(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x", ":pos_y", ":obj_slot", gpu_left),
			(call_script, "script_gpu_resize_object", ":obj_slot", ":font_size"),
			
			# Special comments about the items being upgraded.
			(str_clear, s21),
			(assign, ":count", 0),
			# Filter out heraldic items.
			(try_begin),
				(troop_slot_eq, "$alc_troop", slot_troop_retain_heraldic_items, 1),
				(call_script, "script_cf_als_item_is_heraldic", ":item_old"),
				(str_store_string, s21, "@{s21}Heraldic (old) "),
				(val_add, ":count", 1),
				(troop_set_slot, ALS_TRADE_CONFIRM, ":storage_slot", 0), # Turn off upgrading for now.
				(store_add, ":obj_slot", alc_obj_approval_checkboxes_begin, ":storage_slot"),
				(troop_get_slot, ":obj_no", ALS_OBJECTS, ":obj_slot"),
				(overlay_set_val, ":obj_no", 0),
			(try_end),
			(try_begin),
				(troop_slot_eq, "$alc_troop", slot_troop_retain_heraldic_items, 1),
				(call_script, "script_cf_als_item_is_heraldic", ":item_new"),
				(try_begin),
					(ge, ":count", 1),
					(str_store_string, s21, "@{s21}, "),
				(try_end),
				(str_store_string, s21, "@{s21}Heraldic (new)"),
				(val_add, ":count", 1),
				(troop_set_slot, ALS_TRADE_CONFIRM, ":storage_slot", 1), # Turn off upgrading for now.
				(store_add, ":obj_slot", alc_obj_approval_checkboxes_begin, ":storage_slot"),
				(troop_get_slot, ":obj_no", ALS_OBJECTS, ":obj_slot"),
				(overlay_set_val, ":obj_no", 1),
			(try_end),
			
			# Filter out weapon set items.
			(try_begin),
				(troop_slot_eq, "$alc_troop", slot_troop_prevent_breaking_sets, 1),
				(call_script, "script_cf_dws_item_in_a_weapon_set", "$alc_troop", ":item_old"),
				(try_begin),
					(ge, ":count", 1),
					(str_store_string, s21, "@{s21}, "),
				(try_end),
				(str_store_string, s21, "@{s21}Weapon set (old)"),
				(val_add, ":count", 1),
				(troop_set_slot, ALS_TRADE_CONFIRM, ":storage_slot", 0), # Turn off upgrading for now.
				(store_add, ":obj_slot", alc_obj_approval_checkboxes_begin, ":storage_slot"),
				(troop_get_slot, ":obj_no", ALS_OBJECTS, ":obj_slot"),
				(overlay_set_val, ":obj_no", 0),
			(try_end),
			
			# The best item available to upgrade to for this troop.
			(store_add, ":pos_x", ":pos_x_comments", 5),
			(store_add, ":obj_slot", als_obj_label_comments_0, ":storage_slot"),
			(str_store_string, s21, "@{s21}"),
			(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x", ":pos_y", ":obj_slot", gpu_left),
			(call_script, "script_gpu_resize_object", ":obj_slot", ":font_size"),
			
			(val_sub, ":pos_y", 20),
			(call_script, "script_gpu_draw_line", 930, 2, 35, ":pos_y", gpu_black),
			(val_sub, ":pos_y", 20),
		(try_end),
		# ############### CONTAINER END ###############	
		# (set_container_overlay, -1),
		
		(presentation_set_duration, 999999),
    ]),

	(ti_on_presentation_event_state_change,
    [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(try_begin),
			##### ACCEPT CHANGES / SKIP TO NEXT BUTTONS #####
			(this_or_next|troop_slot_eq, ALS_OBJECTS, alc_obj_button_accept, ":object"),
			(troop_slot_eq, ALS_OBJECTS, alc_obj_button_cancel, ":object"),
			(presentation_set_duration, 0),
			(try_begin),
				(troop_slot_eq, ALS_OBJECTS, alc_obj_button_accept, ":object"),
				(call_script, "script_als_execute_upgrade_checklist"),
			(try_end),
			(try_begin),
				(neq, "$pool_troop", "trp_player"),
				(jump_to_menu, "mnu_als_jump_to_next_looter"),
			(else_try),
				# Jump to Autoloot Settings for Specific Troop
				(party_get_num_companions, reg1, "p_main_party"),
				(party_get_num_companion_stacks, ":stacks", "p_main_party"),
				(assign, "$als_troop", -1),
				(assign, ":menu_item_count", -1),
				(try_for_range, ":stack_no", 0, ":stacks"),
					(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
					(this_or_next|is_between, ":troop_no", companions_begin, companions_end),
					(is_between, ":troop_no", pretenders_begin, pretenders_end),
					(eq, "$als_troop", -1),
					(val_add, ":menu_item_count", 1),
					(eq, ":troop_no", "$alc_troop"),
					(assign, "$als_troop", ":troop_no"),
					(break_loop),
				(try_end),
				
				# Setup default character as first companion.
				(troop_set_slot, ALS_OBJECTS, als_val_menu_selected_character, ":menu_item_count"),
				
				# Initialize settings.
				(call_script, "script_als_initialize_troop_settings"),
				(assign, reg51, "prsnt_als_settings"),
				(jump_to_menu, "mnu_als_jump_to_presentation"),
			(try_end),
			
		# (else_try),
			# ##### SKIP BUTTON #####
			# (troop_slot_eq, ALS_OBJECTS, alc_obj_button_cancel, ":object"),
			# # Clean out ALS_OBJECTS
			# (presentation_set_duration, 0),
			# (jump_to_menu, "mnu_als_jump_to_next_looter"),
			
		(else_try),
			##### CONFIRMATION CHECKBOX #####
			(assign, ":obj_slot", -1),
			(try_for_range, ":slot", alc_obj_approval_checkboxes_begin, alc_obj_approval_checkboxes_end),
				(assign, reg32, ":object"),
				(troop_slot_eq, ALS_OBJECTS, ":slot", ":object"),
				(assign, ":obj_slot", ":slot"),
				(troop_get_slot, ":object_no", ALS_OBJECTS, ":slot"),
				(break_loop),
			(try_end),
			(ge, ":object_no", 0),
			(overlay_set_val, ":object", ":value"),
			(store_sub, ":storage_slot", ":obj_slot", alc_obj_approval_checkboxes_begin),
			(troop_set_slot, ALS_TRADE_CONFIRM, ":storage_slot", ":value"),
			(ge, DEBUG_ALS, 1),
			(assign, reg31, ":storage_slot"),
			(assign, reg32, ":value"),
			(display_message, "@DEBUG (ALS): Approval for upgrade option #{reg31} is {reg32?Enabled:Disabled}."),
			
		(try_end),
		
	]),
  ]),
  

###########################################################################################################################
#####                                           COMPANION RELATION MATRIX                                             #####
###########################################################################################################################
# This preference panel will set what kinds of equipment the player wishes allowed in each city's specific tournaments.
  ("relation_matrix", 0, mesh_load_window, [
    (ti_on_presentation_load,
    [
		(set_fixed_point_multiplier, 1000),
		
		(assign, "$gpu_storage", CRM_OBJECTS),
		(assign, "$gpu_data",    CRM_OBJECTS),
		
		## MARGIN DEFINITIONS ##
		(assign, ":font_size",        75),
		(assign, ":pos_y_row_step",  125),
		# Column 1
		(assign, ":pos_x_portrait",   30),
		(assign, ":pos_y_portrait",   25),
		# Column 2
		(assign, ":pos_x_troop",     150),
		#(assign, ":pos_x_status",    220),
		(assign, ":pos_y_name",       80),
		(assign, ":pos_y_status",     60),
		(assign, ":pos_y_morale",     40),
		# Column 3
		(assign, ":pos_x_issues",    300),
		(assign, ":pos_y_issues",     80),
		(assign, ":pos_y_line_step",  25),
		# Column 4
		(assign, ":pos_x_friends",   500),
		(assign, ":pos_y_friends",    25),
		# Column 5
		(assign, ":pos_x_enemies",   650),
		(assign, ":pos_x_enemies_2", 750),
		(assign, ":pos_y_enemies",    25),
		
		# Button Definitions
		(call_script, "script_gpu_create_game_button", "str_cms_cancel", 870, 30, crm_obj_button_exit),
		
		# Text Labels
		(call_script, "script_gpu_create_text_label", "str_crm_main_title", 500, 680, crm_obj_label_main_title, gpu_center),
		(call_script, "script_gpu_resize_object", crm_obj_label_main_title, 150),
		(call_script, "script_gpu_create_text_label", "str_crm_main_title", 500, 680, crm_obj_label_main_title, gpu_center),
		(call_script, "script_gpu_resize_object", crm_obj_label_main_title, 150),
		# (call_script, "script_gpu_create_text_label", "str_crm_main_title", 500, 680, crm_obj_label_main_title, gpu_center_with_outline),
		# (overlay_set_color, reg1, gpu_white),
		
		# Headers
		(call_script, "script_gpu_create_text_label", "str_crm_title_companion", 120, 620, crm_obj_temporary, gpu_left),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_create_text_label", "str_crm_title_morality",  350, 620, crm_obj_temporary, gpu_left),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_create_text_label", "str_crm_title_friends",   565, 620, crm_obj_temporary, gpu_left),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_create_text_label", "str_crm_title_enemies",   750, 620, crm_obj_temporary, gpu_left),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_draw_line", 852, 37, 73, 605, gpu_brown), # Brown background
		(call_script, "script_gpu_draw_line", 852, 2, 73, 640, gpu_black), # - Header
		(call_script, "script_gpu_draw_line", 852, 2, 73, 605, gpu_black), # - Header
		(call_script, "script_gpu_draw_line", 850, 2, 73, 95, gpu_black), # - Footer
		(call_script, "script_gpu_draw_line", 2, 547, 73, 95, gpu_black), # | Left border
		(call_script, "script_gpu_draw_line", 2, 547, 923, 95, gpu_black), # | Right border
		
		
		# Scrolling list of companions.
		(call_script, "script_gpu_container_heading", 50, 100, 875, 500, crm_obj_label_upgrade_text_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			# Count how many companions are in the party.
			(assign, ":count", -1),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				(val_add, ":count", 1),
			(try_end),
			
			# Set starting limit based on number of companions.
			(store_mul, ":pos_y", ":count", ":pos_y_row_step"),
			
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				
				(call_script, "script_gpu_draw_line", 875, 2, 25, ":pos_y", gpu_black),
				#(eq, ":troop_no", "trp_npc16"), # Klethi
				
				## COLUMN 1 ## - Companion Portrait
				(store_add, ":pos_y_temp", ":pos_y", ":pos_y_portrait"),
				(call_script, "script_gpu_create_portrait", ":troop_no", ":pos_x_portrait", ":pos_y_temp", 300, 0),
				
				## COLUMN 2 ## - Companion Name & Status
				(str_store_troop_name, s21, ":troop_no"),
				(store_add, ":pos_y_line_1", ":pos_y", ":pos_y_name"),
				(store_add, ":pos_y_line_2", ":pos_y", ":pos_y_status"),
				(store_add, ":pos_y_line_3", ":pos_y", ":pos_y_morale"),
				
				#(store_add, ":pos_x_temp", ":pos_x_troop", -5),
				(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x_troop", ":pos_y_line_1", crm_obj_temporary, gpu_left),
				
				(assign, reg21, 0),
				(try_begin),
					(troop_get_slot, ":troop_id", ":troop_no", slot_troop_personalitymatch_object),
					(main_party_has_troop, ":troop_id"),
					(val_add, reg21, 1),
					(eq, 1, 0),
				(else_try),
					(troop_get_slot, ":troop_id", ":troop_no", slot_troop_personalityclash_object),
					(main_party_has_troop, ":troop_id"),
					(val_sub, reg21, 1),
					(eq, 1, 0),
				(else_try),
					(troop_get_slot, ":troop_id", ":troop_no", slot_troop_personalityclash2_object),
					(main_party_has_troop, ":troop_id"),
					(val_sub, reg21, 1),
					(eq, 1, 0),
				(try_end),
				(store_add, ":string_no", "str_crm_status_neutral", reg21),
				(str_store_string, s21, ":string_no"),
				
				(call_script, "script_gpu_create_text_label", "str_crm_companion_status", ":pos_x_troop", ":pos_y_line_2", crm_obj_temporary, gpu_left),
				(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
				
				(call_script, "script_npc_morale", ":troop_no"),
				(assign, reg21, reg0),
				(call_script, "script_gpu_create_text_label", "str_crm_label_morale", ":pos_x_troop", ":pos_y_line_3", crm_obj_temporary, gpu_left),
				(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
				
				## COLUMN 3 ## - Companion Annoyances
				(troop_get_slot, ":morality1", ":troop_no", slot_troop_morality_type),
				(troop_get_slot, ":morality2", ":troop_no", slot_troop_2ary_morality_type),
				(troop_get_slot, ":value1", ":troop_no", slot_troop_morality_value),
				(troop_get_slot, ":value2", ":troop_no", slot_troop_2ary_morality_value),
				(store_add, ":pos_y_temp", ":pos_y", ":pos_y_issues"),
				
				# Loop setup
				(try_for_range, ":morality_type", 1, 8),
					(this_or_next|eq, ":morality1", ":morality_type"),
					(eq, ":morality2", ":morality_type"),
					(store_add, ":string_no", "str_crm_morality_1", ":morality_type"),
					(val_sub, ":string_no", 1),
					(try_begin),
						(eq, ":morality1", ":morality_type"),
						(assign, reg21, ":value1"),
					(else_try),
						(assign, reg21, ":value2"),
					(try_end),
					(call_script, "script_gpu_create_text_label", ":string_no", ":pos_x_issues", ":pos_y_temp", crm_obj_temporary, gpu_left),
					(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
					(val_sub, ":pos_y_temp", ":pos_y_line_step"),
				(try_end),
				
				## COLUMN 4 ## - Companion's Friends
				(try_begin),
					(troop_get_slot, ":troop_friend", ":troop_no", slot_troop_personalitymatch_object),
					(is_between, ":troop_friend", companions_begin, companions_end),
					#(store_add, ":pos_x_temp", ":pos_x", ":pos_x_friends"),
					(store_add, ":pos_y_temp", ":pos_y", ":pos_y_friends"),
					(call_script, "script_gpu_create_portrait", ":troop_friend", ":pos_x_friends", ":pos_y_temp", 250, 0),
					# Name label
					(str_store_troop_name, s21, ":troop_friend"),
					(store_add, ":pos_x_temp", ":pos_x_friends", 40),
					(store_add, ":pos_y_temp", ":pos_y", 15),
					(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x_temp", ":pos_y_temp", crm_obj_temporary, gpu_center),
					(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
					(main_party_has_troop, ":troop_friend"),
					(overlay_set_color, reg1, 14336), # Dark Green
					# Do it twice to bold it.
					(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x_temp", ":pos_y_temp", crm_obj_temporary, gpu_center),
					(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
					(overlay_set_color, reg1, 14336), # Dark Green
				(try_end),
				
				## COLUMN 5 ## - Companion's Enemies
				(try_begin),
					(troop_get_slot, ":troop_enemy", ":troop_no", slot_troop_personalityclash_object),
					(is_between, ":troop_enemy", companions_begin, companions_end),
					#(store_add, ":pos_x_temp", ":pos_x", ":pos_x_enemies"),
					(store_add, ":pos_y_temp", ":pos_y", ":pos_y_enemies"),
					(call_script, "script_gpu_create_portrait", ":troop_enemy", ":pos_x_enemies", ":pos_y_temp", 250, 0),
					# Name label
					(str_store_troop_name, s21, ":troop_enemy"),
					(store_add, ":pos_x_temp", ":pos_x_enemies", 40),
					(store_add, ":pos_y_temp", ":pos_y", 15),
					(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x_temp", ":pos_y_temp", crm_obj_temporary, gpu_center),
					(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
					(main_party_has_troop, ":troop_enemy"),
					(overlay_set_color, reg1, 4980736), # Dark Red
					# Do it twice to bold it.
					(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x_temp", ":pos_y_temp", crm_obj_temporary, gpu_center),
					(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
					(overlay_set_color, reg1, 4980736), # Dark Red
				(try_end),
				
				(try_begin),
					(troop_get_slot, ":troop_enemy", ":troop_no", slot_troop_personalityclash2_object),
					(is_between, ":troop_enemy", companions_begin, companions_end),
					#(store_add, ":pos_x_temp", ":pos_x", ":pos_x_enemies_2"),
					(store_add, ":pos_y_temp", ":pos_y", ":pos_y_enemies"),
					(call_script, "script_gpu_create_portrait", ":troop_enemy", ":pos_x_enemies_2", ":pos_y_temp", 250, 0),
					# Name label
					(str_store_troop_name, s21, ":troop_enemy"),
					(store_add, ":pos_x_temp", ":pos_x_enemies_2", 40),
					(store_add, ":pos_y_temp", ":pos_y", 15),
					(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x_temp", ":pos_y_temp", crm_obj_temporary, gpu_center),
					(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
					(main_party_has_troop, ":troop_enemy"),
					(overlay_set_color, reg1, 4980736), # Dark Red
					# Do it twice to bold it.
					(call_script, "script_gpu_create_text_label", "str_cms_s21", ":pos_x_temp", ":pos_y_temp", crm_obj_temporary, gpu_center),
					(call_script, "script_gpu_resize_object", crm_obj_temporary, ":font_size"),
					(overlay_set_color, reg1, 4980736), # Dark Red
				(try_end),
				
				## END OF ROW ##
				(val_sub, ":pos_y", ":pos_y_row_step"),
				
			(try_end),
			
		################ CONTAINER END ################	
		(set_container_overlay, -1),
		
		(presentation_set_duration, 999999),
    ]),

	(ti_on_presentation_event_state_change,
		[
			(store_trigger_param_1, ":object"),
			#(store_trigger_param_2, ":value"),
			
			(try_begin),
				##### EXIT BUTTON #####
				(troop_slot_eq, CRM_OBJECTS, crm_obj_button_exit, ":object"),
				(presentation_set_duration, 0),
				(jump_to_menu, "$return_menu"),
				
			(try_end),
			
		]),
  ]),
  
###########################################################################################################################
#####                                                 PARTY ROLES                                                     #####
###########################################################################################################################

# This presentation allows the player to select who in their party will fill in specific "assignments" such as storekeeping.
  ("cms_party_roles", 0, mesh_load_window, [
    (ti_on_presentation_load,
    [
		(set_fixed_point_multiplier, 1000),
		
		(assign, "$gpu_storage", ROLE_OBJECTS),
		(assign, "$gpu_data",    ROLE_OBJECTS),
		
		## MARGIN DEFINITIONS ##
		# Column 1
		(assign, ":pos_x_portrait",   30),
		(assign, ":pos_y_portrait",   25),
		# Column 2
		(assign, ":pos_x_title",     155),
		(assign, ":pos_x_menu_adj",  290),
		(assign, ":pos_y2_title",    105),
		(assign, ":pos_y2_menu",      92),
		(assign, ":pos_y2_desc",      73),
		# Column 3
		(assign, ":pos_x_report",    530),
		(assign, ":pos_y3_title",    105),
		
		
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		### BUTTONS+ ###
		(call_script, "script_gpu_create_game_button", "str_cms_cancel", 870, 30, role_obj_button_exit),
		## SHOPPING LIST redirect
		(str_store_string, s21, "@Shopping List"),
		(call_script, "script_gpu_create_game_button", "str_cms_s21", 125, 30, role_obj_button_shopping_list),
		### BUTTONS- ###
		
		### CHECKBOXES+ ###
		## Storekeeper Enable Auto-Buy
		(troop_set_slot, ROLE_OBJECTS, role_val_checkbox_storekeeper_enable, "$cms_enable_auto_buying"),
		(str_store_string, s21, "@Enable Storekeeper Purchasing"),
		(call_script, "script_gpu_create_checkbox", 235, 50, "str_cms_s21", role_obj_checkbox_storekeeper_enable, role_val_checkbox_storekeeper_enable),
		
		## Quartermaster Enable Auto-Sell
		(troop_set_slot, ROLE_OBJECTS, role_val_checkbox_quartermaster_enable, "$cms_enable_auto_selling"),
		(str_store_string, s21, "@Enable Quartermaster Selling"),
		(call_script, "script_gpu_create_checkbox", 235, 25, "str_cms_s21", role_obj_checkbox_quartermaster_enable, role_val_checkbox_quartermaster_enable),
		### CHECKBOXES- ###
		
		# Text Labels
		# (call_script, "script_gpu_create_text_label", "str_role_main_title", 500, 665, role_obj_label_main_title, gpu_center_with_outline),
		# (overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_create_text_label", "str_role_main_title", 500, 665, role_obj_label_main_title, gpu_center),
		(call_script, "script_gpu_resize_object", role_obj_label_main_title, 150),
		# Double print for bolding.
		(call_script, "script_gpu_create_text_label", "str_role_main_title", 500, 665, role_obj_label_main_title, gpu_center),
		(call_script, "script_gpu_resize_object", role_obj_label_main_title, 150),
		
		# Scrolling list of companions.
		(call_script, "script_gpu_container_heading", 50, 100, 875, 500, role_obj_label_main_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			(assign, ":pos_y", 400), # Starting point.
			(assign, ":spacing_roles", 150), # Denotes the space alloted between role sections.
			
			######## STOREKEEPER : BEGIN ########
			(call_script, "script_cms_verify_party_role_filled", ROLE_STOREKEEPER),
			
			## COLUMN 1 ## - Companion Portrait
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y_portrait"),
			(call_script, "script_gpu_create_portrait", "$cms_role_storekeeper", ":pos_x_portrait", ":pos_y_temp", 300, 0),
			
			## COLUMN 2 ## - Role Title: Companion Name, Description of role.
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_title"),
			(call_script, "script_gpu_create_text_label", "str_role_label_storekeeper", ":pos_x_title", ":pos_y_temp", role_obj_label_storekeeper, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_role_label_storekeeper", ":pos_x_title", ":pos_y_temp", role_obj_label_storekeeper, gpu_left),
			
			# ROLE -> CHARACTER SELECTION MENU BEGIN
			(store_add, ":pos_x_menu", ":pos_x_title", ":pos_x_menu_adj"), 	  (position_set_x, pos1, ":pos_x_menu"),
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_menu"), (position_set_y, pos1, ":pos_y_temp"),
			
			(create_combo_button_overlay, reg1),
			(overlay_set_position, reg1, pos1),
			(troop_set_slot, ROLE_OBJECTS, role_obj_menu_storekeeper, reg1),
			(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
			(assign, ":hero_slot", 0),
			(try_for_range, ":stack_num", 0, ":num_stacks"),
				(store_add, ":slot_pick", role_val_menu_troop_1, ":hero_slot"),
				(party_stack_get_troop_id,":troop_no","p_main_party",":stack_num"),
				(troop_is_hero, ":troop_no"),
				(try_begin),
					(eq, ":troop_no", "$cms_role_storekeeper"),
					(troop_set_slot, ROLE_OBJECTS, role_val_menu_storekeeper, ":hero_slot"),
				(try_end),
				(str_clear, s1),
				(str_store_troop_name, s1, ":troop_no"),
				(troop_set_slot, ROLE_OBJECTS, ":slot_pick", ":troop_no"),
				(try_begin),
					(ge, DEBUG_ROLE, 2),
					(assign, reg31, ":slot_pick"),
					(display_message, "@DEBUG (CMS): Added '{s1}' to character chooser menu.  Slot #{reg31}"),
				(try_end),
				(val_add, ":hero_slot", 1),
				(overlay_add_item, reg1, "@{s1}"),
			(try_end),
			(troop_get_slot, ":selected_profile", ROLE_OBJECTS, role_val_menu_storekeeper),
			(overlay_set_val, reg1, ":selected_profile"),
			(call_script, "script_gpu_resize_object", role_obj_menu_storekeeper, 75),
			# ROLE -> CHARACTER SELECTION MENU END
			
			# Description of role.
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_desc"),
			(store_add, ":pos_x_temp", ":pos_x_title", 0),
			(troop_get_type, reg21, "$cms_role_storekeeper"),
			(call_script, "script_gpu_create_text_label", "str_role_desc_storekeeper", ":pos_x_temp", ":pos_y_temp", role_obj_label_storekeeper_desc, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_storekeeper_desc, 75),
			# Requirements
			(val_sub, ":pos_y_temp", 60),
			(call_script, "script_gpu_create_text_label", "str_role_desc_storekeeper_reqs", ":pos_x_temp", ":pos_y_temp", role_obj_label_storekeeper_reqs, gpu_left),
			(overlay_set_color, reg1, gpu_blue),
			(call_script, "script_gpu_resize_object", role_obj_label_storekeeper_reqs, 75),
			# Double for bold effect.
			(call_script, "script_gpu_create_text_label", "str_role_desc_storekeeper_reqs", ":pos_x_temp", ":pos_y_temp", role_obj_label_storekeeper_reqs, gpu_left),
			(overlay_set_color, reg1, gpu_blue),
			(call_script, "script_gpu_resize_object", role_obj_label_storekeeper_reqs, 75),
			
			## COLUMN 3 ## - Reports
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y3_title"),
			(call_script, "script_gpu_create_text_label", "str_role_label_storekeeper_reports", ":pos_x_report", ":pos_y_temp", role_obj_label_storekeeper_report, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_role_label_storekeeper_reports", ":pos_x_report", ":pos_y_temp", role_obj_label_storekeeper_report, gpu_left), # Double for bold effect.
			
			# Days of food left.
			(call_script, "script_calculate_days_of_food_remaining"), # reg0 (# of men), reg1 (food available), reg2 (days left)
			(assign, reg21, reg2),
			(assign, ":days_remaining", reg2),
			(val_sub, ":pos_y_temp", 22),
			(store_add, ":pos_x_temp", ":pos_x_report", 0),
			(call_script, "script_gpu_create_text_label", "str_role_label_skr_days_left", ":pos_x_temp", ":pos_y_temp", role_obj_label_skr_days_left, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_skr_days_left, 75),
			(try_begin), # Change this line of text to be red if we're below our threshold value.
				(lt, ":days_remaining", "$cms_days_of_food_threshold"),
				(ge, "$cms_days_of_food_threshold", 1), # A setting of 0 disables this option.
				(overlay_set_color, reg1, gpu_dark_red),
				(call_script, "script_gpu_create_text_label", "str_role_label_skr_days_left", ":pos_x_temp", ":pos_y_temp", role_obj_label_skr_days_left, gpu_left),
				(call_script, "script_gpu_resize_object", role_obj_label_skr_days_left, 75),
				(overlay_set_color, reg1, gpu_red),
			(try_end),
			
			# Number of kinds of food.
			(assign, ":number_of_foods_player_has", 0),
			(try_for_range, ":item_no", food_begin, food_end),      
				(call_script, "script_cf_player_has_item_without_modifier", ":item_no", imod_rotten),
				(val_add, ":number_of_foods_player_has", 1),
			(try_end),
			(try_begin),
				(ge, ":number_of_foods_player_has", 2),
				(str_store_string, s21, "@different types"),
			(else_try),
				(str_store_string, s21, "@type"),
			(try_end),
			(assign, reg21, ":number_of_foods_player_has"),
			(val_sub, ":pos_y_temp", 15),
			(call_script, "script_gpu_create_text_label", "str_role_label_skr_kinds_of_food", ":pos_x_temp", ":pos_y_temp", role_obj_label_skr_kinds_of_food, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_skr_kinds_of_food, 75),
			# Morale bonus
			(try_begin), ## ENHANCED DIPLOMACY INTERCONNECTION
				(eq, "$diplomacy_use_alt_morale", 1),
				(call_script, "script_diplomacy_get_player_party_morale_values"), # Use alternate morale system.
			(else_try),
				(call_script, "script_get_player_party_morale_values"), # Use native morale system.
			(try_end),
			(try_begin),
				(gt, "$g_player_party_morale_modifier_no_food", 0),
				(store_mul, reg21, "$g_player_party_morale_modifier_no_food", -1),
				(str_clear, s21),
			(else_try),
				(assign, reg21, "$g_player_party_morale_modifier_food"),
				(str_store_string, s21, "@+"),
			(try_end),
			(val_sub, ":pos_y_temp", 15),
			(call_script, "script_gpu_create_text_label", "str_role_label_skr_food_morale", ":pos_x_temp", ":pos_y_temp", role_obj_label_skr_food_morale, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_skr_food_morale, 75),
			######## STOREKEEPER : END ########
			
			######## QUARTERMASTER : BEGIN ########
			(call_script, "script_cms_verify_party_role_filled", ROLE_QUARTERMASTER),
			
			(val_sub, ":pos_y", ":spacing_roles"),
			## COLUMN 1 ## - Companion Portrait
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y_portrait"),
			(call_script, "script_gpu_create_portrait", "$cms_role_quartermaster", ":pos_x_portrait", ":pos_y_temp", 300, 0),
			
			## COLUMN 2 ## - Role Title: Companion Name, Description of role.
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_title"),
			(call_script, "script_gpu_create_text_label", "str_role_label_quartermaster", ":pos_x_title", ":pos_y_temp", role_obj_label_quartermaster, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_role_label_quartermaster", ":pos_x_title", ":pos_y_temp", role_obj_label_quartermaster, gpu_left), # Doubled for bold effect.
			# (call_script, "script_gpu_create_text_label", "str_role_label_quartermaster", ":pos_x_title", ":pos_y_temp", role_obj_label_quartermaster, gpu_left_with_outline),
			# (overlay_set_color, reg1, gpu_white),
			
			# ROLE -> CHARACTER SELECTION MENU BEGIN
			(store_add, ":pos_x_menu", ":pos_x_title", ":pos_x_menu_adj"), 	  (position_set_x, pos1, ":pos_x_menu"),
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_menu"), (position_set_y, pos1, ":pos_y_temp"),
			
			(create_combo_button_overlay, reg1),
			(overlay_set_position, reg1, pos1),
			(troop_set_slot, ROLE_OBJECTS, role_obj_menu_quartermaster, reg1),
			(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
			(assign, ":hero_slot", 0),
			(try_for_range, ":stack_num", 0, ":num_stacks"),
				(store_add, ":slot_pick", role_val_menu_troop_1, ":hero_slot"),
				(party_stack_get_troop_id,":troop_no","p_main_party",":stack_num"),
				(troop_is_hero, ":troop_no"),
				(try_begin),
					(eq, ":troop_no", "$cms_role_quartermaster"),
					(troop_set_slot, ROLE_OBJECTS, role_val_menu_quartermaster, ":hero_slot"),
				(try_end),
				(str_clear, s1),
				(str_store_troop_name, s1, ":troop_no"),
				(troop_set_slot, ROLE_OBJECTS, ":slot_pick", ":troop_no"),
				(try_begin),
					(ge, DEBUG_ROLE, 2),
					(assign, reg31, ":slot_pick"),
					(display_message, "@DEBUG (CMS): Added '{s1}' to character chooser menu.  Slot #{reg31}"),
				(try_end),
				(val_add, ":hero_slot", 1),
				(overlay_add_item, reg1, "@{s1}"),
			(try_end),
			(troop_get_slot, ":selected_profile", ROLE_OBJECTS, role_val_menu_quartermaster),
			(overlay_set_val, reg1, ":selected_profile"),
			(call_script, "script_gpu_resize_object", role_obj_menu_quartermaster, 75),
			# ROLE -> CHARACTER SELECTION MENU END
			
			# Description of role.
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_desc"),
			(store_add, ":pos_x_temp", ":pos_x_title", 0),
			(troop_get_type, reg21, "$cms_role_quartermaster"),
			(call_script, "script_gpu_create_text_label", "str_role_desc_quartermaster", ":pos_x_temp", ":pos_y_temp", role_obj_label_quartermaster_desc, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_quartermaster_desc, 75),
			# Requirements
			(val_sub, ":pos_y_temp", 50),
			(call_script, "script_gpu_create_text_label", "str_role_desc_quartermaster_reqs", ":pos_x_temp", ":pos_y_temp", role_obj_label_quartermaster_reqs, gpu_left),
			(overlay_set_color, reg1, gpu_blue),
			(call_script, "script_gpu_resize_object", role_obj_label_quartermaster_reqs, 75),
			# Double for bold effect.
			(call_script, "script_gpu_create_text_label", "str_role_desc_quartermaster_reqs", ":pos_x_temp", ":pos_y_temp", role_obj_label_quartermaster_reqs, gpu_left),
			(overlay_set_color, reg1, gpu_blue),
			(call_script, "script_gpu_resize_object", role_obj_label_quartermaster_reqs, 75),
			
			## COLUMN 3 ## - Reports
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y3_title"),
			(call_script, "script_gpu_create_text_label", "str_role_label_quartermaster_reports", ":pos_x_report", ":pos_y_temp", role_obj_label_quartermaster_report, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_role_label_quartermaster_reports", ":pos_x_report", ":pos_y_temp", role_obj_label_quartermaster_report, gpu_left), # Doubled for bold effect.
			# (call_script, "script_gpu_create_text_label", "str_role_label_quartermaster_reports", ":pos_x_report", ":pos_y_temp", role_obj_label_quartermaster_report, gpu_left_with_outline),
			# (overlay_set_color, reg1, gpu_white),
			
			# Our bags have X of Y spaces used.
			(store_free_inventory_capacity, ":space_free", "$cms_role_quartermaster"),
			(troop_get_inventory_capacity, ":space_max", "$cms_role_quartermaster"),
			(store_sub, ":space_used", ":space_max", ":space_free"),
			(assign, reg21, ":space_used"),
			(assign, reg22, ":space_max"),
			(val_sub, ":pos_y_temp", 22),
			(store_add, ":pos_x_temp", ":pos_x_report", 0),
			(call_script, "script_gpu_create_text_label", "str_role_label_qm_available_space", ":pos_x_temp", ":pos_y_temp", role_obj_label_quartermaster_space_used, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_quartermaster_space_used, 75),
			
			# We should be able to get X denars for our loot.
			(troop_get_inventory_capacity, ":capacity", "$cms_role_quartermaster"),
			(assign, ":earnings", 0),
			(assign, ":best_item_no", 0),
			(assign, ":best_item_value", 0),
			(try_for_range, ":i_slot", 9, ":capacity"),
				(troop_get_inventory_slot, ":item_no", "$cms_role_quartermaster", ":i_slot"),
				(ge, ":item_no", 1), # Valid item.
				(assign, ":continue", 1),
				(try_begin),
					(call_script, "script_cf_dws_item_in_a_weapon_set", "$cms_role_quartermaster", ":item_no"), # Prevent sale of weapon set gear.
					(assign, ":continue", 0),
				(try_end),
				(eq, ":continue", 1),
			
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
				(gt, ":item_value", ":best_item_value"),
				(assign, ":best_item_no", ":item_no"),
				(assign, ":best_item_value", ":item_value"),
			(try_end),

			(assign, reg21, ":earnings"),
			(val_sub, ":pos_y_temp", 15),
			(call_script, "script_gpu_create_text_label", "str_role_label_qm_loot_value", ":pos_x_temp", ":pos_y_temp", role_obj_label_quartermaster_loot_value, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_quartermaster_loot_value, 75),
			
			# Our most valuable item is worth X denars.
			(try_begin),
				(ge, ":best_item_no", 1),
				(str_store_item_name, s21, ":best_item_no"),
				(assign, reg21, ":best_item_value"),
				(val_sub, ":pos_y_temp", 15),
				(call_script, "script_gpu_create_text_label", "str_role_label_qm_best_item", ":pos_x_temp", ":pos_y_temp", role_obj_label_quartermaster_best_item, gpu_left),
				(call_script, "script_gpu_resize_object", role_obj_label_quartermaster_best_item, 75),
			(try_end),
			######## QUARTERMASTER : END ########
			
			######## JAILER / GAOLER : BEGIN ########
			(call_script, "script_cms_verify_party_role_filled", ROLE_JAILER),
			
			(val_sub, ":pos_y", ":spacing_roles"),
			## COLUMN 1 ## - Companion Portrait
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y_portrait"),
			(call_script, "script_gpu_create_portrait", "$cms_role_jailer", ":pos_x_portrait", ":pos_y_temp", 300, 0),
			
			## COLUMN 2 ## - Role Title: Companion Name, Description of role.
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_title"),
			(call_script, "script_gpu_create_text_label", "str_role_label_jailer", ":pos_x_title", ":pos_y_temp", role_obj_label_jailer, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_role_label_jailer", ":pos_x_title", ":pos_y_temp", role_obj_label_jailer, gpu_left), # Doubled for bold effect.
			
			# ROLE -> CHARACTER SELECTION MENU BEGIN
			(store_add, ":pos_x_menu", ":pos_x_title", ":pos_x_menu_adj"), 	  (position_set_x, pos1, ":pos_x_menu"),
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_menu"), (position_set_y, pos1, ":pos_y_temp"),
			
			(create_combo_button_overlay, reg1),
			(overlay_set_position, reg1, pos1),
			(troop_set_slot, ROLE_OBJECTS, role_obj_menu_jailer, reg1),
			(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
			(assign, ":hero_slot", 0),
			(try_for_range, ":stack_num", 0, ":num_stacks"),
				(store_add, ":slot_pick", role_val_menu_troop_1, ":hero_slot"),
				(party_stack_get_troop_id,":troop_no","p_main_party",":stack_num"),
				(troop_is_hero, ":troop_no"),
				(try_begin),
					(eq, ":troop_no", "$cms_role_jailer"),
					(troop_set_slot, ROLE_OBJECTS, role_val_menu_jailer, ":hero_slot"),
				(try_end),
				(str_clear, s1),
				(str_store_troop_name, s1, ":troop_no"),
				(troop_set_slot, ROLE_OBJECTS, ":slot_pick", ":troop_no"),
				(try_begin),
					(ge, DEBUG_ROLE, 2),
					(assign, reg31, ":slot_pick"),
					(display_message, "@DEBUG (CMS): Added '{s1}' to character chooser menu.  Slot #{reg31}"),
				(try_end),
				(val_add, ":hero_slot", 1),
				(overlay_add_item, reg1, "@{s1}"),
			(try_end),
			(troop_get_slot, ":selected_profile", ROLE_OBJECTS, role_val_menu_jailer),
			(overlay_set_val, reg1, ":selected_profile"),
			(call_script, "script_gpu_resize_object", role_obj_menu_jailer, 75),
			# ROLE -> CHARACTER SELECTION MENU END
			
			# Description of role.
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y2_desc"),
			(val_sub, ":pos_y_temp", 3), # Minor adjustment for this role only.
			(store_add, ":pos_x_temp", ":pos_x_title", 0),
			(troop_get_type, reg21, "$cms_role_jailer"),
			(call_script, "script_gpu_create_text_label", "str_role_desc_jailer", ":pos_x_temp", ":pos_y_temp", role_obj_label_jailer_desc, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_jailer_desc, 75),
			# Requirements
			(val_sub, ":pos_y_temp", 60),
			(call_script, "script_gpu_create_text_label", "str_role_desc_jailer_reqs", ":pos_x_temp", ":pos_y_temp", role_obj_label_jailer_reqs, gpu_left),
			(overlay_set_color, reg1, gpu_blue),
			(call_script, "script_gpu_resize_object", role_obj_label_jailer_reqs, 75),
			# Double for bold effect.
			(call_script, "script_gpu_create_text_label", "str_role_desc_jailer_reqs", ":pos_x_temp", ":pos_y_temp", role_obj_label_jailer_reqs, gpu_left),
			(overlay_set_color, reg1, gpu_blue),
			(call_script, "script_gpu_resize_object", role_obj_label_jailer_reqs, 75),
			
			## COLUMN 3 ## - Reports
			(store_add, ":pos_y_temp", ":pos_y", ":pos_y3_title"),
			(call_script, "script_gpu_create_text_label", "str_role_label_jailer_reports", ":pos_x_report", ":pos_y_temp", role_obj_label_jailer_report, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_role_label_jailer_reports", ":pos_x_report", ":pos_y_temp", role_obj_label_jailer_report, gpu_left), # Doubled for bold effect.
			# (call_script, "script_gpu_create_text_label", "str_role_label_jailer_reports", ":pos_x_report", ":pos_y_temp", role_obj_label_jailer_report, gpu_left_with_outline),
			# (overlay_set_color, reg1, gpu_white),
			
			# We are currently managing X prisoners.
			(party_get_num_prisoners, reg21, "p_main_party"),
			(try_begin),
				(gt, reg21, 0),
				(store_sub, reg22, reg21, 1),
				(str_store_string, s21, "str_role_label_jailer_prisoner_count"),
			(else_try),
				(str_store_string, s21, "str_role_label_jailer_no_prisoners"),
			(try_end),
			(val_sub, ":pos_y_temp", 22),
			(store_add, ":pos_x_temp", ":pos_x_report", 0),
			(call_script, "script_gpu_create_text_label", "str_role_label_blank_s21", ":pos_x_temp", ":pos_y_temp", role_obj_label_jailer_prisoner_count, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_jailer_prisoner_count, 75),
			
			# I estimate their value at X denars.
			(try_begin),
				(ge, reg21, 1), # You should have at least 1 prisoner to have a value.
				(party_get_num_prisoner_stacks, ":stack_limit", "p_main_party"),
				(assign, reg21, 0),
				(assign, "$g_talk_troop", ransom_brokers_begin), # So that an accurate prisoner value is displayed.
				(try_for_range, ":stack_no", 0, ":stack_limit"),
					(party_prisoner_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"), # Prevent companions, lords & player from being counted.
					(party_prisoner_stack_get_size, ":troop_count", "p_main_party", ":stack_no"),
					(call_script, "script_game_get_prisoner_price", ":troop_no"),
					(assign, ":troop_value", reg0),
					(store_mul, ":stack_value", ":troop_value", ":troop_count"),
					(val_add, reg21, ":stack_value"),
				(try_end),
				(val_sub, ":pos_y_temp", 15),
				(call_script, "script_gpu_create_text_label", "str_role_label_jailer_prisoner_value", ":pos_x_temp", ":pos_y_temp", role_obj_label_jailer_prisoner_value, gpu_left),
				(call_script, "script_gpu_resize_object", role_obj_label_jailer_prisoner_value, 75),
			(try_end),
			
			# The last town we visited with a slave trader was X.
			(try_begin),
				(is_between, "$cms_last_town_with_slaver", towns_begin, towns_end),
				(str_store_party_name, s22, "$cms_last_town_with_slaver"),
				(str_store_string, s21, "str_role_label_jailer_last_town"),
				(val_sub, ":pos_y_temp", 17),
			(else_try),
				(str_store_string, s21, "str_role_label_jailer_last_town_invalid"),
				(val_sub, ":pos_y_temp", 15),
			(try_end),
			(call_script, "script_gpu_create_text_label", "str_role_label_blank_s21", ":pos_x_temp", ":pos_y_temp", role_obj_label_jailer_last_town, gpu_left),
			(call_script, "script_gpu_resize_object", role_obj_label_jailer_last_town, 75),
			######## JAILER / GAOLER : END ########
			
			######## FARRIER : BEGIN ########
			######## FARRIER : END ########
			
		################ CONTAINER END ################	
		(set_container_overlay, -1),
		
		(presentation_set_duration, 999999),
    ]),

	(ti_on_presentation_event_state_change,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":value"),
			
			(try_begin),
				##### EXIT BUTTON #####
				(troop_slot_eq, ROLE_OBJECTS, role_obj_button_exit, ":object"),
				(presentation_set_duration, 0),
				(jump_to_menu, "$return_menu"),
				
			(else_try), 
				####### STOREKEEPER: CHARACTER SELECTOR #######
				(troop_slot_eq, ROLE_OBJECTS, role_obj_menu_storekeeper, ":object"),
				(store_add, ":troop_pick", role_val_menu_troop_1, ":value"),
				(troop_get_slot, ":new_person", ROLE_OBJECTS, ":troop_pick"),
				(try_begin),
					(call_script, "script_cf_cms_check_if_qualified_for_role", ":new_person", ROLE_STOREKEEPER),
					(troop_set_slot, ROLE_OBJECTS, role_val_menu_storekeeper, ":value"),
					(assign, ":old_person", "$cms_role_storekeeper"),
					(assign, "$cms_role_storekeeper", ":new_person"),
					(neq, ":old_person", "$cms_role_storekeeper"), # It doesn't hurt anything to continue, but just looks silly for no reason.
					(call_script, "script_cms_turnover_stores", "$cms_role_storekeeper", ":old_person", ROLE_STOREKEEPER),
					(str_store_troop_name, s21, ":old_person"),
					(str_store_troop_name, s22, "$cms_role_storekeeper"),
					(troop_get_type, reg21, ":old_person"),
					(display_message, "@{s21} has turned over {reg21?her:his} food stores to {s22}."),
				(try_end),
				## Automatically enable the auto-buying of food if a companion is selected.
				(try_begin),
					(neq, "$cms_role_storekeeper", "trp_player"),
					(eq, "$cms_enable_auto_buying", 0),
					(display_message, "@Automatic purchasing of food by your storekeeper has been enabled.", gpu_green),
					(assign, "$cms_enable_auto_buying", 1),
					## QUEST HOOK: qst_qp6_storekeeper_assignment
					(try_begin),
						(check_quest_active, "qst_qp6_storekeeper_assignment"),
						(quest_slot_eq, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 0),
						(quest_set_slot, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 1),
						(call_script, "script_qp6_storekeeper_assignment", floris_quest_update),
						(call_script, "script_qp6_storekeeper_assignment", floris_quest_victory_condition),
					(try_end),
				(try_end),
				## QUEST HOOK: qst_qp6_storekeeper_assignment
				(try_begin),
					(check_quest_active, "qst_qp6_storekeeper_assignment"),
					(is_between, "$cms_role_storekeeper", companions_begin, companions_end),
					(quest_slot_eq, "qst_qp6_storekeeper_assignment", slot_quest_stage_2_trigger_chance, 0),
					(quest_set_slot, "qst_qp6_storekeeper_assignment", slot_quest_stage_2_trigger_chance, 1),
					(call_script, "script_qp6_storekeeper_assignment", floris_quest_update),
					(call_script, "script_qp6_storekeeper_assignment", floris_quest_victory_condition),
				(try_end),
				(start_presentation, "prsnt_cms_party_roles"),
				
				
			(else_try), 
				####### QUARTERMASTER: CHARACTER SELECTOR #######
				(troop_slot_eq, ROLE_OBJECTS, role_obj_menu_quartermaster, ":object"),
				(store_add, ":troop_pick", role_val_menu_troop_1, ":value"),
				(troop_get_slot, ":new_person", ROLE_OBJECTS, ":troop_pick"),
				(try_begin),
					(call_script, "script_cf_cms_check_if_qualified_for_role", ":new_person", ROLE_QUARTERMASTER),
					(troop_set_slot, ROLE_OBJECTS, role_val_menu_quartermaster, ":value"),
					(assign, ":old_person", "$cms_role_quartermaster"),
					(assign, "$cms_role_quartermaster", ":new_person"),
					(neq, ":old_person", "$cms_role_quartermaster"), # It doesn't hurt anything to continue, but just looks silly for no reason.
					(call_script, "script_cms_turnover_stores", "$cms_role_quartermaster", ":old_person", ROLE_QUARTERMASTER),
					(str_store_troop_name, s21, ":old_person"),
					(str_store_troop_name, s22, "$cms_role_quartermaster"),
					(troop_get_type, reg21, ":old_person"),
					(display_message, "@{s21} has turned over {reg21?her:his} stored items to {s22}."),
				(try_end),
				## Automatically enable the auto-selling of goods if a companion is selected.
				(try_begin),
					(neq, "$cms_role_quartermaster", "trp_player"),
					(eq, "$cms_enable_auto_selling", 0),
					(display_message, "@Automatic selling of battlefield loot by your quartermaster has been enabled.", gpu_green),
					(assign, "$cms_enable_auto_selling", 1),
					## QUEST HOOK: qst_qp6_quartermaster_assignment
					(try_begin),
						(check_quest_active, "qst_qp6_quartermaster_assignment"),
						(quest_slot_eq, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 0),
						(quest_set_slot, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 1),
						(call_script, "script_qp6_quartermaster_assignment", floris_quest_update),
						(call_script, "script_qp6_quartermaster_assignment", floris_quest_victory_condition),
					(try_end),
				(try_end),
				## QUEST HOOK: qst_qp6_quartermaster_assignment
				(try_begin),
					(check_quest_active, "qst_qp6_quartermaster_assignment"),
					(is_between, "$cms_role_quartermaster", companions_begin, companions_end),
					(quest_slot_eq, "qst_qp6_quartermaster_assignment", slot_quest_stage_2_trigger_chance, 0),
					(quest_set_slot, "qst_qp6_quartermaster_assignment", slot_quest_stage_2_trigger_chance, 1),
					(call_script, "script_qp6_quartermaster_assignment", floris_quest_update),
					(call_script, "script_qp6_quartermaster_assignment", floris_quest_victory_condition),
				(try_end),
				(start_presentation, "prsnt_cms_party_roles"),
				
			(else_try), 
				####### JAILER: CHARACTER SELECTOR #######
				(troop_slot_eq, ROLE_OBJECTS, role_obj_menu_jailer, ":object"),
				(store_add, ":troop_pick", role_val_menu_troop_1, ":value"),
				(troop_get_slot, ":new_person", ROLE_OBJECTS, ":troop_pick"),
				(try_begin),
					(call_script, "script_cf_cms_check_if_qualified_for_role", ":new_person", ROLE_JAILER),
					(troop_set_slot, ROLE_OBJECTS, role_val_menu_jailer, ":value"),
					(assign, ":old_person", "$cms_role_jailer"),
					(assign, "$cms_role_jailer", ":new_person"),
					(neq, ":old_person", "$cms_role_jailer"), # It doesn't hurt anything to continue, but just looks silly for no reason.
					(call_script, "script_cms_turnover_stores", "$cms_role_jailer", ":old_person", ROLE_JAILER),
					(str_store_troop_name, s22, "$cms_role_jailer"),
					(display_message, "@{s22} has assumed the role as party gaoler."),
				(try_end),
				## QUEST HOOK: qst_qp6_jailer_assignment
				(try_begin),
					(check_quest_active, "qst_qp6_jailer_assignment"),
					(is_between, "$cms_role_jailer", companions_begin, companions_end),
					(quest_slot_eq, "qst_qp6_jailer_assignment", slot_quest_stage_1_trigger_chance, 0),
					(quest_set_slot, "qst_qp6_jailer_assignment", slot_quest_stage_1_trigger_chance, 1),
					(call_script, "script_qp6_jailer_assignment", floris_quest_update),
					(call_script, "script_qp6_jailer_assignment", floris_quest_victory_condition),
				(try_end),
				(start_presentation, "prsnt_cms_party_roles"),
				
			(else_try),
				####### STOREKEEPER: REDIRECT TO SHOPPING LIST #######
				(troop_slot_eq, ROLE_OBJECTS, role_obj_button_shopping_list, ":object"),
				## WINDYPLAINS+ ## - Allow switching between shopping list & party role screens.
				(presentation_set_duration, 0),
				(assign, "$cms_display", CMS_MODE_SHOPPING_LIST),
				(jump_to_menu, "mnu_cms_switch_modes"),
				## WINDYPLAINS- ##
			
			(else_try),
				####### STOREKEEPER: CHECKBOX - AUTO-FOOD PURCHASING #######
				(troop_slot_eq, ROLE_OBJECTS, role_obj_checkbox_storekeeper_enable, ":object"),
				(assign, "$cms_enable_auto_buying", ":value"),
				(troop_set_slot, ROLE_OBJECTS, role_val_checkbox_storekeeper_enable, ":value"),
				## QUEST HOOK: qst_qp6_storekeeper_assignment
				(try_begin),
					(check_quest_active, "qst_qp6_storekeeper_assignment"),
					(eq, "$cms_enable_auto_buying", 1),
					(quest_slot_eq, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 0),
					(quest_set_slot, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 1),
					(call_script, "script_qp6_storekeeper_assignment", floris_quest_update),
					(call_script, "script_qp6_storekeeper_assignment", floris_quest_victory_condition),
				(else_try),
					(check_quest_active, "qst_qp6_storekeeper_assignment"),
					(eq, "$cms_enable_auto_buying", 0),
					(quest_slot_eq, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 2),
					(quest_set_slot, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 0),
					(str_store_string, s1, "@Objecive - Enable the Storekeeper purchasing option."),
					(add_quest_note_from_sreg, "qst_qp6_storekeeper_assignment", 3, s1, 0), # Enabling Storekeeper Purchasing option.
				(try_end),
				
			(else_try),
				####### QUARTERMASTER: CHECKBOX - AUTO-SELL LOOT #######
				(troop_slot_eq, ROLE_OBJECTS, role_obj_checkbox_quartermaster_enable, ":object"),
				(assign, "$cms_enable_auto_selling", ":value"),
				(troop_set_slot, ROLE_OBJECTS, role_val_checkbox_quartermaster_enable, ":value"),
				## QUEST HOOK: qst_qp6_quartermaster_assignment
				(try_begin),
					(check_quest_active, "qst_qp6_quartermaster_assignment"),
					(eq, "$cms_enable_auto_selling", 1),
					(quest_slot_eq, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 0),
					(quest_set_slot, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 1),
					(call_script, "script_qp6_quartermaster_assignment", floris_quest_update),
					(call_script, "script_qp6_quartermaster_assignment", floris_quest_victory_condition),
				(else_try),
					(check_quest_active, "qst_qp6_quartermaster_assignment"),
					(eq, "$cms_enable_auto_selling", 0),
					(quest_slot_eq, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 2),
					(quest_set_slot, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 0),
					(str_store_string, s1, "@Objecive - Enable the Quartermaster auto-selling option."),
					(add_quest_note_from_sreg, "qst_qp6_quartermaster_assignment", 3, s1, 0), # Enabling Storekeeper Purchasing option.
				(try_end),
				
			(try_end),
			
		]),
  ]),
  
  ## CUSTOM COMMANDER (auto buying of food).  Credit: rubik
  ("shopping_list_of_food", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
        
        ## back
        (create_game_button_overlay, "$g_presentation_obj_1", "@Done"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_1", pos1),

        ## buy foos automaticly when leaving
        (create_text_overlay, reg0, "@Purchase food automatically when leaving:", tf_vertical_align_center),
        (position_set_x, pos1, 150),
        (position_set_y, pos1, 690),
        (overlay_set_position, reg0, pos1),

        (create_check_box_overlay, "$g_presentation_obj_2", "mesh_checkbox_off", "mesh_checkbox_on"),
        (position_set_x, pos1, 600),
        (position_set_y, pos1, 682),
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        #(overlay_set_val, "$g_presentation_obj_2", "$g_buy_foods_when_leaving"),
		(overlay_set_val, "$g_presentation_obj_2", "$cms_enable_auto_buying"), # cms_enable_auto_buying
		
        (assign, ":pos_x", 60),
        (assign, ":pos_y", 550),
        (try_for_range, ":cur_food", food_begin, food_end),
          # frame
          (create_mesh_overlay, reg1, "mesh_inv_slot"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, reg1, pos1),
          (position_set_x, pos1, ":pos_x"),
          (position_set_y, pos1, ":pos_y"),
          (overlay_set_position, reg1, pos1),
          # back ground
          # (create_mesh_overlay, reg1, "mesh_mp_inventory_choose"),
          # (position_set_x, pos1, 640),
          # (position_set_y, pos1, 640),
          # (overlay_set_size, reg1, pos1),
          # (position_set_x, pos1, ":pos_x"),
          # (position_set_y, pos1, ":pos_y"),
          # (overlay_set_position, reg1, pos1),
          # item overlay
          (troop_set_slot, "trp_temp_array_a", ":cur_food", reg1),
          (create_mesh_overlay_with_item_id, reg1, ":cur_food"),
          (position_set_x, pos1, 800),
          (position_set_y, pos1, 800),
          (overlay_set_size, reg1, pos1),
          (store_add, ":item_x", ":pos_x", 40),
          (store_add, ":item_y", ":pos_y", 40),
          (position_set_x, pos1, ":item_x"),
          (position_set_y, pos1, ":item_y"),
          (overlay_set_position, reg1, pos1),
          (troop_set_slot, "trp_temp_array_b", ":cur_food", reg1),
          # text *
          (create_text_overlay, reg1, "@*", tf_center_justify|tf_vertical_align_center),
          (store_add, ":text_x", ":pos_x", 100),
          (store_add, ":text_y", ":pos_y", 40),
          (position_set_x, pos1, ":text_x"),
          (position_set_y, pos1, ":text_y"),
          (overlay_set_position, reg1, pos1),
          # number_box
          (create_number_box_overlay, reg1, 0, 7),
          (store_add, ":number_box_x", ":pos_x", 115),
          (store_add, ":number_box_y", ":pos_y", 30),
          (position_set_x, pos1, ":number_box_x"),
          (position_set_y, pos1, ":number_box_y"),
          (overlay_set_position, reg1, pos1),
          (item_get_slot, ":food_portion", ":cur_food", slot_item_food_portion),
          (overlay_set_val, reg1, ":food_portion"),
          (troop_set_slot, "trp_temp_array_c", ":cur_food", reg1),
          # next
          (val_add, ":pos_x", 240),
          (try_begin),
            (eq, ":pos_x", 1020),
            (assign, ":pos_x", 60),
            (val_sub, ":pos_y", 120),
          (try_end),
        (try_end),

        ####### mouse fix pos system #######
        #(call_script, "script_mouse_fix_pos_ready"),
        ####### mouse fix pos system #######
		
		## QUEST HOOK: qst_qp6_storekeeper_assignment
		(try_begin),
			(check_quest_active, "qst_qp6_storekeeper_assignment"),
			(quest_slot_eq, "qst_qp6_storekeeper_assignment", slot_quest_stage_3_trigger_chance, 0),
			(quest_set_slot, "qst_qp6_storekeeper_assignment", slot_quest_stage_3_trigger_chance, 1),
			(call_script, "script_qp6_storekeeper_assignment", floris_quest_update),
			(call_script, "script_qp6_storekeeper_assignment", floris_quest_victory_condition),
		(try_end),
      ]),

    #(ti_on_presentation_run,
      #[
        ####### mouse fix pos system #######
        #(call_script, "script_mouse_fix_pos_run"),
        ####### mouse fix pos system #######
    #]),

    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),

      (try_begin),
        (eq, ":enter_leave", 0),
        (try_for_range, ":cur_food", food_begin, food_end),
          (troop_slot_eq, "trp_temp_array_a", ":cur_food", ":object"),
          (troop_get_slot, ":target_obj", "trp_temp_array_b", ":cur_food"),
          (overlay_get_position, pos0, ":target_obj"),
          (show_item_details, ":cur_food", pos0, 100),
          (assign, "$g_current_opened_item_details", ":cur_food"),
        (try_end),
      (else_try),
        (try_for_range, ":cur_food", food_begin, food_end),
          (troop_slot_eq, "trp_temp_array_a", ":cur_food", ":object"),
          (try_begin),
            (eq, "$g_current_opened_item_details", ":cur_food"),
            (close_item_details),
          (try_end),
        (try_end),
      (try_end),
    ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_for_range, ":cur_food", food_begin, food_end),
          (troop_slot_eq, "trp_temp_array_c", ":cur_food", ":object"),
          (item_set_slot, ":cur_food", slot_item_food_portion, ":value"),
        (try_end),

        (try_begin),
          (eq, ":object", "$g_presentation_obj_2"),
          (assign, "$g_buy_foods_when_leaving", ":value"),
		  (assign, "$cms_enable_auto_buying", ":value"),
        (else_try),
          (eq, ":object", "$g_presentation_obj_1"),
		  ## WINDYPLAINS+ ## - Allow switching between shopping list & party role screens.
          (presentation_set_duration, 0),
		  (assign, "$cms_display", CMS_MODE_PARTY_ROLES),
		  (jump_to_menu, "mnu_cms_switch_modes"),
		  ## WINDYPLAINS- ##
        (try_end),
    ]),
  ]),
]
	
def modmerge_presentations(orig_presentations, check_duplicates = False):
    if( not check_duplicates ):
        orig_presentations.extend(presentations) # Use this only if there are no replacements (i.e. no duplicated item names)
    else:
    # Use the following loop to replace existing entries with same id
        for i in range (0,len(presentations)-1):
          find_index = find_object(orig_presentations, presentations[i][0]); # find_object is from header_common.py
          if( find_index == -1 ):
            orig_presentations.append(presentations[i])
          else:
            orig_presentations[find_index] = presentations[i]

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "presentations"
        orig_presentations = var_set[var_name_1]
        modmerge_presentations(orig_presentations)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)