# Tournament Play Enhancements (1.6) by Windyplains

# WHAT THIS FILE DOES:
# Replaces the "arena_melee_fight" tournament template and designates new triggers for different tournament types.

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from module_mission_templates import *
## DISABLE FOR NATIVE OSP+ ##
from pbod_mission_templates import *
## DISABLE FOR NATIVE OSP- ##

##################
# BEGIN TRIGGERS #
##################
tpe_standard_triggers = [
###################
# NATIVE TRIGGERS # This is all stuff copied from the original arena_melee_fight that were relevant to tournaments.
###################
	# TRIGGER 0
	(ti_before_mission_start, 0, 0, [], [(call_script, "script_change_banners_and_chest"),
										   (assign, "$g_arena_training_num_agents_spawned", 0)]),
										   
	# TRIGGER 1
	(ti_inventory_key_pressed, 0, 0, [(display_message,"str_cant_use_inventory_arena")], []),
	
	# TRIGGER 2
	(ti_tab_pressed, 0, 0, [(neg|main_hero_fallen),],
	   [(try_begin),
		  (eq, "$g_mt_mode", abm_visit),
		  (set_trigger_result, 1),
		(else_try),
		  (question_box,"str_give_up_fight"),
		(try_end),
		]),
	
	# TRIGGER 3
	(ti_question_answered, 0, 0, [(neg|main_hero_fallen),],
	   [(store_trigger_param_1,":answer"),
		(eq,":answer",0),
		(try_begin),
		  (eq, "$g_mt_mode", abm_tournament),
		  (call_script, "script_tpe_end_tournament_fight", 0),
		# (else_try),
		  # (eq, "$g_mt_mode", abm_village_fist_fighting),
		  # (call_script, "script_end_village_fist_fight", 0),
		(else_try),
		  (eq, "$g_mt_mode", abm_training),
		  (get_player_agent_no, ":player_agent"),
		  (agent_get_kill_count, "$g_arena_training_kills", ":player_agent", 1),#use this for conversation
		(try_end),
		(finish_mission,0),
		]),
	  
	# TRIGGER 4
	(0, 0, ti_once, [],
	   [
		 (eq, "$g_mt_mode", abm_tournament),
		 (play_sound, "snd_arena_ambiance", sf_looping),
		 (call_script, "script_music_set_situation_with_culture", mtf_sit_arena),
		 ]),


################
# TPE TRIGGERS #
################
	
	# TRIGGER 5: Dynamic Weapon AI
	(1, 0, 0, 
		[(eq, "$g_mt_mode", abm_tournament),],
		[
		  # Run through all active NPCs on the tournament battle field.
		  (try_for_agents, ":agent_self"),
			# Isn't a player.
			(agent_is_non_player, ":agent_self"),
			# Isn't a horse.
			(agent_is_human, ":agent_self"),
			# Hasn't been defeated.
			(agent_is_alive, ":agent_self"),
			# exclude tournament masters
			(agent_get_troop_id, ":troop_self", ":agent_self"),
			(neg|is_between, ":troop_self", "trp_town_1_arena_master", "trp_town_1_armorer"),
			# They riding a horse?
			(agent_get_horse, ":horse", ":agent_self"), # 0 - No, 1 - Yes
			
			# Determine closest enemy.
			(assign, ":shortest_distance", 10000),
			(str_store_string, s31, "@No one"),
			(str_store_troop_name, s32, ":troop_self"),
			(agent_get_position, pos1, ":agent_self"),
			(assign, ":distance", 10000),
			(try_for_agents, ":agent_enemy"),
				(agent_get_troop_id, ":troop_enemy", ":agent_enemy"),
				# Not looking at self.
				(neq, ":agent_enemy", ":agent_self"),
				# exclude tournament masters
				(neg|is_between, ":troop_enemy", "trp_town_1_arena_master", "trp_town_1_armorer"),
				# Not an ally
				(agent_get_team, ":team_self", ":agent_self"),
				(agent_get_team, ":team_enemy", ":agent_enemy"),
				(neq, ":team_self", ":team_enemy"),
				# Isn't a horse.
				(agent_is_human, ":agent_enemy"),
				# Hasn't been defeated.
				(agent_is_alive, ":agent_enemy"),
				(agent_get_position, pos2, ":agent_enemy"),
				(get_distance_between_positions,":distance",pos1,pos2),
				(try_begin),
					(lt, ":distance", ":shortest_distance"),
					(assign, ":shortest_distance", ":distance"),
					(str_store_troop_name, s31, ":troop_enemy"),
					(agent_get_horse, ":enemy_mounted", ":agent_enemy"),
				(try_end),
			(try_end),
			
			# If you enable this save yourself a headache and up the trigger timing.
			(try_begin), 
				(ge, DEBUG_TPE_ai_behavior, 3), 
				(assign, reg30, ":shortest_distance"),
				(display_message, "@DEBUG (Weapon AI): {s32}'s closest enemy is {s31} at a distance of {reg30}."), 
			(try_end),
			
			# TPE+ 1.4 - New custom tournament design items.
			(store_sub, ":city_settings", "$current_town", towns_begin),
			(val_mul, ":city_settings", 10),
			# Normal weapons
			(store_add, ":slot_lance",    ":city_settings", tdp_val_setting_lance),
			(store_add, ":slot_archery",  ":city_settings", tdp_val_setting_archery),
			(store_add, ":slot_onehand",  ":city_settings", tdp_val_setting_onehand),
			(store_add, ":slot_twohand",  ":city_settings", tdp_val_setting_twohand),
			(store_add, ":slot_crossbow", ":city_settings", tdp_val_setting_crossbow),
			(store_add, ":slot_throwing", ":city_settings", tdp_val_setting_throwing),
			(store_add, ":slot_polearm",  ":city_settings", tdp_val_setting_polearm),
			# (store_add, ":slot_horse",    ":city_settings", tdp_val_setting_horse),
			# (store_add, ":slot_outfit",   ":city_settings", tdp_val_setting_outfit),
			(troop_get_slot, ":item_normal_lance",    tpe_appearance, ":slot_lance"),
			(troop_get_slot, ":item_normal_archery",  tpe_appearance, ":slot_archery"),
			(troop_get_slot, ":item_normal_onehand",  tpe_appearance, ":slot_onehand"),
			(troop_get_slot, ":item_normal_twohand",  tpe_appearance, ":slot_twohand"),
			(troop_get_slot, ":item_normal_crossbow", tpe_appearance, ":slot_crossbow"),
			(troop_get_slot, ":item_normal_throwing", tpe_appearance, ":slot_throwing"),
			(troop_get_slot, ":item_normal_polearm",  tpe_appearance, ":slot_polearm"),
			# (troop_get_slot, ":item_normal_horse",    tpe_appearance, ":slot_horse"),
			# (troop_get_slot, ":item_normal_outfit",   tpe_appearance, ":slot_outfit"),
			# Enhanced weapons
			(store_add, ":slot_enh_lance", ":slot_lance", 100),
			(store_add, ":slot_enh_archery", ":slot_archery", 100),
			(store_add, ":slot_enh_onehand", ":slot_onehand", 100),
			(store_add, ":slot_enh_twohand", ":slot_twohand", 100),
			(store_add, ":slot_enh_crossbow", ":slot_crossbow", 100),
			(store_add, ":slot_enh_throwing", ":slot_throwing", 100),
			(store_add, ":slot_enh_polearm", ":slot_polearm", 100),
			# (store_add, ":slot_enh_horse", ":slot_horse", 100),
			# (store_add, ":slot_enh_outfit", ":slot_outfit", 100),
			(troop_get_slot, ":item_enh_lance",    tpe_appearance, ":slot_enh_lance"),
			(troop_get_slot, ":item_enh_archery",  tpe_appearance, ":slot_enh_archery"),
			(troop_get_slot, ":item_enh_onehand",  tpe_appearance, ":slot_enh_onehand"),
			(troop_get_slot, ":item_enh_twohand",  tpe_appearance, ":slot_enh_twohand"),
			(troop_get_slot, ":item_enh_crossbow", tpe_appearance, ":slot_enh_crossbow"),
			(troop_get_slot, ":item_enh_throwing", tpe_appearance, ":slot_enh_throwing"),
			(troop_get_slot, ":item_enh_polearm",  tpe_appearance, ":slot_enh_polearm"),
			# (troop_get_slot, ":item_enh_horse",    tpe_appearance, ":slot_enh_horse"),
			# (troop_get_slot, ":item_enh_outfit",   tpe_appearance, ":slot_enh_outfit"),
			
			(agent_get_speed, pos4, ":agent_self"),
			(position_get_y, ":speed", pos4),
			
			(assign, ":weapon_choice", 0), # Default to a ranged weapon or lance.
			(try_begin), # You're nearly stationary & someone is closing on you quick -> melee weapon
				(lt, ":speed", 2000),
				(le, ":shortest_distance", wp_tpe_enemy_approaching_foot),
				(assign, ":weapon_choice", 1),
			(else_try), # You're mounted, moving fast and have a lance. -> Lance
				(ge, ":horse", 0),
				(ge, ":speed", 2000), # Try to improve on lancers stuck against walls.
				(this_or_next|agent_has_item_equipped, ":agent_self", ":item_normal_lance"),
				(agent_has_item_equipped, ":agent_self", ":item_enh_lance"),
				(assign, ":weapon_choice", 2), # Bypasses melee/ranged options.
			(else_try), # An unmounted enemy is approaching you. -> Melee Weapon.
				(le, ":enemy_mounted", 0),
				(le, ":shortest_distance", wp_tpe_enemy_approaching_foot),
				(assign, ":weapon_choice", 1),
			(else_try), # A mounted enemy is approaching you. -> Melee Weapon
				(ge, ":enemy_mounted", 1),
				(le, ":shortest_distance", wp_tpe_enemy_approaching_mounted),
				(assign, ":weapon_choice", 1),
			(try_end),
			
			(try_begin),
				(eq, ":weapon_choice", 1),
				(agent_set_wielded_item, ":agent_self", ":item_normal_polearm"),
				(agent_set_wielded_item, ":agent_self", ":item_enh_polearm"),
				(agent_set_wielded_item, ":agent_self", ":item_normal_onehand"),
				(agent_set_wielded_item, ":agent_self", ":item_enh_onehand"),
				(agent_set_wielded_item, ":agent_self", ":item_normal_twohand"),
				(agent_set_wielded_item, ":agent_self", ":item_enh_twohand"),
				(try_begin),
					# AI behavior change to make unmounted spear wielders use their spear two-handed.
					(lt, ":horse", 0),
					# Determine if the agent is using a spear.
					(this_or_next|agent_has_item_equipped, ":agent_self", ":item_normal_polearm"),
					(agent_has_item_equipped, ":agent_self", ":item_enh_polearm"),
					# Unwield shield
					(this_or_next|agent_has_item_equipped,":agent_self", wp_tpe_normal_shield),
					(agent_has_item_equipped,":agent_self", wp_tpe_enhanced_shield),
					(agent_unequip_item, ":agent_self", wp_tpe_normal_shield),
					(agent_unequip_item, ":agent_self", wp_tpe_enhanced_shield),
					(ge, DEBUG_TPE_ai_behavior, 1),
					(display_message, "@DEBUG (TPE): {s32} is wielding a spear on foot and discards shield."),
				(try_end),
			(else_try),
				(eq, ":weapon_choice", 0),
				(agent_set_wielded_item, ":agent_self", ":item_normal_archery"),
				(agent_set_wielded_item, ":agent_self", ":item_enh_archery"),
				(agent_set_wielded_item, ":agent_self", ":item_normal_crossbow"),
				(agent_set_wielded_item, ":agent_self", ":item_enh_crossbow"),
				(agent_set_wielded_item, ":agent_self", ":item_normal_throwing"),
				(agent_set_wielded_item, ":agent_self", ":item_enh_throwing"),
			(else_try),
				(eq, ":weapon_choice", 2),
				(agent_set_wielded_item, ":agent_self", ":item_normal_lance"),
				(agent_set_wielded_item, ":agent_self", ":item_enh_lance"),
			(try_end),
		  (try_end),
		  # (try_begin),
			# (get_player_agent_no, ":agent_player"),
			# (agent_get_speed, pos1, ":agent_player"),
			# (position_get_y, reg32, pos1),
			# (display_message, "@Player speed = ({reg31}, {reg32})"),
		  # (try_end),
	   ]),

	# TRIGGER 6: Runs through all active agents on the battlefield and forces them to wear shoes.
	(0, 0, ti_once, 
		[(eq, "$g_mt_mode", abm_tournament),
		(eq, wp_tpe_mod_opt_actual_gear, 0),],
		[
			# Run through all active NPCs on the tournament battle field.
			(try_for_agents, ":agent_self"),
				(agent_equip_item, ":agent_self", wp_tpe_normal_boots),
				(agent_equip_item, ":agent_self", wp_tpe_enhanced_boots),
			(try_end),
		]),
	
	# TRIGGER 7: This trigger sets up the mission end conditions.
	(1, 4, ti_once, 
		[(eq, "$g_mt_mode", abm_tournament),
		(this_or_next|num_active_teams_le, 1),
		(eq, "$tpe_trigger_round_end", 1),
		],
		[
			# Determine highest scoring team.
			(assign, ":best_team", 0),
			(troop_get_slot, ":highest_score", "trp_tpe_presobj", tpe_icd_team_0_points),
			(try_begin),
				(troop_slot_ge, "trp_tpe_presobj", tpe_icd_team_1_points, ":highest_score"),
				(troop_get_slot, ":highest_score", "trp_tpe_presobj", tpe_icd_team_1_points),
				(assign, ":best_team", 1),
			(try_end),
			(try_begin),
				(troop_slot_ge, "trp_tpe_presobj", tpe_icd_team_2_points, ":highest_score"),
				(troop_get_slot, ":highest_score", "trp_tpe_presobj", tpe_icd_team_2_points),
				(assign, ":best_team", 2),
			(try_end),
			(try_begin),
				(troop_slot_ge, "trp_tpe_presobj", tpe_icd_team_3_points, ":highest_score"),
				(troop_get_slot, ":highest_score", "trp_tpe_presobj", tpe_icd_team_3_points),
				(assign, ":best_team", 3),
			(try_end),
			(assign, "$temp_2", ":best_team"), ## ELIMINATION MODE ##
			
			(try_for_agents, ":agent_no"),
				(agent_is_human, ":agent_no"), # Remove horses.
				(agent_get_team, ":agent_team", ":agent_no"),
				(agent_get_troop_id, ":troop_id", ":agent_no"),
				## WINDYPLAINS+ ## - Combat Ability - BONUS_BERKSERER / BONUS_DISCIPLINE - Remove extra health post combat.
				(call_script, "script_ce_reset_agent_max_health", ":agent_no"), # combat_scripts.py
				## WINDYPLAINS- ##
				(try_begin),
					(eq, ":agent_team", ":best_team"),
					(call_script, "script_tpe_award_point_to_troop", ":troop_id", 1, tpe_point_best_scoring_team, wp_green), # Members of highest scoring team get 1 point.
				(try_end),
				(agent_is_alive, ":agent_no"),
				(neg|is_between, ":troop_id", arena_masters_begin, arena_masters_end),#omit tournament master
				
				(try_begin), # AWARD: Cautious Approach (survive a round without scoring a point)
					(troop_slot_eq, ":troop_id", slot_troop_tournament_round_points, 0),
					(ge, "$g_tournament_num_participants_for_fight", tpe_careful_min_participants),
					(troop_set_slot, tpe_award_data, tpe_cautious_approach, ":troop_id"),
					(str_store_troop_name, s1, ":troop_id"),
					(troop_slot_eq, TPE_OPTIONS, tpe_val_opt_awards, 1), # Player option to enable/disable award displays.
					(display_message, "@AWARD GRANTED: {s1} has earned the CAUTIOUS APPROACH award!"),
				(try_end),
				
				### Determine if match merits survivor points ###
				(try_begin),
					(ge, "$g_tournament_num_participants_for_fight", tpe_survival_min_participants),
					(try_begin),
						(eq, "$tpe_tournament_mode", tpe_mode_elimination), ## ELIMINATION MODE ##
						(call_script, "script_tpe_award_point_to_troop", ":troop_id", 10, tpe_point_won_the_round, wp_green), # All surviving members in elimination mode gain 10 points.
					(else_try),
						(call_script, "script_tpe_award_point_to_troop", ":troop_id", 2, tpe_point_won_the_round, wp_green), # All surviving members gain 2 points.
					(try_end),
				(try_end),
				
				# Tally rounds the player survived.
				(try_begin),
					(eq, ":troop_id", "trp_player"),
					(val_add, "$tpe_rounds_survived", 1),
				(try_end),
				
				## ELIMINATION MODE ## - Survivors must be flagged for continuing.
				(try_begin),
					(eq, "$tpe_tournament_mode", tpe_mode_elimination),
					(eq, ":troop_id", "trp_player"), # Prevent other survivors overwriting the message the player sees.
					(troop_set_slot, ":troop_id", slot_troop_tournament_flag_to_continue, 1),
					(assign, "$tpe_rank_1", ":troop_id"),
					(val_add, "$tpe_number_joining", 1),
					(try_begin),
						(ge, "$g_tournament_cur_tier", wp_tpe_max_tournament_tiers),
						(str_store_string, s15, "@Victory is yours!  ^You may continue on.^"),
					(else_try),
						(str_store_string, s15, "@You have won the match ^and will continue on to the ^next round."),
					(try_end),
					
					(agent_get_team, "$temp", ":agent_no"), # Needed below.
				(try_end),
			(try_end),
			
			# Transfer "round points" to the "total points" scores and figure out ranking.  
			# Note: This was moved here for elimination mode changes.
			(call_script, "script_tpe_process_round_points"),
			(call_script, "script_tpe_sort_troops_and_points", slot_troop_tournament_total_points),
			
			## ELIMINATION MODE ## - The rest of the roster needs to be determined.
			# 1st - Survivors are given a pass.  Taken care before this point individually.
			# 2nd - The members of the surviving team are given a pass.
			# 3rd - The members of the highest scoring team are given a pass.
			# 4th - Remaining spots are filled in by the highest scoring people not currently set to continue.
			(try_begin),
				(eq, "$tpe_tournament_mode", tpe_mode_elimination),
				(store_add, ":next_round", "$g_tournament_cur_tier", 1),
				(call_script, "script_tpe_elimination_mode_get_team_sizes", ":next_round"),
				(call_script, "script_tpe_designate_continuing_participants", FTC_TEAM, "$temp"),
				(call_script, "script_tpe_designate_continuing_participants", FTC_TEAM, "$temp_2"),
				(call_script, "script_tpe_designate_continuing_participants", FTC_FILL_REMAINING, -1),
				
				# Assign manual ranking values.
				# (try_begin),
					# (eq, "$g_tournament_cur_tier", 5), # 2nd to last round with 3 opponents.
					# (try_for_agents, ":secondary_agent"),
						# (agent_get_troop_id, ":secondary_troop", ":secondary_agent"),
						# (agent_is_human, ":secondary_agent"),
						# (troop_slot_eq, ":secondary_troop", slot_troop_tournament_flag_to_continue, 0),
						# (assign, "$tpe_rank_3", ":secondary_troop"),
						# ### DIAGNOSTIC ###
						# (str_store_troop_name, s31, ":secondary_troop"),
						# (display_message, "@DEBUG (TPE): Round 5 - rank 3 selection -> {s31}."),
					# (try_end),
					
				# (else_try),
					# (eq, "$g_tournament_cur_tier", 6), # Last round with 2 opponents.
					# (try_for_agents, ":secondary_agent"),
						# (agent_get_troop_id, ":secondary_troop", ":secondary_agent"),
						# (agent_is_human, ":secondary_agent"),
						# (neg|agent_is_alive, ":secondary_agent"),
						# (assign, "$tpe_rank_2", ":secondary_troop"),
						# ### DIAGNOSTIC ###
						# (str_store_troop_name, s31, ":secondary_troop"),
						# (display_message, "@DEBUG (TPE): Round 6 - rank 2 selection -> {s31}."),
					# (try_end),
					
				# (try_end),
				## ERROR CHECK ##
				(lt, "$tpe_number_joining", "$g_tournament_num_participants_for_fight"),
				(assign, reg31, "$tpe_number_joining"),
				(assign, reg32, "$g_tournament_num_participants_for_fight"),
				(display_message, "@ERROR (TPE): Elimination mode did not fill the roster completely.  {reg31} of {reg32} required.", gpu_red),
			(try_end),
			
			# Come up with some progress for the people who didn't get to be in this match.
			(try_begin),
				## PERFORMANCE MODE ##
				(neq, "$tpe_tournament_mode", tpe_mode_elimination),
				(call_script, "script_tpe_score_non_participants"),
			(try_end),
			
			# Tally up difficulty payouts
			(troop_get_slot, ":bid_bonus", TPE_OPTIONS, tpe_val_bet_bid),
			(val_mul, ":bid_bonus", 2),
			(call_script, "script_tpe_get_difficulty_value"),
			(troop_get_slot, ":cumulative_diff", TPE_OPTIONS, tpe_val_cumulative_diff),
			(try_begin),
				(main_hero_fallen),
				(val_div, reg1, 3), # Reduce cumulative difficulty addition by half if you were knocked out.
			(try_end),
			(val_add, ":cumulative_diff", reg1),
			(val_add, ":cumulative_diff", ":bid_bonus"),
			(troop_set_slot, TPE_OPTIONS, tpe_val_cumulative_diff, ":cumulative_diff"),
			
			(get_player_agent_no, ":agent_player"),
			(agent_get_team, ":player_team", ":agent_player"),
			(try_begin),
				(store_remaining_team_no, ":winning_team"),
				(eq, ":winning_team", ":player_team"),
				(neq, "$tpe_trigger_round_end", 1),
				
				# Calculate wager payout.
				(try_begin),
					(troop_get_slot, ":bid", TPE_OPTIONS, tpe_val_bet_bid),
					(troop_get_slot, ":wager", TPE_OPTIONS, tpe_val_bet_wager),
					# Prevent payment if you didn't bid or wager anything.
					(ge, ":bid", 1),
					(ge, ":wager", 1),
					(troop_slot_ge, "trp_player", slot_troop_tournament_round_points, ":bid"),
					# You won, so you get your roundly bet payout.
					(call_script, "script_tpe_calculate_wager_for_bid"),
					(display_message, "@You have earned {reg4} denars for your clever bet this round.", wp_green),
					
					(set_show_messages, 0),
					(troop_add_gold, "trp_player", reg4),
					(val_add, "$tpe_total_earnings", reg4),
					(set_show_messages, 1),
				(try_end),
				
				# End the match.
				#(call_script, "script_play_victorious_sound"),
				(call_script, "script_tpe_end_tournament_fight", 1),
				
				(finish_mission),
			(else_try),
				(call_script, "script_tpe_end_tournament_fight", 0),
				(finish_mission),
			(try_end),
		]),

	# TRIGGER 8: Counts time spent in the current match.
	(1, 0, 0, 
		[
			(eq, "$g_mt_mode", abm_tournament),
		],
		[
			# Count time in the tournament match.
			(val_add, "$g_wp_tpe_timer", 1),
			
			# Updates the match timer display if activated.
			(eq, "$g_wp_tpe_icd_activated", 1),
			(ge, "$g_wp_tpe_timer", 2),
			(store_div, ":minutes", "$g_wp_tpe_timer", 60),
			(store_mod, ":seconds", "$g_wp_tpe_timer", 60),
			(troop_get_slot, ":obj_timer", "trp_tpe_presobj", tpe_obj_match_timer),
			(assign, reg21, ":minutes"),
			(str_clear, s21),
			(try_begin),
				(lt, ":seconds", 10),
				(str_store_string, s21, "@0"),
			(try_end),
			(assign, reg22, ":seconds"),
			(str_store_string, s22, "@{s21}{reg22}"),
			(try_begin),
				(troop_slot_eq, "trp_tpe_presobj", tpe_trigger_enable_icd, 0),
				(is_presentation_active, "prsnt_tpe_team_display"),
				(overlay_set_text, ":obj_timer", "@Match Time - {reg21}:{s22}"),
			(else_try),
				# Attempts to reboot the ICD if it was disabled.
				(neg|is_presentation_active, "prsnt_tpe_team_display"),
				(eq, "$g_wp_tpe_option_icd_active", 1),
				(try_begin),
					(troop_slot_eq, "trp_tpe_presobj", tpe_trigger_enable_icd, 1),
					(troop_set_slot, "trp_tpe_presobj", tpe_trigger_enable_icd, 0),
				(try_end),
				(start_presentation, "prsnt_tpe_team_display"),
				
				# # STAMINA_BAR creation (reboot post disabling)
				# (eq, "$enable_sprinting", 1),
				# (eq, "$block_stamina_bar", 1),
				# ## WINDYPLAINS+ ## - Add the STAMINA BAR to the tournament HUD.
				# (call_script, "script_ce_draw_stamina_bar"),
				# ## WINDYPLAINS- ##
			(try_end),
			
			# Updates the stalemate timer display if activated.
			(troop_slot_eq, "trp_tpe_presobj", tpe_icd_stalemate_active, 1),
			(troop_get_slot, ":time_of_death", "trp_tpe_presobj", tpe_time_of_death),
			(store_sub, ":time_since_death", "$g_wp_tpe_timer", ":time_of_death"),
			(store_sub, ":seconds", wp_tpe_stalemate_timer_limit, ":time_since_death"),
			(troop_get_slot, ":obj_timer", "trp_tpe_presobj", tpe_icd_stalemate_timer),
			(str_clear, s21),
			(try_begin),
				(lt, ":seconds", 10),
				(str_store_string, s21, "@0"),
			(try_end),
			(assign, reg22, ":seconds"),
			(str_store_string, s22, "@{s21}{reg22}"),
			(try_begin),
				(troop_slot_eq, "trp_tpe_presobj", tpe_trigger_enable_icd, 0),
				(is_presentation_active, "prsnt_tpe_team_display"),
				(overlay_set_text, ":obj_timer", "@Stalemate Timer - 0:{s22}"),
			(try_end),
		]),
		
	# TRIGGER 9: Catches the death of a contestant and awards points to victor team/agent, updates displays of points & members.
	(ti_on_agent_killed_or_wounded, 0, 0, 
		[(eq, "$g_mt_mode", abm_tournament),],
		[
			(store_trigger_param_1, ":agent_victim"),
			(store_trigger_param_2, ":agent_killer"),
			
			# Reset the stalemate forced ending timer if active.
			(try_begin),
				(troop_slot_ge, "trp_tpe_presobj", tpe_time_of_death, 0),
				(troop_set_slot, "trp_tpe_presobj", tpe_time_of_death, "$g_wp_tpe_timer"),
				(troop_set_slot, "trp_tpe_presobj", tpe_icd_stalemate_active, 0),
				(try_begin),
					(eq, "$g_wp_tpe_icd_activated", 1),
					(troop_slot_eq, "trp_tpe_presobj", tpe_trigger_enable_icd, 0),
					(is_presentation_active, "prsnt_tpe_team_display"),
					(troop_get_slot, ":obj_timer", "trp_tpe_presobj", tpe_icd_stalemate_timer),
					(str_clear, s31),
					(overlay_set_text, ":obj_timer", "@{s31}"),
				(try_end),
				(ge, DEBUG_TPE_general, 1),
				(assign, reg31, "$g_wp_tpe_timer"),
				(display_message, "@DEBUG (TPE): Stalemate timer reset.  Attack registered at time {reg31} seconds."),
			(try_end),
			
			# Is this a valid kill worth gaining points?
			(agent_is_human, ":agent_victim"),
			(agent_get_team, ":team_victim", ":agent_victim"),
			(agent_get_team, ":team_killer", ":agent_killer"),
			(neq, ":team_killer", ":team_victim"),  # Prevent points gained from friendly kills.
			
			# Award points to killing agent & team.
			(agent_get_troop_id, ":troop_killer", ":agent_killer"),
			(call_script, "script_tpe_award_point_to_troop", ":troop_killer", 1, tpe_point_eliminated_opponent, wp_green),
			(call_script, "script_tpe_update_kill_count", ":troop_killer", 1),
			
			# Announce awarding of points.
			(try_begin),
				(troop_slot_eq, TPE_OPTIONS, tpe_val_opt_teampoints, 1),
				(get_player_agent_no, ":agent_player"),
				(agent_get_team, ":team_player", ":agent_player"),
				(try_begin),
					(eq, ":team_killer", 0),
					(str_store_string, s1, "@red"),
				(else_try),
					(eq, ":team_killer", 1),
					(str_store_string, s1, "@blue"),
				(else_try),
					(eq, ":team_killer", 2),
					(str_store_string, s1, "@green"),
				(else_try),
					(eq, ":team_killer", 3),
					(str_store_string, s1, "@yellow"),
				(try_end),
				
				(try_begin),
					(eq, ":team_killer", ":team_player"),
					(display_message, "@The Tournament Master announces, 'Point awarded to {s1} team for disabling an opponent.'", wp_green),
				(else_try),
					(display_message, "@The Tournament Master announces, 'Point awarded to {s1} team for disabling an opponent.'", wp_red),
				(try_end),
			(try_end),
			
			# Update in combat display (ICD).
			(try_begin),
				(eq, "$g_wp_tpe_option_icd_active", 1),
				(set_fixed_point_multiplier, 1000), # Prevent lifebars from getting crazy sized.
				(troop_slot_eq, "trp_tpe_presobj", tpe_trigger_enable_icd, 0),
				(is_presentation_active, "prsnt_tpe_team_display"),
				(call_script, "script_tpe_update_team_points", ":team_killer"),
				(try_begin),
					(eq, ":team_victim", 0),
					(val_sub, "$g_wp_tpe_team_0_members", 1),
					(store_mul, ":lifebar_length", "$g_wp_tpe_team_0_members", tpe_lifebar_pip_size),
					(val_max, ":lifebar_length", 1),
					# Create outer bar
					(troop_get_slot, ":obj_lifebar_outer", "trp_tpe_presobj", tpe_obj_team_0_outerbar),
					(store_add, ":lifebar_outer", ":lifebar_length", 4),
					(store_mul, ":size_y", tpe_lifebar_outer_width, 50),
					(store_mul, ":size_x", ":lifebar_outer", 50),
					(position_set_y, pos1, ":size_y"),
					(position_set_x, pos1, ":size_x"),
					(overlay_set_size, ":obj_lifebar_outer", pos1),
					# Create inner bar
					(troop_get_slot, ":obj_lifebar", "trp_tpe_presobj", tpe_obj_team_0_lifebar),
					(store_mul, ":size_y", tpe_lifebar_pip_width, 50),
					(store_mul, ":size_x", ":lifebar_length", 50),
					(position_set_y, pos1, ":size_y"),
					(position_set_x, pos1, ":size_x"),
					(overlay_set_size, ":obj_lifebar", pos1),
					
				(else_try),
					(eq, ":team_victim", 1),
					(val_sub, "$g_wp_tpe_team_1_members", 1),
					(store_mul, ":lifebar_length", "$g_wp_tpe_team_1_members", tpe_lifebar_pip_size),
					(val_max, ":lifebar_length", 1),
					# Create outer bar
					(troop_get_slot, ":obj_lifebar_outer", "trp_tpe_presobj", tpe_obj_team_1_outerbar),
					(store_add, ":lifebar_outer", ":lifebar_length", 4),
					(store_mul, ":size_y", tpe_lifebar_outer_width, 50),
					(store_mul, ":size_x", ":lifebar_outer", 50),
					(position_set_y, pos1, ":size_y"),
					(position_set_x, pos1, ":size_x"),
					(overlay_set_size, ":obj_lifebar_outer", pos1),
					# Create inner bar
					(troop_get_slot, ":obj_lifebar", "trp_tpe_presobj", tpe_obj_team_1_lifebar),
					(store_mul, ":size_y", tpe_lifebar_pip_width, 50),
					(store_mul, ":size_x", ":lifebar_length", 50),
					(position_set_y, pos1, ":size_y"),
					(position_set_x, pos1, ":size_x"),
					(overlay_set_size, ":obj_lifebar", pos1),
					
				(else_try),
					(eq, ":team_victim", 2),
					(val_sub, "$g_wp_tpe_team_2_members", 1),
					(store_mul, ":lifebar_length", "$g_wp_tpe_team_2_members", tpe_lifebar_pip_size),
					(val_max, ":lifebar_length", 1),
					# Create outer bar
					(troop_get_slot, ":obj_lifebar_outer", "trp_tpe_presobj", tpe_obj_team_2_outerbar),
					(store_add, ":lifebar_outer", ":lifebar_length", 4),
					(store_mul, ":size_y", tpe_lifebar_outer_width, 50),
					(store_mul, ":size_x", ":lifebar_outer", 50),
					(position_set_y, pos1, ":size_y"),
					(position_set_x, pos1, ":size_x"),
					(overlay_set_size, ":obj_lifebar_outer", pos1),
					# Create inner bar
					(troop_get_slot, ":obj_lifebar", "trp_tpe_presobj", tpe_obj_team_2_lifebar),
					(store_mul, ":size_y", tpe_lifebar_pip_width, 50),
					(store_mul, ":size_x", ":lifebar_length", 50),
					(position_set_y, pos1, ":size_y"),
					(position_set_x, pos1, ":size_x"),
					(overlay_set_size, ":obj_lifebar", pos1),
					
				(else_try),
					(eq, ":team_victim", 3),
					(val_sub, "$g_wp_tpe_team_3_members", 1),
					(store_mul, ":lifebar_length", "$g_wp_tpe_team_3_members", tpe_lifebar_pip_size),
					(val_max, ":lifebar_length", 1),
					# Create outer bar
					(troop_get_slot, ":obj_lifebar_outer", "trp_tpe_presobj", tpe_obj_team_3_outerbar),
					(store_add, ":lifebar_outer", ":lifebar_length", 4),
					(store_mul, ":size_y", tpe_lifebar_outer_width, 50),
					(store_mul, ":size_x", ":lifebar_outer", 50),
					(position_set_y, pos1, ":size_y"),
					(position_set_x, pos1, ":size_x"),
					(overlay_set_size, ":obj_lifebar_outer", pos1),
					# Create inner bar
					(troop_get_slot, ":obj_lifebar", "trp_tpe_presobj", tpe_obj_team_3_lifebar),
					(store_mul, ":size_y", tpe_lifebar_pip_width, 50),
					(store_mul, ":size_x", ":lifebar_length", 50),
					(position_set_y, pos1, ":size_y"),
					(position_set_x, pos1, ":size_x"),
					(overlay_set_size, ":obj_lifebar", pos1),
					
				(try_end),

				(call_script, "script_tpe_icd_ranking"),
			(else_try),
				# Attempts to reboot the ICD if it was disabled.
				(eq, "$g_wp_tpe_option_icd_active", 1),
				(troop_slot_eq, "trp_tpe_presobj", tpe_trigger_enable_icd, 1),
				(troop_set_slot, "trp_tpe_presobj", tpe_trigger_enable_icd, 0),
				(start_presentation, "prsnt_tpe_team_display"),
			(try_end),
			
			## ELIMINATION MODE ##
			# (try_begin),
				# (eq, "$tpe_tournament_mode", tpe_mode_elimination),
				# # Assign manual ranking values.
				# (try_begin),
					# (eq, "$g_tournament_cur_tier", 5), # 2nd to last round with 3 opponents.
					
					# (try_for_agents, ":secondary_agent"),
						# (agent_get_troop_id, ":secondary_troop", ":secondary_agent"),
						# (agent_is_human, ":secondary_agent"),
						# (troop_slot_eq, ":secondary_troop", slot_troop_tournament_flag_to_continue, 0),
						# (assign, "$tpe_rank_3", ":secondary_troop"),
						# ### DIAGNOSTIC ###
						# (str_store_troop_name, s31, ":secondary_troop"),
						# (display_message, "@DEBUG (TPE): Round 5 - rank 3 selection -> {s31}."),
					# (try_end),
					
				# (else_try),
					# (eq, "$g_tournament_cur_tier", 6), # Last round with 2 opponents.
					# (try_for_agents, ":secondary_agent"),
						# (agent_get_troop_id, ":secondary_troop", ":secondary_agent"),
						# (agent_is_human, ":secondary_agent"),
						# (neg|agent_is_alive, ":secondary_agent"),
						# (assign, "$tpe_rank_2", ":secondary_troop"),
						# ### DIAGNOSTIC ###
						# (str_store_troop_name, s31, ":secondary_troop"),
						# (display_message, "@DEBUG (TPE): Round 6 - rank 2 selection -> {s31}."),
					# (try_end),
					
				# (try_end),
			# (try_end),
			
			# QUEST UPDATE: "A Score to Settle" needs to be updated if applicable.
			(try_begin),
				(check_quest_active, "qst_score_to_settle"),
				# Qualify if this is our intended target.
				(agent_get_troop_id, ":troop_victim", ":agent_victim"),
				(quest_slot_eq, "qst_score_to_settle", slot_quest_target_troop, ":troop_victim"), # Is this the intended target?
				(agent_get_troop_id, ":troop_killer", ":agent_killer"), # This is performed earlier in the script as well.
				(eq, ":troop_killer", "trp_player"),                    # Is the player the one scoring the knockout?
				# Update the quest stage if applicable.
				(quest_get_slot, ":quest_stage", "qst_score_to_settle", slot_quest_current_state),
				(is_between, ":quest_stage", qp1_score_to_settle_begun, qp1_score_to_settle_defeated_thrice),
				(val_add, ":quest_stage", 1),
				(quest_set_slot, "qst_score_to_settle", slot_quest_current_state, ":quest_stage"),
				(call_script, "script_quest_score_to_settle", floris_quest_update),
			(try_end),
		]),

	# TRIGGER 10: Allows you to see the damage dealt by your teammates.
	(ti_on_agent_hit, 0, 0, [
		(eq, "$g_mt_mode", abm_tournament),
		(eq, "$g_wp_tpe_option_team_damage", 1),
		], 
		[
			# Trigger Param 1: damage inflicted agent_id
			# Trigger Param 2: damage dealer agent_id
			# Trigger Param 3: inflicted damage
			(store_trigger_param_1, ":agent_victim"),
			(store_trigger_param_2, ":agent_attacker"),
			(store_trigger_param_3, ":damage"),
			## TPE 1.5.2+ ##
			(assign, ":weapon", reg0), 
			(ge, ":damage", 1),
			## TPE 1.5.2- ##
			
			# Figure out player's team.
			(get_player_agent_no, ":agent_player"),
			(agent_get_team, ":team_player", ":agent_player"),
			(neq, ":agent_player", ":agent_attacker"), # Remove player mirroring messages.
			
			# Determine if attacker was from same team as player.
			(agent_get_team, ":team_attacker", ":agent_attacker"),
			(eq, ":team_attacker", ":team_player"),
			
			# Qualify the victim.
			(agent_is_human, ":agent_victim"), # I don't care about horse damage.
			
			# Display information.
			(agent_get_troop_id, ":troop_attacker", ":agent_attacker"),
			(agent_get_troop_id, ":troop_victim", ":agent_victim"),
			(str_store_troop_name, s31, ":troop_attacker"),
			(str_store_troop_name, s32, ":troop_victim"),
			(assign, reg31, ":damage"),
			(str_store_item_name, s33, ":weapon"), ## TPE 1.5.2 ##
			(display_message, "@Your ally, {s31}, delivers {reg31} damage to {s32}. ({s33})", wp_green),
		]),
		
	# TRIGGER 11: Initialization trigger that happens EACH ROUND.
	(ti_after_mission_start, 0, ti_once, 
		[(eq, "$g_mt_mode", abm_tournament),
		(assign, "$g_wp_tpe_icd_activated", 0),],
		[
			(assign, "$g_wp_tpe_icd_activated", 0),
			(assign, "$tpe_trigger_round_end", 0),
			
			# Assign an initial following team for the death camera.
			## DISABLE FOR NATIVE OSP+ ##
			(try_begin),
				(eq, MOD_PBOD_INSTALLED, 1), # (dependency) PBOD - Custom camera
				(get_player_agent_no, ":agent_player"),
				(agent_get_team, ":team_player", ":agent_player"),
				(assign, "$fplayer_team_no", ":team_player"),
				(assign, "$fplayer_agent_no", ":agent_player"),
			(try_end),
			## DISABLE FOR NATIVE OSP- ##
			
			# Reset team point tallies.
			(troop_set_slot, "trp_tpe_presobj", tpe_icd_team_0_points, 0),
			(troop_set_slot, "trp_tpe_presobj", tpe_icd_team_1_points, 0),
			(troop_set_slot, "trp_tpe_presobj", tpe_icd_team_2_points, 0),
			(troop_set_slot, "trp_tpe_presobj", tpe_icd_team_3_points, 0),
			
			# Reset points for all participants.
			(try_for_range, ":slot_no", 0, wp_tpe_max_tournament_participants),
				(troop_get_slot, ":troop_no", tpe_tournament_roster, ":slot_no"),
				(troop_set_slot, ":troop_no", slot_troop_tournament_round_points, 0),
				(troop_set_slot, ":troop_no", slot_troop_tournament_participating, 0),
				
				## ELIMINATION MODE ## - Troop scores should get reset to 0 each round since people eliminated do not get a chance to participate.
				# (eq, "$tpe_tournament_mode", tpe_mode_elimination),
				# (troop_set_slot, ":troop_no", slot_troop_tournament_total_points, 0),
			(try_end),
			(troop_set_slot, "trp_player", slot_troop_tournament_round_points, 0), # For some reason player isn't getting caught above.
			
			# Reset award data for the round.
			(try_for_range, ":award_slot", tpe_awards_begin, tpe_awards_end),
				(troop_set_slot, tpe_award_data, ":award_slot", -1),
			(try_end),
			(troop_set_slot, tpe_award_data, tpe_kill_count, 0),
			(troop_set_slot, tpe_award_data, tpe_award_display_passes, 0),
			
			# Set everyone who actually made it into the round as participating.
			(try_for_agents, ":agent_no"),
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				(troop_set_slot, ":troop_no", slot_troop_tournament_participating, 1),
			(try_end),
			
			# Reset the stalemate timer to 0.
			(troop_set_slot, "trp_tpe_presobj", tpe_time_of_death, 0),
			
			# Flag everyone as not continuing to support elimination mode.  Left always happening since it shouldn't hurt anything.
			(call_script, "script_tpe_designate_continuing_participants", FTC_RESET, -1), 
			(assign, "$tpe_number_joining", 0),
			
			# Create in-combat display.
			(try_begin),
				(eq, "$g_wp_tpe_option_icd_active", 1),
				(start_presentation, "prsnt_tpe_team_display"),
			(try_end),
		]),

	# TRIGGER 12: Initialization trigger that happens ONCE PER TOURNAMENT.
	(ti_before_mission_start, 0, ti_once, 
		[
			(eq, "$g_mt_mode", abm_tournament),
			(eq, "$g_tournament_cur_tier", 1),
		],
		[
			# Reset points for all participants.
			(try_for_range, ":slot_no", 0, wp_tpe_max_tournament_participants),
				(troop_get_slot, ":troop_no", "trp_tournament_participants", ":slot_no"),
				(troop_set_slot, ":troop_no", slot_troop_tournament_round_points, 0),
				(troop_set_slot, ":troop_no", slot_troop_tournament_total_points, 0),
			(try_end),
			
			# Reset total earnings.
			(assign, "$tpe_rounds_survived", 0),
			(assign, "$tpe_trigger_round_end", 0),
		]),
		
	# TRIGGER 13: Equip "native gear" scaled troops in appropriate colors.
	(ti_after_mission_start, 0, ti_once, 
		[(eq, "$g_mt_mode", abm_tournament),
		(eq, wp_tpe_mod_opt_actual_gear, 1),],
		[
			(try_for_agents, ":agent_no"),
				(agent_is_human, ":agent_no"),
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				(is_between, ":troop_no", tpe_scaled_troops_begin, tpe_scaled_troops_end), # Is it a scaled troop.
				(agent_get_team, ":agent_team", ":agent_no"),
				(store_add, ":armor_body", wp_tpe_enhanced_armor, ":agent_team"),
				(store_add, ":armor_helm", wp_tpe_enhanced_helmet, ":agent_team"),
				(agent_equip_item, ":agent_no", ":armor_body"),
				(agent_equip_item, ":agent_no", ":armor_helm"),
				(agent_equip_item, ":agent_no", wp_tpe_enhanced_boots),
			(try_end),
		]),
		
	# TRIGGER 14: Player dies, round continues.  Warning of this feature to the player.
	(0, 0, ti_once, [(main_hero_fallen),],
		[
			(display_message, "@You have fallen during this round, but will be able to continue onto the next round when only one team remains."),
			(troop_set_slot, "trp_tpe_presobj", tpe_time_of_death, "$g_wp_tpe_timer"),
			## DISABLE FOR NATIVE OSP+ ##
			(try_begin),
				(eq, MOD_PBOD_INSTALLED, 1), # (dependency) PBOD - Custom camera
				(display_message, "@You may move your camera around using the arrow keys."),
				# Sets up camera for free movement.
				(call_script, "script_cust_cam_init_death_cam", cam_mode_free),
			(try_end),
			## DISABLE FOR NATIVE OSP-
		]),
	
	# TRIGGER 15: Player dies triggering a countdown timer to prevent infinite matches due to AI stupidity or game glitch.
	(1, 0, 0, [(main_hero_fallen),],
	    [
			(troop_get_slot, ":time_of_death", "trp_tpe_presobj", tpe_time_of_death),
			(store_sub, ":time_since_death", "$g_wp_tpe_timer", ":time_of_death"),
			(store_sub, ":countdown_limit", wp_tpe_stalemate_timer_limit, 10),
			(ge, ":time_since_death", ":countdown_limit"),
			(store_sub, reg1, wp_tpe_stalemate_timer_limit, ":time_since_death"),
			(troop_set_slot, "trp_tpe_presobj", tpe_icd_stalemate_active, 1),
			#(display_message, "@Stalemate defected.  Match will be closed in {reg1} seconds."),
			(ge, ":time_since_death", wp_tpe_stalemate_timer_limit),
			(assign, "$tpe_trigger_round_end", 1),
			# (call_script, "script_tpe_end_tournament_fight", 0),
			# (finish_mission),
		]),
	
	# TRIGGER 16: This trigger tries to capture an attempt to change screens to prevent log spam on the ICD presentation.
	(0, 0, 0, 
		[
			(eq, "$g_wp_tpe_option_icd_active", 1),
			(this_or_next|game_key_clicked, gk_game_log_window),
			(this_or_next|game_key_clicked, gk_quests_window),
			(game_key_clicked, gk_character_window),
			(neg|key_clicked, key_s), # Beats me why 's' is triggering this at all.
		],
	    [
			# (display_message, "@DEBUG: A GAMEKEY WAS CLICKED THAT CAUSED ICD TO DISABLE!!!!"),
			(troop_set_slot, "trp_tpe_presobj", tpe_trigger_enable_icd, 1),
			(assign, "$block_stamina_bar", 1),
			(assign, "$obj_stamina_bar", -1),
			(try_begin), ### DIAGNOSTIC+ ###
				(ge, DEBUG_STAMINA, 1),
				(assign, reg31, "$block_stamina_bar"),
				(display_message, "@DEBUG (Stamina): Stamina bar has been {reg31?BLOCKED:unblocked} @ trigger_escape_key (tournament)", gpu_debug), ## DEBUG: STAMINA_BAR
			(try_end), ### DIAGNOSTIC- ###
		]),
		
	# TRIGGER 17: Attempts to fix the riderless horse immunity bug.
	(20, 0, 0, 
		[
			(eq, "$g_mt_mode", abm_tournament),
		], 
		[
			(try_for_agents, ":agent_no"),
				
				# Qualify the victim.
				(neg|agent_is_human, ":agent_no"),                    # I only want horses.
				(agent_get_rider, ":agent_rider", ":agent_no"),
				(agent_is_alive, ":agent_no"),                        # No point in beating a dead horse :)
				(eq, ":agent_rider", -1),                             # Returned if there is no rider for the horse.
				(agent_get_item_id, ":item_horse", ":agent_no"),
				(remove_agent, ":agent_no"),
				(ge, DEBUG_TPE_general, 2),                           # Diagnostic information if debug turned on.
				(str_store_item_name, s32, ":item_horse"),
				(assign, reg31, ":agent_no"),
				(display_message, "@DEBUG (TPE): Horse '{s32}' #{reg31} is riderless and will be removed."),
			(try_end),
		]),
		
	# TRIGGER 18: ICD Reboot & HP Update : (dependency) Custom Commander
	(0, 0, 0, 
		[(eq, "$g_mt_mode", abm_tournament),], 
		[
			(try_begin),
				(is_presentation_active, "prsnt_tpe_team_display"),
				(eq, "$g_wp_tpe_option_icd_active", 1),
				(troop_slot_eq, "trp_tpe_presobj", tpe_trigger_enable_icd, 0),
				# (eq, MOD_CUSTOM_COMMANDER_INSTALLED, 1), # Dependency (Custom Commander)
				# (troop_slot_eq, TPE_OPTIONS, tpe_val_show_health, 1), # Default display option.
				# (call_script, "script_update_agent_hp_bar"),
			(try_end),
		]),
		
	# TRIGGER 19: Amps up competitors based upon their current total score to make them more consistent.
	(ti_on_agent_hit, 0, 0, 
		[(eq, "$g_mt_mode", abm_tournament),], 
		[
			# Trigger Param 1: damage inflicted agent_id
			# Trigger Param 2: damage dealer agent_id
			# Trigger Param 3: inflicted damage
			(store_trigger_param_1, ":agent_victim"),
			(store_trigger_param_2, ":agent_attacker"),
			(store_trigger_param_3, ":raw_damage"),
			
			# Prevent this from directly harming the player.
			(get_player_agent_no, ":agent_player"),
			(neq, ":agent_attacker", ":agent_player"),
			(neq, ":agent_victim", ":agent_player"),
			
			
			# Qualify the victim.
			(agent_is_human, ":agent_victim"), # I don't care about horse damage.
			(agent_get_troop_id, ":troop_victim", ":agent_victim"),
			(troop_get_slot, ":points_total", ":troop_victim", slot_troop_tournament_total_points),
			(troop_get_slot, ":points_round", ":troop_victim", slot_troop_tournament_round_points),
			(store_add, ":buff_victim", ":points_total", ":points_round"),
			(val_mul, ":buff_victim", 4),
			(val_min, ":buff_victim", 60),
			
			# Qualify the attacker.
			(agent_get_troop_id, ":troop_attacker", ":agent_attacker"),
			(troop_get_slot, ":points_total", ":troop_attacker", slot_troop_tournament_total_points),
			(troop_get_slot, ":points_round", ":troop_attacker", slot_troop_tournament_round_points),
			(store_add, ":buff_attacker", ":points_total", ":points_round"),
			(val_mul, ":buff_attacker", 4),
			(val_min, ":buff_attacker", 60),
			
			# Determine difference in buffs (positive value should improve damage, negative value should lower it).
			(store_sub, ":percent_taken", ":buff_attacker", ":buff_victim"),
			
			# Determine damage absorption.
			(store_mul, ":bonus_damage", ":raw_damage", ":percent_taken"),
			(val_div, ":bonus_damage", 100),
			(store_add, ":damage", ":raw_damage", ":bonus_damage"),
			
			# Display information.
			(try_begin),
				(ge, DEBUG_TPE_ai_behavior, 1),
				(neq, ":percent_taken", 0), # No point in showing this.
				(neq, ":raw_damage", ":damage"),
				(str_store_troop_name, s2, ":troop_victim"),
				(str_store_troop_name, s3, ":troop_attacker"),
				(assign, reg1, ":raw_damage"),
				(assign, reg2, ":damage"),
				(assign, reg4, ":buff_attacker"),
				(assign, reg5, ":buff_victim"),
				(display_message, "@DEBUG (TPE AI): Vic {s2}/{reg5} takes {reg1}->{reg2} damage. Att {s3}/{reg4}", gpu_debug),
			(try_end),
			
			# Add in additional limiter for champions.
			(try_begin),
				(is_between, ":troop_victim", tpe_scaled_champions_begin, tpe_scaled_champions_end),
				(assign, ":initial_damage", ":damage"),
				(troop_get_slot, ":difficulty", TPE_OPTIONS, tpe_val_diff_setting),
				(store_sub, ":limiter", 24, ":difficulty"),
				(store_sub, ":percent_absorbed", wp_tpe_champion_damage_absorb_factor, ":limiter"),
				(store_sub, ":percent_taken", 100, ":percent_absorbed"),
				(store_mul, ":damage", ":initial_damage", ":percent_taken"),
				(val_div, ":damage", 100),
				### DIAGNOSTIC ###
				(ge, DEBUG_TPE_ai_behavior, 1),
				(neq, ":initial_damage", ":damage"),
				(ge, ":damage", 1),
				(str_store_troop_name, s2, ":troop_victim"),
				(assign, reg1, ":initial_damage"),
				(assign, reg2, ":damage"),
				(display_message, "@DEBUG (TPE AI): {s2} receives {reg2} damage reduced from {reg1}.", gpu_debug),
			(try_end),
			
			# Return new damage result.
			(set_trigger_result, ":damage"),
		]),
		
	# TRIGGER 20: Improves damage done by and reduces damage done to companions or lords based on their level to level them out with the enhanced AI.
	(ti_on_agent_hit, 0, 0, 
		[
			(eq, "$g_mt_mode", abm_tournament),
		], 
		[
			# Trigger Param 1: damage inflicted agent_id
			# Trigger Param 2: damage dealer agent_id
			# Trigger Param 3: inflicted damage
			(store_trigger_param_1, ":agent_victim"),
			(store_trigger_param_2, ":agent_attacker"),
			(store_trigger_param_3, ":initial_damage"),
			
			# DISQUALIFY ATTACKS FROM OR AGAINST THE PLAYER
			(get_player_agent_no, ":agent_player"), # Prevent this from hurting the player's gameplay.
			(neq, ":agent_victim", ":agent_player"),
			(neq, ":agent_attacker", ":agent_player"),
			
			(assign, ":use_new_value", 0),
			
			(try_begin),
				### REDUCE DAMAGE TAKEN ###
				# Qualify the victim.
				(agent_is_human, ":agent_victim"), # I don't care about horse damage.
				(agent_get_troop_id, ":troop_victim", ":agent_victim"),
				(is_between, ":troop_victim", active_npcs_begin, active_npcs_end),
				
				# Determine damage absorption.
				(store_character_level, ":level", ":troop_victim"),
				(store_sub, ":limiter", tpe_lord_and_companion_damage_soak_lvl, ":level"),
				(val_max, ":limiter", 0),
				(store_mul, ":percent_absorbed", 2, ":limiter"),
				(store_sub, ":percent_taken", 100, ":percent_absorbed"),
				(store_mul, ":modified_damage", ":initial_damage", ":percent_taken"),
				(val_div, ":modified_damage", 100),
				
				# Display information.
				(try_begin),
					(ge, DEBUG_TPE_ai_behavior, 2),
					(str_store_troop_name, s2, ":troop_victim"),
					(assign, reg1, ":initial_damage"),
					(assign, reg2, ":modified_damage"),
					(display_message, "@DEBUG (TPE AI): {s2} receives {reg2} damage reduced from {reg1}.", wp_green),
				(try_end),
				(assign, ":use_new_value", 1),
			(try_end),
			
			(try_begin),
				### IMPROVE DAMAGE DELIVERED ###
				# Qualify the victim.
				(agent_is_human, ":agent_attacker"), # I don't care about horse damage.
				(agent_get_troop_id, ":troop_attacker", ":agent_attacker"),
				(is_between, ":troop_attacker", active_npcs_begin, active_npcs_end),
				
				# Determine damage boost.
				(store_character_level, ":level", ":troop_attacker"),
				(store_sub, ":bonus", tpe_lord_and_companion_damage_bonus_lvl, ":level"),
				(val_mul, ":bonus", 2),
				(val_max, ":bonus", 0),
				
				(store_mul, ":modified_damage", ":initial_damage", ":bonus"),
				(val_div, ":modified_damage", 100),
				(val_add, ":modified_damage", ":initial_damage"),
				
				# Display information.
				(try_begin),
					(ge, DEBUG_TPE_ai_behavior, 2),
					(str_store_troop_name, s2, ":troop_attacker"),
					(assign, reg1, ":initial_damage"),
					(assign, reg2, ":modified_damage"),
					(display_message, "@DEBUG (TPE AI): {s2} delivers {reg2} damage increased from {reg1}.", wp_green),
				(try_end),
				(assign, ":use_new_value", 1),		
			(try_end),
			
			# Return new damage result.
			(eq, ":use_new_value", 1),
			(set_trigger_result, ":modified_damage"),
		]),
		
	# TRIGGER 21: Optional ability to leave a tournament even after you die, but everyone gains points for surviving.
	(ti_tab_pressed, 0, 0, [(main_hero_fallen),],
		[
			(try_begin),
				(eq, "$g_mt_mode", abm_visit),
				(set_trigger_result, 1),
			(else_try),
				(question_box,"@Do you wish to exit?  Doing so will cause all surviving competitors to gain 3 points."),
			(try_end),
		]),
	
	# TRIGGER 22
	(ti_question_answered, 0, 0, [(main_hero_fallen),],
		[
			(store_trigger_param_1,":answer"),
			(eq,":answer",0),
			(try_begin),
				### Determine if match merits survivor points ###
				(try_for_agents, ":agent_no"),
					(agent_is_human, ":agent_no"),
					(agent_is_alive, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(call_script, "script_tpe_award_point_to_troop", ":troop_no", 3, tpe_point_won_the_round, wp_green), # All surviving members gain 3 points.
				(try_end),
			(try_end),
			(assign, "$tpe_trigger_round_end", 1),
		]),
		
	# TRIGGER 23: Shield Bash (dependency) PBOD
	## DISABLE FOR NATIVE OSP+ ##
	shield_bash,
	shield_bash_ai,
	shield_bash_ai_cooldown,
	## DISABLE FOR NATIVE OSP- ##
		
################
# END TRIGGERS #
################
]
	
	
tpe_tournament_triggers = [
(
    "tpe_tournament_standard",mtf_arena_fight,-1,
    "You enter a melee fight in the arena.",
    [
	  (0,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[]),
	  (1,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[]),
	  (2,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[]),
	  (3,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[]),
	  (4,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[]),
	  (5,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[]),
	  (6,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[]),
	  (7,mtef_visitor_source|mtef_team_0,af_override_all,aif_start_alarmed,1,[]),

	  (8,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[]),
	  (9,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[]),
	  (10,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[]),
	  (11,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[]),
	  (12,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[]),
	  (13,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[]),
	  (14,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[]),
	  (15,mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[]),

	  (16,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[]),
	  (17,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[]),
	  (18,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[]),
	  (19,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[]),
	  (20,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[]),
	  (21,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[]),
	  (22,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[]),
	  (23,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[]),

	  (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[]),
	  (25,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[]),
	  (26,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[]),
	  (27,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[]),
	  (28,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[]),
	  (29,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[]),
	  (30,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[]),
	  (31,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[]),
#32
      # (32, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy]),
      # (33,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      # (34,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_practice_shield]),
      # (35,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      # (36, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows, itm_practice_dagger]),
      # (37,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_practice_shield]),
      # (38,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy]),
      # (39,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
# #40-49 not used yet
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_dagger, itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_practice_shield,itm_arena_tunic_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy,itm_practice_horse,itm_arena_tunic_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),

      # (50, mtef_scene_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (51, mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (52, mtef_visitor_source,af_override_horse,0,1,[]),
# #not used yet:
      (53, mtef_scene_source,af_override_horse,0,1,[]),(54, mtef_scene_source,af_override_horse,0,1,[]),(55, mtef_scene_source,af_override_horse,0,1,[]),
# #used for torunament master scene

      # (56, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_ar_rho_t3_aketon_a, itm_he_swa_t3_helmet_a]),
      # (57, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_ar_rho_t3_aketon_a, itm_he_swa_t3_helmet_a]),
	],
    tpe_standard_triggers + custom_camera_triggers # (dependency) PBOD
  ),
  
(
    "tpe_tournament_native_gear",mtf_arena_fight,-1,
    "You enter a melee fight in the arena.",
    [
	  (0,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
	  (1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
	  (2,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
	  (3,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
	  (4,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
	  (5,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
	  (6,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),
	  (7,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),

	  (8,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
	  (9,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
	  (10,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
	  (11,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
	  (12,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
	  (13,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
	  (14,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),
	  (15,mtef_visitor_source|mtef_team_1,0,aif_start_alarmed,1,[]),

	  (16,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
	  (17,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
	  (18,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
	  (19,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
	  (20,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
	  (21,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
	  (22,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),
	  (23,mtef_visitor_source|mtef_team_2,0,aif_start_alarmed,1,[]),

	  (24,mtef_visitor_source|mtef_team_3,0,aif_start_alarmed,1,[]),
	  (25,mtef_visitor_source|mtef_team_3,0,aif_start_alarmed,1,[]),
	  (26,mtef_visitor_source|mtef_team_3,0,aif_start_alarmed,1,[]),
	  (27,mtef_visitor_source|mtef_team_3,0,aif_start_alarmed,1,[]),
	  (28,mtef_visitor_source|mtef_team_3,0,aif_start_alarmed,1,[]),
	  (29,mtef_visitor_source|mtef_team_3,0,aif_start_alarmed,1,[]),
	  (30,mtef_visitor_source|mtef_team_3,0,aif_start_alarmed,1,[]),
	  (31,mtef_visitor_source|mtef_team_3,0,aif_start_alarmed,1,[]),
#32
      # (32, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy]),
      # (33,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      # (34,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_practice_shield]),
      # (35,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
      # (36, mtef_visitor_source|mtef_team_1,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows, itm_practice_dagger]),
      # (37,mtef_visitor_source|mtef_team_2,af_override_all,aif_start_alarmed,1,[itm_practice_sword, itm_practice_shield]),
      # (38,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy]),
      # (39,mtef_visitor_source|mtef_team_4,af_override_all,aif_start_alarmed,1,[itm_practice_staff]),
# #40-49 not used yet
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_dagger, itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword,itm_practice_shield,itm_arena_tunic_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_sword_heavy,itm_practice_horse,itm_arena_tunic_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_lance,itm_practice_shield,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),
      # (24,mtef_visitor_source|mtef_team_3,af_override_all,aif_start_alarmed,1,[itm_practice_bow,itm_practice_arrows,itm_practice_horse,itm_arena_tunic_yellow, itm_tourney_helm_yellow]),

      # (50, mtef_scene_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (51, mtef_visitor_source,af_override_horse|af_override_weapons|af_override_head,0,1,[]),
      (52, mtef_visitor_source,af_override_horse,0,1,[]),
# #not used yet:
      (53, mtef_scene_source,af_override_horse,0,1,[]),(54, mtef_scene_source,af_override_horse,0,1,[]),(55, mtef_scene_source,af_override_horse,0,1,[]),
#used for torunament master scene

      # (56, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_ar_rho_t3_aketon_a, itm_he_swa_t3_helmet_a]),
      # (57, mtef_visitor_source|mtef_team_0, af_override_all, aif_start_alarmed, 1, [itm_practice_sword, itm_practice_shield, itm_ar_rho_t3_aketon_a, itm_he_swa_t3_helmet_a]),
	],
    tpe_standard_triggers + custom_camera_triggers # (dependency) PBOD
  ),

]
		
# def modmerge_mission_templates(orig_mission_templates):
	# find_i = find_object( orig_mission_templates, "arena_melee_fight" )
	# orig_mission_templates[find_i][5].extend(AI_triggers)

def modmerge_mission_templates(orig_mission_templates, check_duplicates = False):
    if( not check_duplicates ):
        orig_mission_templates.extend(tpe_tournament_triggers) # Use this only if there are no replacements (i.e. no duplicated item names)
    else:
    # Use the following loop to replace existing entries with same id
        for i in range (0,len(tpe_tournament_triggers)-1):
          find_index = find_object(orig_mission_templates, tpe_tournament_triggers[i][0]); # find_object is from header_common.py
          if( find_index == -1 ):
            orig_mission_templates.append(tpe_tournament_triggers[i])
          else:
            orig_mission_templates[find_index] = tpe_tournament_triggers[i]
			
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