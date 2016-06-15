# Tournament Play Enhancements (1.6) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *
from header_presentations import *  # (COMPANIONS OVERSEER MOD)

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [
## TOURNAMENT PLAY ENHANCEMENTS (1.0) begin - Windyplains
# script_TPE_UPDATE_PRESENTATION
  ("tpe_update_presentation",
    [
	
		(try_begin),
			(troop_slot_eq, "trp_tpe_presobj", tpe_options_display_mode, wp_tpe_combat_settings),
			# OBJ 38 - NEVER SPAWN
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_never_spawn),
			(overlay_set_val, "$g_presentation_obj_38", ":status"),
		(try_end),
		
		(try_begin),
			(troop_slot_eq, "trp_tpe_presobj", tpe_options_display_mode, wp_tpe_combat_settings),
			(eq, wp_tpe_mod_opt_actual_gear, 0), # TPE 1.3 + Native Equipment Changes
			# Set the initial checkbox positions
			# OBJ 4 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_lance),
			(overlay_set_val, "$g_presentation_obj_4", ":status"),
			# OBJ 5 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_bow),
			(overlay_set_val, "$g_presentation_obj_5", ":status"),
			# OBJ 6 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_onehand),
			(overlay_set_val, "$g_presentation_obj_6", ":status"),
			# OBJ 7 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_twohand),
			(overlay_set_val, "$g_presentation_obj_7", ":status"),
			# OBJ 8 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_crossbow),
			(overlay_set_val, "$g_presentation_obj_8", ":status"),
			# OBJ 9 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_throwing),
			(overlay_set_val, "$g_presentation_obj_9", ":status"),
			# OBJ 10 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_polearm),
			(overlay_set_val, "$g_presentation_obj_10", ":status"),
			# OBJ 11 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_horse),
			(overlay_set_val, "$g_presentation_obj_11", ":status"),
			# OBJ 12 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_enhanced_horse),
			(overlay_set_val, "$g_presentation_obj_12", ":status"),
			(try_begin),
				(troop_slot_eq, "$g_wp_tpe_troop", slot_troop_tournament_horse, 0),  # Checks if the enhanced horse option should be displayed or not.
				(overlay_set_display, "$g_presentation_obj_12", 0),
			(else_try),
				(overlay_set_display, "$g_presentation_obj_12", 1),
			(try_end),
			# OBJ 13 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_enhanced_armor),
			(overlay_set_val, "$g_presentation_obj_13", ":status"),
			# OBJ 14 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_enhanced_weapons),
			(overlay_set_val, "$g_presentation_obj_14", ":status"),
			# OBJ 15 initialize
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_enhanced_shield),
			(overlay_set_val, "$g_presentation_obj_15", ":status"),
			(try_begin),                                                            # Checks if the enhanced shield option should be displayed or not.
				(troop_slot_eq, "$g_wp_tpe_troop", slot_troop_tournament_onehand, 0),    # Is the player using the 1H + Shield option?
				(troop_slot_eq, "$g_wp_tpe_troop", slot_troop_tournament_throwing, 0),   # Is the player using the Javelin + Shield option?
				(troop_slot_eq, "$g_wp_tpe_troop", slot_troop_tournament_lance, 0),      # Is the player using the Lance + Shield option?
				(overlay_set_display, "$g_presentation_obj_15", 0),
			(else_try),
				(overlay_set_display, "$g_presentation_obj_15", 1),
			(try_end),
			
			# OBJ 24 initialize
			(assign, ":total_options", 0),
			(try_for_range, ":selection", slot_troop_tournament_begin, slot_troop_tournament_end), # Clear out any previously selected options.
				(troop_slot_eq, "$g_wp_tpe_troop", ":selection", 1), # It isn't ON either.
				(val_add, ":total_options", 1),
			(try_end),
			(troop_get_slot, ":status", "$g_wp_tpe_troop", slot_troop_tournament_selections),
			# Error Trap+
			(try_begin),
				(neq, ":status", ":total_options"),
				(assign, reg31, ":status"),
				(assign, reg32, ":total_options"),
				(display_message, "@ERROR - {reg32} options selected, but only {reg31} counted.  Resetting count.", gpu_red),
				(assign, ":status", ":total_options"),
				(troop_set_slot, "$g_wp_tpe_troop", slot_troop_tournament_selections, ":status"),
			(try_end),
			# Error Trap-
			(store_sub, reg0, 3, ":status"),
			(store_sub, reg1, reg0, 1), # plural check.
			(overlay_set_text, "$g_presentation_obj_24", "@You have {reg0} option{reg1?s:} remaining."),
			(try_begin),
				(eq, ":status", 0),
				(troop_set_slot, "$g_wp_tpe_troop", slot_troop_tournament_always_randomize, 1),
			(else_try),
				(troop_set_slot, "$g_wp_tpe_troop", slot_troop_tournament_always_randomize, 0), # Bugfix #1337, v0.23
			(try_end),
			# OBJ 37 initialize
			(try_begin),
				(troop_slot_eq, "$g_wp_tpe_troop", slot_troop_tournament_always_randomize, 1),
				(overlay_set_val, "$g_presentation_obj_37", 1),
			(else_try),
				(overlay_set_val, "$g_presentation_obj_37", 0),
			(try_end),
		(try_end),
	]
  ),
  
# script_TPE_EQUIP_AGENT
# Input: arg1 = troop
  ("tpe_equip_troop",
    [	
		(store_script_param, ":troop", 1),
		
	    # Clear any previous choices
		(call_script, "script_tpe_clear_selections", ":troop"),
		
		# Find the appropriate city settings.
		(store_sub, ":city_settings", "$current_town", towns_begin),
		(val_mul, ":city_settings", 10),
		(store_add, ":slot_lance",    ":city_settings", tdp_val_setting_lance),
		(store_add, ":slot_archery",  ":city_settings", tdp_val_setting_archery),
		(store_add, ":slot_onehand",  ":city_settings", tdp_val_setting_onehand),
		(store_add, ":slot_twohand",  ":city_settings", tdp_val_setting_twohand),
		(store_add, ":slot_crossbow", ":city_settings", tdp_val_setting_crossbow),
		(store_add, ":slot_throwing", ":city_settings", tdp_val_setting_throwing),
		(store_add, ":slot_polearm",  ":city_settings", tdp_val_setting_polearm),
		(store_add, ":slot_horse",    ":city_settings", tdp_val_setting_horse),
		#(store_add, ":slot_outfit",   ":city_settings", tdp_val_setting_outfit),
		(troop_get_slot, ":item_chance_lance",    tpe_settings, ":slot_lance"),
		(troop_get_slot, ":item_chance_archery",  tpe_settings, ":slot_archery"),
		(troop_get_slot, ":item_chance_onehand",  tpe_settings, ":slot_onehand"),
		(troop_get_slot, ":item_chance_twohand",  tpe_settings, ":slot_twohand"),
		(troop_get_slot, ":item_chance_crossbow", tpe_settings, ":slot_crossbow"),
		(troop_get_slot, ":item_chance_throwing", tpe_settings, ":slot_throwing"),
		(troop_get_slot, ":item_chance_polearm",  tpe_settings, ":slot_polearm"),
		(troop_get_slot, ":item_chance_horse",    tpe_settings, ":slot_horse"),
		#(troop_get_slot, ":item_chance_outfit",   tpe_settings, ":slot_outfit"),
		
		(assign, ":choices_taken", 0),
		
		### MELEE WEAPON CHOICE ###
		(assign, ":chance", ":item_chance_polearm"),
		(val_add, ":chance", ":item_chance_onehand"),
		(val_add, ":chance", ":item_chance_twohand"),
		
		# Pick a melee weapon
		(store_random_in_range, ":coin_flip", 1, ":chance"),
		(assign, ":upper_limit", 0),
		(try_begin),
			(assign,  ":lower_limit", 1),
			(val_add, ":upper_limit", ":item_chance_polearm"),
			(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
			(troop_set_slot, ":troop", slot_troop_tournament_polearm, 1),
			(val_add, ":choices_taken", 1),
		(else_try),
			(assign,  ":lower_limit", ":upper_limit"),
			(val_add, ":upper_limit", ":item_chance_twohand"),
			(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
			(troop_set_slot, ":troop", slot_troop_tournament_twohand, 1),
			(val_add, ":choices_taken", 1),
		(else_try),
			# Setup one handed weapon as a default.
			(troop_set_slot, ":troop", slot_troop_tournament_onehand, 1),
			(val_add, ":choices_taken", 1),
		(try_end),
		
		### MOUNT CHECK ###
		(try_begin),
			(ge, ":item_chance_horse", 1),
			(store_random_in_range, ":coin_flip", 1, 100),
			(lt, ":coin_flip", ":item_chance_horse"),
			(troop_set_slot, ":troop", slot_troop_tournament_horse, 1),
			(val_add, ":choices_taken", 1),
		(try_end),
		
		### SECONDARY WEAPON CHOICES ###
		(assign, ":chance", ":item_chance_lance"),
		(val_add, ":chance", ":item_chance_archery"),
		(val_add, ":chance", ":item_chance_crossbow"),
		(val_add, ":chance", ":item_chance_throwing"),
		(val_add, ":chance", ":item_chance_horse"),
		
		# Auxiliary weapon or primary enhancement choice
		(store_random_in_range, ":coin_flip", 1, ":chance"),
		(assign, ":upper_limit", 0),
		(try_begin),
			(assign,  ":lower_limit", 1),
			(val_add, ":upper_limit", ":item_chance_lance"),
			(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
			(troop_set_slot, ":troop", slot_troop_tournament_lance, 1),
			(val_add, ":choices_taken", 1),
		(else_try),
			(assign,  ":lower_limit", ":upper_limit"),
			(val_add, ":upper_limit", ":item_chance_archery"),
			(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
			(troop_set_slot, ":troop", slot_troop_tournament_bow, 1),
			(val_add, ":choices_taken", 1),
		(else_try),
			(assign,  ":lower_limit", ":upper_limit"),
			(val_add, ":upper_limit", ":item_chance_crossbow"),
			(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
			(troop_set_slot, ":troop", slot_troop_tournament_crossbow, 1),
			(val_add, ":choices_taken", 1),
		(else_try),
			(assign,  ":lower_limit", ":upper_limit"),
			(val_add, ":upper_limit", ":item_chance_throwing"),
			(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
			(troop_set_slot, ":troop", slot_troop_tournament_throwing, 1),
			(val_add, ":choices_taken", 1),
		(try_end),
		
		### THIRD WEAPON CHOICES ###
		(assign, ":chance",  25),
		(val_add, ":chance", 25), # Enhanced weapons chance
		(val_add, ":chance", 25), # Enhanced shield chance
		(val_add, ":chance", 25), # Enhanced armor chance
		
		# Last choice for additional enhancement
		(try_for_range, ":unused", 1, 5),
			(lt, ":choices_taken", 3),
			(store_random_in_range, ":coin_flip", 1, ":chance"),
			(assign, ":upper_limit", 0),
			(try_begin),
				(assign,  ":lower_limit", 1),
				(val_add, ":upper_limit", 25),
				(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
				(try_begin),
					(troop_get_slot, ":horse_check", ":troop", slot_troop_tournament_horse),
					(eq, ":horse_check", 0),
					(troop_set_slot, ":troop", slot_troop_tournament_horse, 1),
					(assign, ":last_choice", slot_troop_tournament_horse),
					(val_add, ":choices_taken", 1),
				(else_try),
					(troop_set_slot, ":troop", slot_troop_tournament_enhanced_horse, 1),
					(assign, ":last_choice", slot_troop_tournament_enhanced_horse),
					(val_add, ":choices_taken", 1),
				(try_end),
			(else_try),
				(assign,  ":lower_limit", ":upper_limit"),
				(val_add, ":upper_limit", 25),
				(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
				(troop_set_slot, ":troop", slot_troop_tournament_enhanced_weapons, 1),
				(assign, ":last_choice", slot_troop_tournament_enhanced_weapons),
				(val_add, ":choices_taken", 1),
			(else_try),
				(assign,  ":lower_limit", ":upper_limit"),
				(val_add, ":upper_limit", 25),
				(is_between, ":coin_flip", ":lower_limit", ":upper_limit"),
				(this_or_next|troop_slot_eq, ":troop", slot_troop_tournament_throwing, 1),
				(this_or_next|troop_slot_eq, ":troop", slot_troop_tournament_lance, 1),
				(troop_slot_eq, ":troop", slot_troop_tournament_onehand, 1),
				(troop_set_slot, ":troop", slot_troop_tournament_enhanced_shield, 1),
				(assign, ":last_choice", slot_troop_tournament_enhanced_shield),
				(val_add, ":choices_taken", 1),
			(else_try),
				# Setup enhanced armor as a default.
				(troop_set_slot, ":troop", slot_troop_tournament_enhanced_armor, 1),
				(assign, ":last_choice", slot_troop_tournament_enhanced_armor),
				(val_add, ":choices_taken", 1),
			(try_end),
		(try_end),
		
		(try_begin), # Checks to see if a person has a lance without a horse.
			(troop_slot_eq, ":troop", slot_troop_tournament_lance, 1),
			(troop_slot_eq, ":troop", slot_troop_tournament_horse, 0),
			(troop_set_slot, ":troop", slot_troop_tournament_horse, 1),
			(troop_set_slot, ":troop", ":last_choice", 0),
		(try_end),
		
		(try_begin),
			(neq, ":choices_taken", 3),
			(str_store_troop_name, s1, ":troop"),
			(assign, reg21, ":choices_taken"),
			(display_message, "@ERROR (TPE): {s1} has an invalid number of choices @ {reg21}."),
		(try_end),
		(troop_set_slot, ":troop", slot_troop_tournament_selections, ":choices_taken"),
	]
  ),
  
 
# script_TPE_WEAPON_LOGIC
# Input: arg1 = troop
  ("tpe_weapon_logic",
    [	
		(store_script_param, ":troop", 1),
		
		(assign, ":tally_weapons", 0),
		(assign, ":tally_weapon_slots", 0),
		(assign, ":melee_weapon_check", 0),
		
		(try_for_range, ":weapon_choice", slot_troop_tournament_begin, slot_troop_tournament_horse), # horse is first enhancement after weapons
			(troop_get_slot, ":status", ":troop", ":weapon_choice"),
			(eq, ":status", 1),
			(val_add, ":tally_weapons", 1),
			(try_begin),
				(this_or_next|eq, ":weapon_choice", slot_troop_tournament_onehand),
				(this_or_next|eq, ":weapon_choice", slot_troop_tournament_twohand),
				(eq, ":weapon_choice", slot_troop_tournament_polearm),
				(assign, ":melee_weapon_check", 1),
			(try_end),
			(try_begin),
				(eq, ":weapon_choice", slot_troop_tournament_lance),
				(val_add, ":tally_weapon_slots", 1),
			(else_try),
				(eq, ":weapon_choice", slot_troop_tournament_bow),
				(val_add, ":tally_weapon_slots", 2),
			(else_try),
				(eq, ":weapon_choice", slot_troop_tournament_onehand),
				(val_add, ":tally_weapon_slots", 1),
			(else_try),
				(eq, ":weapon_choice", slot_troop_tournament_twohand),
				(val_add, ":tally_weapon_slots", 1),
			(else_try),
				(eq, ":weapon_choice", slot_troop_tournament_throwing),
				(val_add, ":tally_weapon_slots", 1),
			(else_try),
				(eq, ":weapon_choice", slot_troop_tournament_crossbow),
				(val_add, ":tally_weapon_slots", 2),
			(else_try),
				(eq, ":weapon_choice", slot_troop_tournament_polearm),
				(val_add, ":tally_weapon_slots", 1),
			(try_end),
		(try_end),
		
		# Make sure we only count 1 shield.
		(assign, ":tally_shields", 0),
		(assign, ":add_shield", 0),
		(troop_get_slot, ":add_shield", ":troop", slot_troop_tournament_lance),
		(val_add, ":tally_shields",  ":add_shield"),
		(troop_get_slot, ":add_shield", ":troop", slot_troop_tournament_onehand),
		(val_add, ":tally_shields",  ":add_shield"),
		(troop_get_slot, ":add_shield", ":troop", slot_troop_tournament_throwing),
		(val_add, ":tally_shields",  ":add_shield"),
		(val_min, ":tally_shields", 1),
		(val_add, ":tally_weapon_slots", ":tally_shields"),
			
		(try_begin), # Check to see if you have any weapons selected.
		# TPE 1.3 + Native Equipment Selection
			(eq, wp_tpe_mod_opt_actual_gear, 1),
			(overlay_set_text, "$g_presentation_obj_25", "@You will be using your own equipment^in the upcoming fight."),
		(else_try), # Check to see if you've exceeded four weapon slots.
		# TPE 1.3 -
			(eq, ":tally_weapons", 0),
			(overlay_set_text, "$g_presentation_obj_25", "@You have no weapons selected."),
		(else_try), # Check to see if you've exceeded four weapon slots.
			(gt, ":tally_weapon_slots", 4),
			(overlay_set_text, "$g_presentation_obj_25", "@You're using more than 4 weapon slots."),
		(else_try), # Check to see if you have any melee weapons.
			(neq, ":melee_weapon_check", 1),
			(overlay_set_text, "$g_presentation_obj_25", "@You currently have no melee weapon."),
		(else_try),
			(overlay_set_text, "$g_presentation_obj_25", "@Your weapon selection is adequate."),
		(try_end),
		
		(try_begin),
			(ge, DEBUG_TPE_general, 2),
			(assign, reg0, ":tally_weapons"),
			(assign, reg1, ":tally_weapon_slots"),
			(assign, reg2, ":melee_weapon_check"),
			(assign, reg3, ":tally_shields"),
			(display_message, "@DEBUG (TPE Weapon Logic): You have {reg1} weapon slots ({reg3} shield) used to support {reg0} weapons.  Melee weapon check: {reg2}"),
		(try_end),
	]
  ),

# script_TPE_SET_OPTION
# Input: arg1 = troop, arg2 = slot, arg3 = value, arg4 = object
  ("tpe_set_option",
    [
		(store_script_param, ":troop", 1),
		(store_script_param, ":option_slot", 2),
		(store_script_param, ":new_value", 3),
		(store_script_param, ":obj_option", 4),
		
		(troop_get_slot, ":old_value", ":troop", ":option_slot"),
		(assign, ":allow_remove", 0),
		(assign, ":allow_add", 0),
		(troop_get_slot, ":total_options", ":troop", slot_troop_tournament_selections),
		
		# Bugfix+ (1.3.15)	- To prevent the options presentation getting jammed with 3 options selected when they aren't.
		(try_for_range, ":selection", slot_troop_tournament_begin, slot_troop_tournament_end), # Clear out any previously selected options.
			(neg|troop_slot_eq, ":troop", ":selection", 0), # The option isn't OFF.
			(neg|troop_slot_eq, ":troop", ":selection", 1), # It isn't ON either.
			(troop_get_slot, ":value", ":troop", ":selection"),
			(assign, reg31, ":selection"),
			(assign, reg32, ":value"),
			(display_message, "@ERROR (script_tpe_set_option): Slot #{reg31} has an invalid value of {reg32}."),
		(try_end),
		# Bugfix-
		
		(try_begin),                                 # Too many options to add another.
			(eq, ":new_value", 1),
			(this_or_next|ge, ":total_options", 3),
			(lt, ":total_options", 0),
			(display_message, "@You already have three options selected."),
			(overlay_set_val, ":obj_option", ":old_value"),    # Prevents check being changed if invalid.  Display purpose only.
		(else_try),                                  # Allow option to be unchecked.
			(eq, ":new_value", 0),
			(eq, ":total_options", 3),
			(assign, ":allow_remove", 1),
			(val_sub, ":total_options", 1),
			(troop_set_slot, ":troop", slot_troop_tournament_selections, ":total_options"),
			(troop_set_slot, ":troop", ":option_slot", ":new_value"),
		(else_try),                                  # Allow option to be unchecked or checked.
			(lt, ":total_options", 3),
			(assign, ":allow_add", 1),
			(try_begin),
				(eq, ":new_value", 1),
				(val_add, ":total_options", 1),
			(else_try),
				(eq, ":new_value", 0),
				(val_sub, ":total_options", 1),
			(try_end),
			(troop_set_slot, ":troop", ":option_slot", ":new_value"),
			(troop_set_slot, ":troop", slot_troop_tournament_selections, ":total_options"),
		(try_end),
		
		(try_begin),
			(this_or_next|eq, ":allow_remove", 1),
			(eq, ":allow_add", 1),
			
			## CONDITIONAL CHECKBOXES begin
			(assign, ":remove_option", 0),   # This will toggle to 1 if a conditional checkbox option is removed due to a requirement being unselected.
			(assign, ":add_option", 0),      # This will toggle to 1 if a conditional checkbox option is added due to a requirement being selected.
		
			# Enhanced Horse
			(try_begin),
				(eq, ":option_slot", slot_troop_tournament_horse),
				(assign, ":conditional_obj", "$g_presentation_obj_12"), # Enhanced Horse - OBJ #12
				(assign, ":conditional_slot", slot_troop_tournament_enhanced_horse),
				(try_begin),
					(eq, ":new_value", 0),
					(assign, ":remove_option", 1),
				(else_try),
					(assign, ":add_option", 1),
				(try_end),
			(try_end),
			
			# Enhanced Shield
			(try_begin),
				(this_or_next|eq, ":option_slot", slot_troop_tournament_onehand),
				(this_or_next|eq, ":option_slot", slot_troop_tournament_throwing),
				(eq, ":option_slot", slot_troop_tournament_lance),
				(assign, ":conditional_obj", "$g_presentation_obj_15"), # Enhanced Shield - OBJ #15
				(assign, ":conditional_slot", slot_troop_tournament_enhanced_shield),
				(try_begin),
					(eq, ":new_value", 1),
					(assign, ":add_option", 1),
				(else_try),
					(troop_slot_eq, ":troop", slot_troop_tournament_onehand, 0),
					(troop_slot_eq, ":troop", slot_troop_tournament_throwing, 0),
					(troop_slot_eq, ":troop", slot_troop_tournament_lance, 0),
					(assign, ":remove_option", 1),
				(try_end),
			(try_end),
			
			# Add or remove option as needed.
			(try_begin),
				(eq, ":remove_option", 1), # Remove options that have lost their requirements
				(troop_get_slot, ":status", ":troop", ":conditional_slot"),
				(try_begin),
					(eq, ":status", 1),                                  # Is the conditional item even selected?
					(troop_set_slot, ":troop", ":conditional_slot", 0),  # Change the conditional option to unselected.
					(val_sub, ":total_options", 1),                      # Make sure you get that option back as well.
					(troop_set_slot, ":troop", slot_troop_tournament_selections, ":total_options"),
					(overlay_set_val, ":conditional_obj", ":status"),    # Update the display for the conditional option.
				(try_end),
				(overlay_set_display, ":conditional_obj", 0),            # Disables the lost option.
				(assign, ":remove_option", 0),
			(else_try),
				(eq, ":add_option", 1), # Adds options that have met their requirements
				(troop_get_slot, ":status", ":troop", ":conditional_slot"),  # Make sure it isn't already available & selected.
				(overlay_set_val, ":conditional_obj", ":status"),            # Set it to whatever it was stored as.
				(overlay_set_display, ":conditional_obj", 1),                # Displays the option.
				(assign, ":add_option", 0),
			(try_end),
			## CONDITIONAL CHECKBOXES end
		(try_end),
		
		# Set to randomize or remove based on options taken.
		# (try_begin),
			# (troop_slot_ge, ":troop", slot_troop_tournament_selections, 1),
			# (troop_set_slot, ":troop", slot_troop_tournament_always_randomize, 0),
		# (else_try),
			# (troop_set_slot, ":troop", slot_troop_tournament_always_randomize, 1),
		# (try_end),
		# (assign, ":count", 0),
		# (try_for_range, ":option", slot_troop_tournament_begin, slot_troop_tournament_end),
			# (troop_slot_ge, ":troop", ":option", 1),
			# (troop_set_slot, ":troop", slot_troop_tournament_always_randomize, 0),
			# (val_add, ":count", 1),
		# (try_end),
		# (try_begin),
			# (eq, ":count", 0),
			# (troop_set_slot, ":troop", slot_troop_tournament_always_randomize, 1),
		# (try_end),
		
		# Update display of options remaining.
		(call_script, "script_tpe_update_presentation"),
		(call_script, "script_tpe_weapon_logic", ":troop"), # TPE 1.3 + Limiting options panel reboots
		
		# Update difficulty score.
		(call_script, "script_tpe_get_difficulty_value"),
    ]
  ),

# script_tpe_clear_selections (blanks out troop template choices)
# Input: arg1 = troop
# Output: none
  ("tpe_clear_selections",
    [
		(store_script_param, ":troop_id", 1),
		(try_for_range, ":selection", slot_troop_tournament_begin, slot_troop_tournament_end), # Clear out any previously selected options.
			(troop_set_slot, ":troop_id", ":selection", 0),
		(try_end),
		(troop_set_slot, ":troop_id", slot_troop_tournament_selections, 0),
	]),
	
# script_tpe_set_items_for_tournament
# Input: 
# Output: none (sets mt_arena_melee_fight items)
  ("tpe_set_items_for_tournament",
    [
		(store_script_param, ":troop_id", 1),
		(store_script_param, ":troop_team", 2),
		(store_script_param, ":troop_entry", 3),
		
		(try_begin),
			(eq, "$g_wp_tpe_active", 1),
			(assign, ":mission_template", "mt_tpe_tournament_standard"),
		(try_end),
		
		# Find the appropriate city settings.
		(store_sub, ":city_settings", "$current_town", towns_begin),
		(val_mul, ":city_settings", 10),
		(store_add, ":slot_lance",    ":city_settings", tdp_val_setting_lance),
		(store_add, ":slot_archery",  ":city_settings", tdp_val_setting_archery),
		(store_add, ":slot_onehand",  ":city_settings", tdp_val_setting_onehand),
		(store_add, ":slot_twohand",  ":city_settings", tdp_val_setting_twohand),
		(store_add, ":slot_crossbow", ":city_settings", tdp_val_setting_crossbow),
		(store_add, ":slot_throwing", ":city_settings", tdp_val_setting_throwing),
		(store_add, ":slot_polearm",  ":city_settings", tdp_val_setting_polearm),
		(store_add, ":slot_horse",    ":city_settings", tdp_val_setting_horse),
		#(store_add, ":slot_outfit",   ":city_settings", tdp_val_setting_outfit),
		(troop_get_slot, ":item_normal_lance",    tpe_appearance, ":slot_lance"),
		(troop_get_slot, ":item_normal_archery",  tpe_appearance, ":slot_archery"),
		(troop_get_slot, ":item_normal_onehand",  tpe_appearance, ":slot_onehand"),
		(troop_get_slot, ":item_normal_twohand",  tpe_appearance, ":slot_twohand"),
		(troop_get_slot, ":item_normal_crossbow", tpe_appearance, ":slot_crossbow"),
		(troop_get_slot, ":item_normal_throwing", tpe_appearance, ":slot_throwing"),
		(troop_get_slot, ":item_normal_polearm",  tpe_appearance, ":slot_polearm"),
		(troop_get_slot, ":item_normal_horse",    tpe_appearance, ":slot_horse"),
		#(troop_get_slot, ":item_normal_outfit",   tpe_appearance, ":slot_outfit"),
		(try_begin),
			(assign, ":equip_check", 0),
			(neq, ":item_normal_lance", 0),
			(neq, ":item_normal_archery", 0),
			(neq, ":item_normal_onehand", 0),
			(neq, ":item_normal_twohand", 0),
			(neq, ":item_normal_crossbow", 0),
			(neq, ":item_normal_throwing", 0),
			(neq, ":item_normal_polearm", 0),
			(neq, ":item_normal_horse", 0),
			#(neq, ":item_normal_outfit", 0),
			(assign, ":equip_check", 1),
		(else_try),
			(eq, ":equip_check", 0),
			(display_message, "@ERROR (TPE Design): An invalid item type (normal weapon) is detected."),
		(try_end),
		(store_add, ":item_enh_lance", ":item_normal_lance", 1),
		(store_add, ":item_enh_archery", ":item_normal_archery", 1),
		(store_add, ":item_enh_onehand", ":item_normal_onehand", 1),
		(store_add, ":item_enh_twohand", ":item_normal_twohand", 1),
		(store_add, ":item_enh_crossbow", ":item_normal_crossbow", 1),
		(store_add, ":item_enh_throwing", ":item_normal_throwing", 2),
		(store_add, ":item_enh_polearm", ":item_normal_polearm", 1),
		(store_add, ":item_enh_horse", ":item_normal_horse", 4),
		#(store_add, ":item_enh_outfit", ":item_normal_outfit", 100),
		(try_begin),
			(assign, ":equip_check", 0),
			(neq, ":item_enh_lance", 0),
			(neq, ":item_enh_archery", 0),
			(neq, ":item_enh_onehand", 0),
			(neq, ":item_enh_twohand", 0),
			(neq, ":item_enh_crossbow", 0),
			(neq, ":item_enh_throwing", 0),
			(neq, ":item_enh_polearm", 0),
			(neq, ":item_enh_horse", 0),
			#(neq, ":item_enh_outfit", 0),
			(assign, ":equip_check", 1),
		(else_try),
			(eq, ":equip_check", 0),
			(display_message, "@ERROR (TPE Design): An invalid item type (enhanced weapon) is detected."),
		(try_end),
		(mission_tpl_entry_clear_override_items, ":mission_template", ":troop_entry"),
			
		(try_begin),
			(ge, DEBUG_TPE_general, 3), # Verbose display on entry.
			(str_store_troop_name, s1, ":troop_id"),
			(assign, reg0, ":troop_team"),
			(assign, reg1, ":troop_entry"),
			(display_message, "@DEBUG (TPE): {s1} is on team {reg0} and should load at entry {reg1}."),
		(try_end),
			
		# Do they have any gear arranged for them?
		(try_begin),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_always_randomize, 1),   # Player set to randomize. # Bugfix #1337, v0.23
			(eq, "$g_wp_tpe_active", 0),                                                            # TPE 1.2 + If TPE deactivated by player then everyone gets random stuff.
			(call_script, "script_tpe_equip_troop", ":troop_id"),                                   # gears up the troop.
		(try_end),
		
		(str_clear, s1),
			
		# Do they get a horse?
		(assign, ":give_enhanced_armor", 0),
		(assign, ":give_enhanced_weapons", 0),
		(try_begin),
			# Check if mounts are allowed in this center's tournaments and override if needed.
			(store_sub, ":city_offset", "$current_town", towns_begin),
			(store_mul, ":city_settings", ":city_offset", 10),
			(store_add, ":slot_offset", ":city_settings", tdp_val_setting_horse),
			(troop_get_slot, ":mount_chance", tpe_settings, ":slot_offset"),
			(ge, ":mount_chance", 1), # City allows mounts at all.
			(try_begin),
				(troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_horse, 1),
				(assign, ":team_horse", ":item_enh_horse"),
				(val_add, ":team_horse", ":troop_team"), # TESTING - Commented since I don't have different colored warhorses yet.
				(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":team_horse"),
				(str_store_string, s1, "@{s1} enhanced horse (+2),"), # debugging
			(else_try),
				(troop_slot_eq, ":troop_id", slot_troop_tournament_horse, 1),
				(assign, ":team_horse", ":item_normal_horse"),
				(val_add, ":team_horse", ":troop_team"), # TESTING - Commented since I don't have different colored warhorses yet.
				(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":team_horse"),
				#(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", wp_tpe_normal_horse),
				(str_store_string, s1, "@{s1} horse (+1),"), # debugging
			(try_end),
		(else_try),
			# Give the troop something else if they had mounts enabled, but can't use them.
			(troop_slot_eq, ":troop_id", slot_troop_tournament_horse, 1),
			(eq, ":mount_chance", 0),
			(try_begin),
				(troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_armor, 0),
				(assign, ":give_enhanced_armor", 1),
			(else_try),
				(troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_weapons, 0),
				(assign, ":give_enhanced_weapons", 1),
			(try_end),
		(try_end),
			
		# Do they have enhanced armor?
		(try_begin),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_armor, 1),
			(eq, ":give_enhanced_armor", 1),
			(assign, ":team_armor", wp_tpe_enhanced_armor),
			(val_add, ":team_armor", ":troop_team"),
            (mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":team_armor"),
			(str_store_string, s1, "@{s1} enhanced armor (+1),"), # debugging
			(assign, ":team_helmet", wp_tpe_enhanced_helmet),
			(val_add, ":team_helmet", ":troop_team"),
            (mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":team_helmet"),
			(str_store_string, s1, "@{s1} enhanced helmet,"), # debugging
            (mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", wp_tpe_enhanced_boots),
			(str_store_string, s1, "@{s1} enhanced boots,"), # debugging
		(else_try),
			(assign, ":team_armor", wp_tpe_default_armor),
			(val_add, ":team_armor", ":troop_team"),
			(str_store_string, s1, "@{s1} armor,"), # debugging
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":team_armor"),
			(assign, ":team_helmet", wp_tpe_normal_helmet),  # Section commented out to prevent normal armor having a helm.
			(val_add, ":team_helmet", ":troop_team"),
			(str_store_string, s1, "@{s1} helmet,"), # debugging
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":team_helmet"),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", wp_tpe_normal_boots),
			(str_store_string, s1, "@{s1} boots,"), # debugging
		(try_end),
			
		# Do they have an enhanced shield?
		(try_begin),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_shield, 1),
			(assign, ":team_armor", wp_tpe_enhanced_shield),
			(val_add, ":team_armor", ":troop_team"),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":team_armor"),
			(str_store_string, s1, "@{s1} enhanced shield (+1),"), # debugging
		(else_try),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_lance, 1),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_onehand, 1),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_throwing, 1),
			(assign, ":team_armor", wp_tpe_normal_shield),
			(val_add, ":team_armor", ":troop_team"),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":team_armor"),
			(str_store_string, s1, "@{s1} shield,"), # debugging
		(try_end),
			
		# Lances
		(try_begin),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_lance, 1),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_weapons, 1),
            (eq, ":give_enhanced_weapons", 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_enh_lance"),
			(str_store_item_name, s2, ":item_enh_lance"),
			(str_store_string, s1, "@{s1} enhanced {s2} lance (+2),"), # debugging
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_lance, 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_normal_lance"),
			(str_store_item_name, s2, ":item_normal_lance"),
			(str_store_string, s1, "@{s1} {s2} (+1),"), # debugging
		(try_end),
			
		# Bows
		(try_begin),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_bow, 1),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_weapons, 1),
            (eq, ":give_enhanced_weapons", 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_enh_archery"),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", "itm_practice_arrows"),
			(str_store_item_name, s2, ":item_enh_archery"),
			(str_store_string, s1, "@{s1} enhanced {s2} (+2),"), # debugging
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_bow, 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_normal_archery"),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", "itm_practice_arrows"),
			(str_store_item_name, s2, ":item_normal_archery"),
			(str_store_string, s1, "@{s1} {s2} (+1),"), # debugging
		(try_end),
			
		# Single handed weapons
		(try_begin),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_onehand, 1),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_weapons, 1),
            (eq, ":give_enhanced_weapons", 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_enh_onehand"),
			(str_store_item_name, s2, ":item_enh_onehand"),
			(str_store_string, s1, "@{s1} enhanced {s2} (+2),"), # debugging
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_onehand, 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_normal_onehand"),
			(str_store_item_name, s2, ":item_normal_onehand"),
			(str_store_string, s1, "@{s1} {s2} (+1),"), # debugging
		(try_end),
			
		# Two handed weapons
		(try_begin),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_twohand, 1),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_weapons, 1),
            (eq, ":give_enhanced_weapons", 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_enh_twohand"),
			(str_store_item_name, s2, ":item_enh_twohand"),
			(str_store_string, s1, "@{s1} enhanced {s2} (+2),"), # debugging
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_twohand, 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_normal_twohand"),
			(str_store_item_name, s2, ":item_normal_twohand"),
			(str_store_string, s1, "@{s1} {s2} (+1),"), # debugging
		(try_end),
			
		# Crossbows
		(try_begin),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_crossbow, 1),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_weapons, 1),
            (eq, ":give_enhanced_weapons", 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_enh_crossbow"),
			(str_store_item_name, s2, ":item_enh_crossbow"),
			(str_store_string, s1, "@{s1} enhanced {s2} (+2),"), # debugging
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", "itm_practice_bolts"),
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_crossbow, 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_normal_crossbow"),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", "itm_practice_bolts"),
			(str_store_item_name, s2, ":item_normal_crossbow"),
			(str_store_string, s1, "@{s1} {s2} (+1),"), # debugging
		(try_end),
			
		# Thown Weapons
		(try_begin),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_throwing, 1),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_weapons, 1),
            (eq, ":give_enhanced_weapons", 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_enh_throwing"),
			(str_store_item_name, s2, ":item_enh_throwing"),
			(str_store_string, s1, "@{s1} enhanced {s2} (+2),"), # debugging
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_throwing, 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_normal_throwing"),
			(str_store_item_name, s2, ":item_normal_throwing"),
			(str_store_string, s1, "@{s1} {s2} (+1),"), # debugging
		(try_end),
			
		# Polearms
		(try_begin),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_polearm, 1),
			(this_or_next|troop_slot_eq, ":troop_id", slot_troop_tournament_enhanced_weapons, 1),
            (eq, ":give_enhanced_weapons", 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_enh_polearm"),
			(str_store_item_name, s2, ":item_enh_polearm"),
			(str_store_string, s1, "@{s1} enhanced {s2} (+2),"), # debugging
		(else_try),
			(troop_slot_eq, ":troop_id", slot_troop_tournament_polearm, 1),
			(mission_tpl_entry_add_override_item, ":mission_template", ":troop_entry", ":item_normal_polearm"),
			(str_store_item_name, s2, ":item_normal_polearm"),
			(str_store_string, s1, "@{s1} {s2} (+1),"), # debugging
		(try_end),
			
		(try_begin),
			(ge, DEBUG_TPE_DESIGN, 1), # Very verbose display.
			(str_store_troop_name, s2, ":troop_id"),
			(display_message, "@DEBUG (TPE): {s2} receives {s1}."),
		(try_end),
	]),
