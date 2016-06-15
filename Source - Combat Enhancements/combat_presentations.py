# Combat Enhancements by Windyplains

from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
# from header_items import *   # Added for Show all Items presentation.
# from module_items import *   # Added for Show all Items presentation.
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
#####                                             PLAYER ABILITY CHOOSER                                              #####
###########################################################################################################################
("ce_character_abilities", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(assign, "$gpu_storage", PRES_OBJECTS),
		(assign, "$gpu_data", PRES_OBJECTS),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(str_store_string, s21, "@Ability Selection"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, ce_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", ce_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, ce_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", ce_obj_main_title, 150),
		
		## OBJ - LINE - TITLE DIVIDER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		## OBJ - BUTTON - DONE
        (str_store_string, s21, "@Done"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 500, 30, ce_obj_button_done), # DONE
		
		## OBJ - BUTTON - CLEAR ALL ABILITIES (DEBUGGING)
		(try_begin),
			(this_or_next|ge, DEBUG_TROOP_ABILITIES, 1),
			(ge, BETA_TESTING_MODE, 1),
			(str_store_string, s21, "@Clear Abilities"),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 175, 30, ce_obj_button_clear_abilities),
		(try_end),
		
		#########################
		#### ABILITY UNLOCKS ####
		#########################
		
		# (assign, ":y_bottom", 80),
		(assign, ":x_left",  40),
		(assign, ":x_width", 265),
		# (assign, ":y_width", 285),
		(assign, ":line_step", 40),
		(store_div, ":x_title", ":x_width", 2),
		(val_add, ":x_title", ":x_left"),
		
		## OBJ - Character Portrait
		(create_mesh_overlay_with_tableau_material, reg1, -1, "tableau_troop_note_mesh", "trp_player"),
        (position_set_x, pos2, 70), 
        (position_set_y, pos2, 430),
        (overlay_set_position, reg1, pos2),
        (position_set_x, pos2, 600), #1150
        (position_set_y, pos2, 600), #1150
        (overlay_set_size, reg1, pos2),
		
		## OBJ - TEXT - CHARACTER NAME
		(str_store_troop_name, s21, "trp_player"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_title", 415, 0, gpu_center), # 680
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - TEXT - HEADER
		(str_store_string, s21, "@UNLOCKED ABILITIES"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_title", 370, 0, gpu_center), # 680
		(call_script, "script_gpu_resize_object", 0, 75),
		(overlay_set_color, reg1, gpu_gray),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_title", 370, 0, gpu_center), # 680
		(call_script, "script_gpu_resize_object", 0, 75),
		
		(assign, ":pos_y", 330),
		(assign, ":pos_x", 50),
		(store_add, ":x_name", ":pos_x", 60),
		(store_add, ":x_assign", ":x_name", 120),
		
		## OBJ - TEXT - UNLOCK LEVEL 5
		(assign, ":slot_offset", 0),
		(str_store_string, s21, "@Level 5"),
		(store_add, ":obj_slot", ce_obj_field_levels_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":pos_x", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		
		## OBJ - TEXT - ABILITY TITLE 5
		(troop_get_slot, ":ability_no", "trp_player", slot_troop_ability_1),
		(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
		(str_store_string, s21, s31),
		(store_add, ":obj_slot", ce_obj_field_abilities_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":x_name", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(lt, ":level", 5),
			(str_store_string, s21, "@N / A"),
			(overlay_set_text, reg1, s21),
			(overlay_set_color, reg1, gpu_gray),
		(try_end),
		(store_add, ":val_slot", ce_obj_val_abilities_start, ":slot_offset"),
		(troop_set_slot, PRES_OBJECTS, ":val_slot", ":ability_no"),
		# Add an assign button.
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(this_or_next|ge, DEBUG_TROOP_ABILITIES, 1),
			(ge, ":level", 5),
			(str_store_string, s21, "@<-- Assign"),
			(store_add, ":obj_slot", ce_obj_button_assign_ability, ":slot_offset"),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_assign", ":pos_y", ":obj_slot"),
			(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_end),
		(val_sub, ":pos_y", ":line_step"),
		
		## OBJ - TEXT - UNLOCK LEVEL 10
		(assign, ":slot_offset", 1),
		(str_store_string, s21, "@Level 10"),
		(store_add, ":obj_slot", ce_obj_field_levels_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":pos_x", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		
		## OBJ - TEXT - ABILITY TITLE 10
		(troop_get_slot, ":ability_no", "trp_player", slot_troop_ability_2),
		(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
		(str_store_string, s21, s31),
		(store_add, ":obj_slot", ce_obj_field_abilities_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":x_name", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(lt, ":level", 10),
			(str_store_string, s21, "@N / A"),
			(overlay_set_text, reg1, s21),
			(overlay_set_color, reg1, gpu_gray),
		(try_end),
		(store_add, ":val_slot", ce_obj_val_abilities_start, ":slot_offset"),
		(troop_set_slot, PRES_OBJECTS, ":val_slot", ":ability_no"),
		# Add an assign button.
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(this_or_next|ge, DEBUG_TROOP_ABILITIES, 1),
			(ge, ":level", 10),
			(str_store_string, s21, "@<-- Assign"),
			(store_add, ":obj_slot", ce_obj_button_assign_ability, ":slot_offset"),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_assign", ":pos_y", ":obj_slot"),
			(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_end),
		(val_sub, ":pos_y", ":line_step"),
		
		## OBJ - TEXT - UNLOCK LEVEL 15
		(assign, ":slot_offset", 2),
		(str_store_string, s21, "@Level 15"),
		(store_add, ":obj_slot", ce_obj_field_levels_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":pos_x", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		
		## OBJ - TEXT - ABILITY TITLE 15
		(troop_get_slot, ":ability_no", "trp_player", slot_troop_ability_3),
		(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
		(str_store_string, s21, s31),
		(store_add, ":obj_slot", ce_obj_field_abilities_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":x_name", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(lt, ":level", 15),
			(str_store_string, s21, "@N / A"),
			(overlay_set_text, reg1, s21),
			(overlay_set_color, reg1, gpu_gray),
		(try_end),
		(store_add, ":val_slot", ce_obj_val_abilities_start, ":slot_offset"),
		(troop_set_slot, PRES_OBJECTS, ":val_slot", ":ability_no"),
		# Add an assign button.
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(this_or_next|ge, DEBUG_TROOP_ABILITIES, 1),
			(ge, ":level", 15),
			(str_store_string, s21, "@<-- Assign"),
			(store_add, ":obj_slot", ce_obj_button_assign_ability, ":slot_offset"),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_assign", ":pos_y", ":obj_slot"),
			(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_end),
		(val_sub, ":pos_y", ":line_step"),
		
		## OBJ - TEXT - UNLOCK LEVEL 20
		(assign, ":slot_offset", 3),
		(str_store_string, s21, "@Level 20"),
		(store_add, ":obj_slot", ce_obj_field_levels_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":pos_x", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		
		## OBJ - TEXT - ABILITY TITLE 20
		(troop_get_slot, ":ability_no", "trp_player", slot_troop_ability_4),
		(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
		(str_store_string, s21, s31),
		(store_add, ":obj_slot", ce_obj_field_abilities_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":x_name", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(lt, ":level", 20),
			(str_store_string, s21, "@N / A"),
			(overlay_set_text, reg1, s21),
			(overlay_set_color, reg1, gpu_gray),
		(try_end),
		(store_add, ":val_slot", ce_obj_val_abilities_start, ":slot_offset"),
		(troop_set_slot, PRES_OBJECTS, ":val_slot", ":ability_no"),
		# Add an assign button.
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(this_or_next|ge, DEBUG_TROOP_ABILITIES, 1),
			(ge, ":level", 20),
			(str_store_string, s21, "@<-- Assign"),
			(store_add, ":obj_slot", ce_obj_button_assign_ability, ":slot_offset"),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_assign", ":pos_y", ":obj_slot"),
			(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_end),
		(val_sub, ":pos_y", ":line_step"),
		
		## OBJ - TEXT - UNLOCK LEVEL 25
		(assign, ":slot_offset", 4),
		(str_store_string, s21, "@Level 25"),
		(store_add, ":obj_slot", ce_obj_field_levels_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":pos_x", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		
		## OBJ - TEXT - ABILITY TITLE 25
		(troop_get_slot, ":ability_no", "trp_player", slot_troop_ability_5),
		(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
		(str_store_string, s21, s31),
		(store_add, ":obj_slot", ce_obj_field_abilities_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":x_name", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(lt, ":level", 25),
			(str_store_string, s21, "@N / A"),
			(overlay_set_text, reg1, s21),
			(overlay_set_color, reg1, gpu_gray),
		(try_end),
		(store_add, ":val_slot", ce_obj_val_abilities_start, ":slot_offset"),
		(troop_set_slot, PRES_OBJECTS, ":val_slot", ":ability_no"),
		# Add an assign button.
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(this_or_next|ge, DEBUG_TROOP_ABILITIES, 1),
			(ge, ":level", 25),
			(str_store_string, s21, "@<-- Assign"),
			(store_add, ":obj_slot", ce_obj_button_assign_ability, ":slot_offset"),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_assign", ":pos_y", ":obj_slot"),
			(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_end),
		(val_sub, ":pos_y", ":line_step"),
		
		## OBJ - TEXT - UNLOCK LEVEL 30
		(assign, ":slot_offset", 5),
		(str_store_string, s21, "@Level 30"),
		(store_add, ":obj_slot", ce_obj_field_levels_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":pos_x", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		
		## OBJ - TEXT - ABILITY TITLE 30
		(troop_get_slot, ":ability_no", "trp_player", slot_troop_ability_6),
		(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
		(str_store_string, s21, s31),
		(store_add, ":obj_slot", ce_obj_field_abilities_start, ":slot_offset"),
		(call_script, "script_gpu_create_button", "str_hub_s21", ":x_name", ":pos_y", ":obj_slot"),
		(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(lt, ":level", 30),
			(str_store_string, s21, "@N / A"),
			(overlay_set_text, reg1, s21),
			(overlay_set_color, reg1, gpu_gray),
		(try_end),
		(store_add, ":val_slot", ce_obj_val_abilities_start, ":slot_offset"),
		(troop_set_slot, PRES_OBJECTS, ":val_slot", ":ability_no"),
		# Add an assign button.
		(try_begin),
			(eq, ":ability_no", BONUS_UNASSIGNED),
			(store_character_level, ":level", "trp_player"),
			(this_or_next|ge, DEBUG_TROOP_ABILITIES, 1),
			(ge, ":level", 30),
			(str_store_string, s21, "@<-- Assign"),
			(store_add, ":obj_slot", ce_obj_button_assign_ability, ":slot_offset"),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_assign", ":pos_y", ":obj_slot"),
			(call_script, "script_gpu_resize_object", ":obj_slot", 75),
		(try_end),
		(val_sub, ":pos_y", ":line_step"),
		
		
		#########################
		#### ABILITY TOOLTIP ####
		#########################
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  315),
		(assign, ":x_width", 375),
		(assign, ":y_width", 495),
		(assign, ":line_step", 30),
		
		## OBJ - TEXT - PRESENTATION TITLE
		(troop_get_slot, ":ability_no", PRES_OBJECTS, ce_val_selected_ability),
		(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
		(str_store_string, s21, s31),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 605, ce_obj_selected_ability, gpu_center), # 680
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 605, ce_obj_selected_ability, gpu_center), # 680
		
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", ce_obj_container_ability_list),
			
			(assign, ":pos_y", 0),
			
			## OBJ - TEXT - SPACER
			(str_clear, s21),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 10, ":pos_y", 0, gpu_left), # 680
			(call_script, "script_gpu_resize_object", 0, 75),
			(val_sub, ":pos_y", ":line_step"),
			
			(troop_get_slot, ":ability_no", PRES_OBJECTS, ce_val_selected_ability),
			(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
			(str_store_string, s21, s32),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 10, ":pos_y", ce_obj_field_tooltip_1, gpu_left), # 680
			(call_script, "script_gpu_resize_object", ce_obj_field_tooltip_1, 85),
			(val_sub, ":pos_y", ":line_step"),
			
		(set_container_overlay, -1),
		
		######################
		#### ABILITY LIST ####
		######################
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  710),
		(assign, ":x_width", 250),
		(assign, ":y_width", 515),
		(assign, ":line_step", 30),
		
		## OBJ - TEXT - HEADER
		(store_div, ":x_title", ":x_width", 2),
		(val_add, ":x_title", ":x_left"),
		(str_store_string, s21, "@AVAILABLE ABILITIES"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_title", 605, 0, gpu_center), # 680
		(call_script, "script_gpu_resize_object", 0, 75),
		(overlay_set_color, reg1, gpu_gray),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_title", 605, 0, gpu_center), # 680
		(call_script, "script_gpu_resize_object", 0, 75),
		
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", ce_obj_container_ability_list),
			(assign, ":abilities", 0),
			(try_for_range, ":ability_no", BONUS_UNASSIGNED, BONUS_END_OF_ABILITIES),
				(call_script, "script_cf_ce_player_can_use_ability", ":ability_no", 1), # combat_scripts.py
				(val_add, ":abilities", 1),
			(try_end),
			
			(store_mul, ":pos_y", ":abilities", ":line_step"),
			(assign, ":pos_x", 10),
			
			## OBJ - TEXT - SPACER
			(str_clear, s21),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_name", ":pos_y", 0, gpu_left), # 680
			(call_script, "script_gpu_resize_object", 0, 75),
			(val_sub, ":pos_y", ":line_step"),
			
			(try_for_range, ":ability_no", BONUS_UNASSIGNED, BONUS_END_OF_ABILITIES),
				(call_script, "script_cf_ce_player_can_use_ability", ":ability_no", 1), # combat_scripts.py
				(store_sub, ":offset", ":ability_no", BONUS_UNASSIGNED),
				(store_add, ":slot_no", ce_obj_button_ability_list_start, ":offset"),
				
				## FILTER - Don't pass if the player already has this ability.
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", "trp_player", ":ability_no"),
					(troop_set_slot, PRES_OBJECTS, ":slot_no", -1),
				(else_try),
					(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
					(str_store_string, s21, s31),
					(call_script, "script_gpu_create_button", "str_hub_s21", ":pos_x", ":pos_y", ":slot_no"),
					(call_script, "script_gpu_resize_object", ":slot_no", 75),
					(val_sub, ":pos_y", ":line_step"),
				(try_end),
				
			(try_end),
		(set_container_overlay, -1),
		
		
      ]),
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        # (store_trigger_param_2, ":value"),
		
		(try_begin), ####### BUTTON - DONE #######
			(troop_slot_eq, PRES_OBJECTS, ce_obj_button_done, ":object"),
			(presentation_set_duration, 0),
			
		(else_try), ####### UNLOCKED ABILITIES #######
			(assign, ":continue", 0),
			(try_for_range, ":slot_no", ce_obj_field_levels_start, ce_obj_val_abilities_start),
				(troop_slot_eq, PRES_OBJECTS, ":slot_no", ":object"),
				(assign, ":continue", 1),
				(store_sub, ":selected_no", ":slot_no", ce_obj_field_levels_start),
			(try_end),
			(try_for_range, ":slot_no", ce_obj_field_abilities_start, ce_obj_button_ability_list_start),
				(troop_slot_eq, PRES_OBJECTS, ":slot_no", ":object"),
				(assign, ":continue", 1),
				(store_sub, ":selected_no", ":slot_no", ce_obj_field_abilities_start),
			(try_end),
			(eq, ":continue", 1),
			(store_add, ":ability_slot", ce_obj_val_abilities_start, ":selected_no"),
			(troop_get_slot, ":ability_no", PRES_OBJECTS, ":ability_slot"),
			(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
			(troop_set_slot, PRES_OBJECTS, ce_val_selected_ability, ":ability_no"),
			(start_presentation, "prsnt_ce_character_abilities"),
			
		(else_try), ####### LOCKED ABILITIES #######
			(assign, ":continue", 0),
			(store_add, ":last_slot", ce_obj_button_ability_list_start, 75),
			(try_for_range, ":slot_no", ce_obj_button_ability_list_start, ":last_slot"),
				(eq, ":continue", 0),
				(troop_slot_eq, PRES_OBJECTS, ":slot_no", ":object"),
				(assign, ":continue", 1),
				(store_sub, ":ability_no", ":slot_no", ce_obj_button_ability_list_start),
			(try_end),
			(eq, ":continue", 1),
			(troop_set_slot, PRES_OBJECTS, ce_val_selected_ability, ":ability_no"),
			(start_presentation, "prsnt_ce_character_abilities"),
			
		(else_try), ####### BUTTON - CLEAR ABILITIES #######
			(troop_slot_eq, PRES_OBJECTS, ce_obj_button_clear_abilities, ":object"),
			(try_for_range, ":ability_slot", abilities_begin, abilities_end),
				(troop_set_slot, "trp_player", ":ability_slot", BONUS_UNASSIGNED),
			(try_end),
			(display_message, "@All of your abilities have been reset to an unassigned state.", gpu_green),
			(start_presentation, "prsnt_ce_character_abilities"),
			
		(else_try), ####### ASSIGN AN ABILITY #######
			(assign, ":continue", 0),
			(try_for_range, ":slot_no", ce_obj_button_assign_ability, ce_obj_field_levels_start),
				(troop_slot_eq, PRES_OBJECTS, ":slot_no", ":object"),
				(assign, ":continue", 1),
				(store_sub, ":ability_slot", ":slot_no", ce_obj_button_assign_ability),
				(val_add, ":ability_slot", abilities_begin),
				(store_sub, ":assignment_level", ":slot_no", ce_obj_button_assign_ability),
				(val_add, ":assignment_level", 1),
				(val_mul, ":assignment_level", 5),
			(try_end),
			(eq, ":continue", 1),
			(troop_get_slot, ":ability_no", PRES_OBJECTS, ce_val_selected_ability),
			(troop_set_slot, "trp_player", ":ability_slot", ":ability_no"),
			(troop_set_slot, PRES_OBJECTS, ce_val_selected_ability, BONUS_UNASSIGNED),
			(try_begin),
				(neq, ":ability_no", BONUS_UNASSIGNED),
				(call_script, "script_ce_store_troop_ability_string_to_s31", "trp_player", ":ability_no"),
				(assign, reg31, ":assignment_level"),
				(display_message, "@You have selected {s31} as your level {reg31} ability.", gpu_green),
			(try_end),
			## QUEST HOOK (completion): qst_qp6_expanding_your_talents
			(try_begin),
				(check_quest_active, "qst_qp6_expanding_your_talents"),
				(quest_slot_eq, "qst_qp6_expanding_your_talents", slot_quest_current_state, QP6_EYT_BEGUN),
				(quest_slot_eq, "qst_qp6_expanding_your_talents", slot_quest_temp_slot, ":assignment_level"),  # This is the correct assignment.
				(call_script, "script_qp6_quest_expanding_your_talents", floris_quest_succeed),
			(try_end),
			(start_presentation, "prsnt_ce_character_abilities"),
			
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