from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *

pmf_is_prisoner = 0x0001

####################################################################################################################
#  Each party template record contains the following fields:
#  1) Party-template id: used for referencing party-templates in other files.
#     The prefix pt_ is automatically added before each party-template id.
#  2) Party-template name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Faction
#  6) Personality. See header_parties.py for an explanation of personality flags.
#  7) List of stacks. Each stack record is a tuple that contains the following fields:
#    7.1) Troop-id. 
#    7.2) Minimum number of troops in the stack. 
#    7.3) Maximum number of troops in the stack. 
#    7.4) Member flags(optional). Use pmf_is_prisoner to note that this member is a prisoner.
#     Note: There can be at most 6 stacks.
####################################################################################################################


party_templates = [
  ("none","none",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("rescued_prisoners","Rescued Prisoners",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("enemy","Enemy",icon_gray_knight,0,fac_undeads,merchant_personality,[]),
  ("hero_party","Hero Party",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
####################################################################################################################
# Party templates before this point are hard-wired into the game and should not be changed. 
####################################################################################################################
##  ("old_garrison","Old Garrison",icon_vaegir_knight,0,fac_neutral,merchant_personality,[]),
  ("village_defenders","Village Defenders",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,10,20),(trp_peasant_woman,0,4)]),

  ("cattle_herd","Cattle Herd",icon_cattle|carries_goods(10),0,fac_neutral,merchant_personality,[(trp_cattle,80,120)]),

##  ("vaegir_nobleman","Vaegir Nobleman",icon_vaegir_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_vaegir_knight,2,6),(trp_vaegir_horseman,4,12)]),
##  ("swadian_nobleman","Swadian Nobleman",icon_gray_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_swadian_knight,2,6),(trp_swadian_man_at_arms,4,12)]),
# Ryan BEGIN
  ("looters","Looters",icon_axeman|carries_goods(8),0,fac_outlaws,bandit_personality,[(trp_looter,3,45)]),
# Ryan END
  ("manhunters","Manhunters",icon_gray_knight,0,fac_manhunters,soldier_personality,[(trp_manhunter,9,40)]),
##  ("peasant","Peasant",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,1,6),(trp_peasant_woman,0,7)]),

#  ("black_khergit_raiders","Black Khergit Raiders",icon_khergit_horseman_b|carries_goods(2),0,fac_black_khergits,bandit_personality,[(trp_black_khergit_guard,1,10),(trp_black_khergit_horseman,5,5)]),
  ("steppe_bandits","Steppe Bandits",icon_khergit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_steppe_raider_chief,1,1),(trp_steppe_runner,4,15),(trp_steppe_guard,4,15),(trp_steppe_bandit,4,15)]),
  ("taiga_bandits","Tundra Bandits",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_taiga_leader,1,1),(trp_taiga_spearman,4,15),(trp_taiga_javelineer,4,15),(trp_taiga_bandit,4,15)]),
  ("desert_bandits","Desert Bandits",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_desert_leader,1,1),(trp_desert_fighter,4,15),(trp_desert_nomad,4,15),(trp_desert_bandit,4,15)]),
##DAWG+EDIT FOREST BANDIT PARTY##
  ("forest_bandits","Forest Bandits",icon_axeman|carries_goods(2),0,fac_forest_bandits,bandit_personality,[(trp_forest_leader,1,1),(trp_forest_bandit,4,15),(trp_forest_footpad,4,15),(trp_forest_poacher,4,15)]),
  ("mountain_bandits","Mountain Bandits",icon_axeman|carries_goods(2),0,fac_mountain_bandits,bandit_personality,[(trp_mountain_chief,1,1),(trp_mountain_bandit,4,15),(trp_mountain_tracker,4,15),(trp_mountain_hunter,4,15)]),
