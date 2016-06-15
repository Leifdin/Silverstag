################################################################################
#                                               header_operations expanded RC2 #
################################################################################
# TABLE OF CONTENTS
################################################################################
#
# [ Z00 ] Introduction and Credits.
# [ Z01 ] Operation Modifiers.
# [ Z02 ] Flow Control.
# [ Z03 ] Mathematical Operations.
# [ Z04 ] Script/Trigger Parameters and Results.
# [ Z05 ] Keyboard and Mouse Input.
# [ Z06 ] World Map.
# [ Z07 ] Game Settings.
# [ Z08 ] Factions.
# [ Z09 ] Parties and Party Templates.
# [ Z10 ] Troops.
# [ Z11 ] Quests.
# [ Z12 ] Items.
# [ Z13 ] Sounds and Music Tracks.
# [ Z14 ] Positions.
# [ Z15 ] Game Notes.
# [ Z16 ] Tableaus and Heraldics.
# [ Z17 ] String Operations.
# [ Z18 ] Output And Messages.
# [ Z19 ] Game Control: Screens, Menus, Dialogs and Encounters.
# [ Z20 ] Scenes and Missions.
# [ Z21 ] Scene Props and Prop Instances.
# [ Z22 ] Teams and Agents.
# [ Z23 ] Presentations.
# [ Z24 ] Multiplayer And Networking.
# [ Z25 ] Remaining Esoteric Stuff.
# [ Z26 ] Hardcoded Compiler-Related Code.
#
################################################################################

################################################################################
# [ Z00 ] INTRODUCTION AND CREDITS
################################################################################

  # Everyone who has ever tried to mod Mount&Blade games knows perfectly well,
  # that the documentation for it's Module System is severely lacking. Warband
  # Module System, while introducing many new and useful operations, did not
  # improve considerably in the way of documentation. What's worse, a number of
  # outright errors and inconsistencies appeared between what was documented in
  # the comments to the header_operations.py file (which was the root source of
  # all Warband scripting documentation, whether you like it or not), and what
  # was actually implemented in the game engine.

  # Sooner or later someone was bound to dedicate some time and effort to fix
  # this problem by properly documenting the file. It just so happened that I
  # was the first person crazy enough to accept the challenge.

  # I have tried to make this file a self-sufficient source of information on
  # every operation that the Warband scripting engine knows of. Naturally I
  # failed - there are still many operations for which there is simply not
  # enough information, or operations with effects that have not yet been
  # thoroughly tested and confirmed. But as far as I know, there is currently
  # no other reference more exhaustive than this. I tried to make the file
  # useful to both seasoned scripters and complete newbies, and to a certain
  # degree this file can even serve as a tutorial into Warband scripting -
  # though it still won't replace the wealth of tutorials produced by the
  # Warband modding community.

  # I really hope you will find it useful as well.

  #                                    Alexander Lomski AKA Lav. Jan 18th, 2012.

  # And the credits.

  # First of all, I should credit Taleworlds for the creation of this game and
  # it's Module System. Without them, I wouldn't be able to work on this file
  # so even though I'm often sceptical about their programming style and quality
  # of their code, they still did a damn good job delivering this game to all
  # of us.

  # And then I should credit many members from the Warband modding community
  # who have shared their knowledge and helped me clear out many uncertainties
  # and inconsistencies. Special credits (in no particular order) go to
  # cmpxchg8b, Caba'drin, SonKidd, MadVader, dunde, Ikaguia, MadocComadrin and
  # Cjkjvfnby.

################################################################################
# [ Z01 ] OPERATION MODIFIERS
################################################################################

neg          = 0x80000000  # (neg|<operation_name>, ...),
this_or_next = 0x40000000  # (this_or_next|<operation_name>, ...),

################################################################################
# [ Z02 ] FLOW CONTROL
################################################################################

call_script             =    1  # (call_script, <script_id>, [<script_param>...]),
try_begin               =    4  # (try_begin),
else_try                =    5  # (else_try),
else_try_begin          =    5  # (else_try_begin),
try_end                 =    3  # (try_end),
end_try                 =    3  # (end_try),
try_for_range           =    6  # (try_for_range, <destination>, <lower_bound>, <upper_bound>),
try_for_range_backwards =    7  # (try_for_range_backwards, <destination>, <lower_bound>, <upper_bound>),
try_for_parties         =   11  # (try_for_parties, <destination>),
try_for_agents          =   12  # (try_for_agents, <destination>),

################################################################################
# [ Z03 ] MATHEMATICAL OPERATIONS
################################################################################

  # Mathematical operations deal with numbers. Warband Module System can only
  # deal with integers. Floating point numbers are emulated by the so-called
  # "fixed point numbers". Wherever you encounter a fixed point parameter for
  # some Module System operation, keep in mind that it is actually just a
  # regular integer number, HOWEVER it is supposed to represent a floating
  # point number equal to fixed_point_number / fixed_point_multiplier. As you
  # might have guessed, to convert a floating point number to fixed point, you
  # have to multiply it by fixed_point_multiplier. You can change the value of
  # multiplier with the operation (set_fixed_point_multiplier), thus influencing
  # the precision of all operations dealing with fixed point numbers.

  # A notion very important for Warband modding is that you reference all
  # Warband objects by their numeric values. In other words, you can do maths
  # with your items, troops, agents, scenes, parties et cetera. This is used
  # extensively in the code, so don't be surprised to see code looking like
  # (store_add, ":value", "itm_pike", 4). This code is just calculating a
  # reference to an item which is located 4 positions after "itm_pike" inside
  # the module_items.py file.

gt                         = 32      # (gt, <value1>, <value2>),
ge                         = 30      # (ge, <value1>, <value2>),
eq                         = 31      # (eq, <value1>, <value2>),
neq                        = neg|eq  # (neq, <value1>, <value2>),
le                         = neg|gt  # (le, <value1>, <value2>),
lt                         = neg|ge  # (lt, <value1>, <value2>),
is_between                 = 33      # (is_between, <value>, <lower_bound>, <upper_bound>),

assign                     = 2133    # (assign, <destination>, <value>),

store_add                  = 2120    # (store_add, <destination>, <value>, <value>),
store_sub                  = 2121    # (store_sub, <destination>, <value>, <value>),
store_mul                  = 2122    # (store_mul, <destination>, <value>, <value>),
store_div                  = 2123    # (store_div, <destination>, <value>, <value>),
store_mod                  = 2119    # (store_mod, <destination>, <value>, <value>),
val_add                    = 2105    # (val_add, <destination>, <value>),
val_sub                    = 2106    # (val_sub, <destination>, <value>),
val_mul                    = 2107    # (val_mul, <destination>, <value>),
val_div                    = 2108    # (val_div, <destination>, <value>),
val_mod                    = 2109    # (val_mod, <destination>, <value>),

val_min                    = 2110    # (val_min, <destination>, <value>),
val_max                    = 2111    # (val_max, <destination>, <value>),
val_clamp                  = 2112    # (val_clamp, <destination>, <lower_bound>, <upper_bound>),
val_abs                    = 2113    # (val_abs, <destination>),

store_random               = 2135    # (store_random, <destination>, <upper_range>),
store_random_in_range      = 2136    # (store_random_in_range, <destination>, <range_low>, <range_high>),
shuffle_range              = 2134    # (shuffle_range, <reg_no>, <reg_no>),

store_or                   = 2116    # (store_or, <destination>, <value>, <value>),
store_and                  = 2117    # (store_and, <destination>, <value>, <value>),
val_or                     = 2114    # (val_or, <destination>, <value>),
val_and                    = 2115    # (val_and, <destination>, <value>),
val_lshift                 = 2100    # (val_lshift, <destination>, <value>),
val_rshift                 = 2101    # (val_rshift, <destination>, <value>),

set_fixed_point_multiplier = 2124    # (set_fixed_point_multiplier, <value>),
convert_to_fixed_point     = 2130    # (convert_to_fixed_point, <destination_fixed_point>),
convert_from_fixed_point   = 2131    # (convert_from_fixed_point, <destination>),

store_sqrt                 = 2125    # (store_sqrt, <destination_fixed_point>, <value_fixed_point>),
store_pow                  = 2126    # (store_pow, <destination_fixed_point>, <value_fixed_point>, <power_fixed_point),
store_sin                  = 2127    # (store_sin, <destination_fixed_point>, <value_fixed_point>),
store_cos                  = 2128    # (store_cos, <destination_fixed_point>, <value_fixed_point>),
store_tan                  = 2129    # (store_tan, <destination_fixed_point>, <value_fixed_point>),
store_asin                 = 2140    # (store_asin, <destination_fixed_point>, <value_fixed_point>),
store_acos                 = 2141    # (store_acos, <destination_fixed_point>, <value_fixed_point>),
store_atan                 = 2142    # (store_atan, <destination_fixed_point>, <value_fixed_point>),
store_atan2                = 2143    # (store_atan2, <destination_fixed_point>, <y_fixed_point>, <x_fixed_point>),

################################################################################
# [ Z04 ] SCRIPT/TRIGGER PARAMETERS AND RESULTS
################################################################################

  # Many scripts can accept additional parameters, and many triggers have some
  # parameters of their own (as details in header_triggers.py file). You can
  # only pass numeric values as parameters. Since string constants are also
  # Warband objects, you can pass them as well, and you can also pass string
  # or position registers. However you cannot pass quick strings (string
  # defined directly in the code).

  # You can declare your scripts with as many parameters as you wish. Triggers,
  # however, are always called with their predefined parameters. Also the game
  # engine does not support more than 3 parameters per trigger. As the result,
  # some triggers receive extra information which could not be fit into those
  # three parameters in numeric, string or position registers.

  # Some triggers and scripts called from the game engine (those have names
  # starting with "game_") expect you to return some value to the game engine.
  # That value may be either a number or a string and is set by special
  # operations listed below. Scripts called from the Module System, however,
  # typically use registers to store their return data.

  # Note that if you call a script from a trigger, you can still use operations
  # to retrieve trigger's calling parameters, and they will retrieve values that
  # have been passed to the trigger, not values that have been passed to the
  # script.

store_script_param_1        =   21  # (store_script_param_1, <destination>),
store_script_param_2        =   22  # (store_script_param_2, <destination>),
store_script_param          =   23  # (store_script_param, <destination>, <script_param_index>),
set_result_string           =   60  # (set_result_string, <string>),

store_trigger_param_1       = 2071  # (store_trigger_param_1, <destination>),
store_trigger_param_2       = 2072  # (store_trigger_param_2, <destination>),
store_trigger_param_3       = 2073  # (store_trigger_param_3, <destination>),
store_trigger_param         = 2070  # (store_trigger_param, <destination>, <trigger_param_no>),
get_trigger_object_position =  702  # (get_trigger_object_position, <position>),
set_trigger_result          = 2075  # (set_trigger_result, <value>),

################################################################################
# [ Z05 ] KEYBOARD AND MOUSE INPUT
################################################################################

  # The game provides modders with limited ability to control keyboard input and
  # mouse movements. It is also possible to tamper with game keys (i.e. keys
  # bound to specific game actions), including the ability to override game's
  # reaction to those keys. Note that mouse buttons are keys too, and can be
  # detected with the corresponding operations.

key_is_down                     = 70  # (key_is_down, <key_code>),
key_clicked                     = 71  # (key_clicked, <key_code>),
game_key_is_down                = 72  # (key_is_down, <game_key_code>),
game_key_clicked                = 73  # (key_clicked, <game_key_code>),

omit_key_once                   = 77  # (omit_key_once, <key_code>),
clear_omitted_keys              = 78  # (clear_omitted_keys),

mouse_get_position              = 75  # (mouse_get_position, <position>),

################################################################################
# [ Z06 ] WORLD MAP
################################################################################

  # Generally, all operations which only make sense on the worldmap and have no
  # specific category have been assembled here. These mostly deal with weather,
  # time and resting.

is_currently_night         = 2273  # (is_currently_night),
map_free                   =   37  # (map_free),

get_global_cloud_amount    =   90  # (get_global_cloud_amount, <destination>),
set_global_cloud_amount    =   91  # (set_global_cloud_amount, <value>),
get_global_haze_amount     =   92  # (get_global_haze_amount, <destination>),
set_global_haze_amount     =   93  # (set_global_haze_amount, <value>),

store_current_hours        = 2270  # (store_current_hours, <destination>),
store_time_of_day          = 2271  # (store_time_of_day, <destination>),
store_current_day          = 2272  # (store_current_day, <destination>),

rest_for_hours             = 1030  # (rest_for_hours, <rest_time_in_hours>, [time_speed_multiplier], [remain_attackable]),
rest_for_hours_interactive = 1031  # (rest_for_hours_interactive, <rest_time_in_hours>, [time_speed_multiplier], [remain_attackable]),

################################################################################
# [ Z07 ] GAME SETTINGS AND STATISTICS
################################################################################

  # This group of operations allows you to retrieve some of the game settings
  # as configured by the player on Options page, and change them as necessary
  # (possibly forcing a certain level of difficulty on the player). Operations
  # dealing with achievements (an interesting, but underdeveloped feature of
  # Warband) are also placed in this category.

is_trial_version                      =  250  # (is_trial_version),
is_edit_mode_enabled                  =  255  # (is_edit_mode_enabled),

set_player_troop                      =   47  # (set_player_troop, <troop_id>),
show_object_details_overlay           =  960  # (show_object_details_overlay, <value>),

options_get_damage_to_player          =  260  # (options_get_damage_to_player, <destination>),
options_set_damage_to_player          =  261  # (options_set_damage_to_player, <value>),
options_get_damage_to_friends         =  262  # (options_get_damage_to_friends, <destination>),
options_set_damage_to_friends         =  263  # (options_set_damage_to_friends, <value>),
options_get_combat_ai                 =  264  # (options_get_combat_ai, <destination>),
options_set_combat_ai                 =  265  # (options_set_combat_ai, <value>),
options_get_campaign_ai               =  266  # (options_get_campaign_ai, <destination>),
options_set_campaign_ai               =  267  # (options_set_campaign_ai, <value>),
options_get_combat_speed              =  268  # (options_get_combat_speed, <destination>),
options_set_combat_speed              =  269  # (options_set_combat_speed, <value>),
get_average_game_difficulty           =  990  # (get_average_game_difficulty, <destination>),

get_achievement_stat                  =  370  # (get_achievement_stat, <destination>, <achievement_id>, <stat_index>),
set_achievement_stat                  =  371  # (set_achievement_stat, <achievement_id>, <stat_index>, <value>),
unlock_achievement                    =  372  # (unlock_achievement, <achievement_id>),
get_player_agent_kill_count           = 1701  # (get_player_agent_kill_count, <destination>, [get_wounded]),
get_player_agent_own_troop_kill_count = 1705  # (get_player_agent_own_troop_kill_count, <destination>, [get_wounded]),

################################################################################
# [ Z08 ] FACTIONS
################################################################################

  # Despite the importance of factions to the game, there aren't that many
  # actions to deal with them. Essentially, you can control colors and name of
  # existing game factions, set or retrieve relations between them, and work
  # with faction slots. There's also a number of operations which assign or
  # retrieve the factional allegiance of other game objects, like parties and
  # troops, but these have been placed in the respective sections of the file.

faction_set_slot                =  502  # (faction_set_slot, <faction_id>, <slot_no>, <value>),
faction_get_slot                =  522  # (faction_get_slot, <destination>, <faction_id>, <slot_no>),
faction_slot_eq                 =  542  # (faction_slot_eq, <faction_id>, <slot_no>, <value>),
faction_slot_ge                 =  562  # (faction_slot_ge, <faction_id>, <slot_no>, <value>),

set_relation                    = 1270  # (set_relation, <faction_id_1>, <faction_id_2>, <value>),
store_relation                  = 2190  # (store_relation, <destination>, <faction_id_1>, <faction_id_2>),
faction_set_name                = 1275  # (faction_set_name, <faction_id>, <string>),
faction_set_color               = 1276  # (faction_set_color, <faction_id>, <color_code>),
faction_get_color               = 1277  # (faction_get_color, <destination>, <faction_id>)

################################################################################
# [ Z09 ] PARTIES AND PARTY TEMPLATES
################################################################################

  # Parties are extremely important element of single-player modding, because
  # they are the only object which can be present on the world map. Each party
  # is a semi-independent object with it's own behavior. Note that you cannot
  # control party's behavior directly, instead you can change various factors
  # which affect party behavior (including party AI settings).

  # There are two things of importance when dealing with parties. First, parties
  # can be attached to each other, this allows you, for example, to stack a
  # number of armies inside a single city. Second, parties may encounter each
  # other. When two AI parties are in encounter, it usually means they are
  # fighting. Player's encounter with an AI party is usually much more complex
  # and may involve pretty much anything, which is why player's encounters are
  # covered in a separate section of the file.

  # Each party consists of troop stacks. Each troop stack is either a single
  # hero (troop defined as tf_hero in module_troops.py file) or a number of
  # regular troops (their number may vary from 1 and above). Each party has two
  # sets of troop stacks: members (or companions) set of stacks, and prisoners
  # set of stacks. Many operations will only affect members, others may only
  # affect prisoners, and there are even operations to switch their roles.

  # Another important concept is a party template. It's definition looks very
  # similar to a party. Templates are used when there's a need to create a
  # number of parties with similar set of members, parameters or flags. Also
  # templates can be easily used to differentiate parties from each other,
  # so they are akin to a "party_type" in the game.

  # Note that parties are the only game object which is persistent (i.e. it
  # will be saved to the savegame file and restored on load), has slots and
  # can be created during runtime. This makes parties ideal candidates for
  # dynamic information storage of unlimited volume, which the game otherwise
  # lacks.

