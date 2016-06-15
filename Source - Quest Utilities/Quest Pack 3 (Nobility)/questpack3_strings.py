# Quest Pack 3 (1.0) by Windyplains

strings = [

	# Quest Descriptions
	("qp3_quest_title",                             "Defense of the Realm Quest"),
	
	### QUEST: patrol_for_bandits
	("qp3_summoned_quest_text",                     "You have been requested to return to your owned lands in {s13} to help your steward with a matter of some importance."),
	("qp3_summoned_title",                          "Summoned to Hall"),
	
	### QUEST: patrol_for_bandits
	("qp3_patrol_bandits_quest_text",               "You have been requested to handle the emerging bandit population by your seneshal in the lands around {s13}.  You will need to eliminate at least {reg11} bandits in order to make enough of an impact."),
	("qp3_patrol_bandits_title",                    "Patrol for Bandits"),
	
	### QUEST: mercs_for_hire
	("qp3_mercs_for_hire_quest_text",               "You have been asked to deal with a large force of mercenaries that have setup camp outside within your lands.  They fly a flag of truce, but their true intentions are not known."),
	("qp3_mercs_for_hire_title",                    "Mercenaries for Hire"),
	# Mercenary leader names
	("qp3_merc_hero_name_1",                        "Mathrin Tallows"),
	("qp3_merc_hero_name_2",                        "Meric Landrin"),
	("qp3_merc_hero_name_3",                        "Alric Denfrick"),
	# Mercenary leader titles
	("qp3_merc_hero_title_1",                       "Captain"),
	("qp3_merc_hero_title_2",                       "Master"),
	("qp3_merc_hero_title_3",                       "Thane"),
	# Mercenary group names
	("qp3_merc_band_name_1",                        "Swadian Plainstriders"),     # Swadia
	("qp3_merc_band_name_2",                        "Black Tide Raiders"),        # Nord
	("qp3_merc_band_name_3",                        "Compagnia Falco d'Oro"),     # Rhodoks
	("qp3_merc_band_name_4",                        "Brotherhood of the Raven"),  # Nord
	("qp3_merc_band_name_5",                        "Steppe Lancers"),            # Khergit
	("qp3_merc_band_name_6",                        "Windriders"),                # Khergit
	("qp3_merc_band_name_7",                        "Whitemanes of the North"),   # Vaegirs
	("qp3_merc_band_name_8",                        "Wildclaws"),                 # Nord
	("qp3_merc_band_name_9",                        "Free Blades"),               # Swadia
	("qp3_merc_band_name_10",                       "Scorpions-al-Assadi"),       # Sarranid
	("qp3_merc_band_name_11",                       "Sandraiders"),               # Sarranid
	("qp3_merc_band_name_12",                       "Freemen of Calradia"),       # Undefined
	("qp3_merc_band_name_13",                       "Geroia Mercenaries"),        # Undefined
	("qp3_merc_band_name_14",                       "Balion Mercenaries"),        # Undefined
	("qp3_merc_band_name_end",                      "NOT USED"),
	("qp3_merc_band_name_15",                       "UNDEFINED"),
	("qp3_merc_band_name_16",                       "UNDEFINED"),
	("qp3_merc_band_name_17",                       "UNDEFINED"),
	("qp3_merc_band_name_18",                       "UNDEFINED"),
	("qp3_merc_band_name_19",                       "UNDEFINED"),
	("qp3_merc_band_name_20",                       "UNDEFINED"),
	
	### QUEST: destroy_the_lair
	("qp3_destroy_the_lair_quest_text",             "The bandit population around {s13} has become nearly unmanagable.  Your steward proposes the best response is a decisive assault upon their hideout.  It is up to you to find it."),
	("qp3_destroy_the_lair_title",                  "Destroy the Lair"),
	
	### QUEST: escort_to_mine
	("qp3_escort_to_mine_quest_text",               "The castle dunegeon in {s13} is overcrowded and your steward wishes to send a party of prisoners to the salt mines to generate extra revenue."),
	("qp3_escort_to_mine_title",                    "Escort Prisoners to Salt Mine"),
	
	# General
	("qp3_quest_s41_update_error",                  "ERROR - Quest '{s41}' - Failed to update on function {reg31}."),
	("qp3_quest_s41_update_note_error",             "ERROR - Quest '{s41}' - Failed to update quest note."),
	
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