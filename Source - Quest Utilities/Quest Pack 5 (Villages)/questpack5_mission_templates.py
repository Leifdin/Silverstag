# Quest Pack 5 (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from module_mission_templates import *
from module_items import *
from module_sounds import *

mission_triggers = [

]

# def modmerge_mission_templates(orig_mission_templates):
	# find_i = find_object( orig_mission_templates, "arena_melee_fight" )
	# orig_mission_templates[find_i][5].extend(AI_triggers)

def modmerge_mission_templates(orig_mission_templates, check_duplicates = False):
	if( not check_duplicates ):
		orig_mission_templates.extend(mission_triggers) # Use this only if there are no replacements (i.e. no duplicated item names)
		# for i in range(len(orig_mission_templates)):
			# mt_name = orig_mission_templates[i][0]
			# # Add storyline triggers to the default "walk around town/village/castle" mission templates.
			# if( mt_name=="town_default" or mt_name=="town_center" or mt_name=="village_center" or mt_name=="castle_visit"):
				# orig_mission_templates[i][5].extend(storyline_character_triggers)
			# # Add storyline triggers to companion storyline missions. 
			# if( mt_name=="odval_challenge" or mt_name=="edwyn_town_fight" or mt_name=="edwyn_village_fight"):
				# orig_mission_templates[i][5].extend(storyline_character_triggers)
			# # Add the following triggers to the bandit lair mission template. 
			# if( mt_name=="bandit_lair" ):
				# orig_mission_templates[i][5].extend(bandit_lair_triggers)
			
	else:
	# Use the following loop to replace existing entries with same id
		for i in range (0,len(mission_triggers)-1):
			find_index = find_object(orig_mission_templates, mission_triggers[i][0]); # find_object is from header_common.py
			if( find_index == -1 ):
				orig_mission_templates.append(mission_triggers[i])
			else:
				orig_mission_templates[find_index] = mission_triggers[i]
			
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