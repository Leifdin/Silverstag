# Quest Pack 3 (1.0) by Windyplains

from header_common import *
from header_dialogs import *
from header_operations import *
from header_parties import *
from header_item_modifiers import *
from header_skills import *
from header_triggers import *
from ID_troops import *
from ID_party_templates import *
from module_constants import *

####################################################################################################################
# During a dialog, the dialog lines are scanned from top to bottom.
# If the dialog-line is spoken by the player, all the matching lines are displayed for the player to pick from.
# If the dialog-line is spoken by another, the first (top-most) matching line is selected.
#
#  Each dialog line contains the following fields:
# 1) Dialogue partner: This should match the person player is talking to.
#    Usually this is a troop-id.
#    You can also use a party-template-id by appending '|party_tpl' to this field.
#    Use the constant 'anyone' if you'd like the line to match anybody.
#    Appending '|plyr' to this field means that the actual line is spoken by the player
#    Appending '|other(troop_id)' means that this line is spoken by a third person on the scene.
#       (You must make sure that this third person is present on the scene)
#
# 2) Starting dialog-state:
#    During a dialog there's always an active Dialog-state.
#    A dialog-line's starting dialog state must be the same as the active dialog state, for the line to be a possible candidate.
#    If the dialog is started by meeting a party on the map, initially, the active dialog state is "start"
#    If the dialog is started by speaking to an NPC in a town, initially, the active dialog state is "start"
#    If the dialog is started by helping a party defeat another party, initially, the active dialog state is "party_relieved"
#    If the dialog is started by liberating a prisoner, initially, the active dialog state is "prisoner_liberated"
#    If the dialog is started by defeating a party led by a hero, initially, the active dialog state is "enemy_defeated"
#    If the dialog is started by a trigger, initially, the active dialog state is "event_triggered"
# 3) Conditions block (list): This must be a valid operation block. See header_operations.py for reference.
# 4) Dialog Text (string):
# 5) Ending dialog-state:
#    If a dialog line is picked, the active dialog-state will become the picked line's ending dialog-state.
# 6) Consequences block (list): This must be a valid operation block. See header_operations.py for reference.
# 7) Voice-over (string): sound filename for the voice over. Leave here empty for no voice over
####################################################################################################################

dialogs	= [   

]