##DAWG+EDIT SEA RAIDERS PARTY##
  ("sea_raiders","Sea Raiders",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_nord_chieftain,1,1),(trp_sea_raider,5,16),(trp_marauder,5,16),(trp_nordsman_pelttracker,5,16)]),
  # ("forest_bandits","Forest Bandits",icon_bandit_forest_bandit|carries_goods(2),0,fac_forest_bandits,bandit_personality,[(trp_forest_leader,1,1),(trp_forest_bandit,4,15),(trp_forest_footpad,4,15),(trp_forest_poacher,4,15)]),
  # ("mountain_bandits","Mountain Bandits",icon_bandit_mountain_bandit|carries_goods(2),0,fac_mountain_bandits,bandit_personality,[(trp_mountain_chief,1,1),(trp_mountain_bandit,4,15),(trp_mountain_tracker,4,15),(trp_mountain_hunter,4,15)]),
  # ("sea_raiders","Sea Raiders",icon_bandit_sea_raider|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_nord_chieftain,1,1),(trp_sea_raider,5,16),(trp_marauder,5,16),(trp_nordsman_pelttracker,5,16)]),

  ("deserters","Deserters",icon_vaegir_knight|carries_goods(3),0,fac_deserters,bandit_personality,[]),
    
  ("merchant_caravan","Merchant Caravan",icon_gray_knight|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,5,25)]),
  ("troublesome_bandits","Troublesome Bandits",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_outlaws,bandit_personality,[(trp_bandit,14,55)]),
  ("bandits_awaiting_ransom","Bandits Awaiting Ransom",icon_axeman|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_bandit,24,58),(trp_kidnapped_girl,1,1,pmf_is_prisoner)]),
  ("kidnapped_girl","Kidnapped Girl",icon_woman|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_kidnapped_girl,1,1)]),

  ("village_farmers","Village Farmers",icon_peasant|pf_civilian,0,fac_innocents,merchant_personality,[(trp_farmer,5,10),(trp_peasant_woman,3,8)]),

  ("spy_partners", "Unremarkable Travellers", icon_gray_knight|carries_goods(10)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner,1,1),(trp_caravan_guard,5,11)]),
  ("runaway_serfs","Runaway Serfs",icon_peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_farmer,6,7), (trp_peasant_woman,3,3)]),
  ("spy", "Ordinary Townsman", icon_gray_knight|carries_goods(4)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy,1,1)]),
  ("sacrificed_messenger", "Sacrificed Messenger", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[]),
