# Center Improvements (1.0) by Windyplains
from module_constants import *

# DEBUG_IMPROVEMENTS                              = 0

# Center Improvement Status
cis_unbuilt                                     = 0
cis_built                                       = 1
cis_damaged_20_percent                          = 2
cis_damaged_40_percent                          = 3
cis_damaged_60_percent                          = 4
cis_damaged_80_percent                          = 5
# At 100 percent damage the status reverts to cis_unbuilt.

# Centers an improvement can be built in.
imp_allowed_in_any                              = 0
imp_allowed_in_village                          = 1
imp_allowed_in_castle                           = 2
imp_allowed_in_town                             = 3
imp_allowed_in_village_town                     = 4
imp_allowed_in_village_castle                   = 5
imp_allowed_in_walled_center                    = 6

native_improvements_begin                       = slot_center_has_manor
native_improvements_end                         = 136


slot_center_current_improvement_1               = 390
slot_center_current_improvement_2               = 391
slot_center_current_improvement_3               = 392
slot_center_improvement_end_hour_1              = 393
slot_center_improvement_end_hour_2              = 394
slot_center_improvement_end_hour_3              = 395
slot_center_patrol_party                        = 396
slot_center_improvement_start_hour_1            = 397
slot_center_improvement_start_hour_2            = 398
slot_center_improvement_start_hour_3            = 399

# slot_center_has_manor                         = 130 # V
# slot_center_has_fish_pond                     = 131 # V
# slot_center_has_watch_tower                   = 132 # V
# slot_center_has_school                        = 133 # V
# slot_center_has_messenger_post                = 134 # V, C, T
# slot_center_has_prisoner_tower                = 135 # C, T
slot_center_has_garrison                        = 402 # V
slot_center_has_crops_of_grain                  = 403 # V, C
slot_center_has_armoury                         = 404 # C, T
slot_center_has_small_marketplace               = 405 # V, C, T
slot_center_has_improved_roads                  = 406 # V, C, T
slot_center_has_fire_brigade                    = 407 # V, C, T
slot_center_has_forge                           = 408 # V
slot_center_has_merc_chapterhouse               = 409 # T
slot_center_has_escape_tunnels                  = 410 # C, T
slot_center_has_trade_guilds                    = 411 # T
slot_center_has_castle_library                  = 412 # C, T
slot_center_has_training_grounds                = 413 # C, T
slot_center_has_reinforced_walls                = 414 # C, T
slot_center_has_fishery                         = 415 # V
slot_center_has_stables                         = 416 # V, C, T
slot_center_has_horse_ranch                     = 417 # V
slot_center_has_royal_forge                     = 418 # C, T
slot_center_has_moat                            = 419 # C, T

center_improvements_begin                       = slot_center_has_garrison
center_improvements_end                         = slot_center_has_moat

castle_patrol_create                            = 1
castle_patrol_merge_with_center                 = 2
castle_patrol_engage_party                      = 3
castle_patrol_return_home                       = 4

# Mercenary Chapterhouse (409)
mercenary_chapterhouse_min_troop                = "trp_mercenary_swordsman"
mercenary_chapterhouse_troop_bonus              = 3
mercenary_chapterhouse_hiring_discount          = 40 # %
