## Prebattle Orders & Deployment by Caba'drin
## v0.96.2
## 25 March 2012

from module_constants import *

## Prebattle Orders & Deployment Begin
#PBOD General
##Settings
skirmish_min_distance = 1500 #Min distance you wish maintained, in cm. Where agent will retreat
skirmish_max_distance = 2500 #Max distance to maintain, in cm. Where agent will stop retreating
crouch_speed_limiter  = 1    #Limit AI bot movement speed while crouched
volley_delay_bow      = 2
volley_delay_crossbow = 5
volley_delay_musket   = 7
volley_delay_shift    = 2    #should be 3 (or greater) for muskets; 2 for crossbows/bows
#pbod_debug            = 0    #On/Off for debug messages

##Data Storage, Convenience Constants, etc
current_version = 963
order_frame_presobj = "trp_bandit_leaders_end"  #dummy troop slots used in battle Floris: "trp_tpe_presobj"   Native: "trp_bandit_leaders_end"
order_listeners     = "trp_relative_of_merchants_end" #dummy troop slots used in battle Floris: "trp_"   Native: "trp_relative_of_merchants_end"
sound_whistle = "snd_man_breath_hard"  #Native: "snd_man_breath_hard"   #Floris: "snd_whistle" 


### SLOTS BEGIN
#Troop and Party Slots (Party Slots all for p_main_party ONLY; Troop slots as specified)
slot_party_pbod_mod_version                = 46  #slot_village_player_can_not_steal_cattle
#Deployment
slot_party_prebattle_customized_deployment = 47  #slot_center_accumulated_rents  
slot_troop_prebattle_first_round           = 47  #slot_troop_promised_fief
slot_troop_prebattle_stack_number          = 48  #slot_troop_set_decision_seed
slot_troop_prebattle_stack_xp              = 49  #slot_troop_temp_decision_seed
#Split Divisions
slot_party_prebattle_customized_divisions  = 51  #slot_town_player_odds 
slot_troop_prebattle_alt_division          = 50  #slot_troop_recruitment_random 
slot_troop_prebattle_alt_division_percent  = 51  #slot_troop_intrigue_impatience
slot_troop_prebattle_alt_division_amount   = 52  #slot_lord_reputation_type
#Troop slots--for soldiers (non-heros, non-lords, non-player) only
#Party slots--for the main party and main party backup only
#Orders
slot_party_prebattle_plan                  = 231 #slot_center_shipyards
slot_party_prebattle_num_orders            = 232 #slot_center_household_gardens 
slot_party_prebattle_order_array_begin     = 250 #slot_town_trade_good_prices_begin 
#Party slots--for the main party only--up to 320 used in this version
#reg()s from 6-50 used in this version (only during order presentation)
#Weather Prof Decrease - temp, used only for 1 mission at a time then can be discarded
slot_troop_proficiency_modified  = 335
slot_troop_orig_wpt_archery      = 336
slot_troop_orig_wpt_crossbow     = 337
slot_troop_orig_wpt_throwing     = 338
slot_troop_pnty_wpt_archery      = 339 ##heroes only
slot_troop_pnty_wpt_crossbow     = 340 ##heroes only
slot_troop_pnty_wpt_throwing     = 341 ##heroes only


#Team Slots (so high to allow for formations)
#Team-Division Slots (for orders)
slot_team_d0_order_weapon     = 356 #plus 8 more for the other divisions
slot_team_d0_order_shield     = 365 #plus 8 more for the other divisions
slot_team_d0_order_pavise     = 374 #plus 8 more for the other divisions
slot_team_d0_order_skirmish   = 383 #plus 8 more for the other divisions
slot_team_d0_order_sp_brace   = 392 #plus 8 more for the other divisions
slot_team_d0_order_volley     = 401 #plus 8 more for the other divisions
slot_team_d0_order_volley_counter = 410
slot_team_d0_order_crouch     = 419
slot_team_d0_order_firearrow  = 428
slot_team_d0_order_UNUSED_2   = 437
slot_team_d0_order_UNUSED_3   = 446
slot_team_d0_formation_to_resume = 455
#team-division order slots end at 464