##  ("conspirator", "Conspirators", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator,3,4)]),
##  ("conspirator_leader", "Conspirator Leader", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator_leader,1,1)]),
##  ("peasant_rebels", "Peasant Rebels", icon_peasant,0,fac_peasant_rebels,bandit_personality,[(trp_peasant_rebel,33,97)]),
##  ("noble_refugees", "Noble Refugees", icon_gray_knight|carries_goods(12)|pf_quest_party,0,fac_noble_refugees,merchant_personality,[(trp_noble_refugee,3,5),(trp_noble_refugee_woman,5,7)]),

  ("forager_party","Foraging Party",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("scout_party","Scouts",icon_gray_knight|carries_goods(1)|pf_show_faction,0,fac_commoners,bandit_personality,[]),
  ("patrol_party","Patrol",icon_gray_knight|carries_goods(2)|pf_show_faction,0,fac_commoners,soldier_personality,[]),
#  ("war_party", "War Party",icon_gray_knight|carries_goods(3),0,fac_commoners,soldier_personality,[]),
  ("messenger_party","Messenger",icon_gray_knight|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("raider_party","Raiders",icon_gray_knight|carries_goods(16)|pf_quest_party,0,fac_commoners,bandit_personality,[]),
  ("raider_captives","Raider Captives",0,0,fac_commoners,0,[(trp_peasant_woman,6,30,pmf_is_prisoner)]),
  ("kingdom_caravan_party","Caravan",icon_mule|carries_goods(25)|pf_show_faction,0,fac_commoners,merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,12,40)]),
  ("prisoner_train_party","Prisoner Train",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("default_prisoners","Default Prisoners",0,0,fac_commoners,0,[(trp_bandit,5,10,pmf_is_prisoner)]),

  ("routed_warriors","Routed Enemies",icon_vaegir_knight,0,fac_commoners,soldier_personality,[]),


# Caravans
  ("center_reinforcements","Reinforcements",icon_axeman|carries_goods(16),0,fac_commoners,soldier_personality,[(trp_townsman,5,30),(trp_watchman,4,20)]),  

  ("kingdom_hero_party","War Party",icon_flagbearer_a|pf_show_faction|pf_default_behavior,0,fac_commoners,soldier_personality,[]),
  
 ## REINFORCEMENTS
  
 ## WINDYPLAINS+ ## - Added reinforcement templates for player's culture.
 ### PLAYER CUSTOM CULTURE ###
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to kingdom_parties (50%) and centers (65%) - infantry, Easy 5-10, Normal 7-14, Hard 14-15, Very Hard 20-20
 # Reinforcement B gets added to kingdom_parties (25%) and centers (35%) - archers Easy 3-7, Normal 5-10, Hard 10-11. Very Hard 14-14
 # Reinforcement C gets added to kingdom_parties (25%) only - cavalry and pikemen Easy 1-3, Normal 3-5, Hard 5-6, Very Hard 9-9
 # GAME_MODE_EASY
 ("kingdom_0_reinforcements_a", "kingdom_0_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_player_tier_2,16,36),(trp_player_tier_3_infantry,3,7)]),
 ("kingdom_0_reinforcements_b", "kingdom_0_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_player_tier_3_infantry,8,15),(trp_player_tier_3_ranged,6,13)]),
 ("kingdom_0_reinforcements_c", "kingdom_0_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_player_tier_4_infantry,2,5),(trp_player_tier_4_ranged,2,5),(trp_player_tier_4_mounted,2,6)]),
 # GAME_MODE_NORMAL
 ("kingdom_0_reinforcements_d", "kingdom_0_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_player_tier_2,11,26),(trp_player_tier_3_infantry,3,7),(trp_player_tier_3_ranged,5,10)]),
 ("kingdom_0_reinforcements_e", "kingdom_0_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_player_tier_4_infantry,8,15),(trp_player_tier_4_ranged,5,13)]),
 ("kingdom_0_reinforcements_f", "kingdom_0_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_player_tier_5_mounted,2,6),(trp_player_tier_5_infantry,2,5),(trp_player_tier_5_ranged,2,5)]),
 # GAME_MODE_HARD
 ("kingdom_0_reinforcements_g", "kingdom_0_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_player_tier_3_infantry,8,20),(trp_player_tier_3_ranged,6,13),]),
 ("kingdom_0_reinforcements_h", "kingdom_0_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_player_tier_4_infantry,5,10),(trp_player_tier_4_ranged,3,8),(trp_player_tier_4_mounted,5,10)]),
 ("kingdom_0_reinforcements_i", "kingdom_0_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_player_tier_5_infantry,2,5),(trp_player_tier_5_ranged,2,5),(trp_player_tier_5_mounted,2,6)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_0_reinforcements_j", "kingdom_0_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_player_tier_3_ranged,2,4),(trp_player_tier_4_infantry,3,8),(trp_player_tier_4_ranged,3,6),(trp_player_tier_4_mounted,6,15)]),
 ("kingdom_0_reinforcements_k", "kingdom_0_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_player_tier_4_infantry,1,4),(trp_player_tier_4_ranged,1,3),(trp_player_tier_4_mounted,8,13),(trp_player_tier_5_infantry,2,4),(trp_player_tier_5_ranged,1,4)]),
 ("kingdom_0_reinforcements_l", "kingdom_0_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_player_tier_5_infantry,2,3),(trp_player_tier_5_ranged,2,3),(trp_player_tier_5_mounted,2,10)]),
 
 ### SWADIA ### - NEW TROOPS
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to kingdom_parties (50%) and centers (65%) - infantry, Easy 5-10, Normal 7-14, Hard 14-15, Very Hard 20-20
 # Reinforcement B gets added to kingdom_parties (25%) and centers (35%) - archers Easy 3-7, Normal 5-10, Hard 10-11. Very Hard 14-14
 # Reinforcement C gets added to kingdom_parties (25%) only - cavalry and pikemen Easy 1-3, Normal 3-5, Hard 5-6, Very Hard 9-9
 # GAME_MODE_EASY
 ("kingdom_1_reinforcements_a", "kingdom_1_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_n_swadian_recruit, 3, 6), (trp_n_swadian_militia, 2, 4)]),
 ("kingdom_1_reinforcements_b", "kingdom_1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_n_swadian_crossbowman, 3, 7)]),
 ("kingdom_1_reinforcements_c", "kingdom_1_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_n_swadian_lancer, 1, 3)]),
 # GAME_MODE_NORMAL
 ("kingdom_1_reinforcements_d", "kingdom_1_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_n_swadian_recruit, 2, 4), (trp_n_swadian_militia, 5, 8), (trp_n_swadian_sergeant, 0, 1)]),
 ("kingdom_1_reinforcements_e", "kingdom_1_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_n_swadian_crossbowman, 5, 10)]),
 ("kingdom_1_reinforcements_f", "kingdom_1_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_n_swadian_lancer, 3, 4), (trp_n_swadian_knight, 0, 1)]),
  # GAME_MODE_HARD
 ("kingdom_1_reinforcements_g", "kingdom_1_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_n_swadian_militia, 12, 12), (trp_n_swadian_sergeant, 2, 3)]),
 ("kingdom_1_reinforcements_h", "kingdom_1_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_n_swadian_crossbowman, 10, 11)]),
 ("kingdom_1_reinforcements_i", "kingdom_1_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_n_swadian_lancer, 4, 4), (trp_n_swadian_knight, 1, 2)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_1_reinforcements_j", "kingdom_1_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_n_swadian_militia, 16, 16), (trp_n_swadian_sergeant, 4, 4)]),
 ("kingdom_1_reinforcements_k", "kingdom_1_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_n_swadian_crossbowman, 14, 14)]),
 ("kingdom_1_reinforcements_l", "kingdom_1_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_n_swadian_lancer, 5, 5), (trp_n_swadian_knight, 4, 4)]),
 

 ### VAEGIRS ### - NEW TROOPS
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to kingdom_parties (50%) and centers (65%) - infantry, Easy 3-5, Normal 5-7, Hard 8-9. Very Hard 11-11
 # Reinforcement B gets added to kingdom_parties (25%) and centers (35%) - archers Easy 5-10, Normal 7-14, Hard 14-15, Very Hard 20-20
 # Reinforcement C gets added to kingdom_parties (25%) only - cavalry and pikemen Easy 2-6, Normal 6-8, Hard 9-10, Very Hard 14-14
 # GAME_MODE_EASY
 ("kingdom_2_reinforcements_a", "kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_n_vaegir_recruit, 1, 2), (trp_n_vaegir_skirmisher, 2, 3)]),
 ("kingdom_2_reinforcements_b", "kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_n_vaegir_bowman, 5, 10)]),
 ("kingdom_2_reinforcements_c", "kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_n_vaegir_raider, 2, 4), (trp_n_vaegir_headhunter, 0, 2)]),
 # GAME_MODE_NORMAL
 ("kingdom_2_reinforcements_d", "kingdom_2_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_n_vaegir_recruit, 1, 1), (trp_n_vaegir_skirmisher, 4, 5), (trp_n_vaegir_guard, 0, 1)]),
 ("kingdom_2_reinforcements_e", "kingdom_2_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_n_vaegir_bowman, 7, 14)]),
 ("kingdom_2_reinforcements_f", "kingdom_2_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_n_vaegir_raider, 3, 4), (trp_n_vaegir_headhunter, 3, 3), (trp_n_vaegir_bogatyr, 0, 1)]),
 # GAME_MODE_HARD
 ("kingdom_2_reinforcements_g", "kingdom_2_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_n_vaegir_skirmisher, 7, 7), (trp_n_vaegir_guard, 1, 2)]),
 ("kingdom_2_reinforcements_h", "kingdom_2_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_n_vaegir_bowman, 14, 15)]),
 ("kingdom_2_reinforcements_i", "kingdom_2_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_n_vaegir_raider, 3, 3), (trp_n_vaegir_headhunter, 5, 5), (trp_n_vaegir_bogatyr, 1, 2)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_2_reinforcements_j", "kingdom_2_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_n_vaegir_skirmisher, 7, 7), (trp_n_vaegir_guard, 4, 4)]),
 ("kingdom_2_reinforcements_k", "kingdom_2_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_n_vaegir_bowman, 20, 20)]),
 ("kingdom_2_reinforcements_l", "kingdom_2_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_n_vaegir_raider, 3, 3), (trp_n_vaegir_headhunter, 6, 6), (trp_n_vaegir_bogatyr, 5, 5)]),
 

 ### KHERGITS ### - NEW TROOPS - a lot of cavalry, bigger, less elite parties = slower
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to kingdom_parties (50%) and centers (65%) - infantry Easy 2-6, Normal 6-8, Hard 9-10, Very Hard 14-14
 # Reinforcement B gets added to kingdom_parties (25%) and centers (35%) - archers Easy 5-10, Normal 7-14, Hard 14-15, Very Hard 20-20
 # Reinforcement C gets added to kingdom_parties (25%) only - cavalry and pikemen Easy 3-5, Normal 5-7, Hard 8-9. Very Hard 11-11
 # GAME_MODE_EASY
 ("kingdom_3_reinforcements_a", "kingdom_3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_n_khergit_recruit, 2, 6)]), 
 ("kingdom_3_reinforcements_b", "kingdom_3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_n_khergit_scout, 5, 9), (trp_n_khergit_skirmisher, 0, 1)]), 
 ("kingdom_3_reinforcements_c", "kingdom_3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_n_khergit_lancer, 3, 5)]), 
 # GAME_MODE_NORMAL
 ("kingdom_3_reinforcements_d", "kingdom_3_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_n_khergit_recruit, 2, 3), (trp_n_khergit_shaman, 2, 2), (trp_n_khergit_clansman, 2, 3)]), 
 ("kingdom_3_reinforcements_e", "kingdom_3_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_n_khergit_scout, 5, 11), (trp_n_khergit_skirmisher, 2, 3)]), #
 ("kingdom_3_reinforcements_f", "kingdom_3_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_n_khergit_lancer, 4, 5), (trp_n_khergit_keshig, 1, 2)]), #
 # GAME_MODE_HARD
 ("kingdom_3_reinforcements_g", "kingdom_3_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_n_khergit_shaman, 4, 5), (trp_n_khergit_clansman, 5, 5)]), 
 ("kingdom_3_reinforcements_h", "kingdom_3_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_n_khergit_scout, 10, 11), (trp_n_khergit_skirmisher, 4, 4)]), 
 ("kingdom_3_reinforcements_i", "kingdom_3_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_n_khergit_lancer, 5, 5), (trp_n_khergit_keshig, 3, 4)]), 
 # GAME_MODE_VERY_HARD
 ("kingdom_3_reinforcements_j", "kingdom_3_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_n_khergit_shaman, 6, 6), (trp_n_khergit_clansman, 8, 8)]), 
 ("kingdom_3_reinforcements_k", "kingdom_3_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_n_khergit_scout, 13, 13), (trp_n_khergit_skirmisher, 7, 7)]), #
 ("kingdom_3_reinforcements_l", "kingdom_3_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_n_khergit_lancer, 6, 6), (trp_n_khergit_keshig, 5, 5)]), 
 
 
 ### NORDS ### - NEW TROOPS - smaller elite parties = faster
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to kingdom_parties (50%) and centers (65%) - infantry, Easy 3-8, Normal 5-10, Hard 9-10, Very Hard 13-13
 # Reinforcement B gets added to kingdom_parties (25%) and centers (35%) - archers Easy 3-4, Normal 4-6, Hard 6-7. Very Hard 9-9
 # Reinforcement C gets added to kingdom_parties (25%) only - cavalry and pikemen Easy 0, 1, Normal 2-3, Hard 3-4, Very Hard 4-5
 # GAME_MODE_EASY
 ("kingdom_4_reinforcements_a", "kingdom_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_n_nordic_recruit, 1, 3), (trp_n_nordic_skald, 1, 3), (trp_n_nordic_spearman, 1, 2)]),
 ("kingdom_4_reinforcements_b", "kingdom_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_n_nordic_tracker, 3, 4)]),
 ("kingdom_4_reinforcements_c", "kingdom_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_n_nordic_berserker, 0, 1)]),
 # GAME_MODE_NORMAL
 ("kingdom_4_reinforcements_d", "kingdom_4_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_n_nordic_recruit, 0, 1), (trp_n_nordic_skald, 3, 5), (trp_n_nordic_spearman, 2, 4), (trp_n_nordic_berserker, 0, 1)]),
 ("kingdom_4_reinforcements_e", "kingdom_4_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_n_nordic_tracker, 4, 5), (trp_n_nordic_retinue_archer, 0, 1)]),
 ("kingdom_4_reinforcements_f", "kingdom_4_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_n_nordic_berserker, 2, 3)]),
 # GAME_MODE_HARD
 ("kingdom_4_reinforcements_g", "kingdom_4_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_n_nordic_skald, 3, 3), (trp_n_nordic_spearman, 4, 4), (trp_n_nordic_berserker, 2, 3),]),
 ("kingdom_4_reinforcements_h", "kingdom_4_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_n_nordic_tracker, 4, 5), (trp_n_nordic_retinue_archer, 2, 2)]),
 ("kingdom_4_reinforcements_i", "kingdom_4_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_n_nordic_berserker, 3, 4)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_4_reinforcements_j", "kingdom_4_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_n_nordic_skald, 4, 4), (trp_n_nordic_spearman, 5, 5), (trp_n_nordic_berserker, 4, 4)]),
 ("kingdom_4_reinforcements_k", "kingdom_4_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_n_nordic_tracker, 5, 5), (trp_n_nordic_retinue_archer, 4, 4)]),
 ("kingdom_4_reinforcements_l", "kingdom_4_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_n_nordic_berserker, 4, 5)]),
 
 
 ### RHODOKS ### - NEW TROOPS
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to kingdom_parties (50%) and centers (65%) - infantry, Easy 3-5, Normal 4-8, Hard 7-8, Very Hard 11-11
 # Reinforcement B gets added to kingdom_parties (25%) and centers (35%) - archers Easy 3-4, Normal 4-6, Hard 6-7. Very Hard 9-9
 # Reinforcement C gets added to kingdom_parties (25%) only - cavalry and pikemen Easy 2-3, Normal 4-5, Hard 5-6, Very Hard 7-8
 # GAME_MODE_EASY
 ("kingdom_5_reinforcements_a", "kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_n_rhodok_recruit, 1, 2), (trp_n_rhodok_footman, 1, 2), (trp_n_rhodok_halberdier, 1, 1)]),
 ("kingdom_5_reinforcements_b", "kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_n_rhodok_ranger, 3, 4)]),
 ("kingdom_5_reinforcements_c", "kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_n_rhodok_pikeman, 2, 3)]),
 # GAME_MODE_NORMAL
 ("kingdom_5_reinforcements_d", "kingdom_5_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_n_rhodok_recruit, 1, 1), (trp_n_rhodok_footman, 1, 4), (trp_n_rhodok_halberdier, 1, 2), (trp_n_rhodok_foot_knight, 0, 1)]),
 ("kingdom_5_reinforcements_e", "kingdom_5_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_n_rhodok_ranger, 4, 5), (trp_n_rhodok_siege_breaker, 0, 1)]),
 ("kingdom_5_reinforcements_f", "kingdom_5_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_n_rhodok_pikeman, 4, 5)]),
 # GAME_MODE_HARD
 ("kingdom_5_reinforcements_g", "kingdom_5_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_n_rhodok_footman, 4, 4), (trp_n_rhodok_halberdier, 2, 2), (trp_n_rhodok_foot_knight, 1, 2)]),
 ("kingdom_5_reinforcements_h", "kingdom_5_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_n_rhodok_ranger, 5, 5), (trp_n_rhodok_siege_breaker, 1, 2)]),
 ("kingdom_5_reinforcements_i", "kingdom_5_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_n_rhodok_pikeman, 5, 6)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_5_reinforcements_j", "kingdom_5_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_n_rhodok_footman, 3, 3), (trp_n_rhodok_halberdier, 6, 6), (trp_n_rhodok_foot_knight, 2, 2)]),
 ("kingdom_5_reinforcements_k", "kingdom_5_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_n_rhodok_ranger, 5, 5), (trp_n_rhodok_siege_breaker, 4, 4)]),
 ("kingdom_5_reinforcements_l", "kingdom_5_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_n_rhodok_pikeman, 7, 8)]),
 
 
 ### SARRANID ### - NEW TROOPS
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to kingdom_parties (50%) and centers (65%) - infantry,Easy 3-7, Normal 5-10, Hard 10-11. Very Hard 14-14 
 # Reinforcement B gets added to kingdom_parties (25%) and centers (35%) - archers Easy 5-10, Normal 7-14, Hard 14-15, Very Hard 20-20
 # Reinforcement C gets added to kingdom_parties (25%) only - cavalry and pikemen Easy 1-3, Normal 3-5, Hard 5-6, Very Hard 9-9
 # GAME_MODE_EASY
 ("kingdom_6_reinforcements_a", "kingdom_6_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_n_sarranid_recruit, 2, 5), (trp_n_sarranid_fighter, 1, 2)]),
 ("kingdom_6_reinforcements_b", "kingdom_6_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_n_sarranid_marksman, 5, 9), (trp_n_sarranid_skirmisher, 0, 1)]),
 ("kingdom_6_reinforcements_c", "kingdom_6_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_n_sarranid_tribesman, 1, 3)]),
 # GAME_MODE_NORMAL
 ("kingdom_6_reinforcements_d", "kingdom_6_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_n_sarranid_recruit, 2, 5), (trp_n_sarranid_fighter, 3, 4), (trp_n_sarranid_guard, 0, 1)]),
 ("kingdom_6_reinforcements_e", "kingdom_6_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_n_sarranid_marksman, 6, 11), (trp_n_sarranid_skirmisher, 1, 3)]),
 ("kingdom_6_reinforcements_f", "kingdom_6_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_n_sarranid_tribesman, 1, 2), (trp_n_sarranid_mamluke, 2, 2), (trp_n_sarranid_skirmisher, 0, 1)]),
 # GAME_MODE_HARD
 ("kingdom_6_reinforcements_g", "kingdom_6_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_n_sarranid_fighter, 9, 9), (trp_n_sarranid_guard, 1, 2)]),
 ("kingdom_6_reinforcements_h", "kingdom_6_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_n_sarranid_marksman, 10, 11), (trp_n_sarranid_skirmisher, 4, 4)]),
 ("kingdom_6_reinforcements_i", "kingdom_6_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_n_sarranid_tribesman, 1, 2), (trp_n_sarranid_mamluke, 3, 3), (trp_n_sarranid_skirmisher, 1, 2)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_6_reinforcements_j", "kingdom_6_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_n_sarranid_fighter, 11, 11), (trp_n_sarranid_guard, 3, 3)]),
 ("kingdom_6_reinforcements_k", "kingdom_6_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_n_sarranid_marksman, 13, 13), (trp_n_sarranid_skirmisher, 7, 7)]),
 ("kingdom_6_reinforcements_l", "kingdom_6_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_n_sarranid_tribesman, 3, 3), (trp_n_sarranid_mamluke, 4, 4), (trp_n_sarranid_skirmisher, 2, 2)]),


  ("steppe_bandit_lair" ,"Steppe Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_steppe_bandit,15,58)]),
  ("taiga_bandit_lair","Tundra Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_taiga_bandit,15,58)]),
  ("desert_bandit_lair" ,"Desert Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_desert_bandit,15,58)]),
  ("forest_bandit_lair" ,"Forest Bandit Camp",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_forest_bandit,15,58)]),
  ("mountain_bandit_lair" ,"Mountain Bandit Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_mountain_bandit,15,58)]),
  ("sea_raider_lair","Sea Raider Landing",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_sea_raider,15,50)]),
  ("looter_lair","Kidnappers' Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_looter,15,25)]),
  
  ("bandit_lair_templates_end","{!}bandit_lair_templates_end",icon_axeman|carries_goods(2)|pf_is_static,0,fac_outlaws,bandit_personality,[(trp_sea_raider,15,50)]),

  ("leaded_looters","Band of robbers",icon_axeman|carries_goods(8)|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_looter_leader,1,1),(trp_looter,3,3)]),
  
  ("troop_testing_party_1", "Troop Testing Party", icon_axeman|pf_is_static, 0, fac_commoners, troop_testers, [(trp_item_balancing_pike, 50, 50)]),
  ("troop_testing_party_2", "Troop Testing Party", icon_axeman|pf_is_static, 0, fac_commoners, troop_testers, [(trp_item_balancing_lance, 50, 50)]),
]
