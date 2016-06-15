# Beta Testing Suite (WIP) by Windyplains
# Released --/--/--

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
#####                                          KINGDOM MANAGEMENT SYSTEM                                              #####
###########################################################################################################################
("diplomacy_kingdom_management", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
		(set_fixed_point_multiplier, 1000),
		## WINDYPLAINS+ ## - Faded background.
		# (call_script, "script_gpu_create_mesh", "mesh_marble_background", 0, 0, 1000, 1300),
		## WINDYPLAINS- ##
        
		(assign, "$gpu_storage", KMS_OBJECTS),
		(assign, "$gpu_data",    KMS_OBJECTS),
		(assign, ":font_size", 75),
		
		# Button Definitions
		
		
		(call_script, "script_gpu_create_game_button", "str_kms_label_summary", 500, 30, kms_obj_button_summary),
		
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 1),
			(call_script, "script_gpu_create_game_button", "str_kms_restore", 125, 30, kms_obj_button_restore),
			# (call_script, "script_gpu_create_game_button", "str_kms_label_help", 312, 30, kms_obj_button_help),
			(call_script, "script_gpu_create_game_button", "str_kms_cancel", 693, 30, kms_obj_button_cancel),
			(call_script, "script_gpu_create_game_button", "str_kms_accept", 885, 30, kms_obj_button_accept),
		(else_try),
			# (call_script, "script_gpu_create_game_button", "str_kms_label_help", 125, 30, kms_obj_button_help),
			(call_script, "script_gpu_create_game_button", "str_kms_leave", 885, 30, kms_obj_button_cancel),
		(try_end),
		
		# (call_script, "script_gpu_draw_line", 852, 40, 73, 650, gpu_brown), # Brown background
		# (call_script, "script_gpu_draw_line", 852, 2, 73, 690, gpu_black), # - Header
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		# (call_script, "script_gpu_draw_line", 2, 40, 73, 650, gpu_black), # | Left border
		# (call_script, "script_gpu_draw_line", 2, 40, 923, 650, gpu_black), # | Right border
		
		# Text Labels
		(str_store_faction_name, s21, "$players_kingdom"),
		(call_script, "script_gpu_create_text_label", "str_kms_label_player_faction", 500, 665, kms_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kms_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_kms_label_player_faction", 500, 665, kms_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", kms_obj_main_title, 150),
		(try_begin),
			(call_script, "script_cf_qus_player_is_king", 0),
			(call_script, "script_gpu_create_text_label", "str_kms_label_warning_non_king", 500, 635, kms_obj_label_non_king_warning, gpu_center), # 680
			(call_script, "script_gpu_resize_object", kms_obj_label_non_king_warning, 75),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_kms_label_warning_non_king", 500, 635, kms_obj_label_non_king_warning, gpu_center), # 680
			(call_script, "script_gpu_resize_object", kms_obj_label_non_king_warning, 75),
		(try_end),
		(call_script, "script_gpu_create_text_label", "str_kms_label_policies", 162, 600, 0, gpu_center),  # Domestic Policies
		(overlay_set_color, reg1, gpu_blue),
		(call_script, "script_gpu_create_text_label", "str_kms_label_decrees", 837, 600, 0, gpu_center),  # Royal Decrees
		(overlay_set_color, reg1, gpu_blue),
		
		### POLICY CONTAINER ###
		#(call_script, "script_gpu_container_heading", 25, 100, 325, 525, kms_obj_policy_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			(assign, ":pos_y", 545),
			(assign, ":pos_x", 160),
			(assign, ":slider_step", 85),
			(call_script, "script_diplomacy_create_policy_slider", ":pos_x", ":pos_y", kms_obj_slider_policy_focus, "str_kms_sfp_focus_label", "str_kms_sfp_focus_left_2"),
			(val_sub, ":pos_y", ":slider_step"),
			(call_script, "script_diplomacy_create_policy_slider", ":pos_x", ":pos_y", kms_obj_slider_policy_diversity, "str_kms_sfp_diversity_label", "str_kms_sfp_diversity_left_2"),
			(val_sub, ":pos_y", ":slider_step"),
			(call_script, "script_diplomacy_create_policy_slider", ":pos_x", ":pos_y", kms_obj_slider_policy_borders, "str_kms_sfp_borders_label", "str_kms_sfp_borders_left_2"),
			(val_sub, ":pos_y", ":slider_step"),
			(call_script, "script_diplomacy_create_policy_slider", ":pos_x", ":pos_y", kms_obj_slider_policy_slavery, "str_kms_sfp_slavery_label", "str_kms_sfp_slavery_left_2"),
			(val_sub, ":pos_y", ":slider_step"),
			(call_script, "script_diplomacy_create_policy_slider", ":pos_x", ":pos_y", kms_obj_slider_policy_desertion, "str_kms_sfp_desertion_label", "str_kms_sfp_desertion_left_2"),
			
			(troop_get_slot, reg20, KMS_OBJECTS, kms_obj_slider_policy_focus),
			(troop_get_slot, reg21, KMS_OBJECTS, kms_val_policy_culture_focus),
			(overlay_set_val, reg20, reg21),
			# (display_message, "@Policy 'Cultural Focus' [OBJ: {reg20}] should now be set to {reg21}."),
			
			(troop_get_slot, reg20, KMS_OBJECTS, kms_obj_slider_policy_diversity),
			(troop_get_slot, reg21, KMS_OBJECTS, kms_val_policy_mil_diversity),
			(overlay_set_val, reg20, reg21),
			# (display_message, "@Policy 'Military Diversity' [OBJ: {reg20}] should now be set to {reg21}."),
			
			(troop_get_slot, reg20, KMS_OBJECTS, kms_obj_slider_policy_borders),
			(troop_get_slot, reg21, KMS_OBJECTS, kms_val_policy_border_control),
			(overlay_set_val, reg20, reg21),
			# (display_message, "@Policy 'Border Control' [OBJ: {reg20}] should now be set to {reg21}."),
			
			(troop_get_slot, reg20, KMS_OBJECTS, kms_obj_slider_policy_slavery),
			(troop_get_slot, reg21, KMS_OBJECTS, kms_val_policy_slavery),
			(overlay_set_val, reg20, reg21),
			# (display_message, "@Policy 'Slavery' [OBJ: {reg20}] should now be set to {reg21}."),
			
			(troop_get_slot, reg20, KMS_OBJECTS, kms_obj_slider_policy_desertion),
			(troop_get_slot, reg21, KMS_OBJECTS, kms_val_policy_desertion),
			(overlay_set_val, reg20, reg21),
			# (display_message, "@Policy 'Troop Desertion' [OBJ: {reg20}] should now be set to {reg21}."),
			
			
		################ CONTAINER END ################	
		#(set_container_overlay, -1),
		
		### DECREES ###
		(assign, ":pos_y", 535),
		(assign, ":pos_x", 740),
		# script_gpu_create_checkbox     - pos_x, pos_y, label, storage_slot, value_slot
		(try_for_range, ":decree_slot", kms_val_decrees_begin, kms_val_decrees_end),
			(store_sub, ":offset", ":decree_slot", kms_val_decrees_begin),
			# Determine the title of the checkbox.
			(store_add, ":string_no", ":offset", "str_kms_sfd_conscription_label"),
			# Determine the storage slot for the checkbox object #.
			(store_add, ":checkbox_obj", ":offset", kms_obj_decrees_begin),
			(store_add, ":label_obj", ":offset", kms_obj_label_begin),
			# Build the checkbox.
			# text
			(store_add, ":text_pos_x", ":pos_x", 20), (position_set_x, pos1, ":text_pos_x"),
			(store_add, ":text_pos_y", ":pos_y", 13),  (position_set_y, pos1, ":text_pos_y"),
			(create_text_overlay, reg1, ":string_no", tf_left_align|tf_vertical_align_center),
			(overlay_set_position, reg1, pos1),
			(troop_set_slot, "$gpu_storage", ":label_obj", reg1),
			(call_script, "script_gpu_resize_object", ":label_obj", 85),
			# checkbox
			(store_add, ":checkbox_pos_x", ":pos_x", 0), (position_set_x, pos1, ":checkbox_pos_x"),
			(store_add, ":checkbox_pos_y", ":pos_y", 5), (position_set_y, pos1, ":checkbox_pos_y"),
			(create_check_box_overlay, reg1, "mesh_checkbox_off", "mesh_checkbox_on"),
			(overlay_set_position, reg1, pos1),
			(troop_set_slot, "$gpu_storage", ":checkbox_obj", reg1),
			(troop_get_slot, ":setting", "$gpu_data", ":decree_slot"),
			(overlay_set_val, reg1, ":setting"),
			(call_script, "script_gpu_resize_object", ":checkbox_obj", 85),
			
			# Move down further on the list.
			(val_sub, ":pos_y", 30),
		(try_end),
		
		### TOOLTIP WINDOW ###
		(call_script, "script_gpu_create_text_label", "str_kms_summary_label", 500, 600, kms_obj_title_tooltip, gpu_center),
		(overlay_set_color, reg1, gpu_blue),
		
		(call_script, "script_gpu_container_heading", 300, 440, 400, 130, kms_obj_primary_tooltip_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			(call_script, "script_gpu_create_text_label", "str_kms_blank", 0, 100, 0, gpu_left),
			(call_script, "script_gpu_create_text_label", "str_kms_label_decrees", 0, 10, kms_obj_primary_tooltip, gpu_left),
			(call_script, "script_gpu_resize_object", kms_obj_primary_tooltip, ":font_size"),
		################ CONTAINER END ################	
		(set_container_overlay, -1),
		
		(call_script, "script_gpu_container_heading", 300, 100, 400, 320, kms_obj_secondary_tooltip_container), # Scrolling container
		############### CONTAINER BEGIN ###############
			(call_script, "script_gpu_create_text_label", "str_kms_blank", 0, 680, 0, gpu_left), # 635
			(call_script, "script_gpu_create_text_label", "str_kms_blank", 0, 10, kms_obj_secondary_tooltip, gpu_left),
			(call_script, "script_gpu_resize_object", kms_obj_secondary_tooltip, ":font_size"),
		################ CONTAINER END ################	
		(set_container_overlay, -1),
		(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
      ]),
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(try_begin), ####### CANCEL BUTTON #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_button_cancel, ":object"),
			# End the presentation.
			(presentation_set_duration, 0),
			
		# (else_try), ####### INFORMATION BUTTON #######
			# (troop_slot_eq, KMS_OBJECTS, kms_obj_button_help, ":object"),
			# (assign, "$return_presentation", "prsnt_diplomacy_kingdom_management"),
			# (start_presentation, "prsnt_diplomacy_guide"),
			
		(else_try), ####### SUMMARY TOOLTIP #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_button_summary, ":object"),
			# Reset default data for faction.
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
			
		(try_end),
		
		# Warn player that they can't make changes unless they're a king.
		# (try_begin),
			# (neg|troop_slot_eq, KMS_OBJECTS, kms_obj_button_cancel, ":object"),
			# ## TODO: Add information button exclusion here.
			# (display_message, "@You may not make any alterations to policies for a kingdom until you are a king."),
		# (try_end),
		
		## CONDITIONAL BREAK ##
		(call_script, "script_cf_qus_player_is_king", 1), # Player must be a king to make any changes.
		
		(try_begin), ####### ACCEPT CHOOSER #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_button_accept, ":object"),
			# Save data to faction slots.
			(troop_get_slot, ":faction_no", KMS_OBJECTS, kms_val_faction_no),
			(call_script, "script_diplomacy_sync_faction_data", ":faction_no", STORE_TO_FACTION),
			# End the presentation.
			(presentation_set_duration, 0),
			
		(else_try), ####### RESTORE DEFAULTS #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_button_restore, ":object"),
			# Reset default data for faction.
			(troop_get_slot, ":faction_no", KMS_OBJECTS, kms_val_faction_no),
			(call_script, "script_diplomacy_reset_policy_defaults", ":faction_no"),
			# Save new data to presentation slots.
			(call_script, "script_diplomacy_sync_faction_data", ":faction_no", STORE_TO_PRESENTATION),
			# End the presentation.
			(start_presentation, "prsnt_diplomacy_kingdom_management"),
			
		(else_try), ####### DECREE: CONSCRIPTION #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_decree_conscription, ":object"),
			(troop_set_slot, KMS_OBJECTS, kms_val_decree_conscription, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
			
		(else_try), ####### DECREE: CODE OF LAW (COMMON) #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_decree_laws_commons, ":object"),
			(troop_set_slot, KMS_OBJECTS, kms_val_decree_laws_commons, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
			
		(else_try), ####### DECREE: CODE OF LAW (NOBILITY) #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_decree_laws_nobles, ":object"),
			(troop_set_slot, KMS_OBJECTS, kms_val_decree_laws_nobles, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
			
		(else_try), ####### DECREE: WAR TAXATION #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_decree_war_taxes, ":object"),
			(troop_set_slot, KMS_OBJECTS, kms_val_decree_war_taxes, ":value"),
			# Disable "Period of Reconstruction" if currently enabled.
			(try_begin),
				(troop_slot_eq, KMS_OBJECTS, kms_val_decree_reconstruction, 1),
				(troop_set_slot, KMS_OBJECTS, kms_val_decree_reconstruction, 0),
				(display_message, "@Your royal decree of 'Period of Reconstruction' has been rescinded.", gpu_red),
				## Set oppositng decree to disabled.
				(troop_get_slot, ":obj_checkbox", KMS_OBJECTS, kms_obj_decree_reconstruction),
				(overlay_set_val, ":obj_checkbox", 0),
			(try_end),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
			
		(else_try), ####### DECREE: SANITATION STANDARDS #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_decree_sanitation, ":object"),
			(troop_set_slot, KMS_OBJECTS, kms_val_decree_sanitation, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
			
		(else_try), ####### DECREE: PUBLIC EXECUTIONS #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_decree_executions, ":object"),
			(troop_set_slot, KMS_OBJECTS, kms_val_decree_executions, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
			
		(else_try), ####### DECREE: PERIOD OF RECONSTRUCTION #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_decree_reconstruction, ":object"),
			(troop_set_slot, KMS_OBJECTS, kms_val_decree_reconstruction, ":value"),
			# Disable "War Taxation" if currently enabled.
			(try_begin),
				(troop_slot_eq, KMS_OBJECTS, kms_val_decree_war_taxes, 1),
				(troop_set_slot, KMS_OBJECTS, kms_val_decree_war_taxes, 0),
				(display_message, "@Your royal decree of 'War Taxation' has been rescinded.", gpu_red),
				## Set oppositng decree to disabled.
				(troop_get_slot, ":obj_checkbox", KMS_OBJECTS, kms_obj_decree_war_taxes),
				(overlay_set_val, ":obj_checkbox", 0),
			(try_end),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DIPLOMACY_SUMMARY),
			
		(else_try), ####### POLICY: CULTURAL FOCUS #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_focus, ":object"),
			(neg|troop_slot_eq, KMS_OBJECTS, kms_val_policy_culture_focus, ":value"), # Prevent spamming this script.
			(troop_set_slot, KMS_OBJECTS, kms_val_policy_culture_focus, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_CULTURAL_FOCUS),
			
		(else_try), ####### POLICY: MILITARY DIVERSITY #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_diversity, ":object"),
			(neg|troop_slot_eq, KMS_OBJECTS, kms_val_policy_mil_diversity, ":value"), # Prevent spamming this script.
			(troop_set_slot, KMS_OBJECTS, kms_val_policy_mil_diversity, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_MILITARY_DIVERSITY),
			
		(else_try), ####### POLICY: BORDER CONTROL #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_borders, ":object"),
			(neg|troop_slot_eq, KMS_OBJECTS, kms_val_policy_border_control, ":value"), # Prevent spamming this script.
			(troop_set_slot, KMS_OBJECTS, kms_val_policy_border_control, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_BORDER_CONTROLS),
			
		(else_try), ####### POLICY: SLAVERY #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_slavery, ":object"),
			(neg|troop_slot_eq, KMS_OBJECTS, kms_val_policy_slavery, ":value"), # Prevent spamming this script.
			(troop_set_slot, KMS_OBJECTS, kms_val_policy_slavery, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_SLAVERY),
			
		(else_try), ####### POLICY: TROOP DESERTION #######
			(troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_desertion, ":object"),
			(neg|troop_slot_eq, KMS_OBJECTS, kms_val_policy_desertion, ":value"), # Prevent spamming this script.
			(troop_set_slot, KMS_OBJECTS, kms_val_policy_desertion, ":value"),
			(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_TROOP_DESERTION),
			
		(try_end),
      ]),
	  
	(ti_on_presentation_mouse_enter_leave,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":state"),
		
		# States: 0 (enters), 1 (leaves)
		(mouse_get_position, pos2),
		(position_get_x, ":mouse_x", pos2),
		(assign, ":policy_edge", 300),
		
		(try_begin),
			(eq, ":state", 0),
			
			(try_begin), ####### DECREE: CONSCRIPTION #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_decree_conscription, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_conscription, ":object"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DECREE_CONSCRIPTION),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
				
			(else_try), ####### DECREE: CODE OF LAW (COMMON) #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_decree_laws_commons, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_laws_commons, ":object"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DECREE_CODE_OF_LAW_COMMON),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
				
			(else_try), ####### DECREE: CODE OF LAW (NOBILITY) #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_decree_laws_nobles, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_laws_nobles, ":object"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DECREE_CODE_OF_LAW_NOBLE),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
				
			(else_try), ####### DECREE: WAR TAXATION #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_decree_war_taxes, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_war_taxes, ":object"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DECREE_WAR_TAXATION),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
				
			(else_try), ####### DECREE: SANITATION STANDARDS #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_decree_sanitation, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_sanitation, ":object"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DECREE_SANITATION),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
				
			(else_try), ####### DECREE: PUBLIC EXECUTIONS #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_decree_executions, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_executions, ":object"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DECREE_PUBLIC_EXECUTIONS),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
				
			(else_try), ####### DECREE: PERIOD OF RECONSTRUCTION #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_decree_reconstruction, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_reconstruction, ":object"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_DECREE_RECONSTRUCTION),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
				
			(else_try), ####### POLICY: CULTURAL FOCUS #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_focus, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_policy_focus, ":object"),
				(lt, ":mouse_x", ":policy_edge"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_CULTURAL_FOCUS),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
				
			(else_try), ####### POLICY: MILITARY DIVERSITY #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_diversity, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_policy_diversity, ":object"),
				(lt, ":mouse_x", ":policy_edge"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_MILITARY_DIVERSITY),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
			
			(else_try), ####### POLICY: BORDER CONTROL #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_borders, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_policy_borders, ":object"),
				(lt, ":mouse_x", ":policy_edge"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_BORDER_CONTROLS),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
			
			(else_try), ####### POLICY: SLAVERY #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_slavery, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_policy_slavery, ":object"),
				(lt, ":mouse_x", ":policy_edge"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_SLAVERY),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
			
			(else_try), ####### POLICY: TROOP DESERTION #######
				(this_or_next|troop_slot_eq, KMS_OBJECTS, kms_obj_slider_policy_desertion, ":object"),
				(troop_slot_eq, KMS_OBJECTS, kms_obj_label_policy_desertion, ":object"),
				(lt, ":mouse_x", ":policy_edge"),
				(call_script, "script_diplomacy_create_tooltip", TOOLTIP_POLICY_TROOP_DESERTION),
				(call_script, "script_diplomacy_calculate_policy_data_values", TOOLTIP_DIPLOMACY_SUMMARY),
			
			(try_end),

		(try_end),
      ]),
	  
    ]),

