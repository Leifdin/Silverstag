# Kingdom Management Tools (1.0.1) by Windyplains
# Released --/--/--

strings = [
###########################################################################################################################
#####                                                KMT 1.0 Additions                                                #####
###########################################################################################################################

	# Object Titles
	("kmt_done_button", "Done"),
	("kmt_title_holdings", "Estates of the Realm"),
	("kmt_title_names", "Noble"),
	("kmt_title_relations", "Relation"),
	("kmt_title_towns", "Towns"),
	("kmt_title_castles", "Castles"),
	("kmt_title_villages", "Villages"),
	("kmt_title_friends", "Allies"),
	("kmt_title_enemies", "Enemies"),
	
	# Dynamic Titles
	("kmt_s25", "{s25}"),
	("kmt_relation_to_you_reg0",    "{reg0}"),
	#("kmt_relation_with_king_reg1", "King:   {reg1}"),
	("kmt_footer_lords", "{reg0} Lords"),
	("kmt_footer_towns", "{reg0} Towns"),
	("kmt_footer_castles", "{reg0} Castles"),
	("kmt_footer_villages", "{reg0} Villages"),
	("kmt_opt_remove_background", "Remove Background"),
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