# Companion Management System (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	

###########################################################################################################################
#####                                         UI HANDLING & UTILITY SCRIPTS                                           #####
###########################################################################################################################

# script_cci_game_start
# PURPOSE: Initializes the Custom Commissioning Items kit.
# EXAMPLE: (call_script, "script_cci_game_start"), # cci_scripts.py
("cci_game_start",
	[
		## TOWNS - NPC NAMES
		(try_for_range, ":center_no", towns_begin, towns_end),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(store_sub, ":center_offset", ":center_no", towns_begin),
			# Royal Blacksmiths
			(store_add, ":troop_no", ":center_offset", cci_town_blacksmiths_begin),
			(call_script, "script_common_rename_troop", ":troop_no", ":faction_no", SCRT_FULL),
		(try_end),
		
		## CASTLES - NPC NAMES
		(try_for_range, ":center_no", castles_begin, castles_end),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(store_sub, ":center_offset", ":center_no", castles_begin),
			# Royal Blacksmiths
			(store_add, ":troop_no", ":center_offset", cci_castle_blacksmiths_begin),
			(call_script, "script_common_rename_troop", ":troop_no", ":faction_no", SCRT_FULL),
		(try_end),
		
		## RESET THE ITEM COMMISSIONING QUEUE.
		(call_script, "script_cci_clear_all_commission_entries"),
		
		## CLEAR THE EVENT LOG.
		# Wipe log arrays.
		(try_for_range, ":entry_no", 0, CCI_EVENT_LOG_MAXIMUM_ENTRIES),
			(troop_set_slot, CCI_LOG_EVENT,    ":entry_no", CCI_EVENT_UNDEFINED),
			(troop_set_slot, CCI_LOG_ITEM_NO,  ":entry_no", 0),
			(troop_set_slot, CCI_LOG_IMOD,     ":entry_no", 0),
			(troop_set_slot, CCI_LOG_LOCATION, ":entry_no", 0),
			(troop_set_slot, CCI_LOG_DATE, ":entry_no", 0),
		(try_end),
	]),
	
# script_cci_create_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate this code for each window.
("cci_create_mode_switching_buttons",
    [
		### COMMON ELEMENTS ###
		(assign, "$gpu_storage", CCI_OBJECTS),
		(assign, "$gpu_data",    CCI_OBJECTS),
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		# Setup an initial false value for objects so if they don't get loaded they aren't 0's.
		(try_for_range, ":slot_no", cci_obj_main_title, cci_obj_container_1),
			(store_add, ":value", ":slot_no", 1234),
			(troop_set_slot, CCI_OBJECTS, ":slot_no", ":value"),
		(try_end),
		
		## CONTAINERS ##
		(call_script, "script_gpu_container_heading", 50, 80, 175, 505, cci_obj_container_1),
			
			## BUTTONS ##
			(assign, ":x_buttons", 0), # 90 
			(assign, ":y_button_step", 55),
			(assign, ":pos_y", 420),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_has_royal_forge, cis_built),
				(party_slot_eq, "$current_town", slot_town_lord, "trp_player"),
				
				## OBJ - BUTTON - ARTISAN INFO
				(str_store_string, s21, "@Artisan Crafter "),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", cci_obj_button_artisan), ### ARTISAN INFO ###
				(val_sub, ":pos_y", 10),
				(call_script, "script_cci_get_artisan_id", "$current_town"),
				(str_store_troop_name, s22, reg1),
				(str_store_string, s21, "@({s22})"),
				(call_script, "script_gpu_create_text_label", "str_hub_s21", 75, ":pos_y", 0, gpu_center), # 680
				(call_script, "script_gpu_resize_object", 0, 75),
				(overlay_set_color, reg1, gpu_gray),
				(val_sub, ":pos_y", ":y_button_step"),
				
				## OBJ - BUTTON - REPAIR ITEMS
				(str_store_string, s21, "@Repair Items "),
				(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", cci_obj_button_repair_items), ### REPAIR ITEMS ###
				(call_script, "script_cci_get_artisan_id", "$current_town"),
				(assign, ":troop_no", reg1),
				(troop_get_inventory_capacity, ":inv_capacity", ":troop_no"),
				(assign, ":total_items", 0),
				(try_for_range, ":inv_slot", 0, ":inv_capacity"),
					(troop_get_inventory_slot, ":item_no", ":troop_no", ":inv_slot"),
					(ge, ":item_no", 1),
					(troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":inv_slot"),
					(neq, ":imod", imod_plain),
					## WINDYPLAINS+ ## - Prevent items repaired beyond plain quality from being counted.
					(neq, ":imod", imod_fine),
					(neq, ":imod", imod_well_made),
					(neq, ":imod", imod_sharp),
					(neq, ":imod", imod_balanced),
					(neq, ":imod", imod_tempered),
					(neq, ":imod", imod_deadly),
					(neq, ":imod", imod_exquisite),
					(neq, ":imod", imod_masterwork),
					(neq, ":imod", imod_heavy),
					(neq, ":imod", imod_strong),
					(neq, ":imod", imod_powerful),
					(neq, ":imod", imod_sturdy),
					(neq, ":imod", imod_thick),
					(neq, ":imod", imod_hardened),
					(neq, ":imod", imod_reinforced),
					(neq, ":imod", imod_superb),
					(neq, ":imod", imod_lordly),
					(neq, ":imod", imod_spirited),
					(neq, ":imod", imod_champion),
					## WINDYPLAINS- ##
					(val_add, ":total_items", 1),
				(try_end),
				(try_begin),
					(ge, ":total_items", 1),
					(store_add, ":pos_y_temp", ":pos_y", 11),
					(assign, reg21, ":total_items"),
					(str_store_string, s21, "@({reg21})"),
					(call_script, "script_gpu_create_text_label", "str_hub_s21", 130, ":pos_y_temp", 0, gpu_left), # 680
					# (call_script, "script_gpu_resize_object", 0, 75),
					(overlay_set_color, reg1, gpu_gray),
				(try_end),
				(val_sub, ":pos_y", ":y_button_step"),
				
			(try_end),
			(str_store_string, s21, "@Commission Item "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", cci_obj_button_commission_item), ### COMMISSION ITEM ###
			
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@List All "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", cci_obj_button_list_commissions), ### LIST ALL COMMISSIONS ###
			
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@Emblem Options "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", cci_obj_button_emblem_options), ### EMBLEM OPTIONS ###
			
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@Event Log "),
			(call_script, "script_gpu_create_button", "str_hub_s21", ":x_buttons", ":pos_y", cci_obj_button_event_log), ### EVENT LOG ###
			
			# (try_begin),
				# (ge, DEBUG_GARRISON, 1),
				# (is_presentation_active, "prsnt_garrison_queue"),
				# (val_sub, ":pos_y", ":y_button_step"),
				# (val_sub, ":pos_y", 20),
				# (call_script, "script_gpu_create_text_label", "str_grt_debug_advance_label", ":x_buttons", ":pos_y", 0, gpu_left),
				# (call_script, "script_gpu_create_text_label", "str_grt_debug_advance_label", ":x_buttons", ":pos_y", 0, gpu_left),
				# (val_sub, ":pos_y", 40),
				# (call_script, "script_gpu_create_button", "str_grt_debug_advance", ":x_buttons", ":pos_y", grt_obj_button_debug_advance),
			# (try_end),
			
		(set_container_overlay, -1),
		(call_script, "script_gpu_create_mesh", "mesh_button_up", 55, 35, 350, 500),
		(str_store_string, s21, "@Done"),
		(call_script, "script_gpu_create_button", "str_hub_s21", 65, 40, cci_obj_button_done),
	]),
	
