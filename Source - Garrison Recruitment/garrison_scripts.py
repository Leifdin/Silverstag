# Garrison Recruitment & Training by Windyplains

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

# script_garrison_initialize
# PURPOSE: Sets initial conditions for the GARRISON RECRUITMENT & TRAINING system.
# EXAMPLE: (call_script, "script_garrison_initialize"), # garrison_scripts.py
("garrison_initialize",
	[
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(call_script, "script_grt_clear_center_queue", ":center_no"), # Clear out these slots just in case.
			(party_set_slot, ":center_no", slot_party_queue_progression, GRT_BUDGET_SPLIT), # Set every center to use Split Queue by default.
			(party_set_slot, ":center_no", slot_center_recruiting, 1), # Enable garrison recruiting.
		(try_end),
 	]),  
		
# script_grt_clear_center_queue
# PURPOSE: Initializes all information for a given center's queue.
# EXAMPLE: (call_script, "script_grt_clear_center_queue", ":center_no"), # garrison_scripts.py
("grt_clear_center_queue",
    [
		(store_script_param, ":center_no", 1),
		
		## QUEUE - TROOP ID SLOTS
		(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
			(party_set_slot, ":center_no", ":queue_slot", -1), # Empty space.
		(try_end),
		
		## QUEUE - TROOP QUANTITY SLOTS
		(try_for_range, ":queue_slot", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_quantity_end),
			(party_set_slot, ":center_no", ":queue_slot", 0), # Empty space.
		(try_end),
		
		## DIGANOSTIC
		(try_begin),
			(ge, DEBUG_GARRISON, 2),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@DEBUG (GRT): {s31}'s garrison queue has been reset.", gpu_debug),
		(try_end),
	]),
	
# script_grt_tidy_queue
# PURPOSE: Shifts all entries up removing any blank spaces.
# EXAMPLE: (call_script, "script_grt_tidy_queue", ":center_no"), # garrison_scripts.py
("grt_tidy_queue",
    [
		(store_script_param, ":center_no", 1),
		
		## QUEUE - Consolidate duplicate requests.
		(try_for_range, ":slot_fixed_id", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
			(party_get_slot, ":fixed_id", ":center_no", ":slot_fixed_id"),
			# Figure out our quantity slot.
			(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
			(store_add, ":slot_fixed_qty", ":slot_fixed_id", ":offset"),
			(party_get_slot, ":fixed_qty", ":center_no", ":slot_fixed_qty"),
			(store_add, ":next_slot", ":slot_fixed_id", 1),
			(try_for_range, ":slot_move_id", ":next_slot", slot_party_queue_slot_id_end),
				(party_slot_eq, ":center_no", ":slot_move_id", ":fixed_id"),
				# Figure out our quantity slot.
				(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
				(store_add, ":slot_move_qty", ":slot_move_id", ":offset"),
				(party_get_slot, ":move_qty", ":center_no", ":slot_move_qty"),
				(val_add, ":fixed_qty", ":move_qty"),
				(party_set_slot, ":center_no", ":slot_fixed_qty", ":fixed_qty"),
				# Clear out the duplicate entry.
				(party_set_slot, ":center_no", ":slot_move_qty", 0),
				(party_set_slot, ":center_no", ":slot_move_id", -1),
			(try_end),
		(try_end),
		
		## QUEUE - TROOP ID SLOTS
		(try_for_range, ":slot_fixed_id", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
			(party_slot_eq, ":center_no", ":slot_fixed_id", -1), # Empty space.
			(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
			(store_add, ":slot_fixed_qty", ":slot_fixed_id", ":offset"),
			(try_for_range, ":slot_move_id", ":slot_fixed_id", slot_party_queue_slot_id_end),
				(neg|party_slot_eq, ":center_no", ":slot_move_id", -1), # Empty space.
				(neg|party_slot_eq, ":center_no", ":slot_move_id", 0), # Prevent any chance of duplicate players.
				# Figure out our quantity slot.
				(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
				(store_add, ":slot_move_qty", ":slot_move_id", ":offset"),
				# Error trap for a bad quantity.  Results in removing the troop ID and clearing this entry.
				(try_begin),
					(neg|party_slot_ge, ":center_no", ":slot_move_qty", 1), # Value <= 0.
					(party_set_slot, ":center_no", ":slot_move_id", -1),
					(party_set_slot, ":center_no", ":slot_move_qty", 0),
				(try_end),
				(party_slot_ge, ":center_no", ":slot_move_qty", 1),
				# Replace the fixed slot info with the move slot info.
				(party_get_slot, ":temp_id", ":center_no", ":slot_move_id"),
				(party_get_slot, ":temp_qty", ":center_no", ":slot_move_qty"),
				(party_set_slot, ":center_no", ":slot_fixed_id", ":temp_id"),
				(party_set_slot, ":center_no", ":slot_fixed_qty", ":temp_qty"),
				# Empty our move slot info.
				(party_set_slot, ":center_no", ":slot_move_id", -1),
				(party_set_slot, ":center_no", ":slot_move_qty", 0),
				(break_loop),
			(try_end), # MOVE loop
			(eq, ":slot_move_id", slot_party_queue_slot_id_end), # Nothing left to move up.
			(break_loop),
		(try_end), # FIXED loop
		
		## DIGANOSTIC
		(try_begin),
			(ge, DEBUG_GARRISON, 2),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@DEBUG (GRT): {s31}'s garrison queue has been tidied.", gpu_debug),
		(try_end),
	]),
	
# script_grt_add_troop_to_queue
# PURPOSE: Finds an appropriate slot to add a troop to a given center's queue.
# EXAMPLE: (call_script, "script_grt_add_troop_to_queue", ":center_no", ":troop_no", ":quantity"), # garrison_scripts.py
("grt_add_troop_to_queue",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_no", 2),
		(store_script_param, ":requested_qty", 3),
		
		(assign, ":found", 0),
		
		## Check for any current requests for this troop type.
		(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
			(party_slot_eq, ":center_no", ":queue_slot", ":troop_no"),
			(assign, ":found", 1),
			## Figure out our quantity slot.
			(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
			(store_add, ":slot_qty", ":queue_slot", ":offset"),
			(party_get_slot, ":current_qty", ":center_no", ":slot_qty"),
			(val_add, ":current_qty", ":requested_qty"),
			(party_set_slot, ":center_no", ":slot_qty", ":current_qty"),
		(try_end),
		
		## Find first available spot if not already added previously.
		(try_begin),
			(eq, ":found", 0),
			(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
				(this_or_next|party_slot_eq, ":center_no", ":queue_slot", 0), # Empty space.
				(party_slot_eq, ":center_no", ":queue_slot", -1), # Empty space.
				(assign, ":found", 2),
				## Figure out our quantity slot.
				(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
				(store_add, ":slot_qty", ":queue_slot", ":offset"),
				(party_set_slot, ":center_no", ":queue_slot", ":troop_no"),
				(party_set_slot, ":center_no", ":slot_qty", ":requested_qty"),
				(break_loop),
			(try_end),
		(try_end),
		
		(try_begin),
			(eq, ":found", 0),
			(neq, ":troop_no", 0),
			(str_store_troop_name_plural, s21, ":troop_no"),
			(display_message, "@You are unable to queue more {s21} at this time.", gpu_red),
		(try_end),
	]),
	
# script_grt_remove_troop_from_queue
# PURPOSE: Finds an appropriate slot to add a troop to a given center's queue.
# EXAMPLE: (call_script, "script_grt_remove_troop_from_queue", ":center_no", ":troop_no", ":quantity"), # garrison_scripts.py
("grt_remove_troop_from_queue",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_no", 2),
		(store_script_param, ":removal_quantity", 3),
		
		(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
			(party_slot_eq, ":center_no", ":queue_slot", ":troop_no"),
			## Figure out our quantity slot.
			(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
			(store_add, ":slot_qty", ":queue_slot", ":offset"),
			(party_get_slot, ":quantity", ":center_no", ":slot_qty"),
			(try_begin),
				## Case #1: Remove all of the quantity regardless of size.
				(eq, ":removal_quantity", -1),
				(party_set_slot, ":center_no", ":slot_qty", 0),
			(else_try),
				## Case #2: Remove a portion of the quantity.
				(val_min, ":removal_quantity", ":quantity"),
				(val_sub, ":quantity", ":removal_quantity"),
				(party_set_slot, ":center_no", ":slot_qty", ":quantity"),
			(try_end),
			## No quantity requested = Remove troop request.
			(try_begin),
				(neg|party_slot_ge, ":center_no", ":slot_qty", 1),
				(party_set_slot, ":center_no", ":queue_slot", -1),
				(party_set_slot, ":center_no", ":slot_qty", 0),
			(try_end),
			(break_loop),
		(try_end),
	]),
	
# script_grt_get_total_troop_types
# PURPOSE: This is to find out how many total troop types are being requested at a center and return that value back for splitting the budget.
# EXAMPLE: (call_script, "script_grt_get_total_troop_types", ":center_no"), # garrison_scripts.py
("grt_get_total_troop_types",
    [
		(store_script_param, ":center_no", 1),
		
		(assign, ":tally", 0),
		(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
			(neg|party_slot_eq, ":center_no", ":queue_slot", -1), # Empty space.
			(val_add, ":tally", 1),
		(try_end),
		(assign, reg1, ":tally"),
	]),
	
# script_grt_get_queue_count_for_troop
# PURPOSE: This returns how many of a specific troop at a given city are queued for hiring.
# EXAMPLE: (call_script, "script_grt_get_queue_count_for_troop", ":center_no", ":troop_no"), # garrison_scripts.py
("grt_get_queue_count_for_troop",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":troop_no", 2),
		
		(assign, ":tally", 0),
		(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
			(party_slot_eq, ":center_no", ":queue_slot", ":troop_no"),
			(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
			(store_add, ":qty_slot", ":queue_slot", ":offset"),
			(party_get_slot, ":quantity", ":center_no", ":qty_slot"),
			(val_add, ":tally", ":quantity"),
		(try_end),
		(assign, reg1, ":tally"),
	]),
	
# script_grt_process_weekly_hiring
# PURPOSE: This is to find out how many total troop types are being requested at a center and return that value back for splitting the budget.
# EXAMPLE: (call_script, "script_grt_process_weekly_hiring", ":center_no"), # garrison_scripts.py
("grt_process_weekly_hiring",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":mode", 2),
		
		# GRT_QUEUE_PROCESS                      = 1
		# GRT_QUEUE_PRINT                        = 2
		(str_clear, s49), # Printing process
		(assign, ":line_count", 0),
		
		(try_begin),
			# Verify if any troops are needed to be hired here.
			(call_script, "script_grt_get_total_troop_types", ":center_no"),
			(ge, reg1, 1),
			(assign, ":types", reg1),
			
			# Verify a valid owner of this center exists.
			(party_get_slot, ":troop_lord", ":center_no", slot_town_lord),
			(this_or_next|eq, ":troop_lord", "trp_player"),
			(is_between, ":troop_lord", active_npcs_begin, active_npcs_end),
			
			# Determine our budget parameters
			(party_get_slot, ":budget", ":center_no", slot_party_queue_budget),
			(party_get_slot, ":excess", ":center_no", slot_party_queue_budget_excess),
			(val_add, ":budget", ":excess"),
			(party_set_slot, ":center_no", slot_party_queue_budget_excess, 0),
			(party_get_slot, ":budget_type", ":center_no", slot_party_queue_progression),
			
			# Process hiring costs based upon budget type.
			(try_begin),
				### FOCUSED BUDGET
				(eq, ":budget_type", GRT_BUDGET_FOCUSED),
				(assign, ":stop_hiring", 0),
				(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
					(neg|party_slot_eq, ":center_no", ":queue_slot", -1), # Empty space.
					(eq, ":stop_hiring", 0),
					### DIAGNOSTIC+ ###
					# (try_begin),
						# (eq, ":mode", GRT_QUEUE_PRINT),
						# (assign, reg31, ":budget"),
						# (str_store_string, s49, "@{s49}Focused budget of {reg31} denars will yield:^^"),
						# (val_add, ":line_count", 2),
					# (try_end),
					### DIAGNOSTIC- ###
					(party_get_slot, ":troop_no", ":center_no", ":queue_slot"),
					
					## Figure out our quantity slot.
					(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
					(store_add, ":slot_qty", ":queue_slot", ":offset"),
					(party_get_slot, ":quantity", ":center_no", ":slot_qty"),
					(assign, ":orig_quantity", ":quantity"),
					
					## Limit our quantity by how many recruits are available.
					(call_script, "script_hub_get_troop_recruit_type_for_buyer", ":troop_no", ":troop_lord"), # Returns type slot to reg1
					(assign, ":recruiting_pool", reg1),
					(party_get_slot, ":recruits_available", ":center_no", ":recruiting_pool"),
					(ge, ":recruits_available", 1),
					(val_min, ":quantity", ":recruits_available"),
					
					## Check if mounts are available if needed.
					(assign, ":block_purchase", 0),
					(try_begin), # Does the town have enough mounts available if they're required?
						(this_or_next|troop_is_mounted, ":troop_no"),
						(troop_is_guarantee_horse, ":troop_no"),
						(party_get_slot, ":available_mounts", ":center_no", slot_center_horse_pool_player),
						(lt, ":available_mounts", ":quantity"),
						(assign, ":quantity", ":available_mounts"),
						(assign, ":block_purchase", 1),
					(try_end),
					
					## Determine cost for this troop type.
					(call_script, "script_hub_get_purchase_price_for_troop", ":center_no", ":troop_no", "trp_player"), # Returns reg1 (price), reg2 (discount)
					(assign, ":cost_per_troop", reg1),
					## SILVERSTAG EMBLEM+ ## - Temporary & Permanent Hiring Cost Reductions
					(call_script, "script_grt_apply_hiring_bonuses", ":center_no", ":cost_per_troop"),
					(assign, ":cost_per_troop", reg1),
					## SILVERSTAG EMBLEM- ##
					## Verify we have sufficient funds to pay for troops.
					(store_div, ":purchase_limit", ":budget", ":cost_per_troop"),
					(val_min, ":quantity", ":purchase_limit"),
					
					## Purchase the troops
					(try_begin),
						(lt, ":quantity", ":orig_quantity"),
						(assign, ":stop_hiring", 1),
					(try_end),
					(ge, ":quantity", 1),
					(store_mul, ":request_cost", ":cost_per_troop", ":quantity"),
					(val_sub, ":budget", ":request_cost"),
					(try_begin),
						(eq, ":mode", GRT_QUEUE_PROCESS),
						## Actually add the troops to a garrison.
						(party_add_members, ":center_no", ":troop_no", ":quantity"),
						## Remove Quantity from Queue
						(call_script, "script_grt_remove_troop_from_queue", ":center_no", ":troop_no", ":quantity"),
						## Remove Recruits from Pool
						(val_sub, ":recruits_available", ":quantity"),
						(party_set_slot, ":center_no", ":recruiting_pool", ":recruits_available"),
					(else_try),
						(eq, ":mode", GRT_QUEUE_PRINT),
						(assign, reg31, ":quantity"),
						(str_store_troop_name, s31, ":troop_no"),
						(try_begin),
							(ge, ":quantity", 2),
							(str_store_troop_name_plural, s31, ":troop_no"),
						(try_end),
						(assign, reg32, ":request_cost"),
						(str_store_string, s49, "@{s49}{reg31} {s31} will be hired hired for {reg32} denars.^"),
						(val_add, ":line_count", 1),
					(try_end),
				(try_end),
				## Store Excess Budget
				(try_begin),
					(ge, ":budget", 1),
					(party_set_slot, ":center_no", slot_party_queue_budget_excess, ":budget"),
					(eq, ":mode", GRT_QUEUE_PRINT),
					(assign, reg31, ":budget"),
					(str_store_string, s49, "@{s49}^{reg31} denars will be left in excess for next week.^"),
					(val_add, ":line_count", 2),
				(try_end),
				
				
			(else_try),
				### SPLIT BUDGET
				(eq, ":budget_type", GRT_BUDGET_SPLIT),
				(assign, ":excess", 0),
				(store_div, ":budget_divided", ":budget", ":types"),
				### DIAGNOSTIC+ ###
				(try_begin),
					(eq, ":mode", GRT_QUEUE_PRINT),
					(assign, reg31, ":budget_divided"),
					(assign, reg32, ":types"),
					(str_store_string, s49, "@{s49}Split budget for {reg32} types is {reg31} denars.^^"),
					(val_add, ":line_count", 2),
				(try_end),
				### DIAGNOSTIC- ###
				(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
					(neg|party_slot_eq, ":center_no", ":queue_slot", -1), # Empty space.
					(store_add, ":budget_temp", ":budget_divided", ":excess"),
					## Check to see if the main budget was dipped into and the split budget needs to be reduced.
					(val_min, ":budget_temp", ":budget"),
					### DIAGNOSTIC+ ###
					# (assign, reg31, ":budget_temp"),
					# (assign, reg32, ":budget"),
					# (display_message, "@DEBUG (GRT): Split Budget is {reg31} denars with excess added. [Budget = {reg32}]", gpu_debug),
					### DIAGNOSTIC- ###
					(party_get_slot, ":troop_no", ":center_no", ":queue_slot"),
					
					## Figure out our quantity slot.
					(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
					(store_add, ":slot_qty", ":queue_slot", ":offset"),
					(party_get_slot, ":quantity", ":center_no", ":slot_qty"),
					
					## Limit our quantity by how many recruits are available.
					(call_script, "script_hub_get_troop_recruit_type_for_buyer", ":troop_no", ":troop_lord"), # Returns type slot to reg1
					(assign, ":recruiting_pool", reg1),
					(party_get_slot, ":recruits_available", ":center_no", ":recruiting_pool"),
					(ge, ":recruits_available", 1),
					(val_min, ":quantity", ":recruits_available"),
					
					## Check if mounts are available if needed.
					(assign, ":block_purchase", 0),
					(try_begin), # Does the town have enough mounts available if they're required?
						(this_or_next|troop_is_mounted, ":troop_no"),
						(troop_is_guarantee_horse, ":troop_no"),
						(party_get_slot, ":available_mounts", ":center_no", slot_center_horse_pool_player),
						(lt, ":available_mounts", ":quantity"),
						(assign, ":quantity", ":available_mounts"),
						(assign, ":block_purchase", 1),
					(try_end),
					
					## Determine cost for this troop type.
					(call_script, "script_hub_get_purchase_price_for_troop", ":center_no", ":troop_no", "trp_player"), # Returns reg1 (price), reg2 (discount)
					(assign, ":cost_per_troop", reg1),
					## SILVERSTAG EMBLEM+ ## - Temporary & Permanent Hiring Cost Reductions
					(call_script, "script_grt_apply_hiring_bonuses", ":center_no", ":cost_per_troop"),
					(assign, ":cost_per_troop", reg1),
					## SILVERSTAG EMBLEM- ##
					## Verify we have sufficient funds to pay for troops.
					(store_div, ":purchase_limit", ":budget_temp", ":cost_per_troop"),
					## If purchase_limit <= 0, but main budget can support buying 1 then buy 1.
					(try_begin),
						(lt, ":purchase_limit", 1),          # We can't afford even one troop on the split budget.
						(eq, ":block_purchase", 0),          # We have sufficient mounts (if needed).
						(ge, ":budget", ":cost_per_troop"),  # We can afford one troop if we take from the main budget.
						(assign, ":purchase_limit", 1),
						### DIAGNOSTIC+ ###
						# (assign, reg31, ":budget"),
						# (assign, reg32, ":cost_per_troop"),
						# (str_store_troop_name, s31, ":troop_no"),
						# (display_message, "@DEBUG (GRT): Temp_Budget increased to {reg32} denars to afford 1 {s31}.  Main Budget = {reg31} denars.", gpu_debug),
						### DIAGNOSTIC- ###
					(try_end),
					(val_min, ":quantity", ":purchase_limit"),
					
					## Purchase the troops
					(ge, ":quantity", 1),
					(store_mul, ":request_cost", ":cost_per_troop", ":quantity"),
					(val_sub, ":budget_temp", ":request_cost"),
					(val_sub, ":budget", ":request_cost"), # Reduce main budget too for catching big purchases.
					(try_begin),
						(eq, ":mode", GRT_QUEUE_PROCESS),
						## Actually add the troops to a garrison.
						(party_add_members, ":center_no", ":troop_no", ":quantity"),
						## Remove Quantity from Queue
						(call_script, "script_grt_remove_troop_from_queue", ":center_no", ":troop_no", ":quantity"),
						## Remove Recruits from Pool
						(val_sub, ":recruits_available", ":quantity"),
						(party_set_slot, ":center_no", ":recruiting_pool", ":recruits_available"),
					(else_try),
						(eq, ":mode", GRT_QUEUE_PRINT),
						(assign, reg31, ":quantity"),
						(str_store_troop_name, s31, ":troop_no"),
						(try_begin),
							(ge, ":quantity", 2),
							(str_store_troop_name_plural, s31, ":troop_no"),
						(try_end),
						(assign, reg32, ":request_cost"),
						(str_store_string, s49, "@{s49}{reg31} {s31} will be hired for {reg32} denars.^"),
						(val_add, ":line_count", 1),
					(try_end),
					
					## Store Excess Budget
					(try_begin),
						(ge, ":budget_temp", 1),
						(assign, ":excess", ":budget_temp"),
					(try_end),
				(try_end),
				
				
			(else_try),
				### ERROR
				(str_store_party_name, s31, ":center_no"),
				(display_message, "@ERROR - Unrecognized garrison budget type for {s31}.", gpu_red),
			(try_end),
			
			(try_begin),
				(eq, ":mode", GRT_QUEUE_PRINT),
				(store_sub, ":diff_lines", 12, ":line_count"),
				(ge, ":diff_lines", 1),
				(try_for_range, ":unused", 0, ":diff_lines"),
					(str_store_string, s49, "@{s49}^"),
				(try_end),
			(try_end),
			
			(call_script, "script_grt_tidy_queue", ":center_no"),
		(try_end),
	]),
	
# script_grt_apply_hiring_bonuses
# PURPOSE: Reduces the cost per troop at a location based upon temporary and permanent bonuses applied.
# EXAMPLE: (call_script, "script_grt_apply_hiring_bonuses", ":center_no", ":cost_per_troop"), # garrison_scripts.py
("grt_apply_hiring_bonuses",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":cost_per_troop", 2),
		
		(assign, ":total_discount", 0),
		
		# Permanent Reduction
		(try_begin),
			(party_slot_ge, ":center_no", slot_center_training_cost_reduction, 1), # Effect is valid.
			(party_get_slot, ":permanent_effect", ":center_no", slot_center_training_cost_reduction),
			(val_mul, ":permanent_effect", EMBLEM_EFFECT_TRAINING_PERM_REDUCTION),
			(val_add, ":total_discount", ":permanent_effect"),
			(store_mul, ":reduction_perm", ":cost_per_troop", ":permanent_effect"),
			(val_div, ":reduction_perm", 100),
		(else_try),
			(assign, ":reduction_perm", 0),
		(try_end),
		
		# Temporary Reduction
		(try_begin),
			(party_slot_ge, ":center_no", slot_center_queue_cost_reduce_duration, 1), # Effect is valid.
			(store_mul, ":reduction_temp", ":cost_per_troop", EMBLEM_EFFECT_TRAINING_TEMP_REDUCTION),
			(val_div, ":reduction_temp", 100),
			(val_add, ":total_discount", EMBLEM_EFFECT_TRAINING_TEMP_REDUCTION),
		(else_try),
			(assign, ":reduction_temp", 0),
		(try_end),
		(val_sub, ":cost_per_troop", ":reduction_perm"),
		(val_sub, ":cost_per_troop", ":reduction_temp"),
		
		(assign, reg1, ":cost_per_troop"),
		(assign, reg2, ":total_discount"),
	]),
	
# script_grt_print_queue
# PURPOSE: Used for debugging, this script prints out the contents of the queue to s41.
# EXAMPLE: (call_script, "script_grt_print_queue", ":center_no"), # garrison_scripts.py
("grt_print_queue",
    [
		(store_script_param, ":center_no", 1),
		
		(str_clear, s41),
		(try_for_range, ":queue_slot", slot_party_queue_slot_id_begin, slot_party_queue_slot_id_end),
			(party_get_slot, ":troop_no", ":center_no", ":queue_slot"),
			## Figure out our quantity slot.
			(store_sub, ":offset", slot_party_queue_slot_quantity_begin, slot_party_queue_slot_id_begin),
			(store_add, ":slot_qty", ":queue_slot", ":offset"),
			(party_get_slot, ":quantity", ":center_no", ":slot_qty"),
			## Report Information
			# Slot #
			(store_sub, reg30, ":queue_slot", slot_party_queue_slot_id_begin),
			(str_store_string, s30, "@#{reg30}   "),
			# Troop ID
			(try_begin),
				# (eq, ":troop_no", 0),
				# (str_store_string, s31, "@ERROR (0)   "),
			# (else_try),
				# (eq, ":troop_no", -1),
				# (str_store_string, s31, "@Empty Slot (0)   "),
			# (else_try),
				(neq, ":troop_no", 0),
				(neq, ":troop_no", -1),
				(call_script, "script_hub_get_purchase_price_for_troop", ":center_no", ":troop_no", "trp_player"), # Returns reg1 (price), reg2 (discount)
				(assign, reg31, reg1),
				(str_store_troop_name, s32, ":troop_no"),
				(str_store_string, s31, "@{s32} ({reg31} /ea)   "),
				# Quantity
				(assign, reg32, ":quantity"),
				(str_store_string, s33, "@{reg32} requested"),
				# Display
				(str_store_string, s41, "@{s41}{s30}{s31}{s33}^"),
			(try_end),
			
		(try_end),
		
	]),
	
# script_grt_create_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate this code for each window.
("grt_create_mode_switching_buttons",
    [
		### COMMON ELEMENTS ###
		(assign, "$gpu_storage", GRT_OBJECTS),
		(assign, "$gpu_data",    GRT_OBJECTS),
		(call_script, "script_gpu_draw_line", 850, 2, 73, 650, gpu_gray), # - Footer
		
		# Wipe clean GRT_OBJECTS
		(try_for_range, ":slot", 0, 400),
			(troop_set_slot, GRT_OBJECTS, ":slot", 0),
		(try_end),
		
		# Setup an initial false value for objects so if they don't get loaded they aren't 0's.
		(try_for_range, ":slot_no", grt_obj_button_general, grt_obj_container_1),
			(store_add, ":value", ":slot_no", 1234),
			(troop_set_slot, GRT_OBJECTS, ":slot_no", ":value"),
		(try_end),
		
		# Text Labels
		(str_store_party_name, s22, "$current_town"),
		(str_store_string, s21, "@{s22}'s Garrison"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, grt_obj_label_main_title, gpu_center), # 680
		(call_script, "script_gpu_resize_object", grt_obj_label_main_title, 150),
		
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 665, grt_obj_label_main_title2, gpu_center), # 680
		(call_script, "script_gpu_resize_object", grt_obj_label_main_title2, 150),
		
		## CONTAINERS ##
		(call_script, "script_gpu_container_heading", 50, 80, 175, 505, grt_obj_container_1),
			
			
			## BUTTONS ##
			(assign, ":x_buttons", 0), # 90 
			(assign, ":y_button_step", 55),
			(assign, ":pos_y", 420),
			(call_script, "script_gpu_create_button", "str_grt_general", ":x_buttons", ":pos_y", grt_obj_button_general), ### GENERAL ###
			(val_sub, ":pos_y", ":y_button_step"),
			(call_script, "script_gpu_create_button", "str_grt_current_queue", ":x_buttons", ":pos_y", grt_obj_button_queue), ### QUEUE ###
			(val_sub, ":pos_y", ":y_button_step"),
			(call_script, "script_gpu_create_button", "str_grt_recruitment", ":x_buttons", ":pos_y", grt_obj_button_recruitment), ### RECRUITMENT ###
			(val_sub, ":pos_y", ":y_button_step"),
			(call_script, "script_gpu_create_button", "str_grt_training", ":x_buttons", ":pos_y", grt_obj_button_training), ### TRAINING ###
			(val_sub, ":pos_y", ":y_button_step"),
			(str_store_string, s21, "@Emblem Options"),
			(call_script, "script_gpu_create_button", "str_grt_s21", ":x_buttons", ":pos_y", grt_obj_button_emblems), ### EMBLEM OPTIONS ###
			# (val_sub, ":pos_y", ":y_button_step"),
			# (call_script, "script_gpu_create_button", "str_grt_reordering", ":x_buttons", ":pos_y", grt_obj_button_reorder), ### REORDERING ###
			
			(try_begin),
				(ge, DEBUG_GARRISON, 1),
				(is_presentation_active, "prsnt_garrison_queue"),
				(val_sub, ":pos_y", ":y_button_step"),
				(val_sub, ":pos_y", 20),
				(call_script, "script_gpu_create_text_label", "str_grt_debug_advance_label", ":x_buttons", ":pos_y", 0, gpu_left),
				(call_script, "script_gpu_create_text_label", "str_grt_debug_advance_label", ":x_buttons", ":pos_y", 0, gpu_left),
				(val_sub, ":pos_y", 40),
				(call_script, "script_gpu_create_button", "str_grt_debug_advance", ":x_buttons", ":pos_y", grt_obj_button_debug_advance),
			(try_end),
			
		(set_container_overlay, -1),
		(call_script, "script_gpu_create_mesh", "mesh_button_up", 55, 35, 350, 500),
		(call_script, "script_gpu_create_button", "str_grt_done", 65, 40, grt_obj_button_done),
	]),
	
# script_grt_handle_mode_switching_buttons
# PURPOSE: These button declarations are common to each presentation mode so this prevents needing to recreate the code to handle their functionality for each window.
("grt_handle_mode_switching_buttons",
    [
		(store_script_param, ":object", 1),
		(store_script_param, ":value", 2),
		(assign, reg15, ":value"), # So it won't be whined about.
		
		# hub_obj_button_general_info            = 3
		# hub_obj_button_finances                = 4
		# hub_obj_button_improvements            = 5
		# hub_obj_button_recruitment             = 6
		# hub_obj_button_advisors                = 7
		# hub_obj_button_garrison                = 8
		# hub_obj_button_quests                  = 9
		
		### COMMON ELEMENTS ###
		(try_begin), ####### DONE BUTTON #######
			(troop_slot_eq, GRT_OBJECTS, grt_obj_button_done, ":object"),
			(assign, "$hub_mode", HUB_MODE_GENERAL),
			(assign, "$grt_mode", GARRISON_MODE_GENERAL),
			# If we're in the Garrison Training UI we need to clear the temporary party.
			(try_begin),
				(is_presentation_active, "prsnt_garrison_training"),
				(assign, ":party_temp", "p_temp_party"),
				(call_script, "script_clear_party_group", ":party_temp"),
				(ge, DEBUG_GARRISON, 1),
				(display_message, "@DEBUG (GRT): Temporary party cleared. (done exit)", gpu_debug),
			(try_end),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_hub_switch_modes"),
			
		(else_try), ####### BUTTON : GARRISON INFORMATION #######
			(troop_slot_eq, GRT_OBJECTS, grt_obj_button_general, ":object"),
			(assign, "$grt_mode", GARRISON_MODE_GENERAL),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_garrison_switch_modes"),
			
		(else_try), ####### BUTTON : CURRENT QUEUE #######
			(troop_slot_eq, GRT_OBJECTS, grt_obj_button_queue, ":object"),
			(assign, "$grt_mode", GARRISON_MODE_QUEUE),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_garrison_switch_modes"),
			
		(else_try), ####### BUTTON : GARRISON RECRUITMENT #######
			(troop_slot_eq, GRT_OBJECTS, grt_obj_button_recruitment, ":object"),
			(assign, "$grt_mode", GARRISON_MODE_RECRUITMENT),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_garrison_switch_modes"),
			
		(else_try), ####### BUTTON : GARRISON TRAINING #######
			(troop_slot_eq, GRT_OBJECTS, grt_obj_button_training, ":object"),
			(assign, "$grt_mode", GARRISON_MODE_TRAINING),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_garrison_switch_modes"),
			
		(else_try), ####### BUTTON : GARRISON REORDERING #######
			(troop_slot_eq, GRT_OBJECTS, grt_obj_button_reorder, ":object"),
			(assign, "$grt_mode", GARRISON_MODE_REORDER),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_garrison_switch_modes"),
			
		(else_try), ####### BUTTON : EMBLEM OPTIONS #######
			(troop_slot_eq, GRT_OBJECTS, grt_obj_button_emblems, ":object"),
			(assign, "$grt_mode", GARRISON_MODE_EMBLEM_OPTIONS),
			(presentation_set_duration, 0),
			(jump_to_menu, "mnu_garrison_switch_modes"),
			
		
			
		(try_end),
	]),
	
# script_grt_garrison_troop_get_info
# PURPOSE: Print an info box about a troop for the "recruitment" presentation.
("grt_garrison_troop_get_info",
    [
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":pos_y", 2),
		
		## OBJ - TROOP IMAGE
		(store_sub, ":pos_y_portrait", ":pos_y", 100),
		# script_gpu_create_portrait     - troop_id, pos_x, pos_y, size, storage_id
		(call_script, "script_gpu_create_troop_image", ":troop_no", -15, ":pos_y_portrait", 400, 0),
		
		## OBJ - TROOP NAME
		(store_sub, ":pos_y_line_1", ":pos_y", 0),
		(assign, ":pos_x_col_1", 95),
		(str_store_troop_name, s21, ":troop_no"),
		(str_store_troop_name, s22, ":troop_no"),
		# If troop is a unique location troop then change the name color to a goldish hue.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION),
			(assign, ":color", 10714113), # Goldish yellow.
			(str_store_string, s22, "@{s22} (Unique)"),
		(else_try),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION_UPGRADE),
			(assign, ":color", 10714113), # Goldish yellow.
			(str_store_string, s22, "@{s22} (Unique)"),
		(else_try),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_AFFILIATED),
			(assign, ":color", 101), # Dark Blue
			(str_store_string, s22, "@{s22} (Faction Only)"),
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
			(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(str_store_string, s22, "@Faction Troop"),
		(else_try),
			(is_between, ":troop_no", bandits_begin, bandits_end),
			(str_store_string, s22, "@Outlaw"),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_MERCENARY),
			(str_store_string, s22, "@Mercenary"),
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
		
		# ## OBJ - NUMBER OF MEMBERS
		# (party_count_companions_of_type, reg21, "$current_town", ":troop_no"),
		# (store_add, ":pos_x_temp", ":pos_x_col_1", 550),
		# (call_script, "script_gpu_create_text_label", "str_grt_garrison_count", ":pos_x_temp", ":pos_y_line_1", 0, gpu_right),
		# # (call_script, "script_gpu_create_text_label", "str_grt_garrison_count", ":pos_x_temp", ":pos_y_line_1", 0, gpu_right),
		
		## LABEL - RECRUITMENT REQUIREMENTS
		(store_add, ":pos_x_col_2", ":pos_x_col_1", 200),
		(call_script, "script_gpu_create_text_label", "str_grt_troop_info", ":pos_x_col_2", ":pos_y_line_2", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_gpu_create_text_label", "str_grt_troop_info", ":pos_x_col_2", ":pos_y_line_2", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(assign, ":pos_y_temp", ":pos_y_line_2"),
		
		## OBJ - NUMBER OF MEMBERS
		(party_count_companions_of_type, reg21, "$current_town", ":troop_no"),
		(val_sub, ":pos_y_temp", 20),
		(call_script, "script_gpu_create_text_label", "str_grt_garrison_count", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - UPKEEP COSTS (per troop)
		(call_script, "script_game_get_troop_wage", ":troop_no", "$current_town"),
		(store_div, reg21, reg0, 2),
		(val_sub, ":pos_y_temp", 20),
		(call_script, "script_gpu_create_text_label", "str_grt_troop_wages", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - UPKEEP COSTS (total)
		(party_count_companions_of_type, reg21, "$current_town", ":troop_no"),
		(call_script, "script_game_get_troop_wage", ":troop_no", "$current_town"),
		(store_div, ":cost_per_troop", reg0, 2),
		(store_mul, reg22, ":cost_per_troop", reg21),
		(val_sub, ":pos_y_temp", 20),
		(call_script, "script_gpu_create_text_label", "str_grt_troop_wages_total", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		
	]),
	
# script_grt_troop_get_recruitment_info
# PURPOSE: Print an info box about a troop for the "recruitment" presentation.
("grt_troop_get_recruitment_info",
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
		(store_add, ":obj_slot", grt2_obj_button_inspect_equipment, ":record"),
		(call_script, "script_gpu_create_troop_image", ":troop_no", -15, ":pos_y_portrait", 400, ":obj_slot"),
		
		## OBJ - NUMBER OF MEMBERS
		# (party_count_companions_of_type, reg21, "$current_town", ":troop_no"),
		(call_script, "script_grt_get_queue_count_for_troop", "$current_town", ":troop_no"), # garrison_scripts.py
		(assign, reg21, reg1),
		(store_sub, ":pos_y_troop_count", ":pos_y", 105),
		(call_script, "script_gpu_create_text_label", "str_grt_queue_count", 42, ":pos_y_troop_count", 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 75),
		
		## OBJ - TROOP NAME
		(store_sub, ":pos_y_line_1", ":pos_y", 0),
		(assign, ":pos_x_col_1", 95),
		(str_store_troop_name, s21, ":troop_no"),
		(str_store_troop_name, s22, ":troop_no"),
		# If troop is a unique location troop then change the name color to a goldish hue.
		(try_begin),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION),
			(assign, ":color", 10714113), # Goldish yellow.
			(str_store_string, s22, "@{s22} (Unique)"),
		(else_try),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION_UPGRADE),
			(assign, ":color", 10714113), # Goldish yellow.
			(str_store_string, s22, "@{s22} (Unique)"),
		(else_try),
			(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_AFFILIATED),
			(assign, ":color", 101), # Dark Blue
			(str_store_string, s22, "@{s22} (Faction Only)"),
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
			(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(str_store_string, s22, "@Faction Troop"),
		(else_try),
			(is_between, ":troop_no", bandits_begin, bandits_end),
			(str_store_string, s22, "@Outlaw"),
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_recruit_type, STRT_MERCENARY),
			(str_store_string, s22, "@Mercenary"),
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
		(store_add, ":pos_x_col_2", ":pos_x_col_1", 200),
		(call_script, "script_gpu_create_text_label", "str_hub_troop_prereqs", ":pos_x_col_2", ":pos_y_line_2", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(call_script, "script_gpu_create_text_label", "str_hub_troop_prereqs", ":pos_x_col_2", ":pos_y_line_2", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(assign, ":pos_y_temp", ":pos_y_line_2"),
		
		## OBJ - REQUIREMENT - PURCHASE COST.
		(val_sub, ":pos_y_temp", 20),
		(call_script, "script_hub_get_purchase_price_for_troop", "$current_town", ":troop_no", "trp_player"), # Returns reg1 (price), reg2 (discount)
		(assign, ":cost_per_troop", reg1),
		(assign, ":discount", reg2),
		(call_script, "script_grt_apply_hiring_bonuses", "$current_town", ":cost_per_troop"),
		(assign, reg21, reg1),
		(val_add, ":discount", reg2),
		(assign, ":modified_cost", reg1),
		(try_begin),
			(neq, ":discount", 0),
			(assign, reg2, ":discount"),
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
			(try_end),
		(try_end),
		
		## OBJ - REQUIREMENT - AFFILIATED
		(try_begin),
			(assign, ":continue", 0),
			(try_begin),
				(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_AFFILIATED), # combat_scripts.py - prereq constants in combat_constants.py
				(assign, ":continue", 1),
			(else_try),
				(call_script, "script_cf_ce_troop_has_requirement", ":troop_no", PREREQ_UNIQUE_LOCATION), # combat_scripts.py - prereq constants in combat_constants.py
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			(val_sub, ":pos_y_temp", 20),
			(store_faction_of_party, ":faction_no", "$current_town"),
			(str_store_faction_name, s21, ":faction_no"),
			(call_script, "script_gpu_create_text_label", "str_hub_prereq_affiliated", ":pos_x_col_2", ":pos_y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
			(try_begin),
				(store_faction_of_party, ":faction_no", "$current_town"),
				(eq, ":faction_no", "$players_kingdom"),
				(overlay_set_color, reg1, ":color_good"),
			(else_try),
				(overlay_set_color, reg1, ":color_bad"),
				# (assign, ":disable_recruitment", 1),
			(try_end),
		(try_end),
		
		## BUTTON - INSPECT EQUIPMENT
		# (store_sub, ":pos_y_button_1", ":pos_y", 35),
		# (store_sub, ":pos_y_button_1_mesh", ":pos_y_button_1", 10),
		# (store_add, ":button_obj_slot", grt2_obj_button_inspect_equipment, ":record"),
		# (call_script, "script_gpu_create_mesh", "mesh_button_up", 545, ":pos_y_button_1_mesh", 600, 500),
		# (call_script, "script_gpu_create_button", "str_hub_button_inspect_gear", 558, ":pos_y_button_1", ":button_obj_slot"),
		# (call_script, "script_gpu_resize_object", ":button_obj_slot", 75),
		
		## Define the troop # in each record.
		(store_add, ":button_val_slot", grt2_val_button_troop_no, ":record"),
		(troop_set_slot, GRT_OBJECTS, ":button_val_slot", ":troop_no"),
		
		## BUTTON - QUEUE TROOP
		(store_sub, ":pos_y_button_2", ":pos_y", 35),
		# (store_sub, ":pos_y_button_2", ":pos_y_button_1", 45),
		(store_sub, ":pos_y_button_2_mesh", ":pos_y_button_2", 10),
		(store_add, ":button_obj_slot", grt2_obj_button_recruit_troop, ":record"),
		(try_begin),
			(eq, ":recruitable", 1), # So we can dump troops of the wrong type.
			(call_script, "script_gpu_create_mesh", "mesh_button_up", 545, ":pos_y_button_2_mesh", 600, 500),
			(call_script, "script_gpu_create_button", "str_grt_button_recruit", 573, ":pos_y_button_2", ":button_obj_slot"),
			(call_script, "script_gpu_resize_object", ":button_obj_slot", 75),
		(else_try),
			(store_add, ":pos_y_disabled", ":pos_y_button_2", 10),
			(call_script, "script_gpu_create_mesh", "mesh_button_down", 545, ":pos_y_button_2_mesh", 600, 500),
			(call_script, "script_gpu_create_text_label", "str_grt_button_recruit", 620, ":pos_y_disabled", 0, gpu_center),
			(overlay_set_color, reg1, gpu_gray),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
		
		## BUTTON - REMOVE TROOP
		(store_sub, ":pos_y_button_3", ":pos_y_button_2", 47),
		(store_sub, ":pos_y_button_3_mesh", ":pos_y_button_3", 10),
		(store_add, ":button_obj_slot", grt2_obj_button_dismiss_troop, ":record"),
		(try_begin),
			(call_script, "script_grt_get_queue_count_for_troop", "$current_town", ":troop_no"),
			(ge, reg1, 1),
			(call_script, "script_gpu_create_mesh", "mesh_button_up", 545, ":pos_y_button_3_mesh", 600, 500),
			(call_script, "script_gpu_create_button", "str_grt_button_dismiss", 552, ":pos_y_button_3", ":button_obj_slot"),
			(call_script, "script_gpu_resize_object", ":button_obj_slot", 75),
		(else_try),
			(store_add, ":pos_y_disabled", ":pos_y_button_3", 10),
			(call_script, "script_gpu_create_mesh", "mesh_button_down", 545, ":pos_y_button_3_mesh", 600, 500),
			(call_script, "script_gpu_create_text_label", "str_grt_button_dismiss", 619, ":pos_y_disabled", 0, gpu_center),
			(overlay_set_color, reg1, gpu_gray),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
		
		## BUTTON - QUEUE AMOUNT
		(store_sub, ":pos_y_button_4", ":pos_y_button_3", 45),
		(store_add, ":button_obj_slot", grt2_obj_numbox_queue_qty, ":record"),
		(str_store_string, s21, "@Amount:"),
		(call_script, "script_gpu_create_number_box", 621, ":pos_y_button_4", 0, 250, ":button_obj_slot", 0),
		(overlay_set_val, reg1, 0),
		(store_add, ":pos_y_button_4_text", ":pos_y_button_4", 16),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 551, ":pos_y_button_4_text", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		
	]),
	
# script_grt_get_gold_to_xp_training_ratio
# PURPOSE: This returns the amount of gold required for each point of experience added to a garrison.
# EXAMPLE: (call_script, "script_grt_get_gold_to_xp_training_ratio", ":center_no"),
("grt_get_gold_to_xp_training_ratio",
    [
		(store_script_param, ":center_no", 1),
		
		(assign, ":xp_ratio", 65), # Sets our default value.
		
		## IMPROVEMENT BONUSES
		(try_begin),
			(party_slot_ge, "$current_town", slot_center_has_training_grounds, cis_built),
			(val_add, ":xp_ratio", GRT_FUNDEFF_TRAINING_GROUNDS),
		(try_end),
		
		## CAPTAIN OF THE GUARDS BONUS
		(try_begin),
			(party_get_slot, ":advisor_captain", ":center_no", slot_center_advisor_war),
			(is_between, ":advisor_captain", companions_begin, companions_end),
			(store_skill_level, ":skill_training", "skl_trainer", ":advisor_captain"),
			(val_mul, ":skill_training", 4),
			(val_add, ":xp_ratio", ":skill_training"),
		(try_end),
		
		## FACTION BONUS
		
		## EMBLEM BONUS
		(try_begin),
			(this_or_next|party_slot_ge, ":center_no", slot_center_training_emblem_duration, 1), # Temporary Boost
			(party_slot_eq, ":center_no", slot_center_training_emblem_duration, -1), # Permanent Boost
			(val_add, ":xp_ratio", GRT_FUNDEFF_EMBLEM_BONUS),
		(try_end),
		
		(assign, reg1, ":xp_ratio"),
	]),
	
# script_grt_convert_gold_to_xp_training
# PURPOSE: This script directly upgrades a city's garrison based upon an input amount of gold.
# EXAMPLE: (call_script, "script_grt_convert_gold_to_xp_training", ":center_no", ":budget"),
("grt_convert_gold_to_xp_training",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":budget", 2),
		(store_script_param, ":mode", 3),
		
		(try_begin),
			(str_store_string, s19, "@GRT Training Blocked: No budget allocated for training."),
			(ge, ":budget", 0),
			# FILTER - Training is enabled.
			(str_store_string, s19, "@GRT Training Blocked: Training is disabled."),
			(party_slot_eq, "$current_town", slot_center_upgrade_garrison, 1),
			# FILTER - We have a valid captain of the guard stationed.
			(str_store_string, s19, "@GRT Training Blocked: No Captain of the Guards stationed here."),
			(party_get_slot, ":advisor_captain", "$current_town", slot_center_advisor_war),
			(is_between, ":advisor_captain", companions_begin, companions_end),
			
			(call_script, "script_grt_get_gold_to_xp_training_ratio", "$current_town"),
			(store_mul, ":xp_gain", ":budget", reg1),
			(val_div, ":xp_gain", 100),
			(try_begin),
				(eq, ":mode", GRT_TRAINING_PREVIEW),
				(party_add_xp, ":center_no", ":xp_gain"),
			(else_try),
				(eq, ":mode", GRT_TRAINING_PROCESS),
				(party_upgrade_with_xp, ":center_no", ":xp_gain", 0),
			(try_end),
			
			### DIAGNOSTIC+ ###
			(try_begin),
				(ge, DEBUG_GARRISON, 1),
				(assign, reg2, ":budget"),
				(assign, reg3, ":xp_gain"),
				(str_store_party_name, s21, ":center_no"),
				(display_message, "@DEBUG (GRT): {s21}'s training budget of {reg2} denars converts to +{reg3}xp. ({reg1}% conversion)", gpu_debug),
			(try_end),
			### DIAGNOSTIC- ###
		(else_try),
			(ge, DEBUG_GARRISON, 1),
			(display_message, "@DEBUG (GRT): {s19}", gpu_debug),
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