slot_team_decision_seed       = 465
slot_team_decision_seed_2     = 466
##Mission-Specific Variables as team slots (in lieu of globals as they are only needed in 1 mission; and they get reset to 0 on mission start)
slot_team_mission_variable_1     = 467
slot_team_mission_variable_2     = 468
slot_team_mv_crouching           = slot_team_mission_variable_1 #for team 0
slot_team_mv_reinforcement_stage = slot_team_mission_variable_1 #for team 1
#Order Tracking
slot_team_mv_gk_order                 = slot_team_mission_variable_1 #for team 2
slot_team_mv_gk_order_backup          = slot_team_mission_variable_1 #for team 3
slot_team_mv_gk_order_hold_over_there = slot_team_mission_variable_1 #for team 4
#
slot_team_mv_temp_cheatmode           = slot_team_mission_variable_1 #for team 5 #currently only used in BP_Spawn
slot_team_mv_temp_placement_counter   = slot_team_mission_variable_1 #for team 6 #currently only used in BP_Spawn


#Party Slots, Cont'd
#PBOD Preference Slots (used for p_main_party; available 72 - 108)
slot_party_pref_prefs_set    = 72
slot_party_pref_div_dehorse  = 76 # slot_town_village_product         #76
slot_party_pref_div_no_ammo  = 77 # slot_town_rebellion_readiness     #77
slot_party_pref_wu_lance     = 78 # slot_town_arena_melee_mission_tpl #78
slot_party_pref_wu_harcher   = 79 # slot_town_arena_torny_mission_tpl #79
slot_party_pref_wu_spear     = 80 # slot_town_arena_melee_1_num_teams #80
slot_party_pref_dmg_tweaks   = 81 # slot_town_arena_melee_1_team_size #81
slot_party_pref_formations   = 82 # slot_town_arena_melee_2_num_teams #82
slot_party_pref_bodyguard    = 83 # slot_town_arena_melee_2_team_size #83
# Slot 84 seems to be conflicting with 83 somehow.  leave blank.
slot_party_pref_bc_charge_ko = 85 # slot_town_arena_melee_3_team_size #85
slot_party_pref_wp_prof_decrease = 86 # slot_town_arena_melee_cur_tier#86
slot_party_pref_real_deployment  = 87
slot_party_pref_rdep_time_scale  = 88
slot_party_pref_spo_brace        = 89
slot_party_pref_spo_skirmish     = 90
slot_party_pref_spo_volley       = 91
slot_party_pref_spo_pavise       = 92
slot_party_pref_spo_firearrow    = 93
slot_party_pref_siege_charge     = 94
slot_party_pref_ally_division    = 95
## WINDYPLAINS+ ## - Hold a backup value of the bodyguard setting for QP4 work.
slot_party_bodyguard_backup      = 100
slot_party_pref_bc_continue  = 101
## WINDYPLAINS- ##

#Agent Slots
slot_agent_lance         = 33
slot_agent_horsebow      = 34
slot_agent_spear         = 35
slot_agent_horse         = 36
slot_agent_volley_fire   = 37
slot_agent_spearwall     = 38
slot_agent_player_braced = 39
slot_agent_alt_div_check = 40
#slot_agent_new_division  = 41
slot_agent_deployed_pavise   = 42
slot_agent_crouching         = 43
slot_agent_player_firearrows = 44

## WINDYPLAINS- ##

#Scene Prop Slots
#for Deployable Pavise
slot_prop_pavise_spawn_agent = 3
slot_prop_pavise_item_no     = 4
slot_prop_pavise_item_mod    = 5
slot_prop_pavise_banner_mesh = 6

### SLOTS END

### NON-SLOT Convenience Constants
pavise_begin = "itm_tab_shield_pavise_a"
pavise_end   = "itm_tab_shield_small_round_a"

