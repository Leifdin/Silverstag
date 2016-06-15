# Garrison Recruitment & Training by Windyplains

from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
from header_items import *
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
#####                                                    GARRISON                                                     #####
###########################################################################################################################

("garrison_general", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_grt_create_mode_switching_buttons"),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			# OBJ - Warning note.
			(call_script, "script_gpu_create_text_label", "str_grt_recruitment_header", 500, 635, 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			############################
			### BACKGROUND CONTAINER ###
			############################
			
			(assign, ":y_bottom", 80),
			(assign, ":x_left",  220),
			(assign, ":x_width", 725),
			(assign, ":y_width", 515),
			(assign, ":troop_step", 170),
			
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", hub_obj_container_2),
				(assign, ":pos_y", 0),
				
				## COUNT - PARTY MEMBERS
				(party_get_num_companion_stacks, ":stack_capacity", "$current_town"),
				(try_for_range, ":stack_no", 0, ":stack_capacity"),
					(lt, ":pos_y", MAXIMUM_TROOP_RECORDS),
					(party_stack_get_troop_id, ":troop_no", "$current_town", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"),
					(val_add, ":pos_y", 1),
				(try_end),
				
				# Set our initial position.
				(val_mul, ":pos_y", ":troop_step"),
				
				################## DISPLAY ###################
				(assign, ":record", 0),
				
				## DISPLAY - PARTY MEMBERS
				(party_get_num_companion_stacks, ":stack_capacity", "$current_town"),
				(try_for_range, ":stack_no", 0, ":stack_capacity"),
					(lt, ":record", MAXIMUM_TROOP_RECORDS),
					(party_stack_get_troop_id, ":troop_no", "$current_town", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"),
					(call_script, "script_grt_garrison_troop_get_info", ":troop_no", ":pos_y"),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
			(set_container_overlay, -1),
			
		]),
	
    (ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(assign, "$grt_mode", GARRISON_MODE_GENERAL),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_grt_handle_mode_switching_buttons", ":object", ":value"),
		
      ]),
    ]),
	
	
###########################################################################################################################
#####                                                 CURRENT QUEUE                                                   #####
###########################################################################################################################

