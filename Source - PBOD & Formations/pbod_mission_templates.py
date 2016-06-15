## Prebattle Orders & Deployment by Caba'drin
## v0.96.3
## 29 March 2012

from header_common import *
from header_items import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_scenes import *

## Prebattle Orders & Deployment Begin
init_player_global_variables = ( #in pbod_common_triggers and custom_camera_triggers
  0, 0, ti_once, [(get_player_agent_no, "$fplayer_agent_no"),(ge, "$fplayer_agent_no", 0)], [
	(agent_get_team, "$fplayer_team_no", "$fplayer_agent_no"),		
	(agent_get_horse, ":horse", "$fplayer_agent_no"),
	(agent_set_slot, "$fplayer_agent_no", slot_agent_horse, ":horse"),
   ])
  
init_scene_boundaries = ( #in field_ai_triggers
   ti_after_mission_start, 0, 0, [
    (set_fixed_point_multiplier, 100),
	(get_scene_boundaries, pos2, pos3),
	(position_get_x, "$g_bound_right", pos2),
	(position_get_y, "$g_bound_top", pos2),
	(position_get_x, "$g_bound_left", pos3),
	(position_get_y, "$g_bound_bottom", pos3),
   ], [])

init_weather_effects = ( #in pbod_battle_triggers
  ti_before_mission_start, 0, 0, [(party_slot_eq, "p_main_party", slot_party_pref_wp_prof_decrease, 1)], [
	(call_script, "script_weather_change_rain_or_snow"),
    (call_script, "script_weather_affect_proficiency", reg0, reg1), #from change_rain_or_snow
   ])

horse_whistle = ( #in pbod_common_triggers  #also horse 'rear'
   0, 0, 2, 
   [
    (key_clicked, "$key_special_whistle"),
    (neg|main_hero_fallen),
	(ge, "$fplayer_agent_no", 0),
	(assign, ":do_it", 0),
	(try_begin),
	 	(agent_get_horse, ":mount", "$fplayer_agent_no"),
		(eq, ":mount", -1), ##be sure player isn't currently mounted
		(agent_get_slot, ":horse", "$fplayer_agent_no", slot_agent_horse),
		(gt, ":horse", 0),
		(agent_play_sound, "$fplayer_agent_no", sound_whistle),
		(display_message,"@You whistle for your horse."),
		(assign, ":do_it", 1),
		(agent_is_active, ":horse"), 
		(agent_is_alive, ":horse"),
		(agent_get_position, pos1, "$fplayer_agent_no"),
		(agent_set_scripted_destination, ":horse", pos1, 0),
	(else_try),
		(ge, ":mount", 0),
		(agent_is_active, ":mount"), 
		(agent_is_alive, ":mount"),
		(agent_set_animation, ":mount", "anim_horse_rear"),
		(assign, ":do_it", 1),
	(try_end),
	(eq, ":do_it", 1),
   ],[])
   
shield_bash = ( #in pbod_common_triggers 
   0, 0, 1, 
   [
	(game_key_is_down, gk_defend),
	(key_clicked, "$key_special_bash"),
	(neg|main_hero_fallen),
	(ge, "$fplayer_agent_no", 0),
	(call_script, "script_cf_shield_bash"),
   ],[]) 
   
## WINDYPLAINS+ ## - AI Shield Bashing
shield_bash_ai = ( #in pbod_common_triggers 
   0.5, 0, 1, 
   [
	(try_for_agents, ":agent_no"),
		(get_player_agent_no, ":agent_player"),
		(neq, ":agent_no", ":agent_player"),
		(agent_is_human, ":agent_no"),		
		(agent_is_alive,":agent_no"),
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		(agent_slot_eq, ":agent_no", slot_agent_shield_bash_cooldown, 0), # Prevent constant shield bash attempts.
		(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SHIELD_BASHER),
		# Filter (attacker) - Not currently involved in a bash attempt.
		(agent_get_animation, ":anim", ":agent_no", 0),
		(neq, ":anim", "anim_shield_bash"),
		# Filter (attacker) - Not mounted.
		(agent_get_horse, ":horse", ":agent_no"),
		(eq, ":horse", -1),
		# Filter (attacker) - Wielding a shield.
		(agent_get_wielded_item, ":shield_item", ":agent_no", 1),
		(gt, ":shield_item", itm_no_item),
		(item_get_type, ":type", ":shield_item"),
		(eq, ":type", itp_type_shield),
		# Filter (attacker) - Shield of appropriate size.
		(item_get_shield_width, ":shield_width", ":shield_item"), #WSE
		(item_get_shield_height, ":shield_height", ":shield_item"), #WSE
		(this_or_next|ge, ":shield_height", 50),
		(ge, ":shield_width", 50),
		
		(agent_get_position, pos1, ":agent_no"),
		(position_move_y, pos1, 75),#75 cm directly ahead, so it's not a cuboid space around player center
		(assign, ":victim", -1),
		(assign, ":closest_dist", 100), #100 cm / 1m
		(assign, ":fp_closest_dist", 1), #1 meter
		(try_for_agents,":agent_nearby", pos1, ":fp_closest_dist"),
			(neq, ":agent_nearby", ":agent_no"),
			(neg|agent_is_ally,":agent_nearby"),#don't bash allies
			(agent_is_human, ":agent_nearby"),#stop if not human			
			(agent_is_alive,":agent_nearby"),	
			(agent_get_horse, ":horse", ":agent_nearby"),
			(eq, ":horse", -1),		
			
			(agent_get_position, pos2, ":agent_nearby"),
			(neg|position_is_behind_position, pos2, pos1),
			(get_distance_between_positions,":dist", pos1, pos2),
			(le, ":dist", ":closest_dist"),				
			(assign, ":victim", ":agent_nearby"),
			(assign, ":closest_dist", ":dist"),
		(try_end),
		
		### DIAGNOSTIC+ ###
		# (try_begin),
			# (agent_get_troop_id, ":troop_no", ":agent_no"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (ge, ":victim", 0),
			# (agent_get_troop_id, ":troop_victim", ":victim"),
			# (str_store_troop_name, s32, ":troop_victim"),
			# (assign, reg31, 0),
			# (try_begin),
				# (neg|agent_is_ally,":victim"),#don't bash allies
				# (assign, reg31, 1),
			# (try_end),
			# (display_message, "@DEBUG (PBOD): {s31} attempts a shield bash against their {reg31?ENEMY:ALLY} {s32}.", gpu_debug),
			
			# (try_begin),
				# (eq, reg31, 0), # victim was an ally.
				# (assign, reg32, 0),
				# (try_begin),
					# (agent_get_team, ":team_attacker", ":agent_no"),
					# (agent_get_team, ":team_victim", ":victim"),
					# (eq, ":team_attacker", ":team_victim"),
					# (assign, reg32, 1),
				# (try_end),
				# (display_message, "@DEBUG (PBOD): Team check would {reg31?have:NOT have} prevented this.", gpu_debug),
			# (try_end),
			
		# (try_end),
		### DIAGNOSTIC- ###
		
		## TROOP ABILITY: BONUS_STEADY_FOOTING - Allows an AI to deliver damage with a shield bash attack.
		(try_begin),
			(ge, ":victim", 0),
			(agent_set_slot, ":agent_no", slot_agent_shield_bash_cooldown, AI_SHIELD_BASH_COOLDOWN),
			(agent_get_troop_id, ":troop_attacker", ":agent_no"),
			(store_attribute_level, ":STR_attacker", ":troop_attacker", ca_strength),
			(agent_get_troop_id, ":troop_victim", ":victim"),
			(store_attribute_level, ":STR", ":troop_victim", ca_strength),
			(store_sub, ":STR_difference", ":STR", ":STR_attacker"),
			(val_mul, ":STR_difference", 2),
			(assign, ":resist_chance", 0),
			(val_add, ":resist_chance", ":STR_difference"),
			(val_min, ":resist_chance", 15),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_victim", BONUS_STEADY_FOOTING),
			(val_mul, ":STR", 3),
			(val_add, ":resist_chance", 40),
			(val_add, ":resist_chance", ":STR"),
			# (agent_get_troop_id, ":troop_victim", ":victim"),
			# (call_script, "script_cf_ce_troop_has_ability", ":troop_victim", BONUS_STEADY_FOOTING),
			# (store_attribute_level, ":resist_chance", ":troop_victim", ca_strength),
			# (val_mul, ":resist_chance", 3),
			# (val_add, ":resist_chance", 40),
			(store_random_in_range, ":roll", 0, 100),
			(lt, ":roll", ":resist_chance"),
			(assign, ":victim", -1),
			(try_begin),
				(get_player_agent_no, ":agent_player"),
				(eq, ":victim", ":agent_player"),
				(str_store_troop_name, s1, ":troop_no"),
				(display_message, "@You shrug off {s1}'s attempt to shield bash you.", gpu_green),
			(try_end),
			## DIAGNOSTIC+ ##
			# (str_store_troop_name, s31, ":troop_no"),
			# (str_store_troop_name, s32, ":troop_victim"),
			# (assign, reg31, ":roll"),
			# (assign, reg32, ":resist_chance"),
			# (display_message, "@DEBUG (shield bash): {s32} has resisted {s31}'s shield bash attempt. {reg31} < {reg32}", gpu_debug),
			## DIAGNOSTIC- ##
		(try_end),
		
		## Check for valid victim and then process a shield bash.
		(try_begin),
			(ge, ":victim", 0),
			(agent_set_animation, ":agent_no","anim_shield_bash"),
			## Shield Bash - Attacker
			(agent_get_troop_id, ":id", ":agent_no"),
			(troop_get_type, ":type", ":id"),
			(try_begin),
				(eq, ":type", tf_male),
				(agent_play_sound, ":agent_no", "snd_man_yell"),
			(else_try),
				(agent_play_sound, ":agent_no", "snd_woman_yell"),		
			(try_end),
			## Shield Bash - Victim
			(agent_play_sound, ":agent_no", "snd_wooden_hit_low_armor_high_damage"),				
			(agent_set_animation, ":victim", "anim_shield_strike"),
			## TROOP ABILITY: BONUS_SAVAGE_BASH - Allows an AI to deliver damage with a shield bash attack.
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_SAVAGE_BASH),
				(store_attribute_level, ":STR", ":troop_no", ca_strength),
				(store_skill_level, ":skill_shield", "skl_shield", ":troop_no"),
				(store_add, ":damage", ":STR", ":skill_shield"),
				(val_mul, ":damage", 2),
				(agent_deliver_damage_to_agent, ":agent_no", ":victim", ":damage", "itm_practice_sword"),
			(try_end),
		(try_end),
	(try_end),
   ],[]) 
   
shield_bash_ai_cooldown = ( #in pbod_common_triggers 
   1, 0, 0, 
   [
	(try_for_agents, ":agent_no"),
		(agent_get_slot, ":cooldown", ":agent_no", slot_agent_shield_bash_cooldown),
		(try_begin),
			## FILTER - Catch any odd data in agent cooldown slot.
			(neg|is_between, ":cooldown", 0, AI_SHIELD_BASH_COOLDOWN+1),
			(assign, ":cooldown", 1),
		(try_end),
		(ge, ":cooldown", 1),
		(val_sub, ":cooldown", 1),
		(agent_set_slot, ":agent_no", slot_agent_shield_bash_cooldown, ":cooldown"),
		## DIAGNOSTIC+ ##
		# (agent_get_troop_id, ":troop_no", ":agent_no"),
		# (str_store_troop_name, s31, ":troop_no"),
		# (assign, reg31, ":cooldown"),
		# (store_sub, reg32, reg31, 1),
		# (display_message, "@DEBUG (shield bash): {s31}'s shield bash cooldown is now {reg31} second{reg32?s:}", gpu_debug),
		# (eq, ":cooldown", 0),
		# (display_message, "@DEBUG (shield bash): {s31}'s shield bash cooldown is now RESET.", gpu_green),
		## DIAGNOSTIC- ##
	(try_end),
   ],[])
## WINDYPLAINS- ##

deploy_pavise = ( #in pbod_common_triggers  #also fire arrows
   0, 0, 1, 
   [
    (key_clicked, "$key_special_pavise"),
	(neg|main_hero_fallen),
	(ge, "$fplayer_agent_no", 0),
	(assign, ":do_it", 0),
	(try_begin),
		(agent_get_slot, ":fire", "$fplayer_agent_no", slot_agent_player_firearrows),
		(val_sub, ":fire", 1),
		(val_abs, ":fire"),
		(call_script, "script_cf_agent_set_firearrow", "$fplayer_agent_no", ":fire"),
		(agent_set_slot, "$fplayer_agent_no", slot_agent_player_firearrows, ":fire"),
		(assign, ":do_it", 1),
	(else_try),
		(call_script, "script_cf_agent_deploy_pavise", "$fplayer_agent_no"),
		(assign, ":do_it", 1),
	(else_try),
		(call_script, "script_cf_agent_recover_pavise", "$fplayer_agent_no"),
		(assign, ":do_it", 1),
	(try_end),
	(eq, ":do_it", 1),
   ],[])
#Pavise
##Crouching code, credit dunde; minor edits Caba
player_crouch = ( #in pbod_common_triggers #also cheer
   0, 0, 2,
   [
    (key_clicked,"$key_special_crouch"),
	(neg|main_hero_fallen),
	(ge, "$fplayer_agent_no", 0),
	(assign, ":do_it", 0),
	(try_begin),
		(agent_get_slot, ":crouch", "$fplayer_agent_no", slot_agent_crouching),
		(val_clamp, ":crouch", 0, 2),
		(val_sub, ":crouch", 1),
		(val_abs, ":crouch"),
		(this_or_next|eq, ":crouch", 0),
		(eq, "$g_battle_result", 0), #battle NOT over
		(call_script, "script_cf_agent_set_crouching", "$fplayer_agent_no", ":crouch"),
		(try_begin),
			(eq, ":crouch", 1),
			(team_set_slot, 0, slot_team_mv_crouching, 1),
		(else_try), #crouch =0
			(call_script, "script_cf_order_active_check", slot_team_d0_order_crouch), #slot set there
		(try_end),
		(assign, ":do_it", 1),
	(try_end),
	(try_begin),
		(neq, "$g_battle_result", 0), #battle is over
		(agent_set_animation, "$fplayer_agent_no", "anim_cheer", 1),
		(assign, ":do_it", 1),
	## WINDYPLAINS+ ## - COMPILER_FIX (missing try_end)
	# (else_try),
	(try_end),
	## WINDYPLAINS- ##
	(eq, ":do_it", 1),	
   ], [])

process_crouching = ( #in pbod_common_triggers
   0, 0, 0, [(team_slot_eq, 0, slot_team_mv_crouching, 1)],
   [
    (set_fixed_point_multiplier, 100),
	(try_for_agents, ":agent"),
		(agent_is_alive, ":agent"),
		(agent_is_human, ":agent"),
		(agent_get_slot, ":crouching", ":agent", slot_agent_crouching),
		(gt, ":crouching", 0),
		(agent_get_horse, reg0, ":agent"),
		(le, reg0, 0),
		(assign, ":forced_to_stand", 0),
		(agent_get_wielded_item, ":weapon", ":agent", 0),
		(try_begin),
			(le, ":weapon", itm_no_item),     
		(else_try),   
			(item_get_type, ":weapon_type", ":weapon"),     
			(eq, ":weapon_type", itp_type_crossbow),
			(agent_get_attack_action, ":action", ":agent"), 
			(try_begin),
				(eq, ":action", 5), # Loading Crossbow always standing
				(assign, ":forced_to_stand", 1),
			(else_try),
				(this_or_next|eq, ":action", 1), 
				(eq, ":action", 2),
				(agent_slot_ge, ":agent", slot_agent_deployed_pavise, 1),
				(call_script, "script_cf_agent_is_behind_pavise", ":agent"), #"spr_pavise_shield1"),
				(assign, ":forced_to_stand", 1),
			(try_end),
		(else_try),
			#(eq, ":weapon", itm_long_bow),                    # Attacking with Longbow always standing
			(eq, ":weapon_type", itp_type_bow),
			(item_has_capability, ":weapon", itcf_carry_bow_back), #bow large enough to be on back, not case as proxy for longbow ??
			(agent_get_attack_action, ":action", ":agent"),
			(this_or_next|eq, ":action", 1), 
			(eq, ":action", 2),
			(assign, ":forced_to_stand", 1),        
		(try_end),
		(agent_get_speed, pos6, ":agent"),
		(position_get_y,":speed",pos6), 
		(store_mul, ":speed2", ":speed",2), 
		(val_abs, ":speed2"),
		(position_get_x,":drift",pos6), 
		(assign, ":abs_drift", ":drift"), 
		(val_abs, ":abs_drift"), 
		(try_begin),
			(eq,":forced_to_stand", 1),
			(try_begin),
				(agent_get_animation, ":anim", ":agent",0),
				(eq, ":anim", "anim_stand_to_crouch"),
				(agent_set_animation, ":agent", "anim_crouch_to_low"),
				(agent_set_slot, ":agent", slot_agent_crouching, 3),
			(try_end),
		(else_try),
			(this_or_next|eq, ":abs_drift", 0),
			(lt, ":abs_drift", ":speed2"),
			(try_begin),        
				(eq, ":speed", 0),
				(try_begin),
					(eq, ":crouching", 3),
					(agent_set_animation, ":agent", "anim_stand_to_crouch"),
					(agent_set_slot, ":agent", slot_agent_crouching, 1),
				(try_end),  
			(else_try),
				(eq, ":crouching", 1),
				(agent_set_animation, ":agent", "anim_crouch_to_low"),
				(agent_set_slot, ":agent", slot_agent_crouching, 2),
			(else_try), 
				(agent_set_slot, ":agent", slot_agent_crouching, 3),     
				(is_between, ":speed", 1, 200),     
				(agent_set_animation, ":agent", "anim_walk_forward_crouch"),
			(else_try),
				(is_between, ":speed", -200, 0),     
				(agent_set_animation, ":agent", "anim_walk_backward_crouch"),
			(try_end),
		(else_try),
			(lt, ":abs_drift", 200),
			(agent_set_slot, ":agent", slot_agent_crouching, 3),
			(try_begin),
				(gt, ":drift", 0),
				(agent_set_animation, ":agent", "anim_walk_right_crouch"),
			(else_try),
				(agent_set_animation, ":agent", "anim_walk_left_crouch"),         
			(try_end),  
		(try_end),
	(try_end), 
   ])

pbod_common_triggers = [
  init_player_global_variables,
  horse_whistle,
  shield_bash,
  ## WINDYPLAINS+ ## - Support added for AI shield bashing.
  shield_bash_ai,
  shield_bash_ai_cooldown,
  ## WINDYPLAINS- ##
  deploy_pavise,
  player_crouch,
  process_crouching,
 ] 

