# Quest Pack 4 (1.0) by Windyplains

from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *

from module_constants import *

####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#  
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference. 
#        The consequences are executed for the menu option that has been selected by the player.
#
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################

game_menus = [
	##### QUEST - ODVAL ACCEPT THE CHALLENGE #####
	("qp4_odval_challenge",0,
		"Trial of Arms^^You and {s14} have returned to the village of {s13} to stand against {s14}'s accusers in combat.  The two of you have discussed the best plan available for dealing with the three men and believe you have a good chance at success, but failure may cost {reg3?her:him} more than simply shame.  In the hay field to the left you can see a large crowd gathered.^^OBJECTIVE:^You and {s14} must face {reg3?her:his} accusers in a contest of martial arms.  {s15}^^WARNING:^You may want to ensure {s14}'s equipment is up to this challenge.",
		"none",
		[
			(check_quest_active, "qst_odval_accept_the_challenge"),
			(main_party_has_troop, NPC_Odval),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_accepted),
			(quest_get_slot, reg1, "qst_odval_accept_the_challenge", slot_quest_giver_center),
			(str_store_party_name, s13, reg1),
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
			(try_begin),
				(eq, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(str_store_string, s15, "@{s14} must survive this contest."),
			(else_try),
				(str_clear, s15),
			(try_end),
			# Name the village elder.
			# (party_get_slot, ":troop_village_elder", qp4_odval_home_town, slot_town_elder),
			# (str_store_troop_name, s21, ":troop_village_elder"),
		],
		[
			("odval_challenge_yes", [], "Agree to begin the match.",
				[
					(call_script, "script_common_quest_change_state", "qst_odval_redemption", qp4_odval_accept_the_challenge_challenge_begun),
					(party_get_slot, ":village_scene", "$current_town", slot_castle_exterior), # qp4_odval_home_town
					(modify_visitors_at_site, ":village_scene"),
					(reset_visitors),
					(set_jump_mission, "mt_odval_challenge"),
					(jump_to_scene, ":village_scene"),
					(change_screen_mission),
				]),
			  
			("odval_challenge_wait", [], "Come back later.",
				[
					(jump_to_menu, "mnu_village"),
				]),
			  
			("odval_challenge_no", [], "Forget this whole affair.",
				[
					(quest_set_slot, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_lost),
					(quest_set_slot, "qst_odval_return_to_tulbuk", slot_quest_current_state, qp4_odval_return_to_tulbuk_refused_challenge),
					(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_update),
					(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_fail),
					(jump_to_menu, "mnu_village"),
				]),
		]),
	
	##### QUEST - ODVAL SAVING FACE #####
	("qp4_odval_saving_face",0,
		"Duel in {s13}^^You and {s14} have returned to the village of {s13} to face one another in combat in order to prove {s14}'s ability as a warrior.  You can see that the villagers have gathered near the hay field again along with {s21}.^^OBJECTIVE:^Help clear {s14}'s reputation through a contest of arms.",
		"none",
		[
			(check_quest_active, "qst_odval_saving_face"),
			(main_party_has_troop, NPC_Odval),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_accepted),
			(quest_get_slot, reg1, "qst_odval_saving_face", slot_quest_giver_center),
			# Ensure a couple of days have lapsed.
			(store_current_hours, ":hours"),
			(neg|quest_slot_ge, "qst_odval_saving_face", slot_quest_target_amount, ":hours"),
			(str_store_party_name, s13, reg1),
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
			# Name the village elder.
			(party_get_slot, ":troop_village_elder", qp4_odval_home_town, slot_town_elder),
			(str_store_troop_name, s21, ":troop_village_elder"),
		],
		[
			("odval_saving_yes", [], "Agree to begin the match.",
				[
					(call_script, "script_common_quest_change_state", "qst_odval_saving_face", qp4_odval_saving_face_challenge_begun),
					(troop_set_health, "trp_player", 100),
					(troop_set_health, NPC_Odval, 100),
					(party_get_slot, ":village_scene", qp4_odval_home_town, slot_castle_exterior),
					(modify_visitors_at_site, ":village_scene"),
					(reset_visitors),
					(set_jump_mission, "mt_odval_challenge"),
					(jump_to_scene, ":village_scene"),
					(change_screen_mission),
				]),
			  
			("odval_saving_wait", [], "Come back later.",
				[
					(jump_to_menu, "mnu_village"),
				]),
			  
			("odval_saving_no", [], "Forget this whole affair.",
				[
					(quest_set_slot, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_inactive),
					(call_script, "script_qp4_quest_odval_saving_face", floris_quest_update),
					(call_script, "script_qp4_quest_odval_saving_face", floris_quest_fail),
					(try_begin),
						(ge, "$quest_reactions", QUEST_REACTIONS_HIGH), # 3 successful quests required.
						(call_script, "script_qp4_quest_odval_redemption", floris_quest_fail),
					(else_try),
						(call_script, "script_qp4_quest_odval_redemption", floris_quest_succeed), # 2 of 2 required quests passed.
					(try_end),
					(jump_to_menu, "mnu_village"),
				]),
		]),
		
	##### QUEST - EDWYN FIRST KNIGHT #####
	("qp4_edwyn_knight_1",0,
		"You, {s14} and a few other companions sneak up to the edge of the bandit's encampment looking for any signs of the rogue knight.  Your patience pays off as a man in plate matching {s14}'s description of Sir Tenry comes into view giving orders to those around him.",
		"none",
		[
			(str_store_party_name, s13, reg1),
			(str_store_troop_name, s14, NPC_Edwyn),
			(troop_get_type, reg3, NPC_Edwyn),
		],
		[
			("edwyn_first_yes", [], "Begin the Assault...",
				[
					(call_script, "script_common_quest_change_state", "qst_edwyn_first_knight", qp4_edwyn_first_entered_lair),
					(party_set_slot, "$g_encountered_party", slot_party_ai_substate, 1),
					#(party_get_template_id, ":template", "$g_encountered_party"),
					(assign, "$g_enemy_party", "$g_encountered_party"),
							
					(try_begin),
					  # (eq, ":template", "pt_sea_raider_lair"),
					  # (assign, ":bandit_troop", "trp_sea_raider"),
					  # (assign, ":scene_to_use", "scn_lair_sea_raiders"),
					# (else_try),	
					  # (eq, ":template", "pt_forest_bandit_lair"),
					  # (assign, ":bandit_troop", "trp_forest_bandit"),
					  # (assign, ":scene_to_use", "scn_lair_forest_bandits"),
					# (else_try),
					  # (eq, ":template", "pt_desert_bandit_lair"),
					  # (assign, ":bandit_troop", "trp_desert_bandit"),
					  # (assign, ":scene_to_use", "scn_lair_desert_bandits"),
					# (else_try),
					  # (eq, ":template", "pt_mountain_bandit_lair"),
					  # (assign, ":bandit_troop", "trp_mountain_bandit"),
					  # (assign, ":scene_to_use", "scn_lair_mountain_bandits"),
					# (else_try),
					  # (eq, ":template", "pt_taiga_bandit_lair"),
					  # (assign, ":bandit_troop", "trp_taiga_bandit"),
					  # (assign, ":scene_to_use", "scn_lair_taiga_bandits"),
					# (else_try),
					  # (eq, ":template", "pt_steppe_bandit_lair"),
					  (assign, ":bandit_troop", "trp_steppe_bandit"), # "trp_bandit_n_steppe"),
					  (assign, ":scene_to_use", "scn_lair_steppe_bandits"),
					(try_end),
					
					(modify_visitors_at_site,":scene_to_use"),
					(reset_visitors),	    

					(store_character_level, ":player_level", "trp_player"),                   
					(store_add, ":number_of_bandits_will_be_spawned_at_each_period", 5, ":player_level"),
					(val_div, ":number_of_bandits_will_be_spawned_at_each_period", 3),
					
					(try_for_range, ":unused", 0, ":number_of_bandits_will_be_spawned_at_each_period"),
					  (store_random_in_range, ":random_entry_point", 2, 11),	      
					  (set_visitor, ":random_entry_point", ":bandit_troop", 1),	      
					(try_end),
					
					(set_visitor, 5, qp4_actor_named_knight, 1), # Add Sir Tenry to the scene.
					(troop_set_name, qp4_actor_named_knight, "@Sir Tenry"),
					
					(party_clear, "p_temp_casualties"),
					
					(set_party_battle_mode),
					(set_battle_advantage, 0),
					(assign, "$g_battle_result", 0),
					(set_jump_mission,"mt_bandit_lair"),
					
					(jump_to_scene, ":scene_to_use"),        
					(change_screen_mission),    
				]),
			  
			("edwyn_first_no", [], "Come back later.",
				[				
					(jump_to_menu, "mnu_bandit_lair"),
				]),
		]),
	
	##### QUEST - EDWYN SECOND KNIGHT #####
	("qp4_edwyn_knight_2",0,
		"Skirmish in the Streets of {s17}^^You and {s14} keep an eye out for the knight as you pass through the streets of {s17}, but do not see any immediate sign of Sir Henric.  Possibly a more detailed search will yield better results.^^OBJECTIVE:^ Slay Sir Henric and escape.^^WARNING:^ You will want to have at least a few companions (level 10+) in your party prior to attempting this.",
		"none",
		[
			(str_store_troop_name, s14, NPC_Edwyn),
			(str_store_party_name, s17, "$current_town"),
			(set_background_mesh, "mesh_pic_town1"),
		],
		[
			("edwyn_find_henric_yes", [], "Take a walk around the streets.",
				[
					(try_begin),
					   (party_get_slot, ":town_scene", "$current_town", slot_town_center),
					   (modify_visitors_at_site, ":town_scene"),
					   (reset_visitors),
					   (assign, "$g_mt_mode", tcm_default),
					   (store_faction_of_party, ":town_faction","$current_town"),
						
					   (try_begin),
						 (neq, ":town_faction", "fac_player_supporters_faction"),
						 (faction_get_slot, ":troop_prison_guard", "$g_encountered_party_faction", slot_faction_prison_guard_troop),
						 #(faction_get_slot, ":troop_castle_guard", "$g_encountered_party_faction", slot_faction_castle_guard_troop),
						 (faction_get_slot, ":tier_2_troop", ":town_faction", slot_faction_tier_2_troop),
						 (faction_get_slot, ":tier_3_troop", ":town_faction", slot_faction_tier_3_troop),
					   (else_try),
						 (party_get_slot, ":town_original_faction", "$current_town", slot_center_original_faction),
						 (faction_get_slot, ":troop_prison_guard", ":town_original_faction", slot_faction_prison_guard_troop),
						 #(faction_get_slot, ":troop_castle_guard", ":town_original_faction", slot_faction_castle_guard_troop),
						 (faction_get_slot, ":tier_2_troop", ":town_original_faction", slot_faction_tier_2_troop),
						 (faction_get_slot, ":tier_3_troop", ":town_original_faction", slot_faction_tier_3_troop),
					   (try_end),
					   (set_visitor, 24, ":troop_prison_guard"),
					   
					   (try_begin),
						 (gt,":tier_2_troop", 0),
						 (assign,reg0,":tier_3_troop"),
						 (assign,reg1,":tier_3_troop"),
						 (assign,reg2,":tier_2_troop"),
						 (assign,reg3,":tier_2_troop"),
					   (try_end),
					   (shuffle_range,0,4),
						
					   (party_get_slot, ":spawned_troop", "$current_town", slot_town_armorer),
					   (set_visitor, 9, ":spawned_troop"),
					   (party_get_slot, ":spawned_troop", "$current_town", slot_town_weaponsmith),
					   (set_visitor, 10, ":spawned_troop"),
					   (party_get_slot, ":spawned_troop", "$current_town", slot_town_elder),
					   (set_visitor, 11, ":spawned_troop"),
					   (party_get_slot, ":spawned_troop", "$current_town", slot_town_horse_merchant),
					   (set_visitor, 12, ":spawned_troop"),
					   (call_script, "script_init_town_walkers"),
					   (set_jump_mission,"mt_edwyn_town_fight"),
					   (assign, ":override_state", af_override_horse),
					   (try_begin),
						 (eq, "$sneaked_into_town", 1), #setup disguise
						 (assign, ":override_state", af_override_all),
					   (try_end),
					   (mission_tpl_entry_set_override_flags, "mt_town_center", 0, ":override_state"),
					   (mission_tpl_entry_set_override_flags, "mt_town_center", 2, ":override_state"),
					   (mission_tpl_entry_set_override_flags, "mt_town_center", 3, ":override_state"),
					   (mission_tpl_entry_set_override_flags, "mt_town_center", 4, ":override_state"),
					   (mission_tpl_entry_set_override_flags, "mt_town_center", 5, ":override_state"),
					   (mission_tpl_entry_set_override_flags, "mt_town_center", 6, ":override_state"),
					   (mission_tpl_entry_set_override_flags, "mt_town_center", 7, ":override_state"),
					   (try_begin),
						 (eq, "$town_entered", 0),
						 (assign, "$town_entered", 1),
						 (eq, "$town_nighttime", 0),
						 (set_jump_entry, 1),
					   (try_end),
					   (jump_to_scene, ":town_scene"),
					   (change_screen_mission),
					 (try_end),
				]),
			  
			("edwyn_find_henric_no", [], "Come back to look later.", [(jump_to_menu, "mnu_town"),]),
		]),
	
	##### QUEST - EDWYN THIRD KNIGHT #####
	("qp4_edwyn_third_knight",0,
		"Battle of {s13}^^You and {s14} have returned to the village of {s13} to take Sir Gerrin's forces by surprise and see him slain.  Ahead you can hear the sounds of a battle being waged.^^OBJECTIVE:^Slay Sir Gerrin and protect the villagers.^^WARNING:^You will want to have a reasonable sized host of at least thirty men to face Sir Gerrin's forces.",
		"none",
		[
			(str_store_party_name, s13, "$current_town"),
			(str_store_troop_name, s14, NPC_Edwyn),
			(troop_get_type, reg3, NPC_Edwyn),
			(set_background_mesh, "mesh_pic_villageriot"),
		],
		[
			("edwyn_third_yes", [], "Attack Sir Gerrin's forces.",
				[
					# Fill the player friend party.
					(call_script, "script_party_copy", "p_collective_friends", "p_main_party"),
					(call_script, "script_party_copy", "p_collective_friends_backup", "p_collective_friends"),
					# Fill the enemy friend party.
					(party_clear, "p_collective_enemy"),
					(party_add_members, "p_collective_enemy", qp4_actor_named_knight, 1),
					(party_add_members, "p_collective_enemy", qp4_actor_knight, 2),
					(party_add_members, "p_collective_enemy", qp4_actor_knight_support, 12),
					(assign, "$g_enemy_party", "p_collective_enemy"),
					
					(party_get_slot, ":scene_to_use", "$current_town", slot_castle_exterior),
					(modify_visitors_at_site,":scene_to_use"),
					(reset_visitors),
					(set_visitors, 0, qp4_actor_knight, 2),
					(set_visitors, 0, qp4_actor_knight_support, 12),
					(set_visitors, 0, qp4_actor_named_knight, 1),
					(troop_set_name, qp4_actor_named_knight, "@Sir Gerrin"),
					(party_get_slot, ":village_elder_troop", "$current_town",slot_town_elder),
					(set_visitor, 11, ":village_elder_troop"),
					
					##Floris MTT begin
					#(troop_get_slot,":mercenary_farmer", "$troop_trees", slot_mercenary_farmer),
					(store_faction_of_party, ":faction_no", "$current_town"),
					(faction_get_slot, ":culture", ":faction_no",  slot_faction_culture),
					(faction_get_slot, ":walker", ":culture",  slot_faction_village_walker_male_troop),
					(set_visitors, 2, ":walker", qp4_villagers_present_for_fight),
					##Floris MTT end
					(set_party_battle_mode),
					(set_battle_advantage, 0),
					(assign, "$g_battle_result", 0),
					(set_jump_mission,"mt_edwyn_village_fight"),
					(jump_to_scene, ":scene_to_use"),
					# (assign, "$g_next_menu", "mnu_village"),
					# (jump_to_menu, "mnu_battle_debrief"),
					# (assign, "$g_mt_mode", vba_normal),
					(change_screen_mission),
				]),
			  
			("edwyn_third_no", [], "Come back later.",
				[				
					(jump_to_menu, "mnu_village"),
				]),
		]),
		
 ]

