# Center Improvements (1.0) by Windyplains

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *
from header_parties import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

# NOTES ABOUT ADDING IMPROVEMENTS!

# To add an improvement you need to do the following steps:
# 1 - Add a new constant in improvements_constants.py.
# 2 - Add a new entry in script "get_improvement_details".
# 3 - If the improvement has alters rent/tariff income then an entry needs to be added to script "improvement_weekly_income".
# 4 - If the improvement has an upkeep then an entry needs to be added to script "improvement_get_upkeep".
# 5 - If the improvement has special prerequisites beyond cost or center type then an entry needs to be added to script "cf_improvement_can_be_built_here".
# 6 - If the improvement has unique completion benefits then an entry needs to be added to script "improvement_completion_benefits".
# 7 - If the improvement takes longer than the standard cost based time then make an entry in script "improvement_takes_additional_reg1_days".
# 8 - Finally add into the main code whatever the benefits are for the improvement.

scripts = [	

# script_get_improvement_details
# This script replaces the native script that acquires detailed information on any improvements for display purposes.
("get_improvement_details",
    [
		(store_script_param, ":improvement_no", 1),
		# s0    - Name
		# s1    - Description
		# reg0  - Cost
		# reg1  - Allowable locations
		# reg2  - Relation Boost
		
		(assign, ":initial_cost", 0),
		(assign, ":buildable_locations", imp_allowed_in_any),
		(assign, ":relation_change", 0),
		(assign, ":damage_immune", 0),
		
		(try_begin),
			(eq, ":improvement_no", slot_center_has_manor),
			(str_store_string, s0, "@Manor"),
			#                        ################################################################################
			(str_store_string, s1, "@A manor lets you rest at the village and pay your troops half wages while you \
									^rest.\
									^ \
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a Manor"),
			(assign, ":initial_cost",              8000),
			(assign, ":buildable_locations",       imp_allowed_in_village),
			(assign, ":relation_change",           0),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_fish_pond),
			(str_store_string, s0, "@Mill"),
			#                        ################################################################################
			(str_store_string, s1, "@A mill increases village prosperity by 5%.\
									^ \
									^ \
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a Mill"),
			(assign, ":initial_cost",              6000),
			(assign, ":buildable_locations",       imp_allowed_in_village),
			(assign, ":relation_change",           0),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_watch_tower),
			(str_store_string, s0, "@Watch Tower"),
			#                        ################################################################################
			(str_store_string, s1, "@A watch tower lets the villagers raise alarm earlier. The time it takes for \
									^enemies to loot the village increases by 50%.\
									^ \
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a Watch Tower"),
			(assign, ":initial_cost",              5000),
			(assign, ":buildable_locations",       imp_allowed_in_village),
			(assign, ":relation_change",           0),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_school),
			(str_store_string, s0, "@School"),
			#                        ################################################################################
			(str_store_string, s1, "@A school increases the loyality of the villagers to you by +1 every month. \
									^ \
									^ \
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a School"),
			(assign, ":initial_cost",              9000),
			(assign, ":buildable_locations",       imp_allowed_in_village),
			(assign, ":relation_change",           0),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_messenger_post),
			(str_store_string, s0, "@Messenger Post"),
			#                        ################################################################################
			(str_store_string, s1, "@A messenger post lets the inhabitants send you a message whenever enemies are \
									^nearby, even if you are far away from here.\
									^ \
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a Messenger Post"),
			(assign, ":initial_cost",              4000),
			(assign, ":buildable_locations",       imp_allowed_in_any),
			(assign, ":relation_change",           0),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_prisoner_tower),
			(str_store_string, s0, "@Prison Tower"),
			#                        ################################################################################
			(str_store_string, s1, "@A prison tower reduces the chance of captives held here running away \
									^successfully.\
									^ \
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a Prison Tower"),
			(assign, ":initial_cost",              7000),
			(assign, ":buildable_locations",       imp_allowed_in_walled_center),
			(assign, ":relation_change",           0),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_garrison),
			(str_store_string, s0, "@Garrison"),
			#                        ################################################################################
			(str_store_string, s1, 	"@A local garrison allows a village to hold out twice as long against raids, but \
									^costs a weekly upkeep of 100 denars for the troops stationed there.  Bandits \
									^will not be able to infest the village.\
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a Garrison"),
			(assign, ":initial_cost",              5000),
			(assign, ":buildable_locations",       imp_allowed_in_village),
			(assign, ":relation_change",           2),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_crops_of_grain),
			(str_store_string, s0, "@Field of Grain"),
			#                        ################################################################################
			(str_store_string, s1, "@Planting fields of grain will require 3 full bags of grain in your inventory \
									^or that of your storekeeper and will provide a one time payment of 5000 denars \
									^upon completion.  This can be done repeatedly.\
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a Field of Crops"),
			(assign, ":initial_cost",              100),
			(assign, ":buildable_locations",       imp_allowed_in_village_castle),
			(assign, ":relation_change",           0),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_armoury),
			(str_store_string, s0, "@Armoury"),
			#                        ################################################################################
			(str_store_string, s1, "@Building an armoury makes space for a stockpile of weapons and ammunition \
									^allowing siege defenders to have their ammunition regularly restocked during \
									^combat.  Additionally, an armoury allows for cheaper issuing of gear to new \
									^recruits reducing the training cost of new soldiers by 3%.  A weekly cost of \
									^100 denars is required to maintain the equipment in combat shape.\
									^ "),
			(str_store_string, s2, "@an Armoury"),
			(assign, ":initial_cost",              8000),
			(assign, ":buildable_locations",       imp_allowed_in_walled_center),
			(assign, ":relation_change",           0),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_small_marketplace),
			(str_store_string, s0, "@Marketplace"),
			#                        ################################################################################
			(str_store_string, s1, "@Building a marketplace encourages crafters to congregate in an organized \
									^location and boosts trade within an area.  This will increase your prosperity \
									^(+3%) and generate additional income (+5%).\
									^ \
									^ \
									^ "),
			(str_store_string, s2, "@a Marketplace"),
			(assign, ":initial_cost",              5000),
			(assign, ":buildable_locations",       imp_allowed_in_any),
			(assign, ":relation_change",           2),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_improved_roads),
			(str_store_string, s0, "@Improved Roads"),
			#                        ################################################################################
			(str_store_string, s1, "@Improving the roads of a settlement allows trade caravans easier access and \
									^improves the quality of the settlers lives.  This will improve your relation \
									^(+2) with the settlement, increase its income and allow the settlement to \
									^recover from an abnormally low prosperity twice as fast.\
									^ \
									^ "),
			(str_store_string, s2, "@improved roads"),
			(assign, ":initial_cost",              10000),
			(assign, ":buildable_locations",       imp_allowed_in_any),
			(assign, ":relation_change",           2),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_fire_brigade),
			(str_store_string, s0, "@Fire Brigade"),
			#                        ################################################################################
			(str_store_string, s1, "@Training the members of this community in the organization and execution of a \
									^fire brigade to quickly deliver water from a nearby water source to a damaged \
									^structure can reduce the chances of it being damaged during a raid.  Since \
									^everyone is expected to participate no additional cost is incurred.  As a \
									^non-structure this improvement cannot be damaged.\
									^ "),
			(str_store_string, s2, "@a Fire Brigade"),
			(assign, ":initial_cost",              2000),
			(assign, ":buildable_locations",       imp_allowed_in_any),
			(assign, ":relation_change",           1),
			(assign, ":damage_immune",             1),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_forge),
			(str_store_string, s0, "@Forge"),
			#                        ################################################################################
			(str_store_string, s1, "@Any village owns much of its independence to their blacksmith's capabilities \
									^to produce items that would otherwise need to be traded for.  Once a forge \
									^is built and maintained the town will have weapons and armor available for \
									^sale as well as an increased weekly income for the village elder.\
									^ \
									^ "),
			(str_store_string, s2, "@a Forge"),
			(assign, ":initial_cost",              5000),
			(assign, ":buildable_locations",       imp_allowed_in_village),
			(assign, ":relation_change",           2),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_merc_chapterhouse),
			(str_store_string, s0, "@Mercenary Chapterhouse"),
			#                        ################################################################################
			(str_store_string, s1, "@Creating a welcome haven for mercenary bands to setup a home in your town \
									^gives you a greater source of soldiers to call upon in time of need.  The \
									^number of available mercenaries is increased by 8 and the cost for their \
									^purchase is reduced by 40%.\
									^ \
									^ "),
			(str_store_string, s2, "@a mercenary chapterhouse"),
			(assign, ":initial_cost",              12000),
			(assign, ":buildable_locations",       imp_allowed_in_town),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_escape_tunnels),
			(str_store_string, s0, "@Escape Tunnels"),
			#                        ################################################################################
			(str_store_string, s1, "@A valiant lord never gives up his fief without a fight, but a wise lord makes \
									^sure he has a plan for surviving a losing battle.  Building escape tunnels \
									^that lead away from your castle gives you a strong chance of escaping \
									^undetected from a siege that has gone poorly.  These require regular upkeep \
									^to ensure they stay usable and are prone to caving in, but in a bad situation \
									^they may just keep your neck off of the headsman's block."),
			(str_store_string, s2, "@an escape tunnel"),
			(assign, ":initial_cost",              8000),
			(assign, ":buildable_locations",       imp_allowed_in_walled_center),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_trade_guilds),
			(str_store_string, s0, "@Guild of Merchants"),
			#                        ################################################################################
			(str_store_string, s1, "@The road to prosperity is more than simply keeping the roads safe for travel.  \
									^One must also encourage free trade and no one knows this business better than \
									^the merchants that have survived in this business throughout their lives.  \
									^Encouraging merchants to choose your town as a center of commerce improves \
									^its general income by 8% and raises the prosperity by 3%.\
									^ "),
			(str_store_string, s2, "@a guild of merchants"),
			(assign, ":initial_cost",              9000),
			(assign, ":buildable_locations",       imp_allowed_in_town),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_castle_library),
			(str_store_string, s0, "@Castle Library"),
			#                        ################################################################################
			(str_store_string, s1, "@Among the social elite knowledge is considered as much an asset as martial \
									^prowess.  With the rare addition of a library to your castle the word will \
									^spread to merchants that your town is in demand of their wares.  This also \
									^provides a quiet place for reading that doubles your reading progress for \
									^time spent resting here.\
									^ "),
			(str_store_string, s2, "@a castle library"),
			(assign, ":initial_cost",              4000),
			(assign, ":buildable_locations",       imp_allowed_in_walled_center),
			(assign, ":relation_change",           1),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_training_grounds),
			(str_store_string, s0, "@Training Grounds"),
			#                        ################################################################################
			(str_store_string, s1, "@During war a soldier constantly has their prowess and training challenged such \
									^that success is required for survival.  In times of peace, little such outlet \
									^exists for keeping an armies' instincts at the battle ready.  A training \
									^center provides such an outlet and allows a garrison captain to apply their \
									^training skill (-1%/point) as a direct discount to the cost of training new \
									^troops."),
			(str_store_string, s2, "@a training ground"),
			(assign, ":initial_cost",              7500),
			(assign, ":buildable_locations",       imp_allowed_in_walled_center),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_reinforced_walls),
			(str_store_string, s0, "@Reinforced Walls"),
			#                        ################################################################################
			(str_store_string, s1, "@While the lords of the realm vie for power, the peasants of the surrounding \
									^lands are simply trying to get by.  As armies appear on the horizon the safety \
									^of a strong, outer city wall can mean the difference between living to replant \
									^your fields or failing to see the next sunrise.  Reinforced walls reduce the \
									^chance of improvements taking damage during sieges, render your improvements \
									^immune to critical damage and extend the time to siege a center by 50%."),
			(str_store_string, s2, "@a reinforced wall"),
			(assign, ":initial_cost",              15000),
			(assign, ":buildable_locations",       imp_allowed_in_walled_center),
			(assign, ":relation_change",           2),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_fishery),
			(str_store_string, s0, "@Fishery"),
			#                        ################################################################################
			(str_store_string, s1, "@For villages located near rivers or a coastline it is always profitable to \
									^harvest the nearby waters for the bounty of food they can provide.  The \
									^availability of fishing allows for a greater degree of independence and \
									^growth increasing the income a village can sustain, raising the prosperity \
									^of the fief (+3) and lowering the cost of fish from the elder. \
									^ "),
			(str_store_string, s2, "@a Fishery"),
			(assign, ":initial_cost",              4000),
			(assign, ":buildable_locations",       imp_allowed_in_village),
			(assign, ":relation_change",           2),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_stables),
			(str_store_string, s0, "@Stables"),
			#                        ################################################################################
			(str_store_string, s1, "@Nearly every army that marches across the face of Calradia desires a strong \
									^cavalry such that their forces may break through the lines of their enemies.  In\
									^order to field such a fearsome display of mounted advesaries, though a noble \
									^must ensure these animals are cared for and have lodging just like their \
									^soldiers.  Providing stables increases the capacity for unassigned mounts in a \
									^center by 50% and even improves the growth of their ranks by 25%."),
			(str_store_string, s2, "@a Stable"),
			(try_begin),
				(party_slot_eq, "$current_town", slot_party_type, spt_town),
				(assign, ":initial_cost",             12000),
			(else_try),
				(party_slot_eq, "$current_town", slot_party_type, spt_castle),
				(assign, ":initial_cost",              8000),
			(else_try),
				(assign, ":initial_cost",              4000),
			(try_end),
			(assign, ":buildable_locations",       imp_allowed_in_any),
			(assign, ":relation_change",           1),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_horse_ranch),
			(str_store_string, s0, "@Horse Ranch"),
			#                        ################################################################################
			(str_store_string, s1, "@In a land where mounted combatants rule the battlefield, it is within the \
									^nearby villages where this advantage is born.  Ranches built to care for these \
									^future mounts improve the chance for a successful birth and raising.  This \
									^increases the overall production of battle-capable mounts by 100% with a good \
									^stock of these animals being sent to the village's controlling town.  Providing \
									^this kind of care does, however, require an investment of income to maintain."),
			(str_store_string, s2, "@a Horse Ranch"),
			(assign, ":initial_cost",              5000),
			(assign, ":buildable_locations",       imp_allowed_in_village),
			(assign, ":relation_change",           2),
			
		(else_try),
			(eq, ":improvement_no", slot_center_has_royal_forge),
			(str_store_string, s0, "@Royal Forge"),
			#                        ################################################################################
			(str_store_string, s1, "@Blacksmiths can be found in nearly any village, but true artisans of skill fit \
									^for royalty are a rare find.  Yet a workshop fit for their capabilities must \
									^first be created for skill alone cannot reshape raw materials into usable \
									^equipment.  Such a forge will cost you a weekly upkeep, but it will attract the \
									^services of a skilled artisan that can repair damaged items and create custom \
									^ones faster with less cost involved."),
			(str_store_string, s2, "@a royal forge"),
			(assign, ":initial_cost",              8000),
			(assign, ":buildable_locations",       imp_allowed_in_walled_center),
			(assign, ":relation_change",           0),
			
		# (else_try),
			# (eq, ":improvement_no", slot_center_has_moat),
			# (str_store_string, s0, "@Moat"),
			# (str_store_string, s1, "@Dug to restrict the placement of ladders, they also slow down a sieging army as attackers must waste time filling in the moats to gain access."),
			# (str_store_string, s2, "a moat"),
			# (assign, ":initial_cost",              5000),
			# (assign, ":buildable_locations",       imp_allowed_in_walled_center),
			
		(else_try),
			(assign, reg31, ":improvement_no"),
			(display_message, "@ERROR: Unknown improvement type #{reg31} requested at script_get_improvement_details.", gpu_red),
		(try_end),
		
		(assign, reg0, ":initial_cost"),
		(assign, reg1, ":buildable_locations"),
		(assign, reg2, ":relation_change"),
		(assign, reg3, ":damage_immune"),
	]),
	
