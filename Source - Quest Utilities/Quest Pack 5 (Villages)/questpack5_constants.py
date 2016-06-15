# Quest Pack 5 (1.0) by Windyplains

from module_constants import *

QUEST_NOT_STARTED = 0
QUEST_IS_ACTIVE = 1
QUEST_COMPLETED = 2
QUEST_WAS_FAILED = 3
QUEST_WAS_REJECTED = 4


########################################################################################################################################################
####################                                      PARTY SLOTS USED FOR VILLAGE QUESTS                                       ####################
########################################################################################################################################################

# Start & Stop slots for reference.
# village_elder_quests_begin = "qst_deliver_grain"
# village_elder_quests_end = "qst_quest_pack_5_end" # "qst_eliminate_bandits_infesting_village"
# village_elders_begin   = "trp_village_1_elder"
# village_elders_end     = "trp_merchants_end"

slot_village_quest_cooldown                       = 284
slot_village_quest_deliver_grain                  = 285 # Native Quest
slot_village_quest_deliver_cattle                 = 286 # Native Quest
slot_village_quest_train_peasants_against_bandits = 287 # Native Quest
slot_village_quest_craftsmans_knowledge           = 288
slot_village_quest_sending_aid                    = 289
slot_village_quest_healers_touch                  = 290
slot_village_quest_lambs_become_lions             = 291
slot_village_quest_urgent_delivery                = 292
# slot_village_quest_sending_aid = 293
# slot_village_quest_ = 294
# slot_village_quest_ = 295
# slot_village_quest_ = 296
# slot_village_quest_ = 297
# slot_village_quest_ = 298
# slot_village_quest_ = 299
# slot_village_quest_ = 300

qp5_quest_slots_begin = slot_village_quest_deliver_grain
qp5_quest_slots_end = slot_village_quest_healers_touch

###########################################################
# QUEST: craftsmans_knowledge                             #
###########################################################
# Active states
QP5_QUEST_INACTIVE                              = 0
qp5_ck_begun                                    = 1
qp5_ck_worker_injury                            = 2
qp5_ck_supplies_low                             = 3
qp5_ck_supplies_being_obtained_by_villagers     = 4
qp5_ck_supplies_being_obtained_by_player        = 5
qp5_ck_supplies_restored                        = 6
qp5_ck_work_completed                           = 7
qp5_ck_quest_failed                             = 8
# General constants
qp5_ck_pause_period                             = 24 # This represnets the hours worked each stage.

###########################################################
# QUEST: sending_aid                                      #
###########################################################
# Active states
QP5_QUEST_INACTIVE                              = 0
qp5_sa_begun                                    = 1
qp5_sa_recovery                                 = 2
qp5_sa_village_recovered                        = 3
qp5_sa_escort                                   = 4
qp5_sa_took_too_long                            = 5
qp5_sa_returned_to_giver                        = 6
qp5_sa_failed_to_appear                         = 7

###########################################################
# QUEST: healers_touch                                    #
###########################################################
# Active states
QP5_QUEST_INACTIVE                              = 0
qp5_ht_begun                                    = 1 # Quest picked up, second visit not had.
## SITUATIONAL BREAK - Bandit's Arrow - Begin
qp5_ht_the_bandits_arrow                        = 2 # Elder spoken to companion.  Learn supplies are needed.
qp5_ht_returning_with_supplies                  = 3 # Supplies have been acquired from location.
qp5_ht_awaiting_results                         = 4 # Supplies have been delivered.  Awaiting results.
qp5_ht_arrows_end                               = 5 # Wait period has ended.  Find out if the person recovers.
## SITUATIONAL BREAK - Bandit's Arrow - End