# Kingdom Management Tools (WIP) by Windyplains
# Released --/--/--

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *
from header_presentations import *  # (COMPANIONS OVERSEER MOD)
# from companions_constants import *  # (COMPANIONS OVERSEER MOD)

####################################################################################################################
# scripts is a list of script records.
# Each script record contains the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	 
###########################################################################################################################
#####                                                 FIEF EXCHANGE                                                   #####
###########################################################################################################################
# script_kmt_store_center_long_name_to_s1
# PURPOSE: Converts a basic center_no to a more descriptive name type and stores that in s1.
# EXAMPLE: (call_script, "script_kmt_store_center_long_name_to_s1", ":center_no"), # kmt_scripts.py
("kmt_store_center_long_name_to_s1",
	[
		(store_script_param, ":center_no", 1),
		
		(str_store_party_name, s2, ":center_no"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(str_store_string, s1, "@Town of {s2}"),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(str_store_string, s1, "@{s2}"),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(str_store_string, s1, "@Village of {s2}"),
		(else_try),
			(str_store_string, s1, "@UNDEFINED TYPE of {s2}"),
		(try_end),
	]),
	
# script_kmt_handle_option_change
# PURPOSE: Whenever an option is altered (none, money, lands, ...) this script handles the transition.
# EXAMPLE: (call_script, "script_kmt_handle_option_change", ":base_slot", ":new_type"), # kmt_scripts.py
("kmt_handle_option_change",
	[
		(store_script_param, ":base_slot", 1),
		(store_script_param, ":new_type", 2),
		
		# Determine which side we're on.
		(try_begin),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_1_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_2_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_3_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_4_type),
			(             eq, ":base_slot", kmt3_val_left_opt_5_type),
			(assign, ":slot_troop_no",       kmt3_val_lord_left),
			(assign, ":slot_fiefs_begin",    kmt3_val_left_fiefs_begin),
		(else_try),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_1_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_2_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_3_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_4_type),
			(             eq, ":base_slot", kmt3_val_right_opt_5_type),
			(assign, ":slot_troop_no",       kmt3_val_lord_right),
			(assign, ":slot_fiefs_begin",    kmt3_val_right_fiefs_begin),
		(try_end),
		
		## Setup Slot Variables
		(store_add, ":slot_obj_control",       ":base_slot", 1), # kmt3_obj_left_opt_1 
		(store_add, ":slot_val_control",       ":base_slot", 2), # kmt3_val_left_opt_1
		(store_add, ":slot_obj_type",          ":base_slot", 3), # kmt3_obj_left_opt_1_type
		(store_add, ":slot_obj_control_label", ":base_slot", 4), # kmt3_obj_left_opt_1_slider_label
		(store_add, ":slot_obj_info_1",        ":base_slot", 5), # kmt3_obj_left_opt_1_info_1
		(store_add, ":slot_obj_info_2",        ":base_slot", 6), # kmt3_obj_left_opt_1_info_2
		
		(troop_get_slot, ":troop_no", KMT_OBJECTS, ":slot_troop_no"),
		(try_begin),
			## FILTER - ENSURE LORD HAS CASH.
			(eq, ":new_type", KMT_OPTION_MONEY),
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(store_troop_gold, ":cash_on_hand", ":troop_no"),
			(else_try),
				(troop_get_slot, ":cash_on_hand", ":troop_no", slot_troop_wealth),
			(try_end),
			(lt, ":cash_on_hand", 1),
			(str_store_troop_name, s21, ":troop_no"),
			(display_message, "@Warning - {s21}'s coffers are empty.", gpu_red),
			
		(else_try),
			## FILTER - ONLY ONE MONEY SLIDER ALLOWED (Right)
			(eq, ":new_type", KMT_OPTION_MONEY),
			(eq, ":slot_troop_no", kmt3_val_lord_right),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_1_type, KMT_OPTION_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_2_type, KMT_OPTION_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_3_type, KMT_OPTION_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_4_type, KMT_OPTION_MONEY),
			(             troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_5_type, KMT_OPTION_MONEY),
			(str_store_troop_name, s21, ":troop_no"),
			(display_message, "@Warning - {s21} already has one slider for money allotments active.", gpu_red),
			
		(else_try),
			## FILTER - ONLY ONE MONEY SLIDER ALLOWED (Left)
			(eq, ":new_type", KMT_OPTION_MONEY),
			(eq, ":slot_troop_no", kmt3_val_lord_left),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_1_type, KMT_OPTION_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_2_type, KMT_OPTION_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_3_type, KMT_OPTION_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_4_type, KMT_OPTION_MONEY),
			(             troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_5_type, KMT_OPTION_MONEY),
			(str_store_troop_name, s21, ":troop_no"),
			(display_message, "@Warning - {s21} already has one slider for money allotments active.", gpu_red),
			
		(else_try),
			## FILTER - ENSURE LORD HAS ANY VALID FIEFS.
			(eq, ":new_type", KMT_OPTION_FIEF),
			(assign, ":count", 0),
			(try_for_range, ":center_no", centers_begin, centers_end),
				(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
				(val_add, ":count", 1),
			(try_end),
			(eq, ":count", 0),
			(str_store_troop_name, s21, ":troop_no"),
			(display_message, "@Warning - {s21} has no valid fiefs to offer.", gpu_red),
			
		(else_try),
			## FILTER - ENSURE KING HAS CASH.
			(eq, ":new_type", KMT_OPTION_KINGS_MONEY),
			(store_troop_gold, ":cash_on_hand", "trp_player"),
			(lt, ":cash_on_hand", 1),
			(str_store_troop_name, s21, ":troop_no"),
			(display_message, "@Warning - {s21}'s coffers are empty.", gpu_red),
			
		(else_try),
			## FILTER - ROYAL COFFERS CAN ONLY BE IMPLEMENTED BY A RULER.
			(eq, ":new_type", KMT_OPTION_KINGS_MONEY),
			(call_script, "script_cf_qus_player_is_king", 0),
			(display_message, "@Warning - Only a ruler may select this option.", gpu_red),
			
		(else_try),
			## FILTER - ROYAL COFFERS CAN ONLY BE USED ON A DEAL BETWEEN VASSALS.
			(eq, ":new_type", KMT_OPTION_KINGS_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_lord_left, "trp_player"),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_lord_right, "trp_player"),
			(display_message, "@Warning - This option may only be used in deals between two vassals.", gpu_red),
			
		(else_try),
			## FILTER - ONLY ONE MONEY SLIDER ALLOWED (Right)
			(eq, ":new_type", KMT_OPTION_KINGS_MONEY),
			(eq, ":slot_troop_no", kmt3_val_lord_right),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_1_type, KMT_OPTION_KINGS_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_2_type, KMT_OPTION_KINGS_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_3_type, KMT_OPTION_KINGS_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_4_type, KMT_OPTION_KINGS_MONEY),
			(             troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_5_type, KMT_OPTION_KINGS_MONEY),
			(troop_get_type, reg21, "trp_player"),
			(display_message, "@Warning - The {reg21?Queen:King} already has one slider for money allotments active.", gpu_red),
			
		(else_try),
			## FILTER - ONLY ONE MONEY SLIDER ALLOWED (Left)
			(eq, ":new_type", KMT_OPTION_KINGS_MONEY),
			(eq, ":slot_troop_no", kmt3_val_lord_left),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_1_type, KMT_OPTION_KINGS_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_2_type, KMT_OPTION_KINGS_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_3_type, KMT_OPTION_KINGS_MONEY),
			(this_or_next|troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_4_type, KMT_OPTION_KINGS_MONEY),
			(             troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_5_type, KMT_OPTION_KINGS_MONEY),
			(troop_get_type, reg21, "trp_player"),
			(display_message, "@Warning - The {reg21?Queen:King} already has one slider for money allotments active.", gpu_red),
			
		(else_try),
			## DEFAULT - ALL FILTERS PASSSED
			(troop_set_slot, KMT_OBJECTS, ":base_slot", ":new_type"),
			# Wipe out any previous data on this option.
			(troop_set_slot, KMT_OBJECTS, ":slot_obj_control", 0),
			(troop_set_slot, KMT_OBJECTS, ":slot_val_control", 0),
			(troop_set_slot, KMT_OBJECTS, ":slot_obj_type", 0),
			(troop_set_slot, KMT_OBJECTS, ":slot_obj_control_label", 0),
			(troop_set_slot, KMT_OBJECTS, ":slot_obj_info_1", 0),
			(troop_set_slot, KMT_OBJECTS, ":slot_obj_info_2", 0),
			(try_begin),
				(eq, ":new_type", KMT_OPTION_FIEF),
				(troop_set_slot, KMT_OBJECTS, ":slot_val_control", ":slot_fiefs_begin"),
			(try_end),
			
		(try_end),
		# Update ratings.
		(call_script, "script_kmt_get_offer_ratings"),
		(start_presentation, "prsnt_kmt_fief_exchange"),
	]),
	