# script_improvement_weekly_income
# This script gets inserted in the add_log_event script to catch any allied heroes you fight alongside.  This includes companions.
("improvement_weekly_income",
    [
		(store_script_param, ":center_no", 1),
		
		(assign, ":income_flat", 0),
		(assign, ":income_percent", 100),
		(assign, ":tariffs_flat", 0),
		(assign, ":tariffs_percent", 100),
		
		(try_for_range, ":improvement", native_improvements_begin, center_improvements_end),
			(this_or_next|is_between, ":improvement", native_improvements_begin, native_improvements_end),
			(is_between, ":improvement", center_improvements_begin, center_improvements_end),
			(party_slot_ge, ":center_no", ":improvement", cis_built),
			(call_script, "script_improvement_get_upkeep", ":center_no", ":improvement"),
			
			(val_add, ":income_flat", reg1),
			(val_add, ":income_percent", reg2),
			(val_add, ":tariffs_flat", reg3),
			(val_add, ":tariffs_percent", reg4),
		(try_end),
		
		(assign, reg1, ":income_flat"),
		(assign, reg2, ":income_percent"),
		(assign, reg3, ":tariffs_flat"),
		(assign, reg4, ":tariffs_percent"),
		
	]),
	
# script_improvement_get_upkeep
# This script gets inserted in the add_log_event script to catch any allied heroes you fight alongside.  This includes companions.
("improvement_get_upkeep",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":improvement_no", 2),
		
		(assign, ":income_flat", 0),
		(assign, ":income_percent", 0),
		(assign, ":tariffs_flat", 0),
		(assign, ":tariffs_percent", 0),
		
		(party_get_slot, ":center_type", ":center_no", slot_party_type),
		
		(try_begin),
			(eq, ":improvement_no", slot_center_has_manor),
			(party_slot_ge, ":center_no", slot_center_has_manor, cis_built),
			(val_add, ":income_flat", -50),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_prisoner_tower),
			(party_slot_ge, ":center_no", slot_center_has_prisoner_tower, cis_built),
			(val_add, ":income_flat", -50),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_garrison),
			(party_slot_ge, ":center_no", slot_center_has_garrison, cis_built),
			(val_add, ":income_flat", -100),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_armoury),
			(party_slot_ge, ":center_no", slot_center_has_armoury, cis_built),
			(val_add, ":income_flat", -100),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_merc_chapterhouse),
			(party_slot_ge, ":center_no", slot_center_has_merc_chapterhouse, cis_built),
			(val_add, ":income_flat", -45),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_stables),
			(party_slot_ge, ":center_no", slot_center_has_stables, cis_built),
			(try_begin),
				(party_slot_eq, ":center_no", slot_party_type, spt_town),
				(val_add, ":income_flat", -240),
			(else_try),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(val_add, ":income_flat", -160),
			(else_try),
				(val_add, ":income_flat", -80),
			(try_end),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_horse_ranch),
			(party_slot_ge, ":center_no", slot_center_has_horse_ranch, cis_built),
			(val_add, ":income_flat", -150),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_escape_tunnels),
			(party_slot_ge, ":center_no", slot_center_has_escape_tunnels, cis_built),
			(val_add, ":income_flat", -50),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_royal_forge),
			(party_slot_ge, ":center_no", slot_center_has_royal_forge, cis_built),
			(val_add, ":income_flat", -150),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_improved_roads),
			(party_slot_ge, ":center_no", slot_center_has_improved_roads, cis_built),
			(val_add, ":income_flat", 75),
			(eq, ":center_type", spt_town),
			(val_add, ":income_flat", 150),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_fishery),
			(party_slot_eq, ":center_no", slot_center_has_fishery, cis_built),
			(val_add, ":income_flat", 75),
			(party_slot_ge, ":center_no", slot_center_has_fishery, cis_damaged_20_percent),
			(val_add, ":income_flat", 30),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_small_marketplace),
			(party_slot_eq, ":center_no", slot_center_has_small_marketplace, cis_built),
			(val_add, ":income_percent", 5),
		(else_try),
			(eq, ":improvement_no", slot_center_has_small_marketplace),
			(party_slot_ge, ":center_no", slot_center_has_small_marketplace, cis_damaged_20_percent),
			(val_add, ":income_percent", 2),
		(try_end),
		(try_begin),
			(eq, ":improvement_no", slot_center_has_trade_guilds),
			(party_slot_eq, ":center_no", slot_center_has_trade_guilds, cis_built),
			(val_add, ":tariffs_percent", 8),
		(else_try),
			(eq, ":improvement_no", slot_center_has_trade_guilds),
			(party_slot_ge, ":center_no", slot_center_has_trade_guilds, cis_damaged_20_percent),
			(val_add, ":tariffs_percent", 4),
		(try_end),
		(assign, reg1, ":income_flat"),
		(assign, reg2, ":income_percent"),
		(assign, reg3, ":tariffs_flat"),
		(assign, reg4, ":tariffs_percent"),
		
	]),
	