# script_cci_handle_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate the code to handle their functionality for each window.
("cci_handle_mode_switching_buttons",
    [
		(store_script_param, ":object", 1),
		(store_script_param, ":value", 2),
		(assign, reg1, ":value"), # So it won't be whined about.
		
		# cci_obj_button_done               = 2
		# cci_obj_button_general            = 4
		# cci_obj_button_commission_item    = 5
		# cci_obj_button_list_commissions   = 6
		
		### COMMON ELEMENTS ###
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_done, ":object"),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(assign, "$cci_mode", CCI_STARTING_SCREEN),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : ARTISAN CRAFTER #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_artisan, ":object"),
			(assign, "$cci_mode", CCI_MODE_ARTISAN_INFO),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_cci_switch_modes"),
			
		(else_try), ####### BUTTON : REPAIR ITEMS #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_repair_items, ":object"),
			(assign, "$cci_mode", CCI_MODE_REPAIR_ITEMS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_cci_switch_modes"),
			
		(else_try), ####### BUTTON : COMMISSION AN ITEM #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_commission_item, ":object"),
			(assign, "$cci_mode", CCI_MODE_COMMISSION_ITEM),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_cci_switch_modes"),
			
		(else_try), ####### BUTTON : LIST ALL COMMISSIONS #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_list_commissions, ":object"),
			(assign, "$cci_mode", CCI_MODE_LIST_ALL_COMMISSIONS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_cci_switch_modes"),
			
		(else_try), ####### BUTTON : EVENT LOG #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_event_log, ":object"),
			(assign, "$cci_mode", CCI_MODE_EVENT_LOG),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_cci_switch_modes"),
			
		(else_try), ####### BUTTON : EMBLEM OPTIONS #######
			(troop_slot_eq, CCI_OBJECTS, cci_obj_button_emblem_options, ":object"),
			(assign, "$cci_mode", CCI_MODE_EMBLEM_OPTIONS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_cci_switch_modes"),
			
		(try_end),
	]),
	
# script_cci_describe_imod_to_s1
# PURPOSE: Utility script for translating a numerical IMOD value into a descriptive name.
# EXAMPLE: (call_script, "script_cci_describe_imod_to_s1", ":imod", ":caps"), # cci_scripts.py
("cci_describe_imod_to_s1",
    [
		(store_script_param, ":imod", 1),
		(store_script_param, ":caps", 2),
		
		(try_begin),
			(eq, ":imod", imod_plain),
			(str_store_string, s1, "@plain"),
			(str_store_string, s2, "@100"),
		(else_try),
			(eq, ":imod", imod_cracked),
			(str_store_string, s1, "@cracked"),
			(str_store_string, s2, "@50"),
		(else_try),
			(eq, ":imod", imod_rusty),
			(str_store_string, s1, "@rusty"),
			(str_store_string, s2, "@55"),
		(else_try),
			(eq, ":imod", imod_bent),
			(str_store_string, s1, "@bent"),
			(str_store_string, s2, "@65"),
		(else_try),
			(eq, ":imod", imod_chipped),
			(str_store_string, s1, "@chipped"),
			(str_store_string, s2, "@72"),
		(else_try),
			(eq, ":imod", imod_battered),
			(str_store_string, s1, "@battered"),
			(str_store_string, s2, "@75"),
		(else_try),
			(eq, ":imod", imod_poor),
			(str_store_string, s1, "@poor"),
			(str_store_string, s2, "@80"),
		(else_try),
			(eq, ":imod", imod_crude),
			(str_store_string, s1, "@crude"),
			(str_store_string, s2, "@83"),
		(else_try),
			(eq, ":imod", imod_old),
			(str_store_string, s1, "@old"),
			(str_store_string, s2, "@86"),
		(else_try),
			(eq, ":imod", imod_cheap),
			(str_store_string, s1, "@cheap"),
			(str_store_string, s2, "@90"),
		(else_try),
			(eq, ":imod", imod_fine),
			(str_store_string, s1, "@fine"),
			(str_store_string, s2, "@190"),
		(else_try),
			(eq, ":imod", imod_well_made),
			(str_store_string, s1, "@well made"),
			(str_store_string, s2, "@250"),
		(else_try),
			(eq, ":imod", imod_sharp),
			(str_store_string, s1, "@sharp"),
			(str_store_string, s2, "@160"),
		(else_try),
			(eq, ":imod", imod_balanced),
			(str_store_string, s1, "@balanced"),
			(str_store_string, s2, "@350"),
		(else_try),
			(eq, ":imod", imod_tempered),
			(str_store_string, s1, "@tempered"),
			(str_store_string, s2, "@670"),
		(else_try),
			(eq, ":imod", imod_deadly),
			(str_store_string, s1, "@deadly"),
			(str_store_string, s2, "@850"),
		(else_try),
			(eq, ":imod", imod_exquisite),
			(str_store_string, s1, "@exquisite"),
			(str_store_string, s2, "@1450"),
		(else_try),
			(eq, ":imod", imod_masterwork),
			(str_store_string, s1, "@masterwork"),
			(str_store_string, s2, "@1750"),
		(else_try),
			(eq, ":imod", imod_heavy),
			(str_store_string, s1, "@heavy"),
			(str_store_string, s2, "@190"),
		(else_try),
			(eq, ":imod", imod_strong),
			(str_store_string, s1, "@strong"),
			(str_store_string, s2, "@490"),
		(else_try),
			(eq, ":imod", imod_powerful),
			(str_store_string, s1, "@powerful"),
			(str_store_string, s2, "@320"),
		(else_try),
			(eq, ":imod", imod_tattered),
			(str_store_string, s1, "@tattered"),
			(str_store_string, s2, "@50"),
		(else_try),
			(eq, ":imod", imod_ragged),
			(str_store_string, s1, "@ragged"),
			(str_store_string, s2, "@70"),
		(else_try),
			(eq, ":imod", imod_rough),
			(str_store_string, s1, "@rough"),
			(str_store_string, s2, "@60"),
		(else_try),
			(eq, ":imod", imod_sturdy),
			(str_store_string, s1, "@sturdy"),
			(str_store_string, s2, "@170"),
		(else_try),
			(eq, ":imod", imod_thick),
			(str_store_string, s1, "@thick"),
			(str_store_string, s2, "@260"),
		(else_try),
			(eq, ":imod", imod_hardened),
			(str_store_string, s1, "@hardened"),
			(str_store_string, s2, "@390"),
		(else_try),
			(eq, ":imod", imod_reinforced),
			(str_store_string, s1, "@reinforced"),
			(str_store_string, s2, "@650"),
		(else_try),
			(eq, ":imod", imod_superb),
			(str_store_string, s1, "@superb"),
			(str_store_string, s2, "@250"),
		(else_try),
			(eq, ":imod", imod_lordly),
			(str_store_string, s1, "@lordly"),
			(str_store_string, s2, "@1150"),
		(else_try),
			(eq, ":imod", imod_lame),
			(str_store_string, s1, "@lame"),
			(str_store_string, s2, "@40"),
		(else_try),
			(eq, ":imod", imod_swaybacked),
			(str_store_string, s1, "@swaybacked"),
			(str_store_string, s2, "@60"),
		(else_try),
			(eq, ":imod", imod_stubborn),
			(str_store_string, s1, "@stubborn"),
			(str_store_string, s2, "@90"),
		(else_try),
			(eq, ":imod", imod_timid),
			(str_store_string, s1, "@timid"),
			(str_store_string, s2, "@180"),
		(else_try),
			(eq, ":imod", imod_meek),
			(str_store_string, s1, "@meek"),
			(str_store_string, s2, "@180"),
		(else_try),
			(eq, ":imod", imod_spirited),
			(str_store_string, s1, "@spirited"),
			(str_store_string, s2, "@650"),
		(else_try),
			(eq, ":imod", imod_champion),
			(str_store_string, s1, "@champion"),
			(str_store_string, s2, "@1450"),
		(else_try),
			(eq, ":imod", imod_fresh),
			(str_store_string, s1, "@fresh"),
			(str_store_string, s2, "@100"),
		(else_try),
			(eq, ":imod", imod_day_old),
			(str_store_string, s1, "@day old"),
			(str_store_string, s2, "@100"),
		(else_try),
			(eq, ":imod", imod_two_day_old),
			(str_store_string, s1, "@two day old"),
			(str_store_string, s2, "@90"),
		(else_try),
			(eq, ":imod", imod_smelling),
			(str_store_string, s1, "@smelling"),
			(str_store_string, s2, "@40"),
		(else_try),
			(eq, ":imod", imod_rotten),
			(str_store_string, s1, "@rotten"),
			(str_store_string, s2, "@5"),
		(else_try),
			(eq, ":imod", imod_large_bag),
			(str_store_string, s1, "@large bag"),
			(str_store_string, s2, "@190"),
		(else_try),
			(str_store_string, s1, "@undefined"),
			(str_store_string, s2, "@100"),
		(try_end),
		
		(try_begin),
			(eq, ":caps", 1),
			(str_store_substring, s5, s1, 0, 1),  # Get the first character of the description.
			(str_store_upper, s3, s5),            # Capitalize the first character.
			(str_store_substring, s4, s1, 1),     # Get the rest of the description minus the first character.
			(str_store_string, s1, "@{s3}{s4}"),  # Put it back together into s1.
			# Special Cases
			(try_begin),
				(eq, ":imod", imod_well_made),
				(str_store_string, s1, "@Well Made"),
			(else_try),
				(eq, ":imod", imod_day_old),
				(str_store_string, s1, "@Day Old"),
			(else_try),
				(eq, ":imod", imod_two_day_old),
				(str_store_string, s1, "@Two Day Old"),
			(else_try),
				(eq, ":imod", imod_large_bag),
				(str_store_string, s1, "@Large Bag"),
			(try_end),
		(try_end),
		
	]),
	
# script_cf_cci_imod_appropriate_for_item
# PURPOSE: Utility script that filters out inappropriate item modifiers given an item type.
# EXAMPLE: (call_script, "script_cf_cci_imod_appropriate_for_item", ":item_type", ":imod"), # cci_scripts.py
("cf_cci_imod_appropriate_for_item",
    [
		(store_script_param, ":item_group", 1),
		(store_script_param, ":imod", 2),
		
		(assign, ":continue", 1),
		## FILTER - IMODs that are always blocked.
		(try_begin),
			# Inactive IMODs.  These have no game effects so they're removed for now.
			(this_or_next|eq, ":imod", imod_superb),
			(this_or_next|eq, ":imod", imod_well_made),
			(this_or_next|eq, ":imod", imod_sharp),
			(this_or_next|eq, ":imod", imod_deadly),
			(this_or_next|eq, ":imod", imod_exquisite),
			(this_or_next|eq, ":imod", imod_powerful),
			# Behavioral IMODs.  Not applicable.
			(this_or_next|eq, ":imod", imod_lame),
			(this_or_next|eq, ":imod", imod_swaybacked),
			(this_or_next|eq, ":imod", imod_stubborn),
			(this_or_next|eq, ":imod", imod_timid),
			(this_or_next|eq, ":imod", imod_meek),
			# Below Quality IMODs.  No one would craft this.
			(this_or_next|eq, ":imod", imod_tattered),
			(this_or_next|eq, ":imod", imod_ragged),
			(this_or_next|eq, ":imod", imod_rough),
			(this_or_next|eq, ":imod", imod_cracked),
			(this_or_next|eq, ":imod", imod_rusty),
			(this_or_next|eq, ":imod", imod_bent),
			(this_or_next|eq, ":imod", imod_chipped),
			(this_or_next|eq, ":imod", imod_battered),
			(this_or_next|eq, ":imod", imod_poor),
			(this_or_next|eq, ":imod", imod_crude),
			(this_or_next|eq, ":imod", imod_old),
			(this_or_next|eq, ":imod", imod_cheap),
			# Freshness IMODs.  Not Applicable to Equipment.
			(this_or_next|eq, ":imod", imod_fresh),
			(this_or_next|eq, ":imod", imod_day_old),
			(this_or_next|eq, ":imod", imod_two_day_old),
			(this_or_next|eq, ":imod", imod_smelling),
			(eq, ":imod", imod_rotten),
			(assign, ":continue", 0),
		(try_end),
		(eq, ":continue", 1),
		
		(assign, ":continue", 0),
		(try_begin),
			### WEAPON FILTER ###
			(this_or_next|eq, ":item_group", CCI_GROUP_ONE_HANDED), # One-Handed
			(this_or_next|eq, ":item_group", CCI_GROUP_TWO_HANDED), # Two-Handed
			(this_or_next|eq, ":item_group", CCI_GROUP_POLEARMS), # Polearm
			(eq, ":item_group", CCI_GROUP_RANGED_WEAPONS), # Ranged Weapons
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_strong),
			(this_or_next|eq, ":imod", imod_heavy),
			(this_or_next|eq, ":imod", imod_masterwork),
			(this_or_next|eq, ":imod", imod_tempered),
			(this_or_next|eq, ":imod", imod_balanced),
			(this_or_next|eq, ":imod", imod_fine),
			(eq, ":imod", imod_plain),
			(neq, ":imod", imod_large_bag),
			(assign, ":continue", 1),
			
		(else_try),
			### AMMUNITION FILTER ###
			(eq, ":item_group", CCI_GROUP_AMMUNITION), # Ammunition
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_large_bag),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(else_try),
			### SHIELD FILTER ###
			(eq, ":item_group", CCI_GROUP_SHIELDS), # Shields
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_lordly),
			(this_or_next|eq, ":imod", imod_reinforced),
			(this_or_next|eq, ":imod", imod_hardened),
			(this_or_next|eq, ":imod", imod_thick),
			(this_or_next|eq, ":imod", imod_sturdy),
			(this_or_next|eq, ":imod", imod_heavy),
			(this_or_next|eq, ":imod", imod_masterwork),
			(this_or_next|eq, ":imod", imod_balanced),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(else_try),
			### ARMOR FILTER ###
			(this_or_next|eq, ":item_group", CCI_GROUP_HELMETS), # Head
			(this_or_next|eq, ":item_group", CCI_GROUP_BODY), # Body
			(this_or_next|eq, ":item_group", CCI_GROUP_BOOTS), # Boots
			(eq, ":item_group", CCI_GROUP_HANDS), # Hands
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_lordly),
			(this_or_next|eq, ":imod", imod_reinforced),
			(this_or_next|eq, ":imod", imod_hardened),
			(this_or_next|eq, ":imod", imod_thick),
			(this_or_next|eq, ":imod", imod_sturdy),
			(this_or_next|eq, ":imod", imod_heavy),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(else_try),
			### MOUNTS FILTER ###
			(eq, ":item_group", CCI_GROUP_MOUNTS), # Shields
			# Valid IMODs.
			(this_or_next|eq, ":imod", imod_champion),
			(this_or_next|eq, ":imod", imod_spirited),
			(this_or_next|eq, ":imod", imod_lordly),
			(this_or_next|eq, ":imod", imod_sturdy),
			(this_or_next|eq, ":imod", imod_heavy),
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(else_try),
			### MOUNTS FILTER ###
			(eq, ":item_group", CCI_GROUP_BOOKS), # Shields
			# Valid IMODs.
			(eq, ":imod", imod_plain),
			(assign, ":continue", 1),
			
		(try_end),
		
		(eq, ":continue", 1),
		
	]),
	
	
