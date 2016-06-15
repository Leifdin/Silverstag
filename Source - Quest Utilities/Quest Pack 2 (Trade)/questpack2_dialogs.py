# Quest Pack 2 (1.0) by Windyplains

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

dialogs	= [   
    
	
]


lord_talk_addon	= [   
	##### QUEST : A NOBLE OPPORTUNITY : BEGIN #####
    [anyone|plyr,"lord_talk",
		[
			(check_quest_active, "qst_trade_noble_opportunity"),
			(quest_get_slot, ":troop_no", "qst_trade_noble_opportunity", slot_quest_giver_troop),
			(eq, "$g_talk_troop", ":troop_no"),
			(quest_slot_eq, "qst_trade_noble_opportunity", slot_quest_current_state, qp2_opportunity_begun),
			(str_store_troop_name, s21, ":troop_no"),
		], "I hear you are seeking investors willing to back your campaign.", "quest_noble_opportunity_a1", 
		[
			# Initialize carry over variables.
			(assign, reg51, 0), # Intimidation or Persuasion check.
			(call_script, "script_common_quest_change_state", "qst_trade_noble_opportunity", qp2_opportunity_discussed_with_lord),
			(call_script, "script_troop_get_player_relation", "$g_talk_troop"),
			(try_begin),
				(gt, reg0, 0),
				(assign, reg50, 1),
			(else_try),
				(assign, reg50, 0),
			(try_end),
		]],
		
	## Lord is on neutral or better terms with player so will ask for loan.
	[anyone,"quest_noble_opportunity_a1",
		[
			(this_or_next|eq, reg50, 1),
			(eq, reg51, 1),
			(try_begin),
				(eq, reg50, 1),
				(str_store_string, s21, "@Yes, "),
			(else_try),
				(str_clear, s21),
			(try_end),
			# (troop_slot_eq, "$g_talk_troop", slot_lord_reputation, lrep_martial),
			# Quarrelsome
			# Roguish
		], "{s21}I grown tired listening to tales of our caravans being assaulted in the lands of our enemies while they do nothing to deal with their unruly commoners.", "quest_noble_opportunity_a2", 
		[]],
		
	[anyone,"quest_noble_opportunity_a2",
		[], "I mean to put bring peace to the area even if I have to put every one of these miscreants to the sword myself.  To do so I need more men, likely mercenaries, and that will be costly.", "quest_noble_opportunity_a3", []],
		
	[anyone,"quest_noble_opportunity_a3",
		[
			(quest_get_slot, reg21, "qst_trade_noble_opportunity", slot_quest_target_amount),
			(try_begin),
				(eq, "$quest_reactions", QUEST_REACTIONS_HIGH),
				(str_store_string, s21, "@three times"),
			(else_try),
				(eq, "$quest_reactions", QUEST_REACTIONS_MEDIUM),
				(str_store_string, s21, "@nearly three times"),
			(else_try),
				(str_store_string, s21, "@double"),
			(try_end),
		], "I am seeking a sum of {reg21} denars to ensure this cause is successful and I will offer {s21} this amount in repayment by a month's time should I be successful.  Understand that I will not be held to any notion of debt should this venture fail.  These are my terms.  What say you?", "quest_noble_opportunity_a4", 
		[]],
		
	# PC accepts offer. -> continue A series.
	[anyone|plyr,"quest_noble_opportunity_a4",
		[
			(quest_get_slot, reg21, "qst_trade_noble_opportunity", slot_quest_target_amount),
			(store_troop_gold, ":gold", "trp_player"),
			(ge, ":gold", reg21),
			(str_store_troop_name, s21, "$g_talk_troop"),
		], "Your plan has merit, {s21}.  I will supply the {reg21} denars you need.", "quest_noble_opportunity_a5", 
		[]],
		
	[anyone,"quest_noble_opportunity_a5",
		[], "A wise choice and you have my gratitude.  Just remember, one month's time.  I will send word for you when I have your repayment.", "lord_pretalk", 
		[
			(quest_get_slot, ":investment", "qst_trade_noble_opportunity", slot_quest_target_amount),
			(troop_remove_gold, "trp_player", ":investment"),
			(call_script, "script_common_quest_change_state", "qst_trade_noble_opportunity", qp2_opportunity_provided_loan),
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_update),
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 2),
			(troop_get_slot, ":wealth", "$g_talk_troop", slot_troop_wealth),
			(val_add, ":wealth", ":investment"),
			(troop_set_slot, "$g_talk_troop", slot_troop_wealth, ":wealth"),
		]],
		
	# PC cannot afford offer. -> B series.
	[anyone|plyr,"quest_noble_opportunity_a4",
		[
			(quest_get_slot, reg21, "qst_trade_noble_opportunity", slot_quest_target_amount),
			(store_troop_gold, ":gold", "trp_player"),
			(lt, ":gold", reg21),
			(assign, reg22, ":gold"),
		], "A noble plan, but I cannot part with more than {reg22} denars at this time.", "quest_noble_opportunity_b1", []],
		
	# PC rejects offer politely. -> B series.
	[anyone|plyr,"quest_noble_opportunity_a4",
		[
			(quest_get_slot, reg21, "qst_trade_noble_opportunity", slot_quest_target_amount),
			(str_store_troop_name, s21, "$g_talk_troop"),
		], "I wish you luck in your venture, {s21}, but I must decline.", "quest_noble_opportunity_b1", []],
		
	[anyone,"quest_noble_opportunity_b1",
		[], "That is unfortunate, but I understand your situation.  My offer stands unless I find another lender should you change your mind.", "lord_pretalk", 
		[
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 1),
			# You gain some relation for just listening.  Quest should end now based on expiration or a trade rival winning it.
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_update),
		]],
		
	# PC rejects offer rudely. -> C series.
	[anyone|plyr,"quest_noble_opportunity_a4",
		[
			(quest_get_slot, reg21, "qst_trade_noble_opportunity", slot_quest_target_amount),
		], "{reg21} denars?!  Have you lost your senses?", "quest_noble_opportunity_c1", 
		[]],
		
	[anyone,"quest_noble_opportunity_c1",
		[
			(call_script, "script_cf_qus_player_is_king", 0),
			(call_script, "script_cf_qus_player_is_vassal", 0),
		], "Do not speak to me as if you are my better!  Now begone from my sight before I have my guards cut out your tongue as an example for all to see and not hear!", "close_window", 
		[
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_fail),
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -8),
		]],
		
	[anyone,"quest_noble_opportunity_c1",
		[
			(call_script, "script_cf_qus_player_is_vassal", 1),
		], "Very well, then I shall find someone with a stronger stomach for gaining profit.  Now I must attend to other matters.", "close_window", 
		[
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_fail),
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -4),
		]],
		
	[anyone,"quest_noble_opportunity_c1",
		[
			(call_script, "script_cf_qus_player_is_king", 1),
		], "Very well, {playername}, then I shall have to look elsewhere to find what I need.  Now if you do not mind I have other duties I must attend to.", "close_window", 
		[
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_fail),
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),
		]],
		
	## Lord is on poor terms with the player so will attempt to reject the loan unless convinced. -> D series
	[anyone,"quest_noble_opportunity_a1",
		[
			(eq, reg50, 0),
		], "I am seeking an interested lender, but I have no desire to be indebt to you.", "quest_noble_opportunity_d1", 
		[]],
		
	# PC attempts to persuade lord. -> continue D series.
	[anyone|plyr,"quest_noble_opportunity_d1",
		[], "You don't have to like me to like the coin I carry. (Persuade)", "quest_noble_opportunity_d1", 
		[
			(try_begin),
				(call_script, "script_cf_common_quest_persuasion_check", "trp_player", "$g_talk_troop", CHECK_DC_NORMAL),
				(assign, reg51, 1),
			(else_try),
				(assign, reg51, 0),
			(try_end),
		]],
	
	[anyone,"quest_noble_opportunity_d1",
		[
			(eq, reg51, 1), # Successful persuasion attempt.
		], "You have a valid point.  Very well, I will consider trusting you on this, but if you betray my trust there will be consequences.", "quest_noble_opportunity_a1", []],
		
	[anyone,"quest_noble_opportunity_d1",
		[
			(eq, reg51, 0), # Failed persuasion attempt.
		], "That may be, but I do not simply dislike you.  I do not trust you.  I have more important things to attend to.", "close_window", []],
		
	# PC attempts to intimidate lord. -> E series.
	[anyone|plyr,"quest_noble_opportunity_d1",
		[
			(try_begin),
				(call_script, "script_cf_qus_player_is_king", 1),
				(str_store_string, s22, "@Once these pretenders are cast down I will be king.  You would do well to remember that."),
			(else_try),
				(call_script, "script_cf_qus_player_is_vassal", 1),
				(store_faction_of_troop, ":faction_no", "$g_talk_troop"),
				(faction_get_slot, ":ruler", ":faction_no", slot_faction_leader),
				(ge, ":ruler", 1),
				(troop_get_type, reg22, ":ruler"),
				(str_store_string, s22, "@I suppose you have the blessing of the {reg22?Queen:King?}.  I thought not."),
			(else_try),
				(str_store_string, s22, "@I've heard enough rumor of your plans and so too shall others."),
			(try_end),
		], "{s22} (Intimidate)", "quest_noble_opportunity_e1", 
		[
			(call_script, "script_change_player_honor", -1),
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),
			(try_begin),
				(call_script, "script_cf_common_quest_intimidation_check", "trp_player", "$g_talk_troop", CHECK_DC_HARD),
				(assign, reg51, 1),
			(else_try),
				(assign, reg51, 0),
			(try_end),
		]],
		
	[anyone,"quest_noble_opportunity_e1",
		[
			(eq, reg51, 1), # Successful intimidate attempt.
			(troop_get_type, reg22, "$g_talk_troop"),
			(try_begin),
				(call_script, "script_cf_qus_player_is_king", 1),
				(str_store_string, s22, "@test."),
			(else_try),
				(call_script, "script_cf_qus_player_is_vassal", 1),
				(str_store_string, s22, "@test"),
			(else_try),
				(str_store_string, s22, "@test"),
			(try_end),
		], "{s22}", "quest_noble_opportunity_a1", 
		[
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2),
		]],
		
	[anyone,"quest_noble_opportunity_e1",
		[
			(eq, reg51, 0), # Failed intimidate attempt.
			(troop_get_type, reg22, "$g_talk_troop"),
			(try_begin),
				(call_script, "script_cf_qus_player_is_king", 1),
				(str_store_string, s22, "@I shall not yield to a tyrant, even if {reg22?she:he} is a king.  We are done here."),
			(else_try),
				(call_script, "script_cf_qus_player_is_vassal", 1),
				(str_store_string, s22, "@Have you no honor?  I will not yield to your threats.  Now begone!"),
			(else_try),
				(str_store_string, s22, "@You seek to intimidate me, you impudent whelp?  I will have you flogged if you do not remove yourself from my sight this instant."),
			(try_end),
		], "{s22}", "close_window", 
		[
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_fail),
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -4),
		]],
		
	# PC accepts rejection.
	[anyone|plyr,"quest_noble_opportunity_d1",
		[], "Very well.  Good day to you then.", "close_window", []],
	
	#### REPAYMENT SECTION ####
	[anyone|plyr,"lord_talk",
		[
			(check_quest_active, "qst_trade_noble_opportunity"),
			(quest_get_slot, ":troop_no", "qst_trade_noble_opportunity", slot_quest_giver_troop),
			(eq, "$g_talk_troop", ":troop_no"),
			(quest_slot_eq, "qst_trade_noble_opportunity", slot_quest_current_state, qp2_opportunity_lord_ready_to_repay),
			(str_store_troop_name, s21, ":troop_no"),
		], "I received your letter.", "quest_noble_opportunity_f1", 
		[
			(call_script, "script_common_quest_change_state", "qst_trade_noble_opportunity", qp2_opportunity_received_payment),
		]],
		
	## LORD WILL REPAY THE PLAYER ## -> Continue F series.
	[anyone,"quest_noble_opportunity_f1",
		[
			(neg|quest_slot_eq, "qst_trade_noble_opportunity", slot_quest_lord_will_repay_loan, 0),
		], "Ah, {playername}, I am glad you have received my message.  Things have progressed quite well and I'd be happy to square my debt with you.  Should I have need of a lender again, I shall send word for you.", "lord_pretalk", 
		[
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_succeed),
		]],
		
	## LORD WILL NOT REPAY THE PLAYER ## -> Switch to G series.
	[anyone,"quest_noble_opportunity_f1",
		[
			(quest_slot_eq, "qst_trade_noble_opportunity", slot_quest_lord_will_repay_loan, 0),
		], "And so you have come for payment?  Well I must disappoint you as events did not turn out in my favor.  I trust you understand as part of our agreement I recognize no debt between us.", "quest_noble_opportunity_g1", 
		[]],
	
	# Player response - Persuasion attempt for partial payment. -> Switch to H series.
	[anyone|plyr,"quest_noble_opportunity_g1",
		[], "Surely you can provide some recompensation lest other sources of funding become unavailable. (Persuade)", "quest_noble_opportunity_h1", 
		[
			(try_begin),
				(call_script, "script_cf_common_quest_persuasion_check", "trp_player", "$g_talk_troop", CHECK_DC_NORMAL),
				(assign, reg51, 1),
			(else_try),
				(assign, reg51, 0),
			(try_end),
		]],
		
	[anyone,"quest_noble_opportunity_h1",
		[
			(neq, reg51, 0), # Successful persuasion attempt.
			# Figure out half of our promised loan.
			(quest_get_slot, reg21, "qst_trade_noble_opportunity", slot_quest_target_amount),
			(val_div, reg21, 2),
			# Compare against what the lord can spare.
			(troop_get_slot, ":10_percent_of_wealth", "$g_talk_troop", slot_troop_wealth),
			(val_div, ":10_percent_of_wealth", 10),  # This is 10% because inflated it can be as much as 32%.
			(val_min, reg21, ":10_percent_of_wealth"),
			# Record the uninflated value for later use.
			(assign, "$temp", reg21),
			# Inflate the new contract value for the player's display.
			(quest_get_slot, ":return_factor", "qst_trade_noble_opportunity", slot_quest_payment_return),
			(val_mul, reg21, ":return_factor"),
			(val_div, reg21, 100),
		], "I do not like your tone, but in the spirit of future business arrangements between us I will refund you {reg21} denars.  Is this acceptable?", "quest_noble_opportunity_h2", 
		[]],
	
	[anyone|plyr,"quest_noble_opportunity_h2",
		[], "Yes, that will make things with us even.", "lord_pretalk", 
		[
			(quest_set_slot, "qst_trade_noble_opportunity", slot_quest_target_amount, "$temp"),
			(quest_set_slot, "qst_trade_noble_opportunity", slot_quest_lord_will_repay_loan, 2),
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_succeed),
		]],
	
	[anyone,"quest_noble_opportunity_h1",
		[
			(eq, reg51, 0), # Failed persuasion attempt.
		], "We had an arrangement that you agreed upon.  The potential repayment was balanced against the risk and in this case it did not pay off.  Press me any further and you may find doing business with other lords difficult yourself.", "lord_pretalk", 
		[
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1),
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_succeed),
		]],
	
	# Player response - Okay with non-payment.
	[anyone|plyr,"quest_noble_opportunity_g1",
		[], "Those were the terms, but it is unfortunate things did not turn out as desired.", "quest_noble_opportunity_g1", 
		[
			(quest_set_slot, "qst_trade_noble_opportunity", slot_quest_target_amount, 0),
			(call_script, "script_qp2_quest_trade_noble_opportunity", floris_quest_succeed),
		]],
	
	##### QUEST : A NOBLE OPPORTUNITY : END #####
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