# Condition checking operations

hero_can_join                         =  101  # (hero_can_join, [party_id]),
hero_can_join_as_prisoner             =  102  # (hero_can_join_as_prisoner, [party_id]),
party_can_join                        =  103  # (party_can_join),
party_can_join_as_prisoner            =  104  # (party_can_join_as_prisoner),
troops_can_join                       =  105  # (troops_can_join, <value>),
troops_can_join_as_prisoner           =  106  # (troops_can_join_as_prisoner, <value>),
party_can_join_party                  =  107  # (party_can_join_party, <joiner_party_id>, <host_party_id>, [flip_prisoners]),
main_party_has_troop                  =  110  # (main_party_has_troop, <troop_id>),
party_is_in_town                      =  130  # (party_is_in_town, <party_id>, <town_party_id>),
party_is_in_any_town                  =  131  # (party_is_in_any_town, <party_id>),
party_is_active                       =  132  # (party_is_active, <party_id>),

# Slot operations for parties and party templates

party_template_set_slot               =  504  # (party_template_set_slot, <party_template_id>, <slot_no>, <value>),
party_template_get_slot               =  524  # (party_template_get_slot, <destination>, <party_template_id>, <slot_no>),
party_template_slot_eq                =  544  # (party_template_slot_eq, <party_template_id>, <slot_no>, <value>),
party_template_slot_ge                =  564  # (party_template_slot_ge, <party_template_id>, <slot_no>, <value>),

party_set_slot                        =  501  # (party_set_slot, <party_id>, <slot_no>, <value>),
party_get_slot                        =  521  # (party_get_slot, <destination>, <party_id>, <slot_no>),
party_slot_eq                         =  541  # (party_slot_eq, <party_id>, <slot_no>, <value>),
party_slot_ge                         =  561  # (party_slot_ge, <party_id>, <slot_no>, <value>),

# Generic operations

set_party_creation_random_limits      = 1080  # (set_party_creation_random_limits, <min_value>, <max_value>),
set_spawn_radius                      = 1103  # (set_spawn_radius, <value>),
spawn_around_party                    = 1100  # (spawn_around_party, <party_id>, <party_template_id>),
disable_party                         = 1230  # (disable_party, <party_id>),
enable_party                          = 1231  # (enable_party, <party_id>),
remove_party                          = 1232  # (remove_party, <party_id>),

party_get_current_terrain             = 1608  # (party_get_current_terrain, <destination>, <party_id>),
party_relocate_near_party             = 1623  # (party_relocate_near_party, <relocated_party_id>, <target_party_id>, <spawn_radius>),
party_get_position                    = 1625  # (party_get_position, <dest_position>, <party_id>),
party_set_position                    = 1626  # (party_set_position, <party_id>, <position>),
set_camera_follow_party               = 1021  # (set_camera_follow_party, <party_id>),

party_attach_to_party                 = 1660  # (party_attach_to_party, <party_id>, <party_id_to_attach_to>),
party_detach                          = 1661  # (party_detach, <party_id>),
party_collect_attachments_to_party    = 1662  # (party_collect_attachments_to_party, <source_party_id>, <collected_party_id>),
party_get_cur_town                    = 1665  # (party_get_cur_town, <destination>, <party_id>),
party_get_attached_to                 = 1694  # (party_get_attached_to, <destination>, <party_id>),
party_get_num_attached_parties        = 1695  # (party_get_num_attached_parties, <destination>, <party_id>),
party_get_attached_party_with_rank    = 1696  # (party_get_attached_party_with_rank, <destination>, <party_id>, <attached_party_index>),

party_set_name                        = 1669  # (party_set_name, <party_id>, <string>),
party_set_extra_text                  = 1605  # (party_set_extra_text, <party_id>, <string>),
party_get_icon                        = 1681  # (party_get_icon, <destination>, <party_id>),
party_set_icon                        = 1676  # (party_set_icon, <party_id>, <map_icon_id>),
party_set_banner_icon                 = 1677  # (party_set_banner_icon, <party_id>, <map_icon_id>),
party_set_extra_icon                  = 1682  # (party_set_extra_icon, <party_id>, <map_icon_id>, <vertical_offset_fixed_point>, <up_down_frequency_fixed_point>, <rotate_frequency_fixed_point>, <fade_in_out_frequency_fixed_point>),
party_add_particle_system             = 1678  # (party_add_particle_system, <party_id>, <particle_system_id>),
party_clear_particle_systems          = 1679  # (party_clear_particle_systems, <party_id>),
context_menu_add_item                 =  980  # (context_menu_add_item, <string_id>, <value>),

party_get_template_id                 = 1609  # (party_get_template_id, <destination>, <party_id>),
party_set_faction                     = 1620  # (party_set_faction, <party_id>, <faction_id>),
store_faction_of_party                = 2204  # (store_faction_of_party, <destination>, <party_id>),

store_random_party_in_range           = 2254  # (store_random_party_in_range, <destination>, <lower_bound>, <upper_bound>),
store01_random_parties_in_range       = 2255  # (store01_random_parties_in_range, <lower_bound>, <upper_bound>),
store_distance_to_party_from_party    = 2281  # (store_distance_to_party_from_party, <destination>, <party_id>, <party_id>),

store_num_parties_of_template         = 2310  # (store_num_parties_of_template, <destination>, <party_template_id>),
store_random_party_of_template        = 2311  # (store_random_party_of_template, <destination>, <party_template_id>),

store_num_parties_created             = 2300  # (store_num_parties_created, <destination>, <party_template_id>),
store_num_parties_destroyed           = 2301  # (store_num_parties_destroyed, <destination>, <party_template_id>),
store_num_parties_destroyed_by_player = 2302  # (store_num_parties_destroyed_by_player, <destination>, <party_template_id>),

party_get_morale                      = 1671  # (party_get_morale, <destination>, <party_id>),
party_set_morale                      = 1672  # (party_set_morale, <party_id>, <value>),

# Party members manipulation

party_join                            = 1201  # (party_join),
party_join_as_prisoner                = 1202  # (party_join_as_prisoner),
troop_join                            = 1203  # (troop_join, <troop_id>),
troop_join_as_prisoner                = 1204  # (troop_join_as_prisoner, <troop_id>),
add_companion_party                   = 1233  # (add_companion_party, <troop_id_hero>),
party_add_members                     = 1610  # (party_add_members, <party_id>, <troop_id>, <number>),
party_add_prisoners                   = 1611  # (party_add_prisoners, <party_id>, <troop_id>, <number>),
party_add_leader                      = 1612  # (party_add_leader, <party_id>, <troop_id>, [number]),
party_force_add_members               = 1613  # (party_force_add_members, <party_id>, <troop_id>, <number>),
party_force_add_prisoners             = 1614  # (party_force_add_prisoners, <party_id>, <troop_id>, <number>),
party_add_template                    = 1675  # (party_add_template, <party_id>, <party_template_id>, [reverse_prisoner_status]),
distribute_party_among_party_group    = 1698  # (distribute_party_among_party_group, <party_to_be_distributed>, <group_root_party>),

remove_member_from_party              = 1210  # (remove_member_from_party, <troop_id>, [party_id]),
remove_regular_prisoners              = 1211  # (remove_regular_prisoners, <party_id>),
remove_troops_from_companions         = 1215  # (remove_troops_from_companions, <troop_id>, <value>),
remove_troops_from_prisoners          = 1216  # (remove_troops_from_prisoners, <troop_id>, <value>),
party_remove_members                  = 1615  # (party_remove_members, <party_id>, <troop_id>, <number>),
party_remove_prisoners                = 1616  # (party_remove_members, <party_id>, <troop_id>, <number>),
party_clear                           = 1617  # (party_clear, <party_id>),
add_gold_to_party                     = 1070  # (add_gold_to_party, <value>, <party_id>),

# Calculating party and stack sizes

party_get_num_companions              = 1601  # (party_get_num_companions, <destination>, <party_id>),
party_get_num_prisoners               = 1602  # (party_get_num_prisoners, <destination>, <party_id>),
party_count_members_of_type           = 1630  # (party_count_members_of_type, <destination>, <party_id>, <troop_id>),
party_count_companions_of_type        = 1631  # (party_count_companions_of_type, <destination>, <party_id>, <troop_id>),
party_count_prisoners_of_type         = 1632  # (party_count_prisoners_of_type, <destination>, <party_id>, <troop_id>),
party_get_free_companions_capacity    = 1633  # (party_get_free_companions_capacity, <destination>, <party_id>),
party_get_free_prisoners_capacity     = 1634  # (party_get_free_prisoners_capacity, <destination>, <party_id>),
party_get_num_companion_stacks        = 1650  # (party_get_num_companion_stacks, <destination>, <party_id>),
party_get_num_prisoner_stacks         = 1651  # (party_get_num_prisoner_stacks, <destination>, <party_id>),
party_stack_get_troop_id              = 1652  # (party_stack_get_troop_id, <destination>, <party_id>, <stack_no>),
party_stack_get_size                  = 1653  # (party_stack_get_size, <destination>, <party_id>, <stack_no>),
party_stack_get_num_wounded           = 1654  # (party_stack_get_num_wounded, <destination>, <party_id>, <stack_no>),
party_stack_get_troop_dna             = 1655  # (party_stack_get_troop_dna, <destination>, <party_id>, <stack_no>),
party_prisoner_stack_get_troop_id     = 1656  # (party_get_prisoner_stack_troop, <destination>, <party_id>, <stack_no>),
party_prisoner_stack_get_size         = 1657  # (party_get_prisoner_stack_size, <destination>, <party_id>, <stack_no>),
party_prisoner_stack_get_troop_dna    = 1658  # (party_prisoner_stack_get_troop_dna, <destination>, <party_id>, <stack_no>),
store_num_free_stacks                 = 2154  # (store_num_free_stacks, <destination>, <party_id>),
store_num_free_prisoner_stacks        = 2155  # (store_num_free_prisoner_stacks, <destination>, <party_id>),
store_party_size                      = 2156  # (store_party_size, <destination>,[party_id]),
store_party_size_wo_prisoners         = 2157  # (store_party_size_wo_prisoners, <destination>, [party_id]),
store_troop_kind_count                = 2158  # (store_troop_kind_count, <destination>, <troop_type_id>),
store_num_regular_prisoners           = 2159  # (store_num_regular_prisoners, <destination>, <party_id>),
store_troop_count_companions          = 2160  # (store_troop_count_companions, <destination>, <troop_id>, [party_id]),
store_troop_count_prisoners           = 2161  # (store_troop_count_prisoners, <destination>, <troop_id>, [party_id]),

# Party experience and skills

party_add_xp_to_stack                 = 1670  # (party_add_xp_to_stack, <party_id>, <stack_no>, <xp_amount>),
party_upgrade_with_xp                 = 1673  # (party_upgrade_with_xp, <party_id>, <xp_amount>, <upgrade_path>), #upgrade_path can be:
party_add_xp                          = 1674  # (party_add_xp, <party_id>, <xp_amount>),
party_get_skill_level                 = 1685  # (party_get_skill_level, <destination>, <party_id>, <skill_no>),

# Combat related operations

heal_party                            = 1225  # (heal_party, <party_id>),
party_wound_members                   = 1618  # (party_wound_members, <party_id>, <troop_id>, <number>),
party_remove_members_wounded_first    = 1619  # (party_remove_members_wounded_first, <party_id>, <troop_id>, <number>),
party_quick_attach_to_current_battle  = 1663  # (party_quick_attach_to_current_battle, <party_id>, <side>),
party_leave_cur_battle                = 1666  # (party_leave_cur_battle, <party_id>),
party_set_next_battle_simulation_time = 1667  # (party_set_next_battle_simulation_time, <party_id>, <next_simulation_time_in_hours>),
party_get_battle_opponent             = 1680  # (party_get_battle_opponent, <destination>, <party_id>)
inflict_casualties_to_party_group     = 1697  # (inflict_casualties_to_party, <parent_party_id>, <damage_amount>, <party_id_to_add_causalties_to>), 
party_end_battle                      =  108  # (party_end_battle, <party_no>),

# Party AI

party_set_marshall                    = 1604  # (party_set_marshall, <party_id>, <value>),
party_set_flags                       = 1603  # (party_set_flag, <party_id>, <flag>, <clear_or_set>),
party_set_aggressiveness              = 1606  # (party_set_aggressiveness, <party_id>, <number>),
party_set_courage                     = 1607  # (party_set_courage, <party_id>, <number>),
party_get_ai_initiative               = 1638  # (party_get_ai_initiative, <destination>, <party_id>),
party_set_ai_initiative               = 1639  # (party_set_ai_initiative, <party_id>, <value>),
party_set_ai_behavior                 = 1640  # (party_set_ai_behavior, <party_id>, <ai_bhvr>),
party_set_ai_object                   = 1641  # (party_set_ai_object, <party_id>, <object_party_id>),
party_set_ai_target_position          = 1642  # (party_set_ai_target_position, <party_id>, <position>),
party_set_ai_patrol_radius            = 1643  # (party_set_ai_patrol_radius, <party_id>, <radius_in_km>),
party_ignore_player                   = 1644  # (party_ignore_player, <party_id>, <duration_in_hours>),
party_set_bandit_attraction           = 1645  # (party_set_bandit_attraction, <party_id>, <attaraction>),
party_get_helpfulness                 = 1646  # (party_get_helpfulness, <destination>, <party_id>),
party_set_helpfulness                 = 1647  # (party_set_helpfulness, <party_id>, <number>),
get_party_ai_behavior                 = 2290  # (get_party_ai_behavior, <destination>, <party_id>),
get_party_ai_object                   = 2291  # (get_party_ai_object, <destination>, <party_id>),
party_get_ai_target_position          = 2292  # (party_get_ai_target_position, <position>, <party_id>),
get_party_ai_current_behavior         = 2293  # (get_party_ai_current_behavior, <destination>, <party_id>),
get_party_ai_current_object           = 2294  # (get_party_ai_current_object, <destination>, <party_id>),


################################################################################
# [ Z10 ] TROOPS
################################################################################

  # What troops are.

  # There are two major types of troops: heroes and regulars. They are treated
  # very differently by the game, so it's important not to confuse them. At the
  # same time, most Module System operations will not make any differentiation
  # between hero and regular troops.

  # First of all, hero troops do not stack. You cannot have a stack of heroes
  # in a party, each hero will always occupy a separate troop slot. At the same
  # time, you can put any number of regular troops into a single troop slot.

  # Second, the way the game treats equipment of heroes and troops is also
  # different. All heroes' items are treated in the same way as player's (no
  # big surprise, since player is actually a hero troop himself). Meanwhile,
  # items that the troop has are just suggestions for what this troop *might*
  # take into battle. On the battlefield, each agent spawned from the regular
  # troop, will only take a limited number of items from the inventory provided
  # by the troop definition in module_troops.py. Choice is absolutely random and
  # modder has only limited control over it through the use of guarantee flags.
  # There's one more additional caveat: while you can easily change the outfit
  # of a hero troop and your changes will persist through the game, same applies
  # to regular troops. In other words, by changing equipment of some regular
  # troop, you are changing all instances of that troop throughout the entire
  # game. In other words, you cannot re-equip a stack of regulars in a single
  # party - your changes will affect all parties in the world.

  # Third, while all heroes have a single predefined face code, which is used
  # consistently through the game, troops have entire range of face codes. This
  # range is used to randomize each agent's face within those constraints, so a
  # group of 12 pikemen will not look like a bunch of clones.

  # Fourth, hero troops can't be killed in battle. Every time hero's hit points
  # are reduced to zero, hero is always knocked down. For regular troops, chance
  # to be knocked down depends on the number of factors, but their default fate
  # when driven to zero health is death.

# Condition checking operators

