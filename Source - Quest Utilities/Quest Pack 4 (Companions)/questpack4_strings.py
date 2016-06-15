# Quest Pack 4 (1.0) by Windyplains

strings = [

	# Quest Descriptions
	("qp4_quest_title",                             "Companion Acquisition Quest"),
	# Odval
	("qp4_odval_intro_quest_text",                  "You've met a young {reg3?woman:man}, named {s14}, who tells you that {reg3?she:he}'s on the run from {reg3?her:his} home town of {s13} after being accused of cheating in an archery contest.  {reg3?She:He} wishes for you to help {reg3?her:him} clear {reg3?her:his} name with the village elder."),
	("qp4_odval_redemption_quest_text",             "You have agreed to help {s14} who is seeking to clear {reg3?her:his} name for misdeeds in the village of {s13} after being accused of cheating in an archery contest."),
	("qp4_odval_return_to_tulbuk_quest_text",       "You and {s14} must travel to the village of {s13} and speak with the village elder to clear {reg3?her:his} name.  {reg3?She:He} is accused of cheating in their recent archery contest."),
	("qp4_odval_accept_the_challenge_quest_text",   "You have agreed to stand beside {s14} as {reg3?she:he} faces {reg3?her:his} accusers in a contest of arms.  If victorious it should clear {reg3?her:his} name within the eyes of {reg3?her:his} kin."),
	("qp4_odval_saving_face_quest_text",            "Even though you and {s14} have proven yourselves victorious over {reg3?her:his} accusers, the elder believes that {s14} would not have won the field without your help.  You have suggested that a contest between the two of you could prove {reg3?her:his} worth so the elder has given you a few days to rest from your current match before returning to face one another."),
	# Edwyn
	("qp4_edwyn_intro_quest_text",                  "You've met a young {reg3?woman:man}, named {s14} who tells you of the death of {reg3?her:his} {reg3?husband:wife} and daughter's death at the hands of a band of rogue knights after one of their group died of illness on his farm."),
	("qp4_edwyn_revenge_quest_text",                "You've convinced {s14} to give up drinking over his sorrows and take vengeance for the harm done to {reg3?her:his} family.  Specifically you must hunt down the three knights responsible for the death of {reg3?her:his} {reg3?husband:wife} and daughter before bringing justice to them.  Since the laws of the land will not recognize the injustice inflicted upon a commoner, {s14} intends to find his own justice in revenge."),
	("qp4_edwyn_first_knight_quest_text",           "You've agreed to help track down and eliminate Sir Tenry Jerah.  He is one of the knights that murdered {s14}'s {reg3?husband:wife} and daughter before burning their farm to the ground."),
	("qp4_edwyn_second_knight_quest_text",          "You've agreed to help track down and eliminate Sir Henric Felkata.  He is one of the knights that murdered {s14}'s {reg3?husband:wife} and daughter before burning their farm to the ground."),
	("qp4_edwyn_third_knight_quest_text",           "You've agreed to help track down and eliminate Sir Gerrin Phelwin.  He is one of the knights that murdered {s14}'s {reg3?husband:wife} and daughter before burning their farm to the ground."),
	
	# Quest Titles
	# Odval
	("qp4_odval_intro_title",                       "{s14}'s Introduction"),
	("qp4_odval_redemption_title",                  "{s14}'s Redemption"),
	("qp4_odval_return_to_tulbuk_title",            "{s14}'s Return"),
	("qp4_odval_accept_the_challenge_title",        "{s14} Accepts the Challenge"),
	("qp4_odval_saving_face_title",                 "{s14}'s Challenge"),
	# Edwyn
	("qp4_edwyn_intro_title",                       "{s14}'s Introduction"),
	("qp4_edwyn_revenge_title",                     "{s14}'s Revenge"),
	("qp4_edwyn_first_knight_title",                "{s14}'s First Knight"),
	("qp4_edwyn_second_knight_title",               "{s14}'s Second Knight"),
	("qp4_edwyn_third_knight_title",                "{s14}'s Third Knight"),
	
	# Actors
	("qp4_odval_betrayed_judge_male",               "Batukhan"), # s1
	("qp4_odval_betrayed_judge_female",             "Bayarmaa"), # s2
	("qp4_odval_second_place_finisher",             "Bataar"),   # s3
	("qp4_odval_third_place_finisher",              "Chuluun"),  # s4
	
	# General
	("qp4_quest_s41_update_error",                  "ERROR - Quest '{s41}' - Failed to update on function {reg31}."),
	("qp4_quest_s41_update_note_error",             "ERROR - Quest '{s41}' - Failed to update quest note."),
	("qp4_error_actor_s41_not_found",               "ERROR - Actor '{s41}' not found in scene."),  
	
	### QUEST - Odval_accept_the_challenge ###
	# Tab Box Titles
	("qp4_odval_accept_the_challenge_cant_run",     "It's too late to run away now!"),
	("qp4_odval_accept_the_challenge_pre_fight",    "Your opponents have already seen your approach.  You should speak to the village elder to get this over with."),
	("qp4_odval_accept_the_challenge_post_fight",   "The contest is over.  Now speak with the village elder."),
	# Trash Talking Sequence
	("qp4_challenge_trash_talk_1",                  "{s14} shouts, 'Spineless cowards!  Now you will see why I deserved to win that contest!'"),
	("qp4_challenge_trash_talk_2",                  "{s3} says, 'Coward?  You were the rabbit fleeing at the first sign of trouble.  It took this foreigner to drag you back for judgment.'"),
	("qp4_challenge_trash_talk_3",                  "{reg3?{s1}:{s2}} says, 'You won't sleep your way through this one, {reg3?wench:knave}!'"),
	("qp4_challenge_trash_talk_4",                  "{s14} says, 'As if I'd give a filthy pig like you that chance.'"),
	("qp4_challenge_trash_talk_5",                  "{s14} says, 'Submit and I'll take it easy on you!'"),
	("qp4_challenge_trash_talk_6",                  "{s14} says, '...I'll only break one of your arms instead of your neck!'"),
	("qp4_challenge_trash_talk_7",                  "{s4} says, 'The only thing you've managed to break is my patience.'"),
	
	### QUEST - Odval_saving_face ###
	# Tab Box Titles
	("qst_odval_saving_face_pre_fight",             "Your opponents have already seen your approach.  You should speak to the village elder to get this over with."),
	("qp4_odval_accept_the_challenge_post_fight",   "The contest is over.  Now speak with the village elder."),
	
	### QUEST - odval_redemption ###
	("qp4_redemp_success_odval_won_duel",           "I just wanted to say I know what you did back in {s13} and want you to know that you've earned a loyal friend this day."),
	("qp4_redemp_success_odval_lost_duel",          "Well you certainly proved yourself in a fight, but did you have to do it so soundly in front of my kinsfolk?"),
	("qp4_redemp_success_player_refused_duel",      "You were right back there.  After we trashed those louts back there I should not have been required to prove my value in the fight.  I'll fight at your side any day."),
	("qp4_redemp_success_odval_wounded_but_okay",   "I didn't even see that guy approaching from behind.  Thankfully I had you watching my back, friend.  I may not have resolved everything, but at least this is behind me now."),
	("qp4_redemp_success_player_lost_challenge",    "I cannot believe those horse-faced farmers beat us back there, but at least this is behind me.  I can't go back to {s13}, but at least I have a future in your company."),
	("qp4_redemp_failure_odval_lost_duel",          "You spoke of helping me clear my name only to cut me down in front of my kinfolk?  I can not follow someone with such little honor.  As it is there isn't room for another dagger in my back!"),
	("qp4_redemp_failure_player_refused_duel",      "Why would you suggest a contest between the two of us to clear my name only to refuse to participate in it?  Well thanks for nothing.  I'll find my own path from here."),
	("qp4_redemp_failure_odval_wounded_but_okay",   "Well that didn't turn out the way I had hoped.  I appreciate everything you've done, but I think I should make my own way now.  Take care, {playername}."),
	("qp4_redemp_failure_odval_wounded_not_okay",   "Well that didn't turn out the way I had hoped.  I appreciate everything you've done, but I think I should make my own way now.  Take care, {playername}."),
	("qp4_redemp_failure_player_lost_challenge",    "I cannot believe those horse-faced farmers beat us back there!  I can never go back to {s13} unless I want to find myself tied to a stake and stoned within an inch of my life as an example.  A fine mess your help made of all of this!  I will find my own way from here on out."),
	("qp4_redemp_failure_player_refused_challenge", "Why would you have pushed that I come all of this way only to abandon me when I needed your help?  I didn't stand a chance against those men alone.  I can never go back to {s13} and I certainly have no intention in remaining with your group.  With friends like you I'd be safer dealing with bandits!"),
	
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