###########################################################################################################################
#####                                             COMMISSIONING SCRIPTS                                               #####
###########################################################################################################################

# script_cci_clear_commission_entry
# PURPOSE: Utility script for clearing out a single entry in all commission arrays.
# EXAMPLE: (call_script, "script_cci_clear_commission_entry", ":entry_no", ":tidy_queue"), # cci_scripts.py
("cci_clear_commission_entry",
    [
		(store_script_param, ":entry_no", 1),   # Slot value
		(store_script_param, ":tidy_queue", 2), # Boolean value
		
		(troop_set_slot, CCI_ARRAY_ITEM_NO, ":entry_no", -1),
		(troop_set_slot, CCI_ARRAY_IMOD, ":entry_no", -1),
		(troop_set_slot, CCI_ARRAY_STATUS, ":entry_no", -1),
		(troop_set_slot, CCI_ARRAY_COST, ":entry_no", -1),
		(troop_set_slot, CCI_ARRAY_LOCATION, ":entry_no", -1),
		
		## Tidy the Commissioning Queue
		(try_begin),
			(eq, ":tidy_queue", 1),
			(try_for_range, ":slot_no", ":entry_no", CCI_GOBAL_COMMISSION_LIMIT),
				## Get data from the next slot down.
				(store_add, ":next_slot", ":slot_no", 1),
				(neg|troop_slot_eq, CCI_ARRAY_ITEM_NO, ":next_slot", 0), # Prevent dragging 0's from the last out of bounds into the list.
				(troop_get_slot, ":item_no", CCI_ARRAY_ITEM_NO, ":next_slot"),
				(troop_get_slot, ":imod", CCI_ARRAY_IMOD, ":next_slot"),
				(troop_get_slot, ":initial_price", CCI_ARRAY_COST, ":next_slot"),
				(troop_get_slot, ":cost", CCI_ARRAY_STATUS, ":next_slot"),
				(troop_get_slot, ":center_no", CCI_ARRAY_LOCATION, ":next_slot"),
				(troop_get_slot, ":days_abandoned", CCI_ARRAY_ABANDON_TIMER, ":next_slot"),
				## Put that data into this currently empty slot.
				(troop_set_slot, CCI_ARRAY_ITEM_NO, ":slot_no", ":item_no"),
				(troop_set_slot, CCI_ARRAY_IMOD, ":slot_no", ":imod"),
				(troop_set_slot, CCI_ARRAY_STATUS, ":slot_no", ":cost"),
				(troop_set_slot, CCI_ARRAY_COST, ":slot_no", ":initial_price"),
				(troop_set_slot, CCI_ARRAY_LOCATION, ":slot_no", ":center_no"),
				(troop_set_slot, CCI_ARRAY_ABANDON_TIMER, ":slot_no", ":days_abandoned"),
				
			(try_end), # FIXED LOOP
			
		(try_end),
	]),
	