##############################################################################
####               TOURNAMENT CREDITS & INFORMATION PANEL                 ####
##############################################################################
# This preference panel will set what kinds of equipment the player wishes allowed in each city's specific tournaments.
  ("diplomacy_guide", 0, mesh_load_window, [
    (ti_on_presentation_load,
    [
		(set_fixed_point_multiplier, 1000),
		(assign, "$gpu_storage", GPU_OBJECTS),
		(assign, "$gpu_data",    GPU_OBJECTS),
		
		# Background Mesh
		# (call_script, "script_gpu_create_mesh", "mesh_marble_background", 0, 0, 1000, 1300),
		# (create_mesh_overlay, reg1, "mesh_tournament_design_panel"),
        # (position_set_x, pos1, 0),
        # (position_set_y, pos1, 0),
        # (overlay_set_position, reg1, pos1),
		
		# Margins
		(assign, ":x_col_label_titles",     20), # Left aligned.
		(assign, ":y_line_step",            25), # Spacing between lines of text.
		(store_sub, ":x_col_bold_titles", ":x_col_label_titles", 5), # Left aligned.
		
		# Button Definitions
		(call_script, "script_gpu_create_game_button", "str_kms_exit",        895, 15, guide_obj_button_exit),
		(try_begin),
			(neg|troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 0), # Not the Main Topics Mode
			(call_script, "script_gpu_create_game_button", "str_kms_main_topics", 730, 15, guide_obj_button_main_topics),
		(try_end),
		
		# Create header display
		(call_script, "script_gpu_create_text_label", "str_kms_main_title", 20, 680, 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 150),
		(call_script, "script_gpu_create_text_label", "str_kms_main_title", 20, 680, 0, gpu_left),
		# (call_script, "script_gpu_create_text_label", "str_kms_main_title", 15, 680, 0, gpu_left_with_outline),
		# (overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", 0, 150),
		(call_script, "script_gpu_create_text_label", "str_kms_sub_title", ":x_col_label_titles", 655, 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 80),
		# Dividing Lines
		(call_script, "script_gpu_draw_line", 970, 2, 15, 630, gpu_gray), # horizontal line sub title.
		
		### INFORMATION TOPICS ###
		(call_script, "script_gpu_container_heading", 0, 75, 960, 525, guide_obj_container_info),
			
			# Determine what kind of information to display here.
			(try_begin),
				(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 0), # Main Topics
				(assign, ":string_begin", "str_kms_info_0a"),
				(assign, ":string_end",   "str_kms_info_1a"),
			(else_try),
				(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 1), # Overview
				(assign, ":string_begin", "str_kms_info_1a"),
				(assign, ":string_end",   "str_kms_info_2a"),
			(else_try),
				(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 2), # Message Filtering
				(assign, ":string_begin", "str_kms_info_2a"),
				(assign, ":string_end",   "str_kms_info_3a"),
			(else_try),
				(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 3), # Policies & Decrees
				(assign, ":string_begin", "str_kms_info_3a"),
				(assign, ":string_end",   "str_kms_info_4a"),
			(else_try),
				(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 4), # Dialog Options
				(assign, ":string_begin", "str_kms_info_4a"),
				(assign, ":string_end",   "str_kms_info_5a"),
			(else_try),
				(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 5), # Morale System
				(assign, ":string_begin", "str_kms_info_5a"),
				(assign, ":string_end",   "str_kms_info_6a"),
			(else_try),
				(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 6), # Companion Advisors
				(assign, ":string_begin", "str_kms_info_6a"),
				(assign, ":string_end",   "str_kms_info_8a"),
			# (else_try),
				# (troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 7), # Lo
				# (assign, ":string_begin", "str_kms_info_7a"),
				# (assign, ":string_end",   "str_kms_info_8a"),
			(else_try),
				(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 7), # Credits
				(assign, ":string_begin", "str_kms_info_8a"),
				(assign, ":string_end",   "str_kms_info_9a"),
			(try_end),
			(assign, ":topic_count", 0),
			(store_sub, ":y_start", ":string_end", ":string_begin"),
			(val_mul, ":y_start", ":y_line_step"),
			(val_add, ":y_start", ":y_line_step"),
			(assign, ":pos_y", ":y_start"),
			
			(call_script, "script_gpu_create_text_label", "str_tpe_info_1b",  ":x_col_bold_titles",  ":pos_y", 0, gpu_left),
			
			(troop_get_slot, ":title_string", GPU_OBJECTS, guide_val_information_mode),
			(val_add, ":title_string", "str_kms_info_0"),
			(call_script, "script_gpu_create_text_label", ":title_string",  ":x_col_label_titles",  ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_create_text_label", ":title_string",  ":x_col_label_titles",  ":pos_y", 0, gpu_left),
			# (call_script, "script_gpu_create_text_label", ":title_string",  ":x_col_bold_titles",  ":pos_y", 0, gpu_left_with_outline),
			# (overlay_set_color, reg1, gpu_white),
			(val_sub, ":pos_y", 40),
			
			(try_for_range, ":topic_no", ":string_begin", ":string_end"),
				(store_add, ":obj_slot", guide_obj_topics_begin, ":topic_count"),
				(val_add, ":topic_count", 1),
				(try_begin),
					(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 0), # Main Topics
					(assign, reg5, ":topic_count"),
					(store_sub, ":pos_y_button", ":pos_y", 13),
					(store_add, ":pos_x_button", ":x_col_label_titles", 0),
					(call_script, "script_gpu_create_button", ":topic_no", ":pos_x_button", ":pos_y_button", ":obj_slot"),
					(position_set_x, pos1, 1250),
					(position_set_y, pos1, 1000),
					(overlay_set_size, reg1, pos1),
				(else_try),
					(call_script, "script_gpu_create_text_label",  ":topic_no", ":x_col_label_titles", ":pos_y", 0, gpu_left),
				(try_end),
				(val_sub, ":pos_y", ":y_line_step"),
			(try_end),
			(store_add, ":obj_slot", guide_obj_topics_begin, ":topic_count"),
			(troop_set_slot, GPU_OBJECTS, guide_obj_topics_end, ":obj_slot"),
		(set_container_overlay, -1),
		
		(presentation_set_duration, 999999),
    ]),
	
    (ti_on_presentation_event_state_change,
    [
        (store_trigger_param_1, ":object"),
		
		(assign, ":guide_no", "prsnt_diplomacy_guide"),
		
		(try_begin),
			##### DONE BUTTON #####
			(troop_slot_eq, GPU_OBJECTS, guide_obj_button_exit, ":object"),
			(presentation_set_duration, 0),
			(try_begin),
				## Return to Mod Options if applicable ##
				(eq, "$return_presentation", "prsnt_mod_option"),
				(jump_to_menu, "mnu_tpe_return_to_mod_options"),
			# (else_try),
				## Return to Kingdom Management presentation if applicable ##
				# (eq, "$return_presentation", "prsnt_diplomacy_kingdom_management"),
				# (jump_to_menu, "mnu_tpe_return_to_mod_options"),
			(try_end),
			
		(else_try),
			##### BACK BUTTON #####
			(troop_slot_eq, GPU_OBJECTS, guide_obj_button_main_topics, ":object"),
			(neg|troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 0), # Not the Main Topics Mode
			(troop_set_slot, GPU_OBJECTS, guide_val_information_mode, 0),
			(start_presentation, ":guide_no"),
			
		(else_try),
			##### ANY INFO TOPIC BUTTON #####
			(troop_slot_eq, GPU_OBJECTS, guide_val_information_mode, 0), # Main Topics
			(assign, ":pass", 0),
			(store_sub, ":end_slot", "str_kms_info_1a", "str_kms_info_0a"),
			(val_add, ":end_slot", guide_obj_topics_begin),
			(try_for_range, ":slot_no", guide_obj_topics_begin, ":end_slot"),
				(troop_slot_eq, GPU_OBJECTS, ":slot_no", ":object"),
				(assign, ":pass", ":slot_no"),
			(try_end),
			(ge, ":pass", 1),
			(store_sub, ":topic_no", ":pass", guide_obj_topics_begin),
			(val_add, ":topic_no", 1),
			(troop_set_slot, GPU_OBJECTS, guide_val_information_mode, ":topic_no"),
			(start_presentation, ":guide_no"),
			
		(try_end),
		
	]),
  ]),
  
("banner_background_fixing",0,mesh_load_window,[
    (ti_on_presentation_load,
		[
			(set_fixed_point_multiplier, 1000),
			(assign, "$gpu_storage", GPU_OBJECTS),
			(assign, "$gpu_data", GPU_OBJECTS),
			
			(call_script, "script_gpu_draw_line", 852, 40, 73, 650, gpu_brown), # Brown background
			(call_script, "script_gpu_draw_line", 852, 2, 73, 690, gpu_black), # - Header
			(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_black), # - Footer
			(call_script, "script_gpu_draw_line", 2, 40, 73, 650, gpu_black), # | Left border
			(call_script, "script_gpu_draw_line", 2, 40, 923, 650, gpu_black), # | Right border
			
			# Text Labels
			(str_store_string, s21, "@Banner Background Adjustment"),
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", 500, 665, gpu_obj_main_title, gpu_center_with_outline), # 680
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", gpu_obj_main_title, 150),
		
			(str_store_string, s21, "@Exit"),
			(call_script, "script_gpu_create_game_button", "str_gpu_s21", 500, 30, gpu_obj_button_exit),
			(str_store_string, s21, "@Get Background"),
			(call_script, "script_gpu_create_game_button", "str_gpu_s21", 625, 180, gpu_obj_button_get_color),
			(str_store_string, s21, "@Set Background"),
			(call_script, "script_gpu_create_game_button", "str_gpu_s21", 825, 180, gpu_obj_button_update_color),
			(str_store_string, s21, "@Next Banner"),
			(call_script, "script_gpu_create_game_button", "str_gpu_s21", 350, 275, gpu_obj_button_next_banner),
			(str_store_string, s21, "@Previous Banner"),
			(call_script, "script_gpu_create_game_button", "str_gpu_s21", 150, 275, gpu_obj_button_prev_banner),
			
			(troop_get_slot, reg21, GPU_OBJECTS, gpu_val_current_banner),
			(val_sub, reg21, banner_meshes_begin),
			(call_script, "script_gpu_create_text_label", "str_gpu_banner_number", 243, 575, gpu_obj_label_current_banner, gpu_center),
			
			(troop_get_slot, ":banner_mesh", GPU_OBJECTS, gpu_val_current_banner),
			(create_image_button_overlay, reg1, ":banner_mesh", ":banner_mesh"),
			(position_set_x, pos1, 175),
			(position_set_y, pos1, 550),
			(overlay_set_position, reg1, pos1),
			(position_set_x, pos1, 100),
			(position_set_y, pos1, 100),
			(overlay_set_size, reg1, pos1),
			(troop_set_slot, GPU_OBJECTS, gpu_obj_current_banner, reg1),
			
			#(create_mesh_overlay_with_tableau_material, <destination>, <mesh_id>, <tableau_material_id>, <value>),
			
			# script_gpu_draw_line           - x length, y length, pos_x, pos_y, color
			(troop_get_slot, ":color", GPU_OBJECTS, gpu_val_banner_background),
			(call_script, "script_gpu_draw_line", 100, 200, 250, 350, ":color"),
			(troop_set_slot, GPU_OBJECTS, gpu_obj_banner_background, reg1),
			
			# Create red slider
			(assign, ":pos_x", 600),
			(assign, ":pos_y", 500),
			(store_add, ":pos_x_right", ":pos_x", 250),
			(store_sub, ":pos_x_split", ":pos_x", 0),
			(store_sub, ":pos_y_slider", ":pos_y", 50),
			(call_script, "script_gpu_create_text_label", "str_kmt_title_red", ":pos_x", ":pos_y", gpu_obj_label_red_slider, gpu_left),
			(troop_get_slot, reg21, GPU_OBJECTS, gpu_val_slider_red),
			(call_script, "script_gpu_create_text_label", "str_gpu_r21", ":pos_x_right", ":pos_y", gpu_obj_desc_red_slider, gpu_right),
			(call_script, "script_gpu_create_slider", 0, 255, ":pos_x_split", ":pos_y_slider", gpu_obj_slider_red, gpu_val_slider_red),
			
			# Create green slider
			(assign, ":pos_x", 600),
			(assign, ":pos_y", 400),
			(store_add, ":pos_x_right", ":pos_x", 250),
			(store_sub, ":pos_x_split", ":pos_x", 0),
			(store_sub, ":pos_y_slider", ":pos_y", 50),
			(call_script, "script_gpu_create_text_label", "str_kmt_title_green", ":pos_x", ":pos_y", gpu_obj_label_green_slider, gpu_left),
			(troop_get_slot, reg21, GPU_OBJECTS, gpu_val_slider_green),
			(call_script, "script_gpu_create_text_label", "str_gpu_r21", ":pos_x_right", ":pos_y", gpu_obj_desc_green_slider, gpu_right),
			(call_script, "script_gpu_create_slider", 0, 255, ":pos_x_split", ":pos_y_slider", gpu_obj_slider_green, gpu_val_slider_green),
			
			# Create blue slider
			(assign, ":pos_x", 600),
			(assign, ":pos_y", 300),
			(store_add, ":pos_x_right", ":pos_x", 250),
			(store_sub, ":pos_x_split", ":pos_x", 0),
			(store_sub, ":pos_y_slider", ":pos_y", 50),
			(call_script, "script_gpu_create_text_label", "str_kmt_title_blue", ":pos_x", ":pos_y", gpu_obj_label_blue_slider, gpu_left),
			(troop_get_slot, reg21, GPU_OBJECTS, gpu_val_slider_blue),
			(call_script, "script_gpu_create_text_label", "str_gpu_r21", ":pos_x_right", ":pos_y", gpu_obj_desc_blue_slider, gpu_right),
			(call_script, "script_gpu_create_slider", 0, 255, ":pos_x_split", ":pos_y_slider", gpu_obj_slider_blue, gpu_val_slider_blue),
			
			(call_script, "script_gpu_create_text_label", "str_gpu_rgb", ":pos_x", 550, gpu_obj_label_rgb_text, gpu_left),
			(call_script, "script_gpu_rgb_to_decimal", 0),
			(call_script, "script_gpu_create_text_label", "str_gpu_r21", ":pos_x_right", 550, gpu_obj_label_rgb_value, gpu_right),
			
			(call_script, "script_gpu_rgb_to_decimal", 1),
			
			(presentation_set_duration, 999999),
		]),
    (ti_on_presentation_event_state_change,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":value"),
			
			(try_begin), ####### EXIT BUTTON #######
				(troop_slot_eq, GPU_OBJECTS, gpu_obj_button_exit, ":object"),
				# End the presentation.
				(presentation_set_duration, 0),
				
			(else_try), ####### GET BACKGROUND BUTTON #######
				(troop_slot_eq, GPU_OBJECTS, gpu_obj_button_get_color, ":object"),
				(troop_get_slot, ":banner_slot", GPU_OBJECTS, gpu_val_current_banner),
				(val_sub, ":banner_slot", banner_meshes_begin),
				(troop_get_slot, ":banner_color", "trp_banner_background_color_array", ":banner_slot"),
				(call_script, "script_gpu_decimal_to_rgb", 1, ":banner_color"),
				
			(else_try), ####### UPDATE MESH BUTTON #######
				(troop_slot_eq, GPU_OBJECTS, gpu_obj_button_update_color, ":object"),
				(troop_get_slot, ":banner_slot", GPU_OBJECTS, gpu_val_current_banner),
				(val_sub, ":banner_slot", banner_meshes_begin),
				(call_script, "script_gpu_rgb_to_decimal", 0),
				(troop_set_slot, "trp_banner_background_color_array", ":banner_slot", reg21),
				(start_presentation, "prsnt_banner_background_fixing"),
				
			(else_try), ####### NEXT BANNER BUTTON #######
				(troop_slot_eq, GPU_OBJECTS, gpu_obj_button_next_banner, ":object"),
				(troop_get_slot, reg1, GPU_OBJECTS, gpu_val_current_banner),
				(val_add, reg1, 1),
				(try_begin),
					(ge, reg1, banner_meshes_end_minus_one),
					(assign, reg1, banner_meshes_begin),
				(try_end),
				(troop_set_slot, GPU_OBJECTS, gpu_val_current_banner, reg1),
				(start_presentation, "prsnt_banner_background_fixing"),
				
			(else_try), ####### PREV BANNER BUTTON #######
				(troop_slot_eq, GPU_OBJECTS, gpu_obj_button_prev_banner, ":object"),
				(troop_get_slot, reg1, GPU_OBJECTS, gpu_val_current_banner),
				(val_sub, reg1, 1),
				(try_begin),
					(lt, reg1, banner_meshes_begin),
					(assign, reg1, banner_meshes_end_minus_one),
				(try_end),
				(troop_set_slot, GPU_OBJECTS, gpu_val_current_banner, reg1),
				(start_presentation, "prsnt_banner_background_fixing"),
				
			(else_try), ####### RED SLIDER #######
				(troop_slot_eq, GPU_OBJECTS, gpu_obj_slider_red, ":object"),
				(troop_set_slot, GPU_OBJECTS, gpu_val_slider_red, ":value"),
				(troop_get_slot, ":obj_label", GPU_OBJECTS, gpu_obj_desc_red_slider),
				(assign, reg21, ":value"),
				(overlay_set_text, ":obj_label", "str_gpu_r21"),
				(call_script, "script_gpu_rgb_to_decimal", 1),
				
			(else_try), ####### GREEN SLIDER #######
				(troop_slot_eq, GPU_OBJECTS, gpu_obj_slider_green, ":object"),
				(troop_set_slot, GPU_OBJECTS, gpu_val_slider_green, ":value"),
				(troop_get_slot, ":obj_label", GPU_OBJECTS, gpu_obj_desc_green_slider),
				(assign, reg21, ":value"),
				(overlay_set_text, ":obj_label", "str_gpu_r21"),
				(call_script, "script_gpu_rgb_to_decimal", 1),
				
			(else_try), ####### BLUE SLIDER #######
				(troop_slot_eq, GPU_OBJECTS, gpu_obj_slider_blue, ":object"),
				(troop_set_slot, GPU_OBJECTS, gpu_val_slider_blue, ":value"),
				(troop_get_slot, ":obj_label", GPU_OBJECTS, gpu_obj_desc_blue_slider),
				(assign, reg21, ":value"),
				(overlay_set_text, ":obj_label", "str_gpu_r21"),
				(call_script, "script_gpu_rgb_to_decimal", 1),
				
			(try_end),
		]),
      
      ]),
	  
