from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
#import string

from xgm_mod_options_header import *

############################################################################
## 0) overlay id (not used atm, but can allow searches in future. just put something unique)
## 1) overlay type (defined in xgm_mod_options_header)
## 2) overlay type specific parameters (e.g. for number box, it can be lower/upper range, for cbobox, it would be the cbo items etc)
##    a) xgm_ov_numberbox : lower_bound(inclusive), upper_bound(exclusive). e.g. [0,101] for range of values from 0-100
##    b) xgm_ov_combolabel/xgm_ov_combobutton  : list of combo items. e.g. ["option1", "option2", "option3"]
##    c) xgm_ov_slider : lower_bound(inclusive), upper_bound(exclusive). e.g. [0,101] for range of values from 0-100
##    d) xgm_ov_checkbox : not used fttb. just leave empty. e.g. []
## 3) text label
## 4) reserved for text label flags
## 5) description (unused for now. may be used for stuff like tooltip in future)
## 6) reserved for description flags
## 7) initialization op block.  Used for updating the overlay values from game values. Must assign the desired value to reg1.
## 8) update op block.  Used for updating game values from overlay values. The overlay value is in reg1.
## 9) optional. reserved for option page id. unused for now. leave out for options using general page.
############################################################################

mod_options = [   
    # sample checkbox to switch the in-game cheat mode.  Comment out this if you don't want it.
    
    ("general_title_bar", xgm_ov_title, [], "General Options", tf_center_justify|tf_with_outline),
	
	# ("game_difficulty", xgm_ov_combobutton, ["Easy", "Normal", "Hard", "Very Hard"], "Game Difficulty:", 0,
	  # "This setting will alter how some mod effects function making them more or less restrictive, beneficial to the player or AI.  An example is that as difficulty is improved the AI will gain more healing while the player's allies receive less.", 0,
	  # [
		# (assign, reg1, "$mod_difficulty"),
		# (val_add, reg1, 1),
	  # ],
	  # [
		# (assign, "$mod_difficulty", reg1),
		# (val_sub, "$mod_difficulty", 1),
		# (call_script, "script_initialize_faction_troop_types"),
		# (call_script, "script_reset_garrisons"),
	  # ],),
	
	("enable_tutorials", xgm_ov_checkbox, [], "Enable Tutorial Quests:", 0,
		"When checked, this will allow tutorial quests to trigger if the conditions are right to explain how to use the mod's systems.", 0,
		[(assign, reg1, "$enable_tutorials"),],
		[(assign, "$enable_tutorials", reg1),],),
	
	("floris_ft_force_pause", xgm_ov_combobutton, ["- Disabled -", "Any Enemy", "Actual Threats"], "Pause during fast travel for:", 0,
		"Ticked, while fast-travelling (Ctrl-Space), the game will automatically pause when your party detects a hostile party.^^Unticked, as in Native, the game will NOT pause.", 0,
		[(assign, reg1, "$g_ft_force_pause"),],
		[(assign, "$g_ft_force_pause", reg1),],),
		
	("report_xp_prof", xgm_ov_checkbox, [], "Report Extra Combat Messages:", 0,
		"When checked, certain mod-related options will provide information on when they trigger.^^This includes extra experience gained when defeating an opponnent, extra proficiency gains in combat or when a rider is knocked off of their mount.", 0,
		[(assign, reg1, "$display_extra_xp_prof"),],
		[(assign, "$display_extra_xp_prof", reg1),],),
	
	("enable_pop_ups", xgm_ov_checkbox, [], "Enable Pop-up Notifications:", 0,
		"When checked, certain events will cause a pop-up message box to appear to more readily notify you instead of simply adding a line of text in your message log.^^Examples of this include quest warnings or finishing reading a book.", 0,
		[(assign, reg1, "$enable_popups"),],
		[(assign, "$enable_popups", reg1),],),
	
	("diplomacy_title_bar", xgm_ov_title, [], "Enhanced Diplomacy Options", tf_center_justify|tf_with_outline),
	
	("Disable_popups", xgm_ov_checkbox, [], "Faction only notifications:", 0,
		"Setting this will prevent popup notifications of war or peace between kingdoms that you are not a member of.", 0,
		[(assign, reg1, "$diplomacy_filter_enabled"),],
		[(assign, "$diplomacy_filter_enabled", reg1),],),
	
	# ("alt_morale_system", xgm_ov_checkbox, [], "Use Alternate Morale System:", 0,
		# "When enabled, this causes party morale to be calculated using a more elaborate system that does not simply penalize you for having a large party.^^When disabled, the morale system should function exactly like the native game.", 0,
		# [(assign, reg1, "$diplomacy_use_alt_morale"),],
		# [(assign, "$diplomacy_use_alt_morale", reg1),],),
	
	
	("dipl_ai_switch_cultures", xgm_ov_checkbox, [], "AI Lords Switch Cultures:", 0,
		"When enabled, this will cause vassals of the player's faction to use the culture you have chosen instead of their own original culture when recruiting for their army.^^Note: Their army does not immediately switch over.", 0,
		[(assign, reg1, "$diplomacy_ai_use_player_culture"),],
		[(assign, "$diplomacy_ai_use_player_culture", reg1),],),
	
	("dipl_mandatory_recruitmen", xgm_ov_checkbox, [], "Mandatory Auto-Recruitment:", 0,
		"When enabled, this will cause the 'Mandatory Conscription' decree to trigger every time auto-recruitment via the Captain of the Guard is processed.^^This means you'll gain a lot more recruits at a cost of relation and prosperity with the center.", 0,
		[(assign, reg1, "$diplomacy_force_recruit_enabled"),],
		[(assign, "$diplomacy_force_recruit_enabled", reg1),],),
	
	("companion_title_bar", xgm_ov_title, [], "Companion Options", tf_center_justify|tf_with_outline),
  
	("pbod_npc_complaints", xgm_ov_checkbox, [], "Disable Companions' complaints:", 0,
		"Disabling NPC Complaints will mute your companion's complaints about each other or your decisions.  While disabled, companions will not leave the party regardless of how they feel about your leadership.", 0,
		[(assign, reg1, "$disable_npc_complaints"),],
		[(assign, "$disable_npc_complaints", reg1),],),
	
	("enable_auto_selling", xgm_ov_checkbox, [], "Enable Quartermaster Auto-Sell:", 0,
		"Quartermaster Setting:^When checked, your assigned quartermaster (if not yourself) will automatically sell any battlefield loot he has accumulated upon entering town.", 0,
		[(assign, reg1, "$cms_enable_auto_selling"),],
		[
			(assign, "$cms_enable_auto_selling", reg1),
			## QUEST HOOK: qst_qp6_quartermaster_assignment
			(try_begin),
				(check_quest_active, "qst_qp6_quartermaster_assignment"),
				(eq, "$cms_enable_auto_selling", 1),
				(quest_slot_eq, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 0),
				(quest_set_slot, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 1),
				(call_script, "script_qp6_quartermaster_assignment", floris_quest_update),
				(call_script, "script_qp6_quartermaster_assignment", floris_quest_victory_condition),
			(else_try),
				(check_quest_active, "qst_qp6_quartermaster_assignment"),
				(eq, "$cms_enable_auto_selling", 0),
				(quest_slot_eq, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 2),
				(quest_set_slot, "qst_qp6_quartermaster_assignment", slot_quest_stage_1_trigger_chance, 0),
				(str_store_string, s1, "@Objecive - Enable the Quartermaster auto-selling option."),
				(add_quest_note_from_sreg, "qst_qp6_quartermaster_assignment", 3, s1, 0), # Enabling Storekeeper Purchasing option.
			(try_end),
		],),
	
	("pickup_threshold", xgm_ov_numberbox, [1, 1000], "Minimum Value for Pickup:", 0,
		"Quartermaster Setting:^This setting determines the minimum value that an item must have before you, or your assigned Quartermaster, will pick it up during the auto-loot process when you elect to collect valuable items and leave.", 0,
		[(assign, reg1, "$cms_minimum_pickup_value"),],
		[
			(assign, "$cms_minimum_pickup_value", reg1),
			## QUEST HOOK: qst_qp6_quartermaster_assignment
			(try_begin),
				(check_quest_active, "qst_qp6_quartermaster_assignment"),
				(quest_slot_eq, "qst_qp6_quartermaster_assignment", slot_quest_stage_3_trigger_chance, 0),
				(quest_set_slot, "qst_qp6_quartermaster_assignment", slot_quest_stage_3_trigger_chance, 1),
				(call_script, "script_qp6_quartermaster_assignment", floris_quest_update),
				(call_script, "script_qp6_quartermaster_assignment", floris_quest_victory_condition),
			(try_end),
		],),
	
	("enable_auto_buying", xgm_ov_checkbox, [], "Enable Storekeeper Auto-Buy:", 0,
		"Storekeeper Setting:^When checked, your assigned storekeeper (if not yourself) will automatically purchase selected quantities of food goods upon exiting a town or village.  You need to configure these selections in the marketplace menu.", 0,
		[(assign, reg1, "$cms_enable_auto_buying"),],
		[
			(assign, "$cms_enable_auto_buying", reg1),
			## QUEST HOOK: qst_qp6_storekeeper_assignment
			(try_begin),
				(check_quest_active, "qst_qp6_storekeeper_assignment"),
				(eq, "$cms_enable_auto_buying", 1),
				(quest_slot_eq, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 0),
				(quest_set_slot, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 1),
				(call_script, "script_qp6_storekeeper_assignment", floris_quest_update),
				(call_script, "script_qp6_storekeeper_assignment", floris_quest_victory_condition),
			(else_try),
				(check_quest_active, "qst_qp6_storekeeper_assignment"),
				(eq, "$cms_enable_auto_buying", 0),
				(quest_slot_eq, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 2),
				(quest_set_slot, "qst_qp6_storekeeper_assignment", slot_quest_stage_1_trigger_chance, 0),
				(str_store_string, s1, "@Objecive - Enable the Storekeeper purchasing option."),
				(add_quest_note_from_sreg, "qst_qp6_storekeeper_assignment", 3, s1, 0), # Enabling Storekeeper Purchasing option.
			(try_end),
		],),
	
	("autobuy_threshold", xgm_ov_numberbox, [1, 10000], "Minimum Cash to Maintain:", 0,
		"Storekeeper Setting:^If your current cash falls below this value your Storekeeper will not purchase any new food even if conditions warrant it.", 0,
		[(assign, reg1, "$cms_minimum_cash_block"),],
		[
			(assign, "$cms_minimum_cash_block", reg1),
			## QUEST HOOK: qst_qp6_storekeeper_assignment
			(try_begin),
				(check_quest_active, "qst_qp6_storekeeper_assignment"),
				(quest_slot_eq, "qst_qp6_storekeeper_assignment", slot_quest_stage_4_trigger_chance, 0),
				(quest_set_slot, "qst_qp6_storekeeper_assignment", slot_quest_stage_4_trigger_chance, 1),
				(call_script, "script_qp6_storekeeper_assignment", floris_quest_update),
				(call_script, "script_qp6_storekeeper_assignment", floris_quest_victory_condition),
			(try_end),
		],),
	
	("stores_warning", xgm_ov_numberbox, [0, 10], "Days of Food Left Warning:", 0,
		"Storekeeper Setting:^When your Storekeeper's remaining days of available food drops below this threshold you'll receive a warning.^^To disable this warning set the value to 0.", 0,
		[(assign, reg1, "$cms_days_of_food_threshold"),],
		[(assign, "$cms_days_of_food_threshold", reg1),],),
	
	("gaoler_mode", xgm_ov_combobutton, ["- Disabled -", "Sell Prisoners Only", "Store Prisoners Only", "Store & Sell Prisoners"], "Set Party Gaoler Mode:", 0,
		"Gaoler Setting:^This tells the party gaoler (if not yourself) how to function.^^Sell Prisoners - When the gaoler has prisoners available to sell and a ransom broker nearby they'll automatically sell them.^^Store Prisoners - When your party returns to a castle or town that you own, the gaoler will store any prisoners.", 0,
		[(assign, reg1, "$cms_mode_jailer")],
		[
			(assign, "$cms_mode_jailer", reg1),
			## QUEST HOOK: qst_qp6_quartermaster_assignment
			(try_begin),
				(check_quest_active, "qst_qp6_jailer_assignment"),
				(quest_slot_eq, "qst_qp6_jailer_assignment", slot_quest_stage_2_trigger_chance, 0),
				(quest_set_slot, "qst_qp6_jailer_assignment", slot_quest_stage_2_trigger_chance, 1),
				(call_script, "script_qp6_jailer_assignment", floris_quest_update),
				(call_script, "script_qp6_jailer_assignment", floris_quest_victory_condition),
			(try_end),
		],),
	  
	("party_role_log_mode", xgm_ov_combobutton, ["Summary", "Detailed"], "Companion Action Log:", 0,
	  "This alters how verbose a party role will be in reporting their actions to the message log.", 0,
	  [(assign, reg1, "$cms_report_mode")],
	  [(assign, "$cms_report_mode", reg1),],),
	  
	("pbod_bodyguard", xgm_ov_combobutton, ["Disabled", "1 Bodyguard Limit", "2 Bodyguard Limit", "3 Bodyguard Limit", "4 Bodyguard Limit"], "Enable Bodyguards in Towns:", 0,
		"Bodyguards allows your companions to serve as your character's bodyguards in town and village scenes. The number of bodyguards depends on your character's leadership and renown.", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_bodyguard),],
		[
			(party_set_slot, "p_main_party", slot_party_pref_bodyguard, reg1),
			(party_set_slot, "p_main_party", slot_party_bodyguard_backup, reg1),
			#(display_message, "@Setting is now {reg1}.", gpu_debug),
		],),	
	
   # ( "op_quest_changes", xgm_ov_line ),
	
	# ("block_trade_quests", xgm_ov_checkbox, [], "Block Trade Quests:", 0,
		# "Enabling this will prevent automatic aquisition of trade based quests when you assess local prices in the marketplace.", 0,
		# [(assign, reg1, "$qp2_block_trade_quests"),],
		# [(assign, "$qp2_block_trade_quests", reg1),],),
	
	("tournament_title_bar", xgm_ov_title, [], "Tournament System", tf_center_justify|tf_with_outline),
	
	("tpe_toggle", xgm_ov_checkbox, [], "Enhanced Tournaments:", 0,
	  "Ticked, the enhanced tournament system is active. Unticked, tournaments are as in Native.", 0,
	  [(assign, reg1, "$g_wp_tpe_active"),],
	  [
		(assign, "$g_wp_tpe_active", reg1),
	  ],),
	
   ("tpe_quest_block", xgm_ov_checkbox, [], "Block Tournament Quests:", 0,
	  "When ticked, this will prevent tournament quests from occurring.", 0,
	  [(assign, reg1, "$tpe_block_quests")],
	  [(assign, "$tpe_block_quests", reg1),],),
	  
   ("tpe_mode", xgm_ov_combobutton, ["Performance", "Elimination"], "Tournament Mode:", 0,
	  "Performance Mode: (Default)^Tournament system ranks participants based upon the scoring method.^^Elimination Mode:^Similar to the native design this gives first priority on ranking to survival in a round.", 0,
	  [(assign, reg1, "$tpe_tournament_mode")],
	  [(assign, "$tpe_tournament_mode", reg1),],),
	  
   ("tpe_shortcuts", xgm_ov_combobutton, ["- Disabled -", "Options Panel", "Design Panel", "Information"], "TPE Setting Shortcuts:", 0,
	  "Select any of the presentations on this menu and you'll immediately jump to that panel for configuring up tournament settings.", 0,
	  [(assign, reg1, 0)],
	  [
		(try_begin),
			(eq, reg1, 1),
			(neq, "$g_is_quick_battle", 1), # Not using a custom battle.
			## Options Panel
			(change_screen_return),
			(assign, "$g_wp_tpe_troop", "trp_player"),
			(troop_set_slot, "trp_tpe_presobj", tpe_options_display_mode, wp_tpe_combat_settings),
			(assign, "$return_presentation", "prsnt_mod_option"),
			(start_presentation, "prsnt_tournament_options_panel"),
		(else_try),
			(eq, reg1, 2),
			(neq, "$g_is_quick_battle", 1), # Not using a custom battle.
			## Design Panel
			(change_screen_return),
			(assign, "$tournament_town", "p_town_1"), # Just picking a default.
			(assign, "$return_presentation", "prsnt_mod_option"),
			(start_presentation, "prsnt_tpe_design_settings"),
		(else_try),
			(eq, reg1, 3),
			(neq, "$g_is_quick_battle", 1), # Not using a custom battle.
			## Help Panel
			(change_screen_return),
			(troop_set_slot, tci_objects, tci_val_information_mode, 0),
			(assign, "$return_presentation", "prsnt_mod_option"),
			(start_presentation, "prsnt_tpe_credits"),
		(try_end),
	  ],),
	
	("pbod_title_bar", xgm_ov_title, [], "Pre-Battle Deployment Options", tf_center_justify|tf_with_outline),
	
	("pbod_real_deployment", xgm_ov_checkbox, [], "Enable Real Deployment Phase:", 0,
		"Real Deployment allows you to position your troops on the field before the battle begins.^To access this feature, begin the battle by chosing 'Take the Field' or creating and using a pre-battle plan.^^If you experience problems with this feature, see the Time Slowing option below.", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_real_deployment),],
		[(party_set_slot, "p_main_party", slot_party_pref_real_deployment, reg1),],),	
		
	("pbod_real_deployment_2", xgm_ov_combobutton, ["Default", "Faster", "Fastest"], "R.Dply. Phase Time Slowing:", 0,
		"If Battle Continuation is active, you can select what your troops will do after you get knocked out: Disabled has them continue their previous orders; Charge all will give everyone a charge order; Formations AI (if active for the AI) will allow the new AI to take over for you.", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_rdep_time_scale),],
		[(party_set_slot, "p_main_party", slot_party_pref_rdep_time_scale, reg1),],),	
		
	("pbod_bc_continue", xgm_ov_checkbox, [], "Enable Battle Continuation:", 0,
		"Battle Continuation allows your troops to continue fighting after you are knocked out.", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_bc_continue),],
		[(party_set_slot, "p_main_party", slot_party_pref_bc_continue, reg1),],),	 
		
	("pbod_bc_charge_ko", xgm_ov_combobutton, ["- Disabled -", "Charge All", "Formations AI"], "Batt. Cont., Charge after KO:", 0,
		"If Battle Continuation is active, you can select what your troops will do after you get knocked out: Disabled has them continue their previous orders; Charge all will give everyone a charge order; Formations AI (if active for the AI) will allow the new AI to take over for you.", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_bc_charge_ko),],
		[(party_set_slot, "p_main_party", slot_party_pref_bc_charge_ko, reg1),],),	
		
	("pbod_formations", xgm_ov_combobutton, ["- Disabled -", "Formations AI", "Native AI, w/Formations"], "Formations Battle AI:", 0,
		"Select your prefered Battle AI: Disabled is Native AI; Formations AI both allows the AI to use formations and changes their battle decision-making; Native AI w/Formations is Native AI but carries out the Native AI with basic formations. (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_formations),],
		[(party_set_slot, "p_main_party", slot_party_pref_formations, reg1),],),
		
	("pbod_siege_charge", xgm_ov_checkbox, [], "Disable charge on belfry reaching wall:", 0,
		"Unticked, as Native, when the belfry (siege tower) reaches a wall, the player's attacking force will automatically charge. Ticked and the charge order will not be automatically given.", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_siege_charge),],
		[(party_set_slot, "p_main_party", slot_party_pref_siege_charge, reg1),],),	 
		
	("pbod_div_dehorse", xgm_ov_combobutton, [s0, s1, s2, s3, s4, s5, s6, s7, s8, "- Disabled -"], 
		"Reassign De-horsed Cavalry to:", 0,
		"Mounted bots, once their horse dies, can be re-assinged to a division of your choosing. If active, AI bots will be reassigned to infantry. (Only active in field battles.)", 0,
		[
			(try_for_range, ":i", 0, 9),
			(str_store_class_name, ":i", ":i"),
			(try_end),
			(party_get_slot, reg1, "p_main_party", slot_party_pref_div_dehorse),
		],
		[(party_set_slot, "p_main_party", slot_party_pref_div_dehorse, reg1),],),	
		
	("pbod_div_no_ammo", xgm_ov_combobutton, [s0, s1, s2, s3, s4, s5, s6, s7, s8, "- Disabled -"], 
		"Reassign No-Ammo Archers to:", 0,
		"Foot archer bots, once out of ammo, can be re-assinged to a division of your choosing. If active, AI bots will be reassigned to infantry. (Only active in field battles.)", 0,
		[
			(try_for_range, ":i", 0, 9),
			(str_store_class_name, ":i", ":i"),
			(try_end),
			(party_get_slot, reg1, "p_main_party", slot_party_pref_div_no_ammo),
		],
		[(party_set_slot, "p_main_party", slot_party_pref_div_no_ammo, reg1),],),	
			
	("combat_title_bar", xgm_ov_title, [], "Combat Options", tf_center_justify|tf_with_outline),
  
	("toggle_bodysliding", xgm_ov_combobutton, ["Disabled", "Companions Only", "All Troops"], "Bodysliding Mode:", 0,
		"When enabled, you will switch over to controlling another battlefield troop whenever you die in combat.^^When set to companions only then you will only take over other companions upon death.  If no companions are available the death camera will activate.^^All Troops will allow sliding to companions first and then regular soldiers.", 0,
		[(assign, reg1, "$enable_bodysliding"),],
		[(assign, "$enable_bodysliding", reg1),],),	
		
	("health_regen", xgm_ov_combobutton, ["- Disabled -", "Player Only", "AI Only", "Player & AI"], "Health Regeneration:", 0,
	  "If enabled, depending on who is set to receive it anytime a player or AI (non-player) defeats an enemy in combat they will receive a small boost in health.^^Note: Turning this off will help CPU performance.", 0,
	  [(assign, reg1, "$killer_regen_mode")],
	  [(assign, "$killer_regen_mode", reg1),],),
	
	("toggle_allow_abilities", xgm_ov_checkbox, [], "Enable Combat Ability System:", 0,
	  "When enabled, special combat abilities for troops are turned on to alter their combat performance.^^Note: Turning this off will greatly help CPU performance.  This also disables combat hampering.", 0,
	  [(assign, reg1, "$enable_combat_abilities"),],
	  [(assign, "$enable_combat_abilities", reg1),],),
	  
	("toggle_allow_sprinting", xgm_ov_checkbox, [], "Enable Combat Sprinting:", 0,
	  "When enabled, soldiers (player and AI) on foot may attempt to close the gap with their enemy at a sprinting speed based upon their agility, strength & athletics.^^Note: Turning this off will help CPU performance.", 0,
	  [(assign, reg1, "$enable_sprinting"),],
	  [(assign, "$enable_sprinting", reg1),],),
	
	("fallen_riders", xgm_ov_checkbox, [], "Riders Damaged When Unhorsed:", 0,
		"When checked, this will cause any mounted rider (player or AI) to receive damage when their mount is taken out from under them.  Damage is increased based upon the speed the mount was moving and the total weight of the rider and reduced by the rider's riding skill.^^Note: Turning this off will help CPU performance.", 0,
		[(assign, reg1, "$enable_fallen_riders"),],
		[(assign, "$enable_fallen_riders", reg1),],),
	
	("encumbrance", xgm_ov_checkbox, [], "Enable Encumbrance Penalties:", 0,
		"When checked, the player and companions will have penalties to athletics, shield, power draw, riding & horse archery based upon the total weight of their equipment.^^Note: Turning this off will greatly help CPU performance.", 0,
		[(assign, reg1, "$enable_encumbrance"),],
		[(assign, "$enable_encumbrance", reg1),],),
	
	("encumbrance", xgm_ov_checkbox, [], "Enable Combat Hampering:", 0,
		"When checked, all troops become slower in movement, deal less damage and become less accurate as their health dwindles.  This option affects both player and AI.^^Note: Turning this off will help CPU performance.", 0,
		[(assign, reg1, "$combat_hampering_enabled"),],
		[(assign, "$combat_hampering_enabled", reg1),],),
	
	("pbod_wu_lance", xgm_ov_checkbox, [], "Use NPC Lancer Fix:", 0,
		"Weapon Use Fix for Lancers will force mounted bots with lances to use them unless they are surrounded by enemies. (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_wu_lance),],
		[(party_set_slot, "p_main_party", slot_party_pref_wu_lance, reg1),],),	
		
	("pbod_wu_harcher", xgm_ov_checkbox, [], "Use NPC Horse Archer Fix:", 0,
		"Weapon Use Fix for Horse Archers will force mounted bots with bows to use them until they run out of ammo. (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_wu_harcher),],
		[(party_set_slot, "p_main_party", slot_party_pref_wu_harcher, reg1),],),	
		
	("pbod_wu_spear", xgm_ov_checkbox, [], "Use NPC Spear/Polearm Fix:", 0,
		"Weapon Use Fix for Spear/Polearms will force infantry bots with polearms to use them unless they are surrounded by enemies. (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_wu_spear),],
		[(party_set_slot, "p_main_party", slot_party_pref_wu_spear, reg1),],),
		
	("pbod_dmg_tweaks", xgm_ov_checkbox, [], "Use Pike/Horse Damage Tweaks:", 0,
		"Damage tweaks will give a flat boost to damage from spears to horses, and charge damage from horses to infantry, in an attempt to compensate for poor AI use of polearms and charges. (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_dmg_tweaks),],
		[(party_set_slot, "p_main_party", slot_party_pref_dmg_tweaks, reg1),],),
		
	
	# ("pbod_ally_division", xgm_ov_checkbox, [], "Keep allies in the basic 3 divisions:", 0,
		# "Ticked, troops of ally parties under your command will not be assigned to your customized divisions, but to the default infantry, archer, and cavalry divisions. Unticked, as in Native, any ally troops under your command will be re-assigned to the same divisions as your troops of the same type.", 0,
		# [(party_get_slot, reg1, "p_main_party", slot_party_pref_ally_division),],
		# [(party_set_slot, "p_main_party", slot_party_pref_ally_division, reg1),],
		# ),	
		
	("pbod_spo_brace", xgm_ov_checkbox, [], "Enable AI Spear Bracing:", 0,
		"Enabling AI Special Orders allows the AI teams to use volley fire (crossbows), skirmish mode (bow-users), and spear-bracing (polearm infantry). (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_spo_brace),],
		[(party_set_slot, "p_main_party", slot_party_pref_spo_brace, reg1),],),	
		
	("pbod_spo_skirmish", xgm_ov_checkbox, [], "Enable AI Skirmishing:", 0,
		"Enabling AI Special Orders allows the AI teams to use volley fire (crossbows), skirmish mode (bow-users), and spear-bracing (polearm infantry). (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_spo_skirmish),],
		[(party_set_slot, "p_main_party", slot_party_pref_spo_skirmish, reg1),],),	
	
	("pbod_spo_volley", xgm_ov_checkbox, [], "Enable AI Volley Fire:", 0,
		"Enabling AI Special Orders allows the AI teams to use volley fire (crossbows), skirmish mode (bow-users), and spear-bracing (polearm infantry). (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_spo_volley),],
		[(party_set_slot, "p_main_party", slot_party_pref_spo_volley, reg1),],),	
	
	("pbod_spo_pavise", xgm_ov_checkbox, [], "Enable AI Deploy Pavise Shields:", 0,
		"Enabling AI Special Orders allows the AI teams to use volley fire and pavise deployment (crossbows), skirmish mode (bow-users), and spear-bracing (polearm infantry). (Only active in field battles.)", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_spo_pavise),],
		[(party_set_slot, "p_main_party", slot_party_pref_spo_pavise, reg1),],),
	
	("pbod_wp_prof_decrease", xgm_ov_checkbox, [], "Enable ranged penalty from weather:", 0,
		"The Weather Proficiency Penalties lowers the ranged weapons proficiencies of all troops while in battle in heavy fog, rain/snow, or at night to reflect the poor conditions for archery.", 0,
		[(party_get_slot, reg1, "p_main_party", slot_party_pref_wp_prof_decrease),],
		[(party_set_slot, "p_main_party", slot_party_pref_wp_prof_decrease, reg1),],),	 
	
	("combat_ui_title_bar", xgm_ov_title, [], "Combat Interface Options", tf_center_justify|tf_with_outline),

	("toggle_troop_ratio_bar", xgm_ov_checkbox, [], "Enable Troop Ratio Bar:", 0,
	  "When enabled a graphical bar displaying the ratio of allies and enemies left on the battlefield will appear during combat.^^If unchecked, this will not appear.", 0,
	  [(assign, reg1, "$enable_troop_ratio_bar"),],
	  [(assign, "$enable_troop_ratio_bar", reg1),],),
	  
	("toggle_battle_mini_map", xgm_ov_checkbox, [], "Enable Battle Overview Map:", 0,
	  "When enabled a small transparent map of the current battle will appear in the upper right corner of the combat screen.^^If unchecked, this will not appear.", 0,
	  [(assign, reg1, "$enable_battle_minimap"),],
	  [(assign, "$enable_battle_minimap", reg1),],),
	  
	("toggle_show_stamina_bar", xgm_ov_checkbox, [], "Enable Stamina Bar:", 0,
	  "When enabled, a graphic representation of your current stamina level will appear directly underneath your health bar.", 0,
	  [(assign, reg1, "$enable_stamina_bar_ui"),],
	  [(assign, "$enable_stamina_bar_ui", reg1),],),
	  
	("stamina_color", xgm_ov_combobutton, ["Gold", "Blue", "Green"], "Stamina Bar Color:", 0,
	  "This sets the color of the stamina bar.", 0,
	  [(assign, reg1, "$stamina_bar_color")],
	  [(assign, "$stamina_bar_color", reg1),],),
	  
	("toggle_title_bar", xgm_ov_title, [], "Mod Toggle Options", tf_center_justify|tf_with_outline),

	("toggle_autoloot_data", xgm_ov_checkbox, [], "Enable Troop Debugging:", 0,
	  "When enabled, certain presentations will display extra information for individuals building their own troop trees.^^View All Items - Now displays autoloot ratings and percentage values.^^View All Troops - Now highlights upgraded troops that are not +1 tier above the troop they were hired from.  Below will be displayed how far below their intended tier they are.", 0,
	  [(assign, reg1, "$show_autoloot_data"),],
	  [(assign, "$show_autoloot_data", reg1),],),
	  
	("toggle_troop_prefixes", xgm_ov_checkbox, [], "Enable Troop Prefixes:", 0,
	  "When enabled this will add prefixes to the beginning of troop names describing what kind of troop they are.^^H = Horse Archer^C = Cavalry^A = Archer^I = Infantry^^The following # is the troop's tier.^^Note: This may take a few seconds depending on your computer.", 0,
		[(assign, reg1, "$enable_troop_prefixes"),],
		[
			(assign, "$enable_troop_prefixes", reg1),
			(call_script, "script_alter_troop_prefixes", "$enable_troop_prefixes", troop_definitions_begin, troop_definitions_end), # Faction Troops & Bandits	
		],),
	  
	("naming_convention", xgm_ov_combobutton, ["Immersive", "Functional", "Descriptive"], "Naming Convention:", 0,
	  "This alters how troop upgrades are named.  This stacks with the troop prefix toggle in any mode.^^Immersive:^Rhodok Crossbowman^Veteran Rhodok Crossbowman^Elite Rhodok Crossbowman^^Functional:^Rhodok Crossbowman^Rhodok Crossbowman (+)^Rhodok Crossbowman (++)^^Descriptive:^Rhodok Crossbowman^Rhodok Crossbowman (Veteran)^Rhodok Crossbowman (Elite)", 0,
	  [(assign, reg1, "$troop_naming_convention"),],
	  [
		(assign, ":old_style", "$troop_naming_convention"),
		(assign, "$troop_naming_convention", reg1),
		(call_script, "script_alter_naming_convention", ":old_style", "$troop_naming_convention", kingdom_troops_begin,  kingdom_troops_end),  	# Faction Troops
	    (call_script, "script_alter_naming_convention", ":old_style", "$troop_naming_convention", bandits_begin,  bandits_end),  				# Bandits
	  ],),
	
	("toggle_village_allies", xgm_ov_checkbox, [], "Disable village allies:", 0,
	  "When enabled, this prevents villagers from joining your side while you're defending their village.", 0,
	  [(assign, reg1, "$disable_village_allies"),],
	  [(assign, "$disable_village_allies", reg1),],),
	  
	("toggle_metrics_data", xgm_ov_checkbox, [], "Display Metric Data:", 0,
	  "When enabled, debugging data for long term balance testing.^^Metrics Tracked:^Trainer skill savings", 0,
	  [(assign, reg1, "$enable_metrics"),],
	  [(assign, "$enable_metrics", reg1),],),
	  
	( "op_cheatmode", xgm_ov_checkbox ,  [],
        "Enable Debug Mode:", 0,        
        "This enables the in-game 'cheat' menu and provides access to debugging information.  The output is very verbose if enabled.", 0,
        [(assign, reg1, "$cheat_mode"),], 
        [(assign, "$cheat_mode", reg1),],),
	
	( "op_cheatengine", xgm_ov_checkbox ,  [],
        "Enable Cheat Mode:", 0,        
        "This sets the warband engine cheat mode normally found in the configuration screen and allows the control key cheats.", 0,
        [(options_get_cheat_mode, reg1),], 
        [  # update block (value is in reg1)
            (assign, "$config_cheatmode", reg1),
			(options_set_cheat_mode, "$config_cheatmode"),
        ],),
	
] # mod_options