## TOURNAMENT PLAY ENHANCEMENTS end

# script_tpe_determine_scaled_renown
# This section implements the "Renown Scaling" feature.
# Inputs: troop_id
# Output: reg0 (new renown)
  ("tpe_determine_scaled_renown",
    [
		(store_script_param, ":troop_no", 1),
		
		# Determine renown gained by player level.
		(store_character_level, ":player_level", ":troop_no"),
		(store_div, ":sr_level_factor", 40, ":player_level"),  # Balanced for a max level of 40.  Beyond this you get minimum gain.
		(val_mul, ":sr_level_factor", 5),
		(store_div, ":sr_factor_limit", wp_tpe_max_renown, 2), # Since two factors are used.  Total is split by 2.
		(val_min, ":sr_level_factor", ":sr_factor_limit"),     # Prevents an extremely low level gaining more renown than intended.
		(val_max, ":sr_level_factor", 5),                      # Sets a minimum renown gain of 5 no matter how high your level is.
		
		# Determine renown gained by player renown.
		(troop_get_slot, ":player_renown", ":troop_no", slot_troop_renown),
		(store_div, ":sr_renown_factor", 1500, ":player_renown"),  # Balanced for a max renown of 1500.  Beyond this you get minimum gain.
		(val_mul, ":sr_renown_factor", 5),
		(store_div, ":sr_factor_limit", wp_tpe_max_renown, 2),  # Since two factors are used.  Total is split by 2.
		(val_min, ":sr_renown_factor", ":sr_factor_limit"),     # Prevents an extremely low level gaining more renown than intended.
		(val_max, ":sr_renown_factor", 5),                      # Sets a minimum renown gain of 5 no matter how high your level is.
		
		(store_add, reg0, ":sr_level_factor", ":sr_renown_factor"), # combines both factors.
		
		# Limit renown gain for winning a tournament during feast.
		(try_begin),
			(store_faction_of_party, ":center_faction", "$current_town"),
			(faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
			(faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
			(val_min, reg0, 20),
		(try_end),
	]),
	
###########################################################################################################################
#####                                                TPE 1.3 Additions                                                #####
###########################################################################################################################

###########################################################################################################################
#####                                               REWARDS & BETTING                                                 #####
###########################################################################################################################

# script_tpe_set_bet
# Figures out what your persistent bet is and places it accordingly each round.
# Input: none
# Output: none
  ("tpe_set_bet",
    [
		(try_begin),
			(eq, "$g_wp_tpe_active", 1),
			(call_script, "script_tpe_calculate_wager_for_bid"),
			(assign, ":bid", reg2),
			(troop_get_slot, ":wager", TPE_OPTIONS, tpe_val_bet_wager),
			
			# If the player doesn't want to wager anything or isn't making a bid no bet should be placed.
			(ge, ":bid", 1),
			(ge, ":wager", 1),
			
			(store_troop_gold,":current_gold","trp_player"),
			(try_begin),
				(ge, ":current_gold", ":wager"),
				(call_script, "script_tournament_place_bet", ":wager"),
				(val_sub, "$tpe_total_earnings", ":wager"),
				(store_troop_gold,":current_gold","trp_player"),
				(assign, reg1, ":current_gold"),
				(assign, reg0, ":wager"),
				(assign, reg2, ":bid"),
				#(display_message, "@You place a bet of {reg0} denars before starting the round.  You have {reg1} denars remaining."),
				(display_message, "str_tpe_message_round_bid", gpu_green),
				(display_message, "str_tpe_message_round_cash_left"),
				
			(else_try),
				(assign, reg0, ":wager"),
				(display_message, "str_tpe_message_cant_cover_bet", gpu_red),
			(try_end),
		(try_end),
	]),
	
# script_tpe_calculate_wager_for_bid
# Takes your input of a target number of points to earn then returns the applicable bid.
# Input: (bid)
# Output: reg3 (wager)
  ("tpe_calculate_wager_for_bid",
    [
		(troop_get_slot, ":bid", TPE_OPTIONS, tpe_val_bet_bid),
		(assign, ":modified_bid", ":bid"),
		(troop_get_slot, ":wager", TPE_OPTIONS, tpe_val_bet_wager),
		(call_script, "script_tpe_get_difficulty_value"),
		(assign, ":difficulty", reg1),
		(troop_get_slot, ":difficulty_slider", TPE_OPTIONS, tpe_val_diff_setting),
		
		# Determine how many kills are even possible given the current team setup.
		(assign, ":team_size", "$g_tournament_next_team_size"),
		(assign, ":team_number", "$g_tournament_next_num_teams"),
		(val_sub, ":team_number", 1),
		(store_mul, ":valid_enemies", ":team_size", ":team_number"),
		
		(try_begin),
			(lt, ":valid_enemies", ":bid"),
			(assign, ":bid", ":valid_enemies"),
			(assign, ":modified_bid", ":valid_enemies"),
		(try_end),
		
		# Remove survivor benefit from calculations.
		(try_begin),
			(store_mul, ":roster_size", "$g_tournament_next_team_size", "$g_tournament_next_num_teams"),
			(ge, ":roster_size", tpe_survival_min_participants),
			(val_sub, ":modified_bid", 2),
		(try_end),
		
		#### CONFIGURE PAYOUT ####
		# Determine base payout value. ( Bid * Wager )
		(store_mul, ":payout", ":bid", ":wager"),
		(val_mul, ":payout", ":difficulty"),
		(val_div, ":payout", 100),
		
		# Determine difficulty factor of obtaining bid.  (% of enemies + difficulty setting bonus)
		(store_mul, ":bid_difficulty_factor", ":difficulty_slider", 1),
		(store_mul, ":bid_times_100", ":modified_bid", 100),
		(val_max, ":valid_enemies", 1), # Prevent Div/0 errors.
		(store_div, ":percent_of_enemies_times_100", ":bid_times_100", ":valid_enemies"), # We now have our difficulty score as a %.
		(val_add, ":bid_difficulty_factor", ":percent_of_enemies_times_100"),
		
		# Combine & Div/100 to get a normal value.
		(store_mul, ":payout_bonus", ":payout", ":bid_difficulty_factor"),
		(val_div, ":payout_bonus", 100),
		(val_add, ":payout", ":payout_bonus"),
		
		# Set a minimum limit on payouts. (150% of wager)
		(store_mul, ":payout_minimum", ":wager", 3),
		(val_div, ":payout_minimum", 2),
		
		# Set a maximum limit on payouts.
		(assign, ":payout_maximum", 2501), 
		
		(try_begin),
			(ge, ":payout", ":payout_maximum"),
			(str_store_string, s21, "@ (limited)"),
		(else_try),
			(lt, ":payout", ":payout_minimum"),
			(str_store_string, s21, "@ (limited)"),
		(else_try),
			(str_clear, s21),
		(try_end),
		
		(val_clamp, ":payout", ":payout_minimum", ":payout_maximum"),
		
		# Create output string.
		(assign, reg4, ":payout"),
		(str_store_string, s22, "str_tpe_label_bid_payout_r4"),
		(str_store_string, s23, "@{s22}{s21}"),
		
		(assign, reg2, ":bid"),
		(assign, reg3, ":wager"),
		(assign, reg4, ":payout"),
		
		(try_begin),
			### TOURNAMENT OPTIONS PANEL ###
			(is_presentation_active, "prsnt_tournament_options_panel"),
			# Set the BID slider position
			(troop_get_slot, ":obj_slider", "trp_tpe_presobj", tpe_slider_bid_value),
			(overlay_set_val, ":obj_slider", ":bid"),
			# Set the bid text
			(troop_get_slot, ":obj_text_bid", "trp_tpe_presobj", tpe_text_bid_amount),
			(assign, reg2, ":bid"),
			(overlay_set_text, ":obj_text_bid", "@{reg2} points"),
			# Set the payout text
			(troop_get_slot, ":obj_text_payout", "trp_tpe_presobj", tpe_text_bet_payout),
			(overlay_set_text, ":obj_text_payout", "@{s23}"),
		(else_try),
			### TOURNAMENT RANKING PANEL ###
			(is_presentation_active, "prsnt_tpe_ranking_display"),
			# Set the bid text
			(troop_get_slot, ":obj_text_payout", "trp_tpe_presobj", tpe_text_bet_value),
			(overlay_set_text, ":obj_text_payout", "str_tpe_label_long_bid"),
		(try_end),
		
	]),
	
# script_tpe_calc_final_rewards
# Clears out all award data each round.
# Input: troop_id, rank (1,2,3)
# Output: reg5 (gold payout), reg6 (xp gain)
  ("tpe_calc_final_rewards",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":rank", 2),
		
		(assign, ":div_factor", 1),
		(try_begin),
			(eq, ":rank", 2),
			(assign, ":div_factor", 2),
		(else_try),
			(eq, ":rank", 3),
			(assign, ":div_factor", 4),
		(try_end),
		
		# Limit gains during a feast. (-50% payout)
		(try_begin),
			(store_faction_of_party, ":center_faction", "$current_town"),
			(faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
			(faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
			(val_mul, ":div_factor", 2), # Cut winnings in half.
		(try_end),
		
		(try_begin),
			(eq, wp_tpe_mod_opt_payout_bonus, 1),
			(set_show_messages, 0),
			
			# Determine what your average difficulty score per round was.
			(troop_get_slot, ":difficulty", TPE_OPTIONS, tpe_val_cumulative_diff),
			(val_max, ":difficulty", 1), # Prevent div/0 errors.
			(val_div, ":difficulty", wp_tpe_max_tournament_tiers),
			
			# # Award cash
			# (store_mul, ":gold", wp_tpe_payout_cap_cash, ":difficulty"),
			# (val_max, ":gold", 1), # Prevent div/0 errors.
			# (val_div, ":gold", 100),
			# (val_min, ":gold", wp_tpe_payout_cap_cash), # Sets a hard limit for cash earned.
			# (val_div, ":gold", ":div_factor"),
			# (troop_add_gold, ":troop_no", ":gold"),
			# (val_add, "$tpe_total_earnings", ":gold"),
			
			# Award xp
			(store_mul, ":xp_gain", wp_tpe_payout_cap_xp, ":difficulty"),
			(val_max, ":xp_gain", 1), # Prevent div/0 errors.
			(val_div, ":xp_gain", 100),
			(val_min, ":xp_gain", wp_tpe_payout_cap_xp), # Sets a hard limit for cash earned.
			# Apply level cap.
			(store_character_level, ":level", ":troop_no"),
			(store_mul, ":level_cap", ":level", wp_tpe_cap_increase_per_level),
			(val_add, ":level_cap", wp_tpe_min_xp_gain),
			(val_min, ":xp_gain", ":level_cap"),
			(val_div, ":xp_gain", ":div_factor"),
			(add_xp_to_troop, ":xp_gain", ":troop_no"), # Was 250
			
			# Determine scaled renown
			(call_script, "script_tpe_determine_scaled_renown", ":troop_no"),
			(assign, ":sr_renown", reg0),
			(val_div, ":sr_renown", ":div_factor"),
			
			(set_show_messages, 1),
		(else_try),
			# Award cash
			(assign, ":gold", 200),
			(val_div, ":gold", ":div_factor"),
			(troop_add_gold, ":troop_no", ":gold"),
			(val_add, "$tpe_total_earnings", ":gold"),
			
			# Award xp
			(assign, ":xp_gain", 250),
			(val_div, ":xp_gain", ":div_factor"),
			(add_xp_to_troop, ":xp_gain", ":troop_no"), # Was 250
		(try_end),
		
		(try_begin),
			(eq, wp_tpe_mod_opt_renown_scale_enabled, 1), # TPE 1.3 + Renown Scaling disable option.
			(eq, "$g_wp_tpe_renown_scaling", 1),
			(call_script, "script_change_troop_renown", ":troop_no", ":sr_renown"),
			(eq, ":troop_no", "trp_player"),
			(party_get_slot, ":total_wins", "$current_town", slot_center_tournament_wins),
			(val_min, ":total_wins", 3),
			(call_script, "script_change_player_relation_with_center", "$current_town", ":total_wins"),
		(else_try),
			# Everything in this grouping leaves the settings as they would be in the Native game.
			(eq, ":troop_no", "trp_player"),
			(call_script, "script_change_troop_renown", ":troop_no", 20),
			(call_script, "script_change_player_relation_with_center", "$current_town", 1),
		(try_end),
        (assign, reg5, ":gold"),
		(assign, reg6, ":xp_gain"),
		(assign, reg7, ":sr_renown"),
	]),

# script_tpe_award_loot
# PURPOSE: Returns the minimum and maximum value of a tournament prize for the winner as well as sets the availability for item modifiers.
  ("tpe_award_loot",
    [
		# (store_script_param, ":troop_no", 1),
		# (store_script_param, ":limit", 2),
		
		(store_character_level, ":level", "trp_player"),
		
		# Determine what your average difficulty score per round was.
		(troop_get_slot, ":prize_slot", TPE_OPTIONS, tpe_val_cumulative_diff),
		(val_max, ":prize_slot", 1), # Prevent div/0 errors.
		(val_div, ":prize_slot", wp_tpe_max_tournament_tiers),
		(assign, ":difficulty", ":prize_slot"), # Stored for later use.
		
		# Determine our minimum and maximum prize values.
		(store_div, ":level_multi", ":level", 5),
		(val_max, ":level_multi", 1),
		(store_mul, ":value_min", ":difficulty", 4),
		(store_mul, ":value_max", ":difficulty", 15),
		(val_mul, ":value_max", ":level_multi"),
		(val_add, ":value_max", 500),
		
		# Determine our imod availability based on difficulty
		(store_div, ":imod_avail", ":difficulty", 2),
		(val_clamp, ":imod_avail", 20, 50),
		
		(assign, "$tpe_award_min_value", ":value_min"),
		(assign, "$tpe_award_max_value", ":value_max"),
		(assign, "$tpe_award_imod_availability", ":imod_avail"),
		
		### DIAGNOSTIC+ ###
		(try_begin),
			(ge, DEBUG_TPE_LOOT, 1),
			(assign, reg31, "$tpe_award_min_value"),
			(assign, reg32, "$tpe_award_max_value"),
			(assign, reg33, "$tpe_award_imod_availability"),
			(display_message, "@DEBUG (TPE Loot): Prize price range is {reg31} to {reg32} denars.  IMOD% is {reg33}.", gpu_debug),
		(try_end),
		### DIAGNOSTIC- ###
		
		#### OLD SYSTEM+ ####
		# # Add impose a starting penalty that is reduced and eventually overcome by a linear level bonus.
		# (store_sub, ":level_bonus", ":level", 20),
		# (val_add, ":prize_slot", ":level_bonus"),
		# # Convert value to match the 1-41 scale.
		# (val_mul, ":prize_slot", 41),
		# (val_div, ":prize_slot", 100),
		# # Reduces prize value by input % limiter.  Currently 70% (2nd) and 40% (3rd).
		# (val_mul, ":prize_slot", ":limit"),
		# (val_div, ":prize_slot", 100),
		# # Limit value to between 1-41 so that we don't get invalid item errors.
		# (val_clamp, ":prize_slot", 1, 42),
		# (val_add, ":prize_slot", 200),
		# (troop_get_slot, ":item_no", tpe_xp_table, ":prize_slot"),
		
		# # imod_plain       Plain_%s         1.000000  1.000000
		# # imod_cracked     Cracked_%s       0.500000  1.000000  Armor (ac-4), Shield (ac-4, hp-46), Weapon (damage-5), Horse (ac-4, hp-46)
		# # imod_rusty       Rusty_%s         0.550000  1.000000  Armor (ac-3), Shield (ac-3), Weapon (dmg-3), Horse (ac-3)
		# # imod_bent        Bent_%s          0.650000  1.000000  Shield (speed-3), Weapon (dmg-3, speed-3)
		# # imod_chipped     Chipped_%s       0.720000  1.000000  Weapon (dmg-1)
		# # imod_battered    Battered_%s      0.750000  1.000000  Armor (ac-2), Shield (ac-2, hp-26), Horse (ac-2, hp-26)
		# # imod_poor        Poor_%s          0.800000  1.000000  
		# # imod_crude       Crude_%s         0.830000  1.000000  Armor (ac-1), Shield (ac-1), Weapon (dmg-2), Horse (ac-1)
		# # imod_old         Old_%s           0.860000  1.000000
		# # imod_cheap       Cheap_%s         0.900000  1.000000
		# # imod_fine        Fine_%s          1.900000  0.600000  Weapon (dmg+1)
		# # imod_well_made   Well_Made_%s     2.500000  0.500000
		# # imod_sharp       Sharp_%s         1.600000  0.600000
		# # imod_balanced    Balanced_%s      3.500000  0.500000  Shield (speed+3), Weapon (dmg+3, speed+3)
		# # imod_tempered    Tempered_%s      6.700000  0.400000  Weapon (dmg+4)
		# # imod_deadly      Deadly_%s        8.500000  0.300000
		# # imod_exquisite   Exquisite_%s    14.500000  0.300000
		# # imod_masterwork  Masterwork_%s   17.500000  0.300000  Armor (req+4), Shield (speed+1), Weapon (dmg+5, speed+1, req+4)
		# # imod_heavy       Heavy_%s         1.900000  0.700000  Armor (ac+3, req+1), Shield (ac+3, hp+10, speed-2, req+1), Weapon (speed-2, damage+2, req+1), Horse (ac+3, charge+4, hp+10)
		# # imod_strong      Strong_%s        4.900000  0.400000  Armor (req+2), Shield (speed-3), Weapon (dmg+3, speed-3, req+2)
		# # imod_powerful    Powerful_%s      3.200000  0.400000
		# # imod_tattered    Tattered_%s      0.500000  1.000000  Armor (ac-3), Shield (ac-3), Horse (ac-3)
		# # imod_ragged      Ragged_%s        0.700000  1.000000  Armor (ac-2), Shield (ac-2), Horse (ac-2)
		# # imod_rough       Rough_%s         0.600000  1.000000
		# # imod_sturdy      Sturdy_%s        1.700000  0.500000  Armor (ac+1), Shield (ac+1), Horse (ac+1)
		# # imod_thick       Thick_%s         2.600000  0.350000  Armor (ac+2), Shield (ac+2, hp+47), Horse (ac+2, hp+47)
		# # imod_hardened    Hardened_%s      3.900000  0.300000  Armor (ac+3), Shield (ac+3), Horse (ac+3)
		# # imod_reinforced  Reinforced_%s    6.500000  0.250000  Armor (ac+4), Shield (ac+4, hp+83), Horse (ac+4, hp+83)
		# # imod_superb      Superb_%s        2.500000  0.250000
		# # imod_lordly      Lordly_%s       11.500000  0.250000  Armor (ac+6), Shield (ac+6, hp+155), Horse (ac+6, hp+155)
		# # imod_lame        Lame_%s          0.400000  1.000000  Horse (speed-10, maneuver-5)
		# # imod_swaybacked  Swaybacked_%s    0.600000  1.000000  Horse (speed-4, maneuver-2)
		# # imod_stubborn    Stubborn_%s      0.900000  1.000000  Shield (hp+5), Horse (hp+5, req+1)
		# # imod_timid       Timid_%s         1.800000  1.000000
		# # imod_meek        Meek_%s          1.800000  1.000000
		# # imod_spirited    Spirited_%s      6.500000  0.600000  Horse (speed+2, maneuver+1, charge+1)
		# # imod_champion    Champion_%s     14.500000  0.200000  Horse (speed+4, maneuver+2, charge+2, req+2)
		# # imod_fresh       Fresh_%s         1.000000  1.000000
		# # imod_day_old     Day-old_%s       1.000000  1.000000
		# # imod_two_day_old Two_Days-old_%s  0.900000  1.000000
		# # imod_smelling    Smelling_%s      0.400000  1.000000
		# # imod_rotten      Rotten_%s        0.050000  1.000000
		# # imod_large_bag   Large_Bag_of_%s  1.900000  0.300000  Food (qty+6), Ammo (amount+6), Crossbow (capable to fire twice)

		# # Determine proper item modifier for type.
		# (try_begin),
			# (ge, ":item_no", 1), # Valid item
			# (item_get_type, ":item_type", ":item_no"),
			# (assign, ":imod", imod_plain),
			# (try_begin),
				# # Weapons: itp_type_one_handed_wpn, itp_type_two_handed_wpn, itp_type_polearm, itp_type_crossbow, itp_type_bow, itp_type_thrown, itp_type_pistol, itp_type_musket
				# (this_or_next|eq, ":item_type", itp_type_one_handed_wpn),
				# (this_or_next|eq, ":item_type", itp_type_two_handed_wpn),
				# (this_or_next|eq, ":item_type", itp_type_polearm),
				# (this_or_next|eq, ":item_type", itp_type_crossbow),
				# (this_or_next|eq, ":item_type", itp_type_bow),
				# (this_or_next|eq, ":item_type", itp_type_thrown),
				# (this_or_next|eq, ":item_type", itp_type_pistol),
				# (eq, ":item_type", itp_type_musket),
				# # Valid item.  Now determine item modifier.
				# (try_begin),
					# (assign, ":imod", imod_fine),
					# (ge, ":difficulty", wp_tpe_tier_2_loot),
					# (assign, ":imod", imod_heavy),
					# (ge, ":difficulty", wp_tpe_tier_3_loot),
					# (ge, ":limit", wp_tpe_final_rank_2),
					# (assign, ":imod", imod_balanced),
					# (ge, ":difficulty", wp_tpe_tier_4_loot),
					# (assign, ":imod", imod_strong),
					# (ge, ":difficulty", wp_tpe_tier_5_loot),
					# (ge, ":limit", wp_tpe_final_rank_1),
					# (assign, ":imod", imod_tempered),
					# (ge, ":difficulty", wp_tpe_tier_6_loot),
					# (assign, ":imod", imod_masterwork),
				# (try_end),
			# (else_try),
				# # Shield: itp_type_shield
				# (eq, ":item_type", itp_type_shield),
				# # Valid item.  Now determine item modifier.
				# (try_begin),
					# (assign, ":imod", imod_sturdy),
					# (ge, ":difficulty", wp_tpe_tier_2_loot),
					# (assign, ":imod", imod_heavy),
					# (ge, ":difficulty", wp_tpe_tier_3_loot),
					# (ge, ":limit", wp_tpe_final_rank_2),
					# (assign, ":imod", imod_thick),
					# (ge, ":difficulty", wp_tpe_tier_4_loot),
					# (assign, ":imod", imod_thick), # imod_hardened doesn't work with shields.
					# (ge, ":difficulty", wp_tpe_tier_5_loot),
					# (ge, ":limit", wp_tpe_final_rank_1),
					# (assign, ":imod", imod_reinforced),
					# (ge, ":difficulty", wp_tpe_tier_6_loot),
					# (assign, ":imod", imod_lordly),
				# (try_end),
			# (else_try),
				# # Armor: itp_type_head_armor, itp_type_body_armor, itp_type_foot_armor, itp_type_hand_armor
				# (this_or_next|eq, ":item_type", itp_type_head_armor),
				# (this_or_next|eq, ":item_type", itp_type_body_armor),
				# (this_or_next|eq, ":item_type", itp_type_foot_armor),
				# (eq, ":item_type", itp_type_hand_armor),
				# # Valid item.  Now determine item modifier.
				# (try_begin),
					# (assign, ":imod", imod_sturdy),
					# (ge, ":difficulty", wp_tpe_tier_2_loot),
					# (assign, ":imod", imod_heavy),
					# (ge, ":difficulty", wp_tpe_tier_3_loot),
					# (ge, ":limit", wp_tpe_final_rank_2),
					# (assign, ":imod", imod_thick),
					# (ge, ":difficulty", wp_tpe_tier_4_loot),
					# (assign, ":imod", imod_hardened),
					# (ge, ":difficulty", wp_tpe_tier_5_loot),
					# (ge, ":limit", wp_tpe_final_rank_1),
					# (assign, ":imod", imod_reinforced),
					# (ge, ":difficulty", wp_tpe_tier_6_loot),
					# (assign, ":imod", imod_lordly),
				# (try_end),
			# (else_try),
				# # Ammunition: itp_type_arrows, itp_type_bolts, itp_type_bullets
				# (this_or_next|eq, ":item_type", itp_type_arrows),
				# (this_or_next|eq, ":item_type", itp_type_bolts),
				# (eq, ":item_type", itp_type_bullets),
				# (assign, ":imod", imod_large_bag),
			# (else_try),
				# # Mounts: itp_type_horse, itp_type_animal
				# (this_or_next|eq, ":item_type", itp_type_horse),
				# (eq, ":item_type", itp_type_animal),
				# # Valid item.  Now determine item modifier.
				# (try_begin),
					# (assign, ":imod", imod_sturdy),
					# (ge, ":difficulty", wp_tpe_tier_2_loot),
					# (assign, ":imod", imod_heavy),
					# (ge, ":difficulty", wp_tpe_tier_3_loot),
					# (ge, ":limit", wp_tpe_final_rank_2),
					# (assign, ":imod", imod_thick),
					# (ge, ":difficulty", wp_tpe_tier_4_loot),
					# (assign, ":imod", imod_spirited),
					# (ge, ":difficulty", wp_tpe_tier_5_loot),
					# (ge, ":limit", wp_tpe_final_rank_1),
					# (assign, ":imod", imod_champion),
					# (ge, ":difficulty", wp_tpe_tier_6_loot),
					# (assign, ":imod", imod_lordly),
				# (try_end),
			# (else_try),
				# # Books: itp_type_book
				# (eq, ":item_type", itp_type_book),
				# (assign, ":imod", imod_plain),
			# (else_try),
				# # Goods: itp_type_goods
				# (eq, ":item_type", itp_type_goods),
				# # Valid item.  Now determine item modifier.
				# (try_begin),
					# (assign, ":imod", imod_plain),
					# (ge, ":difficulty", wp_tpe_tier_2_loot),
					# (assign, ":imod", imod_fine),
					# (ge, ":difficulty", wp_tpe_tier_3_loot),
					# (ge, ":limit", wp_tpe_final_rank_2),
					# (assign, ":imod", imod_well_made),
					# (ge, ":difficulty", wp_tpe_tier_4_loot),
					# (assign, ":imod", imod_superb),
					# (ge, ":difficulty", wp_tpe_tier_5_loot),
					# (ge, ":limit", wp_tpe_final_rank_1),
					# (assign, ":imod", imod_exquisite),
					# (ge, ":difficulty", wp_tpe_tier_6_loot),
					# (assign, ":imod", imod_masterwork),
				# (try_end),
			# (try_end),
		# (try_end),
		
		# # Award loot.
		# (try_begin),
			# (ge, ":item_no", 1), # Valid item
			# (eq, ":troop_no", "trp_player"),
			# (troop_add_item, ":troop_no", ":item_no", ":imod"),
		# (else_try),
			# (ge, ":item_no", 1), # Valid item
			# (is_between, ":troop_no", companions_begin, companions_end),
			# (str_store_item_name, s21, ":item_no"),
			# (str_store_troop_name, s22, ":troop_no"),
			# (troop_get_type, reg21, ":troop_no"),
			# (display_message, "@{s22} hands {reg21?her:his} {s21} prize to you."),
			# (troop_add_item, "trp_player", ":item_no", ":imod"),
		# (try_end),
		# (assign, reg1, ":item_no"), # For display.
		#### OLD SYSTEM- ####
		
	]),
	
# script_tpe_award_store_record
# PURPOSE: Stores the item & modifier information into the proper TPE AWARD array slot.
# EXAMPLE: (call_script, "script_tpe_award_store_record", ":record_no", ":item_no", ":imod"),
("tpe_award_store_record",
    [
		(store_script_param, ":record_no", 1),
		(store_script_param, ":item_no", 2),
		(store_script_param, ":imod", 3),
		
		(try_begin),
			# FILTER - Record out of acceptable range.
			(neg|is_between, ":record_no", 0, TPE_ARRAY_RECORD_LIMIT),
			(assign, reg31, ":record_no"),
			(display_message, "@ERROR (TPE) - Rewards array attempted to store information out of bounds. [Record #{reg31}]", gpu_red),
		(else_try),
			(troop_set_slot, "trp_tpe_award_item_no", ":record_no", ":item_no"),
			(troop_set_slot, "trp_tpe_award_imod_no", ":record_no", ":imod"),
			
			(try_begin),
				(ge, DEBUG_TPE_LOOT, 2),
				(assign, reg31, ":record_no"),
				(str_store_item_name, s31, ":item_no"),
				(call_script, "script_cci_describe_imod_to_s1", ":imod", 1), # cci_scripts.py
				(display_message, "@DEBUG (TPE): Record #{reg31} has stored item '{s1} {s31}'.", gpu_debug),
			(try_end),
		(try_end),
	]),
	
# script_tpe_award_get_record
# PURPOSE: Retrieves the item & modifier information from the proper TPE AWARD array slot.
# EXAMPLE: (call_script, "script_tpe_award_get_record", ":record_no"),
("tpe_award_get_record",
    [
		(store_script_param, ":record_no", 1),
		(store_script_param, reg32, 2),
		
		(try_begin),
			# FILTER - Record out of acceptable range.
			(neg|is_between, ":record_no", 0, TPE_ARRAY_RECORD_LIMIT),
			(assign, reg31, ":record_no"),
			(display_message, "@ERROR (TPE) - Rewards array attempted to obtain information out of bounds. [Record #{reg31}] @ {reg32}", gpu_red),
		(else_try),
			(troop_get_slot, ":item_no", "trp_tpe_award_item_no", ":record_no"),
			(troop_get_slot, ":imod", "trp_tpe_award_imod_no", ":record_no"),
			
			(try_begin),
				(ge, DEBUG_TPE_LOOT, 2),
				(assign, reg31, ":record_no"),
				(ge, ":item_no", 0),
				(str_store_item_name, s31, ":item_no"),
				(call_script, "script_cci_describe_imod_to_s1", ":imod", 1), # cci_scripts.py
				(display_message, "@DEBUG (TPE): Record #{reg31} has stored item '{s1} {s31}'.", gpu_debug),
			(try_end),
		(else_try),
			(assign, reg1, -1),
			(assign, reg2, imod_plain),
		(try_end),
		
		(assign, reg1, ":item_no"),
		(assign, reg2, ":imod"),
	]),
	
# script_tpe_award_clear_arrays
# PURPOSE: Sets the TPE ARRAYs to their default values.
# EXAMPLE: (call_script, "script_tpe_award_clear_arrays"),
("tpe_award_clear_arrays",
    [
		(try_for_range, ":record_no", 0, TPE_ARRAY_RECORD_LIMIT),
			(troop_set_slot, "trp_tpe_award_item_no", ":record_no", -1),
			(troop_set_slot, "trp_tpe_award_imod_no", ":record_no", imod_plain),
		(try_end),
		
		(try_begin),
			(ge, DEBUG_TPE_LOOT, 1),
			(display_message, "@DEBUG (TPE): Record arrays have been reset.", gpu_debug),
		(try_end),
	]),
	
# script_tpe_generate_prize_list
# PURPOSE: Sets the TPE ARRAYs to their default values.
# EXAMPLE: (call_script, "script_tpe_generate_prize_list", ":min_value", ":max_value"),
("tpe_generate_prize_list",
    [
		(try_begin),
			(assign, ":record_no", 0),
			(call_script, "script_tpe_award_clear_arrays"),
			(try_for_range, ":item_no", TPE_FIRST_ITEM, TPE_LAST_ITEM),
				## FILTER - ITEM TYPE
				(item_get_type, ":type", ":item_no"),
				(assign, ":continue", 0),
				(assign, ":firearm_blocked", 1),
				(try_begin), ### ONE-HANDED WEAPONS ###
					(eq, "$tpe_award_group", REWARD_GROUP_ONE_HANDED),
					(eq, ":type", itp_type_one_handed_wpn),
					(assign, ":continue", 1),
				(else_try),  ### TWO-HANDED WEAPONS ###
					(eq, "$tpe_award_group", REWARD_GROUP_TWO_HANDED),
					(eq, ":type", itp_type_two_handed_wpn),
					(assign, ":continue", 1),
				(else_try),  ### POLEARMS ###
					(eq, "$tpe_award_group", REWARD_GROUP_POLEARMS),
					(eq, ":type", itp_type_polearm),
					(assign, ":continue", 1),
				(else_try),  ### RANGED WEAPONS & AMMUNITION ###
					(this_or_next|eq, "$tpe_award_group", REWARD_GROUP_RANGED_WEAPONS),
					(eq, "$tpe_award_group", REWARD_GROUP_AMMUNITION),
					(try_begin),
						(assign, ":firearm_type", 0),
						(this_or_next|eq, ":type", itp_type_pistol),
						(this_or_next|eq, ":type", itp_type_musket),
						(eq, ":type", itp_type_bullets),
						(eq, TPE_SETTING_ALLOW_FIREARMS, 1),
						(assign, ":firearm_blocked", 0),
						(assign, ":firearm_type", 1),
					(try_end),
					(this_or_next|eq, ":type", itp_type_bow),
					(this_or_next|eq, ":type", itp_type_crossbow),
					(this_or_next|eq, ":type", itp_type_thrown),
					(this_or_next|eq, ":firearm_type", 1),
					(this_or_next|eq, ":type", itp_type_bolts),
					(eq, ":type", itp_type_arrows),
					(assign, ":continue", 1),
				(else_try),  ### SHIELDS ###
					(eq, "$tpe_award_group", REWARD_GROUP_SHIELDS),
					(eq, ":type", itp_type_shield),
					(assign, ":continue", 1),
				(else_try),  ### HELMETS ###
					(eq, "$tpe_award_group", REWARD_GROUP_HELMETS),
					(eq, ":type", itp_type_head_armor),
					(assign, ":continue", 1),
				(else_try),  ### BODY ARMOR ###
					(eq, "$tpe_award_group", REWARD_GROUP_BODY),
					(eq, ":type", itp_type_body_armor),
					(assign, ":continue", 1),
				(else_try),  ### BOOTS & GAUNTLETS ###
					(this_or_next|eq, "$tpe_award_group", REWARD_GROUP_BOOTS),
					(eq, "$tpe_award_group", REWARD_GROUP_HANDS),
					(this_or_next|eq, ":type", itp_type_foot_armor),
					(eq, ":type", itp_type_hand_armor),
					(assign, ":continue", 1),
				(else_try),  ### MOUNTS ###
					(eq, "$tpe_award_group", REWARD_GROUP_MOUNTS),
					(eq, ":type", itp_type_horse),
					(assign, ":continue", 1),
				(else_try),  ### BOOKS ###
					(eq, "$tpe_award_group", REWARD_GROUP_BOOKS),
					(eq, ":type", itp_type_book),
					(assign, ":continue", 1),
				(else_try),
					(assign, reg31, "$tpe_award_group"),
					(neq, ":firearm_blocked", 1),
					(display_message, "@ERROR (TPE Loot) - An invalid reward group has been selected.  Group = {reg31}", gpu_debug),
				(try_end),
				(eq, ":continue", 1),
				## FILTER - REGION
				# Check for generic items
				(try_begin),
					(assign, ":item_is_generic", 1),
					(try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
						(item_has_faction, ":item_no", ":faction_no"),
						(assign, ":item_is_generic", 0),
					(try_end),
				(try_end),
				(store_faction_of_party, ":faction_no", "$current_town"),
				(this_or_next|item_has_faction, ":item_no", ":faction_no"), # Specific region selected.
				(this_or_next|eq, ":item_is_generic", 1), 					# Item is in every faction.
				(eq, TPE_SETTING_USE_REGIONAL_FLAGS, 0), 					# Item region flags disabled.
				## FILTER - MERCHANDISE
				(this_or_next|ge, BETA_TESTING_MODE, 1),
				(this_or_next|eq, "$tpe_award_group", REWARD_GROUP_BOOKS),
				(this_or_next|eq, TPE_SETTING_LIMIT_TO_MERCHANDISE, 0), # Merchandise setting not required.  Setting in tpe_constants.py
				(item_has_property, ":item_no", itp_merchandise),
				
				## Now that we have filtered group vs. type we need to get a singular type back for imods.
				(call_script, "script_tpe_convert_item_type_to_award_group", ":type"),
				(assign, ":award_group", reg1),
				
				## Determine value of item cycling through imods
				(try_for_range, ":imod", TPE_IMODS_BEGIN, TPE_IMODS_END),
					(call_script, "script_cf_cci_imod_appropriate_for_item", ":award_group", ":imod"), # cci_scripts.py
					
					# Determine the value of this item / imod combination and if it is within our limits.
					(call_script, "script_cms_get_item_value_with_imod", ":item_no", ":imod", CMS_AUTO_LOOTING), # cms_scripts.py
					(assign, ":base_value", reg0),
					(val_div, ":base_value", 100),
					(this_or_next|eq, ":record_no", 0),
					(is_between, ":base_value", "$tpe_award_min_value", "$tpe_award_max_value"),
					
					# Limit things so not every imod type is available, especially for cheap items.
					(store_random_in_range, ":roll", 0, 100),
					(this_or_next|lt, ":roll", "$tpe_award_imod_availability"), # 15%
					(eq, ":imod", imod_plain),
					
					# We're keeping this item / imod combo so store it.
					(call_script, "script_tpe_award_store_record", ":record_no", ":item_no", ":imod"),
					(val_add, ":record_no", 1),
				(try_end),
				
				(troop_set_slot, TPE_OBJECTS, tpe2_val_total_records, ":record_no"),
				(assign, "$tpe_awards_lock_records", 1),
			(try_end),
		(try_end),
		
		(try_begin),
			(ge, DEBUG_TPE_LOOT, 1),
			(display_message, "@DEBUG (TPE): The prize list has been generated.", gpu_debug),
		(try_end),
	]),
	
# script_tpe_get_most_valuable_record
# PURPOSE: Sorts through all of the records and figures out which item / imod combination is the most valuable.  It returns that record #.
# EXAMPLE: (call_script, "script_tpe_get_most_valuable_record"),
("tpe_get_most_valuable_record",
    [
		(assign, ":best_record", -1),
		(assign, ":best_value", 0),
		
		# (troop_get_slot, ":total_records", TPE_OBJECTS, tpe2_val_total_records),
		(try_for_range, ":record_no", 0, TPE_ARRAY_RECORD_LIMIT),
			# Get the current record's information.
			(call_script, "script_tpe_award_get_record", ":record_no", 0),
			(assign, ":item_no", reg1),
			(assign, ":imod", reg2),
			
			# Filter for bad item data
			(ge, ":item_no", 1),
			(is_between, ":imod", TPE_IMODS_BEGIN, TPE_IMODS_END),
			
			# Determine our current record's value.
			(call_script, "script_cms_get_item_value_with_imod", ":item_no", ":imod", CMS_AUTO_LOOTING), # cms_scripts.py
			(assign, ":record_value", reg0),
			(val_div, ":record_value", 100),
			
			# Compare current record value to highest record value and store the best.
			(ge, ":record_value", ":best_value"),
			(assign, ":best_record", ":record_no"),
			(assign, ":best_value", ":record_value"),
		(try_end),
		(assign, reg1, ":best_record"),
	]),
	
# script_tpe_describe_award_group
# PURPOSE: Returns a text description of an award group for use in the awards display & prize display.
# EXAMPLE: (call_script, "script_tpe_describe_award_group", ":award_group"),
("tpe_describe_award_group",
    [
		(store_script_param, ":award_group", 1),
		
		(try_begin), ### ONE-HANDED WEAPONS ###
			(eq, ":award_group", REWARD_GROUP_ONE_HANDED),
			(str_store_string, s1, "@One Handed Weapons"),
		(else_try),  ### TWO-HANDED WEAPONS ###
			(eq, ":award_group", REWARD_GROUP_TWO_HANDED),
			(str_store_string, s1, "@Two Handed Weapons"),
		(else_try),  ### POLEARMS ###
			(eq, ":award_group", REWARD_GROUP_POLEARMS),
			(str_store_string, s1, "@Polearms"),
		(else_try),  ### RANGED WEAPONS & AMMUNITION ###
			(this_or_next|eq, ":award_group", REWARD_GROUP_RANGED_WEAPONS),
			(eq, ":award_group", REWARD_GROUP_AMMUNITION),
			(str_store_string, s1, "@Ranged Weapons"),
		(else_try),  ### SHIELDS ###
			(eq, ":award_group", REWARD_GROUP_SHIELDS),
			(str_store_string, s1, "@Shields"),
		(else_try),  ### HELMETS ###
			(eq, ":award_group", REWARD_GROUP_HELMETS),
			(str_store_string, s1, "@Helmets"),
		(else_try),  ### BODY ARMOR ###
			(eq, ":award_group", REWARD_GROUP_BODY),
			(str_store_string, s1, "@Armor"),
		(else_try),  ### BOOTS  & GAUNTLETS ###
			(this_or_next|eq, ":award_group", REWARD_GROUP_BOOTS),
			(eq, ":award_group", REWARD_GROUP_HANDS),
			(str_store_string, s1, "@Boots & Gauntlets"),
		(else_try),  ### MOUNTS ###
			(eq, ":award_group", REWARD_GROUP_MOUNTS),
			(str_store_string, s1, "@Mounts"),
		(else_try),  ### BOOKS ###
			(eq, ":award_group", REWARD_GROUP_BOOKS),
			(str_store_string, s1, "@Books"),
		(else_try),  ### UNDEFINED DEFAULT ###
			(str_store_string, s1, "@Undefined Group"),
			(assign, reg31, ":award_group"),
			(display_message, "@ERROR - An undefined award group was requested at script 'tpe_describe_award_group'.  [Group #{reg31}]", gpu_red),
		(try_end),
	]),
	
# script_tpe_convert_item_type_to_award_group
# PURPOSE: Receives an item's type and returns its prize group equivalent.
# EXAMPLE: (call_script, "script_tpe_convert_item_type_to_award_group", ":item_type"),
("tpe_convert_item_type_to_award_group",
    [
		(store_script_param, ":item_type", 1),
		
		(assign, ":award_group", -1),
		(try_begin), ### ONE-HANDED WEAPONS ###
			(eq, ":item_type", itp_type_one_handed_wpn),
			(assign, ":award_group", REWARD_GROUP_ONE_HANDED),
		(else_try),  ### TWO-HANDED WEAPONS ###
			(eq, ":item_type", itp_type_two_handed_wpn),
			(assign, ":award_group", REWARD_GROUP_TWO_HANDED),
		(else_try),  ### POLEARMS ###
			(eq, ":item_type", itp_type_polearm),
			(assign, ":award_group", REWARD_GROUP_POLEARMS),
		(else_try),  ### RANGED WEAPONS ###
			(this_or_next|eq, ":item_type", itp_type_bow),
			(this_or_next|eq, ":item_type", itp_type_crossbow),
			(this_or_next|eq, ":item_type", itp_type_thrown),
			(this_or_next|eq, ":item_type", itp_type_pistol),
			(eq, ":item_type", itp_type_musket),
			(assign, ":award_group", REWARD_GROUP_RANGED_WEAPONS),
		(else_try),  ### AMMUNITION ###
			(this_or_next|eq, ":item_type", itp_type_arrows),
			(this_or_next|eq, ":item_type", itp_type_bolts),
			(eq, ":item_type", itp_type_bullets),
			(assign, ":award_group", REWARD_GROUP_AMMUNITION),
		(else_try),  ### SHIELDS ###
			(eq, ":item_type", itp_type_shield),
			(assign, ":award_group", REWARD_GROUP_SHIELDS),
		(else_try),  ### HELMETS ###
			(eq, ":item_type", itp_type_head_armor),
			(assign, ":award_group", REWARD_GROUP_HELMETS),
		(else_try),  ### BODY ARMOR ###
			(eq, ":item_type", itp_type_body_armor),
			(assign, ":award_group", REWARD_GROUP_BODY),
		(else_try),  ### BOOTS ###
			(eq, ":item_type", itp_type_foot_armor),
			(assign, ":award_group", REWARD_GROUP_BOOTS),
		(else_try),  ### GAUNTLETS ###
			(eq, ":item_type", itp_type_hand_armor),
			(assign, ":award_group", REWARD_GROUP_HANDS),
		(else_try),  ### MOUNTS ###
			(eq, ":item_type", itp_type_horse),
			(assign, ":award_group", REWARD_GROUP_MOUNTS),
		(else_try),  ### BOOKS ###
			(eq, ":item_type", itp_type_book),
			(assign, ":award_group", REWARD_GROUP_BOOKS),
		(else_try),  ### UNDEFINED DEFAULT ###
			(assign, reg31, ":item_type"),
			(display_message, "@ERROR - An undefined item type was requested at script 'tpe_convert_item_type_to_award_group'.  [Type #{reg31}]", gpu_red),
		(try_end),
		
		(assign, reg1, ":award_group"),
	]),
# END - REWARDS & BETS SCRIPTS

###########################################################################################################################
#####                                             TOURNAMENT PARTICIPANTS                                             #####
###########################################################################################################################

# script_tpe_pick_random_participant
# Inputs:  none
# Outputs: reg1 (slot # of participant in tpe_tournament_roster)
("tpe_pick_random_participant",
	[
		(assign, ":continue", 1),
		(try_for_range, ":cur_slot", 1, wp_tpe_max_tournament_participants),
		   (eq, ":continue", 1),
		   (troop_get_slot, ":troop_no", tpe_tournament_roster, ":cur_slot"),
		   #(troop_slot_eq, ":troop_no", slot_troop_tournament_eliminated, 0),     # Not already eliminated.
		   (troop_slot_eq, ":troop_no", slot_troop_tournament_participating, 0),  # Not already picked.
		   (assign, ":continue", 0),
		   (troop_set_slot, ":troop_no", slot_troop_tournament_participating, 1),
		(try_end),
		(assign, reg0, ":troop_no"),
	]),
	
# script_tpe_fill_tournament_participants_troop
# Input: arg1 = center_no, arg2 = player_at_center
# Output: none (fills trp_tournament_participants)
("tpe_fill_tournament_participants_troop",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":player_at_center", 2),
		(assign, ":cur_slot", 1),
		(troop_set_slot, "trp_tournament_participants", 0, "trp_player"), # Valid: Initial filling companions.

		(try_begin),
			(eq, ":player_at_center", 1),
			(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
			(try_for_range, ":stack_no", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":cur_troop", "p_main_party", ":stack_no"),
				(troop_is_hero, ":cur_troop"),
				(neq, ":cur_troop", "trp_player"), # Bugfix: duplicate player filter.
				(neq, ":cur_troop", "trp_kidnapped_girl"),
				(troop_set_health, ":cur_troop", 100), # Sets everyone's health to full upon entry into the tournament.
				(neg|troop_slot_eq, ":cur_troop", slot_troop_tournament_never_spawn, 1),
				(troop_set_slot, "trp_tournament_participants", ":cur_slot", ":cur_troop"), # Valid: Initial filling companions.
				(val_add, ":cur_slot", 1),
				(troop_set_slot, ":cur_troop", slot_troop_tournament_total_points, 0),
			(else_try),
				(ge, DEBUG_TPE_general, 1),
				(is_between, ":cur_troop", companions_begin, companions_end),
				(troop_slot_eq, ":cur_troop", slot_troop_tournament_never_spawn, 1),
				(str_store_troop_name, s31, ":cur_troop"),
				(troop_get_slot, reg31, ":cur_troop", slot_troop_tournament_never_spawn),
				(display_message, "@{s31} has been prevented from entering the tournament since never spawn is {reg31?ENABLED:DISABLED}.", gpu_debug),
			(try_end),
		(try_end),
			
		(party_collect_attachments_to_party, ":center_no", "p_temp_party"),
		(party_get_num_companion_stacks, ":num_stacks", "p_temp_party"),
		(try_for_range, ":stack_no", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":cur_troop", "p_temp_party", ":stack_no"),
			(troop_is_hero, ":cur_troop"),
			(neq, ":cur_troop", "trp_player"), # Bugfix: duplicate player filter.
			(troop_set_health, ":cur_troop", 100), # Sets everyone's health to full upon entry into the tournament.
			(troop_set_slot, "trp_tournament_participants", ":cur_slot", ":cur_troop"), # Valid: Initial filling of local lords.
			(val_add, ":cur_slot", 1),
			(troop_set_slot, ":cur_troop", slot_troop_tournament_total_points, 0),
		(try_end),
	 
		(troop_set_health, "trp_player", 100), # TPE 1.5.3
		(troop_set_slot, "trp_player", slot_troop_tournament_total_points, 0),
	 
		# TPE 1.3 + Level Scaled Troops are picked here.
		(try_begin),
			(call_script, "script_tpe_initialize_xp_table"),    # This defines the xp required per level.
			
			# Here is where they get scaled up.
			(try_for_range, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end),
				(call_script, "script_tpe_name_the_scaled_troops", ":troop_no"),    # This assigns a "localized" name to each scaled troop_id.
				(call_script, "script_tpe_level_scale_troop", ":troop_no"),         # This calls the scale up script.
				(troop_set_health, ":troop_no", 100), # Sets everyone's health to full upon entry into the tournament.
				(troop_set_slot, ":troop_no", slot_troop_tournament_total_points, 0),
			(try_end),
			
			# This is used to assign these scaled troops to fill any remaining tournament spots.
			(assign, ":begin_slot", ":cur_slot"),
			(assign, ":scaled_troop", tpe_scaled_troops_begin),
			(try_for_range, ":cur_slot", ":begin_slot", wp_tpe_max_tournament_participants),
				(troop_set_slot, "trp_tournament_participants", ":cur_slot", ":scaled_troop"), # Valid: Initial filling of scaled troops.
				(val_add, ":scaled_troop", 1),
			(try_end),
		(try_end),
		# TPE 1.3 -
	]),
	 
# END - TOURNAMENT PARTICIPANTS SCRIPTS

###########################################################################################################################
#####                                                  MISCELLANEOUS                                                  #####
###########################################################################################################################

# script_tpe_end_tournament_fight
# HOOK: REPLACEMENT SCRIPT FOR NATIVE MODULE SYSTEM
# Input: arg1 = player_team_won (1 or 0)
# Output: none
("tpe_end_tournament_fight",
	[
		(store_script_param, ":player_team_won", 1),

		(assign, "$g_tournament_player_team_won", ":player_team_won"),
		(try_begin),
			(eq, "$tpe_tournament_mode", tpe_mode_elimination),
			(assign, "$g_wp_tpe_rank_pres_mode", wp_tpe_tournament_ranking),
			(jump_to_menu, "mnu_tpe_jump_to_rankings"),
		(else_try),
			(assign, "$g_wp_tpe_rank_pres_mode", wp_tpe_round_ranking),
			(jump_to_menu, "mnu_tpe_jump_to_rankings"),
		(try_end),
	]),
# END - MISCELLANEOUS SCRIPTS

###########################################################################################################################
#####                                                 ARRAY HANDLING                                                  #####
###########################################################################################################################

# script_tpe_copy_array
# Copies source array into target array.
# Input: target array, source array, limit (last cell to copy)
# Output: none
  ("tpe_copy_array",
    [
		(store_script_param, ":target_array", 1),
		(store_script_param, ":source_array", 2),
		(store_script_param, ":limit", 3),
		
		(try_for_range, ":slot_no", 0, ":limit"),
			(troop_get_slot, ":info", ":source_array", ":slot_no"),
			(troop_set_slot, ":target_array", ":slot_no", ":info"),
			### DIAGNOSTIC BEYOND THIS POINT ###
			(ge, DEBUG_TPE_general, 2),
			(lt, ":slot_no", ":limit"),
			(try_begin),
				(eq, ":slot_no", 0),
				(display_message, "@DEBUG (TPE) - ARRAY COPY ATTEMPT."),
			(try_end),
			(str_store_troop_name, s1, ":info"),
			(assign, reg1, ":slot_no"),
			(display_message, "@DEBUG (TPE): Source -> Target Copy.  Slot {reg1} = {s1}."),
		(try_end),
	]),

# script_tpe_process_round_points
# Adds points agents earn in a round to their cumulative tournament points.
# Input: none
# Output: none
  ("tpe_process_round_points",
    [
		(try_for_agents, ":agent_no"),
			(agent_is_human, ":agent_no"), # No horses allowed.
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(troop_get_slot, ":total_points", ":troop_no", slot_troop_tournament_total_points),
			(troop_get_slot, ":round_points", ":troop_no", slot_troop_tournament_round_points),
			(val_add, ":total_points", ":round_points"),
			(troop_set_slot, ":troop_no", slot_troop_tournament_total_points, ":total_points"),
			### DIAGNOSTIC BEYOND THIS POINT ###
			(ge, DEBUG_TPE_general, 2),
			(str_store_troop_name, s1, ":troop_no"),
			(assign, reg1, ":round_points"),
			(assign, reg2, ":total_points"),
			(display_message, "@DEBUG (TPE): {s1} gained {reg1} of {reg2} total points this round."),
		(try_end),
	]),
	
# script_tpe_sort_troops_and_points (new sort from bottom up)
# Receives an array of troops and their associated points and sorts them out.
# Input: source troops slot (round/static)
# Output: tpe_ranking_array (trp_tpe_array_sorted_troops)
  ("tpe_sort_troops_and_points",
    [
		(store_script_param, ":sorted_slot", 1),
		
		(call_script, "script_tpe_copy_array", tpe_ranking_array, tpe_tournament_roster, wp_tpe_max_tournament_participants),
			
		#(assign, ":player_found", 0),
		# Sort the listed arrays.
		(try_for_range, ":limiter", 0, wp_tpe_max_tournament_participants),
			(store_sub, ":limit", wp_tpe_max_tournament_participants, ":limiter"),
			(try_for_range, ":slot_current", 0, ":limit"),
				# Get current troop data.
				(troop_get_slot, ":troop_current", tpe_ranking_array, ":slot_current"),
				(troop_get_slot, ":points_current", ":troop_current", ":sorted_slot"),
				# Get next troop data.
				(store_add, ":slot_next", ":slot_current", 1),
				(troop_get_slot, ":troop_next", tpe_ranking_array, ":slot_next"),
				(troop_get_slot, ":points_next", ":troop_next", ":sorted_slot"),
				# Compare which is higher.
				(lt, ":points_current", ":points_next"),
	
				# (this_or_next|neq, ":troop_lesser", "trp_player"),
				# (eq, ":player_found", 0),
				
				####### DIAGNOSTIC BEGIN #######
				# (str_store_troop_name, s1, ":troop_next"),
				# (str_store_troop_name, s2, ":troop_current"),
				# (assign, reg1, ":slot_current"),
				# (assign, reg2, ":slot_next"),
				# (assign, reg3, ":points_current"),
				# (assign, reg4, ":points_next"),
				# (display_message, "@DEBUG (TPE): {s1}/{reg4} moved from slot #{reg2}->{reg1} displacing {s2}/{reg3}."),
				####### DIAGNOSTIC END #######
				
				# Okay, next troop is higher in score than current troop so switch places.
				(troop_set_slot, tpe_ranking_array, ":slot_current", ":troop_next"),
				(troop_set_slot, tpe_ranking_array, ":slot_next", ":troop_current"),
				(assign, ":points_current", ":points_next"),
				(assign, ":troop_current", ":troop_next"),
			(try_end),
			# (try_begin),
				# (eq, ":troop_higher", "trp_player"),
				# (assign, ":player_found", 1),
			# (try_end),
		(try_end),
		
		### DIAGNOSTIC
		(try_for_range, ":rank", 0, wp_tpe_max_tournament_participants),
			(ge, DEBUG_TPE_general, 2),
			(lt, ":rank", 5),
			(troop_get_slot, ":troop_no", tpe_ranking_array, ":rank"),
			(troop_get_slot, reg1, ":troop_no", ":sorted_slot"),
			(str_store_troop_name, s1, ":troop_no"),
			(assign, reg2, ":rank"),
			(display_message, "@DEBUG (TPE sort): Rank {reg2} is {s1} with {reg1} points."),
		(try_end),
	]),
	
# script_tpe_sort_troops_and_points_without_player (new sort from bottom up)
# Receives an array of troops and their associated points and sorts them out, but finishes by putting the player at the top.  This is an attempt to fix a ranking bug.
# Input: source troops slot (round/static)
# Output: tpe_ranking_array (trp_tpe_array_sorted_troops)
  ("tpe_sort_troops_and_points_without_player",
    [
		(store_script_param, ":sorted_slot", 1),
		
		(call_script, "script_tpe_copy_array", tpe_ranking_array, tpe_tournament_roster, wp_tpe_max_tournament_participants),
			
		#(assign, ":player_found", 0),
		# Sort the listed arrays.
		(try_for_range, ":limiter", 0, wp_tpe_max_tournament_participants),
			(store_sub, ":limit", wp_tpe_max_tournament_participants, ":limiter"),
			(try_for_range, ":slot_current", 0, ":limit"),
				# Get current troop data.
				(troop_get_slot, ":troop_current", tpe_ranking_array, ":slot_current"),
				(troop_get_slot, ":points_current", ":troop_current", ":sorted_slot"),
				# Get next troop data.
				(store_add, ":slot_next", ":slot_current", 1),
				(troop_get_slot, ":troop_next", tpe_ranking_array, ":slot_next"),
				(troop_get_slot, ":points_next", ":troop_next", ":sorted_slot"),
				# Compare which is higher.
				(this_or_next|eq, ":troop_next", "trp_player"),
				(lt, ":points_current", ":points_next"),
				(neq, ":troop_current", "trp_player"),
				
				# (this_or_next|neq, ":troop_lesser", "trp_player"),
				# (eq, ":player_found", 0),
				
				####### DIAGNOSTIC BEGIN #######
				# (str_store_troop_name, s1, ":troop_next"),
				# (str_store_troop_name, s2, ":troop_current"),
				# (assign, reg1, ":slot_current"),
				# (assign, reg2, ":slot_next"),
				# (assign, reg3, ":points_current"),
				# (assign, reg4, ":points_next"),
				# (display_message, "@DEBUG (TPE): {s1}/{reg4} moved from slot #{reg2}->{reg1} displacing {s2}/{reg3}."),
				####### DIAGNOSTIC END #######
				
				# Okay, next troop is higher in score than current troop so switch places.
				(troop_set_slot, tpe_ranking_array, ":slot_current", ":troop_next"),
				(troop_set_slot, tpe_ranking_array, ":slot_next", ":troop_current"),
				(assign, ":points_current", ":points_next"),
				(assign, ":troop_current", ":troop_next"),
			(try_end),
			# (try_begin),
				# (eq, ":troop_higher", "trp_player"),
				# (assign, ":player_found", 1),
			# (try_end),
		(try_end),
		
		### DIAGNOSTIC
		(try_for_range, ":rank", 0, wp_tpe_max_tournament_participants),
			(ge, DEBUG_TPE_general, 1),
			(lt, ":rank", 5),
			(troop_get_slot, ":troop_no", tpe_ranking_array, ":rank"),
			(troop_get_slot, reg1, ":troop_no", ":sorted_slot"),
			(str_store_troop_name, s1, ":troop_no"),
			(assign, reg2, ":rank"),
			(display_message, "@DEBUG (TPE sort): Rank {reg2} is {s1} with {reg1} points."),
		(try_end),
	]),
# END - ARRAY HANDLING SCRIPTS

###########################################################################################################################
#####                                              PRESENTATION SCRIPTS                                               #####
###########################################################################################################################

# script_tpe_get_faction_image
# Clears out all award data each round.
# Input: none
# Output: none
  ("tpe_get_faction_image",
    [
		(store_script_param, ":troop_no", 1),
		
		(try_begin),
			(is_between, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end),
			(troop_get_slot, ":troop_faction", ":troop_no", slot_troop_original_faction),
			(try_begin),
				(eq, ":troop_faction", "fac_commoners"),
				(call_script, "script_tpe_store_town_faction_to_reg0", "$current_town"),
				(assign, ":troop_faction", reg0),
				# (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
				# (store_troop_faction, ":lord_faction", ":town_lord"),
				# (assign, ":troop_faction", ":lord_faction"),
			(try_end),
			(try_begin),
				(eq, ":troop_faction", "fac_kingdom_1"),             (store_random_in_range, ":troop_image", tpe_faction_1_lords_begin, tpe_faction_1_lords_end),
				(else_try), (eq, ":troop_faction", "fac_kingdom_2"), (store_random_in_range, ":troop_image", tpe_faction_2_lords_begin, tpe_faction_2_lords_end),
				(else_try), (eq, ":troop_faction", "fac_kingdom_3"), (store_random_in_range, ":troop_image", tpe_faction_3_lords_begin, tpe_faction_3_lords_end),
				(else_try), (eq, ":troop_faction", "fac_kingdom_4"), (store_random_in_range, ":troop_image", tpe_faction_4_lords_begin, tpe_faction_4_lords_end),
				(else_try), (eq, ":troop_faction", "fac_kingdom_5"), (store_random_in_range, ":troop_image", tpe_faction_5_lords_begin, tpe_faction_5_lords_end),
				(else_try), (eq, ":troop_faction", "fac_kingdom_6"), (store_random_in_range, ":troop_image", tpe_faction_6_lords_begin, tpe_faction_6_lords_end),
				(else_try),                                          (store_random_in_range, ":troop_image", tpe_faction_1_lords_begin, tpe_faction_6_lords_end),
				(ge, DEBUG_TPE_general, 1),
				(str_store_faction_name, s31, ":troop_faction"),
				(str_store_troop_name, s32, ":troop_no"),
				(display_message, "@DEBUG (TPE): Faction ({s31}) not found.  Default faction value used for {s32}."),
			(try_end),
		(else_try),
			(assign, ":troop_image", ":troop_no"),
		(try_end),
		
		(assign, reg1, ":troop_image"),
	]),
	
# script_tpe_difficulty_slider_effects
# Stores agent information, troop information and initializes points.
# Input: difficulty (int)
# Output: s1 (difficulty text), reg4 (payout bonus %)
  ("tpe_difficulty_slider_effects",
    [
		(store_script_param, ":value", 1),
		
		# Determine if set to random
		(try_begin),
			(this_or_next|eq, ":value", 0),
			(troop_slot_eq, "trp_tpe_presobj", tpe_random_diff_enabled, 1),
			# The following setup is designed to weight random rolls with higher numbers of participants at lower tiers.
			(assign, ":random_total", 0),
			(try_for_range, ":unused", 0, 5),
				(store_random_in_range, ":roll", 1, 7),
				(val_add, ":random_total", ":roll"),
			(try_end),
			(assign, ":tier_check", "$g_tournament_cur_tier"),
			(val_max, ":tier_check", 1), # To prevent div/0 errors.
			(val_div, ":random_total", ":tier_check"),
			(val_min, ":random_total", 24),
			(assign, ":value", ":random_total"),
			(troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, ":value"),
		(try_end),
		
		# Determine the size of each teams
		(try_begin),
			(this_or_next|eq, ":value", 1),
			(this_or_next|eq, ":value", 2),
			(eq, ":value", 4),
			(assign, "$g_tournament_next_team_size", 1),
		(else_try),
			(this_or_next|eq, ":value", 3),
			(this_or_next|eq, ":value", 6),
			(eq, ":value", 9),
			(assign, "$g_tournament_next_team_size", 2),
		(else_try),
			(this_or_next|eq, ":value", 5),
			(this_or_next|eq, ":value", 10),
			(eq, ":value", 15),
			(assign, "$g_tournament_next_team_size", 3),
		(else_try),
			(this_or_next|eq, ":value", 7),
			(this_or_next|eq, ":value", 13),
			(eq, ":value", 17),
			(assign, "$g_tournament_next_team_size", 4),
		(else_try),
			(this_or_next|eq, ":value", 8),
			(this_or_next|eq, ":value", 16),
			(eq, ":value", 20),
			(assign, "$g_tournament_next_team_size", 5),
		(else_try),
			(this_or_next|eq, ":value", 11),
			(this_or_next|eq, ":value", 18),
			(eq, ":value", 22),
			(assign, "$g_tournament_next_team_size", 6),
		(else_try),
			(this_or_next|eq, ":value", 12),
			(this_or_next|eq, ":value", 19),
			(eq, ":value", 23),
			(assign, "$g_tournament_next_team_size", 7),
		(else_try),
			(this_or_next|eq, ":value", 14),
			(this_or_next|eq, ":value", 21),
			(eq, ":value", 24),
			(assign, "$g_tournament_next_team_size", 8),
		(else_try),
			(try_begin), (display_message, "@ERROR (TPE): Difficulty slider position invalid.  Default team size = 3.", wp_purple), (try_end),
			(assign, "$g_tournament_next_team_size", 3),
		(try_end),
		
		# Determine the number of teams
		(try_begin),
			(this_or_next|eq, ":value", 1),
			(this_or_next|eq, ":value", 3),
			(this_or_next|eq, ":value", 5),
			(this_or_next|eq, ":value", 7),
			(this_or_next|eq, ":value", 8),
			(this_or_next|eq, ":value", 11),
			(this_or_next|eq, ":value", 12),
			(eq, ":value", 14),
			(assign, "$g_tournament_next_num_teams", 2),
		(else_try),
			(this_or_next|eq, ":value", 2),
			(this_or_next|eq, ":value", 6),
			(this_or_next|eq, ":value", 10),
			(this_or_next|eq, ":value", 13),
			(this_or_next|eq, ":value", 16),
			(this_or_next|eq, ":value", 18),
			(this_or_next|eq, ":value", 19),
			(eq, ":value", 21),
			(assign, "$g_tournament_next_num_teams", 3),
		(else_try),
			(this_or_next|eq, ":value", 4),
			(this_or_next|eq, ":value", 9),
			(this_or_next|eq, ":value", 15),
			(this_or_next|eq, ":value", 17),
			(this_or_next|eq, ":value", 20),
			(this_or_next|eq, ":value", 22),
			(this_or_next|eq, ":value", 23),
			(eq, ":value", 24),
			(assign, "$g_tournament_next_num_teams", 4),
		(else_try),
			(try_begin), (display_message, "@ERROR (TPE): Difficulty slider position invalid.  Default team number = 3.", wp_purple), (try_end),
			(assign, "$g_tournament_next_num_teams", 3),
		(try_end),
		
		(try_begin),
			(this_or_next|eq, ":value", 0),
			(troop_slot_eq, "trp_tpe_presobj", tpe_random_diff_enabled, 1),
			(str_store_string, s1, "@Random"),
			(assign, ":color", 0xDDDDDD),
		(else_try),
			(ge, ":value", 17),
			(str_store_string, s1, "@Hard"),
			(assign, ":color", wp_red),
		(else_try),
			(ge, ":value", 9),
			(str_store_string, s1, "@Normal"),
			(assign, ":color", wp_yellow),
		(else_try),
			(str_store_string, s1, "@Easy"),
			(assign, ":color", wp_green),
		(try_end),
		
		# Set payout bonus %
		(try_begin),
			(eq, wp_tpe_mod_opt_payout_bonus, 1),
			(store_mul, reg4, ":value", wp_tpe_payout_factor),
		(try_end),
		(assign, reg5, ":color"),
	]),
	
# script_tpe_difficulty_display_info
# This updates the infobox display on the options page when you update the difficulty slider.
# Input: none
# Output: s1 (Difficulty title), s2 (difficulty setting info)
  ("tpe_difficulty_display_info",
    [
		(troop_get_slot, ":diff_setting", TPE_OPTIONS, tpe_val_diff_setting),
		(try_begin),
			(this_or_next|eq, ":diff_setting", 0),
			(troop_slot_eq, "trp_tpe_presobj", tpe_random_diff_enabled, 1),
			(str_store_string, s2, "@Random team number and size"),
		(else_try),
			(assign, reg2, "$g_tournament_next_num_teams"),
			(assign, reg3, "$g_tournament_next_team_size"),
			(str_store_string, s2, "@Match: {reg2} teams of {reg3} members"),
		(try_end),
		
		(assign, ":extra_lines", 0),
		(try_begin),
			(eq, wp_tpe_mod_opt_payout_bonus, 1),
			(ge, ":diff_setting", 1),
			(store_mul, reg2, ":diff_setting", wp_tpe_payout_factor),
			(str_store_string, s2, "@{s2}^Payout Bonus +{reg2}%"),
			(val_add, ":extra_lines", 1),
		(try_end),
		
		# (try_begin),
			# (ge, ":diff_setting", 9),
			# (ge, wp_tpe_released_version, 200),
			# (str_store_string, s2, "@{s2}^AI Upgrade - Will remount"),
			# (val_add, ":extra_lines", 1),
		# (try_end),
		
		# (try_begin),
			# (ge, ":diff_setting", 17),
			# (ge, wp_tpe_released_version, 200),
			# (str_store_string, s2, "@{s2}^AI Upgrade - Focus fire"),
			# (val_add, ":extra_lines", 1),
		# (try_end),
		
		(try_for_range, ":unused", ":extra_lines", 5),
			(str_store_string, s2, "@{s2}^"),
		(try_end),
		
		(str_store_string, s1, "@Difficulty Settings"),
	]),
# END - OPTIONS PRESENTATION SCRIPTS

###########################################################################################################################
#####                                               NOBILITY REACTIONS                                                #####
###########################################################################################################################
	
# script_tpe_rep_gain_ladies
# This section implements the "Lady Reactions" feature.
# Inputs: None
# Output: None
  ("tpe_rep_gain_ladies",
    [
		# Raises relation with Ladies that are (present).  More so if in courtship.
		(try_for_range, ":troop_npc", kingdom_ladies_begin, kingdom_ladies_end),
			(troop_slot_eq, ":troop_npc", slot_troop_cur_center, "$current_town"), # For the Ladies.
			(neq, ":troop_npc", "trp_knight_1_1_wife"),
			
			(call_script, "script_tpe_noble_reaction_to_win", ":troop_npc"),
			(call_script, "script_troop_get_player_relation", ":troop_npc"),
			(assign, ":relation", reg0),
			(assign, ":relation_gain", 0),
			
			# Limit gains during a feast. (+/- 1)
			(try_begin),
				(store_faction_of_party, ":center_faction", "$current_town"),
				(faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
				(faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
				(val_clamp, reg12, -1, 2),
				(val_clamp, reg14, -1, 2),
			(try_end),
			
			# What is this lady's disposition towards you already?
			(try_begin),
				(ge, ":relation", wp_tpe_min_relation_to_be_lady_friend),
				(val_add, ":relation_gain", reg12),
			(else_try),
				(le, ":relation", wp_tpe_min_relation_to_be_lady_rival),
				(val_sub, ":relation_gain", reg14),
			(try_end),
			
			# Are you in a courtship with this lady?
			(try_begin),
				(troop_slot_ge, ":troop_npc", slot_troop_courtship_state, 2),
				(troop_slot_eq, "trp_player", slot_troop_spouse, -1), # Make sure you are not married.
				(val_add, ":relation_gain", wp_tpe_bonus_relation_for_courtship),
			(try_end),
			(call_script, "script_change_player_relation_with_troop", ":troop_npc", ":relation_gain", 0),
		(try_end),
	]),
	
# script_tpe_rep_gain_lords
# This section implements the "Lord Reactions" feature.
# Inputs: None
# Output: None
  ("tpe_rep_gain_lords",
    [
		# Alters your relation with lords that are present based upon your current relationship with them.
		(party_collect_attachments_to_party, "$current_town", "p_temp_party"),
		(party_get_num_companion_stacks,":party_stacks","p_temp_party"),
		(try_for_range, ":stack_no", 0, ":party_stacks"),
			(party_stack_get_troop_id,":troop_in_party","p_temp_party",":stack_no"),
			(troop_is_hero, ":troop_in_party"),
			(neg|main_party_has_troop, ":troop_in_party"), # Removed companions from this benefit.
			(call_script, "script_tpe_noble_reaction_to_win", ":troop_in_party"),
			(call_script, "script_troop_get_player_relation", ":troop_in_party"),
			(assign, ":relation", reg0),
			(assign, ":relation_gain", 0),
			
			# Limit gains during a feast. (+/- 2)
			(try_begin),
				(store_faction_of_party, ":center_faction", "$current_town"),
				(faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
				(faction_slot_eq, ":center_faction", slot_faction_ai_object, "$current_town"),
				(val_clamp, reg11, -1, 2),
				(val_clamp, reg13, -1, 2),
			(try_end),
			
			# What is this lord's disposition towards you already?
			(try_begin),
				(ge, ":relation", wp_tpe_min_relation_to_be_lord_friend),
				(val_add, ":relation_gain", reg11),
			(else_try),
				(le, ":relation", wp_tpe_min_relation_to_be_lord_rival),
				(val_sub, ":relation_gain", reg13),
			(try_end),
			
			# Is this troop your vassal?
			(try_begin),
				(store_troop_faction, ":faction_noble", ":troop_in_party"),
				(faction_slot_eq, ":faction_noble", slot_faction_leader, "trp_player"),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"), # Player is hosting the tournament.
				(val_add, ":relation_gain", wp_tpe_bonus_relation_from_vassals),
			(else_try),
				(store_troop_faction, ":faction_noble", ":troop_in_party"),
				(eq, ":faction_noble", "$players_kingdom"),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"), # Player is hosting the tournament.
				(val_add, ":relation_gain", 1),
			(try_end),
				
			(try_begin),
				(ge, DEBUG_TPE_general, 1),
				(str_store_troop_name, s1, ":troop_in_party"),
				(str_store_party_name, s2, "$current_town"),
				(display_message, "@DEBUG (TPE): {s1} was found in {s2}, but relation was too neutral to matter."),
			(try_end),

			(call_script, "script_change_player_relation_with_troop", ":troop_in_party", ":relation_gain", 0),
		(try_end),
	]),
	
# script_tpe_noble_reaction_to_win
# Figures out what your persistent bet is and places it accordingly each round.
# Input: troop_id (noble)
# Output: reg11 (lord gain), reg12 (lady gain), reg13 (lord loss), reg14 (lady loss)
  ("tpe_noble_reaction_to_win",
    [
		(store_script_param, ":troop_noble", 1),
		# Determine noble's personality type.
		(troop_get_slot, ":personality", ":troop_noble", slot_lord_reputation_type),

		# Clear outcome variables.
		(assign, reg11, 0),
		(assign, reg12, 0),
		(assign, reg13, 0),
		(assign, reg14, 0),
		
		# Figure out what the outcomes should be based on personality type.
		(try_begin), ##### MARTIAL #####
			(eq, ":personality", lrep_martial),
			(assign, reg11, wp_tpe_gain_vs_martial_for_male),
			(assign, reg12, wp_tpe_gain_vs_martial_for_female),
			(assign, reg13, wp_tpe_loss_vs_martial_for_male),
			(assign, reg14, wp_tpe_loss_vs_martial_for_female),
			
		(else_try), ##### QUARRELSOME #####
			(eq, ":personality", lrep_quarrelsome),
			(assign, reg11, wp_tpe_gain_vs_quarrelsome_for_male),
			(assign, reg12, wp_tpe_gain_vs_quarrelsome_for_female),
			(assign, reg13, wp_tpe_loss_vs_quarrelsome_for_male),
			(assign, reg14, wp_tpe_loss_vs_quarrelsome_for_female),
			
		(else_try), ##### SELF-RIGHTEOUS #####
			(eq, ":personality", lrep_selfrighteous),
			(assign, reg11, wp_tpe_gain_vs_selfrighteous_for_male),
			(assign, reg12, wp_tpe_gain_vs_selfrighteous_for_female),
			(assign, reg13, wp_tpe_loss_vs_selfrighteous_for_male),
			(assign, reg14, wp_tpe_loss_vs_selfrighteous_for_female),
			
		(else_try), ##### CUNNING #####
			(eq, ":personality", lrep_cunning),
			(assign, reg11, wp_tpe_gain_vs_cunning_for_male),
			(assign, reg12, wp_tpe_gain_vs_cunning_for_female),
			(assign, reg13, wp_tpe_loss_vs_cunning_for_male),
			(assign, reg14, wp_tpe_loss_vs_cunning_for_female),
			
		(else_try), ##### DEBAUCHED #####
			(eq, ":personality", lrep_debauched),
			(assign, reg11, wp_tpe_gain_vs_debauched_for_male),
			(assign, reg12, wp_tpe_gain_vs_debauched_for_female),
			(assign, reg13, wp_tpe_loss_vs_debauched_for_male),
			(assign, reg14, wp_tpe_loss_vs_debauched_for_female),
			
		(else_try), ##### GOOD NATURED #####
			(eq, ":personality", lrep_goodnatured),
			(assign, reg11, wp_tpe_gain_vs_goodnatured_for_male),
			(assign, reg12, wp_tpe_gain_vs_goodnatured_for_female),
			(assign, reg13, wp_tpe_loss_vs_goodnatured_for_male),
			(assign, reg14, wp_tpe_loss_vs_goodnatured_for_female),
			
		(else_try), ##### UPSTANDING #####
			(eq, ":personality", lrep_upstanding),
			(assign, reg11, wp_tpe_gain_vs_upstanding_for_male),
			(assign, reg12, wp_tpe_gain_vs_upstanding_for_female),
			(assign, reg13, wp_tpe_loss_vs_upstanding_for_male),
			(assign, reg14, wp_tpe_loss_vs_upstanding_for_female),
			
		(else_try), ##### ROGUISH #####
			(eq, ":personality", lrep_roguish),
			(assign, reg11, wp_tpe_gain_vs_roguish_for_male),
			(assign, reg12, wp_tpe_gain_vs_roguish_for_female),
			(assign, reg13, wp_tpe_loss_vs_roguish_for_male),
			(assign, reg14, wp_tpe_loss_vs_roguish_for_female),
			
		(else_try), ##### BENEFACTOR #####
			(eq, ":personality", lrep_benefactor),
			(assign, reg11, wp_tpe_gain_vs_benefactor_for_male),
			(assign, reg12, wp_tpe_gain_vs_benefactor_for_female),
			(assign, reg13, wp_tpe_loss_vs_benefactor_for_male),
			(assign, reg14, wp_tpe_loss_vs_benefactor_for_female),
			
		(else_try), ##### CUSTODIAN #####
			(eq, ":personality", lrep_custodian),
			(assign, reg11, wp_tpe_gain_vs_custodian_for_male),
			(assign, reg12, wp_tpe_gain_vs_custodian_for_female),
			(assign, reg13, wp_tpe_loss_vs_custodian_for_male),
			(assign, reg14, wp_tpe_loss_vs_custodian_for_female),
			
		(else_try), ##### CONVENTIONAL #####
			(eq, ":personality", lrep_conventional),
			(assign, reg11, wp_tpe_gain_vs_conventional_for_male),
			(assign, reg12, wp_tpe_gain_vs_conventional_for_female),
			(assign, reg13, wp_tpe_loss_vs_conventional_for_male),
			(assign, reg14, wp_tpe_loss_vs_conventional_for_female),
			
		(else_try), ##### ADVENTUROUS #####
			(eq, ":personality", lrep_adventurous),
			(assign, reg11, wp_tpe_gain_vs_adventurous_for_male),
			(assign, reg12, wp_tpe_gain_vs_adventurous_for_female),
			(assign, reg13, wp_tpe_loss_vs_adventurous_for_male),
			(assign, reg14, wp_tpe_loss_vs_adventurous_for_female),
			
		(else_try), ##### OTHERWORLDLY #####
			(eq, ":personality", lrep_otherworldly),
			(assign, reg11, wp_tpe_gain_vs_otherworldly_for_male),
			(assign, reg12, wp_tpe_gain_vs_otherworldly_for_female),
			(assign, reg13, wp_tpe_loss_vs_otherworldly_for_male),
			(assign, reg14, wp_tpe_loss_vs_otherworldly_for_female),
			
		(else_try), ##### AMBITIOUS #####
			(eq, ":personality", lrep_ambitious),
			(assign, reg11, wp_tpe_gain_vs_ambitious_for_male),
			(assign, reg12, wp_tpe_gain_vs_ambitious_for_female),
			(assign, reg13, wp_tpe_loss_vs_ambitious_for_male),
			(assign, reg14, wp_tpe_loss_vs_ambitious_for_female),
			
		(else_try), ##### MORALIST #####
			(eq, ":personality", lrep_moralist),
			(assign, reg11, wp_tpe_gain_vs_moralist_for_male),
			(assign, reg12, wp_tpe_gain_vs_moralist_for_female),
			(assign, reg13, wp_tpe_loss_vs_moralist_for_male),
			(assign, reg14, wp_tpe_loss_vs_moralist_for_female),
		(try_end),
	]),
# END - NOBILITY REACTIONS

###########################################################################################################################
#####                                                IN-COMBAT DISPLAY                                                #####
###########################################################################################################################

# script_tpe_update_team_points
# Supports the In-Combat Display by updating how many points each team has totaled.
# Input: team_no
# Output: none
  ("tpe_update_team_points",
    [
		(store_script_param_1, ":team_no"),
		(assign, ":tally_points", 0),
		(try_for_agents, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_get_team, ":team_check", ":agent_no"),
			(eq, ":team_no", ":team_check"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(troop_get_slot, ":troop_points", ":troop_no", slot_troop_tournament_round_points),
			(val_add, ":tally_points", ":troop_points"),
		(try_end),
		
		# Update team points storage
		(store_add, ":slot_team_points", tpe_icd_team_0_points, ":team_no"),
		(troop_set_slot, "trp_tpe_presobj", ":slot_team_points", ":tally_points"),
		
		# Update team points display
		(store_add, ":obj_team_slot", tpe_obj_team_0_points, ":team_no"),
		(troop_get_slot, ":obj_team_points", "trp_tpe_presobj", ":obj_team_slot"),
		(assign, reg1, ":tally_points"),
		(overlay_set_text, ":obj_team_points", "@{reg1}"),
		(overlay_set_color, ":obj_team_points", wp_white),
			
	]),

# script_tpe_set_display_color
# Supports the In-Combat Display presentation by coloring team member variables based on people left.
# Input: value, presentation_obj_no
# Output: none
  # ("tpe_set_display_color",
    # [
		# (store_script_param, ":members", 1),
		# (store_script_param, ":object",  2),
		# (val_mul, ":members", 100),
		# (store_div, ":value_percent", ":members", "$g_wp_tpe_team_size"),
		# (try_begin),
			# (ge, ":value_percent", 66),
			# (overlay_set_color, ":object", 0xFFAAFFAA), # Green
		# (else_try),
			# (ge, ":value_percent", 33),
			# (overlay_set_color, ":object", 0xFFFFFFAA), # Yellow
		# (else_try),
			# (overlay_set_color, ":object", 0xFFFFAAAA), # Red
		# (try_end),
	# ]),
	
# script_tpe_create_ranking_box
# Supports "Ranking Display" by creating a box with the rank, troop name, his picture, faction and points.
# Input: type, troop, points, rank, (pos x, pos y) for where to set the bottom left corner.
# Output: none
	("tpe_create_ranking_box",
	  [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":points",   2),
		(store_script_param, ":rank",     3),
		(store_script_param, ":team",     4),
		
		# Define presentation object slots.  These are used with trp_tpe_presobj
		(store_mul, ":slot_base", ":rank", 10),
		(val_add, ":slot_base", 90),              # This should make rank 1 box go to slot 100, rank 2 box start at 110, etc.
		(store_add, ":slot_rank", ":slot_base",   1), # Slot **1
		(store_add, ":slot_image", ":slot_base",  2), # Slot **2
		(store_add, ":slot_name", ":slot_base",   3), # Slot **3
		(store_add, ":slot_title", ":slot_base",  4), # Slot **4
		(store_add, ":slot_points", ":slot_base", 5), # Slot **5
		(store_add, ":slot_pos_x", ":slot_base",  6), # Slot **6
		(store_add, ":slot_pos_y", ":slot_base",  7), # Slot **7
		(store_add, ":slot_type", ":slot_base",   8), # Slot **8
		#(store_add, ":slot_award", ":slot_base",  9), # Slot **9
		
		(troop_get_slot, ":pos_x", "trp_tpe_presobj", ":slot_pos_x"),
		(troop_get_slot, ":pos_y", "trp_tpe_presobj", ":slot_pos_y"),
		(troop_get_slot, ":type", "trp_tpe_presobj", ":slot_type"),
		
		(try_begin),
			(neg|is_presentation_active, "prsnt_tpe_team_display"),
			(eq, ":type", wp_tpe_icd_rank),
			(start_presentation, "prsnt_tpe_team_display"),
		(try_end),
		
		# Define coordinates
		(assign, ":pos_x_left", ":pos_x"),                        # X - This is the left side of the box.
		(store_add, ":pos_x_right", ":pos_x", 375),               # X - This is the right side of the box.
		(store_add, ":pos_x_image", ":pos_x", 50),                # X - This is the left side of the image.
		(store_add, ":pos_x_name", ":pos_x", 100),                 # X - This is the left alignment of the name & faction lines.
		(store_add, ":pos_x_points", ":pos_x", 325),              # X - This is the left alignment of the points.
		(store_add, ":pos_y_top", ":pos_y", 50),                  # Y - This is the top side of the box.
		(assign, ":pos_y_bottom", ":pos_y"),                      # Y - This is the bottom side of the box.
		(store_add, ":pos_y_name", ":pos_y", 25),                 # Y - This is the height of the name line.
		(assign, ":thick", 2),                                    # Sets how thick the lines are.
		(store_sub, ":x_length", ":pos_x_right", ":pos_x_left"),  # Sets the size of the horizontal lines.
		(val_add, ":x_length", ":thick"),                         # Corrects so top right corner isn't missing.
		(store_sub, ":y_length", ":pos_y_top", ":pos_y_bottom"),  # Sets the size of the vertical lines.
		(assign, ":portrait_size", 147),                          # Sets the square size of the troop portrait.
		(store_add, ":pos_y_text1", ":pos_y_name", ":pos_y_top"), # Sets the height for the character's name.
		(val_div, ":pos_y_text1", 2),
		(val_sub, ":pos_y_text1", ":thick"),
		(store_add, ":pos_y_text2", ":pos_y_name", ":pos_y_bottom"), # Sets the height for the character's faction.
		(val_div, ":pos_y_text2", 2),
		(val_sub, ":pos_y_text2", ":thick"),
		(store_sub, ":pos_y_rank", ":pos_y_name", ":thick"),
		(store_sub, ":x_length_title", ":pos_x_points", ":pos_x_name"),
		(store_add, ":pos_x_rank", ":pos_x_left", ":pos_x_image"),
		(val_div, ":pos_x_rank", 2),
		(store_add, ":pos_x_pts", ":pos_x_points", ":pos_x_right"),
		(val_div, ":pos_x_pts", 2),
		(assign, ":pos_x_left_border", ":pos_x_left"),
		(try_begin),
			(eq, ":type", wp_tpe_icd_round_rank),
			(store_sub, ":x_length", ":pos_x_right", ":pos_x_image"),  # Sets the size of the horizontal lines.
			(val_add, ":x_length", ":thick"),                          # Corrects so top right corner isn't missing.
			(assign, ":pos_x_left_border", ":pos_x_image"),
		(try_end),
		
		# Internal background
		(call_script, "script_tpe_draw_line", ":x_length", ":y_length", ":pos_x_left_border", ":pos_y_bottom", 0xFF060606),# - Divides name & faction.
		(overlay_set_alpha, reg1, 0x66),
		# Outer border lines
		(call_script, "script_tpe_draw_line", ":x_length", ":thick", ":pos_x_left_border", ":pos_y_top", wp_black),       # - top border
		(call_script, "script_tpe_draw_line", ":x_length", ":thick", ":pos_x_left_border", ":pos_y_bottom", wp_black),    # - bottom border
		(call_script, "script_tpe_draw_line", ":thick", ":y_length", ":pos_x_left_border", ":pos_y_bottom", wp_black),    # | left border	
		(call_script, "script_tpe_draw_line", ":thick", ":y_length", ":pos_x_right", ":pos_y_bottom", wp_black),          # | right border
		# Internal border lines
		(call_script, "script_tpe_draw_line", ":thick", ":y_length", ":pos_x_image", ":pos_y_bottom", wp_black),          # | Divides rank & image.
		(call_script, "script_tpe_draw_line", ":thick", ":y_length", ":pos_x_name", ":pos_y_bottom", wp_black),           # | Divides image & titles.
		(call_script, "script_tpe_draw_line", ":thick", ":y_length", ":pos_x_points", ":pos_y_bottom", wp_black),         # | Divides titles & points.
		(call_script, "script_tpe_draw_line", ":x_length_title", ":thick", ":pos_x_name", ":pos_y_name", wp_black),       # - Divides name & faction.
		
		(try_begin),
			(eq, ":type", wp_tpe_icd_rank),
			# Rank Display
			(position_set_x, pos1, ":pos_x_rank"),
			(position_set_y, pos1, ":pos_y_rank"),
			(assign, reg0, ":rank"),
			(create_text_overlay, reg1, "@{reg0}", tf_center_justify|tf_vertical_align_center),
			(overlay_set_position, reg1, pos1),
			(overlay_set_color, reg1, wp_red),
			(troop_set_slot, "trp_tpe_presobj", ":slot_rank", reg1),
		(try_end),
		
		# Portrait Display
		(call_script, "script_tpe_get_faction_image", ":troop_no"), # returns reg1 as a troop_id
		(create_mesh_overlay_with_tableau_material, ":portrait_obj", -1, "tableau_troop_note_mesh", reg1),
		(position_set_x, pos2, ":pos_x_image"),
		(position_set_y, pos2, ":pos_y_bottom"),
		(overlay_set_position, ":portrait_obj", pos2),
		(position_set_x, pos2, ":portrait_size"),
		(position_set_y, pos2, ":portrait_size"),
		(overlay_set_size, ":portrait_obj", pos2),
		(troop_set_slot, "trp_tpe_presobj", ":slot_image", ":portrait_obj"),

		# Name Display
		(position_set_x, pos1, ":pos_x_name"),
		(position_set_y, pos1, ":pos_y_text1"),
		(str_store_troop_name, s1, ":troop_no"),
		(try_begin),
			(is_between, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end),
			(str_store_troop_name_plural, s1, ":troop_no"),
		(try_end),
		(create_text_overlay, reg1, "@{s1}", tf_left_align|tf_vertical_align_center),
		(overlay_set_position, reg1, pos1),
		(overlay_set_color, reg1, 0xFFAAAAFF), # Blue
		(troop_set_slot, "trp_tpe_presobj", ":slot_name", reg1),
		
		# Faction / Title Display
		(position_set_x, pos1, ":pos_x_name"),
		(position_set_y, pos1, ":pos_y_text2"),
		(try_begin),
			####### POST-COMBAT RANK DISPLAY #######
			(eq, ":type", wp_tpe_icd_round_rank),  # Display post fight.
			(store_faction_of_troop, ":faction_no", ":troop_no"),
			(str_store_faction_name, s1, ":faction_no"),
			(try_begin),
				(this_or_next|eq, ":troop_no", "trp_player"),
				(is_between, ":troop_no", companions_begin, companions_end),
				(assign, ":player_faction", "$players_kingdom"),
				(str_store_faction_name, s1, ":player_faction"),
				(eq, ":player_faction", "fac_kingdom_2"), # Grand Principality of the Vaegirs (too long)
				(str_store_string, s1, "@Grand Principality"),
			(else_try),
				(is_between, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end),
				(troop_get_slot, ":faction_no", ":troop_no", slot_troop_original_faction),
				(str_store_faction_name, s1, ":faction_no"),
				(eq, ":faction_no", "fac_kingdom_2"),
				(str_store_string, s1, "@Grand Principality"),
			(try_end),
			(try_begin),
				(eq, ":faction_no", "fac_kingdom_2"),
				(str_store_string, s1, "@Grand Principality"),
			(try_end),
		(else_try),
			######## IN-COMBAT RANK DISPLAY #######
			(eq, ":type", wp_tpe_icd_rank),  # In Combat Rank Display
			(call_script, "script_tpe_color_team_name", ":team"),
			(assign, ":color", reg1),
		
		(try_end),
		
		(create_text_overlay, reg1, "@{s1}", tf_left_align|tf_vertical_align_center),
		(overlay_set_position, reg1, pos1),
		(try_begin),
			(eq, ":type", wp_tpe_icd_rank),  # In Combat Rank Display
			(overlay_set_color, reg1, ":color"),
		(try_end),
		(troop_set_slot, "trp_tpe_presobj", ":slot_title", reg1),
		
		# Points Display
		(position_set_x, pos1, ":pos_x_pts"),
		(position_set_y, pos1, ":pos_y_rank"),
		(assign, reg0, ":points"),
		(create_text_overlay, reg1, "@{reg0}", tf_center_justify|tf_vertical_align_center),
		(overlay_set_position, reg1, pos1),
		(overlay_set_color, reg1, wp_white),
		(troop_set_slot, "trp_tpe_presobj", ":slot_points", reg1),
	]),

# script_tpe_update_ranking_box
# Supports "Ranking Display" by updating the box with the rank, troop name, his picture, faction and points.
# Input: type, troop, points, rank, (pos x, pos y) for where to set the bottom left corner.
# Output: none
	("tpe_update_ranking_box",
	  [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":points",   2),
		(store_script_param, ":rank",     3),
		(store_script_param, ":team",     4),
		
		(store_add, ":rank_slot", 30, ":rank"), # Rank 1 state begins at 31, rank 2 at 32, etc.
		(try_begin),
			(troop_slot_eq, "trp_tpe_presobj", ":rank_slot", 0), # Box hasn't been created yet.
			(call_script, "script_tpe_create_ranking_box", ":troop_no", ":points", ":rank", ":team"), # This creates a box to begin with.
			(troop_set_slot, "trp_tpe_presobj", ":rank_slot", 1), # Now it shouldn't try to create it again and will simply update.
		(try_end),
		
		(try_begin),
			(ge, DEBUG_TPE_general, 2),
			(str_store_troop_name, s1, ":troop_no"),
			(assign, reg1, ":points"),
			(display_message, "@DEBUG (TPE): Ranking box update attempt: {s1} with {reg1} points."),
		(try_end),
		
		# Define presentation object slots.  These are used with trp_tpe_presobj
		(store_mul, ":slot_base", ":rank", 10),
		(val_add, ":slot_base", 90),              # This should make rank 1 box go to slot 100, rank 2 box start at 110, etc.
		(store_add, ":slot_rank", ":slot_base",   1), # Slot **1
		#(store_add, ":slot_image", ":slot_base",  2), # Slot **2
		(store_add, ":slot_name", ":slot_base",   3), # Slot **3
		(store_add, ":slot_title", ":slot_base",  4), # Slot **4
		(store_add, ":slot_points", ":slot_base", 5), # Slot **5
		# (store_add, ":slot_pos_x", ":slot_base",  6), # Slot **6
		# (store_add, ":slot_pos_y", ":slot_base",  7), # Slot **7
		(store_add, ":slot_type", ":slot_base",   8), # Slot **8
		
		(troop_get_slot, ":type", "trp_tpe_presobj", ":slot_type"),
		
		(try_begin),
			(neg|is_presentation_active, "prsnt_tpe_team_display"),
			(eq, ":type", wp_tpe_icd_rank),
			(start_presentation, "prsnt_tpe_team_display"),
		(try_end),
		
		(try_begin),
			(eq, ":type", wp_tpe_icd_rank),
			# Rank Display
			(troop_get_slot, reg1, "trp_tpe_presobj", ":slot_rank"),
			(assign, reg2, ":rank"),
			(overlay_set_text, reg1, "@{reg2}"),
		(try_end),

		# Name Display
		(troop_get_slot, reg1, "trp_tpe_presobj", ":slot_name"),
		(str_store_troop_name, s1, ":troop_no"),
		(try_begin),
			(is_between, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end),
			(str_store_troop_name_plural, s1, ":troop_no"),
		(try_end),
		(overlay_set_text, reg1, "@{s1}"),	
		
		# Faction / Title Display
		(troop_get_slot, ":title", "trp_tpe_presobj", ":slot_title"),
		(try_begin),
			####### POST-COMBAT RANK DISPLAY #######
			(eq, ":type", wp_tpe_icd_round_rank),
			(store_faction_of_troop, ":faction_no", ":troop_no"),
			(str_store_faction_name, s1, ":faction_no"),
			(try_begin),
				(is_between, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end),
				(troop_get_slot, ":faction_no", ":troop_no", slot_troop_original_faction),
				(str_store_faction_name, s1, ":faction_no"),
				(eq, ":faction_no", "fac_kingdom_2"),
				(str_store_string, s1, "@Grand Principality"),
			(try_end),
			(try_begin),
				(eq, ":faction_no", "fac_kingdom_2"),
				(str_store_string, s1, "@Grand Principality"),
			(try_end),
			(overlay_set_text, ":title", "@{s1}"),
			
		(else_try),
			####### IN-COMBAT RANK DISPLAY #######
			(eq, ":type", wp_tpe_icd_rank),  # In Combat Rank Display
			(call_script, "script_tpe_color_team_name", ":team"),
			(overlay_set_color, ":title", reg1), # Commented out because it was causing another part of the background display to disappear.
			(overlay_set_text, ":title", "@{s1}"),	
		(try_end),
		
		# Points Display
		(troop_get_slot, reg1, "trp_tpe_presobj", ":slot_points"),
		(assign, reg2, ":points"),
		(overlay_set_text, reg1, "@{reg2}"),	
		
	]),

# script_tpe_icd_ranking
# Figures out who the top three ranked troops are and generates a display for them.
# Input: target array, source array, limit (last cell to copy)
# Output: none
  ("tpe_icd_ranking",
    [
		# Ensure in-combat Display is active
		(try_begin),
			(neg|is_presentation_active, "prsnt_tpe_team_display"),
			(start_presentation, "prsnt_tpe_team_display"),
		(try_end),
		
		# Copy our current round's troop_ids and points into temporary arrays.
		(assign, ":tally", 0),
		(try_for_agents, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(troop_set_slot, tpe_ranking_array, ":tally", ":troop_no"),
			(val_add, ":tally", 1),
		(try_end),
		
		# Sort the listed arrays.
		(call_script, "script_tpe_sort_troops_and_points", slot_troop_tournament_round_points),
		
		# Update the ranking fields.
		(assign, ":offset", -1),
		(try_for_range, ":rank", 0, 5),
			(lt, ":rank", "$g_tournament_num_participants_for_fight"), # This is to prevent matches with only 2 people throwing up errors.
			(troop_get_slot, ":troop_no", tpe_ranking_array, ":rank"),
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(val_add, ":offset", 1),
				(ge, DEBUG_TPE_general, 1),
				(assign, reg21, ":offset"),
				(display_message, "@DEBUG (TPE): Garbage troop_id detected.  ICD now offset by {reg21}."),
			(try_end),
			(try_begin), # Bugfix attempt to skip garbage troops.
				(ge, ":offset", 0),
				(store_add, ":rank_offset", ":rank", ":offset"),
			(else_try),
				(assign, ":rank_offset", ":rank"),
			(try_end),
			(troop_get_slot, ":troop_no", tpe_ranking_array, ":rank_offset"),
			
			# Figure out what agent belongs to this troop_no
			(try_for_agents, ":agent_no"),
				(agent_is_human, ":agent_no"),
				(agent_get_troop_id, ":troop_check", ":agent_no"),
				(eq, ":troop_check", ":troop_no"),
				(agent_get_team, ":team_agent", ":agent_no"),
			(try_end),
			
			# Update points information
			(store_add, ":slot", tpe_icd_rank_1_points, ":rank"),
			(troop_get_slot, ":obj_points", "trp_tpe_presobj", ":slot"),
			(troop_get_slot, reg1, ":troop_no", slot_troop_tournament_round_points),
			(ge, reg1, 1), # Gating line to prevent people listed with 0 points.
			(overlay_set_text, ":obj_points", "@{reg1}"),
			(call_script, "script_tpe_color_team_name", ":team_agent"),
			(overlay_set_color, ":obj_points", reg1),
			
			# Update troop name
			(store_add, ":slot", tpe_icd_rank_1_troop, ":rank"),
			(troop_get_slot, ":obj_troop", "trp_tpe_presobj", ":slot"),
			(str_store_troop_name, s21, ":troop_no"),
			(try_begin),
				(is_between, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end),
				(str_store_troop_name_plural, s21, ":troop_no"),
			(try_end),
			(overlay_set_text, ":obj_troop", "@{s21}"),
			(call_script, "script_tpe_color_team_name", ":team_agent"),
			(overlay_set_color, ":obj_troop", reg1),
			
			# Update team information
			(store_add, ":slot", tpe_icd_rank_1_team, ":rank"),
			(troop_get_slot, ":obj_team", "trp_tpe_presobj", ":slot"),
			(call_script, "script_tpe_color_team_name", ":team_agent"),
			(overlay_set_text, ":obj_team", "@{s1}"),
			(overlay_set_color, ":obj_team", reg1),
		(try_end),
	]),

# script_tpe_draw_line (originally prsnt_line by Rubik)
# Not originally part of TPE, but copied and modified from Custom Commander since it is used.
# Inputs: horizontal size, vertical size, ( pos x, pos y), color code
	("tpe_draw_line",
	  [
		(store_script_param, ":size_x", 1),
		(store_script_param, ":size_y", 2),
		(store_script_param, ":pos_x", 3),
		(store_script_param, ":pos_y", 4),
		(store_script_param, ":color", 5),
		
		(create_mesh_overlay, reg1, "mesh_white_plane"),
		(val_mul, ":size_x", 50),
		(val_mul, ":size_y", 50),
		(position_set_x, pos1, ":size_x"),
		(position_set_y, pos1, ":size_y"),
		(overlay_set_size, reg1, pos1),
		(position_set_x, pos1, ":pos_x"),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
		(overlay_set_color, reg1, ":color"),
	]),
	
# script_tpe_color_team_name
# Copies source array into target array.
# Input: team
# Output: reg1 (color code)
  ("tpe_color_team_name",
    [
		(store_script_param, ":team", 1),
		
		(try_begin),
			(eq, ":team", 0),
			(assign, ":color", wp_red), # RED
			(str_store_string, s1, "@Red Team"),
		(else_try),
			(eq, ":team", 1),
			(assign, ":color", wp_blue), # BLUE
			(str_store_string, s1, "@Blue Team"),
		(else_try),
			(eq, ":team", 2),
			(assign, ":color", wp_green), # GREEN
			(str_store_string, s1, "@Green Team"),
		(else_try),
			(eq, ":team", 3),
			(assign, ":color", wp_yellow), # YELLOW
			(str_store_string, s1, "@Yellow Team"),
		(else_try),
			(str_store_string, s1, "@Random"),
			(assign, ":color", 0xDDDDDD),
		(try_end),
		(assign, reg1, ":color"),
	]),
# END - IN-COMBAT DISPLAY SCRIPTS

###########################################################################################################################
#####                                                  LEVEL SCALING                                                  #####
###########################################################################################################################

# script_tpe_initialize_xp_table
# Populates the xp required to level table..
# Input: none
# Output: none
  ("tpe_initialize_xp_table",
    [
		(troop_set_slot, tpe_xp_table,  0, 0),
		(troop_set_slot, tpe_xp_table,  1, 600),
		(troop_set_slot, tpe_xp_table,  2, 1360),
		(troop_set_slot, tpe_xp_table,  3, 2296),
		(troop_set_slot, tpe_xp_table,  4, 3426),
		(troop_set_slot, tpe_xp_table,  5, 4768),
		(troop_set_slot, tpe_xp_table,  6, 6345),
		(troop_set_slot, tpe_xp_table,  7, 8179),
		(troop_set_slot, tpe_xp_table,  8, 10297),
		(troop_set_slot, tpe_xp_table,  9, 13010),
		(troop_set_slot, tpe_xp_table, 10, 16161),
		(troop_set_slot, tpe_xp_table, 11, 19806),
		(troop_set_slot, tpe_xp_table, 12, 24007),
		(troop_set_slot, tpe_xp_table, 13, 28832),
		(troop_set_slot, tpe_xp_table, 14, 34362),
		(troop_set_slot, tpe_xp_table, 15, 40682),
		(troop_set_slot, tpe_xp_table, 16, 47892),
		(troop_set_slot, tpe_xp_table, 17, 56103),
		(troop_set_slot, tpe_xp_table, 18, 65441),
		(troop_set_slot, tpe_xp_table, 19, 77233),
		(troop_set_slot, tpe_xp_table, 20, 90809),
		(troop_set_slot, tpe_xp_table, 21, 106425),
		(troop_set_slot, tpe_xp_table, 22, 124371),
		(troop_set_slot, tpe_xp_table, 23, 144981),
		(troop_set_slot, tpe_xp_table, 24, 168636),
		(troop_set_slot, tpe_xp_table, 25, 195769),
		(troop_set_slot, tpe_xp_table, 26, 226879),
		(troop_set_slot, tpe_xp_table, 27, 262533),
		(troop_set_slot, tpe_xp_table, 28, 303381),
		(troop_set_slot, tpe_xp_table, 29, 350164),
		(troop_set_slot, tpe_xp_table, 30, 412091),
		(troop_set_slot, tpe_xp_table, 31, 484440),
		(troop_set_slot, tpe_xp_table, 32, 568947),
		(troop_set_slot, tpe_xp_table, 33, 667638),
		(troop_set_slot, tpe_xp_table, 34, 782877),
		(troop_set_slot, tpe_xp_table, 35, 917424),
		(troop_set_slot, tpe_xp_table, 36, 1074494),
		(troop_set_slot, tpe_xp_table, 37, 1257843),
		(troop_set_slot, tpe_xp_table, 38, 1471851),
		(troop_set_slot, tpe_xp_table, 39, 1721626),
		(troop_set_slot, tpe_xp_table, 40, 2070551),
		(troop_set_slot, tpe_xp_table, 41, 2489361),
		(troop_set_slot, tpe_xp_table, 42, 2992033),
		(troop_set_slot, tpe_xp_table, 43, 3595340),
		(troop_set_slot, tpe_xp_table, 44, 4319408),
		(troop_set_slot, tpe_xp_table, 45, 5188389),
		(troop_set_slot, tpe_xp_table, 46, 6231267),
		(troop_set_slot, tpe_xp_table, 47, 7482821),
		(troop_set_slot, tpe_xp_table, 48, 8984785),
		(troop_set_slot, tpe_xp_table, 49, 11236531),
		(troop_set_slot, tpe_xp_table, 50, 14051314),
		(troop_set_slot, tpe_xp_table, 51, 17569892),
		(troop_set_slot, tpe_xp_table, 52, 21968215),
		(troop_set_slot, tpe_xp_table, 53, 27466219),
		(troop_set_slot, tpe_xp_table, 54, 34338823),
		(troop_set_slot, tpe_xp_table, 55, 42929679),
		(troop_set_slot, tpe_xp_table, 56, 53668349),
		(troop_set_slot, tpe_xp_table, 57, 67091786),
		(troop_set_slot, tpe_xp_table, 58, 83871183),
		(troop_set_slot, tpe_xp_table, 59, 160204600),
		(troop_set_slot, tpe_xp_table, 60, 320304600),
		(troop_set_slot, tpe_xp_table, 61, 644046000),
		(troop_set_slot, tpe_xp_table, 62, 2050460000),
	]),
	
# script_tpe_level_scale_troop
# Populates the xp required to level table..
# Input: troop_id
# Output: none
  ("tpe_level_scale_troop",
    [
		(store_script_param, ":troop_no", 1),
		
		##### DETERMINE SCALED LEVEL #####
		# Instead of changing the actual level of the troop, lets try changing only the "effective level" since stats, skills & proficiency don't care.
		(try_begin),
			(assign, ":extra_levels", 0),
			(is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_veterans_end),
			(val_add, ":extra_levels", wp_tpe_level_bonus_for_title),
			(is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_champions_end),
			(val_add, ":extra_levels", wp_tpe_level_bonus_for_traveler),
			## ELIMINATION MODE ##
			# Since elimination is more difficult by inherent design the troops will be a little weaker.
			(eq, "$tpe_tournament_mode", tpe_mode_elimination),
			(val_sub, ":extra_levels", 2),
		(try_end),
		
		## INITIAL CREATION ##
		(store_character_level, ":base_level", "trp_player"),
		(store_add, ":scaled_level", wp_tpe_scaling_disabled_default_level, ":extra_levels"),
		(try_begin),
			# If level scaling is enabled then add the player's level to the scaled level.
			(troop_slot_eq, TPE_OPTIONS, tpe_val_level_scale, 1),
			(val_add, ":scaled_level", ":base_level"),
		(else_try),
			(assign, ":base_level", 0),
		(try_end),
		(troop_set_slot, ":troop_no", slot_troop_tournament_scaled_level, ":scaled_level"),
		
		##### DETERMINE ATTRIBUTES #####
		# Strength
		(store_mul, ":stat_target", ":scaled_level", wp_tpe_attribute_per_level_numerator),
		(val_div, ":stat_target", wp_tpe_attribute_per_level_denominator),
		(val_min, ":stat_target", wp_tpe_attribute_threshold),
		(troop_set_attribute, ":troop_no", ca_strength, ":stat_target"),
		(assign, ":str_diagnostic_target", ":stat_target"),
		
		# Agility
		(store_mul, ":stat_target", ":scaled_level", wp_tpe_attribute_per_level_numerator),
		(val_div, ":stat_target", wp_tpe_attribute_per_level_denominator),
		(val_min, ":stat_target", wp_tpe_attribute_threshold),
		(troop_set_attribute, ":troop_no", ca_agility, ":stat_target"),
		
		##### DETERMINE SKILL LEVELS #####
		# What are the hard skill limits?
		(store_attribute_level, ":str", ":troop_no", ca_strength),
		(store_div, ":str_max", ":str", 3),
		(store_mul, ":str_limit", ":str_max", wp_tpe_skill_per_3_levels_numerator),
		(val_div, ":str_limit", wp_tpe_skill_per_3_levels_denominator),
		(val_min, ":str_limit", wp_tpe_skill_threshold),
		(val_max, ":str_limit", wp_tpe_skill_minimum),
		
		(store_attribute_level, ":agi", ":troop_no", ca_agility),
		(store_div, ":agi_max", ":agi", 3),
		(store_mul, ":agi_limit", ":agi_max", wp_tpe_skill_per_3_levels_numerator),
		(val_div, ":agi_limit", wp_tpe_skill_per_3_levels_denominator),
		(val_min, ":agi_limit", wp_tpe_skill_threshold),
		(val_max, ":agi_limit", wp_tpe_skill_minimum),
		
		# Power Strike
		(troop_set_skill, ":troop_no", "skl_power_strike", ":str_limit"),
		# Power Throw
		(troop_set_skill, ":troop_no", "skl_power_throw", ":str_limit"),
		# Power Draw
		(troop_set_skill, ":troop_no", "skl_power_draw", ":str_limit"),
		# Ironflesh
		(troop_set_skill, ":troop_no", "skl_ironflesh", ":str_limit"),
		# Shield
		(troop_set_skill, ":troop_no", "skl_shield", ":agi_limit"),
		# Athletics
		(troop_set_skill, ":troop_no", "skl_athletics", ":agi_limit"),
		# Horse Archery
		(troop_set_skill, ":troop_no", "skl_horse_archery", ":agi_limit"),
		# Riding
		(troop_set_skill, ":troop_no", "skl_riding", ":agi_limit"),
		
		(try_begin),
			(assign, ":prof_boost", 0),
			(troop_get_slot, ":difficulty", TPE_OPTIONS, tpe_val_diff_setting),
			(ge, ":difficulty", 17),
			(assign, ":prof_boost", wp_tpe_hard_proficiency_bonus),
		(else_try),
			(ge, ":difficulty", 9),
			(assign, ":prof_boost", wp_tpe_medium_proficiency_bonus),
		(else_try),
			(assign, ":prof_boost", wp_tpe_easy_proficiency_bonus),
		(try_end),
		
		##### DETERMINE PROFICIENCY LEVELS #####
		# Determine proficiency target level.
		(store_mul, ":prof_target", ":scaled_level", wp_tpe_proficiency_gain_per_level),
		(val_add, ":prof_target", ":prof_boost"),
		(val_min, ":prof_target", wp_tpe_proficiency_threshold),
		(val_max, ":prof_target", wp_tpe_proficiency_minimum),
		# Set proficiency for all weapon types.
		(troop_set_proficiency, ":troop_no", wpt_one_handed_weapon, ":prof_target"),
		(troop_set_proficiency, ":troop_no", wpt_two_handed_weapon, ":prof_target"),
		(troop_set_proficiency, ":troop_no", wpt_polearm,           ":prof_target"),
		(troop_set_proficiency, ":troop_no", wpt_archery,           ":prof_target"),
		(troop_set_proficiency, ":troop_no", wpt_crossbow,          ":prof_target"),
		(troop_set_proficiency, ":troop_no", wpt_throwing,          ":prof_target"),
		
		(try_begin),
			(ge, DEBUG_TPE_general, 1),
			(this_or_next|eq, ":troop_no", tpe_scaled_champions_begin),
			(this_or_next|eq, ":troop_no", tpe_scaled_veterans_begin),
			(eq, ":troop_no", tpe_scaled_normals_begin),
			(try_begin),
				(eq, ":troop_no", tpe_scaled_champions_begin),
				(str_store_string, s31, "@Champion Troop +12"),
			(else_try),
				(eq, ":troop_no", tpe_scaled_veterans_begin),
				(str_store_string, s31, "@Veteran Troop +6"),
			(else_try),
				(eq, ":troop_no", tpe_scaled_normals_begin),
				(str_store_string, s31, "@Normal Troop +0"),
			(else_try),
				(str_store_string, s31, "@ERROR!"),
			(try_end),
			#(str_store_troop_name, s31, ":troop_no"),     # Target troop.
			(assign, reg31, ":base_level"),
			(store_add, reg32, wp_tpe_scaling_disabled_default_level, ":extra_levels"),
			(assign, reg33, ":scaled_level"),
			(assign, reg34, ":str_diagnostic_target"),    # New STR value.
			(assign, reg35, ":stat_target"),              # New AGI value.
			(assign, reg36, ":str_limit"),                # Max skill level
			(assign, reg37, ":prof_target"),              # Desired weapon proficiency level.
			(display_message, "@DEBUG (TPE): [ {s31} ] - Level ({reg31}+{reg32}) = {reg33}"),
			(display_message, "@---------------> STR = {reg34}, AGI = {reg35}"),
			(display_message, "@---------------> Skill Limit {reg36}, Wpt Prof {reg37}"),
		(try_end),
	]),
	
# script_tpe_name_the_scaled_troops
# Figures out what to call the troop based on where the tournament is held.
# Input: none
# Output: none
  ("tpe_name_the_scaled_troops",
    [
		(store_script_param, ":troop_no", 1),
		
		(troop_set_slot, ":troop_no", slot_troop_original_faction, "fac_commoners"),
		(assign, ":age", 18),
		
		# Dynamically create a name using the Quest Utilities script.
		(troop_get_type, ":is_female", ":troop_no"),
		(try_begin),
			(is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_champions_end),
			(assign, ":home_found", 0),
			(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
				(eq, ":home_found", 0),
				(neq, ":center_no", "$current_town"), # I don't want titles listed if you're local.
				(store_distance_to_party_from_party, ":distance", ":center_no", "$current_town"),
				(lt, ":distance", wp_tpe_max_distance_traveling_people),  # This sets how far away a traveler would likely come from.
				(store_random_in_range, ":chance", 0, 100),
				(lt, ":chance", 25),
				(assign, ":home_found", ":center_no"),
			(try_end),
			(neq, ":home_found", 0),
			(store_faction_of_party, ":faction_no", ":home_found"),
			(call_script, "script_common_store_temp_name_to_s1", ":is_female", ":faction_no", SCRT_FIRST), # Quest Utility script.
		(else_try),
			(store_faction_of_party, ":faction_no", "$current_town"),
			(call_script, "script_common_store_temp_name_to_s1", ":is_female", ":faction_no", SCRT_FIRST), # Quest Utility script.
		(try_end),
		
		# (store_random_in_range, ":name_seed", wp_tpe_male_names_begin, wp_tpe_male_names_end),
		# (str_store_string, s1, ":name_seed"),
		
		# Determine if we want a title added.
		(try_begin),
			(is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_veterans_end),
			(store_random_in_range, ":title_seed", wp_tpe_titles_begin, wp_tpe_titles_end),
			(str_store_string, s2, ":title_seed"),
			(str_store_string, s1, "@{s2} {s1}"), # Example: Sir Gerald, Captain Marcus
			(call_script, "script_tpe_store_town_faction_to_reg0", "$current_town"),
			(troop_set_slot, ":troop_no", slot_troop_original_faction, reg0),
			(val_add, ":age", 12),
		(try_end),
		
		# Store a plural name as our "short name"
		(troop_set_plural_name, ":troop_no", s1),
		
		# Find some towns for traveling participants (actual home determined earlier in script)
		(try_begin),
			(is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_champions_end),
			(is_between, ":home_found", walled_centers_begin, walled_centers_end),
			(val_add, ":age", 5),
			(str_store_party_name, s2, ":home_found"),
			(str_store_string, s1, "@{s1} of {s2}"),
			(call_script, "script_tpe_store_town_faction_to_reg0", ":home_found"),
			(troop_set_slot, ":troop_no", slot_troop_original_faction, reg0),
		(try_end),
		
		##### GENERATE SOME AGE & RENOWN #####
		# Give them a random age.
		(store_random_in_range, ":random_years", 0, 6),
		(val_add, ":age", ":random_years"),
		(troop_set_slot, ":troop_no", slot_troop_age, ":age"),
		# Renown is largely factored by experience represented by age.
		(assign, ":renown_base", 50),
		(val_sub, ":age", 18),
		(val_mul, ":age", 15),
		(store_add, ":renown", ":renown_base", ":age"),
		(troop_set_slot, ":troop_no", slot_troop_renown, ":renown"),
		(troop_set_name, ":troop_no", "@{s1}"),
	]),
	
# script_tpe_setup_neighboring_regions
# Populates the xp required to level table..
# Input: none
# Output: none
  ("tpe_setup_neighboring_regions",
    [
		(troop_set_slot, tpe_xp_table, 101, wp_tpe_kingdom_1_neighbor_1),
		(troop_set_slot, tpe_xp_table, 102, wp_tpe_kingdom_1_neighbor_2),
		(troop_set_slot, tpe_xp_table, 103, wp_tpe_kingdom_1_neighbor_3),
		(troop_set_slot, tpe_xp_table, 104, wp_tpe_kingdom_1_neighbor_4),
		(troop_set_slot, tpe_xp_table, 105, wp_tpe_kingdom_2_neighbor_1),
		(troop_set_slot, tpe_xp_table, 106, wp_tpe_kingdom_2_neighbor_2),
		(troop_set_slot, tpe_xp_table, 107, wp_tpe_kingdom_2_neighbor_3),
		(troop_set_slot, tpe_xp_table, 108, wp_tpe_kingdom_2_neighbor_4),
		(troop_set_slot, tpe_xp_table, 109, wp_tpe_kingdom_3_neighbor_1),
		(troop_set_slot, tpe_xp_table, 110, wp_tpe_kingdom_3_neighbor_2),
		(troop_set_slot, tpe_xp_table, 111, wp_tpe_kingdom_3_neighbor_3),
		(troop_set_slot, tpe_xp_table, 112, wp_tpe_kingdom_3_neighbor_4),
		(troop_set_slot, tpe_xp_table, 113, wp_tpe_kingdom_4_neighbor_1),
		(troop_set_slot, tpe_xp_table, 114, wp_tpe_kingdom_4_neighbor_2),
		(troop_set_slot, tpe_xp_table, 115, wp_tpe_kingdom_4_neighbor_3),
		(troop_set_slot, tpe_xp_table, 116, wp_tpe_kingdom_4_neighbor_4),
		(troop_set_slot, tpe_xp_table, 117, wp_tpe_kingdom_5_neighbor_1),
		(troop_set_slot, tpe_xp_table, 118, wp_tpe_kingdom_5_neighbor_2),
		(troop_set_slot, tpe_xp_table, 119, wp_tpe_kingdom_5_neighbor_3),
		(troop_set_slot, tpe_xp_table, 120, wp_tpe_kingdom_5_neighbor_4),
		(troop_set_slot, tpe_xp_table, 121, wp_tpe_kingdom_6_neighbor_1),
		(troop_set_slot, tpe_xp_table, 122, wp_tpe_kingdom_6_neighbor_2),
		(troop_set_slot, tpe_xp_table, 123, wp_tpe_kingdom_6_neighbor_3),
		(troop_set_slot, tpe_xp_table, 124, wp_tpe_kingdom_6_neighbor_4),
	]),
# END - LEVEL SCALING SCRIPTS

###########################################################################################################################
#####                                                  AWARD SCRIPTS                                                  #####
###########################################################################################################################

# script_tpe_award_scaled_xp
# Receives a base xp award and level scales it.
# Input: troop_id, xp_base
# Output: scaled_xp
  ("tpe_award_scaled_xp",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":xp_base", 2),
		
		# Determine scaling factor.
		(store_character_level, ":level", ":troop_no"),
		(store_mul, ":xp_factor", ":level", tpe_award_scaled_xp_factor),
		(val_add, ":xp_factor", 100),
		
		# Determine scaled xp.
		(store_mul, ":xp_scaled", ":xp_base", ":xp_factor"),
		(val_div, ":xp_scaled", 100),
		
		# Award xp and return value for display.
		(add_xp_to_troop, ":xp_scaled", ":troop_no"),
		(assign, reg1, ":xp_scaled"),
	]),
	
# script_tpe_award_point_to_troop
# Adds points agents earn in a round to their cumulative tournament points.
# Input: none
# Output: none
  ("tpe_award_point_to_troop",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":new_points", 2),
		(store_script_param, ":reason", 3),
		(store_script_param, ":color", 4),
		
		(troop_get_slot, ":round_points", ":troop_no", slot_troop_tournament_round_points),
		(val_add, ":round_points", ":new_points"),
		(troop_set_slot, ":troop_no", slot_troop_tournament_round_points, ":round_points"),
		(try_begin),
			(assign, reg1, ":new_points"),
			(assign, reg2, ":round_points"),
			(str_store_troop_name, s1, ":troop_no"),
			(try_begin),
				(ge, ":new_points", 2),
				(str_store_string, s2, "@points"),
			(else_try),
				(str_store_string, s2, "@point"),
			(try_end),
			(try_begin),
				(eq, ":reason", tpe_point_eliminated_opponent),           (str_store_string, s3, "str_tpe_award_point_eliminate_opponent"),
				(else_try), (eq, ":reason", tpe_point_won_the_round),     (str_store_string, s3, "str_tpe_award_point_winning_team"),
				(else_try), (eq, ":reason", tpe_point_best_scoring_team), (str_store_string, s3, "str_tpe_award_point_highest_scoring_team"),
				(else_try), (str_store_string, s3, "@because I said so"), # This should hopefully never appear.
			(try_end),
			(troop_slot_eq, TPE_OPTIONS, tpe_val_opt_points, 1), # Player option to enable or disable these messages in combat.
			(display_message, "@The Tournament Master announces, '{s1} has been awarded {reg1} {s2} for {s3}.'", ":color"),
			(str_store_string, s35, "@{s35}{s1} has been awarded {reg1} {s2} for {s3}. (Total = {reg2})^"),
		(try_end),
	]),
	
# script_tpe_update_kill_count
# Totals kills per round by everyone and checks for possible awards.
# Input: none
# Output: none
  ("tpe_update_kill_count",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":num_killed", 2),
		
		#(call_script, "script_play_victorious_sound"),
				
		(try_begin),
			(eq, ":troop_no", "trp_player"),
			(assign, ":color", wp_green),
		(else_try),
			(assign, ":color", wp_white),
		(try_end),
		
		(troop_get_slot, ":total_killed", tpe_award_data, tpe_kill_count),
		(try_begin), # AWARD: Swiftest Cut (First kill)
			(lt, ":total_killed", 1),
			(troop_set_slot, tpe_award_data, tpe_first_blood, ":troop_no"),
			(str_store_troop_name, s31, ":troop_no"),
			(troop_slot_eq, TPE_OPTIONS, tpe_val_opt_awards, 1), # Player option to enable/disable award displays.
			(display_message, "@AWARD GRANTED: {s31} has earned the SWIFTEST CUT award!", ":color"),
		(try_end),
		(val_add, ":total_killed", ":num_killed"),
		(troop_set_slot, tpe_award_data, tpe_kill_count, ":total_killed"),
		
		#### AWARD - FIERCEST COMPETITOR ####
		# This is based on the troop gaining the highest number of kills.  Minimum 6 participants.
		(try_begin),
			(assign, ":new_holder", 0),
			(troop_get_slot, ":most_kills", tpe_award_data, tpe_data_most_kills),
			(troop_get_slot, ":personal_kills", ":troop_no", slot_troop_tournament_round_points),
			(gt, ":personal_kills", ":most_kills"),
			(ge, "$g_tournament_num_participants_for_fight", tpe_most_kills_min_participants),
			(try_begin),
				(neg|troop_slot_eq, tpe_award_data, tpe_most_kills, ":troop_no"),
				(assign, ":new_holder", 1),
			(try_end),
			(troop_set_slot, tpe_award_data, tpe_most_kills, ":troop_no"),
			(troop_set_slot, tpe_award_data, tpe_data_most_kills, ":personal_kills"),
			(assign, reg1, ":personal_kills"),
			(str_store_troop_name, s31, ":troop_no"),
			(eq, ":new_holder", 1), # So we don't display this award earned on every subsequent kill.
			(troop_slot_eq, TPE_OPTIONS, tpe_val_opt_awards, 1), # Player option to enable/disable award displays.
			(display_message, "@AWARD GRANTED: {s31} has earned the FIERCEST COMPETITOR award with {reg1} kills!", ":color"),
		(try_end),
		
		#### AWARD - DOMINANT & LEGENDARY PRESENCE ####
		# This is based on the troop gaining over 25/50% of the total kills.
		(try_begin),
			(str_store_troop_name, s31, ":troop_no"),
			(troop_get_slot, ":personal_kills", ":troop_no", slot_troop_tournament_round_points),
			(try_begin), ### MYTHICAL PRESENCE 100% ### - Credit: -AoG- X3N0PH083
				(troop_get_slot, ":personal_kills", ":troop_no", slot_troop_tournament_round_points),
				(store_sub, ":quarter_cutoff", "$g_tournament_num_participants_for_fight", 1),
				(ge, "$g_tournament_num_participants_for_fight", tpe_legendary_min_participants),
				(ge, ":personal_kills", ":quarter_cutoff"),
				(troop_set_slot, tpe_award_data, tpe_mythical_warrior, ":troop_no"),
				(troop_slot_eq, TPE_OPTIONS, tpe_val_opt_awards, 1), # Player option to enable/disable award displays.
				(display_message, "@AWARD GRANTED: {s31} has upgraded to the MYTHICAL PRESENCE award.", ":color"),
				
			(else_try), ### LEGENDARY PRESENCE 50% ###
				(troop_get_slot, ":personal_kills", ":troop_no", slot_troop_tournament_round_points),
				(store_div, ":quarter_cutoff", "$g_tournament_num_participants_for_fight", 2),
				(ge, "$g_tournament_num_participants_for_fight", tpe_legendary_min_participants),
				(ge, ":personal_kills", ":quarter_cutoff"),
				(try_begin),
					(troop_slot_eq, TPE_OPTIONS, tpe_val_opt_awards, 1), # Player option to enable/disable award displays.
					(neg|troop_slot_eq, tpe_award_data, tpe_legendary_warrior_1, ":troop_no"),
					(neg|troop_slot_eq, tpe_award_data, tpe_legendary_warrior_2, ":troop_no"),
					(display_message, "@AWARD GRANTED: {s31} has upgraded to the LEGENDARY PRESENCE award.", ":color"),
				(try_end),
				(try_begin),
					(troop_slot_eq, tpe_award_data, tpe_legendary_warrior_1, -1),
					(neg|troop_slot_eq, tpe_award_data, tpe_legendary_warrior_2, ":troop_no"),
					(troop_set_slot, tpe_award_data, tpe_legendary_warrior_1, ":troop_no"),
				(else_try),
					(troop_slot_eq, tpe_award_data, tpe_legendary_warrior_2, -1),
					(neg|troop_slot_eq, tpe_award_data, tpe_legendary_warrior_1, ":troop_no"),
					(troop_set_slot, tpe_award_data, tpe_legendary_warrior_2, ":troop_no"),
				(try_end),
				
				
			(else_try), ### DOMINANT PRESENCE 25% ###
				(store_div, ":quarter_cutoff", "$g_tournament_num_participants_for_fight", 4),
				(ge, "$g_tournament_num_participants_for_fight", tpe_berserker_min_participants),
				(ge, ":personal_kills", ":quarter_cutoff"),
				(try_begin),
					(troop_slot_eq, TPE_OPTIONS, tpe_val_opt_awards, 1), # Player option to enable/disable award displays.
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_1, ":troop_no"),
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_2, ":troop_no"),
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_3, ":troop_no"),
					(display_message, "@AWARD GRANTED: {s31} has earned the DOMINANT PRESENCE award.", ":color"),
				(try_end),
				(try_begin),
					(troop_slot_eq, tpe_award_data, tpe_berserker_1, -1),
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_2, ":troop_no"),
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_3, ":troop_no"),
					(troop_set_slot, tpe_award_data, tpe_berserker_1, ":troop_no"),
				(else_try),
					(troop_slot_eq, tpe_award_data, tpe_berserker_2, -1),
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_1, ":troop_no"),
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_3, ":troop_no"),
					(troop_set_slot, tpe_award_data, tpe_berserker_2, ":troop_no"),
				(else_try),
					(troop_slot_eq, tpe_award_data, tpe_berserker_3, -1),
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_1, ":troop_no"),
					(neg|troop_slot_eq, tpe_award_data, tpe_berserker_2, ":troop_no"),
					(troop_set_slot, tpe_award_data, tpe_berserker_3, ":troop_no"),
				(try_end),
				
			(try_end),
		(try_end),
		
	]),
	
