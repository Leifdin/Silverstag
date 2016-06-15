# Quest Pack 5 (1.0) by Windyplains

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

dialogs	= [   

]

companion_pretalk_addon = [
	## QUEST - A CRAFTSMAN'S KNOWLEDGE - LOW SUPPLIES CONVERSATION - BEGIN ##
	[anyone,"event_triggered", 
		[
			(check_quest_active, "qst_qp5_craftsmans_knowledge"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_supplies_low),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_center, "$current_town"),
			(quest_get_slot, ":target_center", "qst_qp5_craftsmans_knowledge", slot_quest_target_party),
			(str_store_party_name, s41, ":target_center"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 1),
		],
		"{s66}, it seems we're running short on hand tools for the workers.  What we have available isn't the best quality, but I'm sure if we sent some men to {s41} we could find what we need.", "crafsmans_knowledge_c1",
		[]],
	
	[anyone,"event_triggered", 
		[
			(check_quest_active, "qst_qp5_craftsmans_knowledge"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_supplies_low),
			(is_between, "$g_talk_troop", companions_begin, companions_end),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_center, "$current_town"),
			(quest_get_slot, ":target_center", "qst_qp5_craftsmans_knowledge", slot_quest_target_party),
			(str_store_party_name, s41, ":target_center"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 1),
		],
		"{s66}, the men tell me that our supplies are running low.  The tools these villagers have available for construction are inadequate and break too easily.  I don't want to risk someone getting injured so I think we need to seek better quality tools at a nearby city.  Maybe over in {s41}.", "crafsmans_knowledge_c1",
		[]],
	## QUEST - A CRAFTSMAN'S KNOWLEDGE - LOW SUPPLIES CONVERSATION - end ##
	
	## QUEST - SENDING_AID - Too much time taken escorting elder back to the quest giving village.
	[anyone,"event_triggered", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_took_too_long),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			# Name the center that sent the supplies.
			(quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			(str_store_party_name, s12, ":giver_center"),
		],
		"I appreciate that you've allowed me to come along with your group{s66}.  Now that we're past bandit country I think I can make my own way and I am eager to visit {s12}.  I wish you well on your journey.", "close_window", 
		[
			(quest_set_slot, "qst_qp5_sending_aid", slot_quest_target_state, 2),
			(call_script, "script_qp5_quest_sending_aid", floris_quest_succeed),
		]],
]


