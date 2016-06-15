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
(4,
	[
		(map_free),
		(assign, ":force_popup_menu", 0),
		(try_for_range, ":troop_no", companions_begin, companions_end),
		
			(try_begin),
				(main_party_has_troop, ":troop_no"),
				(troop_slot_eq, ":troop_no", slot_troop_dws_enabled, 1), # DWS enabled.
				
				# Store weapon set information into a temporary array.
				(try_for_range, ":old_slot", slot_troop_battlefield_set_1, slot_troop_dws_enabled),
					(store_sub, ":offset", ":old_slot", slot_troop_battlefield_set_1),
					(store_add, ":new_slot", ":offset", 0),
					(troop_get_slot, ":item_no", ":troop_no", ":old_slot"),
					(try_begin),
						(ge, ":item_no", 1),
						(troop_set_slot, DWS_OBJECTS, ":new_slot", ":item_no"),
					(else_try),
						(troop_set_slot, DWS_OBJECTS, ":new_slot", -1),
					(try_end),
				(try_end),
				
				# Sift through troop inventory to see if they have the items.  Set any items found to -1.
				(troop_get_inventory_capacity, ":capacity", ":troop_no"),
				(try_for_range, ":i_slot", 0, ":capacity"),
					(troop_get_inventory_slot, ":item_no", ":troop_no", ":i_slot"),
					(ge, ":item_no", 1),
					(try_for_range, ":array_slot", 0, 4), # 0-3 range because we don't care about non-weapons for DWS.
						(troop_slot_eq, DWS_OBJECTS, ":array_slot", ":item_no"),
						(troop_set_slot, DWS_OBJECTS, ":array_slot", -1), # Item found, now delete it as outstanding.
					(try_end),
				(try_end),
				
				# Determine how many outstanding items exist.
				(assign, ":count", 0),
				(try_for_range, ":array_slot", 0, 4), # 0-3 range because we don't care about non-weapons for DWS.
					(troop_slot_ge, DWS_OBJECTS, ":array_slot", 1),
					(val_add, ":count", 1),
					### DIAGNOSTIC ###
					(ge, DEBUG_ALS, 1),
					(troop_get_slot, ":item_no", DWS_OBJECTS, ":array_slot"),
					(str_store_troop_name, s31, ":troop_no"),
					(str_store_item_name, s32, ":item_no"),
					(assign, reg31, ":array_slot"),
					(display_message, "@DEBUG (DWS): {s31} has item [ {s32} ] outstanding in slot {reg31}."),
				(try_end),
				
				(try_begin),
					(ge, ":count", 1),
					# Store troop's # for later information.
					(troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 1),
					(val_add, ":force_popup_menu", 1),
				(else_try),
					(troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
				(try_end),
			
			(else_try),
				## Troop wasn't found so set them to not being out of date just in case.
				(troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
			(try_end),
			
		(try_end),
		
		### PLAYER CHECK ###
		(try_begin),
			(assign, ":troop_no", "trp_player"),
			(try_begin),
				(troop_slot_eq, ":troop_no", slot_troop_dws_enabled, 1), # DWS enabled.
				
				# Store weapon set information into a temporary array.
				(try_for_range, ":old_slot", slot_troop_battlefield_set_1, slot_troop_dws_enabled),
					(store_sub, ":offset", ":old_slot", slot_troop_battlefield_set_1),
					(store_add, ":new_slot", ":offset", 0),
					(troop_get_slot, ":item_no", ":troop_no", ":old_slot"),
					(try_begin),
						(ge, ":item_no", 1),
						(troop_set_slot, DWS_OBJECTS, ":new_slot", ":item_no"),
					(else_try),
						(troop_set_slot, DWS_OBJECTS, ":new_slot", -1),
					(try_end),
				(try_end),
				
				# Sift through troop inventory to see if they have the items.  Set any items found to -1.
				(troop_get_inventory_capacity, ":capacity", ":troop_no"),
				(try_for_range, ":i_slot", 0, ":capacity"),
					(troop_get_inventory_slot, ":item_no", ":troop_no", ":i_slot"),
					(ge, ":item_no", 1),
					(try_for_range, ":array_slot", 0, 4), # 0-3 range because we don't care about non-weapons for DWS.
						(troop_slot_eq, DWS_OBJECTS, ":array_slot", ":item_no"),
						(troop_set_slot, DWS_OBJECTS, ":array_slot", -1), # Item found, now delete it as outstanding.
					(try_end),
				(try_end),
				
				# Determine how many outstanding items exist.
				(assign, ":count", 0),
				(try_for_range, ":array_slot", 0, 4), # 0-3 range because we don't care about non-weapons for DWS.
					(troop_slot_ge, DWS_OBJECTS, ":array_slot", 1),
					(val_add, ":count", 1),
					### DIAGNOSTIC ###
					(ge, DEBUG_ALS, 1),
					(troop_get_slot, ":item_no", DWS_OBJECTS, ":array_slot"),
					(str_store_troop_name, s31, ":troop_no"),
					(str_store_item_name, s32, ":item_no"),
					(assign, reg31, ":array_slot"),
					(display_message, "@DEBUG (DWS): {s31} has item [ {s32} ] outstanding in slot {reg31}."),
				(try_end),
				
				(try_begin),
					(ge, ":count", 1),
					# Store troop's # for later information.
					(troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 1),
					(val_add, ":force_popup_menu", 1),
				(else_try),
					(troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
				(try_end),
			
			(else_try),
				## Troop wasn't found so set them to not being out of date just in case.
				(troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 0),
			(try_end),
			
		(try_end),
		
		## CONDITIONAL BREAK ##
		(ge, ":force_popup_menu", 1),
		(jump_to_menu, "mnu_update_dws_settings"),
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