# script_improvement_takes_additional_reg1_days
# When the amount of time calculated by menu "center_improve" is done for an improvement it uses (COST / 100)+3 days.  Certain improvements need more time than this since they have little to no cost.
("improvement_takes_additional_reg1_days",
    [
		(store_script_param, ":improvement", 1),
		
		(try_begin),
			(eq, ":improvement", slot_center_has_crops_of_grain),
			(assign, reg1, 60),
		(else_try),
			## Native default additional time.
			(assign, reg1, 0), # 3),
		(try_end),
	]),
	
# script_improvement_apply_special_cost
# Certain improvements when started in menu "center_improve" need a special cost applied.  This does so.
("improvement_apply_special_cost",
    [
		(store_script_param, ":improvement", 1),
		
		(try_begin),
			(eq, ":improvement", slot_center_has_crops_of_grain),
			(call_script, "script_cf_cms_storekeeper_has_x_of_y_item", 3, "itm_grain", 1),
		(try_end),
	]),

# script_improvement_completion_benefits
# Certain improvements when started in menu "center_improve" need a special cost applied.  This does so.
("improvement_completion_benefits",
    [
		(store_script_param, ":improvement", 1),
		(store_script_param, ":center_no", 2),
		
		(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
		
		(assign, ":cash", 0),
		(assign, ":relation", 0),
		(try_begin),
			(eq, ":improvement", slot_center_has_crops_of_grain),
			(party_slot_eq, ":center_no", ":improvement", cis_built), # Checking if this gets awarded twice.
			(val_add, ":cash", 5000),
			(party_set_slot, ":center_no", ":improvement", cis_unbuilt), # So this can be built again.
		(try_end),
		
		(try_begin),
			(eq, ":improvement", slot_center_has_merc_chapterhouse),
			(eq, ":troop_no", "trp_player"),
			(str_store_party_name, s21, ":center_no"),
			(dialog_box, "@It will take up to three days before the effects of your mercenary chapterhouse built in {s21} take effect.", "@Improvement Note"),
		(try_end),
		
		(try_begin),
			(this_or_next|eq, ":improvement", slot_center_has_forge),
			(eq, ":improvement", slot_center_has_fishery),
			(call_script, "script_refresh_village_merchant_inventory", ":center_no"),
		(try_end),
		
		(call_script, "script_get_improvement_details", ":improvement"),
		(val_add, ":relation", reg2),
		
		(try_begin),
			(gt, ":cash", 0),
			(party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
			(val_add, ":accumulated_rents", ":cash"),
			(party_set_slot, ":center_no", slot_center_accumulated_rents, ":accumulated_rents"),
		(try_end),
		
		(try_begin),
			(neq, ":relation", 0),
			(eq, ":troop_no", "trp_player"),
			(call_script, "script_change_player_relation_with_center", ":center_no", ":relation"),
		(try_end),
		
	]),

# script_improvement_prosperity_changes
# This script is inserted into the native script "get_center_ideal_prosperity" to determine the ideal prosperity of a center that it will drift 1 closer towards each day.
("improvement_prosperity_changes",
    [
		(store_script_param, ":center_no", 1),
		
		(assign, ":prosperity", 0),
		
		(try_begin),
			(is_between, ":center_no", villages_begin, villages_end),
			# (party_slot_ge, ":center_no", slot_center_has_fish_pond, cis_built), # Commented out since this is part of the native script.
			# (val_add, ":prosperity", 5),
			(party_slot_ge, ":center_no", slot_center_has_fish_pond, cis_damaged_20_percent),
			(val_add, ":prosperity", -3),
		(try_end),
		
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_has_small_marketplace, cis_built),
			(val_add, ":prosperity", 3),
		(else_try),
			(party_slot_ge, ":center_no", slot_center_has_small_marketplace, cis_damaged_20_percent),
			(val_add, ":prosperity", 1),
		(try_end),
		
		(try_begin),
			(party_slot_eq, ":center_no", slot_center_has_trade_guilds, cis_built),
			(val_add, ":prosperity", 3),
		(else_try),
			(party_slot_ge, ":center_no", slot_center_has_trade_guilds, cis_damaged_20_percent),
			(val_add, ":prosperity", 1),
		(try_end),
		
		(assign, reg1, ":prosperity"),
	]),
	
# script_cf_improvement_can_be_built_here
# This serves as a filter for sub_menus of menu "center_manage" instead of doing it individually there.
("cf_improvement_can_be_built_here",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":improvement", 2),
		
		# Verify this isn't currently in construction or already built.
		(neg|party_slot_eq, ":center_no", ":improvement", cis_built),
		(neg|party_slot_eq, ":center_no", slot_center_current_improvement_1, ":improvement"),
		(neg|party_slot_eq, ":center_no", slot_center_current_improvement_2, ":improvement"),
		(neg|party_slot_eq, ":center_no", slot_center_current_improvement_3, ":improvement"),
		
		# Count how many improvements are being built here.
		(assign, ":improvements_in_construction", 0),
		(try_for_range, ":improvement_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
			(neg|party_slot_eq, ":center_no", ":improvement_slot", 0),
			(val_add, ":improvements_in_construction", 1),
		(try_end),
		(store_sub, ":limit", slot_center_improvement_end_hour_1, slot_center_current_improvement_1),
		(lt, ":improvements_in_construction", ":limit"),
		
		# Ensure it can be built in this type of center.
		(call_script, "script_get_improvement_details", ":improvement"),
		(assign, ":allowable_locations", reg1),
		(party_get_slot, ":center_type", ":center_no", slot_party_type),
		(assign, ":continue", 0),
		(try_begin),
			(eq, ":allowable_locations", imp_allowed_in_any),
			(assign, ":continue", 1),
		(else_try),
			(eq, ":center_type", spt_village),
			(this_or_next|eq, ":allowable_locations", imp_allowed_in_village),
			(this_or_next|eq, ":allowable_locations", imp_allowed_in_village_town),
			(eq, ":allowable_locations", imp_allowed_in_village_castle),
			(assign, ":continue", 1),
		(else_try),
			(eq, ":center_type", spt_castle),
			(this_or_next|eq, ":allowable_locations", imp_allowed_in_castle),
			(this_or_next|eq, ":allowable_locations", imp_allowed_in_village_castle),
			(eq, ":allowable_locations", imp_allowed_in_walled_center),
			(assign, ":continue", 1),
		(else_try),
			(eq, ":center_type", spt_town),
			(this_or_next|eq, ":allowable_locations", imp_allowed_in_town),
			(this_or_next|eq, ":allowable_locations", imp_allowed_in_village_town),
			(eq, ":allowable_locations", imp_allowed_in_walled_center),
			(assign, ":continue", 1),
		(try_end),
		
		# Is there sufficient money available to build the improvement?
		(call_script, "script_improvement_get_building_time_and_cost", ":center_no", ":improvement"),
		(call_script, "script_cf_diplomacy_treasury_verify_funds", reg1, ":center_no", FUND_FROM_EITHER, TREASURY_FUNDS_AVAILABLE), # diplomacy_scripts.py
		
		(eq, ":continue", 1), ## CONDITIONAL BREAK ## (account for everything above)
		
		# Take into account special considerations such as items in inventory.
		(try_begin),
			(eq, ":improvement", slot_center_has_crops_of_grain),
			(party_slot_eq, ":center_no", slot_town_lord, "trp_player"), # I don't want the AI to need this.
			# Grain crops require that you or your storekeeper have 3 full bags of grain available to take for starting the crops.
			(assign, ":continue", 0),
			(call_script, "script_cf_cms_storekeeper_has_x_of_y_item", 3, "itm_grain", 0),
			(assign, ":continue", 1),
		(try_end),
		
		(try_begin),
			(eq, ":improvement", slot_center_has_trade_guilds),
			(assign, ":continue", 0),
			(party_slot_ge, ":center_no", slot_center_has_small_marketplace, cis_built),
			(party_slot_ge, ":center_no", slot_center_has_improved_roads, cis_built),
			(assign, ":continue", 1),
		(try_end),
		
		(try_begin),
			(eq, ":improvement", slot_center_has_fishery),
			(assign, ":continue", 0),
			(party_slot_ge, ":center_no", slot_center_fishing_fleet, 2),
			(assign, ":continue", 1),
		(try_end),
		
		(eq, ":continue", 1), ## CONDITIONAL BREAK ## (account for special requirements if any)
		
		(try_begin),
			(party_slot_ge, ":center_no", ":improvement", cis_built),
			(str_store_string, s3, "@Repair the"),
		(else_try),
			(str_store_string, s3, "@Build a"),
		(try_end),
	]),
	