village_elder_talk_addon	= [   
#################################################################### QUEST : CRAFTSMANS_KNOWLEDGE : BEGIN ####################################################################
	
	## QUEST ACCEPTANCE - BEGIN ##
	[anyone,"village_elder_tell_mission", 
		[
			(eq, "$random_quest_no", "qst_qp5_craftsmans_knowledge"),
			(store_faction_of_party, ":faction_no", "$current_town"),
			(call_script, "script_common_store_temp_name_to_s1", 0, ":faction_no", SCRT_FIRST),
			(str_store_string, s41, s1), # So it isn't overwritten by the next script.
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			(party_get_slot, ":town_lord", "$current_town", slot_town_lord),
			(str_store_troop_name, s21, ":town_lord"),
		],
   "Yes{s66}.  {s41} was heading construction of the project, but he has fallen quite ill.  Without his guidance we are unable to continue and I fear that news will go quite badly with {s21}.", "crafsmans_knowledge_a2",
		[]],
		
	# Player response.
	[anyone|plyr,"crafsmans_knowledge_a2", 
		[
			(quest_get_slot, ":engineer", "$random_quest_no", slot_quest_object_troop),
			(str_store_troop_name, s22, ":engineer"),
			(troop_get_type, reg21, ":engineer"),
			(try_begin),
				(eq, ":engineer", "trp_player"),
				(str_store_string, s21, "@Well, I have some experience with this kind of work.  Provided it is worth my time, I could oversee the work remaining to complete the project."),
			(else_try),
				(str_store_string, s21, "@I have a {reg21?lady:man}, by the name of {s22}, with me skilled in construction and we could lend a hand getting you back on track."),
			(try_end),
		],
		"{s21}", "crafsmans_knowledge_a3",[]],
	
	[anyone,"crafsmans_knowledge_a3", 
		[
			(party_get_slot, ":town_lord", "$current_town", slot_town_lord),
			(str_store_troop_name, s21, ":town_lord"),
		],
		"You would do this?  This project has already taxed the coffers I was granted by {s21}, but any excess will be yours if you agree to oversee the project.  I'm sure if you use some of your men to aid in the labor then a greater portion will be left for payment.", "crafsmans_knowledge_a4",[]],
	
	# player decision
	[anyone|plyr,"crafsmans_knowledge_a4", [],
		"I agree.  I'll oversee the project and add my men to the laborers.", "crafsmans_knowledge_a5",[]],
	[anyone|plyr,"crafsmans_knowledge_a4", [],
		"I'll oversee the project, but my men are warriors, not laborers.", "crafsmans_knowledge_a6",[]],
	[anyone|plyr,"crafsmans_knowledge_a4", [],
		"I can't spare the time to help you in this right now.", "crafsmans_knowledge_a7",[]],
	
	
	[anyone,"crafsmans_knowledge_a5", [], 
		"Oh, thank you!  I'll let the townsfolk know and make sure you have access to all of the materials you'll need.  When next you return we'll be ready to continue.", "village_elder_pretalk",
		[
			(assign, "$g_leave_encounter",1),
			(quest_set_slot, "$random_quest_no", slot_quest_convince_value, 1), # Player is using soldiers for labor.
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_begin), # Initiate quest.
			#(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
		]],
	
	[anyone,"crafsmans_knowledge_a6", 
		[
			(quest_get_slot, ":center_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount), # The center upgrade spot was hidden here.
			(party_get_slot, ":improvement", "$current_town", ":center_slot"),
			(call_script, "script_get_improvement_details", ":improvement"),
		], 
		"Then it is settled.  I'll make the townsfolk aware of the arrangement and instruct them to follow your orders in completing the {s0}.  When next you return we'll be ready to continue.", "village_elder_pretalk",
		[
			(assign, "$g_leave_encounter",1),
			(quest_set_slot, "$random_quest_no", slot_quest_convince_value, 0), # Player is NOT using soldiers for labor.
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_begin), # Initiate quest.
			#(call_script, "script_start_quest", "$random_quest_no", "$g_talk_troop"),
		]],
	
	[anyone,"crafsmans_knowledge_a7", 
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),], 
		"Yes{s66}, of course. I am sorry if I have bothered you with our troubles.", "close_window",
		[
			(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
		]],
	
	## QUEST ACCEPTANCE - END ##
	
	## POST INJURY CONVERSATION - BEGIN ##
	[anyone,"start", 
		[
			(check_quest_active, "qst_qp5_craftsmans_knowledge"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_worker_injury),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_center, "$current_town"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 1),
			# (party_get_slot, ":town_lord", "$current_town", slot_town_lord),
			# (str_store_troop_name, s21, ":town_lord"),
		],
		"{s66}, I heard what happened.  Is there anything I can do to help?", "crafsmans_knowledge_b1",
		[]],
	
	[anyone|plyr,"crafsmans_knowledge_b1", 
		[],
		"I want to know that the family of that soldier will be rightly compensated.  Can you guarantee this?", "crafsmans_knowledge_b2",
		[]],
	
	[anyone,"crafsmans_knowledge_b2", 
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"Surely you can appreciate that these things happen during such projects.  Is this not a risk you accepted by using your own men{s66}?", "crafsmans_knowledge_b3",
		[]],
	
	[anyone|plyr,"crafsmans_knowledge_b3", 
		[],
		"Perhaps you are right.", "close_window",
		[
			(try_begin),
				(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_primary_commodity, -1),
				(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_supplies_restored),
			(else_try),
				(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_begun),
			(try_end),
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
			(change_screen_return),
		]],
	
	[anyone|plyr,"crafsmans_knowledge_b3", 
		[],
		"This isn't the kind of risk I trained my men for.  You'll have to finish the project yourself.", "crafsmans_knowledge_b4",
		[]],
	
	[anyone,"crafsmans_knowledge_b4", 
		[
			(quest_get_slot, ":center_slot", "qst_qp5_craftsmans_knowledge", slot_quest_target_amount), # The center upgrade spot was hidden here.
			(party_get_slot, ":improvement", "$current_town", ":center_slot"),
			(call_script, "script_get_improvement_details", ":improvement"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"Then we'll continue on without your men if need be, but I will not compensate you for not finishing the {s0}{s66}", "close_window",
		[
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_fail),
			(change_screen_return),
		]],
	## POST INJURY CONVERSATION - END ##
	
	## LOW SUPPLIES CONVERSATION - CONTINUED ##
	[anyone|plyr,"crafsmans_knowledge_c1", 
		[],
		"I see.  I'll gather some men and get the supplies, but keep working for now.", "crafsmans_knowledge_c2",
		[]],
	
	[anyone|plyr,"crafsmans_knowledge_c1", 
		[
			(try_begin),
				(is_between, "$g_talk_troop", companions_begin, companions_end),
				(assign, reg21, 1), # A companion is our talk troop.
			(else_try),
				(assign, reg21, 0), # Village elder is our talk troop.
			(try_end),
		],
		"Then let some of {reg21?the:your} villagers fetch the necessary tools.  We'll come back when things are ready to continue.", "crafsmans_knowledge_c3",
		[]],
	
	[anyone|plyr,"crafsmans_knowledge_c1", 
		[],
		"This project has become too costly to bother with.  I am taking my men and leaving.", "crafsmans_knowledge_c4",
		[]],
	
	[anyone,"crafsmans_knowledge_c2", 
		[
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"Very good{s66}.  Then we shall await your return.", "close_window",
		[
			(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_supplies_being_obtained_by_player),
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_3_trigger_chance, 1), # Record that the player is the one getting the supplies.
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_1_trigger_chance, 0), # Since townsfolk aren't going after the stuff.
		]],
	
	[anyone,"crafsmans_knowledge_c2", 
		[
			(is_between, "$g_talk_troop", companions_begin, companions_end),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"As you wish{s66}.  I'll leave instructions with the workers on what to accomplish while we are gone.", "close_window",
		[
			(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_supplies_being_obtained_by_player),
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_3_trigger_chance, 1), # Record that the player is the one getting the supplies.
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_1_trigger_chance, 0), # Since townsfolk aren't going after the stuff.
		]],
	
	[anyone,"crafsmans_knowledge_c3", 
		[
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_get_slot, reg21, "qst_qp5_craftsmans_knowledge", slot_quest_stage_1_trigger_chance), # Travel time.
			
		],
		"I shall dispatch a few of the men immediately and await your return.  I suspect it will take about {reg21} days.", "close_window",
		[
			(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_supplies_being_obtained_by_villagers),
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_3_trigger_chance, 0),
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
		]],
	
	[anyone,"crafsmans_knowledge_c3", 
		[
			(is_between, "$g_talk_troop", companions_begin, companions_end),
			(quest_get_slot, reg21, "qst_qp5_craftsmans_knowledge", slot_quest_stage_1_trigger_chance), # Travel time.
		],
		"I'll gather a few of the more dependable men and send them off.  I wager it will take them {reg21} days before they're back.", "close_window",
		[
			(call_script, "script_common_quest_change_state", "qst_qp5_craftsmans_knowledge", qp5_ck_supplies_being_obtained_by_villagers),
			(quest_set_slot, "qst_qp5_craftsmans_knowledge", slot_quest_stage_3_trigger_chance, 0),
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_update),
		]],
	
	[anyone,"crafsmans_knowledge_c4", 
		[
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
		],
		"I shall dispatch a few of the men immediately and await your return.  I suspect it will take about X days.", "close_window",
		[
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_fail),
		]],
	
	[anyone,"crafsmans_knowledge_c4", 
		[
			(is_between, "$g_talk_troop", companions_begin, companions_end),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"We made a promise to help these villagers{s66}.  I won't go against your orders, but I can not say I like breaking my word.", "close_window",
		[
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_fail),
		]],
	## LOW SUPPLIES CONVERSATION - END ##
	
	## ENDINGS - begin ##
	[anyone,"start", 
		[
			(check_quest_active, "qst_qp5_craftsmans_knowledge"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_work_completed),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_center, "$current_town"),
			(party_get_slot, ":lord", "$current_town", slot_town_lord),
			(str_store_troop_name, s40, ":lord"),
		],
		"I just heard the news.  You've done our village a great service.  {s40} will be most pleased.", "village_elder_pretalk",
		[
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_succeed),
		]],
	
	[anyone,"start", 
		[
			(check_quest_active, "qst_qp5_craftsmans_knowledge"),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_current_state, qp5_ck_quest_failed),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_qp5_craftsmans_knowledge", slot_quest_target_center, "$current_town"),
			(party_get_slot, ":lord", "$current_town", slot_town_lord),
			(str_store_troop_name, s40, ":lord"),
		],
		"I had hoped that with your help the {s0} could be finished on time.  {s40} will not be pleased, but we will continue on from here.  It is best if were you not around when next he visits.  You must understand that I can only afford to pay you half of what I promised since the work is not complete.", "village_elder_pretalk",
		[
			(call_script, "script_qp5_quest_craftsmans_knowledge", floris_quest_succeed),
		]],
	## ENDINGS - end ##
	