("garrison_queue", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_grt_create_mode_switching_buttons"),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			# OBJ - Warning note.
			# (call_script, "script_gpu_create_text_label", "str_hub_label_construction", 500, 635, 0, gpu_center),
			# (call_script, "script_gpu_resize_object", 0, 75),
			
			#########################################
			###           CURRENT QUEUE           ###
			#########################################
			# Slot, Troop Name, Quantity, Recruit Type, Cost Per Troop, Total Cost, Est. Hired Next Week
			
			# Margins
			(assign, ":x_slot",        50),  # Centered
			(assign, ":x_troop_no",    75),  # Left
			(assign, ":x_quantity",   300),  # Center
			(assign, ":x_recruit",    360),  # Left
			(assign, ":x_cost",       515),  # Right
			(assign, ":x_total_cost", 610),  # Right
			
			(assign, ":y_bottom", 340),
			(assign, ":x_left",  220),
			(assign, ":x_width", 725),
			(assign, ":y_width", 50),
			
			# Title Offsets
			(assign, ":x_offset_titles", ":x_left"),
			(store_add, ":x_slot_t",       ":x_offset_titles", ":x_slot"),  # Centered
			(store_add, ":x_troop_no_t",   ":x_offset_titles", ":x_troop_no"),  # Left
			(store_add, ":x_quantity_t",   ":x_offset_titles", ":x_quantity"),  # Center
			(store_add, ":x_recruit_t",    ":x_offset_titles", ":x_recruit"),  # Left
			(store_add, ":x_cost_t",       ":x_offset_titles", ":x_cost"),  # Right
			(store_add, ":x_total_cost_t", ":x_offset_titles", ":x_total_cost"),  # Right
			
			### QUEUE HEADER
			(assign, ":y_titles", 400),
			(assign, ":text_size", 75),
			
			(call_script, "script_gpu_create_text_label", "str_grt_queue_title", 550, ":y_titles", 0, gpu_center),
			(call_script, "script_gpu_create_text_label", "str_grt_queue_title", 550, ":y_titles", 0, gpu_center),
			# (overlay_set_color, reg1, gpu_blue),
			(val_sub, ":y_titles", 30),
			## TITLE - SLOT
			(str_store_string, s21, "@Slot"),
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_slot_t", ":y_titles", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_slot_t", ":y_titles", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			
			## TITLE - TROOP NAME
			(str_store_string, s21, "@Troop Type"),
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_troop_no_t", ":y_titles", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_troop_no_t", ":y_titles", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			
			## TITLE - QUANTITY
			(str_store_string, s21, "@Requested"),
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_quantity_t", ":y_titles", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_quantity_t", ":y_titles", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			
			## TITLE - RECRUIT TYPE
			(str_store_string, s21, "@Recruit"),
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_recruit_t", ":y_titles", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_recruit_t", ":y_titles", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			
			## TITLE - COST PER TROOP
			(str_store_string, s21, "@Cost"),
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_cost_t", ":y_titles", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_cost_t", ":y_titles", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			
			## TITLE - TOTAL COST
			(str_store_string, s21, "@Total Cost"),
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_total_cost_t", ":y_titles", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_total_cost_t", ":y_titles", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, ":text_size"),
			
			
			(val_sub, ":y_titles", 20),
			(store_sub, ":x_width_temp", ":x_width", 50),
			(store_add, ":x_header_line", ":x_offset_titles", 25),
			(call_script, "script_gpu_draw_line", ":x_width_temp", 2, ":x_header_line", ":y_titles", gpu_gray),
			
			
			(assign, ":y_bottom", 80),
			(assign, ":y_width", 255),
			(assign, ":line_step", 25),
			
			# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), ## SPACING - REMOVE
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt_obj_container_2),
				(str_clear, s21),
				(val_sub, ":y_width", 10),
				(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_slot", ":y_width", 0, gpu_center),
			
				### INFO CYCLE BEGINS
				(call_script, "script_grt_get_total_troop_types", "$current_town"),
				(assign, ":pos_y", 250),
				# (store_mul, ":pos_y", reg1, ":line_step"),
				# (val_add, ":pos_y", 190),
				
				(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
					(neg|party_slot_eq, "$current_town", ":queue_slot", -1),
					(neg|party_slot_eq, "$current_town", ":queue_slot", 0),
					
					## TITLE - SLOT
					(store_sub, reg21, ":queue_slot", slot_party_queue_slot_id_begin),
					(val_add, reg21, 1),
					(str_store_string, s21, "@#{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_slot", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, ":text_size"),
					
					## TITLE - TROOP NAME
					(party_get_slot, ":troop_no", "$current_town", ":queue_slot"),
					(str_store_troop_name, s21, ":troop_no"),
					(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_troop_no", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, ":text_size"),
					
					## TITLE - QUANTITY
					(call_script, "script_grt_get_queue_count_for_troop", "$current_town", ":troop_no"),
					(assign, ":quantity", reg1),
					(str_store_string, s21, "@{reg1} requested"),
					(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_quantity", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, ":text_size"),
					
					## TITLE - RECRUIT TYPE
					(call_script, "script_hub_get_troop_recruit_type_for_buyer", ":troop_no", "trp_player"), # returns type to s1
					(str_store_string, s21, s1),
					(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_recruit", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, ":text_size"),
					
					## TITLE - COST PER TROOP
					(call_script, "script_hub_get_purchase_price_for_troop", "$current_town", ":troop_no", "trp_player"), # Returns reg1 (price), reg2 (discount)
					(call_script, "script_grt_apply_hiring_bonuses", "$current_town", reg1),
					(assign, ":cost_per_troop", reg1),
					(str_store_string, s21, "@{reg1} denars"),
					(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_cost", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, ":text_size"),
					
					## TITLE - TOTAL COST
					(store_mul, reg21, ":cost_per_troop", ":quantity"),
					(str_store_string, s21, "@{reg21} denars"),
					(call_script, "script_gpu_create_text_label", "str_grt_s21", ":x_total_cost", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, ":text_size"),
					
					(val_sub, ":pos_y", ":line_step"),
				(try_end),
				
			(set_container_overlay, -1),
			
			#########################################
			###          ESTIMATION BOX           ###
			#########################################
			## OBJ - TEXT - ESTIMATED HIRES
			(call_script, "script_gpu_create_text_label", "str_grt_estimated_hires", 500, 610, 0, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_grt_estimated_hires", 500, 610, 0, gpu_left),
			# (overlay_set_color, reg1, gpu_blue),
			(call_script, "script_gpu_draw_line", 400, 2, 500, 595, gpu_gray),
			
			## OBJ - CONTAINER - ESTIMATED HIRES
			# (call_script, "script_gpu_draw_line", 400, 125, 500, 430, gpu_white), ## SPACING - REMOVE
			(call_script, "script_gpu_container_heading", 500, 430, 400, 160, grt_obj_container_3),
				(try_begin),
					(party_slot_eq, "$current_town", slot_center_recruiting, 1), # Recruiting is enabled.
					(call_script, "script_grt_process_weekly_hiring", "$current_town", GRT_QUEUE_PRINT),
					(str_store_string, s21, s49),
				(else_try),
					(party_slot_eq, "$current_town", slot_center_recruiting, 0), # Recruiting is disabled.
					(str_store_string, s21, "@Garrison recruitment has been disabled in this location."),
				(try_end),
				(call_script, "script_gpu_create_text_label", "str_grt_s21", 0, 125, grt3_obj_estimation_field, gpu_left),
				(call_script, "script_gpu_resize_object", grt3_obj_estimation_field, 75),
			(set_container_overlay, -1),
			
			#########################################
			###        ALLOCATION & FOCUS         ###
			#########################################
			## OBJ - CHECKBOX - ENABLE GARRISON RECRUIMENT
			(call_script, "script_gpu_create_checkbox", 240, 590, "str_grt_recruitment_enable", grt2_obj_checkbox_enable_recruiting, grt2_val_checkbox_enable_recruiting),
			(party_get_slot, ":setting", "$current_town", slot_center_recruiting),
			(overlay_set_val, reg1, ":setting"),
			
			## OBJ - MENU / LABEL - BUDGET TOGGLE
			(call_script, "script_gpu_create_text_label", "str_grt_budget_spending", 247, 555, 0, gpu_left),
			(position_set_x, pos1, 360),
			(position_set_y, pos1, 515),
			(create_combo_button_overlay, reg1),
			(troop_set_slot, GRT_OBJECTS, grt2_obj_menu_budget_type, reg1),
			(overlay_set_position, reg1, pos1),
			(overlay_add_item, reg1, "@Split Budget"),
			(overlay_add_item, reg1, "@Focused Budget"),
			(party_get_slot, ":option_setting", "$current_town", slot_party_queue_progression),
			(overlay_set_val, reg1, ":option_setting"),
			(call_script, "script_gpu_resize_object", grt2_obj_menu_budget_type, 75),
			
			#######################################
			###   GARRISON RECRUITMENT SLIDER   ###
			#######################################
			
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"), # Secondary block in the event player views this in cheat mode.
				
				(assign, ":pos_x", 330),
				(store_sub, ":x_left", ":pos_x", 90),
				(store_sub, ":x_center", ":pos_x", 15),
				(assign, ":pos_y", 475),
				
				(str_store_string, s21, "@Recruiting Budget"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_center),
				(val_sub, ":pos_y", 25),
				(party_get_slot, ":garrison_budget", "$current_town", slot_party_queue_budget),
				(assign, reg21, ":garrison_budget"),
				(str_store_string, s21, "@{reg21} Denars"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", grt3_obj_text_recruiting_changes, gpu_center),
				(call_script, "script_gpu_resize_object", grt3_obj_text_recruiting_changes, 75),
				(val_sub, ":pos_y", 40),
				# Create the slider.
				(call_script, "script_gpu_create_slider", 0, 5000, ":x_left", ":pos_y", grt3_obj_slider_garrison_recruiting, grt3_val_slider_garrison_recruiting),
				(call_script, "script_gpu_resize_object", grt3_obj_slider_garrison_recruiting, 75),
				(overlay_set_val, reg1, ":garrison_budget"),
				(val_sub, ":pos_y", 25),
				(str_store_string, s21, "@Apply"),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":x_center", ":pos_y", grt3_obj_button_recruiting_apply), # Treasury Deposit
				(call_script, "script_gpu_resize_object", grt3_obj_button_recruiting_apply, 75),
				(overlay_set_display, reg1, 0),
			(try_end),
		]),
	
    (ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(assign, "$grt_mode", GARRISON_MODE_GENERAL),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_grt_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),
			### MENU - BUDGET SPENDING TYPE
			(troop_slot_eq, GRT_OBJECTS, grt2_obj_menu_budget_type, ":object"),
			(party_set_slot, "$current_town", slot_party_queue_progression, ":value"),
			## TODO: Trigger update of estimation field.
			(try_begin),
				(party_slot_eq, "$current_town", slot_center_recruiting, 1), # Recruiting is enabled.
				(call_script, "script_grt_process_weekly_hiring", "$current_town", GRT_QUEUE_PRINT),
				(str_store_string, s21, s49),
			(else_try),
				(party_slot_eq, "$current_town", slot_center_recruiting, 0), # Recruiting is disabled.
				(str_store_string, s21, "@Garrison recruitment has been disabled in this location."),
			(try_end),
			(troop_get_slot, ":obj_no", GRT_OBJECTS, grt3_obj_estimation_field),
			(overlay_set_text, ":obj_no", s21),
			
		(else_try),
			### CHECKBOX - GARRISON RECRUITING ENABLE / DISABLE
			(troop_slot_eq, GRT_OBJECTS, grt2_obj_checkbox_enable_recruiting, ":object"),
			(party_set_slot, "$current_town", slot_center_recruiting, ":value"),
			(start_presentation, "prsnt_garrison_queue"),
			
		(else_try),
			### BUTTON - ADVANCE 1 WEEK (DEBUGGING)
			(troop_slot_eq, GRT_OBJECTS, grt_obj_button_debug_advance, ":object"),
			(party_slot_eq, "$current_town", slot_center_recruiting, 1), # We're recruiting to the garrison.
			(try_begin),
				(ge, DEBUG_GARRISON, 2),
				(call_script, "script_grt_process_weekly_hiring", "$current_town", GRT_QUEUE_PROCESS),
				(display_message, "@DEBUG (GRT): This is intentionally not costing you anything.", gpu_debug),
				(start_presentation, "prsnt_garrison_queue"),
			(else_try),
				(ge, DEBUG_GARRISON, 1),
				(party_get_slot, ":budget_recruitment", "$current_town", slot_party_queue_budget),
				(call_script, "script_cf_diplomacy_treasury_verify_funds", ":budget_recruitment", "$current_town", FUND_FROM_TREASURY, TREASURY_FUNDS_AVAILABLE), # diplomacy_scripts.py
				(call_script, "script_diplomacy_treasury_withdraw_funds", ":budget_recruitment", "$current_town", FUND_FROM_TREASURY), # diplomacy_scripts.py
				(call_script, "script_grt_process_weekly_hiring", "$current_town", GRT_QUEUE_PROCESS),
				(start_presentation, "prsnt_garrison_queue"),
			(try_end),
			
		(else_try),
			### SLIDER - GARRISON RECRUITMENT ###
			(troop_slot_eq, GRT_OBJECTS, grt3_obj_slider_garrison_recruiting, ":object"),
			(troop_set_slot, GRT_OBJECTS, grt3_val_slider_garrison_recruiting, ":value"),
			(overlay_set_val, ":object", ":value"),
			(troop_get_slot, ":obj_label", GRT_OBJECTS, grt3_obj_text_recruiting_changes),
			(assign, reg21, ":value"),
			(str_store_string, s21, "@{reg21} Denars"),
			(overlay_set_text, ":obj_label", "str_grt_s21"),
			# Display Apply Button
			(troop_get_slot, ":obj_apply", GRT_OBJECTS, grt3_obj_button_recruiting_apply),
			(overlay_set_display, ":obj_apply", 1),
			
		(else_try),
			### BUTTON - GARRISON RECRUITMENT BUDGET APPLY ###
			(troop_slot_eq, GRT_OBJECTS, grt3_obj_button_recruiting_apply, ":object"),
			(troop_get_slot, ":setting", GRT_OBJECTS, grt3_val_slider_garrison_recruiting),
			(party_set_slot, "$current_town", slot_party_queue_budget, ":setting"),
			# Enable garrison recruiting if a value other than 0 is set.
			(try_begin),
				(ge, ":setting", 1),
				(try_begin),
					(party_slot_eq, "$current_town", slot_center_recruiting, 0),
					(str_store_party_name, s21, "$current_town"),
					(display_message, "@Garrison recruitment in {s21} has now been enabled.", gpu_green),
				(try_end),
				(party_set_slot, "$current_town", slot_center_recruiting, 1), # Enable garrison recruiting.
			(try_end),
			(start_presentation, "prsnt_garrison_queue"),
			
		(try_end),
		
      ]),
    ]),	
	
	
###########################################################################################################################
#####                                              GARRISON RECRUITMENT                                               #####
###########################################################################################################################

("garrison_recruitment", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_grt_create_mode_switching_buttons"),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			
			##########################
			### AVAILABLE RECRUITS ###
			##########################
			(try_begin),
				(party_slot_eq, "$current_town", slot_party_type, spt_town),
				(assign, ":spread", 170),
			(else_try),
				(assign, ":spread", 200),
			(try_end),
			(assign, ":pos_x", 300),
			
			# OBJ - Available nobles.
			(party_get_slot, reg21, "$current_town", slot_center_veteran_pool),
			(call_script, "script_gpu_create_text_label", "str_hub_available_nobles", ":pos_x", 625, 0, gpu_center),
			(try_begin),
				(party_slot_eq, "$current_town", slot_party_type, spt_town),
				(val_add, ":pos_x", ":spread"),
				# OBJ - Available mercenaries.
				(party_get_slot, reg21, "$current_town", slot_center_mercenary_pool_player),
				(call_script, "script_gpu_create_text_label", "str_hub_available_mercenaries", ":pos_x", 625, 0, gpu_center),
			(try_end),
			# OBJ - Available peasants.
			(val_add, ":pos_x", ":spread"),
			(party_get_slot, reg21, "$current_town", slot_center_volunteer_troop_amount),
			(call_script, "script_gpu_create_text_label", "str_hub_available_peasants", ":pos_x", 625, 0, gpu_center),
			# OBJ - Available mounts.
			(val_add, ":pos_x", ":spread"),
			(party_get_slot, reg21, "$current_town", slot_center_horse_pool_player),
			(call_script, "script_gpu_create_text_label", "str_hub_available_mounts", ":pos_x", 625, 0, gpu_center),
			
			############################
			### BACKGROUND CONTAINER ###
			############################
			
			(assign, ":y_bottom", 80),
			(assign, ":x_left",  220),
			(assign, ":x_width", 725),
			(assign, ":y_width", 515),
			(assign, ":troop_step", 170),
			
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", hub_obj_container_2),
				### QUALIFICATION SCRIPT : START ###
				
				### QUALIFICATION SCRIPT : STOP ###
				
				(party_get_slot, ":culture", "$current_town", slot_center_culture),
				
				## FACTION TROOPS
				(try_begin),
					(eq, ":culture", "fac_culture_player"), # Player Custom Faction
					(assign, ":lower_bound", player_troops_begin),
					(assign, ":upper_bound", player_troops_end),
				(else_try),
					(eq, ":culture", "fac_culture_1"), # Swadia
					(assign, ":lower_bound", swadia_troops_begin),
					(assign, ":upper_bound", swadia_troops_end),
				(else_try),
					(eq, ":culture", "fac_culture_2"), # Vaegirs
					(assign, ":lower_bound", vaegir_troops_begin),
					(assign, ":upper_bound", vaegir_troops_end),
				(else_try),
					(eq, ":culture", "fac_culture_3"), # Khergits
					(assign, ":lower_bound", khergit_troops_begin),
					(assign, ":upper_bound", khergit_troops_end),
				(else_try),
					(eq, ":culture", "fac_culture_4"), # Nords
					(assign, ":lower_bound", nord_troops_begin),
					(assign, ":upper_bound", nord_troops_end),
				(else_try),
					(eq, ":culture", "fac_culture_5"), # Rhodoks
					(assign, ":lower_bound", rhodok_troops_begin),
					(assign, ":upper_bound", rhodok_troops_end),
				(else_try),
					(eq, ":culture", "fac_culture_6"), # Sarranid
					(assign, ":lower_bound", sarranid_troops_begin),
					(assign, ":upper_bound", sarranid_troops_end),
				(try_end),
				
				(assign, ":pos_y", 0),
				
				## COUNT - FACTION TROOPS
				(try_for_range, ":troop_no", ":lower_bound", ":upper_bound"),
					(lt, ":pos_y", MAXIMUM_TROOP_RECORDS),
					## FILTER+ - REMOVE UNIQUES
					(assign, ":pass", 1),
					(try_begin),
						(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION),
						(assign, ":pass", 0),
					(else_try),
						(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION_UPGRADE),
						(assign, ":pass", 0),
					(try_end),
					(eq, ":pass", 1),
					## FILTER- - REMOVE UNIQUES
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(val_add, ":pos_y", 1),
					### DIAGNOSTIC ###
					(ge, DEBUG_RECRUITMENT, 1),
					(assign, reg31, ":pos_y"),
					(str_store_troop_name, s31, ":troop_no"),
					(display_message, "@DEBUG: #{reg31} - {s31}", gpu_green),
				(try_end),
				
				# ## COUNT - UNIQUE TROOPS
				# (try_for_range, ":troop_no", unique_troops_begin, unique_troops_end),
					# (lt, ":pos_y", MAXIMUM_TROOP_RECORDS),
					# (call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					# (val_add, ":pos_y", 1),
					# ### DIAGNOSTIC ###
					# (ge, DEBUG_RECRUITMENT, 1),
					# (assign, reg31, ":pos_y"),
					# (str_store_troop_name, s31, ":troop_no"),
					# (display_message, "@DEBUG: #{reg31} - {s31}", gpu_green),
				# (try_end),
				
				## COUNT - UNIQUE TROOPS
				(try_for_range, ":troop_no", troop_definitions_begin, troop_definitions_end),
					(lt, ":pos_y", MAXIMUM_TROOP_RECORDS),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION),
					(troop_get_slot, ":unique_location", ":troop_no", slot_troop_unique_location),
					(is_between, ":unique_location", centers_begin, centers_end),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(val_add, ":pos_y", 1),
					### DIAGNOSTIC ###
					(ge, DEBUG_RECRUITMENT, 1),
					(assign, reg31, ":pos_y"),
					(str_store_troop_name, s31, ":troop_no"),
					(display_message, "@DEBUG: #{reg31} - {s31}", gpu_green),
				(try_end),
				
				## COUNT - MERCENARIES
				(try_for_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
					(lt, ":pos_y", MAXIMUM_TROOP_RECORDS),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(val_add, ":pos_y", 1),
					### DIAGNOSTIC ###
					(ge, DEBUG_RECRUITMENT, 1),
					(assign, reg31, ":pos_y"),
					(str_store_troop_name, s31, ":troop_no"),
					(display_message, "@DEBUG: #{reg31} - {s31}", gpu_debug),
				(try_end),
				
				## COUNT - BANDITS
				(try_for_range, ":troop_no", bandits_begin, bandits_end),
					(lt, ":pos_y", MAXIMUM_TROOP_RECORDS),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(val_add, ":pos_y", 1),
					### DIAGNOSTIC ###
					(ge, DEBUG_RECRUITMENT, 1),
					(assign, reg31, ":pos_y"),
					(str_store_troop_name, s31, ":troop_no"),
					(display_message, "@DEBUG: #{reg31} - {s31}", gpu_green),
				(try_end),
				
				# Set our initial position.
				(val_mul, ":pos_y", ":troop_step"),
				
				################## DISPLAY ###################
				(assign, ":record", 0),
				
				## DISPLAY - FACTION TROOPS
				(try_for_range, ":troop_no", ":lower_bound", ":upper_bound"),
					(lt, ":record", MAXIMUM_TROOP_RECORDS),
					## FILTER+ - REMOVE UNIQUES
					(assign, ":pass", 1),
					(try_begin),
						(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION),
						(assign, ":pass", 0),
					(else_try),
						(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION_UPGRADE),
						(assign, ":pass", 0),
					(try_end),
					(eq, ":pass", 1),
					## FILTER- - REMOVE UNIQUES
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(call_script, "script_grt_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
				# ## DISPLAY - UNIQUE TROOPS
				# (try_for_range, ":troop_no", unique_troops_begin, unique_troops_end),
					# (lt, ":record", MAXIMUM_TROOP_RECORDS),
					# (call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					# (call_script, "script_grt_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					# (val_add, ":record", 1),
					# (val_sub, ":pos_y", ":troop_step"),
				# (try_end),
				
				## DISPLAY - UNIQUE TROOPS
				(try_for_range, ":troop_no", troop_definitions_begin, troop_definitions_end),
					(lt, ":record", MAXIMUM_TROOP_RECORDS),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION),
					(troop_get_slot, ":unique_location", ":troop_no", slot_troop_unique_location),
					(is_between, ":unique_location", centers_begin, centers_end),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(call_script, "script_grt_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
				## DISPLAY - MERCENARIES
				(try_for_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
					(lt, ":record", MAXIMUM_TROOP_RECORDS),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(call_script, "script_grt_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
				## DISPLAY - BANDITS
				(try_for_range, ":troop_no", bandits_begin, bandits_end),
					(lt, ":record", MAXIMUM_TROOP_RECORDS),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(call_script, "script_grt_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
			(set_container_overlay, -1),
			
		]),
	
    (ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(assign, "$grt_mode", GARRISON_MODE_GENERAL),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
		(try_end), 
	  ]),  

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_grt_handle_mode_switching_buttons", ":object", ":value"),
		
		####### FILTER : QUEUE QUANTITY ADJUSTMENTS #######
		(assign, ":continue", 1),
		(try_for_range, ":record", grt2_obj_numbox_queue_qty, grt2_obj_button_dismiss_troop), 
			(troop_slot_eq, GRT_OBJECTS, ":record", ":object"),
			(assign, ":continue", 0),
		(try_end),
		(eq, ":continue", 1),
		
		####### BUTTON : INSPECT EQUIPMENT #######
		(try_for_range, ":record", grt2_obj_button_inspect_equipment, grt2_obj_numbox_queue_qty), 
			(eq, ":continue", 1),
			(troop_slot_eq, GRT_OBJECTS, ":record", ":object"),
			(assign, ":continue", 0),
			(store_add, ":button_val_slot", grt2_val_button_troop_no, ":record"),  # 100 + (250 to 325)
			(val_sub, ":button_val_slot", grt2_obj_button_inspect_equipment), # Push us back into the 100-199 range.
			(troop_get_slot, "$temp", GRT_OBJECTS, ":button_val_slot"),
			(assign, "$grt_mode", GARRISON_MODE_TROOP_INFO),
			(assign, "$g_presentation_next_presentation", "prsnt_hub_recruitment"),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_garrison_switch_modes"),
		(try_end),
		(eq, ":continue", 1),
		
		####### BUTTON : QUEUE TROOP #######
		(try_for_range, ":record", grt2_obj_button_recruit_troop, grt2_obj_button_inspect_equipment), 
			(eq, ":continue", 1),
			(troop_slot_eq, GRT_OBJECTS, ":record", ":object"),
			(assign, ":continue", 0),
			(store_add, ":button_val_slot", grt2_val_button_troop_no, ":record"),  # 100 + (175 to 250)
			(val_sub, ":button_val_slot", grt2_obj_button_recruit_troop), # Push us back into the 100-199 range.
			(troop_get_slot, "$temp", GRT_OBJECTS, ":button_val_slot"),
			
			# Setup the number of troops being requested.
			(store_sub, ":obj_numbox_slot", ":record", grt2_obj_button_recruit_troop),
			(val_add, ":obj_numbox_slot", grt2_obj_numbox_queue_qty),
			(troop_get_slot, ":obj_numbox", GRT_OBJECTS, ":obj_numbox_slot"),
			(overlay_get_val, ":troop_count", ":obj_numbox"),
			(try_begin),
				(ge, ":troop_count", 1),
				(call_script, "script_grt_add_troop_to_queue", "$current_town", "$temp", ":troop_count"),
			(try_end),
			
			# Report transaction to the player.
			(str_store_troop_name, s21, "$temp"),
			(assign, reg21, ":troop_count"),
			(try_begin),
				(ge, ":troop_count", 2),
				(str_store_troop_name_plural, s21, "$temp"),
			(try_end),
			(str_store_party_name, s22, "$current_town"),
			(try_begin),
				(ge, ":troop_count", 1),
				(display_message, "@You added {reg21} {s21} to the garrison queue in {s22}.", gpu_green),
			(else_try),
				(display_message, "@You need to specify a number of troops to add to the queue.", gpu_red),
			(try_end),
			(start_presentation, "prsnt_garrison_recruitment"),
		(try_end),
		(eq, ":continue", 1),
		
		####### BUTTON : REMOVE TROOP FROM QUEUE #######
		(try_for_range, ":record", grt2_obj_button_dismiss_troop, grt2_obj_end_of_slots), 
			(eq, ":continue", 1),
			(troop_slot_eq, GRT_OBJECTS, ":record", ":object"),
			(assign, ":continue", 0),
			(store_sub, ":offset", ":record", grt2_obj_button_dismiss_troop),
			(store_add, ":button_val_slot", ":offset", grt2_val_button_troop_no),
			(troop_get_slot, "$temp", GRT_OBJECTS, ":button_val_slot"),
			
			# Setup the number of troops being requested.
			(store_add, ":obj_numbox_slot", ":offset", grt2_obj_numbox_queue_qty),
			(troop_get_slot, ":obj_numbox", GRT_OBJECTS, ":obj_numbox_slot"),
			(overlay_get_val, ":troop_count", ":obj_numbox"),
			(call_script, "script_grt_get_queue_count_for_troop", "$current_town", "$temp"),
			(val_min, ":troop_count", reg1),
			(try_begin),
				(ge, ":troop_count", 1),
				(call_script, "script_grt_remove_troop_from_queue", "$current_town", "$temp", ":troop_count"),
			(try_end),
			
			# Report transaction to the player.
			(str_store_troop_name, s21, "$temp"),
			(assign, reg21, ":troop_count"),
			(try_begin),
				(ge, ":troop_count", 2),
				(str_store_troop_name_plural, s21, "$temp"),
			(try_end),
			(str_store_party_name, s22, "$current_town"),
			(try_begin),
				(ge, ":troop_count", 1),
				(display_message, "@You removed {reg21} {s21} from the garrison queue in {s22}.", gpu_green),
			(else_try),
				(display_message, "@You need to specify an amount of troops to remove from the queue.", gpu_red),
			(try_end),
			(start_presentation, "prsnt_garrison_recruitment"),
		(try_end),
      ]),
    ]),
	
	