# script_improvements_damaged_in_center
# Certain improvements when started in menu "center_improve" need a special cost applied.  This does so.
("improvements_damaged_in_center",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":attacking_party", 2),
		
		(str_store_party_name_link, s21, ":center_no"),
		(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
		
		## Questutil_simple_triggers.py - Check if noble recruits join the cause of the winner.
		(try_begin),
			(is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(eq, "$award_nobles_reasoning", 0),
			(eq, ":attacking_party", "p_main_party"),
			(call_script, "script_cf_qus_player_is_vassal", 1),
			(try_begin),
				(assign, "$award_nobles_reasoning", "str_noble_joins_due_to_siege"),
			(try_end),
		(else_try),
			# Give the AI some noble recruits.
			(is_between, ":center_no", walled_centers_begin, walled_centers_end),
			(neq, ":attacking_party", "p_main_party"),
			(party_get_slot, ":veterans", ":center_no", slot_center_veteran_ai),
			(val_add, ":veterans", 20),
			(party_set_slot, ":center_no", slot_center_veteran_ai, 20),
		(try_end),
		
		# Determine looting chance of critical damage.
		(assign, ":critical_chance", 0),
		(try_begin),
			# For the player use the highest party skill in looting.
			(eq, ":attacking_party", "p_main_party"),
			(call_script, "script_get_max_skill_of_player_party", "skl_looting"),
			(store_mul, ":critical_chance", 5, reg0),
			(val_div, ":critical_chance", 10),
		(else_try),
			# For everyone else check the main lord's looting skill, add some bonuses in as a minimum (+2) and add some in based on reputation type.
			(party_stack_get_troop_id, ":attacking_lord", ":attacking_party", 0),
			(troop_slot_eq, ":attacking_lord", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_eq, ":attacking_lord", slot_troop_leaded_party, ":attacking_party"), # Make sure this is the leader.
			(store_skill_level, reg0, "skl_looting", ":attacking_lord"),
			(store_mul, ":critical_chance", 5, reg0),
			(val_add, ":critical_chance", 10), # Every lord gets +1%.
			(try_begin), # Debauched, Roguish & Cunning get +1%
				(this_or_next|troop_slot_eq, ":attacking_lord", slot_lord_reputation_type, lrep_debauched),
				(this_or_next|troop_slot_eq, ":attacking_lord", slot_lord_reputation_type, lrep_roguish),
				(troop_slot_eq, ":attacking_lord", slot_lord_reputation_type, lrep_cunning), 
				(val_add, ":critical_chance", 10),
			(else_try),  # Martial gets +2%
				(troop_slot_eq, ":attacking_lord", slot_lord_reputation_type, lrep_martial),
				(val_add, ":critical_chance", 20),
			(else_try),  # Goodnatured & Upstanding lose 2%.
				(this_or_next|troop_slot_eq, ":attacking_lord", slot_lord_reputation_type, lrep_goodnatured),
				(troop_slot_eq, ":attacking_lord", slot_lord_reputation_type, lrep_upstanding),
				(val_add, ":critical_chance", -20),
			(try_end),
			(val_max, ":critical_chance", 0), # Make sure we're at least 0%.
			(val_div, ":critical_chance", 10),
		(try_end),
		
		(try_for_range, ":improvement", native_improvements_begin, center_improvements_end),
			# Prevent the need for two loops, but make sure we only affect improvement slots.
			(this_or_next|is_between, ":improvement", native_improvements_begin, native_improvements_end),
			(is_between, ":improvement", center_improvements_begin, center_improvements_end),
			# Is there an improvement built here?
			(party_get_slot, ":improvement_status", ":center_no", ":improvement"),
			(ge, ":improvement_status", cis_built),
			# Can this improvement be damaged?
			(call_script, "script_get_improvement_details", ":improvement"),
			(eq, reg3, 0), # Not damage immune.
			# Apply a random chance of it getting damaged or not.
			(assign, ":chance_of_damage", 80),
			(try_begin),
				(party_slot_eq, ":center_no", slot_center_has_fire_brigade, cis_built),
				(val_sub, ":chance_of_damage", 33),
			(try_end),
			(try_begin),
				(party_slot_ge, ":center_no", slot_center_has_reinforced_walls, cis_built),
				(party_get_slot, ":status", ":center_no", slot_center_has_reinforced_walls),
				(val_sub, ":status", 1),
				(val_mul, ":status", 4), # -4% effectiveness per point of damage up to -16%
				(store_sub, ":resist", 33, ":status"),
				(val_sub, ":chance_of_damage", ":resist"),
			(try_end),
			(store_random_in_range, ":roll", 0, 100),
			(lt, ":roll", ":chance_of_damage"),
			# Apply some damage to it.
			(val_add, ":improvement_status", 1),
			# Attempt to apply critical damage based upon looting skill.
			(try_begin),
				(party_slot_eq, ":center_no", slot_center_has_reinforced_walls, cis_unbuilt), # Reinforced walls are immune to critical damage.
				(store_random_in_range, ":crit_attempt", 0, 100),
				(lt, ":crit_attempt", ":critical_chance"),
				(val_add, ":improvement_status", 1),
				(ge, DEBUG_IMPROVEMENTS, 1),
				(str_store_party_name, s31, ":attacking_party"),
				(str_store_party_name, s32, ":center_no"),
				(assign, reg31, ":critical_chance"),
				(display_message, "@DEBUG (Improvements): {s31} has critically damaged {s0} in {s32}.  {reg31}% chance.", gpu_debug),
			(try_end),
			(try_begin),
				# If the improvement is fully damaged then it is destroyed and reset to 0.
				(gt, ":improvement_status", cis_damaged_80_percent),
				(assign, ":improvement_status", cis_unbuilt),
				# Let the player know about this.
				(eq, ":troop_no", "trp_player"),
				(call_script, "script_get_improvement_details", ":improvement"),
				(display_message, "@Your {s0} in {s21} has been destroyed.", gpu_red),
				(call_script, "script_change_player_relation_with_center", ":center_no", -2),
			(try_end),
			(party_set_slot, ":center_no", ":improvement", ":improvement_status"),
		(try_end),
		
	]),
	
