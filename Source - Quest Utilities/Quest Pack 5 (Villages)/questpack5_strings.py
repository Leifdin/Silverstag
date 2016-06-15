# Quest Pack 5 (1.0) by Windyplains

strings = [
	
	# QUEST STATUS STRINGS
	("qp5_quest_status_0", "Not Started"),
	("qp5_quest_status_1", "Currently Active"),
	("qp5_quest_status_2", "Completed"),
	("qp5_quest_status_3", "Failed"),
	("qp5_quest_status_4", "Rejected"),
	
	# QUEST STATUS ERRORS
	("qp5_error_invalid_quest", "ERROR (QP5) - Attempting to use an invalid quest # for a village quest. [{s31}, #{reg31}]."),
	("qp5_error_invalid_center", "ERROR (QP5) - Quest '{s30}' attempting to use invalid center. [{s31}, #{reg31}]."),
	("qp5_quest_s41_update_error", "ERROR - Quest '{s41}' - Failed to update on function {reg31}."),
	("qp5_quest_s41_update_note_error", "ERROR - Quest '{s41}' - Failed to update quest note."),
	("qp5_error_actor_s41_not_found", "ERROR - Actor '{s41}' not found in scene."),  
	
	# QUEST TITLES
	("qp5_q1_title", "Deliver Grain"),
	("qp5_q2_title", "Deliver Cattle"),
	("qp5_q3_title", "Train the Peasants"),
	("qp5_q4_title", "A Craftsman's Knowledge"),
	("qp5_q5_title", "Sending Aid"),
	("qp5_q6_title", "A Healer's Touch"),
	("qp5_q7_title", "When Lambs Become Lions"),
	("qp5_q8_title", "Undefined"),
	("qp5_q9_title", "Undefined"),
	("qp5_q10_title", "Undefined"),
	("qp5_q11_title", "Undefined"),
	("qp5_q12_title", "Undefined"),
	("qp5_q13_title", "Undefined"),
	
	### QUEST: A CRAFTSMAN'S KNOWLEDGE ###
	# Death descriptions. (It seems he....)
	("qp5_ck_death_1", "fell from a make-shift platform, struck {reg21?her:his} head against a nearby cart and has passed away"),
	("qp5_ck_death_2", "was struck in the head from a falling tool and passed away."),
	("qp5_ck_death_end", " "),
	("qp5_ck_death_3", " "),
	("qp5_ck_death_4", " "),
	("qp5_ck_death_5", " "),
	("qp5_ck_death_6", " "),
	("qp5_ck_death_7", " "),
	("qp5_ck_death_8", " "),
	("qp5_ck_death_9", " "),
	("qp5_ck_death_10", " "),
	
	# Injury descriptions. (It seems he....)
	("qp5_ck_injury_1", "was helping to carry a large stack of wood and stumbled backwards letting the pile fall {reg21?her:his} leg resulting in it breaking."),
	("qp5_ck_injury_2", "shattered {reg21?her:his} hand between the side of the structure and a beam {reg21?she:he} was helping guide into place."),
	("qp5_ck_injury_3", "twisted {reg21?her:his} back tripping over a rope line."),
	("qp5_ck_injury_end", " "),
	("qp5_ck_injury_4", " "),
	("qp5_ck_injury_5", " "),
	("qp5_ck_injury_6", " "),
	("qp5_ck_injury_7", " "),
	("qp5_ck_injury_8", " "),
	("qp5_ck_injury_9", " "),
	("qp5_ck_injury_10", " "),
	
	# Quest Descriptions
	("qp5_quest_title",                             "Village Quest"),
	# Odval
	#("qp5_odval_intro_quest_text",                  "You've met a young {reg3?woman:man}, named {s14}, who tells you that {reg3?she:he}'s on the run from {reg3?her:his} home town of {s13} after being accused of cheating in an archery contest.  {reg3?She:He} wishes for you to help {reg3?her:him} clear {reg3?her:his} name with the village elder."),
	# General
	# ("qp5_quest_s41_update_error",                  "ERROR - Quest '{s41}' - Failed to update on function {reg31}."),
	# ("qp5_quest_s41_update_note_error",             "ERROR - Quest '{s41}' - Failed to update quest note."),
	# ("qp5_error_actor_s41_not_found",               "ERROR - Actor '{s41}' not found in scene."),  
	
]

from util_common import *

def modmerge_strings(orig_strings):
    # add remaining strings
    from util_common import add_objects
    num_appended, num_replaced, num_ignored = add_objects(orig_strings, strings)
    #print num_appended, num_replaced, num_ignored
	
	
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "strings"
        orig_strings = var_set[var_name_1]
        modmerge_strings(orig_strings)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)