#################################################################### QUEST : CRAFTSMANS_KNOWLEDGE : END ####################################################################

#################################################################### QUEST : SENDING_AID : BEGIN ####################################################################
	
	## QUEST ACCEPTANCE - BEGIN ##
	[anyone,"village_elder_tell_mission", 
		[
			(eq, "$random_quest_no", "qst_qp5_sending_aid"),
			#(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			# Name the village elder.
			(quest_get_slot, ":center_no", "qst_qp5_sending_aid", slot_quest_target_center),
			(str_store_party_name, s21, ":center_no"),
			(party_get_slot, ":raided_by", ":center_no", slot_village_raided_by),
			(try_begin),
				(party_is_active, ":raided_by"),
				(party_stack_get_troop_id, ":raiding_lord", ":raided_by", 0),
				(is_between, ":raiding_lord", active_npcs_begin, active_npcs_end),
				(store_faction_of_troop, ":faction_no", ":raiding_lord"),
				(str_store_troop_name, s23, ":raiding_lord"),
				(str_store_faction_name, s24, ":faction_no"),
				(str_store_string, s22, "@ by {s23} of the {s24}"),
			(else_try),
				(str_clear, s22),
			(try_end),
		],
   "Our neighbors in {s21} were recently raided{s22} and we're gathering supplies to help them rebuild.  I fear that if we cannot spare enough men to defend the supplies our efforts will be in vain.", "sending_aid_a2", []],
	
	[anyone|plyr,"sending_aid_a2", [], "My men are heading in that direction.  We could bring the supplies for you.", "sending_aid_a3",	[]],
	
	# You've been good to us in the past and I know I can trust you.
	[anyone,"sending_aid_a3", 
		[
			(party_slot_ge, "$current_town", slot_center_player_relation, 5),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"Your help would be most welcome{s66}.  Beyond just supplies they'll need men to help them fend off bandits until things are back to normal.  Would you do this?", "sending_aid_a4",
		[]],
	
	# I don't know you, but I hear you can be trusted.
	[anyone,"sending_aid_a3", 
		[
			(party_slot_ge, "$current_town", slot_center_player_relation, -5),
			(troop_slot_ge, "trp_player", slot_troop_renown, 100),
			(ge, "$player_honor", 4),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			(quest_get_slot, ":center_no", "qst_qp5_sending_aid", slot_quest_target_center),
			(str_store_party_name, s21, ":center_no"),
		],
		"I do not know you well{s66}, but I have heard good word of your deeds from travelers passing by.  Can I trust that you'll see these supplies safely to {s21} and help their village fend off any attacks while repairs are made?", "sending_aid_a4",
		[]],
	
	# Yeah, right.  Buzz off.
	[anyone,"sending_aid_a3", 
		[
			(quest_get_slot, ":center_no", "qst_qp5_sending_aid", slot_quest_target_center),
			(str_store_party_name, s21, ":center_no"),
		],
		"These supplies are direly needed in {s21} and while you may mean well I can't entrust this to a stranger.", "village_elder_pretalk",
		[]],
	
	[anyone|plyr,"sending_aid_a4", [], "Those supplies are as good as delivered.", "sending_aid_a5", []],
	
	[anyone|plyr,"sending_aid_a4", [], "I don't have that much time to spare right now.", "sending_aid_a6", []],
	
	[anyone,"sending_aid_a5", 
		[
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		], "Thank you{s66}.  I'll see that the supplies are turned over to your men.", "village_elder_pretalk", 
		[
			(call_script, "script_qp5_quest_sending_aid", floris_quest_begin),
		]],
	
	[anyone,"sending_aid_a6", 
		[
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		], 
		"Yes{s66}, of course. I am sorry if I have bothered you with our troubles.", "close_window",
		[
			(troop_set_slot, "$g_talk_troop", slot_troop_does_not_give_quest, 1),
		]],
	## QUEST ACCEPTANCE - END ##
		
	## SUPPLIES DELIVERED - BEGIN ##
	[anyone,"start", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_begun),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_target_center, "$current_town"),
			# Name the village elder that sent the supplies.
			(quest_get_slot, ":giver_mayor", "qst_qp5_sending_aid", slot_quest_giver_troop),
			(str_store_troop_name, s11, ":giver_mayor"),
			(troop_get_type, reg11, ":giver_mayor"),
			(quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			(str_store_party_name, s12, ":giver_center"),
		],
		"These supplies came from {s11} in {s12}?  Bless {reg11?her:him} as they are sorely needed.  I know you've already done much by bringing these here, but could I convince you to stay near the town while we make initial repairs?  The village is defenseless at the moment and that will draw bandits to us for certain.", "sending_aid_f1",
		[
			(call_script, "script_common_quest_change_state", "qst_qp5_sending_aid", qp5_sa_recovery),
			(call_script, "script_qp5_quest_sending_aid", floris_quest_update),
		]],
	
	[anyone|plyr,"sending_aid_f1", 
		[(lt, "$quest_reactions", QUEST_REACTIONS_HIGH),],
		"Very well.  My men will remain in the area for a while.", "sending_aid_f2",
		[]],
	
	[anyone|plyr,"sending_aid_f1", 
		[(lt, "$quest_reactions", QUEST_REACTIONS_HIGH),],
		"I wish I could help, but I've already gone out of my way to get here.", "sending_aid_f3",
		[]],
	
	[anyone|plyr,"sending_aid_f1", 
		[(ge, "$quest_reactions", QUEST_REACTIONS_HIGH),],
		"Very well.  My men will remain in the area for a while.", "sending_aid_f2",
		[]],
	
	[anyone,"sending_aid_f2", 
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"That would be most helpful{s66}.  I'll let our lookouts at the edges of town know they can come in to help build while you keep an eye to the horizon.  That should speed things up considerably.", "close_window",
		[]],
	
	[anyone,"sending_aid_f3", 
		[
			# Name the village elder that sent the supplies.
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			(quest_get_slot, ":giver_mayor", "qst_qp5_sending_aid", slot_quest_giver_troop),
			(str_store_troop_name, s21, ":giver_mayor"),
			(quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			(str_store_party_name, s22, ":giver_center"),
		],
		"I understand{s66}.  You've done more for us than most would already and I appreciate that.  Please send {s21} my regards next time you're in {s22}.", "close_window",
		[
			(quest_set_slot, "qst_qp5_sending_aid", slot_quest_target_state, 1),
			(call_script, "script_qp5_quest_sending_aid", floris_quest_succeed),
		]],
	
	## SUPPLIES DELIVERED - END ##
	
	## VILLAGE RESTORED - BEGIN ##
	[anyone,"start", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_village_recovered),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_target_center, "$current_town"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 1),
			# Name the village elder that sent the supplies.
			# (quest_get_slot, ":giver_mayor", "qst_qp5_sending_aid", slot_quest_giver_troop),
			# (str_store_troop_name, s11, ":giver_mayor"),
			# (troop_get_type, reg11, ":giver_mayor"),
			(quest_get_slot, ":target_center", "qst_qp5_sending_aid", slot_quest_target_center),
			(str_store_party_name, s12, ":target_center"),
		],
		"{s66}, you've done us a great service helping rebuild {s12}.   I wish I had more to repay you.", "sending_aid_b1", []],
	
	[anyone|plyr,"sending_aid_b1", 
		[],
		"It was no trouble.  I'm glad we could help.", "sending_aid_b2",
		[]],
	
	[anyone,"sending_aid_b2", 
		[
			# Name the village elder that sent the supplies.
			(quest_get_slot, ":giver_mayor", "qst_qp5_sending_aid", slot_quest_giver_troop),
			(str_store_troop_name, s11, ":giver_mayor"),
			# Name the starting village.
			(quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			(str_store_party_name, s12, ":giver_center"),
		],
		"There is one last request I hope you can help with.  I'd like to visit {s12} to give my thanks to {s11} in person, but the road would be dangerous alone.  Could I convince you to head back that way?", "sending_aid_b3",
		[]],
	
	# Sure, why not.
	[anyone|plyr,"sending_aid_b3", 
		[
			# Name the starting village.
			(quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			(str_store_party_name, s12, ":giver_center"),
		],
		"I'll escort you back to {s12}.", "sending_aid_b4",
		[]],
	
	# Nope, don't have time for that.
	[anyone|plyr,"sending_aid_b3", 
		[],
		"We won't be going back that way anytime soon.", "sending_aid_b5",
		[]],
	
	[anyone,"sending_aid_b4", 
		[],
		"That's greatly appreciated.  I'll go pack a few things and will be ready when you wish to leave.", "close_window",
		[
			(call_script, "script_common_quest_change_state", "qst_qp5_sending_aid", qp5_sa_escort),
			(call_script, "script_qp5_quest_sending_aid", floris_quest_update),
			(party_add_members, "p_main_party", "$g_talk_troop", 1),
		]],
	
	[anyone,"sending_aid_b5", 
		[
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"I understand.  I'll just join one of the caravans that pass through when the chance permits.  Thank you for all that you've done{s66}.", "village_elder_pretalk",
		[
			(quest_set_slot, "qst_qp5_sending_aid", slot_quest_target_state, 2),
			(call_script, "script_qp5_quest_sending_aid", floris_quest_succeed),
		]],
	
	## VILLAGE RESTORED - END ##
	
	## CONCLUSION - BEGIN ##
	[anyone,"start", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_returned_to_giver),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_giver_center, "$current_town"),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			# Name the saved village.
			(quest_get_slot, ":target_center", "qst_qp5_sending_aid", slot_quest_target_center),
			(str_store_party_name, s12, ":target_center"),
			# Name the village elder.
			(store_sub, ":center_offset", ":target_center", villages_begin),
			(store_add, ":mayor", ":center_offset", "trp_village_1_elder"),
			(str_store_troop_name, s11, ":mayor"),
			(troop_get_type, reg11, ":mayor"),
		],
		"Ah, there you are{s66}.  {s11} just informed me of how you helped {reg11?her:him} rebuild and then were gracious enough to escort {reg11?her:him} to our village.  Trade is the lifeblood of our villages so we can't have our neighbors destroyed in the constant warfare around here.  Thank you for your help in restoring {s12}.", "village_elder_pretalk", 
		[
			(quest_set_slot, "qst_qp5_sending_aid", slot_quest_target_state, 3),
			(call_script, "script_qp5_quest_sending_aid", floris_quest_succeed),
		]],
	
	## CONCLUSION - END ##
	