# script_kmt_create_exchange_option_controls
# PURPOSE: Creates the necessary offering controls for the fief exchange interface since these controls are used in 10 locations.
# EXAMPLE: (call_script, "script_kmt_create_exchange_option_controls", base_slot, ":pos_y"), # kmt_scripts.py
("kmt_create_exchange_option_controls",
	[
		(store_script_param, ":base_slot", 1),
		(store_script_param, ":pos_y", 2),
		
		# kmt3_val_left_opt_1_type           = 110 # Holds the option's type (cash, lands, none, etc...)
		# kmt3_obj_left_opt_1                = 111 # Contains the object number of the actual offer slider.
		# kmt3_val_left_opt_1                = 112 # Contains the value of the actual offer slider.
		# kmt3_obj_left_opt_1_type           = 113 # Contains the object number of the option type.
		# kmt3_obj_left_opt_1_slider_label   = 114 # Contains the object number of the label describing the slider's value.
		# kmt3_obj_left_opt_1_info_1         = 115 # Contains the object number of the first extra info line.
		# kmt3_obj_left_opt_1_info_2         = 116 # Contains the object number of the second extra info line.
		
		## Setup Slot Variables
		(store_add, ":slot_obj_control",       ":base_slot", 1), # kmt3_obj_left_opt_1 
		(store_add, ":slot_val_control",       ":base_slot", 2), # kmt3_val_left_opt_1
		(store_add, ":slot_obj_type",          ":base_slot", 3), # kmt3_obj_left_opt_1_type
		(store_add, ":slot_obj_control_label", ":base_slot", 4), # kmt3_obj_left_opt_1_slider_label
		(store_add, ":slot_obj_info_1",        ":base_slot", 5), # kmt3_obj_left_opt_1_info_1
		(store_add, ":slot_obj_info_2",        ":base_slot", 6), # kmt3_obj_left_opt_1_info_2
		(store_add, ":slot_obj_bold_effect",   ":base_slot", 7), # kmt3_obj_left_bold_effect
		
		## Setup Horizontal Placing
		(assign, ":pos_x_menus", 195),
		(assign, ":pos_x_labels", 0),
		(assign, ":pos_x_sliders", 75),
		(assign, ":pos_x_centered_text", 170),
		(try_begin),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_1_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_2_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_3_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_4_type),
			(             eq, ":base_slot", kmt3_val_left_opt_5_type),
			(assign, ":slot_troop_no",       kmt3_val_lord_left),
			(assign, ":slot_val_fief_count", kmt3_val_left_fief_count),
			(assign, ":slot_fiefs_begin",    kmt3_val_left_fiefs_begin), 
		(else_try),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_1_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_2_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_3_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_4_type),
			(             eq, ":base_slot", kmt3_val_right_opt_5_type),
			(assign, ":slot_troop_no",       kmt3_val_lord_right),
			(assign, ":slot_val_fief_count", kmt3_val_right_fief_count),
			(assign, ":slot_fiefs_begin",    kmt3_val_right_fiefs_begin), 
		(try_end),
		
		## OBJ - TEXT - OPTION
		(str_store_string, s21, "@Offering:"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_labels", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_labels", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - MENU - OPTION
		(create_combo_button_overlay, reg1),
		(store_sub, ":pos_y_temp", ":pos_y", 15),
		(troop_set_slot, KMT_OBJECTS, ":slot_obj_type", reg1),
		(position_set_x, pos1, ":pos_x_menus"),
		(position_set_y, pos1, ":pos_y_temp"),
		(overlay_set_position, reg1, pos1),
		(overlay_add_item, reg1, "@Nothing"),
		(overlay_add_item, reg1, "@Lands"),
		(overlay_add_item, reg1, "@Money"),
		(overlay_add_item, reg1, "@Royal Coffers"),
		(troop_get_slot, ":value", KMT_OBJECTS, ":base_slot"),
		(overlay_set_val, reg1, ":value"),
		(call_script, "script_gpu_resize_object", ":slot_obj_type", 75),
		
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_NONE),
			(val_sub, ":pos_y", 35),
			
		(else_try),
			(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
			(val_sub, ":pos_y", 45),
			## OBJ - SLIDER OPTION
			(assign, ":min_slot", ":slot_fiefs_begin"),
			(troop_get_slot, ":max_slot", KMT_OBJECTS, ":slot_val_fief_count"),
			(call_script, "script_gpu_create_slider", ":min_slot", ":max_slot", ":pos_x_sliders", ":pos_y", ":slot_obj_control", ":slot_val_control"),
			(call_script, "script_gpu_resize_object", ":slot_obj_control", 75),
			(val_sub, ":pos_y", 10),
			
			## OBJ - TEXT - FIEF OFFERED
			(troop_get_slot, ":slot_no", KMT_OBJECTS, ":slot_val_control"),
			(troop_get_slot, ":center_no", KMT_OBJECTS, ":slot_no"),
			(call_script, "script_kmt_store_center_long_name_to_s1", ":center_no"),
			(str_store_string, s21, s1),
			(store_add, ":pos_y_temp", ":pos_y", 15),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_centered_text", ":pos_y", ":slot_obj_control_label", gpu_center),
			(call_script, "script_gpu_resize_object", ":slot_obj_control_label", 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_centered_text", ":pos_y", ":slot_obj_bold_effect", gpu_center),
			(call_script, "script_gpu_resize_object", ":slot_obj_bold_effect", 75),
			(val_sub, ":pos_y", 20),
			
			## OBJ - TEXT - FIEF PROSPERITY
			(party_get_slot, reg21, ":center_no", slot_town_prosperity),
			(str_store_string, s21, "@Prosperity: {reg21} / 99"),
			(store_add, ":pos_y_temp", ":pos_y", 15),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_centered_text", ":pos_y", ":slot_obj_info_1", gpu_center),
			(call_script, "script_gpu_resize_object", ":slot_obj_info_1", 75),
			(val_sub, ":pos_y", 20),
			
			## OBJ - TEXT - FIEF IMPROVEMENTS
			# Assess improvements value.
			(call_script, "script_improvement_assess_center_value", ":center_no"), # improvements_scripts.py (reg1 = built, reg2 = total value)
			(store_sub, reg22, reg2, 1),
			(str_store_string, s21, "@Improvements: {reg1} built, {reg2} denar{reg22?s:}"),
			(store_add, ":pos_y_temp", ":pos_y", 15),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_centered_text", ":pos_y", ":slot_obj_info_2", gpu_center),
			(call_script, "script_gpu_resize_object", ":slot_obj_info_2", 75),
			(val_sub, ":pos_y", 35),
			
		(else_try), ## MONEY OFFERING
			(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_MONEY),
			(val_sub, ":pos_y", 45),
			## OBJ - SLIDER OPTION
			(troop_get_slot, ":troop_no", KMT_OBJECTS, ":slot_troop_no"),
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(store_troop_gold, ":cash_limit", ":troop_no"),
				(val_min, ":cash_limit", 200000), # Set a hard limit on how much cash can be offered.
			(else_try),
				(troop_get_slot, ":cash_limit", ":troop_no", slot_troop_wealth),
				(val_mul, ":cash_limit", 30),
				(val_div, ":cash_limit", 100), # Lords will only trade up to 30% of their coffers.
				(val_min, ":cash_limit", 200000), # Set a hard limit on how much cash can be offered.
			(try_end),
			(call_script, "script_gpu_create_slider", 0, ":cash_limit", ":pos_x_sliders", ":pos_y", ":slot_obj_control", ":slot_val_control"),
			(call_script, "script_gpu_resize_object", ":slot_obj_control", 75),
			(val_sub, ":pos_y", 10),
			
			## OBJ - TEXT - AMOUNT OFFERED
			(troop_get_slot, reg21, KMT_OBJECTS, ":slot_val_control"),
			(store_sub, reg22, reg21, 1),
			(str_store_string, s21, "@{reg21} denar{reg22?s:}"),
			(store_add, ":pos_y_temp", ":pos_y", 15),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_centered_text", ":pos_y", ":slot_obj_control_label", gpu_center),
			(call_script, "script_gpu_resize_object", ":slot_obj_control_label", 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_centered_text", ":pos_y", ":slot_obj_bold_effect", gpu_center),
			(call_script, "script_gpu_resize_object", ":slot_obj_bold_effect", 75),
			(val_sub, ":pos_y", 35),
			
		(else_try), ## KING'S OFFERING
			(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_KINGS_MONEY),
			(val_sub, ":pos_y", 45),
			## OBJ - SLIDER OPTION
			(store_troop_gold, ":cash_limit", "trp_player"),
			(val_min, ":cash_limit", 200000), # Set a hard limit on how much cash can be offered.
			(call_script, "script_gpu_create_slider", 0, ":cash_limit", ":pos_x_sliders", ":pos_y", ":slot_obj_control", ":slot_val_control"),
			(call_script, "script_gpu_resize_object", ":slot_obj_control", 75),
			(val_sub, ":pos_y", 10),
			
			## OBJ - TEXT - AMOUNT OFFERED
			(troop_get_slot, reg21, KMT_OBJECTS, ":slot_val_control"),
			(store_sub, reg22, reg21, 1),
			(str_store_string, s21, "@{reg21} denar{reg22?s:}"),
			(store_add, ":pos_y_temp", ":pos_y", 15),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_centered_text", ":pos_y", ":slot_obj_control_label", gpu_center),
			(call_script, "script_gpu_resize_object", ":slot_obj_control_label", 75),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_centered_text", ":pos_y", ":slot_obj_bold_effect", gpu_center),
			(call_script, "script_gpu_resize_object", ":slot_obj_bold_effect", 75),
			(val_sub, ":pos_y", 35),
			
		(try_end),
		
		(assign, reg1, ":pos_y"),
	]),
	
# script_kmt_get_option_spacing
# PURPOSE: Converts a basic center_no to a more descriptive name type and stores that in s1.
# EXAMPLE: (call_script, "script_kmt_get_option_spacing", ":option_type", ":pos_y"), # kmt_scripts.py
("kmt_get_option_spacing",
	[
		(store_script_param, ":option_type", 1),
		(store_script_param, ":pos_y", 2),
		
		(assign, ":y_shift_none", 35),
		(assign, ":y_shift_money", 90),
		(assign, ":y_shift_lands", 130),
		# Determine our starting point based on options chosen.
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, ":option_type", KMT_OPTION_NONE),
			(val_add, ":pos_y", ":y_shift_none"),
		(else_try),
			(troop_slot_eq, KMT_OBJECTS, ":option_type", KMT_OPTION_MONEY),
			(val_add, ":pos_y", ":y_shift_money"),
		(else_try),
			(troop_slot_eq, KMT_OBJECTS, ":option_type", KMT_OPTION_KINGS_MONEY),
			(val_add, ":pos_y", ":y_shift_money"),
		(else_try),
			(troop_slot_eq, KMT_OBJECTS, ":option_type", KMT_OPTION_FIEF),
			(val_add, ":pos_y", ":y_shift_lands"),
		(try_end),
		(assign, reg1, ":pos_y"),
	]),
	
