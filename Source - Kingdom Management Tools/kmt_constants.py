# Kingdom Management Tools (1.0.1) by Windyplains
# Released --/--/--


###########################################################################################################################
#####                                                MODULE SETTINGS                                                  #####
###########################################################################################################################

#kmt_debug                              = 0   # This turns ON (1) or OFF (0) all of the debug messages.  Set to 2 will enable -very- verbose information.

## FACTION SLOTS
slot_faction_title_style_default       = 196 # (0 or 1) Stores whether a faction's title is kept before (0) or after (1) their name.
slot_faction_title_style               = 197 # (0 or 1) Stores whether a faction's title is kept before (0) or after (1) their name.

###########################################################################################################################
#####                                              FACTION DEFINITIONS                                                #####
###########################################################################################################################
kmt_kingdom_0                          = 0 # "fac_player_supporters_faction"
kmt_kingdom_1                          = 1 # "fac_kingdom_1"
kmt_kingdom_2                          = 2 # "fac_kingdom_2"
kmt_kingdom_3                          = 3 # "fac_kingdom_3"
kmt_kingdom_4                          = 4 # "fac_kingdom_4"
kmt_kingdom_5                          = 5 # "fac_kingdom_5"
kmt_kingdom_6                          = 6 # "fac_kingdom_6"

###########################################################################################################################
#####                                            PRESENTATION DEFINITIONS                                             #####
###########################################################################################################################
KMT_OBJECTS                            = "trp_tpe_presobj"
kmt_objects                            = "trp_tpe_presobj"
kmt_data                               = "trp_tpe_xp_table"
kmt_line_step                          = 20
kmt_text_size                          = 75

kmt_ai_enemy_threshold                 = -7
kmt_ai_friend_threshold                = 24

# Slots of KMT_OBJECTS
kmt_obj_button_done                    = 1
kmt_obj_main_container                 = 2
kmt_obj_faction_menu                   = 3
kmt_val_faction_menu                   = 4
kmt_obj_main_title                     = 5
kmt_obj_remove_backgrounds             = 6
kmt_val_remove_backgrounds             = 7
kmt_val_hide_map                       = 8
kmt_val_hide_background                = 9

# Dynamic slot storage
kmt_val_kingdoms_begin                 = 100
# reserve about 20 slots after this.


###########################################################################################################################
#####                                                AFFAIRS OF STATE                                                 #####
###########################################################################################################################

# $kmt_mode Types
KMT_MODE_GENERAL_INFO             = 0  # General Information (Show unassigned fiefs, landless lords, lords near defection)
KMT_MODE_FIEF_ELECTIONS           = 1  # Elections for Unassigned Fiefs
KMT_MODE_FIEF_EXCHANGE            = 2  # Fief Exchange
KMT_MODE_VASSAL_GIFTS             = 3  # Sending a gift to a vassal
KMT_MODE_VASSAL_TITLES            = 4  # Custom vassal titles
KMT_MODE_VASSAL_PRISONERS         = 5  # View vassal prisoners and trade for them

KMT_STARTING_SCREEN               = KMT_MODE_GENERAL_INFO

### UI - CORE ELEMENTS ###
kmt1_obj_main_title                = 1
kmt1_obj_button_done               = 2
kmt1_obj_main_title2               = 3
kmt1_obj_button_general_info       = 4
kmt1_obj_button_fief_election      = 5
kmt1_obj_button_fief_exchange      = 6
kmt1_obj_button_vassal_gifts       = 7
kmt1_obj_button_vassal_titles      = 8
kmt1_obj_button_vassal_prisoners   = 9
kmt1_obj_container_1               = 15


### UI - FIEF EXCHANGE ###
## Option Types
KMT_OPTION_NONE                    = 0
KMT_OPTION_FIEF                    = 1
KMT_OPTION_MONEY                   = 2
KMT_OPTION_KINGS_MONEY             = 3

