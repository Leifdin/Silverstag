# Enhanced Diplomacy Options (1.0) by Windyplains

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

#################################################
##### ADVISOR: CAPTAIN OF THE GUARD : BEGIN #####
#################################################
advisor_war_dialogs = [
	# Opening dialog.
	[anyone, "start",
		[
			(party_slot_eq, "$g_encountered_party", slot_center_advisor_war, "$g_talk_troop"),
			(try_begin),
				(is_currently_night),
				(assign, reg21, 1),
			(else_try),
				(assign, reg21, 0),
			(try_end),
			(str_store_party_name, s21, "$current_town"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"Good {reg21?evening:day}{s66}.  I trust your journey to {s21} was without incident.  How may I be of service?  ", "advisor_war_talk",
		[]],
	   
	[anyone, "advisor_war_pretalk",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"Is there anything else I can do to help you{s66}?", "advisor_war_talk",
		[]],
		
	################ ADVISOR DEVELOPMENT : BEGIN ###################
	[anyone|plyr,"advisor_war_talk", [], "I'd like to discuss your development.", "advisor_development",[]],
	
	[anyone,"advisor_development", [], "Well, all right.", "advisor_development_topics",[]],
	
	[anyone|plyr, "advisor_development_topics",
		[],
		"Let's talk about your training.", "advisor_development_exit",
		[(change_screen_view_character)]],
	
	## BOOK READING : BEGIN ##
	[anyone|plyr, "advisor_development_topics",
		[],
		"Let's talk about your reading.", "advisor_development_reading",
		[]],
	
	[anyone, "advisor_development_reading",
		[
			## Find out current reading information ##
			(troop_get_slot, ":current_book", "$g_talk_troop", slot_troop_reading_book),
			(try_begin),
				(is_between, ":current_book", readable_books_begin, readable_books_end),
				(str_store_item_name, s21, ":current_book"),
				(store_sub, ":companion_no", "$g_talk_troop", companions_begin),
				(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
				(item_get_slot, reg21, ":current_book", ":book_read_slot"),
				(val_div, reg21, 10),
				(str_store_string, s22, "@I'm roughly {reg21}% through reading {s21}."),
			(else_try),
				(str_store_string, s22, "@I'm not currently reading anything."),
			(try_end),
			
			## Find out about current books available to read ##
			(assign, ":book_total", 0),
			(try_for_range, ":item_no", readable_books_begin, readable_books_end),
				(store_item_kind_count, ":book_count", ":item_no", "$g_talk_troop"),
				(ge, ":book_count", 1),
				(val_add, ":book_total", 1),
				(try_begin),
					(eq, ":book_total", 1),
					(str_store_string, s22, "@{s22}^^I'm carrying the following readable books on hand:"),
				(try_end),
				(str_store_item_name, s21, ":item_no"),
				(store_sub, ":companion_no", "$g_talk_troop", companions_begin),
				(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
				(try_begin),
					(item_slot_ge, ":item_no", ":book_read_slot", 1000),
					(str_store_string, s23, "@ (completed)"),
				(else_try),
					(troop_slot_eq, "$g_talk_troop", slot_troop_reading_book, ":item_no"),
					(item_get_slot, reg21, ":item_no", ":book_read_slot"),
					(val_div, reg21, 10),
					(str_store_string, s23, "@ ({reg21}% read)"),
				(else_try),
					(item_slot_ge, ":item_no", ":book_read_slot", 1),
					(item_get_slot, reg21, ":item_no", ":book_read_slot"),
					(val_div, reg21, 10),
					(str_store_string, s23, "@ ({reg21}% read)"),
				(else_try),
					(str_clear, s23),
				(try_end),
				(str_store_string, s22, "@{s22}^{s21} {s23}"),
			(try_end),
			
			## Find out about current books available to read ##
			(assign, ":book_total", 0),
			(try_for_range, ":item_no", reference_books_begin, reference_books_end),
				(store_item_kind_count, ":book_count", ":item_no", "$g_talk_troop"),
				(ge, ":book_count", 1),
				(val_add, ":book_total", 1),
				(try_begin),
					(eq, ":book_total", 1),
					(str_store_string, s22, "@{s22}^^I'm carrying the following reference books on hand:"),
				(try_end),
				(call_script, "script_game_get_item_extra_text", ":item_no", 0, 0),
				(str_store_item_name, s21, ":item_no"),
				(str_store_string, s22, "@{s22}^{s21} (+1 to {s1})"),
			(try_end),
		],
		"{s22}", "advisor_development_reading_topics",
		[]],
	
	## Switch Reading : Begin ##
	[anyone|plyr, "advisor_development_reading_topics",
		[
			(try_begin),
				(neg|troop_slot_eq, "$g_talk_troop", slot_troop_reading_book, 0),
				(str_store_string, s21, "@I want you to read a different book."),
			(else_try),
				(str_store_string, s21, "@I have a book I want you to read."),
			(try_end),
			(assign, ":book_total", 0),
			(try_for_range, ":item_no", readable_books_begin, readable_books_end),
				(store_item_kind_count, ":book_count", ":item_no", "$g_talk_troop"),
				(ge, ":book_count", 1),
				(val_add, ":book_total", 1),
			(try_end),
			(ge, ":book_total", 1), # Make sure we have any books available to read.
		],
		"{s21}", "advisor_development_reading_read_book",
		[]],
	
	[anyone, "advisor_development_reading_read_book",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"Certainly{s66}.  What book did you have in mind?", "advisor_development_reading_book_list",
		[]],
	
	[anyone|plyr|repeat_for_100, "advisor_development_reading_book_list",
		[
			(store_repeat_object, ":count"),
			(val_sub, ":count", 1), # Since we don't start at 0.
			# Make sure we have this book on hand.
			(store_add, ":item_no", readable_books_begin, ":count"),
			(is_between, ":item_no", readable_books_begin, readable_books_end),
			(store_item_kind_count, ":on_hand", ":item_no", "$g_talk_troop"),
			(ge, ":on_hand", 1),
			# See if we've done any reading on it so far.
			(store_sub, ":companion_no", "$g_talk_troop", companions_begin),
			(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
			(item_get_slot, reg21, ":item_no", ":book_read_slot"),
			# Store data for display.
			(str_store_item_name, s21, ":item_no"),
			(try_begin),
				(ge, reg21, 1),
				(val_div, reg21, 10),
				(str_store_string, s22, "@ ({reg21}% progress)"),
			(else_try),
				(str_clear, s22),
			(try_end),
		],
		"{s21}{s22}", "advisor_development_reading_book_selected",
		[
			(store_repeat_object, ":count"),
			(val_sub, ":count", 1), # Since we don't start at 0.
			(store_add, ":item_no", readable_books_begin, ":count"),
			(assign, "$temp", ":item_no"),
		]],
	
	[anyone|plyr, "advisor_development_reading_book_list",
		[],
		"That's it.", "advisor_development",
		[]],
	
	[anyone, "advisor_development_reading_book_selected",
		[
			## WINDYPLAINS+ ## - Bugfix #1604 - Prevent an advisor from reading a book more than once.
			(store_sub, ":companion_no", "$g_talk_troop", companions_begin),
			(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
			(item_get_slot, reg21, "$temp", ":book_read_slot"),
			(lt, reg21, 1000),
			## WINDYPLAINS- ##
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			(str_store_item_name, s23, "$temp"),
		],
		"I'll begin reading {s23} at once{s66}.", "advisor_development",
		[
			(call_script, "script_change_troop_reading_book", "$g_talk_troop", "$temp"),
		]],
	
	[anyone, "advisor_development_reading_book_selected",
		[
			## WINDYPLAINS+ ## - Bugfix #1604 - Prevent an advisor from reading a book more than once.
			# (store_sub, ":companion_no", "$g_talk_troop", companions_begin),
			# (store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
			# (item_get_slot, reg21, ":item_no", ":book_read_slot"),
			# (ge, reg21, 1000),
			## WINDYPLAINS- ##
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 1),
			(str_store_item_name, s23, "$temp"),
		],
		"{s66}, I am already familiar with {s23}.  Perhaps a different book would be appropriate.", "advisor_development",
		[]],
	## Switch Reading : End ##
	
	## Trade Books : Begin ##
	[anyone|plyr, "advisor_development_reading_topics",
		[],
		"I want to exchange books with you.", "advisor_development",
		[
			(change_screen_loot, "$g_talk_troop"),
			# Check to see if a book needs to be removed.
			(troop_get_slot, ":current_book", "$g_talk_troop", slot_troop_reading_book),
			(try_begin),
				(is_between, ":current_book", readable_books_begin, readable_books_end),
				(store_item_kind_count, ":book_count", ":current_book", "$g_talk_troop"),
				(eq, ":book_count", 0),
				(call_script, "script_change_troop_reading_book", "$g_talk_troop", REMOVE_BOOK),
			(try_end),
		]],
	## Trade Books : End ##
	
	[anyone|plyr, "advisor_development_reading_topics",
		[],
		"Let's talk about something else.", "advisor_development",
		[]],
	
	## BOOK READING : END ##
	
	[anyone|plyr, "advisor_development_topics",
		[],
		"Never mind.", "advisor_development_exit",
		[]],
	
	# Kick out to the Castle Steward dialog.
	[anyone, "advisor_development_exit",
		[
			(party_slot_eq, "$current_town", slot_center_steward, "$g_talk_troop"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"That was very insightful{s66}.  Thank you.", "advisor_steward_pretalk",
		[]],
	
	# Kick out to the Captain of the Guard dialog.
	[anyone, "advisor_development_exit",
		[
			(party_slot_eq, "$current_town", slot_center_advisor_war, "$g_talk_troop"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"That was very insightful{s66}.  Thank you.", "advisor_war_pretalk",
		[]],
	
	# ERROR - No advisor dialog specified to go to.
	[anyone, "advisor_development_exit",
		[
			(party_get_slot, ":advisor_steward", "$current_town", slot_center_steward),
			(party_get_slot, ":advisor_war", "$current_town", slot_center_advisor_war),
			(try_begin),
				(is_between, ":advisor_steward", companions_begin, companions_end),
				(str_store_troop_name, s21, ":advisor_steward"),
			(else_try),
				(str_store_string, s21, "@Unassigned"),
			(try_end),
			(try_begin),
				(is_between, ":advisor_war", companions_begin, companions_end),
				(str_store_troop_name, s22, ":advisor_war"),
			(else_try),
				(str_store_string, s22, "@Unassigned"),
			(try_end),
			(str_store_troop_name, s23, "$g_talk_troop"),
		],
		"Well this is embarassing.  I'm not sure where next to go in this conversation.^^Currently speaking to {s23}.^Castle Steward is {s21}^Captain of the Guard is {s22}.^^Please screenshot this and submit a bug ticket.", "close_window",
		[]],
	
	################ ADVISOR DEVELOPMENT : END ###################
	
	################ TREASURY : BEGIN ###################
	[anyone|plyr, "advisor_war_talk",
		[],
		"Let's discuss how you use treasury funds.", "advisor_war_treasury_talk",
		[]],
	
	[anyone, "advisor_war_treasury_talk",
		[
			(party_get_slot, reg20, "$current_town", slot_center_income_to_treasury),
			(party_get_slot, reg21, "$current_town", slot_center_recruiting),
			(party_get_slot, reg22, "$current_town", slot_center_upgrade_garrison),
			(store_sub, reg23, reg20, 1),
			(party_get_slot, reg24, "$current_town", slot_center_treasury),
			(store_sub, reg25, reg24, 1),
			(str_store_party_name, s21, "$current_town"),
		],
		"I've been utilizing the {s21} treasury as follows:^^Garrison recruitment is {reg21?active:disabled}^^Garrison training is {reg22?active:disabled}^^Treasury income is {reg20} denar{reg23?s:} per week.^^The treasury current holds {reg24} denar{reg25?s:}.", "advisor_war_treasury_topic",
		[]],
	
	# [anyone, "advisor_war_treasury_pretalk",
		# [(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		# "Is there anything else you would like to know{s66}?", "advisor_war_treasury_topic",
		# []],
	
	[anyone|plyr, "advisor_war_treasury_topic",
		[
			(store_troop_gold, ":gold", "trp_player"),
			(try_begin),
				(ge, ":gold", 500),
				(assign, "$temp", 500),
			(else_try),
				(ge, ":gold", 100),
				(assign, "$temp", 100),
			(else_try),
				(assign, "$temp", ":gold"),
			(try_end),
			(assign, reg1, "$temp"),
		],
		"Deposit {reg1} denars into the treasury.", "advisor_war_treasury_talk",
		[
			(call_script, "script_diplomacy_treasury_deposit_funds", "$temp", "$current_town"),
		]],
	
	[anyone|plyr, "advisor_war_treasury_topic",
		[
			(party_slot_ge, "$current_town", slot_center_treasury, 1),
			(party_get_slot, ":gold", "$current_town", slot_center_treasury),
			(try_begin),
				(ge, ":gold", 500),
				(assign, "$temp", 500),
			(else_try),
				(ge, ":gold", 100),
				(assign, "$temp", 100),
			(else_try),
				(assign, "$temp", ":gold"),
			(try_end),
			(assign, reg1, "$temp"),
		],
		"Withdraw {reg1} denars from the treasury.", "advisor_war_treasury_talk",
		[
			(call_script, "script_diplomacy_treasury_withdraw_funds", "$temp", "$current_town", FUND_FROM_TREASURY_TO_PLAYER),
		]],
	
	[anyone|plyr, "advisor_war_treasury_topic",
		[],
		"Increase treasury allocation by 250 denars per week.", "advisor_war_treasury_talk",
		[
			(party_get_slot, reg1, "$current_town", slot_center_income_to_treasury),
			(val_add, reg1, 250),
			(party_set_slot, "$current_town", slot_center_income_to_treasury, reg1),
		]],
	
	[anyone|plyr, "advisor_war_treasury_topic",
		[
			(party_slot_ge, "$current_town", slot_center_income_to_treasury, 1),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_income_to_treasury, 250),
				(assign, reg1, 250),
			(else_try),
				(party_get_slot, reg1, "$current_town", slot_center_income_to_treasury),
			(try_end),
			(store_sub, reg2, reg1, 1),
		],
		"Reduce treasury allocation by {reg1} denar{reg2?s:} per week.", "advisor_war_treasury_talk",
		[
			(party_get_slot, reg1, "$current_town", slot_center_income_to_treasury),
			(val_sub, reg1, 250),
			(val_max, reg1, 0),
			(party_set_slot, "$current_town", slot_center_income_to_treasury, reg1),
		]],
	
	[anyone|plyr, "advisor_war_treasury_topic",
		[],	"Nevermind.", "advisor_war_pretalk", []],
	
	################ TREASURY : END ###################
	
	################ PATROL SYSTEM : BEGIN ###################
	
	[anyone|plyr, "advisor_war_talk",
		[],
		"I want to discuss the status of our patrols.", "advisor_war_patrol_talk",
		[]],
	
	[anyone, "advisor_war_patrol_talk",
		[
			(call_script, "script_diplomacy_patrol_functions", "$current_town", PATROL_RESET_CENTER_SLOTS),
			(assign, ":count", 0),
			(assign, ":cost", 0),
			(try_for_range, ":slot_no", slot_center_patrols_begin, slot_center_patrols_end),
				(party_slot_ge, "$current_town", ":slot_no", 1),
				(party_get_slot, ":party_no", "$current_town", ":slot_no"),
				(val_add, ":count", 1),
				(call_script, "script_diplomacy_patrol_functions", ":party_no", PATROL_DETERMINE_COST),
				(val_add, ":cost", reg1),
			(try_end),
			(str_store_party_name, s21, "$current_town"),
			(assign, reg24, ":count"),
			(store_sub, reg22, ":count", 1),
			(assign, reg23, ":cost"),
			(try_begin),
				(ge, ":count", 1),
				(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
				(str_store_string, s22, "@Currently {s21} is supporting {reg24} patrol{reg22?:s} in the area at a total cost of {reg23} denars per week.  I have received {reg22?a:several} status report{reg22?:s} available for your review{s66}."),
			(else_try),
				(str_store_string, s22, "@Currently we have no patrols designated.  I think it would be good for the prosperity of the area if we considered adding one or two.  Banditry can cause havoc to our local economy if the villagers cannot safely travel here."),
			(try_end),
		],
		"{s22}", "advisor_war_patrol_topic",
		[]],
	
	[anyone, "advisor_war_patrol_pretalk",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"Is there anything else you would like to know{s66}?", "advisor_war_patrol_topic",
		[]],
	
	## REQUEST ADVISOR INQUIRE ABOUT PATROLS - BEGIN ##
	# Tell advisor to return to the player's party.
	[anyone|plyr, "advisor_war_patrol_topic",
		[
			# Don't display this dialog option unless a valid patrol exists.
			(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_1, 1),
			(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
			(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
		],
		"Give me a report on the status of our patrols.", "advisor_war_patrol_status_1",
		[
			(assign, "$temp", -1),
			(assign, "$temp_2", -1),
			(assign, "$temp_3", -1),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_patrol_party_1, 1),
				(party_get_slot, "$temp", "$current_town", slot_center_patrol_party_1),
			(else_try),
				(party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
				(party_get_slot, "$temp", "$current_town", slot_center_patrol_party_2),
			(else_try),
				(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
				(party_get_slot, "$temp", "$current_town", slot_center_patrol_party_3),
			(try_end),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
				(party_get_slot, "$temp_2", "$current_town", slot_center_patrol_party_2),
			(else_try),
				(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
				(party_get_slot, "$temp_2", "$current_town", slot_center_patrol_party_3),
			(try_end),
			(try_begin),
				(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
				(party_get_slot, "$temp_3", "$current_town", slot_center_patrol_party_3),
			(try_end),
			
		]],
	
	[anyone, "advisor_war_patrol_status_1",
		[
			(ge, "$temp_2", 1),
			(str_clear, s29),
			(call_script, "script_diplomacy_patrol_functions", "$temp", PATROL_REPORT_STATUS),
		],
		"{s21}", "advisor_war_patrol_status_2",
		[]],
	
	[anyone, "advisor_war_patrol_status_1",
		[
			(eq, "$temp_2", -1),
			(str_clear, s29),
			(call_script, "script_diplomacy_patrol_functions", "$temp", PATROL_REPORT_STATUS),
		],
		"{s21}", "advisor_war_patrol_pretalk",
		[]],
	
	[anyone, "advisor_war_patrol_status_2",
		[
			(ge, "$temp_3", 1),
			(str_clear, s29),
			(call_script, "script_diplomacy_patrol_functions", "$temp_2", PATROL_REPORT_STATUS),
		],
		"{s21}", "advisor_war_patrol_status_3",
		[]],
	
	[anyone, "advisor_war_patrol_status_2",
		[
			(eq, "$temp_3", -1),
			(str_clear, s29),
			(call_script, "script_diplomacy_patrol_functions", "$temp_2", PATROL_REPORT_STATUS),
		],
		"{s21}", "advisor_war_patrol_pretalk",
		[]],
	
	[anyone, "advisor_war_patrol_status_3",
		[
			(str_clear, s29),
			(call_script, "script_diplomacy_patrol_functions", "$temp_3", PATROL_REPORT_STATUS),
		],
		"{s21}", "advisor_war_patrol_pretalk",
		[]],
	## REQUEST ADVISOR INQUIRE ABOUT PATROLS - END ##
	
	## REQUEST ADVISOR HIRE NEW PATROL - BEGIN ##
	# Tell advisor to return to the player's party.
	[anyone|plyr, "advisor_war_patrol_topic",
		[
			# Don't display this dialog option unless there is room for another patrol.
			(this_or_next|party_slot_eq, "$current_town", slot_center_patrol_party_1, 0),
			(this_or_next|party_slot_eq, "$current_town", slot_center_patrol_party_2, 0),
			(party_slot_eq, "$current_town", slot_center_patrol_party_3, 0),
		],
		"I want you to setup a patrol for the region.", "advisor_war_hire_patrol_1",
		[]],
	
	[anyone, "advisor_war_hire_patrol_1",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"We could always use more men keeping the lands safe for our subjects{s66}.  How large of a patrol did you wish?", "advisor_war_hire_patrol_size",
		[]],
	
	# Patrol Size Selection - begin
	[anyone|plyr, "advisor_war_hire_patrol_size",
		[
			(call_script, "script_diplomacy_determine_patrol_size", "$current_town", patrol_size_small),
		],
		"A small patrol of {reg1} soldiers.", "advisor_war_hire_patrol_training",
		[
			(assign, "$temp", patrol_size_small),
		]],
	
	[anyone|plyr, "advisor_war_hire_patrol_size",
		[
			(call_script, "script_diplomacy_determine_patrol_size", "$current_town", patrol_size_medium),
		],
		"An average patrol of {reg1} soldiers.", "advisor_war_hire_patrol_training",
		[
			(assign, "$temp", patrol_size_medium),
		]],
	
	[anyone|plyr, "advisor_war_hire_patrol_size",
		[
			(call_script, "script_diplomacy_determine_patrol_size", "$current_town", patrol_size_large),
		],
		"A large patrol of {reg1} soldiers.", "advisor_war_hire_patrol_training",
		[
			(assign, "$temp", patrol_size_large),
		]],
	
	[anyone|plyr, "advisor_war_hire_patrol_size",
		[],
		"Let's just forget about this.", "advisor_war_patrol_pretalk",
		[]],
	# Patrol Size Selection - End
	
	# Patrol Training Selection - Begin
	[anyone, "advisor_war_hire_patrol_training",
		[],
		"And how well would you like these soldiers equipped and trained?  If we provide them more funding then they will be more effective.", "advisor_war_hire_patrol_training_choice",
		[]],
	
	[anyone|plyr, "advisor_war_hire_patrol_training_choice",
		[], "I just need men on the lookout.  Keep the expenses small.", "advisor_war_hire_patrol_commission",
		[
			(assign, "$temp_2", patrol_training_poor),
		]],
	
	[anyone|plyr, "advisor_war_hire_patrol_training_choice",
		[], "Do your best to keep the costs reasonable, but we need competent soldiers.", "advisor_war_hire_patrol_commission",
		[
			(assign, "$temp_2", patrol_training_average),
		]],
	
	[anyone|plyr, "advisor_war_hire_patrol_training_choice",
		[], "Make sure they are well equipped and seasoned soldiers.", "advisor_war_hire_patrol_commission",
		[
			(assign, "$temp_2", patrol_training_good),
		]],
	
	[anyone|plyr, "advisor_war_hire_patrol_training_choice",
		[], "Spare no expense.  I want bandits fleeing for the hills when this party comes around.", "advisor_war_hire_patrol_commission",
		[
			(assign, "$temp_2", patrol_training_elite),
		]],
	
	[anyone|plyr, "advisor_war_hire_patrol_training_choice",
		[],
		"Let's just forget about this.", "advisor_war_patrol_pretalk",
		[]],
	# Patrol Training Selection - End
	
	# Patrol Confirmation - Begin
	[anyone, "advisor_war_hire_patrol_commission",
		[
			(call_script, "script_diplomacy_patrol_functions", "$current_town", PATROL_GET_SUMMARY),
			(assign, ":cost", reg21),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			(assign, reg21, ":cost"), # Prevents the previous script call from overwriting our cost.
		],
		"Very good{s66}.  I shall gather the men immediately assuming I have your instructions right?^^Patrol Size = {s21}^Patrol Strength = {s22}^^This patrol will cost us {reg21} denars per week to maintain.", "advisor_war_hire_patrol_commission_confirm",
		[]],
	
	[anyone|plyr, "advisor_war_hire_patrol_commission_confirm",
		[],
		"That's correct.  See to it personally.", "advisor_war_hire_patrol_commission_confirmed",
		[]],
	
	[anyone|plyr, "advisor_war_hire_patrol_commission_confirm",
		[],
		"Let's just forget about this.", "advisor_war_patrol_pretalk",
		[]],
	
	[anyone, "advisor_war_hire_patrol_commission_confirmed",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"It shall be as you asked{s66}.", "advisor_war_patrol_pretalk",
		[
			(call_script, "script_diplomacy_patrol_functions", "$current_town", PATROL_GENERATE),
		]],
	# Patrol Confirmation - End
	## REQUEST ADVISOR HIRE NEW PATROL - END ##
	
	## REQUEST ADVISOR DISBAND PATROL - BEGIN ##
	# Tell advisor to return to the player's party.
	[anyone|plyr, "advisor_war_patrol_topic",
		[
			# Don't display this dialog option unless the center has a patrol.
			(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_1, 1),
			(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
			(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
		],
		"I want to disband one of our patrols.", "advisor_war_disband_patrol",
		[]],
	
	[anyone, "advisor_war_disband_patrol",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"As you wish{s66}.  Which patrol did you want me to have disbanded?", "advisor_war_disband_patrol_selection",
		[]],
	
	[anyone|plyr, "advisor_war_disband_patrol_selection",
		[
			(party_slot_ge, "$current_town", slot_center_patrol_party_1, 1), # Ensure a patrol exists in this slot.
			(party_get_slot, ":patrol_party", "$current_town", slot_center_patrol_party_1),
			(call_script, "script_diplomacy_patrol_functions", ":patrol_party", PATROL_GET_SUMMARY), # s21 (size), s22 (training), reg21 (cost)
		],
		"Patrol #1 - A {s21} of {s22} costing {reg21} denars.", "advisor_war_disband_patrol_confirmed",
		[
			(assign, reg23, slot_center_patrol_party_1),
		]],
	
	[anyone|plyr, "advisor_war_disband_patrol_selection",
		[
			(party_slot_ge, "$current_town", slot_center_patrol_party_2, 1), # Ensure a patrol exists in this slot.
			(party_get_slot, ":patrol_party", "$current_town", slot_center_patrol_party_2),
			(call_script, "script_diplomacy_patrol_functions", ":patrol_party", PATROL_GET_SUMMARY), # s21 (size), s22 (training), reg21 (cost)
		],
		"Patrol #2 - A {s21} of {s22} costing {reg21} denars.", "advisor_war_disband_patrol_confirmed",
		[
			(assign, reg23, slot_center_patrol_party_2),
		]],
	
	[anyone|plyr, "advisor_war_disband_patrol_selection",
		[
			(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1), # Ensure a patrol exists in this slot.
			(party_get_slot, ":patrol_party", "$current_town", slot_center_patrol_party_3),
			(call_script, "script_diplomacy_patrol_functions", ":patrol_party", PATROL_GET_SUMMARY), # s21 (size), s22 (training), reg21 (cost)
		],
		"Patrol #3 - A {s21} of {s22} costing {reg21} denars.", "advisor_war_disband_patrol_confirmed",
		[
			(assign, reg23, slot_center_patrol_party_3),
		]],
	
	[anyone|plyr, "advisor_war_disband_patrol_selection",
		[],	"Never mind.", "advisor_war_patrol_pretalk",
		[]],
	
	[anyone, "advisor_war_disband_patrol_confirmed",
		[
			(store_sub, reg22, reg23, slot_center_patrols_begin),
			(val_add, reg22, 1),
		],
		"I will have patrol #{reg22} disbanded immediately.", "advisor_war_patrol_pretalk",
		[
			(party_get_slot, ":patrol_party", "$current_town", reg23),
			(call_script, "script_diplomacy_patrol_functions", ":patrol_party", PATROL_DISBAND),
		]],
	
	
	## REQUEST ADVISOR DISBAND PATROL - END ##
	
	# Exit dialog.
	[anyone|plyr, "advisor_war_patrol_topic",
		[],
		"That is all.", "advisor_war_pretalk",
		[]],
		
	################ PATROL SYSTEM : END ###################
	
	################ RECRUITMENT & UPGRADING SYSTEM : BEGIN ###################
	
	# ## GARRISON RECRUITMENT : BEGIN ##
	# # Tell advisor to return to the player's party.
	# [anyone|plyr, "advisor_war_talk",
		# [],
		# "Give me a report on the status of our defenses.", "advisor_war_garrison_talk",
		# []],
	
	# [anyone, "advisor_war_garrison_talk",
		# [
			# # Determine commentary on garrison size.
			# (party_get_num_companions, reg21, "$current_town"),
			# (str_store_party_name, s22, "$current_town"),
			# (try_begin),
				# (ge, reg21, 300),
				# (assign, ":garrison_strength", 4),
				# (str_store_string, s21, "@our garrison currently houses {reg21} soldiers which should prove adequate when the time comes to defend the keep"),
			# (else_try),
				# (ge, reg21, 200),
				# (assign, ":garrison_strength", 3),
				# (str_store_string, s21, "@with the {reg21} soldiers we currently have in the garrison we should be able to defend the keep, but I'd feel better if we brought in more recruits"),
			# (else_try),
				# (ge, reg21, 100),
				# (assign, ":garrison_strength", 2),
				# (str_store_string, s21, "@we have roughly {reg21} soldiers available to protect your interests here, but beyond stalling an invading force I can't guarantee they'd be able to hold it without help"),
			# (else_try),
				# (ge, reg21, 25),
				# (assign, ":garrison_strength", 1),
				# (str_store_string, s21, "@we have fine defenses here in {s22}, but we lack the soldiers to defend it.  We are in dire need of more troops to be stationed here unless we wish to leave the keep as easy pickings."),
			# (else_try),
				# ## Default ##
				# (assign, ":garrison_strength", 0),
				# (str_store_string, s21, "@our defenses are non-existent.  Unless we conscript more soldiers to man the walls here even if only enough to hold off an sieging army until help arrives then I fear {s22} will be an easy target."),
			# (try_end),
			
			# # Determine commentary on recruiting efforts.
			
			# (try_begin),
				# (party_slot_eq, "$current_town", slot_center_recruiting, 0), # We're NOT recruiting.
				# (ge, ":garrison_strength", 3),
				# (str_store_string, s23, "@Currently we have no resources devoted to active recruiting."),
			# (else_try),
				# (party_slot_eq, "$current_town", slot_center_recruiting, 0), # We're NOT recruiting.
				# (ge, ":garrison_strength", 2),
				# (str_store_string, s23, "@Right now we're devoting nothing to finding new soldiers and I think that would be a mistake if not changed."),
			# (else_try),
				# (party_slot_eq, "$current_town", slot_center_recruiting, 0), # We're NOT recruiting.
				# (str_store_string, s23, "@Furthermore, I am deeply concerned that we are not spending any of our limited resources on recruiting."),
			# (else_try),
				# (party_slot_eq, "$current_town", slot_center_recruiting, 1), # We're currently recruiting.
				# (str_store_string, s23, "@I am relieved, however, that you have authorized spending some of our treasury on finding new soldiers and I have guards in the field seeing that it is done."),
				# (try_begin),
					# (party_slot_ge, "$current_town", slot_center_recruit_pool, 1),
					# (party_get_slot, reg23, "$current_town", slot_center_recruit_pool),
					# (str_store_string, s23, "@{s23}  Currently we have {reg23} new recruits from the nearby villages that I have yet to meet with."),
				# (try_end),
			# (try_end),
			
			# # Determine commentary on training efforts.
			
			# (call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		# ],
		# "Well{s66}, {s21}.  {s23}", "advisor_war_garrison_topics",
		# []],
	
	# [anyone, "advisor_war_garrison_pretalk",
		# [],
		# "Is there anything else about our defenses you'd like to discuss?", "advisor_war_garrison_topics",
		# []],
	
	# [anyone|plyr, "advisor_war_garrison_topics",
		# [(party_slot_eq, "$current_town", slot_center_recruiting, 0),],
		# "We need more soldiers to man the walls.", "advisor_war_recruiting_activate",
		# []],
	
	# [anyone, "advisor_war_recruiting_activate",
		# [
			# (try_begin),
				# (eq, "$diplomacy_force_recruit_enabled", 1), # Make sure we're even using this game option.
				# (store_faction_of_party, ":faction_no", "$current_town"),
				# (faction_slot_eq, ":faction_no", slot_faction_decree_conscription, 1), # Ensure conscription decree is active.
				# (str_store_string, s21, "@  With our edict for conscription in place we should be able to secure plenty of recruits."),
			# (else_try),
				# (str_clear, s21),
			# (try_end),
			# (call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		# ],
		# "Yes{s66}.  I have guards seek out recruits among the townsfolk and send word to our nearby settlements.{s21}  I estimate this will cost us roughly 500 denars per week.", "advisor_war_garrison_pretalk",
		# [
			# (party_set_slot, "$current_town", slot_center_recruiting, 1),
		# ]],
	
	# [anyone|plyr, "advisor_war_garrison_topics",
		# [(neg|party_slot_eq, "$current_town", slot_center_recruiting, 0),],
		# "I want you to stop recruiting for now.", "advisor_war_recruiting_deactivate",
		# []],
	
	# [anyone, "advisor_war_recruiting_deactivate",
		# [(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		# "As you command{s66}.  I'll send word to have our recruiters in the field recalled.", "advisor_war_garrison_pretalk",
		# [
			# (party_set_slot, "$current_town", slot_center_recruiting, 0),
		# ]],
	
	# ## GARRISON RECRUITMENT : END ##
	
	# ## GARRISON UPGRADING : BEGIN ##
	# [anyone|plyr, "advisor_war_garrison_topics",
		# [(ge, DEBUG_DIPLOMACY, 1),],
		# "(DEBUG: 1) Reboot troop upgrade chances.", "advisor_war_garrison_pretalk",
		# [
			# (try_for_range, ":troop_no", 1, "trp_end_of_troops"),
				# (neg|troop_is_hero, ":troop_no"),
				# (call_script, "script_diplomacy_initialize_troop_upgrade_options", ":troop_no"),
			# (try_end),
		# ]],
	
	# # Activate / de-activate garrison upgrading.
	# [anyone|plyr, "advisor_war_garrison_topics",
		# [(party_slot_eq, "$current_town", slot_center_upgrade_garrison, 0),],
		# "I want you to begin training our recruits.", "advisor_war_training_activate",
		# []],
	
	# [anyone, "advisor_war_training_activate",
		# [(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		# "Yes{s66}.  I must caution you that such training may be costly.  There are the blacksmiths and tailors to pay for new equipment, farriers to care for horses and surgeons to care for the men that are injured during the training period.  These costs are variable depending upon the troop, but I'll see everything is taken care of if you wish to proceed?", "advisor_war_training_activate_1",
		# []],
	
	# [anyone|plyr, "advisor_war_training_activate_1",
		# [],	"Yes, see that is done.", "advisor_war_garrison_pretalk",
		# [(party_set_slot, "$current_town", slot_center_upgrade_garrison, 1),]],
	
	# [anyone|plyr, "advisor_war_training_activate_1",
		# [],	"I need to think about this before continuing.", "advisor_war_garrison_pretalk", []],
	
	# [anyone|plyr, "advisor_war_garrison_topics",
		# [(party_slot_eq, "$current_town", slot_center_upgrade_garrison, 1),], 
		# "I want you to stop training our recruits.", "advisor_war_garrison_pretalk",
		# [(party_set_slot, "$current_town", slot_center_upgrade_garrison, 0),]],
	
	# # Setup how upgrades will be handled.
	# [anyone|plyr, "advisor_war_garrison_topics",
		# [],
		# "I'd like to discuss how I want you to train troops.", "advisor_war_training_setup",
		# []],
	
	# [anyone, "advisor_war_training_setup",
		# [(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		# "Which class of soldier would you like to discuss training options for{s66}?", "advisor_war_training_list",
		# []],
	
	# [anyone|plyr|repeat_for_100, "advisor_war_training_list",
		# [
			# (store_repeat_object, ":count"),
			# (val_sub, ":count", 1), # Since repeat begins with 1.
			# # Determine which troop this should refer to.
			# (party_get_slot, ":culture", "$current_town", slot_center_culture),
			# (faction_get_slot, ":recruit_troop", ":culture", slot_faction_tier_1_troop),
			# (store_add, ":troop_no", ":recruit_troop", ":count"),
			# # Block the test holder troop for the player's custom tree.
			# (neq, ":troop_no", "trp_test_holder"),
			# (is_between, ":troop_no", "trp_tournament_participants", "trp_end_of_troops"), # Prevent out of bounds invalid troop errors.
			# # Make sure this troop matches the faction of the town.
			# (store_faction_of_party, ":faction_center", "$current_town"),
			# (store_troop_faction, ":faction_troop", ":troop_no"),
			# # Find out what faction we're emulating incase the player is basing their kingdom on another faction's culture.
			# (assign, ":emulated_faction", "fac_player_supporters_faction"),
			# (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
				# (faction_slot_eq, ":kingdom_no", slot_faction_culture, ":culture"),
				# (assign, ":emulated_faction", ":kingdom_no"),
			# (try_end),
			# (this_or_next|eq, ":faction_center", ":faction_troop"),
			# (eq, ":faction_troop", ":emulated_faction"),
			# # Determine if this troop has a valid upgrade option or block it if not.
			# (troop_get_upgrade_troop, ":path_1", ":troop_no", 0),
			# (troop_get_upgrade_troop, ":path_2", ":troop_no", 1),
			# (this_or_next|neq, ":path_1", 0),
			# (neq, ":path_2", 0),
			# # TODO: Script to determine and display "tier" of soldier.
			# (call_script, "script_diplomacy_determine_troop_tier", ":troop_no"),
			# (str_store_string, s22, "@[Tier {reg1}]"),
			# (str_store_troop_name, s21, ":troop_no"),
			# (try_begin),
				# (ge, DEBUG_DIPLOMACY, 1),
				# (assign, reg31, ":path_1"),
				# (assign, reg32, ":path_2"),
				# (str_store_string, s31, "@ [{reg31}, {reg32}]"),
			# (else_try),
				# (str_clear, s31),
			# (try_end),
		# ],
		# "{s22} {s21}{s31}", "advisor_war_training_list_pick",
		# [
			# (store_repeat_object, ":count"),
			# (val_sub, ":count", 1), # Since repeat begins with 1.
			# (party_get_slot, ":culture", "$current_town", slot_center_culture),
			# (faction_get_slot, ":recruit_troop", ":culture", slot_faction_tier_1_troop),
			# (store_add, ":troop_no", ":recruit_troop", ":count"),
			# (assign, "$temp", ":troop_no"),
		# ]],
	
	# [anyone|plyr, "advisor_war_training_list",
		# [],
		# "Never mind.", "advisor_war_garrison_pretalk",
		# []],
	
	# [anyone, "advisor_war_training_list_pick",
		# [
			# (assign, ":troop_no", "$temp"),
			# (str_store_troop_name, s21, ":troop_no"),
			# # Learn information about the troop.
			# (call_script, "script_diplomacy_describe_troop_to_s2", ":troop_no"),
			# (str_store_string, s20, s2),
			
			# # Get information about upgrade path 1.
			# (troop_get_upgrade_troop, ":path_1", ":troop_no", 0),
			# (try_begin),
				# (neq, ":path_1", 0),
				# (str_store_troop_name, s24, ":path_1"),
				# (troop_get_slot, reg21, ":troop_no", slot_troop_upgrade_chance_1),
				# (call_script, "script_game_get_upgrade_cost", ":path_1"),
				# (assign, reg22, reg0),
				# (call_script, "script_diplomacy_describe_troop_to_s2", ":path_1"),
				# (str_store_string, s22, "@^^{s24} ({reg21}% chance)^{s2}^Costs {reg22} denars"),
			# (else_try),
				# (str_clear, s22),
			# (try_end),
			
			# # Get information about upgrade path 2.
			# (troop_get_upgrade_troop, ":path_2", ":troop_no", 1),
			# (try_begin),
				# (neq, ":path_2", 0),
				# (str_store_troop_name, s24, ":path_2"),
				# (troop_get_slot, reg21, ":troop_no", slot_troop_upgrade_chance_2),
				# (call_script, "script_game_get_upgrade_cost", ":path_2"),
				# (assign, reg22, reg0),
				# (call_script, "script_diplomacy_describe_troop_to_s2", ":path_2"),
				# (str_store_string, s23, "@^^{s24} ({reg21}% chance)^{s2}^Costs {reg22} denars"),
			# (else_try),
				# (str_clear, s23),
			# (try_end),
			
			# (try_begin),
				# (str_clear, s25),
				# (str_equals, s22, s25),
				# (str_equals, s23, s25),
				# (str_store_string, s25, "@^^This soldier has no upgrade options."),
			# (else_try),
				# (this_or_next|str_equals, s22, s25),
				# (str_equals, s23, s25),
				# (str_store_string, s25, "@^^Upgrade Path:^-------------------------------------------"),
			# (else_try),
				# (str_store_string, s25, "@^^Upgrade Paths:^-------------------------------------------"),
			# (try_end),
			# (call_script, "script_diplomacy_determine_troop_tier", ":troop_no"),
		# ],
		# "{s21} [Tier {reg1}]^{s20}{s25}{s22}{s23}", "advisor_war_training_troop_options",
		# []],
	
	# [anyone|plyr, "advisor_war_training_troop_options",
		# [
			# (assign, ":troop_no", "$temp"),
			# # Determine if this troop has a valid upgrade option or block it if not.
			# (troop_get_upgrade_troop, ":path_1", ":troop_no", 0),
			# (troop_get_upgrade_troop, ":path_2", ":troop_no", 1),
			# (this_or_next|neq, ":path_1", 0),
			# (neq, ":path_2", 0),
		# ],
		# "Adjust this troop's training options", "advisor_war_training_troop_setup",
		# []],
	
	# [anyone, "advisor_war_training_troop_setup",
		# [],
		# "How would you like me to split my training efforts for this soldier?^^Note: Click the upgrade path you wish to shift increments by 5%.", "advisor_war_training_troop_setup_options",
		# []],
	
	# [anyone|plyr, "advisor_war_training_troop_setup_options",
		# [
			# (assign, ":troop_no", "$temp"),
			# (troop_get_upgrade_troop, ":upgrade_troop", ":troop_no", 0),
			# (neq, ":upgrade_troop", 0),
			# (str_store_troop_name, s21, ":upgrade_troop"),
			# (troop_get_slot, reg21, ":troop_no", slot_troop_upgrade_chance_1),
		# ],
		# "Focus more towards {s21}. ({reg21}% chance)", "advisor_war_training_troop_setup",
		# [
			# (assign, ":troop_no", "$temp"),
			# (troop_get_slot, ":upgrade_1", ":troop_no", slot_troop_upgrade_chance_1),
			# (troop_get_slot, ":upgrade_2", ":troop_no", slot_troop_upgrade_chance_2),
			# (val_add, ":upgrade_1", 5),
			# (val_sub, ":upgrade_2", 5),
			# (val_clamp, ":upgrade_1", 0, 101),
			# (val_clamp, ":upgrade_2", 0, 101),
			# (troop_set_slot, ":troop_no", slot_troop_upgrade_chance_1, ":upgrade_1"),
			# (troop_set_slot, ":troop_no", slot_troop_upgrade_chance_2, ":upgrade_2"),
		# ]],
	
	# [anyone|plyr, "advisor_war_training_troop_setup_options",
		# [
			# (assign, ":troop_no", "$temp"),
			# (troop_get_upgrade_troop, ":upgrade_troop", ":troop_no", 1),
			# (neq, ":upgrade_troop", 0),
			# (str_store_troop_name, s21, ":upgrade_troop"),
			# (troop_get_slot, reg21, ":troop_no", slot_troop_upgrade_chance_2),
		# ],
		# "Focus more towards {s21}. ({reg21}% chance)", "advisor_war_training_troop_setup",
		# [
			# (assign, ":troop_no", "$temp"),
			# (troop_get_slot, ":upgrade_1", ":troop_no", slot_troop_upgrade_chance_1),
			# (troop_get_slot, ":upgrade_2", ":troop_no", slot_troop_upgrade_chance_2),
			# (val_add, ":upgrade_2", 5),
			# (val_sub, ":upgrade_1", 5),
			# (val_clamp, ":upgrade_1", 0, 101),
			# (val_clamp, ":upgrade_2", 0, 101),
			# (troop_set_slot, ":troop_no", slot_troop_upgrade_chance_1, ":upgrade_1"),
			# (troop_set_slot, ":troop_no", slot_troop_upgrade_chance_2, ":upgrade_2"),
		# ]],
	
	# [anyone|plyr, "advisor_war_training_troop_setup_options",
		# [],
		# "Go back to this soldier's training report.", "advisor_war_training_list_pick",
		# []],
	
	# [anyone|plyr, "advisor_war_training_troop_options",
		# [
			# (assign, ":troop_no", "$temp"),
			# (troop_get_upgrade_troop, ":upgrade_troop", ":troop_no", 0),
			# (neq, ":upgrade_troop", 0),
			# (str_store_troop_name, s21, ":upgrade_troop"),
			# (troop_get_slot, reg21, ":troop_no", slot_troop_upgrade_chance_1),
		# ],
		# "Go to {s21}'s training. ({reg21}% chance)", "advisor_war_training_list_pick",
		# [
			# (assign, ":troop_no", "$temp"),
			# (troop_get_upgrade_troop, "$temp", ":troop_no", 0),
		# ]],
	
	# [anyone|plyr, "advisor_war_training_troop_options",
		# [
			# (assign, ":troop_no", "$temp"),
			# (troop_get_upgrade_troop, ":upgrade_troop", ":troop_no", 1),
			# (neq, ":upgrade_troop", 0),
			# (str_store_troop_name, s21, ":upgrade_troop"),
			# (troop_get_slot, reg21, ":troop_no", slot_troop_upgrade_chance_2),
		# ],
		# "Go to {s21}'s training. ({reg21}% chance)", "advisor_war_training_list_pick",
		# [
			# (assign, ":troop_no", "$temp"),
			# (troop_get_upgrade_troop, "$temp", ":troop_no", 1),
		# ]],
	
	# [anyone|plyr, "advisor_war_training_troop_options",
		# [],
		# "Return to troop list.", "advisor_war_training_setup",
		# []],
	
	# [anyone|plyr, "advisor_war_training_troop_options",
		# [],
		# "Let's talk about something else.", "advisor_war_garrison_pretalk",
		# []],
	
	# # Explain how the upgrading system works.
	# [anyone|plyr, "advisor_war_garrison_topics",
		# [],
		# "Explain to me about how you can train troops.", "advisor_war_upgrading_info",
		# []],
	
	# [anyone, "advisor_war_upgrading_info",
		# [],
		# "Certainly.  The overall process must first be turned on to have any effect.  Each troop that can upgrade has a default chance of 100% (if only one upgrade exists) and 50% each (for two options).  These default values can be changed by going to that troop's info screen and adjusting them.", "advisor_war_upgrading_info_2",
		# []],
	
	# [anyone, "advisor_war_upgrading_info_2",
		# [],
		# "Once you're happy with the upgrade chance for each troop then you'll need to setup some way to pay for their training.  You can do this by either making a one time payment into the treasury that I'll use until it runs out or have me divert some of the town's income towards training instead of sending it to you.", "advisor_war_garrison_pretalk",
		# []],
	
	## GARRISON UPGRADING : END ##
	
	# [anyone|plyr, "advisor_war_garrison_topics",
		# [],	"Never mind.", "advisor_war_pretalk", []],
	
	################ RECRUITMENT & UPGRADING SYSTEM : END ###################
	
	## REQUEST ADVISOR RETIRE - BEGIN ##
	# Tell advisor to return to the player's party.
	[anyone|plyr, "advisor_war_talk",
		[],
		"I wish for you to return to my company.", "advisor_war_return_to_group",
		[]],
	   
	[anyone, "advisor_war_return_to_group",
		[
			(store_sub, ":advisor_no", slot_center_advisor_war, advisors_begin),
			(store_add, ":string_no", ":advisor_no", "str_diplomacy_advisor_steward"),
			(str_store_string, s21, ":string_no"),
			(try_begin),
				# Don't display this dialog option unless the center has a patrol.
				(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_1, 1),
				(this_or_next|party_slot_ge, "$current_town", slot_center_patrol_party_2, 1),
				(party_slot_ge, "$current_town", slot_center_patrol_party_3, 1),
				(str_store_string, s22, "@  Without my guidance our patrols here will be disbanded in my absence."),
			(else_try),
				(str_clear, s22),
			(try_end),
		],
		"You want me to leave my role as {s21} and return to your service?{s22}", "advisor_war_return_confirm",
		[]],

	[anyone|plyr, "advisor_war_return_confirm",
		[],
		"Yes, I have need of your services.", "close_window",
		[
			# Remove any currently assigned advisor.
			(call_script, "script_diplomacy_remove_advisor", "$g_encountered_party", slot_center_advisor_war, ADVISOR_RETURNS_TO_PARTY),
		]],
	   
	[anyone|plyr, "advisor_war_return_confirm",
		[],
		"No, remain at your post.", "advisor_war_pretalk",
		[]],
	## REQUEST ADVISOR RETIRE - END ##

	# Exit dialog.
	[anyone|plyr, "advisor_war_talk",
		[],
		"That is all.", "close_window",
		[]],
###############################################
##### ADVISOR: CAPTAIN OF THE GUARD : END #####
###############################################
]

###########################################
##### ADVISOR: CASTLE STEWARD : BEGIN #####
###########################################
advisor_steward_dialogs = [

	# Opening dialog.
	[anyone, "start",
		[
			(party_slot_eq, "$g_encountered_party", slot_center_steward, "$g_talk_troop"),
			(try_begin),
				(is_currently_night),
				(assign, reg21, 1),
			(else_try),
				(assign, reg21, 0),
			(try_end),
			(str_store_party_name, s21, "$current_town"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"Good {reg21?evening:day}{s66}.  I trust your journey to {s21} was without incident.  How may I be of service?  ", "advisor_steward_talk",
		[]],
	   
	[anyone, "advisor_steward_pretalk",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"Is there anything else I can do to help you{s66}?", "advisor_steward_talk",
		[]],
	
	################ ADVISOR DEVELOPMENT : BEGIN ###################
	[anyone|plyr,"advisor_steward_talk", [], "I'd like to discuss your development.", "advisor_development",[]],
	# Rest of development dialog is maintained within the Captain of the Guard section.
	################ ADVISOR DEVELOPMENT : END ###################
	
	## REQUEST ADVISOR'S ADVICE - BEGIN ##
	[anyone|plyr, "advisor_steward_talk",
		[
			(party_get_slot, ":castle_type", "$current_town", slot_party_type),
			(try_begin),
				(eq, ":castle_type", spt_town),
				(assign, reg21, 1),
			(else_try),
				(assign, reg21, 0),
			(try_end),
		],
		"Do you have any recommendations regarding the {reg21?town:castle}?", "advisor_steward_get_advice",
		[]],
	
	[anyone, "advisor_steward_get_advice",
		[
			(party_slot_eq, "$g_encountered_party", slot_center_steward, "$g_talk_troop"),
			(call_script, "script_diplomacy_store_steward_advice_to_s0"),
		],
		"{s0}", "advisor_steward_pretalk",
		[]],
	## REQUEST ADVISOR'S ADVICE - END ##
	
	## REQUEST ADVISOR CENTER IMPROVEMENTS - BEGIN ##
	[anyone|plyr, "advisor_steward_talk",
		[],
		"Tell me about the current state of construction here.", "advisor_steward_construction",
		[]],
	
	[anyone, "advisor_steward_construction",
		[
			# List the things being built here.
			(try_begin),
				(str_clear, s21),
				(this_or_next|party_slot_ge, "$g_encountered_party", slot_center_current_improvement_1, 1),
				(this_or_next|party_slot_ge, "$g_encountered_party", slot_center_current_improvement_2, 1),
				(party_slot_ge, "$g_encountered_party", slot_center_current_improvement_3, 1),

				(str_store_string, s21, "@We are currently working on:"),
				(try_for_range, ":improvement_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
					(try_begin),
						(party_get_slot, ":cur_improvement", "$g_encountered_party", ":improvement_slot"),
						(gt, ":cur_improvement", 0),
						(call_script, "script_get_improvement_details", ":cur_improvement"),
						(str_store_string, s7, s0),
						(store_current_hours, ":cur_hours"),
						(store_add, ":end_time_slot", ":improvement_slot", 3),
						(party_get_slot, ":finish_time", "$g_encountered_party", ":end_time_slot"),
						(val_sub, ":finish_time", ":cur_hours"),
						(store_div, reg8, ":finish_time", 24),
						(val_max, reg8, 1),
						(store_sub, reg9, reg8, 1),
						(try_begin),
							(party_slot_ge, "$g_encountered_party", ":cur_improvement", cis_built),
							(assign, reg21, 1),
						(else_try),
							(assign, reg21, 0),
						(try_end),
						(str_store_string, s21, "@{s21}^^{reg21?Repairing the:Building a} {s7} will need another {reg8} day{reg9?s:} to complete this task."),
					(try_end),
				(try_end),
			(try_end),
			
		],
		"{s21}", "advisor_steward_construction_state",
		[]],

	# CANCEL a current project.
	[anyone|plyr, "advisor_steward_construction_state",
		[
			(party_slot_ge, "$g_encountered_party", slot_center_current_improvement_1, 1),
			(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_1),
			(call_script, "script_get_improvement_details", ":improvement"),
		],
		"I want the work on the {s0} ended.", "advisor_steward_construction_cancel",
		[
			(assign, "$temp", slot_center_current_improvement_1),
		]],

	# CANCEL a current project.
	[anyone|plyr, "advisor_steward_construction_state",
		[
			(party_slot_ge, "$g_encountered_party", slot_center_current_improvement_2, 1),
			(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_2),
			(call_script, "script_get_improvement_details", ":improvement"),
		],
		"I want the work on the {s0} ended.", "advisor_steward_construction_cancel",
		[
			(assign, "$temp", slot_center_current_improvement_2),
		]],

	# CANCEL a current project.
	[anyone|plyr, "advisor_steward_construction_state",
		[
			(party_slot_ge, "$g_encountered_party", slot_center_current_improvement_3, 1),
			(party_get_slot, ":improvement", "$g_encountered_party", slot_center_current_improvement_3),
			(call_script, "script_get_improvement_details", ":improvement"),
		],
		"I want the work on the {s0} ended.", "advisor_steward_construction_cancel",
		[
			(assign, "$temp", slot_center_current_improvement_3),
		]],

	# BUILD/REPAIR a project.
	[anyone|plyr|repeat_for_100, "advisor_steward_construction_state",
		[
			(store_repeat_object, ":counter"),
			(store_add, ":improvement_slot", native_improvements_begin, ":counter"),
			(is_between, ":improvement_slot", native_improvements_begin, native_improvements_end),
			(call_script, "script_cf_improvement_can_be_built_here", "$g_encountered_party", ":improvement_slot"),
			(neg|party_slot_eq, "$g_encountered_party", ":improvement_slot", cis_built),
			(try_begin),
				(party_slot_ge, "$g_encountered_party", ":improvement_slot", cis_built),
				(assign, reg21, 0),
			(else_try),
				(assign, reg21, 1),
			(try_end),
			(call_script, "script_get_improvement_details", ":improvement_slot"),
		],
		"I wish to {reg21?build {s2}:repair the {s0}}.", "advisor_steward_construction_build",
		[
			(store_repeat_object, ":counter"),
			(store_add, ":improvement", native_improvements_begin, ":counter"),
			
			(call_script, "script_get_improvement_details", ":improvement"),
			# (assign, ":improvement_cost", reg0),
			
			(call_script, "script_improvement_get_building_time_and_cost", "$current_town", ":improvement"),
			(assign, "$temp", ":improvement"),
			(assign, "$temp_2", reg1), # Improvement Cost
			(assign, "$temp_3", reg2), # Build Time
		]],
		
	# BUILD/REPAIR a project.
	[anyone|plyr|repeat_for_100, "advisor_steward_construction_state",
		[
			(store_repeat_object, ":counter"),
			(store_add, ":improvement_slot", center_improvements_begin, ":counter"),
			(is_between, ":improvement_slot", center_improvements_begin, center_improvements_end),
			(call_script, "script_cf_improvement_can_be_built_here", "$g_encountered_party", ":improvement_slot"),
			(neg|party_slot_eq, "$g_encountered_party", ":improvement_slot", cis_built),
			(try_begin),
				(party_slot_ge, "$g_encountered_party", ":improvement_slot", cis_built),
				(assign, reg21, 0),
			(else_try),
				(assign, reg21, 1),
			(try_end),
			(call_script, "script_get_improvement_details", ":improvement_slot"),
		],
		"I wish to {reg21?build {s2}:repair the {s0}}.", "advisor_steward_construction_build",
		[
			(store_repeat_object, ":counter"),
			(store_add, ":improvement", center_improvements_begin, ":counter"),
			
			(call_script, "script_get_improvement_details", ":improvement"),
			# (assign, ":improvement_cost", reg0),
			
			(call_script, "script_improvement_get_building_time_and_cost", "$current_town", ":improvement"),
			(assign, "$temp", ":improvement"),
			(assign, "$temp_2", reg1), # Improvement Cost
			(assign, "$temp_3", reg2), # Build Time
		]],

	# Confirm building an improvement.
	[anyone, "advisor_steward_construction_build",
		[
			(call_script, "script_get_improvement_details", "$temp"),
			(assign, reg21, "$temp_3"),
			(assign, reg22, "$temp_2"),
		],
		"{s1}^^Building a {s0} will likely take {reg21} days and cost us {reg22} denars.  Are you sure you wish to do this?", "advisor_steward_construction_build_confirm",
		[]],
		
	[anyone|plyr, "advisor_steward_construction_build_confirm",
		[],
		"Yes, make it so.", "advisor_steward_construction_build_confirmed",
		[
			(assign, ":improvement", "$temp"),
			(assign, ":improvement_cost", "$temp_2"),
			(assign, ":improvement_time", "$temp_3"),
			(store_troop_gold, ":cur_gold", "trp_player"),
			(ge, ":cur_gold", ":improvement_cost"),
			(troop_remove_gold, "trp_player", ":improvement_cost"),
			(assign, ":continue", 1),
			(try_for_range, ":improvement_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
				(eq, ":continue", 1),
				(party_slot_eq, "$g_encountered_party", ":improvement_slot", 0), # Nothing currently being built in this slot.
				(assign, ":continue", 0),
				(party_set_slot, "$g_encountered_party", ":improvement_slot", ":improvement"),
				(store_current_hours, ":cur_hours"),
				(store_mul, ":hours_takes", ":improvement_time", 24),
				(val_add, ":hours_takes", ":cur_hours"),
				(store_add, ":end_time_slot", ":improvement_slot", 3),
				(party_set_slot, "$g_encountered_party", ":end_time_slot", ":hours_takes"),
			(try_end),
			(call_script, "script_improvement_apply_special_cost", ":improvement"),
		]],
	
	[anyone|plyr, "advisor_steward_construction_build_confirmed",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"Very well{s66}.  I shall have work begun immediately.", "advisor_steward_pretalk",
		[]],
	
	[anyone|plyr, "advisor_steward_construction_build_confirm",[],"No, let's discuss something else.", "advisor_steward_pretalk",[]],

	[anyone, "advisor_steward_construction_cancel",
		[
			(party_get_slot, ":improvement", "$g_encountered_party", "$temp"),
			(call_script, "script_get_improvement_details", ":improvement"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"You are certain you wish to end work on the {s0}{s66}?", "advisor_steward_construction_cancel_confirm",
		[]],

	[anyone|plyr, "advisor_steward_construction_cancel_confirm",
		[],
		"Yes, I have other uses for our workers.", "advisor_steward_construction_cancel_confirmed",
		[]],
	
	[anyone|plyr, "advisor_steward_construction_cancel_confirm",
		[],
		"No, let the men continue their work.", "advisor_steward_pretalk",
		[]],

	[anyone, "advisor_steward_construction_cancel_confirmed",
		[
			(party_get_slot, ":improvement", "$g_encountered_party", "$temp"),
			(call_script, "script_get_improvement_details", ":improvement"),
		],
		"I shall recall the workers on the {s0} project immediately, my {Lord/lady}.", "advisor_steward_pretalk",
		[
			(party_get_slot, ":improvement", "$g_encountered_party", "$temp"),
			(call_script, "script_get_improvement_details", ":improvement"),
			(party_set_slot, "$g_encountered_party", "$temp", 0),
			(store_sub, ":offset", slot_center_improvement_end_hour_1, slot_center_current_improvement_1),
			(store_add, ":end_hour_slot", "$temp", ":offset"),
			(party_set_slot, "$g_encountered_party", ":end_hour_slot", 0),
		]],

	[anyone|plyr, "advisor_steward_construction_state",
		[],
		"Let us discuss something else.", "advisor_steward_pretalk",
		[]],

	## REQUEST ADVISOR CENTER IMPROVEMENTS - END ##

	## HOSTING A TOURNAMENT - BEGIN ##
	[anyone|plyr, "advisor_steward_talk",
		[
			(party_slot_eq, "$current_town", slot_party_type, spt_town),
			(party_slot_eq, "$current_town", slot_town_has_tournament, 0),
		],
		"I would like to host a tournament.", "advisor_steward_host_tourney_1",
		[]],
	
	[anyone, "advisor_steward_host_tourney_1",
		[
			(call_script, "script_cf_diplomacy_treasury_verify_funds", DIPLOMACY_TOURNAMENT_HOSTING_COST, "$current_town", FUND_FROM_EITHER, TREASURY_FUNDS_AVAILABLE),
			(assign, reg21, DIPLOMACY_TOURNAMENT_HOSTING_COST),
		],
		"The townsfolk would certainly be pleased if we were to host games here, but in order to make the proper preparations I would need {reg21} denars.  This would go to cover the prizes paid out to the winners and to spread word of the games to ensure attendance is high.", "advisor_steward_host_tourney_2",
		[]],
	
	[anyone, "advisor_steward_host_tourney_1",
		[
			(call_script, "script_cf_diplomacy_treasury_verify_funds", DIPLOMACY_TOURNAMENT_HOSTING_COST, "$current_town", FUND_FROM_EITHER, TREASURY_FUNDS_INSUFFICIENT),
			(assign, reg21, DIPLOMACY_TOURNAMENT_HOSTING_COST),
		],
		"While it would certainly raise morale within the town, I fear we do not have the necessary funds within the treasury to make such an event successful.  As a minimum for preparations, I would need {reg21} denars to cover the prizes for the winners and pay runners to spread word of the games.", "advisor_steward_pretalk",
		[]],
	
	[anyone, "advisor_steward_host_tourney_2",
		[], "This would go to cover the prizes paid out to the winners and to spread word of the games to ensure attendance is high.  Additionally, we would need to prepare invitations for other lords and provide for a feast worthy of your station.  Is this acceptable?", "advisor_steward_host_tourney_3",
		[]],
	
	[anyone|plyr, "advisor_steward_host_tourney_3",
		[], "Yes, draw whatever funds are needed.", "advisor_steward_host_tourney_4", 
		[
			# Improve player relation with the town as a minimum benefit.
			(call_script, "script_change_player_relation_with_center", "$current_town", 3),
			# Withdraw player funds.
			(call_script, "script_diplomacy_treasury_withdraw_funds", DIPLOMACY_TOURNAMENT_HOSTING_COST, "$current_town", FUND_FROM_EITHER),
		]],
	
	[anyone|plyr, "advisor_steward_host_tourney_3",
		[], "No, we can't afford that right now.", "advisor_steward_pretalk", []],
	
	[anyone, "advisor_steward_host_tourney_4",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"Yes{s66}.  I shall make the necessary preparations.", "advisor_steward_pretalk",
		[
			# Take money from the player.
			
			# Initiate the tournament.
			(party_set_slot, "$current_town", slot_town_has_tournament, 3),
		]],
	## HOSTING A TOURNAMENT - END ##
	
	## REQUEST ADVISOR RETIRE - BEGIN ##
	# Tell advisor to return to the player's party.
	[anyone|plyr, "advisor_steward_talk",
		[],
		"I wish for you to return to my company.", "advisor_steward_return_to_group",
		[]],
	   
	[anyone, "advisor_steward_return_to_group",
		[
			(store_sub, ":advisor_no", slot_center_steward, advisors_begin),
			(store_add, ":string_no", ":advisor_no", "str_diplomacy_advisor_steward"),
			(str_store_string, s21, ":string_no"),
		],
		"You want me to leave my role as {s21} and return to your service?", "advisor_steward_return_confirm",
		[]],

	[anyone|plyr, "advisor_steward_return_confirm",
		[],
		"Yes, I have need of your services.", "close_window",
		[
			# Remove any currently assigned advisor.
			(call_script, "script_diplomacy_remove_advisor", "$g_encountered_party", slot_center_steward, ADVISOR_RETURNS_TO_PARTY),
		]],
	   
	[anyone|plyr, "advisor_steward_return_confirm",
		[],
		"No, remain at your post.", "advisor_steward_pretalk",
		[]],
	## REQUEST ADVISOR RETIRE - END ##

	# Exit dialog.
	[anyone|plyr, "advisor_steward_talk",
		[],
		"That is all.", "close_window",
		[]],
#########################################
##### ADVISOR: CASTLE STEWARD : END #####
#########################################
]

############################
##### MINISTER : BEGIN #####
############################
minister_talk_addon = [

## WINDYPLAINS+ ## - Allow minister to change player faction culture.
	[anyone|plyr, "minister_talk",
	   [],
	   "I wish to change our culture.", "player_culture_change_1",
	   []],
	
	[anyone, "player_culture_change_1",
	   [],
	   "I see, {Sir/my Lady}, but what should we base it upon?", "player_culture_change_2",
	   []],
	
	[anyone|plyr|repeat_for_factions, "player_culture_change_2",
	   [
			(store_repeat_object, ":faction_no"),
			(is_between, ":faction_no", kingdoms_begin, kingdoms_end),
			(try_begin),
				(eq, ":faction_no", "fac_player_supporters_faction"),
				(str_store_string, s22, "@We should break tradition and create our own way."),
			(else_try),
				(str_store_faction_name, s21, ":faction_no"),
				(str_store_string, s22, "@We should emulate the {s21}."),
			(try_end),
			
	   ],
	   "{s22}", "player_culture_change_3",
	   [
			(store_repeat_object, "$temp"),
	   ]],
	
	[anyone|plyr, "player_culture_change_2",
	   [],
	   "Never mind.", "minister_pretalk",
	   []],
	
	[anyone, "player_culture_change_3",
	   [],
	   "Very well, I will make the necessary preparations and announcements.", "minister_pretalk",
	   [
			(assign, ":faction_no", "$temp"),
			(try_begin),
				(eq, ":faction_no", "fac_player_supporters_faction"),
				(assign, ":culture", "fac_culture_player"),
			(else_try),
				(faction_get_slot, ":culture", ":faction_no",  slot_faction_culture),
			(try_end),
			
			(faction_set_slot, "fac_player_supporters_faction",  slot_faction_culture, ":culture"),
			(faction_set_slot, "fac_player_faction",  slot_faction_culture, ":culture"),
				
			# Change centers to match.
			(try_for_range, ":center_no", centers_begin, centers_end),
				(store_faction_of_party, ":faction_check", ":center_no"),
				(eq, ":faction_check", "$players_kingdom"),
				(party_set_slot, ":center_no", slot_center_culture, ":culture"),
				##
				# (str_store_party_name, s31, ":center_no"),
				# (str_store_faction_name, s32, ":culture"),
				# (display_message, "@DEBUG: {s31} culture set to {s32}.", gpu_debug),
			(try_end),
	   ]],
	## WINDYPLAINS- ##
	
	## WINDYPLAINS+ ## - Hiring a new advisor.
	[anyone|plyr, "minister_talk",
		[],
		"I wish to appoint an advisor.", "advisor_appoint_1",
		[]],
	
	[anyone, "advisor_appoint_1",
		[],
		"Very good, my {King/Queen}.  Where do we wish to make this appointment?", "advisor_appoint_2",
		[]],
	
	[anyone|plyr|repeat_for_parties, "advisor_appoint_2",
		[
			(store_repeat_object, ":center_no"),
			(is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(str_store_party_name, s21, ":center_no"),
			(assign, reg21, 0),
			(try_for_range, ":advisor_slot", advisors_begin, advisors_end),
				(party_slot_ge, ":center_no", ":advisor_slot", 1),
				(val_add, reg21, 1),
			(try_end),
			(str_clear, s22),
			(try_begin),
				(ge, reg21, 1),
				(str_store_string, s22, "@  ({reg21} advisors present)"),
			(try_end),
		],
		"In {s21}.{s22}", "advisor_appoint_3",
		[(store_repeat_object, "$temp"),]],
	
	[anyone|plyr, "advisor_appoint_2",
		[],
		"Never mind.", "minister_pretalk",
		[]],
	
	[anyone, "advisor_appoint_3",
		[
			(assign, reg21, 0),
			(try_for_range, ":advisor_slot", advisors_begin, advisors_end),
				(party_slot_ge, "$temp", ":advisor_slot", 1),
				(val_add, reg21, 1),
			(try_end),
			(try_begin),
				(ge, reg21, 1),
				(store_sub, reg22, reg21, 1),
				(str_store_string, s22, "@{reg21} advisor{reg22?s:}.  What position do you wish to appoint a new advisor to or did you wish to replace someone?"),
			(else_try),
				(str_store_string, s22, "@no advisors appointed.  What appointment did you wish to make?"),
			(try_end),
			(str_store_party_name, s21, "$temp"),
		],
		"Currently in {s21} we have {s22}.", "advisor_appoint_4",
		[]],
	
	[anyone|plyr|repeat_for_100, "advisor_appoint_4",
		[
			(store_repeat_object, ":counter"),
			(store_add, ":slot_no", advisors_begin, ":counter"),
			(is_between, ":slot_no", advisors_begin, advisors_end),
			(store_add, ":string_no", "str_diplomacy_advisor_steward", ":counter"),
			(str_store_string, s21, ":string_no"),
			(try_begin),
				(party_slot_eq, "$temp", ":slot_no", 0),
				(str_store_string, s22, "@appoint a"),
				(str_clear, s23),
			(else_try),
				(str_store_string, s22, "@replace my"),
				(party_get_slot, ":advisor", "$temp", ":slot_no"),
				(str_store_troop_name, s24, ":advisor"),
				(str_store_string, s23, "@  (Currently: {s24})"),
			(try_end),
		],
		"I wish to {s22} {s21}.{s23}", "advisor_appoint_5",
		[(store_repeat_object, ":counter"),
		(store_add, "$temp_2", advisors_begin, ":counter"),]],
	
	[anyone|plyr, "advisor_appoint_4",
		[],
		"Let's discuss a different location.", "advisor_appoint_1",
		[]],
	
	[anyone|plyr, "advisor_appoint_4",
		[],
		"Never mind.", "minister_pretalk",
		[]],
	
	[anyone, "advisor_appoint_5",
		[
			(try_begin),
				(party_slot_ge, "$temp", "$temp_2", 1),
				(party_get_slot, ":advisor", "$temp", "$temp_2"),
				(str_store_troop_name, s23, ":advisor"),
				(troop_get_type, reg22, ":advisor"),
				(str_store_string, s22, "@currently filled by {s23}.  Who did you wish to replace {reg22?her:him} with?"),
			(else_try),
				(str_store_string, s22, "@vacant.  Who would you like to appoint?"),
			(try_end),
			(store_sub, ":advisor_no", "$temp_2", advisors_begin),
			(store_add, ":string_no", ":advisor_no", "str_diplomacy_advisor_steward"),
			(str_store_string, s21, ":string_no"),
		],
		"The position of {s21} is {s22}", "advisor_appoint_6",
		[]],
	
	[anyone|plyr|repeat_for_troops, "advisor_appoint_6",
		[
			(store_repeat_object, ":troop_no"),
			(is_between, ":troop_no", companions_begin, companions_end),
			(main_party_has_troop, ":troop_no"),
			(str_store_troop_name, s21, ":troop_no"),
		],
		"I wish to appoint {s21}.", "advisor_appoint_7",
		[
			(store_repeat_object, "$temp_3"),
		]],
	
	# [anyone|plyr|repeat_for_troops, "ransom_companion_list",
		# [
			# (store_repeat_object, ":troop_no"),
			# (is_between, ":troop_no", companions_begin, companions_end),
			# (neg|main_party_has_troop, ":troop_no"),
			# ## Has met the player, joined his band and since been separated.
			# (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, pp_history_scattered),
			# (str_store_troop_name, s21, ":troop_no"),
		# ],
		# "I wish to ransom {s21}.", "ransom_companion_confirm",
		# [
			# (store_repeat_object, "$temp_3"),
		# ]],
		
	[anyone|plyr, "advisor_appoint_6",
		[],
		"Let's discuss advisor roles again.", "advisor_appoint_3",
		[]],
	
	[anyone|plyr, "advisor_appoint_6",
		[],
		"Nevermind.", "minister_pretalk",
		[]],
	
	[anyone, "advisor_appoint_7",
		[
			# Name the position.
			(store_sub, ":advisor_no", "$temp_2", advisors_begin),
			(store_add, ":string_no", ":advisor_no", "str_diplomacy_advisor_steward"),
			(str_store_string, s24, ":string_no"),
			# Name the person.
			(str_store_troop_name, s22, "$temp_3"),
			# Name the location.
			(str_store_party_name, s23, "$temp"),
		],
		"Very well, my {King/Queen}.  {s22} shall become the new {s24} in {s23}.", "minister_pretalk",
		[
			# Remove any currently assigned advisor.
			(call_script, "script_diplomacy_remove_advisor", "$temp", "$temp_2", ADVISOR_RETURN_IF_NEARBY),			
			# Remove the new advisor from the player's party.
			(party_remove_members, "p_main_party", "$temp_3", 1),
			(str_store_troop_name, s22, "$temp_3"),
			(display_message, "@{s22} has left the party.", gpu_light_blue),
			# Assign the new advisor to the castle.
			(party_set_slot, "$temp", "$temp_2", "$temp_3"),
			(troop_set_slot, "$temp_3", slot_troop_advisor_station, "$temp"),
			(troop_set_slot, "$temp_3", slot_troop_advisor_role, "$temp_2"),
			# COMPANION ROLES:
			(try_begin),
				## ROLE: STOREKEEPER ##
				(eq, "$cms_role_storekeeper", "$temp_3"),
				(call_script, "script_cms_replace_troop_with_troop_in_role", "$temp_3", "trp_player", ROLE_STOREKEEPER),
			(else_try),
				## ROLE: JAILER ##
				(eq, "$cms_role_jailer", "$temp_3"),
				(call_script, "script_cms_replace_troop_with_troop_in_role", "$temp_3", "trp_player", ROLE_JAILER),
			(else_try),
				## ROLE: QUARTERMASTER ##
				(eq, "$cms_role_quartermaster", "$temp_3"),
				(call_script, "script_cms_replace_troop_with_troop_in_role", "$temp_3", "trp_player", ROLE_QUARTERMASTER),
			(try_end),
		]],
	## WINDYPLAINS- ##
##########################
##### MINISTER : END #####
##########################
]

minister_talk_addon2 = [
	## RELIQUISH OWNERSHIP OF THE FIEF - BEGIN ##
	# Request the Castle Steward to pack everything up and give up ownership of the fief.
	[anyone|plyr, "minister_talk",
		[(str_store_party_name, s21, "$current_town"),],
		"I want to relinquish ownership of a fief.", "minister_giving_up_fief",
		[]],
	
	[anyone, "minister_giving_up_fief",
		[],	"Which fief do you wish to give up?", "minister_giving_up_fief_1",
		[]],
	
	[anyone|plyr|repeat_for_parties, "minister_giving_up_fief_1",
		[
			(store_repeat_object, ":center_no"),
			(is_between, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(str_store_party_name, s21, ":center_no"),
		],
		"I want to give up {s21}.", "minister_giving_up_fief_2",
		[(store_repeat_object, "$temp"),]],
		
	[anyone|plyr, "minister_giving_up_fief_1",
		[],	"Never mind.", "minister_pretalk",[]],
		
	[anyone, "minister_giving_up_fief_2",
		[
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
			(str_store_party_name, s21, "$temp"),
		],
		"You're sure that you want to reliquish control of {s21}{s66}?", "minister_giving_up_fief_confirm",
		[]],
	
	[anyone|plyr, "minister_giving_up_fief_confirm",
		[],
		"Yes.", "close_window",
		[
			# Remove any assigned advisors.
			(try_for_range, ":advisor_slot", advisors_begin, advisors_end),
				(call_script, "script_diplomacy_remove_advisor", "$temp", ":advisor_slot", ADVISOR_RETURN_IF_NEARBY),
			(try_end),
			# Reliquish control of the town.
			(party_set_slot, "$temp", slot_town_lord, stl_unassigned),
		]],
	
	[anyone|plyr, "minister_giving_up_fief_confirm",
		[],
		"No.  I still need to think about this.", "minister_pretalk",
		[]],
	
	## RELIQUISH OWNERSHIP OF THE FIEF - END ##
]


lord_talk_addon	= [   
	

]

ransom_broker_talk_addon = [

  ## WINDYPLAINS+ ## - Allow ransom broker to by all prisoners at once via dialog.
  [anyone|plyr,"ransom_broker_talk",
   [[store_num_regular_prisoners,reg(0)],[ge,reg(0),1]],
   "I would like to sell all of the prisoners that I have with me.", "ransom_broker_sell_all_prisoners_1", []],
  
  [anyone,"ransom_broker_sell_all_prisoners_1",
   [
		(party_get_num_prisoner_stacks, ":stack_limit", "p_main_party"),
		(assign, reg21, 0),
		(try_for_range, ":stack_no", 0, ":stack_limit"),
			(party_prisoner_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_no"),
			(neg|troop_is_hero, ":troop_no"), # Prevent companions, lords & player from being counted.
			(party_prisoner_stack_get_size, ":troop_count", "p_main_party", ":stack_no"),
			(call_script, "script_game_get_prisoner_price", ":troop_no"),
			(assign, ":troop_value", reg0),
			(store_mul, ":stack_value", ":troop_value", ":troop_count"),
			(val_add, reg21, ":stack_value"),
		(try_end),
   ],
   "I can arrange that.  I will give you {reg21} denars for the lot.  Do we have an agreement?", "ransom_broker_sell_all_prisoners_2", []],
  
  [anyone|plyr,"ransom_broker_sell_all_prisoners_2",
	[], "That is acceptable.", "close_window", 
	[
		(assign, "$g_move_heroes", 0),
		(call_script, "script_party_remove_all_prisoners", "p_main_party"),
		(call_script, "script_troop_add_gold", "trp_player", reg21),
	]],
  
  [anyone|plyr,"ransom_broker_sell_all_prisoners_2",
   [], "No, I'll take my prisoners elsewhere.", "close_window", []],
  ## WINDYPLAINS- ##
  
]

prisoner_talk_addon	= [   
  ## WINDYPLAINS+ ## - Specific dialog for speaking to a king that is prisoner to force peace.
  [anyone|plyr,"prisoner_chat", 
	[
		(store_conversation_troop, "$g_talk_troop"),
		(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(str_store_troop_name, s21, "$g_talk_troop"),
		(store_current_hours, "$g_current_hours"),
		# Reseting these variables since prisoner_chat does get initialized like most dialogs.
		(troop_get_slot, "$g_talk_troop_last_talk_time", "$g_talk_troop", slot_troop_last_talk_time),
		(troop_set_slot, "$g_talk_troop", slot_troop_last_talk_time, "$g_current_hours"),
		(store_sub, "$g_time_since_last_talk","$g_current_hours","$g_talk_troop_last_talk_time"),
		# Get prisoner's faction.
		(store_troop_faction, "$g_talk_troop_faction", "$g_talk_troop"),
	], 
	"{s21}, it is time we spoke, wouldn't you agree?", "prisoner_pretalk",
	[
		# Initialize some variables for options.
		(assign, reg39, 0), # Tracks if the party Jailer is assigned and present.
		(assign, reg40, 0), # Ransoming a prisoner.
		(assign, reg41, 0), # Forcing a king to make peace.
		(assign, reg42, 0), # Recruiting a prisoner.
		(assign, reg43, 0), # Convincing a captive vassal to bring a message of peace.
		(try_begin),
			(neq, "$cms_role_jailer", "trp_player"),
			(main_party_has_troop, "$cms_role_jailer"),
			(assign, reg39, 1),
		(try_end),
	]],
  
  [anyone,"prisoner_pretalk", [], "Well {sir/madam}, I am at your mercy, so what did you want to say?", "prisoner_talk",[]],
  
  # [anyone,"prisoner_subject_transition", [], "Is there anything else?", "prisoner_talk",[]],
  
  # ######################################################
  # ### RELEASING A VASSAL TO CARRY A REQUEST OF PEACE ###
  # ######################################################
  
  # # Requires: Prisoner is a lord.
  # [anyone|plyr,"prisoner_talk", 
	# [
		# (faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
		# (is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		# (troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_kingdom_hero),
		# # Prevent this option from showing up again.
		# (eq, reg43, 0),
	# ], 
	# "I have a mission for you.", "prisoner_discuss_tasks",
	# []],
	
  # [anyone,"prisoner_discuss_tasks", 
	# [
		# (assign, reg43, 1),
		# (call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
	# ], 
	# "What is it you want of me{s66}?", "prisoner_olive_branch_a1",
	# []],
	
  # [anyone|plyr,"prisoner_olive_branch_a1", 
	# [
		# (store_troop_faction, ":faction_no", "$g_talk_troop"),
		# (faction_get_slot, ":troop_no", ":faction_no", slot_faction_leader),
		# (str_store_troop_name, s21, ":troop_no"),
		# (troop_get_type, reg21, ":troop_no"),
	# ], "I see no reason to continue this war with your people, but your ruler has chosen to ignore messages I have sent {reg21?her:him}.  If on your word of honor you will agree to convince {s21} that peace between our people is within our mutual interest then I will release you without ransom.", "prisoner_olive_branch_a2",
	# []],
	
  # [anyone,"prisoner_olive_branch_a2", 
	# [
		# (call_script, "script_troop_get_player_relation", "$g_talk_troop"),
		# (assign, ":relation", reg0),
		# (this_or_next|lt, ":relation", -20),
		# (this_or_next|troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_quarrelsome),
		# (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_debauched),
	# ], "And spoil the fun our common folk would get from seeing your head on a pike?  I think not.", "prisoner_olive_branch_a2",
	# []],
	
	
  # # Cunning lords will look for payment.
  # [anyone,"prisoner_olive_branch_a2", 
	# [
		# (troop_slot_eq, "$g_talk_troop", slot_lord_reputation_type, lrep_cunning),
	# ], "I have no love of being your guest, but I will need traveling money if I am to make the journey back.", "prisoner_olive_branch_b1",
	# []],
	
  # [anyone|plyr,"prisoner_olive_branch_b1", 
	# [], "How much did you have in mind?", "prisoner_olive_branch_b2", []],
	
  # [anyone,"prisoner_olive_branch_b2", 
	# [
		# (store_troop_faction, ":faction_no", "$g_talk_troop"),
		# (faction_get_slot, ":troop_no", ":faction_no", slot_faction_leader),
		# (str_store_troop_name, s21, ":troop_no"),
	# ], "I'll need at least 3000 denars.  After all of this time on the road I prefer a few comforts on the way home, but worry not your coin will buy my words at the {s21}'s ear.", "prisoner_olive_branch_b3", []],
  
  # [anyone|plyr,"prisoner_olive_branch_b3", 
	# [
		# (store_troop_gold, ":cash", "trp_player"),
		# (ge, ":cash", 3000),
	# ], "Very well.  See that it does.  I shall see to your traveling expenses.", "prisoner_olive_branch_b2", 
	# [
		# (troop_remove_gold, "trp_player", 3000),
		# (play_sound, "snd_money_received"),
		# (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 5, 0),
		# ## TODO: Start the timer for seeing if peace is pursued.
		# ## TODO: Release prisoner.
	# ]],
	
  # [anyone|plyr,"prisoner_olive_branch_b3", 
	# [], "I think you need a little more time to consider my proposal instead.", "close_window", 
	# [
		# (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -2, 0),
	# ]],
  
  # # Default - Lord Accepts
  # # Cunning lords will look for payment.
  # [anyone,"prisoner_olive_branch_a2", 
	# [
		# (call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		# (store_troop_faction, ":faction_no", "$g_talk_troop"),
		# (faction_get_slot, ":troop_no", ":faction_no", slot_faction_leader),
		# (str_store_troop_name, s21, ":troop_no"),
	# ], "My freedom for my counsel?  Remaining your captive does me no good so I will honor your request{s66}.  I expect that you will refrain from further hostilities while I bring this offer before {s21} otherwise I can make no promises to how well my words will be received.", "prisoner_olive_branch_c1",
	# []],
	
  # [anyone|plyr,"prisoner_olive_branch_c1", 
	# [], "You have my word.  I will not trespass any further into the lands of your people.", "close_window", 
	# [
		# (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", 3, 0),
		# ## TODO: Start the timer for seeing if peace is pursued.
		# ## TODO: Release prisoner.
	# ]],
  
  # [anyone|plyr,"prisoner_olive_branch_c1", 
	# [], "I can make no such promises.  Just do as I have asked and the fighting will end soon enough.", "close_window", 
	# [
		# (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1, 0),
		# ## TODO: Start the timer for seeing if peace is pursued.
		# ## TODO: Release prisoner.
	# ]],
  
  # [anyone|plyr,"prisoner_olive_branch_c1", 
	# [], "On second thought, you will have to remain as my guest.", "prisoner_subject_transition", 
	# [
		# (call_script, "script_change_player_relation_with_troop", "$g_talk_troop", -1, 0),
	# ]],
  
  
  #################################
  ### RECRUITING AN OUTLAW LORD ###
  #################################
  
  # Requires: Prisoner is a lord.
  [anyone|plyr,"prisoner_talk", 
	[
		(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
		(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_robber_knight),
		# Prevent this option from showing up again.
		(eq, reg42, 0),
	], 
	"So you've resorted to common banditry?", "prisoner_discuss_recruitment",
	[]],
  
  # Requires: Prisoner is a lord.
  [anyone,"prisoner_discuss_recruitment", 
	[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),], 
	"It isn't as if I have been left with much choice{s66}.  Don't waste your breath, I don't have any ties left worth ransoming me to.", "prisoner_discuss_recruitment_2",
	[]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_2", 
	[], 
	"I seek not your coin, but your fealty.", "prisoner_discuss_recruitment_3",
	[]],
  
  [anyone,"prisoner_discuss_recruitment_3", 
	[], "What trick is this?  I have nothing beyond my army of vagabonds and I suspect their careers are about to be short by a head.", "prisoner_discuss_recruitment_4",
	[]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_4", 
	[], 
	"You and I have not seen eye to eye in the past, yet we can see where that has led you.  Forsake all of these other pretenders and back my claim to be the king of a united Calradia and I shall not only set you free, but grant you lands and title once more. ", "prisoner_discuss_recruitment_5",
	[]],
  
  [anyone,"prisoner_discuss_recruitment_5", 
	[], "Just like that?  After going against you you'll just take me as one of your men?", "prisoner_discuss_recruitment_6",
	[]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_6", 
	[], "I mean to unite these lands.  Binding its noble kin to me is the best way to do so.", "prisoner_discuss_recruitment_7",
	[]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_6", 
	[], "I expect an oath of loyalty.  One that any who fail to abide by it shall not live to regret.", "prisoner_discuss_recruitment_7",
	[]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_6", 
	[], "Perhaps you are right and giving you such a chance is of no value to me.", "prisoner_discuss_recruitment_8",
	[]],
  
  [anyone,"prisoner_discuss_recruitment_8", 
	[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),], 
	"There is no need for haste{s66}.  I was merely unprepared for your offer.", "prisoner_discuss_recruitment_8a",
	[]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_8a", 
	[], "So you will pledge to my cause then?", "prisoner_discuss_recruitment_7",
	[]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_8a", 
	[
		(troop_get_type, reg21, "$g_talk_troop"),
	], 
	"No, I've decided I have other plans for you.  Guards, take {reg21?her:him} away.", "close_window",
	[]],
  
  [anyone,"prisoner_discuss_recruitment_7", 
	[
		(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		(str_store_faction_name, s21, "$players_kingdom"),
	], 
	"Perhaps I had the wrong impression of you{s66}.  Very well...^^On my life and hope for rebirth, I pledge myself to your service.  I shall hold no lands or titles except those granted me by your will.  I shall defend your realm as its faithful servant and bring honor to the {s21}.", "prisoner_discuss_recruitment_9",
	[
		# Improve player right to rule.
		(call_script, "script_change_player_right_to_rule", 1),
		# Improve relation with this prisoner.
		(call_script, "script_troop_get_player_relation", "$g_talk_troop"),
		(assign, ":relation", reg0),
		(try_begin),
			(lt, ":relation", 25),
			(store_sub, ":boost", 25, ":relation"),
			(call_script, "script_change_player_relation_with_troop", "$g_talk_troop", ":boost", 1),
		(try_end),
		# Release the prisoner.
		(party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),        
        (call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
		# Change the troop's faction to the player's.
		(call_script, "script_diplomacy_change_troop_faction", "$g_talk_troop", "$players_kingdom"),
		# Announcement
		(str_store_troop_name, s21, "$g_talk_troop"),
		(str_store_faction_name, s22, "$players_kingdom"),
		(display_message, "@{s21} has become a vassal of {s22}!", gpu_green),
	]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_9", 
	[], 
	"You've made a wise decision.  We have much to discuss.", "close_window",
	[]],
  
  [anyone|plyr,"prisoner_discuss_recruitment_2", 
	[], 
	"Well then I will have to find another way to making you useful to me.", "close_window",
	[]],
  
  
  ############################
  ### RANSOMING A PRISONER ###
  ############################
  
  # Requires: Prisoner is a lord.
  [anyone|plyr,"prisoner_talk", 
	[
		(is_between, "$g_talk_troop", active_npcs_begin, active_npcs_end),
		(neg|troop_slot_eq, "$g_talk_troop", slot_troop_occupation, slto_robber_knight),
		# Prevent this option from showing up again.
		(eq, reg40, 0),
	], 
	"I am willing to release you from captivity depending on the ransom your family can pay.", "prisoner_discuss_terms_of_release",
	[
		(assign, reg51, 0), # Unused.
		(assign, reg52, 0), # Tracks if you threatened the prisoner for more money.
		(assign, reg53, 0), # Tracks if you successfully threatened the prisoner for more money.
		(assign, reg40, 1),
	]],
  
  [anyone,"prisoner_discuss_terms_of_release", 
	[
		(call_script, "script_calculate_ransom_amount_for_troop", "$g_talk_troop"),
		(assign, reg21, reg0),
		(val_mul, reg21, 60),
		(val_div, reg21, 100),
		(assign, "$diplomacy_ransom_offer", reg21),
	], 
	"I am certain my family could gather {reg21} denars immediately.  Any more than that would require more time.  You'd be most honorable in accepting that and letting me go.", "prisoner_discuss_terms_of_release_2",
	[]],
	
  [anyone|plyr,"prisoner_discuss_terms_of_release_2", 
	[], 
	"Yes, these terms are acceptable.", "prisoner_discuss_terms_of_release_accepted",
	[]],
  
  [anyone,"prisoner_discuss_terms_of_release_accepted", 
	[
		(try_begin),
			(eq, reg52, 1),
			(str_store_string, s21, "@I'll write your promissory note and go.  Let us hope for your sake we do not cross paths again."),
		(else_try),
			(str_store_string, s21, "@I shall draft the promissory note immediately.  Thank you, {Sir/Lady}.  I will not forgot this."),
		(try_end),
	], 
	"{s21}", "close_window",
	[
		(try_begin),
			(eq, reg52, 1),
			(assign, ":relation_change", -4),
			(assign, ":honor_change", -1),
		(else_try),
			(assign, ":relation_change", 2),
			(assign, ":honor_change", 1),
		(try_end),
		# Change player relation with the prisoner.
		(call_script,"script_change_player_relation_with_troop", "$g_talk_troop", ":relation_change"),
		# Improve player honor.
		(call_script, "script_change_player_honor", ":honor_change"),
		# Release the prisoner.
		(party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),        
        (call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
		# Collect payment.
		(call_script, "script_troop_add_gold", "trp_player", "$diplomacy_ransom_offer"),
		(call_script, "script_add_log_entry", logent_lord_defeated_but_let_go_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
	]],
  
  [anyone|plyr,"prisoner_discuss_terms_of_release_2", [], "I think you can do better than that.", "prisoner_discuss_terms_of_release_3", []],
  
  [anyone,"prisoner_discuss_terms_of_release_3", 
	[], 
	"{Sir/M'Lady}, I assure you that I am not holding out on you.  If you really must hold me hostage then you shall have to await my family's response for anything else.", "prisoner_discuss_terms_of_release_4",
	[]],
  
  [anyone|plyr,"prisoner_discuss_terms_of_release_4", 
	[
		# Must have a persuasion skill of 4+.
		# (store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
		# (ge, ":persuasion", 4),
		# Greater than 24 hours since last time of speaking.  This could be better using a threat only counter, but seems unnecessary.
		(ge, "$g_time_since_last_talk", 20),
	], 
	"I'll bet if I ship them your fingers one at a time they will improve upon your offer. (Intimidate)", "prisoner_discuss_terms_of_release_5",
	[
		(assign, reg52, 1),
		(store_skill_level, ":failure_point", "skl_persuasion", "trp_player"),
		(val_mul, ":failure_point", 6),
		(store_character_level, ":level", "trp_player"),
		(val_add, ":failure_point", ":level"),
		(val_min, ":failure_point", 80),
		(store_random_in_range, ":attempt", 0, 100),
		(try_begin),
			(lt, ":attempt", ":failure_point"),
			(assign, reg53, 1), # Success
		(else_try),
			(assign, reg53, 0), # Failure
		(try_end),
	]],
    
	[anyone,"prisoner_discuss_terms_of_release_5", 
	[
		(eq, reg53, 1),
		(call_script, "script_calculate_ransom_amount_for_troop", "$g_talk_troop"),
		(assign, reg21, reg0),
		(val_mul, reg21, 120),
		(val_div, reg21, 100),
		(assign, "$diplomacy_ransom_offer", reg21),
	], 
	"Have you no honor?  Very well, I will offer you {reg21} and not a denar more!  Will you accept this?", "prisoner_discuss_terms_of_release_2",
	[]],
  
    [anyone,"prisoner_discuss_terms_of_release_5", 
	[
		(eq, reg53, 0),
		(str_store_faction_name, s21, "$players_kingdom"),
	], 
	"You speak tough for your men, but we both know you do not have the courage to face my countrymen after such an act.  I see this is what passes for honor in the {s21}.  Your culture will not be missed when we put your villages to the torch and your families to the sword!", "close_window",
	[
		# Reduce player relation with the prisoner.
		(call_script,"script_change_player_relation_with_troop", "$g_talk_troop", -4),
		# Reduce player honor.
		(call_script, "script_change_player_honor", -1),
	]],
  
  
  [anyone|plyr,"prisoner_discuss_terms_of_release_4", [], "Then we shall have to wait and see.", "prisoner_transition_to_prisoner_talk", []],
  
  
  ##################################################
  ### PERSUADING AN ENEMY KING TO AGREE TO PEACE ###
  ##################################################
  
  # Requires: Prisoner is a ruler.  Player is the ruler or marshall of his faction.
  [anyone|plyr,"prisoner_talk", 
	[
		# Prisoner must be a ruler.
		(faction_get_slot, ":current_ruler", "$g_talk_troop_faction", slot_faction_leader),
		(eq, ":current_ruler", "$g_talk_troop"),
		# Must have a persuasion skill of 2+.
		(store_skill_level, ":persuasion", "skl_persuasion", "trp_player"),
		(ge, ":persuasion", 2),
		# At least 48 hours must have passed since your last attempt.
		(store_current_hours, ":hours"),
		(store_sub, ":time_since_last_attempt", ":hours", "$diplomacy_peace_time_stamp"),
		(ge, ":time_since_last_attempt", 48),
		# The player must be either a king/queen or the faction's marshall to make this decision.
		(this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
		(faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
		# Prevent this option from showing up again.
		(eq, reg41, 0),
	], 
	"This war between our people is senseless.  I wish to end it. (Persuade)", "prisoner_convince_king_to_end_war",
	[
		(store_skill_level, ":failure_point", "skl_persuasion", "trp_player"),
		(val_mul, ":failure_point", 4),
		(store_character_level, ":level", "trp_player"),
		(val_add, ":failure_point", ":level"),
		(val_min, ":failure_point", 80),
		(store_random_in_range, ":attempt", 0, 100),
		(try_begin),
			(lt, ":attempt", ":failure_point"),
			(assign, reg51, 1), # Success
		(else_try),
			(assign, reg51, 0), # Failure
		(try_end),
		(store_current_hours, "$diplomacy_peace_time_stamp"),
		(assign, reg41, 1),
		(assign, reg52, 0), # Attempt to force king to relinquish claim to Calradian throne.
	]],
	
  # Successful persuasion attempt.
  [anyone,"prisoner_convince_king_to_end_war", [(eq, reg51, 1),], "This war has been costly for both of our people I wager.  I will not give up my claim to the throne, but I will accept a truce between our kingdoms on the condition that you release me.", "prisoner_convince_king_to_end_war_2",[]],
  [anyone|plyr,"prisoner_convince_king_to_end_war_2", [(str_store_troop_name, s21, "$g_talk_troop"),], "Very well, {s21}.  You shall be set free, but I expect you to hold to your word.", "prisoner_convince_king_to_end_war_3",[]],
  [anyone,"prisoner_convince_king_to_end_war_3", [], "You have shown good wisdom here and I shall keep my word.  Perhaps we shall meet again under better circumstances.", "close_window",
	[
		# End the war.
		(call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_talk_troop_faction", "$players_kingdom", 1),
		# Improve player relation with the king.
		(call_script,"script_change_player_relation_with_troop", "$g_talk_troop", 5),
		# Improve player honor.
		(call_script, "script_change_player_honor", 3),
		# Improve player right to rule.
		(call_script, "script_change_player_right_to_rule", 3),
		# Release the prisoner.
		(party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),        
        (call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
		(call_script, "script_add_log_entry", logent_lord_defeated_but_let_go_by_player, "trp_player",  -1, "$g_talk_troop", "$g_talk_troop_faction"),
	]],
	
  # 
  [anyone|plyr,"prisoner_convince_king_to_end_war_2", 
	[
		(neg|faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
		(faction_get_slot, ":ruler", "$players_kingdom", slot_faction_leader),
		(str_store_troop_name, s21, ":ruler"),
	], 
	"You will only walk free once you and your vassals have sworn to follow {s21}!", "prisoner_transition_to_prisoner_talk", []],
  
  # Player king will not accept an end to the war unless you give up your claim.
  [anyone|plyr,"prisoner_convince_king_to_end_war_2", [(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),], "You will only walk free if you submit to my claim to the throne! (Intimidate)", "prisoner_king_forfeit_claim",
	[
		### COMPARE STRENGTH OF KINGDOMS ###
		(call_script, "script_diplomacy_rate_kingdom_strength", "$g_talk_troop_faction"),
		(assign, ":rating_enemy", reg1),
		(call_script, "script_diplomacy_rate_kingdom_strength", "$players_kingdom"),
		(assign, ":rating_player", reg1),
		(store_sub, ":chance_of_submit", ":rating_player", ":rating_enemy"),
		(val_div, ":chance_of_submit", 10),
		(val_clamp, ":chance_of_submit", 0, 100),
		# Make random roll.
		(store_random_in_range, ":attempt", 0, 100),
		(try_begin),
			(lt, ":attempt", ":chance_of_submit"),
			(assign, reg52, 1),
		(else_try),
			(assign, reg52, 0),
		(try_end),
		
	]],
	
  # Success intimidation check.
  [anyone,"prisoner_king_forfeit_claim", 
	[
		(eq, reg52, 1),
		(str_store_faction_name, s21, "$g_talk_troop_faction"),
	], 
	"*{s21} seems to consider your threat and sighs* ^^Very well, {playername}.  I do not wish any more bloodshed for my people.  I will reliquish my claim to the throne and swear fealty to you.  {s21}'s nobles shall follow your banner from this day forth.", "close_window",
	[
		# End the war.
		(call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_talk_troop_faction", "$players_kingdom", 1),
		# Improve player right to rule.
		(call_script, "script_change_player_right_to_rule", 8),
		# Release the prisoner.
		(party_remove_prisoners, "p_main_party", "$g_talk_troop", 1),        
        (call_script, "script_remove_troop_from_prison", "$g_talk_troop"),
		
		# Announce this!
		(str_store_faction_name_link, s21, "$g_talk_troop_faction"),
		(str_store_troop_name_link, s22, "$g_talk_troop"),
		(str_store_faction_name_link, s23, "$players_kingdom"),
		(display_message, "@{s22} of the {s21} has reliquished his claim to the throne!  The {s21} has become part of the {s23}!", gpu_green),
		
		# Reduce player kingdom relation with each faction that was at war with the conquered kingdom by 15.
		(try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
			(faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
			(store_relation, ":old_relation", ":kingdom_no", "$g_talk_troop_faction"),
			(lt, ":old_relation", 0),
			(val_div, ":old_relation", 3),
			(store_relation, ":relation", ":kingdom_no", "$players_kingdom"),
			(val_add, ":relation", ":old_relation"),
			(set_relation, ":kingdom_no", "$players_kingdom", ":relation"),
		(try_end),
		
		# Move every lord under the enemy faction over to $players_kingdom.
		(try_for_range, ":lord_no", active_npcs_begin, active_npcs_end),
			(store_faction_of_troop, ":faction_id", ":lord_no"),
			(eq, ":faction_id", "$g_talk_troop_faction"),
			(call_script, "script_diplomacy_change_troop_faction", ":lord_no", "$players_kingdom"),
		(try_end),
		# Deactivate the enemy faction.
		(faction_set_slot, "$g_talk_troop_faction", slot_faction_state, sfs_defeated),
	]],
  # Failed intimidation check.
  [anyone,"prisoner_king_forfeit_claim", [(neq, reg52, 1), (str_store_troop_name, s21, "$g_talk_troop"),], "*{s21} stares hard into your eyes and then spits in your direction before laughing ruefully*", "prisoner_convince_king_to_end_war",[(assign, reg51, 0),]],
  
  # Failed persuasion attempt.
  [anyone,"prisoner_convince_king_to_end_war", [(neq, reg51, 1),], "You want it to end?  Then back my claim to the throne.  Until then you shall not know peace while a single one of my supporters lives!", "prisoner_transition_to_prisoner_talk",[]],
  
  # Transitional dialog.
  [anyone, "prisoner_transition_to_prisoner_talk", 
	[
		(try_begin),
			(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
			(str_clear, s21),
		(else_try),
			(str_store_string, s21, "@, {knave/wench}"),
		(try_end),
	], "Is there anything else you wish to chat about before locking me up again{s21}?", "prisoner_talk", []],
  
  # Exit referring to Jailer role if assigned and present.
  [anyone|plyr,"prisoner_talk", 
	[
		(eq, reg39, 1), # Party "Jailer" is present.
		(troop_get_type, reg21, "$g_talk_troop"),
		(str_store_troop_name, s21, "$cms_role_jailer"),
	], 
	"I am done with you.  {s21}, get this {reg21?woman:man} out of my sight!", "cms_jailer_exit",[]],
  
  [anyone,"cms_jailer_exit", 
	[
		(troop_get_type, reg21, "$g_talk_troop"),
		# Determine Player's title.
		(try_begin),
			(faction_slot_eq, "$players_kingdom", slot_faction_leader, "trp_player"),
			(str_store_string, s21, "@, my {King/Queen}"),
		(else_try),
			(eq, "$player_has_homage", 1),
			(str_store_string, s21, "@, m'{Lord/Lady}"),
		(else_try),
			(str_clear, s21),
		(try_end),
		# Get prisoner's name.
		(str_store_troop_name, s22, "$g_talk_troop"),
		# Generate random closing remark.
		(store_random_in_range, ":roll", 0, 4),
		(try_begin),
			(eq, ":roll", 0),
			(str_store_string, s23, "@And no more arguing or you can do without supper for the night!"),
		(else_try),
			(eq, ":roll", 1),
			(try_begin),
				(neq, "$cms_role_storekeeper", "trp_player"),
				(main_party_has_troop, "$cms_role_storekeeper"),
				(str_store_troop_name, s24, "$cms_role_storekeeper"),
			(else_try),
				(str_store_string, s24, "@the cook"),
			(try_end),
			(str_store_string, s23, "@It is back to washing {s24}'s pots for you."),
		(else_try),
			(eq, ":roll", 2),
			(str_store_string, s23, "@I know a few horse pens that could use mucking and guess who I had in mind to do it?"),
		(else_try),
			(eq, ":roll", 3),
			(str_store_string, s23, "@Tonight let us try a new game, shall we?  You keep quiet or I bash your skull in.  Ransom or no, m'lord."),
		(else_try),
			(str_clear, s23),
		(try_end),
	], 
	"Right away{s21}!  Follow me, {s22}.  {s23}", "close_window",[(set_conversation_speaker_troop, "$cms_role_jailer"),]],
	
  # Default exit.
  [anyone|plyr,"prisoner_talk", 
	[
		(eq, reg39, 0), # Party "Jailer" is NOT present.
		(troop_get_type, reg21, "$g_talk_troop"),
	], 
	"I am done with you.  Guards, remove this {reg21?woman:man} from my sight!", "close_window",[]],
  ## WINDYPLAINS- ##
]

#################################################
#####        PATROL CAPTAIN : BEGIN         #####
#################################################
patrol_captain_dialogs = [

	# Dialog Start - Player meeting one of his own patrols.
	[anyone, "start",
		[
			(eq, "$talk_context", tc_party_encounter),
            (neg|encountered_party_is_attacker),
			(party_slot_eq, "$g_encountered_party", slot_party_type, spt_patrol),
			# Verify ownership.
			(party_get_slot, ":home_center", "$g_encountered_party", slot_party_patrol_home),
			(party_slot_eq, ":home_center", slot_town_lord, "trp_player"),
			# Determine what the patrol is currently assigned to do.
			(party_get_slot, ":patrol_focus", "$g_encountered_party", slot_party_ai_object),
			(this_or_next|is_between, ":patrol_focus", centers_begin, centers_end),
			(this_or_next|party_slot_eq, ":patrol_focus", slot_party_type, spt_kingdom_hero_party),
			(eq, ":patrol_focus", "p_main_party"),
			(str_store_party_name, s21, ":patrol_focus"),
			(try_begin),
				(party_slot_eq, "$g_encountered_party", slot_party_ai_state, spai_patrolling_around_center),
				(str_store_string, s22, "@  Our company is on patrol around {s21} currently."),
			(else_try),
				(party_slot_eq, "$g_encountered_party", slot_party_ai_state, spai_accompanying_army),
				(str_store_string, s22, "@  We're currently following {s21}."),
			(else_try),
				(str_clear, s22),
			(try_end),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		],
		"My scout reported seeing your party in the distance.  It is good to see you{s66}.{s22}  How may I be of service?  ", "patrol_captain_talk",
		[
			(assign, "$temp", 1), # Player owns the patrol.
		]],
		
	# Dialog Start - Player encountering someone else's patrols. (Player is king)
	# Dialog Start - Player encountering someone else's patrols.
	
	[anyone, "patrol_captain_pretalk",
		[
			(try_begin),
				(eq, "$temp", 1),
				(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
				(str_store_string, s22, "@{s66}"),
			(else_try),
				(str_clear, s22),
			(try_end),
		],
		"Is there any thing else I can do for you{s22}.", "patrol_captain_talk",
		[]],
		
	
	## Patrol Captain - Request to Follow / Stay : BEGIN ##
	[anyone|plyr, "patrol_captain_talk",
		[
			# Verify ownership.
			(party_get_slot, ":home_center", "$g_encountered_party", slot_party_patrol_home),
			(party_slot_eq, ":home_center", slot_town_lord, "trp_player"),
			# Verify party is currently in patrol mode.
			(party_slot_eq, "$g_encountered_party", slot_party_ai_state, spai_patrolling_around_center),
		],
		"I need you to follow me for a bit.", "patrol_captain_ordered_to_follow_or_stay",
		[
			(call_script, "script_diplomacy_patrol_functions", "$g_encountered_party", PATROL_ACCOMPANY_OWNER),
		]],
		
	[anyone|plyr, "patrol_captain_talk",
		[
			# Verify ownership.
			(party_get_slot, ":home_center", "$g_encountered_party", slot_party_patrol_home),
			(party_slot_eq, ":home_center", slot_town_lord, "trp_player"),
			# Verify party is currently in accompany mode.
			(party_slot_eq, "$g_encountered_party", slot_party_ai_state, spai_accompanying_army),
			(party_get_slot, ":center_no", "$g_encountered_party", slot_party_patrol_home),
			(str_store_party_name, s21, ":center_no"),
		],
		"I want you to return to patrolling around {s21}.", "patrol_captain_ordered_to_follow_or_stay",
		[
			(call_script, "script_diplomacy_patrol_functions", "$g_encountered_party", PATROL_RESET_AI_THINKING),
		]],
		
	[anyone, "patrol_captain_ordered_to_follow_or_stay",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),], 
		"As you wish{s66}.  I'll pass the word on to my men.", "patrol_captain_pretalk",	[]],
		
	## Patrol Captain - Request to Follow : END ##
	
	## Patrol Captain - Order new patrolling area : BEGIN ##
	[anyone|plyr, "patrol_captain_talk",
		[
			# Verify ownership.
			(party_get_slot, ":home_center", "$g_encountered_party", slot_party_patrol_home),
			(party_slot_eq, ":home_center", slot_town_lord, "trp_player"),
			# Verify party is currently in patrol mode.
			(party_slot_eq, "$g_encountered_party", slot_party_ai_state, spai_patrolling_around_center),
		],
		"I want you to patrol in a different area.", "patrol_captain_new_focus", []],
	
	[anyone, "patrol_captain_new_focus",
		[], "Where would you like me to patrol around?", "patrol_captain_new_focus_pick", []],
		
	[anyone|plyr|repeat_for_parties, "patrol_captain_new_focus_pick",
		[
			(store_repeat_object, ":center_no"),
			(is_between, ":center_no", centers_begin, centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(str_store_party_name, s21, ":center_no"),
		], "{s21}.", "patrol_captain_new_focus_picked", 
		[
			(store_repeat_object, ":center_no"),
			(assign, "$temp_2", ":center_no"),
			(party_set_ai_object, "$g_encountered_party", ":center_no"),
			(party_set_slot, "$g_encountered_party", slot_party_ai_object, ":center_no"),
		]],
	
	[anyone, "patrol_captain_new_focus_picked",
		[
			(str_store_party_name, s21, "$temp_2"),
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		], "Yes{s66}.  I'll pass orders to my men that we are to make for {s21} immediately.", "patrol_captain_pretalk", []],
		
	[anyone|plyr, "patrol_captain_new_focus_pick", [], "Never mind.  Stick with your current route.", "patrol_captain_pretalk", []],
	## Patrol Captain - Order new patrolling area : END ##
	
	## Patrol Captain - Turn over prisoners : BEGIN ##
	[anyone|plyr, "patrol_captain_talk",
		[
			# Verify ownership.
			(party_get_slot, ":home_center", "$g_encountered_party", slot_party_patrol_home),
			(party_slot_eq, ":home_center", slot_town_lord, "trp_player"),
			# Verify the party currently has prisoners.
			(party_get_num_prisoners, ":prisoner_count", "$g_encountered_party"),
			(ge, ":prisoner_count", 1),
			# Verify receiving party has room.
			(party_get_free_prisoners_capacity, ":capacity", "p_main_party"),
			(ge, ":capacity", 1),
		],
		"I want you to turn over your prisoners to my custody.", "patrol_captain_prisoner_exchange", 
		[
			(try_begin),
				(neq, "$cms_role_jailer", "trp_player"), # No point in responding to yourself.
				(set_visitor, 0, "$cms_role_jailer"),
				#(add_visitors_to_current_scene, 0, "$cms_role_jailer", 1), 
			(try_end),
		]],
	
	[anyone, "patrol_captain_prisoner_exchange",
		[
			# Get the current amount of prisoners available for transfer.
			(party_get_num_prisoners, reg21, "$g_encountered_party"),
			# Check how much capacity of the player party has.
			(party_get_free_prisoners_capacity, reg22, "p_main_party"),
			(store_sub, reg23, reg21, 1),
			(ge, reg22, reg21), # Capacity >= prisoners available.
			(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),
		], "Yes{s66}.  We have {reg21} prisoner{reg23?s:} available for transfer.", "patrol_captain_pretalk", 
		[
			(call_script, "script_diplomacy_patrol_functions", "$g_encountered_party", PATROL_OFFLOAD_PRISONERS),
		]],
	
	[anyone, "patrol_captain_prisoner_exchange",
		[
			# Get the current amount of prisoners available for transfer.
			(party_get_num_prisoners, reg21, "$g_encountered_party"),
			# Check how much capacity of the player party has.
			(party_get_free_prisoners_capacity, ":prisoner_capacity", "p_main_party"),
			(lt, ":prisoner_capacity", reg21), # Capacity < prisoners available.
			(assign, reg21, ":prisoner_capacity"), # Set available prisoners to equal capacity.
			(store_sub, reg23, reg21, 1),
		], "Did you want all of them?", "patrol_captain_not_enough_room", 
		[]],
	
	[anyone|plyr, "patrol_captain_not_enough_room",
		[
			(try_begin),
				(neq, "$cms_role_jailer", "trp_player"),
				(main_party_has_troop, "$cms_role_jailer"),
				(str_store_troop_name, s21, "$cms_role_jailer"),
				(str_store_string, s22, "@{s21} tells me that we"),
			(else_try),
				(str_store_string, s22, "@We"),
			(try_end),
		], "{s22} only have spare provisions to take on {reg21} more prisoner{reg23?s:}, but give me the worst of your lot.", "patrol_captain_not_enough_room_2", 
		[]],
	
	[anyone, "patrol_captain_not_enough_room_2",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),], 
		"Yes{s66}.  I'll have the most troublesome rounded up and transfered to your custody.", "patrol_captain_pretalk", 
		[
			(call_script, "script_diplomacy_patrol_functions", "$g_encountered_party", PATROL_OFFLOAD_PRISONERS),
		]],
	## Patrol Captain - Turn over prisoners : END ##
	
	[anyone|plyr, "patrol_captain_talk", [], "Fair journeys to you.  I must be going now.", "close_window", [(assign, "$g_leave_encounter",1)]],
		
	
#################################################
#####         PATROL CAPTAIN : END          #####
#################################################
]

companion_talk_addon = [
	## WINDYPLAINS+ ## - Hiring a new advisor.
	[anyone|plyr, "member_talk",
		[
			(is_between, "$g_talk_troop", companions_begin, companions_end),
			(assign, reg1, 0),
			(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
				(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
				(val_add, reg1, 1),
			(try_end),
			(ge, reg1, 1),
		],
		"I want you to take an advisory position.", "companion_advisor_appoint_1",
		[]],
	
	[anyone, "companion_advisor_appoint_1",
		[(call_script, "script_diplomacy_store_player_title_to_s66", "$g_talk_troop", 0),],
		"Very good{s66}.  Where will I be heading?", "companion_advisor_appoint_2",
		[]],
	
	[anyone|plyr|repeat_for_parties, "companion_advisor_appoint_2",
		[
			(store_repeat_object, ":center_no"),
			(is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
			(str_store_party_name, s21, ":center_no"),
		],
		"You'll need to travel to {s21}.", "companion_advisor_appoint_3",
		[(store_repeat_object, "$temp"),]],
	
	[anyone|plyr, "companion_advisor_appoint_2",
		[],
		"Never mind.", "member_pretalk",
		[]],
	
	[anyone, "companion_advisor_appoint_3",
		[
			(str_store_party_name, s21, "$temp"),
		],
		"What did you have in mind for me to do in {s21}?", "companion_advisor_appoint_4",
		[]],
	
	[anyone|plyr|repeat_for_100, "companion_advisor_appoint_4",
		[
			(store_repeat_object, ":counter"),
			(store_add, ":slot_no", advisors_begin, ":counter"),
			(is_between, ":slot_no", advisors_begin, advisors_end),
			(store_add, ":string_no", "str_diplomacy_advisor_steward", ":counter"),
			(str_store_string, s21, ":string_no"),
			(try_begin),
				(party_slot_eq, "$temp", ":slot_no", 0),
				(str_store_string, s23, "@takeover"),
			(else_try),
				(str_store_string, s22, "@replace"),
				(party_get_slot, ":advisor", "$temp", ":slot_no"),
				(str_store_troop_name, s24, ":advisor"),
				(str_store_string, s23, "@{s22} {s24}"),
			(try_end),
		],
		"I want you to {s23} as {s21}.", "companion_advisor_appoint_5",
		[(store_repeat_object, ":counter"),
		(store_add, "$temp_2", advisors_begin, ":counter"),]],
	
	[anyone|plyr, "companion_advisor_appoint_4",
		[],
		"Let's discuss a different location.", "companion_advisor_appoint_1",
		[]],
	
	[anyone|plyr, "companion_advisor_appoint_4",
		[],
		"Never mind.", "member_pretalk",
		[]],
	
	[anyone, "companion_advisor_appoint_5",
		[
			(try_begin),
				(party_slot_ge, "$temp", "$temp_2", 1),
				(party_get_slot, ":advisor", "$temp", "$temp_2"),
				(str_store_troop_name, s23, ":advisor"),
				(troop_get_type, reg22, ":advisor"),
				(str_store_string, s22, "@currently filled by {s23}"),
				(str_store_string, s24, "@replace {reg22?her:him} in"),
			(else_try),
				(str_store_string, s22, "@vacant"),
				(str_store_string, s24, "@take charge of"),
			(try_end),
			(store_sub, ":advisor_no", "$temp_2", advisors_begin),
			(store_add, ":string_no", ":advisor_no", "str_diplomacy_advisor_steward"),
			(str_store_string, s21, ":string_no"),
		],
		"The position of {s21} is {s22}.  Do you want me to {s24} that role?", "companion_advisor_appoint_6",
		[]],
	
	[anyone|plyr, "companion_advisor_appoint_6",
		[],
		"Yes.  Head out as soon as you're ready.", "close_window",
		[
			#(assign, "$temp_3", "$g_talk_troop"),
			# Remove any currently assigned advisor.
			(call_script, "script_diplomacy_remove_advisor", "$temp", "$temp_2", ADVISOR_BEGIN_RETURN_MISSION),			
			# Remove the new advisor from the player's party.
			(party_remove_members, "p_main_party", "$g_talk_troop", 1),
			(str_store_troop_name, s22, "$g_talk_troop"),
			(display_message, "@{s22} has left the party.", gpu_light_blue),
			# Assign the new advisor to the castle.
			(party_set_slot, "$temp", "$temp_2", "$g_talk_troop"),
			(troop_set_slot, "$g_talk_troop", slot_troop_advisor_station, "$temp"),
			(troop_set_slot, "$g_talk_troop", slot_troop_advisor_role, "$temp_2"),
			# COMPANION ROLES:
			(try_begin),
				## ROLE: STOREKEEPER ##
				(eq, "$cms_role_storekeeper", "$g_talk_troop"),
				(call_script, "script_cms_replace_troop_with_troop_in_role", "$g_talk_troop", "trp_player", ROLE_STOREKEEPER),
			(else_try),
				## ROLE: JAILER ##
				(eq, "$cms_role_jailer", "$g_talk_troop"),
				(call_script, "script_cms_replace_troop_with_troop_in_role", "$g_talk_troop", "trp_player", ROLE_JAILER),
			(else_try),
				## ROLE: QUARTERMASTER ##
				(eq, "$cms_role_quartermaster", "$g_talk_troop"),
				(call_script, "script_cms_replace_troop_with_troop_in_role", "$g_talk_troop", "trp_player", ROLE_QUARTERMASTER),
			(try_end),
		]],
	
	[anyone|plyr, "companion_advisor_appoint_6",
		[],
		"Never mind.", "member_pretalk",
		[]],
	## WINDYPLAINS- ##
]


from util_common import *
from util_wrappers import *

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
		var_name_1 = "dialogs"
		orig_dialogs = var_set[var_name_1]
		orig_dialogs.extend(dialogs)
		# Speaking to Court Steward
		pos = FindDialog_i(orig_dialogs, anyone, "companion_recruit_signup_confirm")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, advisor_steward_dialogs)
		# Insert Companion Dialog
		pos = FindDialog_i(orig_dialogs, anyone|plyr,"member_talk")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, companion_talk_addon)
		# Speaking to Captain of the Guard
		pos = FindDialog_i(orig_dialogs, anyone, "companion_recruit_signup_confirm")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, advisor_war_dialogs)
		# Speaking to Patrol Captain
		pos = FindDialog_i(orig_dialogs, anyone|plyr,"town_dweller_talk",)
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, patrol_captain_dialogs)
		# Speaking to Prisoners
		pos = FindDialog_i(orig_dialogs, anyone|plyr,"prisoner_chat")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, prisoner_talk_addon)
		# Speaking to Ransom Brokers
		pos = FindDialog_i(orig_dialogs, anyone|plyr,"ransom_broker_talk",)
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, ransom_broker_talk_addon)
		# Speaking to Minister
		pos = FindDialog_i(orig_dialogs, anyone|plyr, "minister_talk")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, minister_talk_addon)
		pos = FindDialog_i(orig_dialogs, anyone, "minister_grant_self_fief")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, minister_talk_addon2)
		# Speaking to Lords
		# pos = FindDialog_i(orig_dialogs, anyone,"lord_start")
		# OpBlockWrapper(orig_dialogs).InsertBefore(pos, lord_talk_addon)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)