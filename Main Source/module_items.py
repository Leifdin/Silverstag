from module_constants import *
from ID_factions import *
from header_items import  *
from header_operations import *
from header_triggers import *

####################################################################################################################
#  Each item record contains the following fields:
#  1) Item id: used for referencing items in other files.
#     The prefix itm_ is automatically added before each item id.
#  2) Item name. Name of item as it'll appear in inventory window
#  3) List of meshes.  Each mesh record is a tuple containing the following fields:
#    3.1) Mesh name.
#    3.2) Modifier bits that this mesh matches.
#     Note that the first mesh record is the default.
#  4) Item flags. See header_items.py for a list of available flags.
#  5) Item capabilities. Used for which animations this item is used with. See header_items.py for a list of available flags.
#  6) Item value.
#  7) Item stats: Bitwise-or of various stats about the item such as:
#      weight, abundance, difficulty, head_armor, body_armor,leg_armor, etc...
#  8) Modifier bits: Modifiers that can be applied to this item.
#  9) [Optional] Triggers: List of simple triggers to be associated with the item.
#  10) [Optional] Factions: List of factions that item can be found as merchandise.
####################################################################################################################

# Some constants for ease of use.
imodbits_none = 0
imodbits_horse_basic = imodbit_swaybacked|imodbit_lame|imodbit_spirited|imodbit_heavy|imodbit_stubborn
imodbits_cloth  = imodbit_tattered | imodbit_ragged | imodbit_sturdy | imodbit_thick | imodbit_hardened
imodbits_armor  = imodbit_rusty | imodbit_battered | imodbit_crude | imodbit_thick | imodbit_reinforced |imodbit_lordly
imodbits_plate  = imodbit_cracked | imodbit_rusty | imodbit_battered | imodbit_crude | imodbit_thick | imodbit_reinforced |imodbit_lordly
imodbits_polearm = imodbit_cracked | imodbit_bent | imodbit_balanced
imodbits_shield  = imodbit_cracked | imodbit_battered |imodbit_thick | imodbit_reinforced
imodbits_sword   = imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered
imodbits_sword_high   = imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered|imodbit_masterwork
imodbits_axe   = imodbit_rusty | imodbit_chipped | imodbit_heavy
imodbits_mace   = imodbit_rusty | imodbit_chipped | imodbit_heavy
imodbits_pick   = imodbit_rusty | imodbit_chipped | imodbit_balanced | imodbit_heavy
imodbits_bow = imodbit_cracked | imodbit_bent | imodbit_strong |imodbit_masterwork
imodbits_crossbow = imodbit_cracked | imodbit_bent | imodbit_masterwork
imodbits_missile   = imodbit_bent | imodbit_large_bag
imodbits_thrown   = imodbit_bent | imodbit_heavy| imodbit_balanced| imodbit_large_bag
imodbits_thrown_minus_heavy = imodbit_bent | imodbit_balanced| imodbit_large_bag