# # script_tpe_initialize_award_data_per_round
# # Clears out all award data each round.
# ("tpe_initialize_award_data_per_round",
    # [
		# (try_for_range, ":award_slot", tpe_awards_begin, tpe_awards_end),
			# (troop_set_slot, tpe_award_data, ":award_slot", -1),
		# (try_end),
	# ]),
	
	
# script_tpe_increase_award_count
# Adds an input value (arg2) to the current tally of awards won by the troop (arg1).
("tpe_increase_award_count",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":new_awards", 2),
		
		(troop_get_slot, ":awards", ":troop_no", slot_troop_tournament_awards),
		(val_add, ":awards", ":new_awards"),
		(troop_set_slot, ":troop_no", slot_troop_tournament_awards, ":awards"),
	]),
	
# script_tpe_score_non_participants
# Clears out all award data each round.
("tpe_score_non_participants",
    [
		# Determine who didn't play.
		(assign, ":non_player_tally", 0),
		(try_for_range, ":slot", 0, wp_tpe_max_tournament_participants),
			(troop_get_slot, ":troop_no", tpe_tournament_roster, ":slot"),
			(troop_set_slot, ":troop_no", slot_troop_tournament_odds_worth, 0),   # Cleaning this out so I can sort by it later.
			(troop_slot_eq, ":troop_no", slot_troop_tournament_participating, 0),
			(troop_get_slot, ":points", ":troop_no", slot_troop_tournament_total_points),
			(troop_set_slot, ":troop_no", slot_troop_tournament_odds_worth, ":points"), # was reg1
			(val_add, ":non_player_tally", 1),
		(try_end),
		(assign, ":cutoff", ":non_player_tally"), # This "cutoff" should track how many people are still alive of the non-players in our mock fight.
		
		(store_sub, ":threshold", "$g_tournament_next_num_teams", 1), # Inserted to limit small matches really penalizing the player.
		(val_max, ":threshold", 1), # Prevent 1v* fights yielding a threshold of 0.
		
		(call_script, "script_tpe_sort_troops_and_points", slot_troop_tournament_odds_worth),
		(try_for_range, ":unused", 1, ":threshold"),
			(val_div, ":cutoff", 2),
			#(ge, ":cutoff", 2),
			(try_for_range, ":winners", 0, ":cutoff"),
				(troop_get_slot, ":troop_no", tpe_ranking_array, ":winners"),
				(troop_slot_eq, ":troop_no", slot_troop_tournament_participating, 0),
				(neq, ":troop_no", "trp_player"), # Shouldn't be required, but somehow the player gets into the mix.
				(troop_get_slot, ":points", ":troop_no", slot_troop_tournament_total_points),
				(val_add, ":points", 1),
				(troop_set_slot, ":troop_no", slot_troop_tournament_total_points, ":points"),
				#### DIAGNOSTIC BEYOND THIS POINT ####
				(ge, DEBUG_TPE_general, 2),
				(troop_get_slot, reg31, ":troop_no", slot_troop_tournament_odds_worth),
				(assign, reg32, ":points"),
				(str_store_troop_name, s31, ":troop_no"),
				(display_message, "@DEBUG (TPE): {s31} gains 1 point.  {reg32} points total.  Worth = {reg31}"),
			(try_end),
		(try_end),
		
		# Award survivor points.
		(try_for_range, ":winners", 0, ":cutoff"),
			(troop_get_slot, ":troop_no", tpe_ranking_array, ":winners"),
			(troop_slot_eq, ":troop_no", slot_troop_tournament_participating, 0),
			(neq, ":troop_no", "trp_player"), # Shouldn't be required, but somehow the player gets into the mix.
			(troop_get_slot, ":points", ":troop_no", slot_troop_tournament_total_points),
			(val_add, ":points", 2),
			(troop_set_slot, ":troop_no", slot_troop_tournament_total_points, ":points"),
			#### DIAGNOSTIC BEYOND THIS POINT ####
			(ge, DEBUG_TPE_general, 2),
			(troop_get_slot, reg31, ":troop_no", slot_troop_tournament_odds_worth),
			(assign, reg32, ":points"),
			(str_store_troop_name, s31, ":troop_no"),
			(display_message, "@DEBUG (TPE): {s31} gains 2 point for surviving.  {reg32} points total.  Worth = {reg31}"),
		(try_end),
		
		# Set the ranking back the way it should be.
		(call_script, "script_tpe_sort_troops_and_points", slot_troop_tournament_total_points),
	]),
	
