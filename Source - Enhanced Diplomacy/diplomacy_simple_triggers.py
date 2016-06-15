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
# Checking to give back experience for giving a vassal troops.
  (1,
	[
		# (ge, "$diplomacy_troops_given_party", 1),
		# (assign, reg0, "$diplomacy_troops_given_party"),
		# (display_message, "@DEBUG: Removing party #{reg0}.", gpu_debug),
			
		# # Remove troops from the backup that still remain in the player party which should leave just what we transfered to our vassal.
		# (assign, ":party_no", "p_main_party"),
		# (party_get_num_companion_stacks, ":stack_count",":party_no"),
		# (try_for_range, ":stack_no", 0, ":stack_count"),
			# (party_stack_get_troop_id, ":troop_no",":party_no",":stack_no"),
			# (neg|troop_is_hero, ":troop_no"),
			# (party_stack_get_size, ":stack_size",":party_no",":stack_no"),
			# (party_remove_members, "$diplomacy_troops_given_party", ":troop_no", ":stack_size"),
		# (try_end),
		
		# # Count the troops left in our temporary party and their combined levels.
		# (assign, ":troop_count", 0),
		# (assign, ":level_count", 0),
		# (assign, ":party_no", "$diplomacy_troops_given_party"),
		# (party_get_num_companion_stacks, ":stack_count",":party_no"),
		# (try_for_range, ":stack_no", 0, ":stack_count"),
			# (party_stack_get_troop_id, ":troop_no",":party_no",":stack_no"),
			# (neg|troop_is_hero, ":troop_no"),
			# (party_stack_get_size, ":stack_size",":party_no",":stack_no"),
			# (val_add, ":troop_count", ":stack_size"),
			# (store_character_level, ":troop_level", ":troop_no"),
			# (val_mul, ":troop_level", ":stack_size"),
			# (val_add, ":level_count", ":troop_level"),
		# (try_end),
		# (ge, ":troop_count", 1),
		# # Award some relation gain based on total level.
		# (store_div, ":relation_gain", ":level_count", 30),
		# (val_clamp, ":relation_gain", 0, 6),
		# (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", ":relation_gain", 0),
		# # Clean up variables so we don't do this again.
		# (remove_party, "$diplomacy_troops_given_party"),
		# (assign, "$diplomacy_troops_given_party", -1),
    ]),

## MORALE SYSTEM - BATTLE WEARINESS RECOVERY
(4,
   [
		(store_current_hours, ":hours"),
		(store_sub, ":time_passed", ":hours", "$morale_time_last_battle"),
		(call_script, "script_diplomacy_get_battle_weariness_factor", WEARINESS_RECOVERY_SPACING, 21),
		(val_div, ":time_passed", reg21),
		(call_script, "script_diplomacy_get_battle_weariness_factor", WEARINESS_RECOVERY_LIMIT, 21),
		(store_add, ":limit", reg21, 1),
		(val_clamp, ":time_passed", 0, ":limit"),
		(val_add, "$morale_battle_weary", ":time_passed"),
		(val_clamp, "$morale_battle_weary", morale_min_battle_weariness, morale_max_battle_weariness),
		
		(try_begin),
			(ge, BETA_TESTING_MODE, 2),
			(assign, reg31, ":hours"),
			(assign, reg32, "$morale_time_last_battle"),
			(assign, reg33, "$morale_battle_weary"),
			(assign, reg34, ":time_passed"),
			(display_message, "@DEBUG (BTM-2): Battle weariness ({reg33}) ({reg34}) ... ({reg31}-{reg32})", gpu_debug),
		(try_end),
   ]),
  
