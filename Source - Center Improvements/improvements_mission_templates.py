# Center Improvements (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *

###########################################################################################################################
#####                                             DYNAMIC WEAPON SYSTEM                                               #####
###########################################################################################################################
reload_triggers = [  
(60, 0, 0, [],
    [
		# Ensure this is a siege situation.
		(is_between, "$g_encountered_party", walled_centers_begin, walled_centers_end),   # Sieges
		# Ensure we have the appropriate improvement for getting arrow reloads.
		(party_slot_ge, "$g_encountered_party", slot_center_has_armoury, cis_built),
		# A damaged armoury should work less often.
		(assign, ":continue", 0),
		(try_begin),
			(party_slot_ge, "$g_encountered_party", slot_center_has_armoury, cis_damaged_20_percent),
			(party_get_slot, ":status", "$g_encountered_party", slot_center_has_armoury),
			(val_sub, ":status", cis_built),
			(val_mul, ":status", 20),
			(store_random_in_range, ":roll", 0, 100),
			(ge, ":roll", ":status"), # The more damaged (higher ":status" #) the harder this is to achieve.
			(assign, ":continue", 1),
		(try_end),
		(this_or_next|party_slot_eq, "$g_encountered_party", slot_center_has_armoury, cis_built),
		(eq, ":continue", 1),
		
		# Figure out which side the defenders are.
		(store_faction_of_party, ":faction_defending", "$g_encountered_party"),
		(try_begin),
			(eq, ":faction_defending", "$players_kingdom"),
			(assign, ":player_is_defending", 1),
		(else_try),
			(assign, ":player_is_defending", 0),
		(try_end),
		
		# Sift through the agents and replenish the ammunition of the defenders.
		(get_player_agent_no, ":agent_player"),
		(agent_get_team, ":team_player", ":agent_player"),
		(try_for_agents, ":agent_no"),
			(agent_is_human, ":agent_no"),
			(agent_is_alive, ":agent_no"),
			(agent_get_team, ":team_no", ":agent_no"),
			(try_begin),
				(eq, ":player_is_defending", 1),
				(eq, ":team_no", ":team_player"),
				(agent_refill_ammo, ":agent_no"),
			(else_try),
				(eq, ":player_is_defending", 0),
				(neq, ":team_no", ":team_player"),
				(agent_refill_ammo, ":agent_no"),
			(try_end),
		(try_end),
		(eq, ":player_is_defending", 1),
		(display_message, "@Runners have arrived to replenish your stores of ranged ammunition.", gpu_green),
	]),
]

def modmerge_mission_templates(orig_mission_templates):
	# brute force add dws_triggers to all mission templates with mtf_battle_mode
	for i in range (0,len(orig_mission_templates)):
		if( orig_mission_templates[i][1] & mtf_battle_mode ):
			orig_mission_templates[i][5].extend(reload_triggers)

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