troop_has_item_equipped                  =  151  # (troop_has_item_equipped, <troop_id>, <item_id>),
troop_is_mounted                         =  152  # (troop_is_mounted, <troop_id>),
troop_is_guarantee_ranged                =  153  # (troop_is_guarantee_ranged, <troop_id>),
troop_is_guarantee_horse                 =  154  # (troop_is_guarantee_horse, <troop_id>),
troop_is_hero                            = 1507  # (troop_is_hero, <troop_id>),
troop_is_wounded                         = 1508  # (troop_is_wounded, <troop_id>),
player_has_item                          =  150  # (player_has_item, <item_id>),
# troop slots
troop_set_slot                           =  500  # (troop_set_slot, <troop_id>, <slot_no>, <value>),
troop_get_slot                           =  520  # (troop_get_slot, <destination>, <troop_id>, <slot_no>),
troop_slot_eq                            =  540  # (troop_slot_eq, <troop_id>, <slot_no>, <value>),
troop_slot_ge                            =  560  # (troop_slot_ge, <troop_id>, <slot_no>, <value>),

# troop parameters
troop_set_type                           = 1505  # (troop_set_type, <troop_id>, <gender>),
troop_get_type                           = 1506  # (troop_get_type, <destination>, <troop_id>),
troop_set_class                          = 1517  # (troop_set_class, <troop_id>, <value>),
troop_get_class                          = 1516  # (troop_get_class, <destination>, <troop_id>),
class_set_name                           = 1837  # (class_set_name, <sub_class>, <string_id>),
add_xp_to_troop                          = 1062  # (add_xp_to_troop, <value>, [troop_id]),
add_xp_as_reward                         = 1064  # (add_xp_as_reward, <value>),
troop_get_xp                             = 1515  # (troop_get_xp, <destination>, <troop_id>),
store_attribute_level                    = 2172  # (store_attribute_level, <destination>, <troop_id>, <attribute_id>),
troop_raise_attribute                    = 1520  # (troop_raise_attribute, <troop_id>, <attribute_id>, <value>),
store_skill_level                        = 2170  # (store_skill_level, <destination>, <skill_id>, [troop_id]),
troop_raise_skill                        = 1521  # (troop_raise_skill, <troop_id>, <skill_id>, <value>),
store_proficiency_level                  = 2176  # (store_proficiency_level, <destination>, <troop_id>, <attribute_id>),
troop_raise_proficiency                  = 1522  # (troop_raise_proficiency, <troop_id>, <proficiency_no>, <value>),
troop_raise_proficiency_linear           = 1523  # (troop_raise_proficiency, <troop_id>, <proficiency_no>, <value>),
troop_add_proficiency_points             = 1525  # (troop_add_proficiency_points, <troop_id>, <value>),                    
store_troop_health                       = 2175  # (store_troop_health, <destination>, <troop_id>, [absolute]), # set absolute to 1 to get actual health; otherwise this will return percentage health in range (0-100)
troop_set_health                         = 1560  # (troop_set_health, <troop_id>, <relative health (0-100)>),
troop_get_upgrade_troop                  = 1561  # (troop_get_upgrade_troop, <destination>, <troop_id>, <upgrade_path>),
store_character_level                    = 2171  # (store_character_level, <destination>, [troop_id]),
get_level_boundary                       =  991  # (get_level_boundary, <destination>, <level_no>),
add_gold_as_xp                           = 1063  # (add_gold_as_xp, <value>, [troop_id]),  # Default troop is player

# troop equipment

troop_set_auto_equip                     = 1509  # (troop_set_auto_equip, <troop_id>, <value>),
troop_ensure_inventory_space             = 1510  # (troop_ensure_inventory_space, <troop_id>, <value>),
troop_sort_inventory                     = 1511  # (troop_sort_inventory, <troop_id>),
troop_add_item                           = 1530  # (troop_add_item, <troop_id>, <item_id>, [modifier]),
troop_remove_item                        = 1531  # (troop_remove_item, <troop_id>, <item_id>),
troop_clear_inventory                    = 1532  # (troop_clear_inventory, <troop_id>),
troop_equip_items                        = 1533  # (troop_equip_items, <troop_id>),
troop_inventory_slot_set_item_amount     = 1534  # (troop_inventory_slot_set_item_amount, <troop_id>, <inventory_slot_no>, <value>),
troop_inventory_slot_get_item_amount     = 1537  # (troop_inventory_slot_get_item_amount, <destination>, <troop_id>, <inventory_slot_no>),
troop_inventory_slot_get_item_max_amount = 1538  # (troop_inventory_slot_get_item_max_amount, <destination>, <troop_id>, <inventory_slot_no>),
troop_add_items                          = 1535  # (troop_add_items, <troop_id>, <item_id>, <number>),
troop_remove_items                       = 1536  # (troop_remove_items, <troop_id>, <item_id>, <number>),
troop_loot_troop                         = 1539  # (troop_loot_troop, <target_troop>, <source_troop_id>, <probability>), 
troop_get_inventory_capacity             = 1540  # (troop_get_inventory_capacity, <destination>, <troop_id>),
troop_get_inventory_slot                 = 1541  # (troop_get_inventory_slot, <destination>, <troop_id>, <inventory_slot_no>),
troop_get_inventory_slot_modifier        = 1542  # (troop_get_inventory_slot_modifier, <destination>, <troop_id>, <inventory_slot_no>),
troop_set_inventory_slot                 = 1543  # (troop_set_inventory_slot, <troop_id>, <inventory_slot_no>, <item_id>),
troop_set_inventory_slot_modifier        = 1544  # (troop_set_inventory_slot_modifier, <troop_id>, <inventory_slot_no>, <imod_value>),
store_item_kind_count                    = 2165  # (store_item_kind_count, <destination>, <item_id>, [troop_id]),
store_free_inventory_capacity            = 2167  # (store_free_inventory_capacity, <destination>, [troop_id]),

# Item merchandise operations

reset_price_rates                   = 1170  # (reset_price_rates),
set_price_rate_for_item             = 1171  # (set_price_rate_for_item, <item_id>, <value_percentage>),
set_price_rate_for_item_type        = 1172  # (set_price_rate_for_item_type, <item_type_id>, <value_percentage>),
set_merchandise_modifier_quality    = 1490  # (set_merchandise_modifier_quality, <value>),
set_merchandise_max_value           = 1491  # (set_merchandise_max_value, <value>),
reset_item_probabilities            = 1492  # (reset_item_probabilities, <value>),
set_item_probability_in_merchandise = 1493  # (set_item_probability_in_merchandise, <item_id>, <value>),
troop_add_merchandise               = 1512  # (troop_add_merchandise, <troop_id>, <item_type_id>, <value>),
troop_add_merchandise_with_faction  = 1513  # (troop_add_merchandise_with_faction, <troop_id>, <faction_id>, <item_type_id>, <value>), #faction_id is given to check if troop is eligible to produce that item

# troop various information
troop_set_name                           = 1501  # (troop_set_name, <troop_id>, <string_no>),
troop_set_plural_name                    = 1502  # (troop_set_plural_name, <troop_id>, <string_no>),
troop_set_face_key_from_current_profile  = 1503  # (troop_set_face_key_from_current_profile, <troop_id>),
troop_add_gold                           = 1528  # (troop_add_gold, <troop_id>, <value>),
troop_remove_gold                        = 1529  # (troop_remove_gold, <troop_id>, <value>),
store_troop_gold                         = 2149  # (store_troop_gold, <destination>, <troop_id>),
troop_set_faction                        = 1550  # (troop_set_faction, <troop_id>, <faction_id>),
store_troop_faction                      = 2173  # (store_troop_faction, <destination>, <troop_id>),
store_faction_of_troop                   = 2173  # (store_troop_faction, <destination>, <troop_id>),
troop_set_age                            = 1555  # (troop_set_age, <troop_id>, <age_slider_pos>),
store_troop_value                        = 2231  # (store_troop_value, <destination>, <troop_id>),

################################################################################
# [ Z11 ] QUESTS
################################################################################

  # Quests are just that: some tasks that characters in the game world want the
  # player to do. It's interesting to note that in Warband quests can have three
  # possible outcomes: success, failure and conclusion. Generally the last
  # option is used to indicate some "intermediate" quest result, which is
  # neither a full success, nor a total failure.

check_quest_active            =  200  # (check_quest_active, <quest_id>),
check_quest_finished          =  201  # (check_quest_finished, <quest_id>),
check_quest_succeeded         =  202  # (check_quest_succeeded, <quest_id>),
check_quest_failed            =  203  # (check_quest_failed, <quest_id>),
check_quest_concluded         =  204  # (check_quest_concluded, <quest_id>),

quest_set_slot                =  506  # (quest_set_slot, <quest_id>, <slot_no>, <value>),
quest_get_slot                =  526  # (quest_get_slot, <destination>, <quest_id>, <slot_no>),
quest_slot_eq                 =  546  # (quest_slot_eq, <quest_id>, <slot_no>, <value>),
quest_slot_ge                 =  566  # (quest_slot_ge, <quest_id>, <slot_no>, <value>),

start_quest                   = 1280  # (start_quest, <quest_id>, <giver_troop_id>),
conclude_quest                = 1286  # (conclude_quest, <quest_id>),
succeed_quest                 = 1282  # (succeed_quest, <quest_id>), #also concludes the quest
fail_quest                    = 1283  # (fail_quest, <quest_id>), #also concludes the quest
complete_quest                = 1281  # (complete_quest, <quest_id>),
cancel_quest                  = 1284  # (cancel_quest, <quest_id>),

setup_quest_text              = 1290  # (setup_quest_text, <quest_id>),

store_partner_quest           = 2240  # (store_partner_quest, <destination>),

setup_quest_giver             = 1291  # (setup_quest_giver, <quest_id>, <string_id>),
store_random_quest_in_range   = 2250  # (store_random_quest_in_range, <destination>, <lower_bound>, <upper_bound>),
set_quest_progression         = 1285  # (set_quest_progression, <quest_id>, <value>),
store_random_troop_to_raise   = 2251  # (store_random_troop_to_raise, <destination>, <lower_bound>, <upper_bound>),
store_random_troop_to_capture = 2252  # (store_random_troop_to_capture, <destination>, <lower_bound>, <upper_bound>),
store_quest_number            = 2261  # (store_quest_number, <destination>, <quest_id>),
store_quest_item              = 2262  # (store_quest_item, <destination>, <item_id>),
store_quest_troop             = 2263  # (store_quest_troop, <destination>, <troop_id>),

################################################################################
# [ Z12 ] ITEMS
################################################################################

  # The title is a bit deceitful here. Items, despite the name, are not actual
  # game items. Rather these are the *definitions* for real game items, and you
  # can frequently see them referenced as "item types". However you should not
  # confuse this with so called itp_type_* constants which define the major item
  # classes existing in the game.

  # Consider this: a Smoked Fish (50/50) in your character's inventory is an
  # item in the game world. It's item type is "itm_smoked_fish" and it's basic
  # class is itp_type_food. So take care: operations in this section are dealing
  # with "itm_smoked_fish", not with actual fish in your inventory. The latter
  # is actually just an inventory slot from the Module System's point of view,
  # and operations to work with it are in the troops section of the file.

# Item slot operations

item_set_slot                       =  507  # (item_set_slot, <item_id>, <slot_no>, <value>),
item_get_slot                       =  527  # (item_get_slot, <destination>, <item_id>, <slot_no>),
item_slot_eq                        =  547  # (item_slot_eq, <item_id>, <slot_no>, <value>),
item_slot_ge                        =  567  # (item_slot_ge, <item_id>, <slot_no>, <value>),

# Generic item operations

item_get_type                       = 1570  # (item_get_type, <destination>, <item_id>),
store_item_value                    = 2230  # (store_item_value, <destination>, <item_id>),
store_random_horse                  = 2257  # (store_random_horse, <destination>),
store_random_equipment              = 2258  # (store_random_equipment, <destination>),
store_random_armor                  = 2259  # (store_random_armor, <destination>),

################################################################################
# [ Z13 ] SOUNDS AND MUSIC TRACKS
################################################################################

  # There are two types of sound in the game: sounds and tracks. Sounds are just
  # short sound effects. They can be positional (i.e. emitted by some object on
  # the scene or by player's opponent during the dialog). They can be generic
  # sound effects, like playing some drums when player meets mountain bandits.

  # Tracks are the background music. The game works as a kind of a musuc box,
  # cycling the available melodies according to the situation. It is up to the
  # Module System developer, however, to tell the game what the situation is.
  # There are two factors which you can tell the game: situation and culture.
  # So you can tell the game that the situation is "ambush" and the culture is
  # "khergits", and the game will select the musuc tracks which fit this
  # combination of situation and culture and will rotate them randomly. And of
  # course, you can also tell the game to play one specific track if you want.

play_sound_at_position   =  599  # (play_sound_at_position, <sound_id>, <position>, [options]),
play_sound               =  600  # (play_sound, <sound_id>, [options]),
play_track               =  601  # (play_track, <track_id>, [options]),
play_cue_track           =  602  # (play_cue_track, <track_id>),
music_set_situation      =  603  # (music_set_situation, <situation_type>),
music_set_culture        =  604  # (music_set_culture, <culture_type>),
stop_all_sounds          =  609  # (stop_all_sounds, [options]), 
store_last_sound_channel =  615  # (store_last_sound_channel, <destination>),
stop_sound_channel       =  616  # (stop_sound_channel, <sound_channel_no>),

################################################################################
# [ Z14 ] POSITIONS
################################################################################

  # Positions are the 3D math of the game. If you want to handle objects in
  # space, you will inevitably have to deal with positions. Note that while most
  # position-handling operations work both on global map and on the scenes,
  # there are operations which will only work in one or another mode.

  # Each position consists of three parts: coordinates, rotation and scale.

  # Coordinates are three numbers - (X,Y,Z) - which define a certain point in
  # space relative to the base of coordinates. Most of the time, the base of
  # coordinates is either the center of the global map, or the center of the
  # scene, but there may be exceptions. Note that all operations with
  # coordinates nearly always use fixed point numbers.

  # Position rotation determines just that - rotation around corresponding
  # world axis. So rotation around Z axis means rotation around vertical axis,
  # in other words - turning right and left. Rotation around X and Y axis will
  # tilt the position forward/backwards and right/left respectively.

  # It is common game convention that X world axis points to the East, Y world
  # axis points to the North and Z world axis points straight up. However this
  # is so-called global coordinates system, and more often than not you'll be
  # dealing with local coordinates. Local coordinates are the coordinate system
  # defined by the object's current position. For the object, his X axis is to
  # the right, Y axis is forward, and Z axis is up. This is simple enough, but
  # consider what happens if that object is turned upside down in world space?
  # Object's Z axis will point upwards *from the object's point of view*, in
  # other words, in global space it will be pointing *downwards*. And if the
  # object is moving, then it's local coordinates system is moving with it...
  # you get the idea.

  # Imagine the position as a small point with an arrow somewhere in space.
  # Position's coordinates are the point's position. Arrow points horizontally
  # to the North by default, and position's rotation determines how much was
  # it turned in the each of three directions.

  # Final element of position is scale. It is of no direct relevance to the
  # position itself, and it does not participate in any calculations. However
  # it is important when you retrieve or set positions of objects. In this
  # case, position's scale is object's scale - so you can shrink that wall
  # or quite the opposite, make it grow to the sky, depending on your whim.

# Generic position operations

init_position                               =  701  # (init_position, <position>),
copy_position                               =  700  # (copy_position, <position_target>, <position_source>),
position_copy_origin                        =  719  # (position_copy_origin, <position_target>, <position_source>),
position_copy_rotation                      =  718  # (position_copy_rotation, <position_target>, <position_source>),

position_transform_position_to_parent       =  716  # (position_transform_position_to_parent, <position_dest>, <position_anchor>, <position_relative_to_anchor>),
position_transform_position_to_local        =  717  # (position_transform_position_to_local, <position_dest>, <position_anchor>, <position_source>),

# Position (X,Y,Z) coordinates

position_get_x                              =  726  # (position_get_x, <destination_fixed_point>, <position>),
position_get_y                              =  727  # (position_get_y, <destination_fixed_point>, <position>),
position_get_z                              =  728  # (position_get_z, <destination_fixed_point>, <position>),

position_set_x                              =  729  # (position_set_x, <position>, <value_fixed_point>),
position_set_y                              =  730  # (position_set_y, <position>, <value_fixed_point>),
position_set_z                              =  731  # (position_set_z, <position>, <value_fixed_point>),

position_move_x                             =  720  # (position_move_x, <position>, <movement>, [value]),
position_move_y                             =  721  # (position_move_y, <position>, <movement>,[value]),
position_move_z                             =  722  # (position_move_z, <position>, <movement>,[value]),

position_set_z_to_ground_level              =  791  # (position_set_z_to_ground_level, <position>),
position_get_distance_to_terrain            =  792  # (position_get_distance_to_terrain, <destination>, <position>),
position_get_distance_to_ground_level       =  793  # (position_get_distance_to_ground_level, <destination>, <position>),

# Position rotation

position_get_rotation_around_x              =  742  # (position_get_rotation_around_x, <destination>, <position>),
position_get_rotation_around_y              =  743  # (position_get_rotation_around_y, <destination>, <position>),
position_get_rotation_around_z              =  740  # (position_get_rotation_around_z, <destination>, <position>),