# script_cci_clear_all_commission_entries
# PURPOSE: Utility script initialize all commision arrays.
# EXAMPLE: (call_script, "script_cci_clear_all_commission_entries"), # cci_scripts.py
("cci_clear_all_commission_entries",
    [
		(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
			(call_script, "script_cci_clear_commission_entry", ":slot_no", 0),
		(try_end),
	]),
	
# script_cci_get_number_of_active_commissions
# PURPOSE: Counts how many global and local commissions exist and return these values as they're used in a few locations.
# EXAMPLE: (call_script, "script_cci_get_number_of_active_commissions"), # cci_scripts.py
("cci_get_number_of_active_commissions",
    [
		# Find the next available slot after all current commissions.
		(assign, ":global_commissions", 0),
		(assign, ":local_commissions", 0),
		(assign, ":local_abandonments", 0),
		(assign, ":total_locations", 0),
		
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(party_set_slot, ":center_no", slot_center_commission_counter, 0),
		(try_end),
		
		(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
			(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 0), # An item is commissioned and completed or in progress.
			(store_add, ":global_commissions", ":slot_no", 1),
			(try_begin),
				(troop_slot_eq, CCI_ARRAY_LOCATION, ":slot_no", "$current_town"), # An item is commissioned in this location.
				(val_add, ":local_commissions", 1),
				(troop_slot_ge, CCI_ARRAY_ABANDON_TIMER, ":slot_no", 1), # An item is commissioned in this location.
				(neg|party_slot_ge, "$current_town", slot_center_has_royal_forge, cis_built), ## Royal Blacksmith prevents abandonment.
				(val_add, ":local_abandonments", 1),
			(try_end),
			(try_begin),
				(troop_get_slot, ":center_no", CCI_ARRAY_LOCATION, ":slot_no"),
				(party_slot_eq, ":center_no", slot_center_commission_counter, 0),
				(party_set_slot, ":center_no", slot_center_commission_counter, 1),
				(val_add, ":total_locations", 1),
			(try_end),
		(try_end),
		
		(assign, reg1, ":global_commissions"),
		(assign, reg2, ":local_commissions"),
		(assign, reg3, ":local_abandonments"),
		(assign, reg4, ":total_locations"),
	]),
	
# script_cci_get_queue_delay_for_center
# PURPOSE: Tallies up how much time is needed to complete every previous commission at a center before the one requested will be worked.
# EXAMPLE: (call_script, "script_cci_get_queue_delay_for_center", ":center_no", ":commission_no"), # cci_scripts.py
("cci_get_queue_delay_for_center",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":commission_no", 2),
		
		# Find the next available slot after all current commissions.
		(assign, ":current_commission", 0),
		(assign, ":total_price", 0),
		(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
			(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 0), # An item is commissioned and completed or in progress.
			(troop_slot_eq, CCI_ARRAY_LOCATION, ":slot_no", ":center_no"), # An item is commissioned in this location.
			(val_add, ":current_commission", 1),
			(le, ":current_commission", ":commission_no"),
			(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 1), # An item is in progress.
			(troop_get_slot, ":remaining_price", CCI_ARRAY_STATUS, ":slot_no"),
			(val_add, ":total_price", ":remaining_price"),
		(try_end),
		
		## If you have CCI_SETTING_WORKDOWN_METHOD set to CCI_METHOD_PARALLEL then set the total_price to 0 to ignore previous commissions.
		# (try_begin),
			# (eq, CCI_SETTING_WORKDOWN_METHOD, CCI_METHOD_PARALLEL),
			# (assign, ":total_price", 0),
		# (try_end),
		
		(assign, reg1, ":total_price"),
	]),
	
# script_cci_add_new_commission
# PURPOSE: Add a new commission if an opening is available.
# EXAMPLE: (call_script, "script_cci_add_new_commission", ":center_no", ":item_no", ":imod"), # cci_scripts.py
("cci_add_new_commission",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":item_no", 2),
		(store_script_param, ":imod", 3),
		
		# Find the next available slot after all current commissions.
		(assign, ":empty_slot", -1),
		(assign, ":local_commissions", 0),
		(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
			(try_begin),
				(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 0), # An item is commissioned and completed or in progress.
				(try_begin),
					(troop_slot_eq, CCI_ARRAY_LOCATION, ":slot_no", ":center_no"), # An item is commissioned in this location.
					(val_add, ":local_commissions", 1),
				(try_end),
			(else_try),
				(troop_slot_eq, CCI_ARRAY_STATUS, ":slot_no", -1), # No commission is currently requested in this slot.
				(eq, ":empty_slot", -1), # We haven't already found a new slot.
				(assign, ":empty_slot", ":slot_no"),
				### DIAGNOSTIC+ ###
				(try_begin),
					(ge, DEBUG_CCI, 1),
					(assign, reg31, ":empty_slot"),
					(display_message, "@DEBUG (CCI): New commission request stored to slot #{reg31}.", gpu_debug),
				(try_end),
				### DIAGNOSTIC- ###
			(try_end),
		(try_end),
		
		(assign, ":commission_added", 0),
		(try_begin),
			# FILTER - Prevent adding a commission if the global limit has been reached.
			(eq, ":empty_slot", -1),
			(display_message, "@WARNING - Commission cannot be added due to maximum limit of active commissions reached.", gpu_red),
		(else_try),
			# FILTER - Prevent adding a commission if the local limit has been reached.
			(ge, ":local_commissions", CCI_LOCAL_COMMISSION_LIMIT),
			(str_store_party_name, s21, ":center_no"),
			(display_message, "@WARNING - Commission cannot be added due to maximum limit of commissions in {s21} has been reached.", gpu_red),
		(else_try),
			# ADD COMMISSION
			(call_script, "script_cci_get_commission_price", ":item_no", ":imod"),
			(assign, ":price", reg1),
			(troop_set_slot, CCI_ARRAY_ITEM_NO,       ":empty_slot", ":item_no"),
			(troop_set_slot, CCI_ARRAY_IMOD,          ":empty_slot", ":imod"),
			(troop_set_slot, CCI_ARRAY_STATUS,        ":empty_slot", ":price"),
			(troop_set_slot, CCI_ARRAY_COST,          ":empty_slot", ":price"),
			(troop_set_slot, CCI_ARRAY_LOCATION,      ":empty_slot", ":center_no"),
			(troop_set_slot, CCI_ARRAY_ABANDON_TIMER, ":empty_slot", 0),
			(assign, ":commission_added", 1),
			
			## DISPLAY ADDITION
			(assign, reg21, ":price"),
			(str_store_item_name, s21, ":item_no"),
			(str_store_party_name, s22, ":center_no"),
			(call_script, "script_cci_describe_imod_to_s1", ":imod", 0),
			(display_message, "@A {s1} {s21} has been commissioned in {s22} for {reg21} denars.", gpu_green),
			
			## CHARGE THE PLAYER
			(store_mul, ":upfront_cost", ":price", CCI_UPFRONT_COST),
			(val_div, ":upfront_cost", 100),
			(call_script, "script_diplomacy_treasury_withdraw_funds", ":upfront_cost", ":center_no", FUND_FROM_EITHER), # diplomacy_scripts.py
			
			### METRICS+ ### - MONEY SPENT ON COMMISSIONS
			(troop_get_slot, ":money_spent", METRICS_DATA, metrics_commissions_money_spent),
			(val_add, ":money_spent", ":upfront_cost"),
			(troop_set_slot, METRICS_DATA, metrics_commissions_money_spent, ":money_spent"),
			(try_begin),
				(eq, "$enable_metrics", 1),
				(troop_get_slot, reg31, METRICS_DATA, metrics_commissions_money_spent),
				(store_sub, reg32, reg31, 1),
				(assign, reg33, ":upfront_cost"),
				(display_message, "@METRIC (Commissions): You have spent {reg31} denar{reg32?s:} on commissions. (+{reg33})", gpu_debug),
			(try_end),
			### METRICS- ###
			
			### METRICS+ ### - TOTAL COMMISSIONS
			(troop_get_slot, ":total_requests", METRICS_DATA, metrics_commissions_total_requests),
			(val_add, ":total_requests", 1),
			(troop_set_slot, METRICS_DATA, metrics_commissions_total_requests, ":total_requests"),
			(try_begin),
				(eq, "$enable_metrics", 1),
				(troop_get_slot, reg31, METRICS_DATA, metrics_commissions_total_requests),
				(store_sub, reg32, reg31, 1),
				(display_message, "@METRIC (Commissions): You have requested a total of {reg31} commission{reg32?s:}.", gpu_debug),
			(try_end),
			### METRICS- ###
		(try_end),
		
		(assign, reg1, ":commission_added"),
	]),
	
