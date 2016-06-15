# Quest Pack 5 (1.0) by Windyplains

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
	
	## QUEST - EXPAND YOUR TALENTS
	## PURPOSE - Check if the tutorial quest for "Expand Your Talents" needs to be triggered.
	(1,	[
			(map_free),
			(eq, "$enable_tutorials", 1),
			(neg|check_quest_active, "qst_qp6_expanding_your_talents"),
			(assign, ":continue", 0),
			(store_character_level, ":level", "trp_player"),
			(try_begin),
				(ge, ":level", 5),
				(troop_slot_eq, "trp_player", slot_troop_ability_1, BONUS_UNASSIGNED),
				(assign, ":continue", 1),
				(assign, ":assignment_level", 5),
			(else_try),
				(ge, ":level", 10),
				(troop_slot_eq, "trp_player", slot_troop_ability_2, BONUS_UNASSIGNED),
				(assign, ":continue", 1),
				(assign, ":assignment_level", 10),
			(else_try),
				(ge, ":level", 15),
				(troop_slot_eq, "trp_player", slot_troop_ability_3, BONUS_UNASSIGNED),
				(assign, ":continue", 1),
				(assign, ":assignment_level", 15),
			(else_try),
				(ge, ":level", 20),
				(troop_slot_eq, "trp_player", slot_troop_ability_4, BONUS_UNASSIGNED),
				(assign, ":continue", 1),
				(assign, ":assignment_level", 20),
			(else_try),
				(ge, ":level", 25),
				(troop_slot_eq, "trp_player", slot_troop_ability_5, BONUS_UNASSIGNED),
				(assign, ":continue", 1),
				(assign, ":assignment_level", 25),
			(else_try),
				(ge, ":level", 30),
				(troop_slot_eq, "trp_player", slot_troop_ability_6, BONUS_UNASSIGNED),
				(assign, ":continue", 1),
				(assign, ":assignment_level", 30),
			(try_end),
			(eq, ":continue", 1),
			(quest_set_slot, "qst_qp6_expanding_your_talents", slot_quest_temp_slot, ":assignment_level"),
			# INITIATE QUEST
			(call_script, "script_qp6_quest_expanding_your_talents", floris_quest_begin),
			(try_begin),
				(eq, "$enable_popups", 1),
				(assign, reg21, ":assignment_level"),
				(dialog_box, "str_qp6_q1_popup_intro", "@Expanding Your Talents (Level {reg21})"),
			(try_end),
		]),
		
	## QUEST - ASSIGNING A STOREKEEPER
	## PURPOSE - Check if the tutorial quest for "Assigning a Storekeeper" needs to be triggered.
	(4,	[
			(map_free),
			(eq, "$enable_tutorials", 1),
			# Allow only one of these tutorial quests to be active at a time.
			(neg|check_quest_active, "qst_qp6_storekeeper_assignment"),
			(neg|check_quest_active, "qst_qp6_quartermaster_assignment"),
			(neg|check_quest_active, "qst_qp6_jailer_assignment"),
			
			# No companion currently is in the storekeeper role.
			(eq, "$cms_role_storekeeper", "trp_player"),
			
			# We only want this tutorial quest to trigger once.
			(neg|check_quest_succeeded, "qst_qp6_storekeeper_assignment"),
			
			# Someone qualifies to fit the role.
			(assign, ":continue", 0),
			(set_show_messages, 0),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				(call_script, "script_cf_cms_check_if_qualified_for_role", ":troop_no", ROLE_STOREKEEPER), # cms_scripts.py
				(assign, ":continue", 1),
			(try_end),
			(set_show_messages, 1),
			(eq, ":continue", 1),
			
			# INITIATE QUEST
			(call_script, "script_qp6_storekeeper_assignment", floris_quest_begin),
			(try_begin),
				(eq, "$enable_popups", 1),
				(str_store_string, s21, "@You currently have no companion assigned to the Storekeeper role, yet have a qualified companion that can fulfill this duty.\
										^^Setting up a companion Storekeeper is beneficial in reducing the grind associated with maintain a food source for your troops as well as using their own inventory to carry the stores."),
				(dialog_box, s21, "@Assigning a Storekeeper"),
			(else_try),
				(display_message, "@New Quest Received: Assigning a Storekeeper.", gpu_green),
			(try_end),
		]),
		
	## QUEST - ASSIGNING A QUARTERMASTER
	## PURPOSE - Check if the tutorial quest for "Assigning a Quartermaster" needs to be triggered.
	(4,	[
			(map_free),
			(eq, "$enable_tutorials", 1),
			# Allow only one of these tutorial quests to be active at a time.
			(neg|check_quest_active, "qst_qp6_storekeeper_assignment"),
			(neg|check_quest_active, "qst_qp6_quartermaster_assignment"),
			(neg|check_quest_active, "qst_qp6_jailer_assignment"),
			
			# No companion currently is in the quartermaster role.
			(eq, "$cms_role_quartermaster", "trp_player"),
			
			# We only want this tutorial quest to trigger once.
			(neg|check_quest_succeeded, "qst_qp6_quartermaster_assignment"),
			
			# Someone qualifies to fit the role.
			(assign, ":continue", 0),
			(set_show_messages, 0),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				(call_script, "script_cf_cms_check_if_qualified_for_role", ":troop_no", ROLE_QUARTERMASTER), # cms_scripts.py
				(assign, ":continue", 1),
			(try_end),
			(set_show_messages, 1),
			(eq, ":continue", 1),
			
			# INITIATE QUEST
			(call_script, "script_qp6_quartermaster_assignment", floris_quest_begin),
			(try_begin),
				(eq, "$enable_popups", 1),
				(str_store_string, s21, "@You currently have no companion assigned to the Quartermaster role, yet have a qualified companion that can fulfill this duty.\
										^^Setting up a companion Quartermaster is beneficial in reducing the grind associated with collecting battlefield loot, storing battlefield loot and selling it to merchants.  Your Quartermaster will store all collected loot within his own inventory."),
				(dialog_box, s21, "@Assigning a Quartermaster"),
			(else_try),
				(display_message, "@New Quest Received: Assigning a Quartermaster.", gpu_green),
			(try_end),
		]),
		
	## QUEST - ASSIGNING A GAOLER
	## PURPOSE - Check if the tutorial quest for "Assigning a Gaoler" needs to be triggered.
	(4,	[
			(map_free),
			(eq, "$enable_tutorials", 1),
			# Allow only one of these tutorial quests to be active at a time.
			(neg|check_quest_active, "qst_qp6_storekeeper_assignment"),
			(neg|check_quest_active, "qst_qp6_quartermaster_assignment"),
			(neg|check_quest_active, "qst_qp6_jailer_assignment"),
			
			# No companion currently is in the quartermaster role.
			(eq, "$cms_role_jailer", "trp_player"),
			
			# We only want this tutorial quest to trigger once.
			(neg|check_quest_succeeded, "qst_qp6_jailer_assignment"),
			
			# Someone qualifies to fit the role.
			(assign, ":continue", 0),
			(set_show_messages, 0),
			(try_for_range, ":troop_no", companions_begin, companions_end),
				(main_party_has_troop, ":troop_no"),
				(call_script, "script_cf_cms_check_if_qualified_for_role", ":troop_no", ROLE_JAILER), # cms_scripts.py
				(assign, ":continue", 1),
			(try_end),
			(set_show_messages, 1),
			(eq, ":continue", 1),
			
			# INITIATE QUEST
			(call_script, "script_qp6_jailer_assignment", floris_quest_begin),
			(try_begin),
				(eq, "$enable_popups", 1),
				(str_store_string, s21, "@You currently have no companion assigned to the Gaoler role, yet have a qualified companion that can fulfill this duty.\
										^^Setting up a companion Gaoler is beneficial allowing you to use their Prisoner Management skill for the purpose of determining your party's maximum number of prisoners as well as automatically selling prisoners to ransom brokers while holding on to any quest related prisoners.  Depending on their setting they will also automatically store prisoners in your keep."),
				(dialog_box, s21, "@Assigning a Gaoler"),
			(else_try),
				(display_message, "@New Quest Received: Assigning a Gaoler.", gpu_green),
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