# Companion Management System (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *

###########################################################################################################################
#####                                             DYNAMIC WEAPON SYSTEM                                               #####
###########################################################################################################################
dws_triggers = [  
# (ti_before_mission_start, 0, 0, [],
    # [
		# # Determine which set we want to use.
		# (try_begin),
			# ## SIEGE SET ##
			# (this_or_next|is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),   # Sieges
			# (party_slot_eq, "$g_encountered_party", slot_party_type, spt_bandit_lair),                     # Bandit Lairs
			# #(is_between, "$g_encountered_party", villages_begin, villages_end),                           # Villages
			# (assign, ":item_set_group", slot_troop_siege_set_1),
		# (else_try),
			# ## BATTLEFIELD SET ## (default)
			# (assign, ":item_set_group", slot_troop_battlefield_set_1),
		# (try_end),
		
		# # Report changes to player if desired.
		# (try_begin),
			# #(eq, ":continue", 1),
			# (eq, "$dws_report_activity", 1),
			# (try_begin),
				# (eq, ":item_set_group", slot_troop_battlefield_set_1),
				# (str_store_string, s21, "@battlefield"),
			# (else_try),
				# (eq, ":item_set_group", slot_troop_siege_set_1),
				# (str_store_string, s21, "@siege"),
			# (try_end),
			# (display_message, "@Everyone has switched weapons to their {s21} sets."),
		# (try_end),
	# ]),
	
# (ti_after_mission_start, 0, 0, [],
    # [(assign, "$dws_player_count", 0),]),
	
# (ti_on_agent_spawn, 0, 0, [],
    # [
		# (store_trigger_param_1, ":agent_no"),
		
		# (agent_get_troop_id, ":troop_no", ":agent_no"),
		# (assign, ":continue", 1),
		# (try_begin),
			# ## BLOCK 2ND PLAYER CYCLE ##
			# (eq, ":troop_no", "trp_player"),
			# (val_add, "$dws_player_count", 1),
			# (ge, "$dws_player_count", 2),
			# (assign, ":continue", 0),
		# (try_end),
		# (eq, ":continue", 1), ## CONDITIONAL BREAK ##
		
		# (troop_slot_eq, ":troop_no", slot_troop_dws_enabled, 1),
		# # Set some initial values.
		# (assign, ":set_item_1", -1),
		# (assign, ":set_item_2", -1),
		# (assign, ":set_item_3", -1),
		# (assign, ":set_item_4", -1),
		# (assign, ":set_item_1_imod", imod_plain),
		# (assign, ":set_item_2_imod", imod_plain),
		# (assign, ":set_item_3_imod", imod_plain),
		# (assign, ":set_item_4_imod", imod_plain),
		
		# # Determine which set we want to use.
		# (try_begin),
			# ## SIEGE SET ##
			# (this_or_next|is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),   # Sieges
			# (party_slot_eq, "$g_encountered_party", slot_party_type, spt_bandit_lair),                     # Bandit Lairs
			# #(is_between, "$g_encountered_party", villages_begin, villages_end),                           # Villages
			# (assign, ":item_set_group", slot_troop_siege_set_1),
		# (else_try),
			# ## BATTLEFIELD SET ## (default)
			# (assign, ":item_set_group", slot_troop_battlefield_set_1),
		# (try_end),
		
		# # Report changes to player if desired.
		# # (try_begin),
			# # (eq, ":continue", 1),
			# # (eq, "$dws_report_activity", 1),
			# # (try_begin),
				# # (eq, ":item_set_group", slot_troop_battlefield_set_1),
				# # (str_store_string, s21, "@battlefield"),
			# # (else_try),
				# # (eq, ":item_set_group", slot_troop_siege_set_1),
				# # (str_store_string, s21, "@siege"),
			# # (try_end),
			# # (str_store_troop_name, s22, ":troop_no"),
			# # (troop_get_type, reg21, ":troop_no"),
			# # (display_message, "@{s22} has switched weapons to {reg21?her:his} {s21} set."),
		# # (try_end),
		
		# # See if the set has any empty slots and handle them differently.
		# (try_begin),
			# (assign, ":item_slot", ":item_set_group"),
			# (troop_slot_eq, ":troop_no", ":item_slot", -1),
			# (assign, ":set_item_1", -2),
		# (try_end),
		# (try_begin),
			# (val_add, ":item_slot", 1),
			# (troop_slot_eq, ":troop_no", ":item_slot", -1),
			# (assign, ":set_item_1", -2),
		# (try_end),
		# (try_begin),
			# (val_add, ":item_slot", 1),
			# (troop_slot_eq, ":troop_no", ":item_slot", -1),
			# (assign, ":set_item_1", -2),
		# (try_end),
		# (try_begin),
			# (val_add, ":item_slot", 1),
			# (troop_slot_eq, ":troop_no", ":item_slot", -1),
			# (assign, ":set_item_1", -2),
		# (try_end),
		
		# # Attempt to acquire set items from inventory.
		# (try_begin),
			# (troop_get_inventory_capacity, ":capacity", ":troop_no"),
			# (try_for_range, ":inv_slot", 0, ":capacity"),
				# (troop_get_inventory_slot, ":item_no", ":troop_no", ":inv_slot"),
				# (ge, ":item_no", 1), # Valid Item
				# # Try to fill in the item slot variables.
				# (try_begin),
					# (store_add, ":set_slot", ":item_set_group", 0),
					# (troop_slot_eq, ":troop_no", ":set_slot", ":item_no"),
					# (assign, ":set_item_1", ":item_no"),
					# (troop_get_inventory_slot_modifier, ":set_item_1_imod", ":troop_no", ":inv_slot"),
					# (ge, DEBUG_DWS, 2),
					# (assign, reg31, ":item_no"),
					# (assign, reg32, ":set_item_1_imod"),
					# (str_store_item_name, s31, ":item_no"),
					# (display_message, "@Item [ {s31} ] [#{reg31} & Imod {reg32}] stored as set_item_1."),
				# (else_try),
					# (store_add, ":set_slot", ":item_set_group", 1),
					# (troop_slot_eq, ":troop_no", ":set_slot", ":item_no"),
					# (assign, ":set_item_2", ":item_no"),
					# (troop_get_inventory_slot_modifier, ":set_item_2_imod", ":troop_no", ":inv_slot"),
					# (ge, DEBUG_DWS, 2),
					# (assign, reg31, ":item_no"),
					# (assign, reg32, ":set_item_2_imod"),
					# (str_store_item_name, s31, ":item_no"),
					# (display_message, "@Item [ {s31} ] [#{reg31} & Imod {reg32}] stored as set_item_2."),
				# (else_try),
					# (store_add, ":set_slot", ":item_set_group", 2),
					# (troop_slot_eq, ":troop_no", ":set_slot", ":item_no"),
					# (assign, ":set_item_3", ":item_no"),
					# (troop_get_inventory_slot_modifier, ":set_item_3_imod", ":troop_no", ":inv_slot"),
					# (ge, DEBUG_DWS, 2),
					# (assign, reg31, ":item_no"),
					# (assign, reg32, ":set_item_3_imod"),
					# (str_store_item_name, s31, ":item_no"),
					# (display_message, "@Item [ {s31} ] [#{reg31} & Imod {reg32}] stored as set_item_3."),
				# (else_try),
					# (store_add, ":set_slot", ":item_set_group", 3),
					# (troop_slot_eq, ":troop_no", ":set_slot", ":item_no"),
					# (assign, ":set_item_4", ":item_no"),
					# (troop_get_inventory_slot_modifier, ":set_item_4_imod", ":troop_no", ":inv_slot"),
					# (ge, DEBUG_DWS, 2),
					# (assign, reg31, ":item_no"),
					# (assign, reg32, ":set_item_4_imod"),
					# (str_store_item_name, s31, ":item_no"),
					# (display_message, "@Item [ {s31} ] [#{reg31} & Imod {reg32}] stored as set_item_4."),
				# (try_end),
			# (try_end),
		# (try_end),
		
		# (assign, ":continue", 1),
		# (try_begin),
			# (troop_slot_eq, ":troop_no", slot_troop_dws_all_or_nothing, 1),
			# (assign, ":continue", 0),
			# # (ge, ":set_item_1", 1),
			# # (ge, ":set_item_2", 1),
			# # (ge, ":set_item_3", 1),
			# (this_or_next|ge, ":set_item_1", 1),
			# (eq, ":set_item_1", -2),
			# (this_or_next|ge, ":set_item_2", 1),
			# (eq, ":set_item_2", -2),
			# (this_or_next|ge, ":set_item_3", 1),
			# (eq, ":set_item_3", -2),
			# (this_or_next|ge, ":set_item_4", 1),
			# (eq, ":set_item_4", -2),
			# (assign, ":continue", 1),
		# (else_try),
			# (troop_slot_eq, ":troop_no", slot_troop_dws_all_or_nothing, 1),
			# (str_store_troop_name, s22, ":troop_no"),
			# (display_message, "@{s22} was unable to switch weapon sets due to not having a full set available."),
			# (troop_set_slot, ":troop_no", slot_troop_dws_out_of_date, 1),
		# (try_end),
		# (eq, ":continue", 1), ## CONDITIONAL BREAK ##
		
		# # Unequip items
		# (try_for_range, ":weapon_slot", 0, 4),
			# (troop_get_inventory_slot, ":item_no", ":troop_no", ":weapon_slot"),
			# (troop_set_slot, DWS_OBJECTS, ":weapon_slot", ":item_no"), # For later tracking.
			# (agent_get_item_slot_modifier, ":imod", ":agent_no", ":weapon_slot"),
			# (store_add, ":imod_slot", ":weapon_slot", 10),
			# (troop_set_slot, DWS_OBJECTS, ":imod_slot", ":imod"), # For later tracking.
			# (ge, ":item_no", 1), # Valid item.
			# # Need to remove the item.
			# (agent_unequip_item, ":agent_no", ":item_no"),
		# (try_end),
				
		# # Load Items
		# (try_for_range, ":weapon_slot", 0, 4),
			# # Determine what the DWS item is.
			# (try_begin),
				# (eq, ":weapon_slot", 0),
				# (assign, ":dws_item", ":set_item_1"),
				# (assign, ":dws_imod", ":set_item_1_imod"),
			# (else_try),
				# (eq, ":weapon_slot", 1),
				# (assign, ":dws_item", ":set_item_2"),
				# (assign, ":dws_imod", ":set_item_2_imod"),
			# (else_try),
				# (eq, ":weapon_slot", 2),
				# (assign, ":dws_item", ":set_item_3"),
				# (assign, ":dws_imod", ":set_item_3_imod"),
			# (else_try),
				# (eq, ":weapon_slot", 3),
				# (assign, ":dws_item", ":set_item_4"),
				# (assign, ":dws_imod", ":set_item_4_imod"),
			# (try_end),
			
			# # Load in DWS item or failing that re-equip the original item.
			# (assign, ":switched", 0),
			# (try_begin),
				# (ge, ":dws_item", 1),
				# (agent_set_wielded_item, ":agent_no", ":dws_item"),
				# (agent_set_item_slot_modifier, ":agent_no", ":weapon_slot", ":dws_imod"),
				# # (agent_set_item_slot, ":agent_no", ":weapon_slot", ":dws_item", ":dws_imod"),
				# (assign, ":switched", 1),
			# # (else_try),
				# # (ge, ":item_no", 1),
				# # (troop_get_slot, ":item_no", DWS_OBJECTS, ":weapon_slot"),
				# # (store_add, ":imod_slot", ":weapon_slot", 10),
				# # (troop_get_slot, ":imod", DWS_OBJECTS, ":imod_slot"),
				# # (agent_set_item_slot, ":agent_no", ":weapon_slot", ":item_no", ":imod"),
			# (try_end),
			
			# (try_begin),
				# (ge, DEBUG_DWS, 1),
				# (eq, ":switched", 1),
				# (neq, ":dws_item", ":item_no"),
				# (neg|troop_slot_eq, DWS_OBJECTS, 0, ":dws_item"),
				# (neg|troop_slot_eq, DWS_OBJECTS, 1, ":dws_item"),
				# (neg|troop_slot_eq, DWS_OBJECTS, 2, ":dws_item"),
				# (neg|troop_slot_eq, DWS_OBJECTS, 3, ":dws_item"),
				# (str_store_item_name, s31, ":dws_item"),
				# #(str_store_item_name, s32, ":item_no"),
				# (str_store_troop_name, s33, ":troop_no"),
				# (assign, reg31, ":weapon_slot"),
				# (display_message, "@{s33} equippped {s31} in slot {reg31}."),
			# (try_end),
		# (try_end),
		
    # ]),

]

def modmerge_mission_templates(orig_mission_templates):
	# brute force add dws_triggers to all mission templates with mtf_battle_mode
	for i in range (0,len(orig_mission_templates)):
		if( orig_mission_templates[i][1] & mtf_battle_mode ):
			orig_mission_templates[i][5].extend(dws_triggers)

# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "mission_templates"
        orig_mission_templates = var_set[var_name_1]
        modmerge_mission_templates(orig_mission_templates)

    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)