position_rotate_x                           =  723  # (position_rotate_x, <position>, <angle>),
position_rotate_y                           =  724  # (position_rotate_y, <position>, <angle>),
position_rotate_z                           =  725  # (position_rotate_z, <position>, <angle>, [use_global_z_axis]), # set use_global_z_axis as 1 if needed, otherwise you don't have to give that.

position_rotate_x_floating                  =  738  # (position_rotate_x_floating, <position>, <angle_fixed_point>),
position_rotate_y_floating                  =  739  # (position_rotate_y_floating, <position>, <angle_fixed_point>),

# Position scale

position_get_scale_x                        =  735  # (position_get_scale_x, <destination_fixed_point>, <position>),
position_get_scale_y                        =  736  # (position_get_scale_y, <destination_fixed_point>, <position>),
position_get_scale_z                        =  737  # (position_get_scale_z, <destination_fixed_point>, <position>),

position_set_scale_x                        =  744  # (position_set_scale_x, <position>, <value_fixed_point>),
position_set_scale_y                        =  745  # (position_set_scale_y, <position>, <value_fixed_point>),
position_set_scale_z                        =  746  # (position_set_scale_z, <position>, <value_fixed_point>),

# Measurement of distances and angles

get_angle_between_positions                 =  705  # (get_angle_between_positions, <destination_fixed_point>, <position_no_1>, <position_no_2>),
position_has_line_of_sight_to_position      =  707  # (position_has_line_of_sight_to_position, <position_no_1>, <position_no_2>),
get_distance_between_positions              =  710  # (get_distance_between_positions, <destination>, <position_no_1>, <position_no_2>),
get_distance_between_positions_in_meters    =  711  # (get_distance_between_positions_in_meters, <destination>, <position_no_1>, <position_no_2>),
get_sq_distance_between_positions           =  712  # (get_sq_distance_between_positions, <destination>, <position_no_1>, <position_no_2>),
get_sq_distance_between_positions_in_meters =  713  # (get_sq_distance_between_positions_in_meters, <destination>, <position_no_1>, <position_no_2>),
position_is_behind_position                 =  714  # (position_is_behind_position, <position_base>, <position_to_check>),
get_sq_distance_between_position_heights    =  715  # (get_sq_distance_between_position_heights, <destination>, <position_no_1>, <position_no_2>),
position_normalize_origin                   =  741  # (position_normalize_origin, <destination_fixed_point>, <position>),
position_get_screen_projection              =  750  # (position_get_screen_projection, <position_screen>, <position_world>),

# Global map positions

map_get_random_position_around_position     = 1627  # (map_get_random_position_around_position, <dest_position_no>, <source_position_no>, <radius>),
map_get_land_position_around_position       = 1628  # (map_get_land_position_around_position, <dest_position_no>, <source_position_no>, <radius>),
map_get_water_position_around_position      = 1629  # (map_get_water_position_around_position, <dest_position_no>, <source_position_no>, <radius>),

################################################################################
# [ Z15 ] GAME NOTES
################################################################################

  # The game provides the player with the Notes screen, where there are several
  # sections: Troops, Factions, Parties, Quests and Information. This is the
  # player's "diary", where all information player knows is supposed to be
  # stored. With the operations from this section, modder can control what
  # objects the player will be able to see in their corresponding sections of
  # the Notes screen, and what information will be displayed on each object.

troop_set_note_available        = 1095 # (troop_set_note_available, <troop_id>, <value>),
add_troop_note_tableau_mesh     = 1108 # (add_troop_note_tableau_mesh, <troop_id>, <tableau_material_id>),
add_troop_note_from_dialog      = 1114 # (add_troop_note_from_dialog, <troop_id>, <note_slot_no>, <expires_with_time>),
add_troop_note_from_sreg        = 1117 # (add_troop_note_from_sreg, <troop_id>, <note_slot_no>, <string_id>, <expires_with_time>),

faction_set_note_available      = 1096 # (faction_set_note_available, <faction_id>, <value>), #1 = available, 0 = not available
add_faction_note_tableau_mesh   = 1109 # (add_faction_note_tableau_mesh, <faction_id>, <tableau_material_id>),
add_faction_note_from_dialog    = 1115 # (add_faction_note_from_dialog, <faction_id>, <note_slot_no>, <expires_with_time>),
add_faction_note_from_sreg      = 1118 # (add_faction_note_from_sreg, <faction_id>, <note_slot_no>, <string_id>, <expires_with_time>),

party_set_note_available        = 1097 # (party_set_note_available, <party_id>, <value>), #1 = available, 0 = not available
add_party_note_tableau_mesh     = 1110 # (add_party_note_tableau_mesh, <party_id>, <tableau_material_id>),
add_party_note_from_dialog      = 1116 # (add_party_note_from_dialog, <party_id>, <note_slot_no>, <expires_with_time>),
add_party_note_from_sreg        = 1119 # (add_party_note_from_sreg, <party_id>, <note_slot_no>, <string_id>, <expires_with_time>),

quest_set_note_available        = 1098 # (quest_set_note_available, <quest_id>, <value>), #1 = available, 0 = not available
add_quest_note_tableau_mesh     = 1111 # (add_quest_note_tableau_mesh, <quest_id>, <tableau_material_id>),
add_quest_note_from_dialog      = 1112 # (add_quest_note_from_dialog, <quest_id>, <note_slot_no>, <expires_with_time>),
add_quest_note_from_sreg        = 1113 # (add_quest_note_from_sreg, <quest_id>, <note_slot_no>, <string_id>, <expires_with_time>),

add_info_page_note_tableau_mesh = 1090 # (add_info_page_note_tableau_mesh, <info_page_id>, <tableau_material_id>),
add_info_page_note_from_dialog  = 1091 # (add_info_page_note_from_dialog, <info_page_id>, <note_slot_no>, <expires_with_time>),
add_info_page_note_from_sreg    = 1092 # (add_info_page_note_from_sreg, <info_page_id>, <note_slot_no>, <string_id>, <expires_with_time>),

################################################################################
# [ Z16 ] TABLEAUS AND HERALDICS
################################################################################

  # Tableaus are the tool that gives you limited access to the game graphical
  # renderer. If you know 3D graphics, you know that all 3D objects consist of
  # a mesh (which defines it's form) and the material (which defines how this
  # mesh is "painted"). With tableau functions you can do two things. First, you
  # can replace or alter the materials used to render the game objects (with
  # many restrictions). If this sounds esoteric to you, have a look at the game
  # heraldry - it is implemented using tableaus. Second, you can render images
  # of various game objects and place them on the game menus, presentations and
  # so on. For example, if you open the game Inventory window, you can see your
  # character in his current equipment. This character is rendered using tableau
  # operations. Similarly, if you open the Notes screen and select some kingdom
  # lord on the Troops section, you will see that lord's face and banner. Both
  # face and banner are drawn using tableaus.

cur_tableau_add_tableau_mesh                     = 1980  # (cur_tableau_add_tableau_mesh, <tableau_material_id>, <value>, <position_register_no>),
cur_item_set_tableau_material                    = 1981  # (cur_item_set_tableu_material, <tableau_material_id>, <instance_code>),
cur_scene_prop_set_tableau_material              = 1982  # (cur_scene_prop_set_tableau_material, <tableau_material_id>, <instance_code>),
cur_map_icon_set_tableau_material                = 1983  # (cur_map_icon_set_tableau_material, <tableau_material_id>, <instance_code>),
cur_tableau_render_as_alpha_mask                 = 1984  # (cur_tableau_render_as_alpha_mask)
cur_tableau_set_background_color                 = 1985  # (cur_tableau_set_background_color, <value>),
cur_agent_set_banner_tableau_material            = 1986  # (cur_agent_set_banner_tableau_material, <tableau_material_id>)
cur_tableau_set_ambient_light                    = 1987  # (cur_tableau_set_ambient_light, <red_fixed_point>, <green_fixed_point>, <blue_fixed_point>),
cur_tableau_set_camera_position                  = 1988  # (cur_tableau_set_camera_position, <position>),
cur_tableau_set_camera_parameters                = 1989  # (cur_tableau_set_camera_parameters, <is_perspective>, <camera_width_times_1000>, <camera_height_times_1000>, <camera_near_times_1000>, <camera_far_times_1000>),
cur_tableau_add_point_light                      = 1990  # (cur_tableau_add_point_light, <map_icon_id>, <position>, <red_fixed_point>, <green_fixed_point>, <blue_fixed_point>),
cur_tableau_add_sun_light                        = 1991  # (cur_tableau_add_sun_light, <map_icon_id>, <position>, <red_fixed_point>, <green_fixed_point>, <blue_fixed_point>),
cur_tableau_add_mesh                             = 1992  # (cur_tableau_add_mesh, <mesh_id>, <position>, <value_fixed_point>, <value_fixed_point>),
cur_tableau_add_mesh_with_vertex_color           = 1993  # (cur_tableau_add_mesh_with_vertex_color, <mesh_id>, <position>, <value_fixed_point>, <value_fixed_point>, <value>),
cur_tableau_add_map_icon                         = 1994  # (cur_tableau_add_map_icon, <map_icon_id>, <position>, <value_fixed_point>),
cur_tableau_add_troop                            = 1995  # (cur_tableau_add_troop, <troop_id>, <position>, <animation_id>, <instance_no>),
cur_tableau_add_horse                            = 1996  # (cur_tableau_add_horse, <item_id>, <position>, <animation_id>),
cur_tableau_set_override_flags                   = 1997  # (cur_tableau_set_override_flags, <value>),
cur_tableau_clear_override_items                 = 1998  # (cur_tableau_clear_override_items),
cur_tableau_add_override_item                    = 1999  # (cur_tableau_add_override_item, <item_kind_id>),
cur_tableau_add_mesh_with_scale_and_vertex_color = 2000  # (cur_tableau_add_mesh_with_scale_and_vertex_color, <mesh_id>, <position>, <position>, <value_fixed_point>, <value>),

################################################################################
# [ Z17 ] STRING OPERATIONS
################################################################################

  # The game provides you only limited control over string information. Most
  # operations will either retrieve some string (usually the name) from the game
  # object, or set that object's name to a string.

  # Two important functions are str_store_string and str_store_string_reg. They
  # are different from all others because they not only assign the string to a
  # string register, they *process* it. For example, if source string contains
  # "{reg3}", then the resulting string will have the register name and it's
  # surrounding brackets replaced with the value currently stored in that
  # register. Other strings can be substituted as well, and even some limited
  # logic can be implemented using this mechanism. You can try to read through
  # the module_strings.py file and try to deduce what each particular
  # substitution does.

# Conditional check operations

str_is_empty                    = 2318  # (str_is_empty, <string_register>),

# Other string operations

str_clear                       = 2319  # (str_clear, <string_register>)
str_store_string                = 2320  # (str_store_string, <string_register>, <string_id>),
str_store_string_reg            = 2321  # (str_store_string, <string_register>, <string_no>),
str_store_troop_name            = 2322  # (str_store_troop_name, <string_register>, <troop_id>),
str_store_troop_name_plural     = 2323  # (str_store_troop_name_plural, <string_register>, <troop_id>),
str_store_troop_name_by_count   = 2324  # (str_store_troop_name_by_count, <string_register>, <troop_id>, <number>),
str_store_item_name             = 2325  # (str_store_item_name, <string_register>, <item_id>),
str_store_item_name_plural      = 2326  # (str_store_item_name_plural, <string_register>, <item_id>),
str_store_item_name_by_count    = 2327  # (str_store_item_name_by_count, <string_register>, <item_id>),
str_store_party_name            = 2330  # (str_store_party_name, <string_register>, <party_id>),
str_store_agent_name            = 2332  # (str_store_agent_name, <string_register>, <agent_id>),
str_store_faction_name          = 2335  # (str_store_faction_name, <string_register>, <faction_id>),
str_store_quest_name            = 2336  # (str_store_quest_name, <string_register>, <quest_id>),
str_store_info_page_name        = 2337  # (str_store_info_page_name, <string_register>, <info_page_id>),
str_store_date                  = 2340  # (str_store_date, <string_register>, <number_of_hours_to_add_to_the_current_date>),
str_store_troop_name_link       = 2341  # (str_store_troop_name_link, <string_register>, <troop_id>),
str_store_party_name_link       = 2342  # (str_store_party_name_link, <string_register>, <party_id>),
str_store_faction_name_link     = 2343  # (str_store_faction_name_link, <string_register>, <faction_id>),
str_store_quest_name_link       = 2344  # (str_store_quest_name_link, <string_register>, <quest_id>),
str_store_info_page_name_link   = 2345  # (str_store_info_page_name_link, <string_register>, <info_page_id>),
str_store_class_name            = 2346  # (str_store_class_name, <stribg_register>, <class_id>)

# Network/multiplayer related string operations

str_store_player_username       = 2350  # (str_store_player_username, <string_register>, <player_id>),
str_store_server_password       = 2351  # (str_store_server_password, <string_register>),
str_store_server_name           = 2352  # (str_store_server_name, <string_register>),
str_store_welcome_message       = 2353  # (str_store_welcome_message, <string_register>),
str_encode_url                  = 2355  # (str_encode_url, <string_register>),

################################################################################
# [ Z18 ] OUTPUT AND MESSAGES
################################################################################

  # These operations will provide some textual information to the player during
  # the game. There are three operations which will generate a game message
  # (displayed as a chat-like series of text strings in the bottom-left part of
  # the screen), while most others will be displaying various types of dialog
  # boxes. You can also ask a question to player using these operations.

display_debug_message               = 1104  # (display_debug_message, <string_id>, [hex_colour_code]),
display_log_message                 = 1105  # (display_log_message, <string_id>, [hex_colour_code]),
display_message                     = 1106  # (display_message, <string_id>,[hex_colour_code]),
set_show_messages                   = 1107  # (set_show_messages, <value>),
tutorial_box                        = 1120  # (tutorial_box, <string_id>, <string_id>),
dialog_box                          = 1120  # (dialog_box, <text_string_id>, [title_string_id]),
question_box                        = 1121  # (question_box, <string_id>, [<yes_string_id>], [<no_string_id>]),
tutorial_message                    = 1122  # (tutorial_message, <string_id>, [color], [auto_close_time]),
tutorial_message_set_position       = 1123  # (tutorial_message_set_position, <position_x>, <position_y>), 
tutorial_message_set_size           = 1124  # (tutorial_message_set_size, <size_x>, <size_y>), 
tutorial_message_set_center_justify = 1125  # (tutorial_message_set_center_justify, <val>),
tutorial_message_set_background     = 1126  # (tutorial_message_set_background, <value>),

################################################################################
# [ Z19 ] GAME CONTROL: SCREENS, MENUS, DIALOGS AND ENCOUNTERS
################################################################################

  # An encounter is what happens when player's party meets another party on the
  # world map. While most operations in the game can be performed outside of
  # encounter, there's one thing you can only do when in encounter context -
  # standard game battle. When you are initiating the battle from an encounter,
  # the game engine will do most of the grunt work for you. You can order the
  # engine to add some parties to the battle on this or that side, and the
  # soldiers from those parties will spawn on the battlefield, in the numbers
  # proportional to the party sizes, and the agents will maintain links with
  # their parties. If agents earn experience, this will be reflected on the
  # world map, and if some agents die, party sizes will be decreased. All this
  # stuff can potentially be emulated by the Module System code, but it's tons
  # of work and is still much less efficient than the tool the game engine
  # already provides to you.

  # An important notice: when player encounters an AI party on the map, the game
  # calls "game_event_party_encounter" script in the module_scripts.py. So if
  # you want to implement some non-standard processing of game encounters, this
  # is the place you should start from. Also note that the game implements the
  # Camp menu as an encounter with a hardcoded party "p_camp_bandits".

  # Also you can find many operations in this section dealing with game screens,
  # game menus and game dialogs. Keep in mind that some screens only make sense
  # in certain contexts, and game menus are only available on the world map, you
  # cannot use game menus during the mission.

# Condition check operations

entering_town                         =   36  # (entering_town, <town_id>),
encountered_party_is_attacker         =   39  # (encountered_party_is_attacker),
conversation_screen_is_active         =   42  # (conversation_screen_active),
in_meta_mission                       =   44  # (in_meta_mission),

# Game hardcoded windows and related operations