#################################################################### QUEST : SENDING_AID : END ####################################################################
	
]

member_pretalk = [
	## TRAVEL DIALOG - BEGIN ##
	[anyone,"start", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_escort),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_target_center, "$g_encountered_party"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			# Name the village elder that sent the supplies.
			# (quest_get_slot, ":giver_mayor", "qst_qp5_sending_aid", slot_quest_giver_troop),
			# (str_store_troop_name, s11, ":giver_mayor"),
			# (troop_get_type, reg11, ":giver_mayor"),
			# (quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			# (str_store_party_name, s12, ":giver_center"),
		],
		"I'm ready to leave whenever you are set to go{s66}.", "close_window", []],
	
	[anyone,"member_chat", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_escort),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			(assign, reg50, -1), # Early filter initialization.
			# Check that we're not near the initiating village.
			# (quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			# (store_distance_to_party_from_party, ":distance", "p_main_party", ":giver_center"),
			# (ge, ":distance", 1),
			# Check that we're not near the target village.
			# (quest_get_slot, ":target_center", "qst_qp5_sending_aid", slot_quest_target_center),
			# (store_distance_to_party_from_party, ":distance", "p_main_party", ":target_center"),
			# (ge, ":distance", 1),
			# Now setup our random selector.
			(store_random_in_range, reg50, 0, 3),
			# Prevent this dialog from firing.
			(eq, 1, 0),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			# Name the village elder that sent the supplies.
			# (quest_get_slot, ":giver_mayor", "qst_qp5_sending_aid", slot_quest_giver_troop),
			# (str_store_troop_name, s11, ":giver_mayor"),
			# (troop_get_type, reg11, ":giver_mayor"),
			# (quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			# (str_store_party_name, s12, ":giver_center"),
		],
		"This dialog should not be seen.", "close_window", []],
	
	# [anyone,"member_chat", 
		# [
			# (check_quest_active, "qst_qp5_sending_aid"),
			# (quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_escort),
			# (is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			# # Filter check.
			# (eq, reg50, -1),
			# # Name the village elder that sent the supplies.
			# (quest_get_slot, ":giver_mayor", "qst_qp5_sending_aid", slot_quest_giver_troop),
			# (str_store_troop_name, s11, ":giver_mayor"),
			# (troop_get_type, reg11, ":giver_mayor"),
			# (quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			# (str_store_party_name, s12, ":giver_center"),
		# ],
		# "I do hope we arrive in {s12} before too long.  I am eager to meet with {s11}.", "close_window", []],
	
	[anyone,"member_chat", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_escort),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			# Filter check.
			(eq, reg50, 0),
			# Name the village elder that sent the supplies.
			(quest_get_slot, ":giver_mayor", "qst_qp5_sending_aid", slot_quest_giver_troop),
			(str_store_troop_name, s11, ":giver_mayor"),
			(troop_get_type, reg11, ":giver_mayor"),
			(quest_get_slot, ":giver_center", "qst_qp5_sending_aid", slot_quest_giver_center),
			(str_store_party_name, s12, ":giver_center"),
		],
		"I do hope we arrive in {s12} before too long.  I am eager to meet with {s11}.", "close_window", []],
	
	[anyone,"member_chat", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_escort),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			# Filter check.
			(eq, reg50, 1),
			# Name the raiding faction.
			(quest_get_slot, ":center_no", "qst_qp5_sending_aid", slot_quest_target_center),
			(str_store_party_name, s21, ":center_no"),
			(party_get_slot, ":raided_by", ":center_no", slot_village_raided_by),
			(try_begin),
				(party_is_active, ":raided_by"),
				(party_stack_get_troop_id, ":raiding_lord", ":raided_by", 0),
				(is_between, ":raiding_lord", active_npcs_begin, active_npcs_end),
				(store_faction_of_troop, ":faction_no", ":raiding_lord"),
				(str_store_faction_name, s24, ":faction_no"),
				(str_store_string, s22, "@ from the {24}"),
			(else_try),
				(str_clear, s22),
			(try_end),
		],
		"Do you think we'll run into any trouble{s22} along the way?", "sending_aid_d2", []],
	
	[anyone|plyr,"sending_aid_d2", [], "Nothing we can't handle.", "close_window", []],
	
	[anyone,"member_chat", 
		[
			(check_quest_active, "qst_qp5_sending_aid"),
			(quest_slot_eq, "qst_qp5_sending_aid", slot_quest_current_state, qp5_sa_escort),
			(is_between, "$g_talk_troop", village_elders_begin, village_elders_end),
			# Filter check.
			(eq, reg50, 2),
			# Come up with a nearby city.
			(call_script, "script_qus_select_random_center", center_is_town, 1, 15, "p_main_party"),
			(str_store_party_name, s21, reg1),
		],
		"I see we're near {s21}.  I always wanted to visit there.", "close_window", []],
	## TRAVEL DIALOG - END ##

]

