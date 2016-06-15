# Enhanced Diplomacy Options (1.0) by Windyplains

# DEBUG_DIPLOMACY               = 0
# DEBUG_DIPLOMACY_PATROLS       = 0
# DEBUG_TREASURY                = 0

###########################################################################################################################
#####                                               MESSAGE FILTER                                                    #####
###########################################################################################################################

# Diplomacy contexts
context_party                 = 1
context_center                = 2
context_faction               = 3
context_troop                 = 4

###########################################################################################################################
#####                                               ADVISOR SYSTEM                                                    #####
###########################################################################################################################
# PARTY SLOTS
slot_center_steward           = 440
advisors_begin                = slot_center_steward
slot_center_advisor_war       = 441 # Captain of the Guard
# slot_center_advisor_finance   = 442
advisors_end                  = 442
# Patrols
slot_center_patrol_party_1    = 447  # (party #) This tracks the 1st patrol party of a walled center.
slot_center_patrol_party_2    = 448  # (party #) This tracks the 2nd patrol party of a walled center.
slot_center_patrol_party_3    = 449  # (party #) This tracks the 3rd patrol party of a walled center.
slot_center_recruit_pool      = 450  # (integer) This keeps track of how many recruits from nearby "bound" villages a walled center has collected prior to turning them into basic recruit troops.
slot_center_recruiting        = 451  # (0 - OFF / 1 - ON) With this enabled a center (that has a Captain of the Guard) will attempt to automatically recruit new troops to its garrison.
slot_center_treasury          = 453  # (integer) This holds the current wealth stored at this center for upgrading.
slot_center_income_to_treasury = 454 # (integer) This holds how much money is weekly diverted to the treasury.
slot_center_veteran_pool     = 457  # (integer) This tracks how many nobles are available for training. (Player)
slot_center_intelligence      = 458  # (intenger 0-10) Tracks the amount of information you should be able to retrieve about a location.
slot_center_veteran_ai       = 459  # (integer) This tracks how many nobles are available for training. (AI)

slot_center_patrols_begin     = slot_center_patrol_party_1 # = 447
slot_center_patrols_end       = slot_center_recruit_pool
slot_party_patrol_size        = slot_center_patrol_party_1 # = 447
slot_party_patrol_training    = slot_center_patrol_party_2 # = 448
slot_party_patrol_culture     = slot_center_patrol_party_3 # = 449
slot_party_patrol_home        = slot_center_recruit_pool   # 450
slot_party_patrol_upkeep      = slot_center_recruiting     # 451

# TROOP SLOTS
slot_troop_unique_location    = 298  # This represents the center # where a unique troop can be recruited from.
slot_troop_advisor_station    = 328  # This represents the center # where a companion is assigned to. (Applicable to companions)
slot_troop_advisor_role       = 329  # This represents the center slot # a companion is assigned to. (Applicable to companions)
slot_troop_relation_from_fief = 330  # This holds the % chance of a lord gaining or losing relation with their king weekly. (Applicable to lords & promoted companions)
slot_troop_upgrade_chance_1   = 331  # This holds the 0-100% chance of a troop upgrading to path 1. (Applicable to standard troops)
slot_troop_upgrade_chance_2   = 332  # This holds the 0-100% chance of a troop upgrading to path 2. (Applicable to standard troops)
slot_troop_recruit_type       = 333  # This sets up the type of recruit required to hire this troop.
slot_troop_purchase_cost      = 334  # This contains the direct purchasing cost

###########################################################################################################################
#####                                             GENERIC CONSTANTS                                                   #####
###########################################################################################################################
DIPLOMACY_TOURNAMENT_HOSTING_COST  = 8000

# Recruit types
STRT_PEASANT                       = 0
STRT_NOBLEMAN                      = 1
STRT_MERCENARY                     = 2
STRT_SLAVE                         = 3 # These units should only cost what it takes to feed them.

# Treasury requests using script "cf_diplomacy_treasury_verify_funds".
TREASURY_FUNDS_AVAILABLE           = 0
TREASURY_FUNDS_INSUFFICIENT        = 1