imodbits_horse_good = imodbit_spirited|imodbit_heavy
imodbits_good   = imodbit_sturdy | imodbit_thick | imodbit_hardened | imodbit_reinforced
imodbits_bad    = imodbit_rusty | imodbit_chipped | imodbit_tattered | imodbit_ragged | imodbit_cracked | imodbit_bent
# Replace winged mace/spiked mace with: Flanged mace / Knobbed mace?
# Fauchard (majowski glaive) 
items = [
# item_name, mesh_name, item_properties, item_capabilities, slot_no, cost, bonus_flags, weapon_flags, scale, view_dir, pos_offset
["no_item","INVALID ITEM", [("invalid_item",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_longsword, 3,weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(16,blunt)|thrust_damage(10,blunt),imodbits_none],

["tutorial_spear", "Spear", [("spear",0)], itp_type_polearm| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear, 0 , weight(4.5)|difficulty(0)|spd_rtng(80) | weapon_length(158)|swing_damage(0 , cut) | thrust_damage(19 ,  pierce),imodbits_polearm ],
["tutorial_club", "Club", [("club",0)], itp_type_one_handed_wpn| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 0 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(95)|swing_damage(11 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["tutorial_battle_axe", "Battle Axe", [("battle_ax",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 0 , weight(5)|difficulty(0)|spd_rtng(88) | weapon_length(108)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["tutorial_arrows","Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0,weight(3)|abundance(160)|weapon_length(95)|thrust_damage(0,pierce)|max_ammo(20),imodbits_missile],
["tutorial_bolts","Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag", ixmesh_carry),("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0,weight(2.25)|abundance(90)|weapon_length(55)|thrust_damage(0,pierce)|max_ammo(18),imodbits_missile],
["tutorial_short_bow", "Short Bow", [("short_bow",0),("short_bow_carry",ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 0 , weight(1)|difficulty(0)|spd_rtng(98) | shoot_speed(49) | thrust_damage(12 ,  pierce  ),imodbits_bow ],
["tutorial_crossbow", "Crossbow", [("crossbow",0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_reload_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 0 , weight(3)|difficulty(0)|spd_rtng(42)|  shoot_speed(68) | thrust_damage(32,pierce)|max_ammo(1),imodbits_crossbow ],
["tutorial_throwing_daggers", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown |itp_primary ,itcf_throw_knife, 0 , weight(3.5)|difficulty(0)|spd_rtng(102) | shoot_speed(25) | thrust_damage(16 ,  cut)|max_ammo(14)|weapon_length(0),imodbits_missile ],
["tutorial_saddle_horse", "Saddle Horse", [("saddle_horse",0)], itp_type_horse, 0, 0,abundance(90)|body_armor(3)|difficulty(0)|horse_speed(40)|horse_maneuver(38)|horse_charge(8),imodbits_horse_basic],
["tutorial_shield", "Kite Shield", [("shield_kite_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(150),imodbits_shield ],
["tutorial_staff_no_attack","Staff", [("wooden_staff",0)],itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack,itc_parry_polearm|itcf_carry_sword_back,9, weight(3.5)|spd_rtng(120) | weapon_length(115)|swing_damage(0,blunt) | thrust_damage(0,blunt),imodbits_none],
["tutorial_staff","Staff", [("wooden_staff",0)],itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack,itc_staff|itcf_carry_sword_back,9, weight(3.5)|spd_rtng(120) | weapon_length(115)|swing_damage(16,blunt) | thrust_damage(16,blunt),imodbits_none],
["tutorial_sword", "Sword", [("long_sword",0),("scab_longsw_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 0 , weight(1.5)|difficulty(0)|spd_rtng(100) | weapon_length(102)|swing_damage(18 , cut) | thrust_damage(15 ,  pierce),imodbits_sword ],
["tutorial_axe", "Axe", [("iron_ax",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 0 , weight(4)|difficulty(0)|spd_rtng(91) | weapon_length(108)|swing_damage(19 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],

["tutorial_dagger","Dagger", [("practice_dagger",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_longsword, 3,weight(1.5)|spd_rtng(103)|weapon_length(40)|swing_damage(16,blunt)|thrust_damage(10,blunt),imodbits_none],


["horse_meat","Horse Meat", [("raw_meat",0)], itp_type_goods|itp_consumable|itp_food, 0, 12,weight(40)|food_quality(30)|max_ammo(40),imodbits_none],
# Items before this point are hardwired and their order should not be changed!
["practice_sword","Practice Sword", [("practice_sword",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_wooden_parry|itp_wooden_attack, itc_longsword, 3,weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(22,blunt)|thrust_damage(20,blunt),imodbits_none],
["heavy_practice_sword","Heavy Practice Sword", [("heavy_practicesword",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_greatsword,    21, weight(6.25)|spd_rtng(94)|weapon_length(128)|swing_damage(30,blunt)|thrust_damage(24,blunt),imodbits_none],
["practice_dagger","Practice Dagger", [("practice_dagger",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_attack, itc_dagger|itcf_carry_dagger_front_left, 2,weight(0.5)|spd_rtng(110)|weapon_length(47)|swing_damage(16,blunt)|thrust_damage(14,blunt),imodbits_none],
["practice_axe", "Practice Axe", [("hatchet",0)], itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 24 , weight(2) | spd_rtng(95) | weapon_length(75) | swing_damage(24, blunt) | thrust_damage(0, pierce), imodbits_axe],
["arena_axe", "Axe", [("arena_axe",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 137 , weight(1.5)|spd_rtng(100) | weapon_length(69)|swing_damage(24 , blunt) | thrust_damage(0 ,  pierce),imodbits_axe ],
["arena_sword", "Sword", [("arena_sword_one_handed",0),("sword_medieval_b_scabbard", ixmesh_carry),], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 243 , weight(1.5)|spd_rtng(99) | weapon_length(95)|swing_damage(22 , blunt) | thrust_damage(20 ,  blunt),imodbits_sword_high ],
["arena_sword_two_handed",  "Two-handed Sword", [("arena_sword_two_handed",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 670 , weight(2.75)|spd_rtng(93) | weapon_length(110)|swing_damage(30 , blunt) | thrust_damage(24 ,  blunt),imodbits_sword_high ],
["arena_lance",         "Lance", [("arena_lance",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear, 90 , weight(2.5)|spd_rtng(96) | weapon_length(150)|swing_damage(20 , blunt) | thrust_damage(25 ,  blunt),imodbits_polearm ],
["practice_staff","Practice Staff", [("wooden_staff",0)],itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack,itc_staff|itcf_carry_sword_back,9, weight(2.5)|spd_rtng(103) | weapon_length(118)|swing_damage(18,blunt) | thrust_damage(18,blunt),imodbits_none],
["practice_lance","Practice Lance", [("joust_of_peace",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_greatlance, 18,weight(4.25)|spd_rtng(58)|weapon_length(240)|swing_damage(0,blunt)|thrust_damage(15,blunt),imodbits_none],
["practice_shield","Practice Shield", [("shield_round_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 20,weight(3.5)|body_armor(1)|hit_points(200)|spd_rtng(100)|shield_width(50),imodbits_none],
["practice_bow","Practice Bow", [("hunting_bow",0), ("hunting_bow_carry",ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1.5)|spd_rtng(90) | shoot_speed(40) | thrust_damage(21, blunt),imodbits_bow ],
##                                                     ("hunting_bow",0)],                  itp_type_bow|itp_two_handed|itp_primary|itp_attach_left_hand, itcf_shoot_bow, 4,weight(1.5)|spd_rtng(90)|shoot_speed(40)|thrust_damage(19,blunt),imodbits_none],
["practice_crossbow", "Practice Crossbow", [("crossbow_a",0)], itp_type_crossbow |itp_primary|itp_two_handed ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 0, weight(3)|spd_rtng(42)| shoot_speed(68) | thrust_damage(32,blunt)|max_ammo(1),imodbits_crossbow],
["practice_javelin", "Practice Javelins", [("javelin",0),("javelins_quiver_new", ixmesh_carry)], itp_type_thrown |itp_primary|itp_next_item_as_melee,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 0, weight(5) | spd_rtng(91) | shoot_speed(28) | thrust_damage(27, blunt) | max_ammo(50) | weapon_length(75), imodbits_thrown],
["practice_javelin_melee", "practice_javelin_melee", [("javelin",0)], itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry , itc_staff, 0, weight(1)|difficulty(0)|spd_rtng(91) |swing_damage(12, blunt)| thrust_damage(14,  blunt)|weapon_length(75),imodbits_polearm ],
["practice_throwing_daggers", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown |itp_primary ,itcf_throw_knife, 0 , weight(3.5)|spd_rtng(102) | shoot_speed(25) | thrust_damage(16, blunt)|max_ammo(10)|weapon_length(0),imodbits_thrown ],
["practice_throwing_daggers_100_amount", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown |itp_primary ,itcf_throw_knife, 0 , weight(3.5)|spd_rtng(102) | shoot_speed(25) | thrust_damage(16, blunt)|max_ammo(100)|weapon_length(0),imodbits_thrown ],
# ["cheap_shirt","Cheap Shirt", [("shirt",0)], itp_type_body_armor|itp_covers_legs, 0, 4,weight(1.25)|body_armor(3),imodbits_none],
["practice_horse","Practice Horse", [("saddle_horse",0)], itp_type_horse, 0, 37,body_armor(10)|horse_speed(40)|horse_maneuver(37)|horse_charge(14),imodbits_none],
["practice_arrows","Practice Arrows", [("arena_arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0,weight(1.5)|weapon_length(95)|max_ammo(80),imodbits_missile],
## ["practice_arrows","Practice Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo)], itp_type_arrows, 0, 31,weight(1.5)|weapon_length(95)|max_ammo(80),imodbits_none],
["practice_bolts","Practice Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag", ixmesh_carry),("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0,weight(2.25)|weapon_length(55)|max_ammo(49),imodbits_missile],
["practice_arrows_10_amount","Practice Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0,weight(1.5)|weapon_length(95)|max_ammo(10),imodbits_missile],
["practice_arrows_100_amount","Practice Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0,weight(1.5)|weapon_length(95)|max_ammo(100),imodbits_missile],
["practice_bolts_9_amount","Practice Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag", ixmesh_carry),("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0,weight(2.25)|weapon_length(55)|max_ammo(9),imodbits_missile],
["practice_boots", "Practice Boots", [("boot_nomad_a",0)], itp_type_foot_armor |itp_civilian  | itp_attach_armature,0, 11 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10), imodbits_cloth ],
["red_tourney_armor","Red Tourney Armor", [("tourn_armor_a",0)], itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["blue_tourney_armor","Blue Tourney Armor", [("mail_shirt",0)], itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["green_tourney_armor","Green Tourney Armor", [("leather_vest",0)], itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["gold_tourney_armor","Gold Tourney Armor", [("padded_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 152,weight(15.0)|body_armor(20)|leg_armor(6),imodbits_none],
["red_tourney_helmet","Red Tourney Helmet",[("flattop_helmet",0)],itp_type_head_armor,0,126, weight(2)|head_armor(16),imodbits_none],
["blue_tourney_helmet","Blue Tourney Helmet",[("segmented_helm",0)],itp_type_head_armor,0,126, weight(2)|head_armor(16),imodbits_none],
["green_tourney_helmet","Green Tourney Helmet",[("hood_c",0)],itp_type_head_armor,0,126, weight(2)|head_armor(16),imodbits_none],
["gold_tourney_helmet","Gold Tourney Helmet",[("hood_a",0)],itp_type_head_armor,0,126, weight(2)|head_armor(16),imodbits_none],

["arena_shield_red", "Shield", [("arena_shield_red",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["arena_shield_blue", "Shield", [("arena_shield_blue",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["arena_shield_green", "Shield", [("arena_shield_green",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["arena_shield_yellow", "Shield", [("arena_shield_yellow",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60),imodbits_shield ],

["arena_armor_white", "Arena Armor White", [("arena_armorW_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_red", "Arena Armor Red", [("arena_armorR_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_blue", "Arena Armor Blue", [("arena_armorB_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_green", "Arena Armor Green", [("arena_armorG_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_yellow", "Arena Armor Yellow", [("arena_armorY_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_tunic_white", "Arena Tunic White ", [("arena_tunicW_new",0)], itp_type_body_armor |itp_covers_legs ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_red", "Arena Tunic Red", [("arena_tunicR_new",0)], itp_type_body_armor |itp_covers_legs ,0, 27 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_blue", "Arena Tunic Blue", [("arena_tunicB_new",0)], itp_type_body_armor |itp_covers_legs ,0, 27 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_green", "Arena Tunic Green", [("arena_tunicG_new",0)], itp_type_body_armor |itp_covers_legs ,0, 27 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_yellow", "Arena Tunic Yellow", [("arena_tunicY_new",0)], itp_type_body_armor |itp_covers_legs ,0, 27 , weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
#headwear
["arena_helmet_red", "Arena Helmet Red", [("arena_helmetR",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_blue", "Arena Helmet Blue", [("arena_helmetB",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_green", "Arena Helmet Green", [("arena_helmetG",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_yellow", "Arena Helmet Yellow", [("arena_helmetY",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_white", "Steppe Helmet White", [("steppe_helmetW",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_red", "Steppe Helmet Red", [("steppe_helmetR",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_blue", "Steppe Helmet Blue", [("steppe_helmetB",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_green", "Steppe Helmet Green", [("steppe_helmetG",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_yellow", "Steppe Helmet Yellow", [("steppe_helmetY",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_white", "Tourney Helm White", [("tourney_helmR",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_red", "Tourney Helm Red", [("tourney_helmR",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_blue", "Tourney Helm Blue", [("tourney_helmB",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_green", "Tourney Helm Green", [("tourney_helmG",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_yellow", "Tourney Helm Yellow", [("tourney_helmY",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_turban_red", "Arena Turban", [("tuareg_open",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_turban_blue", "Arena Turban", [("tuareg_open",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_turban_green", "Arena Turban", [("tuareg_open",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_turban_yellow", "Arena Turban", [("tuareg_open",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],

# A treatise on The Method of Mechanical Theorems Archimedes

#This book must be at the beginning of readable books
["book_tactics","De Re Militari", [("book_a",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
["book_persuasion","Rhetorica ad Herennium", [("book_b",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
["book_leadership","The Life of Alixenus the Great", [("book_d",0)], itp_type_book, 0, 4200,weight(2)|abundance(100),imodbits_none],
["book_intelligence","Essays on Logic", [("book_e",0)], itp_type_book, 0, 3000,weight(2)|abundance(100),imodbits_none],
["book_trade","A Treatise on the Value of Things", [("book_f",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
["book_weapon_mastery", "On the Art of Fighting with Swords", [("book_d",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
["book_engineering","Method of Mechanical Theorems", [("book_open",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
# New readable books with v0.12.
["book_tracking","Hunter's Journal on the Local Wildlife", [("book_open",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
["book_training","A Philospher's Approach", [("book_f",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
["book_firstaid","The Place of Herbs in Medicine", [("book_b",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
["book_prison_management","A Sailor's Guide to Ropework", [("book_a",0)], itp_type_book, 0, 4000,weight(2)|abundance(100),imodbits_none],
["book_charisma","The Needs of Man", [("book_d",0)], itp_type_book, 0, 3000,weight(2)|abundance(100),imodbits_none],
## Specialty Books ##
["book_repair_bonus", "Journal of Andrin the Smith", [("book_d",0)], itp_type_book, 0, 5000,weight(2)|abundance(100),imodbits_none],    # Reduces improvement repair costs when this character is engineer by 30%.
["book_tax_reduction","On Levies: Stategems for Taxation and Revenue", [("book_e",0)], itp_type_book, 0, 5000,weight(2)|abundance(100),imodbits_none],
["book_cunning_rule","The Courtier of Veluca", [("book_f",0)], itp_type_book, 0, 6500,weight(2)|abundance(100),imodbits_none],
["book_prosperity_1","Barnolo's Expanded Works On Land Stewardship", [("book_b",0)], itp_type_book, 0, 4250,weight(2)|abundance(100),imodbits_none],
["book_prof75_sword","Needlework by Arya", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_prof75_crossbow","Crossbow Design and Tactics", [("book_f",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_escape_chance","Tactics of the Open Field", [("book_d",0)], itp_type_book, 0, 5000,weight(2)|abundance(100),imodbits_none],
# Placeholders (use the last one first and move it up before "book_1".
["book_1","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_2","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_3","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_4","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_5","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_6","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_7","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_8","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_9","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_10","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_11","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_12","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_13","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_14","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_15","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_crossbow_prof","The Art of Crossbow Design", [("book_b",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],     # One time boost to crossbow proficiency of +30.
#Reference books
#This book must be at the beginning of reference books
["book_wound_treatment_reference","The Book of Healing", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_training_reference","Manual of Arms", [("book_open",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_surgery_reference","The Great Book of Surgery", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
# New reference books with v0.12.
["book_pathfinding_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_trade_ledger","Merchant's Trade Ledger", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_courtship","Idylls at Court", [("book_f",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
# Placeholders (use the last one first and move it up before "book_1_reference".
["book_1_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_2_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_3_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_4_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_5_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_6_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_7_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_8_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_9_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_10_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_11_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_12_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_13_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_14_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
["book_15_reference","Cartographer's Guide to Calradia", [("book_c",0)], itp_type_book, 0, 2500,weight(2)|abundance(100),imodbits_none],
#other trade goods (first one is spice)
["spice","Spice", [("spice_sack",0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 880,weight(40)|abundance(25)|max_ammo(50),imodbits_none],
["salt","Salt", [("salt_sack",0)], itp_merchandise|itp_type_goods, 0, 255,weight(50)|abundance(120),imodbits_none],


#["flour","Flour", [("salt_sack",0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 40,weight(50)|abundance(100)|food_quality(45)|max_ammo(50),imodbits_none],

["oil","Oil", [("oil",0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 450,weight(50)|abundance(60)|max_ammo(50),imodbits_none],

["pottery","Pottery", [("jug",0)], itp_merchandise|itp_type_goods, 0, 100,weight(50)|abundance(90),imodbits_none],

["raw_flax","Flax Bundle", [("raw_flax",0)], itp_merchandise|itp_type_goods, 0, 150,weight(40)|abundance(90),imodbits_none],
["linen","Linen", [("linen",0)], itp_merchandise|itp_type_goods, 0, 250,weight(40)|abundance(90),imodbits_none],

["wool","Wool", [("wool_sack",0)], itp_merchandise|itp_type_goods, 0, 130,weight(40)|abundance(90),imodbits_none],
["wool_cloth","Wool Cloth", [("wool_cloth",0)], itp_merchandise|itp_type_goods, 0, 250,weight(40)|abundance(90),imodbits_none],

["raw_silk","Raw Silk", [("raw_silk_bundle",0)], itp_merchandise|itp_type_goods, 0, 600,weight(30)|abundance(90),imodbits_none],
["raw_dyes","Dyes", [("dyes",0)], itp_merchandise|itp_type_goods, 0, 200,weight(10)|abundance(90),imodbits_none],
["velvet","Velvet", [("velvet",0)], itp_merchandise|itp_type_goods, 0, 1025,weight(40)|abundance(30),imodbits_none],

["iron","Iron", [("iron",0)], itp_merchandise|itp_type_goods, 0,264,weight(60)|abundance(60),imodbits_none],
["tools","Tools", [("iron_hammer",0)], itp_merchandise|itp_type_goods, 0, 410,weight(50)|abundance(90),imodbits_none],

["raw_leather","Hides", [("leatherwork_inventory",0)], itp_merchandise|itp_type_goods, 0, 120,weight(40)|abundance(90),imodbits_none],
["leatherwork","Leatherwork", [("leatherwork_frame",0)], itp_merchandise|itp_type_goods, 0, 220,weight(40)|abundance(90),imodbits_none],
["raw_date_fruit","Date Fruit", [("date_inventory",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 120,weight(40)|food_quality(10)|max_ammo(10),imodbits_none],
["furs","Furs", [("fur_pack",0)], itp_merchandise|itp_type_goods, 0, 391,weight(40)|abundance(90),imodbits_none],

["wine","Wine", [("amphora_slim",0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 220,weight(30)|abundance(60)|max_ammo(50),imodbits_none],
["ale","Ale", [("ale_barrel",0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 120,weight(30)|abundance(70)|max_ammo(50),imodbits_none],

# ["dry_bread", "wheat_sack", itp_type_goods|itp_consumable, 0, slt_none,view_goods,95,weight(2),max_ammo(50),imodbits_none],
#foods (first one is smoked_fish)
["smoked_fish","Smoked Fish", [("smoked_fish",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 65,weight(15)|abundance(110)|food_quality(50)|max_ammo(50),imodbits_none],
["cheese","Cheese", [("cheese_b",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 75,weight(6)|abundance(110)|food_quality(40)|max_ammo(30),imodbits_none],
["honey","Honey", [("honey_pot",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 220,weight(5)|abundance(110)|food_quality(40)|max_ammo(30),imodbits_none],
["sausages","Sausages", [("sausages",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 85,weight(10)|abundance(110)|food_quality(40)|max_ammo(40),imodbits_none],
["cabbages","Cabbages", [("cabbage",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 30,weight(15)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
["dried_meat","Dried Meat", [("smoked_meat",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 85,weight(15)|abundance(100)|food_quality(70)|max_ammo(50),imodbits_none],
["apples","Fruit", [("apple_basket",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 44,weight(20)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
["raw_grapes","Grapes", [("grapes_inventory",0)], itp_merchandise|itp_consumable|itp_type_goods, 0, 75,weight(40)|abundance(90)|food_quality(10)|max_ammo(10),imodbits_none], #x2 for wine
["raw_olives","Olives", [("olive_inventory",0)], itp_merchandise|itp_consumable|itp_type_goods, 0, 100,weight(40)|abundance(90)|food_quality(10)|max_ammo(10),imodbits_none], #x3 for oil
["grain","Grain", [("wheat_sack",0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 30,weight(30)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],

["cattle_meat","Beef", [("raw_meat",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 80,weight(20)|abundance(100)|food_quality(80)|max_ammo(50),imodbits_none],
["bread","Bread", [("bread_a",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 50,weight(30)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
["chicken","Chicken", [("chicken",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 95,weight(10)|abundance(110)|food_quality(40)|max_ammo(50),imodbits_none],
["pork","Pork", [("pork",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 75,weight(15)|abundance(100)|food_quality(70)|max_ammo(50),imodbits_none],
["butter","Butter", [("butter_pot",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 150,weight(6)|abundance(110)|food_quality(40)|max_ammo(30),imodbits_none],

#Would like to remove flour altogether and reduce chicken, pork and butter (perishables) to non-trade items. Apples could perhaps become a generic "fruit", also representing dried fruit and grapes
# Armagan: changed order so that it'll be easier to remove them from trade goods if necessary.
#************************************************************************************************
# ITEMS before this point are hardcoded into item_codes.h and their order should not be changed!
#************************************************************************************************

# Quest Items

["siege_supply","Supplies", [("ale_barrel",0)], itp_type_goods, 0, 96,weight(40)|abundance(70),imodbits_none],
["quest_wine","Wine", [("amphora_slim",0)], itp_type_goods, 0, 46,weight(40)|abundance(60)|max_ammo(50),imodbits_none],
["quest_ale","Ale", [("ale_barrel",0)], itp_type_goods, 0, 31,weight(40)|abundance(70)|max_ammo(50),imodbits_none],


# Tutorial Items

["tutorial_sword_1", "Sword", [("long_sword",0),("scab_longsw_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 0 , weight(1.5)|difficulty(0)|spd_rtng(100) | weapon_length(102)|swing_damage(18 , cut) | thrust_damage(15 ,  pierce),imodbits_sword ],
["tutorial_axe_1", "Axe", [("iron_ax",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 0 , weight(4)|difficulty(0)|spd_rtng(91) | weapon_length(108)|swing_damage(19 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["tutorial_spear_1", "Spear", [("spear",0)], itp_type_polearm| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear, 0 , weight(4.5)|difficulty(0)|spd_rtng(80) | weapon_length(158)|swing_damage(0 , cut) | thrust_damage(19 ,  pierce),imodbits_polearm ],
["tutorial_club_1", "Club", [("club",0)], itp_type_one_handed_wpn| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 0 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(95)|swing_damage(11 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["tutorial_battle_axe_1", "Battle Axe", [("battle_ax",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 0 , weight(5)|difficulty(0)|spd_rtng(88) | weapon_length(108)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["tutorial_arrows_1","Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0,weight(3)|abundance(160)|weapon_length(95)|thrust_damage(0,pierce)|max_ammo(20),imodbits_missile],
["tutorial_bolts_1","Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag", ixmesh_carry),("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0,weight(2.25)|abundance(90)|weapon_length(63)|thrust_damage(0,pierce)|max_ammo(18),imodbits_missile],
["tutorial_short_bow_1", "Short Bow", [("short_bow",0),("short_bow_carry",ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 0 , weight(1)|difficulty(0)|spd_rtng(98) | shoot_speed(49) | thrust_damage(12 ,  pierce  ),imodbits_bow ],
["tutorial_crossbow_1", "Crossbow", [("crossbow_a",0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_reload_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 0 , weight(3)|difficulty(0)|spd_rtng(42)|  shoot_speed(68) | thrust_damage(32,pierce)|max_ammo(1),imodbits_crossbow ],
["tutorial_throwing_daggers_1", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown |itp_primary ,itcf_throw_knife, 0 , weight(3.5)|difficulty(0)|spd_rtng(102) | shoot_speed(25) | thrust_damage(16 ,  cut)|max_ammo(14)|weapon_length(0),imodbits_missile ],
["tutorial_saddle_horse_1", "Saddle Horse", [("saddle_horse",0)], itp_type_horse, 0, 0,abundance(90)|body_armor(3)|difficulty(0)|horse_speed(40)|horse_maneuver(38)|horse_charge(8),imodbits_horse_basic],
["tutorial_shield_1", "Kite Shield", [("shield_kite_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(150),imodbits_shield ],
["tutorial_staff_no_attack_1","Staff", [("wooden_staff",0)],itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack,itc_parry_polearm|itcf_carry_sword_back,9, weight(3.5)|spd_rtng(120) | weapon_length(115)|swing_damage(0,blunt) | thrust_damage(0,blunt),imodbits_none],
["tutorial_staff_1","Staff", [("wooden_staff",0)],itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack,itc_staff|itcf_carry_sword_back,9, weight(3.5)|spd_rtng(120) | weapon_length(115)|swing_damage(16,blunt) | thrust_damage(16,blunt),imodbits_none],

#############################################
##### TOURNAMENT PLAY ENHANCEMENT ITEMS #####
#############################################
# Native Versions of Items
# TPE+ 1.1 items
["red_tpe_tunic",              "Tournament Tunic", [("arena_tunic_red",0)], itp_type_body_armor|itp_covers_legs,0,1720,weight(10)|abundance(55)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_plate,[],[fac_kingdom_1]],
["blue_tpe_tunic",             "Tournament Tunic", [("arena_tunic_blue",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(10)|abundance(55)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
["green_tpe_tunic",            "Tournament Tunic", [("arena_tunic_green",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(10)|abundance(55)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
["gold_tpe_tunic",             "Tournament Tunic", [("arena_tunic_yellow",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(10)|abundance(55)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
["red_tpe_armor",              "Tournament Armor", [("arena_armor_red",0)], itp_type_body_armor|itp_covers_legs,0,1720,weight(22)|abundance(55)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(0),imodbits_plate,[],[fac_kingdom_1]],
["blue_tpe_armor",             "Tournament Armor", [("arena_armor_blue",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(22)|abundance(55)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
["green_tpe_armor",            "Tournament Armor", [("arena_armor_green",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(22)|abundance(55)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
["gold_tpe_armor",             "Tournament Armor", [("arena_armor_yellow",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(22)|abundance(55)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
# ["red_tpe_tunic",              "Tournament Tunic", [("arena_tunicR_new",0)], itp_type_body_armor|itp_covers_legs,0,1720,weight(10)|abundance(55)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_plate,[],[fac_kingdom_1]],
# ["blue_tpe_tunic",             "Tournament Tunic", [("arena_tunicB_new",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(10)|abundance(55)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
# ["green_tpe_tunic",            "Tournament Tunic", [("arena_tunicG_new",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(10)|abundance(55)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
# ["gold_tpe_tunic",             "Tournament Tunic", [("arena_tunicY_new",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(10)|abundance(55)|head_armor(0)|body_armor(15)|leg_armor(8)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
# ["red_tpe_armor",              "Tournament Armor", [("arena_armorR_new",0)], itp_type_body_armor|itp_covers_legs,0,1720,weight(22)|abundance(55)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(0),imodbits_plate,[],[fac_kingdom_1]],
# ["blue_tpe_armor",             "Tournament Armor", [("arena_armorB_new",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(22)|abundance(55)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
# ["green_tpe_armor",            "Tournament Armor", [("arena_armorG_new",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(22)|abundance(55)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
# ["gold_tpe_armor",             "Tournament Armor", [("arena_armorY_new",0)], itp_type_body_armor|itp_covers_legs,0,1544,weight(22)|abundance(55)|head_armor(0)|body_armor(30)|leg_armor(15)|difficulty(0),imodbits_armor,[],[fac_kingdom_1]],
["tpe_enhanced_shield_red",    "Tournament Shield", [("arena_shield_red",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(600)|body_armor(15)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["tpe_enhanced_shield_blue",   "Tournament Shield", [("arena_shield_blue",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(600)|body_armor(15)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["tpe_enhanced_shield_green",  "Tournament Shield", [("arena_shield_green",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(600)|body_armor(15)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["tpe_enhanced_shield_yellow", "Tournament Shield", [("arena_shield_yellow",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  42 , weight(2)|hit_points(600)|body_armor(15)|spd_rtng(100)|weapon_length(60),imodbits_shield ],
["tpe_normal_boots",           "Tournament Greaves", [("spl_greaves",0)], itp_type_foot_armor |itp_civilian  | itp_attach_armature,0, 34 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["tpe_enhanced_boots",         "Tournament Greaves", [("lthr_greaves",0)], itp_type_foot_armor |itp_civilian  | itp_attach_armature,0, 34 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0) ,imodbits_cloth ],
["tpe_normal_spear",           "Tournament Spear", [("bb_serbian_spear_4",0)], itp_type_polearm| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear|itcf_overswing_polearm, 0 , weight(4.5)|difficulty(0)|spd_rtng(95) | weapon_length(118)|swing_damage(17 , blunt) | thrust_damage(25 ,  blunt),imodbits_polearm ],
["tpe_enhanced_spear",         "Tournament Spear", [("bb_serbian_spear_3",0)], itp_type_polearm| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_spear|itcf_overswing_polearm, 0 , weight(4.5)|difficulty(0)|spd_rtng(90) | weapon_length(148)|swing_damage(24 , blunt) | thrust_damage(35 ,  blunt),imodbits_polearm ],
["tpe_normal_bow",             "Tournament Bow", [("hunting_bow",0), ("hunting_bow_carry",ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1.5)|spd_rtng(90) | shoot_speed(40) | thrust_damage(24, blunt),imodbits_bow ],
["tpe_enhanced_bow",           "Tournament Bow", [("hunting_bow",0), ("hunting_bow_carry",ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1.5)|spd_rtng(95) | shoot_speed(40) | thrust_damage(36, blunt),imodbits_bow ],
["tpe_normal_crossbow",        "Tournament Crossbow", [("crossbow_a",0)], itp_type_crossbow |itp_primary|itp_two_handed ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 0, weight(3)|spd_rtng(50)| shoot_speed(68) | thrust_damage(40,blunt)|max_ammo(1),imodbits_crossbow],
["tpe_enhanced_crossbow",      "Tournament Crossbow", [("crossbow_a",0)], itp_type_crossbow |itp_primary|itp_two_handed ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 0, weight(3)|spd_rtng(60)| shoot_speed(68) | thrust_damage(56,blunt)|max_ammo(1),imodbits_crossbow],
["tpe_normal_javelin",         "Tournament Javelins", [("javelin",0),("javelins_quiver_new", ixmesh_carry)], itp_type_thrown |itp_primary|itp_next_item_as_melee,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 0, weight(5) | spd_rtng(100) | shoot_speed(28) | thrust_damage(27, blunt) | max_ammo(50) | weapon_length(75), imodbits_thrown],
["tpe_normal_javelin_melee",   "practice_javelin_melee", [("javelin",0)], itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry , itc_staff, 0, weight(1)|difficulty(0)|spd_rtng(90) |swing_damage(12, blunt)| thrust_damage(16,  blunt)|weapon_length(75),imodbits_polearm ],
["tpe_enhanced_javelin",       "Tournament Javelins", [("javelin",0),("javelins_quiver_new", ixmesh_carry)], itp_type_thrown |itp_primary|itp_next_item_as_melee,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 0, weight(5) | spd_rtng(100) | shoot_speed(28) | thrust_damage(40, blunt) | max_ammo(50) | weapon_length(75), imodbits_thrown],
["tpe_enhanced_javelin_melee", "Tournament Javelin Melee", [("javelin",0)], itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry , itc_staff, 0, weight(1)|difficulty(0)|spd_rtng(95) |swing_damage(12, blunt)| thrust_damage(22,  blunt)|weapon_length(90),imodbits_polearm ],
["tpe_normal_sword",           "Tournament Sword", [("practice_sword",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_wooden_parry|itp_wooden_attack, itc_longsword, 3,weight(1.5)|spd_rtng(95)|weapon_length(90)|swing_damage(18,blunt)|thrust_damage(16,blunt),imodbits_none],
["tpe_enhanced_sword",         "Tournament Sword", [("practice_sword",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_wooden_parry|itp_wooden_attack, itc_longsword, 243 , weight(1.5)|spd_rtng(105) | weapon_length(100)|swing_damage(27 , blunt) | thrust_damage(22 ,  blunt),imodbits_none ],
["tpe_normal_greatsword",      "Tournament Greatsword", [("heavy_practicesword",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_greatsword, 21, weight(6.25)|spd_rtng(80)|weapon_length(110)|swing_damage(27,blunt)|thrust_damage(22,blunt),imodbits_none],
["tpe_enhanced_greatsword",    "Tournament Greatsword", [("heavy_practicesword",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_greatsword|itcf_carry_sword_back, 670 , weight(2.75)|spd_rtng(90) | weapon_length(120)|swing_damage(40 , blunt) | thrust_damage(27 ,  blunt),imodbits_sword_high ],
["tpe_normal_lance",           "Tournament Lance", [("joust_of_peace",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_greatlance, 18, weight(4.25) |spd_rtng(70)|weapon_length(200)|swing_damage(10,blunt)|thrust_damage(15,blunt),imodbits_none],
["tpe_enhanced_lance",         "Tournament Lance", [("joust_of_peace",0)], itp_couchable|itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_greatlance, 90 , weight(4.25)|spd_rtng(75) | weapon_length(240)|swing_damage(15 , blunt) | thrust_damage(23 ,  blunt),imodbits_none ],
["tpe_normal_horse_red",       "Tournament Horse", [("ho_vae_long_royalred",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(100)|body_armor(15)|difficulty(0)|horse_speed(45)|horse_maneuver(41)|horse_charge(10)|horse_scale(110),imodbits_horse_basic],
["tpe_normal_horse_blue",      "Tournament Horse", [("ho_nor_war_bluebarded",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(100)|body_armor(15)|difficulty(0)|horse_speed(45)|horse_maneuver(41)|horse_charge(10)|horse_scale(110),imodbits_horse_basic],
["tpe_normal_horse_green",     "Tournament Horse", [("ho_rho_war_deergreen",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(100)|body_armor(15)|difficulty(0)|horse_speed(45)|horse_maneuver(41)|horse_charge(10)|horse_scale(110),imodbits_horse_basic],
["tpe_normal_horse_yellow",    "Tournament Horse", [("ho_sar_war_yellowroyal",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(100)|body_armor(15)|difficulty(0)|horse_speed(45)|horse_maneuver(41)|horse_charge(10)|horse_scale(110),imodbits_horse_basic],
["tpe_enhanced_horse_red",     "Tournament Warhorse", [("ho_vae_long_royalred",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(0)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["tpe_enhanced_horse_blue",    "Tournament Warhorse", [("ho_nor_war_bluebarded",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(0)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["tpe_enhanced_horse_green",   "Tournament Warhorse", [("ho_rho_war_deergreen",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(0)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["tpe_enhanced_horse_yellow",  "Tournament Warhorse", [("ho_sar_war_yellowroyal",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(0)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
# ["tpe_normal_horse_red",       "Tournament Horse", [("ho_vae_long_royalred",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(100)|body_armor(15)|difficulty(0)|horse_speed(45)|horse_maneuver(41)|horse_charge(10)|horse_scale(110),imodbits_horse_basic],
# ["tpe_normal_horse_blue",      "Tournament Horse", [("ho_nor_war_bluebarded",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(100)|body_armor(15)|difficulty(0)|horse_speed(45)|horse_maneuver(41)|horse_charge(10)|horse_scale(110),imodbits_horse_basic],
# ["tpe_normal_horse_green",     "Tournament Horse", [("ho_rho_war_deergreen",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(100)|body_armor(15)|difficulty(0)|horse_speed(45)|horse_maneuver(41)|horse_charge(10)|horse_scale(110),imodbits_horse_basic],
# ["tpe_normal_horse_yellow",    "Tournament Horse", [("ho_sar_war_yellowroyal",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(100)|body_armor(15)|difficulty(0)|horse_speed(45)|horse_maneuver(41)|horse_charge(10)|horse_scale(110),imodbits_horse_basic],
# ["tpe_enhanced_horse_red",     "Tournament Warhorse", [("ho_vae_long_royalred",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(0)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
# ["tpe_enhanced_horse_blue",    "Tournament Warhorse", [("ho_nor_war_bluebarded",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(0)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
# ["tpe_enhanced_horse_green",   "Tournament Warhorse", [("ho_rho_war_deergreen",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(0)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
# ["tpe_enhanced_horse_yellow",  "Tournament Warhorse", [("ho_sar_war_yellowroyal",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(0)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
# TPE+ 1.4 items
["tpe_normal_axe",             "Tournament Axe", [("we_sar_axe_onehanded",0)], itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 24 , weight(2) | spd_rtng(90) | weapon_length(70) | swing_damage(20, blunt) | thrust_damage(0, pierce), imodbits_axe],
["tpe_enhanced_axe",           "Tournament Axe", [("we_sar_axe_onehanded",0)], itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 24 , weight(2) | spd_rtng(95) | weapon_length(75) | swing_damage(28, blunt) | thrust_damage(0, pierce), imodbits_axe],
["tpe_normal_quarterstaff",    "Tournament Staff", [("we_sar_spear_staff",0)],itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack,itc_staff|itcf_carry_sword_back,9, weight(2.5)|spd_rtng(110) | weapon_length(118)|swing_damage(22, blunt) | thrust_damage(18,blunt),imodbits_none],
["tpe_enhanced_quarterstaff",  "Tournament Staff", [("we_sar_spear_staff",0)],itp_type_polearm|itp_offset_lance|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack,itc_staff|itcf_carry_sword_back,9, weight(2.5)|spd_rtng(115) | weapon_length(118)|swing_damage(31, blunt) | thrust_damage(25,blunt),imodbits_none],
["tpe_normal_greataxe",        "Tournament Greataxe", [("tutorial_battle_axe",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 0 , weight(5)|difficulty(0)|spd_rtng(85) | weapon_length(108)|swing_damage(27 , blunt) | thrust_damage(0 ,  blunt),imodbits_axe ],
["tpe_enhanced_greataxe",      "Tournament Greataxe", [("tutorial_battle_axe",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 0 , weight(5)|difficulty(0)|spd_rtng(90) | weapon_length(108)|swing_damage(38 , blunt) | thrust_damage(0 ,  blunt),imodbits_axe ],
["tpe_normal_scimitar",        "Tournament Scimitar", [("we_sar_sword_scimitar",0),("we_sar_scabbard_scimitar", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,411,weight(1.5)|abundance(60)|difficulty(0)|spd_rtng(100)|weapon_length(97)|swing_damage(16, blunt)|thrust_damage(0, blunt),imodbits_sword_high],
["tpe_enhanced_scimitar",      "Tournament Scimitar", [("we_sar_sword_scimitar",0),("we_sar_scabbard_scimitar", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,411,weight(1.5)|abundance(60)|difficulty(0)|spd_rtng(108)|weapon_length(97)|swing_damage(22, blunt)|thrust_damage(0, blunt),imodbits_sword_high],
["tpe_normal_throwing_axe",    "Tournament Throwing Axes", [("we_nor_axe_throw_light",0)], itp_type_thrown|itp_primary|itp_next_item_as_melee,itcf_throw_axe,100,weight(5)|abundance(100)|difficulty(0)|spd_rtng(85)|shoot_speed(18)|thrust_damage(30, blunt)|max_ammo(4)|weapon_length(53),imodbits_thrown_minus_heavy],
	["tpe_normal_throwing_axe_melee", "Tournament Throwing Axe", [("we_nor_axe_throw_light",0)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield,itc_scimitar,100,weight(1)|abundance(100)|difficulty(0)|spd_rtng(90)|weapon_length(53)|swing_damage(27, blunt),imodbits_thrown_minus_heavy],
["tpe_enhanced_throwing_axe",  "Tournament Throwing Axes", [("we_nor_axe_throw_light",0)], itp_type_thrown|itp_primary|itp_next_item_as_melee,itcf_throw_axe,100,weight(5)|abundance(100)|difficulty(0)|spd_rtng(85)|shoot_speed(18)|thrust_damage(42, blunt)|max_ammo(4)|weapon_length(53),imodbits_thrown_minus_heavy],
	["tpe_enhanced_throwing_axe_melee", "Tournament Throwing Axe", [("we_nor_axe_throw_light",0)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield,itc_scimitar,100,weight(1)|abundance(100)|difficulty(0)|spd_rtng(95)|weapon_length(63)|swing_damage(38, blunt),imodbits_thrown_minus_heavy],
["tpe_normal_throwing_daggers",   "Tournament Daggers", [("practice_dagger",0)], itp_type_thrown |itp_primary|itp_next_item_as_melee ,itcf_throw_knife, 0 , weight(3.5)|difficulty(0)|spd_rtng(100) | shoot_speed(25) | thrust_damage(16 , blunt)|max_ammo(25)|weapon_length(0),imodbits_missile],
	["tpe_normal_throwing_daggers_melee","Practice Dagger", [("practice_dagger",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_attack, itc_dagger|itcf_carry_dagger_front_left, 2,weight(0.5)|spd_rtng(110)|weapon_length(47)|swing_damage(14, blunt)|thrust_damage(14, blunt),imodbits_none],
["tpe_enhanced_throwing_daggers", "Tournament Daggers", [("practice_dagger",0)], itp_type_thrown |itp_primary|itp_next_item_as_melee ,itcf_throw_knife, 0 , weight(3.5)|difficulty(0)|spd_rtng(110) | shoot_speed(25) | thrust_damage(22 , blunt)|max_ammo(25)|weapon_length(0),imodbits_missile],
	["tpe_enhanced_throwing_daggers_melee","Practice Dagger", [("practice_dagger",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_attack, itc_dagger|itcf_carry_dagger_front_left, 2,weight(0.5)|spd_rtng(115)|weapon_length(47)|swing_damage(20, blunt)|thrust_damage(20, blunt),imodbits_none],

["water", "Water", [("water_inventory",0)], itp_type_goods|itp_merchandise|itp_consumable, 0, 50, weight(30)|abundance(70)|max_ammo(50), imodbits_none ],

##################
##### HORSES #####
##################


["sumpter_horse",			"Sumpter Horse",			 [("sumpter_horse",0)], itp_merchandise|itp_type_horse, 0, 134,abundance(90)|hit_points(100)|body_armor(14)|difficulty(1)|horse_speed(37)|horse_maneuver(39)|horse_charge(9)|horse_scale(100),imodbits_horse_basic],
["saddle_horse",			"Saddle Horse", 			[("saddle_horse",0),("horse_c",imodbits_horse_good)], itp_merchandise|itp_type_horse, 0, 240,abundance(90)|hit_points(100)|body_armor(8)|difficulty(1)|horse_speed(45)|horse_maneuver(44)|horse_charge(10)|horse_scale(104),imodbits_horse_basic],
["steppe_horse"	,			"Steppe Horse", 			[("steppe_horse",0)], itp_merchandise|itp_type_horse, 0, 192,abundance(80)|hit_points(120)|body_armor(10)|difficulty(2)|horse_speed(40)|horse_maneuver(51)|horse_charge(8)|horse_scale(98),imodbits_horse_basic, [], [fac_kingdom_2, fac_kingdom_3]],
["arabian_horse_a",			"Desert Horse", 			[("arabian_horse_a",0)], itp_merchandise|itp_type_horse, 0, 550,abundance(80)|hit_points(110)|body_armor(10)|difficulty(2)|horse_speed(42)|horse_maneuver(50)|horse_charge(12)|horse_scale(100),imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_3, fac_kingdom_6]],
["courser",					"Courser", 					[("courser",0)], itp_merchandise|itp_type_horse, 0, 600,abundance(70)|body_armor(12)|hit_points(110)|difficulty(2)|horse_speed(50)|horse_maneuver(44)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
["brown_courser", 			"Brown Courser", 			[("bandits_horse_a",0),("bandits_horse_a",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 810, abundance(60)|hit_points(110)|body_armor(12)|difficulty(2)|horse_speed(50)|horse_maneuver(44)|horse_charge(12)|horse_scale(106), imodbits_horse_basic|imodbit_champion ],
["dark_courser",			"Dark Courser", 			[("bandits_horse_b",0),("bandits_horse_b",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 810, abundance(60)|hit_points(110)|body_armor(12)|difficulty(2)|horse_speed(50)|horse_maneuver(44)|horse_charge(12)|horse_scale(106), imodbits_horse_basic|imodbit_champion ],
["elite_courser",			"Elite Courser", 			[("horse_tyrk_a",0),("horse_tyrk_a",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 810, abundance(60)|hit_points(180)|body_armor(20)|difficulty(3)|horse_speed(50)|horse_maneuver(51)|horse_charge(18)|horse_scale(108), imodbits_horse_basic|imodbit_champion ],
["arabian_horse_b",			"Sarranid Horse", 			[("arabian_horse_b",0)], itp_merchandise|itp_type_horse, 0, 700,abundance(80)|hit_points(120)|body_armor(10)|difficulty(3)|horse_speed(43)|horse_maneuver(54)|horse_charge(16)|horse_scale(100),imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_6]],
["hunter",					"Hunter",					[("hunting_horse",0),("hunting_horse",imodbits_horse_good)], itp_merchandise|itp_type_horse, 0, 810,abundance(60)|hit_points(160)|body_armor(18)|difficulty(3)|horse_speed(43)|horse_maneuver(44)|horse_charge(24)|horse_scale(108),imodbits_horse_basic|imodbit_champion],
["dark_brown_hunter", 		"Dark Brown Hunter", 		[("bandits_horse_c",0),("bandits_horse_c",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 810, abundance(60)|hit_points(160)|body_armor(18)|difficulty(3)|horse_speed(43)|horse_maneuver(44)|horse_charge(24)|horse_scale(108), imodbits_horse_basic|imodbit_champion ],
["white_hunter", 			"White Hunter", 			[("bandits_horse_d",0),("bandits_horse_d",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 810, abundance(60)|hit_points(160)|body_armor(18)|difficulty(3)|horse_speed(43)|horse_maneuver(44)|horse_charge(24)|horse_scale(108), imodbits_horse_basic|imodbit_champion ],
["warhorse",				"War Horse", 				[("warhorse_chain",0)], itp_merchandise|itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(4)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["war_horse_a",				"Light War Horse", 			[("saracin_hard_horses_c",0)], itp_merchandise|itp_type_horse, 0, 700,abundance(50)|hit_points(120)|body_armor(22)|difficulty(2)|horse_speed(44)|horse_maneuver(44)|horse_charge(22)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["war_horse_b",				"War Horse", 				[("saracin_hard_horses_a",0)], itp_merchandise|itp_type_horse, 0, 900,abundance(50)|hit_points(125)|body_armor(30)|difficulty(3)|horse_speed(41)|horse_maneuver(40)|horse_charge(26)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["war_horse_c",				"Heavy War Horse", 			[("saracin_hard_horses_b",0)], itp_merchandise|itp_type_horse, 0, 1300,abundance(50)|hit_points(150)|body_armor(48)|difficulty(4)|horse_speed(32)|horse_maneuver(32)|horse_charge(32)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["war_horse_d",				"Elite War Horse", 			[("saracin_hard_horses_d",0)], itp_merchandise|itp_type_horse, 0, 1600,abundance(50)|hit_points(165)|body_armor(40)|difficulty(5)|horse_speed(44)|horse_maneuver(43)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["war_horse_e",				"Royal War Horse", 			[("saracen_horse_Sultan",0)], itp_merchandise|itp_type_horse, 0, 2000,abundance(50)|hit_points(175)|body_armor(32)|difficulty(4)|horse_speed(48)|horse_maneuver(48)|horse_charge(25)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
["charger",					"Charger", 					[("charger_new",0)], itp_merchandise|itp_type_horse, 0, 1811,abundance(40)|hit_points(165)|body_armor(58)|difficulty(4)|horse_speed(40)|horse_maneuver(44)|horse_charge(32)|horse_scale(112),imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1, fac_kingdom_5]],

#Wilk22's Hussar Wing
["winged_horse",			"Winged Horse",				[("Hus",0),("Hus",imodbits_horse_good)], itp_merchandise|itp_type_horse, 0, 810,abundance(60)|hit_points(200)|body_armor(25)|difficulty(4)|horse_speed(48)|horse_maneuver(50)|horse_charge(24)|horse_scale(108),imodbits_horse_basic|imodbit_champion],

#Bloc's Northerner Horses
["northerner_horse",    	"Northerner Horse", 		[("northerner_horse",0),("horse_c",imodbits_horse_good)], itp_merchandise|itp_type_horse, 0, 350,abundance(90)|hit_points(150)|body_armor(20)|difficulty(1)|horse_speed(35)|horse_maneuver(44)|horse_charge(16)|horse_scale(104),imodbits_horse_basic, [], [fac_kingdom_2, fac_kingdom_3]],
["northerner_horse_black",	"Northerner Horse Black", 	[("northerner_horse_black",0),("horse_c",imodbits_horse_good)], itp_merchandise|itp_type_horse, 0, 480,abundance(90)|hit_points(160)|body_armor(22)|difficulty(2)|horse_speed(39)|horse_maneuver(44)|horse_charge(19)|horse_scale(104),imodbits_horse_basic, [], [fac_kingdom_2, fac_kingdom_3]],
["northerner_horse_white",	"Northerner Horse White", 	[("northerner_horse_white",0)], itp_merchandise|itp_type_horse, 0, 660,abundance(80)|hit_points(175)|body_armor(24)|difficulty(3)|horse_speed(42)|horse_maneuver(51)|horse_charge(21)|horse_scale(98),imodbits_horse_basic, [], [fac_kingdom_2, fac_kingdom_3]],
["northerner_horse_hunter",	"Northerner Horse Hunt", 	[("northerner_horse_hunter",0)], itp_merchandise|itp_type_horse, 0, 850,abundance(80)|hit_points(190)|body_armor(26)|difficulty(4)|horse_speed(45)|horse_maneuver(51)|horse_charge(24)|horse_scale(98),imodbits_horse_basic, [], [fac_kingdom_2, fac_kingdom_3]],






####################### HERALDIC HORSES #######################
["wse_charger","Charger", [("wse_charger",0)], itp_merchandise|itp_type_horse, 0, 1811,abundance(40)|hit_points(165)|body_armor(58)|difficulty(4)|horse_speed(40)|horse_maneuver(44)|horse_charge(32)|horse_scale(112),imodbits_horse_basic|imodbit_champion, 
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),
                      (try_begin), #for in missions
		                (agent_is_active, ":agent_no"),
		                (agent_get_rider, ":agent_no", ":agent_no"),
		                (agent_get_troop_id, ":troop_no", ":agent_no"),
	                  (try_end), 
                      (call_script, "script_shield_item_set_banner", "tableau_wse_charger", ":agent_no", ":troop_no")])]],
["wse_warhorse","War Horse", [("wse_warhorse_chain",0)], itp_merchandise|itp_type_horse, 0, 1224,abundance(50)|hit_points(165)|body_armor(40)|difficulty(4)|horse_speed(40)|horse_maneuver(41)|horse_charge(28)|horse_scale(110),imodbits_horse_basic|imodbit_champion,                      
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),
                      (try_begin), #for in missions
		                (agent_is_active, ":agent_no"),
		                (agent_get_rider, ":agent_no", ":agent_no"),
		                (agent_get_troop_id, ":troop_no", ":agent_no"),
	                  (try_end), 
                      (call_script, "script_shield_item_set_banner", "tableau_wse_warhorse_chain", ":agent_no", ":troop_no")])]], 
["wse_warhorse_sarranid","Sarranian War Horse", [("wse_warhorse_sarranid",0)], itp_merchandise|itp_type_horse, 0, 1811,abundance(40)|hit_points(165)|body_armor(58)|difficulty(5)|horse_speed(40)|horse_maneuver(44)|horse_charge(32)|horse_scale(112),imodbits_horse_basic|imodbit_champion,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),
                      (try_begin), #for in missions
		                (agent_is_active, ":agent_no"),
		                (agent_get_rider, ":agent_no", ":agent_no"),
		                (agent_get_troop_id, ":troop_no", ":agent_no"),
	                  (try_end), 
                      (call_script, "script_shield_item_set_banner", "tableau_wse_warhorse_sarranid", ":agent_no", ":troop_no")])]], 
["wse_warhorse_steppe","Steppe Charger", [("wse_warhorse_steppe",0)], itp_merchandise|itp_type_horse, 0, 1400,abundance(45)|hit_points(150)|body_armor(40)|difficulty(5)|horse_speed(40)|horse_maneuver(50)|horse_charge(28)|horse_scale(112),imodbits_horse_basic|imodbit_champion,
  [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),
                      (try_begin), #for in missions
		                (agent_is_active, ":agent_no"),
		                (agent_get_rider, ":agent_no", ":agent_no"),
		                (agent_get_troop_id, ":troop_no", ":agent_no"),
	                  (try_end), 
                      (call_script, "script_shield_item_set_banner", "tableau_wse_warhorse_steppe", ":agent_no", ":troop_no")])]],   


["camel", 			"Camel",			[("bedyin_camel_a",0),("bedyin_camel_a",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 810, abundance(60)|hit_points(160)|body_armor(18)|difficulty(3)|horse_speed(43)|horse_maneuver(44)|horse_charge(24)|horse_scale(108), imodbits_horse_basic|imodbit_champion ],

#["warhorse_sarranid","Sarranian War Horse", [("warhorse_sarranid",0)], itp_merchandise|itp_type_horse, 0, 1811,abundance(40)|hit_points(165)|body_armor(58)|difficulty(4)|horse_speed(40)|horse_maneuver(44)|horse_charge(32)|horse_scale(112),imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_6]],
#["warhorse_steppe","Steppe Charger", [("warhorse_steppe",0)], itp_merchandise|itp_type_horse, 0, 1400,abundance(45)|hit_points(150)|body_armor(40)|difficulty(4)|horse_speed(40)|horse_maneuver(50)|horse_charge(28)|horse_scale(112),imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_3,fac_kingdom_2]],

#["teutonic_horse1",	"Teutonic Horse",	[("heraldic_horse_1",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(145)|body_armor(38)|difficulty(4)|horse_speed(45)|horse_maneuver(43)|horse_charge(23)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
#["teutonic_horse2",	"Teutonic Horse",	[("heraldic_horse_2",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(145)|body_armor(38)|difficulty(4)|horse_speed(45)|horse_maneuver(43)|horse_charge(23)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
#["teutonic_horse3",	"Teutonic Horse",	[("heraldic_horse_3",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(145)|body_armor(38)|difficulty(4)|horse_speed(45)|horse_maneuver(43)|horse_charge(23)|horse_scale(110),imodbits_horse_basic|imodbit_champion],
#["teutonic_horse4",	"Teutonic Horse",	[("heraldic_horse_4",0)], itp_type_horse, 0, 1224,abundance(50)|hit_points(145)|body_armor(38)|difficulty(4)|horse_speed(45)|horse_maneuver(43)|horse_charge(23)|horse_scale(110),imodbits_horse_basic|imodbit_champion],


#remove ++
#["black_courser","Black Courser", [("courser_black",0)], itp_merchandise|itp_type_horse, 0, 650,abundance(70)|body_armor(12)|hit_points(110)|difficulty(4)|horse_speed(52)|horse_maneuver(46)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
#["grey_courser","Grey Courser", [("courser_grey",0)], itp_merchandise|itp_type_horse, 0, 620,abundance(70)|body_armor(12)|hit_points(110)|difficulty(4)|horse_speed(51)|horse_maneuver(45)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
#["destrier_black","Black Destrier", [("destrier_black",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(12)|hit_points(130)|difficulty(4)|horse_speed(47)|horse_maneuver(44)|horse_charge(20)|horse_scale(113),imodbits_horse_basic|imodbit_champion],
#["destrier_red","Red Destrier", [("destrier_red",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(12)|hit_points(130)|difficulty(4)|horse_speed(47)|horse_maneuver(44)|horse_charge(20)|horse_scale(113),imodbits_horse_basic|imodbit_champion],

#["mod_steppe_blackapp","Steppe Black Appaloosa", [("WSteppeblackappaloosa",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_steppe_bayapp","Steppe Bay Appaloosa", [("WSteppebayappaloosa",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_steppe_chestnutapp","Steppe Chestnut Appaloosa", [("WSteppeChestnutappy",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_steppe_greypaint","Steppe Grey Paint", [("WSteppeGreyPaint",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_steppe_blackpaint","Steppe Black Paint", [("WSteppeBlackPaint",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_steppe_brownpaint","Steppe Brown Paint", [("WSteppeBrownPaint",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_steppe_brownspot","Steppe Brown Spotted", [("WSteppeBrownSpot",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_steppe_splash","Steppe Splash", [("WSteppeSplash",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_steppe_buckskin","Steppe Buckskin", [("WSteppeBuckskin",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic|imodbit_champion],
#["mod_steppe_dun","Steppe Dun", [("WSteppeDun",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic|imodbit_champion],
#["mod_steppe_chestnutspot","Steppe Chestnut Spot", [("WSteppeChestnutSpot",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(2)|horse_speed(44)|horse_maneuver(50)|horse_charge(8)|horse_scale(98),imodbits_horse_basic],
#["mod_courser_darkdapp","Dark Dapple Courser", [("WCourserDarkdapple",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(12)|hit_points(110)|difficulty(2)|horse_speed(50)|horse_maneuver(45)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
#["mod_courser_lightdapp","Light Dapple Courser", [("WCourserLightDapple",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(12)|hit_points(110)|difficulty(2)|horse_speed(50)|horse_maneuver(45)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
#["mod_courser_grullbrindle","Grullo Brindle Courser", [("WCourserGrulloBrindle",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(12)|hit_points(110)|difficulty(2)|horse_speed(50)|horse_maneuver(45)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
#["mod_courser_bayappy","Bay Appaloosa Courser", [("WCourserBayappy",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(12)|hit_points(110)|difficulty(2)|horse_speed(50)|horse_maneuver(45)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
#["mod_courser_grullappy","Grullo Appaloosa Courser", [("WCourserGrullaappy",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(12)|hit_points(110)|difficulty(2)|horse_speed(50)|horse_maneuver(45)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
#["mod_courser_pinto","Pinto Courser", [("WCourserPinto",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(12)|hit_points(110)|difficulty(2)|horse_speed(50)|horse_maneuver(45)|horse_charge(12)|horse_scale(106),imodbits_horse_basic|imodbit_champion],
#["mod_arab_paint","Sarrdakian Paint", [("WArabPaint",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(3)|horse_speed(43)|horse_maneuver(54)|horse_charge(16)|horse_scale(100),imodbits_horse_basic|imodbit_champion],
#["mod_arab_black","Black Sarrdakian ", [("WArabBlack",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(3)|horse_speed(43)|horse_maneuver(54)|horse_charge(16)|horse_scale(100),imodbits_horse_basic|imodbit_champion],
#["mod_arab_white","White Sarrdakian", [("WArabGrey",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(3)|horse_speed(43)|horse_maneuver(54)|horse_charge(16)|horse_scale(100),imodbits_horse_basic|imodbit_champion],
#["mod_arab_brown","Brown Sarrdakian", [("WArabBrown",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(3)|horse_speed(43)|horse_maneuver(54)|horse_charge(16)|horse_scale(100),imodbits_horse_basic|imodbit_champion],
#["mod_arab_darkbrown","Dark Brown Sarrdakian", [("WArabDarkBrown",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(3)|horse_speed(43)|horse_maneuver(54)|horse_charge(16)|horse_scale(100),imodbits_horse_basic|imodbit_champion],
#["mod_arab_appy","Sarrdakian Appaloosa", [("WArabAppy",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(70)|body_armor(10)|hit_points(120)|difficulty(3)|horse_speed(43)|horse_maneuver(54)|horse_charge(16)|horse_scale(100),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_bay","Bay Destrier", [("WDestrierBay3",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_bay2","Dark Bay Destrier", [("WDestrierBay4",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_bay3","Brown Destrier", [("WDestrierBay5",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_chestnut","Chestnut Destrier", [("WDestrierChestnut1",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_chocolate","Chocolate Destrier", [("WDestrierChestnut3",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_chestnut2","Chestnut Destrier", [("WDestrierChestnut4",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_brindle","Brindle Destrier", [("WDestrierBrindleBay",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(5)|horse_speed(42)|horse_maneuver(47)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_snowflake","Snowflake Destrier", [("WDestrierBaysnowflake",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_appybay","Appaloosa Bay Destrier", [("WDestrierAppyBay",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_flea","Grey Destrier", [("WDestrierFleabittenGrey",0)], itp_merchandise|itp_type_horse, 0, 780,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(47)|horse_maneuver(46)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_dapplegrey","Dapple Grey Destrier", [("WDestrierDapplegrey",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_grullo","Grullo Destrier", [("WDestrierGrullo",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(45)|horse_maneuver(42)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_blacksnow","Black Snowflake Destrier", [("WDestrierBlackSnowflake",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
##["mod_destrier_blue","Blue Roan Destrier", [("WDestrierBlueRoan",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(45)|horse_maneuver(42)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#["mod_destrier_blackpaint","Black Paint Destrier", [("WDestrierBlackPaint",0)], itp_merchandise|itp_type_horse, 0, 680,abundance(50)|body_armor(18)|hit_points(165)|difficulty(4)|horse_speed(42)|horse_maneuver(45)|horse_charge(26)|horse_scale(112),imodbits_horse_basic|imodbit_champion],
#remove--


#xenoargh's camel - remove
#["camel",    						"Camel", 							[("camel",0)], itp_merchandise|itp_type_horse, 0, 350,abundance(90)|hit_points(150)|body_armor(20)|difficulty(1)|horse_speed(35)|horse_maneuver(44)|horse_charge(16)|horse_scale(104),imodbits_horse_basic, [], [fac_kingdom_6]],

#["steppe_char_iron",				"Barded Steppe Charger", 			[("steppe_charger_iron",0)], itp_merchandise|itp_type_horse, 0, 1400,abundance(60)|hit_points(150)|body_armor(40)|difficulty(4)|horse_speed(40)|horse_maneuver(50)|horse_charge(28)|horse_scale(112),imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_3,fac_kingdom_2]],
#["steppe_char_brass",				"Barded Steppe Charger", 			[("steppe_charger_brass",0)], itp_merchandise|itp_type_horse, 0, 1400,abundance(60)|hit_points(150)|body_armor(40)|difficulty(4)|horse_speed(40)|horse_maneuver(50)|horse_charge(28)|horse_scale(112),imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_3,fac_kingdom_2]],



######################
##### AMMUNITION #####
######################


##################### Arrows #####################
["arrows",				"Broadhead Arrows",	[("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver", ixmesh_carry)], itp_type_arrows|itp_merchandise|itp_default_ammo, itcf_carry_quiver_back, 72,weight(3)|abundance(160)|weapon_length(95)|thrust_damage(8,cut)|max_ammo(20),imodbits_missile],
["khergit_arrows",		"Khergit Arrows", 	[("arrow_b",0),("flying_missile",ixmesh_flying_ammo),("quiver_b", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right, 410,weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(8,pierce)|max_ammo(20),imodbits_missile, [], [fac_kingdom_3]],
["barbed_arrows",		"Barbed Arrows", 	[("barbed_arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver_d", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right, 124,weight(3)|abundance(70)|weapon_length(95)|thrust_damage(2,cut)|max_ammo(30),imodbits_missile],
["bodkin_arrows",		"Bodkin Arrows", 	[("piercing_arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver_c", ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right, 350,weight(3)|abundance(50)|weapon_length(91)|thrust_damage(2,pierce)|max_ammo(30),imodbits_missile],
["practice_arrows_2",	"Practice Arrows",	[("arena_arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0,weight(1.5)|weapon_length(95)|max_ammo(80),imodbits_missile],

##################### Bolts #####################
["bolts",				"Bolts", 			[("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag", ixmesh_carry),("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts|itp_merchandise|itp_default_ammo|itp_can_penetrate_shield, itcf_carry_quiver_right_vertical, 64,weight(2.25)|abundance(90)|weapon_length(63)|thrust_damage(1,pierce)|max_ammo(29),imodbits_missile],
["steel_bolts",			"Steel Bolts", 		[("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag_c", ixmesh_carry)], itp_type_bolts|itp_merchandise|itp_can_penetrate_shield, itcf_carry_quiver_right_vertical, 210,weight(2.5)|abundance(20)|weapon_length(63)|thrust_damage(2,pierce)|max_ammo(29),imodbits_missile, [], [fac_kingdom_5, fac_kingdom_1]],

##################### Bullets #####################
["cartridges",			"Cartridges",		[("cartridge_a",0)], itp_type_bullets|itp_merchandise|itp_can_penetrate_shield|itp_default_ammo, 0, 41,weight(2.25)|abundance(90)|weapon_length(3)|thrust_damage(1,pierce)|max_ammo(50),imodbits_missile],


##################
##### GLOVES #####
##################



["nobleman_gloves",			"Nobleman Gloves", 			[("gloves_king_L",0)], itp_type_hand_armor|itp_merchandise, 0, 1000, weight(0.2)|abundance(120)|body_armor(3)|difficulty(0), imodbits_cloth ],
["leather_gloves",			"Leather Gloves", 			[("leather_gloves_L",0)], itp_merchandise|itp_type_hand_armor,0, 120, weight(0.2)|abundance(120)|body_armor(3)|difficulty(0),imodbits_cloth],
["reinforced_leather_gloves", "Reinforced Leather Gloves", [("gloves_lord_L",0)], itp_type_hand_armor|itp_merchandise, 0, 250, weight(0.7)|abundance(120)|body_armor(5)|difficulty(0), imodbits_cloth ],
["mail_mittens",			"Mail Mittens", 			[("mail_mittens_L",0)], itp_merchandise|itp_type_hand_armor,0, 333, weight(0.7)|abundance(100)|body_armor(5)|difficulty(0),imodbits_armor],
["brass_lamellar_gauntlets","Brass Lamellar Gauntlets",	[("brass_l_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, 480, weight(1.2)|abundance(100)|body_armor(6)|difficulty(0),imodbits_armor, [], [fac_kingdom_6]],
["scale_gauntlets",			"Scale Gauntlets", 			[("scale_gauntlets_b_L",0)], itp_merchandise|itp_type_hand_armor,0, 653, weight(1.2)|abundance(100)|body_armor(7)|difficulty(0),imodbits_armor],
["plated_gauntlets", 		"Plated Gauntlets", [("gauntlets_arabs_a_L",0),("gauntlets_arabs_a_L",imodbit_reinforced)], itp_type_hand_armor|itp_merchandise, 0, 950, weight(1.4)|abundance(100)|body_armor(7)|difficulty(0), imodbits_armor ],
["ornate_plated_gauntlets", "Ornate Plated Gauntlets", [("gauntlets_arabs_b_L",0),("gauntlets_arabs_b_L",imodbit_reinforced)], itp_type_hand_armor|itp_merchandise, 0, 1500, weight(1.6)|abundance(100)|body_armor(10)|difficulty(0), imodbits_armor ],
["gauntlets",				"Gauntlets", 				[("gauntlets_L",0),("gauntlets_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1080, weight(1.9)|abundance(100)|body_armor(9)|difficulty(0),imodbits_armor],
["black_plate_mittens",		"Black Plate Mittens",		[("black_mitty_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1080, weight(1.9)|abundance(100)|body_armor(9)|difficulty(0),imodbits_armor],
["bnw_gauntlets",			"Black and White Gauntlets",[("bnw_gauntlet_R",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1080, weight(1.9)|abundance(100)|body_armor(9)|difficulty(0),imodbits_armor, [], [fac_kingdom_1, fac_kingdom_5]],
["plate_mittens",			"Plate Mittens", 			[("plate_mittens_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1333, weight(2.1)|abundance(100)|body_armor(10)|difficulty(0),imodbits_armor, [], [fac_kingdom_1, fac_kingdom_5]],

#["padded_gloves",			"Padded Gloves", 			[("leather_gloves_L",0)], itp_merchandise|itp_type_hand_armor,0, 53, weight(0.1)|abundance(120)|body_armor(2)|difficulty(0),imodbits_cloth],
#["leather_gloves_2",		"Vaegiran Leather Gloves", 	[("leather_gloves_L",0)], itp_merchandise|itp_type_hand_armor,0, 213, weight(0.2)|abundance(120)|body_armor(4)|difficulty(0),imodbits_cloth, [], [fac_kingdom_2]],
#["brass_scale_gauntlets",	"Brass Scale Gauntlets",	[("brass_s_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, 480, weight(1.2)|abundance(100)|body_armor(6)|difficulty(0),imodbits_armor, [], [fac_kingdom_6]],
#["nord_mail_gauntlets",	"Nordic Raider Gauntlets",	[("scale_gauntlets_b_L",0)], itp_merchandise|itp_type_hand_armor,0, 653, weight(0.8)|abundance(100)|body_armor(6)|difficulty(0),imodbits_armor, [], [fac_kingdom_4]],
#["lamellar_gauntlets",		"Lamellar Gauntlets",		[("scale_gauntlets_a_L",0)], itp_merchandise|itp_type_hand_armor,0, 653, weight(1.2)|abundance(100)|body_armor(7)|difficulty(0),imodbits_armor, [], [fac_kingdom_2]],
#["bronzeplatemitten",		"Bronze Plate Mittens",		[("bronze_mitten_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1080, weight(1.9)|abundance(100)|body_armor(9)|difficulty(0),imodbits_armor],


## WINDYPLAINS- ##
## WINDYPLAINS+ ## - Original values.
# ["leather_gloves",			"Leather Gloves", 			[("leather_gloves_L",0)], itp_merchandise|itp_type_hand_armor,0, 105, weight(0.3)|abundance(120)|body_armor(3)|difficulty(0),imodbits_cloth],
# ["mail_mittens",			"Mail Mittens", 			[("mail_mittens_L",0)], itp_merchandise|itp_type_hand_armor,0, 180, weight(0.5)|abundance(100)|body_armor(5)|difficulty(0),imodbits_armor],
# ["scale_gauntlets",			"Scale Gauntlets", 			[("scale_gauntlets_b_L",0)], itp_merchandise|itp_type_hand_armor,0, 370, weight(0.8)|abundance(100)|body_armor(7)|difficulty(0),imodbits_armor],
# ["lamellar_gauntlets",		"Lamellar Gauntlets",		[("scale_gauntlets_a_L",0)], itp_merchandise|itp_type_hand_armor,0, 370, weight(0.8)|abundance(100)|body_armor(7)|difficulty(0),imodbits_armor, [], [fac_kingdom_2]],
# ["gauntlets",				"Gauntlets", 				[("gauntlets_L",0),("gauntlets_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 840, weight(1.0)|abundance(100)|body_armor(9)|difficulty(0),imodbits_armor],
## SILVERSTAG+ ## - Mod Gloves
# ["padded_gloves",			"Padded Gloves", 			[("leather_gloves_L",0)], itp_merchandise|itp_type_hand_armor,0, 105, weight(0.3)|abundance(120)|body_armor(3)|difficulty(0),imodbits_cloth],
# ["plate_mittens",			"Plate Mittens", 			[("plate_mittens_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1015, weight(1.3)|abundance(100)|body_armor(10)|difficulty(0),imodbits_armor, [], [fac_kingdom_1, fac_kingdom_5]],
# ["bnw_gauntlets",			"Black and White Gauntlets", [("bnw_gauntlet_R",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 840, weight(1.0)|abundance(100)|body_armor(9)|difficulty(0),imodbits_armor, [], [fac_kingdom_1, fac_kingdom_5]],
# ## WINDYPLAINS+ ## - TAVERN ANIMATION PACK - OSP by Slawomir of Aaarrghh
# ["dedal_kufel",				"Kufel",					[("dedal_kufelL",0)],	itp_type_hand_armor,0,0,weight(1),0],
# ["dedal_lutnia",			"Lutnia",					[("dedal_lutniaL",0)],	itp_type_hand_armor,0,0,weight(1),0],
# ["dedal_lira",				"Lira",						[("dedal_liraL",0)],		itp_type_hand_armor,0,0,weight(1),0],
# ## WINDYPLAINS- ##
# ["leather_gloves_2",		"Vaegiran Leather Gloves", 	[("leather_gloves_L",0)], itp_merchandise|itp_type_hand_armor,0, 145, weight(0.4)|abundance(120)|body_armor(4)|difficulty(0),imodbits_cloth, [], [fac_kingdom_2]],
# ["blackplatemitty",			"Black Plate Mittens", 		[("black_mitty_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1940, weight(1.5)|abundance(100)|body_armor(9)|difficulty(0),imodbits_armor],
# ["bronzeplatemitten",		"Bronze Plate Mittens", 	[("bronze_mitten_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1940, weight(1.5)|abundance(100)|body_armor(9)|difficulty(0),imodbits_armor],
# ["brass_scale_gauntlets",	"Brass Scale Gauntlets",	[("brass_s_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, 710, weight(0.75)|abundance(100)|body_armor(5)|difficulty(0),imodbits_armor, [], [fac_kingdom_6]],
# ["brass_lamellar_gauntlets","Brass Lamellar Gauntlets",	[("brass_l_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, 910, weight(0.75)|abundance(100)|body_armor(5)|difficulty(0),imodbits_armor, [], [fac_kingdom_6]],
## WINDYPLAINS- ##


####################
##### FOOTWEAR #####
####################

["bear_paw_shoes", 				"Bear Paw Shoes", 				[("bear_paw_shoes",0)], itp_merchandise| itp_type_foot_armor |itp_civilian  | itp_attach_armature,0, 150 , weight(1)|abundance(1000)|head_armor(0)|body_armor(0)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["narf_hose", 					"Woolen Hose", 					[("narf_hose",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 7 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(4)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_1, fac_kingdom_5]],
["wrapping_boots", 				"Wrapping Boots", 				[("wrapping_boots_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 3 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(3)|difficulty(0) ,imodbits_cloth ],
["woolen_hose", 				"Woolen Hose", 					[("woolen_hose_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature , 0 , 7 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(4)|difficulty(0) ,imodbits_cloth ],
["blue_hose", 					"Blue Hose", 					[("blue_hose_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 7 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(4)|difficulty(0) ,imodbits_cloth ],
["hunter_boots", 				"Hunter Boots", 				[("hunter_boots_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature,0, 30 , weight(1.3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["hide_boots", 					"Hide Boots", 					[("hide_boots_a",0)], itp_merchandise| itp_type_foot_armor |itp_civilian  | itp_attach_armature,0, 25 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["ankle_boots", 				"Ankle Boots", 					[("ankle_boots_a_new",0)], itp_merchandise| itp_type_foot_armor |itp_civilian  | itp_attach_armature,0, 18 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["nomad_boots", 				"Nomad Boots", 					[("nomad_boots_a",0)], itp_merchandise| itp_type_foot_armor  |itp_civilian | itp_attach_armature,0, 50 , weight(1.3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["leather_boots", 				"Leather Boots", 				[("leather_boots_a",0)], itp_merchandise| itp_type_foot_armor  |itp_civilian | itp_attach_armature,0, 42 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["heavy_leather_boots",  		"Heavy Leather Boots", 			[("light_leather_boots",0)], itp_type_foot_armor |itp_merchandise| itp_attach_armature,0, 60 , weight(1.3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["hose_kneecops_red", 			"Woolen Hose with Kneecops", 	[("hose_kneecops_red",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature ,0, 400 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_1, fac_kingdom_5]],
["hose_kneecops_green", 		"Woolen Hose with Kneecops", 	[("hose_kneecops_green",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature ,400, 15 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_1, fac_kingdom_5]],
["splinted_leather_greaves", 	"Splinted Leather Greaves", 	[("leather_greaves_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0, 260 , weight(2.3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(17)|difficulty(0) ,imodbits_armor ],
["splinted_greaves", 			"Splinted Greaves", 			[("splinted_greaves_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0, 440 , weight(2.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(22)|difficulty(0) ,imodbits_armor ],
["mail_chausses", 				"Mail Chausses", 				[("mail_chausses_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature  ,0, 280 , weight(2.3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(19)|difficulty(0) ,imodbits_armor ],
["mail_boots", 					"Mail Boots", 					[("mail_boots_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature  ,0, 400 , weight(2.3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(21)|difficulty(0) ,imodbits_armor ],
["iron_greaves", 				"Iron Greaves", 				[("iron_greaves_a",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0, 880 , weight(2.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(26)|difficulty(0) ,imodbits_armor ],
["black_greaves", 				"Black Greaves", 				[("black_greaves",0)], itp_type_foot_armor  | itp_attach_armature,0, 2361 , weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(35)|difficulty(0) ,imodbits_armor ],
["khergit_leather_boots", 		"Khergit Leather Boots", 		[("khergit_leather_boots",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 60 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(11)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
["khergit_guard_boots",  		"Khergit Guard Boots", 			[("lamellar_boots_a",0)], itp_type_foot_armor | itp_attach_armature,0, 170 , weight(1.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(16)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
["sarranid_boots_a", 			"Sarranid Shoes", 				[("sarranid_shoes",0)], itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 20 , weight(0.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_boots_b", 			"Sarranid Leather Boots", 		[("sarranid_boots",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 150 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_boots_c", 			"Plated Boots", 				[("sarranid_camel_boots",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 1500 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_6]],
["sarranid_boots_d", 			"Sarranid Mail Boots", 			[("sarranid_mail_chausses",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 360 , weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
["brown_highlander_boots", 		"Brown Highlander Boots", 		[("b_h1",0)], itp_merchandise|itp_type_foot_armor, 0, 100, weight(3)|abundance(80)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["blue_highlander_boots", 		"Blue Highlander Boots", 		[("b_h1_1",0)], itp_merchandise|itp_type_foot_armor, 0, 100, weight(3)|abundance(80)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["brown_highlander_fur_boots", 	"Brown Highlander Fur Boots", 	[("b_h2",0)], itp_merchandise|itp_type_foot_armor, 0, 100, weight(5)|abundance(80)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["blue_highlander_fur_boots", 	"Blue Highlander Fur Boots", 	[("b_h2_1",0)], itp_merchandise|itp_type_foot_armor, 0, 100, weight(5)|abundance(80)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],

#["mail_boots_for_tableau", "Mail Boots", [("mail_boots_a",0)], itp_type_foot_armor | itp_attach_armature  ,0, 400, weight(2.3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(21)|difficulty(0) ,imodbits_armor ],
#["plate_boots", "Plate Boots", [("plate_boots",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0, 1700 , weight(3.3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0) ,imodbits_plate ],
#["sarranid_boots_brass", "Sarranid Brass Boots", [("sar_brass_boots",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 920 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
#["camel_boots_black", "Plated Brass Boots", [("camel_boots_black",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 280 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(26)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_6]],
#["mail_boots_brass", "Brass Mail Boots", [("brass_mail_boots",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature  ,0, 1250 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
#["rus_shoes", "Vaegiran Ankle Boots", [("rus_shoes",0)], itp_merchandise| itp_type_foot_armor |itp_civilian  | itp_attach_armature,0, 35 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(8)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_2]],
#["rus_cav_boots", "Vaegiran Cavalry Boots", [("rus_cav_boots",0)], itp_merchandise| itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 130 , weight(1.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_2]],
#["rus_splint_greaves", "Splinted Greaves", [("rus_splint_greaves",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0, 640 , weight(2.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_plate ],


####################
##### BODYWEAR #####
####################

########## Civilian clothes ##########

########## Common ##########
["monk_robe_a", 			"Monk Robe", 				[("monie_a",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|0, 0, 25, weight(2)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["monk_robe_b", 			"Monk Robe",				[("monie_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|0, 0, 25, weight(2)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["red_dress", 				"Red Dress", 				[("red_dress",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["brown_dress", 			"Brown Dress", 				[("brown_dress",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["green_dress", 			"Green Dress", 				[("green_dress",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["sarranid_common_dress", 	"Sarranid Dress", 			[("sarranid_common_dress",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_common_dress_b",	"Sarranid Dress", 			[("sarranid_common_dress_b",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_dress_a", 		"Dress", 					[("woolen_dress",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 33 , weight(1)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(9)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["dress", 					"Dress", 					[("dress",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) ,imodbits_cloth ],
["blue_dress", 				"Blue Dress", 				[("blue_dress_new",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) ,imodbits_cloth ],
["peasant_dress", 			"Peasant Dress", 			[("peasant_dress_b_new",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) ,imodbits_cloth ],
["woolen_dress", 			"Woolen Dress", 			[("woolen_dress",0)], itp_merchandise| itp_type_body_armor|itp_civilian  |itp_covers_legs ,0, 10 , weight(1.75)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(2)|difficulty(0) ,imodbits_cloth ],
["linen_tunic", 			"Linen Tunic", 				[("shirt_a",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],
["red_tunic", 				"Red Tunic", 				[("arena_tunicR_new",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],
["tunic_with_green_cape", 	"Tunic with Green Cape",	[("peasant_man_a",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 6 , weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0) ,imodbits_cloth ],
["green_tunic", 			"Green Tunic", 				[("arena_tunicG_new",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],
["blue_tunic", 				"Blue Tunic", 				[("arena_tunicB_new",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],
["coarse_tunic", 			"Tunic with vest", 			[("coarse_tunic_a",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 47 , weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["leather_apron", 			"Leather Apron", 			[("leather_apron",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 61 , weight(3)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["tabard", 					"Tabard", 					[("tabard_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs |itp_civilian,0, 107 , weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["sarranid_cloth_robe", 	"Worn Robe", 				[("sar_robe",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 33 , weight(1)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(9)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_cloth_robe_b", 	"Worn Robe", 				[("sar_robe_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 33 , weight(1)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(9)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],


########## Noble ##########
["lady_dress_ruby", 		"Lady Dress", 				[("lady_dress_r",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["lady_dress_green", 		"Lady Dress", 				[("lady_dress_g",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["lady_dress_blue", 		"Lady Dress", 				[("lady_dress_b",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["khergit_lady_dress", 		"Khergit Lady Dress", 		[("khergit_lady_dress",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
["khergit_lady_dress_b", 	"Khergit Lady Dress",		[("khergit_lady_dress_b",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
["sarranid_lady_dress", 	"Sarranid Lady Dress", 		[("sarranid_lady_dress",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_lady_dress_b",	"Sarranid Lady Dress", 		[("sarranid_lady_dress_b",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],

["courtly_outfit", 			"Courtly Outfit", 			[("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian   ,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["court_dress", 			"Court Dress", 				[("court_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian   ,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(4)|difficulty(0) ,imodbits_cloth ],
["rich_outfit", 			"Rich Outfit", 				[("merchant_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian   ,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(4)|difficulty(0) ,imodbits_cloth ],
["nobleman_outfit", 		"Nobleman Outfit", 			[("nobleman_outfit_b_new",0)], itp_type_body_armor|itp_covers_legs|itp_civilian   ,0, 348 , weight(4)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],

#["robe", 						"Robe", [("robe",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs |itp_civilian,0, 31 , weight(1.5)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["burlap_tunic", "Burlap Tunic", [("shirt",0)], itp_type_body_armor  |itp_covers_legs ,0, 5 , weight(1)|abundance(100)|head_armor(0)|body_armor(3)|leg_armor(1)|difficulty(0) ,imodbits_armor ],
#["shirt", "Shirt", [("shirt",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 3 , weight(1)|abundance(100)|head_armor(0)|body_armor(5)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["short_tunic", "Red Tunic", [("rich_tunic_a",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],
#["red_shirt", "Red Shirt", [("rich_tunic_a",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0) ,imodbits_cloth ],




##########################
##### WESTERN ARMOUR #####
##########################

##### WESTERN ARMOURS TIER 1 - ~ 20 BODY ARMOUR, 5 LEG ARMOUR #####
["gambeson", 		"Gambeson", 	[("white_gambeson",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian,0, 260 , weight(4)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["blue_gambeson", 	"Blue Gambeson",[("blue_gambeson",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian,0, 270 , weight(5)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["red_gambeson", 	"Red Gambeson",	[("red_gambeson_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs|itp_civilian,0, 275 , weight(6)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["short_aketon", 	"Short Aketon",	[("aketon",0)],			itp_merchandise|itp_type_body_armor|itp_civilian,0, 325 , weight(4)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(2)|difficulty(0) ,imodbits_cloth, [],],

##### TIER 2 - ~ 26 BODY ARMOUR, 7 LEG ARMOUR #####
["long_aketon", 	"Long Aketon",	[("padded_cloth_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs ,0, 270 , weight(7)|abundance(100)|head_armor(0)|body_armor(25)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["padded_cloth", 	"Padded Cloth",	[("padded_cloth_b",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs ,0, 297 , weight(8)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["padded_coat_a", 	"Padded Coat",	[("padded_shirt_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 330 , weight(9)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["padded_coat_b", 	"Padded Coat",	[("padded_shirt_b",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 330 , weight(9)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["padded_coat_c", 	"Padded Coat",	[("padded_shirt_c",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 330 , weight(9)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],

##### TIER 3 - ~ 33 BODY ARMOUR, 9 LEG ARMOUR #####
["black_gambeson_a", 		"Black Gambeson",			[("turk_bandit_a",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 400, weight(11)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["black_gambeson_b", 		"Black Gambeson", 			[("novici_hospitaller",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 400, weight(11)|abundance(100)|head_armor(0)|body_armor(33)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["swadian_gambeson",		"Swadian Gambeson",			[("novici_tripoli_armor",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 425, weight(12)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(10)|difficulty(0), imodbits_armor ],
["padded_leather_jacket",	"Padded Leather Jacket",	[("padded_leather_c",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 450, weight(13)|abundance(90)|head_armor(0)|body_armor(38)|leg_armor(4)|difficulty(0) ,imodbits_cloth ],
["leather_jerkin", 			"Leather Jerkin", 			[("ragged_leather_jerkin",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 411, weight(11)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],

##### TIER 4 - 38 BODY ARMOUR, 10 LEG ARMOUR #####
["mail_shirt",				"Mail Shirt",				[("mail_shirt_a",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 500, weight(13)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(9)|difficulty(0) ,imodbits_armor ],
["heavy_swadian_gambeson",	"Heavy Swadian Gambeson",	[("armor_infantry_tripoli_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 550, weight(16)|abundance(100)|head_armor(0)|body_armor(37)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["padded_mail_a",			"Padded Mail",				[("padded_mail_a",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs ,0, 630, weight(19)|abundance(90)|head_armor(0)|body_armor(38)|leg_armor(10)|difficulty(0) ,imodbits_armor ],
["padded_mail_b",			"Padded Mail",				[("padded_mail_b",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs ,0, 630, weight(19)|abundance(90)|head_armor(0)|body_armor(38)|leg_armor(10)|difficulty(0) ,imodbits_armor ],
["mail_hauberk",			"Mail Hauberk",				[("hauberk_a_new",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs ,0, 600, weight(16)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(12)|difficulty(0) ,imodbits_armor ],

##### TIER 5 - 44 BODY ARMOUR, 12 LEG ARMOUR #####
["light_brigantine_a",				"Light Brigandine",					[("brigandine_red",0)],				itp_merchandise|itp_type_body_armor,0, 830 , weight(20)|abundance(90)|head_armor(0)|body_armor(47)|leg_armor(9)|difficulty(0) ,imodbits_armor, [], ],
["light_brigantine_b",				"Light Brigandine",					[("brigandine_green",0)],			itp_merchandise|itp_type_body_armor,0, 830 , weight(20)|abundance(90)|head_armor(0)|body_armor(47)|leg_armor(9)|difficulty(0) ,imodbits_armor, [], ],
["light_brigantine_c",				"Light Brigandine",					[("brigandine_blue",0)],			itp_merchandise|itp_type_body_armor,0, 830 , weight(20)|abundance(90)|head_armor(0)|body_armor(47)|leg_armor(9)|difficulty(0) ,imodbits_armor, [], ],
["swadian_gambeson_with_chainmail",	"Swadian Gambeson with Chainmail",	[("sergeant_armor_tripoli_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 750, weight(21)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(11)|difficulty(0), imodbits_armor ],
["mail_with_surcoat_a",				"Mail with Surcoat",				[("mail_long_surcoat_new",0)],		itp_merchandise| itp_type_body_armor|itp_covers_legs ,0, 900 , weight(22)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(0) ,imodbits_armor ],
["mail_with_surcoat_b",				"Mail with Surcoat",				[("surcoat_over_mail_new",0)],		itp_merchandise| itp_type_body_armor|itp_covers_legs ,0, 900 , weight(22)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(0) ,imodbits_armor ],

##### TIER 6 - 49 BODY ARMOUR, 14 LEG ARMOUR #####
["heavy_brigandine_a",	"Heavy Brigandine",		[("brigandine_b",0)],				itp_merchandise|itp_type_body_armor,0, 1830, weight(26)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
["heavy_brigandine_b",	"Heavy Brigandine",		[("brigandine_red_mail",0)],		itp_merchandise|itp_type_body_armor,0, 1130, weight(24)|abundance(90)|head_armor(0)|body_armor(51)|leg_armor(11)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_5]],
["heavy_brigandine_c",	"Heavy Brigandine",		[("brigandine_green_mail",0)],		itp_merchandise|itp_type_body_armor,0, 1130, weight(24)|abundance(90)|head_armor(0)|body_armor(51)|leg_armor(11)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_5]],
["heavy_brigandine_d",	"Heavy Brigandine",		[("brigandine_blue_mail",0)],		itp_merchandise|itp_type_body_armor,0, 1130, weight(24)|abundance(90)|head_armor(0)|body_armor(51)|leg_armor(11)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_5]],
["swadian_chainmail",	"Swadian Chainmail",	[("knight_armor_tripolli_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1500, weight(26)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(13)|difficulty(0), imodbits_armor ],
["coat_of_plates",		"Coat of Plates",		[("coat_of_plates_a",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs ,0, 3828, weight(29)|abundance(80)|head_armor(0)|body_armor(52)|leg_armor(13)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_1]],
["coat_of_plates_red",	"Coat of Plates",		[("coat_of_plates_red",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs ,0, 3828, weight(29)|abundance(80)|head_armor(0)|body_armor(52)|leg_armor(13)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_1]],

##### TIER 7 - 54 BODY ARMOUR, 16 LEG ARMOUR #####
["mail_and_plate_a",	"Mail and Plate",		[("light_mail_and_plate",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3900, weight(34)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
["mail_and_plate_b",	"Mail and Plate",		[("mail_and_plate",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3900, weight(34)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
["plate_armor",			"Plate Armor",			[("full_plate_armor",0)], 			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 4253, weight(31)|abundance(60)|head_armor(0)|body_armor(52)|leg_armor(15)|difficulty(0) ,imodbits_plate ],

##### TIER 8 - 59 BODY ARMOUR, 17 LEG ARMOUR #####
["stripped_armour",		"Stripped Armour",		[("bnw_armour_slashed",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 6000, weight(37)|abundance(100)|head_armor(0)|body_armor(59)|leg_armor(16)|difficulty(0) ,imodbits_plate ],
["slashed_armour",		"Slashed Armour",		[("bnw_armour_stripes",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 6000, weight(37)|abundance(100)|head_armor(0)|body_armor(59)|leg_armor(16)|difficulty(0) ,imodbits_plate ],
["gothic_armour",		"Gothic Armour",		[("gothic_armour",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 7000, weight(40)|abundance(100)|head_armor(8)|body_armor(58)|leg_armor(17)|difficulty(0) ,imodbits_plate ],
["milanese_armour",		"Milanese Armour",		[("milanese_armour",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 8000, weight(39)|abundance(100)|head_armor(0)|body_armor(62)|leg_armor(18)|difficulty(0) ,imodbits_plate ],


#["padded_teutonic_2", "Padded Teutonic Coat", [("armor_36",0)],  itp_type_body_armor  |itp_covers_legs ,0, 620 , weight(17)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],
#["padded_teutonic_3", "Padded Teutonic Coat", [("armor_37",0)],  itp_type_body_armor  |itp_covers_legs ,0, 620 , weight(17)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],
#["padded_teutonic_4", "Padded Teutonic Coat", [("armor_38",0)],  itp_type_body_armor  |itp_covers_legs ,0, 620 , weight(17)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],
#["padded_teutonic_5", "Padded Teutonic Coat", [("armor_39",0)],  itp_type_body_armor  |itp_covers_legs ,0, 620 , weight(17)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],
#["padded_hospit_1", "Padded Hospitaller Coat", [("armor_40",0)],  itp_type_body_armor  |itp_covers_legs ,0, 620 , weight(17)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(14)|difficulty(0) ,imodbits_cloth ],
#["teutonic_surcoat_mail", "Teutonic Surcoat With Mail", [("armor_29",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(25)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(14)|difficulty(0) ,imodbits_armor ],
#["teutonic_surcoat_leather", "Teutonic Surcoat With Leather", [("armor_28",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(21)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(13)|difficulty(0) ,imodbits_cloth ],

#["padded_teutonic_surcoat", "Padded Teutonic Armor", [("armor_12",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(22)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(0) ,imodbits_cloth ],
#["padded_teutonic_coat", "Padded Teutonic Coat", [("armor_15",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(22)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(0) ,imodbits_cloth ],
#["padded_teutonic_coat2", "Padded Teutonic Coat", [("armor_16",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(22)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(0) ,imodbits_cloth ],
#["teutonic_surcoat_mail2", "Teutonic Surcoat With Mail", [("armor_30",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(25)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(0) ,imodbits_armor ],
#["teutonic_surcoat_mail3", "Teutonic Surcoat With Mail", [("armor_34",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(25)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(0) ,imodbits_armor ],
#["teutonic_chain_coat", "Teutonic Chain Coat", [("armor_43",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1120 , weight(20)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
#["teutonic_surcoat", "Teutonic Surcoat Over Mail", [("armor_10",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(22)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
#["teutonic_coat_plates", "Teutonic Coat of Plates", [("armor_35",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1220 , weight(23)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(17)|difficulty(0) ,imodbits_armor ],
#["hospit_2", "Hospitaller Coat of Plates", [("armor_44",0)],  itp_type_body_armor  |itp_covers_legs ,0, 1122 , weight(23)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
#["xbowman_leatherred", "Leather Coat", [("rich_leather_a",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 345 , weight(13)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["xbowman_leatheryellow", "Leather Coat", [("rich_leather_b",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 345 , weight(13)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
#["leather_armor3", "Leather Armor", [("armor_3",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 295 , weight(13)|abundance(100)|head_armor(0)|body_armor(25)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["leather_armor4", "Leather Armor", [("armor_5",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 295 , weight(13)|abundance(100)|head_armor(0)|body_armor(25)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["xbowman_paddedred", "Padded Coat", [("rich_padded",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 255 , weight(10)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["xbowman_paddedyellow", "Padded Coat", [("rich_padded_b",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 255 , weight(10)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["mail_with_tunic_red", "Mail with Tunic", [("arena_armorR_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(8), imodbits_armor ],
#["mail_with_tunic_green", "Mail with Tunic", [("arena_armorG_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(8), imodbits_armor ],
#["lamellar_cuirass", "Lamellar Cuirass", [("lamellar_armor",0)], itp_type_body_armor  |itp_covers_legs,0, 1020 , weight(25)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(15)|difficulty(9) ,imodbits_armor ],
#["chain_mailwhite", "Chain Mail", [("ragged_armour",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1395 , weight(19)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
#["chain_mailgreen", "Chain Mail", [("ragged_armour_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1395 , weight(19)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
#["chain_mailblue", "Chain Mail", [("ragged_armour_c",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1395 , weight(19)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
#["chain_mailred", "Chain Mail", [("ragged_armour_d",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1395 , weight(19)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
#["chain_mailyellow", "Chain Mail", [("ragged_armour_e",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1395 , weight(19)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
#["black_armor", "Black Armor", [("black_armor",0)], itp_merchandise|itp_type_body_armor  |itp_covers_legs ,0, 4296 , weight(28)|abundance(10)|head_armor(0)|body_armor(57)|leg_armor(18)|difficulty(0) ,imodbits_plate ],



########## Teutonic ##########




##### TIER 1 - ~ 20 BODY ARMOUR, 5 LEG ARMOUR #####
["rawhide_coat",		"Rawhide Coat",			[("coat_of_plates_b",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 250, weight(5)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["fur_coat",			"Fur Coat",				[("fur_coat",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 260, weight(6)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(4)|difficulty(0), imodbits_armor ],
["leather_armor",		"Leather Armor",		[("tattered_leather_armor_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 270, weight(7)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(5)|difficulty(0), imodbits_cloth ],

##### TIER 2 - ~ 26 BODY ARMOUR, 7 LEG ARMOUR #####
["pelt_coat", 				"Pelt Coat", 				[("thick_coat_a",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 350, weight(9)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["cloth_tunicstriped", 		"Cloth Striped Tunic", 		[("byrnie_a_tunic_d",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 350, weight(8)|abundance(100)|head_armor(0)|body_armor(25)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["cloth_tunicstriped2", 	"Cloth Striped Tunic", 		[("byrnie_a_tunic_e",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 350, weight(8)|abundance(100)|head_armor(0)|body_armor(25)|leg_armor(7)|difficulty(0), imodbits_cloth ],

##### TIER 3 - ~ 33 BODY ARMOUR, 9 LEG ARMOUR #####
["leather_jacket",			"Leather Jacket",			[("leather_jacket_new",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 500, weight(12)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["cloth_tunicred", 			"Cloth Tunic", 				[("byrnie_a_tunic",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 600, weight(10)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["cloth_tunicwhite", 		"Cloth Tunic", 				[("byrnie_a_tunic_b",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 600, weight(10)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["cloth_tunicgreen", 		"Cloth Tunic", 				[("byrnie_a_tunic_c",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 600, weight(10)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["light_leather",			"Light Leather",			[("light_leather",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 650, weight(11)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(7)|difficulty(0) ,imodbits_armor ],
["padded_byrniered",		"Padded Byrnie",			[("byrnie_a_padded",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 325, weight(14)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
["padded_byrniewhite",		"Padded Byrnie",			[("byrnie_a_padded_b",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 325, weight(14)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
["padded_byrniegreen",		"Padded Byrnie",			[("byrnie_a_padded_c",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 325, weight(14)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],

##### TIER 4 - 38 BODY ARMOUR, 10 LEG ARMOUR #####
["padded_leather",			"Padded Leather",			[("leather_armor_b",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 750, weight(15)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["padded_jacketwhite",		"Padded Jacket",			[("padded_jack_a",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 690, weight(14)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
["padded_jacketgreen",		"Padded Jacket",			[("padded_jack_b",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 690, weight(14)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
["byrnie",					"Byrnie",					[("byrnie_a_new",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 850, weight(16)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(8)|difficulty(0) ,imodbits_armor ],
["studded_leather_coat",	"Studded Leather Coat",		[("leather_armor_a",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 690, weight(14)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(10)|difficulty(0) ,imodbits_armor ],
["light_lamellar_armor",	"Light Lamellar Armor",		[("armor_medium_tyrk_c",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 850, weight(19)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(8)|difficulty(0), imodbits_armor ],
["light_coat_of_plates",	"Light Coat of Plates",		[("armor_medium_tyrk_d",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 750, weight(17)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(8)|difficulty(0), imodbits_armor ],

##### TIER 5 - 44 BODY ARMOUR, 12 LEG ARMOUR #####
["heavy_coat_of_plates",	"Heavy Coat of Plates",		[("lamellar_armor_d",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1000, weight(18)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(0) ,imodbits_armor ],
["heavy_chainmail_armor",	"Heavy Chianmail Armor",	[("armor_medium_tyrk_e",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1000, weight(17)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(13)|difficulty(0), imodbits_armor ],
["banded_armor",			"Banded Armor",				[("banded_armor_a",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1100, weight(21)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
["heavy_lamellar_vest_a",	"Heavy Lamellar Vest",		[("khergit_mail_b",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1200, weight(19)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(11)|difficulty(0) ,imodbits_armor ],
["heavy_lamellar_vest_b",	"Heavy Lamellar Vest",		[("khergit_mail_c",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1200, weight(19)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(11)|difficulty(0) ,imodbits_armor ],
["heavy_lamellar_vest_c",	"Heavy Lamellar Vest",		[("khergit_mail_d",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1200, weight(19)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(11)|difficulty(0) ,imodbits_armor ],
["heavy_lamellar_vest_d", 	"Heavy Lamellar Vest",		[("khergit_mail_a",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1200, weight(19)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(11)|difficulty(0) ,imodbits_armor ],
["kuyak_a",					"Kuyak",					[("kuyak_a",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1250, weight(22)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(0) ,imodbits_armor ],
["kuyak_b",					"Kuyak",					[("kuyak_b",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1250, weight(22)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(0) ,imodbits_armor ],

##### TIER 6 - 49 BODY ARMOUR, 13 LEG ARMOUR #####
["heavy_lamellar_armor_a",	"Heavy Lamellar Armor",		[("armor_medium_tyrk_b",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1750, weight(25)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(10)|difficulty(0), imodbits_armor ],
["heavy_lamellar_armor_b",	"Heavy Lamellar Armor",		[("armor_medium_tyrk_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1750, weight(25)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(10)|difficulty(0), imodbits_armor ],
["haubergeon", 				"Haubergeon", 				[("haubergeon_c",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1800 , weight(21)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(14)|difficulty(0) ,imodbits_armor ],
["lamellar_armor", 			"Lamellar Armor", 			[("lamellar_armor_b",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1450 , weight(25)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(11)|difficulty(0) ,imodbits_armor ],
["lamellar_scale_blue", 	"Lamellar Scale", 			[("arabian_mail_shirt",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1800 , weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(10)|difficulty(0) ,imodbits_armor ],
["lamellar_scale_yellow", 	"Lamellar Scale", 			[("arabian_mail_shirt_b",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1800 , weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(10)|difficulty(0) ,imodbits_armor ],
["lamellar_scale_white", 	"Lamellar Scale", 			[("arabian_mail_shirt_c",0)], 	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1800 , weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(10)|difficulty(0) ,imodbits_armor ],

##### TIER 7 - 54 BODY ARMOUR, 15 LEG ARMOUR #####
["cuir_bouilli",				"Cuir Bouilli", 			[("cuir_bouilli_a",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 2500, weight(26)|abundance(100)|head_armor(0)|body_armor(53)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
["heavvy_lamellar_chainmail",	"Heavy Lamellar Chainmail",	[("tyrk_armor_heavi_c",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3000, weight(21)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(13)|difficulty(0), imodbits_armor ],
["vaegir_elite_armor",			"Vaegiran Elite Armor", 	[("lamellar_armor_c",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3528, weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
["nordic_elite_armor",			"Nordic Elite Armor", 		[("dejawolf_vikingbyrnie",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3600, weight(18)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
["elite_lamellar_armor_a",		"Elite Lamellar Armor", 	[("Ghulam_heavy_cavalryman_1",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 4000, weight(22)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(12)|difficulty(0), imodbits_armor ],
["elite_lamellar_armor_b",		"Elite Lamellar Armor", 	[("Ghulam_heavy_cavalryman_2",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 4000, weight(22)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(11)|difficulty(0), imodbits_armor ],
["elite_lamellar_armor_c",		"Elite Lamellar Armor", 	[("Ghulam_heavy_cavalryman_3",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 4000, weight(22)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(13)|difficulty(0), imodbits_armor ],


#Remove++
#["scale_armor", "Scale Armor", [("lamellar_armor_e",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 2558 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
#["padded_byrniestriped", "Padded Byrnie", [("byrnie_a_padded_d",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 325 , weight(11)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["padded_byrniestriped2", "Padded Byrnie", [("byrnie_a_padded_e",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 325 , weight(11)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
#["viking_lamellar", "Nordic Lamellar", [("vikinglamellar1",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 825 , weight(16)|abundance(80)|head_armor(0)|body_armor(37)|leg_armor(10)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_4]],
#["viking_lamellar2", "Nordic Lamellar Blue", [("vikinglamellar_blue",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 825 , weight(16)|abundance(80)|head_armor(0)|body_armor(37)|leg_armor(10)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_4]],
#["viking_lamellar3", "Nordic Lamellar Red", [("vikinglamellar_red",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 825 , weight(16)|abundance(80)|head_armor(0)|body_armor(37)|leg_armor(10)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_4]],
#["byrnie_white", "Byrnie Chain", [("byrnie_a_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1025 , weight(18)|abundance(90)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
#["byrnie_green", "Byrnie Chain", [("byrnie_a_c",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1025, weight(18)|abundance(90)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
#["byrnie_striped", "Byrnie Chain", [("byrnie_a_d",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1025 , weight(18)|abundance(90)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
#["byrnie_striped2", "Byrnie Chain", [("byrnie_a_e",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1025 , weight(18)|abundance(90)|head_armor(0)|body_armor(45)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
#["kuyak_a", "Kuyak", [("kuyak_a",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 995 , weight(16)|abundance(70)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_2]],
#["kuyak_b", "Kuyak", [("kuyak_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 995 , weight(16)|abundance(70)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_2]],
#["rus_lamellar_a", "Vaegiran lamellar", [("rus_lamellar_a",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1295 , weight(18)|abundance(70)|head_armor(0)|body_armor(48)|leg_armor(12)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_2]],
#["rus_lamellar_b", "Vaegiran lamellar", [("rus_lamellar_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1295 , weight(18)|abundance(70)|head_armor(0)|body_armor(48)|leg_armor(12)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_2]],
#["rus_scale", "Vaegiran Scale", [("rus_scale",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1595 , weight(19)|abundance(60)|head_armor(0)|body_armor(52)|leg_armor(18)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_2]],
#Remove--




##### TIER 1 - ~ 20 BODY ARMOUR, 5 LEG ARMOUR #####
["steppe_robe_a",			"Steppe Robe",				[("khergit_vest_a",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 210 , weight(6)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["steppe_robe_b",			"Steppe Robe",				[("khergit_vest_b",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 190 , weight(6)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["steppe_robe_c",			"Steppe Robe",				[("khergit_vest_c",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 230 , weight(6)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(4)|difficulty(0) ,imodbits_cloth ],
["steppe_robe_d",			"Steppe Robe",				[("khergit_vest_d",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 250 , weight(6)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["nomad_robe",				"Nomad Robe",				[("nomad_robe_a",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 250 , weight(6)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],

##### TIER 2 - ~ 26 BODY ARMOUR, 7 LEG ARMOUR #####
["nomad_vest",				"Nomad Vest",				[("nomad_vest_new",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 360, weight(7)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(6)|difficulty(0) ,imodbits_cloth ],
["tribal_warrior_outfit",	"Tribal Warrior Outfit",	[("tribal_warrior_outfit_a_new",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 150, weight(12)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["leather_vest",			"Leather Vest",				[("leather_vest_a",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 300, weight(10)|abundance(100)|head_armor(0)|body_armor(25)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["archers_vest",			"Archer's Vest",			[("archers_vest",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 400, weight(7)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
["desert_leather_armor",	"Desert Leather Armor",		[("sarranid_leather_armor",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 300, weight(11)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(9)|difficulty(0) ,imodbits_armor ],
["sarranid_robe_a",			"Sarranid Robe",			[("arab_bandit_a",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 250, weight(10)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["sarranid_robe_d",			"Sarranid Robe",			[("arab_bandit_d",0)],					itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 250, weight(10)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(7)|difficulty(0), imodbits_cloth ],

##### TIER 3 - ~ 33 BODY ARMOUR, 9 LEG ARMOUR #####
["steppe_armor",				"Steppe Armor", 			[("lamellar_leather",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 450, weight(13)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(7)|difficulty(0) ,imodbits_cloth ],
["desert_robe_with_leatther_a",	"Desert Robe with Leather", [("arab_bandit_b",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 690, weight(15)|abundance(100)|head_armor(0)|body_armor(33)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["desert_robe_with_leather_b",	"Desert Robe with Leather", [("arab_bandit_c",0)], 				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 690, weight(15)|abundance(100)|head_armor(0)|body_armor(33)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["cavalry_robe",				"Cavalry Robe",				[("arabian_armor_a",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 900, weight(15)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(8)|difficulty(0) ,imodbits_armor ],
["steppe_leather_armor_a",		"Steppe Leather Armor",		[("turk_bandit_c",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 600, weight(15)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(8)|difficulty(0), imodbits_armor ],
["steppe_leather_armor_b",		"Steppe Leather Armor",		[("turk_bandit_d",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 600, weight(14)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(9)|difficulty(0), imodbits_armor ],
["desert_padded_coat_a",		"Desert Padded Coat",		[("armor_archer_saracin_2",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 450, weight(13)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["desert_padded_coat_b",		"Desert Padded Coat",		[("armor_archer_saracin_3",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 450, weight(13)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(7)|difficulty(0), imodbits_cloth ],

##### TIER 4 - 38 BODY ARMOUR, 10 LEG ARMOUR #####
["desert_mail_shirt",			"Desert Mail Shirt",				[("sarranian_mail_shirt",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 800, weight(17)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(11)|difficulty(0) ,imodbits_armor ],
["desert_chainmail",			"Desert Chainmail",					[("armor_archer_saracin_1",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 750, weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(10)|difficulty(0), imodbits_armor ],
["desert_lamellar_armor_a",		"Desert Lamellar Armor",			[("heavy_armor_arabs_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 950, weight(18)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(9)|difficulty(0), imodbits_armor ],
["desert_lamellar_armor_b",		"Desert Lamellar Armor",			[("heavy_armor_arabs_c_1",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 950, weight(19)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(9)|difficulty(0), imodbits_armor ],
["desert_lamellar_armor_c",		"Desert Lamellar Armor",			[("heavy_armor_arabs_c",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 999, weight(23)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(11)|difficulty(0), imodbits_armor ],
["steppe_lamellar_vest_a",		"Steppe Lamellar Vest",				[("lamellar_vest_b",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 970, weight(19)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["steppe_lamellar_vest_b",		"Steppe Lamellar Vest",				[("lamellar_vest_a",0)], 		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 970, weight(19)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["steppe_chainmail",			"Steppe Chainmail",					[("turk_bandit_b",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 900, weight(19)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(10)|difficulty(0), imodbits_armor ],

##### TIER 5 - 44 BODY ARMOUR, 12 LEG ARMOUR #####
#khergit heavy chainmail armor, khergit lamellar chainmail, mamluke mail, ##### TIER 5 - 44 BODY ARMOUR, 12 LEG ARMOUR #####
["heavy_steppe_chainmail_armor",	"Heavy Steppe Chianmail Armor",		[("armor_medium_tyrk_f",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1100, weight(24)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(12)|difficulty(0), imodbits_armor ],
["heavy_steppe_lamellar_armor",		"Heavy Steppe Lamellar Chainmail", 	[("tyrk_armor_heavi_b",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1200, weight(23)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(0), imodbits_armor ],
["heavy_desert_chainmail_armor",	"Heavy Desert Chainmail Armor",		[("tyrk_armor_heavi_a",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1300, weight(24)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(13)|difficulty(0) ,imodbits_armor ],

##### TIER 6 - 49 BODY ARMOUR, 14 LEG ARMOUR #####
["heavy_desert_lamellar_armor",	"Heavy Desert Lamellar Armor",		[("heavy_armor_arabs_b",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 2500, weight(26)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(14)|difficulty(0), imodbits_cloth ],
["heavy_lamellar_armor",		"Heavy Lamellar Armor",				[("heavy_lamellar_armor",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3000, weight(27)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
["elite_steppe_armor",			"Elite Steppe Armor",				[("lamellar_armor_a",0)],		itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3500, weight(25)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
["steppe_nobleman_armor", 		"Steppe Nobleman Armor",			[("tunic_armor_a",0)],			itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3250, weight(25)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(14)|difficulty(0) ,imodbits_armor ],

##### TIER 7 - 54 BODY ARMOUR, 16 LEG ARMOUR #####
["elite_desert_armor",			"Sarranid Elite Armor",				[("saladin",0)],				itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 4000, weight(28)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(15)|difficulty(0) ,imodbits_armor ],
["desert_nobleman_armor",		"Sarranid Sultan Armor",			[("armor_Sultan_saracens",0)],	itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 4500, weight(29)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(16)|difficulty(0), imodbits_armor ],

#remove++
#["khergit_leatherwhite", "Khergit Leather Armor", [("khergit_leather_e",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 405 , weight(14)|abundance(80)|head_armor(0)|body_armor(28)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
#["khergit_leatherred", "Khergit Leather Armor", [("khergit_leather_f",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 405 , weight(14)|abundance(80)|head_armor(0)|body_armor(28)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
#["khergit_leatherblue", "Khergit Leather Armor", [("khergit_leather_g",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 405 , weight(14)|abundance(80)|head_armor(0)|body_armor(28)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
#["khergit_leatherpattern", "Khergit Leather Armor", [("khergit_leather_h",0)], itp_merchandise| itp_type_body_armor|itp_covers_legs,0, 405 , weight(14)|abundance(80)|head_armor(0)|body_armor(28)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
#["skirmisher_armor", "Skirmisher Armor", [("skirmisher_armor",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 74 , weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
#["ragged_outfit", "Ragged Outfit", [("ragged_outfit_a_new",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 390 , weight(7)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(9)|difficulty(0) ,imodbits_cloth ],
#["nomad_armor", "Nomad Armor", [("nomad_armor_new",0)], itp_merchandise| itp_type_body_armor |itp_covers_legs   ,0, 25 , weight(2)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
#["khergit_armor", "Khergit Armor", [("khergit_armor_new",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs ,0, 38 , weight(2)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
#["mongol_scalewhite", "Khergit Scale", [("khergit_scale_a",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1295 , weight(20)|abundance(70)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_3]],
#["mongol_scalered", "Khergit Scale", [("khergit_scale_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1295 , weight(20)|abundance(70)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_3]],
#["mongol_scaleblue", "Khergit Scale", [("khergit_scale_c",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1295 , weight(20)|abundance(70)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_3]],
#["mongol_scalepattern", "Khergit Scale", [("khergit_scale_d",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1295, weight(20)|abundance(70)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_3]],
#["scale_armor_royal", "Royal Scale Armor", [("royal_scale_armor",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 2858 , weight(25)|abundance(100)|head_armor(0)|body_armor(53)|leg_armor(16)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
#["brass_mamluke_mail", "Royal Mamluke Mail", [("brass_mamluk_armor",0)], itp_merchandise| itp_type_body_armor |itp_covers_legs|itp_civilian  ,0, 2900 , weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
#["sarranid_studded_leather", "Studded Leather Coat", [("sarranid_studded_leather",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 690 , weight(14)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(10)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
#["arabian_armor_b", "Sarranid Guard Armor", [("arabian_armor_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1200 , weight(19)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(8)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
#["sarranid_gambeson", "Sarranid Gambeson", [("arabian_light_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 450, weight(12)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(9)|difficulty(0), imodbits_cloth ],
#["lamellar_vest", "Lamellar Vest", [("lamellar_vest_a",0)], itp_merchandise| itp_type_body_armor |itp_civilian |itp_covers_legs ,0, 970 , weight(18)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
#["khergit_chainmail_armor", "Khergit Chianmail Armor", [("armor_medium_tyrk_e",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(14)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(10)|difficulty(0), imodbits_armor ],
#["khergit_full_chainmail", "Khergit Full Chainmail", [("tyrk_armor_heavi_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(18)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(11)|difficulty(0), imodbits_armor ],
#["khergit_lamellar_vest_with_chainmail_armor", "Khergit Lamellar Vesr with Chainmail Armor", [("armor_medium_tyrk_e",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 950, weight(20)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(10)|difficulty(0), imodbits_armor ],
#["lamellar_armor_f", "Lamellar Armor", [("lamellar_armor_f",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 2410 , weight(25)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(12)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
#remove--


########## Heraldic ##########

["heraldic_mail_with_surcoat", "Heraldic Mail with Surcoat", [("heraldic_armor_new_a",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 3454 , weight(22)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(17)|difficulty(0) ,imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_a", ":agent_no", ":troop_no")])]],
["heraldic_mail_with_tunic", "Heraldic Mail", [("heraldic_armor_new_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 3520 , weight(22)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(16)|difficulty(0) ,imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_b", ":agent_no", ":troop_no")])]],
["heraldic_mail_with_tunic_b", "Heraldic Mail", [("heraldic_armor_new_c",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 3610 , weight(22)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(16)|difficulty(0) ,imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_c", ":agent_no", ":troop_no")])]],
["heraldic_mail_with_tabard", "Heraldic Mail with Tabard", [("heraldic_armor_new_d",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 3654 , weight(21)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(15)|difficulty(0) ,imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_d", ":agent_no", ":troop_no")])]],
["heraldic_mail_with_surcoat_for_tableau", "{!}Heraldic Mail with Surcoat", [("heraldic_armor_new_a",0)], itp_type_body_armor |itp_covers_legs ,0, 3500, weight(22)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(15),imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_a", ":agent_no", ":troop_no")])]],
["plate_heraldic", "Heraldic Heavy Mail and Plate", [("plate_heraldic",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0,2430,weight(21)|abundance(50)|head_armor(0)|body_armor(51)|leg_armor(20)|difficulty(0),imodbits_plate,[(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_plate", ":agent_no", ":troop_no")])],[fac_player_faction]],
["heraldic_tabard", "Heraldic Tabard", [("tabard_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs |itp_civilian,0, 100, weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0) ,imodbits_cloth, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_tabard", ":agent_no", ":troop_no")])]],
["heraldic_cuir_bouilli", "Heraldic Cuir Bouilli", [("cuir_bouilli_a",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 1200, weight(24)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_cuir_bouilli", ":agent_no", ":troop_no")])]],
["heraldic_cuir_bouilli_starter", "Heraldic Cuir Bouilli", [("cuir_bouilli_a",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 750, weight(24)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0) ,imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_cuir_bouilli", ":agent_no", ":troop_no")])]],
["heraldic_padded_cloth", "Heraldic Padded Cloth", [("padded_cloth_b",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 250, weight(11)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(6)|difficulty(0) ,imodbits_cloth, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_padded_cloth", ":agent_no", ":troop_no")])]],
["heraldic_mail_and_plate", "Heraldic Mail and Plate", [("mail_and_plate",0)], itp_type_body_armor|itp_covers_legs   ,0, 3500, weight(16)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(16)|difficulty(0) ,imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_mail_and_plate", ":agent_no", ":troop_no")])]],
["heraldic_light_mail_and_plate", "Heraldic Light Mail and Plate", [("light_mail_and_plate",0)], itp_type_body_armor|itp_covers_legs   ,0, 2500, weight(10)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0) ,imodbits_armor, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_light_mail_and_plate", ":agent_no", ":troop_no")])]],
["heraldic_fur_coat", "Heraldic Fur Coat", [("fur_heraldic",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 654, weight(12)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(9)|difficulty(0), imodbits_cloth, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_fur_coat", ":agent_no", ":troop_no")])]],


########## Mercenary ########## 

["white_highlander_shirt", 			"White Highlander Shirt", 			[("a_h1",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 55, weight(7)|abundance(80)|head_armor(0)|body_armor(12)|leg_armor(2)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["blue_highlander_shirt", 			"Blue Highlander Shirt", 			[("a_h1_1",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 55, weight(7)|abundance(80)|head_armor(0)|body_armor(12)|leg_armor(2)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["brown_highlander_vest", 			"Brown Highlander Vest", 			[("a_h4",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 100, weight(12)|abundance(80)|head_armor(0)|body_armor(18)|leg_armor(3)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["blue_highlander_vest", 			"Blue Highlander Vest", 			[("a_h4_1",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 100, weight(12)|abundance(80)|head_armor(0)|body_armor(18)|leg_armor(3)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["white_highlander_coat", 			"White Highlander Coat", 			[("a_h3",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 250, weight(17)|abundance(80)|head_armor(0)|body_armor(30)|leg_armor(6)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["black_highlander_coat", 			"Black Highlander Coat", 			[("a_h3_1",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 250, weight(17)|abundance(80)|head_armor(0)|body_armor(30)|leg_armor(6)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["brown_highlander_armour", 		"Brown Highlander Armour", 			[("a_h2",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 350, weight(22)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(8)|difficulty(0), imodbits_armor, [], [fac_kingdom_5]],
["yellow_highlander_armour", 		"Yellow Highlander Armour", 		[("a_h2_1",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs,0, 350, weight(22)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(8)|difficulty(0), imodbits_armor, [], [fac_kingdom_5]],


["blue_company_gambeson", "Blue Company Gambeson", [("novici_antioh_armor",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 250, weight(8)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["blue_company_jack", "Blue Company Jack", [("armor_infantry_antioh_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 350, weight(14)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["blue_company_chainmail", "Blue Company Chainmail", [("sergeant_armor_antioh_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 500, weight(19)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(11)|difficulty(0), imodbits_armor ],
["blue_company_hauberk", "Blue Company Hauberk", [("knight_armor_antioh_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(19)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(0), imodbits_armor ],

["caravan_master_robe", "Caravan Master Robe", [("caravan_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 150, weight(4)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["caravan_guard_robe_t1", "Caravan Guard Robe", [("beduin_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 250, weight(7)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["caravan_guard_robe_t2", "Caravan Guard Robe", [("beduin_armor_c",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 300, weight(8)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["caravan_guard_robe_t3", "Caravan Guard Robe", [("beduin_armor_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(12)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(11)|difficulty(0), imodbits_cloth ],

["hospitaller_gambeson", "Hospitaller Gambeson", [("sergeant_hospitaller_armor_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 450, weight(15)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["hospitaller_chainmail", "Hospitaller Chainmail", [("knight_armor_hospitaller_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(21)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(0), imodbits_armor ],
["grandmaster_chainmail", "Grandmaster Chainmail", [("armor_king_Jerusalem",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1000, weight(24)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(14)|difficulty(0), imodbits_armor ],
["noivce_gambeson", "Novice Gambeson", [("novici_Jerusalem",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 250, weight(8)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["sargeant_gambeson", "Sargeant Gambeson", [("sergeant_Jerusalem_armor",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 450, weight(13)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["caravan_guard_cloak_a", "Caravan Guard Cloak", [("securiti_caravan_cloak_crusader",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 350, weight(10)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["caravan_guard_cloak_b", "Caravan Guard Cloak", [("securiti_caravan_crusader",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 350, weight(10)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(8)|difficulty(0), imodbits_cloth ],

["black_cuirass", "Black Cuirass", [("cuirassier1",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1500, weight(20)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(12)|difficulty(0), imodbits_armor|imodbits_plate ],
["white_cuirass", "White Cuirass", [("cuirassier2",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1500, weight(20)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(12)|difficulty(0), imodbits_armor|imodbits_plate ],
["black_milanese_cuirass", "Black Milanese Cuirass", [("cuirassier3",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1500, weight(21)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(14)|difficulty(0), imodbits_armor|imodbits_plate ],
["white_milanese_cuirass", "White Milanese Cuirass", [("cuirassier4",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1500, weight(21)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(14)|difficulty(0), imodbits_armor|imodbits_plate ],


########## Bandit ##########

["bandit_tunic", "Bandit Tunic", [("dethertir_armor_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 150, weight(5)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["bandit_gambeson_t1", "Bandit Gambeson", [("dethertir_armor_f",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 250, weight(10)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["bandit_gambeson_t2", "Bandit Gambeson", [("dethertir_armor_c",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 350, weight(12)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["bandit_chainmail", "Bandit Chainmail", [("dethertir_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 450, weight(15)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(9)|difficulty(0), imodbits_armor ],


####################
##### HEADWEAR #####
####################

########## Civilian ##########

["khergit_lady_hat",		"Khergit Lady Hat", [("khergit_lady_hat",0)],  itp_type_head_armor   |itp_civilian |itp_doesnt_cover_hair | itp_fit_to_head,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
["khergit_lady_hat_b",		"Khergit Lady Leather Hat", [("khergit_lady_hat_b",0)], itp_type_head_armor  | itp_doesnt_cover_hair | itp_fit_to_head  |itp_civilian ,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
["sarranid_head_cloth",		"Lady Head Cloth", [("tulbent",0)],  itp_type_head_armor | itp_doesnt_cover_hair |itp_civilian |itp_attach_armature,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_head_cloth_b",	"Lady Head Cloth", [("tulbent_b",0)],  itp_type_head_armor | itp_doesnt_cover_hair |itp_civilian |itp_attach_armature,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["turret_hat_ruby",			"Turret Hat", [("turret_hat_r",0)], itp_type_head_armor  |itp_civilian|itp_fit_to_head ,0, 70 , weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["turret_hat_blue", 		"Turret Hat", [("turret_hat_b",0)], itp_type_head_armor  |itp_civilian|itp_fit_to_head ,0, 80 , weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["turret_hat_green",		 "Barbette", [("barbette_new",0)],itp_merchandise|itp_type_head_armor|itp_civilian|itp_fit_to_head,0,70, weight(0.5)|abundance(100)|head_armor(6)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
["head_wrappings",			"Head Wrapping",[("head_wrapping",0)],itp_type_head_armor|itp_fit_to_head,0,16, weight(0.25)|head_armor(3),imodbit_tattered | imodbit_ragged | imodbit_sturdy | imodbit_thick],
["court_hat", 				"Turret Hat", [("court_hat",0)], itp_type_head_armor  |itp_civilian|itp_fit_to_head ,0, 80 , weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["wimple_a", 				"Wimple", [("wimple_a_new",0)],itp_merchandise|itp_type_head_armor|itp_civilian|itp_fit_to_head,0,10, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
["wimple_with_veil", 		"Wimple with Veil", [("wimple_b_new",0)],itp_merchandise|itp_type_head_armor|itp_civilian|itp_fit_to_head,0,10, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
["female_hood", 			"Lady's Hood", [("ladys_hood_new",0)], itp_merchandise| itp_type_head_armor |itp_civilian  ,0, 9 , weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

["sarranid_felt_hat",			"Sarranid Felt Hat", [("sar_helmet3",0)], itp_merchandise| itp_type_head_armor   ,0, 16 , weight(2)|abundance(100)|head_armor(5)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_felt_head_cloth",	"Head Cloth", [("common_tulbent",0)],  itp_type_head_armor  |itp_civilian |itp_attach_armature,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],
["sarranid_felt_head_cloth_b",	"Head Cloth", [("common_tulbent_b",0)],  itp_type_head_armor  |itp_civilian |itp_attach_armature,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_6]],

["straw_hat", 			"Straw Hat", [("straw_hat_new",0)],itp_merchandise|itp_type_head_armor|itp_civilian,0,9, weight(1)|abundance(100)|head_armor(2)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
["common_hood", 		"Hood", [("hood_new",0)],itp_merchandise|itp_type_head_armor|itp_civilian,0,9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
["headcloth", 			"Headcloth", [("headcloth_a_new",0)], itp_merchandise| itp_type_head_armor  |itp_civilian ,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["woolen_hood", 		"Woolen Hood", [("woolen_hood",0)], itp_merchandise| itp_type_head_armor |itp_civilian  ,0, 4 , weight(1)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["black_hood", 			"Black Hood", [("hood_black",0)], itp_type_head_armor|itp_merchandise   ,0, 193 , weight(2)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["straw_hat_a", 		"Straw Hat", [("strawhat1",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 12, weight(0.2)|abundance(100)|head_armor(9)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["straw_hat_b",			"Straw Hat", [("strawhat2",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 12, weight(0.2)|abundance(100)|head_armor(9)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["brown_hat", 			"Brown Hat", [("officerhatbrown",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 50, weight(0.2)|abundance(100)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],


#tier breakdown: 59, 52, 45, 38, 31, 24, 17, 10
##### TIER 1 - 10 ARMOR #####
["arming_cap_a",		"Arming Cap",		[("arming_cap_a_new",0)],	itp_merchandise|itp_type_head_armor, 0, 50, weight(1)|abundance(100)|head_armor(9)|body_armor(0)|leg_armor(0)|difficulty(0) , imodbits_cloth ],
["arming_cap_b", 		"Arming Cap",		[("arming_cap_new",0)],		itp_merchandise|itp_type_head_armor, 0, 75, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["felt_hat",			"Felt Hat",			[("felt_hat_b_new",0)],		itp_merchandise|itp_type_head_armor, 0, 80, weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["hood_a", 				"Hood",				[("hood_new_b",0)],			itp_merchandise|itp_type_head_armor, 0, 58, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["hood_b", 				"Hood",				[("hood_new_c",0)],			itp_merchandise|itp_type_head_armor, 0, 59, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

##### TIER 2 - 17 ARMOR #####
["padded_coif",			"Padded Coif",		[("padded_coif_a_new",0)],	itp_merchandise|itp_type_head_armor, 0, 110, weight(1.25)|abundance(100)|head_armor(17)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["leather_cap",			"Leather Cap",		[("leather_cap_a_new",0)],	itp_merchandise|itp_type_head_armor, 0, 95, weight(1.25)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

##### TIER 3 - 24 ARMOR #####
["mail_coif",			"Mail Coif",		[("mail_coif_new",0)],		itp_merchandise|itp_type_head_armor, 0, 250, weight(1.5)|abundance(100)|head_armor(23)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_armor ],
["chainmail_coif",		"Chainmail Coif",	[("crusader_koif_a",0)],	itp_merchandise|itp_type_head_armor, 0, 275, weight(1.8)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["coif",				"Coif",				[("coif",0)],				itp_merchandise|itp_type_head_armor, 0, 290, weight(2)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, ],

##### TIER 4 - 31 ARMOR #####
["simple_iberian_helmet",	"Simple Iberian Helmet",	[("simple_iberian_helmet",0)],	itp_merchandise|itp_type_head_armor, 0, 400, weight(2.5)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
["kettle_helm_a",			"Kettle Helm",				[("kettlehat",0)],				itp_merchandise|itp_type_head_armor, 0, 415, weight(2.2)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["carlingian_helm",			"Carlolingian Helm",		[("carolingian_helmet_b",0)],	itp_merchandise|itp_type_head_armor, 0, 450, weight(2.4)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["chapel_de_fer_a",			"Chapel-de-Fer",			[("chapel-de-fer_cloth1",0),("inv_chapel-de-fer_cloth1",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0, 600, weight(2.6)|abundance(80)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],

##### TIER 5 - 38 ARMOR #####
["flat_top_helmet",				"Flat Top Helmet",			[("crusader_helm_7",0)],		itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 550, weight(3.2)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["kettle_helm_b",				"Kettle Hat",				[("kettle_hat_new",0)],			itp_merchandise|itp_type_head_armor,					0, 700, weight(3.3)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["capelina_with_chainmail",		"Capelina with Chainmail",	[("capelina_crusader_a",0)],	itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 700, weight(3.1)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["norman_helmet_with_coif_a",	"Norman Helmet with Coif",	[("crusader_helm_6",0)],		itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 650, weight(3.1)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["bascinet", 					"Bascinet",					[("bascinet_avt_new",0)],		itp_merchandise|itp_type_head_armor,					0, 600, weight(2.9)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["open_sallet",					"Open Sallet",				[("open_salet",0)],				itp_merchandise|itp_type_head_armor,					0, 600, weight(2.9)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],

##### TIER 6 - 45 ARMOR #####
["chapel_de_fer_b",				"Chapel-de-Fer",			[("chapel-de-fer",0)],			itp_merchandise|itp_type_head_armor, 0, 825, weight(3.5)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["high_helmet",					"High Helmet",				[("high_helmet",0)],			itp_merchandise|itp_type_head_armor, 0, 950, weight(3.6)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["combed_morion",				"Combed Morion",			[("combed_morion",0)],			itp_merchandise|itp_type_head_armor, 0, 715, weight(3.4)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_plate ],
["blued_combed_morion",			"Blued Combed Morion",		[("combed_morion_blued",0)],	itp_merchandise|itp_type_head_armor, 0, 850, weight(3.5)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_plate ],
["big_nasal_helmet",			"Big Nasal Helmet",			[("big_nasal_helmet",0)],		itp_merchandise|itp_type_head_armor, 0, 950, weight(3.9)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["nasal_cap",					"Nasal Cap",				[("andalusian_helmet_c",0)],	itp_merchandise|itp_type_head_armor, 0, 900, weight(3.5)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["guard_helmet",				"Guard Helmet",				[("reinf_helmet_new",0)],		itp_merchandise|itp_type_head_armor, 0, 725, weight(3.3)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_plate ],
["open_sallet_with_coif", 		"Open Sallet with Coif", 	[("open_salet_coif",0)], 		itp_merchandise|itp_type_head_armor, 0, 950, weight(3.1)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],

##### TIER 7 - 52 ARMOR #####
["norman_helmet_with_coif_b",		"Norman Helmet with Coif",		[("crusader_helm_2",0)],			itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 1500, weight(3.9)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["marching_helmet",					"Marching Helmet",				[("marching_helmet_crusader_a",0)],	itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 1750, weight(4.1)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["flat_top_pepperpot_a",			"Flat Top Pepperpot",			[("crusader_knight_helm_d",0)],		itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 1325, weight(3.8)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["flat_top_pepperpot_b",			"Flat Top Pepperpot",			[("crusader_knight_helm_f",0)],		itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 1450, weight(3.8)|abundance(100)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["visored_sallet",					"Visored Sallet",				[("visored_salet",0)],				itp_merchandise| itp_type_head_armor,					0, 2475 , weight(3.7)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["chapel_de_fer_c",					"Chapel-de-Fer",				[("chapel-de-fer_mail1",0), ("inv_chapel-de-fer_mail1",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 1925 , weight(4.2)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["chapel_de_fer_d",					"Chapel-de-Fer",				[("chapel-de-fer_mail2",0), ("inv_chapel-de-fer_mail2",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 2215 , weight(4.2)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],

##### TIER 8 - 59 ARMOR #####
["full_helm",						"Full Helm",						[("great_helmet_new_b",0)],			itp_merchandise|itp_type_head_armor|itp_covers_head,					0, 5500, weight(5.1)|abundance(100)|head_armor(58)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["visored_sallet_with_coif",		"Visored Sallet with Coif",			[("visored_salet_coif",0)],			itp_merchandise|itp_type_head_armor,									0, 8000, weight(3.9)|abundance(100)|head_armor(58)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["armet",							"Armet", 							[("armet2",0)],						itp_merchandise|itp_type_head_armor|itp_fit_to_head,					0, 4000, weight(4.3)|abundance(100)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["norman_helmet_with_faceplate",	"Norman Helmet with Faceplate",		[("crusader_hard_helm_b",0)],		itp_merchandise|itp_type_head_armor|itp_fit_to_head,					0, 5750, weight(4.4)|abundance(100)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["white_sturmhaube_a", 				"White Sturmhaube", 				[("sturmhaube_7",0)],				itp_merchandise|itp_type_head_armor,									0, 6500, weight(4.5)|abundance(100)|head_armor(58)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
["white_sturmhaube_b", 				"White Sturmhaube", 				[("sturmhaube_5",0)],				itp_merchandise|itp_type_head_armor,									0, 6500, weight(4.1)|abundance(100)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
["bascinet_with_visor",				"Bascinet with Visor",				[("zitta_bascinet",0)],				itp_merchandise|itp_type_head_armor|itp_fit_to_head|itp_attach_armature,0, 9250, weight(5.5)|abundance(100)|head_armor(59)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],



##rm++
#["hood_b", 				"Hood", [("hood_b",0)],itp_merchandise|itp_type_head_armor|itp_civilian,0,9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
#["hood_c", 				"Hood", [("hood_c",0)],itp_merchandise|itp_type_head_armor|itp_civilian,0,9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
#["hood_d", 				"Hood", [("hood_d",0)],itp_merchandise|itp_type_head_armor|itp_civilian,0,9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
#["flat_topped_helmet", "Flat Topped Helmet", [("flattop_helmet_new",0)], itp_merchandise| itp_type_head_armor   ,0, 203 , weight(1.75)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["crusader_helmet", "Crusader Helmet", [("helmet_cross",0)], itp_merchandise|itp_type_head_armor, 0, 300, weight(2.75)|abundance(80)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["arming_helm", "Arming Helm", [("cervelliere",0)], itp_type_head_armor   ,0, 324 , weight(2)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["gilded_nasal_helmet", "Gilded Nasal Helmet", [("gilded_nasal_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 350, weight(3)|abundance(80)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["southern_cerveliere", "Southern Cerveliere", [("southern_cerveliere",0)], itp_merchandise|itp_type_head_armor, 0, 350, weight(3)|abundance(80)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["iberian_helmet", "Iberian Helmet", [("iberian_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 500, weight(3.25)|abundance(80)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["blue_iberian_helmet", "Blue berian Helmet", [("iberian_helmet_blue",0)], itp_merchandise|itp_type_head_armor, 0, 500, weight(3.25)|abundance(80)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["red_iberian_helmet", "Mailed Red Cap", [("iberian_helmet_red",0)], itp_merchandise|itp_type_head_armor, 0, 500, weight(3.25)|abundance(80)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["flat_top_fracia_helmet", "Flat Top Fracia Helmet", [("fracia_helmet_2",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 750, weight(3.5)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["bascinet_4", "Bascinet", [("zitta_bascinet_novisor",0)], itp_merchandise|itp_type_head_armor|itp_fit_to_head|itp_attach_armature, 0, 900, weight(3.5)|abundance(80)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["bascinet_2", "Bascinet with Aventail", [("bascinet_new_a",0)], itp_merchandise|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["bascinet_3", "Bascinet with Nose Guard", [("bascinet_new_b",0)], itp_merchandise|itp_type_head_armor   ,0, 479 , weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["chapel_de_fer_cloth2", "Chapel-de-Fer", [("chapel-de-fer_cloth2",0), ("inv_chapel-de-fer_cloth2",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 975 , weight(2.15)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_5]],
#["chapel_de_fer_cloth3", "Chapel-de-Fer", [("chapel-de-fer_cloth3",0), ("inv_chapel-de-fer_cloth3",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 995 , weight(2.15)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_5]],
#["crowned_helm", "Crowned Helm", [("crownedhelm",0)], itp_merchandise | itp_type_head_armor,0, 1754 , weight(2.2)|abundance(50)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["chapel_de_fer_mail3", "Chapel-de-Fer", [("chapel-de-fer_mail3",0), ("inv_chapel-de-fer_mail3",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 1225 , weight(2.75)|abundance(70)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_5]],
#["fluted_helmet", "Fluted Helmet", [("fluted_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 650, weight(3.25)|abundance(80)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_1]],
#["black_helmet", "Black Helmet", [("black_helm",0)], itp_type_head_armor,0, 638 , weight(2.75)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["mediterranean_helmet", "Mediterranean Helmet", [("mediterranean_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 700, weight(3.5)|abundance(80)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_1]],
#["red_phrygian_helmet", "Red Phrygian Helmet", [("red_phrygian_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.5)|abundance(80)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_1]],
#["iberian_phrygian_helmet", "Iberian Phrygian Helmet", [("iberian_phrygian_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.5)|abundance(80)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_1]],
#["pepperpot_helm1", "Pepperpot Helm", [("pepperpothelm1",0)], itp_merchandise | itp_type_head_armor,0, 914 , weight(2.3)|abundance(80)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["gilded_phrygian_helmet", "Gilded Phrygian Helmet", [("gilded_phrygian_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_1]],
#["gilded_nasal_helmet_2", "Gilded Nasal Helmet", [("gilded_nasal_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_1]],
#["andalusian_helmet_a", "Gilded Cap", [("andalusian_helmet_a",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_1]],
#["pepperpot_helmet_a", "Pepperpot Helmet", [("crusader_hard_helm_c",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 900, weight(3.8)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["andalusian_helmet_b", "Gilded Cap", [("andalusian_helmet_b",0)], itp_merchandise|itp_type_head_armor, 0, 1250, weight(3.5)|abundance(80)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_1]],
#["great_helmet", "Great Helmet", [("great_helmet_new",0)], itp_merchandise| itp_type_head_armor|itp_covers_head,0, 980 , weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["red_andalusian_helmet", "Red-Banded Nasal Helmet", [("andalusian_helmet_d",0)], itp_merchandise|itp_type_head_armor, 0, 1250, weight(3.5)|abundance(80)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_6]],
#["yellow_andalusian_helmet", "Yellow-Banded Nasal Helmet", [("andalusian_helmet_e",0)], itp_merchandise|itp_type_head_armor, 0, 1250, weight(3.5)|abundance(80)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_6]],
#["winged_great_helmet", "Winged Great Helmet", [("maciejowski_helmet_new",0)], itp_merchandise|itp_type_head_armor|itp_covers_head,0, 1240 , weight(2.75)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["norman_pepperpot", "Pepperpot", [("normanpepperpot",0)], itp_merchandise | itp_type_head_armor,0, 954 , weight(2.6)|abundance(90)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_4]],
#["white_sturmhaube_g", 				"White Sturmhaube", 				[("sturmhaube_1",0)], itp_merchandise|itp_type_head_armor, 0, 500, weight(3)|abundance(80)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["white_sturmhaube_h", 				"White Sturmhaube", 				[("sturmhaube_2",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["white_sturmhaube_c", 				"White Sturmhaube", 				[("sturmhaube_3",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["white_sturmhaube_d", 				"White Sturmhaube", 				[("sturmhaube_4",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["white_sturmhaube_f", 				"White Sturmhaube", 				[("sturmhaube_6",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_sturmhaube_a", 				"Black Sturmhaube", 				[("sturmhaube_1B",0)], itp_merchandise|itp_type_head_armor, 0, 500, weight(3)|abundance(80)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_sturmhaube_b", 				"Black Sturmhaube", 				[("sturmhaube_2B",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_sturmhaube_c", 				"Black Sturmhaube", 				[("sturmhaube_3B",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_sturmhaube_d", 				"Black Sturmhaube", 				[("sturmhaube_4B",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_sturmhaube_e", 				"Black Sturmhaube", 				[("sturmhaube_5B",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_sturmhaube_f", 				"Black Sturmhaube", 				[("sturmhaube_6B",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_sturmhaube_g", 				"Black Sturmhaube", 				[("sturmhaube_7B",0)], itp_merchandise|itp_type_head_armor, 0, 1250, weight(3.5)|abundance(80)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_white_sturmhaube_a", 		"Black-White Sturmhaube", 			[("sturmhaube_1BW",0)], itp_merchandise|itp_type_head_armor, 0, 500, weight(3)|abundance(80)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_white_sturmhaube_b", 		"Black-White Sturmhaube", 			[("sturmhaube_2BW",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_white_sturmhaube_c", 		"Black-White Sturmhaube", 			[("sturmhaube_3BW",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_white_sturmhaube_d", 		"Black-White Sturmhaube", 			[("sturmhaube_4BW",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.25)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_white_sturmhaube_e", 		"Black-White Sturmhaube", 			[("sturmhaube_5BW",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_white_sturmhaube_f", 		"Black-White Sturmhaube", 			[("sturmhaube_6BW",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["black_white_sturmhaube_g", 		"Black-White Sturmhaube", 			[("sturmhaube_7BW",0)], itp_merchandise|itp_type_head_armor, 0, 1250, weight(3.5)|abundance(80)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate,],
#["fracia_helmet",					"Fracia Helmet",					[("fracia_helmet_1",0)],			itp_merchandise|itp_type_head_armor|itp_fit_to_head,					0, 4850, weight(4.8)|abundance(100)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],

#rm--


##### TIER 1 - 10 ARMOR #####
["cloth_cap_a",			"Cloth Cap",		[("chionite_hat_b",0)],	itp_merchandise|itp_type_head_armor, 0, 50, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth ],
["cloth_cap_b",			"Cloth Cap",		[("chionite_hat_d",0)],	itp_merchandise|itp_type_head_armor, 0, 50, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth ],
["cloth_cap_c",			"Cloth Cap",		[("chionite_hat_f",0)],	itp_merchandise|itp_type_head_armor, 0, 50, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth ],
["woolen_cap",			"Woolen Cap",		[("woolen_cap_new",0)],	itp_merchandise|itp_type_head_armor, 0, 79, weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["pointed_felt_hat",	"Pointed Felt Hat",	[("felt_hat_a_new",0)],	itp_merchandise|itp_type_head_armor, 0, 85, weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

##### TIER 2 - 17 ARMOR #####
["fur_hat",					"Fur Hat",				[("fur_hat_a_new",0)],		itp_merchandise|itp_type_head_armor, 0, 90, weight(1.25)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["leather_helmet",			"Leather Helmet",		[("Helmet_A_vs2",0)],		itp_merchandise|itp_type_head_armor, 0, 100, weight(1.25)|abundance(100)|head_armor(17)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["leather_warrior_cap",		"Leather Warrior Cap",	[("skull_cap_new_b",0)],	itp_merchandise|itp_type_head_armor, 0, 125, weight(1.25)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

##### TIER 3 - 24 ARMOR #####
["cap_with_fur",			"Cap with Fur",					[("vaeg_helmet3",0)],		itp_merchandise|itp_type_head_armor, 0, 185, weight(1.5)|abundance(100)|head_armor(21)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["skullcap",				"Skullcap",						[("skull_cap_new_a",0)],	itp_merchandise|itp_type_head_armor, 0, 190, weight(1.6)|abundance(100)|head_armor(22)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["heavy_leather_helmet",	"Heavy Leather Helmet",			[("Helmet_A",0)],			itp_merchandise|itp_type_head_armor, 0, 215, weight(1.5)|abundance(100)|head_armor(23)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["nomad_cap",				"Nomad Cap",					[("nomad_cap_a_new",0)],	itp_merchandise|itp_type_head_armor, 0, 245, weight(1.8)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

##### TIER 4 - 31 ARMOR #####
["helmet_with_cap",				"Helmet with Cap",				[("norman_helmet_a",0)],							itp_merchandise|itp_type_head_armor|itp_fit_to_head,		0, 345 , weight(2.1)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["spiked_cap",					"Spiked Cap",					[("vaeg_helmet1",0)],								itp_merchandise|itp_type_head_armor,						0, 390 , weight(2.2)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["northern_helmet",				"Northern Helmet",				[("Helmet_B_vs2",0)],								itp_merchandise|itp_type_head_armor|itp_fit_to_head,		0, 450 , weight(2.1)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["helmet_with_lamellar_guard",	"Helmet with Lamellar Guard",	[("vaeg_helmet4",0)],								itp_merchandise|itp_type_head_armor,						0, 495 , weight(2.3)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["steppe_helmet_a",				"Steppe Helmet",				[("rus_helm",0), ("inv_rus_helm",ixmesh_inventory)],itp_merchandise|itp_type_head_armor|itp_attach_armature,	0, 515 , weight(2.1)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["steppe_helmet_b",				"Steppe Helmet",				[("vaeg_helmet2",0)],								itp_merchandise|itp_type_head_armor,						0, 530 , weight(2.5)|abundance(100)|head_armor(34)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],

##### TIER 5 - 38 ARMOR #####
["spiked_helmet",			"Spiked Helmet",			[("spiked_helmet_new",0)],		itp_merchandise| itp_type_head_armor,					0, 278, weight(2.4)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["nordic_helmet",			"Nordic Helmet",			[("helmet_w_eyeguard_new",0)],	itp_merchandise| itp_type_head_armor,					0, 340, weight(2.6)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["norsk_decorated",			"Norsk Decorated",			[("norskspangendecorated",0)],	itp_merchandise| itp_type_head_armor,					0, 754, weight(2.7)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["nordic_fighter_helmet",	"Nordic Fighter Helmet",	[("Helmet_B",0)], 				itp_merchandise| itp_type_head_armor|itp_fit_to_head,	0, 240, weight(2.5)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["pointed_helmet",			"Pointed Helmet",			[("tagancha_helm_b",0),	("inv_tagancha_helm_b",ixmesh_inventory)],	itp_merchandise|itp_type_head_armor|itp_attach_armature,	0, 820 , weight(2.7)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["reyvadin_helm_a",			"Reyvadin Helm",			[("gnezdovo_helm_a",0),	("inv_gnezdovo_helm_a",ixmesh_inventory)],	itp_merchandise|itp_type_head_armor|itp_attach_armature,	0, 640 , weight(3.1)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["reyvadin_helm_b",			"Reyvadin Helm",			[("gnezdovo_helm_b",0),	("inv_gnezdovo_helm_b",ixmesh_inventory)],	itp_merchandise|itp_type_head_armor|itp_attach_armature,	0, 640 , weight(3.1)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],

##### TIER 6 - 45 ARMOR #####
["heavy_pointed_helmet",	"Heavy Pointed Helmet",		[("tagancha_helm_a",0),		("inv_tagancha_helm_a",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0, 950, weight(3.3)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["war_helmet",				"War Helmet",				[("vaeg_helmet6",0)],		itp_merchandise|itp_type_head_armor, 0, 1250 , weight(3.4)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["coifed_nordic_helm",		"Coifed Nordic Helm",		[("coifedpointyhelm",0)],	itp_merchandise|itp_type_head_armor, 0, 1500 , weight(3.3)|abundance(90)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["nordic_huscarl_helmet",	"Nordic Huscarl's Helmet",	[("Helmet_C_vs2",0)],		itp_merchandise|itp_type_head_armor, 0, 1750 , weight(3.6)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["nordic_helm_a",			"Nordic Helm",				[("normanhelmet",0)],		itp_merchandise|itp_type_head_armor, 0, 1500 , weight(3.4)|abundance(90)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["nordic_helm_b",			"Nordic Helm",				[("pointedhelmet",0)],		itp_merchandise|itp_type_head_armor, 0, 2250 , weight(3.5)|abundance(90)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],

##### TIER 7 - 52 ARMOR #####
["nasal_helmet",			"Nasal Helmet",				[("nasal_helmet_b",0)],		itp_merchandise|itp_type_head_armor,	0, 2750 , weight(3.8)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["noble_nordic_helm",		"Noble Nordic Helm",		[("noble_vikinghelm",0)],	itp_merchandise|itp_type_head_armor,	0, 3000 , weight(3.9)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["nordic_warlord_helmet",	"Nordic Warlord Helmet",	[("Helmet_C",0)],			itp_merchandise|itp_type_head_armor,	0, 3250 , weight(4.0)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["face_mask",				"Face Mask",				[("litchina_helm",0), ("inv_litchina_helm",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0, 3500 , weight(3.9)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["heavy_war_helm",			"Heavy War Helm",			[("novogrod_helm",0), ("inv_novogrod_helm",ixmesh_inventory)], itp_merchandise|itp_type_head_armor|itp_attach_armature, 0, 3750 , weight(4.1)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],






##rm++
#["rus_helmet_a", "Vaegiran Helmet", [("rus_helmet_a",0)], itp_type_head_armor   ,0, 278 , weight(2)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0) ,imodbits_cloth, [], [fac_kingdom_2]],
#["footman_helmet", "Footman's Helmet", [("skull_cap_new",0)], itp_merchandise| itp_type_head_armor   ,0, 95 , weight(1.5)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1, fac_kingdom_5]],
#["segmented_helmet", "Segmented Helmet", [("segmented_helm_new",0)], itp_merchandise| itp_type_head_armor   ,0, 174 , weight(1.25)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["helmet_with_neckguard", "Helmet with Neckguard", [("neckguard_helm_new",0)], itp_merchandise| itp_type_head_armor   ,0, 190 , weight(1.5)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["viking_helm1", "Nordic Helm", [("plainhelm",0)], itp_merchandise | itp_type_head_armor,0, 524 , weight(1.6)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_4]],
#["norsk_spangen", "Norsk Helm", [("norskspangen1",0)], itp_merchandise | itp_type_head_armor,0, 578 , weight(1.8)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_4]],
#["vaegir_noble_helmet", "Vaegiran Nobleman Helmet", [("vaeg_helmet7",0)], itp_merchandise| itp_type_head_armor   ,0, 710, weight(2.75)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_2]],
#["nikolskoe_helm", "Nikolskoe helm", [("nikolskoe_helm",0), ("inv_nikolskoe_helm",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature  ,0, 820 , weight(2)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_2]],
#["viking_helm2", "Chieftain Helm", [("chieftainhelm",0)], itp_merchandise | itp_type_head_armor,0, 974 , weight(2.3)|abundance(70)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["vaegir_mask", "Vaegiran War Mask", [("vaeg_helmet9",0)], itp_merchandise| itp_type_head_armor |itp_covers_beard ,0, 950 , weight(3.50)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_2]],
##rm--









##### TIER 1 - 10 ARMOR #####
["turban_a",			"Turban",				[("tuareg_open",0)],		itp_merchandise|itp_type_head_armor,					0, 50, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["turban_b",			"Turban",				[("tuareg",0)],				itp_merchandise|itp_type_head_armor|itp_covers_beard,	0, 75, weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["leather_nomad_cap",	"Leather Nomad Cap",	[("nomad_cap_b_new",0)],	itp_merchandise|itp_type_head_armor,					0, 95, weight(1)|abundance(100)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

##### TIER 2 - 17 ARMOR #####
["leather_steppe_cap_a",		"Leather Steppe Cap",					[("leather_steppe_cap_a_new",0)],	itp_merchandise|itp_type_head_armor,					0, 110, weight(1.25)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["leather_steppe_cap_b",		"Leather Steppe Cap",					[("tattered_steppe_cap_b_new",0)],	itp_merchandise|itp_type_head_armor,					0, 115, weight(1.35)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["desert_leather_cap",			"Desert Leather Cap",					[("helm_saracin_3",0)],				itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 145, weight(1.15)|abundance(100)|head_armor(17)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["white_turban_with_iron_cap",	"White Turban With Iron Cap",			[("saracen_helmet_f",0)],			itp_merchandise|itp_type_head_armor,					0, 155, weight(1.45)|abundance(100)|head_armor(19)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["yellow_turban_with_iron_cap",	"Yellow Turban With Iron Cap",			[("saracen_helmet_a",0)],			itp_merchandise|itp_type_head_armor,					0, 195, weight(1.55)|abundance(100)|head_armor(21)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],

##### TIER 3 - 24 ARMOR #####
["felt_steppe_cap",			"Felt Steppe Cap",			[("felt_steppe_cap",0)],	itp_merchandise|itp_type_head_armor,					0, 175, weight(1.75)|abundance(100)|head_armor(22)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["leather_steppe_cap_c",	"Leather Steppe Cap",		[("steppe_cap_a_new",0)],	itp_merchandise|itp_type_head_armor,					0, 195, weight(1.85)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["turban_with_coif_a",		"Turban With Mail Coif",	[("saracin_turban_a",0)],	itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 215, weight(1.95)|abundance(100)|head_armor(21)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["turban_with_coif_b",		"Turban With Mail Coif",	[("saracin_turban_b",0)],	itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 275, weight(1.95)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["turban_with_coif_c",		"Turban With Mail Coif",	[("saracin_turban_c",0)],	itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 325, weight(1.95)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["turban_with_coif_d",		"Turban With Mail Coif",	[("turban_mail_a",0)],		itp_merchandise|itp_type_head_armor,					0, 415, weight(2.10)|abundance(100)|head_armor(27)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["steppe_helmet",			"Steppe Helmet",			[("magyar_helmet_a",0)],	itp_merchandise|itp_type_head_armor,					0, 315, weight(2.10)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_cloth ],

##### TIER 4 - 31 ARMOR #####
["cavalry_helmet",			"Cavalry Helmet",			[("lamellar_helmet_b",0)],		itp_merchandise|itp_type_head_armor,					0, 375, weight(2.25)|abundance(100)|head_armor(29)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["helmet_with_turban_a",	"Helmet With Turban",		[("saracen_helmet_b",0)],		itp_merchandise|itp_type_head_armor,					0, 425, weight(2.75)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["helmet_with_turban_b",	"Helmet With Turban",		[("saracen_helmet_d",0)],		itp_merchandise|itp_type_head_armor,					0, 400, weight(2.55)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["shahi",					"Shahi",					[("shahi",0)],					itp_merchandise|itp_type_head_armor,					0, 475, weight(2.45)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["rabati",					"Rabati",					[("rabati",0)],					itp_merchandise|itp_type_head_armor,					0, 525, weight(2.60)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["iron_cap_with_padding",	"Iron Cap with Padding",	[("helm_saracin_c",0)],			itp_merchandise|itp_type_head_armor|itp_fit_to_head,	0, 575, weight(2.85)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["conical_helm",			"Conical Helm",				[("conical_helmet_steppe",0)],	itp_merchandise|itp_type_head_armor,					0, 525, weight(2.95)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],

##### TIER 5 - 38 ARMOR #####
["helmet_with_turban_c",	"Helmet With Turban",		[("gulam_helm_b",0)],				itp_merchandise|itp_type_head_armor|itp_fit_to_head|itp_attach_armature,	0, 625, weight(2.70)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["helmet_with_turban_d",	"Helmet With Turban",		[("gulam_helm_c",0)],				itp_merchandise|itp_type_head_armor|itp_fit_to_head|itp_attach_armature,	0, 695, weight(2.70)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["heavy_conical_helm",		"Heavy Conical Helm",		[("tattered_steppe_cap_a_new",0)],	itp_merchandise|itp_type_head_armor|itp_merchandise,						0, 725, weight(2.85)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["heavy_steppe_helmet",		"Heavy Steppe Helmet",		[("khergit_guard_helmet",0)],		itp_merchandise|itp_type_head_armor,										0, 750, weight(2.95)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["desert_warrior_helmet",	"Desert Warrior Helmet",	[("helm_saracin_j",0)],				itp_merchandise|itp_type_head_armor|itp_fit_to_head,						0, 775, weight(3.10)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["iron_cap_with_turban",	"Iron Cap with Turban",		[("helm_saracin_2",0)],				itp_merchandise|itp_type_head_armor|itp_fit_to_head,						0, 800, weight(3.00)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["veiled_helmet",			"Veiled Helmet",			[("gulam_helm_a",0)],				itp_merchandise|itp_type_head_armor|itp_fit_to_head,						0, 725, weight(3.10)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],

##### TIER 6 - 45 ARMOR #####
["elite_steppe_helmet",		"Elite Steppe Helmet",		[("lamellar_helmet_a",0)],		itp_merchandise|itp_type_head_armor,										0, 1000, weight(3.75)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["nobleman_steppe_helmet",	"Nobleman Steppe Helmet",	[("helm_saracin_1",0)],			itp_merchandise|itp_type_head_armor|itp_fit_to_head,						0, 1250, weight(3.50)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["elite_desert_helmet",		"Elite Desert Helmet",		[("gulam_helm_f",0)],			itp_merchandise|itp_type_head_armor|itp_fit_to_head|itp_attach_armature,	0, 1500, weight(3.85)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],

##### TIER 7 - 52 ARMOR #####
["royal_desert_helmet",		"Royal Desert Helmet",		[("helm_Sultan_saracens",0)],	itp_merchandise|itp_type_head_armor|itp_fit_to_head|itp_attach_armature,	0, 2500, weight(4.00)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],



##rm++
#["steppe_cap", "Steppe Cap", [("steppe_cap_a_new",0)], itp_merchandise| itp_type_head_armor  |itp_civilian ,0, 14 , weight(1)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3]],
#["iron_cap_with_chainmail", "Iron Cap with Chainmail", [("helm_saracin_c",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 550, weight(3.5)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["sipahi_helmet_a", "Sipahi Helmet", [("sipahi_helmet_a",0)], itp_type_head_armor   ,0, 278 , weight(2)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
#["sarranid_warrior_cap", "Sarranid Warrior Cap", [("tuareg_helmet",0)], itp_merchandise| itp_type_head_armor | itp_covers_beard  ,0, 90 , weight(2)|abundance(100)|head_armor(19)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_6]],
#["sarranid_horseman_helmet", "Horseman Helmet", [("sar_helmet2",0)], itp_merchandise| itp_type_head_armor   ,0, 180 , weight(2.75)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_6]],
#["heavy_ghulam_helmet", "Heavy Ghulam Helmet", [("gulam_helm_d",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head|itp_attach_armature, 0, 500, weight(3.5)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["sarranid_helmet1", "Sarranid Keffiyeh Helmet", [("sar_helmet1",0)], itp_merchandise| itp_type_head_armor   ,0, 290 , weight(2.50)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_6]],
#["sarranid_archer_helmet", "Sarranid Archer Helmet", [("helm_saracin_b",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 450, weight(2.9)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["sarranid_mail_coif", "Sarranid Mail Coif", [("tuareg_helmet2",0)], itp_merchandise| itp_type_head_armor ,0, 430 , weight(3)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_6]],
#["sarranid_helmet_with_coif", "Sarranid Helmet with Coif", [("helm_saracin_a",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 700, weight(3.5)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["saracen_helmet_with_mail", "Saracen Helmet With Mail", [("saracen_helmet_e",0)], itp_merchandise|itp_type_head_armor, 0, 500, weight(3.25)|abundance(80)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_6]],
#["sarranid_veiled_helmet", "Sarranid Veiled Helmet", [("sar_helmet4",0)], itp_merchandise| itp_type_head_armor | itp_covers_beard  ,0, 810 , weight(3.50)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_6]],
#["full_saracen_helmet", "Full Saracen Helmet", [("saracen_helmet_c",0)], itp_merchandise|itp_type_head_armor, 0, 750, weight(3.5)|abundance(80)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_6]],
#["gilded_mamluke_helmet", "Gilded Mamluke Helmet", [("mamluk_helmet_2",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_6]],
#["mamluke_helmet", "Mamluke Helmet", [("mamluk_helmet",0)], itp_merchandise|itp_type_head_armor, 0, 1000, weight(3.5)|abundance(80)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate, [], [fac_kingdom_6]],
##rm--


########## Mercenary ##########

["blue_highlander_cap", "Blue Highlander Cap", [("h_h1",0)], itp_merchandise|itp_type_head_armor|itp_attach_armature|itp_fit_to_head , 0, 50, weight(2)|abundance(80)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["brown_highlander_cap", "Brown Highlander Cap", [("h_h1_1",0)], itp_merchandise|itp_type_head_armor|itp_attach_armature|itp_fit_to_head , 0, 50, weight(2)|abundance(80)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["blue_eathered_highlander_cap", "Blue Feathered Highlander Cap",[("h_h2",0)], itp_merchandise|itp_type_head_armor|itp_attach_armature|itp_fit_to_head , 0, 100, weight(3)|abundance(80)|head_armor(15)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],
["brown_feathered_highlander_cap", "Brown Feathered Highlander Cap", [("h_h1_1",0)], itp_merchandise|itp_type_head_armor|itp_attach_armature|itp_fit_to_head , 0, 100, weight(3)|abundance(80)|head_armor(15)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_5]],

["grandmaster_helmet", "Grandmaster Helmet", [("helm_king_Jerusalem",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head|itp_attach_armature, 0, 750, weight(3)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],


########## Bandit ##########
["bandit_helmet_a", "Bandit Helmet", [("dethertir_helm_c",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 250, weight(1.5)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["bandit_helmet_b", "Bandit Helmet", [("dethertir_helm_b",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 350, weight(1.8)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
["bandit_helmet_c", "Bandit Helmet", [("dethertir_helm_a",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 450, weight(2.5)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],





##################
##### SWORDS #####
##################



########## One-handed ##########

##### Western #####
##### Tier 1 #####
["short_sword",	"Short Sword",	[("sword_medieval_c_small",0),("sword_medieval_c_small_scabbard", ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	450, weight(1.5)|difficulty(6)|spd_rtng(99)|weapon_length(86)|swing_damage(25, cut)|thrust_damage(15, pierce), imodbits_sword_high ],
["sword",		"Sword",		[("sword_medieval_c",0),("sword_medieval_c_scabbard", ixmesh_carry)],				itp_merchandise|itp_type_one_handed_wpn|itp_primary,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	400, weight(1.5)|difficulty(6)|spd_rtng(95)|weapon_length(95)|swing_damage(22, cut)|thrust_damage(12, pierce), imodbits_sword_high ],
["falchion",	"Falchion",		[("falchion_new",0)],																itp_merchandise|itp_type_one_handed_wpn|itp_primary,itc_scimitar|itcf_carry_sword_left_hip,									375, weight(2.5)|difficulty(8)|spd_rtng(110)|weapon_length(73)|swing_damage(24, cut)|thrust_damage(0, pierce), imodbits_sword ],

##### Tier 2 #####
["arming_sword",			"Arming Sword",			[("sword_medieval_b",0),("sword_medieval_b_scabbard", ixmesh_carry),("sword_rusty_a",imodbit_rusty),("sword_rusty_a_scabbard", ixmesh_carry|imodbit_rusty)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 575 , weight(1.5)|difficulty(2)|spd_rtng(95)|weapon_length(95)|swing_damage(25 , cut)|thrust_damage(15 ,  pierce), imodbits_sword_high ],
["long_sword",				"Long Sword",			[("sword_medieval_d_long",0),("sword_medieval_d_long_scabbard", ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	550, weight(1.8)|difficulty(2)|spd_rtng(93) |weapon_length(105)|swing_damage(24, cut)|thrust_damage(14, pierce), imodbits_sword ],
["mercenary_falchion_a",	"Mercenary Falchion",	[("falshion_1",0),("falshion_1_scab",ixmesh_carry)],							itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	300, weight(1.5)|difficulty(8)|spd_rtng(115)|weapon_length(65)|swing_damage(28, cut)|thrust_damage(0, pierce), imodbits_sword_high ],
["mercenary_falchion_b",	"Mercenary Falchion",	[("falshion_2",0)],																itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	300, weight(2.1)|difficulty(9)|spd_rtng(110)|weapon_length(68)|swing_damage(30, cut)|thrust_damage(0, pierce), imodbits_sword_high ],
["cheap_cleaver",			"Cheap Cleaver",		[("military_cleaver_c",0)],														itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip,								263, weight(1.5)|difficulty(5)|spd_rtng(95) |weapon_length(95)|swing_damage(25, cut)|thrust_damage(0, pierce), imodbits_sword_high ],

##### Tier 3 #####
["western_arming_sword",		"Western Arming Sword",		[("crusaders_swords_a",0),("crusader_sword_a_scabbard",ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	750, weight(1.5)|difficulty(8)|spd_rtng(110)|weapon_length(75)|swing_damage(29,cut)|thrust_damage(17,pierce), imodbits_sword_high ],
["western_infantry_sword_a",	"Western Infantry Sword",	[("crusader_sword_b",0),("crusader_sword_b_scabbard",ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	800, weight(1.5)|difficulty(8)|spd_rtng(102)|weapon_length(86)|swing_damage(30,cut)|thrust_damage(18,pierce), imodbits_sword_high ],
["western_infantry_sword_b",	"Western Infantry Sword",	[("crusader_sword_c",0),("crusader_sword_c_scabbard",ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	850, weight(1.7)|difficulty(8)|spd_rtng(100)|weapon_length(86)|swing_damage(31,cut)|thrust_damage(18,pierce), imodbits_sword_high ],

##### Tier 4 #####
["western_long_sword_a", "Western Long Sword", [("k_long_sword_a",0),("k_long_sword_a",ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	1000, weight(2.0)|difficulty(12)|spd_rtng(95)|weapon_length(100)|swing_damage(32,cut)|thrust_damage(20,pierce), imodbits_sword_high ],
["western_long_sword_b", "Western Long Sword", [("k_long_sword_b",0),("k_long_sword_b",ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	1250, weight(2.0)|difficulty(12)|spd_rtng(93)|weapon_length(100)|swing_damage(33,cut)|thrust_damage(20,pierce), imodbits_sword_high ],
["western_long_sword_c", "Western Long Sword", [("k_long_sword_c",0),("k_long_sword_c",ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	1500, weight(2.0)|difficulty(12)|spd_rtng(91)|weapon_length(100)|swing_damage(33,cut)|thrust_damage(21,pierce), imodbits_sword_high ],

##### Tier 5 #####
["western_nobleman_sword_a", "Western Nobleman Sword", [("crusader_long_sword_a",0),("crusader_long_sword_a_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 2000, weight(1.5)|difficulty(8)|spd_rtng(95)|weapon_length(100)|swing_damage(34,cut)|thrust_damage(22,pierce), imodbits_sword_high ],
["western_nobleman_sword_b", "Western Nobleman Sword", [("crusader_long_sword_b",0),("crusader_long_sword_b_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 3000, weight(1.5)|difficulty(8)|spd_rtng(92)|weapon_length(100)|swing_damage(35,cut)|thrust_damage(22,pierce), imodbits_sword_high ],
["western_nobleman_sword_c", "Western Nobleman Sword", [("crusader_long_sword_c",0),("crusader_long_sword_c_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 4000, weight(1.5)|difficulty(8)|spd_rtng(89)|weapon_length(100)|swing_damage(35,cut)|thrust_damage(23,pierce), imodbits_sword_high ],

##### Northern #####

##### Tier 3 #####
["nordic_short_sword",	"Nordic Short Sword",	[("sword_viking_b_small",0),("sword_viking_b_small_scabbard", ixmesh_carry)],		itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 1000 , weight(1.25)|difficulty(2)|spd_rtng(99)|weapon_length(85)|swing_damage(27, cut)|thrust_damage(25, pierce), imodbits_sword_high ],
["nordic_sword",		"Nordic Sword",			[("sword_viking_b",0),("sword_viking_b_scabbard", ixmesh_carry)],					itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 1250 , weight(1.50)|difficulty(2)|spd_rtng(95)|weapon_length(95)|swing_damage(26, cut)|thrust_damage(24, pierce), imodbits_sword_high ],

##### Tier 4 #####
["nordic_war_sword",		"Nordic War Sword", [("sword_viking_c",0),("sword_viking_c_scabbard ", ixmesh_carry)],					itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 1500, weight(1.50)|difficulty(2)|spd_rtng(99) |weapon_length(94)|swing_damage(30, cut)|thrust_damage(24, pierce), imodbits_sword_high ] ,
["nordic_short_war_sword",	"Nordic Short War Sword", [("sword_viking_a_small",0),("sword_viking_a_small_scabbard", ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 2000, weight(1.25)|difficulty(2)|spd_rtng(103)|weapon_length(86)|swing_damage(30, cut)|thrust_damage(26, pierce), imodbits_sword_high ],

##### Tier 5 #####
["nordic_nobleman_sword",	"Nordic Nobleman Sword", [("sword_viking_a",0),("sword_viking_a_scabbard", ixmesh_carry)],				itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 3000 , weight(1.5)|difficulty(2)|spd_rtng(99)|weapon_length(95)|swing_damage(31 , cut) | thrust_damage(30 ,  pierce),imodbits_sword_high, [], [fac_kingdom_4]],

##### Eastern #####

##### Tier 1 #####
["scimitar", "Scimitar", [("scimitar_a",0),("scab_scimeter_a", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 300, weight(1.5)|difficulty(2)|spd_rtng(105)|weapon_length(97)|swing_damage(22 , cut)|thrust_damage(0 ,  pierce), imodbits_sword_high ],

##### Tier 2 #####
["scimitar_b", "Elite Scimitar", [("scimitar_b",0),("scab_scimeter_b", ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 450 , weight(1.5)|difficulty(3)|spd_rtng(100)|weapon_length(103)|swing_damage(24 , cut)|thrust_damage(0 ,  pierce), imodbits_sword_high ],

##### Tier 3 #####
["nomad_sabre",		"Nomad Sabre",		[("khergit_sword_b",0),("khergit_sword_b_scabbard", ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	750, weight(1.2)|difficulty(2)|spd_rtng(110)|weapon_length(97)|swing_damage(26, cut),imodbits_sword_high ],
["eastern_sword",	"Eastern Sword",	[("saracin_sword_b",0),("scab_saracin_sword_b",ixmesh_carry)],		itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	850, weight(1.5)|difficulty(8)|spd_rtng(110)|weapon_length(89)|swing_damage(27, cut)|thrust_damage(19, pierce), imodbits_sword_high ],

##### Tier 4 #####
["sabre_a",					"Sabre",				[("khergit_sword_c",0),("khergit_sword_c_scabbard", ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	1250, weight(1.5)|difficulty(2)|spd_rtng(110)|weapon_length(97)|swing_damage(29 , cut), imodbits_sword_high ],
["sabre_b",					"Sabre",				[("khergit_sword_a",0),("khergit_sword_a_scabbard", ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	1500, weight(1.5)|difficulty(2)|spd_rtng(103)|weapon_length(98)|swing_damage(32 , cut), imodbits_sword_high ],
["eastern_long_sword_a",	"Eastern Long Sword",	[("saracin_sword_a",0),("scab_saracin_sword_a",ixmesh_carry)],		itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	2000, weight(1.5)|difficulty(8)|spd_rtng(95)|weapon_length(100)|swing_damage(29,cut)|thrust_damage(24,pierce), imodbits_sword_high ],
["eastern_long_sword_b",	"Eastern Long Sword",	[("saracin_sword_d",0),("scab_saracin_sword_d",ixmesh_carry)],		itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	2250, weight(1.5)|difficulty(8)|spd_rtng(91)|weapon_length(100)|swing_damage(30,cut)|thrust_damage(24,pierce), imodbits_sword_high ],

##### Tier 5 #####
["heavy_sabre",					"Heavy Sabre",				[("khergit_sword_d",0),("khergit_sword_d_scabbard", ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	3500, weight(1.75)|difficulty(2)|spd_rtng(110)|weapon_length(96)|swing_damage(33, cut),imodbits_sword_high ],
["eastern_nobleman_sword_a",	"Eastern Nobleman Sword",	[("saracin_sword_e",0),("scab_saracin_sword_e",ixmesh_carry)],		itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	3500, weight(1.5)|difficulty(8)|spd_rtng(100)|weapon_length(102)|swing_damage(32,cut)|thrust_damage(26,pierce), imodbits_sword_high ],
["eastern_nobleman_sword_b",	"Eastern Nobleman Sword",	[("saracin_sword_c",0),("scab_saracin_sword_c",ixmesh_carry)],		itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,	4500, weight(1.5)|difficulty(8)|spd_rtng(95)|weapon_length(105)|swing_damage(33,cut)|thrust_damage(27,pierce), imodbits_sword_high ],

##### Sidearms #####
##### Tier 1 #####
["sickle",	"Sickle",	[("sickle",0)],				itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_parry, itc_cleaver,				10, weight(1.5)|difficulty(0)|spd_rtng(125)|weapon_length(40)|swing_damage(22 , cut)|thrust_damage(0,  pierce), imodbits_none ],
["cleaver",	"Cleaver",	[("cleaver_new",0)],		itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_wooden_parry, itc_cleaver,				14, weight(1.5)|difficulty(0)|spd_rtng(120)|weapon_length(35)|swing_damage(26 , cut)|thrust_damage(0,  pierce), imodbits_none ],
["knife",	"Knife",	[("peasant_knife_new",0)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left,	18, weight(0.5)|difficulty(0)|spd_rtng(120)|weapon_length(40)|swing_damage(23 , cut)|thrust_damage(13,  pierce), imodbits_sword ],

##### Tier 2 #####
["long_knife",	"Long Knife",	[("khyber_knife_new",0)],																											itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_right,								23, weight(0.75)|difficulty(0)|spd_rtng(117)|weapon_length(60)|swing_damage(24 , cut)|thrust_damage(20 ,  pierce), imodbits_sword ],
["dagger",		"Dagger",		[("dagger_b",0),("dagger_b_scabbard",ixmesh_carry),("dagger_b",imodbits_good),("dagger_b_scabbard",ixmesh_carry|imodbits_good)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn,	37, weight(0.75)|difficulty(0)|spd_rtng(125)|weapon_length(47)|swing_damage(22 , cut)|thrust_damage(26 ,  pierce), imodbits_sword_high ],

##### Tier 3 #####
["war_dirk", "War Dirk",[("dirk",0),("dirk_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_dagger|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 183, weight(1.25)|difficulty(6)|spd_rtng(120)|weapon_length(55)|swing_damage(25 , cut)|thrust_damage(26, pierce),imodbits_sword ],

########## Mercenary ##########

["mercenary_sword_a",		"Mercenary Sword",			[("cheapsword1",0),("cheapswords1_scabbard",ixmesh_carry)],					itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 1500, weight(1.5)|difficulty(8)|spd_rtng(109)|weapon_length(102)|swing_damage(18, cut)|thrust_damage(25,pierce), imodbits_sword_high ],
["mercenary_sword_b",		"Mercenary Sword",			[("cheapsword2",0),("cheapswords2_scabbard",ixmesh_carry)],					itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 1750, weight(1.5)|difficulty(8)|spd_rtng(108)|weapon_length(102)|swing_damage(18, cut)|thrust_damage(26,pierce), imodbits_sword_high ],
["mercenary_sword_c",		"Mercenary Sword",			[("cheapsword3",0),("cheapswords3_scabbard",ixmesh_carry)],					itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 2000, weight(1.5)|difficulty(8)|spd_rtng(106)|weapon_length(102)|swing_damage(20, cut)|thrust_damage(27,pierce), imodbits_sword_high ],
["mercenary_captain_sword", "Mercenary Captain Sword",	[("goodrapier1",0),("goodrapier1_scabbard",ixmesh_carry)],					itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 2500, weight(1.5)|difficulty(8)|spd_rtng(104)|weapon_length(102)|swing_damage(23, cut)|thrust_damage(29,pierce), imodbits_sword_high ],
["broadsword_a",			"Broadsword",				[("goodsword1",0),("goodsword1_scabbard",ixmesh_carry)],					itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 3000, weight(1.5)|difficulty(8)|spd_rtng(98)|weapon_length(97)|swing_damage(30, cut)|thrust_damage(17, pierce), imodbits_sword_high ],
["broadsword_b",			"Broadsword",				[("goodsword1",0),("goodsword1_scabbard",ixmesh_carry)],					itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 3500, weight(1.5)|difficulty(8)|spd_rtng(97)|weapon_length(90)|swing_damage(31, cut)|thrust_damage(17, pierce), imodbits_sword_high ],
["broadsword_c",			"Broadsword",				[("highlad_broadsword",0),("highlad_broadsword_scabbard", ixmesh_carry)],	itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 4000, weight(1.5)|difficulty(9)|spd_rtng(99)|weapon_length(95)|swing_damage(33, cut)|thrust_damage(21, pierce), imodbits_sword_high, [], ],



["arabian_sword_a",         "Sarranid Sword", [("arabian_sword_a",0),("scab_arabian_sword_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 108 , weight(1.5)|difficulty(2)|spd_rtng(99) | weapon_length(97)|swing_damage(26 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high, [], [fac_kingdom_3, fac_kingdom_6]],
["arabian_sword_b",         "Sarranid Arming Sword", [("arabian_sword_b",0),("scab_arabian_sword_b", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 218 , weight(1.7)|difficulty(2)|spd_rtng(99) | weapon_length(97)|swing_damage(28 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high, [], [fac_kingdom_3, fac_kingdom_6]],
["sarranid_cavalry_sword",  "Sarranid Cavalry Sword", [("arabian_sword_c",0),("scab_arabian_sword_c", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 310 , weight(1.5)|difficulty(2)|spd_rtng(98) | weapon_length(105)|swing_damage(28 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high, [], [fac_kingdom_3, fac_kingdom_6]],
["arabian_sword_d",         "Sarranid Guard Sword", [("arabian_sword_d",0),("scab_arabian_sword_d", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 420 , weight(1.7)|difficulty(2)|spd_rtng(99) | weapon_length(97)|swing_damage(30 , cut) | thrust_damage(20 ,  pierce),imodbits_sword_high, [], [fac_kingdom_3, fac_kingdom_6]],

["sword_medieval_a", "Sword", [("sword_medieval_a",0),("sword_medieval_a_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 163 , weight(1.5)|difficulty(2)|spd_rtng(99) | weapon_length(95)|swing_damage(27 , cut) | thrust_damage(22 ,  pierce),imodbits_sword_high ],
["sword_medieval_b_small", "Short Sword", [("sword_medieval_b_small",0),("sword_medieval_b_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 152 , weight(1)|difficulty(2)|spd_rtng(102) | weapon_length(85)|swing_damage(26, cut) | thrust_damage(24, pierce),imodbits_sword_high ],
["sword_medieval_c_long", "Arming Sword", [("sword_medieval_c_long",0),("sword_medieval_c_long_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 480 , weight(1.7)|difficulty(2)|spd_rtng(99) | weapon_length(100)|swing_damage(29 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high ],





########## Two-handed ##########
["two_handed_cleaver", "War Cleaver", [("military_cleaver_a",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 640 , weight(2.75)|difficulty(10)|spd_rtng(93) | weapon_length(120)|swing_damage(45 , cut) | thrust_damage(0 ,  cut),imodbits_sword_high ],
["military_cleaver_b", "Soldier's Cleaver", [("military_cleaver_b",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 193 , weight(1.5)|difficulty(5)|spd_rtng(96) | weapon_length(95)|swing_damage(31 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high ],
["great_sword",         "Great Sword", [("b_bastard_sword",0),("scab_bastardsw_b", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 423 , weight(2.75)|difficulty(10)|spd_rtng(95) | weapon_length(125)|swing_damage(39 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
["sword_of_war", "Sword of War", [("b_bastard_sword",0),("scab_bastardsw_b", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 524 , weight(3)|difficulty(11)|spd_rtng(94) | weapon_length(130)|swing_damage(40 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
["sword_two_handed_b",         "Two-handed Sword", [("sword_two_handed_b",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 670 , weight(2.75)|difficulty(10)|spd_rtng(97) | weapon_length(110)|swing_damage(40 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high ],
["sword_two_handed_a",         "Great Sword", [("sword_two_handed_a",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 1123 , weight(2.75)|difficulty(10)|spd_rtng(96) | weapon_length(120)|swing_damage(42 , cut) | thrust_damage(29 ,  pierce),imodbits_sword_high ],
["khergit_sword_two_handed_a",         "Two-handed Sabre", [("khergit_sword_two_handed_a",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 523 , weight(2.75)|difficulty(10)|spd_rtng(96) | weapon_length(120)|swing_damage(40 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high, [], [fac_kingdom_3]],
["khergit_sword_two_handed_b",         "Two-handed Sabre", [("khergit_sword_two_handed_b",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 920 , weight(2.75)|difficulty(10)|spd_rtng(96) | weapon_length(120)|swing_damage(44 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high, [], [fac_kingdom_3]],
["bastard_sword_a", "Bastard Sword", [("bastard_sword_a",0),("bastard_sword_a_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise| itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 294 , weight(2.0)|difficulty(9)|spd_rtng(98) | weapon_length(101)|swing_damage(35 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high ],
["bastard_sword_b", "Swadian Bastard Sword", [("bastard_sword_b",0),("bastard_sword_b_scabbard", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise| itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 526 , weight(2.25)|difficulty(9)|spd_rtng(97) | weapon_length(105)|swing_damage(37 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high, [], [fac_kingdom_1]],
["flamberge",  "Flamberge Zweihander", [("flamberge",0)], itp_type_two_handed_wpn|itp_merchandise|itp_crush_through|itp_unbalanced|itp_always_loot|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 1123 , weight(4.75)|abundance(15)|difficulty(11)|spd_rtng(84) | weapon_length(148)|swing_damage(45, cut) | thrust_damage(28 ,  pierce),imodbits_sword_high ],
["mod_stag_sword1",  "Sword of The Stag", [("faradon_twohanded2",0)], itp_crush_through|itp_unbalanced|itp_type_two_handed_wpn|itp_bonus_against_shield|itp_can_knock_down|itp_merchandise| itp_cant_use_on_horseback|itp_primary, itc_greatsword|itcf_carry_sword_back, 1970 , weight(3.95)|difficulty(15)|spd_rtng(87) | weapon_length(118)|swing_damage(41 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high, [], [fac_player_supporters_faction]],
["highlander_claymore", "Highlander Claymore", [("2h_claymore",0)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_back, 294, weight(2.0)|difficulty(13)|spd_rtng(98)|weapon_length(101)|swing_damage(47, cut)|thrust_damage(42 , pierce),imodbits_sword_high, [], [fac_kingdom_5]],
["flamberge_b",         "Flamberge Zweihander", [("flamberge",0)], itp_type_two_handed_wpn|itp_merchandise|itp_always_loot|itp_two_handed|itp_next_item_as_melee|itp_primary, itc_staff|itcf_carry_sword_back, 1123 , weight(3.75)|difficulty(11)|spd_rtng(95) | weapon_length(135)|swing_damage(42, cut) | thrust_damage(56 ,  pierce),imodbits_sword_high ],
["flamberge_b_alt",         "Flamberge Zweihander", [("flamberge",0)], itp_type_polearm|itp_merchandise|itp_always_loot|itp_two_handed|itp_primary, itc_staff|itcf_carry_sword_back, 1123 , weight(3.75)|difficulty(11)|spd_rtng(77) | weapon_length(145)|swing_damage(50, cut) | thrust_damage(28 ,  pierce),imodbits_sword_high ],



################
##### AXES #####
################


########## One-handed ##########
["western_short_war_axe_b", "Western Short War Axe", [("axe_crusader_b",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 250, weight(1.8)|difficulty(13)|spd_rtng(105)|weapon_length(64)|swing_damage(29,pierce)|thrust_damage(0,pierce), imodbits_axe ],
["western_short_war_axe_a", "Western Short War Axe", [("axe_crusader_a",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 250, weight(1.8)|difficulty(10)|spd_rtng(106)|weapon_length(66)|swing_damage(32,cut)|thrust_damage(0,pierce), imodbits_axe ],
["western_war_axe_a", "Western War Axe", [("axe_crusader_1",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 250, weight(2.5)|difficulty(12)|spd_rtng(98)|weapon_length(80)|swing_damage(36,cut)|thrust_damage(0,pierce), imodbits_axe ],
["western_bearded_axe_a", "Western Bearded Axe", [("axe_crusader_c",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 500, weight(2.4)|difficulty(14)|spd_rtng(95)|weapon_length(70)|swing_damage(39,cut)|thrust_damage(0,pierce), imodbits_axe ],
["western_bearded_axe_b", "Western Bearded Axe", [("axe_crusader_d",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 500, weight(2.6)|difficulty(15)|spd_rtng(92)|weapon_length(75)|swing_damage(45,cut)|thrust_damage(0,pierce), imodbits_axe ],


["hatchet",         "Hatchet", [("hatchet",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 13 , weight(2)|difficulty(0)|spd_rtng(97) | weapon_length(60)|swing_damage(23 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["hand_axe",         "Hand Axe", [("hatchet",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 24 , weight(2)|difficulty(7)|spd_rtng(95) | weapon_length(75)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["fighting_axe", "Fighting Axe", [("fighting_ax",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 77 , weight(2.5)|difficulty(8)|spd_rtng(92) | weapon_length(90)|swing_damage(31 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["one_handed_war_axe_a", "One Handed Axe", [("one_handed_war_axe_a",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 87 , weight(1.5)|difficulty(9)|spd_rtng(98) | weapon_length(71)|swing_damage(32 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["one_handed_battle_axe_a", "One Handed Battle Axe", [("one_handed_battle_axe_a",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 142 , weight(1.5)|difficulty(9)|spd_rtng(98) | weapon_length(73)|swing_damage(33 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe ],
["one_handed_war_axe_b", "One Handed War Axe", [("one_handed_war_axe_b",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 190 , weight(1.5)|difficulty(9)|spd_rtng(98) | weapon_length(76)|swing_damage(34 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["one_handed_battle_axe_b", "One Handed Battle Axe", [("one_handed_battle_axe_b",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 230 , weight(1.75)|difficulty(9)|spd_rtng(98) | weapon_length(72)|swing_damage(36 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["one_handed_battle_axe_c", "One Handed Battle Axe", [("one_handed_battle_axe_c",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 550 , weight(2.0)|difficulty(9)|spd_rtng(98) | weapon_length(76)|swing_damage(37 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["one_handed_axe",         "One-handed Axe", [("two_handed_battle_axe_a",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 90 , weight(4.5)|difficulty(12)|spd_rtng(96) | weapon_length(90)|swing_damage(35 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],
["sarranid_axe_a", "Iron Battle Axe", [("one_handed_battle_axe_g",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 250 , weight(1.65)|difficulty(9)|spd_rtng(97) | weapon_length(71)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["sarranid_axe_b", "Iron War Axe", [("one_handed_battle_axe_h",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 540 , weight(2.0)|difficulty(9)|spd_rtng(92) | weapon_length(71)|swing_damage(30 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe ],
["sarranid_two_handed_axe_a",         "Sarranid Battle Axe", [("two_handed_battle_axe_g",0)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_longsword|itcf_carry_axe_back, 350 , weight(3.0)|difficulty(10)|spd_rtng(94) | weapon_length(95)|swing_damage(38 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_6]],
["sarranid_two_handed_axe_b",         "Sarranid War Axe", [("two_handed_battle_axe_h",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_unbalanced, itc_longsword|itcf_carry_axe_back, 280 , weight(2.50)|difficulty(10)|spd_rtng(90) | weapon_length(90)|swing_damage(35 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_6]],
["mod_onehand_axe1", "Vaegiran Fighting Axe", [("bb_serbian_hand_axe",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,  447 , weight(1.3)|difficulty(4)|spd_rtng(98) | weapon_length(65)|swing_damage(26 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2]],
["mod_onehand_axe2", "Vaegiran Field Axe", [("bb_serbian_one_handed_axe_b",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,  397 , weight(1.2)|difficulty(3)|spd_rtng(105) | weapon_length(52)|swing_damage(34 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2]],
["mod_onehand_axe3", "Vaegiran Battle Axe", [("bb_serbian_one_handed_battle_axe_a",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,  557 , weight(1.6)|difficulty(4)|spd_rtng(99) | weapon_length(68)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2]],
["mod_onehandaxe4", "Nordic Footman Axe", [("bb_slavic_axe_1",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,  357 , weight(1.8)|difficulty(3)|spd_rtng(102) | weapon_length(62)|swing_damage(29 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_4]],
["mod_cavalry_axe1", "Cavalry Axe", [("bb_slavic_cavalry_axe_1",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,  457 , weight(1.9)|difficulty(4)|spd_rtng(101) | weapon_length(75)|swing_damage(32 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe ],
["military_sickle_a", "Military Sickle", [("military_sickle_a",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip, 220 , weight(1.0)|difficulty(9)|spd_rtng(100) | weapon_length(75)|swing_damage(26 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_5]],

########## Two-handed ##########
["axe",                 "Axe", [("iron_ax",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 65 , weight(4)|difficulty(10)|spd_rtng(91) | weapon_length(108)|swing_damage(32 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["voulge1",         "Voulge", [("voulge",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 129 , weight(4.5)|difficulty(11)|spd_rtng(87) | weapon_length(119)|swing_damage(35 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["battle_axe",         "Battle Axe", [("battle_ax",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 240 , weight(5)|difficulty(12)|spd_rtng(88) | weapon_length(108)|swing_damage(41 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["war_axe",         "War Axe", [("war_ax",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 264 , weight(5)|difficulty(12)|spd_rtng(86) | weapon_length(110)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["two_handed_battle_axe_2",         "Two-handed War Axe", [("two_handed_battle_axe_b",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 152 , weight(4.5)|difficulty(12)|spd_rtng(96) | weapon_length(92)|swing_damage(44 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_4, fac_kingdom_5]],
["shortened_voulge",         "Shortened Voulge", [("two_handed_battle_axe_c",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 228 , weight(4.5)|difficulty(12)|spd_rtng(92) | weapon_length(100)|swing_damage(45 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2]],
["great_axe",         "Great Axe", [("two_handed_battle_axe_e",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 316 , weight(4.5)|difficulty(12)|spd_rtng(94) | weapon_length(96)|swing_damage(47 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],
["long_axe",         "Long Axe", [("long_axe_a",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_next_item_as_melee|itp_unbalanced|itp_merchandise,itc_staff|itcf_carry_axe_back, 390 , weight(4.75)|difficulty(12)|spd_rtng(93) | weapon_length(120)|swing_damage(46 , cut) | thrust_damage(19 ,  blunt),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],
["long_axe_alt",         "Long Axe", [("long_axe_a",0)],itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 390 , weight(4.75)|difficulty(12)|spd_rtng(88) | weapon_length(120)|swing_damage(46 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],
["long_axe_b",         "Long War Axe", [("long_axe_b",0)], itp_type_polearm| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_next_item_as_melee|itp_unbalanced|itp_merchandise, itc_staff|itcf_carry_axe_back, 510 , weight(5.0)|difficulty(13)|spd_rtng(92) | weapon_length(125)|swing_damage(50 , cut) | thrust_damage(18 ,  blunt),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],
["long_axe_b_alt",         "Long War Axe", [("long_axe_b",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 510 , weight(5.0)|difficulty(13)|spd_rtng(87) | weapon_length(125)|swing_damage(50 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],
["long_axe_c",         "Great Long Axe", [("long_axe_c",0)], itp_type_polearm| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_next_item_as_melee|itp_unbalanced|itp_merchandise, itc_staff|itcf_carry_axe_back, 660 , weight(5.5)|difficulty(13)|spd_rtng(91) | weapon_length(127)|swing_damage(54 , cut) | thrust_damage(19 ,  blunt),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],
["long_axe_c_alt",      "Great Long Axe", [("long_axe_c",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 660 , weight(5.5)|difficulty(13)|spd_rtng(85) | weapon_length(127)|swing_damage(54 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],
["bardiche",         "Bardiche", [("two_handed_battle_axe_d",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 291 , weight(4.75)|difficulty(13)|spd_rtng(91) | weapon_length(102)|swing_damage(47 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2]],
["great_bardiche",         "Great Bardiche", [("two_handed_battle_axe_f",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 617 , weight(5.0)|difficulty(14)|spd_rtng(89) | weapon_length(116)|swing_damage(50 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2]],
["voulge",         "Voulge", [("two_handed_battle_long_axe_a",0)], itp_type_polearm|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_staff, 120 , weight(3.0)|difficulty(10)|spd_rtng(88) | weapon_length(175)|swing_damage(40 , cut) | thrust_damage(18 ,  pierce),imodbits_axe ],
["long_bardiche",         "Long Bardiche", [("two_handed_battle_long_axe_b",0)], itp_type_polearm|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_staff, 390 , weight(4.75)|difficulty(12)|spd_rtng(89) | weapon_length(140)|swing_damage(48 , cut) | thrust_damage(17 ,  pierce),imodbits_axe ],
["great_long_bardiche",         "Great Long Bardiche", [("two_handed_battle_long_axe_c",0)], itp_type_polearm|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_staff, 660 , weight(5.0)|difficulty(13)|spd_rtng(88) | weapon_length(155)|swing_damage(50 , cut) | thrust_damage(17 ,  pierce),imodbits_axe ],
["poleaxe",         "Poleaxe", [("pole_ax",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_two_handed|itp_wooden_parry, itc_staff, 384 , weight(4.5)|difficulty(13)|spd_rtng(77) | weapon_length(180)|swing_damage(50 , cut) | thrust_damage(15 ,  blunt),imodbits_polearm, [], [fac_kingdom_1]],
["mod_two_handed_taxe_1", "Dohaken War Axe", [("axe_1",0)], itp_type_polearm|itp_offset_lance|itp_primary|itp_bonus_against_shield|itp_two_handed|itp_wooden_parry|itp_wooden_parry, itc_staff|itcf_carry_axe_back, 280 , weight(2.50)|difficulty(10)|spd_rtng(87) | weapon_length(145)|swing_damage(39 , pierce) | thrust_damage(32 ,  pierce),imodbits_axe ],
["mod_onehand_taxe3", "Dohaken Battle Axe", [("axe_2",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,  397 , weight(1.4)|difficulty(4)|spd_rtng(99) | weapon_length(55)|swing_damage(32 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["mod_tpoleaxe",  "Poleaxe of The Order", [("weapon_1",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_two_handed|itp_wooden_parry, itc_staff, 384 , weight(4.3)|difficulty(13)|spd_rtng(78) | weapon_length(190)|swing_damage(48 , cut) | thrust_damage(24 ,  blunt),imodbits_polearm, [], [fac_player_supporters_faction]],
["two_handed_axe",         "One-handed Axe", [("two_handed_battle_axe_a",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 90 , weight(4.5)|difficulty(12)|spd_rtng(96) | weapon_length(90)|swing_damage(35 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_2, fac_kingdom_4]],


###########################
##### MACES AND CLUBS #####
###########################


########## One-handed ##########
["wooden_stick",         "Wooden Stick", [("wooden_stick",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 4 , weight(2.5)|difficulty(0)|spd_rtng(99) | weapon_length(63)|swing_damage(13 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["cudgel",         "Cudgel", [("club",0)], itp_type_one_handed_wpn|itp_merchandise| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 4 , weight(2.5)|difficulty(0)|spd_rtng(99) | weapon_length(70)|swing_damage(13 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["hammer",         "Hammer", [("iron_hammer_new",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar, 7 , weight(2)|difficulty(0)|spd_rtng(100) | weapon_length(55)|swing_damage(24 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["club",         "Club", [("club",0)], itp_type_one_handed_wpn|itp_merchandise| itp_can_knock_down|itp_primary|itp_wooden_parry|itp_wooden_attack, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(98) | weapon_length(70)|swing_damage(20 , blunt) | thrust_damage(0 ,  pierce),imodbits_none ],
["winged_mace",         "Flanged Mace", [("flanged_mace",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 122 , weight(3.5)|difficulty(2)|spd_rtng(103) | weapon_length(70)|swing_damage(24 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["spiked_mace",         "Spiked Mace", [("spiked_mace_new",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 180 , weight(3.5)|difficulty(2)|spd_rtng(98) | weapon_length(70)|swing_damage(28 , blunt) | thrust_damage(0 ,  pierce),imodbits_pick ],
["military_hammer", "Military Hammer", [("military_hammer",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 317 , weight(2)|difficulty(0)|spd_rtng(95) | weapon_length(70)|swing_damage(31 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace, [], [fac_kingdom_5]],
["pickaxe",         "Pickaxe", [("fighting_pick_new",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 27 , weight(3)|difficulty(2)|spd_rtng(99) | weapon_length(70)|swing_damage(19 , pierce) | thrust_damage(0 ,  pierce),imodbits_pick ],
["spiked_club",         "Spiked Club", [("spiked_club",0)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 83 , weight(3)|difficulty(2)|spd_rtng(97) | weapon_length(70)|swing_damage(21 , pierce) | thrust_damage(0 ,  pierce),imodbits_mace ],
["fighting_pick", "Fighting Pick", [("fighting_pick_new",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 108 , weight(1.0)|difficulty(1)|spd_rtng(98) | weapon_length(70)|swing_damage(22 , pierce) | thrust_damage(0 ,  pierce),imodbits_pick ],
["military_pick", "Military Pick", [("steel_pick_new",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 280 , weight(1.5)|difficulty(1)|spd_rtng(97) | weapon_length(70)|swing_damage(31 , pierce) | thrust_damage(0 ,  pierce),imodbits_pick ],
["mace_1",         "Spiked Club", [("mace_d",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 45 , weight(1.5)|difficulty(3)|spd_rtng(99) | weapon_length(70)|swing_damage(19 , pierce) | thrust_damage(0 ,  pierce),imodbits_mace, [], [fac_kingdom_1, fac_kingdom_2, fac_kingdom_5]],
["mace_2",         "Knobbed_Mace", [("mace_a",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 98 , weight(2.5)|difficulty(3)|spd_rtng(98) | weapon_length(70)|swing_damage(21 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace, [], [fac_kingdom_1, fac_kingdom_2, fac_kingdom_5]],
["mace_3",         "Spiked Mace", [("mace_c",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 152 , weight(2.75)|difficulty(3)|spd_rtng(98) | weapon_length(70)|swing_damage(23 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace, [], [fac_kingdom_1, fac_kingdom_2, fac_kingdom_5]],
["mace_4",         "Winged_Mace", [("mace_b",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 212 , weight(2.75)|difficulty(3)|spd_rtng(98) | weapon_length(70)|swing_damage(24 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["knobbed_mace1",  "Round Knobbed Mace", [("bb_serbian_knobbed_mace_1",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,  325 , weight(1.2)|difficulty(2)|spd_rtng(102) | weapon_length(68)|swing_damage(24 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["knobbed_mace2",  "Flanged Mace", [("bb_serbian_knobbed_mace_2",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,  352 , weight(1.3)|difficulty(2)|spd_rtng(101) | weapon_length(70)|swing_damage(25 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["knobbed_mace3",  "Flanged Mace", [("bb_serbian_knobbed_mace_3",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,  394 , weight(1.2)|difficulty(2)|spd_rtng(103) | weapon_length(67)|swing_damage(27 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["flanged_mace1",  "Flanged Steel Mace", [("bb_serbian_flanged_mace_1",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary, itc_scimitar|itcf_carry_mace_left_hip,  782 , weight(1.9)|difficulty(2)|spd_rtng(94) | weapon_length(65)|swing_damage(31 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["faradon_warhammer",  "Exiled Warhammer", [("faradon_warhammer",0)],  itp_type_one_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_wooden_parry, itc_longsword|itcf_carry_sword_left_hip, 200 , weight(1.5)|difficulty(3)|spd_rtng(115) | weapon_length(73)|swing_damage(25 , blunt) | thrust_damage(17 ,  pierce),imodbits_mace ],
["faradon_mace",  "War Mace", [("faradon_iberianmace",0)],  itp_type_one_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_wooden_parry, itc_longsword|itcf_carry_sword_left_hip, 200 , weight(1.4)|difficulty(3)|spd_rtng(114) | weapon_length(66)|swing_damage(25 , blunt)| thrust_damage(15, pierce) ,imodbits_mace ],
["faradon_club",  "War Club", [("faradon_largeclub",0)],  itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry, itc_longsword|itcf_carry_sword_left_hip, 200 , weight(1.3)|difficulty(3)|spd_rtng(115) | weapon_length(87)|swing_damage(24 , blunt)| thrust_damage(18, blunt) ,imodbits_mace ],
["faradon_iron_club",  "Iron War Club", [("faradon_ironclub",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip,  558 , weight(1.3)|difficulty(2)|spd_rtng(105) | weapon_length(85)|swing_damage(30 , blunt)| thrust_damage(24, blunt) ,imodbits_sword_high ],

["long_spiked_club",         "Long Spiked Club", [("mace_long_c",0)], itp_type_one_handed_wpn|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_morningstar|itcf_carry_axe_back, 264 , weight(3)|difficulty(4)|spd_rtng(90) | weapon_length(108)|swing_damage(16 , blunt) | thrust_damage(13 ,  blunt),imodbits_mace ],
["sarranid_mace_1",         "Iron Mace", [("mace_small_d",0)], itp_type_one_handed_wpn|itp_merchandise|itp_can_knock_down |itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 45 , weight(2.0)|difficulty(2)|spd_rtng(99) | weapon_length(73)|swing_damage(22 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],



########## Two-handed ##########

["staff",         "Staff", [("wooden_staff",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_horseback_slashright_onehanded|itcf_carry_sword_back, 36 , weight(1.5)|difficulty(2)|spd_rtng(104) | weapon_length(130)|swing_damage(18 , blunt) | thrust_damage(19 ,  blunt),imodbits_polearm ],
["quarter_staff", "Quarter Staff", [("quarter_staff",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry|itp_wooden_attack, itc_staff|itcf_horseback_slashright_onehanded|itcf_carry_sword_back, 60 , weight(2)|difficulty(3)|spd_rtng(100) | weapon_length(140)|swing_damage(25 , blunt) | thrust_damage(20 ,  blunt),imodbits_polearm ],
["iron_staff",         "Iron Staff", [("iron_staff",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary, itc_staff|itcf_horseback_slashright_onehanded|itcf_carry_sword_back, 202 , weight(2.8)|difficulty(4)|spd_rtng(95) | weapon_length(140)|swing_damage(28 , blunt) | thrust_damage(26 ,  blunt),imodbits_polearm ],
["club_with_spike_head",  "Goedendag", [("mace_e",0)],  itp_type_two_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_wooden_parry, itc_bastardsword|itcf_carry_axe_back, 200 , weight(2.80)|difficulty(9)|spd_rtng(95) | weapon_length(117)|swing_damage(24 , blunt) | thrust_damage(20 ,  pierce),imodbits_mace ],
["maul",         "Maul", [("maul_b",0)], itp_crush_through|itp_type_two_handed_wpn|itp_merchandise|itp_can_knock_down |itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_unbalanced, itc_nodachi|itcf_carry_spear, 97 , weight(6)|difficulty(15)|spd_rtng(83) | weapon_length(79)|swing_damage(36 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["sledgehammer", "Sledgehammer", [("maul_c",0)], itp_crush_through|itp_type_two_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_unbalanced, itc_nodachi|itcf_carry_spear, 101 , weight(7)|difficulty(16)|spd_rtng(81) | weapon_length(82)|swing_damage(39, blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["warhammer",         "Great Hammer", [("maul_d",0)], itp_crush_through|itp_type_two_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_unbalanced, itc_nodachi|itcf_carry_spear, 290 , weight(9)|difficulty(17)|spd_rtng(79) | weapon_length(75)|swing_damage(45 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["morningstar",         "Morningstar", [("mace_morningstar_new",0)], itp_crush_through|itp_type_two_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry|itp_unbalanced, itc_morningstar|itcf_carry_mace_left_hip, 305 , weight(4.5)|difficulty(13)|spd_rtng(95) | weapon_length(85)|swing_damage(38 , pierce) | thrust_damage(0 ,  pierce),imodbits_mace ],
["long_hafted_knobbed_mace",         "Long-hafted Knobbed Mace", [("mace_long_a",0)], itp_type_polearm| itp_can_knock_down|itp_primary|itp_wooden_parry, itc_staff|itcf_carry_axe_back, 324 , weight(3)|difficulty(4)|spd_rtng(95) | weapon_length(133)|swing_damage(26 , blunt) | thrust_damage(23 ,  blunt),imodbits_mace, [], [fac_kingdom_1, fac_kingdom_2, fac_kingdom_5]],
["long_hafted_spiked_mace",         "Long-hafted Spiked Mace", [("mace_long_b",0)], itp_type_polearm|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff|itcf_carry_axe_back, 310 , weight(3)|difficulty(4)|spd_rtng(94) | weapon_length(140)|swing_damage(28 , blunt) | thrust_damage(26 ,  blunt),imodbits_mace, [], [fac_kingdom_1, fac_kingdom_2, fac_kingdom_5]],
["sarranid_two_handed_mace_1",         "Sarranid War Mace", [("mace_long_d",0)], itp_type_two_handed_wpn|itp_can_knock_down|itp_merchandise|itp_primary|itp_crush_through|itp_unbalanced, itc_morningstar|itcf_carry_axe_back,470 , weight(4.5)|difficulty(9)|spd_rtng(85) | weapon_length(95)|swing_damage(35 , blunt) | thrust_damage(22 ,  blunt),imodbits_mace, [], [fac_kingdom_6]],
["polehammer",         "Polehammer", [("pole_hammer",0)], itp_type_polearm|itp_offset_lance| itp_primary|itp_two_handed|itp_wooden_parry, itc_staff, 169 , weight(7)|difficulty(18)|spd_rtng(50) | weapon_length(126)|swing_damage(50 , blunt) | thrust_damage(35 ,  blunt),imodbits_polearm ],
["bec_de_corbin_a",  "War Hammer", [("bec_de_corbin_a",0)], itp_type_polearm|itp_merchandise| itp_cant_use_on_horseback|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed,itcf_carry_spear, 125 , weight(3.0)|difficulty(4)|spd_rtng(91) | weapon_length(135)|swing_damage(38, blunt) | thrust_damage(38 ,  pierce),imodbits_polearm ],
["staghammer",         "Staghammer", [("staghammer",0)], itp_type_polearm|itp_can_knock_down|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff|itcf_carry_axe_back, 310 , weight(7)|difficulty(12)|spd_rtng(92) | weapon_length(175)|swing_damage(35 , blunt) | thrust_damage(22 ,  pierce),imodbits_mace, [], [fac_player_supporters_faction] ],

####################
##### POLEARMS #####
####################

########## Spears ##########

["cutting_spear", "Cutting Spear", [("crusader_spear_a",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff|itcf_carry_spear, 102, weight(2.25)|difficulty(8)|spd_rtng(105)|weapon_length(190)|swing_damage(31,cut)|thrust_damage(24,pierce), imodbits_polearm, [], [fac_kingdom_1,fac_kingdom_2] ],
["peasant_spear", "Peasant Spear", [("crusader_spear_b",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff|itcf_carry_spear, 75, weight(2.25)|difficulty(8)|spd_rtng(108)|weapon_length(190)|swing_damage(24,cut)|thrust_damage(21,pierce), imodbits_polearm, [], [fac_kingdom_1,fac_kingdom_2] ],
["infantry_spear", "Infantry Spear", [("crusader_spear_c",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff|itcf_carry_spear, 105, weight(2.25)|difficulty(8)|spd_rtng(107)|weapon_length(190)|swing_damage(16,blunt)|thrust_damage(31,pierce), imodbits_polearm, [], [fac_kingdom_1,fac_kingdom_2] ],
["trident_spear", "Triden Spear", [("mameluk_spears_a",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff|itcf_carry_spear, 150, weight(2.25)|difficulty(8)|spd_rtng(106)|weapon_length(190)|swing_damage(24,blunt)|thrust_damage(27,pierce), imodbits_polearm, [], [fac_kingdom_1,fac_kingdom_2] ],
["winged_spear", "Winged Spear", [("mameluk_spears_b",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff|itcf_carry_spear, 175, weight(2.25)|difficulty(8)|spd_rtng(109)|weapon_length(190)|swing_damage(17,cut)|thrust_damage(31, pierce), imodbits_polearm, [], [fac_kingdom_1,fac_kingdom_2] ],


["scythe",         "Scythe", [("scythe",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear, 43 , weight(2)|difficulty(0)|spd_rtng(97) | weapon_length(182)|swing_damage(30 , cut) | thrust_damage(14 ,  pierce),imodbits_polearm ],
["pitch_fork",         "Pitch Fork", [("pitch_fork",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry,itc_staff, 19 , weight(1.5)|difficulty(0)|spd_rtng(87) | weapon_length(154)|swing_damage(16 , blunt) | thrust_damage(22 ,  pierce),imodbits_polearm ],
["military_fork", "Military Fork", [("military_fork",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry,itc_staff, 153 , weight(2)|difficulty(0)|spd_rtng(95) | weapon_length(135)|swing_damage(15 , blunt) | thrust_damage(30 ,  pierce),imodbits_polearm ],
["battle_fork",         "Battle Fork", [("battle_fork",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry,itc_staff, 282 , weight(2.2)|difficulty(0)|spd_rtng(90) | weapon_length(144)|swing_damage(15, blunt) | thrust_damage(35 ,  pierce),imodbits_polearm ],
["boar_spear",         "Boar Spear", [("spear",0)], itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry,itc_staff|itcf_carry_spear, 76 , weight(1.5)|difficulty(3)|spd_rtng(110) | weapon_length(157)|swing_damage(26 , cut) | thrust_damage(23 ,  pierce),imodbits_polearm ],
["shortened_spear",         "Shortened Spear", [("spear_g_1-9m",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff|itcf_carry_spear, 53 , weight(2.0)|difficulty(2)|spd_rtng(122) | weapon_length(120)|swing_damage(19 , blunt) | thrust_damage(25 ,  pierce),imodbits_polearm ],
["spear",         "Spear", [("spear_h_2-15m",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff|itcf_carry_spear, 85 , weight(2.25)|difficulty(2)|spd_rtng(98) | weapon_length(135)|swing_damage(20 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_2]],
["bamboo_spear",         "Bamboo Spear", [("arabian_spear_a_3m",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear, 80 , weight(2.0)|difficulty(2)|spd_rtng(88) | weapon_length(200)|swing_damage(15 , blunt) | thrust_damage(20 ,  pierce),imodbits_polearm ],
["war_spear",         "War Spear", [("spear_i_2-3m",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff|itcf_carry_spear, 140 , weight(2.5)|difficulty(3)|spd_rtng(115) | weapon_length(150)|swing_damage(20 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["mod_hookedspear1", "Hooked Spear", [("bb_serbian_hooked_spear_1",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  495 , weight(2.5)|difficulty(4)|spd_rtng(96) | weapon_length(132)|swing_damage(28, pierce) | thrust_damage(26 ,  pierce),imodbits_polearm ],
["mod_hookedspear2", "Hooked Spear", [("bb_serbian_hooked_spear_2",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  485 , weight(2.4)|difficulty(4)|spd_rtng(95) | weapon_length(130)|swing_damage(27, pierce) | thrust_damage(25 ,  pierce),imodbits_polearm ],

########## Pikes #########

["pike",         "Pike", [("spear_a_3m",0)], itp_type_polearm|itp_merchandise| itp_cant_use_on_horseback|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed, itc_cutting_spear, 125 , weight(3.0)|difficulty(4)|spd_rtng(107) | weapon_length(245)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm, [], [fac_kingdom_2, fac_kingdom_5]],
["ashwood_pike", "Ashwood Pike", [("pike",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_two_handed|itp_wooden_parry, itc_cutting_spear, 205 , weight(3.5)|difficulty(9)|spd_rtng(90) | weapon_length(170)|swing_damage(19 , blunt) | thrust_damage(29,  pierce),imodbits_polearm, [], [fac_kingdom_2]],
["mod_pike1", "Heavy Pike", [("bb_rus_pike",0)], itp_type_polearm|itp_cant_use_on_horseback|itp_offset_lance|itp_merchandise|itp_primary|itp_two_handed|itp_wooden_parry|itp_cant_use_on_horseback, itc_staff,  582 , weight(4.5)|difficulty(7)|spd_rtng(105) | weapon_length(250)|swing_damage(21, cut) | thrust_damage(22 ,  pierce),imodbits_polearm, [], [fac_kingdom_2]],
["mercenary_pike_a", "Mercenary Pike", [("pike1",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_offset_lance, itc_staff, 582, weight(6)|difficulty(12)|spd_rtng(100)|weapon_length(430)|swing_damage(25,blunt)|thrust_damage(29,pierce), imodbits_polearm, [], [fac_kingdom_2] ],
["mercenary_pike_b", "Mercenary Pike", [("pike2",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_offset_lance, itc_staff, 582, weight(6)|difficulty(12)|spd_rtng(100)|weapon_length(430)|swing_damage(25,blunt)|thrust_damage(29,pierce), imodbits_polearm, [], [fac_kingdom_2] ],

########## Lances ##########
["simple_lance", "Simple Lance", [("crusader_knight_spear_a",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear, 450, weight(2.5)|difficulty(10)|spd_rtng(90)|weapon_length(260)|swing_damage(21,blunt)|thrust_damage(25,pierce), imodbits_polearm ],
["eastern_lance", "Eastern Lance", [("mameluk_spears_c",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear, 450, weight(2.5)|difficulty(10)|spd_rtng(90)|weapon_length(260)|swing_damage(21,blunt)|thrust_damage(25,pierce), imodbits_polearm ],


["jousting_lance", "Jousting Lance", [("joust_of_peace",0)], itp_couchable|itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance, 158 , weight(5)|difficulty(0)|spd_rtng(61) | weapon_length(240)|swing_damage(0 , cut) | thrust_damage(17 ,  blunt),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_5]],
["double_sided_lance", "Double Sided Lance", [("lance_dblhead",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff, 261 , weight(4.0)|difficulty(0)|spd_rtng(95) | weapon_length(128)|swing_damage(25, cut) | thrust_damage(27 ,  pierce),imodbits_polearm ],
["light_lance",         "Light Lance", [("spear_b_2-75m",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 180 , weight(2.5)|difficulty(3)|spd_rtng(85) | weapon_length(175)|swing_damage(16 , blunt) | thrust_damage(27 ,  pierce),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_3]],
["lance",         "Lance", [("spear_d_2-8m",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 270 , weight(2.5)|difficulty(3)|spd_rtng(80) | weapon_length(180)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_3, fac_kingdom_6]],
["heavy_lance",         "Heavy Lance", [("spear_f_2-9m",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear, 360 , weight(2.75)|difficulty(10)|spd_rtng(75) | weapon_length(190)|swing_damage(16 , blunt) | thrust_damage(26 ,  pierce),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_3, fac_kingdom_6]],
["great_lance",         "Great Lance", [("heavy_lance",0)], itp_couchable|itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance,  410 , weight(5)|difficulty(11)|spd_rtng(55) | weapon_length(240)|swing_damage(0 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm, [], [fac_kingdom_1]],
["mod_lance1", "Vaegiran Lance", [("bb_serbian_lance",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  565 , weight(3.2)|difficulty(3)|spd_rtng(93) | weapon_length(200)|swing_damage(23, cut) | thrust_damage(26 ,  pierce),imodbits_polearm, [], [fac_kingdom_2]],
["mod_lance2", "Vaegiran Lance", [("bb_rus_lance",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  475 , weight(4.0)|difficulty(6)|spd_rtng(91) | weapon_length(189)|swing_damage(21, cut) | thrust_damage(21 ,  pierce),imodbits_polearm, [], [fac_kingdom_2]],
["mod_tlance1", "Great Black & White Lance", [("lance_1",0)], itp_couchable|itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance,  410 , weight(5)|difficulty(11)|spd_rtng(55) | weapon_length(230)|swing_damage(0 , cut) | thrust_damage(23 ,  pierce),imodbits_polearm, [], [fac_kingdom_1]],
["mod_tlance2", "Great Brown & Black Lance", [("lance_2",0)], itp_couchable|itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance,  410 , weight(5)|difficulty(11)|spd_rtng(55) | weapon_length(230)|swing_damage(0 , cut) | thrust_damage(23 ,  pierce),imodbits_polearm, [], [fac_kingdom_1]],
["mod_tlance3", "Great Red & White Lance", [("lance_3",0)], itp_couchable|itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance,  410 , weight(5)|difficulty(11)|spd_rtng(55) | weapon_length(230)|swing_damage(0 , cut) | thrust_damage(23 ,  pierce),imodbits_polearm, [], [fac_kingdom_1]],
["mod_tlance4", "Great Painted Lance", [("lance_4",0)], itp_couchable|itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance,  410 , weight(5)|difficulty(11)|spd_rtng(55) | weapon_length(230)|swing_damage(0 , cut) | thrust_damage(23 ,  pierce),imodbits_polearm, [], [fac_kingdom_1]],
["mod_tlance5", "Great Painted Lance", [("lance_5",0)], itp_couchable|itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance,  410 , weight(5)|difficulty(11)|spd_rtng(55) | weapon_length(230)|swing_damage(0 , cut) | thrust_damage(23 ,  pierce),imodbits_polearm, [], [fac_kingdom_1]],
["mod_tlance6", "Great Red & Purple Lance", [("lance_6",0)], itp_couchable|itp_type_polearm|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_greatlance,  410 , weight(5)|difficulty(11)|spd_rtng(55) | weapon_length(230)|swing_damage(0 , cut) | thrust_damage(23 ,  pierce),imodbits_polearm, [], [fac_kingdom_1]],

########## Glaives ##########
["hafted_blade_b",         "Hafted Blade", [("khergit_pike_b",0)], itp_type_polearm|itp_merchandise| itp_primary|itp_two_handed|itp_penalty_with_shield|itp_wooden_parry, itcf_carry_spear|itc_guandao, 185 , weight(2.75)|difficulty(2)|spd_rtng(95) | weapon_length(135)|swing_damage(37 , cut) | thrust_damage(20 ,  pierce),imodbits_polearm, [], [fac_kingdom_3]],
["hafted_blade_a",         "Hafted Blade", [("khergit_pike_a",0)], itp_type_polearm|itp_merchandise| itp_primary|itp_two_handed|itp_penalty_with_shield|itp_wooden_parry, itcf_carry_spear|itc_guandao, 350 , weight(3.25)|difficulty(2)|spd_rtng(93) | weapon_length(153)|swing_damage(39 , cut) | thrust_damage(19 ,  pierce),imodbits_polearm, [], [fac_kingdom_3]],
["shortened_military_scythe",         "Shortened Military Scythe", [("two_handed_battle_scythe_a",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 264 , weight(3.0)|difficulty(10)|spd_rtng(98) | weapon_length(112)|swing_damage(48 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high ],
["glaive",         "Glaive", [("glaive_b",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_two_handed|itp_wooden_parry, itc_staff|itcf_carry_spear, 352 , weight(4.5)|difficulty(5)|spd_rtng(90) | weapon_length(157)|swing_damage(39 , cut) | thrust_damage(21 ,  pierce),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_5]],
["military_scythe",         "Military Scythe", [("spear_e_2-5m",0),("spear_c_2-5m",imodbits_bad)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear, 155 , weight(2.5)|difficulty(3)|spd_rtng(90) | weapon_length(155)|swing_damage(36 , cut) | thrust_damage(25 ,  pierce),imodbits_polearm ],
["awlpike",    "Awlpike", [("awl_pike_b",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_two_handed|itp_wooden_parry, itcf_carry_spear, 345 , weight(2.25)|difficulty(3)|spd_rtng(94) | weapon_length(165)|swing_damage(25 , blunt) | thrust_damage(38 ,  pierce),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_5]],
["awlpike_long",  "Long Awlpike", [("awl_pike_a",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_two_handed|itp_wooden_parry, itc_cutting_spear| itcf_carry_spear, 385 , weight(2.25)|difficulty(3)|spd_rtng(91) | weapon_length(185)|swing_damage(30 , blunt) | thrust_damage(46 ,  pierce),imodbits_polearm, [], [fac_kingdom_5]],
["mod_guisarm1", "Long-hafted Bill-guisarme", [("luc_bill_guisarme_long_n",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  582 , weight(4.3)|difficulty(12)|spd_rtng(89) | weapon_length(212)|swing_damage(26, pierce) | thrust_damage(24 ,  pierce),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_5]],
["mod_guisarm2", "Short-hafted Bill-guisarme", [("luc_bill_guisarme_n",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  582 , weight(3.5)|difficulty(8)|spd_rtng(92) | weapon_length(177)|swing_damage(24, pierce) | thrust_damage(28 ,  pierce),imodbits_polearm, [], [fac_kingdom_1, fac_kingdom_5]],


###################
##### SHIELDS #####
###################

########## Round ##########
["wooden_shield", 					"Wooden Shield", [("shield_round_a",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  42 , weight(2)|hit_points(280)|body_armor(8)|spd_rtng(100)|shield_width(50),imodbits_shield, [], [fac_kingdom_4]],
["nordic_shield", 					"Nordic Shield", [("shield_round_b",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  95 , weight(2)|hit_points(310)|body_armor(9)|spd_rtng(100)|shield_width(50),imodbits_shield, [], [fac_kingdom_4]],
["hide_covered_round_shield", 		"Hide Covered Round Shield", [("shield_round_f",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  40 , weight(2)|hit_points(330)|body_armor(10)|spd_rtng(100)|shield_width(40),imodbits_shield ],
["leather_covered_round_shield", 	"Leather Covered Round Shield", [("shield_round_d",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  80 , weight(2.5)|hit_points(360)|body_armor(11)|spd_rtng(96)|shield_width(40),imodbits_shield ],
["plate_covered_round_shield", 		"Plate Covered Round Shield", [("shield_round_e",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  140 , weight(4)|hit_points(500)|body_armor(15)|spd_rtng(90)|shield_width(40),imodbits_shield ],
["steel_shield", 					"Steel Shield", [("shield_dragon",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  697 , weight(4)|hit_points(620)|body_armor(19)|spd_rtng(61)|shield_width(40),imodbits_shield ],
["kngiht_round_shield_a",			"Knight Round Shield", [("shield_vostoka_b",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(8)|hit_points(400)|body_armor(22)|spd_rtng(55)|shield_width(57), imodbits_shield, [], [fac_kingdom_6] ],
["kngiht_round_shield_b",			"Knight Round Shield", [("shield_vostoka_c",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(8)|hit_points(400)|body_armor(22)|spd_rtng(55)|shield_width(57), imodbits_shield, [], [fac_kingdom_6] ],


["tab_shield_round_a", 				"Old Round Shield", [("tableau_shield_round_5",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 26 , weight(2.5)|hit_points(200)|body_armor(6)|spd_rtng(93)|shield_width(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_round_shield_5", ":agent_no", ":troop_no")])]],
["tab_shield_round_b", 				"Plain Round Shield", [("tableau_shield_round_3",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 65 , weight(3)|hit_points(260)|body_armor(8)|spd_rtng(90)|shield_width(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_round_shield_3", ":agent_no", ":troop_no")])]],
["tab_shield_round_c", 				"Round Shield", [("tableau_shield_round_2",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 105 , weight(3.5)|hit_points(310)|body_armor(9)|spd_rtng(87)|shield_width(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner","tableau_round_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_round_d", 				"Heavy Round Shield", [("tableau_shield_round_1",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 210 , weight(4)|hit_points(400)|body_armor(12)|spd_rtng(84)|shield_width(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_round_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_round_e", 				"Huscarl's Round Shield", [("tableau_shield_round_4",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield, 430 , weight(4.5)|hit_points(450)|body_armor(13)|spd_rtng(81)|shield_width(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_round_shield_4", ":agent_no", ":troop_no")])]],

["tab_shield_small_round_a", 		"Plain Cavalry Shield", [("tableau_shield_small_round_3",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 96 , weight(2)|hit_points(160)|body_armor(8)|spd_rtng(105)|shield_width(40),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_small_round_shield_3", ":agent_no", ":troop_no")])]],
["tab_shield_small_round_b", 		"Round Cavalry Shield", [("tableau_shield_small_round_1",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 195 , weight(2.5)|hit_points(200)|body_armor(14)|spd_rtng(103)|shield_width(40),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_small_round_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_small_round_c", 		"Elite Cavalry Shield", [("tableau_shield_small_round_2",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield, 370 , weight(3)|hit_points(250)|body_armor(22)|spd_rtng(100)|shield_width(40),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_small_round_shield_2", ":agent_no", ":troop_no")])]],

["mod_wooden_shield", 				"Wooden Round Shield", [("luc_wooden_shield_y",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 42 , weight(2)|hit_points(330)|body_armor(1)|spd_rtng(100)|shield_width(50),imodbits_shield ],
["mod_wooden_shield2", 				"Wooden Round Shield", [("luc_wooden_shield_w",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 42 , weight(2)|hit_points(350)|body_armor(1)|spd_rtng(100)|shield_width(50),imodbits_shield ],
["mod_wooden_shield3", 				"Strong Covered Round Shield", [("luc_leather_covered_shield_z",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 42 , weight(2)|hit_points(375)|body_armor(1)|spd_rtng(100)|shield_width(50),imodbits_shield ],
["mod_wooden_shield4", 				"Strong Round Shield", [("luc_heavy_wooden_shield",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 42 , weight(2)|hit_points(370)|body_armor(1)|spd_rtng(100)|shield_width(50),imodbits_shield ],
["mod_wooden_shield5", 				"Covered Round Shield", [("luc_leather_covered_shield_3",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 42 , weight(2)|hit_points(340)|body_armor(1)|spd_rtng(100)|shield_width(50),imodbits_shield ],
["mod_wooden_shield6", 				"Cavalry Round Shield", [("luc_cavalry_shield_z",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 42 , weight(2)|hit_points(380)|body_armor(1)|spd_rtng(100)|shield_width(50),imodbits_shield ],

["highlander_buckler_1", 			"Highlander Buckler", 				[("s_h2",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield ,  350 , weight(3.5)|hit_points(300)|body_armor(2)|spd_rtng(100)|shield_width(60),imodbits_shield, [], [fac_kingdom_5]],
["highlander_buckler_2", 			"Highlander Buckler", 				[("s_h2_1",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield ,  350 , weight(3.5)|hit_points(300)|body_armor(2)|spd_rtng(100)|shield_width(60),imodbits_shield, [], [fac_kingdom_5]],
["highlander_buckler_3", 			"Highlander Buckler", 				[("s_h2_2",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield ,  350 , weight(3.5)|hit_points(300)|body_armor(2)|spd_rtng(100)|shield_width(60),imodbits_shield, [], [fac_kingdom_5]],
["spiked_highlander_buckler_1", 	"Spiked Highlander Buckler", 		[("s_h1",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield ,  450 , weight(4)|hit_points(400)|body_armor(5)|spd_rtng(100)|shield_width(60),imodbits_shield, [], [fac_kingdom_5]],
["spiked_highlander_buckler_2", 	"Spiked Highlander Buckler", 		[("s_h1_1",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield ,  450 , weight(4)|hit_points(400)|body_armor(5)|spd_rtng(100)|shield_width(60),imodbits_shield, [], [fac_kingdom_5]],
["spiked_highlander_buckler_3", 	"Spiked Highlander Buckler", 		[("s_h1_2",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_round_shield ,  450 , weight(4)|hit_points(400)|body_armor(5)|spd_rtng(100)|shield_width(60),imodbits_shield, [], [fac_kingdom_5]],
["dec_steel_shield", 				"Decorated Steel Shield", 			[("dec_steel_shield",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  2125 , weight(4)|hit_points(550)|body_armor(21)|spd_rtng(61)|shield_width(40),imodbits_shield, [], [fac_kingdom_6]],

["brass_shield1", 					"Decorated Brass Shield", 			[("brass_shield1",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  697 , weight(4)|hit_points(300)|body_armor(17)|spd_rtng(61)|shield_width(40),imodbits_shield, [], [fac_kingdom_6]],
["brass_shield", 					"Decorated Brass Shield", 			[("brass_shield",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  697 , weight(4)|hit_points(300)|body_armor(17)|spd_rtng(61)|shield_width(40),imodbits_shield, [], [fac_kingdom_6]],
["painted_brass_shield", 			"Painted Brass Shield", 			[("brass_shield2",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  697 , weight(4)|hit_points(300)|body_armor(17)|spd_rtng(61)|shield_width(40),imodbits_shield, [], [fac_kingdom_6]],
["painted_brass_shield1", 			"Painted Brass Shield", 			[("brass_shield3",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  697 , weight(4)|hit_points(350)|body_armor(17)|spd_rtng(61)|shield_width(40),imodbits_shield, [], [fac_kingdom_6]],
["painted_brass_shield5", 			"Painted Brass Shield", 			[("brass_shield7",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield,  697 , weight(4)|hit_points(400)|body_armor(17)|spd_rtng(61)|shield_width(40),imodbits_shield, [], [fac_kingdom_6]],

["sarranid_shield_a", "Sarranid Shield", [("saracin_shield_b",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(5)|hit_points(400)|body_armor(19)|spd_rtng(58)|shield_width(50), imodbits_shield, [], [fac_kingdom_6] ],
["sarranid_shield_b", "Sarranid Shield", [("saracin_shield_f",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(5)|hit_points(400)|body_armor(19)|spd_rtng(58)|shield_width(50), imodbits_shield, [], [fac_kingdom_6] ],
["sarranid_shield_c", "Sarranid Shield", [("saracin_shield_m",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(5)|hit_points(400)|body_armor(19)|spd_rtng(58)|shield_width(50), imodbits_shield, [], [fac_kingdom_6] ],
["sarranid_shield_d", "Sarranid Shield", [("saracin_shield_n",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(5)|hit_points(400)|body_armor(19)|spd_rtng(58)|shield_width(50), imodbits_shield, [], [fac_kingdom_6] ],
["sarranid_round_shield_a", "Sarranid Round Shield", [("saracin_shield_y",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(8)|hit_points(300)|body_armor(20)|spd_rtng(62)|shield_width(52), imodbits_shield, [], [fac_kingdom_6] ],
["sarranid_round_shield_b", "Sarranid Round Shield", [("saracin_shield_v",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(8)|hit_points(300)|body_armor(20)|spd_rtng(62)|shield_width(52), imodbits_shield, [], [fac_kingdom_6] ],
["sarranid_round_shield_c", "Sarranid Round Shield", [("saracin_shield_w",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(8)|hit_points(300)|body_armor(20)|spd_rtng(62)|shield_width(52), imodbits_shield, [], [fac_kingdom_6] ],
["sarranid_round_shield_d", "Sarranid Round Shield", [("shield_vostoka_a",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 850, weight(8)|hit_points(400)|body_armor(22)|spd_rtng(55)|shield_width(57), imodbits_shield, [], [fac_kingdom_6] ],


########## Heater ##########

["shield_heater_c", 				"Heater Shield", [("shield_heater_c",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  277 , weight(3.5)|hit_points(340)|body_armor(10)|spd_rtng(80)|shield_width(50),imodbits_shield ],
["tab_shield_heater_a", 			"Old Heater Shield",   [("tableau_shield_heater_1" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 36 , weight(2)|hit_points(160)|body_armor(6)|spd_rtng(96)|shield_width(36)|shield_height(70),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_heater_b", 			"Plain Heater Shield",   [("tableau_shield_heater_1" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 74 , weight(2.5)|hit_points(210)|body_armor(11)|spd_rtng(93)|shield_width(36)|shield_height(70),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_heater_c", 			"Heater Shield",   [("tableau_shield_heater_1" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 160 , weight(3)|hit_points(260)|body_armor(14)|spd_rtng(90)|shield_width(36)|shield_height(70),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_heater_d", 			"Heavy Heater Shield",   [("tableau_shield_heater_1" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 332 , weight(3.5)|hit_points(305)|body_armor(19)|spd_rtng(87)|shield_width(36)|shield_height(70),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_heater_cav_a", 		"Horseman's Heater Shield",   [("tableau_shield_heater_2" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 229 , weight(2)|hit_points(160)|body_armor(16)|spd_rtng(103)|shield_width(30)|shield_height(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_heater_cav_b", 		"Knightly Heater Shield",   [("tableau_shield_heater_2" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 390 , weight(2.5)|hit_points(220)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heater_shield_2", ":agent_no", ":troop_no")])]],

["steel_shield_heater", 			"Steel Heater Shield", 				[("steel_heater1",0)], itp_merchandise|itp_type_shield, itcf_carry_kite_shield,  1290 , weight(4)|hit_points(450)|body_armor(17)|spd_rtng(61)|shield_width(40)|shield_height(50),imodbits_shield ],

########## Kite ##########

["fur_covered_shield",  			"Fur Covered Shield", [("shield_kite_m",0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  227 , weight(3.5)|hit_points(400)|body_armor(12)|spd_rtng(76)|shield_width(81),imodbits_shield ],
["norman_shield_1",         		"Kite Shield", [("norman_shield_1",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(280)|body_armor(8)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["norman_shield_2",         		"Kite Shield", [("norman_shield_2",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(280)|body_armor(8)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["norman_shield_3",         		"Kite Shield", [("norman_shield_3",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(280)|body_armor(8)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["norman_shield_4",         		"Kite Shield", [("norman_shield_4",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(280)|body_armor(8)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["norman_shield_5",         		"Kite Shield", [("norman_shield_5",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(280)|body_armor(8)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["norman_shield_6",         		"Kite Shield", [("norman_shield_6",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(280)|body_armor(8)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["norman_shield_7",         		"Kite Shield", [("norman_shield_7",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(280)|body_armor(8)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["norman_shield_8",         		"Kite Shield", [("norman_shield_8",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  118 , weight(2.5)|hit_points(280)|body_armor(8)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["tab_shield_kite_a", 				"Old Kite Shield",   [("tableau_shield_kite_1" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 33 , weight(2)|hit_points(165)|body_armor(5)|spd_rtng(96)|shield_width(36)|shield_height(70),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_1", ":agent_no", ":troop_no")])]],
["tab_shield_kite_b", 				"Plain Kite Shield",   [("tableau_shield_kite_3" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 70 , weight(2.5)|hit_points(215)|body_armor(10)|spd_rtng(93)|shield_width(36)|shield_height(70),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_3", ":agent_no", ":troop_no")])]],
["tab_shield_kite_c", 				"Kite Shield",   [("tableau_shield_kite_2" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 156 , weight(3)|hit_points(265)|body_armor(13)|spd_rtng(90)|shield_width(36)|shield_height(70),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_kite_d", 				"Kite Shield",   [("tableau_shield_kite_2" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 320 , weight(3.5)|hit_points(310)|body_armor(18)|spd_rtng(87)|shield_width(36)|shield_height(70),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_2", ":agent_no", ":troop_no")])]],
["tab_shield_kite_cav_a", 			"Horseman's Kite Shield",   [("tableau_shield_kite_4" ,0)], itp_merchandise|itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 205 , weight(2)|hit_points(165)|body_armor(14)|spd_rtng(103)|shield_width(30)|shield_height(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_4", ":agent_no", ":troop_no")])]],
["tab_shield_kite_cav_b", 			"Knightly Kite Shield",   [("tableau_shield_kite_4" ,0)], itp_merchandise|itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_kite_shield_4", ":agent_no", ":troop_no")])]],
["tab_shield_pavise_a", 			"Old Board Shield",   [("tableau_shield_pavise_2" ,0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield, 60 , weight(3.5)|hit_points(280)|body_armor(4)|spd_rtng(89)|shield_width(43)|shield_height(100),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_pavise_shield_2", ":agent_no", ":troop_no")])], [fac_kingdom_5]],
["tab_shield_pavise_b", 			"Plain Board Shield",   [("tableau_shield_pavise_2" ,0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield, 114 , weight(4)|hit_points(360)|body_armor(8)|spd_rtng(85)|shield_width(43)|shield_height(100),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_pavise_shield_2", ":agent_no", ":troop_no")])], [fac_kingdom_5]],
["tab_shield_pavise_c", 			"Board Shield",   [("tableau_shield_pavise_1" ,0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield, 210 , weight(4.5)|hit_points(430)|body_armor(10)|spd_rtng(81)|shield_width(43)|shield_height(100),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_pavise_shield_1", ":agent_no", ":troop_no")])], [fac_kingdom_5]],
["tab_shield_pavise_d", 			"Heavy Board Shield",   [("tableau_shield_pavise_1" ,0)], itp_merchandise|itp_type_shield|itp_cant_use_on_horseback|itp_wooden_parry, itcf_carry_board_shield, 370 , weight(5)|hit_points(550)|body_armor(14)|spd_rtng(78)|shield_width(43)|shield_height(100),imodbits_shield, [(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_pavise_shield_1", ":agent_no", ":troop_no")])], [fac_kingdom_5]],

["teutonic_knight_shield1", 		"Teutonic Knight Shield",   [("shield_2" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield2", 		"Teutonic Knight Shield",   [("shield_3" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield3", 		"Teutonic Knight Shield",   [("shield_4" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield4", 		"Teutonic Knight Shield",   [("shield_5" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield5", 		"Teutonic Knight Shield",   [("shield_6" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield6", 		"Teutonic Knight Shield",   [("shield_7" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield7", 		"Teutonic Knight Shield",   [("shield_8" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield8", 		"Teutonic Knight Shield",   [("shield_9" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield9", 		"Teutonic Knight Shield",   [("shield_10" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_knight_shield10", 		"Teutonic Knight Shield",   [("shield_11" ,0)], itp_type_shield, itcf_carry_kite_shield, 360 , weight(2.5)|hit_points(225)|body_armor(23)|spd_rtng(100)|shield_width(30)|shield_height(50),imodbits_shield ],
["teutonic_kite_shield1", 			"Teutonic Kite Shield", [("kite_shield_1",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["teutonic_kite_shield2", 			"Teutonic Kite Shield", [("kite_shield_2",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["teutonic_kite_shield3", 			"Teutonic Kite Shield", [("kite_shield_3",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["teutonic_kite_shield4", 			"Teutonic Kite Shield", [("kite_shield_4",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["teutonic_kite_shield5", 			"Teutonic Kite Shield", [("kite_shield_5",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["teutonic_kite_shield6", 			"Teutonic Kite Shield", [("kite_shield_6",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["teutonic_kite_shield7", 			"Teutonic Kite Shield", [("kite_shield_7",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["teutonic_kite_shield8", 			"Teutonic Kite Shield", [("kite_shield_8",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  218 , weight(2.0)|hit_points(380)|body_armor(1)|spd_rtng(82)|shield_width(90),imodbits_shield ],
["steel_shield_kite", 				"Steel Kite Shield", 				[("steel_kite1",0)], itp_merchandise|itp_type_shield, itcf_carry_kite_shield,  1390 , weight(5.5)|hit_points(450)|body_armor(15)|spd_rtng(55)|shield_width(40)|shield_height(70),imodbits_shield ],

["knight_shield", "Knight Shield", [("shield_knight_jerusalem_a",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 1900, weight(5)|hit_points(600)|body_armor(23)|spd_rtng(52)|shield_width(40), imodbits_shield, [], [fac_kingdom_6] ],
["man-at-arms_shield_a", "Man-at-Arms Shield", [("shield_veteran_jerusalem_a",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 1500, weight(5)|hit_points(500)|body_armor(20)|spd_rtng(60)|shield_width(40), imodbits_shield, [], [fac_kingdom_6] ],
["man-at-arms_shield_b", "Man-at-Arms Shield", [("shield_veteran_jerusalem_e",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 1500, weight(5)|hit_points(500)|body_armor(20)|spd_rtng(60)|shield_width(40), imodbits_shield, [], [fac_kingdom_6] ],


########### Mercenary ##########

["blue_company_round_shield", "Blue Company Round Shield", [("shields_archer_antioh_a",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 1500, weight(4)|hit_points(400)|body_armor(17)|spd_rtng(61)|shield_width(40), imodbits_shield, [], [fac_kingdom_6] ],
["blue_company_heater_shield_a", "Blue Company Heater Shield", [("shield_knight_antioh_d",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 1800, weight(6)|hit_points(500)|body_armor(22)|spd_rtng(57)|shield_width(40), imodbits_shield, [], [fac_kingdom_6] ],
["blue_company_heatet_shield_b", "Blue Company Heater Shield", [("antioh_shield_a",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 1800, weight(5)|hit_points(500)|body_armor(20)|spd_rtng(59)|shield_width(40), imodbits_shield, [], [fac_kingdom_6] ],
["blue_company_kite_shield_a", "Blue Company Kite Shield", [("shield_veteran_antioh_b",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 1900, weight(5)|hit_points(600)|body_armor(23)|spd_rtng(52)|shield_width(40), imodbits_shield, [], [fac_kingdom_6] ],
["blue_company_kite_shield_b", "Blue Company Kite Shield", [("shield_veteran_antioh_g",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 1900, weight(5)|hit_points(600)|body_armor(23)|spd_rtng(52)|shield_width(40), imodbits_shield, [], [fac_kingdom_6] ],

["caravan_guard_shield", "Caravan Guard Shield", [("securiti_caravan_crusader_shield",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 350, weight(2.5)|hit_points(500)|body_armor(22)|spd_rtng(96)|shield_width(40), imodbits_shield ],


########### Bandit ##########

["bandit_shield_a", "Bandit Shield", [("bandit_shield_a",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 150, weight(2.5)|hit_points(400)|body_armor(15)|spd_rtng(96)|shield_width(40), imodbits_shield ],
["bandit_shield_b", "Bandit Shield", [("bandit_shield_b",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 150, weight(2.5)|hit_points(400)|body_armor(15)|spd_rtng(96)|shield_width(40), imodbits_shield ],
["bandit_shield_c", "Bandit Shield", [("bandit_shield_d",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 150, weight(2.5)|hit_points(400)|body_armor(15)|spd_rtng(96)|shield_width(40), imodbits_shield ],
["reinforced_round_shield_a", "Reinforced Round Shield", [("bandit_shield_c",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 250, weight(2.5)|hit_points(400)|body_armor(18)|spd_rtng(96)|shield_width(40), imodbits_shield ],
["reinforced_round_shield_b", "Reinforced Round Shield", [("bandit_shield_e",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 250, weight(2.5)|hit_points(400)|body_armor(18)|spd_rtng(96)|shield_width(40), imodbits_shield ],
["reinforced_round_shield_c", "Reinforced Round Shield", [("bandit_shield_f",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 250, weight(2.5)|hit_points(400)|body_armor(18)|spd_rtng(96)|shield_width(40), imodbits_shield ],

########### Musical instruments ##########

["lyre",   							"Lyre", [("lyre",0)], itp_type_shield|itp_wooden_parry|itp_civilian, itcf_carry_bow_back,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),0 ],
["lute",         					"Lute", [("lute",0)], itp_type_shield|itp_wooden_parry|itp_civilian, itcf_carry_bow_back,  118 , weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90),0 ],


##########################
##### RANGED WEAPONS #####
##########################

["stones",         "Stones", [("throwing_stone",0)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_stone, 1 , weight(4)|difficulty(0)|spd_rtng(97) | shoot_speed(30) | thrust_damage(11 ,  blunt)|max_ammo(18)|weapon_length(8),imodbit_large_bag ],
["throwing_knives", "Throwing Knives", [("throwing_knife",0)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_knife, 76 , weight(2.5)|difficulty(1)|spd_rtng(121) | shoot_speed(25) | thrust_damage(19 ,  cut)|max_ammo(14)|weapon_length(0),imodbits_thrown ],
["throwing_daggers", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_knife, 193 , weight(2.5)|difficulty(1)|spd_rtng(110) | shoot_speed(24) | thrust_damage(25 ,  cut)|max_ammo(13)|weapon_length(0),imodbits_thrown ],

########### Darts ##########

["darts",         "Darts", [("dart_b",0),("dart_b_bag", ixmesh_carry)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_javelin|itcf_carry_quiver_right_vertical|itcf_show_holster_when_drawn, 155 , weight(2)|difficulty(1)|spd_rtng(95) | shoot_speed(28) | thrust_damage(22 ,  pierce)|max_ammo(12)|weapon_length(32),imodbits_thrown ],
["war_darts",         "War Darts", [("dart_a",0),("dart_a_bag", ixmesh_carry)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 285 , weight(2)|difficulty(1)|spd_rtng(93) | shoot_speed(27) | thrust_damage(25 ,  pierce)|max_ammo(12)|weapon_length(45),imodbits_thrown ],

########### Javelins ##########

["javelin",         "Javelins", [("javelin",0),("javelins_quiver_new", ixmesh_carry)], itp_type_thrown |itp_merchandise|itp_primary|itp_next_item_as_melee ,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 300, weight(4)|difficulty(2)|spd_rtng(91) | shoot_speed(25) | thrust_damage(38 ,  pierce)|max_ammo(8)|weapon_length(75),imodbits_thrown ],
["javelin_melee",         "Javelin", [("javelin",0)], itp_type_polearm|itp_primary|itp_wooden_parry , itc_staff, 300, weight(4)|difficulty(2)|spd_rtng(95) |swing_damage(12, cut)| thrust_damage(14,  pierce)|weapon_length(75),imodbits_polearm ],

["throwing_spears",         "Throwing Spears", [("jarid_new_b",0),("jarid_new_b_bag", ixmesh_carry)], itp_type_thrown |itp_merchandise|itp_primary|itp_next_item_as_melee ,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 525 , weight(4)|difficulty(3)|spd_rtng(87) | shoot_speed(22) | thrust_damage(50 ,  pierce)|max_ammo(4)|weapon_length(65),imodbits_thrown ],
["throwing_spear_melee",         "Throwing Spear", [("jarid_new_b",0),("javelins_quiver", ixmesh_carry)],itp_type_polearm|itp_primary|itp_wooden_parry , itc_staff, 525 , weight(4)|difficulty(3)|spd_rtng(91) | swing_damage(18, cut) | thrust_damage(23 ,  pierce)|weapon_length(75),imodbits_thrown ],
["jarid",         "Jarids", [("jarid_new",0),("jarid_quiver", ixmesh_carry)], itp_type_thrown |itp_merchandise|itp_primary|itp_next_item_as_melee ,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 560 , weight(2.75)|difficulty(2)|spd_rtng(89) | shoot_speed(24) | thrust_damage(45 ,  pierce)|max_ammo(6)|weapon_length(65),imodbits_thrown ],
["jarid_melee",         "Jarid", [("jarid_new",0),("jarid_quiver", ixmesh_carry)], itp_type_polearm|itp_primary|itp_wooden_parry , itc_staff, 560 , weight(2.75)|difficulty(2)|spd_rtng(93) | swing_damage(16, cut) | thrust_damage(20 ,  pierce)|weapon_length(65),imodbits_thrown ],

########### Axes ##########

["light_throwing_axes", "Light Throwing Axes", [("francisca",0)], itp_type_thrown |itp_merchandise|itp_primary|itp_next_item_as_melee,itcf_throw_axe,360, weight(3)|difficulty(1)|spd_rtng(99) | shoot_speed(18) | thrust_damage(40,cut)|max_ammo(4)|weapon_length(53),imodbits_thrown_minus_heavy ],
["light_throwing_axes_melee", "Light Throwing Axe", [("francisca",0)], itp_type_one_handed_wpn |itp_primary|itp_bonus_against_shield,itc_scimitar,360, weight(3)|difficulty(1)|spd_rtng(99)|weapon_length(53)| swing_damage(26,cut),imodbits_thrown_minus_heavy ],
["throwing_axes", "Throwing Axes", [("throwing_axe_a",0)], itp_type_thrown |itp_merchandise|itp_primary|itp_next_item_as_melee,itcf_throw_axe,490, weight(5)|difficulty(2)|spd_rtng(98) | shoot_speed(18) | thrust_damage(45,cut)|max_ammo(4)|weapon_length(53),imodbits_thrown_minus_heavy ],
["throwing_axes_melee", "Throwing Axe", [("throwing_axe_a",0)], itp_type_one_handed_wpn |itp_primary|itp_bonus_against_shield,itc_scimitar,490, weight(5)|difficulty(2)|spd_rtng(98) | swing_damage(29,cut)|weapon_length(53),imodbits_thrown_minus_heavy ],
["heavy_throwing_axes", "Heavy Throwing Axes", [("throwing_axe_b",0)], itp_type_thrown |itp_merchandise|itp_primary|itp_next_item_as_melee,itcf_throw_axe,620, weight(7)|difficulty(4)|spd_rtng(97) | shoot_speed(18) | thrust_damage(53,cut)|max_ammo(4)|weapon_length(53),imodbits_thrown_minus_heavy ],
["heavy_throwing_axes_melee", "Heavy Throwing Axe", [("throwing_axe_b",0)], itp_type_one_handed_wpn |itp_primary|itp_bonus_against_shield,itc_scimitar,620, weight(7)|difficulty(4)|spd_rtng(97) | swing_damage(32,cut)|weapon_length(53),imodbits_thrown_minus_heavy ],
["keys", "Ring of Keys", [("throwing_axe_a",0)], itp_type_one_handed_wpn |itp_primary|itp_bonus_against_shield,itc_scimitar,240, weight(5)|spd_rtng(98) | swing_damage(29,cut)|max_ammo(5)|weapon_length(53),imodbits_thrown ],

########### Bows ##########
["light_hunting_boow", "Light Hunting Bow", [("saracin_bow_a",0),("saracin_bow_case_a",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 150, weight(1)|difficulty(0)|spd_rtng(110)|shoot_speed(52)|thrust_damage(20,cut), imodbits_bow, [], [fac_kingdom_3] ],
["hunting_bow",         "Hunting Bow", [("hunting_bow",0),("hunting_bow_carry",ixmesh_carry)],itp_type_bow |itp_merchandise|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back, 17 , weight(1)|difficulty(0)|spd_rtng(100) | shoot_speed(52) | thrust_damage(15 ,  pierce),imodbits_bow ],
["short_bow",         "Short Bow", [("short_bow",0),("short_bow_carry",ixmesh_carry)], itp_type_bow |itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 58 , weight(1)|difficulty(1)|spd_rtng(97) | shoot_speed(55) | thrust_damage(18 ,  pierce  ),imodbits_bow ],
["nomad_bow",         "Nomad Bow", [("nomad_bow",0),("nomad_bow_case", ixmesh_carry)], itp_type_bow |itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 164 , weight(1.25)|difficulty(2)|spd_rtng(94) | shoot_speed(56) | thrust_damage(20 ,  pierce),imodbits_bow ],
["long_bow",         "Long Bow", [("long_bow",0),("long_bow_carry",ixmesh_carry)], itp_type_bow |itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 145 , weight(1.75)|difficulty(3)|spd_rtng(79) | shoot_speed(56) | thrust_damage(22 ,  pierce),imodbits_bow ],
["light_war_bow", "Light War Bow", [("saracin_bow_b",0),("saracin_bow_case_b",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 250, weight(1.75)|difficulty(0)|spd_rtng(88)|shoot_speed(63)|thrust_damage(19,pierce), imodbits_bow, [], [fac_kingdom_3] ],
["khergit_bow",         "Khergit Bow", [("khergit_bow",0),("khergit_bow_case", ixmesh_carry)], itp_type_bow |itp_merchandise|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 269 , weight(1.25)|difficulty(2)|spd_rtng(90) | shoot_speed(57) | thrust_damage(21 ,pierce),imodbits_bow, [], [fac_kingdom_3]],
["strong_bow",         "Strong Bow", [("strong_bow",0),("strong_bow_case", ixmesh_carry)], itp_type_bow |itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 437 , weight(1.25)|difficulty(3)|spd_rtng(88) | shoot_speed(60) | thrust_damage(23 ,pierce),imodbit_cracked | imodbit_bent | imodbit_masterwork ],
["war_bow",         "War Bow", [("war_bow",0),("war_bow_carry",ixmesh_carry)],itp_type_bow|itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 728 , weight(1.5)|difficulty(4)|spd_rtng(84) | shoot_speed(65) | thrust_damage(26 ,pierce),imodbits_bow ],
["heavy_war_bow", "Heavy War Bow", [("saracin_bow_c",0),("saracin_bow_case_c",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 1000, weight(2.25)|difficulty(7)|spd_rtng(80)|shoot_speed(70)|thrust_damage(30,pierce), imodbits_bow, [], [fac_kingdom_3] ],
["practice_bow_2","Practice Bow", [("hunting_bow",0), ("hunting_bow_carry",ixmesh_carry)], itp_type_bow |itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1.5)|spd_rtng(90) | shoot_speed(40) | thrust_damage(21, blunt),imodbits_bow ],



########### Crossbows ##########

["hunting_crossbow", "Hunting Crossbow", [("crossbow_a",0)], itp_type_crossbow |itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 22 , weight(2.25)|difficulty(2)|spd_rtng(47) | shoot_speed(62) | thrust_damage(37 ,  pierce)|max_ammo(1),imodbits_crossbow ],
["light_crossbow", "Light Crossbow", [("crossbow_b",0)], itp_type_crossbow |itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 67 , weight(2.5)|difficulty(3)|spd_rtng(45) | shoot_speed(70) | thrust_damage(44 ,  pierce)|max_ammo(1),imodbits_crossbow ],
["crossbow",         "Crossbow",         [("crossbow_a",0)], itp_type_crossbow |itp_merchandise|itp_primary|itp_two_handed|itp_cant_reload_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 182 , weight(3)|difficulty(3)|spd_rtng(43) | shoot_speed(78) | thrust_damage(49,pierce)|max_ammo(1),imodbits_crossbow ],
["heavy_crossbow", "Heavy Crossbow", [("crossbow_c",0)], itp_type_crossbow |itp_merchandise|itp_primary|itp_two_handed|itp_cant_reload_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 349 , weight(3.5)|difficulty(5)|spd_rtng(41) | shoot_speed(82) | thrust_damage(58 ,pierce)|max_ammo(1),imodbits_crossbow ],
["sniper_crossbow", "Siege Crossbow", [("crossbow_c",0)], itp_type_crossbow |itp_merchandise|itp_primary|itp_two_handed|itp_cant_reload_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 683 , weight(3.75)|difficulty(10)|spd_rtng(37) | shoot_speed(90) | thrust_damage(63 ,pierce)|max_ammo(1),imodbits_crossbow ],

########### Firearms ##########

["flintlock_pistol", "Flintlock Pistol", [("flintlock_pistol",0)], itp_type_pistol |itp_merchandise|itp_primary ,itcf_shoot_pistol|itcf_reload_pistol, 1230 , weight(1.5)|difficulty(0)|spd_rtng(38) | shoot_speed(160) | thrust_damage(45 ,pierce)|max_ammo(1)|accuracy(75),imodbits_none, [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,27),(position_move_y, pos1,36),(particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],
["flintlock_pistol_2", "Flintlock Pistol", [("flintlock_pistol_1",0)], itp_type_pistol |itp_merchandise|itp_primary ,itcf_shoot_pistol|itcf_reload_pistol, 2300 , weight(1.5)|difficulty(0)|spd_rtng(55) | shoot_speed(160) | thrust_damage(45 ,pierce)|max_ammo(1)|accuracy(75),imodbits_none, [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,27),(position_move_y, pos1,36),(particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],
["flintlock_rifle", "Flintlock Rifle",[("flintlock_rifle_1",0)],itp_type_musket|itp_merchandise|itp_cant_reload_on_horseback|itp_primary|itp_next_item_as_melee|itp_two_handed, itcf_reload_musket|itcf_carry_spear|itcf_shoot_musket, 2800 , weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(24) | shoot_speed(180) | thrust_damage(95 ,pierce)|max_ammo(1)|accuracy(99),imodbits_none, [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,0),(position_move_y, pos1,139),(particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],
["arquebus", "Arquebus",[("arquebus",0)],itp_type_musket|itp_merchandise|itp_cant_reload_on_horseback|itp_primary|itp_next_item_as_melee|itp_two_handed, itcf_reload_musket|itcf_carry_spear|itcf_shoot_musket, 3100 , weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(45) | shoot_speed(160) | thrust_damage(60 ,pierce)|max_ammo(1)|accuracy(78),imodbits_none, [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,0),(position_move_y, pos1,100),(particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],
["blunderbus", "Blunderbus",[("blunderbus",0)],itp_type_musket|itp_merchandise|itp_cant_reload_on_horseback|itp_primary|itp_next_item_as_melee|itp_two_handed, itcf_reload_musket|itcf_carry_spear|itcf_shoot_musket, 4600 , weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(50) | shoot_speed(160) | thrust_damage(85 ,pierce)|max_ammo(1)|accuracy(70),imodbits_none, [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,0),(position_move_y, pos1,72),(particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],
["matchlock_2", "Matchlock Musket",[("matchlock_2",0)],itp_type_musket|itp_merchandise|itp_cant_reload_on_horseback|itp_primary|itp_next_item_as_melee|itp_two_handed, itcf_reload_musket|itcf_carry_spear|itcf_shoot_musket, 2800 , weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(38) | shoot_speed(160) | thrust_damage(70 ,pierce)|max_ammo(1)|accuracy(85),imodbits_none, [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,0),(position_move_y, pos1,112),(particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],
["matchlock_1", "Matchlock Musket",[("matchlock_1",0)],itp_type_musket|itp_merchandise|itp_cant_reload_on_horseback|itp_primary|itp_next_item_as_melee|itp_two_handed, itcf_reload_musket|itcf_carry_spear|itcf_shoot_musket, 3800 , weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(42) | shoot_speed(160) | thrust_damage(65 ,pierce)|max_ammo(1)|accuracy(80),imodbits_none, [(ti_on_weapon_attack, [(play_sound,"snd_pistol_shot"),(position_move_x, pos1,0),(position_move_y, pos1,107),(particle_system_burst, "psys_pistol_smoke", pos1, 15)])]],

["torch",         "Torch", [("club",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar, 11 , weight(2.5)|difficulty(0)|spd_rtng(95) | weapon_length(95)|swing_damage(11 , blunt) | thrust_damage(0 ,  pierce),imodbits_none, [(ti_on_init_item, [(set_position_delta,0,60,0),(particle_system_add_new, "psys_torch_fire"),(particle_system_add_new, "psys_torch_smoke"),(set_current_color,150, 130, 70),(add_point_light, 10, 30),])]],





#####################
##### ITEM SETS #####
#####################

["strange_armor",  "Strange Armor", [("samurai_armor",0)], itp_type_body_armor  |itp_covers_legs ,0, 1259 , weight(18)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(19)|difficulty(0) ,imodbits_armor ],
["strange_boots",  "Strange Boots", [("samurai_boots",0)], itp_type_foot_armor | itp_attach_armature,0, 465 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(21)|difficulty(0) ,imodbits_cloth ],
["strange_helmet", "Strange Helmet", [("samurai_helmet",0)], itp_type_head_armor   ,0, 824 , weight(2)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["strange_sword", "Strange Sword", [("katana",0),("katana_scabbard",ixmesh_carry)], itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_katana|itcf_show_holster_when_drawn, 879 , weight(2.0)|difficulty(9)|spd_rtng(110) | weapon_length(95)|swing_damage(42 , cut) | thrust_damage(28 ,  pierce),imodbits_sword ],
["strange_great_sword",  "Strange Great Sword", [("no_dachi",0),("no_dachi_scabbard",ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back|itcf_show_holster_when_drawn, 1420 , weight(3.5)|difficulty(12)|spd_rtng(97) | weapon_length(125)|swing_damage(50 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["strange_short_sword", "Strange Short Sword", [("wakizashi",0),("wakizashi_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn, 321 , weight(1.25)|difficulty(0)|spd_rtng(108) | weapon_length(65)|swing_damage(25 , cut) | thrust_damage(19 ,  pierce),imodbits_sword ],

["bride_dress", "Bride Dress", [("bride_dress",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 500 , weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0) ,imodbits_cloth],
["bride_crown", "Crown of Flowers", [("bride_crown",0)],  itp_type_head_armor | itp_doesnt_cover_hair |itp_civilian |itp_attach_armature,0, 1 , weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["bride_shoes", "Bride Shoes", [("bride_shoes",0)], itp_type_foot_armor |itp_civilian | itp_attach_armature ,0, 30 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],

["blacksale_salad", "Black Visored Sallet with Coif", [("blacksale_salad",0)], itp_merchandise| itp_type_head_armor   ,0, 1100 , weight(2.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["blacky_platey_salad", "Black Milanese Armour", [("blacky_platey_salad",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 4600 , weight(30)|abundance(60)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(0) ,imodbits_plate ],
["black_boot_salad_of", "Black Steel Greaves", [("black_boot_salad_of",0)], itp_type_foot_armor  | itp_attach_armature,0, 3001 , weight(3.5)|abundance(60)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0) ,imodbits_armor ],

["bronzesalet", "Bronze Visored Sallet with Coif", [("bronzesalet",0)], itp_merchandise| itp_type_head_armor   ,0, 1100 , weight(2.5)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["bronzeplate", "Bronze Milanese Armour", [("bronzeplate",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 4600 , weight(30)|abundance(60)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(0) ,imodbits_plate ],
["bronzeshynald", "Bronze Steel Greaves", [("bronzeshynald",0)], itp_type_foot_armor  | itp_attach_armature,0, 3001 , weight(3.5)|abundance(60)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0) ,imodbits_armor ],

["nord_splinted_greaves", "Nordic Splinted Greaves", [("nord_splinted_greaves",0)], itp_merchandise| itp_type_foot_armor | itp_attach_armature,0, 440 , weight(2.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_4]],
["nord_plated_coat", "Nordic Plated Coat", [("nord_coat_of_plates",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 3828 , weight(25)|abundance(80)|head_armor(0)|body_armor(52)|leg_armor(18)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_4]],
["nord_pelted_coat", "Nordic Plated Coat With Fur", [("nord_coat_of_plates_pelt",0)], itp_merchandise| itp_type_body_armor  |itp_covers_legs ,0, 3828 , weight(25)|abundance(80)|head_armor(0)|body_armor(52)|leg_armor(18)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_4]],
["ornate_nordic_helm", "Ornate Nordic Helm", [("nord_ornate_visored_helmet",0)], itp_merchandise | itp_type_head_armor| itp_attach_armature,0, 954 , weight(2.6)|abundance(90)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_4]],

["pilgrim_disguise", "Pilgrim Disguise", [("pilgrim_outfit",0)], 0| itp_type_body_armor |itp_covers_legs |itp_civilian ,0, 25 , weight(2)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(8)|difficulty(0) ,imodbits_cloth ],
["pilgrim_hood", "Pilgrim Hood", [("pilgrim_hood",0)], 0| itp_type_head_armor |itp_civilian  ,0, 35 , weight(1.25)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],



######################
##### MERC STUFF #####
######################

#Blue Company


#



#remove++
#["armet_a", "Armet", [("armet",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 1500, weight(4)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["lobster_a", "Lobster Helmet", [("lobster",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 1250, weight(3.2)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["lobster_b", "Lobster Helmet", [("lobster2",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 1250, weight(3.2)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["morion_a", "Morion", [("morion1",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 1000, weight(2.5)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["morion_b", "Morion", [("morion2",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 1100, weight(3)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#["round_morion", "Round Morion", [("morion3",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 1250, weight(3)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_armor ],
#remove--


#remove++
#["white_doublet", "White Doublet", [("civilian_02",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 175, weight(7)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(4)|difficulty(0), imodbits_cloth ],
#["brown_doublet", "Brown Doublet", [("civilian_05",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 175, weight(7)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(4)|difficulty(0), imodbits_cloth ],
#["brown_pikeman_cuirass", "Brown Pikeman Cuirass", [("genericpikeman_01",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(17)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(8)|difficulty(0), imodbits_armor|imodbits_plate ],
#["brown_pikeman_cuirass_with_legguard", "Brown Pikeman Cuirass with Legguard", [("genericpikeman_02",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(20)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(13)|difficulty(0), imodbits_armor|imodbits_plate ],
#["blue_pikeman_cuirass", "Blue Pikeman Cuirass", [("genericpikeman_07",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(17)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(8)|difficulty(0), imodbits_armor|imodbits_plate ],
#["blue_pikeman_cuirass_with_legguard", "Blue Pikeman Cuirass with Legguard", [("genericpikeman_08",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(20)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(13)|difficulty(0), imodbits_armor|imodbits_plate ],
#["white_pikeman_cuirass", "White Pikeman Cuirass", [("genericpikeman_09",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(17)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(8)|difficulty(0), imodbits_armor|imodbits_plate ],
#["white_pikeman_cuirass_with_legguard", "White Pikeman Cuirass with Legguard", [("genericpikeman_10",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 750, weight(20)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(13)|difficulty(0), imodbits_armor|imodbits_plate ],
#remove--
















#############################
##### ITEMS FOR REMOVAL #####
#############################

#["paramerion_sword",  "Single Edged Sword", [("bb_paramerion",0),("bb_paramerion_1_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  418 , weight(1.3)|difficulty(2)|spd_rtng(100) | weapon_length(93)|swing_damage(27 , cut) | thrust_damage(18 ,  pierce),imodbits_sword_high ],
#["romeyan_sword",  "Arming Sword", [("bb_romeyan_sword_1",0),("bb_romeyan_sword_1_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  528 , weight(1.5)|difficulty(2)|spd_rtng(100) | weapon_length(92)|swing_damage(28 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high ],
#["spathion_sword",  "Infantry Sword", [("bb_spathion",0),("bb_spathion_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  548 , weight(1.2)|difficulty(2)|spd_rtng(100) | weapon_length(93)|swing_damage(27 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high ],
#["varyag_axe",    "Nordic Axe", [("bb_varyag_axe",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 490 , weight(3.5)|difficulty(13)|spd_rtng(88) | weapon_length(95)|swing_damage(39 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_4]],
#["romeyan_sword_2",  "Swadian Sword", [("bb_romeyan_sword_1",0),("bb_romeyan_sword_1_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  528 , weight(1.5)|difficulty(2)|spd_rtng(100) | weapon_length(95)|swing_damage(28 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high, [], [fac_kingdom_1]],
#["serbian_sword",  "Vaegiran Sword", [("bb_serbian_sword_4",0),("bb_serbian_sword_4_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  728 , weight(1.7)|difficulty(2)|spd_rtng(101) | weapon_length(99)|swing_damage(29 , cut) | thrust_damage(18 ,  pierce),imodbits_sword_high, [], [fac_kingdom_2]],
#["serbian_sword2",  "Vaegiran Longsword", [("bb_serbian_sword_10",0),("bb_serbian_sword_10_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  688 , weight(1.8)|difficulty(2)|spd_rtng(99) | weapon_length(102)|swing_damage(28 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high, [], [fac_kingdom_2]],
#["serbian_th_sword",  "Two-handed Sword", [("bb_serbian_two_handed_sword_1",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 870 , weight(2.75)|difficulty(10)|spd_rtng(89) | weapon_length(117)|swing_damage(40 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high ],
#["mod_spear1", "Vaegiran Short Spear", [("bb_serbian_spear_1",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  365 , weight(2.5)|difficulty(3)|spd_rtng(95) | weapon_length(134)|swing_damage(23, cut) | thrust_damage(26 ,  pierce),imodbits_polearm, [], [fac_kingdom_2]],
#["mod_spear2", "Vaegiran Short Spear", [("bb_serbian_spear_2",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  395 , weight(2.5)|difficulty(3)|spd_rtng(95) | weapon_length(136)|swing_damage(25, cut) | thrust_damage(28 ,  pierce),imodbits_polearm, [], [fac_kingdom_2]],
#["mod_spear3", "Vaegiran Spear", [("bb_serbian_spear_3",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  455 , weight(2.7)|difficulty(4)|spd_rtng(93) | weapon_length(165)|swing_damage(25, cut) | thrust_damage(27 ,  pierce),imodbits_polearm, [], [fac_kingdom_2]],
#["mod_spear4", "Rhodok Spear", [("bb_serbian_spear_4",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  397 , weight(2.4)|difficulty(3)|spd_rtng(97) | weapon_length(130)|swing_damage(22, cut) | thrust_damage(25 ,  pierce),imodbits_polearm, [], [fac_kingdom_5]],
#["mod_spear5", "Rhodok Spear", [("bb_serbian_spear_6",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  367 , weight(2.6)|difficulty(3)|spd_rtng(95) | weapon_length(142)|swing_damage(24, cut) | thrust_damage(25 ,  pierce),imodbits_polearm, [], [fac_kingdom_5]],
#["english_war_axe", "Swadian War Axe", [("bb_english_war_axe_1",0)], itp_type_two_handed_wpn|itp_merchandise| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,  557 , weight(2.5)|difficulty(5)|spd_rtng(94) | weapon_length(93)|swing_damage(34 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_1]],
#["mod_spear6", "Khergit Spear", [("bb_mongol_spear_1",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  395 , weight(4.0)|difficulty(6)|spd_rtng(94) | weapon_length(135)|swing_damage(21, cut) | thrust_damage(20 ,  pierce),imodbits_polearm, [], [fac_kingdom_3]],
#["mod_knife1",  "Traders Knife", [("medieval_knife",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_dagger|itcf_carry_dagger_front_left,  38 , weight(0.7)|difficulty(0)|spd_rtng(112) | weapon_length(49)|swing_damage(22 , cut) | thrust_damage(13 ,  pierce),imodbits_sword ],
#["mod_sword1",  "Rhodok Sword", [("bb_medieval_sword_3",0),("bb_medieval_sword_3_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  558 , weight(1.8)|difficulty(3)|spd_rtng(100) | weapon_length(95)|swing_damage(29 , cut) | thrust_damage(19 ,  pierce),imodbits_sword_high, [], [fac_kingdom_5]],
#["battle_bow",   "Battle Bow", [("battle_bow",0),("battle_bow_carry",ixmesh_carry)], itp_type_bow |itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back,  545 , weight(1.1)|difficulty(4)|spd_rtng(98) | shoot_speed(76) | thrust_damage(25 ,  pierce),imodbits_bow ],
#["mod_bow1",  "Bow of War", [("bb_war_bow",0),("bb_war_bow_carry",ixmesh_carry)],itp_type_bow|itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back,  728 , weight(1.3)|difficulty(5)|spd_rtng(90) | shoot_speed(72) | thrust_damage(26 ,pierce),imodbits_bow ],
#["french_pepperpot2", "Yaleni Pepperpot", [("frenchpepperpot2",0)], itp_merchandise | itp_type_head_armor,0, 824 , weight(2.5)|abundance(80)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_5]],
#["french_pepperpot3", "Southern Pepperpot", [("frenchpepperpot3",0)], itp_merchandise | itp_type_head_armor,0, 834 , weight(2.5)|abundance(80)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_5]],
#["munitions_helm2", "Munitions Helm", [("munitionshelm2",0)], itp_merchandise | itp_type_head_armor,0, 714 , weight(2.6)|abundance(80)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["munitions_helm1", "Munitions Helm", [("munitionshelm1",0)], itp_merchandise | itp_type_head_armor,0, 744 , weight(2.8)|abundance(90)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["french_pepperpot", "Jelkalan Pepperpot", [("frenchpepperpot",0)], itp_merchandise | itp_type_head_armor,0, 894 , weight(2.5)|abundance(80)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_5]],
#["flattop_helmet", "Flattop Helmet", [("flattophelmet",0)], itp_merchandise | itp_type_head_armor,0, 737 , weight(2.4)|abundance(80)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["kettlehatface_brynie", "Kettle Covered face Helm", [("kettlehatfacebyrnie",0)], itp_merchandise | itp_type_head_armor,0, 824 , weight(2)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_5]],
#["balaclava_coif", "Coif", [("balaclavacoif",0)], itp_merchandise | itp_type_head_armor,0, 654 , weight(1.5)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["fullface_coif", "Full Coif", [("fullfacecoif",0)], itp_merchandise | itp_type_head_armor,0, 824 , weight(1.8)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["kettle_fullcoif", "Kettle Full Coif", [("kettlehatfullcoif",0)], itp_merchandise | itp_type_head_armor,0, 954 , weight(2.3)|abundance(90)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_5]],
#["norman_clavacoif", "Nordic Helm Bala Coif", [("normanhelmbalaclavacoif",0)], itp_merchandise | itp_type_head_armor,0, 982 , weight(2.4)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_4]],
#["norman_coif", "Nordic Helm Coif", [("normanhelmcoif",0)], itp_merchandise | itp_type_head_armor,0, 889 , weight(2.3)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_4]],
#["norman_fullcoif", "Nordic Helm Full Coif", [("normanhelmfullcoif",0)], itp_merchandise | itp_type_head_armor,0, 1014 , weight(2.5)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_4]],
#["bolzano_bucket", "Crusader Bucket", [("bolzanobucket",0)], itp_merchandise | itp_type_head_armor,0, 1224 , weight(2.7)|abundance(70)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["bolzano_painted1", "Painted Crusader Bucket", [("col1_bolzanobucket",0)], itp_merchandise | itp_type_head_armor,0, 1424 , weight(2.7)|abundance(70)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["bolzano_painted2", "Painted Crusader Bucket", [("col2_bolzanobucket",0)], itp_merchandise | itp_type_head_armor,0, 1324 , weight(2.5)|abundance(80)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["crusader_bucket1", "Crusader Bucket", [("crusaderbucket1",0)], itp_merchandise | itp_type_head_armor,0, 1388 , weight(2.6)|abundance(70)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["gotland_bucket", "Gotland Bucket", [("gotlandbucket",0)], itp_merchandise | itp_type_head_armor,0, 1464 , weight(2.7)|abundance(80)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["madeln_bucket1", "Crusader Bucket", [("madelnbucket1",0)], itp_merchandise | itp_type_head_armor,0, 1624 , weight(2.8)|abundance(80)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["madeln_bucket2", "Crusader Bucket", [("madelnbucket2",0)], itp_merchandise | itp_type_head_armor,0, 1467 , weight(2.7)|abundance(80)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["paintedcrusaderbucket1", "Red Crusader Helm", [("col2_crusaderbucket1",0)], itp_merchandise | itp_type_head_armor,0, 1357 , weight(2.5)|abundance(80)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["paintedcrusaderbucket2", "Red Crusader Helm", [("col2_crusaderbucket2",0)], itp_merchandise | itp_type_head_armor,0, 1724 , weight(2.6)|abundance(80)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["paintedgotland", "Painted Gotland Helm", [("col2_gotlandbucket",0)], itp_merchandise | itp_type_head_armor,0, 1387 , weight(2.7)|abundance(80)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["paintedmadelnbucket", "Painted Helm", [("col2_madelnbucket1",0)], itp_merchandise | itp_type_head_armor,0, 1634 , weight(2.4)|abundance(70)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["paintedmadelnbucket2", "Painted Helm", [("col2_madelnbucket2",0)], itp_merchandise | itp_type_head_armor,0, 1474 , weight(2.4)|abundance(70)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["paintedcrusaderbucket3", "Blue Crusader Helm", [("col1_crusaderbucket1",0)], itp_merchandise | itp_type_head_armor,0, 1244 , weight(2.3)|abundance(80)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["paintedcrusaderbucket4", "Blue Crusader Helm", [("col1_crusaderbucket2",0)], itp_merchandise | itp_type_head_armor,0, 1224 , weight(2.3)|abundance(80)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["redwhitecrusaderhelm", "Painted Crusader Helm", [("col1_gotlandbucket",0)], itp_merchandise | itp_type_head_armor,0, 1354 , weight(2.5)|abundance(70)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["redyellowcrusaderhelm", "Painted Crusader Helm", [("col1_madelnbucket1",0)], itp_merchandise | itp_type_head_armor,0, 1324 , weight(2.5)|abundance(70)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["paintedmadelnbucket3", "Painted Helm", [("col1_madelnbucket2",0)], itp_merchandise | itp_type_head_armor,0, 1624 , weight(2.6)|abundance(80)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_1]],
#["khergit_conical_face", "Conical Full Helm", [("conical_helmet_steppe_b",0)], itp_merchandise | itp_type_head_armor | itp_attach_armature   ,0, 624 , weight(1.6)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate, [], [fac_kingdom_3]],
#["mongol_leather_cap", "Tribesmans Cap", [("leather_cap_new",0)],itp_merchandise|itp_type_head_armor,0,101, weight(1)|abundance(100)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth, [], [fac_kingdom_3]],
#["padded_coif_1", "Padded Coif", [("helmet_22",0)],itp_merchandise|itp_type_head_armor,0,101, weight(1)|abundance(100)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
#["padded_coif_2", "Padded Coif", [("helmet_23",0)],itp_merchandise|itp_type_head_armor,0,101, weight(1)|abundance(100)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(0),imodbits_cloth],
#["teutonic_helm", "Teutonic Helm", [("helmet_20",0)], itp_type_head_armor   ,0, 1224 , weight(2.3)|abundance(80)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["teutonic_helm_winged", "Winged Teutonic Helm", [("helmet_21",0)], itp_type_head_armor   ,0, 1224 , weight(2.3)|abundance(80)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
#["mod_voulge", "Nordic Voulge", [("luc_saxon_voulge",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  397 , weight(3.3)|difficulty(3)|spd_rtng(89) | weapon_length(166)|swing_damage(32, cut) | thrust_damage(19 ,  pierce),imodbits_polearm, [], [fac_kingdom_4]],
#["mod_voulge2", "Nordic Reinforced Voulge", [("luc_saxon_voulge_b",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  397 , weight(3.4)|difficulty(3)|spd_rtng(88) | weapon_length(170)|swing_damage(35, cut) | thrust_damage(20 ,  pierce),imodbits_polearm, [], [fac_kingdom_4]],
#["mod_swadian_axe", "Swadian Bastard Axe", [("luc_two_handed_axe_1",0)], itp_type_two_handed_wpn|itp_merchandise| itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_morningstar|itcf_carry_axe_back, 90 , weight(3.5)|difficulty(9)|spd_rtng(95) | weapon_length(90)|swing_damage(44 , cut) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_1]],
#["mod_vaegir_axe", "Vaegiran Bastard Axe", [("luc_two_handed_axe_2",0)], itp_type_two_handed_wpn|itp_merchandise| itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_morningstar|itcf_carry_axe_back, 90 , weight(3.5)|difficulty(10)|spd_rtng(106) | weapon_length(88)|swing_damage(42 , cut) | thrust_damage(0, pierce), imodbits_axe, [], [fac_kingdom_2]],
#["mod_bastard_axe", "Bastard Axe", [("luc_knightly_axe_two_handed",0)], itp_type_two_handed_wpn|itp_merchandise|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_bastardsword|itcf_carry_axe_back, 90 , weight(3.3)|difficulty(8)|spd_rtng(98) | weapon_length(98)|swing_damage(42 , cut) | thrust_damage(14 ,  pierce),imodbits_axe ],
#["mod_swadian_warpick", "Swadian War Pick", [("luc_knightly_hammer",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip,  27 , weight(2.5)|difficulty(2)|spd_rtng(99) | weapon_length(71)|swing_damage(29 , pierce) | thrust_damage(0 ,  pierce),imodbits_pick, [], [fac_kingdom_1]],
#["mod_morningstar1",  "Short-hafted Morning Star", [("luc_morningstar_2",0)],  itp_type_one_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_wooden_parry, itc_longsword|itcf_carry_sword_left_hip, 240 , weight(1.5)|difficulty(7)|spd_rtng(104) | weapon_length(70)|swing_damage(26 , pierce) |thrust_damage(7, pierce) ,imodbits_mace, [], [fac_kingdom_1]],
#["mod_morningstar2",  "Light Morning Star", [("luc_morningstar_3",0)],  itp_type_one_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_wooden_parry, itc_longsword|itcf_carry_sword_left_hip, 200 , weight(1.3)|difficulty(5)|spd_rtng(110) | weapon_length(68)|swing_damage(24 , pierce) |thrust_damage(7, pierce) ,imodbits_mace, [], [fac_kingdom_1]],
#["mod_morningstar3",  "Heavy Morning Star", [("luc_morningstar_4",0)],  itp_type_one_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_wooden_parry, itc_longsword|itcf_carry_sword_left_hip, 360 , weight(2.3)|difficulty(10)|spd_rtng(100) | weapon_length(90)|swing_damage(28 , pierce) |thrust_damage(8, pierce) ,imodbits_mace, [], [fac_kingdom_1]],
#["mod_bardiche","Short-hafted Vaegiran Bardiche", [("luc_polish_bardiche",0)], itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary|itp_unbalanced|itp_bonus_against_shield|itp_wooden_parry, itc_staff, 390 , weight(3.35)|difficulty(8)|spd_rtng(89) | weapon_length(103)|swing_damage(48 , cut) | thrust_damage(17 ,  pierce),imodbits_axe, [], [fac_kingdom_2]],
#["mod_partisan", "Partisan", [("luc_partisan",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  582 , weight(3.7)|difficulty(7)|spd_rtng(89) | weapon_length(170)|swing_damage(28, cut) | thrust_damage(30 ,  pierce),imodbits_polearm ],
#["mod_hafted_morningstar", "Long-hafted Morningstar", [("luc_long_hafted_morningstar_b",0)], itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_wooden_parry, itc_staff,  582 , weight(3.3)|difficulty(6)|spd_rtng(90) | weapon_length(145)|swing_damage(23, pierce) | thrust_damage(10 ,  pierce),imodbits_polearm ],
#["mod_bastard_axe2", "Lochaber Axe", [("luc_knightly_axe_v2",0)], itp_type_two_handed_wpn|itp_merchandise|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_morningstar|itcf_carry_axe_back, 90 , weight(3.5)|difficulty(7)|spd_rtng(97) | weapon_length(106)|swing_damage(38 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
#["mod_bastard_axe3", "Knights Axe", [("luc_knightly_axe_b",0)], itp_type_two_handed_wpn|itp_merchandise|itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_unbalanced, itc_bastardsword|itcf_carry_axe_back, 90 , weight(3.3)|difficulty(6)|spd_rtng(97) | weapon_length(108)|swing_damage(40 , cut) | thrust_damage(20 ,  pierce),imodbits_axe ],
#["mod_hhbow",  "Highland Hunting Bow", [("bb_hunting_bow_v1",0),("bb_hunting_bow_v1_carry",ixmesh_carry)],itp_type_bow|itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back,  728 , weight(1)|difficulty(0)|spd_rtng(100) | shoot_speed(61) | thrust_damage(20 ,pierce),imodbits_bow ],
#["throwing_hammer", "Throwing Hammer", [("luc_throwing_hammer",0)], itp_type_thrown |itp_merchandise|itp_primary,itcf_throw_stone,620, weight(8)|difficulty(3)|spd_rtng(97) | shoot_speed(18) | thrust_damage(24,blunt)|max_ammo(3)|weapon_length(35),imodbits_none ],
#["jack_anduril",  "Two-handed Knightly Sword", [("jack_anduril",0),("jack_anduril_scab", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_greatsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  558 , weight(1.9)|difficulty(12)|spd_rtng(98) | weapon_length(127)|swing_damage(45 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high ],
#["jack_boromir",  "Ornate Arming Sword", [("jack_boromir",0),("jack_boromir_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  688 , weight(1.6)|difficulty(6)|spd_rtng(103) | weapon_length(100)|swing_damage(31 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["jack_faramir",  "Ornate Knight's Sword", [("jack_faramir",0),("jack_faramir_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  758 , weight(1.7)|difficulty(8)|spd_rtng(106) | weapon_length(96)|swing_damage(34 , cut) | thrust_damage(21 ,  pierce),imodbits_sword_high ],
#["jack_glamdring",  "Ornate Greatsword", [("jack_glamdring",0),("jack_glamdring_scab", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  1050 , weight(3.6)|difficulty(12)|spd_rtng(103) | weapon_length(120)|swing_damage(42 , cut) | thrust_damage(30 ,  pierce),imodbits_sword_high ],
#["jack_herugrim",  "Kingsblade", [("jack_herugrim",0),("jack_herugrim_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  858 , weight(1.3)|difficulty(7)|spd_rtng(105) | weapon_length(98)|swing_damage(30 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high ],
#["jack_sting",  "Longknife", [("jack_sting",0),("jack_sting_scab", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,  558 , weight(1.0)|difficulty(3)|spd_rtng(125) | weapon_length(55)|swing_damage(27 , cut) | thrust_damage(27 ,  pierce),imodbits_sword ],
#["faradon_two_hander",  "Two-handed Sword", [("faradon_twohanded1",0)], itp_unbalanced|itp_type_two_handed_wpn|itp_merchandise| itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 1970 , weight(3.95)|difficulty(15)|spd_rtng(88) | weapon_length(118)|swing_damage(38 , cut) | thrust_damage(25 ,  pierce),imodbits_sword_high ],













## WINDYPLAINS+ ## - TAVERN ANIMATION PACK - OSP by Slawomir of Aaarrghh
["dedal_kufel",				"Mug",					[("dedal_kufelL",0)], itp_type_hand_armor|itp_unique,0,0,weight(1),0],
["dedal_lutnia",			"Lute",					[("dedal_lutniaL",0)], itp_type_hand_armor|itp_unique,0,0,weight(1),0],
["dedal_lira",				"Lyre",						[("dedal_liraL",0)], itp_type_hand_armor|itp_unique,0,0,weight(1),0],

["silverstag_emblem", "Silverstag Emblem", [("stag_coin",0)], itp_type_goods, 0, 75,weight(0)|abundance(110)|max_ammo(100),imodbits_none],


#################################################
##DAWG+ - Added since certain lords won't equip original item, lowered requirements and is not merchandise
["plate_heraldic_lord", "Heraldic Heavy Mail and Plate", [("plate_heraldic",0)], itp_type_body_armor|itp_covers_legs,0, 2430,weight(21)|abundance(50)|head_armor(0)|body_armor(51)|leg_armor(20)|difficulty(0),imodbits_plate,[(ti_on_init_item, [(store_trigger_param_1, ":agent_no"),(store_trigger_param_2, ":troop_no"),(call_script, "script_shield_item_set_banner", "tableau_heraldic_armor_plate", ":agent_no", ":troop_no")])],[fac_player_faction]],
["vaegir_elite_armor_lord", "Vaegiran Elite Armor", [("lamellar_armor_c",0)],  itp_type_body_armor  |itp_covers_legs ,0, 3828 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_2]],
["sarranid_elite_armor_lord", "Sarranid Elite Armor", [("tunic_armor_a",0)],  itp_type_body_armor  |itp_covers_legs ,0, 3828 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
["sarranid_mail_shirt_lord", "Sarranid Mail Shirt", [("sarranian_mail_shirt",0)], itp_type_body_armor  |itp_covers_legs|itp_civilian ,0, 1400 , weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
["mamluke_mail_lord", "Mamluke Mail", [("sarranid_elite_cavalary",0)], itp_type_body_armor |itp_covers_legs|itp_civilian  ,0,  2900 , weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(0) ,imodbits_armor, [], [fac_kingdom_6]],
["winged_great_helmet_lord", "Winged Great Helmet", [("maciejowski_helmet_new",0)], itp_type_head_armor,0,  1240 , weight(2.75)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["splinted_greaves_lord", "Splinted Greaves", [("splinted_greaves_a",0)], itp_type_foot_armor | itp_attach_armature,0, 853 , weight(2.75)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(0) ,imodbits_armor ],
["mail_boots_lord", "Mail Boots", [("mail_boots_a",0)],  itp_type_foot_armor | itp_attach_armature  ,0, 1250 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(0) ,imodbits_armor ],
["lamellar_armor_lord", "Lamellar Armor", [("lamellar_armor_b",0)],  itp_type_body_armor  |itp_covers_legs ,0, 2410 , weight(25)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
["khergit_elite_armor_lord", "Khergit Elite Armor", [("lamellar_armor_d",0)], itp_type_body_armor  |itp_covers_legs ,0, 3828 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
["banded_armor_lord", "Banded Armor", [("banded_armor_a",0)], itp_type_body_armor  |itp_covers_legs ,0, 2710 , weight(23)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(14)|difficulty(0) ,imodbits_armor ],
["coat_of_plates_lord", "Coat of Plates", [("coat_of_plates_a",0)], itp_type_body_armor  |itp_covers_legs ,0, 3828 , weight(25)|abundance(80)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(0) ,imodbits_armor ],
["scale_armor_lord", "Scale Armor", [("lamellar_armor_e",0)], itp_type_body_armor  |itp_covers_legs ,0, 2558 , weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(13)|difficulty(0) ,imodbits_armor ],
#################################################


["items_end", "Items End", [("shield_round_a",0)], 0, 0, 1, 0, 0],
]
# modmerger_start version=201 type=2
try:
    component_name = "items"
    var_set = { "items" : items }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
