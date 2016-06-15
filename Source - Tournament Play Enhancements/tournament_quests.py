# Tournament Play Enhancements (1.6) by Windyplains

from header_quests import *

quests = [
  ("floris_active_tournament", "Attend Tournament in {s13}", 0,
  "{!}A tournament of champions has begun in the town of {s13} where you should attend."),
  
  ("score_to_settle", "A Score to Settle", 0,
  "{!}After an embarassing defeat at the tournaments in {s13} by a fellow noble, you've decided to return the favor."),
  
  ("tpe_reserved_1", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("tpe_reserved_2", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("tpe_reserved_3", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("tpe_reserved_4", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("tpe_reserved_5", "Reserved Quest", 0,
  "{!}Quest Description"),
  
]
from util_common import *
from util_wrappers import *
def modmerge_quests(orig_quests):
    pos = list_find_first_match_i(orig_quests, "quests_end")
    OpBlockWrapper(orig_quests).InsertBefore(pos, quests)	
	
def modmerge(var_set):
    try:
        var_name_1 = "quests"
        orig_quests = var_set[var_name_1]
        modmerge_quests(orig_quests)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)