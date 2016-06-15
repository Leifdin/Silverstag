# -*- coding: cp1254 -*-

wse_warhorse_strings = [
("param1", "Param 1"),
("param1", "Param 2"),
("param1", "Param 3"),
("param1", "Param 4"),
("banner_adjuster", "Heraldic Adjuster"),
("debug", "Debug"),
("norm", "Normalize"),
("close", "Close"),
]

from util_common import *

def modmerge_strings(orig_strings):
    # add remaining strings
    from util_common import add_objects
    num_appended, num_replaced, num_ignored = add_objects(orig_strings, wse_warhorse_strings)
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