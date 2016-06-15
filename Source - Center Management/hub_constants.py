# Center Hub (1.0) by Windyplains

###########################################################################################################################
#####                                                MODULE SETTINGS                                                  #####
###########################################################################################################################

# DEBUG_HUB                              = 0   # This turns ON (1) or OFF (0) all of the debug messages.  Set to 2 will enable -very- verbose information.

## TROOP SLOTS
slot_troop_recruitable_faction_1   = 155
slot_troop_recruitable_faction_2   = 156
slot_troop_recruitable_faction_3   = 157

###########################################################################################################################
#####                                            ITEM BALANCING & RATINGS                                             #####
###########################################################################################################################

slot_item_best_in_type                 = 125
slot_item_worst_in_type                = 126
slot_item_rated_weight                 = 127

rating_multiplier_armor                = 25    # Effectively improves armor rating by x2.5 of base value.
rating_multiplier_weapon               = 40    # 40%
rating_multiplier_skill                = 75    # Skill * multiplier for weapon ratings.
rating_multiplier_weapon_weight        = 3     # Item % * multiplier.
rating_ranged_melee_discount           = 15    # -15% to both ranged & melee attack rating costs.

###########################################################################################################################
#####                                            PRESENTATION DEFINITIONS                                             #####
###########################################################################################################################
HUB_OBJECTS                            = "trp_tpe_presobj"
MAXIMUM_TROOP_RECORDS                  = 75

# $hub_mode Types
HUB_MODE_GENERAL                       = 1
HUB_MODE_FINANCES                      = 2
HUB_MODE_IMPROVEMENTS                  = 3
HUB_MODE_RECRUITMENT                   = 4
HUB_MODE_ADVISORS                      = 5
HUB_MODE_GARRISON                      = 6
HUB_MODE_QUESTS                        = 7
HUB_MODE_TROOP_INFO                    = 8
HUB_MODE_COMMISSIONS                   = 9
HUB_MODE_REALM_AFFAIRS                 = 10

# Slots of HUB_OBJECTS
hub_obj_button_done                    = 1
hub_obj_label_main_title               = 2
hub_obj_button_general_info            = 3
hub_obj_button_finances                = 4
hub_obj_button_improvements            = 5
hub_obj_button_recruitment             = 6
hub_obj_button_advisors                = 7
hub_obj_button_garrison                = 8
hub_obj_button_quests                  = 9
hub_obj_container_1                    = 20
hub_obj_container_2                    = 21
hub_obj_container_3                    = 22
hub1_obj_label_town                    = 23
hub1_obj_label_faction                 = 24
hub_obj_label_main_title2              = 25
hub_obj_label_player_gold              = 26
hub_obj_label_treasury_gold            = 27
hub_obj_label_player_emblems           = 28
hub_obj_button_commissions             = 29
hub_obj_button_realm_affairs           = 30

## GENERAL INFORMATION
hub1_obj_button_rename_center          = 100
hub1_obj_textbox_rename_center         = 101
hub1_obj_button_give_up_center         = 102

## FINANCIAL
hub2_obj_button_treasury_deposit       = 100
hub2_obj_button_allocation_increase    = 101
hub2_obj_treasury_changes              = 102
hub2_obj_button_treasury_withdraw      = 103
hub2_obj_slider_treasury               = 104
hub2_val_slider_treasury               = 105
hub2_obj_button_allocation_decrease    = 106
hub2_obj_slider_garrison_recruiting    = 107
hub2_val_slider_garrison_recruiting    = 108
hub2_obj_text_recruiting_changes       = 109
hub2_obj_button_recruiting_apply       = 110
hub2_obj_slider_garrison_training      = 111
hub2_val_slider_garrison_training      = 112
hub2_obj_text_training_changes         = 113
hub2_obj_button_training_apply         = 114

## IMPROVEMENTS
hub3_obj_slider_improvement_selector   = 100
hub3_val_slider_improvement_selector   = 101
hub3_obj_button_cancel_const_1         = 102
hub3_obj_button_cancel_1_label         = 103
hub3_obj_button_cancel_1_back_enabled  = 104
hub3_obj_button_cancel_1_back_disabled = 105
hub3_obj_button_cancel_const_2         = 106
hub3_obj_button_cancel_2_label         = 107
hub3_obj_button_cancel_2_back_enabled  = 108
hub3_obj_button_cancel_2_back_disabled = 109
hub3_obj_button_cancel_const_3         = 110
hub3_obj_button_cancel_3_label         = 111
hub3_obj_button_cancel_3_back_enabled  = 112
hub3_obj_button_cancel_3_back_disabled = 113
hub3_obj_label_improvement_name        = 114
hub3_obj_label_improvement_desc        = 115
hub3_obj_label_improvement_time        = 116
hub3_obj_label_improvement_cost        = 117
hub3_obj_button_improvement_build      = 118
hub3_obj_button_build_label            = 119
hub3_obj_button_build_back_enabled     = 120
hub3_obj_button_build_back_disabled    = 121
hub3_obj_button_improvement_destroy    = 122
hub3_obj_button_destroy_label          = 123
hub3_obj_button_destroy_back_enabled   = 124
hub3_obj_button_destroy_back_disabled  = 125
hub3_obj_label_improvement_applicable  = 126
hub3_obj_button_improvement_complete   = 127
hub3_obj_button_complete_label         = 128
hub3_obj_button_complete_back_enabled  = 129
hub3_obj_button_complete_back_disabled = 130
hub3_obj_menu_emblem_build_time        = 131
hub3_val_menu_emblem_build_time        = 132
hub3_obj_menu_emblem_build_cost        = 133
hub3_val_menu_emblem_build_cost        = 134

## RECRUITMENT
hub4_obj_toggle_party_members_only     = 75
hub4_label_toggle_party_members_only   = 76
hub4_obj_numbox_hire_amount            = 77
hub4_val_numbox_hire_amount            = 78
hub4_obj_button_reduce_training_cost   = 79
hub4_val_button_troop_no               = 100
hub4_obj_button_recruit_troop          = 175
hub4_obj_button_inspect_equipment      = 250
hub4_obj_button_dismiss_troop          = 325


AI_RECRUIT_CAVALRY                     = 0
AI_RECRUIT_INFANTRY                    = 1
AI_RECRUIT_ARCHERS                     = 2
AI_RECRUIT_HORSE_ARCHERS               = 3