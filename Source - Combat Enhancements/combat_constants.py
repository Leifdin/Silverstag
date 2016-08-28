# Combat Enhancements by Windyplains

## KILLER REGENERATION (1.1) begin
#  Rates listed below are per kill, not based on duration.  They are also % of health, not exact values.
wp_hr_player_rate                  = 3
wp_hr_strength_factor              = 4   # This is the value STR is divided by.  So 4 = .25% per point of Strength.
wp_hr_leadership_factor            = 2   # This is the value Leadership is divided by.  Only non-heroes gain this.
wp_hr_lord_rate                    = 15
wp_hr_companion_rate               = 10
wp_hr_king_rate                    = 20
wp_hr_common_rate                  = 5
wp_hr_elite_rate                   = 15  # Currently unused.
wp_hr_factor_difficulty            = 1   # This turns ON (1) or OFF (0) any code changes based on difficulty.
wp_hr_diff_enemy_bonus             = 4   # Amount the health regeneration of enemies is boosted by per difficulty rank.
wp_hr_diff_ally_penalty            = -3  # Amount the health regeneration of allies is reduced by per difficulty rank.
# wp_hr_debug                        = 0   # This turns ON (1) or OFF (0) all of the debug messages.
## KILLER REGENERATION end

## BODYSLIDING+ ##
BODYSLIDING_STORAGE                = "trp_bodysliding_temp"

# Modes of Operation:
BODYSLIDING_DISABLED               = 0
BODYSLIDING_HEROES_ONLY            = 1
BODYSLIDING_ALL_TROOPS             = 2
## BODYSLIDING- ##

### AGENT SLOTS ####
slot_agent_sprint_timer            = 45 # This holds the time that an agent began sprinting.
slot_agent_sprint_cooldown         = 46 # This holds the timer value until an agent can sprint again.
slot_agent_is_sprinting            = 47 # This tracks whether an AI agent is sprinting or not.
slot_agent_horse_agent             = 48 # Tracks what horse the rider should have been attached to.
slot_agent_rider_agent             = 49 # Tracks what agent this horse was attached to.
slot_agent_last_calculated_speed   = 50 # Tracks what speed to reset an agent to.
slot_agent_time_since_attack       = 51 # Tracks how many seconds you've waited since last attack.
slot_agent_sprint_speed            = 52 # Tracks how fast someone is sprinting.
slot_agent_is_poisoned             = 53 # Tracks if an agent is poisoned (Combat Hampering)
slot_agent_duration_poisoned       = 54 # Tracks how many more ticks (4 sec each) a troop is poisoned for.
slot_agent_honor_lost_for_poison   = 55 # Tracks if the player has already lost 1 honor for using poison this battle.
slot_agent_current_stamina         = 56
slot_agent_max_stamina             = 57
slot_agent_shield_bash_cooldown    = 58 # This sets a limit on how soon an AI can use shield bash again.
slot_agent_last_stamina_value      = 59 # This tracks the player's last stamina value and prevents it from updating more than it has to.


### TROOP SLOTS ###
slot_troop_requirement_1           = 480
slot_troop_requirement_2           = 481
slot_troop_requirement_3           = 482
slot_troop_requirement_4           = 483
slot_troop_requirement_5           = 484
slot_troop_requirement_6           = 485
ce_requirements_begin              = slot_troop_requirement_1
ce_requirements_end                = 486

slot_troop_ability_1               = 490
slot_troop_ability_2               = 491
slot_troop_ability_3               = 492
slot_troop_ability_4               = 493
slot_troop_ability_5               = 494
slot_troop_ability_6               = 495
abilities_begin                    = slot_troop_ability_1
abilities_end                      = 496


## TROOP CLASSES
CLASS_INFANTRY                     = 0
CLASS_RANGED                       = 1
CLASS_CAVALRY                      = 2