# script_tpe_get_difficulty_value
# Returns the current difficulty value based on player options.
# Input:  none
# Output: reg1 (difficulty value)
  ("tpe_get_difficulty_value",
    [
		(assign, ":score", 0),
		
		# Determine player's difficulty slider setting. (0% - 36%)
		(try_begin),
			## ELIMINATION MODE ##
			# Since the difficulty slider cannot be adjusted it is considered as set at 100% difficulty.
			(eq, "$tpe_tournament_mode", tpe_mode_elimination),
			(val_add, ":score", 36),
		(else_try),
			## PERFORMANCE MODE ##
			(troop_get_slot, ":difficulty_setting", TPE_OPTIONS, tpe_val_diff_setting),      # Setting is 1 (easy) - 24 (hard)
			(val_max, ":difficulty_setting", 1), # Prevent possible Div/0 errors.
			(store_div, ":difficulty_additive", ":difficulty_setting", 2),
			(val_add, ":score", ":difficulty_setting"),
			(val_add, ":score", ":difficulty_additive"),
		(try_end),
		
		# Determine if level scaling is enabled. (0% / 20%)
		(try_begin),
			(troop_slot_eq, TPE_OPTIONS, tpe_val_level_scale, 1),                        # 1 = YES, 0 = NO
			(val_add, ":score", 20),
		(try_end),
		
		# Determine if the player is choosing his team or leaving it random. (0% / 5%)
		(try_begin),
			(troop_slot_eq, "trp_player", slot_troop_tournament_team_request, 4),        # 0 = Random.  Anything else is not.
			(val_add, ":score", 5),
		(try_end),
		
		# Get game settings for damage done to the player. (0% / 12% / 24%)
		(options_get_damage_to_player, ":player_damage_setting"),                        # 0 = 1/4, 1 = 1/2, 2 = 1/1
		(try_begin),
			(eq, ":player_damage_setting", 2),
			(val_add, ":score", 24),
		(else_try),
			(eq, ":player_damage_setting", 1),
			(val_add, ":score", 12),
		(try_end),
		
		# Get the player's settings on randomizing equipment or selecting it. (0% / 10%)
		(try_begin),
			(troop_slot_eq, "trp_player", slot_troop_tournament_always_randomize, 1),    # 1 = randomize
			(val_add, ":score", 10),
		(try_end),
		
		# Get the player's settings on scene choice. (0% / 5%)
		(try_begin),
			(party_slot_eq, "$current_town", slot_town_arena_option, 1),
			(val_add, ":score", 5),
		(try_end),
		
		(assign, reg1, ":score"),
		
		# Update presentation values if active.
		(try_begin),
			(is_presentation_active, "prsnt_tournament_options_panel"),
			(troop_get_slot, ":object", "trp_tpe_presobj", tpe_text_difficulty_score),
			(str_store_string, s21, "@{reg1}% Difficulty"),
			(overlay_set_text, ":object", "@{s21}"),
		# (else_try),
			# (is_presentation_active, "prsnt_tpe_ranking_display"),
			# (eq, DEBUG_TPE_general, 0), # Object isn't displayed otherwise.
			# (troop_get_slot, ":object", "trp_tpe_presobj", tpe_text_difficulty_score),
			# (str_store_string, s21, "@{reg1}% Difficulty"),
			# (overlay_set_text, ":object", "@{s21}"),
		(try_end),
	]),
