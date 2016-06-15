# Quest Pack 3 (1.0) by Windyplains

from module_constants import *

# Overwritten Slots
slot_quest_current_tally                        = slot_quest_stage_1_trigger_chance
slot_quest_merc_leader_title                    = slot_quest_stage_2_trigger_chance
slot_quest_merc_band_name                       = slot_quest_stage_3_trigger_chance
slot_quest_merc_band_ideal_size                 = slot_quest_stage_4_trigger_chance
slot_quest_merc_contract_debt                   = slot_quest_stage_5_trigger_chance
slot_quest_merc_culture                         = slot_quest_stage_6_trigger_chance
slot_quest_town_radius                          = slot_quest_stage_7_trigger_chance

# General constants
qp3_quests_begin                                = "qst_summoned_to_hall"
qp3_quests_end                                  = "qst_quest_pack_3_end"

qp3_actor_minister                              = "trp_qp3_steward" # seneshal?
qp3_actor_messenger                             = "trp_qp3_messenger"
qp3_actor_mercenary_leader                      = "trp_qp3_mercenary_leader" # Should be a hero troop.

# Mercenary troops
# qp3_merc_tier_1                                 = "trp_swadian_recruit"
# qp3_merc_tier_2                                 = "trp_swadian_militia"
# qp3_merc_tier_3                                 = "trp_swadian_footman"
# qp3_merc_tier_4                                 = "trp_swadian_infantry"
# qp3_merc_tier_5                                 = "trp_swadian_sergeant"

# Functions of script_qp3_mercenary_function
mercs_generate_party          = 0
mercs_upgrade_troops          = 1
mercs_recruit_troops          = 2
mercs_generate_contract_cost  = 3
mercs_set_behavior_to_follow  = 4
mercs_destroy_party           = 5
mercs_remove_non_mercenaries  = 6
mercs_contract_renew          = 7
mercs_contract_end            = 8
mercs_payment_due             = 9
mercs_join_combat             = 10
mercs_sell_prisoners          = 11

# For testing purposes only.
#Starting Faction Options
start_fac_random   = 0
start_fac_swadia   = 1
start_fac_nords    = 2
start_fac_rhodoks  = 3
start_fac_khergits = 4
start_fac_sarrind  = 5
start_fac_vaegirs  = 6
wp_start_fac_end   = 7    # Update this to be your last starting faction.
wp_start_fac_begin = 0

########################################################################################################################################################
####################                                             COMMON NOBILITY QUESTS                                             ####################
########################################################################################################################################################
###########################################################
# QUEST: summoned_to_hall                                 #
###########################################################
# Active states
qp3_summoned_inactive                           = 0
qp3_summoned_summoned_to_fief                   = 1
qp3_summoned_problem_explained                  = 2

###########################################################
# QUEST: patrol_for_bandits                               #
###########################################################
# Active states
qp3_patrol_bandits_inactive                     = 0
qp3_patrol_bandits_begun                        = 1
qp3_patrol_bandits_complete                     = 2
# General Parameters
# qp3_bandits_begin                               = "trp_bandit_n_looter"    # Floris
# qp3_bandits_end                                 = "trp_bandit_e_manhunter" # Floris
# qp3_bandits_template                            = "pt_looters"             # Floris
qp3_bandits_begin                               = "trp_looter"               # Native
qp3_bandits_end                                 = "trp_manhunter"            # Native
qp3_bandits_template                            = "pt_looters"               # Native

###########################################################
# QUEST: mercs_for_hire                                   #
###########################################################
# Active states
qp3_mercs_for_hire_inactive                     = 0
qp3_mercs_for_hire_begun                        = 1
qp3_mercs_for_hire_active_contract              = 2 # Decision made to reject or accept.
qp3_mercs_for_hire_contract_due                 = 3 # Triggers map conversation with leader.  Depending on decision stage continues to 4 or 5.
qp3_mercs_for_hire_agree_to_renew               = 4 # When contract expires the stage is reset to 2 & duration refreshed.
qp3_mercs_for_hire_refused_to_renew             = 5 # When contract expires the stage is continued to 6.
qp3_mercs_for_hire_contract_ended               = 6 # Mercenary party leaves.

###########################################################
# QUEST: destroy_the_lair                                 #
###########################################################
# Active states
qp3_destroy_the_lair_inactive                   = 0
qp3_destroy_the_lair_begun                      = 1
qp3_destroy_the_lair_found_it                   = 2
qp3_destroy_the_lair_end                        = 3

###########################################################
# QUEST: escort_to_mine                                   #
###########################################################
# Active states
qp3_escort_to_mine_inactive                     = 0
qp3_escort_to_mine_begun                        = 1
qp3_escort_to_mine_slaves_delivered             = 2
qp3_escort_to_mine_money_returned               = 3
qp3_escort_to_mine_slaves_lost                  = 4

###########################################################
# QUEST: spy_revealed                                     #
###########################################################
# Active states
qp3_spy_revealed_inactive                       = 0 # Quest isn't active.
qp3_spy_revealed_begun                          = 1 # You've learned of the spy within your halls.
qp3_spy_revealed_decision_made                  = 2 # You've decided to either execute, imprison or release the spy.
qp3_spy_revealed_sent_companion                 = 3 # You sent a companion to pretend to be the spy and setup a false meeting. (12 hour wait)
qp3_spy_revealed_companion_successful           = 4 # Your companion was successful.
qp3_spy_revealed_companion_failed               = 5 # Your companion failed and barely makes it back alive. (Quest Fail)
qp3_spy_revealed_house_fight_begun              = 6 # The trap is set and you've cornered the spies in a house.
qp3_spy_revealed_house_fight_success            = 7 # The spies have all been caught. (Quest Success)
qp3_spy_revealed_house_fight_failed             = 8 # The spies have won and escaped. (Quest Fail)
qp3_spy_revealed_broken_chain                   = 9 # Some decision to not continue was made. (Quest Cancel)

### Encounter Scene Ideas ###
# forest campsite
# inside of a cave
# a road passing through fields
# a road passing through forest
# a small pond area.
# a small farm with a house


