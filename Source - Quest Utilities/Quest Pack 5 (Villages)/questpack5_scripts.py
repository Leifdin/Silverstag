# Quest Pack 5 (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_triggers import *
from module_quests import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contains the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [
##############################################################################################################################################
############                                                COMMON QUEST SCRIPTS                                                   ###########
##############################################################################################################################################

# script_cf_common_village_quest_available
# Checks if a village quest is available for use to build a quest menu.
# Input: none
# Output: none
("cf_common_village_quest_available",
    [
		(store_script_param, ":giver_troop", 1),
		(store_script_param, ":quest_no", 2),
		
		(neg|check_quest_active,":quest_no"),
		(neg|quest_slot_ge, ":quest_no", slot_quest_dont_give_again_remaining_days, 1),
		
		(troop_get_slot, ":giver_party_no", ":giver_troop", slot_troop_leaded_party),
      
		(assign, ":giver_center_no", -1),
		(try_begin),
			(gt, ":giver_party_no", 0),
			(party_get_attached_to, ":giver_center_no", ":giver_party_no"),
		(else_try),
			(is_between, "$g_encountered_party", centers_begin, centers_end),
			(assign, ":giver_center_no", "$g_encountered_party"),
		(try_end),
		
		(assign, ":result", -1),
		(assign, ":quest_target_troop", -1),
		(assign, ":quest_target_center", -1),
		(assign, ":quest_target_faction", -1),
		(assign, ":quest_object_faction", -1),
		(assign, ":quest_object_troop", -1),
		(assign, ":quest_object_center", -1),
		(assign, ":quest_target_party", -1),
		(assign, ":quest_target_party_template", -1),
		(assign, ":quest_target_amount", -1),
		(assign, ":quest_target_dna", -1),
		(assign, ":quest_target_item", -1),
		(assign, ":quest_importance", 1),
		(assign, ":quest_xp_reward", 0),
		(assign, ":quest_gold_reward", 0),
		(assign, ":quest_convince_value", 0),
		(assign, ":quest_expiration_days", 0),
		(assign, ":quest_dont_give_again_period", 0),	 
		
		### QUEST: DELIVER GRAIN ###
		(try_begin),
			# Village Elder quests
			(eq, ":quest_no", "qst_deliver_grain"),
			(try_begin),
				(is_between, ":giver_center_no", villages_begin, villages_end),
				#The quest giver is the village elder
				(call_script, "script_get_troop_item_amount", ":giver_troop", "itm_grain"),
				(eq, reg0, 0),
				(neg|party_slot_ge, ":giver_center_no", slot_town_prosperity, 40),
				# Make sure the quest hasn't already been done here recently AND has never been failed.
				(call_script, "script_cf_qp5_verify_common_village_requirements", ":giver_center_no", ":quest_no"),
				# Setup quest info.
				(assign, ":quest_target_center", ":giver_center_no"),
				(store_random_in_range, ":quest_target_amount", 4, 8),
				(assign, ":quest_expiration_days", 0), # 30),
				(assign, ":quest_dont_give_again_period", 0), # 20),
				(assign, ":result", ":quest_no"),
			(try_end),
		
		### QUEST: DELIVER CATTLE ###
		(else_try),
			(eq, ":quest_no", "qst_deliver_cattle"),
			(try_begin),
				(is_between, ":giver_center_no", villages_begin, villages_end),
				(party_get_slot, ":num_cattle", ":giver_center_no", slot_village_number_of_cattle),
				(lt, ":num_cattle", 50),
				# Make sure the quest hasn't already been done here recently AND has never been failed.
				(call_script, "script_cf_qp5_verify_common_village_requirements", ":giver_center_no", ":quest_no"),
				#The quest giver is the village elder
				# Setup quest info.
				(assign, ":quest_target_center", ":giver_center_no"),
				(store_random_in_range, ":quest_target_amount", 5, 10),
				(assign, ":quest_expiration_days", 0), # 30),
				(assign, ":quest_dont_give_again_period", 0), # 20),
				(assign, ":result", ":quest_no"),
			(try_end),
			
		### QUEST: TRAIN PEASANTS AGAINST BANDITS ###
		(else_try),
			(eq, ":quest_no", "qst_train_peasants_against_bandits"),
			(try_begin),
				(is_between, ":giver_center_no", villages_begin, villages_end),
				#The quest giver is the village elder
				(store_skill_level, ":player_trainer", "skl_trainer", "trp_player"),
				(gt, ":player_trainer", 0),
				# Make sure the quest hasn't already been done here recently AND has never been failed.
				(call_script, "script_cf_qp5_verify_common_village_requirements", ":giver_center_no", ":quest_no"),
				# Setup quest info.
				(store_random_in_range, ":quest_target_amount", 5, 8),
				(assign, ":quest_target_center", ":giver_center_no"),
				(assign, ":quest_expiration_days", 0), # 20),
				(assign, ":quest_dont_give_again_period", 0), # 40),
				(assign, ":result", ":quest_no"),
			(try_end),
			
		### QUEST: A CRAFTSMAN'S KNOWLEDGE ###
		(else_try),
			(eq, ":quest_no", "qst_qp5_craftsmans_knowledge"),
			(try_begin),
				(is_between, ":giver_center_no", villages_begin, villages_end),
				## PREREQUISITES ##
				# Party Engineering skill of 4+.
				(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
				#(assign, ":max_skill", reg0),
				(assign, ":quest_object_troop", reg1),
				# (ge, ":max_skill", 4),
				# The village must have an assigned town lord that is not the player.
				(neg|party_slot_eq, ":giver_center_no", slot_town_lord, "trp_player"),
				(neg|party_slot_eq, ":giver_center_no", slot_town_lord, stl_unassigned),
				# An improvement must currently be in construction with less than 20 days remaining.
				(assign, ":pass", 0),
				(try_for_range, ":slot_no", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
					(party_slot_ge, ":giver_center_no", ":slot_no", 1),
					# Block certain improvements because they wouldn't make sense.
					# (neg|party_slot_eq, ":giver_center_no", ":slot_no", slot_center_has_crops_of_grain),
					(neg|party_slot_eq, ":giver_center_no", ":slot_no", slot_center_has_fire_brigade),
					# (neg|party_slot_eq, ":giver_center_no", ":slot_no", slot_center_has_improved_roads),
					# (neg|party_slot_eq, ":giver_center_no", ":slot_no", slot_center_has_crops_of_grain),
					# (neg|party_slot_eq, ":giver_center_no", ":slot_no", slot_center_has_crops_of_grain),
					(store_add, ":time_slot", ":slot_no", 3),
					(party_get_slot, ":finish_time", ":giver_center_no", ":time_slot"),
					(store_current_hours, ":cur_hours"),
					(val_sub, ":finish_time", ":cur_hours"),
					(store_div, ":days_left", ":finish_time", 24),
					### DIAGNOSTIC BEGIN
					# (assign, reg31, ":days_left"),
					# (assign, reg32, ":finish_time"),
					# (display_message, "@Improvement has {reg31} days or {reg32} hours left for construction.", gpu_debug),
					### DIAGNOSTIC END
					(lt, ":days_left", 20),
					(assign, ":pass", ":slot_no"),
				(try_end),
				(ge, ":pass", 1),
				# The player's relation with the village must be at least 0.
				(party_slot_ge, ":giver_center_no", slot_center_player_relation, 0),
				# Make sure the quest hasn't already been done here recently AND has never been failed.
				(call_script, "script_cf_qp5_verify_common_village_requirements", ":giver_center_no", ":quest_no"),
				# Setup quest info.
				(assign, ":quest_target_amount", ":pass"),
				(assign, ":quest_target_center", ":giver_center_no"),
				(assign, ":quest_expiration_days", 0), # 20),
				(assign, ":quest_dont_give_again_period", 0), # 40),
				(assign, ":result", ":quest_no"),
			(try_end),
			
		### QUEST: SENDING AID ###
		(else_try),
			(eq, ":quest_no", "qst_qp5_sending_aid"),
			(try_begin),
				(is_between, ":giver_center_no", villages_begin, villages_end),
				## PREREQUISITES ##
				# The player's relation with the village must be >= -5.
				(party_slot_ge, ":giver_center_no", slot_center_player_relation, -5),
				# Make sure the quest hasn't already been done here recently AND has never been failed.
				(call_script, "script_cf_qp5_verify_common_village_requirements", ":giver_center_no", ":quest_no"),
				# Another village nearby needs to be recovering from a raid.
				(assign, ":raided_village", -1),
				(store_faction_of_party, ":giver_faction", ":giver_center_no"),
				(try_for_range, ":center_no", villages_begin, villages_end),
					(party_slot_eq, ":center_no", slot_village_state, svs_looted),
					(neq, ":center_no", ":giver_center_no"), # Right..don't ask for help sending aid to yourself.
					(neg|party_slot_ge, ":center_no", slot_village_recover_progress, 50), # Our potential target is <= 49% recovery.
					(store_faction_of_party, ":faction_no", ":center_no"),
					(store_relation, ":relation", ":faction_no", ":giver_faction"),
					(ge, ":relation", 0),
					(store_distance_to_party_from_party, ":distance", ":center_no", ":giver_center_no"),
					(try_begin),
						### DIAGNOSTIC ###
						# (assign, reg31, ":distance"),
						# (assign, reg32, ":relation"),
						# (party_get_slot, reg33, ":center_no", slot_village_recover_progress),
						# (str_store_party_name, s31, ":center_no"),
						# (display_message, "@DEBUG (sending aid): {s31} has a relation of {reg32}, distance {reg31} and recovery {reg33}%.", gpu_debug),
						### DIAGNOSTIC ###
					(try_end),
					(lt, ":distance", 30),
					(assign, ":raided_village", ":center_no"),
					(break_loop),
				(try_end),
				# Setup quest info.
				(is_between, ":raided_village", villages_begin, villages_end),
				(assign, ":quest_target_center", ":raided_village"),
				(assign, ":quest_expiration_days", 0), # 20),
				(assign, ":quest_dont_give_again_period", 0), # 40),
				(assign, ":result", ":quest_no"),
			(try_end),
		
		### QUEST: A HEALER'S TOUCH ###
		(else_try),
			(eq, ":quest_no", "qst_qp5_healers_touch"),
			(eq, 1, 0), ### DEVELOPMENT BLOCK ###
			(try_begin),
				(is_between, ":giver_center_no", villages_begin, villages_end),
				## PREREQUISITES ##
				# Make sure the quest hasn't already been done here recently AND has never been failed.
				(call_script, "script_cf_qp5_verify_common_village_requirements", ":giver_center_no", ":quest_no"),
				# Player party must have a companion with surgery or wound treatment of 4+.
				(party_get_num_companion_stacks, ":stack_limit","p_main_party"),
				(assign, ":max_skill_wound_treatment", -1),
				(assign, ":max_skill_surgery", -1),
				(assign, ":troop_wound_treatment", -1),
				(assign, ":troop_surgery", -1),
				(try_for_range, ":stack_no", 0, ":stack_limit"),
					(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
					(neq, ":troop_no", "trp_player"),
					(troop_is_hero, ":troop_no"),
					(store_skill_level, ":skill_wound_treatment", "skl_wound_treatment", ":troop_no"),
					(store_skill_level, ":skill_surgery", "skl_surgery", ":troop_no"),
					# See if this person's wound treatment skill is better than our current value.
					(try_begin),
						(gt, ":skill_wound_treatment", ":max_skill_wound_treatment"),
						(assign, ":max_skill_wound_treatment", ":skill_wound_treatment"),
						(assign, ":troop_wound_treatment", ":troop_no"),
					(try_end),
					# See if this person's surgery skill is better than our current value.
					(try_begin),
						(gt, ":skill_surgery", ":max_skill_surgery"),
						(assign, ":max_skill_surgery", ":skill_surgery"),
						(assign, ":troop_surgery", ":troop_no"),
					(try_end),
				(try_end),
				(this_or_next|ge, ":max_skill_surgery", 4),
				(ge, ":max_skill_wound_treatment", 4),
				# Determine which skill to use for the quest.
				(assign, ":pass", 0),
				(try_begin),
					(ge, ":max_skill_surgery", ":max_skill_wound_treatment"), # Use the highest skill.
					(ge, ":max_skill_surgery", 4),
					(assign, ":skill_type", "skl_surgery"),
					(assign, ":quest_object_troop", ":troop_surgery"),
					(assign, ":pass", 1),
				(else_try),
					(ge, ":max_skill_wound_treatment", 4),
					(assign, ":skill_type", "skl_wound_treatment"),
					(assign, ":quest_object_troop", ":troop_wound_treatment"),
					(assign, ":pass", 1),
				(try_end),
				(eq, ":pass", 1),
				# Name the sick individual.
				(store_faction_of_party, ":giver_faction", ":giver_center_no"),
				(store_random_in_range, ":is_female", 0, 2),
				(call_script, "script_common_store_temp_name_to_s1", ":is_female", ":giver_faction", SCRT_FULL),
				(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance, reg1),         # Holds the first name of the sick individual.
				(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance, reg2),         # Holds the last name of the sick individual.
				(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance, ":is_female"), # Holds the gender of the sick individual.
				(quest_set_slot, ":quest_no", slot_quest_object_state, ":skill_type"),          # Holds the skill type of the companion.
			
				# Setup quest info.
				(is_between, ":raided_village", villages_begin, villages_end),
				(assign, ":quest_expiration_days", 0), # 20),
				(assign, ":quest_dont_give_again_period", 0), # 40),
				(assign, ":result", ":quest_no"),
			(try_end),
		
		(try_end),
		
		(neq, ":result", -1),
			
		(try_begin),
		  (party_is_active, ":quest_target_center"),
		  (store_faction_of_party, ":quest_target_faction", ":quest_target_center"),
		(try_end),
		
		(quest_set_slot, ":quest_no", slot_quest_target_troop, ":quest_target_troop"),
		(quest_set_slot, ":quest_no", slot_quest_target_center, ":quest_target_center"),
		(quest_set_slot, ":quest_no", slot_quest_object_troop, ":quest_object_troop"),
		(quest_set_slot, ":quest_no", slot_quest_target_faction, ":quest_target_faction"),
		(quest_set_slot, ":quest_no", slot_quest_object_faction, ":quest_object_faction"),
		(quest_set_slot, ":quest_no", slot_quest_object_center, ":quest_object_center"),
		(quest_set_slot, ":quest_no", slot_quest_target_party, ":quest_target_party"),
		(quest_set_slot, ":quest_no", slot_quest_target_party_template, ":quest_target_party_template"),
		(quest_set_slot, ":quest_no", slot_quest_target_amount, ":quest_target_amount"),
		(quest_set_slot, ":quest_no", slot_quest_importance, ":quest_importance"),
		(quest_set_slot, ":quest_no", slot_quest_xp_reward, ":quest_xp_reward"),
		(quest_set_slot, ":quest_no", slot_quest_gold_reward, ":quest_gold_reward"),
		(quest_set_slot, ":quest_no", slot_quest_convince_value, ":quest_convince_value"),
		(quest_set_slot, ":quest_no", slot_quest_expiration_days, ":quest_expiration_days"),
		(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period, ":quest_dont_give_again_period"),
		(quest_set_slot, ":quest_no", slot_quest_current_state, 0),
		(quest_set_slot, ":quest_no", slot_quest_giver_troop, ":giver_troop"),
		(quest_set_slot, ":quest_no", slot_quest_giver_center, ":giver_center_no"),
		(quest_set_slot, ":quest_no", slot_quest_target_dna, ":quest_target_dna"),
		(quest_set_slot, ":quest_no", slot_quest_target_item, ":quest_target_item"),
	]),
	
# script_cf_qp5_ignore_failures
# PURPOSE: These quests are not intended to trigger humanitarian companions complaining so they are added to the module_scripts exception list.
("cf_qp5_ignore_failures",
  [
		#(store_script_param, ":quest_no", 1),
		
		## NOTE: The quests that are commented out are included to show they were intentionally ommitted so as to cause objection.
		# (neq, ":quest_no", "qst_qp5_craftsmans_knowledge"),
		# (neq, ":quest_no", "qst_qp5_sending_aid"),
	]),
	
# script_qp5_track_town_entry
# PURPOSE: Checks when the player enters a town using script "music_set_situation_with_culture" called in menu "town" to update quest stages as needed.
("qp5_track_town_entry",
  [
		(store_script_param, ":center_no", 1),
		
		(try_begin),
			##### QUEST: A CRAFTSMAN'S KNOWLEDGE #####
			(check_quest_active, "qst_qp5_craftsmans_knowledge"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_party, ":center_no"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_supplies_being_obtained_by_player),
			(quest_get_slot, ":item_no", "qst_qp5_craftsmans_knowledge", slot_quest_primary_commodity),
			(call_script, "script_common_merchant_stock_minimum_amount", ":center_no", ":item_no", 1),
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
		(try_end),
	]),
	
# script_qp5_arrive_in_village
# PURPOSE: 
("qp5_arrive_in_village",
	[
		(store_script_param, ":center_no", 1),
		
		(try_begin),
			##### QUEST: A CRAFTSMAN'S KNOWLEDGE #####
			(check_quest_active, "qst_qp5_craftsmans_knowledge"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_center, ":center_no"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_supplies_being_obtained_by_player),
			(quest_get_slot, ":item_no", "qst_qp5_craftsmans_knowledge", slot_quest_primary_commodity),
			(store_item_kind_count, ":count", ":item_no", "trp_player"),
			(ge, ":count", 1),
			(display_message, "@You have brought the necessary tools back for construction to continue.", gpu_green),
			(troop_remove_item, "trp_player", ":item_no"),
			(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_supplies_restored),
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_primary_commodity, -1), # To track we've done this side-quest.
		(try_end),
		
		(try_begin),
			##### QUEST: SENDING AID #####
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_giver_center, ":center_no"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_escort),
			(call_script, "script_common_quest_change_state", "qst_qp5_sending_aid", qp5_sa_returned_to_giver),
			# We've delivered the elder.  Now remove him from the party.
			(party_get_num_companion_stacks, ":stack_limit", "p_main_party"),
			(try_for_range, ":stack_no", 0, ":stack_limit"),
				(party_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
				(is_between, ":troop_no", village_elders_begin, village_elders_end),
				#(party_stack_get_troop_dna, ":troop_dna", "p_main_party", ":stack_no"),
				(party_remove_members, "p_main_party", ":troop_no", 1), # Remove the elder from the party.
				(break_loop),
			(try_end),
			## ERROR TRAP ##
			(neg|is_between, ":troop_no", village_elders_begin, village_elders_end),
			(display_message, "@ERROR - Quest 'Sending Aid' did not have an Elder to turn in at end of journey.", gpu_red),
		(try_end),
	]),
	 
# script_qp5_game_start
# Contains all initialization scripts needed for Quest Pack 5.
# INPUT:  none
# OUTPUT: none
("qp5_game_start",
  [
		# Setup initial pre-define for $quest_reactions
		#(assign, "$quest_reactions", QUEST_REACTIONS_HIGH),
		#(troop_raise_skill, "trp_player", "skl_persuasion", 4),
		
		(try_begin),
			(ge, DEBUG_QUEST_PACK_5, 1),
			(display_message, "@DEBUG (QP5): Quest Pack 5 initialized."),
		(try_end),
	]),
	
# script_cf_qp5_verify_common_village_requirements
# PURPOSE: Makes sure this quest has never been failed in this center AND that no other quest has been recently completed here.
("cf_qp5_verify_common_village_requirements",
  [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":quest_no", 2),
		
		# Make sure the quest hasn't already been done here recently AND has never been failed.
		(party_slot_eq, ":center_no", slot_village_quest_cooldown, 0),
		(call_script, "script_qp5_verify_quest_status", ":quest_no", QUEST_NOT_STARTED, ":center_no"),
		(assign, ":status_never_taken", reg1),
		(call_script, "script_qp5_verify_quest_status", ":quest_no", QUEST_COMPLETED, ":center_no"),
		(assign, ":status_succeeded", reg1),
		(this_or_next|eq, ":status_never_taken", 1),
		(eq, ":status_succeeded", 1),
		
	]),
	
# script_qp5_verify_quest_status - (":quest_no", ":desired_status", ":center_no")
# PURPOSE: These quests are not intended to trigger humanitarian companions complaining so they are added to the module_scripts exception list.
("qp5_verify_quest_status",
  [
		(store_script_param, ":quest_no", 1),
		(store_script_param, ":desired_status", 2),
		(store_script_param, ":center_no", 3),
		
		(assign, ":pass", 0), # Fail this check by default.
		
		(try_begin),
			(is_between, ":quest_no", village_elder_quests_begin, village_elder_quests_end),
			(try_begin),
				(is_between, ":center_no", villages_begin, villages_end),
				# Determine appropriate quest slot.
				(store_sub, ":quest_slot", ":quest_no", village_elder_quests_begin),
				(val_add, ":quest_slot", qp5_quest_slots_begin),
				# Check current status against the desired status.
				(try_begin),
					(party_slot_eq, ":center_no", ":quest_slot", ":desired_status"),
					(assign, ":pass", 1),
				(try_end),
				(try_begin),
					(ge, DEBUG_QUEST_PACK_5, 2),
					(store_sub, ":string_title", ":quest_no", village_elder_quests_begin),
					(val_add, ":string_title", "str_qp5_q1_title"),
					(str_store_string, s30, ":string_title"),
					(party_get_slot, ":current_status", ":center_no", ":quest_slot"),
					(store_add, ":string_desired", "str_qp5_quest_status_0", ":desired_status"),
					(str_store_string, s31, ":string_desired"),
					(store_add, ":string_current", "str_qp5_quest_status_0", ":current_status"),
					(str_store_string, s32, ":string_current"),
					(assign, reg31, ":pass"),
					(display_message, "@DEBUG (QP5): Quest '{s30}' status is {s32}.  Desired {s31} => Check {reg31?Passed:Failed}.", gpu_debug),
				(try_end),
				
			(else_try),
				### ERROR - INVALID CENTER ###
				(str_store_quest_name, s30, ":quest_no"),
				(str_store_party_name, s31, ":center_no"),
				(assign, reg31, ":center_no"),
				(display_message, "str_qp5_error_invalid_center", gpu_red),
			(try_end),
			
		(else_try),
			### ERROR - INVALID QUEST ###
			(str_store_party_name, s31, ":quest_no"),
			(assign, reg31, ":quest_no"),
			(display_message, "str_qp5_error_invalid_quest", gpu_red),
		(try_end),
		(assign, reg1, ":pass"),
	]),

# script_qp5_set_quest_status - (":quest_no", ":new_status", ":center_no")
# PURPOSE: These quests are not intended to trigger humanitarian companions complaining so they are added to the module_scripts exception list.
("qp5_set_quest_status",
  [
		(store_script_param, ":quest_no", 1),
		(store_script_param, ":new_status", 2),
		(store_script_param, ":center_no", 3),
		
		(try_begin),
			(is_between, ":quest_no", village_elder_quests_begin, village_elder_quests_end),
			(try_begin),
				(is_between, ":center_no", villages_begin, villages_end),
				# Determine appropriate quest slot.
				(store_sub, ":quest_slot", ":quest_no", village_elder_quests_begin),
				(val_add, ":quest_slot", qp5_quest_slots_begin),
				# Get the old status for debugging.
				(party_get_slot, ":old_status", ":center_no", ":quest_slot"),
				# Set the current status.
				(party_set_slot, ":center_no", ":quest_slot", ":new_status"),
				# Remove global cooldown for native quests, but set village cooldown to 5 days.
				(try_begin),
					(eq, ":new_status", QUEST_COMPLETED),
					(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period, 0),
					(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
					# Set in a try block to allow "not equal" operations stopping story quests from becoming available again.
					(party_set_slot, ":center_no", slot_village_quest_cooldown, 5),
				(try_end),
				
				(try_begin),
					(ge, DEBUG_QUEST_PACK_5, 1),
					(store_sub, ":string_title", ":quest_no", village_elder_quests_begin),
					(val_add, ":string_title", "str_qp5_q1_title"),
					(str_store_string, s30, ":string_title"),
					(party_get_slot, ":new_status", ":center_no", ":quest_slot"),
					(store_add, ":string_new", "str_qp5_quest_status_0", ":new_status"),
					(str_store_string, s31, ":string_new"),
					(store_add, ":string_old", "str_qp5_quest_status_0", ":old_status"),
					(str_store_string, s32, ":string_old"),
					(display_message, "@DEBUG (QP5): Quest '{s30}' status changed from {s32} to {s31}.", gpu_debug),
				(try_end),
				
			(else_try),
				### ERROR - INVALID CENTER ###
				(str_store_quest_name, s30, ":quest_no"),
				(str_store_party_name, s31, ":center_no"),
				(assign, reg31, ":center_no"),
				(display_message, "str_qp5_error_invalid_center", gpu_red),
			(try_end),
			
		(else_try),
			### ERROR - INVALID QUEST ###
			(str_store_party_name, s31, ":quest_no"),
			(assign, reg31, ":quest_no"),
			(display_message, "str_qp5_error_invalid_quest", gpu_red),
		(try_end),
		
	]),
	

# script_qp5_quest_craftsmans_knowledge
# PURPOSE: Handles all quest specific actions for quest "qp5_craftsmans_knowledge".
("qp5_quest_craftsmans_knowledge",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_qp5_craftsmans_knowledge"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp5_q4_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# QP5_QUEST_INACTIVE                              = 0
		# qp5_ck_begun                                    = 1
		# qp5_ck_worker_injury                            = 2
		# qp5_ck_supplies_low                             = 3
		# qp5_ck_supplies_being_obtained_by_villagers     = 4
		# qp5_ck_supplies_being_obtained_by_player        = 5
		# qp5_ck_supplies_restored                        = 6
		# qp5_ck_work_completed                           = 7
		# qp5_ck_quest_failed                             = 8
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            qp5_ck_begun),
			
			#(quest_set_slot, ":quest_no", slot_quest_giver_troop,                    -1),              # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,                   "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_target_center,                  "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_expiration_days,                30),              # Based upon the duration of the improvement being built.
			#(quest_set_slot, ":quest_no", slot_quest_object_troop,                   30),              # Holds the troop # of the maximum engineering skill owner.
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_temp_slot,                       0),               # We're storing how many hours have been spent building on the project here.
			(quest_set_slot, ":quest_no", slot_quest_target_state,                    0),               # Tracks whether or not the player is currently building.  (1 = yes, 0 = no)
			(quest_set_slot, ":quest_no", slot_quest_object_state,                    0),               # This tracks overall progress needed to complete the improvement.  (Done to speed it up).
			(quest_set_slot, ":quest_no", slot_quest_target_party,                    0),               # This will hold the town # of the center we need to buy supplies from.
			(quest_set_slot, ":quest_no", slot_quest_primary_commodity,     "itm_tools"),               # This holds the "low supplies" item # needed.
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          0),               # This tracks how many days until the workers return from getting supplies if the player doesn't fetch them.
			#(quest_set_slot, ":quest_no", slot_quest_target_amount,                   0),              # Holds the center slot that is building the improvement.
			#(quest_set_slot, ":quest_no", slot_quest_convince_value,                  0),              # Tracks whether or not the player is using his own men. (1 = yes, 0 = no)
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          0),               # This tracks how many injuries occur during construction to keep a limit on that.
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          0),               # This tracks if the player went to get the supplies or not.
			
			# Setup an expiration date based upon the completion of the improvement.
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(quest_get_slot, ":building_slot", ":quest_no", slot_quest_target_amount),
			(call_script, "script_building_slot_get_days_to_complete", ":center_no", ":building_slot"),
			(assign, ":days_left", reg1),
			(val_add, ":days_left", 1), # Make sure a remainder of hours doesn't fail the quest.
			(quest_set_slot, ":quest_no", slot_quest_expiration_days, ":days_left"),
			# Establish who our main engineer is.
			(quest_get_slot, ":engineer", ":quest_no", slot_quest_object_troop),
			(try_begin),
				(is_between, ":engineer", companions_begin, companions_end),
				(str_store_troop_name_link, s12, ":engineer"),
				(troop_get_type, reg21, ":engineer"),
				(str_store_string, s21, "@the aid of your companion {s12}, due to {reg21?her:his} skill in engineering,"),
			(else_try),
				(str_store_troop_name, s12, "trp_player"),
				(str_store_string, s21, "@your aid"),
			(try_end),
			# Figure out how long this should take.
			(party_get_slot, ":improvement_no", ":center_no", ":building_slot"),
			(store_mul, ":duration", ":days_left", 100),
			(try_begin),
				# Special Case: For Fields of Grain ensure we cut the duration down to only a few days.
				(eq, ":improvement_no", slot_center_has_crops_of_grain),
				(val_min, ":duration", 600),
				(store_div, ":reduced_days_left", ":duration", 75),
				(quest_set_slot, ":quest_no", slot_quest_expiration_days, ":reduced_days_left"),
			(try_end),
			(quest_set_slot, ":quest_no", slot_quest_object_state, ":duration"),
			# Figure out what it is we're building.
			(call_script, "script_get_improvement_details", ":improvement_no"),
			# Determine who is giving the quest.
			(quest_get_slot, ":giver_troop", ":quest_no", slot_quest_giver_troop),
			# Setup quest text.
			(str_store_party_name_link, s13, ":center_no"),
			(str_store_troop_name, s14, ":giver_troop"),
			(str_store_string, s61, "@{s14}, village elder of {s13}, has requested {s21} to help finish the construction of {s2}."),
			#(str_store_string, s3, "@^One of your merchant mentioned that an old friend of his in {s13} has been trying to sell his {s14} unsuccessfully and is offering a considerable discount.^{s3}"),
			# Clear out any old quest notes.
			(str_clear, s1),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", ":giver_troop", "str_qp5_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Special information needed.
			(quest_get_slot, ":giver_troop", ":quest_no", slot_quest_giver_troop),
			# Improvement
			(quest_get_slot, ":target_village", ":quest_no", slot_quest_target_center),
			(quest_get_slot, ":center_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount), # The center upgrade spot was hidden here.
			(party_get_slot, ":improvement", ":target_village", ":center_slot"),
			(call_script, "script_get_improvement_details", ":improvement"),
			(str_store_string, s22, s0),
			(str_store_troop_name, s21, ":giver_troop"),
			(quest_get_slot, ":item_no", ":quest_no", slot_quest_primary_commodity),
			(try_begin),
				(ge, ":item_no", 1),
				(str_store_item_name, s23, ":item_no"),
			(try_end),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(assign, ":notify_of_update", 1),
			(try_begin),
				(eq, ":quest_stage", qp5_ck_worker_injury),
				(str_store_string, s65, "@One of your men has been harmed during construction and you've had all work stopped until you speak to {s21}."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp5_ck_begun),
				(str_store_string, s65, "@Work on {s22} has resumed."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp5_ck_supplies_being_obtained_by_villagers),
				(str_store_string, s65, "@Work on the {s22} has stopped due to a shortage of {s23}.  You have had several villagers sent to acquire more."),
				(assign, ":note_slot", 4),
				(assign, ":notify_of_update", 0),
			(else_try),
				(eq, ":quest_stage", qp5_ck_supplies_being_obtained_by_player),
				(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_party),
				(str_store_party_name_link, s24, ":target_center"),
				(str_store_string, s65, "@Work on the {s22} has stopped due to a shortage of {s23} and you have chosen to travel to {s24} to acquire more."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp5_ck_supplies_restored),
				(str_store_string, s65, "@The shortage of {s23} has been resolved and work is now able to resume."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp5_ck_work_completed),
				(str_store_string, s65, "@The {s22} has been completed.  You should seek out {s21} to inform him."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp5_ck_quest_failed),
				(str_store_string, s65, "@You have failed to complete the {s22} in time.  You should seek out {s21} to inform him."),
				(assign, ":note_slot", 5),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64}{s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(try_begin),
				(eq, ":notify_of_update", 1),
				(display_message, "str_quest_log_updated", gpu_light_blue),
			(try_end),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_COMPLETED, ":center_no"), 
			# Rewards
			(assign, ":xp_bonus", 200),       # Experience gain given to the player for getting supplies if they were low.
			(assign, ":gold_base", 10),       # Default payment.
			(assign, ":gold_high", 20),       # Higher payment amount based upon 
			(assign, ":relation_town", 1),
			(assign, ":relation_lord", 2),    # Relation boost with the village's lord.
			(assign, ":relation_faction", 0), # Relation boost with the village's faction.
			(assign, ":xp_engineer", 300),    # Experience gain given towards the party engineer.
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(assign, ":gold_base", 14),
				(assign, ":gold_high", 30),
				(val_add, ":relation_town", 1),
				(val_add, ":relation_lord", 1),
				(val_add, ":relation_faction", 1),
				(val_add, ":xp_engineer", 150),
				(val_add, ":xp_bonus", 150),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(assign, ":gold_base", 18),
				(assign, ":gold_high", 40),
				(val_add, ":relation_town", 1),
				(val_add, ":xp_engineer", 150),
				(val_add, ":xp_bonus", 150),
			(try_end),
			
			# Award party experience.
			(quest_get_slot, ":troop_engineer", ":quest_no", slot_quest_object_troop),
			(try_begin),
				(is_between, ":troop_engineer", companions_begin, companions_end),
				(add_xp_to_troop, ":xp_engineer", ":troop_engineer"),
				(str_store_troop_name, s21, ":troop_engineer"),
				(display_message, "@Experience awarded to the {s21} for overseeing construction.", gpu_green),
			(else_try),
				(add_xp_to_troop, ":xp_engineer", "trp_player"),
			(try_end),
			
			# Award bonus experience if the player went to get the bonus supplies.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_primary_commodity, -1), # We know that this supplies trigger occurred.
				(quest_slot_eq, ":quest_no", slot_quest_stage_3_trigger_chance, 1), # We know the player went to get the supplies.
				(add_xp_to_troop, ":xp_bonus", "trp_player"),
				(display_message, "@Bonus experience awarded to the {playername} for acquiring the needed supplies.", gpu_green),
			(try_end),
			
			# Raise relation with the local town lord.
			(party_get_slot, ":troop_lord", ":center_no", slot_town_lord),
			(try_begin),
				(ge, ":relation_lord", 1),
				(is_between, ":troop_lord", active_npcs_begin, active_npcs_end),
				(call_script, "script_change_player_relation_with_troop", ":troop_lord", ":relation_lord", 1),
			(try_end),
			
			# Change town reputation.
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":center_no", ":relation_town"),
			
			# Change faction reputation.
			(try_begin),
				(ge, ":relation_faction", 1),
				(store_faction_of_party, ":faction_no", ":center_no"),
				(call_script, "script_change_player_relation_with_faction", ":faction_no", ":relation_faction"),
			(try_end),
			
			# Pay the player.
			(try_begin),
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_convince_value, 1), # Player used his men as a labor force.
				(assign, ":gold_base", ":gold_high"),
			(try_end),
			(quest_get_slot, ":building_slot", ":quest_no", slot_quest_target_amount),
			(party_get_slot, ":improvement_no", ":center_no", ":building_slot"),
			(call_script, "script_get_improvement_details", ":improvement_no"), # Retrieves reg0 as a base cost for building.
			(try_begin),
				# Special Case: Fields of grain cost almost nothing to make so a base value needs to be set.
				(eq, ":improvement_no", slot_center_has_crops_of_grain),
				(assign, reg0, 1200),
			(try_end),
			(store_mul, ":gold_reward", reg0, ":gold_base"),
			(val_div, ":gold_reward", 100),
			(call_script, "script_troop_add_gold", "trp_player", ":gold_reward"),
			
			## SILVERSTAG EMBLEMS+ ##
			(call_script, "script_cf_emblem_quest_reward_check", 2), # emblem_scripts.py
			## SILVERSTAG EMBLEMS- ##
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_common_quest_change_state", ":quest_no", qp5_ck_quest_failed),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_WAS_FAILED, ":center_no"),
			# Rewards
			(assign, ":relation_town", -2),
			(assign, ":relation_engineer", -2), # Relation hit with the engineer troop if not the player.
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":relation_town", -1),
				(val_add, ":relation_engineer", -1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":relation_town", -1),
				(val_add, ":relation_engineer", -1),
			(try_end),
			# Change town reputation.
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":center_no", ":relation_town"),
			# Change relation with the engineer (if not the player).
			(quest_get_slot, ":troop_engineer", ":quest_no", slot_quest_object_troop),
			(try_begin),
				(is_between, ":troop_engineer", companions_begin, companions_end),
				(call_script, "script_change_player_relation_with_troop", ":troop_engineer", ":relation_engineer", 0),
			(try_end),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_NOT_STARTED, ":center_no"),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp5_quest_sending_aid