# script_cci_get_commission_price
# PURPOSE: Return the price for requesting this item be commissioned to reg1.
# EXAMPLE: (call_script, "script_cci_get_commission_price", ":item_no", ":imod"), # cci_scripts.py
("cci_get_commission_price",
    [
		(store_script_param, ":item_no", 1),
		(store_script_param, ":imod", 2),
		
		# Get the base value of this item with this item modifier.
		(call_script, "script_cms_get_item_value_with_imod", ":item_no", ":imod", CMS_AUTO_LOOTING),
		(assign, ":base_value", reg0),
		(val_div, ":base_value", 100),
		
		# Add in markup cost for commissioning an item.  Setting found in cci_constants.py
		(store_mul, ":cost", ":base_value", CCI_MARKUP_PERCENTAGE),
		(val_div, ":cost", 100),
		
		(assign, reg1, ":cost"),
	]),
	
	
###########################################################################################################################
#####                                            CRAFTING ARTISAN SCRIPTS                                             #####
###########################################################################################################################

# script_cci_get_artisan_id
# PURPOSE: This returns the troop # for the artisan attached to a specific center.
# EXAMPLE: (call_script, "script_cci_get_artisan_id", ":center_no"), # cci_scripts.py
("cci_get_artisan_id",
    [
		(store_script_param, ":center_no", 1),
		
		(try_begin),
			(party_slot_eq, ":center_no", slot_party_type, spt_town),
			(store_sub, ":center_offset", ":center_no", towns_begin),
			(store_add, ":troop_no", ":center_offset", cci_town_blacksmiths_begin),
		(else_try),
			(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			(store_sub, ":center_offset", ":center_no", castles_begin),
			(store_add, ":troop_no", ":center_offset", cci_castle_blacksmiths_begin),
		(try_end),
		
		(assign, reg1, ":troop_no"),
	]),
	
# script_cci_get_artisan_benefits
# PURPOSE: This determines the building speed & building cost benefits a given center's artisan should confer.
# EXAMPLE: (call_script, "script_cci_get_artisan_benefits", ":center_no", ":level"), # cci_scripts.py
("cci_get_artisan_benefits",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":level", 2),
		
		# (call_script, "script_cci_get_artisan_id", ":center_no"),
		# (assign, ":troop_no", reg1),
		
		(try_begin),
			(lt, ":level", 0),
			# (store_character_level, ":level", ":troop_no"),
			(party_get_slot, ":xp", ":center_no", slot_center_artisan_level_blacksmith),
			(call_script, "script_cci_convert_xp_to_level", ":xp"),
			(assign, ":level", reg1),
			(val_min, ":level", CCI_MAXIMUM_ARTISAN_LEVEL), # Block anything past level 20.
		(try_end),
		
		# 2 build speed for each level.
		(store_mul, ":build_speed", ":level", 2),
		# +1 build speed extra for each level beyond 10.
		(store_sub, ":level_10_bonus", ":level", 10),
		(val_max, ":level_10_bonus", 0),
		(val_add, ":build_speed", ":level_10_bonus"),
		(val_clamp, ":build_speed", 0, 80), # 76 at level 20 (304% speed)
		
		# -8% cost for each level.
		(store_mul, ":build_cost", ":level", 8),
		# -4% cost for each level beyond 5 beyond the base amount.
		(store_sub, ":level_5_bonus", ":level", 5),
		(val_max, ":level_5_bonus", 0),
		(val_mul, ":level_5_bonus", 4),
		(val_add, ":build_cost", ":level_5_bonus"),
		# -3% cost for each level beyond 15 beyond the base amount.
		(store_sub, ":level_15_bonus", ":level", 15),
		(val_max, ":level_15_bonus", 0),
		(val_mul, ":level_15_bonus", 3),
		(val_add, ":build_cost", ":level_15_bonus"),
		(val_clamp, ":build_cost", 0, 300), # -242% cost at level 20
		
		(assign, reg1, ":build_speed"),
		(assign, reg2, ":build_cost"),
	]),
	
