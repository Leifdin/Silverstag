# Companion Management System (1.0) by Windyplains

DEBUG_DWS                              = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.
DEBUG_ALS                              = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.
DEBUG_CRM                              = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.
DEBUG_ROLE                             = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.

# TROOP SLOTS
###########################################################################################################################
#####                                         COMBINED TROOP / PARTY SLOTS                                            #####
###########################################################################################################################
# DWS Slots
slot_troop_dws_out_of_date             = 239
slot_troop_dws_sets_begin              = 240
slot_troop_battlefield_set_1           = 240
slot_troop_battlefield_set_2           = 241
slot_troop_battlefield_set_3           = 242
slot_troop_battlefield_set_4           = 243
slot_troop_siege_set_1                 = 244
slot_troop_siege_set_2                 = 245
slot_troop_siege_set_3                 = 246
slot_troop_siege_set_4                 = 247
slot_troop_dws_sets_end                = 248
slot_troop_dws_enabled                 = 248
slot_troop_dws_all_or_nothing          = 249
# Autolooting Slots
slot_troop_upgrade_weapon_1            = 250
slot_troop_upgrade_weapon_2            = 251
slot_troop_upgrade_weapon_3            = 252
slot_troop_upgrade_weapon_4            = 253
slot_troop_upgrade_helm                = 254
slot_troop_upgrade_armor               = 255
slot_troop_upgrade_boots               = 256
slot_troop_upgrade_gloves              = 257
slot_troop_upgrade_mount               = 258
slot_troop_enable_autolooting          = 259
slot_troop_retain_heraldic_items       = 260
slot_troop_prevent_breaking_sets       = 261
slot_troop_upgrade_weapon_1_type       = 262
slot_troop_upgrade_weapon_2_type       = 263
slot_troop_upgrade_weapon_3_type       = 264
slot_troop_upgrade_weapon_4_type       = 265
slot_troop_weight_limit                = 266
# Companion Roles
slot_party_role_storekeeper            = 390 # Quest system stops at 389.
slot_item_food_portion                 = 81
###########################################################################################################################
#####                                             DYNAMIC WEAPON SYSTEM                                               #####
###########################################################################################################################

DWS_OBJECTS                            = "trp_als_presobj"

## PRESENTATION OBJECT DEFINITIONS ##
dws_obj_button_accept                  = 1
dws_obj_button_cancel                  = 2
dws_obj_portrait_selected_troop        = 3
dws_obj_menu_selected_character        = 4
dws_val_menu_selected_character        = 5
dws_obj_label_main_title               = 6
dws_obj_selected_item                  = 7
dws_val_selected_item                  = 8
dws_obj_test                           = 9
dws_val_battlefield_set_1              = 10
dws_val_battlefield_set_2              = 11
dws_val_battlefield_set_3              = 12
dws_val_battlefield_set_4              = 13
dws_val_siege_set_1                    = 14
dws_val_siege_set_2                    = 15
dws_val_siege_set_3                    = 16
dws_val_siege_set_4                    = 17
dws_end_of_sets                        = 18 # Nothing is stored here.
dws_obj_checkbox_enable                = 23
dws_val_checkbox_enable                = 24
dws_obj_checkbox_all_or_nothing        = 25
dws_val_checkbox_all_or_nothing        = 26
dws_obj_checkbox_report                = 27
dws_val_checkbox_report                = 28
dws_val_menu_troop_1                   = 100
# Reserve next 30 slots.  Start with 130 next.

###########################################################################################################################
#####                                               AUTOLOOT SYSTEM                                                   #####
###########################################################################################################################

ALS_OBJECTS                            = "trp_als_presobj"
ALS_TRADE_CONFIRM                      = "trp_als_approval_item"
ALS_OLD_ITEM                           = "trp_als_old_item"
ALS_NEW_ITEM                           = "trp_als_new_item"
ALS_LOOTER                             = "trp_als_troop"

als_head_armor_medium                  = 250
als_head_armor_light                   = 100
als_body_armor_medium                  = 2000
als_body_armor_light                   = 1500
als_hand_armor_medium                  = 150
als_hand_armor_light                   = 50
als_foot_armor_medium                  = 200
als_foot_armor_light                   = 125