# WEEKLY: Check for relation changes with your vassals and centers. (Player Faction)
(24*7,
	[
		(call_script, "script_cf_qus_player_is_king", 1), # Needs to be a king.
		
		### RIGHT TO RULE ###
		(try_begin),
			(faction_get_slot, ":chance", "$players_kingdom", slot_faction_right_to_rule),
			(call_script, "script_diplomacy_convert_percent_to_direct_change", ":chance"),
			(assign, ":change", reg1),
			(neq, ":change", 0),
			(call_script, "script_change_player_right_to_rule", ":change"),
		(try_end),
		(try_begin),
			(eq, "$award_nobles_reasoning", 0),
			(call_script, "script_cf_qus_player_is_king", 1),
			(store_random_in_range, ":roll", 0, 100),
			(lt, ":roll", "$player_right_to_rule"),
			(assign, "$award_nobles_reasoning", "str_noble_joins_due_to_rtr"),
		(try_end),
		
		### RESET LORD RELATION GAIN DUE TO FIEFS ###
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(troop_set_slot, ":troop_no", slot_troop_relation_from_fief, 0),
		(try_end),
		
		### CENTER RELATIONS ###
		(try_for_range, ":center_no", centers_begin, centers_end),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(eq, ":faction_no", "$players_kingdom"),
			
			# Relation Change
			(try_begin),
				(faction_get_slot, ":chance", ":faction_no", slot_faction_fief_relation),
				## * CASTLE STEWARD: RELATION GAIN BONUS
				(try_begin),
					(try_begin),
						(party_slot_eq, ":center_no", slot_party_type, spt_village),
						(party_get_slot, ":fief", ":center_no", slot_village_bound_center),
					(else_try),
						(assign, ":fief", ":center_no"),
					(try_end),
					(party_get_slot, ":castle_steward", ":fief", slot_center_steward),
					(is_between, ":castle_steward", companions_begin, companions_end),
					## TROOP EFFECT: BONUS_ADMINISTRATOR in Castle Steward position improves chance of gaining relation with center by 1% per point of Leadership.
					(call_script, "script_cf_ce_troop_has_ability", ":castle_steward", BONUS_ADMINISTRATOR), # combat_scripts.py - ability constants in combat_constants.py
					(store_skill_level, ":leadership_bonus", "skl_leadership", ":castle_steward"),
					(val_add, ":chance", ":leadership_bonus"),
				(try_end),
				(call_script, "script_diplomacy_convert_percent_to_direct_change", ":chance"),
				(assign, ":change", reg1),
				(neq, ":change", 0),
				(call_script, "script_change_player_relation_with_center", ":center_no", ":change"),
			(try_end),
			
			# Prosperity Change
			(try_begin),
				(faction_slot_eq, ":faction_no", slot_faction_decree_war_taxes, 1), # "WAR TAXATION" decree active.
				(call_script, "script_change_center_prosperity", ":center_no", diplomacy_war_taxation_prosperity_loss),
			(try_end),
			
			# Add relation gain due to fief ownership.
			(try_begin),
				(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
				(is_between, ":troop_no", active_npcs_begin, active_npcs_end),
				(troop_get_slot, ":gain", ":troop_no", slot_troop_relation_from_fief),
				(try_begin),
					(party_slot_eq, ":center_no", slot_party_type, spt_town),
					(val_add, ":gain", 75),
				(else_try),
					(party_slot_eq, ":center_no", slot_party_type, spt_castle),
					(val_add, ":gain", 55),
				(else_try),
					(party_slot_eq, ":center_no", slot_party_type, spt_village),
					(val_add, ":gain", 30),
				(try_end),
				(troop_set_slot, ":troop_no", slot_troop_relation_from_fief, ":gain"),
			(try_end),
			
			# Change intelligence level on center.
			(call_script, "script_diplomacy_set_party_intel_level", ":center_no", -1, 0),
		(try_end),
		
		### LORD RELATIONS ###
		(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
			(store_troop_faction, ":faction_no", ":troop_no"),
			(eq, ":faction_no", "$players_kingdom"),
			(faction_slot_eq, ":faction_no", slot_faction_leader, "trp_player"),
			(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
			(troop_get_slot, ":reputation", ":troop_no", slot_lord_reputation_type),
			(assign, ":continue", 1),
			(try_begin),
				(eq, ":reputation", lrep_martial),
				(assign, ":data_slot", slot_faction_lrep_martial_relation),
			(else_try),
				(eq, ":reputation", lrep_quarrelsome),
				(assign, ":data_slot", slot_faction_lrep_quarrelsome_relation),
			(else_try),
				(eq, ":reputation", lrep_selfrighteous),
				(assign, ":data_slot", slot_faction_lrep_selfrighteous_relation),
			(else_try),
				(eq, ":reputation", lrep_cunning),
				(assign, ":data_slot", slot_faction_lrep_cunning_relation),
			(else_try),
				(eq, ":reputation", lrep_debauched),
				(assign, ":data_slot", slot_faction_lrep_debauched_relation),
			(else_try),
				(eq, ":reputation", lrep_goodnatured),
				(assign, ":data_slot", slot_faction_lrep_goodnatured_relation),
			(else_try),
				(eq, ":reputation", lrep_upstanding),
				(assign, ":data_slot", slot_faction_lrep_upstanding_relation),
			(else_try),
				(eq, ":reputation", lrep_roguish),
				(assign, ":data_slot", slot_faction_lrep_roguish_relation),
			(else_try),
				(eq, ":reputation", lrep_benefactor),
				(assign, ":data_slot", slot_faction_lrep_benefactor_relation),
			(else_try),
				(eq, ":reputation", lrep_custodian),
				(assign, ":data_slot", slot_faction_lrep_custodian_relation),
			(else_try),
				(eq, ":reputation", lrep_none),
				(assign, ":data_slot", slot_faction_lrep_martial_relation),
			(else_try),
				### ERROR - No valid reputation type. ###
				(assign, reg31, ":reputation"),
				(str_store_troop_name, s31, ":troop_no"),
				(display_message, "@ERROR (Diplomacy): Invalid reputation type {reg31} on {s31}.", gpu_red),
				(assign, ":continue", 0),
			(try_end),
			(eq, ":continue", 1),
			(faction_get_slot, ":chance", ":faction_no", ":data_slot"),
			(troop_get_slot, ":fief_bonus", ":troop_no", slot_troop_relation_from_fief),
			(try_begin),
				(ge, ":fief_bonus", 1),
				(val_add, ":chance", ":fief_bonus"),
			(else_try),
				(val_add, ":chance", 0),
			(try_end),
			## Persuasion Skill - Improve negative relation trend by 1% per rank of the skill.
			(try_begin),
				(store_skill_level, ":skill", "skl_persuasion", "trp_player"),
				(lt, ":chance", 0),
				## TROOP EFFECT - BONUS_SILVER_TONGUED - Improve persuasion effect from 1% to 2% per rank.
				(try_begin),
					(call_script, "script_cf_ce_troop_has_ability", "trp_player", BONUS_SILVER_TONGUED),
					(val_mul, ":skill", 2),
				(try_end),
				(val_add, ":chance", ":skill"),
				(val_max, ":chance", 0),
			(try_end),
			(call_script, "script_diplomacy_convert_percent_to_direct_change", ":chance"),
			(assign, ":change", reg1),
			(neq, ":change", 0),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", ":troop_no", ":change"),
			
		(try_end),
    ]),
	
# WEEKLY: Captain of the Guard.  Weekly pulse.
# Weekly charge owner of the patrol for the cost.  This applies to the AI only as the player pays for it during his weekly budget screen.
# Weekly attempt to recruit a few new troops to each patrol.
(24*7,
	[
		(try_begin),
			(ge, DEBUG_DIPLOMACY_PATROLS, 1),
			(display_message, "@DEBUG (patrols): Weekly diplomacy pulse.", gpu_debug),
			(display_message, "@DEBUG (patrols): ...Charging AI lords for any active patrols.", gpu_debug),
			(display_message, "@DEBUG (patrols): ...Each active patrol will attempt to recruit new members if needed.", gpu_debug),
			(display_message, "@DEBUG (patrols): ...Each active patrol will offload any prisoners held.", gpu_debug),
			(display_message, "@DEBUG (advisors): ...Each active advisor should gain 10 renown to a maximum of 250.", gpu_debug),
			# (display_message, "@DEBUG (garrison): ...Each garrison should attempt to train up if a Captain is assigned.", gpu_debug),
			(display_message, "@DEBUG (recruitment): ...Each center is gaining mounts based on their growth.", gpu_debug),
			(display_message, "@DEBUG (culture): ...Converting any new centers over to the new culture.", gpu_debug),
		(try_end),
		
		(call_script, "script_hub_update_center_stock_of_mounts", spt_village),
		(call_script, "script_hub_update_center_stock_of_mounts", spt_castle),
		(call_script, "script_hub_update_center_stock_of_mounts", spt_town),
		
		(try_for_range, ":center_no", centers_begin, centers_end),
			
			### UPDATE CULTURE OF PROPERTY ###
			(try_for_range, ":center_no", centers_begin, centers_end),
				(store_faction_of_party, ":original_faction", ":center_no"),
				(faction_get_slot, ":culture", ":original_faction", slot_faction_culture),
				(party_set_slot, ":center_no", slot_center_culture,  ":culture"),
			(try_end),

			(try_begin),
				(store_faction_of_party, ":faction_no", ":center_no"),
				(faction_get_slot, ":culture_faction", ":faction_no",  slot_faction_culture),
				(party_get_slot, ":culture_center", ":center_no", slot_center_culture),
				(assign, ":culture_changed", 0),
				(try_begin),
					(neq, ":culture_center", ":culture_faction"),
					(party_set_slot, ":center_no", slot_center_culture, ":culture_faction"),
					(assign, ":culture_changed", 1),
				(try_end),
				(this_or_next|ge, BETA_TESTING_MODE, 1),
				(ge, DEBUG_DIPLOMACY, 1),
				(eq, ":culture_changed", 1),
				(str_store_faction_name, s31, ":faction_no"),
				(str_store_faction_name, s32, ":culture_faction"),
				(str_store_faction_name, s33, ":culture_center"),
				(str_store_party_name, s34, ":center_no"),
				(display_message, "@DEBUG (culture): {s34} of the {s31} has updated its culture from {s33} to {s32}.", gpu_debug),
			(try_end),
			
			### ADVISOR RENOWN & EXPERIENCE BOOST ###
			(try_begin),
				(is_between, ":center_no", walled_centers_begin, walled_centers_end),
				(try_for_range, ":advisor_no", advisors_begin, advisors_end),
					(party_get_slot, ":troop_no", ":center_no", ":advisor_no"),
					(is_between, ":troop_no", companions_begin, companions_end),
					(troop_get_slot, ":renown", ":troop_no", slot_troop_renown),
					(store_sub, ":gain", 250, ":renown"),
					(val_clamp, ":gain", 0, 11),
					(ge, ":gain", 1),
					(val_add, ":renown", ":gain"),
					(troop_set_slot, ":troop_no", slot_troop_renown, ":renown"),
					(add_xp_to_troop, 250, ":troop_no"),
					(ge, DEBUG_DIPLOMACY, 1),
					(str_store_troop_name, s31, ":troop_no"),
					(assign, reg31, ":gain"),
					(assign, reg32, ":renown"),
					(display_message, "@DEBUG (diplomacy): Advisor '{s31}' has gained {reg31} renown for a total of {reg32} renown.", gpu_debug),
				(try_end),
				
				### PATROL PAYMENT ### (for AI)
				(try_begin),
					(neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), # Player is charged for his patrols on the weekly upkeep screen.
					(call_script, "script_diplomacy_order_all_patrols_of_center", ":center_no", PATROL_PAYMENT_DUE),
				(try_end),
				
				### PATROL RECRUITMENT ###
				(call_script, "script_diplomacy_order_all_patrols_of_center", ":center_no", PATROL_RECRUIT_TROOPS),
				
				### PATROL PRISONER OFFLOAD ###
				(call_script, "script_diplomacy_order_all_patrols_of_center", ":center_no", PATROL_DUMP_PRISONERS),
				
				# ### GARRISON TRAINING ###
				# (try_begin),
					# (eq, 1, 0), ## WINDYPLAINS+ ## - Garrison Training has been disabled intentionally until it can be reworked.
					# (party_slot_eq, ":center_no", slot_center_upgrade_garrison, 1), # Training Enabled
					# # Verify a Captain of the Guard is assigned.
					# (party_get_slot, ":captain", ":center_no", slot_center_advisor_war), 
					# (is_between, ":captain", companions_begin, companions_end),
					# # Get the captain's relevant stats.
					# (store_skill_level, ":leadership", "skl_leadership", ":captain"),
					# (store_skill_level, ":training", "skl_trainer", ":captain"),
					# # Determine maximum tier of training.
					# (store_add, ":competency", ":leadership", ":training"),
					# (store_div, ":tier_bonus", ":competency", 5),
					# (store_add, ":max_tier", 2, ":tier_bonus"),
					# (val_clamp, ":max_tier", 1, 6),
					# # Determine percentage of troops to upgrade.  Formula = 8 + (Leadership + Training)/2
					# (store_div, ":upgrade_boost", ":competency", 2),
					# (store_add, ":upgrade_chance", 8, ":upgrade_boost"),
					# ## WINDYPLAINS+ ## IMPROVEMENT [ Training Grounds ] - Increases upgrade chance by 5%.
					# (try_begin),
						# (party_slot_ge, ":center_no", slot_center_has_training_grounds, cis_built),
						# (val_add, ":upgrade_chance", 5),
						# (party_slot_ge, ":center_no", slot_center_has_training_grounds, cis_damaged_40_percent),
						# (val_sub, ":upgrade_chance", 2),
					# (try_end),
					# ## WINDYPLAINS- ##
					# # Upgrade troops as applicable.
					# (party_get_num_companion_stacks, ":stack_limit", ":center_no"),
					# (try_for_range_backwards, ":stack_no", 0, ":stack_limit"),
						# # Verify if this stack should get upgraded.
						# (party_stack_get_troop_id, ":troop_old", ":center_no", ":stack_no"),
						# (neg|troop_is_hero, ":troop_old"),
						# # Make sure the troop is of the right culture.
						# (store_troop_faction, ":faction_no", ":troop_old"),
						# (faction_get_slot, ":troop_culture", ":faction_no", slot_faction_culture),
						# (party_slot_eq, ":center_no", slot_center_culture, ":troop_culture"),
						# # Make sure its tier isn't too high.
						# (call_script, "script_diplomacy_determine_troop_tier", ":troop_old"),
						# (lt, reg1, ":max_tier"),
						
						# # Determine how many to upgrade in this stack.
						# (party_stack_get_size, ":stack_size", ":center_no", ":stack_no"),
						# (store_mul, ":total_upgraded", ":stack_size", ":upgrade_chance"),
						# (val_div, ":total_upgraded", 100),
						# (val_max, ":total_upgraded", 1), # Ensure we always get some benefit.
						
						# # Determine which paths to upgrade to.
						# (troop_get_slot, ":chance_1", ":troop_old", slot_troop_upgrade_chance_1),
						# (troop_get_slot, ":chance_2", ":troop_old", slot_troop_upgrade_chance_2),
						# (troop_get_upgrade_troop, ":troop_1", ":troop_old", 0),
						# (troop_get_upgrade_troop, ":troop_2", ":troop_old", 1),
						# # Determine how many go to path 1.
						# (try_begin),
							# (ge, ":chance_1", 1),
							# (store_mul, ":count_1", ":total_upgraded", ":chance_1"),
							# (val_div, ":count_1", 100),
							# (eq, ":chance_2", 0), # No chance of a 2nd path so path 1 needs to get them all.
							# (val_max, ":count_1", ":total_upgraded"),
						# (try_end),
						# # Determine how many go to path 2.
						# (try_begin),
							# (ge, ":chance_2", 1),
							# (store_mul, ":count_2", ":total_upgraded", ":chance_2"),
							# (val_div, ":count_2", 100),
							# (eq, ":chance_1", 0), # No chance of a 1st path so path 2 needs to get them all.
							# (val_max, ":count_2", ":total_upgraded"),
						# (try_end),
						# # Final check to make sure we didn't short the player any.
						# (try_begin),
							# (ge, ":chance_1", 1),
							# (ge, ":chance_2", 1),
							# (store_add, ":count", ":count_1", ":count_2"),
							# (lt, ":count", ":total_upgraded"),
							# (store_sub, ":missing", ":total_upgraded", ":count"),
							# (val_add, ":count_1", ":missing"),
						# (try_end),
						
						# # Upgrade troops in stack if applicable.
						# (ge, ":total_upgraded", 1),
						# (try_begin),
							# (ge, ":count_1", 1),
							# (call_script, "script_game_get_upgrade_cost", ":troop_1"),
							# (store_mul, ":cost", ":count_1", reg0),
							# ## WINDYPLAINS+ ## IMPROVEMENT [ Training Grounds ] - Reduces cost of training garrison soldiers by 10%.
							# (try_begin),
								# (party_slot_ge, ":center_no", slot_center_has_training_grounds, cis_built),
								# (store_mul, ":discount", ":cost", 10),
								# (val_div, ":discount", 100),
								# (val_sub, ":cost", ":discount"),
							# (try_end),
							# ## WINDYPLAINS- ##
							# (call_script, "script_cf_diplomacy_treasury_verify_funds", ":cost", ":center_no", FUND_FROM_TREASURY, TREASURY_FUNDS_AVAILABLE),
							# (call_script, "script_diplomacy_treasury_withdraw_funds", ":cost", ":center_no", FUND_FROM_TREASURY),
							# # Track the amount spent.
							# (party_get_slot, reg1, ":center_no", slot_center_spent_upgrading),
							# (val_add, reg1, ":cost"),
							# (display_message, "@DEBUG (recruiting): Training costs now total {reg1} denars.", gpu_debug),
							# (party_set_slot, ":center_no", slot_center_spent_upgrading, reg1),
							# # Add the new party member.
							# (party_add_members, ":center_no", ":troop_1", ":count_1"),
						# (else_try),
							# (assign, ":count_1", -1),
						# (try_end),
						# (try_begin),
							# (ge, ":count_2", 1),
							# (call_script, "script_game_get_upgrade_cost", ":troop_2"),
							# (store_mul, ":cost", ":count_2", reg0),
							# ## WINDYPLAINS+ ## IMPROVEMENT [ Training Grounds ] - Reduces cost of training garrison soldiers by 10%.
							# (try_begin),
								# (party_slot_ge, ":center_no", slot_center_has_training_grounds, cis_built),
								# (store_mul, ":discount", ":cost", 10),
								# (val_div, ":discount", 100),
								# (val_sub, ":cost", ":discount"),
							# (try_end),
							# ## WINDYPLAINS- ##
							# (call_script, "script_cf_diplomacy_treasury_verify_funds", ":cost", ":center_no", FUND_FROM_TREASURY, TREASURY_FUNDS_AVAILABLE),
							# (call_script, "script_diplomacy_treasury_withdraw_funds", ":cost", ":center_no", FUND_FROM_TREASURY),
							# (party_add_members, ":center_no", ":troop_2", ":count_2"),
						# (else_try),
							# (assign, ":count_2", -1),
						# (try_end),
						# (party_remove_members, ":center_no", ":troop_old", ":total_upgraded"),
						
						# # Diagnostic
						# (ge, DEBUG_DIPLOMACY, 1),
						# (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
						# (assign, reg31, ":count_1"),
						# (assign, reg32, ":count_2"),
						# (assign, reg33, ":total_upgraded"),
						# (assign, reg34, ":chance_1"),
						# (assign, reg35, ":chance_2"),
						# (str_store_troop_name, s31, ":troop_old"),
						# (str_store_troop_name, s32, ":troop_1"),
						# (str_store_troop_name, s33, ":troop_2"),
						# (str_store_party_name, s34, ":center_no"),
						# (display_message, "@DEBUG (garrison): {s31} has gained {reg31} {s32} through upgrading.", gpu_debug),
						# (display_message, "@DEBUG (garrison): {s31} has gained {reg32} {s33} through upgrading.", gpu_debug),
						# (display_message, "@DEBUG (garrison): {s31} has lost {reg33} {s31} through upgrading.", gpu_debug),
					# (try_end),
				# (try_end),
				
			(try_end),
			
		(try_end),
    ]),
	
# MONTHLY: Captain of the Guard Patrols.  Monthly pulse.
# Monthly attempt to upgrade troops in existing patrols.
(24*30,
	[
		(try_begin),
			(ge, DEBUG_DIPLOMACY_PATROLS, 1),
			(display_message, "@DEBUG (patrols): Monthly patrol pulse.", gpu_debug),
			(display_message, "@DEBUG (patrols): ...Upgrading 20% of patrol troops.", gpu_debug),
		(try_end),
		
		(try_for_range, ":center_no", centers_begin, centers_end),
			
			### PATROL UPGRADES ###
			(call_script, "script_diplomacy_order_all_patrols_of_center", ":center_no", PATROL_UPGRADE_TROOPS),
			
		(try_end),
    ]),
	
# DAILY: Captain of the Guard Recruitment.  Monthly pulse.
# Monthly attempt to upgrade troops in existing patrols.
(24*1,
	[
		# FACTION SEQUENCER
		# This is intended to prevent every faction from trying to perform these recruitment upgrades every day.
		(val_add, "$diplomacy_recruiting_faction", 1),
		(try_begin),
			(this_or_next|eq, "$diplomacy_recruiting_faction", kingdoms_end),
			(neg|is_between, "$diplomacy_recruiting_faction", kingdoms_begin, kingdoms_end),
			(assign, "$diplomacy_recruiting_faction", kingdoms_begin),
		(try_end),
		(str_store_faction_name, s21, "$diplomacy_recruiting_faction"),
		
		(try_begin),
			(ge, DEBUG_RECRUITMENT, 1),
			(display_message, "@DEBUG (recruitment): Daily recruitment pulse.", gpu_green),
			(display_message, "@DEBUG (recruitment): ...Faction currently recruiting is {s21}.", gpu_debug),
			(display_message, "@DEBUG (recruitment): ...Calculating recruits from villages.", gpu_debug),
			(display_message, "@DEBUG (recruitment): ...Calculating recruits for castles & towns.", gpu_debug),
		(try_end),
		
		(assign, "$diplomacy_apply_conscription_penalties", 1),
		
		# LOGIC:
		#  * Figure out how many recruits should be spawned within a village.
		#  * Store these recruits into an "owner" pool and a "visitor" pool.
		#  * Add these recruits to the same "owner" and "visitor" pools at the village's bound center.
		(try_for_range, ":center_no", villages_begin, villages_end),
			# See if it is this faction's turn to recruit today.
			(store_faction_of_party, ":faction_no", ":center_no"),
			(eq, ":faction_no", "$diplomacy_recruiting_faction"),
			(party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
			(party_get_slot, ":bound_center_pool", ":bound_center", slot_center_recruit_pool),
			(party_get_slot, ":player_pool", ":center_no", slot_center_volunteer_troop_amount),
			(party_get_slot, ":npc_pool", ":center_no", slot_center_npc_volunteer_troop_amount),
			(call_script, "script_diplomacy_get_recruitment_score", ":center_no"),
			(call_script, "script_diplomacy_convert_percent_to_direct_change", reg1),
			(assign, ":recruits", reg1),
			(val_max, ":recruits", 0),
			## BOUND CENTER CONTRIBUTION ##
			(val_add, ":bound_center_pool", ":recruits"),
			(party_set_slot, ":bound_center", slot_center_recruit_pool, ":bound_center_pool"),
			
			## PLAYER RECRUITS ##
			(try_begin),
				(faction_slot_eq, ":faction_no", slot_faction_decree_conscription, 1), # Ensure conscription decree is active.
				(val_add, ":player_pool", ":recruits"),
			(else_try),
				(val_add, ":player_pool", ":recruits"),
				(party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
				(val_div, ":player_relation", 4),
				(val_clamp, ":player_relation", -10, 15),
				(store_add, ":recruit_limit", 10, ":player_relation"),
				(val_min, ":player_pool", ":recruit_limit"),
			(try_end),
			(party_set_slot, ":center_no", slot_center_volunteer_troop_amount, ":player_pool"),
			
			## NPC RECRUITS ##
			(store_mul, ":recruits_for_npcs", ":recruits", 5),
			(try_begin),
				(faction_slot_eq, ":faction_no", slot_faction_decree_conscription, 1), # Ensure conscription decree is active.
				(val_add, ":npc_pool", ":recruits_for_npcs"),
			(else_try),
				(val_add, ":npc_pool", ":recruits_for_npcs"),
				(party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
				(val_min, ":npc_pool", ":prosperity"),
			(try_end),
			(party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, ":npc_pool"),
			(ge, DEBUG_RECRUITMENT, 2),
			(str_store_party_name, s31, ":center_no"),
			(party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
			(str_store_party_name, s32, ":bound_center"),
			(assign, reg31, ":recruits"),
			(display_message, "@DEBUG (recruitment): {s31} has contributed {reg31} recruits to {s32}.", gpu_debug),
			
			
		(try_end),
		
		# Figure out how many recruits a castle should gain from itself as well as how many are pulled from villagers.
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			#(party_slot_eq, ":center_no", slot_center_recruiting, 1),
			
			# See if it is this faction's turn to recruit today.
			(store_faction_of_party, ":faction_no", ":center_no"),
			(eq, ":faction_no", "$diplomacy_recruiting_faction"),
			
			# Figure out how many troops this center should gain.
			(call_script, "script_diplomacy_get_recruitment_score", ":center_no"),
			(call_script, "script_diplomacy_convert_percent_to_direct_change", reg1),
			(assign, ":recruits", reg1),
			(val_max, ":recruits", 0),
			
			# Sum up all of the sources.
			(party_get_slot, ":village_input", ":center_no", slot_center_recruit_pool),
			(party_get_slot, ":player_pool", ":center_no", slot_center_volunteer_troop_amount),
			(party_get_slot, ":npc_pool", ":center_no", slot_center_npc_volunteer_troop_amount),
			(party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
			
			## PLAYER RECRUITS ##
			(try_begin),
				(faction_slot_eq, ":faction_no", slot_faction_decree_conscription, 1), # Ensure conscription decree is active.
				(store_add, ":new_recruits", ":recruits", ":village_input"),
				(val_add, ":player_pool", ":new_recruits"),
			(else_try),
				(store_add, ":new_recruits", ":recruits", ":village_input"),
				(val_add, ":player_pool", ":new_recruits"),
				(party_get_slot, ":player_relation", ":center_no", slot_center_player_relation),
				(val_div, ":player_relation", 2),
				(val_clamp, ":player_relation", -10, 15),
				(store_add, ":recruit_limit", 20, ":player_relation"),
				(val_min, ":player_pool", ":recruit_limit"),
			(try_end),
			(party_set_slot, ":center_no", slot_center_volunteer_troop_amount, ":player_pool"),
			
			## NPC RECRUITS ##
			(store_add, ":npc_recruits", ":recruits", ":village_input"),
			(val_mul, ":npc_recruits", 5),
			(try_begin),
				(faction_slot_eq, ":faction_no", slot_faction_decree_conscription, 1), # Ensure conscription decree is active.
				(val_add, ":npc_pool", ":npc_recruits"),
			(else_try),
				(val_add, ":npc_pool", ":npc_recruits"),
				(party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
				(val_mul, ":prosperity", 3),
				(val_div, ":prosperity", 2),
				(val_min, ":npc_pool", ":prosperity"),
			(try_end),
			(party_set_slot, ":center_no", slot_center_npc_volunteer_troop_amount, ":npc_pool"),
			# Reset the recruits coming from neighboring villages.
			(party_set_slot, ":center_no", slot_center_recruit_pool, 0),
			
			## WINDYPLAINS+ ## - AI receives veteran recruits regularly.
			(party_get_slot, ":veterans", ":center_no", slot_center_veteran_ai),
			(val_add, ":veterans", 8),
			(val_min, ":veterans", 30),
			(party_set_slot, ":center_no", slot_center_veteran_ai, 8),
			## WINDYPLAINS- ##
			
			### DIAGNOSTIC ###
			(try_begin),
				(ge, DEBUG_RECRUITMENT, 1),
				(assign, reg31, ":player_pool"),
				(assign, reg32, ":npc_pool"),
				(assign, reg33, ":village_input"),
				(assign, reg34, ":recruits"),
				(str_store_party_name, s31, ":center_no"),
				(display_message, "@DEBUG (recruitment): {s31} gains ({reg33}v + {reg34}c) recruits.  Pools: Player ({reg31}), NPC ({reg32}).", gpu_debug),
			(try_end),
			
		(try_end),
		
		(assign, "$diplomacy_apply_conscription_penalties", 0),
    ]),
	
# ALTERNATE MORALE SYSTEM - Shift real morale value towards ideal values.
(12,
	[
		(is_currently_night),
		(eq, "$diplomacy_use_alt_morale", 1),
		# Get player leadership score.
		(store_skill_level, ":leadership_bonus", "skl_leadership", "trp_player"),
		(assign, ":morale_recovery_rate", 10),
		# Get our IDEAL morale.
		(call_script, "script_diplomacy_get_player_party_morale_values"),
		(assign, ":ideal_morale", reg0),
		# Get our CURRENT morale.
		(party_get_morale, ":current_morale", "p_main_party"),
		# Compare our two values.
		(store_sub, ":morale_change", ":ideal_morale", ":current_morale"),
		# Add our leadership bonus in a way that is beneficial.
		(try_begin),
			(ge, ":morale_change", 0),
			(val_add, ":morale_recovery_rate", ":leadership_bonus"),
			(assign, ":sign", 1),
		(else_try),
			(lt, ":morale_change", 0),
			(val_div, ":leadership_bonus", 2),
			(val_sub, ":morale_recovery_rate", ":leadership_bonus"),
			(assign, ":sign", -1),
		(try_end),
		(val_mul, ":morale_change", ":morale_recovery_rate"),
		(val_div, ":morale_change", 100),
		
		# Now prevent our recovery rate & difference being so small that rounded integers never bring it to ideal.
		(try_begin),
			(eq, ":morale_change", 0),
			(neq, ":ideal_morale", ":current_morale"),
			(assign, ":morale_change", 1),
			(try_begin),
				(store_sub, ":diff", ":ideal_morale", ":current_morale"),
				(neg|is_between, ":diff", -1, 2),
				(assign, ":morale_change", 2),
			(try_end),
			(val_mul, ":morale_change", ":sign"),
		(try_end),
		
		# (neq, ":ideal_morale", ":current_morale"),
		# (display_message, "@As night approaches, your warband strikes camp and reflects on recent events...", gpu_light_blue),
		(set_show_messages, 0),
		(call_script, "script_change_party_morale", "p_main_party", ":morale_change", PMR_DAILY_SHIFT),
		(set_show_messages, 1),
    ]),
	
## INTELLIGENCE SYSTEM - Drifting downward over time.
(24*7,
   [
		(try_for_range, ":center_no", centers_begin, centers_end),
			(try_begin),
				(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
				(assign, ":minimum_intel", 10),
			(else_try),
				(store_faction_of_party, ":faction_no", "$current_town"),
				(eq, ":faction_no", "$players_kingdom"),
				(assign, ":minimum_intel", 7),
			(else_try),
				(assign, ":minimum_intel", 3),
			(try_end),
			(party_get_slot, ":intel", ":center_no", slot_center_intelligence),
			(val_sub, ":intel", 1),
			(val_max, ":intel", ":minimum_intel"),
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