# script_cci_give_artisan_xp
# PURPOSE: This grants experience to a given center's artisan and notifies the player if they level up.
# EXAMPLE: (call_script, "script_cci_give_artisan_xp", ":center_no", ":xp"), # cci_scripts.py
("cci_give_artisan_xp",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":xp", 2),
		
		(call_script, "script_cci_get_artisan_id", ":center_no"),
		(assign, ":troop_no", reg1),
		
		(try_begin),
			(party_get_slot, ":xp_artisan", ":center_no", slot_center_artisan_level_blacksmith),
			(call_script, "script_cci_convert_xp_to_level", ":xp_artisan"),
			(assign, ":level_before", reg1),
			(lt, ":level_before", CCI_MAXIMUM_ARTISAN_LEVEL),
			
			## Apply Artisan Bonus Experience.
			(try_begin),
				(ge, ":level_before", 19),
				(assign, ":bonus_multiplier", 30),
			(else_try),
				(ge, ":level_before", 16),
				(assign, ":bonus_multiplier", 25),
			(else_try),
				(ge, ":level_before", 13),
				(assign, ":bonus_multiplier", 20),
			(else_try),
				(ge, ":level_before", 10),
				(assign, ":bonus_multiplier", 15),
			(else_try),
				(ge, ":level_before", 7),
				(assign, ":bonus_multiplier", 10),
			(else_try),
				(ge, ":level_before", 4),
				(assign, ":bonus_multiplier", 5),
			(else_try),
				# Default
				(assign, ":bonus_multiplier", 0),
			(try_end),
			(store_mul, ":xp_bonus", ":xp", ":bonus_multiplier"),
			(val_div, ":xp_bonus", 100),
			(val_add, ":xp", ":xp_bonus"),
			### DIAGNOSTIC+ ###
			# (assign, reg31, ":xp"),
			# (assign, reg32, ":xp_bonus"),
			# (assign, reg33, ":bonus_multiplier"),
			# (assign, reg34, ":level_before"),
			# (display_message, "@DEBUG (CCI): Artisan Level {reg34} improves xp by +{reg32}xp to {reg31}xp (+{reg33}%).", gpu_debug),
			### DIAGNOSTIC- ###
			(val_add, ":xp_artisan", ":xp"),
			(party_set_slot, ":center_no", slot_center_artisan_level_blacksmith, ":xp_artisan"),
			
			(call_script, "script_cci_convert_xp_to_level", ":xp_artisan"),
			(assign, ":level_after", reg1),
			
			## REPORT TO PLAYER
			(try_begin),
				(neq, ":level_after", ":level_before"),
				(str_store_troop_name, s21, ":troop_no"),
				(str_store_party_name, s22, ":center_no"),
				(assign, reg21, ":level_after"),
				(try_begin),
					(gt, ":level_after", ":level_before"),
					(display_message, "@{s21}, your artisan blacksmith in {s22}, has advanced to level {reg21}.", gpu_green),
				(else_try),
					(lt, ":level_after", ":level_before"),
					(display_message, "@{s21}, your artisan blacksmith in {s22}, has been reduced to level {reg21}.", gpu_green),
				(try_end),
				## Event Log Entry.
				(try_begin),
					(call_script, "script_cf_cci_add_event_log_entry", CCI_EVENT_ARTISAN_LEVELED, ":center_no", ":level_after", 0),
				(try_end),
			(try_end),
			
			## SET INVENTORY LIMIT
			(store_div, ":skill_im", ":level_after", 2),
			(troop_set_skill, ":troop_no", "skl_inventory_management", ":skill_im"),
		(try_end),
	]),
	
# script_cci_get_workdown_rate_in_center
# PURPOSE: This puts the calculations for how fast items can be worked on in a single location.
# EXAMPLE: (call_script, "script_cci_get_workdown_rate_in_center", ":center_no", ":critical_effects"), # cci_scripts.py
("cci_get_workdown_rate_in_center",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":critical_effects", 2),
		
		(call_script, "script_cci_get_artisan_benefits", ":center_no", -1),
		(assign, ":build_speed", reg1),
		(val_add, ":build_speed", CCI_HOURLY_WORKDOWN),
		
		## Check for Artisan Critical Progress.
		(try_begin),
			(eq, ":critical_effects", 1),
			(party_get_slot, ":xp", ":center_no", slot_center_artisan_level_blacksmith),
			(call_script, "script_cci_convert_xp_to_level", ":xp"),
			(assign, ":level", reg1),
			(try_begin),
				(ge, ":level", 18),
				(assign, ":crit_chance", 15),
				(assign, ":crit_multiplier", 5),
			(else_try),
				(ge, ":level", 15),
				(assign, ":crit_chance", 15),
				(assign, ":crit_multiplier", 4),
			(else_try),
				(ge, ":level", 12),
				(assign, ":crit_chance", 12),
				(assign, ":crit_multiplier", 4),
			(else_try),
				(ge, ":level", 9),
				(assign, ":crit_chance", 9),
				(assign, ":crit_multiplier", 4),
			(else_try),
				(ge, ":level", 6),
				(assign, ":crit_chance", 9),
				(assign, ":crit_multiplier", 3),
			(else_try),
				(ge, ":level", 3),
				(assign, ":crit_chance", 6),
				(assign, ":crit_multiplier", 4),
			(else_try),
				# Default
				(assign, ":crit_chance", 0),
				(assign, ":crit_multiplier", 1),
			(try_end),
			(ge, ":crit_chance", 1),
			(store_random_in_range, ":roll", 0, 100),
			(lt, ":roll", ":crit_chance"),
			(val_mul, ":build_speed", ":crit_multiplier"),
		(try_end),
		
		## EMBLEM+ - +30% PRODUCTION BOOST ##
		(try_begin),
			(party_slot_ge, ":center_no", slot_center_commission_boost_duration, 1),
			(store_mul, ":boost", ":build_speed", 30),
			(val_div, ":boost", 100),
			(val_add, ":build_speed", ":boost"),
		(try_end),
		## EMBLEM- ##
		
		(assign, reg1, ":build_speed"),
	]),
	
# script_cci_reset_artisan_in_center
# PURPOSE: This resets the Artisan Crafter in the given center back to an inexperienced state (killed during sieges).
# EXAMPLE: (call_script, "script_cci_reset_artisan_in_center", ":center_no"), # cci_scripts.py
("cci_reset_artisan_in_center",
    [
		(store_script_param, ":center_no", 1),
		
		(call_script, "script_cci_get_artisan_id", ":center_no"),
		(assign, ":troop_no", reg1),
		(party_set_slot, ":center_no", slot_center_artisan_level_blacksmith, 0),
		(troop_set_skill, ":troop_no", "skl_inventory_management", 0),
		
		## Event Log Entry.
		(try_begin),
			(call_script, "script_cf_cci_add_event_log_entry", CCI_EVENT_ARTISAN_SLAIN, ":center_no", 0, 0),
		(try_end),
	]),
	
