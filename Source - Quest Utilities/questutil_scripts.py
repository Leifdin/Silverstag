# Quest Utilities (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from ID_animations import *
from module_skills import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contains the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [
# script_qus_game_start
# Contains all common initialization scripts needed for Quest Packs.
("qus_game_start",
  [
		# (try_begin),
			# (assign, "$quest_reactions", QUEST_REACTIONS_HIGH),
			# (call_script, "script_qus_give_player_starting_castle"),
			# (troop_add_gold, "trp_player", 20000),
		# (try_end),
	]),

# script_common_start_quest
("common_start_quest",
  [ 
	(store_script_param, ":quest_no", 1),
	(store_script_param, ":giver_troop_no", 2),
	(store_script_param, ":title_string", 3),
	#(quest_set_slot, ":quest_no", slot_quest_giver_troop, ":giver_troop_no"),
	
	(try_begin),
	  (eq, ":giver_troop_no", -1),
	  (str_store_string, s63, ":title_string"),
	(else_try),
	  (is_between, ":giver_troop_no", active_npcs_begin, active_npcs_end),
	  (str_store_troop_name_link, s62, ":giver_troop_no"),
	  (str_store_string, s63, "@Given by: {s62}"),
	(else_try),
	  (str_store_troop_name, s62, ":giver_troop_no"),
	  (str_store_string, s63, "@Given by: {s62}"),
	(try_end),
	(store_current_hours, ":cur_hours"),
	(str_store_date, s60, ":cur_hours"),
	(str_store_string, s60, "@Given on: {s60}"),
	(add_quest_note_from_sreg, ":quest_no", 0, s60, 0),
	(add_quest_note_from_sreg, ":quest_no", 1, s63, 0),
	(add_quest_note_from_sreg, ":quest_no", 2, s61, 0),
	
	(try_begin),
	  (quest_slot_ge, ":quest_no", slot_quest_expiration_days, 1),
	  (quest_get_slot, reg20, ":quest_no", slot_quest_expiration_days),
	  (add_quest_note_from_sreg, ":quest_no", 7, "@You have {reg20} days to finish this quest.", 0),
	(try_end),
	
	(start_quest, ":quest_no", ":giver_troop_no"),
	
	(display_message, "str_quest_log_updated"),
	]),
	
# script_common_quest_change_slot
("common_quest_change_slot",
	[ 
		(store_script_param, ":quest_no", 1),
		(store_script_param, ":quest_slot", 2),
		(store_script_param, ":amount", 3),
		
		(quest_get_slot, ":value", ":quest_no", ":quest_slot"),
		(val_add, ":value", ":amount"),
		(quest_set_slot, ":quest_no", ":quest_slot", ":value"),
		
		(try_begin),
			(ge, DEBUG_QUEST_UTILITIES, 1), # Diagnostic
			(assign, reg31, ":amount"),
			(quest_get_slot, ":title_string", ":quest_no", slot_quest_unique_name),
			(str_store_string, s31, ":title_string"),
			(assign, reg32, ":quest_slot"),
			(assign, reg33, ":value"),
			(display_message, "@DEBUG (Quest Util): Quest [ {s31} ], Slot #{reg32} changed by {reg31} to {reg33}.", gpu_debug),
		(try_end),
	]),
	
# script_cf_common_quest_intimidation_check
# Given a set DC attempts to make an intimidation check by one troop against another.  Script fails if the check fails.
# EXAMPLE: (call_script, "script_cf_common_quest_intimidation_check", ":intimidation_troop", ":victim_troop", DC), # questutil_scripts.py (See questutil_constants for 3rd arg constants)
("cf_common_quest_intimidation_check",
    [
	    (store_script_param, ":intimidation_troop", 1),
		(store_script_param, ":victim_troop", 2),
		(store_script_param, ":difficulty", 3),
		
		# Get information about intimidating_troop.
		(store_attribute_level, ":int_strength", ":intimidation_troop", ca_strength),
		(store_attribute_level, ":int_charisma", ":intimidation_troop", ca_charisma),
		(troop_get_slot, ":int_renown", ":intimidation_troop", slot_troop_renown),
		(store_character_level, ":int_level", ":intimidation_troop"),
		
		# Get information about victim_troop.
		(store_attribute_level, ":vict_strength", ":victim_troop", ca_strength),
		(store_attribute_level, ":vict_charisma", ":victim_troop", ca_charisma),
		(troop_get_slot, ":vict_renown", ":victim_troop", slot_troop_renown),
		(store_character_level, ":vict_level", ":victim_troop"),
		
		(assign, ":success_threshold", 0),
		# Compare:
		#  - Renown
		(store_sub, ":renown_value", ":int_renown", ":vict_renown"),
		(val_div, ":renown_value", 50),
		(val_clamp, ":renown_value", -20, 21),
		(val_add, ":success_threshold", ":renown_value"),
		
		#  - Strength
		(store_sub, ":strength_value", ":int_strength", ":vict_strength"),
		(val_mul, ":strength_value", 2),
		(val_clamp, ":strength_value", -20, 21),
		(val_add, ":success_threshold", ":strength_value"),
		
		#  - Charisma
		(store_sub, ":charisma_value", ":int_charisma", ":vict_charisma"),
		(val_mul, ":charisma_value", 2),
		(val_clamp, ":charisma_value", -20, 21),
		(val_add, ":success_threshold", ":charisma_value"),
		
		#  - Level
		(store_sub, ":level_value", ":int_level", ":vict_level"),
		(val_mul, ":level_value", 2),
		(val_clamp, ":level_value", -20, 21),
		(val_add, ":success_threshold", ":level_value"),
		
		#  - Relation
		(call_script, "script_troop_get_relation_with_troop", ":intimidation_troop", ":victim_troop"),
		(assign, ":relation_value", reg0),
		(val_clamp, ":relation_value", -20, 21),
		(val_add, ":success_threshold", ":relation_value"),
		
		#  - Factor DC in.
		(val_add, ":success_threshold", ":difficulty"),
		
		#  - Factor personality of victim.  Some lords are just plain stubborn.
		(try_begin),
			(assign, ":reputation_value", 0),
			(this_or_next|troop_slot_eq, ":victim_troop", slot_lord_reputation_type, lrep_martial),
			(troop_slot_eq, ":victim_troop", slot_lord_reputation_type, lrep_quarrelsome),
			(assign, ":reputation_value", -5),
			(val_add, ":success_threshold", ":reputation_value"),
		(try_end),
		
		#  - Kings do not allow themselves to be bullied unless it is by another king.  Kings are more intimidating in general.
		(assign, ":king_value", 0),
		(try_begin),
			(assign, ":intimidator_is_king", 0),
			(assign, ":victim_is_king", 0),
			(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
				(faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
				(try_begin),
					(faction_slot_eq, ":kingdom_no", slot_faction_leader, ":intimidation_troop"),
					(assign, ":intimidator_is_king", 1),
				(try_end),
				(try_begin),
					(faction_slot_eq, ":kingdom_no", slot_faction_leader, ":victim_troop"),
					(assign, ":victim_is_king", 1),
				(try_end),
			(try_end),
			(try_begin),
				(eq, ":intimidator_is_king", 1),
				(eq, ":victim_is_king", 0),
				(assign, ":king_value", 30),
			(else_try),
				(eq, ":intimidator_is_king", 0),
				(eq, ":victim_is_king", 1),
				(assign, ":king_value", -75),
			(try_end),
			(val_add, ":success_threshold", ":king_value"),
		(try_end),
		
		(val_clamp, ":success_threshold", 0, 95), # Always inserts a 4% chance of failure.
		(store_random_in_range, ":intimidation_check", 0, 100),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(str_store_troop_name, s31, ":intimidation_troop"),
			(str_store_troop_name, s32, ":victim_troop"),
			(assign, reg30, ":difficulty"),
			(assign, reg31, ":intimidation_check"),
			(assign, reg32, ":success_threshold"),
			(assign, reg33, ":renown_value"), # renown
			(assign, reg34, ":strength_value"), # strength
			(assign, reg35, ":charisma_value"), # charisma
			(assign, reg36, ":level_value"), # level
			(assign, reg37, ":relation_value"), # relation
			(assign, reg38, ":reputation_value"), # reputation
			(assign, reg39, ":king_value"), # King
			# Conditional Failure
			(neg|le, ":intimidation_check", ":success_threshold"),
			(display_message, "@DEBUG (Quest Util): {s31} fails to intimidate {s32}.  {reg31} vs {reg32}.  Condition failed.", gpu_debug),
			(ge, DEBUG_QUEST_CONDITIONS, 2),
			(display_message, "@Difficulty {reg32} = DC {reg30} + Renown {reg33} + STR {reg34} + CHA {reg35} + Level {reg36} + Relation {reg37} + Rep {reg38} + King {reg39}.", gpu_debug),
		(try_end),
		
		(le, ":intimidation_check", ":success_threshold"), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(display_message, "@DEBUG (Quest Util): {s31} intimidated {s32}.  {reg31} vs {reg32}.  Condition passed.", gpu_debug),
			(ge, DEBUG_QUEST_CONDITIONS, 2),
			(display_message, "@Difficulty {reg32} = DC {reg30} + Renown {reg33} + STR {reg34} + CHA {reg35} + Level {reg36} + Relation {reg37} + Rep {reg38} + King {reg39}.", gpu_debug),
		(try_end),
    ]),
	
# script_cf_common_quest_persuasion_check
# Given a set DC attempts to make a persuasion check by one troop against another.  Script fails if the check fails.
# EXAMPLE: (call_script, "script_cf_common_quest_persuasion_check", ":persuading_troop", ":victim_troop", DC), # questutil_scripts.py (See questutil_constants for 3rd arg constants)
("cf_common_quest_persuasion_check",
    [
	    (store_script_param, ":persuading_troop", 1),
		(store_script_param, ":victim_troop", 2),
		(store_script_param, ":difficulty", 3),
		
		# Get information about intimidating_troop.
		(store_skill_level, ":int_persuasion", "skl_persuasion", ":persuading_troop"),
		(store_attribute_level, ":int_charisma", ":persuading_troop", ca_charisma),
		
		# Get information about victim_troop.
		(store_skill_level, ":vict_persuasion", "skl_persuasion", ":victim_troop"),
		(store_attribute_level, ":vict_charisma", ":victim_troop", ca_charisma),
		
		(assign, ":success_threshold", 0),
		# Compare:
		#  - Persuasion
		(store_sub, ":persuasion_value", ":int_persuasion", ":vict_persuasion"),
		(val_mul, ":persuasion_value", 4),
		(val_clamp, ":persuasion_value", -40, 41),
		(val_add, ":success_threshold", ":persuasion_value"),
		
		#  - Silver Tongued
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":persuading_troop", BONUS_SILVER_TONGUED), # combat_scripts.py - ability constants in combat_constants.py
			(val_add, ":persuasion_value", 25),
		(try_end),
		
		#  - Charisma
		(store_sub, ":charisma_value", ":int_charisma", ":vict_charisma"),
		(val_mul, ":charisma_value", 2),
		(val_clamp, ":charisma_value", -25, 26),
		(val_add, ":success_threshold", ":charisma_value"),
		
		#  - Relation
		(call_script, "script_troop_get_relation_with_troop", ":persuading_troop", ":victim_troop"),
		(assign, ":relation_value", reg0),
		(val_clamp, ":relation_value", -40, 41),
		(val_add, ":success_threshold", ":relation_value"),
		
		#  - Factor DC in.
		(val_add, ":success_threshold", ":difficulty"),
		
		#  - Factor personality of victim.  Some lords are just plain stubborn.
		(try_begin),
			(assign, ":reputation_value", 0),
			(this_or_next|troop_slot_eq, ":victim_troop", slot_lord_reputation_type, lrep_selfrighteous),
			(troop_slot_eq, ":victim_troop", slot_lord_reputation_type, lrep_quarrelsome),
			(assign, ":reputation_value", -5),
			(val_add, ":success_threshold", ":reputation_value"),
		(try_end),
		
		(val_clamp, ":success_threshold", 0, 95), # Always inserts a 4% chance of failure.
		(store_random_in_range, ":persuasion_check", 0, 100),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(str_store_troop_name, s31, ":persuading_troop"),
			(str_store_troop_name, s32, ":victim_troop"),
			(assign, reg30, ":difficulty"),
			(assign, reg31, ":persuasion_check"),
			(assign, reg32, ":success_threshold"),
			(assign, reg33, ":persuasion_value"), # persuasion
			(assign, reg35, ":charisma_value"), # charisma
			(assign, reg37, ":relation_value"), # relation
			(assign, reg38, ":reputation_value"), # reputation
			# Conditional Failure
			(gt, ":persuasion_check", ":success_threshold"),
			(display_message, "@DEBUG (Quest Util): {s31} fails to persuade {s32}.  {reg31} vs {reg32}.  Condition failed.", gpu_debug),
			(ge, DEBUG_QUEST_CONDITIONS, 2),
			(display_message, "@Difficulty {reg32} = DC {reg30} + Persuasion {reg33} + CHA {reg35} + Relation {reg37} + Rep {reg38}.", gpu_debug),
		(try_end),
		
		(le, ":persuasion_check", ":success_threshold"), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(display_message, "@DEBUG (Quest Util): {s31} persuaded {s32}.  {reg31} vs {reg32}.  Condition passed.", gpu_debug),
			(ge, DEBUG_QUEST_CONDITIONS, 2),
			(display_message, "@Difficulty {reg32} = DC {reg30} + Persuasion {reg33} + CHA {reg35} + Relation {reg37} + Rep {reg38}.", gpu_debug),
		(try_end),
    ]),
	
# script_qus_give_player_starting_castle
# Automatically gives the player a castle "sunspire keep" based upon starting faction.  For testing purposes.
# INPUT:  none
# OUTPUT: none
# ("qus_give_player_starting_castle",
  # [
		# # Adds character to faction of choice.
		# (try_begin),
			# (eq, "$background_answer_2", start_fac_swadia),
			# (assign, ":faction_initial", "fac_kingdom_1"),
			# (assign, ":center_initial", "p_castle_23"), # Tevarin Castle
		# (else_try),
			# (eq, "$background_answer_2", start_fac_nords),
			# (assign, ":faction_initial", "fac_kingdom_4"),
			# (assign, ":center_initial", "p_castle_12"), # Chalbek Castle
		# (else_try),
			# (eq, "$background_answer_2", start_fac_rhodoks),
			# (assign, ":faction_initial", "fac_kingdom_5"),
			# (assign, ":center_initial", "p_castle_21"), # Ibdeles Castle
		# (else_try),
			# (eq, "$background_answer_2", start_fac_khergits),
			# (assign, ":faction_initial", "fac_kingdom_3"),
			# (assign, ":center_initial", "p_castle_17"), # Distar Castle
		# (else_try),
			# (eq, "$background_answer_2", start_fac_sarrind),
			# (assign, ":faction_initial", "fac_kingdom_6"),
			# (assign, ":center_initial", "p_castle_44"), # Durrin Castle
		# (else_try),
			# (eq, "$background_answer_2", start_fac_vaegirs),
			# (assign, ":faction_initial", "fac_kingdom_2"),
			# (assign, ":center_initial", "p_castle_19"), # Yruma Castle
		# (else_try),
			# (assign, ":faction_initial", "fac_kingdom_1"),
			# (assign, ":center_initial", "p_castle_23"), # Yruma Castle
		# (try_end),
		# (call_script, "script_player_join_faction", ":faction_initial"),
		# (assign, "$player_has_homage" ,1),
		# (troop_set_faction, "trp_player", ":faction_initial"),
		# (assign, "$g_player_banner_granted", 1),
		# (assign, "$g_invite_faction", 0),
		# (assign, "$g_invite_faction_lord", 0),
		# (assign, "$g_invite_offered_center", 0),
		# (party_relocate_near_party, "p_main_party", ":center_initial", 0.5), # Moves you to your new castle.
		# (party_set_name, ":center_initial", "@Sunspire Keep"),
		# (call_script, "script_give_center_to_lord", ":center_initial", "trp_player", 0), # Gives you control of a castle.
	# ]),
	
# script_common_prisoner_caravan_function
# Handles all scripts specific to the AI for prisoner caravans.
# INPUT: none
# OUTPUT: none
("common_prisoner_caravan_function",
    [
		(store_script_param, ":function", 1),
		(store_script_param, ":caravan", 2),
		(store_script_param, ":center_no", 3),
		
		(try_begin),
			(eq, ":function", prisoner_caravan_create),
			##### CREATE PARTY #####
			# Define tier 1-5 troops for initializing city center.
			# Determine faction flavor
			(store_faction_of_party, ":faction_no", ":center_no"),
			(faction_get_slot, ":culture", ":faction_no", slot_faction_culture),
			(faction_get_slot, ":tier_1", ":culture",  slot_faction_tier_1_troop),
			(faction_get_slot, ":tier_2", ":culture",  slot_faction_tier_2_troop),
			(faction_get_slot, ":tier_3", ":culture",  slot_faction_tier_3_troop),
			(faction_get_slot, ":tier_4", ":culture",  slot_faction_tier_4_troop),
			# Count prisoners
			(party_get_num_prisoners, ":prisoner_count", ":center_no"),
			(val_max, ":prisoner_count", 1), # Prevent DIV/0 errors.
			# Determine number of guards.
			(store_div, ":guard_count", ":prisoner_count", 4),
			(val_max, ":guard_count", 10), # Ensure a minimum of 10 guards.
			# Create the party
			(set_spawn_radius, 1),
			(spawn_around_party, ":center_no", "pt_patrol_party"),
			(assign, ":caravan", reg0),
			# Add troop leader
			(party_add_leader, ":caravan", ":tier_4"),
			(store_sub, ":troops_left", ":guard_count", 1),
			(try_begin),
				# Add TIER 1 members
				(ge, ":troops_left", 1),
				(store_mul, ":tier_1_troops", ":troops_left", 60),
				(val_div, ":tier_1_troops", 100),
				(party_add_members, ":caravan", ":tier_1", ":tier_1_troops"),
				(val_sub, ":troops_left", ":tier_1_troops"),
				# Add TIER 2 members
				(ge, ":troops_left", 1),
				(store_mul, ":tier_2_troops", ":troops_left", 60),
				(val_div, ":tier_2_troops", 100),
				(party_add_members, ":caravan", ":tier_2", ":tier_2_troops"),
				(val_sub, ":troops_left", ":tier_2_troops"),
				# Add TIER 3 members (anything left)
				(ge, ":troops_left", 1),
				(party_add_members, ":caravan", ":tier_3", ":troops_left"),
			(try_end),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(party_set_faction, ":caravan", ":faction_no"),
			# Name the caravan.
			(str_store_party_name, s13, ":center_no"),
			(party_set_name, ":caravan", "@Prisoner Caravan from {s13}"),
			# Output variables.
			(party_set_slot, ":caravan", slot_party_caravan_origin, ":center_no"),
			(party_set_slot, ":caravan", slot_party_wealth, 0),
			(party_set_slot, ":caravan", slot_party_caravan_escort_price, 0),
			(assign, reg51, ":caravan"),
			
		(else_try),
			(eq, ":function", prisoner_caravan_load_from_center),
			##### LOAD FROM CENTER #####
			(call_script, "script_party_prisoners_add_party_prisoners", ":caravan", ":center_no"),  # Move prisoners from center to caravan.
			(call_script, "script_party_remove_all_prisoners", ":center_no"),
			
		(else_try),
			(eq, ":function", prisoner_caravan_unload_to_center_for_free),
			##### UNLOAD TO CENTER FOR FREE #####
			(call_script, "script_party_prisoners_add_party_prisoners", ":center_no", ":caravan"),  # Move prisoners from caravan to center.
			(call_script, "script_party_remove_all_prisoners", ":caravan"),
			
		(else_try),
			(eq, ":function", prisoner_caravan_unload_to_center_for_pay),
			##### UNLOAD TO CENTER FOR PAY #####
			(party_get_num_prisoners, ":prisoner_count", ":caravan"),
			(party_get_num_prisoner_stacks, ":stack_limit", ":caravan"),
			(try_begin),
				(ge, ":stack_limit", 1), # They need to have something worth selling.
				(assign, ":earnings", 0),
				(try_for_range, ":stack_no", 0, ":stack_limit"),
					(party_prisoner_stack_get_troop_id, ":troop_no", ":caravan", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"), # Prevent companions, lords & player from being taken.
					(party_prisoner_stack_get_size, ":troop_count", ":caravan", ":stack_no"),
					# (assign, "$g_talk_troop", "trp_ramun_the_slave_trader"), # Prevent prices being abnormally low.
					(call_script, "script_game_get_prisoner_price", ":troop_no"),
					(assign, ":troop_value", reg0),
					(store_mul, ":stack_value", ":troop_value", ":troop_count"),
					(val_add, ":earnings", ":stack_value"),
				(try_end),
				(assign, "$g_move_heroes", 0),
				(call_script, "script_party_prisoners_add_party_prisoners", ":center_no", ":caravan"),  # Move prisoners from caravan to center.
				(call_script, "script_party_remove_all_prisoners", ":caravan"),
				(party_get_slot, ":wealth", ":caravan", slot_party_wealth),
				(val_add, ":wealth", ":earnings"),
				(party_set_slot, ":caravan", slot_party_wealth, ":wealth"),
				(try_begin),
					(ge, DEBUG_QUEST_AI, 2),
					(str_store_party_name, s31, ":caravan"),
					(str_store_party_name, s32, ":center_no"),
					(assign, reg31, ":earnings"),
					(assign, reg32, ":prisoner_count"),
					(display_message, "@DEBUG (Caravan AI): {s31} offloads {reg32} prisoners in {s32} for {reg31} denars.", gpu_debug),
				(try_end),
			(try_end),
			
		(else_try),
			(eq, ":function", prisoner_caravan_offload_wealth_and_remove),
			##### OFFLOAD WEALTH AND REMOVE PARTY #####
			(party_get_slot, ":earnings", ":caravan", slot_party_wealth),
			(party_get_slot, ":treasury", ":center_no", slot_party_wealth),
			(party_get_slot, ":escort_fee", ":caravan", slot_party_caravan_escort_price),
			(val_add, ":treasury", ":earnings"),
			(val_sub, ":treasury", ":escort_fee"),
			(party_set_slot, ":center_no", slot_party_wealth, ":treasury"),
			(party_set_slot, ":caravan", slot_party_wealth, 0),
			(try_begin),
				(ge, DEBUG_QUEST_AI, 2),
				(str_store_party_name, s31, ":caravan"),
				(str_store_party_name, s32, ":center_no"),
				(assign, reg31, ":earnings"),
				(assign, reg32, ":treasury"),
				(assign, reg33, ":escort_fee"),
				(display_message, "@DEBUG (Caravan AI): {s31} arrived in {s32} and increased treasury to {reg32} denars [+{reg31} earnings, -{reg33} escort fee].", gpu_debug),
			(try_end),
			(remove_party, ":caravan"),
			
		(else_try),
			(eq, ":function", prisoner_caravan_direct_to_destination),
			##### DIRECT TO DESTINATION #####
			(party_set_slot, ":caravan", slot_party_caravan_destination, ":center_no"),
			(party_set_ai_object, ":caravan", ":center_no"),
			(party_set_ai_behavior, ":caravan", ai_bhvr_travel_to_party),
			(party_set_slot, ":caravan", slot_party_ai_state, spai_retreating_to_center),
			(party_set_slot, ":caravan", slot_party_type, spt_prisoner_train),
			(party_set_bandit_attraction, ":caravan", 100),
			(try_begin),
				(ge, DEBUG_QUEST_AI, 2),
				(str_store_party_name, s31, ":caravan"),
				(str_store_party_name, s32, ":center_no"),
				# (party_get_slot, ":current_center", ":caravan", slot_party_caravan_origin),
				# (str_store_party_name, s33, ":current_center"),
				(party_get_slot, reg31, ":caravan", slot_party_wealth),
				(party_get_num_prisoners, reg32, ":caravan"),
				(display_message, "@DEBUG (Caravan AI): {s31} has departed on route to {s32} with {reg32} prisoners and {reg31} denars.", gpu_debug),
			(try_end),
			
		(else_try),
			(eq, ":function", prisoner_caravan_return_to_origin),
			##### DIRECT TO DESTINATION #####
			(party_get_cur_town, ":current_center", ":caravan"),
			(try_begin),
				(ge, ":current_center", 0),
				(party_detach, ":caravan"),
			(else_try),
				(party_get_slot, ":current_center", ":caravan", slot_party_caravan_origin),
			(try_end),
			(party_set_ai_object, ":caravan", ":center_no"),
			(party_set_ai_behavior, ":caravan", ai_bhvr_travel_to_party),
			(party_set_slot, ":caravan", slot_party_ai_state, spai_retreating_to_center),
			(party_set_slot, ":caravan", slot_party_type, spt_prisoner_train),
			(party_set_bandit_attraction, ":caravan", 40),
			(try_begin),
				(ge, DEBUG_QUEST_AI, 2),
				(str_store_party_name, s31, ":caravan"),
				(str_store_party_name, s32, ":center_no"),
				(str_store_party_name, s33, ":current_center"),
				(party_get_slot, reg31, ":caravan", slot_party_wealth),
				(party_get_num_prisoners, reg32, ":caravan"),
				(display_message, "@DEBUG (Caravan AI): {s31} is leaving {s33} to go to {s32} with {reg32} prisoners and {reg31} denars.", gpu_debug),
			(try_end),
			
		(else_try),
			(eq, ":function", prisoner_caravan_generate_escort_cost),
			##### GENERATE ESCORT COST ##### - Stores cost in reg51
			(party_get_num_prisoners, ":prisoner_count", ":center_no"),
			(party_get_num_prisoner_stacks, ":stack_limit", ":center_no"),
			(assign, ":payment", 0),
			(try_begin),
				(ge, ":stack_limit", 1), # They need to have something worth selling.
				(try_for_range, ":stack_no", 0, ":stack_limit"),
					(party_prisoner_stack_get_troop_id, ":troop_no", ":center_no", ":stack_no"),
					(neg|troop_is_hero, ":troop_no"), # Prevent companions, lords & player from being taken.
					(party_prisoner_stack_get_size, ":troop_count", ":center_no", ":stack_no"),
					(call_script, "script_game_get_prisoner_price", ":troop_no"),
					(assign, ":troop_value", reg0),
					(store_mul, ":stack_value", ":troop_value", ":troop_count"),
					(val_add, ":payment", ":stack_value"),
				(try_end),
			(try_end),
			(val_mul, ":payment", 35),
			(val_div, ":payment", 100),
			(assign, reg51, ":payment"),
			
		(else_try),
			(eq, ":function", prisoner_caravan_add_escort_troops),
			##### ADD ESCORT TROOPS ##### - Expects cost input as center_no
			(assign, ":payment", ":center_no"),
			(call_script, "script_game_get_prisoner_price", ":tier_1"),
			(store_mul, ":tier_1_value", 5, reg0),
			(call_script, "script_game_get_prisoner_price", ":tier_2"),
			(store_mul, ":tier_2_value", 2, reg0),
			(call_script, "script_game_get_prisoner_price", ":tier_3"),
			(store_mul, ":tier_3_value", 1, reg0),
			(assign, ":reinforcement_cost", ":tier_1_value"),
			(val_add, ":reinforcement_cost", ":tier_2_value"),
			(val_add, ":reinforcement_cost", ":tier_3_value"),
			(try_for_range, ":unused", 0, 10),
				(ge, ":payment", ":reinforcement_cost"),
				(party_add_members, ":caravan", ":tier_1", 5),
				(party_add_members, ":caravan", ":tier_2", 2),
				(party_add_members, ":caravan", ":tier_3", 1),
				(val_sub, ":payment", ":reinforcement_cost"),
			(try_end),
			(store_sub, ":cost", ":center_no", ":payment"),
			(party_set_slot, ":caravan", slot_party_caravan_escort_price, ":cost"),
			(try_begin), (ge, DEBUG_QUEST_AI, 3), (assign, reg31, ":cost"), (display_message, "@DEBUG (Caravan AI): Escort troops added based upon 35% of contract price. [{reg31} denars]", gpu_debug), (try_end),
			
		(else_try),
			(eq, ":function", prisoner_caravan_raided_by_troop),
			##### RAIDED BY TROOP ##### - Expects valid troop in center_no slot.
			(assign, ":troop_no", ":center_no"),
			(try_begin),
				(party_get_slot, ":caravan_wealth", ":caravan", slot_party_wealth),
				(ge, ":caravan_wealth", 1),
				(party_set_slot, ":caravan", slot_party_wealth, 0),
				(try_begin),
					(eq, ":troop_no", "trp_player"),
					(call_script, "script_troop_add_gold", "trp_player", ":caravan_wealth"),
					(assign, reg21, ":caravan_wealth"),
					(display_message, "@You have looted {reg21} denars from a prisoner caravan!"),
				(else_try),
					(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
					(troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),
					(val_add, ":troop_wealth", ":caravan_wealth"),
					(troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
					(ge, DEBUG_QUEST_AI, 1),
					(assign, reg31, ":caravan_wealth"),
					(assign, reg32, ":troop_wealth"),
					(str_store_troop_name, s31, ":troop_no"),
					(display_message, "@DEBUG (Caravan AI): {s31} has raided a prisoner caravan worth {reg31} denars.  He now has {reg32} denars.", gpu_debug),
				(try_end),
			(try_end),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "@ERROR: script_common_prisoner_caravan_function failed on function #{reg31}.", qp_error_color),
		(try_end),
    ]),
	
# script_qus_exit_to_map
# Exits to the map from any dynamically generated menu.
# Input: none
# Output: none
("qus_exit_to_map",
    [
		#(store_script_param, ":menu_no", 1),
		#(store_script_param, ":troop_no", 2),
		
		(change_screen_map),
	]),
	
# script_qus_select_random_center
# PURPOSE: Picks a random center based upon center type that is within a given distance from an input central location.
# EXAMPLE: (call_script, "script_qus_select_random_center", center_is_any, min, max, ":epicenter"),
("qus_select_random_center",
  [
		(store_script_param, ":type",         1),
		(store_script_param, ":min_distance", 2),
		(store_script_param, ":max_distance", 3),
		(store_script_param, ":epicenter",    4),
		
		# center_is_any                                   = 0
		# center_is_village                               = 1
		# center_is_town                                  = 2
		# center_is_castle                                = 3
		# center_is_any_friendly                          = 4
		# center_is_village_friendly                      = 5
		# center_is_town_friendly                         = 6
		# center_is_castle_friendly                       = 7
		
		(try_begin),
			(this_or_next|eq, ":type", center_is_village_friendly),
			(eq, ":type", center_is_village),
			(assign, ":center_start", villages_begin),
			(assign, ":center_end", villages_end),
			(str_store_string, s22, "@village"),
		(else_try),
			(this_or_next|eq, ":type", center_is_town_friendly),
			(eq, ":type", center_is_town),
			(assign, ":center_start", towns_begin),
			(assign, ":center_end", towns_end),
			(str_store_string, s22, "@town"),
		(else_try),
			(this_or_next|eq, ":type", center_is_castle_friendly),
			(eq, ":type", center_is_castle),
			(assign, ":center_start", castles_begin),
			(assign, ":center_end", castles_end),
			(str_store_string, s22, "@castle"),
		(else_try),
			(this_or_next|eq, ":type", center_is_any_friendly),
			(eq, ":type", center_is_any),
			(assign, ":center_start", centers_begin),
			(assign, ":center_end", centers_end),
			(str_store_string, s22, "@center"),
		(else_try),
			# Default Error
			(display_message, "@ERROR - No valid center type specified for script 'qus_select_random_center'."),
			(assign, ":center_start", centers_begin),
			(assign, ":center_end", centers_end),
			(str_store_string, s22, "@ERROR"),
		(try_end),
		
		(assign, ":center_picked", -1),
		
		(assign, ":records", 0),
		(assign, ":array", "trp_temp_array_a"),
		(try_for_range, ":center_no", ":center_start", ":center_end"),
			(store_distance_to_party_from_party, ":distance", ":epicenter", ":center_no"),
			(neq, ":center_no", ":epicenter"),
			(ge, ":distance", ":min_distance"),
			(le, ":distance", ":max_distance"),
			# Filter if friendly or not.
			(assign, ":pass", 1),
			(try_begin),
				(this_or_next|eq, ":type", center_is_any_friendly),
				(this_or_next|eq, ":type", center_is_village_friendly),
				(this_or_next|eq, ":type", center_is_castle_friendly),
				(eq, ":type", center_is_town_friendly),
				(assign, ":pass", 0),
				(store_faction_of_party, ":faction_no", ":center_no"),
				(store_relation, ":faction_relation", ":faction_no", "$players_kingdom"),
				(ge, ":faction_relation", 0),
				(assign, ":pass", 1),
			(try_end),
			(eq, ":pass", 1),
			(troop_set_slot, ":array", ":records", ":center_no"),
			(val_add, ":records", 1),
		(try_end),
		
		(try_begin),
			(ge, ":records", 1),
			(store_random_in_range, ":slot_no", 0, ":records"),
			(troop_get_slot, ":center_picked", ":array", ":slot_no"),
		(else_try),
			(store_random_in_range, ":center_picked", ":center_start", ":center_end"),
		(try_end),
		
		(try_begin),
			(ge, DEBUG_QUEST_UTILITIES, 1),
			(str_store_party_name, s31, ":center_picked"),
			(display_message, "@DEBUG (Quest Util): {s31} chosen as target center.", gpu_green),
			(display_message, "@DEBUG (Quest Util): Additional centers available for this choice:", gpu_debug),
			(try_for_range, ":slot_no", 0, ":records"),
				(troop_get_slot, ":center_check", ":array", ":slot_no"),
				(store_distance_to_party_from_party, reg31, ":epicenter", ":center_check"),
				(assign, reg32, ":slot_no"),
				(str_store_party_name, s31, ":center_check"),
				(display_message, "@DEBUG (Quest Util): #{reg32} - {s31} at a distance of {reg31}.", gpu_debug),
			(try_end),
		(try_end),
		
		(assign, reg1, ":center_picked"),
	]),
	
# script_common_quest_change_state
# PURPOSE: Common utility script used to change the current stage of a quest, force a reset of any dialog comments that 
# may be relevant and report back that action being taken if desired.
("common_quest_change_state",
  [
		(store_script_param, ":quest_no", 1),
		(store_script_param, ":new_stage", 2),
		
		(quest_set_slot, ":quest_no", slot_quest_current_state, ":new_stage"),
		(quest_set_slot, ":quest_no", slot_quest_comment_made, 0),
		
		(try_begin),
			(ge, DEBUG_QUEST_UTILITIES, 1),
			(quest_get_slot, ":quest_title", ":quest_no", slot_quest_unique_name),
			(str_store_string, s41, ":quest_title"),
			(assign, reg31, ":new_stage"),
			(display_message, "@DEBUG (Quest Util): Quest '{s41}' current state changed to {reg31}.", gpu_debug),
		(try_end),
	]),
	
# script_cf_qus_player_owns_walled_center
# PURPOSE: Checks if the player owns a walled center for use in determine court based quests.  Returns random walled center via reg1.
# EXAMPLE: (call_script, "script_cf_qus_player_owns_walled_center"), # questutil_scripts.py  - Returns center via reg1.
("cf_qus_player_owns_walled_center",
    [
	    (assign, ":fiefs_owned", 0),
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":fiefs_owned", 1),
		(try_end),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(eq, ":fiefs_owned", 0),
			(display_message, "@DEBUG (Quest Util): Player does not own any walled centers.  Condition failed.", gpu_debug),
		(try_end),
		
		(ge, ":fiefs_owned", 1), # Conditional Failure
		
		(store_random_in_range, ":offset", 0, ":fiefs_owned"),
		(store_sub, ":target_center", ":fiefs_owned", ":offset"),
		(assign, ":fiefs_owned", 0),
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":fiefs_owned", 1),
			(eq, ":fiefs_owned", ":target_center"),
			(assign, reg1, ":center_no"),
		(try_end),
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(str_store_party_name, s31, reg1),
			(display_message, "@DEBUG (Quest Util): Player does own a walled center [ {s31} ].  Condition passed.", gpu_debug),
		(try_end),
    ]),
	
# script_cf_qus_player_is_king
# Checks if the player is a king, matches it against whether you wanted him to be king or not and fails (as a conditional script) if he doesn't match desired status.
# Input: arg1 (True-1/False-0)
# Output: none
("cf_qus_player_is_king",
    [
	    (store_script_param, ":king_status_desired", 1),
		(assign, ":fiefs_owned", 0),
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(val_add, ":fiefs_owned", 1),
		(try_end),
		(try_begin),
			(ge, ":fiefs_owned", 1),
			(eq, "$players_kingdom", "fac_player_supporters_faction"),
			(assign, ":king_status", 1),
		(else_try),
			(assign, ":king_status", 0),
		(try_end),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(neq, ":king_status", ":king_status_desired"),
			(assign, reg31, ":king_status"),
			(assign, reg32, ":king_status_desired"),
			(display_message, "@DEBUG (Quest Util): Player {reg32?SHOULD be:shouldn NOT be} and {reg31?IS:is NOT} a king.  Condition failed.", gpu_debug),
		(try_end),
		
		(eq, ":king_status", ":king_status_desired"), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(assign, reg31, ":king_status"),
			(assign, reg32, ":king_status_desired"),
			(display_message, "@DEBUG (Quest Util): Player {reg32?SHOULD be:shouldn NOT be} and {reg31?IS:is NOT} a king.  Condition passed.", gpu_debug),
		(try_end),
    ]),

# script_cf_qus_player_is_vassal
# Checks if the player is a vassal, matches it against whether you wanted him to be king or not and fails (as a conditional script) if he doesn't match desired status.
# Input: arg1 (True-1/False-0)
# Output: none
("cf_qus_player_is_vassal",
    [
	    (store_script_param, ":vassal_status_desired", 1),
		
		(try_begin),
			(gt, "$players_kingdom", 0),
			(neq, "$players_kingdom", "fac_player_supporters_faction"),
			(neq, "$players_kingdom", "fac_player_faction"),
			(eq, "$player_has_homage", 1),
			
			# # Make sure we are not our own faction or unaffiliated.
			# (neq, "$players_kingdom", "fac_player_supporters_faction"),
			# # Make sure we're not a mercenary.
			# (store_current_day, ":current_day"),
			# (neg|gt, ":current_day", "$mercenary_service_next_renew_day"),
			(assign, ":vassal_status", 1),
		(else_try),
			(assign, ":vassal_status", 0),
		(try_end),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(neq, ":vassal_status", ":vassal_status_desired"),
			(assign, reg31, ":vassal_status"),
			(assign, reg32, ":vassal_status_desired"),
			(display_message, "@DEBUG (Quest Util): Player {reg32?SHOULD be:shouldn NOT be} and {reg31?IS:is NOT} a vassal.  Condition failed.", gpu_debug),
		(try_end),
		
		(eq, ":vassal_status", ":vassal_status_desired"), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(assign, reg31, ":vassal_status"),
			(assign, reg32, ":vassal_status_desired"),
			(display_message, "@DEBUG (Quest Util): Player {reg32?SHOULD be:shouldn NOT be} and {reg31?IS:is NOT} a vassal.  Condition passed.", gpu_debug),
		(try_end),
    ]),
	
# script_cf_common_player_is_vassal_or_greater
# Checks if the player is a vassal, matches it against whether you wanted him to be king or not and fails (as a conditional script) if he doesn't match desired status.
# Input: arg1 (True-1/False-0)
# Output: none
("cf_common_player_is_vassal_or_greater",
    [
	    (store_script_param, ":status_desired", 1),
		
		### VASSAL STATUS ###
		(try_begin),
			(neq, "$players_kingdom", "fac_player_supporters_faction"),
			(assign, ":vassal_status", 1),
		(else_try),
			(assign, ":vassal_status", 0),
		(try_end),
		# (assign, ":fiefs_owned", 0),
		# (try_for_range, ":center_no", centers_begin, centers_end),
			# (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			# (val_add, ":fiefs_owned", 1),
		# (try_end),
		# (try_begin),
			# (ge, ":fiefs_owned", 1),
			# (eq, "$players_kingdom", "fac_player_supporters_faction"),
			# (assign, ":king_status", 1),
		# (else_try),
			# (assign, ":king_status", 0),
		# (try_end),
		
		### KING STATUS ###
		(try_begin),
			(eq, "$players_kingdom_name_set", 1),
			(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
			(faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
			(assign, ":king_status", 1),
		(else_try),
			(assign, ":king_status", 0),
		(try_end),
		
		(try_begin),
			(eq, ":king_status", 0),
			(eq, ":vassal_status", 0),
			(assign, ":noble_status", 0),
		(else_try),
			(this_or_next|eq, ":king_status", 1),
			(eq, ":vassal_status", 1),
			(assign, ":noble_status", 1),
		(try_end),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(neq, ":noble_status", ":status_desired"),
			(assign, reg31, ":noble_status"),
			(assign, reg32, ":status_desired"),
			(display_message, "@DEBUG (Quest Util): Player {reg32?SHOULD be:shouldn NOT be} and {reg31?IS:is NOT} a vassal or king.  Condition failed.", gpu_debug),
		(try_end),
		
		(eq, ":noble_status", ":status_desired"), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(assign, reg31, ":noble_status"),
			(assign, reg32, ":status_desired"),
			(display_message, "@DEBUG (Quest Util): Player {reg32?SHOULD be:shouldn NOT be} and {reg31?IS:is NOT} a vassal or king.  Condition passed.", gpu_debug),
		(try_end),
    ]),
	
# script_cf_common_player_is_mercenary
# Checks if the player is a vassal, matches it against whether you wanted him to be king or not and fails (as a conditional script) if he doesn't match desired status.
# Input: arg1 (True-1/False-0)
# Output: none
("cf_common_player_is_mercenary",
    [
	    (store_script_param, ":mercenary_status_desired", 1),
		
		(try_begin),
			(gt, "$players_kingdom", 0),
			(neq, "$players_kingdom", "fac_player_supporters_faction"),
			(neq, "$players_kingdom", "fac_player_faction"),
			(eq, "$player_has_homage", 0),
			(assign, ":mercenary_status", 1),
		(else_try),
			(assign, ":mercenary_status", 0),
		(try_end),
		
		# Backup check to be safe.
		(try_begin),
			(neq, ":mercenary_status", 0),
			(try_begin),
				(call_script, "script_cf_qus_player_is_king", 1),
				(display_message, "@Player was thought to be a mercenary, but really is a king.", gpu_debug),
				(assign, ":mercenary_status", 0),
			(else_try),
				(call_script, "script_cf_qus_player_is_vassal", 1),
				(display_message, "@Player was thought to be a mercenary, but really is a vassal.", gpu_debug),
				(assign, ":mercenary_status", 0),
			(else_try),
				(call_script, "script_cf_qus_player_is_king", 0),
				(call_script, "script_cf_qus_player_is_vassal", 0),
				(eq, "$players_kingdom", 0),
				(eq, "$player_has_homage", 0),
				(display_message, "@Player was thought to be a mercenary, but really is unaffiliated.", gpu_debug),
				(assign, ":mercenary_status", 0),
			(try_end),
		(try_end),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(neq, ":mercenary_status", ":mercenary_status_desired"),
			(assign, reg31, ":mercenary_status"),
			(assign, reg32, ":mercenary_status_desired"),
			(display_message, "@DEBUG (Quest Util): Player {reg32?SHOULD be:shouldn NOT be} and {reg31?IS:is NOT} a mercenary.  Condition failed.", gpu_debug),
		(try_end),
		
		(eq, ":mercenary_status", ":mercenary_status_desired"), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(assign, reg31, ":mercenary_status"),
			(assign, reg32, ":mercenary_status_desired"),
			(display_message, "@DEBUG (Quest Util): Player {reg32?SHOULD be:shouldn NOT be} and {reg31?IS:is NOT} a mercenary.  Condition passed.", gpu_debug),
		(try_end),
    ]),
	
# script_cf_qus_party_within_range_of_owned_fiefs
# Checks what property the party leader owns and if he is within that realm of his property.
# Input: arg1 (party_no)
# Output: none
("cf_qus_party_within_range_of_owned_fiefs",
    [
	    (store_script_param, ":party_no", 1),
		(set_fixed_point_multiplier, 1),
		
		# Initialize boundary variables.
		(assign, ":west_border", 0),  # X - axis (-)
		(assign, ":east_border", 0),  # X - axis (+)
		(assign, ":north_border", 0), # Y - axis (+)
		(assign, ":south_border", 0), # Y - axis (-)
		(assign, ":min_fief_distance", -1),
		
		# Determine player position on the map.
		(party_get_position, pos1, ":party_no"),
		(position_get_x, ":x_player", pos1),
		(position_get_y, ":y_player", pos1),
		
		# Determine leader of the party
		(party_stack_get_troop_id, ":troop_leader", ":party_no", 0),
		(str_store_troop_name, s31, ":troop_leader"),
		
		# Figure out the borders of the owned properties.
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, ":troop_leader"),
			(party_get_position, pos2, ":center_no"),
			(position_get_x, ":x_loc", pos2),
			(position_get_y, ":y_loc", pos2),
			(try_begin),
				(this_or_next|ge, ":x_loc", ":east_border"),
				(eq, ":east_border", 0),
				(assign, ":east_border", ":x_loc"),
			(try_end),
			(try_begin),
				(this_or_next|lt, ":x_loc", ":west_border"),
				(eq, ":west_border", 0),
				(assign, ":west_border", ":x_loc"),
			(try_end),
			(try_begin),
				(this_or_next|ge, ":y_loc", ":north_border"),
				(eq, ":north_border", 0),
				(assign, ":north_border", ":y_loc"),
			(try_end),
			(try_begin),
				(this_or_next|lt, ":y_loc", ":south_border"),
				(eq, ":south_border", 0),
				(assign, ":south_border", ":y_loc"),
			(try_end),
			(try_begin),
				(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
				(this_or_next|ge, ":min_fief_distance", ":distance"),
				(eq, ":min_fief_distance", -1),
				(assign, ":min_fief_distance", ":distance"),
			(try_end),
			
			(ge, DEBUG_QUEST_UTILITIES, 2),
			(assign, reg31, ":x_loc"),
			(assign, reg32, ":y_loc"),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@DEBUG (Quest Util): {s31} is located at {reg31}, {reg32}.", gpu_debug),
		(try_end),
		
		(try_begin),
			(ge, DEBUG_QUEST_UTILITIES, 2),
			(assign, reg31, ":north_border"),
			(assign, reg32, ":south_border"),
			(assign, reg33, ":west_border"),
			(assign, reg34, ":east_border"),
			(assign, reg35, ":min_fief_distance"),
			(assign, reg36, ":x_player"),
			(assign, reg37, ":y_player"),
			(str_store_party_name, s31, ":party_no"),
			(display_message, "@DEBUG (Quest Util): {s31} @ ({reg36}, {reg37}), {reg33} W, {reg31} N, {reg34} E, {reg32} S, {reg35} Min Dist", gpu_debug),
		(try_end),
		
		(try_begin),
			(le, ":west_border", ":x_player"),
			(ge, ":east_border", ":x_player"),
			(le, ":south_border", ":y_player"),
			(ge, ":north_border", ":y_player"),
			(assign, ":player_in_box", 1),
		(else_try),
			(assign, ":player_in_box", 0),
		(try_end),
		
		(try_begin),
			(le, ":min_fief_distance", 10),
			(assign, ":party_near_fief", 1),
		(else_try),
			(assign, ":party_near_fief", 0),
		(try_end),
		
		(try_begin),
			(this_or_next|eq, ":player_in_box", 1),
			(eq, ":party_near_fief", 1),
			(assign, ":party_within_realm", 1),
		(else_try),
			(assign, ":party_within_realm", 0),
		(try_end),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(neq, ":party_within_realm", 1),
			(assign, reg31, ":player_in_box"),
			(assign, reg32, ":party_near_fief"),
			(str_store_party_name, s31, ":party_no"),
			(display_message, "@DEBUG (Quest Util): {s31} {reg32?IS:is NOT} near a fief and {reg31?IS:is NOT} within owned land.  Condition failed.", gpu_debug),
		(try_end),
		
		(eq, ":party_within_realm", 1), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(assign, reg31, ":player_in_box"),
			(assign, reg32, ":party_near_fief"),
			(str_store_party_name, s31, ":party_no"),
			(display_message, "@DEBUG (Quest Util): {s31} {reg32?IS:is NOT} near a fief and {reg31?IS:is NOT} within owned land.  Condition passed.", gpu_debug),
		(try_end),
    ]),
	
# script_cf_qus_party_within_range_of_kingdom
# Checks what property the kingdom owns and if he is within that realm of his property.
# Input: arg1 (party_no)
# Output: none
("cf_qus_party_within_range_of_kingdom",
    [
	    (store_script_param, ":party_no", 1),
		(set_fixed_point_multiplier, 1),
		
		# Initialize boundary variables.
		(assign, ":west_border", 0),  # X - axis (-)
		(assign, ":east_border", 0),  # X - axis (+)
		(assign, ":north_border", 0), # Y - axis (+)
		(assign, ":south_border", 0), # Y - axis (-)
		(assign, ":min_fief_distance", -1),
		
		# Determine player position on the map.
		(party_get_position, pos1, ":party_no"),
		(position_get_x, ":x_player", pos1),
		(position_get_y, ":y_player", pos1),
		(store_sub, ":x_lower_limit", ":x_player", REALM_QUAL_MAX_DISTANCE_TO_CENTER),
		(store_add, ":x_upper_limit", ":x_player", REALM_QUAL_MAX_DISTANCE_TO_CENTER),
		(store_add, ":y_upper_limit", ":y_player", REALM_QUAL_MAX_DISTANCE_TO_CENTER),
		(store_sub, ":y_lower_limit", ":y_player", REALM_QUAL_MAX_DISTANCE_TO_CENTER),
		
		# Determine leader of the party & his faction.
		(party_stack_get_troop_id, ":troop_leader", ":party_no", 0),
		(str_store_troop_name, s31, ":troop_leader"),
		(store_troop_faction, ":faction_no", ":troop_leader"),
		(try_begin),
			(eq, ":troop_leader", "trp_player"),
			(assign, ":faction_no", "$players_kingdom"),
		(try_end),
		
		# Figure out the borders of the kingdom.
		(try_for_range, ":center_no", centers_begin, centers_end),
			(store_faction_of_party, ":faction_town", ":center_no"),
			(eq, ":faction_no", ":faction_town"),
			(party_get_position, pos2, ":center_no"),
			(position_get_x, ":x_loc", pos2),
			(position_get_y, ":y_loc", pos2),
			
			# Qualify if the center is horizontally and/or vertically within +/- 100 distance of the player.
			(assign, ":pass", 0),
			(try_begin),
				(try_begin),
					(assign, ":player_inside_box", 0),
					(is_between, ":x_loc", ":x_lower_limit", ":x_upper_limit"),
					(is_between, ":y_loc", ":y_lower_limit", ":y_upper_limit"),
					(assign, ":player_inside_box", 1),
				(try_end),
				(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
				(this_or_next|eq, ":player_inside_box", 1),
				(le, ":distance", 40),
				(assign, ":pass", 1),
			(else_try),
				(ge, DEBUG_QUEST_UTILITIES, 2), # Diagnostic
				(str_store_party_name, s31, ":center_no"),
				(display_message, "@DEBUG (Quest Util): {s31} disqualified for not being within limited range.", gpu_debug),
			(try_end),
			(eq, ":pass", 1),
			
			(try_begin),
				(this_or_next|ge, ":x_loc", ":east_border"),
				(eq, ":east_border", 0),
				(assign, ":east_border", ":x_loc"),
			(try_end),
			(try_begin),
				(this_or_next|lt, ":x_loc", ":west_border"),
				(eq, ":west_border", 0),
				(assign, ":west_border", ":x_loc"),
			(try_end),
			(try_begin),
				(this_or_next|ge, ":y_loc", ":north_border"),
				(eq, ":north_border", 0),
				(assign, ":north_border", ":y_loc"),
			(try_end),
			(try_begin),
				(this_or_next|lt, ":y_loc", ":south_border"),
				(eq, ":south_border", 0),
				(assign, ":south_border", ":y_loc"),
			(try_end),
			(try_begin),
				(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
				(this_or_next|ge, ":min_fief_distance", ":distance"),
				(eq, ":min_fief_distance", -1),
				(assign, ":min_fief_distance", ":distance"),
			(try_end),
			
			(ge, DEBUG_QUEST_UTILITIES, 1), # Diagnostic
			(assign, reg31, ":x_loc"),
			(assign, reg32, ":y_loc"),
			(assign, reg33, ":distance"),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@DEBUG (Quest Util): {s31} is located at {reg31}, {reg32} some {reg33} leagues away.", gpu_debug),
		(try_end),
		
		(try_begin),
			(ge, DEBUG_QUEST_UTILITIES, 1), # Diagnostic
			(assign, reg31, ":north_border"),
			(assign, reg32, ":south_border"),
			(assign, reg33, ":west_border"),
			(assign, reg34, ":east_border"),
			(assign, reg35, ":min_fief_distance"),
			(assign, reg36, ":x_player"),
			(assign, reg37, ":y_player"),
			(str_store_party_name, s31, ":party_no"),
			(display_message, "@DEBUG (Quest Util): {s31} @ ({reg36}, {reg37}), {reg33} W, {reg31} N, {reg34} E, {reg32} S, {reg35} leagues", gpu_debug),
		(try_end),
		
		(try_begin),
			(le, ":west_border", ":x_player"),
			(ge, ":east_border", ":x_player"),
			(le, ":south_border", ":y_player"),
			(ge, ":north_border", ":y_player"),
			(assign, ":player_in_box", 1),
		(else_try),
			(assign, ":player_in_box", 0),
		(try_end),
		
		(try_begin),
			(le, ":min_fief_distance", 10),
			(assign, ":party_near_fief", 1),
		(else_try),
			(assign, ":party_near_fief", 0),
		(try_end),
		
		(try_begin),
			(this_or_next|eq, ":player_in_box", 1),
			(eq, ":party_near_fief", 1),
			(assign, ":party_within_realm", 1),
		(else_try),
			(assign, ":party_within_realm", 0),
		(try_end),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(neq, ":party_within_realm", 1),
			(assign, reg31, ":player_in_box"),
			(assign, reg32, ":party_near_fief"),
			(str_store_party_name, s31, ":party_no"),
			(display_message, "@DEBUG (Quest Util): {s31} {reg32?IS:is NOT} near a fief and {reg31?IS:is NOT} in the kingdom.  Condition failed.", gpu_debug),
		(try_end),
		
		(eq, ":party_within_realm", 1), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(assign, reg31, ":player_in_box"),
			(assign, reg32, ":party_near_fief"),
			(str_store_party_name, s31, ":party_no"),
			(display_message, "@DEBUG (Quest Util): {s31} {reg32?IS:is NOT} near a fief and {reg31?IS:is NOT} in the kingdom.  Condition passed.", gpu_debug),
		(try_end),
    ]),

# script_cf_qus_party_close_to_center
# Checks what property the kingdom owns and if he is within that realm of his property.
("cf_qus_party_close_to_center",
    [
	    (store_script_param, ":party_no", 1),
		(store_script_param, ":center_no", 2),
		(store_script_param, ":max_distance", 3),
		
		(set_fixed_point_multiplier, 1),
		
		(store_distance_to_party_from_party, ":distance", ":party_no", ":center_no"),
		
		# CONDITIONAL OUTPUT
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(gt, ":distance", ":max_distance"),
			(str_store_party_name, s31, ":party_no"),
			(str_store_party_name, s32, ":center_no"),
			(display_message, "@DEBUG (Quest Util): {s31} is NOT near {s32}.  Condition failed.", gpu_debug),
		(try_end),
		
		(le, ":distance", ":max_distance"), # Conditional Failure
		
		(try_begin),
			(ge, DEBUG_QUEST_CONDITIONS, 1),
			(str_store_party_name, s31, ":party_no"),
			(str_store_party_name, s32, ":center_no"),
			(display_message, "@DEBUG (Quest Util): {s31} IS near {s32}.  Condition passed.", gpu_debug),
		(try_end),
    ]),
	
# script_common_battle_end
# Checks for end of battle conditions.
# Goal #1 - Track when prisoner caravans are attacked.
("common_battle_end",
    [
		(store_script_param, ":party_attacker", 1),
		(store_script_param, ":party_defender", 2),
		(store_script_param, ":defender_won", 3),
		
		(assign, ":leader_attacker", -1),
		(assign, ":leader_defender", -1),
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(try_begin),
				(troop_slot_eq, ":troop_no", slot_troop_leaded_party, ":party_attacker"),
				(assign, ":leader_attacker", ":troop_no"),
			(else_try),
				(troop_slot_eq, ":troop_no", slot_troop_leaded_party, ":party_defender"),
				(assign, ":leader_defender", ":troop_no"),
			(try_end),
		(try_end),
		(try_begin),
			(eq, ":party_attacker", "p_main_party"),
			(assign, ":leader_attacker", "trp_player"),
		(else_try),
			(eq, ":party_defender", "p_main_party"),
			(assign, ":leader_defender", "trp_player"),
		(try_end),
		
		(party_get_slot, ":party_type_attacker", ":party_attacker", slot_party_type),
		(party_get_slot, ":party_type_defender", ":party_defender", slot_party_type),
		
		(try_begin),
			### PRISONER CARAVAN DEFEATED ### (defender)
			(eq, ":defender_won", 0),
			(eq, ":party_type_defender", spt_prisoner_train),
			# Caravan attacked by kingdom lord or player.
			(this_or_next|eq, ":party_type_attacker", spt_kingdom_hero_party),
			(eq, ":party_attacker", "p_main_party"),
			# Give caravan wealth to leader of party.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_raided_by_troop, ":party_defender", ":leader_attacker"),
			
		(else_try),
			### PRISONER CARAVAN DEFEATED ### (attacker)
			(eq, ":defender_won", 1),
			(eq, ":party_type_attacker", spt_prisoner_train),
			# Caravan attacked by kingdom lord or player.
			(this_or_next|eq, ":party_type_defender", spt_kingdom_hero_party),
			(eq, ":party_defender", "p_main_party"),
			# Give caravan wealth to leader of party.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_raided_by_troop, ":party_attacker", ":leader_defender"),
			
		(else_try),
			### REGIONAL PATROL DEFEATED ### (defender)
			(eq, ":defender_won", 0),
			(eq, ":party_type_defender", spt_patrol),
			(call_script, "script_diplomacy_patrol_functions", ":party_type_defender", PATROL_DETERMINE_PATROL_NO),
			(is_between, reg2, walled_centers_begin, walled_centers_end),
			(str_store_party_name, s21, reg2),
			(assign, reg21, ":party_type_defender"),
			(display_message, "@DEBUG (patrols): Party #{reg21} is a patrol from {s21} and has been defeated.", gpu_debug),
			
		(else_try),
			### REGIONAL PATROL DEFEATED ### (attacker)
			(eq, ":defender_won", 1),
			(eq, ":party_type_attacker", spt_patrol),
			(call_script, "script_diplomacy_patrol_functions", ":party_type_attacker", PATROL_DETERMINE_PATROL_NO),
			(is_between, reg2, walled_centers_begin, walled_centers_end),
			(str_store_party_name, s21, reg2),
			(assign, reg21, ":party_type_attacker"),
			(display_message, "@DEBUG (patrols): Party #{reg21} is a patrol from {s21} and has been defeated.", gpu_debug),
			
		(else_try),
			### PRISONER CARAVAN ### (defender)
			(eq, ":defender_won", 0),
			(eq, ":party_type_defender", spt_prisoner_train),
			(quest_get_slot, ":party_caravan", "qst_escort_to_mine", slot_quest_target_party),
			(quest_get_slot, ":caravan_home", "qst_escort_to_mine", slot_quest_giver_center),
			(try_begin),
				(ge, DEBUG_QUEST_PACK_3, 1),
				(str_store_party_name, s21, ":caravan_home"),
				(assign, reg21, ":party_caravan"),
				(display_message, "@DEBUG (QP3): The prisoner caravan from {s21} (Party #{reg21}) has been defeated.", gpu_debug),
			(try_end),
			(call_script, "script_qp3_quest_escort_to_mine", floris_quest_failure_condition), ## Fail Quest
			
		(else_try),
			### PRISONER CARAVAN ### (attacker)
			(eq, ":defender_won", 1),
			(eq, ":party_type_attacker", spt_prisoner_train),
			(quest_get_slot, ":party_caravan", "qst_escort_to_mine", slot_quest_target_party),
			(quest_get_slot, ":caravan_home", "qst_escort_to_mine", slot_quest_giver_center),
			(try_begin),
				(ge, DEBUG_QUEST_PACK_3, 1),
				(str_store_party_name, s21, ":caravan_home"),
				(assign, reg21, ":party_caravan"),
				(display_message, "@DEBUG (QP3): The prisoner caravan from {s21} (Party #{reg21}) has been defeated.", gpu_debug),
			(try_end),
			(call_script, "script_qp3_quest_escort_to_mine", floris_quest_failure_condition), ## Fail Quest
			
		(try_end),
		
	]),
	
# script_common_rename_troop
# PURPOSE: Create a regional name based on the faction of a troop and then set that troop's name to that value.
("common_rename_troop",
  [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":faction_no", 2),
		(store_script_param, ":type", 3), # SCRT_FIRST, SCRT_LAST, SCRT_FULL
		
		# Western European
		(assign, ":euro_boy_names_begin", "str_set_boy_2000"),
		(assign, ":euro_boy_names_end", "str_set_girl_2000"),
		(assign, ":euro_girl_names_begin", ":euro_boy_names_end"),
		(assign, ":euro_girl_names_end", "str_set_last_2000"),
		(assign, ":euro_last_names_begin", ":euro_girl_names_end"),
		(assign, ":euro_last_names_end", "str_set_boy_3000"),
		# Arabic
		# (assign, ":arabic_boy_names_begin", ":euro_last_names_end"),
		# (assign, ":arabic_boy_names_end", "str_set_girl_3000"),
		(assign, ":arabic_girl_names_begin", "str_set_girl_3000"),
		(assign, ":arabic_girl_names_end", "str_set_last_3001"),
		(assign, ":arabic_last_names_begin", ":arabic_girl_names_end"),
		(assign, ":arabic_last_names_end", "str_set_boy_4000"),
		# Norse
		(assign, ":viking_boy_names_begin", ":arabic_last_names_end"),
		(assign, ":viking_boy_names_end", "str_set_girl_4000"),
		(assign, ":viking_girl_names_begin", ":viking_boy_names_end"),
		(assign, ":viking_girl_names_end", "str_set_last_4000"),
		(assign, ":viking_last_names_begin", ":viking_girl_names_end"),
		(assign, ":viking_last_names_end", "str_name_list_end"),
		
		# Get the regional set to draw from.
		(try_begin),
			(neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(store_random_in_range, ":faction_no", kingdoms_begin, kingdoms_end),
			(eq, 1, 0), # Fail this block and try a new block with this fixed value.
		(else_try),
			(faction_get_slot, ":culture", ":faction_no", slot_faction_culture),
		(try_end),

		# Find our start & stop string limits.
		(try_begin),
			### ARABIC ###
			(this_or_next|eq, ":culture", "fac_culture_3"), ### MONGOLIAN ### - Khergit
			(eq, ":culture", "fac_culture_6"), ### ARABIC ### - Sarranid
			(assign, ":boy_name_start",  ":arabic_last_names_begin"),
			(assign, ":boy_name_end",    ":arabic_last_names_end"),
			(assign, ":girl_name_start", ":arabic_girl_names_begin"),
			(assign, ":girl_name_end",   ":arabic_girl_names_end"),
			(assign, ":last_name_start", ":arabic_last_names_begin"),
			(assign, ":last_name_end",   ":arabic_last_names_end"),
		(else_try),
			### NORSE ###
			(this_or_next|eq, ":culture", "fac_culture_2"), ### RUSSIAN ### - Vaegir
			(eq, ":culture", "fac_culture_4"), ### NORSE ### - Nord
			(assign, ":boy_name_start",  ":viking_boy_names_begin"),
			(assign, ":boy_name_end",    ":viking_boy_names_end"),
			(assign, ":girl_name_start", ":viking_girl_names_begin"),
			(assign, ":girl_name_end",   ":viking_girl_names_end"),
			(assign, ":last_name_start", ":viking_last_names_begin"),
			(assign, ":last_name_end",   ":viking_last_names_end"),
		(else_try),
			### WESTERN EUROPEAN ###
			(this_or_next|eq, ":culture", "fac_culture_1"), ### WESTERN EUROPEAN ### - Swadian
			(eq, ":culture", "fac_culture_5"), ### WESTERN EUROPEAN ### - Rhodoks
			(assign, ":boy_name_start",  ":euro_boy_names_begin"),
			(assign, ":boy_name_end",    ":euro_boy_names_end"),
			(assign, ":girl_name_start", ":euro_girl_names_begin"),
			(assign, ":girl_name_end",   ":euro_girl_names_end"),
			(assign, ":last_name_start", ":euro_last_names_begin"),
			(assign, ":last_name_end",   ":euro_last_names_end"),
		(try_end),
		
		# Get the strings.
		(troop_get_type, reg21, ":troop_no"),
		(try_begin),
			(eq, reg21, 0),
			(store_random_in_range, ":boy_string", ":boy_name_start", ":boy_name_end"),
			(str_store_string, s22, ":boy_string"),
		(else_try),
			(store_random_in_range, ":girl_string", ":girl_name_start", ":girl_name_end"),
			(str_store_string, s22, ":girl_string"),
		(try_end),
		(store_random_in_range, ":last_string", ":last_name_start", ":last_name_end"),
		(str_store_string, s23, ":last_string"),
		
		# Add a NPC title if applicable.
		(str_clear, s24),
		(try_begin),
			## Travelers ##
			(is_between, ":troop_no", tavern_travelers_begin, tavern_travelers_end),
			(str_store_string, s24, "@ the Traveler"),
			(store_random_in_range, ":roll", 0, 2),
			(try_begin), (eq, ":roll", 0), (str_store_string, s24, "@ the Traveler"),
			(else_try),  (eq, ":roll", 1), (str_store_string, s24, "@ the Explorer"),
			(try_end),
		(else_try),
			## Book Sellers ##
			(is_between, ":troop_no", tavern_booksellers_begin, tavern_booksellers_end),
			(store_random_in_range, ":roll", 0, 3),
			(try_begin), (eq, ":roll", 0), (str_store_string, s24, "@ the Bookseller"),
			(else_try),  (eq, ":roll", 1), (str_store_string, s24, "@ the Scribe"),
			(else_try),  (eq, ":roll", 2), (str_store_string, s24, "@ the Scholar"),
			(try_end),
		(else_try),
			## Ransom Brokers ##
			(is_between, ":troop_no", ransom_brokers_begin, ransom_brokers_end),
			(store_random_in_range, ":roll", 0, 3),
			(try_begin), (eq, ":roll", 0), (str_store_string, s24, "@ the Slaver"),
			(else_try),  (eq, ":roll", 1), (str_store_string, s24, "@ the Broker"),
			(else_try),  (eq, ":roll", 2), (str_store_string, s24, "@ the Smuggler"),
			(try_end),
			(str_store_string, s24, "@ the Slaver"),
		(else_try),
			## Minstrels ##
			(is_between, ":troop_no", tavern_minstrels_begin, tavern_minstrels_end),
			(store_random_in_range, ":roll", 0, 4),
			(try_begin), (eq, ":roll", 0), (str_store_string, s24, "@ the Minstrel"),
			(else_try),  (eq, ":roll", 1), (str_store_string, s24, "@ the Bard"),
			(else_try),  (eq, ":roll", 2), (str_store_string, s24, "@ the Magnificent"),
			(else_try),  (eq, ":roll", 3), (str_store_string, s24, "@ the Poet"),
			(try_end),
		(try_end),
		
		# Put the name together.
		(str_clear, s21),
		(try_begin),
			(eq, ":type", SCRT_FIRST),
			(str_store_string, s21, "@{s22}{s24}"),
		(else_try),
			(eq, ":type", SCRT_LAST),
			(str_store_string, s21, "@{s23}{s24}"),
		(else_try),
			(eq, ":type", SCRT_FULL),
			(str_store_string, s21, "@{s22} {s23}{s24}"),	
		(try_end),
		
		(troop_set_name, ":troop_no", s21),
	]),
	
# script_common_store_temp_name_to_s1
# PURPOSE: Create a regional name based on the faction of a troop and then set that troop's name to that value.
# EXAMPLE: (call_script, "script_common_store_temp_name_to_s1", ":is_female", ":faction_no", ":type"),
("common_store_temp_name_to_s1",
  [
		(store_script_param, ":is_female", 1),
		(store_script_param, ":faction_no", 2),
		(store_script_param, ":type", 3), # SCRT_FIRST, SCRT_LAST, SCRT_FULL
		
		# Western European
		(assign, ":euro_boy_names_begin", "str_set_boy_2000"),
		(assign, ":euro_boy_names_end", "str_set_girl_2000"),
		(assign, ":euro_girl_names_begin", ":euro_boy_names_end"),
		(assign, ":euro_girl_names_end", "str_set_last_2000"),
		(assign, ":euro_last_names_begin", ":euro_girl_names_end"),
		(assign, ":euro_last_names_end", "str_set_boy_3000"),
		# Arabic
		# (assign, ":arabic_boy_names_begin", ":arabic_girl_names_end"),
		# (assign, ":arabic_boy_names_end", "str_set_boy_4000"),
		(assign, ":arabic_girl_names_begin", "str_set_girl_3000"),
		(assign, ":arabic_girl_names_end", "str_set_last_3001"),
		(assign, ":arabic_last_names_begin", ":arabic_girl_names_end"),
		(assign, ":arabic_last_names_end", "str_set_boy_4000"),
		# # Norse
		(assign, ":viking_boy_names_begin", ":arabic_last_names_end"),
		(assign, ":viking_boy_names_end", "str_set_girl_4000"),
		(assign, ":viking_girl_names_begin", ":viking_boy_names_end"),
		(assign, ":viking_girl_names_end", "str_set_last_4000"),
		(assign, ":viking_last_names_begin", ":viking_girl_names_end"),
		(assign, ":viking_last_names_end", "str_name_list_end"),
		
		# Get the regional set to draw from.
		(try_begin),
			(neg|is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(store_random_in_range, ":faction_no", kingdoms_begin, kingdoms_end),
			(eq, 1, 0), # Fail this block and try a new block with this fixed value.
		(else_try),
			(faction_get_slot, ":culture", ":faction_no", slot_faction_culture),
		(try_end),

		# Find our start & stop string limits.
		(try_begin),
			### ARABIC ###
			(this_or_next|eq, ":culture", "fac_culture_3"), ### MONGOLIAN ### - Khergit
			(eq, ":culture", "fac_culture_6"), ### ARABIC ### - Sarranid
			(assign, ":boy_name_start",  ":arabic_last_names_begin"),
			(assign, ":boy_name_end",    ":arabic_last_names_end"),
			(assign, ":girl_name_start", ":arabic_girl_names_begin"),
			(assign, ":girl_name_end",   ":arabic_girl_names_end"),
			(assign, ":last_name_start", ":arabic_last_names_begin"),
			(assign, ":last_name_end",   ":arabic_last_names_end"),
		(else_try),
			### NORSE ###
			(this_or_next|eq, ":culture", "fac_culture_2"), ### RUSSIAN ### - Vaegir
			(eq, ":culture", "fac_culture_4"), ### NORSE ### - Nord
			(assign, ":boy_name_start",  ":viking_boy_names_begin"),
			(assign, ":boy_name_end",    ":viking_boy_names_end"),
			(assign, ":girl_name_start", ":viking_girl_names_begin"),
			(assign, ":girl_name_end",   ":viking_girl_names_end"),
			(assign, ":last_name_start", ":viking_last_names_begin"),
			(assign, ":last_name_end",   ":viking_last_names_end"),
		(else_try),
			### WESTERN EUROPEAN ###
			(this_or_next|eq, ":culture", "fac_culture_1"), ### WESTERN EUROPEAN ### - Swadian
			(eq, ":culture", "fac_culture_5"), ### WESTERN EUROPEAN ### - Rhodoks
			(assign, ":boy_name_start",  ":euro_boy_names_begin"),
			(assign, ":boy_name_end",    ":euro_boy_names_end"),
			(assign, ":girl_name_start", ":euro_girl_names_begin"),
			(assign, ":girl_name_end",   ":euro_girl_names_end"),
			(assign, ":last_name_start", ":euro_last_names_begin"),
			(assign, ":last_name_end",   ":euro_last_names_end"),
		(try_end),
		
		# Get the strings.
		(assign, reg21, ":is_female"),
		(try_begin),
			(eq, reg21, 0),
			(store_random_in_range, ":boy_string", ":boy_name_start", ":boy_name_end"),
			(str_store_string, s22, ":boy_string"),
			(assign, reg1, ":boy_string"),
		(else_try),
			(store_random_in_range, ":girl_string", ":girl_name_start", ":girl_name_end"),
			(str_store_string, s22, ":girl_string"),
			(assign, reg1, ":girl_string"),
		(try_end),
		(store_random_in_range, ":last_string", ":last_name_start", ":last_name_end"),
		(str_store_string, s23, ":last_string"),
		(assign, reg2, ":last_string"),
		
		# Put the name together.
		(str_clear, s21),
		(try_begin),
			(eq, ":type", SCRT_FIRST),
			(str_store_string, s21, "@{s22}"),
			(assign, reg2, -1), # Clear out last name.
		(else_try),
			(eq, ":type", SCRT_LAST),
			(str_store_string, s21, "@{s23}"),
			(assign, reg1, -1), # Clear out first name.
		(else_try),
			(eq, ":type", SCRT_FULL),
			(str_store_string, s21, "@{s22} {s23}"),	
		(try_end),
		
		(str_store_string, s1, s21),
	]),
	
# script_cf_common_mayor_quest_available
# Checks if a mayor quest is available for use to build a quest menu.
# Input: none
# Output: none
("cf_common_mayor_quest_available",
    [
		(store_script_param, ":giver_troop", 1),
		(store_script_param, ":quest_no", 2),
		
		(store_character_level, ":player_level", "trp_player"),
		# (store_troop_faction, ":giver_faction_no", ":giver_troop"),
		
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
		
		(try_begin),
			# Mayor quests
			(eq, ":quest_no", "qst_escort_merchant_caravan"),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			## WINDYPLAINS+ ## - Filtered selection town a little.
			#(store_random_party_in_range, ":quest_target_center", towns_begin, towns_end),
			(call_script, "script_qus_select_random_center", center_is_town_friendly, 5, 35, ":giver_center_no"),
			(assign, ":quest_target_center", reg1),
			(try_begin), # Second check done in the event that no town is viable in the first check and giver center randomly picked.
				(eq, ":quest_target_center", ":giver_center_no"),
				(call_script, "script_qus_select_random_center", center_is_town_friendly, 0, 60, ":giver_center_no"),
				(assign, ":quest_target_center", reg1),
			(try_end),
			## WINDYPLAINS- ##
			(store_distance_to_party_from_party, ":dist", ":giver_center_no",":quest_target_center"),
			(assign, ":quest_gold_reward", ":dist"),
			(val_add, ":quest_gold_reward", 25),
			(val_mul, ":quest_gold_reward", 25),
			(val_div, ":quest_gold_reward", 5), # 20),
			(store_random_in_range, ":quest_target_amount", 6, 12),
			(assign, "$escort_merchant_caravan_mode", 0),
			(assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_deliver_wine"),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			## WINDYPLAINS+ ## - Filtered selection town a little.
			#(store_random_party_in_range, ":quest_target_center", towns_begin, towns_end),
			(call_script, "script_qus_select_random_center", center_is_town_friendly, 25, 95, ":giver_center_no"),
			(assign, ":quest_target_center", reg1),
			## WINDYPLAINS- ##
			(store_random_in_range, ":random_no", 0, 2),
			## WINDYPLAINS+ ## - Revised gold earned from hauling cargo.
			(try_begin),
				(eq, ":random_no", 0),
				(assign, ":quest_target_item", "itm_quest_wine"),
				(assign, ":cash_seed", 30),
			(else_try),
				(assign, ":quest_target_item", "itm_quest_ale"),
				(assign, ":cash_seed", 10),
			(try_end),
			(store_random_in_range, ":quest_target_amount", 6, 12),
			(store_distance_to_party_from_party, ":dist", ":giver_center_no",":quest_target_center"),
			(assign, ":quest_gold_reward", ":cash_seed"),
			(val_add, ":quest_gold_reward", ":dist"), # 18/38 - 70/90
			(val_mul, ":quest_gold_reward", ":quest_target_amount"), # 156 - 384
			## WINDYPLAINS- ##
			# (assign, ":quest_gold_reward", ":dist"),
			# (val_add, ":quest_gold_reward", 2),
			# (assign, ":multiplier", 5),
			# (val_add, ":multiplier", ":quest_target_amount"),
			# (val_mul, ":quest_gold_reward", ":multiplier"),
			# (val_div, ":quest_gold_reward", 100),
			# (val_mul, ":quest_gold_reward", 10),
			(store_item_value,"$qst_deliver_wine_debt",":quest_target_item"),
			(val_mul,"$qst_deliver_wine_debt",":quest_target_amount"),
			(val_mul,"$qst_deliver_wine_debt", 6),
			(val_div,"$qst_deliver_wine_debt",5),
			(assign, ":quest_expiration_days", 7),
			(assign, ":quest_dont_give_again_period", 5), # 20),
			(assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_troublesome_bandits"),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			(store_character_level, ":quest_gold_reward", "trp_player"),
			(val_add, ":quest_gold_reward", 20),
			(val_mul, ":quest_gold_reward", 35),
			(val_div, ":quest_gold_reward",100),
			(val_mul, ":quest_gold_reward", 10),
			(assign, ":quest_expiration_days", 30),
			(assign, ":quest_dont_give_again_period", 30),
			(assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_kidnapped_girl"),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			## WINDYPLAINS+ ## - Filtered selection town a little.
			# (store_random_in_range, ":quest_target_center", villages_begin, villages_end),
			(call_script, "script_qus_select_random_center", center_is_village_friendly, 25, 100, ":giver_center_no"),
			(assign, ":quest_target_center", reg1),
			## WINDYPLAINS- ##
			(store_character_level, ":quest_target_amount"),
			(val_add, ":quest_target_amount", 15),
			(store_distance_to_party_from_party, ":dist", ":giver_center_no", ":quest_target_center"),
			(val_add, ":dist", 15),
			(val_mul, ":dist", 2),
			(val_mul, ":quest_target_amount", ":dist"),
			(val_div, ":quest_target_amount",100),
			(val_mul, ":quest_target_amount",10),
			(assign, ":quest_gold_reward", ":quest_target_amount"),
			(val_div, ":quest_gold_reward", 40),
			(val_mul, ":quest_gold_reward", 10),
			(assign, ":quest_expiration_days", 15),
			(assign, ":quest_dont_give_again_period", 30),
			(assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_move_cattle_herd"),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			## WINDYPLAINS+ ## - Filtered selection town a little.
			# (call_script, "script_cf_select_random_town_at_peace_with_faction", ":giver_faction_no"),
			# (neq, ":giver_center_no", reg0),
			# (assign, ":quest_target_center", reg0),
			(call_script, "script_qus_select_random_center", center_is_town_friendly, 15, 85, ":giver_center_no"),
			(assign, ":quest_target_center", reg1),
			(try_begin), # Second check done in the event that no town is viable in the first check and giver center randomly picked.
				(eq, ":quest_target_center", ":giver_center_no"),
				(call_script, "script_qus_select_random_center", center_is_town_friendly, 0, 120, ":giver_center_no"),
				(assign, ":quest_target_center", reg1),
			(try_end),
			## WINDYPLAINS- ##
			(store_distance_to_party_from_party, ":dist",":giver_center_no",":quest_target_center"),
			(assign, ":quest_gold_reward", ":dist"),
			(val_add, ":quest_gold_reward", 25),
			(val_mul, ":quest_gold_reward", 50),
			(val_div, ":quest_gold_reward", 6), # 20),
			(assign, ":quest_expiration_days", 30),
			(assign, ":quest_dont_give_again_period", 5), # 20),
			(assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_persuade_lords_to_make_peace"),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			(store_faction_of_party, ":cur_object_faction", ":giver_center_no"),
			(call_script, "script_cf_faction_get_random_enemy_faction", ":cur_object_faction"),
			(assign, ":cur_target_faction", reg0),
			(call_script, "script_cf_get_random_lord_except_king_with_faction", ":cur_object_faction"),
			(assign, ":cur_object_troop", reg0),
			(this_or_next|troop_slot_eq, ":cur_object_troop", slot_lord_reputation_type, lrep_quarrelsome),
			(this_or_next|troop_slot_eq, ":cur_object_troop", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":cur_object_troop", slot_lord_reputation_type, lrep_martial),
			(troop_slot_eq, ":cur_object_troop", slot_lord_reputation_type, lrep_debauched),

			(call_script, "script_cf_get_random_lord_except_king_with_faction", ":cur_target_faction"),
			(assign, ":quest_target_troop", reg0),
			(this_or_next|troop_slot_eq, ":quest_target_troop", slot_lord_reputation_type, lrep_quarrelsome),
			(this_or_next|troop_slot_eq, ":quest_target_troop", slot_lord_reputation_type, lrep_selfrighteous),
			(this_or_next|troop_slot_eq, ":quest_target_troop", slot_lord_reputation_type, lrep_martial),
			(troop_slot_eq, ":quest_target_troop", slot_lord_reputation_type, lrep_debauched),

			(assign, ":quest_object_troop", ":cur_object_troop"),
			(assign, ":quest_target_faction", ":cur_target_faction"),
			(assign, ":quest_object_faction", ":cur_object_faction"),
			(assign, ":quest_gold_reward", 12000),
			(assign, ":quest_convince_value", 7000),
			(assign, ":quest_expiration_days", 30),
			(assign, ":quest_dont_give_again_period", 100),
			(assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_deal_with_looters"),
			(is_between, ":player_level", 0, 15),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			(store_faction_of_party, ":cur_object_faction", ":giver_center_no"),
			(store_num_parties_destroyed_by_player, ":num_looters_destroyed", "pt_looters"),
			(party_template_set_slot,"pt_looters",slot_party_template_num_killed,":num_looters_destroyed"),
			(quest_set_slot,":quest_no",slot_quest_current_state,0),
			(quest_set_slot,":quest_no",slot_quest_target_party_template,"pt_looters"),
			(assign, ":quest_gold_reward", 500),
			(assign, ":quest_xp_reward", 500),
			(assign, ":quest_expiration_days", 20),
			(assign, ":quest_dont_give_again_period", 30),
			(assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_deal_with_night_bandits"),
			(is_between, ":player_level", 0, 15),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			(party_slot_ge, ":giver_center_no", slot_center_has_bandits, 1),
			(assign, ":quest_target_center", ":giver_center_no"),
			(assign, ":quest_expiration_days", 4),
			(assign, ":quest_dont_give_again_period", 15),
			(assign, ":result", ":quest_no"),
		(else_try),
			(eq, ":quest_no", "qst_fight_in_duel"),
			(is_between, ":giver_center_no", centers_begin, centers_end),
			(assign, ":quest_target_center", ":giver_center_no"),
			(assign, ":quest_expiration_days", 7),
			(assign, ":quest_dont_give_again_period", 30),
			(assign, ":quest_gold_reward", 750),
			(assign, ":quest_xp_reward", 750),
			(assign, ":quest_target_troop", "trp_new_geroian_swordsman"),
			(assign, ":result", ":quest_no"),
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
	
# script_common_merchant_stock_minimum_amount
# MODEL: (call_script, "script_common_merchant_stock_minimum_amount", ":center_no", ":item_no", ":minimum"),
# PURPOSE: Checks to see if a merchant has enough of a given item and if not then adds more to their stock.
("common_merchant_stock_minimum_amount",
  [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":item_no", 2),
		(store_script_param, ":minimum", 3),
		
		(try_begin),
			(this_or_next|is_between, ":center_no", towns_begin, towns_end),
			(is_between, ":center_no", villages_begin, villages_end),
			
			# Make sure the goods merchant has enough of the trade goods in his inventory to call it a 'surplus'.
			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(store_sub, ":troop_merchant", ":center_no", towns_begin),
				(val_add, ":troop_merchant", "trp_town_1_merchant"),
				(str_store_string, s32, "@town goods merchant"),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
				(store_sub, ":troop_merchant", ":center_no", villages_begin),
				(val_add, ":troop_merchant", "trp_village_1_elder"),
				(str_store_string, s32, "@village elder"),
			(try_end),
			
			(store_item_kind_count, ":item_count", ":item_no", ":troop_merchant"),
			(try_begin),
				(lt, ":item_count", ":minimum"),
				(store_sub, ":add_count", ":minimum", ":item_count"),
				(ge, ":add_count", 1),
				(troop_add_items, ":troop_merchant", ":item_no", ":add_count"),
			(else_try),
				(assign, ":add_count", 0),
			(try_end),
			(try_begin),
				(ge, DEBUG_QUEST_UTILITIES, 1),
				(ge, ":add_count", 1),
				(assign, reg31, ":add_count"),
				(str_store_item_name, s31, ":item_no"),
				(display_message, "@DEBUG (Quest Util): Added {reg31} {s31} to the {s32}'s inventory.", gpu_debug),
			(try_end),
		(else_try),
			(assign, reg31, ":center_no"),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@ERROR (Quest Util): Invalid center ({s31}, #{reg31}) used for script 'common_merchant_stock_minimum_amount'."),
		(try_end),
	]),
	
# script_common_change_veteran_recruits_in_party
# MODEL: (call_script, "script_common_change_veteran_recruits_in_party", ":center_no", ":troop_no", ":amount", ":reason_string"),
# PURPOSE: Add or remove noble recruits to a center/party for either the player or AI.
("common_change_veteran_recruits_in_party",
  [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_no", 2),
		(store_script_param, ":amount", 3),
		(store_script_param, ":reason_string", 4),
		
		# Determine which slot should get the recruits. (AI or player)
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(assign, ":recruit_slot", slot_center_veteran_pool),
		(else_try),
			(assign, ":recruit_slot", slot_center_veteran_ai),
		(try_end),
		
		# Change the amount of noble recruits available.
		(party_get_slot, ":recruits", ":center_no", ":recruit_slot"),
		(val_add, ":recruits", ":amount"),
		(party_set_slot, ":center_no", ":recruit_slot", ":recruits"),
		
		# Notify the player. (if applicable)
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(assign, reg1, ":amount"),
			(store_sub, reg2, reg1, 1),
			(str_store_party_name, s2, ":center_no"),
			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(str_store_string, s1, "@the town of {s2}"),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(str_store_string, s1, "@{s2}"),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
				(str_store_string, s1, "@the village of {s2}"),
			(else_try),
				(str_store_string, s1, "@your party"),
			(try_end),
			(try_begin),
				(neq, ":reason_string", -1),
				(str_store_string, s4, ":reason_string"),
			(else_try),
				(str_clear, s4),
			(try_end),
			(str_store_string, s1, "@{s4}{reg1} veteran{reg2?s:} {reg2?have:has} decided to join your cause in {s1}."),
			(str_store_string, s3, "@A Veteran Has Joined Your Cause"),
			(try_begin),
				(eq, "$enable_popups", 1),
				(dialog_box, "@{s1}", "@{s3}"),
			(else_try),
				(display_message, "@{s1}", gpu_green),
			(try_end),
		(else_try),
			(ge, DEBUG_RECRUITMENT, 1),
			(assign, reg1, ":amount"),
			(str_store_party_name, s2, ":center_no"),
			(display_message, "@DEBUG (recruitment): {reg1} recruits have been added to {s2}.", gpu_debug),
		(try_end),
	]),

# script_cf_common_troop_needed_for_quest
# PURPOSE: Checks if a troop is needed for a current quest and if so fails the script.
# EXAMPLE: (call_script, "script_cf_common_troop_needed_for_quest", ":troop_no"), # questutil_scripts.py
("cf_common_troop_needed_for_quest",
  [
	(store_script_param, ":troop_no", 1),
	
	(assign, ":continue", 1),
	## CAPTURE PRISONERS (Native)
	(try_begin),
		(check_quest_active, "qst_capture_prisoners"),
		(quest_slot_eq, "qst_capture_prisoners", slot_quest_target_troop, ":troop_no"),
		(assign, ":continue", 0),
		(ge, DEBUG_QUEST_UTILITIES, 1),
		(quest_get_slot, ":quest_target_troop", "qst_capture_prisoners", slot_quest_target_troop),
		(store_troop_count_prisoners, reg1, ":quest_target_troop", "p_main_party"),
		(gt, reg1, 0),
		(str_store_troop_name, s1, ":quest_target_troop"),
		(display_message, "@Your {s1} {reg1?prisoner:prisoners} were intentionally not sold.", gpu_debug),
	(try_end),
	
	## FOLLOW SPY (Native)
	(try_begin),
		(check_quest_active, "qst_follow_spy"),
		(this_or_next|eq, ":troop_no", "trp_spy"),
		(eq, ":troop_no", "trp_spy_partner"),
		(assign, ":continue", 0),
		(ge, DEBUG_QUEST_UTILITIES, 1),
		(store_troop_count_prisoners, reg1, "trp_spy", "p_main_party"),
		(store_troop_count_prisoners, reg2, "trp_spy_partner", "p_main_party"),
		(val_add, reg1, reg2),
		(display_message, "@Your {reg1} spy {reg1?prisoner:prisoners} were intentionally not sold.", gpu_debug),
	(try_end),
	
	## HUNT DOWN FUGITIVE (Native - Silverstag Modified)
	(try_begin),
		(check_quest_active, "qst_hunt_down_fugitive"),
		(eq, ":troop_no", "trp_fugitive"),
		(assign, ":continue", 0),
		(ge, DEBUG_QUEST_UTILITIES, 1),
		(store_troop_count_prisoners, reg1, "trp_fugitive", "p_main_party"),
		(store_sub, reg2, reg1, 1),
		(display_message, "@Your {reg1} fugitive {reg2?prisoner:prisoners} were intentionally not sold.", gpu_debug),
	(try_end),
	
	(eq, ":continue", 1),
  ]),
]


from util_wrappers import *
from util_scripts import *

scripts_directives = [
	# HOOK: Check for ending battle conditions.  Used to track when prisoner caravans are destroyed.
	[SD_OP_BLOCK_INSERT, "game_event_simulate_battle", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (assign, ":do_not_end_battle", 0), 0, 
		[
			(try_begin),
				(eq, ":new_attacker_strength", 0),
				(assign, ":outcome", 1),
			(else_try),
				(assign, ":outcome", 0),
			(try_end),
			(call_script, "script_common_battle_end", ":root_attacker_party", ":root_defender_party", ":outcome"),
		], 1],
		
	# HOOK: Individual quest packs insert a hook into script "abort_quest" that disables messages.  This common hook re-enables them.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (call_script, "script_end_quest", ":quest_no"), 0, 
		[(set_show_messages, 1),], 1],
		
	# HOOK: Inserts the initializing scripts in game start as needed.
	# [SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		# [(call_script, "script_qus_game_start"),], 1],
	#rename scripts to "insert" switch scripts (see end of scripts[])
	#[SD_RENAME, "end_tournament_fight" , "orig_end_tournament_fight"], 
	#[SD_RENAME, "fill_tournament_participants_troop" , "orig_fill_tournament_participants_troop"],
	#[SD_RENAME, "get_random_tournament_participant" , "orig_get_random_tournament_participant"],
	#[SD_RENAME, "set_items_for_tournament" , "orig_set_items_for_tournament"], 
	#Add in global variable $g_wp_town_walkers into the visitor code for script_init_town_walkers.
	# [SD_OP_BLOCK_INSERT, "init_town_walkers", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (set_visitor, ":entry_no", ":walker_troop_id"), 0, 
		# [(set_visitors,":entry_no", ":walker_troop_id", "$g_wp_town_walkers"),], 1],
	# [SD_OP_BLOCK_INSERT, "init_town_walkers", D_SEARCH_FROM_BOTTOM | D_SEARCH_LINENUMBER | D_INSERT_BEFORE, 0, 0, [
		# (call_script, "script_player_order_formations", ":order"),	#for formations
	# ]],
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
