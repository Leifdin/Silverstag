# Custom Commissioned Items by Windyplains

## Non-Kit File Inclusions
# $gpu_data - Storage global for interfaces. (cci_presentations.py)
# $gpu_storage - Storage global for interfaces. (cci_presentations.py)
# $enable_popups - Sets if pop-up notifications will happen when an item is completed. (cci_scripts.py)
# gpu_<color> codes. (These can be found in "Source - Generic Presentation Utilities"\gpu_constants.py)
# Troop definitions ("trp_array_commission_item_no" -> "castle_end_blacksmith" in module_troops.py

## PARTY SLOTS
slot_center_commission_order           = 316  # This is a temporary value used to track how many commissions have been handled in this location.
slot_center_commission_counter         = 317  # This is a temporary value used to track of this center has any commissions.
slot_center_artisan_level_blacksmith   = 318  # This is a permanent value tracking the artisan crafter's level so it can go up and down.
slot_center_repairing_item_no          = 319  # This tracks the item no of the current item selected for repair.
slot_center_repairing_imod             = 320  # This tracks the item modifier of the current item selected for repair.
slot_center_repairing_progress         = 321  # This tracks how much work is left to be done on the currently selected item.
slot_center_commission_boost_duration  = 322  # This tracks how many hours remain to boost a center's production in a location.

## CORE LIMITS
CCI_GOBAL_COMMISSION_LIMIT             = 100  # This is the maximum number of commissions allowed in every location combined.
CCI_LOCAL_COMMISSION_LIMIT             = 5    # This is the maximum number of commissions allowed at a single location.
CCI_HOURLY_WORKDOWN                    = 25   # This is how many denars of price each hour reduces towards completing an item.
CCI_WORKDOWN_PERIODICITY               = 4    # This is how many hours pass between each processing of the commission list.  The lower the number the more CPU lag you'll generate on the world map.
                                              # NOTE: You -must- change the simple trigger periodicity to match this value in cci_simple_triggers.py labeled for "Commission Advancement".
CCI_MARKUP_PERCENTAGE                  = 350  # This is a % value for how much an item+imod's standard value is marked up for commissioning.
CCI_FIRST_ITEM          = "itm_sumpter_horse" # This is the first item in module_items you want people to be able to commission.
CCI_LAST_ITEM           = "itm_items_end"     # This is the last valid item in module_items you want people to be able to commission.
CCI_UPFRONT_COST                       = 50   # (0 - 100%) This is how much of the commission cost must be paid at the time of request.
CCI_ABANDONED_DAYS_LIMIT               = 60   # If a completed item has been left uncollected for this many days it is removed from the queue.
CCI_MAXIMUM_ARTISAN_LEVEL              = 20   # This is the maximum level a crafting artisan can rank up to and gain any benefits.
CCI_XP_GAIN_REPAIR_TICK                = 8    # The artisan blacksmith gains this much experience each tick on repair work.
CCI_XP_GAIN_COMMISSION_TICK            = 15   # The artisan blacksmith gains this much experience each tick on commission work.
CCI_XP_GAIN_COMPLETION_MULTIPLIER      = 10   # (This) x (CCI_HOURLY_WORKDOWN) is gained as experience by the artisan blacksmith when any work is completed.

## MODULE PREFERENCE SETTINGS
CCI_SETTING_USE_REGIONAL_FLAGS         = 0    # (0 - No / 1 - Yes) Only display items flagged for this region in the center you're commissioning an item from.
CCI_SETTING_UNIQUES_COMMISSIONABLE     = 0    # (0 - No / 1 - Yes) If enabled, this allows unique items to be commissioned directly.
CCI_SETTING_LIMIT_TO_MERCHANDISE       = 1    # (0 - No / 1 - Yes) If enabled, only items flagged itp_merchandise will be commissionable.
CCI_SETTING_HORSES_COMMISSIONABLE      = 0    # (0 - No / 1 - Yes) If enabled, horses may be comissioned directly.
CCI_SETTING_WORKDOWN_METHOD            = 0    # (CONSTANTS LISTED BELOW)
CCI_METHOD_SEQUENTIAL              = 0    # Causes all commissions at a location to be worked in order one at a time.
CCI_METHOD_PARALLEL                = 1    # Causes all commissions at a location to be worked at the same time. (Disabled)