# VALUES FOR UPGRADE MENUS
als_keep_current                       = 0
# Armor
als_find_upgrade                       = 1 # Used by armor & mounts.
# Mounts
als_mount_fastest                      = 1
als_mount_resilient                    = 2
als_mount_best                         = 3
# Weapons
als_shield_mounted                     = 1 # Used by weapons.
als_shield_unmounted                   = 2
als_one_hand                           = 3
als_two_hand                           = 4
als_polearm                            = 5
als_lance                              = 6
als_arrows                             = 7
als_bow_mounted                        = 8
als_bow_unmounted                      = 9
als_bolts                              = 10
als_crossbow_mounted                   = 11
als_crossbow_unmounted                 = 12
als_throwing                           = 13

# VALUES FOR WEIGHT LIMIT OPTION
als_limit_armor_any                    = 0
als_limit_armor_light                  = 1
als_limit_armor_medium                 = 2

##########################################
## PRESENTATION: Autoloot Configuration ##
##########################################
als_obj_button_accept                  = 1
als_obj_button_cancel                  = 2
als_obj_portrait_selected_troop        = 3
als_obj_menu_selected_character        = 4
als_val_menu_selected_character        = 5
als_obj_label_main_title               = 6
dws_obj_selected_item                  = 7
dws_val_selected_item                  = 8
als_obj_test                           = 9
als_val_slot_0                         = 10
als_val_slot_1                         = 11
als_val_slot_2                         = 12
als_val_slot_3                         = 13
als_val_slot_4                         = 14
als_val_slot_5                         = 15
als_val_slot_6                         = 16
als_val_slot_7                         = 17
als_val_slot_8                         = 18
als_obj_menu_slot_0                    = 20
als_obj_menu_slot_1                    = 21
als_obj_menu_slot_2                    = 22
als_obj_menu_slot_3                    = 23
als_obj_menu_slot_4                    = 24
als_obj_menu_slot_5                    = 25
als_obj_menu_slot_6                    = 26
als_obj_menu_slot_7                    = 27
als_obj_menu_slot_8                    = 28
als_val_menu_slot_0                    = 30
als_val_menu_slot_1                    = 31
als_val_menu_slot_2                    = 32
als_val_menu_slot_3                    = 33
als_val_menu_slot_4                    = 34
als_val_menu_slot_5                    = 35
als_val_menu_slot_6                    = 36
als_val_menu_slot_7                    = 37
als_val_menu_slot_8                    = 38
als_val_menu_slot_9                    = 39 # Unused, but needed.
als_obj_checkbox_enable                = 43
als_val_checkbox_enable                = 44
als_obj_checkbox_no_break_sets         = 45
als_val_checkbox_no_break_sets         = 46
als_obj_checkbox_heraldic_items        = 47
als_val_checkbox_heraldic_items        = 48
als_obj_label_strength                 = 49
als_obj_label_powerdraw                = 50
als_obj_label_powerthrow               = 51
als_obj_label_shield                   = 52
als_obj_label_riding                   = 53
als_obj_label_horsearchery             = 54
als_obj_label_onehand                  = 55
als_obj_label_twohand                  = 56
als_obj_label_polearm                  = 57
als_obj_label_archery                  = 58
als_obj_label_crossbow                 = 59
als_obj_label_thrown                   = 60
als_obj_menu_weapon_type_0             = 61
als_obj_menu_weapon_type_1             = 62
als_obj_menu_weapon_type_2             = 63
als_obj_menu_weapon_type_3             = 64
als_val_menu_weapon_type_0             = 65
als_val_menu_weapon_type_1             = 66
als_val_menu_weapon_type_2             = 67
als_val_menu_weapon_type_3             = 68
als_obj_label_comments_0               = 69
als_obj_label_comments_1               = 70
als_obj_label_comments_2               = 71
als_obj_label_comments_3               = 72
als_obj_label_comments_4               = 73
als_obj_label_comments_5               = 74
als_obj_label_comments_6               = 75
als_obj_label_comments_7               = 76
als_obj_label_comments_8               = 77
als_obj_inventory_search               = 78
als_obj_copy_settings_to_all           = 79
als_obj_equipment_page                 = 80
als_obj_menu_weight_limit              = 81
als_val_menu_weight_limit              = 82
als_obj_label_weight_limit             = 83
als_obj_label_encumbrance              = 84