from util_common import *
from util_wrappers import *

def modmerge_game_menus(orig_game_menus, check_duplicates = False):
    if( not check_duplicates ):
        orig_game_menus.extend(game_menus) # Use this only if there are no replacements (i.e. no duplicated item names)
    else:
    # Use the following loop to replace existing entries with same id
        for i in range (0,len(game_menus)-1):
          find_index = find_object(orig_game_menus, game_menus[i][0]); # find_object is from header_common.py
          if( find_index == -1 ):
            orig_game_menus.append(game_menus[i])
          else:
            orig_game_menus[find_index] = game_menus[i]
			
	# QUEST: ODVAL_ACCEPT_THE_CHALLENGE (village)
    find_index = find_object(orig_game_menus, "village")
    orig_game_menus[find_index][5].insert(3,
            ("qp4_odval_contest_1",[
			(party_slot_eq, "$current_town", slot_village_infested_by_bandits, 0),
	        (party_slot_eq, "$current_town", slot_village_state, svs_normal),
			(check_quest_active, "qst_odval_accept_the_challenge"),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_accepted),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_target_amount, 0),
			(eq, qp4_odval_home_town, "$current_town"),
			(str_store_party_name, s13, qp4_odval_home_town),],"Return to {s13} for contest. (Story Quest)", [(jump_to_menu, "mnu_qp4_odval_challenge"),]),
          )
	
	# QUEST: ODVAL_SAVING_FACE (village)
    find_index = find_object(orig_game_menus, "village")
    orig_game_menus[find_index][5].insert(3,
            ("qp4_odval_contest_2",[
			(party_slot_eq, "$current_town", slot_village_infested_by_bandits, 0),
	        (party_slot_eq, "$current_town", slot_village_state, svs_normal),
			(check_quest_active, "qst_odval_saving_face"),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_accepted),
			(neg|quest_slot_ge, "qst_odval_saving_face", slot_quest_target_amount, 4),
			(eq, qp4_odval_home_town, "$current_town"),
			(str_store_troop_name, s14, NPC_Odval),],"Return to fight {s14}. (Story Quest)", [(jump_to_menu, "mnu_qp4_odval_saving_face"),]),
          )
	
	# QUEST: EDWYN_FIRST_KNIGHT (bandit lair)
    find_index = find_object(orig_game_menus, "bandit_lair")
    orig_game_menus[find_index][5].insert(1, 
            ("qp4_edwyn_knight_1",
			[
				(check_quest_active, "qst_edwyn_first_knight"),
				(main_party_has_troop, NPC_Edwyn),
				(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_current_state, qp4_edwyn_first_found_lair_on_map),
				(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_stage_2_trigger_chance, "$g_encountered_party"),
			],"Investigate the Lair. (Story Quest)", [(jump_to_menu, "mnu_qp4_edwyn_knight_1"),]),
          )
	
	# QUEST: EDWYN_SECOND_KNIGHT (town)
    find_index = find_object(orig_game_menus, "town")
    orig_game_menus[find_index][5].insert(9, 
            ("qp4_edwyn_knight_2",
			[
				(check_quest_active, "qst_edwyn_second_knight"),
				(main_party_has_troop, NPC_Edwyn),
				(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_arrived_in_town),
				(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance, "$current_town"),
			],"Search for Sir Henric in the streets. (Story Quest)", [(jump_to_menu, "mnu_qp4_edwyn_knight_2"),]),
          )
	
	# QUEST: EDWYN_THIRD_KNIGHT (village)
    find_index = find_object(orig_game_menus, "village")
    orig_game_menus[find_index][5].insert(3,
            ("qp4_edwyn_knight_3",[
				(party_slot_eq, "$current_town", slot_village_infested_by_bandits, 0),
				(party_slot_eq, "$current_town", slot_village_state, svs_normal),
				(check_quest_active, "qst_edwyn_third_knight"),
				(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_planning_to_kill_knight),
				(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_stage_2_trigger_chance, "$current_town"),
			],"Attack Sir Gerrin's forces. (Story Quest)", [(jump_to_menu, "mnu_qp4_edwyn_third_knight"),]),
          )
	
	
	
# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "game_menus"
        orig_game_menus = var_set[var_name_1]
        modmerge_game_menus(orig_game_menus)
        # find_i = list_find_first_match_i( orig_game_menus, "town_trade_assessment" )
        # codeblock = GameMenuWrapper(orig_game_menus[find_i]).GetOpBlock()
        # line_i = codeblock.GetLength() - 2
        # codeblock.InsertBefore(line_i, hook_assessment_quest_initiation)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)