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
  
# Reinforcements
  # each faction includes three party templates. One is less-modernised, one is med-modernised and one is high-modernised
  # less-modernised templates are generally includes 7-14 troops in total, 
  # med-modernised templates are generally includes 5-10 troops in total, 
  # high-modernised templates are generally includes 3-5 troops in total


 ## WINDYPLAINS+ ## - Added reinforcement templates for player's culture.
 ### PLAYER CUSTOM CULTURE ###
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to kingdom_parties (50%) and centers (65%).
 # Reinforcement B gets added to kingdom_parties (25%) and centers (35%).
 # Reinforcement C gets added to kingdom_parties (25%) only .
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
 # GAME_MODE_EASY
 ("kingdom_1_reinforcements_a", "kingdom_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_new_swadian_farmer, 4, 12), (trp_new_swadian_militia, 4, 10), (trp_new_swadian_supplyman, 1, 5), (trp_new_swadian_hunter, 0, 2), (trp_new_swadian_footman, 0, 1)]),
 ("kingdom_1_reinforcements_b", "kingdom_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_new_swadian_crossbowman, 2, 5), (trp_new_swadian_hunter, 2, 5), (trp_new_swadian_supplyman, 6, 7), (trp_new_swadian_militia, 7, 12), (trp_new_swadian_footman, 0, 4)]),
 ("kingdom_1_reinforcements_c", "kingdom_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_new_swadian_lancer, 4, 12), (trp_new_swadian_man_at_arms, 3, 5)]),
 # GAME_MODE_NORMAL
 ("kingdom_1_reinforcements_d", "kingdom_4_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_new_swadian_farmer, 4, 8), (trp_new_swadian_militia, 4, 12), (trp_new_swadian_supplyman, 4, 5), (trp_new_swadian_hunter, 1, 2), (trp_new_swadian_footman, 5, 10)]),
 ("kingdom_1_reinforcements_e", "kingdom_4_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_new_swadian_crossbowman, 2, 6), (trp_new_swadian_hunter, 4, 7), (trp_new_swadian_supplyman, 5, 13), (trp_new_swadian_billman, 0, 3), (trp_new_swadian_footman, 0, 5)]),
 ("kingdom_1_reinforcements_f", "kingdom_4_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_new_swadian_lancer, 6, 8), (trp_new_swadian_man_at_arms, 4, 5)]),
 # GAME_MODE_HARD
 ("kingdom_1_reinforcements_g", "kingdom_4_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_new_swadian_crossbowman, 7, 12), (trp_new_swadian_supplyman, 4, 5), (trp_new_swadian_sargeant, 6, 13), (trp_new_swadian_billman, 4, 5)]),
 ("kingdom_1_reinforcements_h", "kingdom_4_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_new_swadian_crossbowman, 3, 7), (trp_new_swadian_supplyman, 2, 3), (trp_new_swadian_billman, 3, 8), (trp_new_swadian_sargeant, 5, 10)]),
 ("kingdom_1_reinforcements_i", "kingdom_4_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_new_swadian_lancer, 3, 5), (trp_new_swadian_man_at_arms, 4, 8), (trp_new_swadian_knight, 0, 4)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_1_reinforcements_j", "kingdom_4_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_new_swadian_crossbowman, 1, 5), (trp_new_swadian_supplyman, 0, 1), (trp_new_swadian_sargeant, 2, 8), (trp_new_swadian_billman, 2, 8)]),
 ("kingdom_1_reinforcements_k", "kingdom_4_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_new_swadian_crossbowman, 2, 4), (trp_new_swadian_supplyman, 0, 1), (trp_new_swadian_billman, 3, 8), (trp_new_swadian_sargeant, 5, 10), (trp_new_swadian_footman, 5 , 10)]),
 ("kingdom_1_reinforcements_l", "kingdom_4_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_new_swadian_lancer, 1, 4), (trp_new_swadian_man_at_arms, 5, 12), (trp_new_swadian_knight, 1, 6)]),
 

 ### VAEGIRS ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_2_reinforcements_a", "kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_r_vaegir_sentry,16,36),(trp_r_vaegir_psiloi,3,7)]),
 ("kingdom_2_reinforcements_b", "kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_r_vaegir_psiloi,8,15),(trp_r_vaegir_skirmisher,6,13)]),
 ("kingdom_2_reinforcements_c", "kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_r_vaegir_peltast,2,5),(trp_r_vaegir_longbowman,2,5),(trp_r_vaegir_koursores,1,3),(trp_r_vaegir_pecheneg,1,3)]),
 # GAME_MODE_NORMAL
 ("kingdom_2_reinforcements_d", "kingdom_2_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_r_vaegir_sentry,11,26),(trp_r_vaegir_psiloi,3,7),(trp_r_vaegir_skirmisher,5,10)]),
 ("kingdom_2_reinforcements_e", "kingdom_2_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_r_vaegir_peltast,8,15),(trp_r_vaegir_longbowman,5,13)]),
 ("kingdom_2_reinforcements_f", "kingdom_2_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_r_vaegir_cavalrycaptain,1,3),(trp_r_vaegir_bogatyr,1,3),(trp_r_vaegir_vanguard,2,5),(trp_r_vaegir_marksman,2,5)]),
 # GAME_MODE_HARD
 ("kingdom_2_reinforcements_g", "kingdom_2_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_r_vaegir_psiloi,8,20),(trp_r_vaegir_skirmisher,6,13)]),
 ("kingdom_2_reinforcements_h", "kingdom_2_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_r_vaegir_peltast,5,10),(trp_r_vaegir_longbowman,3,8),(trp_r_vaegir_koursores,2,5),(trp_r_vaegir_pecheneg,3,5)]),
 ("kingdom_2_reinforcements_i", "kingdom_2_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_r_vaegir_vanguard,2,5),(trp_r_vaegir_marksman,2,5),(trp_r_vaegir_cavalrycaptain,1,3),(trp_r_vaegir_bogatyr,1,3)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_2_reinforcements_j", "kingdom_2_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_r_vaegir_skirmisher,2,4),(trp_r_vaegir_peltast,3,8),(trp_r_vaegir_longbowman,3,6),(trp_r_vaegir_koursores,3,7),(trp_r_vaegir_pecheneg,3,8)]),
 ("kingdom_2_reinforcements_k", "kingdom_2_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_r_vaegir_peltast,1,4),(trp_r_vaegir_longbowman,1,3),(trp_r_vaegir_koursores,4,6),(trp_r_vaegir_pecheneg,4,7),(trp_r_vaegir_vanguard,2,4),(trp_r_vaegir_marksman,1,4)]),
 ("kingdom_2_reinforcements_l", "kingdom_2_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_r_vaegir_vanguard,2,3),(trp_r_vaegir_marksman,2,3),(trp_r_vaegir_cavalrycaptain,1,5),(trp_r_vaegir_bogatyr,1,5)]),
 

 ### KHERGITS ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_3_reinforcements_a", "kingdom_3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_r_khergit_slave,16,36),(trp_r_khergit_outcast, 5, 10), (trp_r_khergit_surcin, 10, 15)]), 
 ("kingdom_3_reinforcements_b", "kingdom_3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_r_khergit_scout, 25, 35)]), 
 ("kingdom_3_reinforcements_c", "kingdom_3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_r_khergit_lancer, 1, 2), (trp_r_khergit_morici, 1, 6), (trp_r_khergit_abaci, 1, 5) ]), 
 # GAME_MODE_NORMAL
 ("kingdom_3_reinforcements_d", "kingdom_3_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_r_khergit_asud, 5, 10), (trp_r_khergit_kharvaach, 8, 15)]), 
 ("kingdom_3_reinforcements_e", "kingdom_3_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_r_khergit_lancer, 3, 8), (trp_r_khergit_scout, 10, 15), (trp_r_khergit_morici, 5, 8), (trp_r_khergit_abaci, 8, 12), (trp_r_khergit_skirmisher, 10, 13)]), #
 ("kingdom_3_reinforcements_f", "kingdom_3_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_r_khergit_parthian, 6, 16)]), #
 # GAME_MODE_HARD
 ("kingdom_3_reinforcements_g", "kingdom_3_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_r_khergit_skirmisher, 14, 33), (trp_r_khergit_raider, 12, 15)]), 
 ("kingdom_3_reinforcements_h", "kingdom_3_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_r_khergit_lancer, 8, 15), (trp_r_khergit_parthian, 5, 13)]), 
 ("kingdom_3_reinforcements_i", "kingdom_3_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_r_khergit_skirmisher, 6, 16), (trp_r_khergit_noyan, 1, 3)]), 
 # GAME_MODE_VERY_HARD
 ("kingdom_3_reinforcements_j", "kingdom_3_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_r_khergit_torguu,2,4), (trp_r_khergit_lancer, 6, 16), (trp_r_khergit_skirmisher, 6, 13)]), 
 ("kingdom_3_reinforcements_k", "kingdom_3_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_r_khergit_lancer, 5, 11), (trp_r_khergit_skirmisher, 5, 9), (trp_r_khergit_torguu, 3, 8), (trp_r_khergit_noyan, 1, 3)]), #
 ("kingdom_3_reinforcements_l", "kingdom_3_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_r_khergit_bahatur, 1, 2), (trp_r_khergit_noker, 1, 3), (trp_r_khergit_raider, 15, 25), (trp_r_khergit_parthian, 15, 20)]), 
 
 
 ### NORDS ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_4_reinforcements_a", "kingdom_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_new_nord_farmhand, 8, 18), (trp_new_nord_bowman, 8, 18), (trp_new_nord_spearman, 1, 2), (trp_new_nord_skald, 0, 2), (trp_new_nord_retainer, 0, 1)]),
 ("kingdom_4_reinforcements_b", "kingdom_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_new_nord_bowman, 2, 5), (trp_new_nord_skald, 2, 5), (trp_new_nord_retainer, 6, 7), (trp_new_nord_spearman, 7, 12), (trp_new_nord_tracker, 0, 4)],),
 ("kingdom_4_reinforcements_c", "kingdom_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_new_nord_retainer, 2, 6), (trp_new_nord_spearman, 2, 10), (trp_new_nord_skirmisher, 3, 8), (trp_new_nord_tracker, 1, 3), (trp_new_nord_berserker, 0, 3)]),
 # GAME_MODE_NORMAL
 ("kingdom_4_reinforcements_d", "kingdom_4_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_new_nord_farmhand, 4, 8), (trp_new_nord_bowman, 4, 12), (trp_new_nord_spearman, 4, 5), (trp_new_nord_retainer, 1, 2), (trp_new_nord_skirmisher, 5, 10)]),
 ("kingdom_4_reinforcements_e", "kingdom_4_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_new_nord_retainer, 2, 6), (trp_new_nord_spearman, 4, 7), (trp_new_nord_skirmisher, 5, 13), (trp_new_nord_berserker, 0, 3), (trp_new_nord_tracker, 0, 5)]),
 ("kingdom_4_reinforcements_f", "kingdom_4_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_new_nord_berserker, 2, 6), (trp_new_nord_sharpshooter, 2, 8), (trp_new_nord_godi,2,3), (trp_new_nord_hirdman, 0, 1)],),
 # GAME_MODE_HARD
 ("kingdom_4_reinforcements_g", "kingdom_4_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_new_nord_spearman, 7, 12), (trp_new_nord_skald, 4, 5), (trp_new_nord_tracker, 6, 13), (trp_new_nord_skirmisher, 3, 5), (trp_new_nord_retainer, 4, 5)]),
 ("kingdom_4_reinforcements_h", "kingdom_4_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_new_nord_retainer, 3, 7), (trp_new_nord_spearman, 2, 3), (trp_new_nord_skirmisher, 3, 8), (trp_new_nord_sharpshooter, 5, 10)]),
 ("kingdom_4_reinforcements_i", "kingdom_4_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_new_nord_berserker, 3, 8), (trp_new_nord_hirdman, 0, 1), (trp_new_nord_godi, 0, 2)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_4_reinforcements_j", "kingdom_4_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_new_nord_spearman, 1, 5), (trp_new_nord_skald, 0, 1), (trp_new_nord_tracker, 2, 8), (trp_new_nord_skirmisher, 2, 8), (trp_new_nord_retainer, 4, 5), (trp_new_nord_berserker, 2, 6)]),
 ("kingdom_4_reinforcements_k", "kingdom_4_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_new_nord_retainer, 2, 4), (trp_new_nord_spearman, 0, 3), (trp_new_nord_skirmisher, 3, 8), (trp_new_nord_sharpshooter, 5, 10), (trp_new_nord_berserker, 5 , 8), (trp_new_nord_godi, 1, 2)]),
 ("kingdom_4_reinforcements_l", "kingdom_4_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_new_nord_berserker, 4, 6), (trp_new_nord_hirdman, 1, 3), (trp_new_nord_godi, 1, 3), (trp_new_nord_sharpshooter, 4, 8)]),
 
 
 ### RHODOKS ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_5_reinforcements_a", "kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_rhodok_militia,8,18),(trp_rhodok_trained_militia,8,18),(trp_rhodok_trained_militia,3,7)]),
 ("kingdom_5_reinforcements_b", "kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_rhodok_trained_militia,8,15),(trp_rhodok_crossbowman,6,13)]),
 ("kingdom_5_reinforcements_c", "kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_rhodok_pikeman,3,8),(trp_rhodok_crossbowman_2,3,8),(trp_rhodok_arbalestier,2,5)]),
 # GAME_MODE_NORMAL
 ("kingdom_5_reinforcements_d", "kingdom_5_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_rhodok_militia,6,13),(trp_rhodok_trained_militia,4,11),(trp_rhodok_crossbowman,7,12)]),
 ("kingdom_5_reinforcements_e", "kingdom_5_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_rhodok_pikeman,8,15),(trp_rhodok_crossbowman_2,2,8),(trp_rhodok_arbalestier,4,10)]),
 ("kingdom_5_reinforcements_f", "kingdom_5_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_rhodok_pikeman_2,3,8),(trp_rhodok_arbalestier,3,8),(trp_rhodok_siege_commander,1,3),(trp_rhodok_mercenary_captain,0,2)]),
 # GAME_MODE_HARD
 ("kingdom_5_reinforcements_g", "kingdom_5_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_rhodok_trained_militia,8,20),(trp_rhodok_crossbowman,6,13)]),
 ("kingdom_5_reinforcements_h", "kingdom_5_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_rhodok_pikeman,7,15),(trp_rhodok_crossbowman_2,6,13),(trp_rhodok_arbalestier,4,10),(trp_rhodok_highland_pikeman,2,6)]),
 ("kingdom_5_reinforcements_i", "kingdom_5_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_rhodok_pikeman_2,3,8),(trp_rhodok_arbalestier,3,8),(trp_rhodok_hedge_knight,1,4),(trp_rhodok_siege_commander,1,2),(trp_rhodok_mercenary_captain,1,1)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_5_reinforcements_j", "kingdom_5_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_rhodok_crossbowman,2,4),(trp_rhodok_pikeman,6,15),(trp_rhodok_crossbowman_2,6,14)]),
 ("kingdom_5_reinforcements_k", "kingdom_5_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_rhodok_pikeman,5,11),(trp_rhodok_crossbowman_2,2,5),(trp_rhodok_pikeman_2,3,8),(trp_rhodok_arbalestier,4,10),(trp_rhodok_siege_commander,2,5)]),
 ("kingdom_5_reinforcements_l", "kingdom_5_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_rhodok_arbalestier,3,8),(trp_rhodok_hedge_knight,1,4),(trp_rhodok_siege_commander,1,3),(trp_rhodok_mercenary_captain,1,3),(trp_rhodok_siege_breaker,1,4)]),
 
 
 ### SARRANID ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_6_reinforcements_a", "kingdom_6_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_r_sarranid_azab, 12, 18), (trp_r_sarranid_yaya, 5, 12), (trp_r_sarranid_janissary, 3, 5)]),
 ("kingdom_6_reinforcements_b", "kingdom_6_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_r_sarranid_corbaci, 1, 4), (trp_r_sarranid_musellem, 4, 5), (trp_r_sarranid_janissary, 4, 8), (trp_r_sarranid_timariot, 2, 5)]),
 ("kingdom_6_reinforcements_c", "kingdom_6_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_r_sarranid_boluk_bashi,1,4),(trp_r_sarranid_timariot,5,8),(trp_r_sarranid_musellem,4,5),(trp_r_sarranid_sipahi,0,2)]),
 # GAME_MODE_NORMAL
 ("kingdom_6_reinforcements_d", "kingdom_6_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_r_sarranid_azab, 2, 5), (trp_r_sarranid_yaya, 6, 14), (trp_r_sarranid_janissary, 5, 12)]),
 ("kingdom_6_reinforcements_e", "kingdom_6_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_r_sarranid_corbaci, 2, 5), (trp_r_sarranid_musellem, 4, 5), (trp_r_sarranid_janissary, 4, 8), (trp_r_sarranid_timariot, 3, 7), (trp_r_sarranid_bashibozuk, 2, 6)]),
 ("kingdom_6_reinforcements_f", "kingdom_6_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_r_sarranid_boluk_bashi, 3, 6), (trp_r_sarranid_timariot, 8, 12), (trp_r_sarranid_musellem, 4, 8), (trp_r_sarranid_sipahi, 1, 4), (trp_r_sarranid_garip, 1, 2)]),
 # GAME_MODE_HARD
 ("kingdom_6_reinforcements_g", "kingdom_6_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_r_sarranid_azab, 2, 5), (trp_r_sarranid_yaya, 2, 8), (trp_r_sarranid_janissary, 7, 18)]),
 ("kingdom_6_reinforcements_h", "kingdom_6_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_r_sarranid_corbaci, 3, 8), (trp_r_sarranid_musellem, 2, 4), (trp_r_sarranid_janissary, 2, 6), (trp_r_sarranid_timariot, 5, 10), (trp_r_sarranid_bashibozuk, 4, 8), (trp_r_sarranid_sipahi, 3,5)]),
 ("kingdom_6_reinforcements_i", "kingdom_6_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_r_sarranid_boluk_bashi, 3, 6), (trp_r_sarranid_timariot, 2, 4), (trp_r_sarranid_musellem, 2, 4), (trp_r_sarranid_sipahi, 3, 6), (trp_r_sarranid_garip, 2, 4)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_6_reinforcements_j", "kingdom_6_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_r_sarranid_azab, 1, 4), (trp_r_sarranid_yaya, 2, 8), (trp_r_sarranid_janissary, 12, 24)]),
 ("kingdom_6_reinforcements_k", "kingdom_6_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_r_sarranid_corbaci, 6, 10), (trp_r_sarranid_musellem, 2, 4), (trp_r_sarranid_janissary, 2, 6), (trp_r_sarranid_timariot, 3, 5), (trp_r_sarranid_bashibozuk, 6, 10), (trp_r_sarranid_sipahi, 3,8)]),
 ("kingdom_6_reinforcements_l", "kingdom_6_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_r_sarranid_boluk_bashi, 5, 10), (trp_r_sarranid_timariot, 2, 4), (trp_r_sarranid_musellem, 2, 4), (trp_r_sarranid_sipahi, 8, 10), (trp_r_sarranid_garip, 2, 10)]),
 ## LEIFDIN--

  ("steppe_bandit_lair" ,"Steppe Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_steppe_bandit,15,58)]),
  ("taiga_bandit_lair","Tundra Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_taiga_bandit,15,58)]),
  ("desert_bandit_lair" ,"Desert Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_desert_bandit,15,58)]),
  ("forest_bandit_lair" ,"Forest Bandit Camp",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_forest_bandit,15,58)]),
  ("mountain_bandit_lair" ,"Mountain Bandit Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_mountain_bandit,15,58)]),
  ("sea_raider_lair","Sea Raider Landing",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_sea_raider,15,50)]),
  ("looter_lair","Kidnappers' Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_looter,15,25)]),
  
  ("bandit_lair_templates_end","{!}bandit_lair_templates_end",icon_axeman|carries_goods(2)|pf_is_static,0,fac_outlaws,bandit_personality,[(trp_sea_raider,15,50)]),

  ("leaded_looters","Band of robbers",icon_axeman|carries_goods(8)|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_looter_leader,1,1),(trp_looter,3,3)]),
  
  ("troop_testing_party_1", "Troop Testing Party", icon_axeman|pf_is_static, 0, fac_outlaws, troop_testers, [(trp_looter, 1, 1)]),
  ("troop_testing_party_2", "Troop Testing Party", icon_axeman|pf_is_static, 0, fac_outlaws, troop_testers, [(trp_looter, 1, 1)]),
  ("troop_testing_party_3", "Troop Testing Party", icon_axeman|pf_is_static, 0, fac_outlaws, troop_testers, [(trp_looter, 1, 1)]),
]