fix_maintain_division_triggers = [    #Fix for setting divisions, duplicated in formations code, so disabled in mst_lead_charge, quick_battle_battle
  (ti_on_agent_spawn, 0, 0, [], [(store_trigger_param_1, ":agent"),(call_script, "script_prebattle_agent_fix_division", ":agent")]),
  (0.5, 0, 0, [(store_mission_timer_a, reg0),(gt, reg0, 4)], 
   [
    (try_for_agents, ":agent"),
		(agent_is_alive, ":agent"),
		(agent_slot_ge, ":agent", slot_agent_new_division, 0),
	    (agent_get_division, ":division", ":agent"),
		(neg|agent_slot_eq, ":agent", slot_agent_new_division, ":division"),
		(agent_get_slot, ":division", ":agent", slot_agent_new_division),
		(agent_set_division, ":agent", ":division"),
	(try_end),   
   ]), 
 ]

real_deployment_triggers = [
 (0, 0.8, ti_once, [(mission_cam_set_screen_color, 0xFF000000)],
   [
	(mission_cam_animate_to_screen_color, 0x00000000, 1000),
	(neg|is_vanilla_warband),
	(party_slot_eq, "p_main_party", slot_party_pref_real_deployment, 2),
	(assign, "$battle_phase", BP_Spawn),
	(try_begin),
		(neg|camera_in_first_person), #WSE bugfixing
		(assign, "$cam_mode", cam_mode_follow),
		(assign, "$g_camera_z", 600),
		(assign, "$g_camera_y", -1000),
		(assign, "$g_camera_x", 0),
		(mission_cam_set_mode, 1),
	(try_end),
	(call_script, "script_init_key_config"), #necessary for the way I've set up the key system
	(game_key_get_key, reg0, gk_action),
	(call_script, "script_str_store_key_name", s49, reg0),
	(game_key_get_key, reg0, gk_order_1),
	(call_script, "script_str_store_key_name", s48, reg0),

	#Tactics-Based number of orders
	(try_begin),
		(eq, "$g_is_quick_battle", 1),
		(assign, reg0, 5),
	(else_try),
		(store_skill_level, reg0, "skl_tactics", "trp_player"),
	(try_end),
	(val_mul, reg0, 2),
	(val_max, reg0, 2),

	(team_set_slot, 6, slot_team_mv_temp_placement_counter, reg0),
	(party_set_slot, "p_main_party", slot_party_pref_real_deployment, 1), #reset to standard preference on

	(tutorial_message_set_size, 20, 20),
	(tutorial_message_set_position, 500, 250),
	(tutorial_message_set_center_justify, 1),
	(tutorial_message_set_background, 1),
	(tutorial_message, "str_real_deployment_start", 0xFFFFFFFF, 20),
   ]),
 (0, 1.3, ti_once, [(neg|is_vanilla_warband),(party_slot_eq, "p_main_party", slot_party_pref_real_deployment, 2)], #activated by "Take the Field" or "Enough Planning"
   [
    (assign, "$battle_phase", BP_Spawn),
	(mission_cam_set_screen_color, 0x00000000),	
	## WINDYPLAINS+ ## - Altered to see if the player cheat mode setting is being broken by the original design.
	# (options_get_cheat_mode, reg0), 
	# (team_set_slot, 5, slot_team_mv_temp_cheatmode, reg0), #so player's cheat mode setting is preserved
	# (options_set_cheat_mode, 1),
	# (options_get_cheat_mode, "$config_cheatmode"),
	(options_get_cheat_mode, reg31), ## DIAGNOSTIC ##
	(options_set_cheat_mode, 1),
	## DIAGNOSTIC+ ##
	(try_begin),
		(ge, BETA_TESTING_MODE, 2),
		(options_get_cheat_mode, reg32),
		(display_message, "@DEBUG (BT-2): Cheat mode changed from {reg31?ENABLED:Disabled} to {reg32?ENABLED:Disabled}.", gpu_debug),
		(assign, reg33, "$config_cheatmode"),
		(display_message, "@DEBUG (BT-2): Requested cheat mode = {reg33?ENABLED:Disabled}.", gpu_debug),
	(try_end),
	## DIAGNOSTIC- ##
	## WINDYPLAINS- ##
	
	(set_fixed_point_multiplier, 1000),
	(party_get_slot, reg0, "p_main_party", slot_party_pref_rdep_time_scale),
	(try_begin),
		(eq, reg0, 1),		
		(mission_set_time_speed, 5),
	(else_try),
		(eq, reg0, 2),
		(mission_set_time_speed, 10),
	(else_try),
		(mission_set_time_speed, 1),
	(try_end),
    #(stop_time, 1),
	
	(set_fixed_point_multiplier, 100),
	(call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
   ]),
 
 #(0, 0, 0, [(eq, "$battle_phase", BP_Spawn),(game_key_clicked, gk_order_1),(stop_time, 0)],[]), ##still won't allow division assignments to change :/
 (0, 0, 0, [(eq, "$battle_phase", BP_Spawn),(game_key_released, gk_order_1), #hold down-F1 flag released
 	(team_slot_ge, 4, slot_team_mv_gk_order_hold_over_there, 1),
	(team_set_slot, 4, slot_team_mv_gk_order_hold_over_there, 0),
	(team_slot_ge, 6, slot_team_mv_temp_placement_counter, 1), ## Error Check to be sure placements remain
	], 
   [
    #(stop_time, 1),
	(set_fixed_point_multiplier, 100),
	(assign, ":num_bgroups", 0),
	(try_for_range, ":division", 0, 9),
		(class_is_listening_order, "$fplayer_team_no", ":division"),
		(store_add, ":slot", slot_team_d0_size, ":division"),
		(team_slot_ge, "$fplayer_team_no", ":slot", 1),
		(team_get_order_position, pos1, "$fplayer_team_no", ":division"),
		(val_add, ":num_bgroups", 1),
	(try_end),		
	(gt, ":num_bgroups", 0),
	
	(copy_position, Target_Pos, pos1),	#kludge around team_get_order_position rotation problems
	#Limit Range
	(try_begin),
		(eq, "$g_is_quick_battle", 1),
		(assign, reg0, 5),
	(else_try),
		(store_skill_level, reg0, "skl_tactics", "trp_player"),
	(try_end),
	(store_mul, ":pos_limit", reg0, 1000),    
	(store_mul, ":neg_limit", ":pos_limit", -1),
	(agent_get_position, Temp_Pos, "$fplayer_agent_no"),
	(position_transform_position_to_local, Target_Pos, Temp_Pos, Target_Pos),
	(position_get_x, reg0, Target_Pos),
	(val_clamp, reg0, ":neg_limit", ":pos_limit"),
	(position_set_x, Target_Pos, reg0),
	(position_get_y, reg0, Target_Pos),
	(val_mul, ":neg_limit", 10), #OK to position backwards much farther
	(val_clamp, reg0, ":neg_limit", ":pos_limit"), 	
	(position_set_y, Target_Pos, reg0),
	(position_transform_position_to_parent, Target_Pos, Temp_Pos, Target_Pos),
	#Limit Range - end
	(call_script, "script_point_y_toward_position", Target_Pos, Enemy_Team_Pos),
	
	#place player divisions -- use the formation system to set agents' scripted_destination (hopefully this works)
	(try_for_range, ":division", 0, 9),
		(class_is_listening_order, "$fplayer_team_no", ":division"),
		(store_add, ":slot", slot_team_d0_size, ":division"),
		(team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
		(gt, ":troop_count", 0),
		(store_add, ":slot", slot_team_d0_formation, ":division"),
		(team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),
		(call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", Target_Pos),
		(store_add, ":slot", slot_team_d0_formation_space, ":division"),
		(team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
		(try_begin),
			(eq, ":fformation", formation_none),
			(try_begin),
				(lt, ":div_spacing", 0), #ordered stand_closer at least once
				(assign, ":fformation", formation_ranks),
				(assign, ":sd_type", sdt_archer), #so uses archer stagger
			(try_end),
			(val_add, ":div_spacing", formation_start_spread_out),
		(try_end),
		(store_add, ":slot", slot_team_d0_type, ":division"),
		(team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),			
		(try_begin),
			(this_or_next|eq, ":fformation", formation_none),
			(eq, ":sd_type", sdt_archer),
			(call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
			(val_mul, reg0, -1), #test - archer fix
			(assign, ":script", "script_form_archers"),
		(else_try),
			(this_or_next|eq, ":sd_type", sdt_cavalry),
			(eq, ":sd_type", sdt_harcher),
			(call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
			(assign, ":script", "script_form_cavalry"),
		(else_try),
			(call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
			(assign, ":script", "script_form_infantry"),	
		(try_end),	
		(position_move_x, Target_Pos, reg0),
		(copy_position, pos1, Target_Pos),
		(call_script, ":script", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":fformation"),		
		(store_add, ":slot", slot_team_d0_move_order, ":division"),
		(team_set_slot, "$fplayer_team_no", ":slot", mordr_hold),
	(try_end), #division loop
	
    (call_script, "script_prebattle_agents_set_start_positions", "$fplayer_team_no"),
	
	
	(team_get_slot, reg0, 6, slot_team_mv_temp_placement_counter),
	(val_sub, reg0, 1),
	(team_set_slot, 6, slot_team_mv_temp_placement_counter, reg0),
	(store_sub, reg1, reg0, 1), #for the plural/singular 's'
	(tutorial_message_set_size, 20, 20),
	(tutorial_message_set_position, 500, 160),
	(tutorial_message_set_center_justify, 1),
	(tutorial_message_set_background, 1),
	(tutorial_message, "str_real_deployment_inprogress"),	
   ]),
 #End  
 (0, 0, ti_once, [(eq, "$battle_phase", BP_Spawn),(this_or_next|game_key_clicked, gk_action),(neg|team_slot_ge, 6, slot_team_mv_temp_placement_counter, 1),
   	(try_begin),
		(this_or_next|game_key_clicked, gk_action),
		(team_slot_eq, 6, slot_team_mv_temp_placement_counter, 0), #first run
		(get_time, reg0), #WSE
		(val_mul, reg0, -1),
		(team_set_slot, 6, slot_team_mv_temp_placement_counter, reg0),
	
		(tutorial_message_set_size, 25, 25),
		(tutorial_message_set_position, 500, 207),
		(tutorial_message_set_center_justify, 1),
		(tutorial_message_set_background, 1),
		(tutorial_message, "str_real_deployment_end", 0xFFFFFFFF, 2),
		
		(try_begin),
			(eq, "$cam_mode", cam_mode_follow),
			(neg|camera_in_first_person), #WSE #bugfix?
			(agent_get_look_position, cam_position, "$cam_current_agent"),
			(party_get_slot, reg0, "p_main_party", slot_party_pref_rdep_time_scale),
            (try_begin),
				(eq, reg0, 1),
				(mission_cam_animate_to_position, cam_position, 15, 1),
			(else_try),
				(eq, reg0, 2),
				(mission_cam_animate_to_position, cam_position, 30, 1),
			(else_try),
				(mission_cam_animate_to_position, cam_position, 3, 1),
			(try_end),
		(try_end),
		(assign, "$cam_mode", cam_mode_default),
	(try_end),
	(get_time, reg0), #WSE
	(team_get_slot, reg1, 6, slot_team_mv_temp_placement_counter),
	(val_add, reg0, reg1), #val_add not val_sub, since reg1 is negative
	(ge, reg0, 2), #2 real-time seconds for variable mission speeds
	],  #delay of .00075 okish too   0.0005
   [
	(team_set_slot, 2, slot_team_mv_gk_order, 0),
	(team_set_slot, 4, slot_team_mv_gk_order_hold_over_there, 0),
	(close_order_menu), #WSE
	
	(assign, "$battle_phase", BP_Setup),
    #(stop_time, 0),
    (set_fixed_point_multiplier, 10),
	(mission_set_time_speed, 10),
	## WINDYPLAINS+ ## - Altered to see if the player cheat mode setting is being broken by the original design.
	# (team_get_slot, reg0, 5, slot_team_mv_temp_cheatmode), #so player's cheat mode setting is preserved
	# (options_set_cheat_mode, reg0),
	(try_begin),
		(options_get_cheat_mode, ":cheat_setting"),
		
		## DIAGNOSTIC+ ##
		(try_begin),
			(ge, BETA_TESTING_MODE, 2),
			(display_message, "@DEBUG (BT-2): Attempting to restore your original cheat settings.", gpu_debug),
			(options_get_cheat_mode, reg31),
			(assign, reg33, "$config_cheatmode"),
			(display_message, "@DEBUG (BT-2): Requested cheat mode = {reg33?ENABLED:Disabled}.", gpu_debug),
		(try_end),
		## DIAGNOSTIC- ##
		
		(neq, ":cheat_setting", "$config_cheatmode"),
		(options_set_cheat_mode, "$config_cheatmode"),
		
		## DIAGNOSTIC+ ##
		(try_begin),
			(ge, BETA_TESTING_MODE, 2),
			(assign, reg32, "$config_cheatmode"),
			(display_message, "@DEBUG (cheats): Cheat mode changed from {reg31?ENABLED:Disabled} to {reg32?ENABLED:Disabled}.", gpu_debug),
		(try_end),
		## DIAGNOSTIC- ##
	(try_end),
	## WINDYPLAINS- ##
	#(dialog_box, "str_real_deployment_end", "@Deploy Your Forces"),	
	#(assign, "$cam_mode", cam_mode_default),
	(mission_cam_set_mode, 0),
   ]),
 ]

split_troop_division_triggers = [
 (0, 0.5, ti_once, [(party_slot_eq, "p_main_party", slot_party_prebattle_customized_divisions, 1)], [  #was ti_after_mission_start, 0, 0 ...better to distance from spawning
	(call_script, "script_prebattle_split_troop_divisions"),
   ]),
 (1, 0, 0, [(party_slot_eq, "p_main_party", slot_party_prebattle_customized_divisions, 1)], [
    (try_begin),
		(this_or_next|eq, "$fplayer_team_no", 0),
		(eq, "$fplayer_team_no", 2),
		(assign, ":reinforcement_stage", "$defender_reinforcement_stage"),
	(else_try),
		(assign, ":reinforcement_stage", "$attacker_reinforcement_stage"),
	(try_end),
	(neg|team_slot_eq, 1, slot_team_mv_reinforcement_stage, ":reinforcement_stage"),
	
	(call_script, "script_prebattle_split_troop_divisions"),
	
	(team_set_slot, 1, slot_team_mv_reinforcement_stage, ":reinforcement_stage"),
   ]),
 ]
		
prebattle_deployment_triggers  = [
 (ti_before_mission_start, 0, 0, [(party_slot_eq, "p_main_party", slot_party_prebattle_customized_deployment, 1)], [
	(try_begin),
		(eq, pbod_debug, 1),
		(call_script, "script_prebattle_print_party_to_s0", "p_main_party"),
	(try_end),
	#Store XP and stack order to maintain
	(party_get_num_companion_stacks, ":num_of_stacks", "p_main_party"),
	(try_for_range, ":i", 1, ":num_of_stacks"), #skip player
		(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i"),
		(troop_set_slot, ":troop_id", slot_troop_prebattle_stack_number, ":i"), #maintain prior stack order
		(neg|troop_is_hero, ":troop_id"),
		(call_script, "script_party_stack_get_xp", 0, "p_main_party", ":i"),
		(troop_set_slot, ":troop_id", slot_troop_prebattle_stack_xp, reg0),
	(try_end),
	
	#Copy party to know who to restore
	(call_script, "script_party_copy", "p_temp_party", "p_main_party"),	
	
    #REMOVE 'EXTRA' SOLDIERS FROM THE PARTY, TO ENSURE CORRECT SPAWN
	(troop_set_slot, "trp_player", slot_troop_prebattle_first_round, 1),
	(val_add, ":num_of_stacks", 1),
	(try_for_range_backwards, ":i", 0, ":num_of_stacks"),
		(party_stack_get_troop_id, ":troop_id", "p_main_party", ":i"),
		(troop_get_slot, ":num_of_agents", ":troop_id", slot_troop_prebattle_first_round),
		(party_stack_get_size, ":stack_size", "p_main_party", ":i"),
		(store_sub, ":difference", ":stack_size", ":num_of_agents"),
		(gt, ":difference", 0),
	    (party_remove_members_wounded_first, "p_main_party", ":troop_id", ":difference"),
	(try_end),
	(try_begin),
		(eq, pbod_debug, 1),
		(call_script, "script_prebattle_print_party_to_s0", "p_main_party"),
	(try_end),
    ]),
	
 (ti_after_mission_start, 0, 0, [(party_slot_eq, "p_main_party", slot_party_prebattle_customized_deployment, 1)], [
    #Add people back to the party 
	(party_get_num_companion_stacks, ":starting_num_of_stacks", "p_main_party"),
	(party_get_num_companion_stacks, ":target_num_of_stacks", "p_temp_party"),
	(try_for_range, ":i", 0, ":target_num_of_stacks"),
		(party_stack_get_troop_id, ":target_stack_troop", "p_temp_party", ":i"),
		(neq, ":target_stack_troop", "trp_player"),
		(party_stack_get_size, ":target_stack_size", "p_temp_party", ":i"),		

		(assign, ":cur_stack_size", 0),
		(assign, ":cur_num_wounded", 0),
		(call_script, "script_party_get_members_stack_no", 0, "p_main_party", ":target_stack_troop"),
        (assign, ":stack_no", reg0),
		(try_begin),
			(neq, ":stack_no", -1), #stack no was found
			(party_stack_get_size, ":cur_stack_size", "p_main_party", ":stack_no"),
			(party_stack_get_num_wounded, ":cur_num_wounded", "p_main_party", ":stack_no"),
		(try_end),
		
        (store_sub, ":difference", ":target_stack_size", ":cur_stack_size"),
		(gt, ":difference", 0),
		(party_add_members, "p_main_party", ":target_stack_troop", ":difference"),
		(try_begin), #wounded
            (party_stack_get_num_wounded, ":target_num_wounded", "p_temp_party", ":i"),
		    (val_sub, ":target_num_wounded", ":cur_num_wounded"),
		    (gt, ":target_num_wounded", 0),
            (party_wound_members, "p_main_party", ":target_stack_troop", ":target_num_wounded"),
		(try_end),
		
		#Re-apply XP
		(neg|troop_is_hero, ":target_stack_troop"),
		(troop_get_slot, ":prior_xp", ":target_stack_troop", slot_troop_prebattle_stack_xp),
		(gt, ":prior_xp", 0),
		(call_script, "script_party_restore_members_xp", "p_main_party", ":target_stack_troop", ":prior_xp"),
	(try_end), #Backup party stack loop
	(party_set_slot, "p_main_party", slot_party_prebattle_customized_deployment, ":starting_num_of_stacks"), #was 0
	(try_begin),
		(eq, pbod_debug, 1),
		(call_script, "script_prebattle_print_party_to_s0", "p_main_party"),
	(try_end),
    ]),
 ] + split_troop_division_triggers

prebattle_orders_triggers = [
 (0, 0.6, ti_once, [(party_slot_ge, "p_main_party", slot_party_prebattle_num_orders, 1)], [ #was ti_once, adjusted to conditions failure to work around engine problems
		(party_get_slot, ":num_of_orders", "p_main_party", slot_party_prebattle_num_orders),
		(party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 0), #fix test
		(set_show_messages, 0),	 
		(assign, ":delay_count", 0),
		(assign, ":start_position", 0), #real deployment/positioning
		(try_for_range, ":i", 0, ":num_of_orders"),    
		    (store_add, ":ith_order_slot", ":i", slot_party_prebattle_order_array_begin),
            (party_get_slot, ":order_index", "p_main_party", ":ith_order_slot"),
			(ge, ":order_index", 10), 
			
			#Take 3 digit order index and get component parts: group, type, order
			(store_div, ":ith_order_group", ":order_index", 100),
			(store_mul, ":ith_order_type", ":ith_order_group", 100),
			(val_sub, ":order_index", ":ith_order_type"),
			(store_div, ":ith_order_type", ":order_index", 10),
			(store_mul, ":ith_order", ":ith_order_type", 10),
			(store_sub, ":ith_order", ":order_index", ":ith_order"),

			#Turn type and order into Native order
			(assign, ":delay_order", 0),
			(try_begin),
			    (eq, ":ith_order_type", 1), #Start Position: hold, follow, charge; mordr_ 0-2; 3=11 stand ground
				(eq, ":ith_order", 3), 
				(assign, ":ith_order", 11), #Stand Ground
			(else_try),
			    (eq, ":ith_order_type", 2), #Other movement orders: mordr_ 3-8, 
				(is_between, ":ith_order", 5, 9), #5 - 8; Forward/Back 10 Paces, Stand Closer/Spread Out
				(assign, ":delay_order", 1), #To fix bugs with these orders, and to accomodate formations
				(val_add, ":delay_count", 1), #they are delayed 1-2 seconds
			(else_try), 
			    (eq, ":ith_order_type", 3), #Native Weapon Use orders: mordr_ 9,10,12,13
				(try_begin),
				    (eq, ":ith_order", 0),
					(assign, ":ith_order", 10), #Use Any Weapon
				(else_try),
				    (eq, ":ith_order", 2),
					(assign, ":ith_order", 12), #Hold Fire
				(else_try),
				    (eq, ":ith_order", 3),
					(assign, ":ith_order", 13), #Fire at Will
				(try_end),
			(else_try),
			    (eq, ":ith_order_type", 4), #Formations
				(set_show_messages, 0),
				(assign, "$battle_phase", BP_Spawn), #real deployment/positioning
				(call_script, "script_player_attempt_formation", ":ith_order_group", ":ith_order", 0),
				(assign, ":start_position", 1), #real deployment/positioning
			(else_try),
				(is_between, ":ith_order_type", 5, 7), #5 or 6; Caba Weapon and Shield orders
				(val_add, ":delay_count", 1), #To fix bugs with these orders, they are delayed 1-2 seconds
			(else_try),
			    (eq, ":ith_order_type", 7), #Caba Skirmish
				(eq, ":ith_order", 1), #Begin Skirmish, any other value would be an error			
				(team_set_order_listener, "$fplayer_team_no", ":ith_order_group"),
				(call_script, "script_order_skirmish_begin_end", "$fplayer_team_no", begin),
				(team_set_order_listener, "$fplayer_team_no", -1),
			(try_end),
            (try_begin),
			    (is_between, ":ith_order_type", 1, 4),
				(neq, ":delay_order", 1),
				(team_give_order, "$fplayer_team_no", ":ith_order_group", ":ith_order"),
				(eq, ":ith_order_type", 1),
				(try_for_range, ":division", 0, 9),
					(this_or_next|eq, ":ith_order_group", grc_everyone),
					(eq, ":ith_order_group", ":division"),
					(store_add, ":slot", slot_team_d0_size, ":division"),
					(team_slot_ge, "$fplayer_team_no", ":slot", 1),
					(store_add, ":slot", slot_team_d0_move_order, ":division"),
					(team_set_slot, "$fplayer_team_no", ":slot", ":ith_order"),
				(try_end),
			(try_end),			
		(try_end), #End Order Slot Loop	
        (team_set_order_listener, "$fplayer_team_no", grc_everyone), #Reset	
        (set_show_messages, 1),
		(display_message, "@Everyone, you know what to do. To your positions!", 0xFFDDDD66),
		(try_begin),
		    (eq, ":num_of_orders", 1),
			(party_get_slot, ":first_order", "p_main_party_backup", slot_party_prebattle_order_array_begin),
			(party_set_slot, "p_main_party", slot_party_prebattle_order_array_begin, ":first_order"),
			(party_set_slot, "p_main_party_backup", slot_party_prebattle_order_array_begin, 0),
		(try_end),	
        # (try_begin),
            # (eq, ":delay_count", 0),
            # (party_set_slot, "p_main_party", slot_party_prebattle_num_orders, 0),
		# (try_end),
		(try_begin),
			(eq, ":delay_count", 0), #deal with formations if no +/-10 paces orders are given
			(eq, ":start_position", 1),
			(call_script, "script_prebattle_agents_set_start_positions", "$fplayer_team_no"),
		(try_end),
		(assign, "$battle_phase", BP_Setup), #real deployment/positioning
	]),
	
 (0, 1, ti_once, [(party_slot_ge, "p_main_party_backup", slot_party_prebattle_num_orders, 1)], [ #was ti_once, adjusted to conditions failure to work around engine problems
		#To fix bugs with Move Forward/Back 10 Paces and Caba Weapon orders
		#these orders are applied separately, after other orders
		(set_show_messages, 0),	 
		
		(party_get_slot, ":num_of_orders", "p_main_party_backup", slot_party_prebattle_num_orders), #change to _backup, fix test
		(party_set_slot, "p_main_party_backup", slot_party_prebattle_num_orders, 0), #change to _backup, fix test
		(try_for_range, ":i", 0, ":num_of_orders"),    
		    (store_add, ":ith_order_slot", ":i", slot_party_prebattle_order_array_begin),
            (party_get_slot, ":order_index", "p_main_party", ":ith_order_slot"),
			(ge, ":order_index", 10), 

			#Take 3 digit order index and get component parts: group, type, order
			(store_div, ":ith_order_group", ":order_index", 100),
			(store_mul, ":ith_order_type", ":ith_order_group", 100),
			(val_sub, ":order_index", ":ith_order_type"),
			(store_div, ":ith_order_type", ":order_index", 10),
			(this_or_next|is_between, ":ith_order_type", 5, 7), # 5 or 6; Caba Weapon and Shield orders
			(eq, ":ith_order_type", 2), #Movement Orders
			(store_mul, ":ith_order", ":ith_order_type", 10),
			(store_sub, ":ith_order", ":order_index", ":ith_order"),
			
			(try_begin), 
                (eq, ":ith_order_type", 2),	 #set slots for execution below		
                (is_between, ":ith_order", 5, 9), #5 - 8; Forward/Back 10 Paces, Stand Closer/Spread Out	
			    # (store_add, ":slot", slot_team_d0_formation, ":ith_order_group"),
				# (team_get_slot, ":formation", "$fplayer_team_no", ":slot"),
				(store_add, ":ith_repeat_slot", ":ith_order_slot", 70), #30 for partial version
			    (party_get_slot, ":num_repeats", "p_main_party", ":ith_repeat_slot"),
			    (val_max, ":num_repeats", 1),
			    #(try_for_range, ":unused", 0, ":num_repeats"),
				(try_begin),
					# (set_show_messages, 0),	
					# (team_give_order, "$fplayer_team_no", ":ith_order_group", ":ith_order"),
				    # (team_set_order_listener, "$fplayer_team_no", ":ith_order_group"),
				    # (call_script, "script_player_order_formations", ":ith_order"),
				    # (team_set_order_listener, "$fplayer_team_no", -1), #Reset					
					(is_between, ":ith_order", 5, 7), #+/-10 paces
					# (store_add, ":slot", slot_team_d0_move_order, ":ith_order_group"),
					# (team_get_slot, ":prev_order", "$fplayer_team_no", ":slot"),	
					# (team_set_slot, "$fplayer_team_no", ":slot", ":ith_order"),	
											
					# (try_begin),
						# (store_add, ":slot", slot_team_d0_formation, ":ith_order_group"),
						# (neg|team_slot_eq, "$fplayer_team_no", ":slot", formation_none),
						(call_script, "script_formation_current_position", pos63, "$fplayer_team_no", ":ith_order_group"),
					# (else_try),
						# (agent_get_position, pos63, "$fplayer_agent_no"),
						# (call_script, "script_get_formation_destination", pos0, "$fplayer_team_no", ":ith_order_group"),
						# (position_copy_rotation, pos63, pos0),
					# (try_end),
					(call_script, "script_set_formation_destination", "$fplayer_team_no", ":ith_order_group", pos63),
					(try_begin),
						(eq, ":ith_order", mordr_advance),
						(assign, ":ith_order", 1),
					(else_try),
						(assign, ":ith_order", -1),
					(try_end),
					(val_mul, ":ith_order", ":num_repeats"),
					(call_script, "script_formation_move_position", "$fplayer_team_no", ":ith_order_group", pos63, ":ith_order"),
				(else_try), #Closer/spread out
					(store_add, ":slot", slot_team_d0_formation_space, ":ith_order_group"),
					(team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
					(try_begin),
						(eq, ":ith_order", mordr_stand_closer),
						(val_mul, ":num_repeats", -1),
					(try_end),
					(val_add, ":div_spacing", ":num_repeats"),
					(val_clamp, ":div_spacing", -3, 2), #Native formations go down to four ranks, and at most 2 spread out
					(team_set_slot, "$fplayer_team_no", ":slot", ":div_spacing"),
			    (try_end),
			(else_try),
			    (is_between, ":ith_order_type", 5, 7), #5 or 6; Caba Weapon and Shield orders
				(team_set_order_listener, "$fplayer_team_no", ":ith_order_group"),
				(call_script, "script_order_weapon_type_switch", "$fplayer_team_no", ":ith_order"),
				(team_set_order_listener, "$fplayer_team_no", -1), #Reset
			(try_end),	
		(try_end),		
        (team_set_order_listener, "$fplayer_team_no", grc_everyone), #Reset			
        		
		#place player divisions -- use the formation system to set agents' scripted_destination (hopefully this works)
		(set_fixed_point_multiplier, 100),
		(call_script, "script_team_get_position_of_enemies", Enemy_Team_Pos, "$fplayer_team_no", grc_everyone),
		(try_for_range, ":division", 0, 9),
			(store_add, ":slot", slot_team_d0_size, ":division"),
			(team_get_slot, ":troop_count", "$fplayer_team_no", ":slot"),
			(gt, ":troop_count", 0),
			(team_get_order_position, Target_Pos, "$fplayer_team_no", ":division"),
			(position_get_x, reg0, Target_Pos),
			(convert_from_fixed_point, reg0),
			(store_add, ":slot", slot_team_d0_formation_space, ":division"),
			(team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
			(this_or_next|neq, reg0, 20), #some reason the initial order position is always (20, 20); if this isn't the position there should be a +/-10 order
			(neq, ":div_spacing", 0), #theres a stand closer/spread out order
			(store_add, ":slot", slot_team_d0_formation, ":division"),
			(team_get_slot, ":fformation", "$fplayer_team_no", ":slot"),
			(try_begin),
			    (eq, ":fformation", formation_none),
				(eq, reg0, 20), #correct order position from (20,20) for spacing-only fixes
				(call_script, "script_formation_current_position", Target_Pos, "$fplayer_team_no", ":division"),
			(try_end),
			(call_script, "script_point_y_toward_position", Target_Pos, Enemy_Team_Pos),
			(call_script, "script_set_formation_destination", "$fplayer_team_no", ":division", Target_Pos),
			(try_begin),
				(eq, ":fformation", formation_none),
				(try_begin),
					(lt, ":div_spacing", 0), #ordered stand_closer at least once
					(assign, ":fformation", formation_ranks),
					(assign, ":sd_type", sdt_archer), #so uses archer stagger
				(try_end),
				(val_add, ":div_spacing", formation_start_spread_out),
			(try_end),
			(store_add, ":slot", slot_team_d0_type, ":division"),
			(team_get_slot, ":sd_type", "$fplayer_team_no", ":slot"),			
			(try_begin),
				(this_or_next|eq, ":fformation", formation_none),
				(eq, ":sd_type", sdt_archer),
				(call_script, "script_get_centering_amount", formation_default, ":troop_count", ":div_spacing"),
				(val_mul, reg0, -1), #test - archer fix
				(assign, ":script", "script_form_archers"),
			(else_try),
				(this_or_next|eq, ":sd_type", sdt_cavalry),
				(eq, ":sd_type", sdt_harcher),
				(call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
				(assign, ":script", "script_form_cavalry"),
			(else_try),
				(call_script, "script_get_centering_amount", ":fformation", ":troop_count", ":div_spacing"),
				(assign, ":script", "script_form_infantry"),	
			(try_end),	
			(position_move_x, Target_Pos, reg0),
			(copy_position, pos1, Target_Pos),
			(assign, "$battle_phase", BP_Spawn), #real deployment/positioning
			(call_script, ":script", "$fplayer_team_no", ":division", "$fplayer_agent_no", ":div_spacing", ":fformation"),		
			
			#for post-positioning business, so the spread out/stand closer orders apply in the re-arranging
			(store_add, ":slot", slot_team_d0_formation, ":division"),
			(team_slot_eq, "$fplayer_team_no", ":slot", formation_none),
			(store_add, ":slot", slot_team_d0_formation_space, ":division"),
			(team_get_slot, ":div_spacing", "$fplayer_team_no", ":slot"),
			(neq, ":div_spacing", 0),
			(assign, ":start", 0),
			(assign, ":end", 0),
			(try_begin),
				(lt, ":div_spacing", 0),
				(assign, ":start", ":div_spacing"),
			(else_try),
				(assign, ":end", ":div_spacing"),
			(try_end),
			(try_for_range, ":unused", ":start", ":end"),
				(lt, ":div_spacing", 0),
				(team_give_order, "$fplayer_team_no", ":division", mordr_stand_closer),
			(else_try),
				(team_give_order, "$fplayer_team_no", ":division", mordr_spread_out),
			(try_end),		
		(try_end), #division loop
		(call_script, "script_prebattle_agents_set_start_positions", "$fplayer_team_no"), #set position based on scripted destination
		(assign, "$battle_phase", BP_Setup), #real deployment/positioning
		
		(set_show_messages, 1),
	]),
 ] + real_deployment_triggers

caba_order_triggers = [
    (0, 0, 0, [
        (this_or_next|game_key_clicked, gk_group0_hear),
        (this_or_next|game_key_clicked, gk_group1_hear),
        (this_or_next|game_key_clicked, gk_group2_hear),
        (this_or_next|game_key_clicked, gk_group3_hear),
        (this_or_next|game_key_clicked, gk_group4_hear),
        (this_or_next|game_key_clicked, gk_group5_hear),
        (this_or_next|game_key_clicked, gk_group6_hear),
        (this_or_next|game_key_clicked, gk_group7_hear),
        (this_or_next|game_key_clicked, gk_group8_hear),
        (this_or_next|game_key_clicked, gk_everyone_hear),
		(this_or_next|game_key_clicked, gk_reverse_order_group), 
		(game_key_clicked, gk_everyone_around_hear),
		(neg|main_hero_fallen)
	], [
		(team_set_slot, 2, slot_team_mv_gk_order, 0),
        (start_presentation, "prsnt_caba_order_display"),
    ]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_1),(neg|main_hero_fallen)], [
		(try_begin),
			#(team_slot_eq, 2, slot_team_mv_gk_order, 0),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_1),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),
			(team_set_slot, 2, slot_team_mv_gk_order, gk_order_1),
			(team_set_slot, 4, slot_team_mv_gk_order_hold_over_there, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_1),	#HOLD		
			(call_script, "script_player_order_formations", mordr_hold),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
			(team_set_slot, 4, slot_team_mv_gk_order_hold_over_there, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),	#ADVANCE
			(call_script, "script_player_order_formations", mordr_advance),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),	#HOLD FIRE
			(call_script, "script_order_volley_begin_end", "$fplayer_team_no", end),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(try_end),
	]),
	
	(0, 0, 0, [(order_flag_is_active),(team_slot_eq, 4, slot_team_mv_gk_order_hold_over_there, 0)], [
		(team_set_slot, 4, slot_team_mv_gk_order_hold_over_there, 1),
		(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(game_key_is_down, gk_action),
		(team_set_slot, 4, slot_team_mv_gk_order_hold_over_there, 2),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_2),(neg|main_hero_fallen)], [
		(try_begin),
			#(team_slot_eq, 2, slot_team_mv_gk_order, 0),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_1),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),
			(team_set_slot, 2, slot_team_mv_gk_order, gk_order_2),
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_1),	#FOLLOW
			(call_script, "script_player_order_formations", mordr_follow),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),	#FALL BACK
			(call_script, "script_player_order_formations", mordr_fall_back),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),	#FIRE AT WILL
			(call_script, "script_order_volley_begin_end", "$fplayer_team_no", end),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_3),(neg|main_hero_fallen)], [
		(try_begin),
			#(team_slot_eq, 2, slot_team_mv_gk_order, 0),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_1),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),
			(neg|team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),
			(team_set_slot, 2, slot_team_mv_gk_order, gk_order_3),
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_1),	#CHARGE
			(call_script, "script_player_order_formations", mordr_charge),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),	#SPREAD OUT
			(call_script, "script_player_order_formations", mordr_spread_out),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),	#BLUNT WEAPONS
			(call_script, "script_order_set_team_slot", "$fplayer_team_no", clear),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_4),(neg|main_hero_fallen)], [
		(try_begin),
			(team_slot_eq, 2, slot_team_mv_gk_order, 0),
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
			(team_set_slot, 2, slot_team_mv_gk_order, gk_order_4),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_1),	#STAND GROUND
			(call_script, "script_player_order_formations", mordr_stand_ground),			
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),	#STAND CLOSER
			(call_script, "script_player_order_formations", mordr_stand_closer),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),	#ANY WEAPON
			(call_script, "script_order_set_team_slot", "$fplayer_team_no", clear),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_4),	#FORMATION - RANKS	
			(call_script, "script_division_reset_places"), ## CABA - check this new script
			(agent_get_position, pos49, "$fplayer_agent_no"),
			(try_for_range, ":division", 0, 9),
			    (class_is_listening_order, "$fplayer_team_no", ":division"),
				(store_add, ":slot", slot_team_d0_target_team, ":division"),
				(team_set_slot, "$fplayer_team_no", ":slot", -1),
				(store_add, ":slot", slot_team_d0_size, ":division"),
				(team_slot_ge, "$fplayer_team_no", ":slot", 1),
				(store_add, ":slot", slot_team_d0_fclock, ":division"),
				(team_set_slot, "$fplayer_team_no", ":slot", 1),
				
				#Fake out at position
				(call_script, "script_battlegroup_get_position", Temp_Pos, "$fplayer_team_no", ":division"),
				(agent_set_position, "$fplayer_agent_no", Temp_Pos),
				(call_script, "script_player_attempt_formation", ":division", formation_ranks, 1),				
			(try_end),
			(agent_set_position, "$fplayer_agent_no", pos49),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, "$key_order_7"),	#End Special Order
			(call_script, "script_order_end_active_order", "$fplayer_team_no"),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),  
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_5),(neg|main_hero_fallen)], [
		(try_begin),
			(team_slot_eq, 2, slot_team_mv_gk_order, 0),
			(team_set_slot, 2, slot_team_mv_gk_order, gk_order_5),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_1),	#RETREAT
			(call_script, "script_player_order_formations", mordr_retreat),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),	#MOUNT
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),	#Volley
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
			(call_script, "script_order_set_display_text", "str_order_volley_start"),
			(call_script, "script_order_volley_begin_end", "$fplayer_team_no", begin, volley_type_mass),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),  
		(else_try),
		    (team_slot_eq, 2, slot_team_mv_gk_order, gk_order_4), #FORMATION - SHIELDWALL
			(call_script, "script_division_reset_places"),
			(agent_get_position, pos49, "$fplayer_agent_no"),
			(try_for_range, ":division", 0, 9),
			    (class_is_listening_order, "$fplayer_team_no", ":division"),
				(store_add, ":slot", slot_team_d0_target_team, ":division"),
				(team_set_slot, "$fplayer_team_no", ":slot", -1),
				(store_add, ":slot", slot_team_d0_size, ":division"),
				(team_slot_ge, "$fplayer_team_no", ":slot", 1),
				(store_add, ":slot", slot_team_d0_fclock, ":division"),
				(team_set_slot, "$fplayer_team_no", ":slot", 1),
				
				#Fake out at position
				(call_script, "script_battlegroup_get_position", Temp_Pos, "$fplayer_team_no", ":division"),
				(agent_set_position, "$fplayer_agent_no", Temp_Pos),
				(call_script, "script_player_attempt_formation", ":division", formation_shield, 1),				
			(try_end),
			(agent_set_position, "$fplayer_agent_no", pos49),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_5),	#One-Hander
			(call_script, "script_order_set_display_text", "str_order_wpt_onehand"),
			(call_script, "script_order_weapon_type_switch", "$fplayer_team_no", onehand),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),		
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_6),	#Shield
			(call_script, "script_order_set_display_text", "str_order_wpt_use_shield"),
			(call_script, "script_order_weapon_type_switch", "$fplayer_team_no", shield),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, "$key_order_7"),	#Begin Skirmish
			(call_script, "script_order_set_display_text", "str_order_skirmish_start"),
			(call_script, "script_order_skirmish_begin_end", "$fplayer_team_no", begin),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),    
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, "$key_order_8"),	#Ignite Arrows
			(call_script, "script_order_set_display_text", "str_order_firearrow_start"),
			(call_script, "script_order_firearrow_begin_end", "$fplayer_team_no", begin),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),    
		(try_end),
	]),
	
	(0, 0, 0, [(game_key_clicked, gk_order_6),(neg|main_hero_fallen)], [
	    (try_begin),
			(team_slot_eq, 2, slot_team_mv_gk_order, 0),
			(team_set_slot, 2, slot_team_mv_gk_order, gk_order_6),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
		    (team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2),	#DISMOUNT
		    (call_script, "script_player_order_formations", mordr_dismount),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),	#Volley by Rank
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
			(call_script, "script_order_set_display_text", "str_order_volley_rank_start"),
			(call_script, "script_order_volley_begin_end", "$fplayer_team_no", begin, volley_type_rank),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),  
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_4), #FORMATION - WEDGE
			(call_script, "script_division_reset_places"),
			(agent_get_position, pos49, "$fplayer_agent_no"),
			(try_for_range, ":division", 0, 9),
			    (class_is_listening_order, "$fplayer_team_no", ":division"),
				(store_add, ":slot", slot_team_d0_target_team, ":division"),
				(team_set_slot, "$fplayer_team_no", ":slot", -1),
				(store_add, ":slot", slot_team_d0_size, ":division"),
				(team_slot_ge, "$fplayer_team_no", ":slot", 1),
				(store_add, ":slot", slot_team_d0_fclock, ":division"),
				(team_set_slot, "$fplayer_team_no", ":slot", 1),
				
				#Fake out at position
				(call_script, "script_battlegroup_get_position", Temp_Pos, "$fplayer_team_no", ":division"),
				(agent_set_position, "$fplayer_agent_no", Temp_Pos),
				(call_script, "script_player_attempt_formation", ":division", formation_wedge, 1),				
			(try_end),
			(agent_set_position, "$fplayer_agent_no", pos49),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_5),	#Two-Handers
			(call_script, "script_order_set_display_text", "str_order_wpt_twohands"),
			(call_script, "script_order_weapon_type_switch", "$fplayer_team_no", twohands),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_6),	#No Shield
			(call_script, "script_order_set_display_text", "str_order_wpt_no_shield"),
			(call_script, "script_order_weapon_type_switch", "$fplayer_team_no", noshield),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, "$key_order_7"),	#Deploy Pavise
			(call_script, "script_order_set_display_text", "str_order_pavise_start"),
			(call_script, "script_order_deploy_pavise_begin_end", "$fplayer_team_no", begin),
		    (team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, "$key_order_8"),	#Extinguish Arrows
			(call_script, "script_order_set_display_text", "str_order_firearrow_end"),
			(call_script, "script_order_firearrow_begin_end", "$fplayer_team_no", end),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),    			
		(try_end),
	]),

    (0, 0, 0, [(key_clicked, "$key_order_7"),(neg|main_hero_fallen)], [ #f7
	    (try_begin),
		    (team_slot_eq, 2, slot_team_mv_gk_order, 0), 
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
		    (team_set_slot, 2, slot_team_mv_gk_order, "$key_order_7"),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2), #Add Rank
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
			(call_script, "script_order_set_display_text", "str_order_num_ranks_add"),			
			(try_for_range, ":division", 0, 9),
				(class_is_listening_order, "$fplayer_team_no", ":division"),
				(store_add, ":slot", slot_team_d0_size, ":division"),
				(team_slot_ge, "$fplayer_team_no", ":slot", 1),
				(call_script, "script_formation_change_num_ranks", "$fplayer_team_no", ":division", 1),
			(try_end),
			(team_set_slot, 2, slot_team_mv_gk_order, 0), 
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_3),	#Volley by Platoon
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
			(call_script, "script_order_set_display_text", "str_order_volley_platoon_start"),
			(call_script, "script_order_volley_begin_end", "$fplayer_team_no", begin, volley_type_platoon),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),  			
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_4), #FORMATION - SQUARE
			(call_script, "script_division_reset_places"),
			(agent_get_position, pos49, "$fplayer_agent_no"),
			(try_for_range, ":division", 0, 9),
				(class_is_listening_order, "$fplayer_team_no", ":division"),
				(store_add, ":slot", slot_team_d0_target_team, ":division"),
				(team_set_slot, "$fplayer_team_no", ":slot", -1),
				(store_add, ":slot", slot_team_d0_size, ":division"),
				(team_slot_ge, "$fplayer_team_no", ":slot", 1),
				(store_add, ":slot", slot_team_d0_fclock, ":division"),
				(team_set_slot, "$fplayer_team_no", ":slot", 1),
				
				#Fake out at position
				(call_script, "script_battlegroup_get_position", Temp_Pos, "$fplayer_team_no", ":division"),
				(agent_set_position, "$fplayer_agent_no", Temp_Pos),
				(call_script, "script_player_attempt_formation", ":division", formation_square, 1),				
			(try_end),
			(agent_set_position, "$fplayer_agent_no", pos49),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_5),	#Polearms
			(call_script, "script_order_set_display_text", "str_order_wpt_polearm"),
			(call_script, "script_order_weapon_type_switch", "$fplayer_team_no", polearm),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_6),	#Free Shield
			(call_script, "script_order_set_display_text", "str_order_wpt_free_shield"),
			(call_script, "script_order_set_team_slot", "$fplayer_team_no", free),
			#(call_script, "script_order_weapon_type_switch", "$fplayer_team_no", free),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, "$key_order_7"),	#Brace Spear
			(call_script, "script_order_set_display_text", "str_order_brace_start"),
			(call_script, "script_order_sp_brace_begin_end", "$fplayer_team_no", begin),
			(team_set_slot, 2, slot_team_mv_gk_order, 0), 
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, "$key_order_8"),	#Crouch
			(call_script, "script_order_set_display_text", "str_order_crouch_start"),
			(call_script, "script_order_crouch_begin_end", "$fplayer_team_no", begin),
			(team_set_slot, 2, slot_team_mv_gk_order, 0), 			
		(try_end),
	]),
		
    (0, 0, 0, [(key_clicked, "$key_order_8"),(neg|main_hero_fallen)], [ #F8
	    (try_begin),
		    (team_slot_eq, 2, slot_team_mv_gk_order, 0), 
		    (team_set_slot, 2, slot_team_mv_gk_order, "$key_order_8"),
            (start_presentation, "prsnt_caba_order_display"),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_2), #Remove Rank
			(store_cur_mission_template_no, reg0),(this_or_next|eq, reg0, "mt_lead_charge"),(eq, reg0, "mt_quick_battle_battle"),
			(call_script, "script_order_set_display_text", "str_order_num_ranks_remove"),					
			(try_for_range, ":division", 0, 9),
				(class_is_listening_order, "$fplayer_team_no", ":division"),
				(store_add, ":slot", slot_team_d0_size, ":division"),
				(team_slot_ge, "$fplayer_team_no", ":slot", 1),
				(call_script, "script_formation_change_num_ranks", "$fplayer_team_no", ":division", -1),
			(try_end),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),  
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_4), #FORMATION - CANCEL
			(call_script, "script_player_order_formations", mordr_charge),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, gk_order_5), #Ranged
			(call_script, "script_order_set_display_text", "str_order_wpt_ranged"),
		    (call_script, "script_order_weapon_type_switch", "$fplayer_team_no", ranged),
		    (team_set_slot, 2, slot_team_mv_gk_order, 0),
		(else_try),
			(team_slot_eq, 2, slot_team_mv_gk_order, "$key_order_8"),	#Crouch - Stand
			(call_script, "script_order_set_display_text", "str_order_crouch_end"),
			(call_script, "script_order_crouch_begin_end", "$fplayer_team_no", end),
			(team_set_slot, 2, slot_team_mv_gk_order, 0),  			
		(try_end),
	]),
 ]
 