# script_cf_improvement_get_priority_for_ai
# Given a counter, this script will return an improvement slot # to work on so that the AI intelligently builds/repairs improvements.
("cf_improvement_get_priority_for_ai",
    [
		(store_script_param, ":counter", 1),
		
		(assign, reg1, -1),
		(try_begin),
			(assign, ":count", 0),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_fish_pond),
		(else_try), 
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_fishery),
		(else_try), 
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_stables),
		(else_try), 
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_horse_ranch),
		(else_try), 
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_training_grounds),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_armoury),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_crops_of_grain),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_small_marketplace),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_improved_roads),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_escape_tunnels),
		(else_try), 
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_garrison),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_trade_guilds),
		(else_try), 
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_fire_brigade),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_reinforced_walls),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_watch_tower),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_prisoner_tower),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_school),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_manor),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_messenger_post),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_forge),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_castle_library),
		(else_try),
			(val_add, ":count", 1),
			(eq, ":counter", ":count"),
			(assign, reg1, slot_center_has_merc_chapterhouse),
		(try_end),
		
		(gt, reg1, 0), ## CONDITIONAL BREAK ##
	]),
	
# script_improvement_get_building_time_and_cost
# Will determine the cost of building an improvement for the AI based upon the player.
("improvement_get_building_time_and_cost",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":improvement_no", 2),
		
		(call_script, "script_get_improvement_details", ":improvement_no"),
		(assign, ":improvement_cost", reg0),
		(str_store_string, s4, s0),
		(str_store_string, s19, s1),
		(call_script, "script_get_max_skill_of_player_party", "skl_engineer"),
		(assign, ":max_skill", reg0),
		(assign, ":max_skill_owner", reg1),
		(assign, reg2, ":max_skill"),

		(store_sub, ":multiplier", 20, ":max_skill"),
		(val_mul, ":improvement_cost", ":multiplier"),
		(val_div, ":improvement_cost", 20),

		## WINDYPLAINS+ ## - Alter cost based upon current state (for repairing).
		(try_begin),
			(party_slot_ge, ":center_no", ":improvement_no", cis_damaged_20_percent),
			(assign, reg21, 0), # Repairing
			(party_get_slot, ":status_factor", ":center_no", ":improvement_no"),
			(val_sub, ":status_factor", 1),
			(val_mul, ":status_factor", 20),
			(val_mul, ":improvement_cost", ":status_factor"),
			(val_div, ":improvement_cost", 100),
			# BOOK EFFECT+: Factor in if the companion or player has read the guide to cheaper repairs book.
			(try_begin),
				(is_between, ":max_skill_owner", companions_begin, companions_end),
				(store_sub, ":companion_no", ":max_skill_owner", companions_begin),
				(store_add, ":book_read_slot", cms_reading_checklist, ":companion_no"),
				(item_slot_ge, "itm_book_repair_bonus", ":book_read_slot", 1000),             # Companion has read this book.
				(store_mul, ":discount", ":improvement_cost", 30),
				(val_div, ":discount", 100),
				(val_sub, ":improvement_cost", ":discount"),
			(else_try),
				(eq, ":max_skill_owner", "trp_player"),
				(item_slot_eq, "itm_book_repair_bonus", slot_item_book_read, 1), # Book has been read.
				(store_mul, ":discount", ":improvement_cost", 30),
				(val_div, ":discount", 100),
				(val_sub, ":improvement_cost", ":discount"),
			(try_end),
			# BOOK EFFECT-
		(else_try),
			(assign, reg21, 1), # Building
		(try_end),
		## WINDYPLAINS- ##
		(store_div, ":improvement_time", ":improvement_cost", 150), ## WINDYPLAINS+ ## Reduced construction time of improvements by 33%.  Native divided by 100.
		(call_script, "script_improvement_takes_additional_reg1_days", ":improvement_no"),
		(val_add, ":improvement_time", reg1),

		## WINDYPLAINS+ ## - Enhanced Diplomacy - Improvement cost & time adjustment.
		(store_faction_of_party, ":faction_no", ":center_no"),
		(faction_get_slot, ":diplomacy_cost_factor", ":faction_no", slot_faction_improvement_cost),
		(store_mul, ":diplomacy_cost_bonus", ":improvement_cost", ":diplomacy_cost_factor"),
		(val_div, ":diplomacy_cost_bonus", 100),

		(faction_get_slot, ":diplomacy_time_factor", ":faction_no", slot_faction_improvement_time),
		(store_mul, ":diplomacy_time_bonus", ":improvement_time", ":diplomacy_time_factor"),
		(val_div, ":diplomacy_time_bonus", 100),
		
		## WINDYPLAINS+ ## - Troop Effect - WATCHFUL EYE - Extends prisoner capacity.
		(try_begin),
			## ADVISOR CHECK: Castle Steward
			(assign, ":continue", 0),
			(try_begin),
				# This is a village, check if the bound steward has an engineering skill of 4+.
				(party_slot_eq, ":center_no", slot_party_type, spt_village),
				(party_get_slot, ":center_bound", ":center_no", slot_village_bound_center),
				(is_between, ":center_bound", walled_centers_begin, walled_centers_end),
				(party_get_slot, ":troop_steward", ":center_bound", slot_center_steward),
				(is_between, ":troop_steward", companions_begin, companions_end),
				(store_skill_level, ":skill_engineering", "skl_engineer", ":troop_steward"),
				(ge, ":skill_engineering", 4),
				(assign, ":continue", 1),
			(else_try),
				# This is a walled center, check if a steward is assigned.
				(this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
				(party_get_slot, ":troop_steward", ":center_no", slot_center_steward),
				(is_between, ":troop_steward", companions_begin, companions_end),
				(assign, ":continue", 1),
			(try_end),
			(eq, ":continue", 1),
			## TROOP EFFECT: BONUS_ENGINEER
			(call_script, "script_cf_ce_troop_has_ability", ":troop_steward", BONUS_ENGINEER), # combat_scripts.py - ability constants in combat_constants.py
			# Reduce buiding COST by 2% per point of Trade.
			(store_skill_level, ":skill_trade", "skl_trade", ":troop_steward"),
			(val_mul, ":skill_trade", 2),
			(store_mul, ":advisor_cost_bonus", ":improvement_cost", ":skill_trade"),
			(val_div, ":advisor_cost_bonus", -100),
			# Reduce building TIME by 2% per point of Engineering.
			(store_skill_level, ":skill_engineering", "skl_engineer", ":troop_steward"),
			(val_mul, ":skill_engineering", 2),
			(store_mul, ":advisor_time_bonus", ":improvement_time", ":skill_engineering"),
			(val_div, ":advisor_time_bonus", -100),
		(else_try),
			(assign, ":advisor_cost_bonus", 0),
			(assign, ":advisor_time_bonus", 0),
		(try_end),
		## WINDYPLAINS- ##

		# Diagnostic
		(try_begin),
			(eq, DEBUG_DIPLOMACY, 2), # Cost & time adjustment for building improvements (AI).  (verbose)
			(assign, reg31, ":improvement_cost"),
			(assign, reg32, ":diplomacy_cost_bonus"),
			(assign, reg33, ":diplomacy_cost_factor"),
			(store_add, reg34, ":improvement_cost", ":diplomacy_cost_bonus"),
			(assign, reg35, ":improvement_time"),
			(assign, reg36, ":diplomacy_time_bonus"),
			(assign, reg37, ":diplomacy_time_factor"),
			(store_add, reg38, ":improvement_time", ":diplomacy_time_bonus"),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@DEBUG (Diplomacy): {s0} cost in {s31} changed from {reg31} -> {reg34} denars.  [{reg32} change, {reg33}%].", gpu_debug),
			(display_message, "@DEBUG (Diplomacy): {s0} time in {s31} changed from {reg35} -> {reg38} denars.  [{reg36} change, {reg37}%].", gpu_debug),
		(try_end),
		
		(val_add, ":improvement_cost", ":diplomacy_cost_bonus"),
		(val_add, ":improvement_time", ":diplomacy_time_bonus"),
		
		# Diagnostic
		(try_begin),
			(eq, DEBUG_TROOP_ABILITIES, 2), # Cost & time adjustment for building improvements (AI).  (verbose)
			(lt, ":advisor_cost_bonus", 0),
			(assign, reg31, ":improvement_cost"),
			(assign, reg32, ":advisor_cost_bonus"),
			(store_add, reg34, ":improvement_cost", ":advisor_cost_bonus"),
			(assign, reg35, ":improvement_time"),
			(assign, reg36, ":advisor_time_bonus"),
			(store_add, reg38, ":improvement_time", ":advisor_time_bonus"),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@DEBUG (Abilities): {s0} cost in {s31} changed from {reg31} -> {reg34} denars.  [{reg32} change].", gpu_debug),
			(display_message, "@DEBUG (Abilities): {s0} time in {s31} changed from {reg35} -> {reg38} denars.  [{reg36} change].", gpu_debug),
		(try_end),
		
		(val_add, ":improvement_cost", ":advisor_cost_bonus"),
		(val_add, ":improvement_time", ":advisor_time_bonus"),
		
		## SILVERSTAG EMBLEM+ ##
		(try_begin),
			(is_presentation_active, "prsnt_hub_improvements"),
			
			## REDUCED COST
			(try_begin),
				(troop_slot_ge, HUB_OBJECTS, hub3_val_menu_emblem_build_cost, 1),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_menu_emblem_build_cost),
				(assign, ":reduction", 0),
				(try_begin),
					(eq, ":setting", EMBLEM_COST_REDUCE_BUILD_COST),
					(assign, ":reduction", 25),
				(else_try),
					(eq, ":setting", EMBLEM_COST_REDUCE_BUILD_COST*2),
					(assign, ":reduction", 50),
				(else_try),
					(eq, ":setting", EMBLEM_COST_FREE_BUILD_COST),
					(assign, ":reduction", 100),
				(else_try),
					(display_message, "@ERROR - Invalid cost reduction setting for improvement emblem bonus.", gpu_error),
				(try_end),
				(ge, ":reduction", 1),
				(store_mul, ":emblem_bonus", ":improvement_cost", ":reduction"),
				(val_div, ":emblem_bonus", 100),
				(val_sub, ":improvement_cost", ":emblem_bonus"),
				(val_max, ":improvement_cost", 0),
			(try_end),
			
			## REDUCED TIME
			(try_begin),
				(troop_slot_ge, HUB_OBJECTS, hub3_val_menu_emblem_build_time, 1),
				(troop_get_slot, ":setting", HUB_OBJECTS, hub3_val_menu_emblem_build_time),
				(assign, ":reduction", 0),
				(try_begin),
					(eq, ":setting", EMBLEM_COST_ENHANCE_BUILD_RATE),
					(assign, ":reduction", 25),
				(else_try),
					(eq, ":setting", EMBLEM_COST_ENHANCE_BUILD_RATE*2),
					(assign, ":reduction", 50),
				(else_try),
					(eq, ":setting", EMBLEM_COST_INSTANT_BUILD),
					(assign, ":reduction", 100),
				(else_try),
					(display_message, "@ERROR - Invalid time reduction setting for improvement emblem bonus.", gpu_error),
				(try_end),
				(ge, ":reduction", 1),
				(store_mul, ":emblem_bonus", ":improvement_time", ":reduction"),
				(val_div, ":emblem_bonus", 100),
				(val_sub, ":improvement_time", ":emblem_bonus"),
				(val_max, ":improvement_time", 0),
			(try_end),
		(try_end),
		## SILVERSTAG EMBLEM- ##
		
		# Output
		(assign, reg1, ":improvement_cost"),
		(assign, reg2, ":improvement_time"),
	]),