# END - IN-COMBAT DISPLAY SCRIPTS
	
###########################################################################################################################
#####                                        TOURNAMENT DESIGN PANEL SCRIPTS                                          #####
###########################################################################################################################
# script_tdp_create_slider
# Creates a slider.
# Input: min, max, pos_x, pos_y, storage_id, value_id
# Output: none
("tdp_create_slider",
		[
			(store_script_param, ":pos_x", 1),
			(store_script_param, ":pos_y", 2),
			(store_script_param, ":storage", 3),
			(store_script_param, ":value_id", 4),
			
			(set_fixed_point_multiplier, 1000),
			
			(store_sub, ":town_slot_offset", "$tournament_town", towns_begin),
			(val_mul, ":town_slot_offset", 10),
			(val_add, ":town_slot_offset", ":value_id"),
			
			(store_add, ":text_pos_y", ":pos_y", 0), (position_set_y, pos1, ":text_pos_y"),
			(store_add, ":text_pos_x", ":pos_x", 125), (position_set_x, pos1, ":text_pos_x"),
			(create_slider_overlay, reg1, 0, 100),
			(troop_set_slot, tdp_objects, ":storage", reg1),
			(overlay_set_position, reg1, pos1),
			(troop_get_slot, ":value", tpe_settings, ":town_slot_offset"),
			(overlay_set_val, reg1, ":value"),
		]
	),
	
