# Quest Pack 4 (1.0) by Windyplains

from module_constants import *

# OPTIONS TO ADD
# Checkbox - Disable automatic quest triggers
# Menu -     Quest Reaction Level

# General constants
qp4_quests_begin                                = "qst_odval_intro"
qp4_quests_end                                  = "qst_quest_pack_4_end"
qp4_companion_subquest_low_xp_reward            = 1200  # x3 = 3600
qp4_companion_subquest_med_xp_reward            = 1150  # x3 = 3450
qp4_companion_subquest_high_xp_reward           = 1150  # x3 = 3450
qp4_companion_subquest_low_relation_reward      = 6     # x3 = +18
qp4_companion_subquest_med_relation_reward      = 5     # x3 = +15
qp4_companion_subquest_high_relation_reward     = 4     # x3 = +12

# Companion Definitions
NPC_Odval                                       = "trp_npc17" # "trp_npc19" # Nissa
NPC_Edwyn                                       = "trp_npc2" # "trp_npc22" # Marnid

# Actors
qp4_actor_townsfolk                             = "trp_r_khergit_skirmisher"#"trp_khergit_skirmisher" # "trp_khergit_n_tariachin"  # Odval's Story
qp4_actor_knight                                = "trp_hired_blade" # "trp_mercenary_e_komtur_ritter"     # Edwyn's Story
qp4_actor_knight_support                        = "trp_mercenary_swordsman" # "trp_mercenary_e_ritter"    # Edwyn's Story
qp4_actor_named_knight                          = "trp_qp4_actor_knight"   # Edwyn's Story

########################################################################################################################################################
####################                                                ODVAL STORY LINE                                                ####################
########################################################################################################################################################
# General constants
qp4_odval_home_town                             = "p_village_88" # Tulbuk
qp4_odval_storyarc_enabled                      = 1              # This is a general on/off switch for the story quests related to Nissa.

###########################################################
# QUEST: Odval_intro                                      #
###########################################################
# Active states
qp4_odval_intro_inactive                        = 0
qp4_odval_intro_story_heard                     = 1
qp4_odval_intro_agreed_to_help                  = 2
qp4_odval_intro_refused_to_help                 = 3

###########################################################
# QUEST: Odval_redemption                                 #
###########################################################
# Active states
qp4_odval_redemption_inactive                   = 0
qp4_odval_redemption_return_to_tulbuk_done      = 1
qp4_odval_redemption_accept_the_challenge_done  = 2
qp4_odval_redemption_saving_face_done           = 3
qp4_odval_redemption_success                    = 4
qp4_odval_redemption_failure                    = 5
qp4_odval_redemption_success_via_bribe          = 6

###########################################################
# QUEST: Odval_return_to_tulbuk                           #
###########################################################
# Active states
qp4_odval_return_to_tulbuk_inactive             = 0
qp4_odval_return_to_tulbuk_odval_joined_party   = 1
qp4_odval_return_to_tulbuk_accepted_challenge   = 2
qp4_odval_return_to_tulbuk_refused_challenge    = 3

###########################################################
# QUEST: Odval_accept_the_challenge                       #
###########################################################
# Active states
qp4_odval_accept_the_challenge_inactive             = 0
qp4_odval_accept_the_challenge_challenge_accepted   = 1
qp4_odval_accept_the_challenge_challenge_begun      = 2
qp4_odval_accept_the_challenge_challenge_won        = 3
qp4_odval_accept_the_challenge_challenge_lost       = 4
qp4_odval_accept_the_challenge_challenge_complete   = 5
qp4_odval_accept_the_challenge_odval_fell           = 6
qp4_odval_accept_the_challenge_odval_fell_not_okay  = 7
qp4_odval_accept_the_challenge_odval_fell_but_okay  = 8
# General Parameters
qp4_odval_accept_the_challenge_wait_period          = 72

