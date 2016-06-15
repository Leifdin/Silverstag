# Quest Pack 2 (1.0) by Windyplains

from header_quests import *

quests = [

###########################################################################################################################
#####                                          QUEST PACK 2 (TRADE QUESTS)                                            #####
###########################################################################################################################

  ### QUEST: TRADE SHORTAGE ###
  # Trigger: During assessment of local trade prices in the marketplace menu.
  # Desc:    Player is prompted to bring a specific commodity to the target center for a large profit margin.
  ("floris_trade_shortage", "Exploit Shortage in {s13}", 0,
  "{!}A shortage of {s14} has occurred in {s13} that you should take advantage of before your competitors do."),
  
  ### QUEST: TRADE SURPLUS ###
  # Trigger: During assessment of local trade prices in the marketplace menu.
  # Desc:    Player is prompted to go to the target center and pick up a commodity determined to be in surplus at a substantial discount.
  ("floris_trade_surplus", "Exploit Surplus in {s13}", 0,
  "{!}A surplus of {s14} has occurred in {s13} that you should take advantage of before your competitors do."),
  
  ### QUEST: FORTUNE FAVORS THE BOLD ###
  # Trigger: During assessment of local trade prices in the marketplace menu.
  # Desc:    Player is prompted to repeat a trade route between two cities bringing each a specific commodity while under constant bandit raids.
  ("floris_trade_fortune_favors_bold", "Fortune Favors the Bold", 0,
  "{!}A lucrative trade route has formed between here and {s13}, but can you avoid the bandit patrols?"),
  
  ### QUEST: A NOBLE OPPORTUNITY ###
  ("trade_noble_opportunity", "A Noble Opportunity", 0,
  "{!}You have learned that {s9} is looking for a new investor to help fund raising an army for his latest ambition."),
  
  ### QUEST: DISCOUNT ENTERPRISE ###
  ("trade_discount_enterprise", "Discount Enterprise", 0,
  "{!}The store owner in {s13} is looking to sell his shop at a discounted price."),
  
  ## Trade quest ideas:
  # Risky Business - If you buy the enterprise in "Discount Enterprise" thugs may show up expecting you to make good on the last owner's debt.
  
  
  ("qp2_reserved_3", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp2_reserved_4", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp2_reserved_5", "Reserved Quest", 0,
  "{!}Quest Description"),
  
  ### END OF QUESTS ###
  ("quest_pack_2_end", "Quest Pack 2 End Quest", 0,
  "{!}Null - You should not be seeing this."),

  
###########################################################################################################################
#####                                         QUEST PACK 3 (NOBILITY QUESTS)                                          #####
###########################################################################################################################

  ### QUEST: SUMMONED TO HALL ###
  # Trigger: Daily chance of triggering.
  # Desc:    Odval wants you to listen to her story of why she's on the road and agree to help her clear her name.
  ("summoned_to_hall", "Summoned To Your Keep", 0,
  "{!}A messenger sent by your steward has requested your return to your home keep to deal with a matter of some importance."
  ),
  
  ### QUEST: PATROL FOR BANDITS ###
  # Trigger: Triggers upon returning to to visit your minister during "summoned_to_hall".
  # Desc:    This requires a player lord or king to remove at least four groups of bandits.
  ("patrol_for_bandits", "Patrol For Bandits", 0,
  "{!}You need to help your subjects by clearing the area of the rising bandit threat."
  ),
  
  ### QUEST: MERCS FOR HIRE ###
  # Trigger: Triggers upon returning to to visit your minister during "summoned_to_hall".
  # Desc:    This provides the player with the opportunity to have a party of mercenaries accompany them while it is active.
  ("mercs_for_hire", "Mercenary Contract", 0,
  "{!}You have entered into negotiation for a mercenary band to join your employment as long as their contract stands.  Fail to maintain their wages and they'll quickly abandon your cause though."
  ),
  
  ### QUEST: DESTROY THE LAIR ###
  # Trigger: Triggers upon returning to to visit your minister during "summoned_to_hall".
  # Desc:    This targets a nearby bandit lair as the source of troubles in the area for your fief.
  ("destroy_the_lair", "Root Them Out", 0,
  "{!}The alarming number of bandits in the area around your home suggests the existence of a hidden hideout that must be eliminated."
  ),
  
  ### QUEST: ESCORT TO MINE ###
  # Trigger: Triggers upon returning to to visit your minister during "summoned_to_hall".
  # Desc:    Greater than 40 prisoners available in walled center.
  ("escort_to_mine", "Escort Prisoners to Salt Mines", 0,
  "{!}In order to clear out the castle dungeons and generate a little extra revenue a prisoner caravan has been established to send to the salt mines."
  ),
  
  ("qp3_reserved_1", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp3_reserved_2", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp3_reserved_3", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp3_reserved_4", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp3_reserved_5", "Reserved Quest", 0,
  "{!}Quest Description"),
  
  ### END OF QUESTS ###
  ("quest_pack_3_end", "Quest Pack 3 End Quest", 0,
  "{!}Null - You should not be seeing this."),
  
  
###########################################################################################################################
#####                                        QUEST PACK 4 (COMPANION QUESTS)                                          #####
###########################################################################################################################

  ### QUEST: ODVAL INTRO ###
  # Trigger: During initial dialog with Nissa upon requesting to join the party.
  # Desc:    Nissa wants you to listen to her story of why she's on the road and agree to help her clear her name.
  ("odval_intro", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: ODVAL REDEMPTION ###
  # Trigger: Automatic upon success of qst_odval_intro.
  # Desc:    This is the main story arc of the Nissa companion.
  ("odval_redemption", "Nissa's Redemption", 0,
  "{!}Now that you've agreed to help Nissa, you must help her return to her town and clear her name."
  ),
  
  ### QUEST: ODVAL RETURN TO TULBUK ###
  # Trigger: Automatic upon success of qst_odval_intro.
  # Desc:    Nissa must return to her home village to speak to the village elder and face her accusers.
  ("odval_return_to_tulbuk", "Nissa Part I - Return to Village", 0,
  "{!}Now that you've agreed to help Nissa, you must travel with her back to her home town to speak with the village elder and face her accusers."
  ),
  
  ### QUEST: ODVAL ACCEPT THE CHALLENGE ###
  # Trigger: Upon success of qst_odval_return_to_tulbuk and agreeing to accept the accuser's challenge.
  # Desc:    You must stand with Nissa in combat against her accusers.
  ("odval_accept_the_challenge", "Nissa Part II - Accept The Challenge", 0,
  "{!}Nissa has demanded the right to face her accusers in combat in order to clear her name and has asked you stand by her side."
  ),
  
  ### QUEST: ODVAL SAVING FACE ###
  # Trigger: Upon success of qst_odval_accept_the_challenge and agreeing to accept Nissa's challenge.
  # Desc:    You must face Nissa in combat and help her save face.
  ("odval_saving_face", "Nissa Part III - Saving Face", 0,
  "{!}Now that you've agreed to help Nissa, you must travel with her back to her home town to speak with the village elder and face her accusers."
  ),
  
  ### QUEST: EDWYN INTRO ###
  # Trigger: During initial dialog with Edwyn upon requesting to join the party.
  # Desc:    Edwyn wants you to listen to his story of why he's on the road and agree to help him clear his name.
  ("edwyn_intro", "Edwyn's Introduction", 0,
  "{!}You've met a man drinking himself to his grave who is distraught over the savage deaths of his wife and daughter.  Can you find a way to bring him beyond the despair of his past?"
  ),
  
  ### QUEST: EDWYN REVENGE ###
  # Trigger: Automatic upon success of qst_odval_intro.
  # Desc:    This is the main story arc of the Edwyn companion.
  ("edwyn_revenge", "Edwyn's Revenge", 0,
  "{!}You've agreed to help Edwyn track down and eliminate the knights responsible for the destruction his home and the deaths of his family.  Nothing short of their demise will satisify his need for vengeance."
  ),
  
  ### QUEST: EDWYN FIRST KNIGHT ###
  # Trigger: Automatic upon success of qst_odval_intro.
  # Desc:    Odval must return to her home village to speak to the village elder and face her accusers.
  ("edwyn_first_knight", "Help Edwyn Kill Sir Tenry", 0,
  "{!}You need to track down the whereabouts of Sir Tenry Jerah.  He is one of the knights responsible for killing Edwyn's family and destroying his home.  Once found he should be eliminated."
  ),
  
  ### QUEST: EDWYN SECOND KNIGHT ###
  # Trigger: Upon success of qst_odval_return_to_tulbuk and agreeing to accept the accuser's challenge.
  # Desc:    You must stand with Odval in combat against her accusers.
  ("edwyn_second_knight", "Help Edwyn Kill Sir Henric", 0,
  "{!}You need to track down the whereabouts of Sir Henric Felkala.  He is one of the knights responsible for killing Edwyn's family and destroying his home.  Once found he should be eliminated."
  ),
  
  ### QUEST: EDWYN THIRD KNIGHT ###
  # Trigger: Upon success of qst_odval_accept_the_challenge and agreeing to accept Odval's challenge.
  # Desc:    You must face Odval in combat and help her save face.
  ("edwyn_third_knight", "Help Edwyn Kill Sir Gerrin", 0,
  "{!}You need to track down the whereabouts of Sir Gerrin Phelwin.  He is one of the knights responsible for killing Edwyn's family and destroying his home.  Once found he should be eliminated."
  ),
  
  ### END OF QUESTS ###
  ("quest_pack_4_end", "Quest Pack 4 End Quest", 0,
  "{!}Null - You should not be seeing this."
  ),
  

###########################################################################################################################
#####                                         QUEST PACK 6 (TUTORIAL QUESTS)                                           #####
###########################################################################################################################

  ### QUEST: EXPANDING YOUR TALENTS ###
  # Trigger: Triggers when you have an available ability slot that isn't assigned.
  # Desc:    Explains how to assign character abilities.
  ("qp6_expanding_your_talents", "Expanding Your Talents", 0,
  "{!}You have an open ability slot that needs assignment."),
  
  ### QUEST: STOREKEEPER ASSIGNMENT ###
  # Trigger: Triggers when you have a qualifying companion and no storekeeper is currently assigned.
  # Desc:    Explains how to assign a storekeeper and setup their shopping list.
  ("qp6_storekeeper_assignment", "Assigning a Storekeeper", 0,
  "{!}You have not yet assigned a companion to the storekeeper role, but have one that meets the qualifications."),
  
  ### QUEST: QUARTERMASTER ASSIGNMENT ###
  # Trigger: Triggers when you have a qualifying companion and no quartermaster is currently assigned.
  # Desc:    Explains how to assign a quartermaster.
  ("qp6_quartermaster_assignment", "Assigning a Quartermaster", 0,
  "{!}You have not yet assigned a companion to the quartermaster role, but have one that meets the qualifications."),
  
  ### QUEST: JAILER ASSIGNMENT ###
  # Trigger: Triggers when you have a qualifying companion and no gaoler is currently assigned.
  # Desc:    Explains how to assign a gaoler and setup their operating mode.
  ("qp6_jailer_assignment", "Assigning a Gaoler", 0,
  "{!}You have not yet assigned a companion to the gaoler role, but have one that meets the qualifications."),
  
  ("qp6_reserved_4", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp6_reserved_5", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp6_reserved_6", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp6_reserved_7", "Reserved Quest", 0,
  "{!}Quest Description"),
  
###########################################################################################################################
#####                                      QUEST PACK 7 (STORY-LINKED QUESTS)                                         #####
###########################################################################################################################

  ### QUEST: A FREEMAN'S RETURN ###
  # Trigger: Dialog triggered if you pay to free the fugitive in "qst_hunt_down_fugitive" and agree to escort him home.
  # Desc:    Simple escort to location & drop off.
  ("qp7_freemans_return", "A Freeman's Return", 0,
  "{!}You have agreed to escort your freed prisoner back to his home village."),
  
  ("qp7_reserved_1", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp7_reserved_2", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp7_reserved_3", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp7_reserved_4", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp7_reserved_5", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp7_reserved_6", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp7_reserved_7", "Reserved Quest", 0,
  "{!}Quest Description"),
  ("qp7_reserved_8", "Reserved Quest", 0,
  "{!}Quest Description"),
  
]

  
###########################################################################################################################
#####                                                 QUEST DIVISION                                                  #####
###########################################################################################################################  

###########################################################################################################################
#####                                         QUEST PACK 5 (VILLAGE QUESTS)                                           #####
###########################################################################################################################
quest_pack_5 = [
  ### QUEST: A CRAFTSMAN'S KNOWLEDGE ### (Slot: 288)
  # Trigger: Village elder quest menu.
  # Desc:    The local craftsman responsible for seeing an improvement in the village be completed has fallen ill and the elder wants you to take over construction.
  ("qp5_craftsmans_knowledge", "A Craftsman's Knowledge", 0,
  "{!}You have been asked to help aid in the completion of a construction project by the local village elder."
  ),
  
  ### QUEST: SENDING AID ### (Slot: 289)
  # Trigger: Village elder quest menu.
  # Desc:    None.
  ("qp5_sending_aid", "Sending Aid", 0,
  "{!}The local village elder has asked that you safely deliver supplies to a neighboring village that has recently been raided."
  ),
  
  ### QUEST: A HEALER'S TOUCH ### (Slot: 290)
  # Trigger: Village elder quest menu.
  # Desc:    None.
  ("qp5_healers_touch", "A Healer's Touch", 0,
  "{!}The village elder has asked for the help of your surgeon to deal with a condition one of his townsfolk faces."
  ),
  
  ### END OF QUESTS ###
  ("quest_pack_5_end", "Quest Pack 5 End Quest", 0,
  "{!}Null - You should not be seeing this."
  ),
  
  ### QUEST: WHEN LAMBS BECOME LIONS ### (Slot: 291)
  # Trigger: Village elder quest menu.
  # Desc:    None.
  ("qp5_when_lambs_become_lions", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: URGENT DELIVERY ###
  # Trigger: Village elder quest menu. (Slot: 292)
  # Desc:    None.
  ("qp5_urgent_delivery", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: PLACEHOLDER ###
  # Trigger: Village elder quest menu.
  # Desc:    None.
  ("qp5_q6", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: PLACEHOLDER ###
  # Trigger: Village elder quest menu.
  # Desc:    None.
  ("qp5_q7", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: PLACEHOLDER ###
  # Trigger: Village elder quest menu.
  # Desc:    None.
  ("qp5_q8", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: PLACEHOLDER ###
  # Trigger: Village elder quest menu.
  # Desc:    None.
  ("qp5_q9", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: PLACEHOLDER ###
  # Trigger: During initial dialog with Nissa upon requesting to join the party.
  # Desc:    None.
  ("qp5_q10", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: PLACEHOLDER ###
  # Trigger: During initial dialog with Nissa upon requesting to join the party.
  # Desc:    None.
  ("qp5_q11", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: PLACEHOLDER ###
  # Trigger: During initial dialog with Nissa upon requesting to join the party.
  # Desc:    None.
  ("qp5_q12", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
  
  ### QUEST: PLACEHOLDER ###
  # Trigger: During initial dialog with Nissa upon requesting to join the party.
  # Desc:    None.
  ("qp5_q13", "Nissa's Introduction", 0,
  "{!}You have met a young woman, named Nissa, on the run from her home village after being accused of cheating in an archery contest."
  ),
]

from util_common import *
from util_wrappers import *
def modmerge_quests(orig_quests):
	## QUEST PACKS 2, 3, 4 & 6
	pos = list_find_first_match_i(orig_quests, "quests_end")
	OpBlockWrapper(orig_quests).InsertBefore(pos, quests)
	## QUEST PACK 5 - VILLAGE QUESTS
	pos = list_find_first_match_i(orig_quests, "eliminate_bandits_infesting_village")
	OpBlockWrapper(orig_quests).InsertBefore(pos, quest_pack_5)	
	
def modmerge(var_set):
    try:
        var_name_1 = "quests"
        orig_quests = var_set[var_name_1]
        modmerge_quests(orig_quests)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)