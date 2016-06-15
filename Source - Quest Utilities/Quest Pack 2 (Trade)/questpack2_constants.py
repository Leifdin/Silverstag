# Quest Pack 2 (1.0) by Windyplains

from module_constants import *

# General constants
qp2_buying_an_item                              = 201
qp2_selling_an_item                             = 202
qp2_trade_goods_begin                           = trade_goods_begin
qp2_trade_goods_end                             = food_begin
qp2_quests_begin                                = "qst_floris_trade_shortage"
qp2_quests_end                                  = "qst_quest_pack_2_end"

###########################################################
# QUEST: floris_trade_shortage                            #
###########################################################
# Active states
qp2_shortage_inactive                           = 0
qp2_shortage_discovery                          = 1
qp2_shortage_picked_up_commodity                = 2
qp2_shortage_arrived_in_target_center           = 3
qp2_shortage_sold_items_to_town                 = 4
qp2_shortage_sold_items_to_merchant             = 5
# Parameters
qp2_shortage_cooldown                           = 3
qp2_shortage_expiration                         = 30

###########################################################
# QUEST: floris_trade_surplus                             #
###########################################################
# Active states
qp2_surplus_inactive                            = 0
qp2_surplus_discovery                           = 1
qp2_surplus_arrived_in_target_center            = 2
qp2_surplus_picked_up_commodity                 = 3
qp2_surplus_sold_items_to_town                  = 4

###########################################################
# QUEST: floris_trade_bargain                             #
###########################################################
# Active states
qp2_bargain_inactive                            = 0
qp2_bargain_discovery                           = 1
qp2_bargain_purchased_commodity                 = 2
qp2_bargain_sold_commodity                      = 3
# Parameters
qp2_min_distance_to_target_center_fortune       = 30
qp2_max_distance_to_target_center_fortune       = 100
qp2_bargain_cooldown                            = 1
qp2_bargain_expiration                          = 10

###########################################################
# QUEST: floris_trade_fortune_favors_the_bold             #
###########################################################
qp2_fortune_inactive                            = 0
qp2_fortune_arrived_in_primary_center           = 1
qp2_fortune_purchased_commodity_in_primary_town = 2
qp2_fortune_arrived_in_second_center            = 3
qp2_fortune_purchased_commodity_in_second_town  = 4
qp2_fortune_completed_route                     = 5
# Parameters
qp2_fortune_bandit_troop                        = "trp_bandit" # "trp_bandit_n_bandit" (Floris) # "trp_bandit" (Native)

###########################################################
# QUEST: trade_noble_opportunity                          #
###########################################################
qp2_opportunity_inactive                        = 0
qp2_opportunity_begun                           = 1  # You've learned he needs a loan.
qp2_opportunity_discussed_with_lord             = 2  # You mentioned his need while speaking with him.
qp2_opportunity_provided_loan                   = 3  # You've invested.  Now you need to wait until he's ready to repay the loan.
qp2_opportunity_lord_ready_to_repay             = 4  # You've received word (upon entering a town) he's ready to repay you.
qp2_opportunity_received_payment                = 5  # You've received payment.
# Parameters
slot_quest_payment_return                       = slot_quest_stage_7_trigger_chance
slot_quest_payment_failure_chance               = slot_quest_stage_8_trigger_chance
slot_quest_lord_will_repay_loan                 = slot_quest_stage_9_trigger_chance
slot_quest_days_remaining_for_repayment         = slot_quest_stage_10_trigger_chance

###########################################################
# QUEST: trade_discount_enterprise                        #
###########################################################
qp2_discount_inactive                           = 0
qp2_discount_discovered                         = 1
qp2_discount_spoken_with_guildmaster            = 2
qp2_discount_purchased                          = 3
qp2_discount_declined                           = 4
# Parameters
slot_quest_enterprise_discount                  = slot_quest_stage_8_trigger_chance
slot_quest_enterprise_item                      = slot_quest_stage_9_trigger_chance
slot_quest_enterprise_name                      = slot_quest_stage_10_trigger_chance

# Trade Rival Constants
qp2_trade_rivals_begin                          = "trp_trade_rival_1"
qp2_trade_rivals_end                            = "trp_trade_rival_end"

# Trade Rival Status
qp2_rival_status_inactive                       = 0
qp2_rival_status_active                         = 1
qp2_rival_status_captured                       = 2

# Trade Rival Misc
qp2_trs_proficiency_gain_per_day                = 3
qp2_trs_proficiency_per_level_ratio             = 100
qp2_trs_proficiency_penalty_per_level           = 2

