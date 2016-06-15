# Quest Pack 4 (1.0) by Windyplains

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

actor_dialog	= [   

	##### QUEST : EDWYN_SECOND_KNIGHT : BEGIN #####
	# We confront Sir Henric in the streets of a town.
	[anyone, "start", 
		[
			(eq, "$g_talk_troop", qp4_actor_named_knight),
			(eq, "$npc_map_talk_context", "qst_edwyn_second_knight"),
			(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_arrived_in_town),
			(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance, "$current_town"),
		], "Eh?  What do you want?", "edwyn_town_fight_1", 
		[
			(call_script, "script_common_quest_change_state", "qst_edwyn_second_knight", qp4_edwyn_second_knight_confrontation),
		]],
	
	[anyone|plyr, "edwyn_town_fight_1", 
		[
		], "Your head on the end of a pike would be a nice start.", "edwyn_town_fight_2", 
		[]],
	
	[anyone, "edwyn_town_fight_2", 
		[], "Oh yeah?  Let's fight!", "close_window", 
		[ 
			(assign, "$timer_active", 1), # Begins combat.
		]],
	
	##### QUEST : EDWYN_SECOND_KNIGHT : END #####

]
companion_pretalk_addon	= [   
	##### QUEST : ODVAL_RETURN_TO_TULBUK : BEGIN #####
	[anyone, "member_chat", 
		[
			(store_conversation_troop, "$g_talk_troop"),
			(eq, "$g_talk_troop", NPC_Odval),
			(quest_slot_eq, "qst_odval_return_to_tulbuk", slot_quest_current_state, qp4_odval_return_to_tulbuk_odval_joined_party),
			(quest_slot_eq, "qst_odval_return_to_tulbuk", slot_quest_comment_made, 0),
			(str_store_party_name, s13, qp4_odval_home_town),
		], "I hope for my sake you are right about returning to {s13}, but with you at my side I will see it through.", "member_talk", 
		[(quest_set_slot, "qst_odval_return_to_tulbuk", slot_quest_comment_made, 1),]],
	##### QUEST : ODVAL_RETURN_TO_TULBUK : END #####
	
	##### QUEST : ODVAL_ACCEPT_THE_CHALLENGE : BEGIN #####
	[anyone, "member_chat", 
		[
			(store_conversation_troop, "$g_talk_troop"),
			(eq, "$g_talk_troop", NPC_Odval),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_accepted),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_comment_made, 0),
		], "I am honored to have you fighting by my side.  Those sheep-brained farmers will not stand a chance against us.", "member_talk", 
		[(quest_set_slot, "qst_odval_accept_the_challenge", slot_quest_comment_made, 1),]],
	
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, "$npc_map_talk_context", qp4_odval_redemption_return_to_tulbuk_done),
			(quest_slot_eq, "qst_odval_redemption", slot_quest_current_state, qp4_odval_redemption_return_to_tulbuk_done),
			(quest_slot_eq, "qst_odval_redemption", slot_quest_comment_made, 0),
			(str_store_party_name, s13, qp4_odval_home_town),
		], "Our opponents are probably ready for us back in {s13} by now.", "close_window", 
		[
			(quest_set_slot, "qst_odval_redemption", slot_quest_comment_made, 1),
		]],
	
	##### QUEST : ODVAL_ACCEPT_THE_CHALLENGE : END #####
	
	##### QUEST : ODVAL_SAVING_FACE : BEGIN #####
	[anyone, "member_chat", 
		[
			(store_conversation_troop, "$g_talk_troop"),
			(eq, "$g_talk_troop", NPC_Odval),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_accepted),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_comment_made, 0),
			(str_store_party_name, s13, qp4_odval_home_town),
		], "When we face off in {s13} I will finally have a chance to see what you are made of, pretty {boy/girl}!", "member_talk", 
		[(quest_set_slot, "qst_odval_saving_face", slot_quest_comment_made, 1),]],
	
	##### QUEST : ODVAL_SAVING_FACE : END #####
	
	##### QUEST : ODVAL_REDEMPTION : BEGIN #####
	# Odval's redemption succeeds (generic)
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, "$npc_map_talk_context", slot_troop_intro_quest_complete),
			(check_quest_succeeded, "qst_odval_redemption"),
			(quest_slot_eq, "qst_odval_redemption", slot_quest_comment_made, 0),
			(call_script, "script_qp4_odval_store_final_comment_to_s2"),
		], "{s2}", "close_window", 
		[
			(quest_set_slot, "qst_odval_redemption", slot_quest_comment_made, 1),
			(complete_quest, "qst_odval_redemption"),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Odval, reg52),
		]],
	
	# Odval's redemption fails (generic)
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, "$npc_map_talk_context", slot_troop_intro_quest_complete),
			(check_quest_failed, "qst_odval_redemption"),
			(quest_slot_eq, "qst_odval_redemption", slot_quest_comment_made, 0),
			(call_script, "script_qp4_odval_store_final_comment_to_s2"),
		], "{s2}", "close_window", 
		[
			(quest_set_slot, "qst_odval_redemption", slot_quest_comment_made, 1),
			(complete_quest, "qst_odval_redemption"),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Odval, reg52),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_storyline_failure),
		]],
		
	# Odval's redemption debug default.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, "$npc_map_talk_context", slot_troop_intro_quest_complete),
			(quest_slot_eq, "qst_odval_redemption", slot_quest_comment_made, 0),
			(call_script, "script_qp4_odval_store_final_comment_to_s2"),
		], "{s2}", "close_window", 
		[
			(quest_set_slot, "qst_odval_redemption", slot_quest_comment_made, 1),
		]],
	
	# Odval is worried that odval_redemption is about to expire so is warning the player in advance.
	[anyone, "event_triggered",
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, "$npc_map_talk_context", slot_troop_story_arc_quest),
			(quest_slot_eq, "qst_odval_return_to_tulbuk", slot_quest_current_state, qp4_odval_return_to_tulbuk_odval_joined_party),
			(str_store_party_name, s13, qp4_odval_home_town),
		], "I know it isn't my place to say where our band goes, but when I joined you promised to help me clear things up in {s13}.  I am hoping you still plan on seeing that through.", "close_window", 
		[]],
	
	# Odval is worried that odval_redemption is about to expire so is warning the player in advance.
	[anyone, "event_triggered",
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, "$npc_map_talk_context", slot_troop_story_arc_quest),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_accepted),
			(str_store_party_name, s13, qp4_odval_home_town),
		], "We had best get back to {s13} soon or the elder will think we aren't showing up for the fight.", "close_window", 
		[]],
	
	# Odval is worried that odval_redemption is about to expire so is warning the player in advance. (Special case for odval_saving_face's shorter duration).
	[anyone, "event_triggered",
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, "$npc_map_talk_context", slot_troop_story_arc_quest),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_accepted),
			#(neg|quest_slot_ge, "qst_odval_saving_face", slot_quest_expiration_days, 4),
			(str_store_party_name, s13, qp4_odval_home_town),
		], "I just wanted to remind you that we're expected back in {s13} before much longer.", "close_window", 
		[]],
	##### QUEST : ODVAL_REDEMPTION : END #####
	
	##### QUEST : EDWYN_FIRST_KNIGHT : BEGIN #####
	# We've got a first lead on Sir Tenry's location.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_quest_stage_1_trigger_chance),
			(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_current_state, qp4_edwyn_first_begun),
			(quest_get_slot, ":target_center", "qst_edwyn_first_knight", slot_quest_stage_1_trigger_chance),
			(str_clear, s17),
			(str_store_party_name, s12, "$current_town"),
			(str_store_party_name, s17, ":target_center"),
			(call_script, "script_qp4_store_informant_to_s2"),
			
		], "Captain, back in {s12}, I learned from a {s2} that a knight matching Sir Tenry's description was tossed out of their order.  I didn't even know folks could be unknighted.  Something about stealing from the order.  I guess even they figured out what a treacherous bastard he was.  The {s2} didn't know his exact whereabouts, but mentioned rumor has it Tenry took up banditry in the area around {s17}.  We should head that way and see what we can find.", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_first_knight", slot_quest_comment_made, 1),
			(call_script, "script_common_quest_change_state", "qst_edwyn_first_knight", qp4_edwyn_first_learn_about_knight),
			(call_script, "script_qp4_quest_edwyn_first_knight", floris_quest_update),
		]],
	
	# We went to the area described and it seems someone has heard of a bandit lair near center X that might be what we are looking for.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_quest_stage_2_trigger_chance),
			(quest_slot_eq, "qst_edwyn_first_knight", slot_quest_current_state, qp4_edwyn_first_learn_about_knight),
			(quest_get_slot, ":target_center", "qst_edwyn_first_knight", slot_quest_stage_2_trigger_chance),
			(str_clear, s12),
			(str_clear, s17),
			(str_store_party_name, s12, "$current_town"),
			(str_store_party_name, s17, ":target_center"),
			(call_script, "script_qp4_store_informant_to_s2"),
			
		], "I didn't see any sign of Sir Tenry back in {s12}, but a {s2} did mention there is increased bandit activity up by {s17}.  There is almost sure to be a lair nearby.", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_first_knight", slot_quest_comment_made, 1),
			(call_script, "script_common_quest_change_state", "qst_edwyn_first_knight", qp4_edwyn_first_learn_of_lair_location),
			(call_script, "script_qp4_quest_edwyn_first_knight", floris_quest_update),
			# Create Bandit Lair
			(quest_get_slot, ":target_center", "qst_edwyn_first_knight", slot_quest_stage_2_trigger_chance),
			(set_spawn_radius, 4),
			(spawn_around_party, ":target_center", "pt_steppe_bandit_lair"),
			(party_set_flags, reg0, pf_always_visible, 0),
			(quest_set_slot, "qst_edwyn_first_knight", slot_quest_target_party, reg0),
		]],
	##### QUEST : EDWYN_FIRST_KNIGHT : END #####
	
	##### QUEST : EDWYN_SECOND_KNIGHT : BEGIN #####
	# We've got a first lead on Sir Henric's location.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_quest_stage_1_trigger_chance),
			(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_begun),
			(quest_get_slot, ":target_center", "qst_edwyn_second_knight", slot_quest_stage_1_trigger_chance),
			(str_clear, s17),
			(str_store_party_name, s12, "$current_town"),
			(str_store_party_name, s17, ":target_center"),
			(call_script, "script_qp4_store_informant_to_s2"),
			
		], "One of the {s2}s I spoke to back in {s12} said he's seen a knight that matches Sir Henric's description, but that it was a month ago.  He said based on the direction he was traveling he may have been on his way towards {s17}.", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_second_knight", slot_quest_comment_made, 1),
			(call_script, "script_common_quest_change_state", "qst_edwyn_second_knight", qp4_edwyn_second_learn_of_location),
			(call_script, "script_qp4_quest_edwyn_second_knight", floris_quest_update),
		]],
	
	# We arrived in center X only to find we missed Sir Henric by two weeks.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_quest_stage_2_trigger_chance),
			(quest_slot_eq, "qst_edwyn_second_knight", slot_quest_current_state, qp4_edwyn_second_learn_of_location),
			(quest_get_slot, ":target_center", "qst_edwyn_second_knight", slot_quest_stage_2_trigger_chance),
			(str_clear, s12),
			(str_clear, s17),
			(str_store_party_name, s12, "$current_town"),
			(str_store_party_name, s17, ":target_center"),
			(call_script, "script_qp4_store_informant_to_s2"),
			
		], "Seems we were too slow to catch Sir Henric in {s12}, Captain, but a {s2} did see him passing through a couple of weeks past.  Believes he's on his way towards {s17}.", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_second_knight", slot_quest_comment_made, 1),
			(call_script, "script_common_quest_change_state", "qst_edwyn_second_knight", qp4_edwyn_second_just_missed_him),
			(call_script, "script_qp4_quest_edwyn_second_knight", floris_quest_update),
		]],
		
	##### QUEST : EDWYN_SECOND_KNIGHT : END #####
	
	##### QUEST : EDWYN_THIRD_KNIGHT : BEGIN #####
	# We've got a first lead on Sir Gerrin's location.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_quest_stage_1_trigger_chance),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_begun),
			(quest_get_slot, ":target_center", "qst_edwyn_third_knight", slot_quest_stage_1_trigger_chance),
			(str_clear, s17),
			(str_store_party_name, s12, "$current_town"),
			(str_store_party_name, s17, ":target_center"),
			#(call_script, "script_qp4_store_informant_to_s2"),
			
		], "Captain, while speaking to a trader back in {s12} he mentioned he'd heard the name Sir Gerrin before when he was last in {s17}.  He couldn't be much more specific than that, but I think it is worth checking out.", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_third_knight", slot_quest_comment_made, 1),
			(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_last_seen_location),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
		]],
	
	# We arrived in the town, but just missed Sir Gerrin.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_quest_stage_2_trigger_chance),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_last_seen_location),
			(quest_get_slot, ":target_center", "qst_edwyn_third_knight", slot_quest_stage_2_trigger_chance),
			(str_clear, s17),
			(str_store_party_name, s12, "$current_town"),
			(str_store_party_name, s17, ":target_center"),
			(call_script, "script_qp4_store_informant_to_s2"),
			
		], "Seems no one in the town knows of a Sir Gerrin, but a {s2} did mention that she's heard of some fellas that might be knights visiting down in {s17}.  Maybe it is worth a look, Captain.", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_third_knight", slot_quest_comment_made, 1),
			(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_not_here_check_nearby_village),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
		]],
	##### QUEST : EDWYN_THIRD_KNIGHT : END #####
	
	##### QUEST : EDWYN_REVENGE : BEGIN #####
	# Edwyn's revenge succeeds.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_troop_intro_quest_complete),
			(check_quest_succeeded, "qst_edwyn_revenge"),
			(quest_slot_eq, "qst_edwyn_revenge", slot_quest_comment_made, 0),
			(call_script, "script_qp4_edwyn_store_final_comment_to_s2"),
			
		], "{s2}", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_comment_made, 1),
			(complete_quest, "qst_edwyn_revenge"),
		]],
	
	# Edwyn's revenge fails.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_troop_intro_quest_complete),
			(check_quest_failed, "qst_edwyn_revenge"),
			(quest_slot_eq, "qst_edwyn_revenge", slot_quest_comment_made, 0),
			(call_script, "script_qp4_edwyn_store_final_comment_to_s2"),
			
		], "{s2}", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_comment_made, 1),
			(complete_quest, "qst_edwyn_revenge"),
			(call_script, "script_troop_change_relation_with_troop", "trp_player", NPC_Edwyn, reg52),
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_storyline_failure),
		]],
		
	# Edwyn's revenge debug default.
	[anyone, "event_triggered", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, "$npc_map_talk_context", slot_troop_intro_quest_complete),
			(quest_slot_eq, "qst_edwyn_revenge", slot_quest_comment_made, 0),
			(call_script, "script_qp4_edwyn_store_final_comment_to_s2"),
			
		], "{s2}", "close_window", 
		[
			(quest_set_slot, "qst_edwyn_revenge", slot_quest_comment_made, 1),
		]],
	##### QUEST : EDWYN_REVENGE : END #####
]