# script_kmt_get_center_value_rating
# PURPOSE: Converts a basic center_no to a more descriptive name type and stores that in s1.
# EXAMPLE: (call_script, "script_kmt_get_center_value_rating", ":center_no", ":troop_no"), # kmt_scripts.py
("kmt_get_center_value_rating",
	[
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_no", 2),  # Buyer / Seller
		
		## INITIALIZATION
		(assign, ":rating", 0),
		
		## PROSPERITY (50 to 99) x 5
		(party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
		(val_max, ":prosperity", 50), # Reduce how effective "gaming the market" is.
		(store_mul, ":rating_prosperity", ":prosperity", 5),
		
		## DISTANCE FROM BEST CENTER
		(assign, ":best_center_type", -1),
		# (assign, ":best_center_no", -1),
		(assign, ":best_center_distance", 100000000),
		(try_for_range, ":fief_no", centers_begin, centers_end),
			(party_slot_eq, ":fief_no", slot_town_lord, ":troop_no"),
			
			# Determine the best center type.
			(try_begin), # Nothing currently rated, take anything.
				(eq, ":best_center_type", -1),
				(party_get_slot, ":best_center_type", ":fief_no", slot_party_type),
				(assign, ":best_center_distance", 100000000),
			(else_try), # Upgrade from a village to a castle or town.
				(eq, ":best_center_type", spt_village),
				(this_or_next|party_slot_eq, ":fief_no", slot_party_type, spt_castle),
				(party_slot_eq, ":fief_no", slot_party_type, spt_town),
				(party_get_slot, ":best_center_type", ":fief_no", slot_party_type),
				(assign, ":best_center_distance", 100000000),
			(else_try), # Upgrade from a castle to a town.
				(eq, ":best_center_type", spt_castle),
				(party_slot_eq, ":fief_no", slot_party_type, spt_town),
				(party_get_slot, ":best_center_type", ":fief_no", slot_party_type),
				(assign, ":best_center_distance", 100000000),
			(try_end),
			
			# Determine the closest center of the current best type to this new property.
			(try_begin),
				(party_slot_eq, ":fief_no", slot_party_type, ":best_center_type"),
				(store_distance_to_party_from_party, ":distance", ":center_no", ":fief_no"),
				(lt, ":distance", ":best_center_distance"),
				(assign, ":best_center_distance", ":distance"),
				# (assign, ":best_center_no", ":fief_no"),
			(try_end),
		(try_end),
		(store_sub, ":rating_distance", 30, ":best_center_distance"),
		(val_mul, ":rating_distance", 3),
		(val_max, ":rating_distance", 0), # Prevent negative ratings here.
		
		## BOUND CENTER BONUS
		(assign, ":rating_bound", 0),
		(try_begin), # You own a castle / town bound to this village you're acquiring.
			(party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
			(party_slot_eq, ":bound_center", slot_town_lord, ":troop_no"),
			(assign, ":rating_bound", 300), 
		(else_try), # You own a village bound to this castle / town you're acquiring.
			(try_for_range, ":fief_no", villages_begin, villages_end),
				(party_slot_eq, ":fief_no", slot_town_lord, ":troop_no"),
				(party_slot_eq, ":fief_no", slot_village_bound_center, ":center_no"),
				(val_add, ":rating_bound", 250), 
			(try_end),
		(try_end),
		
		## POTENTIAL FOR TITLE UPGRADE
		(call_script, "script_kmt_center_alters_vassal_title", ":center_no", ":troop_no"),
		(try_begin),
			(ge, reg1, 1), # New land will bring a higher title.
			(store_mul, ":rating_title", reg1, 200),
		(else_try),
			(assign, ":rating_title", 0),
		(try_end),
		
		## IMPROVEMENT VALUE
		(call_script, "script_improvement_assess_center_value", ":center_no"), # improvements_scripts.py (reg1 = built, reg2 = total value)
		(assign, ":improvement_value", reg2),
		(store_mul, ":rating_improvements", ":improvement_value", 8),
		(val_div, ":rating_improvements", 100),
		
		## UNCOLLECTED RENTS
		(party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
		(party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
		(store_add, ":uncollected_cash", ":accumulated_rents", ":accumulated_tariffs"),
		(store_mul, ":rating_rents", ":uncollected_cash", 10),
		(val_div, ":rating_rents", 100),
		
		## INFESTATION PENALTY
		(assign, ":rating_raided", 0),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(party_slot_eq, ":center_no", slot_village_state, svs_looted),
			(val_add, ":rating_raided", -150),
		(try_end),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(party_slot_ge, ":center_no", slot_village_infested_by_bandits, 1),
			(val_add, ":rating_raided", -150),
		(try_end),
		
		## COMBINE RATINGS
		(val_add, ":rating", ":rating_prosperity"),
		(val_add, ":rating", ":rating_improvements"),
		(val_add, ":rating", ":rating_rents"),
		(val_add, ":rating", ":rating_distance"),
		(val_add, ":rating", ":rating_bound"),
		(val_add, ":rating", ":rating_raided"),
		(val_add, ":rating", ":rating_title"),
		(val_max, ":rating", 250),
		
		## CENTER TYPE MULTIPLIER
		(assign, ":center_multiplier", 1),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(assign, ":center_multiplier", 7),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(assign, ":center_multiplier", 4),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(assign, ":center_multiplier", 2),
		(try_end),
		(val_mul, ":rating", ":center_multiplier"),
		
		### DIAGNOSTIC+ ###
		# (assign, reg31, ":rating_prosperity"),
		# (assign, reg32, ":rating_improvements"),
		# (assign, reg33, ":rating_rents"),
		# (assign, reg34, ":rating_distance"),
		# (assign, reg35, ":rating_bound"),
		# (assign, reg36, ":rating_raided"),
		# (assign, reg37, ":rating_title"),
		# (assign, reg38, ":rating"),
		# (assign, reg39, ":center_multiplier"),
		# (display_message, "@DEBUG: ({reg31} prosperity) + ({reg32} improvements) + ({reg33} rents) + ({reg34} distance)", gpu_debug),
		# (display_message, "@DEBUG: ({reg35} bound) + ({reg36} raided) + ({reg37} title) + ({reg39} multiplier)", gpu_debug),
		# (display_message, "@DEBUG: Final rating = {reg38}", gpu_debug),
		### DIAGNOSTIC- ###
		
		(assign, reg1, ":rating"),
	]),
	
# script_kmt_center_alters_vassal_title
# PURPOSE: Checks if acquiring this center will either raise (positive value), reduce (negative value) or have no effect on a vassal's status.
# EXAMPLE: (call_script, "script_kmt_center_alters_vassal_title", ":center_no", ":troop_no"), # kmt_scripts.py
("kmt_center_alters_vassal_title",
	[
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_no", 2),
		
		## Determine which lord we're using.
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_lord_left, ":troop_no"),
			(assign, ":slot_best_type", kmt3_val_left_best_fief_type),
			(assign, ":slot_best_count", kmt3_val_left_best_fief_count),
		(else_try),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_lord_right, ":troop_no"),
			(assign, ":slot_best_type", kmt3_val_right_best_fief_type),
			(assign, ":slot_best_count", kmt3_val_right_best_fief_count),
		(try_end),
		
		## DETERMINE THE LORD'S CURRENT BEST CENTER
		(troop_get_slot, ":troop_spouse", ":troop_no", slot_troop_spouse),
		(assign, ":best_center_type", -1),
		(assign, ":best_center_count", 0),
		(try_for_range, ":fief_no", centers_begin, centers_end),
			(this_or_next|party_slot_eq, ":fief_no", slot_town_lord, ":troop_no"),
			(party_slot_eq, ":fief_no", slot_town_lord, ":troop_spouse"), # For female players married to lords.
			(store_troop_faction, ":faction_troop", ":troop_no"),
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(assign, ":faction_troop", "$players_kingdom"),
			(try_end),
			(try_begin),
				(is_between, ":center_no", centers_begin, centers_end),
				(store_faction_of_party, ":faction_center", ":center_no"),
			(else_try),
				(assign, ":faction_center", ":faction_troop"),
			(try_end),
			(eq, ":faction_troop", ":faction_center"),
			# Determine the best center type.
			(try_begin), # Nothing currently rated, take anything.
				(eq, ":best_center_type", -1),
				(party_get_slot, ":best_center_type", ":fief_no", slot_party_type),
				(assign, ":best_center_count", 0),
			(else_try), # Upgrade from a village to a castle or town.
				(eq, ":best_center_type", spt_village),
				(this_or_next|party_slot_eq, ":fief_no", slot_party_type, spt_castle),
				(party_slot_eq, ":fief_no", slot_party_type, spt_town),
				(party_get_slot, ":best_center_type", ":fief_no", slot_party_type),
				(assign, ":best_center_count", 0),
			(else_try), # Upgrade from a castle to a town.
				(eq, ":best_center_type", spt_castle),
				(party_slot_eq, ":fief_no", slot_party_type, spt_town),
				(party_get_slot, ":best_center_type", ":fief_no", slot_party_type),
				(assign, ":best_center_count", 0),
			(try_end),
			# Tally the number of the best type this lord has.
			(try_begin),
				(party_slot_eq, ":fief_no", slot_party_type, ":best_center_type"),
				(val_add, ":best_center_count", 1),
			(try_end),
		(try_end),
		
		## DETERMINE TITLE SHIFT
		(try_begin),
			(eq, ":best_center_type", -1),
			(assign, ":current_title", 0),
		(else_try),
			(eq, ":best_center_type", spt_village),
			(assign, ":current_title", 1),
		(else_try),
			(eq, ":best_center_type", spt_castle),
			(assign, ":current_title", 2),
		(else_try),
			(eq, ":best_center_type", spt_town),
			(assign, ":current_title", 3),
		(try_end),
		
		## DETERMINE TITLE LEVEL FOR OFFERED FIEF
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(is_between, ":center_no", centers_begin, centers_end),
			(assign, ":offered_title", 1),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(is_between, ":center_no", centers_begin, centers_end),
			(assign, ":offered_title", 2),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(is_between, ":center_no", centers_begin, centers_end),
			(assign, ":offered_title", 3),
		(else_try),
			(assign, ":offered_title", 0),
		(try_end),
		
		(store_sub, reg1, ":offered_title", ":current_title"),
		(troop_set_slot, KMT_OBJECTS, ":slot_best_type", ":best_center_type"),
		(troop_set_slot, KMT_OBJECTS, ":slot_best_count", ":best_center_count"),
		### DIAGNOSTIC+ ###
		# (assign, reg31, ":best_center_count"),
		# (try_begin),
			# (eq, ":best_center_type", spt_town),
			# (str_store_string, s31, "@TOWN"),
		# (else_try),
			# (eq, ":best_center_type", spt_castle),
			# (str_store_string, s31, "@CASTLE"),
		# (else_try),
			# (eq, ":best_center_type", spt_village),
			# (str_store_string, s31, "@VILLAGE"),
		# (else_try),
			# (str_store_string, s31, "@LANDLESS"),
		# (try_end),
		# (str_store_troop_name, s32, ":troop_no"),
		# (display_message, "@DEBUG: {s32}'s best type is a {s31} of which he has {reg31}. (rating set)", gpu_debug),
		### DIAGNOSTIC- ###
	]),
	
# script_kmt_get_offer_ratings
# PURPOSE: This combines all of the offers made on a given side and updates those displays.  Only useful within the "fief exchange" interface.
# EXAMPLE: (call_script, "script_kmt_get_offer_ratings"), # kmt_scripts.py
("kmt_get_offer_ratings",
	[
		(troop_get_slot, ":troop_left", KMT_OBJECTS, kmt3_val_lord_left),
		(troop_get_slot, ":troop_right", KMT_OBJECTS, kmt3_val_lord_right),
		(call_script, "script_kmt_center_alters_vassal_title", 0, ":troop_left"),
		(call_script, "script_kmt_center_alters_vassal_title", 0, ":troop_right"),
		
		## LEFT LORD
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_left_opt_1_type),
		(assign, ":rating_left", reg1),
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_left_opt_2_type),
		(val_add, ":rating_left", reg1),
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_left_opt_3_type),
		(val_add, ":rating_left", reg1),
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_left_opt_4_type),
		(val_add, ":rating_left", reg1),
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_left_opt_5_type),
		(val_add, ":rating_left", reg1),
		# Factor in Persuasion Benefit
		(store_skill_level, ":persuasion", "skl_persuasion", ":troop_left"),
		(val_mul, ":persuasion", 8),
		(store_skill_level, ":trade", "skl_trade", ":troop_left"),
		(val_mul, ":trade", 8),
		(store_add, ":convincing_skill", ":persuasion", ":trade"),
		(store_mul, ":rating_bonus", ":rating_left", ":convincing_skill"),
		(val_div, ":rating_bonus", 1000),
		(val_add, ":rating_left", ":rating_bonus"),
		(troop_set_slot, KMT_OBJECTS, kmt3_val_left_rating, ":rating_left"),
		
		## UPDATE LEFT RATING DISPLAY
		(troop_get_slot, ":object_no", KMT_OBJECTS, kmt3_obj_left_rating),
		(assign, reg1, ":rating_left"),
		(str_store_string, s1, "@{reg1}"),
		(overlay_set_text, ":object_no", s1),
		
		## UPDATE LEFT PENALTY DISPLAY (Ruler Mode)
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 1),
			(call_script, "script_kmt_get_relation_penalty_for_offer", kmt3_val_left_rating),
			(call_script, "script_kmt_describe_relation_penalty_for_offer", kmt3_val_lord_left),
			(troop_get_slot, ":object_no", KMT_OBJECTS, kmt3_obj_left_label_forced_loss),
			(overlay_set_text, ":object_no", s21),
		(try_end),
		
		## RIGHT LORD
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_right_opt_1_type),
		(assign, ":rating_right", reg1),
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_right_opt_2_type),
		(val_add, ":rating_right", reg1),
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_right_opt_3_type),
		(val_add, ":rating_right", reg1),
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_right_opt_4_type),
		(val_add, ":rating_right", reg1),
		(call_script, "script_kmt_handle_offer_type_for_rating", kmt3_val_right_opt_5_type),
		(val_add, ":rating_right", reg1),
		# Factor in Persuasion Benefit
		(store_skill_level, ":persuasion", "skl_persuasion", ":troop_right"),
		(val_mul, ":persuasion", 8),
		(store_skill_level, ":trade", "skl_trade", ":troop_right"),
		(val_mul, ":trade", 8),
		(store_add, ":convincing_skill", ":persuasion", ":trade"),
		(store_mul, ":rating_bonus", ":rating_right", ":convincing_skill"),
		(val_div, ":rating_bonus", 1000),
		(val_add, ":rating_right", ":rating_bonus"),
		(troop_set_slot, KMT_OBJECTS, kmt3_val_right_rating, ":rating_right"),
		
		## UPDATE RIGHT RATING DISPLAY
		(troop_get_slot, ":object_no", KMT_OBJECTS, kmt3_obj_right_rating),
		(assign, reg1, ":rating_right"),
		(str_store_string, s1, "@{reg1}"),
		(overlay_set_text, ":object_no", s1),
		
		## UPDATE RIGHT PENALTY DISPLAY (Ruler Mode)
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 1),
			(call_script, "script_kmt_get_relation_penalty_for_offer", kmt3_val_right_rating),
			(call_script, "script_kmt_describe_relation_penalty_for_offer", kmt3_val_lord_right),
			(troop_get_slot, ":object_no", KMT_OBJECTS, kmt3_obj_right_label_forced_loss),
			(overlay_set_text, ":object_no", s21),
		(try_end),
	]),
	