## TROOP ABILITIES
BONUS_UNASSIGNED                   =  0
BONUS_ADMINISTRATOR                =  1 # Improves several aspects of a Castle Steward or Captain of the Guard's efficiency.
BONUS_AGILE_RIDER                  =  2 # Prevents falling damage from being taken when a rider is unhorsed.
BONUS_BERSERKER                    =  3 # Raises the health of an agenty by 1 per strenght point
BONUS_BLADEMASTER                  =  4 # This troop gains +2% damage per point of weapon master when wielding a melee cutting weapon.
BONUS_BLOODLUST                    =  5 # Troop gains +20% damage / -10% accuracy.  Gains more damage and loses more accuracy as health diminishes.
BONUS_BOUNDLESS_ENDURANCE          =  6 # Combat sprinting is 50% faster and 50% longer in duration. (+125% improvement in sprint distance)
BONUS_CARGOMASTER                  =  7 # This Quartermaster bonus improves merchant cash cap by 10% per point of Trade and sale value by 4% per point of Persuasion.
BONUS_CHARGING_STRIKE              =  8 # Further improves damage based upon agent speed.
BONUS_CHEAP                        =  9 # This unit is exceptionally cheap to hire.  -40% to hiring cost.
BONUS_CHEF                         = 10 # This Storekeeper bonus extends food stores by 25% and improves food morale bonus by 2% per point of Trade.
BONUS_COMMANDING_PRESENCE          = 11 # Raises the health regeneration of nearby troops by +2% + 1%/Leadership point.  Doesn't benefit the commander directly.
BONUS_DEDICATED                    = 12 # This troop is treated as one step better for determining its effect on party unity.
BONUS_DEVOTED                      = 13 # This troop costs only half as much for weekly wages.
BONUS_DISCIPLINED                  = 14 # Improves combat health based upon having a high intelligence.
BONUS_EFFICIENT                    = 15 # Improves several aspects of a Castle Steward's efficiency.
BONUS_ENDURANCE                    = 16 # Combat sprinting is 25% slower, but 100% longer in duration. (+50% improvement in sprint distance)
BONUS_ENGINEER                     = 17 # Improves several aspects of a Castle Steward's efficiency.
BONUS_ESCAPE_ARTIST                = 18 # Not implemented.
BONUS_FORTITUDE                    = 19 # This troop is resistent to the effects of combat performance hampering.  Sees its health 30% higher than it is.
BONUS_GRACEFUL_RIDER               = 20 # Allows a chance to ignore enhanced damage from pikes while on a mount.
BONUS_HARDY                        = 21 # Raises the health regeneration of this troop by +1% per point of Ironflesh.  Caps at +5% for heroes.
BONUS_HUNTER                       = 22 # This troop reduces the amount of mouths to feed in a party by using local game.
BONUS_INDOMITABLE                  = 23 # This troop more readily ignores encumbrance penalties associated with Strength.
BONUS_INSPIRING                    = 24 # This troop improves party morale by +2.  Companions improve it by +0.5/Leadership point.  (Limit: +15)
BONUS_LOYAL                        = 25 # This troop sees party morale as +20 higher than it really is when deciding to desert or not.
BONUS_MASTER_BOWMAN                = 26 # This troop gains 10% +2% damage per point of weapon master when wielding a bow.
BONUS_NIMBLE                       = 27 # This troop more readily ignores encumbrance penalties associated with Agility.
BONUS_POISONED_WEAPONS             = 28 # Reduces victim effective health by 50% and causes 1 health loss per 4s tick. (20 ticks)
BONUS_QUICK_STUDY                  = 29 # This troop gains +1% experience / 2 INT from bonus experience earned in a party role.  Reads as if 10 INT higher than actual.
BONUS_RALLYING_FIGURE              = 30 # Increases how many people you can have in your party.
BONUS_SAVAGE_BASH                  = 31 # Causes shield bash to deliver damage.
BONUS_SAVANT                       = 32 # Increases the bonus experience earned by a high intelligence by 50%.
BONUS_SCAVENGER                    = 33 # Improves the amount and quality of loot obtained from the battlefield.
BONUS_SECOND_WIND                  = 34 # Whenever you defeat an enemy you regain more stamina.
BONUS_SHARPSHOOTER                 = 35 # This troop gains (20% + 4%) accuracy per point of Weapon Master.
BONUS_SHIELD_BASHER                = 36 # Allows a troop to use the shield bash manuever.
BONUS_SIEGE_GENERAL                = 37 # This troop applies volley commander, tactician & commanding presence bonuses to all siege defenders if assigned as CotG.
BONUS_SILVER_TONGUED               = 38 # Not implemented.
BONUS_SPRINTER                     = 39 # Combat sprinting is 50% faster, but for -20% duration. (+20% improvement in sprint distance)
BONUS_STEADY_AIM                   = 40 # Improves ranged damage by 2% per second between shots up to a maximum of your Strength.
BONUS_STEADY_FOOTING               = 41 # Allows a troop to resist the effects of a shield bash.
BONUS_STEALTHY                     = 42 # This troop hides a certain number of party members when traveling on the world map.
BONUS_STORYTELLER                  = 43 # This troop increases the renown you gain from combat.
BONUS_SUPPLY_RUNNER                = 44 # Restocks ranged attackers in the field at a rate of 3 per minute.
BONUS_TACTICIAN                    = 45 # This troop improves the damage of nearby troops by 3% per point of Tactics.
BONUS_TAX_COLLECTOR                = 46 # This troop reduces tax inefficiency by 4% (-25% stacking limit) in any garrison he is stationed.
BONUS_THRIFTY                      = 47 # Shows how under or over-priced an item is in its tooltip.
BONUS_TIGHT_FORMATION              = 48 # This unit deals 25% more damage from pikes and ignores trample damage.
BONUS_TRAILBLAZER                  = 49 # Increases the party leader's path-finding skill by 1 per 5 troops.
BONUS_USEFUL_CONTACTS              = 50 # Allows new options to be added to someone in a party role.
BONUS_VOLLEY_COMMANDER             = 51 # This troop improves the accuracy of nearby troops by 8% per point of Tactics.
BONUS_WATCHFUL_EYE                 = 52 # This troop or companion improves the party's prisoner capacity.
BONUS_WHOLESALER                   = 53 # Reduce or eliminate the price drift due to purchasing or selling multiple of the same trade good.
BONUS_RAPID_RELOAD                 = 54 # Increases the reloading speed of troops by 5% per point of Agility.
BONUS_FIRING_CAPTAIN               = 55 # Increases the reloading speed of nearby troops by 4% per point of Leadership.
BONUS_SAVAGERY                     = 56 # Increases the courage lost by nearby troops when this troop defeats an enemy.
BONUS_RALLYING_STRIKE              = 57 # Increases the courage gained by nearby troops when this troop defeats an enemy.
BONUS_DRILL_SARGEANT               = 58 # Decreases morale by 5. Increases health of all troops by 1 per 5 strenght points. Morale penalty is decreased by 0.5 per Leadership point.
BONUS_END_OF_ABILITIES             = 59


