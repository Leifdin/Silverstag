# Character Creation Presentation (1.0.3)
# Created by Windyplains.  Inspired by Dunde's character creation presentation in Custom Commander.

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *
from header_presentations import *  # (COMPANIONS OVERSEER MOD)
# from companions_constants import *  # (COMPANIONS OVERSEER MOD)
from header_skills import *  # Supports script_ccp_start_adventuring_raise_skills
from header_parties import * # Supports script_ccp_end_presentation_begin_game for Fog of War conditions.
from module_items import *
from ID_skills import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	 
# script_ccp_default_settings 
# Establishes the default character creation settings to use upon initializing the presentation or using the default button option.
# Input: none
# Output: none
("ccp_default_settings",
	[
		(assign, "$character_gender", tf_male),
		(assign,"$background_type",cb_noble),
		(assign,"$background_answer_2", cb2_page),
		(assign,"$background_answer_3",cb3_squire),
		(assign,"$background_answer_4", cb4_revenge),
		(assign, "$quest_reactions", QUEST_REACTIONS_HIGH),
		(troop_set_slot, ccp_objects, ccp_val_menu_questreaction, 0),
		(assign, "$g_gether_npcs", 0),
		(troop_set_slot, ccp_objects, ccp_val_checkbox_gather_npcs, 0),
		# Setup the initial default mod difficulty.
		(store_add, ":setting", "$mod_difficulty", 1),
		(troop_set_slot, ccp_objects, ccp_val_menu_mod_difficulty, ":setting"),
		# (assign, "$g_fog", 0),
		# (troop_set_slot, ccp_objects, ccp_val_checkbox_fogofwar, 0),
		# (assign, "$troop_trees", troop_trees_2),
		# (troop_set_slot, ccp_objects, ccp_val_menu_trooptrees, troop_trees_2),
	]),
	
# script_ccp_end_presentation_begin_game 
# Establishes the default character creation settings to use upon initializing the presentation or using the default button option.
# Input: none
# Output: none
("ccp_end_presentation_begin_game",
	[
		# # MTT INITIALIZATION
		# (call_script, "script_initialize_troop_tree_sets"),
		
		# # FOG OF WAR ENABLED
		# (try_begin),
			# (eq, "$g_fog", 1),
			# ##Floris Fog of War // Initialize Centers
			# (try_for_range, ":center_no", centers_begin, "p_Bridge_14"),
				# (party_set_slot, ":center_no", slot_center_explored, 0), # Bugfix.  Needs to be 0.
				# (party_set_flags,":center_no", pf_always_visible, 0),
			# (try_end),
		# (try_end),
		# (assign, "$g_date", 0),
		
		# BUILD CHARACTER STATS
		(call_script, "script_ccp_generate_skill_set", equip_the_player), # This tells the kit to generate the new stat combination AND give the actual equipment to the player vs. display the information.
			
		# gender
		(try_begin),
			(eq,"$character_gender",tf_male),
			(troop_set_type,"trp_player", 0),
		(else_try),
			(eq,"$character_gender",tf_female),
			(troop_set_type,"trp_player", 1),
		(try_end),
		
		# Clean out ccp_objects & ccp_data
		(try_for_range, ":slot", 0, 400),
			(troop_set_slot, ccp_objects, ":slot", 0),
			(troop_set_slot, ccp_data, ":slot", 0),
		(try_end),
		
		## CCP 1.1+ ## - Workaround for Warband 1.151 breaking the banner presentation at game start.
		(try_begin),
			(eq, "$background_type", cb_noble),
			(assign, "$player_needs_a_banner", 1),
		(else_try),
			(assign, "$player_needs_a_banner", 0),
		(try_end),
	]),
	
# script_ccp_add_item 
# Records item IDs based on character background choices for later equipping the character.
# Input: item_id
# Output: none
("ccp_add_item",
	[
		(store_script_param, ":item_no", 1),
		(try_begin),
			(is_between, ":item_no", "itm_tutorial_spear", "itm_items_end"),
			(assign, ":stored", 0),
		(else_try),
			(assign, ":stored", 1),
			(display_message, "@ERROR (CCP): An invalid item was detected and will not be stored."),
		(try_end),
		(try_for_range, ":slot", ccp_item_storage_begin, ccp_item_storage_end),
			(eq, ":stored", 0),
			(troop_slot_eq, ccp_data, ":slot", 0),
			(troop_set_slot, ccp_data, ":slot", ":item_no"),
			(assign, ":stored", 1),
			(ge, DEBUG_CCP_general, 2),
			(assign, reg31, ":slot"),
			(str_store_item_name, s31, ":item_no"),
			(display_message, "@DEBUG (CCP): Item '{s31}' successfully stored in slot {reg31}."),
		(try_end),
		(try_begin),
			(eq, ":stored", 0),
			(ge, DEBUG_CCP_general, 1),
			(display_message, "@DEBUG (CCP): There was no valid spot to place this item."),
		(try_end),
	]),
	
# script_ccp_remove_item 
# Removes a specified item ID from the character creation inventory data.
# Input: item_id
# Output: none
("ccp_remove_item",
	[
		(store_script_param, ":item_no", 1),
		(try_begin),
			(is_between, ":item_no", "itm_tutorial_spear", "itm_items_end"),
			(assign, ":removed", 0),
		(else_try),
			(assign, ":removed", 1),
			(display_message, "@ERROR (CCP): An invalid item was detected and will not be removed."),
		(try_end),
		(try_for_range, ":slot", ccp_item_storage_begin, ccp_item_storage_end),
			(eq, ":removed", 0),
			(troop_slot_eq, ccp_data, ":slot", ":item_no"),
			(troop_set_slot, ccp_data, ":slot", 0),
			(assign, ":removed", 1),
			(ge, DEBUG_CCP_general, 2),
			(assign, reg31, ":slot"),
			(str_store_item_name, s31, ":item_no"),
			(display_message, "@DEBUG (CCP): Item '{s31}' successfully removed from slot {reg31}."),
		(try_end),
		(try_begin),
			(eq, ":removed", 0),
			(ge, DEBUG_CCP_general, 1),
			(str_store_item_name, s31, ":item_no"),
			(display_message, "@DEBUG (CCP): The player did not have a '{s31}'."),
		(try_end),
	]),
	
# script_ccp_add_skill_display 
# Creates a new display for each skill added and keeps them in order.
# Input: none
# Output: none
("ccp_add_skill_display",
	[
		(store_script_param, ":title", 1),
		(store_script_param, ":value", 2),
		(store_script_param, ":line", 3),
		
		# Determine height to place it at.
		(assign, ":pos_y", 300), # was 230, but that was causing it to run out of scroll room if too many options were selected.
		(store_mul, ":line_adjust", ":line", 25),
		(val_sub, ":pos_y", ":line_adjust"),
		
		# Value of skill
		(assign, reg2, ":value"),
		(create_text_overlay, reg1, "@+{reg2}", tf_right_align|tf_with_outline|tf_vertical_align_center),
		(position_set_x, pos1, 120),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
		(overlay_set_color, reg1, gpu_white),
		(position_set_x, pos2, 750),
		(position_set_y, pos2, 750),
		(overlay_set_size, reg1, pos2),
		
		# Label of skill
		(create_text_overlay, reg1, ":title", tf_left_align|tf_with_outline|tf_vertical_align_center),
		(position_set_x, pos1, 110),
		(position_set_y, pos1, ":pos_y"),
		(overlay_set_position, reg1, pos1),
		(overlay_set_color, reg1, gpu_white),
		(overlay_set_size, reg1, pos2),
		
	]),
	
