# Dynamic Troop Trees by Dunde, modified by Caba'drin.

from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
# from header_items import *   # Added for Show all Items presentation.
# from module_items import *   # Added for Show all Items presentation.
from header_skills import *

import string

####################################################################################################################
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################

presentations = [
   
  ("troop_note", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		(assign, "$gpu_storage", VAT_OBJECTS),
		(assign, "$gpu_data",    VAT_OBJECTS),
		
		## init troop items
        (call_script, "script_copy_inventory", "$temp", "trp_temp_array_a"),
        (try_for_range, ":i_slot", 0, 10),
          (troop_get_inventory_slot, ":item", "trp_temp_array_a", ":i_slot"),
          (gt, ":item", -1),
          (troop_add_item,"trp_temp_array_a",":item"),
          (troop_set_inventory_slot, "trp_temp_array_a", ":i_slot", -1),
        (try_end),
		
		## OBJ - BUTTON - DONE
		(str_store_string, s21, "@Done"),
        (call_script, "script_gpu_create_game_button", "str_hub_s21", 500, 35, insp_obj_button_done),
		
		## OBJ - TROOP IMAGE
		(call_script, "script_gpu_create_troop_image", "$temp", 75, 420, 900, insp_obj_portrait_troop),
		
		## OBJ - LABEL - TROOP NAME
		(str_store_troop_name, s21, "$temp"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", 210, 410, 0, gpu_center),
		(overlay_set_color, reg1, gpu_blue),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 210, 410, 0, gpu_center),
		(overlay_set_color, reg1, gpu_blue),
		
		## OBJ - LABEL - TROOP CLASS
		(troop_get_class, ":class", "$temp"),
		(try_begin),
			(eq, ":class", 0),
			(str_store_string, s21, "@Infantry Unit"),
		(else_try),
			(eq, ":class", 1),
			(str_store_string, s21, "@Ranged Unit"),
		(else_try),
			(eq, ":class", 2),
			(str_store_string, s21, "@Cavalry Unit"),
		(else_try),
			(assign, reg31, ":class"),
			(str_store_string, s21, "@Undefined Class #{reg31}"),
		(try_end),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 210, 392, 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		
		###################################
		#### PREREQUISITES / ABILITIES ####
		###################################
		
		(assign, ":pos_y", 345),
		(assign, ":pos_x", 50),
		(assign, ":y_step_line", 25),
		(store_add, ":pos_x_col_2", ":pos_x", 30),
		(store_add, ":pos_x_col_3", ":pos_x_col_2", 80),
		# (store_add, ":pos_x_col_4", ":pos_x", 75),
		
		## OBJ - LABEL - PREREQUISITES
		(str_store_string, s21, "@Prerequisites:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		
		## OBJ - LABEL - PREREQUISITE 1
		(val_sub, ":pos_y", ":y_step_line"),
		(call_script, "script_trees_stamp_requirement_info", "$temp", slot_troop_requirement_1, ":pos_x", ":pos_y"),
		
		## OBJ - LABEL - PREREQUISITE 2
		(val_sub, ":pos_y", ":y_step_line"),
		(call_script, "script_trees_stamp_requirement_info", "$temp", slot_troop_requirement_2, ":pos_x", ":pos_y"),
		
		## OBJ - LABEL - PREREQUISITE 3
		(val_sub, ":pos_y", ":y_step_line"),
		(call_script, "script_trees_stamp_requirement_info", "$temp", slot_troop_requirement_3, ":pos_x", ":pos_y"),
		
		## OBJ - LABEL - PREREQUISITE 4
		(val_sub, ":pos_y", ":y_step_line"),
		(call_script, "script_trees_stamp_requirement_info", "$temp", slot_troop_requirement_4, ":pos_x", ":pos_y"),
		
		## OBJ - LABEL - ABILITIES
		(val_sub, ":pos_y", ":y_step_line"),
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Abilities:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		
		## OBJ - LABEL - ABILITY 1
		(val_sub, ":pos_y", ":y_step_line"),
		(call_script, "script_trees_stamp_ability_info", "$temp", slot_troop_ability_1, ":pos_x", ":pos_y"),
		
		## OBJ - LABEL - ABILITY 2
		(val_sub, ":pos_y", ":y_step_line"),
		(call_script, "script_trees_stamp_ability_info", "$temp", slot_troop_ability_2, ":pos_x", ":pos_y"),
		
		## OBJ - LABEL - ABILITY 3
		(val_sub, ":pos_y", ":y_step_line"),
		(call_script, "script_trees_stamp_ability_info", "$temp", slot_troop_ability_3, ":pos_x", ":pos_y"),
		
		## OBJ - LABEL - ABILITY 4
		(val_sub, ":pos_y", ":y_step_line"),
		(call_script, "script_trees_stamp_ability_info", "$temp", slot_troop_ability_4, ":pos_x", ":pos_y"),
		
		
		####################
		#### STATISTICS ####
		####################
		
		(assign, ":pos_y", 625),
		(assign, ":pos_x", 430),
		(assign, ":y_step_line", 25),
		(store_add, ":pos_x_col_2", ":pos_x", 140),
		(store_add, ":pos_x_col_3", ":pos_x_col_2", 50),
		(store_add, ":pos_x_col_4", ":pos_x_col_3", 140),
				
		## OBJ - LABEL - GENERAL INFO
		(str_store_string, s21, "@General Information:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		
		## OBJ - LABEL - TIER
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Tier:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(troop_get_slot, reg21, "$temp", slot_troop_tier),
		(str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - ARMOR RATING
		(str_store_string, s21, "@Armor Rating:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_hub_troop_get_armor_rating", "$temp"), # Returns armor rating to reg1
		(str_store_string, s21, "@{reg1}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - LEVEL
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Level:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_character_level, reg21, "$temp"),
		(str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - MELEE RATING
		(str_store_string, s21, "@Melee Rating:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_hub_troop_get_melee_rating", "$temp"), # Returns melee rating to reg1
		(str_store_string, s21, "@{reg1}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - HEALTH
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Health:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_get_troop_max_hp", "$temp"),
		(str_store_string, s21, "@{reg0}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - RANGED RATING
		(str_store_string, s21, "@Ranged Rating:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_hub_troop_get_ranged_rating", "$temp"), # Returns ranged rating to reg1
		(str_store_string, s21, "@{reg1}"),
		(try_begin),
			(eq, reg1, 0),
			(str_store_string, s21, "@None"),
		(try_end),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - RECRUIT TYPE
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Recruit:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_get_troop_max_hp", "$temp"),
		(try_begin),
			(troop_slot_eq, "$temp", slot_troop_recruit_type, STRT_NOBLEMAN),
			(str_store_string, s22, "@Veteran"),
		(else_try),
			(troop_slot_eq, "$temp", slot_troop_recruit_type, STRT_MERCENARY),
			(str_store_string, s22, "@Mercenary"),
		(else_try),
			(str_store_string, s22, "@Peasant"),
		(try_end),
		(str_store_string, s21, "@{s22}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - PURCHASE COST
		(str_store_string, s21, "@Cost:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_hub_troop_get_melee_rating", "$temp"), # Returns melee rating to reg1
		(troop_get_slot, reg21, "$temp", slot_troop_purchase_cost),
		(str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - GUARANTEED RANGED
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Ranged:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(try_begin),
			(troop_is_guarantee_ranged, "$temp"),
			(str_store_string, s21, "@Yes"),
		(else_try),
			(str_store_string, s21, "@No"),
		(try_end),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - GUARANTEED MOUNT
		(str_store_string, s21, "@Mounted:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(try_begin),
			(troop_is_guarantee_horse, "$temp"),
			(str_store_string, s21, "@Yes"),
		(else_try),
			(str_store_string, s21, "@No"),
		(try_end),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - ATTRIBUTES
		(val_sub, ":pos_y", ":y_step_line"),
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Attributes:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		
		## OBJ - LABEL - STRENGTH
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Strength:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_attribute_level, reg21, "$temp", ca_strength),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - INTELLIGENCE
		(str_store_string, s21, "@Intelligence:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_attribute_level, reg21, "$temp", ca_intelligence),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - AGILITY
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Agility:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_attribute_level, reg21, "$temp", ca_agility),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - CHARISMA
		(str_store_string, s21, "@Charisma:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_attribute_level, reg21, "$temp", ca_charisma),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - SKILLS
		(val_sub, ":pos_y", ":y_step_line"),
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Skills:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		
		## OBJ - LABEL - POWER STRIKE
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Power Strike:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_power_strike, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - IRONFLESH
		(str_store_string, s21, "@Ironflesh:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_ironflesh, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - POWER DRAW
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Power Draw:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_power_draw, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - SHIELD
		(str_store_string, s21, "@Shield:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_shield, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - POWER THROW
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Power Throw:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_power_throw, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - ATHLETICS
		(str_store_string, s21, "@Athletics:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_athletics, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - HORSE ARCHERY
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Horse Archery:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_horse_archery, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - RIDING
		(str_store_string, s21, "@Riding:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_riding, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - TACTICS
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Tactics:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_tactics, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - WEAPON MASTERY
		(str_store_string, s21, "@Weapon Master:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_skill_level, reg21, skl_weapon_master, "$temp"),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		
		## OBJ - LABEL - WEAPON PROFICIENCIES
		(val_sub, ":pos_y", ":y_step_line"),
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Weapon Proficiencies:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		
		## OBJ - LABEL - One Handed Proficiency
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@One Handed:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_proficiency_level, reg21, "$temp", wpt_one_handed_weapon),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - Archery
		(str_store_string, s21, "@Archery:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_proficiency_level, reg21, "$temp", wpt_archery),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - Two Handed Proficiency
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Two Handed:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_proficiency_level, reg21, "$temp", wpt_two_handed_weapon),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - Crossbows
		(str_store_string, s21, "@Crossbows:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_proficiency_level, reg21, "$temp", wpt_crossbow),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - Polearms
		(val_sub, ":pos_y", ":y_step_line"),
		(str_store_string, s21, "@Polearms:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_proficiency_level, reg21, "$temp", wpt_polearm),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - LABEL - Throwing
		(str_store_string, s21, "@Throwing:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_3", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(store_proficiency_level, reg21, "$temp", wpt_throwing),
        (str_store_string, s21, "@{reg21}"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_4", ":pos_y", 0, gpu_right),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		###################
		#### INVENTORY ####
		###################
		
		## OBJ - LABEL - EQUIPMENT:
		(str_store_string, s21, "@Equipment:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", 790, 625, 0, gpu_left),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 790, 625, 0, gpu_left),
		
		## OBJ - INVENTORY CONTAINER
		(call_script, "script_gpu_container_heading", 790, 50, 160, 560, insp_obj_container_inventory),
		
			(assign, ":pos_x", 0),
			(assign, ":pos_y", 1840),
			(assign, ":slot_no", 10),
			(try_for_range, ":unused_height", 0, 48), # 24),
				(try_for_range, ":unused_width", 0, 2), # 4),
					(create_mesh_overlay, reg1, "mesh_inv_slot"),
					(position_set_x, pos1, 800),
					(position_set_y, pos1, 800),
					(overlay_set_size, reg1, pos1),
					(position_set_x, pos1, ":pos_x"),
					(position_set_y, pos1, ":pos_y"),
					(overlay_set_position, reg1, pos1),
					(troop_set_slot, "trp_temp_array_a", ":slot_no", reg1),
					(troop_get_inventory_slot, ":item_no", "trp_temp_array_a", ":slot_no"),
					(try_begin),
						(gt, ":item_no", -1),
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
					(try_end),
					(val_add, ":pos_x", 80),
					(val_add, ":slot_no", 1),
				(try_end),
				(assign, ":pos_x", 0),
				(val_sub, ":pos_y", 80),
			(try_end),

        (set_container_overlay, -1),
		
      ]),

    (ti_on_presentation_mouse_enter_leave,
      [
		(store_trigger_param_1, ":object"),
		(store_trigger_param_2, ":enter_leave"),

		(try_begin),
			(eq, ":enter_leave", 0),
			(try_for_range, ":slot_no", 10, 106),
				(troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
				(troop_get_inventory_slot, ":item_no", "trp_temp_array_a", ":slot_no"),
				(try_begin),
					(gt, ":item_no", -1),
					(troop_get_slot, ":target_obj", "trp_temp_array_b", ":slot_no"),
					(overlay_get_position, pos0, ":target_obj"),
					(show_item_details, ":item_no", pos0, 100),
					(assign, "$g_current_opened_item_details", ":slot_no"),
				(try_end),
			(try_end),
		(else_try),
			(try_for_range, ":slot_no", 10, 106),
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

        (try_begin),
			### BUTTON - DONE ###
			(troop_slot_eq, VAT_OBJECTS, vat_obj_button_done, ":object"),
			(try_begin),
				(eq, "$g_presentation_next_presentation", "prsnt_hub_recruitment"),
				(assign, "$g_presentation_next_presentation", -1),
				(assign, "$hub_mode", HUB_MODE_RECRUITMENT),
				(presentation_set_duration, 0),
				(jump_to_menu, "mnu_hub_switch_modes"),
			(else_try),
				(eq, "$g_presentation_next_presentation", "prsnt_garrison_recruitment"),
				(assign, "$g_presentation_next_presentation", -1),
				(assign, "$grt_mode", GARRISON_MODE_RECRUITMENT),
				(presentation_set_duration, 0),
				(jump_to_menu, "mnu_garrison_switch_modes"),
			(else_try),
				(eq, "$g_presentation_next_presentation", "prsnt_all_troops"),
				(assign, "$g_presentation_next_presentation", -1),
				(assign, "$hub_mode", VAT_MODE_TREE_DISPLAY),
				(presentation_set_duration, 0),
				(jump_to_menu, "mnu_troop_tree_switch_modes"),
			(else_try),
				(presentation_set_duration, 0),
			(try_end),
        (try_end),
    ]),
  ]),    

## WINDYPLAINS+ ## - Show all troops
("all_troops", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(assign, "$gpu_storage", VAT_OBJECTS),
		(assign, "$gpu_data",    VAT_OBJECTS),
		
		## OBJ - COMBO LABEL - REGION SELECTOR
        (create_combo_label_overlay, "$vai_region_selector"),
        (position_set_x, pos1, 500),
        (position_set_y, pos1, 675),
        (overlay_set_position, "$vai_region_selector", pos1),
        (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
			# (neq, ":kingdom_no", "fac_player_supporters_faction"),
			(str_store_faction_name, s21, ":kingdom_no"),
			(try_begin),
				(eq, ":kingdom_no", "fac_player_supporters_faction"),
				(str_store_string, s21, "@Player Faction"),
			(try_end),
			(overlay_add_item, "$vai_region_selector", "@{s21}"),
		(try_end),
		(overlay_add_item, "$vai_region_selector", "@Bandits"),
		(overlay_set_val, "$vai_region_selector", "$vai_region_value"),
		
		## OBJ - CREDITS DISPLAY
		(assign, ":pos_x_temp", 950),
		(assign, ":pos_y_temp", 690),
		(try_begin),
			(eq, "$vai_region_value", 1),
			(str_store_string, s21, "@Faction Design^by Leifdin"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
		(else_try),
			(eq, "$vai_region_value", 2),
			(str_store_string, s21, "@Faction Design^by Huillam"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
		(else_try),
			(eq, "$vai_region_value", 3),
			(str_store_string, s21, "@Faction Design^by Huillam & Leifdin"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
		(else_try),
			(eq, "$vai_region_value", 4),
			(str_store_string, s21, "@Faction Design^by Leifdin"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
		(else_try),
			(eq, "$vai_region_value", 5),
			(str_store_string, s21, "@Faction Design^by Dawg of War"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", 0, gpu_right),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
		
		## LOGIC - Determine starting & ending troops for display.
		## FACTION TROOPS
		(try_begin),
			(assign, ":faction_counter", 0),
			(eq, "$vai_region_value", ":faction_counter"), # Player Custom Faction
			(assign, ":culture", "fac_culture_player"),
		(else_try),
			(val_add, ":faction_counter", 1),
			(eq, "$vai_region_value", ":faction_counter"), # Swadia
			(assign, ":culture", "fac_culture_1"),
		(else_try),
			(val_add, ":faction_counter", 1),
			(eq, "$vai_region_value", ":faction_counter"), # Vaegirs
			(assign, ":culture", "fac_culture_2"),
		(else_try),
			(val_add, ":faction_counter", 1),
			(eq, "$vai_region_value", ":faction_counter"), # Khergits
			(assign, ":culture", "fac_culture_3"),
		(else_try),
			(val_add, ":faction_counter", 1),
			(eq, "$vai_region_value", ":faction_counter"), # Nords
			(assign, ":culture", "fac_culture_4"),
		(else_try),
			(val_add, ":faction_counter", 1),
			(eq, "$vai_region_value", ":faction_counter"), # Rhodoks
			(assign, ":culture", "fac_culture_5"),
		(else_try),
			(val_add, ":faction_counter", 1),
			(eq, "$vai_region_value", ":faction_counter"), # Sarranid
			(assign, ":culture", "fac_culture_6"),
		(else_try),
			(val_add, ":faction_counter", 1),
			(eq, "$vai_region_value", ":faction_counter"), # Bandits
			(assign, ":culture", "fac_outlaws"),
		(try_end),
		
		## OBJ - BUTTON - DONE
		(str_store_string, s21, "@Done"),
        (call_script, "script_gpu_create_game_button", "str_hub_s21", 500, 40, vat_obj_button_done),
		
		## LOGIC - SPACING DEFINITIONS
		(assign, ":y_bottom", 105),
		(assign, ":x_left",  70),
		(assign, ":x_width", 860),
		(assign, ":y_width", 500),
		(assign, ":y_step", 85),
		(assign, ":x_step", 65),
		(assign, ":portrait_size", 250),
		
		## OBJ - LABEL - TIER HEADER
		(try_for_range, ":tier_cycle", 1, 11),
			(store_mul, ":x_tier_title", ":tier_cycle", ":x_step"),
			(val_add, ":x_tier_title", 230),
			(assign, reg21, ":tier_cycle"),
			(str_store_string, s21, "@TIER {reg21}"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_tier_title", 640, 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
		
		## OBJ - LINE - TIER FOOTER
		(call_script, "script_gpu_draw_line", 850, 2, 73, 620, gpu_gray), # - Footer
		
		## OBJ - MAIN CONTAINER
		# (call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left", ":y_bottom", gpu_white), # - TESTING BACKGROUND
		(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", vat_obj_container_1),
			
			(assign, ":total_records", 0),
			(try_for_range, ":troop_no", troop_definitions_begin, troop_definitions_end),
				# Filter - Remove heroes & data arrays.
				(neg|troop_is_hero, ":troop_no"),
				(call_script, "script_cf_troop_is_non_array", ":troop_no"), # Module_scripts.py
				(assign, ":unique_culture", -1),
				(try_begin),
					(troop_get_slot, ":unique_location", ":troop_no", slot_troop_unique_location),
					(is_between, ":unique_location", centers_begin, centers_end),
					(party_get_slot, ":unique_culture", ":unique_location", slot_center_culture),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION_UPGRADE),
					(assign, ":unique_culture", -1), # Don't show veteran / elite uniques.
				(try_end),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_1, ":culture"),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_2, ":culture"),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_3, ":culture"),
				(eq, ":unique_culture", ":culture"), # For unique troops.
				(val_add, ":total_records", 1),
			(try_end),
			(store_mul, ":pos_y", ":total_records", ":y_step"),
			(val_add, ":pos_y", 40),
			
			(assign, ":x1", 0),
			(assign, ":record", 0),
			(store_sub, ":max_records", vat_val_troop_record, vat_obj_troop_image),
			
			(try_for_range, ":troop_no", troop_definitions_begin, troop_definitions_end),
				# Filter - Remove heroes & data arrays.
				(neg|troop_is_hero, ":troop_no"),
				(call_script, "script_cf_troop_is_non_array", ":troop_no"), # Module_scripts.py
				(assign, ":unique_culture", -1),
				(try_begin),
					(troop_get_slot, ":unique_location", ":troop_no", slot_troop_unique_location),
					(is_between, ":unique_location", centers_begin, centers_end),
					(party_get_slot, ":unique_culture", ":unique_location", slot_center_culture),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION_UPGRADE),
					(assign, ":unique_culture", -1), # Don't show veteran / elite uniques.
				(try_end),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_1, ":culture"),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_2, ":culture"),
				(this_or_next|troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_3, ":culture"),
				(eq, ":unique_culture", ":culture"), # For unique troops.
				(lt, ":record", ":max_records"),
				(ge, ":troop_no", 1),
				(call_script, "script_hub_determine_purchase_cost", ":troop_no"),
				
				## OBJ - LABEL - TROOP NAME
				(store_add, ":y1_troop_title", ":pos_y", -65),
				(store_add, ":x1_troop_title", ":x1", 10),
				(str_store_troop_name, s21, ":troop_no"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x1_troop_title", ":y1_troop_title", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x1_troop_title", ":y1_troop_title", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(try_begin),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION), 
					(assign, ":color", gpu_unique), # Goldish yellow.
					(overlay_set_color, reg1, ":color"),
				(else_try),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION_UPGRADE), 
					(assign, ":color", gpu_unique), # Goldish yellow.
					(overlay_set_color, reg1, ":color"),
				(else_try),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_AFFILIATED),
					(assign, ":color", gpu_affiliated), # Dark Blue
					(overlay_set_color, reg1, ":color"),
				(else_try),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_OWNER_ONLY),
					(assign, ":color", gpu_owner_only), # Goldish yellow.
					(overlay_set_color, reg1, ":color"),
				(else_try),
					(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_DISHONORABLE),
					(assign, ":color", gpu_dishonorable),
					(overlay_set_color, reg1, ":color"),
				(try_end),
				
				(store_add, ":pos_y_portrait", ":pos_y", -100),
				(troop_get_slot, ":tier", ":troop_no", slot_troop_tier),
				(store_mul, ":x1_portrait", ":tier", ":x_step"),
				(val_add, ":x1_portrait", 125),
				
				## OBJ - IMAGE BACKGROUND FOR DEBUGGING.
				(try_begin),
					(eq, "$show_autoloot_data", 1),
					(store_add, ":x2_portrait", ":x1_portrait", 18),
					(store_add, ":pos_y_portrait", ":pos_y", -100),
					(try_begin),
						(store_character_level, ":level", ":troop_no"),
						(troop_get_slot, ":tier_check", ":troop_no", slot_troop_tier),
						(val_mul, ":tier_check", 4),
						(neq, ":level", ":tier_check"),
						(call_script, "script_gpu_draw_line", 40, 65, ":x2_portrait", ":pos_y_portrait", gpu_red), # - TESTING BACKGROUND
						
						## OBJ - LABEL - BELOW TIER
						# (store_add, ":x_temp", ":x2", 35),
						# (store_add, ":y_temp", ":pos_y", -107),
						# (store_mul, ":minimum_value", ":upgraded_tier", 175),
						# (store_sub, reg21, reg65, ":minimum_value"),
						# (str_store_string, s21, "@{reg21}"),
						# (call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
						# (call_script, "script_gpu_resize_object", 0, 75),
					(try_end),
				(try_end),
				
				## OBJ - TROOP IMAGE
				(store_add, ":obj_slot", vat_obj_troop_image, ":record"),
				(call_script, "script_gpu_create_troop_image", ":troop_no", ":x1_portrait", ":pos_y_portrait", ":portrait_size", ":obj_slot"),
				(store_add, ":val_slot", vat_val_troop_record, ":record"),
				(troop_set_slot, VAT_OBJECTS, ":val_slot", ":troop_no"),
				
				(assign, ":x_adj_ability", 50),
				(assign, ":y_adj_ability", 5),
				(assign, ":x_adj_prereq", 20),
				(assign, ":y_adj_prereq", ":y_adj_ability"),
				
				## OBJ - LABEL - ABILITY COUNT (bottom right of image, blue font)
				(try_begin),
					(eq, "$show_autoloot_data", 1),
					(store_add, ":x_temp", ":x1_portrait", ":x_adj_ability"),
					(store_add, ":y_temp", ":pos_y_portrait", ":y_adj_ability"),
					(call_script, "script_ce_count_troop_abilities", ":troop_no"), # combat_scripts.py
					(str_store_string, s21, "@{reg1}"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, gpu_blue),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, gpu_blue),
				(try_end),
				
				## OBJ - LABEL - PREREQUISITE COUNT (bottom left of image, red font)
				(try_begin),
					(eq, "$show_autoloot_data", 1),
					(store_add, ":x_temp", ":x1_portrait", ":x_adj_prereq"),
					(store_add, ":y_temp", ":pos_y_portrait", ":y_adj_prereq"),
					(call_script, "script_ce_count_troop_prerequisites", ":troop_no"), # combat_scripts.py
					(str_store_string, s21, "@{reg1}"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, gpu_dark_red),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, gpu_dark_red),
				(try_end),
				
				(val_add, ":record", 1),
				
				## CHECK UPGRADE PATHS
				(assign, ":troop_prev", ":troop_no"),
				(store_add, ":x2", ":x1_portrait", ":x_step"),
				(store_add, ":line_x_left", ":x1_portrait", 51),
				(try_for_range, ":upgrades", 0, 6),
					(troop_get_upgrade_troop, ":troop_next", ":troop_prev", 0),
					(ge, ":troop_next", 1),
					(call_script, "script_hub_determine_purchase_cost", ":troop_next"),
					
					## OBJ - UPGRADE LINE
					(store_sub, ":line_x_width", ":x_step", 32),
					(store_add, ":line_y_bottom", ":pos_y", -65),
					(call_script, "script_gpu_draw_line", ":line_x_width", 1, ":line_x_left", ":line_y_bottom", gpu_gray), # - Upgrade path
					
					## OBJ - IMAGE BACKGROUND FOR DEBUGGING.
					(try_begin),
						(eq, "$show_autoloot_data", 1),
						(store_add, ":x2_portrait", ":x2", 18),
						(store_add, ":pos_y_portrait", ":pos_y", -100),
						(try_begin),
							(store_add, ":upgraded_tier", ":tier", ":upgrades"),
							(val_add, ":upgraded_tier", 1),
							(troop_get_slot, ":current_tier", ":troop_next", slot_troop_tier),
							(neq, ":current_tier", ":upgraded_tier"),
							(call_script, "script_gpu_draw_line", 40, 65, ":x2_portrait", ":pos_y_portrait", gpu_red), # - TESTING BACKGROUND
							
							## OBJ - LABEL - BELOW TIER
							(store_add, ":x_temp", ":x2", 35),
							(store_add, ":y_temp", ":pos_y", -107),
							(store_mul, ":minimum_value", ":upgraded_tier", 175),
							(store_sub, reg21, reg65, ":minimum_value"),
							(str_store_string, s21, "@{reg21}"),
							(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
							(call_script, "script_gpu_resize_object", 0, 75),
						(try_end),
					(try_end),
					
					## OBJ - TROOP IMAGE
					(store_add, ":x2_portrait", ":x2", 0),
					(store_add, ":obj_slot", vat_obj_troop_image, ":record"),
					(call_script, "script_gpu_create_troop_image", ":troop_next", ":x2_portrait", ":pos_y_portrait", ":portrait_size", ":obj_slot"),
					(store_add, ":val_slot", vat_val_troop_record, ":record"),
					(troop_set_slot, VAT_OBJECTS, ":val_slot", ":troop_next"),
					
					## OBJ - LABEL - ABILITY COUNT (bottom right of image, blue font)
					(try_begin),
						(eq, "$show_autoloot_data", 1),
						(store_add, ":x_temp", ":x2_portrait", ":x_adj_ability"),
						(store_add, ":y_temp", ":pos_y_portrait", ":y_adj_ability"),
						(call_script, "script_ce_count_troop_abilities", ":troop_next"), # combat_scripts.py
						(str_store_string, s21, "@{reg1}"),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
						(call_script, "script_gpu_resize_object", 0, 75),
						(overlay_set_color, reg1, gpu_blue),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
						(call_script, "script_gpu_resize_object", 0, 75),
						(overlay_set_color, reg1, gpu_blue),
					(try_end),
					
					## OBJ - LABEL - PREREQUISITE COUNT (bottom left of image, red font)
					(try_begin),
						(eq, "$show_autoloot_data", 1),
						(store_add, ":x_temp", ":x2_portrait", ":x_adj_prereq"),
						(store_add, ":y_temp", ":pos_y_portrait", ":y_adj_prereq"),
						(call_script, "script_ce_count_troop_prerequisites", ":troop_next"), # combat_scripts.py
						(str_store_string, s21, "@{reg1}"),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
						(call_script, "script_gpu_resize_object", 0, 75),
						(overlay_set_color, reg1, gpu_dark_red),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_temp", 0, gpu_center),
						(call_script, "script_gpu_resize_object", 0, 75),
						(overlay_set_color, reg1, gpu_dark_red),
					(try_end),
					
					(val_add, ":record", 1),
					(val_add, ":x2", ":x_step"),
					(val_add, ":line_x_left", ":x_step"),
					(assign, ":troop_prev", ":troop_next"),
				(try_end),
				
				(val_sub, ":pos_y", ":y_step"),
			(try_end),
			
        (set_container_overlay, -1),

      ]),

    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

        (try_begin),
        	## COMBO LABEL - REGION SELECTOR
			(eq, ":object", "$vai_region_selector"),
			(assign, "$vai_region_value", ":value"),
			(store_add, "$vai_region_kingdom", "$vai_region_value", kingdoms_begin),
			(start_presentation, "prsnt_all_troops"),
		
        (else_try),
			### BUTTON - DONE ###
			(troop_slot_eq, VAT_OBJECTS, vat_obj_button_done, ":object"),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_reference_reports"),
			
		(else_try),
			### BUTTON - INSPECT TROOP ###
			(try_for_range, ":record", vat_obj_troop_image, vat_val_troop_record), 
				(troop_slot_eq, VAT_OBJECTS, ":record", ":object"),
				(store_add, ":button_val_slot", 100, ":record"),
				(troop_get_slot, "$temp", VAT_OBJECTS, ":button_val_slot"),
				(assign, "$hub_mode", VAT_MODE_INSPECTION),
				(assign, "$g_presentation_next_presentation", "prsnt_all_troops"),
				(presentation_set_duration, 0),
				(jump_to_menu, "mnu_troop_tree_switch_modes"),
			(try_end),
			
        (try_end),
    ]),
]),
 
("add_troops", 0, mesh_load_window, [
	(ti_on_presentation_load,[
		(presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(assign, "$gpu_storage", VAT_OBJECTS),
		(assign, "$gpu_data",    VAT_OBJECTS),
		
		## TITLE
		(str_store_string, s21, "@Add Troops"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, ce_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", ce_obj_main_title, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, ce_obj_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", ce_obj_main_title, 150),

		
		
		## TROOP ID INUT BOX
		(str_store_string, s21, "@Troop ID"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 200, 580, gpu_left),
		(call_script, "script_gpu_create_text_box", 350, 580, vat_obj_text_input_troop_id),
		#(call_script, "script_gpu_resize_object", vat_obj_text_input_troop_id, 150),
		
		## TROOP COUNT INPUT BOX
		(str_store_string, s21, "@Troop Count"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 200, 500, gpu_left),
		(call_script, "script_gpu_create_number_box", 350, 500, 1, 100, vat_obj_number_box_troop_count, vat_val_troop_count),
		(call_script, "script_gpu_resize_object", vat_obj_number_box_troop_count, 150),
		
		## ADD TROOPS BUTTON
		(str_store_string, s21, "@Add Troops"),
		(call_script, "script_gpu_create_button", "str_hub_s21", 550, 490, vat_obj_button_add_troops),
		
		
		## DONE BUTTON ##
		(str_store_string, s21, "@Done"),
		(call_script, "script_gpu_create_game_button", "str_hub_s21", 500, 40, vat_obj_button_done),
	]),
	
	
	(ti_on_presentation_run, [
		(try_begin),
			(key_clicked, key_escape),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_cheat_reports"),
		(try_end), 
	]),
	
	(ti_on_presentation_event_state_change, [
		(store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
        (try_begin),
        	## COMBO LABEL - REGION SELECTOR
			(eq, ":object", "$vai_region_selector"),
			(assign, "$vai_region_value", ":value"),
			(store_add, "$vai_region_kingdom", "$vai_region_value", kingdoms_begin),
			(start_presentation, "prsnt_add_troops"),
		
        (else_try),
			### BUTTON - DONE ###
			(troop_slot_eq, VAT_OBJECTS, vat_obj_button_done, ":object"),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_cheat_reports"),
		(try_end),
	]),
]),
  
## WINDYPLAINS- ##
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