("party_morale",0,mesh_load_window,[
    (ti_on_presentation_load,
		[
			(set_fixed_point_multiplier, 1000),
			(assign, "$gpu_storage", PMR_OBJECTS),
			(assign, "$gpu_data", PMR_OBJECTS),
			(call_script, "script_diplomacy_get_player_party_morale_values"),
			(assign, ":morale_ideal", reg0),
			(party_get_morale, ":morale_real", "p_main_party"),
			(store_sub, ":recent_events", ":morale_real", ":morale_ideal"),
			
			## OBJ - BUTTON - EXIT
			(str_store_string, s21, "@Exit"),
			(call_script, "script_gpu_create_game_button", "str_gpu_s21", 500, 30, pmr_obj_button_exit),
			
			## OBJ - UI HEADER
			(str_store_string, s21, "@Party Morale Report"),
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", 500, 680, 0, gpu_center), # 680
			(call_script, "script_gpu_resize_object", 0, 150),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", 500, 680, 0, gpu_center), # 680
			(call_script, "script_gpu_resize_object", 0, 150),
			
			## OBJ - HEADER UNDERLINE
			(call_script, "script_gpu_draw_line", 850, 2, 73, 665, gpu_gray), # - Footer
			
			## GENERAL POSITION DEFINITIONS
			(assign, ":pos_x_1", 10),   # Counts the factor number. (center)
			(assign, ":pos_x_2", 30),  # Factor Title (left)
			(assign, ":pos_x_3", 225), # Factor Value (center)
			(assign, ":pos_x_4", 260), # Factor Contributors (left)
			(assign, ":pos_x_5", 535), # Factor Contributor values (center)
			(assign, ":line_step", 25),
			(assign, ":line_count", 26),
			(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
				(faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),
				(val_div, ":faction_morale", 100),
				(neq, ":faction_morale", 0),
				(val_add, ":line_count", 1),
			(try_end),
			(try_begin),
				(ge, "$g_player_party_morale_modifier_leadership", 1),
				(val_add, ":line_count", 1),
			(try_end),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", "$cms_role_storekeeper", BONUS_CHEF),
				(store_skill_level, ":trade_bonus", "skl_trade", "$cms_role_storekeeper"),
				(ge, ":trade_bonus", 1),
				(val_add, ":line_count", 1),
			(try_end),
			(try_begin),
				(call_script, "script_ce_inspiring_get_party_bonus", "p_main_party"),
				(ge, reg0, 1), # Inspiring bonus
				(val_add, ":line_count", 1),
			(try_end),
			(try_begin),
				(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
				(faction_get_slot, ":faction_morale_bonus", "$players_kingdom", slot_faction_party_morale_adjust),
				(neq, ":faction_morale_bonus", 0),
				(val_add, ":line_count", 1),
			(try_end),
			(try_begin),
				(gt, "$g_player_party_morale_modifier_debt", 0),
				(val_add, ":line_count", 1),
			(try_end),
			(try_begin),
				(gt, "$g_player_party_morale_modifier_no_food", 0),
				(val_add, ":line_count", 1),
			(try_end),
			(store_mul, ":pos_y", ":line_step", ":line_count"),   # Starting position.
			
			##################################
			###### PARTY MORALE SECTION ######
			##################################
			(assign, ":x_width", 550),
			(assign, ":y_width", 500),
			(assign, ":x_left", 25),
			(assign, ":y_bottom", 100),
			
			## OBJ - PARTY MORALE HEADER
			(store_div, ":x_center", ":x_width", 2),
			(val_add, ":x_center", ":x_left"),
			(store_add, ":y_title", ":y_bottom", ":y_width"),
			(val_add, ":y_title", 20),
			(party_get_morale, reg21, "p_main_party"),
			(str_store_string, s21, "@Party Morale ( {reg21} of 99 )"),
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_center", ":y_title", 0, gpu_center), # 680
			(call_script, "script_gpu_resize_object", 0, 120),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_center", ":y_title", 0, gpu_center), # 680
			(call_script, "script_gpu_resize_object", 0, 120),
			
			(store_add, ":y_top", ":y_bottom", ":y_width"),
			(call_script, "script_gpu_draw_line", ":x_width", 2, ":x_left", ":y_top", gpu_gray), # - Header Line
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", pmr_obj_factors_container), # Scrolling container
			############### CONTAINER BEGIN ###############
				
				## SPACER
				(str_store_string, s21, "@ "),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				(val_sub, ":pos_y", 15),
				
				######### BASE VALUE ##########
				## COLUMN 1 - Factor #
				(str_store_string, s21, "@1"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 2 - Factor
				(str_store_string, s21, "@BASE VALUE"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 3 - Factor Value
				(try_begin),
					(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
					(faction_get_slot, ":faction_morale_bonus", "$players_kingdom", slot_faction_party_morale_adjust),
				(else_try),
					(assign, ":faction_morale_bonus", 0),
				(try_end),
				
				(store_add, reg21, ":faction_morale_bonus", "$g_player_party_morale_modifier_debt"),
				(str_clear, s22),
				(try_begin),
					(ge, reg21, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 4 - Factor Contributors
				(assign, reg21, morale_min_party_size),
				(store_sub, reg22, morale_max_party_size, 1),
				(str_store_string, s21, "@FACTORS:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: FACTION BONUS
				(try_begin),
					(neq, ":faction_morale_bonus", 0),
					(val_sub, ":pos_y", ":line_step"),
					## COLUMN 4 - Factor Contributors
					(str_store_faction_name, s21, "$players_kingdom"),
					(str_store_string, s21, "@{s21} slavery policy"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(assign, reg21, ":faction_morale_bonus"),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				#### SUB-FACTOR: PARTY WAGE DEBT
				(try_begin),
					(gt, "$g_player_party_morale_modifier_debt", 0),
					(val_sub, ":pos_y", ":line_step"),
					## COLUMN 4 - Factor Contributors
					(str_store_faction_name, s21, "$players_kingdom"),
					(str_store_string, s21, "@Troop debt from wages"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(assign, reg21, "$g_player_party_morale_modifier_debt"),
					(try_begin),
						(ge, reg21, 1),
						(store_mul, ":penalty", reg21, 2),
						(val_sub, reg21, ":penalty"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				
				######### PARTY SIZE ##########
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", ":line_step"),
				## COLUMN 1 - Factor #
				(str_store_string, s21, "@2"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 2 - Factor
				(str_store_string, s21, "@PARTY SIZE"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 3 - Factor Value
				(assign, reg21, "$g_player_party_morale_modifier_party_size"),
				(str_clear, s22),
				(try_begin),
					(ge, reg21, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 4 - Factor Contributors
				(assign, reg21, morale_min_party_size),
				(store_sub, reg22, morale_max_party_size, 1),
				(str_store_string, s21, "@FACTORS: {reg21} to {reg22}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(str_store_string, s21, "@FACTORS:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: PARTY SIZE
				(val_sub, ":pos_y", ":line_step"),
				(party_get_num_companion_stacks, ":num_stacks","p_main_party"),
				(assign, ":troop_count", 0),
				(try_for_range, ":i_stack", 1, ":num_stacks"),
					(party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
					(val_add, ":troop_count", ":stack_size"),
				(try_end),
				(store_div, ":troops_size_to_morale", ":troop_count", morale_party_size_factor),
				(assign, reg23, 0),
				(try_begin),
					(neg|is_between, ":troops_size_to_morale", morale_min_party_size, morale_max_party_size),
					(assign, reg23, 1), # clamped
				(try_end),
				(val_clamp, ":troops_size_to_morale", morale_min_party_size, morale_max_party_size),
				
				(try_begin),
					(neq, ":troops_size_to_morale", 0),
					## COLUMN 4 - Factor Contributors
					(assign, reg22, ":troop_count"),
					(store_sub, reg24, reg22, 1),
					(assign, reg25, morale_party_size_factor),
					(str_store_string, s21, "@{reg22} soldier{reg24?s:} within the party (+1/{reg25})"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(assign, reg21, ":troops_size_to_morale"),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				
				######### FOOD VARIETY ##########
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", ":line_step"),
				## COLUMN 1 - Factor #
				(str_store_string, s21, "@3"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 2 - Factor
				(str_store_string, s21, "@FOOD VARIETY"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 3 - Factor Value
				(assign, reg21, "$g_player_party_morale_modifier_food"),
				(str_clear, s22),
				(try_begin),
					(ge, reg21, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 4 - Factor Contributors
				(str_store_string, s21, "@FACTORS: 0 to Unlimited"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(str_store_string, s21, "@FACTORS:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: FOOD TYPES
				(val_sub, ":pos_y", ":line_step"),
				(assign, ":number_of_foods_player_has", 0),
				(assign, ":total_food_bonus", 0),
				(try_for_range, ":item_no", food_begin, food_end),      
					(call_script, "script_cf_player_has_item_without_modifier", ":item_no", imod_rotten),
					(val_add, ":number_of_foods_player_has", 1),
					(item_get_slot, ":food_bonus", ":item_no", slot_item_food_bonus),
					(val_add, ":total_food_bonus", ":food_bonus"),
				(try_end),
				## COLUMN 4 - Factor Contributors
				(str_store_item_name, s23, ":item_no"),
				(str_store_string, s21, "@Food Stores:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 5 - Factor Contributor Values
				(str_clear, s22),
				(assign, reg21, ":total_food_bonus"),
				(try_begin),
					(ge, reg21, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## TROOP EFFECT: BONUS_CHEF
				(try_begin),
					(assign, ":chef_bonus", 0),
					(call_script, "script_cf_ce_troop_has_ability", "$cms_role_storekeeper", BONUS_CHEF),
					(store_skill_level, ":trade_bonus", "skl_trade", "$cms_role_storekeeper"),
					(ge, ":trade_bonus", 1),
					(val_mul, ":trade_bonus", 25),
					(store_mul, ":chef_bonus", "$g_player_party_morale_modifier_food", ":trade_bonus"),
					(val_div, ":chef_bonus", 1000),
				(try_end),
				
				#### SUB-FACTOR: CHEF BONUS
				(try_begin),
					(neq, ":chef_bonus", 0),
					(val_sub, ":pos_y", ":line_step"),
					
					## COLUMN 4 - Factor Contributors
					(str_store_string, s21, "@Storekeeper Chef Bonus:"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(assign, reg21, ":chef_bonus"),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				#### SUB-FACTOR: NO FOOD PENALTY
				(try_begin),
					(gt, "$g_player_party_morale_modifier_no_food", 0),
					(val_sub, ":pos_y", ":line_step"),
					## COLUMN 4 - Factor Contributors
					(str_store_faction_name, s21, "$players_kingdom"),
					(str_store_string, s21, "@No food penalty"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(assign, reg21, "$g_player_party_morale_modifier_no_food"),
					(try_begin),
						(ge, reg21, 1),
						(store_mul, ":penalty", reg21, 2),
						(val_sub, reg21, ":penalty"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				
				######### LEADERSHIP ##########
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", ":line_step"),
				## COLUMN 1 - Factor #
				(str_store_string, s21, "@4"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 2 - Factor
				(str_store_string, s21, "@LEADERSHIP"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 3 - Factor Value
				(assign, reg21, "$g_player_party_morale_modifier_leadership"),
				(val_add, reg21, "$morale_modifier_inspiring"),
				(str_clear, s22),
				(try_begin),
					(ge, reg21, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 4 - Factor Contributors
				(str_store_string, s21, "@FACTORS: 0 to 40 / 60 (king)"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(str_store_string, s21, "@FACTORS:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: LEADERSHIP SKILL
				(store_skill_level, ":player_leadership", "skl_leadership", "trp_player"),
				
				(try_begin),
					(neq, "$g_player_party_morale_modifier_leadership", 0),
					(val_sub, ":pos_y", ":line_step"),
					## COLUMN 4 - Factor Contributors
					(assign, reg22, ":player_leadership"),
					(str_store_string, s21, "@Leadership skill of {reg22}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(assign, reg21, "$g_player_party_morale_modifier_leadership"),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				#### SUB-FACTOR: INSPIRING EFFECT
				(call_script, "script_ce_inspiring_get_party_bonus", "p_main_party"),
				(assign, reg21, reg0), # Inspiring bonus
				(assign, reg22, reg1), # Troop count
				(assign, reg23, reg2), # Clamped
				
				(try_begin),
					(neq, reg21, 0),
					(val_sub, ":pos_y", ":line_step"),
					## COLUMN 4 - Factor Contributors
					(store_sub, reg24, reg22, 1),
					(str_store_string, s21, "@{reg22} troop{reg24?s:} with the Inspiring ability"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				
				######### PARTY UNITY ##########
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", ":line_step"),
				
				###### PARTY UNITY CALCULATIONS+ ######
				# Determine combined leadership score for player & companions.
				(store_skill_level, ":party_leadership_score", "skl_leadership", "trp_player"),
				(try_for_range, ":companion_no", companions_begin, companions_end),
					(main_party_has_troop, ":companion_no"),
					(store_skill_level, ":leadership", "skl_leadership", ":companion_no"),
					(val_add, ":party_leadership_score", ":leadership"),
				(try_end),
				(val_mul, ":party_leadership_score", 3),
				# Figure out how many of each type of troop the player party has.
				(assign, ":faction_troops", 0),
				(assign, ":non_faction_troops", 0),
				(assign, ":mercenary_troops", 0),
				(assign, ":companion_troops", 0),
				(party_get_num_companion_stacks, ":stack_count","p_main_party"),
				(try_for_range, ":stack_no", 1, ":stack_count"),
					(party_stack_get_troop_id, ":troop_no","p_main_party",":stack_no"),
					(party_stack_get_size, ":stack_size","p_main_party",":stack_no"),
					(store_faction_of_troop, ":faction_no", ":troop_no"),
					##
					(faction_get_slot, ":troop_culture", ":faction_no",  slot_faction_culture),
					(faction_get_slot, ":player_culture", "$players_kingdom",  slot_faction_culture),
					## Determine Troop Type
					(try_begin),
						(is_between, ":troop_no", companions_begin, companions_end),
						(assign, ":treat_as_type", 1),
					(else_try),
						(faction_slot_eq, "$players_kingdom", slot_faction_culture, "fac_culture_player"),
						(eq, ":troop_culture", "fac_culture_player"),
						(is_between, ":troop_no", player_troops_begin, player_troops_end),
						# (this_or_next|neq, "$players_kingdom", "fac_player_supporters_faction"),
						# (eq, ":player_culture", "fac_culture_player"),
						# (eq, ":faction_no", "$players_kingdom"),
						(assign, ":treat_as_type", 2),
					(else_try),
						(neg|faction_slot_eq, "$players_kingdom", slot_faction_culture, "fac_culture_player"),
						(eq, ":troop_culture", ":player_culture"),
						(neg|is_between, ":troop_no", player_troops_begin, player_troops_end),
						(assign, ":treat_as_type", 2),
					(else_try),
						(is_between, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
						(assign, ":treat_as_type", 4),
					(else_try),
						(assign, ":treat_as_type", 3),
					(try_end),
					
					(try_begin),
						## TROOP ABILITY: BONUS_DEDICATED
						(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_DEDICATED), # combat_scripts.py - ability constants in combat_constants.py
						(val_sub, ":treat_as_type", 1),
						(val_max, ":treat_as_type", 1),
					(try_end),
					
					(try_begin),
						(eq, ":treat_as_type", 1),
						(val_add, ":companion_troops", ":stack_size"),
					(else_try),
						(eq, ":treat_as_type", 2),
						(val_add, ":faction_troops", ":stack_size"),
					(else_try),
						(eq, ":treat_as_type", 4),
						(val_add, ":mercenary_troops", ":stack_size"),
					(else_try),
						(val_add, ":non_faction_troops", ":stack_size"),
					(try_end),
				(try_end),
				
				# Determine unity based on faction troops.
				(try_begin),
					(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
					(faction_get_slot, ":faction_top", "$players_kingdom", slot_faction_unity_top_faction),
					(faction_get_slot, ":faction_bot", "$players_kingdom", slot_faction_unity_bottom_faction),
				(else_try),
					## DEFAULT: -1 for every 3 faction troops.
					(assign, ":faction_top", 1),
					(assign, ":faction_bot", 3),
				(try_end),
				(val_max, ":faction_bot", 1), # Prevent Div/0 errors.
				(assign, ":faction_troops_orig", ":faction_troops"),
				(val_mul, ":faction_troops", ":faction_top"),
				(val_div, ":faction_troops", ":faction_bot"),
				
				# Determine unity based on non-faction troops.
				(try_begin),
					(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
					(faction_get_slot, ":non_faction_top", "$players_kingdom", slot_faction_unity_top_nonfaction),
					(faction_get_slot, ":non_faction_bot", "$players_kingdom", slot_faction_unity_bottom_nonfaction),
				(else_try),
					## DEFAULT: -1 for every 1 non-faction troops.
					(assign, ":non_faction_top", 1),
					(assign, ":non_faction_bot", 1),
				(try_end),
				(val_max, ":non_faction_bot", 1), # Prevent Div/0 errors.
				(assign, ":non_faction_troops_orig", ":non_faction_troops"),
				(val_mul, ":non_faction_troops", ":non_faction_top"),
				(val_div, ":non_faction_troops", ":non_faction_bot"),
				
				# Determine unity based on mercenary troops.
				(try_begin),
					(call_script, "script_cf_common_player_is_vassal_or_greater", 1),
					(faction_get_slot, ":merc_top", "$players_kingdom", slot_faction_unity_top_mercs),
					(faction_get_slot, ":merc_bot", "$players_kingdom", slot_faction_unity_bottom_mercs),
				(else_try),
					## DEFAULT: -2 for every 1 non-faction troops.
					(assign, ":merc_top", 2),
					(assign, ":merc_bot", 1),
				(try_end),
				(val_max, ":merc_bot", 1), # Prevent Div/0 errors.
				(assign, ":mercenary_troops_orig", ":mercenary_troops"),
				(val_mul, ":mercenary_troops", ":merc_top"),
				(val_div, ":mercenary_troops", ":merc_bot"),
				###### PARTY UNITY CALCULATIONS- ######
				
				## COLUMN 1 - Factor #
				(str_store_string, s21, "@5"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 2 - Factor
				(str_store_string, s21, "@PARTY UNITY"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 3 - Factor Value
				(call_script, "script_diplomacy_get_player_party_morale_values"),
				(assign, reg23, "$party_unity"), # ":unity"), # 
				(str_clear, s22),
				(try_begin),
					(ge, reg23, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg23}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 4 - Factor Contributors
				(assign, reg21, morale_min_party_unity),
				(store_sub, reg22, morale_max_party_unity, 1),
				(str_store_string, s21, "@FACTORS: {reg21} to {reg22}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(str_store_string, s21, "@FACTORS:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: PARTY UNITY - COMPANIONS
				(val_sub, ":pos_y", ":line_step"),
				
				## COLUMN 4 - Factor Contributors
				(store_div, reg24, ":party_leadership_score", 3),
				(str_store_string, s21, "@Combined companion leadership ({reg24})"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 5 - Factor Contributor Values
				(str_clear, s22),
				(assign, reg21, ":party_leadership_score"),
				(try_begin),
					(ge, reg21, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: PARTY UNITY - FACTION TROOPS
				(val_sub, ":pos_y", ":line_step"),
				
				## COLUMN 4 - Factor Contributors
				(assign, reg22, ":faction_troops_orig"),
				(store_sub, reg23, reg22, 1),
				(assign, reg24, ":faction_top"),
				(assign, reg25, ":faction_bot"),
				(str_store_string, s21, "@{reg22} faction troop{reg23?s:} (-{reg24}/{reg25})"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 5 - Factor Contributor Values
				(str_clear, s22),
				(assign, reg21, ":faction_troops"),
				(try_begin),
					(ge, reg21, 1),
					(store_mul, ":penalty", reg21, 2),
					(val_sub, reg21, ":penalty"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: PARTY UNITY - NON-FACTION TROOPS
				(val_sub, ":pos_y", ":line_step"),
				
				## COLUMN 4 - Factor Contributors
				(assign, reg22, ":non_faction_troops_orig"),
				(store_sub, reg23, reg22, 1),
				(assign, reg24, ":non_faction_top"),
				(assign, reg25, ":non_faction_bot"),
				(str_store_string, s21, "@{reg22} non-faction troop{reg23?s:} (-{reg24}/{reg25})"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 5 - Factor Contributor Values
				(str_clear, s22),
				(assign, reg21, ":non_faction_troops"),
				(try_begin),
					(ge, reg21, 1),
					(store_mul, ":penalty", reg21, 2),
					(val_sub, reg21, ":penalty"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: PARTY UNITY - MERCENARY TROOPS
				(val_sub, ":pos_y", ":line_step"),
				
				## COLUMN 4 - Factor Contributors
				(assign, reg22, ":mercenary_troops_orig"),
				(store_sub, reg23, reg22, 1),
				(assign, reg24, ":merc_top"),
				(assign, reg25, ":merc_bot"),
				(str_store_string, s21, "@{reg22} mercenary troop{reg23?s:} (-{reg24}/{reg25})"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 5 - Factor Contributor Values
				(str_clear, s22),
				(assign, reg21, ":mercenary_troops"),
				(try_begin),
					(ge, reg21, 1),
					(store_mul, ":penalty", reg21, 2),
					(val_sub, reg21, ":penalty"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				
				######### BATTLE WEARINESS ##########
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", ":line_step"),
				## COLUMN 1 - Factor #
				(str_store_string, s21, "@6"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 2 - Factor
				(str_store_string, s21, "@BATTLE WEARINESS"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 3 - Factor Value
				(assign, reg21, "$morale_battle_weary"),
				(str_clear, s22),
				(try_begin),
					(ge, reg21, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 4 - Factor Contributors
				(assign, reg21, morale_min_battle_weariness),
				(store_sub, reg22, morale_max_battle_weariness, 1),
				(str_store_string, s21, "@FACTORS: {reg21} to {reg22}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(str_store_string, s21, "@FACTORS:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: PENALTY PER BATTLE
				(val_sub, ":pos_y", ":line_step"),
				(store_current_hours, ":hours"),
				
				(try_begin),
					## COLUMN 4 - Factor Contributors
					(str_store_string, s21, "@Penalty per Battle"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(call_script, "script_diplomacy_get_battle_weariness_factor", WEARINESS_PENALTY, 21),
					(str_store_string, s21, "@{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				#### SUB-FACTOR: DAYS SINCE LAST COMBAT
				(val_sub, ":pos_y", ":line_step"),
				(store_current_hours, ":hours"),
				
				(try_begin),
					## COLUMN 4 - Factor Contributors
					(str_store_string, s21, "@Hours Since Last Fight"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(store_sub, reg21, ":hours", "$morale_time_last_battle"),
					# (try_begin),
						# (ge, reg21, 1),
						# (str_store_string, s22, "@+"),
					# (try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				#### SUB-FACTOR: IMPROVEMENT RATE
				(val_sub, ":pos_y", ":line_step"),
				(try_begin),
					## COLUMN 4 - Factor Contributors
					(call_script, "script_diplomacy_get_battle_weariness_factor", WEARINESS_RECOVERY_LIMIT, 21),
					(str_store_string, s21, "@Improvement (every 4 hours) (Max: {reg21})"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(call_script, "script_diplomacy_get_battle_weariness_factor", WEARINESS_RECOVERY_RATE, 21),
					(str_clear, s22),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				
				######### RECENT EVENTS ##########
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", ":line_step"),
				## COLUMN 1 - Factor #
				(str_store_string, s21, "@7"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 2 - Factor
				(str_store_string, s21, "@RECENT EVENTS"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 3 - Factor Value
				(assign, reg21, ":recent_events"),
				(str_clear, s22),
				(try_begin),
					(ge, reg21, 1),
					(str_store_string, s22, "@+"),
				(try_end),
				(str_store_string, s21, "@{s22}{reg21}"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 4 - Factor Contributors
				(str_store_string, s21, "@FACTORS:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: IDEAL MORALE
				(val_sub, ":pos_y", ":line_step"),
				(assign, reg21, ":morale_ideal"),
				
				(try_begin),
					## COLUMN 4 - Factor Contributors
					(str_store_string, s21, "@Ideal party morale"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				#### SUB-FACTOR: REAL MORALE
				(val_sub, ":pos_y", ":line_step"),
				(assign, reg21, ":morale_real"),
				
				(try_begin),
					## COLUMN 4 - Factor Contributors
					(str_store_string, s21, "@Real party morale"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				
				######### KINGDOM PENALTIES ##########
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", ":line_step"),
				## COLUMN 1 - Factor #
				(str_store_string, s21, "@8"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 2 - Factor
				(str_store_string, s21, "@CULTURAL RELATION"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 3 - Factor Value
				(str_store_string, s21, "@Varies"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## COLUMN 4 - Factor Contributors
				(str_store_string, s21, "@FACTORS:"),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				#### SUB-FACTOR: CULTURAL FACTORS
				(val_sub, ":pos_y", ":line_step"),
				
				(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
					(faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),
					(val_div, ":faction_morale", 100),
					(str_store_faction_name, s22, ":kingdom_no"),
					(assign, reg21, ":faction_morale"),
					(neq, reg21, 0),
					
					## COLUMN 4 - Factor Contributors
					(str_store_string, s21, "@{s22} Troops"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Factor Contributor Values
					(str_clear, s22),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					(val_sub, ":pos_y", ":line_step"),
				(try_end),
				
			################ CONTAINER END ################	
			(set_container_overlay, -1),
			
			##################################
			###### PARTY MORALE SECTION ######
			##################################
			## GENERAL POSITION DEFINITIONS
			(assign, ":pos_x_1", 10),   # Number of troops in a stack. (center)
			(assign, ":pos_x_2", 30),  # Troop name. (left)
			(assign, ":pos_x_3", 240), # Morale Value (center)
			(assign, ":pos_x_4", 260), # Thinking (left)
			(assign, ":line_step", 25),
			(assign, ":line_count", 1),
			(party_get_num_companion_stacks, ":stack_count", "p_main_party"),
			(try_for_range, ":stack_no", 1, ":stack_count"),
				(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
				(neg|troop_is_hero, ":troop_no"),
				(val_add, ":line_count", 1),
			(try_end),
			(store_mul, ":pos_y", ":line_count", ":line_step"), # Starting position.
			
			(assign, ":x_width", 350),
			(assign, ":y_width", 235),
			(assign, ":x_left", 610),
			(assign, ":y_bottom", 365),
			
			## OBJ - PARTY MORALE HEADER
			(store_div, ":x_center", ":x_width", 2),
			(val_add, ":x_center", ":x_left"),
			(store_add, ":y_title", ":y_bottom", ":y_width"),
			(val_add, ":y_title", 20),
			(str_store_string, s21, "@Troop Morale"),
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_center", ":y_title", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 120),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_center", ":y_title", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 120),
			
			(store_add, ":y_top", ":y_bottom", ":y_width"),
			(call_script, "script_gpu_draw_line", ":x_width", 2, ":x_left", ":y_top", gpu_gray), # - Header Line
			
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", pmr_obj_factors_container), # Scrolling container
			############### CONTAINER BEGIN ###############
				
				## SPACER
				(str_store_string, s21, "@   "),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				(val_sub, ":pos_y", 15),
				
				(party_get_num_companion_stacks, ":stack_count", "p_main_party"),
				(try_for_range, ":stack_no", 1, ":stack_count"),
					(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"),
					
					## COLUMN 1 - Number of troops in a stack. (center)
					(party_count_companions_of_type, reg21, "p_main_party", ":troop_no"),
					(str_store_string, s21, "@{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 2 - Troop name. (left)
					(str_store_troop_name, s21, ":troop_no"),
					(try_begin),
						(ge, reg21, 2),
						(str_store_troop_name_plural, s21, ":troop_no"),
					(try_end),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 3 - Morale Value (center)
					(party_get_morale, ":troop_morale", "p_main_party"),
					(store_faction_of_troop, ":kingdom_no", ":troop_no"),
					(faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),
					(val_div, ":faction_morale", 100),
					(val_add, ":troop_morale", ":faction_morale"),
					## WINDYPLAINS+ ## - Troop Ability - BONUS_LOYAL
					(try_begin),
						(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_LOYAL), # combat_scripts.py - ability constants in combat_constants.py
						(val_add, ":troop_morale", 20),
						(val_clamp, ":troop_morale", 0, 101),
					(try_end),
					## WINDYPLAINS- ##
					(assign, reg21, ":troop_morale"),
					(str_store_string, s21, "@{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 4 - Thinking (left)
					(faction_get_slot, ":desertion_threshold", "$players_kingdom", slot_faction_desertion_threshold),
					(store_add, ":unhappy_threshold", ":desertion_threshold", 10),
					(try_begin),
						(lt, ":troop_morale", ":desertion_threshold"),
						(str_store_string, s21, "@Ready to desert"),
						(assign, ":color", 4980736),  # Dark Red
					(else_try),
						(is_between, ":troop_morale", ":desertion_threshold", ":unhappy_threshold"),
						(str_store_string, s21, "@Unhappy"),
						(assign, ":color", gpu_black),
					(else_try),
						(ge, ":troop_morale", 85),
						(str_store_string, s21, "@Loyal"),
						(assign, ":color", 14336),     # Dark Green
					(else_try),
						(str_store_string, s21, "@Content"),
						(assign, ":color", 14336),     # Dark Green
					(try_end),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_left),
					(overlay_set_color, reg1, ":color"),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					(val_sub, ":pos_y", ":line_step"),
				(try_end),
				
			################ CONTAINER END ################	
			(set_container_overlay, -1),
			
			##################################
			###### MORALE LOG SECTION ######
			##################################
			## GENERAL POSITION DEFINITIONS
			(assign, ":pos_x_1", 5),   # Date (left)
			(assign, ":pos_x_2", 100), # Reason (left)
			(assign, ":pos_x_3", 275), # Change (right)
			(assign, ":pos_x_4", 297), # Real Morale (center)
			(assign, ":pos_x_5", 335), # Ideal Morale (center)
			(assign, ":line_step", 25),
			(store_mul, ":pos_y", "$morale_log_entries", ":line_step"),
			(val_add, ":pos_y", ":line_step"),
			
			(assign, ":x_width", 350),
			(assign, ":y_width", 215),
			(assign, ":x_left", 610),
			(assign, ":y_bottom", 100),
			
			## OBJ - PARTY MORALE HEADER
			(store_div, ":x_center", ":x_width", 2),
			(val_add, ":x_center", ":x_left"),
			(store_add, ":y_title", ":y_bottom", ":y_width"),
			(val_add, ":y_title", 20),
			(str_store_string, s21, "@Morale History"),
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_center", ":y_title", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 120),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_center", ":y_title", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 120),
			
			## mini-header
			(str_store_string, s21, "@REAL"),
			(store_add, ":x_temp", ":x_left", ":pos_x_4"),
			# (val_add, ":x_temp", 4),
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_temp", ":y_title", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 60),
			(str_store_string, s21, "@IDEAL"),
			(store_add, ":x_temp", ":x_left", ":pos_x_5"),
			# (val_add, ":x_temp", 0),
			(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_temp", ":y_title", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 60),
			
			(store_add, ":y_top", ":y_bottom", ":y_width"),
			(call_script, "script_gpu_draw_line", ":x_width", 2, ":x_left", ":y_top", gpu_gray), # - Header Line
			
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", pmr_obj_factors_container), # Scrolling container
			############### CONTAINER BEGIN ###############
				
				## SPACER
				(try_begin),
					(eq, "$morale_log_entries", 0),
					(str_store_string, s21, "@  ^Morale history is empty."),
				(else_try),
					(str_store_string, s21, "@   "),
				(try_end),
				(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":x_center", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				(val_sub, ":pos_y", 15),
				(store_add, ":total_entries", "$morale_log_entries", 1),
				
				(try_for_range_backwards, ":entry_no", 1, ":total_entries"),
					(neq, "$morale_log_entries", 0), # Prevent errors if no entries exist.
					
					## COLUMN 1 - Date (left)
					(call_script, "script_diplomacy_get_morale_log_entry", ":entry_no", PMR_LOG_DATE, 21),
					(str_store_date, s21, reg21),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_1", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 2 - Reason (left)
					(call_script, "script_diplomacy_get_morale_log_entry", ":entry_no", PMR_LOG_REASON, 21),
					(try_begin),
						(eq, reg21, PMR_PARTY_NOT_FED),
						(str_store_string, s21, "@Party Not Fed"),
					(else_try),
						(eq, reg21, PMR_PARTY_DEFEATED),
						(str_store_string, s21, "@Defeated in Battle"),
					(else_try),
						(eq, reg21, PMR_PARTY_VICTORY),
						(str_store_string, s21, "@Battle Victory"),
					(else_try),
						(eq, reg21, PMR_DAILY_SHIFT),
						(str_store_string, s21, "@Daily Shift"),
					(else_try),
						(eq, reg21, PMR_FRIENDLY_FIRE),
						(str_store_string, s21, "@Friendly Fire"),
					(else_try),
						(eq, reg21, PMR_RETREAT),
						(str_store_string, s21, "@Retreated From Battle"),
					(else_try),
						(eq, reg21, PMR_RECRUITED_PRISONERS),
						(str_store_string, s21, "@Recruited Prisoners"),
					(else_try),
						(eq, reg21, PMR_SACRIFICED_MEN),
						(str_store_string, s21, "@Sacrificed Men"),
					(else_try),
						(eq, reg21, PMR_LOOTED_VILLAGE),
						(str_store_string, s21, "@Village Looted"),
					(else_try),
						(eq, reg21, PMR_ATTENDED_FEAST),
						(str_store_string, s21, "@Attended Feast"),
					(else_try),
						(str_store_string, s21, "@Undefined Reason"),
					(try_end),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_2", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 3 - Change (right)
					(call_script, "script_diplomacy_get_morale_log_entry", ":entry_no", PMR_LOG_CHANGE, 21),
					(str_clear, s22),
					(try_begin),
						(ge, reg21, 1),
						(str_store_string, s22, "@+"),
					(try_end),
					(str_store_string, s21, "@{s22}{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_3", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 4 - Real Morale (right)
					(call_script, "script_diplomacy_get_morale_log_entry", ":entry_no", PMR_LOG_MORALE, 21),
					(str_store_string, s21, "@{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_4", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## COLUMN 5 - Ideal Morale (left)
					(call_script, "script_diplomacy_get_morale_log_entry", ":entry_no", PMR_LOG_IDEAL, 21),
					(str_store_string, s21, "@{reg21}"),
					(call_script, "script_gpu_create_text_label", "str_gpu_s21", ":pos_x_5", ":pos_y", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					(val_sub, ":pos_y", ":line_step"),
				(try_end),
				
			################ CONTAINER END ################	
			(set_container_overlay, -1),
			
			(presentation_set_duration, 999999),
		]),
    (ti_on_presentation_event_state_change,
		[
			(store_trigger_param_1, ":object"),
			# (store_trigger_param_2, ":value"),
			
			(try_begin), ####### EXIT BUTTON #######
				(troop_slot_eq, PMR_OBJECTS, pmr_obj_button_exit, ":object"),
				# End the presentation.
				(presentation_set_duration, 0),
				
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