# script_kmt_handle_offer_type_for_rating
# PURPOSE: This combines all of the offers made on a given side and updates those displays.  Only useful within the "fief exchange" interface.
# EXAMPLE: (call_script, "script_kmt_handle_offer_type_for_rating", ":base_slot"), # kmt_scripts.py
("kmt_handle_offer_type_for_rating",
	[
		(store_script_param, ":base_slot", 1),
		
		(troop_get_slot, ":offer_type", KMT_OBJECTS, ":base_slot"),
		## Determine side
		(try_begin),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_1_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_2_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_3_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_4_type),
			(             eq, ":base_slot", kmt3_val_left_opt_5_type),
			# (troop_get_slot, ":troop_seller", KMT_OBJECTS, kmt3_val_lord_left),
			(troop_get_slot, ":troop_buyer", KMT_OBJECTS, kmt3_val_lord_right),
		(else_try),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_1_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_2_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_3_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_4_type),
			(             eq, ":base_slot", kmt3_val_right_opt_5_type),
			(troop_get_slot, ":troop_buyer", KMT_OBJECTS, kmt3_val_lord_left),
			# (troop_get_slot, ":troop_seller", KMT_OBJECTS, kmt3_val_lord_right),
		(try_end),
		
		(assign, ":offer_rating", 0),
		(try_begin),
			(eq, ":offer_type", KMT_OPTION_NONE),
			(val_add, ":offer_rating", 0),
		(else_try),
			(eq, ":offer_type", KMT_OPTION_MONEY),
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
			(store_add, ":money_slot", ":base_slot", ":offset"),
			(troop_get_slot, ":cash", KMT_OBJECTS, ":money_slot"),
			(val_mul, ":cash", 17),
			(val_div, ":cash", 100),
			(val_add, ":offer_rating", ":cash"),
		(else_try),
			(eq, ":offer_type", KMT_OPTION_KINGS_MONEY),
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
			(store_add, ":money_slot", ":base_slot", ":offset"),
			(troop_get_slot, ":cash", KMT_OBJECTS, ":money_slot"),
			(val_mul, ":cash", 17),
			(val_div, ":cash", 100),
			(val_add, ":offer_rating", ":cash"),
		(else_try),
			(eq, ":offer_type", KMT_OPTION_FIEF),
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
			(store_add, ":slot_no", ":base_slot", ":offset"),
			(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
			(troop_get_slot, ":center_no", KMT_OBJECTS, ":center_slot"),
			(call_script, "script_kmt_get_center_value_rating", ":center_no", ":troop_buyer"),
			(call_script, "script_kmt_divide_fief_rating_by_multiple_offerings", ":base_slot", reg1),
			(val_add, ":offer_rating", reg1),
		(try_end),
		(assign, reg1, ":offer_rating"),
	]),
	
# script_kmt_divide_fief_rating_by_multiple_offerings
# PURPOSE: In the event that the same fief is being offered more than once this will divide the rating by the number of offerings.
# EXAMPLE: (call_script, "script_kmt_divide_fief_rating_by_multiple_offerings", ":base_slot", ":rating"), # kmt_scripts.py
("kmt_divide_fief_rating_by_multiple_offerings",
	[
		(store_script_param, ":base_slot", 1),
		(store_script_param, ":rating", 2),
		
		# Convert our offered slot into a center.
		(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
		(store_add, ":slot_no", ":base_slot", ":offset"),
		(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
		# (troop_get_slot, ":center_no", KMT_OBJECTS, ":center_slot"),
		
		(assign, ":fief_count", 0), # Start at zero since at least one of these will match the offered fief.
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_1_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_1, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_2_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_2, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_3_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_3, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_4_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_4, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_5_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_left_opt_5, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_1_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_1, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_2_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_2, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_3_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_3, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_4_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_4, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_5_type, KMT_OPTION_FIEF),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_right_opt_5, ":center_slot"),
			(val_add, ":fief_count", 1),
		(try_end),
		(store_div, reg1, ":rating", ":fief_count"),
	]),
	
# script_cf_kmt_vassal_will_lose_status_in_trade
# PURPOSE: This checks a specific option to see if the vassal's title will go down due to the proposed trade.
# EXAMPLE: (call_script, "script_cf_kmt_vassal_will_lose_status_in_trade", ":troop_no"), # kmt_scripts.py
("cf_kmt_vassal_will_lose_status_in_trade",
	[
		(store_script_param, ":troop_no", 1),
		
		(assign, ":block_1", -1),
		(assign, ":block_2", -1),
		(assign, ":block_3", -1),
		(assign, ":block_4", -1),
		(assign, ":block_5", -1),
		(assign, ":accept_1", -1),
		(assign, ":accept_2", -1),
		(assign, ":accept_3", -1),
		(assign, ":accept_4", -1),
		(assign, ":accept_5", -1),
		
		(try_begin),
			(troop_slot_eq, KMT_OBJECTS, kmt3_val_lord_left, ":troop_no"),
			(assign, ":slot_best_type",  kmt3_val_left_best_fief_type),
			# (assign, ":slot_best_count", kmt3_val_left_best_fief_count),
			## Get offered center in option #1 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_1_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_1", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #2 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_2_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_2", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #3 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_3_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_3", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #4 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_4_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_4", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #5 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_5_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_5", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #1 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_1_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_1", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #2 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_2_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_2", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #3 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_3_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_3", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #4 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_4_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_4", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #5 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_5_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_5", KMT_OBJECTS, ":center_slot"),
			(try_end),
		(else_try),
			(assign, ":slot_best_type",  kmt3_val_right_best_fief_type),
			# (assign, ":slot_best_count", kmt3_val_right_best_fief_count),
			## Get offered center in option #1 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_1_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_1", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #2 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_2_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_2", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #3 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_3_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_3", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #4 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_4_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_4", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #5 (left)
			(try_begin),
				(assign, ":base_slot", kmt3_val_left_opt_5_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":accept_5", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #1 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_1_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_1", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #2 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_2_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_2", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #3 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_3_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_3", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #4 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_4_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_4", KMT_OBJECTS, ":center_slot"),
			(try_end),
			## Get offered center in option #5 (right)
			(try_begin),
				(assign, ":base_slot", kmt3_val_right_opt_5_type),
				(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
				(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
				(store_add, ":slot_no", ":base_slot", ":offset"),
				(troop_get_slot, ":center_slot", KMT_OBJECTS, ":slot_no"),
				(troop_get_slot, ":block_5", KMT_OBJECTS, ":center_slot"),
			(try_end),
		(try_end),
		(troop_get_slot, ":best_type", KMT_OBJECTS, ":slot_best_type"),
		# (troop_get_slot, ":best_count", KMT_OBJECTS, ":slot_best_count"),
		
		### DIAGNOSTIC+ ###
		# (assign, reg31, ":best_count"),
		# (try_begin),
			# (eq, ":best_type", spt_town),
			# (str_store_string, s31, "@TOWN"),
		# (else_try),
			# (eq, ":best_type", spt_castle),
			# (str_store_string, s31, "@CASTLE"),
		# (else_try),
			# (eq, ":best_type", spt_village),
			# (str_store_string, s31, "@VILLAGE"),
		# (else_try),
			# (str_store_string, s31, "@LANDLESS"),
		# (try_end),
		# (str_store_troop_name, s32, ":troop_no"),
		# (display_message, "@DEBUG: {s32}'s best type is a {s31} of which he has {reg31}.", gpu_debug),
		### DIAGNOSTIC- ###
		
		(assign, ":count", 0),
		(assign, ":center_is_upgrade", 0),
		(troop_get_slot, ":troop_spouse", ":troop_no", slot_troop_spouse),
		(try_for_range, ":center_no", centers_begin, centers_end),
			(try_begin),
				(this_or_next|eq, ":center_no", ":accept_1"),
				(this_or_next|eq, ":center_no", ":accept_2"),
				(this_or_next|eq, ":center_no", ":accept_3"),
				(this_or_next|eq, ":center_no", ":accept_4"),
				(             eq, ":center_no", ":accept_5"),
				(try_begin),
					(eq, ":best_type", spt_village),
					(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_castle),
					(party_slot_eq, ":center_no", slot_party_type, spt_town),
					(assign, ":center_is_upgrade", 1),
				(else_try),
					(eq, ":best_type", spt_castle),
					(party_slot_eq, ":center_no", slot_party_type, spt_town),
					(assign, ":center_is_upgrade", 1),
				(try_end),
			(try_end),
			(party_slot_eq, ":center_no", slot_party_type, ":best_type"),
			# You own the fief or are married to the person who does OR it is being offered to you.
			(this_or_next|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
			(this_or_next|party_slot_eq, ":center_no", slot_town_lord, ":troop_spouse"),
			(this_or_next|eq, ":center_no", ":accept_1"),
			(this_or_next|eq, ":center_no", ":accept_2"),
			(this_or_next|eq, ":center_no", ":accept_3"),
			(this_or_next|eq, ":center_no", ":accept_4"),
			(             eq, ":center_no", ":accept_5"),
			# It isn't on the block list.
			(neq, ":center_no", ":block_1"),
			(neq, ":center_no", ":block_2"),
			(neq, ":center_no", ":block_3"),
			(neq, ":center_no", ":block_4"),
			(neq, ":center_no", ":block_5"),
			# It passes, let's count it.
			(val_add, ":count", 1),
			### DIAGNOSTIC+ ###
			# (assign, reg31, ":count"),
			# (str_store_party_name, s31, ":center_no"),
			# (str_store_troop_name, s32, ":troop_no"),
			# (display_message, "@DEBUG: {s32} will have {s31} after the trade.  Count = {reg31}.", gpu_debug),
			### DIAGNOSTIC- ###
			
		(try_end),
		
		(lt, ":count", 1), # Some number of the best type are retained after the trade.
		(eq, ":center_is_upgrade", 0),
	]),
	
# script_kmt_process_all_trade_offers
# PURPOSE: This handles the actual switching of lands and cash based on offered trades.  Same functionality used for regular trades and forced ones.
# EXAMPLE: (call_script, "script_kmt_process_all_trade_offers"), # kmt_scripts.py
("kmt_process_all_trade_offers",
	[
		# (troop_get_slot, ":troop_left",  KMT_OBJECTS, kmt3_val_lord_left),
		# (troop_get_slot, ":troop_right", KMT_OBJECTS, kmt3_val_lord_right),
		
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_left_opt_1_type),
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_left_opt_2_type),
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_left_opt_3_type),
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_left_opt_4_type),
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_left_opt_5_type),
		
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_right_opt_1_type),
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_right_opt_2_type),
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_right_opt_3_type),
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_right_opt_4_type),
		(call_script, "script_kmt_process_specific_trade_offer", kmt3_val_right_opt_5_type),
		
		(start_presentation, "prsnt_kmt_fief_exchange"),
	]),
	
	