companion_talk_addon	= [   
	##### QUEST : ODVAL_INTRO : BEGIN #####
	# Initial background story quest hook.
	[anyone|plyr, "companion_recruit_backstory_response", 
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, qp4_odval_storyarc_enabled, 1),
			(quest_slot_eq, "qst_odval_intro", slot_quest_current_state, qp4_odval_intro_inactive),
		], "Ever thought of trying to clear your name?", "odval_intro_1", 
		[
			(call_script, "script_qp4_quest_odval_intro", floris_quest_begin),
			(call_script, "script_common_quest_change_state", "qst_odval_intro", qp4_odval_intro_story_heard),
			(call_script, "script_qp4_quest_odval_intro", floris_quest_update),
		]],
	
	# Secondary attempt to recruit Nissa if you had a full party before.
	[anyone|plyr, "companion_recruit_secondchance", 
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, qp4_odval_storyarc_enabled, 1),
			(quest_slot_eq, "qst_odval_intro", slot_quest_current_state, qp4_odval_intro_agreed_to_help),
		], "Still interested in returning home to clear your name?", "odval_intro_1", []],
	
	# Give the player a chance to spark the introduction quest even if they didn't upon initial hiring.
	[anyone|plyr, "member_question_2", 
		[
			(eq, "$g_talk_troop", NPC_Odval),
			(eq, qp4_odval_storyarc_enabled, 1),
			(quest_slot_eq, "qst_odval_intro", slot_quest_current_state, qp4_odval_intro_inactive),
		], "Ever thought of trying to clear your name?", "odval_intro_3", 
		[
			(call_script, "script_qp4_quest_odval_intro", floris_quest_begin),
			(call_script, "script_common_quest_change_state", "qst_odval_intro", qp4_odval_intro_story_heard),
			(call_script, "script_qp4_quest_odval_intro", floris_quest_update),
		]],
		
	[anyone, "odval_intro_1", 
		[], "Clear my name?  I would likely find myself out numbered and at the end of a sword if I tried, but perhaps if I had allies to help me it might be worth the attempt.  What do you say, pretty {boy/girl}?", "odval_intro_2", []],
		
	[anyone|plyr, "odval_intro_2", 
		[], "Join my company and I'll help you clear your name.", "odval_intro_3", 
		[
			(call_script, "script_common_quest_change_state", "qst_odval_intro", qp4_odval_intro_agreed_to_help),
			(call_script, "script_qp4_quest_odval_intro", floris_quest_update),
		]],
		
	[anyone|plyr, "odval_intro_2", 
		[], "I wasn't volunteering to clear your name for you!", "odval_intro_4", 
		[
			(call_script, "script_common_quest_change_state", "qst_odval_intro", qp4_odval_intro_refused_to_help),
			(call_script, "script_qp4_quest_odval_intro", floris_quest_update),
		]],
		
	[anyone, "odval_intro_3", # QUEST SUCCESS PATH
		[
			(party_get_free_companions_capacity, reg1, "p_main_party"),
			(ge, reg1, 1), # The party has room.
		], "You'd help a stranger so?  Clear my name, pretty {boy/lady}, and I'll follow under your banner in any battle.  Just let me get my things.", "close_window", 
		[
			(call_script, "script_qp4_quest_odval_intro", floris_quest_succeed),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_begin),
			(call_script, "script_qp4_quest_odval_return_to_tulbuk", floris_quest_begin),
		]],
		
	[anyone, "odval_intro_3", # You don't have room for her to join the party.
		[
			(party_get_free_companions_capacity, reg1, "p_main_party"),
			(lt, reg1, 1), # No room.
		], "You'd help a stranger so?  It would be an honor, but you do not appear to have room left for me to join your warband.", "close_window", 
		[]],
		
	[anyone, "odval_intro_4", # QUEST FAILURE PATH
		[
			(troop_get_type, reg3, NPC_Odval),
		], "So you're all talk then?  Or is it that you'd enjoy watching a stranger get lynched for something {reg3?she:he} didn't do?  Get out of my sight, milk drinker!", "close_window", 
		[
			(call_script, "script_qp4_quest_odval_intro", floris_quest_fail),
		]],
    ##### QUEST : ODVAL_INTRO : END #####
	
	##### QUEST : EDWYN_INTRO : BEGIN #####
	# Initial background story quest hook.
	[anyone|plyr, "companion_recruit_backstory_response", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, qp4_edwyn_storyarc_enabled, 1),
			(quest_slot_eq, "qst_edwyn_intro", slot_quest_current_state, qp4_edwyn_intro_inactive),
		], "Ever thought of getting even?", "edwyn_intro_1", 
		[
			(call_script, "script_qp4_quest_edwyn_intro", floris_quest_begin),
			(call_script, "script_common_quest_change_state", "qst_edwyn_intro", qp4_edwyn_intro_story_heard),
			(call_script, "script_qp4_quest_edwyn_intro", floris_quest_update),
		]],
	
	# Give the player a chance to spark the introduction quest even if they didn't upon initial hiring.
	[anyone|plyr, "member_question_2", 
		[
			(eq, "$g_talk_troop", NPC_Edwyn),
			(eq, qp4_edwyn_storyarc_enabled, 1),
			(quest_slot_eq, "qst_edwyn_intro", slot_quest_current_state, qp4_edwyn_intro_inactive),
		], "Ever thought of getting even?", "edwyn_intro_1", 
		[
			(call_script, "script_qp4_quest_edwyn_intro", floris_quest_begin),
			(call_script, "script_common_quest_change_state", "qst_edwyn_intro", qp4_edwyn_intro_story_heard),
			(call_script, "script_qp4_quest_edwyn_intro", floris_quest_update),
		]],
		
	[anyone, "edwyn_intro_1", 
		[], "Avenge my family?  Against a band of trained knights?  Are you mad?", "edwyn_intro_2", []],
		
	[anyone|plyr, "edwyn_intro_2", 
		[], "Join my company and I'll help you kill them all.", "edwyn_intro_3", 
		[
			(call_script, "script_common_quest_change_state", "qst_edwyn_intro", qp4_edwyn_intro_agreed_to_help),
			(call_script, "script_qp4_quest_edwyn_intro", floris_quest_update),
		]],
		
	[anyone|plyr, "edwyn_intro_2", 
		[], "I wasn't volunteering to go on a murdering rampage!", "edwyn_intro_4", 
		[
			(call_script, "script_common_quest_change_state", "qst_edwyn_intro", qp4_edwyn_intro_refused_to_help),
			(call_script, "script_qp4_quest_edwyn_intro", floris_quest_update),
		]],
		
	[anyone, "edwyn_intro_3", # QUEST SUCCESS PATH
		[], "You're going to help me kill them all?  Great.", "close_window", 
		[
			(call_script, "script_qp4_quest_edwyn_intro", floris_quest_succeed),
			(call_script, "script_qp4_quest_edwyn_revenge", floris_quest_begin),
			(call_script, "script_qp4_quest_edwyn_first_knight", floris_quest_begin),
			(call_script, "script_qp4_quest_edwyn_second_knight", floris_quest_begin),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_begin),
		]],
		
	[anyone, "edwyn_intro_4", # QUEST FAILURE PATH
		[
			(troop_get_type, reg3, NPC_Edwyn),
		], "You're not going to help?  To hell with you then.", "close_window", 
		[
			(call_script, "script_qp4_quest_edwyn_intro", floris_quest_fail),
		]],
    ##### QUEST : EDWYN_INTRO : END #####
]

