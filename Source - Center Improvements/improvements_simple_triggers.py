# Center Improvements (1.0) by Windyplains

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
## WINDYPLAINS+ ## - Altered center improvements to allow queing up to 3 at a time.
  # Checking center upgrades
  (12,
	[
		(try_for_range, ":center_no", centers_begin, centers_end),
			(try_for_range, ":building_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
				(party_get_slot, ":improvement", ":center_no", ":building_slot"),
				(store_add, ":end_time_slot", ":building_slot", 3),
				(gt, ":improvement", 0),
				(party_get_slot, ":cur_improvement_end_time", ":center_no", ":end_time_slot"),
				(store_current_hours, ":cur_hours"),
				(ge, ":cur_hours", ":cur_improvement_end_time"),
				(try_begin),
					(party_slot_ge, ":center_no", ":improvement", 2),
					(str_store_string, s21, "@Repair"),
					(str_store_string, s23, "@repairing the"),
				(else_try),
					(str_store_string, s21, "@Building"),
					(str_store_string, s23, "@building a"),
				(try_end),
				(party_set_slot, ":center_no", ":improvement", cis_built),
				(party_set_slot, ":center_no", ":building_slot", 0),
				(call_script, "script_get_improvement_details", ":improvement"),
				(str_store_party_name, s4, ":center_no"),
				(try_begin),
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(display_log_message, "@{s21} of the {s0} in {s4} has been completed.", gpu_green),
				(else_try),
					(ge, DEBUG_IMPROVEMENTS, 1),
					(party_get_slot, ":lord", ":center_no", slot_town_lord),
					(try_begin),
						(this_or_next|is_between, ":lord", active_npcs_begin, active_npcs_end),
						(eq, ":lord", "trp_player"),
						(str_store_troop_name, s22, ":lord"),
					(else_try),
						(str_store_string, s22, "@(Unassigned Lord)"),
					(try_end),
					(display_log_message, "@{s22} has completed {s23} {s0} in {s4}.", gpu_debug),
				(try_end),
				(call_script, "script_improvement_completion_benefits", ":improvement", ":center_no"),
			(try_end),

		(try_end),
    ]),
	
# Check to see if centers gain additional prosperity improvements towards their ideal values.
(24,
	[
		(try_for_range, ":center_no", centers_begin, centers_end),
			# Get prosperity values.
			(call_script, "script_get_center_ideal_prosperity", ":center_no"),
			(assign, ":ideal_prosperity", reg0),
			(party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
			# Determine if we're below ideal.
			(lt, ":prosperity", ":ideal_prosperity"),
			(assign, ":prosperity_boost", 0),
			
			### IMPROVEMENT [ Improved Roads ] - Enhanced restoration of prosperity.
			(try_begin),
				(party_slot_eq, ":center_no", slot_center_has_improved_roads, cis_built),
				(val_add, ":prosperity_boost", 1),
			(try_end),
			
			### ENHANCED DIPLOMACY+ ###
			(store_faction_of_party, ":faction_no", ":center_no"),
			(faction_get_slot, ":fief_recovery", ":faction_no", slot_faction_prosperity_recovery),
			(val_div, ":fief_recovery", 100),
			(val_add, ":prosperity_boost", ":fief_recovery"),
			
			# (store_add, ":boost", ":prosperity_boost", 1),
			# (store_faction_of_party, ":faction_no", ":center_no"),
			# (faction_get_slot, ":recovery_rate", ":faction_no", slot_faction_prosperity_recovery),
			# (val_mul, ":boost", ":recovery_rate"),
			# (val_div, ":boost", 100),
			# (val_add, ":prosperity_boost", ":boost"),
			### ENHANCED DIPLOMACY- ###
			
			# Make changes if needed.
			(gt, ":prosperity_boost", 0),
			(call_script, "script_change_center_prosperity", ":center_no", ":prosperity_boost"),
			(val_add, "$newglob_total_prosperity_from_convergence", ":prosperity_boost"),
			### DIAGNOSTIC ###
			(ge, DEBUG_IMPROVEMENTS, 1),
			(this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(ge, DEBUG_IMPROVEMENTS, 2),
			(str_store_party_name, s21, ":center_no"),
			(assign, reg21, ":prosperity"),
			(assign, reg22, ":ideal_prosperity"),
			(assign, reg23, ":prosperity_boost"),
			(display_message, "@DEBUG: {s21} has {reg21} of {reg22} ideal prosperity.  Improvement by {reg23}.", gpu_debug),
		(try_end),
    ]),
	
# LORD AI - Building improvements in centers.
(12,
	[
		(try_for_range, ":center_no", centers_begin, centers_end),
			(neg|party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
			(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
			(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
			
			(store_faction_of_party, ":faction_no", ":center_no"),
			(str_store_troop_name, s21, ":troop_no"),
			(str_store_faction_name, s22, ":faction_no"),
			
			# Is the lord near this center?
			(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
			(ge, ":party_no", 0),
			(party_is_active, ":party_no"), # Bugfix - Prevent party numbers stored in this slot that are now inactive from being invalid.
			(store_distance_to_party_from_party, ":distance", ":center_no", ":party_no"),
			(lt, ":distance", 5),
			# Make sure the fief isn't looted if it is a village.
			(this_or_next|neg|party_slot_eq, ":center_no", slot_village_state, svs_looted),
			(neg|party_slot_eq, ":center_no", slot_party_type, spt_village),
			(str_store_party_name, s23, ":center_no"),
			
			# Are any spaces available to build improvements?
			(try_begin),
				(this_or_next|party_slot_eq, ":center_no", slot_center_current_improvement_1, 0),
				(this_or_next|party_slot_eq, ":center_no", slot_center_current_improvement_2, 0),
				(party_slot_eq, ":center_no", slot_center_current_improvement_3, 0),
				(assign, ":continue", 1),
			(else_try),
				(assign, ":continue", 0),
			(try_end),
			(eq, ":continue", 1),
			
			# How much can the lord afford to spend?
			(troop_get_slot, ":wealth", ":troop_no", slot_troop_wealth),
			(store_mul, ":budget", ":wealth", 20),
			(val_div, ":budget", 100),
			
			(assign, ":improvement_built", 0),
			(try_for_range, ":current_count", native_improvements_begin, center_improvements_end),
				(eq, ":improvement_built", 0),
				(store_sub, ":counter", ":current_count", native_improvements_begin),
				(call_script, "script_cf_improvement_get_priority_for_ai", ":counter"),
				(assign, ":improvement", reg1),
				
				(call_script, "script_get_improvement_details", ":improvement"),
				
				# Prevent the need for two loops, but make sure we only affect improvement slots.
				(this_or_next|is_between, ":improvement", native_improvements_begin, native_improvements_end),
				(is_between, ":improvement", center_improvements_begin, center_improvements_end),
				
				# Can this improvement be built here?
				(neg|party_slot_ge, ":center_no", ":improvement", cis_built),
				(call_script, "script_improvement_store_ai_building_cost_to_reg1_and_time_to_reg2", ":improvement", ":center_no"),
				(assign, ":cost", reg1),
				(assign, reg51, reg2),
				(ge, ":budget", ":cost"),
				(call_script, "script_cf_improvement_can_be_built_here", ":center_no", ":improvement"),
				
				# Improvement can be built, so build it.
				(assign, ":continue", 1),
				(try_for_range, ":improvement_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
					(eq, ":continue", 1),
					(party_slot_eq, ":center_no", ":improvement_slot", 0), # Nothing currently being built in this slot.
					(assign, ":continue", 0),
					(party_set_slot, ":center_no", ":improvement_slot", ":improvement"),
					(store_current_hours, ":cur_hours"),
					(store_mul, ":hours_takes", reg51, 24),
					(val_add, ":hours_takes", ":cur_hours"),
					(store_add, ":end_time_slot", ":improvement_slot", 3),
					(party_set_slot, ":center_no", ":end_time_slot", ":hours_takes"),
					(assign, ":improvement_built", ":improvement"),
					(break_loop),
				(try_end),
				(eq, ":continue", 0),
				(break_loop),
			(try_end),
			### DIAGNOSTIC ###
			(ge, DEBUG_IMPROVEMENTS, 1),
			(ge, ":improvement_built", 1),
			(call_script, "script_get_improvement_details", ":improvement_built"),
			(display_message, "@{s21} of the {s22} has begun work on a {s0} in {s23}.  It will take {reg51} days.", gpu_debug),
		(try_end),
    ]),
## WINDYPLAINS- ##

# Checking for parties near a hostile castle.
  (72,
	[
		
		# (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			# # (store_faction_of_party, ":faction_center", ":center_no"),
			
			# # (try_begin),
				# # (try_for_parties, ":party_no"),
					# # (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
					# # (eq, ":party_no", "p_main_party"),
					# # (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), # Don't pull defenders away while you're under siege.
					# # (store_faction_of_party, ":faction_no", ":party_no"),
					# # (neq, ":faction_no", ":faction_center"),
					# # (store_relation, ":relation", ":faction_no", ":faction_center"),
					# # (lt, ":relation", -20),
					# # (store_distance_to_party_from_party, reg21, ":center_no", ":party_no"),
					# # (lt, reg21, 5),
					# # # (assign, reg22, ":relation"),
					# # # (str_store_party_name, s21, ":center_no"),
					# # # (str_store_party_name, s22, ":party_no"),
					# # # (display_message, "@{s21} sees {s22} passing nearby at a range of {reg21} and relation {reg22}.", gpu_light_blue),
					# # ## CREATE INTERCEPT PARTY ##
					# # (party_get_slot, ":current_patrol", ":center_no", slot_center_patrol_party),
					# # (try_begin),
						# # (le, ":current_patrol", 0),
						# # (call_script, "script_castle_patrol_action", castle_patrol_create, -1, ":center_no"),
						# # (call_script, "script_castle_patrol_action", castle_patrol_engage_party, reg51, ":party_no"),
					# # (try_end),
					
				# # (try_end),
			# # (try_end),
			
			# (try_begin),
				# (party_get_slot, ":current_patrol", ":center_no", slot_center_patrol_party),
				# (ge, ":current_patrol", 1),
				# (try_begin),
					# (party_is_active, ":current_patrol"),
					# (party_get_slot, ":home_center", ":current_patrol", slot_party_caravan_origin),
					# (try_begin),
						# ## Patrol is active and stationed in their home center.
						# (party_is_active, ":current_patrol"),
						# (is_between, ":home_center", walled_centers_begin, walled_centers_end),
						# (party_get_cur_town, ":current_center", ":current_patrol"),
						# (eq, ":current_center", ":home_center"),
						# (call_script, "script_castle_patrol_action", castle_patrol_merge_with_center, ":current_patrol", ":home_center"),
					# (else_try),
						# ## Patrol is in pursuit, but is too far from home.
						# (party_is_active, ":current_patrol"),
						# (is_between, ":home_center", walled_centers_begin, walled_centers_end),
						# (store_distance_to_party_from_party, reg21, ":home_center", ":current_patrol"),
						# (this_or_next|gt, reg21, 3),
						# (neg|party_slot_eq, ":home_center", slot_center_is_besieged_by, -1), # Bring your patrol back quick if under siege.
						# (call_script, "script_castle_patrol_action", castle_patrol_return_home, ":current_patrol", ":home_center"),
					# (else_try),
						# ## Patrol is assigned, but apparently inactive. (defeated)
						# (neg|party_is_active, ":current_patrol"),
						# (party_set_slot, ":center_no", slot_center_patrol_party, -1),
					# (try_end),
				# (else_try),
					# (party_set_slot, ":center_no", slot_center_patrol_party, -1),
					# ## DEBUG DIAGNOSTIC ##
					# (ge, DEBUG_IMPROVEMENTS, 1),
					# (assign, reg31, ":current_patrol"),
					# (str_store_party_name, s31, ":center_no"),
					# (display_message, "@DEBUG (Patrols): Invalid party ID detected.  Party #{reg31} from {s31}.", gpu_red),
				# (try_end),
			# (try_end),
		
		# (try_end),
    ]),
	
# IMPROVEMENT: Recruitment Resource Upgrades
(72,
	[
		(try_for_range, ":center_no", centers_begin, centers_end),
			
			### IMPROVEMENT [ Training Grounds ] - Chance to convert Peasants -> Veterans
			(try_begin),
				## DETERMINE CHANCE TO UPGRADE
				(assign, ":chance", 0),
				(party_slot_ge, ":center_no", slot_center_has_training_grounds, cis_built),
				(assign, ":chance", 20),
				# Captain of the Guard can increase chance greater than 2% if equal to half of his total training skill.
				(try_begin),
					## Player Owns Settlement
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					
					(party_get_slot, ":captain", ":center_no", slot_center_advisor_war),
					(is_between, ":captain", companions_begin, companions_end),
					(store_skill_level, ":skill_training", "skl_trainer", ":captain"),
					(val_mul, ":skill_training", 3),
					(val_max, ":chance", ":skill_training"),
				(else_try),
					## AI Owns Settlement
					(neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(assign, ":chance", 200),
				(try_end),
				
				## CONVERT PEASANT TO VETERAN
				(try_begin),
					(store_random_in_range, ":roll", 0, 1000),
					(lt, ":roll", ":chance"),
					(try_begin),
						## Player Owns Settlement
						(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
						(party_get_slot, ":recruits", ":center_no", slot_center_volunteer_troop_amount),
						(ge, ":recruits", 1),
						(assign, ":change", 1),
						(party_get_slot, ":veterans", ":center_no", slot_center_veteran_pool),
						(val_sub, ":recruits", ":change"),
						(val_add, ":veterans", ":change"),
						(party_set_slot, ":center_no", slot_center_volunteer_troop_amount, ":recruits"),
						(party_set_slot, ":center_no", slot_center_veteran_pool, ":veterans"),
						
					(else_try),
						## AI Owns Settlement
						(neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
						(party_get_slot, ":recruits", ":center_no", slot_center_npc_volunteer_troop_amount),
						(ge, ":recruits", 1),
						(assign, ":change", 3),
						(val_max, ":change", ":recruits"),
						(party_get_slot, ":veterans", ":center_no", slot_center_veteran_ai),
						(val_sub, ":recruits", ":change"),
						(val_add, ":veterans", ":change"),
						(party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, ":recruits"),
						(party_set_slot, ":center_no", slot_center_veteran_ai, ":veterans"),
						
					(try_end),
					### DIAGNOSTIC ###
					(ge, DEBUG_IMPROVEMENTS, 1),
					(this_or_next|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(ge, DEBUG_IMPROVEMENTS, 2),
					(assign, reg22, ":recruits"),
					(assign, reg23, ":veterans"),
					(assign, reg24, ":change"),
					(store_sub, reg25, reg24, 1),
					(str_store_party_name, s21, ":center_no"),
					(assign, reg21, ":chance"),
					(display_message, "@DEBUG: {s21} has upgraded {reg24} peasant{reg25?s:} -> veteran{reg25?s:}.  ({reg21}).", gpu_debug),
				(try_end),
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