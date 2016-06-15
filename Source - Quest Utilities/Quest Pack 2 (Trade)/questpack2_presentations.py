# Tournament Play Enhancements (1.4) by Windyplains

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
#####                                              RIVAL DEBUG DISPLAY                                                #####
###########################################################################################################################
# # OBJECT SLOTS - RIVAL DEBUG DISPLAY
# # Trade Rival Slots (start with 200)
# trs_obj_rival_proficiency                       = 1
# trs_obj_rival_status                            = 2
# trs_obj_rival_trade_skill                       = 3
# trs_obj_rival_position                          = 4
# trs_obj_rival_x_loc                             = 5
# trs_obj_rival_y_loc                             = 6
# trs_obj_rival_destination                       = 7
# trs_obj_rival_current_wealth                    = 8
# trs_obj_rival_accumulated_wealth                = 9

# script_gpu_create_checkbox     - pos_x, pos_y, label, storage_slot, value_slot
# script_gpu_create_mesh         - mesh_id, pos_x, pos_y, size_x, size_y
# script_gpu_create_portrait     - troop_id, pos_x, pos_y, size, storage_id
# script_gpu_create_button       - title, pos_x, pos_y, storage_id
# script_gpu_create_text_label   - title, pos_x, pos_y, storage_id, design
# script_gpu_resize_object       - storage_id, percent size
# script_gpu_draw_line           - x length, y length, pos_x, pos_y, color
# script_gpu_container_heading   - pos_x, pos_y, size_x, size_y, storage_id
# script_gpu_create_slider       - min, max, pos_x, pos_y, storage_id, value_id