village_elder_talk_addon	= [   
	##### QUEST : ODVAL_RETURN_TO_TULBUK : BEGIN #####
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_return_to_tulbuk"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_return_to_tulbuk", slot_quest_current_state, qp4_odval_return_to_tulbuk_odval_joined_party),
			(str_store_troop_name, s14, NPC_Odval),
		], "{s14}?  You dare show your face in these parts after your treachery in the games?  Be gone before you find yourself tied to a pole and beaten as an example for the children!", "odval_return_1", 
		[]],
	
	[anyone|plyr, "odval_return_1", 
		[], "Care to try that threat on me, peasant?", "odval_return_2", 
		[]],
	
	[anyone, "odval_return_2", 
		[
			(str_store_troop_name, s14, NPC_Odval),
		], "*{s14} glances sharply at you before turning to the elder*^^Elder, please this is all a misunderstanding.  I have come back to speak on my behalf.", "odval_return_3", 
		[(set_conversation_speaker_troop, NPC_Odval),]],
	
	[anyone|plyr, "odval_return_1", 
		[
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
		], "{s14} has returned with me to address these charges against {reg3?her:him}.  {reg3?She:He} has been a loyal warrior in my army and I'll not have its honor stained.", "odval_return_3", 
		[]],
	
	[anyone, "odval_return_3", 
		[
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
		], "I see.  {s14}, your leaving does not speak well on your behalf.  Two of your fellow competitors have come forward to speak against you as well as one of the judges.  This judge claims {reg3?he:she} may have given you information {reg3?he:she} should not have during a moment of indescretion.  Is this true?", "odval_return_4", 
		[]],
	
	[anyone, "odval_return_4", 
		[
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
		], "*{s14} grins sheepishly*^^Perhaps the {reg3?man:lady}'s tongue wagged a little and {reg3?his:her} mind wasn't where it belonged, but this is no proof that I cheated.  I beat those men in fair contest and I can do it again.", "odval_return_5", 
		[(set_conversation_speaker_troop, NPC_Odval),]],
	
	[anyone, "odval_return_5", 
		[], "So you say, but it will take more than words to convince these men.", "odval_return_6", []],
	
	[anyone, "odval_return_6", 
		[], "Very well, Elder.  I invoke the right to contest.  I shall clear my name with their blood and once I am done with them no one will dare speak ill of my honor!", "odval_return_7", 
		[(set_conversation_speaker_troop, NPC_Odval),]],
	
	[anyone, "odval_return_7", [], "You shall have your fight, but a match of one against three is hardly fair.  Or did your friend come along to stand by you for this very purpose?  You should know stranger that men have died in these challenges.", "odval_return_8", 
		[(assign, reg2, 0),]],
	
	[anyone|plyr, "odval_return_8", 
		[
			(store_skill_level, ":persuasion", skl_persuasion, "trp_player"),
			(ge, ":persuasion", 2),
			(eq, reg2, 0),
		], "Surely we can work something out without coming to blows? (Bribe)", "odval_return_9", 
		[
			(store_skill_level, ":persuasion", skl_persuasion, "trp_player"),
			(val_mul, ":persuasion", 7),
			(val_add, ":persuasion", 15),
			(store_random_in_range, reg2, 0, 100),
			(try_begin),
				(le, reg2, ":persuasion"),
				(assign, reg1, 1),
			(else_try),
				(assign, reg1, 0),
			(try_end),
			(assign, reg2, 1),
		]],
	
	[anyone|plyr, "odval_return_8", 
		[], "If you want me to break a few peasant necks then I accept the challenge.", "odval_return_accept", 
		[
			(call_script, "script_common_quest_change_state", "qst_odval_return_to_tulbuk", qp4_odval_return_to_tulbuk_accepted_challenge),
			(call_script, "script_qp4_quest_odval_return_to_tulbuk", floris_quest_update),
		]],
	
	[anyone|plyr, "odval_return_8", 
		[
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
		], "I think {s14} can manage on {reg3?her:his} own.", "odval_return_refuse", 
		[
			(call_script, "script_common_quest_change_state", "qst_odval_return_to_tulbuk", qp4_odval_return_to_tulbuk_refused_challenge),
			(call_script, "script_qp4_quest_odval_return_to_tulbuk", floris_quest_update),
			(call_script, "script_qp4_quest_odval_return_to_tulbuk", floris_quest_fail),
		]],
	
	[anyone, "odval_return_9", 
		[(eq, reg1, 1),], "What did you have in mind?", "odval_return_10", []],
	
	[anyone, "odval_return_9", 
		[
			(neq, reg1, 1),
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
		], "No.  Only a contest of arms will prove {s14}'s worth.  Do you think us so easily bribed?  So does that mean you will not stand with {reg3?her:him}?", "odval_return_8", []],
	
	[anyone|plyr, "odval_return_10", 
		[
			(store_troop_gold, ":gold", "trp_player"),
			(ge, ":gold", 5000),
		], "I was just thinking the village could use a new stable.  (5,000 denars)", "odval_return_11", 
		[]],
	
	[anyone|plyr, "odval_return_10", 
		[], "Nevermind.  About that challenge...", "odval_return_8", []],
	
	[anyone, "odval_return_11", 
		[
			(str_store_troop_name, s14, NPC_Odval),
		], "Now that you mention it I think the village could indeed do with such.  Never can have enough space for fine horses.  With such honorable friends as you I am sure we can look past {s14}'s past activities.", "close_window", 
		[
			(call_script, "script_common_quest_change_state", "qst_odval_return_to_tulbuk", qp4_odval_return_to_tulbuk_accepted_challenge),
			(call_script, "script_qp4_quest_odval_return_to_tulbuk", floris_quest_succeed),
			(call_script, "script_common_quest_change_state", "qst_odval_redemption", qp4_odval_redemption_return_to_tulbuk_done),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_succeed),
			(troop_remove_gold, "trp_player", 5000),
		]],
	
	
	[anyone, "odval_return_accept", 
		[], "That's the spirit, pretty {boy/girl}!  We'll show those dung chewers how real warriors fight.", "close_window", 
		[
			(set_conversation_speaker_troop, NPC_Odval),
			(call_script, "script_qp4_quest_odval_return_to_tulbuk", floris_quest_succeed),
			(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_begin),
			(quest_set_slot, "qst_odval_accept_the_challenge", slot_quest_target_amount, qp4_odval_accept_the_challenge_wait_period),
		]],
	
	[anyone, "odval_return_refuse", 
		[], "You goat-faced, dung chewing coward!  Too spineless to stand by your word?  Fine, I'll face these louts alone.", "close_window", 
		[(set_conversation_speaker_troop, NPC_Odval),]],
	##### QUEST : ODVAL_RETURN_TO_TULBUK : END #####
	
	##### QUEST : ODVAL_ACCEPT_THE_CHALLENGE : BEGIN #####
	# Odval reminds the player it is time to return to Tulbuk.
	# [anyone, "event_triggered", 
		# [
			# (display_message, "@The right script is being triggered."),
			# (eq, "$g_talk_troop", NPC_Odval),
			# (display_message, "@You're talking to NPC_Odval."),
			# (eq, "$npc_map_talk_context", slot_troop_add_to_scene),
			# (display_message, "@You're talking about the right context."),
			# (check_quest_active, "qst_odval_accept_the_challenge"),
			# (display_message, "@Accept the challenge quest is active."),
			# (str_store_party_name, s13, qp4_odval_home_town),
		# ], "I think we should head back to {s13} to see if the elder is ready.  I'm anxious to get this over with.", "close_window", 
		# []],
	
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_accept_the_challenge"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_accepted),
		], "I have not had a chance to inform the others of the challenge yet.  Come back in a day or two and all should be ready.", "village_elder_pretalk", 
		[]],
	
	# Odval & Player have returned.  Everyone is ready for the challenge to begin.
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_accept_the_challenge"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_begun),
			(eq, "$fight_timer", 0),
			(str_store_troop_name, s14, NPC_Odval),
		], "{s14}, you have demanded the right of contest to clear your name against accusations of deceit.  There is no sure way to know which party here speaks the truth, but let it be known that whichever group that falls will be considered the deceitful party.", "odval_challenge_beginning_1", 
		[]],
	
	[anyone, "odval_challenge_beginning_1", 
		[
			(str_store_troop_name, s14, NPC_Odval),
		], "{s14}, are you and your companion ready to begin?", "odval_challenge_beginning_2", 
		[]],
	
	[anyone, "odval_challenge_beginning_2", 
		[], "We are elder.", "odval_challenge_beginning_3", 
		[(set_conversation_speaker_troop, NPC_Odval),]],
	
	[anyone, "odval_challenge_beginning_3", 
		[
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
			(str_store_string, s1, "str_qp4_odval_betrayed_judge_male"),
			(str_store_string, s2, "str_qp4_odval_betrayed_judge_female"),
			(str_store_string, s3, "str_qp4_odval_second_place_finisher"),
			(str_store_string, s4, "str_qp4_odval_third_place_finisher"),
		], "{reg3?{s1}:{s2}}, you claim {s14} learned of how to cheat from you.  This is as much a contest for regaining your honor as {reg3?hers:his}.  {s3} and {s4}, the two of you tied for placement behind {s14} and feel {reg3?she:he} has cheated you from your rightful recognition.  Are the three of you ready?", "odval_challenge_beginning_4", 
		[]],
	
	[anyone, "odval_challenge_beginning_4", 
		[
			(troop_get_type, reg3, NPC_Odval),
		], "We are ready, honored elder.  We will not let this {reg3?woman:man} disgrace our village without challenge.", "odval_challenge_beginning_5", 
		[(set_conversation_speaker_troop, qp4_actor_townsfolk),]],
	
	[anyone, "odval_challenge_beginning_5", 
		[
			(str_store_troop_name, s14, NPC_Odval),
		], "Very well.  Begin!", "close_window", 
		[
			(assign, "$timer_active", 1), # Start our timer.
		]],
	
	
	# Odval & Player have won the fight against Odval's accusers.
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_accept_the_challenge"),
			(main_party_has_troop, NPC_Odval),
			# (neg|troop_is_wounded, NPC_Odval),
			(assign, ":continue", 0),
			(try_for_agents, ":agent_no"),
				(agent_get_troop_id, ":troop_no", ":agent_no"),
				(eq, ":troop_no", NPC_Odval),
				(agent_is_alive, ":agent_no"),
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_won),
			(str_store_troop_name, s14, NPC_Odval),
		], "You have done well {s14}, but while your fight played out I heard a number of our villagers questioning how well you might have faired if not for your companion's help.", "odval_challenge_won_1", 
		[(assign, "$timer_active", 3),]],
	
	# Odval & Player have won the fight against Odval's accusers, but Odval was knocked out.
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_accept_the_challenge"),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_odval_fell),
			(str_store_troop_name, s14, NPC_Odval),
		], "Well {s14}, if that was your way of proving yourself a great warrior then you have failed.  You on the other hand handled yourself quite well.  Were it not for you {s14} may not have survived.  I think it best if the two of you go.", "odval_challenge_won_sort_of_1", 
		[(assign, "$timer_active", 3),]],
	
	[anyone|plyr, "odval_challenge_won_sort_of_1", 
		[
			(store_skill_level, ":persuasion", skl_persuasion, "trp_player"),
			(ge, ":persuasion", 3),
		], "Even the best warriors can fall in combat. (Persuade)", "odval_challenge_won_sort_of_2",
		[
			(store_skill_level, ":persuasion", skl_persuasion, "trp_player"),
			(val_mul, ":persuasion", 7),
			(val_add, ":persuasion", 20),
			(store_random_in_range, reg2, 0, 100),
			(try_begin),
				(le, reg2, ":persuasion"),
				(assign, reg1, 1),
			(else_try),
				(assign, reg1, 0),
			(try_end),
		]],
	
	[anyone|plyr, "odval_challenge_won_sort_of_1", 
		[], "And you believe you could have done better?", "odval_challenge_won_sort_of_3",
		[]],
	
	[anyone, "odval_challenge_won_sort_of_2", 
		[
			(eq, reg1, 1), # Successful persuasion attempt.
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
		], "You make a wise argument.  {s14} has done well in choosing the captain {reg3?she:he} follows.  Not everyone would agree with your assessment though.  It would be best if you two left.", "close_window",
		[
			(call_script, "script_common_quest_change_state", "qst_odval_accept_the_challenge", qp4_odval_accept_the_challenge_odval_fell_but_okay),
			(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_update),
			(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_succeed),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH), # 3 successful quests required.
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_fail),
			(else_try),
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_succeed), # 2 of 2 required quests passed.
			(try_end),
			(finish_mission, 4),
			(change_screen_map),
		]],
	
	[anyone, "odval_challenge_won_sort_of_2", 
		[
			(neq, reg1, 1), # Failed persuasion attempt.
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
		], "Perhaps, stranger, but I am not claiming the title 'Champion of {s13}' either.  Now it is time you were on your way and take {reg3?her:him} with you.", "odval_challenge_won_sort_of_4",
		[]],
	
	[anyone, "odval_challenge_won_sort_of_3", 
		[], "Perhaps, stranger, but I am not claiming the title 'Champion of {s13}' either.  Now it is time you two left.", "odval_challenge_won_sort_of_4",
		[]],
	
	[anyone|plyr, "odval_challenge_won_sort_of_4", 
		[], "Very well, but you have made a great mistake this day.", "close_window",
		[
			(call_script, "script_common_quest_change_state", "qst_odval_accept_the_challenge", qp4_odval_accept_the_challenge_odval_fell_not_okay),
			(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_update),
			(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_fail),
			(finish_mission, 4),
			(change_screen_map),
		]],
	
	[anyone, "odval_challenge_won_1", 
		[
			(main_party_has_troop, NPC_Odval),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_won),
			(str_store_party_name, s13, qp4_odval_home_town),
		], "We win and yet still you all question my ability?  Will nothing satisfy this lot or is it that you cannot live with the fact that I AM the greatest warrior {s13} has ever known!", "odval_challenge_won_2", 
		[(set_conversation_speaker_troop, NPC_Odval),]],
	
	[anyone|plyr, "odval_challenge_won_2", 
		[
			(str_store_troop_name, s14, NPC_Odval),
		], "Perhaps that could easily be solved.", "odval_challenge_won_3", 
		[]],
	
	[anyone, "odval_challenge_won_3", 
		[], "What did you have in mind, {playername}?", "odval_challenge_won_4", 
		[]],
		
	[anyone|plyr, "odval_challenge_won_4", 
		[
			(str_store_troop_name, s14, NPC_Odval),
			(troop_get_type, reg3, NPC_Odval),
		], "If the crowd doubts {s14}'s ability because of my presence then perhaps a fight between {reg3?her:him} and I will settle that matter.", "odval_challenge_won_5", 
		[]],
	
	[anyone, "odval_challenge_won_5", 
		[
			(main_party_has_troop, NPC_Odval),
		], "I always enjoy a good fight, but so soon?  I wouldn't mind the chance to teach you a lesson or two, but it would not seem fair if I did not give you time to prepare.", "odval_challenge_won_6", 
		[(set_conversation_speaker_troop, NPC_Odval),]],
	
	[anyone, "odval_challenge_won_6", 
		[
			(main_party_has_troop, NPC_Odval),
		], "Then we will allow for up to five days to let each of you rest.  Are you both in agreement of these terms?", "odval_challenge_won_7", 
		[]],
	
	[anyone|plyr, "odval_challenge_won_7", 
		[], "Yes, I agree to the terms.", "odval_challenge_won_8", 
		[]],
	
	[anyone|plyr, "odval_challenge_won_7", 
		[], "No, I don't have time for this kind of distraction.", "odval_challenge_won_9", 
		[]],
	
	# You agreed to fight Odval.
	[anyone, "odval_challenge_won_8", 
		[
			(main_party_has_troop, NPC_Odval),
		], "Agreed.  Rest well for when next we meet here I will teach you the ways of a real warrior.", "close_window", 
		[
			(set_conversation_speaker_troop, NPC_Odval),
			(call_script, "script_common_quest_change_state", "qst_odval_accept_the_challenge", qp4_odval_accept_the_challenge_challenge_complete),
			(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_succeed),
			(call_script, "script_qp4_quest_odval_saving_face", floris_quest_begin),
			(quest_set_slot, "qst_odval_saving_face", slot_quest_target_amount, qp4_odval_saving_face_wait_period),
		]],
	
	# You refused to fight Odval.
	[anyone, "odval_challenge_won_9", 
		[
			(main_party_has_troop, NPC_Odval),
		], "Scared?  You should be.  I have nothing left to prove to these people.  If you will not accept my victory was by my own skill then I shall have nothing more to do with this place.", "close_window", 
		[
			(set_conversation_speaker_troop, NPC_Odval),
			(call_script, "script_common_quest_change_state", "qst_odval_accept_the_challenge", qp4_odval_accept_the_challenge_challenge_complete),
			(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_succeed),
			(try_begin),
				(ge, "$quest_reactions", QUEST_REACTIONS_HIGH), # 3 successful quests required.
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_fail),
			(else_try),
				(call_script, "script_qp4_quest_odval_redemption", floris_quest_succeed), # 2 of 2 required quests passed.
			(try_end),
			(finish_mission, 4),
			(change_screen_map),
		]],
	
	# Odval & Player have lost the fight against Odval's accusers.
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_accept_the_challenge"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_accept_the_challenge", slot_quest_current_state, qp4_odval_accept_the_challenge_challenge_lost),
			(str_store_party_name, s13, qp4_odval_home_town),
			(str_store_troop_name, s14, NPC_Odval),
		], "{s14}, you have failed to defeat your accusers and I have no choice but to believe their account of your deceit.  You have been stripped of your victory and shall never be allowed to set foot in {s13} again!  Now leave our village.", "close_window", 
		[
			(call_script, "script_qp4_quest_odval_accept_the_challenge", floris_quest_fail),
			(assign, "$timer_active", 3),
			(finish_mission, 4),
			(change_screen_map),
		]],
	
	##### QUEST : ODVAL_ACCEPT_THE_CHALLENGE : END #####
	
	##### QUEST : ODVAL_SAVING_FACE : BEGIN #####
	# Odval reminds the player it is time to return to Tulbuk.
	# [anyone, "event_triggered", 
		# [
			# (eq, "$g_talk_troop", NPC_Odval),
			# (eq, "$npc_map_talk_context", slot_troop_add_to_scene),
			# (check_quest_active, "qst_odval_saving_face"),
			# (str_store_party_name, s13, qp4_odval_home_town),
		# ], "Well, I'm rested up enough if you are.  I'm looking forward to a chance to cross swords with you so we should head back to {s13}.", "close_window", 
		# []],
	
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_saving_face"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_accepted),
			(str_store_troop_name, s14, NPC_Odval),
		], "I respect what you are trying to do for {s14}, but I hope you are doing it for the right reasons.", "village_elder_pretalk", 
		[]],
	
	# Odval & Player have returned.  Everyone is ready for the challenge to begin.
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_saving_face"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_begun),
			(eq, "$fight_timer", 0),
			(str_store_troop_name, s14, NPC_Odval),
		], "{playername} and {s14}, I trust that you are both ready to begin?", "odval_saving_face_1", 
		[]],
	
	[anyone, "odval_saving_face_1", 
		[], "This shouldn't be necessary, but if you all need to see two warriors beat one another down for your entertainment then so be it.", "odval_saving_face_2", 
		[(set_conversation_speaker_troop, NPC_Odval),]],
	
	[anyone|plyr, "odval_saving_face_2", 
		[], "Let's just get this over with.", "close_window", 
		[
			(assign, "$timer_active", 1), # Start our timer.
		]],
	
	# You defeat Odval
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_saving_face"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_won),
			(str_store_party_name, s13, qp4_odval_home_town),
			(str_store_troop_name, s14, NPC_Odval),
		], "I'm sorry to see that your companion has proven the misgivings the folks of {s13} have of you, {s14}.", "close_window", 
		[
			(call_script, "script_qp4_quest_odval_saving_face", floris_quest_fail),
			(assign, "$timer_active", 3),
			(finish_mission, 4),
			(change_screen_map),
		]],
	
	# Odval defeated you, but you didn't even harm her.
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_saving_face"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_lost),
			(eq, reg56, 0),
			(str_store_troop_name, s14, NPC_Odval),
		], "Do you think everyone here is a fool, {s14}?  Your 'friend' did not even defend {himself/herself} against you.  We may be simple folk, but we are not stupid.  If you must even now resort to cheating in order to win then you were certainly guilty before.  Get out of our sight!", "close_window", 
		[
			(call_script, "script_qp4_quest_odval_saving_face", floris_quest_fail),
			(assign, "$timer_active", 3),
			(finish_mission, 4),
			(change_screen_map),
		]],
	
	# Odval defeated you.
	[anyone, "start", 
		[
			(check_quest_active, "qst_odval_saving_face"),
			(main_party_has_troop, NPC_Odval),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(eq, "$current_town", qp4_odval_home_town),
			(quest_slot_eq, "qst_odval_saving_face", slot_quest_current_state, qp4_odval_saving_face_challenge_lost),
			(neq, reg56, 0),
			(str_store_party_name, s13, qp4_odval_home_town),
			(str_store_troop_name, s14, NPC_Odval),
		], "Impressive performance, {s14}.  It seems we were wrong about you.", "close_window", 
		[
			(call_script, "script_qp4_quest_odval_saving_face", floris_quest_succeed),
			(call_script, "script_qp4_quest_odval_redemption", floris_quest_succeed), # 3 of 3 required quests passed.
			(assign, "$timer_active", 3),
			(finish_mission, 4),
			(change_screen_map),
		]],
	##### QUEST : ODVAL_SAVING_FACE : END #####
	
	##### QUEST : EDWYN_THIRD_KNIGHT : BEGIN #####
	# Village elder is first spoken to about Sir Gerrin's description.
	[anyone, "start", 
		[
			(check_quest_active, "qst_edwyn_third_knight"),
			(main_party_has_troop, NPC_Edwyn),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_arrival_in_village),
		], "Welcome to our humble home, my {lord/lady}.  How may I serve you?", "edwyn_third_inquiry_1", 
		[]],
	
	[anyone, "edwyn_third_inquiry_1", 
		[
			(main_party_has_troop, NPC_Edwyn),
		], "We're looking for a knight by the name of Sir Gerrin.  I heard that he is often seen here in the village?", "edwyn_third_inquiry_2", 
		[(set_conversation_speaker_troop, NPC_Edwyn),]],
	
	[anyone, "edwyn_third_inquiry_2", 
		[], "Yes, I know of him.  What business do you have with him?", "edwyn_third_inquiry_3", 
		[]],
	
	[anyone, "edwyn_third_inquiry_3", 
		[
			(main_party_has_troop, NPC_Edwyn),
		], "I intend to kill him.", "edwyn_third_inquiry_4", 
		[(set_conversation_speaker_troop, NPC_Edwyn),]],
	
	[anyone, "edwyn_third_inquiry_4", 
		[], "What?  Surely you jest, good sir.  He comes here with a sizable force and I cannot have that kind of bloodshed here in the village.", "edwyn_third_inquiry_5", 
		[]],
	
	[anyone, "edwyn_third_inquiry_5", 
		[
			(main_party_has_troop, NPC_Edwyn),
		], "Nope, still intend to kill him.  I really do hate him after all.", "edwyn_third_inquiry_6", 
		[(set_conversation_speaker_troop, NPC_Edwyn),]],
	
	[anyone, "edwyn_third_inquiry_6", 
		[], "Are you sure?  This would really make life difficult for us.  He'll come back and kill us and stuff.  Please reconsider?", "edwyn_third_inquiry_7", 
		[
			(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_learned_story_from_elder),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
		]],
	
	[anyone|plyr, "edwyn_third_inquiry_7", 
		[], "Edwyn, for the greater good we should let Sir Gerrin live.", "edwyn_third_inquiry_9", 
		[
			(assign, reg56, 0),
			(store_random_in_range, ":roll", 0, 100),
			(try_begin),
				(lt, ":roll", 15),
				(assign, reg56, 1),
			(try_end),
		]],
	
	[anyone|plyr, "edwyn_third_inquiry_7", 
		[], "Nope.  Edwyn's right.  He needs to die.", "edwyn_third_inquiry_8", 
		[]],
	
	[anyone, "edwyn_third_inquiry_8", 
		[], "Aw shucks.  Gerrin should be back in a day or so.  You guys suck.", "close_window", 
		[
			(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_planning_to_kill_knight),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
		]],
	
	[anyone, "edwyn_third_inquiry_9", 
		[
			(main_party_has_troop, NPC_Edwyn),
			(eq, reg56, 1),
		], "Oh, all right.  Fighting tires me out anyway.", "close_window", 
		[
			(set_conversation_speaker_troop, NPC_Edwyn),
			(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_convinced_edwyn_to_spare_knight),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_succeed),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
		]],
	
	[anyone, "edwyn_third_inquiry_9", 
		[
			(main_party_has_troop, NPC_Edwyn),
			(eq, reg56, 0),
		], "Screw that.  I'm fairly set on killing him.  Are you going to help?", "edwyn_third_inquiry_10", 
		[(set_conversation_speaker_troop, NPC_Edwyn),]],
	
	[anyone|plyr, "edwyn_third_inquiry_10", 
		[], "Very well.  We'll kill him together.", "close_window", 
		[
			(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_planning_to_kill_knight),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
		]],
	
	[anyone|plyr, "edwyn_third_inquiry_10", 
		[], "Screw that.  I'll be busy washing my hair or something.", "close_window", 
		[
			(call_script, "script_common_quest_change_state", "qst_edwyn_third_knight", qp4_edwyn_third_allowed_knight_to_live),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_fail),
			(call_script, "script_qp4_quest_edwyn_third_knight", floris_quest_update),
		]],
	
	# Village elder is upset at you for having killed the knights.
	[anyone, "start", 
		[
			(check_quest_active, "qst_edwyn_third_knight"),
			(main_party_has_troop, NPC_Edwyn),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_knight_is_slain),
		], "What have you done?!  Even our own villagers have bloodied their hands in this.  We could have found another way.  Now they're sure to blame our village, but I am sure that is not your problem!", "close_window", 
		[
			(finish_mission, 4),
			(change_screen_map),
			(jump_to_menu, "mnu_village"),
		]],
	
	# Village elder is upset at you for having tried and failed to kill the knights.
	[anyone, "start", 
		[
			(check_quest_active, "qst_edwyn_third_knight"),
			(is_between,"$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_edwyn_third_knight", slot_quest_current_state, qp4_edwyn_third_knight_lives_on),
		], "Have you any idea what you fools have done?!  Our own villagers have involved themselves in this.  Those men will be back and with a larger force to raze our homes to the ground!", "close_window", 
		[
			(finish_mission, 4),
			(change_screen_map),
			(jump_to_menu, "mnu_village"),
		]],
	##### QUEST : EDWYN_THIRD_KNIGHT : END #####
]