## ARRAY DEFINITIONS
CCI_ARRAY_ITEM_NO                      = "trp_array_commission_item_no"
CCI_ARRAY_IMOD                         = "trp_array_commission_imod"
CCI_ARRAY_STATUS                       = "trp_array_commission_status"
CCI_ARRAY_COST                         = "trp_array_commission_cost"
CCI_ARRAY_LOCATION                     = "trp_array_commission_location"
CCI_ARRAY_ABANDON_TIMER                = "trp_array_commission_abandon"
# EVENT LOG
CCI_LOG_EVENT                          = "trp_array_commission_log_event"
CCI_LOG_ITEM_NO                        = "trp_array_commission_log_item_no"
CCI_LOG_IMOD                           = "trp_array_commission_log_imod"
CCI_LOG_LOCATION                       = "trp_array_commission_log_location"
CCI_LOG_DATE                           = "trp_array_commission_log_date"

## ROYAL BLACKSMITHS
cci_town_blacksmiths_begin             = "trp_town_1_blacksmith"
cci_town_blacksmiths_end               = "trp_castle_1_blacksmith"
cci_castle_blacksmiths_begin           = "trp_castle_1_blacksmith"
cci_castle_blacksmiths_end             = "trp_castle_end_blacksmith"
cci_royal_blacksmiths_begin            = cci_town_blacksmiths_begin
cci_royal_blacksmiths_end              = cci_castle_blacksmiths_end

CCI_EVENT_LOG_MAXIMUM_ENTRIES          = 500  # Compared against $cci_event_log_entries for resetting the event log.
## LOG EVENTS
CCI_EVENT_UNDEFINED                    = 0
CCI_EVENT_COMMISSION_COMPLETED         = 1 # TRIGGER: Occurs when a commissioned item is completed. (done)
CCI_EVENT_REPAIR_COMPLETED             = 2 # TRIGGER: Occurs when an item in the artisan's repair inventory is completed.
CCI_EVENT_UPGRADE_COMPLETED            = 3 # TRIGGER: Occurs when an item in the artisan's repair inventory receives a free imod upgrade.
CCI_EVENT_ARTISAN_LEVELED              = 4 # TRIGGER: Occurs during experience gains for the artisan if a level up is detected. (done)
CCI_EVENT_ARTISAN_SLAIN                = 5 # TRIGGER: Occurs when the kill script is called.  Generally this happens in sieges. (done)
CCI_EVENT_LOG_RESET                    = 6 # TRIGGER: Occurs when the total number of valid events is reached to restart the list. (done)
CCI_EVENT_LOG_PRODUCTION_BOOST_BEGIN   = 7 # TRIGGER: You spend an emblem to boost production in an area.
CCI_EVENT_LOG_PRODUCTION_BOOST_END     = 8 # TRIGGER: The duration for production boost in a location runs out.
CCI_EVENT_COMMISSIONS_RESET            = 9 # TRIGGER: The list all UI reset option was used.
# ...
CCI_EVENT_LOG_TYPES_END                = 9

# imod_plain = 0
# imod_cracked = 1
# imod_rusty = 2
# imod_bent = 3
# imod_chipped = 4
# imod_battered = 5
# imod_poor = 6
# imod_crude = 7
# imod_old = 8
# imod_cheap = 9
# imod_fine = 10
# imod_well_made = 11
# imod_sharp = 12
# imod_balanced = 13
# imod_tempered = 14
# imod_deadly = 15
# imod_exquisite = 16
# imod_masterwork = 17
# imod_heavy = 18
# imod_strong = 19
# imod_powerful = 20
# imod_tattered = 21
# imod_ragged = 22
# imod_rough = 23
# imod_sturdy = 24
# imod_thick = 25
# imod_hardened = 26
# imod_reinforced = 27
# imod_superb = 28
# imod_lordly = 29
# imod_lame = 30
# imod_swaybacked = 31
# imod_stubborn = 32
# imod_timid = 33
# imod_meek = 34
# imod_spirited = 35
# imod_champion = 36
# imod_fresh = 37
# imod_day_old = 38
# imod_two_day_old = 39
# imod_smelling = 40
# imod_rotten = 41
# imod_large_bag = 42