("qp2_debug_rival_status", 0, mesh_load_window, [
  (ti_on_presentation_load,
    [
		(set_fixed_point_multiplier, 1000),
		(assign, "$gpu_storage", "trp_tpe_presobj"),
		(assign, "$gpu_data",    "trp_tpe_presobj"),
		
		# Button Definitions
		(call_script, "script_gpu_create_game_button", "str_qp2_trd_label_done", 895, 25, trs_obj_rival_button_done),
		(call_script, "script_gpu_create_button", "str_qp2_trd_button_prev", 225, 580, trs_obj_rival_prev_troop),
		(call_script, "script_gpu_create_button", "str_qp2_trd_button_next", 300, 580, trs_obj_rival_next_troop),
		
		### HEADER DISPLAY ### - Begin
		# Portrait
		(call_script, "script_gpu_create_portrait", "$rival_troop", 30, 575, 500, trs_obj_rival_portrait),
		# Troop name
		(str_store_troop_name, s31, "$rival_troop"),
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 220, 675, trs_obj_rival_name, gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		# Troop proficiency / level
		(troop_get_slot, reg31, "$rival_troop", slot_rival_proficiency),
		(store_div, reg32, reg31, qp2_trs_proficiency_per_level_ratio),
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_level", 225, 650, trs_obj_rival_proficiency, gpu_left),
		# Faction
		(troop_get_slot, ":faction_no", "$rival_troop", slot_rival_home_region),
		(str_store_faction_name, s31, ":faction_no"),
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 225, 625, trs_obj_rival_home_region, gpu_left),
		# Dividing Lines
		(call_script, "script_gpu_draw_line", 950, 2, 25, 560, gpu_gray), # horizontal line underneath header.
		### HEADER DISPLAY ### - End
		
		### FACTION RELATIONS ### - Begin
		# Title
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_relation_factions", 25, 535, trs_obj_rival_faction_relations_end, gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		# Scrolling Display
		(store_sub, ":pos_y", slot_rival_faction_relations_end, slot_rival_relation_fac_player),
		(val_mul, ":pos_y", 25),
		(call_script, "script_gpu_container_heading", 30, 365, 300, 150, trs_obj_rival_container_faction_relation), # script_gpu_container_heading   - pos_x, pos_y, size_x, size_y, storage_id
			(try_for_range, ":faction_slot", slot_rival_relation_fac_player, slot_rival_faction_relations_end),
				(store_sub, ":faction_no", ":faction_slot", slot_rival_relation_fac_player),
				(store_add, ":object_slot", trs_obj_rival_relation_fac_player, ":faction_no"),
				# CONDITIONAL: If player is not king I don't want to show his faction.
				(try_begin),
					(assign, ":king", 0),
					(call_script, "script_cf_qus_player_is_king", 1), # Quest Util Script
					(assign, ":king", 1),
				(try_end),
				(this_or_next|neq, ":faction_no", 0),
				(eq, ":king", 1),
				# Faction Name
				(store_add, ":faction_no_actual", ":faction_no", "fac_player_supporters_faction"),
				(str_store_faction_name, s31, ":faction_no_actual"),
				(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 0, ":pos_y", ":object_slot", gpu_left),
				# Relation
				(troop_get_slot, reg31, "$rival_troop", ":faction_slot"),
				(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_reg31", 300, ":pos_y", ":object_slot", gpu_right),
				(val_sub, ":pos_y", 25),
			(try_end),
		(set_container_overlay, -1),
		### FACTION RELATIONS ### - End
		
		### RIVAL RELATIONS ### - Begin
		# Title
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_relation_rivals", 25, 335, trs_obj_rival_individual_relations_end, gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		# Scrolling Display
		(store_sub, ":pos_y", slot_rival_individual_relations_end, slot_rival_relation_player),
		(val_mul, ":pos_y", 25),
		(call_script, "script_gpu_container_heading", 30, 165, 300, 150, trs_obj_rival_container_individual_relation), # script_gpu_container_heading   - pos_x, pos_y, size_x, size_y, storage_id
			(try_for_range, ":rival_slot", slot_rival_relation_player, slot_rival_individual_relations_end),
				(store_sub, ":rival_no", ":rival_slot", slot_rival_relation_player),
				(store_add, ":object_slot", trs_obj_rival_relation_player, ":rival_no"),
				# Rival Name
				(store_add, ":troop_rival", ":rival_no", qp2_trade_rivals_begin),
				(str_store_troop_name, s31, ":troop_rival"),
				(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 0, ":pos_y", ":object_slot", gpu_left),
				# Relation
				(troop_get_slot, reg31, "$rival_troop", ":rival_slot"),
				(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_reg31", 300, ":pos_y", ":object_slot", gpu_right),
				(val_sub, ":pos_y", 25),
			(try_end),
		(set_container_overlay, -1),
		### RIVAL RELATIONS ### - End
		
		### MERCHANT INFORMATION ### - Begin
		# Title
		(assign, ":pos_y", 535),
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_useful_stats", 375, ":pos_y", trs_obj_rival_y_loc, gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		# Current Status & Location
		(val_sub, ":pos_y", 25),
		(try_begin),
			(troop_slot_eq, "$rival_troop", slot_rival_status, 1),
			(str_store_string, s31, "@Merchant is active"),
		(else_try),
			(str_store_string, s31, "@Merchant is INACTIVE"),
		(try_end),
		(troop_get_slot, ":location", "$rival_troop", slot_rival_location),
		(try_begin),
			#(neg|is_between, ":location", centers_begin, centers_end),
			(eq, 1, 0),
			(str_store_string, s33, "@in the field"),
		(else_try),
			(is_between, ":location", centers_begin, centers_end),
			(str_store_party_name, s32, ":location"),
			(str_store_string, s33, "@near {s32}"),
		(else_try),
			(str_clear, s33),
		(try_end),
		(str_store_string, s31, "@{s31} {s33}."),
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 380, ":pos_y", trs_obj_rival_status, gpu_left),
		
		# Current & Accumulated Wealth
		(val_sub, ":pos_y", 25),
		(troop_get_slot, reg31, "$rival_troop", slot_rival_current_wealth),
		(troop_get_slot, reg32, "$rival_troop", slot_rival_accumulated_wealth),
		(str_store_string, s31, "@{reg31} denars currently of {reg32} total."),
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 380, ":pos_y", trs_obj_rival_current_wealth, gpu_left),
		
		# Pos X / Y + Destination
		(val_sub, ":pos_y", 25),
		(troop_get_slot, ":location", "$rival_troop", slot_rival_destination),
		(party_get_position, pos1, ":location"),
		(troop_get_slot, reg31, "$rival_troop", slot_rival_x_loc),
		(position_set_x, pos2, reg31),
		(troop_get_slot, reg31, "$rival_troop", slot_rival_y_loc),
		(position_set_y, pos2, reg31),
		#(store_distance_to_party_from_party, ":distance", ":current_location", reg32),
		(get_distance_between_positions_in_meters, reg32, pos1, pos2),
		(try_begin),
			(neg|is_between, ":location", centers_begin, centers_end),
			(str_store_party_name, s32, ":location"),
			(assign, reg31, ":location"),
			(str_store_string, s31, "@Merchant is in {s32} @ {reg31}."),
			#(str_store_string, s31, "@Merchant has no valid destination."),
		(else_try),
			(troop_slot_eq, "$rival_troop", slot_rival_location, ":location"),
			(str_store_party_name, s32, ":location"),
			(str_store_string, s31, "@Merchant plans to remain in {s32}"),
		(else_try),
			(str_store_party_name, s32, ":location"),
			#(str_store_string, s32, "@in route to {s32}"),
			(str_store_string, s31, "@Headed for {s32} that is {reg32} leagues distant."),
		(try_end),
		#(str_store_string, s31, "@Loc: ({reg31},{reg32}) {s32}"),
		#(str_store_string, s31, "@Headed for {s32} that is {reg32} leagues distant."),
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 380, ":pos_y", trs_obj_rival_x_loc, gpu_left),
		### MERCHANT INFORMATION ### - End
		
		### PREVIOUS QUEST ### - Begin
		(try_begin),
			(troop_get_slot, reg31, "$rival_troop", slot_rival_last_quest_attempted),
			(is_between, reg31, qp2_quests_begin, qp2_quests_end),
			(assign, ":show_quest", 1),
		(else_try),
			(assign, ":show_quest", 0),
		(try_end),
		
		(try_begin),
			(eq, ":show_quest", 1),
			(val_sub, ":pos_y", 45),
			# Title
			(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_last_quest", 375, ":pos_y", trs_obj_rival_last_quest_title, gpu_left_with_outline),
			(overlay_set_color, reg1, gpu_white),
			# Quest Name
			(val_sub, ":pos_y", 25),
			(str_clear, s31),
			(troop_get_slot, reg31, "$rival_troop", slot_rival_last_quest_attempted),
			(str_store_quest_name, s31, reg31),
			(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_last_quest_s31", 380, ":pos_y", slot_rival_last_quest_attempted, gpu_left),
			# Quest Winner
			(val_sub, ":pos_y", 25),
			(str_clear, s31),
			(troop_get_slot, reg31, "$rival_troop", slot_rival_last_quest_winner),
			(str_store_troop_name, s31, reg31),
			(call_script, "script_gpu_create_text_label", "str_qp2_trd_last_quest_s31_winner", 380, ":pos_y", slot_rival_last_quest_attempted, gpu_left),
		(try_end),
		### PREVIOUS QUEST ### - End
		
		### CURRENT QUEST ### - Begin
		# Title
		(val_sub, ":pos_y", 45),
		(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_current_quest", 375, ":pos_y", trs_obj_rival_current_quest_title, gpu_left_with_outline),
		(overlay_set_color, reg1, gpu_white),
		
		# Setup Information
		(assign, ":show_quest", 0),
		(try_begin),
			(troop_slot_eq, "$rival_troop", slot_rival_quest_shortage_status, 1),
			(str_store_string, s31, "@Trade Shortage"),
			(troop_get_slot, reg31, "$rival_troop", slot_rival_quest_shortage_stage),
			(troop_get_slot, reg32, "$rival_troop", slot_rival_quest_shortage_trigger_chance),
			(quest_get_slot, ":primary_item", "qst_floris_trade_shortage", slot_quest_primary_commodity),
			(quest_get_slot, ":target_center", "qst_floris_trade_shortage", slot_quest_target_center),
			(str_store_item_name,  s33, ":primary_item"),
			(str_store_party_name, s34, ":target_center"),
			(store_add, ":next_stage", reg31, 1),
			(try_begin),
				(quest_get_slot, ":final_stage", "qst_floris_trade_shortage", slot_quest_final_stage),
				(ge, ":next_stage", ":final_stage"),
				(str_store_string, s36, "@completing the quest"),
			(else_try),
				(assign, reg33, ":next_stage"),
				(str_store_string, s36, "@advancing to stage {reg33}"),
			(try_end),
			(str_store_string, s32, "@Description: Bring {s33} to the town of {s34}."),
			(str_store_string, s35, "@Stage {reg31} with a {reg32}% chance of {s36}."),
			(assign, ":show_quest", 1),
		(else_try),
			(troop_slot_eq, "$rival_troop", slot_rival_quest_surplus_status, 1),
			(str_store_string, s31, "@Trade Surplus"),
			(troop_get_slot, reg31, "$rival_troop", slot_rival_quest_surplus_stage),
			(troop_get_slot, reg32, "$rival_troop", slot_rival_quest_surplus_trigger_chance),
			(quest_get_slot, ":primary_item", "qst_floris_trade_surplus", slot_quest_primary_commodity),
			(quest_get_slot, ":target_center", "qst_floris_trade_surplus", slot_quest_target_center),
			(str_store_item_name,  s33, ":primary_item"),
			(str_store_party_name, s34, ":target_center"),
			(store_add, ":next_stage", reg31, 1),
			(try_begin),
				(quest_get_slot, ":final_stage", "qst_floris_trade_surplus", slot_quest_final_stage),
				(ge, ":next_stage", ":final_stage"),
				(str_store_string, s36, "@completing the quest"),
			(else_try),
				(assign, reg33, ":next_stage"),
				(str_store_string, s36, "@advancing to stage {reg33}"),
			(try_end),
			(str_store_string, s32, "@Description: Buy {s33} in the town of {s34}."),
			(str_store_string, s35, "@Stage {reg31} with a {reg32}% chance of {s36}."),
			(assign, ":show_quest", 1),
		(else_try),
			(troop_slot_eq, "$rival_troop", slot_rival_quest_fortune_status, 1),
			(str_store_string, s31, "@Fortune Favors The Bold"),
			(troop_get_slot, reg31, "$rival_troop", slot_rival_quest_fortune_stage),
			(troop_get_slot, reg32, "$rival_troop", slot_rival_quest_fortune_cycle_count),
			(quest_get_slot, ":primary_item", "qst_floris_trade_fortune_favors_bold", slot_quest_primary_commodity),
			(quest_get_slot, ":target_center", "qst_floris_trade_fortune_favors_bold", slot_quest_target_center),
			(quest_get_slot, ":secondary_item", "qst_floris_trade_fortune_favors_bold", slot_quest_secondary_commodity),
			(quest_get_slot, ":giver_center", "qst_floris_trade_fortune_favors_bold", slot_quest_giver_center),
			(str_store_item_name,  s33, ":primary_item"),
			(str_store_party_name, s34, ":target_center"),
			(str_store_item_name, s35, ":secondary_item"),
			(str_store_party_name, s36, ":giver_center"),
			(try_begin),
				(troop_slot_eq, "$rival_troop", slot_rival_quest_fortune_stage, qp2_fortune_arrived_in_primary_center),
				(str_store_string, s37, "@Buy {s35} and deliver to {s36}."),
			(else_try),
				(troop_slot_eq, "$rival_troop", slot_rival_quest_fortune_stage, qp2_fortune_purchased_commodity_in_primary_town),
				(str_store_string, s37, "@Traveling to {s36}."),
			(else_try),
				(troop_slot_eq, "$rival_troop", slot_rival_quest_fortune_stage, qp2_fortune_arrived_in_second_center),
				(str_store_string, s37, "@Buy {s33} and deliver to {s34}."),
			(else_try),
				(troop_slot_eq, "$rival_troop", slot_rival_quest_fortune_stage, qp2_fortune_purchased_commodity_in_second_town),
				(str_store_string, s37, "@Traveling to {s34}."),
			(try_end),
			(store_add, ":next_stage", reg31, 2),
			(try_begin),
				(quest_get_slot, ":final_stage", "qst_floris_trade_fortune_favors_bold", slot_quest_final_stage),
				(ge, ":next_stage", ":final_stage"),
				(ge, reg32, 4), # Last trip.
				(str_store_string, s37, "@Completing the quest upon arrival in {s36}."),
			(try_end),
			(str_store_string, s32, "@Description: {s37}"),
			(str_store_string, s35, "@Stage {reg31} on cycle {reg32}."),
			(assign, ":show_quest", 1),
		(try_end),
		
		# Quest Name
		(val_sub, ":pos_y", 25),
		(try_begin),
			(eq, ":show_quest", 1),
			(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_last_quest_s31", 380, ":pos_y", trs_obj_rival_current_quest_name, gpu_left),
			# Quest Progress
			(val_sub, ":pos_y", 25),
			(str_clear, s31),
			(str_store_string, s31, s35),
			(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 380, ":pos_y", trs_obj_rival_current_quest_progress, gpu_left),
			# Quest Description
			(val_sub, ":pos_y", 25),
			(str_clear, s31),
			(str_store_string, s31, s32),
			(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_s31", 380, ":pos_y", trs_obj_rival_current_quest_description, gpu_left),
		(else_try),
			(str_store_string, s31, "@None Active"),
			(call_script, "script_gpu_create_text_label", "str_qp2_trd_label_last_quest_s31", 380, ":pos_y", trs_obj_rival_current_quest_name, gpu_left),
		(try_end),
		
		### CURRENT QUEST ### - End
		
		(presentation_set_duration, 999999),
    ]),
	
    (ti_on_presentation_event_state_change,
    [
        (store_trigger_param_1, ":object"),
        #(store_trigger_param_2, ":value"),
		# (assign, reg21, ":object"),
		# (display_message, "@The object interacted with is #{reg21}."),
		
		# (store_sub, ":city_offset", "$tournament_town", towns_begin),
		# (store_mul, ":city_settings", ":city_offset", 10),
		
		(try_begin),
			##### DONE BUTTON #####
			(troop_slot_eq, tdp_objects, trs_obj_rival_button_done, ":object"),
			(presentation_set_duration, 0),
		
		(else_try),
			##### PREV BUTTON #####
			(troop_slot_eq, tdp_objects, trs_obj_rival_prev_troop, ":object"),
			(val_sub, "$rival_troop", 1),
			(try_begin),
				(lt, "$rival_troop", qp2_trade_rivals_begin),
				(assign, "$rival_troop", qp2_trade_rivals_end),
				(val_sub, "$rival_troop", 1),
			(try_end),
			(start_presentation, "prsnt_qp2_debug_rival_status"),
			
		(else_try),
			##### NEXT BUTTON #####
			(troop_slot_eq, tdp_objects, trs_obj_rival_next_troop, ":object"),
			(val_add, "$rival_troop", 1),
			(try_begin),
				(ge, "$rival_troop", qp2_trade_rivals_end),
				(assign, "$rival_troop", qp2_trade_rivals_begin),
			(try_end),
			(start_presentation, "prsnt_qp2_debug_rival_status"),
			
		# (else_try),
			# ##### CHANGE CENTER BUTTON #####
			# (troop_get_slot, ":towns_begin", tdp_objects, tdp_obj_centers_begin),
			# (troop_get_slot, ":towns_end",   tdp_objects, tdp_obj_centers_end),
			# (assign, ":pass", 0),
			# (try_for_range, ":center_button_check", ":towns_begin", ":towns_end"),
				# (eq, ":pass", 0), # Makes sure only the first qualifying match is used.
				# (troop_slot_eq, tdp_objects, ":center_button_check", ":object"),
				# (assign, ":pass", ":center_button_check"),
			# (try_end),
			# (is_between, ":pass", ":towns_begin", ":towns_end"),
			# (store_sub, ":center_selected", ":pass", ":towns_begin"),
			# (store_add, ":center_no", towns_begin, ":center_selected"),
			# (assign, "$tournament_town", ":center_no"),
			# (start_presentation, "prsnt_tpe_design_settings"),
			
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