# PURPOSE: Handles all quest specific actions for quest "qp5_sending_aid".
("qp5_quest_sending_aid",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_qp5_sending_aid"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp5_q5_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# QP5_QUEST_INACTIVE                              = 0
		# qp5_sa_begun                                    = 1
		# qp5_sa_recovery                                 = 2
		# qp5_sa_village_recovered                        = 3
		# qp5_sa_escort                                   = 4
		# qp5_sa_took_too_long                            = 5
		# qp5_sa_returned_to_giver                        = 6
		# qp5_sa_failed_to_appear                         = 7
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            qp5_sa_begun),
			
			#(quest_set_slot, ":quest_no", slot_quest_giver_troop,                    -1),              # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,                   "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_target_center,                  "$current_town"), # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_expiration_days,                30),              # Based upon the duration of the improvement being built.
			(quest_set_slot, ":quest_no", slot_quest_object_troop,                    0),              
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,        ":quest_title"),
			# (quest_set_slot, ":quest_no", slot_quest_temp_slot,                       0),
			(quest_set_slot, ":quest_no", slot_quest_target_state,                    0),               # Tracks exit stage. (1 = left after supplie delivery, 2 = left after town recovery, 3 = finished entire quest)
			# (quest_set_slot, ":quest_no", slot_quest_object_state,                    0),
			# (quest_set_slot, ":quest_no", slot_quest_target_party,                    0),
			# (quest_set_slot, ":quest_no", slot_quest_primary_commodity,               0),
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          0),               # Tracks the # of days you've been traveling with the village elder.
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   0),               # Tracks the % of recovery spent guarding the village.
			# (quest_set_slot, ":quest_no", slot_quest_convince_value,                  0),
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          0),               # Tracks how many times the player has been warned to stay near the target village to defend it.
			# (quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          0),
			
			# Setup an expiration date based upon the recovery rate of the target center.
			(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
			# (party_get_slot, ":recovery_state", ":target_center", slot_village_recover_progress),
			# (store_sub, ":days_left", 100, ":recovery_state"),
			
			# Determine who is giving the quest.
			(quest_get_slot, ":giver_troop", ":quest_no", slot_quest_giver_troop),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_giver_center),
			# Setup quest text.
			(str_store_party_name_link, s13, ":center_no"),
			(str_store_troop_name, s14, ":giver_troop"),
			(str_store_party_name_link, s15, ":target_center"),
			(str_store_string, s61, "@{s14}, village elder of {s13}, has requested your help in transporting supplies to help the village of {s15} rebuild after being recently raided.  He has requested that you stay in the area to help them rebuild quicker and fend off any that would take advantage of their defenseless state."),
			# Clear out any old quest notes.
			(str_clear, s1),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", ":giver_troop", "str_qp5_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Name the town (target)
			(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
			(str_store_party_name_link, s21, ":target_center"),
			# Name the village elder. (target)
			(store_sub, ":center_offset", ":target_center", villages_begin),
			(store_add, ":target_mayor", ":center_offset", "trp_village_1_elder"),
			(str_store_troop_name, s22, ":target_mayor"),
			# Name the town (giver)
			(quest_get_slot, ":giver_center", ":quest_no", slot_quest_giver_center),
			(str_store_party_name_link, s23, ":giver_center"),
			# Name the village elder. (giver)
			(store_sub, ":center_offset", ":giver_center", villages_begin),
			(store_add, ":giver_mayor", ":center_offset", "trp_village_1_elder"),
			(str_store_troop_name, s24, ":giver_mayor"),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(assign, ":notify_of_update", 1),
			(try_begin),
				(eq, ":quest_stage", qp5_sa_recovery),
				(str_store_string, s65, "@The necessary supplies have arrived in {s21}.  The village could use your help keeping the area clear of raiders while they rebuild."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp5_sa_village_recovered),
				(str_store_string, s65, "@Your scouts inform you that repairs in {s21} have been made.  You should seek out {s22}."),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp5_sa_escort),
				(str_store_string, s65, "@{s22} has asked that you escort him back to {s23} to meet with {s24}."),
				(assign, ":note_slot", 5),
			(else_try),
				(eq, ":quest_stage", qp5_sa_took_too_long),
				(str_store_string, s65, "@{s22} has left the party to make his own way to {s23}."),
				(assign, ":note_slot", 5),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64}{s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(try_begin),
				(eq, ":notify_of_update", 1),
				(display_message, "str_quest_log_updated", gpu_light_blue),
			(try_end),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_COMPLETED, ":center_no"), 
			# Rewards
			(assign, ":xp_base", 400),        # Experience gain given to the player for getting supplies if they were low.
			(assign, ":relation_giver", 2),   # Relation boost with the village that sent the aid.
			(assign, ":relation_target", 1),  # Relation boost with the village that received the aid.
			(assign, ":relation_lord", 0),    # Relation boost with the village's lord.
			(assign, ":right_to_rule", 0),    # Change the player's right to rule.
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":relation_giver", 1),
				(val_add, ":relation_target", 1),
				(val_add, ":relation_lord", 0),
				(val_add, ":xp_base", 400),
				(val_add, ":right_to_rule", 1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":relation_giver", 1),
				(val_add, ":relation_target", 2),
				(val_add, ":relation_lord", 2),
				(val_add, ":xp_base", 400),
			(try_end),
			
			# Award bonus experience if the player stayed to defend the town.  This is mandatory for high quest reactions.
			(try_begin),
				(quest_slot_ge, ":quest_no", slot_quest_target_amount, -1), # Make sure the player spent some time helping the raided village.
				(quest_get_slot, ":xp_help", ":quest_no", slot_quest_target_amount),
				(store_mul, ":xp_award", ":xp_base", ":xp_help"),
				(val_div, ":xp_award", 100),
				(party_add_xp, "p_main_party", ":xp_award"),
				(assign, reg21, ":xp_award"),
				(display_message, "@Bonus experience awarded for helping defend the town. [+{reg21}xp]", gpu_green),
			(try_end),
			
			# Award bonus experience if the player escorted the elder back.
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_target_state, 3),
				# Award bonus experience.
				(store_mul, ":xp_award", ":xp_base", 25),
				(val_div, ":xp_award", 100),
				(party_add_xp, "p_main_party", ":xp_award"),
				(assign, reg21, ":xp_award"),
				# Name the village elder.
				(quest_get_slot, ":giver_center", ":quest_no", slot_quest_giver_center),
				(quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
				(store_sub, ":center_offset", ":target_center", villages_begin),
				(store_add, ":mayor", ":center_offset", "trp_village_1_elder"),
				(str_store_troop_name, s21, ":mayor"),
				(str_store_party_name, s22, ":giver_center"),
				(display_message, "@Bonus experience awarded for escorting {s21} to {s22}. [+{reg21}xp]", gpu_green),
				
				# Increase player honor.
				(call_script, "script_change_player_honor", 2),
				
				# Change player right to rule.
				(call_script, "script_change_player_right_to_rule", ":right_to_rule"),
				
			(try_end),
			
			# Raise relation with the local town lord.
			(party_get_slot, ":troop_lord", ":center_no", slot_town_lord),
			(try_begin),
				(ge, ":relation_lord", 1),
				(is_between, ":troop_lord", active_npcs_begin, active_npcs_end),
				(call_script, "script_change_player_relation_with_troop", ":troop_lord", ":relation_lord", 1),
			(try_end),
			
			# Change town reputation.
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":center_no", ":relation_giver"),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_change_player_relation_with_center", ":center_no", ":relation_target"),
			
			## SILVERSTAG EMBLEMS+ ##
			(call_script, "script_cf_emblem_quest_reward_check", 2), # emblem_scripts.py
			## SILVERSTAG EMBLEMS- ##
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_WAS_FAILED, ":center_no"),
			# Rewards
			(assign, ":relation_town", -2),
			(assign, ":honor_loss", -1),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":relation_town", -1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":relation_town", -1),
				(val_add, ":honor_loss", -1),
			(try_end),
			# Change town reputation.
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_giver_center),
			(call_script, "script_change_player_relation_with_center", ":center_no", ":relation_town"),
			
			# Reduce player's honor.
			(call_script, "script_change_player_honor", ":honor_loss"),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_NOT_STARTED, ":center_no"),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