change_screen_return                  = 2040  # (change_screen_return),
change_screen_loot                    = 2041  # (change_screen_loot, <troop_id>),
change_screen_trade                   = 2042  # (change_screen_trade, [troop_id]),
change_screen_exchange_members        = 2043  # (change_screen_exchange_members, [exchange_leader], [party_id]),
change_screen_trade_prisoners         = 2044  # (change_screen_trade_prisoners),
change_screen_buy_mercenaries         = 2045  # (change_screen_buy_mercenaries),
change_screen_view_character          = 2046  # (change_screen_view_character),
change_screen_training                = 2047  # (change_screen_training),
change_screen_mission                 = 2048  # (change_screen_mission),
change_screen_map_conversation        = 2049  # (change_screen_map_conversation, <troop_id>),
change_screen_exchange_with_party     = 2050  # (change_screen_exchange_with_party, <party_id>),
change_screen_equip_other             = 2051  # (change_screen_equip_other, [troop_id]),
change_screen_map                     = 2052  # (change_screen_map),
change_screen_notes                   = 2053  # (change_screen_notes, <note_type>, <object_id>),
change_screen_quit                    = 2055  # (change_screen_quit),
change_screen_give_members            = 2056  # (change_screen_give_members, [party_id]),
change_screen_controls                = 2057  # (change_screen_controls),
change_screen_options                 = 2058  # (change_screen_options),

set_mercenary_source_party            = 1320  # (set_mercenary_source_party, <party_id>),
start_map_conversation                = 1025  # (start_map_conversation, <troop_id>, [troop_dna]),

# Game menus

set_background_mesh                   = 2031  # (set_background_mesh, <mesh_id>),
set_game_menu_tableau_mesh            = 2032  # (set_game_menu_tableau_mesh, <tableau_material_id>, <value>, <position_register_no>),
jump_to_menu                          = 2060  # (jump_to_menu, <menu_id>),
disable_menu_option                   = 2061  # (disable_menu_option),

# Game encounter handling operations

set_party_battle_mode                 = 1020  # (set_party_battle_mode),
finish_party_battle_mode              = 1019  # (finish_party_battle_mode),


start_encounter                       = 1300  # (start_encounter, <party_id>),
leave_encounter                       = 1301  # (leave_encounter),
encounter_attack                      = 1302  # (encounter_attack),
select_enemy                          = 1303  # (select_enemy, <value>),
set_passage_menu                      = 1304  # (set_passage_menu, <value>),
start_mission_conversation            = 1920  # (start_mission_conversation, <troop_id>),

set_conversation_speaker_troop        = 2197  # (set_conversation_speaker_troop, <troop_id>),
set_conversation_speaker_agent        = 2198  # (set_conversation_speaker_agent, <agent_id>),
store_conversation_agent              = 2199  # (store_conversation_agent, <destination>),
store_conversation_troop              = 2200  # (store_conversation_troop, <destination>),
store_partner_faction                 = 2201  # (store_partner_faction, <destination>),
store_encountered_party               = 2202  # (store_encountered_party, <destination>),
store_encountered_party2              = 2203  # (store_encountered_party2, <destination>),
set_encountered_party                 = 2205  # (set_encountered_party, <party_no>),

end_current_battle                    = 1307  # (end_current_battle),

# Operations specific to dialogs

store_repeat_object                   =   50  # (store_repeat_object, <destination>),
talk_info_show                        = 2020  # (talk_info_show, <hide_or_show>),
talk_info_set_relation_bar            = 2021  # (talk_info_set_relation_bar, <value>),
talk_info_set_line                    = 2022  # (talk_info_set_line, <line_no>, <string_no>)

################################################################################
# [ Z20 ] SCENES AND MISSIONS
################################################################################

  # To put the player into a 3D scene, you need two things. First is the scene
  # itself. All scenes are defined in module_scenes.py file. The second element
  # is no less important, and it's called mission template. Mission template
  # will determine the context of the events on the scene - who will spawn
  # where, who will be hostile or friendly to player or to each other, etc.
  # Because of all this, when player is put on the 3D scene in the game, it is
  # commonly said that player is "in a mission".

# Conditional check operations

all_enemies_defeated                         = 1003  # (all_enemies_defeated, [team_id]),
race_completed_by_player                     = 1004  # (race_completed_by_player),
num_active_teams_le                          = 1005  # (num_active_teams_le, <value>),
main_hero_fallen                             = 1006  # (main_hero_fallen),
scene_allows_mounted_units                   = 1834  # (scene_allows_mounted_units),
is_zoom_disabled                             = 2222  # (is_zoom_disabled),

# Scene slot operations

scene_set_slot                               =  503  # (scene_set_slot, <scene_id>, <slot_no>, <value>),
scene_get_slot                               =  523  # (scene_get_slot, <destination>, <scene_id>, <slot_no>),
scene_slot_eq                                =  543  # (scene_slot_eq, <scene_id>, <slot_no>, <value>),
scene_slot_ge                                =  563  # (scene_slot_ge, <scene_id>, <slot_no>, <value>),

# Scene visitors handling operations

add_troop_to_site                            = 1250  # (add_troop_to_site, <troop_id>, <scene_id>, <entry_no>),
remove_troop_from_site                       = 1251  # (remove_troop_from_site, <troop_id>, <scene_id>),
modify_visitors_at_site                      = 1261  # (modify_visitors_at_site, <scene_id>),
reset_visitors                               = 1262  # (reset_visitors),
set_visitor                                  = 1263  # (set_visitor, <entry_no>, <troop_id>, [<dna>]),
set_visitors                                 = 1264  # (set_visitors, <entry_no>, <troop_id>, <number_of_troops>),
add_visitors_to_current_scene                = 1265  # (add_visitors_to_current_scene, <entry_no>, <troop_id>, <number_of_troops>, <team_no>, <group_no>),

mission_tpl_entry_set_override_flags         = 1940  # (mission_entry_set_override_flags, <mission_template_id>, <entry_no>, <value>),
mission_tpl_entry_clear_override_items       = 1941  # (mission_entry_clear_override_items, <mission_template_id>, <entry_no>),
mission_tpl_entry_add_override_item          = 1942  # (mission_entry_add_override_item, <mission_template_id>, <entry_no>, <item_kind_id>),

# Mission/scene general operations

set_mission_result                           = 1906  # (set_mission_result, <value>),
finish_mission                               = 1907  # (finish_mission, <delay_in_seconds>),
set_jump_mission                             = 1911  # (set_jump_mission, <mission_template_id>),
jump_to_scene                                = 1910  # (jump_to_scene, <scene_id>, [entry_no]),
set_jump_entry                               = 1912  # (set_jump_entry, <entry_no>),

store_current_scene                          = 2211  # (store_current_scene, <destination>),

entry_point_get_position                     = 1780  # (entry_point_get_position, <position>, <entry_no>),
entry_point_set_position                     = 1781  # (entry_point_set_position, <entry_no>, <position>),
entry_point_is_auto_generated                = 1782  # (entry_point_is_auto_generated, <entry_no>),

# Scene parameters handling

scene_set_day_time                           = 1266  # (scene_set_day_time, <value>),
set_rain                                     = 1797  # (set_rain, <rain-type>, <strength>),
set_fog_distance                             = 1798  # (set_fog_distance, <distance_in_meters>, [fog_color]),

set_skybox                                   = 2389  # (set_skybox, <non_hdr_skybox_index>, <hdr_skybox_index>),
set_startup_sun_light                        = 2390  # (set_startup_sun_light, <r>, <g>, <b>),
set_startup_ambient_light                    = 2391  # (set_startup_ambient_light, <r>, <g>, <b>),
set_startup_ground_ambient_light             = 2392  # (set_startup_ground_ambient_light, <r>, <g>, <b>),

get_battle_advantage                         = 1690  # (get_battle_advantage, <destination>),
set_battle_advantage                         = 1691  # (set_battle_advantage, <value>),

get_scene_boundaries                         = 1799  # (get_scene_boundaries, <position_min>, <position_max>),

mission_enable_talk                          = 1935  # (mission_enable_talk),
mission_disable_talk                         = 1936  # (mission_disable_talk),

mission_get_time_speed                       = 2002  # (mission_get_time_speed, <destination_fixed_point>),
mission_set_time_speed                       = 2003  # (mission_set_time_speed, <value_fixed_point>),
mission_time_speed_move_to_value             = 2004  # (mission_speed_move_to_value, <value_fixed_point>, <duration-in-1/1000-seconds>),
mission_set_duel_mode                        = 2006  # (mission_set_duel_mode, <value>),

store_zoom_amount                            = 2220  # (store_zoom_amount, <destination_fixed_point>),
set_zoom_amount                              = 2221  # (set_zoom_amount, <value_fixed_point>),

# Timers

reset_mission_timer_a                        = 2375  # (reset_mission_timer_a),
reset_mission_timer_b                        = 2376  # (reset_mission_timer_b),
reset_mission_timer_c                        = 2377  # (reset_mission_timer_c),

store_mission_timer_a                        = 2370  # (store_mission_timer_a, <destination>),
store_mission_timer_b                        = 2371  # (store_mission_timer_b, <destination>),
store_mission_timer_c                        = 2372  # (store_mission_timer_c, <destination>),

store_mission_timer_a_msec                   = 2365  # (store_mission_timer_a_msec, <destination>),
store_mission_timer_b_msec                   = 2366  # (store_mission_timer_b_msec, <destination>),
store_mission_timer_c_msec                   = 2367  # (store_mission_timer_c_msec, <destination>),

# Camera and rendering operations

mission_cam_set_mode                         = 2001  # (mission_cam_set_mode, <mission_cam_mode>, <duration-in-1/1000-seconds>, <value>) # 
mission_cam_set_screen_color                 = 2008  # (mission_cam_set_screen_color, <value>),
mission_cam_animate_to_screen_color          = 2009  #(mission_cam_animate_to_screen_color, <value>, <duration-in-1/1000-seconds>),

mission_cam_get_position                     = 2010  # (mission_cam_get_position, <position_register_no>)
mission_cam_set_position                     = 2011  # (mission_cam_set_position, <position_register_no>)
mission_cam_animate_to_position              = 2012  # (mission_cam_animate_to_position, <position_register_no>, <duration-in-1/1000-seconds>, <value>)
mission_cam_get_aperture                     = 2013  # (mission_cam_get_aperture, <destination>)
mission_cam_set_aperture                     = 2014  # (mission_cam_set_aperture, <value>)
mission_cam_animate_to_aperture              = 2015  # (mission_cam_animate_to_aperture, <value>, <duration-in-1/1000-seconds>, <value>)
mission_cam_animate_to_position_and_aperture = 2016  # (mission_cam_animate_to_position_and_aperture, <position_register_no>, <value>, <duration-in-1/1000-seconds>, <value>)
mission_cam_set_target_agent                 = 2017  # (mission_cam_set_target_agent, <agent_id>, <value>)
mission_cam_clear_target_agent               = 2018  # (mission_cam_clear_target_agent)
mission_cam_set_animation                    = 2019  # (mission_cam_set_animation, <anim_id>),

set_postfx                                   = 2386  # (set_postfx, ???)
set_river_shader_to_mud                      = 2387  # (set_river_shader_to_mud, ???)
rebuild_shadow_map                           = 2393  # (rebuild_shadow_map),

set_shader_param_int                         = 2400  # (set_shader_param_int, <parameter_name>, <value>), #Sets the int shader parameter <parameter_name> to <value>
set_shader_param_float                       = 2401  # (set_shader_param_float, <parameter_name>, <value_fixed_point>),
set_shader_param_float4                      = 2402  # (set_shader_param_float4, <parameter_name>, <valuex>, <valuey>, <valuez>, <valuew>),
set_shader_param_float4x4                    = 2403  # (set_shader_param_float4x4, <parameter_name>, [0][0], [0][1], [0][2], [1][0], [1][1], [1][2], [2][0], [2][1], [2][2], [3][0], [3][1], [3][2]),

################################################################################
# [ Z21 ] SCENE PROPS, SCENE ITEMS, LIGHT SOURCES AND PARTICLE SYSTEMS
################################################################################

  # On each scene in the game you can find scene props and scene items.

  # Scene props are the building bricks of the scene. Nearly every 3D object you
  # will see on any scene in the game is a scene prop, with the exception of
  # terrain and flora (on some scenes flora elements are actually scene props
  # as well though).

  # Just like with troops and agents, it is important to differentiate between
  # scene props and scene prop instances. You can have a dozen archer agents on
  # the scene, and each of them will be an instance of the archer troop. Scene
  # props are the same - there can be many castle wall sections on the scene,
  # and these are instances of the same castle wall scene prop.

  # It is also possible to use game items as elements of the scene. These are
  # the scene items, and they behave just like normal scene props. However all
  # operations will affect either scene prop instances, or scene items, but
  # not both.

  # Finally, there are spawned items. These are the "dropped" items which the
  # player can pick up during the mission.

prop_instance_is_valid                      = 1838  # (prop_instance_is_valid, <scene_prop_instance_id>),
prop_instance_is_animating                  = 1862  # (prop_instance_is_animating, <destination>, <scene_prop_id>),
prop_instance_intersects_with_prop_instance = 1880  # (prop_instance_intersects_with_prop_instance, <checked_scene_prop_id>, <scene_prop_id>),
scene_prop_has_agent_on_it                  = 1801  # (scene_prop_has_agent_on_it, <scene_prop_instance_id>, <agent_id>)

# Scene prop instance slot operations

scene_prop_set_slot                         =  510  # (scene_prop_set_slot, <scene_prop_instance_id>, <slot_no>, <value>),
scene_prop_get_slot                         =  530  # (scene_prop_get_slot, <destination>, <scene_prop_instance_id>, <slot_no>),
scene_prop_slot_eq                          =  550  # (scene_prop_slot_eq, <scene_prop_instance_id>, <slot_no>, <value>),
scene_prop_slot_ge                          =  570  # (scene_prop_slot_ge, <scene_prop_instance_id>, <slot_no>, <value>),

# Scene prop general operations

scene_prop_get_num_instances                = 1810  # (scene_prop_get_num_instances, <destination>, <scene_prop_id>),
scene_prop_get_instance                     = 1811  # (scene_prop_get_instance, <destination>, <scene_prop_id>, <instance_no>),

scene_prop_enable_after_time                = 1800  # (scene_prop_enable_after_time, <scene_prop_id>, <time_period>),

set_spawn_position                          = 1970  # (set_spawn_position, <position>),
spawn_scene_prop                            = 1974  # (spawn_scene_prop, <scene_prop_id>),

prop_instance_get_variation_id              = 1840  # (prop_instance_get_variation_id, <destination>, <scene_prop_id>),
prop_instance_get_variation_id_2            = 1841  # (prop_instance_get_variation_id_2, <destination>, <scene_prop_id>),

replace_prop_instance                       = 1889  # (replace_prop_instance, <scene_prop_id>, <new_scene_prop_id>),
replace_scene_props                         = 1890  # (replace_scene_props, <old_scene_prop_id>, <new_scene_prop_id>),
scene_prop_fade_out                         = 1822  # (scene_prop_fade_out, <scene_prop_id>, <fade_out_time>)
scene_prop_fade_in                          = 1823  # (scene_prop_fade_in, <scene_prop_id>, <fade_in_time>)

# Scene prop manipulation

scene_prop_get_visibility                   = 1812  # (scene_prop_get_visibility, <destination>, <scene_prop_id>),
scene_prop_set_visibility                   = 1813  # (scene_prop_set_visibility, <scene_prop_id>, <value>),
scene_prop_get_hit_points                   = 1815  # (scene_prop_get_hit_points, <destination>, <scene_prop_id>),
scene_prop_get_max_hit_points               = 1816  # (scene_prop_get_max_hit_points, <destination>, <scene_prop_id>),
scene_prop_set_hit_points                   = 1814  # (scene_prop_set_hit_points, <scene_prop_id>, <value>),
scene_prop_set_cur_hit_points               = 1820  # (scene_prop_set_cur_hit_points, <scene_prop_id>, <value>),
prop_instance_receive_damage                = 1877  # (prop_instance_receive_damage, <scene_prop_id>, <agent_id>, <damage_value>),
prop_instance_refill_hit_points             = 1870  # (prop_instance_refill_hit_points, <scene_prop_id>), 
scene_prop_get_team                         = 1817  # (scene_prop_get_team, <value>, <scene_prop_id>),
scene_prop_set_team                         = 1818  # (scene_prop_set_team, <scene_prop_id>, <value>),
scene_prop_set_prune_time                   = 1819  # (scene_prop_set_prune_time, <scene_prop_id>, <value>),