# TODO: add option pages here


# collation of all *_mod_options.py from active mods
# import and merge related variables from all {active_mod}_mod_options.py for all active mods
try:
    from modmerger_options import options, mods_active
    from modmerger import mod_get_process_order, mod_is_active
    from util_common import add_objects
    modcomp_name = "mod_options"
    var_list = ["mod_options",]
    
    #from modmerger import modmerge
    #modmerge(var_set)

    mod_process_order = mod_get_process_order(modcomp_name)
    
    vars_to_import= ["mod_options"]
    
    for x in mod_process_order:
        if(mod_is_active(x) and x <> "xgm_mod_options"): # must exclude this file since we are using this file as base
            try:
                #mergefn_name = "modmerge_%s"%(modcomp_name)
                target_module_name = "%s_%s"%(x,modcomp_name)
                
                _temp = __import__( target_module_name , globals(), locals(), vars_to_import,-1)
                logger.info("Merging objects for component \"%s\" from mod \"%s\"..."%(modcomp_name,x))

                add_objects(mod_options, _temp.mod_options) # import from target module.

                # TODO: collect option pages

            except ImportError:
                errstring = "Failed importing for component \"%s\" for mod \"%s\"." % (modcomp_name, x)
                logger.debug(errstring)
        else:
            errstring = "Mod \"%s\" not active for Component \"%s\"." % (x, modcomp_name)
            logger.debug(errstring)

