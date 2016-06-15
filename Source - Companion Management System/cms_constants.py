# Companion Management System (1.0) by Windyplains

from module_constants import *

# DEBUG_DWS                              = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.
# DEBUG_ALS                              = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.
# DEBUG_CRM                              = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.
# DEBUG_ROLE                             = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.
# DEBUG_READING                          = 0   # ON (1) / OFF (0) - Displays all of the undefined debug messages.  Set to 2 will enable -very- verbose information.

# TROOP SLOTS
###########################################################################################################################
#####                                         COMBINED TROOP / PARTY SLOTS                                            #####
###########################################################################################################################
# Companion Reading
slot_troop_reading_book                = 299
# DWS Slots
slot_troop_dws_out_of_date             = 300
slot_troop_dws_sets_begin              = 301
slot_troop_battlefield_set_1           = 301
slot_troop_battlefield_set_2           = 302
slot_troop_battlefield_set_3           = 303
slot_troop_battlefield_set_4           = 304
slot_troop_siege_set_1                 = 305
slot_troop_siege_set_2                 = 306
slot_troop_siege_set_3                 = 307
slot_troop_siege_set_4                 = 308
slot_troop_dws_sets_end                = 309
slot_troop_dws_enabled                 = 309
slot_troop_dws_all_or_nothing          = 310
# Autolooting Slots
slot_troop_upgrade_weapon_1            = 311
slot_troop_upgrade_weapon_2            = 312
slot_troop_upgrade_weapon_3            = 313
slot_troop_upgrade_weapon_4            = 314
slot_troop_upgrade_helm                = 315
slot_troop_upgrade_armor               = 316
slot_troop_upgrade_boots               = 317
slot_troop_upgrade_gloves              = 318
slot_troop_upgrade_mount               = 319
slot_troop_enable_autolooting          = 320
slot_troop_retain_heraldic_items       = 321
slot_troop_prevent_breaking_sets       = 322
slot_troop_upgrade_weapon_1_type       = 323
slot_troop_upgrade_weapon_2_type       = 324
slot_troop_upgrade_weapon_3_type       = 325
slot_troop_upgrade_weapon_4_type       = 326
slot_troop_weight_limit                = 327

# Companion Roles
#slot_party_role_storekeeper            = 390 # Quest system stops at 389.
slot_item_food_portion                 = 81
# Slots 82-84 left open for future use.
slot_item_npc1_read                    = 85
# Slots 86-110 reserved for companion use.
cms_reading_checklist                  = slot_item_npc1_read


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

# $autoloot_mode constant values
ALS_MODE_BATTLEFIELD_LOOT              = 1
ALS_MODE_PLAYER_SEARCH                 = 2
ALS_MODE_BROWSE_MERCHANTS              = 3

## Baseline comparison values for autoloot ratings
# MOUNTS
MOUNT_BASELINE_HEALTH                  = 140
MOUNT_BASELINE_SPEED                   = 40
MOUNT_BASELINE_MANEUVER                = 40
MOUNT_BASELINE_ARMOR                   = 25
# SHIELDS
SHIELD_BASELINE_HEALTH                 = 220
SHIELD_BASELINE_RESIST                 = 15
SHIELD_BASELINE_WIDTH                  = 75
SHIELD_BASELINE_HEIGHT                 = 75
# ARMOR
ARMOR_BASELINE_HEAD                    = 25
ARMOR_BASELINE_BODY                    = 30
ARMOR_BASELINE_LEGS                    = 15
# AMMUNITION
AMMO_BASELINE_DAMAGE                   = 1
AMMO_BASELINE_AMMO                     = 30
# RANGED WEAPONS
RANGED_BASELINE_DAMAGE                 = 20
RANGED_BASELINE_ACCURACY               = 100
RANGED_BASELINE_SPEED                  = 95
# MELEE WEAPONS
MELEE_BASELINE_DAMAGE                  = 25
MELEE_BASELINE_REACH                   = 100
MELEE_BASELINE_SPEED                   = 95

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

# Used by $cms_report_mode
CMS_REPORTS_SUMMARY                     = 0
CMS_REPORTS_DETAILED                    = 1

# General Roles
ROLE_UNASSIGNED                         = 0
ROLE_STOREKEEPER                        = 1
ROLE_QUARTERMASTER                      = 2
ROLE_JAILER                             = 3
ROLE_FARRIER                            = 4

# Jailer Mode Definitions
CMS_JAILER_DISABLED                     = 0
CMS_JAILER_SELL_ONLY                    = 1
CMS_JAILER_STORE_ONLY                   = 2
CMS_JAILER_STORE_AND_SELL               = 3

# script_cms_get_item_value_with_imod - Functions
CMS_AUTO_BUYING                         = 1
CMS_AUTO_SELLING                        = 2
CMS_AUTO_LOOTING                        = 3

# $cms_display = CMS_MODE constants to switch between presentations.
CMS_MODE_MAIN                           = 1  # Displays all companions with links to other modes.
CMS_MODE_AUTOLOOT_SETTINGS              = 2  # Auto-loot setting screen for a specific companion.
CMS_MODE_READING                        = 3  # Displays reading information about a specific companion.
CMS_MODE_RELATION_MATRIX                = 4  # Shows the companion relationship matrix.
CMS_MODE_INVENTORY                      = 5  # Inventory screen for a specific companion.
CMS_MODE_EQUIPMENT                      = 6  # Equipment trading screen for a specific companion.
CMS_MODE_CHARACTER_VIEWER               = 7  # Inspection description for a specific companion.
CMS_MODE_PARTY_ROLES                    = 8  # Party role assignment screen.
CMS_MODE_SHOPPING_LIST                  = 9  # Storekeeper shopping list screen.

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
role_obj_button_shopping_list           = 14
role_obj_checkbox_storekeeper_enable    = 15
role_val_checkbox_storekeeper_enable    = 16

role_obj_menu_quartermaster             = 40
role_val_menu_quartermaster             = 41
role_obj_label_quartermaster            = 42
role_obj_label_quartermaster_desc       = 43
role_obj_label_quartermaster_report     = 44
role_obj_label_quartermaster_reqs       = 45
role_obj_label_quartermaster_space_used = 46
role_obj_label_quartermaster_loot_value = 47
role_obj_label_quartermaster_best_item  = 48
role_obj_checkbox_quartermaster_enable  = 49
role_val_checkbox_quartermaster_enable  = 50

role_obj_menu_jailer                    = 60
role_val_menu_jailer                    = 61
role_obj_label_jailer                   = 62
role_obj_label_jailer_desc              = 63
role_obj_label_jailer_report            = 64
role_obj_label_jailer_prisoner_count    = 65
role_obj_label_jailer_prisoner_value    = 66
role_obj_label_jailer_last_town         = 67
role_obj_label_jailer_reqs              = 68

role_val_menu_troop_1                   = 100 # Next several slots store troop_no's of each hero in the party so menus know who is selected.

###########################################################################################################################
#####                                            COMPANION BOOK READING                                               #####
###########################################################################################################################

REMOVE_BOOK                             = 0
COMPLETED_BOOK                          = 1