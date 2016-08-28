# Killer Regeneration (1.11) by Windyplains
# Released 10/5/2011

# WHAT THIS FILE DOES:
# Adds "combat_enhancement_triggers" to every mission template with mtf_battle_mode to enable health regeneration on killing.

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *

combat_enhancement_triggers = [  

## TRIGGER: TROOP RATIO BAR
## PURPOSE: Displays a scaling slider to show how many allies & enemies are left on the battlefield.
(0.1, 0, 0, [],  # (neq, "$g_mt_mode", abm_tournament),
	[
		# (try_for_range, ":presentation_no", "prsnt_game_credits", "prsnt_hub_quests"),
			# (is_presentation_active, ":presentation_no"),
			# (assign, reg21, ":presentation_no"),
			# (display_message, "@DEBUG (minimap): Presentation ID# {reg21} is active.", gpu_red),
		# (try_end),
		(neg|is_presentation_active, "prsnt_troop_ratio_bar"),
		(neg|is_presentation_active, "prsnt_battle"),
		(store_cur_mission_template_no, ":mission_no"), # WSE
		(neq, ":mission_no", "mt_arena_melee_fight"), # Arena fights to prevent the map from showing up there or while talking to the arena master.
		(neq, ":mission_no", "mt_tpe_tournament_native_gear"), # Tournament fights should be excluded.
		(neq, ":mission_no", "mt_tpe_tournament_standard"), # Tournament fights should be excluded.
		(neq, ":mission_no", "mt_visit_town_castle"), # Don't display this when visiting court.
		(this_or_next|neq, ":mission_no", "mt_town_center"), # Don't display this when walking around in a town.
		(eq, "$talk_context", tc_prison_break), # Allow this to show up on prison breaks.
		(neq, ":mission_no", "mt_village_center"), # Don't display this when walking around in a village.
		(this_or_next|eq, "$enable_troop_ratio_bar", 1),
		(eq, "$enable_battle_minimap", 1),
		(start_presentation, "prsnt_troop_ratio_bar"),
	]),
	
# # TRIGGER: This trigger tries to capture an attempt to change screens to prevent log spam on the ICD presentation.
	# (0, 0, 0, 
		# [
			# (eq, "$enable_sprinting", 1),
			# # (neq, ":mission_no", "mt_arena_melee_fight"), # Arena fights to prevent the map from showing up there or while talking to the arena master.
			# # Prevent this from triggering in tournaments since there the ICD triggers cover this.
			# (store_cur_mission_template_no, ":mission_no"), # WSE
			# (neq, ":mission_no", "mt_tpe_tournament_native_gear"), # Tournament fights should be excluded.
			# (neq, ":mission_no", "mt_tpe_tournament_standard"), # Tournament fights should be excluded.
			# (this_or_next|game_key_clicked, gk_game_log_window),
			# (this_or_next|game_key_clicked, gk_quests_window),
			# (this_or_next|game_key_clicked, gk_character_window),
			# (this_or_next|game_key_clicked, gk_leave),
			# (game_key_clicked, key_escape),
			# (neg|key_clicked, key_s), # Beats me why 's' is triggering this at all.
		# ],
	    # [
			# (assign, "$block_stamina_bar", 1),
			# (assign, "$obj_stamina_bar", -1),
			# (try_begin),
				# (ge, DEBUG_STAMINA, 1),
				# (display_message, "@DEBUG (Stamina): A GAMEKEY WAS CLICKED THAT CAUSED THE STAMINA BAR TO DISABLE!!!!"),
				# (assign, reg31, "$block_stamina_bar"),
				# (display_message, "@DEBUG (Stamina): Stamina bar has been {reg31?BLOCKED:unblocked} @ escape_trigger (combat)", gpu_debug), ## DEBUG: STAMINA_BAR
			# (try_end),
		# ]),
		
# TRIGGER: This trigger tries to capture an attempt to change screens to prevent log spam on the ICD presentation.
	(0, 0, 0, 
		[],
	    [
			(get_player_agent_no, ":agent_player"),
			(key_clicked, key_j),
			(try_begin),
				(eq, reg63, 0),
				(agent_set_reload_speed_modifier, ":agent_player", 150),
				(display_message, "@DEBUG: Player reload speed set to 150%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 1),
				(agent_set_reload_speed_modifier, ":agent_player", 200),
				(display_message, "@DEBUG: Player reload speed set to 200%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 2),
				(agent_set_reload_speed_modifier, ":agent_player", 300),
				(display_message, "@DEBUG: Player reload speed set to 300%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 3),
				(agent_set_reload_speed_modifier, ":agent_player", 400),
				(display_message, "@DEBUG: Player reload speed set to 400%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 4),
				(agent_set_reload_speed_modifier, ":agent_player", 500),
				(display_message, "@DEBUG: Player reload speed set to 500%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 5),
				(agent_set_reload_speed_modifier, ":agent_player", 600),
				(display_message, "@DEBUG: Player reload speed set to 600%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 6),
				(agent_set_reload_speed_modifier, ":agent_player", 700),
				(display_message, "@DEBUG: Player reload speed set to 700%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 7),
				(agent_set_reload_speed_modifier, ":agent_player", 800),
				(display_message, "@DEBUG: Player reload speed set to 800%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 8),
				(agent_set_reload_speed_modifier, ":agent_player", 900),
				(display_message, "@DEBUG: Player reload speed set to 900%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(eq, reg63, 9),
				(agent_set_reload_speed_modifier, ":agent_player", 1000),
				(display_message, "@DEBUG: Player reload speed set to 1000%.", gpu_debug),
				(val_add, reg63, 1),
			(else_try),
				(agent_set_reload_speed_modifier, ":agent_player", 100),
				(display_message, "@DEBUG: Player reload speed RESET to 100%.", gpu_debug),
				(assign, reg63, 0),
			(try_end),
		]),
		
# TRIGGER: This trigger tries to capture an attempt to change screens to prevent log spam on the ICD presentation.
	(0, 0, 0, 
		[
			(eq, "$enable_sprinting", 1),
			# Prevent this from triggering in tournaments since there the ICD triggers cover this.
			(store_cur_mission_template_no, ":mission_no"), # WSE
			(neq, ":mission_no", "mt_tpe_tournament_native_gear"), # Tournament fights should be excluded.
			(neq, ":mission_no", "mt_tpe_tournament_standard"), # Tournament fights should be excluded.
		],
	    [
			
			(neg|is_presentation_active, "prsnt_troop_ratio_bar"),
			(neg|is_presentation_active, "prsnt_battle"),
			(assign, "$block_stamina_bar", 1),
			(assign, "$obj_stamina_bar", -1),
			(try_begin),
				(ge, DEBUG_STAMINA, 1),
				(assign, reg31, "$block_stamina_bar"),
				(display_message, "@DEBUG (Stamina): Stamina bar has been {reg31?BLOCKED:unblocked} @ catch-all (combat)", gpu_debug), ## DEBUG: STAMINA_BAR
			(try_end),
		]),
	
## TRIGGER: HEALTH REGENERATION
## PURPOSE: Restores a % of health to player and AI based upon downing an enemy combatant.
(ti_on_agent_killed_or_wounded, 0, 0, [(neq, "$killer_regen_mode", 0),],
    [
		(store_trigger_param_1, ":agent_victim"),
		(store_trigger_param_2, ":agent_killer"),
      
		# Is this a valid kill worth gaining morale?
		(agent_is_human, ":agent_victim"),
	    (agent_is_active, ":agent_killer"), # Prevent possible script errors.
		
		# Determine health amount to regenerate
		(try_begin), # Is it the player?
			(get_player_agent_no, ":agent_player"),
			(eq, ":agent_killer", ":agent_player"),
			(assign, ":health_regeneration", wp_hr_player_rate),
		(else_try), # Is it a companion?
			(is_between, ":agent_killer", companions_begin, companions_end),
			(assign, ":health_regeneration", wp_hr_companion_rate),
		(else_try), # Is it a lord?
			(is_between, ":agent_killer", lords_begin, lords_end),
			(assign, ":health_regeneration", wp_hr_lord_rate),
		(else_try), # Is it a king?
			(is_between, ":agent_killer", kings_begin, kings_end),
			(assign, ":health_regeneration", wp_hr_king_rate),
		(else_try), # This should catch all common soldiers, horses, etc.
			# This section commented out because it is designed for use with "elite units" which most mods do not use.
			# (try_begin),  
				# (agent_get_troop_id, ":troop_no", ":agent_killer"), # Is this an elite unit?
				# (troop_slot_eq, ":troop_no", slot_troop_is_elite, 1),
				# (assign, ":health_regeneration", wp_hr_elite_rate),
			# (else_try),
				# (assign, ":health_regeneration", wp_hr_common_rate),
			# (try_end),
			(assign, ":health_regeneration", wp_hr_common_rate),
			# This adds a small bonus to all non-heroes based on the leadership of their owner.
			(agent_get_team, ":team_killer", ":agent_killer"),
			(team_get_leader, ":agent_leader", ":team_killer"),
			(ge, ":agent_leader", 0), # Prevent -1 invalid agent spam in the event a leader is unavailable.
			(agent_get_troop_id, ":troop_leader", ":agent_leader"),
			(store_skill_level, ":leadership", "skl_leadership", ":troop_leader"),
			(assign, reg4, ":leadership"), # stored for debug display purposes.
			(val_div, ":leadership", wp_hr_leadership_factor),
			(val_add, ":health_regeneration", ":leadership"),
		(try_end),
	  
		# Adds in Strength as a bonus or penalty.  (STR - 10) / wp_hr_strength_factor
		(agent_get_troop_id, ":troop_killer", ":agent_killer"),
		(store_attribute_level, ":strength", ":troop_killer", ca_strength),
		(val_sub, ":strength", 10),
		(val_div, ":strength", wp_hr_strength_factor),
		(val_add, ":health_regeneration", ":strength"),
	  
		# Changes health regeneration based on this factor.
		(try_begin),
			(eq, wp_hr_factor_difficulty, 1),  # Is this difficulty script even being used.
			(assign, ":bonus_difficulty", "$mod_difficulty"),
			(try_begin),
				(agent_is_ally, ":agent_killer"),
				(val_mul, ":bonus_difficulty", wp_hr_diff_ally_penalty),
			(else_try),
				(val_mul, ":bonus_difficulty", wp_hr_diff_enemy_bonus),
			(try_end),
			(val_add, ":health_regeneration", ":bonus_difficulty"),
		(try_end),
		
		## Troop Ability: BONUS_HARDY
		(assign, ":bonus_abilities", 0),
		(try_begin),
			(eq, "$enable_combat_abilities", 1),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_killer", BONUS_HARDY),
			(store_skill_level, ":ironflesh_bonus", "skl_ironflesh", ":troop_killer"),
			(try_begin),
				(troop_is_hero, ":troop_killer"),
				(val_div, ":ironflesh_bonus", 2),
			(try_end),
			(val_add, ":bonus_abilities", ":ironflesh_bonus"),
			# (try_begin),  ### DIAGNOSTIC+ ###
				# (ge, DEBUG_TROOP_ABILITIES, 1),
				# (call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_killer", BONUS_HARDY),
				# (str_store_troop_name, s32, ":troop_killer"),
				# (assign, reg31, ":ironflesh_bonus"),
				# (display_message, "@DEBUG: {s32} has the '{s31}' bonus so gains +{reg31}% to health regen.", gpu_green),
			# (try_end), ### DIAGNOSTIC- ###
		(try_end),
		
		## Nearby Troop Ability: BONUS_COMMANDING_PRESENCE
		(try_begin),
			(eq, "$enable_combat_abilities", 1),
			# (eq, ":troop_killer", "trp_player"), ## limited to player for testing.
			(agent_get_position, pos1, ":agent_killer"),
			#(set_fixed_point_multiplier, 1000),
			(try_for_agents, ":nearby_agent", pos1, 5000),
				(neq, ":nearby_agent", ":agent_killer"),
				(neq, ":nearby_agent", ":agent_victim"),
				(agent_is_alive, ":nearby_agent"),
				(agent_is_human, ":nearby_agent"),
				(agent_get_team, ":nearby_agent_team", ":nearby_agent"),
				(agent_get_team, ":team_killer", ":agent_killer"),
				(eq, ":team_killer", ":nearby_agent_team"),
				(agent_get_troop_id, ":nearby_troop", ":nearby_agent"),
				(call_script, "script_cf_ce_troop_has_ability", ":nearby_troop", BONUS_COMMANDING_PRESENCE),
				(store_skill_level, ":presence_bonus", "skl_leadership", ":nearby_troop"),
				(val_div, ":presence_bonus", 2),
				(val_add, ":presence_bonus", 2),
				(val_add, ":bonus_abilities", ":presence_bonus"),
				# (try_begin),  ### DIAGNOSTIC+ ###
					# (ge, DEBUG_TROOP_ABILITIES, 1),
					# (call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_killer", BONUS_COMMANDING_PRESENCE),
					# (str_store_troop_name, s33, ":nearby_troop"),
					# (str_store_troop_name, s32, ":troop_killer"),
					# (assign, reg31, ":presence_bonus"),
					# (display_message, "@DEBUG: {s33} has '{s31}' and raises {s32}'s health regen by {reg31}.", gpu_green),
				# (try_end),  ### DIAGNOSTIC- ###
				(break_loop),
			(try_end),
			
		(try_end),
		(val_add, ":health_regeneration", ":bonus_abilities"),
		
		(val_max, ":health_regeneration", 0), # We don't want a negative health regeneration.
	  
		# Remove regeneration value if option not enabled for this unit type.
		(try_begin),  # Check if this is the player and regeneration is disabled.
			(neq, ":agent_killer", ":agent_player"),
			(this_or_next|eq, "$killer_regen_mode", 1), # Player Only
			(eq, "$killer_regen_mode", 0), # Disabled
			(assign, ":health_regeneration", 0),
			(assign, ":disable_debug", 1),
		(else_try),   # If not player assume AI troop and check if AI regen is disabled.
			(eq, ":agent_killer", ":agent_player"),  # To prevent player enabled, AI disabled conflicts.
			(this_or_next|eq, "$killer_regen_mode", 2), # AI Only
			(eq, "$killer_regen_mode", 0), # Disabled
			(assign, ":health_regeneration", 0),
			(assign, ":disable_debug", 1),
		(else_try),
			(assign, ":disable_debug", 0),
		(try_end),
	  
		# Displays debug messages if turned on.
		(try_begin), 
			(eq, DEBUG_COMBAT, 1),
			(this_or_next|eq, ":troop_killer", "trp_player"),
			(eq, DEBUG_COMBAT, 2),
			(eq, ":disable_debug", 0),
			(str_store_troop_name, s1, ":troop_killer"),
			(assign, reg0, ":health_regeneration"),
			(assign, reg1, ":strength"),
			(try_begin), (ge, ":leadership", 10), (assign, ":leadership", -1), (try_end), # If no leadership bonus exists put in a default value.
			(assign, reg2, ":leadership"),
			(display_message, "@DEBUG (Health Regen): Agent leadership skill is {reg4}."),
			(try_begin), (eq, wp_hr_factor_difficulty, 1),(assign, reg3, ":bonus_difficulty"), (else_try), (assign, reg3, 0), (try_end),  # Get difficulty bonus OR use 0.
			(assign, reg5, ":bonus_abilities"),
			(display_message, "@DEBUG (Health Regen): {s1} regains {reg0}% health.  = +{reg1}% STR +{reg2}% Lead + {reg3}% Diff + {reg5}% Abilities."),
		(try_end),
	  
		# Regenerates the given health amount.
		(ge, ":health_regeneration", 1),
		(store_agent_hit_points, ":current_health", ":agent_killer", 0),
		(val_add, ":current_health", ":health_regeneration"),
		(agent_set_hit_points, ":agent_killer", ":current_health", 0),
    ]),

## TRIGGER: BONUS EXPERIENCE FOR INTELLIGENCE
## PURPOSE: Grants extra experience for killing opponents if you have a high intelligence.
(ti_on_agent_killed_or_wounded, 0, 0, [],
    [
		(store_trigger_param_1, ":agent_victim"),
		(store_trigger_param_2, ":agent_killer"),
		
		(agent_is_active, ":agent_killer"),
		# Should agent get this benefit?
		(agent_is_human, ":agent_killer"),
		(agent_is_human, ":agent_victim"),
		(agent_get_troop_id, ":troop_killer", ":agent_killer"),
		(agent_get_troop_id, ":troop_victim", ":agent_victim"),
		(troop_is_hero, ":troop_killer"),
		
		# Prevent gaining experience due to falling from your own horse.
		(assign, ":continue", 1),
		(try_begin),
			(eq, "$enable_fallen_riders", 1),
			(agent_get_slot, ":agent_rider", ":agent_victim", slot_agent_rider_agent),
			(ge, ":agent_rider", 0),
			(eq, ":agent_killer", ":agent_rider"),
			(assign, ":continue", 0),
		(try_end),
		(eq, ":continue", 1),
		
		(try_begin),
			(store_character_level, ":level_victim", ":troop_victim"),
			(store_attribute_level, ":intelligence_killer", ":troop_killer", ca_intelligence),
			(val_sub, ":intelligence_killer", 10),
			(ge, ":intelligence_killer", 2),
			(val_div, ":intelligence_killer", 2),
			(store_mul, ":xp_value", ":level_victim", ":intelligence_killer"),
			# Limit benefit during tournaments.
			(try_begin),
				(store_cur_mission_template_no, ":mission_template"),
				(this_or_next|eq, ":mission_template", "mt_tpe_tournament_standard"),
				(this_or_next|eq, ":mission_template", "mt_arena_melee_fight"),
				(eq, ":mission_template", "mt_tpe_tournament_native_gear"),
				(val_min, ":xp_value", 50),
			(else_try), # Limit to 25xp at the training grounds.
				(store_cur_mission_template_no, ":mission_template"),
				(this_or_next|eq, ":mission_template", "mt_training_ground_training"),
				(eq, ":mission_template", "mt_training_ground_trainer_training"),
				(val_min, ":xp_value", 25),
			(else_try),
				## DEFAULT BALANCING - Limit maximum gain without Savant to 300.  (Equivalent level 30 enemy with 30 INT)
				(val_min, ":xp_value", 300),
			(try_end),
			
			### TROOP EFFECT: SAVANT ###
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_killer", BONUS_SAVANT),
				(store_div, ":savant_bonus", ":xp_value", 2),
				(val_add, ":xp_value", ":savant_bonus"),
				(val_min, ":xp_value", 450),
				(try_begin),
					(ge, DEBUG_TROOP_ABILITIES, 1),
					(assign, reg31, ":savant_bonus"),
					(display_message, "@You receive +{reg31}xp due to your SAVANT bonus. (Included)", gpu_debug),
				(try_end),
			(try_end),
			
			(set_show_messages, 0),
			(add_xp_to_troop, ":xp_value", ":troop_killer"),
			(set_show_messages, 1),
			(eq, ":troop_killer", "trp_player"),
			(eq, "$display_extra_xp_prof", 1),
			(assign, reg21, ":xp_value"),
			(display_message, "@You receive +{reg21} extra experience because of your intelligence.", 0xFFFFFFAA),
		(try_end),
		
		# (try_begin),
			# (store_skill_level, ":skill_weapon_master", "skl_weapon_master", ":troop_killer"),
			# (val_mul, ":skill_weapon_master", 3),
			# (store_random_in_range, ":roll", 0, 100),
			# (lt, ":roll", ":skill_weapon_master"),
			# (agent_get_wielded_item, ":item_no", ":agent_killer", 0),
			# (ge, ":item_no", 1),
			# (item_get_type, ":item_type", ":item_no"),
			# (assign, ":continue", 0),
			# (str_clear, s21),
			# (try_begin),
				# (eq, ":item_type", itp_type_one_handed_wpn),
				# (assign, ":prof_type", wpt_one_handed_weapon),
				# (str_store_string, s21, "@One Handed Weapons"),
				# (assign, ":continue", 1),
			# (else_try),
				# (eq, ":item_type", itp_type_two_handed_wpn),
				# (assign, ":prof_type", wpt_two_handed_weapon),
				# (str_store_string, s21, "@Two Handed Weapons"),
				# (assign, ":continue", 1),
			# (else_try),
				# (eq, ":item_type", itp_type_polearm),
				# (assign, ":prof_type", wpt_polearm),
				# (str_store_string, s21, "@Polearms"),
				# (assign, ":continue", 1),
			# (else_try),
				# (eq, ":item_type", itp_type_bow),
				# (assign, ":prof_type", wpt_archery),
				# (str_store_string, s21, "@Archery"),
				# (assign, ":continue", 1),
			# (else_try),
				# (eq, ":item_type", itp_type_crossbow),
				# (assign, ":prof_type", wpt_crossbow),
				# (str_store_string, s21, "@Crossbows"),
				# (assign, ":continue", 1),
			# (else_try),
				# (eq, ":item_type", itp_type_thrown),
				# (assign, ":prof_type", wpt_throwing),
				# (str_store_string, s21, "@Throwing Weapons"),
				# (assign, ":continue", 1),
			# (try_end),
			# (store_proficiency_level, ":prof", ":troop_killer", ":prof_type"),
			# (store_skill_level, ":prof_cutoff", "skl_weapon_master", ":troop_killer"),
			# (val_mul, ":prof_cutoff", 30), 
			# (val_add, ":prof_cutoff", 90), # WM cutoffs 120, 150, 180, 210, 240, 270, 300, 330, 360, 390
			# (lt, ":prof", ":prof_cutoff"),
			# (eq, ":continue", 1),
			# (val_add, ":prof", 1),
			# (troop_set_proficiency, ":troop_killer", ":prof_type", ":prof"),
			# (eq, ":troop_killer", "trp_player"),
			# (eq, "$display_extra_xp_prof", 1),
			# (assign, reg21, ":prof"),
			# (display_message, "@You have improved your proficiency in {s21} to {reg21}.", 0xFFFFFFAA),
		# (try_end),
	]),
	
## TRIGGER: BONUS_SECOND_WIND EFFECT
## PURPOSE: Immediately resets sprinting cooldown upon defeating an enemy.
(ti_on_agent_killed_or_wounded, 0, 0, 
	[
		(eq, "$enable_sprinting", 1),
	],
    [
		(store_trigger_param_1, ":agent_victim"),
		(store_trigger_param_2, ":agent_killer"),
		
		# Should agent get this benefit?
		(agent_is_active, ":agent_killer"),
		(agent_is_human, ":agent_killer"),
		(agent_is_human, ":agent_victim"),
		(agent_get_troop_id, ":troop_killer", ":agent_killer"),
		(call_script, "script_cf_ce_troop_has_ability", ":troop_killer", BONUS_SECOND_WIND),
		(agent_get_slot, ":stamina", ":agent_killer", slot_agent_current_stamina),
		(agent_get_slot, ":max_stamina", ":agent_killer", slot_agent_max_stamina),
		(val_add, ":stamina", 1500),
		(val_min, ":stamina", ":max_stamina"),
		(agent_set_slot, ":agent_killer", slot_agent_current_stamina, ":stamina"),
		(agent_set_slot, ":agent_killer", slot_agent_sprint_cooldown, 0),
	]),
	
## TRIGGER: STAMINA BAR INITIALIZATION
(ti_before_mission_start, 0, 0, 
	[],
	[
		(assign, "$obj_stamina_bar", -1),
		(assign, "$block_stamina_bar", 1),
		(try_begin), ### DIAGNOSTIC+ ###
			(ge, DEBUG_STAMINA, 1),
			(assign, reg31, "$block_stamina_bar"),
			(display_message, "@DEBUG (Stamina): Stamina bar has been {reg31?BLOCKED:unblocked} @ trigger_mission_start (combat)", gpu_debug), ## DEBUG: STAMINA_BAR
		(try_end), ### DIAGNOSTIC- ###
	]),
	
## TRIGGER: STAMINA_BAR UPDATES - PLAYER
## PURPOSE: Handles the stamina loss or recovery rate of each agent.
## PURPOSE: Reboots the stamina bar if it is disabled due to a screen change.
## PURPOSE: Updates the stamina bar.
(1, 0, 0, 
	[(eq, "$enable_sprinting", 1),],
    [
		# (store_trigger_param_1, ":agent_no"),
		
		(get_player_agent_no, ":agent_player"),
		
		## PURPOSE: Handles the stamina loss or recovery rate of each agent.
		(try_for_agents, ":agent_no"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(try_begin),
				## CASE - CURRENTLY SPRINTING
				(this_or_next|key_is_down, "$key_special_sprint"),
				(neg|eq, ":agent_no", ":agent_player"),
				(agent_slot_ge, ":agent_no", slot_agent_sprint_timer, 1),
				# Ability (BONUS_SPRINTER)
				(assign, ":sprinter_penalty", 0),
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SPRINTER),
					(assign, ":sprinter_penalty", 50),
				(try_end),
				(agent_get_slot, ":stamina", ":agent_no", slot_agent_current_stamina),
				(val_sub, ":stamina", 200),
				(val_sub, ":stamina", ":sprinter_penalty"),
				(val_max, ":stamina", 0),
				(agent_set_slot, ":agent_no", slot_agent_current_stamina, ":stamina"),
			(else_try),
				## CASE - NOT SPRINTING, RECOVER STAMINA
				(agent_slot_eq, ":agent_no", slot_agent_sprint_cooldown, 0),
				(store_skill_level, ":athletics_bonus", "skl_athletics", ":troop_no"),
				(val_mul, ":athletics_bonus", 5),
				(agent_get_slot, ":stamina", ":agent_no", slot_agent_current_stamina),
				(agent_get_slot, ":max_stamina", ":agent_no", slot_agent_max_stamina),
				(val_add, ":stamina", 25),
				(val_add, ":stamina", ":athletics_bonus"),
				(val_min, ":stamina", ":max_stamina"),
				(agent_set_slot, ":agent_no", slot_agent_current_stamina, ":stamina"),
			(try_end),
		(try_end),
		
		### DIAGNOSTIC+ ###
		(try_begin),
			(ge, DEBUG_STAMINA, 1),
			(agent_get_slot, ":current_stamina", ":agent_no", slot_agent_current_stamina),
			(agent_get_slot, ":max_stamina", ":agent_no", slot_agent_max_stamina),
			(store_div, reg31, ":current_stamina", 100),
			(store_mod, reg35, ":current_stamina", 100),
			(store_div, reg32, ":max_stamina", 100),
			(this_or_next|is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_champions_end), # Limit Debug Flow ge, DEBUG_STAMINA, 2),
			(eq, ":agent_no", ":agent_player"),
			
			(neq, ":current_stamina", ":max_stamina"),
			(display_message, "@DEBUG (Stamina): Stamina ({reg31}.{reg35}/{reg32}.00)", gpu_debug),
		(try_end),
		### DIAGNOSTIC- ###
		
		## PURPOSE: Reboots the stamina bar if it is disabled due to a screen change.
		(try_begin),
			(eq, "$enable_sprinting", 1),  # Without sprinting the stamina bar doesn't belong.
			(eq, "$block_stamina_bar", 1), # Already disabled, so reboot it.
			(call_script, "script_cf_ce_stamina_bar_has_background_presentation"), # combat_scripts.py
			(call_script, "script_ce_draw_stamina_bar"),
		(try_end),
		
		## PURPOSE: Updates the stamina bar.
		(call_script, "script_ce_update_stamina_bar", ":agent_player"),
	]),
	
## TRIGGER: COMBAT SPRINTING - PLAYER
## PURPOSE: Handles everything associated with combat sprinting for the player.
(0.1, 0, 0, 
	[(eq, "$enable_sprinting", 1),],
	[
		# slot_agent_sprint_timer                  = 45
		# slot_agent_sprint_cooldown               = 46
		(get_player_agent_no, ":agent_no"),
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		(store_attribute_level, ":agility", ":troop_no", ca_agility),
		(store_skill_level, ":athletics", "skl_athletics", ":troop_no"),
		(assign, ":maximum_cooldown", 80),
		(store_mul, ":speed_athletics", ":athletics", 3),
		(store_add, ":sprint_speed", ":agility", ":speed_athletics"),
		(call_script, "script_ce_get_troop_base_movement_speed", ":troop_no", SPEED_FACTOR_AGILITY),
		(val_add, ":sprint_speed", reg1), # This adds the base 100% (modified by agility)
		(val_add, ":sprint_speed", 130), # Ideally this should make us between 134-190%
		## TROOP ABILITIES - SPRINTER, ENDURANCE, BOUNDLESS ENDURANCE
		(assign, ":speed_factor", 0),
		(assign, ":speed_max", 180),
		(try_begin),
			(eq, "$enable_combat_abilities", 1),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SPRINTER),
			## +50% speed & +30% maximum speed
			(val_add, ":speed_factor", 50),
			(val_add, ":speed_max", 30),
		(else_try),
			(eq, "$enable_combat_abilities", 1),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_ENDURANCE),
			## -25% speed
			(val_add, ":speed_factor", 0),
			(val_add, ":speed_max", -20),
			## -3 seconds to cooldown
			(val_sub, ":maximum_cooldown", 30),
		(else_try),
			(eq, "$enable_combat_abilities", 1),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BOUNDLESS_ENDURANCE),
			## +50% speed
			(val_add, ":speed_factor", 25),
			(val_add, ":speed_max", 0),
		(try_end),
		## Adjust sprinting speed.
		(store_sub, ":base_sprint", ":sprint_speed", 100),
		(val_add, ":speed_factor", 100),
		(store_mul, ":speed_after_abilities", ":speed_factor", ":base_sprint"),
		(val_div, ":speed_after_abilities", 100),
		(store_add, ":sprint_speed", 100, ":speed_after_abilities"),
		(assign, reg31, ":sprint_speed"),
		(val_min, ":sprint_speed", ":speed_max"), # maximum speed.
		### DIAGNOSTIC+ ### - Testing ability boosts and sprint speeds.
		# (try_begin),
			# (key_is_down, "$key_special_sprint"),
			# (assign, reg32, ":base_sprint"),
			# (assign, reg33, ":speed_factor"),
			# (assign, reg34, ":speed_after_abilities"),
			# (assign, reg35, ":sprint_speed"),
			# (display_message, "@DEBUG (sprint): Player sprinting.  base {reg32}, factor {reg33}, speed after abilities {reg34}, raw {reg31}, capped {reg35}.", gpu_debug),
		# (try_end),
		### DIAGNOSTIC- ###
		## Add in speed changes from the combat hampering system.
		(try_begin),
			(eq, "$combat_hampering_enabled", 1),
			(agent_get_slot, ":modified_speed", ":agent_no", slot_agent_last_calculated_speed),
			(store_sub, ":speed_penalty", 100, ":modified_speed"),
			(val_sub, ":sprint_speed", ":speed_penalty"),
		(try_end),
		## TROOP ABILITY - CHARGING STRIKE - Data collection
		(try_begin),
			(agent_set_slot, ":agent_no", slot_agent_sprint_speed, ":sprint_speed"),
		(try_end),
		
		(try_begin),
			## START SPRINTING ##
			(key_is_down, "$key_special_sprint"),
			(agent_get_horse, ":horse", ":agent_no"),
			(agent_slot_ge, ":agent_no", slot_agent_current_stamina, 1),
			(eq, ":horse", -1),
			# (agent_slot_eq, ":agent_no", slot_agent_sprint_cooldown, 0),
			# Display output.
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg1, ":sprint_speed"),
				(str_store_string, s31, "@ at {reg1}% speed"),
			(else_try),
				(str_clear, s31),
			(try_end),
			(agent_set_speed_modifier, ":agent_no", ":sprint_speed"),
			(store_mission_timer_c, ":timer"),
			(agent_set_slot, ":agent_no", slot_agent_sprint_timer, ":timer"), # "$g_wp_tpe_timer"),
			(agent_slot_eq, ":agent_no", slot_agent_sprint_cooldown, 0),  # Sprint can be activated repeatedly now, but endless war cries are annoying.
			(agent_set_slot, ":agent_no", slot_agent_sprint_cooldown, 1), # Done to prevent this block from repeating.
			(display_message, "@You have started sprinting{s31}.", gpu_debug),
			(troop_get_type, ":gender", ":troop_no"),
			(try_begin),
				(eq, ":gender", 0),
				(agent_play_sound, ":agent_no", "snd_man_warcry"),
			(else_try),
				(agent_play_sound, ":agent_no", "snd_woman_yell"),
			(try_end),
			(assign, reg63, 666), # Done to prevent seeing the normal speed message upon mission loading.
		(else_try),
			## STOP SPRINTING DUE TO RUNNING OUT OF STAMINA ##
			(agent_slot_ge, ":agent_no", slot_agent_sprint_timer, 1),
			(neg|agent_slot_ge, ":agent_no", slot_agent_current_stamina, 1),
			(agent_set_slot, ":agent_no", slot_agent_sprint_timer, 0),
			(agent_set_slot, ":agent_no", slot_agent_sprint_speed, 0),
			# Figure out our cooldown.
			(assign, ":cooldown", 80),
			(val_min, ":cooldown", ":maximum_cooldown"),
			(agent_set_slot, ":agent_no", slot_agent_sprint_cooldown, ":cooldown"),
			# Determine base speed with agility boost.
			(store_attribute_level, ":base_speed", ":troop_no", ca_agility),
			(val_add, ":base_speed", 90),
			## Add in speed changes from the combat hampering system.  Use whichever is lower.
			(try_begin),
				(eq, "$combat_hampering_enabled", 1),
				(agent_get_slot, ":modified_speed", ":agent_no", slot_agent_last_calculated_speed),
				(val_min, ":base_speed", ":modified_speed"),
			(try_end),
			(agent_set_speed_modifier, ":agent_no", ":base_speed"),
			# Display output.
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg1, ":base_speed"),
				(store_div, reg2, ":cooldown", 10),
				(store_mod, reg3, ":cooldown", 10),
				(str_store_string, s31, "@  Speed {reg1}% for {reg2}.{reg3} sec"),
			(else_try),
				(str_clear, s31),
			(try_end),
			(display_message, "@You have stopped sprinting due to tiring out.{s31}", gpu_red),
		(else_try),
			## STOP SPRINTING DUE TO RELEASING CNTL BUTTON ##
			(neg|key_is_down, "$key_special_sprint"),
			(agent_slot_ge, ":agent_no", slot_agent_sprint_timer, 1),
			# Reset our sprint timer.
			# (agent_get_slot, ":sprint_start", ":agent_no", slot_agent_sprint_timer),
			(agent_set_slot, ":agent_no", slot_agent_sprint_timer, 0),
			(agent_set_slot, ":agent_no", slot_agent_sprint_speed, 0),
			# Figure out our cooldown.
			(assign, ":cooldown", 80),
			(val_min, ":cooldown", ":maximum_cooldown"),
			(agent_set_slot, ":agent_no", slot_agent_sprint_cooldown, ":cooldown"),
			# Determine base speed with agility boost.
			(store_attribute_level, ":base_speed", ":troop_no", ca_agility),
			(val_add, ":base_speed", 90),
			## Add in speed changes from the combat hampering system.  Use whichever is lower.
			(try_begin),
				(eq, "$combat_hampering_enabled", 1),
				(agent_get_slot, ":modified_speed", ":agent_no", slot_agent_last_calculated_speed),
				(val_min, ":base_speed", ":modified_speed"),
			(try_end),
			(agent_set_speed_modifier, ":agent_no", ":base_speed"),
		(else_try),
			## COOLDOWN REDUCTION ##
			(neg|key_is_down, "$key_special_sprint"),
			(agent_slot_eq, ":agent_no", slot_agent_sprint_timer, 0),
			(agent_slot_ge, ":agent_no", slot_agent_sprint_cooldown, 1),
			(agent_get_slot, ":cooldown", ":agent_no", slot_agent_sprint_cooldown),
			(val_sub, ":cooldown", 1),
			(agent_set_slot, ":agent_no", slot_agent_sprint_cooldown, ":cooldown"),
		(else_try),
			## RESTORE NORMAL SPEED ##
			(eq, reg63, 666), # Done to prevent seeing the normal speed message upon mission loading.
			(agent_slot_eq, ":agent_no", slot_agent_sprint_timer, 0),
			(agent_slot_eq, ":agent_no", slot_agent_sprint_cooldown, 0),
			(agent_get_slot, ":modified_speed", ":agent_no", slot_agent_last_calculated_speed),
			(agent_set_speed_modifier, ":agent_no", ":modified_speed"),
			# (display_message, "@You have recovered your normal speed.", gpu_green),
			(agent_set_slot, ":agent_no", slot_agent_sprint_timer, -1), # So we don't keep seeing that our speed is normal again.
			(assign, reg63, 0), # Done to prevent seeing the normal speed message upon mission loading.
		(try_end),
	]),

## TRIGGER: COMBAT SPRINTING - AI
## PURPOSE: Handles everything associated with combat sprinting for every other troop.  This is done separately to reduce processor load and
##          because logic is required since the AI won't be using gamekeys to control their sprinting.
(1, 0, 0, 
	[(eq, "$enable_sprinting", 1),],
	[
		(try_for_agents, ":agent_no"),
			(get_player_agent_no, ":agent_player"),
			(neq, ":agent_no", ":agent_player"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(store_attribute_level, ":agility", ":troop_no", ca_agility),
			(store_skill_level, ":athletics", "skl_athletics", ":troop_no"),
			(assign, ":maximum_cooldown", 8),
			(store_mul, ":speed_athletics", ":athletics", 3),
			(store_add, ":sprint_speed", ":agility", ":speed_athletics"),
			(call_script, "script_ce_get_troop_base_movement_speed", ":troop_no", SPEED_FACTOR_AGILITY),
			(val_add, ":sprint_speed", reg1), # This adds the base 100% (modified by agility)
			(val_add, ":sprint_speed", 130), # Ideally this should make us between 134-190%
			## TROOP ABILITIES - SPRINTER, ENDURANCE, BOUNDLESS ENDURANCE
			(assign, ":speed_factor", 0),
			(assign, ":speed_max", 180),
			(try_begin),
				(eq, "$enable_combat_abilities", 1),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SPRINTER),
				## +50% speed & +30% maximum speed
				(val_add, ":speed_factor", 50),
				(val_add, ":speed_max", 30),
			(else_try),
				(eq, "$enable_combat_abilities", 1),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_ENDURANCE),
				## -25% speed
				(val_add, ":speed_factor", 0),
				(val_add, ":speed_max", -20),
				## -3 seconds to cooldown
				(val_sub, ":maximum_cooldown", 3),
			(else_try),
				(eq, "$enable_combat_abilities", 1),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BOUNDLESS_ENDURANCE),
				## +50% speed
				(val_add, ":speed_factor", 25),
				(val_add, ":speed_max", 0),
			(try_end),
			## Adjust sprinting speed.
			(store_sub, ":base_sprint", ":sprint_speed", 100),
			(val_add, ":speed_factor", 100),
			(store_mul, ":speed_after_abilities", ":speed_factor", ":base_sprint"),
			(val_div, ":speed_after_abilities", 100),
			(store_add, ":sprint_speed", 100, ":speed_after_abilities"),
			(assign, reg31, ":sprint_speed"),
			(val_min, ":sprint_speed", ":speed_max"), # maximum speed.
			### DIAGNOSTIC+ ### - Testing ability boosts and sprint speeds.
			# (try_begin),
				# (key_is_down, "$key_special_sprint"),
				# (assign, reg32, ":base_sprint"),
				# (assign, reg33, ":speed_factor"),
				# (assign, reg34, ":speed_after_abilities"),
				# (assign, reg35, ":sprint_speed"),
				# (display_message, "@DEBUG (sprint): Player sprinting.  base {reg32}, factor {reg33}, speed after abilities {reg34}, raw {reg31}, capped {reg35}.", gpu_debug),
			# (try_end),
			### DIAGNOSTIC- ###
			## Add in speed changes from the combat hampering system.
			(try_begin),
				(eq, "$combat_hampering_enabled", 1),
				(agent_get_slot, ":modified_speed", ":agent_no", slot_agent_last_calculated_speed),
				(store_sub, ":speed_penalty", 100, ":modified_speed"),
				(val_sub, ":sprint_speed", ":speed_penalty"),
			(try_end),
			## TROOP ABILITY - CHARGING STRIKE - Data collection
			(try_begin),
				(agent_set_slot, ":agent_no", slot_agent_sprint_speed, ":sprint_speed"),
			(try_end),
			
			# Determine logic.
			(agent_ai_get_behavior_target, ":agent_target", ":agent_no"),
			(agent_is_active, ":agent_target"),
			(agent_is_alive, ":agent_target"),
			(agent_get_position, pos1, ":agent_target"),
			(agent_get_position, pos2, ":agent_no"),
			(get_distance_between_positions, ":distance", pos1, pos2),
			# (try_begin),
				# (str_store_troop_name, s31, ":troop_no"),
				# (agent_get_troop_id, ":troop_target", ":agent_target"),
				# (str_store_troop_name, s32, ":troop_target"),
				# (assign, reg31, ":distance"),
				# (display_message, "@Agent ({s31}), Target ({s32}), Distance ({reg31}).", gpu_debug),
			# (try_end),
			# Determine how far we can go.
			(assign, ":dps_base_100", 269), # Base distance per second at 100% speed.
			(store_mul, ":dps_sprint", ":dps_base_100", ":sprint_speed"),
			(val_div, ":dps_sprint", 100),
			(agent_get_slot, ":sprint_duration", ":agent_no", slot_agent_current_stamina),
			(val_min, ":sprint_duration", 8), # No more than 8 sec sprints.
			(store_mul, ":maximum_distance", ":dps_sprint", ":sprint_duration"),
			(store_mul, ":minimum_distance", ":maximum_distance", 15),
			(val_div, ":minimum_distance", 100),
			(try_begin),
				(is_between, ":distance", ":minimum_distance", ":maximum_distance"),
				(agent_slot_eq, ":agent_no", slot_agent_is_sprinting, 0),
				(assign, ":agent_wants_to_sprint", 1),
			(else_try),
				(is_between, ":distance", ":minimum_distance", ":maximum_distance"),
				(agent_slot_eq, ":agent_no", slot_agent_is_sprinting, 1),
				(assign, ":agent_wants_to_sprint", 1),
			(else_try),
				(assign, ":agent_wants_to_sprint", 0),
			(try_end),
			
			(try_begin),
				## START SPRINTING ##
				(eq, ":agent_wants_to_sprint", 1),
				(agent_get_horse, ":horse", ":agent_no"),
				(agent_slot_ge, ":agent_no", slot_agent_current_stamina, 1),
				(eq, ":horse", -1),
				# Display output.
				(try_begin),
					(ge, "$cheat_mode", 1),
					(assign, reg1, ":sprint_speed"),
					(str_store_string, s31, "@ at {reg1}% speed"),
				(else_try),
					(str_clear, s31),
				(try_end),
				(agent_set_speed_modifier, ":agent_no", ":sprint_speed"),
				(store_mission_timer_c, ":timer"),
				(agent_set_slot, ":agent_no", slot_agent_sprint_timer, ":timer"), # "$g_wp_tpe_timer"),
				(agent_slot_eq, ":agent_no", slot_agent_sprint_cooldown, 0),  # Sprint can be activated repeatedly now, but endless war cries are annoying.
				(agent_set_slot, ":agent_no", slot_agent_sprint_cooldown, 1), # Done to prevent this block from repeating.
				(troop_get_type, ":gender", ":troop_no"),
				(try_begin),
					(eq, ":gender", 0),
					(agent_play_sound, ":agent_no", "snd_man_warcry"),
				(else_try),
					(agent_play_sound, ":agent_no", "snd_woman_yell"),
				(try_end),
				(try_begin),
					(ge, DEBUG_SPRINTING, 1),
					(is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_champions_end), # Limit Debug Flow
					(str_store_troop_name, s31, ":troop_no"),
					(assign, reg1, ":sprint_speed"),
					(agent_get_slot, ":current_stamina", ":agent_no", slot_agent_current_stamina),
					(store_div, reg2, ":current_stamina", 100),
					(store_mod, reg4, ":current_stamina", 100),
					(try_begin),
						(lt, reg4, 10),
						(str_store_string, s4, "@0{reg4}"),
					(else_try),
						(str_store_string, s4, "@{reg4}"),
					(try_end),
					(agent_get_slot, reg3, ":agent_no", slot_agent_max_stamina),
					(val_div, reg3, 100),
					(display_message, "@DEBUG (Sprinting): {s31} has started sprinting.  Speed = {reg1}%, {reg2}.{s4}/{reg3}.00", gpu_debug),
				(try_end),
				(assign, reg63, 666), # Done to prevent seeing the normal speed message upon mission loading.
			(else_try),
				## STOP SPRINTING DUE TO RUNNING OUT OF STAMINA ##
				(agent_slot_ge, ":agent_no", slot_agent_sprint_timer, 1),
				(neg|agent_slot_ge, ":agent_no", slot_agent_current_stamina, 1),
				(agent_set_slot, ":agent_no", slot_agent_sprint_timer, 0),
				(agent_set_slot, ":agent_no", slot_agent_sprint_speed, 0),
				# Figure out our cooldown.
				(assign, ":cooldown", 8),
				(val_min, ":cooldown", ":maximum_cooldown"),
				(agent_set_slot, ":agent_no", slot_agent_sprint_cooldown, ":cooldown"),
				# Determine base speed with agility boost.
				(store_attribute_level, ":base_speed", ":troop_no", ca_agility),
				(val_add, ":base_speed", 90),
				## Add in speed changes from the combat hampering system.  Use whichever is lower.
				(try_begin),
					(eq, "$combat_hampering_enabled", 1),
					(agent_get_slot, ":modified_speed", ":agent_no", slot_agent_last_calculated_speed),
					(val_min, ":base_speed", ":modified_speed"),
				(try_end),
				(agent_set_speed_modifier, ":agent_no", ":base_speed"),
				(try_begin),
					(ge, DEBUG_SPRINTING, 1),
					(is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_champions_end), # Limit Debug Flow
					(str_store_troop_name, s31, ":troop_no"),
					(agent_get_slot, ":current_stamina", ":agent_no", slot_agent_current_stamina),
					(store_div, reg2, ":current_stamina", 100),
					(store_mod, reg4, ":current_stamina", 100),
					(try_begin),
						(lt, reg4, 10),
						(str_store_string, s4, "@0{reg4}"),
					(else_try),
						(str_store_string, s4, "@{reg4}"),
					(try_end),
					(agent_get_slot, reg3, ":agent_no", slot_agent_max_stamina),
					(val_div, reg3, 100),
					(display_message, "@DEBUG (Sprinting): {s31} has stopped sprinting due to tiring out.  Stamina {reg2}.{s4}/{reg3}.00", gpu_debug),
				(try_end),
			(else_try),
				## STOP SPRINTING DUE TO LOGIC CHANGE ##
				(neq, ":agent_wants_to_sprint", 1),
				(agent_slot_ge, ":agent_no", slot_agent_sprint_timer, 1),
				# Reset our sprint timer.
				# (agent_get_slot, ":sprint_start", ":agent_no", slot_agent_sprint_timer),
				(agent_set_slot, ":agent_no", slot_agent_sprint_timer, 0),
				(agent_set_slot, ":agent_no", slot_agent_sprint_speed, 0),
				# Figure out our cooldown.
				(assign, ":cooldown", 8),
				(val_min, ":cooldown", ":maximum_cooldown"),
				(agent_set_slot, ":agent_no", slot_agent_sprint_cooldown, ":cooldown"),
				# Determine base speed with agility boost.
				(store_attribute_level, ":base_speed", ":troop_no", ca_agility),
				(val_add, ":base_speed", 90),
				## Add in speed changes from the combat hampering system.  Use whichever is lower.
				(try_begin),
					(eq, "$combat_hampering_enabled", 1),
					(agent_get_slot, ":modified_speed", ":agent_no", slot_agent_last_calculated_speed),
					(val_min, ":base_speed", ":modified_speed"),
				(try_end),
				(agent_set_speed_modifier, ":agent_no", ":base_speed"),
			(else_try),
				## COOLDOWN REDUCTION ##
				(neq, ":agent_wants_to_sprint", 1),
				(agent_slot_eq, ":agent_no", slot_agent_sprint_timer, 0),
				(agent_slot_ge, ":agent_no", slot_agent_sprint_cooldown, 1),
				(agent_get_slot, ":cooldown", ":agent_no", slot_agent_sprint_cooldown),
				(val_sub, ":cooldown", 1),
				(agent_set_slot, ":agent_no", slot_agent_sprint_cooldown, ":cooldown"),
			(else_try),
				## RESTORE NORMAL SPEED ##
				(eq, reg63, 666), # Done to prevent seeing the normal speed message upon mission loading.
				(agent_slot_eq, ":agent_no", slot_agent_sprint_timer, 0),
				(agent_slot_eq, ":agent_no", slot_agent_sprint_cooldown, 0),
				(agent_get_slot, ":modified_speed", ":agent_no", slot_agent_last_calculated_speed),
				(agent_set_speed_modifier, ":agent_no", ":modified_speed"),
				# (display_message, "@You have recovered your normal speed.", gpu_green),
				(try_begin),
					(ge, DEBUG_SPRINTING, 1),
					(is_between, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_champions_end), # Limit Debug Flow
					(str_store_troop_name, s31, ":troop_no"),
					(display_message, "@DEBUG (Sprinting): {s31} has recovered to normal speed.", gpu_debug),
				(try_end),
				(agent_set_slot, ":agent_no", slot_agent_sprint_timer, -1), # So we don't keep seeing that our speed is normal again.
				(assign, reg63, 0), # Done to prevent seeing the normal speed message upon mission loading.
			(try_end),
		(try_end),
	]),

## TRIGGER: BODYSLIDING (1 OF 2)
(ti_before_mission_start, 0, 0, 
	[],
	[
		#reset global variables
		(assign, "$player_has_bodyslided", 0), #variable for player party after party rebalancing
		(neq, "$enable_bodysliding", 0),  #is active player enabled?
		
		#backup player party
		(assign, "$g_move_heroes", 1),
		(party_clear, "p_temp_casualties_3"),
		(call_script, "script_party_add_party", "p_temp_casualties_3", "p_main_party"),
		(set_player_troop, "trp_player"), #just in case?
		(assign, "$bodysliding_last_troop", "trp_player"),
	]),
	
## TRIGGER: BODYSLIDING (2 OF 2)
(5, 0, 0, 
	[
		(neq, "$enable_bodysliding", 0),
		(get_player_agent_no,":agent"),
		(neg|agent_is_alive, ":agent"),
	],
	[
		(set_fixed_point_multiplier, 100),
		(get_player_agent_no, ":player_agent"),
		(agent_get_team, ":player_team", ":player_agent"),
		(agent_get_group, ":player_group", ":player_agent"),
		(agent_get_position, pos1, ":player_agent"),
		# (agent_get_division, ":player_division", ":p_agent"),
		(assign, ":spawned", 0),
		(assign, ":bodyslide_target", -1),
		(assign, ":bodyslide_agent", -1),
		(assign, ":closest_distance", 1000000),
		
		## CHECK FOR COMPANIONS FIRST
		(try_for_agents, ":agent_no"),
			(eq, ":bodyslide_target", -1),
			(agent_is_human, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_get_team, ":agent_team", ":agent_no"),
			(eq, ":agent_team", ":player_team"),
			(agent_get_party_id, ":agent_party",":agent_no"),
			(eq, ":agent_party", "p_main_party"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(is_between, ":troop_no", companions_begin, companions_end),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_player_companion),
			# Check for distance.
			(agent_get_position, pos2, ":agent_no"),
			(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
			(lt, ":distance", ":closest_distance"),
			(assign, ":bodyslide_target", ":troop_no"),
			(assign, ":bodyslide_agent", ":agent_no"),
			(assign, ":closest_distance", ":distance"),
			
			### DIAGNOSTIC+ ###
			# (assign, reg31, ":closest_distance"),
			(str_store_troop_name, s31, ":bodyslide_target"),
			(display_message, "@You have assumed control of {s31} to continue the battle.", gpu_debug),
			### DIAGNOSTIC- ###
		(try_end),
		
		## IF NO COMPANION AVAILABLE, CHECK FOR ANOTHER TROOP TYPE.
		(try_begin),
			(eq, ":bodyslide_target", -1),
			(eq, "$enable_bodysliding", BODYSLIDING_ALL_TROOPS),
			(try_for_agents, ":agent_no"),
				(eq, ":bodyslide_target", -1),
				(agent_is_human, ":agent_no"),
				(agent_is_alive, ":agent_no"),
				(agent_get_team, ":agent_team", ":agent_no"),
				(eq, ":agent_team", ":player_team"),
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				(agent_get_party_id, ":agent_party",":agent_no"),
				(eq, ":agent_party", "p_main_party"),
				# Check for distance.
				(agent_get_position, pos2, ":agent_no"),
				(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
				(lt, ":distance", ":closest_distance"),
				(assign, ":bodyslide_target", ":troop_no"),
				(assign, ":bodyslide_agent", ":agent_no"),
				(assign, ":closest_distance", ":distance"),
				
				### DIAGNOSTIC+ ###
				# (assign, reg31, ":closest_distance"),
				(str_store_troop_name, s31, ":bodyslide_target"),
				(display_message, "@You have assumed control of {s31} to continue the battle.", gpu_debug),
				### DIAGNOSTIC- ###
			(try_end),
		(try_end),
		
		(try_begin),
			(ge, ":bodyslide_target", 1),
			(ge, ":bodyslide_agent", 0),
			# (eq, ":spawned", 0),
			# (agent_is_human, ":agent"),
			# (agent_is_alive, ":agent"),
			# (agent_get_team, ":agent_team", ":agent"),
			# (agent_get_party_id, ":agent_party",":agent"),
			# (eq, ":agent_party", "p_main_party"),
			# (agent_get_division, ":agent_division", ":p_agent"),
			# (agent_get_group, ":agent_group", ":p_agent"),
			# # (eq, ":player_team", ":agent_team"),
			# # (eq, ":player_division", ":agent_division"),
			# (agent_get_troop_id,":troop_id", ":agent"),
			# ##
			# (this_or_next|troop_slot_eq, ":troop_id", slot_troop_occupation, slto_player_companion),
			# ##
			# (neg|is_between, ":troop_id", active_npcs_begin, active_npcs_end), #just in case
			## Store Target Troop's Inventory
			(call_script, "script_copy_inventory", ":bodyslide_target", BODYSLIDING_STORAGE),
			(assign, "$bodysliding_last_troop", ":bodyslide_target"),
			(set_player_troop, ":bodyslide_target"),
			(store_agent_hit_points,":hp",":bodyslide_agent",1),
			(agent_get_position, pos1, ":bodyslide_agent"),
			(position_set_z, pos1, -2000), 
			(position_set_x, pos1, 0), 
			(position_set_y, pos1, 0), 
			(agent_get_position, pos0, ":bodyslide_agent"),
			(set_spawn_position, pos0),
			(agent_get_horse, ":horse", ":bodyslide_agent"),
			(try_begin),
				(gt, ":horse", 0),
				(agent_set_position,":horse",pos1),
				(remove_agent, ":horse"),
			(try_end),
			(agent_set_position,":bodyslide_agent", pos1),
			(agent_set_slot, ":bodyslide_agent", slot_agent_possessed, 1), 
			(agent_get_slot, ":index", ":bodyslide_agent", slot_agent_index_value), #lance recruitment flag
			(remove_agent, ":bodyslide_agent"),
			(assign, "$bodyslide_spawn_block", 1),
			(spawn_agent, ":bodyslide_target"),
			(assign, "$bodyslide_spawn_block", 0),
			(assign, ":player_agent", reg0),
			(agent_set_slot, ":player_agent", slot_agent_index_value, ":index"),
			(agent_set_team, ":player_agent", ":player_team"),
			#(agent_set_division, ":player_agent", ":agent_division"),
			(agent_set_hit_points, ":player_agent" ,":hp",1),
			(agent_set_group, ":player_agent", ":player_group"),
			(agent_set_slot, ":player_agent", slot_agent_possessed, 2), 
			(agent_set_slot, ":player_agent", slot_agent_real_troop, ":bodyslide_target"),
			(try_begin),
				(agent_get_horse, ":p_horse", ":player_agent"),
				(gt, ":p_horse", 0), #player is mounted
				(lt, ":horse", 0), #AI is not mounted!
				(agent_set_position,":p_horse",pos1),
				(remove_agent, ":p_horse"),
			(try_end),
			(set_player_troop, "trp_player"),
			(assign, ":spawned", 1),
			(assign, "$player_has_bodyslided", 1), #checks that player spawned and will need to manualy correct party
		(try_end),  
		(eq, ":bodyslide_target", -1),
		(eq, ":spawned", 0),
		(neq, "$cam_free", 1),
		(call_script, "script_cust_cam_init_death_cam", cam_mode_free),
	]),
	
## TRIGGER: FALLEN RIDERS
## PURPOSE: Damages a mounted character whenever their horse is knocked out from under them.
(ti_on_agent_killed_or_wounded, 0, 0, 
	[
		(eq, "$enable_fallen_riders", 1),
	],
    [
		(store_trigger_param_1, ":agent_victim"),
		(store_trigger_param_2, ":agent_killer"),
		(agent_is_active, ":agent_killer"), # Put in to prevent script errors on bodysliding.
		(neg|agent_is_human, ":agent_victim"),
		(agent_get_slot, ":agent_rider", ":agent_victim", slot_agent_rider_agent),
		(ge, ":agent_rider", 0),
		(agent_is_active, ":agent_rider"),
		(agent_is_alive, ":agent_rider"),
		(agent_get_troop_id, ":troop_no", ":agent_rider"),
		
		# Check if the rider is an agile rider and break script if so.
		(assign, ":continue", 1),
		(try_begin),
			(eq, "$enable_combat_abilities", 1),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_AGILE_RIDER),
			(assign, ":continue", 0),
		(try_end),
		(eq, ":continue", 1),
		
		(agent_get_speed, pos4, ":agent_rider"),
		(position_get_y, reg21, pos2),
		(store_div, ":speed", reg21, 2000), # Seems to usually produce a number in the mid 100's.
		(call_script, "script_ce_get_troop_encumbrance", ":troop_no", -1),
		(assign, ":weight", reg1),
		# (try_begin),
			# (gt, ":weight", 100),
			# (val_div, ":weight", 10),
		# (try_end),
		(store_mul, ":weighted_damage", ":weight", ":weight"),
		(val_div, ":weighted_damage", 100),
		(store_div, ":minimum_weighted", ":weight", 2),
		(val_max, ":weighted_damage", ":minimum_weighted"),
		(store_mul, ":damage", ":weighted_damage", ":speed"),
		(val_div, ":damage", 100),
		(assign, reg31, ":damage"), ### DIAGNOSTIC ### - Raw Damage
		(store_skill_level, ":skill_riding", "skl_riding", ":troop_no"),
		(assign, reg32, ":skill_riding"), ### DIAGNOSTIC ### - Riding Skill
		(val_mul, ":skill_riding", 8),
		(assign, reg34, ":skill_riding"), ### DIAGNOSTIC ### - Damage Reduction %
		(store_mul, ":damage_reduction", ":damage", ":skill_riding"),
		(val_div, ":damage_reduction", 100),
		(val_sub, ":damage", ":damage_reduction"),
		
		(assign, reg33, ":damage"), ### DIAGNOSTIC ### - Raw Reduced Damage
		
		(set_show_messages, 0),
		(store_agent_hit_points, ":health", ":agent_rider", 1),
		(val_sub, ":health", ":damage"),
		(try_begin),
			(lt, ":health", 1),
			(assign, ":agent_killed", 1),
			(assign, ":health", 1),
			(agent_set_hit_points, ":agent_rider", ":health", 1),
			(agent_get_kill_count, ":kills_before", ":agent_killer"),
			(agent_deliver_damage_to_agent_advanced, reg0, ":agent_killer", ":agent_rider", ":damage"), # WSE
			(agent_get_kill_count, ":kills_after", ":agent_killer"),
			(try_begin),
				(gt, ":kills_after", ":kills_before"), # If it is higher than the victim was killed.
				(assign, reg24, 1),
			(else_try),
				(assign, reg24, 0),
			(try_end),
		(else_try),
			(assign, ":agent_killed", 0),
			(agent_set_hit_points, ":agent_rider", ":health", 1),
		(try_end),
		(set_show_messages, 1),
		(str_store_troop_name, s21, ":troop_no"),
		## script error
		(agent_get_troop_id, ":troop_killer", ":agent_killer"),
		(str_store_troop_name, s22, ":troop_killer"),
		## script error
		(troop_get_type, reg23, ":troop_no"),
		(get_player_agent_no, ":agent_player"),
		(agent_get_team, ":team_player", ":agent_player"),
		#(agent_get_team, ":team_killer", ":agent_killer"),
		(agent_get_team, ":team_victim", ":agent_rider"),
		(assign, reg22, ":damage"),
		(try_begin),
			(eq, "$display_extra_xp_prof", 1), # combat messages turned ON.
			(troop_get_class, ":class", ":troop_no"),
			(this_or_next|troop_is_hero, ":troop_no"),
			(eq, ":class", 2), # Cavalry
			(try_begin),
				## PLAYER - Horse killed.
				(eq, ":agent_rider", ":agent_player"),
				(display_message, "@Your mount has fallen to the ground beneath you!", gpu_red),
				(display_message, "@Receive {reg22} damage."), # due to falling from your mount.", gpu_red),
				(try_begin),
					(eq, ":agent_killed", 1),
					(display_message, "@You have been knocked unconscious by {s22}.", gpu_red),
				(try_end),
			(else_try),
				## ANYONE - Killed someone's horse (teammate)
				(eq, ":team_player", ":team_victim"),
				(display_message, "@{s21} has been knocked off of {reg23?her:his} mount.", 0xB48211),
				#(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", 0xB48211),
				(try_begin),
					(eq, ":agent_killed", 1),
					(display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", 0xB48211),
				(try_end),
			(else_try),
				## ANYONE - Killed someone's horse (ally)
				(agent_is_ally, ":agent_rider"),
				(display_message, "@{s21} has been knocked off of {reg23?her:his} mount.", 0xB06EDA),
				#(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", 0xB06EDA),
				(try_begin),
					(eq, ":agent_killed", 1),
					(display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", 0xB06EDA),
				(try_end),
			(else_try),
				## ANYONE - Killed someone's horse (enemy)
				(teams_are_enemies, ":team_player", ":team_victim"),
				(display_message, "@{s21} has been knocked off of {reg23?her:his} mount.", 0x42D8A6),
				#(display_message, "@{s21} receives {reg22} damage due to falling from {reg23?her:his} mount.", 0x42D8A6),
				(try_begin),
					(eq, ":agent_killed", 1),
					(display_message, "@{s21} {reg24?killed:knocked unconscious} by {s22}.", 0x42D8A6),
				(try_end),
			(try_end),
		(try_end),
		#(ge, DEBUG_COMBAT_EFFECTS, 2),
		# (assign, reg35, ":weight"),
		# (assign, reg36, ":speed"),
		# (display_message, "@DEBUG: {reg31} [({reg35}wt^2/100 * {reg36}% speed)] raw -> {reg32} ride = -{reg34}% -> {reg33} given", gpu_debug),
	]),
	
## TRIGGER: FALLEN RIDERS (2nd trigger)
## PURPOSE: Does an initial iteration through all agents and stores which mounts & riders are bonded together.
(ti_after_mission_start, 0, ti_once, 
	[(eq, "$enable_fallen_riders", 1),],
    [
		(try_for_agents, ":agent_no"),
			(agent_set_slot, ":agent_no", slot_agent_horse_agent, -1),
			(agent_set_slot, ":agent_no", slot_agent_rider_agent, -1),
			(try_begin),
				## Humans - Get the horse they're attached to and store it.
				(agent_is_human, ":agent_no"),
				(agent_get_horse, reg1, ":agent_no"),
				(agent_set_slot, ":agent_no", slot_agent_horse_agent, reg1),
			(else_try),
				## Mounts - Get the human they're attached to and store it.
				(neg|agent_is_human, ":agent_no"),
				(agent_get_rider, reg1, ":agent_no"),
				(agent_set_slot, ":agent_no", slot_agent_rider_agent, reg1),
			(try_end),
		(try_end),
	]),
	
## TRIGGER: TROOP ABILITY - BONUS_BERSERKER / BONUS_DISCIPLINED
## PURPOSE: Enhances the health of spawning troops.
(ti_on_agent_spawn, 0, 0, [],
    [
		(store_trigger_param_1, ":agent_no"),
		
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		
		## Tossed in to setup modified speed later on.
		(call_script, "script_ce_get_troop_base_movement_speed", ":troop_no", SPEED_FACTOR_TOTAL),
		(agent_set_slot, ":agent_no", slot_agent_last_calculated_speed, reg1),
		
		## STAMINA_BAR TESTING+
		(call_script, "script_ce_agent_get_max_stamina", ":agent_no"),
		## STAMINA_BAR TESTING-
		
		## BERSERKER ABILITY
		(eq, "$enable_combat_abilities", 1),
		(store_agent_hit_points, reg31, ":agent_no", 1),
		(agent_get_party_id, ":party_id", ":agent_no"),
		(call_script, "script_ce_troop_get_bonus_health", ":troop_no", ":party_id"), # combat_scripts.py
		(assign, ":extra_health", reg1),
		(store_agent_hit_points, ":base_health", ":agent_no", 1),
		(val_add, ":base_health", ":extra_health"),
		(agent_set_max_hit_points, ":agent_no", ":base_health", 1),
		(try_begin),
			#(ge, DEBUG_TROOP_ABILITIES, 2),
			(eq, ":troop_no", "trp_player"),
			(store_agent_hit_points, reg32, ":agent_no", 1),
			(str_store_troop_name, s31, ":troop_no"),
			(display_message, "@DEBUG (Abilities): {s31} health improves from {reg31} to {reg32}.", gpu_debug),
		(try_end),
	]),

	
## TRIGGER: COMBAT EFFECTIVENESS HAMPERING
## PURPOSE: As agents take damage they become slower, less accurate and deal less damage.  Very generic at the moment.
(4, 0, 0, 
	[
		(eq, "$enable_combat_abilities", 1),
	],
    [
		(try_for_agents, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(store_agent_hit_points, ":health", ":agent_no"),
			(assign, ":modifed_health", ":health"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(try_begin),
				## TROOP EFFECT: BONUS_FORTITUDE
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_FORTITUDE),
				(assign, reg31, ":health"),
				(val_add, ":modifed_health", 40),
				## TROOP SYNERGY EFFECT: BONUS_DISCIPLINED (+20% Effectiveness)
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_DISCIPLINED),
					(val_add, ":modifed_health", 20),
				(try_end),
			(try_end),
			(try_begin),
				## TROOP EFFECT: BONUS_DISCIPLINED
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_DISCIPLINED),
				(assign, reg31, ":health"),
				(val_add, ":modifed_health", 20),
			(try_end),
			
			## SET BASE VALUES
			# Damage
			(assign, ":modifier_damage", 100),
			# Accuracy
			(assign, ":modifier_accuracy", 100),
			# Movement Speed			
			(call_script, "script_ce_get_troop_base_movement_speed", ":troop_no", SPEED_FACTOR_TOTAL),
			(assign, ":modifier_speed", reg1),
			# Reload Speed
			(assign, ":modifier_reload", 100),
			
			## AGILITY BONUS: Quicker reloading.
			(store_attribute_level, ":AGI", ":troop_no", ca_agility),
			(val_sub, ":AGI", 10),
			(val_mul, ":AGI", 2),
			(val_max, ":AGI", 0),
			(val_add, ":modifier_reload", ":AGI"),
			
			## TROOP ABILITY: BONUS_POISONED_WEAPONS (Poisoned Effect)
			(try_begin),
				(agent_slot_eq, ":agent_no", slot_agent_is_poisoned, 1),
				(val_sub, ":modifed_health", 50),
				## TROOP SYNERGY EFFECT: BONUS_FORTITUDE (Poisons is only half effective)
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_FORTITUDE),
					(val_add, ":modifed_health", 25),
				(try_end),
				## Poison Duration
				(agent_get_slot, ":ticks", ":agent_no", slot_agent_duration_poisoned),
				(val_sub, ":ticks", 1),
				(agent_set_slot, ":agent_no", slot_agent_duration_poisoned, ":ticks"),
				(try_begin),
					(neg|agent_slot_ge, ":agent_no", slot_agent_duration_poisoned, 1),
					(agent_set_slot, ":agent_no", slot_agent_is_poisoned, 0),
					(try_begin),
						(eq, ":troop_no", "trp_player"),
						(display_message, "@You have recovered from the effects of the poison.", gpu_green),
					(try_end),
				(try_end),
				## Health Damage Occurs
				(store_agent_hit_points, ":temp_health", ":agent_no", 1),
				(assign, reg31, ":temp_health"),
				(val_sub, ":temp_health", 1),
				(val_max, ":temp_health", 1), # Can't be killed by poison.
				(agent_set_hit_points, ":agent_no",":temp_health", 1),
			(try_end),
			(val_clamp, ":modifed_health", 0, 101),
			
			## DETERMINE HEALTH BASED LIMITS
			(try_begin),
				(eq, "$combat_hampering_enabled", 1),
				# Damage
				(store_sub, ":health_damage", 100, ":modifed_health"),
				(val_div, ":health_damage", 3),
				(val_sub, ":modifier_damage", ":health_damage"),
				# Accuracy
				(store_sub, ":health_damage", 100, ":modifed_health"),
				(val_div, ":health_damage", 4),
				(val_sub, ":modifier_accuracy", ":health_damage"),
				# Speed
				(store_sub, ":health_damage", 100, ":modifed_health"),
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BOUNDLESS_ENDURANCE),
					(val_div, ":health_damage", 4),
				(else_try),
					(val_div, ":health_damage", 2),
				(try_end),
				(val_sub, ":modifier_speed", ":health_damage"),
			(try_end),
			
			## SEARCH FOR NEARBY COMMANDER EFFECTS
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BLOODLUST),
				(assign, ":troop_is_frenzying", 1),
				# Damage
				(store_sub, ":frenzy_damage", 100, ":health"),
				(val_min, ":frenzy_damage", 25),
				(val_add, ":frenzy_damage", 20),
				(val_add, ":modifier_damage", ":frenzy_damage"),
				# Accuracy
				(store_sub, ":frenzy_accuracy", 100, ":health"),
				(val_div, ":frenzy_accuracy", 2),
				(val_min, ":frenzy_accuracy", 30),
				(val_sub, ":modifier_accuracy", 10),
				(val_sub, ":modifier_accuracy", ":frenzy_accuracy"),
			(else_try),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BERSERKER),
				(assign, ":troop_is_frenzying", 1),
			(else_try),
				(assign, ":troop_is_frenzying", 0),
			(try_end),
			
			(assign, ":highest_tactician_bonus", 0),
			(assign, ":highest_tactician_troop", -1),
			(assign, ":highest_volley_commander_bonus", 0),
			(assign, ":highest_volley_commander_troop", -1),
			(assign, ":highest_firing_captain_bonus", 0),
			(assign, ":highest_firing_captain_troop", -1),
			(try_begin),
				(eq, ":troop_is_frenzying", 0),
				(agent_get_position, pos1, ":agent_no"),
				(set_fixed_point_multiplier, 1000),
				(try_for_agents, ":nearby_agent", pos1, 8000),
					# Qualify our nearby troop to see if they're a valid, active commander.
					(neq, ":nearby_agent", ":agent_no"),
					(agent_is_alive, ":nearby_agent"),
					(agent_is_human, ":nearby_agent"),
					(agent_get_team, ":nearby_agent_team", ":nearby_agent"),
					(agent_get_team, ":team_no", ":agent_no"),
					(eq, ":team_no", ":nearby_agent_team"),
					(agent_get_troop_id, ":nearby_troop", ":nearby_agent"),
					
					## TROOP EFFECT: BONUS_TACTICIAN
					(try_begin),
						(call_script, "script_cf_ce_troop_has_ability", ":nearby_troop", BONUS_TACTICIAN),
						(store_skill_level, ":skill_tactics", "skl_tactics", ":nearby_troop"),
						(val_mul, ":skill_tactics", 3),
						(ge, ":skill_tactics", ":highest_tactician_bonus"),
						(assign, ":highest_tactician_bonus", ":skill_tactics"),
						(assign, ":highest_tactician_troop", ":nearby_troop"),
					(try_end),
					
					## TROOP EFFECT: BONUS_VOLLEY_COMMANDER
					(try_begin),
						(call_script, "script_cf_ce_troop_has_ability", ":nearby_troop", BONUS_VOLLEY_COMMANDER),
						(store_skill_level, ":skill_tactics", "skl_tactics", ":nearby_troop"),
						(val_mul, ":skill_tactics", 3),
						(ge, ":skill_tactics", ":highest_volley_commander_bonus"),
						(assign, ":highest_volley_commander_bonus", ":skill_tactics"),
						(assign, ":highest_volley_commander_troop", ":nearby_troop"),
					(try_end),
					
					## TROOP EFFECT: BONUS_FIRING_CAPTAIN
					(try_begin),
						(call_script, "script_cf_ce_troop_has_ability", ":nearby_troop", BONUS_FIRING_CAPTAIN),
						(store_skill_level, ":skill_leadership", "skl_leadership", ":nearby_troop"),
						(val_mul, ":skill_leadership", 4),
						(val_add, ":skill_leadership", 20),
						(ge, ":skill_leadership", ":highest_firing_captain_bonus"),
						(assign, ":highest_firing_captain_bonus", ":skill_leadership"),
						(assign, ":highest_firing_captain_troop", ":nearby_troop"),
					(try_end),
					
				(try_end), # Nearby Agents Loop
				
				## TROOP EFFECT: SIEGE GENERAL
				(try_begin),
					(party_get_slot, ":troop_cotg", "$current_town", slot_center_advisor_war),
					(is_between, ":troop_cotg", companions_begin, companions_end),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_cotg", BONUS_SIEGE_GENERAL),
					(is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),   # Sieges
					
					(agent_get_team, ":team_no", ":agent_no"),
					(eq, ":team_no", 0), # Defenders are team 0.
					
					(store_skill_level, ":skill_tactics", "skl_tactics", ":troop_cotg"),
					(val_mul, ":skill_tactics", 3),
					(try_begin),
						(ge, ":skill_tactics", ":highest_volley_commander_bonus"),
						(assign, ":highest_volley_commander_bonus", ":skill_tactics"),
						(assign, ":highest_volley_commander_troop", ":troop_cotg"),
					(try_end),
					(try_begin),
						(ge, ":skill_tactics", ":highest_tactician_bonus"),
						(assign, ":highest_tactician_bonus", ":skill_tactics"),
						(assign, ":highest_tactician_troop", ":troop_cotg"),
					(try_end),
				(try_end),
				
				(val_add, ":modifier_damage", ":highest_tactician_bonus"),
				(val_add, ":modifier_accuracy", ":highest_volley_commander_bonus"),
				(val_add, ":modifier_reload", ":highest_firing_captain_bonus"),
			(try_end),
			
			## TROOP EFFECT: BONUS_SHARPSHOOTER
			(try_begin),
				(eq, ":troop_is_frenzying", 0),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SHARPSHOOTER),
				(store_skill_level, ":skill_weapon_master", "skl_weapon_master", ":troop_no"),
				(val_mul, ":skill_weapon_master", 4),
				(val_add, ":skill_weapon_master", 20),
				## TROOP EFFECT SYNERGY: BONUS_MASTER_BOWMAN (+40% effectiveness)
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_MASTER_BOWMAN),
					(store_mul, ":synergy_bonus", ":skill_weapon_master", 30),
					(val_div, ":synergy_bonus", 100),
					(val_add, ":skill_weapon_master", ":synergy_bonus"),
				(try_end),
				(val_add, ":modifier_accuracy", ":skill_weapon_master"),
			(try_end),
			
			## TROOP EFFECT: BONUS_BLADEMASTER
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BLADEMASTER),
				(agent_get_wielded_item, ":item_left", ":agent_no", 0),
				(agent_get_wielded_item, ":item_right", ":agent_no", 1),
				(assign, ":blademaster_continue", 0),
				(try_begin),
					(store_cur_mission_template_no, ":mission_no"), # WSE
					(this_or_next|eq, ":mission_no", "mt_tpe_tournament_standard"),
					(this_or_next|eq, ":mission_no", "mt_tpe_tournament_native_gear"),
					(eq, ":mission_no", "mt_arena_melee_fight"),
					(assign, ":mission_is_tournament", 1),
				(else_try),
					(assign, ":mission_is_tournament", 0),
				(try_end),
				(try_begin),
					(ge, ":item_left", 1),
					(item_get_type, ":item_type", ":item_left"),
					# Are we wielding a melee weapon?
					(this_or_next|eq, ":item_type", itp_type_one_handed_wpn),
					(this_or_next|eq, ":item_type", itp_type_two_handed_wpn),
					(eq, ":item_type", itp_type_polearm),
					# Is it a cutting weapon?
					(item_get_swing_damage_type, ":damage_type", ":item_left"),
					(this_or_next|eq, ":mission_is_tournament", 1),
					(eq, ":damage_type", cut),
					(assign, ":blademaster_continue", 1),
				(else_try),
					(ge, ":item_right", 1),
					(item_get_type, ":item_type", ":item_right"),
					# Are we wielding a melee weapon?
					(this_or_next|eq, ":item_type", itp_type_one_handed_wpn),
					(this_or_next|eq, ":item_type", itp_type_two_handed_wpn),
					(eq, ":item_type", itp_type_polearm),
					# Is it a cutting weapon?
					(item_get_swing_damage_type, ":damage_type", ":item_right"),
					(this_or_next|eq, ":mission_is_tournament", 1),
					(eq, ":damage_type", cut),
					(assign, ":blademaster_continue", 1),
				(try_end),
				(eq, ":blademaster_continue", 1),
				(store_skill_level, ":skill_weapon_master", "skl_weapon_master", ":troop_no"),
				(val_mul, ":skill_weapon_master", 2),
				(val_add, ":modifier_damage", ":skill_weapon_master"),
				### TROOP EFFECT SYNERGY: BONUS_SAVANT (+1% damage per 2 INT > 10.)
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SAVANT),
					(store_attribute_level, ":INT", ":troop_no", ca_intelligence),
					(val_sub, ":INT", 10),
					(val_div, ":INT", 2),
					(val_max, ":INT", 0), # Don't let this penalize the player.
					(val_add, ":modifier_damage", ":INT"),
				(try_end),
			(try_end),
			
			## TROOP EFFECT: BONUS_MASTER_BOWMAN
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_MASTER_BOWMAN),
				(call_script, "script_cf_ce_agent_is_wielding_weapon_type", ":agent_no", itp_type_bow),
				(store_skill_level, ":skill_weapon_master", "skl_weapon_master", ":troop_no"),
				(val_mul, ":skill_weapon_master", 2),
				(val_add, ":skill_weapon_master", 8),
				## TROOP EFFECT SYNERGY: BONUS_SHARPSHOOTER (+40% effectiveness)
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SHARPSHOOTER),
					(store_mul, ":synergy_bonus", ":skill_weapon_master", 30),
					(val_div, ":synergy_bonus", 100),
					(val_add, ":skill_weapon_master", ":synergy_bonus"),
				(try_end),
				(val_add, ":modifier_damage", ":skill_weapon_master"),
			(try_end),
			
			## TROOP EFFECT: BONUS_ENGINEER
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_ENGINEER),
				(call_script, "script_cf_ce_agent_is_wielding_weapon_type", ":agent_no", itp_type_crossbow),
				(store_skill_level, ":skill_weapon_master", "skl_weapon_master", ":troop_no"),
				(store_mul, ":bonus_damage", ":skill_weapon_master", 3),
				(val_add, ":modifier_damage", ":bonus_damage"),
				(store_mul, ":bonus_accuracy", ":skill_weapon_master", 2),
				(val_add, ":modifier_accuracy", ":bonus_accuracy"),
			(try_end),
			
			## TROOP EFFECT: BONUS_RAPID_RELOAD (Crossbows, Muskets & Pistols)
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_RAPID_RELOAD),
				(assign, ":pass", 0),
				(try_begin),
					(call_script, "script_cf_ce_agent_is_wielding_weapon_type", ":agent_no", itp_type_crossbow),
					(assign, ":pass", 1),
				(else_try),
					(call_script, "script_cf_ce_agent_is_wielding_weapon_type", ":agent_no", itp_type_pistol),
					(assign, ":pass", 1),
				(else_try),
					(call_script, "script_cf_ce_agent_is_wielding_weapon_type", ":agent_no", itp_type_musket),
					(assign, ":pass", 1),
				(try_end),
				(eq, ":pass", 1),
				(store_proficiency_level, ":prof_crossbow", ":troop_no", wpt_crossbow),
				(val_div, ":prof_crossbow", 3),
				(val_add, ":modifier_reload", ":prof_crossbow"),
			(try_end),
			
			## ORDER: VOLLEY FIRE - Improve the accuracy of volley firing troops to make up for the inherent accuracy lose from holding fire.
			(try_begin),
				(agent_slot_ge, ":agent_no", slot_agent_volley_fire, 1),
				(val_add, ":modifier_accuracy", 40),
			(try_end),
			
			## APPLY NEW MODIFICATIONS
			(agent_set_damage_modifier, ":agent_no", ":modifier_damage"),
			(agent_set_accuracy_modifier, ":agent_no", ":modifier_accuracy"),
			(try_begin),
				(agent_slot_eq, ":agent_no", slot_agent_is_sprinting, 0),
				(agent_set_speed_modifier, ":agent_no", ":modifier_speed"),
			(try_end),
			(agent_set_slot, ":agent_no", slot_agent_last_calculated_speed, ":modifier_speed"),
			(agent_set_reload_speed_modifier, ":agent_no", ":modifier_reload"),
			
			### DIAGNOSTIC+ ###
			(try_begin),
				(eq, ":troop_no", "trp_player"), # Very spammy if set to show everyone.
				(ge, DEBUG_TROOP_ABILITIES, 2), 
				(assign, reg31, ":modifier_damage"),
				(assign, reg32, ":modifier_accuracy"),
				(assign, reg33, ":modifier_speed"),
				(assign, reg34, ":modifier_reload"),
				(str_store_troop_name, s31, ":troop_no"),
				# (this_or_next|eq, ":highest_tactician_troop", "trp_player"),
				# (this_or_next|eq, ":highest_volley_commander_troop", "trp_player"),
				# (this_or_next|eq, ":highest_firing_captain_troop", "trp_player"),
				# (eq, ":troop_no", "trp_player"),
				
				(try_begin),
					(display_message, "@DEBUG (Abilities): {s31} modifies damage ({reg31}%), accuracy ({reg32}%), speed ({reg33}%), reload ({reg34}%).", gpu_debug),
					(try_begin),
						(ge, ":highest_tactician_bonus", 1),
						(assign, reg34, ":highest_tactician_bonus"),
						(str_store_troop_name, s32, ":highest_tactician_troop"),
						(display_message, "@DEBUG (Abilities): {s31} is enhanced by {s32}'s tactician bonus of {reg34}.", gpu_debug),
					(try_end),
					(try_begin),
						(ge, ":highest_volley_commander_bonus", 1),
						(assign, reg35, ":highest_volley_commander_bonus"),
						(str_store_troop_name, s33, ":highest_volley_commander_troop"),
						(display_message, "@DEBUG (Abilities): {s31} is enhanced by {s33}'s volley commander bonus of {reg35}.", gpu_debug),
					(try_end),
					(try_begin),
						(ge, ":highest_firing_captain_bonus", 1),
						(assign, reg35, ":highest_firing_captain_bonus"),
						(str_store_troop_name, s33, ":highest_firing_captain_troop"),
						(display_message, "@DEBUG (Abilities): {s31} is enhanced by {s33}'s firing captain bonus of +{reg35}%.", gpu_debug),
					(try_end),
					(try_begin),
						(eq, ":troop_is_frenzying", 1),
						(assign, reg34, ":frenzy_damage"),
						(assign, reg35, ":frenzy_accuracy"),
						(display_message, "@DEBUG (Abilities): {s31}'s frenzy effects: +{reg34}% damage & {reg35}% accuracy", gpu_debug),
					(try_end),
				(try_end),
			(try_end),
			### DIAGNOSTIC- ###
		(try_end),
	]),
	
