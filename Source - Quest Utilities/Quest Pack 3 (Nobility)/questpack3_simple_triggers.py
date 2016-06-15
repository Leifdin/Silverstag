# Quest Pack 3 (1.0) by Windyplains

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
	
	# TRIGGER: Enables a bunch of cheats.
	(0.1,[
			# (map_free),
			# (try_begin),
				# (store_distance_to_party_from_party, reg1, "p_main_party", "$current_town"),
				# (neq, reg1, "$old_dist"),
				# (assign, "$old_dist", reg1),
				# (check_quest_active, "qst_patrol_for_bandits"),
				# (quest_get_slot, ":target_center", "qst_patrol_for_bandits", slot_quest_giver_center),
				# (str_store_party_name, s1, ":target_center"),
				# (try_begin),
					# (ge, "$old_dist", 25),
					# (display_message, "@You are now {reg1} distance from {s1}.  You are within the range to hunt for bandits."),
				# (else_try),
					# (display_message, "@You are now {reg1} distance from {s1} which is too far away to hunt for bandits."),
				# (try_end),
			# (try_end),
			# (try_begin),
				# (store_troop_gold, ":gold", "trp_player"),
				# (lt, ":gold", 20000),
				# (store_sub, ":add_gold", 20000, ":gold"),
				# (troop_add_gold, "trp_player", ":add_gold"),
			# (try_end),
		]
	),
	
	##### QUEST : SUMMONED_TO_HALL : BEGIN #####
	
	# TRIGGER: Daily check to see if a "court quest" is available.
	(24,[
			(map_free),
			(neg|check_quest_active, "qst_summoned_to_hall"),
			(quest_slot_eq, "qst_summoned_to_hall", slot_quest_dont_give_again_remaining_days, 0),
			# When was the last time the player was annoyed with a popup like this?
			(store_current_hours, ":hours_current"),
			(store_sub, ":time_passed", ":hours_current", "$time_since_last_summoned"),
			(ge, ":time_passed", 168), # 7 Days
			# Is the player within a messenger's ride of his owned territories?
			(call_script, "script_cf_qus_party_within_range_of_owned_fiefs", "p_main_party"),
			# Does the player own any castles?
			(call_script, "script_cf_qus_player_owns_walled_center"),
			(quest_set_slot, "qst_summoned_to_hall", slot_quest_giver_center, reg1),
			(assign, ":center_no", reg1),
			# Does this castle have an assigned steward?
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(is_between, ":castle_steward", companions_begin, companions_end),
			
			# Check if any quests are available and trigger.
			(assign, ":trigger_talk", 0),
			(assign, ":context", -1),
			(try_begin),
				##### QUEST ( patrol_for_bandits ) INITIATION #####
				(assign, ":quest_no", "qst_patrol_for_bandits"),
				(neg|check_quest_active, ":quest_no"),
				(quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", 15),
				(assign, ":trigger_talk", 1),
				(assign, ":context", ":quest_no"),
			(else_try),
				##### QUEST ( destroy_the_lair ) INITIATION #####
				(assign, ":quest_no", "qst_destroy_the_lair"),
				(neg|check_quest_active, ":quest_no"),
				(neg|check_quest_active, "qst_destroy_bandit_lair"), # No sense in letting both quests aim at this lair.
				(quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", 15),
				(store_add, ":bandit_templates_end", "pt_sea_raiders", 1),
				(assign, ":closest_template", -1),
				(try_for_range, ":bandit_template", "pt_steppe_bandits", ":bandit_templates_end"),
					(eq, ":closest_template", -1),
					(party_template_get_slot, ":bandit_lair", ":bandit_template", slot_party_template_lair_party),
					(call_script, "script_cf_qus_party_close_to_center", ":center_no", ":bandit_lair", 25),
					(assign, ":closest_template", ":bandit_template"),
				(try_end),
				(neq, ":closest_template", -1),
				(party_template_get_slot, ":bandit_lair", ":closest_template", slot_party_template_lair_party),
				(quest_set_slot, ":quest_no", slot_quest_target_party, ":bandit_lair"),
				(assign, ":trigger_talk", 1),
				(assign, ":context", ":quest_no"),
			(else_try),
				##### QUEST ( escort_to_mine ) INITIATION #####
				(assign, ":quest_no", "qst_escort_to_mine"),
				(neg|check_quest_active, ":quest_no"),
				(quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(party_get_num_prisoners, ":prisoner_count", ":center_no"),
				(ge, ":prisoner_count", 40),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", 20),
				(assign, ":trigger_talk", 1),
				(assign, ":context", ":quest_no"),
			(else_try),
				##### QUEST ( mercs_for_hire ) INITIATION #####
				(assign, ":quest_no", "qst_mercs_for_hire"),
				(neg|check_quest_active, ":quest_no"),
				(quest_slot_eq, ":quest_no", slot_quest_dont_give_again_remaining_days, 0),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", 15),
				(assign, ":trigger_talk", 1),
				(assign, ":context", ":quest_no"),
			(try_end),
			(eq, ":trigger_talk", 1),
			(ge, ":context", 0),
			#(display_message, "@TRIGGER: Messenger should activate."),
			(neg|main_party_has_troop, qp3_actor_messenger),
			(party_add_members, "p_main_party", qp3_actor_messenger, 1),
			(str_store_party_name, s13, ":center_no"),
			(troop_set_name, qp3_actor_messenger, "@Messenger from {s13}"),
			(assign, "$g_talk_troop", qp3_actor_messenger),
			(assign, "$npc_map_talk_context", ":context"),
			(quest_set_slot, "qst_summoned_to_hall", slot_quest_temp_slot, "$npc_map_talk_context"),
			(assign, "$time_since_last_summoned", ":hours_current"),
			(start_map_conversation, qp3_actor_messenger),
		]
	),
	##### QUEST : SUMMONED_TO_HALL : END #####
	
	##### QUEST : PATROL_FOR_BANDITS : BEGIN #####
	
	# TRIGGER: Each day spawn another looter party.
	(24,[
			(check_quest_active, "qst_patrol_for_bandits"),
			(quest_slot_eq, "qst_patrol_for_bandits", slot_quest_current_state, qp3_patrol_bandits_begun),
			(quest_get_slot, ":quest_center", "qst_patrol_for_bandits", slot_quest_giver_center),
			(set_spawn_radius, 10),
			(spawn_around_party, ":quest_center", qp3_bandits_template),
			(ge, DEBUG_QUEST_PACK_3, 1),
			(display_message, "@Bandits have been spawned around {s13}."),
		]
	),
	##### QUEST : PATROL_FOR_BANDITS : BEGIN #####
	
	##### QUEST : MERCS_FOR_HIRE : BEGIN #####
	
	# TRIGGER: Daily check to see if mercenary party is about to expire on their contract.
	(24,[
			(map_free),
			(check_quest_active, "qst_mercs_for_hire"),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_active_contract),
			(neg|quest_slot_ge, "qst_mercs_for_hire", slot_quest_expiration_days, 4), # 3 or less days remain on contract.
			(assign, "$g_talk_troop", qp3_actor_mercenary_leader),
			(assign, "$npc_map_talk_context", qp3_mercs_for_hire_active_contract), # Troop wants to talk about renewing contract.
			(start_map_conversation, qp3_actor_mercenary_leader),
		]
	),
	
	# TRIGGER: Daily check to remove the mercenary party if the contract is ended.
	(24,[
			(map_free),
			(neg|check_quest_active, "qst_mercs_for_hire"),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_expiration_days, 0),
			(neg|quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_inactive),
			(quest_get_slot, ":merc_party", "qst_mercs_for_hire", slot_quest_target_party),
			(party_is_active, ":merc_party"),
			(call_script, "script_qp3_quest_mercenary_function", mercs_destroy_party),
			(call_script, "script_common_quest_change_state", "qst_mercs_for_hire", qp3_mercs_for_hire_inactive), # prevent repeats.
			(ge, DEBUG_QUEST_PACK_3, 1),
			(display_message, "@DEBUG (QP3): Mercenary party has been removed from the game due to contract expiration."),
		]
	),
	
	# TRIGGER: Weekly check to charge the player the contract cost.
	(24*7,[
			(check_quest_active, "qst_mercs_for_hire"),
			(this_or_next|quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_active_contract),
			(this_or_next|quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_refused_to_renew),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_agree_to_renew),
			(call_script, "script_qp3_quest_mercenary_function", mercs_payment_due),
			(try_begin),
				(eq, reg20, 1), # Mercenaries should leave.
				### Mercenaries leave due to non-payment ###
				(call_script, "script_common_quest_change_state", "qst_mercs_for_hire", qp3_mercs_for_hire_contract_ended),
				(call_script, "script_qp3_quest_mercenary_function", mercs_destroy_party),
				(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_fail),
				(display_message, "@Your mercenary party has abandoned you due to non-payment."),
			(try_end),
			(ge, DEBUG_QUEST_PACK_3, 1),
			(quest_get_slot, reg31, "qst_mercs_for_hire", slot_quest_merc_contract_debt),
			(ge, reg31, 1),
			(display_message, "@DEBUG (QP3): You still owe the mercenaries {reg31} denars in debt."),
		]
	),
	
	# TRIGGER: Weekly check to replesh mercenary party's numbers with fresh recruits.
	(24*7,[
			(check_quest_active, "qst_mercs_for_hire"),
			(this_or_next|quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_active_contract),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_agree_to_renew),
			(try_begin),
				(ge, DEBUG_QUEST_PACK_3, 1),
				(display_message, "@DEBUG (QP3): Mercenary party has attempted to hire new recruits."),
			(try_end),
			# Clean out non-mercenary troops.
			(call_script, "script_qp3_quest_mercenary_function", mercs_remove_non_mercenaries),
			# Upgrade surviving troops.
			(call_script, "script_qp3_quest_mercenary_function", mercs_recruit_troops),
		]
	),
	
	# TRIGGER: Monthly check to upgrade mercenary party troops still alive.
	(24*14,[
			(check_quest_active, "qst_mercs_for_hire"),
			(this_or_next|quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_active_contract),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_agree_to_renew),
			(try_begin),
				(ge, DEBUG_QUEST_PACK_3, 1),
				(display_message, "@DEBUG (QP3): Mercenary party has received its monthly upgrade check."),
			(try_end),
			# Clean out non-mercenary troops.
			(call_script, "script_qp3_quest_mercenary_function", mercs_remove_non_mercenaries),
			# Upgrade surviving troops.
			(call_script, "script_qp3_quest_mercenary_function", mercs_upgrade_troops),
		]
	),
	
	##### QUEST : MERCS_FOR_HIRE : END #####
	
	##### QUEST : ESCORT_TO_MINE : BEGIN #####
	# TROOP AI: Prisoner Caravans
	(8,[
			(try_for_parties, ":party_no"),
				## QUALIFY PARTY AS PRISONER CARAVAN ##
				(party_slot_eq, ":party_no", slot_party_type, spt_prisoner_train),
				(party_get_cur_town, ":cur_center", ":party_no"),
				(party_get_slot, ":center_destination", ":party_no", slot_party_caravan_destination),
				(party_get_slot, ":center_origin", ":party_no", slot_party_caravan_origin),
				(try_begin),
					(eq, ":cur_center", ":center_destination"),
					## UNLOAD PRISONERS AT DESTINATION ##
					(assign, "$g_move_heroes", 0),
					(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_unload_to_center_for_pay, ":party_no", ":cur_center"),
					## RETURN CARAVAN TO ORIGINAL CENTER ##
					(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_return_to_origin, ":party_no", ":center_origin"),  # Set party AI
					## CHECK FOR QUESTS UPDATES ##
					(try_begin),
						(check_quest_active, "qst_escort_to_mine"),
						(quest_slot_eq, "qst_escort_to_mine", slot_quest_target_party, ":party_no"), # Make sure some random caravan doesn't trigger this.
						(quest_slot_eq, "qst_escort_to_mine", slot_quest_current_state, qp3_escort_to_mine_begun),
						(call_script, "script_common_quest_change_state", "qst_escort_to_mine", qp3_escort_to_mine_slaves_delivered), # prevent repeats.
						(call_script, "script_qp3_quest_escort_to_mine", floris_quest_update),
					(try_end),
					
				(else_try),
					(eq, ":cur_center", ":center_origin"),
					## UNLOAD WEALTH AT ORIGIN ##
					(party_get_num_prisoner_stacks, ":stack_limit", ":party_no"),
					(eq, ":stack_limit", 0), # Make sure they don't have any prisoners.
					(try_begin),
						(check_quest_active, "qst_escort_to_mine"),
						(quest_slot_eq, "qst_escort_to_mine", slot_quest_target_party, ":party_no"), # Make sure some random caravan doesn't trigger this.
						(quest_slot_eq, "qst_escort_to_mine", slot_quest_current_state, qp3_escort_to_mine_slaves_delivered),
						(call_script, "script_common_quest_change_state", "qst_escort_to_mine", qp3_escort_to_mine_money_returned), # prevent repeats.
						(call_script, "script_qp3_quest_escort_to_mine", floris_quest_succeed),
					(try_end),
					(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_offload_wealth_and_remove, ":party_no", ":cur_center"),
					
				(try_end),
			(try_end),
		]),
	##### QUEST : ESCORT_TO_MINE : END #####
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