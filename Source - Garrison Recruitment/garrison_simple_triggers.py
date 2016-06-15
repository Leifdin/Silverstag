# Garrison Recruitment & Training by Windyplains

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

### TRIGGER: PROCESS GARRISON RECRUITMENT
(24*7, 
	[
		(try_begin),
			(ge, DEBUG_GARRISON, 1),
			(display_message, "@DEBUG (GRT): Weekly garrison upgrading pulse.", gpu_debug),
		(try_end),
		
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			
			## GARRISON RECRUITMENT
			(try_begin),
				## Are we recruiting?
				(party_slot_eq, ":center_no", slot_center_recruiting, 1), # We're recruiting to the garrison.
				## Do we have sufficient funds?
				(party_get_slot, ":budget_recruitment", ":center_no", slot_party_queue_budget),
				(try_begin),
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(call_script, "script_cf_diplomacy_treasury_verify_funds", ":budget_recruitment", ":center_no", FUND_FROM_TREASURY, TREASURY_FUNDS_AVAILABLE), # diplomacy_scripts.py
					(call_script, "script_diplomacy_treasury_withdraw_funds", ":budget_recruitment", ":center_no", FUND_FROM_TREASURY), # diplomacy_scripts.py
					(call_script, "script_grt_process_weekly_hiring", ":center_no", GRT_QUEUE_PROCESS),
				(else_try),
					## PLAYER OWNS FIEF - NOTIFICATION OF FAILURE
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(assign, reg31, ":budget_recruitment"),
					(str_store_party_name, s31, ":center_no"),
					(play_sound, "snd_quest_failed"),
					(display_message, "@{s31} was unable to hire new recruits due to insufficient funding.", gpu_red),
				# (else_try),
					# ## AI OWNS FIEF - DEBUG MESSAGE
					# (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					# ## TODO: Charge the AI.
					# (call_script, "script_grt_process_weekly_hiring", ":center_no", GRT_QUEUE_PROCESS),
				(try_end),
			(try_end),
			
			## GARRISON TRAINING
			(try_begin),
				## Prerequisites
				(party_slot_eq, ":center_no", slot_center_upgrade_garrison, 1), # We're training this garrison.
				# We have a valid captain of the guard stationed.
				(party_get_slot, ":advisor_captain", ":center_no", slot_center_advisor_war),
				(is_between, ":advisor_captain", companions_begin, companions_end),
				## Do we have sufficient funds?
				(party_get_slot, ":budget_training", ":center_no", slot_center_training_budget),
				(try_begin),
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(call_script, "script_cf_diplomacy_treasury_verify_funds", ":budget_training", ":center_no", FUND_FROM_TREASURY, TREASURY_FUNDS_AVAILABLE), # diplomacy_scripts.py
					(call_script, "script_diplomacy_treasury_withdraw_funds", ":budget_training", ":center_no", FUND_FROM_TREASURY), # diplomacy_scripts.py
					(call_script, "script_grt_convert_gold_to_xp_training", ":center_no", ":budget_training", GRT_TRAINING_PROCESS),
					(str_store_party_name, s21, ":center_no"),
				(else_try),
					## PLAYER OWNS FIEF - NOTIFICATION OF FAILURE
					(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					(assign, reg31, ":budget_training"),
					(str_store_party_name, s31, ":center_no"),
					(play_sound, "snd_quest_failed"),
					(display_message, "@{s31} was unable to upgrade its garrison due to insufficient funding.", gpu_red),
				# (else_try),
					# ## AI OWNS FIEF - DEBUG MESSAGE
					# (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
					# ## TODO: Charge the AI.
					# (call_script, "script_grt_process_weekly_hiring", ":center_no", GRT_QUEUE_PROCESS),
				(try_end),
			(try_end),
			
		(try_end),
    ]),

### TRIGGER: TEMPORARY HIRING COST REDUCTION DURATION COUNTDOWN
(24, 
	[
		## GARRISON RECRUITMENT EMBLEM COOLDOWN
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_ge, ":center_no", slot_center_queue_cost_reduce_duration, 1),
			(party_get_slot, ":hours", ":center_no", slot_center_queue_cost_reduce_duration),
			(val_sub, ":hours", 24),
			(val_max, ":hours", 0),
			(party_set_slot, ":center_no", slot_center_queue_cost_reduce_duration, ":hours"),
		(try_end),
		
		## GARRISON TRAINING EMBLEM COOLDOWN
		(try_for_range, ":center_no", centers_begin, centers_end),
			(party_slot_ge, ":center_no", slot_center_training_emblem_duration, 1),
			(party_get_slot, ":hours", ":center_no", slot_center_training_emblem_duration),
			(val_sub, ":hours", 24),
			(val_max, ":hours", 0),
			(party_set_slot, ":center_no", slot_center_training_emblem_duration, ":hours"),
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