from util_common import *
from util_wrappers import *

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
		var_name_1 = "dialogs"
		orig_dialogs = var_set[var_name_1]
		orig_dialogs.extend(dialogs)
		
		# Insert Companion Pretalk Dialog
		pos = FindDialog_i(orig_dialogs, anyone,"member_chat")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, companion_pretalk_addon)
		
		# Insert Village Elder Dialog
		pos = FindDialog_i(orig_dialogs, anyone,"village_elder_deliver_cattle_thank")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, village_elder_talk_addon)
		
		# Insert Village Elder Dialog (traveling dialog to block member chat)
		pos = FindDialog_i(orig_dialogs, trp_kidnapped_girl,"member_chat")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, member_pretalk)
		
		# Insert Lord Dialog
		# pos = FindDialog_i(orig_dialogs, anyone,"lord_start")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, lord_talk_addon)
		# Insert Companion Dialog
		# pos = FindDialog_i(orig_dialogs, anyone|plyr, "companion_recruit_backstory_response")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, companion_talk_addon)
		# Prevent companions from quitting if their introduction story arc is complete.
		# pos = FindDialog_i(orig_dialogs, eq, "$map_talk_troop", "$npc_is_quitting")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, (neg|troop_slot_eq, "$map_talk_troop", slot_troop_intro_quest_complete, floris_story_arc_successful),)
		# Prevent companions from complaining if their introduction story arc is complete.
		# pos = FindDialog_i(orig_dialogs, eq, "$map_talk_troop", "$npc_with_grievance")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, (neg|troop_slot_eq, "$map_talk_troop", slot_troop_intro_quest_complete, floris_story_arc_successful),)
		# Insert Generic Actor Dialog
		# pos = FindDialog_i(orig_dialogs, anyone ,"start")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, actor_dialog)
		
		##ORIG_DIALOGS is a list, can use OpBlockWrapper and other list operations.
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)