# script_tdp_update_slider
# Updates a slider based upon player input.
# Input: storage_id, value_id, new_value
# Output: none
("tdp_update_slider",
		[
			(store_script_param, ":storage_slot", 1),
			(store_script_param, ":setting_slot", 2),
			(store_script_param, ":value", 3),
			
			(store_sub, ":town_slot_offset", "$tournament_town", towns_begin),
			(val_mul, ":town_slot_offset", 10),
			(val_add, ":town_slot_offset", ":setting_slot"),
			(store_add, ":label_slot", ":storage_slot", 9),
			
			(troop_get_slot, ":obj_storage", tdp_objects, ":storage_slot"),
			# (troop_get_slot, ":obj_label",   tdp_objects, ":label_slot"),
			# (troop_get_slot, ":obj_real",    tdp_objects, ":real_slot"),
			(overlay_set_val, ":obj_storage", ":value"),
			(troop_set_slot, tpe_settings, ":town_slot_offset", ":value"),
			(assign, reg21, ":value"),
			#(str_store_string, s21, "@{reg21}%"),
			(overlay_set_text, ":label_slot", "@{reg21}%"),
			
			(try_begin),
				# Anti-Exploit - Establish minimum mount chance of 50% if player has them selected.
				(troop_slot_eq, "trp_player", slot_troop_tournament_horse, 1),
				(troop_slot_eq, tdp_objects, tdp_obj_slider_horse, ":storage_slot"),
				(is_between, ":value", 1, 50),
				(troop_set_slot, tpe_settings, ":town_slot_offset", 50),
				(assign, reg21, 50),
				#(str_store_string, s21, "@{reg21}%"),
				(overlay_set_text, ":label_slot", "@{reg21}%"),
				#(overlay_set_color, ":obj_label", gpu_red),
				(overlay_set_val, ":obj_storage", reg21),
			(try_end),
			
			
			(call_script, "script_tpe_determine_real_chance"),
			
			#### Diagnostic ####
			# (assign, reg22, ":setting_slot"),
			# (assign, reg23, ":storage_slot"),
			# (assign, reg24, ":obj_label"),
			# (assign, reg25, ":obj_storage"),
			# (display_message, "@DEBUG (TDP): value {reg21}, setting slot {reg22}, storage slot {reg23} & obj {reg25}, label obj {reg24}."),
		]
	),

	
