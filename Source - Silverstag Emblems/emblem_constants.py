# Silverstag Emblems by Windyplains

EMBLEM_MAX_QUANTITY                  = 50
SILVERSTAG_EMBLEM                    = "itm_silverstag_emblem"

## PARTY SLOTS
slot_center_training_cost_reduction    = 474
slot_center_training_cost_reduce_duration = 475
slot_center_queue_cost_reduce_duration = 476


## Functions for Spending Emblems
EMBLEM_COST_CLEAR_ABILITY            = 1   # Allows reseting a single player ability to an unassigned status.
EMBLEM_COST_ENHANCE_BUILD_RATE       = 1   # Improves the rate of building an improvement by 25%.  Stacks up to instant completion.
EMBLEM_COST_INSTANT_BUILD            = 3   # Instantly finishes construction on an improvement.
EMBLEM_COST_REDUCE_BUILD_COST        = 1   # Reduce the cost for building an improvement by 25%.  Stacks up to free cost.
EMBLEM_COST_FREE_BUILD_COST          = 3   # Reduce the cost for building an improvement to free.
EMBLEM_COST_REDUCE_RECRUITMENT_COST  = 1   # Reduce the cost of hiring new troops by 25% for 24 hours.
EMBLEM_COST_REDUCE_GARRISON_COST     = 1   # Reduce the cost of hiring new garrison troops by 10% for one week.
EMBLEM_COST_ADD_PROFICIENCY_POINTS   = 1   # Adds 30 unassigned weapon proficiency points to a companion.
EMBLEM_COST_ADD_ATTRIBUTE_POINT      = 1   # Adds 1 unassigned attribute point to a companion.
EMBLEM_COST_ADD_SKILL_POINT          = 1   # Adds 1 unassigned skill point to a companion.
EMBLEM_COST_RETCON_COMPANION         = 8   # Resets a companion's attributes, skill points & proficiencies to base values.
EMBLEM_COST_FINISH_BOOK_COMPANION    = 1   # Instantly completes reading of a book for a companion.
EMBLEM_COST_FINISH_BOOK_PLAYER       = 2   # Instantly completes reading of a book for the player.
EMBLEM_COST_BOOST_ARTISAN_XP         = 1   # Instantly boosts the experience of the location's artisan crafter.
EMBLEM_COST_COMMISSION_PRODUCTION    = 1   # Improves the rate of production for all commission / repair work at a location.
EMBLEM_COST_TRAINING_PERM_REDUCTION  = 1   # Reduces the training cost for new troops by 2% at a location permanently.
EMBLEM_COST_PLAYER_ADD_PROFICIENCY   = 1   # Adds 15 unassigned attribute points to the player's character.
EMBLEM_COST_PLAYER_RESET_ATTRIBUTES  = 3   # Allows the player to fully reset his attributes.
EMBLEM_COST_PLAYER_RESET_SKILLS      = 3   # Allows the player to fully reset his skill points.
EMBLEM_COST_PLAYER_RESET_PROFICIENCIES = 3 # Allows the player to fully reset his proficiency points.
EMBLEM_COST_PLAYER_RESET_ABILITIES   = 3   # Allows the player to fully reset his ability selections.
EMBLEM_COST_PLAYER_FULL_RETCON       = 8   # Allows the player to fully reset all aspects of his character.
EMBLEM_COST_TEMP_ACCELERATE_TRAINING = 1   # Increases the funding to experience ratio for training a garrison temporarily (one month).
EMBLEM_COST_PERM_ACCELERATE_TRAINING = 6   # Increases the funding to experience ratio for training a garrison permanently.

## Specific Factors
EMBLEM_STACK_LIMIT_TRAINING_PERM_REDUCTION = 5  # Any amount past this value will prevent an emblem from being spent.
EMBLEM_EFFECT_TRAINING_PERM_REDUCTION      = 2  # Costs are reduced by (Stacks * This Value)%.
EMBLEM_EFFECT_TRAINING_TEMP_REDUCTION      = 15 # Direct % cost reduction while this bonus is in effect.

########################################
###### PLAYER EMBLEM PRESENTATION ######
########################################
EMBLEM_OBJECTS                       = "trp_tpe_presobj"
# Presentation modes controlled by $pep_mode
PEP_MODE_INFORMATIONAL               = 0   # Describe the emblem system in game.
PEP_MODE_CHARACTER_RESET             = 1   # Resets for abilities, attributes, skills, proficiencies and all of the above.
PEP_MODE_STATISTICS                  = 2   # Add +1 skill, attribute or +10 proficiency.
PEP_MODE_MISC                        = 3   # Instantly finish a book
PEP_MODE_DEBUGGING                   = 4   # Add or remove emblems.


### UI - CORE ELEMENTS ###
pep1_obj_main_title                = 1
pep1_obj_button_done               = 2
pep1_obj_main_title2               = 3
pep1_obj_button_emblem_info        = 4
pep1_obj_button_character_resets   = 5
pep1_obj_button_statistics         = 6
pep1_obj_button_misc_options       = 7
pep1_obj_button_debugging          = 8
pep1_obj_container_1               = 100

### UI - PEP2 - CHARACTER RESETS
pep2_obj_option_reset_attributes   = 100
pep2_obj_option_reset_skills       = 101
pep2_obj_option_reset_proficiency  = 102
pep2_obj_option_reset_abilities    = 103
pep2_obj_option_full_retcon        = 104

### UI - PEP3 - CHARACTER DEVELOPMENT
pep3_obj_option_gain_attribute     = 100
pep3_obj_option_gain_skill         = 101
pep3_obj_option_gain_proficiency   = 102

### UI - PEP4 - MISC OPTIONS
pep4_obj_option_finish_book        = 100

### UI - PEP5 - DEBUGGING
pep5_obj_option_gain_emblem        = 100
pep5_obj_option_lose_emblem        = 101