#Order Constants
no_order  = -1
clear     = 0
onehand   = 1
twohands  = 2
polearm   = 3
ranged    = 4
free      = 5 #shield
shield    = 6
noshield  = 7
begin     = 1
end       = 0
#for ease of order-slot setting with begin/end
skirmish_shift = 8
volley_shift   = 10
brace_shift    = 12
pavise_shift   = 14
crouch_shift   = 16
firearrow_shift= 18

#full volley system
volley_type_at_will      = 0
volley_type_mass         = 1
volley_type_rank         = 2
volley_type_platoon      = 3
volley_type_on_command   = 4


#Custom Camera (for $cam_mode)
cam_mode_default = 0
cam_mode_follow  = 1
cam_mode_free    = 2
cam_mode_shoot   = 3
cam_position     = 47 #pos47

#(For $battle_phase)
BP_Spawn = 0

#Values for agent_get_combat_state
cs_free                      = 0
cs_target_in_sight           = 1     # ranged units
cs_guard                     = 2     # no shield
cs_wield                     = 3     # reach out weapon, preparing to strike, melee units
cs_fire                      = 3     # ranged units
cs_swing                     = 4     # cut / thrust, melee units
cs_load                      = 4     # crossbow units
cs_still                     = 7     # melee units, happens, not always (seems to have something to do with the part of body hit), when hit
cs_no_visible_targets        = 7     # ranged units or blocking iwth a shield
cs_target_on_right_hand_side = 8     # horse archers

# For the player or dead units it always returns 0.
# But for living human agents here are some of the values it can return and what each seems to mean:
# 0 = nothing active
# 1 = firing ranged
# 3 = preparing and holding attack (either melee or ranged)
# 4 = swinging with melee
# 7 = recovering from being hit
# 8 = ranged equipped, no target in field of view

#AutoLoot compile-time-set item slots no longer necessary with WSE

#from module_items import arrows_begin, arrows_end
# arrows_begin = "itm_arrows"
# arrows_end = "itm_bolts"
# firearrows_begin = "itm_arrows_fire"
# firearrows_end = "itm_fire_arrows_end"

#-- Dunde's Key Config BEGIN
from header_triggers import *
#-- Parts to modify as your mod need --------------
keys_list = [
			  ("$key_camera_forward",  key_up,                "Camera Forward"),
              ("$key_camera_backward", key_down,              "Camera Backward"),
	          ("$key_camera_left",     key_left,              "Camera Left"),
	          ("$key_camera_right",    key_right,             "Camera Right"),
			  ("$key_camera_zoom_plus",key_numpad_plus,       "Camera Up"),
              ("$key_camera_zoom_min", key_numpad_minus,      "Camera Down"),
			  ("$key_camera_next",     key_left_mouse_button, "Next BOT"),
              ("$key_camera_prev",     key_right_mouse_button,"Prev BOT"),
			  ("$key_camera_toggle",   key_end,               "Toggle Camera Mode"),
	          ("$key_order_7",         key_f7,                "Select Order 7"),
	          ("$key_order_8",         key_f8,                "Select Order 8"),
	          ("$key_order_9",         key_f9,                "Select Order 9"),
			  ("$key_order_10",        key_f10,               "Select Order 10"),
	          ("$key_special_brace",   key_b,                 "Spear Brace"),
	          ("$key_special_whistle", key_m,                 "Call Horse / Rear"),
			  ("$key_special_pavise",  key_h,                 "Deploy/Recover Pavise^Fire Arrows"),
			  ("$key_special_bash",    key_left_mouse_button, "Shield Bash Attack"),	  
			  ("$key_special_crouch",  key_caps_lock,         "Crouch / Cheer"),
			  ("$key_special_sprint",  key_left_control,      "Sprint"),
            ] # end of keys_list