FUND_FROM_TREASURY                 = 0
FUND_FROM_PLAYER                   = 1
FUND_FROM_EITHER                   = 2 # This will prioritize the player first.
FUND_FROM_TREASURY_TO_PLAYER       = 3

# Script "diplomacy_remove_advisor"
ADVISOR_FLEES                      = 0  # When removed the advisor will not rejoin the party and will be one of the free floating companions.
ADVISOR_RETURNS_TO_PARTY           = 1  # When removed the advisor will immediately rejoin the party.
ADVISOR_RETURN_IF_NEARBY           = 2  # When removed the advisor will attempt to rejoin the party if nearby, otherwise becomes free floating.
ADVISOR_BEGIN_RETURN_MISSION       = 3  # When removed the advisor will attempt to find the party and takes as long as he is distant.

DIPLOMACY_TEMP_ARRAY               = "trp_relative_of_merchants_end" # This is used to store party #'s when vassals are given troops.  So those parties can be cleaned out by a simple trigger.
###########################################################################################################################
#####                                             DISPLAY RECOLORING                                                  #####
###########################################################################################################################

###########################################################################################################################
#####                                           EXPANDED PRISONER DIALOG                                              #####
###########################################################################################################################

###########################################################################################################################
#####                                             REVISED MORALE SYSTEM                                               #####
###########################################################################################################################

## MORALE LOG - REASONS
PMR_UNDEFINED                 = 0
PMR_PARTY_NOT_FED             = 1
PMR_PARTY_DEFEATED            = 2
PMR_PARTY_VICTORY             = 3
PMR_DAILY_SHIFT               = 4
PMR_FRIENDLY_FIRE             = 5
PMR_RETREAT                   = 6
PMR_RECRUITED_PRISONERS       = 7
PMR_SACRIFICED_MEN            = 8
PMR_LOOTED_VILLAGE            = 9
PMR_ATTENDED_FEAST            = 10

## MORALE LOG - ENTRY TYPES
PMR_LOG_DATE                  = "trp_pmr_log_date"
PMR_LOG_REASON                = "trp_pmr_log_reason"
PMR_LOG_CHANGE                = "trp_pmr_log_change"
PMR_LOG_MORALE                = "trp_pmr_log_morale"
PMR_LOG_IDEAL                 = "trp_pmr_log_ideal"

## Party Size
morale_max_party_size         = 46
morale_min_party_size         = 0
morale_party_size_factor      = 6  # +1 morale per this many troops.
## Leadership bonuses
morale_king_leadership_bonus  = 6
morale_basic_leadership_bonus = 4
## Party Unity
morale_max_party_unity        = 61
morale_min_party_unity        = -60
## Battle Weariness
morale_max_battle_weariness   = 16
morale_min_battle_weariness   = -60
morale_weariness_recovery_max = 6
morale_weariness_hour_spacing = 16
morale_weariness_penalty      = -8
## Constants used for querrying info from script "diplomacy_get_battle_weariness_factor"
WEARINESS_PENALTY             = 1  # Returns how much ideal morale is lost per battle.
WEARINESS_RECOVERY_RATE       = 2  # Returns how much you should recover per 4 hours.
WEARINESS_RECOVERY_LIMIT      = 3  # Returns the maximum recovery rate you can achieve.
WEARINESS_RECOVERY_SPACING    = 4  # Returns the intervals between weariness recovery procs.

###########################################################################################################################
#####                                                 PATROL SYSTEM                                                   #####
###########################################################################################################################
# Functions of script "diplomacy_patrol_functions"
PATROL_GENERATE               = 0
PATROL_DISBAND                = 1
PATROL_UPGRADE_TROOPS         = 2
PATROL_RECRUIT_TROOPS         = 3
PATROL_DETERMINE_COST         = 4
PATROL_PAYMENT_DUE            = 5
PATROL_DETERMINE_PATROL_NO    = 6
PATROL_JOIN_COMBAT            = 7
PATROL_OFFLOAD_PRISONERS      = 8
PATROL_REPORT_STATUS          = 9
PATROL_GET_SUMMARY            = 10
PATROL_TRIM_EXTRAS            = 11
PATROL_RESET_AI_THINKING      = 12
PATROL_ACCOMPANY_OWNER        = 13
PATROL_DUMP_PRISONERS         = 14
PATROL_RESET_CENTER_SLOTS     = 15