## UI Elements
kmt3_obj_portrait_lord_left        = 100
kmt3_obj_portrait_lord_right       = 101
kmt3_obj_menu_lord_left            = 102
kmt3_val_menu_lord_left            = 103
kmt3_obj_menu_lord_right           = 104
kmt3_val_menu_lord_right           = 105
kmt3_val_lord_left                 = 106
kmt3_val_lord_right                = 107
kmt3_obj_button_make_offer         = 108
# Option 1 - Left
kmt3_val_left_opt_1_type           = 110
kmt3_obj_left_opt_1                = 111
kmt3_val_left_opt_1                = 112
kmt3_obj_left_opt_1_type           = 113
kmt3_obj_left_opt_1_slider_label   = 114
kmt3_obj_left_opt_1_info_1         = 115
kmt3_obj_left_opt_1_info_2         = 116
kmt3_obj_left_bold_effect          = 117
# Option 2 - Left
kmt3_val_left_opt_2_type           = 120
kmt3_obj_left_opt_2                = 121
kmt3_val_left_opt_2                = 122
kmt3_obj_left_opt_2_type           = 123
# Option 3 - Left
kmt3_val_left_opt_3_type           = 130
kmt3_obj_left_opt_3                = 131
kmt3_val_left_opt_3                = 132
kmt3_obj_left_opt_3_type           = 133
# Option 4 - Left
kmt3_val_left_opt_4_type           = 140
kmt3_obj_left_opt_4                = 141
kmt3_val_left_opt_4                = 142
kmt3_obj_left_opt_4_type           = 143
# Option 5 - Left
kmt3_val_left_opt_5_type           = 150
kmt3_obj_left_opt_5                = 151
kmt3_val_left_opt_5                = 152
kmt3_obj_left_opt_5_type           = 153
# Option 1 - Right
kmt3_val_right_opt_1_type          = 160
kmt3_obj_right_opt_1               = 161
kmt3_val_right_opt_1               = 162
kmt3_obj_right_opt_1_type          = 163
# Option 2 - Right
kmt3_val_right_opt_2_type          = 170
kmt3_obj_right_opt_2               = 171
kmt3_val_right_opt_2               = 172
kmt3_obj_right_opt_2_type          = 173
# Option 3 - Right
kmt3_val_right_opt_3_type          = 180
kmt3_obj_right_opt_3               = 181
kmt3_val_right_opt_3               = 182
kmt3_obj_right_opt_3_type          = 183
# Option 4 - Right
kmt3_val_right_opt_4_type          = 190
kmt3_obj_right_opt_4               = 191
kmt3_val_right_opt_4               = 192
kmt3_obj_right_opt_4_type          = 193
# Option 5 - Right
kmt3_val_right_opt_5_type          = 200
kmt3_obj_right_opt_5               = 201
kmt3_val_right_opt_5               = 202
kmt3_obj_right_opt_5_type          = 203
# Generic values
kmt3_val_left_fief_count           = 210
kmt3_val_right_fief_count          = 211
kmt3_obj_left_rating               = 212
kmt3_val_left_rating               = 213
kmt3_obj_right_rating              = 214
kmt3_val_right_rating              = 215
kmt3_obj_container_left_options    = 216
kmt3_obj_container_right_options   = 217
kmt3_obj_button_force_exchange     = 218
kmt3_obj_left_label_forced_loss    = 219
kmt3_val_left_label_forced_loss    = 220
kmt3_obj_right_label_forced_loss   = 221
kmt3_val_right_label_forced_loss   = 222
kmt3_val_left_best_fief_type       = 223
kmt3_val_left_best_fief_count      = 224
kmt3_val_right_best_fief_type      = 225
kmt3_val_right_best_fief_count     = 226
# Left / Right Fief Lists
kmt3_val_left_fiefs_begin          = 300
kmt3_val_left_fiefs_end            = 350
kmt3_val_right_fiefs_begin         = 351
kmt3_val_right_fiefs_end           = 400
# Left / Right Lord Selector Storage
kmt3_val_lord_selector_begin       = 400
kmt3_val_lord_selector_end         = 500


### UI - VASSAL TITLES ###
# Script "" functions
KMT_TITLE_FUNCTION_SET             = 0
KMT_TITLE_FUNCTION_STORE           = 1
# Interface Constants
kmt5_obj_textbox_landless_lords    = 100
kmt5_obj_textbox_village_lords     = 101
kmt5_obj_textbox_castle_lords      = 102
kmt5_obj_textbox_town_lords        = 103
kmt5_obj_textbox_marshal           = 104
kmt5_obj_textbox_king              = 105
kmt5_obj_textbox_landless_ladies   = 106
kmt5_obj_textbox_village_ladies    = 107
kmt5_obj_textbox_castle_ladies     = 108
kmt5_obj_textbox_town_ladies       = 109
kmt5_obj_textbox_marshal_lady      = 110
kmt5_obj_textbox_queen             = 111
kmt5_obj_button_load_titles        = 112
kmt5_obj_button_save_titles        = 113
kmt5_obj_button_default_titles     = 114
kmt5_obj_faction_selector          = 115
kmt5_val_faction_selector          = 116
kmt5_val_selected_faction          = 117
kmt5_obj_textbox_prince            = 118
kmt5_obj_textbox_princess          = 119
kmt5_obj_button_delete_titles      = 120
kmt5_obj_menu_title_style          = 121
kmt5_val_menu_title_style          = 122


### UI - VASSAL PRISONERS ###
kmt6_obj_container_captive_list    = 100
kmt6_obj_container_selected_lord   = 101
kmt6_obj_container_offered         = 102
# kmt6_obj_container_requested       = 103
kmt6_obj_container_chat            = 104
kmt6_obj_button_confirm            = 105
kmt6_obj_button_offer              = 106