## TRIGGER: TRACK WHERE AGENTS ARE HIT
## PURPOSE: This will track where an agent is hit and apply penalties to speed, damage or accuracy as appropriate.
(ti_on_agent_hit, 0, 0, 
	[
		(eq, 1, 0),
	], 
	[
		# Trigger Param 1: damage inflicted agent_id
		# Trigger Param 2: damage dealer agent_id
		# Trigger Param 3: inflicted damage
		(store_trigger_param_1, ":agent_victim"),
		(store_trigger_param_2, ":agent_attacker"),
		#(store_trigger_param_3, ":initial_damage"),
		(store_trigger_param, ":bone", 5),
		
		(agent_get_troop_id, ":troop_attacker", ":agent_attacker"),
		(agent_get_troop_id, ":troop_victim", ":agent_victim"),
		(this_or_next|eq, ":troop_attacker", "trp_player"),
		(eq, ":troop_victim", "trp_player"),
		(agent_is_human, ":agent_victim"),
		(agent_is_human, ":agent_attacker"),
		(try_begin),
			(eq, ":troop_attacker", "trp_player"),
			(str_store_string, s21, "@You have"),
		(else_try),
			(str_store_troop_name, s21, ":troop_attacker"),
			(str_store_string, s21, "@{s21} has"),
		(try_end),
		(try_begin),
			(eq, ":troop_victim", "trp_player"),
			(str_store_string, s22, "@you"),
		(else_try),
			(str_store_troop_name, s22, ":troop_victim"),
		(try_end),
		(try_begin),
			(eq, ":bone", hb_abdomen),
			(display_message, "@{s21} struck {s22} in the ABDOMEN."),
		(else_try),
			(this_or_next|eq, ":bone", hb_thigh_l),
			(eq, ":bone", hb_thigh_r),
			(display_message, "@{s21} struck {s22} in the THIGH."),
		(else_try),
			(this_or_next|eq, ":bone", hb_calf_l),
			(eq, ":bone", hb_calf_r),
			(display_message, "@{s21} struck {s22} in the CALF."),
		(else_try),
			(this_or_next|eq, ":bone", hb_foot_l),
			(eq, ":bone", hb_foot_r),
			(display_message, "@{s21} struck {s22} in the FOOT."),
		(else_try),
			(eq, ":bone", hb_spine),
			(display_message, "@{s21} struck {s22} in the SPINE."),
		(else_try),
			(eq, ":bone", hb_thorax),
			(display_message, "@{s21} struck {s22} in the THORAX."),
		(else_try),
			(eq, ":bone", hb_head),
			(display_message, "@{s21} struck {s22} in the HEAD."),
		(else_try),
			(this_or_next|eq, ":bone", hb_shoulder_l),
			(eq, ":bone", hb_shoulder_r),
			(display_message, "@{s21} struck {s22} in the SHOULDER."),
		(else_try),
			(this_or_next|eq, ":bone", hb_upperarm_l),
			(eq, ":bone", hb_upperarm_r),
			(display_message, "@{s21} struck {s22} in the UPPER ARM."),
		(else_try),
			(this_or_next|eq, ":bone", hb_forearm_l),
			(eq, ":bone", hb_forearm_r),
			(display_message, "@{s21} struck {s22} in the FOREARM."),
		(else_try),
			(this_or_next|eq, ":bone", hb_hand_l),
			(eq, ":bone", hb_hand_r),
			(display_message, "@{s21} struck {s22} in the HANDS."),
		(else_try),
			(eq, ":bone", hb_item_l),
			(display_message, "@{s21} struck {s22} in the ITEM / LEFT HAND."),
		(else_try),
			(eq, ":bone", hb_item_r),
			(display_message, "@{s21} struck {s22} in the ITEM / RIGHT HAND."),
		(else_try),
			(display_message, "@{s21} struck {s22} in an UNDEFINED LOCATION!"),
		(try_end),


# #Horse bones
# hrsb_pelvis = 0
# hrsb_spine_1 = 1
# hrsb_spine_2 = 2
# hrsb_spine_3 = 3
# hrsb_neck_1 = 4
# hrsb_neck_2 = 5
# hrsb_neck_3 = 6
# hrsb_head = 7
# hrsb_l_clavicle = 8
# hrsb_l_upper_arm = 9
# hrsb_l_forearm = 10
# hrsb_l_hand = 11
# hrsb_l_front_hoof = 12
# hrsb_r_clavicle = 13
# hrsb_r_upper_arm = 14
# hrsb_r_forearm = 15
# hrsb_r_hand = 16
# hrsb_r_front_hoof = 17
# hrsb_l_thigh = 18
# hrsb_l_calf = 19
# hrsb_l_foot = 20
# hrsb_l_back_hoof = 21
# hrsb_r_thigh = 22
# hrsb_r_calf = 23
# hrsb_r_foot = 24
# hrsb_r_back_hoof = 25
# hrsb_tail_1 = 26
# hrsb_tail_2 = 27
		#(set_trigger_result, ":initial_damage"),
	]),
	