# script_cci_convert_xp_to_level
# PURPOSE: This converts a raw experience value to a level.
# EXAMPLE: (call_script, "script_cci_convert_xp_to_level", ":xp"), # cci_scripts.py
("cci_convert_xp_to_level",
    [
		(store_script_param, ":xp", 1),
		
		(assign, ":level", 1),
		(assign, ":level_xp", 0),
		(assign, ":xp_to_level", 0),
		(try_for_range, ":cycle", 1, 100),
			(store_mul, ":temp_xp", ":cycle", 15),
			(val_add, ":temp_xp", 85),
			(val_mul, ":temp_xp", 7),
			(val_add, ":level_xp", ":temp_xp"),
			(try_begin),
				(lt, ":xp", ":level_xp"),
				(store_sub, ":xp_to_level", ":level_xp", ":xp"),
				(break_loop),
			(try_end),
			(ge, ":xp", ":level_xp"),
			(val_add, ":level", 1),
		(try_end),
		
		(assign, reg1, ":level"),
		(assign, reg2, ":xp_to_level"),
	]),
	
	
# script_cci_check_for_repair_upgrade
# PURPOSE: This returns an appropriate Item Modifier upgrade for a given item type.
# EXAMPLE: (call_script, "script_cci_check_for_repair_upgrade", ":center_no", ":item_type"), # cci_scripts.py
("cci_check_for_repair_upgrade",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":item_type", 2),
		
		# Set the default value.
		(assign, ":imod", imod_plain),
		
		(try_begin),
			# Filter out undesired types.
			(neq, ":item_type", itp_type_horse),
			(neq, ":item_type", itp_type_animal),
			(neq, ":item_type", itp_type_book),
			(neq, ":item_type", itp_type_goods),
			
			# Determine chance of getting an upgrade.
			(party_get_slot, ":xp", ":center_no", slot_center_artisan_level_blacksmith),
			(call_script, "script_cci_convert_xp_to_level", ":xp"),
			(assign, ":level", reg1),
			(try_begin),
				(ge, ":level", 20),
				(assign, ":upgrade_chance", 15), # 8),
			(else_try),
				(ge, ":level", 17),
				(assign, ":upgrade_chance", 12), # 6),
			(else_try),
				(ge, ":level", 14),
				(assign, ":upgrade_chance", 10), # 4),
			(else_try),
				(ge, ":level", 11),
				(assign, ":upgrade_chance", 8), # 3),
			(else_try),
				(ge, ":level", 8),
				(assign, ":upgrade_chance", 6), # 2),
			(else_try),
				(ge, ":level", 5),
				(assign, ":upgrade_chance", 4), # 1),
			(else_try),
				# Default
				(assign, ":upgrade_chance", 0),
			(try_end),
			(store_random_in_range, ":roll", 0, 100),
			
			### DIAGNOSTIC+ ###
			(try_begin),
				(ge, DEBUG_CCI, 1),
				(assign, reg31, ":upgrade_chance"),
				(assign, reg32, ":roll"),
				(str_store_party_name, s31, ":center_no"),
				(display_message, "@DEBUG (CCI): Item repaired, upgrade chance {reg31}%, rolled {reg32} in {s31}.", gpu_debug),
			(try_end),
			### DIAGNOSTIC- ###
			
			(lt, ":roll", ":upgrade_chance"),
			
			# Determine proper item modifier for type.
			(store_random_in_range, ":roll", 0, 100),
			(try_begin),
				# Weapons: itp_type_one_handed_wpn, itp_type_two_handed_wpn, itp_type_polearm, itp_type_crossbow, itp_type_bow, itp_type_thrown, itp_type_pistol, itp_type_musket
				(this_or_next|eq, ":item_type", itp_type_one_handed_wpn),
				(this_or_next|eq, ":item_type", itp_type_two_handed_wpn),
				(this_or_next|eq, ":item_type", itp_type_polearm),
				(this_or_next|eq, ":item_type", itp_type_crossbow),
				(this_or_next|eq, ":item_type", itp_type_bow),
				(this_or_next|eq, ":item_type", itp_type_thrown),
				(this_or_next|eq, ":item_type", itp_type_pistol),
				(eq, ":item_type", itp_type_musket),
				# Valid item.  Now determine item modifier.
				(try_begin),
					(assign, ":imod", imod_fine), # x1.9
					(ge, ":roll", 60),
					(assign, ":imod", imod_heavy), # x1.9
					(ge, ":roll", 90),
					(assign, ":imod", imod_balanced), # x3.5
				(try_end),
			(else_try),
				# Shield: itp_type_shield
				(eq, ":item_type", itp_type_shield),
				# Valid item.  Now determine item modifier.
				(try_begin),
					(assign, ":imod", imod_sturdy), # x1.7
					(ge, ":roll", 60),
					(assign, ":imod", imod_heavy), # x1.9
					(ge, ":roll", 90),
					(assign, ":imod", imod_thick), # x2.6
				(try_end),
			(else_try),
				# Armor: itp_type_head_armor, itp_type_body_armor, itp_type_foot_armor, itp_type_hand_armor
				(this_or_next|eq, ":item_type", itp_type_head_armor),
				(this_or_next|eq, ":item_type", itp_type_body_armor),
				(this_or_next|eq, ":item_type", itp_type_foot_armor),
				(eq, ":item_type", itp_type_hand_armor),
				# Valid item.  Now determine item modifier.
				(try_begin),
					(assign, ":imod", imod_sturdy), # x1.7
					(ge, ":roll", 60),
					(assign, ":imod", imod_heavy), # x1.9
					(ge, ":roll", 90),
					(assign, ":imod", imod_thick), # x2.6
				(try_end),
			(else_try),
				# Ammunition: itp_type_arrows, itp_type_bolts, itp_type_bullets
				(this_or_next|eq, ":item_type", itp_type_arrows),
				(this_or_next|eq, ":item_type", itp_type_bolts),
				(eq, ":item_type", itp_type_bullets),
				(assign, ":imod", imod_large_bag), # x1.9
			(try_end),
			
			(ge, ":upgrade_chance", 1),
			
			### DIAGNOSTIC+ ###
			(try_begin),
				(ge, DEBUG_CCI, 1),
				(call_script, "script_cci_describe_imod_to_s1", ":imod", 0),
				(str_store_party_name, s31, ":center_no"),
				(display_message, "@DEBUG (CCI): Item upgraded from plain to {s1} in {s31}.", gpu_debug),
			(try_end),
			### DIAGNOSTIC- ###
			
			### METRICS+ ### - REPAIR UPGRADES
			(try_begin),
				(troop_get_slot, ":upgrades", METRICS_DATA, metrics_repairs_total_upgrades),
				(val_add, ":upgrades", 1),
				(troop_set_slot, METRICS_DATA, metrics_repairs_total_upgrades, ":upgrades"),
				(try_begin),
					(eq, "$enable_metrics", 1),
					(troop_get_slot, reg31, METRICS_DATA, metrics_repairs_total_upgrades),
					(store_sub, reg32, reg31, 1),
					(display_message, "@METRIC (Repairs): Your repaired item has received a free upgrade.", gpu_debug),
				(try_end),
			(try_end),
			### METRICS- ###
		(try_end),
		
		(assign, reg1, ":imod"),
	]),
	
	