# script_improvement_store_ai_building_cost_to_reg1_and_time_to_reg2
# Will determine the cost of building an improvement for the AI based upon the lord's troop_no.
("improvement_store_ai_building_cost_to_reg1_and_time_to_reg2",
    [
		(store_script_param, ":improvement", 1),
		(store_script_param, ":center_no", 2),
		
		# Get the town lord.  Should already be filtered by the center # we are sent.
		(party_get_slot, ":troop_no", ":center_no", slot_town_lord),
		
		# Get base cost.
		(call_script, "script_get_improvement_details", ":improvement"),
		(assign, ":improvement_cost", reg0),
		
		# Modify cost based on troop engineering level.
		(store_skill_level, ":max_skill", "skl_engineer",":troop_no"),
		(store_sub, ":multiplier", 20, ":max_skill"),
		(val_mul, ":improvement_cost", ":multiplier"),
		(val_div, ":improvement_cost", 20),
		
		# Factor in if we're just repairing vs. building from scratch.
		(try_begin),
			(party_slot_ge, ":center_no", ":improvement", cis_damaged_20_percent),
			(party_get_slot, ":status_factor", ":center_no", ":improvement"),
			(val_sub, ":status_factor", 1),
			(val_mul, ":status_factor", 20),
			(val_mul, ":improvement_cost", ":status_factor"),
			(val_div, ":improvement_cost", 100),
		(try_end),
		
		# How long should this take us?
		(store_div, ":improvement_time", ":improvement_cost", 150), ## WINDYPLAINS+ ## Reduced construction time of improvements by 33%.  Native divided by 100.
		(call_script, "script_improvement_takes_additional_reg1_days", ":improvement"),
		(val_add, ":improvement_time", reg1),
		
		### ENHANCED DIPLOMACY+ ###
		(store_faction_of_party, ":faction_no", ":center_no"),
		(faction_get_slot, ":diplomacy_cost_factor", ":faction_no", slot_faction_improvement_cost),
		(store_mul, ":diplomacy_cost_bonus", ":improvement_cost", ":diplomacy_cost_factor"),
		(val_div, ":diplomacy_cost_bonus", 100),
		
		(faction_get_slot, ":diplomacy_time_factor", ":faction_no", slot_faction_improvement_time),
		(store_mul, ":diplomacy_time_bonus", ":improvement_time", ":diplomacy_time_factor"),
		(val_div, ":diplomacy_time_bonus", 100),
		
		# Diagnostic
		(try_begin),
			(eq, DEBUG_DIPLOMACY, 3), # Cost & time adjustment for building improvements (AI).  (verbose)
			(assign, reg31, ":improvement_cost"),
			(assign, reg32, ":diplomacy_cost_bonus"),
			(assign, reg33, ":diplomacy_cost_factor"),
			(store_add, reg34, ":improvement_cost", ":diplomacy_cost_bonus"),
			(assign, reg35, ":improvement_time"),
			(assign, reg36, ":diplomacy_time_bonus"),
			(assign, reg37, ":diplomacy_time_factor"),
			(store_add, reg38, ":improvement_time", ":diplomacy_time_bonus"),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@DEBUG (Diplomacy): {s0} cost in {s31} changed from {reg31} -> {reg34} denars.  [{reg32} change, {reg33}%].", gpu_debug),
			(display_message, "@DEBUG (Diplomacy): {s0} time in {s31} changed from {reg35} -> {reg38} denars.  [{reg36} change, {reg37}%].", gpu_debug),
		(try_end),
		
		(val_add, ":improvement_cost", ":diplomacy_cost_bonus"),
		(val_add, ":improvement_time", ":diplomacy_time_bonus"),
		### ENHANCED DIPLOMACY- ###
		
		(assign, reg1, ":improvement_cost"),
		(assign, reg2, ":improvement_time"),
	]),
	
