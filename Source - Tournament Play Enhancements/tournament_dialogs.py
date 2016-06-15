# Tournament Play Enhancements (1.6) by Windyplains

from header_common import *
from header_dialogs import *
from header_operations import *
from header_parties import *
from header_item_modifiers import *
from header_skills import *
from header_triggers import *
from ID_troops import *
from ID_party_templates import *
##diplomacy start+
from header_troops import ca_intelligence
from header_terrain_types import *
from header_items import * #For ek_food, and so forth
##diplomacy end+
from module_constants import *
## CC
from header_items import *
from header_troops import *
## CC


# #lord reputation type, for commentaries
# #"Martial" will be twice as common as the other types
# lrep_none           = 0 
# lrep_martial        = 1 #chivalrous but not terribly empathetic or introspective, - eg Richard Lionheart, your average 14th century French baron
# lrep_quarrelsome    = 2 #spiteful, cynical, a bit paranoid, possibly hotheaded - eg Robert Graves' Tiberius, some of Charles VI's uncles
# lrep_selfrighteous  = 3 #coldblooded, moralizing, often cruel - eg William the Conqueror, Timur, Octavian, Aurangzeb (although he is arguably upstanding instead, particularly after his accession)
# lrep_cunning        = 4 #coldblooded, pragmatic, amoral - eg Louis XI, Guiscard, Akbar Khan, Abd al-Aziz Ibn Saud
# lrep_debauched      = 5 #spiteful, amoral, sadistic - eg Caligula, Tuchman's Charles of Navarre
# lrep_goodnatured    = 6 #chivalrous, benevolent, perhaps a little too decent to be a good warlord - eg Hussein ibn Ali. Few well-known historical examples maybe. because many lack the drive to rise to faction leadership. Ranjit Singh has aspects
# lrep_upstanding     = 7 #moralizing, benevolent, pragmatic, - eg Bernard Cornwell's Alfred, Charlemagne, Salah al-Din, Sher Shah Suri

# lrep_roguish        = 8 #used for commons, specifically ex-companions. Tries to live life as a lord to the full
# lrep_benefactor     = 9 #used for commons, specifically ex-companions. Tries to improve lot of folks on land
# lrep_custodian      = 10 #used for commons, specifically ex-companions. Tries to maximize fief's earning potential

# #lreps specific to dependent noblewomen
# lrep_conventional    = 21 #Charlotte York in SATC seasons 1-2, probably most medieval aristocrats
# lrep_adventurous     = 22 #Tomboyish. However, this basically means that she likes to travel and hunt, and perhaps yearn for wider adventures. However, medieval noblewomen who fight are rare, and those that attempt to live independently of a man are rarer still, and best represented by pre-scripted individuals like companions
# lrep_otherworldly    = 23 #Prone to mysticism, romantic. 
# lrep_ambitious       = 24 #Lady Macbeth
# lrep_moralist        = 25 #Equivalent of upstanding or benefactor -- takes nobless oblige, and her traditional role as repository of morality, very seriously. Based loosely on Christine de Pisa 

dialogs	= [   
    ##### QUEST : FLORIS_ACTIVE_TOURNAMENT : BEGIN #####
	# [anyone,"start",
		# [
			# #(eq, "$g_talk_troop", "trp_custom_messenger"),
			# (eq, "$g_quest_attempt", "qst_floris_active_tournament"),
			# (neg|check_quest_active, "qst_floris_active_tournament"),
			# (quest_get_slot, ":troop_no", "qst_floris_active_tournament", slot_quest_giver_troop),
			# (str_store_troop_name, s21, ":troop_no"),
		# ], "Pardon, m'{Lord/Lady}, but I've been sent by {s21} to deliver this message to you.", "qp1_messenger_1", []],
		
    # [anyone|plyr,"qp1_messenger_1", [], "I see.  Let's see what this is about.", "qp1_messenger_2", []],
	
	# [anyone|plyr,"qp1_messenger_2", 
		# [
			# (quest_get_slot, ":troop_no", "qst_floris_active_tournament", slot_quest_giver_troop),
			# (str_store_troop_name, s21, ":troop_no"),
		# ], "Seems we have an engagement awaiting us in {s21}.", "close_window",
		# [
			# # Begin Quest
			# (change_screen_map),
		# ]],
	##### QUEST : FLORIS_ACTIVE_TOURNAMENT : END #####
	
]