field_ai_triggers = [
  init_scene_boundaries,
  (ti_on_agent_spawn, 0, 0, [], [(store_trigger_param_1, ":agent"),(call_script, "script_weapon_use_classify_agent", ":agent")]), # On spawn, mark lancers, spears, horse archers using a slot. Force lancers to equip lances, horse archers to equip bows 
  (2, 0, 0, [(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_wu_lance, 1),(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_wu_harcher, 1),(party_slot_eq, "p_main_party", slot_party_pref_wu_spear, 1),(store_mission_timer_a, reg0),(gt, reg0, 4)],
   # Check to make sure there are no lance users on foot, if so force them to
   # switch to their sword. This should also affect troops that were NEVER mounted,
   # but are still equipped with lances, such as Taiga Bandits.
   # Check horse archers ammo, and if none left, switch to sword.
   # For mounted lancers and foot spears, affect their Decision on weapon use,
   # based on if closest 3 enemies are within 5 meters and if currently attacking/defending.
   [  	   
	(try_for_agents, ":agent"), # Run through all active NPCs on the battle field.
     # Hasn't been defeated.
        (agent_is_alive, ":agent"),
		(agent_is_non_player, ":agent"),
		(assign, ":caba_weapon_order", clear), # For Caba'drin Orders
		(assign, ":shield_order", clear), # For Caba'drin Orders
		(assign, ":weapon_order", 0),
		(assign, ":fire_order", 0),
		(try_begin),
		    (agent_get_team, ":team", ":agent"),
			(eq, ":team", "$fplayer_team_no"),
			(agent_get_division, ":class", ":agent"),
			(team_get_weapon_usage_order, ":weapon_order", ":team", ":class"),
			(team_get_hold_fire_order, ":fire_order", ":team", ":class"),

			(store_add, ":slot", slot_team_d0_order_weapon, ":class"),
			(team_get_slot, ":caba_weapon_order", ":team", ":slot"),
			(store_add, ":slot", slot_team_d0_order_shield, ":class"),
			(team_get_slot, ":shield_order", ":team", ":slot"),
		(try_end),
		(neq, ":weapon_order", wordr_use_blunt_weapons), #Not ordered to use blunts
		(eq, ":caba_weapon_order", clear), # For Caba'drin orders; no active weapon order
        (try_begin),
			(party_slot_eq, "p_main_party", slot_party_pref_wu_lance, 1),
            (agent_get_slot, ":lance", ":agent", slot_agent_lance),
            (gt, ":lance", 0),  # Lancer?
     # Get wielded item.
            (agent_get_wielded_item, ":wielded", ":agent", 0),
      # They riding a horse?
            (agent_get_horse, ":horse", ":agent"),
            (try_begin),
                (le, ":horse", 0), # Isn't riding a horse.
                (agent_set_slot, ":agent", slot_agent_lance, 0), # No longer a lancer
                (eq, ":wielded", ":lance"), # Still using lance?
				(try_begin),
				    (eq, ":shield_order", 1),
					(assign, ":inc_two_handers", 0),
				(else_try),
				    (assign, ":inc_two_handers", 1),
				(try_end),
                (call_script, "script_weapon_use_backup_weapon", ":agent", ":inc_two_handers"), # Then equip a close weapon
            (else_try),
     # Still mounted
                (agent_get_position, pos1, ":agent"),    
				(assign, ":radius", 10), #10 meters
				(convert_to_fixed_point, ":radius"),
				(call_script, "script_get_closest3_distance_of_enemies_at_pos1_with_radius", ":team", ":radius"),
                (assign, ":avg_dist", reg0), # Find distance of nearest 3 enemies
				#SHOULD CLOSEST MATTER???
                (try_begin),
                    (lt, ":avg_dist", 500), # Are the enemies within 5 meters?
                    (agent_get_combat_state, ":combat", ":agent"),
                    (gt, ":combat", 3), # Agent currently in combat? ...avoids switching before contact
                    (eq, ":wielded", ":lance"), # Still using lance?
					(try_begin),
				        (eq, ":shield_order", 1),
					    (assign, ":inc_two_handers", 0),
				    (else_try),
				        (assign, ":inc_two_handers", 1),
				    (try_end),
                    (call_script, "script_weapon_use_backup_weapon", ":agent", ":inc_two_handers"), # Then equip a close weapon
                (else_try),
                    (neq, ":wielded", ":lance"), # Enemies farther than 5 meters and/or not fighting, and not using lance?
                    (agent_set_wielded_item, ":agent", ":lance"), # Then equip it!
                (try_end),
            (try_end),
        (else_try),
			(party_slot_eq, "p_main_party", slot_party_pref_wu_harcher, 1),
		    (agent_get_slot, ":bow", ":agent", slot_agent_horsebow),
            (gt, ":bow", 0),  # Horse archer?
			(neq, ":fire_order", aordr_hold_your_fire), #Not ordered to hold fire
     # Get wielded item.
            (agent_get_wielded_item, ":wielded", ":agent", 0),
      # They have ammo left?
            (agent_get_ammo, ":ammo", ":agent"),
            (try_begin),
			    (le, ":ammo", 0), # No ammo left
				(agent_set_slot, ":agent", slot_agent_horsebow, 0), # No longer a horse archer
                (eq, ":wielded", ":bow"), # Still using bow?
				(try_begin),
				    (eq, ":shield_order", 1),
					(assign, ":inc_two_handers", 0),
				(else_try),
				    (assign, ":inc_two_handers", 1),
				(try_end),
                (call_script, "script_weapon_use_backup_weapon", ":agent", ":inc_two_handers"), # Then equip a close weapon
			(else_try),
			    (gt, ":ammo", 0),
				(agent_get_horse, ":horse", ":agent"),
				(le, ":horse", 0), #No Horse, no command, let AI choose (I think)
			(else_try),
                (gt, ":ammo", 0),
				(neq, ":wielded", ":bow"), # Still have ammo, still mounted and not using bow?
                (agent_set_wielded_item, ":agent", ":bow"), # Then equip it!
			(try_end),
		(else_try),
		    (party_slot_eq, "p_main_party", slot_party_pref_wu_spear, 1),
		    (agent_get_slot, ":spear", ":agent", slot_agent_spear),   
            (gt, ":spear", 0), # Spear-Unit?   

			(store_add, ":slot", slot_team_d0_formation, ":class"),
			(team_slot_eq, ":team", ":slot", formation_none),			
			(neq, ":shield_order", 1),
			
            (agent_get_position, pos1, ":agent"), # Find distance of nearest 3 enemies
			(assign, ":radius", 10), #10 meters
	        (convert_to_fixed_point, ":radius"),
            (call_script, "script_get_closest3_distance_of_enemies_at_pos1_with_radius", ":team", ":radius"),
            (assign, ":avg_dist", reg0),
            (assign, ":closest_dist", reg1),
			(agent_get_wielded_item, ":wielded", ":agent", 0), # Get wielded
            (try_begin), #Weapon Use
                (this_or_next|lt, ":closest_dist", 300), # Closest enemy within 3 meters?
                (lt, ":avg_dist", 700), # Are the 3 enemies within an average of 7 meters?
                (agent_get_combat_state, ":combat", ":agent"),
                (gt, ":combat", 3), # Agent currently in combat? ...avoids switching before contact
                (eq, ":wielded", ":spear"), # Still using spear?
                (call_script, "script_weapon_use_backup_weapon", ":agent", 1), # Then equip a close weapon
            (else_try),
                (neq, ":wielded", ":spear"), # Enemies farther than 7 meters and/or not fighting, and not using spear?
                (agent_set_wielded_item, ":agent", ":spear"), # Then equip it!                
            (try_end),
        (try_end),
    (try_end),
    ]),
	
  (ti_on_agent_hit, 0, 0, [(party_slot_eq, "p_main_party", slot_party_pref_dmg_tweaks, 1)],
    # Horse Trample buff  
    # Pike vs Horse buff
   [
    (store_trigger_param_1, ":agent"),
	(store_trigger_param_2, ":attacker"),
	(store_trigger_param_3, ":damage"),
	(assign, ":weapon", reg0),
	
	(assign, ":orig_damage", ":damage"),
	
	(try_begin),
	    (agent_is_human, ":agent"), 
		#(agent_is_non_player, ":agent"), #Maybe remove?
	    (try_begin), #Horse Trample Buff
		    (neg|agent_is_human, ":attacker"),
            (eq, ":weapon", -1),
            (agent_get_item_id, ":horse", ":attacker"),
			(ge, ":horse", 0),
			(gt, ":orig_damage", 5),
			## WINDYPLAINS+ ## - BONUS_TIGHT_FORMATION - Troop ignores horse trample damage.
			(assign, ":ignore_damage", 0),
			(try_begin),
				(agent_get_troop_id, ":troop_victim", ":agent"),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_victim", BONUS_TIGHT_FORMATION),
				(assign, ":ignore_damage", 1),
			(try_end),
			(eq, ":ignore_damage", 0),
			## WINDYPLAINS- ##
			#(item_get_slot, ":horse_charge", ":horse", slot_item_horse_charge), #Approximation for weight
            (item_get_horse_charge_damage, ":horse_charge", ":horse"), #WSE
			(try_begin),      
                (lt, ":horse_charge", 18),
				(val_div, ":horse_charge", 3),
                (val_max, ":damage", ":horse_charge"),
            (else_try),
                (is_between, ":horse_charge", 18, 25),
				(val_div, ":horse_charge", 2),
                (val_max, ":damage", ":horse_charge"),      
            (else_try),
                (val_max, ":damage", ":horse_charge"),
            (try_end),
			(try_begin),
				(agent_get_speed, pos0, ":attacker"),
				(position_get_y, ":forward_speed", pos0),
				(position_get_x, ":lateral_speed", pos0), #Double check
				(val_max, ":forward_speed", ":lateral_speed"), #Double check
				(convert_from_fixed_point, ":forward_speed"),
				(gt, ":forward_speed", 6),
				(val_mul, ":damage", 2),
			(try_end),
        (try_end),
	(else_try), #Pike Buff
	    (neg|agent_is_human, ":agent"),
		(gt, ":weapon", 0),
		#(item_slot_ge, ":weapon", slot_item_length, 150),
		(item_get_weapon_length, reg0, ":weapon"), #WSE
		(ge, reg0, 150),
		(agent_get_horse, ":horse", ":attacker"),
		(eq, ":horse", -1),
		
		## WINDYPLAINS+ ## - TROOP EFFECT - BONUS_GRACEFUL_RIDER
		(try_begin),
			(agent_get_rider, ":agent_rider", ":agent"),
			(ge, ":agent_rider", 0),
			(agent_get_troop_id, ":troop_rider", ":agent_rider"),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_rider", BONUS_GRACEFUL_RIDER),
			(agent_get_item_id, ":item_horse", ":agent"),
			(item_get_horse_maneuver, ":maneuver", ":item_horse"),
			(store_skill_level, ":riding", "skl_riding", ":troop_rider"),
			(val_mul, ":riding", 3),
			(store_add, ":dodge_chance", ":maneuver", ":riding"),
			(store_random_in_range, ":attack_attempt", 0, 100),
			(le, ":attack_attempt", ":dodge_chance"),
			(assign, ":block_damage", 1),
			(assign, ":block_message", 1),
		(else_try),
			(assign, ":block_message", 0),
			(assign, ":block_damage", 0),
		(try_end),
		(eq, ":block_damage", 0), # Continue on.
		## WINDYPLAINS- ##
		(try_begin),
		    (agent_get_action_dir, ":direction", ":attacker"), #invalid = -1, down = 0, right = 1, left = 2, up = 3
		    (eq, ":direction", 0), #thrust	
			(val_mul, ":damage", 2),
    		(val_max, ":damage", 50), #was 120
		(else_try),
			(val_mul, ":damage", 3),
			(val_div, ":damage", 2),
		    (val_max, ":damage", 30), #was 60
		(try_end),
		## WINDYPLAINS+ ## - BONUS_TIGHT_FORMATION - Enhances pike damage effect for pikers.
		(try_begin),
			(agent_get_troop_id, ":troop_attacker", ":attacker"),
			(call_script, "script_cf_ce_troop_has_ability", ":troop_attacker", BONUS_TIGHT_FORMATION),
			(val_mul, ":damage", 125),
			(val_div, ":damage", 100),
		(try_end),
		## WINDYPLAINS- ##
		(val_max, ":damage", ":orig_damage"),

		(agent_get_speed, pos0, ":agent"),
		(position_get_y, ":forward_speed", pos0),
		(position_get_x, ":lateral_speed", pos0), #Double check
		(val_max, ":forward_speed", ":lateral_speed"), #Double check
		(convert_from_fixed_point, ":forward_speed"),
		(val_sub, ":forward_speed", 3),
		(val_clamp, ":forward_speed", -2, 4),
		(store_mul, ":speed_mod", ":forward_speed", 10), #Between -20 and +40
		(val_add, ":damage", ":speed_mod"),		

		(agent_get_item_id, ":horse", ":agent"), #New Armor damage reduction
		#(item_get_slot, ":armor", ":horse", slot_item_horse_armor),
		(item_get_body_armor, ":armor", ":horse"), #WSE
		(val_div, ":armor", 4), #Range of 2-14
		(val_sub, ":damage", ":armor"),
		
		#Horses randomly rear if they take damage
		(store_random_in_range, ":random_no", 0, 100),
		(try_begin),
		    (store_div, ":chance_mod", ":orig_damage", 5),
			(val_sub, ":random_no", ":chance_mod"),
			(val_sub, ":random_no", ":forward_speed"),
			(try_begin),
			    (gt, ":orig_damage", 5),
				(eq, ":direction", 0),
				(val_sub, ":random_no", 10),
			(try_end),
			(lt, ":random_no", 10),
			(agent_set_animation, ":agent", "anim_horse_rear"),
		(try_end),	
	(try_end), #Human v Horse
	
	(gt, ":damage", ":orig_damage"),
	(val_sub, ":damage", ":orig_damage"),
    (store_agent_hit_points, ":hitpoints" , ":agent", 1),
    (val_sub, ":hitpoints", ":damage"),
	(agent_set_hit_points, ":agent", ":hitpoints", 1),	
	
	(assign, reg2, -1),
	(agent_get_horse,":playerhorse","$fplayer_agent_no"),
	(try_begin),
		## WINDYPLAINS+ ## - Troop Effect - BONUS_GRACEFUL_RIDER - Hide message.
		(eq, ":block_message", 0),
		## WINDYPLAINS- ##
		(try_begin),
	        (eq, ":agent", ":playerhorse"),
			(assign, reg2, 0),
		(else_try),
		    (eq, ":agent", "$fplayer_agent_no"),
			(assign, reg2, 1),
		(try_end),
		(neq, reg2, -1),
	    (assign, reg1, ":damage"),		
	    (display_message, "@{reg2?You:Your mount} received {reg1} extra damage!",0xff4040),
    (else_try),
	    (try_begin),
		    (eq, ":attacker", ":playerhorse"),
			(assign, reg2, 0),
		(else_try),
		    (eq, ":attacker", "$fplayer_agent_no"),
			(assign, reg2, 1),
		(try_end),
		(neq, reg2, -1),
		(assign, reg1, ":damage"),	
		(display_message, "@{reg2?You strike:Your horse charges} for {reg1} bonus damage!"),
    (try_end),
   ]),	
  
  (ti_on_agent_dismount, 0, 0, [(party_get_slot, reg3, "p_main_party", slot_party_pref_div_dehorse),(is_between, reg3, 0, 9)], #De-Horse Trigger #Valid division 0-8
   [
	(store_trigger_param_2, ":horse"),
	(neg|agent_is_alive, ":horse"),
	
	(store_trigger_param_1, ":rider"), 
	(agent_is_alive, ":rider"),
    (agent_is_non_player, ":rider"),
	
	(agent_get_team, ":team", ":rider"),
	(agent_get_division, reg0, ":rider"),
	(store_add, ":slot", slot_team_d0_formation, reg0),
	
	(try_begin),
	    (eq, ":team", "$fplayer_team_no"),
		(agent_set_division, ":rider", reg3),
		(agent_set_slot, ":rider", slot_agent_new_division, reg3),
	(else_try),
	    (agent_set_division, ":rider", grc_infantry),
		(agent_set_slot, ":rider", slot_agent_new_division, grc_infantry),
	(try_end),
	
	(neg|team_slot_eq, ":team", ":slot", formation_none),
	(agent_clear_scripted_mode, ":rider"),
	(agent_set_speed_limit, ":rider", 100),
	(agent_set_slot, ":rider", slot_agent_formation_rank_no, 0),
	(agent_set_slot, ":rider", slot_agent_inside_formation, 0),
   ]),

  (ti_on_item_unwielded, 0, 0, [(party_get_slot, reg3, "p_main_party", slot_party_pref_div_no_ammo),(is_between, reg3, 0, 9)], #Out of Ammo Trigger #Valid division 0-8
   [
    (store_trigger_param_2, ":weapon"),
	(ge, ":weapon", 0),
	(item_get_type, ":type", ":weapon"),
	(this_or_next|eq, ":type", itp_type_bow),
	(eq, ":type", itp_type_crossbow),
	
	(store_trigger_param_1, ":agent"),
    (agent_is_alive, ":agent"),
    (agent_is_non_player, ":agent"),
	
	(agent_get_ammo, ":ammo", ":agent", 0),
	(le, ":ammo", 0),	
	(agent_get_horse, ":horse", ":agent"),
	(eq, ":horse", -1),
	
	(agent_get_team, ":team", ":agent"),
	(agent_get_division, reg0, ":agent"),
	(store_add, ":slot", slot_team_d0_formation, reg0),
	## No longer active in siege missions--re-activate this block if you call this trigger in siege missions
	# (assign, ":continue", 1),
	# (try_begin),
		# (this_or_next|party_slot_eq, "$g_encountered_party", slot_party_type, spt_town), #Sieges
		# (party_slot_eq, "$g_encountered_party", slot_party_type, spt_castle),		
		# (this_or_next|eq, ":team", "$defender_team"),
		# (eq, ":team", "$defender_team_2"),
		# (assign, ":continue", 0), #To not reassign units that will get their ammo refilled.
	# (try_end),
	# (eq, ":continue", 1),	
	
	(try_begin),
	    (eq, ":team", "$fplayer_team_no"),
		(agent_set_division, ":agent", reg3),
		(agent_set_slot, ":agent", slot_agent_new_division, reg3),
	(else_try),
	    (agent_set_division, ":agent", grc_infantry),
		(agent_set_slot, ":agent", slot_agent_new_division, grc_infantry),
	(try_end),

	(neg|team_slot_eq, ":team", ":slot", formation_none),
	(agent_clear_scripted_mode, ":agent"),
	(agent_set_speed_limit, ":agent", 100),
	(agent_set_slot, ":agent", slot_agent_formation_rank_no, 0),
	(agent_set_slot, ":agent", slot_agent_inside_formation, 0),	
   ]),
   
  (2, 0, ti_once, [(store_mission_timer_a, reg0),(gt, reg0, 2)], [ #Force Cav to Stay Mounted; Special Orders decision seeds
    (set_show_messages, 0),   
    (try_for_range, ":team", 0, 4),		
	    (store_random_in_range, reg0, 0, 3),
		(team_set_slot, ":team", slot_team_decision_seed, reg0),
		(store_random_in_range, reg0, 0, 3),
		(team_set_slot, ":team", slot_team_decision_seed_2, reg0),
		(try_for_range, ":division", 0, 9),
		    (store_add, ":slot", slot_team_d0_type, ":division"),
			(this_or_next|team_slot_eq, ":team", ":slot", sdt_cavalry),
			(team_slot_eq, ":team", ":slot", sdt_harcher),
			(team_get_riding_order, reg0, ":team", ":division"),
			(eq, reg0, rordr_free),
			(team_give_order, ":team", ":division", mordr_mount),
		(try_end),		
	(try_end),
	(set_show_messages, 1),
   ]),
  
  (1, 0, 0, [(store_mission_timer_a, reg0),(gt, reg0, 3), ###GENERAL AI TRIGGER for SPECIAL ORDERS 
		(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_spo_brace, 1),
		(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_spo_skirmish, 1),
		(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_spo_volley, 1),
		(party_slot_eq, "p_main_party", slot_party_pref_spo_pavise, 1),
	   ], [ 
		(set_fixed_point_multiplier, 100),
		(try_begin),
		    (party_slot_eq, "p_main_party", slot_party_pref_spo_brace, 1),
			(try_for_range, ":division", 0, 9), #Player auto-remove brace
				(store_add, ":slot", slot_team_d0_order_sp_brace, ":division"),
				(neg|team_slot_eq, "$fplayer_team_no", ":slot", 0), #brace active
				(call_script, "script_formation_current_position", pos2, "$fplayer_team_no", ":division"),
				(call_script, "script_get_nearest_enemy_battlegroup_current_position", pos1, "$fplayer_team_no", pos2),
				(this_or_next|lt, reg0, 325), #distance
				(position_is_behind_position,pos1,pos2),
				(team_set_order_listener, "$fplayer_team_no", ":division"),
				(call_script, "script_order_sp_brace_begin_end", "$fplayer_team_no", end),
				(team_set_order_listener, "$fplayer_team_no", -1),
			(try_end),
		(try_end),
	    (try_for_range, ":team", 0, 4), #For AI
			(neq, ":team", "$fplayer_team_no"),
			(team_slot_ge, ":team", slot_team_size, 1),
			(assign, ":mordr", -1),
			(team_get_slot, ":faction", ":team", slot_team_faction),
			(this_or_next|eq, ":faction", "fac_deserters"),
			(is_between, ":faction", kingdoms_begin, kingdoms_end),
			(try_begin), #Spear Bracing Decision-making
				(party_slot_eq, "p_main_party", slot_party_pref_spo_brace, 1),
			    (this_or_next|neg|team_slot_eq, ":team", slot_team_decision_seed, 0),
				(neg|team_slot_eq, ":team", slot_team_decision_seed_2, 0), #If both decision seeds = 0, then no special orders (0.1 prob)
				(this_or_next|eq, ":faction", "fac_player_supporters_faction"), #Player's lords can brace
				(eq, ":faction", "fac_kingdom_5"), #Rhodoks	
				(try_begin),
					(team_slot_eq, ":team", slot_team_d0_order_sp_brace, 0), #Spearbrace order not active
					(store_add, ":slot", slot_team_d0_size, grc_infantry), 
					(team_slot_ge, ":team", slot_team_d0_size, 10),
					(store_add, ":slot", slot_team_d0_weapon_length, grc_infantry),
					(team_slot_ge, ":team", ":slot", 80), #have long weapons/polearms (until bumped to a separate division)
					(store_add, ":slot", slot_team_d0_formation, grc_infantry),
					(team_get_movement_order, ":mordr", ":team", grc_infantry),
					(this_or_next|neg|team_slot_eq, ":team", ":slot", formation_none),
					(neq, ":mordr", mordr_charge), #Not Charging	
					(assign, ":num_cav", 0),
					(try_for_range, ":enemy_team", 0, 4),
						(teams_are_enemies, ":enemy_team", ":team"),
						(team_slot_ge, ":enemy_team", slot_team_size, 1),
						(team_get_slot, reg0, ":enemy_team", slot_team_num_cavalry), 
						(val_add, ":num_cav", reg0),
					(try_end),		
					(ge, ":num_cav", 5), #sufficent enemy cav to care
					(assign, ":distance", 99999),
					(call_script, "script_formation_current_position", pos2, ":team", grc_infantry),
					(call_script, "script_team_get_position_of_enemies", pos1, ":team", grc_cavalry),
					(get_distance_between_positions, ":distance", pos1, pos2),
					(is_between, ":distance", 1500, 5000), #cav distance
					(call_script, "script_get_nearest_enemy_battlegroup_current_position", pos1, ":team", pos2),
					(gt, reg0, 600), #nearest distance
					(neg|position_is_behind_position,pos1,pos2),
					#(team_set_order_listener, ":team", grc_infantry),
					(call_script, "script_non_player_team_set_order_listener", 1, grc_infantry),
					(call_script, "script_order_sp_brace_begin_end", ":team", begin),
					#(team_set_order_listener, ":team", -1),
					(call_script, "script_restore_team_order_listener"),
				(else_try), #Should only capture an eligible team that is now charging, so bracing should turn off
					(neg|team_slot_eq, ":team", slot_team_d0_order_sp_brace, 0), #Order Active
					(assign, ":end", 0),
					(try_begin),
						(assign, ":num_cav", 0),
						(try_for_range, ":enemy_team", 0, 4),
							(teams_are_enemies, ":enemy_team", ":team"),
							(team_slot_ge, ":enemy_team", slot_team_size, 1),
							(team_get_slot, reg0, ":enemy_team", slot_team_num_cavalry), 
							(val_add, ":num_cav", reg0),
						(try_end),		
						(team_get_movement_order, ":mordr", ":team", grc_infantry),
						(this_or_next|eq, ":mordr", mordr_charge),
						(lt, ":num_cav", 5),
						(assign, ":end", 1),
					(else_try),
						(store_add, ":slot", slot_team_d0_size, grc_infantry), 
						(neg|team_slot_ge, ":team", slot_team_d0_size, 10),
						(assign, ":end", 1),
					(else_try),
						(store_add, ":slot", slot_team_d0_weapon_length, grc_infantry),
						(neg|team_slot_ge, ":team", ":slot", 80), #have long weapons/polearms (until bumped to a separate division)
						(assign, ":end", 1),
					(else_try),
						(assign, ":distance", 0),
						(call_script, "script_formation_current_position", pos2, ":team", grc_infantry),
						(call_script, "script_team_get_position_of_enemies", pos1, ":team", grc_cavalry),
						(get_distance_between_positions, ":distance", pos1, pos2),
						(gt, ":distance", 6500),
						(assign, ":end", 1),
					(else_try), #after contact, end brace
						(call_script, "script_get_nearest_enemy_battlegroup_current_position", pos1, ":team", pos2),
						(this_or_next|lt, reg0, 350), #distance
						(position_is_behind_position,pos1,pos2),
						(assign, ":end", 1),
					(try_end),
					(eq, ":end", 1),
					#(team_set_order_listener, ":team", grc_infantry),
					(call_script, "script_non_player_team_set_order_listener", 1, grc_infantry),
					(call_script, "script_order_sp_brace_begin_end", ":team", end),
					#(team_set_order_listener, ":team", -1),
					(call_script, "script_restore_team_order_listener"),
				(try_end),
			(try_end), #End Spear Bracing
			(neg|team_slot_eq, ":team", slot_team_decision_seed, 0), #1/3 chance not to use
			(try_begin), #Volley/Skirmish Decision Making	
				(party_slot_eq, "p_main_party", slot_party_pref_spo_skirmish, 1),			
				(neq, ":faction", "fac_kingdom_1"), #Swadia
				(neq, ":faction", "fac_kingdom_5"), #Rhodoks...Exclude Cross-bow users
				(try_begin), #Skirmish
					(store_add, ":slot", slot_team_d0_order_skirmish, grc_archers),
					(neg|team_slot_eq, ":team", ":slot", 1), #not skirmishing
					(team_get_slot, ":num_archers", ":team", slot_team_num_archers),
					(team_get_slot, ":size", ":team", slot_team_size),
					(store_mul, reg0, ":num_archers", 100),
					(val_div, reg0, ":size"),
					(is_between, reg0, 25, 76), #25-75% archers
					(assign, ":num_enemies", 0),
					(try_for_range, ":enemy_team", 0, 4),
						(teams_are_enemies, ":enemy_team", ":team"),
						(team_get_slot, reg0, ":enemy_team", slot_team_size), 
						(val_add, ":num_enemies", reg0),
					(try_end),		
					(lt, ":num_archers", ":num_enemies"),
					#(team_set_order_listener, ":team", grc_archers),
					(call_script, "script_non_player_team_set_order_listener", 1, grc_archers),
					(call_script, "script_order_skirmish_begin_end", ":team", begin),
					#(team_set_order_listener, ":team", -1),
					(call_script, "script_restore_team_order_listener"),
				(else_try),
					(store_add, ":slot", slot_team_d0_order_skirmish, grc_archers),
					(team_slot_eq, ":team", ":slot", 1), #skirmishing
					(team_get_slot, ":num_archers", ":team", slot_team_num_archers),
					(assign, ":num_enemies", 0),
					(try_for_range, ":enemy_team", 0, 4),
						(teams_are_enemies, ":enemy_team", ":team"),
						(team_get_slot, reg0, ":enemy_team", slot_team_size), 
						(val_add, ":num_enemies", reg0),
					(try_end),	
					(team_get_slot, ":size", ":team", slot_team_size),
					(store_mul, reg0, ":num_archers", 100),
					(val_div, reg0, ":size"),
					(this_or_next|neg|is_between, reg0, 25, 76), #25-75% archers
					(gt, ":num_archers", ":num_enemies"),
					#(team_set_order_listener, ":team", grc_archers),
					(call_script, "script_non_player_team_set_order_listener", 1, grc_archers),
					(call_script, "script_order_skirmish_begin_end", ":team", end),
					#(team_set_order_listener, ":team", -1),
					(call_script, "script_restore_team_order_listener"),
				(try_end),
			(else_try),
				(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_spo_pavise, 1),
				(party_slot_eq, "p_main_party", slot_party_pref_spo_volley, 1),
				(this_or_next|eq, ":faction", "fac_kingdom_1"), #Swadia
				(eq, ":faction", "fac_kingdom_5"), #Rhodoks... Cross-bow users
				(try_begin), #Pavise/Crouch
					(party_slot_eq, "p_main_party", slot_party_pref_spo_pavise, 1),
					(eq, ":faction", "fac_kingdom_5"), #Rhodoks
					(neq, "$battle_phase", BP_Setup), #?
					(store_add, ":slot", slot_team_d0_order_pavise, grc_archers),
					(neg|team_slot_ge, ":team", ":slot", 1), #Not Deployed
					(team_get_slot, reg1, ":team", slot_team_num_archers),
					(team_get_slot, ":size", ":team", slot_team_size),
					(val_mul, reg1, 100),
					(val_div, reg1, ":size"),
					(gt, reg1, 25), #>25% archers
					(team_get_movement_order, ":mordr", ":team", grc_archers),
					(eq, ":mordr", mordr_hold),	
					(store_add, ":slot", slot_team_d0_closest_enemy_dist, grc_archers),
					(team_slot_ge, ":team", ":slot", AI_charge_distance), #don't begin to deploy if enemy is within charge distance (20m)
					#Check for Movement
					(call_script, "script_formation_current_position", pos2, ":team", grc_archers), #stores formation destination to pos0
					(position_transform_position_to_local, Temp_Pos, pos2, pos0), #pos0 from above
					(position_get_y, ":forward_behind", Temp_Pos),
					(val_abs, ":forward_behind"),
					(lt, ":forward_behind", 300),
					(store_add, ":slot", slot_team_d0_order_pavise, grc_archers),
					(team_get_slot, reg0, ":team", ":slot"),
					(val_sub, reg0, 1),
					(team_set_slot, ":team", ":slot", reg0),
					(eq, reg0, -5), #5 consecutive seconds of being about at the right position
					#(team_set_order_listener, ":team", grc_archers),
					(call_script, "script_non_player_team_set_order_listener", 1, grc_archers),
					(call_script, "script_order_deploy_pavise_begin_end", ":team", begin),
					#(team_set_order_listener, ":team", -1),
					(call_script, "script_restore_team_order_listener"),
				(else_try),
					(store_add, ":slot", slot_team_d0_order_pavise, grc_archers),
					(team_slot_ge, ":team", ":slot", 1), #Deployed
					(assign, ":end", 0),
					(try_begin),
						(team_get_movement_order, ":mordr", ":team", grc_archers),
						(neq, ":mordr", mordr_hold),	
						(assign, ":end", 1),
					(else_try), #moving  --first agent speed? current pos vs destination pos--compare relative Ys?
						(call_script, "script_formation_current_position", pos2, ":team", grc_archers), #stores formation destination to pos0
						(position_transform_position_to_local, Temp_Pos, pos2, pos0), #pos0 from above
						(position_get_y, ":forward_behind", Temp_Pos),
						(val_abs, ":forward_behind"),
						(gt, ":forward_behind", 700),
						(assign, ":end", 1),
					(else_try),
						(store_add, ":slot", slot_team_d0_closest_enemy_dist, grc_archers),
						(neg|team_slot_ge, ":team", ":slot", AI_charge_distance / 2), #within charge distance (20m)
						#(call_script, "script_formation_current_position", pos2, ":team", grc_archers),
						(call_script, "script_get_nearest_enemy_battlegroup_current_position", pos1, ":team", pos2), #pos2 from above else_try
						(position_is_behind_position, pos1, pos2), #over run
						(assign, ":end", 1),
					(try_end),					
					(eq, ":end", 1),
					#(team_set_order_listener, ":team", grc_archers),
					(call_script, "script_non_player_team_set_order_listener", 1, grc_archers),
					(call_script, "script_order_deploy_pavise_begin_end", ":team", end),
					#(team_set_order_listener, ":team", -1),
					(call_script, "script_restore_team_order_listener"),
				(try_end),
				(party_slot_eq, "p_main_party", slot_party_pref_spo_volley, 1),
				(assign, ":distance", 99999), #Volley
				(try_begin),
					(store_add, ":slot", slot_team_d0_order_volley, grc_archers),
					(neg|team_slot_ge, ":team", ":slot", 1), #Not Volleying
					(team_get_slot, reg1, ":team", slot_team_num_archers),
					(team_get_slot, ":size", ":team", slot_team_size),
					(val_mul, reg1, 100),
					(val_div, reg1, ":size"),
					(gt, reg1, 25), #>25% archers
					(team_get_movement_order, ":mordr", ":team", grc_archers),
					(neq, ":mordr", mordr_charge),	
					(call_script, "script_battlegroup_get_position", pos2, ":team", grc_archers),
					(call_script, "script_get_nearest_enemy_battlegroup_location", Temp_Pos, ":team", pos2),					
					(is_between, reg0, 1000, 7000),
					#(team_set_order_listener, ":team", grc_archers),
					(call_script, "script_non_player_team_set_order_listener", 1, grc_archers),
					(store_random_in_range, ":volley_type", volley_type_mass, volley_type_platoon + 1),
					(call_script, "script_order_volley_begin_end", ":team", begin, ":volley_type"),
					#(team_set_order_listener, ":team", -1),
					(call_script, "script_restore_team_order_listener"),
				(else_try),
					(store_add, ":slot", slot_team_d0_order_volley, grc_archers),
					(team_slot_ge, ":team", ":slot", 1),
					(assign, ":end", 0),
					(try_begin),
						(team_get_movement_order, ":mordr", ":team", grc_archers),
						(eq, ":mordr", mordr_charge),	
						(assign, ":end", 1),
					(else_try),
						(call_script, "script_battlegroup_get_position", pos2, ":team", grc_archers),
					    (call_script, "script_get_nearest_enemy_battlegroup_location", Temp_Pos, ":team", pos2),
						(neg|is_between, reg0, 1000, 8000),
						(assign, ":end", 1),
					(try_end),					
					(eq, ":end", 1),
					#(team_set_order_listener, ":team", grc_archers),
					(call_script, "script_non_player_team_set_order_listener", 1, grc_archers),
					(call_script, "script_order_volley_begin_end", ":team", end),
					#(team_set_order_listener, ":team", -1),
					(call_script, "script_restore_team_order_listener"),
				(try_end),
			(try_end), #End Skirmish/Volley
		(try_end), #Team Loop
    ]),
      
  (0.5, 0, 0, [(call_script, "script_cf_order_active_check", slot_team_d0_order_skirmish)], [(call_script, "script_order_skirmish_skirmish")]), 
 
  (1, 0, 0, [(call_script, "script_cf_order_active_check", slot_team_d0_order_volley)], [
		(try_begin), #Disable Volley @ end of battle 
			(neq, "$g_battle_result", 0),
			(try_for_range, ":team", 0, 4),
				(try_for_range, ":slot", slot_team_d0_order_volley, slot_team_d0_order_volley_counter + 9),
					(team_set_slot, ":team", ":slot", 0),
				(try_end),
			(try_end),
		(try_end),
		
		(try_for_range, ":team", 0, 4),
			(try_for_range, ":division", 0, 9),
			    (store_add, ":slot", slot_team_d0_order_volley_counter, ":division"),
				(team_slot_ge, ":team", ":slot", 1),
				(team_get_slot, ":volley_counter", ":team", ":slot"),
				(val_add, ":volley_counter", 1),
				(team_set_slot, ":team", ":slot", ":volley_counter"),
			(try_end),
		(try_end),
		
		(try_for_agents, ":agent"),
		    (agent_is_alive, ":agent"),
			(agent_is_non_player, ":agent"),
			(agent_slot_ge, ":agent", slot_agent_volley_fire, 1),
			(agent_get_ammo, ":ammo", ":agent", 1),
			(gt, ":ammo", 0),
			
			(agent_get_combat_state, ":cs", ":agent"),
			(try_begin),
				(eq, pbod_debug, 1),
				(assign, reg0, ":cs"),
				(display_message, "str_reg0"),
			(try_end),
			#(lt, ":cs", 4),(neq, ":cs", 2),
			(this_or_next|eq, ":cs", 1),
			(eq, ":cs", 3),
			
			(agent_get_team, ":team", ":agent"),
			(agent_get_division, ":division", ":agent"),
			(store_add, ":slot", slot_team_d0_order_volley, ":division"),
			(team_get_slot, ":volley_order_type", ":team", ":slot"),
			(store_add, ":slot", slot_team_d0_order_volley_counter, ":division"),
			(team_get_slot, ":volley_counter", ":team", ":slot"),
			
			(try_begin),
				(eq, ":volley_order_type", volley_type_rank),
				(store_add, ":slot", slot_team_d0_formation_num_ranks, ":division"),
				(team_get_slot, ":rank_shift", ":team", ":slot"),
				(store_mul, ":delay", ":rank_shift", volley_delay_shift),
				
				(agent_get_slot, reg0, ":agent", slot_agent_formation_rank_no),
				(ge, reg0, 1),				
				(val_sub, ":rank_shift", reg0),
				(val_mul, ":rank_shift", volley_delay_shift),
				(val_add, ":volley_counter", ":rank_shift"), ##move back to agent_slot...or leave to allow for rank re-shuffling?
			(else_try),
				(eq, ":volley_order_type", volley_type_platoon),
				(store_mul, ":delay", 3, volley_delay_shift),
				
				(agent_get_slot, reg0, ":agent", slot_agent_volley_fire),
				(val_sub, reg0, 1),
				(val_add, ":volley_counter", reg0),
			(else_try),
				(agent_get_slot, ":volley_wpn_type", ":agent", slot_agent_volley_fire),
				(eq, ":volley_wpn_type", itp_type_bow),
				(assign, ":delay", volley_delay_bow),
			(else_try),
				(eq, ":volley_wpn_type", itp_type_crossbow),
				(assign, ":delay", volley_delay_crossbow),
			(else_try),
				(eq, ":volley_wpn_type", itp_type_musket),
				(assign, ":delay", volley_delay_musket),
			(else_try),
				(assign, ":delay", -1),
			(try_end),
			(neq, ":delay", -1),
						
			(store_mod, reg0, ":volley_counter", ":delay"),
			(try_begin),
				(eq, pbod_debug, 1),
				(assign, reg1, ":volley_counter"),
				(assign, reg2, ":delay"),			
				(display_message, "@Counter {reg1}, Delay {reg2}: {reg0}"),
			(try_end),
			(try_begin),
				(eq, reg0, 0),
				(agent_set_attack_action, ":agent", 0, 0), #Fire
			(else_try),
				(agent_set_attack_action, ":agent", 0, 1), #Ready and Aim
			(try_end),
		(try_end),
     ]),
    
  ##Spearwall Kit - Edited from The Mercenary by Caba'drin  
  (0.1, 0, 0, [(call_script, "script_cf_order_active_check", slot_team_d0_order_sp_brace)], [ #spearwall_trigger_1
		(try_for_agents,":agent"),
           (agent_is_alive,":agent"),
           (agent_is_human,":agent"),
		   (agent_slot_eq, ":agent", slot_agent_is_running_away, 0),
		   (agent_slot_ge, ":agent", slot_agent_spear, 1),
		   (agent_get_wielded_item, ":weapon", ":agent", 0),
           (agent_slot_eq, ":agent", slot_agent_spear, ":weapon"),
		   (agent_get_team,":team1",":agent"),
           (agent_get_division,":class",":agent"),
		   (team_get_movement_order,":order",":team1",":class"),
		   (assign,":continue",0),
           (try_begin),
		      (neq, ":agent", "$fplayer_agent_no"),
		      (store_add, ":slot", slot_team_d0_order_sp_brace, ":class"),
			  (team_slot_eq, ":team1", ":slot", 1),
			  (this_or_next|eq,":order",mordr_hold),
              (eq,":order",mordr_stand_ground),
			  (assign, ":continue", 1),
		   (else_try),
              (eq, ":agent", "$fplayer_agent_no"), 
              (agent_slot_eq, "$fplayer_agent_no", slot_agent_player_braced, 1),
              (assign, ":continue", 1),
		   (try_end),
		   (eq, ":continue", 1),
		   (agent_get_speed, pos0, ":agent"), #New
		   (position_get_y, ":speed", pos0),
		   (position_get_x, ":speed_x", pos0),
		   (val_max, ":speed", ":speed_x"),
		   #(assign, reg0, ":speed"),
		   #(display_message, "@Speed: {reg0}"),
		   (eq, ":speed", 0),
		   (try_begin),
				(agent_get_animation, ":anim", ":agent"),				
				(item_get_weapon_length, ":spear_dist", ":weapon"), #WSE
				#Try block for proper animation--high, low, standing; w or w/o shield (hopefully?)
				(try_begin),
				    #(item_slot_eq, ":weapon", slot_item_pike, 1),
					(ge, ":spear_dist", 150),
					(assign, ":anim_bracing", "anim_spearwall_bracing_low"),
				(else_try),
				    (assign, ":anim_bracing", "anim_spearwall_bracing"),
				(try_end),
				(neq, ":anim", ":anim_bracing"),
				(agent_set_animation, ":agent", ":anim_bracing"),
				(agent_get_position, pos1, ":agent"), ##lessens some spinning
				(agent_set_scripted_destination, ":agent", pos1), ##lessens some spinning
				# (agent_get_look_position, pos1, ":agent"),
				# (position_get_x, ":x", pos1),
				# (position_get_y, ":y", pos1),
				# (agent_set_slot, ":agent", slot_agent_target_x_pos, ":x"),
				# (agent_set_slot, ":agent", slot_agent_target_y_pos, ":y"),
				(agent_set_slot, ":agent", slot_agent_spearwall, 0), #Begin count with animation resetting
		   (try_end),
		   #(eq, ":continue", 1),
		   (agent_get_slot,":speartimer",":agent",slot_agent_spearwall),
           (try_begin),
                (lt,":speartimer",20),
                (val_add,":speartimer",1),
                (agent_set_slot,":agent",slot_agent_spearwall,":speartimer"),
           (try_end),
		   (agent_set_is_alarmed, ":agent", 0), ##lessens some spinning
		   # (agent_get_slot, ":x", ":agent", slot_agent_target_x_pos),
		   # (agent_get_slot, ":y", ":agent", slot_agent_target_y_pos),
		   # (init_position, pos2),
		   # (position_set_x, pos2, ":x"),
		   # (position_set_y, pos2, ":y"),
		   # (agent_set_look_target_position, ":agent", pos2),
           (ge,":speartimer",20),
		   #(item_get_slot, ":spear_dist", ":weapon", slot_item_length), #done above
           (assign, ":dist_to_beat", ":spear_dist"),
           (assign,":victim",-1),
		   (assign, ":vic_rider", -1),
           (agent_get_position,pos1,":agent"),
		   #(convert_to_fixed_point, ":spear_dist"),
           (try_for_agents, ":possible_victim", pos1, ":spear_dist"),
              (agent_is_alive,":possible_victim"),
              (neg|agent_is_human,":possible_victim"),
              (agent_get_rider,":rider",":possible_victim"),
              (ge,":rider",0),
              (agent_get_team,":team2",":rider"),
              (teams_are_enemies,":team1",":team2"),
              (agent_get_position,pos2,":possible_victim"),
              (get_distance_between_positions,":dist",pos1,pos2),
              (lt,":dist",":dist_to_beat"), #CABA
              (neg|position_is_behind_position,pos2,pos1),
			  (get_angle_between_positions, ":angle", pos1, pos2), #CABA
			  (val_abs, ":angle"), #CABA
			  (convert_from_fixed_point, ":angle"), #CABA
              (is_between, ":angle", 165, 181),  #30 degrees... have to be facing one another		  			  
			  (agent_get_speed, pos0, ":possible_victim"), #CABA
              (position_get_y, ":speed", pos0), #CABA
			  (position_get_x, ":speed_x", pos0), #CABA - just be be sure
			  (val_max, ":speed", ":speed_x"), #CABA - just to be sure
              (ge, ":speed", 300), #CABA at least half speed; full speed horse 800-1100, was 400
              (assign, ":dist_to_beat", ":dist"), #CABA ...now it will progressively find the closest target
              (assign,":victim",":possible_victim"), #CABA
			  (assign,":vic_rider", ":rider"),
           (try_end),
           (gt,":victim",-1),
		  # (display_message, "@Brace should hit"),
           (agent_set_animation, ":agent", "anim_spearwall_bracing_recoil"),
		   (agent_set_slot, ":agent", slot_agent_spearwall, 0),
           (agent_play_sound,":victim","snd_metal_hit_high_armor_high_damage"),
           (store_agent_hit_points,":hp",":victim",0), #This stores as a %
           (store_agent_hit_points,":oldhp",":victim",1), #This stores as absoulte # - Pre-Damage
           (val_div,":speed",6), # Orig 2; Remember to change this if the timing on speed checks changes
           (val_sub,":speed",10), #CABA - w/speed div by 8-10, a speed over 900 will be an instant-kill. Might want to change divisor to 10?
           (try_begin), #Pike Bonus Damage
			  #(item_slot_eq, ":weapon", slot_item_pike, 1),
			  (ge, ":spear_dist", 150),
			  (val_add, ":speed", 5),
			  (gt, ":spear_dist", 200),
			  (val_add, ":speed", 5),
		   (try_end),
		   # (assign, reg0, ":speed"),
		   # (display_message, "str_reg0"),
		   (val_sub,":hp",":speed"),
           (val_max,":hp", 0),
           (agent_set_hit_points, ":victim", ":hp", 0), #NEW HP% = Previous HP% - (Speed/8)
           (agent_deliver_damage_to_agent,":victim",":victim"), ##CHANGE TO THE AGENT DEALING DAMAGE? Probably not to avoid double pike-buff
           (store_agent_hit_points,":hp",":victim",1), #Post-Damage HP 
		   (try_begin), ## REAR or RIDER DAMAGE
		       (gt, ":hp", 0), #IF THE HORSE IS STILL ALIVE, base 50% chance of rearing
			   (store_random_in_range, ":random_no", 0, 100),
			   (try_begin), #Pike bonus block
				  #(item_slot_eq, ":weapon", slot_item_pike, 1),
				  (ge, ":spear_dist", 150),
				  (val_sub, ":random_no", 10), #"Pike" with 60% chance
				  (gt, ":spear_dist", 200),
				  (val_sub, ":random_no", 10), #Longest Pikes with 70% chance
			   (try_end),
			   (lt, ":random_no", 50),
			   (agent_set_animation, ":victim", "anim_horse_rear"),
		   (else_try), #Horse Killed, so damage rider on fall
		       (le, ":hp", 0),
		       # #(agent_set_no_dynamics, ":victim", 1), #0 = turn dynamics off, 1 = turn dynamics on (required for cut-scenes)    ????
			   # (agent_get_position, pos2, ":victim"),
			   # (position_move_y, pos2, -100), #back 1m
			   # (agent_set_position, ":victim", pos2), #above here, trying to prevent horse forward momentum too much...nothing works
			   (store_random_in_range, ":random_no", 40, 75), #Rider should loose 1/4 - 3/5 of HP
			   (store_agent_hit_points, ":rider_hp", ":vic_rider", 0),
			   (val_min, ":random_no", ":rider_hp"),
			   (agent_set_hit_points, ":vic_rider", ":random_no", 0),
		   (try_end),
		   (try_begin),
              (agent_get_horse,":playerhorse","$fplayer_agent_no"),
              (eq,":victim",":playerhorse"),         
              (val_sub,":oldhp",":hp"),
              (assign,reg1,":oldhp"),
              (display_message,"@Your horse received {reg1} damage from a braced spear!",0xff4040),
           (else_try),
              (eq, ":agent", "$fplayer_agent_no"),
              (val_sub,":oldhp",":hp"),
              (assign,reg1,":oldhp"),
              (str_store_item_name, s1, ":weapon"),
              (display_message,"@Braced {s1} dealt {reg1} damage!"),
              (agent_set_slot, "$fplayer_agent_no", slot_agent_player_braced, 0),
           (try_end),
        (try_end),
    ]),

  (0, 0, 2, [(key_clicked, "$key_special_brace"),(agent_is_alive,"$fplayer_agent_no"), #spearwall_trigger_2
        (neg|agent_slot_eq, "$fplayer_agent_no", slot_agent_player_braced, 1), 
        (agent_get_horse, reg0, "$fplayer_agent_no"),
		(eq, reg0, -1), ##be sure player isn't currently mounted
		(agent_get_wielded_item, reg0, "$fplayer_agent_no", 1),
		(le, reg0, 0), #no shield
		], 
       [
        (agent_get_wielded_item, ":weapon", "$fplayer_agent_no", 0), #CABA
        (assign, ":valid_weapon", 0), #CABA
        (try_begin), #CABA-whole block
            (agent_slot_ge, "$fplayer_agent_no", slot_agent_spear, 1),
            (agent_slot_eq, "$fplayer_agent_no", slot_agent_spear, ":weapon"),
            (assign, ":valid_weapon", 1),
        (else_try),
            (ge, ":weapon", 0),
            (item_get_type, ":wpn_type", ":weapon"),
            (eq, ":wpn_type", itp_type_polearm),
            (agent_set_slot, "$fplayer_agent_no", slot_agent_spear, ":weapon"),
            (assign, ":valid_weapon", 1),
        (try_end),
        (eq, ":valid_weapon", 1),       
		(str_store_item_name, s1, ":weapon"), #CABA
        (display_message,"@Bracing {s1} for charge.",0x6495ed),
        #(agent_set_animation, "$fplayer_agent_no", "anim_spearwall_hold"),
        (agent_set_slot, "$fplayer_agent_no", slot_agent_player_braced, 1), #CABA
    ]),
       
  (0, 0, 0, [(this_or_next|game_key_clicked, gk_attack),(this_or_next|game_key_clicked, gk_defend), #spearwall_trigger_3
        (this_or_next|game_key_clicked, gk_move_forward),(this_or_next|game_key_clicked, gk_move_backward),
        (this_or_next|game_key_clicked, gk_move_left),(this_or_next|game_key_clicked, gk_move_right),
        (this_or_next|game_key_clicked, gk_equip_primary_weapon),(this_or_next|game_key_clicked, gk_equip_secondary_weapon),
        (this_or_next|game_key_clicked, gk_action),(game_key_clicked, gk_sheath_weapon),
		(agent_is_alive,"$fplayer_agent_no"),(neg|agent_slot_eq, "$fplayer_agent_no", slot_agent_player_braced, 0),
        ],
       [
        (display_message,"@Releasing from brace.",0x6495ed),
        #(agent_set_animation, "$fplayer_agent_no", "anim_release_thrust_staff"),
		(agent_set_animation, "$fplayer_agent_no", "anim_spearwall_bracing_recoil"),
        (agent_set_slot, "$fplayer_agent_no", slot_agent_player_braced, 0), #CABA
    ]), 
  ##Spearwall Kit - Edited from The Mercenary by Caba'drin
 ] 