# script_kmt_process_specific_trade_offer
# PURPOSE: This handles the actual switching of lands and cash based on an offered trade.  Same functionality used for regular trades and forced ones.
# EXAMPLE: (call_script, "script_kmt_process_specific_trade_offer", ":base_slot"), # kmt_scripts.py
("kmt_process_specific_trade_offer",
	[
		(store_script_param, ":base_slot", 1),
		
		## Determine side
		(try_begin),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_1_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_2_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_3_type),
			(this_or_next|eq, ":base_slot", kmt3_val_left_opt_4_type),
			(             eq, ":base_slot", kmt3_val_left_opt_5_type),
			(troop_get_slot, ":troop_giver", KMT_OBJECTS, kmt3_val_lord_left),
			(troop_get_slot, ":troop_receiver", KMT_OBJECTS, kmt3_val_lord_right),
		(else_try),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_1_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_2_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_3_type),
			(this_or_next|eq, ":base_slot", kmt3_val_right_opt_4_type),
			(             eq, ":base_slot", kmt3_val_right_opt_5_type),
			(troop_get_slot, ":troop_receiver", KMT_OBJECTS, kmt3_val_lord_left),
			(troop_get_slot, ":troop_giver", KMT_OBJECTS, kmt3_val_lord_right),
		(try_end),
		
		(try_begin), # PROCESS: MONEY
			(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_MONEY),
			# Get amount offered.
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
			(store_add, ":slot_value", ":base_slot", ":offset"),
			(troop_get_slot, ":offer", KMT_OBJECTS, ":slot_value"),
			(set_show_messages, 0),
			# Remove money from the GIVER.
			(try_begin),
				(eq, ":troop_giver", "trp_player"),
				(troop_remove_gold, "trp_player", ":offer"),
				(play_sound, "snd_money_received"),
			(else_try),
				(neq, ":troop_giver", "trp_player"),
				(troop_get_slot, ":cash", ":troop_giver", slot_troop_wealth),
				(val_sub, ":cash", ":offer"),
				(troop_set_slot, ":troop_giver", slot_troop_wealth, ":cash"),
			(try_end),
			# Add money to the RECEIVER.
			(try_begin),
				(eq, ":troop_receiver", "trp_player"),
				(troop_add_gold, "trp_player", ":offer"),
				(play_sound, "snd_money_received"),
			(else_try),
				(neq, ":troop_receiver", "trp_player"),
				(troop_get_slot, ":cash", ":troop_receiver", slot_troop_wealth),
				(val_add, ":cash", ":offer"),
				(troop_set_slot, ":troop_receiver", slot_troop_wealth, ":cash"),
			(try_end),
			(set_show_messages, 1),
			(str_store_troop_name, s21, ":troop_giver"),
			(str_store_troop_name, s22, ":troop_receiver"),
			(assign, reg21, ":offer"),
			(store_sub, reg22, reg21, 1),
			(display_message, "@{s21} has paid {reg21} denar{reg22?s:} to {s22}.", gpu_green),
			
		(else_try), # PROCESS: ROYAL COFFERS
			(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_KINGS_MONEY),
			# Get amount offered.
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
			(store_add, ":slot_value", ":base_slot", ":offset"),
			(troop_get_slot, ":offer", KMT_OBJECTS, ":slot_value"),
			(set_show_messages, 0),
			# Remove money from the GIVER.
			(troop_remove_gold, "trp_player", ":offer"),
			# Add money to the RECEIVER.
			(troop_get_slot, ":cash", ":troop_receiver", slot_troop_wealth),
			(val_add, ":cash", ":offer"),
			(troop_set_slot, ":troop_receiver", slot_troop_wealth, ":cash"),
			(set_show_messages, 1),
			(str_store_troop_name, s21, ":troop_giver"),
			(str_store_troop_name, s22, ":troop_receiver"),
			(assign, reg21, ":offer"),
			(store_sub, reg22, reg21, 1),
			(display_message, "@{s21} has paid {reg21} denar{reg22?s:} to {s22}.", gpu_green),
			
		(else_try),  # PROCESS: LANDS
			(troop_slot_eq, KMT_OBJECTS, ":base_slot", KMT_OPTION_FIEF),
			# Get amount offered.
			(store_sub, ":offset", kmt3_val_left_opt_1, kmt3_val_left_opt_1_type),
			(store_add, ":slot_value", ":base_slot", ":offset"),
			(troop_get_slot, ":slot_center", KMT_OBJECTS, ":slot_value"),
			(troop_get_slot, ":center_no", KMT_OBJECTS, ":slot_center"),
			(assign, "$block_relation_gain", 1),
			(call_script, "script_give_center_to_lord", ":center_no", ":troop_receiver", 0),
			(assign, "$block_relation_gain", 0),
			# Check if titles need to be updated for each troop.
			(store_troop_faction, ":faction_giver", ":troop_giver"),
			(store_troop_faction, ":faction_receiver", ":troop_receiver"),
			(call_script, "script_kmt_set_custom_noble_title_for_troop", ":troop_giver", ":faction_giver", KMT_TITLE_FUNCTION_SET),
			(call_script, "script_kmt_set_custom_noble_title_for_troop", ":troop_receiver", ":faction_receiver", KMT_TITLE_FUNCTION_SET),
			# Display transaction to the player.
			(str_store_troop_name, s21, ":troop_giver"),
			(str_store_troop_name, s22, ":troop_receiver"),
			(str_store_party_name, s23, ":center_no"),
			(display_message, "@{s21} has transfered control of {s23} to {s22}.", gpu_green),
			
		(try_end),
		
		## WIPE OUT OFFER INFORMATION.
		(store_add, ":base_upper", ":base_slot", 10),
		(try_for_range, ":slot_no", ":base_slot", ":base_upper"),
			(troop_set_slot, KMT_OBJECTS, ":slot_no", 0),
		(try_end),
	]),
	
# script_kmt_get_relation_penalty_for_offer
# PURPOSE: This gets the relation change that would occur based on the rating difference given.
# EXAMPLE: (call_script, "script_kmt_get_relation_penalty_for_offer", ":receiver_slot"), # kmt_scripts.py
("kmt_get_relation_penalty_for_offer",
	[
		(store_script_param, ":receiver_slot", 1),
		
		(try_begin),
			(eq, ":receiver_slot", kmt3_val_left_rating),
			(troop_get_slot, ":rating_receiver", KMT_OBJECTS, kmt3_val_left_rating),
			(troop_get_slot, ":rating_offerer", KMT_OBJECTS, kmt3_val_right_rating),
			(assign, ":penalty_slot", kmt3_val_left_label_forced_loss),
		(else_try),
			(eq, ":receiver_slot", kmt3_val_right_rating),
			(troop_get_slot, ":rating_offerer", KMT_OBJECTS, kmt3_val_left_rating),
			(troop_get_slot, ":rating_receiver", KMT_OBJECTS, kmt3_val_right_rating),
			(assign, ":penalty_slot", kmt3_val_right_label_forced_loss),
		(else_try),
			(assign, reg31, ":receiver_slot"),
			(display_message, "@ERROR - An invalid rating slot was given to script 'kmt_get_relation_penalty_for_offer' (Slot #{reg31}).", gpu_red),
		(try_end),
		
		(try_begin),
			(store_sub, ":delta", ":rating_offerer", ":rating_receiver"),
			(assign, ":change", 0),
			(assign, ":counter", 0),
			(assign, ":shift", 0),
			(assign, ":variance", 250),
			(assign, ":value_check", ":delta"),
			(val_abs, ":value_check"),
			(try_for_range, ":cycles", 0, 10), # 1 (250), 3 (500), 6 (1000), 10 (3000), 15 (9000), 21 (36k), 28 (144k), 36 (high), 45 (high), 50 (high)
				(eq, ":shift", 0),
				(store_div, ":half_cycle", ":cycles", 2),
				(store_mul, ":variance_addition", ":variance", ":half_cycle"),
				(val_add, ":variance", ":variance_addition"),
				(val_add, ":counter", 1),
				(val_add, ":change", ":counter"),
				(lt, ":value_check", ":variance"),
				(assign, ":shift", ":change"),
				(try_begin),
					(lt, ":delta", 0),
					(val_mul, ":shift", -1),
				(try_end),
			(try_end),
			(try_begin),
				(eq, ":delta", 0),
				(assign, ":shift", 0),
			(try_end),
			(val_clamp, ":shift", -50, 51),
			(troop_set_slot, KMT_OBJECTS, ":penalty_slot", ":shift"),
		(try_end),
	]),
	
	
# script_kmt_describe_relation_penalty_for_offer
# PURPOSE: This gets the display text for the resulting relation change that would occur based on a forced trade.
# EXAMPLE: (call_script, "script_kmt_describe_relation_penalty_for_offer", ":troop_slot"), # kmt_scripts.py
("kmt_describe_relation_penalty_for_offer",
	[
		(store_script_param, ":troop_slot", 1),
		
		(troop_get_slot, ":troop_no", KMT_OBJECTS, ":troop_slot"),
		
		(try_begin),
			(eq, ":troop_slot", kmt3_val_lord_left),
			(assign, ":slot_penalty", kmt3_val_left_label_forced_loss),
		(else_try),
			(eq, ":troop_slot", kmt3_val_lord_right),
			(assign, ":slot_penalty", kmt3_val_right_label_forced_loss),
		(else_try),
			(assign, reg31, ":troop_slot"),
			(assign, ":slot_penalty", 0),
			(display_message, "@ERROR - An invalid troop slot was given to script 'kmt_describe_relation_penalty_for_offer' (Slot #{reg31}).", gpu_red),
		(try_end),
		
		(troop_get_slot, reg21, KMT_OBJECTS, ":slot_penalty"),
		(str_store_troop_name, s22, ":troop_no"),
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(str_store_string, s21, "@ "),
		(else_try),
			(troop_slot_eq, KMT_OBJECTS, ":slot_penalty", 0),
			(str_store_string, s21, "@{s22} is indifferent to this arrangement."),
		(else_try),
			(troop_slot_ge, KMT_OBJECTS, ":slot_penalty", 1),
			(str_store_string, s21, "@{s22} will gain {reg21} relation if forced."),
		(else_try),
			(neg|troop_slot_ge, KMT_OBJECTS, ":slot_penalty", 0),
			(val_mul, reg21, -1),
			(str_store_string, s21, "@{s22} will lose {reg21} relation if forced."),
		(else_try),
			(str_store_string, s21, "@ERROR - Invalid Data"),
		(try_end),
	]),
	
	
###########################################################################################################################
#####                                                 VASSAL TITLES                                                   #####
###########################################################################################################################

# dict_create      = 3200 #(dict_create, <destination>), #Creates an empty dictionary object and stores it into <destination>
# dict_free        = 3201 #(dict_free, <dict>), #Frees the dictionary object <dict>. A dictionary can't be used after freeing it
# dict_load_file   = 3202 #(dict_load_file, <dict>, <file>, [<mode>]), #Loads a dictionary file into <dict>. Setting [<mode>] to 0 (default) clears <dict> and then loads the file, setting [<mode>] to 1 doesn't clear <dict> but overrides any key that's already present, [<mode>] to 2 doesn't clear <dict> and doesn't overwrite keys that are already present
# dict_load_dict   = 3203 #(dict_load_dict, <dict_1>, <dict_2>, [<mode>]), #Loads <dict_2> into <dict_1>. [<mode>]: see above
# dict_save        = 3204 #(dict_save, <dict>, <file>), #Saves <dict> into a file. For security reasons, <file> is just a name, not a full path, and will be stored into a WSE managed directory
# dict_clear       = 3205 #(dict_clear, <dict>), #Clears all key-value pairs from <dict>
# dict_is_empty    = 3206 #(dict_is_empty, <dict>), #Fails if <dict> is not empty
# dict_has_key     = 3207 #(dict_has_key, <dict>, <key>), #Fails if <key> is not present in <dict>
# dict_get_size    = 3208 #(dict_get_size, <destination>, <dict>), #Stores the count of key-value pairs in <dict> into <destination>
# dict_delete_file = 3209 #(dict_delete_file, <file>), #Deletes dictionary file <file> from disk
# dict_get_str     = 3210 #(dict_get_str, <string_register>, <dict>, <key>, [<default>]), #Stores the string value paired to <key> into <string_register>. If the key is not found and [<default>] is set, [<default>] will be stored instead. If [<default>] is not set, an empty string will be stored
# dict_get_int     = 3211 #(dict_get_int, <destination>, <dict>, <key>, [<default>]), #Stores the numeric value paired to <key> into <destination>. If the key is not found and [<default>] is set, [<default>] will be stored instead. If [<default>] is not set, 0 will be stored
# dict_set_str     = 3212 #(dict_set_str, <dict>, <key>, <string_no>), #Adds (or changes) <string_no> as the string value paired to <key>
# dict_set_int     = 3213 #(dict_set_int, <dict>, <key>, <value>), #Adds (or changes) <value> as the numeric value paired to <key>