# script_improvement_get_days_to_complete
# PURPOSE: Given a center & improvement # this will return how many days are left until completion via reg1.
("improvement_get_days_to_complete",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":improvement", 2),
		
		# We're given an improvement slot.
		(assign, ":building_slot", -1),
		(try_for_range, ":slot_no", slot_center_current_improvement_1, slot_center_improvement_end_hour_1),
			(party_slot_eq, ":center_no", ":slot_no", ":improvement"),
			(assign, ":building_slot", ":slot_no"),
			(break_loop),
		(try_end),
		(try_begin),
			(is_between, ":building_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1), # We have a valid slot.
			(store_add, ":time_slot", ":building_slot", 3),
			(party_get_slot, ":hours_left", ":center_no", ":time_slot"),
			(store_current_hours, ":current_hours"),
			(val_sub, ":hours_left", ":current_hours"),
			(store_div, ":days_left", ":hours_left", 24),
			(party_get_slot, ":improvement_no", ":center_no", ":building_slot"),
			(store_mod, ":remainder", ":hours_left", 24),
		(else_try),
			# Bad improvement data.
			(assign, ":improvement_no", -1),
			(assign, ":days_left", -1),
		(try_end),
		(assign, reg1, ":days_left"),
		(assign, reg2, ":improvement_no"),
		(assign, reg3, ":remainder"),
	]),
	
# script_building_slot_get_days_to_complete
# PURPOSE: Given a center & improvement building slot this will return how many days are left until completion via reg1.
("building_slot_get_days_to_complete",
    [
		(store_script_param, ":center_no", 1),
		(store_script_param, ":building_slot", 2),
		
		# We're given an improvement slot.
		(try_begin),
			(is_between, ":building_slot", slot_center_current_improvement_1, slot_center_improvement_end_hour_1), # We have a valid slot.
			(store_add, ":time_slot", ":building_slot", 3),
			(party_get_slot, ":hours_left", ":center_no", ":time_slot"),
			(store_current_hours, ":current_hours"),
			(val_sub, ":hours_left", ":current_hours"),
			(store_div, ":days_left", ":hours_left", 24),
			(party_get_slot, ":improvement_no", ":center_no", ":building_slot"),
		(else_try),
			# Bad slot data.
			(assign, ":days_left", -1),
			(assign, ":improvement_no", -1),
			(display_message, "@ERROR (improvements) - Invalid building slot used in script 'building_slot_get_days_to_complete'.", gpu_red),
		(try_end),
		(assign, reg1, ":days_left"),
		(assign, reg2, ":improvement_no"),
	]),
	
