from module_constants import *

# DEBUG_QUEST_UTILITIES                           = 0
# DEBUG_QUEST_CONDITIONS                          = 0
# DEBUG_QUEST_AI                                  = 0
# DEBUG_QUEST_PACK_1                              = 0
# DEBUG_QUEST_PACK_2                              = 0
# DEBUG_QUEST_PACK_3                              = 0
# DEBUG_QUEST_PACK_4                              = 0
# DEBUG_QUEST_PACK_5                              = 0

QUEST_PACK_1_INSTALLED                          = 1 # Misc. Quests
QUEST_PACK_2_INSTALLED                          = 1 # Trade Quests & Trade Rival System
QUEST_PACK_3_INSTALLED                          = 1 # Nobility Quests
QUEST_PACK_4_INSTALLED                          = 1 # Companion Quests
QUEST_PACK_5_INSTALLED                          = 1 # Village Quests

CHECK_DC_VERY_EASY                              = 25
CHECK_DC_EASY                                   = 15
CHECK_DC_NORMAL                                 = 0
CHECK_DC_HARD                                   = -15
CHECK_DC_VERY_HARD                              = -30
CHECK_DC_IMPOSSIBLE                             = -45


# States of the *_quest_reactions global variable for each pack.
QUEST_REACTIONS_HIGH                            = 3
QUEST_REACTIONS_MEDIUM                          = 2
QUEST_REACTIONS_LOW                             = 1
QUEST_REACTIONS_OFF                             = 0

# TROOP SLOTS
slot_troop_intro_quest_complete                 = 380  # Once completed (value = 1) this companion will never leave the party.
slot_troop_story_arc_quest                      = 381
slot_troop_add_to_scene                         = 382

# PARTY / CENTER SLOTS
slot_party_pref_bodyguard                       = slot_town_arena_melee_3_num_teams #84   # Taken from PBOD to override bodyguards when storyline character should be used instead.
slot_party_time_in_field                        = 380
slot_party_wealth                               = 381
slot_party_caravan_origin                       = 382
slot_party_caravan_destination                  = 383
slot_party_caravan_escort_price                 = 384
# Stop at 389.  CMS system begins at 390.

REALM_QUAL_MAX_DISTANCE_TO_CENTER               = 15

# NEW QUEST SLOTS
slot_quest_primary_commodity                    = 40
slot_quest_secondary_commodity                  = 41
slot_quest_final_stage                          = 42
slot_quest_proficiency_gain_low                 = 43
slot_quest_proficiency_gain_medium              = 44
slot_quest_proficiency_gain_high                = 45
slot_quest_unique_name                          = 46
# unused slots 47-59
slot_quest_stage_1_trigger_chance               = 60
slot_quest_stage_2_trigger_chance               = 61
slot_quest_stage_3_trigger_chance               = 62
slot_quest_stage_4_trigger_chance               = 63
slot_quest_stage_5_trigger_chance               = 64
slot_quest_stage_6_trigger_chance               = 65
slot_quest_stage_7_trigger_chance               = 66
slot_quest_stage_8_trigger_chance               = 67
slot_quest_stage_9_trigger_chance               = 68
slot_quest_stage_10_trigger_chance              = 69
slot_quest_comment_made                         = 70

# General Script Parameter
floris_quest_begin                              = 1  # Initializes quest parameters and begins the quest.
floris_quest_update                             = 2  # Used to update the quest log.
floris_quest_succeed                            = 3  # Will cause specific quest to succeed with rewards.
floris_quest_fail                               = 4  # Will cause specific quest to fail with consequences.
floris_quest_cancel                             = 5  # Will cause specific quest to fail without consequence.
floris_quest_story_arc_check                    = 6  # Will check to see if the main story arc quest should fail or continue.  Intended for use as a check after failing any sub-quest.
floris_quest_reset_duration                     = 7  # Will reset the main story arc quest's duration whenever a sub-quest is completed.
floris_quest_storyline_failure                  = 8  # Triggered by simple trigger whenever story line has failed.  Sets up companion leaving.
floris_quest_setup                              = 9  # Used for initializing parameters prior to starting a quest.
floris_quest_victory_condition                  = 10 # Used by some quests to verify victory conditions met.
floris_quest_failure_condition                  = 11 # Used by some quests to verify failure conditions met.