quest_dialogs	= [   
	##### QUEST : SUMMONED_TO_HALL : BEGIN #####
	# A messenger joins your party to talk about you needing to return to your keep.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", qp3_actor_messenger),
			(neg|check_quest_active, "qst_summoned_to_hall"),
		], "M'{Lord/Lady}, excuse me my interruption, but I was told to seek you out.", "qp3_messenger_1", 
		[]],
	
	# # Default capture for the messenger.
	# [anyone, "event_triggered", 
		# [
			# (eq, "$g_talk_troop", qp3_actor_messenger),
			# (neg|check_quest_active, "qst_summoned_to_hall"),
			# #(eq, "$npc_map_talk_context", "qst_patrol_for_bandits"),
			# (quest_slot_eq, "qst_summoned_to_hall", slot_quest_current_state, qp3_summoned_inactive),
		# ], "M'{Lord/Lady}, excuse me my interruption, but I was told to seek you out.", "qp3_messenger_1", 
		# []],
	
	[anyone|plyr, "qp3_messenger_1", 
		[], "Yes, what is it?", "qp3_messenger_2", 
		[]],
	
	[anyone, "qp3_messenger_2", 
		[
			(quest_get_slot, ":center_no", "qst_summoned_to_hall", slot_quest_giver_center),
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(str_store_troop_name, s12, ":castle_steward"),
			(str_store_party_name, s13, ":center_no"),
			(troop_get_type, reg21, ":castle_steward"),
		], "Your pardon m'{Lord/Lady}.  I was sent by {reg21?Lady:Lord} {s12}, Steward of {s13}, to request your presence for a matter of some importance.", "qp3_messenger_3", 
		[]],
	
	[anyone|plyr, "qp3_messenger_3", 
		[], "I see.  Ride back and make the steward aware of my impending arrival.", "qp3_messenger_4", 
		[
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_begin),
		]],
	
	[anyone|plyr, "qp3_messenger_3", 
		[
			(quest_get_slot, ":center_no", "qst_summoned_to_hall", slot_quest_giver_center),
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(str_store_troop_name, s12, ":castle_steward"),
		], "Tell {s12} that I do not have time to return home for now.", "qp3_messenger_4", 
		[
			(quest_set_slot, "qst_summoned_to_hall", slot_quest_dont_give_again_remaining_days,  10),
			# Change town reputation.
			(quest_get_slot, ":quest_center", "qst_summoned_to_hall", slot_quest_giver_center),
			(party_get_slot, ":castle_steward", ":quest_center", slot_center_steward),
			(try_begin),
				(assign, ":relation_hit", -1),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(val_add, ":relation_hit", -1),
			(try_end),
			(call_script, "script_change_player_relation_with_center", ":quest_center", ":relation_hit"),
			(call_script, "script_change_player_relation_with_troop", ":castle_steward", ":relation_hit", 0),
		]],
	
	[anyone, "qp3_messenger_4", 
		[
			(quest_get_slot, ":center_no", "qst_summoned_to_hall", slot_quest_giver_center),
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(str_store_troop_name, s12, ":castle_steward"),
			(troop_get_type, reg21, ":castle_steward"),
		], "Very good, m'{Lord/Lady}.  I will make {reg21?Lady:Lord} {s12} aware of your answer immediately.", "close_window", 
		[
			# Remove messenger from party.
			(party_remove_members, "p_main_party", qp3_actor_messenger, 1),
		]],
	
	# The castle steward responds to your arrival.
	[anyone, "start", 
		[
			(check_quest_active, "qst_summoned_to_hall"),
			(store_conversation_troop, "$g_talk_troop"),
			(quest_slot_eq, "qst_summoned_to_hall", slot_quest_giver_center, "$current_town"),
			(party_slot_eq, "$current_town", slot_center_steward, "$g_talk_troop"),
			(quest_slot_eq, "qst_summoned_to_hall", slot_quest_current_state, qp3_summoned_summoned_to_fief),
		], "I see you received my message.  It is good to see you, m'{Lord/Lady}.  I apologize for diverting you from your travels, but a matter of some importance has emerged.", "qp3_steward_1", 
		[]],
	
	[anyone|plyr, "qp3_steward_1", 
		[], "I came as soon as word reached me.  What is this problem you spoke of?", "qp3_steward_2", 
		[]],
	
	##### QUEST ( patrol_for_bandits ) BEGIN
	[anyone, "qp3_steward_2", 
		[
			(quest_slot_eq, "qst_summoned_to_hall", slot_quest_temp_slot, "qst_patrol_for_bandits"),
			#(eq, "$npc_map_talk_context", "qst_patrol_for_bandits"),
		], "Bandits have been disrupting our trade routes into the town, m'{Lord/Lady}.  I have sent patrols, but we do not have enough men to spare.  I was hoping your army would have better luck thinning their numbers.", "qp3_steward_issue_bandits", 
		[
			(call_script, "script_common_quest_change_state", "qst_summoned_to_hall", qp3_summoned_problem_explained),
			(call_script, "script_qp3_quest_patrol_for_bandits", floris_quest_begin),
			(quest_get_slot, ":center_no", "qst_summoned_to_hall", slot_quest_giver_center),
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(call_script, "script_change_player_relation_with_troop", ":castle_steward", 2, 0),
		]],
	
	[anyone|plyr, "qp3_steward_issue_bandits", 
		[], "Rest assured the bandits will be on the run soon enough.", "close_window", 
		[
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_succeed),
		]],
	
	[anyone|plyr, "qp3_steward_issue_bandits", 
		[], "I can't spare the men or time for this at the moment.", "close_window", 
		[
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_succeed), # Success even if you don't agree to help.  Just don't get next quest.
			(call_script, "script_qp3_quest_patrol_for_bandits", floris_quest_fail),
		]],
	##### QUEST ( patrol_for_bandits ) END
	
	##### QUEST ( destroy_the_lair ) BEGIN
	[anyone, "qp3_steward_2", 
		[
			(quest_slot_eq, "qst_summoned_to_hall", slot_quest_temp_slot, "qst_destroy_the_lair"),
			#(eq, "$npc_map_talk_context", "qst_destroy_the_lair"),
		], "M'{Lord/Lady}, there have been reports of bandits raiding farms all across the countryside.  These raids are coordinated and they always manage to evade the men I've sent.  I suspect the bandits have a hideout nearby that must be destroyed, but I cannot spare the men to search for it and still protect lands vital to feeding our city.", "qp3_steward_issue_bandit_lair", 
		[
			(call_script, "script_common_quest_change_state", "qst_summoned_to_hall", qp3_summoned_problem_explained),
			(call_script, "script_qp3_quest_destroy_the_lair", floris_quest_begin),
			(quest_get_slot, ":center_no", "qst_summoned_to_hall", slot_quest_giver_center),
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(call_script, "script_change_player_relation_with_troop", ":castle_steward", 2, 0),
		]],
	
	[anyone|plyr, "qp3_steward_issue_bandit_lair", 
		[], "I see.  Keep your men at their posts.  My army will root the bandits out.", "close_window", 
		[
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_succeed),
		]],
	
	[anyone|plyr, "qp3_steward_issue_bandit_lair", 
		[], "I can't spare the men right now.  You'll have to make do on your own.", "close_window", 
		[
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_succeed), # Success even if you don't agree to help.  Just don't get next quest.
			(call_script, "script_qp3_quest_destroy_the_lair", floris_quest_fail),
		]],
	##### QUEST ( destroy_the_lair ) END
	
	##### QUEST ( mercs_for_hire ) BEGIN
	[anyone, "qp3_steward_2", 
		[
			(quest_slot_eq, "qst_summoned_to_hall", slot_quest_temp_slot, "qst_mercs_for_hire"),
			#(eq, "$npc_map_talk_context", "qst_mercs_for_hire"),
		], "A sizable force of mercenaries have camped themselves not far from our keep.  They fly a flag of truce and have requested an audience with you, m'{Lord/Lady}.  What word should I send them?", "qp3_steward_issue_mercenaries", 
		[
			(call_script, "script_common_quest_change_state", "qst_summoned_to_hall", qp3_summoned_problem_explained),
		]],
	
	[anyone|plyr, "qp3_steward_issue_mercenaries", 
		[], "Send for their commander to meet me here.", "qp3_steward_issue_mercenaries_end", 
		[
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_succeed),
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_begin),
			(quest_get_slot, ":center_no", "qst_summoned_to_hall", slot_quest_giver_center),
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(call_script, "script_change_player_relation_with_troop", ":castle_steward", 2, 0),
		]],
	
	[anyone|plyr, "qp3_steward_issue_mercenaries", 
		[], "Send them word they are to leave my lands at once.", "qp3_steward_issue_mercenaries_end", 
		[
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_succeed), # Success even if you don't agree to help.  Just don't get next quest.
		]],
	
	[anyone, "qp3_steward_issue_mercenaries_end", 
		[], "I will send word at once, m'{Lord/Lady}.", "close_window", 
		[]],
	##### QUEST ( mercs_for_hire ) END
	
	##### QUEST ( escort_to_mine ) BEGIN
	[anyone, "qp3_steward_2", 
		[
			(quest_slot_eq, "qst_summoned_to_hall", slot_quest_temp_slot, "qst_escort_to_mine"),
			#(eq, "$npc_map_talk_context", "qst_escort_to_mine"),
		], "M'{Lord/Lady}, our dungeons are crowded beyond our capacity.  I fear that pestilence may spread if we keep this many prisoners on hand for too long.  We should consider selling prisoners of no political value to the salt mines, however, I cannot spare enough men from the garrison to ensure their safe arrival.  Would you escort them, m'{lord/lady}?", "qp3_steward_issue_prisoner_escort", 
		[
			(call_script, "script_common_quest_change_state", "qst_summoned_to_hall", qp3_summoned_problem_explained),
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_succeed),
		]],
	
	[anyone|plyr, "qp3_steward_issue_prisoner_escort", 
		[], "You know my feelings on slavery.  These prisoners will not be sold.", "close_window", 
		[
			(quest_set_slot, "qst_escort_to_mine", slot_quest_dont_give_again_remaining_days, 30),
			(call_script, "script_change_player_honor", 1),
		]],
		
	
	[anyone|plyr, "qp3_steward_issue_prisoner_escort", 
		[], "Spare what men you can and I shall accompany their party to the mines.", "close_window", 
		[
			(call_script, "script_qp3_quest_escort_to_mine", floris_quest_begin),
			(quest_get_slot, ":center_no", "qst_summoned_to_hall", slot_quest_giver_center),
			(party_get_slot, ":castle_steward", ":center_no", slot_center_steward),
			(call_script, "script_change_player_relation_with_troop", ":castle_steward", 2, 0),
		]],
	
	[anyone|plyr, "qp3_steward_issue_prisoner_escort", 
		[], "You will have to make do.  I cannot spare the men or time to transport prisoners.", "qp3_steward_issue_prisoner_escort_2", 
		[
			(quest_set_slot, "qst_escort_to_mine", slot_quest_dont_give_again_remaining_days, 10),
		]],
		
	[anyone, "qp3_steward_issue_prisoner_escort_2", 
		[
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_generate_escort_cost, -1, "$current_town"),
		], "Understandable, m'{Lord/Lady}.  We could comission local mercenaries to accomplish the task for {reg51} denars if you wish?  This would run the risk of them falling afoul of bandits or simply running off with our money, but I will try to find reliable men.", "qp3_steward_issue_prisoner_escort_3", 
		[]],
		
	[anyone|plyr, "qp3_steward_issue_prisoner_escort_3", 
		[], "Very well.  Make the arrangements.", "close_window", 
		[
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_create, 0, "$current_town"),
			(assign, ":caravan", reg51),
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_generate_escort_cost, ":caravan", "$current_town"), # Since no player escort is available figure out escort price.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_add_escort_troops, ":caravan", reg51),              # Add in extra escort troops.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_load_from_center, ":caravan", "$current_town"),     # Move prisoners from town to new party.
			(call_script, "script_common_prisoner_caravan_function", prisoner_caravan_direct_to_destination, ":caravan", "p_salt_mine"),  # Set party AI
		]],
		
	[anyone|plyr, "qp3_steward_issue_prisoner_escort_3", 
		[], "Nonsense.  I will take care of our prisoners when I am ready.", "close_window", 
		[]],
		
	
	##### QUEST ( escort_to_mine ) END
	
	# Last default option which shouldn't be seen.
	[anyone, "qp3_steward_2", 
		[
			(quest_get_slot, reg31, "qst_summoned_to_hall", slot_quest_temp_slot),
			#(assign, reg31, "$npc_map_talk_context"),
		], "Oh, I just thought it'd be fun to have you come all this way for nothing.  Please don't behead me?^^This text shouldn't be seen.  Failed slot_quest_temp_slot = {reg31}.", "close_window", 
		[
			(call_script, "script_qp3_quest_summoned_to_hall", floris_quest_cancel),
		]],
	
	##### QUEST : SUMMONED_TO_HALL : END #####
	
	##### QUEST : MERCS_FOR_HIRE : BEGIN #####
	# Keep conversation while contract is active, but not due.
	[anyone, "start", 
		[
			(check_quest_active, "qst_mercs_for_hire"),
			(store_conversation_troop, "$g_talk_troop"),
			(eq, "$g_talk_troop", qp3_actor_mercenary_leader),
			(this_or_next|quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_active_contract),
			(this_or_next|quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_agree_to_renew),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_refused_to_renew),
		], "My men are busy training in the courtyard and we'll be ready to move as soon as you need us, M'{Lord/Lady}.", "close_window", 
		[(assign, "$g_leave_encounter",1)]],
	
	# Contract is nearly expired when conversation began within your keep.
	[anyone, "start", 
		[
			(check_quest_active, "qst_mercs_for_hire"),
			(store_conversation_troop, "$g_talk_troop"),
			(eq, "$g_talk_troop", qp3_actor_mercenary_leader),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_contract_due),
		], "There is something I wish to discuss with you, m'{Lord/Lady}.  If you have the time?", "qp3_mercs_rehire_1", 
		[]],
	
	# Answer to the meeting began for hiring the mercenary party.
	[anyone, "start", 
		[
			(check_quest_active, "qst_mercs_for_hire"),
			(store_conversation_troop, "$g_talk_troop"),
			(party_slot_eq, "$current_town", slot_center_steward, "$g_talk_troop"),
			#(eq, "$g_talk_troop", qp3_actor_minister),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_begun),
			(str_store_troop_name, s2, qp3_actor_mercenary_leader),
			(quest_get_slot, ":merc_title", "qst_mercs_for_hire", slot_quest_merc_leader_title),
			(str_store_string, s3, ":merc_title"),
			(quest_get_slot, ":merc_band", "qst_mercs_for_hire", slot_quest_merc_band_name),
			(str_store_string, s4, ":merc_band"),
		], "M'{Lord/Lady}, may I introduce you to {s2}, {s3} of the {s4}.", "qp3_mercs_for_hire_1", 
		[]],
	
	[anyone, "start", 
		[
			(check_quest_active, "qst_mercs_for_hire"),
			(store_conversation_troop, "$g_talk_troop"),
			(eq, "$g_talk_troop", qp3_actor_mercenary_leader),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_begun),
			(str_store_troop_name, s2, qp3_actor_mercenary_leader),
			(quest_get_slot, ":merc_title", "qst_mercs_for_hire", slot_quest_merc_leader_title),
			(str_store_string, s3, ":merc_title"),
			(quest_get_slot, ":merc_band", "qst_mercs_for_hire", slot_quest_merc_band_name),
			(str_store_string, s4, ":merc_band"),
		], "An honor to meet you, m'{Lord/Lady}.  I am {s2}, {s3} of the {s4}.  Forgive my intrusion into your lands, but my band is looking for employment and I hear you may be interested.", "qp3_mercs_for_hire_2", 
		[]],
	
	[anyone, "qp3_mercs_for_hire_1", 
		[], "An honor to meet you, m'{Lord/Lady}.  Forgive my intrusion into your lands, but my band is looking for employment and I hear you may be interested.", "qp3_mercs_for_hire_2", 
		[(set_conversation_speaker_troop, qp3_actor_mercenary_leader),]],
	
	[anyone|plyr, "qp3_mercs_for_hire_2", 
		[], "That depends on how many men you've got and what it will cost me.", "qp3_mercs_for_hire_3", 
		[]],
	
	[anyone|plyr, "qp3_mercs_for_hire_2", 
		[], "You heard wrong.  I do not need any additional men.", "close_window", 
		[
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_cancel),
		]],
	
	[anyone, "qp3_mercs_for_hire_3", 
		[
			(quest_get_slot, reg31, "qst_mercs_for_hire", slot_quest_merc_band_ideal_size),
			(quest_get_slot, reg32, "qst_mercs_for_hire", slot_quest_target_amount),
		], "I currently have {reg31} able men at my disposal, but our band is always recruiting new members as we travel.  We would expect {reg32} denars in payment each week for our services.  A better offer I do not believe you will find.", "qp3_mercs_for_hire_4", 
		[(set_conversation_speaker_troop, qp3_actor_mercenary_leader),]],
	
	[anyone|plyr, "qp3_mercs_for_hire_4", 
		[
			(store_mul, reg33, reg32, 80),
			(val_div, reg33, 100),
		], "For only {reg31} men I would expect to pay no more than {reg33} denars!", "qp3_mercs_for_hire_5", 
		[]],
	
	[anyone, "qp3_mercs_for_hire_5", 
		[], "My {Lord/Lady}, I trust as an experienced soldier you know the value of well trained men as I do.  My price stands.  Perhaps one of your rivals may recognize the value of my service.", "qp3_mercs_for_hire_6", 
		[(set_conversation_speaker_troop, qp3_actor_mercenary_leader),]],
	
	[anyone|plyr, "qp3_mercs_for_hire_6", 
		[], "Very well, I will accept your contract at {reg32} denars.", "qp3_mercs_for_hire_7", 
		[]],
	
	[anyone|plyr, "qp3_mercs_for_hire_6", 
		[], "I will not pay such a price for farmers holding swords!  We're done here.", "close_window", 
		[
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_cancel),
		]],
	
	[anyone, "qp3_mercs_for_hire_7", 
		[], "Very good, m'{Lord/Lady}.  I shall ready my men and await your orders.", "close_window", 
		[
			(set_conversation_speaker_troop, qp3_actor_mercenary_leader),
			(call_script, "script_common_quest_change_state", "qst_mercs_for_hire", qp3_mercs_for_hire_active_contract),
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_update),
			(call_script, "script_qp3_quest_mercenary_function", mercs_generate_party),
			(call_script, "script_qp3_quest_mercenary_function", mercs_set_behavior_to_follow),
		]],
	
	# Contract is nearly expired.
	[anyone, "event_triggered", 
		[
			(check_quest_active, "qst_mercs_for_hire"),
			(eq, "$g_talk_troop", qp3_actor_mercenary_leader),
			(eq, "$npc_map_talk_context", qp3_mercs_for_hire_active_contract),
			(quest_slot_eq, "qst_mercs_for_hire", slot_quest_current_state, qp3_mercs_for_hire_active_contract),
		], "There is something I wish to discuss with you, m'{Lord/Lady}.  If you have the time?", "qp3_mercs_rehire_1", 
		[]],
	
	[anyone|plyr, "qp3_mercs_rehire_1", 
		[], "Very well.  What is it?", "qp3_mercs_rehire_2", 
		[
			(call_script, "script_common_quest_change_state", "qst_mercs_for_hire", qp3_mercs_for_hire_contract_due), # prevent repeats.
		]],
	
	[anyone|plyr, "qp3_mercs_rehire_1", 
		[], "I do not have time for this right now.", "close_window", 
		[(assign, "$g_leave_encounter",1)]],
	
	[anyone, "qp3_mercs_rehire_2", 
		[
			(quest_get_slot, reg31, "qst_mercs_for_hire", slot_quest_expiration_days),
		], "Our contract is going to expire in the next {reg31} days and I would like to know your intentions on renewing it for another month or not?", "qp3_mercs_rehire_3", 
		[
			(assign, reg51, 0), # Setup for persuasion attempt on a discount.
		]],
	
	[anyone|plyr, "qp3_mercs_rehire_3", 
		[], "Your men have proven their worth.  I would like to continue our agreement.", "qp3_mercs_rehire_4", 
		[]],
	
	[anyone|plyr, "qp3_mercs_rehire_3", 
		[], "I plan parting ways once this contract expires.", "close_window", 
		[
			(call_script, "script_common_quest_change_state", "qst_mercs_for_hire", qp3_mercs_for_hire_refused_to_renew),
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_succeed),
			(call_script, "script_qp3_quest_mercenary_function", mercs_destroy_party),
			(call_script, "script_common_quest_change_state", "qst_mercs_for_hire", qp3_mercs_for_hire_inactive),
			(assign, "$g_leave_encounter",1),
		]],
	
	[anyone, "qp3_mercs_rehire_4", 
		[
			(call_script, "script_qp3_quest_mercenary_function", mercs_remove_non_mercenaries),
			(call_script, "script_qp3_quest_mercenary_function", mercs_generate_contract_cost),
			(quest_get_slot, reg31, "qst_mercs_for_hire", slot_quest_target_amount),
		], "Very well, m'{Lord/Lady}.  I have had a number of expenses to contend with while on the road with you.  Fresh recruits to replace the dead, stipends for the families of the fallen, supplies and the usual trivalties of war.  I ask our wage for this next contract be {reg31} denars per week.  Is this agreeable?", "qp3_mercs_rehire_5", 
		[]],
	
	[anyone|plyr, "qp3_mercs_rehire_5", 
		[], "I understand the costs all too well.  Very well {reg31} denars it is.", "close_window", 
		[
			(call_script, "script_qp3_quest_mercenary_function", mercs_contract_renew),
			(assign, "$g_leave_encounter",1),
		]],
	
	[anyone|plyr, "qp3_mercs_rehire_5", 
		[
			(eq, reg51, 0),
			(store_skill_level, ":persuasion", "trp_player", "skl_persuasion"),
			(ge, ":persuasion", 2),
			(store_mul, reg21, reg31, 85), # 15% discount attempt.
			(val_div, reg21, 100),
		], "I'll give you {reg21} denars.  I have costs of my own to deal with. (Persuade)", "qp3_mercs_rehire_6", 
		[
			(try_begin),
				(call_script, "script_cf_common_quest_persuasion_check", "trp_player", qp3_actor_mercenary_leader, CHECK_DC_VERY_EASY), # Not a lord so an easier DC is necessary.
				(assign, reg50, 1), # Success
			(else_try),
				(assign, reg50, 0), # Failure
			(try_end),
			(assign, reg51, 1), # don't reattempt.
		]],
	
	[anyone|plyr, "qp3_mercs_rehire_5", 
		[], "Agreeable? I thought you were mercenaries, not bandits.  My answer is no.", "close_window", 
		[
			(call_script, "script_common_quest_change_state", "qst_mercs_for_hire", qp3_mercs_for_hire_refused_to_renew),
			(call_script, "script_qp3_quest_mercs_for_hire", floris_quest_succeed),
			(call_script, "script_qp3_quest_mercenary_function", mercs_destroy_party),
			(call_script, "script_common_quest_change_state", "qst_mercs_for_hire", qp3_mercs_for_hire_inactive),
			(assign, "$g_leave_encounter",1),
		]],
	
	[anyone, "qp3_mercs_rehire_6", 
		[
			(eq, reg50, 1), # Successful attempt.
			(quest_set_slot, "qst_mercs_for_hire", slot_quest_target_amount, reg21),
		], "Generally I make it a habit not to haggle over the value of my men as they prove their worth on the battlefield, but service with you hasn't been unagreeable.  Very well, {reg21} denars it is.", "close_window", 
		[
			(call_script, "script_qp3_quest_mercenary_function", mercs_contract_renew),
			(assign, "$g_leave_encounter",1),
		]],
	
	[anyone, "qp3_mercs_rehire_6", 
		[
			(eq, reg50, 0), # Failed attempt.
			(quest_get_slot, reg31, "qst_mercs_for_hire", slot_quest_target_amount),
		], "My men prove their worth with their blood on the battlefield.  If you will not honor them with what they are worth then I will find employment elsewhere.  My price stands at {reg31} denars.", "qp3_mercs_rehire_5", 
		[]],
	
	
	##### QUEST : MERCS_FOR_HIRE : END #####
	
]

# companion_talk_addon	= [   
	
# ]

# village_elder_talk_addon	= [   

# ]

# lord_talk_addon	= [   
	
# ]

from util_common import *
from util_wrappers import *

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
		var_name_1 = "dialogs"
		orig_dialogs = var_set[var_name_1]
		orig_dialogs.extend(dialogs)
        # Insert Lord Dialog
		# pos = FindDialog_i(orig_dialogs, anyone,"lord_start")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, lord_talk_addon)
		# Insert Companion Pretalk Dialog
		pos = FindDialog_i(orig_dialogs, anyone,"start")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, quest_dialogs)
		# Insert Companion Dialog
		# pos = FindDialog_i(orig_dialogs, anyone|plyr, "companion_recruit_backstory_response")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, companion_talk_addon)
		# Insert Village Elder Dialog
		# pos = FindDialog_i(orig_dialogs, anyone,"village_elder_deliver_cattle_thank")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, village_elder_talk_addon)
		
		##ORIG_DIALOGS is a list, can use OpBlockWrapper and other list operations.
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)