# slot_party_patrol_size types
patrol_size_small             = 0 # 10 men
patrol_size_medium            = 1 # 20 men
patrol_size_large             = 2 # 30 men

# slot_party_patrol_training types
patrol_training_poor          = 1
patrol_training_average       = 2
patrol_training_good          = 3
patrol_training_elite         = 4

###########################################################################################################################
#####                                          KINGDOM MANAGEMENT SYSTEM                                              #####
###########################################################################################################################
KMS_OBJECTS                         = "trp_tpe_presobj"

### FACTION SLOTS ###

# POLICY SETTINGS
diplomacy_policies_begin             = 200
slot_faction_policy_culture_focus    = 200
slot_faction_policy_mil_diversity    = 201 # Not implemented.
slot_faction_policy_border_control   = 202
slot_faction_policy_slavery          = 203
slot_faction_policy_desertion        = 204 # Not implemented.
# NOTE: Reserve several slots here for future policy sliders.
diplomacy_policies_end               = 205

# ROYAL DECREES
diplomacy_decrees_begin              = 210
slot_faction_decree_conscription     = 210
slot_faction_decree_laws_commons     = 211
slot_faction_decree_laws_nobles      = 212
slot_faction_decree_war_taxes        = 213
slot_faction_decree_sanitation       = 214
slot_faction_decree_reconstruction   = 215
slot_faction_decree_executions       = 216
# NOTE: Reserve several slots here for royal decree options.
diplomacy_decrees_end                = 217

# Minor Data
diplomacy_policy_data_begin          = 225
slot_faction_village_recruits        = 225
slot_faction_desertion_factor        = 226
slot_faction_desertion_threshold     = 227
slot_faction_unity_top_faction       = 228
slot_faction_unity_bottom_faction    = 229
slot_faction_unity_top_nonfaction    = 230
slot_faction_unity_bottom_nonfaction = 231
slot_faction_unity_top_mercs         = 232
slot_faction_unity_bottom_mercs      = 233
slot_faction_center_income           = 234
slot_faction_army_size_adjust        = 235
slot_faction_patrol_size_adjust      = 236
slot_faction_raw_material_discount   = 237
slot_faction_price_of_slaves         = 238
slot_faction_slaver_availability     = 239
slot_faction_party_morale_adjust     = 240
slot_faction_improvement_time        = 241
slot_faction_village_recruit_tier    = 242
slot_faction_castle_recruit_tier     = 243
slot_faction_labor_discount          = 244
slot_faction_troop_wages             = 245
slot_faction_improvement_cost        = 246
slot_faction_march_unrest            = 247
slot_faction_march_tolerance         = 248
slot_faction_prosperity_ideal        = 249
slot_faction_center_tariffs          = 250
slot_faction_prosperity_real         = 251
slot_faction_prosperity_recovery     = 252
slot_faction_fief_relation           = 253
slot_faction_lrep_martial_relation   = 254
slot_faction_lrep_quarrelsome_relation = 255
slot_faction_lrep_selfrighteous_relation = 256
slot_faction_lrep_cunning_relation      = 257
slot_faction_lrep_debauched_relation    = 258
slot_faction_lrep_goodnatured_relation  = 259
slot_faction_lrep_upstanding_relation   = 260
slot_faction_lrep_roguish_relation      = 261
slot_faction_lrep_benefactor_relation   = 262
slot_faction_lrep_custodian_relation    = 263
slot_faction_bandit_infest_chance       = 264
slot_faction_right_to_rule              = 265
slot_faction_weariness_battle_penalty   = 266 # Added in v0.16
slot_faction_weariness_recovery_max     = 267 # Added in v0.16
slot_faction_weariness_recovery_rate    = 268 # Added in v0.16
slot_faction_center_recruitment_factor  = 269 # Added in v0.24
diplomacy_policy_data_end                = 270