except:
    raise
# collation end

# At this point, mod_options will contain the list of all mod_options specified.



## utility functions

from util_wrappers import *

# helper wrapper to access mod_options
class ModOptionWrapper(BaseWrapper):

    def __init__(self, _data):
        # verify _data
        if( not isinstance(_data,TupleType) or (len(_data)<2)):
            raise ValueError("ItemSetWrapper: Wrapped must be a tuple.")
        BaseWrapper.__init__(self,_data)
        
        
    def GetId(self):
        return self.data[0]

    def GetType(self):
        return self.data[1]

    def GetParameters(self):
        if len(self.data) >2: 
            return self.data[2]
        return None

    def GetParameter(self, i):
        if len(self.data) >2: 
            return self.data[2][i]
        return None

    def GetTextLabel(self):
        if len(self.data) >3: 
            return self.data[3]
        return None

    def GetTextLabelFlags(self):
        if len(self.data) >4: 
            return self.data[4]
        return None

    def GetDescription(self):
        if len(self.data) >5: 
            return self.data[5]
        return None

    def GetDescriptionFlags(self):
        if len(self.data) >6: 
            return self.data[6]
        return None

    def GetInitializeBlock(self):
        if len(self.data) >7: 
            return OpBlockWrapper(self.data[7])
        return None

    def GetUpdateBlock(self):
        if len(self.data) >8: 
            return OpBlockWrapper(self.data[8])
        return None

    def GetHeight(self):
        if self.GetType() == xgm_ov_line:
            return xgm_mod_options_line_height
        elif self.GetType() in [xgm_ov_checkbox, xgm_ov_numberbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_title]:
            return xgm_mod_options_property_height        
        # elif self.GetType() in [xgm_ov_title]:
            # return (xgm_mod_options_property_height * 1)   
        return 0 # no other types supported

## class ModOptionWrapper
	


# this function will compute the total height required for a list of mod_options.
def mod_options_get_total_height(_mod_options = mod_options):
    height = 0
    for x in _mod_options:
        aModOption = ModOptionWrapper(x)
        height += aModOption.GetHeight()	
    # for x in _mod_options:
    return height;    
## mod_options_get_total_height	