## TRIGGER: BONUS_SUPPLY_RUNNER
## PURPOSE: Restocks ammunition of ranged attackers on the same team every minute based on how many runners exist on the battlefield.
(60, 0, 0, 
	[
		# (neq, "$g_mt_mode", abm_tournament),
		(eq, "$enable_combat_abilities", 1),
		(store_cur_mission_template_no, ":mission_no"), # WSE
		(neq, ":mission_no", "mt_arena_melee_fight"), # Arena fights to prevent the map from showing up there or while talking to the arena master.
		(neq, ":mission_no", "mt_tpe_tournament_native_gear"), # Tournament fights should be excluded.
		(neq, ":mission_no", "mt_tpe_tournament_standard"), # Tournament fights should be excluded.
	],
    [
		(assign, ":troop_array", "trp_temp_array_a"),
		
		(try_for_range, ":slot_no", 0, 8),
			(troop_set_slot, ":troop_array", ":slot_no", 0),
		(try_end),
		
		## CHECK FOR TOTAL ARCHERS ON EACH TEAM.
		(try_for_agents, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_get_troop_id, ":troop_no", ":agent_no"),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SUPPLY_RUNNER),
			(agent_get_team, ":team_no", ":agent_no"),
			(assign, ":runner_value", 3),
			(try_begin),
				(is_between, ":troop_no", companions_begin, companions_end),
				# Companions with this effect gain +1 troop restocked per minute per combined 1 point of Athletics & Inventory Management. (Limit +5)
				(store_skill_level, ":skill_athletics", "skl_athletics", ":troop_no"),
				(store_skill_level, ":runner_bonus", "skl_inventory_management", ":troop_no"),
				(val_min, ":runner_bonus", ":skill_athletics"),
				(val_min, ":runner_bonus", 5),
				(val_add, ":runner_value", ":runner_bonus"),
			(try_end),
			## DIAGNOSTIC+ ##
			# (assign, reg31, ":runner_value"),
			# (assign, reg32, ":team_no"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (display_message, "@DEBUG (SR): {s31} adds a value of +{reg31} to team #{reg32}. (Supply Runner)", gpu_debug),
			## DIAGNOSTIC- ##
			(troop_get_slot, ":restock", ":troop_array", ":team_no"),
			(val_add, ":restock", ":runner_value"),
			(troop_set_slot, ":troop_array", ":team_no", ":restock"),
		(try_end),
		
		## DIAGNOSTIC+ ##
		# (try_for_range, ":slot_no", 0, 8),
			# (troop_get_slot, reg31, ":troop_array", ":slot_no"),
			# (ge, reg31, 1),
			# (assign, reg32, ":slot_no"),
			# (display_message, "@DEBUG (SR): Team #{reg32} has a restocking value of {reg31}.", gpu_debug),
		# (try_end),
		## DIAGNOSTIC- ##
		
		(try_for_agents, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_get_team, ":team_no", ":agent_no"),
			(troop_slot_ge, ":troop_array", ":team_no", 1),
			(assign, ":continue", 0),
			(try_begin),
				(agent_get_wielded_item, ":item_no", ":agent_no", 0),
				(ge, ":item_no", 1),
				(item_get_type, ":item_type", ":item_no"),
				(this_or_next|eq, ":item_type", itp_type_bow),
				(this_or_next|eq, ":item_type", itp_type_crossbow),
				(eq, ":item_type", itp_type_thrown),
				(assign, ":continue", 1),
			(else_try),
				(agent_get_wielded_item, ":item_no", ":agent_no", 1),
				(ge, ":item_no", 1),
				(item_get_type, ":item_type", ":item_no"),
				(this_or_next|eq, ":item_type", itp_type_bow),
				(this_or_next|eq, ":item_type", itp_type_crossbow),
				(eq, ":item_type", itp_type_thrown),
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			(agent_get_ammo, ":ammo_max", ":agent_no", 0),
			(assign, ":ammo_current", 0),
			(assign, ":ammo_max", 0),
			(try_for_range, ":weapon_slot", 0, 4),
				(agent_get_item_slot, ":item_wielded", ":agent_no", ":weapon_slot"),
				(ge, ":item_wielded", 1),
				(item_get_type, ":item_type", ":item_wielded"),
				(this_or_next|eq, ":item_type", itp_type_arrows),
				(this_or_next|eq, ":item_type", itp_type_bolts),
				(eq, ":item_type", itp_type_bullets),
				(item_get_max_ammo, reg31, ":item_wielded"),
				(agent_get_item_cur_ammo, reg32, ":agent_no", ":weapon_slot"),
				(val_add, ":ammo_current", reg32),
				(val_add, ":ammo_max", reg31),
			(try_end),
			(store_mul, ":ammo_80", ":ammo_max", 80),
			(val_div, ":ammo_80", 100),
			## DIAGNOSTIC+ ##
			# (agent_get_troop_id, ":troop_no", ":agent_no"),
			# (assign, reg31, ":ammo_max"),
			# (assign, reg32, ":ammo_current"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (display_message, "@DEBUG (SR): {s31} has {reg32} / {reg31} ammo.", gpu_debug),
			## DIAGNOSTIC- ##
			(lt, ":ammo_current", ":ammo_80"),
			(agent_refill_ammo, ":agent_no"),
			(troop_get_slot, ":restock", ":troop_array", ":team_no"),
			(val_sub, ":restock", 1),
			(troop_set_slot, ":troop_array", ":team_no", ":restock"),
			## DIAGNOSTIC+ ##
			# (assign, reg31, ":restock"),
			# (assign, reg32, ":team_no"),
			# (store_sub, reg33, ":ammo_max", ":ammo_current"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (display_message, "@DEBUG (SR): {s31} of team #{reg32} gets restocked {reg33} ammo. ({reg31} left)", gpu_debug),
			## DIAGNOSTIC- ##
		(try_end),
		
		# Sift through the agents and replenish the ammunition of the defenders.
		# (try_for_agents, ":agent_no"),
			# (agent_is_human, ":agent_no"),
			# (agent_is_alive, ":agent_no"),
			# (agent_get_team, ":team_no", ":agent_no"),
			# (agent_refill_ammo, ":agent_no"),
		# (try_end),
		# (display_message, "@Runners have arrived to replenish your stores of ranged ammunition.", gpu_green),
	]),
	
