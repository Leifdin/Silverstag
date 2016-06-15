# Quest Pack 7 by Windyplains

# WHAT THIS FILE DOES:
# Adds "combat_enhancement_triggers" to every mission template with mtf_battle_mode to enable health regeneration on killing.

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *

battle_triggers = [  

## TRIGGER: QUEST - qst_qp7_freemans_return
## PURPOSE: If the Nervous Man / Fugitive is slain during combat then the quest fails.
(ti_on_agent_killed_or_wounded, 0, 0, [],
    [
		(store_trigger_param_1, ":agent_no"),
		
		(check_quest_active, "qst_qp7_freemans_return"),
		(quest_get_slot, ":troop_object", "qst_qp7_freemans_return", slot_quest_object_troop),
		(main_party_has_troop, ":troop_object"),
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		(eq, ":troop_no", ":troop_object"),
		(call_script, "script_qp7_quest_freemans_return", floris_quest_fail),  ## Quest Completed.
    ]),

]


def modmerge_mission_templates(orig_mission_templates):
	
	for i in range (0,len(orig_mission_templates)):
		# brute force add formation triggers to all mission templates with mtf_battle_mode
		if( orig_mission_templates[i][1] & mtf_battle_mode ):
			orig_mission_templates[i][5].extend(battle_triggers)
		# brute force add formation triggers to all mission templates with mtf_arena_fight
		if( orig_mission_templates[i][1] & mtf_arena_fight ):
			orig_mission_templates[i][5].extend(battle_triggers)
		
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
	
	##Extending Mission Templates' trigger lists with triggers appropriate to the templates
	for i in range(len(orig_mission_templates)):
		mt_name = orig_mission_templates[i][0]
		if(mt_name=="bandits_at_night"):
			orig_mission_templates[i][5].extend(battle_triggers)