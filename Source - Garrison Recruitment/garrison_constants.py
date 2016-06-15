# Garrison Recruitment & Training by Windyplains

###########################################################################################################################
#####                                                MODULE SETTINGS                                                  #####
###########################################################################################################################

# DEBUG_GARRISON                         = 0   # This turns ON (1) or OFF (0) all of the debug messages.  Set to 2 will enable -very- verbose information.

# $hub_mode Types
GARRISON_MODE_GENERAL                  = 1
GARRISON_MODE_RECRUITMENT              = 2
GARRISON_MODE_TRAINING                 = 3
GARRISON_MODE_REORDER                  = 4
GARRISON_MODE_QUEUE                    = 5
GARRISON_MODE_TROOP_INFO               = 6
GARRISON_MODE_EMBLEM_OPTIONS           = 7

###########################################################################################################################
#####                                                  PARTY SLOTS                                                    #####
###########################################################################################################################

slot_party_queue_progression           = 477
GRT_BUDGET_SPLIT                       = 0
GRT_BUDGET_FOCUSED                     = 1

slot_center_upgrade_garrison           = 452  # (0 - OFF / 1 - ON) With this enabled a center (that has a Captain of the Guard) will attempt to automatically upgrade its garrison.
slot_center_training_budget            = 455  # (integer) This holds how much money is to be spent on recruiting troops in a week.
slot_center_training_emblem_duration   = 456
slot_party_queue_budget                = 478
slot_party_queue_budget_excess         = 479
slot_party_queue_slot_id_begin         = 480 # This takes up slots 480-489
slot_party_queue_slot_id_end           = 490
slot_party_queue_slot_quantity_begin   = 490 # This takes up slots 490-499
slot_party_queue_slot_quantity_end     = 500


###########################################################################################################################
#####                                              GENERAL PARAMETERS                                                 #####
###########################################################################################################################

GRT_FUNDEFF_EMBLEM_BONUS               = 30
GRT_FUNDEFF_BASE                       = 65
GRT_FUNDEFF_TRAINING_GROUNDS           = 15

# script_grt_process_weekly_hiring modes
GRT_QUEUE_PROCESS                      = 1
GRT_QUEUE_PRINT                        = 2

# script_grt_convert_gold_to_xp_training
GRT_TRAINING_PREVIEW                   = 1   # This will simply apply the budget towards experience, but will not upgrade the target party.
GRT_TRAINING_PROCESS                   = 2   # This will directly upgrade a party given to it based on the budget.


###########################################################################################################################
#####                                            PRESENTATION DEFINITIONS                                             #####
###########################################################################################################################
GRT_OBJECTS                            = "trp_tpe_presobj"
# MAXIMUM_TROOP_RECORDS                  = 75

# Slots of HUB_OBJECTS
grt_obj_button_done                    = 1
grt_obj_label_main_title               = 2
grt_obj_button_general                 = 3
grt_obj_button_recruitment             = 4
grt_obj_button_training                = 5
grt_obj_button_reorder                 = 6
grt_obj_button_queue                   = 7
grt_obj_button_emblems                 = 8
grt_obj_container_1                    = 20
grt_obj_container_2                    = 21
grt_obj_container_3                    = 22
# hub1_obj_label_town                    = 23
# hub1_obj_label_faction                 = 24
grt_obj_label_main_title2              = 25
grt_obj_button_debug_advance           = 26

## RECRUITMENT
grt2_obj_numbox_hire_amount            = 77
grt2_val_numbox_hire_amount            = 78
grt2_obj_menu_budget_type              = 79
grt2_obj_checkbox_enable_recruiting    = 83
grt2_val_checkbox_enable_recruiting    = 84
grt2_val_button_troop_no               = 100
grt2_obj_button_recruit_troop          = 175
grt2_obj_button_inspect_equipment      = 250
grt2_obj_numbox_queue_qty              = 325
grt2_obj_button_dismiss_troop          = 400
grt2_obj_end_of_slots                  = 475

## QUEUE
grt3_obj_estimation_field              = 100
grt3_obj_button_debug_advance          = 101
grt3_obj_slider_garrison_recruiting    = 102
grt3_val_slider_garrison_recruiting    = 103
grt3_obj_text_recruiting_changes       = 104
grt3_obj_button_recruiting_apply       = 105

## EMBLEM OPTIONS
grt4_obj_button_option_1               = 100
grt4_obj_button_debug_gain_emblem      = 101
grt4_obj_container_1                   = 102
grt4_obj_button_option_2               = 103
grt4_obj_button_option_3               = 104
grt4_obj_button_option_4               = 105

## TRAINING
grt5_obj_portrait_guard_captain        = 100
grt5_obj_checkbox_enable_training      = 101
grt5_val_checkbox_enable_training      = 102
grt5_obj_container_1                   = 103
grt5_obj_container_2                   = 104
grt5_obj_button_upgrade_stacks         = 105 # Depreciated
grt5_obj_button_cheat_xp_party         = 106
grt5_obj_slider_garrison_training      = 107
grt5_val_slider_garrison_training      = 108
grt5_obj_text_training_changes         = 109
grt5_obj_button_training_apply         = 110
grt5_obj_checkbox_hide_maxed_units     = 111
grt5_val_checkbox_hide_maxed_units     = 112