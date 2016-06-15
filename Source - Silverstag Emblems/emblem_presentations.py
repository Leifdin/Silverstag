# Silverstag Emblems by Windyplains

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
#####                                              EMBLEM INFORMATION                                                 #####
###########################################################################################################################

("pep_emblem_info", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_pep_create_mode_switching_buttons"),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 515),
		
		## OBJ - CONTAINER+ - EMBLEM OPTIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt4_obj_container_1),
		
			(assign, ":pos_y", 475),
			(assign, ":y_line_step", 20),
			(assign, ":x_desc", 110),
			# (assign, ":y_option_step", 70),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@The cost of hiring troops for your garrison at this location "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
		(set_container_overlay, -1), ## CONTAINER- - EMBLEM OPTIONS

      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_pep_handle_mode_switching_buttons", ":object", ":value"),
    ]),
  ]),
  

###########################################################################################################################
#####                                              CHARACTER RESETS                                                   #####
###########################################################################################################################

("pep_character_resets", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_pep_create_mode_switching_buttons"),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 515),
		
		## OBJ - CONTAINER+ - EMBLEM OPTIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt4_obj_container_1),
			
			(assign, ":pos_y", 475),
			(assign, ":y_line_step", 20),
			(assign, ":x_desc", 110),
			(assign, ":y_option_step", 70),
			
			# Dynamic Pos_Y setting based on space actually used.
			(store_mul, ":spacing_line_steps", ":y_line_step", 17),
			(store_mul, ":spacing_option_steps", ":y_option_step", 5),
			(store_add, ":pos_y", ":spacing_line_steps", ":spacing_option_steps"),
			
			##############################
			# OPTION - RESET ATTRIBUTES  #
			##############################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Reset Attributes"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep2_obj_option_reset_attributes, EMBLEM_COST_PLAYER_RESET_ATTRIBUTES), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Using this option will reset all of your character"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@strength, agility & charisma attributes to a value of"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@4 with any excess beyond that refunded as unspent points."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			##########################
			# OPTION - RESET SKILLS  #
			##########################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Reset Skills"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep2_obj_option_reset_skills, EMBLEM_COST_PLAYER_RESET_SKILLS), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Using this option will reset all of your character's"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@skills to a value of 0 with any excess beyond that"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@refunded as unspent points.  Intelligence is also reset."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			#################################
			# OPTION - RESET PROFICIENCIES  #
			#################################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Reset Weapon Proficiencies"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep2_obj_option_reset_proficiency, EMBLEM_COST_PLAYER_RESET_PROFICIENCIES), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Using this option will reset all of your character's"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@weapon proficiencies to a value of 25 with any excess "),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@beyond that refunded as unspent points.  This is not an"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@exact process due to diminishing returns."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			#############################
			# OPTION - RESET ABILITIES  #
			#############################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Reset Character Abilities"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep2_obj_option_reset_abilities, EMBLEM_COST_PLAYER_RESET_ABILITIES), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Using this option will clear all of your character's"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@abilities and allow them to be chosen again up to your"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@previous level."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			##################################
			# OPTION - FULL CHARACTER RESET  #
			##################################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Reset Everything"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep2_obj_option_full_retcon, EMBLEM_COST_PLAYER_FULL_RETCON), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Using this option will clear all of your character's"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@attributes, skills, proficiencies and abilities as if"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@you had chosen the option for each individually."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
		(set_container_overlay, -1), ## CONTAINER- - EMBLEM OPTIONS

      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_pep_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### BUTTON - OPTION (Reset Attributes) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep2_obj_option_reset_attributes, ":object"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_PLAYER_RESET_ATTRIBUTES), # emblem_scripts.py
			(call_script, "script_emblem_reset_troop_attributes", "trp_player"),
			(start_presentation, "prsnt_pep_character_resets"),
			
		(else_try),  ####### BUTTON - OPTION (Reset Skills) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep2_obj_option_reset_skills, ":object"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_PLAYER_RESET_SKILLS), # emblem_scripts.py
			(call_script, "script_emblem_reset_troop_skills", "trp_player"),
			(start_presentation, "prsnt_pep_character_resets"),
			
		(else_try),  ####### BUTTON - OPTION (Reset Proficiencies) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep2_obj_option_reset_proficiency, ":object"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_PLAYER_RESET_PROFICIENCIES), # emblem_scripts.py
			(call_script, "script_emblem_reset_troop_proficiencies", "trp_player"),
			(start_presentation, "prsnt_pep_character_resets"),
			
		(else_try),  ####### BUTTON - OPTION (Reset Abilities) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep2_obj_option_reset_abilities, ":object"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_PLAYER_RESET_ABILITIES), # emblem_scripts.py
			(call_script, "script_ce_reset_troop_abilities", "trp_player"), # combat_scripts.py
			(start_presentation, "prsnt_pep_character_resets"),
			
		(else_try),  ####### BUTTON - OPTION (Full Character Reset) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep2_obj_option_full_retcon, ":object"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_PLAYER_FULL_RETCON), # emblem_scripts.py
			(call_script, "script_emblem_reset_troop_attributes", "trp_player"),
			(call_script, "script_emblem_reset_troop_skills", "trp_player"),
			(call_script, "script_emblem_reset_troop_proficiencies", "trp_player"),
			(call_script, "script_ce_reset_troop_abilities", "trp_player"), # combat_scripts.py
			(start_presentation, "prsnt_pep_character_resets"),
			
		(try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                            CHARACTER DEVELOPMENT                                                #####
###########################################################################################################################

("pep_character_development", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_pep_create_mode_switching_buttons"),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 515),
		
		## OBJ - CONTAINER+ - EMBLEM OPTIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt4_obj_container_1),
		
			(assign, ":pos_y", 475),
			(assign, ":y_line_step", 20),
			(assign, ":x_desc", 110),
			(assign, ":y_option_step", 70),
			
			############################
			# OPTION - GAIN ATTRIBUTE  #
			############################
			(val_sub, ":pos_y", ":y_option_step"),
			(troop_get_slot, ":usage_cost", METRICS_DATA, metrics_attributes_upgraded),
			(val_add, ":usage_cost", 3),
			(val_clamp, ":usage_cost", 3, 21),
			(str_store_string, s21, "@Gain Attribute Point"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep3_obj_option_gain_attribute, ":usage_cost"), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Your character gains one extra unassigned attribute point"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@that you may spend as desired.  The cost of this option"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@scales upward with each purchase."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(troop_get_slot, reg21, METRICS_DATA, metrics_attributes_upgraded),
			(store_sub, reg22, reg21, 1),
			(str_store_string, s21, "@Status: You have used this option {reg21} time{reg22?s:}."),
			(val_sub, ":pos_y", 25),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			##############################
			# OPTION - GAIN SKILL POINT  #
			##############################
			(val_sub, ":pos_y", ":y_option_step"),
			(troop_get_slot, ":usage_cost", METRICS_DATA, metrics_skills_upgraded),
			(val_div, ":usage_cost", 2),
			(val_add, ":usage_cost", 2),
			(val_clamp, ":usage_cost", 2, 11),
			(str_store_string, s21, "@Gain Skill Point"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep3_obj_option_gain_skill, ":usage_cost"), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Your character gains one extra unassigned skill point"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@that you may spend as desired.  The cost of this option"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@scales upward with each purchase."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(troop_get_slot, reg21, METRICS_DATA, metrics_skills_upgraded),
			(store_sub, reg22, reg21, 1),
			(str_store_string, s21, "@Status: You have used this option {reg21} time{reg22?s:}."),
			(val_sub, ":pos_y", 25),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			
			##############################
			# OPTION - GAIN PROFICIENCY  #
			##############################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Gain Proficiency Points"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep3_obj_option_gain_proficiency, EMBLEM_COST_PLAYER_ADD_PROFICIENCY), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Your character gains 15 extra unassigned proficiency"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@points that you may spend as desired."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
		(set_container_overlay, -1), ## CONTAINER- - EMBLEM OPTIONS

      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_pep_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### BUTTON - OPTION (Gain Attribute Point) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep3_obj_option_gain_attribute, ":object"),
			# Determine emblem cost
			(troop_get_slot, ":usage_cost", METRICS_DATA, metrics_attributes_upgraded),
			(val_add, ":usage_cost", 3),
			(val_clamp, ":usage_cost", 3, 21),
			(call_script, "script_cf_emblem_spend_emblems", ":usage_cost"), # emblem_scripts.py
			(display_message, "@You have gained 1 attribute point.", gpu_green),
			# Apply new attribute point
			(troop_get_attribute_points, ":points", "trp_player"),
			(val_add, ":points", 1),
			(troop_set_attribute_points, "trp_player", ":points"),
			# Update Metric
			(troop_get_slot, reg21, METRICS_DATA, metrics_attributes_upgraded),
			(val_add, reg21, 1),
			(troop_set_slot, METRICS_DATA, metrics_attributes_upgraded, reg21),
			(start_presentation, "prsnt_pep_character_development"),
			
		(else_try),  ####### BUTTON - OPTION (Gain Skill Point) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep3_obj_option_gain_skill, ":object"),
			# Determine emblem cost
			(troop_get_slot, ":usage_cost", METRICS_DATA, metrics_skills_upgraded),
			(val_div, ":usage_cost", 2),
			(val_add, ":usage_cost", 2),
			(val_clamp, ":usage_cost", 2, 11),
			(call_script, "script_cf_emblem_spend_emblems", ":usage_cost"), # emblem_scripts.py
			(display_message, "@You have gained 1 skill point.", gpu_green),
			# Apply new skill point
			(troop_get_skill_points, ":points", "trp_player"),
			(val_add, ":points", 1),
			(troop_set_skill_points, "trp_player", ":points"),
			# Update Metric
			(troop_get_slot, reg21, METRICS_DATA, metrics_skills_upgraded),
			(val_add, reg21, 1),
			(troop_set_slot, METRICS_DATA, metrics_skills_upgraded, reg21),
			(start_presentation, "prsnt_pep_character_development"),
			
		(else_try),  ####### BUTTON - OPTION (Gain Proficiency Points) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep3_obj_option_gain_proficiency, ":object"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_PLAYER_ADD_PROFICIENCY), # emblem_scripts.py
			(display_message, "@You have gained 15 points of weapon proficiency.", gpu_green),
			# Apply new proficiency points
			(troop_get_proficiency_points, ":points", "trp_player"),
			(val_add, ":points", 15),
			(troop_set_proficiency_points, "trp_player", ":points"),
			(start_presentation, "prsnt_pep_character_development"),
			
		(try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                            CHARACTER DEVELOPMENT                                                #####
###########################################################################################################################

("pep_misc_options", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_pep_create_mode_switching_buttons"),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 515),
		
		## OBJ - CONTAINER+ - EMBLEM OPTIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt4_obj_container_1),
		
			(assign, ":pos_y", 475),
			(assign, ":y_line_step", 20),
			(assign, ":x_desc", 110),
			(assign, ":y_option_step", 70),
			
			#################################
			# OPTION - FINISH CURRENT BOOK  #
			#################################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Finish Current Book"),
			(call_script, "script_emblem_add_option_header", "str_hub_s21", ":pos_y", pep4_obj_option_finish_book, EMBLEM_COST_FINISH_BOOK_PLAYER), # emblem_scripts.py
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@Using this will return you to the world map in order to"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@instantly finish the book you're currently reading.  If you"),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(str_store_string, s21, "@are not currently reading one this will not work."),
			(val_sub, ":pos_y", ":y_line_step"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			## OBJ - TEXT - TEXT LINE
			(try_begin), # Filter - Is any book being read?
				(neg|is_between, "$g_player_reading_book", readable_books_begin, readable_books_end),
				(str_store_string, s21, "@Status: You are not currently reading a book."),
			(else_try),  # Filter - Does the player currently have this book?
				(neg|player_has_item, "$g_player_reading_book"),
				(str_store_item_name, s21, "$g_player_reading_book"),
				(str_store_string, s21, "@Status: You do not currently possess {s21}."),
			(else_try),  # Filter - Is this book finished already?
				(item_slot_ge, "$g_player_reading_book", slot_item_book_reading_progress, 1000),
				(str_store_item_name, s21, "$g_player_reading_book"),
				(str_store_string, s21, "@Status: You have already read {s21}."),
			(else_try),  # Filter - Is this book nearly finished already?
				(item_slot_ge, "$g_player_reading_book", slot_item_book_reading_progress, 995),
				(str_store_item_name, s21, "$g_player_reading_book"),
				(item_get_slot, ":progress", "$g_player_reading_book", slot_item_book_reading_progress),
				(store_div, reg21, ":progress", 10),
				(store_mod, reg22, ":progress", 10),
				(str_store_string, s21, "@Status: You almost finished with {s21}. ({reg21}.{reg22}%)"),
			(else_try),  # Default - Display book being read and current progress.
				(str_store_item_name, s21, "$g_player_reading_book"),
				(item_get_slot, ":progress", "$g_player_reading_book", slot_item_book_reading_progress),
				(store_div, reg21, ":progress", 10),
				(store_mod, reg22, ":progress", 10),
				(str_store_string, s21, "@Status: You are reading {s21}. ({reg21}.{reg22}%)"),
			(try_end),
			(val_sub, ":pos_y", 25),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(str_store_string, s21, "@Status:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_desc", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			
		(set_container_overlay, -1), ## CONTAINER- - EMBLEM OPTIONS

      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_pep_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### BUTTON - OPTION (Finish Current Book) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep4_obj_option_finish_book, ":object"),
			# Filter out inappropriate status values.
			(try_begin), # FILTER - Is any book being read?
				(neg|is_between, "$g_player_reading_book", readable_books_begin, readable_books_end),
				(display_message, "@Warning - You are not currently reading a book.", gpu_red),
			(else_try),  # FILTER - Does the player currently have this book?
				(neg|player_has_item, "$g_player_reading_book"),
				(str_store_item_name, s21, "$g_player_reading_book"),
				(display_message, "@Warning - You do not currently possess {s21}.", gpu_red),
			(else_try),  # FILTER - Is this book finished already?
				(item_slot_ge, "$g_player_reading_book", slot_item_book_reading_progress, 1000),
				(str_store_item_name, s21, "$g_player_reading_book"),
				(display_message, "@Warning - You have already finished reading {s21}.", gpu_red),
			(else_try),  # SUCCESS - Instantly finish reading the book.
				(item_set_slot, "$g_player_reading_book", slot_item_book_reading_progress, 999),
				(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_FINISH_BOOK_PLAYER), # emblem_scripts.py
				(change_screen_map),
				(rest_for_hours_interactive, 2, 5, 0),
			(try_end),
			(start_presentation, "prsnt_pep_misc_options"),
			
		(try_end),
    ]),
  ]),
  
  
###########################################################################################################################
#####                                                  DEBUGGING                                                      #####
###########################################################################################################################

("pep_debugging", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_pep_create_mode_switching_buttons"),
		
		(assign, ":y_bottom", 80),
		(assign, ":x_left",  250),
		(assign, ":x_width", 700),
		(assign, ":y_width", 515),
		
		## OBJ - CONTAINER+ - EMBLEM OPTIONS
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - Footer
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", grt4_obj_container_1),
		
			(assign, ":pos_y", 475),
			# (assign, ":y_line_step", 20),
			# (assign, ":x_desc", 110),
			(assign, ":y_option_step", 70),
			
			(val_sub, ":pos_y", 100),
			
			#########################
			# OPTION - GAIN EMBLEM  #
			#########################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Gain 1 Emblem"),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 250, ":pos_y", pep5_obj_option_gain_emblem),
			
			#########################
			# OPTION - LOSE EMBLEM  #
			#########################
			(val_sub, ":pos_y", ":y_option_step"),
			(str_store_string, s21, "@Remove 1 Emblem"),
			(call_script, "script_gpu_create_game_button", "str_hub_s21", 250, ":pos_y", pep5_obj_option_lose_emblem),
			
			
			
		(set_container_overlay, -1), ## CONTAINER- - EMBLEM OPTIONS

      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_pep_handle_mode_switching_buttons", ":object", ":value"),
		
		(try_begin),  ####### BUTTON - OPTION (Gain 1 Emblem) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep5_obj_option_gain_emblem, ":object"),
			(call_script, "script_emblem_award_to_player", 1),
			(start_presentation, "prsnt_pep_debugging"),
			
		(else_try),  ####### BUTTON - OPTION (Lose 1 Emblem) #######
			(troop_slot_eq, EMBLEM_OBJECTS, pep5_obj_option_lose_emblem, ":object"),
			(call_script, "script_cf_emblem_spend_emblems", 1),
			(start_presentation, "prsnt_pep_debugging"),
			
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