# script_tdp_update_menu_selection
# Updates a slider based upon player input.
# Input: weapon type, menu selection, slot offset
# Output: none
("tdp_update_menu_selection",
		[
			(store_script_param, ":type",      1),
			(store_script_param, ":offset",    2),
			(store_script_param, ":selection", 3),
			
			# Filter the menu selection out for error tracking.
			(val_min, ":selection", 9),
			(val_max, ":selection", 0),
			(store_add, ":slot", ":offset", ":selection"),
			
			(troop_get_slot, ":item_no", tpe_weapons, ":slot"),
			
			# Store our new weapon preference.
			(store_sub, ":appearance_slot", "$tournament_town", towns_begin),      # Get center # (i.e. Town #13)
			(val_mul, ":appearance_slot", 10),                                     # Convert to basic initial slot range in tpe_appearances.  Town 13 -> slot 130.
			(val_add, ":appearance_slot", ":type"),                                # Get the specific slot for that town range.  Town 13 (lances) -> slot 131.
			
			(troop_set_slot, tpe_appearance, ":appearance_slot", ":item_no"),      # Store the item_no for the menu choice.
			(troop_set_slot, tpe_menu_options, ":appearance_slot", ":selection"),  # Set the menu options.
			
			(try_begin),  ### DIAGNOSTIC ###
				(ge, DEBUG_TPE_DESIGN, 1),
				(assign, reg21, ":slot"),
				(assign, reg22, ":appearance_slot"),
				(str_store_item_name, s21, ":item_no"),
				(display_message, "@DEBUG (TPE Design): Item '{s21}' [#{reg21}] stored in slot {reg22} of tpe_appearances."),
			(try_end),
		]
	),
	
# script_tdp_define_weapons
# Sets the item numbers associated with each weapon slot for player customization.
# Input: none
# Output: none
("tdp_define_weapons",
		[
			# Lances - 10 - 19
			(assign, ":slot", tpe_weapons_lance),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_default_lance),
			
			# Archery - 20 - 29
			(assign, ":slot", tpe_weapons_archery),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_default_bow),
			
			# One Hand - 30 - 39
			(assign, ":slot", tpe_weapons_onehand),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_default_onehand),
			(val_add, ":slot", 1),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_alt_onehand_1),
			(val_add, ":slot", 1),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_alt_onehand_2),
			
			# Two Hand - 40 - 49
			(assign, ":slot", tpe_weapons_twohand),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_default_twohand),
			(val_add, ":slot", 1),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_alt_twohand_1),
			# (val_add, ":slot", 1),
			# (troop_set_slot, tpe_weapons, ":slot", wp_tpe_alt_twohand_2),
			
			# Crossbow - 50 - 59
			(assign, ":slot", tpe_weapons_crossbow),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_default_crossbow),
			
			# Throwing - 60 - 69
			(assign, ":slot", tpe_weapons_throwing),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_default_javelin),
			(val_add, ":slot", 1),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_alt_throwing_1),
			(val_add, ":slot", 1),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_alt_throwing_2),
			
			# Polearm - 70 - 79
			(assign, ":slot", tpe_weapons_polearm),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_default_polearm),
			(val_add, ":slot", 1),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_alt_polearm_1),
			# (val_add, ":slot", 1),
			# (troop_set_slot, tpe_weapons, ":slot", wp_tpe_alt_polearm_2),
			
			# Mount - 80 - 89
			(assign, ":slot", tpe_weapons_mount),
			(troop_set_slot, tpe_weapons, ":slot", wp_tpe_default_horse),
			
			# Outfit - 90 - 99
			(assign, ":slot", tpe_weapons_outfit),
			(troop_set_slot, tpe_weapons, ":slot", "itm_red_tpe_tunic"),
			
		]
	),

# script_tpe_initialize_default_weapons
# Initialize the player settings for weapons in each center.
# Input: none
# Output: none
  ("tpe_initialize_default_weapons",
    [
		(try_for_range, ":center_no", towns_begin, towns_end),
			(store_sub, ":slot_base", ":center_no", towns_begin),
			(val_mul, ":slot_base", 10),
			# Lances
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_lance),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_lance),
			# Archery
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_archery),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_bow),
			# One Handed
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_onehand),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_onehand),
			# Two Handed
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_twohand),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_twohand),
			# Crossbows
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_crossbow),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_crossbow),
			# Throwing
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_throwing),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_javelin),
			# Polearms
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_polearm),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_polearm),
			# Mounts
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_horse),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_horse),
			# Outfits
			(store_add, ":slot_no", ":slot_base", tdp_val_setting_outfit),
			(troop_set_slot, tpe_appearance, ":slot_no", wp_tpe_default_armor),
		(try_end),
	]),

# script_tpe_determine_real_chance
# Initialize the player settings.
# Input: none
# Output: none
  ("tpe_determine_real_chance",
    [
		(store_sub, ":city_offset", "$tournament_town", towns_begin),
		(store_mul, ":slot_base", ":city_offset", 10),
		
		### MELEE WEAPONS ###
		(store_add, ":slot_onehand", ":slot_base", tdp_val_setting_onehand),
		(store_add, ":slot_twohand", ":slot_base", tdp_val_setting_twohand),
		(store_add, ":slot_polearm", ":slot_base", tdp_val_setting_polearm),
		(troop_get_slot, ":chance_onehand", tpe_settings, ":slot_onehand"),
		(troop_get_slot, ":chance_twohand", tpe_settings, ":slot_twohand"),
		(troop_get_slot, ":chance_polearm", tpe_settings, ":slot_polearm"),
		(assign, ":total", ":chance_onehand"),
		(val_add, ":total", ":chance_twohand"),
		(val_add, ":total", ":chance_polearm"),
		(val_max,   ":total", 1), # Prevent Div/0 errors.
		
		# One Hand
		(store_mul, reg21, ":chance_onehand", 100),
		(val_div,   reg21, ":total"),
		(troop_get_slot, ":obj_text", tdp_objects, tdp_obj_label_real_chance_of_onehand),
		(overlay_set_text, ":obj_text", "@{reg21}%"),
		# Two Hand
		(store_mul, reg21, ":chance_twohand", 100),
		(val_div,   reg21, ":total"),
		(troop_get_slot, ":obj_text", tdp_objects, tdp_obj_label_real_chance_of_twohand),
		(overlay_set_text, ":obj_text", "@{reg21}%"),
		# Polearm
		(store_mul, reg21, ":chance_polearm", 100),
		(val_div,   reg21, ":total"),
		(troop_get_slot, ":obj_text", tdp_objects, tdp_obj_label_real_chance_of_polearm),
		(overlay_set_text, ":obj_text", "@{reg21}%"),
		
		### RANGED WEAPONS & LANCES ###
		(store_add, ":slot_lance", ":slot_base", tdp_val_setting_lance),
		(store_add, ":slot_archery", ":slot_base", tdp_val_setting_archery),
		(store_add, ":slot_crossbow", ":slot_base", tdp_val_setting_crossbow),
		(store_add, ":slot_throwing", ":slot_base", tdp_val_setting_throwing),
		(troop_get_slot, ":chance_lance", tpe_settings, ":slot_lance"),
		(troop_get_slot, ":chance_archery", tpe_settings, ":slot_archery"),
		(troop_get_slot, ":chance_crossbow", tpe_settings, ":slot_crossbow"),
		(troop_get_slot, ":chance_throwing", tpe_settings, ":slot_throwing"),
		(assign,  ":total", ":chance_lance"),
		(val_add, ":total", ":chance_archery"),
		(val_add, ":total", ":chance_crossbow"),
		(val_add, ":total", ":chance_throwing"),
		(val_max,   ":total", 1), # Prevent Div/0 errors.
		
		# Lance
		(store_mul, reg21, ":chance_lance", 100),
		(val_div,   reg21, ":total"),
		(troop_get_slot, ":obj_text", tdp_objects, tdp_obj_label_real_chance_of_lance),
		(overlay_set_text, ":obj_text", "@{reg21}%"),
		
		# Archery
		(store_mul, reg21, ":chance_archery", 100),
		(val_div,   reg21, ":total"),
		(troop_get_slot, ":obj_text", tdp_objects, tdp_obj_label_real_chance_of_archery),
		(overlay_set_text, ":obj_text", "@{reg21}%"),
		
		# Crossbow
		(store_mul, reg21, ":chance_crossbow", 100),
		(val_div,   reg21, ":total"),
		(troop_get_slot, ":obj_text", tdp_objects, tdp_obj_label_real_chance_of_crossbow),
		(overlay_set_text, ":obj_text", "@{reg21}%"),
		
		# Throwning
		(store_mul, reg21, ":chance_throwing", 100),
		(val_div,   reg21, ":total"),
		(troop_get_slot, ":obj_text", tdp_objects, tdp_obj_label_real_chance_of_throwing),
		(overlay_set_text, ":obj_text", "@{reg21}%"),
		
		### MOUNTS ###
		(store_add, ":slot_horse", ":slot_base", tdp_val_setting_horse),
		(troop_get_slot, reg21, tpe_settings, ":slot_horse"),
		(troop_get_slot, ":obj_text", tdp_objects, tdp_obj_label_real_chance_of_mount),
		(overlay_set_text, ":obj_text", "@{reg21}%"),
	]),
	
# script_tpe_initialize_default_design_settings
# Initialize the default settings of load chances in each center.
# Input: none
# Output: none
("tpe_initialize_default_design_settings",
    [
		(store_script_param, ":center_no", 1),
		(store_sub, ":slot_base", ":center_no", towns_begin),
		(val_mul, ":slot_base", 10),
		(try_for_range, ":setting_slot", tdp_val_setting_lance, tdp_val_setting_horse),
			(store_add, ":slot_no", ":slot_base", ":setting_slot"),
			(troop_set_slot, tpe_settings, ":slot_no", 100),
		(try_end),
		# Mounts
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_horse),
		(troop_set_slot, tpe_settings, ":slot_no", 50),
		(try_begin),
			(eq, MOD_ARENA_OVERHAUL_INSTALLED, 1),
			(party_set_slot, ":center_no", slot_town_arena_option, tpe_default_arena_scene),
		(try_end),
	]),
	
# script_tpe_initialize_native_design_settings
# Initialize the default settings of load chances in each center.
# Input: none
# Output: none
("tpe_initialize_native_design_settings",
    [
		(store_script_param, ":center_no", 1),
		
		(try_begin),
			(eq, ":center_no", "p_town_1"), 
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 0, 0, 50, 80, 0, 0, 0, 0), # Sargoth
		(else_try),
			(eq, ":center_no", "p_town_2"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 0, 0, 50, 80, 50, 0, 0, 0), # Tihr
		(else_try),
			(eq, ":center_no", "p_town_4"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 40, 80, 50, 20, 0, 0, 0, 0), # Suno
		(else_try),
			(eq, ":center_no", "p_town_6"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 100, 100, 0, 0, 0, 0, 0, 0), # Praven
		(else_try),
			(eq, ":center_no", "p_town_7"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 100, 0, 100, 0, 0, 0, 0, 0), # Uxkhal
		(else_try),
			(eq, ":center_no", "p_town_8"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 40, 80, 50, 20, 0, 0, 0, 0), # Reyvadin
		(else_try),
			(eq, ":center_no", "p_town_9"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 100, 50, 0, 0, 0, 20, 30, 0), # Khudan
		(else_try),
			(this_or_next|eq, ":center_no", "p_town_10"),    # Tulga
			(eq, ":center_no", "p_town_17"),                 # Ichamur
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 100, 0, 0, 0, 0, 40, 60, 0), 
		(else_try),
			(eq, ":center_no", "p_town_11"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 100, 0, 50, 0, 0, 20, 30, 0), # Curaw
		(else_try),
			(eq, ":center_no", "p_town_12"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 40, 0, 0, 100, 0, 0, 0, 0), # Wercheg
		(else_try),
			(eq, ":center_no", "p_town_13"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 40, 80, 50, 20, 30, 0, 60, 0), # Rivacheg
		(else_try),
			(this_or_next|eq, ":center_no", "p_town_14"),    # Halmar
			(eq, ":center_no", "p_town_18"),                 # Narra
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 100, 50, 25, 0, 0, 30, 50, 0), 
		(else_try),
			(this_or_next|eq, ":center_no", "p_town_5"),     # Jelkala
			(this_or_next|eq, ":center_no", "p_town_15"),    # Yalen
			(eq, ":center_no", "p_town_3"),                  # Veluca
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 25, 100, 60, 0, 30, 0, 30, 50),
		(else_try),
			(eq, ":center_no", "p_town_16"),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 40, 80, 50, 20, 40, 0, 0, 0), # Dhirim
		(else_try),
			(this_or_next|eq, ":center_no", "p_town_19"),    # Shariz
			(eq, ":center_no", "p_town_21"),                 # Ahmerrad
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 100, 40, 60, 0, 30, 30, 0, 0),
		(else_try),
			(this_or_next|eq, ":center_no", "p_town_20"),    # Durquba
			(eq, ":center_no", "p_town_22"),                 # Bariyye
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 50, 0, 60, 0, 30, 30, 0, 0),
		(else_try),
			(call_script, "script_tpe_define_city_native_settings", ":center_no", 50, 100, 100, 100, 100, 100, 100, 100), # Default Response
		(try_end),
		(party_set_slot, ":center_no", slot_town_arena_option, 0),
	]),

# script_tpe_define_city_native_settings
# Initialize the default settings of load chances in each center.
# Input: none
# Output: none
("tpe_define_city_native_settings",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":horse_chance", 2),
		(store_script_param, ":lance_chance", 3),
		(store_script_param, ":sword_chance", 4),
		(store_script_param, ":axe_chance", 5),
		(store_script_param, ":bow_chance", 6),
		(store_script_param, ":javelin_chance", 7),
		(store_script_param, ":mounted_bow_chance", 8),
		(store_script_param, ":crossbow_sword_chance", 9),
		# (store_script_param, ":armor_item_begin", 9),
		# (store_script_param, ":helm_item_begin", 10),
		
		(store_add, ":total_chance", ":sword_chance", ":axe_chance"),
		(val_add, ":total_chance", ":crossbow_sword_chance"),
		(val_min, ":total_chance", 100),
		
		(val_add, ":bow_chance", ":mounted_bow_chance"),
		(val_min, ":bow_chance", 100),
		
		(store_sub, ":slot_base", ":center_no", towns_begin),
		(val_mul, ":slot_base", 10),
		# Lances
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_lance),
		(troop_set_slot, tpe_settings, ":slot_no", ":lance_chance"),
		# Archery
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_archery),
		(troop_set_slot, tpe_settings, ":slot_no", ":bow_chance"),
		# One Handed
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_onehand),
		(troop_set_slot, tpe_settings, ":slot_no", ":total_chance"),
		# Two Handed
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_twohand),
		(troop_set_slot, tpe_settings, ":slot_no", ":total_chance"),
		# Crossbows
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_crossbow),
		(troop_set_slot, tpe_settings, ":slot_no", ":crossbow_sword_chance"),
		# Throwing
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_throwing),
		(troop_set_slot, tpe_settings, ":slot_no", ":javelin_chance"),
		# Polearms
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_polearm),
		(troop_set_slot, tpe_settings, ":slot_no", 0),
		# Mounts
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_horse),
		(troop_set_slot, tpe_settings, ":slot_no", ":horse_chance"),
		# Outfits
		(store_add, ":slot_no", ":slot_base", tdp_val_setting_outfit),
		(troop_set_slot, tpe_settings, ":slot_no", 100),
	]),

# END - TOURNAMENT DESIGN PANEL SCRIPTS

###########################################################################################################################
#####                                           TOURNAMENT QUEST SCRIPTS                                              #####
###########################################################################################################################

# script_quest_floris_active_tournament_hook_1
# Causes the quest to register as being completed successfully if you enter the town the tournament is being held in while having the quest active and join the tournament.
# Input: none
# Output: none
("quest_floris_active_tournament_hook_1",
    [
	    (try_begin),
			(check_quest_active, "qst_floris_active_tournament"),
			(neg|quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_participated_in_tournament), # Prevents repeated reputation gains in the TPE menu.
			(quest_slot_eq, "qst_floris_active_tournament", slot_quest_target_center, "$current_town"),
			(try_begin),
				(quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_message_received), # You were invited to attend.  Still need to meet with host.
				(call_script, "script_succeed_quest", "qst_floris_active_tournament"),
				(call_script, "script_common_quest_change_state", "qst_floris_active_tournament", qp1_tournament_participated_in_tournament),
				(call_script, "script_quest_floris_active_tournament", floris_quest_update),
			(else_try),
				(quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, 0), # You were not invited to attend.  Quest is automatically completed.
				(call_script, "script_quest_floris_active_tournament", floris_quest_succeed),
			(try_end),
			(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
			(troop_slot_ge, "trp_player", slot_troop_renown, 200),
			(call_script, "script_change_player_relation_with_center", "$current_town", 2),
		(try_end),
    ]),
	
# script_quest_floris_active_tournament
# Handles all quest specific actions for quest "floris_active_tournament".
# INPUT: none
# OUTPUT: none
("quest_floris_active_tournament",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_floris_active_tournament"),
		(assign, ":quest_title", "str_qp1_tournament_invitation_title"),
		(str_store_string, s41, ":quest_title"),
		# Get specific string data.
		(try_begin),
			(check_quest_active, ":quest_no"),
			(quest_get_slot, ":troop_giver", ":quest_no", slot_quest_giver_troop),
			(quest_get_slot, ":center_giver", ":quest_no", slot_quest_target_center),
			(str_store_party_name, s13, ":center_giver"),
			(str_store_troop_name, s14, ":troop_giver"),
			(troop_get_type, reg3, ":troop_giver"),
		(try_end),
		
		# Quest Stages
		# qp1_tournament_message_received                 = 1
		# qp1_tournament_participated_in_tournament       = 2
		# qp1_tournament_refused_invitation               = 3
		
		(try_begin),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_setup),
			
			
		(else_try),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			(quest_get_slot, ":center_no", ":quest_no", slot_quest_target_center),
			(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
			
			# Setup quest text.
			(str_store_party_name_link, s13, ":center_no"),
			# (str_store_string, s61,       "str_qp4_edwyn_third_knight_quest_text"),
			# Setup quest parameters.
			# (quest_set_slot, ":quest_no", slot_quest_current_state,                   qp4_edwyn_third_begun),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     ":town_lord"),
			(quest_set_slot, ":quest_no", slot_quest_target_troop,                    ":town_lord"),
			# (quest_set_slot, ":quest_no", slot_quest_giver_center,                    ":center_no"),
			# (quest_set_slot, ":quest_no", slot_quest_expiration_days,                 90),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          10),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  10),
			# (quest_set_slot, ":quest_no", slot_quest_xp_reward,                       100),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			
			# Set quest to active.
			(str_store_troop_name_link, s9, ":town_lord"),
			(str_store_party_name_link, s13, ":center_no"),
			(str_store_troop_name, s8, ":town_lord"),
			(str_store_party_name, s12, ":center_no"),
			(try_begin), # Checks if your renown warrants an invitation based on distance away.
				(store_distance_to_party_from_party, ":distance", "p_main_party", ":center_no"),
				(val_mul, ":distance", 2),
				# Make sure you're close enough to bother with a random invitation.
				(try_begin),
					(assign, ":check_distance", 0),
					(troop_slot_ge, "trp_player", slot_troop_renown, 50),
					(troop_slot_ge, "trp_player", slot_troop_renown, ":distance"),
					(assign, ":check_distance", 1),
				(try_end),
				# Check if Lord is a friend.
				(try_begin),
					(assign, ":check_relation", 0),
					(ge, ":town_lord", 1),
					(call_script, "script_troop_get_player_relation", ":town_lord"),
					(ge, reg0, 10),
					(assign, ":check_relation", 1),
				(try_end),
				# Check if host is of the same faction.
				(try_begin),
					(assign, ":check_faction", 0),
					(call_script, "script_tpe_store_town_faction_to_reg0", ":center_no"),
					(eq, reg0, "$players_kingdom"),
					(assign, ":check_faction", 1),
				(try_end),
				(this_or_next|eq, ":check_faction", 1),
				(eq, ":check_distance", 1),
				(this_or_next|eq, ":check_faction", 1),
				(eq, ":check_relation", 1),
				# Ensure town lord isn't a prisoner somewhere.
				(troop_slot_eq, ":town_lord", slot_troop_prisoner_of_party, -1),
				
				(dialog_box, "str_qp1_tournaments_invited_by_s8_to_s12", "@A Messenger Arrives"),
				(str_store_string, s2, "str_qp1_quest_desc_tournament_invited_by_s9_to_s13"),
				(quest_set_slot, ":quest_no", slot_quest_current_state, qp1_tournament_message_received),
			(else_try),
				(dialog_box, "str_qp1_tournaments_held_by_s8_in_s12", "@Rumor of the Road"),
				(str_store_string, s2, "str_qp1_quest_desc_tournament_held_by_s9_to_s13"),
				(quest_set_slot, ":quest_no", slot_quest_current_state, 0), # Should mean no one cares if you come or not.
			(try_end),
			# Set the duration of the quest.
			(party_get_slot, ":days_left", ":center_no", slot_town_has_tournament),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days, ":days_left"),
			(setup_quest_text, ":quest_no"),
			(call_script, "script_start_quest", ":quest_no", ":town_lord"),
			(str_clear, s1),
			(add_quest_note_from_sreg, ":quest_no", 3, s1, 0),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(try_begin),
				(eq, ":quest_stage", qp1_tournament_participated_in_tournament),
				(str_store_string, s65, "@You have participated in the tournament at {s13} and {s14} will wish to speak with you."),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp1_tournament_refused_invitation),
				(str_store_string, s65, "@You have failed to participate in the tournament at {s13}.  {s14} will be most displeased, but you should speak with {reg3?her:him} and ease any offense."),
				(assign, ":note_slot", 3),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			(display_message, "str_quest_log_updated"),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(complete_quest, "qst_floris_active_tournament"),
			# Rewards
			(try_begin),
				(assign, ":reward_xp", 150),
				(assign, ":reward_relation", 1),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":reward_xp", 150),
				(val_add, ":reward_relation", 1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":reward_xp", 200),
				(val_add, ":reward_relation", 1),
			(try_end),
			(add_xp_to_troop, ":reward_xp", "trp_player"),
			(try_begin),
				(quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_participated_in_tournament), # If you weren't invited then no one should care if you don't attend.
				(quest_get_slot, ":town_lord", "qst_floris_active_tournament", slot_quest_giver_troop),
				(call_script, "script_troop_change_relation_with_troop", "trp_player", ":town_lord", ":reward_relation"),
			(try_end),
			(quest_set_slot, "qst_floris_active_tournament", slot_quest_current_state, 0),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			# Set quest to failed due to timeout.
			(fail_quest, ":quest_no"),
			(complete_quest, ":quest_no"),
			(quest_set_slot, ":quest_no", slot_quest_current_state, qp1_tournament_refused_invitation),
			(try_begin),
				(quest_slot_eq, ":quest_no", slot_quest_current_state, qp1_tournament_message_received), # If you weren't invited then no one should care if you don't attend.
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(call_script, "script_change_troop_renown", "trp_player", -2),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(quest_get_slot, ":town_lord", ":quest_no", slot_quest_giver_troop),
				(str_store_troop_name, s21, ":town_lord"),
				(display_message, "@{s21} is insulted by your refusal of his invitation.", gpu_red),
				(call_script, "script_troop_change_relation_with_troop", "trp_player", ":town_lord", -2),
			(try_end),
			(display_message, "@The tournament in {s13} has ended."),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence.", gpu_light_blue),
			(display_message, "@Quest ended due to {s13} becoming a hostile city."),
			(quest_set_slot, ":quest_no", slot_quest_current_state, 0),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
	
	