###########################################################
# QUEST: Odval_saving_face                                #
###########################################################
# Active states
qp4_odval_saving_face_inactive                      = 0
qp4_odval_saving_face_challenge_accepted            = 1
qp4_odval_saving_face_challenge_begun               = 2
qp4_odval_saving_face_challenge_won                 = 3
qp4_odval_saving_face_challenge_lost                = 4
# General Parameters
qp4_odval_saving_face_wait_period                   = 48

########################################################################################################################################################
####################                                                EDWYN STORY LINE                                                ####################
########################################################################################################################################################
# General Parameters
qp4_edwyn_home_town                             = "p_village_88"
qp4_edwyn_gather_info_chance_random             = 95
qp4_edwyn_gather_info_chance_specific           = 100
qp4_edwyn_storyarc_enabled                      = 0
###########################################################
# QUEST: Edwyn_intro                                      #
###########################################################
# Active states
qp4_edwyn_intro_inactive                        = 0
qp4_edwyn_intro_story_heard                     = 1
qp4_edwyn_intro_agreed_to_help                  = 2   # Quest Success
qp4_edwyn_intro_refused_to_help                 = 3   # Quest Failure

###########################################################
# QUEST: Edwyn_revenge                                    #
###########################################################
# Active states
qp4_edwyn_revenge_inactive                      = 0
qp4_edwyn_revenge_begun                         = 1
qp4_edwyn_revenge_one_knight_done               = 2
qp4_edwyn_revenge_two_knights_done              = 3
qp4_edwyn_revenge_three_knights_done            = 4
qp4_edwyn_revenge_success                       = 5   # Quest Success
qp4_edwyn_revenge_failure                       = 6   # Quest Failure

###########################################################
# QUEST: Edwyn_first_knight                               #
###########################################################
# Active states
qp4_edwyn_first_inactive                        = 0
qp4_edwyn_first_begun                           = 1
qp4_edwyn_first_learn_about_knight              = 2
qp4_edwyn_first_learn_of_lair_location          = 3
qp4_edwyn_first_found_lair_on_map               = 4
qp4_edwyn_first_entered_lair                    = 5
qp4_edwyn_first_conversation                    = 6
qp4_edwyn_first_knight_is_slain                 = 7   # Quest Success
qp4_edwyn_first_knight_lives_on                 = 8   # Quest Failure

###########################################################
# QUEST: Edwyn_second_knight                              #
###########################################################
# Active states
qp4_edwyn_second_inactive                       = 0
qp4_edwyn_second_begun                          = 1
qp4_edwyn_second_learn_of_location              = 2
qp4_edwyn_second_just_missed_him                = 3
qp4_edwyn_second_arrived_in_town                = 4
qp4_edwyn_second_knight_confrontation           = 5
qp4_edwyn_second_knight_is_slain                = 6   # Quest Success
qp4_edwyn_second_knight_lives_on                = 7   # Quest Failure
# General Parameters
qp4_edwyn_second_time_until_guard_arrives       = 20

###########################################################
# QUEST: Edwyn_third_knight                               #
###########################################################
# Active states
qp4_edwyn_third_inactive                        = 0
qp4_edwyn_third_begun                           = 1
qp4_edwyn_third_last_seen_location              = 2
qp4_edwyn_third_not_here_check_nearby_village   = 3
qp4_edwyn_third_arrival_in_village              = 4
qp4_edwyn_third_learned_story_from_elder        = 5
qp4_edwyn_third_allowed_knight_to_live          = 6   # Quest Failure, good for village.
qp4_edwyn_third_convinced_edwyn_to_spare_knight = 7   # Quest Success, good for village.
qp4_edwyn_third_planning_to_kill_knight         = 8
qp4_edwyn_third_knight_is_slain                 = 9   # Quest Success, but bad for village.
qp4_edwyn_third_knight_lives_on                 = 10  # Quest Failure
# General Parameters
qp4_villagers_present_for_fight                 = 20
qp4_villagers_that_must_survive                 = 10