lord_talk_addon	= [   
	
]

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
		pos = FindDialog_i(orig_dialogs, anyone,"member_chat")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, companion_pretalk_addon)
		# Insert Companion Dialog
		pos = FindDialog_i(orig_dialogs, anyone|plyr, "companion_recruit_backstory_response")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, companion_talk_addon)
		# Prevent companions from quitting if their introduction story arc is complete.
		pos = FindDialog_i(orig_dialogs, eq, "$map_talk_troop", "$npc_is_quitting")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, (neg|troop_slot_eq, "$map_talk_troop", slot_troop_intro_quest_complete, floris_story_arc_successful),)
		# Prevent companions from complaining if their introduction story arc is complete.
		# pos = FindDialog_i(orig_dialogs, eq, "$map_talk_troop", "$npc_with_grievance")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, (neg|troop_slot_eq, "$map_talk_troop", slot_troop_intro_quest_complete, floris_story_arc_successful),)
		# Insert Village Elder Dialog
		pos = FindDialog_i(orig_dialogs, anyone,"village_elder_deliver_cattle_thank")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, village_elder_talk_addon)
		# Insert Generic Actor Dialog
		pos = FindDialog_i(orig_dialogs, anyone ,"start")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, actor_dialog)
		
		##ORIG_DIALOGS is a list, can use OpBlockWrapper and other list operations.
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)