## TRIGGER: BONUS_STEADY_AIM (1 of 2)
## PURPOSE: Cycles through agents increasing a counter for every second since their last attack.
(1, 0, 0, 
	[
		(eq, "$enable_combat_abilities", 1),
	],
    [
		## INCREASE COUNTER FOR AGENTS.
		(try_for_agents, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_get_slot, ":time", ":agent_no", slot_agent_time_since_attack),
			(val_add, ":time", 1),
			(agent_set_slot, ":agent_no", slot_agent_time_since_attack, ":time"),
		(try_end),
	]),
	
## TRIGGER: BONUS_STEADY_AIM (2 of 2)
## PURPOSE: Cycles through agents increasing a counter for every second since their last attack.
(ti_on_agent_hit, 0, 0, 
	[
		(eq, "$enable_combat_abilities", 1),
	],
    [
		# (store_trigger_param_1, ":agent_victim"),
		(store_trigger_param_2, ":agent_attacker"),
		(store_trigger_param_3, ":initial_damage"),
		
		# Get base time bonus.
		(agent_get_slot, ":time", ":agent_attacker", slot_agent_time_since_attack),
		(agent_set_slot, ":agent_attacker", slot_agent_time_since_attack, 0), # Reset time.
		
		## Check abilities that benefit from time delays.
		(agent_get_troop_id, ":troop_attacker", ":agent_attacker"),
		(assign, ":continue", 0),
		(assign, ":bonus", 0),
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_attacker", BONUS_STEADY_AIM),
			(assign, ":pass", 0),
			(try_begin),
				(call_script, "script_cf_ce_agent_is_wielding_weapon_type", ":agent_attacker", itp_type_bow),
				(assign, ":pass", 1),
			(else_try),
				(call_script, "script_cf_ce_agent_is_wielding_weapon_type", ":agent_attacker", itp_type_crossbow),
				(assign, ":pass", 1),
			(try_end),
			(eq, ":pass", 1),
			(assign, ":continue", 1),
			
			(store_attribute_level, ":STR", ":troop_attacker", ca_strength),
			## SYNERGY EFFECT: BONUS_MASTER_BOWMAN
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_attacker", BONUS_MASTER_BOWMAN),
				## 65% of Strength
				(store_mul, ":STR_limit", ":STR", 65),
				(val_div, ":STR_limit", 100),
				(assign, ":STR", ":STR_limit"),
			(else_try),
				## 50% of Strength.
				(val_div, ":STR", 2),
			(try_end),
			(val_add, ":STR", 1),
			## SYNERGY EFFECT: BONUS_SHARPSHOOTER
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_attacker", BONUS_SHARPSHOOTER),
				## Synergy: +3 damage per second.
				(store_mul, ":bonus", ":time", 3),
			(else_try),
				## Default: +2 damage per second.
				(store_mul, ":bonus", ":time", 2),
			(try_end),
			(val_clamp, ":bonus", 0, ":STR"),
		(try_end),
		(eq, ":continue", 1),
		(val_add, ":initial_damage", ":bonus"),
		
		### DIAGNOSTIC+ ###
		# (assign, reg31, ":time"),
		# (assign, reg32, ":bonus"),
		# (store_attribute_level, reg33, ":troop_attacker", ca_strength),
		# (str_store_troop_name, s31, ":troop_attacker"),
		# (display_message, "@DEBUG: {s31} improves damage by +{reg32} after {reg31} sec pause.  STR = {reg33}.", gpu_debug),
		### DIAGNOSTIC- ###
		
		(set_trigger_result, ":initial_damage"),
	]),
	
