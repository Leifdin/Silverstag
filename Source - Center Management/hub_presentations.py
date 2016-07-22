# Center Hub (1.0) by Windyplains

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
#####                                               GENERAL INFORMATION                                               #####
###########################################################################################################################
("hub_general_info", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			(call_script, "script_hub_create_mode_switching_buttons"),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			
			## RENAMING THE CENTER
			(store_faction_of_party, ":faction_no", "$current_town"),
			(try_begin),
				(this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
				(faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
				## OBJ - RENAMING LABEL
				#(call_script, "script_gpu_create_text_label", "str_hub_general_info", 865, 620, hub1_obj_label_rename_center, gpu_center),
				## OBJ - BUTTON TO EXECUTE RENAMING
				(call_script, "script_gpu_create_button", "str_hub_center_rename", 780, 580, hub1_obj_button_rename_center),
				## OBJ - INPUT TEXT BOX
				(call_script, "script_gpu_create_text_box", 910, 545, hub1_obj_textbox_rename_center),
				(call_script, "script_gpu_resize_object", hub1_obj_textbox_rename_center, 75),
				(str_store_party_name, s21, "$current_town"),
				(overlay_set_text, reg1, "@{s21}"),
			(try_end),
			
			################ DETERMINE INTELLIGENCE OF CENTER ##################
			(try_begin),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
				(assign, ":minimum_intel", 10),
			(else_try),
				(store_faction_of_party, ":faction_no", "$current_town"),
				(eq, ":faction_no", "$players_kingdom"),
				(assign, ":minimum_intel", 7),
			(else_try),
				(assign, ":minimum_intel", 3),
			(try_end),
			(party_get_slot, ":intel", "$current_town", slot_center_intelligence),
			(val_max, ":intel", ":minimum_intel"),
			#(assign, reg1, ":intel"),
			#(display_message, "@DEBUG: Intelligence level is {reg1}.", gpu_debug),
			#(party_set_slot, "$current_town", slot_center_intelligence, ":intel"),
			
			################ DETERMINE NUMBER OF LINES #################
			(assign, ":num_lines", 0),
			(try_begin),
				(val_add, ":num_lines", 10), # headings x3, partial steps x5
				(val_add, ":num_lines", 9), # town lord, prosperity, relation, culture, mercenaries, last owner, peasant recruits, noble recruits, available mounts
				
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(val_add, ":num_lines", 2), # recruitment & bound center headers.
					# (try_begin),
						# (party_slot_eq, "$current_town", slot_party_type, spt_town),
						# (val_add, ":num_lines", 1), # mercenary recruits.
					# (try_end),
				(try_end),
				
				(try_begin),
					(party_slot_eq, "$current_town", slot_party_type, spt_village),
					(this_or_next|party_slot_eq, "$current_town", slot_village_state, svs_looted),
					(party_slot_eq, "$current_town", slot_village_state, svs_recovering),
					(ge, ":intel", 5),
					(val_add, ":num_lines", 1), # village recovery progress
					(ge, ":intel", 7),
					(val_add, ":num_lines", 1), # last raided by.
				(try_end),
				
				(try_begin),
					(ge, ":intel", 7),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(try_for_range, ":village_no", villages_begin, villages_end),
						(party_slot_eq, ":village_no", slot_village_bound_center, "$current_town"),
						(val_add, ":num_lines", 1), # once per bound center.
					(try_end),
				(try_end),
				
				(try_begin),
					(ge, ":intel", 7),
					(call_script, "script_diplomacy_get_recruitment_score", "$current_town"),
					(assign, ":rating", reg1),
					(try_begin), # once for each non-zero recruitment rating factor.
						(neq, ":rating", 0),
						(val_add, ":num_lines", 1),
						(try_begin), (neq, reg32, 0), (val_add, ":num_lines", 1), (try_end), # Prosperity
						(try_begin), (neq, reg33, 0), (val_add, ":num_lines", 1), (try_end), # Distance
						(try_begin), (neq, reg34, 0), (val_add, ":num_lines", 1), (try_end), # COTG Persuasion
						(try_begin), (neq, reg35, 0), (val_add, ":num_lines", 1), (try_end), # COTG Renown
						(try_begin), (neq, reg36, 0), (val_add, ":num_lines", 1), (try_end), # Player Renown
						(try_begin), (neq, reg37, 0), (val_add, ":num_lines", 1), (try_end), # Faction Setting
						(try_begin), (neq, reg38, 0), (val_add, ":num_lines", 1), (try_end), # Game Difficulty
						(try_begin), (neq, reg39, 0), (val_add, ":num_lines", 1), (try_end), # Mandatory Conscription
					(try_end),
				(try_end),
				
				(try_begin),
					(ge, ":intel", 5),				
					(assign, ":improvements", 0),
					(try_for_range, ":building_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
						(party_get_slot, ":improvement_no", "$current_town", ":building_slot"),
						(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
						(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
						(val_add, ":num_lines", 1), # one per improvement in construction.
						(val_add, ":improvements", 1),
						(eq, ":improvements", 1),
						(val_add, ":num_lines", 1),
					(try_end),
				(try_end),
				
				(assign, ":count", 1),
				(try_for_range, ":improvement_no", native_improvements_begin, center_improvements_end),
					(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
					(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
					(party_slot_ge, "$current_town", ":improvement_no", cis_built),
					(val_add, ":count", 1),
					(try_begin),
						(eq, ":count", 1),
						(val_add, ":num_lines", 1),
					(try_end),
					(val_add, ":num_lines", 1),
				(try_end),
			(try_end),
			
			################ PRINT INFORMATION #################
			(assign, ":y_bottom", 80),
			(assign, ":x_left",  240),
			(assign, ":x_width", 490),
			(assign, ":y_width", 525),
			
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", hub_obj_container_3),
				(assign, ":left_margin", 5),
				(assign, ":line_step", 20),
				#(assign, ":post_heading_step", 30),
				(assign, ":section_step", 50),
				(store_mul, ":pos_y", ":line_step", ":num_lines"),
				
				# Blank line to push things off of the border.
				(str_clear, s21),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":left_margin", ":pos_y", 0, gpu_left),
				
				####### HEADER - GENERAL INFORMATION ######
				(val_sub, ":pos_y", 20),
				(call_script, "script_gpu_create_text_label", "str_hub_general_info", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_create_text_label", "str_hub_general_info", ":left_margin", ":pos_y", 0, gpu_left),
				
				## TOWN LORD ##
				(val_sub, ":pos_y", 8),
				(val_sub, ":pos_y", ":line_step"),
				(party_get_slot, ":troop_no", "$current_town", slot_town_lord),
				(try_begin),
					(ge, ":troop_no", 0),
					(str_store_troop_name, s21, ":troop_no"),
				(else_try),
					(str_store_string, s21, "@No owner is assigned"),
				(try_end),
				(try_begin),
					(party_slot_eq, "$current_town", slot_party_type, spt_town),
					(str_store_string, s22, "@Town"),
				(else_try),
					(party_slot_eq, "$current_town", slot_party_type, spt_castle),
					(str_store_string, s22, "@Castle"),
				(else_try),
					(party_slot_eq, "$current_town", slot_party_type, spt_village),
					(str_store_string, s22, "@Village"),
				(try_end),
				(call_script, "script_gpu_create_text_label", "str_hub_town_lord", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## PROSPERITY ##
				(val_sub, ":pos_y", ":line_step"),
				(party_get_slot, reg21, "$current_town", slot_town_prosperity),
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(assign, ":string_no", "str_hub_prosperity"),
				(else_try),
					(party_slot_eq, "$current_town", slot_party_type, spt_village),
					(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
					(neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
					(neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
					(assign, ":string_no", "str_hub_prosperity"),
				(else_try),
					(party_slot_eq, "$current_town", slot_party_type, spt_village),
					(party_slot_eq, "$current_town", slot_village_state, svs_looted),
					(assign, ":string_no", "str_hub_info_looted"),
				(else_try),
					(party_slot_eq, "$current_town", slot_party_type, spt_village),
					(party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
					(assign, ":string_no", "str_hub_info_being_raided"),
				(else_try),
					(party_slot_eq, "$current_town", slot_party_type, spt_village),
					(party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
					(assign, ":string_no", "str_hub_info_bandits"),
				(try_end),
				(call_script, "script_gpu_create_text_label", "str_hub_prosperity", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				##  * VILLAGES - RECOVERY PERCENTAGE (if looted) ##
				(try_begin),
					(party_slot_eq, "$current_town", slot_party_type, spt_village),
					(this_or_next|party_slot_eq, "$current_town", slot_village_state, svs_looted),
					(party_slot_eq, "$current_town", slot_village_state, svs_recovering),
					(ge, ":intel", 5),
					(val_sub, ":pos_y", ":line_step"),
					(party_get_slot, reg21, "$current_town", slot_village_recover_progress),
					(call_script, "script_gpu_create_text_label", "str_hub_recovery_state", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(ge, ":intel", 7),
					(val_sub, ":pos_y", ":line_step"),
					(party_get_slot, ":raiding_lord", "$current_town", slot_village_raided_by),
					(this_or_next|is_between, ":raiding_lord", active_npcs_begin, active_npcs_end),
					(eq, ":raiding_lord", "trp_player"),
					(str_store_troop_name, s22, ":raiding_lord"),
					(try_begin),
						(eq, ":raiding_lord", "trp_player"),
						(str_store_faction_name, s23, "$players_kingdom"),
					(else_try),
						(store_faction_of_troop, ":raiding_faction", ":raiding_lord"),
						(str_store_faction_name, s32, ":raiding_faction"),
					(try_end),
					(str_store_string, s21, "@Recently raided by {s22} of the {s23}."),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
				(try_end),
				
				## RELATION ##
				(val_sub, ":pos_y", ":line_step"),
				(party_get_slot, reg21, "$current_town", slot_center_player_relation),
				(call_script, "script_gpu_create_text_label", "str_hub_relation", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## CULTURE ##
				(val_sub, ":pos_y", ":line_step"),
				(party_get_slot, ":culture", "$current_town", slot_center_culture),
				###
				# (assign, reg31, ":culture"),
				# (str_store_party_name, s31, "$current_town"),
				# (display_message, "@DEBUG: {s31} uses culture #{reg31}.", gpu_debug),
				###
				# (party_get_slot, ":culture", "$current_town", slot_center_original_faction),
				(try_begin),
					## Error Trap in case we have a kingdom value here vs. culture value.
					(is_between, ":culture", kingdoms_begin, kingdoms_end),
					(assign, ":faction_no", ":culture"),
					(str_store_faction_name, s21, ":faction_no"),
				(else_try),
					## Catch player's unique culture entry.
					(eq, ":culture", "fac_culture_player"),
					(str_store_faction_name, s21, "$players_kingdom"),
				(else_try),
					## Default: Turn culture into a kingdom value.
					(store_sub, ":faction_no", ":culture", "fac_culture_1"),
					(val_add, ":faction_no", kingdoms_begin),
					(val_add, ":faction_no", 1), # Because no player faction exists before Faction 1 in the cultures.
					(str_store_faction_name, s21, ":faction_no"),
				(try_end),
				
				# (try_begin),
					# (eq, ":faction_no", "fac_player_supporters_faction"),
					# # (str_store_string, s21, "@Custom Culture"),
					# (str_store_faction_name, s21, "$players_kingdom"),
				# (else_try),
					# (eq, ":culture", "fac_culture_player"),
					# # (str_store_string, s21, "@Custom Culture"),
					# (str_store_faction_name, s21, "$players_kingdom"),
				# (else_try),
					# (str_store_faction_name, s21, ":faction_no"),
				# (try_end),
				(call_script, "script_gpu_create_text_label", "str_hub_culture", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## LAST OWNER ##
				(try_begin),
					(party_get_slot, ":last_owner", "$current_town", slot_center_ex_faction),
					(is_between, ":last_owner", kingdoms_begin, kingdoms_end),
					(str_store_faction_name, s21, ":last_owner"),
					(str_store_party_name, s22, "$current_town"),
					(try_begin),
						(store_faction_of_party, ":current_owner", "$current_town"),
						(eq, ":last_owner", ":current_owner"),
						(str_store_string, s22, "@{s22} is still held by {s21}."),
					(else_try),
						(str_store_string, s22, "str_hub_last_owner"),
					(try_end),
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				####### HEADER - DEFENSE ######
				(val_sub, ":pos_y", ":section_step"),
				(call_script, "script_gpu_create_text_label", "str_hub_recruitment", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_create_text_label", "str_hub_recruitment", ":left_margin", ":pos_y", 0, gpu_left),
				
				## AVAILABLE VETERANS ##
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", 8),
				(party_get_slot, reg21, "$current_town", slot_center_veteran_pool),
				(call_script, "script_gpu_create_text_label", "str_hub_available_nobles", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## AVAILABLE MERCENARIES ##
				(val_sub, ":pos_y", ":line_step"),
				(party_get_slot, reg21, "$current_town", slot_center_mercenary_pool_player),
				(call_script, "script_gpu_create_text_label", "str_hub_available_mercenaries", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## AVAILABLE RECRUITS ##
				(val_sub, ":pos_y", ":line_step"),
				(party_get_slot, reg21, "$current_town", slot_center_volunteer_troop_amount),
				(call_script, "script_gpu_create_text_label", "str_hub_available_peasants", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## AVAILABLE MOUNTS ##
				(val_sub, ":pos_y", ":line_step"),
				(party_get_slot, reg21, "$current_town", slot_center_horse_pool_player),
				(call_script, "script_gpu_create_text_label", "str_hub_available_mounts", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				## RECRUITMENT RATING ##
				(try_begin),
					(ge, ":intel", 7),
					(val_sub, ":pos_y", ":line_step"),
					(val_sub, ":pos_y", 8),
					(call_script, "script_diplomacy_get_recruitment_score", "$current_town"),
					(assign, ":rating", reg1),
					(call_script, "script_gpu_create_text_label", "str_hub_recruitment_rating", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					# Get Factors
					(try_begin),
						(neq, ":rating", 0),
						(val_sub, ":pos_y", ":line_step"), 
						(call_script, "script_gpu_create_text_label", "str_hub_rec_rate_type", ":left_margin", ":pos_y", 0, gpu_left), 
						(call_script, "script_gpu_resize_object", 0, 75), 
						(try_begin), (neq, reg32, 0), (val_sub, ":pos_y", ":line_step"), (call_script, "script_gpu_create_text_label", "str_hub_rec_rate_prosperity", ":left_margin", ":pos_y", 0, gpu_left), (call_script, "script_gpu_resize_object", 0, 75), (try_end),    # Prosperity
						(try_begin), (neq, reg33, 0), (val_sub, ":pos_y", ":line_step"), (call_script, "script_gpu_create_text_label", "str_hub_rec_rate_distance", ":left_margin", ":pos_y", 0, gpu_left), (call_script, "script_gpu_resize_object", 0, 75), (try_end),      # Distance
						(try_begin), (neq, reg34, 0), (val_sub, ":pos_y", ":line_step"), (call_script, "script_gpu_create_text_label", "str_hub_rec_rate_cotg_pers", ":left_margin", ":pos_y", 0, gpu_left), (call_script, "script_gpu_resize_object", 0, 75), (try_end),     # COTG Persuasion
						(try_begin), (neq, reg35, 0), (val_sub, ":pos_y", ":line_step"), (call_script, "script_gpu_create_text_label", "str_hub_rec_rate_cotg_renown", ":left_margin", ":pos_y", 0, gpu_left), (call_script, "script_gpu_resize_object", 0, 75), (try_end),   # COTG Renown
						(try_begin), (neq, reg36, 0), (val_sub, ":pos_y", ":line_step"), (call_script, "script_gpu_create_text_label", "str_hub_rec_rate_player_renown", ":left_margin", ":pos_y", 0, gpu_left), (call_script, "script_gpu_resize_object", 0, 75), (try_end), # Player Renown
						(try_begin), (neq, reg37, 0), (val_sub, ":pos_y", ":line_step"), (call_script, "script_gpu_create_text_label", "str_hub_rec_rate_faction", ":left_margin", ":pos_y", 0, gpu_left), (call_script, "script_gpu_resize_object", 0, 75), (try_end),       # Faction Setting
						(try_begin), (neq, reg38, 0), (val_sub, ":pos_y", ":line_step"), (call_script, "script_gpu_create_text_label", "str_hub_rec_rate_difficulty", ":left_margin", ":pos_y", 0, gpu_left), (call_script, "script_gpu_resize_object", 0, 75), (try_end),    # Game Difficulty
						(try_begin), (neq, reg39, 0), (val_sub, ":pos_y", ":line_step"), (call_script, "script_gpu_create_text_label", "str_hub_rec_rate_conscription", ":left_margin", ":pos_y", 0, gpu_left), (call_script, "script_gpu_resize_object", 0, 75), (try_end),  # Mandatory Conscription
					(else_try),
						(val_sub, ":pos_y", ":line_step"), 
						(call_script, "script_gpu_create_text_label", "str_hub_rec_rate_no_rating", ":left_margin", ":pos_y", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75), 
					(try_end),
				(try_end),
				
				## RATINGS OF BOUND VILLAGES ##
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(ge, ":intel", 7),
					(val_sub, ":pos_y", ":line_step"),
					(val_sub, ":pos_y", 8),
					(call_script, "script_gpu_create_text_label", "str_hub_label_bound_ratings", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(try_for_range, ":village_no", villages_begin, villages_end),
						(party_slot_eq, ":village_no", slot_village_bound_center, "$current_town"),
						(val_sub, ":pos_y", ":line_step"),
						(call_script, "script_diplomacy_get_recruitment_score", ":village_no"),
						(assign, ":rating", reg1),
						(str_store_party_name, s21, ":village_no"),
						(try_begin),
							(neq, ":rating", 0),
							(assign, ":string_no", "str_hub_recruitment_bound"),
						(else_try),
							(party_slot_eq, ":village_no", slot_village_state, svs_looted),
							(assign, ":string_no", "str_hub_village_looted"),
						(else_try),
							(party_slot_eq, ":village_no", slot_village_state, svs_being_raided),
							(assign, ":string_no", "str_hub_village_raiding"),
						(else_try),
							(party_slot_ge, ":village_no", slot_village_infested_by_bandits, 1),
							(assign, ":string_no", "str_hub_village_infested"),
						(else_try),
							(assign, ":string_no", "str_hub_recruitment_bound"),
						(try_end),
						(call_script, "script_gpu_create_text_label", ":string_no", ":left_margin", ":pos_y", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						# Village lord
						(party_get_slot, ":owner_no", ":village_no", slot_town_lord),
						(try_begin),
							(ge, ":owner_no", 0),
							(str_store_troop_name, s21, ":owner_no"),
						(else_try),
							(str_store_string, s21, "@Unassigned"),
						(try_end),
						(store_sub, ":right_margin", ":x_width", 15),
						(call_script, "script_gpu_create_text_label", "str_hub_village_owner", ":right_margin", ":pos_y", 0, gpu_right),
						(call_script, "script_gpu_resize_object", 0, 75),
						
					(try_end),
				(try_end),
				
				####### HEADER - INFRASTRUCTURE ######
				(val_sub, ":pos_y", ":section_step"),
				(call_script, "script_gpu_create_text_label", "str_hub_title_infrastructure", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_create_text_label", "str_hub_title_infrastructure", ":left_margin", ":pos_y", 0, gpu_left),
				
				## IMPROVEMENTS IN CONSTRUCTION ##
				(try_begin),
					(ge, ":intel", 5),
					(assign, ":count", 0),
					(try_for_range, ":building_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
						(party_get_slot, ":improvement_no", "$current_town", ":building_slot"),
						(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
						(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
						(val_add, ":count", 1),
						(try_begin),
							(eq, ":count", 1),
							(val_sub, ":pos_y", ":line_step"),
							(val_sub, ":pos_y", 8),
							(call_script, "script_gpu_create_text_label", "str_hub_current_construction", ":left_margin", ":pos_y", 0, gpu_left),
							(call_script, "script_gpu_resize_object", 0, 75),
						(try_end),
						(call_script, "script_get_improvement_details", ":improvement_no"),
						(val_sub, ":pos_y", ":line_step"),
						(call_script, "script_gpu_create_text_label", "str_hub_improvement_building", ":left_margin", ":pos_y", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
					(try_end),
				(try_end),
				
				## CURRENT IMPROVEMENTS ##
				(try_for_range, ":improvement_no", native_improvements_begin, center_improvements_end),
					(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
					(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
					(party_slot_ge, "$current_town", ":improvement_no", cis_built),
					(val_add, ":count", 1),
					(try_begin),
						(eq, ":count", 1),
						(val_sub, ":pos_y", ":line_step"),
						(val_sub, ":pos_y", 8),
						(call_script, "script_gpu_create_text_label", "str_hub_current_improvements", ":left_margin", ":pos_y", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
					(try_end),
					(call_script, "script_get_improvement_details", ":improvement_no"),
					# Assess damage to structure.
					(try_begin),
						(str_clear, s11),
						(ge, ":intel", 5),
						(party_slot_ge, "$current_town", ":improvement_no", cis_damaged_20_percent),
						(str_store_string, s11, "@ (minorly damaged)"),
						(party_slot_ge, "$current_town", ":improvement_no", cis_damaged_40_percent),
						(str_store_string, s11, "@ (moderately damaged)"),
						(party_slot_ge, "$current_town", ":improvement_no", cis_damaged_60_percent),
						(str_store_string, s11, "@ (heavily damaged)"),
						(party_slot_ge, "$current_town", ":improvement_no", cis_damaged_80_percent),
						(str_store_string, s11, "@ (total ruins)"),
					(try_end),
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_improvement_name", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
			(set_container_overlay, -1),
			
		]),
	
	(ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(presentation_set_duration, 0),
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(jump_to_menu, "mnu_town"),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(jump_to_menu, "mnu_village"),
			(try_end),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_hub_handle_mode_switching_buttons", ":object", ":value"),
		
		# (call_script, "script_gpu_create_button", "str_hub_center_rename", 780, 580, hub1_obj_button_rename_center),
		# OBJ - INPUT TEXT BOX
		# (call_script, "script_gpu_create_text_box", 910, 545, hub1_obj_textbox_rename_center),
		
		(try_begin),
			(troop_slot_eq, HUB_OBJECTS, hub1_obj_button_rename_center, ":object"),
			(troop_get_slot, ":obj_textbox", HUB_OBJECTS, hub1_obj_textbox_rename_center),
			(overlay_obtain_focus, ":obj_textbox"),
			(str_store_string, s22, s0),
			(call_script, "script_hub_rename_center_to_s22", "$current_town"),
			(start_presentation, "prsnt_hub_general_info"),
		(try_end),
      ]),
    ]),
	
	
	
	
	
###########################################################################################################################
#####                                                    FINANCES                                                     #####
###########################################################################################################################

("hub_finances", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_hub_create_mode_switching_buttons"),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			# OBJ - Warning note.
			(call_script, "script_gpu_create_text_label", "str_hub_label_starred", 500, 635, 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			
			#######################################
			### TREASURY DEPOSITS / WITHDRAWALS ###
			#######################################
			
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"), # Secondary block in the event player views this in cheat mode.
				
				(assign, ":y_bottom", 275),
				(assign, ":x_left", 752),
				(assign, ":x_width", 218),
				(assign, ":y_width", 330),
				
				(assign, ":y_button_step", 30),
				(assign, ":x_center", 860),
				(assign, ":x_left", 770),
				(assign, ":pos_y", 585),
				
				(call_script, "script_gpu_create_text_label", "str_hub_label_treasury", ":x_center", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_create_text_label", "str_hub_label_treasury", ":x_center", ":pos_y", 0, gpu_center),
				(val_sub, ":pos_y", 25),
				(assign, reg21, 0),
				(assign, reg22, 0),
				(call_script, "script_gpu_create_text_label", "str_hub_label_treasury_value", ":x_center", ":pos_y", hub2_obj_treasury_changes, gpu_center),
				(call_script, "script_gpu_resize_object", hub2_obj_treasury_changes, 75),
				(val_sub, ":pos_y", 40),
				# Figure out the lower bound.
				(party_get_slot, ":treasury_balance", "$current_town", slot_center_treasury),
				# Figure out the upper bound.
				(store_troop_gold, ":player_gold", "trp_player"),
				(val_max, ":player_gold", ":treasury_balance"),
				# Create the slider.
				(call_script, "script_gpu_create_slider", 0, ":player_gold", ":x_left", ":pos_y", hub2_obj_slider_treasury, hub2_val_slider_treasury),
				(call_script, "script_gpu_resize_object", hub2_obj_slider_treasury, 75),
				(val_sub, ":pos_y", ":y_button_step"),
				(call_script, "script_gpu_create_button", "str_hub_button_deposit", 770, ":pos_y", hub2_obj_button_treasury_deposit), # Treasury Deposit
				(call_script, "script_gpu_resize_object", hub2_obj_button_treasury_deposit, 75),
				
				(call_script, "script_gpu_create_button", "str_hub_button_withdrawal", 890, ":pos_y", hub2_obj_button_treasury_withdraw), # Treasury Withdraw
				(call_script, "script_gpu_resize_object", hub2_obj_button_treasury_withdraw, 75),
				(val_sub, ":pos_y", 30),
				(call_script, "script_gpu_create_button", "str_hub_button_increase", 770, ":pos_y", hub2_obj_button_allocation_increase), # Allocation change
				(call_script, "script_gpu_resize_object", hub2_obj_button_allocation_increase, 75),
				(store_add, ":pos_y_temp", ":pos_y", 12),
				(call_script, "script_gpu_create_text_label", "str_hub_button_allocation", ":x_center", ":pos_y_temp", 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_gpu_create_button", "str_hub_button_decrease", 915, ":pos_y", hub2_obj_button_allocation_decrease), # Allocation change
				(call_script, "script_gpu_resize_object", hub2_obj_button_allocation_decrease, 75),
			(try_end),
			
			#######################################
			###   GARRISON RECRUITMENT SLIDER   ###
			#######################################
			
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"), # Secondary block in the event player views this in cheat mode.
				
				(assign, ":pos_y", 400),
				(assign, ":x_left", 770),
				(store_add, ":x_center", ":x_left", 90),
				(store_add, ":x_apply", ":x_left", 70),
				
				(str_store_string, s21, "@Recruiting Budget"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", ":pos_y", 0, gpu_center),
				(val_sub, ":pos_y", 25),
				(assign, reg21, 0),
				(assign, reg22, 0),
				(party_get_slot, ":garrison_budget", "$current_town", slot_party_queue_budget),
				(assign, reg21, ":garrison_budget"),
				(str_store_string, s21, "@{reg21} Denars"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", ":pos_y", hub2_obj_text_recruiting_changes, gpu_center),
				(call_script, "script_gpu_resize_object", hub2_obj_text_recruiting_changes, 75),
				(val_sub, ":pos_y", 40),
				# Create the slider.
				(call_script, "script_gpu_create_slider", 0, 5000, ":x_left", ":pos_y", hub2_obj_slider_garrison_recruiting, hub2_val_slider_garrison_recruiting),
				(call_script, "script_gpu_resize_object", hub2_obj_slider_garrison_recruiting, 75),
				(overlay_set_val, reg1, ":garrison_budget"),
				(val_sub, ":pos_y", 30),
				(str_store_string, s21, "@Apply"),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":x_apply", ":pos_y", hub2_obj_button_recruiting_apply), # Treasury Deposit
				(call_script, "script_gpu_resize_object", hub2_obj_button_recruiting_apply, 75),
				(overlay_set_display, reg1, 0),
			(try_end),
			
			#######################################
			###    GARRISON TRAINING SLIDER     ###
			#######################################
			
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"), # Secondary block in the event player views this in cheat mode.
				
				(assign, ":pos_y", 280),
				(assign, ":x_left", 770),
				(store_add, ":x_center", ":x_left", 90),
				(store_add, ":x_apply", ":x_left", 70),
				
				(str_store_string, s21, "@Training Budget"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", ":pos_y", 0, gpu_center),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", ":pos_y", 0, gpu_center),
				(val_sub, ":pos_y", 25),
				(assign, reg21, 0),
				(assign, reg22, 0),
				(party_get_slot, ":garrison_budget", "$current_town", slot_center_training_budget),
				(assign, reg21, ":garrison_budget"),
				(str_store_string, s21, "@{reg21} Denars"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_center", ":pos_y", hub2_obj_text_training_changes, gpu_center),
				(call_script, "script_gpu_resize_object", hub2_obj_text_training_changes, 75),
				(val_sub, ":pos_y", 40),
				# Create the slider.
				(call_script, "script_gpu_create_slider", 0, 5000, ":x_left", ":pos_y", hub2_obj_slider_garrison_training, hub2_val_slider_garrison_training),
				(call_script, "script_gpu_resize_object", hub2_obj_slider_garrison_training, 75),
				(overlay_set_val, reg1, ":garrison_budget"),
				(val_sub, ":pos_y", 30),
				(str_store_string, s21, "@Apply"),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":x_apply", ":pos_y", hub2_obj_button_training_apply), # Treasury Deposit
				(call_script, "script_gpu_resize_object", hub2_obj_button_training_apply, 75),
				(overlay_set_display, reg1, 0),
			(try_end),
			
			## DETERMINE THE NUMBER OF LINES FOR SCROLLING ##
			(assign, ":num_lines", 9), # 3 titles + 3 spaces, rent, funds to player
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_player_enterprise, 1),
				(is_between, "$current_town", towns_begin, towns_end),
				(val_add, ":num_lines", 2), # Enterprise + Header
			(try_end),
			# Add in improvement lines.
			(call_script, "script_hub_display_improvements", "$current_town", 3, 0, 0, 0),
			(val_add, ":num_lines", reg2),
			# Add in patrols
			(try_begin),
				# Get patrol payment info.
				(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_1, 1),
				(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
				(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
				(val_add, ":num_lines", 1), # Header
				(try_begin),
					(party_slot_ge, "$current_town", slot_center_patrol_party_1, 1),
					(val_add, ":num_lines", 1),
				(try_end),
				(try_begin),
					(party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
					(val_add, ":num_lines", 1),
				(try_end),
				(try_begin),
					(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
					(val_add, ":num_lines", 1),
				(try_end),
			(try_end),
			# Add in town type specific lines.
			(try_begin),
				(party_slot_eq, "$current_town", slot_party_type, spt_town),
				# prisoner caravans, tariffs, treasury x4, garrison training & recruitment
				(val_add, ":num_lines", 8),
			(else_try),
				(party_slot_eq, "$current_town", slot_party_type, spt_castle),
				# prisoner caravans, treasury x4, garrison training & recruitment
				(val_add, ":num_lines", 7),
			(else_try),
				(party_slot_eq, "$current_town", slot_party_type, spt_village),
				(val_add, ":num_lines", 0),
			(try_end),
			# Kingdom Setting - Center Income
			(store_faction_of_party, ":faction_no", "$current_town"),
			(try_begin),
				(neg|faction_slot_eq, ":faction_no", slot_faction_center_income, 0),
				(val_add, ":num_lines", 1),
			(try_end),
			# Kingdom Setting - Tariff Income
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(neg|faction_slot_eq, ":faction_no", slot_faction_center_tariffs, 0),
				(val_add, ":num_lines", 1),
			(try_end),
			# Kingdom Setting - Troop Wages
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(neg|faction_slot_eq, ":faction_no", slot_faction_troop_wages, 0),
				(val_add, ":num_lines", 1),
			(try_end),
			# Castle Steward Bonuses
			(assign, ":cs_tariff_income", 0),
			(assign, ":cs_patrol_discount", 0),
			(try_begin),
				(party_get_slot, ":advisor_no", "$current_town", slot_center_steward),
				(is_between, ":advisor_no", companions_begin, companions_end),
				
				## Check for Tariff Income
				(try_begin),
					## TROOP EFFECT: BONUS_ADMINISTRATOR in Castle Steward position reduces tax inefficiency by 1% per point of intelligence.
					(call_script, "script_cf_ce_troop_has_ability", ":advisor_no", BONUS_ADMINISTRATOR), # combat_scripts.py - ability constants in combat_constants.py
					(val_add, ":num_lines", 1),
					(assign, ":cs_tariff_income", 1),
				(try_end),
				
				## Check for Patrol Cost Reduction
				(try_begin),
					(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_1, 1),
					(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
					(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
					## TROOP EFFECT: BONUS_EFFICIENT in Castle Steward position reduces the cost of regional patrols by 2% per point of leadership.
					(call_script, "script_cf_ce_troop_has_ability", ":advisor_no", BONUS_EFFICIENT), # combat_scripts.py - ability constants in combat_constants.py
					(val_add, ":num_lines", 1),
					(assign, ":cs_patrol_discount", 1),
				(try_end),
			(try_end),
			
			(assign, ":left_margin", 5),
			(assign, ":pos_x_col_2", 280), # Right-justify.  Actual value.
			(assign, ":pos_x_col_3", 283), # Left-justify.  Description of value.  Denars / Denars per week.
			(assign, ":line_step", 25),
			(store_mul, ":pos_y", ":num_lines", ":line_step"),
			(val_max, ":pos_y", 400), # Set a minimum to keep things at the top of the screen.
			
			(assign, ":net_change_player", 0),
			(assign, ":net_change_treasury", 0),
			
			###############
			### INCOMES ###
			###############
			
			(assign, ":y_bottom", 80),
			(assign, ":x_left",  240),
			(assign, ":x_width", 485),
			(assign, ":y_width", 530),
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", hub_obj_container_3),
				# Place keeper.
				(str_store_string, s22, "@ "),
				(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
				(val_sub, ":pos_y", 20),
				
				(call_script, "script_gpu_create_text_label", "str_hub_incomes", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_create_text_label", "str_hub_incomes", ":left_margin", ":pos_y", 0, gpu_left),
				#(overlay_set_color, reg1, ":color_income"),
				
				## ACCUMULATED RENTS ##
				(try_begin),
					#(is_between, "$current_town", towns_begin, towns_end), # Unnecessary
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_income_rent", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(call_script, "script_hub_get_center_income", "$current_town"),
					(val_add, ":net_change_player", reg1),
					(call_script, "script_hub_get_fund_string", reg1, 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				## * FACTION SETTING: CENTER INCOME ##
				(try_begin),
					(neg|faction_slot_eq, ":faction_no", slot_faction_center_income, 0),
					(val_sub, ":pos_y", ":line_step"),
					# Print description.
					(call_script, "script_gpu_create_text_label", "str_hub_faction_center_income", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					# Determine value.
					(faction_get_slot, reg21, ":faction_no", slot_faction_center_income),
					# Print value.
					(call_script, "script_hub_get_fund_string", reg21, 2, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					# Print unit type data.
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				## * IMPROVEMENTS THAT AFFECT RENT ##
				(assign, reg1, ":pos_y"),
				(call_script, "script_hub_display_improvements", "$current_town", 0, ":left_margin", ":pos_x_col_2", ":pos_x_col_3"),
				(assign, ":pos_y", reg1),
				
				## ACCUMULATED TARIFFS ##
				(try_begin),
					(is_between, "$current_town", towns_begin, towns_end),
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_income_tariffs", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(call_script, "script_hub_get_center_tariffs", "$current_town"),
					(val_add, ":net_change_player", reg1),
					(call_script, "script_hub_get_fund_string", reg1, 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
				(try_end),
				
				## * CASTLE STEWARD: TARIFF INCOME BONUS
				(try_begin),
					(eq, ":cs_tariff_income", 1),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(party_get_slot, ":castle_steward", "$current_town", slot_center_steward),
					(is_between, ":castle_steward", companions_begin, companions_end),
					(try_begin),
						## TROOP EFFECT: BONUS_ADMINISTRATOR in Castle Steward position improves center trade income by 1% per point of Trade.
						(call_script, "script_cf_ce_troop_has_ability", ":castle_steward", BONUS_ADMINISTRATOR), # combat_scripts.py - ability constants in combat_constants.py
						(store_skill_level, ":trade_bonus", "skl_trade", ":castle_steward"),
					(try_end),
					# Output
					(val_sub, ":pos_y", ":line_step"),
					(str_store_string, s21, "@ * Castle Steward: Tariff Income"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(call_script, "script_hub_get_fund_string", ":trade_bonus", 2, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(str_store_string, s22, "@{s22}  (Administrator Bonus)"),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				## * FACTION SETTING: TARIFF INCOME ##
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(neg|faction_slot_eq, ":faction_no", slot_faction_center_tariffs, 0),
					(val_sub, ":pos_y", ":line_step"),
					# Print description.
					(call_script, "script_gpu_create_text_label", "str_hub_faction_tariff_income", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					# Determine value.
					(faction_get_slot, reg21, ":faction_no", slot_faction_center_tariffs),
					# Print value.
					(call_script, "script_hub_get_fund_string", reg21, 2, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					# Print unit type data.
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				## * IMPROVEMENTS THAT AFFECT TARIFFS ##
				(assign, reg1, ":pos_y"),
				(call_script, "script_hub_display_improvements", "$current_town", 1, ":left_margin", ":pos_x_col_2", ":pos_x_col_3"),
				(assign, ":pos_y", reg1),
				
				## PRISONER CARAVANS ##
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_income_prisoners", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(party_get_slot, reg21, "$current_town", slot_party_wealth),
					(val_add, ":net_change_player", reg21),
					(call_script, "script_hub_get_fund_string", reg21, 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
				(try_end),
				
				## ENTERPRISE ##
				(try_begin),
					(is_between, "$current_town", towns_begin, towns_end),
					(call_script, "script_cf_hub_get_center_enterprise", "$current_town"),
					(assign, ":net_profit", reg1),
					(val_add, ":net_change_player", ":net_profit"),
					
					## HEADER ##
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_investments", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					(party_get_slot, ":enterprise_output", "$current_town", slot_center_player_enterprise),
					(call_script, "script_get_enterprise_name", ":enterprise_output"),
					(str_store_string, s21, reg0),
					
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_improvement", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					(call_script, "script_hub_get_fund_string", ":net_profit", 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
				(try_end),
				
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					## TREASURY ALLOTMENT ##
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_treasury_income", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					# Get rent info.
					(party_get_slot, reg21, "$current_town", slot_center_income_to_treasury),
					(val_add, ":net_change_treasury", reg21),
					(val_sub, ":net_change_player", reg21),
					(call_script, "script_hub_get_fund_string", reg21, 1, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
				(try_end),
				
					
				################
				### EXPENSES ###
				################
				(val_sub, ":pos_y", ":line_step"),
				(val_sub, ":pos_y", ":line_step"),
				(call_script, "script_gpu_create_text_label", "str_hub_expenses", ":left_margin", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_create_text_label", "str_hub_expenses", ":left_margin", ":pos_y", 0, gpu_left),
				
				## GARRISON WAGES ##
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_expense_wages", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(call_script, "script_hub_get_party_wages", "$current_town", 1),
					(val_add, ":net_change_player", reg1),
					(call_script, "script_hub_get_fund_string", reg1, 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
				(try_end),
				
				## * FACTION SETTING: TROOP WAGES ##
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(neg|faction_slot_eq, ":faction_no", slot_faction_troop_wages, 0),
					(val_sub, ":pos_y", ":line_step"),
					# Print description.
					(call_script, "script_gpu_create_text_label", "str_hub_faction_troop_wages", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					# Determine value.
					(faction_get_slot, reg21, ":faction_no", slot_faction_troop_wages),
					# Print value.
					(call_script, "script_hub_get_fund_string", reg21, 2, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					# Print unit type data.
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				
				## REGIONAL PATROLS ##
				(try_begin),
					# Get patrol payment info.
					(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_1, 1),
					(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
					(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
					
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_expense_patrols", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(assign, ":pos_y_temp", ":pos_y"), # Stored for later use of showing patrol totals.
					(assign, ":patrol_count", -1), # Start at -1 so we don't have to reduce this by 1 later for display purposes.
					(assign, ":patrol_upkeep", 0),
					(try_for_range, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
						(party_get_slot, ":party_no", "$current_town", ":slot_no"),
						(ge, ":party_no", 1),
						(party_is_active, ":party_no"),
						(val_add, ":patrol_count", 1),
						(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DETERMINE_COST),
						(val_mul, reg1, -1), # Flip our sign around.
						(val_add, ":patrol_upkeep", reg1),
						(assign, ":patrol_cost", reg1),
						# Display each patrol as its own line.
						(val_sub, ":pos_y", ":line_step"),
						(store_add, reg21, ":patrol_count", 1),
						(call_script, "script_gpu_create_text_label", "str_hub_expense_patrol_no", ":left_margin", ":pos_y", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						(call_script, "script_hub_get_fund_string", ":patrol_cost", 1, 0),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
						(call_script, "script_gpu_resize_object", 0, 75),
						(overlay_set_color, reg1, reg51),
						(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
					
					(try_end),
					#(val_mul, ":patrol_upkeep", -1),
					(val_add, ":net_change_player", ":patrol_upkeep"),
					(call_script, "script_hub_get_fund_string", ":patrol_upkeep", 1, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y_temp", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y_temp", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## * CASTLE STEWARD: PATROL DISCOUNT BONUS
					(try_begin),
						(eq, ":cs_patrol_discount", 1),
						(is_between, "$current_town", walled_centers_begin, walled_centers_end),
						(party_get_slot, ":advisor_no", "$current_town", slot_center_steward),
						(is_between, ":advisor_no", companions_begin, companions_end),
						(try_begin),
							## TROOP EFFECT: BONUS_EFFICIENT in Castle Steward position improves center trade income by 1% per point of Trade.
							(call_script, "script_cf_ce_troop_has_ability", ":advisor_no", BONUS_EFFICIENT), # combat_scripts.py - ability constants in combat_constants.py
							(store_skill_level, ":leadership_bonus", "skl_leadership", ":advisor_no"),
							(store_mul, ":patrol_discount", ":leadership_bonus", efficient_patrol_discount),
						(try_end),
						# Output
						(val_sub, ":pos_y", ":line_step"),
						(str_store_string, s21, "@ * Castle Steward: Patrol Discount"),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":left_margin", ":pos_y", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
						(call_script, "script_hub_get_fund_string", ":patrol_discount", 2, 0),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
						(call_script, "script_gpu_resize_object", 0, 75),
						(overlay_set_color, reg1, reg51),
						(str_store_string, s22, "@{s22}  (Efficient Bonus)"),
						(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
						(call_script, "script_gpu_resize_object", 0, 75),
					(try_end),
				(try_end),
				
				## GARRISON RECRUITMENT ##
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_expense_recruitment", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(try_begin),
						(party_slot_eq, "$current_town", slot_center_recruiting, 1), # Recruiting is enabled.
						(party_get_slot, reg21, "$current_town", slot_party_queue_budget),
					(else_try),
						(assign, reg21, 0),
					(try_end),
					(val_sub, ":net_change_treasury", reg21),
					(call_script, "script_hub_get_fund_string", reg21, 3, 1),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				## GARRISON RECRUITMENT ##
				
				## GARRISON TRAINING ##
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_expense_training", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(try_begin),
						(party_slot_eq, "$current_town", slot_center_upgrade_garrison, 1), # Training is enabled.
						(party_get_slot, reg21, "$current_town", slot_center_training_budget),
					(else_try),
						(assign, reg21, 0),
					(try_end),
					(val_sub, ":net_change_treasury", reg21),
					(call_script, "script_hub_get_fund_string", reg21, 3, 1),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
				## GARRISON TRAINING ##
				
				
				################
				### TREASURY ###
				################
				(try_begin),
					(is_between, "$current_town", walled_centers_begin, walled_centers_end),
					#(assign, ":color_treasury", gpu_yellow),
					
					## TREASURY HEADER ##
					(val_sub, ":pos_y", ":line_step"),
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_total", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_create_text_label", "str_hub_total", ":left_margin", ":pos_y", 0, gpu_left),
					#(overlay_set_color, reg1, ":color_treasury"),
				
					## CURRENT BALANCE ##
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_treasury_balance", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					# Get rent info.
					(party_get_slot, reg21, "$current_town", slot_center_treasury),
					(call_script, "script_hub_get_fund_string", reg21, 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## NET CHANGE ##
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_net_change", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(call_script, "script_hub_get_fund_string", ":net_change_treasury", 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## PROJECTED BALANCE ##
					(val_sub, ":pos_y", ":line_step"),
					(call_script, "script_gpu_create_text_label", "str_hub_treasury_projection", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					# Get rent info.
					(party_get_slot, reg21, "$current_town", slot_center_treasury),
					(val_add, reg21, ":net_change_treasury"),
					(call_script, "script_hub_get_fund_string", reg21, 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
					## NET CHANGE SENT TO PLAYER ##
					(val_sub, ":pos_y", ":line_step"),
					(str_store_string, s21, "@Funds Sent to You"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					(call_script, "script_hub_get_fund_string", ":net_change_player", 0, 0),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, reg51),
					(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					
				(try_end),
				
			(set_container_overlay, -1),
		]),
	
    (ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(presentation_set_duration, 0),
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(jump_to_menu, "mnu_town"),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(jump_to_menu, "mnu_village"),
			(try_end),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
		[
			(store_trigger_param_1, ":object"),
			(store_trigger_param_2, ":value"),
			
			(call_script, "script_hub_handle_mode_switching_buttons", ":object", ":value"),
			
			(try_begin),
				### SLIDER - TREASURY DEPOSIT / WITHDRAWAL ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_slider_treasury, ":object"),
				(troop_set_slot, HUB_OBJECTS, hub2_val_slider_treasury, ":value"),
				(overlay_set_val, ":object", ":value"),
				(troop_get_slot, ":obj_label", HUB_OBJECTS, hub2_obj_treasury_changes),
				(assign, reg21, ":value"),
				(try_begin),
					(ge, ":value", 0),
					(assign, reg22, 0),
					
				(else_try),
					(lt, ":value", 0),
					(assign, reg22, 1),
					
				(try_end),
				(overlay_set_text, ":obj_label", "str_hub_label_treasury_value"),
				
			(else_try),
				### BUTTON - TREASURY DEPOSIT ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_button_treasury_deposit, ":object"),
				(troop_get_slot, ":transfer", HUB_OBJECTS, hub2_val_slider_treasury),
				(try_begin),
					(call_script, "script_cf_diplomacy_treasury_verify_funds", ":transfer", "$current_town", FUND_FROM_PLAYER, TREASURY_FUNDS_AVAILABLE),
					(call_script, "script_diplomacy_treasury_deposit_funds", ":transfer", "$current_town"),
					(start_presentation, "prsnt_hub_finances"),
				(else_try),
					(display_message, "@You do not have that many denars available to deposit.", gpu_red),
				(try_end),
				
			(else_try),
				### BUTTON - TREASURY WITHDRAWAL ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_button_treasury_withdraw, ":object"),
				(troop_get_slot, ":transfer", HUB_OBJECTS, hub2_val_slider_treasury),
				(try_begin),
					(call_script, "script_cf_diplomacy_treasury_verify_funds", ":transfer", "$current_town", FUND_FROM_TREASURY, TREASURY_FUNDS_AVAILABLE),
					(call_script, "script_diplomacy_treasury_withdraw_funds", ":transfer", "$current_town", FUND_FROM_TREASURY_TO_PLAYER),
					(start_presentation, "prsnt_hub_finances"),
				(else_try),
					(display_message, "@You do not have that many denars available to withdraw.", gpu_red),
				(try_end),
				
			(else_try),
				### BUTTON - TREASURY ALLOCATION INCREASE ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_button_allocation_increase, ":object"),
				(party_get_slot, ":setting", "$current_town", slot_center_income_to_treasury),
				(val_add, ":setting", 250),
				(party_set_slot, "$current_town", slot_center_income_to_treasury, ":setting"),
				(start_presentation, "prsnt_hub_finances"),
				
			(else_try),
				### BUTTON - TREASURY ALLOCATION DECREASE ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_button_allocation_decrease, ":object"),
				(party_get_slot, ":setting", "$current_town", slot_center_income_to_treasury),
				(try_begin),
					(ge, ":setting", 1),
					(val_sub, ":setting", 250),
					(val_max, ":setting", 0),
					(party_set_slot, "$current_town", slot_center_income_to_treasury, ":setting"),
					(start_presentation, "prsnt_hub_finances"),
				(try_end),
				
			(else_try),
				### SLIDER - GARRISON RECRUITMENT ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_slider_garrison_recruiting, ":object"),
				(troop_set_slot, HUB_OBJECTS, hub2_val_slider_garrison_recruiting, ":value"),
				(overlay_set_val, ":object", ":value"),
				(troop_get_slot, ":obj_label", HUB_OBJECTS, hub2_obj_text_recruiting_changes),
				(assign, reg21, ":value"),
				(str_store_string, s21, "@{reg21} Denars"),
				(overlay_set_text, ":obj_label", "str_hub_s21"),
				# Display Apply Button
				(troop_get_slot, ":obj_apply", HUB_OBJECTS, hub2_obj_button_recruiting_apply),
				(overlay_set_display, ":obj_apply", 1),
				
			(else_try),
				### BUTTON - GARRISON RECRUITMENT BUDGET APPLY ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_button_recruiting_apply, ":object"),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub2_val_slider_garrison_recruiting),
				(party_set_slot, "$current_town", slot_party_queue_budget, ":setting"),
				# Enable garrison recruiting if a value other than 0 is set.
				(try_begin),
					(ge, ":setting", 1),
					(party_set_slot, "$current_town", slot_center_recruiting, 1), # Enable garrison recruiting.
				(else_try),
					(party_set_slot, "$current_town", slot_center_recruiting, 0), # Disable garrison recruiting.
				(try_end),
				(start_presentation, "prsnt_hub_finances"),
				
			(else_try),
				### SLIDER - GARRISON TRAINING ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_slider_garrison_training, ":object"),
				(troop_set_slot, HUB_OBJECTS, hub2_val_slider_garrison_training, ":value"),
				(overlay_set_val, ":object", ":value"),
				(troop_get_slot, ":obj_label", HUB_OBJECTS, hub2_obj_text_training_changes),
				(assign, reg21, ":value"),
				(str_store_string, s21, "@{reg21} Denars"),
				(overlay_set_text, ":obj_label", "str_hub_s21"),
				# Display Apply Button
				(troop_get_slot, ":obj_apply", HUB_OBJECTS, hub2_obj_button_training_apply),
				(overlay_set_display, ":obj_apply", 1),
				
			(else_try),
				### BUTTON - GARRISON TRAINING BUDGET APPLY ###
				(troop_slot_eq, HUB_OBJECTS, hub2_obj_button_training_apply, ":object"),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub2_val_slider_garrison_training),
				(party_set_slot, "$current_town", slot_center_training_budget, ":setting"),
				# Enable garrison training if a value other than 0 is set.
				(try_begin),
					(ge, ":setting", 1),
					(party_set_slot, "$current_town", slot_center_upgrade_garrison, 1), # Enable garrison training.
				(else_try),
					(party_set_slot, "$current_town", slot_center_upgrade_garrison, 0), # Disable garrison training.
				(try_end),
				(start_presentation, "prsnt_hub_finances"),
				
			(try_end),
		]),
    ]),

	
	
	
	
###########################################################################################################################
#####                                                  IMPROVEMENTS                                                   #####
###########################################################################################################################

("hub_improvements", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_hub_create_mode_switching_buttons"),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			# OBJ - Warning note.
			# (call_script, "script_gpu_create_text_label", "str_hub_label_construction", 500, 635, 0, gpu_center),
			# (call_script, "script_gpu_resize_object", 0, 75),
			
			# script_gpu_create_slider       - min, max, pos_x, pos_y, storage_id, value_id
			#                                     Xw   Yw   Xp    Yp
			# (call_script, "script_gpu_draw_line", 530, 200, 220, 410, gpu_white),  ### UPPER IMPROVEMENT CONSTRUCTION AREA ###
			# (call_script, "script_gpu_draw_line", 530, 310, 220,  80, gpu_white),  ### BOTTOM IMPROVEMENT INFO AREA ###
			# (call_script, "script_gpu_draw_line", 200, 530, 760,  80, gpu_white),  ### RIGHT IMPROVEMENT LIST AREA ###
			
			(assign, ":y_button_step", 50),
			(assign, ":pos_y", 570),
			(assign, ":x_numerals", 240),
			(assign, ":x_imp_name", 280),
			(assign, ":x_days_left", 640),
			(assign, ":x_cancel", 665),
			#(call_script, "script_gpu_draw_line", 530, 1, 220,  575, gpu_gray),  ### LEVELING LINE ###
			
			############################################
			###       IMPROVEMENT CONSTRUCTION       ###
			############################################
			
			#### IMPROVEMENT CONSTRUCTION #1 ####
			(str_store_string, s21, "@#1"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_numerals", ":pos_y", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 150),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_numerals", ":pos_y", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 150),
			(try_begin),
				# Check if we have a valid improvement being built and acquire that information.
				(neg|party_slot_eq, "$current_town", slot_center_current_improvement_1, 0),
				(party_get_slot, ":improvement_no", "$current_town", slot_center_current_improvement_1),
				(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
				(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
				# Improvement is valid continue on.
				(call_script, "script_building_slot_get_days_to_complete", "$current_town", slot_center_current_improvement_1), # improvements_scripts.py
				(assign, ":days_left", reg1),
				(assign, ":improvement_no", reg2),
				## OBJ - IMPROVEMENT BEING BUILT IN SLOT #1
				(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
				(str_store_string, s21, s0),
				(store_add, ":pos_y_text", ":pos_y", 7),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_imp_name", ":pos_y_text", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				## OBJ - DAYS LEFT
				(assign, reg21, ":days_left"),
				(store_sub, reg22, reg21, 1),
				(party_get_slot, ":time_end", "$current_town", slot_center_improvement_end_hour_1),
				(party_get_slot, ":time_start", "$current_town", slot_center_improvement_start_hour_1),
				(store_sub, ":time_total", ":time_end", ":time_start"),
				(val_div, ":time_total", 24),
				(assign, reg23, ":time_total"),
				(call_script, "script_gpu_create_text_label", "str_hub_build_days_left", ":x_days_left", ":pos_y_text", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				## OBJ - CANCEL BUTTON #1
				(store_add, ":pos_y_button", ":pos_y", -4),
				(call_script, "script_gpu_create_button", "str_hub_build_cancel", ":x_cancel", ":pos_y_button", hub3_obj_button_cancel_const_1),
				(call_script, "script_gpu_resize_object", hub3_obj_button_cancel_const_1, 75),
			(else_try),
				## OBJ - EMPTY
				(store_add, ":pos_y_text", ":pos_y", 7),
				(call_script, "script_gpu_create_text_label", "str_hub_improvement_empty", ":x_imp_name", ":pos_y_text", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, gpu_gray),
			(try_end),
			
			#### IMPROVEMENT CONSTRUCTION #2 ####
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@#2"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_numerals", ":pos_y", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 150),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_numerals", ":pos_y", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 150),
			(try_begin),
				# Check if we have a valid improvement being built and acquire that information.
				(neg|party_slot_eq, "$current_town", slot_center_current_improvement_2, 0),
				(party_get_slot, ":improvement_no", "$current_town", slot_center_current_improvement_2),
				(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
				(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
				# Improvement is valid continue on.
				(call_script, "script_building_slot_get_days_to_complete", "$current_town", slot_center_current_improvement_2), # improvements_scripts.py
				(assign, ":days_left", reg1),
				(assign, ":improvement_no", reg2),
				## OBJ - IMPROVEMENT BEING BUILT IN SLOT #1
				(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
				(str_store_string, s21, s0),
				(store_add, ":pos_y_text", ":pos_y", 7),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_imp_name", ":pos_y_text", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				## OBJ - DAYS LEFT
				(assign, reg21, ":days_left"),
				(store_sub, reg22, reg21, 1),
				(party_get_slot, ":time_end", "$current_town", slot_center_improvement_end_hour_2),
				(party_get_slot, ":time_start", "$current_town", slot_center_improvement_start_hour_2),
				(store_sub, ":time_total", ":time_end", ":time_start"),
				(val_div, ":time_total", 24),
				(assign, reg23, ":time_total"),
				(call_script, "script_gpu_create_text_label", "str_hub_build_days_left", ":x_days_left", ":pos_y_text", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				## OBJ - CANCEL BUTTON #2
				(store_add, ":pos_y_button", ":pos_y", -4),
				(call_script, "script_gpu_create_button", "str_hub_build_cancel", ":x_cancel", ":pos_y_button", hub3_obj_button_cancel_const_2),
				(call_script, "script_gpu_resize_object", hub3_obj_button_cancel_const_2, 75),
			(else_try),
				## OBJ - EMPTY
				(store_add, ":pos_y_text", ":pos_y", 7),
				(call_script, "script_gpu_create_text_label", "str_hub_improvement_empty", ":x_imp_name", ":pos_y_text", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, gpu_gray),
			(try_end),
			
			#### IMPROVEMENT CONSTRUCTION #3 ####
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@#3"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_numerals", ":pos_y", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 150),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_numerals", ":pos_y", 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 150),
			(try_begin),
				# Check if we have a valid improvement being built and acquire that information.
				(neg|party_slot_eq, "$current_town", slot_center_current_improvement_3, 0),
				(party_get_slot, ":improvement_no", "$current_town", slot_center_current_improvement_3),
				(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
				(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
				# Improvement is valid continue on.
				(call_script, "script_building_slot_get_days_to_complete", "$current_town", slot_center_current_improvement_3), # improvements_scripts.py
				(assign, ":days_left", reg1),
				(assign, ":improvement_no", reg2),
				## OBJ - IMPROVEMENT BEING BUILT IN SLOT #1
				(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
				(str_store_string, s21, s0),
				(store_add, ":pos_y_text", ":pos_y", 7),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_imp_name", ":pos_y_text", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				## OBJ - DAYS LEFT
				(assign, reg21, ":days_left"),
				(store_sub, reg22, reg21, 1),
				(party_get_slot, ":time_end", "$current_town", slot_center_improvement_end_hour_3),
				(party_get_slot, ":time_start", "$current_town", slot_center_improvement_start_hour_3),
				(store_sub, ":time_total", ":time_end", ":time_start"),
				(val_div, ":time_total", 24),
				(assign, reg23, ":time_total"),
				(call_script, "script_gpu_create_text_label", "str_hub_build_days_left", ":x_days_left", ":pos_y_text", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				## OBJ - CANCEL BUTTON #3
				(store_add, ":pos_y_button", ":pos_y", -4),
				(call_script, "script_gpu_create_button", "str_hub_build_cancel", ":x_cancel", ":pos_y_button", hub3_obj_button_cancel_const_3),
				(call_script, "script_gpu_resize_object", hub3_obj_button_cancel_const_3, 75),
			(else_try),
				## OBJ - EMPTY
				(store_add, ":pos_y_text", ":pos_y", 7),
				(call_script, "script_gpu_create_text_label", "str_hub_improvement_empty", ":x_imp_name", ":pos_y_text", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, gpu_gray),
			(try_end),
			
			#######################################################
			###       IMPROVEMENT DESCRIPTION & SELECTION       ###
			#######################################################
			
			## OBJ - IMPROVEMENT SELECTION SLIDER
			(store_sub, ":native_span", native_improvements_end, native_improvements_begin),
			(store_sub, ":lower_limit", center_improvements_begin, ":native_span"),
			(troop_set_slot, HUB_OBJECTS, hub3_val_slider_improvement_selector, center_improvements_begin), ### FOR BUILDING.  NEEDS REMOVAL ###
			(call_script, "script_gpu_create_slider", ":lower_limit", center_improvements_end, 355, 320, hub3_obj_slider_improvement_selector, hub3_val_slider_improvement_selector),
			
			## DETERMINE THE IMPROVEMENT WE'RE WORKING WITH.
			(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_slider_improvement_selector),
			(try_begin), # Fix our out of place native improvements.
				(lt, ":setting", center_improvements_begin),
				(store_sub, ":offset", ":setting", ":lower_limit"),
				(store_add, ":improvement_no", native_improvements_begin, ":offset"),
			(else_try),
				(assign, ":improvement_no", ":setting"),
			(try_end),
			
			## OBJ - IMPROVEMENT NAME
			(call_script, "script_gpu_create_text_label", "str_hub_label_construction", 480, 370, hub3_obj_label_improvement_name, gpu_center),
			#(call_script, "script_gpu_resize_object", hub3_obj_label_improvement_name, 85),
			## OBJ - IMPROVEMENT APPLICABILITY
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 480, 303, hub3_obj_label_improvement_applicable, gpu_center),
			(call_script, "script_gpu_resize_object", hub3_obj_label_improvement_applicable, 75),
			## OBJ - IMPROVEMENT DESC
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 215, hub3_obj_label_improvement_desc, gpu_center), # x = 235
			(call_script, "script_gpu_resize_object", hub3_obj_label_improvement_desc, 75),
			## OBJ - IMPROVEMENT TIME
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 480, 190, hub3_obj_label_improvement_time, gpu_center),
			(call_script, "script_gpu_resize_object", hub3_obj_label_improvement_time, 75),
			## OBJ - IMPROVEMENT COST
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 480, 170, hub3_obj_label_improvement_cost, gpu_center),
			(call_script, "script_gpu_resize_object", hub3_obj_label_improvement_cost, 75),
			
			## OBJ - IMPROVEMENT BUILD BUTTON
			(assign, ":improvement_is_buildable", 0),
			(assign, ":string_build", "str_hub_button_build"),
			(try_begin), # Repairing
				(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement_no"), # improvements_scripts.py
				(party_slot_ge, "$current_town", ":improvement_no", cis_built), # Capture repair attempts.
				(assign, ":string_build", "str_hub_button_repair"),
				(assign, ":improvement_is_buildable", 1),
			(else_try), # Building
				(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement_no"), # improvements_scripts.py
				(assign, ":improvement_is_buildable", 1),
			(try_end),
			(call_script, "script_gpu_create_texture_button", ":string_build", 370, 100, hub3_obj_button_improvement_build),
			(call_script, "script_gpu_set_button_status", hub3_obj_button_improvement_build, ":improvement_is_buildable"),
			
			## OBJ - IMPROVEMENT DESTROY BUTTON
			(assign, ":improvement_is_destroyable", 0),
			(try_begin),
				(party_slot_ge, "$current_town", ":improvement_no", cis_built),
				(assign, ":improvement_is_destroyable", 1),
			(else_try),
			(try_end),
			(call_script, "script_gpu_create_texture_button", "str_hub_button_destroy", 545, 100, hub3_obj_button_improvement_destroy),
			(call_script, "script_gpu_set_button_status", hub3_obj_button_improvement_destroy, ":improvement_is_destroyable"),
			
			## OBJ - IMPROVEMENT INSTANT COMPLETE (TESTING)
			(try_begin),
				(ge, DEBUG_IMPROVEMENTS, 1),
				(assign, ":improvement_in_progress", 0),
				(assign, ":string_build", "str_hub_button_build"),
				
				## DETERMINE THE IMPROVEMENT WE'RE WORKING WITH.
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_slider_improvement_selector),
				(try_begin), # Fix our out of place native improvements.
					(lt, ":setting", center_improvements_begin),
					(store_sub, ":offset", ":setting", ":lower_limit"),
					(store_add, ":improvement_no", native_improvements_begin, ":offset"),
				(else_try),
					(assign, ":improvement_no", ":setting"),
				(try_end),
				
				(try_begin), # Repairing
					(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement_no"), # improvements_scripts.py
					(party_slot_ge, "$current_town", ":improvement_no", cis_built), # Capture repair attempts.
					(assign, ":string_build", "str_hub_button_repair"),
					(assign, ":improvement_in_progress", 1),
				(else_try), # Building
					(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement_no"), # improvements_scripts.py
					(assign, ":improvement_in_progress", 1),
				(else_try), # In-Progress
					(this_or_next|party_slot_eq, "$current_town", slot_center_current_improvement_1, ":improvement_no"),
					(this_or_next|party_slot_eq, "$current_town", slot_center_current_improvement_2, ":improvement_no"),
					(party_slot_eq, "$current_town", slot_center_current_improvement_3, ":improvement_no"),
					(assign, ":improvement_in_progress", 1),
				(try_end),
				(call_script, "script_gpu_create_texture_button", ":string_build", 460, 55, hub3_obj_button_improvement_complete),
				(call_script, "script_gpu_set_button_status", hub3_obj_button_improvement_complete, ":improvement_in_progress"),
				
				(str_store_string, s21, "@INSTANTLY"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", 480, 45, 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 50),
			(try_end),
			
			(try_begin),
				(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
				(ge, reg1, 1),
				
				## OBJ - Header
				(str_store_string, s21, "@Silverstag Emblems"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", 850, 200, 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", 850, 200, 0, gpu_center),
				(call_script, "script_gpu_resize_object", 0, 75),
				
				### SILVERSTAG EMBLEMS ### - Dropdown Menu for reducing build speed.
				(create_combo_button_overlay, reg1),
				(troop_set_slot, HUB_OBJECTS, hub3_obj_menu_emblem_build_time, reg1),
				(position_set_x, pos1, 875),
				(position_set_y, pos1, 160),
				(overlay_set_position, reg1, pos1),
				(overlay_add_item, reg1, "@Use Normal Build Time"),
				(overlay_add_item, reg1, "@1 Emblem, -25% Build Time"),
				(overlay_add_item, reg1, "@2 Emblems, -50% Build Time"),
				(overlay_add_item, reg1, "@3 Emblems, Instant Build Time"),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_menu_emblem_build_time),
				(overlay_set_val, reg1, ":setting"),
				(call_script, "script_gpu_resize_object", hub3_obj_menu_emblem_build_time, 75),
				
				### SILVERSTAG EMBLEMS ### - Dropdown Menu for reducing build cost.
				(create_combo_button_overlay, reg1),
				(troop_set_slot, HUB_OBJECTS, hub3_obj_menu_emblem_build_cost, reg1),
				(position_set_x, pos1, 875),
				(position_set_y, pos1, 125),
				(overlay_set_position, reg1, pos1),
				(overlay_add_item, reg1, "@Pay Regular Cost"),
				(overlay_add_item, reg1, "@1 Emblem, -25% Build Cost"),
				(overlay_add_item, reg1, "@2 Emblems, -50% Build Cost"),
				(overlay_add_item, reg1, "@3 Emblems, No Build Cost"),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_menu_emblem_build_cost),
				(overlay_set_val, reg1, ":setting"),
				(call_script, "script_gpu_resize_object", hub3_obj_menu_emblem_build_cost, 75),
			(else_try),
				(troop_set_slot, HUB_OBJECTS, hub3_val_menu_emblem_build_time, 0),
				(troop_set_slot, HUB_OBJECTS, hub3_val_menu_emblem_build_cost, 0),
			(try_end),
			
			####################################
			###       IMPROVEMENT LIST       ###
			####################################
			
			(assign, ":y_bottom", 80),
			(assign, ":x_left",  735),
			(assign, ":x_width", 245),
			(assign, ":y_width", 500),
			#(call_script, "script_gpu_draw_line", ":x_width", ":y_width", ":x_left",  ":y_bottom", gpu_white),  ### RIGHT IMPROVEMENT LIST AREA ###
			(call_script, "script_gpu_container_heading", ":x_left", ":y_bottom", ":x_width", ":y_width", hub_obj_container_3),
				(assign, ":pos_y", 400),
				(assign, ":left_margin", 0),
				(assign, ":line_step", 20),
				
				## HEADER ##
				(store_div, ":x_center", ":x_width", 2),
				(call_script, "script_gpu_create_text_label", "str_hub_improvements_caps", ":x_center", ":pos_y", 0, gpu_center),
				# Doubled for bold effect.
				(call_script, "script_gpu_create_text_label", "str_hub_improvements_caps", ":x_center", ":pos_y", 0, gpu_center),
				(val_sub, ":pos_y", 5),
				
				## CURRENT IMPROVEMENTS ##
				(try_for_range, ":improvement_no", native_improvements_begin, center_improvements_end),
					(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
					(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
					## Can this be built here?
					(call_script, "script_get_improvement_details", ":improvement_no"),
					(str_store_string, s41, s0), # Name
					(assign, ":allowable_locations", reg1),
					(party_get_slot, ":center_type", "$current_town", slot_party_type),
					(assign, ":continue", 0),
					(try_begin),
						(eq, ":allowable_locations", imp_allowed_in_any),
						(assign, ":continue", 1),
					(else_try),
						(eq, ":center_type", spt_village),
						(this_or_next|eq, ":allowable_locations", imp_allowed_in_village),
						(this_or_next|eq, ":allowable_locations", imp_allowed_in_village_town),
						(eq, ":allowable_locations", imp_allowed_in_village_castle),
						(assign, ":continue", 1),
					(else_try),
						(eq, ":center_type", spt_castle),
						(this_or_next|eq, ":allowable_locations", imp_allowed_in_castle),
						(this_or_next|eq, ":allowable_locations", imp_allowed_in_village_castle),
						(eq, ":allowable_locations", imp_allowed_in_walled_center),
						(assign, ":continue", 1),
					(else_try),
						(eq, ":center_type", spt_town),
						(this_or_next|eq, ":allowable_locations", imp_allowed_in_town),
						(this_or_next|eq, ":allowable_locations", imp_allowed_in_village_town),
						(eq, ":allowable_locations", imp_allowed_in_walled_center),
						(assign, ":continue", 1),
					(try_end),
					(eq, ":continue", 1), ## CONDITIONAL BREAK ## (account for everything above)
					
					## What condition is this in?
					
					# Assess damage to structure.
					(assign, ":color", gpu_black),
					(try_begin),
						(str_store_string, s11, "@ N/A"),
						(party_slot_ge, "$current_town", ":improvement_no", cis_built),
						(str_store_string, s11, "@ Finished"),
						(assign, ":color", 14336), # Dark Green
						(party_slot_ge, "$current_town", ":improvement_no", cis_damaged_20_percent),
						(str_store_string, s11, "@ Damaged"),
						(assign, ":color", 4980736), # Dark Red
						(eq, 1, 0), # Intentionally fail at this point.
					(else_try),
						(this_or_next|party_slot_eq, "$current_town", slot_center_current_improvement_1, ":improvement_no"),
						(this_or_next|party_slot_eq, "$current_town", slot_center_current_improvement_2, ":improvement_no"),
						(party_slot_eq, "$current_town", slot_center_current_improvement_3, ":improvement_no"),
						(assign, ":color", gpu_black),
						(str_store_string, s11, "@ Building"),
						(party_slot_ge, "$current_town", ":improvement_no", cis_built),
						(str_store_string, s11, "@ Repairing"),
					(try_end),
					(val_sub, ":pos_y", ":line_step"),
					## OBJ - Improvement Name
					(str_store_string, s21, s41),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":left_margin", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
					## OBJ - Improvement Status / Condition
					(store_sub, ":right_margin", ":x_width", 9),
					(str_store_string, s21, s11),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":right_margin", ":pos_y", 0, gpu_right),
					(call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, ":color"),
					
				(try_end),
			(set_container_overlay, -1),
			
			## UPDATE IMPROVEMENT OBJECTS
			(call_script, "script_hub_update_improvement_screen"),
		]),
	
    (ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(presentation_set_duration, 0),
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(jump_to_menu, "mnu_town"),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(jump_to_menu, "mnu_village"),
			(try_end),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_hub_handle_mode_switching_buttons", ":object", ":value"),
		
		## PRESENTATION EVENTS ##
		(try_begin),
			### SLIDER - IMPROVEMENT SELECTION ###
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_slider_improvement_selector, ":object"),
			(is_between, ":value", native_improvements_begin, center_improvements_end),
			(troop_set_slot, HUB_OBJECTS, hub3_val_slider_improvement_selector, ":value"),
			(call_script, "script_hub_update_improvement_screen"),
			
		(else_try),
			### MENU - EMBLEM BONUS - BUILD TIME ###
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_menu_emblem_build_time, ":object"),
			(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
			(assign, ":current_emblems", reg1),
			(troop_get_slot, ":used_emblems", HUB_OBJECTS, hub3_val_menu_emblem_build_cost),
			(val_sub, ":current_emblems", ":used_emblems"),
			(try_begin),
				(ge, ":current_emblems", ":value"),
				(troop_set_slot, HUB_OBJECTS, hub3_val_menu_emblem_build_time, ":value"),
				(call_script, "script_hub_update_improvement_screen"),
			(else_try),
				(display_message, "@You have insufficient emblems available to use that setting.", gpu_red),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_menu_emblem_build_time),
				(overlay_set_val, ":object", ":setting"),
			(try_end),
			
		(else_try),
			### MENU - EMBLEM BONUS - BUILD COST ###
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_menu_emblem_build_cost, ":object"),
			(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
			(assign, ":current_emblems", reg1),
			(troop_get_slot, ":used_emblems", HUB_OBJECTS, hub3_val_menu_emblem_build_time),
			(val_sub, ":current_emblems", ":used_emblems"),
			(try_begin),
				(ge, ":current_emblems", ":value"),
				(troop_set_slot, HUB_OBJECTS, hub3_val_menu_emblem_build_cost, ":value"),
				(call_script, "script_hub_update_improvement_screen"),
			(else_try),
				(display_message, "@You have insufficient emblems available to use that setting.", gpu_red),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_menu_emblem_build_cost),
				(overlay_set_val, ":object", ":setting"),
			(try_end),
			
		(else_try),
			### BUTTON - BUILD IMPROVEMENT ###
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_button_improvement_build, ":object"),
			(troop_get_slot, ":slider_setting", HUB_OBJECTS, hub3_val_slider_improvement_selector),
			(store_sub, ":native_span", native_improvements_end, native_improvements_begin),
			(store_sub, ":lower_limit", center_improvements_begin, ":native_span"),
			(is_between, ":slider_setting", ":lower_limit", center_improvements_end),
			(try_begin), # Fix our out of place native improvements.
				(lt, ":slider_setting", center_improvements_begin),
				(store_sub, ":offset", ":slider_setting", ":lower_limit"),
				(store_add, ":improvement_no", native_improvements_begin, ":offset"),
			(else_try),
				(assign, ":improvement_no", ":slider_setting"),
			(try_end),
			## BUILDING THE IMPROVEMENT
			(try_begin),
				# ## CHEAT - Allow instant & cost-free production.
				# (ge, DEBUG_HUB, 2),
				# (party_set_slot, "$current_town", ":improvement_no", cis_built),
			# (else_try),
				# Take the player's cash.
				(call_script, "script_improvement_get_building_time_and_cost", "$current_town", ":improvement_no"), # improvements_scripts.py
				(assign, ":improvement_time", reg2),
				(call_script, "script_diplomacy_treasury_withdraw_funds", reg1, "$current_town", FUND_FROM_EITHER), # diplomacy_scripts.py
				# Find a slot.
				(assign, ":continue", 1),
				(try_for_range, ":building_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
					(eq, ":continue", 1),
					(party_slot_eq, "$current_town", ":building_slot", 0), # Nothing currently being built in this slot.
					(assign, ":continue", 0),
					(party_set_slot, "$current_town", ":building_slot", ":improvement_no"),
					(store_current_hours, ":current_hours"),
					(store_mul, ":hours_takes", ":improvement_time", 24),
					(val_add, ":hours_takes", ":current_hours"),
					(store_add, ":end_time_slot", ":building_slot", 3),
					(party_set_slot, "$current_town", ":end_time_slot", ":hours_takes"),
					# Set starting time record.
					(store_add, ":start_time_slot", ":building_slot", 7),
					(party_set_slot, "$current_town", ":start_time_slot", ":current_hours"),
				(try_end),
				(call_script, "script_improvement_apply_special_cost", ":improvement_no"), # improvements_scripts.py
			(try_end),
			## BUILDING THE IMPROVEMENT
			#(call_script, "script_hub_update_improvement_screen"),
			(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
			(str_store_party_name, s21, "$current_town"),
			(display_message, "@You have begun construction of {s2} in {s21}.", gpu_debug),
			# Charge the player for any emblems spent.
			(assign, ":emblems_used", 0),
			(try_begin), ## BUILD COST
				(troop_slot_ge, HUB_OBJECTS, hub3_val_menu_emblem_build_cost, 1),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_menu_emblem_build_cost),
				(val_add, ":emblems_used", ":setting"),
			(try_end),
			(try_begin), ## BUILD TIME
				(troop_slot_ge, HUB_OBJECTS, hub3_val_menu_emblem_build_time, 1),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_menu_emblem_build_time),
				(val_add, ":emblems_used", ":setting"),
			(try_end),
			(try_begin),
				(ge, ":emblems_used", 1),
				(call_script, "script_cf_emblem_spend_emblems", ":emblems_used"), # emblem_scripts.py
			(try_end),
			# Remove any emblem settings.
			(troop_set_slot, HUB_OBJECTS, hub3_val_menu_emblem_build_time, 0),
			(troop_set_slot, HUB_OBJECTS, hub3_val_menu_emblem_build_cost, 0),
			(start_presentation, "prsnt_hub_improvements"),
			
		(else_try),
			### BUTTON - DESTROY IMPROVEMENT ###
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_button_improvement_destroy, ":object"),
			(troop_get_slot, ":slider_setting", HUB_OBJECTS, hub3_val_slider_improvement_selector),
			(store_sub, ":native_span", native_improvements_end, native_improvements_begin),
			(store_sub, ":lower_limit", center_improvements_begin, ":native_span"),
			(is_between, ":slider_setting", ":lower_limit", center_improvements_end),
			(try_begin), # Fix our out of place native improvements.
				(lt, ":slider_setting", center_improvements_begin),
				(store_sub, ":offset", ":slider_setting", ":lower_limit"),
				(store_add, ":improvement_no", native_improvements_begin, ":offset"),
			(else_try),
				(assign, ":improvement_no", ":slider_setting"),
			(try_end),
			(try_begin),
				(this_or_next|key_is_down, key_left_shift),
				(key_is_down, key_right_shift),
				(party_set_slot, "$current_town", ":improvement_no", cis_unbuilt),
				(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
				(str_store_party_name, s21, "$current_town"),
				(display_message, "@You have demolished the {s0} in {s21}.", gpu_debug),
				(start_presentation, "prsnt_hub_improvements"),
			(else_try),
				(display_message, "@You must hold down the SHIFT key while pushing the DESTROY button to remove an improvement.", gpu_red),
			(try_end),
			
		(else_try),
			### BUTTON - INSTANTLY BUILD AN IMPROVEMENT (DEBUG) ###
			(ge, DEBUG_IMPROVEMENTS, 1),
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_button_improvement_complete, ":object"),
			(troop_get_slot, ":slider_setting", HUB_OBJECTS, hub3_val_slider_improvement_selector),
			(store_sub, ":native_span", native_improvements_end, native_improvements_begin),
			(store_sub, ":lower_limit", center_improvements_begin, ":native_span"),
			(is_between, ":slider_setting", ":lower_limit", center_improvements_end),
			(try_begin), # Fix our out of place native improvements.
				(lt, ":slider_setting", center_improvements_begin),
				(store_sub, ":offset", ":slider_setting", ":lower_limit"),
				(store_add, ":improvement_no", native_improvements_begin, ":offset"),
			(else_try),
				(assign, ":improvement_no", ":slider_setting"),
			(try_end),
			## BUILDING THE IMPROVEMENT
			(party_set_slot, "$current_town", ":improvement_no", cis_built),
			(call_script, "script_improvement_completion_benefits", ":improvement_no", "$current_town"), ## improvements_scripts.py
			## Remove this improvement if it is currently being built.
			(try_for_range, ":building_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
				(party_slot_eq, "$current_town", ":building_slot", ":improvement_no"),
				## Store slot offsets
				(store_sub, ":offset_end", slot_center_improvement_end_hour_1, slot_center_current_improvement_1),
				(store_add, ":slot_hour_end", ":offset_end", ":building_slot"),
				(store_sub, ":offset_start", slot_center_improvement_start_hour_1, slot_center_current_improvement_1),
				(store_add, ":slot_hour_start", ":offset_start", ":building_slot"),
				## Empty out building slots.
				(party_set_slot, "$current_town", ":building_slot", cis_unbuilt),
				(party_set_slot, "$current_town", ":slot_hour_end", 0),
				(party_set_slot, "$current_town", ":slot_hour_start", 0),
			(try_end),
			## BUILDING THE IMPROVEMENT
			#(call_script, "script_hub_update_improvement_screen"),
			(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
			(str_store_party_name, s21, "$current_town"),
			(display_message, "@You have completed construction of {s2} in {s21}.", gpu_debug),
			(start_presentation, "prsnt_hub_improvements"),
			
		(else_try),
			### BUTTON - CANCEL IMPROVEMENT 1 ###
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_button_cancel_const_1, ":object"),
			(try_begin),
				(this_or_next|key_is_down, key_left_shift),
				(key_is_down, key_right_shift),
				(party_get_slot, ":improvement_no", "$current_town", slot_center_current_improvement_1),
				(party_set_slot, "$current_town", slot_center_current_improvement_1, cis_unbuilt),
				(party_set_slot, "$current_town", slot_center_improvement_end_hour_1, 0),
				(party_set_slot, "$current_town", slot_center_improvement_start_hour_1, 0),
				(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
				(str_store_party_name, s21, "$current_town"),
				(display_message, "@You have canceled construction of {s2} in {s21}.", gpu_debug),
				(start_presentation, "prsnt_hub_improvements"),
			(else_try),
				(display_message, "@You must hold down the SHIFT key while pushing the CANCEL button to stop building an improvement.", gpu_red),
			(try_end),
			
		(else_try),
			### BUTTON - CANCEL IMPROVEMENT 2 ###
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_button_cancel_const_2, ":object"),
			(try_begin),
				(this_or_next|key_is_down, key_left_shift),
				(key_is_down, key_right_shift),
				(party_get_slot, ":improvement_no", "$current_town", slot_center_current_improvement_2),
				(party_set_slot, "$current_town", slot_center_current_improvement_2, cis_unbuilt),
				(party_set_slot, "$current_town", slot_center_improvement_end_hour_2, 0),
				(party_set_slot, "$current_town", slot_center_improvement_start_hour_2, 0),
				(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
				(str_store_party_name, s21, "$current_town"),
				(display_message, "@You have canceled construction of {s2} in {s21}.", gpu_debug),
				(start_presentation, "prsnt_hub_improvements"),
			(else_try),
				(display_message, "@You must hold down the SHIFT key while pushing the CANCEL button to stop building an improvement.", gpu_red),
			(try_end),
			
		(else_try),
			### BUTTON - CANCEL IMPROVEMENT 3 ###
			(troop_slot_eq, HUB_OBJECTS, hub3_obj_button_cancel_const_3, ":object"),
			(try_begin),
				(this_or_next|key_is_down, key_left_shift),
				(key_is_down, key_right_shift),
				(party_get_slot, ":improvement_no", "$current_town", slot_center_current_improvement_3),
				(party_set_slot, "$current_town", slot_center_current_improvement_3, cis_unbuilt),
				(party_set_slot, "$current_town", slot_center_improvement_end_hour_3, 0),
				(party_set_slot, "$current_town", slot_center_improvement_start_hour_3, 0),
				(call_script, "script_get_improvement_details", ":improvement_no"), # improvements_scripts.py
				(str_store_party_name, s21, "$current_town"),
				(display_message, "@You have canceled construction of {s2} in {s21}.", gpu_debug),
				(start_presentation, "prsnt_hub_improvements"),
			(else_try),
				(display_message, "@You must hold down the SHIFT key while pushing the CANCEL button to stop building an improvement.", gpu_red),
			(try_end),
			
		(try_end),
      ]),
    ]),
	
	
###########################################################################################################################
#####                                                  RECRUITMENT                                                    #####
###########################################################################################################################

("hub_recruitment", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_hub_create_mode_switching_buttons"),
			
			#########################################
			###        SILVERSTAG EMBLEMS         ###
			#########################################
			
			(try_begin),
				(call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
				(ge, reg1, 1),
				
				## EMBLEM EFFECT - -25% Training Cost
				(assign, ":pos_y", 172),
				(assign, ":pos_x", 52),
				(assign, ":line_step", 18),
				(try_begin),
					(store_current_hours, ":hours"),
					(party_slot_ge, "$current_town", slot_center_training_cost_reduce_duration, ":hours"),
					(str_store_string, s21, "@Extend Effect:"),
				(else_try),
					(str_store_string, s21, "@Apply Effect:"),
				(try_end),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":pos_x", ":pos_y", hub4_obj_button_reduce_training_cost), ### -25% TRAINING ###
				(call_script, "script_gpu_resize_object", hub4_obj_button_reduce_training_cost, 85),
				(overlay_set_color, reg1, gpu_blue),
				## Effect
				(val_sub, ":pos_y", 10),
				(str_store_string, s21, "@-25% Training Cost"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left), # 172
				(call_script, "script_gpu_resize_object", 0, 75),
				## Duration
				(val_sub, ":pos_y", ":line_step"),
				(str_store_string, s21, "@Duration: 24 Hours"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				## Emblem Cost
				(val_sub, ":pos_y", ":line_step"),
				(assign, reg21, EMBLEM_COST_REDUCE_RECRUITMENT_COST),
				(store_sub, reg22, reg21, 1),
				(str_store_string, s21, "@Cost: {reg21} Emblem{reg22?s:}"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				## Remaining Duration
				(try_begin),
					(party_slot_ge, "$current_town", slot_center_training_cost_reduce_duration, ":hours"),
					(party_get_slot, reg21, "$current_town", slot_center_training_cost_reduce_duration),
					(val_sub, reg21, ":hours"),
					(store_sub, reg22, reg21, 1),
					(val_sub, ":pos_y", ":line_step"),
					(str_store_string, s21, "@Ends: {reg21} hour{reg22?s:}"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
					(call_script, "script_gpu_resize_object", 0, 75),
				(try_end),
			(try_end),
			
			#########################################
			###       MODE SELECTION BLOCKS       ###
			#########################################
			# OBJ - Warning note.
			# (call_script, "script_gpu_create_text_label", "str_hub_title_recruitment", 572, 630, 0, gpu_center_with_outline),
			# (overlay_set_color, reg1, gpu_blue),
			
			#################################
			### DISPLAY SELECTION BUTTONS ###
			#################################
			(assign, ":pos_x", 775),
			(assign, ":pos_y", 665),
			
			# OBJ - CHECKBOX
			(store_add, ":pos_x_temp", ":pos_x", 0), (position_set_x, pos1, ":pos_x_temp"),
			(store_add, ":pos_y_temp", ":pos_y", 0), (position_set_y, pos1, ":pos_y_temp"),
			(create_check_box_overlay, reg1, "mesh_button_up", "mesh_button_down"),
			(overlay_set_position, reg1, pos1),
			(troop_set_slot, HUB_OBJECTS, hub4_obj_toggle_party_members_only, reg1),
			(overlay_set_val, reg1, "$hub_display_party_members"),
			# OBJ - LABEL
			(store_add, ":pos_x_temp", ":pos_x",60), (position_set_x, pos1, ":pos_x_temp"),
			(store_add, ":pos_y_temp", ":pos_y",23), (position_set_y, pos1, ":pos_y_temp"),
			(try_begin),
				(eq, "$hub_display_party_members", 1), # Enabled
				(str_store_string, s21, "@Hide Party Members"),
			(else_try),
				(str_store_string, s21, "@Show Party Members"),
			(try_end),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_temp", ":pos_y_temp", hub4_label_toggle_party_members_only, gpu_center),
			(call_script, "script_gpu_resize_object", hub4_label_toggle_party_members_only, 50),
			(call_script, "script_gpu_resize_object", hub4_obj_toggle_party_members_only, 50),
			
			##########################
			### AVAILABLE RECRUITS ###
			##########################
			(assign, ":spread", 170),
			# (try_begin),
				# (party_slot_eq, "$current_town", slot_party_type, spt_town),
				# (assign, ":spread", 170),
			# (else_try),
				# (assign, ":spread", 200),
			# (try_end),
			(assign, ":pos_x", 300),
			
			# OBJ - Available nobles.
			(party_get_slot, reg21, "$current_town", slot_center_veteran_pool),
			(call_script, "script_gpu_create_text_label", "str_hub_available_nobles", ":pos_x", 625, 0, gpu_center),
			(try_begin),
				# (party_slot_eq, "$current_town", slot_party_type, spt_town),
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
					(assign, ":lower_bound",   player_troops_begin),
					(assign, ":upper_bound",   player_troops_end),
					# (assign, ":uniques_begin", player_uniques_begin),
					# (assign, ":uniques_end",   player_uniques_begin),
				(else_try),
					(eq, ":culture", "fac_culture_1"), # Swadia
					(assign, ":lower_bound",   swadia_troops_begin),
					(assign, ":upper_bound",   swadia_troops_end),
					# (assign, ":uniques_begin", swadia_uniques_begin),
					# (assign, ":uniques_end",   swadia_uniques_end),
				(else_try),
					(eq, ":culture", "fac_culture_2"), # Vaegirs
					(assign, ":lower_bound",   vaegir_troops_begin),
					(assign, ":upper_bound",   vaegir_troops_end),
					# (assign, ":uniques_begin", vaegir_uniques_begin),
					# (assign, ":uniques_end",   vaegir_uniques_end),
				(else_try),
					(eq, ":culture", "fac_culture_3"), # Khergits
					(assign, ":lower_bound",   khergit_troops_begin),
					(assign, ":upper_bound",   khergit_troops_end),
					# (assign, ":uniques_begin", khergit_uniques_begin),
					# (assign, ":uniques_end",   khergit_uniques_end),
				(else_try),
					(eq, ":culture", "fac_culture_4"), # Nords
					(assign, ":lower_bound",   nord_troops_begin),
					(assign, ":upper_bound",   nord_troops_end),
					# (assign, ":uniques_begin", nord_uniques_begin),
					# (assign, ":uniques_end",   nord_uniques_end),
				(else_try),
					(eq, ":culture", "fac_culture_5"), # Rhodoks
					(assign, ":lower_bound",   rhodok_troops_begin),
					(assign, ":upper_bound",   rhodok_troops_end),
					# (assign, ":uniques_begin", rhodok_uniques_begin),
					# (assign, ":uniques_end",   rhodok_uniques_end),
				(else_try),
					(eq, ":culture", "fac_culture_6"), # Sarranid
					(assign, ":lower_bound",   sarranid_troops_begin),
					(assign, ":upper_bound",   sarranid_troops_end),
					# (assign, ":uniques_begin", sarranid_uniques_begin),
					# (assign, ":uniques_end",   sarranid_uniques_end),
				(try_end),
				
				(assign, ":pos_y", 0),
				
				## COUNT - PARTY MEMBERS
				(party_get_num_companion_stacks, ":stack_capacity", "p_main_party"),
				(try_for_range, ":stack_no", 0, ":stack_capacity"),
					(lt, ":pos_y", MAXIMUM_TROOP_RECORDS),
					(eq, "$hub_display_party_members", 1), # SHOW - Party Members
					(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
						(assign, ":recruitable", 1),
					(else_try),
						(assign, ":recruitable", 0),
					(try_end),
					# Faction Troops
					(eq, ":recruitable", 0), # Isn't going to be included in the next search.
					(val_add, ":pos_y", 1),
					### DIAGNOSTIC ###
					(ge, DEBUG_RECRUITMENT, 1),
					(assign, reg31, ":pos_y"),
					(str_store_troop_name, s31, ":troop_no"),
					(assign, reg32, ":recruitable"),
					(display_message, "@DEBUG: #{reg31} - {s31} - Recruitable: {reg32?Yes:No}", gpu_debug),
				(try_end),
				
				## COUNT - FACTION TROOPS
				(try_for_range, ":troop_no", troop_definitions_begin, troop_definitions_end), # ":lower_bound", ":upper_bound"),
					# Does this troop belong to this culture?
					(this_or_next|troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_1, ":culture"),
					(this_or_next|troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_2, ":culture"),
					(troop_slot_eq, ":troop_no", slot_troop_recruitable_faction_3, ":culture"),
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
				
				## DEBUG TESTING+ ##
				# (try_for_range, ":troop_no", "trp_knight_6_1", "trp_kingdom_1_pretender"),
					# (val_add, ":pos_y", 1),
				# (try_end),
				## DEBUG TESTING- ##
				
				# Set our initial position.
				(val_mul, ":pos_y", ":troop_step"),
				
				################## DISPLAY ###################
				(assign, ":record", 0),
				
				## DEBUG TESTING+ ##
				# (try_for_range, ":troop_no", "trp_knight_6_1", "trp_kingdom_1_pretender"),
					# (call_script, "script_hub_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					# (val_add, ":record", 1),
					# (val_sub, ":pos_y", ":troop_step"),
				# (try_end),
				## DEBUG TESTING- ##
				
				## DISPLAY - PARTY MEMBERS
				(party_get_num_companion_stacks, ":stack_capacity", "p_main_party"),
				(try_for_range, ":stack_no", 0, ":stack_capacity"),
					(lt, ":record", MAXIMUM_TROOP_RECORDS),
					(eq, "$hub_display_party_members", 1), # SHOW - Party Members
					(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
						(assign, ":recruitable", 1),
					(else_try),
						(assign, ":recruitable", 0),
					(try_end),
					# Faction Troops
					(eq, ":recruitable", 0), # Isn't going to be included in the next search.
					(call_script, "script_hub_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 0),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
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
					(call_script, "script_hub_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
				# ## DISPLAY - UNIQUE TROOPS
				# (try_for_range, ":troop_no", ":uniques_begin", ":uniques_end"),
					# (lt, ":record", MAXIMUM_TROOP_RECORDS),
					# (call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					# (call_script, "script_hub_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
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
					(call_script, "script_hub_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
				## DISPLAY - MERCENARIES
				(try_for_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
					(lt, ":record", MAXIMUM_TROOP_RECORDS),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(call_script, "script_hub_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
				## DISPLAY - BANDITS
				(try_for_range, ":troop_no", bandits_begin, bandits_end),
					(lt, ":record", MAXIMUM_TROOP_RECORDS),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", "$current_town", ":troop_no", "trp_player"),
					(call_script, "script_hub_troop_get_recruitment_info", ":troop_no", ":record", ":pos_y", 1),
					(val_add, ":record", 1),
					(val_sub, ":pos_y", ":troop_step"),
				(try_end),
				
			(set_container_overlay, -1),
			
			(str_store_string, s21, "@Recruit / Dismiss Amount:"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 430, 55, 0, gpu_center),
			(call_script, "script_gpu_create_number_box", 570, 43, 1, 50, hub4_obj_numbox_hire_amount, hub4_val_numbox_hire_amount),
			
			(str_store_string, s21, "@Holding [Shift] hires or dismisses 10.  Holding [Ctrl] hires or dismisses all available."),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 30, 0, gpu_center),
			(call_script, "script_gpu_resize_object", 0, 75),
			
		]),
	
    (ti_on_presentation_run,
	  [
		(try_begin),
			(key_clicked, key_escape),
			(presentation_set_duration, 0),
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(jump_to_menu, "mnu_town"),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(jump_to_menu, "mnu_village"),
			(try_end),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_hub_handle_mode_switching_buttons", ":object", ":value"),
		
		# hub4_val_button_troop_no               = 100
		# hub4_obj_button_recruit_troop          = 175
		# hub4_obj_button_inspect_equipment      = 250
		# hub4_obj_button_dismiss_troop          = 325
		
		(try_begin),
			### TOGGLE BUTTON : SHOW PARTY MEMBERS ###
			(troop_slot_eq, HUB_OBJECTS, hub4_obj_toggle_party_members_only, ":object"),
			(assign, "$hub_display_party_members", ":value"),
			(troop_get_slot, ":obj_label", HUB_OBJECTS, hub4_label_toggle_party_members_only),
			(try_begin),
				(eq, "$hub_display_party_members", 1), # Enabled
				(str_store_string, s21, "@Hide Party Members"),
			(else_try),
				(str_store_string, s21, "@Show Party Members"),
			(try_end),
			(overlay_set_text, ":obj_label", "@{s21}"),
			# (assign, reg21, ":value"),
			# (display_message, "@DEBUG: You clicked the toggle.  Setting is {reg21?Enabled:Disabled} {reg21}", gpu_debug),
			(start_presentation, "prsnt_hub_recruitment"),
		(else_try),
			### BUTTON : EMBLEM EFFECT -25% TRAINING COST ###
			(troop_slot_eq, HUB_OBJECTS, hub4_obj_button_reduce_training_cost, ":object"),
			(store_current_hours, ":hours"),
			(try_begin), # Effect currently applied, extend hours by 24.
				(party_slot_ge, "$current_town", slot_center_training_cost_reduce_duration, ":hours"),
				(party_get_slot, ":hours", "$current_town", slot_center_training_cost_reduce_duration),
			(try_end),
			(val_add, ":hours", 24),
			(party_set_slot, "$current_town", slot_center_training_cost_reduce_duration, ":hours"),
			(call_script, "script_cf_emblem_spend_emblems", EMBLEM_COST_REDUCE_RECRUITMENT_COST), # emblem_scripts.py
			(start_presentation, "prsnt_hub_recruitment"),
		(try_end),
		
		####### BUTTON : INSPECT EQUIPMENT #######
		(try_for_range, ":record", hub4_obj_button_inspect_equipment, hub4_obj_button_dismiss_troop), 
			(troop_slot_eq, HUB_OBJECTS, ":record", ":object"),
			(store_add, ":button_val_slot", hub4_val_button_troop_no, ":record"),  # 100 + (250 to 325)
			(val_sub, ":button_val_slot", hub4_obj_button_inspect_equipment), # Push us back into the 100-199 range.
			(troop_get_slot, "$temp", HUB_OBJECTS, ":button_val_slot"),
			(assign, "$hub_mode", HUB_MODE_TROOP_INFO),
			(assign, "$g_presentation_next_presentation", "prsnt_hub_recruitment"),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
		(try_end),
		
		####### BUTTON : RECRUIT TROOP #######
		(try_for_range, ":record", hub4_obj_button_recruit_troop, hub4_obj_button_inspect_equipment), 
			(troop_slot_eq, HUB_OBJECTS, ":record", ":object"),
			(store_add, ":button_val_slot", hub4_val_button_troop_no, ":record"),  # 100 + (175 to 250)
			(val_sub, ":button_val_slot", hub4_obj_button_recruit_troop), # Push us back into the 100-199 range.
			(troop_get_slot, "$temp", HUB_OBJECTS, ":button_val_slot"),
			
			# Setup the number of troops being requested.
			(assign, ":troop_count", 1),
			(troop_get_slot, ":obj_numbox_amount", HUB_OBJECTS, hub4_obj_numbox_hire_amount),
			(overlay_get_val, ":troop_count", ":obj_numbox_amount"),
			(troop_set_slot, HUB_OBJECTS, hub4_val_numbox_hire_amount, ":troop_count"),
			
			# Batch hires
			(try_begin),
				(this_or_next|key_is_down, key_left_shift),
				(key_is_down, key_right_shift),
				(assign, ":troop_count", 10),
			(else_try),
				(this_or_next|key_is_down, key_left_control),
				(key_is_down, key_right_control),
				(call_script, "script_hub_get_troop_recruit_type_for_buyer", "$temp", "trp_player"),
				(party_get_slot, ":max_amount", "$current_town", reg1),
				(assign, ":troop_count", ":max_amount"),
			(try_end),
			
			(call_script, "script_hub_get_troop_recruit_type_for_buyer", "$temp", "trp_player"), # Returns type slot to reg1
			(assign, ":recruiting_pool", reg1),
			
			(call_script, "script_hub_get_purchase_price_for_troop", "$current_town", "$temp", "trp_player"), # Returns reg1 (price), reg2 (discount)
			(assign, ":troop_cost", reg1),
			(store_mul, ":multiplied_cost", ":troop_count", ":troop_cost"),
			(try_begin), # Can we afford this many troops?
				(call_script, "script_cf_diplomacy_treasury_verify_funds", ":multiplied_cost", "$current_town", FUND_FROM_EITHER, TREASURY_FUNDS_INSUFFICIENT), # diplomacy_scripts.py
				(assign, ":funds_available", reg1),
				(store_div, ":troop_count", ":funds_available", ":troop_cost"),
				(store_mul, ":multiplied_cost", ":troop_count", ":troop_cost"),
				(str_store_string, s41, "@You cannot afford to purchase any more troops of this type."), # Stored if no troops can be purchased.
			(try_end),
			(try_begin), # Does the player party have space for this many troops?
				(party_get_free_companions_capacity, ":party_capacity", "p_main_party"),
				(lt, ":party_capacity", ":troop_count"),
				(assign, ":troop_count", ":party_capacity"),
				(store_mul, ":multiplied_cost", ":troop_count", ":troop_cost"),
				(str_store_string, s41, "@Your party does not have enough room to hire any more troops."), # Stored if no troops can be purchased.
			(try_end),
			(try_begin), # Does the player party have enough available recruits?
				(party_get_slot, ":available_recruits", "$current_town", ":recruiting_pool"),
				(lt, ":available_recruits", ":troop_count"),
				(assign, ":troop_count", ":available_recruits"),
				(store_mul, ":multiplied_cost", ":troop_count", ":troop_cost"),
				(str_store_string, s41, "@You do not have enough available recruits to train."), # Stored if no troops can be purchased.
			(try_end),
			(try_begin), # Does the town have enough mounts available if they're required?
				(this_or_next|troop_is_mounted, "$temp"),
				(troop_is_guarantee_horse, "$temp"),
				(party_get_slot, ":available_mounts", "$current_town", slot_center_horse_pool_player),
				(lt, ":available_mounts", ":troop_count"),
				(assign, ":troop_count", ":available_mounts"),
				(store_mul, ":multiplied_cost", ":troop_count", ":troop_cost"),
				(str_store_string, s41, "@You do not have any spare mounts to equip these troops with."), # Stored if no troops can be purchased.
			(try_end),
			
			(try_begin),
				(ge, ":troop_count", 1),
				# Purchase the maximum troops available or requested.
				(call_script, "script_diplomacy_treasury_withdraw_funds", ":multiplied_cost", "$current_town", FUND_FROM_EITHER), # diplomacy_scripts.py
				(party_add_members, "p_main_party", "$temp", ":troop_count"),
				
				# Take from the appropriate recruit types.
				(party_get_slot, reg1, "$current_town", ":recruiting_pool"),
				(val_sub, reg1, ":troop_count"),
				(party_set_slot, "$current_town", ":recruiting_pool", reg1),
				# Remove a mount if needed.
				(try_begin),
					(this_or_next|troop_is_mounted, "$temp"),
					(troop_is_guarantee_horse, "$temp"),
					(party_get_slot, reg1, "$current_town", slot_center_horse_pool_player),
					(val_sub, reg1, ":troop_count"),
					(party_set_slot, "$current_town", slot_center_horse_pool_player, reg1),
				(try_end),
				
				# Report transaction to the player.
				(str_store_troop_name, s21, "$temp"),
				(assign, reg21, ":troop_count"),
				(try_begin),
					(ge, ":troop_count", 2),
					(str_store_troop_name_plural, s21, "$temp"),
				(try_end),
				(display_message, "@You have hired {reg21} {s21}.", gpu_green),
				
				# METRICS DATA - Report how much training skill has saved the player.
				(try_begin),
					(store_skill_level, ":skill_training", "skl_trainer", "trp_player"),
					(ge, ":skill_training", 1), # Don't track unless a bonus exists.
					# Total Savings
					(troop_get_slot, ":trainer_discount", METRICS_DATA, metrics_trainer_troop_saving),
					(store_mul, ":total_discount", ":troop_count", ":trainer_discount"),
					(val_add, ":trainer_discount", ":total_discount"),
					(troop_set_slot, METRICS_DATA, metrics_trainer_total_savings, ":trainer_discount"),
					# Total Purchases
					(troop_get_slot, ":trainer_purchases", METRICS_DATA, metrics_trainer_troop_purchases),
					(val_add, ":trainer_purchases", ":troop_count"),
					(troop_set_slot, METRICS_DATA, metrics_trainer_troop_purchases, ":trainer_purchases"),
					# Savings per Rank
					(val_div, ":trainer_discount", ":skill_training"),
					(troop_set_slot, METRICS_DATA, metrics_trainer_saving_per_rank, ":trainer_discount"),
					(troop_set_slot, METRICS_DATA, metrics_trainer_troop_saving, 0),
					(try_begin),
						(eq, "$enable_metrics", 1),
						(troop_get_slot, reg31, METRICS_DATA, metrics_trainer_total_savings),
						(troop_get_slot, reg32, METRICS_DATA, metrics_trainer_troop_purchases),
						(troop_get_slot, reg33, METRICS_DATA, metrics_trainer_saving_per_rank),
						(display_message, "@METRIC (Trainer): Total savings of {reg31} denars over {reg32} troops purchased.", gpu_debug),
						(display_message, "@METRIC (Trainer): You have saved {reg33} denars per rank.", gpu_debug),
					(try_end),
				(try_end),
				
				(start_presentation, "prsnt_hub_recruitment"),
			(else_try),
				(display_message, "@{s41}", gpu_red),
			(try_end),
			
		(try_end),
		
		####### BUTTON : DISMISS TROOP #######
		(try_for_range, ":record", hub4_obj_button_dismiss_troop, 400), 
			(troop_slot_eq, HUB_OBJECTS, ":record", ":object"),
			(store_add, ":button_val_slot", hub4_val_button_troop_no, ":record"),  # 100 + (325 to 400)
			(val_sub, ":button_val_slot", hub4_obj_button_dismiss_troop), # Push us back into the 100-199 range.
			(troop_get_slot, "$temp", HUB_OBJECTS, ":button_val_slot"),
			(assign, ":troop_count", 1),
			(troop_get_slot, ":obj_numbox_amount", HUB_OBJECTS, hub4_obj_numbox_hire_amount),
			(overlay_get_val, ":troop_count", ":obj_numbox_amount"),
			(troop_set_slot, HUB_OBJECTS, hub4_val_numbox_hire_amount, ":troop_count"),
			
			# Batch dismissing.
			(try_begin),
				(this_or_next|key_is_down, key_left_shift),
				(key_is_down, key_right_shift),
				(assign, ":troop_count", 10),
			(else_try),
				(this_or_next|key_is_down, key_left_control),
				(key_is_down, key_right_control),
				(party_count_companions_of_type, ":max_amount", "p_main_party", "$temp"),
				(assign, ":troop_count", ":max_amount"),
			(try_end),
			
			(party_count_companions_of_type, ":current_count", "p_main_party", "$temp"),
			(val_min, ":troop_count", ":current_count"), # Prevent trying to remove more than we have.
			(party_remove_members, "p_main_party", "$temp", ":troop_count"),
			
			# Shift these to the appropriate recruit types.
			# (try_begin),
				# (troop_slot_eq, "$temp", slot_troop_recruit_type, STRT_NOBLEMAN),
				# (assign, ":storage_slot", slot_center_veteran_pool),
				# (str_store_string, s29, "@noble"),
			# (else_try),
				# (troop_slot_eq, "$temp", slot_troop_recruit_type, STRT_MERCENARY),
				# (assign, ":storage_slot", slot_center_mercenary_pool_player),
				# (str_store_string, s29, "@mercenary"),
			# (else_try),
				# (assign, ":storage_slot", slot_center_volunteer_troop_amount),
				# (str_store_string, s29, "@peasant"),
			# (try_end),
			(call_script, "script_hub_get_troop_recruit_type_for_buyer", "$temp", "trp_player"),
			(str_store_string, s29, s1),
			(assign, ":storage_slot", reg1),
			(party_get_slot, reg1, "$current_town", ":storage_slot"),
			(val_add, reg1, ":troop_count"),
			(party_set_slot, "$current_town", ":storage_slot", reg1),
			
			# Add back mounts if appropriate.
			(try_begin),
				(this_or_next|troop_is_mounted, "$temp"),
				(troop_is_guarantee_horse, "$temp"),
				(party_get_slot, reg1, "$current_town", slot_center_horse_pool_player),
				(val_add, reg1, ":troop_count"),
				(party_set_slot, "$current_town", slot_center_horse_pool_player, reg1),
			(try_end),
			
			# Report transaction to player.
			(assign, reg21, ":troop_count"),
			(str_store_troop_name, s21, "$temp"),
			(try_begin),
				(ge, ":troop_count", 2),
				(str_store_troop_name_plural, s21, "$temp"),
			(try_end),
			(store_sub, reg23, reg21, 1),
			(display_message, "@You have dismissed {reg21} {s21} and gained {reg21} new {s29} recruit{reg23?s:}.", gpu_green),
			(start_presentation, "prsnt_hub_recruitment"),
		(try_end),
		
		
      ]),
    ]),
	
	
	
	
	
###########################################################################################################################
#####                                                    ADVISORS                                                     #####
###########################################################################################################################

("hub_advisors", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_hub_create_mode_switching_buttons"),
			
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
			(presentation_set_duration, 0),
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(jump_to_menu, "mnu_town"),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(jump_to_menu, "mnu_village"),
			(try_end),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_hub_handle_mode_switching_buttons", ":object", ":value"),
		
      ]),
    ]),
	
###########################################################################################################################
#####                                                     QUESTS                                                      #####
###########################################################################################################################

("hub_quests", 0, mesh_load_window, [
    (ti_on_presentation_load,
		[
			(presentation_set_duration, 999999),
			(set_fixed_point_multiplier, 1000),
			
			(call_script, "script_hub_create_mode_switching_buttons"),
			
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
			(presentation_set_duration, 0),
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(jump_to_menu, "mnu_town"),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(jump_to_menu, "mnu_village"),
			(try_end),
		(try_end), 
	  ]),  
	
    (ti_on_presentation_event_state_change,
      [
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
		
		(call_script, "script_hub_handle_mode_switching_buttons", ":object", ":value"),
		
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