# script_qp5_quest_healers_touch
# PURPOSE: Handles all quest specific actions for quest "qp5_healers_touch".
("qp5_quest_healers_touch",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_qp5_healers_touch"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp5_q6_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# QP5_QUEST_INACTIVE                              = 0
		# qp5_ht_begun                                    = 1 # Quest picked up, second visit not had.
		# ## SITUATIONAL BREAK - Bandit's Arrow - Begin
		# qp5_ht_the_bandits_arrow                        = 2 # Elder spoken to companion.  Learn supplies are needed.
		# qp5_ht_returning_with_supplies                  = 3 # Supplies have been acquired from location.
		# qp5_ht_awaiting_results                         = 4 # Supplies have been delivered.  Awaiting results.
		# qp5_ht_arrows_end                               = 5 # Wait period has ended.  Find out if the person recovers.
		# ## SITUATIONAL BREAK - Bandit's Arrow - End
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest parameters.
			(call_script, "script_common_quest_change_state", ":quest_no",            qp5_ht_begun),
			
			#(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     -1),             # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_giver_center,       "$current_town"),             # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_target_center,      "$current_town"),             # Already established.
			#(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 30),             # Based upon the duration of the improvement being built.
			# (quest_set_slot, ":quest_no", slot_quest_object_troop,                    0),             # Holds the name of the companion being used as a healer. (already established)
			# (quest_set_slot, ":quest_no", slot_quest_object_state,                    0),             # Holds the skill type of the companion. (already established)
			# (quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,          0),             # Holds the first name of the sick individual. (already established)
			# (quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,          0),             # Holds the last name of the sick individual. (already established)
			# (quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,          0),             # Holds the gender of the sick individual. (already established)
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  0),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,        ":quest_title"),
			## UNUSED+ ##
			# (quest_set_slot, ":quest_no", slot_quest_temp_slot,                       0),
			# (quest_set_slot, ":quest_no", slot_quest_target_state,                    0),               # Tracks exit stage. (1 = left after supplie delivery, 2 = left after town recovery, 3 = finished entire quest)
			# (quest_set_slot, ":quest_no", slot_quest_target_party,                    0),
			# (quest_set_slot, ":quest_no", slot_quest_primary_commodity,               0),
			# (quest_set_slot, ":quest_no", slot_quest_target_amount,                   0),               # Tracks the % of recovery spent guarding the village.
			# (quest_set_slot, ":quest_no", slot_quest_convince_value,                  0),
			## UNUSED- ##
			
			# Acquire quest variables.
			(quest_get_slot, ":giver_troop", ":quest_no", slot_quest_giver_troop),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_giver_center),
			(quest_get_slot, ":string_first", ":quest_no", slot_quest_stage_1_trigger_chance),
			(quest_get_slot, ":string_last", ":quest_no", slot_quest_stage_2_trigger_chance),
			(quest_get_slot, reg21, ":quest_no", slot_quest_stage_3_trigger_chance), # Gender
			(quest_get_slot, ":troop_surgeon", ":quest_no", slot_quest_object_troop),
			
			# Setup quest text.
			(str_store_party_name_link, s13, ":center_no"),
			(str_store_troop_name, s14, ":giver_troop"),
			(str_store_string, s15, ":string_first"),
			(str_store_string, s16, ":string_last"),
			(str_store_troop_name, s17, ":troop_surgeon"),
			(str_store_string, s61, "@{s14}, village elder of {s13}, has requested the aid of {s17} in tending the illness of a {reg21?woman:man} named {s15} {s16}."),
			# Clear out any old quest notes.
			(str_clear, s1),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 4, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 5, s1, 0),
			(add_quest_note_from_sreg, ":quest_no", 6, s1, 0),
			# Activate the quest.
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", ":giver_troop", "str_qp5_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Name the village (giver)
			(quest_get_slot, ":giver_center", ":quest_no", slot_quest_giver_center),
			(str_store_party_name_link, s11, ":giver_center"),
			# Name the village elder. (giver)
			(store_sub, ":center_offset", ":giver_center", villages_begin),
			(store_add, ":giver_mayor", ":center_offset", "trp_village_1_elder"),
			(str_store_troop_name, s12, ":giver_mayor"),
			# Name our surgeon.
			(quest_get_slot, ":troop_surgeon", ":quest_no", slot_quest_object_troop),
			(str_store_troop_name, s13, ":troop_surgeon"),
			(troop_get_type, reg21, ":troop_surgeon"),
			# Name our victim.
			(quest_get_slot, ":string_first", ":quest_no", slot_quest_stage_1_trigger_chance),
			(quest_get_slot, ":string_last", ":quest_no", slot_quest_stage_2_trigger_chance),
			(quest_get_slot, reg22, ":quest_no", slot_quest_stage_3_trigger_chance), # Gender
			(str_store_string, s14, ":string_first"),
			(str_store_string, s15, ":string_last"),
			
			# Name our destination.
			
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(assign, ":notify_of_update", 1),
			(try_begin),
				(eq, ":quest_stage", qp5_ht_the_bandits_arrow),
				(str_store_string, s65, "@{s13} has informed you that {reg21?she:he} will need herbs from the apothacary in {target town} and as fast as possible or {s14} {s15} won't make it.  {s13} will remain in {s11} to watch {reg22?her:his} condition."),
				(assign, ":note_slot", 3),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64}{s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(try_begin),
				(eq, ":notify_of_update", 1),
				(display_message, "str_quest_log_updated", gpu_light_blue),
			(try_end),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_COMPLETED, ":center_no"), 
			# # Rewards
			# (assign, ":xp_base", 400),        # Experience gain given to the player for getting supplies if they were low.
			# (assign, ":relation_giver", 2),   # Relation boost with the village that sent the aid.
			# (assign, ":relation_target", 1),  # Relation boost with the village that received the aid.
			# (assign, ":relation_lord", 0),    # Relation boost with the village's lord.
			# (assign, ":right_to_rule", 0),    # Change the player's right to rule.
			# (try_begin),
				# (ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				# (val_add, ":relation_giver", 1),
				# (val_add, ":relation_target", 1),
				# (val_add, ":relation_lord", 0),
				# (val_add, ":xp_base", 400),
				# (val_add, ":right_to_rule", 1),
				# (ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				# (val_add, ":relation_giver", 1),
				# (val_add, ":relation_target", 2),
				# (val_add, ":relation_lord", 2),
				# (val_add, ":xp_base", 400),
			# (try_end),
			
			# # Award bonus experience if the player stayed to defend the town.  This is mandatory for high quest reactions.
			# (try_begin),
				# (quest_slot_ge, ":quest_no", slot_quest_target_amount, -1), # Make sure the player spent some time helping the raided village.
				# (quest_get_slot, ":xp_help", ":quest_no", slot_quest_target_amount),
				# (store_mul, ":xp_award", ":xp_base", ":xp_help"),
				# (val_div, ":xp_award", 100),
				# (party_add_xp, "p_main_party", ":xp_award"),
				# (assign, reg21, ":xp_award"),
				# (display_message, "@Bonus experience awarded for helping defend the town. [+{reg21}xp]", gpu_green),
			# (try_end),
			
			# # Award bonus experience if the player escorted the elder back.
			# (try_begin),
				# (quest_slot_eq, ":quest_no", slot_quest_target_state, 3),
				# # Award bonus experience.
				# (store_mul, ":xp_award", ":xp_base", 25),
				# (val_div, ":xp_award", 100),
				# (party_add_xp, "p_main_party", ":xp_award"),
				# (assign, reg21, ":xp_award"),
				# # Name the village elder.
				# (quest_get_slot, ":giver_center", ":quest_no", slot_quest_giver_center),
				# (quest_get_slot, ":target_center", ":quest_no", slot_quest_target_center),
				# (store_sub, ":center_offset", ":target_center", villages_begin),
				# (store_add, ":mayor", ":center_offset", "trp_village_1_elder"),
				# (str_store_troop_name, s21, ":mayor"),
				# (str_store_party_name, s22, ":giver_center"),
				# (display_message, "@Bonus experience awarded for escorting {s21} to {s22}. [+{reg21}xp]", gpu_green),
				
				# # Increase player honor.
				# (call_script, "script_change_player_honor", 2),
				
				# # Change player right to rule.
				# (call_script, "script_change_player_right_to_rule", ":right_to_rule"),
				
			# (try_end),
			
			# # Raise relation with the local town lord.
			# (party_get_slot, ":troop_lord", ":center_no", slot_town_lord),
			# (try_begin),
				# (ge, ":relation_lord", 1),
				# (is_between, ":troop_lord", active_npcs_begin, active_npcs_end),
				# (call_script, "script_change_player_relation_with_troop", ":troop_lord", ":relation_lord", 0),
			# (try_end),
			
			# # Change town reputation.
			# (quest_get_slot, ":center_no", ":quest_no", slot_quest_giver_center),
			# (call_script, "script_change_player_relation_with_center", ":center_no", ":relation_giver"),
			# (quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			# (call_script, "script_change_player_relation_with_center", ":center_no", ":relation_target"),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_WAS_FAILED, ":center_no"),
			# # Rewards
			# (assign, ":relation_town", -2),
			# (assign, ":honor_loss", -1),
			# (try_begin),
				# (ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				# (val_add, ":relation_town", -1),
				# (ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				# (val_add, ":relation_town", -1),
				# (val_add, ":honor_loss", -1),
			# (try_end),
			# # Change town reputation.
			# (quest_get_slot, ":center_no", ":quest_no", slot_quest_giver_center),
			# (call_script, "script_change_player_relation_with_center", ":center_no", ":relation_town"),
			
			# # Reduce player's honor.
			# (call_script, "script_change_player_honor", ":honor_loss"),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence."),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(call_script, "script_qp5_set_quest_status", ":quest_no", QUEST_NOT_STARTED, ":center_no"),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
]

from util_wrappers import *
from util_scripts import *

scripts_directives = [
	# HOOK: Inserts a script that tracks village entry.
	[SD_OP_BLOCK_INSERT, "update_center_recon_notes", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp5_arrive_in_village", ":center_no"),], 1],
	# HOOK: Inserts the initializing scripts in game start as needed.
	[SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_qp5_game_start"),], 1],
	# HOOK: Inserts the names of quests I do not want humanitarian companions to object to failing.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"), 0, 
		[(call_script, "script_cf_qp5_ignore_failures", ":quest_no"),], 1],
	# HOOK: Captures when a player enters town.
	[SD_OP_BLOCK_INSERT, "game_event_party_encounter", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), 0, 
		[(call_script, "script_qp5_track_town_entry", "$g_encountered_party"),], 1],
] # scripts_rename
                
def modmerge_scripts(orig_scripts):
	# process script directives first
	process_script_directives(orig_scripts, scripts_directives)
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