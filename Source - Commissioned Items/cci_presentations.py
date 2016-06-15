# Custom Commissioned Items by Windyplains

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
#####                                               ITEM COMMISSIONING                                                #####
###########################################################################################################################

("commission_requests", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_cci_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_party_name, s22, "$current_town"),
		(str_store_string, s21, "@Item Commissioning in {s22}"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		# ## OBJ - BUTTON - DONE
        # (str_store_string, s21, "@Done"),
		# (call_script, "script_gpu_create_game_button", "str_hub_s21", 500, 35, cci_obj_button_done), # DONE
		
		## OBJ - TEXT - ITEM TYPE TITLE
		# (str_store_string, s21, "@Requested Type:"),
		# (call_script, "script_gpu_create_text_label", "str_hub_s21", 50, 600, cci_obj_title_type, gpu_left), # 680
		
		## OBJ - COMBO BUTTON - ITEM TYPE SELECTOR
        (create_combo_label_overlay, "$g_presentation_obj_1"),
        (position_set_x, pos1, 450), # 500),
        (position_set_y, pos1, 582),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (overlay_add_item, "$g_presentation_obj_1", "@One-Handed Weapons"),
        (overlay_add_item, "$g_presentation_obj_1", "@Two-Handed Weapons"),
        (overlay_add_item, "$g_presentation_obj_1", "@Polearms"),
        (overlay_add_item, "$g_presentation_obj_1", "@Ranged Weapons"),
        (overlay_add_item, "$g_presentation_obj_1", "@Ammunition"),
        (overlay_add_item, "$g_presentation_obj_1", "@Shields"),
        (overlay_add_item, "$g_presentation_obj_1", "@Helmets"),
        (overlay_add_item, "$g_presentation_obj_1", "@Armors"),
        (overlay_add_item, "$g_presentation_obj_1", "@Boots"),
        (overlay_add_item, "$g_presentation_obj_1", "@Gauntlets"),
		(try_begin),  ### MOUNTS ###
			(eq, CCI_SETTING_HORSES_COMMISSIONABLE, 1), # Horses can be commissioned at all.  Setting in cci_constants.py
			(overlay_add_item, "$g_presentation_obj_1", "@Horses"),
		(try_end),
		(overlay_set_val, "$g_presentation_obj_1", "$temp"),
		
		## OBJ - CONTAINER - AVAILABLE ITEMS FOR COMMISSIONING
		(assign, ":y_bottom", 330),
		(assign, ":x_left",   250),
		(assign, ":x_width",  395), # 5 items wide
		(assign, ":y_width",  240), # 4 items high
		
		## OBJ - CONTAINER+ - CURRENT COMMISSIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", cci_obj_container_items),
		
        # (str_clear, s0),
        # (create_text_overlay, "$g_presentation_obj_6", s0, tf_scrollable),
        # (position_set_x, pos1, 250),
        # (position_set_y, pos1, 330), # 100),
        # (overlay_set_position, "$g_presentation_obj_6", pos1),
        # (position_set_x, pos1, 395), # 50 + (80 * 5); 7 items
        # (position_set_y, pos1, 240), # 80 * 4; 4 items
        # (overlay_set_area_size, "$g_presentation_obj_6", pos1),
        # (set_container_overlay, "$g_presentation_obj_6"),

			(assign, "$temp_2", 0),
			(store_faction_of_party, ":faction_no", "$current_town"),
			## types
			(try_for_range, ":item_no", CCI_FIRST_ITEM, CCI_LAST_ITEM),
				## FILTER - ITEM TYPE
				(item_get_type, ":type", ":item_no"),
				(assign, ":continue", 0),
				(try_begin), ### ONE-HANDED WEAPONS ###
					(eq, "$temp", CCI_GROUP_ONE_HANDED),
					(eq, ":type", itp_type_one_handed_wpn),
					(assign, ":continue", 1),
				(else_try),  ### TWO-HANDED WEAPONS ###
					(eq, "$temp", CCI_GROUP_TWO_HANDED),
					(eq, ":type", itp_type_two_handed_wpn),
					(assign, ":continue", 1),
				(else_try),  ### POLEARMS ###
					(eq, "$temp", CCI_GROUP_POLEARMS),
					(eq, ":type", itp_type_polearm),
					(assign, ":continue", 1),
				(else_try),  ### RANGED WEAPONS ###
					(eq, "$temp", CCI_GROUP_RANGED_WEAPONS),
					(this_or_next|eq, ":type", itp_type_bow),
					(this_or_next|eq, ":type", itp_type_crossbow),
					(this_or_next|eq, ":type", itp_type_thrown),
					(this_or_next|eq, ":type", itp_type_pistol),
					(eq, ":type", itp_type_musket),
					(assign, ":continue", 1),
				(else_try),  ### AMMUNITION ###
					(eq, "$temp", CCI_GROUP_AMMUNITION),
					(this_or_next|eq, ":type", itp_type_bolts),
					(this_or_next|eq, ":type", itp_type_arrows),
					(eq, ":type", itp_type_bullets),
					(assign, ":continue", 1),
				(else_try),  ### SHIELDS ###
					(eq, "$temp", CCI_GROUP_SHIELDS),
					(eq, ":type", itp_type_shield),
					(assign, ":continue", 1),
				(else_try),  ### HELMETS ###
					(eq, "$temp", CCI_GROUP_HELMETS),
					(eq, ":type", itp_type_head_armor),
					(assign, ":continue", 1),
				(else_try),  ### BODY ARMOR ###
					(eq, "$temp", CCI_GROUP_BODY),
					(eq, ":type", itp_type_body_armor),
					(assign, ":continue", 1),
				(else_try),  ### BOOTS ###
					(eq, "$temp", CCI_GROUP_BOOTS),
					(eq, ":type", itp_type_foot_armor),
					(assign, ":continue", 1),
				(else_try),  ### GAUNTLETS ###
					(eq, "$temp", CCI_GROUP_HANDS),
					(eq, ":type", itp_type_hand_armor),
					(assign, ":continue", 1),
				(else_try),  ### MOUNTS ###
					(eq, "$temp", CCI_GROUP_MOUNTS),
					(eq, ":type", itp_type_horse),
					(eq, CCI_SETTING_HORSES_COMMISSIONABLE, 1), # Horses can be commissioned at all.  Setting in cci_constants.py
					(assign, ":continue", 1),
				(try_end),
				(eq, ":continue", 1),
				## FILTER - REGION
				(this_or_next|item_has_faction, ":item_no", ":faction_no"), # Specific region selected.
				(eq, CCI_SETTING_USE_REGIONAL_FLAGS, 0), # Item region flags disabled.
				## FILTER - MERCHANDISE
				(this_or_next|ge, BETA_TESTING_MODE, 1),
				(this_or_next|eq, CCI_SETTING_LIMIT_TO_MERCHANDISE, 0), # Merchandise setting not required.  Setting in cci_constants.py
				(item_has_property, ":item_no", itp_merchandise),
				
				(val_add, "$temp_2", 1),
			(try_end),

			(store_div, ":height", "$temp_2", 5), # 7), # 7 items wide
			(store_mod, ":offset", "$temp_2", 5), # 7),
			(val_min, ":offset", 1),
			(val_add, ":height", ":offset"),
			(store_mul, ":pos_y", ":height", 80),
			(val_sub, ":pos_y", 80),
			(assign, ":pos_x", 0),
			(assign, ":slot_no", 0),
			(try_for_range, ":item_no", CCI_FIRST_ITEM, CCI_LAST_ITEM),
				## FILTER - REGION
				(this_or_next|item_has_faction, ":item_no", ":faction_no"), # Specific region selected.
				(eq, CCI_SETTING_USE_REGIONAL_FLAGS, 0), # Item region flags disabled.
				# (neq, ":faction_no", "fac_player_supporters_faction"),
				
				## FILTER - MERCHANDISE
				(this_or_next|eq, ":item_no", "itm_flintlock_pistol"),
				(this_or_next|ge, BETA_TESTING_MODE, 1),
				(this_or_next|eq, CCI_SETTING_LIMIT_TO_MERCHANDISE, 0), # Merchandise setting not required.  Setting in cci_constants.py
				(item_has_property, ":item_no", itp_merchandise),

				## FILTER - ITEM TYPE
				(item_get_type, ":type", ":item_no"),
				(assign, ":continue", 0),
				(try_begin), ### ONE-HANDED WEAPONS ###
					(eq, "$temp", CCI_GROUP_ONE_HANDED),
					(eq, ":type", itp_type_one_handed_wpn),
					(assign, ":continue", 1),
				(else_try),  ### TWO-HANDED WEAPONS ###
					(eq, "$temp", CCI_GROUP_TWO_HANDED),
					(eq, ":type", itp_type_two_handed_wpn),
					(assign, ":continue", 1),
				(else_try),  ### POLEARMS ###
					(eq, "$temp", CCI_GROUP_POLEARMS),
					(eq, ":type", itp_type_polearm),
					(assign, ":continue", 1),
				(else_try),  ### RANGED WEAPONS ###
					(eq, "$temp", CCI_GROUP_RANGED_WEAPONS),
					(this_or_next|eq, ":type", itp_type_bow),
					(this_or_next|eq, ":type", itp_type_crossbow),
					(this_or_next|eq, ":type", itp_type_thrown),
					(this_or_next|eq, ":type", itp_type_pistol),
					(eq, ":type", itp_type_musket),
					(assign, ":continue", 1),
				(else_try),  ### AMMUNITION ###
					(eq, "$temp", CCI_GROUP_AMMUNITION),
					(this_or_next|eq, ":type", itp_type_bolts),
					(this_or_next|eq, ":type", itp_type_arrows),
					(eq, ":type", itp_type_bullets),
					(assign, ":continue", 1),
				(else_try),  ### SHIELDS ###
					(eq, "$temp", CCI_GROUP_SHIELDS),
					(eq, ":type", itp_type_shield),
					(assign, ":continue", 1),
				(else_try),  ### HELMETS ###
					(eq, "$temp", CCI_GROUP_HELMETS),
					(eq, ":type", itp_type_head_armor),
					(assign, ":continue", 1),
				(else_try),  ### BODY ARMOR ###
					(eq, "$temp", CCI_GROUP_BODY),
					(eq, ":type", itp_type_body_armor),
					(assign, ":continue", 1),
				(else_try),  ### BOOTS ###
					(eq, "$temp", CCI_GROUP_BOOTS),
					(eq, ":type", itp_type_foot_armor),
					(assign, ":continue", 1),
				(else_try),  ### GAUNTLETS ###
					(eq, "$temp", CCI_GROUP_HANDS),
					(eq, ":type", itp_type_hand_armor),
					(assign, ":continue", 1),
				(else_try),  ### MOUNTS ###
					(eq, "$temp", CCI_GROUP_MOUNTS),
					(eq, ":type", itp_type_horse),
					(eq, CCI_SETTING_HORSES_COMMISSIONABLE, 1), # Horses can be commissioned at all.  Setting in cci_constants.py
					(assign, ":continue", 1),
				(try_end),
				(eq, ":continue", 1),
			  
				## item slot
				(call_script, "script_gpu_create_mesh", "mesh_inv_slot", ":pos_x", ":pos_y", 800, 800),
				(troop_set_slot, "trp_temp_array_a", ":slot_no", reg1),
				## item
				(create_mesh_overlay_with_item_id, reg1, ":item_no"),
				(position_set_x, pos1, 800),
				(position_set_y, pos1, 800),
				(overlay_set_size, reg1, pos1),
				(store_add, ":item_x", ":pos_x", 40),
				(store_add, ":item_y", ":pos_y", 40),
				(position_set_x, pos1, ":item_x"),
				(position_set_y, pos1, ":item_y"),
				(overlay_set_position, reg1, pos1),
				(troop_set_slot, "trp_temp_array_b", ":slot_no", reg1),
				(troop_set_slot, "trp_temp_array_c", ":slot_no", ":item_no"),
				(val_add, ":pos_x", 80),
				(val_add, ":slot_no", 1),
				(try_begin),
					(ge, ":pos_x", 400), # x5 items wide
					(assign, ":pos_x", 0),
					(val_sub, ":pos_y", 80),
				(try_end),
			(try_end),

        (set_container_overlay, -1), ## CONTAINER- - ITEM SELECTION
		
		
		## OBJ - TEXT - COMMISSION REQUESTS TITLE
		(str_store_string, s21, "@Current Commission Requests:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 250, 295, cci_obj_title_commissions, gpu_left),
		
		(assign, ":y_bottom", 85),
		(assign, ":x_left",  250),
		(assign, ":x_width", 395),
		(assign, ":y_width", 195),
		
		## OBJ - CONTAINER+ - CURRENT COMMISSIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", cci_obj_container_commissions),
			(call_script, "script_cci_get_number_of_active_commissions"),
			(assign, ":local_commissions", reg2),
			(assign, ":abandonments", reg3),
			(assign, ":commission_no", 0),
			(assign, ":y_step_long", 27),
			(assign, ":y_step_short", 20),
			(store_mul, ":pos_y", ":local_commissions", ":y_step_long"),
			(store_mul, reg1, ":local_commissions", ":y_step_short"),
			(val_add, ":pos_y", reg1),
			(val_add, ":pos_y", reg1),
			(store_mul, reg1, ":abandonments", ":y_step_short"),
			(val_add, ":pos_y", reg1),
			(val_add, ":pos_y", 5),
			
			## OBJ - LABEL - SPACER
			(str_store_string, s21, "@ "),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 10, ":pos_y", 0, gpu_left),
			(val_sub, ":pos_y", 5), # Next Line
			
			(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
				(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 0), # An item is commissioned and completed or in progress.
				(troop_slot_eq, CCI_ARRAY_LOCATION, ":slot_no", "$current_town"), # An item is commissioned in this location.
				(val_add, ":commission_no", 1),
				(assign, ":pos_x", 12), # Left margin
				
				## OBJ - LABEL - COMMISSION NUMBER
				(assign, reg21, ":commission_no"),
				(str_store_string, s21, "@#{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 85),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 85),
				
				## OBJ - LABEL - COMMISSIONED ITEM
				(troop_get_slot, ":item_no", CCI_ARRAY_ITEM_NO, ":slot_no"),
				(troop_get_slot, ":imod", CCI_ARRAY_IMOD, ":slot_no"),
				(call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
				(try_begin),
					(neq, ":imod", imod_plain),
					(str_store_string, s1, "@{s1} "),
				(else_try),
					(str_clear, s1),
				(try_end),
				(str_store_item_name, s2, ":item_no"),
				(str_store_string, s21, "@{s1}{s2}"),
				(val_add, ":pos_x", 25),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 85),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 85),
				
				## OBJ - LABEL - INVESTED PRICE
				(troop_get_slot, ":initial_price", CCI_ARRAY_COST, ":slot_no"),
				(store_mul, ":upfront_cost", ":initial_price", CCI_UPFRONT_COST),
				(val_div, ":upfront_cost", 100),
				(assign, reg21, ":initial_price"),
				(store_sub, reg22, ":initial_price", ":upfront_cost"),
				(str_store_string, s21, "@This will cost another {reg22} of a total {reg21} denars."),
				(val_sub, ":pos_y", ":y_step_short"), # Next Line
				(assign, ":pos_x", 37),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## OBJ - LABEL - COMPLETION DAYS
				# (troop_get_slot, ":remaining_price", CCI_ARRAY_STATUS, ":slot_no"),
				(call_script, "script_cci_get_queue_delay_for_center", "$current_town", ":commission_no"),
				(assign, ":remaining_price", reg1),
				(call_script, "script_cci_get_workdown_rate_in_center", "$current_town", 0),
				(assign, ":hourly_workdown", reg1),
				(store_div, ":total_hours", ":remaining_price", ":hourly_workdown"),
				(store_div, ":days", ":total_hours", 24),
				(store_mod, ":hours", ":total_hours", 24),
				(assign, reg21, ":days"),
				(store_sub, reg22, reg21, 1),
				(assign, reg23, ":hours"),
				(store_sub, reg24, reg23, 1),
				(str_store_string, s21, "@Estimated completion in {reg21} day{reg22?s:} and {reg23} hour{reg24?s:}."),
				(try_begin),
					# (eq, ":total_hours", 0),
					(troop_slot_eq, CCI_ARRAY_STATUS, ":slot_no", 0),
					(str_store_string, s21, "@Work on this item has been completed."),
				(try_end),
				(val_sub, ":pos_y", ":y_step_short"), # Next Line
				(assign, ":pos_x", 37),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## OBJ - LABEL - ABANDONMENT DAYS
				(troop_get_slot, ":days_abandoned", CCI_ARRAY_ABANDON_TIMER, ":slot_no"),
				(try_begin),
					(ge, ":days_abandoned", 1),
					(neg|party_slot_ge, "$current_town", slot_center_has_royal_forge, cis_built), ## Royal Blacksmith prevents abandonment.
					(store_sub, reg21, CCI_ABANDONED_DAYS_LIMIT, ":days_abandoned"),
					(store_sub, reg22, reg21, 1),
					(str_store_string, s21, "@This item is will be abandoned in {reg21} day{reg22?s:}."),
					(val_sub, ":pos_y", ":y_step_short"), # Next Line
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, 10092544), # gpu_dark_red
				(try_end),
				
				(val_sub, ":pos_y", ":y_step_long"), # Next Line
			(try_end), ## Commission Loop #1
			
		(set_container_overlay, -1), ## CONTAINER- - CURRENT COMMISSIONS
		
		(assign, ":commission_no", 0),
		# Giving each button a ridiculously high ID so it isn't seen as 0.
		(try_for_range, ":button_slot", cci_obj_button_item_0, cci_val_item_1_entry_slot),
			(store_add, ":fake_id", ":button_slot", 2345),
			(troop_set_slot, CCI_OBJECTS, ":button_slot", ":fake_id"),
		(try_end),
		(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
			(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 0), # An item is commissioned and completed or in progress.
			(troop_slot_eq, CCI_ARRAY_LOCATION, ":slot_no", "$current_town"), # An item is commissioned in this location.
			(val_add, ":commission_no", 1),
			
			### ADD COLLECT / CANCEL BUTTONS
			(store_add, ":button_slot",  cci_obj_button_item_0, ":commission_no"),
			(store_add, ":val_entry_no", ":button_slot", 10),
			(store_add, ":val_button_type", ":button_slot", 20),
			(troop_set_slot, CCI_OBJECTS, ":val_entry_no", ":slot_no"),
			(try_begin),
				## Commission Complete - "Collect" Button
				(troop_slot_eq, CCI_ARRAY_STATUS, ":slot_no", 0),
				(troop_set_slot, CCI_OBJECTS, ":val_button_type", 1),
				(str_store_string, s22, "@Collect"),
			(else_try),
				## Commission In Progress - "Cancel" Button
				(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 1),
				(troop_set_slot, CCI_OBJECTS, ":val_button_type", 0),
				(str_store_string, s22, "@Cancel"),
			(try_end),
			
			(store_mul, ":x_temp", ":commission_no", 85),
			(val_add, ":x_temp", 175),
			## OBJ (0 to 5) - BUTTON - COLLECT / CANCEL ITEM
			(assign, reg21, ":commission_no"),
			(str_store_string, s21, "@{s22} #{reg21}"),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_temp", 45, ":button_slot"), # COLLECT / CANCEL
			(call_script, "script_gpu_resize_object", ":button_slot", 75),
		(try_end), ## Commission Loop #2
		
		## OBJ - TEXT - ITEM MODIFIERS TITLE
		(assign, ":x_center", 800),
		(str_store_string, s21, "@Available Modifiers:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", 600, cci_obj_title_commissions, gpu_center),
		
		## OBJ - TEXT - ITEM MODIFIERS UNDERLINE DESCRIPTION
		(str_store_string, s21, "@(Only one may be selected)"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", 580, cci_obj_label_warning_1, gpu_center),
		(call_script, "script_gpu_resize_object", cci_obj_label_warning_1, 75),
		(overlay_set_color, reg1, gpu_gray),
		
		## CLEAN OUT OBJECT NUMBERS ON NON-APPLICABLE IMOD CHECKBOXES.
		(try_for_range, ":slot_no", cci_obj_checkbox_modifiers_begin, cci_val_checkbox_modifiers_begin),
			(troop_set_slot, CCI_OBJECTS, ":slot_no", 0),
		(try_end),
		
		(assign, ":y_bottom", 330),
		(assign, ":x_left",  675), # 655
		(assign, ":x_width", 290),
		(assign, ":y_width", 235),
		
		## OBJ - CONTAINER+ - IMOD SELECTION
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", cci_obj_container_imod_list),
			
			(assign, ":count", 0),
			(try_for_range, ":imod", imod_plain, imod_large_bag+1),
				## Filter for appropriate IMODs based on item type.
				(call_script, "script_cf_cci_imod_appropriate_for_item", "$temp", ":imod"),
				(val_add, ":count", 1),
			(try_end),
			
			## OBJ - CHECKBOXES - MODIFIERS
			(assign, ":pos_x", 5),
			(assign, ":x_return", ":pos_x"),
			(assign, ":y_step", 30),
			(assign, ":x_step", 150),
			(store_mul, ":pos_y", ":count", ":y_step"),
			(val_div, ":pos_y", 2),
			(assign, ":count", 0),
			
			(try_for_range, ":imod", imod_plain, imod_large_bag+1),
				## Filter for appropriate IMODs based on item type.
				(call_script, "script_cf_cci_imod_appropriate_for_item", "$temp", ":imod"),
				(val_add, ":count", 1),
				
				(store_sub, ":offset", ":imod", imod_plain),
				(store_add, ":obj_slot", cci_obj_checkbox_modifiers_begin, ":offset"),
				(store_add, ":value_slot", cci_val_checkbox_modifiers_begin, ":offset"),
				(call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
				(str_store_string, s21, s1),
				(call_script, "script_gpu_create_checkbox", ":pos_x", ":pos_y", "str_hub_s21", ":obj_slot", ":value_slot"),
				(call_script, "script_gpu_resize_object", ":obj_slot", 60),
				
				(val_add, ":pos_x", ":x_step"),
				(try_begin),
					(eq, ":count", 2),
					(assign, ":pos_x", ":x_return"),
					(val_sub, ":pos_y", ":y_step"),
					(assign, ":count", 0),
				(try_end),
			(try_end),
		(set_container_overlay, -1), ## CONTAINER- - IMOD SELECTION
		
		
		(assign, ":y_bottom", 85),
		(assign, ":x_left",  665),
		(assign, ":x_width", 300),
		(assign, ":y_width", 195),
		
		## OBJ - TEXT - SELECTED ITEM TITLE
		(str_store_string, s21, "@Item To Commission:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", 295, cci_obj_title_commissions, gpu_center),
		
		## OBJ - CONTAINER+ - SELECTED ITEM
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", cci_obj_container_selected_item),
			
			(str_store_string, s21, "@ "),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 85, 180, 0, gpu_left),
			
			## OBJ - IMAGE - SELECTED ITEM
			(assign, ":pos_x", 5),
			(assign, ":pos_y", 170),
			(assign, ":y_step", 25),
			(assign, ":x_col_1", 90),
			(assign, ":x_col_2", 165),
			(store_add, ":pos_y_temp", ":pos_y", -78),
			(troop_get_slot, ":selected_item_no", CCI_OBJECTS, cci_val_selected_item_no),
			(call_script, "script_gpu_create_mesh", "mesh_inv_slot", ":pos_x", ":pos_y_temp", 800, 800),
			## item
			(try_begin),
				(is_between, ":selected_item_no", CCI_FIRST_ITEM, CCI_LAST_ITEM),
				## OBJ - IMAGE - SELECTED ITEM
				(store_add, ":pos_x_item", ":pos_x", 40),
				(store_add, ":pos_y_item", ":pos_y_temp", 40),
				(call_script, "script_gpu_create_item_mesh", ":selected_item_no", ":pos_x_item", ":pos_y_item", 800),
				(troop_set_slot, CCI_OBJECTS, cci_obj_image_selected_item, reg1),
				
				## OBJ - TEXT - SELECTED ITEM
				(str_store_item_name, s21, ":selected_item_no"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_col_1", ":pos_y", cci_obj_label_selected_item, gpu_left),
				(call_script, "script_gpu_resize_object", cci_obj_label_selected_item, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_col_1", ":pos_y", cci_obj_label_selected_item, gpu_left),
				(call_script, "script_gpu_resize_object", cci_obj_label_selected_item, 75),
				
			(try_end),
					
			## OBJ - TEXT - SELECTED MODIFIER
			(troop_get_slot, ":selected_imod", CCI_OBJECTS, cci_val_selected_imod),
			(try_begin),
				(is_between, ":selected_imod", imod_plain, imod_large_bag+1),
				(call_script, "script_cci_describe_imod_to_s1", ":selected_imod", 1),
				(str_store_string, s21, "@{s1} (x{s2}%)"),
			(else_try),
				(str_clear, s21),
			(try_end),
			(val_sub, ":pos_y", ":y_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_col_1", ":pos_y", cci_obj_label_selected_imod, gpu_left),
			(call_script, "script_gpu_resize_object", cci_obj_label_selected_imod, 75),
			# (overlay_set_color, reg1, gpu_gray),
			
			## OBJ - LABEL - COMMISSION PRICE
			(str_store_string, s21, "@Price:"),
			(val_sub, ":pos_y", ":y_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_col_1", ":pos_y", cci_obj_label_selected_price, gpu_left),
			(call_script, "script_gpu_resize_object", cci_obj_label_selected_price, 75),
			
			## OBJ - DISPLAY - COMMISSION PRICE
			(troop_get_slot, reg21, CCI_OBJECTS, cci_val_selected_price),
			(str_store_string, s21, "@{reg21} denars"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_col_2", ":pos_y", cci_obj_label_selected_price, gpu_left),
			(call_script, "script_gpu_resize_object", cci_obj_label_selected_price, 75),
			
			## OBJ - LABEL - TIME ESTIMATE
			(str_store_string, s21, "@Estimate:"),
			(val_sub, ":pos_y", ":y_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_col_1", ":pos_y", cci_obj_label_selected_duration, gpu_left),
			(call_script, "script_gpu_resize_object", cci_obj_label_selected_duration, 75),
			
			## OBJ - DISPLAY - TIME ESTIMATE
			(troop_get_slot, ":price", CCI_OBJECTS, cci_val_selected_price),
			(call_script, "script_cci_get_workdown_rate_in_center", "$current_town", 0),
			(assign, ":hourly_workdown", reg1),
			(store_div, ":hours", ":price", ":hourly_workdown"),
			(store_div, reg21, ":hours", 24),
			(store_mod, reg22, ":hours", 24),
			(str_store_string, s21, "@{reg21} days & {reg22} hours"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_col_2", ":pos_y", cci_obj_label_selected_duration, gpu_left),
			(call_script, "script_gpu_resize_object", cci_obj_label_selected_duration, 75),
			
		(set_container_overlay, -1), ## CONTAINER- - SELECTED ITEM
		
		## OBJ - BUTTON - COMMISSION
        (str_store_string, s21, "@Commission"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 805, 35, cci_obj_button_commission), # DONE
		
      ]),
	
	(ti_on_presentation_mouse_press,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":mouse_button"),
			
			(try_begin),
				##################################
				#####      ITEM CLICKED      #####
				##################################
				## Locate the item that was clicked
				(eq, ":mouse_button", 0), # Left Button
				(assign, ":continue", 0),
				(try_for_range, ":slot_no", 0, "$temp_2"),
					(this_or_next|troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
					(troop_slot_eq, "trp_temp_array_b", ":slot_no", ":object"),
					(troop_get_slot, ":selected_item", "trp_temp_array_c", ":slot_no"),
					(is_between, ":selected_item", CCI_FIRST_ITEM, CCI_LAST_ITEM),
					(troop_set_slot, CCI_OBJECTS, cci_val_selected_item_no, ":selected_item"),
					(assign, ":continue", 1),
					(break_loop),
				(try_end),
				(eq, ":continue", 1),
				(troop_get_slot, ":imod", CCI_OBJECTS, cci_val_selected_imod),
				(call_script, "script_cci_get_commission_price", ":selected_item", ":imod"),
				(troop_set_slot, CCI_OBJECTS, cci_val_selected_price, reg1),
				(start_presentation, "prsnt_commission_requests"),
			(try_end),
		]),
		
    (ti_on_presentation_mouse_enter_leave,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":enter_leave"),

			(try_begin),
				(eq, ":enter_leave", 0),
				(neq, ":object", "$g_presentation_obj_1"),
				## ITEM SELECTION GROUP - OPEN DETAILS
				(try_for_range, ":slot_no", 0, "$temp_2"),
					(troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
					(troop_get_slot, ":item_no", "trp_temp_array_c", ":slot_no"),
					(troop_get_slot, ":target_obj", "trp_temp_array_b", ":slot_no"),
					(overlay_get_position, pos0, ":target_obj"),
					(show_item_details, ":item_no", pos0, 100),
					(assign, "$g_current_opened_item_details", ":slot_no"),
				(try_end),
				
				## SELECTED ITEM - OPEN DETAILS
				(try_begin),
					(troop_slot_eq, CCI_OBJECTS, cci_obj_image_selected_item, ":object"),
					(troop_get_slot, ":item_no", CCI_OBJECTS, cci_val_selected_item_no),
					(is_between, ":item_no", CCI_FIRST_ITEM, CCI_LAST_ITEM),
					(troop_get_slot, ":imod", CCI_OBJECTS, cci_val_selected_imod),
					(overlay_get_position, pos0, ":object"),
					(show_item_details_with_modifier, ":item_no", ":imod", pos0, 1),
					(assign, "$g_current_opened_item_details", ":object"),
				(try_end),
				
			(else_try),
				## ITEM SELECTION GROUP - CLOSE DETAILS
				(try_for_range, ":slot_no", 0, "$temp_2"),
					(troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
					(try_begin),
						(eq, "$g_current_opened_item_details", ":slot_no"),
						(close_item_details),
					(try_end),
				(try_end),
				
				## SELECTED ITEM - CLOSE DETAILS
				(try_begin),
					(troop_slot_eq, CCI_OBJECTS, cci_obj_image_selected_item, ":object"),
					(eq, "$g_current_opened_item_details", ":object"),
					(close_item_details),
				(try_end),
			(try_end),
		]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_cci_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin), ####### COMBO BUTTON - ITEM TYPE SELECTOR #######
			(eq, ":object", "$g_presentation_obj_1"),
			(assign, "$temp", ":value"),
			(start_presentation, "prsnt_commission_requests"),

		(else_try),  ####### BUTTON - DONE #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_done, ":object"),
			(presentation_set_duration, 0),
		
		(else_try),  ####### BUTTON - CANCEL COMMISSION #######
			(assign, ":found", 0),
			(try_for_range, ":slot_button_no", cci_obj_button_item_1, cci_val_item_1_entry_slot),
				(eq, ":found", 0),
				(troop_slot_eq, CCI_OBJECTS, ":slot_button_no", ":object"), # Checks which button was clicked.
				(store_add, ":slot_button_type", ":slot_button_no", 20),
				(store_add, ":slot_entry_no", ":slot_button_no", 10),
				(troop_slot_eq, CCI_OBJECTS, ":slot_button_type", 0), # Checks that this button is for an item to cancel.
				(troop_get_slot, ":entry_no", CCI_OBJECTS, ":slot_entry_no"),
				(assign, ":found", 1),
			(try_end),
			(eq, ":found", 1),
			## Alert the player to hold down the shift key if not done.
			(try_begin),
				(neg|key_is_down, key_left_shift),
				(neg|key_is_down, key_right_shift),
				(display_message, "@NOTE: You must hold down the 'shift' key while chosing to cancel an item.", gpu_debug),
			(try_end),
			## Make sure the player wants the item removed.
			(this_or_next|key_is_down, key_left_shift),
			(key_is_down, key_right_shift),
			## Remove item from queue.
			(call_script, "script_cci_clear_commission_entry", ":entry_no", 1),
			(start_presentation, "prsnt_commission_requests"),
			
		(else_try),  ####### BUTTON - COLLECT COMMISSION #######
			(assign, ":found", 0),
			(try_for_range, ":slot_button_no", cci_obj_button_item_1, cci_val_item_1_entry_slot),
				(eq, ":found", 0),
				(troop_slot_eq, CCI_OBJECTS, ":slot_button_no", ":object"), # Checks which button was clicked.
				(store_add, ":slot_button_type", ":slot_button_no", 20),
				(store_add, ":slot_entry_no", ":slot_button_no", 10),
				(troop_slot_eq, CCI_OBJECTS, ":slot_button_type", 1), # Checks that this button is for an item to collect.
				(troop_get_slot, ":entry_no", CCI_OBJECTS, ":slot_entry_no"),
				(assign, ":found", 1),
			(try_end),
			(eq, ":found", 1),
			## Alert the player to hold down the shift key if not done.
			(try_begin),
				(neg|key_is_down, key_left_shift),
				(neg|key_is_down, key_right_shift),
				(display_message, "@NOTE: You must hold down the 'shift' key while chosing to collect an item.", gpu_debug),
			(try_end),
			## Make sure the player wants the item removed.
			(this_or_next|key_is_down, key_left_shift),
			(key_is_down, key_right_shift),
			## Charge player for the remainder of the cost and deliver the item.
			(troop_get_slot, ":item_no", CCI_ARRAY_ITEM_NO, ":entry_no"),
			(troop_get_slot, ":imod", CCI_ARRAY_IMOD, ":entry_no"),
			(troop_get_slot, ":initial_cost", CCI_ARRAY_COST, ":entry_no"),
			(try_begin),
				## FILTER - Insufficient Funds.
				(store_mul, ":upfront_cost", ":initial_cost", CCI_UPFRONT_COST),
				(val_div, ":upfront_cost", 100),
				(store_sub, ":backend_cost", ":initial_cost", ":upfront_cost"),
				(call_script, "script_cf_diplomacy_treasury_verify_funds", ":backend_cost", "$current_town", FUND_FROM_EITHER, TREASURY_FUNDS_INSUFFICIENT), # diplomacy_scripts.py
				(display_message, "@WARNING - You have insufficient funds to complete the remaining payment for this item.", gpu_red),
			(else_try),
				## FILTER - Insufficient inventory space for the item.
				(store_free_inventory_capacity, ":space", "trp_player"),
				(lt, ":space", 1),
				(display_message, "@WARNING - You have insufficient inventory space to collect this item.", gpu_red),
			(else_try),
				## Charge the player.
				(call_script, "script_diplomacy_treasury_withdraw_funds", ":backend_cost", "$current_town", FUND_FROM_EITHER), # diplomacy_scripts.py
				### METRICS+ ### - MONEY SPENT ON COMMISSIONS
				(troop_get_slot, ":money_spent", METRICS_DATA, metrics_commissions_money_spent),
				(val_add, ":money_spent", ":backend_cost"),
				(troop_set_slot, METRICS_DATA, metrics_commissions_money_spent, ":money_spent"),
				(try_begin),
					(eq, "$enable_metrics", 1),
					(troop_get_slot, reg31, METRICS_DATA, metrics_commissions_money_spent),
					(store_sub, reg32, reg31, 1),
					(assign, reg33, ":backend_cost"),
					(display_message, "@METRIC (Commissions): You have spent {reg31} denar{reg32?s:} on commissions. (+{reg33})", gpu_debug),
				(try_end),
				### METRICS- ###
				## Deliver Item.
				(troop_add_item, "trp_player", ":item_no", ":imod"),
				## Remove item from queue.
				(call_script, "script_cci_clear_commission_entry", ":entry_no", 1),
				(start_presentation, "prsnt_commission_requests"),
			(try_end),
			
			
		(else_try),  ####### BUTTON - COMMISSION #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_commission, ":object"),
			(call_script, "script_cci_get_number_of_active_commissions"),
			(assign, ":global_commissions", reg1),
			(assign, ":local_commissions", reg2),
			(troop_get_slot, ":item_no", CCI_OBJECTS, cci_val_selected_item_no),
			(troop_get_slot, ":imod", CCI_OBJECTS, cci_val_selected_imod),
			(try_begin),
				# FILTER - Prevent adding a commission if the global limit has been reached.
				(ge, ":global_commissions", CCI_GOBAL_COMMISSION_LIMIT),
				(display_message, "@WARNING - Commission cannot be added due to maximum limit of active commissions reached.", gpu_red),
			(else_try),
				# FILTER - Prevent adding a commission if the local limit has been reached.
				(ge, ":local_commissions", CCI_LOCAL_COMMISSION_LIMIT),
				(str_store_party_name, s21, "$current_town"),
				(display_message, "@WARNING - Commission cannot be added due to maximum limit of commissions in {s21} has been reached.", gpu_red),
			(else_try),
				## FILTER - Unspecific Item Request
				(neg|is_between, ":item_no", CCI_FIRST_ITEM, CCI_LAST_ITEM),
				(display_message, "@WARNING - Commission cannot be added as you have not specified a valid item to create.", gpu_red),
			(else_try),
				## FILTER - Unspecific IMOD Request
				(neg|is_between, ":imod", imod_plain, imod_large_bag+1),
				(display_message, "@WARNING - Commission cannot be added as you have not specified a valid modifier for the item.", gpu_red),
			(else_try),
				## FILTER - Insufficient Funds.
				(call_script, "script_cci_get_commission_price", ":item_no", ":imod"),
				(store_mul, ":upfront_cost", reg1, CCI_UPFRONT_COST),
				(val_div, ":upfront_cost", 100),
				(call_script, "script_cf_diplomacy_treasury_verify_funds", ":upfront_cost", "$current_town", FUND_FROM_EITHER, TREASURY_FUNDS_INSUFFICIENT), # diplomacy_scripts.py
				(display_message, "@WARNING - You have insufficient funds to commission this item.", gpu_red),
			(else_try),
				## ADD COMMISION
				(call_script, "script_cci_add_new_commission", "$current_town", ":item_no", ":imod"),
				(start_presentation, "prsnt_commission_requests"),
			(try_end),
		
		(else_try), ####### CHECKBOXS - MODIFIERS ####### (ENABLING)
			(eq, ":value", 1),
			(assign, ":continue", 0),
			(try_for_range, ":slot_no", cci_obj_checkbox_modifiers_begin, cci_val_checkbox_modifiers_begin),
				(troop_slot_eq, CCI_OBJECTS, ":slot_no", ":object"),
				(store_sub, ":imod", ":slot_no", cci_obj_checkbox_modifiers_begin),
				(troop_set_slot, CCI_OBJECTS, cci_val_selected_imod, ":imod"),
				(store_add, ":val_slot", ":imod", cci_val_checkbox_modifiers_begin),
				(troop_set_slot, CCI_OBJECTS, ":val_slot", 1),
				(store_add, ":obj_slot", ":imod", cci_obj_checkbox_modifiers_begin),
				(assign, ":continue", 1),
				(break_loop),
			(try_end),
			(eq, ":continue", 1),
			## Update Other Checkboxes to Disabled
			(try_for_range, ":slot_no", cci_obj_checkbox_modifiers_begin, cci_val_checkbox_modifiers_begin),
				(neq, ":slot_no", ":obj_slot"),
				(neg|troop_slot_eq, CCI_OBJECTS, ":slot_no", 0),
				(troop_get_slot, ":obj_no", CCI_OBJECTS, ":slot_no"),
				# (start_presentation, "prsnt_commission_requests"),
				(overlay_set_val, ":obj_no", 0),
			(try_end),
			(try_for_range, ":slot_no", cci_val_checkbox_modifiers_begin, cci_val_checkbox_modifiers_end),
				(neq, ":slot_no", ":val_slot"),
				(troop_set_slot, CCI_OBJECTS, ":slot_no", 0),
			(try_end),
			## Update Selected Imod Display
			(troop_get_slot, ":obj_selected_imod", CCI_OBJECTS, cci_obj_label_selected_imod),
			(call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
			(overlay_set_text, ":obj_selected_imod", "@{s1} (x{s2}%)"),
			## Update Selected Price & Estimate
			(troop_get_slot, ":item_no", CCI_OBJECTS, cci_val_selected_item_no),
			(call_script, "script_cci_get_commission_price", ":item_no", ":imod"),
			(assign, ":price", reg1),
			(troop_set_slot, CCI_OBJECTS, cci_val_selected_price, ":price"),
			# Price
			(troop_get_slot, ":obj_price", CCI_OBJECTS, cci_obj_label_selected_price),
			(assign, reg21, ":price"),
			(overlay_set_text, ":obj_price", "@{reg21} denars"),
			# Estimate
			(troop_get_slot, ":obj_estimate", CCI_OBJECTS, cci_obj_label_selected_duration),
			(call_script, "script_cci_get_workdown_rate_in_center", "$current_town", 0),
			(assign, ":hourly_workdown", reg1),
			(store_div, ":hours", ":price", ":hourly_workdown"),
			(store_div, reg21, ":hours", 24),
			(store_mod, reg22, ":hours", 24),
			# (store_div, ":hours", ":price", CCI_HOURLY_WORKDOWN),
			# (store_div, reg21, ":hours", 24),
			# (store_mod, reg22, ":hours", 24),
			(overlay_set_text, ":obj_estimate", "@{reg21} days & {reg22} hours"),
			
		(else_try), ####### CHECKBOXS - MODIFIERS ####### (DISABLING)
			(eq, ":value", 0),
			(assign, ":continue", 0),
			(try_for_range, ":slot_no", cci_obj_checkbox_modifiers_begin, cci_val_checkbox_modifiers_begin),
				(troop_slot_eq, CCI_OBJECTS, ":slot_no", ":object"),
				(troop_set_slot, CCI_OBJECTS, cci_val_selected_imod, imod_plain),
				(assign, ":continue", 1),
				(break_loop),
			(try_end),
			(eq, ":continue", 1),
			## Update Other Checkboxes to Disabled
			(try_for_range, ":slot_no", cci_obj_checkbox_modifiers_begin, cci_val_checkbox_modifiers_begin),
				(troop_get_slot, ":obj_no", CCI_OBJECTS, ":slot_no"),
				(overlay_set_val, ":obj_no", 0),
			(try_end),
			(try_for_range, ":slot_no", cci_val_checkbox_modifiers_begin, cci_val_checkbox_modifiers_end),
				(troop_set_slot, CCI_OBJECTS, ":slot_no", 0),
			(try_end),
			## Enable IMOD_PLAIN
			(troop_set_slot, CCI_OBJECTS, cci_val_checkbox_modifiers_begin, 1), # Enabled by default.
			(troop_get_slot, ":obj_no", CCI_OBJECTS, cci_obj_checkbox_modifiers_begin),
			(overlay_set_val, ":obj_no", 1),
			## Update Selected Imod Display
			(troop_get_slot, ":obj_selected_imod", CCI_OBJECTS, cci_obj_label_selected_imod),
			(call_script, "script_cci_describe_imod_to_s1", imod_plain, 1),
			(overlay_set_text, ":obj_selected_imod", "@{s1} (x{s2}%)"),
			## Update Selected Price & Estimate
			(troop_get_slot, ":item_no", CCI_OBJECTS, cci_val_selected_item_no),
			(call_script, "script_cci_get_commission_price", ":item_no", imod_plain),
			(assign, ":price", reg1),
			(troop_set_slot, CCI_OBJECTS, cci_val_selected_price, ":price"),
			# Price
			(troop_get_slot, ":obj_price", CCI_OBJECTS, cci_obj_label_selected_price),
			(assign, reg21, ":price"),
			(overlay_set_text, ":obj_price", "@{reg21} denars"),
			# Estimate
			(troop_get_slot, ":obj_estimate", CCI_OBJECTS, cci_obj_label_selected_duration),
			(store_div, ":hours", ":price", CCI_HOURLY_WORKDOWN),
			(store_div, reg21, ":hours", 24),
			(store_mod, reg22, ":hours", 24),
			(overlay_set_text, ":obj_estimate", "@{reg21} days & {reg22} hours"),
			
		(try_end),
    ]),
  ]),
  

###########################################################################################################################
#####                                          LIST ALL COMMISSIONED ITEMS                                            #####
###########################################################################################################################

("all_commissions", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_cci_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@List of Commissioned Items"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		## OBJ - TEXT - COMMISSION REQUESTS TITLE
		# (str_store_string, s21, "@Current Commission Requests:"),
		# (call_script, "script_gpu_create_text_label", "str_hub_s21", 250, 295, cci_obj_title_commissions, gpu_left),
		
		(assign, ":y_bottom", 85),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 500),
		
		## OBJ - CONTAINER+ - ALL COMMISSIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", cci_obj_container_commissions),
			(call_script, "script_cci_get_number_of_active_commissions"),
			(assign, ":total_commissions", reg1),
			(assign, ":total_centers", reg4),
			
			(assign, ":y_step_short", 20),
			(assign, ":y_titles", 65),
			(assign, ":y_commissions", 100),
			(store_mul, ":pos_y", ":total_commissions", ":y_commissions"),
			(store_mul, reg1, ":total_centers", ":y_titles"),
			(val_add, ":pos_y", reg1),
			(val_add, ":pos_y", -85),
			
			## OBJ - LABEL - SPACER
			(str_store_string, s21, "@ "),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 10, ":pos_y", 0, gpu_left),
			(val_sub, ":pos_y", 15), # Next Line
			
			(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
				(assign, ":commission_no", 0),
				
				(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
					(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 0), # An item is commissioned and completed or in progress.
					(troop_slot_eq, CCI_ARRAY_LOCATION, ":slot_no", ":center_no"), # An item is commissioned in this location.
					(val_add, ":commission_no", 1),
					(assign, ":pos_x", 12), # Left margin
					
					(troop_get_slot, ":item_no", CCI_ARRAY_ITEM_NO, ":slot_no"),
					(troop_get_slot, ":imod", CCI_ARRAY_IMOD, ":slot_no"),
					(troop_get_slot, ":remaining_price", CCI_ARRAY_STATUS, ":slot_no"),
					(troop_get_slot, ":initial_cost", CCI_ARRAY_COST, ":slot_no"),
					
					## OBJ - HEADER - ONLY APPLY TO FIRST COMMISSION
					(try_begin),
						(eq, ":commission_no", 1),
						(assign, ":pos_x_temp", 350),
						(str_store_party_name, s22, ":center_no"),
						(store_add, ":pos_y_temp", ":pos_y", 75),
						(call_script, "script_gpu_draw_line", 740, 1, 5, ":pos_y_temp", gpu_gray), # - Footer
						(val_sub, ":pos_y_temp", 20), # Next Line
						(str_store_string, s21, "@{s22}"),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
						(call_script, "script_gpu_resize_object", 0, 125),
						# Doubled for bold effect.
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_center),
						(call_script, "script_gpu_resize_object", 0, 125),
						(val_sub, ":pos_y_temp", 15), # Next Line
						(call_script, "script_gpu_draw_line", 740, 1, 5, ":pos_y_temp", gpu_gray), # - Footer
						(val_sub, ":pos_y", ":y_titles"), # Next Line
					(try_end),
					
					## OBJ - LABEL - COMMISSION NUMBER
					(assign, reg21, ":commission_no"),
					(str_store_string, s21, "@#{reg21}"),
					(val_add, ":pos_x", 5),
					(store_add, ":pos_y_temp", ":pos_y", 40),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 85),
					# Doubled for bold effect.
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 85),
					
					## OBJ - IMAGE - SELECTED ITEM
					(val_add, ":pos_x", 25),
					(store_add, ":pos_y_temp", ":pos_y", 0),
					(call_script, "script_gpu_create_mesh", "mesh_inv_slot", ":pos_x", ":pos_y_temp", 800, 800),
					(store_add, ":pos_x_item", ":pos_x", 40),
					(store_add, ":pos_y_item", ":pos_y_temp", 40),
					(call_script, "script_gpu_create_item_mesh", ":item_no", ":pos_x_item", ":pos_y_item", 800),
					(store_add, ":slot_image", cci2_obj_items_begin, ":slot_no"),
					(troop_set_slot, CCI_OBJECTS, ":slot_image", reg1),
					(store_add, ":slot_val", cci2_val_items_begin, ":slot_no"),
					(troop_set_slot, CCI_OBJECTS, ":slot_val", ":slot_no"),
					
					## OBJ - LABEL - COMMISSIONED ITEM
					(val_add, ":pos_x", 85),
					(store_add, ":pos_y_temp", ":pos_y", 70),
					(call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
					(try_begin),
						(neq, ":imod", imod_plain),
						(str_store_string, s1, "@{s1} "),
					(else_try),
						(str_clear, s1),
					(try_end),
					(str_store_item_name, s2, ":item_no"),
					(str_store_string, s21, "@{s1}{s2}"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 85),
					# Doubled for bold effect.
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 85),
					
					## OBJ - LABEL - INVESTED PRICE
					(store_mul, ":upfront_cost", ":initial_cost", CCI_UPFRONT_COST),
					(val_div, ":upfront_cost", 100),
					(assign, reg21, ":initial_cost"),
					(store_sub, reg22, ":initial_cost", ":upfront_cost"),
					(str_store_string, s21, "@This will cost another {reg22} of a total {reg21} denars."),
					(val_sub, ":pos_y_temp", ":y_step_short"), # Next Line
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## OBJ - LABEL - COMPLETION DAYS
					(call_script, "script_cci_get_queue_delay_for_center", ":center_no", ":commission_no"),
					(assign, ":remaining_price", reg1),
					(call_script, "script_cci_get_workdown_rate_in_center", ":center_no", 0),
					(assign, ":hourly_workdown", reg1),
					(store_div, ":total_hours", ":remaining_price", ":hourly_workdown"),
					(store_div, ":days", ":total_hours", 24),
					(store_mod, ":hours", ":total_hours", 24),
					(assign, reg21, ":days"),
					(store_sub, reg22, reg21, 1),
					(assign, reg23, ":hours"),
					(store_sub, reg24, reg23, 1),
					(str_store_string, s21, "@Estimated completion in {reg21} day{reg22?s:} and {reg23} hour{reg24?s:}."),
					(try_begin),
						# (eq, ":total_hours", 0),
						(troop_slot_eq, CCI_ARRAY_STATUS, ":slot_no", 0),
						(str_store_string, s21, "@Work on this item has been completed."),
					(try_end),
					(val_sub, ":pos_y_temp", ":y_step_short"), # Next Line
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## OBJ - LABEL - ABANDONMENT DAYS
					(troop_get_slot, ":days_abandoned", CCI_ARRAY_ABANDON_TIMER, ":slot_no"),
					(try_begin),
						(ge, ":days_abandoned", 1),
						(neg|party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built), ## Royal Blacksmith prevents abandonment.
						(store_sub, reg21, CCI_ABANDONED_DAYS_LIMIT, ":days_abandoned"),
						(store_sub, reg22, reg21, 1),
						(str_store_string, s21, "@This item is will be abandoned in {reg21} day{reg22?s:}."),
						(val_sub, ":pos_y_temp", ":y_step_short"), # Next Line
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						(overlay_set_color, reg1, 10092544), # gpu_dark_red),
					(try_end),
					
					### ARTISAN INFORMATION+ ###
					(try_begin),
						(party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built), # troop_id, pos_x, pos_y, size, storage_id
						(eq, ":commission_no", 1),
						(assign, ":pos_x", 470),
						
						## OBJ - IMAGE - ARTISAN PORTRAIT
						(call_script, "script_cci_get_artisan_id", ":center_no"),
						#(call_script, "script_gpu_create_portrait", reg1, ":pos_x", ":pos_y", 250, 0),
						(call_script, "script_gpu_create_mesh", "mesh_artisan_blacksmith", ":pos_x", ":pos_y", 75, 100),
						
						## OBJ - LABEL - ARTISAN NAME
						(val_add, ":pos_x", 85),
						(call_script, "script_cci_get_artisan_id", ":center_no"),
						(assign, ":artisan", reg1),
						(str_store_troop_name, s21, ":artisan"),						
						(store_add, ":pos_y_temp", ":pos_y", 70),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						# Doubled for bold effect.
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						
						## OBJ - LABEL - ARTISAN LEVEL
						(party_get_slot, ":xp", ":center_no", slot_center_artisan_level_blacksmith),
						(call_script, "script_cci_convert_xp_to_level", ":xp"),
						(assign, ":level", reg1),
						(str_store_string, s21, "@Level {reg1} Artisan"),
						(val_sub, ":pos_y_temp", ":y_step_short"), # Next Line
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						
						(call_script, "script_cci_get_artisan_benefits", "$current_town", ":level"),
						(assign, ":build_speed", reg1),
						(assign, ":build_cost", reg2),
						
						## OBJ - LABEL - ARTISAN BUILDING SPEED
						(store_add, ":workrate", ":build_speed", CCI_HOURLY_WORKDOWN),
						(val_mul, ":workrate", 100),
						(val_div, ":workrate", CCI_HOURLY_WORKDOWN),
						(val_sub, ":workrate", 100),
						(assign, reg21, ":workrate"),
						(str_store_string, s21, "@Works {reg21}% faster."),
						(val_sub, ":pos_y_temp", ":y_step_short"), # Next Line
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						
						## OBJ - LABEL - ARTISAN COST REDUCTION
						(assign, reg21, ":build_cost"),
						(str_store_string, s21, "@Reduces costs by {reg21}%."), # Costs {reg2}% less."),
						(val_sub, ":pos_y_temp", ":y_step_short"), # Next Line
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						
					(try_end),
					### ARTISAN INFORMATION- ###
					
					(val_sub, ":pos_y", ":y_commissions"), # Next Line
					
				(try_end), ## Commission Loop
			(try_end), ## Town Loop
			
		(set_container_overlay, -1), ## CONTAINER- - CURRENT COMMISSIONS
		
		## OBJ - BUTTON - RESET REQUESTS
        (str_store_string, s21, "@Reset Requests"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 500, 35, cci2_obj_button_reset_requests), # RESET
		
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_cci_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin), ####### BUTTON - RESET REQUESTS #######  (Ticket #1535, v0.24)
			(troop_slot_eq, CCI_OBJECTS, cci2_obj_button_reset_requests, ":object"),
			(try_begin),
				(neg|key_is_down, key_left_shift),
				(neg|key_is_down, key_right_shift),
				(display_message, "@Warning - You need to hold down either SHIFT key while pressing this button to reset all commissions.", gpu_red),
				(display_message, "@Note - You will not be refunded anything for commissions in progress.  This is for save game repair only.", gpu_red),
			(else_try),
				(call_script, "script_cci_clear_all_commission_entries"), # cci_scripts.py
				(display_message, "@All commissioned items have been canceled and their requests have been reset.", gpu_green),
				(call_script, "script_cf_cci_add_event_log_entry", CCI_EVENT_COMMISSIONS_RESET, "$current_town", 0, 0),
				(start_presentation, "prsnt_all_commissions"),
			(try_end),
		(try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                                ARTISAN CRAFTER                                                  #####
###########################################################################################################################

("artisan_blacksmith", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_cci_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Royal Forge"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		(assign, ":y_step_short", 20),
		
		## OBJ - IMAGE - ARTISAN PORTRAIT
		(assign, ":pos_x", 250),
		(assign, ":pos_y", 530),
		# (call_script, "script_cci_get_artisan_id", "$current_town"),
		# (store_character_level, ":artisan_level", reg1),
		(call_script, "script_gpu_create_mesh", "mesh_artisan_blacksmith", ":pos_x", ":pos_y", 75, 100),
		
		## OBJ - LABEL - ARTISAN NAME
		(val_add, ":pos_x", 85),
		(call_script, "script_cci_get_artisan_id", "$current_town"),
		(assign, ":artisan", reg1),
		(str_store_troop_name, s21, ":artisan"),						
		(store_add, ":pos_y_temp", ":pos_y", 70),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
		# (call_script, "script_gpu_resize_object", 0, 75),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
		# (call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - ARTISAN LEVEL
		(party_get_slot, ":xp", "$current_town", slot_center_artisan_level_blacksmith),
		(call_script, "script_cci_convert_xp_to_level", ":xp"),
		(assign, ":artisan_level", reg1),
		(str_store_string, s21, "@Level {reg1} Artisan Blacksmith"),
		(val_sub, ":pos_y_temp", 25), # Next Line
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
		
		## OBJ - LABEL - ARTISAN EXPERIENCE TO LEVEL
		(party_get_slot, ":xp", "$current_town", slot_center_artisan_level_blacksmith),
		(call_script, "script_cci_convert_xp_to_level", ":xp"),
		(try_begin),
			(eq, reg1, CCI_MAXIMUM_ARTISAN_LEVEL),
			(str_store_string, s21, "@Maximum Level Achieved"),
		(else_try),
			(str_store_string, s21, "@{reg2}xp to Next Level"),
		(try_end),
		(val_sub, ":pos_y_temp", 25), # Next Line
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
		
		## OBJ - LABEL - ARTISAN INVENTORY
		# (troop_get_inventory_capacity, ":capacity", ":artisan"),
		# (store_free_inventory_capacity, ":free", ":artisan"),
		# (store_sub, ":stock", ":capacity", ":free"),
		# (assign, reg21, ":stock"),
		# (assign, reg22, ":capacity"),
		# (str_store_string, s21, "@{reg21} / {reg22} Items in Repair Inventory"),
		# (val_sub, ":pos_y_temp", 25), # Next Line
		# (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y_temp", 0, gpu_left),
		
		
		(assign, ":y_header", 505),
		## OBJ - TITLE - ARTISAN LEVEL
		(str_store_string, s21, "@LEVEL"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 270, ":y_header", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 270, ":y_header", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - TITLE - BUILD SPEED
		(str_store_string, s21, "@WORKRATE"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 350, ":y_header", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 350, ":y_header", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - TITLE - BUILD COST
		(str_store_string, s21, "@COST"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 458, ":y_header", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 458, ":y_header", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 420),
		
		## OBJ - CONTAINER+ - ARTISAN LEVEL INFO
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", cci_obj_container_commissions),
			(assign, ":y_step_short", 20),
			(store_mul, ":pos_y", CCI_MAXIMUM_ARTISAN_LEVEL, ":y_step_short"),
			(val_add, ":pos_y", 5),
			
			## OBJ - LABEL - SPACER
			(str_store_string, s21, "@ "),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 10, ":pos_y", 0, gpu_left),
			(val_sub, ":pos_y", 5), # Next Line
			
			(try_for_range, ":level", 1, CCI_MAXIMUM_ARTISAN_LEVEL+1),
				
				(try_begin),
					(eq, ":artisan_level", ":level"),
					(assign, ":level_color", gpu_blue),
				(else_try),
					(assign, ":level_color", gpu_black),
				(try_end),
				
				## OBJ - LABEL - LEVEL NUMBER
				(assign, reg21, ":level"),
				(assign, ":pos_x", 25),
				(str_store_string, s21, "@{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, ":level_color"),
				
				(call_script, "script_cci_get_artisan_benefits", "$current_town", ":level"),
				(assign, ":build_speed", reg1),
				(assign, ":build_cost", reg2),
				
				## OBJ - LABEL - SPEED BONUS
				(store_add, ":workrate", ":build_speed", CCI_HOURLY_WORKDOWN),
				(val_mul, ":workrate", 100),
				(val_div, ":workrate", CCI_HOURLY_WORKDOWN),
				(val_sub, ":workrate", 100),
				(assign, reg21, ":workrate"),
				(val_add, ":pos_x", 65),
				(str_store_string, s21, "@+{reg21}%"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, ":level_color"),
				
				## OBJ - LABEL - SPEED BONUS
				(val_add, ":pos_x", 5),
				(str_store_string, s21, "@Faster"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, ":level_color"),
				
				## OBJ - LABEL - BUILDING COST BONUS
				(assign, reg21, ":build_cost"),
				(val_add, ":pos_x", 95),
				(str_store_string, s21, "@-{reg21}%"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, ":level_color"),
				
				## OBJ - TEXT - BUILDING COST BONUS
				(val_add, ":pos_x", 5),
				(str_store_string, s21, "@Mark-up"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, ":level_color"),
				
				## OBJ - TEXT - SPECIAL BONUSES
				(val_add, ":pos_x", 70),
				(try_begin),
					(eq, ":level", 1),
					(str_store_string, s21, "@ "),
				(else_try),
					(eq, ":level", 2),
					(str_store_string, s21, "@ "),
				(else_try),
					(eq, ":level", 3),
					(str_store_string, s21, "@+6% chance of +300% work for one hour."),
				(else_try),
					(eq, ":level", 4),
					(str_store_string, s21, "@+5% experience gain."),
				(else_try),
					(eq, ":level", 5),
					(str_store_string, s21, "@+4% chance that a repaired item will improve beyond plain quality."),
				(else_try),
					(eq, ":level", 6),
					(str_store_string, s21, "@+9% chance of +300% work for one hour."),
				(else_try),
					(eq, ":level", 7),
					(str_store_string, s21, "@+10% experience gain."),
				(else_try),
					(eq, ":level", 8),
					(str_store_string, s21, "@+6% chance that a repaired item will improve beyond plain quality."),
				(else_try),
					(eq, ":level", 9),
					(str_store_string, s21, "@+9% chance of +400% work for one hour."),
				(else_try),
					(eq, ":level", 10),
					(str_store_string, s21, "@+15% experience gain."),
				(else_try),
					(eq, ":level", 11),
					(str_store_string, s21, "@+8% chance that a repaired item will improve beyond plain quality."),
				(else_try),
					(eq, ":level", 12),
					(str_store_string, s21, "@+12% chance of +400% work for one hour."),
				(else_try),
					(eq, ":level", 13),
					(str_store_string, s21, "@+20% experience gain."),
				(else_try),
					(eq, ":level", 14),
					(str_store_string, s21, "@+10% chance that a repaired item will improve beyond plain quality."),
				(else_try),
					(eq, ":level", 15),
					(str_store_string, s21, "@+15% chance of +400% work for one hour."),
				(else_try),
					(eq, ":level", 16),
					(str_store_string, s21, "@+25% experience gain."),
				(else_try),
					(eq, ":level", 17),
					(str_store_string, s21, "@+12% chance that a repaired item will improve beyond plain quality."),
				(else_try),
					(eq, ":level", 18),
					(str_store_string, s21, "@+15% chance of +500% work for one hour."),
				(else_try),
					(eq, ":level", 19),
					(str_store_string, s21, "@+30% experience gain."),
				(else_try),
					(eq, ":level", 20),
					(str_store_string, s21, "@+15% chance that a repaired item will improve beyond plain quality."),
				(else_try),
					(str_store_string, s21, "@ERROR - Undefined level bonus."),
				(try_end),
				
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(store_sub, ":bonus_lower", ":artisan_level", 2),
				(val_max, ":bonus_lower", 1),
				(store_add, ":bonus_upper", ":artisan_level", 1),
				(try_begin),
					(is_between, ":level", ":bonus_lower", ":bonus_upper"),
					(assign, ":level_color", gpu_blue),
				(else_try),
					(assign, ":level_color", gpu_black),
				(try_end),
				
				(overlay_set_color, reg1, ":level_color"),
				
				(val_sub, ":pos_y", ":y_step_short"), # Next Line
			(try_end),
			
		(set_container_overlay, -1), ## CONTAINER- - ARTISAN LEVEL INFO
		
		(try_begin),
			(this_or_next|ge, BETA_TESTING_MODE, 1),
			(ge, DEBUG_CCI, 1),
			(str_store_string, s21, "@Reset Artisan "),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 505, 35, cci3_obj_button_reset_xp),
			
			(str_store_string, s21, "@Add 150XP "),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 680, 35, cci3_obj_button_add_xp),
			
			(str_store_string, s21, "@Remove 150XP "),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 855, 35, cci3_obj_button_remove_xp),
			
			
		(try_end),
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_cci_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### BUTTON - ADD TEST EXPERIENCE #######
			(troop_slot_eq, CCI_OBJECTS, cci3_obj_button_add_xp, ":object"),
			(call_script, "script_cci_give_artisan_xp", "$current_town", 150),
			(start_presentation, "prsnt_artisan_blacksmith"),
			
		(else_try),  ####### BUTTON - REMOVE TEST EXPERIENCE #######
			(troop_slot_eq, CCI_OBJECTS, cci3_obj_button_remove_xp, ":object"),
			(call_script, "script_cci_give_artisan_xp", "$current_town", -150),
			(start_presentation, "prsnt_artisan_blacksmith"),
			
		(else_try),  ####### BUTTON - RESET ARTISAN EXPERIENCE #######
			(troop_slot_eq, CCI_OBJECTS, cci3_obj_button_reset_xp, ":object"),
			(call_script, "script_cci_reset_artisan_in_center", "$current_town"),
			(start_presentation, "prsnt_artisan_blacksmith"),
			
		(try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                                   EVENT LOG                                                     #####
###########################################################################################################################

("cci_event_log", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_cci_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Event Log"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		(assign, ":y_step_short", 20),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 535),
		
		## OBJ - CONTAINER+ - ARTISAN LEVEL INFO
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", cci_obj_container_commissions),
			## COUNT RELEVANT ENTRIES
			(assign, ":relevant_entries", 0),
			(try_for_range, ":entry_no", 0, CCI_EVENT_LOG_MAXIMUM_ENTRIES),
				(le, ":entry_no", "$cci_event_log_entries"),
				(troop_slot_ge, CCI_LOG_EVENT, ":entry_no", CCI_EVENT_COMMISSION_COMPLETED),
				(this_or_next|troop_slot_eq, CCI_LOG_LOCATION, ":entry_no", "$current_town"),
				(troop_slot_eq, CCI_OBJECTS, cci4_val_display_setting, 1), # Display all locations.
				(val_add, ":relevant_entries", 1),
			(try_end),
			(assign, ":y_step_short", 20),
			(store_mul, ":pos_y", ":relevant_entries", ":y_step_short"),
			(val_add, ":pos_y", 5),
			
			## OBJ - LABEL - SPACER
			(str_store_string, s21, "@ "),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 10, ":pos_y", 0, gpu_left),
			(val_sub, ":pos_y", 5), # Next Line
			
			## EVENT ENTRIES LOOP
			(try_for_range, ":entry_no", 0, CCI_EVENT_LOG_MAXIMUM_ENTRIES),
				(le, ":entry_no", "$cci_event_log_entries"),
				(this_or_next|troop_slot_eq, CCI_LOG_LOCATION, ":entry_no", "$current_town"),
				(troop_slot_eq, CCI_OBJECTS, cci4_val_display_setting, 1), # Display all locations.
				(troop_slot_ge, CCI_LOG_EVENT, ":entry_no", CCI_EVENT_COMMISSION_COMPLETED),
				
				(try_begin),
					(troop_slot_eq, CCI_OBJECTS, cci4_val_display_setting, 1), # Display all locations.
					(troop_slot_eq, CCI_LOG_LOCATION, ":entry_no", "$current_town"),
					(assign, ":log_color", gpu_blue),
				(else_try),
					(assign, ":log_color", gpu_black),
				(try_end),
				
				## OBJ - LABEL - DATE
				(troop_get_slot, ":hours", CCI_LOG_DATE, ":entry_no"),
				(str_store_date, s21, ":hours"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", 10, ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, ":log_color"),
				
				## OBJ - LABEL - DESCRIPTION OF EVENT
				(call_script, "script_cci_convert_entry_to_string", ":entry_no"),
				(str_store_string, s21, s1),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", 150, ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, ":log_color"),
				
				(val_sub, ":pos_y", ":y_step_short"), # Next Line
			(try_end),
			
		(set_container_overlay, -1), ## CONTAINER- - ARTISAN LEVEL INFO
		
		(try_begin),
			(troop_slot_eq, CCI_OBJECTS, cci4_val_display_setting, 1),
			(str_store_string, s21, "@Display This Location Only "),
		(else_try),
			(str_store_string, s21, "@Display All Locations "),
		(try_end),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 855, 35, cci4_obj_button_display_toggle),
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_cci_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### BUTTON - DISPLAY TOGGLE (Current Location) #######
			(troop_slot_eq, CCI_OBJECTS, cci4_obj_button_display_toggle, ":object"),
			(troop_slot_eq, CCI_OBJECTS, cci4_val_display_setting, 0), # Currently displaying location only.
			(troop_set_slot, CCI_OBJECTS, cci4_val_display_setting, 1), # Display all locations.
			(start_presentation, "prsnt_cci_event_log"),
			
		(else_try),  ####### BUTTON - DISPLAY TOGGLE (All Locations) #######
			(troop_slot_eq, CCI_OBJECTS, cci4_obj_button_display_toggle, ":object"),
			(troop_slot_eq, CCI_OBJECTS, cci4_val_display_setting, 1), # Currently displaying all locations.
			(troop_set_slot, CCI_OBJECTS, cci4_val_display_setting, 0), # Display current location only.
			(start_presentation, "prsnt_cci_event_log"),
			
		(try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                                EMBLEM OPTIONS                                                   #####
###########################################################################################################################

("cci_emblem_options", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_cci_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Emblem Options"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, cci_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", cci_obj_main_title, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		# (assign, ":y_step_short", 20),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 515),
		
		## OBJ - CONTAINER+ - EMBLEM OPTIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", cci_obj_container_commissions),
		
			(assign, ":pos_y", 475),
			(assign, ":y_line_step", 20),
			(assign, ":x_desc", 110),
			(assign, ":y_option_step", 70),
			
			##############
			# OPTION #1  #
			##############
			(str_store_string, s21, "@Artisan Experience Boost"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", cci5_obj_button_option_1, EMBLEM_COST_BOOST_ARTISAN_XP), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Instantly grants the artisan crafter of this location "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@1000 experience which improves the rate that commissions "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@or repairs are completed and reduces their cost."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Prerequisite: You must have a Royal Forge built here."),
			(val_sub, ":pos_y", 25),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Prerequisite:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(party_get_slot, ":xp", "$current_town", slot_center_artisan_level_blacksmith),
			(call_script, "script_cci_convert_xp_to_level", ":xp"), # Stores level to reg1.
			(val_min, reg1, CCI_MAXIMUM_ARTISAN_LEVEL), # Block anything past level 20.
			(str_store_string, s21, "@Status: Your crafter is currently level {reg1}."),
			(try_begin),
				(ge, reg1, CCI_MAXIMUM_ARTISAN_LEVEL),
				(str_store_string, s21, "@Status: Your crafter is already at maximum level."),
			(try_end),
			(val_sub, ":pos_y", 25),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			##############
			# OPTION #2  #
			##############
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Production Boost"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", cci5_obj_button_option_2, EMBLEM_COST_COMMISSION_PRODUCTION), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@The production rate on commission or repair work will be "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@increased by 30% for a period of one week."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(party_get_slot, reg21, "$current_town", slot_center_commission_boost_duration),
			(try_begin),
				(ge, reg21, 1),
				(store_sub, reg22, reg21, 1),
				(str_store_string, s21, "@Status: Currently {reg21} hour{reg22?s:} remain for this boost."),
			(else_try),
				(str_store_string, s21, "@Status: This boost is not currently active here."),
			(try_end),
			(val_sub, ":pos_y", 25),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			##############
			# OPTION #3  #
			##############
			(try_begin),
				(this_or_next|ge, BETA_TESTING_MODE, 1),
				(ge, DEBUG_CCI, 1),
				(val_sub, ":pos_y", ":y_option_step"),
				(str_store_string, s21, "@Instant Royal Forge (Cheat)"),
				(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", cci5_obj_button_option_3, EMBLEM_COST_COMMISSION_PRODUCTION), # emblem_scripts.py
				
				## OBJ - TEXT - TEXT LINE
				(str_store_string, s21, "@This will instantly create a royal forge here for testing. "),
				(val_sub, ":pos_y", ":y_line_step"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
			(try_end),
			
		(set_container_overlay, -1), ## CONTAINER- - EMBLEM OPTIONS
		
		(try_begin),
			(this_or_next|ge, BETA_TESTING_MODE, 1),
			(ge, DEBUG_CCI, 1),
			(str_store_string, s21, "@Gain 1 Emblem "),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 855, 35, cci5_obj_button_debug_gain_emblem),
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
		
		(call_script, "script_cci_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### BUTTON - OPTION 1 (+XP to Artisan) #######
			(troop_slot_eq, CCI_OBJECTS, cci5_obj_button_option_1, ":object"),
			(try_begin), # Prerequisite - Royal Forge improvement must be built here.
				(neg|party_slot_ge, "$current_town", slot_center_has_royal_forge, cis_built),
				(display_message, "@Warning: You must have a royal forge built here to use this option.", gpu_red),
			(else_try), # Filter - Prevent spending an emblem if the crafter is already maximum level.
				(party_get_slot, ":xp", "$current_town", slot_center_artisan_level_blacksmith),
				(call_script, "script_cci_convert_xp_to_level", ":xp"), # Stores level to reg1.
				(ge, reg1, CCI_MAXIMUM_ARTISAN_LEVEL), # Block anything past level 20.
				(display_message, "@Warning: Your artisan crafter is already at maximum level.", gpu_red),
			(else_try),
				(party_slot_ge, "$current_town", slot_center_has_royal_forge, cis_built),
				(call_script, "script_cci_give_artisan_xp", "$current_town", 1000),
				(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_BOOST_ARTISAN_XP), # emblem_scripts.py
				(start_presentation, "prsnt_cci_emblem_options"),
			(try_end),
			
		(else_try),  ####### BUTTON - OPTION 2 (Production Boost) #######
			(troop_slot_eq, CCI_OBJECTS, cci5_obj_button_option_2, ":object"),
			(party_get_slot, ":hours", "$current_town", slot_center_commission_boost_duration),
			(try_begin),
				(lt, ":hours", 1),
				(call_script, "script_cf_cci_add_event_log_entry", CCI_EVENT_LOG_PRODUCTION_BOOST_BEGIN, "$current_town", 0, 0),
			(try_end),
			(val_add, ":hours", 24*7),
			(party_set_slot, "$current_town", slot_center_commission_boost_duration, ":hours"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_COMMISSION_PRODUCTION), # emblem_scripts.py
			(display_message, "@Commission and repair production in this fief has been boosted for one week.", gpu_green),
			(start_presentation, "prsnt_cci_emblem_options"),
			
		(else_try),  ####### BUTTON - OPTION 3 (CHEAT: Instant Royal Forge) #######
			(troop_slot_eq, CCI_OBJECTS, cci5_obj_button_option_3, ":object"),
			(this_or_next|ge, BETA_TESTING_MODE, 1),
			(ge, DEBUG_CCI, 1),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_has_royal_forge, cis_built),
				(display_message, "@Warning: A royal forge has already been built in this location.", gpu_red),
			(else_try),
				(party_set_slot, "$current_town", slot_center_has_royal_forge, cis_built),
				(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_COMMISSION_PRODUCTION), # emblem_scripts.py
				(display_message, "@A royal forge has been constructed here.", gpu_green),
				(start_presentation, "prsnt_cci_emblem_options"),
			(try_end),
			
		(else_try),  ####### BUTTON - DEBUGGING +1 EMBLEM #######
			(troop_slot_eq, CCI_OBJECTS, cci5_obj_button_debug_gain_emblem, ":object"),
			(this_or_next|ge, BETA_TESTING_MODE, 1),
			(ge, DEBUG_CCI, 1),
			(call_script, "script_emblem_award_to_player", 1), # emblem_scripts.py
			(start_presentation, "prsnt_cci_emblem_options"),
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