# Character Creation Presentation (1.0.2)
# Created by Windyplains.  Inspired by Dunde's character creation presentation in Custom Commander.

strings = [
	# Object Titles
	("ccp_label_done", "Done"),
	("ccp_label_back", "Back"),
	("ccp_label_default", "Default"),
	("ccp_label_random", "Randomize"),
	("ccp_label_menus", "Character Background"),
	("ccp_label_story", "Your Story"),
	("ccp_label_gender", "Your gender:"),
	("ccp_label_father", "Your father was:"),
	("ccp_label_earlylife", "You spent your early life as:"),
	("ccp_label_later", "Later you became:"),
	("ccp_label_reason", "The reason for an adventure:"),
	("ccp_label_gameplay_options", "Game Options"),
	("ccp_label_fog_of_war", "Fog of War"),
	("ccp_label_mtt", "Troop Tree"),
	("ccp_label_quest_reaction", "Quest Difficulty"),
	("ccp_label_mod_difficulty", "Mod Difficulty"),
	("ccp_label_gather_npcs", "Gather Companions"),
	("ccp_label_region", "Starting Region"),
	("ccp_empty", "{s31}"),
	("ccp_str", "STR"),
	("ccp_agi", "AGI"),
	("ccp_int", "INT"),
	("ccp_cha", "CHA"),
	("ccp_zero", "0"),
	("ccp_skl_ironflesh", "Ironflesh"),
	("ccp_skl_powerstrike", "Power Strike"),
	("ccp_skl_powerthrow", "Power Throw"),
	("ccp_skl_powerdraw", "Power Draw"),
	("ccp_skl_weaponmaster", "Weapon Master"),
	("ccp_skl_shield", "Shield"),
	("ccp_skl_athletics", "Athletics"),
	("ccp_skl_riding", "Riding"),
	("ccp_skl_horsearchery", "Horse Archery"),
	("ccp_skl_looting", "Looting"),
	("ccp_skl_foraging", "Foraging"),
	("ccp_skl_trainer", "Trainer"),
	("ccp_skl_tracking", "Tracking"),
	("ccp_skl_tactics", "Tactics"),
	("ccp_skl_pathfinding", "Path-finding"),
	("ccp_skl_spotting", "Spotting"),
	("ccp_skl_inventorymanagement", "Inventory Mgmt."),
	("ccp_skl_woundtreatment", "Wound Treatment"),
	("ccp_skl_surgery", "Surgery"),
	("ccp_skl_firstaid", "First Aid"),
	("ccp_skl_engineer", "Engineer"),
	("ccp_skl_persuasion", "Persuasion"),
	("ccp_skl_prisonermanagement", "Prisoner Mgmt."),
	("ccp_skl_leadership", "Leadership"),
	("ccp_skl_trade", "Trade"),
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