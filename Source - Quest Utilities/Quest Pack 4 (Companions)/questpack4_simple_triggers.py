# Quest Pack 4 (1.0) by Windyplains

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
	
	# TRIGGER: Daily check to see if any companions currently in the party have a finished story arc quest that needs addressing.
	(3,[
			(map_free),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(str_store_troop_name, s12, ":troop_no"),
				(main_party_has_troop, ":troop_no"),                                                             # Companion is currently in the party.
				(neg|troop_slot_eq, ":troop_no", slot_troop_intro_quest_complete, floris_story_arc_unfinished),  # Intro Quest either failed or succeeded.
				(neg|troop_slot_eq, ":troop_no", slot_troop_story_arc_quest, -1),                                # This companion has a story arc quest.
				(troop_get_slot, ":quest_no", ":troop_no", slot_troop_story_arc_quest),
				(check_quest_active, ":quest_no"),                                                               # That story arc is active.
				(assign, "$g_talk_troop", ":troop_no"),
				(assign, "$npc_map_talk_context", slot_troop_intro_quest_complete),                              # Troop wants to talk about quest failure.
				(start_map_conversation, ":troop_no"),
			(try_end),
		]
	),
	
	# TRIGGER: Every three days check to see if any companions currently in the party have a story arc quest nearing expiration.
	(12,[
			(map_free),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),                                                             # Companion is currently in the party.
				(troop_slot_eq, ":troop_no", slot_troop_intro_quest_complete, floris_story_arc_unfinished),      # Intro quest not succeeded or failed.
				(neg|troop_slot_eq, ":troop_no", slot_troop_story_arc_quest, -1),                                # This companion has a story arc quest.
				(troop_get_slot, ":quest_no", ":troop_no", slot_troop_story_arc_quest),
				(check_quest_active, ":quest_no"),                                                               # That story arc is active.
				(try_begin),
					(eq, ":troop_no", NPC_Odval),
					(check_quest_active, "qst_odval_saving_face"),
					(assign, ":limit", 4),
				(else_try),
					(assign, ":limit", 7),
				(try_end),
				(neg|quest_slot_ge, ":quest_no", slot_quest_expiration_days, ":limit"),                          # Less than a week remains. (generally)
				# Make sure we haven't made this comment before.
				(quest_slot_eq, ":quest_no", slot_quest_stage_10_trigger_chance, 0),
				(quest_set_slot, ":quest_no", slot_quest_stage_10_trigger_chance, 1),
				(assign, "$g_talk_troop", ":troop_no"),
				(assign, "$npc_map_talk_context", slot_troop_story_arc_quest),                                   # Troop wants to talk about nearing expiration.
				(start_map_conversation, ":troop_no"),
			(try_end),
		]
	),
	
	# TRIGGER: Serves as a waiting period plus dialog trigger.
	(1,[
			### QUEST: odval_accept_the_challenge
			# Purpose: Warn the player it is time to return to Tulbuk.
			(try_begin),
				(check_quest_active, "qst_odval_accept_the_challenge"),
				(quest_get_slot, reg1, "qst_odval_accept_the_challenge", slot_quest_target_amount),
				(ge, reg1, 1),
				(val_sub, reg1, 1),
				(quest_set_slot, "qst_odval_accept_the_challenge", slot_quest_target_amount, reg1),
				(try_begin),
					(ge, DEBUG_QUEST_PACK_4, 1),
					(display_message, "@DEBUG (QP4 - Accept the Challenge): There is {reg1} hours left to wait.", gpu_debug),
				(try_end),
				(eq, reg1, 0),
				(main_party_has_troop, NPC_Odval),
				(try_begin),
					(map_free),
					(assign, "$g_talk_troop", NPC_Odval),
					(assign, "$npc_map_talk_context", qp4_odval_redemption_return_to_tulbuk_done), # Troop wants to talk about nearing expiration.
					(start_map_conversation, NPC_Odval),
				(else_try),
					(str_store_party_name, s13, qp4_odval_home_town),
					(str_store_troop_name, s14, NPC_Odval),
					(display_message, "@{s14} reminds you that the village elder in {s13} is expecting the two of you to return about now.", gpu_purple),
				(try_end),
			(try_end),
			
			### QUEST: odval_saving_face
			# Purpose: Warn the player it is time to return to Tulbuk.
			(try_begin),
				(check_quest_active, "qst_odval_saving_face"),
				(quest_get_slot, reg1, "qst_odval_saving_face", slot_quest_target_amount),
				(ge, reg1, 1),
				(val_sub, reg1, 1),
				(quest_set_slot, "qst_odval_saving_face", slot_quest_target_amount, reg1),
				(eq, reg1, 0),
				# (main_party_has_troop, NPC_Odval),
				# (try_begin),
					# (map_free),
					# (assign, "$g_talk_troop", NPC_Odval),
					# (assign, "$npc_map_talk_context", slot_troop_add_to_scene),                                  # Troop wants to talk about nearing expiration.
					# (start_map_conversation, NPC_Odval),
				# (else_try),
					# (str_store_party_name, s13, qp4_odval_home_town),
					# (str_store_troop_name, s14, NPC_Odval),
					# (display_message, "@{s14} reminds you that the village elder in {s13} is expecting the two of you to return about now.", gpu_purple),
				# (try_end),
			(try_end),
		]
	),
	
	# TRIGGER: Check twice daily to see if Edwyn learned any news of the knights from his story line.
	(3,[
			(map_free),
			(main_party_has_troop, NPC_Edwyn), # Companion is currently in the party.
			(store_current_hours, ":hours_current"),
			(party_get_slot, ":hours_since", "p_main_party", slot_party_time_in_field),
			(store_sub, ":hours", ":hours_current", ":hours_since"),
			(lt, ":hours", 6),
			(assign, ":trigger_talk", 0),
			(try_begin),
				### STAGE UPGRADE TRIGGER ( edwyn_first_knight ) 1 -> 2 ###
				(check_quest_active, "qst_edwyn_first_knight"),
				(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_current_state, qp4_edwyn_first_begun),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", qp4_edwyn_gather_info_chance_random),
				(assign, ":context", slot_quest_stage_1_trigger_chance),
				(assign, ":trigger_talk", 1),
			(else_try),
				### STAGE UPGRADE TRIGGER ( edwyn_first_knight ) 2 -> 3 ###
				(check_quest_active, "qst_edwyn_first_knight"),
				(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_current_state, qp4_edwyn_first_learn_about_knight),
				(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_stage_1_trigger_chance, "$current_town"), # Make sure we're actually on his trail.
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", qp4_edwyn_gather_info_chance_specific),
				(assign, ":context", slot_quest_stage_2_trigger_chance),
				(assign, ":trigger_talk", 1),
			(else_try),
				### STAGE UPGRADE TRIGGER ( edwyn_second_knight ) 1 -> 2 ###
				(check_quest_active, "qst_edwyn_second_knight"),
				(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_begun),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", qp4_edwyn_gather_info_chance_random),
				(assign, ":context", slot_quest_stage_1_trigger_chance),
				(assign, ":trigger_talk", 1),
			(else_try),
				### STAGE UPGRADE TRIGGER ( edwyn_second_knight ) 2 -> 3 ###
				(check_quest_active, "qst_edwyn_second_knight"),
				(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_learn_of_location),
				(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_stage_1_trigger_chance, "$current_town"), # Make sure we're actually on his trail.
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", qp4_edwyn_gather_info_chance_specific),
				(assign, ":context", slot_quest_stage_2_trigger_chance),
				(assign, ":trigger_talk", 1),
			(else_try),
				### STAGE UPGRADE TRIGGER ( edwyn_third_knight ) 1 -> 2 ###
				(check_quest_active, "qst_edwyn_third_knight"),
				(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_begun),
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", qp4_edwyn_gather_info_chance_random),
				(assign, ":context", slot_quest_stage_1_trigger_chance),
				(assign, ":trigger_talk", 1),
			(else_try),
				### STAGE UPGRADE TRIGGER ( edwyn_third_knight ) 2 -> 3 ###
				(check_quest_active, "qst_edwyn_third_knight"),
				(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_last_seen_location),
				(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_stage_1_trigger_chance, "$current_town"), # Make sure we're actually on his trail.
				(store_random_in_range, ":roll", 0, 100),
				(lt, ":roll", qp4_edwyn_gather_info_chance_specific),
				(assign, ":context", slot_quest_stage_2_trigger_chance),
				(assign, ":trigger_talk", 1),
			(try_end),
			(eq, ":trigger_talk", 1),
			(assign, "$g_talk_troop", NPC_Edwyn),
			(assign, "$npc_map_talk_context", ":context"), # Troop wants to talk about nearing expiration.
			(start_map_conversation, NPC_Edwyn),
		]
	),
	
	# TRIGGER: Check twice daily to see if Edwyn learned any news of the knights from his story line.
	(1,[
			### STAGE UPGRADE TRIGGER ( edwyn_first_knight ) 3 -> 4 ###
			(map_free),
			(check_quest_active, "qst_edwyn_first_knight"),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_first_learn_of_lair_location),
			(quest_get_slot, ":bandit_lair", "qst_edwyn_first_knight", slot_quest_target_party),
			#(call_script, "script_cf_qus_party_close_to_center", "p_main_party", ":bandit_lair", 3),
			(store_distance_to_party_from_party, ":distance", ":bandit_lair", "p_main_party"),
			(lt, ":distance", 3),
			(party_set_flags, ":bandit_lair", pf_always_visible, 1),
			(display_message, "@You have discovered the location of Sir Tenry's lair."),
			(call_script, "script_common_quest_change_state", "qst_edwyn_first_knight", qp4_edwyn_first_found_lair_on_map),
			(call_script, "script_qp4_quest_edwyn_first_knight", floris_quest_update),
		]
	),
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