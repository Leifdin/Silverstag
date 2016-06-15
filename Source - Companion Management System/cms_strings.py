# Companion Management System (1.0) by Windyplains

strings = [
###########################################################################################################################
#####                                                COMMON STRINGS                                                   #####
###########################################################################################################################
	("cms_accept",                  "Accept Changes"),
	("cms_cancel",                  "Exit"),
	("cms_s21",                     "{s21}"),
	("cms_blank",                   " "),
	("cms_r21",                     "{reg21}"),
	
###########################################################################################################################
#####                                             DYNAMIC WEAPON SYSTEM                                               #####
###########################################################################################################################
	# Settings Panel
	("dws_test",                    "Test"),
	("dws_main_title",              "Dynamic Weapon Set Configuration"),
	("dws_battlefield_title",       "Battlefield Equipment Set"),
	("dws_siege_title",             "Siege Equipment Set"),
	("dws_inventory_title",         "Available Inventory"),
	("dws_selected_title",          "Selected Item"),
	("dws_checkbox_enable",         "Enable Switching"),
	("dws_checkbox_all_or_nothing", "'All or Nothing'"),
	("dws_checkbox_report",         "Report Activity"),
	
###########################################################################################################################
#####                                               AUTOLOOT SYSTEM                                                   #####
###########################################################################################################################
	# AUTOLOOT SETTINGS PANEL
	("als_main_title", "{s21}'s Autoloot Settings"),
	("als_label_slot_1", "Weapon 1"),
	("als_label_slot_2", "Weapon 2"),
	("als_label_slot_3", "Weapon 3"),
	("als_label_slot_4", "Weapon 4"),
	("als_label_slot_5", "Helm"),
	("als_label_slot_6", "Armor"),
	("als_label_slot_7", "Boots"),
	("als_label_slot_8", "Gauntlets"),
	("als_label_slot_9", "Mount"),
	("als_apply_to_all", "Apply to All Companions"),
	("als_checkbox_enable", "Enable Autolooting"),
	("als_checkbox_breaking_sets", "Do not break weapon sets"),
	("als_checkbox_heralic", "Retain heraldic equipment"),
	("als_label_strength", "Strength:"),
	("als_label_powerdraw", "Power Draw:"),
	("als_label_powerthrow", "Power Throw:"),
	("als_label_shield", "Shield:"),
	("als_label_riding", "Riding:"),
	("als_label_horsearchery", "Horse Archery:"),
	("als_label_abilities", "Skills & Attributes"),
	("als_label_r21", "{reg21}"),
	("als_label_onehand", "One Hand:"),
	("als_label_twohand", "Two Hand:"),
	("als_label_polearm", "Polearm:"),
	("als_label_archery", "Archery:"),
	("als_label_crossbow", "Crossbow:"),
	("als_label_thrown", "Throwing:"),
	("als_label_search", "Search Player Inventory"),
	("als_label_copy", "Copy Settings to All"),
	("als_label_actual_gear", "Equipment Page"),
	("als_label_weight_limit", "Restrict to:"),
	("als_label_r21_of_r22", "{reg21} / {reg22} lbs."),
	
	# AUTOLOOT CONFIRMATION SCREEN
	("alc_main_title", "Autoloot Confirmation Screen"),
	("alc_sub_title", "Your companion would like to make the following upgrades.  Check / uncheck the box to approve / disapprove each."),
	("alc_header_approval", "Approve"),
	("alc_header_companion", "Companion"),
	("alc_header_slot", "Location"),
	("alc_header_old", "Current Item"),
	("alc_header_new", "New Item"),
	("alc_header_special", "Comments"),
	("alc_confirm", "Allow & Continue"),
	("alc_skip", "Skip to Next"),
	("alc_label_s41", "{s41}"),
	# Testing strings.
	("alc_itp_type_horse",          "horse"),
	("alc_itp_type_one_handed_wpn", "one hand"),
	("alc_itp_type_two_handed_wpn", "two hand"),
	("alc_itp_type_polearm",        "polearm"),
	("alc_itp_type_arrows",         "arrows"),
	("alc_itp_type_bolts",          "bolts"),
	("alc_itp_type_shield",         "shield"),
	("alc_itp_type_bow",            "bow"),
	("alc_itp_type_crossbow",       "crossbow"),
	("alc_itp_type_thrown",         "thrown"),
	("alc_itp_type_goods",          "goods"),
	("alc_itp_type_head_armor",     "head armor"),
	("alc_itp_type_body_armor",     "body armor"),
	("alc_itp_type_foot_armor",     "foot armor"),
	("alc_itp_type_hand_armor",     "hand armor"),
	("alc_itp_type_pistol",         "pistol"),
	("alc_itp_type_musket",         "musket"),
	("alc_itp_type_bullets",        "bullets"),
	("alc_itp_type_animal",         "animal"),
	("alc_itp_type_book",           "book"),
	
	
###########################################################################################################################
#####                                           COMPANION RELATION MATRIX                                             #####
###########################################################################################################################
	("crm_main_title", "Companion Relations"),
	("crm_companion_status", "Status: {s21}"),
	("crm_morality_1", "Aristocratic ({reg21})"),
	("crm_morality_2", "Egalitarian ({reg21})"),
	("crm_morality_3", "Humanitarian ({reg21})"),
	("crm_morality_4", "Honest ({reg21})"),
	("crm_morality_5", "Pious ({reg21})"),
	("crm_morality_6", "Gladiator ({reg21})"),
	("crm_morality_7", "Egotistic ({reg21})"),
	("crm_title_companion", "Companion"),
	("crm_title_morality", "Morality"),
	("crm_title_friends", "Likes"),
	("crm_title_enemies", "Dislikes"),
	("crm_status_unhappy", "Unhappy"),
	("crm_status_discontent", "Grumbling"),
	("crm_status_neutral", "Neutral"),
	("crm_status_happy", "Happy"),
	("crm_label_morale", "Morale: {reg21}"),
	
###########################################################################################################################
#####                                                 PARTY ROLES                                                     #####
###########################################################################################################################
	("role_main_title", "Party Assignments"),
	("role_label_blank_s21", "{s21}"),
	# Storekeeper
	("role_label_storekeeper", "Storekeeper:"),
	("role_desc_storekeeper", "The storekeeper maintains the party's stash of consumable ^goods.  {reg21?She:He} is responsible for acquiring new food stocks ^either by purchasing these goods in town or acquiring them ^from fallen enemies.  {reg21?She:He} will ensure rotten food is ^discarded."),
	("role_desc_storekeeper_reqs", "Requires: Inventory Management 3+"),
	("role_label_storekeeper_reports", "Storekeeper's Report:"),
	("role_label_skr_food_morale", "Morale bonus from variety is {s21}{reg21}."),
	("role_label_skr_days_left", "We currently have {reg21} days of food remaining."),
	("role_label_skr_kinds_of_food", "I'm stocking {reg21} {s21} of food."),
	# Quartermaster
	("role_label_quartermaster", "Quartermaster:"),
	("role_desc_quartermaster", "The quartermaster handles the party's trade goods.  {reg21?She:He} will ^manage any equipment taken from the fallen enemies ^and attempt to obtain the best price available for it upon ^entering the next town for a 15% cut of the profit."),
	("role_desc_quartermaster_reqs", "Requires: Trade 3+, Inventory Management 3+"),
	("role_label_quartermaster_reports", "Quartermaster's Report:"),
	("role_label_qm_available_space", "Our bags have {reg21} of {reg22} spaces used."),
	("role_label_qm_loot_value", "We should be able to get {reg21} denars for our loot."),
	("role_label_qm_best_item", "{s21} is our most valuable item at {reg21} denars."),
	# Jailer
	("role_label_jailer", "Gaoler:"),
	("role_desc_jailer", "The gaoler manages the party's prisoners.  When a gaoler is ^hired their prisoner management skill will be used instead ^of your own to determine prisoner limitation.  {reg21?She:He} will try ^to sell prisoners for 15% of the profit upon enterting towns ^with a ransom broker."),
	("role_desc_jailer_reqs", "Requires: Prisoner Management 2+"),
	("role_label_jailer_reports", "Gaoler's Report:"),
	("role_label_jailer_prisoner_count", "We are currently managing {reg21} prisoner{reg22?s:}."),
	("role_label_jailer_no_prisoners", "We have no prisoners currently."),
	("role_label_jailer_prisoner_value", "I estimate their value at {reg21} denars."),
	("role_label_jailer_last_town", "The last town we visited with a slave trader ^was {s22}."),
	("role_label_jailer_last_town_invalid", "We haven't seen any slavers yet."),
	
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