###########################################################################################################################
#####                                               GARRISON TRAINING                                                 #####
###########################################################################################################################

("garrison_training", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_grt_create_mode_switching_buttons"),
			
			(try_begin),
				(neg|is_between, "$g_presentation_obj_item_select_1", 0, 2),
				(assign, "$g_presentation_obj_item_select_1", 0),
			(try_end),
			
			#########################################
			###      TEMPORARY PARTY CREATION     ###
			#########################################
			(assign, ":party_temp", "p_temp_party"),
			(call_script, "script_party_copy", ":party_temp", "$current_town"),
			(party_get_slot, reg21, "$current_town", slot_center_training_budget),
			(call_script, "script_grt_convert_gold_to_xp_training", ":party_temp", reg21, GRT_TRAINING_PREVIEW),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			## OBJ - PORTRAIT - CAPTAIN OF THE GUARDS
			(assign, ":pos_x", 265),
			(assign, ":pos_y", 445),
			(try_begin),
				(party_get_slot, ":advisor_captain", "$current_town", slot_center_advisor_war),
				(is_between, ":advisor_captain", companions_begin, companions_end),
				(call_script, "script_gpu_create_portrait", ":advisor_captain", ":pos_x", ":pos_y", 400, grt5_obj_portrait_guard_captain),
				# Name of the captain of the guards. (below the portrait)
				(store_add, ":pos_x_temp", ":pos_x", 70),
				(store_add, ":pos_y_temp", ":pos_y", -10),
				(str_store_troop_name, s1, ":advisor_captain"),
				(str_store_string, s21, "@{s1}"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Captain of the Guards Title (above the portrait)
				(store_add, ":pos_x_temp", ":pos_x", 70),
				(store_add, ":pos_y_temp", ":pos_y", 140),
				(str_store_troop_name, s1, ":advisor_captain"),
				(str_store_string, s21, "@Captain of the Guards"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
			(else_try),
				(display_message, "@No Captain of the Guards is assigned to this center.", gpu_red),
				(str_store_string, s21, "@No Captain^^of the Guard^^selected."),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", 335, 540, 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
			(try_end),
			
			#######################################
			###    GARRISON TRAINING SLIDER     ###
			#######################################
			(assign, ":pos_y", 390),
			(assign, ":x_left", 245),
			(store_add, ":x_apply", ":x_left", 70),
			(store_add, ":x_right", ":x_left", 180),
			
			(str_store_string, s21, "@Budget"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_left", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_left", ":pos_y", 0, gpu_left),
			(val_add, ":pos_y", 3),
			(assign, reg21, 0),
			(assign, reg22, 0),
			(party_get_slot, ":garrison_budget", "$current_town", slot_center_training_budget),
			(assign, reg21, ":garrison_budget"),
			(str_store_string, s21, "@{reg21} Denars"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_right", ":pos_y", grt5_obj_text_training_changes, gpu_right),
			(call_script, "script_gpu_resize_object", grt5_obj_text_training_changes, 75),
			(val_sub, ":pos_y", 40),
			# Create the slider.
			(call_script, "script_gpu_create_slider", 0, 5000, ":x_left", ":pos_y", grt5_obj_slider_garrison_training, grt5_val_slider_garrison_training),
			(call_script, "script_gpu_resize_object", grt5_obj_slider_garrison_training, 75),
			(overlay_set_val, reg1, ":garrison_budget"),
			(val_sub, ":pos_y", 25),
			(str_store_string, s21, "@Apply"),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_apply", ":pos_y", grt5_obj_button_training_apply), # Treasury Deposit
			(call_script, "script_gpu_resize_object", grt5_obj_button_training_apply, 75),
			(overlay_set_display, reg1, 0),
			
			## OBJ - CHECKBOX - ENABLE GARRISON TRAINING
			(str_store_string, s21, "@Enable Training"),
			(call_script, "script_gpu_create_checkbox", 245, 295, "str_grt_s21", grt5_obj_checkbox_enable_training, grt5_val_checkbox_enable_training),
			(call_script, "script_gpu_resize_object", grt5_obj_checkbox_enable_training, 75),
			(party_get_slot, ":setting", "$current_town", slot_center_upgrade_garrison),
			(overlay_set_val, reg1, ":setting"),
			
			## OBJ - CHECKBOX - HIDE MAX LEVEL UNITS
			(str_store_string, s21, "@Hide Maxed Units"),
			(call_script, "script_gpu_create_checkbox", 245, 270, "str_grt_s21", grt5_obj_checkbox_hide_maxed_units, grt5_val_checkbox_hide_maxed_units),
			(call_script, "script_gpu_resize_object", grt5_obj_checkbox_hide_maxed_units, 75),
			(overlay_set_val, reg1, "$g_presentation_obj_item_select_1"),
			
			
			#######################################
			###  FUNDING EFFICIENCY BREAKDOWN   ###
			#######################################
			## OBJ - CONTAINER - CURRENT GARRISON COMPLIMENT
			(assign, ":y_bottom", 65),
			(assign, ":x_left",  235),
			(assign, ":x_width", 200),
			(assign, ":y_width", 125),
			(assign, ":x_factor", 5),
			(assign, ":x_bonus", 195),
			(assign, ":y_line_step", 20),
			
			## OBJ - LABEL - EFFICIENCY HEADING
			(str_store_string, s21, "@Funding Efficiency"),
			(store_div, ":pos_x_temp", ":x_width", 2),
			(val_add, ":pos_x_temp", ":x_left"),
			(store_add, ":pos_y_temp", ":y_bottom", ":y_width"),
			(val_add, ":pos_y_temp", 40),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			# (call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - LABELS - FUNDING EFFICIENCY COLUMN LABELS
			(val_sub, ":pos_y_temp", 25),
			(store_add, ":pos_x_temp", ":x_left", ":x_factor"),
			(str_store_string, s21, "@Factor"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(store_add, ":pos_x_temp", ":x_left", ":x_bonus"),
			(str_store_string, s21, "@Bonus"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - CONTAINER+ - FUNDING EFFICIENCY BREAKDOWN
			# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt5_obj_container_2),
				
				(store_mul, ":pos_y", ":y_line_step", 5),
				
				## Base Bonus
				(str_store_string, s21, "@Base"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_factor", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(assign, reg21, GRT_FUNDEFF_BASE),
				(str_store_string, s21, "@+{reg21}%"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_bonus", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## Captain of the Guard Bonus
				(try_begin),
					(party_get_slot, ":advisor_captain", "$current_town", slot_center_advisor_war),
					(is_between, ":advisor_captain", companions_begin, companions_end),
					(store_skill_level, ":skill_training", "skl_trainer", ":advisor_captain"),
					(val_mul, ":skill_training", 4),
					(assign, reg21, ":skill_training"),
				(else_try),
					(assign, reg21, 0),
				(try_end),
				(val_sub, ":pos_y", ":y_line_step"),
				(str_store_string, s21, "@Guard Captain"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_factor", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(str_store_string, s21, "@+{reg21}%"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_bonus", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## Emblem Bonus
				(try_begin),
					(this_or_next|party_slot_ge, "$current_town", slot_center_training_emblem_duration, 1), # Temporary Boost
					(party_slot_eq, "$current_town", slot_center_training_emblem_duration, -1), # Permanent Boost
					(assign, reg21, GRT_FUNDEFF_EMBLEM_BONUS),
				(else_try),
					(assign, reg21, 0),
				(try_end),
				(val_sub, ":pos_y", ":y_line_step"),
				(str_store_string, s21, "@Emblem Boosts"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_factor", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(str_store_string, s21, "@+{reg21}%"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_bonus", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## Improvement Bonus
				(try_begin),
					(party_slot_ge, "$current_town", slot_center_has_training_grounds, cis_built),
					(assign, reg21, GRT_FUNDEFF_TRAINING_GROUNDS),
				(else_try),
					(assign, reg21, 0),
				(try_end),
				(val_sub, ":pos_y", ":y_line_step"),
				(str_store_string, s21, "@Improvements"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_factor", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(str_store_string, s21, "@+{reg21}%"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_bonus", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## TOTAL EFFICIENCY BONUS
				(val_sub, ":pos_y", ":y_line_step"),
				(str_store_string, s21, "@Total Efficiency"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_factor", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_factor", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_grt_get_gold_to_xp_training_ratio", "$current_town"),
				(str_store_string, s21, "@{reg1}%"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_bonus", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_bonus", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
			(set_container_overlay, -1), ## CONTAINER- - FUNDING EFFICIENCY BREAKDOWN
			
			#######################################
			###          GARRISON LIST          ###
			#######################################
			
			## OBJ - CONTAINER - CURRENT GARRISON COMPLIMENT
			(assign, ":y_bottom", 80),
			(assign, ":x_left",  450),
			(assign, ":x_width", 485),
			(assign, ":y_width", 480),
			(assign, ":x_count", 35),
			(assign, ":x_name", 50),
			(assign, ":x_xp", 360),
			(assign, ":x_upgrade", 440),
			
			## OBJ - LABEL - GARRISON HEADING
			(str_store_string, s21, "@Garrison Compliment"),
			(store_div, ":pos_x_temp", ":x_width", 2),
			(val_add, ":pos_x_temp", ":x_left"),
			(store_add, ":pos_y_temp", ":y_bottom", ":y_width"),
			(val_add, ":pos_y_temp", 65),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			# (call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - LABELS - GARRISON HEADING COLUMN LABELS
			(val_sub, ":pos_y_temp", 30),
			(store_add, ":pos_x_temp", ":x_left", ":x_xp"),
			(str_store_string, s21, "@Current"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			(store_add, ":pos_x_temp", ":x_left", ":x_upgrade"),
			(str_store_string, s21, "@Will"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			(val_sub, ":pos_y_temp", 20),
			(store_add, ":pos_x_temp", ":x_left", ":x_count"),
			(str_store_string, s21, "@#"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
			(store_add, ":pos_x_temp", ":x_left", ":x_name"),
			(str_store_string, s21, "@Troop Type"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(store_add, ":pos_x_temp", ":x_left", ":x_xp"),
			(str_store_string, s21, "@Experience"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			(store_add, ":pos_x_temp", ":x_left", ":x_upgrade"),
			(str_store_string, s21, "@Upgrade"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - CONTAINER+ - GARRISON LIST
			# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt5_obj_container_1),
				
				(assign, ":lines", 0),
				(party_get_num_companion_stacks, ":stack_capacity", "$current_town"),
				(try_for_range, ":stack_no", 0, ":stack_capacity"),
					(party_stack_get_troop_id, ":troop_no", "$current_town", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"),
					# Check if unit is a max level unit for filtering.
					(troop_get_upgrade_troop, ":upgrade_1", ":troop_no", 0),
					(troop_get_upgrade_troop, ":upgrade_2", ":troop_no", 0),
					(this_or_next|eq, "$g_presentation_obj_item_select_1", 0),
					(neq, ":upgrade_1", 0),
					(this_or_next|eq, "$g_presentation_obj_item_select_1", 0),
					(neq, ":upgrade_2", 0),
					(val_add, ":lines", 1),
				(try_end),
				
				(assign, ":line_step", 25),
				(store_mul, ":pos_y", ":lines", ":line_step"),
				
				(party_get_num_companion_stacks, ":stack_capacity", "$current_town"),
				(try_for_range, ":stack_no", 0, ":stack_capacity"),
					(party_stack_get_troop_id, ":troop_no", "$current_town", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"),
					# Check if unit is a max level unit for filtering.
					(troop_get_upgrade_troop, ":upgrade_1", ":troop_no", 0),
					(troop_get_upgrade_troop, ":upgrade_2", ":troop_no", 0),
					(this_or_next|eq, "$g_presentation_obj_item_select_1", 0),
					(neq, ":upgrade_1", 0),
					(this_or_next|eq, "$g_presentation_obj_item_select_1", 0),
					(neq, ":upgrade_2", 0),
					
					# Display party stack size
					(party_stack_get_size, ":troop_count", "$current_town", ":stack_no"),
					(assign, reg1, ":troop_count"),
					(str_store_string, s21, "@{reg1}"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_count", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					# Display the stack troop name
					(try_begin),
						(ge, ":troop_count", 2),
						(str_store_troop_name_plural, s21, ":troop_no"),
					(else_try),
						(str_store_troop_name, s21, ":troop_no"),
					(try_end),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_name", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					# Display the party stack experience
					(party_stack_get_experience, reg1, "$current_town", ":stack_no"), # WSE
					(str_store_string, s21, "@{reg1}"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_xp", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					# Display the # upgradeable
					(party_stack_get_num_upgradeable, reg1, ":party_temp", ":stack_no"), # WSE
					(str_store_string, s21, "@{reg1}"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_upgrade", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					(val_sub, ":pos_y", ":line_step"),
				(try_end),
				
			(set_container_overlay, -1), ## CONTAINER- - GARRISON LIST
			
			## OBJ - BUTTON (DEBUG) - PROCESS BUDGET
			(try_begin),
				(this_or_next|ge, DEBUG_GARRISON, 1),
				(ge, BETA_TESTING_MODE, 1),
				(str_store_string, s21, "@DEBUG: Process Budget"),
				(call_script, "script_gpu_create_game_button", "str_hub_s21", 700, 35, grt5_obj_button_cheat_xp_party),
			(try_end),
		]),
	
    (ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(assign, "$grt_mode", GARRISON_MODE_GENERAL),
			## Clear Temporary Party
			(assign, ":party_temp", "p_temp_party"),
			(call_script, "script_clear_party_group", ":party_temp"),
			(try_begin),
				(ge, DEBUG_GARRISON, 1),
				(display_message, "@DEBUG (GRT): Temporary party cleared. (escape exit)", gpu_debug),
			(try_end),
			## Exit the presentation
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_grt_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### CHECKBOX - ENABLE TRAINING #######
			(troop_slot_eq, GRT_OBJECTS, grt5_obj_checkbox_enable_training, ":object"),
			(party_set_slot, "$current_town", slot_center_upgrade_garrison, ":value"),
		
		(else_try),   ####### CHECKBOX - HIDE MAX LEVEL UNITS #######
			(troop_slot_eq, GRT_OBJECTS, grt5_obj_checkbox_hide_maxed_units, ":object"),
			(assign, "$g_presentation_obj_item_select_1", ":value"),
			(start_presentation, "prsnt_garrison_training"),
			
		(else_try),  ####### BUTTON - CHEAT XP TO PARTY #######
			(troop_slot_eq, GRT_OBJECTS, grt5_obj_button_cheat_xp_party, ":object"),
			(party_get_slot, reg21, "$current_town", slot_center_training_budget),
			(call_script, "script_grt_convert_gold_to_xp_training", "$current_town", reg21, GRT_TRAINING_PROCESS),
			(start_presentation, "prsnt_garrison_training"),
			
		(else_try),
				### SLIDER - GARRISON TRAINING ###
				(troop_slot_eq, GRT_OBJECTS, grt5_obj_slider_garrison_training, ":object"),
				(troop_set_slot, GRT_OBJECTS, grt5_val_slider_garrison_training, ":value"),
				(overlay_set_val, ":object", ":value"),
				(troop_get_slot, ":obj_label", GRT_OBJECTS, grt5_obj_text_training_changes),
				(assign, reg21, ":value"),
				(str_store_string, s21, "@{reg21} Denars"),
				(overlay_set_text, ":obj_label", "str_hub_s21"),
				# Display Apply Button
				(troop_get_slot, ":obj_apply", GRT_OBJECTS, grt5_obj_button_training_apply),
				(overlay_set_display, ":obj_apply", 1),
				
			(else_try),
				### BUTTON - GARRISON TRAINING BUDGET APPLY ###
				(troop_slot_eq, GRT_OBJECTS, grt5_obj_button_training_apply, ":object"),
				(troop_get_slot, ":setting", GRT_OBJECTS, grt5_val_slider_garrison_training),
				(party_set_slot, "$current_town", slot_center_training_budget, ":setting"),
				# Enable garrison training if a value other than 0 is set.
				(try_begin),
					(ge, ":setting", 1),
					(party_set_slot, "$current_town", slot_center_upgrade_garrison, 1), # Enable garrison training.
				(else_try),
					(party_set_slot, "$current_town", slot_center_upgrade_garrison, 0), # Disable garrison training.
				(try_end),
				(start_presentation, "prsnt_garrison_training"),
				
			(try_end),
		
      ]),
    ]),	
	
	
###########################################################################################################################
#####                                              GARRISON REORDERING                                                #####
###########################################################################################################################

("garrison_reordering", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_grt_create_mode_switching_buttons"),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			# OBJ - Warning note.
			(call_script, "script_gpu_create_text_label", "str_hub_label_construction", 500, 635, 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			
		]),
	
    (ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(assign, "$grt_mode", GARRISON_MODE_GENERAL),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_grt_handle_mode_switching_buttons", ":object", ":value"),
		
      ]),
    ]),	
	
	
###########################################################################################################################
#####                                                EMBLEM OPTIONS                                                   #####
###########################################################################################################################

("garrison_emblem_options", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_grt_create_mode_switching_buttons"),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 515),
		
		## OBJ - CONTAINER+ - EMBLEM OPTIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt4_obj_container_1),
		
			(assign, ":y_line_step", 20),
			(assign, ":y_note_step", 25),
			(assign, ":x_desc", 110),
			(assign, ":y_option_step", 70),
			
			(assign, ":pos_y", 30),
			(store_mul, ":y_temp", ":y_option_step", 4),
			(val_add, ":pos_y", ":y_temp"),
			(store_mul, ":y_temp", ":y_line_step", 12),
			(val_add, ":pos_y", ":y_temp"),
			(store_mul, ":y_temp", ":y_note_step", 4),
			(val_add, ":pos_y", ":y_temp"),
			
			##############
			# OPTION #1  #
			##############
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Training Cost Reduction"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", grt4_obj_button_option_1, EMBLEM_COST_REDUCE_GARRISON_COST), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@The cost of hiring troops for your garrison at this location "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@will be reduced by 15% for a period of one week."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Note: This applies only to troops hired for your garrison."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(party_get_slot, reg21, "$current_town", slot_center_queue_cost_reduce_duration),
			(val_div, reg21, 24), # Convert hours to days.
			(try_begin),
				(ge, reg21, 1),
				(store_sub, reg22, reg21, 1),
				(str_store_string, s21, "@Status: Currently {reg21} day{reg22?s:} remain for this boost."),
			(else_try),
				(str_store_string, s21, "@Status: This boost is not currently active here."),
			(try_end),
			(val_sub, ":pos_y", ":y_note_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			##############
			# OPTION #2  #
			##############
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Advanced Efficiency"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", grt4_obj_button_option_2, EMBLEM_COST_TRAINING_PERM_REDUCTION), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@The cost of hiring troops for this location is reduced "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@permanently by 2%.  This benefit can stack up to 5 times."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Note: This applies only to troops hired for your garrison."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(party_get_slot, reg21, "$current_town", slot_center_training_cost_reduction),
			(val_mul, reg21, EMBLEM_EFFECT_TRAINING_PERM_REDUCTION),
			(str_store_string, s21, "@Status: This location receives a {reg21}% reduction to training costs."),
			(val_sub, ":pos_y", ":y_note_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			##############
			# OPTION #3  #
			##############
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Accelerate Training (Temporarily)"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", grt4_obj_button_option_3, EMBLEM_COST_TEMP_ACCELERATE_TRAINING), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@The rate at which troops within your garrison at this location "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@are upgraded for a given budget will be enhanced for a period "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@of one month. "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(party_get_slot, reg21, "$current_town", slot_center_training_emblem_duration),
			(try_begin),
				(lt, reg21, 0),
				(assign, reg21, 0),
			(try_end),
			(val_div, reg21, 24), # Convert hours to days.
			(try_begin),
				(ge, reg21, 1),
				(store_sub, reg22, reg21, 1),
				(str_store_string, s21, "@Status: Currently {reg21} day{reg22?s:} remain for this boost."),
			(else_try),
				(lt, reg21, 0),
				(str_store_string, s21, "@Status: This boost is already permanent."),
			(else_try),
				(str_store_string, s21, "@Status: This boost is not currently active here."),
			(try_end),
			(val_sub, ":pos_y", ":y_note_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			##############
			# OPTION #4  #
			##############
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Accelerate Training (Permanent)"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", grt4_obj_button_option_4, EMBLEM_COST_PERM_ACCELERATE_TRAINING), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@The rate at which troops within your garrison at this location "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@are upgraded for a given budget will be enhanced permanently. "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@This option may only be used one time."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(party_get_slot, reg21, "$current_town", slot_center_training_emblem_duration),
			(try_begin),
				(ge, reg21, 0),
				(str_store_string, s21, "@Status: This boost has not been activated here."),
			(else_try),
				(str_store_string, s21, "@Status: This boost has been used here."),
			(try_end),
			(val_sub, ":pos_y", ":y_note_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
		(set_container_overlay, -1), ## CONTAINER- - EMBLEM OPTIONS
		
		(try_begin),
			(this_or_next|ge, BETA_TESTING_MODE, 1),
			(ge, DEBUG_GARRISON, 1),
			(str_store_string, s21, "@Gain 1 Emblem "),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 855, 35, grt4_obj_button_debug_gain_emblem),
		(try_end),
		
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
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_grt_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### BUTTON - OPTION 1 (Temporary Cost Reduction) #######
			(troop_slot_eq, GRT_OBJECTS, grt4_obj_button_option_1, ":object"),
			(party_get_slot, ":hours", "$current_town", slot_center_queue_cost_reduce_duration),
			(val_add, ":hours", 24*7),
			(party_set_slot, "$current_town", slot_center_queue_cost_reduce_duration, ":hours"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_REDUCE_GARRISON_COST), # emblem_scripts.py
			(display_message, "@The cost for training new troops at this location has been lowered temporarily.", gpu_green),
			(start_presentation, "prsnt_garrison_emblem_options"),
			
		(else_try),  ####### BUTTON - OPTION 2 (Permanent Cost Reduction) #######
			(troop_slot_eq, GRT_OBJECTS, grt4_obj_button_option_2, ":object"),
			(party_get_slot, ":bonus", "$current_town", slot_center_training_cost_reduction),
			(try_begin),
				(ge, ":bonus", EMBLEM_STACK_LIMIT_TRAINING_PERM_REDUCTION),
				(display_message, "@Warning - This location already has the highest bonus available.", gpu_red),
			(else_try),
				(val_add, ":bonus", 1),
				(party_set_slot, "$current_town", slot_center_training_cost_reduction, ":bonus"),
				(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_TRAINING_PERM_REDUCTION), # emblem_scripts.py
				(display_message, "@The cost for training new troops at this location has been lowered permanently.", gpu_green),
				(start_presentation, "prsnt_garrison_emblem_options"),
			(try_end),
			
		(else_try),  ####### BUTTON - OPTION 3 (Temporary Accelerate Training) #######
			(troop_slot_eq, GRT_OBJECTS, grt4_obj_button_option_3, ":object"),
			(party_get_slot, ":hours", "$current_town", slot_center_training_emblem_duration),
			(try_begin),
				## FILTER - Permanent option already selected.
				(lt, ":hours", 0),
				(display_message, "@Warning - The permanent option for accelerating training has already been used.", gpu_red),
			(else_try),
				(val_add, ":hours", 24*30),
				(party_set_slot, "$current_town", slot_center_training_emblem_duration, ":hours"),
				(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_TEMP_ACCELERATE_TRAINING), # emblem_scripts.py
				(display_message, "@The upgrading garrison troops at this location has been upgraded temporarily.", gpu_green),
				(start_presentation, "prsnt_garrison_emblem_options"),
			(try_end),
			
		(else_try),  ####### BUTTON - OPTION 4 (Permanently Accelerate Training) #######
			(troop_slot_eq, GRT_OBJECTS, grt4_obj_button_option_4, ":object"),
			(party_set_slot, "$current_town", slot_center_training_emblem_duration, -1),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_PERM_ACCELERATE_TRAINING), # emblem_scripts.py
			(display_message, "@The upgrading garrison troops at this location has been upgraded permanently.", gpu_green),
			(start_presentation, "prsnt_garrison_emblem_options"),
			
		(else_try),  ####### BUTTON - DEBUGGING +1 EMBLEM #######
			(troop_slot_eq, GRT_OBJECTS, grt4_obj_button_debug_gain_emblem, ":object"),
			(this_or_next|ge, BETA_TESTING_MODE, 1),
			(ge, DEBUG_GARRISON, 1),
			(call_script, "script_emblem_award_to_player", 1), # emblem_scripts.py
			(start_presentation, "prsnt_garrison_emblem_options"),
		
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