# script_quest_score_to_settle
# Handles all quest specific actions for quest "qp1_score_to_settle".
("quest_score_to_settle",
  [
		(store_script_param, ":function", 1),
		(assign, ":quest_no",    "qst_score_to_settle"),
		# Get specific string data.
		(assign, ":quest_title", "str_qp1_score_to_settle_title"),
		(str_store_string, s41, ":quest_title"),
		
		# Quest Stages
		# qp1_score_to_settle_inactive                    = 0
		# qp1_score_to_settle_begun                       = 1
		# qp1_score_to_settle_defeated_once               = 2
		# qp1_score_to_settle_defeated_twice              = 3
		# qp1_score_to_settle_defeated_thrice             = 4
		
		(try_begin),
			##### QUEST START #####
			(eq, ":function", floris_quest_begin),
			# Setup quest text.
			(str_store_party_name_link, s13, "$current_town"),
			(str_store_troop_name_link, s14, "$g_talk_troop"),
			(str_store_string, s61,       "str_qp1_score_to_settle_quest_text"), # Needs: s13 (giver center), s14 (insulting lord)
			# Setup quest parameters.
			(quest_set_slot, ":quest_no", slot_quest_current_state,                   qp1_score_to_settle_begun),
			(quest_set_slot, ":quest_no", slot_quest_giver_troop,                     "$g_talk_troop"),
			(quest_set_slot, ":quest_no", slot_quest_target_troop,                    "$g_talk_troop"),
			(quest_set_slot, ":quest_no", slot_quest_giver_center,                    "$current_town"),
			(quest_set_slot, ":quest_no", slot_quest_target_center,                   -1),
			(quest_set_slot, ":quest_no", slot_quest_expiration_days,                 0),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_period,          30),
			(quest_set_slot, ":quest_no", slot_quest_dont_give_again_remaining_days,  30),
			(quest_set_slot, ":quest_no", slot_quest_comment_made,                    0),
			(quest_set_slot, ":quest_no", slot_quest_unique_name,                     ":quest_title"),
			(quest_set_slot, ":quest_no", slot_quest_target_amount,                   3),
			#(quest_set_slot, ":quest_no", slot_quest_current_tally,                   0),
			# Unique parameters.
			(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance,         -1),
			(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance,         -1),
			(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance,         -1),
			## Activate the quest. ##
			(setup_quest_text, ":quest_no"),
			(call_script, "script_common_start_quest", ":quest_no", -1, "str_qp1_quest_title"),
			
		(else_try),
			##### QUEST UPDATE #####
			(eq, ":function", floris_quest_update),
			# Get the date stamp.
			(store_current_hours, ":cur_hours"),
			(str_store_date, s64, ":cur_hours"),
			(str_store_string, s64, "@[{s64}]: "),
			# Update quest notes as required.
			(quest_get_slot, ":quest_stage", ":quest_no", slot_quest_current_state),
			(quest_get_slot, ":target_troop", ":quest_no", slot_quest_target_troop),
			(str_store_party_name_link, s14, "$current_town"),
			(str_store_troop_name_link, s13, ":target_troop"),
			(try_begin),
				(eq, ":quest_stage", qp1_score_to_settle_defeated_once),
				(str_store_string, s65, "@You managed to defeat {s13} in {s14}.  Now you need only show him up twice more."),
				(display_message, "@You have embarassed {s13} in front of the crowds at {s14}.", gpu_green),
				(quest_set_slot, ":quest_no", slot_quest_stage_1_trigger_chance, "$current_town"),
				(assign, ":note_slot", 3),
			(else_try),
				(eq, ":quest_stage", qp1_score_to_settle_defeated_twice),
				(str_store_string, s65, "@You managed to defeat {s13} in {s14}.  Now you need to show him up one more time."),
				(display_message, "@You have embarassed {s13} in front of the crowds at {s14}.", gpu_green),
				(quest_set_slot, ":quest_no", slot_quest_stage_2_trigger_chance, "$current_town"),
				(assign, ":note_slot", 4),
			(else_try),
				(eq, ":quest_stage", qp1_score_to_settle_defeated_thrice),
				(str_store_string, s65, "@You defeated {s13} yet again in front of the crowds at {s14}.  Now speak to {s13}."),
				(display_message, "@You have embarassed {s13} in front of the crowds at {s14}.", gpu_green),
				(quest_set_slot, ":quest_no", slot_quest_stage_3_trigger_chance, "$current_town"),
				(assign, ":note_slot", 5),
			(else_try),
				# Default error on failure to update note.
				(display_message, "str_common_quest_s41_update_note_error", qp_error_color),
			(try_end),
			# Update quest note.
			(str_store_string, s64, "@{s64} {s65}"),
			(add_quest_note_from_sreg, ":quest_no", ":note_slot", s64, 0),
			
		(else_try),
			##### QUEST SUCCEED #####
			(eq, ":function", floris_quest_succeed),
			# Complete the quest.
			(succeed_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Rewards
			(assign, ":reward_xp", 400),
			(assign, ":relation", 1),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":relation", 1),
				(val_add, ":reward_xp", 300),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":relation", 1),
				(val_add, ":reward_xp", 300),
			(try_end),
			# Award party experience.
			(party_add_xp, "p_main_party", ":reward_xp"),
			# Change reputation with lord.
			(quest_get_slot, ":troop_no", ":quest_no", slot_quest_giver_troop),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation", 0),
			
		(else_try),
			##### QUEST FAIL #####
			(eq, ":function", floris_quest_fail),
			(fail_quest, ":quest_no"),
			(set_show_messages, 0),
			(complete_quest, ":quest_no"),
			(set_show_messages, 1),
			# Consequences
			(assign, ":relation", -2),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(val_add, ":relation", -1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":relation", -1),
			(try_end),
			# Change town reputation.
			(quest_get_slot, ":troop_no", ":quest_no", slot_quest_giver_troop),
			(call_script, "script_change_player_relation_with_troop", ":troop_no", ":relation", 0),
			
		(else_try),
			##### QUEST CANCEL #####
			(eq, ":function", floris_quest_cancel),
			(cancel_quest, ":quest_no"),
			(display_message, "@Quest '{s41}' was canceled without consequence.", gpu_light_blue),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "str_common_quest_s41_update_error", qp_error_color),
		(try_end),
	]),
# END - TOURNAMENT QUEST SCRIPTS

###########################################################################################################################
#####                                          TOURNAMENT DEFAULT SCRIPTS                                             #####
###########################################################################################################################

# script_tpe_initialize_player_settings
# Initialize the player settings.
# Input: none
# Output: none
("tpe_initialize_player_settings",
    [
		(troop_set_slot, TPE_OPTIONS, tpe_val_opt_awards, 1),
		(troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 0),
		(troop_set_slot, "trp_tpe_presobj", tpe_checkbox_opt_damage, 0),
		(troop_set_slot, TPE_OPTIONS, tpe_val_level_scale, 1),
		(troop_set_slot, "trp_player", slot_troop_tournament_team_request, 4),
		(troop_set_slot, TPE_OPTIONS, tpe_val_show_health, 1),
		(assign, "$g_wp_tpe_active", 1),
		(assign, "$tpe_quests_active", 1),
		# (assign, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
		(assign, "$g_wp_tpe_renown_scaling", 1),
		(assign, "$g_wp_tpe_option_icd_active", 1),
		(call_script, "script_tpe_initialize_default_weapons"),
		(assign, "$tpe_tournament_mode", tpe_mode_performance),
		(assign, "$tpe_initialized", 1),
		
		#### INITIALIZE ARENA SCENES ####
		# This was done to prevent Floris 2.52 from breaking save games.
		(try_for_range, ":town_no", towns_begin, towns_end),
			(store_sub, ":offset", ":town_no", towns_begin),
			(store_add, ":cur_object_no", "scn_town_1_arena", ":offset"),
			(party_set_slot,":town_no", slot_town_arena, ":cur_object_no"),
			(store_add, ":cur_object_no", "scn_town_1_arena_alternate", ":offset"),
			(party_set_slot,":town_no", slot_town_arena_alternate, ":cur_object_no"),
		(try_end),
		#### END INITIALIZATION OF SCENES ####
		
		(try_for_range, ":center_no", towns_begin, towns_end),
			(call_script, "script_tpe_initialize_default_design_settings", ":center_no"),
		(try_end),
		
		### LORD PRESETS ###
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(neg|is_between, ":troop_no", companions_begin, companions_end),
			(troop_set_slot, ":troop_no", slot_troop_tournament_always_randomize, 1), # Bugfix - Ticket #1406, v0.23
		(try_end),
		# Setting up randomized weapon options for tournament troops.
		(try_for_range, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end),
			(troop_set_slot, ":troop_no", slot_troop_tournament_always_randomize, 1), # Bugfix - Ticket #1406, v0.23
		(try_end),
		
		### COMPANION PRESETS ###
		(try_for_range, ":troop_no", companions_begin, companions_end),
			(troop_set_slot, ":troop_no", slot_troop_tournament_always_randomize, 0),
			(troop_set_slot, ":troop_no", slot_troop_tournament_selections, 3),
			(try_for_range, ":slot_no", slot_troop_tournament_begin, slot_troop_tournament_end),
				(troop_set_slot, ":troop_no", ":slot_no", 0),
			(try_end),
		(try_end),
		## NPC1 - Borcha
		(troop_set_slot, "trp_npc1", slot_troop_tournament_twohand, 1),
		(troop_set_slot, "trp_npc1", slot_troop_tournament_throwing, 1),
		(troop_set_slot, "trp_npc1", slot_troop_tournament_enhanced_weapons, 1),
		## NPC2 - Marnid
		(troop_set_slot, "trp_npc2", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc2", slot_troop_tournament_crossbow, 1),
		(troop_set_slot, "trp_npc2", slot_troop_tournament_enhanced_armor, 1),
		## NPC3 - Ymira
		(troop_set_slot, "trp_npc3", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc3", slot_troop_tournament_crossbow, 1),
		(troop_set_slot, "trp_npc3", slot_troop_tournament_horse, 1),
		## NPC4 - Rolf
		(troop_set_slot, "trp_npc4", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc4", slot_troop_tournament_enhanced_armor, 1),
		(troop_set_slot, "trp_npc4", slot_troop_tournament_enhanced_shield, 1),
		## NPC5 - Baheshtur
		(troop_set_slot, "trp_npc5", slot_troop_tournament_twohand, 1),
		(troop_set_slot, "trp_npc5", slot_troop_tournament_bow, 1),
		(troop_set_slot, "trp_npc5", slot_troop_tournament_horse, 1),
		## NPC6 - Firentis
		(troop_set_slot, "trp_npc6", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc6", slot_troop_tournament_enhanced_armor, 1),
		(troop_set_slot, "trp_npc6", slot_troop_tournament_enhanced_weapons, 1),
		## NPC7 - Deshavi
		(troop_set_slot, "trp_npc7", slot_troop_tournament_polearm, 1),
		(troop_set_slot, "trp_npc7", slot_troop_tournament_bow, 1),
		(troop_set_slot, "trp_npc7", slot_troop_tournament_enhanced_weapons, 1),
		## NPC8 - Matheld
		(troop_set_slot, "trp_npc8", slot_troop_tournament_twohand, 1),
		(troop_set_slot, "trp_npc8", slot_troop_tournament_enhanced_armor, 1),
		(troop_set_slot, "trp_npc8", slot_troop_tournament_enhanced_weapons, 1),
		## NPC9 - Alayen
		(troop_set_slot, "trp_npc9", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc9", slot_troop_tournament_lance, 1),
		(troop_set_slot, "trp_npc9", slot_troop_tournament_horse, 1),
		## NPC10 - Bunduk
		(troop_set_slot, "trp_npc10", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc10", slot_troop_tournament_crossbow, 1),
		(troop_set_slot, "trp_npc10", slot_troop_tournament_enhanced_armor, 1),
		## NPC11 - Katrin
		(troop_set_slot, "trp_npc11", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc11", slot_troop_tournament_crossbow, 1),
		(troop_set_slot, "trp_npc11", slot_troop_tournament_enhanced_armor, 1),
		## NPC12 - Jeremus
		(troop_set_slot, "trp_npc12", slot_troop_tournament_polearm, 1),
		(troop_set_slot, "trp_npc12", slot_troop_tournament_crossbow, 1),
		(troop_set_slot, "trp_npc12", slot_troop_tournament_enhanced_armor, 1),
		## NPC13 - Nizar
		(troop_set_slot, "trp_npc13", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc13", slot_troop_tournament_enhanced_weapons, 1),
		(troop_set_slot, "trp_npc13", slot_troop_tournament_horse, 1),
		## NPC14 - Lezalit
		(troop_set_slot, "trp_npc14", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc14", slot_troop_tournament_enhanced_armor, 1),
		(troop_set_slot, "trp_npc14", slot_troop_tournament_enhanced_shield, 1),
		## NPC15 - Artimenner
		(troop_set_slot, "trp_npc15", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc15", slot_troop_tournament_crossbow, 1),
		(troop_set_slot, "trp_npc15", slot_troop_tournament_enhanced_horse, 1),
		## NPC16 - Klethi
		(troop_set_slot, "trp_npc16", slot_troop_tournament_onehand, 1),
		(troop_set_slot, "trp_npc16", slot_troop_tournament_throwing, 1),
		(troop_set_slot, "trp_npc16", slot_troop_tournament_enhanced_weapons, 1),
		## NPC17 - Nissa
		(troop_set_slot, "trp_npc17", slot_troop_tournament_polearm, 1),
		(troop_set_slot, "trp_npc17", slot_troop_tournament_bow, 1),
		(troop_set_slot, "trp_npc17", slot_troop_tournament_horse, 1),
	]),
	
# script_tpe_hook_switch_between_native_or_tpe
# Evaluates if TPE is activated and sends the player to the TPE or native menus.
# Input: none
# Output: none
("tpe_hook_switch_between_native_or_tpe",
    [
		(assign, "$g_tournament_cur_tier", 0),
		(assign, "$g_tournament_player_team_won", -1),
		(assign, "$g_tournament_bet_placed", 0),
		(assign, "$g_tournament_bet_win_amount", 0),
		(assign, "$g_tournament_last_bet_tier", -1),
		(assign, "$g_tournament_next_num_teams", 0),
		(assign, "$g_tournament_next_team_size", 0),
		(try_begin),
			(eq, "$g_wp_tpe_active", 0),
			(call_script, "script_fill_tournament_participants_troop", "$current_town", 1),
			(jump_to_menu, "mnu_town_tournament"),
		(else_try),
			(eq, "$g_wp_tpe_active", 1),
			(call_script, "script_tpe_fill_tournament_participants_troop", "$current_town", 1),
			(jump_to_menu, "mnu_tpe_town_tournament"),
		(try_end),
	]),
	
# script_tpe_store_town_faction_to_reg0
# Returns the faction number of a center under a number of different circumstances.
# Input: none
# Output: none
("tpe_store_town_faction_to_reg0",
    [
		(store_script_param, ":center_no", 1),
		
		(assign, ":faction_picked", 0),
		(try_begin),
			# Figure out faction based on center.
			(store_faction_of_party, ":faction_no", ":center_no"),
			(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(assign, ":faction_picked", ":faction_no"),
			(ge, DEBUG_TPE_general, 2),
			(str_store_faction_name, s21, ":faction_no"),
			(str_store_party_name, s22, ":center_no"),
			(display_message, "@DEBUG (TPE): Faction '{s21}' determined by '{s22}'."),
		(else_try),
			# Use the lord of the town if possible.
			(eq, ":faction_picked", 0),
			(party_get_slot, ":troop_lord", ":center_no", slot_town_lord),
			(ge, ":troop_lord", 0),
			(store_troop_faction, ":faction_no", ":troop_lord"),
			(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(assign, ":faction_picked", ":faction_no"),
			(ge, DEBUG_TPE_general, 2),
			(str_store_faction_name, s21, ":faction_no"),
			(str_store_troop_name, s22, ":troop_lord"),
			(display_message, "@DEBUG (TPE): Faction '{s21}' determined by '{s22}'."),
		(else_try),
			# No valid faction could be determined.
			(eq, ":faction_picked", 0),
			(display_message, "@TPE ERROR!  No valid faction could be determined for this town.", gpu_red),
		(try_end),
		(assign, reg0, ":faction_picked"),
	]),
# END - TOURNAMENT DESIGN PANEL SCRIPTS

###########################################################################################################################
#####                                      TOURNAMENT HALL OF RECORDS SCRIPTS                                         #####
###########################################################################################################################
# script_tpe_add_log_entry
# Adds a new log entry every time a tournament is participated in.
("tpe_add_log_entry",
    [
		# TPE_LOG_DATE                           = "trp_tpe_log_date" # Stores hours
		# TPE_LOG_LOCATION                       = "trp_tpe_log_location"
		# TPE_LOG_LEVEL                          = "trp_tpe_log_level"
		# TPE_LOG_RANK                           = "trp_tpe_log_rank"
		# TPE_LOG_DIFFICULTY                     = "trp_tpe_log_difficulty"
		# TPE_LOG_TYPE                           = "trp_tpe_log_type"
		# TPE_LOG_SURVIVED                       = "trp_tpe_log_rounds_survived"
		# TPE_LOG_SCORE                          = "trp_tpe_log_score"
		# TPE_LOG_EARNINGS                       = "trp_tpe_log_earnings"
		
		# Date of tournament.
		(store_current_hours, reg1),
		(troop_set_slot, TPE_LOG_DATE, "$tpe_total_log_entries", reg1),
		# Location of the tournament.
		(troop_set_slot, TPE_LOG_LOCATION, "$tpe_total_log_entries", "$current_town"),
		# Level of the player.
		(store_character_level, reg1, "trp_player"),
		(troop_set_slot, TPE_LOG_LEVEL, "$tpe_total_log_entries", reg1),
		# Rank of the player.
		(assign, ":rank", 0),
		(try_for_range, ":slot", 0, wp_tpe_max_tournament_participants),
			(troop_slot_eq, tpe_ranking_array, ":slot", "trp_player"),
			(store_add, ":rank", ":slot", 1),
		(try_end),
		(troop_set_slot, TPE_LOG_RANK, "$tpe_total_log_entries", ":rank"),
		# Difficulty Settings.
		(call_script, "script_tpe_get_difficulty_value"),
		(troop_set_slot, TPE_LOG_DIFFICULTY, "$tpe_total_log_entries", reg1),
		# Tournament Type.
		(troop_set_slot, TPE_LOG_TYPE, "$tpe_total_log_entries", "$tpe_tournament_mode"),
		# Number of rounds survived.
		(troop_set_slot, TPE_LOG_SURVIVED, "$tpe_total_log_entries", "$tpe_rounds_survived"),
		# Tournament Score.
		(troop_get_slot, reg1, "trp_player", slot_troop_tournament_total_points),
		(troop_set_slot, TPE_LOG_SCORE, "$tpe_total_log_entries", reg1),
		# Tournament Earnings.
		(troop_set_slot, TPE_LOG_EARNINGS, "$tpe_total_log_entries", "$tpe_total_earnings"),
		# DISPLAY OUTPUT TO PLAYER
		(display_message, "@Your tournament record has been updated...", gpu_light_blue),
		(val_add, "$tpe_total_log_entries", 1),
	]),
	
# script_tpe_get_log_data
# Returns specific log data back (via reg1, reg2 & s1) based upon the requested log entry & type.
("tpe_get_log_data",
    [
		(store_script_param, ":entry", 1),
		(store_script_param, ":log_type", 2),
		
		(assign, reg1, -1),
		(assign, reg2, -1),
		(str_clear, s1),
		(try_begin),
			### ERROR ### - Invalid entry request.
			(neg|is_between, ":entry", 0, "$tpe_total_log_entries"),
			(display_message, "@ERROR (TPE Log): Request for entry #{reg31} outside of acceptable range.", gpu_red),
			
		(else_try),
			# Date of tournament.
			(eq, ":log_type", TPE_LOG_DATE),
			(troop_get_slot, ":hours", TPE_LOG_DATE, ":entry"),
			(str_store_date, s1, ":hours"),
		
		(else_try),
			# Location of the tournament.
			(eq, ":log_type", TPE_LOG_LOCATION),
			(troop_get_slot, reg1, TPE_LOG_LOCATION, ":entry"),
			(str_store_party_name, s1, reg1),
			
		(else_try),
			# Level of the player.
			(eq, ":log_type", TPE_LOG_LEVEL),
			(troop_get_slot, reg1, TPE_LOG_LEVEL, ":entry"),
			
		(else_try),
			# Rank of the player.
			(eq, ":log_type", TPE_LOG_RANK),
			(troop_get_slot, reg1, TPE_LOG_RANK, ":entry"),
			
		(else_try),
			# Difficulty Settings.
			(eq, ":log_type", TPE_LOG_DIFFICULTY),
			(troop_get_slot, reg1, TPE_LOG_DIFFICULTY, ":entry"),
			(troop_get_slot, reg2, TPE_LOG_TYPE, ":entry"),
			(try_begin),
				(eq, reg2, tpe_mode_performance),
				(str_store_string, s1, "@Performance"),
			(else_try),
				(eq, reg2, tpe_mode_elimination),
				(str_store_string, s1, "@Elimination"),
			(try_end),
			
		(else_try),
			# Tournament Type.
			(eq, ":log_type", TPE_LOG_TYPE),
			(troop_get_slot, reg1, TPE_LOG_TYPE, ":entry"),
			
		(else_try),
			# Number of rounds survived.
			(eq, ":log_type", TPE_LOG_SURVIVED),
			(troop_get_slot, reg1, TPE_LOG_SURVIVED, ":entry"),
			(assign, reg2, wp_tpe_max_tournament_tiers),
			
		(else_try),
			# Tournament Score.
			(eq, ":log_type", TPE_LOG_SCORE),
			(troop_get_slot, reg1, TPE_LOG_SCORE, ":entry"),
			
		(else_try),
			# Tournament Earnings.
			(eq, ":log_type", TPE_LOG_EARNINGS),
			(troop_get_slot, reg1, TPE_LOG_EARNINGS, ":entry"),
			
		(else_try),
			### ERROR ### - Invalid log type requested.
			(assign, reg31, ":log_type"),
			(display_message, "@ERROR (TPE Log): Invalid log type requested {reg31} at script_tpe_get_log_data.", gpu_red),
		(try_end),
		
	]),
# END - TOURNAMENT HALL OF RECORD SCRIPTS

# script_tpe_elimination_mode_get_team_sizes
# Receives current tournament tier and returns the desired number of teams and the size of the teams if in elimination mode of play.
("tpe_elimination_mode_get_team_sizes",
    [
		(store_script_param, ":tournament_round", 1),
		
		(try_begin),
			(eq, ":tournament_round", 0),
			(assign, "$g_tournament_next_num_teams", 4),
			(assign, "$g_tournament_next_team_size", 8),
			(troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 24),
		(else_try),
			(eq, ":tournament_round", 1),
			(assign, "$g_tournament_next_num_teams", 4),
			(assign, "$g_tournament_next_team_size", 8),
			(troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 24),
		(else_try),
			(eq, ":tournament_round", 2),
			(assign, "$g_tournament_next_num_teams", 2),
			(assign, "$g_tournament_next_team_size", 8),
			(troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 14),
		(else_try),
			(eq, ":tournament_round", 3),
			(assign, "$g_tournament_next_num_teams", 2),
			(assign, "$g_tournament_next_team_size", 1),
			(troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 1),
		(else_try),
			(eq, ":tournament_round", 4),
			(assign, "$g_tournament_next_num_teams", 2),
			(assign, "$g_tournament_next_team_size", 1),
			(troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 1),
		# (else_try),
			# (eq, ":tournament_round", 4),
			# (assign, "$g_tournament_next_num_teams", 4),
			# (assign, "$g_tournament_next_team_size", 2),
			# (troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 9),
		# (else_try),
			# (eq, ":tournament_round", 5),
			# (assign, "$g_tournament_next_num_teams", 3),
			# (assign, "$g_tournament_next_team_size", 1),
			# (troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 2),
		# (else_try),
			# (eq, ":tournament_round", 6),
			# (assign, "$g_tournament_next_num_teams", 2),
			# (assign, "$g_tournament_next_team_size", 1),
			# (troop_set_slot, TPE_OPTIONS, tpe_val_diff_setting, 1),
		# (else_try),
			# (eq, ":tournament_round", 7),
			# (assign, "$g_tournament_next_num_teams", 2),
			# (assign, "$g_tournament_next_team_size", 1),
		(else_try),
			(assign, reg21, ":tournament_round"),
			(display_message, "@ERROR (TPE): Illegal tournament round #{reg21} attempted.", gpu_red),
			(assign, "$g_tournament_next_num_teams", 2),
			(assign, "$g_tournament_next_team_size", 1),
		(try_end),
		
		(store_mul, "$g_tournament_num_participants_for_fight", "$g_tournament_next_num_teams", "$g_tournament_next_team_size"),
	]),
	
# script_tpe_designate_continuing_participants
# ELIMINATION MODE: Controls the logic of who continues on to the next round.
("tpe_designate_continuing_participants",
    [
		(store_script_param, ":reasoning", 1),
		(store_script_param, ":team_no", 2),
		
		(try_begin),
			### RESET FLAGGING ###
			(eq, ":reasoning", FTC_RESET),
			# Clean out points from the last round.
			(try_for_range, ":slot_no", 0, wp_tpe_max_tournament_participants),
				(troop_get_slot, ":troop_no", tpe_tournament_roster, ":slot_no"),
				(troop_set_slot, ":troop_no", slot_troop_tournament_flag_to_continue, 0),
				(eq, ":troop_no", "trp_player"),
				(str_store_string, s15, "@You have failed to qualify ^for the next round and will ^be eliminated from the ^games."),
			(try_end),
			
		(else_try),
			### FLAG AN ENTIRE TEAM ###
			(eq, ":reasoning", FTC_TEAM),
			(try_for_agents, ":agent_no"),
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				(agent_get_team, ":team_agent", ":agent_no"),
				(eq, ":team_agent", ":team_no"),
				(lt, "$tpe_number_joining", "$g_tournament_num_participants_for_fight"),
				(neg|troop_slot_eq, ":troop_no", slot_troop_tournament_flag_to_continue, 1),
				(troop_set_slot, ":troop_no", slot_troop_tournament_flag_to_continue, 1),
				(val_add, "$tpe_number_joining", 1),
				(try_begin),
					(ge, DEBUG_TPE_general, 1),
					(str_store_troop_name, s31, ":troop_no"),
					(assign, reg31, ":team_agent"),
					(assign, reg32, "$tpe_number_joining"),
					(assign, reg33, "$g_tournament_num_participants_for_fight"),
					(call_script, "script_tpe_color_team_name", ":team_agent"),
					(display_message, "@DEBUG: {s31} is flagged to continue as part of the {s1} ({reg31}).  {reg32}/{reg33}", gpu_debug),
				(try_end),
				(eq, ":troop_no", "trp_player"),
				(str_store_string, s15, "@You have been allowed to ^continue based upon the ^merits of your team.^"),
			(try_end),
			
		(else_try),
			### FILL THE REMAINING SLOTS ###
			(eq, ":reasoning", FTC_FILL_REMAINING),
			(try_for_range, ":slot_no", 0, wp_tpe_max_tournament_participants),
				(troop_get_slot, ":troop_no", tpe_ranking_array, ":slot_no"),
				(lt, "$tpe_number_joining", "$g_tournament_num_participants_for_fight"),
				(neg|troop_slot_eq, ":troop_no", slot_troop_tournament_flag_to_continue, 1),
				(troop_set_slot, ":troop_no", slot_troop_tournament_flag_to_continue, 1),
				(val_add, "$tpe_number_joining", 1),
				(try_begin),
					(ge, DEBUG_TPE_general, 1),
					(str_store_troop_name, s31, ":troop_no"),
					(assign, reg31, ":slot_no"),
					(assign, reg32, "$tpe_number_joining"),
					(assign, reg33, "$g_tournament_num_participants_for_fight"),
					(display_message, "@DEBUG: {s31} is fills a remaining spot since he was rank #{reg31}.  {reg32}/{reg33}", gpu_debug),
				(try_end),
				(eq, ":troop_no", "trp_player"),
				(str_store_string, s15, "@You have been allowed ^to continue based upon ^your personal performance.^"),
			(try_end),
			
		(try_end),
	]),
	
]


from util_wrappers import *
from util_scripts import *

scripts_directives = [
	#rename scripts to "insert" switch scripts (see end of scripts[])  
	#[SD_RENAME, "end_tournament_fight" , "orig_end_tournament_fight"], 
	#[SD_RENAME, "fill_tournament_participants_troop" , "orig_fill_tournament_participants_troop"],
	#[SD_RENAME, "get_random_tournament_participant" , "orig_get_random_tournament_participant"],
	#[SD_RENAME, "set_items_for_tournament" , "orig_set_items_for_tournament"], 
	# Puts in exception to companions being upset over failing to acknowledge a tournament invitation quest.
	[SD_OP_BLOCK_INSERT, "abort_quest", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (call_script, "script_objectionable_action", tmt_honest, "str_fail_quest"), 0, 
		[(neq, ":quest_no", "qst_floris_active_tournament"),], 1],
	[SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_LINENUMBER | D_INSERT_BEFORE, 0, 0, 
		[(call_script, "script_tpe_initialize_player_settings"),], 1],
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