# script_castle_patrol_action
# Handles all scripts specific to the AI for prisoner caravans.
# INPUT: none
# OUTPUT: none
("castle_patrol_action",
    [
		(store_script_param, ":function", 1),
		(store_script_param, ":patrol", 2),
		(store_script_param, ":center_no", 3),
		
		(try_begin),
			(eq, ":function", castle_patrol_create),
			##### CREATE PARTY #####
			# Create the party
			(set_spawn_radius, 1),
			(spawn_around_party, ":center_no", "pt_patrol_party"),
			(assign, ":patrol", reg0),
			# Transfer 75% of the garrison to the patrol.
			(party_get_num_companion_stacks, ":num_stacks",":center_no"),
			(try_for_range, ":stack_no", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":stack_troop",":center_no",":stack_no"),
				(neg|troop_is_hero, ":stack_troop"),
				(party_stack_get_size, ":stack_size",":center_no",":stack_no"),
				(store_mul, ":modified_size", ":stack_size", 75),
				(val_div, ":modified_size", 100),
				(store_sub, ":left_behind", ":stack_size", ":modified_size"),
				(party_add_members, ":patrol", ":stack_troop", ":modified_size"),
				(party_stack_get_num_wounded, ":num_wounded", ":center_no", ":stack_no"),
				(party_remove_members, ":center_no", ":stack_troop", ":modified_size"),
				(store_sub, ":num_to_wound", ":num_wounded", ":left_behind"),
				(val_max, ":num_to_wound", 0),
				(gt, ":num_to_wound", 1),
				(party_wound_members, ":patrol", ":stack_troop", ":num_to_wound"),
			(try_end),
			(store_faction_of_party, ":faction_no", ":center_no"),
			(party_set_faction, ":patrol", ":faction_no"),
			# Name the caravan.
			(str_store_party_name, s13, ":center_no"),
			(party_set_name, ":patrol", "@Patrol from {s13}"),
			# Output variables.
			(party_set_slot, ":patrol", slot_party_caravan_origin, ":center_no"), 
			(party_set_slot, ":center_no", slot_center_patrol_party, ":patrol"),
			(assign, reg51, ":patrol"),
			
		(else_try),
			(eq, ":function", castle_patrol_merge_with_center),
			##### UNLOAD PRISONERS TO CENTER #####
			(call_script, "script_party_prisoners_add_party_prisoners", ":center_no", ":patrol"),  # Move prisoners from patrol to center.
			(call_script, "script_party_remove_all_prisoners", ":patrol"),
			
			##### REMOVE PARTY #####
			(party_set_slot, ":center_no", slot_center_patrol_party, -1),
			(assign, "$g_move_heroes", 0),
			(call_script, "script_party_add_party_companions", ":center_no", ":patrol"),
			(try_begin),
				(ge, DEBUG_QUEST_AI, 2),
				(str_store_party_name, s31, ":patrol"),
				(str_store_party_name, s32, ":center_no"),
				(display_message, "@DEBUG (Patrol AI): {s31} arrived in {s32} and has been removed.", gpu_debug),
			(try_end),
			(remove_party, ":patrol"),
			
		(else_try),
			(eq, ":function", castle_patrol_engage_party),
			##### TARGET INVADING PARTY #####
			(party_set_slot, ":patrol", slot_party_caravan_destination, ":center_no"),
			(party_set_ai_object, ":patrol", ":center_no"),
			(party_set_ai_behavior, ":patrol", ai_bhvr_attack_party),
			(party_set_slot, ":patrol", slot_party_ai_state, spai_engaging_army),
			(party_set_slot, ":patrol", slot_party_type, spt_patrol),
			(try_begin),
				(ge, DEBUG_QUEST_AI, 2),
				(str_store_party_name, s31, ":patrol"),
				(str_store_party_name, s32, ":center_no"),
				(display_message, "@DEBUG (Patrol AI): {s31} has departed to engage {s32}.", gpu_debug),
			(try_end),
			
		(else_try),
			(eq, ":function", castle_patrol_return_home),
			##### DIRECT TO DESTINATION #####
			(party_get_cur_town, ":current_center", ":patrol"),
			(try_begin),
				(ge, ":current_center", 0),
				(party_detach, ":patrol"),
			(else_try),
				(party_get_slot, ":current_center", ":patrol", slot_party_caravan_origin),
			(try_end),
			(party_set_ai_object, ":patrol", ":center_no"),
			(party_set_ai_behavior, ":patrol", ai_bhvr_travel_to_party),
			(party_set_slot, ":patrol", slot_party_ai_state, spai_retreating_to_center),
			(party_set_slot, ":patrol", slot_party_type, spt_patrol),
			(try_begin),
				(ge, DEBUG_QUEST_AI, 2),
				(str_store_party_name, s31, ":patrol"),
				(str_store_party_name, s32, ":center_no"),
				(display_message, "@DEBUG (Patrol AI): {s31} has broken pursuit and is returning back to {s32}.", gpu_debug),
			(try_end),
			
		(else_try),
			(assign, reg31, ":function"),
			(display_message, "@ERROR: script_castle_patrol_action failed on function #{reg31}.", qp_error_color),
		(try_end),
    ]),
	
# script_improvement_assess_center_value
# PURPOSE: Converts a basic center_no to a more descriptive name type and stores that in s1.
# EXAMPLE: (call_script, "script_improvement_assess_center_value", ":center_no"), # improvements_scripts.py (reg1 = built, reg2 = total value)
("improvement_assess_center_value",
	[
		(store_script_param, ":center_no", 1),
		
		(assign, ":improvements_built", 0),
		(assign, ":total_value", 0),
		(try_for_range, ":improvement_no", native_improvements_begin, center_improvements_end),
			(this_or_next|is_between, ":improvement_no", native_improvements_begin, native_improvements_end),
			(is_between, ":improvement_no", center_improvements_begin, center_improvements_end),
			(party_slot_ge, ":center_no", ":improvement_no", cis_built), # improvement built at all.
			(call_script, "script_get_improvement_details", ":improvement_no"),
			(assign, ":cost", reg0),
			(party_get_slot, ":status", ":center_no", ":improvement_no"),
			(store_sub, ":repair_factor", ":status", cis_built),
			(val_mul, ":repair_factor", 20),
			# Reduce improvement value by costs.
			(store_mul, ":repair_cost", ":cost", ":repair_factor"),
			(val_div, ":repair_cost", 100),
			(store_sub, ":improvement_value", ":cost", ":repair_cost"),
			# Update tallies.
			(val_add, ":total_value", ":improvement_value"),
			(val_add, ":improvements_built", 1),
		(try_end),
		
		(assign, reg1, ":improvements_built"),
		(assign, reg2, ":total_value"),
	]),
]

from util_wrappers import *
from util_scripts import *

scripts_directives = [
	#rename scripts to "insert" switch scripts (see end of scripts[])  
	[SD_RENAME, "get_improvement_details" , "get_improvement_details_orig"],
	# [SD_RENAME, "change_player_honor" , "change_player_honor_orig"],
	
	# HOOK: Maintain prosperity benefits of a center.
	[SD_OP_BLOCK_INSERT, "get_center_ideal_prosperity", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (val_max, ":ideal", 0), 0, 
		[(call_script, "script_improvement_prosperity_changes", ":center_no"),
		(val_add, ":ideal", reg1),], 1],
	
] # scripts_rename
                
def modmerge_scripts(orig_scripts):
	# process script directives first
	process_script_directives(orig_scripts, scripts_directives)
	# add remaining scripts
	add_scripts(orig_scripts, scripts, True)
	
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "scripts"
        orig_scripts = var_set[var_name_1]
    
        
		# START do your own stuff to do merging
		
        modmerge_scripts(orig_scripts)

		# END do your own stuff
        
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)