###########################################################################################################################
#####                                             CCI EVENT LOG SCRIPTS                                               #####
###########################################################################################################################
# script_cf_cci_add_event_log_entry
# PURPOSE: This records an event in the CCI EVENT LOG for later display for the player.
# EXAMPLE: (call_script, "script_cf_cci_add_event_log_entry", ":event_type", ":location", ":item_no", ":imod"), # cci_scripts.py
("cf_cci_add_event_log_entry",
    [
		(store_script_param, ":event_type", 1),
		(store_script_param, ":location", 2),
		(store_script_param, ":item_no", 3),
		(store_script_param, ":imod", 4),
		
		# Ensure event type is legitimate.
		(is_between, ":event_type", CCI_EVENT_UNDEFINED, CCI_EVENT_LOG_TYPES_END),
		# Ensure location type is legitimate if applicable.
		(is_between, ":location", centers_begin, centers_end),
		
		(val_add, "$cci_event_log_entries", 1),
		(store_current_hours, ":hours"),
		
		# Check if maximum number of records has been reached and reset if necessary.
		(try_begin),
			(ge, "$cci_event_log_entries", CCI_EVENT_LOG_MAXIMUM_ENTRIES),
			# Wipe log arrays.
			(try_for_range, ":entry_no", 0, CCI_EVENT_LOG_MAXIMUM_ENTRIES),
				(troop_set_slot, CCI_LOG_EVENT,    ":entry_no", CCI_EVENT_UNDEFINED),
				(troop_set_slot, CCI_LOG_ITEM_NO,  ":entry_no", 0),
				(troop_set_slot, CCI_LOG_IMOD,     ":entry_no", 0),
				(troop_set_slot, CCI_LOG_LOCATION, ":entry_no", 0),
				(troop_set_slot, CCI_LOG_DATE, ":entry_no", 0),
			(try_end),
			# Set first entry to reset event.
			(assign, "$cci_event_log_entries", 0),
			(troop_set_slot, CCI_LOG_EVENT,    "$cci_event_log_entries", CCI_EVENT_LOG_RESET),
			(troop_set_slot, CCI_LOG_ITEM_NO,  "$cci_event_log_entries", 0),
			(troop_set_slot, CCI_LOG_IMOD,     "$cci_event_log_entries", 0),
			(troop_set_slot, CCI_LOG_LOCATION, "$cci_event_log_entries", 0),
			(troop_set_slot, CCI_LOG_DATE,     "$cci_event_log_entries", 0),
			(val_add, "$cci_event_log_entries", 1), # Setup our original entry to now go in slot #1.
		(try_end),
		
		# Make New Entry.
		(troop_set_slot, CCI_LOG_EVENT,    "$cci_event_log_entries", ":event_type"),
		(troop_set_slot, CCI_LOG_ITEM_NO,  "$cci_event_log_entries", ":item_no"),
		(troop_set_slot, CCI_LOG_IMOD,     "$cci_event_log_entries", ":imod"),
		(troop_set_slot, CCI_LOG_LOCATION, "$cci_event_log_entries", ":location"),
		(troop_set_slot, CCI_LOG_DATE,     "$cci_event_log_entries", ":hours"),
		
	]),
	
# script_cci_convert_entry_to_string
# PURPOSE: This looks at an entry value in the CCI EVENT LOG and returns s1 with a string describing it.
# EXAMPLE: (call_script, "script_cci_convert_entry_to_string", ":entry_no"), # cci_scripts.py
("cci_convert_entry_to_string",
    [
		(store_script_param, ":entry_no", 1),
		
		# Get entry values.
		(troop_get_slot, ":event_type", CCI_LOG_EVENT,    ":entry_no"),
		(troop_get_slot, ":item_no",    CCI_LOG_ITEM_NO,  ":entry_no"),
		(troop_get_slot, ":imod",       CCI_LOG_IMOD,     ":entry_no"),
		(troop_get_slot, ":location",   CCI_LOG_LOCATION, ":entry_no"),
		
		## s21 - Describe the imod & item.
		(try_begin),
			(neq, ":event_type", CCI_EVENT_UNDEFINED),
			(neq, ":event_type", CCI_EVENT_LOG_RESET),
			(call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
			(try_begin),
				(neq, ":imod", imod_plain),
				(str_store_string, s2, "@{s1} "),
			(else_try),
				(str_clear, s2),
			(try_end),
			(str_store_item_name, s23, ":item_no"),
			(str_store_string, s21, "@{s2}{s23}"),
		(else_try),
			(str_store_string, s21, "@UNDEFINED"),
			(str_store_string, s23, "@UNDEFINED"),
		(try_end),
		
		## s22 - Describe the location.
		(try_begin),
			(neq, ":event_type", CCI_EVENT_UNDEFINED),
			(neq, ":event_type", CCI_EVENT_LOG_RESET),
			(is_between, ":location", centers_begin, centers_end),
			(str_store_party_name, s22, ":location"),
		(else_try),
			(str_store_string, s22, "@UNDEFINED"),
		(try_end),
		
		## s21 - Describe the imod & item.
		## s22 - Describe the location.
		(try_begin),
			(eq, ":event_type", CCI_EVENT_UNDEFINED),
			(str_store_string, s1, "@This is an UNDEFINED event."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_COMMISSION_COMPLETED),
			(str_store_string, s1, "@Your {s21} commission has been completed in {s22}."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_REPAIR_COMPLETED),
			(str_store_string, s1, "@Your artisan blacksmith has completed repairing {s23} in {s22}."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_UPGRADE_COMPLETED),
			(str_store_string, s1, "@Artisan Upgrade - {s23} upgraded to {s21}."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_ARTISAN_LEVELED),
			(assign, reg21, ":item_no"),
			# (try_begin),
				# (eq, reg21, 0),
				# (str_store_string, s23, "@
			# (try_end),
			(str_store_string, s1, "@The artisan blacksmith in {s22} has increased {reg21?to level {reg21}:in level}."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_ARTISAN_SLAIN),
			(str_store_string, s1, "@The artisan blacksmith in {s22} has been slain."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_LOG_RESET),
			(str_store_string, s1, "@The event log has been reset."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_LOG_PRODUCTION_BOOST_BEGIN),
			(str_store_string, s1, "@Production in {s22} has been boosted by use of an emblem."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_LOG_PRODUCTION_BOOST_END),
			(str_store_string, s1, "@The production boost in {s22} has expired."),
		(else_try),
			(eq, ":event_type", CCI_EVENT_COMMISSIONS_RESET),
			(str_store_string, s1, "@All active commissions were reset by player request."),
		(else_try),
			### DEFAULT - ERROR TRAP.
			(str_store_string, s1, "@ERROR: This is an UNDEFINED event."),
		(try_end),
	]),
]
# CCI_EVENT_UNDEFINED                    = 0
# CCI_EVENT_COMMISSION_COMPLETED         = 1 # TRIGGER: Occurs when a commissioned item is completed.
# CCI_EVENT_REPAIR_COMPLETED             = 2 # TRIGGER: Occurs when an item in the artisan's repair inventory is completed.
# CCI_EVENT_UPGRADE_COMPLETED            = 3 # TRIGGER: Occurs when an item in the artisan's repair inventory receives a free imod upgrade.
# CCI_EVENT_ARTISAN_LEVELED              = 4 # TRIGGER: Occurs during experience gains for the artisan if a level up is detected.
# CCI_EVENT_ARTISAN_SLAIN                = 5 # TRIGGER: Occurs when the kill script is called.  Generally this happens in sieges.
# CCI_EVENT_LOG_RESET                    = 6 # TRIGGER: Occurs when the total number of valid events is reached to restart the list.
# CCI_EVENT_LOG_PRODUCTION_BOOST_BEGIN   = 7 # TRIGGER: You spend an emblem to boost production in an area.
# CCI_EVENT_LOG_PRODUCTION_BOOST_END     = 8 # TRIGGER: The duration for production boost in a location runs out.

from util_wrappers import *
from util_scripts import *

scripts_directives = [
	# HOOK: Inserts the initializing scripts in game start as needed.
	[SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_BOTTOM | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (try_end), 0, 
		[(call_script, "script_cci_game_start"),], 1],
] # scripts_rename

def modmerge_scripts(orig_scripts):
	# process script directives first
	process_script_directives(orig_scripts, scripts_directives)
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