# POLICY STAGES - Generically used by all policies.
POLICY_STAGE_LEFT_2                      = 0
POLICY_STAGE_LEFT_1                      = 1
POLICY_STAGE_NEUTRAL                     = 2
POLICY_STAGE_RIGHT_1                     = 3
POLICY_STAGE_RIGHT_2                     = 4
POLICY_MAX                               = 5

# SYNC Functions
STORE_TO_PRESENTATION                    = 0
STORE_TO_FACTION                         = 1

# General Defaults
diplomacy_default_slaver_availability    = 20
diplomacy_conscription_troop_multiplier  = 2
diplomacy_conscription_relation_loss     = -2
diplomacy_conscritpion_prosperity_loss   = -2
diplomacy_war_taxation_prosperity_loss   = -5
diplomacy_war_taxation_recovery_penalty  = 2   # Divides recovery gain by 2 so cuts it by 50%.
diplomacy_reconstruction_recovery_bonus  = 3   # Recovery value multiplied by this giving a +200% rate increase.

# TOOLTIP DEFINITIONS
TOOLTIP_DIPLOMACY_SUMMARY                = 1
TOOLTIP_POLICY_CULTURAL_FOCUS            = 2
TOOLTIP_POLICY_MILITARY_DIVERSITY        = 3
TOOLTIP_POLICY_BORDER_CONTROLS           = 4
TOOLTIP_POLICY_SLAVERY                   = 5
TOOLTIP_POLICY_TROOP_DESERTION           = 6
TOOLTIP_DECREE_CONSCRIPTION              = 7
TOOLTIP_DECREE_CODE_OF_LAW_COMMON        = 8
TOOLTIP_DECREE_CODE_OF_LAW_NOBLE         = 9
TOOLTIP_DECREE_WAR_TAXATION              = 10
TOOLTIP_DECREE_SANITATION                = 11
TOOLTIP_DECREE_RECONSTRUCTION            = 12
TOOLTIP_DECREE_PUBLIC_EXECUTIONS         = 13

### PRESENTATION SLOTS (KMS_OBJECTS) ###
kms_val_faction_no                       = 1
kms_val_policies_begin                   = 2
kms_val_policy_culture_focus             = 2
kms_val_policy_mil_diversity             = 3
kms_val_policy_border_control            = 4
kms_val_policy_slavery                   = 5
kms_val_policy_desertion                 = 6
kms_val_policies_end                     = 7
# Reserve 7 - 11 for policies
kms_val_decrees_begin                    = 12
kms_val_decree_conscription              = 12
kms_val_decree_laws_commons              = 13
kms_val_decree_laws_nobles               = 14
kms_val_decree_war_taxes                 = 15
kms_val_decree_sanitation                = 16
kms_val_decree_reconstruction            = 17
kms_val_decree_executions                = 18
kms_val_decrees_end                      = 19
# Reserve 20 - 26 for decrees
kms_val_data_begin                       = 27
kms_val_data_village_recruits            = 27
kms_val_data_desertion_factor            = 28
kms_val_data_desertion_threshold         = 29
kms_val_data_unity_top_faction           = 30
kms_val_data_unity_bot_faction           = 31
kms_val_data_unity_top_nonfaction        = 32
kms_val_data_unity_bot_nonfaction        = 33
kms_val_data_unity_top_mercs             = 34
kms_val_data_unity_bot_mercs             = 35
kms_val_data_center_income               = 36
kms_val_data_army_size_adjust            = 37
kms_val_data_patrol_size                 = 38
kms_val_data_raw_material_discount       = 39
kms_val_data_price_of_slaves             = 40
kms_val_data_slaver_availability         = 41
kms_val_data_party_morale                = 42
kms_val_data_improvement_time            = 43
kms_val_data_village_recruit_tier        = 44
kms_val_data_castle_recruit_tier         = 45
kms_val_data_labor_discount              = 46
kms_val_data_troop_wages                 = 47
kms_val_data_improvement_cost            = 48
kms_val_data_march_unrest                = 49
kms_val_data_march_tolerance             = 50
kms_val_data_prosperity_ideal            = 51
kms_val_data_center_tariffs              = 52
kms_val_data_prosperity_real             = 53
kms_val_data_prosperity_recovery         = 54
kms_val_data_fief_relation               = 55
kms_val_data_lrep_martial_relation       = 56
kms_val_data_lrep_quarrelsome_relation   = 57
kms_val_data_lrep_selfrighteous_relation = 58
kms_val_data_lrep_cunning_relation       = 59
kms_val_data_lrep_debauched_relation     = 60
kms_val_data_lrep_goodnatured_relation   = 61
kms_val_data_lrep_upstanding_relation    = 62
kms_val_data_lrep_roguish_relation       = 63
kms_val_data_lrep_benefactor_relation    = 64
kms_val_data_lrep_custodian_relation     = 65
kms_val_data_bandit_infest_chance        = 66
kms_val_data_right_to_rule               = 67
kms_val_data_weariness_battle_penalty    = 68 # Added in v0.16
kms_val_data_weariness_recovery_max      = 69 # Added in v0.16
kms_val_data_weariness_recovery_rate     = 70 # Added in v0.16
kms_val_data_center_recruitment_factor   = 71 # Added in v0.24
kms_val_data_end                         = 72
# Reserve 67 - 85 for data points
kms_obj_button_restore                   = 100
kms_obj_policy_container                 = 101
kms_obj_decree_container                 = 102
kms_obj_primary_tooltip_container        = 103
kms_obj_secondary_tooltip_container      = 104
kms_obj_button_accept                    = 105
kms_obj_button_cancel                    = 106
kms_obj_primary_tooltip                  = 107
kms_obj_secondary_tooltip                = 108
kms_obj_title_tooltip                    = 109