# Story Arc Ending Conditions
floris_story_arc_unfinished                     = 0
floris_story_arc_successful                     = 1
floris_story_arc_failed                         = 2
floris_story_arc_success_lite                   = 3

# Center Types for Random Selection
center_is_any                                   = 0
center_is_village                               = 1
center_is_town                                  = 2
center_is_castle                                = 3
center_is_any_friendly                          = 4
center_is_village_friendly                      = 5
center_is_town_friendly                         = 6
center_is_castle_friendly                       = 7

# Color Definitions
qp_error_color                                  = 0xFFFFAAAA

# Prisoner Caravan functions
prisoner_caravan_create                         = 1  # Create a prisoner caravan party.                                           Syntax: (Function, Caravan Party, Center #)
prisoner_caravan_load_from_center               = 2  # Transfer all prisoners from specified center to caravan.                   Syntax: (Function, Caravan Party, Center #)
prisoner_caravan_unload_to_center_for_free      = 3  # Offload all prisoners to specified center without earning money.           Syntax: (Function, Caravan Party, Center #)
prisoner_caravan_unload_to_center_for_pay       = 4  # Offload all prisoners to specified center for a price.                     Syntax: (Function, Caravan Party, Center #)
prisoner_caravan_offload_wealth_and_remove      = 5  # Transfer wealth to specified center and remove caravan from game.          Syntax: (Function, Caravan Party, Center #)
prisoner_caravan_direct_to_destination          = 6  # Setup caravan to travel to destination.                                    Syntax: (Function, Caravan Party, Center # to go to)
prisoner_caravan_return_to_origin               = 7  # Setup caravan to return home.                                              Syntax: (Function, Caravan Party, Center # to go to)
prisoner_caravan_generate_escort_cost           = 8  # Calculate the cost of hiring mercenaries to protect caravan.               Syntax: (Function, 0, Center #)
prisoner_caravan_add_escort_troops              = 9  # Add additional troops based upon 35% of the prisoner total value.          Syntax: (Function, Caravan Party, Cost generated by generate_escort_cost)
prisoner_caravan_raided_by_troop                = 10 # Handles a lord or player raiding a caravan for its wealth.                 Syntax: (Function, Caravan Party, Troop #)

### NAME GENERATOR ###
# Western European
euro_boy_names_begin                            = "str_set_boy_2000"
euro_boy_names_end                              = "str_set_girl_2000"
euro_girl_names_begin                           = euro_boy_names_end
euro_girl_names_end                             = "str_set_last_2000"
euro_last_names_begin                           = euro_girl_names_end
euro_last_names_end                             = "str_set_boy_3000"
# Arabic
arabic_boy_names_begin                          = euro_last_names_end
arabic_boy_names_end                            = "str_set_girl_3000"
arabic_girl_names_begin                         = arabic_boy_names_end
arabic_girl_names_end                           = "str_set_last_3001"
arabic_last_names_begin                         = arabic_girl_names_end
arabic_last_names_end                           = "str_set_boy_4000"
# Norse
viking_boy_names_begin                          = arabic_last_names_end
viking_boy_names_end                            = "str_set_girl_4000"
viking_girl_names_begin                         = viking_boy_names_end
viking_girl_names_end                           = "str_set_last_4000"
viking_last_names_begin                         = viking_girl_names_end
viking_last_names_end                           = "str_name_list_end"

SCRT_FIRST                                      = 1
SCRT_LAST                                       = 2
SCRT_FULL                                       = 3