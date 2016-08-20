# Companion Management System (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	

# script_ce_companion_ability_presets
# EXAMPLE: (call_script, "script_ce_companion_ability_presets"), # combat_scripts.py - ability constants in combat_constants.py
("ce_companion_ability_presets",
    [
		## NPC1 - Borcha
		(assign, ":troop_no", "trp_npc1"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_NIMBLE),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_SCAVENGER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_USEFUL_CONTACTS),
		## NPC2 - Marnid
		(assign, ":troop_no", "trp_npc2"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_QUICK_STUDY),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_CARGOMASTER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_ADMINISTRATOR),
		## NPC3 - Ymira
		(assign, ":troop_no", "trp_npc3"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_INSPIRING),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_QUICK_STUDY),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_ADMINISTRATOR),
		## NPC4 - Rolf
		(assign, ":troop_no", "trp_npc4"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_HARDY),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_ENDURANCE),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_COMMANDING_PRESENCE),
		## NPC5 - Baheshtur
		(assign, ":troop_no", "trp_npc5"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_HUNTER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_SHARPSHOOTER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_MASTER_BOWMAN),
		## NPC6 - Firentis
		(assign, ":troop_no", "trp_npc6"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_HARDY),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_INDOMITABLE),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_FORTITUDE),
		## NPC7 - Deshavi
		(assign, ":troop_no", "trp_npc7"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_TRAILBLAZER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_SHARPSHOOTER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_MASTER_BOWMAN),
		## NPC8 - Matheld
		(assign, ":troop_no", "trp_npc8"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_BERSERKER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_BOUNDLESS_ENDURANCE),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_BLOODLUST),
		## NPC9 - Alayen
		(assign, ":troop_no", "trp_npc9"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_BLADEMASTER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_COMMANDING_PRESENCE),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_TACTICIAN),
		## NPC10 - Bunduk
		(assign, ":troop_no", "trp_npc10"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_RAPID_RELOAD),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_BOUNDLESS_ENDURANCE),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_FIRING_CAPTAIN),
		## NPC11 - Katrin
		(assign, ":troop_no", "trp_npc11"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_SUPPLY_RUNNER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_CHEF),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_EFFICIENT),
		## NPC12 - Jeremus
		(assign, ":troop_no", "trp_npc12"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_QUICK_STUDY),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_UNASSIGNED),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_ADMINISTRATOR),
		## NPC13 - Nizar
		(assign, ":troop_no", "trp_npc13"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_INSPIRING),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_WATCHFUL_EYE),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_USEFUL_CONTACTS),
		## NPC14 - Lezalit
		(assign, ":troop_no", "trp_npc14"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_FORTITUDE),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_TACTICIAN),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_SIEGE_GENERAL),
		## NPC15 - Artimenner
		(assign, ":troop_no", "trp_npc15"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_SHIELD_BASHER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_TACTICIAN),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_ENGINEER),
		## NPC16 - Klethi
		(assign, ":troop_no", "trp_npc16"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_SCAVENGER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_POISONED_WEAPONS),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_SHARPSHOOTER),
		## NPC17 - Nissa
		(assign, ":troop_no", "trp_npc17"),
		(troop_set_slot, ":troop_no", slot_troop_requirement_1, BONUS_SHARPSHOOTER),
		(troop_set_slot, ":troop_no", slot_troop_requirement_2, BONUS_MASTER_BOWMAN),
		(troop_set_slot, ":troop_no", slot_troop_requirement_3, BONUS_VOLLEY_COMMANDER),
		
	]),
	
# script_cf_ce_troop_has_ability
# EXAMPLE: (call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_XXX), # combat_scripts.py - ability constants in combat_constants.py
("cf_ce_troop_has_ability",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":ability", 2),
		
		# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_ability_1, ":ability"),
		# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_ability_2, ":ability"),
		# (troop_slot_eq, ":troop_no", slot_troop_ability_3, ":ability"),
		(assign, ":continue", 0),
		(try_for_range, ":ability_slot", abilities_begin, abilities_end),
			(troop_slot_eq, ":troop_no", ":ability_slot", ":ability"),
			(assign, ":continue", 1),
		(try_end),
		(eq, ":continue", 1),
		
		(try_begin),
			(ge, DEBUG_TROOP_ABILITIES, 2),
			(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"), # combat_scripts.py - ability constants in combat_constants.py
			(str_store_troop_name, s32, ":troop_no"),
			(display_message, "@DEBUG (Abilities): {s32} found to have the '{s31}' ability.", gpu_debug),
		(try_end),
		
	]),
	
# script_ce_assign_troop_ability
# EXAMPLE: (call_script, "script_ce_assign_troop_ability", ":troop_no", BONUS_XXX, BONUS_TO_REPLACE), # combat_scripts.py - ability constants in combat_constants.py
("ce_assign_troop_ability",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":ability", 2),
		(store_script_param, ":ability_to_replace", 3),
		
		# Make sure we aren't assigning the same ability twice.
		(assign, ":block", 0),
		(try_for_range, ":ability_slot", abilities_begin, abilities_end),
			(troop_slot_eq, ":troop_no", ":ability_slot", ":ability"),
			(assign, ":block", 1),
		(try_end),
		
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_ability_1, ":ability_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 1),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_ability_1, ":ability"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_ability_1, BONUS_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_ability_2, ":ability_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 2),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_ability_2, ":ability"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_ability_2, BONUS_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_ability_3, ":ability_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 3),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_ability_3, ":ability"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_ability_3, BONUS_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_ability_4, ":ability_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 4),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_ability_4, ":ability"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_ability_4, BONUS_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_ability_5, ":ability_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 5),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_ability_5, ":ability"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_ability_5, BONUS_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_ability_6, ":ability_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 6),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_ability_6, ":ability"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_ability_6, BONUS_UNASSIGNED),
			(try_end),
		(else_try),
			## ERROR - No available slots for assignment.
			(assign, ":assignment_successful", 0),
			(assign, ":slot_no", 0),
		(try_end),
		
		(try_begin),
			(ge, DEBUG_TROOP_ABILITIES, 1),
			(eq, ":assignment_successful", 1),
			(eq, ":block", 1),
			(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"),
			(str_store_troop_name, s32, ":troop_no"),
			(assign, reg31, ":slot_no"),
			(display_message, "@DEBUG (Abilities): {s32} already had '{s31}'.", gpu_debug),
			(neq, ":ability_to_replace", BONUS_UNASSIGNED),
			(call_script, "script_ce_store_troop_ability_string_to_s31", ":ability_to_replace"),
			(display_message, "@DEBUG (Abilities): {s32} removed ability '{s31}' from slot {reg31}.", gpu_debug),
		(else_try),
			(ge, DEBUG_TROOP_ABILITIES, 2),
			(eq, ":assignment_successful", 1),
			(eq, ":block", 0),
			(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"),
			(str_store_troop_name, s32, ":troop_no"),
			(assign, reg31, ":slot_no"),
			(display_message, "@DEBUG (Abilities): {s32} assigned the '{s31}' ability in slot #{reg31}.", gpu_debug),
		(else_try),
			(eq, ":assignment_successful", 0),
			(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"),
			(str_store_troop_name, s32, ":troop_no"),
			(display_message, "@ERROR - Failed to assign ability '{s31}' to troop {s32}.  No available slots.", gpu_red),
		(try_end),
	]),
	
# script_cf_ce_troop_has_requirement
# EXAMPLE: (call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_XXX), # combat_scripts.py - prereq constants in combat_constants.py
("cf_ce_troop_has_requirement",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":prereq", 2),
		
		# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_requirement_1, ":prereq"),
		# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_requirement_2, ":prereq"),
		# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_requirement_3, ":prereq"),
		# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_requirement_4, ":prereq"),
		# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_requirement_5, ":prereq"),
		# (troop_slot_eq, ":troop_no", slot_troop_requirement_6, ":prereq"),
		(assign, ":continue", 0),
		(try_for_range, ":prereq_slot", ce_requirements_begin, ce_requirements_end),
			(troop_slot_eq, ":troop_no", ":prereq_slot", ":prereq"),
			(assign, ":continue", 1),
		(try_end),
		(eq, ":continue", 1),
		
		(try_begin),
			(ge, DEBUG_TROOP_PREREQUISITES, 1),
			(call_script, "script_ce_store_troop_requirement_string_to_s31", ":prereq"),
			(str_store_troop_name, s32, ":troop_no"),
			(display_message, "@DEBUG (Abilities): {s32} found to have the '{s31}' prerequisite.", gpu_debug),
		(try_end),
		
	]),
	
# script_ce_assign_troop_requirement
# EXAMPLE: (call_script, "script_ce_assign_troop_requirement", ":troop_no", PREREQ_XXX, PREREQ_TO_REPLACE), # combat_scripts.py - prereq constants in combat_constants.py
("ce_assign_troop_requirement",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":prereq", 2),
		(store_script_param, ":prereq_to_replace", 3),
		
		# Make sure we aren't assigning the same requirement twice.
		# (try_begin),
			# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_requirement_1, ":prereq"),
			# (this_or_next|troop_slot_eq, ":troop_no", slot_troop_requirement_2, ":prereq"),
			# (troop_slot_eq, ":troop_no", slot_troop_requirement_3, ":prereq"),
			# (assign, ":block", 1),
		# (else_try),
			# (assign, ":block", 0),
		# (try_end),
		(assign, ":block", 0),
		(try_for_range, ":prereq_slot", ce_requirements_begin, ce_requirements_end),
			(troop_slot_eq, ":troop_no", ":prereq_slot", ":prereq"),
			(assign, ":block", 1),
		(try_end),
		
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_requirement_1, ":prereq_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 1),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_requirement_1, ":prereq"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_requirement_1, PREREQ_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_requirement_2, ":prereq_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 2),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_requirement_2, ":prereq"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_requirement_2, PREREQ_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_requirement_3, ":prereq_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 3),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_requirement_3, ":prereq"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_requirement_3, PREREQ_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_requirement_4, ":prereq_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 4),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_requirement_4, ":prereq"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_requirement_4, PREREQ_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_requirement_5, ":prereq_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 5),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_requirement_5, ":prereq"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_requirement_5, PREREQ_UNASSIGNED),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_requirement_6, ":prereq_to_replace"),
			(assign, ":assignment_successful", 1),
			(assign, ":slot_no", 6),
			(try_begin),
				(eq, ":block", 0),
				(troop_set_slot, ":troop_no", slot_troop_requirement_6, ":prereq"),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_requirement_6, PREREQ_UNASSIGNED),
			(try_end),
		(else_try),
			## ERROR - No available slots for assignment.
			(assign, ":assignment_successful", 0),
			(assign, ":slot_no", 0),
		(try_end),
		
		
		(try_begin),
			(ge, DEBUG_TROOP_PREREQUISITES, 2),
			(eq, ":assignment_successful", 1),
			(eq, ":block", 1),
			(call_script, "script_ce_store_troop_requirement_string_to_s31", ":prereq"),
			(str_store_troop_name, s32, ":troop_no"),
			(assign, reg31, ":slot_no"),
			(display_message, "@DEBUG (Abilities): {s32} already had '{s31}'.", gpu_debug),
			(neq, ":prereq_to_replace", PREREQ_UNASSIGNED),
			(call_script, "script_ce_store_troop_requirement_string_to_s31", ":prereq_to_replace"),
			(display_message, "@DEBUG (Abilities): {s32} removed prereq '{s31}' from slot {reg31}.", gpu_debug),
		(else_try),
			(ge, DEBUG_TROOP_PREREQUISITES, 2),
			(eq, ":assignment_successful", 1),
			(eq, ":block", 0),
			(call_script, "script_ce_store_troop_requirement_string_to_s31", ":prereq"),
			(str_store_troop_name, s32, ":troop_no"),
			(assign, reg31, ":slot_no"),
			(display_message, "@DEBUG (Abilities): {s32} assigned the '{s31}' prerequisite in slot #{reg31}.", gpu_debug),
		(else_try),
			(eq, ":assignment_successful", 0),
			(call_script, "script_ce_store_troop_requirement_string_to_s31", ":prereq"),
			(str_store_troop_name, s32, ":troop_no"),
			(display_message, "@ERROR - Failed to assign prerequisite '{s31}' to troop {s32}.  No available slots.", gpu_red),
		(try_end),
	]),
	