## TRIGGER: BONUS_CHARGING_STIRKE
## PURPOSE: Captures an attack attempt and improves damage based on player speed.
(ti_on_agent_hit, 0, 0, 
	[
		(eq, "$enable_combat_abilities", 1),
		(eq, "$enable_sprinting", 1),
	],
    [
		# (store_trigger_param_1, ":agent_victim"),
		(store_trigger_param_2, ":agent_attacker"),
		(store_trigger_param_3, ":initial_damage"),
		
		(agent_get_troop_id, ":troop_no", ":agent_attacker"),
		(agent_slot_ge, ":agent_attacker", slot_agent_sprint_timer, 1),
		(try_begin),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_CHARGING_STRIKE),
			(agent_get_slot, ":speed", ":agent_attacker", slot_agent_sprint_speed),
			(assign, reg32, ":speed"),
			(val_sub, ":speed", 100),
			(ge, ":speed", 1),
			(store_div, ":bonus", ":speed", 4),
			(store_attribute_level, ":limiter", ":troop_no", ca_strength),
			## TROOP SYNERGY EFFECT: BONUS_SECOND_WIND (Allows STR or AGI, whichever is higher)
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SECOND_WIND),
				(store_attribute_level, ":AGI", ":troop_no", ca_agility),
				(val_max, ":limiter", ":AGI"),
			(try_end),
			## TROOP SYNERGY EFFECT: BONUS_BLADEMASTER (Improves limit of attribute from 60% to 75%)
			(assign, ":limiter_scaler", 50),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BLADEMASTER),
				(assign, ":limiter_scaler", 65),
			(try_end),
			(val_mul, ":limiter", ":limiter_scaler"),
			(val_div, ":limiter", 100),
			(val_min, ":bonus", ":limiter"),
			
			(val_add, ":initial_damage", ":bonus"),
			
			### DIAGNOSTIC+ ###
			# (assign, reg31, ":initial_damage"),
			# (assign, reg32, ":initial_damage"),
			# (assign, reg33, ":bonus"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (display_message, "@CHARGING STRIKE: {s31} improves damage from {reg31} to {reg32} by +{reg33}.", gpu_debug),
			### DIAGNOSTIC- ###
		(try_end),
		
		(set_trigger_result, ":initial_damage"),
	]),
	