#--------------------------------------------------
all_keys_list   = [
(key_1, "1"), (key_2, "2"), (key_3, "3"), (key_4, "4"), (key_5, "5"), (key_6, "6"), (key_7, "7"), (key_8, "8"), (key_9, "9"), (key_0, "0"), 
(key_a, "A"), (key_b, "B"), (key_c, "C"), (key_d, "D"), (key_e, "E"), (key_f, "F"), (key_g, "G"), (key_h, "H"), (key_i, "I"), (key_j, "J"),
(key_k, "K"), (key_l, "L"), (key_m, "M"), (key_n, "N"), (key_o, "O"), (key_p, "P"), (key_q, "Q"), (key_r, "R"), (key_s, "S"), (key_t, "T"), 
(key_u, "U"), (key_v, "V"), (key_w, "W"), (key_x, "X"), (key_y, "Y"), (key_z, "Z"), 
(key_numpad_0, "Numpad 0"), (key_numpad_1, "Numpad 1"), (key_numpad_2, "Numpad 2"), (key_numpad_3, "Numpad 3"), (key_numpad_4, "Numpad 4"), 
(key_numpad_5, "Numpad 5"), (key_numpad_6, "Numpad 6"), (key_numpad_7, "Numpad 7"), (key_numpad_8, "Numpad 8"), (key_numpad_9, "Numpad 9"), 
(key_num_lock, "Num Lock"), (key_numpad_slash, "Numpad DIV"), (key_numpad_multiply, "Numpad MUL"), 
(key_numpad_minus, "Numpad MIN"), (key_numpad_plus, "Numpad PLUS"), (key_numpad_enter, "Numpad ENTER"), (key_numpad_period, "Numpad DEL)"), 
(key_insert, "Insert"), (key_delete, "Delete"), (key_home, "Home"), (key_end, "End"), (key_page_up, "Page Up"), (key_page_down, "Page Down"), 
(key_up, "Up"), (key_down, "Down"), (key_left, "Left"), (key_right, "Right"),
(key_f1, "F1"), (key_f1, "F2"), (key_f3, "F3"), (key_f4, "F4"),  (key_f5, "F5"),  (key_f6, "F6"), 
(key_f7, "F7"), (key_f8, "F8"), (key_f9, "F9"), (key_f10, "F10"), (key_f11, "F11"), (key_f12, "F12"),
(key_space, "Space Bar"), (key_enter, "Enter"), (key_tab, "Tab"), (key_back_space, "Backspace"), 
(key_open_braces, "[ "), (key_close_braces, " ] "), (key_comma, " < "), (key_period, " > "), (key_slash, " ? "), (key_back_slash, "\\"), 
(key_equals, " = "), (key_minus, " -- "), (key_semicolon, "Semicolon"), (key_apostrophe, "Apostrophe"), (key_tilde, "Tilde"), (key_caps_lock, "Caps Lock"),
(key_left_shift, "Left Shift"), (key_right_shift, "Right Shift"), (key_left_control, "Left Ctrl"), (key_right_control, "Right Ctrl"), (key_left_alt, "Left Alt"), (key_right_alt, "Right Alt"),
(key_left_mouse_button, "Left Click"), (key_right_mouse_button, "Right Click"), (key_middle_mouse_button, "Middle Mouse Button"), 
(key_mouse_button_4, "Mouse Button 4"), (key_mouse_button_5, "Mouse Button 5"), (key_mouse_button_6, "Mouse Button 6"), 
(key_mouse_button_7, "Mouse Button 7"), (key_mouse_button_8, "Mouse Button 8"), (key_mouse_scroll_up, "Mouse Scroll Up"), (key_mouse_scroll_down, "Mouse Scroll Down"), 
]

number_of_keys            = len(keys_list)
number_of_all_keys        = len(all_keys_list)
two_columns_limit         = 20 

slot_default_keys_begin   = 0
slot_keys_begin           = slot_default_keys_begin + number_of_keys
slot_key_overlay_begin    = slot_keys_begin         + number_of_keys
slot_key_defs_begin       = slot_key_overlay_begin  + number_of_keys + number_of_keys

key_config_data = "trp_key_config"
key_names_begin = "str_key_no1"
key_label_begin = "str_key_1"
#-- Dunde's Key Config END
from header_common import find_object
key_ignore_check_begin = find_object(keys_list, "$key_camera_next") + slot_keys_begin
key_ignore_check_end   = find_object(keys_list, "$key_camera_prev") + slot_keys_begin + 1



## Prebattle Orders & Deployment End