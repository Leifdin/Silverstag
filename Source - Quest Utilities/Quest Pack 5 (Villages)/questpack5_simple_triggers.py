# Quest Pack 5 (1.0) by Windyplains

from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from module_quests import *
from module_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################



simple_triggers = [
	
	# TRIGGER: (Daily) - Reduce any active village quest cooldowns by 1.
	(24,[
			(try_begin),
				(ge, DEBUG_QUEST_PACK_5, 1),
				(display_message, "@DEBUG (QP5): Reducing village quest cooldowns by 1.", gpu_green),
			(try_end),
			
			(try_for_range, ":center_no", villages_begin, villages_end),
				(party_slot_ge, ":center_no", slot_village_quest_cooldown, 1),
				(party_get_slot, ":cooldown", ":center_no", slot_village_quest_cooldown),
				(val_sub, ":cooldown", 1),
				(val_max, ":cooldown", 0),
				(party_set_slot, ":center_no", slot_village_quest_cooldown, ":cooldown"),
				(ge, DEBUG_QUEST_PACK_5, 1),
				(assign, reg31, ":cooldown"),
				(str_store_party_name, s31, ":center_no"),
				(display_message, "@DEBUG (QP5): Village '{s31}' quest cooldown reduced to {reg31} days.", gpu_debug),
			(try_end),
			
			### QUEST: A CRAFTSMAN'S KNOWLEDGE
			# Purpose: Reduce days left to gather supplies by 1 if villagers are getting them.
			(try_begin),
				(check_quest_active, "qst_qp5_craftsmans_knowledge"),
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_supplies_being_obtained_by_villagers),
				(quest_slot_ge, "qst_qp5_craftsmans_knowledge", slot_quest_stage_1_trigger_chance, 1),
				(quest_get_slot, ":days_left", "qst_qp5_craftsmans_knowledge", slot_quest_stage_1_trigger_chance),
				(val_sub, ":days_left", 1),
				(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_1_trigger_chance, ":days_left"),
				(eq, ":days_left", 0),
				### Trigger warning that quest can continue.
				(quest_get_slot, ":target_center", "qst_qp5_craftsmans_knowledge", slot_quest_target_center),
				(quest_get_slot, ":center_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount), # The center upgrade spot was hidden here.
				(party_get_slot, ":improvement", ":target_center", ":center_slot"),
				(call_script, "script_get_improvement_details", ":improvement"),
				(str_store_string, s22, s0),
				(str_store_party_name, s21, ":target_center"),
				(quest_get_slot, ":item_no", "qst_qp5_craftsmans_knowledge", slot_quest_primary_commodity),
				(try_begin),
					(ge, ":item_no", 1),
					(str_store_item_name, s23, ":item_no"),
				(try_end),
				(try_begin),
					(eq, "$enable_popups", 1),
					(dialog_box, "@The villagers of {s21} have returned with the necessary {s23} to continue work on the {s22}.", "str_qp5_q4_title"),
				(try_end),
				(display_message, "@Supplies have been brought to {s21}.", gpu_green),
				# Update the quest information.
				(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_supplies_restored),
				(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
			(try_end),
			
			### QUEST: SENDING AID
			# Purpose: Count the days since you started escorting the village elder back to the initiating town.
			(try_begin),
				(check_quest_active, "qst_qp5_sending_aid"),
				(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_escort),
				(quest_get_slot, ":timer", "qst_qp5_sending_aid", slot_quest_stage_1_trigger_chance),
				(val_add, ":timer", 1),
				(quest_set_slot, "qst_qp5_sending_aid", slot_quest_stage_1_trigger_chance, ":timer"),
				# Have we taken too long to escort the elder?
				(quest_slot_ge, "qst_qp5_sending_aid", slot_quest_stage_1_trigger_chance, 10),
				# Figure out which stack the village elder is within our party.
				(party_get_num_companion_stacks, ":stack_limit", "p_main_party"),
				(try_for_range, ":stack_no", 0, ":stack_limit"),
					(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
					(is_between, ":troop_no", village_elders_begin, village_elders_end),
					(party_stack_get_troop_dna, ":troop_dna", "p_main_party", ":stack_no"),
					(party_remove_members, "p_main_party", ":troop_no", 1), # Remove the elder from the party.
					(break_loop),
				(try_end),
				# If a valid elder is found in the player's party then trigger the conversation and stage update.
				(is_between, ":troop_no", village_elders_begin, village_elders_end),
				(call_script, "script_common_quest_change_state", "qst_qp5_sending_aid", qp5_sa_took_too_long),
				(call_script, "script_qp5_quest_sending_aid", floris_quest_update),
				(start_map_conversation, ":troop_no", ":troop_dna"),
			(try_end),
		]
	),
	
	# PURPOSE: Hourly quest pulse for "A Craftsman's Knowledge" while active construction is being done.
	(1,	[
			(neg|map_free),
			(check_quest_active, "qst_qp5_craftsmans_knowledge"),
			(neg|check_quest_concluded, "qst_qp5_craftsmans_knowledge"),
			
			# Stop process if village is now being raided.
			(assign, ":continue", 1),
			(try_begin),
				(quest_get_slot, ":center_no", "qst_qp5_craftsmans_knowledge", slot_quest_target_center),
				(neg|party_slot_eq, ":center_no", slot_village_state, svs_normal),
				(assign, ":continue", 0),
				(quest_get_slot, ":building_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount),
				(party_get_slot, ":improvement_no", ":center_no", ":building_slot"),
				(call_script, "script_get_improvement_details", ":improvement_no"),
				(str_store_party_name, s21, ":center_no"),
				(rest_for_hours, 0, 0, 0), #stop resting
				(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_target_state, 0), # Stop building.
				(display_message, "@Work has been discontinued on the {s0} in {s21}.", gpu_red),
			(try_end),
			(eq, ":continue", 1),
			
			(quest_get_slot, reg1, "qst_qp5_craftsmans_knowledge", slot_quest_temp_slot),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_state, 1),
			(val_add, reg1, 1),
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_temp_slot, reg1),
			
			(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
			(assign, ":engineer_skill", reg0),
			
			# Determine how much progress is made.
			(quest_get_slot, ":progress_total", "qst_qp5_craftsmans_knowledge", slot_quest_object_state),
			(store_div, ":progress", 100, qp5_ck_pause_period), # Set this to one day's progress if you don't want to use your own men.
			#(party_get_slot, ":progress", ":center_no", slot_town_prosperity),
			(try_begin),
				# If the player is using his own men then tie his party size into progress.
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_convince_value, 1), # Player is using his men as a labor force.
				(call_script, "script_party_count_fit_regulars", "p_main_party"),
				(store_div, ":party_boost", reg0, 2),
				(store_mul, ":max_progress", ":progress", 3),
				(val_clamp, ":party_boost", 0, ":max_progress"),
				(val_max, ":progress", ":party_boost"),
			(try_end),
			(assign, reg31, ":progress"), ## Diagnostic ##
			(store_div, ":skill_progress", ":engineer_skill", 3),
			(val_max, ":skill_progress", 1), # Just in case our engineering skill is < 3.
			(assign, reg32, ":skill_progress"), ## Diagnostic ##
			(val_mul, ":progress", ":skill_progress"),
			(val_sub, ":progress_total", ":progress"),
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_object_state, ":progress_total"),
			(try_begin),
				(ge, DEBUG_QUEST_PACK_5, 1),
				(assign, reg33, ":progress"),
				(str_store_string, s31, "str_qp5_q4_title"),
				(display_message, "@DEBUG (QP5): Quest '{s31}' hourly progress = {reg32} skill * {reg31} labor = {reg33}.", gpu_debug),
			(try_end),
			
			# Advance our building time.
			(store_sub, ":needed_hours", 24, ":engineer_skill"),
			(val_mul, ":needed_hours", 3),
			(val_div, ":needed_hours", 5),
			(quest_slot_ge, "qst_qp5_craftsmans_knowledge", slot_quest_temp_slot, ":needed_hours"),
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_temp_slot, 0), # Reset building hours.
			
			(rest_for_hours, 0, 0, 0), #stop resting
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_target_state, 0), # Stop building.
			
			# Determine if someone gets hurt. [25% - (engineering skill * 3)%].  Essentially impossible > 9 engineering.
			(store_random_in_range, ":injury_roll", 0, 100),
			(store_random_in_range, ":supplies_roll", 0, 100),
			(store_mul, ":injury_prevention", ":engineer_skill", 3),
			(store_sub, ":injury_threshold", 25, ":injury_prevention"),
			# Get details on the improvement.
			(quest_get_slot, ":building_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount),
			(party_get_slot, ":improvement_no", ":center_no", ":building_slot"),
			(try_begin),
				### PROJECT COMPLETION ###
				(quest_get_slot, ":work_left", "qst_qp5_craftsmans_knowledge", slot_quest_object_state),
				(lt, ":work_left", 1),
				(quest_get_slot, ":target_center", "qst_qp5_craftsmans_knowledge", slot_quest_target_center),
				# (quest_get_slot, ":center_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount), # The center upgrade spot was hidden here.
				# (party_get_slot, ":improvement", ":target_center", ":center_slot"),
				(call_script, "script_get_improvement_details", ":improvement_no"),
				(str_store_string, s22, s0),
				(str_store_party_name, s21, ":target_center"),
				(try_begin),
					(eq, "$enable_popups", 1),
					(quest_get_slot, ":giver_troop", "qst_qp5_craftsmans_knowledge", slot_quest_giver_troop),
					(str_store_troop_name, s23, ":giver_troop"),
					(dialog_box, "@The villagers of {s21} have completed work on the {s22}.  You should seek out {s23} to discuss payment.", "str_qp5_q4_title"),
				(else_try),
					(display_message, "@The villagers of {s21} have completed work on the {s22}.", gpu_green),
				(try_end),
				(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_work_completed),
				# Change the duration to 0 so that it can't fail by time-out once we finished the project.
				(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_expiration_days, 0),
				# Set the quest text up for having been successful.
				(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
				
			(else_try),
				### WORKER IS INJURED / KILLED ###
				(lt, ":injury_roll", ":injury_threshold"),
				# Player is using his men as a labor force.
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_convince_value, 1), 
				# Make sure we aren't planting in the fields.
				(neq, ":improvement_no", slot_center_has_crops_of_grain),
				# Ensure we're at the proper stage of the quest.  This can trigger from any basic "working stage".
				(this_or_next|quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_begun),
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_supplies_restored),
				(neg|quest_slot_ge, "qst_qp5_craftsmans_knowledge", slot_quest_stage_2_trigger_chance, 3),
				(quest_get_slot, ":injuries", "qst_qp5_craftsmans_knowledge", slot_quest_stage_2_trigger_chance),
				(val_add, ":injuries", 1),
				(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_2_trigger_chance, ":injuries"),
				(jump_to_menu, "mnu_qp5_craftsmans_knowledge"),
			
			(else_try),
				### SUPPLIES RUN OUT ###
				# Ensure we're at the proper stage of the quest.  We only want this to trigger once.
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_begun),
				(neg|quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_primary_commodity, -1),
				# Determine check to beat.
				(try_begin),
					(assign, ":chance", 25),
					(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
					(assign, ":chance", 45),
					(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
					(assign, ":chance", 65),
				(try_end),
				(try_begin),
					(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_convince_value, 1),
					(val_sub, ":chance", 35),
					(val_clamp, ":chance", 0, 100),
				(try_end),
				(lt, ":supplies_roll", ":chance"),
				
				# Update the quest to the low supplies stage.
				(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_supplies_low),
				
				# Figure out where we are sending the player to.
				(call_script, "script_qus_select_random_center", center_is_town, 1, 30, ":center_no"),
				(assign, ":target_center", reg1), # Returns center # of nearby town.
				# Error trap
				(try_begin),
					(neg|is_between, ":target_center", towns_begin, towns_end),
					(store_random_in_range, ":target_center", towns_begin, towns_end),
				(try_end),
				(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_target_party, ":target_center"),
				
				# Figure out how long this should take characters that are not the player.
				(store_distance_to_party_from_party, ":distance", "p_main_party", ":target_center"),
				(store_div, ":upper", ":distance", 3),
				(store_div, ":lower", ":distance", 4),
				(store_random_in_range, ":travel_time", ":lower", ":upper"),
				(val_clamp, ":travel_time", 1, 6),
				(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_1_trigger_chance, ":travel_time"),
				
				# Start a conversation with the village elder.
				(quest_get_slot, ":target_village", "qst_qp5_craftsmans_knowledge", slot_quest_target_center),
				(party_get_slot, ":village_scene", ":target_village", slot_castle_exterior),
				(modify_visitors_at_site,":village_scene"),
				(reset_visitors),
				(try_begin),
					(quest_get_slot, ":engineer", "qst_qp5_craftsmans_knowledge", slot_quest_object_troop),
					(is_between, ":engineer", companions_begin, companions_end),
					(assign, ":conversation_troop", ":engineer"),
					(set_visitor, 11, ":engineer"),
				(else_try),
					(party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
					(assign, ":conversation_troop", ":village_elder_troop"),
					(set_visitor, 11, ":village_elder_troop"),
				(try_end),
				(set_jump_mission,"mt_village_center"),
				(jump_to_scene,":village_scene"),           
				# (change_screen_map_conversation, ":conversation_troop"),
				# (display_message, "@Conversation should have triggered!", gpu_red),
				(assign, "$g_talk_troop", ":conversation_troop"),
				# (assign, "$npc_map_talk_context", slot_troop_intro_quest_complete),
				(start_map_conversation, ":conversation_troop"),
			(else_try),
				### NO INCIDENT ENCOUNTERED ###
				(jump_to_menu, "mnu_qp5_craftsmans_knowledge_progress"),
			(try_end),
		]),
]

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "simple_triggers"
        orig_simple_triggers = var_set[var_name_1]
        orig_simple_triggers.extend(simple_triggers)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)