## TRIGGER: BONUS_POISONED_WEAPONS (1 of 1)
## PURPOSE: Triggers on attack to poison the target of someone who uses poisoned weapons.
(ti_on_agent_hit, 0, 0, 
	[
		(eq, "$enable_combat_abilities", 1),
		(eq, "$combat_hampering_enabled", 1),
	],
    [
		(store_trigger_param_1, ":agent_victim"),
		(store_trigger_param_2, ":agent_attacker"),
		(store_trigger_param_3, ":initial_damage"),
		
		(ge, ":initial_damage", 1), # You have to actually hurt them.
		(agent_is_human, ":agent_victim"),
		(agent_is_alive, ":agent_victim"),
		(neq, ":agent_victim", ":agent_attacker"),
		(agent_get_troop_id, ":troop_attacker", ":agent_attacker"),
		(agent_get_troop_id, ":troop_victim", ":agent_victim"),
		(call_script, "script_cf_ce_troop_has_ability", ":troop_attacker", BONUS_POISONED_WEAPONS),
		
		# Filter Inappropriate Missions
		(store_cur_mission_template_no, ":mission_no"), # WSE
		(neq, ":mission_no", "mt_arena_melee_fight"), # Arena fights to prevent the map from showing up there or while talking to the arena master.
		(neq, ":mission_no", "mt_tpe_tournament_native_gear"), # Tournament fights should be excluded.
		(neq, ":mission_no", "mt_tpe_tournament_standard"), # Tournament fights should be excluded.
		(neq, ":mission_no", "mt_village_training"), # Training peasants should be excluded.
		
		# Player notification of poisoning someone else.
		(try_begin),
			(eq, ":troop_attacker", "trp_player"),
			(agent_slot_eq, ":agent_victim", slot_agent_is_poisoned, 0),
			(str_store_troop_name, s21, ":troop_victim"),
			(display_message, "@Your attack has left {s21} poisoned.", gpu_green),
		(try_end),
		
		# Apply poison effect to victim.
		(agent_set_slot, ":agent_victim", slot_agent_is_poisoned, 1),
		(agent_set_slot, ":agent_victim", slot_agent_duration_poisoned, 20),
		
		# Player notification of being poisoned.
		(try_begin),
			(eq, ":troop_victim", "trp_player"),
			(str_store_troop_name, s21, ":troop_attacker"),
			(display_message, "@{s21}'s attack has left you feeling suddenly flush and weakened.", gpu_green),
		(try_end),
		
		# Attacker must lose one honor (player effect)
		(agent_get_team, ":team_attacker", ":agent_attacker"),
		(get_player_agent_no, ":agent_player"),
		(agent_get_team, ":team_player", ":agent_player"),
		(try_begin),
			(this_or_next|eq, ":troop_attacker", "trp_player"),
			(eq, ":team_attacker", ":team_player"),
			(neq, ":troop_attacker", "trp_npc16"), # Klethi does not trigger this penalty.
			(agent_slot_eq, ":agent_player", slot_agent_honor_lost_for_poison, 0),
			(agent_set_slot, ":agent_player", slot_agent_honor_lost_for_poison, 1),
			(call_script, "script_change_player_honor", -1),
		(try_end),
	]),
	