# Berserker Settings
BERSERKER_BONUS_EASY               = 7
BERSERKER_BONUS_NORMAL             = 5
BERSERKER_BONUS_HARD               = 4
BERSERKER_BONUS_VERY_HARD          = 3

## TROOP PREREQUISITES
PREREQ_UNASSIGNED                  = 0
PREREQ_UNIQUE_LOCATION             = 1  # Tracked via slot_troop_unique_location.
PREREQ_ELITE_MERCENARY             = 2  # Requires that a mercenary unit has a chapterhouse built at the center before it can be hired.
PREREQ_OWNER_ONLY                  = 3  # Requires that you own the center to hire them.  Always upgrade PREREQ_AFFILIATED / PREREQ_CHARTERED -> PREREQ_OWNER_ONLY as it covers that.
PREREQ_FRIEND                      = 4  # Requires relation with a center >= troop_prereq_friend_relation
PREREQ_ALLY                        = 5  # Requires relation with a center >= troop_prereq_ally_relation
PREREQ_DISHONORABLE                = 6  # Not implemented.  Requires a negative honor value.
PREREQ_AFFILIATED                  = 7  # Requires that you are a part of the same faction to hire them.
PREREQ_CHARTERED                   = 8  # Not implemented.
PREREQ_UNIQUE_LOCATION_UPGRADE     = 9  # Used for slot upgrades on uniques to prevent them from being recruitable.
PREREQ_LIEGE_RELATION              = 10 # Requires that you have a minimum of 50 relation with the leader of this faction.
PREREQ_EXPENSIVE                   = 11 # Troop is twice as expensive as usually
PREREQ_DISREPUTABLE                = 12 # Hiring troop may reduce honor
PREREQ_DOPPELSOLDNER               = 13 # Double wage

troop_prereq_friend_relation       = 10
troop_prereq_ally_relation         = 25
troop_prereq_liege_relation        = 50
efficient_patrol_discount          = 2  # Value represents % discount per point of Leadership.

## ENCUMBRANCE
ENCUMBRANCE_FACTOR_MOVEMENT_SPEED  = -2

## SPEED
SPEED_FACTOR_TOTAL                 = 0
SPEED_FACTOR_AGILITY               = 1
SPEED_FACTOR_ENCUMBRANCE           = 2

## STAMINA
# Stamina Bar Presentation (script_ce_draw_stamina_bar)
STAMINA_BAR_CREATE                 = 0
STAMINA_BAR_UPDATE                 = 1

## SHIELD BASHING
AI_SHIELD_BASH_COOLDOWN            = 6  # Used in pbod_mission_templates.py

###########################################################################################################################
#####                                             PLAYER ABILITY CHOOSER                                              #####
###########################################################################################################################
PRES_OBJECTS                       = "trp_tpe_presobj"
ce_obj_button_done                 = 1
ce_obj_main_title                  = 2
ce_obj_container_ability_list      = 3
ce_obj_selected_ability            = 4
ce_val_selected_ability            = 5
ce_obj_button_clear_abilities      = 6
ce_obj_field_tooltip_1             = 7

ce_obj_button_assign_ability       = 360 # Reserve the next ten slots.
ce_obj_field_levels_start          = 370 # Reserve the next ten slots.
ce_obj_val_abilities_start         = 380 # Reserve the next ten slots.
ce_obj_field_abilities_start       = 390 # Reserve the next ten slots.
ce_obj_button_ability_list_start   = 400
## Reserve the next 100 slots.