# script_ce_wipe_troop_prerequisies_and_abilities
# EXAMPLE: (call_script, "script_ce_wipe_troop_prerequisies_and_abilities", ":troop_no"), # combat_scripts.py
("ce_wipe_troop_prerequisies_and_abilities",
    [
		(store_script_param, ":troop_no", 1),
		
		(troop_set_slot, ":troop_no", slot_troop_unique_location, -1),
		(try_for_range, ":prereq_slot", ce_requirements_begin, ce_requirements_end),
			(troop_set_slot, ":troop_no", ":prereq_slot", PREREQ_UNASSIGNED),
		(try_end),
		(try_for_range, ":ability_slot", abilities_begin, abilities_end),
			(troop_set_slot, ":troop_no", ":ability_slot", BONUS_UNASSIGNED),
		(try_end),
	]),
	
# script_ce_count_troop_abilities
# PURPOSE: Counts how many abilities a troop has.  This is used for in-game balancing and display on the dynamic troop trees presentation.
# EXAMPLE: (call_script, "script_ce_count_troop_abilities", ":troop_no"), # combat_scripts.py - prereq constants in combat_constants.py
("ce_count_troop_abilities", 
	[
		(store_script_param, ":troop_no", 1),
		
		(assign, ":count", 0),
		(try_for_range, ":slot_no", abilities_begin, abilities_end),
			(neg|troop_slot_eq, ":troop_no", ":slot_no", BONUS_UNASSIGNED),
			(val_add, ":count", 1),
		(try_end),
		(assign, reg1, ":count"),
	]),
	
# script_ce_count_troop_prerequisites
# PURPOSE: Counts how many abilities a troop has.  This is used for in-game balancing and display on the dynamic troop trees presentation.
# EXAMPLE: (call_script, "script_ce_count_troop_prerequisites", ":troop_no"), # combat_scripts.py - prereq constants in combat_constants.py
("ce_count_troop_prerequisites", 
	[
		(store_script_param, ":troop_no", 1),
		
		(assign, ":count", 0),
		(try_for_range, ":slot_no", ce_requirements_begin, ce_requirements_end),
			(neg|troop_slot_eq, ":troop_no", ":slot_no", PREREQ_UNASSIGNED),
			(val_add, ":count", 1),
		(try_end),
		(assign, reg1, ":count"),
	]),
	
# script_ce_store_troop_requirement_string_to_s31
# EXAMPLE: (call_script, "script_ce_store_troop_requirement_string_to_s31", PREREQ_XXX), # combat_scripts.py - prereq constants in combat_constants.py
("ce_store_troop_requirement_string_to_s31",
    [
		(store_script_param, ":prereq", 1),
		
		(try_begin),
			(this_or_next|eq, ":prereq", PREREQ_UNIQUE_LOCATION),
			(eq, ":prereq", PREREQ_UNIQUE_LOCATION_UPGRADE),
			(str_store_string, s31, "@UNIQUE_LOCATION"),
		(else_try),
			(eq, ":prereq", PREREQ_ELITE_MERCENARY),
			(str_store_string, s31, "@ELITE_MERCENARY"),
		(else_try),
			(eq, ":prereq", PREREQ_OWNER_ONLY),
			(str_store_string, s31, "@OWNER_ONLY"),
		(else_try),
			(eq, ":prereq", PREREQ_FRIEND),
			(str_store_string, s31, "@FRIEND"),
		(else_try),
			(eq, ":prereq", PREREQ_ALLY),
			(str_store_string, s31, "@ALLY"),
		(else_try),
			(eq, ":prereq", PREREQ_DISHONORABLE),
			(str_store_string, s31, "@DISHONORABLE"),
		(else_try),
			(eq, ":prereq", PREREQ_AFFILIATED),
			(str_store_string, s31, "@AFFILIATED"),
		(else_try),
			(eq, ":prereq", PREREQ_CHARTERED),
			(str_store_string, s31, "@CHARTERED"),
		(else_try),
			(eq, ":prereq", PREREQ_LIEGE_RELATION),
			(str_store_string, s31, "@LIEGE RELATION"),
		(else_try),
			(eq, ":prereq", PREREQ_DISREPUTABLE),
			(str_store_string, s31, "@DISREPUTABLE"),
		(else_try),
			(eq, ":prereq", PREREQ_EXPENSIVE),
			(str_store_string, s31, "@EXPENSIVE"),
		(else_try), 
			### DEFAULT RESPONSE ###
			(str_store_string, s31, "@UNDEFINED"),
		(try_end),
		
	]),
	