## TRIGGER: TESTING JUNK.  DELETE FROM FINAL VERSION.
# (999, 0, 0, [], []),
	
]


def modmerge_mission_templates(orig_mission_templates):
	
	for i in range (0,len(orig_mission_templates)):
		# brute force add formation triggers to all mission templates with mtf_battle_mode
		if( orig_mission_templates[i][1] & mtf_battle_mode ):
			orig_mission_templates[i][5].extend(combat_enhancement_triggers)
		# brute force add formation triggers to all mission templates with mtf_arena_fight
		if( orig_mission_templates[i][1] & mtf_arena_fight ):
			orig_mission_templates[i][5].extend(combat_enhancement_triggers)
		
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
	try:
		var_name_1 = "mission_templates"
		orig_mission_templates = var_set[var_name_1]
		modmerge_mission_templates(orig_mission_templates)

	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)
	
	##Extending Mission Templates' trigger lists with triggers appropriate to the templates
	for i in range(len(orig_mission_templates)):
		mt_name = orig_mission_templates[i][0]
		if(mt_name=="bandits_at_night" or mt_name=="castle_visit" or mt_name=="town_fight" or mt_name=="town_center" or mt_name=="visit_town_castle" or mt_name=="village_center" or mt_name=="village_training"):
			orig_mission_templates[i][5].extend(combat_enhancement_triggers)