# script_kmt_save_default_titles
# PURPOSE: Sets each title textbox to the default version for that faction.  This is only useful within prsnt_vassal_titles.
# EXAMPLE: (call_script, "script_kmt_save_default_titles"), # kmt_scripts.py
("kmt_save_default_titles",
	[
		## CREATE DICTIONARY FOR STORAGE
		(dict_create, ":dict_titles"),
		
		###################################
		###      KINGDOM OF SWADIA      ###
		###################################
		
		(str_store_faction_name, s22, "fac_kingdom_1"),
		
		## Landless
		(str_store_string, s21, "@{s22}_lord_landless"),
		(dict_set_str, ":dict_titles", s21, "@Sir"),
		(str_store_string, s21, "@{s22}_lady_landless"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Villages
		(str_store_string, s21, "@{s22}_lord_villages"),
		(dict_set_str, ":dict_titles", s21, "@Baron"),
		(str_store_string, s21, "@{s22}_lady_villages"),
		(dict_set_str, ":dict_titles", s21, "@Baroness"),
		
		## Castles
		(str_store_string, s21, "@{s22}_lord_castles"),
		(dict_set_str, ":dict_titles", s21, "@Count"),
		(str_store_string, s21, "@{s22}_lady_castles"),
		(dict_set_str, ":dict_titles", s21, "@Countess"),
		
		## Towns
		(str_store_string, s21, "@{s22}_lord_towns"),
		(dict_set_str, ":dict_titles", s21, "@Duke"),
		(str_store_string, s21, "@{s22}_lady_towns"),
		(dict_set_str, ":dict_titles", s21, "@Duchess"),
		
		## Marshal
		(str_store_string, s21, "@{s22}_lord_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Archduke"),
		(str_store_string, s21, "@{s22}_lady_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Duchess"),
		
		## Rulers
		(str_store_string, s21, "@{s22}_lord_ruler"),
		(dict_set_str, ":dict_titles", s21, "@King"),
		(str_store_string, s21, "@{s22}_lady_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Queen"),
		
		## Royal Children
		(str_store_string, s21, "@{s22}_lord_prince"),
		(dict_set_str, ":dict_titles", s21, "@Prince"),
		(str_store_string, s21, "@{s22}_lady_princess"),
		(dict_set_str, ":dict_titles", s21, "@Princess"),
		
		
		####################################
		###      KINGDOM OF VAEGIRS      ###
		####################################
		
		(str_store_faction_name, s22, "fac_kingdom_2"),
		
		## Landless
		(str_store_string, s21, "@{s22}_lord_landless"),
		(dict_set_str, ":dict_titles", s21, "@Sir"),
		(str_store_string, s21, "@{s22}_lady_landless"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Villages
		(str_store_string, s21, "@{s22}_lord_villages"),
		(dict_set_str, ":dict_titles", s21, "@Boyar"),
		(str_store_string, s21, "@{s22}_lady_villages"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Castles
		(str_store_string, s21, "@{s22}_lord_castles"),
		(dict_set_str, ":dict_titles", s21, "@Boyar"),
		(str_store_string, s21, "@{s22}_lady_castles"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Towns
		(str_store_string, s21, "@{s22}_lord_towns"),
		(dict_set_str, ":dict_titles", s21, "@Knyaz"),
		(str_store_string, s21, "@{s22}_lady_towns"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Marshal
		(str_store_string, s21, "@{s22}_lord_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Lord Marshal"),
		(str_store_string, s21, "@{s22}_lady_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Lady Marshal"),
		
		## Rulers
		(str_store_string, s21, "@{s22}_lord_ruler"),
		(dict_set_str, ":dict_titles", s21, "@King"),
		(str_store_string, s21, "@{s22}_lady_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Queen"),
		
		## Royal Children
		(str_store_string, s21, "@{s22}_lord_prince"),
		(dict_set_str, ":dict_titles", s21, "@Prince"),
		(str_store_string, s21, "@{s22}_lady_princess"),
		(dict_set_str, ":dict_titles", s21, "@Princess"),
		
		
		#####################################
		###      KINGDOM OF KHERGITS      ###
		#####################################
		
		(str_store_faction_name, s22, "fac_kingdom_3"),
		
		## Landless
		(str_store_string, s21, "@{s22}_lord_landless"),
		(dict_set_str, ":dict_titles", s21, "@Sir"),
		(str_store_string, s21, "@{s22}_lady_landless"),
		(dict_set_str, ":dict_titles", s21, "@Behi"),
		
		## Villages
		(str_store_string, s21, "@{s22}_lord_villages"),
		(dict_set_str, ":dict_titles", s21, "@Noyan"),
		(str_store_string, s21, "@{s22}_lady_villages"),
		(dict_set_str, ":dict_titles", s21, "@Behi"),
		
		## Castles
		(str_store_string, s21, "@{s22}_lord_castles"),
		(dict_set_str, ":dict_titles", s21, "@Noyan"),
		(str_store_string, s21, "@{s22}_lady_castles"),
		(dict_set_str, ":dict_titles", s21, "@Behi"),
		
		## Towns
		(str_store_string, s21, "@{s22}_lord_towns"),
		(dict_set_str, ":dict_titles", s21, "@Khan"),
		(str_store_string, s21, "@{s22}_lady_towns"),
		(dict_set_str, ":dict_titles", s21, "@Khatun"),
		
		## Marshal
		(str_store_string, s21, "@{s22}_lord_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Khan"),
		(str_store_string, s21, "@{s22}_lady_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Khatun"),
		
		## Rulers
		(str_store_string, s21, "@{s22}_lord_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Khagan"),
		(str_store_string, s21, "@{s22}_lady_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Khatun"),
		
		## Royal Children
		(str_store_string, s21, "@{s22}_lord_prince"),
		(dict_set_str, ":dict_titles", s21, "@Mirza"),
		(str_store_string, s21, "@{s22}_lady_princess"),
		(dict_set_str, ":dict_titles", s21, "@Gonji"),
		
		
		##################################
		###      KINGDOM OF NORDS      ###
		##################################
		
		(str_store_faction_name, s22, "fac_kingdom_4"),
		
		## Landless
		(str_store_string, s21, "@{s22}_lord_landless"),
		(dict_set_str, ":dict_titles", s21, "@Thegn"),
		(str_store_string, s21, "@{s22}_lady_landless"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Villages
		(str_store_string, s21, "@{s22}_lord_villages"),
		(dict_set_str, ":dict_titles", s21, "@Jarl"),
		(str_store_string, s21, "@{s22}_lady_villages"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Castles
		(str_store_string, s21, "@{s22}_lord_castles"),
		(dict_set_str, ":dict_titles", s21, "@Jarl"),
		(str_store_string, s21, "@{s22}_lady_castles"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Towns
		(str_store_string, s21, "@{s22}_lord_towns"),
		(dict_set_str, ":dict_titles", s21, "@Duke"),
		(str_store_string, s21, "@{s22}_lady_towns"),
		(dict_set_str, ":dict_titles", s21, "@Duchess"),
		
		## Marshal
		(str_store_string, s21, "@{s22}_lord_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Lord Marshal"),
		(str_store_string, s21, "@{s22}_lady_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Lady Marshal"),
		
		## Rulers
		(str_store_string, s21, "@{s22}_lord_ruler"),
		(dict_set_str, ":dict_titles", s21, "@King"),
		(str_store_string, s21, "@{s22}_lady_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Queen"),
		
		## Royal Children
		(str_store_string, s21, "@{s22}_lord_prince"),
		(dict_set_str, ":dict_titles", s21, "@Prince"),
		(str_store_string, s21, "@{s22}_lady_princess"),
		(dict_set_str, ":dict_titles", s21, "@Princess"),
		
		####################################
		###      KINGDOM OF RHODOKS      ###
		####################################
		
		(str_store_faction_name, s22, "fac_kingdom_5"),
		
		## Landless
		(str_store_string, s21, "@{s22}_lord_landless"),
		(dict_set_str, ":dict_titles", s21, "@Sir"),
		(str_store_string, s21, "@{s22}_lady_landless"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Villages
		(str_store_string, s21, "@{s22}_lord_villages"),
		(dict_set_str, ":dict_titles", s21, "@Baron"),
		(str_store_string, s21, "@{s22}_lady_villages"),
		(dict_set_str, ":dict_titles", s21, "@Baroness"),
		
		## Castles
		(str_store_string, s21, "@{s22}_lord_castles"),
		(dict_set_str, ":dict_titles", s21, "@Count"),
		(str_store_string, s21, "@{s22}_lady_castles"),
		(dict_set_str, ":dict_titles", s21, "@Countess"),
		
		## Towns
		(str_store_string, s21, "@{s22}_lord_towns"),
		(dict_set_str, ":dict_titles", s21, "@Duke"),
		(str_store_string, s21, "@{s22}_lady_towns"),
		(dict_set_str, ":dict_titles", s21, "@Duchess"),
		
		## Marshal
		(str_store_string, s21, "@{s22}_lord_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Archduke"),
		(str_store_string, s21, "@{s22}_lady_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Duchess"),
		
		## Rulers
		(str_store_string, s21, "@{s22}_lord_ruler"),
		(dict_set_str, ":dict_titles", s21, "@King"),
		(str_store_string, s21, "@{s22}_lady_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Queen"),
		
		## Royal Children
		(str_store_string, s21, "@{s22}_lord_prince"),
		(dict_set_str, ":dict_titles", s21, "@Prince"),
		(str_store_string, s21, "@{s22}_lady_princess"),
		(dict_set_str, ":dict_titles", s21, "@Princess"),
		
		
		######################################
		###      KINGDOM OF SARRANIDS      ###
		######################################
		
		(str_store_faction_name, s22, "fac_kingdom_6"),
		
		## Landless
		(str_store_string, s21, "@{s22}_lord_landless"),
		(dict_set_str, ":dict_titles", s21, "@Sir"),
		(str_store_string, s21, "@{s22}_lady_landless"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Villages
		(str_store_string, s21, "@{s22}_lord_villages"),
		(dict_set_str, ":dict_titles", s21, "@Lord"),
		(str_store_string, s21, "@{s22}_lady_villages"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Castles
		(str_store_string, s21, "@{s22}_lord_castles"),
		(dict_set_str, ":dict_titles", s21, "@Lord"),
		(str_store_string, s21, "@{s22}_lady_castles"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Towns
		(str_store_string, s21, "@{s22}_lord_towns"),
		(dict_set_str, ":dict_titles", s21, "@Lord"),
		(str_store_string, s21, "@{s22}_lady_towns"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Marshal
		(str_store_string, s21, "@{s22}_lord_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Emir"),
		(str_store_string, s21, "@{s22}_lady_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Emira"),
		
		## Rulers
		(str_store_string, s21, "@{s22}_lord_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Sultan"),
		(str_store_string, s21, "@{s22}_lady_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Sultana"),
		
		## Royal Children
		(str_store_string, s21, "@{s22}_lord_prince"),
		(dict_set_str, ":dict_titles", s21, "@Mirza"),
		(str_store_string, s21, "@{s22}_lady_princess"),
		(dict_set_str, ":dict_titles", s21, "@Gonji"),
		
		
		#######################################
		###      PLAYER CUSTOM FACTION      ###
		#######################################
		
		(str_store_string, s22, "@Player Faction"),
		
		## Landless
		(str_store_string, s21, "@{s22}_lord_landless"),
		(dict_set_str, ":dict_titles", s21, "@Sir"),
		(str_store_string, s21, "@{s22}_lady_landless"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Villages
		(str_store_string, s21, "@{s22}_lord_villages"),
		(dict_set_str, ":dict_titles", s21, "@Lord"),
		(str_store_string, s21, "@{s22}_lady_villages"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Castles
		(str_store_string, s21, "@{s22}_lord_castles"),
		(dict_set_str, ":dict_titles", s21, "@Lord"),
		(str_store_string, s21, "@{s22}_lady_castles"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Towns
		(str_store_string, s21, "@{s22}_lord_towns"),
		(dict_set_str, ":dict_titles", s21, "@Lord"),
		(str_store_string, s21, "@{s22}_lady_towns"),
		(dict_set_str, ":dict_titles", s21, "@Lady"),
		
		## Marshal
		(str_store_string, s21, "@{s22}_lord_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Lord Marshal"),
		(str_store_string, s21, "@{s22}_lady_marshal"),
		(dict_set_str, ":dict_titles", s21, "@Lady Marshal"),
		
		## Rulers
		(str_store_string, s21, "@{s22}_lord_ruler"),
		(dict_set_str, ":dict_titles", s21, "@King"),
		(str_store_string, s21, "@{s22}_lady_ruler"),
		(dict_set_str, ":dict_titles", s21, "@Queen"),
		
		## Royal Children
		(str_store_string, s21, "@{s22}_lord_prince"),
		(dict_set_str, ":dict_titles", s21, "@Prince"),
		(str_store_string, s21, "@{s22}_lady_princess"),
		(dict_set_str, ":dict_titles", s21, "@Princess"),
		
		## SAVE TO DEFAULTS FILE
		(dict_save, ":dict_titles", "@Silverstag Default Titles"),
		
		## SET TITLE STYLE DEFAULTS FOR FACTIONS
		(faction_set_slot, "fac_kingdom_1", slot_faction_title_style_default, 0),
		(faction_set_slot, "fac_kingdom_2", slot_faction_title_style_default, 0),
		(faction_set_slot, "fac_kingdom_3", slot_faction_title_style_default, 1),
		(faction_set_slot, "fac_kingdom_4", slot_faction_title_style_default, 0),
		(faction_set_slot, "fac_kingdom_5", slot_faction_title_style_default, 0),
		(faction_set_slot, "fac_kingdom_6", slot_faction_title_style_default, 0),
		(faction_set_slot, "fac_player_supporters_faction", slot_faction_title_style_default, 0),
		
	]),
	
# script_kmt_load_default_titles_for_faction
# PURPOSE: Sets each title textbox to the default version for that faction.  This is only useful within prsnt_vassal_titles.
# EXAMPLE: (call_script, "script_kmt_load_default_titles_for_faction"), # kmt_scripts.py
("kmt_load_default_titles_for_faction",
	[
		(store_script_param, ":faction_no", 1),
		
		## Save our defaults incase they need resetting.
		(call_script, "script_kmt_save_default_titles"), # kmt_scripts.py
		(dict_create, ":dict_titles"),
		(dict_load_file, ":dict_titles", "@Silverstag Default Titles", 0),
		
		## Setup Faction Key
		(str_store_faction_name, s22, ":faction_no"),
		(try_begin),
			(eq, ":faction_no", "fac_player_supporters_faction"),
			(str_store_string, s22, "@Player Faction"),
		(try_end),
		
		## Landless
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_landless"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Sir"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_landless_lords),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_landless"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_landless_ladies),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Villages
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_villages"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lord"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_village_lords),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_villages"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_village_ladies),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Castles
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_castles"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lord"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_castle_lords),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_castles"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_castle_ladies),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Towns
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_towns"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lord"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_town_lords),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_towns"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_town_ladies),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Marshal
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_marshal"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lord Marshal"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_marshal),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_marshal"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady Marshal"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_marshal_lady),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Rulers
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_ruler"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@King"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_king),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_ruler"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Queen"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_queen),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Royal Children
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_prince"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Prince"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_prince),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_princess"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Princess"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_princess),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## SET TITLE STYLE
		(try_begin),
			(faction_get_slot, ":setting", ":faction_no", slot_faction_title_style_default),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_menu_title_style),
			(overlay_set_val, ":obj_no", ":setting"),
			(troop_set_slot, KMT_OBJECTS, kmt5_val_menu_title_style, ":setting"),
		(try_end),
	]),

# script_kmt_save_titles_for_faction
# PURPOSE: Sets each title textbox to the default version for that faction.  This is only useful within prsnt_vassal_titles.
# EXAMPLE: (call_script, "script_kmt_save_titles_for_faction", ":faction_no"), # kmt_scripts.py
("kmt_save_titles_for_faction",
	[
		(store_script_param, ":faction_no", 1),
		
		## CREATE DICTIONARY & LOAD FILE - All factions loaded here to make sure we don't overwrite undisplayed factions.
		(dict_create, ":dict_titles"),
		(dict_clear, ":dict_titles"),
		(dict_load_file, ":dict_titles", "@Silverstag Default Titles", 0),
		(dict_load_file, ":dict_titles", "@Silverstag Vassal Titles", 1),
		
		(str_store_faction_name, s22, ":faction_no"),
		(try_begin),
			(eq, ":faction_no", "fac_player_supporters_faction"),
			(str_store_string, s22, "@Player Faction"),
		(try_end),
		
		## Landless - Lord
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_landless_lords),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lord_landless"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Landless - Lady
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_landless_ladies),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lady_landless"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Villages - Lord
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_village_lords),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lord_villages"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Villages - Lady
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_village_ladies),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lady_villages"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Castles - Lord
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_castle_lords),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lord_castles"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Castles - Lady
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_castle_ladies),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lady_castles"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Towns - Lord
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_town_lords),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lord_towns"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Towns - Lady
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_town_ladies),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lady_towns"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Marshal - Lord
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_marshal),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lord_marshal"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Marshal - Lady
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_marshal_lady),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lady_marshal"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Ruler - Lord
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_king),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lord_ruler"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Ruler - Lady
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_queen),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lady_ruler"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Prince - Lord
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_prince),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lord_prince"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## Princess - Lady
		(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_princess),
		(str_store_overlay_text, s21, ":obj_no"), # Data to store
		(str_store_string, s23, "@{s22}_lady_princess"), # Key
		(dict_set_str, ":dict_titles", s23, s21),
		
		## SAVE TO FILE
		(dict_save, ":dict_titles", "@Silverstag Vassal Titles"),
		
		## SAVE TITLE STYLE
		(try_begin),
			(troop_get_slot, ":setting", KMT_OBJECTS, kmt5_val_menu_title_style),
			(faction_set_slot, ":faction_no", slot_faction_title_style, ":setting"),
		(try_end),
		
		## UPDATE ALL LORDS OF THIS FACTION
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":faction_id", ":troop_no"),
			(eq, ":faction_id", ":faction_no"),
			(call_script, "script_kmt_set_custom_noble_title_for_troop", ":troop_no", ":faction_no", KMT_TITLE_FUNCTION_SET),
		(try_end),
		
		## UPDATE ALL LADIES OF THIS FACTION
		(try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
			# (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
			(store_troop_faction, ":faction_id", ":troop_no"),
			(eq, ":faction_id", ":faction_no"),
			(call_script, "script_kmt_set_custom_noble_title_for_troop", ":troop_no", ":faction_no", KMT_TITLE_FUNCTION_SET),
		(try_end),
	]),


