# Garrison Recruitment & Training by Windyplains

strings = [
###########################################################################################################################
#####                                                COMMON STRINGS                                                   #####
###########################################################################################################################
	("grt_done",                  "Done"),
	("grt_general",               "General Info "),
	("grt_recruitment",           "Recruitment "),
	("grt_current_queue",         "Queue "),
	("grt_training",              "Training "),
	("grt_reordering",            "Reordering "),
	("grt_garrison_count",        "{reg21} are currently stationed here"),
	("grt_troop_wages",           "They cost {reg21} denars each per week"), # "Weekly wages {reg21} denars each"),
	("grt_troop_wages_total",     "All {reg21} stationed cost {reg22} denars weekly"), # Total wages are {reg22} denars"),
	("grt_troop_info",            "Troop Information"),
	("grt_button_recruit",        "Add to Queue"),
	("grt_button_dismiss",        "Remove from Queue"),
	("grt_queue_count",           "{reg21} Queued"),
	("grt_recruitment_header","This is a list of what is currently in the garrison."),
	("grt_s21",                   "{s21}"),
	("grt_budget_spending",       "Budget Spending"),
	("grt_budget_focused",        "Focused Spending"),
	("grt_budget_split",          "Split Spending"),
	("grt_queue_title",           "Current Queue"),
	("grt_recruitment_enable",    "Enable Recruiting"),
	("grt_estimated_hires",       "Should Be Hired Next Week:"),
	("grt_debug_advance",         "Advance 1 Week"),
	("grt_debug_advance_label",   "DEBUGGING"),
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