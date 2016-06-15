# Companion Management System (1.0) by Windyplains

from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from module_quests import *
from module_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################



simple_triggers = [

###########################################################################################################################
#####                                             DYNAMIC WEAPON SYSTEM                                               #####
###########################################################################################################################
# OUT OF DATE SETTINGS POPUP TRIGGER
# If the player or any companion has dynamic weapon settings then this trigger will cause a menu to pop up reminding the player to update that companion's settings.
(999,
	[
		# (map_free),
		# (assign, ":force_popup_menu", 0),
		# (try_for_range, ":troop_no", companions_begin, companions_end),
		
			# (try_begin),
				# (main_party_has_troop, ":troop_no"),
				# (troop_slot_eq, ":troop_no", slot_troop_dws_enabled, 1), # DWS enabled.
				
				# # Store weapon set information into a temporary array.
				# (try_for_range, ":old_slot", slot_troop_battlefield_set_1, slot_troop_dws_enabled),
					# (store_sub, ":offset", ":old_slot", slot_troop_battlefield_set_1),
					# (store_add, ":new_slot", ":offset", 0),
					# (troop_get_slot, ":item_no", ":troop_no", ":old_slot"),
					# (try_begin),
						# (ge, ":item_no", 1),
						# (troop_set_slot, DWS_OBJECTS, ":new_slot", ":item_no"),
					# (else_try),
						# (troop_set_slot, DWS_OBJECTS, ":new_slot", -1),
					# (try_end),
				# (try_end),
				
				# # Sift through troop inventory to see if they have the items.  Set any items found to -1.
				# (troop_get_inventory_capacity, ":capacity", ":troop_no"),
				# (try_for_range, ":i_slot", 0, ":capacity"),
					# (troop_get_inventory_slot, ":item_no", ":troop_no", ":i_slot"),
					# (ge, ":item_no", 1),
					# (try_for_range, ":array_slot", 0, 4), # 0-3 range because we don't care about non-weapons for DWS.
						# (troop_slot_eq, DWS_OBJECTS, ":array_slot", ":item_no"),
						# (troop_set_slot, DWS_OBJECTS, ":array_slot", -1), # Item found, now delete it as outstanding.
					# (try_end),
				# (try_end),
				
				# # Determine how many outstanding items exist.
				# (assign, ":count", 0),
				# (try_for_range, ":array_slot", 0, 4), # 0-3 range because we don't care about non-weapons for DWS.
					# (troop_slot_ge, DWS_OBJECTS, ":array_slot", 1),
					# (val_add, ":count", 1),
					# ### DIAGNOSTIC ###
					# (ge, DEBUG_ALS, 1),
					# (troop_get_slot, ":item_no", DWS_OBJECTS, ":array_slot"),
					# (str_store_troop_name, s31, ":troop_no"),
					# (str_store_item_name, s32, ":item_no"),
					# (assign, reg31, ":array_slot"),
					# (display_message, "@DEBUG (DWS): {s31} has item [ {s32} ] outstanding in slot {reg31}."),
				# (try_end),
				
				# (try_begin),
					# (ge, ":count", 1),
					# # Store troop's # for later information.
					# (troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 1),
					# (val_add, ":force_popup_menu", 1),
				# (else_try),
					# (troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
				# (try_end),
			
			# (else_try),
				# ## Troop wasn't found so set them to not being out of date just in case.
				# (troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
			# (try_end),
			
		# (try_end),
		
		# ### PLAYER CHECK ###
		# (try_begin),
			# (assign, ":troop_no", "trp_player"),
			# (try_begin),
				# (troop_slot_eq, ":troop_no", slot_troop_dws_enabled, 1), # DWS enabled.
				
				# # Store weapon set information into a temporary array.
				# (try_for_range, ":old_slot", slot_troop_battlefield_set_1, slot_troop_dws_enabled),
					# (store_sub, ":offset", ":old_slot", slot_troop_battlefield_set_1),
					# (store_add, ":new_slot", ":offset", 0),
					# (troop_get_slot, ":item_no", ":troop_no", ":old_slot"),
					# (try_begin),
						# (ge, ":item_no", 1),
						# (troop_set_slot, DWS_OBJECTS, ":new_slot", ":item_no"),
					# (else_try),
						# (troop_set_slot, DWS_OBJECTS, ":new_slot", -1),
					# (try_end),
				# (try_end),
				
				# # Sift through troop inventory to see if they have the items.  Set any items found to -1.
				# (troop_get_inventory_capacity, ":capacity", ":troop_no"),
				# (try_for_range, ":i_slot", 0, ":capacity"),
					# (troop_get_inventory_slot, ":item_no", ":troop_no", ":i_slot"),
					# (ge, ":item_no", 1),
					# (try_for_range, ":array_slot", 0, 4), # 0-3 range because we don't care about non-weapons for DWS.
						# (troop_slot_eq, DWS_OBJECTS, ":array_slot", ":item_no"),
						# (troop_set_slot, DWS_OBJECTS, ":array_slot", -1), # Item found, now delete it as outstanding.
					# (try_end),
				# (try_end),
				
				# # Determine how many outstanding items exist.
				# (assign, ":count", 0),
				# (try_for_range, ":array_slot", 0, 4), # 0-3 range because we don't care about non-weapons for DWS.
					# (troop_slot_ge, DWS_OBJECTS, ":array_slot", 1),
					# (val_add, ":count", 1),
					# ### DIAGNOSTIC ###
					# (ge, DEBUG_ALS, 1),
					# (troop_get_slot, ":item_no", DWS_OBJECTS, ":array_slot"),
					# (str_store_troop_name, s31, ":troop_no"),
					# (str_store_item_name, s32, ":item_no"),
					# (assign, reg31, ":array_slot"),
					# (display_message, "@DEBUG (DWS): {s31} has item [ {s32} ] outstanding in slot {reg31}."),
				# (try_end),
				
				# (try_begin),
					# (ge, ":count", 1),
					# # Store troop's # for later information.
					# (troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 1),
					# (val_add, ":force_popup_menu", 1),
				# (else_try),
					# (troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
				# (try_end),
			
			# (else_try),
				# ## Troop wasn't found so set them to not being out of date just in case.
				# (troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
			# (try_end),
			
		# (try_end),
		
		# ## CONDITIONAL BREAK ##
		# (ge, ":force_popup_menu", 1),
		# (jump_to_menu, "mnu_update_dws_settings"),
	]),
	
# Setting item modifiers for food
(24,
	[
		#(party_get_slot, ":troop_no", "p_main_party", slot_party_role_chef), # 
		(assign, ":troop_no", "$cms_role_storekeeper"),
		(troop_get_inventory_capacity, ":inv_size", ":troop_no"),
		(try_for_range, ":i_slot", 0, ":inv_size"),
			(troop_get_inventory_slot, ":item_id", ":troop_no", ":i_slot"),
			(this_or_next|eq, ":item_id", "itm_cattle_meat"),
			(this_or_next|eq, ":item_id", "itm_chicken"),
			(eq, ":item_id", "itm_pork"),
			
			(troop_get_inventory_slot_modifier, ":modifier", ":troop_no", ":i_slot"),
			(try_begin),
				(eq, ":modifier", imod_rotten),
				(neq, ":troop_no", "trp_player"),
				(str_store_item_name, s21, ":item_id"),
				(str_store_troop_name, s22, ":troop_no"),
				(display_message, "@{s22} has thrown out some {s21} because it has gone rotten."),
				(troop_set_inventory_slot, ":troop_no", ":i_slot", -1),
			(else_try),
				(ge, ":modifier", imod_fresh),
				(lt, ":modifier", imod_rotten),
				(val_add, ":modifier", 1),
				(troop_set_inventory_slot_modifier, ":troop_no", ":i_slot", ":modifier"),
			(else_try),
				(lt, ":modifier", imod_fresh),
				(troop_set_inventory_slot_modifier, ":troop_no", ":i_slot", imod_fresh),
			(try_end),
		(try_end),
    ]),
	
## WARNING - RUNNING OUT OF FOOD!
#  Purpose: Tracks how much food your Storekeeper has remaining in days and warns you if your store drop below this value.
(24,
	[
		(call_script, "script_calculate_days_of_food_remaining"), # reg0 (# of men), reg1 (food available), reg2 (days left)
		(assign, ":days_remaining", reg2),
		# Display warning if stores are low.
		(try_begin),
			(ge, "$cms_days_of_food_threshold", 1), # A setting of 0 disables this option.
			(lt, ":days_remaining", "$cms_days_of_food_threshold"),
			(str_store_troop_name, s21, "$cms_role_storekeeper"),
			(troop_get_type, reg21, "$cms_role_storekeeper"),
			(assign, reg22, ":days_remaining"),
			(store_sub, reg23, reg22, 1),
			(try_begin),
				(eq, "$cms_role_storekeeper", "trp_player"),
				(str_store_string, s20, "@During inventory of your stores you note that you only have {reg22} day{reg23?s:} of food remaining for the troops."),
			(else_try),
				(str_store_string, s20, "@{s21} warns you that {reg21?she:he} has only {reg22} day{reg23?s:} of food remaining for the troops."),
			(try_end),
			## Display text update.
			(display_message, "@{s20}", gpu_red),
			## Display pop-up update if enabled.
			(eq, "$enable_popups", 1),
			(str_store_string, s21, "@Food Stores Running Low!"),
			(str_store_string, s22, "@{s20}"),
			(dialog_box, "@{s22}", "@{s21}"),
		(try_end),
    ]),
###########################################################################################################################
#####                                            COMPANION BOOK READING                                               #####
###########################################################################################################################
# Read books if player is resting.
(1, 
	[
		(try_for_range, ":troop_no", companions_begin, companions_end),
			# Check that we have a valid companion.
			(assign, ":pass", 0),
			(try_begin),
				(main_party_has_troop, ":troop_no"),                   # Companion is in our party.
				(neg|map_free),
				(assign, ":pass", 1),
				(assign, ":factor", 1),
			(else_try),
				(neg|troop_slot_eq, ":troop_no", slot_troop_advisor_station, 0),    # Companion is an advisor somewhere.
				(assign, ":pass", 1),
				(assign, ":factor", 4),
			(try_end),
			(eq, ":pass", 1),
			# Make sure this companion is even reading anything.
			(troop_get_slot, ":item_no", ":troop_no", slot_troop_reading_book),
			(is_between, ":item_no", readable_books_begin, readable_books_end),
			
			# Make sure the companion has the book in his/her position.
			(store_item_kind_count, ":book_count", ":item_no", ":troop_no"),
			(try_begin),
				(eq, ":book_count", 0),
				# If the companion doesn't have the book anymore then stop trying to read it.
				(call_script, "script_change_troop_reading_book", ":troop_no", REMOVE_BOOK),
			(try_end),
			(ge, ":book_count", 1),
			
			# Setup variables for progressing reading.
			(store_sub, ":companion_no", ":troop_no", companions_begin),
			(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
			(item_get_slot, ":reading_progress", ":item_no", ":book_read_slot"),
			(store_attribute_level, ":reading_speed", ":troop_no", ca_intelligence),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_QUICK_STUDY),
				(val_add, ":reading_speed", 10),
			(try_end),
			(val_div, ":reading_speed", 2),
			(val_div, ":reading_speed", ":factor"), # This is used to slow down advisor reading speed.
			
			## WINDYPLAINS+ ## - IMPROVEMENT [ Castle Library ] - Speeds reading time up by 100%.
			(try_begin),
				(main_party_has_troop, ":troop_no"),
				(store_distance_to_party_from_party, ":distance", "p_main_party", "$current_town"),
				(eq, ":distance", 0),
				(party_slot_ge, "$current_town", slot_center_has_castle_library, cis_built),
				(val_mul, ":reading_speed", 2),
			(else_try),
				# Second check for advisors.
				(neg|troop_slot_eq, ":troop_no", slot_troop_advisor_station, 0),
				(troop_get_slot, ":center_no", ":troop_no", slot_troop_advisor_station),
				(party_slot_ge, ":center_no", slot_center_has_castle_library, cis_built),
				(val_mul, ":reading_speed", 2),
			(try_end),
			## WINDYPLAINS- ##
			
			# Continue progress.
			(val_add, ":reading_progress", ":reading_speed"),
			(try_begin),
				(ge, DEBUG_READING, 1),
				(assign, reg31, ":reading_progress"),
				(assign, reg32, ":reading_speed"),
				(str_store_troop_name, s31, ":troop_no"),
				(str_store_item_name, s32, ":item_no"),
				(display_message, "@DEBUG (Reading): {s31}'s reading progress of {s32} is now {reg31} / 1000. (+{reg32})", gpu_debug),
			(try_end),
			(val_clamp, ":reading_progress", 0, 1001),
			(item_set_slot, ":item_no", ":book_read_slot", ":reading_progress"),
			
			# Setup completion notifications.
			(ge, ":reading_progress", 1000),
			(call_script, "script_change_troop_reading_book", ":troop_no", COMPLETED_BOOK),
		(try_end),
		
       ]),
	   
###########################################################################################################################
#####                                             COMPANION ABILITIES                                                 #####
###########################################################################################################################

# COMPANION ABILITIES - Check if a companion's level has raised such that he should unlock a new ability.
(3, 
	[
		(str_clear, s42),
		(assign, ":unlocked_abilities", 0),
		(try_for_range, ":troop_no", companions_begin, companions_end),
			(main_party_has_troop, ":troop_no"),
			(store_character_level, ":level", ":troop_no"),
			## Ability #1
			(lt, ":unlocked_abilities", 3),
			(try_begin),
				(ge, ":level", 5),
				(neg|troop_slot_eq, ":troop_no", slot_troop_requirement_1, BONUS_UNASSIGNED),
				(troop_get_slot, ":ability", ":troop_no", slot_troop_requirement_1),
				(assign, ":continue", 1),
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", ":ability"),
					(assign, ":continue", 0),
				(try_end),
				(eq, ":continue", 1),
				(call_script, "script_ce_assign_troop_ability", ":troop_no", ":ability", BONUS_UNASSIGNED),
				(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"),
				(str_store_troop_name, s21, ":troop_no"),
				(str_store_string, s2, "@{s21} has unlocked {s31}."),
				(str_store_string, s42, "@{s2}^{s1}^^{s42}"),
				(val_add, ":unlocked_abilities", 1),
				(neq, "$enable_popups", 1),
				(display_message, "@{s1}", gpu_green),
			(try_end),
			
			## Ability #2
			(lt, ":unlocked_abilities", 3),
			(try_begin),
				(ge, ":level", 12),
				(neg|troop_slot_eq, ":troop_no", slot_troop_requirement_2, BONUS_UNASSIGNED),
				(troop_get_slot, ":ability", ":troop_no", slot_troop_requirement_2),
				(assign, ":continue", 1),
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", ":ability"),
					(assign, ":continue", 0),
				(try_end),
				(eq, ":continue", 1),
				(call_script, "script_ce_assign_troop_ability", ":troop_no", ":ability", BONUS_UNASSIGNED),
				(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"),
				(str_store_troop_name, s21, ":troop_no"),
				(str_store_string, s2, "@{s21} has unlocked {s31}."),
				(str_store_string, s42, "@{s2}^{s1}^^{s42}"),
				(val_add, ":unlocked_abilities", 1),
				(neq, "$enable_popups", 1),
				(display_message, "@{s1}", gpu_green),
			(try_end),
			
			## Ability #3
			(lt, ":unlocked_abilities", 3),
			(try_begin),
				(ge, ":level", 20),
				(neg|troop_slot_eq, ":troop_no", slot_troop_requirement_3, BONUS_UNASSIGNED),
				(troop_get_slot, ":ability", ":troop_no", slot_troop_requirement_3),
				(assign, ":continue", 1),
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", ":troop_no", ":ability"),
					(assign, ":continue", 0),
				(try_end),
				(eq, ":continue", 1),
				(call_script, "script_ce_assign_troop_ability", ":troop_no", ":ability", BONUS_UNASSIGNED),
				(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"),
				(str_store_troop_name, s21, ":troop_no"),
				(str_store_string, s2, "@{s21} has unlocked {s31}."),
				(str_store_string, s42, "@{s2}^{s1}^^{s42}"),
				(val_add, ":unlocked_abilities", 1),
				(neq, "$enable_popups", 1),
				(display_message, "@{s1}", gpu_dark_green),
			(try_end),

		(try_end),
		(try_begin),
			(ge, ":unlocked_abilities", 1),
			(str_store_string, s3, "@Companion Ability Unlocked"),
			(eq, "$enable_popups", 1),
			(dialog_box, "@{s42}", "@{s3}"),
		(try_end),
			
       ]),

]


# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "simple_triggers"
        orig_simple_triggers = var_set[var_name_1]
        orig_simple_triggers.extend(simple_triggers)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)