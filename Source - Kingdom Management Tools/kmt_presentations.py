# Kingdom Management Tools (1.0) by Windyplains

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

# script_gpu_create_checkbox     - pos_x, pos_y, label, storage_slot, value_slot
# script_gpu_create_mesh         - mesh_id, pos_x, pos_y, size_x, size_y
# script_gpu_create_portrait     - troop_id, pos_x, pos_y, size, storage_id
# script_gpu_create_button       - title, pos_x, pos_y, storage_id
# script_gpu_create_text_label   - title, pos_x, pos_y, storage_id, design
# script_gpu_resize_object       - storage_id, percent size
# script_gpu_draw_line           - x length, y length, pos_x, pos_y, color
# script_gpu_container_heading   - pos_x, pos_y, size_x, size_y, storage_id
# script_gpu_create_slider       - min, max, pos_x, pos_y, storage_id, value_id

presentations = [
###########################################################################################################################
#####                                                 FIEF EXCHANGE                                                   #####
###########################################################################################################################

("kmt_fief_exchange", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_kmt_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Fief Exchange"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title2, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		## OBJ - PORTRAIT - LEFT LORD IMAGE
		(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_left),
		(call_script, "script_gpu_create_portrait", ":troop_no", 370, 535, 250, kmt3_obj_portrait_lord_left),
		
		## OBJ - MENU - LEFT LORD NAME
		(create_combo_label_overlay, reg1),
		(troop_set_slot, KMT_OBJECTS, kmt3_obj_menu_lord_left, reg1),
		(position_set_x, pos1, 410),
		(position_set_y, pos1, 495),
		(overlay_set_position, reg1, pos1),
		(str_store_troop_name, s21, "trp_player"),
		(overlay_add_item, reg1, "@{s21}"),
		(assign, ":slot_counter", 0),
		(store_add, ":slot_storage", kmt3_val_lord_selector_begin, ":slot_counter"),
		(troop_set_slot, KMT_OBJECTS, ":slot_storage", "trp_player"),
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":faction_no", ":troop_no"),
			(eq, ":faction_no", "$players_kingdom"),
			(str_store_troop_name, s21, ":troop_no"),
			(overlay_add_item, reg1, "@{s21}"),
			# Store the troop_no so we can recall it later.  The right person selector uses the same list, but it only needs creating here.
			(val_add, ":slot_counter", 1),
			(store_add, ":slot_storage", kmt3_val_lord_selector_begin, ":slot_counter"),
			(troop_set_slot, KMT_OBJECTS, ":slot_storage", ":troop_no"),
		(try_end),
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt3_obj_menu_lord_left),
		(troop_get_slot, ":value", KMT_OBJECTS, kmt3_val_menu_lord_left),
		(overlay_set_val, ":obj_no", ":value"),
		
		
		## OBJ - PORTRAIT - RIGHT LORD IMAGE
		(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_right),
		(call_script, "script_gpu_create_portrait", ":troop_no", 750, 535, 250, kmt3_obj_portrait_lord_left),
		
		## OBJ - MENU - RIGHT LORD NAME
		(create_combo_label_overlay, reg1),
		(troop_set_slot, KMT_OBJECTS, kmt3_obj_menu_lord_right, reg1),
		(position_set_x, pos1, 785),
		(position_set_y, pos1, 495),
		(overlay_set_position, reg1, pos1),
		(str_store_troop_name, s21, "trp_player"),
		(overlay_add_item, reg1, "@{s21}"),
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":faction_no", ":troop_no"),
			(eq, ":faction_no", "$players_kingdom"),
			(str_store_troop_name, s21, ":troop_no"),
			(overlay_add_item, reg1, "@{s21}"),
		(try_end),
		(troop_get_slot, ":value", KMT_OBJECTS, kmt3_val_menu_lord_right),
		(overlay_set_val, reg1, ":value"),
		# (call_script, "script_gpu_resize_object", kmt3_obj_menu_lord_right, 75),
		
		## VALUE STORAGE - POPULATE RIGHT & LEFT LORD FIEF LIST
		# Left Lord
		(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_left),
		(assign, ":slot_no", kmt3_val_left_fiefs_begin),
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
			(troop_set_slot, KMT_OBJECTS, ":slot_no", ":center_no"),
			(val_add, ":slot_no", 1),
		(try_end),
		(val_sub, ":slot_no", 1),
		(troop_set_slot, KMT_OBJECTS, kmt3_val_left_fief_count, ":slot_no"),
		# Right Lord
		(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_right),
		(assign, ":slot_no", kmt3_val_right_fiefs_begin),
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
			(troop_set_slot, KMT_OBJECTS, ":slot_no", ":center_no"),
			(val_add, ":slot_no", 1),
		(try_end),
		(val_sub, ":slot_no", 1),
		(troop_set_slot, KMT_OBJECTS, kmt3_val_right_fief_count, ":slot_no"),
		
		## OBJ - CONTAINER+ - LEFT OPTION LIST (Section 1)
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 1),
			(assign,  ":y_top",    425),
			(assign,  ":y_limit",  295),
		(else_try),
			(assign,  ":y_top",    450),
			(assign,  ":y_limit",  320),
		(try_end),
		(assign,  ":y_bottom", 110),
		(assign,  ":x_left",   250),
		(assign,  ":x_right",  550),
		(store_sub, ":x_width", ":x_right", ":x_left"),
		(store_sub, ":y_width", ":y_top", ":y_bottom"),
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", kmt3_obj_container_left_options),
			(assign, ":pos_y", 0), # 500),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_left_opt_1_type, ":pos_y"),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_left_opt_2_type, reg1),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_left_opt_3_type, reg1),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_left_opt_4_type, reg1),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_left_opt_5_type, reg1),
			(assign, ":pos_y", reg1),
			(val_max, ":pos_y", ":y_limit"), # Vertical spacing of the container to ensure options are at least at the top.
			
			## LEFT OPTIONS
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_left_opt_1_type, ":pos_y"), # LEFT OPTION #1
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_left_opt_2_type, reg1),     # LEFT OPTION #2
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_left_opt_3_type, reg1),     # LEFT OPTION #3
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_left_opt_4_type, reg1),     # LEFT OPTION #4
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_left_opt_5_type, reg1),     # LEFT OPTION #5
			
		(set_container_overlay, -1), ## CONTAINER- - LEFT OPTION LIST
		
		## OBJ - TEXT - LEFT RATING LABEL
		(assign, ":pos_y_rating", 470),
		(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_left),
		(str_store_troop_name, s22, ":troop_no"),
		(str_store_string, s21, "@{s22}'s offer rating:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_left", ":pos_y_rating", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - TEXT - LEFT RATING VALUE
		# (troop_set_slot, KMT_OBJECTS, kmt3_val_left_rating, 3000000), # TODO: Implement rating system.
		(troop_get_slot, reg21, KMT_OBJECTS, kmt3_val_left_rating),
		(str_store_string, s21, "@{reg21}"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_right", ":pos_y_rating", kmt3_obj_left_rating, gpu_right),
		(call_script, "script_gpu_resize_object", kmt3_obj_left_rating, 75),
		
		## OBJ - TEXT - LEFT FORCED EXCHANGE PENALTY LABEL (Ruler Mode)
		(assign, ":pos_y_forced", 445),
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 1),
			(call_script, "script_kmt_describe_relation_penalty_for_offer", kmt3_val_lord_left),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_left", ":pos_y_forced", kmt3_obj_left_label_forced_loss, gpu_left),
			(call_script, "script_gpu_resize_object", kmt3_obj_left_label_forced_loss, 75),
		(try_end),
		
		## OBJ - CONTAINER+ - RIGHT OPTION LIST (Section 1)
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 1),
			(assign,  ":y_top",    425),
			(assign,  ":y_limit",  295),
		(else_try),
			(assign,  ":y_top",    450),
			(assign,  ":y_limit",  320),
		(try_end),
		(assign,  ":y_bottom", 110),
		(assign,  ":x_left",   630),
		(assign,  ":x_right",  930),
		(store_sub, ":x_width", ":x_right", ":x_left"),
		(store_sub, ":y_width", ":y_top", ":y_bottom"),
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", kmt3_obj_container_right_options),
			(assign, ":pos_y", 0), # 500),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_right_opt_1_type, ":pos_y"),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_right_opt_2_type, reg1),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_right_opt_3_type, reg1),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_right_opt_4_type, reg1),
			(call_script, "script_kmt_get_option_spacing", kmt3_val_right_opt_5_type, reg1),
			(assign, ":pos_y", reg1),
			(val_max, ":pos_y", ":y_limit"), # Vertical spacing of the container to ensure options are at least at the top.
			
			## RIGHT OPTIONS
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_right_opt_1_type, ":pos_y"), # RIGHT OPTION #1
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_right_opt_2_type, reg1),     # RIGHT OPTION #2
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_right_opt_3_type, reg1),     # RIGHT OPTION #3
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_right_opt_4_type, reg1),     # RIGHT OPTION #4
			(call_script, "script_kmt_create_exchange_option_controls", kmt3_val_right_opt_5_type, reg1),     # RIGHT OPTION #5
			
		(set_container_overlay, -1), ## CONTAINER- - RIGHT OPTION LIST
		
		## OBJ - TEXT - RIGHT RATING LABEL
		(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_right),
		(str_store_troop_name, s22, ":troop_no"),
		(str_store_string, s21, "@{s22}'s offer rating:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_left", ":pos_y_rating", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - TEXT - RIGHT RATING VALUE
		# (troop_set_slot, KMT_OBJECTS, kmt3_val_right_rating, 4000000), # TODO: Implement rating system.
		(troop_get_slot, reg21, KMT_OBJECTS, kmt3_val_right_rating),
		(str_store_string, s21, "@{reg21}"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_right", ":pos_y_rating", kmt3_obj_right_rating, gpu_right),
		(call_script, "script_gpu_resize_object", kmt3_obj_right_rating, 75),
		
		## OBJ - TEXT - RIGHT FORCED EXCHANGE PENALTY LABEL (Ruler Mode)
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 1),
			(call_script, "script_kmt_describe_relation_penalty_for_offer", kmt3_val_lord_right),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_left", ":pos_y_forced", kmt3_obj_right_label_forced_loss, gpu_left),
			(call_script, "script_gpu_resize_object", kmt3_obj_right_label_forced_loss, 75),
		(try_end),
		
		## OBJ - BUTTON - MAKE OFFER
        (str_store_string, s21, "@Make Offer"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 400, 35, kmt3_obj_button_make_offer), # MAKE OFFER
		
		## OBJ - BUTTON - FORCE EXCHANGE (Ruler Mode)
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 1),
			(str_store_string, s21, "@Force Exchange"),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 790, 35, kmt3_obj_button_force_exchange), # FORCE EXCHANGE
		(try_end),
		
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_kmt_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin), ####### COMBO BUTTON - LEFT LORD SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_menu_lord_left, ":object"),
			(try_begin),
				(call_script, "script_cf_qus_player_is_king", 1), # Left selector can only be moved from player if he is a king.
				(store_add, ":storage_troop_no", kmt3_val_lord_selector_begin, ":value"),
				(troop_get_slot, ":troop_no", KMT_OBJECTS, ":storage_troop_no"),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_menu_lord_left, ":value"),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_lord_left, ":troop_no"),
				# Reset offer types for this side
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_opt_1_type, KMT_OPTION_NONE),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_opt_2_type, KMT_OPTION_NONE),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_opt_3_type, KMT_OPTION_NONE),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_opt_4_type, KMT_OPTION_NONE),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_opt_5_type, KMT_OPTION_NONE),
			(else_try),
				(display_message, "@Warning - Unless you are a ruler, you may not select a different vassal on the left side.", gpu_red),
			(try_end),
			(start_presentation, "prsnt_kmt_fief_exchange"),
			
		(else_try), ####### COMBO BUTTON - RIGHT LORD SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_menu_lord_right, ":object"),
			(store_add, ":storage_troop_no", kmt3_val_lord_selector_begin, ":value"),
			(troop_get_slot, ":troop_no", KMT_OBJECTS, ":storage_troop_no"),
			# Player can't be on the right side of these options.
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(troop_get_slot, ":old_value", KMT_OBJECTS, kmt3_val_menu_lord_right),
				(overlay_set_val, ":object", ":old_value"),
			(try_end),
			(neq, ":troop_no", "trp_player"),
			(troop_set_slot, KMT_OBJECTS, kmt3_val_menu_lord_right, ":value"),
			(troop_set_slot, KMT_OBJECTS, kmt3_val_lord_right, ":troop_no"),
			# Reset offer types for this side
			(troop_set_slot, KMT_OBJECTS, kmt3_val_right_opt_1_type, KMT_OPTION_NONE),
			(troop_set_slot, KMT_OBJECTS, kmt3_val_right_opt_2_type, KMT_OPTION_NONE),
			(troop_set_slot, KMT_OBJECTS, kmt3_val_right_opt_3_type, KMT_OPTION_NONE),
			(troop_set_slot, KMT_OBJECTS, kmt3_val_right_opt_4_type, KMT_OPTION_NONE),
			(troop_set_slot, KMT_OBJECTS, kmt3_val_right_opt_5_type, KMT_OPTION_NONE),
			(start_presentation, "prsnt_kmt_fief_exchange"),
			
		(else_try), ####### COMBO BUTTON - LEFT OPTION 1 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_1_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_left_opt_1_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - LEFT OPTION 2 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_2_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_left_opt_2_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - LEFT OPTION 3 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_3_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_left_opt_3_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - LEFT OPTION 4 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_4_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_left_opt_4_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - LEFT OPTION 5 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_5_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_left_opt_5_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - RIGHT OPTION 1 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_1_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_right_opt_1_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - RIGHT OPTION 2 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_2_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_right_opt_2_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - RIGHT OPTION 3 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_3_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_right_opt_3_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - RIGHT OPTION 4 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_4_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_right_opt_4_type, ":value"),
			
		(else_try), ####### COMBO BUTTON - RIGHT OPTION 5 SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_5_type, ":object"),
			(call_script, "script_kmt_handle_option_change", kmt3_val_right_opt_5_type, ":value"),
			
		(else_try), ####### CASH OPTION - SLIDER #######
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_1, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_2, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_3, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_4, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_5, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_1, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_2, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_3, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_4, ":object"),
			(             troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_5, ":object"),
			# Acquire correct slot number from object clicked.
			(assign, ":slot_base", 0),
			(try_for_range, ":slot_no", kmt3_obj_left_opt_1, kmt3_obj_right_opt_5+1),
				(eq, ":slot_base", 0),
				(troop_slot_eq, KMT_OBJECTS, ":slot_no", ":object"),
				(assign, ":slot_base", ":slot_no"),
			(try_end),
			# Filter - Correct slider type.
			(store_sub, ":offset", kmt3_val_left_opt_1_type, kmt3_obj_left_opt_1),
			(store_add, ":slot_type", ":slot_base", ":offset"),
			(troop_slot_eq, KMT_OBJECTS, ":slot_type", KMT_OPTION_MONEY),
			# Store our new offered amount.
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_obj_left_opt_1),
			(store_add, ":slot_value", ":slot_base", ":offset"),
			(troop_set_slot, KMT_OBJECTS, ":slot_value", ":value"),
			# Update slider label.
			(store_sub, ":offset", kmt3_obj_left_opt_1_slider_label, kmt3_obj_left_opt_1),
			(store_add, ":slot_object", ":slot_base", ":offset"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, ":slot_object"),
			(store_sub, reg22, ":value", 1),
			(assign, reg21, ":value"),
			(str_store_string, s21, "@{reg21} denar{reg22?s:}"),
			(overlay_set_text, ":obj_no", s21),
			# Repeated for bold effect.
			(store_sub, ":offset", kmt3_obj_left_bold_effect, kmt3_obj_left_opt_1),
			(store_add, ":slot_object", ":slot_base", ":offset"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, ":slot_object"),
			(overlay_set_text, ":obj_no", s21),
			# Update ratings.
			(call_script, "script_kmt_get_offer_ratings"),
			
		(else_try), ####### FIEF OPTION - SLIDER #######
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_1, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_2, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_3, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_4, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_5, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_1, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_2, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_3, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_4, ":object"),
			(             troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_5, ":object"),
			# Acquire correct slot number from object clicked.
			(assign, ":slot_base", 0),
			(try_for_range, ":slot_no", kmt3_obj_left_opt_1, kmt3_obj_right_opt_5+1),
				(eq, ":slot_base", 0),
				(troop_slot_eq, KMT_OBJECTS, ":slot_no", ":object"),
				(assign, ":slot_base", ":slot_no"),
			(try_end),
			# Filter - Correct slider type.
			(store_sub, ":offset", kmt3_val_left_opt_1_type, kmt3_obj_left_opt_1),
			(store_add, ":slot_type", ":slot_base", ":offset"),
			(troop_slot_eq, KMT_OBJECTS, ":slot_type", KMT_OPTION_FIEF),
			# Filter - Prevent duplicate fiefs being offered.
			(assign, ":block", 0),
			(try_for_range, ":base_slot", kmt3_val_left_opt_1_type, kmt3_obj_right_opt_5+1),
				# Only check at certain slot values.
				(this_or_next|eq, ":base_slot", kmt3_val_left_opt_1_type),
				(this_or_next|eq, ":base_slot", kmt3_val_left_opt_2_type),
				(this_or_next|eq, ":base_slot", kmt3_val_left_opt_3_type),
				(this_or_next|eq, ":base_slot", kmt3_val_left_opt_4_type),
				(this_or_next|eq, ":base_slot", kmt3_val_left_opt_5_type),
				(this_or_next|eq, ":base_slot", kmt3_val_right_opt_1_type),
				(this_or_next|eq, ":base_slot", kmt3_val_right_opt_2_type),
				(this_or_next|eq, ":base_slot", kmt3_val_right_opt_3_type),
				(this_or_next|eq, ":base_slot", kmt3_val_right_opt_4_type),
				(             eq, ":base_slot", kmt3_val_right_opt_5_type),
				# Make sure this option is offering a fief.
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				# We don't care about the option we're currently altering.
				(neq, ":base_slot", ":slot_type"),
				# If the same fief is already being listed then block this update.
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_value", ":base_slot", ":offset"),
				(troop_slot_eq, KMT_OBJECTS, ":slot_value", ":value"),
				(assign, ":block", 1),
			(try_end),
			(eq, ":block", 0),
			# Update value slot.
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_obj_left_opt_1),
			(store_add, ":slot_value", ":slot_base", ":offset"),
			(troop_set_slot, KMT_OBJECTS, ":slot_value", ":value"),
			## Update center's name label.
			(store_sub, ":offset", kmt3_obj_left_opt_1_slider_label, kmt3_obj_left_opt_1),
			(store_add, ":slot_object", ":slot_base", ":offset"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, ":slot_object"),
			(troop_get_slot, ":center_no", KMT_OBJECTS, ":value"),
			(call_script, "script_kmt_store_center_long_name_to_s1", ":center_no"),
			(overlay_set_text, ":obj_no", s1),
			# Repeated for bold effect.
			(store_sub, ":offset", kmt3_obj_left_bold_effect, kmt3_obj_left_opt_1),
			(store_add, ":slot_object", ":slot_base", ":offset"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, ":slot_object"),
			(overlay_set_text, ":obj_no", s1),
			## Update center's prosperity value.
			(party_get_slot, reg21, ":center_no", slot_town_prosperity),
			(str_store_string, s21, "@Prosperity: {reg21} / 99"),
			(store_sub, ":offset", kmt3_obj_left_opt_1_info_1, kmt3_obj_left_opt_1),
			(store_add, ":slot_object", ":slot_base", ":offset"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, ":slot_object"),
			(overlay_set_text, ":obj_no", s21),
			## Update center's improvements value.
			(call_script, "script_improvement_assess_center_value", ":center_no"), # improvements_scripts.py (reg1 = built, reg2 = total value)
			(store_sub, reg22, reg2, 1),
			(str_store_string, s21, "@Improvements: {reg1} built, {reg2} denar{reg22?s:}"),
			(store_sub, ":offset", kmt3_obj_left_opt_1_info_2, kmt3_obj_left_opt_1),
			(store_add, ":slot_object", ":slot_base", ":offset"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, ":slot_object"),
			(overlay_set_text, ":obj_no", s21),
			## Update ratings.
			(call_script, "script_kmt_get_offer_ratings"),
			
		(else_try), ####### ROYAL COFFERS OPTION - SLIDER #######
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_1, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_2, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_3, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_4, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_left_opt_5, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_1, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_2, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_3, ":object"),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_4, ":object"),
			(             troop_slot_eq, KMT_OBJECTS, kmt3_obj_right_opt_5, ":object"),
			# Acquire correct slot number from object clicked.
			(assign, ":slot_base", 0),
			(try_for_range, ":slot_no", kmt3_obj_left_opt_1, kmt3_obj_right_opt_5+1),
				(eq, ":slot_base", 0),
				(troop_slot_eq, KMT_OBJECTS, ":slot_no", ":object"),
				(assign, ":slot_base", ":slot_no"),
			(try_end),
			# Filter - Correct slider type.
			(store_sub, ":offset", kmt3_val_left_opt_1_type, kmt3_obj_left_opt_1),
			(store_add, ":slot_type", ":slot_base", ":offset"),
			(troop_slot_eq, KMT_OBJECTS, ":slot_type", KMT_OPTION_KINGS_MONEY),
			# Store our new offered amount.
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_obj_left_opt_1),
			(store_add, ":slot_value", ":slot_base", ":offset"),
			(troop_set_slot, KMT_OBJECTS, ":slot_value", ":value"),
			# Update slider label.
			(store_sub, ":offset", kmt3_obj_left_opt_1_slider_label, kmt3_obj_left_opt_1),
			(store_add, ":slot_object", ":slot_base", ":offset"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, ":slot_object"),
			(store_sub, reg22, ":value", 1),
			(assign, reg21, ":value"),
			(str_store_string, s21, "@{reg21} denar{reg22?s:}"),
			(overlay_set_text, ":obj_no", s21),
			# Repeated for bold effect.
			(store_sub, ":offset", kmt3_obj_left_bold_effect, kmt3_obj_left_opt_1),
			(store_add, ":slot_object", ":slot_base", ":offset"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, ":slot_object"),
			(overlay_set_text, ":obj_no", s21),
			# Update ratings.
			(call_script, "script_kmt_get_offer_ratings"),
			
		(else_try), ####### BUTTON - MAKE OFFER #######
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_obj_button_make_offer, ":object"),
			(troop_slot_eq, KMT_OBJECTS, kmt3_obj_button_force_exchange, ":object"),
			## Update ratings.
			(call_script, "script_kmt_get_offer_ratings"),
			## Get our two sides and allow only qualified options to pass.
			(troop_get_slot, ":troop_left", KMT_OBJECTS, kmt3_val_lord_left),
			(troop_get_slot, ":troop_right", KMT_OBJECTS, kmt3_val_lord_right),
			(try_begin),
				## FILTER - Prevent the same person trading with themselves.
				(eq, ":troop_left", ":troop_right"),
				(display_message, "@Warning - As satisfying as it may be, you cannot trade with yourself.", gpu_red),
			(else_try),
				## FILTER - Left side is offering nothing.
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_1_type, KMT_OPTION_NONE),
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_2_type, KMT_OPTION_NONE),
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_3_type, KMT_OPTION_NONE),
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_4_type, KMT_OPTION_NONE),
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_5_type, KMT_OPTION_NONE),
				(str_store_troop_name, s21, ":troop_left"),
				(str_store_troop_name, s22, ":troop_right"),
				(display_message, "@{s22} says, '{s21} isn't offering anything.  I won't accept this trade.'", gpu_red),
			(else_try),
				## FILTER - Right side is offering nothing.
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_1_type, KMT_OPTION_NONE),
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_2_type, KMT_OPTION_NONE),
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_3_type, KMT_OPTION_NONE),
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_4_type, KMT_OPTION_NONE),
				(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_5_type, KMT_OPTION_NONE),
				(str_store_troop_name, s21, ":troop_left"),
				(str_store_troop_name, s22, ":troop_right"),
				(display_message, "@{s21} says, '{s22} isn't offering anything.  I won't accept this trade.'", gpu_red),
			(else_try),
				## FILTER - Left side would take a loss in title (AI) if trade went through.
				(neq, ":troop_left", "trp_player"), # Player can do whatever they want.
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_obj_button_force_exchange, ":object"), # Forced exchanges can go through.
				(call_script, "script_cf_kmt_vassal_will_lose_status_in_trade", ":troop_left"),
				(str_store_troop_name, s21, ":troop_left"),
				(display_message, "@{s21} says, 'I would lose status within the realm if I were to accept this trade.'", gpu_red),
			(else_try),
				## FILTER - Right side would take a loss in title (AI) if trade went through.
				(neq, ":troop_right", "trp_player"), # Player can do whatever they want.
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_obj_button_force_exchange, ":object"), # Forced exchanges can go through.
				(call_script, "script_cf_kmt_vassal_will_lose_status_in_trade", ":troop_right"),
				(str_store_troop_name, s21, ":troop_right"),
				(display_message, "@{s21} says, 'I would lose status within the realm if I were to accept this trade.'", gpu_red),
			(else_try),
				## FILTER - The AI (Left) feels it is getting the poorer end of this deal.
				(neq, ":troop_left", "trp_player"), # Player can do whatever they want.
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_obj_button_force_exchange, ":object"), # Forced exchanges can go through.
				(troop_get_slot, ":rating", KMT_OBJECTS, kmt3_val_left_rating),
				(troop_get_slot, ":rating_offer", KMT_OBJECTS, kmt3_val_right_rating),
				(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
				(val_mul, ":persuasion", 2),
				(val_add, ":persuasion", 10),
				(store_mul, ":persuasion_boost", ":rating", ":persuasion"),
				(val_div, ":persuasion_boost", 100),
				# (store_add, ":rating_maximum", ":rating", ":persuasion_boost"),
				(store_sub, ":rating_minimum", ":rating", ":persuasion_boost"),
				# (neg|is_between, ":rating_offer", ":rating_minimum", ":rating_maximum"),
				(lt, ":rating_offer", ":rating_minimum"),
				(str_store_troop_name, s21, ":troop_left"),
				(display_message, "@{s21} says, 'This deal is clearly not in my favor.  I must decline.'", gpu_red),
			(else_try),
				## FILTER - The AI (Right) feels it is getting the poorer end of this deal.
				(neq, ":troop_right", "trp_player"), # Player can do whatever they want.
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_obj_button_force_exchange, ":object"), # Forced exchanges can go through.
				(troop_get_slot, ":rating", KMT_OBJECTS, kmt3_val_right_rating),
				(troop_get_slot, ":rating_offer", KMT_OBJECTS, kmt3_val_left_rating),
				(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
				(val_mul, ":persuasion", 2),
				(val_add, ":persuasion", 10),
				(store_mul, ":persuasion_boost", ":rating", ":persuasion"),
				(val_div, ":persuasion_boost", 100),
				# (store_add, ":rating_maximum", ":rating", ":persuasion_boost"),
				(store_sub, ":rating_minimum", ":rating", ":persuasion_boost"),
				# (neg|is_between, ":rating_offer", ":rating_minimum", ":rating_maximum"),
				(lt, ":rating_offer", ":rating_minimum"),
				(str_store_troop_name, s21, ":troop_right"),
				(display_message, "@{s21} says, 'This deal is clearly not in my favor.  I must decline.'", gpu_red),
			(else_try),
				## FILTER - Every trade must include land on one side or the other.
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_1_type,  KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_2_type,  KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_3_type,  KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_4_type,  KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_5_type,  KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_1_type, KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_2_type, KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_3_type, KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_4_type, KMT_OPTION_FIEF),
				(neg|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_5_type, KMT_OPTION_FIEF),
				(display_message, "@Warning - A trade agreement must include land on at least one side.", gpu_red),
			(else_try),
				## FINAL - TRADE ACCEPTED
				(call_script, "script_kmt_process_all_trade_offers"),
				(try_begin), ## Forced trades always process a relation change.
					(troop_slot_eq, KMT_OBJECTS, kmt3_obj_button_force_exchange, ":object"),
					## Left Rating Penalty
					(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_left),
					(troop_get_slot, ":relation_change", KMT_OBJECTS, kmt3_val_left_label_forced_loss),
					(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change", 1),
					## Right Rating Penalty
					(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_right),
					(troop_get_slot, ":relation_change", KMT_OBJECTS, kmt3_val_right_label_forced_loss),
					(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change", 1),
				(else_try), ## Favourable trades should improve a lord's relation even if not forced.
					(troop_slot_eq, KMT_OBJECTS, kmt3_obj_button_make_offer, ":object"),
					(troop_slot_ge, KMT_OBJECTS, kmt3_val_right_label_forced_loss, 1),
					(troop_get_slot, ":troop_no", KMT_OBJECTS, kmt3_val_lord_right),
					(troop_get_slot, ":relation_change", KMT_OBJECTS, kmt3_val_right_label_forced_loss),
					(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation_change", 1),
				(try_end),
				# Reset offer ratings.
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_rating, 0),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_right_rating, 0),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_left_label_forced_loss, 0),
				(troop_set_slot, KMT_OBJECTS, kmt3_val_right_label_forced_loss, 0),
				
			(try_end),
			
		(try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                                VASSAL PRISONERS                                                 #####
###########################################################################################################################

("kmt_vassal_prisoners", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_kmt_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Prisoners of the Realm"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title2, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		
		## OBJ - TEXT - CONTAINER TITLE
		(str_store_string, s21, "@Enemy Nobles Held Captive:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 450, 580, 0, gpu_center),
		
		## OBJ - CONTAINER+ - CAPTIVE LIST (Section 1)
		(assign,  ":y_top",    570),
		(assign,  ":y_bottom", 330),
		(assign,  ":x_left",   250),
		(assign,  ":x_right",  645),
		(store_sub, ":x_width", ":x_right", ":x_left"),
		(store_sub, ":y_width", ":y_top", ":y_bottom"),
		(call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", kmt6_obj_container_captive_list),
			
		(set_container_overlay, -1), ## CONTAINER- - CAPTIVE LIST
		
		
		## OBJ - TEXT - CONTAINER TITLE
		(str_store_string, s21, "@Selected Captive:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 808, 580, 0, gpu_center),
		
		## OBJ - CONTAINER+ - SELECTED LORD (Section 2)
		(assign,  ":y_top",    570),
		(assign,  ":y_bottom", 430), # Above Section 3
		(assign,  ":x_left",   665), # Right of Section 1
		(assign,  ":x_right",  950),
		(store_sub, ":x_width", ":x_right", ":x_left"),
		(store_sub, ":y_width", ":y_top", ":y_bottom"),
		(call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", kmt6_obj_container_selected_lord),
			
		(set_container_overlay, -1), ## CONTAINER- - SELECTED LORD
		
		
		## OBJ - TEXT - CONTAINER TITLE
		(str_store_string, s21, "@Proposed Offer:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 808, 415, 0, gpu_center),
		
		## OBJ - CONTAINER+ - OFFERS (Section 3)
		(assign,  ":y_top",    405), # Below Section 2
		(assign,  ":y_bottom", 100),
		(assign,  ":x_left",   665), # Match Section 2 (left)
		(assign,  ":x_right",  950), # Match Section 2 (right)
		(store_sub, ":x_width", ":x_right", ":x_left"),
		(store_sub, ":y_width", ":y_top", ":y_bottom"),
		(call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", kmt6_obj_container_offered),
			
		(set_container_overlay, -1), ## CONTAINER- - OFFERS
		
		
		## OBJ - TEXT - CONTAINER TITLE
		(str_store_string, s21, "@Lord Grainwad's Message:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 450, 315, 0, gpu_center),
		
		## OBJ - CONTAINER+ - COUNTER OFFER (Section 4)
		(assign,  ":y_top",    305), # Below Section 1
		(assign,  ":y_bottom", 100),
		(assign,  ":x_left",   250), # Match Section 1 (left)
		(assign,  ":x_right",  645), # Match Section 1 (right)
		(store_sub, ":x_width", ":x_right", ":x_left"),
		(store_sub, ":y_width", ":y_top", ":y_bottom"),
		(call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", kmt6_obj_container_chat),
			
		(set_container_overlay, -1), ## CONTAINER- - COUNTER OFFER
		
		## OBJ - BUTTON - MAKE OFFER
        (str_store_string, s21, "@Make Offer"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 550, 35, kmt6_obj_button_confirm), # MAKE OFFER
		
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_kmt_handle_mode_switching_buttons", ":object", ":value"),
		
		# (try_begin), ####### COMBO BUTTON - ITEM TYPE SELECTOR #######
			# (eq, ":object", "$g_presentation_obj_1"),
			# (assign, "$temp", ":value"),
			# (start_presentation, "prsnt_commission_requests"),
			
		# (try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                                 VASSAL TITLES                                                   #####
###########################################################################################################################

("kmt_vassal_titles", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_kmt_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Custom Vassal Titles"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title2, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		## OBJ - TEXT - SELECTED FACTION
		(str_store_string, s21, "@Selected Faction:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 250, 580, 0, gpu_left),
		
		## OBJ - DROP-DOWN MENU - FACTION SELECTOR
        (create_combo_button_overlay, reg1),
		(troop_set_slot, KMT_OBJECTS, kmt5_obj_faction_selector, reg1),
        (position_set_x, pos1, 600),
        (position_set_y, pos1, 563),
        (overlay_set_position, reg1, pos1),
        (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
			(str_store_faction_name, s21, ":kingdom_no"),
			(overlay_add_item, reg1, "@{s21}"),
		(try_end),
		(troop_get_slot, ":value", KMT_OBJECTS, kmt5_val_faction_selector),
		(overlay_set_val, reg1, ":value"),
		
		## OBJ - TEXT - SELECTED FACTION
		(str_store_string, s21, "@Display Style:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 250, 535, 0, gpu_left),
		
		## OBJ - DROP-DOWN MENU - TITLE STYLE
		(create_combo_button_overlay, reg1),
		(troop_set_slot, KMT_OBJECTS, kmt5_obj_menu_title_style, reg1),
        (position_set_x, pos1, 600),
        (position_set_y, pos1, 518),
        (overlay_set_position, reg1, pos1),
		(overlay_add_item, reg1, "@Title Before Name"),
        (overlay_add_item, reg1, "@Title After Name"),
        (troop_get_slot, ":value", KMT_OBJECTS, kmt5_val_menu_title_style),
		(overlay_set_val, reg1, ":value"),
		
		# script_gpu_create_text_box     - pos_x, pos_y, storage_id
		(assign, ":x_labels", 250),
		(assign, ":x_lord", 570),
		(assign, ":x_lady", 830),
		(assign, ":pos_y", 480),
		(assign, ":pos_y_step", 45),
		(assign, ":y_input_adjust", 10),
		(assign, ":size_textbox", 75),
		
		## OBJ - TEXT - OWNERSHIP LEVEL
		# (str_store_string, s21, "@Ownership:"),
		# (call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		# (call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		
		## OBJ - TEXT - LORDS
		(str_store_string, s21, "@Lords"),
		(store_sub, ":x_lord_title", ":x_lord", 40),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_lord_title", ":pos_y", 0, gpu_center),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_lord_title", ":pos_y", 0, gpu_center),
		
		## OBJ - TEXT - LADIES
		(str_store_string, s21, "@Ladies"),
		(store_sub, ":x_lady_title", ":x_lady", 40),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_lady_title", ":pos_y", 0, gpu_center),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_lady_title", ":pos_y", 0, gpu_center),
		
		## OBJ - TEXT - TITLE FOR LANDLESS LORDS
		(str_store_string, s21, "@Landless:"),
		(val_sub, ":pos_y", ":pos_y_step"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		(store_sub, ":pos_y_temp", ":pos_y", ":y_input_adjust"),
		(call_script, "script_gpu_create_text_box", ":x_lord", ":pos_y_temp", kmt5_obj_textbox_landless_lords, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_landless_lords, ":size_textbox"),
		(call_script, "script_gpu_create_text_box", ":x_lady", ":pos_y_temp", kmt5_obj_textbox_landless_ladies, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_landless_ladies, ":size_textbox"),
		
		## OBJ - TEXT - TITLE FOR VILLAGE LORDS
		(str_store_string, s21, "@Villages:"),
		(val_sub, ":pos_y", ":pos_y_step"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		(store_sub, ":pos_y_temp", ":pos_y", ":y_input_adjust"),
		(call_script, "script_gpu_create_text_box", ":x_lord", ":pos_y_temp", kmt5_obj_textbox_village_lords, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_village_lords, ":size_textbox"),
		(call_script, "script_gpu_create_text_box", ":x_lady", ":pos_y_temp", kmt5_obj_textbox_village_ladies, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_village_ladies, ":size_textbox"),
		
		## OBJ - TEXT - TITLE FOR CASTLE LORDS
		(str_store_string, s21, "@Castles:"),
		(val_sub, ":pos_y", ":pos_y_step"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		(store_sub, ":pos_y_temp", ":pos_y", ":y_input_adjust"),
		(call_script, "script_gpu_create_text_box", ":x_lord", ":pos_y_temp", kmt5_obj_textbox_castle_lords, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_castle_lords, ":size_textbox"),
		(call_script, "script_gpu_create_text_box", ":x_lady", ":pos_y_temp", kmt5_obj_textbox_castle_ladies, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_castle_ladies, ":size_textbox"),
		
		## OBJ - TEXT - TITLE FOR TOWN LORDS
		(str_store_string, s21, "@Towns:"),
		(val_sub, ":pos_y", ":pos_y_step"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		(store_sub, ":pos_y_temp", ":pos_y", ":y_input_adjust"),
		(call_script, "script_gpu_create_text_box", ":x_lord", ":pos_y_temp", kmt5_obj_textbox_town_lords, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_town_lords, ":size_textbox"),
		(call_script, "script_gpu_create_text_box", ":x_lady", ":pos_y_temp", kmt5_obj_textbox_town_ladies, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_town_ladies, ":size_textbox"),
		
		## OBJ - TEXT - TITLE FOR MARSHALS
		(str_store_string, s21, "@Marshal:"),
		(val_sub, ":pos_y", ":pos_y_step"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		(store_sub, ":pos_y_temp", ":pos_y", ":y_input_adjust"),
		(call_script, "script_gpu_create_text_box", ":x_lord", ":pos_y_temp", kmt5_obj_textbox_marshal, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_marshal, ":size_textbox"),
		(call_script, "script_gpu_create_text_box", ":x_lady", ":pos_y_temp", kmt5_obj_textbox_marshal_lady, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_marshal_lady, ":size_textbox"),
		
		## OBJ - TEXT - TITLE FOR KINGS / QUEENS
		(str_store_string, s21, "@Rulers:"),
		(val_sub, ":pos_y", ":pos_y_step"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		(store_sub, ":pos_y_temp", ":pos_y", ":y_input_adjust"),
		(call_script, "script_gpu_create_text_box", ":x_lord", ":pos_y_temp", kmt5_obj_textbox_king, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_king, ":size_textbox"),
		(call_script, "script_gpu_create_text_box", ":x_lady", ":pos_y_temp", kmt5_obj_textbox_queen, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_queen, ":size_textbox"),
		
		## OBJ - TEXT - TITLE FOR ROYAL CHILDREN
		(str_store_string, s21, "@Royal Children:"),
		(val_sub, ":pos_y", ":pos_y_step"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_labels", ":pos_y", 0, gpu_left),
		(store_sub, ":pos_y_temp", ":pos_y", ":y_input_adjust"),
		(call_script, "script_gpu_create_text_box", ":x_lord", ":pos_y_temp", kmt5_obj_textbox_prince, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_prince, ":size_textbox"),
		(call_script, "script_gpu_create_text_box", ":x_lady", ":pos_y_temp", kmt5_obj_textbox_princess, gpu_left),
		(call_script, "script_gpu_resize_object", kmt5_obj_textbox_princess, ":size_textbox"),
		
		## OBJ - BUTTON - DELETE TITLES
        (str_store_string, s21, "@Delete Saved Titles"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 350, 35, kmt5_obj_button_delete_titles), # DELETE
		
		## OBJ - BUTTON - DEFAULT TITLES
        (str_store_string, s21, "@Load Defaults"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 550, 35, kmt5_obj_button_default_titles), # DEFAULTS
		
		## OBJ - BUTTON - LOAD TITLES
        # (str_store_string, s21, "@Load Titles"),
		# (call_script, "script_gpu_create_game_button", "str_hub_s21", 675, 35, kmt5_obj_button_load_titles), # LOAD
		
		## OBJ - BUTTON - SAVE TITLES
        (str_store_string, s21, "@Save Titles"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 750, 35, kmt5_obj_button_save_titles), # SAVE
		
		## FUNCTION - LOAD SELECTED FACTION
		(troop_get_slot, ":faction_no", KMT_OBJECTS, kmt5_val_selected_faction),
		(try_begin),
			(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(call_script, "script_kmt_load_titles_for_faction", ":faction_no"),
			(str_store_faction_name, s21, ":faction_no"),
			(display_message, "@Custom titles for lords and ladies in the {s21} have been loaded.", gpu_green),
		(try_end),
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_kmt_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin), ####### BUTTON - DEFAULT TITLES #######
			(troop_slot_eq, KMT_OBJECTS, kmt5_obj_button_default_titles, ":object"),
			(troop_get_slot, ":faction_no", KMT_OBJECTS, kmt5_val_selected_faction),
			(call_script, "script_kmt_load_default_titles_for_faction", ":faction_no"),
			(str_store_faction_name, s21, ":faction_no"),
			(display_message, "@The default titles for lords and ladies in the {s21} have been loaded.", gpu_green),
			
		(else_try), ####### BUTTON - SAVE TITLES #######
			(troop_slot_eq, KMT_OBJECTS, kmt5_obj_button_save_titles, ":object"),
			(troop_get_slot, ":faction_no", KMT_OBJECTS, kmt5_val_selected_faction),
			(call_script, "script_kmt_save_titles_for_faction", ":faction_no"),
			(str_store_faction_name, s21, ":faction_no"),
			(display_message, "@Custom titles for lords and ladies in the {s21} have been saved.", gpu_green),
			
		(else_try), ####### BUTTON - DELETE TITLES #######
			(troop_slot_eq, KMT_OBJECTS, kmt5_obj_button_delete_titles, ":object"),
			(dict_delete_file, "@Silverstag Vassal Titles"),
			## Set title styles to default values.
			(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
				(faction_get_slot, ":setting", ":kingdom_no", slot_faction_title_style_default),
				(faction_set_slot, ":kingdom_no", slot_faction_title_style, ":setting"),
			(try_end),
			(display_message, "@The custom title file has been removed.", gpu_green),
			
		(else_try), ####### MENU - FACTION SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt5_obj_faction_selector, ":object"),
			(troop_set_slot, KMT_OBJECTS, kmt5_val_faction_selector, ":value"),
			(store_add, ":faction_no", kingdoms_begin, ":value"),
			(troop_set_slot, KMT_OBJECTS, kmt5_val_selected_faction, ":faction_no"),
			(call_script, "script_kmt_load_titles_for_faction", ":faction_no"),
			(str_store_faction_name, s21, ":faction_no"),
			(display_message, "@Custom titles for lords and ladies in the {s21} have been loaded.", gpu_green),
			
		(else_try), ####### MENU - STYLE SELECTOR #######
			(troop_slot_eq, KMT_OBJECTS, kmt5_obj_menu_title_style, ":object"),
			(troop_set_slot, KMT_OBJECTS, kmt5_val_menu_title_style, ":value"),
			
		(try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                                  GENERAL INFO                                                   #####
###########################################################################################################################

("kmt_general_info", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_kmt_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Affairs of the Realm"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title2, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		## OBJ - TEXT - COMMISSION REQUESTS TITLE
		# (str_store_string, s21, "@Current Commission Requests:"),
		# (call_script, "script_gpu_create_text_label", "str_hub_s21", 250, 295, cci_obj_title_commissions, gpu_left),
		
		
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_kmt_handle_mode_switching_buttons", ":object", ":value"),
		
		# (try_begin), ####### COMBO BUTTON - ITEM TYPE SELECTOR #######
			# (eq, ":object", "$g_presentation_obj_1"),
			# (assign, "$temp", ":value"),
			# (start_presentation, "prsnt_commission_requests"),
			
		# (try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                                FIEF ELECTIONS                                                   #####
###########################################################################################################################

("kmt_fief_elections", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_kmt_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Fief Elections"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title2, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		## OBJ - TEXT - COMMISSION REQUESTS TITLE
		# (str_store_string, s21, "@Current Commission Requests:"),
		# (call_script, "script_gpu_create_text_label", "str_hub_s21", 250, 295, cci_obj_title_commissions, gpu_left),
		
		
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_kmt_handle_mode_switching_buttons", ":object", ":value"),
		
		# (try_begin), ####### COMBO BUTTON - ITEM TYPE SELECTOR #######
			# (eq, ":object", "$g_presentation_obj_1"),
			# (assign, "$temp", ":value"),
			# (start_presentation, "prsnt_commission_requests"),
			
		# (try_end),
    ]),
  ]),
  

###########################################################################################################################
#####                                                 VASSAL GIFTS                                                   #####
###########################################################################################################################

("kmt_vassal_gifts", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_kmt_create_mode_switching_buttons"),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Vassal Gifts"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, kmt1_obj_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kmt1_obj_main_title2, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		## OBJ - TEXT - COMMISSION REQUESTS TITLE
		# (str_store_string, s21, "@Current Commission Requests:"),
		# (call_script, "script_gpu_create_text_label", "str_hub_s21", 250, 295, cci_obj_title_commissions, gpu_left),
		
		
      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_kmt_handle_mode_switching_buttons", ":object", ":value"),
		
		# (try_begin), ####### COMBO BUTTON - ITEM TYPE SELECTOR #######
			# (eq, ":object", "$g_presentation_obj_1"),
			# (assign, "$temp", ":value"),
			# (start_presentation, "prsnt_commission_requests"),
			
		# (try_end),
    ]),
  ]),
  

###########################################################################################################################
#####                                                KMT Lord Holdings                                                #####
###########################################################################################################################
("kmt_lord_holdings", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(assign, ":x_names", 25),
		(store_add, ":x_relations", ":x_names",  190),
		(store_add, ":x_towns", ":x_relations",   55),
		(store_add, ":x_castles", ":x_towns",    105),
		(store_add, ":x_villages", ":x_castles", 150),
		(store_add, ":x_friends", ":x_villages", 110),
		(store_add, ":x_enemies", ":x_friends",  165),
		
		(assign, "$gpu_storage", kmt_objects),
		
		# (try_begin),
			# (troop_slot_eq, kmt_objects, kmt_val_remove_backgrounds, 0),
			# (call_script, "script_gpu_create_mesh", "mesh_pic_map_calradia_half", 0, 0, 1000, 1300),
			# (overlay_set_alpha, reg1, 0x00),
		# (try_end),
		# (call_script, "script_gpu_draw_line", 950, 510, 25, 115, 10526880), # White background above the map.
		# (overlay_set_alpha, reg1, 0x77),
		# (call_script, "script_gpu_draw_line", 950, 30, 25, 625, gpu_brown), # Brown header background above the map.
		# (overlay_set_alpha, reg1, 0xCC),
		# (call_script, "script_gpu_draw_line", 950, 30, 25, 85, gpu_brown), # Brown footer background above the map.
		# (overlay_set_alpha, reg1, 0xCC),
		
		
		
		(call_script, "script_gpu_create_game_button", "str_kmt_done_button", 500, 25, kmt_obj_button_done), # DONE Button @ 895, 35
		
		(call_script, "script_gpu_create_text_label", "str_kmt_title_holdings", 847, 688, kmt_obj_main_title, gpu_center), # Estates of the Realm
		(call_script, "script_gpu_resize_object", kmt_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_title_holdings", 847, 688, kmt_obj_main_title, gpu_center), # Estates of the Realm
		(call_script, "script_gpu_resize_object", kmt_obj_main_title, 150),
		
		# script_gpu_create_checkbox     - pos_x, pos_y, label, storage_slot, value_slot
		#(call_script, "script_gpu_create_checkbox", 30, 56, "str_kmt_opt_remove_background", kmt_obj_remove_backgrounds, kmt_val_remove_backgrounds),
		
		# Header
		(assign, ":pos_y", 655),
		#(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_black),
		(store_sub, ":pos_y_titles", ":pos_y", 13),
		(call_script, "script_gpu_create_text_label", "str_kmt_title_names", ":x_names", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_title_names", ":x_names", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(call_script, "script_gpu_create_text_label", "str_kmt_title_relations", ":x_relations", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_title_relations", ":x_relations", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(call_script, "script_gpu_create_text_label", "str_kmt_title_towns", ":x_towns", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_title_towns", ":x_towns", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(call_script, "script_gpu_create_text_label", "str_kmt_title_castles", ":x_castles", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_title_castles", ":x_castles", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(call_script, "script_gpu_create_text_label", "str_kmt_title_villages", ":x_villages", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_title_villages", ":x_villages", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(call_script, "script_gpu_create_text_label", "str_kmt_title_friends", ":x_friends", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_title_friends", ":x_friends", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(call_script, "script_gpu_create_text_label", "str_kmt_title_enemies", ":x_enemies", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_title_enemies", ":x_enemies", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(val_sub, ":pos_y", 30),
		(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_gray),
		
		# OBJ - Faction Menu
		(position_set_x, pos1, 190),
        (position_set_y, pos1, 675),
		(create_combo_label_overlay, reg1),
        (overlay_set_position, reg1, pos1),
		(assign, ":valid_kingdoms", 0),
		(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
			(faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
			(str_store_faction_name, s21, ":kingdom_no"),
			(overlay_add_item, reg1, "@{s21}"),
			#(store_sub, ":storage_slot", ":kingdom_no", kingdoms_begin),
			(store_add, ":storage_slot", ":valid_kingdoms", kmt_val_kingdoms_begin),
			(troop_set_slot, kmt_objects, ":storage_slot", ":kingdom_no"),
			(val_add, ":valid_kingdoms", 1),
		(try_end),
		(troop_set_slot, kmt_objects, kmt_obj_faction_menu, reg1),
		(troop_get_slot, ":value", kmt_objects, kmt_val_faction_menu),
		(overlay_set_val, reg1, ":value"),
		# Determine which faction we're looking at
		(store_add, ":faction_slot", ":value", kmt_val_kingdoms_begin),
		(troop_get_slot, ":faction_id", kmt_objects, ":faction_slot"),
		
		(call_script, "script_gpu_container_heading", 0, 115, 1000, 485, kmt_obj_main_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			
			# Determine how many lords there are for spacing consideration.
			(assign, ":lord_count", 0),
			(try_for_range, ":troop_no", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
				(try_begin),
					(eq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
					(assign, ":troop_check", "trp_player"),
					(assign, ":faction_no", "$players_kingdom"),
				(else_try),
					(assign, ":troop_check", ":troop_no"),
					(store_troop_faction, ":faction_no", ":troop_check"),
				(try_end),
				(eq, ":faction_no", ":faction_id"),
				(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
				(val_add, ":lord_count", 1),
			(try_end),
			(store_mul, ":container_length", ":lord_count", 265),
			
			(assign, ":pos_y", ":container_length"),
			(assign, ":city_count", 0),
			(assign, ":castle_count", 0),
			(assign, ":village_count", 0),
			(try_for_range, ":troop_check", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
				(assign, ":total_lines", 2),
				(try_begin),
					(eq, ":troop_check", "trp_kingdom_heroes_including_player_begin"),
					(assign, ":troop_no", "trp_player"),
					(assign, ":faction_no", "$players_kingdom"),
				(else_try),
					(assign, ":troop_no", ":troop_check"),
					(store_troop_faction, ":faction_no", ":troop_no"),
				(try_end),
				
				(eq, ":faction_no", ":faction_id"),
				(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
				
				### COLUMN 1 ###
				# Add Lord Name
				(assign, ":line_count", 0),
				(str_store_troop_name, s25, ":troop_no"),
				(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_names", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, kmt_text_size),
				(overlay_set_color, reg1, gpu_dark_blue), # 65547), # dark blue
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_names", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, kmt_text_size),
				(overlay_set_color, reg1, gpu_dark_blue), # 65547), # dark blue
				# Display reputation if previously met
				(try_begin),
					# Conditions
					(this_or_next|troop_slot_eq, ":troop_no", slot_troop_met, 1),           # Player has met this lord before...
					(eq, ":faction_no", "fac_player_supporters_faction"),                  # ...or they are a vassal of the player's.
					(neg|is_between, ":troop_no", kings_begin, kings_end),                  # No need to display king reputations.
					(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),        # No need to display pretender reputations.
					(neq, ":troop_no", "trp_player"),                                       # We don't want to view the reputation type for the player.
					# Data
					(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
					(store_add, ":reputation_string", ":reputation", "str_personality_archetypes"),
					(str_store_string, s25, ":reputation_string"),
					(str_store_string, s25, "@Reputation: {s25}"),
					# Display creation
					(val_add, ":line_count", 1),
					(store_mul, ":y_adj", ":line_count", kmt_line_step),
					(store_sub, ":y_line", ":pos_y", ":y_adj"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_names", ":y_line", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					#(overlay_set_color, reg1, 0x222222), # dark grey
					(val_add, ":total_lines", 1),
				(try_end),
				#show renown
				(troop_get_slot, reg0, ":troop_no", slot_troop_renown),
				(str_store_string, s25, "@Renown: {reg0}"),
				(val_add, ":line_count", 1),
				(store_mul, ":y_adj", ":line_count", kmt_line_step),
				(store_sub, ":y_line", ":pos_y", ":y_adj"),
				(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_names", ":y_line", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, kmt_text_size),
				#(overlay_set_color, reg1, 0x222222), # dark grey
				
				### COLUMN 2 ###
				# Add Relation Information
				(call_script, "script_troop_get_player_relation", ":troop_no"),
				(call_script, "script_gpu_create_text_label", "str_kmt_relation_to_you_reg0", ":x_relations", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, kmt_text_size),
				(assign, ":line_count", 0),
				# Add relation based changes due to Enhanced Diplomacy.
				(try_begin),
					(eq, ":faction_no", "$players_kingdom"),
					(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
					(neq, ":troop_no", "trp_player"),
					(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
					(neg|is_between, ":troop_no", kings_begin, kings_end),
					(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
					(assign, ":continue", 1),
					(try_begin),
						(eq, ":reputation", lrep_martial),
						(assign, ":data_slot", slot_faction_lrep_martial_relation),
					(else_try),
						(eq, ":reputation", lrep_quarrelsome),
						(assign, ":data_slot", slot_faction_lrep_quarrelsome_relation),
					(else_try),
						(eq, ":reputation", lrep_selfrighteous),
						(assign, ":data_slot", slot_faction_lrep_selfrighteous_relation),
					(else_try),
						(eq, ":reputation", lrep_cunning),
						(assign, ":data_slot", slot_faction_lrep_cunning_relation),
					(else_try),
						(eq, ":reputation", lrep_debauched),
						(assign, ":data_slot", slot_faction_lrep_debauched_relation),
					(else_try),
						(eq, ":reputation", lrep_goodnatured),
						(assign, ":data_slot", slot_faction_lrep_goodnatured_relation),
					(else_try),
						(eq, ":reputation", lrep_upstanding),
						(assign, ":data_slot", slot_faction_lrep_upstanding_relation),
					(else_try),
						(eq, ":reputation", lrep_roguish),
						(assign, ":data_slot", slot_faction_lrep_roguish_relation),
					(else_try),
						(eq, ":reputation", lrep_benefactor),
						(assign, ":data_slot", slot_faction_lrep_benefactor_relation),
					(else_try),
						(eq, ":reputation", lrep_custodian),
						(assign, ":data_slot", slot_faction_lrep_custodian_relation),
					(else_try),
						### ERROR - No valid reputation type. ###
						(assign, reg31, ":reputation"),
						(str_store_troop_name, s31, ":troop_no"),
						(display_message, "@ERROR (KMT): Invalid reputation type {reg31} on {s31}.", gpu_red),
						(assign, ":continue", 0),
					(try_end),
					(eq, ":continue", 1),
					(faction_get_slot, ":chance", ":faction_no", ":data_slot"),
					(troop_get_slot, ":fief_bonus", ":troop_no", slot_troop_relation_from_fief),
					(try_begin),
						(ge, ":fief_bonus", 1),
						(val_add, ":chance", ":fief_bonus"),
					(else_try),
						(val_add, ":chance", -50),
					(try_end),
					
					# Create the data line.
					
					(assign, reg21, ":chance"),
					(str_store_string, s25, "@{reg21}%"),
					(val_add, ":line_count", 1),
					(store_mul, ":y_adj", ":line_count", kmt_line_step),
					(store_sub, ":y_line", ":pos_y", ":y_adj"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_relations", ":y_line", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
				(try_end),
				# (try_begin),
					# (ge, reg0, 11),
					# (overlay_set_color, reg1, gpu_green),
				# (else_try),
					# (lt, reg0, -5),
					# (overlay_set_color, reg1, gpu_red),
				# (try_end),
				# (try_begin),
					# (faction_get_slot, ":troop_king", ":faction_no", slot_faction_leader),
					# (neq, ":troop_king", "trp_player"),
					# (assign, ":total_lines", 2),
					# (store_sub, ":pos_y_line_2", ":pos_y", kmt_line_step),
					# (call_script, "script_gpu_create_text_label", "str_kmt_relation_with_king_reg1", ":x_relations", ":pos_y_line_2", 0, gpu_left),
					# (call_script, "script_gpu_resize_object", 0, kmt_text_size),
				# (try_end),
				
				### COLUMN 3 ###
				# Determine which cities are owned by troop_no
				(assign, ":line_count", 0),
				(try_for_range, ":center_no", towns_begin, towns_end),
					(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
					(str_store_party_name, s25, ":center_no"),
					(store_mul, ":y_adj", ":line_count", kmt_line_step),
					(store_sub, ":y_line", ":pos_y", ":y_adj"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_towns", ":y_line", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					(val_add, ":line_count", 1),
					(val_add, ":city_count", 1),
					(lt, ":total_lines", ":line_count"),
					(assign, ":total_lines", ":line_count"),
				(try_end),
				
				### COLUMN 4 ###
				# Determine which castles are owned by troop_no
				(assign, ":line_count", 0),
				(try_for_range, ":center_no", castles_begin, castles_end),
					(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
					(str_store_party_name, s25, ":center_no"),
					(store_mul, ":y_adj", ":line_count", kmt_line_step),
					(store_sub, ":y_line", ":pos_y", ":y_adj"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_castles", ":y_line", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					(val_add, ":line_count", 1),
					(val_add, ":castle_count", 1),
					(lt, ":total_lines", ":line_count"),
					(assign, ":total_lines", ":line_count"),
				(try_end),
				
				### COLUMN 5 ###
				# Determine which villages are owned by troop_no
				(assign, ":line_count", 0),
				(try_for_range, ":center_no", villages_begin, villages_end),
					(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
					(str_store_party_name, s25, ":center_no"),
					(store_mul, ":y_adj", ":line_count", kmt_line_step),
					(store_sub, ":y_line", ":pos_y", ":y_adj"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_villages", ":y_line", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					(val_add, ":line_count", 1),
					(val_add, ":village_count", 1),
					(lt, ":total_lines", ":line_count"),
					(assign, ":total_lines", ":line_count"),
				(try_end),
				
				### COLUMN 6 ###
				# Determine which allies the lord has.
				(assign, ":line_count", 0),
				(try_for_range, ":lord_no", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
					(neq, ":lord_no", ":troop_no"),
					## Ensure lord is of the same faction or we simply don't care.
					(store_troop_faction, ":faction_no", ":lord_no"),
					(eq, ":faction_no", ":faction_id"), # Faction_ID is the faction being displayed.
					## Check on the lord's relation and how that affects us.
					(call_script, "script_troop_get_relation_with_troop", ":lord_no", ":troop_no"),
					(assign, ":relation_with_troop", reg0),
					(ge, ":relation_with_troop", kmt_ai_friend_threshold),
					(try_begin),
						(str_clear, s22),
						(eq, ":faction_no", "$players_kingdom"),
						(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
						(neq, ":troop_no", "trp_player"),
						## Determine how much the friend would like to see this lord receive a fief. (Defined in module_scripts @ script "give_center_to_lord"
						(store_div, ":relation_change", reg0, 8),
						(val_sub, ":relation_change", 2),
						(val_clamp, ":relation_change", -5, 3),
						(assign, reg0, ":relation_change"),
						(str_clear, s21),
						(try_begin),
							(ge, ":relation_change", 0),
							(str_store_string, s21, "@+"),
						(try_end),
						(str_store_string, s22, "@ ({s21}{reg0})"),
					(try_end),
					
					(str_store_troop_name, s25, ":lord_no"),
					(str_store_string, s25, "@{s25}{s22}"),
					(store_mul, ":y_adj", ":line_count", kmt_line_step),
					(store_sub, ":y_line", ":pos_y", ":y_adj"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_friends", ":y_line", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					(val_add, ":line_count", 1),
					(lt, ":total_lines", ":line_count"),
					(assign, ":total_lines", ":line_count"),
				(try_end),
				
				### COLUMN 7 ###
				# Determine which enemies the lord has.
				(assign, ":line_count", 0),
				(try_for_range, ":lord_no", active_npcs_begin, active_npcs_end),
					(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
					(neq, ":lord_no", ":troop_no"),
					## Ensure lord is of the same faction or we simply don't care.
					(store_troop_faction, ":faction_no", ":lord_no"),
					(eq, ":faction_no", ":faction_id"), # Faction_ID is the faction being displayed.
					## Check on the lord's relation and how that affects us.
					(call_script, "script_troop_get_relation_with_troop", ":lord_no", ":troop_no"),
					(assign, ":relation_with_troop", reg0),
					(lt, ":relation_with_troop", kmt_ai_enemy_threshold),
					(try_begin),
						(str_clear, s22),
						(eq, ":faction_no", "$players_kingdom"),
						(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
						(neq, ":troop_no", "trp_player"),
						## Determine how much the enemy would hate to see this lord receive a fief. (Defined in module_scripts @ script "give_center_to_lord"
						(store_div, ":relation_change", reg0, 8),
						(val_sub, ":relation_change", 2),
						(val_clamp, ":relation_change", -5, 3),
						(assign, reg0, ":relation_change"),
						(str_clear, s21),
						(try_begin),
							(ge, ":relation_change", 0),
							(str_store_string, s21, "@+"),
						(try_end),
						(str_store_string, s22, "@ ({s21}{reg0})"),
					(try_end),
					
					(str_store_troop_name, s25, ":lord_no"),
					(str_store_string, s25, "@{s25}{s22}"),
					(store_mul, ":y_adj", ":line_count", kmt_line_step),
					(store_sub, ":y_line", ":pos_y", ":y_adj"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_enemies", ":y_line", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					(val_add, ":line_count", 1),
					(lt, ":total_lines", ":line_count"),
					(assign, ":total_lines", ":line_count"),
				(try_end),
				
				
				
				(store_mul, ":pos_y_adjust", ":total_lines", kmt_line_step),
				(val_sub, ":pos_y", ":pos_y_adjust"),
				(call_script, "script_gpu_draw_line", 946, 2, 27, ":pos_y", gpu_gray), # 1315860),
				(val_sub, ":pos_y", kmt_line_step),
			(try_end), # End of troop_no cycle
		############### CONTAINER END ###############	
		(set_container_overlay, -1),
		
		# Footer
		(assign, ":pos_y", 115),
		(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_gray),
		(store_sub, ":pos_y_titles", ":pos_y", 13),
		(assign, reg0, ":lord_count"),
		(call_script, "script_gpu_create_text_label", "str_kmt_footer_lords", ":x_names", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_footer_lords", ":x_names", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(assign, reg0, ":city_count"),
		(call_script, "script_gpu_create_text_label", "str_kmt_footer_towns", ":x_towns", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_footer_towns", ":x_towns", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(assign, reg0, ":castle_count"),
		(call_script, "script_gpu_create_text_label", "str_kmt_footer_castles", ":x_castles", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_footer_castles", ":x_castles", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		(assign, reg0, ":village_count"),
		(call_script, "script_gpu_create_text_label", "str_kmt_footer_villages", ":x_villages", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_footer_villages", ":x_villages", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		#(overlay_set_color, reg1, gpu_white),
		
		# (val_sub, ":pos_y", 30),
		# (call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_black),
		
		# (call_script, "script_gpu_draw_line", 2, 570, 25, 85, gpu_black), # left border
		# (call_script, "script_gpu_draw_line", 2, 570, 973, 85, gpu_black), # right border
		
		#(call_script, "script_gpu_prsnt_panel_color_chooser", 250, 475),
      ]),
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		# (try_begin),
			# (ge, kmt_debug, 2),
			# (assign, reg1, ":object"),
			# (assign, reg2, ":value"),
			# (display_message, "@DEBUG (KMT): Object clicked is {reg1}.  Value is {reg2}."),
		# (try_end),
		
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, kmt_objects, kmt_obj_button_done, ":object"),
			(presentation_set_duration, 0),
			
		(else_try), ####### REMOVE BACKGROUNDS CHECKBOX #######
			(troop_slot_eq, kmt_objects, kmt_obj_remove_backgrounds, ":object"),
			(troop_set_slot, kmt_objects, kmt_val_remove_backgrounds, ":value"),
			# (troop_get_slot, reg1, kmt_objects, kmt_val_remove_backgrounds),
			# (display_message, "@Background should be {reg1?hidden:displayed}."),
			(start_presentation, "prsnt_kmt_lord_holdings"),
			
		(else_try), ####### FACTION MENU #######
			(troop_slot_eq, kmt_objects, kmt_obj_faction_menu, ":object"),
			(troop_set_slot, kmt_objects, kmt_val_faction_menu, ":value"),
			(start_presentation, "prsnt_kmt_lord_holdings"),
			
		(try_end),

		# (call_script, "script_gpu_events_panel_color_chooser", ":object", ":value"),
		# (try_begin),
			# (eq, reg0, 1),
			# (start_presentation, "prsnt_kmt_lord_holdings"),
		# (try_end),
      ]),
	  
	# (ti_on_presentation_mouse_press,
      # [
        # (store_trigger_param_1, ":object"),
        # (store_trigger_param_2, ":value"),
		
		# (call_script, "script_gpu_mouseclick_panel_color_chooser", ":object", ":value"),

      # ]),
    ]),

("verify_troop_equipment", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(assign,    ":x_col_1",              35), # Troop #
		(store_add, ":x_col_2", ":x_col_1",  40), # Troop Name
		(store_add, ":x_col_3", ":x_col_2", 225), # Required Stat
		(store_add, ":x_col_4", ":x_col_3", 175), # Required Stat value
		(store_add, ":x_col_5", ":x_col_4", 100), # Item #
		(store_add, ":x_col_6", ":x_col_5",  50), # Item Name  
		(store_add, ":x_col_7", ":x_col_6", 250), # Difficulty Value
		
		
		(assign, "$gpu_storage", kmt_objects),
		
		(call_script, "script_gpu_create_game_button", "str_kmt_done_button", 500, 25, kmt_obj_button_done), # DONE Button @ 895, 35
		
		(str_store_string, s25, "@Troop Equipment Checker"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", 500, 688, kmt_obj_main_title, gpu_center), # Estates of the Realm
		(call_script, "script_gpu_resize_object", kmt_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", 500, 688, kmt_obj_main_title, gpu_center), # Estates of the Realm
		(call_script, "script_gpu_resize_object", kmt_obj_main_title, 150),
		
		# Header
		(assign, ":pos_y", 655),
		#(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_black),
		(store_sub, ":pos_y_titles", ":pos_y", 13),
		(str_store_string, s25, "@ # "),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_1", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_1", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@TROOP NAME"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_2", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_2", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@REQUIRED STAT"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_3", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_3", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@VALUE"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_4", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_4", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@ # "),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_5", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_5", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@ITEM NAME"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_6", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_6", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@DIFFICULTY"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_7", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_7", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(val_sub, ":pos_y", 30),
		(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_gray),
		
		(call_script, "script_gpu_container_heading", 0, 115, 1000, 485, kmt_obj_main_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			(assign, ":records", 0),
			(assign, ":start_troop", "trp_tutorial_maceman"),
			(assign, ":stop_troop", "trp_end_of_troops"),
			
			(try_for_range, ":troop_no", ":start_troop", ":stop_troop"),
				(str_store_troop_name, s31, ":troop_no"),
				(store_attribute_level, ":STR", ":troop_no", ca_strength),
				(store_skill_level, ":riding", "skl_riding", ":troop_no"),
				(store_skill_level, ":power_throw", "skl_power_throw", ":troop_no"),
				(store_skill_level, ":power_draw", "skl_power_draw", ":troop_no"),
				
				(try_for_range, ":i_slot", 0, 30),
					(troop_get_inventory_slot, ":item_no", ":troop_no", ":i_slot"),
					(ge, ":item_no", 1),
					(item_get_difficulty, ":difficulty", ":item_no"),
					(item_get_type, ":item_type", ":item_no"),
					(assign, ":usable", 0),
					(assign, reg32, ":difficulty"),
					(try_begin),
						## RIDING BASED
						(eq, ":item_type", itp_type_horse),
						(assign, reg31, ":riding"),
						(str_store_string, s32, "@Riding skill ({reg31}) less than ({reg32}) Difficulty"),
						(ge, ":riding", ":difficulty"),
						(assign, ":usable", 1),
					(else_try),
						## STRENGTH BASED
						(this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_arrows),
						(this_or_next|is_between, ":item_type", itp_type_head_armor, itp_type_pistol),
						(eq, ":item_type", itp_type_crossbow),
						(assign, reg31, ":STR"),
						(str_store_string, s32, "@Strength ({reg31}) less than ({reg32}) Difficulty"),
						(ge, ":STR", ":difficulty"),
						(assign, ":usable", 1),
					(else_try),
						## POWER DRAW BASED
						(eq, ":item_type", itp_type_bow),
						(assign, reg31, ":power_draw"),
						(str_store_string, s32, "@Power Draw ({reg31}) less than({reg32}) Difficulty"),
						(ge, ":power_draw", ":difficulty"),
						(assign, ":usable", 1),
					(else_try),
						## POWER THROW BASED
						(eq, ":item_type", itp_type_thrown),
						(assign, reg31, ":power_throw"),
						(str_store_string, s32, "@Power Throw ({reg31}) less than ({reg32}) Difficulty"),
						(ge, ":power_throw", ":difficulty"),
						(assign, ":usable", 1),
					(else_try),
						(this_or_next|eq, ":item_type", itp_type_arrows),
						(this_or_next|eq, ":item_type", itp_type_bolts),
						(this_or_next|eq, ":item_type", itp_type_shield),
						(this_or_next|eq, ":item_type", itp_type_goods),
						(this_or_next|eq, ":item_type", itp_type_pistol),
						(this_or_next|eq, ":item_type", itp_type_musket),
						(this_or_next|eq, ":item_type", itp_type_bullets),
						(this_or_next|eq, ":item_type", itp_type_animal),
						(eq, ":item_type", itp_type_book),
						(assign, ":usable", 1),
					(try_end),
					(eq, ":usable", 0),
					(val_add, ":records", 1),
					
				(try_end),
			(try_end),
			
			#### ACTUAL DISPLAY ####
			(store_mul, ":pos_y", ":records", 25),
			
			(try_for_range, ":troop_no", ":start_troop", ":stop_troop"),
				(str_store_troop_name, s31, ":troop_no"),
				(store_attribute_level, ":STR", ":troop_no", ca_strength),
				(store_skill_level, ":riding", "skl_riding", ":troop_no"),
				(store_skill_level, ":power_throw", "skl_power_throw", ":troop_no"),
				(store_skill_level, ":power_draw", "skl_power_draw", ":troop_no"),
				
				(try_for_range, ":i_slot", 0, 30),
					(troop_get_inventory_slot, ":item_no", ":troop_no", ":i_slot"),
					(ge, ":item_no", 1),
					(item_get_difficulty, ":difficulty", ":item_no"),
					(item_get_type, ":item_type", ":item_no"),
					(assign, ":usable", 0),
					(assign, reg42, ":difficulty"),
					(try_begin),
						## RIDING BASED
						(eq, ":item_type", itp_type_horse),
						(assign, reg41, ":riding"),
						(str_store_string, s32, "@Riding skill"),
						(ge, ":riding", ":difficulty"),
						(assign, ":usable", 1),
					(else_try),
						## STRENGTH BASED
						(this_or_next|is_between, ":item_type", itp_type_one_handed_wpn, itp_type_arrows),
						(this_or_next|is_between, ":item_type", itp_type_head_armor, itp_type_pistol),
						(eq, ":item_type", itp_type_crossbow),
						(assign, reg41, ":STR"),
						(str_store_string, s32, "@Strength"),
						(ge, ":STR", ":difficulty"),
						(assign, ":usable", 1),
					(else_try),
						## POWER DRAW BASED
						(eq, ":item_type", itp_type_bow),
						(assign, reg41, ":power_draw"),
						(str_store_string, s32, "@Power Draw"),
						(ge, ":power_draw", ":difficulty"),
						(assign, ":usable", 1),
					(else_try),
						## POWER THROW BASED
						(eq, ":item_type", itp_type_thrown),
						(assign, reg41, ":power_throw"),
						(str_store_string, s32, "@Power Throw"),
						(ge, ":power_throw", ":difficulty"),
						(assign, ":usable", 1),
					(else_try),
						(this_or_next|eq, ":item_type", itp_type_arrows),
						(this_or_next|eq, ":item_type", itp_type_bolts),
						(this_or_next|eq, ":item_type", itp_type_shield),
						(this_or_next|eq, ":item_type", itp_type_goods),
						(this_or_next|eq, ":item_type", itp_type_pistol),
						(this_or_next|eq, ":item_type", itp_type_musket),
						(this_or_next|eq, ":item_type", itp_type_bullets),
						(this_or_next|eq, ":item_type", itp_type_animal),
						(eq, ":item_type", itp_type_book),
						(assign, ":usable", 1),
					(try_end),
					(eq, ":usable", 0),
					
					(assign, reg21, ":troop_no"),
					(str_store_string, s25, "@{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_1", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					
					(str_store_troop_name, s25, ":troop_no"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_2", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					
					(str_store_string, s25, s32),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					
					(str_store_string, s25, "@{reg41}"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_4", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					
					(assign, reg21, ":item_no"),
					(str_store_string, s25, "@{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_5", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					
					(str_store_item_name, s25, ":item_no"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_6", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					
					(str_store_string, s25, "@{reg42}"),
					(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_7", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, kmt_text_size),
					
					
					(val_sub, ":pos_y", 25),
					(call_script, "script_gpu_draw_line", 946, 2, 27, ":pos_y", gpu_gray), # 1315860),
					(val_sub, ":pos_y", kmt_line_step),
					
				(try_end),
				
				
			(try_end), # End of troop_no cycle
			(display_message, "@End of Records.", gpu_debug),
		############### CONTAINER END ###############	
		(set_container_overlay, -1),
		
      ]),
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        #(store_trigger_param_2, ":value"),
		
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, kmt_objects, kmt_obj_button_done, ":object"),
			(presentation_set_duration, 0),
			
		(try_end),
      ]),
	  
    ]),
	
("best_in_class", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(assign,    ":x_col_1",              35), # Item #
		(store_add, ":x_col_2", ":x_col_1",  40), # Item Name
		(store_add, ":x_col_3", ":x_col_2", 225), # Score
		(store_add, ":x_col_4", ":x_col_3", 150), # Data 1
		(store_add, ":x_col_5", ":x_col_4", 150), # Data 2
		(store_add, ":x_col_6", ":x_col_5", 150), # Data 3
		(store_add, ":x_col_7", ":x_col_6", 150), # Data 4
		
		
		(assign, "$gpu_storage", kmt_objects),
		(assign, "$gpu_data", kmt_objects),
		
		(call_script, "script_gpu_create_game_button", "str_kmt_done_button", 500, 25, kmt_obj_button_done), # DONE Button @ 895, 35
		
		(str_store_string, s25, "@Best Equipment in a Class"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", 500, 715, kmt_obj_main_title, gpu_center), # Estates of the Realm
		(call_script, "script_gpu_resize_object", kmt_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", 500, 715, kmt_obj_main_title, gpu_center), # Estates of the Realm
		(call_script, "script_gpu_resize_object", kmt_obj_main_title, 150),
		
		(create_combo_label_overlay, "$g_presentation_obj_1"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 660),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (overlay_add_item, "$g_presentation_obj_1", "@One-Handed Weapons"),
        (overlay_add_item, "$g_presentation_obj_1", "@Two-Handed Weapons"),
        (overlay_add_item, "$g_presentation_obj_1", "@Polearms"),
        (overlay_add_item, "$g_presentation_obj_1", "@Bows"),
        (overlay_add_item, "$g_presentation_obj_1", "@Crossbows"),
        (overlay_add_item, "$g_presentation_obj_1", "@Thrown Weapons"),
        (overlay_add_item, "$g_presentation_obj_1", "@Shields"),
        (overlay_add_item, "$g_presentation_obj_1", "@Helmets"),
        (overlay_add_item, "$g_presentation_obj_1", "@Armors"),
        (overlay_add_item, "$g_presentation_obj_1", "@Boots"),
        (overlay_add_item, "$g_presentation_obj_1", "@Gauntlets"),
        (overlay_add_item, "$g_presentation_obj_1", "@Horses"),
		(overlay_set_val, "$g_presentation_obj_1", "$temp"),
		
		# Header
		(assign, ":pos_y", 655),
		#(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_black),
		(store_sub, ":pos_y_titles", ":pos_y", 13),
		(str_store_string, s25, "@ # "),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_1", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_1", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@ITEM NAME"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_2", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_2", ":pos_y_titles", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@RATING"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_3", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_3", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@DATA 1"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_4", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_4", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@DATA 2"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_5", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_5", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@DATA 3"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_6", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_6", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(str_store_string, s25, "@DATA 4"),
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_7", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_7", ":pos_y_titles", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, kmt_text_size),
		
		(val_sub, ":pos_y", 30),
		(call_script, "script_gpu_draw_line", 950, 2, 25, ":pos_y", gpu_gray),
		
		(call_script, "script_gpu_container_heading", 0, 115, 1000, 485, kmt_obj_main_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			# (assign, ":records", 0),
			# (assign, ":start_troop", "trp_tutorial_maceman"),
			# (assign, ":stop_troop", "trp_end_of_troops"),
			
			
			
			#### ACTUAL DISPLAY ####
			(store_mul, ":pos_y", 10, 25),
			
			(try_begin),
				            (eq, "$temp", 0),  (assign, ":filter_type", itp_type_one_handed_wpn),
				(else_try), (eq, "$temp", 1),  (assign, ":filter_type", itp_type_two_handed_wpn),
				(else_try), (eq, "$temp", 2),  (assign, ":filter_type", itp_type_polearm),
				(else_try), (eq, "$temp", 3),  (assign, ":filter_type", itp_type_bow),
				(else_try), (eq, "$temp", 4),  (assign, ":filter_type", itp_type_crossbow),
				(else_try), (eq, "$temp", 5),  (assign, ":filter_type", itp_type_thrown),
				(else_try), (eq, "$temp", 6),  (assign, ":filter_type", itp_type_shield),
				(else_try), (eq, "$temp", 7),  (assign, ":filter_type", itp_type_head_armor),
				(else_try), (eq, "$temp", 8),  (assign, ":filter_type", itp_type_body_armor),
				(else_try), (eq, "$temp", 9),  (assign, ":filter_type", itp_type_foot_armor),
				(else_try), (eq, "$temp", 10), (assign, ":filter_type", itp_type_hand_armor),
				(else_try), (eq, "$temp", 11), (assign, ":filter_type", itp_type_horse),
			(try_end),
			
			(assign, reg31, ":filter_type"),
			(display_message, "@Filter type = {reg31}.", gpu_debug),
			# (try_for_range, ":item_no", ":start_troop", ":stop_troop"),
				
				# #(eq, ":usable", 0),
				
				# ## OBJ - ITEM #
				# (assign, reg21, ":item_no"),
				# (str_store_string, s25, "@{reg21}"),
				# (call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_1", ":pos_y", 0, gpu_center),
				# (call_script, "script_gpu_resize_object", 0, kmt_text_size),
				
				# ## OBJ - ITEM NAME
				# (str_store_item_name, s25, ":item_no"),
				# (call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_2", ":pos_y", 0, gpu_left),
				# (call_script, "script_gpu_resize_object", 0, kmt_text_size),
				
				# ## OBJ - AUTOLOOT SCORE
				# (str_store_string, s25, s32),
				# (call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_3", ":pos_y", 0, gpu_left),
				# (call_script, "script_gpu_resize_object", 0, kmt_text_size),
				
				# ## OBJ - DATA 1
				# (str_store_string, s25, "@{reg41}"),
				# (call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_4", ":pos_y", 0, gpu_center),
				# (call_script, "script_gpu_resize_object", 0, kmt_text_size),
				
				# ## OBJ - DATA 2
				# (assign, reg21, ":item_no"),
				# (str_store_string, s25, "@{reg21}"),
				# (call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_5", ":pos_y", 0, gpu_center),
				# (call_script, "script_gpu_resize_object", 0, kmt_text_size),
				
				# ## OBJ - DATA 3
				# (str_store_item_name, s25, ":item_no"),
				# (call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_6", ":pos_y", 0, gpu_left),
				# (call_script, "script_gpu_resize_object", 0, kmt_text_size),
				
				# ## OBJ - DATA 4
				# (str_store_string, s25, "@{reg42}"),
				# (call_script, "script_gpu_create_text_label", "str_kmt_s25", ":x_col_7", ":pos_y", 0, gpu_center),
				# (call_script, "script_gpu_resize_object", 0, kmt_text_size),
				
				
				# (val_sub, ":pos_y", 25),
				# (call_script, "script_gpu_draw_line", 946, 2, 27, ":pos_y", gpu_gray), # 1315860),
				# (val_sub, ":pos_y", kmt_line_step),
				
				
			# (try_end), # End of troop_no cycle
			(display_message, "@End of Records.", gpu_debug),
		############### CONTAINER END ###############	
		(set_container_overlay, -1),
		
      ]),
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, kmt_objects, kmt_obj_button_done, ":object"),
			(presentation_set_duration, 0),
			
		(else_try), ####### TYPE SELECTOR #######
          (eq, ":object", "$g_presentation_obj_1"),
          (assign, "$temp", ":value"),
          (start_presentation, "prsnt_best_in_class"),
		  
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