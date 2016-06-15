# Enhanced Diplomacy Options (1.0) by Windyplains

strings = [
###########################################################################################################################
#####                                                COMMON STRINGS                                                   #####
###########################################################################################################################
	("diplomacy_advisor_steward",                  "Court Steward"),
	("diplomacy_advisor_war",                      "Captain of the Guard"),
	("diplomacy_advisor_finances",                 "Financial Advisor"),
	("diplomacy_party_morale_report", "Current party morale is {reg5}.^Current party morale modifiers are:^^Party size: {s2}{reg1}^Leadership: {s3}{reg2}^Food variety: {s4}{reg3}{s5}{s6}^Days on the Road: {s8}{reg8}^Party Unity: {s10}{reg10}^Troop Bonuses: {s11}{reg11}^Recent events: {s7}{reg4}^TOTAL:  {reg5}^^^"),
	
###########################################################################################################################
#####                                          KINGDOM MANAGEMENT SYSTEM                                              #####
###########################################################################################################################
	("kms_accept",                                 "Enact Policy Changes"),
	("kms_cancel",                                 "Cancel"),
	("kms_leave",                                  "Leave"),
	("kms_restore",                                "Restore Defaults"),
	("kms_main_title",                             "Kingdom Policies"),
	("kms_label_policies",                         "Domestic Policies"),
	("kms_label_decrees",                          "Royal Decrees"),
	("kms_label_summary",                          "Total Summary"),
	("kms_label_help",                             "Information"),
	("kms_label_player_faction",                   "{s21} Policies"),
	("kms_label_warning_non_king",                 "This display is for information only.  No alterations can be made unless you are king."),
	("kms_blank",                                  " "),
	("diplomacy_data_benefit_line",                "{s40}^* {s1}"),
	
	# POLICY - CULTURAL FOCUS
	("kms_sfp_focus_label",                        "Cultural Focus"),
	# Stage Labels
	("kms_sfp_focus_left_2",                       "Trade Empire"),
	("kms_sfp_focus_left_1",                       "Trading"),
	("kms_sfp_focus_neutral",                      "Balanced"),
	("kms_sfp_focus_right_1",                      "Militant"),
	("kms_sfp_focus_right_2",                      "Conquest"),
	# Descriptions of stages
	("kms_sfp_focus_desc_left_2",                  "The citizens of your culture focus primarily upon ^establishing a trade empire."),
	("kms_sfp_focus_desc_left_1",                  "Ensuring the growth and prosperity of your towns through ^trade is the focus of your citizens."),
	("kms_sfp_focus_desc_neutral",                 "Focus within your kingdom is balanced between the needs of ^trade and security."),
	("kms_sfp_focus_desc_right_1",                 "Security has become the primary focus for the citizens of ^your kingdom."),
	("kms_sfp_focus_desc_right_2",                 "Your citizens are committed to making your kingdom the ^dominant military power."),
	# Long Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_focus_long_desc_1",                  "A ruler's vision for their kingdom is often only successful"),
	("kms_sfp_focus_long_desc_2",                  "if the citizens share a similar desire.  The population of"),
	("kms_sfp_focus_long_desc_3",                  "a kingdom tends to sit between focus on trade and ensuring"),
	("kms_sfp_focus_long_desc_4",                  "security of the region.  This has a strong influence on the"),
	("kms_sfp_focus_long_desc_5",                  "every day life of your subjects, how willing they may be to"),
	("kms_sfp_focus_long_desc_6",                  "join in the defense of the kingdom and what kind of"),
	("kms_sfp_focus_long_desc_7",                  "prosperity the kingdom enjoys."),
	### SPACING GUIDE #############################                                                              ##########
	
	# DIPLOMACY SUMMARY
	("kms_summary_label",                          "Policy Game Effects"),
	# Stage Labels
	### SPACING GUIDE #############################                                                              ##########
	("kms_summary_long_desc_1",                    "When every aspect of a kingdom's policies are tied together"),
	("kms_summary_long_desc_2",                    "a greater picture of its strengths and weaknesses can be"),
	("kms_summary_long_desc_3",                    "seen.  Some cultures may push towards an empire built upon"),
	("kms_summary_long_desc_4",                    "trade and maintaining the peace while others must conquer"),
	("kms_summary_long_desc_5",                    "in order to survive.  How kingdom is guided by its liege"),
	("kms_summary_long_desc_6",                    "will be greatly influenced by the laws that are enacted and"),
	("kms_summary_long_desc_7",                    "the careful timing of when to use them."),
	### SPACING GUIDE #############################                                                              ##########
	
	# POLICY - MILITARY DIVERSITY
	("kms_sfp_diversity_label",                    "Military Diversity"),
	# Stage Labels
	("kms_sfp_diversity_left_2",                   "Multi-cultural"),
	("kms_sfp_diversity_left_1",                   "Diverse"),
	("kms_sfp_diversity_neutral",                  "Balanced"),
	("kms_sfp_diversity_right_1",                  "Rigid"),
	("kms_sfp_diversity_right_2",                  "Uniform"),
	# Descriptions of stages
	("kms_sfp_diversity_desc_left_2",              "Your commanders are taught to embrace the different talents ^other cultures bring."),
	("kms_sfp_diversity_desc_left_1",              "Commanders in your army make regular use of troops trained ^in other lands."),
	("kms_sfp_diversity_desc_neutral",             "Unit leaders in your kingdom strive to strike a balance in ^unit diversity."),
	("kms_sfp_diversity_desc_right_1",             "Your commanders generally prefer to rely upon men trained ^under their own guidance."),
	("kms_sfp_diversity_desc_right_2",             "Your army is uniformly trained and has strong bonds, but ^distrusts outsiders."),
	# Long Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_diversity_long_desc_1",              "A long standing debate exists among military commanders on"),
	("kms_sfp_diversity_long_desc_2",              "whether the benefits of a multi-cultured army that makes"),
	("kms_sfp_diversity_long_desc_3",              "use of a wider variety of talents outweight the benefits of"),
	("kms_sfp_diversity_long_desc_4",              "a uniformly trained fighting force that shares a common"),
	("kms_sfp_diversity_long_desc_5",              "background.  This common ground, or lack there of, can also"),
	("kms_sfp_diversity_long_desc_6",              "have a strong influence on the morale of a party with the"),
	("kms_sfp_diversity_long_desc_7",              "inclusion of mercenaries proving especially troublesome."),
	### SPACING GUIDE #############################                                                              ##########
	
	# POLICY - BORDER CONTROL
	("kms_sfp_borders_label",                      "Border Control"),
	# Stage Labels
	("kms_sfp_borders_left_2",                     "Open Borders"),
	("kms_sfp_borders_left_1",                     "Abundant Travel"),
	("kms_sfp_borders_neutral",                    "Regular Travel"),
	("kms_sfp_borders_right_1",                    "Limited Travel"),
	("kms_sfp_borders_right_2",                    "Sealed Borders"),
	# Descriptions of stages
	("kms_sfp_borders_desc_left_2",                "Outsiders are welcomed in your lands for the news and ^goods they bring."),
	("kms_sfp_borders_desc_left_1",                "Foreigners are commonplace upon your roads and treated ^well."),
	("kms_sfp_borders_desc_neutral",               "Travelers are free to come and go so long as order is ^maintained."),
	("kms_sfp_borders_desc_right_1",               "Outsiders are viewed with suspicion, but allowed to cross ^your territory."),
	("kms_sfp_borders_desc_right_2",               "Few travelers are allowed to cross your borders ^unchallenged."),
	# Long Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_borders_long_desc_1",                "Trade is the lifeblood of any growing civilization, yet so"),
	("kms_sfp_borders_long_desc_2",                "too is maintaining security.  A wise ruler must seek the"),
	("kms_sfp_borders_long_desc_3",                "balance that best compliments the needs of the kingdom"),
	("kms_sfp_borders_long_desc_4",                "without too strong an impact on free trade with other"),
	("kms_sfp_borders_long_desc_5",                "realms, yet still maintain a strong defensive line.  This"),
	("kms_sfp_borders_long_desc_6",                "choice will have lasting implications upon a kingdom's"),
	("kms_sfp_borders_long_desc_7",                "ability to conduct trade."),
	### SPACING GUIDE #############################                                                              ##########
	
	# POLICY - SLAVERY
	("kms_sfp_slavery_label",                      "Slavery"),
	# Stage Labels
	("kms_sfp_slavery_left_2",                     "Outlawed"),
	("kms_sfp_slavery_left_1",                     "Banned"),
	("kms_sfp_slavery_neutral",                    "Uncommon"),
	("kms_sfp_slavery_right_1",                    "Accepted"),
	("kms_sfp_slavery_right_2",                    "Commonplace"),
	# Descriptions of stages
	("kms_sfp_slavery_desc_left_2",                "Slavery is not allowed within your realm and any found are ^freed immediately."),
	("kms_sfp_slavery_desc_left_1",                "The citizens of the kingdom hold slavery in contempt, ^preferring to do things for themselves."),
	("kms_sfp_slavery_desc_neutral",               "Slaves are not unheard of, but it is a luxury to own one.^"),
	("kms_sfp_slavery_desc_right_1",               "Even houses of modest income enjoy the benefit of a slave or ^two."),
	("kms_sfp_slavery_desc_right_2",               "The kingdom thrives due to the support of its slave ^population."),
	# Long Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_slavery_long_desc_1",                "A population's views on the subject of slavery can have far"),
	("kms_sfp_slavery_long_desc_2",                "reaching implications into the daily lives of its subjects."),
	("kms_sfp_slavery_long_desc_3",                "With slaves available to perform the more demanding tasks"),
	("kms_sfp_slavery_long_desc_4",                "the subjects are often weaker than a culture that focuses"),
	("kms_sfp_slavery_long_desc_5",                "upon self-reliance.  A steady supply of slaves ensures that"),
	("kms_sfp_slavery_long_desc_6",                "expendable labor is available for any project, yet this"),
	("kms_sfp_slavery_long_desc_7",                "also effects the value one will pay for such slaves."),
	### SPACING GUIDE #############################                                                              ##########
	
	# POLICY - TROOP DESERTION
	("kms_sfp_desertion_label",                    "Desertion"),
	# Stage Labels
	("kms_sfp_desertion_left_2",                   "Accepted"),
	("kms_sfp_desertion_left_1",                   "Tolerated"),
	("kms_sfp_desertion_neutral",                  "Ignored"),
	("kms_sfp_desertion_right_1",                  "Disgraced"),
	("kms_sfp_desertion_right_2",                  "Hunted"),
	# Descriptions of stages
	("kms_sfp_desertion_desc_left_2",              "Desertion is an accepted reality of in your armies due to ^their voluntary nature."),
	("kms_sfp_desertion_desc_left_1",              "Serving in the kingdom's army is at the soldier's choice ^knowing they can return home if desired."),
	("kms_sfp_desertion_desc_neutral",             "When conditions are difficult, some soldiers may desert and ^this is viewed with indifference."),
	("kms_sfp_desertion_desc_right_1",             "Knowing that only disgrace will greet them at home should ^they leave, few soldiers will risk fleeing."),
	("kms_sfp_desertion_desc_right_2",             "Deserters in your kingdom are often betrayed by their own ^disgraced families."),
	# Long Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_desertion_long_desc_1",              "A civilization's outlook upon the act of desertion can have"),
	("kms_sfp_desertion_long_desc_2",              "a strong influence in a commoner's outlook upon joining a "),
	("kms_sfp_desertion_long_desc_3",              "passing army voluntarily.  If a deserter is likely to face"),
	("kms_sfp_desertion_long_desc_4",              "imprisonment or death then the choice of fleeing back to"),
	("kms_sfp_desertion_long_desc_5",              "their home village becomes much more difficult, but so too"),
	("kms_sfp_desertion_long_desc_6",              "does the choice to join at all.  Conditions in an army that"),
	("kms_sfp_desertion_long_desc_7",              "accepts desertion must remain good or face losing soldiers."),
	### SPACING GUIDE #############################                                                              ##########
	
	# DIPLOMACY DATA OUTPUT TYPES: (these should be used by a common script that outputs an s1 line.
	### SPACING GUIDE #############################                                                              ##########
	("kms_data_type_village_recruits",             "Recruits available in villages are {reg2?reduced:increased} by {reg1}."),
	("kms_data_type_desertion_threshold",          "Soldiers may desert if party morale is below {reg1}."),
	("kms_data_type_desertion_factor",             "Soldiers are {s2} likely to desert."),
	("kms_data_type_unity_faction",                "Unity is reduced by {reg1} for {reg3?every {reg2}:each} faction {reg3?troops:troop}."),
	("kms_data_type_unity_nonfaction",             "Unity is reduced by {reg1} for {reg3?every {reg2}:each} non-faction {reg3?troops:troop}."),
	("kms_data_type_unity_mercs",                  "Unity is reduced by {reg1} for {reg3?every {reg2}:each} mercenary {reg3?troops:troop}."),
	("kms_data_type_center_income",                "Base income for fiefs is {reg2?reduced:improved} by {reg1}%."),
	("kms_data_type_center_tariffs",               "Trade income for fiefs is {reg2?reduced:improved} by {reg1}%."),
	("kms_data_type_army_size",                    "Kingdom armies have {reg1} {reg2?fewer:more} troops."),
	("kms_data_type_patrol_size",                  "Kingdom patrols have {reg1}% {reg2?fewer:more} troops."),
	("kms_data_type_raw_material_discount",        "Enterprises find raw materials cost {reg1}% {reg2?less:more}."),
	("kms_data_type_prosperity_ideal",             "The ideal prosperity of fiefs is {reg2?reduced:increased} by {reg1}."),
	("kms_data_type_price_of_slaves",              "Slaves are sold for {reg1}% {reg2?less:more} in your kingdom."),
	("kms_data_type_slaver_availability",          "Ransom brokers have a {reg1}% chance to appear in your towns."),
	("kms_data_type_party_morale",                 "Base party morale is {reg2?reduced:increased} by {reg1}."),
	("kms_data_type_improvement_cost",             "The cost of improvements is {reg2?reduced:increased} by {reg1}%."),
	("kms_data_type_improvement_time",             "The time required to build improvements is {reg2?reduced:increased} by {reg1}%."),
	("kms_data_type_village_recruit_tier",         "The proficiency of village recruits is {reg2?reduced:improved} by {reg1} {reg3?tiers:tier}."),
	("kms_data_type_castle_recruit_tier",          "The proficiency of castle recruits is {reg2?reduced:improved} by {reg1} {reg3?tiers:tier}."),
	("kms_data_type_labor_discount",               "Enterprises find labor costs to be {reg1}% {reg2?less:more} than standard."),
	("kms_data_type_troop_wages",                  "Troop wages are {reg2?reduced:raised} by {reg1}%."),
	("kms_data_type_march_unrest",                 "Campaign morale will drop by {reg1} each day once triggered."),
	("kms_data_type_march_tolerance",              "Campaign morale will begin lowering after {reg1} {reg2?days:day}."),
	("kms_data_type_prosperity_real",              "The immediate prosperity of fiefs is {reg2?reduced:improved} by {reg1}."),
	("kms_data_type_prosperity_recovery",          "A fief's prosperity recovery rate {reg2?reduced:increased} by {reg1}%."),
	("kms_data_type_lrep_martial_relation",        "Martial lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_quarrelsome_relation",    "Quarrelsome lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_selfrighteous_relation",  "Self-righteous lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_cunning_relation",        "Cunning lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_debauched_relation",      "Debauched lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_goodnatured_relation",    "Goodnatured lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_upstanding_relation",     "Upstanding lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_roguish_relation",        "Roguish lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_benefactor_relation",     "Benefactor lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_lrep_custodian_relation",      "Custodian lords have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_fief_relation",                "Fiefs have a {reg1}% chance to {reg2?lose:gain} 1 relation weekly."),
	("kms_data_type_bandit_infestation",           "Villages have a {reg1}% {reg2?smaller:greater} chance of becoming infested."),
	("kms_data_type_right_to_rule",                "Citizens are {reg1}% {reg2?less:more} likely to approve of your rule."),
	# v0.16 additions.
	("kms_data_type_weariness_penalty",            "The weariness penalty per battle is {reg2?increased:reduced} by {reg1}."),
	("kms_data_type_weariness_recovery_rate",      "The weariness recovery is {reg1}% {reg2?slower:faster}."),
	("kms_data_type_weariness_recovery_limit",     "The weariness recovery rate limit is {reg2?reduced:improved} by {reg1}."),
	
	### SPACING GUIDE #############################                                                              ##########
	
	# ROYAL DECREE labels.  These need to be kept together in order so their checkbox labels are not messed up.
	("kms_sfd_conscription_label",                 "Mandatory Conscription"),
	("kms_sfd_code_of_law_common_label",           "Code of Law (Common)"),
	("kms_sfd_code_of_law_noble_label",            "Code of Law (Nobility)"),
	("kms_sfd_war_taxation_label",                 "War Taxation"),
	("kms_sfd_sanitation_label",                   "Sanitation Standards"),
	("kms_sfd_reconstruction_label",               "Period of Reconstruction"),
	("kms_sfd_executions_label",                   "Public Executions"),
	
	# DECREE - MANDATORY CONSCRIPTION
	# Tooltip Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_conscription_long_desc_1",           "During times of war it is often necessary for a liege to"),
	("kms_sfp_conscription_long_desc_2",           "make service in the kingdom's army an obligation in order"),
	("kms_sfp_conscription_long_desc_3",           "to ensure a proper defense for the realm.  While this will"),
	("kms_sfp_conscription_long_desc_4",           "immediately boost the ranks of a kingdom, it does have a"),
	("kms_sfp_conscription_long_desc_5",           "strong impact on the villages left behind with fewer hands"),
	("kms_sfp_conscription_long_desc_6",           "to work the fields.  It is vital for a ruler to know when"),
	("kms_sfp_conscription_long_desc_7",           "to implement such a drastic rule and when to revoke it."),
	### SPACING GUIDE #############################                                                              ##########
	
	# DECREE - CODE OF LAW (COMMON)
	# Tooltip Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_commonlaw_long_desc_1",              "A wise ruler knows that the reach of a ruler only extends"),
	("kms_sfp_commonlaw_long_desc_2",              "as far as it is enforced.  Implementing a standardized code"),
	("kms_sfp_commonlaw_long_desc_3",              "of law for all subjects may override the local laws each"),
	("kms_sfp_commonlaw_long_desc_4",              "village or town may have followed, but it sets a more"),
	("kms_sfp_commonlaw_long_desc_5",              "consistent order of justice within the kingdom's borders."),
	("kms_sfp_commonlaw_long_desc_6",              "While this promotes a greater overall prosperity for a"),
	("kms_sfp_commonlaw_long_desc_7",              "settlement, it presents an expense to maintain it."),
	### SPACING GUIDE #############################                                                              ##########
	
	# DECREE - CODE OF LAW (NOBILITY)
	# Tooltip Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_noblelaw_long_desc_1",               "With experience, a ruler must learn that while it is the"),
	("kms_sfp_noblelaw_long_desc_2",               "nobility that helps maintain a sense of order and brings"),
	("kms_sfp_noblelaw_long_desc_3",               "men to fight in their wars, it is the lot of the peasant"),
	("kms_sfp_noblelaw_long_desc_4",               "that defines a kingdom's true prosperity.  Enacting a set"),
	("kms_sfp_noblelaw_long_desc_5",               "of laws designed to keep the nobility from taking too much"),
	("kms_sfp_noblelaw_long_desc_6",               "advantage of their fiefs allows for their settlements to"),
	("kms_sfp_noblelaw_long_desc_7",               "flourish and in turn improves the strength of the kingdom."),
	### SPACING GUIDE #############################                                                              ##########
	
	# DECREE - WAR TAXATION
	# Tooltip Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_wartaxes_long_desc_1",               "The waging of war is costly business and can drain the"),
	("kms_sfp_wartaxes_long_desc_2",               "treasury of even a prospering kingdom if not carefully"),
	("kms_sfp_wartaxes_long_desc_3",               "maintained.  Passing on a greater degree of that burden to"),
	("kms_sfp_wartaxes_long_desc_4",               "the merchants, craftsmen and even other nobles may prove"),
	("kms_sfp_wartaxes_long_desc_5",               "unpopular, but it may very well keep your men equipped and"),
	("kms_sfp_wartaxes_long_desc_6",               "well fed.  Beware pushing a kingdom too hard for too long and"),
	("kms_sfp_wartaxes_long_desc_7",               "the road to recovery will be steep once war is past."),
	### SPACING GUIDE #############################                                                              ##########
	
	# DECREE - PERIOD OF RECONSTRUCTION
	# Tooltip Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_reconstruction_long_desc_1",         "With the turmoil of war past, a ruler must look to"),
	("kms_sfp_reconstruction_long_desc_2",         "rebuilding communities within the kingdom.  Channeling all"),
	("kms_sfp_reconstruction_long_desc_3",         "of a settlement's normal taxation into rebuilding it will"),
	("kms_sfp_reconstruction_long_desc_4",         "greatly reduce the recovery time of looted villages by"),
	("kms_sfp_reconstruction_long_desc_5",         "allowing them to spend the excess coin on supplies.  This"),
	("kms_sfp_reconstruction_long_desc_6",         "does leave the kingdom dealing with a great loss in its"),
	("kms_sfp_reconstruction_long_desc_7",         "standard income forcing it to rely upon income from trade."),
	### SPACING GUIDE #############################                                                              ##########
	
	# DECREE - SANITATION STANDARDS
	# Tooltip Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_sanitation_long_desc_1",             "Growing cities face dangers beyond the standard of warfare"),
	("kms_sfp_sanitation_long_desc_2",             "and banditry.  They must also content with the chance of"),
	("kms_sfp_sanitation_long_desc_3",             "plague which is often accelerated through poor standards in"),
	("kms_sfp_sanitation_long_desc_4",             "sanitation.  Enacting ordinances that ensure a standard"),
	("kms_sfp_sanitation_long_desc_5",             "method of dealing with the dead, ensuring the town's water"),
	("kms_sfp_sanitation_long_desc_6",             "supply remains untainted and provide more immediate care to"),
	("kms_sfp_sanitation_long_desc_7",             "the sick can save far more than it costs in the end."),
	### SPACING GUIDE #############################                                                              ##########
	
	# DECREE - PUBLIC EXECUTIONS
	# Tooltip Description
	### SPACING GUIDE #############################                                                              ##########
	("kms_sfp_executions_long_desc_1",             "The sight of a thief hanging from a rope can drive a fear"),
	("kms_sfp_executions_long_desc_2",             "of order deeply into a society and turn many away from the"),
	("kms_sfp_executions_long_desc_3",             "temptation of easy wealth.  Such acts may or may not be"),
	("kms_sfp_executions_long_desc_4",             "popular within a kingdom depending upon its culture, but"),
	("kms_sfp_executions_long_desc_5",             "the outcome is usually the same.  Bandits will find easier"),
	("kms_sfp_executions_long_desc_6",             "places to ply their trade when capture involves a grim end"),
	("kms_sfp_executions_long_desc_7",             "to one's career."),
	### SPACING GUIDE #############################                                                              ##########
	
	# Tournament Credits & Information Panel
	("kms_exit",        "Exit"),
	("kms_main_topics", "Back"),
	("kms_main_title",  "Kingdom Management System"),
	("kms_sub_title",   "Version (Alpha)"),
	
	# Diplomacy Guide
	("kms_info_0",   "Information Topics:"),
	("kms_info_0a",  "Overview"),           # Reference strings kms_info_1* Overview
	("kms_info_0b",  "Message Filtering"),  # Reference strings kms_info_2* Message Filtering
	("kms_info_0c",  "Policies & Decrees"), # Reference strings kms_info_3* Policies & Decrees
	("kms_info_0d",  "Dialog Options"),     # Reference strings kms_info_4* Dialog Options
	("kms_info_0e",  "Morale System"),      # Reference strings kms_info_5* Morale System
	("kms_info_0f",  "Companion Advisors"), # Reference strings kms_info_6* Companion Advisors
	#("kms_info_0g",  "Reserved"),           # Reference strings kms_info_7* Unused
	("kms_info_0z",  "Credits"),            # Reference strings kms_info_8*
	# Overview
	("kms_info_1a",  "I've long felt that Mount & Blade needed more options for kings to control their culture "),
	("kms_info_1b",  "and how things are conducted within it.  Many mods have taken a stab at trying to "),
	("kms_info_1c",  "improve this aspect of the game and I've taken inspiration from the changes I agreed "),
	("kms_info_1d",  "with.  My goal here has been to make kingdoms less generic, add in some conveniences "),
	("kms_info_1e",  "for the player and improve the immersion a little. "),
	("kms_info_1f",  " "),
	("kms_info_1g",  "Within these topics you should find at least a generic sense of what each sub-system "),
	("kms_info_1h",  "does and how to alter it to your own needs.  "),
	# Message Filtering
	("kms_info_2a",  "There are a number of game updates shown in the message log while you travel the world "),
	("kms_info_2b",  "map that simply do not pertain to your kingdom and this can distract you from seeing "),
	("kms_info_2c",  "information that  is more pertinent.  The goal here was to alter what information you "),
	("kms_info_2d",  "see, how you perceive it and limit some of the distracting 'pop-up' menus that appear "),
	("kms_info_2e",  "in the game naturally. "),
	("kms_info_2ea", " "),
	("kms_info_2f",  "Enabling message filtering: "),
	("kms_info_2g",  "You should find message filtering enabled by default, but if you wish to disable it then "),
	("kms_info_2h",  "visit the main mod options page under the 'camp' menu.  From there you should find an "),
	("kms_info_2i",  "option listed as 'Faction Only Notifications'.  If it is checked then it is enabled. "),
	("kms_info_2j",  " "),
	("kms_info_2k",  "Effects of enabling this option:"),
	("kms_info_2l",  "1)  Messages related to lords being captured, towns being sieged, villages being "),
	("kms_info_2m",  "raided, lords being defeated and lords defecting to another faction will now be hidden "),
	("kms_info_2n",  "unless the lord or town in question belongs to your faction."),
	("kms_info_2o",  " "),
	("kms_info_2p",  "2) Messages that are not hidden will be colored based on how this information benefits "),
	("kms_info_2q",  "or damages your kingdom.  Events that are beneficial will be green, ones that are "),
	("kms_info_2r",  "detrimental will be red and ones that are neither will be light blue."),
	("kms_info_2s",  " "),
	("kms_info_2t",  "3) The pop-up menus that appear notifying you of peace or war breaking out will now be "),
	("kms_info_2u",  "suppressed.  They will show up as a simple message in the message window with red (war) "),
	("kms_info_2v",  "or green (peace) coloring.  If your faction is involved the pop-up menu will still occur."),
	# Policies & Decrees
	("kms_info_3a",  "As the ruler of a kingdom you may now select specific aspects of your culture to match"),
	("kms_info_3b",  "your desired vision.  Within the 'Kingdom Management Report' found in the reports menu"),
	("kms_info_3c",  "under 'View Kingdom Reports' you'll see a list of options for domestic policies and royal"),
	("kms_info_3d",  "decrees.  You can access this screen when you are not a ruler, but changes can only"),
	("kms_info_3e",  "be kept if you are the leader of a faction."),
	("kms_info_3f",  " "),
	("kms_info_3g",  "DOMESTIC POLICIES:"),
	("kms_info_3h",  "These represent the main cultural influences of your kingdom and how it views various"),
	("kms_info_3i",  "aspects of life within the realm.  They may be changed at any time, but these options"),
	("kms_info_3j",  "are intended to stay fixed once set as ones culture does not generally shift rapidly."),
	("kms_info_3k",  "The policies will influence many aspects of the game from how much income your towns"),
	("kms_info_3l",  "can bring to how easily troops may desert from your party."),
	("kms_info_3m",  " "),
	("kms_info_3n",  "ROYAL DECREES:"),
	("kms_info_3o",  "The decrees represent situational changes that are generally not meant to be permanent."),
	("kms_info_3p",  "Some of the decrees make sense to leave enabled at all times and were put in as decrees"),
	("kms_info_3q",  "because they fit there better than having a slider option.  Others, such as war"),
	("kms_info_3r",  "taxation, would be quite harmful to your kingdom if left enabled for too long.  These"),
	("kms_info_3s",  "options are meant to reflect measures taken by the ruler to deal with short term issues."),
	# Dialog Options
	("kms_info_4a",  "Some new dialog options have been added for dealing with lords and kings."),
	("kms_info_4b",  " "),
	("kms_info_4c",  "Breaking a Mercenary Contract:"),
	("kms_info_4d",  "By speaking to the king you can now choose to end a mercenary contract.  You will "),
	("kms_info_4e",  "receive no pro-rated pay for doing so."),
	("kms_info_4f",  " "),
	("kms_info_4g",  "Declaring Independence:"),
	("kms_info_4h",  "Speaking to the leader of your faction you may choose to end your vassalage and will "),
	("kms_info_4i",  "have an option to keep or give back your fiefs.  If you leave and keep your fiefs you "),
	("kms_info_4j",  "will effectively be declaring independence, but expect this to instigate war with your "),
	("kms_info_4k",  "previous liege."),
	("kms_info_4l",  " "),
	("kms_info_4m",  "Ransoming a Lord (via dialog):"),
	("kms_info_4n",  "Whenever a lord is your captive, you may offer them the chance to ransom themselves "),
	("kms_info_4o",  "for a lesser amount.  If you meet the requirements, you may be able to try to "),
	("kms_info_4p",  "intimidate them into paying more than the usual amount, but this will have some "),
	("kms_info_4q",  "consequences."),
	("kms_info_4r",  " "),
	("kms_info_4s",  "Forcing a king to give up their claim to the throne:"),
	("kms_info_4t",  "If you manage to take a king prisoner and vastly out match their kingdom then you may "),
	("kms_info_4u",  "have a chance at coercing them into relinquishing their claim to the throne.  If "),
	("kms_info_4v",  "successful their kingdom will become a part of your own with all of their vassals "),
	("kms_info_4w",  "switching to your allegiance."),
	("kms_info_4x",  " "),
	("kms_info_4y",  "Offering Troops to a Vassal:"),
	("kms_info_4z",  "While speaking to a vassal you may offer to give them troops with a scaling relation "),
	("kms_info_4ab", "gain based on the quality and quantity of the troops that are given."),
	("kms_info_4ac", " "),
	("kms_info_4ad", "Exchanging fiefs (planned):"),
	("kms_info_4ae", "If you are speaking to a fellow vassal then you may be able to exchange fiefs with "),
	("kms_info_4af", "them provided that the deal is of a comparable nature.  Generally the person you are "),
	("kms_info_4ag", "offering a trade will expect to get the better deal."),
	# Morale System
	("kms_info_5a",  "A number of new factors influence how the mod's morale system works.  I wanted to get "),
	("kms_info_5b",  "the game away from native's design of simply everything being a positive except for "),
	("kms_info_5c",  "party size becoming a large negative."),
	("kms_info_5d",  " "),
	("kms_info_5e",  "Party Size - It makes more sense to me that folks would be happier having a large number "),
	("kms_info_5f",  "of allies than they would be fighting outnumbered.  Natively this is always a negative "),
	("kms_info_5g",  "value equal to the size of your party.  Now it functions as a positive effect with a "),
	("kms_info_5h",  "+1 per 8 troops benefit."),
	("kms_info_5i",  " "),
	("kms_info_5j",  "Leadership - This factor functions the same as it does in the native system applying a "),
	("kms_info_5k",  "positive benefit based upon your leadership score.  The only difference is that it is "),
	("kms_info_5l",  "now roughly 1/3rd as effective as it once was."),
	("kms_info_5m",  " "),
	("kms_info_5n",  "Food - This factor functions nearly the same as it does in the native system.  "),
	("kms_info_5o",  "Generally all of your different food types are added together and then you receive a "),
	("kms_info_5p",  "50% bonus on top of that.  Now you receive the listed benefit of each food type only "),
	("kms_info_5q",  "without the +50% bonus.  This is because the new storekeeper system allows you to "),
	("kms_info_5r",  "carry a much greater variety of food then you normally would have."),
	("kms_info_5s",  " "),
	("kms_info_5t",  "Days on the Road - To balance out the positive influences listed above now your party "),
	("kms_info_5u",  "morale will be limited by campaign length.  This factor will continually become more "),
	("kms_info_5v",  "negative the longer you spend outside of your owned lands, but will rapidly improve "),
	("kms_info_5w",  "when you are nearby or resting within your fief or those of your faction.  This "),
	("kms_info_5x",  "effect is capped at -50 to 0 morale."),
	("kms_info_5y",  " "),
	("kms_info_5z",  "Party Unity - Also balancing out morale is a measure of how well your party gets along.  "),
	("kms_info_5aa", "Whereas the changes to the party size factor benefits large parties, this unity factor "),
	("kms_info_5ab", "is more beneficial to smaller parties.  Party unity is capped at -40 to +40 morale.  "),
	("kms_info_5ac", "This value is generated from the following components:"),
	("kms_info_5ad", "    +3 for every point of leadership that you and your companions (combined) possess."),
	("kms_info_5ae", "    -1 for every 3 troops in your party from your own faction."),
	("kms_info_5af", "    -1 for every troop in your party from any other faction."),
	("kms_info_5ag", "    -2 for every mercenary in your party. "),
	("kms_info_5ah", " "),
	("kms_info_5ai", "Disabling the alternate party morale system:"),
	("kms_info_5aj", "If you dislike this method of calculating morale you can disable it and return to the "),
	("kms_info_5ak", "native system by visiting the main mod options under the 'camp' menu.  Then simply "),
	("kms_info_5al", "uncheck the option listed as 'Use Alternate Morale System'."),
	# Companion Advisors
	##########################################################################################################
	("kms_info_6a",  "While still in the system's infancy, my goal here is to improve the usefulness of "),
	("kms_info_6b",  "companions that might otherwise be left by the roadside.  Instead of discarding a "),
	("kms_info_6c",  "companion because they do not get along well with your current party you may instead "),
	("kms_info_6d",  "appoint them to an advisory role at one of your fiefs.  Advisors can be appointed by "),
	("kms_info_6e",  "speaking to your chief minister in your royal court.  They may be dismissed by speaking "),
	("kms_info_6f",  "to them directly."),
	("kms_info_6g",  " "),
	("kms_info_6h",  "Castle Steward:"),
	("kms_info_6aa", "This is the main advisor acting in your stead while you are unavailable.  Having a"),
	("kms_info_6ab", "steward gives you someone you can request advice on fief construction, the current"),
	("kms_info_6ac", "state of affairs and serves as a point of contact for quests generated from that "),
	("kms_info_6ad", "location.  If no steward is appointed then these quests will not activate."),
	("kms_info_6i",  " "),
	("kms_info_6j",  "Captain of the Guard:"),
	("kms_info_6ba", "Serving as the head of your fief's defensive forces, this advisor will have a hand "),
	("kms_info_6bb", "in garrison recruitment, training of your troops and commissioning of patrols to "),
	("kms_info_6bc", "protect your lands from bandits."),
	# Unused
	#("kms_info_7a",  " "),
	# Credits
	# ("kms_info_8a",  "This page being blank is a known issue awaiting the next save game breaking update to fix."),
	("kms_info_8a",  "While the works contained in this diplomacy system are largely my own there are several "),
	("kms_info_8b",  "aspects that were drawn from or inspired by works in other mods and I'd like to take "),
	("kms_info_8c",  "a moment to credit them here for their ideas."),
	("kms_info_8d",  " "),
	("kms_info_8e",  "Prophesy of Pendor (Mod)"),
	("kms_info_8f",  "Message filtering"),
	("kms_info_8g",  "Ransoming a lord via dialog."),
	("kms_info_8h",  "Gaining relation with a lord by giving them troops."),
	("kms_info_8i",  " "),
	("kms_info_8j",  "Floris Mod Pack (Mod)"),
	("kms_info_8k",  "Declaring Independence"),
	("kms_info_8l",  " "),
	("kms_info_8m",  "Diplomacy (Mod)"),
	("kms_info_8n",  "Exchanging fiefs with a fellow vassal. (planned)"),
	("kms_info_8na", "Regional patrols, garrison training & recruitment."),
	("kms_info_8o",  "The concept of appointing advisors even though our approach is different."),
	("kms_info_8p",  " "),
	# ("kms_info_8q",  "Individuals:"),
	# ("kms_info_8r",  "Deftech - Suggesting the message filtering system."),
	# ("kms_info_8s",  "Dienes - Suggesting numerous additions to the lord holdings & center notes screens."),
	# Placeholder
	("kms_info_9a",  "xxx"),
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