lord_talk_addon	= [   
	##### QUEST : SCORE_TO_SETTLE : BEGIN #####
    [anyone,"lord_start",
		[
			(eq, 1, 0),
			(neg|check_quest_active, "qst_score_to_settle"),
			(quest_slot_eq, "qst_score_to_settle", slot_quest_giver_troop, "$g_talk_troop"),
			(quest_slot_eq, "qst_score_to_settle", slot_quest_current_state, qp1_score_to_settle_inactive),
		], "Well, well.  I see that you are up and about.  Word is that you could barely walk unaided after that disgraceful performance in {s13}.", "lord_sts_insult_offered", []],
	
	[anyone|plyr,"lord_sts_insult_offered",
		[], "Rumors are the truth of fools, even 'noble' ones.", "lord_sts_insult_returned", []],
	
	[anyone|plyr,"lord_sts_insult_offered",
		[], "I took some minor injuries, but it was nothing to be concerned about.", "lord_talk", []],
	
	# Insulted: Noble background.
	[anyone,"lord_sts_insult_returned",
		[
			(eq, "$background_type", cb_noble),
			(troop_get_type, ":type", "trp_player"),
			(try_begin),
				(eq, ":type", 0), # Male
				# TODO: Add in secondary check for if female discrimination is disabled.
				(str_store_string, s21, "@You may claim to be the child of a noble, but it is quite clear you lack any of the true refinement and knowledge that being a man of gentle background entails.  I will not have one such as you question my honor."),
			(else_try),
				(str_store_string, s21, "@I do not care for the opinion of a woman who does not know her place in this realm.  Do not test my patience further or I may forget the fact that you are supposed to be a lady."),
			(try_end),
		], "Do you presume to name me a fool?  {s21}", "lord_sts_insult_returned_2", []],
	
	# Insulted: Mercantile background.
	# [anyone,"lord_sts_insult_returned",
		# [
			# (eq, "$background_type", cb_merchant),
		# ], "Do you presume to name me a fool?", "lord_sts_insult_returned_2", 
		# [
			# (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1, 0),
		# ]],
	
	# Insulted: Commoner background.
	[anyone,"lord_sts_insult_returned",
		[
			(neq, "$background_type", cb_noble),
			(faction_get_slot, ":leader", "$players_kingdom", slot_faction_leader),
			(try_begin),
				(ge, ":leader", 1),
				(str_store_troop_name, s21, ":leader"),
				(troop_get_type, reg21, ":leader"),
			(else_try),
				(str_store_string, s21, "@The King"),
				(assign, reg21, 0),
			(try_end),
		], "{s21} may believe you to be of use to our cause, but I know you are little more than a peasant in the clothing of your betters.  Do not forget your place or I will be forced to remind you of it.", "lord_sts_insult_returned_2", 
		[
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2, 0),
		]],
	
	[anyone|plyr,"lord_sts_insult_returned_2",
		[
			(faction_get_slot, ":leader", "$players_kingdom", slot_faction_leader),
			(try_begin),
				(ge, ":leader", 1),
				(str_store_troop_name, s21, ":leader"),
				(troop_get_type, reg21, ":leader"),
			(else_try),
				(str_store_string, s21, "@the king"),
				(assign, reg21, 0),
			(try_end),
		], "A fool and a windbag as well it seems.  I don't have time for this.  Just be thankful that {s21} needs all of the vassals {reg21?she:he} can get or we would settle this here and now.", "lord_sts_insult_4", []],
		
	[anyone,"lord_sts_insult_4",
		[
			(eq, "$background_type", cb_noble),
			(troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
			(store_add, ":string_no", "str_comment_qp1_sts_insulted2_liege", ":reputation"),
			(str_store_string, s21, ":string_no"),
		], "{s21}", "lord_sts_insult_challenge_given", []],
		
	[anyone,"lord_sts_insult_4",
		[
			(neq, "$background_type", cb_noble),
			(troop_get_slot, ":reputation", "$g_talk_troop", slot_lord_reputation_type),
			(store_add, ":string_no", "str_comment_qp1_sts_insulted_liege", ":reputation"),
			(str_store_string, s21, ":string_no"),
		], "{s21}", "lord_sts_insult_challenge_given", []],
		
	[anyone|plyr,"lord_sts_insult_challenge_given",
		[], "Very well.  I'll deal with you on the field.", "close_window", 
		[
			(call_script, "script_quest_score_to_settle", floris_quest_begin),
		]],
		
	[anyone|plyr,"lord_sts_insult_challenge_given",
		[], "I have better uses for my time like guarding our territory.", "lord_sts_challenge_rejected", 
		[]],
		
	[anyone,"lord_sts_challenge_rejected",
		[], "Go then.  Hide your cowardice behind your duty, but this is not settled between us.", "close_window", 
		[
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -5, 0),
		]],
		
	# Talking to this lord at any point in the quest prior to completion results in this.
	[anyone,"lord_start",
		[
			(eq, 1, 0),
			(check_quest_active, "qst_score_to_settle"),
			(quest_slot_eq, "qst_score_to_settle", slot_quest_giver_troop, "$g_talk_troop"),
			(quest_get_slot, ":stage", "qst_score_to_settle", slot_quest_current_state),
			(is_between, ":stage", qp1_score_to_settle_begun, qp1_score_to_settle_defeated_thrice),
		], "Well, well.  I see that you are up and about.  Word is that you could barely walk unaided after that disgraceful performance in {s13}.", "lord_sts_insult_offered", []],
	
	# After proving yourself the winner this dialog should trigger upon next meeting.
	[anyone,"lord_start",
		[
			(eq, 1, 0),
			(check_quest_active, "qst_score_to_settle"),
			(quest_slot_eq, "qst_score_to_settle", slot_quest_giver_troop, "$g_talk_troop"),
			(quest_slot_eq, "qst_score_to_settle", slot_quest_current_state, qp1_score_to_settle_defeated_thrice),
		], "sdf", "lord_sts_insult_offered", []],
	
	
	##### QUEST : SCORE_TO_SETTLE : END #####
	
	##### QUEST : FLORIS_ACTIVE_TOURNAMENT : BEGIN #####
    [anyone,"lord_start",
		[
			(check_quest_active, "qst_floris_active_tournament"),
			(quest_get_slot, ":troop_no", "qst_floris_active_tournament", slot_quest_giver_troop),
			(eq, "$g_talk_troop", ":troop_no"),
			(quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_message_received),
			(quest_set_slot, "qst_floris_active_tournament", slot_quest_current_state, 0),
			(str_store_troop_name, s21, ":troop_no"),
		], "I see you received my invitation to our games.  It is good to have you among us.", "lord_talk", []],
		
    [anyone,"lord_start",
		[
			(neg|check_quest_active, "qst_floris_active_tournament"),
			(quest_get_slot, ":troop_no", "qst_floris_active_tournament", slot_quest_giver_troop),
			(eq, "$g_talk_troop", ":troop_no"),
			(quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_refused_invitation),
			(quest_set_slot, "qst_floris_active_tournament", slot_quest_current_state, 0),
			(str_store_troop_name, s21, ":troop_no"),
		], "So there you are.  It is a shame you couldn't make it out this way for the games.  I would have enjoyed the chance to cross swords with you.", "lord_talk", 
		[
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(quest_get_slot, ":town_lord", "qst_floris_active_tournament", slot_quest_giver_troop),
				(call_script, "script_troop_change_relation_with_troop", "trp_player", ":town_lord", -1),
			(try_end),
		]],
		
    [anyone,"lord_start",
		[
			(check_quest_active, "qst_floris_active_tournament"),
			(quest_get_slot, ":troop_no", "qst_floris_active_tournament", slot_quest_giver_troop),
			(eq, "$g_talk_troop", ":troop_no"),
			(quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_participated_in_tournament),
			(str_store_troop_name, s21, ":troop_no"),
		], "It was an honor to have you among the participants for our games.", "lord_talk", 
		[
			(call_script, "script_quest_floris_active_tournament", floris_quest_succeed),
		]],
		
	[anyone,"start",
		[
			(check_quest_active, "qst_floris_active_tournament"),
			(quest_get_slot, ":troop_no", "qst_floris_active_tournament", slot_quest_giver_troop),
			(quest_get_slot, ":center_no", "qst_floris_active_tournament", slot_quest_target_center),
			(eq, ":center_no", "$current_town"),
			(store_conversation_troop, "$g_talk_troop"),
			(is_between, "$g_talk_troop", arena_masters_begin, arena_masters_end),
			(quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_participated_in_tournament),
			(party_count_members_of_type, reg1, ":center_no", ":troop_no"),
			(lt, reg1, 1), # hosting lord isn't in town.
			(str_store_troop_name, s21, ":troop_no"),
		], "It was an honor to have you among the participants for our games.  {s21} will be most pleased you were able to make it.", "close_window", 
		[
			(call_script, "script_quest_floris_active_tournament", floris_quest_succeed),
		]],
	
	[anyone,"start",
		[
			(check_quest_active, "qst_floris_active_tournament"),
			(quest_get_slot, ":troop_no", "qst_floris_active_tournament", slot_quest_giver_troop),
			(quest_get_slot, ":center_no", "qst_floris_active_tournament", slot_quest_giver_center),
			(eq, ":center_no", "$current_town"),
			(store_conversation_troop, "$g_talk_troop"),
			(is_between, "$g_talk_troop", arena_masters_begin, arena_masters_end),
			(quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_participated_in_tournament),
			(str_store_troop_name, s21, ":troop_no"),
		], "It was an honor to have you among the participants for our games, but you should speak with {s21} as he will be most pleased by your attendance.", "close_window", 
		[]],
	##### QUEST : FLORIS_ACTIVE_TOURNAMENT : END #####
]

from util_common import *
from util_wrappers import *

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
		var_name_1 = "dialogs"
		orig_dialogs = var_set[var_name_1]
		orig_dialogs.extend(dialogs)
		pos = FindDialog_i(orig_dialogs, anyone,"lord_start")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, lord_talk_addon)
		##ORIG_DIALOGS is a list, can use OpBlockWrapper and other list operations.
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)