###########################################################################################################################
#####                                              PRESENTATION OBJECTS                                               #####
#####                                                                                                                 #####
##### WARNING : If you alter this stuff you'll break the interfaces associated with this sub-mod.                     #####
###########################################################################################################################
CCI_OBJECTS                       = "trp_cci_presobjects"


# $cci_mode Types
CCI_MODE_ARTISAN_INFO             = 0
CCI_MODE_COMMISSION_ITEM          = 1
CCI_MODE_LIST_ALL_COMMISSIONS     = 2
CCI_MODE_REPAIR_ITEMS             = 3
CCI_MODE_EVENT_LOG                = 4
CCI_MODE_EMBLEM_OPTIONS           = 5
# CCI_MODE_TROOP_INFO               = 6

CCI_STARTING_SCREEN               = CCI_MODE_COMMISSION_ITEM

# Display Groups ("$temp")
CCI_GROUP_ONE_HANDED              = 0
CCI_GROUP_TWO_HANDED              = 1
CCI_GROUP_POLEARMS                = 2
CCI_GROUP_RANGED_WEAPONS          = 3
CCI_GROUP_AMMUNITION              = 4
CCI_GROUP_SHIELDS                 = 5
CCI_GROUP_HELMETS                 = 6
CCI_GROUP_BODY                    = 7
CCI_GROUP_BOOTS                   = 8
CCI_GROUP_HANDS                   = 9
CCI_GROUP_MOUNTS                  = 10
CCI_GROUP_BOOKS                   = 11


### UI - CORE ELEMENTS ###
cci_obj_main_title                = 1
cci_obj_button_done               = 2
cci_obj_main_title2               = 3
cci_obj_button_artisan            = 4
cci_obj_button_commission_item    = 5
cci_obj_button_list_commissions   = 6
cci_obj_container_1               = 7
cci_obj_button_repair_items       = 8
cci_obj_button_event_log          = 9
cci_obj_button_emblem_options     = 10

### UI - ITEM COMMISSIONING ###
# cci_obj_main_title                = 101
# cci_obj_button_done               = 102
cci_obj_title_type                = 103
cci_obj_title_commissions         = 104
cci_obj_label_warning_1           = 105
cci_obj_container_imod_list       = 106
cci_obj_container_commissions     = 107
cci_val_selected_item_no          = 108
cci_val_selected_imod             = 109
cci_obj_label_selected_item       = 110
cci_obj_label_selected_imod       = 111
cci_obj_image_selected_item       = 112
cci_obj_button_commission         = 113
cci_obj_container_selected_item   = 114
cci_val_selected_price            = 115
cci_obj_label_selected_price      = 116
cci_obj_label_selected_duration   = 117
cci_obj_container_items           = 118
cci_obj_button_item_0             = 119
cci_obj_button_item_1             = 120
cci_obj_button_item_2             = 121
cci_obj_button_item_3             = 122
cci_obj_button_item_4             = 123
cci_obj_button_item_5             = 124
# ...
cci_val_item_1_entry_slot         = 130
cci_val_item_2_entry_slot         = 131
cci_val_item_3_entry_slot         = 132
cci_val_item_4_entry_slot         = 133
cci_val_item_5_entry_slot         = 134
# ...
cci_val_item_1_button_type        = 140
cci_val_item_2_button_type        = 141
cci_val_item_3_button_type        = 142
cci_val_item_4_button_type        = 143
cci_val_item_5_button_type        = 144
# ...

# Spaces between these values are reserved.
cci_obj_checkbox_modifiers_begin  = 300
cci_val_checkbox_modifiers_begin  = 350
cci_val_checkbox_modifiers_end    = 400

### UI - LIST ALL ITEMS ###
cci2_obj_items_begin              = 100
cci2_obj_items_end                = 200
cci2_val_items_begin              = 200
cci2_val_items_end                = 300
cci2_obj_button_reset_requests    = 399

### UI - ARTISAN INFORMATION ###
cci3_obj_button_add_xp              = 100
cci3_obj_button_remove_xp           = 101
cci3_obj_button_reset_xp            = 102

### UI - EVENT LOG ###
cci4_obj_button_display_toggle      = 100
cci4_val_display_setting            = 101

### UI - EMBLEM OPTIONS ###
cci5_obj_button_option_1            = 100
cci5_obj_button_option_2            = 101
cci5_obj_button_option_3            = 102
cci5_obj_button_debug_gain_emblem   = 103