kms_obj_decrees_begin                    = 110
kms_obj_decree_conscription              = 110
kms_obj_decree_laws_commons              = 111
kms_obj_decree_laws_nobles               = 112
kms_obj_decree_war_taxes                 = 113
kms_obj_decree_sanitation                = 114
kms_obj_decree_reconstruction            = 115 
kms_obj_decree_executions                = 116
# FUTURE DECREES GO HERE.  Update the end constant if you add more.
kms_obj_decrees_end                      = 117
# Reserve 118 - 129 for future decrees

kms_obj_label_non_king_warning           = 129
kms_obj_button_help                      = 130
kms_obj_button_summary                   = 131

kms_obj_label_begin                      = 132
kms_obj_label_conscription               = 132
kms_obj_label_laws_commons               = 133
kms_obj_label_laws_nobles                = 134
kms_obj_label_war_taxes                  = 135
kms_obj_label_sanitation                 = 136
kms_obj_label_reconstruction             = 137
kms_obj_label_executions                 = 138
# FUTURE DECREES GO HERE.  Update the end constant if you add more.
kms_obj_label_end                        = 139
# Reserve 140-151
kms_obj_main_title                       = 152
kms_obj_slider_policy_focus              = 153
kms_obj_label_policy_focus               = 154
kms_obj_desc_left_policy_focus           = 155
kms_obj_desc_right_policy_focus          = 156
kms_obj_slider_policy_diversity          = 157
kms_obj_label_policy_diversity           = 158
kms_obj_desc_left_policy_diversity       = 159
kms_obj_desc_right_policy_diversity      = 160
kms_obj_slider_policy_borders            = 161
kms_obj_label_policy_borders             = 162
kms_obj_desc_left_policy_borders         = 163
kms_obj_desc_right_policy_borders        = 164
kms_obj_slider_policy_slavery            = 165
kms_obj_label_policy_slavery             = 166
kms_obj_desc_left_policy_borders         = 167
kms_obj_desc_right_policy_slavery        = 168
kms_obj_slider_policy_desertion          = 169
kms_obj_label_policy_desertion           = 170
kms_obj_desc_left_policy_borders         = 171
kms_obj_desc_right_policy_desertion      = 172


PMR_OBJECTS                              = "trp_tpe_presobj"
pmr_obj_button_exit                      = 1
pmr_obj_factors_container                = 2