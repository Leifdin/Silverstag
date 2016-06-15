# Character Creation Presentation (1.0.2)
# Created by Windyplains.  Inspired by Dunde's character creation presentation in Custom Commander.



###########################################################################################################################
#####                                                MODULE SETTINGS                                                  #####
###########################################################################################################################

# DEBUG_CCP_general                      = 0   # This turns ON (1) or OFF (0) all of the debug messages.  Set to 2 will enable -very- verbose information.

# script_ccp_generate_skill_set modes
limit_to_stats                         = 0
equip_the_player                       = 1
summarize_skill_count                  = 2

###########################################################################################################################
#####                                              CHARACTER BACKGROUNDS                                              #####
###########################################################################################################################

# character backgrounds
cb_noble = 6
cb_merchant = 5
cb_guard = 4
cb_forester = 3
cb_nomad = 2
cb_thief = 1
cb_priest = 0

cb2_page = 8
cb2_apprentice = 7
cb2_urchin  = 6
cb2_steppe_child = 5
cb2_merchants_helper = 4
##diplomacy start+ add background constants
dplmc_cb2_mummer = 3
dplmc_cb2_courtier = 2
dplmc_cb2_noble = 1
dplmc_cb2_acolyte = 0
##diplomacy end+

# diplomacy start+ add background constants
floris_cb3_slaver = 12
floris_cb3_bandit = 11
floris_cb3_gladiator = 10
floris_cb3_thief = 9
dplmc_cb3_bravo = 8
dplmc_cb3_merc = 7
# diplomacy end+
cb3_poacher = 6
cb3_craftsman = 5
cb3_peddler = 4
# diplomacy start+ add background constants
dplmc_cb3_preacher = 3
# diplomacy end+
cb3_troubadour = 2
cb3_student = 1
cb3_squire = 0
cb3_lady_in_waiting = 0

floris_cb4_duty = 6
cb4_revenge = 5
cb4_loss    = 4
cb4_wanderlust =  3
##diplomacy start+ add background constants
dplmc_cb4_fervor = 2
##diplomacy end+
cb4_disown  = 1
cb4_greed  = 0

###########################################################################################################################
#####                                            PRESENTATION DEFINITIONS                                             #####
###########################################################################################################################
ccp_objects                            = "trp_tpe_presobj"
ccp_data                               = "trp_tpe_xp_table"

# Slots of CCP_OBJECTS
ccp_obj_button_done                    = 1
ccp_obj_button_default                 = 2
ccp_obj_button_random                  = 3
ccp_obj_label_menus                    = 4
ccp_obj_label_story                    = 5
ccp_obj_label_gender                   = 6
ccp_obj_label_father                   = 7
ccp_obj_label_earlylife                = 8
ccp_obj_label_later                    = 9
ccp_obj_label_reason                   = 10
ccp_obj_menu_gender                    = 11
ccp_obj_menu_father                    = 12
ccp_obj_menu_earlylife                 = 13
ccp_obj_menu_later                     = 14
ccp_obj_menu_reason                    = 15
ccp_obj_label_options                  = 16
ccp_obj_menu_trooptrees                = 17
ccp_val_menu_trooptrees                = 18
ccp_obj_checkbox_fogofwar              = 19
ccp_val_checkbox_fogofwar              = 20
ccp_obj_label_mtt                      = 21
ccp_obj_checkbox_gather_npcs           = 22
ccp_val_checkbox_gather_npcs           = 23
ccp_obj_menu_initial_region            = 24
ccp_val_menu_initial_region            = 25
ccp_obj_label_region                   = 26
ccp_obj_label_strength                 = 27
ccp_obj_stat_strength                  = 28
ccp_obj_label_agility                  = 29
ccp_obj_stat_agility                   = 30
ccp_obj_label_intelligence             = 31
ccp_obj_stat_intelligence              = 32
ccp_obj_label_charisma                 = 33
ccp_obj_stat_charisma                  = 34
ccp_obj_stat_gold                      = 35
ccp_obj_stat_renown                    = 36
ccp_obj_stat_weapon_onehand            = 37
ccp_obj_stat_weapon_twohand            = 38
ccp_obj_stat_weapon_polearm            = 39
ccp_obj_stat_weapon_archery            = 40
ccp_obj_stat_weapon_crossbow           = 41
ccp_obj_stat_weapon_throwing           = 42
ccp_obj_stat_container                 = 43
ccp_obj_button_back                    = 44
ccp_obj_menu_questreaction             = 45
ccp_val_menu_questreaction             = 46
ccp_obj_menu_mod_difficulty            = 47
ccp_val_menu_mod_difficulty            = 48
ccp_label_mod_difficulty               = 49

