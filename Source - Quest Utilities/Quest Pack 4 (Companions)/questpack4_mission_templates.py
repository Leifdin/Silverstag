# Quest Pack 4 (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from module_mission_templates import *
from module_items import *
from module_sounds import *
from pbod_mission_templates import *
from combat_mission_templates import *

mission_triggers = [
(
    "odval_challenge",0,mtf_battle_mode,
    "village center",
    [(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (2,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (3,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (4,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (5,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
     (6,mtef_visitor_source,af_override_horse,0,1,[]), # Skirmishers
     (7,mtef_visitor_source,af_override_horse,0,1,[]),
     (8,mtef_visitor_source,af_override_horse,0,1,[]),
     (9,mtef_visitor_source,af_override_horse,0,1,[]),
	 (10,mtef_visitor_source,af_override_horse,0,1,[]),
	 (11,mtef_visitor_source,af_override_horse,0,1,[]),
	 (12,mtef_visitor_source,af_override_horse,0,1,[]),
	 (13,mtef_visitor_source,af_override_horse,0,1,[]), # Elder in the field.
	 (14,mtef_visitor_source,af_override_horse,0,1,[]), # Spectators
	 (15,mtef_visitor_source,af_override_horse,0,1,[]), # Spectators
	 (16,mtef_visitor_source,af_override_horse,0,1,[]), # Spectators
	 (17,mtef_visitor_source,af_override_horse,0,1,[]), # Spectators
	 (18,mtef_visitor_source,af_override_horse,0,1,[]), # Spectators
	 (19,mtef_visitor_source,af_override_horse,0,1,[]), # Spectators
	 (20,mtef_visitor_source,af_override_horse,0,1,[]), # Spectators
	 
	],
    [
		# COMMON TRIGGER: Initalize globals.
		(ti_before_mission_start, 0, ti_once, 
			[], 
			[
				# Initialize our global variables.
				(assign, "$timer_active", 0),
				(assign, "$fight_timer", 0),
				(assign, "$agent_elder", -1),
				(assign, reg55, 0), # used to check when Odval is wounded.
				
				(party_get_slot, ":troop_village_elder", qp4_odval_home_town, slot_town_elder),
				(set_spawn_radius, 1),
				(add_visitors_to_current_scene, 13, ":troop_village_elder", 1, 0, 0),
				# (set_spawn_radius, 2),
				# (add_visitors_to_current_scene, 7, "trp_khergit_townsman", 3, 0, 0), # Spectator
				# (set_spawn_radius, 2),
				# (add_visitors_to_current_scene, 7, "trp_khergit_townswoman", 2, 0, 0), # Spectator
				### SPECTATORS ###
				(try_for_range, ":entry_point", 14, 21),
					(set_spawn_radius, 2),
					(store_random_in_range, ":total", 3, 6),
					(store_random_in_range, ":men", 1, 4),
					(add_visitors_to_current_scene, ":entry_point", "trp_khergit_townsman", ":men", 0, 0), # Spectator
					(set_spawn_radius, 2),
					(store_sub, ":women", ":total", ":men"),
					(ge, ":women", 1),
					(add_visitors_to_current_scene, ":entry_point", "trp_khergit_townswoman", ":women", 0, 0), # Spectator
				(try_end),
			]),
		
		# COMMON TRIGGER: Have townsfolk watch the player's movements.
		(0.5, 0, 0, 
			[
				# (eq, "$timer_active", 2),
				# (ge, "$fight_timer", 3),
			], 
			[
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(this_or_next|eq, ":troop_no", "trp_khergit_townsman"),
					(this_or_next|eq, ":troop_no", "trp_khergit_townswoman"),
					(eq, ":agent_no", "$agent_elder"),
					
					(store_random_in_range, ":turn_chance", 0, 100),
					(this_or_next|lt, ":turn_chance", 20),
					(eq, ":agent_no", "$agent_elder"),
					
					(get_player_agent_no, ":agent_player"),
					(agent_get_position, pos10, ":agent_player"),
					(agent_set_look_target_position, ":agent_no", pos10),
					
					(neq, ":agent_no", "$agent_elder"),
					(store_random_in_range, ":pose", "anim_pose_1", "anim_wedding_guest"),
					(agent_set_animation, ":agent_no", ":pose"),
					(eq, "$timer_active", 1),
					(lt, ":turn_chance", 5),
					(troop_get_type, ":gender", ":troop_no"),
					(try_begin),
						(eq, ":gender", 0),
						(agent_play_sound, ":agent_no", "snd_man_warcry"),
					(try_end),
				(try_end),
			]),
			
		# COMMON TRIGGER: Move our spawned actors to the right team and starting place.
		(ti_on_agent_spawn, 0, 0, [], 
			[
				(store_trigger_param_1, ":agent_no"),
				
				(try_begin),
					(ge, DEBUG_QUEST_PACK_4, 2),
					(assign, reg31, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(str_store_troop_name, s33, ":troop_no"),
					(display_message, "@DEBUG (QP4): Actor '{s33}' spawned as agent #{reg31}."),
				(try_end),
				
				# Figure out what agent our village elder is.
				(party_get_slot, ":troop_village_elder", qp4_odval_home_town, slot_town_elder),
				(try_begin),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(eq, ":troop_no", ":troop_village_elder"),
					(assign, "$agent_elder", ":agent_no"),
					(ge, DEBUG_QUEST_PACK_4, 2),
					(display_message, "@DEBUG (QP4): Village elder actor assigned."),
				(try_end),
				
				# Make sure this isn't our story line character.
				(call_script, "script_qp4_add_storyline_characters"),
				#(assign, ":story_troop_no", reg41),
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				
				# Setup our agent to not be on the player's side.
				(try_begin),
					(neq, ":troop_no", "trp_khergit_townsman"),
					(neq, ":troop_no", "trp_khergit_townswoman"),
					
					(agent_set_team, ":agent_no", 0),
				(else_try),
					(store_random_in_range, ":pose", "anim_pose_1", "anim_wedding_guest"),
					(agent_set_animation, ":agent_no", ":pose"),
				(try_end),
			]),
		
		# COMMON TRIGGER: Check if NPC_Odval is wounded.
		(ti_on_agent_killed_or_wounded, 0, 0, 
			[(eq, reg55, 0),], 
			[
				(store_trigger_param_1, ":agent_no"),
				
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				(eq, ":troop_no", NPC_Odval),
				(agent_is_wounded, ":agent_no"),
				(assign, reg55, 1),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(str_store_troop_name, s14, NPC_Odval),
				(display_message, "@DEBUG (QP4): {s14} has fallen in battle."),
			]),
				
		# COMMON TRIGGER: Timer Pulse.
		(1, 0, 0, 
			[
				(ge, "$timer_active", 1),
				(neg|conversation_screen_is_active),
			], 
			[
				(val_add, "$fight_timer", 1),
				
				(eq, "$timer_active", 1),
				(eq, reg55, 0),
				
				(neg|troop_is_wounded, NPC_Odval),
				(str_store_troop_name, s14, NPC_Odval),
				(troop_get_type, reg3, NPC_Odval),
				(try_begin),
					(check_quest_active, "qst_odval_accept_the_challenge"),
					(str_store_string, s1, "str_qp4_odval_betrayed_judge_male"),
					(str_store_string, s2, "str_qp4_odval_betrayed_judge_female"),
					(str_store_string, s3, "str_qp4_odval_second_place_finisher"),
					(str_store_string, s4, "str_qp4_odval_third_place_finisher"),
					
					(try_begin),		(eq, "$fight_timer", 5),	(display_message, "str_qp4_challenge_trash_talk_1"),
						(else_try),		(eq, "$fight_timer", 7),	(display_message, "str_qp4_challenge_trash_talk_2"),
						(else_try),		(eq, "$fight_timer", 11),	(display_message, "str_qp4_challenge_trash_talk_3"),
						(else_try),		(eq, "$fight_timer", 13),	(display_message, "str_qp4_challenge_trash_talk_4"),
						(else_try),		(eq, "$fight_timer", 18),	(display_message, "str_qp4_challenge_trash_talk_5"),
						(else_try),		(eq, "$fight_timer", 21),	(display_message, "str_qp4_challenge_trash_talk_6"),
						(else_try),		(eq, "$fight_timer", 24),	(display_message, "str_qp4_challenge_trash_talk_7"),
					(try_end),
				(else_try),
					(check_quest_active, "qst_odval_saving_face"),
					# (str_store_string, s1, "str_qp4_odval_betrayed_judge_male"),
					# (str_store_string, s2, "str_qp4_odval_betrayed_judge_female"),
					# (str_store_string, s3, "str_qp4_odval_second_place_finisher"),
					# (str_store_string, s4, "str_qp4_odval_third_place_finisher"),
					
					# (try_begin),		(eq, "$fight_timer", 5),	(display_message, "str_qp4_challenge_trash_talk_1"),
						# (else_try),		(eq, "$fight_timer", 7),	(display_message, "str_qp4_challenge_trash_talk_2"),
						# (else_try),		(eq, "$fight_timer", 11),	(display_message, "str_qp4_challenge_trash_talk_3"),
						# (else_try),		(eq, "$fight_timer", 13),	(display_message, "str_qp4_challenge_trash_talk_4"),
						# (else_try),		(eq, "$fight_timer", 18),	(display_message, "str_qp4_challenge_trash_talk_5"),
						# (else_try),		(eq, "$fight_timer", 21),	(display_message, "str_qp4_challenge_trash_talk_6"),
						# (else_try),		(eq, "$fight_timer", 24),	(display_message, "str_qp4_challenge_trash_talk_7"),
					# (try_end),
				(try_end),
			]),
				
		# COMMON TRIGGER: Contest end conditions.
		(1, 0, ti_once, 
			[
				(eq, "$timer_active", 2),
				(ge, "$fight_timer", 3),
				(agent_is_active, "$agent_elder"),
				(agent_is_alive, "$agent_elder"),
				(agent_get_position, pos1, "$agent_elder"),
				(get_player_agent_no, ":agent_player"),
				(agent_get_position, pos2, ":agent_player"),
				(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
				(lt, ":distance", 5),
			], 
			[
				# Initiate elder conversation.
				(neq, "$agent_elder", -1),
				(agent_get_troop_id, ":troop_elder", "$agent_elder"),
				(assign, "$g_talk_troop", ":troop_elder"),
				(start_mission_conversation, ":troop_elder"),
			]),
		
		########## TRIGGERS SPECIFIC TO ODVAL_ACCEPT_THE_CHALLENGE ##########
		
		# TRIGGER: Spawn Actors.
		(ti_after_mission_start, 0, ti_once, 
			[(neg|check_quest_active, "qst_odval_saving_face"),], 
			[
				(set_spawn_radius, 2),
				(add_visitors_to_current_scene, 8, qp4_actor_townsfolk, 3, 0, 0),
				
				#(start_presentation, "prsnt_gpu_dialog"),
			]),
			
		# TRIGGER: Ensure everyone is near the village elder for this fight.
		(1, 5, 0, 
			[
				(eq, "$timer_active", 0),
			], 
			[
				(assign, ":ready_check", 1),
				
				(neq, "$agent_elder", -1),
				(agent_get_troop_id, ":troop_elder", "$agent_elder"),
				(agent_get_position, pos1, "$agent_elder"),
				
				# Determine if anyone is not ready.
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(this_or_next|eq, ":troop_no", qp4_actor_townsfolk),
					(this_or_next|eq, ":troop_no", "trp_player"),
					(is_between, ":troop_no", companions_begin, companions_end),
					
					(agent_get_position, pos2, ":agent_no"),
					(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
					# (assign, reg31, ":distance"),
					# (str_store_troop_name, s31, ":troop_no"),
					# (display_message, "@DEBUG (qp4): {s31} is {reg31} distance from the elder.", gpu_debug),
					(ge, ":distance", 10),
					(assign, ":ready_check", 0),
				(try_end),
				(eq, ":ready_check", 1),
				(assign, "$timer_active", 1),
				
				# Initiate elder conversation.
				(try_begin),
					(check_quest_active, "qst_odval_accept_the_challenge"),
					(call_script, "script_common_quest_change_state", "qst_odval_accept_the_challenge", qp4_odval_accept_the_challenge_challenge_begun),
				(try_end),
				(try_begin),
					(check_quest_active, "qst_odval_saving_face"),
					(call_script, "script_common_quest_change_state", "qst_odval_saving_face", qp4_odval_saving_face_challenge_begun),
				(try_end),
				
				(assign, "$g_talk_troop", ":troop_elder"),
				(start_mission_conversation, ":troop_elder"),
			]),
		
		# TRIGGER: Contest begin conditions.
		(1, 0, ti_once, 
			[
				(check_quest_active, "qst_odval_accept_the_challenge"),
				(eq, "$timer_active", 1),
				(ge, "$fight_timer", 3),
			], 
			[
				# Remove the village elder from the fight.
				(agent_set_team, "$agent_elder", 2),
				(entry_point_get_position, pos2, 7),
				(agent_set_scripted_destination_no_attack, "$agent_elder", pos2, 1),
				
				(call_script, "script_qp4_add_storyline_characters"),
				(try_for_agents, ":agent_no"),
					(neq, ":agent_no", "$agent_elder"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(neq, ":troop_no", reg41),
					(neq, ":troop_no", reg42),
					(neq, ":troop_no", reg43),
					(neq, ":troop_no", reg44),
					(neq, ":troop_no", reg45),
					(neq, ":troop_no", reg46),
					(neq, ":troop_no", reg47),
					(neq, ":troop_no", reg48),
					(neq, ":troop_no", "trp_player"),
					(try_begin),
						(eq, ":troop_no", qp4_actor_townsfolk),
						(agent_set_team, ":agent_no", 1),
						(agent_ai_set_aggressiveness, ":agent_no", 199),
					(else_try),
						(this_or_next|eq, ":troop_no", "trp_khergit_townsman"),
						(eq, ":troop_no", "trp_khergit_townswoman"),
						(agent_set_team, ":agent_no", 2),
						#(agent_ai_set_aggressiveness, ":agent_no", 199),
					(try_end),
				(try_end),
				
				(team_set_relation, 0, 1, -1), # Player & Odval hate enemies.
				(team_set_relation, 0, 2, 1),  # Player & Odval are okay with the elder.
				(team_set_relation, 1, 0, -1), # Enemies are okay with the elder.
				(team_set_relation, 1, 2, 1),  # Enemies are okay with the elder.
				(team_set_relation, 2, 0, 1),  # Enemies are okay with the elder.
				(team_set_relation, 2, 1, 1),  # Enemies are okay with the elder.
				
				(set_party_battle_mode),
				
			]),
		
		# TRIGGER: Contest end conditions.
		(3, 0, 0, 
			[
				(check_quest_active, "qst_odval_accept_the_challenge"),
				(eq, "$timer_active", 1),
				(ge, "$fight_timer", 5),
				(assign, ":player_team", 0),
				(assign, ":enemy_team", 0),
				(assign, ":wounded", 0),
				
				(try_for_agents, ":agent_no"),
					(try_begin),
						(agent_get_troop_id, ":troop_no", ":agent_no"),
						(eq, ":troop_no", NPC_Odval),
						(agent_is_wounded, ":agent_no"),
						(assign, ":wounded", 1),
					(try_end),
					(agent_is_alive, ":agent_no"),
					(agent_get_team, ":agent_team", ":agent_no"),
					(try_begin),
						(eq, ":agent_team", 1),
						(val_add, ":enemy_team", 1),
					(else_try),
						(neq, ":agent_no", "$agent_elder"),
						(val_add, ":player_team", 1),
					(try_end),
				(try_end),
				(this_or_next|eq, ":player_team", 0),
				(eq, ":enemy_team", 0),
				(assign, reg50, ":player_team"),
				(assign, reg51, ":enemy_team"),
				(assign, reg52, ":wounded"),
			], 
			[
				
				(try_begin),
					# player team lost.
					(eq, reg50, 0),
					(call_script, "script_common_quest_change_state", "qst_odval_accept_the_challenge", qp4_odval_accept_the_challenge_challenge_lost),
					(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_update),
				(else_try),
					# player team wins.
					(eq, reg51, 0),
					(call_script, "script_common_quest_change_state", "qst_odval_accept_the_challenge", qp4_odval_accept_the_challenge_challenge_won),
					(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_update),
					(try_begin),
						(eq, reg52, 1),
						(call_script, "script_common_quest_change_state", "qst_odval_accept_the_challenge", qp4_odval_accept_the_challenge_odval_fell),
					(try_end),
				(else_try),
					(display_message, "@Error - No valid winner detected."),
				(try_end),
				(finish_party_battle_mode),
				(assign, "$timer_active", 2),
				(assign, "$fight_timer", 2),
				
				# Put everyone back on the same side.
				(try_for_agents, ":agent_no"),
					(agent_set_team, ":agent_no", 0),
				(try_end),
				
				# Restore Village Elder agent.
				(get_player_agent_no, ":agent_player"),
				(agent_get_position, pos1, ":agent_player"),
				(agent_set_scripted_destination, "$agent_elder", pos1),
			]),
		
		# TRIGGER
		(ti_tab_pressed, 0, 0, 
			[
				(this_or_next|check_quest_active, "qst_odval_accept_the_challenge"),
				(this_or_next|quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_complete),
				(this_or_next|quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_odval_fell_not_okay),
				(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_odval_fell_but_okay),
			],
			[
				(try_begin),
					(eq, "$timer_active", 0),
					(dialog_box, "str_qp4_odval_accept_the_challenge_pre_fight", "str_qp4_odval_accept_the_challenge_title"),
				(else_try),
					(eq, "$timer_active", 1),
					(dialog_box, "str_qp4_odval_accept_the_challenge_cant_run", "str_qp4_odval_accept_the_challenge_title"),
				(else_try),
					(eq, "$timer_active", 2),
					(dialog_box, "str_qp4_odval_accept_the_challenge_post_fight", "str_qp4_odval_accept_the_challenge_title"),
				(else_try),
					(finish_mission, 0),
					(jump_to_menu, "mnu_village"),
				(try_end),
			]),
		
		########## TRIGGERS SPECIFIC TO ODVAL_SAVING_FACE ##########
		
		# TRIGGER: Contest begin conditions.
		(1, 0, ti_once, 
			[
				(check_quest_active, "qst_odval_saving_face"),
				(eq, "$timer_active", 1),
				(ge, "$fight_timer", 3),
			], 
			[
				(team_set_relation, 0, 1, -1), # Player doesn't like Odval's team.
				(team_set_relation, 0, 2, 1),  # Player is friends with the elder.
				(team_set_relation, 1, 0, -1), # Odval doesn't like the player's team.
				(team_set_relation, 1, 2, 1),  # Odval is friends with the elder.
				(team_set_relation, 2, 0, 1),  # The Elder is friends with player's team.
				(team_set_relation, 2, 1, 1),  # The Elder is friends with Odval's team.
				
				# Remove the village elder from the fight.
				#(agent_set_team, "$agent_elder", 2),
				(get_player_agent_no, ":agent_player"),
				
				(try_for_agents, ":agent_no"),
					#(neq, ":agent_no", "$agent_elder"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(neq, ":troop_no", "trp_player"),
					(try_begin),
						(this_or_next|eq, ":agent_no", "$agent_elder"),
						(this_or_next|eq, ":troop_no", "trp_khergit_townsman"),
						(eq, ":troop_no", "trp_khergit_townswoman"),
						(agent_set_team, ":agent_no", 2),
					(else_try),
						(eq, ":troop_no", NPC_Odval),
						(agent_set_team, ":agent_no", 1),
						(agent_ai_set_aggressiveness, ":agent_no", 199),
						(agent_add_relation_with_agent, ":agent_no", ":agent_player", -1),
					(try_end),
					# (agent_set_team, ":agent_no", 1),
					# (agent_ai_set_aggressiveness, ":agent_no", 199),
					# (agent_add_relation_with_agent, ":agent_no", ":agent_player", -1),
					(ge, DEBUG_QUEST_PACK_4, 1),
					(str_store_troop_name, s31, ":troop_no"),
					(agent_get_team, reg31, ":agent_no"),
					(display_message, "@DEBUG (QP4): {s31} has been switched to team {reg31}."),
				(try_end),
				
				(team_give_order, 1, grc_everyone, mordr_charge),
				
				(set_party_battle_mode),
				
				(assign, reg56, 0), # Tracking Odval's injuries.
			]),
		
		# TRIGGER
		(ti_tab_pressed, 0, 0, 
			[
				(check_quest_active, "qst_odval_saving_face"),
				(this_or_next|quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_begun),
				(this_or_next|quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_won),
				(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_lost),
			],
			[
				(try_begin),
					(eq, "$timer_active", 0),
					(dialog_box, "str_qst_odval_saving_face_pre_fight", "str_qp4_odval_saving_face_title"),
				(else_try),
					(eq, "$timer_active", 1),
					(dialog_box, "str_qp4_odval_accept_the_challenge_cant_run", "str_qp4_odval_saving_face_title"),
				(else_try),
					(eq, "$timer_active", 2),
					(dialog_box, "str_qp4_odval_accept_the_challenge_post_fight", "str_qp4_odval_saving_face_title"),
				(else_try),
					(finish_mission, 0),
					(jump_to_menu, "mnu_village"),
				(try_end),
			]),
		
		# TRIGGER: Used to track how much damage Odval has taken to ensure it is a convincing fight.
		(ti_on_agent_hit, 0, 0, 
			[
				(check_quest_active, "qst_odval_saving_face"),
			],
			[
				(store_trigger_param_1, ":agent_victim"),
				#(store_trigger_param_2, ":agent_attacker"),
				(store_trigger_param_3, ":damage"),
				
				(agent_get_troop_id, ":troop_no", ":agent_victim"),
				(eq, ":troop_no", NPC_Odval),
				(ge, ":damage", 1),
				(val_div, ":damage", 2),
				(val_add, reg56, ":damage"),
				(set_trigger_result, ":damage"),
			]),
		
		# TRIGGER: Contest end conditions.
		(3, 0, 0, 
			[
				(check_quest_active, "qst_odval_saving_face"),
				(eq, "$timer_active", 1),
				(ge, "$fight_timer", 5),
				(this_or_next|eq, reg55, 1),
				(main_hero_fallen),
			], 
			[
				
				(try_begin),
					# player team lost.
					(main_hero_fallen),
					(call_script, "script_common_quest_change_state", "qst_odval_saving_face", qp4_odval_saving_face_challenge_lost),
					(call_script, "script_qp4_quest_odval_saving_face", floris_quest_update),
				(else_try),
					# player team wins.
					(eq, reg55, 1),
					(call_script, "script_common_quest_change_state", "qst_odval_saving_face", qp4_odval_saving_face_challenge_won),
					(call_script, "script_qp4_quest_odval_saving_face", floris_quest_update),
				(else_try),
					(display_message, "@Error - No valid winner detected."),
				(try_end),
				(finish_party_battle_mode),
				(assign, "$timer_active", 2),
				(assign, "$fight_timer", 2),
				
				# Put everyone back on the same side.
				(try_for_agents, ":agent_no"),
					(agent_set_team, ":agent_no", 0),
				(try_end),
				
				# Restore Village Elder agent.
				(get_player_agent_no, ":agent_player"),
				(agent_get_position, pos1, ":agent_player"),
				(agent_set_scripted_destination, "$agent_elder", pos1),
			]),
    ]+pbod_common_triggers+combat_enhancement_triggers,),
	
	###### EDWYN SECOND KNIGHT FIGHT IN TOWN ######
	(
		"edwyn_town_fight",0,-1,
		"Town Fight",
    [
		(0,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
		(1,mtef_scene_source|mtef_team_0,af_override_horse,0,1,[]),
		(2,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
		(3,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
		(4,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
		(5,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
		(6,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
		(7,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),          
		(8,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]),
		(9,mtef_visitor_source,af_override_horse,0,1,[]),
		(10,mtef_visitor_source,af_override_horse,0,1,[]),
		(11,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
		(12,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
		(13,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
		(14,mtef_visitor_source,af_override_horse,0,1,[]),
		(15,mtef_visitor_source,af_override_horse,0,1,[]),
		(16,mtef_visitor_source,af_override_horse,0,1,[]),
		(17,mtef_visitor_source,af_override_horse,0,1,[]),
		(18,mtef_visitor_source,af_override_horse,0,1,[]),
		(19,mtef_visitor_source,af_override_horse,0,1,[]),
		(20,mtef_visitor_source,af_override_horse,0,1,[]),
		(21,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
		(22,mtef_visitor_source|mtef_team_1,af_override_horse,0,1,[]),
		(23,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
		(24,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
		(25,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
		(26,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
		(27,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
		(28,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #guard
		(29,mtef_visitor_source,af_override_horse,0,1,[]),
		(30,mtef_visitor_source,af_override_horse,0,1,[]), 
		(31,mtef_visitor_source,af_override_horse,0,1,[]), 
		(32,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
		(33,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
		(34,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
		(35,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
		(36,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
		(37,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
		(38,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
		(39,mtef_visitor_source|mtef_team_0,af_override_horse,0,1,[]), #town walker point
		(40,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
		(41,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
		(42,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
		(43,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]), #in towns, can be used for guard reinforcements
		(44,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(45,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(46,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
		(47,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),
    ],
    [
		# TRIGGER (any): Make the townsfolk move around.
		(3, 0, 0, 
			[], 
			[ (call_script, "script_tick_town_walkers") ]),	  	  
        
		# TRIGGER (any): Set everyone to team 0 initial to keep things neutral.
		(ti_on_agent_spawn, 0, 0, 
			[],
			[
				(store_trigger_param_1, ":agent_no"),
				(agent_set_team, ":agent_no", 0),
				# (agent_get_troop_id, ":troop_no", ":agent_no"),
				# (eq, ":troop_no", "$town_guard"),
				# (agent_set_team, ":agent_no", 3),
			]),
		
		# TRIGGER (any): Inventory use.
		(ti_inventory_key_pressed, 0, 0, 
			[], 
			[
				(try_begin),
					(eq, "$g_mt_mode", tcm_default),
					(set_trigger_result,1),
				(else_try),
					(eq, "$g_mt_mode", tcm_disguised),
					(display_message,"str_cant_use_inventory_disguised"),
				(else_try),
					(display_message, "str_cant_use_inventory_now"),
				(try_end),
			]),
		
		# TRIGGER (pre-battle): Initialize parameters.
		(ti_before_mission_start, 0, 0, 
			[],
			[
				(set_fixed_point_multiplier, 100),
				(assign, "$fight_timer", 0),
				(assign, "$timer_active", 0),
				(assign, reg27, 0), # Tracks when the guards have appeared close enough.
				
				(store_faction_of_party, ":town_faction","$current_town"),
				(try_begin),
					(neq, ":town_faction", "fac_player_supporters_faction"),
					(faction_get_slot, "$town_guard", ":town_faction", slot_faction_tier_3_troop),
				(else_try),
					(party_get_slot, ":town_original_faction", "$current_town", slot_center_original_faction),
					(faction_get_slot, "$town_guard", ":town_original_faction", slot_faction_tier_3_troop),
				(try_end),
			]),
		
		# TRIGGER (pre-battle): Populate the streets.
        (ti_after_mission_start, 0, 0, 
			[],
			[
				# Add some knights to the walking areas.
				(add_visitors_to_current_scene, 34, qp4_actor_named_knight, 1, 0, 0),
				(troop_set_name, qp4_actor_named_knight, "@Sir Henric"),
				(add_visitors_to_current_scene, 34, qp4_actor_knight_support, 2, 0, 0), # qp4_actor_knight_support
				# Add some peasants walking about.
				(call_script, "script_init_town_walker_agents"),
			]),
		
		# TRIGGER (pre-battle): Check to see if the player is nearby then move to him and begin confrontation.
		(1, 0, 0, 
			[ 
				(eq, "$timer_active", 0),
				(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_arrived_in_town),
			], 
			[ 
				(get_player_agent_no, ":agent_player"),
				(agent_get_position, pos1, ":agent_player"),
				(assign, ":ready_check", 0),
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(eq, ":troop_no", qp4_actor_named_knight),
					(agent_get_position, pos2, ":agent_no"),
					(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
					(lt, ":distance", 5),
					(assign, ":ready_check", 1),
				(try_end),
				(eq, ":ready_check", 1),
				(assign, "$g_talk_troop", qp4_actor_named_knight),
				(assign, "$npc_map_talk_context", "qst_edwyn_second_knight"),
				(start_mission_conversation, "$g_talk_troop"),
			]),
		
		# TRIGGER (battle): Battle has begun.  Keep track of time.
		(1, 0, 0, 
			[ 
				(eq, "$timer_active", 1),
				(neg|conversation_screen_is_active),
			], 
			[
				(val_add, "$fight_timer", 1),
				
				# Someone call for the guards.
				(try_begin),
					(eq, "$fight_timer", 3),
					(display_message, "@A townswoman calls, 'Someone call for the guards!  Guards!'"),
				(else_try),
					(eq, "$fight_timer", qp4_edwyn_second_time_until_guard_arrives),
					(eq, "$timer_active", 1), # Fight still active.
					# Guards appear
					(display_message, "@You hear the sounds of the town guard pushing their way towards you..."), # 37 is too far.
					(add_visitors_to_current_scene, 32, "$town_guard", 2, 0, 0),
					(add_visitors_to_current_scene, 35, "$town_guard", 2, 0, 0),
					(ge, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
					(add_visitors_to_current_scene, 39, "$town_guard", 2, 0, 0),
					(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
					(add_visitors_to_current_scene, 31, "$town_guard", 2, 0, 0),
					
				(try_end),
			]),
		
		# TRIGGER (battle): Battle has begun.  Keep track of time.
		(1, 0, 0, 
			[ 
				(eq, "$timer_active", 1),
				(neg|conversation_screen_is_active),
				(ge, "$fight_timer", qp4_edwyn_second_time_until_guard_arrives),
				(eq, reg27, 0),
			], 
			[
				(get_player_agent_no, ":agent_player"),
				(agent_get_position, pos1, ":agent_player"),
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(eq, ":troop_no", "$town_guard"),
					(agent_get_position, pos2, ":agent_no"),
					(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
					(agent_set_scripted_destination, ":agent_no", pos1),
					(agent_play_sound, ":agent_no", "snd_footstep_grass"),
					(lt, ":distance", 12),
					(assign, reg27, 1),
				(try_end),
				
				(eq, reg27, 1), # Trigger the guards hostility.
				(display_message, "@The guards have arrived!"),
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(eq, ":troop_no", "$town_guard"),
					(agent_set_team, ":agent_no", 3),
					(agent_clear_scripted_mode, ":agent_no"),
				(try_end),
				# Set the team relation of the guards.
				(team_set_relation, 3, 0,  1), # The guards are friends with the townsfolk.
				(team_set_relation, 3, 1, -1), # The guards are enemies with the player team.
				(team_set_relation, 3, 2, -1), # The guards are enemies with the knights.
				(team_set_relation, 0, 3,  1), # The townsfolk are friends with the guards.
				(team_set_relation, 1, 3, -1), # The player team is enemies with the guards.
				(team_set_relation, 2, 3, -1), # The knights are enemies with the guards.
			]),
		
		# TRIGGER (battle): Conversation has ended.  Begin the fight.
		(1, 0, ti_once, 
			[ (eq, "$timer_active", 1), ], 
			[
				# Setup battle mode.
				(mission_disable_talk),        
				(set_party_battle_mode),
				
				# Switch the player party to team 1, knights to team 2 and leave peasants on team 0.
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(agent_clear_scripted_mode, ":agent_no"),
					(try_begin),
						(this_or_next|eq, ":troop_no", qp4_actor_knight_support),
						(this_or_next|eq, ":troop_no", qp4_actor_knight),
						(eq, ":troop_no", qp4_actor_named_knight),
						(agent_set_team, ":agent_no", 2),
					(else_try),
						(main_party_has_troop, ":troop_no"),
						(agent_set_team, ":agent_no", 1),
					(else_try),
						(agent_set_team, ":agent_no", 0),
					(try_end),
				(try_end),
				
				# Setup team relations
				(team_set_relation, 0, 1,  1), # Townsfolk are okay with the player team.
				(team_set_relation, 0, 2,  1), # Townsfolk are okay with the knights.
				(team_set_relation, 1, 0,  1), # Player team is okay with the townsfolk.
				(team_set_relation, 1, 2, -1), # Player team is enemies with the knights.
				(team_set_relation, 2, 0,  1), # Knights are okay with the townsfolk.
				(team_set_relation, 2, 1, -1), # Knights are enemies with the player team.
			]),
		
		# TRIGGER 2
		(ti_tab_pressed, 0, 0, [],
		   [
				(try_begin),
					(eq, "$timer_active", 0),
					(set_trigger_result, 1),
				(else_try),
					(eq, "$timer_active", 2),
					(question_box,"@Do you wish to leave the scene?"),
				(else_try),
					(question_box,"str_give_up_fight"),
				(try_end),
			]),
		
		# TRIGGER 3
		(ti_question_answered, 0, 0, [],
			[
				(store_trigger_param_1,":answer"),
				(eq,":answer",0),
				(try_begin),
					(eq, "$timer_active", 0),
					# finish mission.
					(mission_enable_talk),   
					(finish_mission),               
					(change_screen_return),
					
				(else_try),
					# Conditions set to leave.  Should have already triggered ending.
					(assign, ":quest_knight_dead", 0),   # If he is found alive this gets set to 1.
					(assign, ":player_team_dead", 1),    # If any are found alive this gets set to 0.
					(assign, ":guards_have_arrived", 0), # If any guards are within a small distance this is set to 1.
					
					(get_player_agent_no, ":agent_player"),
					(agent_get_team, ":team_player", ":agent_player"),
					(agent_get_position, pos1, ":agent_player"),
					
					(try_for_agents, ":agent_no"),
						(agent_get_troop_id, ":troop_no", ":agent_no"),
						(agent_get_team, ":team_no", ":agent_no"),
						
						(try_begin),
							# Determine if our quest targets are alive or dead.
							(eq, ":troop_no", qp4_actor_named_knight),
							(neg|agent_is_alive, ":agent_no"),
							(assign, ":quest_knight_dead", 1),
						
						(else_try),
							# Determine if the player team members are alive.
							(eq, ":team_no", ":team_player"),
							(agent_is_alive, ":agent_no"),
							(assign, ":player_team_dead", 0), # We found someone alive.
						
						(else_try),
							# Determine if the guard are active and have arrived.
							(eq, ":troop_no", "$town_guard"),
							(agent_is_alive, ":agent_no"),
							(agent_get_position, pos2, ":agent_no"),
							(get_distance_between_positions, ":dist", pos1, pos2),
							(lt, ":dist", 10), # Guards are close enough.
							(assign, ":guards_have_arrived", 1),
						(try_end),
					(try_end),
					
					(assign, ":pass", 0), # Do not allow the tab action to continue.
					(try_begin),
						(eq, "$timer_active", 2),
						(assign, ":pass", 1),
					(else_try),
						(eq, "$timer_active", 1),
						(eq, ":guards_have_arrived", 0),
						(assign, ":pass", 1),
						(display_message, "@You make a quick escape before the guards reach your position."),
					(else_try),
						# Prevent leaving.
						(display_message, "@You can't escape with so many enemies about!"),
					(try_end),
					(eq, ":pass", 1),
					
					# Setup final conditions.
					(assign, ":quest_function", floris_quest_fail),
					(try_begin),
						# WIN: Player team alive, quest_knight dead
						(eq, ":player_team_dead", 0),   # Player team survived.
						(eq, ":quest_knight_dead", 1),  # Knight is dead.
						(assign, ":quest_function", floris_quest_succeed),
						(assign, ":quest_stage", qp4_edwyn_second_knight_is_slain),
					(else_try),
						# LOSS: Player team alive, quest_knight alive
						(eq, ":player_team_dead", 0),   # Player team survived.
						(eq, ":quest_knight_dead", 0),  # Knight is alive.
						(assign, ":quest_function", floris_quest_fail),
						(assign, ":quest_stage", qp4_edwyn_second_knight_lives_on),
					(else_try),
						# LOSS: Player team dead, quest knight alive.
						(eq, ":player_team_dead", 1),   # Player team is dead.
						(eq, ":quest_knight_dead", 0),  # Knight is alive.
						(assign, ":quest_function", floris_quest_fail),
						(assign, ":quest_stage", qp4_edwyn_second_knight_lives_on),
					(else_try),
						# LOSS: Player team dead, quest knight dead.
						(eq, ":player_team_dead", 1),   # Player team is dead.
						(eq, ":quest_knight_dead", 1),  # Knight is dead.
						(assign, ":quest_function", floris_quest_fail),
						(assign, ":quest_stage", qp4_edwyn_second_knight_is_slain),
					(try_end),
					
					# Update the quest.
					(call_script, "script_common_quest_change_state", "qst_edwyn_second_knight", ":quest_stage"),
					(call_script, "script_qp4_quest_edwyn_second_knight", ":quest_function"),
					(call_script, "script_qp4_quest_edwyn_second_knight", floris_quest_update),
					
					(assign, "$timer_active", 2),
					(mission_enable_talk),   
					(finish_mission),               
					(change_screen_return),
					(jump_to_menu, "mnu_town"),
					(set_trigger_result, 1),
				(try_end),
			]),
			
		# TRIGGER (battle): Check for end conditions.
		(3, 0, ti_once,
			[                  
				(num_active_teams_le, 2),
				(ge, "$fight_timer", 3),
				(eq, "$timer_active", 1), # This is the only thing preventing the mission from auto-closure prior to the fight.
			],
			[         
				(assign, "$timer_active", 2),
				
				# Conditions set to leave.  Should have already triggered ending.
				(assign, ":quest_knight_dead", 0),   # If he is found alive this gets set to 1.
				(assign, ":player_team_dead", 1),    # If any are found alive this gets set to 0.
				
				(get_player_agent_no, ":agent_player"),
				(agent_get_team, ":team_player", ":agent_player"),
				
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(agent_get_team, ":team_no", ":agent_no"),
					
					(try_begin),
						# Determine if our quest targets are alive or dead.
						(eq, ":troop_no", qp4_actor_named_knight),
						(neg|agent_is_alive, ":agent_no"),
						(assign, ":quest_knight_dead", 1),
					
					(else_try),
						# Determine if the player team members are alive.
						(eq, ":team_no", ":team_player"),
						(agent_is_alive, ":agent_no"),
						(assign, ":player_team_dead", 0), # We found someone alive.
					
					(try_end),
				(try_end),
				
				(try_begin),
					(eq, ":quest_knight_dead", 1),
					(str_store_string, s21, "@SUCCESS"),
				(else_try),
					(str_store_string, s21, "@FAILED"),
				(try_end),
				
				(try_begin),
					(eq, ":player_team_dead", 0),
					(str_store_string, s22, "@SUCCESS"),
				(else_try),
					(str_store_string, s22, "@FAILED"),
				(try_end),
				(str_store_party_name, s23, "$current_town"),
				(dialog_box, "@OBJECTIVES:^Sir Henric slain   [ {s21} ]^Party survived   [ {s22} ]^^Press [ TAB ] to Exit", "@Battle in the Streets of {s23}"),
				(neg|main_hero_fallen),
				(ge, "$fight_timer", qp4_edwyn_second_time_until_guard_arrives),
				(display_message, "@Now would be a good time to get out of here before the guards arrive."),
			]),
  ]),
  
 
 (
    "edwyn_village_fight",mtf_battle_mode|mtf_synch_inventory,charge,	#	1.143 Port // mtf_synch_inventory added
    "You lead your men to battle.",
    [
		(3,mtef_visitor_source|mtef_team_1,af_override_horse,aif_start_alarmed,1,[]),         # Knights under Sir Gerrin.
		(1,mtef_team_0|mtef_use_exact_number,0,aif_start_alarmed, 7,[]),      # Player
		(1,mtef_visitor_source|mtef_team_0,0,aif_start_alarmed,1,[]),         # Player Team
		(11,mtef_team_2,0,0,1,[]),                            				   # Elder
    ],
    [
		# TRIGGER 2
		(ti_before_mission_start, 0, ti_once, [],
		   [
				(assign, "$timer_active", 1),
				(assign, "$agent_elder", -1),
				(assign, reg27, 0), # Tracks when the elder's spoken.
			]),
		
		# TRIGGER: Check for village elder spawn.
		(ti_on_agent_spawn, 0, 0, [], 
			[
				(store_trigger_param_1, ":agent_no"),
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				
				# Figure out what agent our village elder is.
				(party_get_slot, ":troop_village_elder", "$current_town", slot_town_elder),
				(try_begin),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(eq, ":troop_no", ":troop_village_elder"),
					(assign, "$agent_elder", ":agent_no"),
					(ge, DEBUG_QUEST_PACK_4, 1),
					(display_message, "@DEBUG (QP4): Village elder actor assigned."),
				(try_end),
				
				# Move the villagers to a different starting point than the player.
				(try_begin),
					# (troop_get_slot,":mercenary_farmer", "$troop_trees", slot_mercenary_farmer),
					# (eq, ":troop_no", ":mercenary_farmer"),
					(store_faction_of_party, ":faction_no", "$current_town"),
					(faction_get_slot, ":culture", ":faction_no",  slot_faction_culture),
					(faction_get_slot, ":walker", ":culture",  slot_faction_village_walker_male_troop),
					(eq, ":troop_no", ":walker"),
					(entry_point_get_position, pos1, 4),
					(agent_set_position, ":agent_no", pos1),
				(try_end),
				
				# Move the player's people to their side.
				(try_begin),
					#(neq, ":troop_no", ":mercenary_farmer"),
					(neq, ":troop_no", ":walker"),
					(neq, ":troop_no", qp4_actor_knight),
					(neq, ":troop_no", qp4_actor_knight_support),
					(neq, ":troop_no", qp4_actor_named_knight),
					(neq, ":troop_no", ":troop_village_elder"),
					(entry_point_get_position, pos1, 1),
					(agent_set_position, ":agent_no", pos1),
				(try_end),
				
			]),
			
		# TRIGGER 2
		(10, 0, 0, 
			[
				(eq, "$timer_active", 2),
				(eq, "$g_battle_result", 1),
			],
			[
				(display_message,"str_msg_battle_won"),
			]),
		
		# TRIGGER 2
		(ti_tab_pressed, 0, 0, [],
		   [
				(try_begin),
					(eq, "$timer_active", 0),
					(set_trigger_result, 1),
					(jump_to_menu, "mnu_village"),
				(else_try),
					(eq, "$timer_active", 2),
					(set_trigger_result, 1),
					(jump_to_menu, "mnu_village"),
				(else_try),
					(question_box,"@Do you wish to abandon the villagers to be slaughtered?"),
				(try_end),
			]),
		
		# TRIGGER 3
		(ti_question_answered, 0, 0, [],
			[
				(store_trigger_param_1,":answer"),
				(eq, ":answer", 0),
				(try_begin),
					(neq, "$timer_active", 1),
					(eq, ":answer", 0),
					# finish mission.
					(mission_enable_talk),   
					(finish_mission),               
					(jump_to_menu, "mnu_village"),
					(change_screen_return),
					(set_trigger_result, 1),
					
				(else_try),
					(eq, ":answer", 0),
					# Fail the quest.
					(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_knight_lives_on),
					(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_fail),
					(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
					  
					(finish_mission),   
					(change_screen_return),
					(set_trigger_result, 1),
				(try_end),
			]),
			
		# TRIGGER (Battle): Check for end conditions.
		(3, 0, ti_once,
			[                  
				(num_active_teams_le, 1),
			],
			[         
				(assign, "$timer_active", 2),
				
				# Conditions set to leave.  Should have already triggered ending.
				(assign, ":quest_knight_dead", 0),   # If he is found alive this gets set to 1.
				(assign, ":player_team_dead", 1),    # If any are found alive this gets set to 0.
				(assign, ":villagers_alive", 0),     # Count the number of villagers left.
				(store_mul, ":villagers_needed", qp4_villagers_present_for_fight, qp4_villagers_that_must_survive),
				(val_div, ":villagers_needed", 100),
				
				(get_player_agent_no, ":agent_player"),
				(agent_get_team, ":team_player", ":agent_player"),
				#(troop_get_slot,":mercenary_farmer", "$troop_trees", slot_mercenary_farmer),
				(store_faction_of_party, ":faction_no", "$current_town"),
				(faction_get_slot, ":culture", ":faction_no",  slot_faction_culture),
				(faction_get_slot, ":mercenary_farmer", ":culture",  slot_faction_village_walker_male_troop),
				
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(agent_get_team, ":team_no", ":agent_no"),
					
					(try_begin),
						# Determine if our quest targets are alive or dead.
						(eq, ":troop_no", qp4_actor_named_knight),
						(neg|agent_is_alive, ":agent_no"),
						(assign, ":quest_knight_dead", 1),
					
					(else_try),
						# Determine if the player team members are alive.
						(eq, ":team_no", ":team_player"),
						(agent_is_alive, ":agent_no"),
						(assign, ":player_team_dead", 0), # We found someone alive.
					
					(else_try),
						# See if any villagers survived.
						(eq, ":troop_no", ":mercenary_farmer"),
						(val_add, ":villagers_alive", 1),
						
					(try_end),
				(try_end),
				
				# Setup final conditions.
				(assign, ":quest_function", floris_quest_fail),
				(try_begin),
					# WIN: Player team alive, quest_knight dead, some villagers live.
					(eq, ":player_team_dead", 0),   # Player team survived.
					(eq, ":quest_knight_dead", 1),  # Knight is dead.
					(ge, ":villagers_alive", ":villagers_needed"),
					(assign, "$g_battle_result", 1),
					(assign, ":quest_function", floris_quest_succeed),
					(assign, ":quest_stage", qp4_edwyn_third_knight_is_slain),
				(else_try),
					# LOSS: Player team alive, quest_knight dead, not enough villagers live.
					(eq, ":player_team_dead", 0),   # Player team survived.
					(eq, ":quest_knight_dead", 1),  # Knight is dead.
					(lt, ":villagers_alive", ":villagers_needed"),
					(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
					(assign, "$g_battle_result", -1),
					(assign, ":quest_function", floris_quest_fail),
					(assign, ":quest_stage", qp4_edwyn_third_knight_is_slain),
				(else_try),
					# WIN: Player team lives, quest knight dies, villagers die (medium reactions)
					(eq, ":player_team_dead", 0),   # Player team survived.
					(eq, ":quest_knight_dead", 0),  # Knight is alive.
					(lt, "$quest_reactions", QUEST_REACTIONS_HIGH),
					(assign, "$g_battle_result", 1),
					(assign, ":quest_function", floris_quest_succeed),
					(assign, ":quest_stage", qp4_edwyn_third_knight_is_slain),
				(else_try),
					# LOSS: Anything less.
					(assign, "$g_battle_result", -1),
					(assign, ":quest_function", floris_quest_fail),
					(assign, ":quest_stage", qp4_edwyn_third_knight_lives_on),
				(try_end),
				
				(try_begin),
					(eq, ":quest_knight_dead", 1),
					(str_store_string, s21, "@SUCCESS"),
				(else_try),
					(str_store_string, s21, "@FAILED"),
				(try_end),
				
				(try_begin),
					(eq, ":player_team_dead", 0),
					(str_store_string, s22, "@SUCCESS"),
				(else_try),
					(str_store_string, s22, "@FAILED"),
				(try_end),
				
				(try_begin),
					(lt, "$quest_reactions", QUEST_REACTIONS_HIGH),
					(str_store_string, s23, "@N/A"),
				(else_try),
					(ge, ":villagers_alive", ":villagers_needed"),
					(str_store_string, s23, "@SUCCESS"),
				(else_try),
					(str_store_string, s23, "@FAILED"),
				(try_end),
				
				(try_begin),
					(eq, "$g_battle_result", 1),
					(str_store_string, s25, "@Speak to the Elder"),
				(else_try),
					(str_store_string, s25, "@Press [ TAB ] to Exit"),
				(try_end),
				
				(assign, reg21, qp4_villagers_that_must_survive),
				(str_store_party_name, s24, "$current_town"),
				(dialog_box, "@OBJECTIVES:^Sir Gerrin slain   [ {s21} ]^Party survived   [ {s22} ]^Villagers survived ({reg21}+%)   [ {s23} ]^^{s25}", "@Battle of {s24}"),
				
				
				
				# Update the quest.
				(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", ":quest_stage"),
				(call_script, "script_qp4_quest_edwyn_third_knight", ":quest_function"),
				(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
				
				# Spawn a village elder and have him speak to the player.
				(mission_enable_talk), 
				(neg|main_hero_fallen),
				(entry_point_get_position, pos1, 4),
				(set_spawn_position, pos1),
				(party_get_slot, ":troop_village_elder", "$current_town", slot_town_elder),
				(spawn_agent, ":troop_village_elder"),
				(get_player_agent_no, ":agent_player"),
				(agent_get_position, pos1, ":agent_player"),
				(agent_set_scripted_destination, ":agent_no", pos1),
			]),
		
		# TRIGGER (post battle): Elder rushes to find you to talk.
		(4, 0, 0, 
			[
				# (eq, "$timer_active", 2),
				# (eq, "$g_battle_result", 1),
				(eq, reg27, 0),
			],
			[
				(get_player_agent_no, ":agent_player"),
				(agent_get_position, pos1, ":agent_player"),
				(party_get_slot, ":troop_village_elder", "$current_town", slot_town_elder),
				(try_for_agents, ":agent_no"),
					(agent_get_troop_id, ":troop_no", ":agent_no"),
					(eq, ":troop_no", ":troop_village_elder"),
					(agent_get_position, pos2, ":agent_no"),
					(agent_set_scripted_destination, ":agent_no", pos1),
					(get_distance_between_positions_in_meters, ":distance", pos1, pos2),
					(lt, ":distance", 5),
					(assign, reg27, 1),
					(assign, "$g_talk_troop", ":troop_village_elder"),
					(assign, "$npc_map_talk_context", qp4_edwyn_third_knight_is_slain),
					(start_mission_conversation, ":troop_village_elder"),
				(try_end),
			]),
		
		
	  common_battle_tab_press,
      common_battle_init_banner,
      common_music_situation_update,
      # common_battle_check_friendly_kills,
      # common_battle_check_victory_condition,
      # common_battle_victory_display,
      common_battle_inventory,      
      common_battle_order_panel,
      common_battle_order_panel_tick,
      # custom_commander_check_player_can_join_battle, ## CC

    ] # + custom_commander_commom_triggers, ## CC
  ),
  
]

############################## END OF STANDARD MISSION TEMPLATES ##############################

storyline_character_triggers = [
	(ti_before_mission_start, 0, 0, 
		[],
		[
			(call_script, "script_qp4_add_storyline_characters"),
			(try_begin),
				(is_between, reg41, active_npcs_begin, active_npcs_end),
				(party_get_slot, reg1, "p_main_party", slot_party_pref_bodyguard),
				(neq, reg1, 0), # keep bodyguards set to 0 if currently desired there.
				(party_set_slot, "p_main_party", slot_party_pref_bodyguard, 0),  # Prevent bodyguards from showing up during storyline missions.
				(ge, DEBUG_QUEST_PACK_4, 1),
				(display_message, "@DEBUG (QP4): Normal bodyguard settings overridden due to story character use."),
			(else_try),
				(party_get_slot, ":bodyguard_setting", "p_main_party", slot_party_bodyguard_backup),
				(neg|party_slot_eq, "p_main_party", slot_party_pref_bodyguard, ":bodyguard_setting"),
				(party_set_slot, "p_main_party", slot_party_pref_bodyguard, ":bodyguard_setting"),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(display_message, "@DEBUG (QP4): Normal bodyguard settings restored as no story character needed."),
			(try_end),
		]),   
   
	(ti_after_mission_start, 0, 0, 
		[],
		[
			# Check if a storyline character is warranted.
			(call_script, "script_qp4_add_storyline_characters"),
			(is_between, reg41, companions_begin, companions_end),
			(assign, ":story_1", reg41),
			(assign, ":story_2", reg42),
			(assign, ":story_3", reg43),
			(assign, ":story_4", reg44),
			(assign, ":story_5", reg45),
			(assign, ":story_6", reg46),
			(assign, ":story_7", reg47),
			(assign, ":story_8", reg48),
			
			#Prepare Scene/Mission Template
			(assign, ":entry_point", 0),
			#(assign, ":mission_tpl", 0),
			(try_begin),		
				(this_or_next|check_quest_active, "qst_odval_accept_the_challenge"),
				(check_quest_active, "qst_odval_saving_face"),
				(eq, "$current_town", qp4_odval_home_town),
				(party_slot_eq, "$current_town", slot_party_type, spt_village),
				(assign, ":entry_point", 6), # Special entry.
				#(assign, ":mission_tpl", "mt_village_center"),
			(else_try),		
				(party_slot_eq, "$current_town", slot_party_type, spt_village),
				(assign, ":entry_point", 11), #Village Elder's Entry
				#(assign, ":mission_tpl", "mt_village_center"),
			(else_try),
				(this_or_next|eq, "$talk_context", tc_prison_break),
				(this_or_next|eq, "$talk_context", tc_escape),
				(eq, "$talk_context", tc_town_talk),
				(assign, ":entry_point", 24), #Prison Guard's Entry
				# (try_begin),
					# (party_slot_eq, "$current_town", slot_party_type, spt_castle),
					# (assign, ":mission_tpl", "mt_castle_visit"),
				# (else_try),
					# (assign, ":mission_tpl", "mt_town_center"),
				# (try_end),
			(else_try),
				(eq, "$talk_context", tc_tavern_talk),
				(assign, ":entry_point", 17), #First NPC Tavern Entry
			(try_end),
			# (try_begin),
				# (neq, "$talk_context", tc_tavern_talk),
				# (get_player_agent_no, ":agent_player"),
				# (agent_get_horse, ":agent_horse", ":agent_player"),
				# (ge, ":agent_horse", 0),
				# (agent_get_item_id, ":item_horse", ":agent_horse"),
				# (agent_slot_ge, "$fplayer_agent_no", slot_agent_horse, 1), #If the player spawns with a horse, the bodyguard will too.
				# (mission_tpl_entry_set_override_flags, ":mission_tpl", ":entry_point", ":item_horse"),
			# (try_end),	
			(store_current_scene, ":cur_scene"),
			(modify_visitors_at_site, ":cur_scene"),  
		   
			#Find and Spawn Story NPC
			(try_for_range, ":count", 1, 9),
				(try_begin),
					(eq, ":count", 1),
					(assign, ":story_troop_no", ":story_1"),
				(else_try),
					(eq, ":count", 2),
					(assign, ":story_troop_no", ":story_2"),
				(else_try),
					(eq, ":count", 3),
					(assign, ":story_troop_no", ":story_3"),
				(else_try),
					(eq, ":count", 4),
					(assign, ":story_troop_no", ":story_4"),
				(else_try),
					(eq, ":count", 5),
					(assign, ":story_troop_no", ":story_5"),
				(else_try),
					(eq, ":count", 6),
					(assign, ":story_troop_no", ":story_6"),
				(else_try),
					(eq, ":count", 7),
					(assign, ":story_troop_no", ":story_7"),
				(else_try),
					(eq, ":count", 8),
					(assign, ":story_troop_no", ":story_8"),
				(try_end),
				(neq, ":story_troop_no", -1),
				(add_visitors_to_current_scene, ":entry_point", ":story_troop_no", 1),
				(get_player_agent_no, ":agent_player"),
				(agent_get_team, ":team_player", ":agent_player"),
				(set_show_messages, 0),   
				(team_give_order, ":team_player", 8, mordr_follow), #Division 8 to avoid potential conflicts
				(team_set_order_listener, ":team_player", 8),
				(set_show_messages, 1),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(str_store_troop_name, s14, ":story_troop_no"),
				(display_message, "@{s14} has arrived with you."),
			(try_end),
		]),   

	(ti_on_agent_spawn, 0, 0, [], 
		[
			(store_trigger_param_1, ":agent"),
			(agent_get_troop_id, ":troop", ":agent"),
			(call_script, "script_qp4_add_storyline_characters"),
			(this_or_next|eq, ":troop", reg41), # This is in fact a story character in their requested scene.
			(this_or_next|eq, ":troop", reg42), # This is in fact a story character in their requested scene.
			(this_or_next|eq, ":troop", reg43), # This is in fact a story character in their requested scene.
			(this_or_next|eq, ":troop", reg44), # This is in fact a story character in their requested scene.
			(this_or_next|eq, ":troop", reg45), # This is in fact a story character in their requested scene.
			(this_or_next|eq, ":troop", reg46), # This is in fact a story character in their requested scene.
			(this_or_next|eq, ":troop", reg47), # This is in fact a story character in their requested scene.
			(eq, ":troop", reg48), # This is in fact a story character in their requested scene.
			
			(get_player_agent_no, ":player"),
			(ge, ":player", 0),
			(agent_get_team, ":player_team", ":player"),
			
			(agent_get_position,pos1,":player"),		
			
			(agent_set_team, ":agent", ":player_team"),
			(agent_set_division, ":agent", 8),
			(try_begin),
				(main_party_has_troop, ":troop"),
				(agent_add_relation_with_agent, ":agent", ":player", 1),
			(try_end),
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
  
	(ti_on_agent_killed_or_wounded, 0, 0, [],
		[
			(store_trigger_param_1, ":dead_agent"),
				
			(agent_get_troop_id, ":troop", ":dead_agent"),
			(call_script, "script_qp4_add_storyline_characters"),
			(this_or_next|eq, ":troop", reg41), # This is in fact a story character in their requested scene.
			(this_or_next|eq, ":troop", reg42),
			(this_or_next|eq, ":troop", reg43),
			(this_or_next|eq, ":troop", reg44),
			(this_or_next|eq, ":troop", reg45),
			(this_or_next|eq, ":troop", reg46),
			(this_or_next|eq, ":troop", reg47),
			(eq, ":troop", reg48),
			(neg|troop_is_wounded, ":troop"),
			(party_wound_members, "p_main_party", ":troop", 1),
		]),
 ]


bandit_lair_triggers = [

	# TRIGGER: Sir Tenry slain.
		(ti_on_agent_killed_or_wounded, 0, 0, 
			[
				(check_quest_active, "qst_edwyn_first_knight"),
				(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_current_state, qp4_edwyn_first_entered_lair),
			], 
			[
				(store_trigger_param_1, ":agent_no"),
				
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				(eq, ":troop_no", qp4_actor_named_knight),
				(call_script, "script_common_quest_change_state", "qst_edwyn_first_knight", qp4_edwyn_first_knight_is_slain),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(display_message, "@Sir Tenry has been slain."),
			]),
			
	# TRIGGER: Sir Tenry injured.
		(ti_on_agent_hit, 0, 0, 
			[
				(check_quest_active, "qst_edwyn_first_knight"),
				(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_current_state, qp4_edwyn_first_entered_lair),
			], 
			[
				(store_trigger_param_1, ":agent_victim"),
				#(store_trigger_param_2, ":agent_attacker"),
				(store_trigger_param_3, ":damage"),
				
				(agent_get_troop_id, ":troop_no", ":agent_victim"),
				(eq, ":troop_no", qp4_actor_named_knight),
				(store_agent_hit_points, ":health", ":agent_victim", 1),
				(try_begin),
					# Prevent Tenry from being slain.
					(ge, ":damage", ":health"),
					(assign, ":damage", ":health"),
					(val_sub, ":damage", 1),
					# Switch Tenry to a neutral team.
					(agent_set_team, ":agent_victim", 0),
					# Set him fall down.
				(try_end),
				(set_trigger_result, ":damage"),
				(ge, DEBUG_QUEST_PACK_4, 1),
				(display_message, "@Sir Tenry has fallen in battle."),
			]),
			
	# Need to prevent Tenry from falling below 1 health.
	# Need to have Tenry trigger a conversation once the entire fight is done.
	
]

# def modmerge_mission_templates(orig_mission_templates):
	# find_i = find_object( orig_mission_templates, "arena_melee_fight" )
	# orig_mission_templates[find_i][5].extend(AI_triggers)

def modmerge_mission_templates(orig_mission_templates, check_duplicates = False):
	if( not check_duplicates ):
		orig_mission_templates.extend(mission_triggers) # Use this only if there are no replacements (i.e. no duplicated item names)
		for i in range(len(orig_mission_templates)):
			mt_name = orig_mission_templates[i][0]
			# Add storyline triggers to the default "walk around town/village/castle" mission templates.
			if( mt_name=="town_default" or mt_name=="town_center" or mt_name=="village_center" or mt_name=="castle_visit"):
				orig_mission_templates[i][5].extend(storyline_character_triggers)
			# Add storyline triggers to companion storyline missions. 
			if( mt_name=="odval_challenge" or mt_name=="edwyn_town_fight" or mt_name=="edwyn_village_fight"):
				orig_mission_templates[i][5].extend(storyline_character_triggers)
			# Add the following triggers to the bandit lair mission template. 
			if( mt_name=="bandit_lair" ):
				orig_mission_templates[i][5].extend(bandit_lair_triggers)
			
	else:
	# Use the following loop to replace existing entries with same id
		for i in range (0,len(mission_triggers)-1):
			find_index = find_object(orig_mission_templates, mission_triggers[i][0]); # find_object is from header_common.py
			if( find_index == -1 ):
				orig_mission_templates.append(mission_triggers[i])
			else:
				orig_mission_templates[find_index] = mission_triggers[i]
			
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