# kmt5_obj_textbox_landless_lords    = 100
# kmt5_obj_textbox_village_lords     = 101
# kmt5_obj_textbox_castle_lords      = 102
# kmt5_obj_textbox_town_lords        = 103
# kmt5_obj_textbox_marshal           = 104
# kmt5_obj_textbox_king              = 105
# kmt5_obj_textbox_landless_ladies   = 106
# kmt5_obj_textbox_village_ladies    = 107
# kmt5_obj_textbox_castle_ladies     = 108
# kmt5_obj_textbox_town_ladies       = 109
# kmt5_obj_textbox_marshal_lady      = 110
# kmt5_obj_textbox_queen             = 111

# script_kmt_load_titles_for_faction
# PURPOSE: Sets each title textbox to the default version for that faction.  This is only useful within prsnt_vassal_titles.
# EXAMPLE: (call_script, "script_kmt_load_titles_for_faction", ":faction_no"), # kmt_scripts.py
("kmt_load_titles_for_faction",
	[
		(store_script_param, ":faction_no", 1),
		
		## CREATE DICTIONARY & LOAD FILE
		(dict_create, ":dict_titles"),
		(dict_clear, ":dict_titles"),
		(dict_load_file, ":dict_titles", "@Silverstag Default Titles", 0),
		(dict_load_file, ":dict_titles", "@Silverstag Vassal Titles", 1),
		
		## Setup Faction Key
		(str_store_faction_name, s22, ":faction_no"),
		(try_begin),
			(eq, ":faction_no", "fac_player_supporters_faction"),
			(str_store_string, s22, "@Player Faction"),
		(try_end),
		
		## Landless
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_landless"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Sir"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_landless_lords),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_landless"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_landless_ladies),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Villages
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_villages"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lord"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_village_lords),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_villages"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_village_ladies),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Castles
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_castles"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lord"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_castle_lords),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_castles"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_castle_ladies),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Towns
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_towns"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lord"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_town_lords),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_towns"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_town_ladies),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Marshal
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_marshal"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lord Marshal"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_marshal),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_marshal"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Lady Marshal"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_marshal_lady),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Rulers
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_ruler"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@King"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_king),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_ruler"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Queen"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_queen),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## Royal Children
		(try_begin),
			(str_store_string, s21, "@{s22}_lord_prince"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Prince"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_prince),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		(try_begin),
			(str_store_string, s21, "@{s22}_lady_princess"),
			(dict_has_key, ":dict_titles", s21),
			(dict_get_str, s23, ":dict_titles", s21, "@Princess"),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_textbox_princess),
			(overlay_set_text, ":obj_no", s23),
		(try_end),
		
		## SET TITLE STYLE
		(try_begin),
			(faction_get_slot, ":setting", ":faction_no", slot_faction_title_style),
			(troop_get_slot, ":obj_no", KMT_OBJECTS, kmt5_obj_menu_title_style),
			(overlay_set_val, ":obj_no", ":setting"),
			(troop_set_slot, KMT_OBJECTS, kmt5_val_menu_title_style, ":setting"),
		(try_end),
	]),
	