bodyguard_triggers = [
 (ti_after_mission_start, 0, 0, 
   [
	   (party_slot_ge, "p_main_party", slot_party_pref_bodyguard, 1),
	   ## WINDYPLAINS+ ## - Disabled so that bodyguards exist in disguise missions.
	   # (neq, "$g_mt_mode", tcm_disguised)
	   ## WINDYPLAINS- ##
   ], #condition for not sneaking in; to exclude prison-breaks, etc change to (eq, "$g_mt_mode", tcm_default")
   [
    #Get number of bodyguards
    (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
    (troop_get_slot, ":renown", "trp_player", slot_troop_renown),
    (val_div, ":leadership", 3),
    (val_div, ":renown", 400),
    (store_add, ":max_guards", ":renown", ":leadership"),
	(party_get_slot, ":limit", "p_main_party", slot_party_pref_bodyguard),
	#(val_add, ":limit", 1),
    (val_min, ":max_guards", ":limit"),
    (ge, ":max_guards", 1),
	
	#Prepare Scene/Mission Template
	(store_cur_mission_template_no, ":mission_tpl"),
	(try_begin),		
		(eq, ":mission_tpl", "mt_village_center"),
		(assign, ":entry_point", 11), #Village Elder's Entry
	(else_try),
		(this_or_next|eq, ":mission_tpl", "mt_castle_visit"),
		(eq, ":mission_tpl", "mt_town_center"),
		(assign, ":entry_point", 24), #Prison Guard's Entry
	## WINDYPLAINS+ ## - Companion bodyguards can show up in disguise missions.
	(else_try),
		(eq, ":mission_tpl", "mt_sneak_caught_fight"),
		(assign, ":entry_point", 2), # Visitor source
		# (mission_tpl_entry_clear_override_items, ":mission_tpl", ":entry_point"),
		# (mission_tpl_entry_add_override_item, ":mission_tpl", ":entry_point", "itm_pilgrim_hood"),
		# (mission_tpl_entry_add_override_item, ":mission_tpl", ":entry_point", "itm_pilgrim_disguise"),
		# (mission_tpl_entry_add_override_item, ":mission_tpl", ":entry_point", "itm_bastard_sword_a"),
		# (mission_tpl_entry_add_override_item, ":mission_tpl", ":entry_point", "itm_throwing_daggers"),
	## WINDYPLAINS- ##
	(else_try),
		(assign, ":entry_point", 17), #First NPC Tavern Entry
	(try_end),
	(try_begin),
		(neq, "$talk_context", tc_tavern_talk),
		(agent_slot_ge, "$fplayer_agent_no", slot_agent_horse, 1), #If the player spawns with a horse, the bodyguard will too.
		(mission_tpl_entry_set_override_flags, ":mission_tpl", ":entry_point", 0),
	(try_end),
	(store_current_scene, ":cur_scene"),
	(modify_visitors_at_site, ":cur_scene"),  
   
    #Find and Spawn Bodyguards
    (assign, ":bodyguard_count", 0),   
    (party_get_num_companion_stacks, ":num_of_stacks", "p_main_party"),
    (try_for_range, ":i", 0, ":num_of_stacks"),
        (party_stack_get_troop_id, ":troop_id", "p_main_party", ":i"),
        (neq, ":troop_id", "trp_player"),
        (troop_is_hero, ":troop_id"),
        (neg|troop_is_wounded, ":troop_id"),
        (val_add, ":bodyguard_count", 1),
				
		(try_begin), #For prison-breaks
		    (this_or_next|eq, "$talk_context", tc_escape),
            (eq, "$talk_context", tc_prison_break),	  
            (troop_set_slot, ":troop_id", slot_troop_will_join_prison_break, 1),
		(try_end),

        (add_visitors_to_current_scene, ":entry_point", ":troop_id", 1),

        (eq, ":bodyguard_count", ":max_guards"),
        (assign, ":num_of_stacks", 0), #Break Loop       
    (try_end), #Stack Loop
    (gt, ":bodyguard_count", 0), #If bodyguards spawned...
    (set_show_messages, 0),   
    (team_give_order, "$fplayer_team_no", 8, mordr_follow), #Division 8 to avoid potential conflicts
	(team_set_order_listener, "$fplayer_team_no", 8),
    (set_show_messages, 1),   
   ]),   

 (ti_on_agent_spawn, 0, 0, [(party_slot_ge, "p_main_party", slot_party_pref_bodyguard, 1)], 
   [
	(store_trigger_param_1, ":agent"),
	(agent_get_troop_id, ":troop", ":agent"),
	(neq, ":troop", "trp_player"),
	(troop_is_hero, ":troop"),
	(main_party_has_troop, ":troop"),
	
	(get_player_agent_no, ":player"),
	(ge, ":player", 0),
	(agent_get_team, ":player_team", ":player"),
	
	(agent_get_position,pos1,":player"),		
	
	(agent_set_team, ":agent", ":player_team"),
	(agent_set_division, ":agent", 8),
	(agent_add_relation_with_agent, ":agent", ":player", 1),
	(agent_set_is_alarmed, ":agent", 1),
	(store_random_in_range, ":shift", 1, 3),
	(val_mul, ":shift", 100),
	(position_move_y, pos1, ":shift"),
	(store_random_in_range, ":shift", 1, 3),
	(store_random_in_range, ":shift_2", 0, 2),
	(val_mul, ":shift_2", -1),
	(try_begin),
		(neq, ":shift_2", 0),
		(val_mul, ":shift", ":shift_2"),
	(try_end),
	(position_move_x, pos1, ":shift"),
	(agent_set_position, ":agent", pos1),
   ]),
  
 (ti_on_agent_killed_or_wounded, 0, 0, [(party_slot_ge, "p_main_party", slot_party_pref_bodyguard, 1)],
    [
     (store_trigger_param_1, ":dead_agent"),
        
     (agent_get_troop_id, ":troop", ":dead_agent"),
	 (neq, ":troop", "trp_player"),
	 (troop_is_hero, ":troop"),
	 (main_party_has_troop, ":troop"),
	 (neg|troop_is_wounded, ":troop"),
	 (party_wound_members, "p_main_party", ":troop", 1),
	]),
 ]
  
custom_camera_triggers = [  
 init_player_global_variables,
 # CUSTOM CAMERA - dunde (Rubik, MartinF) + DEATH CAMERA - MadVader  + Combination and reworking by Caba
 (0, 0, ti_once, [(get_player_agent_no, "$cam_current_agent"), (gt, "$cam_current_agent", -1)], #camera_init
    [ (assign,"$cam_mode", cam_mode_default),(assign, "$cam_free", -1), #cam_free was 0; -1 not free; 0 custom/movement free; 1 all agent cycle free		   
	  #(assign, "$g_camera_z", 300),(assign, "$g_camera_y", -1000),(assign, "$g_camera_x", 0),	  
	  #(assign, "$deathcam_on", 0),(assign, "$shoot_mode",0), 			
	  (assign, "$pin_player_fallen", 0),
      # mouse center coordinates (non-windowed)
      (assign, "$camera_mouse_center_x", 500),
      (assign, "$camera_mouse_center_y", 375),
      # last recorded mouse coordinates
      (assign, "$camera_mouse_x", "$camera_mouse_center_x"),
      (assign, "$camera_mouse_y", "$camera_mouse_center_y"),
      # counts how many cycles the mouse stays in the same position, to determine new center in windowed mode
      (assign, "$camera_mouse_counter", 0),
	  (neg|is_between, "$camera_mouse_deadzone", 1, 11),(assign, "$camera_mouse_deadzone", 3), #CABA Changed from a constant, former comment: set this to a positive number (MV: 2 or 3 works well for me, but needs testing on other people's PCs)
	]),
	
 ## MadVader deathcam begin
 (0, 0, 0, [(eq, "$cam_mode", cam_mode_free), #deathcam_move & key_rotate
      (this_or_next|key_clicked, "$key_camera_forward"),
      (this_or_next|key_is_down, "$key_camera_forward"),
      (this_or_next|key_clicked, "$key_camera_backward"),
      (this_or_next|key_is_down, "$key_camera_backward"),
      (this_or_next|key_clicked, "$key_camera_left"),
      (this_or_next|key_is_down, "$key_camera_left"),
      (this_or_next|key_clicked, "$key_camera_right"),
      (this_or_next|key_is_down, "$key_camera_right"),
	  #key_rotate
	  (this_or_next|game_key_clicked, gk_move_forward),
      (this_or_next|game_key_is_down, gk_move_forward),
      (this_or_next|game_key_clicked, gk_move_backward),
      (this_or_next|game_key_is_down, gk_move_backward),
      (this_or_next|game_key_clicked, gk_move_left),
      (this_or_next|game_key_is_down, gk_move_left),
      (this_or_next|game_key_clicked, gk_move_right),
      (game_key_is_down, gk_move_right),],
    [
      (mission_cam_get_position, cam_position),
      (assign, ":move_x", 0),
      (assign, ":move_y", 0),
	  (assign, ":rotate_x", 0),
	  (assign, ":rotate_z", 0),
      (try_begin), #forward
        (this_or_next|key_clicked, "$key_camera_forward"),
        (key_is_down, "$key_camera_forward"),
        (assign, ":move_y", 10),
      (try_end),
      (try_begin), #backward
        (this_or_next|key_clicked, "$key_camera_backward"),
        (key_is_down, "$key_camera_backward"),
        (assign, ":move_y", -10),
      (try_end),
      (try_begin), #left
        (this_or_next|key_clicked, "$key_camera_left"),
        (key_is_down, "$key_camera_left"),
        (assign, ":move_x", -10),
      (try_end),
      (try_begin), #right
        (this_or_next|key_clicked, "$key_camera_right"),
        (key_is_down, "$key_camera_right"),
        (assign, ":move_x", 10),
      (try_end),
	  #key_rotate
	  (try_begin),
	    (this_or_next|game_key_clicked, gk_move_forward),
        (game_key_is_down, gk_move_forward),
        (assign, ":rotate_x", 2),
	  (try_end),
	  (try_begin),
	    (this_or_next|game_key_clicked, gk_move_backward),
        (game_key_is_down, gk_move_backward),
        (assign, ":rotate_x", -2),
	  (try_end),
	  (try_begin),
	    (this_or_next|game_key_clicked, gk_move_left),
        (game_key_is_down, gk_move_left),
        (assign, ":rotate_z", 2),
	  (try_end),
	  (try_begin),
	    (this_or_next|game_key_clicked, gk_move_right),
        (game_key_is_down, gk_move_right),
        (assign, ":rotate_z", -2),
	  (try_end),
	  #key_rotate
	  (try_begin),
		(game_key_is_down, gk_zoom),
		(val_mul, ":move_x", 3),
		(val_mul, ":move_y", 3),
		(val_mul, ":rotate_x", 2),
		(val_mul, ":rotate_z", 2),
	  (try_end),
      (position_move_x, cam_position, ":move_x"),
      (position_move_y, cam_position, ":move_y"),	  
	  #key_rotate	
      (position_rotate_x, cam_position, ":rotate_x"),
      (val_add, "$g_camera_rotx", ":rotate_x"),	  
	  (try_begin),
        (neq, ":rotate_z", 0),
        (store_mul, ":minusrotx", "$g_camera_rotx", -1),
        (position_rotate_x, cam_position, ":minusrotx"), #needed so camera yaw won't change
        (position_rotate_z, cam_position, ":rotate_z"),
        (position_rotate_x, cam_position, "$g_camera_rotx"), #needed so camera yaw won't change
      (try_end),
	  #key_rotate
	  (try_begin),
		(position_get_distance_to_ground_level, ":to_ground", cam_position),
		(lt, ":to_ground", 0),
		(position_set_z_to_ground_level, cam_position),
		(position_move_z, cam_position, 50),
	  (try_end),
	  (mission_cam_set_position, cam_position),   
    ]),

 (0, 0, 0, [(eq, "$cam_mode", cam_mode_free),  #deathcam_rotate
      (neg|is_presentation_active, "prsnt_battle"),
      (mouse_get_position, pos1),
      (set_fixed_point_multiplier, 1000),
      (position_get_x, reg1, pos1),
      (position_get_y, reg2, pos1),
      (this_or_next|neq, reg1, "$camera_mouse_center_x"),
      (neq, reg2, "$camera_mouse_center_y"),],
    [
      # fix for windowed mode: recenter the mouse
      (assign, ":continue", 1),
      (try_begin),
        (eq, reg1, "$camera_mouse_x"),
        (eq, reg2, "$camera_mouse_y"),
        (val_add, "$camera_mouse_counter", 1),
        (try_begin), #hackery: if the mouse hasn't moved for X cycles, recenter it
          (gt, "$camera_mouse_counter", 50),
          (assign, "$camera_mouse_center_x", reg1),
          (assign, "$camera_mouse_center_y", reg2),
          (assign, "$camera_mouse_counter", 0),
        (try_end),
        (assign, ":continue", 0),
      (try_end),
      (eq, ":continue", 1), #continue only if mouse has moved
      (assign, "$camera_mouse_counter", 0), # reset recentering hackery
     
      # update recorded mouse position
      (assign, "$camera_mouse_x", reg1),
      (assign, "$camera_mouse_y", reg2),
     
      (mission_cam_get_position, cam_position),
      (store_sub, ":shift", "$camera_mouse_center_x", reg1), #horizontal shift for pass 0
      (store_sub, ":shift_vertical", reg2, "$camera_mouse_center_y"), #for pass 1
     
      (try_for_range, ":pass", 0, 2), #pass 0: check mouse x movement (left/right), pass 1: check mouse y movement (up/down)
        (try_begin),
          (eq, ":pass", 1),
          (assign, ":shift", ":shift_vertical"), #get ready for the second pass
        (try_end),
		(store_mul, ":neg_deadzone", "$camera_mouse_deadzone", -1), #Caba - this and next line altered to make variable
        (this_or_next|lt, ":shift", ":neg_deadzone"), #skip pass if not needed (mouse deadzone)
        (gt, ":shift", "$camera_mouse_deadzone"),
       
        (assign, ":sign", 1),
        (try_begin),
          (lt, ":shift", 0),
          (assign, ":sign", -1),
        (try_end),
        # square root calc
        (val_abs, ":shift"),
        (val_sub, ":shift", "$camera_mouse_deadzone"), # ":shift" is now 1 or greater
        (convert_to_fixed_point, ":shift"),
        (store_sqrt, ":shift", ":shift"),
        (convert_from_fixed_point, ":shift"),
        (val_clamp, ":shift", 1, 6), #limit rotation speed
        (val_mul, ":shift", ":sign"),
        (try_begin),
          (eq, ":pass", 0), # rotate around z (left/right)
          (store_mul, ":minusrotx", "$g_camera_rotx", -1),
          (position_rotate_x, cam_position, ":minusrotx"), #needed so camera yaw won't change
          (position_rotate_z, cam_position, ":shift"),
          (position_rotate_x, cam_position, "$g_camera_rotx"), #needed so camera yaw won't change
        (try_end),
        (try_begin),
          (eq, ":pass", 1), # rotate around x (up/down)
          (position_rotate_x, cam_position, ":shift"),
          (val_add, "$g_camera_rotx", ":shift"),
        (try_end),
      (try_end), #try_for_range ":pass"
      (mission_cam_set_position, cam_position),
    ]),
 ## MadVader deathcam end
 
 (0, 0, 0, [(eq, "$cam_mode", cam_mode_follow)], #camera_follow
   [
     (set_fixed_point_multiplier, 100),
     (agent_get_look_position, cam_position, "$cam_current_agent"),
     (position_get_rotation_around_x, ":angle", cam_position),
     (store_sub, ":reverse", 0, ":angle"),
     (position_rotate_x, cam_position, ":reverse"),
	 (try_begin),
	    (eq, "$cam_free", -1),
		(val_clamp, "$g_camera_x", -1000, 1000),
	    (val_clamp, "$g_camera_y", -1000, 1000),
		(val_min, "$g_camera_z", 1000),
	 (try_end),
     (position_move_y, cam_position, "$g_camera_y"),
     (position_move_z, cam_position, "$g_camera_z"),
	 (position_move_x, cam_position, "$g_camera_x"),
     (agent_get_horse, ":horse_agent", "$cam_current_agent"),
     (try_begin),
        (ge, ":horse_agent", 0),
        (position_move_z, cam_position, 80),       
     (try_end),
     (store_mul, ":reverse", -1, "$g_camera_y"),
     (store_atan2, ":drop", "$g_camera_z", ":reverse"),
     (convert_from_fixed_point, ":drop"),
     (val_sub, ":angle", ":drop"),
     (position_rotate_x, cam_position, ":angle"),
	 (try_begin),
		(position_get_distance_to_ground_level, ":to_ground", cam_position),
		(lt, ":to_ground", 0),
		(position_set_z_to_ground_level, cam_position),
		(position_move_z, cam_position, 50),
	 (try_end),
	 (try_begin), ##CABA - Deployment
		(eq, "$battle_phase", BP_Spawn),  ##CABA - Deployment
		(mission_cam_set_position, cam_position), ##CABA - Deployment
	 (else_try), ##CABA - Deployment
		(mission_cam_animate_to_position, cam_position, 100, 0),
	 (try_end), ##CABA - Deployment	 
  
    (try_begin), 
		(neg|main_hero_fallen),
		(this_or_next|game_key_clicked, gk_view_char),
		(game_key_clicked, gk_cam_toggle),
		(mission_cam_set_mode, 0),
		(assign, "$cam_mode", cam_mode_default),
	(try_end),
  ]),
  
 (0, 0, 0, [(key_clicked, "$key_camera_toggle"),(lt, "$cam_mode", cam_mode_shoot)], #camera_toggle
   # toggling only when came mode =0 or 1 (2=disable) ; shoot_mode=1 temporary diable toggling
   [(try_begin),
     (eq, "$cam_mode", cam_mode_default),
	 (assign, "$g_camera_z", 300),
	 (assign, "$g_camera_y", -1000),
	 (assign, "$g_camera_x", 0),
	 (assign, "$cam_mode", cam_mode_follow),
    (else_try),
     (eq, "$cam_mode", cam_mode_follow),
	 (try_begin),
	    (eq, "$cam_free", -1),
		(try_begin),
		    (neg|main_hero_fallen),
			(get_player_agent_no, "$cam_current_agent"),                 
		(try_end),
		(assign, "$cam_mode", cam_mode_default),
	 (else_try),
		(try_begin),
			(main_hero_fallen),
			(mission_cam_get_position, cam_position),
			(position_get_rotation_around_x, "$g_camera_rotx", cam_position),
			(call_script, "script_cust_cam_init_message", cam_mode_free),
		(else_try),
			(assign, "$g_camera_rotx", 0),
		(try_end),		
		(assign, "$cam_mode", cam_mode_free),
     (try_end),
    (else_try),
     (eq, "$cam_mode", cam_mode_free),
	 (try_begin),
	    (ge, "$cam_free", 0),
		(assign, "$g_camera_z", 300),
	    (assign, "$g_camera_y", -1000),
	    (assign, "$g_camera_x", 0),
		(try_begin),
			(main_hero_fallen),
			(call_script, "script_cust_cam_init_message", cam_mode_follow),
		(try_end),
		(assign, "$cam_mode", cam_mode_follow),
	 (else_try),
	    (assign, "$cam_mode", cam_mode_default),
	 (try_end),
    (try_end),
	(start_presentation, "prsnt_caba_camera_mode_display"),
    (try_begin),
      (eq, "$cam_mode", cam_mode_default),
      (mission_cam_set_mode, 0),
    (else_try),
      (mission_cam_set_mode, 1),
    (try_end),
  ]),

 (0, 0, 0, [(eq, "$cam_mode", cam_mode_follow), #camera_follow_move
      (this_or_next|key_is_down, "$key_camera_forward"),
      (this_or_next|key_is_down, "$key_camera_backward"),
      (this_or_next|key_is_down, "$key_camera_left"),
      (this_or_next|key_is_down, "$key_camera_right"),
      (this_or_next|key_is_down, "$key_camera_zoom_plus"), 
	  (this_or_next|key_is_down, "$key_camera_zoom_min"),
	  (this_or_next|key_clicked, "$key_camera_next"),
	  (this_or_next|key_clicked, "$key_camera_prev"),
	  (game_key_is_down, gk_attack),
	  ## WINDYPLAINS+ ## - Bodysliding block
	  (neq, "$enable_bodysliding", 1),
	  ## WINDYPLAINS- ##
	  ],
    [ 
	  (try_begin), #initialize shoot
		(game_key_is_down, gk_attack),
		(neg|main_hero_fallen),
		(eq, "$fplayer_agent_no","$cam_current_agent"),(agent_is_alive, "$fplayer_agent_no"),(agent_get_wielded_item,":weapon","$cam_current_agent",0),(ge, ":weapon", 0),(item_get_type, ":type", ":weapon"), (this_or_next|eq,":type",itp_type_bow),(this_or_next|eq,":type",itp_type_crossbow),(eq,":type",itp_type_thrown),
		(assign, "$cam_mode", cam_mode_shoot),
		(mission_cam_set_mode, 0),
	  (try_end),
	  (try_begin), #cycle agents
		(ge, "$cam_free", 1),
		(try_begin),
			(key_clicked, "$key_camera_next"),
			(call_script, "script_cust_cam_cycle_forwards"),
		(else_try),
			(key_clicked, "$key_camera_prev"),
			(call_script, "script_cust_cam_cycle_backwards"),
		(try_end),		
	  (try_end),
      (try_begin), #forward
        (key_is_down, "$key_camera_forward"),
        (val_add, "$g_camera_y",10),(game_key_is_down, gk_zoom),(val_add, "$g_camera_y",10),
      (try_end),
      (try_begin), #backward
        (key_is_down, "$key_camera_backward"),
        (val_sub, "$g_camera_y",10),(game_key_is_down, gk_zoom),(val_sub, "$g_camera_y",10),
      (try_end),
      (try_begin), #left
        (key_is_down, "$key_camera_left"),
        (val_sub, "$g_camera_x",10),(game_key_is_down, gk_zoom),(val_sub, "$g_camera_x",10),
      (try_end),
      (try_begin), #right
        (key_is_down, "$key_camera_right"),
        (val_add, "$g_camera_x",10),(game_key_is_down, gk_zoom),(val_add, "$g_camera_x",10),
      (try_end),
	  (try_begin), #up
        (key_is_down, "$key_camera_zoom_plus"),
        (val_add, "$g_camera_z",10),(game_key_is_down, gk_zoom),(val_add, "$g_camera_z",10),
      (try_end),
      (try_begin), #down
        (key_is_down, "$key_camera_zoom_min"),
        (val_sub, "$g_camera_z",10),(game_key_is_down, gk_zoom),(val_sub, "$g_camera_z",10),(val_max,"$g_camera_z", 50),
      (try_end),
    ]),
	
 (0, 0, 0,[(eq, "$cam_mode", cam_mode_shoot),(neg|game_key_is_down, gk_attack)], [(assign,"$cam_mode", cam_mode_follow),(mission_cam_set_mode, 1)]) , #camera_return_normal      
  
 ]
## Prebattle Orders & Deployment End

pbod_battle_triggers = pbod_common_triggers + [init_weather_effects] + prebattle_deployment_triggers + prebattle_orders_triggers + caba_order_triggers


bc_tab_press_addon = [
		#PBOD - Battle Continuation
		(else_try),
		  (party_slot_eq, "p_main_party", slot_party_pref_bc_continue, 1), #PBOD Battle Continuation On
		  (this_or_next|main_hero_fallen),   #CABA EDIT/FIX FOR DEATH CAM
		  (eq, "$pin_player_fallen", 1),
		  (str_store_string, s5, "str_retreat"),
		  (call_script, "script_simulate_retreat", 5, 20, 0),
		  (call_script, "script_count_mission_casualties_from_agents"),
		  (set_mission_result, -1),
		  (finish_mission,0),
		#PBOD - Battle Continuation END
 ]

batt_continue_addon = [
	(try_begin),
	  (party_slot_eq, "p_main_party", slot_party_pref_bc_continue, 1), #PBOD Battle Continuation Active
	  (assign, ":num_allies", 0),		
	  (try_for_agents, ":agent"),
		 (agent_is_ally, ":agent"),
		 (agent_is_alive, ":agent"),
		 (val_add, ":num_allies", 1),
	  (try_end),
	  (gt, ":num_allies", 0),
	  (display_message, "@DEBUG (PBOD): Battle continuation has kicked in!", gpu_debug),
	  (try_begin),
		  (neq, "$cam_free", 1),
		  (call_script, "script_cust_cam_init_death_cam", cam_mode_free),
		  (party_slot_eq, "p_main_party", slot_party_pref_bc_charge_ko, 1), #PBOD "Charge on KO" Active
		  (set_show_messages, 0),
		  (team_give_order, "$fplayer_team_no", grc_everyone, mordr_charge),
		  (team_set_order_listener, "$fplayer_team_no", grc_everyone),
		  (call_script, "script_player_order_formations", mordr_charge),
		  (set_show_messages, 1),
	  (try_end),
	(else_try),
 ]

custom_battle_batt_continue_addon = [
	(try_begin),
	  (party_slot_eq, "p_main_party", slot_party_pref_bc_continue, 1), #PBOD Battle Continuation Active
	  (try_begin),
		  (neq, "$cam_free", 1),
		  (call_script, "script_cust_cam_init_death_cam", cam_mode_free),
		  (party_slot_eq, "p_main_party", slot_party_pref_bc_charge_ko, 1), #PBOD "Charge on KO" Active
		  (set_show_messages, 0),
		  (team_give_order, "$fplayer_team_no", grc_everyone, mordr_charge),
		  (team_set_order_listener, "$fplayer_team_no", grc_everyone),
		  (call_script, "script_player_order_formations", mordr_charge),
		  (set_show_messages, 1),
	  (try_end),
	(else_try),
	  (assign,"$g_battle_result",-1),
 ]

	
from util_wrappers import *
from util_common import *

def modmerge(var_set):
	try:
		from modmerger_options import module_sys_info
		version = module_sys_info["version"]
	except:
		version = 1143 # version not specified.  assume latest warband at this time

	try:
		var_name_1 = "mission_templates"
		orig_mission_templates = var_set[var_name_1]

		# START do your own stuff to do merging

		modmerge_mission_templates(orig_mission_templates)

		# END do your own stuff
            
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)