prop_instance_get_position                  = 1850  # (prop_instance_get_position, <position>, <scene_prop_id>),
prop_instance_get_starting_position         = 1851  # (prop_instance_get_starting_position, <position>, <scene_prop_id>),
prop_instance_set_position                  = 1855  # (prop_instance_set_position, <scene_prop_id>, <position>, [dont_send_to_clients]),
prop_instance_animate_to_position           = 1860  # (prop_instance_animate_to_position, <scene_prop_id>, position, <duration-in-1/100-seconds>),
prop_instance_get_animation_target_position = 1863  # (prop_instance_get_animation_target_position, <pos>, <scene_prop_id>)
prop_instance_stop_animating                = 1861  # (prop_instance_stop_animating, <scene_prop_id>),
prop_instance_get_scale                     = 1852  # (prop_instance_get_scale, <position>, <scene_prop_id>),
prop_instance_set_scale                     = 1854  # (prop_instance_set_scale, <scene_prop_id>, <value_x_fixed_point>, <value_y_fixed_point>, <value_z_fixed_point>),
prop_instance_get_scene_prop_kind           = 1853  # (prop_instance_get_scene_prop_type, <destination>, <scene_prop_id>)
prop_instance_enable_physics                = 1864  # (prop_instance_enable_physics, <scene_prop_id>, <value>),
prop_instance_initialize_rotation_angles    = 1866  # (prop_instance_initialize_rotation_angles, <scene_prop_id>),
prop_instance_rotate_to_position            = 1865  # (prop_instance_rotate_to_position, <scene_prop_id>, <position>, <duration-in-1/100-seconds>, <total_rotate_angle_fixed_point>),
prop_instance_clear_attached_missiles       = 1885  # (prop_instance_clear_attached_missiles, <scene_prop_id>),

prop_instance_dynamics_set_properties       = 1871  # (prop_instance_dynamics_set_properties, <scene_prop_id>, <position>),
prop_instance_dynamics_set_velocity         = 1872  # (prop_instance_dynamics_set_velocity, <scene_prop_id>, <position>),
prop_instance_dynamics_set_omega            = 1873  # (prop_instance_dynamics_set_omega, <scene_prop_id>, <position>),
prop_instance_dynamics_apply_impulse        = 1874  # (prop_instance_dynamics_apply_impulse, <scene_prop_id>, <position>),

prop_instance_play_sound                    = 1881  # (prop_instance_play_sound, <scene_prop_id>, <sound_id>, [flags]),
prop_instance_stop_sound                    = 1882  # (prop_instance_stop_sound, <scene_prop_id>),

# Scene items operations

scene_item_get_num_instances                = 1830  # (scene_item_get_num_instances, <destination>, <item_id>),
scene_item_get_instance                     = 1831  # (scene_item_get_instance, <destination>, <item_id>, <instance_no>),
scene_spawned_item_get_num_instances        = 1832  # (scene_spawned_item_get_num_instances, <destination>, <item_id>),
scene_spawned_item_get_instance             = 1833  # (scene_spawned_item_get_instance, <destination>, <item_id>, <instance_no>),

replace_scene_items_with_scene_props        = 1891  # (replace_scene_items_with_scene_props, <old_item_id>, <new_scene_prop_id>),

set_spawn_position                          = 1970  # (set_spawn_position, <position>) ## DUPLICATE ENTRY
spawn_item                                  = 1971  # (spawn_item, <item_kind_id>, <item_modifier>, [seconds_before_pruning]),
spawn_item_without_refill                   = 1976  # (spawn_item_without_refill, <item_kind_id>, <item_modifier>, [seconds_before_pruning]),

# Light sources and particle systems

set_current_color                           = 1950  # (set_current_color, <red_value>, <green_value>, <blue_value>),
set_position_delta                          = 1955  # (set_position_delta, <value>, <value>, <value>),
add_point_light                             = 1960  # (add_point_light, [flicker_magnitude], [flicker_interval]),
add_point_light_to_entity                   = 1961  # (add_point_light_to_entity, [flicker_magnitude], [flicker_interval]),
particle_system_add_new                     = 1965  # (particle_system_add_new, <par_sys_id>,[position]),
particle_system_emit                        = 1968  # (particle_system_emit, <par_sys_id>, <value_num_particles>, <value_period>),
particle_system_burst                       = 1969  # (particle_system_burst, <par_sys_id>, <position>, [percentage_burst_strength]),
particle_system_burst_no_sync               = 1975  # (particle_system_burst_without_sync,<par_sys_id>,<position_no>,[percentage_burst_strength]),
prop_instance_add_particle_system           = 1886  # (prop_instance_add_particle_system, <scene_prop_id>, <par_sys_id>, <position_no>),
prop_instance_stop_all_particle_systems     = 1887  # (prop_instance_stop_all_particle_systems, <scene_prop_id>),

################################################################################
# [ Z22 ] TEAMS AND AGENTS
################################################################################

  # An agent represents of a single soldier on the 3D scene. Always keep this in
  # mind when dealing with regular troops. A party may have 30 Swadian Knights.
  # They will form a single troop stack in the party, and they will all be
  # copies of the one and only Swadian Knight troop. However when the battle
  # starts, this stack will spawn 30 distinct Agents.

  # Agents do not persist - they only exist in the game for the duration of the
  # mission. As soon as the player returns to the world map, all agents who were
  # present on the scene immediately disappear. If this was a battle during a
  # normal game encounter, then the game will keep track of the battle results,
  # and depending on the number of agents killed from all sides the engine will
  # kill or wound some troops in the troop stacks of the parties who were
  # participating in the battle.

  # During the mission, all agents are split into teams. By default player and
  # his companions are placed into Team 0, but this may be changed in the
  # mission template or by code. Player's enemies are usually team 1 (though
  # again, this is not set in stone). Module System provides the modder with
  # a great degree of control over teams composition, relation to each other
  # (you can make hostile, allied or neutral teams, and you can have more than
  # one team on the scene).

# Conditional check operations

agent_is_in_special_mode                 = 1693  # (agent_is_in_special_mode, <agent_id>),
agent_is_routed                          = 1699  # (agent_is_routed, <agent_id>),
agent_is_alive                           = 1702  # (agent_is_alive, <agent_id>),
agent_is_wounded                         = 1703  # (agent_is_wounded, <agent_id>),
agent_is_human                           = 1704  # (agent_is_human, <agent_id>),
agent_is_ally                            = 1706  # (agent_is_ally, <agent_id>),
agent_is_non_player                      = 1707  # (agent_is_non_player, <agent_id>),
agent_is_defender                        = 1708  # (agent_is_defender, <agent_id>),
agent_is_active                          = 1712  # (agent_is_active, <agent_id>),
agent_has_item_equipped                  = 1729  # (agent_has_item_equipped, <agent_id>, <item_id>),
agent_is_in_parried_animation            = 1769  # (agent_is_in_parried_animation, <agent_id>),
agent_is_alarmed                         = 1806  # (agent_is_alarmed, <agent_id>),
class_is_listening_order                 = 1775  # (class_is_listening_order, <team_no>, <sub_class>),
teams_are_enemies                        = 1788  # (teams_are_enemies, <team_no>, <team_no_2>), 
agent_is_in_line_of_sight                = 1826  # (agent_is_in_line_of_sight, <agent_id>, <position_no>),

# Team and agent slot operations

team_set_slot                            =  509  # (team_set_slot, <team_id>, <slot_no>, <value>),
team_get_slot                            =  529  # (team_get_slot, <destination>, <player_id>, <slot_no>),
team_slot_eq                             =  549  # (team_slot_eq, <team_id>, <slot_no>, <value>),
team_slot_ge                             =  569  # (team_slot_ge, <team_id>, <slot_no>, <value>),

agent_set_slot                           =  505  # (agent_set_slot, <agent_id>, <slot_no>, <value>),
agent_get_slot                           =  525  # (agent_get_slot, <destination>, <agent_id>, <slot_no>),
agent_slot_eq                            =  545  # (agent_slot_eq, <agent_id>, <slot_no>, <value>),
agent_slot_ge                            =  565  # (agent_slot_ge, <agent_id>, <slot_no>, <value>),

# Agent spawning, removal and general operations

add_reinforcements_to_entry              = 1930  # (add_reinforcements_to_entry, <mission_template_entry_no>, <wave_size>),
set_spawn_position                       = 1970  # (set_spawn_position, <position>),
spawn_agent                              = 1972  # (spawn_agent, <troop_id>),
spawn_horse                              = 1973  # (spawn_horse, <item_kind_id>, <item_modifier>),
remove_agent                             = 1755  # (remove_agent, <agent_id>),
agent_fade_out                           = 1749  # (agent_fade_out, <agent_id>),
agent_play_sound                         = 1750  # (agent_play_sound, <agent_id>, <sound_id>),
agent_stop_sound                         = 1808  # (agent_stop_sound, <agent_id>),
agent_set_visibility                     = 2096  # (agent_set_visibility, <agent_id>, <value>),

get_player_agent_no                      = 1700  # (get_player_agent_no, <destination>),
agent_get_player_id                      = 1724  # (agent_get_player_id, <destination>, <agent_id>),
agent_get_kill_count                     = 1723  # (agent_get_kill_count, <destination>, <agent_id>, [get_wounded]),

agent_get_position                       = 1710  # (agent_get_position, <position>, <agent_id>),
agent_set_position                       = 1711  # (agent_set_position, <agent_id>, <position>),
agent_get_horse                          = 1714  # (agent_get_horse, <destination>, <agent_id>),
agent_get_rider                          = 1715  # (agent_get_rider, <destination>, <horse_agent_id>),
agent_get_party_id                       = 1716  # (agent_get_party_id, <destination>, <agent_id>),
agent_get_entry_no                       = 1717  # (agent_get_entry_no, <destination>, <agent_id>),
agent_get_troop_id                       = 1718  # (agent_get_troop_id, <destination>, <agent_id>),
agent_get_item_id                        = 1719  # (agent_get_item_id, <destination>, <horse_agent_id>),

# Agent combat parameters and stats

store_agent_hit_points                   = 1720  # (store_agent_hit_points, <destination>, <agent_id>, [absolute]),
agent_set_hit_points                     = 1721  # (agent_set_hit_points, <agent_id>, <value>,[absolute]),
agent_set_max_hit_points                 = 2090  # (agent_set_max_hit_points, <agent_id>, <value>, [absolute]),
agent_deliver_damage_to_agent            = 1722  # (agent_deliver_damage_to_agent, <agent_id_deliverer>, <agent_id>, [damage_amount], [weapon_item_id]),
agent_deliver_damage_to_agent_advanced   = 1827  # (agent_deliver_damage_to_agent_advanced, <destination>, <attacker_agent_id>, <agent_id>, <value>, [weapon_item_id]), #if value <= 0, then damage will be calculated using the weapon item. # item_id is the item that the damage is delivered. can be ignored.
add_missile                              = 1829  # (add_missile, <agent_id>, <starting_position>, <starting_speed_fixed_point>, <weapon_item_id>, <weapon_item_modifier>, <missile_item_id>, <missile_item_modifier>),

agent_get_speed                          = 1689  # (agent_get_speed, <position>, <agent_id>),
agent_set_no_death_knock_down_only       = 1733  # (agent_set_no_death_knock_down_only, <agent_id>, <value>),
agent_set_horse_speed_factor             = 1734  # (agent_set_horse_speed_factor, <agent_id>, <speed_multiplier-in-1/100>),
agent_set_speed_limit                    = 1736  # (agent_set_speed_limit, <agent_id>, <speed_limit(kilometers/hour)>),
agent_set_damage_modifier                = 2091  # (agent_set_damage_modifier, <agent_id>, <value>),
agent_set_accuracy_modifier              = 2092  # (agent_set_accuracy_modifier, <agent_id>, <value>),
agent_set_speed_modifier                 = 2093  # (agent_set_speed_modifier, <agent_id>, <value>),
agent_set_reload_speed_modifier          = 2094  # (agent_set_reload_speed_modifier, <agent_id>, <value>),
agent_set_use_speed_modifier             = 2095  # (agent_set_use_speed_modifier, <agent_id>, <value>),
agent_get_time_elapsed_since_removed     = 1760  # (agent_get_time_elapsed_since_removed, <destination>, <agent_id>),

# Agent equipment

agent_refill_wielded_shield_hit_points   = 1692  # (agent_refill_wielded_shield_hit_points, <agent_id>),
agent_set_invulnerable_shield            = 1725  # (agent_set_invulnerable_shield, <agent_id>, <value>),
agent_get_wielded_item                   = 1726  # (agent_get_wielded_item, <destination>, <agent_id>, <hand_no>),
agent_get_ammo                           = 1727  # (agent_get_ammo, <destination>, <agent_id>, <value>),
agent_get_item_cur_ammo                  = 1977  # (agent_get_item_cur_ammo, <destination>, <agent_id>, <slot_no>),
agent_refill_ammo                        = 1728  # (agent_refill_ammo, <agent_id>),
agent_set_wielded_item                   = 1747  # (agent_set_wielded_item, <agent_id>, <item_id>),
agent_equip_item                         = 1779  # (agent_equip_item, <agent_id>, <item_id>, [weapon_slot_no]),
agent_unequip_item                       = 1774  # (agent_unequip_item, <agent_id>, <item_id>, [weapon_slot_no]),
agent_set_ammo                           = 1776  # (agent_set_ammo, <agent_id>, <item_id>, <value>),
agent_get_item_slot                      = 1804  # (agent_get_item_slot, <destination>, <agent_id>, <value>),
agent_get_ammo_for_slot                  = 1825  # (agent_get_ammo_for_slot, <destination>, <agent_id>, <slot_no>),

# Agent animations

agent_set_no_dynamics                    = 1762  # (agent_set_no_dynamics, <agent_id>, <value>),

agent_get_animation                      = 1768  # (agent_get_animation, <destination>, <agent_id>, <body_part),
agent_set_animation                      = 1740  # (agent_set_animation, <agent_id>, <anim_id>, [channel_no]),
agent_set_stand_animation                = 1741  # (agent_set_stand_action, <agent_id>, <anim_id>),
agent_set_walk_forward_animation         = 1742  # (agent_set_walk_forward_action, <agent_id>, <anim_id>),
agent_set_animation_progress             = 1743  # (agent_set_animation_progress, <agent_id>, <value_fixed_point>),
agent_ai_set_can_crouch                  = 2083  # (agent_ai_set_can_crouch, <agent_id>, <value>),
agent_get_crouch_mode                    = 2097  # (agent_ai_get_crouch_mode, <destination>, <agent_id>),
agent_set_crouch_mode                    = 2098  # (agent_ai_set_crouch_mode, <agent_id>, <value>),

agent_get_attached_scene_prop            = 1756  # (agent_get_attached_scene_prop, <destination>, <agent_id>)
agent_set_attached_scene_prop            = 1757  # (agent_set_attached_scene_prop, <agent_id>, <scene_prop_id>)
agent_set_attached_scene_prop_x          = 1758  # (agent_set_attached_scene_prop_x, <agent_id>, <value>)
agent_set_attached_scene_prop_y          = 1809  # (agent_set_attached_scene_prop_y, <agent_id>, <value>)
agent_set_attached_scene_prop_z          = 1759  # (agent_set_attached_scene_prop_z, <agent_id>, <value>)

# Agent AI and scripted behavior

agent_set_is_alarmed                     = 1807  # (agent_set_is_alarmed, <agent_id>, <value>),
agent_clear_relations_with_agents        = 1802  # (agent_clear_relations_with_agents, <agent_id>),
agent_add_relation_with_agent            = 1803  # (agent_add_relation_with_agent, <agent_id>, <agent_id>, <value>),

agent_get_number_of_enemies_following    = 1761  # (agent_get_number_of_enemies_following, <destination>, <agent_id>),

agent_get_attack_action                  = 1763  # (agent_get_attack_action, <destination>, <agent_id>),
agent_get_defend_action                  = 1764  # (agent_get_defend_action, <destination>, <agent_id>),
agent_get_action_dir                     = 1767  # (agent_get_action_dir, <destination>, <agent_id>),
agent_set_attack_action                  = 1745  # (agent_set_attack_action, <agent_id>, <direction_value>, <action_value>),
agent_set_defend_action                  = 1746  # (agent_set_defend_action, <agent_id>, <value>, <duration-in-1/1000-seconds>),

agent_set_scripted_destination           = 1730  # (agent_set_scripted_destination, <agent_id>, <position>, [auto_set_z_to_ground_level]),
agent_set_scripted_destination_no_attack = 1748  # (agent_set_scripted_destination_no_attack, <agent_id>, <position>, <auto_set_z_to_ground_level>),
agent_get_scripted_destination           = 1731  # (agent_get_scripted_destination, <position>, <agent_id>),
agent_force_rethink                      = 1732  # (agent_force_rethink, <agent_id>),
agent_clear_scripted_mode                = 1735  # (agent_clear_scripted_mode, <agent_id>),
agent_ai_set_always_attack_in_melee      = 1737  # (agent_ai_set_always_attack_in_melee, <agent_id>, <value>),
agent_get_simple_behavior                = 1738  # (agent_get_simple_behavior, <destination>, <agent_id>),
agent_ai_get_behavior_target             = 2082  # (agent_ai_get_behavior_target, <destination>, <agent_id>),
agent_get_combat_state                   = 1739  # (agent_get_combat_state, <destination>, <agent_id>),
                                                 #   0 = nothing special, this value is also always returned for player and for dead agents.
                                                 #   2 = guarding (without a shield)
                                                 #   4 = releasing a melee attack or reloading a crossbow
                                                 #   8 = target to the right (horse archers) OR no target in sight (ranged units). Contradictory information, 4research.