# script_kmt_set_custom_noble_title_for_troop
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate this code for each window.
# EXAMPLE: (call_script, "script_kmt_set_custom_noble_title_for_troop", ":troop_no", ":faction_no", ":function"),
("kmt_set_custom_noble_title_for_troop",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":faction_no", 2),
		(store_script_param, ":function", 3),
		
		## CREATE DICTIONARY & LOAD FILE
		(dict_create, ":dict_titles"),
		(dict_clear, ":dict_titles"),
		(dict_load_file, ":dict_titles", "@Silverstag Default Titles", 0),
		(dict_load_file, ":dict_titles", "@Silverstag Vassal Titles", 1),
		
		(str_store_troop_name, s1, ":troop_no"),
		
		(str_clear, s4),
		(assign, ":title_type", 0),	
		(try_begin),
			(this_or_next|is_between, ":troop_no", active_npcs_begin, active_npcs_end),
			(this_or_next|is_between, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
			(eq, ":troop_no", "trp_player"),
			
			## DETERMINE FACTION
			(try_begin),
				(neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
				(store_troop_faction, ":faction_no", ":troop_no"),
			(try_end),
			(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(str_store_faction_name, s2, ":faction_no"),
			(try_begin),
				(eq, ":faction_no", "fac_player_supporters_faction"),
				(str_store_string, s2, "@Player Faction"),
			(try_end),
			
			## DETERMINE LEVEL OF NOBILITY
			# Get relative data.
			(troop_get_type, ":gender", ":troop_no"),
			(troop_get_slot, ":troop_spouse", ":troop_no", slot_troop_spouse),
			(troop_get_slot, ":troop_father", ":troop_no", slot_troop_father), # Only important for royal children.
			(troop_get_slot, ":troop_mother", ":troop_no", slot_troop_mother), # Only important for royal children.
			(troop_get_slot, ":troop_guardian", ":troop_no", slot_troop_guardian), # Only important for royal children.
			# Check for owned lands.
			(assign, ":highest_fief_type", -1), # Populate with spt_village, spt_castle, spt_town as appropriate.
			(try_for_range, ":center_no", centers_begin, centers_end),
				(this_or_next|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
				(party_slot_eq, ":center_no", slot_town_lord, ":troop_spouse"),
				(neg|party_slot_eq, ":center_no", slot_town_lord, -1), # Needs to be assigned to someone.
				(try_begin),
					(eq, ":highest_fief_type", -1), # None found.
					(party_get_slot, ":highest_fief_type", ":center_no", slot_party_type),
				(else_try),
					(eq, ":highest_fief_type", spt_village),
					(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_castle),
					(party_slot_eq, ":center_no", slot_party_type, spt_town),
					(party_get_slot, ":highest_fief_type", ":center_no", slot_party_type),
				(else_try),
					(eq, ":highest_fief_type", spt_castle),
					(party_slot_eq, ":center_no", slot_party_type, spt_town),
					(party_get_slot, ":highest_fief_type", ":center_no", slot_party_type),
				(try_end),
			(try_end),
			
			# Check for royal family.
			(try_begin), # King / Queen
				(this_or_next|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
				(faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_spouse"),
				(assign, ":title_type", 1),
				(try_begin), # Gender Split
					(eq, ":gender", tf_male),
					(str_store_string, s3, "@{s2}_lord_ruler"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@King"),
				(else_try),
					(eq, ":gender", tf_female),
					(str_store_string, s3, "@{s2}_lady_ruler"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Queen"),
				(try_end),
				
			(else_try), # Prince / Princess
				(this_or_next|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_father"),
				(this_or_next|faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_guardian"),
				(faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_mother"),
				(assign, ":title_type", 2),
				(try_begin), # Gender Split
					(eq, ":gender", tf_male),
					(str_store_string, s3, "@{s2}_lord_prince"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Prince"),
				(else_try),
					(eq, ":gender", tf_female),
					(str_store_string, s3, "@{s2}_lady_princess"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Princess"),
				(try_end),
				
			(else_try), # Town Owners
				(eq, ":highest_fief_type", spt_town),
				(assign, ":title_type", 3),
				(try_begin), # Gender Split
					(eq, ":gender", tf_male),
					(str_store_string, s3, "@{s2}_lord_towns"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Lord"),
				(else_try),
					(eq, ":gender", tf_female),
					(str_store_string, s3, "@{s2}_lady_towns"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Lady"),
				(try_end),
				
			(else_try), # Castle Owners
				(eq, ":highest_fief_type", spt_castle),
				(assign, ":title_type", 4),
				(try_begin), # Gender Split
					(eq, ":gender", tf_male),
					(str_store_string, s3, "@{s2}_lord_castles"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Lord"),
				(else_try),
					(eq, ":gender", tf_female),
					(str_store_string, s3, "@{s2}_lady_castles"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Lady"),
				(try_end),
				
			(else_try), # Village Owners
				(eq, ":highest_fief_type", spt_village),
				(assign, ":title_type", 5),
				(try_begin), # Gender Split
					(eq, ":gender", tf_male),
					(str_store_string, s3, "@{s2}_lord_villages"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Lord"),
				(else_try),
					(eq, ":gender", tf_female),
					(str_store_string, s3, "@{s2}_lady_villages"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Lady"),
				(try_end),
				
			(else_try), # Landless
				(assign, ":title_type", 6),
				(try_begin), # Gender Split
					(eq, ":gender", tf_male),
					(str_store_string, s3, "@{s2}_lord_landless"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Sir"),
				(else_try),
					(eq, ":gender", tf_female),
					(str_store_string, s3, "@{s2}_lady_landless"),
					(dict_has_key, ":dict_titles", s3),
					(dict_get_str, s4, ":dict_titles", s3, "@Lady"),
				(try_end),
				
			(else_try), # Error Trap
				(assign, ":title_type", 0),				
			(try_end),
			(neq, ":title_type", 0),
			(str_store_troop_name_plural, s0, ":troop_no"),
			(eq, ":function", KMT_TITLE_FUNCTION_SET),
			(try_begin),
				(faction_slot_eq, ":faction_no", slot_faction_title_style, 1), # Title After Name
				(str_store_string, s1, "@{s0} {s4}"),
			(else_try),
				(str_store_string, s1, "@{s4} {s0}"), # Title Before Name
			(try_end),
			(troop_set_name, ":troop_no", s1),
			(troop_get_slot, ":troop_party", ":troop_no", slot_troop_leaded_party),
			(gt, ":troop_party", 0),
			(str_store_troop_name, s5, ":troop_no"),
			(party_set_name, ":troop_party", "str_s5_s_party"),
		(try_end),
	]),
	
# script_kmt_initialize_custom_titles
# PURPOSE: Names every lord based on their custom titles.
# EXAMPLE: (call_script, "script_kmt_initialize_custom_titles"), # kmt_scripts.py
("kmt_initialize_custom_titles",
	[
		(call_script, "script_kmt_save_default_titles"), # kmt_scripts.py   (Initializes our default nobility titles)
		
		## UPDATE ALL LORDS OF THIS FACTION
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(store_troop_faction, ":faction_no", ":troop_no"),
			(call_script, "script_kmt_set_custom_noble_title_for_troop", ":troop_no", ":faction_no", KMT_TITLE_FUNCTION_SET),
		(try_end),
		
		## UPDATE ALL LADIES OF THIS FACTION
		(try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
			# (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),
			(store_troop_faction, ":faction_no", ":troop_no"),
			(call_script, "script_kmt_set_custom_noble_title_for_troop", ":troop_no", ":faction_no", KMT_TITLE_FUNCTION_SET),
		(try_end),
	]),
	
	
###########################################################################################################################
#####                                             AFFAIRS OF THE REALM                                                #####
###########################################################################################################################

# script_kmt_create_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate this code for each window.
("kmt_create_mode_switching_buttons",
    [
		### COMMON ELEMENTS ###
		(assign, "$gpu_storage", KMT_OBJECTS),
		(assign, "$gpu_data",    KMT_OBJECTS),
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		# Setup an initial false value for objects so if they don't get loaded they aren't 0's.
		(try_for_range, ":slot_no", 0, 50),
			(store_add, ":value", ":slot_no", 1234),
			(troop_set_slot, KMT_OBJECTS, ":slot_no", ":value"),
		(try_end),
		
		## CONTAINERS ##
		(call_script, "script_gpu_container_heading", 50, 80, 175, 505, kmt1_obj_container_1),
			
			## BUTTONS ##
			(assign, ":x_buttons", 0), # 90 
			(assign, ":y_button_step", 55),
			(assign, ":pos_y", 420),
			
			(str_store_string, s21, "@General Info "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", kmt1_obj_button_general_info), ### GENERAL INFO ###
			
			# (val_sub, ":pos_y", ":y_button_step"),
			# (str_store_string, s21, "@Fief Elections "),
			# (call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", kmt1_obj_button_fief_election), ### FIEF ELECTIONS ###
			
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@Fief Exchange "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", kmt1_obj_button_fief_exchange), ### FIEF EXCHANGE ###
			
			# (val_sub, ":pos_y", ":y_button_step"),
			# (str_store_string, s21, "@Vassal Gifts "),
			# (call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", kmt1_obj_button_vassal_gifts), ### VASSAL GIFTS ###
			
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@Vassal Titles "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", kmt1_obj_button_vassal_titles), ### VASSAL TITLES ###
			
			# (val_sub, ":pos_y", ":y_button_step"),
			# (str_store_string, s21, "@Noble Prisoners "),
			# (call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", kmt1_obj_button_vassal_prisoners), ### NOBLE PRISONERS ###
			
		(set_container_overlay, -1),
		(call_script, "script_gpu_create_mesh", "mesh_button_up", 55, 35, 350, 500),
		(str_store_string, s21, "@Done"),
		(call_script, "script_gpu_create_button", "str_hub_s21", 65, 40, kmt1_obj_button_done),
	]),
	
# script_kmt_handle_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate the code to handle their functionality for each window.
("kmt_handle_mode_switching_buttons",
    [
		(store_script_param, ":object", 1),
		(store_script_param, ":value", 2),
		(assign, reg1, ":value"), # So it won't be whined about.
		
		### COMMON ELEMENTS ###
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, KMT_OBJECTS, kmt1_obj_button_done, ":object"),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(assign, "$kmt_mode", KMT_STARTING_SCREEN),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : GENERAL INFO #######
			(troop_slot_eq, KMT_OBJECTS, kmt1_obj_button_general_info, ":object"),
			(assign, "$kmt_mode", KMT_MODE_GENERAL_INFO),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_kmt_switch_modes"),
			
		(else_try), ####### BUTTON : FIEF ELECTIONS #######
			(troop_slot_eq, KMT_OBJECTS, kmt1_obj_button_fief_election, ":object"),
			(assign, "$kmt_mode", KMT_MODE_FIEF_ELECTIONS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_kmt_switch_modes"),
			
		(else_try), ####### BUTTON : FIEF EXCHANGE #######
			(troop_slot_eq, KMT_OBJECTS, kmt1_obj_button_fief_exchange, ":object"),
			(assign, "$kmt_mode", KMT_MODE_FIEF_EXCHANGE),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_kmt_switch_modes"),
			
		(else_try), ####### BUTTON : VASSAL GIFTS #######
			(troop_slot_eq, KMT_OBJECTS, kmt1_obj_button_vassal_gifts, ":object"),
			(assign, "$kmt_mode", KMT_MODE_VASSAL_GIFTS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_kmt_switch_modes"),
			
		(else_try), ####### BUTTON : VASSAL TITLES #######
			(troop_slot_eq, KMT_OBJECTS, kmt1_obj_button_vassal_titles, ":object"),
			(assign, "$kmt_mode", KMT_MODE_VASSAL_TITLES),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_kmt_switch_modes"),
			
		(else_try), ####### BUTTON : VASSAL PRISONERS #######
			(troop_slot_eq, KMT_OBJECTS, kmt1_obj_button_vassal_prisoners, ":object"),
			(assign, "$kmt_mode", KMT_MODE_VASSAL_PRISONERS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_kmt_switch_modes"),
			
		(try_end),
	]),
	
]


from util_wrappers import *
from util_scripts import *

                
def modmerge_scripts(orig_scripts):
	# process script directives first
	# process_script_directives(orig_scripts, scripts_directives)
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