# Custom Commissioned Items by Windyplains

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
#####                                             GARRISON RECRUITMENT                                                #####
###########################################################################################################################

### TRIGGER: COMMISSION ADVANCEMENT
#   Purpose: This is how often all custom items will be worked on.  Their rate is calculated hourly, but this is how often those pulses hit the CPU.
(CCI_WORKDOWN_PERIODICITY, 
	[
		### COMMISSION PROGRESSION+ ###
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(party_set_slot, ":center_no", slot_center_commission_order, 0),
		(try_end),
		
		(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
			(troop_slot_ge, CCI_ARRAY_STATUS, ":slot_no", 1), # An item is commissioned and is in progress.
			
			(troop_get_slot, ":item_no", CCI_ARRAY_ITEM_NO, ":slot_no"),
			(troop_get_slot, ":imod", CCI_ARRAY_IMOD, ":slot_no"),
			# (troop_get_slot, ":initial_price", CCI_ARRAY_COST, ":slot_no"),
			(troop_get_slot, ":progress_current", CCI_ARRAY_STATUS, ":slot_no"),
			(troop_get_slot, ":center_no", CCI_ARRAY_LOCATION, ":slot_no"),
			(ge, ":progress_current", 1), # Prevent repeated cycling of an item already done.
			
			## Increase the number of commissions handled in this location tally.
			(party_get_slot, ":count", ":center_no", slot_center_commission_order),
			(val_add, ":count", 1),
			(party_set_slot, ":center_no", slot_center_commission_order, ":count"),
			
			## Prevent continuing if workdown is in SEQUENTIAL mode and this isn't the first item.
			(eq, ":count", 1),
			
			## Determine workdown rate.
			(call_script, "script_cci_get_workdown_rate_in_center", ":center_no", 1),
			(assign, ":hourly_workdown", reg1),
			
			## Advance current progress.
			(store_mul, ":progress_change", ":hourly_workdown", CCI_WORKDOWN_PERIODICITY), # Settings found in cci_constants.py
			(val_sub, ":progress_current", ":progress_change"),
			(try_begin),
				(le, ":progress_current", 0),   # Item has completed.
				(assign, ":progress_current", 0),
			(try_end),
			(troop_set_slot, CCI_ARRAY_STATUS, ":slot_no", ":progress_current"),
			
			## Add experience to local artisan if available.
			(try_begin),
				(party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built),
				(call_script, "script_cci_give_artisan_xp", ":center_no", CCI_XP_GAIN_COMMISSION_TICK),
			(try_end),
			
			## Notify Player if Completed.
			(try_begin),
				(eq, ":progress_current", 0),
				## Add experience boost to local artisan if available.
				(try_begin),
					(party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built),
					(store_mul, ":xp_boost", CCI_XP_GAIN_COMPLETION_MULTIPLIER, CCI_HOURLY_WORKDOWN),
					(call_script, "script_cci_give_artisan_xp", ":center_no", ":xp_boost"),
				(try_end),
				## Event Log Entry.
				(try_begin),
					(call_script, "script_cf_cci_add_event_log_entry", CCI_EVENT_COMMISSION_COMPLETED, ":center_no", ":item_no", ":imod"),
				(try_end),
				## Generate text messages.
				(call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
				(try_begin),
					(neq, ":imod", imod_plain),
					(str_store_string, s1, "@{s1} "),
				(else_try),
					(str_clear, s1),
				(try_end),
				(str_store_item_name, s2, ":item_no"),
				(str_store_string, s23, "@{s1}{s2}"),
				(str_store_party_name, s24, ":center_no"),
				## Display text update.
				(display_message, "@Work on your {s23} has been completed in {s24}."),
				## Display pop-up update if enabled.
				(eq, "$enable_popups", 1),
				(str_store_string, s21, "@Commissioned Item Completed"),
				(str_store_string, s22, "@Work on your {s23} has been completed in {s24}."),
				(dialog_box, "@{s22}", "@{s21}"),
			(try_end),
		(try_end),
		### COMMISSION PROGRESSION- ###
		
		### REPAIR PROGRESSION+ ###
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_center_commission_order, 0), # No active commissions here taking priority.
			(party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built), # Artisan Blacksmith required.
			(call_script, "script_cci_get_artisan_id", ":center_no"),
			(assign, ":troop_no", reg1),
			
			# Check if an item is currently scheduled for repair and still possessed.
			(party_get_slot, ":item_no", ":center_no", slot_center_repairing_item_no),
			(party_get_slot, ":imod", ":center_no", slot_center_repairing_imod),
			(party_get_slot, ":progress_current", ":center_no", slot_center_repairing_progress),
			(assign, ":continue", 0),
			(try_begin), ## LOGIC - We check if the already setup item is available to continue repairing.
				(ge, ":item_no", 1),
				(neq, ":imod", imod_plain),
				## WINDYPLAINS+ ## - Bugfix Ticket #1630 - Artisan re-repairing a better than plain item until it becomes plain again.
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
				# Find this item in the artisan's inventory.
				(troop_get_inventory_capacity, ":inv_capacity", ":troop_no"),
				(assign, ":working_slot", -1),
				(try_for_range, ":inv_slot", 0, ":inv_capacity"),
					(eq, ":working_slot", -1),
					(troop_get_inventory_slot, ":inv_item_no", ":troop_no", ":inv_slot"),
					(ge, ":inv_item_no", 1),
					(troop_get_inventory_slot_modifier, ":inv_imod", ":troop_no", ":inv_slot"),
					(eq, ":inv_item_no", ":item_no"),
					(eq, ":inv_imod", ":imod"),
					(assign, ":working_slot", ":inv_slot"),
				(try_end),
				(neq, ":working_slot", -1), # We found the item.
				(assign, ":continue", 1),
				
			(else_try), ## LOGIC - We didn't find the preset item or one wasn't set.  Pick a new one.
				(troop_get_inventory_capacity, ":inv_capacity", ":troop_no"),
				(assign, ":working_slot", -1),
				(try_for_range, ":inv_slot", 0, ":inv_capacity"),
					(eq, ":working_slot", -1),
					(troop_get_inventory_slot, ":inv_item_no", ":troop_no", ":inv_slot"),
					(ge, ":inv_item_no", 1),
					(troop_get_inventory_slot_modifier, ":inv_imod", ":troop_no", ":inv_slot"),
					(neq, ":inv_imod", imod_plain),
					## WINDYPLAINS+ ## - Bugfix Ticket #1630 - Artisan re-repairing a better than plain item until it becomes plain again.
					(neq, ":inv_imod", imod_fine),
					(neq, ":inv_imod", imod_well_made),
					(neq, ":inv_imod", imod_sharp),
					(neq, ":inv_imod", imod_balanced),
					(neq, ":inv_imod", imod_tempered),
					(neq, ":inv_imod", imod_deadly),
					(neq, ":inv_imod", imod_exquisite),
					(neq, ":inv_imod", imod_masterwork),
					(neq, ":inv_imod", imod_heavy),
					(neq, ":inv_imod", imod_strong),
					(neq, ":inv_imod", imod_powerful),
					(neq, ":inv_imod", imod_sturdy),
					(neq, ":inv_imod", imod_thick),
					(neq, ":inv_imod", imod_hardened),
					(neq, ":inv_imod", imod_reinforced),
					(neq, ":inv_imod", imod_superb),
					(neq, ":inv_imod", imod_lordly),
					(neq, ":inv_imod", imod_spirited),
					(neq, ":inv_imod", imod_champion),
					## WINDYPLAINS- ##
					(assign, ":working_slot", ":inv_slot"),
				(try_end),
				(neq, ":working_slot", -1), # We found the item.
				(troop_get_inventory_slot, ":item_no", ":troop_no", ":working_slot"),
				(troop_get_inventory_slot_modifier, ":imod", ":troop_no", ":working_slot"),
				(party_set_slot, ":center_no", slot_center_repairing_item_no, ":item_no"),
				(party_set_slot, ":center_no", slot_center_repairing_imod, ":imod"),
				## DIAGNOSTIC+ ##
				# (str_store_item_name, s23, ":item_no"),
				# (call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
				# (str_store_party_name, s2, ":center_no"),
				# (display_message, "@DEBUG (CCI): Artisan has started work on {s1} {s23} in {s2}.", gpu_blue),
				## DIAGNOSTIC- ##
				# Determine repair cost for this item.
				(call_script, "script_cci_get_commission_price", ":item_no", imod_plain),
				(assign, ":value_fixed", reg1),
				(call_script, "script_cci_get_commission_price", ":item_no", ":imod"),
				(assign, ":value_broken", reg1),
				(store_sub, ":repair_cost", ":value_fixed", ":value_broken"),
				(party_set_slot, ":center_no", slot_center_repairing_progress, ":repair_cost"),
				(assign, ":continue", 1),
				(assign, ":progress_current", ":repair_cost"),
				### DIAGNOSTIC+ ###
				# (assign, reg21, ":repair_cost"),
				# (assign, reg22, ":value_fixed"),
				# (assign, reg23, ":value_broken"),
				# (display_message, "@DEBUG: Repair Cost = {reg21} denars.  ({reg22} Fixed - {reg23} Broken).", gpu_debug),
				### DIAGNOSTIC- ###
			(else_try), ## LOGIC - No items were found available to repair.
				(party_set_slot, ":center_no", slot_center_repairing_item_no, 0),
				(party_set_slot, ":center_no", slot_center_repairing_imod, 0),
				(party_set_slot, ":center_no", slot_center_repairing_progress, 0),
				(assign, ":continue", 0),
			(try_end),
			(eq, ":continue", 1),
			
			### DIAGNOSTIC+ ###
			(try_begin),
				(ge, DEBUG_CCI, 1),
				(str_store_party_name, s21, ":center_no"),
				(str_store_troop_name, s22, ":troop_no"),
				(str_store_item_name, s23, ":item_no"),
				(call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
				(display_message, "@DEBUG: {s21} - Artisan: {s22} - Working on {s1} {s23}.", gpu_debug),
				# Determine repair cost for this item.
				(call_script, "script_cci_get_commission_price", ":item_no", imod_plain),
				(assign, ":value_fixed", reg1),
				(call_script, "script_cci_get_commission_price", ":item_no", ":imod"),
				(assign, ":value_broken", reg1),
				(store_sub, ":repair_cost", ":value_fixed", ":value_broken"),
				(assign, reg21, ":repair_cost"),
				(assign, reg22, ":progress_current"),
				(display_message, "@DEBUG: Progress left is {reg22} / {reg21}.", gpu_debug),
			(try_end),
			### DIAGNOSTIC- ###
			
			## Determine workdown rate.
			(call_script, "script_cci_get_workdown_rate_in_center", ":center_no", 1),
			(assign, ":hourly_workdown", reg1),
			
			## Advance current progress.
			(store_mul, ":progress_change", ":hourly_workdown", CCI_WORKDOWN_PERIODICITY), # Settings found in cci_constants.py
			(val_sub, ":progress_current", ":progress_change"),
			(try_begin),
				(le, ":progress_current", 0),   # Item has completed.
				## Notify player of item completion.
				(assign, ":progress_current", 0),
			(try_end),
			(party_set_slot, ":center_no", slot_center_repairing_progress, ":progress_current"),
			
			## Add experience to local artisan if available.
			(try_begin),
				(party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built),
				(call_script, "script_cci_give_artisan_xp", ":center_no", CCI_XP_GAIN_REPAIR_TICK),
			(try_end),
			
			## Notify Player if Completed.
			(try_begin),
				(eq, ":progress_current", 0),
				## Add experience boost to local artisan if available.
				(try_begin),
					(party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built),
					(store_mul, ":xp_boost", CCI_XP_GAIN_COMPLETION_MULTIPLIER, CCI_HOURLY_WORKDOWN),
					(call_script, "script_cci_give_artisan_xp", ":center_no", ":xp_boost"),
				(try_end),
				## Event Log Entry.
				(try_begin),
					(call_script, "script_cf_cci_add_event_log_entry", CCI_EVENT_REPAIR_COMPLETED, ":center_no", ":item_no", ":imod"),
				(try_end),
				## Check for chance of upgrading beyond imod_plain.
				(item_get_type, ":item_type", ":item_no"),
				(call_script, "script_cci_check_for_repair_upgrade", ":center_no", ":item_type"),
				(assign, ":imod_new", reg1),
				## Upgrade item to imod_plain.
				(troop_set_inventory_slot_modifier, ":troop_no", ":working_slot", ":imod_new"),
				## Log Entry if upgraded.
				## Event Log Entry.
				(try_begin),
					(neq, ":imod_new", imod_plain),
					(call_script, "script_cf_cci_add_event_log_entry", CCI_EVENT_UPGRADE_COMPLETED, ":center_no", ":item_no", ":imod"),
				(try_end),
				### METRICS+ ### - REPAIR PROFIT TOTALS
				(troop_get_slot, ":repair_profits", METRICS_DATA, metrics_repairs_total_profit),
				(call_script, "script_cci_get_commission_price", ":item_no", ":imod_new"), # imod_plain),
				(assign, ":value_fixed", reg1),
				(call_script, "script_cci_get_commission_price", ":item_no", ":imod"),
				(assign, ":value_broken", reg1),
				(store_sub, ":repair_cost", ":value_fixed", ":value_broken"),
				(val_add, ":repair_profits", ":repair_cost"),
				(troop_set_slot, METRICS_DATA, metrics_repairs_total_profit, ":repair_profits"),
				(try_begin),
					(eq, "$enable_metrics", 1),
					(troop_get_slot, reg31, METRICS_DATA, metrics_repairs_total_profit),
					(store_sub, reg32, reg31, 1),
					(display_message, "@METRIC (Repairs): Your repairs have increased item values by {reg31} denar{reg32?s:}.", gpu_debug),
				(try_end),
				### METRICS- ###
				### METRICS+ ### - TOTAL REPAIRS
				(troop_get_slot, ":total_repairs", METRICS_DATA, metrics_repairs_total_repairs),
				(val_add, ":total_repairs", 1),
				(troop_set_slot, METRICS_DATA, metrics_repairs_total_repairs, ":total_repairs"),
				(try_begin),
					(eq, "$enable_metrics", 1),
					(troop_get_slot, reg31, METRICS_DATA, metrics_repairs_total_repairs),
					(store_sub, reg32, reg31, 1),
					(display_message, "@METRIC (Repairs): Your artisans have repaired a total of {reg31} item{reg32?s:}.", gpu_debug),
				(try_end),
				### METRICS- ###
				## Clear out the preset repair item.
				(party_set_slot, ":center_no", slot_center_repairing_item_no, 0),
				(party_set_slot, ":center_no", slot_center_repairing_imod, 0),
				(party_set_slot, ":center_no", slot_center_repairing_progress, 0),
				## Generate text messages.
				(call_script, "script_cci_describe_imod_to_s1", ":imod_new", 1),
				(try_begin),
					(neq, ":imod_new", imod_plain),
					(str_store_string, s1, "@{s1} "),
				(else_try),
					(str_clear, s1),
				(try_end),
				(str_store_item_name, s2, ":item_no"),
				(str_store_string, s23, "@{s1}{s2}"),
				(str_store_party_name, s24, ":center_no"),
				## Display text update.
				(display_message, "@Repairs on your {s23} has been completed in {s24}."),
				## Display pop-up update if enabled.
				(eq, "$enable_popups", 1),
				(str_store_string, s21, "@Repairs Completed"),
				(str_store_string, s22, "@Repairs on your {s23} has been completed in {s24}."),
				(dialog_box, "@{s22}", "@{s21}"),
			(try_end),
			
		(try_end),
		### REPAIR PROGRESSION- ###
		
		### EMBLEM+ BOOST TIMER DURATION ###
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(party_get_slot, ":hours", ":center_no", slot_center_commission_boost_duration),
			(ge, ":hours", 1),
			(val_sub, ":hours", CCI_WORKDOWN_PERIODICITY),
			(try_begin),
				(lt, ":hours", 1),
				(call_script, "script_cf_cci_add_event_log_entry", CCI_EVENT_LOG_PRODUCTION_BOOST_END, "$current_town", 0, 0),
				(assign, ":hours", 0),
			(try_end),
			(party_set_slot, ":center_no", slot_center_commission_boost_duration, ":hours"),
		(try_end),
		### EMBLEM- BOOST TIMER DURATION ###
    ]),

### TRIGGER: ABANDONMENT TIMER
#   Purpose: This tracks how many days a commissioned item has been left in a completed state at a location.
(24, 
	[
		(try_for_range, ":slot_no", 0, CCI_GOBAL_COMMISSION_LIMIT),
			(troop_slot_eq, CCI_ARRAY_STATUS, ":slot_no", 0), # An commissioned item is completed here.
			(troop_get_slot, ":center_no", CCI_ARRAY_LOCATION, ":slot_no"),
			(troop_get_slot, ":days_abandoned", CCI_ARRAY_ABANDON_TIMER, ":slot_no"),
			(val_add, ":days_abandoned", 1),
			(troop_set_slot, CCI_ARRAY_ABANDON_TIMER, ":slot_no", ":days_abandoned"),
			
			## Warn player once 30 days has been reached.
			(store_sub, ":days_left", CCI_ABANDONED_DAYS_LIMIT, ":days_abandoned"),
			(try_begin),
				(this_or_next|eq, ":days_left", 30),
				(eq, ":days_left", 7),
				(troop_get_slot, ":item_no", CCI_ARRAY_ITEM_NO, ":slot_no"),
				(troop_get_slot, ":imod", CCI_ARRAY_IMOD, ":slot_no"),
				(call_script, "script_cci_describe_imod_to_s1", ":imod", 1),
				(try_begin),
					(neq, ":imod", imod_plain),
					(str_store_string, s1, "@{s1} "),
				(else_try),
					(str_clear, s1),
				(try_end),
				(str_store_item_name, s2, ":item_no"),
				(str_store_string, s21, "@{s1}{s2}"),
				(str_store_party_name, s22, ":center_no"),
				(assign, reg21, ":days_left"),
				(display_message, "@Warning - Your {s21} commissioned in {s22} will be considered abandoned within {reg21} days and sold off.", gpu_red),
			(try_end),
			
			## Cancel items abandoned past (CCI_ABANDONED_DAYS_LIMIT) days.
			(ge, ":days_abandoned", CCI_ABANDONED_DAYS_LIMIT),
			
			## Royal Blacksmith prevents abandoned items from being sold off.
			(neg|party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built),
			
			## Remove item from the queue.
			(call_script, "script_cci_clear_commission_entry", ":slot_no", 1),
			
		(try_end),
    ]),
	
	
### TRIGGER: POSITION CHECK
#   Purpose: This tracks how many days a commissioned item has been left in a completed state at a location.
# (0.1, 
	# [
		# (this_or_next|key_is_down, key_left_shift),
		# (key_is_down, key_right_shift),
		# (set_fixed_point_multiplier, 1),
		# # Determine player position on the map.
		# (party_get_position, pos1, "p_main_party"),
		# (position_get_x, reg31, pos1),
		# (position_get_y, reg32, pos1),
		# (display_message, "@DEBUG: Player sitting at {reg31}, {reg32}."),
    # ]),
		
		
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