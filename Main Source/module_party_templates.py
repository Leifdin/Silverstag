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


 ## LEIFDIN+ ## - Added reinforcement templates for player's culture.
 ### PLAYER CUSTOM CULTURE ###
 # Following data is per script "cf_reinforce_party".
 # Reinforcement A gets added to centres only
 # Reinforcement B gets added to kingdom_parties (50%) and centers (50%).
 # Reinforcement C gets added to kingdom_parties only .
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
 ("kingdom_1_reinforcements_a", "kingdom_1_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_new_swadian_farmer, 11, 11), (trp_new_swadian_hunter, 11, 11), (trp_new_swadian_militia, 3, 3), (trp_new_swadian_supplyman, 1, 1), (trp_new_swadian_footman, 2, 2), (trp_new_swadian_crossbowman, 2, 2)]),
 ("kingdom_1_reinforcements_b", "kingdom_1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_new_swadian_farmer, 9, 9), (trp_new_swadian_hunter, 9, 9), (trp_new_swadian_supplyman, 1, 1), (trp_new_swadian_footman, 4, 4), (trp_new_swadian_lancer, 4, 4), (trp_new_swadian_man_at_arms, 3, 3)]),
 ("kingdom_1_reinforcements_c", "kingdom_1_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_new_swadian_hunter, 10, 10), (trp_new_swadian_footman, 5, 5), (trp_new_swadian_militia, 5, 5), (trp_new_swadian_lancer, 5, 5), (trp_new_swadian_man_at_arms, 4, 4), (trp_new_swadian_sharpshooter, 1, 1)]),
 # GAME_MODE_NORMAL
 ("kingdom_1_reinforcements_d", "kingdom_1_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_new_swadian_farmer, 6, 6), (trp_new_swadian_hunter, 6, 6), (trp_new_swadian_militia, 7, 7), (trp_new_swadian_supplyman, 2, 2), (trp_new_swadian_footman, 7, 7), (trp_new_swadian_crossbowman, 4, 4) ]), ## 30 troops
 ("kingdom_1_reinforcements_e", "kingdom_1_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_new_swadian_farmer, 4, 4), (trp_new_swadian_crossbowman, 5, 5), (trp_new_swadian_supplyman, 1, 1), (trp_new_swadian_man_at_arms, 5, 5), (trp_new_swadian_lancer, 5, 5), (trp_new_swadian_man_at_arms, 5, 5)],), ## 30 troops
 ("kingdom_1_reinforcements_f", "kingdom_1_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_new_swadian_footman, 3, 3), (trp_new_swadian_crossbowman, 9, 9), (trp_new_swadian_militia, 5, 5), (trp_new_swadian_man_at_arms, 5, 5), (trp_new_swadian_lancer, 5, 5), (trp_new_swadian_sharpshooter, 3, 3)]), ## 30 troops
  # GAME_MODE_HARD
 ("kingdom_1_reinforcements_g", "kingdom_1_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_new_swadian_militia, 8, 8), (trp_new_swadian_supplyman, 2, 2), (trp_new_swadian_footman, 8, 8), (trp_new_swadian_sharpshooter, 8, 8), (trp_new_swadian_crossbowman, 6, 6)]), ## 30 troops
 ("kingdom_1_reinforcements_h", "kingdom_1_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_new_swadian_supplyman, 1, 1), (trp_new_swadian_footman, 7, 7), (trp_new_swadian_man_at_arms, 7, 7), (trp_new_swadian_lancer, 7, 7), (trp_new_swadian_billman, 4, 4), (trp_new_swadian_sharpshooter, 4, 4) ],), ## 30 troops
 ("kingdom_1_reinforcements_i", "kingdom_1_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_new_swadian_sentinel, 2, 2), (trp_new_swadian_billman, 2, 2), (trp_new_swadian_man_at_arms, 8, 8), (trp_new_swadian_lancer, 8, 8), (trp_new_swadian_knight, 2, 2), (trp_new_swadian_sharpshooter, 8, 8)]), ## 30 troops
 # GAME_MODE_VERY_HARD
 ("kingdom_1_reinforcements_j", "kingdom_1_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_new_swadian_crossbowman, 5, 5), (trp_new_swadian_supplyman, 2, 2), (trp_new_swadian_footman, 5, 5), (trp_new_swadian_sharpshooter, 8, 8), (trp_new_swadian_sentinel, 5, 5), (trp_new_swadian_sargeant, 5, 5)]), ## 30 troops
 ("kingdom_1_reinforcements_k", "kingdom_1_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_new_swadian_supplyman, 1, 1), (trp_new_swadian_footman, 3, 3), (trp_new_swadian_crossbowman, 3, 3), (trp_new_swadian_sentinel, 4, 4), (trp_new_swadian_sharpshooter, 10, 10), (trp_new_swadian_sargeant, 9, 9) ],), ## 30 troops
 ("kingdom_1_reinforcements_l", "kingdom_1_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_new_swadian_sentinel, 2, 2), (trp_new_swadian_billman, 1, 1), (trp_new_swadian_man_at_arms, 10, 10), (trp_new_swadian_lancer, 10, 10), (trp_new_swadian_knight, 4, 4), (trp_new_swadian_sargeant, 3, 3)]), ## 30 troops
 
 
 ### VAEGIRS ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_2_reinforcements_a", "kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_new_vaegir_peasant, 11, 11), (trp_new_vaegir_bowman, 11, 11), (trp_new_vaegir_militia, 3, 3), (trp_new_vaegir_retainer, 1, 1), (trp_new_vaegir_outrider, 2, 2), (trp_new_vaegir_longbowman, 2, 2)]),
 ("kingdom_2_reinforcements_b", "kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_new_vaegir_peasant, 9, 9), (trp_new_vaegir_bowman, 9, 9), (trp_new_vaegir_skirmisher, 1, 1), (trp_new_vaegir_spearman, 4, 4), (trp_new_vaegir_retainer, 4, 4), (trp_new_vaegir_outrider, 3, 3)]),
 ("kingdom_2_reinforcements_c", "kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_new_vaegir_bowman, 10, 10), (trp_new_vaegir_militia, 5, 5), (trp_new_vaegir_outrider, 5, 5), (trp_new_vaegir_retainer, 5, 5), (trp_new_vaegir_skirmisher, 4, 4), (trp_new_vaegir_longbowman, 1, 1)]),
 # GAME_MODE_NORMAL
 ("kingdom_2_reinforcements_d", "kingdom_2_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_new_vaegir_peasant, 6, 6), (trp_new_vaegir_bowman, 6, 6), (trp_new_vaegir_militia, 7, 7), (trp_new_vaegir_skirmisher, 2, 2), (trp_new_vaegir_retainer, 7, 7), (trp_new_vaegir_outrider, 4, 4) ]), ## 30 troops
 ("kingdom_2_reinforcements_e", "kingdom_2_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_new_vaegir_peasant, 4, 4), (trp_new_vaegir_longbowman, 5, 5), (trp_new_vaegir_sentry, 1, 1), (trp_new_vaegir_retainer, 5, 5), (trp_new_vaegir_skirmisher, 5, 5), (trp_new_vaegir_outrider, 5, 5)],), ## 30 troops
 ("kingdom_2_reinforcements_f", "kingdom_2_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_new_vaegir_militia, 3, 3), (trp_new_vaegir_longbowman, 9, 9), (trp_new_vaegir_retainer, 11, 11), (trp_new_vaegir_outrider, 3, 3), (trp_new_vaegir_skirmisher, 3, 3), (trp_new_vaegir_knight, 1, 1)]), ## 30 troops
  # GAME_MODE_HARD
 ("kingdom_2_reinforcements_g", "kingdom_2_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_new_vaegir_militia, 8, 8), (trp_new_vaegir_sentry, 2, 2), (trp_new_vaegir_longbowman, 8, 8), (trp_new_vaegir_retainer, 8, 8), (trp_new_vaegir_skirmisher, 6, 6)]), ## 30 troops
 ("kingdom_2_reinforcements_h", "kingdom_2_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_new_vaegir_outrider, 4, 4), (trp_new_vaegir_militia, 4, 4), (trp_new_vaegir_retainer, 7, 7), (trp_new_vaegir_skirmisher, 7, 7), (trp_new_vaegir_longbowman, 4, 4), (trp_new_vaegir_druzhina, 4, 4) ],), ## 30 troops
 ("kingdom_2_reinforcements_i", "kingdom_2_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_new_vaegir_sentry, 5, 5), (trp_new_vaegir_knight, 2, 2), (trp_new_vaegir_retainer, 8, 8), (trp_new_vaegir_skirmisher, 8, 8), (trp_new_vaegir_druzhina, 2, 2), (trp_new_vaegir_marksman, 5, 5)]), ## 30 troops
 # GAME_MODE_VERY_HARD
 ("kingdom_2_reinforcements_j", "kingdom_2_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_new_vaegir_longbowman, 5, 5), (trp_new_vaegir_outrider, 2, 2), (trp_new_vaegir_militia, 5, 5), (trp_new_vaegir_marksman, 8, 8), (trp_new_vaegir_sentry, 5, 5), (trp_new_vaegir_druzhina, 5, 5)]), ## 30 troops
 ("kingdom_2_reinforcements_k", "kingdom_2_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_new_vaegir_outrider, 4, 4), (trp_new_vaegir_militia, 3, 3), (trp_new_vaegir_longbowman, 3, 3), (trp_new_vaegir_sentry, 4, 4), (trp_new_vaegir_marksman, 7, 7), (trp_new_vaegir_skirmisher, 9, 9) ],), ## 30 troops
 ("kingdom_2_reinforcements_l", "kingdom_2_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_new_vaegir_retainer, 2, 2), (trp_new_vaegir_retainer, 10, 10), (trp_new_vaegir_skirmisher, 10, 10), (trp_new_vaegir_knight, 4, 4), (trp_new_vaegir_druzhina, 4, 4)]), ## 30 troops
 

 ### KHERGITS ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_3_reinforcements_a", "kingdom_3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_new_khergit_bowman, 11, 11), (trp_new_khergit_outcast, 11, 11), (trp_new_khergit_scout, 3, 3), (trp_new_khergit_hunter, 3, 3), (trp_new_khergit_master_bowman, 2, 2)]),
 ("kingdom_3_reinforcements_b", "kingdom_3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_new_khergit_bowman, 9, 9), (trp_new_khergit_outcast, 9, 9), (trp_new_khergit_clansman, 4, 4), (trp_new_khergit_hunter, 5, 5), (trp_new_khergit_master_bowman, 3, 3)]),
 ("kingdom_3_reinforcements_c", "kingdom_3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_new_khergit_outcast, 10, 10), (trp_new_khergit_scout, 5, 5), (trp_new_khergit_hunter, 5, 5), (trp_new_khergit_clansman, 5, 5), (trp_new_khergit_raider, 4, 4), (trp_new_khergit_lancer, 1, 1)]),
 # GAME_MODE_NORMAL
 ("kingdom_3_reinforcements_d", "kingdom_3_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_new_khergit_bowman, 6, 6), (trp_new_khergit_outcast, 6, 6), (trp_new_khergit_scout, 7, 7), (trp_new_khergit_hunter, 2, 2), (trp_new_khergit_clansman, 7, 7), (trp_new_khergit_master_bowman, 4, 4) ]), ## 30 troops
 ("kingdom_3_reinforcements_e", "kingdom_2_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_new_khergit_bowman, 4, 4), (trp_new_khergit_clansman, 5, 5), (trp_new_khergit_skirmisher, 1, 1), (trp_new_khergit_hunter, 5, 5), (trp_new_khergit_scout, 5, 5), (trp_new_khergit_outcast, 5, 5)],), ## 30 troops
 ("kingdom_3_reinforcements_f", "kingdom_2_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_new_khergit_outcast, 3, 3), (trp_new_khergit_master_bowman, 9, 9), (trp_new_khergit_scout, 11, 11), (trp_new_khergit_raider, 3, 3), (trp_new_khergit_hunter, 3, 3), (trp_new_khergit_skirmisher, 1, 1)]), ## 30 troops
  # GAME_MODE_HARD
 ("kingdom_3_reinforcements_g", "kingdom_3_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_new_khergit_outcast, 8, 8), (trp_new_khergit_guard, 2, 2), (trp_new_khergit_master_bowman, 8, 8), (trp_new_khergit_scout, 8, 8), (trp_new_khergit_raider, 6, 6)]), ## 30 troops
 ("kingdom_3_reinforcements_h", "kingdom_3_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_new_khergit_hunter, 4, 4), (trp_new_khergit_clansman, 4, 4), (trp_new_khergit_scout, 7, 7), (trp_new_khergit_lancer, 7, 7), (trp_new_khergit_master_bowman, 4, 4), (trp_new_khergit_skirmisher, 4, 4) ],), ## 30 troops
 ("kingdom_3_reinforcements_i", "kingdom_3_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_new_khergit_guard, 5, 5), (trp_new_khergit_lancer, 2, 2), (trp_new_khergit_scout, 8, 8), (trp_new_khergit_raider, 8, 8), (trp_new_khergit_master_bowman, 2, 2), (trp_new_khergit_skirmisher, 5, 5)]), ## 30 troops
 # GAME_MODE_VERY_HARD
 ("kingdom_3_reinforcements_j", "kingdom_3_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_new_khergit_master_bowman, 5, 5), (trp_new_khergit_guard, 2, 2), (trp_new_khergit_scout, 5, 5), (trp_new_khergit_clansman, 8, 8), (trp_new_khergit_lancer, 5, 5), (trp_new_khergit_skirmisher, 5, 5)]), ## 30 troops
 ("kingdom_3_reinforcements_k", "kingdom_3_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_new_khergit_scout, 4, 4), (trp_new_khergit_hunter, 3, 3), (trp_new_khergit_lancer, 3, 3), (trp_new_khergit_guard, 4, 4), (trp_new_khergit_skirmisher, 7, 7), (trp_new_khergit_master_bowman, 9, 9) ],), ## 30 troops
 ("kingdom_3_reinforcements_l", "kingdom_3_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_new_khergit_scout, 2, 2), (trp_new_khergit_raider, 10, 10), (trp_new_khergit_skirmisher, 10, 10), (trp_new_khergit_lancer, 4, 4), (trp_new_khergit_guard, 4, 4)]), ## 30 troops
 
 
 ### NORDS ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_4_reinforcements_a", "kingdom_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_new_nord_farmhand, 11, 11), (trp_new_nord_bowman, 11, 11), (trp_new_nord_spearman, 3, 3), (trp_new_nord_skald, 1, 1), (trp_new_nord_retainer, 2, 2), (trp_new_nord_skirmisher, 2, 2)]), ## 30 troops
 ("kingdom_4_reinforcements_b", "kingdom_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_new_nord_farmhand, 9, 9), (trp_new_nord_bowman, 9, 9), (trp_new_nord_skald, 1, 1), (trp_new_nord_retainer, 4, 4), (trp_new_nord_spearman, 4, 4), (trp_new_nord_tracker, 3, 3)],), ## 30 troops
 ("kingdom_4_reinforcements_c", "kingdom_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_new_nord_bowman, 10, 10), (trp_new_nord_retainer, 5, 5), (trp_new_nord_spearman, 5, 5), (trp_new_nord_skirmisher, 5, 5), (trp_new_nord_tracker, 4, 4), (trp_new_nord_berserker, 1, 1)]), ## 30 troops
 # GAME_MODE_NORMAL
 ("kingdom_4_reinforcements_d", "kingdom_4_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_new_nord_farmhand, 6, 6), (trp_new_nord_bowman, 6, 6), (trp_new_nord_spearman, 7, 7), (trp_new_nord_skald, 2, 2), (trp_new_nord_retainer, 7, 7), (trp_new_nord_skirmisher, 4, 4) ]), ## 30 troops
 ("kingdom_4_reinforcements_e", "kingdom_4_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_new_nord_farmhand, 4, 4), (trp_new_nord_bowman, 5, 5), (trp_new_nord_skald, 1, 1), (trp_new_nord_retainer, 5, 5), (trp_new_nord_spearman, 5, 5), (trp_new_nord_tracker, 5, 5)],), ## 30 troops
 ("kingdom_4_reinforcements_f", "kingdom_4_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_new_nord_bowman, 3, 3), (trp_new_nord_retainer, 9, 9), (trp_new_nord_spearman, 5, 5), (trp_new_nord_skirmisher, 5, 5), (trp_new_nord_tracker, 5, 5), (trp_new_nord_berserker, 3, 3)]), ## 30 troops
 # GAME_MODE_HARD
 ("kingdom_4_reinforcements_g", "kingdom_4_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_new_nord_spearman, 8, 8), (trp_new_nord_skald, 2, 2), (trp_new_nord_retainer, 8, 8), (trp_new_nord_tracker, 8, 8), (trp_new_nord_skirmisher, 6, 6)]), ## 30 troops
 ("kingdom_4_reinforcements_h", "kingdom_4_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_new_nord_skald, 1, 1), (trp_new_nord_retainer, 7, 7), (trp_new_nord_spearman, 7, 7), (trp_new_nord_tracker, 7, 7), (trp_new_nord_berserker, 4, 4), (trp_new_nord_retinue_archer, 4, 4) ],), ## 30 troops
 ("kingdom_4_reinforcements_i", "kingdom_4_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_new_nord_hirdman, 2, 2), (trp_new_nord_godi, 2, 2), (trp_new_nord_skirmisher, 5, 5), (trp_new_nord_tracker, 5, 5), (trp_new_nord_berserker, 8, 8), (trp_new_nord_retinue_archer, 8, 8)]), ## 30 troops
 # GAME_MODE_VERY_HARD
 ("kingdom_4_reinforcements_j", "kingdom_4_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_new_nord_skirmisher, 5, 5), (trp_new_nord_skald, 2, 2), (trp_new_nord_retainer, 5, 5), (trp_new_nord_tracker, 8, 8), (trp_new_nord_berserker, 5, 5), (trp_new_nord_retinue_archer, 5, 5)]), ## 30 troops
 ("kingdom_4_reinforcements_k", "kingdom_4_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_new_nord_skald, 1, 1), (trp_new_nord_retainer, 3, 3), (trp_new_nord_spearman, 3, 3), (trp_new_nord_tracker, 4, 4), (trp_new_nord_berserker, 10, 10), (trp_new_nord_retinue_archer, 9, 9) ],), ## 30 troops
 ("kingdom_4_reinforcements_l", "kingdom_4_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_new_nord_hirdman, 4, 4), (trp_new_nord_godi, 4, 4), (trp_new_nord_skirmisher, 5, 5), (trp_new_nord_tracker, 5, 5), (trp_new_nord_berserker, 6, 6), (trp_new_nord_retinue_archer, 6, 6)]), ## 30 troops
 
 ### RHODOKS ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_5_reinforcements_a", "kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_new_rhodok_militia, 10, 10), (trp_new_rhodok_militia_archer, 10, 10), (trp_new_rhodok_vanguard, 5, 5), (trp_new_rhodok_crossbowman, 5, 5)]), ## 30 troops
 ("kingdom_5_reinforcements_b", "kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_new_rhodok_halberdier, 2, 2), (trp_new_rhodok_vanguard, 8, 8), (trp_new_rhodok_scout, 10, 10), (trp_new_rhodok_militia, 10, 10)],), ## 30 troops
 ("kingdom_5_reinforcements_c", "kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_new_rhodok_captain, 1, 1), (trp_new_rhodok_siege_breaker, 1, 1), (trp_new_rhodok_pikeman, 2, 2), (trp_new_rhodok_footman, 10, 10), (trp_new_rhodok_crossbowman, 6, 6), (trp_new_rhodok_scout, 10, 10)]), ## 30 troops
 # GAME_MODE_NORMAL
 ("kingdom_5_reinforcements_d", "kingdom_5_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_new_rhodok_militia, 6, 6), (trp_new_rhodok_militia_archer, 6, 6), (trp_new_rhodok_vanguard, 9, 9), (trp_new_rhodok_crossbowman, 9, 9)]), ## 30 troops
 ("kingdom_5_reinforcements_e", "kingdom_5_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_new_rhodok_halberdier, 4, 4), (trp_new_rhodok_vanguard, 10, 10), (trp_new_rhodok_scout, 12, 12), (trp_new_rhodok_militia, 5, 5)],), ## 30 troops
 ("kingdom_5_reinforcements_f", "kingdom_5_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_new_rhodok_captain, 2, 2), (trp_new_rhodok_siege_breaker, 2, 2), (trp_new_rhodok_pikeman, 4, 4), (trp_new_rhodok_footman, 5, 5), (trp_new_rhodok_crossbowman, 7, 7), (trp_new_rhodok_scout, 10, 10)]), ## 30 troops
  # GAME_MODE_HARD
 ("kingdom_5_reinforcements_g", "kingdom_5_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_new_rhodok_halberdier, 4, 4), (trp_new_rhodok_siege_breaker, 3, 3), (trp_new_rhodok_vanguard, 11, 11), (trp_new_rhodok_crossbowman, 12, 12)]), ## 30 troops
 ("kingdom_5_reinforcements_h", "kingdom_5_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_new_rhodok_halberdier, 9, 9), (trp_new_rhodok_vanguard, 10, 10), (trp_new_rhodok_scout, 10, 10), (trp_new_rhodok_siege_commander, 2, 2)],), ## 30 troops
 ("kingdom_5_reinforcements_i", "kingdom_5_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_new_rhodok_captain, 3, 3), (trp_new_rhodok_siege_breaker, 3, 3), (trp_new_rhodok_pikeman, 10, 10), (trp_new_rhodok_crossbowman, 9, 9), (trp_new_rhodok_hedge_knight, 2, 2), (trp_new_rhodok_siege_breaker, 3, 3)]), ## 30 troops
 # GAME_MODE_VERY_HARD
 ("kingdom_5_reinforcements_j", "kingdom_5_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_new_rhodok_halberdier, 6, 6), (trp_new_rhodok_siege_breaker, 5, 5), (trp_new_rhodok_vanguard, 9, 9), (trp_new_rhodok_crossbowman, 12, 12)]), ## 30 troops
 ("kingdom_5_reinforcements_k", "kingdom_5_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_new_rhodok_halberdier, 9, 9), (trp_new_rhodok_vanguard, 10, 10), (trp_new_rhodok_scout, 7, 7), (trp_new_rhodok_siege_commander, 3, 3), (trp_new_rhodok_hedge_knight, 1, 1), (trp_new_rhodok_captain, 1, 1)],), ## 30 troops
 ("kingdom_5_reinforcements_l", "kingdom_5_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_new_rhodok_captain, 4, 4), (trp_new_rhodok_siege_breaker, 4, 4), (trp_new_rhodok_pikeman, 10, 10), (trp_new_rhodok_crossbowman, 5, 5), (trp_new_rhodok_hedge_knight, 3, 3), (trp_new_rhodok_siege_breaker, 4, 4)]), ## 30 troops
 
 
 ### SARRANID ### - NEW TROOPS
 # GAME_MODE_EASY
 ("kingdom_6_reinforcements_a", "kingdom_6_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_new_sarranid_slave, 10, 10), (trp_new_sarranid_swordsman, 10, 10), (trp_new_sarranid_spearman, 10, 10)]),
 ("kingdom_6_reinforcements_b", "kingdom_6_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_new_sarranid_bowman, 25, 25), (trp_new_sarranid_skirmisher, 5, 5)]),
 ("kingdom_6_reinforcements_c", "kingdom_6_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_new_sarranid_raider, 10, 10), (trp_new_sarranid_horseman, 2, 2), (trp_new_sarranid_manhunter, 16, 16), (trp_new_sarranid_lancer, 2, 2)]),
 # GAME_MODE_NORMAL
 ("kingdom_6_reinforcements_d", "kingdom_6_reinforcements_d", 0, 0, fac_commoners, 0, [(trp_new_sarranid_slave, 7, 7), (trp_new_sarranid_swordsman, 13, 13), (trp_new_sarranid_spearman, 8, 8), (trp_new_sarranid_guard, 2, 2)]),
 ("kingdom_6_reinforcements_e", "kingdom_6_reinforcements_e", 0, 0, fac_commoners, 0, [(trp_new_sarranid_bowman, 21, 21), (trp_new_sarranid_skirmisher, 9, 9)]),
 ("kingdom_6_reinforcements_f", "kingdom_6_reinforcements_f", 0, 0, fac_commoners, 0, [(trp_new_sarranid_raider, 7, 7), (trp_new_sarranid_horseman, 4, 4), (trp_new_sarranid_sipahi, 1, 1), (trp_new_sarranid_manhunter, 13, 13), (trp_new_sarranid_lancer, 4, 4), (trp_new_sarranid_mamluke, 1, 1)]),
 # GAME_MODE_HARD
 ("kingdom_6_reinforcements_g", "kingdom_6_reinforcements_g", 0, 0, fac_commoners, 0, [(trp_new_sarranid_swordsman, 18, 18), (trp_new_sarranid_spearman, 5, 5), (trp_new_sarranid_guard, 7, 7)]),
 ("kingdom_6_reinforcements_h", "kingdom_6_reinforcements_h", 0, 0, fac_commoners, 0, [(trp_new_sarranid_bowman, 17, 17), (trp_new_sarranid_skirmisher, 13, 13)]),
 ("kingdom_6_reinforcements_i", "kingdom_6_reinforcements_i", 0, 0, fac_commoners, 0, [(trp_new_sarranid_raider, 3, 3), (trp_new_sarranid_horseman, 7, 7), (trp_new_sarranid_sipahi, 2, 2), (trp_new_sarranid_manhunter, 10, 10), (trp_new_sarranid_lancer, 6, 6), (trp_new_sarranid_mamluke, 2, 2)]),
 # GAME_MODE_VERY_HARD
 ("kingdom_6_reinforcements_j", "kingdom_6_reinforcements_j", 0, 0, fac_commoners, 0, [(trp_new_sarranid_swordsman, 18, 18), (trp_new_sarranid_guard, 13, 13)]),
 ("kingdom_6_reinforcements_k", "kingdom_6_reinforcements_k", 0, 0, fac_commoners, 0, [(trp_new_sarranid_bowman, 12, 12), (trp_new_sarranid_skirmisher, 18, 18)]),
 ("kingdom_6_reinforcements_l", "kingdom_6_reinforcements_l", 0, 0, fac_commoners, 0, [(trp_new_sarranid_horseman, 9, 9), (trp_new_sarranid_sipahi, 3, 3), (trp_new_sarranid_manhunter, 6, 6), (trp_new_sarranid_lancer, 8, 8), (trp_new_sarranid_mamluke, 4, 4)]),
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
  
  ("troop_testing_party_1", "Troop Testing Party", icon_axeman|pf_is_static, 0, fac_outlaws, troop_testers, [(trp_new_nord_berserker, 50, 50)]),
  ("troop_testing_party_2", "Troop Testing Party", icon_axeman|pf_is_static, 0, fac_outlaws, troop_testers, [(trp_new_swadian_knight, 75, 75)]),
  ("troop_testing_party_3", "Troop Testing Party", icon_axeman|pf_is_static, 0, fac_outlaws, troop_testers, [(trp_looter, 1, 1)]),
]