agent_ai_get_move_target                 = 2081  # (agent_ai_get_move_target, <destination>, <agent_id>),
agent_get_look_position                  = 1709  # (agent_get_look_position, <position>, <agent_id>),
agent_set_look_target_position           = 1744  # (agent_set_look_target_position, <agent_id>, <position>),
agent_ai_get_look_target                 = 2080  # (agent_ai_get_look_target, <destination>, <agent_id>),
agent_set_look_target_agent              = 1713  # (agent_set_look_target_agent, <watcher_agent_id>, <observed_agent_id>),
agent_start_running_away                 = 1751  # (agent_start_running_away, <agent_id>, [<position_no>]),
agent_stop_running_away                  = 1752  # (agent_stop_run_away, <agent_id>),
agent_ai_set_aggressiveness              = 1753  # (agent_ai_set_aggressiveness, <agent_id>, <value>),
agent_set_kick_allowed                   = 1754  # (agent_set_kick_allowed, <agent_id>, <value>),
set_cheer_at_no_enemy                    = 2379  # (set_cheer_at_no_enemy, <value>),

agent_add_offer_with_timeout             = 1777  # (agent_add_offer_with_timeout, <agent_id>, <offerer_agent_id>, <duration-in-1/1000-seconds>),
agent_check_offer_from_agent             = 1778  # (agent_check_offer_from_agent, <agent_id>, <offerer_agent_id>), #second agent_id is offerer

# Team operations

agent_get_group                          = 1765  # (agent_get_group, <destination>, <agent_id>),
agent_set_group                          = 1766  # (agent_set_group, <agent_id>, <player_leader_id>),

agent_get_team                           = 1770  # (agent_get_team, <destination>, <agent_id>),
agent_set_team                           = 1771  # (agent_set_team, <agent_id>, <value>),
agent_get_class                          = 1772  # (agent_get_class , <destination>, <agent_id>),
agent_get_division                       = 1773  # (agent_get_division , <destination>, <agent_id>),
agent_set_division                       = 1783  # (agent_set_division, <agent_id>, <value>),

team_get_hold_fire_order                 = 1784  # (team_get_hold_fire_order, <destination>, <team_no>, <division>),
team_get_movement_order                  = 1785  # (team_get_movement_order, <destination>, <team_no>, <division>),
team_get_riding_order                    = 1786  # (team_get_riding_order, <destination>, <team_no>, <division>),
team_get_weapon_usage_order              = 1787  # (team_get_weapon_usage_order, <destination>, <team_no>, <division>),
team_give_order                          = 1790  # (team_give_order, <team_no>, <division>, <order_id>),
team_set_order_position                  = 1791  # (team_set_order_position, <team_no>, <division>, <position>),
team_get_leader                          = 1792  # (team_get_leader, <destination>, <team_no>),
team_set_leader                          = 1793  # (team_set_leader, <team_no>, <new_leader_agent_id>),
team_get_order_position                  = 1794  # (team_get_order_position, <position>, <team_no>, <division>),
team_set_order_listener                  = 1795  # (team_set_order_listener, <team_no>, <division>, [add_to_listeners]),
team_set_relation                        = 1796  # (team_set_relation, <team_no>, <team_no_2>, <value>),
store_remaining_team_no                  = 2360  # (store_remaining_team_no, <destination>),
team_get_gap_distance                    = 1828  # (team_get_gap_distance, <destination>, <team_no>, <sub_class>),

# Combat statistics

store_enemy_count                        = 2380  # (store_enemy_count, <destination>),
store_friend_count                       = 2381  # (store_friend_count, <destination>),
store_ally_count                         = 2382  # (store_ally_count, <destination>),
store_defender_count                     = 2383  # (store_defender_count, <destination>),
store_attacker_count                     = 2384  # (store_attacker_count, <destination>),
store_normalized_team_count              = 2385  # (store_normalized_team_count, <destination>, <team_no>),

################################################################################
# [ Z23 ] PRESENTATIONS
################################################################################

  # Presentations are a complex subject, because of their flexibility. Each
  # presentation is nothing more but a number of screen control elements, called
  # overlays. There are many types of overlays, each coming with it's own
  # behavior and looks. For as long as the presentation is running, you can
  # monitor the status of those overlays and change their looks, contents and
  # position on the screen.

  # Presentation is nothing but a set of triggers. There are only five triggers
  # that the presentation can have, but skillful control of them allows you to
  # do nearly everything you can think of.

  # ti_on_presentation_load fires only once when the presentation is started.
  # This is the place where you will usually create all overlays that your
  # presentation needs, initialize their looks and contents and put them to
  # their positions on the screen.

  # ti_on_presentation_event_state_change is probably the most important and
  # easy one. It fires every time some overlay in your presentation changes
  # state. For each type of overlay this means something. For a button overlay,
  # this means that the user has clicked the button. In this case, you will want
  # to run the code responsible for that button effects. So you can put a "Win"
  # button on your presentation, and when it's clicked, you can run the code
  # which will give all castles and towns in the game to you. :-)

  # ti_on_presentation_mouse_press trigger fires every time user clicks a mouse
  # button on one of presentation overlays, even if the overlay did not change
  # it's state as the result.

  # ti_on_presentation_mouse_enter_leave trigger fires when the mouse pointer
  # moves over one of presentation's overlays, or moves out of it. This might
  # be useful if you want your presentation to react to user's mouse movements,
  # not only clicks.

  # ti_on_presentation_run trigger will fire every frame (in other words, with
  # the frequency of your game FPS). You can put some code in this trigger if
  # you want your presentation to constantly do something even if the user is
  # passive.

  # Note that while a running presentation will usually pause your game until
  # you stop it, it is also possible to write presentations which will not stop
  # the game, but will run as the time goes. To see an example, go into any
  # battle in Warband and press Backspace. You will see the interface which
  # displays the mini-map of the battle, positions of all troops, and elements
  # that you can use to issue orders to your companions (if you have any). All
  # this is a presentation as well, called "prsnt_battle". And if you have
  # played multiplayer, then you might be interested to know that all menus,
  # including equipment selection for your character, are presentations as well.

# Conditional check operations

is_presentation_active                            =  903  # (is_presentation_active, <presentation_id),

# General presentation operations

start_presentation                                =  900  # (start_presentation, <presentation_id>),
start_background_presentation                     =  901  # (start_background_presentation, <presentation_id>),
presentation_set_duration                         =  902  # (presentation_set_duration, <duration-in-1/100-seconds>),

# Creating overlays

create_text_overlay                               =  910  # (create_text_overlay, <destination>, <string_id>),
create_mesh_overlay                               =  911  # (create_mesh_overlay, <destination>, <mesh_id>),
create_mesh_overlay_with_item_id                  =  944  # (create_mesh_overlay_with_item_id, <destination>, <item_id>),
create_mesh_overlay_with_tableau_material         =  939  # (create_mesh_overlay_with_tableau_material, <destination>, <mesh_id>, <tableau_material_id>, <value>),
create_button_overlay                             =  912  # (create_button_overlay, <destination>, <string_id>),
create_game_button_overlay                        =  940  # (create_game_button_overlay, <destination>, <string_id>),
create_in_game_button_overlay                     =  941  # (create_in_game_button_overlay, <destination>, <string_id>),
create_image_button_overlay                       =  913  # (create_image_button_overlay, <destination>, <mesh_id>, <mesh_id>),
create_image_button_overlay_with_tableau_material =  938  # (create_image_button_overlay_with_tableau_material, <destination>, <mesh_id>, <tableau_material_id>, <value>),
create_slider_overlay                             =  914  # (create_slider_overlay, <destination>, <min_value>, <max_value>),
create_progress_overlay                           =  915  # (create_progress_overlay, <destination>, <min_value>, <max_value>),
create_number_box_overlay                         =  942  # (create_number_box_overlay, <destination>, <min_value>, <max_value>),
create_text_box_overlay                           =  917  # (create_text_box_overlay, <destination>),
create_simple_text_box_overlay                    =  919  # (create_simple_text_box_overlay, <destination>),
create_check_box_overlay                          =  918  # (create_check_box_overlay, <destination>),
create_listbox_overlay                            =  943  # (create_list_box_overlay, <destination>, <string>, <value>),
create_combo_label_overlay                        =  948  # (create_combo_label_overlay, <destination>),
create_combo_button_overlay                       =  916  # (create_combo_button_overlay, <destination>),
overlay_add_item                                  =  931  # (overlay_add_item, <overlay_id>, <string_id>),

# Overlays hierarchy manipulation

set_container_overlay                             =  945  # (set_container_overlay, <overlay_id>),
overlay_set_container_overlay                     =  951  # (overlay_set_container_overlay, <overlay_id>, <container_overlay_id>),

# Overlay manipulation

overlay_get_position                              =  946  # (overlay_get_position, <position>, <overlay_id>)
overlay_set_val                                   =  927  # (overlay_set_val, <overlay_id>, <value>),
overlay_set_text                                  =  920  # (overlay_set_text, <overlay_id>, <string_id>),
overlay_set_boundaries                            =  928  # (overlay_set_boundaries, <overlay_id>, <min_value>, <max_value>),
overlay_set_position                              =  926  # (overlay_set_position, <overlay_id>, <position>),
overlay_set_size                                  =  925  # (overlay_set_size, <overlay_id>, <position>),
overlay_set_area_size                             =  929  # (overlay_set_area_size, <overlay_id>, <position>),
overlay_set_additional_render_height              =  952  # (overlay_set_additional_render_height, <overlay_id>, <height_adder>),
overlay_animate_to_position                       =  937  # (overlay_animate_to_position, <overlay_id>, <duration-in-1/1000-seconds>, <position>),
overlay_animate_to_size                           =  936  # (overlay_animate_to_size, <overlay_id>, <duration-in-1/1000-seconds>, <position>),
overlay_set_mesh_rotation                         =  930  # (overlay_set_mesh_rotation, <overlay_id>, <position>),
overlay_set_color                                 =  921  # (overlay_set_color, <overlay_id>, <color>),
overlay_set_alpha                                 =  922  # (overlay_set_alpha, <overlay_id>, <alpha>),
overlay_set_hilight_color                         =  923  # (overlay_set_hilight_color, <overlay_id>, <color>),
overlay_set_hilight_alpha                         =  924  # (overlay_set_hilight_alpha, <overlay_id>, <alpha>),
overlay_animate_to_color                          =  932  # (overlay_animate_to_color, <overlay_id>, <duration-in-1/1000-seconds>, <color>)
overlay_animate_to_alpha                          =  933  # (overlay_animate_to_alpha, <overlay_id>, <duration-in-1/1000-seconds>, <color>),
overlay_animate_to_highlight_color                =  934  # (overlay_animate_to_highlight_color, <overlay_id>, <duration-in-1/1000-seconds>, <color>),
overlay_animate_to_highlight_alpha                =  935  # (overlay_animate_to_highlight_alpha, <overlay_id>, <duration-in-1/1000-seconds>, <color>),
overlay_set_display                               =  947  # (overlay_set_display, <overlay_id>, <value>),
overlay_obtain_focus                              =  949  # (overlay_obtain_focus, <overlay_id>),

overlay_set_tooltip                               =  950  # (overlay_set_tooltip, <overlay_id>, <string_id>),

# Popups and some esoteric stuff

show_item_details                                 =  970  # (show_item_details, <item_id>, <position>, <price_multiplier_percentile>),
show_item_details_with_modifier                   =  972  # (show_item_details_with_modifier, <item_id>, <item_modifier>, <position>, <price_multiplier_percentile>),
close_item_details                                =  971  # (close_item_details)
show_troop_details                                = 2388  # (show_troop_details, <troop_id>, <position>, <troop_price>)

################################################################################
# [ Z24 ] MULTIPLAYER AND NETWORKING (LEFT FOR SOMEONE MORE FAMILIAR WITH THIS)
################################################################################

  # This section is eagerly waiting for someone to write documentation comments.

# Conditional check operations

player_is_active                             =  401  # (player_is_active, <player_id>),
multiplayer_is_server                        =  417  # (multiplayer_is_server),
multiplayer_is_dedicated_server              =  418  # (multiplayer_is_dedicated_server),
game_in_multiplayer_mode                     =  419  # (game_in_multiplayer_mode),
player_is_admin                              =  430  # (player_is_admin, <player_id>),
player_is_busy_with_menus                    =  438  # (player_is_busy_with_menus, <player_id>),
player_item_slot_is_picked_up                =  461  # (player_item_slot_is_picked_up, <player_id>, <item_slot_no>), #item slots are overriden when player picks up an item and stays alive until the next round

# Player slot operations

player_set_slot                              =  508  # (player_set_slot, <player_id>, <slot_no>, <value>),
player_get_slot                              =  528  # (player_get_slot, <destination>, <player_id>, <slot_no>),
player_slot_eq                               =  548  # (player_slot_eq, <player_id>, <slot_no>, <value>),
player_slot_ge                               =  568  # (player_slot_ge, <player_id>, <slot_no>, <value>),

# Network communication operations

send_message_to_url                          =  380  # (send_message_to_url, <string_id>, <encode_url>), #result will be returned to script_game_receive_url_response

multiplayer_send_message_to_server           =  388  # (multiplayer_send_int_to_server, <message_type>),
multiplayer_send_int_to_server               =  389  # (multiplayer_send_int_to_server, <message_type>, <value>),
multiplayer_send_2_int_to_server             =  390  # (multiplayer_send_2_int_to_server, <message_type>, <value>, <value>),
multiplayer_send_3_int_to_server             =  391  # (multiplayer_send_3_int_to_server, <message_type>, <value>, <value>, <value>),
multiplayer_send_4_int_to_server             =  392  # (multiplayer_send_4_int_to_server, <message_type>, <value>, <value>, <value>, <value>),
multiplayer_send_string_to_server            =  393  # (multiplayer_send_string_to_server, <message_type>, <string_id>),
multiplayer_send_message_to_player           =  394  # (multiplayer_send_message_to_player, <player_id>, <message_type>),
multiplayer_send_int_to_player               =  395  # (multiplayer_send_int_to_player, <player_id>, <message_type>, <value>),
multiplayer_send_2_int_to_player             =  396  # (multiplayer_send_2_int_to_player, <player_id>, <message_type>, <value>, <value>),
multiplayer_send_3_int_to_player             =  397  # (multiplayer_send_3_int_to_player, <player_id>, <message_type>, <value>, <value>, <value>),
multiplayer_send_4_int_to_player             =  398  # (multiplayer_send_4_int_to_player, <player_id>, <message_type>, <value>, <value>, <value>, <value>),
multiplayer_send_string_to_player            =  399  # (multiplayer_send_string_to_player, <player_id>, <message_type>, <string_id>),

# Player handling operations

get_max_players                              =  400  # (get_max_players, <destination>),
player_get_team_no                           =  402  # (player_get_team_no,  <destination>, <player_id>),
player_set_team_no                           =  403  # (player_get_team_no,  <destination>, <player_id>),
player_get_troop_id                          =  404  # (player_get_troop_id, <destination>, <player_id>),
player_set_troop_id                          =  405  # (player_get_troop_id, <destination>, <player_id>),
player_get_agent_id                          =  406  # (player_get_agent_id, <destination>, <player_id>),
player_get_gold                              =  407  # (player_get_gold, <destination>, <player_id>),
player_set_gold                              =  408  # (player_set_gold, <player_id>, <value>, <max_value>), #set max_value to 0 if no limit is wanted
player_spawn_new_agent                       =  409  # (player_spawn_new_agent, <player_id>, <entry_point>),
player_add_spawn_item                        =  410  # (player_add_spawn_item, <player_id>, <item_slot_no>, <item_id>),
multiplayer_get_my_team                      =  411  # (multiplayer_get_my_team, <destination>),
multiplayer_get_my_troop                     =  412  # (multiplayer_get_my_troop, <destination>),
multiplayer_set_my_troop                     =  413  # (multiplayer_get_my_troop, <destination>),
multiplayer_get_my_gold                      =  414  # (multiplayer_get_my_gold, <destination>),
multiplayer_get_my_player                    =  415  # (multiplayer_get_my_player, <destination>),

multiplayer_make_everyone_enemy              =  420  # (multiplayer_make_everyone_enemy),
player_control_agent                         =  421  # (player_control_agent, <player_id>, <agent_id>),
player_get_item_id                           =  422  # (player_get_item_id, <destination>, <player_id>, <item_slot_no>) #only for server
player_get_banner_id                         =  423  # (player_get_banner_id, <destination>, <player_id>),