def modmerge_mission_templates(orig_mission_templates):
	from module_mission_templates import common_battle_tab_press, common_battle_check_victory_condition, common_siege_check_defeat_condition, custom_battle_check_victory_condition, custom_battle_check_defeat_condition, common_battle_order_panel, common_battle_order_panel_tick
	
	##Bugfix - for overlapping presentations (battle and order_display)
	try:
		codeblock = TriggerWrapper(common_battle_order_panel_tick).GetConsequenceBlock()
		pos = codeblock.FindLineMatching((is_presentation_active, "prsnt_battle"))
		codeblock.InsertAfter(pos, [(presentation_activate, "prsnt_battle"),]) #WSE
	except:
		import sys
		print "Injecton 0 failed:", sys.exc_info()[1]
		raise
	
	##Battle Continuation: editing common triggers
	try:
		# codeblock = TriggerWrapper(common_battle_tab_press).GetConsequenceBlock()
		# pos = codeblock.FindLineMatching((call_script, "script_cf_check_enemies_nearby"))
		# codeblock.InsertBefore(pos-1, bc_tab_press_addon) #pos-1 to jump above the else try
		
		# codeblock = TriggerWrapper(common_battle_check_victory_condition).GetConditionBlock()
		# pos = codeblock.FindLineMatching((neg|main_hero_fallen, 0))
		# codeblock.InsertBefore(pos,[(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_bc_continue, 1)])
		
		# codeblock = TriggerWrapper(common_battle_order_panel).GetConsequenceBlock()
		# pos = codeblock.FindLineMatching((game_key_clicked, gk_view_orders))
		# codeblock.InsertAfter(pos,[(neg|main_hero_fallen),(neq, "$battle_phase", BP_Spawn)]) #disabled in Deployment Phase
		
		#quick/custom battles
		codeblock = TriggerWrapper(custom_battle_check_victory_condition).GetConditionBlock()
		pos = codeblock.FindLineMatching((neg|main_hero_fallen, 0))
		codeblock.InsertBefore(pos,[(this_or_next|party_slot_eq, "p_main_party", slot_party_pref_bc_continue, 1)])
		
		codeblock = TriggerWrapper(custom_battle_check_defeat_condition).GetConsequenceBlock()
		codeblock.InsertBefore(0, custom_battle_batt_continue_addon)
		codeblock.Append([(try_end)])
		TriggerWrapper(custom_battle_check_defeat_condition).GetConditionBlock().RemoveAt(1) #remove the second line (assign,"$g_battle_result",-1),
	except:
		import sys
		print "Injecton 1 failed:", sys.exc_info()[1]
		raise
	
	##Extending Mission Templates' trigger lists with triggers appropriate to the templates
	for i in range(len(orig_mission_templates)):
		mt_name = orig_mission_templates[i][0]
		if(   mt_name=="lead_charge"):
			orig_mission_templates[i][5].extend(pbod_battle_triggers+field_ai_triggers+custom_camera_triggers)
		elif( mt_name=="quick_battle_battle"):
			orig_mission_templates[i][5].extend([common_battle_order_panel, common_battle_order_panel_tick]+pbod_common_triggers+real_deployment_triggers+caba_order_triggers+field_ai_triggers+custom_camera_triggers)
		elif( mt_name=="quick_battle_siege"):
			orig_mission_templates[i][5].extend([common_battle_order_panel, common_battle_order_panel_tick]+pbod_common_triggers+real_deployment_triggers+caba_order_triggers+custom_camera_triggers)
		elif( mt_name=="village_raid" or mt_name=="village_attack_bandits"):
			orig_mission_templates[i][5].extend(pbod_battle_triggers+fix_maintain_division_triggers+field_ai_triggers+pbod_common_triggers+real_deployment_triggers+caba_order_triggers+custom_camera_triggers)
			# orig_mission_templates[i][5].extend(pbod_battle_triggers+fix_maintain_division_triggers+field_ai_triggers+custom_camera_triggers)
		elif( "besiege" in mt_name or "castle_attack" in mt_name or mt_name=="entrenched_encounter" or mt_name=="ship_battle"):
			orig_mission_templates[i][5].extend(pbod_battle_triggers+fix_maintain_division_triggers+custom_camera_triggers)
		elif( mt_name=="town_default" or mt_name=="town_center" or mt_name=="village_center" or mt_name=="bandits_at_night" or mt_name=="castle_visit" or mt_name=="visit_entrenchment" or mt_name=="sneak_caught_fight"):
			orig_mission_templates[i][5].extend(pbod_common_triggers+bodyguard_triggers+caba_order_triggers+custom_camera_triggers)
		elif( not "tutorial" in mt_name and not "multiplayer" in mt_name and not "conversation" in mt_name ):
		    #( mt_name=="alley_fight" or orig_mission_templates[i][1] & mtf_arena_fight):
			orig_mission_templates[i][5].extend(pbod_common_triggers+custom_camera_triggers)
		
		##Battle Continuation:
		# trigger_i = MissionTemplateWrapper(orig_mission_templates[i]).FindTrigger_i(1,4,ti_once,[(main_hero_fallen)])
		# if ( trigger_i != None ):
			# trigger = orig_mission_templates[i][5][trigger_i]
			# codeblock = TriggerWrapper(trigger).GetConsequenceBlock()
			# pos = codeblock.FindLineMatching((assign, "$pin_player_fallen", 1))
			# if (codeblock.GetLineContent(pos+1) != (try_begin) ): #hasn't yet been edited (error check for common triggers, used in sieges)
				# codeblock.InsertAfter(pos, batt_continue_addon)
				# codeblock.Append([(try_end)])
				# if (trigger == common_siege_check_defeat_condition):
					# pos = codeblock.FindLineMatching((party_slot_eq, "p_main_party", slot_party_pref_bc_charge_ko, 1))
					# codeblock.RemoveAt(pos, 6) #remove "Charge on KO" lines for main siege missions
			# #Change re-arm interval from ti_once to 0 (using work around to edit immutable tuple)
			# orig_mission_templates[i][5][trigger_i] = list(orig_mission_templates[i][5][trigger_i])
			# orig_mission_templates[i][5][trigger_i][2] = 0
			# orig_mission_templates[i][5][trigger_i] = tuple(orig_mission_templates[i][5][trigger_i])
	