# script_ccp_initialize_faction_items
# Fills the array with items designed for each faction.
# Input: none
# Output: none
("ccp_initialize_faction_items",
	[
		# Define Swadia items.
		(troop_set_slot, ccp_data, ccp_swadia_item_trade1, "itm_tools"),
		(troop_set_slot, ccp_data, ccp_swadia_item_trade2, "itm_iron"),
		(troop_set_slot, ccp_data, ccp_swadia_item_horse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_swadia_item_richhorse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_swadia_item_shield, "itm_tab_shield_heater_a"),
		(troop_set_slot, ccp_data, ccp_swadia_item_instrument, "itm_lute"),
		(troop_set_slot, ccp_data, ccp_swadia_item_poorboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_swadia_item_boots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_swadia_item_richboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_swadia_item_cloth, "itm_heraldic_tabard"),
		(troop_set_slot, ccp_data, ccp_swadia_item_dress, "itm_lady_dress_green"),
		(troop_set_slot, ccp_data, ccp_swadia_item_armor, "itm_heraldic_cuir_bouilli_starter"),
		(troop_set_slot, ccp_data, ccp_swadia_item_gauntlets, "itm_leather_gloves"),         # "itm_ga_swa_a2_leather"),
		(troop_set_slot, ccp_data, ccp_swadia_item_hood, "itm_common_hood"),
		(troop_set_slot, ccp_data, ccp_swadia_item_helmet, "itm_mail_coif"),
		(troop_set_slot, ccp_data, ccp_swadia_item_ladyhelmet, "itm_leather_cap"),
		(troop_set_slot, ccp_data, ccp_swadia_item_axe, "itm_light_axe"),              # Diff 0
		(troop_set_slot, ccp_data, ccp_swadia_item_blunt, "itm_spiked_club_b"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_swadia_item_dagger, "itm_dagger"), # Diff 0
		(troop_set_slot, ccp_data, ccp_swadia_item_spear, "itm_shortened_spear"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_swadia_item_sword, "itm_western_arming_sword"),           # Diff 0
		(troop_set_slot, ccp_data, ccp_swadia_item_bow, "itm_hunting_bow"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_swadia_item_arrow, "itm_arrows"),          # Diff n/a
		(troop_set_slot, ccp_data, ccp_swadia_item_throwing, "itm_throwing_spears"),         # Diff 1, but downgrades to lesser knives if needed.
		
		# Define Vaegir items.
		(troop_set_slot, ccp_data, ccp_vaegir_item_trade1, "itm_tools"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_trade2, "itm_iron"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_horse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_richhorse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_shield, "itm_tab_shield_heater_a"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_instrument, "itm_lute"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_poorboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_boots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_richboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_cloth, "itm_heraldic_tabard"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_dress, "itm_lady_dress_green"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_armor, "itm_heraldic_cuir_bouilli_starter"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_gauntlets, "itm_leather_gloves"),         # "itm_ga_swa_a2_leather"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_hood, "itm_common_hood"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_helmet, "itm_mail_coif"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_ladyhelmet, "itm_leather_cap"),
		(troop_set_slot, ccp_data, ccp_vaegir_item_axe, "itm_light_axe"),              # Diff 0
		(troop_set_slot, ccp_data, ccp_vaegir_item_blunt, "itm_spiked_club_b"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_vaegir_item_dagger, "itm_dagger"), # Diff 0
		(troop_set_slot, ccp_data, ccp_vaegir_item_spear, "itm_shortened_spear"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_vaegir_item_sword, "itm_western_arming_sword"),           # Diff 0
		(troop_set_slot, ccp_data, ccp_vaegir_item_bow, "itm_hunting_bow"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_vaegir_item_arrow, "itm_arrows"),          # Diff n/a
		(troop_set_slot, ccp_data, ccp_vaegir_item_throwing, "itm_throwing_spears"),         # Diff 1, but downgrades to lesser knives if needed.
		
		# Define Khergit items.
		(troop_set_slot, ccp_data, ccp_khergit_item_trade1, "itm_tools"),
		(troop_set_slot, ccp_data, ccp_khergit_item_trade2, "itm_iron"),
		(troop_set_slot, ccp_data, ccp_khergit_item_horse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_khergit_item_richhorse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_khergit_item_shield, "itm_tab_shield_heater_a"),
		(troop_set_slot, ccp_data, ccp_khergit_item_instrument, "itm_lute"),
		(troop_set_slot, ccp_data, ccp_khergit_item_poorboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_khergit_item_boots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_khergit_item_richboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_khergit_item_cloth, "itm_heraldic_tabard"),
		(troop_set_slot, ccp_data, ccp_khergit_item_dress, "itm_lady_dress_green"),
		(troop_set_slot, ccp_data, ccp_khergit_item_armor, "itm_heraldic_cuir_bouilli_starter"),
		(troop_set_slot, ccp_data, ccp_khergit_item_gauntlets, "itm_leather_gloves"),         # "itm_ga_swa_a2_leather"),
		(troop_set_slot, ccp_data, ccp_khergit_item_hood, "itm_common_hood"),
		(troop_set_slot, ccp_data, ccp_khergit_item_helmet, "itm_mail_coif"),
		(troop_set_slot, ccp_data, ccp_khergit_item_ladyhelmet, "itm_leather_cap"),
		(troop_set_slot, ccp_data, ccp_khergit_item_axe, "itm_light_axe"),              # Diff 0
		(troop_set_slot, ccp_data, ccp_khergit_item_blunt, "itm_spiked_club_b"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_khergit_item_dagger, "itm_dagger"), # Diff 0
		(troop_set_slot, ccp_data, ccp_khergit_item_spear, "itm_shortened_spear"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_khergit_item_sword, "itm_western_arming_sword"),           # Diff 0
		(troop_set_slot, ccp_data, ccp_khergit_item_bow, "itm_hunting_bow"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_khergit_item_arrow, "itm_arrows"),          # Diff n/a
		(troop_set_slot, ccp_data, ccp_khergit_item_throwing, "itm_throwing_spears"),         # Diff 1, but downgrades to lesser knives if needed.
		
		# Define Nord items.
		(troop_set_slot, ccp_data, ccp_nord_item_trade1, "itm_tools"),
		(troop_set_slot, ccp_data, ccp_nord_item_trade2, "itm_iron"),
		(troop_set_slot, ccp_data, ccp_nord_item_horse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_nord_item_richhorse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_nord_item_shield, "itm_tab_shield_heater_a"),
		(troop_set_slot, ccp_data, ccp_nord_item_instrument, "itm_lute"),
		(troop_set_slot, ccp_data, ccp_nord_item_poorboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_nord_item_boots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_nord_item_richboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_nord_item_cloth, "itm_heraldic_tabard"),
		(troop_set_slot, ccp_data, ccp_nord_item_dress, "itm_lady_dress_green"),
		(troop_set_slot, ccp_data, ccp_nord_item_armor, "itm_heraldic_cuir_bouilli_starter"),
		(troop_set_slot, ccp_data, ccp_nord_item_gauntlets, "itm_leather_gloves"),         # "itm_ga_swa_a2_leather"),
		(troop_set_slot, ccp_data, ccp_nord_item_hood, "itm_common_hood"),
		(troop_set_slot, ccp_data, ccp_nord_item_helmet, "itm_mail_coif"),
		(troop_set_slot, ccp_data, ccp_nord_item_ladyhelmet, "itm_leather_cap"),
		(troop_set_slot, ccp_data, ccp_nord_item_axe, "itm_light_axe"),              # Diff 0
		(troop_set_slot, ccp_data, ccp_nord_item_blunt, "itm_spiked_club_b"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_nord_item_dagger, "itm_dagger"), # Diff 0
		(troop_set_slot, ccp_data, ccp_nord_item_spear, "itm_shortened_spear"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_nord_item_sword, "itm_western_arming_sword"),           # Diff 0
		(troop_set_slot, ccp_data, ccp_nord_item_bow, "itm_hunting_bow"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_nord_item_arrow, "itm_arrows"),          # Diff n/a
		(troop_set_slot, ccp_data, ccp_nord_item_throwing, "itm_throwing_spears"),         # Diff 1, but downgrades to lesser knives if needed.
		
		# Define Rhodok items.
		(troop_set_slot, ccp_data, ccp_rhodok_item_trade1, "itm_tools"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_trade2, "itm_iron"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_horse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_richhorse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_shield, "itm_tab_shield_heater_a"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_instrument, "itm_lute"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_poorboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_boots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_richboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_cloth, "itm_heraldic_tabard"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_dress, "itm_lady_dress_green"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_armor, "itm_heraldic_cuir_bouilli_starter"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_gauntlets, "itm_leather_gloves"),         # "itm_ga_swa_a2_leather"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_hood, "itm_common_hood"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_helmet, "itm_mail_coif"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_ladyhelmet, "itm_leather_cap"),
		(troop_set_slot, ccp_data, ccp_rhodok_item_axe, "itm_light_axe"),              # Diff 0
		(troop_set_slot, ccp_data, ccp_rhodok_item_blunt, "itm_spiked_club_b"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_rhodok_item_dagger, "itm_dagger"), # Diff 0
		(troop_set_slot, ccp_data, ccp_rhodok_item_spear, "itm_shortened_spear"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_rhodok_item_sword, "itm_western_arming_sword"),           # Diff 0
		(troop_set_slot, ccp_data, ccp_rhodok_item_bow, "itm_hunting_bow"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_rhodok_item_arrow, "itm_arrows"),          # Diff n/a
		(troop_set_slot, ccp_data, ccp_rhodok_item_throwing, "itm_throwing_spears"),         # Diff 1, but downgrades to lesser knives if needed.
		
		# Define Sarrand items.
		(troop_set_slot, ccp_data, ccp_sarrand_item_trade1, "itm_tools"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_trade2, "itm_iron"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_horse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_richhorse, "itm_saddle_horse"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_shield, "itm_tab_shield_heater_a"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_instrument, "itm_lute"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_poorboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_boots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_richboots, "itm_leather_boots"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_cloth, "itm_heraldic_tabard"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_dress, "itm_lady_dress_green"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_armor, "itm_heraldic_cuir_bouilli_starter"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_gauntlets, "itm_leather_gloves"),         # "itm_ga_swa_a2_leather"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_hood, "itm_common_hood"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_helmet, "itm_mail_coif"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_ladyhelmet, "itm_leather_cap"),
		(troop_set_slot, ccp_data, ccp_sarrand_item_axe, "itm_light_axe"),              # Diff 0
		(troop_set_slot, ccp_data, ccp_sarrand_item_blunt, "itm_spiked_club_b"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_sarrand_item_dagger, "itm_dagger"), # Diff 0
		(troop_set_slot, ccp_data, ccp_sarrand_item_spear, "itm_shortened_spear"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_sarrand_item_sword, "itm_western_arming_sword"),           # Diff 0
		(troop_set_slot, ccp_data, ccp_sarrand_item_bow, "itm_hunting_bow"),             # Diff 0
		(troop_set_slot, ccp_data, ccp_sarrand_item_arrow, "itm_arrows"),          # Diff n/a
		(troop_set_slot, ccp_data, ccp_sarrand_item_throwing, "itm_throwing_spears"),         # Diff 1, but downgrades to lesser knives if needed.
		
	]),
	