# Slots of CCP_DATA
# Slots 0-99 reserved.
ccp_item_storage_begin                 = 100
# Slots 101-120 reserved.
ccp_item_storage_end                   = 121
# Swadian items begin.
ccp_swadia_items_begin                 = 130
ccp_swadia_item_trade1                 = 130
ccp_swadia_item_trade2                 = 131
ccp_swadia_item_horse                  = 132
ccp_swadia_item_richhorse              = 133
ccp_swadia_item_shield                 = 134
ccp_swadia_item_instrument             = 135
ccp_swadia_item_poorboots              = 136
ccp_swadia_item_boots                  = 137
ccp_swadia_item_richboots              = 138
ccp_swadia_item_cloth                  = 139
ccp_swadia_item_dress                  = 140
ccp_swadia_item_armor                  = 141
ccp_swadia_item_gauntlets              = 142
ccp_swadia_item_hood                   = 143
ccp_swadia_item_helmet                 = 144
ccp_swadia_item_ladyhelmet             = 145
ccp_swadia_item_axe                    = 146
ccp_swadia_item_blunt                  = 147
ccp_swadia_item_dagger                 = 148
ccp_swadia_item_spear                  = 149
ccp_swadia_item_sword                  = 150
ccp_swadia_item_bow                    = 151
ccp_swadia_item_arrow                  = 152
ccp_swadia_item_throwing               = 153
ccp_swadia_items_end                   = 154
# slots 155-159 reserved for Swadia.
# Swadian items end.  Vaegir items begin.
ccp_vaegir_items_begin                 = 160
ccp_vaegir_item_trade1                 = 160
ccp_vaegir_item_trade2                 = 161
ccp_vaegir_item_horse                  = 162
ccp_vaegir_item_richhorse              = 163
ccp_vaegir_item_shield                 = 164
ccp_vaegir_item_instrument             = 165
ccp_vaegir_item_poorboots              = 166
ccp_vaegir_item_boots                  = 167
ccp_vaegir_item_richboots              = 168
ccp_vaegir_item_cloth                  = 169
ccp_vaegir_item_dress                  = 170
ccp_vaegir_item_armor                  = 171
ccp_vaegir_item_gauntlets              = 172
ccp_vaegir_item_hood                   = 173
ccp_vaegir_item_helmet                 = 174
ccp_vaegir_item_ladyhelmet             = 175
ccp_vaegir_item_axe                    = 176
ccp_vaegir_item_blunt                  = 177
ccp_vaegir_item_dagger                 = 178
ccp_vaegir_item_spear                  = 179
ccp_vaegir_item_sword                  = 180
ccp_vaegir_item_bow                    = 181
ccp_vaegir_item_arrow                  = 182
ccp_vaegir_item_throwing               = 183
ccp_vaegir_items_end                   = 184
# slots 185-189 reserved for Vaegir.
# Vaegir items end.  Khergit items begin.
ccp_khergit_items_begin                = 190
ccp_khergit_item_trade1                = 190
ccp_khergit_item_trade2                = 191
ccp_khergit_item_horse                 = 192
ccp_khergit_item_richhorse             = 193
ccp_khergit_item_shield                = 194
ccp_khergit_item_instrument            = 195
ccp_khergit_item_poorboots             = 196
ccp_khergit_item_boots                 = 197
ccp_khergit_item_richboots             = 198
ccp_khergit_item_cloth                 = 199
ccp_khergit_item_dress                 = 200
ccp_khergit_item_armor                 = 201
ccp_khergit_item_gauntlets             = 202
ccp_khergit_item_hood                  = 203
ccp_khergit_item_helmet                = 204
ccp_khergit_item_ladyhelmet            = 205
ccp_khergit_item_axe                   = 206
ccp_khergit_item_blunt                 = 207
ccp_khergit_item_dagger                = 208
ccp_khergit_item_spear                 = 209
ccp_khergit_item_sword                 = 210
ccp_khergit_item_bow                   = 211
ccp_khergit_item_arrow                 = 212
ccp_khergit_item_throwing              = 213
ccp_khergit_items_end                  = 214
# slots 215-219 reserved for Khergit.
# Khergit items end.  Nord items begin.
ccp_nord_items_begin                   = 220
ccp_nord_item_trade1                   = 220
ccp_nord_item_trade2                   = 221
ccp_nord_item_horse                    = 222
ccp_nord_item_richhorse                = 223
ccp_nord_item_shield                   = 224
ccp_nord_item_instrument               = 225
ccp_nord_item_poorboots                = 226
ccp_nord_item_boots                    = 227
ccp_nord_item_richboots                = 228
ccp_nord_item_cloth                    = 229
ccp_nord_item_dress                    = 230
ccp_nord_item_armor                    = 231
ccp_nord_item_gauntlets                = 232
ccp_nord_item_hood                     = 233
ccp_nord_item_helmet                   = 234
ccp_nord_item_ladyhelmet               = 235
ccp_nord_item_axe                      = 236
ccp_nord_item_blunt                    = 237
ccp_nord_item_dagger                   = 238
ccp_nord_item_spear                    = 239
ccp_nord_item_sword                    = 240
ccp_nord_item_bow                      = 241
ccp_nord_item_arrow                    = 242
ccp_nord_item_throwing                 = 243
ccp_nord_items_end                     = 244
# slots 245-249 reserved for Nord.
# Nord items end.  Rhodok items begin.
ccp_rhodok_items_begin                 = 250
ccp_rhodok_item_trade1                 = 250
ccp_rhodok_item_trade2                 = 251
ccp_rhodok_item_horse                  = 252
ccp_rhodok_item_richhorse              = 253
ccp_rhodok_item_shield                 = 254
ccp_rhodok_item_instrument             = 255
ccp_rhodok_item_poorboots              = 256
ccp_rhodok_item_boots                  = 257
ccp_rhodok_item_richboots              = 258
ccp_rhodok_item_cloth                  = 259
ccp_rhodok_item_dress                  = 260
ccp_rhodok_item_armor                  = 261
ccp_rhodok_item_gauntlets              = 262
ccp_rhodok_item_hood                   = 263
ccp_rhodok_item_helmet                 = 264
ccp_rhodok_item_ladyhelmet             = 265
ccp_rhodok_item_axe                    = 266
ccp_rhodok_item_blunt                  = 267
ccp_rhodok_item_dagger                 = 268
ccp_rhodok_item_spear                  = 269
ccp_rhodok_item_sword                  = 270
ccp_rhodok_item_bow                    = 271
ccp_rhodok_item_arrow                  = 272
ccp_rhodok_item_throwing               = 273
ccp_rhodok_items_end                   = 274
# slots 275-279 reserved for Rhodok.
# Rhodok items end.  Sarrand items begin.
ccp_sarrand_items_begin                = 280
ccp_sarrand_item_trade1                = 280
ccp_sarrand_item_trade2                = 281
ccp_sarrand_item_horse                 = 282
ccp_sarrand_item_richhorse             = 283
ccp_sarrand_item_shield                = 284
ccp_sarrand_item_instrument            = 285
ccp_sarrand_item_poorboots             = 286
ccp_sarrand_item_boots                 = 287
ccp_sarrand_item_richboots             = 288
ccp_sarrand_item_cloth                 = 289
ccp_sarrand_item_dress                 = 290
ccp_sarrand_item_armor                 = 291
ccp_sarrand_item_gauntlets             = 292
ccp_sarrand_item_hood                  = 293
ccp_sarrand_item_helmet                = 294
ccp_sarrand_item_ladyhelmet            = 295
ccp_sarrand_item_axe                   = 296
ccp_sarrand_item_blunt                 = 297
ccp_sarrand_item_dagger                = 298
ccp_sarrand_item_spear                 = 299
ccp_sarrand_item_sword                 = 300
ccp_sarrand_item_bow                   = 301
ccp_sarrand_item_arrow                 = 302
ccp_sarrand_item_throwing              = 303
ccp_sarrand_items_end                  = 304
# slots 305-309 reserved for Sarrand.
# Sarrand items end.