# script_ce_store_troop_ability_string_to_s31
# EXAMPLE: (call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", BONUS_XXX), # combat_scripts.py - ability constants in combat_constants.py
("ce_store_troop_ability_string_to_s31",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":ability", 2),
		
		(try_begin),
			(is_between, ":troop_no", companions_begin, companions_end),
			(str_store_string, s2, "@companion"),
		(else_try),
			(str_store_string, s2, "@troop"),
		(try_end),
		(troop_get_type, reg1, ":troop_no"),
		(str_store_string, s3, "@{reg1?her:his}"),
		(str_store_string, s4, "@{reg1?she:he}"),
		
		# s1  = Short description for when companions unlock an ability and what is shown in the character notes.
		# s31 = Short name for the ability.
		# s32 = Longer description for when the player is viewing the ability in the ability selection UI.
		
		(try_begin),
			(eq, ":ability", BONUS_UNASSIGNED),
			(str_store_string, s31, "@UNASSIGNED"),
			(str_store_string, s1, "@None."),
			(str_store_string, s32, "@You currently have no ability selected.  To select \
									^an ability click one of the ability names listed to \
									^the right."),
		(else_try),
			(eq, ":ability", BONUS_SHIELD_BASHER),
			(str_store_string, s31, "@SHIELD_BASHER"),
			(str_store_string, s1, "@This {s2} knows how to turn their shield into an offensive weapon knocking {s3} enemies prone."),
			(str_store_string, s32, "@Undefined"), # Not a player ability.
		(else_try),
			(eq, ":ability", BONUS_ENDURANCE),
			(str_store_string, s31, "@ENDURANCE"),
			(str_store_string, s1, "@This {s2} is conditioned for longer sprinting, but cannot run quite as fast as {s3} peers."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You gain +40 to your maximum stamina.\
									^^Effect #2:\
									^Your maximum sprinting speed is reduced \
									^by 20%.\
									^^Effect #3:\
									^The cooldown before stamina recover begins\
									^is reduced by 3 seconds.\
									^^Effect #4:\
									^The weight used for calculating encumbrance \
									^is reduced by 1 for every 3 points of \
									^Strength that you possess."),
		(else_try),
			(eq, ":ability", BONUS_INSPIRING),
			(str_store_string, s31, "@INSPIRING"),
			(str_store_string, s1, "@This {s2} inspires members of the party, keeping morale higher based upon the Leadership skill."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^Effect #1:\
									^You increase the morale of your party \
									^members by +2 for every point of the \
									^Leadership skill that you possess."),
		(else_try),
			(eq, ":ability", BONUS_TAX_COLLECTOR),
			(str_store_string, s31, "@TAX_COLLECTOR"),
			(str_store_string, s1, "@This {s2} is especially effective at reducing tax inefficiency within a city {s4} is garrisoned in."),
			(str_store_string, s32, "@Undefined"), # Not a player ability.
		(else_try),
			(eq, ":ability", BONUS_COMMANDING_PRESENCE),
			(str_store_string, s31, "@COMMANDING_PRESENCE"),
			(str_store_string, s1, "@This {s2}'s calm charisma emboldens the fighting spirit of nearby troops."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^Effect #1:\
									^This ability allows you to improve the health\
									^regeneration of all nearby allies by 2% + 1%\
									^for every 2 points of Leadership.  This health\
									^regeneration effect is received when the nearby\
									^troop kills or wounds an opponent.\
									^^Note: ^The originator of this effect does not\
									^benefit from it."),
		(else_try),
			(eq, ":ability", BONUS_HARDY),
			(str_store_string, s31, "@HARDY"),
			(str_store_string, s1, "@This {s2} is more resilient and recovers health quicker in combat from defeating enemies."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^This benefit improves your health regeneration\
									^by 0.5% per point of Ironflesh.  The health\
									^regeneration effect is received when you kill or\
									^wound an opponent."),
		(else_try),
			(eq, ":ability", BONUS_AGILE_RIDER),
			(str_store_string, s31, "@AGILE_RIDER"),
			(str_store_string, s1, "@This {s2} is a better rider and will no longer take falling damage when unhorsed."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^With this ability you will receive no falling\
									^damage when you are unhorsed in combat.\
									^^Effect #2:\
									^You ignore any encumbrance penalties to the\
									^Riding skill."),
		(else_try),
			(eq, ":ability", BONUS_SPRINTER),
			(str_store_string, s31, "@SPRINTER"),
			(str_store_string, s1, "@This {s2} is much quicker on the battlefield able to run faster, but tires quicker."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You can sprint 50% faster.\
									^^Effect #2:\
									^The maximum sprinting speed is increased by\
									^30%.\
									^^Effect #3:\
									^Your maximum stamina is reduced by 20."),
									
		(else_try),
			(eq, ":ability", BONUS_DEDICATED),
			(str_store_string, s31, "@DEDICATED"),
			(str_store_string, s1, "@This {s2} is more committed to your cause and gets along with other troops more easily."),
			(str_store_string, s32, "@Undefined"), # Not a player ability.
		(else_try),
			(eq, ":ability", BONUS_DEVOTED),
			(str_store_string, s31, "@DEVOTED"),
			(str_store_string, s1, "@This {s2} is deeply committed to your cause accepting only half the standard wages."),
			(str_store_string, s32, "@Undefined"), # Not a player ability.
		(else_try),
			(eq, ":ability", BONUS_LOYAL),
			(str_store_string, s31, "@LOYAL"),
			(str_store_string, s1, "@This {s2} is especially loyal and will remain when others desert you."),
			(str_store_string, s32, "@Undefined"), # Not a player ability.
		(else_try),
			(eq, ":ability", BONUS_HUNTER),
			(str_store_string, s31, "@HUNTER"),
			(str_store_string, s1, "@This {s2} is capable of hunting food to provide for the party during travel."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^Effect #1:\
									^You reduce the need to consume food stores by\
									^hunting in the local area.  Success of this\
									^effect is influenced by geographical location.\
									^Adding ranks of Tracking will further increase\
									^your chance of a successful hunt."),
		(else_try),
			(eq, ":ability", BONUS_SUPPLY_RUNNER), # Not a player ability.
			(str_store_string, s31, "@SUPPLY_RUNNER"),
			(str_store_string, s1, "@This {s2} manages to brave the battlefield restocking the quivers of ranged attackers."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_BERSERKER),
			(str_store_string, s31, "@BERSERKER"),
			(str_store_string, s1, "@This {s2} flies into a frenzy gaining additional health during combat based on the Ironflesh skill."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You gain an +X% health for each rank of\
									^Ironflesh upon entering combat due to your\
									^frenzied state.  While under the effects of\
									^this ability you cannot receive any benefits\
									^from the Volley Commander, Tactician or\
									^Sharpshooter effects from nearby allies.\
									^^X% is based upon your mod difficulty setting:\
									^ * +7% / rank in Easy\
									^ * +5% / rank in Normal\
									^ * +4% / rank in Hard\
									^ * +3% / rank in Very Hard"),
		(else_try),
			(eq, ":ability", BONUS_BOUNDLESS_ENDURANCE),
			(str_store_string, s31, "@BOUNDLESS_ENDURANCE"),
			(str_store_string, s1, "@This {s2} is able to run faster and for a longer time then others on the battlefield."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Your sprinting speed is improved by 25%.\
									^^Effect #2:\
									^Your maximum stamina is improved by +20.\
									^^Effect #3:\
									^You become twice as resistant to movement\
									^speed reducing effects due to the combat\
									^hampering system."),
		(else_try),
			(eq, ":ability", BONUS_TACTICIAN),
			(str_store_string, s31, "@TACTICIAN"),
			(str_store_string, s1, "@This {s2} now applies a bonus to the damage of nearby allies based on the Tactics skill."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^Effect #1:\
									^Your grasp of strategy improves the damage\
									^of nearby allies by 3% for each rank in\
									^Tactics.\
									^^Note: ^The originator of this effect does not\
									^benefit from it."),
		(else_try),
			(eq, ":ability", BONUS_TRAILBLAZER), 
			(str_store_string, s31, "@TRAILBLAZER"),
			(str_store_string, s1, "@This {s2} knows how quicken the party's pace by finding the easiest travel paths."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^Effect #1:\
									^Your path-finding skill is enhanced by 2.\
									^^Effect #2:\
									^The number of party members you can conceal\
									^using the Stealthy ability is doubled."),
		(else_try),
			(eq, ":ability", BONUS_BLOODLUST),
			(str_store_string, s31, "@BLOODLUST"),
			(str_store_string, s1, "@This {s2} is a terror on the battlefield, swinging wildly for enhanced damage."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You gain 20% damage at the cost of 10% \
									^accuracy.  For each 1% of health lost you\
									^will gain an additional 1% damage and will\
									^lose 0.5% accuracy.\
									^^Notes: \
									^ * Damage improvement is limited to +45%.\
									^ * Accuracy penalty is limited to -30%."),
		(else_try),
			(eq, ":ability", BONUS_FORTITUDE),
			(str_store_string, s31, "@FORTITUDE"),
			(str_store_string, s1, "@This {s2} is tougher than most and now able to resist the effects of health loss."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You are more adept at resisting the effects\
									^of damage due to the combat hampering system.\
									^When calculating penalties your health is\
									^considered as 40% higher than it actually is.\
									^^Synergy Bonus: (Disciplined)\
									^Effectiveness is increased by +20% health."),
		(else_try),
			(eq, ":ability", BONUS_VOLLEY_COMMANDER),
			(str_store_string, s31, "@VOLLEY_COMMANDER"),
			(str_store_string, s1, "@This {s2} now applies a bonus to the accuracy of nearby allies based on the Tactics skill."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^Effect #1:\
									^Your knowledge of strategy improves the accuracy\
									^rating of nearby allies by 8 for each rank of\
									^Tactics.\
									^^Note: ^The originator of this effect does not\
									^benefit from it."),
		(else_try),
			(eq, ":ability", BONUS_SHARPSHOOTER),
			(str_store_string, s31, "@SHARPSHOOTER"),
			(str_store_string, s1, "@This {s2} has a deadly aim that improves ranged attacks based upon the Weapon Master skill."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Your accuracy rating with ranged weapons is\
									^improved by 20 with an additional +8 per rank\
									^of Weapon Master.\
									^^Synergy Bonus: (Master Archer)\
									^If you also have the Master Archer ability then\
									^the effectiveness of this talent is increased by\
									^+30%."),
		(else_try),
			(eq, ":ability", BONUS_SCAVENGER),
			(str_store_string, s31, "@SCAVENGER"),
			(str_store_string, s1, "@This {s2} is valuable for finding extra battlefield loot and loot of higher quality."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^Effect #1:\
									^Adept at sifting through the remains of a battle\
									^to find equipment worth salvaging, you improve\
									^the amount of loot found by the party for each\
									^rank of Looting."),
		(else_try),
			(eq, ":ability", BONUS_QUICK_STUDY), # Not a player ability.
			(str_store_string, s31, "@QUICK_STUDY"),
			(str_store_string, s1, "@This {s2} is faster at reading books and gains extra experience from party role assignments."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_WATCHFUL_EYE),
			(str_store_string, s31, "@WATCHFUL_EYE"),
			(str_store_string, s1, "@This {s2}'s vigiliance allows your party to handle a greater number of prisoners."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^Effect #1:\
									^You increase the number of prisoners the party\
									^can manage by 3 per rank of Prisoner Management."),
		(else_try),
			(eq, ":ability", BONUS_ESCAPE_ARTIST),
			(str_store_string, s31, "@ESCAPE_ARTIST"),
			(str_store_string, s1, "@This {s2} is talented at escaping captivity and may help others escape as well."),
			(str_store_string, s32, "@Type: Personal Benefit\
									^^Effect #1:\
									^Few rope bonds or even dungeons can hold you for\
									^long.  Your chance of increasing from captivity\
									^is dramatically increased.\
									^^Synergy Bonus: (Stealthy)\
									^If you have the Stealthy ability then you will\
									^also break out any allies captive in the same\
									^location when you escape."),
		(else_try),
			(eq, ":ability", BONUS_ADMINISTRATOR), # Not a player ability.
			(str_store_string, s31, "@ADMINISTRATOR"),
			(str_store_string, s1, "@This {s2} is talented as either a Castle Steward or Captain of the Guard."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_ENGINEER), # Not a player ability.
			(str_store_string, s31, "@ENGINEER"),
			(str_store_string, s1, "@This {s2} is now a capable overseer of construction as Castle Steward."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_SIEGE_GENERAL), # Not a player ability.
			(str_store_string, s31, "@SIEGE_GENERAL"),
			(str_store_string, s1, "@This {s2} is now capable of leading a legendary defense as Captain of the Guard."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_MASTER_BOWMAN),
			(str_store_string, s31, "@MASTER_ARCHER"),
			(str_store_string, s1, "@This {s2}'s ability to deliver punishing shots with a bow are now improved by the Weapon Master skill."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You gain an 8% bonus to damage when wielding\
									^a bow.  This effect is increased by an additional\
									^+2% bonus to damage for each rank of\
									^Weapon Master.\
									^^Synergy Bonus: (Sharpshooter)\
									^If you also have the Sharpshooter ability then\
									^the effectiveness of this talent is increased by\
									^+30%."),
		(else_try),
			(eq, ":ability", BONUS_EFFICIENT), # Not a player ability.
			(str_store_string, s31, "@EFFICIENT"),
			(str_store_string, s1, "@This {s2} now makes for an exceptional Castle Steward."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_CHEF), # Not a player ability.
			(str_store_string, s31, "@CHEF"),
			(str_store_string, s1, "@This {s2} can now maintain stores longer and gain more party morale as storekeeper."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_USEFUL_CONTACTS), # Not a player ability.
			(str_store_string, s31, "@USEFUL_CONTACTS"),
			(str_store_string, s1, "@This {s2} is now considerably more adept at the storekeeper, quartermaster or gaoler roles."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_BLADEMASTER),
			(str_store_string, s31, "@BLADEMASTER"),
			(str_store_string, s1, "@This {s2}'s ferocity with melee cutting weapons is now improved by the Weapon Master skill."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You gain a +2% bonus to damage for each rank of\
									^Weapon Master when wielding a melee cutting\
									^weapon.\
									^^Synergy Bonus: (Savant)\
									^You gain an additional +1% damage for every 2\
									^points of intelligence you have above 10 if\
									^you also possess the Savant ability."),
		(else_try),
			(eq, ":ability", BONUS_CARGOMASTER), # Not a player ability.
			(str_store_string, s31, "@CARGOMASTER"),
			(str_store_string, s1, "@This {s2} is a capable quartermaster knowing how to work the best deals from battlefield loot being sold."),
			(str_store_string, s32, "@Undefined"),
		(else_try),
			(eq, ":ability", BONUS_GRACEFUL_RIDER),
			(str_store_string, s31, "@GRACEFUL_RIDER"),
			(str_store_string, s1, "@This {s2} is adept at avoiding the dangers of pikemen during a charge."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You have a chance to avoid any extra damage\
									^dealt by pikes equal to your horse's maneuverability\
									^+ 3% per rank of the Riding skill.\
									^^Effect #2:\
									^You ignore any encumbrance penalties to the\
									^Horse Archery skill."),
		(else_try),
			(eq, ":ability", BONUS_INDOMITABLE),
			(str_store_string, s31, "@INDOMITABLE"),
			(str_store_string, s1, "@This {s2} can more easily ignore encumbrance penalties based upon strength."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Your strength is considered to be three times\
									^as much when used for calculations related to\
									^encumbrance penalties."),
		(else_try),
			(eq, ":ability", BONUS_NIMBLE),
			(str_store_string, s31, "@NIMBLE"),
			(str_store_string, s1, "@This {s2} can more easily ignore encumbrance penalties based upon agility."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Your agility is considered to be three times\
									^as much when used for calculations related to\
									^encumbrance penalties."),
		(else_try),
			(eq, ":ability", BONUS_STEALTHY),
			(str_store_string, s31, "@STEALTHY"),
			(str_store_string, s1, "@This {s2} can hide smaller parties from being spotted during travel."),
			(str_store_string, s32, "@Type: Party Benefit\
									^^The base chance of evading detection of a hostile\
									^party is 100% - 4% for each troop in your party.\
									^^Effect #1:\
									^^ * Each troop with this ability reduces your chance of\
									^   your party being detected by 3%.\
									^^ * A companion or player with this ability reduces \
									^   the chance of your party being detected by 2% \
									^   per rank of Spotting and Tracking. (Minimum +3%)\
									^^Effect #2:\
									^When escaping captivity through use of the Escape\
									^Artist talent, this ability allows you to free any\
									^other allies held at the same location.\
									^^Synergy Bonus: (Trailblazer)\
									^The number of troops concealed by this talent is\
									^doubled if you also possess the Trailblazing ability."),
		(else_try),
			(eq, ":ability", BONUS_STORYTELLER),
			(str_store_string, s31, "@STORYTELLER"),
			(str_store_string, s1, "@This {s2} is adept at boosting your renown with retelling the tales of your exploits."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^The renown you gain from combat is increased by 2\
									^per rank of Persuasion.  This effect may not exceed\
									^a total of +15 renown per battle."),
		
		(else_try),
			(eq, ":ability", BONUS_SILVER_TONGUED),
			(str_store_string, s31, "@SILVER_TONGUED"),
			(str_store_string, s1, "@This {s2} is now more convincing when making attempts at persuasion."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^Options to persuade individuals during dialog \
									^encountersalways appear regardless of other \
									^prerequisites.\
									^^Effect #2:\
									^The chances of successfully persuading a target is \
									^increased by 25%.  This effects stacks with benefits \
									^gained from the Persuasion skill.  This effect is \
									^reduced to +15% when convincing lords to join your \
									^faction."),
		
		(else_try),
			(eq, ":ability", BONUS_SAVAGE_BASH),
			(str_store_string, s31, "@SAVAGE_BASH"),
			(str_store_string, s1, "@This {s2} can now deliver shield bashes with devasting power."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Your shield bash attempts now apply +2 damage per\
									^point of Strength and per rank of Shield.  This\
									^damage is mitigated normally by armor reducing\
									^its effectiveness."),
		
		(else_try),
			(eq, ":ability", BONUS_THRIFTY),
			(str_store_string, s31, "@THRIFTY"),
			(str_store_string, s1, "@This {s2} sees how far above or below the average price a good is."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^Tooltips for trade goods will now display how\
									^far above or below the base price those items\
									^are.\
									^^Effect #2:\
									^A notification will be added to the message log\
									^whenever the inventories of trade good merchants\
									^are reset.\
									^^Effect #3:\
									^Trade goods that are used in an enterprise that\
									^you currently own will now display this."),
		
		(else_try),
			(eq, ":ability", BONUS_SAVANT),
			(str_store_string, s31, "@SAVANT"),
			(str_store_string, s1, "@This {s2} has become an incredibly quick learner."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^Extra experience gained from having a high\
									^Intelligence is increased by 50%."),
		
		(else_try),
			(eq, ":ability", BONUS_RALLYING_FIGURE),
			(str_store_string, s31, "@RALLYING_FIGURE"),
			(str_store_string, s1, "@This {s2} can gather a greater host of men then most peers."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^Each rank of Leadership that you possess\
									^contributes an extra +3 troops to your\
									^maximum party limit.\
									^^Effect #2:\
									^Your morale bonus due to Leadership is\
									^improved by +2 per rank."),
		
		(else_try),
			(eq, ":ability", BONUS_WHOLESALER),
			(str_store_string, s31, "@WHOLESALER"),
			(str_store_string, s1, "@This {s2} can trade more of a single good without penalty."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^This talent reduces the change in purchase \
									^or sale price of an item due to selling \
									^multiple copies of it in the same location \
									^15% per rank of your Trade skill."), 
		
		(else_try),
			(eq, ":ability", BONUS_SECOND_WIND),
			(str_store_string, s31, "@SECOND WIND"),
			(str_store_string, s1, "@This {s2} can quickly move from one enemy to the next."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^Whenever you defeat an enemy in combat your\
									^current stamina is increased by 15.\
									^^Effect #2:\
									^Whenever you defeat an enemy in combat your\
									^cooldown for recovering stamina will be\
									^immediately reset."), 
		
		(else_try),
			(eq, ":ability", BONUS_DISCIPLINED),
			(str_store_string, s31, "@DISCIPLINED"),
			(str_store_string, s1, "@This {s2} has learned to ignore minor wounds through mental discipline."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^Combat health is increased by 1 for every\
									^2 points of intelligence you have above 8.\
									^This effect cannot combine with the health\
									^granted by the Berserker ability.\
									^^Effect #2:\
									^You are more adept at resisting the effects\
									^of damage due to the combat hampering system.\
									^When calculating penalties your health is\
									^considered as 20% higher than it actually is.\
									^^Synergy Bonus: (Fortitude)\
									^The minimum requirement of 8 intelligence is\
									^removed."),
		
		(else_try),
			(eq, ":ability", BONUS_STEADY_AIM),
			(str_store_string, s31, "@STEADY AIM"),
			(str_store_string, s1, "@This {s2} has learned to pick shots carefully for maximum damage."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Increases the damage of the next bow or crossbow\
									^attack you make by +2 per second up to a maximum \
									^of half your Strength value.  25 STR = +12 damage \
									^after a 6 second pause.\
									^^Synergy (Sharpshooter):\
									^Rate of damage increase is improved to +3 damage\
									^per second.\
									^^Synergy (Master Archer):\
									^Upper limit of damage is improved to 65% of your\
									^Strength value."),
		
		(else_try),
			(eq, ":ability", BONUS_CHARGING_STRIKE),
			(str_store_string, s31, "@CHARGING STRIKE"),
			(str_store_string, s1, "@This {s2} has learned to gain the most advantage from their momentum."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Increases the speed damage bonus of attacks made \
									^while sprinting.  You gain a bonus of 1 damage for\
									^every 4% speed you have above normal.  This effect \
									^is limited to a maximum of 50% of your strength \
									^attribute. \
									^^Synergy (Second Wind):\
									^Your damage bonus is now limited by either your\
									^strength or agility attribute based on whichever\
									^is higher.\
									^^Synergy (Blademaster):\
									^Upper limit of damage is improved to 65% of your\
									^Strength value."),
		
		(else_try),
			(eq, ":ability", BONUS_POISONED_WEAPONS),
			(str_store_string, s31, "@POISONED WEAPONS"),
			(str_store_string, s1, "@This {s2} has mastered the art of crippling enemies with poisoned weapons."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Increases the speed damage bonus of attacks made \
									^Whenever you damage another troop they become \
									^poisoned causing their effective health to be \
									^lowered by 50% (combat hampering).\
									^^Effect #2:\
									^A poisoned enemy loses one health every four \
									^seconds for a total of 20 ticks (80 sec duration).\
									^^Special Note:\
									^Use of this ability will lower your honor by 1\
									^for each battle it is used in to a minimum of -15.\
									^^Special Note:\
									^This ability is disabled in tournaments, arena\
									^matches and while training peasants."),
		
		(else_try),
			(eq, ":ability", BONUS_STEADY_FOOTING),
			(str_store_string, s31, "@STEADY FOOTING"),
			(str_store_string, s1, "@This {s2} is resistant to shield bashing attempts."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^You are able to resist the attempts of other \
									^troops trying to shield bash you.  Your chance\
									^to resist is equal to 40% + 3% for each point \
									^you have in the Strength attribute."),
		
		(else_try),
			(eq, ":ability", BONUS_CHEAP), # Not a player or companion ability.
			(str_store_string, s31, "@CHEAP"),
			(str_store_string, s1, "@Undedescribed"),
			(str_store_string, s32, "@Undefined"),
		
		(else_try),
			(eq, ":ability", BONUS_TIGHT_FORMATION), # Not a player or companion ability.
			(str_store_string, s31, "@TIGHT FORMATION"),
			(str_store_string, s1, "@Undedescribed"),
			(str_store_string, s32, "@Undefined"),
		
		(else_try),
			(eq, ":ability", BONUS_RAPID_RELOAD),
			(str_store_string, s31, "@RAPID RELOAD"),
			(str_store_string, s1, "@This {s2} is exceptionally fast at firing ranged weapons."),
			(str_store_string, s32, "@Type: Boost\
									^^Effect #1:\
									^You are adept at quickly firing ranged weapons\
									^by reloading 1% faster for every three points of\
									^proficiency you have in that type of weapon.\
									^^Note: ^This applies only to crossbows, muskets \
									or pistols."),
		
		(else_try),
			(eq, ":ability", BONUS_FIRING_CAPTAIN),
			(str_store_string, s31, "@FIRING CAPTAIN"),
			(str_store_string, s1, "@This {s2} is adept at leading firing volleys that strike rapidly."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Your steady control of troops improves the reload\
									^speed of nearby allies by 20% with an additional +4%\
									^for each rank of Leadership.\
									^^Note: ^The originator of this effect does not\
									^benefit from it.\
									^^Note: ^This applies to all ranged weapons."),
		
		(else_try),
			(eq, ":ability", BONUS_SAVAGERY),
			(str_store_string, s31, "@SAVAGERY"),
			(str_store_string, s1, "@This {s2} is particularly vicious in their attacks striking fear into nearby enemies."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Your proficiency with your wielded weapon strikes\
									^greater fear in nearby enemies whenever you \
									^dispatch one.  Nearby enemies lose an additional \
									^10% + 1% per point of proficiency you have with \
									^your wielded weapon for each opponent you \
									^defeat.\
									^^Note: ^This applies only to melee weapons."),
		
		(else_try),
			(eq, ":ability", BONUS_RALLYING_STRIKE),
			(str_store_string, s31, "@RALLYING STRIKE"),
			(str_store_string, s1, "@This {s2} inspires courage in nearby allies whenever {s4} defeats an enemy."),
			(str_store_string, s32, "@Type: Personal Combat\
									^^Effect #1:\
									^Whenever you strike an opponent down in during \
									^combat all nearby allies gain an increased \
									^amount of courage from your actions equal to \
									^20% + 10% for each rank of Leadership that \
									^you possess. \
									^^Synergy (Inspiring):\
									^Your courage boosting effect is increased by +30%.\
									^^Note: ^This applies to all ranged weapons."),
		
		(else_try), 
			### DEFAULT RESPONSE ### 
			(str_store_string, s31, "@UNDEFINED"),
			(str_store_string, s1, "@Undescribed."),
			(str_store_string, s32, "@Undefined"),
		(try_end),
	]),
	
# script_ce_reset_troop_abilities
# PURPOSE: Handles resetting a troop's abilities for reselection.
# EXAMPLE: (call_script, "script_ce_reset_troop_abilities", ":troop_no"), # combat_scripts.py
("ce_reset_troop_abilities",
    [
		(store_script_param, ":troop_no", 1),
		
		(try_for_range, ":ability_slot", abilities_begin, abilities_end),
			(troop_set_slot, ":troop_no", ":ability_slot", BONUS_UNASSIGNED),
		(try_end),
		# Handle notification.
		(try_begin),
			(main_party_has_troop, ":troop_no"),
			(troop_get_type, reg1, ":troop_no"),
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(str_store_string, s1, "@You have"),
				(str_store_string, s3, "@your"),
			(else_try),
				(str_store_troop_name, s2, ":troop_no"),
				(str_store_string, s1, "@{s2} has"),
				(str_store_string, s3, "@{reg1?her:his}"),
			(try_end),
			(display_message, "@{s1} reset all of {s3} abilities reset.", gpu_green),
		(try_end),
	]),
	
# script_ce_note_describe_troop_ability
# EXAMPLE: (call_script, "script_ce_note_describe_troop_ability", ":troop_no", slot_troop_ability_1), # combat_scripts.py - ability constants in combat_constants.py
("ce_note_describe_troop_ability",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":ability_slot", 2),
		
		(try_begin),
			(troop_get_slot, ":ability", ":troop_no", ":ability_slot"),
			
			(store_sub, ":offset", slot_troop_ability_1, slot_troop_requirement_1), # Should be -3
			(store_sub, ":prereq_slot", ":ability_slot", ":offset"),
			(troop_get_slot, ":ability_to_unlock", ":troop_no", ":prereq_slot"),
			(neq, ":ability_to_unlock", BONUS_UNASSIGNED),
			
			(try_begin),
				(is_between, ":troop_no", companions_begin, companions_end),
				(str_store_string, s2, "@companion"),
			(else_try),
				(str_store_string, s2, "@troop"),
			(try_end),
			(troop_get_type, reg1, ":troop_no"),
			(str_store_string, s3, "@{reg1?her:his}"),
			(str_store_string, s4, "@{reg1?she:he}"),
			
			(str_clear, s41), # Holds the information on the ability.
			(str_clear, s42), # Holds the unlocking level of the ability.
			(str_clear, s43), # Holds the name of the ability.
			
			## CHECK IF ABILITY NEEDS TO BE UNLOCKED.
			(try_begin),
				(troop_slot_eq, ":troop_no", ":ability_slot", BONUS_UNASSIGNED),
				(try_begin),
					(ge, ":ability_slot", slot_troop_ability_1),
					(assign, reg31, 5),
					(ge, ":ability_slot", slot_troop_ability_2),
					(assign, reg31, 12),
					(ge, ":ability_slot", slot_troop_ability_3),
					(assign, reg31, 20),
				(try_end),
				(str_store_string, s42, "@(Unlocked at Level {reg31})"),
			(else_try),
				(str_clear, s42),
			(try_end),
			
			(try_begin),
				(eq, ":ability", BONUS_UNASSIGNED),
				(assign, ":ability", ":ability_to_unlock"),
			(try_end),
			(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"),
			
		(else_try),
			(str_clear, s41),
			(str_store_string, s31, "@No Ability Designated"),
			(str_clear, s1),
			(str_clear, s42),
			(assign, reg41, 0),
		(try_end),
	]),
	
# script_cf_ce_player_can_use_ability
# EXAMPLE: (call_script, "script_cf_ce_player_can_use_ability", ":ability_no", ":desired"), # combat_scripts.py
("cf_ce_player_can_use_ability",
    [
		(store_script_param, ":ability_no", 1),
		(store_script_param, ":desired", 2),
		
		(assign, ":player_can_use", 0),
		## ABILITIES NOT DESIGNED FOR PLAYER USE.
		(try_begin),
			(neq, ":ability_no", BONUS_UNASSIGNED),
			(neq, ":ability_no", BONUS_SHIELD_BASHER),
			(neq, ":ability_no", BONUS_TAX_COLLECTOR),
			(neq, ":ability_no", BONUS_DEDICATED),
			(neq, ":ability_no", BONUS_DEVOTED),
			(neq, ":ability_no", BONUS_LOYAL),
			(neq, ":ability_no", BONUS_SUPPLY_RUNNER),
			(neq, ":ability_no", BONUS_QUICK_STUDY),
			(neq, ":ability_no", BONUS_ADMINISTRATOR),
			(neq, ":ability_no", BONUS_ENGINEER),
			(neq, ":ability_no", BONUS_SIEGE_GENERAL),
			(neq, ":ability_no", BONUS_EFFICIENT),
			(neq, ":ability_no", BONUS_CHEF),
			(neq, ":ability_no", BONUS_USEFUL_CONTACTS),
			(neq, ":ability_no", BONUS_CARGOMASTER),
			(neq, ":ability_no", BONUS_CHEAP),
			(neq, ":ability_no", BONUS_TIGHT_FORMATION),
			(assign, ":player_can_use", 1),
		(try_end),
		
		## ABILITIES NOT ACTUALLY DESIGNED YET.
		(try_begin),
			(eq, ":ability_no", BONUS_ESCAPE_ARTIST),
			(assign, ":player_can_use", 0),
		(try_end),
		
		## Check if the player already has the ability.
		# (try_begin),
			# (call_script, "script_cf_ce_troop_has_ability", "trp_player", ":ability_no"),
			# (assign, ":player_can_use", 0),
		# (try_end),
		
		(assign, ":continue", 0),
		(try_begin),
			(eq, ":desired", ":player_can_use"),
			(assign, ":continue", 1),
		(try_end),
		(eq, ":continue", 1),
	]),
	
# script_ce_inspiring_get_party_bonus
# EXAMPLE: (call_script, "script_ce_inspiring_get_party_bonus", ":party_no"), # combat_scripts.py - prereq constants in combat_constants.py
("ce_inspiring_get_party_bonus",
    [
		(store_script_param, ":party_no", 1),
		
		(party_get_num_companion_stacks, ":num_stacks",":party_no"),
		(assign, ":troop_count", 0),
		(assign, ":inspiring_bonus", 0),
		(assign, reg2, 0), # Value not clamped.
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
			## TROOP EFFECT: BONUS_INSPIRING
			(party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_INSPIRING),
			(val_add, ":troop_count", ":stack_size"),
			(assign, ":inspiring_effect", 2),
			(try_begin),
				## COMPANIONS
				(is_between, ":troop_no", companions_begin, companions_end),
				(store_skill_level, ":inspiring_effect", "skl_leadership", ":troop_no"),
			(else_try),
				## NON-COMPANION HEROES (Player, Lords)
				(troop_is_hero, ":troop_no"),
				(store_skill_level, ":inspiring_effect", "skl_leadership", ":troop_no"),
				(val_mul, ":inspiring_effect", 2),
			(try_end),
			(val_add, ":inspiring_bonus", ":inspiring_effect"),
		(try_end),
		(try_begin),
			(neg|is_between, ":inspiring_effect", 1, 26),
			(assign, reg2, 1),
		(try_end),
		(val_clamp, ":inspiring_effect", 0, 26),
		(assign, reg0, ":inspiring_bonus"),
		(assign, reg1, ":troop_count"),
		(assign, "$morale_modifier_inspiring", reg0),
	]),
	
# script_ce_storyteller_get_party_bonus
# EXAMPLE: (call_script, "script_ce_storyteller_get_party_bonus", ":party_no"), # combat_scripts.py - prereq constants in combat_constants.py
("ce_storyteller_get_party_bonus",
    [
		(store_script_param, ":party_no", 1),
		(store_script_param, ":raw_renown", 2),
		
		(party_get_num_companion_stacks, ":num_stacks",":party_no"),
		(assign, ":renown_bonus_troop", 0),
		(assign, ":renown_bonus_hero", 0),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
			## TROOP EFFECT: BONUS_STORYTELLER
			(party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_STORYTELLER),
			
			(try_begin),
				(this_or_next|eq, ":troop_no", "trp_player"),
				(is_between, ":troop_no", companions_begin, companions_end),
				(store_skill_level, ":renown_troop", "skl_persuasion", ":troop_no"),
				(val_mul, ":renown_troop", 5),
				(val_max, ":renown_troop", 5),
				(val_add, ":renown_bonus_hero", ":renown_troop"),
				(assign, reg39, 1), ## DIAGNOSTIC ##
			(else_try),
				(store_mul, ":renown_troop", 3, ":stack_size"),
				(val_add, ":renown_bonus_troop", ":renown_troop"),
				(assign, reg39, 0), ## DIAGNOSTIC ##
			(try_end),
			
			### DIAGNOSTIC+ ###
			(try_begin),
				(ge, DEBUG_TROOP_ABILITIES, 2),
				(assign, reg31, ":renown_troop"),
				(try_begin),
					(eq, reg39, 1),
					(assign, reg32, ":renown_bonus_hero"),
				(else_try),
					(assign, reg32, ":renown_bonus_troop"),
				(try_end),
				(assign, reg33, ":stack_size"),
				(str_store_troop_name, s31, ":troop_no"),
				(display_message, "@DEBUG (Storyteller): {reg33} {s31} add +{reg31}% to renown.  {reg39?Heroes:Troops} = +{reg32}%", gpu_debug),
			(try_end),
			### DIAGNOSTIC- ###
		(try_end),
		(val_clamp, ":renown_bonus_troop", 0, 101),
		(val_clamp, ":renown_bonus_hero", 0, 101),
		(store_add, ":renown_factor", ":renown_bonus_troop", ":renown_bonus_hero"),
		
		(store_mul, ":renown_bonus", ":raw_renown", ":renown_factor"),
		(val_div, ":renown_bonus", 100),
		
		### DIAGNOSTIC+ ###
		(try_begin),
			(ge, DEBUG_TROOP_ABILITIES, 1),
			(assign, reg32, ":renown_bonus"),
			(assign, reg33, ":renown_factor"),
			(display_message, "@DEBUG (Storyteller): Total renown bonus is {reg32}.  Bonus = +{reg33}%", gpu_debug),
		(try_end),
		### DIAGNOSTIC- ###
		(assign, reg1, ":renown_bonus"),
	]),
	
# script_ce_get_party_stealth_rating
# EXAMPLE: (call_script, "script_ce_get_party_stealth_rating", ":party_no"), # combat_scripts.py
("ce_get_party_stealth_rating",
    [
		(store_script_param, ":party_no", 1),
		
		(party_get_num_companion_stacks, ":num_stacks",":party_no"),
		(assign, ":stealth_from_troops", 0),
		(assign, ":stealth_from_heroes", 0),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
			## TROOP EFFECT: BONUS_STEALTHY
			(party_stack_get_troop_id, ":troop_no", ":party_no", ":stack_no"),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_STEALTHY),
			
			(try_begin),
				(troop_is_hero, ":troop_no"),
				(store_skill_level, ":skill_tracking", "skl_tracking", ":troop_no"),
				(store_skill_level, ":skill_spotting", "skl_spotting", ":troop_no"),
				(store_add, ":hero_stealth", ":skill_tracking", ":skill_spotting"),
				(val_mul, ":hero_stealth", 2),
				(val_max, ":hero_stealth", 3), # Ensure a minimum of 3%.
				## SYNERGY EFFECT: BONUS_TRAILBLAZER
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_TRAILBLAZER),
					(val_mul, ":hero_stealth", 2),
				(try_end),
				(val_add, ":stealth_from_heroes", ":hero_stealth"),
				### DIAGNOSTIC+ ###
				(try_begin),
					(ge, DEBUG_TROOP_ABILITIES, 2),
					(assign, reg31, ":hero_stealth"),
					(assign, reg32, ":stealth_from_heroes"),
					(str_store_troop_name, s31, ":troop_no"),
					(display_message, "@DEBUG (Stealth): {s31} adds +{reg31}% concealment chance.  Heroes = +{reg32}%", gpu_debug),
				(try_end),
				### DIAGNOSTIC- ###
			(else_try),
				(neg|troop_is_hero, ":troop_no"),
				(store_mul, ":troop_stealth", 3, ":stack_size"),
				## SYNERGY EFFECT: BONUS_TRAILBLAZER
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_TRAILBLAZER),
					(val_mul, ":troop_stealth", 2),
				(try_end),
				(val_add, ":stealth_from_troops", ":troop_stealth"),
				### DIAGNOSTIC+ ###
				(try_begin),
					(ge, DEBUG_TROOP_ABILITIES, 2),
					(assign, reg31, ":troop_stealth"),
					(assign, reg32, ":stealth_from_troops"),
					(assign, reg33, ":stack_size"),
					(str_store_troop_name, s31, ":troop_no"),
					(display_message, "@DEBUG (Stealthy): {reg33} {s31} adds +{reg31}% concealment chance.  Troops = +{reg32}%", gpu_debug),
				(try_end),
				### DIAGNOSTIC- ###
			(try_end),
		(try_end),
		(store_add, ":concealment", ":stealth_from_troops", ":stealth_from_heroes"),
		(val_clamp, ":concealment", 0, 101),
		### DIAGNOSTIC+ ###
		(try_begin),
			(ge, DEBUG_TROOP_ABILITIES, 1),
			(assign, reg32, ":concealment"),
			(display_message, "@DEBUG (Stealthy): Total concealment bonus is +{reg32}%.", gpu_debug),
		(try_end),
		### DIAGNOSTIC- ###
		(assign, reg1, ":concealment"),
	]),
	
# script_ce_get_player_party_encumbrance
# EXAMPLE: (call_script, "script_ce_get_player_party_encumbrance"), # combat_scripts.py
("ce_get_player_party_encumbrance",
    [
		(assign, ":cargo", 0),
		(set_fixed_point_multiplier, 100),
		(troop_get_inventory_capacity, ":inv_capacity", "trp_player"),
		(try_for_range, ":inv_slot", 10, ":inv_capacity"),
			(troop_get_inventory_slot, ":item_no", "trp_player", ":inv_slot"),
			(ge, ":item_no", 1),
			(item_get_weight, ":weight", ":item_no"),
			(val_add, ":cargo", ":weight"),
		(try_end),
		(store_div, reg1, ":cargo", 100),
	]),
	
# script_cf_ce_party_avoids_other_party
# EXAMPLE: (call_script, "script_cf_ce_party_avoids_other_party", ":party_sneaking", ":party_spotting"), # combat_scripts.py - prereq constants in combat_constants.py
("cf_ce_party_avoids_other_party",
    [
		(store_script_param, ":party_sneaking", 1),
		(store_script_param, ":party_spotting", 2),
		
		## Get Sneaking DC
		(party_get_num_companions, ":party_sneaking_size", ":party_sneaking"),
		(store_mul, ":sneak_penalty", ":party_sneaking_size", 4),
		(store_sub, ":DC_sneaking", 100, ":sneak_penalty"),
		
		(call_script, "script_ce_get_party_stealth_rating", ":party_sneaking"),
		(assign, ":stealth_rating", reg1),
		(val_add, ":DC_sneaking", ":stealth_rating"),
		
		## Encumbrance: -1% Stealth Chance per 25 lbs. of Cargo.
		(call_script, "script_ce_get_player_party_encumbrance"),
		(assign, ":encumbrance", reg1),
		(val_div, ":encumbrance", 25),
		(val_sub, ":DC_sneaking", ":encumbrance"),
		
		## Distance: -1% Stealth Chance
		(store_distance_to_party_from_party, ":distance", ":party_sneaking", ":party_spotting"),
		(val_sub, ":distance", 10),
		(val_clamp, ":distance", -10, 21),
		(val_add, ":DC_sneaking", ":distance"),
		
		## TODO: Put in a check to have the spotting party reduce your sneak chance by their spotting chance.
		
		(store_random_in_range, ":sneak_attempt", 0, 100),
		
		### DIAGNOSTIC+ ###
		(try_begin),
			(ge, BETA_TESTING_MODE, 1),
			(assign, reg31, ":DC_sneaking"),
			(assign, reg32, ":sneak_penalty"),
			(assign, reg33, ":stealth_rating"),
			(assign, reg34, ":encumbrance"),
			(assign, reg35, ":distance"),
			(display_message, "@DEBUG (Stealthy): {reg31}% DC = 100 - {reg32}% Party Size + {reg33}% Concealment + {reg34}% Encumbrance + {reg35}% Distance.", gpu_debug),
		(try_end),
		### DIAGNOSTIC- ###
		
		(lt, ":sneak_attempt", ":DC_sneaking"),
	]),
	
# script_cf_ce_skill_affected_by_encumbrance
# EXAMPLE: (call_script, "script_cf_ce_skill_affected_by_encumbrance", ":skill_no"), # combat_scripts.py
("cf_ce_skill_affected_by_encumbrance",
    [
		(store_script_param, ":skill_no", 1),
		
		(this_or_next|eq, ":skill_no", "skl_shield"),
		(this_or_next|eq, ":skill_no", "skl_power_draw"),
		(this_or_next|eq, ":skill_no", "skl_riding"),
		(this_or_next|eq, ":skill_no", "skl_horse_archery"),
		(             eq, ":skill_no", "skl_athletics"),
	]),
	
# script_ce_get_troop_encumbrance
("ce_get_troop_encumbrance",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":skill_no", 2),
		
		(assign, ":total_weight", 0),
		(assign, ":encumbrance", 0),
		(assign, ":encumbrance_skill_penalty", 0),
		(assign, ":encumbrance_speed_penalty", 0),
		
		(set_fixed_point_multiplier, 1000),
		
		## WEAPON SLOT #0
		(try_begin),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_item_0),
			(ge, ":item_no", 1),
			(item_get_weight, ":item_weight", ":item_no"),
			(val_add, ":total_weight", ":item_weight"),
			###
			# (assign, reg1, ":item_weight"),
			# (assign, reg2, ":total_weight"),
			# (display_message, "@DEBUG: Weapon #0 weighs {reg1}.  Total weight {reg2}.", gpu_debug),
		(try_end),
		
		## WEAPON SLOT #1
		(try_begin),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_item_1),
			(ge, ":item_no", 1),
			(item_get_weight, ":item_weight", ":item_no"),
			(val_add, ":total_weight", ":item_weight"),
			###
			# (assign, reg1, ":item_weight"),
			# (assign, reg2, ":total_weight"),
			# (display_message, "@DEBUG: Weapon #1 weighs {reg1}.  Total weight {reg2}.", gpu_debug),
		(try_end),
		
		## WEAPON SLOT #2
		(try_begin),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_item_2),
			(ge, ":item_no", 1),
			(item_get_weight, ":item_weight", ":item_no"),
			(val_add, ":total_weight", ":item_weight"),
			###
			# (assign, reg1, ":item_weight"),
			# (assign, reg2, ":total_weight"),
			# (display_message, "@DEBUG: Weapon #2 weighs {reg1}.  Total weight {reg2}.", gpu_debug),
		(try_end),
		
		## WEAPON SLOT #3
		(try_begin),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_item_3),
			(ge, ":item_no", 1),
			(item_get_weight, ":item_weight", ":item_no"),
			(val_add, ":total_weight", ":item_weight"),
			###
			# (assign, reg1, ":item_weight"),
			# (assign, reg2, ":total_weight"),
			# (display_message, "@DEBUG: Weapon #3 weighs {reg1}.  Total weight {reg2}.", gpu_debug),
		(try_end),
		
		## HEAD
		(try_begin),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_head),
			(ge, ":item_no", 1),
			(item_get_weight, ":item_weight", ":item_no"),
			(val_add, ":total_weight", ":item_weight"),
			###
			# (assign, reg1, ":item_weight"),
			# (assign, reg2, ":total_weight"),
			# (display_message, "@DEBUG: Head item weighs {reg1}.  Total weight {reg2}.", gpu_debug),
		(try_end),
		
		## BODY
		(try_begin),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_body),
			(ge, ":item_no", 1),
			(item_get_weight, ":item_weight", ":item_no"),
			(val_add, ":total_weight", ":item_weight"),
			###
			# (assign, reg1, ":item_weight"),
			# (assign, reg2, ":total_weight"),
			# (display_message, "@DEBUG: Body item weighs {reg1}.  Total weight {reg2}.", gpu_debug),
		(try_end),
		
		## FOOT
		(try_begin),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_foot),
			(ge, ":item_no", 1),
			(item_get_weight, ":item_weight", ":item_no"),
			(val_add, ":total_weight", ":item_weight"),
			###
			# (assign, reg1, ":item_weight"),
			# (assign, reg2, ":total_weight"),
			# (display_message, "@DEBUG: Foot item weighs {reg1}.  Total weight {reg2}.", gpu_debug),
		(try_end),
		
		## HAND
		(try_begin),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ek_gloves),
			(ge, ":item_no", 1),
			(item_get_weight, ":item_weight", ":item_no"),
			(val_add, ":total_weight", ":item_weight"),
			###
			# (assign, reg1, ":item_weight"),
			# (assign, reg2, ":total_weight"),
			# (display_message, "@DEBUG: Glove item weighs {reg1}.  Total weight {reg2}.", gpu_debug),
		(try_end),
		
		(val_div, ":total_weight", 10), # Bring the size down due to raising fixed point multiplier to 1000.
		
		## DETERMINE ENCUMBRANCE
		(try_begin),
			(store_div, ":encumbrance", ":total_weight", 100),
			# (try_begin),
				# (gt, ":encumbrance", 100),
				# (val_div, ":encumbrance", 10),
			# (try_end),
			(val_sub, ":encumbrance", 15),
			# (call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_ENDURANCE),
			# (assign, "$recursive_skill_block", "skl_athletics"),
			# (store_skill_level, ":athletics_bonus", "skl_athletics", ":troop_no"),
			# (assign, "$recursive_skill_block", -1),
			# (val_sub, ":encumbrance", ":athletics_bonus"),
		(try_end),
		
		## DETERMINE SKILL PENALTIES
		(store_attribute_level, ":STR", ":troop_no", ca_strength),
		(val_div, ":STR", 2),
		(store_attribute_level, ":AGI", ":troop_no", ca_agility),
		(val_div, ":AGI", 2),
		
		## TROOP EFFECT: BONUS_ENDURANCE
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_ENDURANCE),
			(store_attribute_level, ":STR_temp", ":troop_no", ca_strength),
			(val_div, ":STR_temp", 3),
			(val_sub, ":encumbrance", ":STR_temp"),
			(val_max, ":encumbrance", 0),
		(try_end),
		
		## TROOP EFFECT: BONUS_INDOMITABLE
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_INDOMITABLE),
			(val_mul, ":STR", 3),
		(try_end),
		
		## TROOP EFFECT: BONUS_NIMBLE
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_NIMBLE),
			(val_mul, ":AGI", 3),
		(try_end),
		
		(try_begin), ### SHIELD ###
			(eq, ":skill_no", "skl_shield"),
			(store_sub, ":penalty", ":encumbrance", ":STR"),
			(val_div, ":penalty", 8),
			(assign, ":encumbrance_skill_penalty", ":penalty"),
			# Diagnostic
			(assign, reg31, ":encumbrance_skill_penalty"),
			(str_store_string, s32, "@Shield (-{reg31})"),
		(else_try), ### POWER DRAW ###
			(eq, ":skill_no", "skl_power_draw"),
			(store_add, ":combined", ":STR", ":AGI"),
			(val_div, ":combined", 2),
			(store_sub, ":penalty", ":encumbrance", ":combined"),
			(val_div, ":penalty", 6),
			(assign, ":encumbrance_skill_penalty", ":penalty"),
			# Diagnostic
			(assign, reg31, ":encumbrance_skill_penalty"),
			(str_store_string, s32, "@Power Draw (-{reg31})"),
		(else_try), ### RIDING ###
			(eq, ":skill_no", "skl_riding"),
			(store_sub, ":penalty", ":encumbrance", ":AGI"),
			(val_div, ":penalty", 12),
			(assign, ":encumbrance_skill_penalty", ":penalty"),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_AGILE_RIDER),
				(assign, ":encumbrance_skill_penalty", 0),
			(try_end),
			# Diagnostic
			(assign, reg31, ":encumbrance_skill_penalty"),
			(str_store_string, s32, "@Riding (-{reg31})"),
		(else_try), ### HORSE ARCHERY ###
			(eq, ":skill_no", "skl_horse_archery"),
			(store_sub, ":penalty", ":encumbrance", ":AGI"),
			(val_div, ":penalty", 6),
			(assign, ":encumbrance_skill_penalty", ":penalty"),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_GRACEFUL_RIDER),
				(assign, ":encumbrance_skill_penalty", 0),
			(try_end),
			# Diagnostic
			(assign, reg31, ":encumbrance_skill_penalty"),
			(str_store_string, s32, "@Horse Archery (-{reg31})"),
		(else_try), ### ATHLETICS ###
			(eq, ":skill_no", "skl_athletics"),
			(store_add, ":combined", ":STR", ":AGI"),
			(val_div, ":combined", 2),
			(store_sub, ":penalty", ":encumbrance", ":combined"),
			(val_div, ":penalty", 8),
			(assign, ":encumbrance_skill_penalty", ":penalty"),
			# Diagnostic
			(assign, reg31, ":encumbrance_skill_penalty"),
			(str_store_string, s32, "@Athletics (-{reg31})"),
		(else_try), ## DETERMINE SPEED PENALTY
			(eq, ":skill_no", ENCUMBRANCE_FACTOR_MOVEMENT_SPEED),
			(store_sub, ":encumbrance_speed_penalty", ":encumbrance", ":STR"),
			(val_clamp, ":encumbrance_speed_penalty", 0, 26),
			(assign, reg31, ":encumbrance_speed_penalty"),
			(str_store_string, s32, "@Speed Penalty (-{reg31})"),
		(else_try),
			(str_store_string, s32, "@No Skill Penalty Assigned"),
		(try_end),
		(val_max, ":encumbrance_skill_penalty", 0), # No beneficial penalties.
		
		(store_div, reg1, ":total_weight", 100),
		(store_mod, reg5, ":total_weight", 100),
		(assign, reg2, ":encumbrance"),
		(assign, reg3, ":encumbrance_skill_penalty"),
		(assign, reg4, ":encumbrance_speed_penalty"),
		
		### DIAGNOSTIC ###
		# (try_begin),
			# (eq, ":troop_no", "trp_player"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (display_message, "@{s31}, weight = {reg1}.{reg5}, encumbrance = {reg2}, {s32}"),
		# (try_end),
	]),
	
# script_ce_set_minimum_skills_for_troop
# PURPOSE: Establishes a hard minimum value for weapon proficiency & tactics to be used with traits that make use of this skill.
# EXAMPLE: (call_script, "script_ce_set_minimum_skills_for_troop", ":troop_no"), # combat_scripts.py
("ce_set_minimum_skills_for_troop",
    [
		(store_script_param, ":troop_no", 1),
		
		(troop_get_slot, ":tier", ":troop_no", slot_troop_tier),
		
		## BLADEMASTER - Improves weapon mastery.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BLADEMASTER),
			(store_skill_level, ":skill", "skl_weapon_master", ":troop_no"),
			(lt, ":skill", ":tier"),
			(troop_set_skill, ":troop_no", "skl_weapon_master", ":tier"),
		(try_end),
		
		## SHARPSHOOTER - Improves weapon mastery.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SHARPSHOOTER),
			(store_skill_level, ":skill", "skl_weapon_master", ":troop_no"),
			(lt, ":skill", ":tier"),
			(troop_set_skill, ":troop_no", "skl_weapon_master", ":tier"),
		(try_end),
		
		## MASTER BOWMAN - Improves weapon mastery.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_MASTER_BOWMAN),
			(store_skill_level, ":skill", "skl_weapon_master", ":troop_no"),
			(lt, ":skill", ":tier"),
			(troop_set_skill, ":troop_no", "skl_weapon_master", ":tier"),
		(try_end),
		
		## BERSERKER - Improves ironflesh.
		# (try_begin),
			# (call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BERSERKER),
			# (store_skill_level, ":skill", "skl_ironflesh", ":troop_no"),
			# (lt, ":skill", ":tier"),
			# (troop_set_skill, ":troop_no", "skl_ironflesh", ":tier"),
		# (try_end),
		
		## HARDY - Improves ironflesh.
		# (try_begin),
			# (call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_HARDY),
			# (store_skill_level, ":skill", "skl_ironflesh", ":troop_no"),
			# (lt, ":skill", ":tier"),
			# (troop_set_skill, ":troop_no", "skl_ironflesh", ":tier"),
		# (try_end),
		
		## COMMANDING PRESENCE - Improves leadership.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_COMMANDING_PRESENCE),
			(store_skill_level, ":skill", "skl_leadership", ":troop_no"),
			(lt, ":skill", ":tier"),
			(troop_set_skill, ":troop_no", "skl_leadership", ":tier"),
		(try_end),
		
		## TACTICIAN - Improves tactics.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_TACTICIAN),
			(store_skill_level, ":skill", "skl_tactics", ":troop_no"),
			(lt, ":skill", ":tier"),
			(troop_set_skill, ":troop_no", "skl_tactics", ":tier"),
		(try_end),
		
		## VOLLEY COMMANDER - Improves tactics.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_VOLLEY_COMMANDER),
			(store_skill_level, ":skill", "skl_tactics", ":troop_no"),
			(lt, ":skill", ":tier"),
			(troop_set_skill, ":troop_no", "skl_tactics", ":tier"),
		(try_end),
		
		## DISCIPLINED - Improves Intelligence.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_DISCIPLINED),
			(store_attribute_level, ":INT", ":troop_no", ca_intelligence),
			(store_add, ":minimum", 10, ":tier"),
			(val_add, ":minimum", ":tier"),
			(lt, ":INT", ":minimum"),
			(troop_set_attribute, ":troop_no", ca_intelligence, ":minimum"),
		(try_end),
	]),
	
# script_cf_ce_agent_is_wielding_weapon_type
# PURPOSE: Fails if the given agent is not wielding the specified weapon type.
# EXAMPLE: (call_script, "script_cf_ce_agent_is_wielding_weapon_type", ":agent_no", ":type"), # combat_scripts.py
("cf_ce_agent_is_wielding_weapon_type",
    [
		(store_script_param, ":agent_no", 1),
		(store_script_param, ":type", 2),
		
		(agent_get_wielded_item, ":item_left", ":agent_no", 0),
		(agent_get_wielded_item, ":item_right", ":agent_no", 1),
		(assign, ":continue", 0),
		(try_begin),
			(ge, ":item_left", 1),
			(item_get_type, ":item_type", ":item_left"),
			(eq, ":item_type", ":type"),
			(assign, ":continue", 1),
		(else_try),
			(ge, ":item_right", 1),
			(item_get_type, ":item_type", ":item_right"),
			(eq, ":item_type", ":type"),
			(assign, ":continue", 1),
		(try_end),
		(eq, ":continue", 1),
	]),
	
# script_cf_ce_troop_has_ability
# EXAMPLE: (call_script, "script_ce_troop_get_bonus_health", ":troop_no"), # combat_scripts.py - ability constants in combat_constants.py
("ce_troop_get_bonus_health",
    [
		(store_script_param, ":troop_no", 1),
		
		(assign, ":extra_health", 0),
		(try_begin),
			(eq, "$enable_combat_abilities", 1),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BERSERKER),
				(store_skill_level, ":extra_health", "skl_ironflesh", ":troop_no"),
				(try_begin),
					(neq, ":troop_no", "trp_player"),
					(neg|is_between, ":troop_no", companions_begin, companions_end),
					(assign, ":difficulty_constant", BERSERKER_BONUS_EASY),
				(else_try),
					(eq, "$mod_difficulty", GAME_MODE_EASY),
					(assign, ":difficulty_constant", BERSERKER_BONUS_EASY),
				(else_try),
					(eq, "$mod_difficulty", GAME_MODE_HARD),
					(assign, ":difficulty_constant", BERSERKER_BONUS_HARD),
				(else_try),
					(eq, "$mod_difficulty", GAME_MODE_VERY_HARD),
					(assign, ":difficulty_constant", BERSERKER_BONUS_VERY_HARD),
				(else_try),
					(assign, ":difficulty_constant", BERSERKER_BONUS_NORMAL),
				(try_end),
				(val_mul, ":extra_health", ":difficulty_constant"),
			(else_try),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_DISCIPLINED),
				(store_attribute_level, ":extra_health", ":troop_no", ca_intelligence),
				## TROOP SYNERGY EFFECT: BONUS_FORTITUDE (+8 INT)
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_FORTITUDE),
				(else_try),
					(val_sub, ":extra_health", 8),
				(try_end),
				(val_div, ":extra_health", 2),
				(val_max, ":extra_health", 0),
			(try_end),
		(try_end),
		(assign, reg1, ":extra_health"),
		# (try_begin),
			# (eq, ":troop_no", "trp_player"),
			# (str_store_troop_name, s31, "trp_player"),
			# (display_message, "@DEBUG (CE): {s31}'s health bonus is {reg1}.", gpu_debug),
		# (try_end),
	]),
	
# script_ce_reset_agent_max_health
# EXAMPLE: (call_script, "script_ce_reset_agent_max_health", ":agent_no"), # combat_scripts.py - ability constants in combat_constants.py
("ce_reset_agent_max_health",
    [
		(store_script_param, ":agent_no", 1),
		
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		(try_begin),
			(eq, 1, 0), # Blocked due to hero health resetting issues after each round.
			(troop_is_hero, ":troop_no"),
			(call_script, "script_ce_troop_get_bonus_health", ":troop_no"), # combat_scripts.py
			(assign, ":extra_health", reg1),
			(store_agent_hit_points, ":base_health", ":agent_no", 1),
			(assign, ":initial_health", ":base_health"),
			(val_sub, ":base_health", ":extra_health"),
			(try_begin),
				(ge, ":initial_health", 1),
				(val_max, ":base_health", 1), # This shouldn't kill a troop.
			(else_try),
				(assign, ":base_health", 0),
			(try_end),
			(agent_set_hit_points, ":agent_no", ":base_health", 1),
			(store_troop_health, ":max_health", ":troop_no", 1),
			(agent_set_max_hit_points, ":agent_no", ":max_health", 1),
	   (try_end),
	]),
	
# script_ce_get_troop_base_movement_speed
# EXAMPLE: (call_script, "script_ce_get_troop_base_movement_speed", ":troop_no", ":info_requested"), # combat_scripts.py - ability constants in combat_constants.py
("ce_get_troop_base_movement_speed",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":info_requested", 2),
		
		(assign, ":total_speed", 100),
		
		## SPEED MODIFICATION: Agility greater than 10 improves base speed.
		(store_attribute_level, ":modifier_agility", ":troop_no", ca_agility),
		(val_sub, ":modifier_agility", 10),
		(val_add, ":total_speed", ":modifier_agility"),
		
		## SPEED MODIFICATION: ENCUMBRANCE (-1.5% per 1 lbs. > 15+(STR/2)
		(assign, ":modifier_encumbrance", 0),
		(try_begin),
			(eq, "$enable_encumbrance", 1),
			(this_or_next|eq, ":info_requested", SPEED_FACTOR_TOTAL),
			(eq, ":info_requested", SPEED_FACTOR_ENCUMBRANCE),
			(call_script, "script_ce_get_troop_encumbrance", ":troop_no", ENCUMBRANCE_FACTOR_MOVEMENT_SPEED),
			(assign, ":modifier_encumbrance", reg4),
			(val_sub, ":total_speed", ":modifier_encumbrance"),
		(try_end),
		
		(try_begin),
			(eq, ":info_requested", SPEED_FACTOR_AGILITY),
			(assign, reg1, ":modifier_agility"),
		(else_try),
			(eq, ":info_requested", SPEED_FACTOR_ENCUMBRANCE),
			(assign, reg1, ":modifier_encumbrance"),
		(else_try),
			(assign, reg1, ":total_speed"),
		(try_end),
	]),
	
# script_ce_draw_stamina_bar
# EXAMPLE: (call_script, "script_ce_draw_stamina_bar"), # combat_scripts.py - ability constants in combat_constants.py
("ce_draw_stamina_bar",
    [
		(assign, ":bar_width", 5650),
		(assign, ":bar_height", 110),
		
		# (display_message, "@DEBUG (Stamina): Stamina bar draw request.", gpu_debug), ## DEBUG: STAMINA_BAR
		(try_begin),
			(eq, "$enable_sprinting", 1), # We're using sprinting.
			(eq, "$block_stamina_bar", 1),
			(eq, "$enable_stamina_bar_ui", 1), # Mod option to block stamina bar appearance.
			(call_script, "script_cf_ce_stamina_bar_has_background_presentation"),
			## stamina bar
			(set_fixed_point_multiplier, 1000),
			(create_mesh_overlay, "$obj_stamina_bar", "mesh_white_plane"),
			(assign, ":color", 0xFFCC6600),
			(try_begin),
				(eq, "$stamina_bar_color", 0), # Muted Gold
				(assign, ":color", 0xFFCC6600),
			(else_try),
				(eq, "$stamina_bar_color", 1), # Blue
				(assign, ":color", gpu_blue),
			(else_try),
				(eq, "$stamina_bar_color", 2), # Green
				(assign, ":color", gpu_green),
			(try_end),
			(overlay_set_color, "$obj_stamina_bar", ":color"),
			# stamina bar position
			(position_set_x, pos1, 866),
			(position_set_y, pos1, 64),
			(overlay_set_position, "$obj_stamina_bar", pos1),
			# stamina bar size
			(position_set_x, pos1, ":bar_width"),
			(position_set_y, pos1, ":bar_height"),
			(overlay_set_size, "$obj_stamina_bar", pos1),
			# (assign, "$obj_stamina_bar", reg5),
			(assign, "$block_stamina_bar", 0),
			
			(try_begin), ### DIAGNOSTIC+ ###
				(ge, DEBUG_STAMINA, 1),
				(assign, reg31, "$block_stamina_bar"),
				(assign, reg32, "$obj_stamina_bar"),
				(display_message, "@DEBUG (Stamina): Stamina bar has been {reg31?BLOCKED:unblocked} @ draw_stamina_bar.  Object #{reg32}", gpu_debug), ## DEBUG: STAMINA_BAR
			(try_end), ### DIAGNOSTIC- ###
		(try_end),
	]),
	

# script_ce_update_stamina_bar
# EXAMPLE: (call_script, "script_ce_update_stamina_bar", ":agent_no"), # combat_scripts.py - ability constants in combat_constants.py
("ce_update_stamina_bar",
    [
		(store_script_param, ":agent_no", 1),
		
		(assign, ":bar_width", 5650),
		(assign, ":bar_height", 110),
		
		(try_begin),
			(eq, "$enable_sprinting", 1), # We're using sprinting.
			(eq, "$block_stamina_bar", 0), # The stamina bar is active.
			(eq, "$enable_stamina_bar_ui", 1), # Mod option to block stamina bar appearance.
			(neq, "$obj_stamina_bar", -1),
			(call_script, "script_cf_ce_stamina_bar_has_background_presentation"),
			
			(set_fixed_point_multiplier, 1000),
			(assign, ":obj_bar", "$obj_stamina_bar"),
			# Figure out what % stamina the agent has.
			(agent_get_slot, ":max_stamina", ":agent_no", slot_agent_max_stamina),
			(agent_get_slot, ":current_stamina", ":agent_no", slot_agent_current_stamina),
			(val_max, ":max_stamina", 1), # prevent div/0 errors.
			(store_mul, ":stamina_percent", ":current_stamina", 100),
			(val_div, ":stamina_percent", ":max_stamina"),
			# FILTER - If our stamina value hasn't really changed let's block it from changing.
			(agent_get_slot, ":last_update", ":agent_no", slot_agent_last_stamina_value),
			(neq, ":stamina_percent", ":last_update"),
			(agent_set_slot, ":agent_no", slot_agent_last_stamina_value, ":stamina_percent"),
			# Convert % stamina into % of the stamina bar's size.
			(store_mul, ":current_width", ":stamina_percent", ":bar_width"),
			(val_div, ":current_width", 100),
			(val_max, ":current_width", 1),
			# Set the stamina bar's size.
			(position_set_x, pos1, ":current_width"),
			(position_set_y, pos1, ":bar_height"),
			(set_fixed_point_multiplier, 1000),
			(overlay_set_size, ":obj_bar", pos1),
		(try_end),
	]),
	
# script_cf_ce_stamina_bar_has_background_presentation
# PURPOSE: Since the stamina bar runs "piggy backed" onto other presentations, it needs to verify at least one of them is active to prevent errors.
# EXAMPLE: (call_script, "script_cf_ce_stamina_bar_has_background_presentation"), # combat_scripts.py - ability constants in combat_constants.py
("cf_ce_stamina_bar_has_background_presentation",
    [
		## Either the ratio bar or tournament HUD needs to be active.
		# (this_or_next|is_presentation_active, "prsnt_troop_ratio_bar"),
		# (is_presentation_active, "prsnt_tpe_team_display"),
		
		## FILTER - See if any background presentation is available for the stamina bar and if not block it from updating.
		(try_begin),
			(this_or_next|presentation_activate, "prsnt_troop_ratio_bar"),
			(presentation_activate, "prsnt_tpe_team_display"),
		(else_try),
			(assign, "$block_stamina_bar", 1),
			(assign, "$obj_stamina_bar", -1),
			(try_begin),
				(ge, DEBUG_STAMINA, 1),
				(assign, reg31, "$block_stamina_bar"),
				(display_message, "@DEBUG (Stamina): Stamina bar has been {reg31?BLOCKED:unblocked} @ update script filter (combat)", gpu_debug), ## DEBUG: STAMINA_BAR
			(try_end),
		(try_end),
		
		(this_or_next|presentation_activate, "prsnt_troop_ratio_bar"),
		(presentation_activate, "prsnt_tpe_team_display"),
		
	]),
	
# script_ce_agent_get_max_stamina
# EXAMPLE: (call_script, "script_ce_agent_get_max_stamina", ":agent_no"), # combat_scripts.py - ability constants in combat_constants.py
("ce_agent_get_max_stamina",
    [
		(store_script_param, ":agent_no", 1),
		
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		
		(assign, ":max_stamina", 20),
		
		# Strength (+2 per point)
		(store_attribute_level, ":STR", ":troop_no", ca_strength),
		(val_mul, ":STR", 2),
		(val_add, ":max_stamina", ":STR"),
		
		# Athletics (+4 per rank)
		(store_skill_level, ":athletics_bonus", "skl_athletics", ":troop_no"),
		(val_mul, ":athletics_bonus", 4),
		(val_add, ":max_stamina", ":athletics_bonus"),
		
		# Ability (BONUS_ENDURANCE)
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_ENDURANCE),
			(val_add, ":max_stamina", 40),
		(try_end),
		
		# Ability (BONUS_BOUNDLESS_ENDURANCE)
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BOUNDLESS_ENDURANCE),
			(val_add, ":max_stamina", 20),
		(try_end),
		
		(val_mul, ":max_stamina", 100), # Converts the significant digit into 1/100ths.
		(agent_set_slot, ":agent_no", slot_agent_max_stamina, ":max_stamina"),
		(agent_set_slot, ":agent_no", slot_agent_current_stamina, ":max_stamina"),
	]),
]


from util_wrappers import *
from util_scripts import *

scripts_directives = [
	# #rename scripts to "insert" switch scripts (see end of scripts[])  
	# [SD_RENAME, "consume_food" , "consume_food_orig"],                                               # Replaced for using the storekeeper role.
	# [SD_RENAME, "cf_player_has_item_without_modifier" , "cf_player_has_item_without_modifier_orig"], # Replaced for using the storekeeper role.
	
	# # HOOK: Alters native script to allow player selected jailer's prisoner management skill to function.
	# [SD_OP_BLOCK_INSERT, "game_get_party_prisoner_limit", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (assign, ":troop_no", "trp_player"), 0, 
		# [(assign, ":troop_no", "$cms_role_jailer"),], 1],
	
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
