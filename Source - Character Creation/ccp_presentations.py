# Character Creation Presentation (1.0.8)
# Created by Windyplains.  Inspired by Dunde's character creation presentation in Custom Commander.


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
# script_gpu_create_game_button  - title, pos_x, pos_y, storage_id
# script_gpu_create_text_label   - title, pos_x, pos_y, storage_id, design
# script_gpu_resize_object       - storage_id, percent size
# script_gpu_draw_line           - x length, y length, pos_x, pos_y, color
# script_gpu_container_heading   - pos_x, pos_y, size_x, size_y, storage_id
# script_gpu_create_slider       - min, max, pos_x, pos_y, storage_id, value_id

presentations = [
###########################################################################################################################
#####                                        CHARACTER CREATION PRESENTATION                                          #####
###########################################################################################################################

("ccp_character_creation", 0, mesh_load_window, [
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),
		
		(call_script, "script_gpu_create_mesh", "mesh_character_creator", 0, 0, 1000, 1325),
		(overlay_set_alpha, reg1, 0x00),
		
		(assign, "$gpu_storage", "trp_tpe_presobj"),
		
		# Bottom Buttons
		(call_script, "script_gpu_create_game_button", "str_ccp_label_done", 890, 15, ccp_obj_button_done),
		(call_script, "script_gpu_create_game_button", "str_ccp_label_back", 715, 15, ccp_obj_button_back),
		(call_script, "script_gpu_create_game_button", "str_ccp_label_default", 105, 15, ccp_obj_button_default),
		(call_script, "script_gpu_create_game_button", "str_ccp_label_random", 280, 15, ccp_obj_button_random),
		
		(assign, ":menu_size", 75), # This is % of original size.  So 75 -> 750.
		
		(assign, ":pos_x_menus", 122),
		(call_script, "script_gpu_create_text_label", "str_ccp_label_gender",    ":pos_x_menus", 650, ccp_obj_label_gender, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_create_text_label", "str_ccp_label_father",    ":pos_x_menus", 590, ccp_obj_label_father, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_create_text_label", "str_ccp_label_earlylife", ":pos_x_menus", 530, ccp_obj_label_earlylife, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_create_text_label", "str_ccp_label_later",     ":pos_x_menus", 470, ccp_obj_label_later, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_create_text_label", "str_ccp_label_reason",    ":pos_x_menus", 410, ccp_obj_label_reason, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_label_gender, ":menu_size"),
		(call_script, "script_gpu_resize_object", ccp_obj_label_father, ":menu_size"),
		(call_script, "script_gpu_resize_object", ccp_obj_label_earlylife, ":menu_size"),
		(call_script, "script_gpu_resize_object", ccp_obj_label_later, ":menu_size"),
		(call_script, "script_gpu_resize_object", ccp_obj_label_reason, ":menu_size"),
		
		(position_set_x, pos1, 150),
		# gender
        (position_set_y, pos1, 610),
        (create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
        (overlay_add_item, reg1, "@male"),
		(overlay_add_item, reg1, "@female"),
        (overlay_set_val, reg1, "$character_gender"),
		(troop_set_slot, ccp_objects, ccp_obj_menu_gender, reg1),
        (call_script, "script_gpu_resize_object", ccp_obj_menu_gender, ":menu_size"),
		
		# father
        (position_set_y, pos1, 550),
        (create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
        (overlay_add_item, reg1, "@a priest"),
        (overlay_add_item, reg1, "@a thief"),
        (overlay_add_item, reg1, "@a steppe nomad"),
        (overlay_add_item, reg1, "@a hunter"),
        (overlay_add_item, reg1, "@a veteran warrior"),
        (overlay_add_item, reg1, "@a travelling merchant"),
        (overlay_add_item, reg1, "@an impoverished noble"),
		(overlay_set_val, reg1, "$background_type"),
		(troop_set_slot, ccp_objects, ccp_obj_menu_father, reg1),
		(call_script, "script_gpu_resize_object", ccp_obj_menu_father, ":menu_size"),
		
		# early life
        (position_set_y, pos1, 490),
        (create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
        (overlay_add_item, reg1, "@an acolyte"),
        (overlay_add_item, reg1, "@a noble in training"),
        (overlay_add_item, reg1, "@a courtier"),
        (overlay_add_item, reg1, "@a mummer"),
        (overlay_add_item, reg1, "@a shop assistant"),
        (overlay_add_item, reg1, "@a steppe child"),
        (overlay_add_item, reg1, "@a street urchin"),
        (overlay_add_item, reg1, "@a craftsman's apprentice"),
        (overlay_add_item, reg1, "@a page at a nobleman's court"),
		(overlay_set_val, reg1, "$background_answer_2"),
		(troop_set_slot, ccp_objects, ccp_obj_menu_earlylife, reg1),
		(call_script, "script_gpu_resize_object", ccp_obj_menu_earlylife, ":menu_size"),
		
		
		# later
        (position_set_y, pos1, 430),
        (create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
        (try_begin),
          (eq,"$character_gender",tf_male),
          (overlay_add_item, reg1, "@a squire"),
        (else_try),
          (eq,"$character_gender",tf_female),
          (overlay_add_item, reg1, "@a lady-in-waiting"),
        (try_end),
		(overlay_add_item, reg1, "@a university student"),
		(overlay_add_item, reg1, "@a troubadour"),
		(overlay_add_item, reg1, "@a preacher"),
		(overlay_add_item, reg1, "@a goods peddler"),
        (overlay_add_item, reg1, "@a smith"),
        (overlay_add_item, reg1, "@a game poacher"),
        (overlay_add_item, reg1, "@a mercenary"),
		(overlay_add_item, reg1, "@a bravo"),
		(overlay_add_item, reg1, "@a thief"),
		(overlay_add_item, reg1, "@a gladiator"),
		(overlay_add_item, reg1, "@a bandit"),
		(overlay_add_item, reg1, "@a slave-trader"),
		(overlay_set_val, reg1, "$background_answer_3"),
		(troop_set_slot, ccp_objects, ccp_obj_menu_later, reg1),
		(call_script, "script_gpu_resize_object", ccp_obj_menu_later, ":menu_size"),

		# reason
        (position_set_y, pos1, 370),
        (create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
        (overlay_add_item, reg1, "@lust for money and power"),
        (overlay_add_item, reg1, "@being forced out of your home"),
        (overlay_add_item, reg1, "@religious fervor"),
        (overlay_add_item, reg1, "@wanderlust"),
        (overlay_add_item, reg1, "@the loss of a loved one"),
        (overlay_add_item, reg1, "@personal revenge"),
		(overlay_add_item, reg1, "@sense of duty"),
		(overlay_set_val, reg1, "$background_answer_4"),
		(troop_set_slot, ccp_objects, ccp_obj_menu_reason, reg1),
		(call_script, "script_gpu_resize_object", ccp_obj_menu_reason, ":menu_size"),
		
		
		## story
        (call_script, "script_ccp_get_character_background_text"),
        (create_text_overlay, reg1, "@{s1}", tf_double_space|tf_scrollable),
        (position_set_x, pos1, 255),
        (position_set_y, pos1, 90),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 470),
        (position_set_y, pos1, 585),
        (overlay_set_area_size, reg1, pos1),
        
		
		##########################################################
		###                 FLORIS GAME OPTIONS                ###
		##########################################################
		
		# MTT Choice begin
		# (assign, ":pos_x_labels", 870),
		# (call_script, "script_gpu_create_text_label", "str_ccp_label_mtt", ":pos_x_labels", 650, ccp_obj_label_mtt, gpu_center_with_outline),
		# (overlay_set_color, reg1, gpu_white),
		# (call_script, "script_gpu_resize_object", ccp_obj_label_mtt, ":menu_size"),
		
		# (store_add, ":pos_x_menus", ":pos_x_labels", 28),
		# (position_set_x, pos1, ":pos_x_menus"),
		# (position_set_y, pos1, 610),
        # (create_combo_button_overlay, reg1),
        # (overlay_set_position, reg1, pos1),
        # (overlay_add_item, reg1, "@Native Troops"),
		# (overlay_add_item, reg1, "@Reworked Troops"),
        # (overlay_add_item, reg1, "@Expanded Troops"),
        # (troop_get_slot, ":value", ccp_objects, ccp_val_menu_trooptrees),
        # (overlay_set_val, reg1, ":value"),
		# (troop_set_slot, ccp_objects, ccp_obj_menu_trooptrees, reg1),
		# (call_script, "script_gpu_resize_object", ccp_obj_menu_trooptrees, ":menu_size"),
		# MTT Choice end
		
		# Starting Area Choice begin
		(assign, ":pos_x_labels", 870),
		(call_script, "script_gpu_create_text_label", "str_ccp_label_region", ":pos_x_labels", 650, ccp_obj_label_region, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_label_region, ":menu_size"),
		
		(store_add, ":pos_x_menus", ":pos_x_labels", 28),
		(position_set_x, pos1, ":pos_x_menus"),
		(position_set_y, pos1, 610),
        (create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
		(try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
			(neq, ":faction_no", kingdoms_begin),
			(str_store_faction_name, s1, ":faction_no"),
			(overlay_add_item, reg1, s1),
		(try_end),
        (troop_get_slot, ":value", ccp_objects, ccp_val_menu_initial_region),
        (overlay_set_val, reg1, ":value"),
		(troop_set_slot, ccp_objects, ccp_obj_menu_initial_region, reg1),
		(call_script, "script_gpu_resize_object", ccp_obj_menu_initial_region, ":menu_size"),
		# Starting Area Choice end
		
		# MOD DIFFICULTY MENU begin
		(assign, ":pos_x_labels", 870),
		(call_script, "script_gpu_create_text_label", "str_ccp_label_mod_difficulty", ":pos_x_labels", 590, ccp_label_mod_difficulty, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_label_mod_difficulty, ":menu_size"),
		
		(store_add, ":pos_x_menus", ":pos_x_labels", 28),
		(position_set_x, pos1, ":pos_x_menus"),
		(position_set_y, pos1, 550),
        (create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
        (overlay_add_item, reg1, "@Easy"),
		(overlay_add_item, reg1, "@Normal"),
        (overlay_add_item, reg1, "@Hard"),
        (overlay_add_item, reg1, "@Very Hard"),
		(troop_get_slot, ":value", ccp_objects, ccp_val_menu_mod_difficulty),
        (overlay_set_val, reg1, ":value"),
		(troop_set_slot, ccp_objects, ccp_obj_menu_mod_difficulty, reg1),
		(call_script, "script_gpu_resize_object", ccp_obj_menu_mod_difficulty, ":menu_size"),
		# MOD DIFFICULTY MENU end
		
		# QUEST REACTION MENU begin
		(assign, ":pos_x_labels", 870),
		(call_script, "script_gpu_create_text_label", "str_ccp_label_quest_reaction", ":pos_x_labels", 530, ccp_obj_label_mtt, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_label_mtt, ":menu_size"),
		
		(store_add, ":pos_x_menus", ":pos_x_labels", 28),
		(position_set_x, pos1, ":pos_x_menus"),
		(position_set_y, pos1, 490),
        (create_combo_button_overlay, reg1),
        (overlay_set_position, reg1, pos1),
        (overlay_add_item, reg1, "@High"),
		(overlay_add_item, reg1, "@Medium"),
        (overlay_add_item, reg1, "@Low"),
		(troop_get_slot, ":value", ccp_objects, ccp_val_menu_questreaction),
        (overlay_set_val, reg1, ":value"),
		(troop_set_slot, ccp_objects, ccp_obj_menu_questreaction, reg1),
		(call_script, "script_gpu_resize_object", ccp_obj_menu_questreaction, ":menu_size"),
		# QUEST REACTION MENU end
		
		# Gather companions at nearest tavern
		# (try_begin),
			# (eq, "$g_gether_npcs", 1),
			# (troop_set_slot, ccp_objects, ccp_val_checkbox_gather_npcs, "$g_gether_npcs"),
		# (try_end),
		(call_script, "script_gpu_create_checkbox_white", 755, 450, "str_ccp_label_gather_npcs", ccp_obj_checkbox_gather_npcs, ccp_val_checkbox_gather_npcs), # was 755, 460 with Fog of War
		(overlay_set_val, reg1, "$g_gether_npcs"),
		
		# Fog of War
		# (try_begin),
			# (eq, "$g_fog", 1),
			# (troop_set_slot, ccp_objects, ccp_val_checkbox_fogofwar, "$g_fog"),
		# (try_end),
		# (call_script, "script_gpu_create_checkbox_white", 755, 420, "str_ccp_label_fog_of_war", ccp_obj_checkbox_fogofwar, ccp_val_checkbox_fogofwar),
		
		# Initialize the equipment list
		(call_script, "script_ccp_initialize_faction_items"),
		
		##########################################################
		###                 GENERATE STAT INFO                 ###
		##########################################################
		(assign, ":pos_y_stats", 290),
		(store_sub, ":pos_y_stat_values", ":pos_y_stats", 25),
		(assign, ":pos_x_stat_1", 55),  # Strength
		(assign, ":pos_x_stat_2", 100),  # Agility
		(assign, ":pos_x_stat_3", 145), # Intelligence
		(assign, ":pos_x_stat_4", 190), # Charisma
		(str_clear, s31),
		
		### STRENGTH ###
		# Label
		(call_script, "script_gpu_create_text_label", "str_ccp_str", ":pos_x_stat_1", ":pos_y_stats", ccp_obj_label_strength, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_label_strength, ":menu_size"),
		# Value
		(call_script, "script_gpu_create_text_label", "str_ccp_empty", ":pos_x_stat_1", ":pos_y_stat_values", ccp_obj_stat_strength, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_stat_strength, ":menu_size"),
		
		### AGILITY ###
		# Label
		(call_script, "script_gpu_create_text_label", "str_ccp_agi", ":pos_x_stat_2", ":pos_y_stats", ccp_obj_label_agility, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_label_agility, ":menu_size"),
		# Value
		(call_script, "script_gpu_create_text_label", "str_ccp_empty", ":pos_x_stat_2", ":pos_y_stat_values", ccp_obj_stat_agility, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_stat_agility, ":menu_size"),
		
		### INTELLIGENCE ###
		# Label
		(call_script, "script_gpu_create_text_label", "str_ccp_int", ":pos_x_stat_3", ":pos_y_stats", ccp_obj_label_intelligence, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_label_intelligence, ":menu_size"),
		# Value
		(call_script, "script_gpu_create_text_label", "str_ccp_empty", ":pos_x_stat_3", ":pos_y_stat_values", ccp_obj_stat_intelligence, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_stat_intelligence, ":menu_size"),
		
		### CHARISMA ###
		# Label
		(call_script, "script_gpu_create_text_label", "str_ccp_cha", ":pos_x_stat_4", ":pos_y_stats", ccp_obj_label_charisma, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_label_charisma, ":menu_size"),
		# Value
		(call_script, "script_gpu_create_text_label", "str_ccp_empty", ":pos_x_stat_4", ":pos_y_stat_values", ccp_obj_stat_charisma, gpu_center_with_outline),
		(overlay_set_color, reg1, gpu_white),
		(call_script, "script_gpu_resize_object", ccp_obj_stat_charisma, ":menu_size"),
		
		(assign, ":pos_x_misc_icon", 65),
		(assign, ":pos_x_misc_labels", 25),
		# (call_script, "script_ccp_generate_skill_set", summarize_skill_count),
		# (store_mul, ":pos_y_misc", reg1, 25),
		(assign, ":pos_y_misc", 300), # was 230, but that was causing it to run out of scroll room if too many options were selected.
		(assign, ":y_step_1", 20), # For text lines.
		(assign, ":y_step_2", 5), # For images
		
		# script_gpu_container_heading   - pos_x, pos_y, size_x, size_y, storage_id
		(call_script, "script_gpu_container_heading", 0, 60, 220, 195, ccp_obj_stat_container),
		############### ATTRIBUTES CONTAINER BEGIN ###############	
		
			### GOLD ###
			# Value
			(call_script, "script_gpu_create_text_label", "str_ccp_zero", ":pos_x_misc_labels", ":pos_y_misc", ccp_obj_stat_gold, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", ccp_obj_stat_gold, ":menu_size"),
			# Image
			(val_sub, ":pos_y_misc", ":y_step_2"),
			(store_sub, ":pos_y_temp", ":pos_y_misc", 5),
			(store_sub, ":pos_x_temp", ":pos_x_misc_icon", 22),
			(call_script, "script_gpu_create_mesh", "mesh_golden_coins", ":pos_x_temp", ":pos_y_temp", 250, 250),
			
			### RENOWN ###
			(val_sub, ":pos_y_misc", ":y_step_1"),
			# Value
			(call_script, "script_gpu_create_text_label", "str_ccp_zero", ":pos_x_misc_labels", ":pos_y_misc", ccp_obj_stat_renown, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", ccp_obj_stat_renown, ":menu_size"),
			# Image
			(val_sub, ":pos_y_misc", ":y_step_2"),
			# (store_add, ":pos_y_temp", ":pos_y_misc", 2), # Line used when image was a shield.
			(store_sub, ":pos_y_temp", ":pos_y_misc", -5), # line used for new crown image.
			(store_sub, ":pos_x_temp", ":pos_x_misc_icon", -3), # 12 as a shield.
			(str_store_string, s31, "@Renown"),
			(call_script, "script_gpu_create_text_label", "str_ccp_empty", ":pos_x_temp", ":pos_y_temp", 0, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", 0, ":menu_size"),
			#(call_script, "script_gpu_create_mesh", "mesh_status_renown", ":pos_x_temp", ":pos_y_temp", 150, 150),
			
			### WEAPON PROF - ONE HAND ###
			(val_sub, ":pos_y_misc", ":y_step_1"),
			# Value
			(call_script, "script_gpu_create_text_label", "str_ccp_zero", ":pos_x_misc_labels", ":pos_y_misc", ccp_obj_stat_weapon_onehand, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", ccp_obj_stat_weapon_onehand, ":menu_size"),
			# Image
			(val_sub, ":pos_y_misc", ":y_step_2"),
			(store_sub, ":pos_x_temp", ":pos_x_misc_icon", 5),
			(call_script, "script_gpu_create_mesh", "mesh_weapon_onehand", ":pos_x_temp", ":pos_y_misc", 150, 150),
			
			### WEAPON PROF - TWO HAND ###
			(val_sub, ":pos_y_misc", ":y_step_1"),
			# Value
			(call_script, "script_gpu_create_text_label", "str_ccp_zero", ":pos_x_misc_labels", ":pos_y_misc", ccp_obj_stat_weapon_twohand, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", ccp_obj_stat_weapon_twohand, ":menu_size"),
			# Image
			(val_sub, ":pos_y_misc", ":y_step_2"),
			(call_script, "script_gpu_create_mesh", "mesh_weapon_twohand", ":pos_x_misc_icon", ":pos_y_misc", 150, 150),
			
			### WEAPON PROF - POLEARM ###
			(val_sub, ":pos_y_misc", ":y_step_1"),
			# Value
			(call_script, "script_gpu_create_text_label", "str_ccp_zero", ":pos_x_misc_labels", ":pos_y_misc", ccp_obj_stat_weapon_polearm, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", ccp_obj_stat_weapon_polearm, ":menu_size"),
			# Image
			(val_sub, ":pos_y_misc", ":y_step_2"),
			(store_sub, ":pos_x_temp", ":pos_x_misc_icon", 2),
			(call_script, "script_gpu_create_mesh", "mesh_weapon_polearm", ":pos_x_temp", ":pos_y_misc", 200, 200),
			
			### WEAPON PROF - ARCHERY ###
			(val_sub, ":pos_y_misc", ":y_step_1"),
			# Value
			(call_script, "script_gpu_create_text_label", "str_ccp_zero", ":pos_x_misc_labels", ":pos_y_misc", ccp_obj_stat_weapon_archery, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", ccp_obj_stat_weapon_archery, ":menu_size"),
			# Image
			(val_sub, ":pos_y_misc", ":y_step_2"),
			(store_sub, ":pos_x_temp", ":pos_x_misc_icon", 10),
			(call_script, "script_gpu_create_mesh", "mesh_weapon_bow", ":pos_x_temp", ":pos_y_misc", 250, 250),
			
			### WEAPON PROF - CROSSBOW ###
			(val_sub, ":pos_y_misc", ":y_step_1"),
			# Value
			(call_script, "script_gpu_create_text_label", "str_ccp_zero", ":pos_x_misc_labels", ":pos_y_misc", ccp_obj_stat_weapon_crossbow, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", ccp_obj_stat_weapon_crossbow, ":menu_size"),
			# Image
			(val_sub, ":pos_y_misc", ":y_step_2"),
			(store_sub, ":pos_x_temp", ":pos_x_misc_icon", 3),
			(call_script, "script_gpu_create_mesh", "mesh_weapon_crossbow", ":pos_x_temp", ":pos_y_misc", 250, 250),
			
			### WEAPON PROF - THROWING ###
			(val_sub, ":pos_y_misc", ":y_step_1"),
			# Value
			(call_script, "script_gpu_create_text_label", "str_ccp_zero", ":pos_x_misc_labels", ":pos_y_misc", ccp_obj_stat_weapon_throwing, gpu_center_with_outline),
			(overlay_set_color, reg1, gpu_white),
			(call_script, "script_gpu_resize_object", ccp_obj_stat_weapon_throwing, ":menu_size"),
			# Image
			(val_sub, ":pos_y_misc", ":y_step_2"),
			(store_sub, ":pos_x_temp", ":pos_x_misc_icon", 3),
			(call_script, "script_gpu_create_mesh", "mesh_weapon_thorwing", ":pos_x_temp", ":pos_y_misc", 150, 150),
			
			# This needs to come after all of the text fields are created since it fills them.
			(call_script, "script_ccp_generate_skill_set", limit_to_stats),
			
		############### ATTRIBUTES CONTAINER END ###############	
		(set_container_overlay, -1),
		
      ]),
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, ccp_objects, ccp_obj_button_done, ":object"),
			(call_script, "script_ccp_end_presentation_begin_game"),
			# Decide on whether to use a banner or not
			(try_begin),
			## CCP 1.1+ ## - Workaround for the Warband 1.151 broken banner presentation.
				# (eq, "$background_type", cb_noble),
				# (jump_to_menu, "mnu_auto_return"),
				# (start_presentation, "prsnt_banner_selection"),
			# (else_try),
			## CCP 1.1- ##
				(presentation_set_duration, 0),
				(jump_to_menu, "mnu_auto_return"),
			(try_end),

			#(jump_to_menu, "mnu_start_phase_2_5"),
			
		(else_try), ####### BACK BUTTON #######
			(troop_slot_eq, ccp_objects, ccp_obj_button_back, ":object"),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_start_game_0"),
			
		(else_try), ####### DEFAULT BUTTON #######]
			(troop_slot_eq, ccp_objects, ccp_obj_button_default, ":object"),
			(call_script, "script_ccp_default_settings"),
			(start_presentation, "prsnt_ccp_character_creation"),
		  
		(else_try), ####### RANDOMIZE BUTTON #######
			(troop_slot_eq, ccp_objects, ccp_obj_button_random, ":object"),
			(store_random_in_range, "$character_gender", 0, 2),    # Gender
			(store_random_in_range, "$background_type", 0, 6),     # Father background
			(store_random_in_range, "$background_answer_2", 0, 5), # Early life
			(store_random_in_range, "$background_answer_3", 0, 6), # Later life
			(store_random_in_range, "$background_answer_4", 0, 5), # Reason
            (store_random_in_range, reg21, 0, 5), # Starting Region
			(troop_set_slot, ccp_objects, ccp_val_menu_initial_region, reg21),
            (start_presentation, "prsnt_ccp_character_creation"),
			
			
		(else_try), ####### GENDER MENU #######
			(troop_slot_eq, ccp_objects, ccp_obj_menu_gender, ":object"),
			(assign, "$character_gender", ":value"),
			(start_presentation, "prsnt_ccp_character_creation"),
			(ge, DEBUG_CCP_general, 2),
			(assign, reg1, ":value"),
			(display_message, "@Gender option changed to option {reg1}."),
			
		(else_try), ####### FATHER BACKGROUND MENU #######
			(troop_slot_eq, ccp_objects, ccp_obj_menu_father, ":object"),
			(assign, "$background_type", ":value"),
			(start_presentation, "prsnt_ccp_character_creation"),
			(ge, DEBUG_CCP_general, 2),
			(assign, reg1, ":value"),
			(display_message, "@Father background option changed to option {reg1}."),
			
		(else_try), ####### EARLY LIFE BACKGROUND MENU #######
			(troop_slot_eq, ccp_objects, ccp_obj_menu_earlylife, ":object"),
			(assign, "$background_answer_2", ":value"),
			(start_presentation, "prsnt_ccp_character_creation"),
			(ge, DEBUG_CCP_general, 2),
			(assign, reg1, ":value"),
			(display_message, "@Early life option changed to option {reg1}."),
			
		(else_try), ####### LATER LIFE BACKGROUND MENU #######
			(troop_slot_eq, ccp_objects, ccp_obj_menu_later, ":object"),
			(assign, "$background_answer_3", ":value"),
			(start_presentation, "prsnt_ccp_character_creation"),
			(ge, DEBUG_CCP_general, 2),
			(assign, reg1, ":value"),
			(display_message, "@Later life option changed to option {reg1}."),
			
		(else_try), ####### REASON BACKGROUND MENU #######
			(troop_slot_eq, ccp_objects, ccp_obj_menu_reason, ":object"),
			(assign, "$background_answer_4", ":value"),
			(start_presentation, "prsnt_ccp_character_creation"),
			(ge, DEBUG_CCP_general, 2),
			(assign, reg1, ":value"),
			(display_message, "@Reason option changed to option {reg1}."),
			
		# (else_try), ####### TROOP TREE SELECTION MENU #######
			# (troop_slot_eq, ccp_objects, ccp_obj_menu_trooptrees, ":object"),
			# (troop_set_slot, ccp_objects, ccp_val_menu_trooptrees, ":value"),
			# (try_begin),
				# (eq, ":value", 0),
				# (assign, "$troop_trees", troop_trees_0),
			# (else_try),
				# (eq, ":value", 1),
				# (assign, "$troop_trees", troop_trees_1),
			# (else_try),
				# (eq, ":value", 2),
				# (assign, "$troop_trees", troop_trees_2),
			# (else_try),
				# (display_message, "@ERROR: No valid troop tree selection found."),
			# (try_end),
			# (start_presentation, "prsnt_ccp_character_creation"),
			# (ge, DEBUG_CCP_general, 1),
			# (assign, reg1, ":value"),
			# (display_message, "@Troop tree changed to option {reg1?Expanded or Reworked:Native} Trees [ {reg1} ]."),
			
		(else_try), ####### MOD DIFFICULTY SELECTION MENU #######
			(troop_slot_eq, ccp_objects, ccp_obj_menu_mod_difficulty, ":object"),
			(troop_set_slot, ccp_objects, ccp_val_menu_mod_difficulty, ":value"),
			(try_begin),
				(eq, ":value", 0),
				(assign, "$mod_difficulty", GAME_MODE_EASY),
			(else_try),
				(eq, ":value", 1),
				(assign, "$mod_difficulty", GAME_MODE_NORMAL),
			(else_try),
				(eq, ":value", 2),
				(assign, "$mod_difficulty", GAME_MODE_HARD),
			(else_try),
				(eq, ":value", 3),
				(assign, "$mod_difficulty", GAME_MODE_VERY_HARD),
			(else_try),
				(display_message, "@ERROR: No mod difficulty selection found so defaulting to normal.", gpu_red),
				(assign, "$mod_difficulty", GAME_MODE_NORMAL),
			(try_end),
			(call_script, "script_initialize_faction_troop_types"),
			(call_script, "script_reset_garrisons"),
			
		(else_try), ####### QUEST REACTION SELECTION MENU #######
			(troop_slot_eq, ccp_objects, ccp_obj_menu_questreaction, ":object"),
			(troop_set_slot, ccp_objects, ccp_val_menu_questreaction, ":value"),
			(try_begin),
				(eq, ":value", 0),
				(assign, "$quest_reactions", QUEST_REACTIONS_HIGH),
			(else_try),
				(eq, ":value", 1),
				(assign, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
			(else_try),
				(eq, ":value", 2),
				(assign, "$quest_reactions", QUEST_REACTIONS_LOW),
			(else_try),
				(display_message, "@ERROR: No quest reaction selection found."),
			(try_end),
			#(start_presentation, "prsnt_ccp_character_creation"),
			(ge, DEBUG_CCP_general, 1),
			(assign, reg1, ":value"),
			(assign, reg2, "$quest_reactions"),
			(display_message, "@Quest reaction changed to option {reg1} -> reaction {reg2}.", gpu_red),
		
		# (else_try), ####### FOG OF WAR CHECKBOX #######
			# (troop_slot_eq, ccp_objects, ccp_obj_checkbox_fogofwar, ":object"),
			# (assign, "$g_fog", ":value"),
			# (call_script, "script_initialize_fog"),
			# (troop_set_slot, ccp_objects, ccp_val_checkbox_fogofwar, ":value"),
			# (ge, DEBUG_CCP_general, 1),
			# (assign, reg1, ":value"),
			# (display_message, "@Option: Fog of War has been {reg1?ENABLED:turned off} [ {reg1} ]."),
			
		(else_try), ####### GATHER NPCS CHECKBOX #######
			(troop_slot_eq, ccp_objects, ccp_obj_checkbox_gather_npcs, ":object"),
			(assign, "$g_gether_npcs", ":value"),
			(troop_set_slot, ccp_objects, ccp_val_checkbox_gather_npcs, ":value"),
			(ge, DEBUG_CCP_general, 1),
			(assign, reg1, ":value"),
			(display_message, "@Option: Gathering companions has been {reg1?ENABLED:turned off} [ {reg1} ].", gpu_debug),
		
		(else_try), ####### STARTING REGION MENU #######
			(troop_slot_eq, ccp_objects, ccp_obj_menu_initial_region, ":object"),
			(troop_set_slot, ccp_objects, ccp_val_menu_initial_region, ":value"),
			(start_presentation, "prsnt_ccp_character_creation"),
			(ge, DEBUG_CCP_general, 1),
			(assign, reg1, ":value"),
			(store_add, ":faction_picked", kingdoms_begin, ":value"),
			(val_add, ":faction_picked", 1),
			(str_store_faction_name, s2, ":faction_picked"),
			(display_message, "@Option: Starting region has been set to {s2} [{reg1}]."),
		
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