# Trade Rival Slots (start with 200)
slot_rival_proficiency                          = 200
slot_rival_status                               = 201
slot_rival_trade_skill                          = 202
slot_rival_location                             = 203
slot_rival_x_loc                                = 204
slot_rival_y_loc                                = 205
slot_rival_destination                          = 206
slot_rival_current_wealth                       = 207
slot_rival_accumulated_wealth                   = 208
slot_rival_home_region                          = 209
slot_rival_relation_player                      = 210
slot_rival_relation_rival_1                     = 211
slot_rival_relation_rival_2                     = 212
slot_rival_relation_rival_3                     = 213
slot_rival_relation_rival_4                     = 214
slot_rival_relation_rival_5                     = 215
slot_rival_individual_relations_end             = 216
# Skip 10 slots to make available space for new rivals.
slot_rival_relation_fac_player                  = 226
slot_rival_relation_fac_1                       = 227
slot_rival_relation_fac_2                       = 228
slot_rival_relation_fac_3                       = 229
slot_rival_relation_fac_4                       = 230
slot_rival_relation_fac_5                       = 231
slot_rival_relation_fac_6                       = 232
slot_rival_faction_relations_end                = 233
# Skip 10 slots to make available space for new rivals.
slot_rival_last_quest_attempted                 = 243
slot_rival_last_quest_winner                    = 244
slot_rival_last_quest_destination               = 245
slot_rival_last_quest_focus                     = 246
slot_rival_last_quest_commentary                = 247
slot_rival_destination_set                      = 248
# Begin quest related information
# Quest Pack 2, Quest 1 - Trade Commodity Shortage
slot_rival_quest_shortage_status                = 300
slot_rival_quest_shortage_stage                 = 301
slot_rival_quest_shortage_trigger_chance        = 302
# Quest Pack 2, Quest 2 - Trade Commodity Surplus
slot_rival_quest_surplus_status                 = 310
slot_rival_quest_surplus_stage                  = 311
slot_rival_quest_surplus_trigger_chance         = 312
# Quest Pack 2, Quest 3 - Fortune Favors the Bold
slot_rival_quest_fortune_status                 = 320
slot_rival_quest_fortune_stage                  = 321
slot_rival_quest_fortune_cycle_count            = 322
slot_rival_quest_fortune_trigger_chance         = 323
# Quest Pack 2, Quest 4 - A Noble Opportunity
slot_rival_quest_opportunity_status             = 330
slot_rival_quest_opportunity_stage              = 331
slot_rival_quest_opportunity_trigger_chance     = 332
# Quest Pack 2, Quest 5 - Discount Enterprise
slot_rival_quest_discount_ent_status            = 340
slot_rival_quest_discount_ent_stage             = 341
slot_rival_quest_discount_ent_trigger_chance    = 342
# Quest Pack 2, Quest 3 - Trade Commodity Bargain
# slot_rival_quest_bargain_status                 = 320
# slot_rival_quest_bargain_stage                  = 321
# slot_rival_quest_bargain_purchase_price         = 322
# slot_rival_quest_bargain_sale_price             = 323
# slot_rival_quest_bargain_trigger_chance         = 324

slot_rival_data_begin                           = 200
slot_rival_data_end                             = 343

# OBJECT SLOTS - RIVAL DEBUG DISPLAY
# Trade Rival Slots (start with 200)
trs_obj_rival_proficiency                       = 1
trs_obj_rival_status                            = 2
trs_obj_rival_trade_skill                       = 3
trs_obj_rival_location                          = 4
trs_obj_rival_x_loc                             = 5
trs_obj_rival_y_loc                             = 6
trs_obj_rival_destination                       = 7
trs_obj_rival_current_wealth                    = 8
trs_obj_rival_accumulated_wealth                = 9
trs_obj_rival_home_region                       = 10
trs_obj_rival_relation_player                   = 11
trs_obj_rival_relation_rival_1                  = 12
trs_obj_rival_relation_rival_2                  = 13
trs_obj_rival_relation_rival_3                  = 14
trs_obj_rival_relation_rival_4                  = 15
trs_obj_rival_relation_rival_5                  = 16
trs_obj_rival_individual_relations_end          = 17
# Skip 10 slots to make available space for new rivals.
trs_obj_rival_relation_fac_player               = 27
trs_obj_rival_relation_fac_1                    = 28
trs_obj_rival_relation_fac_2                    = 29
trs_obj_rival_relation_fac_3                    = 30
trs_obj_rival_relation_fac_4                    = 31
trs_obj_rival_relation_fac_5                    = 32
trs_obj_rival_relation_fac_6                    = 33
trs_obj_rival_faction_relations_end             = 34
# Skip 10 slots to make available spac for new rivals.
trs_obj_rival_last_quest_attempted              = 44
trs_obj_rival_last_quest_winner                 = 45
trs_obj_rival_last_quest_destination            = 46
trs_obj_rival_last_quest_focus                  = 47
trs_obj_rival_last_quest_commentary             = 48
# Skip 10 slots to make available for new last quest info.
trs_obj_rival_name                              = 50
trs_obj_rival_portrait                          = 51
trs_obj_rival_button_done                       = 52
trs_obj_rival_container_faction_relation        = 53
trs_obj_rival_container_individual_relation     = 54
trs_obj_rival_prev_troop                        = 55
trs_obj_rival_next_troop                        = 56
trs_obj_rival_last_quest_title                  = 57
trs_obj_rival_current_quest_title               = 58
trs_obj_rival_current_quest_name                = 59
trs_obj_rival_current_quest_progress            = 60
trs_obj_rival_current_quest_description         = 61