als_val_menu_troop_1                   = 100
# Reserve next 30 slots.  Start with 130 next.


##########################################
## PRESENTATION: Autoloot Confirmation  ##
##########################################
alc_obj_button_accept                  = 1
alc_obj_button_cancel                  = 2
alc_obj_label_main_title               = 3
alc_obj_label_sub_title                = 4
alc_obj_label_approve                  = 5
alc_obj_label_slot                     = 6
alc_obj_label_old                      = 7
alc_obj_label_new                      = 8
alc_obj_label_comment                  = 9
alc_obj_label_companion                = 10
alc_obj_main_container                 = 11
alc_obj_portrait_selected_troop        = 12
alc_obj_label_main_title               = 13
alc_obj_label_upgrade_text             = 14
alc_obj_label_upgrade_text_container   = 15
alc_obj_approval_checkboxes_begin      = 100
alc_obj_approval_checkboxes_end        = 115
alc_obj_companion_labels               = 120 # - 139
alc_obj_slot_labels                    = 140 # - 159
alc_obj_old_item_labels                = 160 # - 179
alc_obj_new_item_labels                = 180 # - 199
alc_obj_comment_labels                 = 200 # - 219


###########################################################################################################################
#####                                           COMPANION RELATION MATRIX                                             #####
###########################################################################################################################

CRM_OBJECTS                            = "trp_als_presobj"

##########################################
## PRESENTATION: Companion Relations    ##
##########################################
crm_obj_button_exit                    = 1
crm_obj_label_upgrade_text_container   = 2
crm_obj_label_main_title               = 3
crm_obj_temporary                      = 4

###########################################################################################################################
#####                                                  PARTY ROLES                                                    #####
###########################################################################################################################

ROLE_OBJECTS                            = "trp_als_presobj"

# General Roles
ROLE_UNASSIGNED                         = 0
ROLE_STOREKEEPER                        = 1
ROLE_QUARTERMASTER                      = 2
ROLE_JAILER                             = 3
ROLE_FARRIER                            = 4

##########################################
## PRESENTATION: Companion Relations    ##
##########################################
role_obj_button_exit                    = 1
role_obj_label_main_container           = 2
role_obj_label_main_title               = 3
role_obj_menu_storekeeper               = 4
#role_obj_menu_storekeeper               = 5
role_val_menu_storekeeper               = 6
role_obj_label_storekeeper              = 7
role_obj_label_storekeeper_desc         = 8
role_obj_label_storekeeper_report       = 9
role_obj_label_skr_days_left            = 10
role_obj_label_skr_food_morale          = 11
role_obj_label_skr_kinds_of_food        = 12
role_obj_label_storekeeper_reqs         = 13

role_obj_menu_quartermaster             = 20
role_val_menu_quartermaster             = 21
role_obj_label_quartermaster            = 22
role_obj_label_quartermaster_desc       = 23
role_obj_label_quartermaster_report     = 24
role_obj_label_quartermaster_reqs       = 25
role_obj_label_quartermaster_space_used = 26
role_obj_label_quartermaster_loot_value = 27
role_obj_label_quartermaster_best_item  = 28

role_obj_menu_jailer                    = 30
role_val_menu_jailer                    = 31
role_obj_label_jailer                   = 32
role_obj_label_jailer_desc              = 33
role_obj_label_jailer_report            = 34
role_obj_label_jailer_prisoner_count    = 35
role_obj_label_jailer_prisoner_value    = 36
role_obj_label_jailer_last_town         = 37
role_obj_label_jailer_reqs              = 38

role_val_menu_troop_1                   = 100 # Next several slots store troop_no's of each hero in the party so menus know who is selected.

