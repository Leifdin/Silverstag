# Center Hub by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *
from ID_skills import *
from header_terrain_types import *


####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	 

# script_hub_initialize
# Sets initial conditions for the enhanced diplomacy system.
("hub_initialize",
	[
		######################################################
		#####          INITIALIZE ITEM WEIGHTS           #####
		######################################################
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_horse),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_one_handed_wpn),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_two_handed_wpn),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_polearm),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_shield),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_bow),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_crossbow),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_thrown),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_head_armor),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_body_armor),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_foot_armor),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_hand_armor),
		(call_script, "script_hub_define_item_type_best_and_worst", itp_type_pistol),
		
		
		######################################################
		#####         INITIALIZE TROOP DEFAULTS          #####
		######################################################
		(try_for_range, ":troop_no", troop_definitions_begin, troop_definitions_end),
			(neg|troop_is_hero, ":troop_no"),
			(call_script, "script_cf_troop_is_non_array", ":troop_no"), # Module_scripts.py
			
			(call_script, "script_hub_determine_purchase_cost", ":troop_no"),
			
			# Set default value for recruit type.
			(troop_set_slot, ":troop_no", slot_troop_recruit_type, STRT_PEASANT),
			
			# Set everyone to having no unique location.  Unique troops will be initialized further down.
			(troop_set_slot, ":troop_no", slot_troop_unique_location, 0),
			
			# Setup recruitable faction.
			(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, 0),
			(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_2, 0),
			(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_3, 0),
			(try_begin), ## SWADIA
				(is_between, ":troop_no", swadia_troops_begin, swadia_troops_end),
				(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, "fac_culture_1"),
			(else_try), ## VAEGIRS
				(is_between, ":troop_no", vaegir_troops_begin, vaegir_troops_end),
				(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, "fac_culture_2"),
			(else_try), ## KHERGITS
				(is_between, ":troop_no", khergit_troops_begin, khergit_troops_end),
				(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, "fac_culture_3"),
			(else_try), ## NORDS
				(is_between, ":troop_no", nord_troops_begin, nord_troops_end),
				(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, "fac_culture_4"),
			(else_try), ## RHODOKS
				(is_between, ":troop_no", rhodok_troops_begin, rhodok_troops_end),
				(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, "fac_culture_5"),
			(else_try), ## SARRANID
				(is_between, ":troop_no", sarranid_troops_begin, sarranid_troops_end),
				(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, "fac_culture_6"),
			(else_try), ## PLAYER FACTION
				(is_between, ":troop_no", player_troops_begin, player_troops_end),
				(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, "fac_culture_player"),
			(try_end),
		(try_end),
		
		
		######################################################
		#####          MERCENARY TROOP DEFAULTS          #####
		######################################################
		(try_for_range, ":troop_no", mercenary_troops_begin, mercenary_troops_end),
			(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", ":troop_no"), # combat_scripts.py
			(troop_set_slot, ":troop_no", slot_troop_recruit_type, STRT_MERCENARY),
			
			# Common Mercenaries
			(neq, ":troop_no", "trp_watchman"),
			(neq, ":troop_no", "trp_caravan_guard"),
			# Setup requirement for mercenary chapterhouses.
			(call_script, "script_ce_assign_troop_requirement", ":troop_no", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED), # combat_scripts.py - prereq constants in combat_constants.py
		(try_end),
		
		######################################################
		#####           BANDIT TROOP DEFAULTS            #####
		######################################################
		(try_for_range, ":troop_no", bandits_begin, bandit_upgrades_end),
			(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", ":troop_no"), # combat_scripts.py
			(call_script, "script_ce_assign_troop_requirement", ":troop_no", PREREQ_DISHONORABLE, PREREQ_UNASSIGNED), # combat_scripts.py - prereq constants in combat_constants.py
			
			# Define their class type.
			(troop_set_class, ":troop_no", CLASS_INFANTRY),
			(try_begin),
				(troop_has_flag, ":troop_no", tf_guarantee_horse),
				(troop_set_class, ":troop_no", CLASS_CAVALRY),
			(else_try),
				(troop_has_flag, ":troop_no", tf_guarantee_ranged),
				(troop_set_class, ":troop_no", CLASS_RANGED),
			(try_end),
			
			# Set their recruitable cultures.
			(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_1, 0),
			(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_2, 0),
			(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_3, 0),
			(is_between, ":troop_no", bandits_begin, bandits_end),
			(troop_set_slot, ":troop_no", slot_troop_recruitable_faction_3, "fac_outlaws"),
		(try_end),
		# Mountain Bandits (Rhodok & Khergit territories)
		(troop_set_slot, "trp_mountain_bandit", slot_troop_recruitable_faction_1, "fac_culture_5"),
		(troop_set_slot, "trp_mountain_tracker", slot_troop_recruitable_faction_1, "fac_culture_5"),
		(troop_set_slot, "trp_mountain_hunter", slot_troop_recruitable_faction_1, "fac_culture_5"),
		# Forest Bandits (Rhodok & Swadia territories)
		(troop_set_slot, "trp_forest_bandit", slot_troop_recruitable_faction_1, "fac_culture_5"),
		(troop_set_slot, "trp_forest_bandit", slot_troop_recruitable_faction_2, "fac_culture_1"),
		(troop_set_slot, "trp_forest_poacher", slot_troop_recruitable_faction_1, "fac_culture_5"),
		(troop_set_slot, "trp_forest_poacher", slot_troop_recruitable_faction_2, "fac_culture_1"),
		(troop_set_slot, "trp_forest_footpad", slot_troop_recruitable_faction_1, "fac_culture_5"),
		(troop_set_slot, "trp_forest_footpad", slot_troop_recruitable_faction_2, "fac_culture_1"),
		# Sea Raiders (Nord & Vaegir territories)
		(troop_set_slot, "trp_sea_raider", slot_troop_recruitable_faction_1, "fac_culture_2"),
		(troop_set_slot, "trp_sea_raider", slot_troop_recruitable_faction_2, "fac_culture_4"),
		(troop_set_slot, "trp_marauder", slot_troop_recruitable_faction_1, "fac_culture_2"),
		(troop_set_slot, "trp_marauder", slot_troop_recruitable_faction_2, "fac_culture_4"),
		(troop_set_slot, "trp_nordsman_pelttracker", slot_troop_recruitable_faction_1, "fac_culture_2"),
		(troop_set_slot, "trp_nordsman_pelttracker", slot_troop_recruitable_faction_2, "fac_culture_4"),
		# Steppe Bandits (Khergit territories)
		(troop_set_slot, "trp_steppe_bandit", slot_troop_recruitable_faction_1, "fac_culture_3"),
		(troop_set_slot, "trp_steppe_runner", slot_troop_recruitable_faction_1, "fac_culture_3"),
		(troop_set_slot, "trp_steppe_guard", slot_troop_recruitable_faction_1, "fac_culture_3"),
		# Taiga Bandits (Vaegir territories)
		(troop_set_slot, "trp_taiga_bandit", slot_troop_recruitable_faction_1, "fac_culture_2"),
		(troop_set_slot, "trp_taiga_spearman", slot_troop_recruitable_faction_1, "fac_culture_2"),
		(troop_set_slot, "trp_taiga_javelineer", slot_troop_recruitable_faction_1, "fac_culture_2"),
		# Desert Bandits (Sarranid territories)
		(troop_set_slot, "trp_desert_bandit", slot_troop_recruitable_faction_1, "fac_culture_6"),
		(troop_set_slot, "trp_desert_fighter", slot_troop_recruitable_faction_1, "fac_culture_6"),
		(troop_set_slot, "trp_desert_nomad", slot_troop_recruitable_faction_1, "fac_culture_6"),
		# Misc
		(troop_set_slot, "trp_black_khergit_horseman", slot_troop_recruitable_faction_1, "fac_culture_3"),
		(troop_set_slot, "trp_black_khergit_horseman", slot_troop_recruitable_faction_2, "fac_culture_6"),
		
		# D4 - Highland Chieftain
		(call_script, "script_ce_assign_troop_ability", "trp_mountain_chief", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_mountain_chief", BONUS_SHIELD_BASHER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_mountain_chief", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_assign_troop_ability", "trp_mountain_chief_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_mountain_chief_1", BONUS_SHIELD_BASHER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_mountain_chief_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_mountain_chief_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_assign_troop_ability", "trp_mountain_chief_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_mountain_chief_2", BONUS_SHIELD_BASHER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_mountain_chief_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_mountain_chief_2", CLASS_INFANTRY),
		
		# D4 - Raider Chieftain
		(call_script, "script_ce_assign_troop_ability", "trp_nord_chieftain", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_nord_chieftain", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_nord_chieftain", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_assign_troop_ability", "trp_nord_chieftain_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_nord_chieftain_1", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_nord_chieftain_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_nord_chieftain_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_assign_troop_ability", "trp_nord_chieftain_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_nord_chieftain_2", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_nord_chieftain_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_nord_chieftain_2", CLASS_INFANTRY),
		
		# D4 - Sarrdakian Leader
		(call_script, "script_ce_assign_troop_ability", "trp_desert_leader", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_desert_leader", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_desert_leader", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_assign_troop_ability", "trp_desert_leader_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_desert_leader_1", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_desert_leader_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_desert_leader_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_assign_troop_ability", "trp_desert_leader_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_desert_leader_2", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_desert_leader_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_desert_leader_2", CLASS_CAVALRY),
		
		
		######################################################
		#####         DEFINE FACTION TROOP LISTS         #####
		######################################################
		## SWADIA
		(faction_set_slot, "fac_kingdom_1", slot_faction_troops_begin, swadia_troops_begin),
		(faction_set_slot, "fac_kingdom_1", slot_faction_troops_end,   swadia_troops_end),
		## VAEGIRS
		(faction_set_slot, "fac_kingdom_2", slot_faction_troops_begin, vaegir_troops_begin),
		(faction_set_slot, "fac_kingdom_2", slot_faction_troops_end,   vaegir_troops_end),
		## KHERGITS
		(faction_set_slot, "fac_kingdom_3", slot_faction_troops_begin, khergit_troops_begin),
		(faction_set_slot, "fac_kingdom_3", slot_faction_troops_end,   khergit_troops_end),
		## NORDS
		(faction_set_slot, "fac_kingdom_4", slot_faction_troops_begin, nord_troops_begin),
		(faction_set_slot, "fac_kingdom_4", slot_faction_troops_end,   nord_troops_end),
		## RHODOKS
		(faction_set_slot, "fac_kingdom_5", slot_faction_troops_begin, rhodok_troops_begin),
		(faction_set_slot, "fac_kingdom_5", slot_faction_troops_end,   rhodok_troops_end),
		## SARRANID
		(faction_set_slot, "fac_kingdom_6", slot_faction_troops_begin, sarranid_troops_begin),
		(faction_set_slot, "fac_kingdom_6", slot_faction_troops_end,   sarranid_troops_end),
		## PLAYER CUSTOM FACTION
		(faction_set_slot, "fac_player_supporters_faction", slot_faction_troops_begin, player_troops_begin),
		(faction_set_slot, "fac_player_supporters_faction", slot_faction_troops_end,   player_troops_end),
		
		
		######################################################
		#####               SWADIA FACTION               #####
		######################################################
		
		## I1 Swadian Recruit
		(troop_set_class, "trp_n_swadian_recruit", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_swadian_recruit", slot_troop_purchase_cost, 10),
		
		## I3 Swadian Militia
		(troop_set_class, "trp_n_swadian_militia", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_swadian_militia", slot_troop_purchase_cost, 100),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_swadian_militia"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_swadian_militia", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_swadian_militia", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		
		## A3 Swadian Crossbowman
		(troop_set_class, "trp_n_swadian_crossbowman", CLASS_RANGED),
		(troop_set_slot, "trp_n_swadian_crossbowman", slot_troop_purchase_cost, 75),
		
		## C4 Swadian Lancer
		(troop_set_class, "trp_n_swadian_lancer", CLASS_CAVALRY),
		(troop_set_slot, "trp_n_swadian_lancer", slot_troop_purchase_cost, 700),
		
		## I5 Swadian Sergeant
		(troop_set_class, "trp_n_swadian_sergeant", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_swadian_sergeant"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_swadian_sergeant", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_swadian_sergeant", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_swadian_sergeant", slot_troop_purchase_cost, 750),
		
		## A6 Swadian Siege Breaker
		#(troop_set_class, "trp_n_swadian_siege_breaker", CLASS_RANGED),
		#(troop_set_slot, "trp_n_swadian_siege_breaker", slot_troop_purchase_cost, 1250),
		
		## C7 Swadian Knight
		(troop_set_class, "trp_n_swadian_knight", CLASS_CAVALRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_swadian_knight"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_swadian_knight", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_swadian_knight", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_swadian_knight", slot_troop_purchase_cost, 2500),
		
		## I2 - Swadia Militia
		(troop_set_class, "trp_r_swadian_militia", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_r_swadian_militia_1", CLASS_INFANTRY),
		# +2 tier
		(troop_set_class, "trp_r_swadian_militia_2", CLASS_INFANTRY),
		
		## A3 - Swadia Crossbowman
		(troop_set_class, "trp_r_swadian_crossbowman", CLASS_RANGED),
		# +1 tier
		(troop_set_class, "trp_r_swadian_crossbowman_1", CLASS_RANGED),
		# +2 tier
		(troop_set_class, "trp_r_swadian_crossbowman_2", CLASS_RANGED),
		(troop_set_slot, "trp_r_swadian_crossbowman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I4 - Swadia Footman
		(troop_set_class, "trp_r_swadian_footman", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_r_swadian_footman_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_swadian_footman_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(troop_set_class, "trp_r_swadian_footman_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_swadian_footman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I4 - Swadia Billman
		(troop_set_class, "trp_r_swadian_billman", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_r_swadian_billman_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_swadian_billman_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(troop_set_class, "trp_r_swadian_billman_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_swadian_billman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I4 - Swadia Mercenary
		(troop_set_class, "trp_r_swadian_mercenary", CLASS_RANGED),
		(troop_set_slot, "trp_r_swadian_mercenary", slot_troop_recruit_type, STRT_MERCENARY),
		# +1 tier
		(troop_set_class, "trp_r_swadian_mercenary_1", CLASS_RANGED),
		(troop_set_slot, "trp_r_swadian_mercenary_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(troop_set_class, "trp_r_swadian_mercenary_2", CLASS_RANGED),
		(troop_set_slot, "trp_r_swadian_mercenary_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## C4 - Swadia Man at Arms
		(troop_set_class, "trp_r_swadian_man_at_arms", CLASS_CAVALRY),
		# +1 tier
		(troop_set_class, "trp_r_swadian_man_at_arms_1", CLASS_CAVALRY),
		(troop_set_slot, "trp_r_swadian_man_at_arms_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(troop_set_class, "trp_r_swadian_man_at_arms_2", CLASS_CAVALRY),
		(troop_set_slot, "trp_r_swadian_man_at_arms_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I1 - Swadian Supplyman (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_supplyman"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_supplyman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_supplyman", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_swadian_supplyman", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_supplyman_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_supplyman_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_supplyman_1", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_swadian_supplyman_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_supplyman_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_supplyman_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_supplyman_2", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_supplyman_2", BONUS_SPRINTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_swadian_supplyman_2", CLASS_INFANTRY),
		
		## A1 - Swadian Hunter (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_hunter"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_hunter", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_hunter", BONUS_HUNTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_hunter", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_swadian_hunter", CLASS_RANGED),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_hunter_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_hunter_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_hunter_1", BONUS_HUNTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_hunter_1", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_swadian_hunter_1", CLASS_RANGED),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_hunter_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_hunter_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_hunter_2", BONUS_HUNTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_hunter_2", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_swadian_hunter_2", CLASS_RANGED),
		
		## H3 - Uxkhal Bandit (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_uxkhal_bandit"), # combat_scripts.py
		(troop_set_slot, "trp_r_uxkhal_bandit", slot_troop_unique_location, "p_town_7"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_uxkhal_bandit", PREREQ_DISHONORABLE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_uxkhal_bandit", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_uxkhal_bandit", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_hub_determine_purchase_cost", "trp_r_uxkhal_bandit"), # To force discount.
		(troop_set_class, "trp_r_uxkhal_bandit", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_uxkhal_bandit_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_uxkhal_bandit_1", slot_troop_unique_location, "p_town_7"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_uxkhal_bandit_1", PREREQ_DISHONORABLE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_uxkhal_bandit_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_uxkhal_bandit_1", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_uxkhal_bandit_1", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_uxkhal_bandit_1", CLASS_CAVALRY),
		(call_script, "script_hub_determine_purchase_cost", "trp_r_uxkhal_bandit_1"), # To force discount.
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_uxkhal_bandit_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_uxkhal_bandit_2", slot_troop_unique_location, "p_town_7"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_uxkhal_bandit_2", PREREQ_DISHONORABLE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_uxkhal_bandit_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_uxkhal_bandit_2", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_uxkhal_bandit_2", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_uxkhal_bandit_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_uxkhal_bandit_2", CLASS_CAVALRY),
		(call_script, "script_hub_determine_purchase_cost", "trp_r_uxkhal_bandit_2"), # To force discount.
		
		## C4 - Swadian Lancer (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_lancer"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_lancer", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_lancer", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_swadian_lancer", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_lancer_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_lancer_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_lancer_1", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_lancer_1", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_swadian_lancer_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_lancer_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_lancer_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_lancer_2", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_lancer_2", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_swadian_lancer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_swadian_lancer_2", CLASS_CAVALRY),
		
		## I5 - Swadian Sentinel (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_sentinel"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_sentinel", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sentinel", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sentinel", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_swadian_sentinel", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_swadian_sentinel", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_sentinel_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_sentinel_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sentinel_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sentinel_1", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_swadian_sentinel_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_swadian_sentinel_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_sentinel_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_sentinel_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sentinel_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sentinel_2", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sentinel_2", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_swadian_sentinel_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_swadian_sentinel_2", CLASS_INFANTRY),
		
		## I5 - Swadian Sergeant (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_sergeant"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_sergeant", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_swadian_sergeant", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_swadian_sergeant", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_sergeant_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_sergeant_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant_1", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant_1", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_swadian_sergeant_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_swadian_sergeant_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_swadian_sergeant_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_swadian_sergeant_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_swadian_sergeant_2", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_swadian_sergeant_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_swadian_sergeant_2", CLASS_INFANTRY),
		
		## A5 - Tilbaut Archer (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_tilbaut_archer"), # combat_scripts.py
		(troop_set_slot, "trp_r_tilbaut_archer", slot_troop_unique_location, "p_castle_6"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_tilbaut_archer", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_tilbaut_archer", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_tilbaut_archer", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_tilbaut_archer", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_tilbaut_archer", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_tilbaut_archer", CLASS_RANGED),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_tilbaut_archer_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_tilbaut_archer_1", slot_troop_unique_location, "p_castle_6"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_tilbaut_archer_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_tilbaut_archer_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_tilbaut_archer_1", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_tilbaut_archer_1", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_tilbaut_archer_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_tilbaut_archer_1", CLASS_RANGED),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_tilbaut_archer_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_tilbaut_archer_2", slot_troop_unique_location, "p_castle_6"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_tilbaut_archer_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_tilbaut_archer_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_tilbaut_archer_2", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_tilbaut_archer_2", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_tilbaut_archer_2", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_tilbaut_archer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_tilbaut_archer_2", CLASS_RANGED),
		
		## C5 - Dhirim Captain (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_dhirim_captain"), # combat_scripts.py
		(troop_set_slot, "trp_r_dhirim_captain", slot_troop_unique_location, "p_town_16"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_dhirim_captain", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_dhirim_captain", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_dhirim_captain", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_dhirim_captain", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_dhirim_captain_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_dhirim_captain_1", slot_troop_unique_location, "p_town_16"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_dhirim_captain_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_dhirim_captain_1", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain_1", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_dhirim_captain_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_dhirim_captain_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_dhirim_captain_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_dhirim_captain_2", slot_troop_unique_location, "p_town_16"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_dhirim_captain_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_dhirim_captain_2", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_dhirim_captain_2", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_dhirim_captain_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_dhirim_captain_2", CLASS_CAVALRY),
		
		## A6 - Suno Master Archer (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_suno_master_archer"), # combat_scripts.py
		(troop_set_slot, "trp_r_suno_master_archer", slot_troop_unique_location, "p_town_4"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_suno_master_archer", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_suno_master_archer", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_suno_master_archer", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_suno_master_archer", CLASS_RANGED),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_suno_master_archer_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_suno_master_archer_1", slot_troop_unique_location, "p_town_4"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_suno_master_archer_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_suno_master_archer_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer_1", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer_1", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_suno_master_archer_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_suno_master_archer_1", CLASS_RANGED),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_suno_master_archer_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_suno_master_archer_2", slot_troop_unique_location, "p_town_4"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_suno_master_archer_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_suno_master_archer_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer_2", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_suno_master_archer_2", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_suno_master_archer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_suno_master_archer_2", CLASS_RANGED),
		
		## C7 - Praven Knight (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_praven_knight"), # combat_scripts.py
		(troop_set_slot, "trp_r_praven_knight", slot_troop_unique_location, "p_town_6"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight", BONUS_RALLYING_STRIKE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_praven_knight", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_praven_knight", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_praven_knight_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_praven_knight_1", slot_troop_unique_location, "p_town_6"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight_1", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight_1", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight_1", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight_1", BONUS_RALLYING_STRIKE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_praven_knight_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_praven_knight_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_praven_knight_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_praven_knight_2", slot_troop_unique_location, "p_town_6"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight_2", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_praven_knight_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight_2", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_praven_knight_2", BONUS_RALLYING_STRIKE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_praven_knight_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_praven_knight_2", CLASS_CAVALRY),
		
		
		######################################################
		#####               VAEGIR FACTION               #####
		######################################################
		
		## I1 Vaegir Recruit
		(troop_set_class, "trp_n_vaegir_recruit", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_vaegir_recruit", slot_troop_purchase_cost, 10),
		
		## I2 Vaegir Skrimisher
		(troop_set_class, "trp_n_vaegir_skirmisher", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_vaegir_skirmisher", slot_troop_purchase_cost, 15),
		
		## H3 Vaegir Skrimisher
		(troop_set_class, "trp_n_vaegir_raider", CLASS_CAVALRY),
		(troop_set_slot, "trp_n_vaegir_raider", slot_troop_purchase_cost, 50),
		
		
		## A4 Vaegir Bowman
		(troop_set_class, "trp_n_vaegir_bowman", CLASS_RANGED),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_vaegir_bowman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_vaegir_bowman", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_vaegir_bowman", slot_troop_purchase_cost, 400),
		
		## C5 Vaegir Headhunter
		(troop_set_class, "trp_n_vaegir_headhunter", CLASS_CAVALRY),
		(troop_set_slot, "trp_n_vaegir_headhunter", slot_troop_purchase_cost, 900),
		
		## I6 Vaegir Guard
		(troop_set_class, "trp_n_vaegir_guard", CLASS_CAVALRY),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_vaegir_guard", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_vaegir_guard", BONUS_CHARGING_STRIKE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_vaegir_guard", slot_troop_purchase_cost, 1000),
		
		## H7 Vaegir Bogatyr
		(troop_set_class, "trp_n_vaegir_bogatyr", CLASS_CAVALRY),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_vaegir_bogatyr", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_vaegir_bogatyr", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_vaegir_bogatyr", slot_troop_purchase_cost, 1750),
		
		## I1 - Vaegiran Militia
		(troop_set_class, "trp_r_vaegir_militia", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_r_vaegir_militia_1", CLASS_INFANTRY),
		# +2 tier
		(troop_set_class, "trp_r_vaegir_militia_2", CLASS_INFANTRY),
		
		## I3 - Vaegiran Psiloi
		(troop_set_class, "trp_r_vaegir_psiloi", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_r_vaegir_psiloi_1", CLASS_INFANTRY),
		# +2 tier
		(troop_set_class, "trp_r_vaegir_psiloi_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_vaegir_psiloi_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I3 - Vaegiran Peltast
		(troop_set_class, "trp_r_vaegir_peltast", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_r_vaegir_peltast_1", CLASS_INFANTRY),
		# +2 tier
		(troop_set_class, "trp_r_vaegir_peltast_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_vaegir_peltast_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## A2 - Vaegiran Skirmisher
		(troop_set_class, "trp_r_vaegir_skirmisher", CLASS_RANGED),
		# +1 tier
		(troop_set_class, "trp_r_vaegir_skirmisher_1", CLASS_RANGED),
		# +2 tier
		(troop_set_class, "trp_r_vaegir_skirmisher_2", CLASS_RANGED),
		
		## A5 - Vaegiran Longbowman
		(troop_set_class, "trp_r_vaegir_longbowman", CLASS_RANGED),
		(troop_set_slot, "trp_r_vaegir_longbowman", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +1 tier
		(troop_set_class, "trp_r_vaegir_longbowman_1", CLASS_RANGED),
		(troop_set_slot, "trp_r_vaegir_longbowman_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(troop_set_class, "trp_r_vaegir_longbowman_2", CLASS_RANGED),
		(troop_set_slot, "trp_r_vaegir_longbowman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## C3 - Vaegiran Koursores
		(troop_set_class, "trp_r_vaegir_koursores", CLASS_CAVALRY),
		# +1 tier
		(troop_set_class, "trp_r_vaegir_koursores_1", CLASS_CAVALRY),
		# +2 tier
		(troop_set_class, "trp_r_vaegir_koursores_2", CLASS_CAVALRY),
		(troop_set_slot, "trp_r_vaegir_koursores_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## H3 - Vaegiran Pecheneg
		(troop_set_class, "trp_r_vaegir_pecheneg", CLASS_RANGED),
		# +1 tier
		(troop_set_class, "trp_r_vaegir_pecheneg_1", CLASS_RANGED),
		# +2 tier
		(troop_set_class, "trp_r_vaegir_pecheneg_2", CLASS_RANGED),
		(troop_set_slot, "trp_r_vaegir_pecheneg_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I2 - Vaegir Sentry (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_sentry"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_sentry", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_sentry", BONUS_TAX_COLLECTOR, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_sentry", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_sentry_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_sentry_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_sentry_1", BONUS_TAX_COLLECTOR, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_sentry_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_sentry_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_sentry_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_sentry_2", BONUS_TAX_COLLECTOR, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_sentry_2", CLASS_INFANTRY),
		
		## C4 - Vaegir Cavalry Captain (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_cavalrycaptain"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cavalrycaptain", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cavalrycaptain", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cavalrycaptain", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_cavalrycaptain", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_cavalrycaptain_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cavalrycaptain_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cavalrycaptain_1", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cavalrycaptain_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_cavalrycaptain_1", CLASS_CAVALRY),
		(troop_set_slot, "trp_r_vaegir_cavalrycaptain_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_cavalrycaptain_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cavalrycaptain_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cavalrycaptain_2", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cavalrycaptain_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_cavalrycaptain_2", CLASS_CAVALRY),
		(troop_set_slot, "trp_r_vaegir_cavalrycaptain_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I5 - Vaegir Vanguard (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_vanguard"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_vanguard", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_vanguard", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_vanguard", BONUS_SECOND_WIND, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_vanguard", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_vanguard", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_vanguard_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_vanguard_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_vanguard_1", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_vanguard_1", BONUS_SECOND_WIND, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_vanguard_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_vanguard_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_vanguard_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_vanguard_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_vanguard_2", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_vanguard_2", BONUS_SECOND_WIND, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_vanguard_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_vanguard_2", CLASS_INFANTRY),
		
		## C6 - Vaegir Bogatyr (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_bogatyr"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_bogatyr", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_bogatyr", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_bogatyr", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_bogatyr_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_bogatyr_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr_1", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr_1", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_bogatyr_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_bogatyr_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_bogatyr_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_bogatyr_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr_2", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_bogatyr_2", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_bogatyr_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_bogatyr_2", CLASS_CAVALRY),
		
		## A7 - Vaegir Marksman (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_marksman"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_marksman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_marksman", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_marksman", CLASS_RANGED),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_marksman_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_marksman_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman_1", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman_1", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_marksman_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_marksman_1", CLASS_RANGED),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_marksman_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_marksman_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman_2", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_marksman_2", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_marksman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_marksman_2", CLASS_RANGED),
		
		## C3 - Outrider of Nelag (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_scout"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_scout", slot_troop_unique_location, "p_castle_29"), # Nelag Castle (Khergit Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_scout", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_scout", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_scout", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_scout", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_scout", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_scout_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_scout_1", slot_troop_unique_location, "p_castle_29"), # Nelag Castle (Khergit Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_scout_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_scout_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_scout_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_scout_1", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_scout_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_scout_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_scout_2", slot_troop_unique_location, "p_castle_29"), # Nelag Castle (Khergit Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_scout_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_scout_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_scout_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_scout_2", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_scout_2", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_scout_2", CLASS_CAVALRY),
		(troop_set_slot, "trp_r_vaegir_scout_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I4 - Jeirbe Sellsword (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_varagian"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_varagian", slot_troop_unique_location, "p_castle_8"), # Jeirbe Castle (Nord Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_varagian", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_varagian", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_varagian", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_varagian", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_varagian", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_vaegir_varagian", slot_troop_recruit_type, STRT_MERCENARY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_varagian_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_varagian_1", slot_troop_unique_location, "p_castle_8"), # Jeirbe Castle (Nord Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_varagian_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_varagian_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_varagian_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_varagian_1", BONUS_BOUNDLESS_ENDURANCE, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_varagian_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_vaegir_varagian_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_varagian_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_varagian_2", slot_troop_unique_location, "p_castle_8"), # Jeirbe Castle (Nord Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_varagian_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_varagian_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_varagian_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_varagian_2", BONUS_BOUNDLESS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_varagian_2", BONUS_DEDICATED, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_vaegir_varagian_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_vaegir_varagian_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## C5 - Southward Cataphract (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_cataphract"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_cataphract", slot_troop_unique_location, "p_castle_37"), # Dramug Castle (Swadian Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cataphract", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cataphract", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract", BONUS_LOYAL, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_cataphract", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_cataphract", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_cataphract_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_cataphract_1", slot_troop_unique_location, "p_castle_37"), # Dramug Castle (Swadian Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cataphract_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cataphract_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract_1", BONUS_LOYAL, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract_1", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract_1", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_cataphract_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_cataphract_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_vaegir_cataphract_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_vaegir_cataphract_2", slot_troop_unique_location, "p_castle_37"), # Dramug Castle (Swadian Border)
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cataphract_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_vaegir_cataphract_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract_2", BONUS_LOYAL, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract_2", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_vaegir_cataphract_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_vaegir_cataphract_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_vaegir_cataphract_2", CLASS_CAVALRY),
		
		## C4 - Boyars Druzhina (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_boyars_druzhina"), # combat_scripts.py
		(troop_set_slot, "trp_boyars_druzhina", slot_troop_unique_location, "p_town_8"), # Reyvadin
		(call_script, "script_ce_assign_troop_requirement", "trp_boyars_druzhina", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_boyars_druzhina", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_boyars_druzhina", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_boyars_druzhina", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_boyars_druzhina_1"), # combat_scripts.py
		(troop_set_slot, "trp_boyars_druzhina_1", slot_troop_unique_location, "p_town_8"), # Reyvadin
		(call_script, "script_ce_assign_troop_requirement", "trp_boyars_druzhina_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_boyars_druzhina_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina_1", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina_1", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina_1", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_class, "trp_boyars_druzhina_1", CLASS_CAVALRY),
		(troop_set_slot, "trp_boyars_druzhina_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_boyars_druzhina_2"), # combat_scripts.py
		(troop_set_slot, "trp_boyars_druzhina_2", slot_troop_unique_location, "p_town_8"), # Reyvadin
		(call_script, "script_ce_assign_troop_requirement", "trp_boyars_druzhina_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_boyars_druzhina_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina_2", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina_2", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_boyars_druzhina_2", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_class, "trp_boyars_druzhina_2", CLASS_CAVALRY),
		(troop_set_slot, "trp_boyars_druzhina_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## C2 - Huntsman of Khudan (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_khudan_mounted_archer"), # combat_scripts.py
		(troop_set_slot, "trp_khudan_mounted_archer", slot_troop_unique_location, "p_town_9"), # Khudan
		(call_script, "script_ce_assign_troop_requirement", "trp_khudan_mounted_archer", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_khudan_mounted_archer", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_khudan_mounted_archer", BONUS_HUNTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_khudan_mounted_archer", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_khudan_mounted_archer_1"), # combat_scripts.py
		(troop_set_slot, "trp_khudan_mounted_archer_1", slot_troop_unique_location, "p_town_9"), # Khudan
		(call_script, "script_ce_assign_troop_requirement", "trp_khudan_mounted_archer_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_khudan_mounted_archer_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_khudan_mounted_archer_1", BONUS_HUNTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_khudan_mounted_archer_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_khudan_mounted_archer_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_khudan_mounted_archer_2"), # combat_scripts.py
		(troop_set_slot, "trp_khudan_mounted_archer_2", slot_troop_unique_location, "p_town_9"), # Khudan
		(call_script, "script_ce_assign_troop_requirement", "trp_khudan_mounted_archer_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_khudan_mounted_archer_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_khudan_mounted_archer_2", BONUS_HUNTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_khudan_mounted_archer_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_khudan_mounted_archer_2", BONUS_STEADY_AIM, BONUS_UNASSIGNED),
		(troop_set_class, "trp_khudan_mounted_archer_2", CLASS_CAVALRY),
		
		## I3 - Curaw Guardsman (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_curaw_guardsman"), # combat_scripts.py
		(troop_set_slot, "trp_curaw_guardsman", slot_troop_unique_location, "p_town_11"), # Curaw
		(call_script, "script_ce_assign_troop_requirement", "trp_curaw_guardsman", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_curaw_guardsman", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_curaw_guardsman", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_curaw_guardsman", BONUS_SPRINTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_curaw_guardsman", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_curaw_guardsman_1"), # combat_scripts.py
		(troop_set_slot, "trp_curaw_guardsman_1", slot_troop_unique_location, "p_town_11"), # Curaw
		(call_script, "script_ce_assign_troop_requirement", "trp_curaw_guardsman_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_curaw_guardsman_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_curaw_guardsman_1", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_curaw_guardsman_1", BONUS_SPRINTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_curaw_guardsman_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_curaw_guardsman_2"), # combat_scripts.py
		(troop_set_slot, "trp_curaw_guardsman_2", slot_troop_unique_location, "p_town_11"), # Curaw
		(call_script, "script_ce_assign_troop_requirement", "trp_curaw_guardsman_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_curaw_guardsman_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_curaw_guardsman_2", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_curaw_guardsman_2", BONUS_SPRINTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_curaw_guardsman_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_curaw_guardsman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		
		######################################################
		#####              KHERGIT FACTION               #####
		######################################################

		#KHERGITS - STANDARD TROOPS
		
		#I1 Khergit Recruit
		(troop_set_class, "trp_n_khergit_recruit", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_khergit_recruit", slot_troop_purchase_cost, 10),
		
		#H2 Khergit Scout
		(troop_set_class, "trp_n_khergit_scout", CLASS_CAVALRY),
		(troop_set_slot, "trp_n_khergit_scout", slot_troop_purchase_cost, 35),
 
		
		#I3 Khergit Shaman
		(troop_set_class, "trp_n_khergit_shaman", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_khergit_shaman"),
		(call_script, "script_ce_assign_troop_ability", "trp_n_khergit_shaman", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_khergit_scout", slot_troop_purchase_cost, 125),
 
		
		#C3 Khergit Lancer
		(troop_set_class, "trp_n_khergit_shaman", CLASS_CAVALRY),
		(troop_set_slot, "trp_n_khergit_scout", slot_troop_purchase_cost, 75),
 
 		#I4 Khergit Clansman
		(troop_set_class, "trp_n_khergit_clansman", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_khergit_clansman"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_khergit_clansman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_khergit_clansman", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_khergit_clansman", slot_troop_purchase_cost, 225),
		
 		#H5 Khergit Skirmisher
		(troop_set_class, "trp_n_khergit_skirmisher", CLASS_CAVALRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_khergit_skirmisher"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_khergit_skirmisher", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_khergit_skirmisher", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_khergit_skirmisher", slot_troop_purchase_cost, 500),
		
 		#C6 Khergit Keshig
		(troop_set_class, "trp_n_khergit_keshig", CLASS_CAVALRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_khergit_keshig"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_khergit_keshig", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_khergit_keshig", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_khergit_keshig", slot_troop_purchase_cost, 950),
		
		
		#Khergit Slave I1
		(troop_set_class, "trp_r_khergit_slave", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_r_khergit_slave_1", CLASS_INFANTRY),
		# +2 tier
		(troop_set_class, "trp_r_khergit_slave_2", CLASS_INFANTRY),
		
		#Khergit Outcast I2
		(troop_set_class, "trp_r_khergit_outcast", CLASS_INFANTRY),
		#+1 tier
		(troop_set_class, "trp_r_khergit_outcast_1", CLASS_INFANTRY),
		#+2 tier
		(troop_set_class, "trp_r_khergit_outcast_2", CLASS_INFANTRY),
		
		#Khergit Surcin A2
		(troop_set_class, "trp_r_khergit_surcin", CLASS_RANGED),
		#+1 tier
		(troop_set_class, "trp_r_khergit_surcin_1", CLASS_RANGED),
		#+2 tier
		(troop_set_class, "trp_r_khergit_surcin_2", CLASS_RANGED),
		
		#Khergit Scout C2
		(troop_set_class, "trp_r_khergit_scout", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_scout", slot_troop_recruit_type, STRT_MERCENARY),
		#+1 tier
		(troop_set_class, "trp_r_khergit_scout_1", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_scout_1", slot_troop_recruit_type, STRT_MERCENARY),
		#+2 tier
		(troop_set_class, "trp_r_khergit_scout_2", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_scout", slot_troop_recruit_type, STRT_MERCENARY),
		
		#Khergit Asud I3
		(troop_set_class, "trp_r_khergit_asud", CLASS_INFANTRY),
		#+1 tier
		(troop_set_class, "trp_r_khergit_asud_1", CLASS_INFANTRY),
		#+2 tier
		(troop_set_class, "trp_r_khergit_asud_2", CLASS_INFANTRY),
		(troop_set_slot,  "trp_r_khergit_asud_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		#Khergit Kharvaach A3
		(troop_set_class, "trp_r_khergit_kharvaach", CLASS_RANGED),
		#+1 tier
		(troop_set_class, "trp_r_khergit_kharvaach_1", CLASS_RANGED),
		#+2 tier
		(troop_set_class, "trp_r_khergit_kharvaach_2", CLASS_RANGED),
		(troop_set_slot,  "trp_r_khergit_kharvaach_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		#Khergit Morici C3
		(troop_set_class, "trp_r_khergit_morici", CLASS_CAVALRY),
		#+1 tier
		(troop_set_class, "trp_r_khergit_morici_1", CLASS_CAVALRY),
		#+2 tier
		(troop_set_class, "trp_r_khergit_morici_2", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_morici_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		#Khergit Abaci H3
		(troop_set_class, "trp_r_khergit_abaci", CLASS_CAVALRY),
		#+1 tier
		(troop_set_class, "trp_r_khergit_abaci_1", CLASS_CAVALRY),
		#+2 tier
		(troop_set_class, "trp_r_khergit_abaci_2", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_abaci_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		#Khergit Skirmisher H4
		(troop_set_class, "trp_r_khergit_skirmisher", CLASS_CAVALRY),
		#+1 tier
		(troop_set_class, "trp_r_khergit_skirmisher_1", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_skirmisher_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		#+2 tier
		(troop_set_class, "trp_r_khergit_skirmisher_2", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_skirmisher_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		#Khergit Torguu C5
		(troop_set_class, "trp_r_khergit_torguu", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_torguu", slot_troop_recruit_type, STRT_NOBLEMAN),
		#+1 tier
		(troop_set_class, "trp_r_khergit_torguu_1", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_torguu_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		#+2 tier
		(troop_set_class, "trp_r_khergit_torguu_2", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_torguu_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		#Khergit Parthian H5
		(troop_set_class, "trp_r_khergit_parthian", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_parthian", slot_troop_recruit_type, STRT_NOBLEMAN),
		#+1 tier
		(troop_set_class, "trp_r_khergit_parthian_1", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_parthian_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		#+2 tier
		(troop_set_class, "trp_r_khergit_parthian_2", CLASS_CAVALRY),
		(troop_set_slot,  "trp_r_khergit_parthian_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		#KHERGITS - AFFILIATED TROOPS
		
		#Khergit Shaman I2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_shaman"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_shaman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_shaman", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_shaman", BONUS_INSPIRING, BONUS_UNASSIGNED),
		#(troop_set_slot, "trp_r_khergit_shaman", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_shaman", CLASS_INFANTRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_shaman_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_shaman_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_shaman_1", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_shaman_1", BONUS_INSPIRING, BONUS_UNASSIGNED),
		#(troop_set_slot, "trp_r_khergit_shaman", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_shaman_1", CLASS_INFANTRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_shaman_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_shaman_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_shaman_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_shaman_2", BONUS_INSPIRING, BONUS_UNASSIGNED),
		#(troop_set_slot, "trp_r_khergit_shaman", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_shaman_2", CLASS_INFANTRY),
		
		# Khergit Raider C3
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_raider"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_raider", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_raider", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_raider", BONUS_TAX_COLLECTOR, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_shaman", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_khergit_raider", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_raider_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_raider_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_raider_1", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_raider_1", BONUS_TAX_COLLECTOR, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_shaman", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_khergit_raider_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_raider_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_raider_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_raider_2", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_raider_2", BONUS_TAX_COLLECTOR, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_raider_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_raider_2", CLASS_CAVALRY),
		
		# Khergit Lancer C4
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_lancer"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_lancer", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_lancer", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_lancer", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_khergit_lancer", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_lancer_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_lancer_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_lancer_1", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_lancer_1", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_khergit_lancer_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_lancer_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_lancer_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_lancer_2", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_lancer_2", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_lancer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_lancer_2", CLASS_CAVALRY),
		
		#Khergit Clansman I4
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_clansman"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_clansman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_clansman", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_clansman", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_clansman", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_khergit_clansman", CLASS_INFANTRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_clansman_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_clansman_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_clansman_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_clansman_1", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_clansman_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_clansman_1", CLASS_INFANTRY),
		#+2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_clansman_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_clansman_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_clansman_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_clansman_2", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_clansman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_clansman_2", CLASS_INFANTRY),
		
		#Khergit Noyan C6
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_noyan"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noyan", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noyan", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noyan", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_noyan", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_noyan", CLASS_CAVALRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_noyan_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noyan_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noyan_1", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noyan_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_noyan_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_noyan_1", CLASS_CAVALRY),
		#+2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_noyan_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noyan_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noyan_2", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noyan_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_noyan_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_noyan_2", CLASS_CAVALRY),
		
		#Khergit Bahatur H7
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_bahatur"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_bahatur", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_bahatur", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_bahatur", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_bahatur", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_bahatur", CLASS_CAVALRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_bahatur_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_bahatur_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_bahatur_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_bahatur_1", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_bahatur_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_bahatur_1", CLASS_CAVALRY),
		#+2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_bahatur_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_bahatur_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_bahatur_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_bahatur_2", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_bahatur_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_bahatur_2", CLASS_CAVALRY),
		
		#KHERGIT UNIQUE TROOPS
		#Khergit Orlok H4
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_orlok"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_orlok", slot_troop_unique_location, "p_town_17"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_orlok", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_orlok", BONUS_SIEGE_GENERAL, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_orlok", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		#(troop_set_slot, "trp_r_khergit_orlok", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_khergit_orlok", CLASS_CAVALRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_orlok_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_orlok_1", slot_troop_unique_location, "p_town_17"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_orlok_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_orlok_1", BONUS_SIEGE_GENERAL, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_orlok_1", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_orlok_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_orlok_1", CLASS_CAVALRY),
		#+2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_orlok_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_orlok_2", slot_troop_unique_location, "p_town_17"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_orlok_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_orlok_2", BONUS_SIEGE_GENERAL, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_orlok_2", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_orlok_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_orlok_2", CLASS_CAVALRY),
		
		#Khergit Narcarra C4
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_narcarra"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_narcarra", slot_troop_unique_location, "p_town_14"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_narcarra", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_narcarra", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_narcarra", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		#(troop_set_slot, "trp_r_khergit_narcarra", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_khergit_narcarra", CLASS_CAVALRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_narcarra_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_narcarra_1", slot_troop_unique_location, "p_town_14"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_narcarra_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_narcarra_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_narcarra_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_narcarra_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_narcarra_1", CLASS_CAVALRY),
		#+2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_narcarra_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_narcarra_2", slot_troop_unique_location, "p_town_14"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_narcarra_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_narcarra_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_narcarra_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_narcarra_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_narcarra_2", CLASS_CAVALRY),
		
		#Khergit Noker I6
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_noker"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_noker", slot_troop_unique_location, "p_town_18"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noker", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noker", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noker", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noker", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_noker", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_noker", CLASS_INFANTRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_noker_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_noker_1", slot_troop_unique_location, "p_town_18"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noker_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noker_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noker_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noker_1", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_noker_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_noker_1", CLASS_INFANTRY),
		#+2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_noker_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_noker_2", slot_troop_unique_location, "p_town_18"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noker_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_noker_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noker_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_noker_2", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_noker_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_noker_2", CLASS_INFANTRY),
		
		#Khergit Keshig C7
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_keshig"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_keshig", slot_troop_unique_location, "p_town_10"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_keshig", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_keshig", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_keshig", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_keshig", CLASS_CAVALRY),
		#+1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_keshig_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_keshig_1", slot_troop_unique_location, "p_town_10"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig_1", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_keshig_1", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_keshig_1", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_keshig_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_keshig_1", CLASS_CAVALRY),
		#+2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_khergit_keshig_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_khergit_keshig_2", slot_troop_unique_location, "p_town_10"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_khergit_keshig_2", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_keshig_2", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_khergit_keshig_2", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_khergit_keshig_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_khergit_keshig_2", CLASS_CAVALRY),

		
		######################################################
		#####                NORD FACTION                #####
		######################################################
		
		## I1 Nordic Recruit
		(troop_set_class, "trp_n_nordic_recruit", CLASS_INFANTRY),
		#(troop_set_slot, "trp_n_nordic_recruit", slot_troop_purchase_cost, 10),
		
		## I3 Nordic Skald
		(troop_set_class, "trp_n_nordic_skald", CLASS_INFANTRY),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_nordic_skald", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_nordic_skald", BONUS_STORYTELLER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_nordic_skald", slot_troop_purchase_cost, 45),
		
		## A3 Nordic Tracker
		(troop_set_class, "trp_n_nordic_tracker", CLASS_RANGED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_nordic_tracker", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_nordic_tracker", slot_troop_purchase_cost, 185),
		
		## I4 Nordic Spearman
		(troop_set_class, "trp_n_nordic_spearman", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_nordic_tracker", slot_troop_purchase_cost, 225),
		
		## C6 Nordic Retainer
		(troop_set_class, "trp_n_nordic_retainer", CLASS_CAVALRY),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_nordic_retainer", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_nordic_retainer", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_nordic_retainer", slot_troop_purchase_cost, 1100),
		
		## A6 Nordic Retinue Archer
		(troop_set_class, "trp_n_nordic_retinue_archer", CLASS_RANGED),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_nordic_retinue_archer", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_nordic_retinue_archer", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_nordic_retinue_archer", slot_troop_purchase_cost, 850),

		## I7 Nordic Berserker
		(troop_set_class, "trp_n_nordic_berserker", CLASS_INFANTRY),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_nordic_berserker", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_nordic_berserker", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_nordic_berserker", slot_troop_purchase_cost, 2500),
		
		## A1 - Nordic Hunter
		(troop_set_class, "trp_r_nord_hunter", CLASS_RANGED),
		# +1
		(troop_set_class, "trp_r_nord_hunter_1", CLASS_RANGED),
		# +2
		(troop_set_class, "trp_r_nord_hunter_2", CLASS_RANGED),
		
		## I1 - Nordic Bondsman
		(troop_set_class, "trp_r_nord_bondsman", CLASS_INFANTRY),
		# +1
		(troop_set_class, "trp_r_nord_bondsman_1", CLASS_INFANTRY),
		# +2
		(troop_set_class, "trp_r_nord_bondsman_2", CLASS_INFANTRY),
		
		## I2 - Nordic Peasant
		(troop_set_class, "trp_r_nord_peasant", CLASS_INFANTRY),
		# +1
		(troop_set_class, "trp_r_nord_peasant_1", CLASS_INFANTRY),
		# +2
		(troop_set_class, "trp_r_nord_peasant_2", CLASS_INFANTRY),
		
		## A3 - Nordic Retinue Archer
		(troop_set_class, "trp_r_nord_retinue_archer", CLASS_RANGED),
		# +1
		(troop_set_class, "trp_r_nord_retinue_archer_1", CLASS_RANGED),
		# +2
		(troop_set_class, "trp_r_nord_retinue_archer_2", CLASS_RANGED),
		(troop_set_slot, "trp_r_nord_retinue_archer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I3 - Shield Maiden
		(troop_set_class, "trp_r_nord_shield_maiden", CLASS_INFANTRY),
		# +1
		(troop_set_class, "trp_r_nord_shield_maiden_1", CLASS_INFANTRY),
		# +2
		(troop_set_class, "trp_r_nord_shield_maiden_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_shield_maiden_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I3 - Nordic Raider (Bandit)
		(troop_set_class, "trp_r_nord_raider", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_raider"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_raider", PREREQ_DISHONORABLE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_raider", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_raider", BONUS_STEALTHY, BONUS_UNASSIGNED),
		# +1
		(troop_set_class, "trp_r_nord_raider_1", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_raider_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_raider_1", PREREQ_DISHONORABLE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_raider_1", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_raider_1", BONUS_STEALTHY, BONUS_UNASSIGNED),
		# +2
		(troop_set_class, "trp_r_nord_raider_2", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_raider_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_raider_2", PREREQ_DISHONORABLE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_raider_2", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_raider_2", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_raider_2", BONUS_SECOND_WIND, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_raider_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I4 - Nordic Retainer
		(troop_set_class, "trp_r_nord_retainer", CLASS_INFANTRY),
		# +1
		(troop_set_class, "trp_r_nord_retainer_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_retainer_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2
		(troop_set_class, "trp_r_nord_retainer_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_retainer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I4 - Nordic Spearman
		(troop_set_class, "trp_r_nord_spearman", CLASS_INFANTRY),
		# +1
		(troop_set_class, "trp_r_nord_spearman_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_spearman_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2
		(troop_set_class, "trp_r_nord_spearman_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_spearman_2", slot_troop_recruit_type, STRT_NOBLEMAN),

		## A4 - Nordic Skirmisher
		(troop_set_class, "trp_r_nord_skirmisher", CLASS_INFANTRY),
		# +1
		(troop_set_class, "trp_r_nord_skirmisher_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_skirmisher_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		(troop_set_class, "trp_r_nord_skirmisher_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_skirmisher_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I4 - Jomsviking
		(troop_set_class, "trp_r_nord_jomsviking", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_jomsviking", slot_troop_recruit_type, STRT_MERCENARY),
		# +1
		(troop_set_class, "trp_r_nord_jomsviking_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_jomsviking_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2
		(troop_set_class, "trp_r_nord_jomsviking_2", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_jomsviking_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## A5 - Varangian Archer (Mercenary)
		(troop_set_class, "trp_r_nord_varangian_archer", CLASS_RANGED),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_varangian_archer"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_varangian_archer", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_varangian_archer", slot_troop_recruit_type, STRT_NOBLEMAN),
		#+1
		(troop_set_class, "trp_r_nord_varangian_archer_1", CLASS_RANGED),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_varangian_archer_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_varangian_archer_1", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_varangian_archer_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2
		(troop_set_class, "trp_r_nord_varangian_archer_2", CLASS_RANGED),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_varangian_archer_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_varangian_archer_2", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_varangian_archer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I7 - Nordic Hirdmadr
		(troop_set_class, "trp_r_nord_hirdmadr", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_hirdmadr", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +1
		(troop_set_class, "trp_r_nord_hirdmadr_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_hirdmadr_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2
		(troop_set_class, "trp_r_nord_hirdmadr_1", CLASS_INFANTRY),
		(troop_set_slot, "trp_r_nord_hirdmadr_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I7 - Varangian Guard (Mercenary)
		(troop_set_class, "trp_r_nord_varangian_guard", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_varangian_guard"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_varangian_guard", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_varangian_guard", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +1
		(troop_set_class, "trp_r_nord_varangian_guard_1", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_varangian_guard_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_varangian_guard_1", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_varangian_guard_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2
		(troop_set_class, "trp_r_nord_varangian_guard_2", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_varangian_guard_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_varangian_guard_2", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_varangian_guard_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## C3 - Jelbegi Lancer (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_jelbegi_lancer"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_jelbegi_lancer", slot_troop_unique_location, "p_castle_36"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_jelbegi_lancer", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_jelbegi_lancer", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_jelbegi_lancer", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_jelbegi_lancer", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_nord_jelbegi_lancer", CLASS_CAVALRY),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_jelbegi_lancer_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_jelbegi_lancer_1", slot_troop_unique_location, "p_castle_36"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_jelbegi_lancer_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_jelbegi_lancer_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_jelbegi_lancer_1", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_jelbegi_lancer_1", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_nord_jelbegi_lancer_1", CLASS_CAVALRY),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_jelbegi_lancer_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_jelbegi_lancer_2", slot_troop_unique_location, "p_castle_36"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_jelbegi_lancer_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_jelbegi_lancer_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_jelbegi_lancer_2", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_jelbegi_lancer_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_jelbegi_lancer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_jelbegi_lancer_2", CLASS_CAVALRY),
		
		## C5 - Thane of Sargoth (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_thane"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_thane", slot_troop_unique_location, "p_town_1"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_thane", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_thane", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_thane", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_thane", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_thane", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_thane", CLASS_CAVALRY),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_thane_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_thane_1", slot_troop_unique_location, "p_town_1"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_thane_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_thane_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_thane_1", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_thane_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_thane_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_thane_1", CLASS_CAVALRY),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_thane_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_thane_2", slot_troop_unique_location, "p_town_1"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_thane_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_thane_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_thane_2", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_thane_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_thane_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_thane_2", CLASS_CAVALRY),
		
		## C6 - Valkyrie of Tihr (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_valkyrie"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_valkyrie", slot_troop_unique_location, "p_town_2"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_valkyrie", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_valkyrie", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_valkyrie", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_valkyrie", CLASS_CAVALRY),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_valkyrie_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_valkyrie_1", slot_troop_unique_location, "p_town_2"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_valkyrie_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_valkyrie_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie_1", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie_1", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie_1", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_valkyrie_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_valkyrie_1", CLASS_CAVALRY),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_valkyrie_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_valkyrie_2", slot_troop_unique_location, "p_town_2"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_valkyrie_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_valkyrie_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie_2", BONUS_AGILE_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie_2", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_valkyrie_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_valkyrie_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_valkyrie_2", CLASS_CAVALRY),
		
		## A2 - Maiden of Aldelen (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_maiden"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_maiden", slot_troop_unique_location, "p_village_61"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_maiden", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_maiden", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_maiden", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_maiden", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_nord_maiden", CLASS_RANGED),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_maiden_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_maiden_1", slot_troop_unique_location, "p_village_61"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_maiden_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_maiden_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_maiden_1", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_maiden_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_nord_maiden_1", CLASS_RANGED),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_maiden_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_nord_maiden_2", slot_troop_unique_location, "p_village_61"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_maiden_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_maiden_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_maiden_2", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_maiden_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_nord_maiden_2", CLASS_RANGED),
		
		## A4 - Nordic Scout (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_scout"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_scout", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_scout", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_scout", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_nord_scout", CLASS_RANGED),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_scout_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_scout_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_scout_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_scout_1", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_scout_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_scout_1", CLASS_RANGED),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_scout_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_scout_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_scout_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_scout_2", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_scout_2", BONUS_HUNTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_scout_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_scout_2", CLASS_RANGED),
		
		## I3 - Nordic Skald (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_skald"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_skald", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_skald", BONUS_STORYTELLER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_nord_skald", CLASS_INFANTRY),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_skald_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_skald_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_skald_1", BONUS_STORYTELLER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_skald_1", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_nord_skald_1", CLASS_INFANTRY),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_skald_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_skald_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_skald_2", BONUS_STORYTELLER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_skald_2", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_skald_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_skald_2", CLASS_INFANTRY),
		
		## I6 - Nordic Godi (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_godi"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_godi", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi", BONUS_CHARGING_STRIKE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_godi", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_godi", CLASS_INFANTRY),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_godi_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_godi_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi_1", BONUS_CHARGING_STRIKE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi_1", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi_1", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_godi_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_godi_1", CLASS_INFANTRY),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_godi_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_godi_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi_2", BONUS_CHARGING_STRIKE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi_2", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_godi_2", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_godi_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_godi_2", CLASS_INFANTRY),
		
		## I7 - Nord Huscarl (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_huscarl"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_huscarl", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl", BONUS_SAVAGERY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_huscarl", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_huscarl", CLASS_INFANTRY),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_huscarl_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_huscarl_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl_1", BONUS_SAVAGERY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl_1", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl_1", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_huscarl_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_huscarl_1", CLASS_INFANTRY),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_huscarl_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_huscarl_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl_2", BONUS_SAVAGERY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl_2", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_huscarl_2", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_huscarl_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_huscarl_2", CLASS_INFANTRY),
		
		# Bandits
		## I5 - Nord Berserker (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_berserker"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_berserker", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker", BONUS_CHARGING_STRIKE , BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_berserker", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_berserker", CLASS_INFANTRY),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_berserker_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_berserker_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker_1", BONUS_CHARGING_STRIKE , BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker_1", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_berserker_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_berserker_1", CLASS_INFANTRY),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_nord_berserker_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_nord_berserker_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker_2", BONUS_CHARGING_STRIKE , BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker_2", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_nord_berserker_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_nord_berserker_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_nord_berserker_2", CLASS_INFANTRY),
		
		######################################################
		#####               RHODOK FACTION               #####
		######################################################
		
		## H5 Khergit Skirmisher
		(troop_set_class, "trp_n_khergit_skirmisher", CLASS_CAVALRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_khergit_skirmisher"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_khergit_skirmisher", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_khergit_skirmisher", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_khergit_skirmisher", slot_troop_purchase_cost, 500),
		
		## I1 Rhodok Recruit
		(troop_set_class, "trp_n_rhodok_recruit", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_rhodok_recruit", slot_troop_purchase_cost, 10),
		
		## I3 Rhodok Footman
		(troop_set_class, "trp_n_rhodok_footman", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_rhodok_footman", slot_troop_purchase_cost, 250),
		
		## A3 Rhodok Ranger
		(troop_set_class, "trp_n_rhodok_ranger", CLASS_RANGED),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_rhodok_ranger"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_rhodok_ranger", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_rhodok_ranger", BONUS_RAPID_RELOAD, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_rhodok_ranger", slot_troop_purchase_cost, 250),
		
		## I4 Rhodok Halberdier
		(troop_set_class, "trp_n_rhodok_halberdier", CLASS_INFANTRY),
		(troop_set_slot, "trp_n_rhodok_halberdier", slot_troop_purchase_cost, 750),
		
		## I6 Rhodok Pikeman
		(troop_set_class, "trp_n_rhodok_pikeman", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_rhodok_pikeman"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_rhodok_pikeman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_rhodok_pikeman", BONUS_TIGHT_FORMATION, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_rhodok_pikeman", slot_troop_purchase_cost, 2500),
		
		## A6 Rhodok Siege Breaker
		(troop_set_class, "trp_n_rhodok_siege_breaker", CLASS_RANGED),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_rhodok_siege_breaker"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_rhodok_siege_breaker", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_rhodok_siege_breaker", BONUS_FIRING_CAPTAIN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_rhodok_siege_breaker", slot_troop_purchase_cost, 2500),
		
		## I7 Rhodok Foot Knight
		(troop_set_class, "trp_n_rhodok_foot_knight", CLASS_INFANTRY),
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_n_rhodok_foot_knight"),
		(call_script, "script_ce_assign_troop_requirement", "trp_n_rhodok_foot_knight", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_n_rhodok_siege_breaker", BONUS_RALLYING_STRIKE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_n_rhodok_foot_knight", slot_troop_purchase_cost, 4000),
		
		
		
		
		## I1 - Rhodok Militia
		(troop_set_class, "trp_rhodok_militia", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_rhodok_militia_1", CLASS_INFANTRY),
		# +2 tier
		(troop_set_class, "trp_rhodok_militia_2", CLASS_INFANTRY),
		
		## A2 - Rhodok Militia Archer
		(troop_set_class, "trp_rhodok_militia_archer", CLASS_RANGED),
		# +1 tier
		(troop_set_class, "trp_rhodok_militia_archer_1", CLASS_RANGED),
		# +2 tier
		(troop_set_class, "trp_rhodok_militia_archer_2", CLASS_RANGED),
		
		## A3 - Rhodok Crossbowman
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_crossbowman"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_crossbowman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_crossbowman", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_crossbowman", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_rhodok_crossbowman", CLASS_RANGED),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_crossbowman_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_crossbowman_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_crossbowman_1", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_crossbowman_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_rhodok_crossbowman_1", CLASS_RANGED),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_crossbowman_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_crossbowman_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_crossbowman_2", BONUS_SUPPLY_RUNNER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_crossbowman_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_rhodok_crossbowman_2", CLASS_RANGED),
		
		## I3 - Rhodok Footman
		(troop_set_class, "trp_rhodok_trained_militia", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_rhodok_trained_militia_1", CLASS_INFANTRY),
		# +2 tier
		(troop_set_class, "trp_rhodok_trained_militia_2", CLASS_INFANTRY),
		
		## I3 - Rhodok Pikeman
		(troop_set_class, "trp_rhodok_pikeman", CLASS_INFANTRY),
		# +1 tier
		(troop_set_class, "trp_rhodok_pikeman_1", CLASS_INFANTRY),
		# +2 tier
		(troop_set_class, "trp_rhodok_pikeman_2", CLASS_INFANTRY),
		# (troop_set_slot, "trp_rhodok_pikeman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## A4 - Rhodok Arbalestier
		(troop_set_class, "trp_rhodok_arbalestier", CLASS_RANGED),
		# +1 tier
		(troop_set_class, "trp_rhodok_arbalestier_1", CLASS_RANGED),
		# (troop_set_slot, "trp_rhodok_arbalestier_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		# +2 tier
		(troop_set_class, "trp_rhodok_arbalestier_2", CLASS_RANGED),
		# (troop_set_slot, "trp_rhodok_arbalestier_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		## I3 - Rhodok Vanguard (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_vanguard"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_vanguard", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_vanguard", BONUS_SHIELD_BASHER, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_rhodok_vanguard", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_vanguard", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_vanguard_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_vanguard_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_vanguard_1", BONUS_SHIELD_BASHER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_vanguard_1", BONUS_SAVAGE_BASH, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_rhodok_vanguard_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_vanguard_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_vanguard_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_vanguard_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_vanguard_2", BONUS_SHIELD_BASHER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_vanguard_2", BONUS_SAVAGE_BASH, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_rhodok_vanguard_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_vanguard_2", CLASS_INFANTRY),
		
		## I5 - Highland Pikeman (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_highland_pikeman"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_highland_pikeman", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_highland_pikeman", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_highland_pikeman", BONUS_TIGHT_FORMATION, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_rhodok_highland_pikeman", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_highland_pikeman", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_highland_pikeman_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_highland_pikeman_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_highland_pikeman_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_highland_pikeman_1", BONUS_TIGHT_FORMATION, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_highland_pikeman_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_highland_pikeman_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_highland_pikeman_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_highland_pikeman_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_highland_pikeman_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_highland_pikeman_2", BONUS_TIGHT_FORMATION, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_highland_pikeman_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_highland_pikeman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_highland_pikeman_2", CLASS_INFANTRY),
		
		## A6 - Siege-Breaker Crossbowman (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_siege_breaker"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_siege_breaker", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_breaker", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_breaker", BONUS_RAPID_RELOAD, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_siege_breaker", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_siege_breaker", CLASS_RANGED),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_siege_breaker_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_siege_breaker_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_breaker_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_breaker_1", BONUS_RAPID_RELOAD, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_siege_breaker_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_siege_breaker_1", CLASS_RANGED),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_siege_breaker_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_siege_breaker_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_breaker_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_breaker_2", BONUS_RAPID_RELOAD, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_breaker_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_siege_breaker_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_siege_breaker_2", CLASS_RANGED),
		
		## I6 - Hedge Knight (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_hedge_knight"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_hedge_knight", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight", BONUS_SECOND_WIND, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_hedge_knight", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_hedge_knight", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_hedge_knight_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_hedge_knight_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight_1", BONUS_SECOND_WIND, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight_1", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_hedge_knight_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_hedge_knight_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_hedge_knight_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_hedge_knight_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight_2", BONUS_SECOND_WIND, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_hedge_knight_2", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_hedge_knight_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_hedge_knight_2", CLASS_INFANTRY),

		## A6 - Siege Commander
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_siege_commander"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_siege_commander", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_commander", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_commander", BONUS_FIRING_CAPTAIN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_siege_commander", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_siege_commander", CLASS_RANGED),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_siege_commander_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_siege_commander_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_commander_1", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_commander_1", BONUS_FIRING_CAPTAIN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_siege_commander_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_siege_commander_1", CLASS_RANGED),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_siege_commander_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_siege_commander_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_commander_2", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_siege_commander_2", BONUS_FIRING_CAPTAIN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_siege_commander_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_siege_commander_2", CLASS_RANGED),

		## I6 - Mercenary Captain
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_mercenary_captain"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_mercenary_captain", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_mercenary_captain", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_mercenary_captain", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_mercenary_captain", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_mercenary_captain", CLASS_INFANTRY),
		# +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_mercenary_captain_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_mercenary_captain_1", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_mercenary_captain_1", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_mercenary_captain_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_mercenary_captain_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_mercenary_captain_1", CLASS_INFANTRY),
		# +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_mercenary_captain_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_mercenary_captain_2", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_mercenary_captain_2", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_mercenary_captain_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_mercenary_captain_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_rhodok_mercenary_captain_2", CLASS_INFANTRY),
		
		## H3 - Jamiche Border Guard (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_jamiche_border_guard"), # combat_scripts.py
		(troop_set_slot, "trp_jamiche_border_guard", slot_troop_unique_location, "p_castle_9"),
		(call_script, "script_ce_assign_troop_requirement", "trp_jamiche_border_guard", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_jamiche_border_guard", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jamiche_border_guard", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jamiche_border_guard", BONUS_LOYAL, BONUS_UNASSIGNED),
		(troop_set_class, "trp_jamiche_border_guard", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_jamiche_border_guard_1"), # combat_scripts.py
		(troop_set_slot, "trp_jamiche_border_guard_1", slot_troop_unique_location, "p_castle_9"),
		(call_script, "script_ce_assign_troop_requirement", "trp_jamiche_border_guard_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_jamiche_border_guard_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jamiche_border_guard_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jamiche_border_guard_1", BONUS_LOYAL, BONUS_UNASSIGNED),
		(troop_set_class, "trp_jamiche_border_guard_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_jamiche_border_guard_2"), # combat_scripts.py
		(troop_set_slot, "trp_jamiche_border_guard_2", slot_troop_unique_location, "p_castle_9"),
		(call_script, "script_ce_assign_troop_requirement", "trp_jamiche_border_guard_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_jamiche_border_guard_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jamiche_border_guard_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jamiche_border_guard_2", BONUS_LOYAL, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_jamiche_border_guard_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_jamiche_border_guard_2", CLASS_CAVALRY),
		
		## I6 - Veluca Pikeman Captain (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_veluca_pikeman"), # combat_scripts.py
		(troop_set_slot, "trp_veluca_pikeman", slot_troop_unique_location, "p_town_3"),
		(call_script, "script_ce_assign_troop_requirement", "trp_veluca_pikeman", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_veluca_pikeman", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_veluca_pikeman", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_veluca_pikeman", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_veluca_pikeman", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_veluca_pikeman", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_veluca_pikeman_1"), # combat_scripts.py
		(troop_set_slot, "trp_veluca_pikeman_1", slot_troop_unique_location, "p_town_3"),
		(call_script, "script_ce_assign_troop_requirement", "trp_veluca_pikeman_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_veluca_pikeman_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_veluca_pikeman_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_veluca_pikeman_1", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_veluca_pikeman_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_veluca_pikeman_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_veluca_pikeman_2"), # combat_scripts.py
		(troop_set_slot, "trp_veluca_pikeman_2", slot_troop_unique_location, "p_town_3"),
		(call_script, "script_ce_assign_troop_requirement", "trp_veluca_pikeman_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_veluca_pikeman_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_veluca_pikeman_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_veluca_pikeman_2", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_veluca_pikeman_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_veluca_pikeman_2", CLASS_INFANTRY),
		
		## I4 - Grunwalder Voulgiers (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_grunwalder_voulgiers"), # combat_scripts.py
		(troop_set_slot, "trp_grunwalder_voulgiers", slot_troop_unique_location, "p_castle_28"),
		(call_script, "script_ce_assign_troop_requirement", "trp_grunwalder_voulgiers", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_grunwalder_voulgiers", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_grunwalder_voulgiers", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_grunwalder_voulgiers", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(troop_set_class, "trp_grunwalder_voulgiers", CLASS_INFANTRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_grunwalder_voulgiers_1"), # combat_scripts.py
		(troop_set_slot, "trp_grunwalder_voulgiers_1", slot_troop_unique_location, "p_castle_28"),
		(call_script, "script_ce_assign_troop_requirement", "trp_grunwalder_voulgiers_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_grunwalder_voulgiers_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_grunwalder_voulgiers_1", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_grunwalder_voulgiers_1", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_grunwalder_voulgiers_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_grunwalder_voulgiers_1", CLASS_INFANTRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_grunwalder_voulgiers_2"), # combat_scripts.py
		(troop_set_slot, "trp_grunwalder_voulgiers_2", slot_troop_unique_location, "p_castle_28"),
		(call_script, "script_ce_assign_troop_requirement", "trp_grunwalder_voulgiers_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_grunwalder_voulgiers_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_grunwalder_voulgiers_2", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_grunwalder_voulgiers_2", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_grunwalder_voulgiers_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_grunwalder_voulgiers_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_grunwalder_voulgiers_2", CLASS_INFANTRY),
		
		## C3 - Ergellon Lancer (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_ergellon_lancer"), # combat_scripts.py
		(troop_set_slot, "trp_ergellon_lancer", slot_troop_unique_location, "p_castle_15"),
		(call_script, "script_ce_assign_troop_requirement", "trp_ergellon_lancer", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_ergellon_lancer", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_ergellon_lancer", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_ergellon_lancer", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_ergellon_lancer", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_ergellon_lancer_1"), # combat_scripts.py
		(troop_set_slot, "trp_ergellon_lancer_1", slot_troop_unique_location, "p_castle_15"),
		(call_script, "script_ce_assign_troop_requirement", "trp_ergellon_lancer_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_ergellon_lancer_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_ergellon_lancer_1", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_ergellon_lancer_1", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_ergellon_lancer_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_ergellon_lancer_2"), # combat_scripts.py
		(troop_set_slot, "trp_ergellon_lancer_2", slot_troop_unique_location, "p_castle_15"),
		(call_script, "script_ce_assign_troop_requirement", "trp_ergellon_lancer_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_ergellon_lancer_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_ergellon_lancer_2", BONUS_DISCIPLINED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_ergellon_lancer_2", BONUS_GRACEFUL_RIDER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_ergellon_lancer_2", BONUS_DEVOTED, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_ergellon_lancer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_ergellon_lancer_2", CLASS_CAVALRY),
		
		## A3 - Yaleni Dyoken (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_yaleni_dyoken"), # combat_scripts.py
		(troop_set_slot, "trp_yaleni_dyoken", slot_troop_unique_location, "p_town_15"),
		(call_script, "script_ce_assign_troop_requirement", "trp_yaleni_dyoken", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_yaleni_dyoken", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_yaleni_dyoken", BONUS_BOUNDLESS_ENDURANCE, BONUS_UNASSIGNED),
		(troop_set_class, "trp_yaleni_dyoken", CLASS_RANGED),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_yaleni_dyoken_1"), # combat_scripts.py
		(troop_set_slot, "trp_yaleni_dyoken_1", slot_troop_unique_location, "p_town_15"),
		(call_script, "script_ce_assign_troop_requirement", "trp_yaleni_dyoken_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_yaleni_dyoken_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_yaleni_dyoken_1", BONUS_BOUNDLESS_ENDURANCE, BONUS_UNASSIGNED),
		(troop_set_class, "trp_yaleni_dyoken_1", CLASS_RANGED),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_yaleni_dyoken_2"), # combat_scripts.py
		(troop_set_slot, "trp_yaleni_dyoken_2", slot_troop_unique_location, "p_town_15"),
		(call_script, "script_ce_assign_troop_requirement", "trp_yaleni_dyoken_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_yaleni_dyoken_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_yaleni_dyoken_2", BONUS_BOUNDLESS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_yaleni_dyoken_2", BONUS_SECOND_WIND, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_yaleni_dyoken_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_yaleni_dyoken_2", CLASS_RANGED),
		
		## Jelkalen Balister (Unique)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_jelkalen_balister"), # combat_scripts.py
		(troop_set_slot, "trp_jelkalen_balister", slot_troop_unique_location, "p_town_5"),
		(call_script, "script_ce_assign_troop_requirement", "trp_jelkalen_balister", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_jelkalen_balister", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		# (troop_set_slot, "trp_jelkalen_balister", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_jelkalen_balister", CLASS_RANGED),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_jelkalen_balister_1"), # combat_scripts.py
		(troop_set_slot, "trp_jelkalen_balister_1", slot_troop_unique_location, "p_town_5"),
		(call_script, "script_ce_assign_troop_requirement", "trp_jelkalen_balister_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_jelkalen_balister_1", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister_1", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister_1", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_jelkalen_balister_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_jelkalen_balister_1", CLASS_RANGED),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_jelkalen_balister_2"), # combat_scripts.py
		(troop_set_slot, "trp_jelkalen_balister_2", slot_troop_unique_location, "p_town_5"),
		(call_script, "script_ce_assign_troop_requirement", "trp_jelkalen_balister_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_jelkalen_balister_2", PREREQ_ALLY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister_2", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister_2", BONUS_ENDURANCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_jelkalen_balister_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_jelkalen_balister_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_jelkalen_balister_2", CLASS_RANGED),
		
		## Rhodok Ranger (Affiliated)
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_ranger"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_ranger", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger", BONUS_HUNTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_ranger", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_rhodok_ranger", CLASS_CAVALRY),
		# +1 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_ranger_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_ranger_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger_1", BONUS_HUNTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger_1", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_ranger_1", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_rhodok_ranger_1", CLASS_CAVALRY),
		# +2 tier
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_rhodok_ranger_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_rhodok_ranger_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger_2", BONUS_HUNTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_rhodok_ranger_2", BONUS_STEALTHY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_rhodok_ranger_2", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_rhodok_ranger_2", CLASS_CAVALRY),
		
		
		######################################################
		#####              SARRANID FACTION              #####
		######################################################
		

		
		## Sultan Foot Guards
		#(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_sultan_foot_guards"), # combat_scripts.py
		#(troop_set_slot, "trp_sultan_foot_guards", slot_troop_unique_location, "p_town_19"),
		#(call_script, "script_ce_assign_troop_requirement", "trp_sultan_foot_guards", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		#(call_script, "script_ce_assign_troop_requirement", "trp_sultan_foot_guards", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		#(call_script, "script_ce_assign_troop_ability", "trp_sultan_foot_guards", BONUS_FORTITUDE, BONUS_UNASSIGNED),
		#(call_script, "script_ce_assign_troop_ability", "trp_sultan_foot_guards", BONUS_HARDY, BONUS_UNASSIGNED),
		#(troop_set_class, "trp_sultan_foot_guards", CLASS_INFANTRY),

		
		## LEIFDIN - NEW TROOPS REVAMP
		
		#AFFILIATED
		#Sarranid Bashibozuk
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_bashibozuk"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_bashibozuk", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_bashibozuk", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_bashibozuk", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_sarranid_bashibozuk", CLASS_INFANTRY),
		#Sarranid Bashibozuk +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_bashibozuk_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_bashibozuk_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_bashibozuk_1", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk_1", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk_1", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk_1", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk_1", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_bashibozuk_1", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_sarranid_bashibozuk_1", CLASS_INFANTRY),
		#Sarranid Bashibozuk +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_bashibozuk_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_bashibozuk_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_bashibozuk_2", PREREQ_ELITE_MERCENARY, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk_2", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk_2", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk_2", BONUS_BERSERKER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_bashibozuk_2", BONUS_BLOODLUST, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_bashibozuk_2", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_sarranid_bashibozuk_2", CLASS_INFANTRY),
		
		#Sarranid Corbaci
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_corbaci"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_corbaci", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci", BONUS_RALLYING_FIGURE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_corbaci", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_corbaci", CLASS_RANGED),
		#Sarranid Corbaci +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_corbaci_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_corbaci_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci_1", BONUS_RALLYING_FIGURE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci_1", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci_1", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_corbaci_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_corbaci_1", CLASS_RANGED),
		#Sarranid Corbaci +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_corbaci_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_corbaci_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci_2", BONUS_RALLYING_FIGURE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci_2", BONUS_TACTICIAN, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_corbaci_2", BONUS_VOLLEY_COMMANDER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_corbaci_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_corbaci_2", CLASS_RANGED),
		
		#Sarranid Sipahi
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_sipahi"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_sipahi", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi", BONUS_CHARGING_STRIKE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_sipahi", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_sipahi", CLASS_CAVALRY),
		#Sarranid Sipahi +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_sipahi_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_sipahi_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi_1", BONUS_CHARGING_STRIKE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi_1", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi_1", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_sipahi_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_sipahi_1", CLASS_CAVALRY),
		#Sarranid Sipahi +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_sipahi_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_sipahi_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi_2", BONUS_CHARGING_STRIKE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi_2", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_sipahi_2", BONUS_BLADEMASTER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_sipahi_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_sipahi_2", CLASS_CAVALRY),
		
		#Sarranid Boluk-bashi
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_boluk_bashi"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_boluk_bashi", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_boluk_bashi", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_boluk_bashi", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_boluk_bashi", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_boluk_bashi", CLASS_CAVALRY),
		#Sarranid Boluk-bashi +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_boluk_bashi_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_boluk_bashi_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_boluk_bashi_1", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_boluk_bashi_1", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_boluk_bashi_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_boluk_bashi_1", CLASS_CAVALRY),
		#Sarranid Boluk-bashi +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_boluk_bashi_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_boluk_bashi_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_boluk_bashi_2", BONUS_COMMANDING_PRESENCE, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_boluk_bashi_2", BONUS_INSPIRING, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_boluk_bashi_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_boluk_bashi_2", CLASS_CAVALRY),
		
		#Sarranid Garip
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_garip"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_garip", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip", BONUS_POISONED_WEAPONS, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_garip", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_garip", CLASS_CAVALRY),
		#Sarranid Garip +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_garip_1"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_garip_1", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip_1", BONUS_POISONED_WEAPONS, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip_1", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_garip_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_garip_1", CLASS_CAVALRY),
		#Sarranid Garip +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sarranid_garip_2"), # combat_scripts.py
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sarranid_garip_2", PREREQ_AFFILIATED, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip_2", BONUS_POISONED_WEAPONS, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sarranid_garip_2", BONUS_MASTER_BOWMAN, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sarranid_garip_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sarranid_garip_2", CLASS_CAVALRY),
		
		# UNIQUE
		
		# Bariyye Raider
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_bariyye_raider"), # combat_scripts.py
		(troop_set_slot, "trp_r_bariyye_raider", slot_troop_unique_location, "p_town_22"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_bariyye_raider", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_bariyye_raider", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_bariyye_raider", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_bariyye_raider", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_bariyye_raider", CLASS_CAVALRY),
		# Bariyye Raider +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_bariyye_raider_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_bariyye_raider_1", slot_troop_unique_location, "p_town_22"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_bariyye_raider_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_bariyye_raider_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_bariyye_raider_1", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_bariyye_raider_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_bariyye_raider_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_bariyye_raider_1", CLASS_CAVALRY),
		# Bariyye Raider +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_bariyye_raider_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_bariyye_raider_2", slot_troop_unique_location, "p_town_22"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_bariyye_raider_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_bariyye_raider_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_bariyye_raider_2", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_bariyye_raider_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_bariyye_raider_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_bariyye_raider_2", CLASS_CAVALRY),
		
		# Shariz Siegemaster
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_shariz_siegemaster_xbow"), # combat_scripts.py
		(troop_set_slot, "trp_r_shariz_siegemaster_xbow", slot_troop_unique_location, "p_town_22"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_shariz_siegemaster_xbow", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_shariz_siegemaster_xbow", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_shariz_siegemaster_xbow", slot_troop_recruit_type, STRT_MERCENARY),
		(troop_set_class, "trp_r_shariz_siegemaster_xbow", CLASS_RANGED),
		# Shariz Siegemaster +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_shariz_siegemaster_xbow_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_shariz_siegemaster_xbow_1", slot_troop_unique_location, "p_town_22"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_shariz_siegemaster_xbow_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_shariz_siegemaster_xbow_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow_1", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow_1", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_shariz_siegemaster_xbow_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_shariz_siegemaster_xbow_1", CLASS_RANGED),
		# Shariz Siegemaster +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_shariz_siegemaster_xbow_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_shariz_siegemaster_xbow_2", slot_troop_unique_location, "p_town_22"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_shariz_siegemaster_xbow_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_shariz_siegemaster_xbow_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow_2", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow_2", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_shariz_siegemaster_xbow_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_shariz_siegemaster_xbow_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_shariz_siegemaster_xbow_2", CLASS_RANGED),
		
		
		## Durquba Javelineer
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_durquba_javelineer"), # combat_scripts.py
		(troop_set_slot, "trp_r_durquba_javelineer", slot_troop_unique_location, "p_town_20"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_durquba_javelineer", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_durquba_javelineer", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_durquba_javelineer", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_durquba_javelineer", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_durquba_javelineer", CLASS_RANGED),
		## Durquba Javelineer +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_durquba_javelineer_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_durquba_javelineer_1", slot_troop_unique_location, "p_town_20"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_durquba_javelineer_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_durquba_javelineer_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_durquba_javelineer_1", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_durquba_javelineer_1", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_durquba_javelineer_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_durquba_javelineer_1", CLASS_RANGED),
		## Durquba Javelineer +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_durquba_javelineer_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_durquba_javelineer_2", slot_troop_unique_location, "p_town_20"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_durquba_javelineer_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_durquba_javelineer_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_durquba_javelineer_2", BONUS_SCAVENGER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_durquba_javelineer_2", BONUS_TRAILBLAZER, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_durquba_javelineer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_durquba_javelineer_2", CLASS_RANGED),
		
		## Mamluke Mounted Archer
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_mamluke_mounted_archer"), # combat_scripts.py
		(troop_set_slot, "trp_r_mamluke_mounted_archer", slot_troop_unique_location, "p_castle_41"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_mamluke_mounted_archer", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_mamluke_mounted_archer", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_mamluke_mounted_archer", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_mamluke_mounted_archer", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_class, "trp_r_mamluke_mounted_archer", CLASS_CAVALRY),
		## Mamluke Mounted Archer +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_mamluke_mounted_archer_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_mamluke_mounted_archer_1", slot_troop_unique_location, "p_castle_41"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_mamluke_mounted_archer_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_mamluke_mounted_archer_1", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_mamluke_mounted_archer_1", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_mamluke_mounted_archer_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_mamluke_mounted_archer_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_mamluke_mounted_archer_1", CLASS_CAVALRY),
		## Mamluke Mounted Archer +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_mamluke_mounted_archer_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_mamluke_mounted_archer_2", slot_troop_unique_location, "p_castle_41"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_mamluke_mounted_archer_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_mamluke_mounted_archer_2", PREREQ_FRIEND, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_mamluke_mounted_archer_2", BONUS_SHARPSHOOTER, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_mamluke_mounted_archer_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_mamluke_mounted_archer_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_mamluke_mounted_archer_2", CLASS_CAVALRY),
		
		# Sarranid Sultan Guard
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sultan_guard"), # combat_scripts.py
		(troop_set_slot, "trp_r_sultan_guard", slot_troop_unique_location, "p_town_19"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sultan_guard", PREREQ_UNIQUE_LOCATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sultan_guard", PREREQ_LIEGE_RELATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sultan_guard", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sultan_guard", CLASS_INFANTRY),
		# Sarranid Sultan Guard +1
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sultan_guard_1"), # combat_scripts.py
		(troop_set_slot, "trp_r_sultan_guard_1", slot_troop_unique_location, "p_town_19"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sultan_guard_1", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sultan_guard_1", PREREQ_LIEGE_RELATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard_1", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard_1", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard_1", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sultan_guard_1", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sultan_guard_1", CLASS_INFANTRY),
		# Sarranid Sultan Guard +2
		(call_script, "script_ce_wipe_troop_prerequisies_and_abilities", "trp_r_sultan_guard_2"), # combat_scripts.py
		(troop_set_slot, "trp_r_sultan_guard_2", slot_troop_unique_location, "p_town_19"),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sultan_guard_2", PREREQ_UNIQUE_LOCATION_UPGRADE, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_requirement", "trp_r_sultan_guard_2", PREREQ_LIEGE_RELATION, PREREQ_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard_2", BONUS_CHEAP, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard_2", BONUS_DEVOTED, BONUS_UNASSIGNED),
		(call_script, "script_ce_assign_troop_ability", "trp_r_sultan_guard_2", BONUS_HARDY, BONUS_UNASSIGNED),
		(troop_set_slot, "trp_r_sultan_guard_2", slot_troop_recruit_type, STRT_NOBLEMAN),
		(troop_set_class, "trp_r_sultan_guard_2", CLASS_INFANTRY),
		
		
		
		######################################################
		#####               PLAYER FACTION               #####
		######################################################
		(troop_set_slot, "trp_player_tier_5_mounted", slot_troop_recruit_type, STRT_NOBLEMAN),
		
		
		######################################################
		#####             TOURNAMENT TROOPS              #####
		######################################################
		(try_for_range, ":troop_no", tpe_scaled_champions_begin, tpe_scaled_champions_end),
			(troop_set_slot, ":troop_no", slot_troop_ability_1, BONUS_UNASSIGNED),
			(troop_set_slot, ":troop_no", slot_troop_ability_2, BONUS_UNASSIGNED),
			(troop_set_slot, ":troop_no", slot_troop_ability_3, BONUS_UNASSIGNED),
			(call_script, "script_ce_assign_troop_ability", ":troop_no", BONUS_SECOND_WIND, BONUS_UNASSIGNED), # combat_scripts.py - prereq constants in combat_constants.py
			(call_script, "script_ce_assign_troop_ability", ":troop_no", BONUS_HARDY, BONUS_UNASSIGNED), # combat_scripts.py - prereq constants in combat_constants.py
			(call_script, "script_ce_assign_troop_ability", ":troop_no", BONUS_SHIELD_BASHER, BONUS_UNASSIGNED), # combat_scripts.py - prereq constants in combat_constants.py
		(try_end),
		(try_for_range, ":troop_no", tpe_scaled_veterans_begin, tpe_scaled_veterans_end),
			(troop_set_slot, ":troop_no", slot_troop_ability_1, BONUS_UNASSIGNED),
			(troop_set_slot, ":troop_no", slot_troop_ability_2, BONUS_UNASSIGNED),
			(troop_set_slot, ":troop_no", slot_troop_ability_3, BONUS_UNASSIGNED),
			(call_script, "script_ce_assign_troop_ability", ":troop_no", BONUS_ENDURANCE, BONUS_UNASSIGNED), # combat_scripts.py - prereq constants in combat_constants.py
			(call_script, "script_ce_assign_troop_ability", ":troop_no", BONUS_SHIELD_BASHER, BONUS_UNASSIGNED), # combat_scripts.py - prereq constants in combat_constants.py
			(call_script, "script_ce_assign_troop_ability", ":troop_no", BONUS_BERSERKER, BONUS_UNASSIGNED), # combat_scripts.py - prereq constants in combat_constants.py
		(try_end),
		
		######################################################
		#####    INITIALIZE TROOP SKILLS/ATTRIBUTES      #####
		######################################################
		(try_for_range, ":troop_no", 1, "trp_end_of_troops"),
			(neg|troop_is_hero, ":troop_no"),
			(call_script, "script_ce_set_minimum_skills_for_troop", ":troop_no"),
		(try_end),
		
		# # Setup defaults for Rhodok Troops (new)
		# (try_for_range, ":troop_no", rhodok_troops_begin, "trp_rhodok_end_troop"),
			# (neg|troop_is_hero, ":troop_no"),
			# (call_script, "script_ce_set_minimum_skills_for_troop", ":troop_no"),
		# (try_end),
		
		# # Setup defaults for Swadian Troops (new)
		# (try_for_range, ":troop_no", swadia_troops_begin, "trp_swadia_end_troop"),
			# (neg|troop_is_hero, ":troop_no"),
			# (call_script, "script_ce_set_minimum_skills_for_troop", ":troop_no"),
		# (try_end),
		
		
 	]),  
	
# script_hub_create_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate this code for each window.
("hub_create_mode_switching_buttons",
    [
		### COMMON ELEMENTS ###
		(assign, "$gpu_storage", HUB_OBJECTS),
		(assign, "$gpu_data",    HUB_OBJECTS),
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		# Setup an initial false value for objects so if they don't get loaded they aren't 0's.
		(try_for_range, ":slot_no", hub_obj_button_general_info, 50),
			(store_add, ":value", ":slot_no", 1234),
			(troop_set_slot, HUB_OBJECTS, ":slot_no", ":value"),
		(try_end),
		
		# Check for town conditions
		(try_begin),
			(party_slot_eq, "$current_town", slot_party_type, spt_village),
			(neg|party_slot_eq, "$current_town", slot_village_state, svs_looted),
			(neg|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
			(neg|party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),
			(assign, ":village_is_normal", 1),
		(else_try),
			(assign, ":village_is_normal", 0),
		(try_end),
		
		# Text Labels
		(try_begin),
			(is_between, "$current_town", towns_begin, towns_end),
			(str_store_party_name, s22, "$current_town"),
			(str_store_string, s21, "@Town of {s22}"),
		(else_try),
			(is_between, "$current_town", castles_begin, castles_end),
			(str_store_party_name, s22, "$current_town"),
			(str_store_string, s21, "@{s22}"),
		(else_try),
			(is_between, "$current_town", villages_begin, villages_end),
			(str_store_party_name, s22, "$current_town"),
			(str_store_string, s21, "@Village of {s22}"),
		(try_end),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, hub_obj_label_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", hub_obj_label_main_title, 150),
		
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, hub_obj_label_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", hub_obj_label_main_title2, 150),
		
		## CONTAINERS ##
		(call_script, "script_gpu_container_heading", 50, 80, 175, 505, hub_obj_container_1),
			
			
			## BUTTONS ##
			(assign, ":x_buttons", 0), # 90 
			(assign, ":y_button_step", 55),
			(assign, ":pos_y", 420),
			(call_script, "script_gpu_create_button", "str_hub_general_info", ":x_buttons", ":pos_y", hub_obj_button_general_info), ### GENERAL INFORMATION ###
			(try_begin),
				### PLAYER ONLY SEES THESE PRESENTATIONS IF HE OWNS THE CENTER ###
				(this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_town),
				(this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
				(eq, ":village_is_normal", 1),
				(this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
				(ge, DEBUG_HUB, 1),
				(val_sub, ":pos_y", ":y_button_step"),
				(call_script, "script_gpu_create_button", "str_hub_finances", ":x_buttons", ":pos_y", hub_obj_button_finances), ### FINANCES ###
				(val_sub, ":pos_y", ":y_button_step"),
				(call_script, "script_gpu_create_button", "str_hub_improvements", ":x_buttons", ":pos_y", hub_obj_button_improvements), ### IMPROVEMENTS ###
			(try_end),
			(try_begin),
				### THESE PRESENTATIONS ARE ALWAYS AVAILABLE ###
				(this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_town),
				(this_or_next|party_slot_eq, "$current_town", slot_party_type, spt_castle),
				(eq, ":village_is_normal", 1),
				(val_sub, ":pos_y", ":y_button_step"),
				(call_script, "script_gpu_create_button", "str_hub_recruitment", ":x_buttons", ":pos_y", hub_obj_button_recruitment), ### RECRUITMENT ###
			(try_end),
			(try_begin),
				### PLAYER ONLY SEES THESE PRESENTATIONS IF HE OWNS THE CENTER ###
				(this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
				(ge, DEBUG_HUB, 1),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				# (val_sub, ":pos_y", ":y_button_step"),
				# (call_script, "script_gpu_create_button", "str_hub_advisors", ":x_buttons", ":pos_y", hub_obj_button_advisors), ### ADVISORS ###
				(val_sub, ":pos_y", ":y_button_step"),
				(call_script, "script_gpu_create_button", "str_hub_garrison", ":x_buttons", ":pos_y", hub_obj_button_garrison), ### GARRISON ###			
			(else_try),
				### THESE PRESENTATIONS ARE ALWAYS AVAILABLE ###
				(is_between, "$current_town", villages_begin, villages_end),
				(eq, ":village_is_normal", 1),
				(val_sub, ":pos_y", ":y_button_step"),
				(call_script, "script_gpu_create_button", "str_hub_quests", ":x_buttons", ":pos_y", hub_obj_button_quests), ### QUESTS ###
			(try_end),
			(try_begin),
				### PLAYER ONLY SEES THESE PRESENTATIONS IF IT IS A WALLED CENTER ###
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(val_sub, ":pos_y", ":y_button_step"),
				(str_store_string, s21, "@Commissions"),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", hub_obj_button_commissions), ### COMMISSIONS ###
			(try_end),
			## AFFAIRS OF THE REALM - Only seen if of this faction and capital town or owned town.
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(store_faction_of_party, ":center_faction", "$current_town"),
				(eq, ":center_faction", "$players_kingdom"),
				(val_sub, ":pos_y", ":y_button_step"),
				(str_store_string, s21, "@Realm Affairs"),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", hub_obj_button_realm_affairs), ### REALM AFFAIRS ###
			(try_end),
			
		(set_container_overlay, -1),
		(call_script, "script_gpu_create_mesh", "mesh_button_up", 55, 35, 350, 500),
		(call_script, "script_gpu_create_button", "str_hub_done", 65, 40, hub_obj_button_done),
		## PLAYER GOLD ##
		(store_troop_gold, reg21, "trp_player"),
		(call_script, "script_gpu_create_text_label", "str_hub_player_gold", 925, 38, hub_obj_label_player_gold, gpu_right),
		(call_script, "script_gpu_resize_object", hub_obj_label_player_gold, 75),
		(call_script, "script_gpu_create_mesh", "mesh_hub_golden_coins", 935, 25, 250, 250),
		## TREASURY ##
		(try_begin),
			(is_between, "$current_town", walled_centers_begin, walled_centers_end),
			(this_or_next|party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
			(ge, DEBUG_HUB, 1),
			(party_get_slot, reg21, "$current_town", slot_center_treasury),
			(call_script, "script_gpu_create_text_label", "str_hub_treasury_gold", 925, 61, hub_obj_label_treasury_gold, gpu_right),
			(call_script, "script_gpu_resize_object", hub_obj_label_treasury_gold, 75),
			(call_script, "script_gpu_create_mesh", "mesh_hub_golden_coins", 935, 48, 250, 250),
		(try_end),
		## EMBLEMS ##
		# (try_begin),
			# (call_script, "script_emblem_get_current_quantity"), # emblem_scripts.py
			# (ge, reg1, 1),
			# (str_store_string, s21, "@Emblems: {reg1}"),
			# (call_script, "script_gpu_create_text_label", "str_hub_s21", 925, 61, hub_obj_label_player_emblems, gpu_right),
			# (call_script, "script_gpu_resize_object", hub_obj_label_player_emblems, 75),
			# # (call_script, "script_gpu_create_mesh", "mesh_hub_golden_coins", 935, 48, 250, 250),
			# (create_mesh_overlay_with_item_id, reg1, SILVERSTAG_EMBLEM),
			# (position_set_x, pos1, 250),
			# (position_set_y, pos1, 250),
			# (overlay_set_size, reg1, pos1),
			# (position_set_x, pos1, 945),
			# (position_set_y, pos1, 66),
			# (overlay_set_position, reg1, pos1),
		# (try_end),
		
	]),
	
# script_hub_handle_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate the code to handle their functionality for each window.
("hub_handle_mode_switching_buttons",
    [
		(store_script_param, ":object", 1),
		(store_script_param, ":value", 2),
		(assign, reg1, ":value"), # So it won't be whined about.
		
		# hub_obj_button_general_info            = 3
		# hub_obj_button_finances                = 4
		# hub_obj_button_improvements            = 5
		# hub_obj_button_recruitment             = 6
		# hub_obj_button_advisors                = 7
		# hub_obj_button_garrison                = 8
		# hub_obj_button_quests                  = 9
		# hub_obj_button_commissions             = 29
		
		### COMMON ELEMENTS ###
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_done, ":object"),
			(presentation_set_duration, 0),
			(try_begin),
				(is_between, "$current_town", walled_centers_begin, walled_centers_end),
				(jump_to_menu, "mnu_town"),
			(else_try),
				(is_between, "$current_town", villages_begin, villages_end),
				(jump_to_menu, "mnu_village"),
			(try_end),
			
		(else_try), ####### BUTTON : GENERAL INFORMATION #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_general_info, ":object"),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : FINANCES #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_finances, ":object"),
			(assign, "$hub_mode", HUB_MODE_FINANCES),
			(assign, "$g_apply_budget_report_to_gold", 0),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : IMPROVEMENTS #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_improvements, ":object"),
			(assign, "$hub_mode", HUB_MODE_IMPROVEMENTS),
			(troop_set_slot, HUB_OBJECTS, hub3_val_slider_improvement_selector, center_improvements_begin),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : RECRUITMENT #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_recruitment, ":object"),
			(assign, "$hub_mode", HUB_MODE_RECRUITMENT),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : ADVISORS #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_advisors, ":object"),
			(assign, "$hub_mode", HUB_MODE_ADVISORS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : GARRISON #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_garrison, ":object"),
			(assign, "$hub_mode", HUB_MODE_GARRISON),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : QUESTS #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_quests, ":object"),
			(assign, "$hub_mode", HUB_MODE_QUESTS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : COMMISSIONS #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_commissions, ":object"),
			(assign, "$hub_mode", HUB_MODE_COMMISSIONS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : AFFAIRS OF THE REALM #######
			(troop_slot_eq, HUB_OBJECTS, hub_obj_button_realm_affairs, ":object"),
			(assign, "$hub_mode", HUB_MODE_REALM_AFFAIRS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(try_end),
	]),
	
# script_hub_get_troop_recruit_type_for_buyer
# PURPOSE: Return the type of recruit pool slot a troop uses.
# EXAMPLE: (call_script, "script_hub_get_troop_recruit_type_for_buyer", ":troop_no", ":buyer"), # Returns type slot to reg1
("hub_get_troop_recruit_type_for_buyer",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":buyer", 2),
		
		(try_begin),
			## PLAYER - VETERAN TROOP
			(eq, ":buyer", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_NOBLEMAN),
			(assign, ":recruiting_pool", slot_center_veteran_pool),
			(str_store_string, s1, "@Veteran"),
		(else_try),
			## AI - VETERAN TROOP
			(neq, ":buyer", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_NOBLEMAN),
			(assign, ":recruiting_pool", slot_center_veteran_ai),
			(str_store_string, s1, "@Veteran (AI)"),
		(else_try),
			## PLAYER - MERCENARY TROOP
			(eq, ":buyer", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_MERCENARY),
			(assign, ":recruiting_pool", slot_center_mercenary_pool_player),
			(str_store_string, s1, "@Mercenary"),
		(else_try),
			## AI - MERCENARY TROOP
			(neq, ":buyer", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_MERCENARY),
			(assign, ":recruiting_pool", slot_center_mercenary_pool_npc),
			(str_store_string, s1, "@Mercenary (AI)"),
		(else_try),
			## PLAYER - PEASANT TROOP
			(eq, ":buyer", "trp_player"),
			(assign, ":recruiting_pool", slot_center_volunteer_troop_amount),
			(str_store_string, s1, "@Peasant"),
		(else_try),
			## AI - PEASANT TROOP
			(neq, ":buyer", "trp_player"),
			(assign, ":recruiting_pool", slot_center_npc_volunteer_troop_amount),
			(str_store_string, s1, "@Peasant (AI)"),
		(else_try),
			## ERROR
			(try_begin),
				(eq, ":buyer", "trp_player"),
				(str_store_string, s32, "@Player"),
			(else_try),
				(str_store_troop_name, s32, ":buyer"),
			(try_end),
			(assign, reg31, ":troop_no"),
			(str_store_troop_name, s31, ":troop_no"),
			(display_message, "@ERROR - Failed to retrieve troop type for {s31} (#{reg31}).  Buyer = {s32}"),
		(try_end),
		
		(assign, reg1, ":recruiting_pool"),
	]),
	
# script_hub_get_center_income
# PURPOSE: Return the amount of rent a fief should produce.
("hub_get_center_income",
    [
		(store_script_param, ":center_no", 1),
		
		(store_faction_of_party, ":faction_no", ":center_no"),
		(party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
        (call_script, "script_improvement_weekly_income", ":center_no"), # improvement_scripts.py
		(val_add, ":accumulated_rents", reg1), # Applies all flat income/upkeep modifiers for center improvements.
		(store_faction_of_party, ":faction_no", ":center_no"),
		(faction_get_slot, ":income_percent", ":faction_no", slot_faction_center_income),
		(val_add, ":income_percent", reg2), # Applies all percentage income/upkeep modifiers for center improvements.
		(store_mul, ":income_bonus", ":accumulated_rents", ":income_percent"),
		(val_div, ":income_bonus", 100),
		(val_add, ":accumulated_rents", ":income_bonus"),
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_village),
			(faction_slot_eq, ":faction_no", slot_faction_decree_reconstruction, 1), # "PERIOD OF RECONSTRUCTION" decree active.
			(assign, ":accumulated_rents", 0), # While in reconstruction all income is channeled into rebuilding.
		(try_end),

		(assign, reg1, ":accumulated_rents"),
	]),
	
# script_hub_get_center_tariffs
# PURPOSE: Return the amount of tariffs a fief has earned.
("hub_get_center_tariffs",
    [
		(store_script_param, ":center_no", 1),
		
		(store_faction_of_party, ":faction_no", ":center_no"),
		(call_script, "script_improvement_weekly_income", ":center_no"), # improvement_scripts.py
		(party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
		(val_add, ":accumulated_tariffs", reg3), # Applies all flat tariff modifiers for center improvements.
		(faction_get_slot, ":income_percent", ":faction_no", slot_faction_center_tariffs),
		(val_add, ":income_percent", reg4), # Applies all percentage tariff modifiers for center improvements.
		## TROOP EFFECT: BONUS_ADMINISTRATOR in Castle Steward position improves center trade income by 1% per point of Trade.
		(try_begin),
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(is_between, ":castle_steward", companions_begin, companions_end),
			(call_script, "script_cf_ce_troop_has_ability", ":castle_steward", BONUS_ADMINISTRATOR), # combat_scripts.py - ability constants in combat_constants.py
			(store_skill_level, ":trade_bonus", "skl_trade", ":castle_steward"),
			(val_add, ":income_percent", ":trade_bonus"),
		(try_end),
		(val_sub, ":income_percent", 20), # Apply 20% reduction in tariffs to everything.  Balance change in v0.23.
		(store_mul, ":income_bonus", ":accumulated_tariffs", ":income_percent"),
		(val_div, ":income_bonus", 100),
		(val_add, ":accumulated_tariffs", ":income_bonus"),
		
		(assign, reg1, ":accumulated_tariffs"),
	]),
	
# script_hub_get_party_wages
# PURPOSE: Return the amount of tariffs a fief has earned.
("hub_get_party_wages",
    [
		(store_script_param, ":party_no", 1),
		(store_script_param, ":garrison_troop", 2),
		
		(assign, ":total_wage", 0),
		(party_get_num_companion_stacks, ":num_stacks", ":party_no"),
		(try_for_range, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
			(party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
			(call_script, "script_game_get_troop_wage", ":stack_troop", ":party_no"),
			(assign, ":cur_wage", reg0),
			(val_mul, ":cur_wage", ":stack_size"),
			(try_begin),
				## TROOP EFFECT: BONUS_DEVOTED
				(call_script, "script_cf_ce_troop_has_ability", ":stack_troop", BONUS_DEVOTED), # combat_scripts.py - ability constants in combat_constants.py
				(val_div, ":cur_wage", 2),
			(try_end),
			(val_add, ":total_wage", ":cur_wage"),
		(try_end),
		(try_begin),
			(eq, ":garrison_troop", 1),
			(val_div, ":total_wage", 2), #Half payment for garrisons
			
			## TROOP EFFECT: BONUS_EFFICIENT in Castle Steward position reduces wages of garrisoned troops by 1% per point of intelligence.
			(try_begin),
				(party_get_slot, ":castle_steward", ":party_no", slot_center_steward),
				(is_between, ":castle_steward", companions_begin, companions_end),
				(call_script, "script_cf_ce_troop_has_ability", ":castle_steward", BONUS_EFFICIENT), # combat_scripts.py - ability constants in combat_constants.py
				(store_attribute_level, ":INT", ":castle_steward", ca_intelligence),
				(store_div, ":half_bonus", ":INT", 2),
				(val_add, ":INT", ":half_bonus"),
				(store_mul, ":garrison_discount", ":total_wage", ":INT"),
				(val_div, ":garrison_discount", 100),
				(val_sub, ":total_wage", ":garrison_discount"),
			(try_end),
		(else_try),
			(eq, ":party_no", "p_main_party"),
			(store_sub, ":total_payment_ratio", 14, "$g_cur_week_half_daily_wage_payments"), #between 0 and 7
			(val_mul, ":total_wage", ":total_payment_ratio"),
			(val_div, ":total_wage", 14),
		(try_end),
		(val_mul, ":total_wage", -1),
		
		(assign, reg1, ":total_wage"),
	]),
		
# script_hub_get_mercenary_wages
# PURPOSE: Return the amount of rent a fief should produce.
("hub_get_mercenary_wages",
    [
		(store_script_param, ":garrison_troop", 1),
		
		(assign, ":party_no", "p_main_party"),
		(assign, ":total_wage", 0),
		(assign, ":combined_hero_level", 0),
		(party_get_num_companion_stacks, ":num_stacks", ":party_no"),
		(try_for_range, ":i_stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
			(party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
			(call_script, "script_game_get_troop_wage", ":stack_troop", ":party_no"),
			(assign, ":cur_wage", reg0),
			(val_mul, ":cur_wage", ":stack_size"),
			(val_add, ":total_wage", ":cur_wage"),
			(troop_is_hero, ":stack_troop"),
			(store_character_level, ":level", ":stack_troop"),
			(val_sub, ":level", 4), # They won't pay extra for peons.
			(ge, ":level", 1),
			(val_add, ":combined_hero_level", ":level"),
		(try_end),
		# Provide mercenary payment for player & companions.
		(try_begin),
			(ge, ":combined_hero_level", 1),
			(store_mul, ":hero_wage", ":combined_hero_level", 15),
			(val_add, ":total_wage", ":hero_wage"),
		(try_end),
		(try_begin),
			(eq, ":garrison_troop", 1),
			(val_div, ":total_wage", 2), #Half payment for garrisons
		(else_try),
			(eq, ":party_no", "p_main_party"),
			(store_sub, ":total_payment_ratio", 14, "$g_cur_week_half_daily_wage_payments"), #between 0 and 7
			(val_mul, ":total_wage", ":total_payment_ratio"),
			(val_div, ":total_wage", 14),
		(try_end),
		# Calculate a -25% contract penalty to keep things more balanced.
		(store_mul, ":base_contract_penalty", ":total_wage", 25),
		(val_div, ":base_contract_penalty", 100),
		# Improve your bonus based upon your persuasion skill for haggling a better deal.  (Persuasion * 3)%
		(store_skill_level, ":persuasiveness", skl_persuasion, "trp_player"),
		(val_mul, ":persuasiveness", 3),
		(val_min, ":persuasiveness", 30),
		(store_add, ":leader_cut", 0, ":persuasiveness"),
		# Improve your bonus based upon renown / 20 with a cap of +40%.
		(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
		(store_div, ":renown_bonus", ":renown", 20),
		(val_min, ":renown_bonus", 40),
		(val_add, ":leader_cut", ":renown_bonus"),
		(val_max, ":leader_cut", 1),
		# Update pay and report it to the presentation.
		(store_div, ":extra_pay", ":total_wage", ":leader_cut"),
		(val_add, ":total_wage", ":extra_pay"),
		(val_sub, ":total_wage", ":base_contract_penalty"),
		(assign, reg1, ":total_wage"),
	]),
	
# script_cf_hub_get_center_enterprise
# PURPOSE: Return the amount of money an enterprise has earned.
("cf_hub_get_center_enterprise",
    [
		(store_script_param, ":center_no", 1),
		
		(party_get_slot, ":enterprise_output", ":center_no", slot_center_player_enterprise),
		(gt, ":enterprise_output", 1),
		(neg|party_slot_ge, ":center_no", slot_center_player_enterprise_days_until_complete, 1),

		(str_store_party_name, s0, ":center_no"),

		(call_script, "script_process_player_enterprise", ":enterprise_output", ":center_no"),
		(assign, ":net_profit", reg0),
		(assign, ":price_of_single_output", reg4),
		(assign, ":price_of_single_input", reg5),
		(assign, ":price_of_secondary_input", reg10),

		(store_sub, ":town_order", ":center_no", towns_begin),
		(store_add, ":craftsman_troop", ":town_order", "trp_town_1_master_craftsman"),

		(item_get_slot, ":outputs_added_to_market", ":enterprise_output", slot_item_output_per_run),
		(assign, ":outputs_added_to_warehouse", 0),

		#Enterprise impact of outputs
		(try_begin),
			#output placed in inventory: deduct selling price and add one good
			(party_slot_eq, ":center_no", slot_center_player_enterprise_production_order, 1),

			#Count empty slots
			(assign, ":empty_slots", 0),
			(troop_get_inventory_capacity, ":total_capacity", ":craftsman_troop"),
			(try_for_range, ":capacity_iterator", 0, ":total_capacity"),
				(troop_get_inventory_slot, ":slot", ":craftsman_troop", ":capacity_iterator"),
				(lt, ":slot", 1),
				(val_add, ":empty_slots", 1),
			(try_end),

			(assign, ":outputs_added_to_warehouse", ":outputs_added_to_market"),
			(val_min, ":outputs_added_to_warehouse",  ":empty_slots"),
			(gt, ":outputs_added_to_warehouse", 0),

			(store_mul, ":cancelled_sales", ":price_of_single_output", ":outputs_added_to_warehouse"),
			(val_sub, ":net_profit", ":cancelled_sales"),
			(val_sub, ":outputs_added_to_market", ":outputs_added_to_warehouse"),
		(try_end),
		  
		#If the transaction is for real, and not just a budget check
		(try_begin),
			(eq, "$g_apply_budget_report_to_gold", 1),
			(troop_add_items, ":craftsman_troop", ":enterprise_output", ":outputs_added_to_warehouse"),

			#Affect prices by outputs added to market
			(store_sub, ":item_slot_no", ":enterprise_output", trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(party_get_slot, ":current_index", ":center_no", ":item_slot_no"),			
			(store_mul, ":impact_on_price", ":outputs_added_to_market", 15),
			(val_sub, ":current_index", ":impact_on_price"),
			(party_set_slot, ":center_no", ":item_slot_no",":current_index"),			
					
			(gt, "$cheat_mode", 0),
			(str_store_troop_name, s3, ":craftsman_troop"),
			(assign, reg3, ":outputs_added_to_warehouse"),
			(display_message, "@{!}DEBUG -- Adding {reg3} items to {s3}"),
		(try_end),
		  
		#Enterprise impact of outputs
		(item_get_slot, ":inputs_taken_from_market", ":enterprise_output", slot_item_input_number),		  
		(try_begin),
			(item_slot_ge, ":enterprise_output", slot_item_secondary_raw_material, 1),
			(assign, ":2ary_inputs_taken_from_market", ":inputs_taken_from_market"),
		(else_try),
			(assign, ":2ary_inputs_taken_from_market", 0),
		(try_end),

		(assign, ":inputs_taken_from_warehouse", 0),
		(assign, ":2ary_inputs_taken_from_warehouse", 0),
		  
		(try_begin),
		    #input present in inventory: reimburse for input cost and remove one good
			(troop_get_inventory_capacity, ":total_capacity", ":craftsman_troop"),
			(try_for_range, ":capacity_iterator", 0, ":total_capacity"),
				(troop_get_inventory_slot, ":item_in_slot", ":craftsman_troop", ":capacity_iterator"),
			
				(lt, ":inputs_taken_from_warehouse", ":inputs_taken_from_market"),
				(item_slot_eq, ":enterprise_output", slot_item_primary_raw_material, ":item_in_slot"),
                #(troop_inventory_slot_get_item_amount, ":item_ammo", ":craftsman_troop", ":capacity_iterator"),
                #(troop_inventory_slot_get_item_max_amount, ":item_max_ammo", ":craftsman_troop", ":capacity_iterator"),
                #(eq, ":item_ammo", ":item_max_ammo"),
				
				(val_add, ":inputs_taken_from_warehouse", 1),
			(else_try),	
				(lt, ":2ary_inputs_taken_from_warehouse", ":2ary_inputs_taken_from_market"),
				(item_slot_eq, ":enterprise_output", slot_item_secondary_raw_material, ":item_in_slot"),
                #(troop_inventory_slot_get_item_amount, ":item_ammo", ":craftsman_troop", ":capacity_iterator"),
                #(troop_inventory_slot_get_item_max_amount, ":item_max_ammo", ":craftsman_troop", ":capacity_iterator"),
                #(eq, ":item_ammo", ":item_max_ammo"),

				(val_add, ":2ary_inputs_taken_from_warehouse", 1),
			(try_end),
		  
			(try_begin),
				(gt, ":inputs_taken_from_warehouse", 0),
				(val_sub, ":inputs_taken_from_market", ":inputs_taken_from_warehouse"),
				(store_mul, ":savings_from_warehoused_inputs",	":price_of_single_input", ":inputs_taken_from_warehouse"),
				(val_add, ":net_profit", ":savings_from_warehoused_inputs"),
			(try_end),	
			(try_begin),
				(gt, ":2ary_inputs_taken_from_warehouse", 0),
				(val_sub, ":2ary_inputs_taken_from_market", ":2ary_inputs_taken_from_warehouse"),
				(assign, ":savings_from_warehoused_inputs",	":price_of_secondary_input"),
				(val_add, ":net_profit", ":savings_from_warehoused_inputs"),
			(try_end),					
		(try_end),
		  
		  #If the transaction is for real, and not just a budget check
		(try_begin),
			(eq, "$g_apply_budget_report_to_gold", 1),
			(item_get_slot, ":raw_material", ":enterprise_output", slot_item_primary_raw_material),
			(troop_remove_items, ":craftsman_troop", ":raw_material", ":inputs_taken_from_warehouse"),
			(item_get_slot, ":secondary_raw_material", ":enterprise_output", slot_item_secondary_raw_material),
			(troop_remove_items, ":craftsman_troop", ":secondary_raw_material", ":2ary_inputs_taken_from_warehouse"),

			#Affect prices by intputs added to market
			(store_sub, ":item_slot_no", ":raw_material", trade_goods_begin),
			(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
			(party_get_slot, ":current_index", ":center_no", ":item_slot_no"),			
			(store_mul, ":impact_on_price", ":outputs_added_to_market", 15),
			(val_add, ":current_index", ":impact_on_price"),
			(party_set_slot, ":center_no", ":item_slot_no",":current_index"),			

			(try_begin),
				(gt, ":2ary_inputs_taken_from_market", 0),
				(store_sub, ":item_slot_no", ":secondary_raw_material", trade_goods_begin),
				(val_add, ":item_slot_no", slot_town_trade_good_prices_begin),
				(party_get_slot, ":current_index", ":center_no", ":item_slot_no"),			
				(val_add, ":current_index", 15),
				(party_set_slot, ":center_no", ":item_slot_no",":current_index"),			
			(try_end),
		(try_end),
		
		(assign, reg1, ":net_profit"),
	]),
	
# script_hub_get_fund_string
# PURPOSE: Return the amount of rent a fief should produce.
("hub_get_fund_string",
    [
		(store_script_param, ":value", 1),
		(store_script_param, ":type", 2),
		(store_script_param, ":force_sign", 3),
		
		(assign, ":color_income", 14336),     # Dark Green
		(assign, ":color_expense", 4980736),  # Dark Red
		(assign, ":color_neutral", 0),        # Black
		(assign, reg51, ":color_neutral"),
		
		(assign, reg21, ":value"),
		(try_begin),
			(eq, ":type", 0), # One time change.
			(str_store_string, s21, "@{reg21}"),
			(str_store_string, s22, "@denars"),
		(else_try),
			(eq, ":type", 1), # Weekly change.
			(str_store_string, s21, "@{reg21}"),
			(str_store_string, s22, "@denars per week"),
		(else_try),
			(eq, ":type", 2), # Percentage change.
			(str_store_string, s21, "@{reg21}"),
			(str_store_string, s22, "@percent"),
			(try_begin),
				(ge, ":value", 0),
				(eq, ":force_sign", 0),
				(str_store_string, s21, "@+{s21}"),
			(else_try),
				(ge, ":value", 0),
				(eq, ":force_sign", 1),
				(str_store_string, s21, "@-{s21}"),
			(try_end),
		(else_try),
			(eq, ":type", 3), # Money spent directly from treasury
			(str_store_string, s21, "@{reg21}"),
			(str_store_string, s22, "@denars per week (from treasury)"),
		(try_end),
		
		(try_begin),
			(eq, ":value", 0),
			(str_store_string, s21, "@None"),
			(str_clear, s22),
			(assign, reg51, ":color_neutral"),
		(else_try),
			(lt, ":value", 0),
			(assign, reg51, ":color_expense"),
		(else_try),
			(ge, ":value", 1),
			(assign, reg51, ":color_income"),
		(try_end),
		
		(try_begin),
			(eq, ":force_sign", 1), # This means flip the current sign.
			(try_begin),
				(ge, ":value", 0),
				(assign, reg51, ":color_expense"),
			(else_try),
				(lt, ":value", 0),
				(assign, reg51, ":color_income"),
			(try_end),
		(try_end),
		#(assign, reg51, gpu_black),
	]),
	
# script_hub_display_improvements
# PURPOSE: Display a list of improvements for a given center based on the desired output (income, tariffs, all)
# EXAMPLE: (call_script, "script_hub_display_improvements", ":center_no", ":display_mode", ":pos_x_col_1", ":pos_y", ":pos_x_col_2"),
("hub_display_improvements",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":display_mode", 2),
		(store_script_param, ":pos_x_col_1", 3),
		(store_script_param, ":pos_x_col_2", 4),
		(store_script_param, ":pos_x_col_3", 5),
		
		(assign, ":pos_y", reg1),
		(assign, ":line_step", 25),
		(assign, ":line_count", 0),
		
		## IMPROVEMENTS ##
		(try_for_range, ":improvement", native_improvements_begin, center_improvements_end),
			(this_or_next|is_between, ":improvement", native_improvements_begin, native_improvements_end),
			(is_between, ":improvement", center_improvements_begin, center_improvements_end),
			(party_slot_ge, ":center_no", ":improvement", cis_built),
			
			## Get upkeep information.
			(call_script, "script_improvement_get_upkeep", ":center_no", ":improvement"),
			(assign, ":income_flat",     reg1),
			(assign, ":income_percent",  reg2),
			(assign, ":tariffs_flat",    reg3),
			(assign, ":tariffs_percent", reg4),
			
			## Get info about the improvement.
			(call_script, "script_get_improvement_details", ":improvement"),
			(str_store_string, s41, s0), # Stored in s41 so it isn't overwritten.
			
			## Display improvement.
			(try_begin),
				(neq, ":income_flat", 0),
				(this_or_next|eq, ":display_mode", 0), # Income
				(this_or_next|eq, ":display_mode", 2), # All
				(eq, ":display_mode", 3), # Line Count
				(val_add, ":line_count", 1),
				(neq, ":display_mode", 3), # Line count shouldn't continue on to display anything.
				(val_sub, ":pos_y", ":line_step"),
				(str_store_string, s21, s41),
				(call_script, "script_gpu_create_text_label", "str_hub_improvement", ":pos_x_col_1", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_hub_get_fund_string", ":income_flat", 1, 0),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, reg51),
				(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
			(try_end),
			(try_begin),
				(neq, ":income_percent", 0),
				(this_or_next|eq, ":display_mode", 0), # Income
				(this_or_next|eq, ":display_mode", 2), # All
				(eq, ":display_mode", 3), # Line Count
				(val_add, ":line_count", 1),
				(neq, ":display_mode", 3), # Line count shouldn't continue on to display anything.
				(val_sub, ":pos_y", ":line_step"),
				(str_store_string, s21, s41),
				(call_script, "script_gpu_create_text_label", "str_hub_improvement", ":pos_x_col_1", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_hub_get_fund_string", ":income_percent", 2, 0),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, reg51),
				(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
			(try_end),
			(try_begin),
				(neq, ":tariffs_flat", 0),
				(this_or_next|eq, ":display_mode", 1), # Tariffs
				(this_or_next|eq, ":display_mode", 2), # All
				(eq, ":display_mode", 3), # Line Count
				(val_add, ":line_count", 1),
				(neq, ":display_mode", 3), # Line count shouldn't continue on to display anything.
				(val_sub, ":pos_y", ":line_step"),
				(str_store_string, s21, s41),
				(call_script, "script_gpu_create_text_label", "str_hub_improvement", ":pos_x_col_1", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_hub_get_fund_string", ":tariffs_flat", 1, 0),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, reg51),
				(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
			(try_end),
			(try_begin),
				(neq, ":tariffs_percent", 0),
				(this_or_next|eq, ":display_mode", 1), # Tariffs
				(this_or_next|eq, ":display_mode", 2), # All
				(eq, ":display_mode", 3), # Line Count
				(val_add, ":line_count", 1),
				(neq, ":display_mode", 3), # Line count shouldn't continue on to display anything.
				(val_sub, ":pos_y", ":line_step"),
				(str_store_string, s21, s41),
				(call_script, "script_gpu_create_text_label", "str_hub_improvement", ":pos_x_col_1", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
				(call_script, "script_hub_get_fund_string", ":tariffs_percent", 2, 0),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_right),
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, reg51),
				(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_3", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_resize_object", 0, 75),
			(try_end),
		(try_end),
		
		(assign, reg1, ":pos_y"),
		(assign, reg2, ":line_count"),
	]),
	
	
# script_hub_troop_get_average_value_of_item_type
# PURPOSE: Given a troop and item type figure out the average autoloot score for every item of that type within the troop's inventory.
("hub_troop_get_average_value_of_item_type",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":item_type", 2),
		
		(assign, ":count", 0),
		(assign, ":rating", 0),
		(troop_get_inventory_capacity, ":inventory_cap", ":troop_no"),
		(try_for_range, ":inventory_slot", 0, ":inventory_cap"),
			(troop_get_inventory_slot, ":item_no", ":troop_no", ":inventory_slot"),
			(ge, ":item_no", 1),
			(item_get_type, ":type", ":item_no"),
			(eq, ":type", ":item_type"),
			# (troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":inventory_slot"),
			(val_add, ":count", 1),
			# (call_script, "script_als_get_item_rating", ":troop_no", ":item_no", ":imod"), # cms_scripts.py
			(item_get_slot, reg1, ":item_no", slot_item_rated_weight), # 0 - 100% rating.
			(val_add, ":rating", reg1),
		(try_end),
		
		(try_begin),
			(ge, ":count", 2),
			(store_div, reg1, ":rating", ":count"),
		(else_try),
			(assign, reg1, ":rating"),
		(try_end),
		
	]),
	
# script_hub_define_item_type_best_and_worst
# PURPOSE: Given a troop and item type figure out the average autoloot score for every item of that type within the troop's inventory.
("hub_define_item_type_best_and_worst",
    [
		(store_script_param, ":desired_type", 1),
		
		(assign, ":highest_rating", 0),
		(assign, ":lowest_rating", 10000),
		
		(try_for_range, ":item_no", "itm_sumpter_horse", "itm_items_end"),
			(item_get_type, ":item_type", ":item_no"),
			(eq, ":item_type", ":desired_type"),
			(neg|item_has_property, ":item_no", itp_unique), # Block uniques from being rated.
			(call_script, "script_als_get_item_rating", "trp_autoloot_reference", ":item_no", imod_plain), # cms_scripts.py
			(assign, ":rating", reg1),
			# Check if this item is the best or worst in its class.
			(try_begin),
				(ge, ":rating", ":highest_rating"),
				(assign, ":highest_rating", ":rating"),
				### DIAGNOSTIC ###
				# (assign, reg31, ":rating"),
				# (assign, reg32, ":item_type"),
				# (str_store_item_name, s31, ":item_no"),
				# (display_message, "@DEBUG: {s31} is the new BEST item in type [{reg32}] at {reg31} rating.", gpu_debug),
			(try_end),
			(try_begin),
				(lt, ":rating", ":lowest_rating"),
				(assign, ":lowest_rating", ":rating"),
				### DIAGNOSTIC ###
				# (assign, reg31, ":rating"),
				# (assign, reg32, ":item_type"),
				# (str_store_item_name, s31, ":item_no"),
				# (display_message, "@DEBUG: {s31} is the new WORST item in type [{reg32}] at {reg31} rating.", gpu_debug),
			(try_end),
		(try_end),
		
		(try_for_range, ":item_no", "itm_sumpter_horse", "itm_items_end"),
			(item_get_type, ":item_type", ":item_no"),
			(eq, ":item_type", ":desired_type"),
			(item_set_slot, ":item_no", slot_item_best_in_type, ":highest_rating"),
			(item_set_slot, ":item_no", slot_item_worst_in_type, ":lowest_rating"),
			# Determine % modifier.
			(store_sub, ":rating_span", ":highest_rating", ":lowest_rating"),
			(call_script, "script_als_get_item_rating", "trp_autoloot_reference", ":item_no", imod_plain), # cms_scripts.py
			(assign, ":rating", reg1),
			(store_sub, ":rating_item", ":rating", ":lowest_rating"),
			(store_mul, ":weight", ":rating_item", 100),
			(val_max, ":rating_span", 1), # Prevent DIV/0 errors.
			(val_div, ":weight", ":rating_span"),
			(item_set_slot, ":item_no", slot_item_rated_weight, ":weight"),
			### DIAGNOSTIC ###
			# (assign, reg31, ":rating"),
			# (assign, reg32, ":weight"),
			# (assign, reg33, ":highest_rating"),
			# (assign, reg34, ":lowest_rating"),
			# (str_store_item_name, s31, ":item_no"),
			# (display_message, "@DEBUG: {s31} weight is {reg32}% ({reg31} rating). Span = {reg34} to {reg33}.", gpu_debug),
		(try_end),
	]),
	
# script_hub_troop_get_recruitment_info
# PURPOSE: Print an info box about a troop for the "recruitment" presentation.
("hub_troop_get_recruitment_info",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":record", 2),
		(store_script_param, ":pos_y", 3),
		(store_script_param, ":recruitable", 4),
		
		(assign, ":color_good", 14336), # Dark Green
		(assign, ":color_bad", 4980736), # Dark Red
		
		## OBJ - TROOP IMAGE
		(store_sub, ":pos_y_portrait", ":pos_y", 100),
		# script_gpu_create_portrait     - troop_id, pos_x, pos_y, size, storage_id
		(call_script, "script_gpu_create_troop_image", ":troop_no", -15, ":pos_y_portrait", 400, 0),
		
		## OBJ - NUMBER OF MEMBERS
		(party_count_companions_of_type, reg21, "p_main_party", ":troop_no"),
		(store_sub, ":pos_y_troop_count", ":pos_y", 105),
		(call_script, "script_gpu_create_text_label", "str_hub_troop_count", 42, ":pos_y_troop_count", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - TROOP NAME
		(store_sub, ":pos_y_line_1", ":pos_y", 0),
		(assign, ":pos_x_col_1", 95),
		(str_store_troop_name, s21, ":troop_no"),
		(str_store_troop_name, s22, ":troop_no"),
		# If troop is a unique location troop then change the name color to a goldish hue.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION), 
			(assign, ":color", gpu_unique), # Goldish yellow.
			(str_store_string, s22, "@{s22} (Unique)"),
		(else_try),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION_UPGRADE), 
			(assign, ":color", gpu_unique), # Goldish yellow.
			(str_store_string, s22, "@{s22} (Unique)"),
		(else_try),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_AFFILIATED),
			(assign, ":color", gpu_affiliated), # Dark Blue
			(str_store_string, s22, "@{s22} (Faction Only)"),
		(else_try),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_DISHONORABLE),
			(assign, ":color", gpu_dishonorable),
			(str_store_string, s22, "@{s22} (Dishonorable)"),
		(else_try),
			(assign, ":color", gpu_black),
		(try_end),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_1", ":pos_y_line_1", 0, gpu_left),
		(overlay_set_color, reg1, ":color"),
		(call_script, "script_gpu_create_text_label", "str_hub_s22", ":pos_x_col_1", ":pos_y_line_1", 0, gpu_left),
		(overlay_set_color, reg1, ":color"),
		
		## LABEL - GENERAL STATISTICS
		(store_sub, ":pos_y_line_2", ":pos_y_line_1", 25),
		(call_script, "script_gpu_create_text_label", "str_hub_general_stats", ":pos_x_col_1", ":pos_y_line_2", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_gpu_create_text_label", "str_hub_general_stats", ":pos_x_col_1", ":pos_y_line_2", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - TROOP LEVEL & TYPE
		(store_sub, ":pos_y_line_3", ":pos_y_line_2", 20),
		(store_troop_faction, ":faction_no", ":troop_no"),
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_MERCENARY),
			(str_store_string, s22, "@Mercenary"),
		(else_try),
			(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(str_store_string, s22, "@Faction Troop"),
		(else_try),
			(is_between, ":troop_no", bandits_begin, bandits_end),
			(str_store_string, s22, "@Outlaw"),
		(else_try),
			(str_store_string, s22, "@Soldier"),
		(try_end),
		(store_character_level, reg21, ":troop_no"),
		(troop_get_slot, reg23, ":troop_no", slot_troop_tier),
		(str_store_string, s23, "@(T{reg23})"),
		(str_store_string, s21, "@Level {reg21} {s22} {s23}"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_1", ":pos_y_line_3", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - ARMOR RATING
		(call_script, "script_hub_troop_get_armor_rating", ":troop_no"), # Returns armor rating to reg1
		(assign, reg21, reg1),
		(store_sub, ":pos_y_line_4", ":pos_y_line_3", 20),
		(call_script, "script_gpu_create_text_label", "str_hub_desc_armor_value", ":pos_x_col_1", ":pos_y_line_4", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		(store_skill_level, ":rating_power_strike", "skl_power_strike", ":troop_no"),
		(val_mul, ":rating_power_strike", rating_multiplier_skill),
		
		## OBJ - MELEE ATTACK RATING
		(store_sub, ":pos_y_line_5", ":pos_y_line_4", 20),
		(call_script, "script_hub_troop_get_melee_rating", ":troop_no"), # Returns melee rating to reg1
		(assign, reg21, reg1),
		(call_script, "script_gpu_create_text_label", "str_hub_desc_melee_value", ":pos_x_col_1", ":pos_y_line_5", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - RANGED ATTACK RATING
		(call_script, "script_hub_troop_get_ranged_rating", ":troop_no"), # Returns ranged rating to reg1
		(assign, reg21, reg1),
		(store_sub, ":pos_y_line_6", ":pos_y_line_5", 20),
		(try_begin),
			(ge, reg21, 1),
			(call_script, "script_gpu_create_text_label", "str_hub_desc_ranged_value", ":pos_x_col_1", ":pos_y_line_6", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
		(else_try),
			(call_script, "script_gpu_create_text_label", "str_hub_no_range", ":pos_x_col_1", ":pos_y_line_6", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
		
		## LABEL - RECRUITMENT REQUIREMENTS
		(assign, ":disable_recruitment", 0),
		(store_add, ":pos_x_col_2", ":pos_x_col_1", 200),
		(call_script, "script_gpu_create_text_label", "str_hub_troop_prereqs", ":pos_x_col_2", ":pos_y_line_2", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_gpu_create_text_label", "str_hub_troop_prereqs", ":pos_x_col_2", ":pos_y_line_2", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(assign, ":pos_y_temp", ":pos_y_line_2"),
		
		## OBJ - REQUIREMENT - PURCHASE COST.
		(val_sub, ":pos_y_temp", 20),
		(call_script, "script_hub_get_purchase_price_for_troop", "$current_town", ":troop_no", "trp_player"), # Returns reg1 (price), reg2 (discount)
		(assign, reg21, reg1),
		(assign, ":modified_cost", reg1),
		(try_begin),
			(neq, reg2, 0),
			(str_store_string, s22, "@ (-{reg2}%)"),
		(else_try),
			(str_clear, s22),
		(try_end),
		(call_script, "script_gpu_create_text_label", "str_hub_troop_cost_modified", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
		(assign, ":obj_requirement", reg1),
		(call_script, "script_gpu_resize_object", 0, 75),
		(try_begin),
			(call_script, "script_cf_diplomacy_treasury_verify_funds", ":modified_cost", "$current_town", FUND_FROM_EITHER, TREASURY_FUNDS_AVAILABLE), # diplomacy_scripts.py
			(overlay_set_color, ":obj_requirement", ":color_good"),
		(else_try),
			(overlay_set_color, ":obj_requirement", ":color_bad"),
			(assign, ":disable_recruitment", 1),
		(try_end),
		
		## OBJ - REQUIREMENT - PERSON TO TRAIN
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_NOBLEMAN),
			(val_sub, ":pos_y_temp", 20),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_noble", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(assign, ":obj_requirement", reg1),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_veteran_pool, 1),
				(overlay_set_color, ":obj_requirement", ":color_good"),
			(else_try),
				(overlay_set_color, ":obj_requirement", ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_MERCENARY),
			(val_sub, ":pos_y_temp", 20),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_mercenary", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(assign, ":obj_requirement", reg1),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_mercenary_pool_player, 1),
				(overlay_set_color, ":obj_requirement", ":color_good"),
			(else_try),
				(overlay_set_color, ":obj_requirement", ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(else_try),
			(val_sub, ":pos_y_temp", 20),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_peasant", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_volunteer_troop_amount, 1),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## OBJ - REQUIREMENT - MOUNT REQUIRED
		(try_begin),
			(this_or_next|troop_is_mounted, ":troop_no"),
			(troop_is_guarantee_horse, ":troop_no"),
			(val_sub, ":pos_y_temp", 20),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_mount", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_horse_pool_player, 1),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## OBJ - REQUIREMENT - CENTER RELATION
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_unique_location, "$current_town"),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_FRIEND), # combat_scripts.py - prereq constants in combat_constants.py
			(assign, reg21, troop_prereq_friend_relation),
			(val_sub, ":pos_y_temp", 20),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_center_relation", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
				## Special case for castles since they have no viable way for the player to gain relation with them.  Use their village instead.
				(try_begin),
					(party_slot_eq, "$current_town", slot_party_type, spt_castle),
					(try_for_range, ":village_no", villages_begin, villages_end),
						(party_slot_eq, ":village_no", slot_village_bound_center, "$current_town"),
						(party_get_slot, ":village_relation", ":village_no", slot_center_player_relation),
						(ge, ":village_relation", ":center_relation"),
						(assign, ":center_relation", ":village_relation"),
					(try_end),
				(try_end),
				(ge, ":center_relation", troop_prereq_friend_relation),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_unique_location, "$current_town"),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_ALLY), # combat_scripts.py - prereq constants in combat_constants.py
			(assign, reg21, troop_prereq_ally_relation),
			(val_sub, ":pos_y_temp", 20),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_center_relation", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(party_get_slot, ":center_relation", "$current_town", slot_center_player_relation),
				(ge, ":center_relation", troop_prereq_ally_relation),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## OBJ - REQUIREMENT - CENTER OWNER
		(try_begin),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_OWNER_ONLY), # combat_scripts.py - prereq constants in combat_constants.py
			(val_sub, ":pos_y_temp", 20),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_owner_only", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## OBJ - REQUIREMENT - AFFILIATED
		(try_begin),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_AFFILIATED), # combat_scripts.py - prereq constants in combat_constants.py
			# SPECIAL CASE - Villages that you have a high relation with ignore this prerequisite.
			(assign, ":ignore_prereq", 0),
			(try_begin),
				(party_slot_eq, "$current_town", slot_party_type, spt_village),
				(party_slot_ge, "$current_town", slot_center_player_relation, 20),
				(assign, ":ignore_prereq", 1),
			(try_end),
			(neq, ":ignore_prereq", 1),
			(store_faction_of_party, ":faction_no", "$current_town"),
			(str_store_faction_name, s21, ":faction_no"),
			(val_sub, ":pos_y_temp", 20),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_affiliated", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(store_faction_of_party, ":faction_no", "$current_town"),
				(eq, ":faction_no", "$players_kingdom"),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## OBJ - REQUIREMENT - ELITE_MERCENARY
		(try_begin),
			(assign, ":continue", 0),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_ELITE_MERCENARY), # combat_scripts.py - prereq constants in combat_constants.py
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			(val_sub, ":pos_y_temp", 20),
			(str_store_string, s21, "@Built: Mercenary Chapterhouse"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_has_merc_chapterhouse, cis_built),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## OBJ - REQUIREMENT - DISHONORABLE
		(try_begin),
			(assign, ":continue", 0),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_DISHONORABLE), # combat_scripts.py - prereq constants in combat_constants.py
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			(val_sub, ":pos_y_temp", 20),
			(str_store_string, s21, "@Player Honor < 1"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(lt, "$player_honor", 1),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## OBJ - REQUIREMENT - LIEGE RELATION
		(try_begin),
			(assign, ":continue", 0),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_LIEGE_RELATION), # combat_scripts.py - prereq constants in combat_constants.py
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			(val_sub, ":pos_y_temp", 20),
			(str_store_string, s21, "@Liege Relation 50+"),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(store_faction_of_party, ":faction_no", "$current_town"),
				(faction_get_slot, ":troop_leader", ":faction_no", slot_faction_leader),
				(ge, ":troop_leader", 0),
				(call_script, "script_troop_get_player_relation", ":troop_leader"),
				(ge, reg1, troop_prereq_liege_relation),
				(overlay_set_color, reg0, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				(assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## BUTTON - RECRUIT TROOP
		(store_sub, ":pos_y_button_1", ":pos_y", 35),
		(store_sub, ":pos_y_button_1_mesh", ":pos_y_button_1", 10),
		(store_add, ":button_obj_slot", hub4_obj_button_recruit_troop, ":record"),
		(try_begin),
			(eq, ":disable_recruitment", 0),
			(eq, ":recruitable", 1), # So we can dump troops of the wrong type.
			(call_script, "script_gpu_create_mesh", "mesh_button_up", 545, ":pos_y_button_1_mesh", 600, 500),
			(call_script, "script_gpu_create_button", "str_hub_button_recruit", 573, ":pos_y_button_1", ":button_obj_slot"),
			(call_script, "script_gpu_resize_object", ":button_obj_slot", 75),
		(else_try),
			(store_add, ":pos_y_disabled", ":pos_y_button_1", 10),
			(call_script, "script_gpu_create_mesh", "mesh_button_down", 545, ":pos_y_button_1_mesh", 600, 500),
			(call_script, "script_gpu_create_text_label", "str_hub_button_recruit", 620, ":pos_y_disabled", 0, gpu_center),
			(overlay_set_color, reg1, gpu_gray),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
		
		## BUTTON - DISMISS TROOP
		(store_sub, ":pos_y_button_2", ":pos_y_button_1", 45),
		(store_sub, ":pos_y_button_2_mesh", ":pos_y_button_2", 10),
		(store_add, ":button_obj_slot", hub4_obj_button_dismiss_troop, ":record"),
		(try_begin),
			(party_count_companions_of_type, ":troop_count", "p_main_party", ":troop_no"),
			(ge, ":troop_count", 1),
			# (main_party_has_troop, ":troop_no"),
			(call_script, "script_gpu_create_mesh", "mesh_button_up", 545, ":pos_y_button_2_mesh", 600, 500),
			(call_script, "script_gpu_create_button", "str_hub_button_dismiss", 573, ":pos_y_button_2", ":button_obj_slot"),
			(call_script, "script_gpu_resize_object", ":button_obj_slot", 75),
		(else_try),
			(store_add, ":pos_y_disabled", ":pos_y_button_2", 10),
			(call_script, "script_gpu_create_mesh", "mesh_button_down", 545, ":pos_y_button_2_mesh", 600, 500),
			(call_script, "script_gpu_create_text_label", "str_hub_button_dismiss", 620, ":pos_y_disabled", 0, gpu_center),
			(overlay_set_color, reg1, gpu_gray),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
		
		## BUTTON - INSPECT EQUIPMENT
		(store_sub, ":pos_y_button_3", ":pos_y_button_2", 45),
		(store_sub, ":pos_y_button_3_mesh", ":pos_y_button_3", 10),
		(store_add, ":button_obj_slot", hub4_obj_button_inspect_equipment, ":record"),
		(store_add, ":button_val_slot", hub4_val_button_troop_no, ":record"),
		(call_script, "script_gpu_create_mesh", "mesh_button_up", 545, ":pos_y_button_3_mesh", 600, 500),
		(call_script, "script_gpu_create_button", "str_hub_button_inspect_gear", 558, ":pos_y_button_3", ":button_obj_slot"),
		(call_script, "script_gpu_resize_object", ":button_obj_slot", 75),
		(troop_set_slot, HUB_OBJECTS, ":button_val_slot", ":troop_no"),
		
		## TROOP DIVIDER LINE
	]),

# script_hub_determine_purchase_cost
# This script is called from game engine for calculating needed troop upgrade exp
("hub_determine_purchase_cost",
	[
		(store_script_param_1, ":troop_no"),
		
		(try_begin), #Do not calculate recruitment cost once it has been determined - this improves performance and allows for static cost determination
			(troop_get_slot, ":troop_cost", ":troop_no", slot_troop_purchase_cost),
			(gt, ":troop_cost", 1),
			(assign, reg1, ":troop_cost"),
		(else_try),
			## ATTRIBUTES ## - (STR-10 + AGI-10)*8
			(store_attribute_level, ":STR", ":troop_no", ca_strength),
			(val_sub, ":STR", 10),
			(val_max, ":STR", 1),
			(store_attribute_level, ":AGI", ":troop_no", ca_agility),
			(val_sub, ":AGI", 10),
			(val_max, ":AGI", 1),
			(store_add, ":rating_attributes", ":STR", ":AGI"),
			(val_mul, ":rating_attributes", 8),
			
			## SKILLS ## - Value 5-10 per point depending on skill.
			(assign, ":rating_skills", 0),
			## HORSE ARCHERY - Only applies if troop is mounted & ranged.
			(try_begin),
				(troop_is_guarantee_ranged, ":troop_no"),
				(this_or_next|troop_is_mounted, ":troop_no"),
				(troop_is_guarantee_horse, ":troop_no"),
				(store_skill_level, ":skill_horse_archery", "skl_horse_archery", ":troop_no"),
				(val_mul, ":skill_horse_archery", 6),
				(val_add, ":rating_skills", ":skill_horse_archery"),
			(try_end),
			(try_begin),
				## RIDING - Only applies if troop is mounted.
				(this_or_next|troop_is_mounted, ":troop_no"),
				(troop_is_guarantee_horse, ":troop_no"),
				(store_skill_level, ":skill_riding", "skl_riding", ":troop_no"),
				(val_mul, ":skill_riding", 8),
				(val_add, ":rating_skills", ":skill_riding"),
			(else_try),
				## ATHLETICS - Only applies if troop is not mounted.
				(store_skill_level, ":skill_athletics", "skl_athletics", ":troop_no"),
				(val_mul, ":skill_athletics", 5),
				(val_add, ":rating_skills", ":skill_athletics"),
			(try_end),
			## IRONFLESH - Always applicable.
			(store_skill_level, ":skill_ironflesh", "skl_ironflesh", ":troop_no"),
			(val_mul, ":skill_ironflesh", 10),
			(val_add, ":rating_skills", ":skill_ironflesh"),
			
			## ARMOR RATING ## - Item Rating * Placement Weight * 25 / 1000
			(call_script, "script_hub_troop_get_armor_rating", ":troop_no"), # Returns armor rating to reg1
			(assign, ":rating_armor", reg1),
			
			## MELEE ATTACK RATING
			(call_script, "script_hub_troop_get_melee_rating", ":troop_no"), # Returns melee rating to reg1
			(assign, ":rating_melee", reg1),
					
			## RANGED ATTACK RATING
			## FORMULA = (Item Rating * 3) + (Proficiency * 2) + (Power Draw/Throw * rating_multiplier_skill)
			(try_begin),
				(troop_is_guarantee_ranged, ":troop_no"),
				(call_script, "script_hub_troop_get_ranged_rating", ":troop_no"), # Returns ranged rating to reg1
				(assign, ":rating_ranged", reg1),
				
				(store_mul, ":discount_ranged", ":rating_ranged", rating_ranged_melee_discount), # -15%
				(val_div, ":discount_ranged", 100),
				(store_mul, ":discount_melee", ":rating_melee", rating_ranged_melee_discount), # -15%
				(val_div, ":discount_melee", 100),
			(else_try),
				(assign, ":rating_ranged", 0),
				(assign, ":discount_ranged", 0),
				(assign, ":discount_melee", 0),
			(try_end),
			
			## PUT IT ALL TOGETHER ##
			(assign, ":rating_total", ":rating_attributes"),
			(val_add, ":rating_total", ":rating_skills"),
			(val_add, ":rating_total", ":rating_armor"),
			(val_add, ":rating_total", ":rating_melee"),
			(val_add, ":rating_total", ":rating_ranged"),
			(val_sub, ":rating_total", ":discount_ranged"),
			(val_sub, ":rating_total", ":discount_melee"),
			
			### DIAGNOSTIC ###
			(try_begin),
				(ge, DEBUG_RECRUITMENT, 2),
				(assign, reg31, ":rating_attributes"),
				(assign, reg32, ":rating_skills"),
				(assign, reg33, ":rating_armor"),
				(assign, reg34, ":rating_melee"),
				(assign, reg35, ":rating_ranged"),
				(assign, reg36, ":discount_melee"),
				(assign, reg37, ":discount_ranged"),
				(str_store_troop_name, s31, ":troop_no"),
				(display_message, "@{s31} = Att {reg31} + Skill {reg32} + Armor {reg33} + Melee {reg34}(-{reg36}) + Rng {reg35}(-{reg37}).", gpu_debug),
			(try_end),
			
			## DETERMINE TIER
			# This is done prior to scaling rating up based on mounted/ranged.  It is a true representation of how strong a unit is.
			(store_div, ":tier", ":rating_total", 175),
			(val_max, ":tier", 1),
			(troop_set_slot, ":troop_no", slot_troop_tier, ":tier"),
			
			# Stored for debugging.
			(assign, reg65, ":rating_total"),
			
			## GUARANTEES ## - Mounted (+45%)
			(assign, ":rating_guarantees", 0),
			(assign, ":cost_uprate", 0),
			(try_begin),
				(this_or_next|troop_is_mounted, ":troop_no"),
				(troop_is_guarantee_horse, ":troop_no"),
				(assign, ":cost_uprate", 45),
			(try_end),
			(try_begin),
				(ge, ":cost_uprate", 1),
				(store_mul, ":rating_boost", ":rating_total", ":cost_uprate"),
				(val_div, ":rating_boost", 100),
				(val_add, ":rating_guarantees", ":rating_boost"),
			(try_end),
			(val_add, ":rating_total", ":rating_guarantees"),
			
			## TIER MULTIPLIER ##
			(val_add, ":rating_total", ":discount_ranged"),
			(val_add, ":rating_total", ":discount_melee"),
			
			(store_add, ":tier_multiplier", ":tier", 7),
			(val_mul, ":tier", ":tier_multiplier"),
			(val_mul, ":rating_total", ":tier"),
			(val_div, ":rating_total", 100),
			
			## Set minimum pricing for mounted troops.
			(try_begin),
				(this_or_next|troop_is_mounted, ":troop_no"),
				(troop_is_guarantee_horse, ":troop_no"),
				(val_max, ":rating_total", 150),
			(try_end),
			
			## DISHONORABLE TROOPS ## - Reduce price by 60%.
			(try_begin),
				(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_DISHONORABLE),
				(store_mul, ":discount_dishonorable", ":rating_total", 60),
				(val_div, ":discount_dishonorable", 100),
				(val_sub, ":rating_total", ":discount_dishonorable"),
			(try_end),
			
			## CHEAP TROOPS ## - Reduce price by 40%.
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_CHEAP),
				(store_mul, ":discount_cheap", ":rating_total", 40),
				(val_div, ":discount_cheap", 100),
				(val_sub, ":rating_total", ":discount_cheap"),
			(try_end),
			

			(troop_set_slot, ":troop_no", slot_troop_purchase_cost, ":rating_total"),
			(assign, reg1, ":rating_total"),
		(try_end),
		]),
		
	# script_hub_troop_get_melee_rating
	# PURPOSE: Return the melee rating of a troop.
	# EXAMPLE: (call_script, "script_hub_troop_get_melee_rating", ":troop_no"), # Returns melee rating to reg1
("hub_troop_get_melee_rating",
	[
	(store_script_param, ":troop_no", 1),
	
	(store_skill_level, ":rating_power_strike", "skl_power_strike", ":troop_no"),
	(val_mul, ":rating_power_strike", rating_multiplier_skill),
	
	## FORMULA = (Item Rating * 3) + (Proficiency * 2) + (Power Strike * rating_multiplier_skill)
	(assign, ":rating", 0),
	(assign, ":weapon_count", 0),
	
	## ONE-HANDED WEAPONS
	(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_one_handed_wpn),
	(store_mul, ":item_rating", reg1, 3),
	(store_proficiency_level, ":prof", ":troop_no", wpt_one_handed_weapon),
	(val_mul, ":prof", 2),
	(try_begin),
		(ge, reg1, 1),
		(val_add, ":item_rating", ":prof"),
		(val_add, ":item_rating", ":rating_power_strike"),
		(val_add, ":weapon_count", 1),
		(val_add, ":rating", ":item_rating"),
	(try_end),
	
	## TWO-HANDED WEAPONS
	(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_two_handed_wpn),
	(store_mul, ":item_rating", reg1, 3),
	(store_proficiency_level, ":prof", ":troop_no", wpt_two_handed_weapon),
	(val_mul, ":prof", 2),
	(try_begin),
		(ge, reg1, 1),
		(val_add, ":item_rating", ":prof"),
		(val_add, ":item_rating", ":rating_power_strike"),
		(val_add, ":weapon_count", 1),
		(val_add, ":rating", ":item_rating"),
	(try_end),
	
	## POLEARMS
	(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_polearm),
	(store_mul, ":item_rating", reg1, 3),
	(store_proficiency_level, ":prof", ":troop_no", wpt_polearm),
	(val_mul, ":prof", 2),
	(try_begin),
		(ge, reg1, 1),
		(val_add, ":item_rating", ":prof"),
		(val_add, ":item_rating", ":rating_power_strike"),
		(val_add, ":weapon_count", 1),
		(val_add, ":rating", ":item_rating"),
	(try_end),
	
	(val_max, ":weapon_count", 1), # Prevent DIV/0 errors.
	(store_div, ":rating_melee", ":rating", ":weapon_count"),
	(val_mul, ":rating_melee", rating_multiplier_weapon), # 40%
	(val_div, ":rating_melee", 100),
		
	(assign, reg1, ":rating_melee"),
]),
	
# script_hub_troop_get_ranged_rating
# PURPOSE: Return the ranged rating of a troop.
# EXAMPLE: (call_script, "script_hub_troop_get_ranged_rating", ":troop_no"), # Returns ranged rating to reg1
("hub_troop_get_ranged_rating",
    [
		(store_script_param, ":troop_no", 1),
		
		## FORMULA = (Item Rating * 3) + (Proficiency * 2) + (Power Draw/Throw * rating_multiplier_skill)
		(assign, ":rating", 0),
		(assign, ":weapon_count", 0),
		
		## ARCHERY
		(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_bow),
		(store_mul, ":item_rating", reg1, rating_multiplier_weapon_weight),
		(store_proficiency_level, ":prof", ":troop_no", wpt_archery),
		(val_mul, ":prof", 2),
		(store_skill_level, ":rating_power_draw", "skl_power_draw", ":troop_no"),
		(val_mul, ":rating_power_draw", rating_multiplier_skill),
		(try_begin),
			(ge, reg1, 1),
			(val_add, ":item_rating", ":prof"),
			(val_add, ":item_rating", ":rating_power_draw"),
			(val_add, ":weapon_count", 1),
			(val_add, ":rating", ":item_rating"),
		(try_end),
		
		## CROSSBOWS
		# Special Case: Crossbows get x3 on weapon proficiency.
		# Special Case: Crossbows get x4 on weapon rating.
		(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_crossbow),
		(store_mul, ":item_rating", reg1, 4),
		(store_proficiency_level, ":prof", ":troop_no", wpt_crossbow),
		(val_mul, ":prof", 3),
		(try_begin),
			(ge, reg1, 1),
			(val_add, ":item_rating", ":prof"),
			(val_add, ":weapon_count", 1),
			(val_add, ":rating", ":item_rating"),
		(try_end),
		
		## THROWN ITEMS
		(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_thrown),
		(store_mul, ":item_rating", reg1, rating_multiplier_weapon_weight),
		(store_proficiency_level, ":prof", ":troop_no", wpt_throwing),
		(val_mul, ":prof", 2),
		(store_skill_level, ":rating_power_throw", "skl_power_throw", ":troop_no"),
		(val_mul, ":rating_power_throw", rating_multiplier_skill),
		(try_begin),
			(ge, reg1, 1),
			(val_add, ":item_rating", ":prof"),
			(val_add, ":item_rating", ":rating_power_throw"),
			(val_add, ":weapon_count", 1),
			(val_add, ":rating", ":item_rating"),
		(try_end),
		
		(val_max, ":weapon_count", 1), # Prevent DIV/0 errors.
		(store_div, ":rating_ranged", ":rating", ":weapon_count"),
		(val_mul, ":rating_ranged", rating_multiplier_weapon), # 40%
		(val_div, ":rating_ranged", 100),
		
		(assign, reg1, ":rating_ranged"),
	]),
	
# script_hub_troop_get_armor_rating
# PURPOSE: Return the armor rating of a troop.
# EXAMPLE: (call_script, "script_hub_troop_get_armor_rating", ":troop_no"), # Returns armor rating to reg1
("hub_troop_get_armor_rating",
    [
		(store_script_param, ":troop_no", 1),
		
		(assign, ":rating", 0),
		## HEAD ARMOR
		(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_head_armor),
		(store_mul, ":item_rating", reg1, 60),
		(val_mul, ":item_rating", rating_multiplier_armor),
		(val_div, ":item_rating", 1000),
		(val_add, ":rating", ":item_rating"),
		## BODY ARMOR
		(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_body_armor),
		(store_mul, ":item_rating", reg1, 100),
		(val_mul, ":item_rating", rating_multiplier_armor),
		(val_div, ":item_rating", 1000),
		(val_add, ":rating", ":item_rating"),
		## FOOT ARMOR
		(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_foot_armor), 
		(store_mul, ":item_rating", reg1, 35),
		(val_mul, ":item_rating", rating_multiplier_armor),
		(val_div, ":item_rating", 1000),
		(val_add, ":rating", ":item_rating"),
		## HAND ARMOR
		(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_hand_armor), 
		(store_mul, ":item_rating", reg1, 15),
		(val_mul, ":item_rating", rating_multiplier_armor),
		(val_div, ":item_rating", 1000),
		(val_add, ":rating", ":item_rating"),
		## SHIELDS
		(call_script, "script_hub_troop_get_average_value_of_item_type", ":troop_no", itp_type_shield),
		(store_mul, ":item_score", reg1, 3),
		(store_skill_level, ":skill_shield", "skl_shield", ":troop_no"),
		(val_mul, ":skill_shield", 8),
		(store_add, ":item_rating", ":item_score", ":skill_shield"),
		(val_div, ":item_rating", 3),
		(val_add, ":rating", ":item_rating"),
		## OBJ - ARMOR RATING
		
		(assign, reg1, ":rating"),
	]),
	
# script_hub_update_improvement_screen
# PURPOSE: This is called to update elements of the hub_improvements presentation without restarting it.
("hub_update_improvement_screen",
    [
		(store_sub, ":native_span", native_improvements_end, native_improvements_begin),
		(store_sub, ":lower_limit", center_improvements_begin, ":native_span"),
		
		(troop_get_slot, ":slider_setting", HUB_OBJECTS, hub3_val_slider_improvement_selector),
		(troop_get_slot, ":obj_label", HUB_OBJECTS, hub3_obj_label_improvement_name),
		(troop_get_slot, ":obj_desc", HUB_OBJECTS, hub3_obj_label_improvement_desc),
		(troop_get_slot, ":obj_time", HUB_OBJECTS, hub3_obj_label_improvement_time),
		(troop_get_slot, ":obj_cost", HUB_OBJECTS, hub3_obj_label_improvement_cost),
		(troop_get_slot, ":obj_build_button", HUB_OBJECTS, hub3_obj_button_improvement_build),
		(troop_get_slot, ":obj_applicable", HUB_OBJECTS, hub3_obj_label_improvement_applicable),
			(try_begin), # Fix our out of place native improvements.
			(lt, ":slider_setting", center_improvements_begin),
			(store_sub, ":offset", ":slider_setting", ":lower_limit"),
			(store_add, ":improvement_no", native_improvements_begin, ":offset"),
		(else_try),
			(assign, ":improvement_no", ":slider_setting"),
		(try_end),
		
		## UPDATE - IMPROVEMENT BUILD BUTTON
		(assign, ":improvement_is_buildable", 0),
		(assign, ":string_build", "str_hub_button_build"),
		(assign, ":string_time", "str_hub_build_time"),
		(assign, ":string_cost", "str_hub_build_cost"),
		(try_begin), # Repairing
			(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement_no"),
			(party_slot_ge, "$current_town", ":improvement_no", cis_built), # Capture repair attempts.
			(assign, ":string_build", "str_hub_button_repair"),
			(assign, ":improvement_is_buildable", 1),
		(else_try), # Building
			(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement_no"),
			(assign, ":improvement_is_buildable", 1),
		(else_try), # Already built.
			(party_slot_eq, "$current_town", ":improvement_no", cis_built), # Capture repair attempts.
			(assign, ":string_time", "str_hub_build_time_done"),
			(assign, ":string_cost", "str_hub_build_cost_done"),
		(try_end),
		(overlay_set_text, ":obj_build_button", ":string_build"),
		(call_script, "script_gpu_set_button_status", hub3_obj_button_improvement_build, ":improvement_is_buildable"),
		
		## UPDATE - IMPROVEMENT DESCRIPTIONS
		(call_script, "script_get_improvement_details", ":improvement_no"),
		(assign, ":applicable_locations", reg1),
		(str_store_string, s21, s0),
		(overlay_set_text, ":obj_label", "str_hub_s21"),
		(overlay_set_text, ":obj_desc", "@{s1}"),
		(call_script, "script_improvement_get_building_time_and_cost", "$current_town", ":improvement_no"),
		(assign, reg21, reg1),
		(store_sub, reg3, reg1, 1),
		(overlay_set_text, ":obj_time", ":string_time"),
		(overlay_set_text, ":obj_cost", ":string_cost"),
		
		## UPDATE - IMPROVEMENT DESTROY BUTTON
		(assign, ":improvement_is_destroyable", 0),
		(try_begin),
			(party_slot_ge, "$current_town", ":improvement_no", cis_built),
			(assign, ":improvement_is_destroyable", 1),
		(try_end),
		(call_script, "script_gpu_set_button_status", hub3_obj_button_improvement_destroy, ":improvement_is_destroyable"),
		
		## UPDATE - IMPROVEMENT INSTANT CREATION BUTTON
		(try_begin),
			(ge, DEBUG_IMPROVEMENTS, 1),
			(assign, ":improvement_in_progress", 0),
			
			## DETERMINE THE IMPROVEMENT WE'RE WORKING WITH.
			(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_slider_improvement_selector),
			(try_begin), # Fix our out of place native improvements.
				(lt, ":setting", center_improvements_begin),
				(store_sub, ":offset", ":setting", ":lower_limit"),
				(store_add, ":improvement_no", native_improvements_begin, ":offset"),
			(else_try),
				(assign, ":improvement_no", ":setting"),
			(try_end),
			
			(try_begin), # Repairing
				(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement_no"), # improvements_scripts.py
				(party_slot_ge, "$current_town", ":improvement_no", cis_built), # Capture repair attempts.
				(assign, ":string_build", "str_hub_button_repair"),
				(assign, ":improvement_in_progress", 1),
			(else_try), # Building
				(call_script, "script_cf_improvement_can_be_built_here", "$current_town", ":improvement_no"), # improvements_scripts.py
				(assign, ":improvement_in_progress", 1),
			(else_try),
				(this_or_next|party_slot_eq, "$current_town", slot_center_current_improvement_1, ":improvement_no"),
				(this_or_next|party_slot_eq, "$current_town", slot_center_current_improvement_2, ":improvement_no"),
				(party_slot_eq, "$current_town", slot_center_current_improvement_3, ":improvement_no"),
				(assign, ":improvement_in_progress", 1),
			(try_end),
			(call_script, "script_gpu_set_button_status", hub3_obj_button_improvement_complete, ":improvement_in_progress"),
		(try_end),
		
		## UPDATE - IMPROVEMENT APPLICABILITY
		(try_begin),
			(eq, ":applicable_locations", imp_allowed_in_any),
			(assign, ":string_applicable", "str_hub_center_type_vct"),
		(else_try),
			(eq, ":applicable_locations", imp_allowed_in_village),
			(assign, ":string_applicable", "str_hub_center_type_v"),
		(else_try),
			(eq, ":applicable_locations", imp_allowed_in_castle),
			(assign, ":string_applicable", "str_hub_center_type_c"),
		(else_try),
			(eq, ":applicable_locations", imp_allowed_in_town),
			(assign, ":string_applicable", "str_hub_center_type_t"),
		(else_try),
			(eq, ":applicable_locations", imp_allowed_in_village_town),
			(assign, ":string_applicable", "str_hub_center_type_vt"),
		(else_try),
			(eq, ":applicable_locations", imp_allowed_in_village_castle),
			(assign, ":string_applicable", "str_hub_center_type_vc"),
		(else_try),
			(eq, ":applicable_locations", imp_allowed_in_walled_center),
			(assign, ":string_applicable", "str_hub_center_type_ct"),
		(try_end),
		(overlay_set_text, ":obj_applicable", ":string_applicable"),
		
	]),
	
# script_cf_hub_troop_can_be_recruited_here
# PURPOSE: Filters out any conditions that would prevent a troop from showing up in a recruitment list.
# EXAMPLE: (call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", ":troop_recruit", ":troop_buyer"),
("cf_hub_troop_can_be_recruited_here",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_recruit", 2),
		(store_script_param, ":troop_buyer", 3),
		
		## NO HEROES
		(neg|troop_is_hero, ":troop_recruit"),
		
		(assign, ":recruitable", 0),
		(store_faction_of_party, ":faction_no", ":center_no"),
		(party_get_slot, ":culture", "$current_town", slot_center_culture),
		
		## RELATION TO BUYER - How does this troop feel about you?
		(try_begin),
			(eq, ":troop_buyer", "trp_player"),
			(party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),
			(store_relation, ":faction_relation", ":faction_no", "fac_player_faction"),
			(this_or_next|ge, ":center_relation", 5),
			(this_or_next|eq, ":faction_no", "$players_kingdom"),
			(this_or_next|ge, ":faction_relation", 0),
			(this_or_next|eq, ":faction_no", "$supported_pretender_old_faction"),
			(eq, "$players_kingdom", 0),
			(assign, ":recruitable", 1),
		(else_try),
			(neq, ":troop_buyer", "trp_player"),
			(store_troop_faction, ":faction_buyer", ":troop_buyer"),
			(store_relation, ":faction_relation", ":faction_no", ":faction_buyer"),
			(ge, ":faction_relation", 0),
			(assign, ":recruitable", 1),
		(try_end),
		
		### DIAGNOSTIC ###
		# (try_begin),
			# (this_or_next|eq, ":troop_recruit", "trp_nord_warrior"), # Just need one to test.
			# (eq, ":troop_recruit", "trp_vaegir_infantry"), # Just need one to test.
			# (str_store_party_name, s30, ":center_no"),
			# (str_store_faction_name, s31, ":culture"),
			# (str_store_faction_name, s32, "$players_kingdom"),
			# (str_store_troop_name, s33, ":troop_recruit"),
			# (assign, reg31, ":culture"),
			# (assign, reg32, "$players_kingdom"),
			# (assign, reg33, ":faction_relation"),
			# (assign, reg34, ":center_relation"),
			# (assign, reg35, ":recruitable"),
			# (display_message, "@DEBUG: {s33} is {reg35?recruitable:NOT recruitable} in {s30}.", gpu_green),
			# (eq, ":recruitable", 0),
			# (display_message, "@DEBUG: {s30} is in faction {s31}/{reg31}.  Player is in faction {s32}/{reg32}.", gpu_debug),
			# (display_message, "@DEBUG: Player relation with {s30} is {reg34}.  Faction relation with {s30} is {reg33}.", gpu_debug),
		# (try_end),
		### DIAGNOSTIC ###
		
		# Faction Filter
		(try_begin),
			(is_between, ":troop_recruit", kingdom_troops_begin, kingdom_troops_end),
			(neg|troop_slot_eq, ":troop_recruit", slot_troop_recruitable_faction_1, ":culture"),
			(neg|troop_slot_eq, ":troop_recruit", slot_troop_recruitable_faction_2, ":culture"),
			(neg|troop_slot_eq, ":troop_recruit", slot_troop_recruitable_faction_3, ":culture"),
			# FILTER - Keep out unique units since they don't have a culture and will fail this.
			(troop_slot_eq, ":troop_recruit", slot_troop_unique_location, 0),
			(assign, ":recruitable", 0),
		(try_end),
		
		### DIAGNOSTIC ###
		# (try_begin),
			# (this_or_next|eq, ":troop_recruit", "trp_nord_champion"), # Just need one to test.
			# (eq, ":troop_recruit", "trp_r_nord_huscarl"), # Just need one to test.
			# (str_store_party_name, s30, ":center_no"),
			# (str_store_faction_name, s31, ":culture"),
			# (str_store_faction_name, s32, "$players_kingdom"),
			# (str_store_troop_name, s33, ":troop_recruit"),
			# (assign, reg31, ":culture"),
			# (assign, reg32, "$players_kingdom"),
			# (assign, reg33, ":faction_relation"),
			# (assign, reg34, ":center_relation"),
			# (assign, reg35, ":recruitable"),
			# (display_message, "@DEBUG: {s33} is {reg35?recruitable:NOT recruitable} in {s30}. [faction filter]", gpu_green),
		# (try_end),
		### DIAGNOSTIC ###
		
		## UPGRADED TROOPS
		(try_for_range, ":troop_base", troop_definitions_begin, troop_definitions_end),
			(troop_get_upgrade_troop, ":upgrade_0", ":troop_base", 0),
			(troop_get_upgrade_troop, ":upgrade_1", ":troop_base", 1),
			(eq, ":upgrade_1", -1), # do not remove troops which are actual upgrades, not veteran/elite units
			(this_or_next|eq, ":upgrade_0", ":troop_recruit"),
			(eq, ":upgrade_1", ":troop_recruit"),
			(assign, ":recruitable", 0),
		(try_end),
		
		## TIER LIMITER - Villages
		(try_begin),
			(party_slot_eq, "$current_town", slot_party_type, spt_village),
			(faction_get_slot, ":recruit_tier", ":faction_no", slot_faction_village_recruit_tier),
			(val_add, ":recruit_tier", 1),
			## BUGFIX (Temporary) - Swadia has no recruitable tier 1 soldiers.
			(assign, ":minimum", 1),
			(try_begin),
				(eq, ":faction_no", "fac_kingdom_1"), # Swadia
				(assign, ":minimum", 2),
			(try_end),
			(val_clamp, ":recruit_tier", ":minimum", 4), # Limit to tier 3.
			(call_script, "script_diplomacy_determine_troop_tier", ":troop_recruit"),
			(lt, ":recruit_tier", reg1),
			(assign, ":recruitable", 0),
		(try_end),
		
		## UNIQUE TROOPS
		(try_begin),
			## Capture unique troops that didn't come from this place and make them unrecruitable.
			(neg|troop_slot_eq, ":troop_recruit", slot_troop_unique_location, ":center_no"),
			(troop_get_slot, ":unique_center", ":troop_recruit", slot_troop_unique_location),
			(is_between, ":unique_center", centers_begin, centers_end),
			(assign, ":recruitable", 0),
		(else_try),
			## AI Buyer.
			(troop_slot_eq, ":troop_recruit", slot_troop_unique_location, ":center_no"),
			(neq, ":troop_buyer", "trp_player"),
			(store_troop_faction, ":faction_ai", ":troop_buyer"),
			(eq, ":faction_ai", ":faction_no"),
			(assign, ":recruitable", 0),
		(try_end),
		
		## MERCENARIES
		(try_begin),
			(is_between, ":troop_recruit", mercenary_troops_begin, mercenary_troops_end),
			(try_begin),
				(neg|party_slot_eq, ":center_no", slot_party_type, spt_town), # Mercenaries are only in towns.
				(assign, ":recruitable", 0),
			(try_end),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_recruit", PREREQ_ELITE_MERCENARY),
			# Mercenaries that require a mercenary chapterhouse
			(neg|party_slot_ge, ":center_no", slot_center_has_merc_chapterhouse, cis_built), # Not built at all.
			(assign, ":recruitable", 0),
		(try_end),
		
		## DISHONORABLE TROOPS
		(try_begin),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_recruit", PREREQ_DISHONORABLE),
			(neg|troop_slot_eq, ":troop_recruit", slot_troop_recruitable_faction_1, ":culture"),
			(neg|troop_slot_eq, ":troop_recruit", slot_troop_recruitable_faction_2, ":culture"),
			(neg|troop_slot_eq, ":troop_recruit", slot_troop_recruitable_faction_3, ":culture"),
			(assign, ":recruitable", 0),
		(try_end),
		
		(eq, ":recruitable", 1),
	]),
	
# script_hub_ai_lord_considers_recruits_in_center
# PURPOSE: Filters out any conditions that would prevent a troop from showing up in a recruitment list.
("hub_ai_lord_considers_recruits_in_center",
    [
		(store_script_param, ":lord_no", 1),
		(store_script_param, ":center_no", 2),
		
		(party_get_slot, ":culture", ":center_no", slot_center_original_faction),
		(try_begin),
			(is_between, ":culture", kingdoms_begin, kingdoms_end),
			(assign, ":faction_no", ":culture"),
		(else_try),
			(store_sub, ":faction_no", ":culture", "fac_culture_1"),
			(val_add, ":faction_no", kingdoms_begin),
		(try_end),
		
		(try_begin),
			# Is this NPC a kingdom hero?
			(troop_slot_eq, ":lord_no", slot_troop_occupation, slto_kingdom_hero),
			# Get current capacity for this lord's party.
			(troop_get_slot, ":party_no", ":lord_no", slot_troop_leaded_party),
			(party_get_free_companions_capacity, ":capacity", ":party_no"),
			(ge, ":capacity", 1),
			# Is this party active?
			(party_is_active, ":party_no"),
			
			# Get our desired troop types.
			(call_script, "script_hub_ai_lord_determines_needed_troop_type", ":lord_no"),
			(assign, ":infantry", reg1),
			(assign, ":archers", reg2),
			(assign, ":cavalry", reg3),
			(assign, ":horse_archers", reg4),
			
			##### FACTION CHOICES #####
			(try_begin),
				### SWADIA ###
				(eq, ":faction_no", "fac_kingdom_1"),
				# Cavalry
				(try_begin),
					(ge, ":cavalry", 1),
					(try_begin), ## UNIQUE - PRAVEN
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_praven_knight", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_praven_knight", ":lord_no", ":cavalry"),
					(else_try), ## UNIQUE - DHIRIM
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_dhirim_captain", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_dhirim_captain", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_man_at_arms", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_man_at_arms", ":lord_no", ":cavalry"),
					(else_try), ## AFFILIATED - SWADIA
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_lancer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_lancer", ":lord_no", ":cavalry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_CAVALRY, ":cavalry"),
				(try_end),
				# infantry
				(try_begin),
					(ge, ":infantry", 1),
					(try_begin), ## AFFILIATED - SWADIA
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_sergeant", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_sergeant", ":lord_no", ":infantry"),
					(else_try), ## AFFILIATED - SWADIA
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_sentinel", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_sentinel", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_billman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_billman", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_footman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_footman", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_militia", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_militia", ":lord_no", ":infantry"),
					(else_try), ## AFFILIATED - SWADIA
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_supplyman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_supplyman", ":lord_no", ":infantry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_INFANTRY, ":infantry"),
				(try_end),
				# archers
				(try_begin),
					(ge, ":archers", 1),
					(try_begin), ## UNIQUE - SUNO
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_suno_master_archer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_suno_master_archer", ":lord_no", ":archers"),
					(else_try), ## UNIQUE - TILBAUT CASTLE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_tilbaut_archer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_tilbaut_archer", ":lord_no", ":archers"),
					(else_try), ## MERCENARY - SWADIA
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_mercenary", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_mercenary", ":lord_no", ":archers"),
					(else_try), ## AFFILIATED - SWADIA
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_hunter", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_hunter", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_crossbowman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_crossbowman", ":lord_no", ":archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_ARCHERS, ":archers"),
				(try_end),
				# horse archers
				(try_begin),
					(ge, ":horse_archers", 1),
					# (try_begin),
						# (call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_", ":lord_no"),
						# (call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_", ":lord_no", ":horse_archers"),
					# (try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_HORSE_ARCHERS, ":horse_archers"),
				(try_end),
				
			(else_try),
				### VAEGIRS ###
				(eq, ":faction_no", "fac_kingdom_2"),
				# Cavalry
				(try_begin),
					(ge, ":cavalry", 1),
					(try_begin), ## AFFILIATED - VAEGIRS
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_bogatyr", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_bogatyr", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_cavalrycaptain", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_cavalrycaptain", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_koursores", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_koursores", ":lord_no", ":cavalry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_CAVALRY, ":cavalry"),
				(try_end),
				# infantry
				(try_begin),
					(ge, ":infantry", 1),
					(try_begin), ## AFFILIATED - VAEGIRS
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_vanguard", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_vanguard", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_peltast", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_peltast", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_psiloi", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_psiloi", ":lord_no", ":infantry"),
					(else_try), ## AFFILIATED - VAEGIRS
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_sentry", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_sentry", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_militia", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_militia", ":lord_no", ":infantry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_INFANTRY, ":infantry"),
				(try_end),
				# archers
				(try_begin),
					(ge, ":archers", 1),
					(try_begin), ## AFFILIATED - VAEGIRS
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_marksman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_marksman", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_longbowman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_longbowman", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_skirmisher", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_skirmisher", ":lord_no", ":archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_ARCHERS, ":archers"),
				(try_end),
				# horse archers
				(try_begin),
					(ge, ":horse_archers", 1),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_pecheneg", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_pecheneg", ":lord_no", ":horse_archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_HORSE_ARCHERS, ":horse_archers"),
				(try_end),
				
			(else_try),
				### KHERGITS ###
				(eq, ":faction_no", "fac_kingdom_3"),
				# Cavalry
				(try_begin),
					(ge, ":cavalry", 1),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_morici", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_morici", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_raider", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_raider", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_lancer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_lancer", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_narcarra", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_narcarra", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_torguu", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_torguu", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_noyan", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_noyan", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_keshig", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_keshig", ":lord_no", ":cavalry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_CAVALRY, ":cavalry"),
				(try_end),
				# infantry
				(try_begin),
					(ge, ":infantry", 1),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_slave", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_slave", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_outcast", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_outcast", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_shaman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_shaman", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_asud", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_asud", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_clansman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_clansman", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_noker", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_noker", ":lord_no", ":infantry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_INFANTRY, ":infantry"),
				(try_end),
				# archers
				(try_begin),
					(ge, ":archers", 1),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_surcin", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_surcin", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_kharvaach", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_kharvaach", ":lord_no", ":archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_ARCHERS, ":archers"),
				(try_end),
				# horse archers
				(try_begin),
					(ge, ":horse_archers", 1),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_scout", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_scout", ":lord_no", ":horse_archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_abaci", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_abaci", ":lord_no", ":horse_archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_orlok", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_orlok", ":lord_no", ":horse_archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_skirmisher", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_skirmisher", ":lord_no", ":horse_archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_parthian", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_parthian", ":lord_no", ":horse_archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_bahatur", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_bahatur", ":lord_no", ":horse_archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_HORSE_ARCHERS, ":horse_archers"),
				(try_end),
				
			(else_try),
				### NORDS ###
				(eq, ":faction_no", "fac_kingdom_4"),
				# Cavalry
				(try_begin),
					(ge, ":cavalry", 1),
					(try_begin), ## UNIQUE - C6
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_valkyrie", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_valkyrie", ":lord_no", ":cavalry"),
					(else_try), ## UNIQUE - C5
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_thane", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_thane", ":lord_no", ":cavalry"),
					(else_try), ## UNIQUE - C3
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_jelbegi_lancer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_jelbegi_lancer", ":lord_no", ":cavalry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_CAVALRY, ":cavalry"),
				(try_end),
				# infantry
				(try_begin),
					(ge, ":infantry", 1),
					(try_begin), ## AFFILIATED - T7
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_huscarl", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_huscarl", ":lord_no", ":infantry"),
					(else_try), ## AFFILIATED - T6
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_godi", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_godi", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_hirdmadr", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_hirdmadr", ":lord_no", ":infantry"),
					(else_try), ## AFFILIATED - T5
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_berserker", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_berserker", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_spearman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_spearman", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_retainer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_retainer", ":lord_no", ":infantry"),
					(else_try), ## AFFILIATED - T3
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_skald", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_skald", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_shield_maiden", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_shield_maiden", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_peasant", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_peasant", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_bondsman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_bondsman", ":lord_no", ":infantry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_INFANTRY, ":infantry"),
				(try_end),
				# archers
				(try_begin),
					(ge, ":archers", 1),
					(try_begin), ## AFFILIATED - T4
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_scout", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_scout", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_skirmisher", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_skirmisher", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_retinue_archer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_retinue_archer", ":lord_no", ":archers"),
					(else_try), ## UNIQUE - A2
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_maiden", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_maiden", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_hunter", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_hunter", ":lord_no", ":archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_ARCHERS, ":archers"),
				(try_end),
				# horse archers
				(try_begin),
					(ge, ":horse_archers", 1),
					# (try_begin),
						# (call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_", ":lord_no"),
						# (call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_", ":lord_no", ":horse_archers"),
					# (try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_HORSE_ARCHERS, ":horse_archers"),
				(try_end),
				
			(else_try),
				### RHODOKS ###
				(eq, ":faction_no", "fac_kingdom_5"),
				# Cavalry
				(try_begin),
					(ge, ":cavalry", 1),
					(try_begin), ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_ergellon_lancer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_ergellon_lancer", ":lord_no", ":cavalry"),
					(else_try), ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_ranger", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_ranger", ":lord_no", ":cavalry"),
					(else_try), ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_jamiche_border_guard", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_jamiche_border_guard", ":lord_no", ":cavalry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_CAVALRY, ":cavalry"),
				(try_end),
				# infantry
				(try_begin),
					(ge, ":infantry", 1),
					(try_begin), ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_highland_pikeman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_highland_pikeman", ":lord_no", ":infantry"),
					(else_try), ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_hedge_knight", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_hedge_knight", ":lord_no", ":infantry"),
					(else_try), ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_vanguard", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_vanguard", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_pikeman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_pikeman", ":lord_no", ":infantry"),
					(else_try), ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_grunwalder_voulgiers", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_grunwalder_voulgiers", ":lord_no", ":infantry"),
					(else_try), ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_veluca_pikeman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_veluca_pikeman", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_trained_militia", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_trained_militia", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_militia", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_militia", ":lord_no", ":infantry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_INFANTRY, ":infantry"),
				(try_end),
				# archers
				(try_begin),
					(ge, ":archers", 1),
					(try_begin), ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_siege_breaker", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_siege_breaker", ":lord_no", ":archers"),
					(else_try), ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_jelkalen_balister", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_jelkalen_balister", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_arbalestier", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_arbalestier", ":lord_no", ":archers"),
					(else_try), ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_yaleni_dyoken", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_yaleni_dyoken", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_crossbowman", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_crossbowman", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_militia_archer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_militia_archer", ":lord_no", ":archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_ARCHERS, ":archers"),
				(try_end),
				# horse archers
				(try_begin),
					(ge, ":horse_archers", 1),
					# (try_begin),
						# (call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_", ":lord_no"),
						# (call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_", ":lord_no", ":horse_archers"),
					# (try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_HORSE_ARCHERS, ":horse_archers"),
				(try_end),
				
			(else_try),
				### SARRANID ###
				(eq, ":faction_no", "fac_kingdom_6"),
				# Cavalry
				(try_begin),
					(ge, ":cavalry", 1),
					(try_begin), ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_sipahi", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_sipahi", ":lord_no", ":cavalry"),
					(else_try),  ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_boluk_bashi", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_boluk_bashi", ":lord_no", ":cavalry"),
					(else_try),  ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_bariyye_raider", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_bariyye_raider", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_timariot", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_timariot", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_musellem", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_musellem", ":lord_no", ":cavalry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_CAVALRY, ":cavalry"),
				(try_end),
				# infantry
				(try_begin),
					(ge, ":infantry", 1),
					(try_begin), ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sultan_guard", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sultan_guard", ":lord_no", ":infantry"),
					(else_try),  ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_bashibozuk", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_bashibozuk", ":lord_no", ":infantry"),
					(else_try),  ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_durquba_javelineer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_durquba_javelineer", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_yaya", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_yaya", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_kul", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_kul", ":lord_no", ":infantry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_INFANTRY, ":infantry"),
				(try_end),
				# archers
				(try_begin),
					(ge, ":archers", 1),
					(try_begin), ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_corbaci", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_corbaci", ":lord_no", ":archers"),
					(else_try),  ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_shariz_siegemaster_xbow", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_shariz_siegemaster_xbow", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_janissary", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_janissary", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_azab", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_azab", ":lord_no", ":archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_ARCHERS, ":archers"),
				(try_end),
				# horse archers
				(try_begin),
					(ge, ":horse_archers", 1),
					(try_begin), ## AFFILIATED
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sarranid_garip", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sarranid_garip", ":lord_no", ":horse_archers"),
					(else_try),  ## UNIQUE
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_mamluke_mounted_archer", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_mamluke_mounted_archer", ":lord_no", ":horse_archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_HORSE_ARCHERS, ":horse_archers"),
				(try_end),
				
			(else_try),
				### PLAYER FACTION ###
				(eq, ":faction_no", "fac_player_supporters_faction"),
				# Cavalry
				(try_begin),
					(ge, ":cavalry", 1),
					(call_script, "script_hub_ai_lord_considers_uniques", ":lord_no", ":center_no", AI_RECRUIT_CAVALRY, ":cavalry"),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_5_mounted", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_5_mounted", ":lord_no", ":cavalry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_4_mounted", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_4_mounted", ":lord_no", ":cavalry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_CAVALRY, ":cavalry"),
				(try_end),
				# infantry
				(try_begin),
					(ge, ":infantry", 1),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_5_infantry", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_5_infantry", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_4_infantry", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_4_infantry", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_3_infantry", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_3_infantry", ":lord_no", ":infantry"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_2", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_2", ":lord_no", ":infantry"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_INFANTRY, ":infantry"),
				(try_end),
				# archers
				(try_begin),
					(ge, ":archers", 1),
					(try_begin),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_5_ranged", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_5_ranged", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_4_ranged", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_4_ranged", ":lord_no", ":archers"),
					(else_try),
						(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_player_tier_3_ranged", ":lord_no"),
						(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_player_tier_3_ranged", ":lord_no", ":archers"),
					(try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_ARCHERS, ":archers"),
				(try_end),
				# horse archers
				(try_begin),
					(ge, ":horse_archers", 1),
					# (try_begin),
						# (call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_", ":lord_no"),
						# (call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_", ":lord_no", ":horse_archers"),
					# (try_end),
					(call_script, "script_hub_ai_lord_considers_mercenaries", ":lord_no", ":center_no", AI_RECRUIT_HORSE_ARCHERS, ":horse_archers"),
				(try_end),
				
			(try_end),
		(try_end),
		
	]),
	
# script_hub_ai_lord_determines_needed_troop_type
# PURPOSE: Filters out any conditions that would prevent a troop from showing up in a recruitment list.
("hub_ai_lord_determines_needed_troop_type",
    [
		(store_script_param, ":troop_no", 1),
		
		(store_troop_faction, ":faction_no", ":troop_no"),
			
		(try_begin),
			(eq, ":faction_no", "fac_player_supporters_faction"), # Player Custom Faction
			(assign, ":infantry",     35),
			(assign, ":archers",      30),
			(assign, ":horse_archers", 0),
			(assign, ":cavalry",      35),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_1"), # Swadia
			(assign, ":infantry",     35),
			(assign, ":archers",      30),
			(assign, ":horse_archers", 0),
			(assign, ":cavalry",      35),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_2"), # Vaegirs
			(assign, ":infantry",     35),
			(assign, ":archers",      40),
			(assign, ":horse_archers", 0),
			(assign, ":cavalry",      25),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_3"), # Khergits
			(assign, ":infantry",      0),
			(assign, ":archers",       0),
			(assign, ":horse_archers",60),
			(assign, ":cavalry",      40),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_4"), # Nords
			(assign, ":infantry",     65),
			(assign, ":archers",      35),
			(assign, ":horse_archers", 0),
			(assign, ":cavalry",       0),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_5"), # Rhodoks
			(assign, ":infantry",     50),
			(assign, ":archers",      50),
			(assign, ":horse_archers", 0),
			(assign, ":cavalry",       0),
		(else_try),
			(eq, ":faction_no", "fac_kingdom_6"), # Sarranid
			(assign, ":infantry",     25),
			(assign, ":archers",      25),
			(assign, ":horse_archers",20),
			(assign, ":cavalry",      30),
		(try_end),
		
		(try_begin),
			# Get current capacity for this lord's party.
			(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
			(party_get_free_companions_capacity, ":capacity", ":party_no"),
			# Is this party active?
			(party_is_active, ":party_no"),
			# Count how many of each troop type we have.
			(assign, ":count_infantry",      0),
			(assign, ":count_archers",       0),
			(assign, ":count_horse_archers", 0),
			(assign, ":count_cavalry",       0),
			(party_get_num_companion_stacks, ":stack_capacity", ":party_no"),
			(try_for_range, ":stack_no", 0, ":stack_capacity"),
				(party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no"),
				(party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
				(neg|troop_is_hero, ":stack_troop"),
				(try_begin),
					(troop_is_guarantee_ranged, ":stack_troop"),
					(this_or_next|troop_is_mounted, ":stack_troop"),
					(troop_is_guarantee_horse, ":stack_troop"),
					(val_add, ":count_horse_archers", ":stack_size"),
				(else_try),
					(this_or_next|troop_is_mounted, ":stack_troop"),
					(troop_is_guarantee_horse, ":stack_troop"),
					(val_add, ":count_cavalry", ":stack_size"),
				(else_try),
					(troop_is_guarantee_ranged, ":stack_troop"),
					(val_add, ":count_archers", ":stack_size"),
				(else_try),
					(val_add, ":count_infantry", ":stack_size"),
				(try_end),
			(try_end),
			# Determine individual troop type demand (raw).  I want 40%, but only found 20%...so now I want 20%
			(store_sub, ":demand_infantry", ":infantry", ":count_infantry"),
			(store_sub, ":demand_archers", ":archers", ":count_archers"),
			(store_sub, ":demand_cavalry", ":cavalry", ":count_cavalry"),
			(store_sub, ":demand_horse_archers", ":horse_archers", ":count_horse_archers"),
			# Determine total demand.  I wanted 20%, 5%, 17% & 13% so now that 55% is my new 100%.
			(store_add, ":total_demand", ":demand_infantry", ":demand_archers"),
			(val_add, ":total_demand", ":demand_cavalry"),
			(val_add, ":total_demand", ":demand_horse_archers"),
			# Renormalize our demand to match our new 100% value.  So now my 20% want has become 36% of my total demand.
			(store_mul, ":rating_infantry", ":total_demand", ":demand_infantry"),
			(val_div, ":rating_infantry", 100),
			(store_mul, ":rating_archers", ":total_demand", ":demand_archers"),
			(val_div, ":rating_archers", 100),
			(store_mul, ":rating_cavalry", ":total_demand", ":demand_cavalry"),
			(val_div, ":rating_cavalry", 100),
			(store_mul, ":rating_horse_archers", ":total_demand", ":demand_horse_archers"),
			(val_div, ":rating_horse_archers", 100),
			# Create our actual demanded number of recruits vs. capacity available.
			(store_mul, ":seek_infantry", ":capacity", ":rating_infantry"),
			(val_div, ":seek_infantry", 100),
			(store_mul, ":seek_archers", ":capacity", ":rating_archers"),
			(val_div, ":seek_archers", 100),
			(store_mul, ":seek_cavalry", ":capacity", ":rating_cavalry"),
			(val_div, ":seek_cavalry", 100),
			(store_mul, ":seek_horse_archers", ":capacity", ":rating_horse_archers"),
			(val_div, ":seek_horse_archers", 100),
			# Output our new desired recruits.
			(assign, reg1, ":seek_infantry"),
			(assign, reg2, ":seek_archers"),
			(assign, reg3, ":seek_cavalry"),
			(assign, reg4, ":seek_horse_archers"),
		(else_try),
			(assign, reg1, 0),
			(assign, reg2, 0),
			(assign, reg3, 0),
			(assign, reg4, 0),
		(try_end),
	]),
	
# script_cf_hub_ai_lord_wants_to_purchase_troop
# PURPOSE: Filters out any conditions that would prevent a troop from showing up in a recruitment list.
("cf_hub_ai_lord_wants_to_purchase_troop",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_no", 2),
		(store_script_param, ":lord_no", 3),
		(store_script_param, ":desired_amount", 4),
		
		# Make sure there are recruits of the appropriate type since we didn't check before.
		(call_script, "script_hub_get_troop_recruit_type_for_buyer", ":troop_no", ":lord_no"), # Returns type slot to reg1
		(assign, ":recruit_slot", reg1),
		(party_slot_ge, ":center_no", ":recruit_slot", 1),
		
		# Get current capacity for this lord's party.
		(troop_get_slot, ":party_no", ":lord_no", slot_troop_leaded_party),
		(party_get_free_companions_capacity, ":capacity", ":party_no"),
		(ge, ":capacity", 1),
		# Is this party active?
		(party_is_active, ":party_no"),
		
		# Limit recruits by capacity.
		(party_get_slot, ":recruits", ":center_no", ":recruit_slot"),
		(val_min, ":desired_amount", ":capacity"),
		(val_min, ":desired_amount", ":recruits"),
		# Determine if the lord can afford this many troops.
		(troop_get_slot, ":troop_cost", ":troop_no", slot_troop_purchase_cost),
		(val_div, ":troop_cost", 2), # CHEAT - allowing the AI to buy troops at 50%
		# Determine if enough mounts are available if needed.
		(try_begin),
			(this_or_next|troop_is_mounted, ":troop_no"),
			(troop_is_guarantee_horse, ":troop_no"),
			(party_get_slot, ":available_mounts", "$current_town", slot_center_horse_pool_npc),
			(val_min, ":desired_amount", ":available_mounts"),
		(try_end),
		
		# Modify cost by use of the trainer skill.
		(store_skill_level, ":skill_training", "skl_trainer", ":lord_no"),
		(val_mul, ":skill_training", 2),
		(store_mul, ":discount", ":troop_cost", ":skill_training"),
		(val_div, ":discount", 100),
		(val_sub, ":troop_cost", ":discount"),
		# Limit by Lord's wealth.
		(troop_get_slot, ":wealth", ":lord_no", slot_troop_wealth),
		(store_mul, ":limited_wealth", ":wealth", 20), # Prevent the lord from spending more than 20% of his cash in this one purchase.
		(val_div, ":limited_wealth", 100),
		(assign, ":reject", 0),
		(try_begin),
			(lt, ":wealth", 10000),
			(ge, ":troop_cost", 500),
			(assign, ":reject", 1),
		(else_try),
			(lt, ":wealth", 7000),
			(ge, ":troop_cost", 250),
			(assign, ":reject", 1),
		(else_try),
			(lt, ":wealth", 5000),
			(ge, ":troop_cost", 100),
			(assign, ":reject", 1),
		(try_end),
		(eq, ":reject", 0),
		(val_max, ":troop_cost", 1), # Prevent DIV/0 errors.
		(store_div, ":wealth_limit", ":limited_wealth", ":troop_cost"),
		(val_min, ":desired_amount", ":wealth_limit"),
		(ge, ":desired_amount", 1),
		# Setup our total price.
		(store_mul, ":multiplied_cost", ":desired_amount", ":troop_cost"),
		# Purchase our new troops.
		(val_sub, ":wealth", ":multiplied_cost"),
		(troop_set_slot, ":lord_no", slot_troop_wealth, ":wealth"),
		# Add the new troops to the party.
		(party_add_members, ":party_no", ":troop_no", ":desired_amount"),
		# Remove these recruits from the pool.
		(assign, reg37, ":recruits"), ### DIAGNOSTIC ### Below
		(val_sub, ":recruits", ":desired_amount"),
		(party_set_slot, ":center_no", ":recruit_slot", ":recruits"),
		
		### DIAGNOSTIC ###
		# (try_begin),
			# (store_troop_faction, ":faction_no", ":lord_no"),
			# (eq, ":faction_no", "fac_kingdom_1"), # Just show Swadia.
			# (str_store_troop_name, s31, ":lord_no"),
			# (str_store_troop_name_plural, s32, ":troop_no"),
			# (str_store_party_name, s33, ":center_no"),
			# (assign, reg31, ":desired_amount"),
			# (assign, reg32, ":limited_wealth"),
			# (assign, reg33, ":recruits"),
			# (assign, reg34, ":capacity"),
			# (assign, reg35, ":multiplied_cost"),
			# (troop_get_slot, reg38, ":troop_no", slot_troop_tier),
			# (display_message, "@DEBUG (AI): {s31} buys {reg31} {s32} in {s33} for {reg35} [T{reg38}].", gpu_debug),
			# (display_message, "@DEBUG (AI): ...Limits: wealth ({reg32}), avail ({reg37}), cap ({reg34}).", gpu_debug),
			# (display_message, "@DEBUG (AI): ...{s33} now has {reg33} recruits left.", gpu_debug),
		# (try_end),
	]),
	
# script_hub_ai_lord_considers_mercenaries
# PURPOSE: Generic mercenary checklist for the lords to consider when recruiting new troops.
# EXAMPLE: (call_script, "script_hub_ai_lord_considers_mercenaries", ":troop_no", ":center_no", AI_RECRUIT_CAVALRY, ":quantity"),
("hub_ai_lord_considers_mercenaries",
    [
		(store_script_param, ":lord_no", 1),
		(store_script_param, ":center_no", 2),
		(store_script_param, ":type", 3),
		(store_script_param, ":quantity", 4),
		
		# AI_RECRUIT_CAVALRY
		# AI_RECRUIT_INFANTRY
		# AI_RECRUIT_ARCHERS
		# AI_RECRUIT_HORSE_ARCHERS
		(try_begin),
			### MERCENARIES ###
			# CAVALRY
			(try_begin),
				(eq, ":type", AI_RECRUIT_CAVALRY),
				(ge, ":quantity", 1),
				(try_begin), ## AFFILIATED - RHODOK
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_ranger", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_ranger", ":lord_no", ":quantity"),
				(else_try),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_mercenary_cavalry", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_mercenary_cavalry", ":lord_no", ":quantity"),
				(else_try),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_mercenary_horseman", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_mercenary_horseman", ":lord_no", ":quantity"),
				(else_try),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_caravan_guard", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_caravan_guard", ":lord_no", ":quantity"),
				(try_end),
			(try_end),
			
			# INFANTRY
			(try_begin),
				(eq, ":type", AI_RECRUIT_INFANTRY),
				(ge, ":quantity", 1),
				(try_begin), ## NON-AFFILIATED - NORDS
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_varangian_guard", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_varangian_guard", ":lord_no", ":quantity"),
				(else_try),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_hired_blade", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_hired_blade", ":lord_no", ":quantity"),
				(else_try),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_mercenary_swordsman", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_mercenary_swordsman", ":lord_no", ":quantity"),
				(else_try), ## NON-AFFILIATED - SWADIA (Primarily an archer, but has strong melee traits and decent armor)
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_mercenary", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_mercenary", ":lord_no", ":quantity"),
				(else_try), ## NON-AFFILIATED - NORDS
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_jomsviking", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_jomsviking", ":lord_no", ":quantity"),
				(else_try), ## NON-AFFILIATED / BANDIT - NORDS
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_raider", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_raider", ":lord_no", ":quantity"),
				(else_try),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_watchman", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_watchman", ":lord_no", ":quantity"),
				(try_end),
			(try_end),
			
			# ARCHERS
			(try_begin),
				(eq, ":type", AI_RECRUIT_ARCHERS),
				(ge, ":quantity", 1),
				(try_begin), ## NON-AFFILIATED - SWADIA
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_swadian_mercenary", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_swadian_mercenary", ":lord_no", ":quantity"),
				(else_try), ## NON-AFFILIATED - NORDS
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_varangian_archer", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_varangian_archer", ":lord_no", ":quantity"),
				(else_try),
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_mercenary_crossbowman", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_mercenary_crossbowman", ":lord_no", ":quantity"),
				(try_end),
			(try_end),
			
			# HORSE ARCHERS
			(try_begin),
				(eq, ":type", AI_RECRUIT_HORSE_ARCHERS),
				(ge, ":quantity", 1),
				(try_begin), ## AFFILIATED - RHODOK
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_rhodok_ranger", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_rhodok_ranger", ":lord_no", ":quantity"),
				(try_end),
			(try_end),

		(try_end),
		
	]),
	
# script_hub_ai_lord_considers_uniques
# PURPOSE: Generic unique checklist for the lords to consider when recruiting new troops.
# EXAMPLE: (call_script, "script_hub_ai_lord_considers_uniques", ":troop_no", ":center_no", AI_RECRUIT_CAVALRY, ":quantity"),
("hub_ai_lord_considers_uniques",
    [
		(store_script_param, ":lord_no", 1),
		(store_script_param, ":center_no", 2),
		(store_script_param, ":type", 3),
		(store_script_param, ":quantity", 4),
		
		# AI_RECRUIT_CAVALRY
		# AI_RECRUIT_INFANTRY
		# AI_RECRUIT_ARCHERS
		# AI_RECRUIT_HORSE_ARCHERS
		(try_begin),
			### MERCENARIES ###
			# CAVALRY
			(try_begin),
				(eq, ":type", AI_RECRUIT_CAVALRY),
				(ge, ":quantity", 1),
				(try_begin), # SWADIA - C7
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_praven_knight", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_praven_knight", ":lord_no", ":quantity"),
				(else_try),  # KHERGIT - C7
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_keshig", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_keshig", ":lord_no", ":quantity"),
				(else_try),  # NORD - C6
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_valkyrie", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_valkyrie", ":lord_no", ":quantity"),
				(else_try),  # SWADIA - C5
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_dhirim_captain", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_dhirim_captain", ":lord_no", ":quantity"),
				(else_try),  # VAEGIR - C5
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_boyars_druzhina", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_boyars_druzhina", ":lord_no", ":quantity"),
				(else_try),  # VAEGIR - C5
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_cataphract", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_cataphract", ":lord_no", ":quantity"),
				(else_try),  # NORD - C5
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_thane", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_thane", ":lord_no", ":quantity"),
				(else_try),  # KHERGIT - C4
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_narcarra", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_narcarra", ":lord_no", ":quantity"),
				(else_try),  # SARRANID - C4
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_bariyye_raider", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_bariyye_raider", ":lord_no", ":quantity"),
				(else_try),  # SWADIA - C3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_uxkhal_bandit", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_uxkhal_bandit", ":lord_no", ":quantity"),
				(else_try),  # VAEGIR - C3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_scout", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_scout", ":lord_no", ":quantity"),
				(else_try),  # RHODOK - C3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_ergellon_lancer", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_ergellon_lancer", ":lord_no", ":quantity"),
				(else_try),  # NORD - C3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_jelbegi_lancer", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_jelbegi_lancer", ":lord_no", ":quantity"),
				(else_try),  # RHODOK - H3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_jamiche_border_guard", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_jamiche_border_guard", ":lord_no", ":quantity"),
				(try_end),
			(try_end),
			
			# INFANTRY
			(try_begin),
				(eq, ":type", AI_RECRUIT_INFANTRY),
				(ge, ":quantity", 1),
				(try_begin), # SARRANID - I7
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_sultan_guard", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_sultan_guard", ":lord_no", ":quantity"),
				(else_try),  # RHODOK - I6
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_veluca_pikeman", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_veluca_pikeman", ":lord_no", ":quantity"),
				(else_try),  # KHERGIT - I6
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_noker", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_noker", ":lord_no", ":quantity"),
				(else_try),  # RHODOK - I4
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_grunwalder_voulgiers", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_grunwalder_voulgiers", ":lord_no", ":quantity"),
				(else_try),  # SARRANID - I4
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_durquba_javelineer", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_durquba_javelineer", ":lord_no", ":quantity"),
				(else_try),  # VAEGIR - I4
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_vaegir_varagian", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_vaegir_varagian", ":lord_no", ":quantity"),
				(else_try),  # VAEGIR - I3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_curaw_guardsman", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_curaw_guardsman", ":lord_no", ":quantity"),
				(else_try),  # NORD - I3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_nord_maiden", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_nord_maiden", ":lord_no", ":quantity"),
				(else_try),  # RHODOK - I3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_yaleni_dyoken", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_yaleni_dyoken", ":lord_no", ":quantity"),
				(try_end),
			(try_end),
			
			# ARCHERS
			(try_begin),
				(eq, ":type", AI_RECRUIT_ARCHERS),
				(ge, ":quantity", 1),
				(try_begin), # SWADIA - A6
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_suno_master_archer", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_suno_master_archer", ":lord_no", ":quantity"),
				(else_try),  # RHODOK - A5
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_jelkalen_balister", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_jelkalen_balister", ":lord_no", ":quantity"),
				(else_try),  # SWADIA - A5
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_tilbaut_archer", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_tilbaut_archer", ":lord_no", ":quantity"),
				(else_try),  # SARRANID - A4
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_shariz_siegemaster_xbow", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_shariz_siegemaster_xbow", ":lord_no", ":quantity"),
				(try_end),
			(try_end),
			
			# HORSE ARCHERS
			(try_begin),
				(eq, ":type", AI_RECRUIT_HORSE_ARCHERS),
				(ge, ":quantity", 1),
				(try_begin), # KHERGIT - H4
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_khergit_orlok", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_khergit_orlok", ":lord_no", ":quantity"),
				(else_try),  # SARRANID - H4
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_r_mamluke_mounted_archer", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_r_mamluke_mounted_archer", ":lord_no", ":quantity"),
				(else_try),  # RHODOK - H3
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_jamiche_border_guard", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_jamiche_border_guard", ":lord_no", ":quantity"),
				(else_try),  # VAEGIR - H2
					(call_script, "script_cf_hub_troop_can_be_recruited_here", ":center_no", "trp_khudan_mounted_archer", ":lord_no"),
					(call_script, "script_cf_hub_ai_lord_wants_to_purchase_troop", ":center_no", "trp_khudan_mounted_archer", ":lord_no", ":quantity"),
				(try_end),
			(try_end),

		(try_end),
	]),
# script_hub_get_purchase_price_for_troop
# PURPOSE: Filters out any conditions that would prevent a troop from showing up in a recruitment list.
# EXAMPLE: (call_script, "script_hub_get_purchase_price_for_troop", ":center_no", ":troop_no", ":buyer_troop"), # Returns reg1 (price), reg2 (discount)
("hub_get_purchase_price_for_troop",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_no", 2),
		(store_script_param, ":buyer_troop", 3),
		
		# Get the base price.
		(try_begin),
			(troop_slot_ge, ":troop_no", slot_troop_purchase_cost, 1),
			(troop_get_slot, ":cost", ":troop_no", slot_troop_purchase_cost),
		(else_try),
			# This troop must have lost its value somehow.  Re-initialize it.
			(call_script, "script_hub_determine_purchase_cost", ":troop_no"),
			(troop_get_slot, ":cost", ":troop_no", slot_troop_purchase_cost),
		(try_end),
		
		(assign, ":factor", 0),
		
		# Modify cost by use of the trainer skill.
		(store_skill_level, ":skill_training", "skl_trainer", ":buyer_troop"),
		(val_mul, ":skill_training", 2),
		(val_add, ":factor", ":skill_training"),
		# Metrics Data - Track how much trainer helped this troop's cost.
		(store_mul, ":trainer_discount", ":cost", ":skill_training"),
		(val_div, ":trainer_discount", 100),
		(troop_set_slot, METRICS_DATA, metrics_trainer_troop_saving, ":trainer_discount"),
		
		# Does this center have an Armoury?
		(try_begin),
			(party_slot_ge, ":center_no", slot_center_has_armoury, cis_built),
			(val_add, ":factor", 3),
		(try_end),
		
		# Does this center have a Training Ground and Captain of the Guard?
		(try_begin),
			(party_slot_ge, ":center_no", slot_center_has_training_grounds, cis_built),
			(assign, ":bonus", 3),
			(try_begin),
				(party_get_slot, ":captain", ":center_no", slot_center_advisor_war),
				(is_between, ":captain", companions_begin, companions_end),
				(store_skill_level, ":skill_training", "skl_trainer", ":captain"),
				(val_max, ":bonus", ":skill_training"),
			(try_end),
			(val_add, ":factor", ":bonus"),
		(try_end),
		
		## SILVERSTAG EMBLEMS+ ##
		(store_current_hours, ":hours"),
		(try_begin),
			(party_slot_ge, "$current_town", slot_center_training_cost_reduce_duration, ":hours"),
			(val_add, ":factor", 25),
		(else_try),
			(party_slot_ge, "$current_town", slot_center_training_cost_reduce_duration, 1),
			(str_store_party_name, s21, "$current_town"),
			(display_message, "@The reduced cost for training troops in {s21} has expired.", gpu_debug),
			(party_set_slot, "$current_town", slot_center_training_cost_reduce_duration, 0),
		(try_end),
		## SILVERSTAG EMBLEMS- ##
		
		## CAPTAIN OF THE GUARD: BONUS_ADMINISTRATOR
		## TROOP EFFECT: Reduces the cost of training troops at this center by 1% per point of Training.
		(try_begin),
			(is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(party_get_slot, ":advisor_no", ":center_no", slot_center_advisor_war),
			(is_between, ":advisor_no", companions_begin, companions_end),
			(call_script, "script_cf_ce_troop_has_ability", ":advisor_no", BONUS_ADMINISTRATOR), # combat_scripts.py - ability constants in combat_constants.py
			(store_skill_level, ":training_bonus", "skl_trainer", ":advisor_no"),
			(val_add, ":factor", ":training_bonus"),
		(try_end),
		
		# Does this center have a stables for mounted troops?
		(try_begin),
			(party_slot_ge, ":center_no", slot_center_has_stables, cis_built),
			(party_slot_eq, ":center_no", slot_town_lord, ":buyer_troop"),
			(this_or_next|troop_is_mounted, ":troop_no"),
			(troop_is_guarantee_horse, ":troop_no"),
			(val_add, ":factor", 25),
		(try_end),
		
		# Factor in all discounts.
		(store_mul, ":discount", ":cost", ":factor"),
		(val_div, ":discount", 100),
		(val_sub, ":cost", ":discount"),
		
		# Is this a lord?
		(try_begin),
			(neq, ":buyer_troop", "trp_player"),
			(val_div, ":cost", 2),
		(try_end),
		
		(assign, reg1, ":cost"),
		(assign, reg2, ":factor"),
	]),
	
#script_hub_update_center_stock_of_mounts
("hub_update_center_stock_of_mounts",
	[
		(store_script_param, ":party_type", 1),
		
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_party_type, ":party_type"),
			
			## DETERMINE LIMIT & REGENERATION RATE FOR THIS LOCATION
			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(assign, ":raw_capacity", 30),
				(assign, ":raw_growth", 6),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(assign, ":raw_capacity", 8),
				(assign, ":raw_growth", 1),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
				(assign, ":raw_capacity", 15),
				(assign, ":raw_growth", 3),
			(try_end),
			(assign, ":stable_capacity", ":raw_capacity"),
			(assign, ":stable_growth", ":raw_growth"),
			
			## IMPROVEMENT [ Stables ] increases capacity in a center for housing available mounts and their production.
			(try_begin),
				(party_slot_ge, ":center_no", slot_center_has_stables, cis_built),
				# Increase capacity by 50%.
				(store_div, ":stable_bonus", ":raw_capacity", 2),
				(val_add, ":stable_capacity", ":stable_bonus"),
				# Increase production by 20%.
				(store_div, ":stable_bonus", ":raw_growth", 5),
				(val_add, ":stable_growth", ":stable_bonus"),
			(try_end),
			
			## IMPROVEMENT [ Horse Ranch ] increases production of available mounts.
			(try_begin),
				(party_slot_ge, ":center_no", slot_center_has_horse_ranch, cis_built),
				# Increase production by 50% here.  The other 50% bonus goes towards the bound center.
				(store_div, ":ranch_bonus", ":raw_growth", 2),
				(val_add, ":stable_growth", ":ranch_bonus"),
			(try_end),
			
			## FACTION BONUSES (Khergits) increases production of available mounts by 100% and housing by 50%.
			(try_begin),
				(store_faction_of_party, ":faction_no", ":center_no"),
				(eq, ":faction_no", "fac_kingdom_3"), # Khergits
				# Increase production by 100% here.
				(val_add, ":stable_growth", ":raw_growth"),
				# Increase capacity by 50%.
				(store_div, ":stable_bonus", ":raw_capacity", 2),
				(val_add, ":stable_capacity", ":stable_bonus"),
			(try_end),
			
			## PRODUCE NEW MOUNTS (player)
			(party_get_slot, ":available_mounts", ":center_no", slot_center_horse_pool_player),
			(val_add, ":available_mounts", ":stable_growth"),
			(try_begin),
				(party_slot_ge, ":center_no", slot_center_horse_pool_imported, 1),
				(party_get_slot, ":imported_mounts", ":center_no", slot_center_horse_pool_imported),
				(val_add, ":available_mounts", ":imported_mounts"),
			(try_end),
			(val_min, ":available_mounts", ":stable_capacity"),
			(party_set_slot, ":center_no", slot_center_horse_pool_player, ":available_mounts"),
			
			## PRODUCE NEW MOUNTS (AI)
			(store_mul, ":ai_capacity", ":stable_capacity", 5),
			(store_mul, ":ai_growth", ":stable_growth", 5),
			(party_get_slot, ":npc_mounts", ":center_no", slot_center_horse_pool_npc),
			(val_add, ":npc_mounts", ":ai_growth"),
			(try_begin),
				(party_slot_ge, ":center_no", slot_center_horse_pool_imported, 1),
				(party_get_slot, ":imported_mounts", ":center_no", slot_center_horse_pool_imported),
				(val_mul, ":imported_mounts", 5),
				(val_add, ":npc_mounts", ":imported_mounts"),
			(try_end),
			(val_min, ":npc_mounts", ":ai_capacity"),
			(party_set_slot, ":center_no", slot_center_horse_pool_npc, ":npc_mounts"),
			
			## CLEAN OUT ANY SLOTS IN NEED.
			(party_set_slot, ":center_no", slot_center_horse_pool_imported, 0),
			
			## ADD NEW MOUNTS TO BOUND CENTERS (villages)
			(party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
			(party_set_slot, ":bound_center", slot_center_horse_pool_imported, ":ranch_bonus"),
			
			## DIAGNOSTIC OUTPUT ##
			(try_begin),
				(ge, DEBUG_RECRUITMENT, 2),
				(party_get_slot, reg31, ":center_no", slot_center_has_stables),
				(val_min, reg31, 1),
				(party_get_slot, reg32, ":center_no", slot_center_has_horse_ranch),
				(val_min, reg32, 1),
				(str_store_party_name, s31, ":center_no"),
				(assign, reg33, ":stable_growth"),
				(assign, reg34, ":available_mounts"),
				(assign, reg35, ":stable_capacity"),
				(display_message, "@DEBUG (hub): {s31} gets {reg33}/{reg34} mounts ({reg35} Cap).  Stables = {reg31?Built:None}, Ranch = {reg32?Built:None}", gpu_debug),
			(try_end),
		(try_end),
	]),
	
#script_hub_initialize_original_center_names
("hub_initialize_original_center_names",
	[
		# Copy of the original center name into a slot.  This needs to be refreshed at times to preserve save breaks.
		(try_for_range, ":center_no", centers_begin, centers_end),
			(store_sub, ":center_offset", ":center_no", centers_begin),
			(store_add, ":string_no", ":center_offset", "str_hub_town_1"),
			(party_set_slot, ":center_no", slot_center_original_name, ":string_no"),
			(party_set_name, ":center_no", ":string_no"),
			### DIAGNOSTIC+ ###
			# (str_store_party_name, s21, ":center_no"),
			# (party_set_name, ":center_no", ":string_no"),
			# (str_store_party_name, s22, ":center_no"),
			# (neg|str_equals, s21, s22, 1),
			# (display_message, "@DEBUG: {s21} renamed to {s22}.", gpu_debug),
			### DIAGNOSTIC- ###
		(try_end),
	]),
	
#script_hub_rename_center_to_s22
("hub_rename_center_to_s22",
	[
		(store_script_param, ":center_no", 1),
		
		(str_store_party_name, s21, ":center_no"),
		(str_store_troop_name, s23, "trp_player"),
		(party_set_name, ":center_no", s22),
		
		## Determine if player is king of this town.
		(try_begin),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
			(assign, ":player_is_king", 1),
		(else_try),
			(assign, ":player_is_king", 0),
		(try_end),
		
		## Display name change to the player.
		(try_begin),
			(this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), # Player owns the fief.
			(eq, ":player_is_king", 1), # Player is king of the faction the center belongs to.
			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(str_store_string, s24, "@the town of {s21}"),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(str_store_string, s24, "@{s21}"),
			(else_try),
				(str_store_string, s24, "@the village of {s21}"),
			(try_end),
			(display_message, "@By order of {s23}, {s24} has been renamed to {s22}.", gpu_green),
		(try_end),
		
		## Determine if any unique troops need their names changed.
		# (try_for_range, ":troop_no", unique_troops_begin, unique_troops_end),
			# (troop_slot_eq, ":troop_no", slot_troop_unique_location, ":center_no"),
			# (call_script, "script_hub_rename_unique_troop", ":troop_no"),
		# (try_end),
		(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
			(faction_get_slot, ":start_troop", ":kingdom_no", slot_faction_troops_begin),
			(faction_get_slot, ":end_troop", ":kingdom_no", slot_faction_troops_end),
			(try_for_range, ":troop_no", ":start_troop", ":end_troop"),
				(troop_slot_eq, ":troop_no", slot_troop_unique_location, ":center_no"),
				(call_script, "script_hub_rename_unique_troop", ":troop_no"),
			(try_end), # Troop loop
		(try_end), # Kingdom loop
	]),
	
#script_hub_rename_unique_troop
("hub_rename_unique_troop",
	[
		(store_script_param, ":troop_no", 1),
		
		(troop_get_slot, ":center_no", ":troop_no", slot_troop_unique_location),
		(try_begin),
			(is_between, ":center_no", centers_begin, centers_end),
			(str_store_party_name, s21, ":center_no"),
			
			(try_begin),
				## DURQUBA JAVELINEER
				(eq, ":troop_no", "trp_r_durquba_javelineer"),
				(str_store_string, s22, "@{s21} Javelineer"),
				(str_store_string, s23, "@{s21} Javelineers"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			## v0.21 UNIQUE TROOPS BEGIN ##
			(else_try),
				## UXKHAL BANDIT
				(eq, ":troop_no", "trp_r_uxkhal_bandit"),
				(str_store_string, s22, "@{s21} Bandit"),
				(str_store_string, s23, "@{s21} Bandits"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## TILBAUT ARCHER
				(eq, ":troop_no", "trp_r_tilbaut_archer"),
				(str_store_string, s22, "@{s21} Archer"),
				(str_store_string, s23, "@{s21} Archers"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## DHIRIM CAPTAIN
				(eq, ":troop_no", "trp_r_dhirim_captain"),
				(str_store_string, s22, "@{s21} Captain"),
				(str_store_string, s23, "@{s21} Captains"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## SUNO MASTER ARCHER
				(eq, ":troop_no", "trp_r_suno_master_archer"),
				(str_store_string, s22, "@{s21} Master Archer"),
				(str_store_string, s23, "@{s21} Master Archers"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## PRAVEN KNIGHT
				(eq, ":troop_no", "trp_r_praven_knight"),
				(str_store_string, s22, "@{s21} Knight"),
				(str_store_string, s23, "@{s21} Knights"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## ERGELLON LANCER
				(eq, ":troop_no", "trp_ergellon_lancer"),
				(str_store_string, s22, "@{s21} Lancer"),
				(str_store_string, s23, "@{s21} Lancers"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## YALENI DYOKEN
				(eq, ":troop_no", "trp_yaleni_dyoken"),
				(str_store_string, s22, "@{s21} Dyoken"),
				(str_store_string, s23, "@{s21} Dyoken"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## JELKALEN BALISTER
				(eq, ":troop_no", "trp_jelkalen_balister"),
				(str_store_string, s22, "@{s21} Balister"),
				(str_store_string, s23, "@{s21} Balisters"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## JAMICHE BORDER GUARD
				(eq, ":troop_no", "trp_jamiche_border_guard"),
				(str_store_string, s22, "@{s21} Border Guard"),
				(str_store_string, s23, "@{s21} Border Guards"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## VELUCA PIKEMEN
				(eq, ":troop_no", "trp_veluca_pikeman"),
				(str_store_string, s22, "@{s21} Pikeman"),
				(str_store_string, s23, "@{s21} Pikemen"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## GRUNWALDER VOULGIERS
				(eq, ":troop_no", "trp_grunwalder_voulgiers"),
				(str_store_string, s22, "@{s21} Voulgier"),
				(str_store_string, s23, "@{s21} Voulgiers"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			## v0.21 UNIQUE TROOPS END ##
			## v0.23 UNIQUE TROOPS BEGIN ##
			(else_try),
				## CURAW GUARDSMAN
				(eq, ":troop_no", "trp_curaw_guardsman"),
				(str_store_string, s22, "@{s21} Guardsman"),
				(str_store_string, s23, "@{s21} Guardsmen"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## JEIRBE SELLSWORD
				(eq, ":troop_no", "trp_r_vaegir_varagian"),
				(str_store_string, s22, "@{s21} Sellsword"),
				(str_store_string, s23, "@{s21} Sellswords"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## HUNTSMEN OF KHUDAN
				(eq, ":troop_no", "trp_khudan_mounted_archer"),
				(str_store_string, s22, "@Huntsman of {s21}"),
				(str_store_string, s23, "@Huntsmen of {s21}"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## OUTRIDER OF NELAG
				(eq, ":troop_no", "trp_r_vaegir_scout"),
				(str_store_string, s22, "@Outrider of {s21}"),
				(str_store_string, s23, "@Outrider of {s21}"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## DRUZHINA OF REYVADIN
				(eq, ":troop_no", "trp_boyars_druzhina"),
				(str_store_string, s22, "@Druzhina of {s21}"),
				(str_store_string, s23, "@Druzhina of {s21}"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			## v0.23 UNIQUE TROOPS END ##
			## v0.24 UNIQUE TROOPS BEGIN ##
			(else_try),
				## MAIDEN OF ADELEN
				(eq, ":troop_no", "trp_r_nord_maiden"),
				(str_store_string, s22, "@Maiden of {s21}"),
				(str_store_string, s23, "@Maidens of {s21}"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## JELBEGI LANCER
				(eq, ":troop_no", "trp_r_nord_jelbegi_lancer"),
				(str_store_string, s22, "@{s21} Lancer"),
				(str_store_string, s23, "@{s21} Lancers"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## THANE OF SARGOTH
				(eq, ":troop_no", "trp_r_nord_thane"),
				(str_store_string, s22, "@Thane of {s21}"),
				(str_store_string, s23, "@Thanes of {s21}"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			(else_try),
				## VALKYRIE OF TIHR
				(eq, ":troop_no", "trp_r_nord_valkyrie"),
				(str_store_string, s22, "@Valkyrie of {s21}"),
				(str_store_string, s23, "@Valkyries of {s21}"),
				(troop_set_name, ":troop_no", s22),
				(troop_set_plural_name, ":troop_no", s23),
			## v0.24 UNIQUE TROOPS END ##
			## v0.26 UNIQUE TROOPS BEGIN ##
			## v0.26 UNIQUE TROOPS END ##
			(try_end),
			
		(else_try),
			(str_store_troop_name, s31, ":troop_no"),
			(str_store_party_name, s32, ":center_no"),
			(display_message, "@ERROR - Attempt failed to rename '{s31}' for center '{s32}'.", gpu_red),
		(try_end),
		
	]),
]


from util_wrappers import *
from util_scripts import *

                
def modmerge_scripts(orig_scripts):
	# process script directives first
	# process_script_directives(orig_scripts, scripts_directives)
	# add remaining scripts
	add_scripts(orig_scripts, scripts, True)
	
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "scripts"
        orig_scripts = var_set[var_name_1]
    
        
		# START do your own stuff to do merging
		
        modmerge_scripts(orig_scripts)

		# END do your own stuff
        
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