# script_ccp_get_character_background_text
# Generates the story text based on your background descisions.
# Input: none
# Output: s1 (story text)
("ccp_get_character_background_text",
	[
		(str_clear,s1),
		(assign, reg3, "$character_gender"),
		## father
		(try_begin),
			(eq, "$background_type", cb_noble),
			(str_store_string,s2,"@an impoverished noble"),
			(str_store_string,s3,"@You came into the world a {reg3?daughter:son} of declining nobility,	owning only the house in which they lived. However, despite your family's hardships, they afforded you a good education and trained you from childhood for the rigors of aristocracy and life at court."),
		(else_try),
			(eq, "$background_type", cb_merchant),
			(str_store_string,s2,"@a travelling merchant"),
			(str_store_string,s3,"@You were born the {reg3?daughter:son} of travelling merchants, always moving from place to place in search of a profit. Although your parents were wealthier than most	and educated you as well as they could, you found little opportunity to make friends on the road, living mostly for the moments when you could sell something to somebody."),
		(else_try),
			(eq, "$background_type", cb_guard),
			(str_store_string,s2,"@a veteran warrior"),
			(str_store_string,s3,"@As a child, your family scrabbled out a meagre living from your father's wages as a guardsman to the local lord. It was not an easy existence, and you were too poor to get much of an	education. You learned mainly how to defend yourself on the streets, with or without a weapon in hand."),
		(else_try),
			(eq, "$background_type", cb_forester),
			(str_store_string,s2,"@a hunter"),
			(str_store_string,s3,"@You were the {reg3?daughter:son} of a family who lived off the woods, doing whatever they needed to make ends meet. Hunting, woodcutting, making arrows, even a spot of poaching whenever things got tight. Winter was never a good time for your family	as the cold took animals and people alike, but you always lived to see another dawn, though your brothers and sisters might not be so fortunate."),
		(else_try),
			(eq, "$background_type", cb_nomad),
			(str_store_string,s2,"@a steppe nomad"),
			(str_store_string,s3,"@You were a child of the steppe, born to a tribe of wandering nomads who lived in great camps throughout the arid grasslands.  Like the other tribesmen, your family revered horses above almost everything else, and they taught you how to ride almost before you learned how to walk. "),
		(else_try),
			(eq, "$background_type", cb_thief),
			(str_store_string,s2,"@a thief"),
			(str_store_string,s3,"@As the {reg3?daughter:son} of a thief, you had very little 'formal' education.  Instead you were out on the street, begging until you learned how to cut purses, cutting purses	until you learned how to pick locks, all the way through your childhood.  Still, these long years made you streetwise and sharp to the secrets of cities and shadowy backways."),
		(else_try),
			(eq, "$background_type", cb_priest), # Diplomacy addition
			(str_store_string,s2,"@a priest"),
			(str_store_string,s3,"@A {reg3?daughter:son} that nobody wanted, you were left to the church as a baby, a foundling raised by the priests and nuns to their own traditions.  You were only one of many other foundlings and orphans, but you nonetheless received a lot of attention	as well as many years of study in the church library and before the altar. They taught you many things.  Gradually, faith became such a part of your life that it was no different from the blood coursing through your veins."),
		(try_end),
		(str_store_string,s1,"@ You were born years ago, in a land far away. Your father was {s2}. {s3}"),
	  
		## early life
		(try_begin),
			(eq, "$background_answer_2", cb2_page),
			(str_store_string,s2,"@a page at a nobleman's court"),
			(str_store_string,s3,"@As a {reg3?girl:boy} growing out of childhood, you were sent to live in the court of one of the nobles of the land.  There, your first lessons were in humility, as you waited upon the lords and ladies of the household.  But from their chess games, their gossip, even the poetry of great deeds and courtly love, you quickly began to learn about the adult world of conflict	and competition. You also learned from the rough games of the other children, who battered at each other with sticks in imitation of their elders' swords."),
		(else_try),
			(eq, "$background_answer_2", cb2_apprentice),
			(str_store_string,s2,"@a craftsman's apprentice"),
			(str_store_string,s3,"@As a {reg3?girl:boy} growing out of childhood, you apprenticed with a local craftsman to learn a trade. After years of hard work and study under your new master, he promoted you to journeyman and employed you as a fully paid craftsman for as long as you wished to stay."),
		(else_try),
			(eq, "$background_answer_2", cb2_merchants_helper),
			(str_store_string,s2,"@a shop assistant"),
			(str_store_string,s3,"@As a {reg3?girl:boy} growing out of childhood, you apprenticed to a wealthy merchant, picking up the trade over years of working shops and driving caravans.  You soon became adept at the art of buying low, selling high, and leaving the customer thinking they'd	got the better deal."),
		(else_try),
			(eq, "$background_answer_2", cb2_urchin),
			(str_store_string,s2,"@a street urchin"),
			(str_store_string,s3,"@As a {reg3?girl:boy} growing out of childhood, you took to the streets, doing whatever you must to survive. Begging, thieving and working for gangs to earn your bread, you lived from day to day in this violent world, always one step ahead of the law and those who wished you ill."),
		(else_try),
			(eq, "$background_answer_2", cb2_steppe_child),
			(str_store_string,s2,"@a steppe child"),
			(str_store_string,s3,"@As a {reg3?girl:boy} growing out of childhood, you rode the great steppes on a horse of your own, learning the ways of the grass and the desert.  Although you sometimes went hungry, you became a skillful hunter and pathfinder in your trackless country.  Your body too started to harden with muscle as you grew into the life of a nomad {reg3?woman:man}."),
		(else_try),
			(eq, "$background_answer_2", dplmc_cb2_mummer), # Diplomacy addition
			(str_store_string,s2,"@a mummer"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s12,"@{reg3?girl:boy}"),
			(str_store_string,s3,"@As a {s12} growing out of childhood,	you attached yourself to a troupe of wandering entertainers, going from town to town setting up mummer's shows. It was a life of hard work, selling, begging and stealing your living from the punters who flocked to watch your antics. Over time you became a performer well capable of attracting a crowd."),
		(else_try),
			(eq, "$background_answer_2", dplmc_cb2_courtier), # Diplomacy addition
			(str_store_string,s2,"@a courtier"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s12,"@{reg3?girl:boy}"),
			(str_store_string,s3,"@As a {s12} growing out of childhood, you spent much of your life at court, inserting yourself into the tightly-knit circles of nobility.  With the years you became more and more involved with the politics and intrigue demanded of a high-born {s13}.  You could not afford to remain a stranger to backstabbing and political violence, even if you wanted to."),
		(else_try),
			(eq, "$background_answer_2", dplmc_cb2_noble), # Diplomacy addition
			(str_store_string,s2,"@a noble in training"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s12,"@{reg3?girl:boy}"),
			(try_begin),
				(eq,"$character_gender",tf_male),
				(str_store_string,s3,"@As a {s12} growing out of childhood,	you were trained and educated to perform the duties and wield the rights of a noble landowner.	The managing of taxes and rents were equally important in your education as diplomacy and even personal defence. You learned everything you needed to become a lord of your own hall."),
			(else_try),
				(str_store_string,s3,"@As a {s12} growing out of childhood,	you were trained and educated to the duties of a noble {s13}. You learned much about the household arts, but even more about diplomacy and decorum, and all the things that a future husband might choose to speak of.  Truly, you became every inch as shrewd as any lord, though it would be rude to admit it aloud."),
			(try_end),
		(else_try),
			(eq, "$background_answer_2", dplmc_cb2_acolyte), # Diplomacy addition
			(str_store_string,s2,"@a cleric acolyte"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s12,"@{reg3?girl:boy}"),
			(str_store_string,s3,"@As a {s12} growing out of childhood,	you became an acolyte in the church, the lowest rank on the way to priesthood.	Years of rigorous learning and hard work followed. You were one of several acolytes, performing most of the menial labour in the church in addition to being trained for more holy tasks.  On the night of your adulthood you were allowed to conduct your first service.	After that you were no longer an acolyte {s12}, but a {s13} waiting to take your vows into the service of God."),
		(try_end),
		(str_store_string,s1,"@{s1}^^ You started to learn about the world almost as soon as you could walk and talk.\
		You spent your early life as {s2}. {s3}"),
	  
		## later
		(try_begin),
			(eq, "$background_answer_3", cb3_squire),
			(str_store_string,s2,"@a squire"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.  When you were named squire to a noble at court, you practiced long hours with weapons, learning how to deal out hard knocks and how to take them, too.  You were instructed in your obligations to your lord, and of your duties to those who might one day be your vassals.  But in addition to learning the chivalric ideal, you also learned about the less uplifting side	-- old warriors' stories of ruthless power politics, of betrayals and usurpations, of men who used guile as well as valor to achieve their aims."),
		(else_try),
			(eq, "$background_answer_3", dplmc_cb3_bravo), # Diplomacy addition
			(str_store_string,s2,"@a bravo"),
			(str_store_string,s14,"@{reg3?daughter:man}"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {s13}, and the whole world seemed to change around you.  You left your old life behind to travel the roads as a mercenary, a bravo, guarding caravans for coppers or bashing in heads for silvers. You became a {s14} of the open road, working with bandits as often as against.  Going from fight to fight, you grew experienced at battle, and you learned what it was to kill."),
		(else_try),
			(eq, "$background_answer_3", dplmc_cb3_merc), # Diplomacy addition
			(str_store_string,s2,"@a mercenary"),
			(str_store_string,s14,"@{reg3?daughter:man}"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {s13}, and the whole world seemed to change around you.  You signed on with a mercenary company and travelled far from your home. The life you found was rough and ready, marching to the beat of strange drums and learning unusual ways of fighting.  There were men who taught you how to wield any weapon you desired, and plenty of battles to hone your skills.  You were one of the charmed few who survived through every campaign in which you marched."),
		(else_try),
			(eq, "$background_answer_3", cb3_lady_in_waiting),
			(str_store_string,s2,"@a lady-in-waiting"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.  You joined the tightly-knit circle of women at court, ladies who all did proper ladylike things, the wives and mistresses of noble men as well as maidens who had yet to find a husband.  However, even here you found politics at work as the ladies schemed for prominence and fought each other bitterly to catch the eye of whatever unmarried man was in fashion at court.  You soon learned ways of turning these situations and goings-on to your advantage. With it came the	realisation that you yourself could wield great influence in the world, if only you applied yourself with a little bit of subtlety."),
		(else_try),
			(eq, "$background_answer_3", cb3_troubadour),
			(str_store_string,s2,"@a troubadour"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.  You set out on your own with nothing except the instrument slung over your back and your own voice.  It was a poor existence, with many a hungry night when people failed to appreciate your play, but you managed to survive on your music alone. As the years went by you became adept at playing the drunken crowds in your taverns, and even better at talking anyone out of anything you wanted."),
		(else_try),
			(eq, "$background_answer_3", cb3_student),
			(str_store_string,s2,"@a university student"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.  You found yourself as a student in the university of one of the great cities, where you studied theology, philosophy, and medicine.  But not all your lessons were learned in the lecture halls.  You may or may not have joined in with your fellows as they roamed the alleys in search of wine, women, and a good fight.  However, you certainly were able to observe how a broken jaw is set, or how an angry townsman can be persuaded to set down his club and accept cash compensation for the destruction of his shop."),
		(else_try),
			(eq, "$background_answer_3", cb3_peddler),
			(str_store_string,s2,"@a goods peddler"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.  Heeding the call of the open road, you travelled from village to village buying and selling what you could.  It was not a rich existence, but you became a master at haggling even the most miserly elders into giving you a good price. Soon, you knew, you would be well-placed to start your own trading empire..."),
		(else_try),
			(eq, "$background_answer_3", cb3_craftsman),
			(str_store_string,s2,"@a smith"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.  You pursued a career as a smith, crafting items of function and beauty out of simple metal.  As time wore on you became a master of your trade, and fine work started to fetch fine prices.  With food in your belly and logs on your fire, you could take pride in your work and your growing reputation."),
		(else_try),
			(eq, "$background_answer_3", cb3_poacher),
			(str_store_string,s2,"@a game poacher"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {reg3?woman:man}, and the whole world seemed to change around you.  Dissatisfied with common men's desperate scrabble for coin, you took to your local lord's own forests and decided to help yourself to its bounty, laws be damned. You hunted stags, boars and geese and sold the precious meat under the table. You cut down trees right under the watchmen's noses and turned them into firewood that warmed many freezing homes during winter. All for a few silvers, of course."),
		(else_try),
			(eq, "$background_answer_3", dplmc_cb3_preacher), # Diplomacy addition
			(str_store_string,s2,"@a preacher"),
			(str_store_string,s14,"@{reg3?daughter:man}"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {s13}, and the whole world seemed to change around you.  You packed your few belongings and went out into the world to spread the word of God. You preached to anyone who would listen, and impressed many with the passion of your sermons. Though you had taken a vow to remain in poverty through your itinerant years, you never lacked for food, drink or shelter; the hospitality of the peasantry was always generous to a rising {s13} of God."),
		(else_try),
			(eq, "$background_answer_3", floris_cb3_thief), # Floris addition
			(str_store_string,s2,"@a thief"),
			(str_store_string,s14,"@{reg3?daughter:man}"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {reg3?woman:man}, relying upon your quick thinking and even quicker reflexes to get you through each day.  Dissatisfied with a simple life of laboring for coin, you took to your local streets intent on helping yourself to what you needed in order to survive.  You shun the standard laws of man and have chosen to live by whatever rules allow you to avoid the headsman's block."),
		(else_try),
			(eq, "$background_answer_3", floris_cb3_gladiator), # Floris addition - Credit: eastpaw
			(str_store_string,s2,"@a gladiator"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {s13}, and the whole world seemed to change around you. You earned applause and denars in brutal contests against men and beasts and grew to crave both rewards. Drunk on the bloodlust of the cheering crowd, you learned to tease the opponent and draw out your fight before eventually seizing victory with savage flair. Your agile moves and flamboyant presence mark you as both warrior and artist."),
		(else_try),
			(eq, "$background_answer_3", floris_cb3_bandit), # Floris addition - Credit: eastpaw
			(str_store_string,s2,"@a bandit"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {s13}, and with that change came understanding that the strong have the right to take from the weak. You became part of a band of robbers and grew adept at the art of ambush. You learned how to wield, with some facility, whatever weapon your prey bequeathed to you. When times were good, you caroused and feasted like a king. When pickings were slim, you lived off the land or perfomed quick raids on small villages. You prided yourself on your adaptability and capacity for violence."),
		(else_try),
			(eq, "$background_answer_3", floris_cb3_slaver), # Floris addition - Credit: eastpaw
			(str_store_string,s2,"@a slaver"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s3,"@Though the distinction felt sudden to you, somewhere along the way you had become a {s13}, and the whole world seemed to change around you. By some strange twist of fate you joined a slave caravan as a guard and slowly grew competent at watching over crafty human cattle on long journeys across the face of Calradia. Every so often, you had to raid isolated villages or chase down new livestock, and through these experiences grew accustomed to the blunt language of club and stick. Though your profession is tolerated, it is not particularly respectable, and so you became inured also to suspicion and derision."),
		(try_end),
		(str_store_string,s1,"@{s1}^^ Then, as a young adult, life changed as it always does. You became {s2}. {s3}"),

		## reason
		(try_begin),
			(eq, "$background_answer_4", cb4_revenge),
			(str_store_string,s2,"@personal revenge"),
			(str_store_string,s3,"@Only you know exactly what caused you to give up your old life and become an adventurer.  Still, it was not a difficult choice to leave, with the rage burning brightly in your heart.  You want vengeance. You want justice. What was done to you cannot be undone, and these debts can only be paid in blood..."),
		(else_try),
			(eq, "$background_answer_4", cb4_loss),
			(str_store_string,s2,"@the loss of a loved one"),
			(str_store_string,s3,"@Only you know exactly what caused you to give up your old life and become an adventurer.  All you can say is that you couldn't bear to stay, not with the memories of those you loved so close and so painful. Perhaps your new life will let you forget,	or honour the name that you can no longer bear to speak..."),
		(else_try),
			(eq, "$background_answer_4", cb4_wanderlust),
			(str_store_string,s2,"@wanderlust"),
			(str_store_string,s3,"@Only you know exactly what caused you to give up your old life and become an adventurer.  You're not even sure when your home became a prison, when the familiar became mundane, but your dreams of wandering have taken over your life. Whether you yearn for some faraway place or merely for the open road and the freedom to travel, you could no longer bear to stay in the same place. You simply went and never looked back..."),
		(else_try),
			(eq, "$background_answer_4", cb4_disown),
			(str_store_string,s2,"@being forced out of your home"),
			(str_store_string,s3,"@Only you know exactly what caused you to give up your old life and become an adventurer.  However, you know you cannot go back. There's nothing to go back to. Whatever home you may have had is gone now, and you must face the fact that you're out in the world, alone to fend for yourself..."),
		(else_try),
			(eq, "$background_answer_4", cb4_greed),
			(str_store_string,s2,"@lust for money and power"),
			(str_store_string,s3,"@Only you know exactly what caused you to give up your old life and become an adventurer.  To everyone else, it's clear that you're now motivated solely by personal gain.  You want to be rich, powerful, respected, feared.  You want to be the one whom others hurry to obey.  You want people to know your name, and tremble whenever it is spoken.  You want everything, and you won't let anyone stop you from having it..."),
		(else_try),
			(eq, "$background_answer_4", dplmc_cb4_fervor),
			(str_store_string,s2,"@religious fervor"),
			(str_store_string,s3,"@Only you know exactly what caused you to give up your old life and become an adventurer.  Regardless, the intense faith burning in your soul would not let you find peace in any single place.  There were others in the world, souls to be washed in the light of God. Now you preach wherever you go,	seeking to bring salvation and revelation to the masses, be they faithful or pagan. They will all know the glory of God by the time you're done..."),
		(else_try),
			(eq, "$background_answer_4", floris_cb4_duty),
			(assign, reg3, "$character_gender"),
			(str_store_string,s2,"@a sense of duty"),
			(str_store_string,s13,"@{reg3?woman:man}"),
			(str_store_string,s3,"@As war begins to tear the land apart and many march off to war the desire to join them becomes ever pressing.  As a {s13} of honor you feel duty bound to join the armies of your land and protect the region you call home."),
		(try_end),
		(str_store_string,s1,"@{s1}^^ But soon everything changed and you decided to strike out on your own as an adventurer.\
		What made you take this decision was {s2}. {s3}"),

		## choose skill
		(assign, ":difficulty", 0),
		(try_begin),
			(eq, "$character_gender", tf_female),
			(str_store_string, s2, "str_woman"),
			(val_add, ":difficulty", 1),
		(else_try),
			(str_store_string, s2, "str_man"),
		(try_end),
		(try_begin),
			(eq,"$background_type",cb_noble),
			(str_store_string, s3, "str_noble"),
			(val_sub, ":difficulty", 1),
		(else_try),
			(str_store_string, s3, "str_common"),
		(try_end),
		  
		(try_begin),
			(eq, ":difficulty", -1),
			(str_store_string, s4, "str_may_find_that_you_are_able_to_take_your_place_among_calradias_great_lords_relatively_quickly"),
		(else_try),
			(eq, ":difficulty", 0),
			(str_store_string, s4, "str_may_face_some_difficulties_establishing_yourself_as_an_equal_among_calradias_great_lords"),
		(else_try),
			(eq, ":difficulty", 1),
			(str_store_string, s4, "str_may_face_great_difficulties_establishing_yourself_as_an_equal_among_calradias_great_lords"),
		(try_end),
		(str_store_string,s1,"@^{s1}^^ As a {s3} {s2}. You {s4}"),
	]),
  
# script_ccp_generate_skill_set
# Generates skills a character starts with based upon their background choices.
# Input: mode
# Output: none
("ccp_generate_skill_set",
	[
		(store_script_param, ":mode", 1),
		
		# Clean out inventory
		(try_for_range, ":slot", ccp_item_storage_begin, ccp_item_storage_end),
			(troop_set_slot, ccp_data, ":slot", 0),
		(try_end),
		
		# Initialize abilities
		(assign, ":strength", 0),
		(assign, ":agility", 0),
		(assign, ":intelligence", 0),
		(assign, ":charisma", 0),
		# Initialize proficiencies
		(assign, ":prof_onehand", 0),
		(assign, ":prof_twohand", 0),
		(assign, ":prof_polearm", 0),
		(assign, ":prof_archery", 0),
		(assign, ":prof_crossbow", 0),
		(assign, ":prof_throwing", 0),
		# Initialize skills
		(assign, ":skill_ironflesh", 0),
		(assign, ":skill_powerstrike", 0),
		(assign, ":skill_weaponmaster", 0),
		(assign, ":skill_riding", 0),
		(assign, ":skill_tactics", 0),
		(assign, ":skill_leadership", 0),
		(assign, ":skill_firstaid", 0),
		(assign, ":skill_pathfinding", 0),
		(assign, ":skill_spotting", 0),
		(assign, ":skill_tracking", 0),
		(assign, ":skill_trade", 0),
		#(assign, ":skill_foraging", 0),
		(assign, ":skill_surgery", 0),
		(assign, ":skill_powerthrow", 0),
		(assign, ":skill_powerdraw", 0),
		(assign, ":skill_horsearchery", 0),
		(assign, ":skill_athletics", 0),
		(assign, ":skill_engineer", 0),
		(assign, ":skill_persuasion", 0),
		(assign, ":skill_prisonmanagement", 0),
		(assign, ":skill_inventorymanagement", 0),
		(assign, ":skill_trainer", 0),
		(assign, ":skill_looting", 0),
		(assign, ":skill_woundtreatment", 0),
		(assign, ":skill_shield", 0),
		# (assign, ":skill_reserved", 0),
		# Initialize misc
		(assign, ":gold", 0),
		(assign, ":renown", 0),
		(assign, ":honor", 0),
		(assign, ":lands", 0),
		(assign, ":smithy", 0),
		(assign, ":ledger", 0),
		# Initialize equipment choices
		(assign, ":trade1", 0),
		(assign, ":trade2", 0),
		(assign, ":horse", 0),
		(assign, ":richhorse", 0),
		(assign, ":shield", 0),
		(assign, ":instrument", 0),
		# (assign, ":poorboots", 0),
		(assign, ":boots", 0),
		(assign, ":richboots", 0),
		# (assign, ":cloth", 0),
		(assign, ":dress", 0),
		(assign, ":armor", 0),
		(assign, ":gauntlets", 0),
		(assign, ":hood", 0),
		(assign, ":helmet", 0),
		(assign, ":ladyhelmet", 0),
		(assign, ":axe", 0),
		(assign, ":blunt", 0),
		# (assign, ":dagger", 0),
		(assign, ":spear", 0),
		(assign, ":sword", 0),
		(assign, ":bow", 0),
		(assign, ":throwing", 0),
		(assign, ":throwing_knives", 0),
		
		(try_begin),
			(eq,"$character_gender",0),		#Male
			(val_add, ":charisma", 1),
			(val_add, ":strength", 1),
		(else_try),						    #Female
			(val_add, ":agility", 1),
			(val_add, ":intelligence", 1),
		(try_end),
		  
		(val_add, ":strength", 1),
		(val_add, ":agility", 1),
		(val_add, ":charisma", 1),
		
		(val_add, ":skill_leadership", 1),
		(val_add, ":skill_riding", 1),
		(val_add, ":skill_prisonmanagement", 1),
		
		(try_begin), #You father was a...
			(eq,"$background_type", cb_noble),
			(eq,"$character_gender", tf_male),
			(val_add, ":intelligence", 1),
			(val_add, ":charisma", 2),
			(val_add, ":skill_weaponmaster", 1),
			(val_add, ":skill_powerstrike", 1),
			(val_add, ":skill_riding", 1),
			# (val_add, ":skill_tactics", 1),  # Removed from native for balancing.
			(val_add, ":skill_leadership", 1),
			(val_add, ":prof_onehand", 10),
			(val_add, ":prof_twohand", 10),
			(val_add, ":prof_polearm", 10),
			(val_add, ":gold", 100),
			(val_add, ":honor", 3),
			(val_add, ":renown", 100),
			(val_add, ":lands", 2),                # non-native
			(assign, ":shield", 1),
			(assign, ":richhorse", 1),
		(else_try),
			(eq,"$background_type", cb_noble),
			(eq,"$character_gender", tf_female),
			(val_add, ":intelligence", 1),         # native = 2
			(val_add, ":charisma", 2),             # native = 1
			(val_add, ":skill_riding", 2),
			(val_add, ":skill_persuasion", 1),     # Native = first aid
			(val_add, ":skill_leadership", 1),
			(val_add, ":prof_onehand", 20),
			(val_add, ":prof_crossbow", 10),       # non-native
			(val_add, ":gold", 100),
			(val_add, ":renown", 50),
			(val_add, ":lands", 2),                # non-native
			(assign, ":shield", 1),
			(assign, ":richhorse", 1),
		(else_try),
			(eq,"$background_type", cb_merchant),
			(val_add, ":intelligence", 2),
			(val_add, ":charisma", 1),
			(val_add, ":skill_trade", 2),
			(val_add, ":skill_inventorymanagement", 2),
			(val_add, ":skill_riding", 1),
			(val_add, ":skill_leadership", 1),
			(val_add, ":prof_twohand", 10),
			(val_add, ":gold", 1000),
			(val_add, ":renown", 20),
			(assign, ":horse", 1),
			(assign, ":trade1", 1),
			(assign, ":ledger", 1),
		(else_try),
			(eq,"$background_type", cb_guard),
			(val_add, ":strength", 1),
			(val_add, ":agility", 1),
			(val_add, ":charisma", 1),
			(val_add, ":skill_ironflesh", 1),
			(val_add, ":skill_weaponmaster", 1),
			(val_add, ":skill_powerstrike", 1),
			(val_add, ":skill_trainer", 1),
			(val_add, ":skill_leadership", 1),
			(val_add, ":prof_onehand", 10),
			(val_add, ":prof_twohand", 15),
			(val_add, ":prof_polearm", 20),
			(val_add, ":prof_throwing", 10),
			(val_add, ":gold", 20),
			(val_add, ":renown", 10),
			(assign, ":shield", 1),
			(assign, ":horse", 1),
		(else_try),
			(eq,"$background_type", cb_forester),
			(val_add, ":strength", 1),
			(val_add, ":agility", 2),
			(val_add, ":skill_powerdraw", 2),         # Native = 1
			(val_add, ":skill_tracking", 1),
			(val_add, ":skill_pathfinding", 1),
			(val_add, ":skill_spotting", 1),
			(val_add, ":skill_athletics", 1),
			#(val_add, ":skill_foraging", 1),          # Non-native
			(val_add, ":prof_twohand", 10),
			(val_add, ":prof_archery", 30),
			(val_add, ":gold", 30),
			(val_add, ":honor", 3),
			(assign, ":horse", 1),
		(else_try),
			(eq,"$background_type", cb_nomad),
			(eq,"$character_gender", tf_male),
			(val_add, ":strength", 1),
			(val_add, ":agility", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_powerdraw", 1),
			(val_add, ":skill_horsearchery", 1),
			(val_add, ":skill_pathfinding", 1),
			(val_add, ":skill_riding", 1),           # Native = 2
			(val_add, ":skill_trade", 1),            # Non-native
			(val_add, ":prof_onehand", 10),
			(val_add, ":prof_archery", 30),
			(val_add, ":prof_throwing", 25),         # native = 10
			(val_add, ":gold", 15),
			(val_add, ":renown", 10),
			(assign, ":horse", 1),
			(assign, ":shield", 1),
		(else_try),
			(eq,"$background_type", cb_nomad),
			(eq,"$character_gender", tf_female),
			# (val_add, ":strength", 1),
			(val_add, ":agility", 2),                # Native = 1
			(val_add, ":intelligence", 1),
			(val_add, ":skill_woundtreatment", 1),
			(val_add, ":skill_firstaid", 1),
			#(val_add, ":skill_pathfinding", 1),
			(val_add, ":skill_tracking", 1),         # Non-native
			(val_add, ":skill_trade", 1),            # Non-native
			(val_add, ":skill_riding", 2),
			(val_add, ":prof_onehand", 10),           # native = 5
			(val_add, ":prof_archery", 30),          # native = 20
			(val_add, ":prof_throwing", 5),
			(val_add, ":gold", 20),
			(assign, ":horse", 1),
			(assign, ":shield", 1),
		(else_try),
			(eq,"$background_type", cb_thief),
			(val_add, ":agility", 3),
			(val_add, ":skill_powerthrow", 1),
			(val_add, ":skill_athletics", 2),
			(val_add, ":skill_inventorymanagement", 1),
			(val_add, ":skill_looting", 2),
			(val_add, ":prof_onehand", 25),     # Native 20
			(val_add, ":prof_archery", 10),     # Non-native
			(val_add, ":prof_throwing", 25),    # Native 20
			(val_add, ":gold", 25),
			(assign, ":horse", 1),
		(else_try),
			(eq,"$background_type", cb_priest), # Diplomacy addition
			(val_add, ":strength", 2),
			(val_add, ":charisma", 2),
			(val_add, ":skill_woundtreatment", 2),
			(val_add, ":skill_persuasion", 2),
			(val_add, ":skill_leadership", 1),
			(val_add, ":skill_firstaid", 1),
			(val_add, ":skill_ironflesh", 1),
			(val_add, ":prof_polearm", 20),
			(assign, ":richhorse", 1),
			(assign, ":blunt", 1),
		(try_end),
	  
		(try_begin), #Early life
			(eq,"$background_answer_2", cb2_page),
			(val_add, ":strength", 1),
			(val_add, ":charisma", 1),
			(val_add, ":skill_powerstrike", 1),
			# (val_add, ":skill_persuasion", 1),
			(val_add, ":skill_shield", 1),         # non-native
			(val_add, ":prof_onehand", 15),
			(val_add, ":prof_polearm", 10),        # native = 5
			(val_add, ":prof_crossbow", 10),       # non-native
			(val_add, ":gold", 25),                # non-native
			(assign, ":richboots", 1),
			(assign, ":bow", 1),
		(else_try),
			(eq,"$background_answer_2", cb2_apprentice),
			(val_add, ":strength", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_trade", 1),
			(val_add, ":skill_engineer", 2),        # native = 1
			(val_add, ":prof_onehand", 15),         # non-native
			(val_add, ":gold", 200),                # non-native
			(assign, ":boots", 1),
			(assign, ":bow", 1),
		(else_try),
			(eq,"$background_answer_2", cb2_urchin),
			(val_add, ":agility", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_spotting", 1),
			(val_add, ":skill_athletics", 1),       # non-native
			(val_add, ":skill_looting", 1),
			(val_add, ":skill_powerthrow", 1),       # non-native
			(val_add, ":prof_onehand", 10),         # native = 15
			(val_add, ":prof_throwing", 20),
			# (assign, ":poorboots", 1),
			# (assign, ":throwing", 1),
			(assign, ":throwing_knives", 1),
		(else_try),
			(eq,"$background_answer_2", cb2_steppe_child),
			(val_add, ":strength", 1),
			(val_add, ":agility", 1),
			(val_add, ":skill_horsearchery", 1),
			#(val_add, ":skill_powerthrow", 1),
			(val_add, ":skill_powerdraw", 1),       # non-native
			(val_add, ":skill_spotting", 1),        # non-native
			#(val_add, ":skill_foraging", 1),        # non-native
			(val_add, ":prof_archery", 15),
			(val_add, ":renown", 5),
			(assign, ":boots", 1),
			(assign, ":bow", 1),
		(else_try),
			(eq,"$background_answer_2", cb2_merchants_helper),
			(val_add, ":intelligence", 1),
			(val_add, ":charisma", 1),
			(val_add, ":skill_inventorymanagement", 1),
			(val_add, ":skill_trade", 2),           # Native = 1
			(val_add, ":skill_persuasion", 1),      # non-native
			(val_add, ":gold", 200),                # non-native
			(assign, ":boots", 1),
			(assign, ":bow", 1),
		(else_try),
		    (eq,"$background_answer_2", dplmc_cb2_mummer), # Diplomacy addition
			(val_add, ":agility", 1),
			(val_add, ":charisma", 1),
			(val_add, ":skill_leadership", 1),
			(val_add, ":skill_athletics", 1),
			(val_add, ":skill_riding", 1),
			(val_add, ":prof_twohand", 5),
			(val_add, ":prof_polearm", 5),
			(val_add, ":renown", 15),
			(assign, ":boots", 1),
			(assign, ":bow", 1),
		(else_try),
		    (eq,"$background_answer_2", dplmc_cb2_courtier), # Diplomacy addition
			(val_add, ":charisma", 2),
			(val_add, ":skill_weaponmaster", 1),
			(val_add, ":prof_polearm", 10),
			(val_add, ":prof_onehand", 15),
			(val_add, ":prof_crossbow", 10),
			(val_add, ":renown", 20),
			(assign, ":richboots", 1),
			# (call_script, "script_ccp_add_item", "itm_we_rho_crossbow_hunting"),
			# (call_script, "script_ccp_add_item", "itm_we_rho_bolt"),
		(else_try),
		    (eq,"$background_answer_2", dplmc_cb2_noble), # Diplomacy addition
			(val_add, ":intelligence", 2),
			(val_add, ":skill_leadership", 2),
			(val_add, ":skill_tactics", 2),
			# (val_add, ":prof_onehand", 10),
			# (val_add, ":prof_twohand", 10),
			(val_add, ":renown", 15),
			#(val_add, ":lands", 2),
			(assign, ":richboots", 1),
			(assign, ":bow", 1),
		(else_try),
		    (eq,"$background_answer_2", dplmc_cb2_acolyte), # Diplomacy addition
			(val_add, ":charisma", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_firstaid", 1),
			(val_add, ":skill_surgery", 1),
			(val_add, ":skill_riding", 1),
			(val_add, ":prof_polearm", 10),
			(val_add, ":renown", 5),
			#(call_script, "script_ccp_add_item", "itm_bo_pla_t0_sandal"),
			(assign, ":bow", 1),
		(try_end),
		
		(try_begin), #Adulthood
		    (eq,"$background_answer_3", dplmc_cb3_bravo), # Diplomacy addition
			(val_add, ":strength", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_powerstrike", 1),
			(val_add, ":skill_shield", 1),
			(val_add, ":skill_riding", 1),
			(val_add, ":skill_horsearchery", 1),
			(val_add, ":skill_spotting", 1),
			(val_add, ":prof_onehand", 20),
			(val_add, ":prof_crossbow", 20),
			(val_add, ":gold", 10),
			(assign, ":armor", 1),
			(assign, ":gauntlets", 1),
			(assign, ":helmet", 1),
			(assign, ":sword", 1),
			(assign, ":trade2", 1),
	    (else_try),
		    (eq,"$background_answer_3", dplmc_cb3_merc), # Diplomacy addition
			(val_add, ":agility", 1),
			(val_add, ":strength", 1),
			(val_add, ":skill_powerstrike", 1),
			(val_add, ":skill_powerdraw", 1),
			(val_add, ":skill_shield", 1),
			(val_add, ":prof_crossbow", 10),
			(val_add, ":prof_twohand", 25),
			(val_add, ":prof_onehand", 25),
			(val_add, ":prof_archery", 20),
			# (val_add, ":prof_throwing", 15),
			# (val_add, ":prof_polearm", 20),
			(val_add, ":gold", 20),
			(assign, ":armor", 1),
			(assign, ":gauntlets", 1),
			(assign, ":helmet", 1),
			(assign, ":spear", 1),
		 (else_try),
		    (eq,"$background_answer_3", floris_cb3_gladiator), # Floris addition - Credit: eastpaw
			(val_add, ":agility", 1),
			(val_add, ":charisma", 1),
			(val_add, ":skill_weaponmaster", 2),
			(val_add, ":skill_ironflesh", 1),
			(val_add, ":skill_shield", 1),
			(val_add, ":prof_twohand", 30),
			(val_add, ":prof_onehand", 30),
			(val_add, ":renown", 30),
			(val_add, ":gold", 20),
			(assign, ":armor", 1),
			(assign, ":gauntlets", 1),
			(assign, ":helmet", 1),
			(assign, ":sword", 1),
		(else_try),
		    (eq,"$background_answer_3", floris_cb3_bandit), # Floris addition - Credit: eastpaw
			(val_add, ":agility", 2),
			(val_add, ":skill_powerstrike", 1),
			(val_add, ":skill_riding", 1),
			(val_add, ":skill_looting", 1),
			#(val_add, ":skill_foraging", 1),
			(val_add, ":skill_spotting", 1),
			(val_add, ":prof_twohand", 15),
			(val_add, ":prof_onehand", 15),
			(val_add, ":prof_archery", 15),
			(val_add, ":prof_throwing", 15),
			(val_add, ":gold", 75),
			(assign, ":gauntlets", 1),
			(assign, ":helmet", 1),
			(assign, ":sword", 1),
		(else_try),
		    (eq,"$background_answer_3", floris_cb3_slaver), # Floris addition - Credit: eastpaw
			(val_add, ":strength", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_weaponmaster", 1),
			(val_add, ":skill_riding", 1),
			(val_add, ":skill_prisonmanagement", 3),
			(val_add, ":prof_polearm", 10),
			(val_add, ":prof_onehand", 35),
			(val_add, ":gold", 100),
			(val_add, ":honor", 3),
			(assign, ":armor", 1),
			(assign, ":gauntlets", 1),
			(assign, ":helmet", 1),
			(assign, ":blunt", 1),
		(else_try),
		    (eq,"$background_answer_3", dplmc_cb3_preacher), # Diplomacy addition
			(val_add, ":strength", 1),
			(val_add, ":charisma", 1),
			(val_add, ":skill_woundtreatment", 1),
			(val_add, ":skill_firstaid", 1),
			(val_add, ":skill_surgery", 1),
			(val_add, ":skill_leadership", 1),
			(val_add, ":skill_persuasion", 2),
			(val_add, ":prof_polearm", 30),
			(val_add, ":gold", 50),
			(assign, ":blunt", 1),
			#(call_script, "script_ccp_add_item", "itm_ar_pla_pri_monkrobe"),
	    (else_try),
			(eq,"$background_answer_3",cb3_poacher),
			(val_add, ":strength", 1),
			(val_add, ":agility", 1),
			(val_add, ":skill_powerdraw", 1),
			(val_add, ":skill_tracking", 1),
			(val_add, ":skill_spotting", 1),
			(val_add, ":skill_athletics", 1),  # Native = 2
			#(val_add, ":skill_foraging", 1),   # Non-native
			(val_add, ":prof_onehand", 10),    # Non-native
			(val_add, ":prof_polearm", 10),
			(val_add, ":prof_archery", 35),
			(val_add, ":gold", 10),
			# (assign, ":armor", 1),
			# (assign, ":cloth", 1),
			(call_script, "script_ccp_add_item", "itm_fur_coat"),
			(assign, ":hood", 1),
			(assign, ":dagger", 1),
			(assign, ":bow", 1),
		(else_try),
			(eq,"$background_answer_3",cb3_craftsman),
			(val_add, ":strength", 2),                # native = 1
			# (val_add, ":intelligence", 1),
			# (val_add, ":skill_weaponmaster", 1),
			(val_add, ":skill_engineer", 1),
			# (val_add, ":skill_tactics", 1),
			(val_add, ":skill_trade", 1),
			(val_add, ":skill_ironflesh", 1),
			(val_add, ":prof_onehand", 15),
			(val_add, ":gold", 100),
			(assign, ":smithy", 1),                # non-native
			# (assign, ":cloth", 1),
			(assign, ":sword", 1),
		(else_try),
			(eq,"$background_answer_3",cb3_peddler),
			(val_add, ":charisma", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_trade", 2),
			(val_add, ":skill_inventorymanagement", 1),
			# (val_add, ":skill_pathfinding", 1),
			(val_add, ":skill_riding", 1),
			(val_add, ":prof_polearm", 15),
			(val_add, ":gold", 1200),
			# (assign, ":cloth", 1),
			(assign, ":trade2", 1),
			(assign, ":sword", 1),
			(assign, ":ledger", 1),
		(else_try),
			(eq,"$background_answer_3",cb3_troubadour),
			(val_add, ":charisma", 2),
			(val_add, ":skill_weaponmaster", 1),
			(val_add, ":skill_persuasion", 2),
			(val_add, ":skill_pathfinding", 1),
			(val_add, ":skill_leadership", 1),
			(val_add, ":prof_onehand", 25),
			(val_add, ":prof_crossbow", 10),
			(val_add, ":gold", 200),
			# (assign, ":cloth", 1),
			(assign, ":instrument", 1),
			(assign, ":sword", 1),
		(else_try),
			(eq,"$background_answer_3",cb3_squire),
			(eq,"$character_gender",tf_male),
			(val_add, ":strength", 1),
			(val_add, ":agility", 1),
			(val_add, ":skill_riding", 1),
			(val_add, ":skill_powerstrike", 1),
			# (val_add, ":skill_leadership", 1),  # Removed for balance.
			(val_add, ":skill_weaponmaster", 1),
			(val_add, ":prof_onehand", 30),
			(val_add, ":prof_twohand", 10),
			(val_add, ":prof_polearm", 30),
			# (val_add, ":prof_archery", 10),
			# (val_add, ":prof_throwing", 10),
			(val_add, ":prof_crossbow", 10),
			(val_add, ":gold", 20),
			(assign, ":armor", 1),
			(assign, ":gauntlets", 1),
			(assign, ":helmet", 1),
			(assign, ":sword", 1),
		(else_try),
			(eq,"$background_answer_3",cb3_lady_in_waiting),
			(eq,"$character_gender",tf_female),
			(val_add, ":charisma", 2),              # Native = 1
			(val_add, ":intelligence", 1),
			(val_add, ":skill_woundtreatment", 1),
			(val_add, ":skill_persuasion", 2),
			(val_add, ":skill_riding", 2),
			(val_add, ":prof_onehand", 10),
			(val_add, ":prof_crossbow", 15),
			(val_add, ":gold", 100),
			(assign, ":dress", 1),
			(assign, ":ladyhelmet", 1),
			(assign, ":sword", 1),
		(else_try),
			(eq,"$background_answer_3",cb3_student),
			(val_add, ":intelligence", 2),
			(val_add, ":skill_woundtreatment", 1),
			(val_add, ":skill_weaponmaster", 1),
			(val_add, ":skill_surgery", 1),
			(val_add, ":skill_engineer", 1),     # Non-native
			(val_add, ":skill_persuasion", 1),
			(val_add, ":prof_onehand", 20),
			(val_add, ":prof_crossbow", 20),
			(val_add, ":gold", 200),
			# (assign, ":cloth", 1),
			(assign, ":sword", 1),
			(store_random_in_range, ":type_of_book", 0, 2), # Done because we have dummy books between readable and reference types.
			(try_begin),
				(eq, ":type_of_book", 0),
				(store_random_in_range, ":book_no", readable_books_begin, readable_books_end),
			(else_try),
				(store_random_in_range, ":book_no", reference_books_begin, reference_books_end),
			(try_end),
			(call_script, "script_ccp_add_item", ":book_no"),
		(else_try),
			(eq,"$background_answer_3",floris_cb3_thief),
			(val_add, ":agility", 2),
			(val_add, ":skill_persuasion", 1),
			(val_add, ":skill_athletics", 2),
			(val_add, ":skill_looting", 2),
			(val_add, ":prof_onehand", 25),
			(val_add, ":prof_throwing", 25),
			(val_add, ":prof_archery", 10),
			(val_add, ":gold", 10),
			# (assign, ":cloth", 1),
			# (assign, ":dagger", 1),
		(try_end),
	  
		(try_begin), #Reason for adventuring
			(eq,"$background_answer_4", cb4_revenge),
			(val_add, ":strength", 2),
			(val_add, ":skill_powerstrike", 1),
			(call_script, "script_ccp_add_item", "itm_smoked_fish"),
		(else_try),
			(eq,"$background_answer_4", cb4_loss),
			(val_add, ":charisma", 2),
			(val_add, ":skill_ironflesh", 1),
			(call_script, "script_ccp_add_item", "itm_dried_meat"),
		(else_try),
			(eq,"$background_answer_4", cb4_wanderlust),
			(val_add, ":agility", 2),
			# (val_add, ":skill_pathfinding", 1),
			(val_add, ":skill_riding", 1),
			(call_script, "script_ccp_add_item", "itm_bread"),
		(else_try),
			(eq,"$background_answer_4", cb4_disown),
			(val_add, ":strength", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_weaponmaster", 1),
			(call_script, "script_ccp_add_item", "itm_cabbages"),
		(else_try),
			(eq,"$background_answer_4", cb4_greed),
			(val_add, ":agility", 1),
			(val_add, ":intelligence", 1),
			(val_add, ":skill_looting", 1),
			(call_script, "script_ccp_add_item", "itm_apples"),
			(store_mul, ":gold_bonus", ":gold", 10),
			(val_div, ":gold_bonus", 100),
			(val_add, ":gold", ":gold_bonus"),
		(else_try),
		    (eq,"$background_answer_4", dplmc_cb4_fervor),
			(val_add, ":charisma", 1),
			(val_add, ":strength", 1),
			(val_add, ":skill_woundtreatment", 1),
		    (call_script, "script_ccp_add_item", "itm_sausages"),
		(else_try),
		    (eq,"$background_answer_4", floris_cb4_duty),
			(val_add, ":strength", 1),
			(val_add, ":agility", 1),
			(val_add, ":skill_leadership", 1),
		    (call_script, "script_ccp_add_item", "itm_dried_meat"),
		(try_end),
		
		(troop_get_slot, ":value", ccp_objects, ccp_val_menu_initial_region),
		(store_add, ":faction", kingdoms_begin, ":value"),
		(val_add, ":faction", 1),
		(try_begin), #Starting region benefits
			(eq, ":faction", "fac_kingdom_1"), # Swadia
			(val_add, ":prof_polearm", 15),
			(val_add, ":prof_onehand", 10),
			(val_add, ":prof_archery", 5),
			# replaces some native game menu code
			(assign, "$current_town", "p_town_6"),
			(assign, "$g_starting_town", "$current_town"),
			(assign, "$g_journey_string", "str_journey_to_praven"),
		(else_try),
			(eq, ":faction", "fac_kingdom_2"), # Vaegir
			(val_add, ":prof_archery", 15),
			(val_add, ":prof_polearm", 10),
			(val_add, ":prof_onehand", 5),
			# replaces some native game menu code
			(assign, "$current_town", "p_town_8"),
			(assign, "$g_starting_town", "$current_town"),
			(assign, "$g_journey_string", "str_journey_to_reyvadin"),
		(else_try),
			(eq, ":faction", "fac_kingdom_3"), # Khergit
			(val_add, ":prof_archery", 15),
			(val_add, ":prof_onehand", 10),
			(val_add, ":prof_twohand", 5),
			# replaces some native game menu code
			(assign, "$current_town", "p_town_10"),
			(assign, "$g_starting_town", "$current_town"),
			(assign, "$g_journey_string", "str_journey_to_tulga"),
		(else_try),
			(eq, ":faction", "fac_kingdom_4"), # Nord
			(val_add, ":prof_twohand", 15),
			(val_add, ":prof_throwing", 10),
			(val_add, ":prof_onehand", 5),
			# replaces some native game menu code
			(assign, "$current_town", "p_town_1"),
			(assign, "$g_starting_town", "$current_town"),
			(assign, "$g_journey_string", "str_journey_to_sargoth"),
		(else_try),
			(eq, ":faction", "fac_kingdom_5"), # Rhodoks
			(val_add, ":prof_crossbow", 15),
			(val_add, ":prof_onehand", 10),
			(val_add, ":prof_polearm", 5),
			# replaces some native game menu code
			(assign, "$current_town", "p_town_5"),
			(assign, "$g_starting_town", "$current_town"),
			(assign, "$g_journey_string", "str_journey_to_jelkala"),
		(else_try),
		    (eq, ":faction", "fac_kingdom_6"), # Sarranid
			(val_add, ":prof_onehand", 15),
			(val_add, ":prof_twohand", 10),
			(val_add, ":prof_archery", 5),
			# replaces some native game menu code
			(assign, "$current_town", "p_town_19"),
			(assign, "$g_starting_town", "$current_town"),
			(assign, "$g_journey_string", "str_journey_to_shariz"),
		(else_try),
		    (display_message, "@ERROR: No valid faction designated."),
		(try_end),
		
		(try_begin),
			(eq, "$background_type", cb_noble),
			(eq, "$background_answer_2", dplmc_cb2_noble),
			(val_add, ":lands", 2),
		(try_end),
		
		##### DEVELOP STAT REPORT #####
		(try_begin),
			(eq, ":mode", limit_to_stats),
			
			# Update the player's strength
			(store_add, reg5, ":strength", 4),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_strength),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's agility
			(store_add, reg5, ":agility", 4),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_agility),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's intelligence
			(store_add, reg5, ":intelligence", 4),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_intelligence),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's charisma
			(store_add, reg5, ":charisma", 4),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_charisma),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's gold
			(store_add, reg5, ":gold", 0),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_gold),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's renown
			(store_add, reg5, ":renown", 0),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_renown),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's one handed proficiency
			(store_add, reg5, ":prof_onehand", 15),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_weapon_onehand),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's two handed proficiency
			(store_add, reg5, ":prof_twohand", 15),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_weapon_twohand),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's polearm proficiency
			(store_add, reg5, ":prof_polearm", 15),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_weapon_polearm),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's archery proficiency
			(store_add, reg5, ":prof_archery", 15),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_weapon_archery),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's crossbow proficiency
			(store_add, reg5, ":prof_crossbow", 15),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_weapon_crossbow),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			# Update the player's throwing proficiency
			(store_add, reg5, ":prof_throwing", 15),
			(troop_get_slot, ":obj_label", ccp_objects, ccp_obj_stat_weapon_throwing),
			(overlay_set_text, ":obj_label", "@{reg5}"),
			###### UPDATE SKILLS ######
			(assign, ":line_count", 0),
			# Ironflesh
			(try_begin),
				(ge, ":skill_ironflesh", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_ironflesh", ":skill_ironflesh", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Power Strike
			(try_begin),
				(ge, ":skill_powerstrike", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_powerstrike", ":skill_powerstrike", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Power Throw
			(try_begin),
				(ge, ":skill_powerthrow", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_powerthrow", ":skill_powerthrow", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Power Draw
			(try_begin),
				(ge, ":skill_powerdraw", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_powerdraw", ":skill_powerdraw", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Weapon Master
			(try_begin),
				(ge, ":skill_weaponmaster", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_weaponmaster", ":skill_weaponmaster", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Shield
			(try_begin),
				(ge, ":skill_shield", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_shield", ":skill_shield", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Athletics
			(try_begin),
				(ge, ":skill_athletics", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_athletics", ":skill_athletics", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Riding
			(try_begin),
				(ge, ":skill_riding", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_riding", ":skill_riding", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Horse Archery
			(try_begin),
				(ge, ":skill_horsearchery", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_horsearchery", ":skill_horsearchery", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Looting
			(try_begin),
				(ge, ":skill_looting", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_looting", ":skill_looting", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Foraging
			# (try_begin),
				# (ge, ":skill_foraging", 1),
				# (call_script, "script_ccp_add_skill_display", "str_ccp_skl_foraging", ":skill_foraging", ":line_count"),
				# (val_add, ":line_count", 1),
			# (try_end),
			# Trainer
			(try_begin),
				(ge, ":skill_trainer", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_trainer", ":skill_trainer", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Tracking
			(try_begin),
				(ge, ":skill_tracking", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_tracking", ":skill_tracking", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Tactics
			(try_begin),
				(ge, ":skill_tactics", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_tactics", ":skill_tactics", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Path-Finding
			(try_begin),
				(ge, ":skill_pathfinding", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_pathfinding", ":skill_pathfinding", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Spotting
			(try_begin),
				(ge, ":skill_spotting", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_spotting", ":skill_spotting", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Inventory Management
			(try_begin),
				(ge, ":skill_inventorymanagement", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_inventorymanagement", ":skill_inventorymanagement", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Wound Treatment
			(try_begin),
				(ge, ":skill_woundtreatment", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_woundtreatment", ":skill_woundtreatment", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Surgery
			(try_begin),
				(ge, ":skill_surgery", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_surgery", ":skill_surgery", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# First Aid
			(try_begin),
				(ge, ":skill_firstaid", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_firstaid", ":skill_firstaid", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Engineer
			(try_begin),
				(ge, ":skill_engineer", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_engineer", ":skill_engineer", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Persuasion
			(try_begin),
				(ge, ":skill_persuasion", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_persuasion", ":skill_persuasion", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Prisoner Management
			(try_begin),
				(ge, ":skill_prisonmanagement", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_prisonermanagement", ":skill_prisonmanagement", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Leadership
			(try_begin),
				(ge, ":skill_leadership", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_leadership", ":skill_leadership", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
			# Trade
			(try_begin),
				(ge, ":skill_trade", 1),
				(call_script, "script_ccp_add_skill_display", "str_ccp_skl_trade", ":skill_trade", ":line_count"),
				(val_add, ":line_count", 1),
			(try_end),
		(try_end),
		
		##### INCREASE PLAYER SKILLS / LOAD ITEMS INTO INVENTORY #####
		(try_begin),
			(eq, ":mode", equip_the_player),
			### LOAD IN EQUIPMENT ###
			# Determine faction choice.
			(troop_get_slot, ":value", ccp_objects, ccp_val_menu_initial_region),
			(store_add, ":faction", kingdoms_begin, ":value"),
			(val_add, ":faction", 1),
			(assign, ":faction_slot", ccp_swadia_items_begin),   # This just gets us a base of 130 to begin with.
			(store_mul, ":faction_range", ":value", 30),       # The '30' is defined by how many constants were set aside for each faction in ccp_constants.py
			(val_add, ":faction_slot", ":faction_range"),        # This is where we figure out the first slot # for the specified faction.
			(try_begin),
				(ge, DEBUG_CCP_general, 1),
				(assign, reg31, ":faction_slot"),
				(str_store_faction_name, s32, ":faction"),
				# (display_message, "@Faction = {s32}"),
				# (display_message, "@Starting slot = {reg31}"),
				(display_message, "@Equipment will be determined by faction {s32} starting at slot {reg31}."),
			(try_end),
			
			# Designate our slots to get faction gear from.
			(store_add, ":slot_trade1", ":faction_slot", 0),
			(store_add, ":slot_trade2", ":faction_slot", 1),
			(store_add, ":slot_horse", ":faction_slot", 2),
			(store_add, ":slot_richhorse", ":faction_slot", 3),
			(store_add, ":slot_shield", ":faction_slot", 4),
			(store_add, ":slot_instrument", ":faction_slot", 5),
			(store_add, ":slot_poorboots", ":faction_slot", 6),
			(store_add, ":slot_boots", ":faction_slot", 7),
			(store_add, ":slot_richboots", ":faction_slot", 8),
			(store_add, ":slot_cloth", ":faction_slot", 9),
			(store_add, ":slot_dress", ":faction_slot", 10),
			(store_add, ":slot_armor", ":faction_slot", 11),
			(store_add, ":slot_gauntlets", ":faction_slot", 12),
			(store_add, ":slot_hood", ":faction_slot", 13),
			(store_add, ":slot_helmet", ":faction_slot", 14),
			(store_add, ":slot_ladyhelmet", ":faction_slot", 15),
			(store_add, ":slot_axe", ":faction_slot", 16),
			(store_add, ":slot_blunt", ":faction_slot", 17),
			(store_add, ":slot_dagger", ":faction_slot", 18),
			(store_add, ":slot_spear", ":faction_slot", 19),
			(store_add, ":slot_sword", ":faction_slot", 20),
			(store_add, ":slot_bow", ":faction_slot", 21),
			(store_add, ":slot_arrow", ":faction_slot", 22),
			(store_add, ":slot_throwing", ":faction_slot", 23),
			
			# Caba's Trade Ledger
			(try_begin),
				(eq, ":ledger", 1),
				(call_script, "script_ccp_add_item", "itm_book_trade_ledger"),
			(try_end),
			
			# Horse - no default option
			(try_begin),
				(eq, ":richhorse", 1),
				(ge, ":skill_riding", 3),
				(troop_get_slot, ":item_no", ccp_data, ":slot_richhorse"),
				(call_script, "script_ccp_add_item", ":item_no"),
			# (else_try),
				# (eq, ":richhorse", 1),
				# (val_add, ":gold", 150), # This is to compensate a player for losing their better horse due to not meeting the requirements.
				# (call_script, "script_ccp_add_item", "itm_ho_pla_sumpter_white"),
			(else_try),
				(eq, ":horse", 1),
				(ge, ":skill_riding", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_horse"),
				(call_script, "script_ccp_add_item", ":item_no"),
				#(display_message, "@Horse -> Settled for default."),
			(try_end),
			
			# Armor - defaults to cloth
			(try_begin),
				(eq, ":armor", 1),
				(ge, ":strength", 3),
				(troop_get_slot, ":item_no", ccp_data, ":slot_armor"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":dress", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_dress"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(troop_get_slot, ":item_no", ccp_data, ":slot_cloth"),
				(call_script, "script_ccp_add_item", ":item_no"),
				#(display_message, "@Armor -> Settled for default."),
			(try_end),
			
			# Melee Weapons - defaults to a dagger
			(try_begin),
				(eq, ":sword", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_sword"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":axe", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_axe"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":spear", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_spear"),
				(call_script, "script_ccp_add_item", ":item_no"),
				(troop_get_slot, ":item_no2", ccp_data, ":slot_sword"),
				(call_script, "script_ccp_add_item", ":item_no2"),
			(else_try),
				(eq, ":blunt", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_blunt"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":dagger", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_dagger"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(troop_get_slot, ":item_no", ccp_data, ":slot_dagger"),
				(call_script, "script_ccp_add_item", ":item_no"),
				#(display_message, "@Melee weapon -> Settled for default."),
			(try_end),
			
			# Ranged Weapons - no default option
			(try_begin),
				(eq, ":bow", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_bow"),
				# (try_begin),
					# (this_or_next|eq, ":item_no", "itm_we_vae_bow_hunting"),
					# (eq, ":item_no", "itm_we_khe_bow_red"),
					# (lt, ":skill_powerdraw", 2), # Filter - Prevent Khergits & Vaegir bow users from getting a bow they can't use.
					# (val_add, ":gold", 50),
					# (assign, ":item_no", "itm_we_nor_bow_hunting"),
				# (try_end),
				(call_script, "script_ccp_add_item", ":item_no"),
				(troop_get_slot, ":item_no", ccp_data, ":slot_arrow"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":throwing", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_throwing"),
				# (try_begin),
					# (this_or_next|eq, ":item_no", "itm_we_nor_axe_throw_light"),
					# (this_or_next|eq, ":item_no", "itm_we_sar_spear_javelin"),
					# (eq, ":item_no", "itm_we_swa_throw_darts"),
					# (lt, ":skill_powerthrow", 1), # Filter - Prevent Swadian thrown weapon users from getting a weapon they can't use.
					# (assign, ":item_no", "itm_we_vae_sword_throw_knives"),
				# (try_end),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":throwing_knives", 1),
				(call_script, "script_ccp_add_item", "itm_throwing_daggers"),
			(try_end),
			
			# Shield - no default option
			(try_begin),
				(eq, ":shield", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_shield"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(try_end),
			
			# Head gear - no default option
			(try_begin),
				(eq, ":helmet", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_helmet"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":ladyhelmet", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_ladyhelmet"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":hood", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_hood"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(try_end),
			
			# Hand gear - no default option
			(try_begin),
				(eq, ":gauntlets", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_gauntlets"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(try_end),
			
			# Footwear - defaults to poor boots
			(try_begin),
				(eq, ":richboots", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_richboots"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(eq, ":boots", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_boots"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(else_try),
				(troop_get_slot, ":item_no", ccp_data, ":slot_poorboots"),
				(call_script, "script_ccp_add_item", ":item_no"),
				#(display_message, "@Footwear -> Settled for default."),
			(try_end),
			
			# Additional gear - no default option
			(try_begin),
				(eq, ":trade1", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_trade1"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(try_end),
			# Additional gear - no default option
			(try_begin),
				(eq, ":trade2", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_trade2"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(try_end),
			# Additional gear - no default option
			(try_begin),
				(eq, ":instrument", 1),
				(troop_get_slot, ":item_no", ccp_data, ":slot_instrument"),
				(call_script, "script_ccp_add_item", ":item_no"),
			(try_end),
			
			(set_show_messages, 0),
			### UPDATE THE PLAYER'S STATS ###
			# Update abilties.
			(troop_raise_attribute, "trp_player",ca_charisma, ":charisma"),
			(troop_raise_attribute, "trp_player",ca_strength, ":strength"),
			(troop_raise_attribute, "trp_player",ca_intelligence, ":intelligence"),
			(troop_raise_attribute, "trp_player",ca_agility, ":agility"),
			
			# Update skills.
			(troop_raise_skill, "trp_player", skl_ironflesh, ":skill_ironflesh"),
			(troop_raise_skill, "trp_player", skl_power_strike, ":skill_powerstrike"),
			(troop_raise_skill, "trp_player", skl_power_throw, ":skill_powerthrow"),
			(troop_raise_skill, "trp_player", skl_power_draw, ":skill_powerdraw"),
			(troop_raise_skill, "trp_player", skl_weapon_master, ":skill_weaponmaster"),
			(troop_raise_skill, "trp_player", skl_shield, ":skill_shield"),
		    (troop_raise_skill, "trp_player", skl_athletics, ":skill_athletics"),
			(troop_raise_skill, "trp_player", skl_riding, ":skill_riding"),
			(troop_raise_skill, "trp_player", skl_horse_archery, ":skill_horsearchery"),
			(troop_raise_skill, "trp_player", skl_looting, ":skill_looting"),
			#(troop_raise_skill, "trp_player", skl_foraging, ":skill_foraging"),
			(troop_raise_skill, "trp_player", skl_trainer, ":skill_trainer"),
			(troop_raise_skill, "trp_player", skl_tracking, ":skill_tracking"),
			(troop_raise_skill, "trp_player", skl_tactics, ":skill_tactics"),
			(troop_raise_skill, "trp_player", skl_pathfinding, ":skill_pathfinding"),
			(troop_raise_skill, "trp_player", skl_spotting, ":skill_spotting"),
			(troop_raise_skill, "trp_player", skl_inventory_management, ":skill_inventorymanagement"),
			(troop_raise_skill, "trp_player", skl_wound_treatment, ":skill_woundtreatment"),
			(troop_raise_skill, "trp_player", skl_surgery, ":skill_surgery"),
		    (troop_raise_skill, "trp_player", skl_first_aid, ":skill_firstaid"),
			(troop_raise_skill, "trp_player", skl_engineer, ":skill_engineer"),
			(troop_raise_skill, "trp_player", skl_persuasion, ":skill_persuasion"),
			(troop_raise_skill, "trp_player", skl_prisoner_management, ":skill_prisonmanagement"),
			(troop_raise_skill, "trp_player", skl_leadership, ":skill_leadership"),
			(troop_raise_skill, "trp_player", skl_trade, ":skill_trade"),
			
			# Update proficiencies.
			(troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, ":prof_onehand"),
			(troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, ":prof_twohand"),
			(troop_raise_proficiency_linear, "trp_player", wpt_polearm, ":prof_polearm"),
			(troop_raise_proficiency_linear, "trp_player", wpt_archery, ":prof_archery"),
			(troop_raise_proficiency_linear, "trp_player", wpt_crossbow, ":prof_crossbow"),
			(troop_raise_proficiency_linear, "trp_player", wpt_throwing, ":prof_throwing"),
			
			# Update miscellaneous.
			(troop_set_slot, "trp_player", slot_troop_renown, ":renown"),
			(call_script, "script_change_player_honor", ":honor"),
			(troop_add_gold, "trp_player", ":gold"),
			
			# Give the player his equipment.
			(try_for_range, ":slot", ccp_item_storage_begin, ccp_item_storage_end),
				(troop_slot_ge, ccp_data, ":slot", 1), # Prevent invalid items.
				(troop_get_slot, ":item_no", ccp_data, ":slot"),
				(troop_add_item, "trp_player", ":item_no", 0),
			(try_end),
		
			# For smiths make sure they get a smithy in their starting town.  :smithy = 1
			(try_begin),
				(ge, ":smithy", 1),
				(assign, "$enterprise_production", "itm_tools"),
				(party_set_slot, "$g_encountered_party", slot_center_player_enterprise, "itm_tools"),
				(party_set_slot, "$g_encountered_party", slot_center_player_enterprise_days_until_complete, 7),
				(store_sub, ":current_town_order", "$current_town", towns_begin),
				(store_add, ":craftsman_troop", ":current_town_order", "trp_town_1_master_craftsman"),
				(troop_set_name, ":craftsman_troop", "str_master_smith"),
				(ge, DEBUG_CCP_general, 1),
				(str_store_party_name, s31, "$current_town"),
				(display_message, "@DEBUG (CCP): The player has bene given a smithy in the town of {s31}."),
			(try_end),
			
			# For nobles & sons of nobles make sure they get their lands in their starting town.  :lands = acres
			# (try_begin),
				# (ge, ":lands", 1),
				# (party_get_slot, ":acres_available", "$current_town", slot_town_acres),
				# (val_sub, ":acres_available", ":lands"),
				# (party_set_slot, "$current_town", slot_town_acres, ":acres_available"),
				# (party_set_slot, "$current_town", slot_player_acres, ":lands"),
				# (ge, DEBUG_CCP_general, 1),
				# (str_store_party_name, s31, "$current_town"),
				# (assign, reg31, ":lands"),
				# (display_message, "@DEBUG (CCP): The player has bene given {reg31} acres of land in the town of {s31}."),
			# (try_end),
			
			(set_show_messages, 1),
		(try_end),
	]),

# script_ccp_convert_trainer_to_training
# PURPOSE: In Silverstag v0.15 the trainer skill was disabled and the training skill created to avoid the hard-coded effects of trainer.
("ccp_convert_trainer_to_training",
	[
		(try_for_range, ":troop_no", 0, "trp_end_of_troops"),
			(store_skill_level, ":trainer_skill", "skl_training", ":troop_no"),
			(ge, ":trainer_skill", 1),
			(troop_set_skill, ":troop_no", "skl_training", 0),
			(troop_set_skill, ":troop_no", "skl_trainer", ":trainer_skill"),
			### DIAGNOSTIC+ ###
			# (is_between, ":troop_no", companions_begin, companions_end),
			# (assign, reg31, ":trainer_skill"),
			# (store_skill_level, reg32, "skl_trainer", ":troop_no"),
			# (str_store_troop_name, s31, ":troop_no"),
			# (display_message, "@DEBUG (Training): {s31} had {reg31} trainer skill.  Now has {reg32} trainer.", gpu_debug),
			### DIAGNOSTIC- ###
		(try_end),
	]),
("ccp_tester_settings",
	[
	# Update abilties.
		(troop_raise_attribute, "trp_player",ca_charisma, 50),
		(troop_raise_attribute, "trp_player",ca_strength, 50),
		(troop_raise_attribute, "trp_player",ca_intelligence, 50),
		(troop_raise_attribute, "trp_player",ca_agility, 50),
		
		# Update skills.
		(troop_raise_skill, "trp_player", skl_ironflesh, 10),
		(troop_raise_skill, "trp_player", skl_power_strike, 10),
		(troop_raise_skill, "trp_player", skl_power_throw, 10),
		(troop_raise_skill, "trp_player", skl_power_draw, 10),
		(troop_raise_skill, "trp_player", skl_weapon_master, 10),
		(troop_raise_skill, "trp_player", skl_shield, 10),
		(troop_raise_skill, "trp_player", skl_athletics, 10),
		(troop_raise_skill, "trp_player", skl_riding, 10),
		(troop_raise_skill, "trp_player", skl_horse_archery, 10),
		(troop_raise_skill, "trp_player", skl_looting, 10),
		#(troop_raise_skill, "trp_player", skl_foraging, ":skill_foraging"),
		(troop_raise_skill, "trp_player", skl_trainer, 10),
		(troop_raise_skill, "trp_player", skl_tracking, 10),
		(troop_raise_skill, "trp_player", skl_tactics, 10),
		(troop_raise_skill, "trp_player", skl_pathfinding,10),
		(troop_raise_skill, "trp_player", skl_spotting, 10),
		(troop_raise_skill, "trp_player", skl_inventory_management, 10),
		(troop_raise_skill, "trp_player", skl_wound_treatment, 10),
		(troop_raise_skill, "trp_player", skl_surgery, 10),
		(troop_raise_skill, "trp_player", skl_first_aid, 10),
		(troop_raise_skill, "trp_player", skl_engineer, 10),
		(troop_raise_skill, "trp_player", skl_persuasion, 10),
		(troop_raise_skill, "trp_player", skl_prisoner_management, 10),
		(troop_raise_skill, "trp_player", skl_leadership, 10),
		(troop_raise_skill, "trp_player", skl_trade, 10),
		
		# Update proficiencies.
		(troop_raise_proficiency_linear, "trp_player", wpt_one_handed_weapon, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_two_handed_weapon, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_polearm, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_archery, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_crossbow, 350),
		(troop_raise_proficiency_linear, "trp_player", wpt_throwing, 350),
		
		# Update miscellaneous.
		(troop_add_gold, "trp_player", 250000),
		
	])




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