player_set_is_admin                          =  429  # (player_set_is_admin, <player_id>, <value>), #value is 0 or 1
player_get_score                             =  431  # (player_get_score, <destination>, <player_id>),
player_set_score                             =  432  # (player_set_score, <player_id>, <value>),
player_get_kill_count                        =  433  # (player_get_kill_count, <destination>, <player_id>),
player_set_kill_count                        =  434  # (player_set_kill_count, <player_id>, <value>),
player_get_death_count                       =  435  # (player_get_death_count, <destination>, <player_id>),
player_set_death_count                       =  436  # (player_set_death_count, <player_id>, <value>),
player_get_ping                              =  437  # (player_get_ping, <destination>, <player_id>),
player_get_is_muted                          =  439  # (player_get_is_muted, <destination>, <player_id>),
player_set_is_muted                          =  440  # (player_set_is_muted, <player_id>, <value>, [mute_for_everyone]), #mute_for_everyone optional parameter should be set to 1 if player is muted for everyone (this works only on server).
player_get_unique_id                         =  441  # (player_get_unique_id, <destination>, <player_id>), #can only bew used on server side
player_get_gender                            =  442  # (player_get_gender, <destination>, <player_id>),

player_save_picked_up_items_for_next_spawn   =  459  # (player_save_picked_up_items_for_next_spawn, <player_id>),
player_get_value_of_original_items           =  460  # (player_get_value_of_original_items, <player_id>), #this operation returns values of the items, but default troop items will be counted as zero (except horse)

profile_get_banner_id                        =  350  # (profile_get_banner_id, <destination>),
profile_set_banner_id                        =  351  # (profile_set_banner_id, <value>),

# Team handling operations

team_get_bot_kill_count                      =  450  # (team_get_bot_kill_count, <destination>, <team_id>),
team_set_bot_kill_count                      =  451  # (team_get_bot_kill_count, <destination>, <team_id>),
team_get_bot_death_count                     =  452  # (team_get_bot_death_count, <destination>, <team_id>),
team_set_bot_death_count                     =  453  # (team_get_bot_death_count, <destination>, <team_id>),
team_get_kill_count                          =  454  # (team_get_kill_count, <destination>, <team_id>),
team_get_score                               =  455  # (team_get_score, <destination>, <team_id>),
team_set_score                               =  456  # (team_set_score, <team_id>, <value>),
team_set_faction                             =  457  # (team_set_faction, <team_id>, <faction_id>),
team_get_faction                             =  458  # (team_get_faction, <destination>, <team_id>),

# General scene and mission handling operations

multiplayer_clear_scene                      =  416  # (multiplayer_clear_scene),
game_get_reduce_campaign_ai                  =  424  # (game_get_reduce_campaign_ai, <destination>), #depreciated, use options_get_campaign_ai instead
multiplayer_find_spawn_point                 =  425  # (multiplayer_find_spawn_point, <destination>, <team_no>, <examine_all_spawn_points>, <is_horseman>), 
set_spawn_effector_scene_prop_kind           =  426  # (set_spawn_effector_scene_prop_kind <team_no> <scene_prop_kind_no>)
set_spawn_effector_scene_prop_id             =  427  # (set_spawn_effector_scene_prop_id <scene_prop_id>)

start_multiplayer_mission                    =  470  # (start_multiplayer_mission, <mission_template_id>, <scene_id>, <started_manually>),

# Administrative operations and settings

kick_player                                  =  465  # (kick_player, <player_id>),
ban_player                                   =  466  # (ban_player, <player_id>, <value>, <player_id>), #set value = 1 for banning temporarily, assign 2nd player id as the administrator player id if banning is permanent
save_ban_info_of_player                      =  467  # (save_ban_info_of_player, <player_id>),
ban_player_using_saved_ban_info              =  468  # (ban_player_using_saved_ban_info),

server_add_message_to_log                    =  473  # (server_add_message_to_log, <string_id>),

server_get_renaming_server_allowed           =  475  # (server_get_renaming_server_allowed, <destination>), #0-1
server_get_changing_game_type_allowed        =  476  # (server_get_changing_game_type_allowed, <destination>), #0-1
server_get_combat_speed                      =  478  # (server_get_combat_speed, <destination>), #0-2
server_set_combat_speed                      =  479  # (server_set_combat_speed, <value>), #0-2
server_get_friendly_fire                     =  480  # (server_get_friendly_fire, <destination>),
server_set_friendly_fire                     =  481  # (server_set_friendly_fire, <value>), #0 = off, 1 = on
server_get_control_block_dir                 =  482  # (server_get_control_block_dir, <destination>),
server_set_control_block_dir                 =  483  # (server_set_control_block_dir, <value>), #0 = automatic, 1 = by mouse movement
server_set_password                          =  484  # (server_set_password, <string_id>),
server_get_add_to_game_servers_list          =  485  # (server_get_add_to_game_servers_list, <destination>),
server_set_add_to_game_servers_list          =  486  # (server_set_add_to_game_servers_list, <value>),
server_get_ghost_mode                        =  487  # (server_get_ghost_mode, <destination>),
server_set_ghost_mode                        =  488  # (server_set_ghost_mode, <value>),
server_set_name                              =  489  # (server_set_name, <string_id>),
server_get_max_num_players                   =  490  # (server_get_max_num_players, <destination>),
server_set_max_num_players                   =  491  # (server_set_max_num_players, <value>),
server_set_welcome_message                   =  492  # (server_set_welcome_message, <string_id>),
server_get_melee_friendly_fire               =  493  # (server_get_melee_friendly_fire, <destination>),
server_set_melee_friendly_fire               =  494  # (server_set_melee_friendly_fire, <value>), #0 = off, 1 = on
server_get_friendly_fire_damage_self_ratio   =  495  # (server_get_friendly_fire_damage_self_ratio, <destination>),
server_set_friendly_fire_damage_self_ratio   =  496  # (server_set_friendly_fire_damage_self_ratio, <value>), #0-100
server_get_friendly_fire_damage_friend_ratio =  497  # (server_get_friendly_fire_damage_friend_ratio, <destination>),
server_set_friendly_fire_damage_friend_ratio =  498  # (server_set_friendly_fire_damage_friend_ratio, <value>), #0-100
server_get_anti_cheat                        =  499  # (server_get_anti_cheat, <destination>),
server_set_anti_cheat                        =  477  # (server_set_anti_cheat, <value>), #0 = off, 1 = on

################################################################################
# [ Z25 ] REMAINING ESOTERIC STUFF (NO IDEA WHAT IT DOES)
################################################################################

  # Honestly, I have no idea what these functions could be used for. If you
  # know, please let me know ASAP! :-)

set_tooltip_text             = 1130  #  (set_tooltip_text, <string_id>),
ai_mesh_face_group_show_hide = 1805  #  (ai_mesh_face_group_show_hide, <group_no>, <value>), # 1 for enable, 0 for disable
auto_set_meta_mission_at_end_commited = 1305  # (auto_set_meta_mission_at_end_commited), Not documented. Not used in Native. Was (simulate_battle, <value>) before.

################################################################################
# [ Z26 ] HARDCODED COMPILER-RELATED CODE
################################################################################

  # Do not touch this stuff unless necessary. Module System compiler needs this
  # code to correctly compile your module into format that Warband understands.

lhs_operations = [try_for_range, try_for_range_backwards, try_for_parties, try_for_agents, store_script_param_1, store_script_param_2, store_script_param, store_repeat_object,
get_global_cloud_amount, get_global_haze_amount, options_get_damage_to_player, options_get_damage_to_friends, options_get_combat_ai, options_get_campaign_ai, options_get_combat_speed,
profile_get_banner_id, get_achievement_stat, get_max_players, player_get_team_no, player_get_troop_id, player_get_agent_id, player_get_gold, multiplayer_get_my_team,
multiplayer_get_my_troop, multiplayer_get_my_gold, multiplayer_get_my_player, player_get_score, player_get_kill_count, player_get_death_count, player_get_ping, player_get_is_muted,
player_get_unique_id, player_get_gender, player_get_item_id, player_get_banner_id, game_get_reduce_campaign_ai, multiplayer_find_spawn_point, team_get_bot_kill_count,
team_get_bot_death_count, team_get_kill_count, team_get_score, team_get_faction, player_get_value_of_original_items, server_get_renaming_server_allowed,
server_get_changing_game_type_allowed, server_get_friendly_fire, server_get_control_block_dir, server_get_combat_speed, server_get_add_to_game_servers_list, server_get_ghost_mode,
server_get_max_num_players, server_get_melee_friendly_fire, server_get_friendly_fire_damage_self_ratio, server_get_friendly_fire_damage_friend_ratio, server_get_anti_cheat, troop_get_slot,
party_get_slot, faction_get_slot, scene_get_slot, party_template_get_slot, agent_get_slot, quest_get_slot, item_get_slot, player_get_slot, team_get_slot, scene_prop_get_slot,
store_last_sound_channel, get_angle_between_positions, get_distance_between_positions, get_distance_between_positions_in_meters, get_sq_distance_between_positions,
get_sq_distance_between_positions_in_meters, get_sq_distance_between_position_heights, position_get_x, position_get_y, position_get_z, position_get_scale_x,
position_get_scale_y, position_get_scale_z, position_get_rotation_around_z, position_normalize_origin, position_get_rotation_around_x, position_get_rotation_around_y,
position_get_distance_to_terrain, position_get_distance_to_ground_level, create_text_overlay, create_mesh_overlay, create_button_overlay, create_image_button_overlay, create_slider_overlay,
create_progress_overlay, create_combo_button_overlay, create_text_box_overlay, create_check_box_overlay, create_simple_text_box_overlay, create_image_button_overlay_with_tableau_material,
create_mesh_overlay_with_tableau_material, create_game_button_overlay, create_in_game_button_overlay, create_number_box_overlay,  create_listbox_overlay, create_mesh_overlay_with_item_id,
overlay_get_position, create_combo_label_overlay, get_average_game_difficulty, get_level_boundary, faction_get_color, troop_get_type, troop_get_xp, troop_get_class,
troop_inventory_slot_get_item_amount, troop_inventory_slot_get_item_max_amount, troop_get_inventory_capacity, troop_get_inventory_slot, troop_get_inventory_slot_modifier,
troop_get_upgrade_troop, item_get_type, party_get_num_companions, party_get_num_prisoners, party_get_current_terrain, party_get_template_id, party_count_members_of_type,
party_count_companions_of_type, party_count_prisoners_of_type, party_get_free_companions_capacity, party_get_free_prisoners_capacity, party_get_helpfulness, party_get_ai_initiative,
party_get_num_companion_stacks, party_get_num_prisoner_stacks, party_stack_get_troop_id, party_stack_get_size, party_stack_get_num_wounded, party_stack_get_troop_dna,
party_prisoner_stack_get_troop_id, party_prisoner_stack_get_size, party_prisoner_stack_get_troop_dna, party_get_cur_town, party_get_morale, party_get_battle_opponent, party_get_icon,
party_get_skill_level, get_battle_advantage, party_get_attached_to, party_get_num_attached_parties, party_get_attached_party_with_rank, get_player_agent_no, get_player_agent_kill_count,
get_player_agent_own_troop_kill_count, agent_get_horse, agent_get_rider, agent_get_party_id, agent_get_entry_no, agent_get_troop_id, agent_get_item_id, store_agent_hit_points,
agent_get_kill_count, agent_get_player_id, agent_get_wielded_item, agent_get_ammo, agent_get_simple_behavior, agent_get_combat_state, agent_get_attached_scene_prop,
agent_get_time_elapsed_since_removed, agent_get_number_of_enemies_following, agent_get_attack_action, agent_get_defend_action, agent_get_group, agent_get_action_dir, agent_get_animation,
agent_get_team, agent_get_class, agent_get_division, team_get_hold_fire_order, team_get_movement_order, team_get_riding_order, team_get_weapon_usage_order, team_get_leader,
agent_get_item_slot, scene_prop_get_num_instances, scene_prop_get_instance, scene_prop_get_visibility, scene_prop_get_hit_points, scene_prop_get_max_hit_points, scene_prop_get_team,
agent_get_ammo_for_slot, agent_deliver_damage_to_agent_advanced, team_get_gap_distance, add_missile, scene_item_get_num_instances, scene_item_get_instance,
scene_spawned_item_get_num_instances, scene_spawned_item_get_instance, prop_instance_get_variation_id, prop_instance_get_variation_id_2, prop_instance_get_position,
prop_instance_get_starting_position, prop_instance_get_scale, prop_instance_get_scene_prop_kind, prop_instance_is_animating, prop_instance_get_animation_target_position,
agent_get_item_cur_ammo, mission_get_time_speed, mission_cam_get_aperture, store_trigger_param, store_trigger_param_1, store_trigger_param_2, store_trigger_param_3, agent_ai_get_look_target,
agent_ai_get_move_target, agent_ai_get_behavior_target, agent_get_crouch_mode, store_or, store_and, store_mod, store_add, store_sub, store_mul, store_div, store_sqrt, store_pow, store_sin,
store_cos, store_tan, assign, store_random, store_random_in_range, store_asin, store_acos, store_atan, store_atan2, store_troop_gold, store_num_free_stacks, store_num_free_prisoner_stacks,
store_party_size, store_party_size_wo_prisoners, store_troop_kind_count, store_num_regular_prisoners, store_troop_count_companions, store_troop_count_prisoners, store_item_kind_count,
store_free_inventory_capacity, store_skill_level, store_character_level, store_attribute_level, store_troop_faction, store_troop_health, store_proficiency_level, store_relation,
store_conversation_agent, store_conversation_troop, store_partner_faction, store_encountered_party, store_encountered_party2, store_faction_of_party, store_current_scene, store_zoom_amount,
store_item_value, store_troop_value, store_partner_quest, store_random_quest_in_range, store_random_troop_to_raise, store_random_troop_to_capture, store_random_party_in_range,
store_random_horse, store_random_equipment, store_random_armor, store_quest_number, store_quest_item, store_quest_troop, store_current_hours, store_time_of_day, store_current_day,
store_distance_to_party_from_party, get_party_ai_behavior, get_party_ai_object, get_party_ai_current_behavior, get_party_ai_current_object, store_num_parties_created,
store_num_parties_destroyed, store_num_parties_destroyed_by_player, store_num_parties_of_template, store_random_party_of_template, store_remaining_team_no, store_mission_timer_a_msec,
store_mission_timer_b_msec, store_mission_timer_c_msec, store_mission_timer_a, store_mission_timer_b, store_mission_timer_c, store_enemy_count, store_friend_count, store_ally_count,
store_defender_count, store_attacker_count, store_normalized_team_count,]

global_lhs_operations = [val_lshift, val_rshift, val_add, val_sub, val_mul, val_div, val_max, val_min, val_mod]

can_fail_operations = [ge, eq, gt, is_between, entering_town, map_free, encountered_party_is_attacker, conversation_screen_is_active, in_meta_mission, troop_is_hero, troop_is_wounded,
key_is_down, key_clicked, game_key_is_down, game_key_clicked, hero_can_join, hero_can_join_as_prisoner, party_can_join, party_can_join_as_prisoner, troops_can_join,
troops_can_join_as_prisoner, party_can_join_party, main_party_has_troop, party_is_in_town, party_is_in_any_town, party_is_active, player_has_item, troop_has_item_equipped, troop_is_mounted,
troop_is_guarantee_ranged, troop_is_guarantee_horse, player_is_active, multiplayer_is_server, multiplayer_is_dedicated_server, game_in_multiplayer_mode, player_is_admin,
player_is_busy_with_menus, player_item_slot_is_picked_up, check_quest_active, check_quest_finished, check_quest_succeeded, check_quest_failed, check_quest_concluded, is_trial_version,
is_edit_mode_enabled, troop_slot_eq, party_slot_eq, faction_slot_eq, scene_slot_eq, party_template_slot_eq, agent_slot_eq, quest_slot_eq, item_slot_eq, player_slot_eq, team_slot_eq,
scene_prop_slot_eq, troop_slot_ge, party_slot_ge, faction_slot_ge, scene_slot_ge, party_template_slot_ge, agent_slot_ge, quest_slot_ge, item_slot_ge, player_slot_ge, team_slot_ge,
scene_prop_slot_ge, position_has_line_of_sight_to_position, position_is_behind_position, is_presentation_active, all_enemies_defeated, race_completed_by_player, num_active_teams_le,
main_hero_fallen, lt, neq, le, teams_are_enemies, agent_is_alive, agent_is_wounded, agent_is_human, agent_is_ally, agent_is_non_player, agent_is_defender, agent_is_active, agent_is_routed,
agent_is_in_special_mode, agent_is_in_parried_animation, class_is_listening_order, agent_check_offer_from_agent, entry_point_is_auto_generated, scene_prop_has_agent_on_it, agent_is_alarmed,
agent_is_in_line_of_sight, scene_prop_get_instance, scene_item_get_instance, scene_allows_mounted_units, prop_instance_is_valid, prop_instance_intersects_with_prop_instance,
agent_has_item_equipped, map_get_land_position_around_position, map_get_water_position_around_position, is_zoom_disabled, is_currently_night, store_random_party_of_template, str_is_empty]
