# Dynamic Troop Trees by Dunde, modified by Caba'drin.

from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *
from header_items import *
from header_presentations import *
from header_skills import *

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [	 
 
("copy_inventory", 
	[
		(store_script_param_1, ":source"),
		(store_script_param_2, ":target"),
		
		(troop_clear_inventory, ":target"),
		(troop_get_inventory_capacity, ":inv_cap", ":source"),
		(try_for_range, ":i_slot", 0, ":inv_cap"),
			(troop_get_inventory_slot, ":item", ":source", ":i_slot"),
			(troop_set_inventory_slot, ":target", ":i_slot", ":item"),
			(troop_get_inventory_slot_modifier, ":imod", ":source", ":i_slot"),
			(troop_set_inventory_slot_modifier, ":target", ":i_slot", ":imod"),
			(troop_inventory_slot_get_item_amount, ":amount", ":source", ":i_slot"),
			(gt, ":amount", 0),
			(troop_inventory_slot_set_item_amount, ":target", ":i_slot", ":amount"),
		(try_end), 
	]),

# script_get_troop_max_hp
# PURPOSE: Return the maximum health a troop should have in combat.
# EXAMPLE: (call_script, "script_get_troop_max_hp", ":troop_no"),
("get_troop_max_hp",
	[
		(store_script_param_1, ":troop_no"),
		
		(assign, ":max_health", 35),
		
		# Add in basic bonus from Ironflesh
		(store_skill_level, ":skill_ironflesh", skl_ironflesh, ":troop_no"),
		(store_mul, ":ironflesh_bonus", ":skill_ironflesh", 2),
		(val_add, ":max_health", ":ironflesh_bonus"),
		
		# Add in bonus from Strength.
		(store_attribute_level, ":STR", ":troop_no", ca_strength),
		(val_add, ":max_health", ":STR"),
		
		# Add in ability bonuses from Disciplined or Bloodlust.
		(call_script, "script_ce_troop_get_bonus_health", ":troop_no"), # combat_scripts.py
		(assign, ":extra_health", reg1),
		(val_add, ":max_health", ":extra_health"),
		# (try_begin),
			# (call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_BERSERKER),
			# (try_begin),
				# (neq, ":troop_no", "trp_player"),
				# (neg|is_between, ":troop_no", companions_begin, companions_end),
				# (assign, ":difficulty_constant", BERSERKER_BONUS_EASY),
			# (else_try),
				# (eq, "$mod_difficulty", GAME_MODE_EASY),
				# (assign, ":difficulty_constant", BERSERKER_BONUS_EASY),
			# (else_try),
				# (eq, "$mod_difficulty", GAME_MODE_HARD),
				# (assign, ":difficulty_constant", BERSERKER_BONUS_HARD),
			# (else_try),
				# (eq, "$mod_difficulty", GAME_MODE_VERY_HARD),
				# (assign, ":difficulty_constant", BERSERKER_BONUS_VERY_HARD),
			# (else_try),
				# (assign, ":difficulty_constant", BERSERKER_BONUS_NORMAL),
			# (try_end),
			# (store_mul, ":berserker_factor", ":skill_ironflesh", ":difficulty_constant"),
			# (store_mul, ":berserker_bonus", ":max_health", ":berserker_factor"),
			# (val_div, ":berserker_bonus", 100),
			# (val_add, ":max_health", ":berserker_bonus"),
		# (else_try),
			# (call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_DISCIPLINED),
			# (store_attribute_level, ":INT", ":troop_no", ca_intelligence),
			# ## TROOP SYNERGY EFFECT: BONUS_FORTITUDE (+8 INT)
			# (try_begin),
				# (call_script, "script_cf_ce_troop_has_ability", ":troop_no", BONUS_FORTITUDE),
			# (else_try),
				# (val_sub, ":INT", 8),
			# (try_end),
			# (val_max, ":INT", 0),
			# (store_div, ":disciplined_bonus", ":INT", 2),
			# (val_add, ":max_health", ":disciplined_bonus"),
		# (try_end),
		
		(assign, reg0, ":max_health"),
		(assign, reg1, ":extra_health"),
		# (assign, reg11, ":berserker_bonus"),
		# (assign, reg12, ":disciplined_bonus"),
	]),	

# script_trees_stamp_requirement_info
# PURPOSE: Used in presentation "all_troops" to create a line of information about a prerequisite in a slot.
# EXAMPLE: (call_script, "script_trees_stamp_requirement_info", ":troop_no", ":slot_no", ":pos_x", ":pos_y"),
("trees_stamp_requirement_info",
	[
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":slot_no", 2),
		(store_script_param, ":pos_x", 3),
		(store_script_param, ":pos_y", 4),
		
		(store_add, ":pos_x_col_2", ":pos_x", 30),
		
		(store_sub, reg21, ":slot_no", slot_troop_requirement_1),
		(val_add, reg21, 1),
		(str_store_string, s21, "@#{reg21}:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(troop_get_slot, ":prereq", ":troop_no", ":slot_no"),
		(try_begin),
			(neq, ":prereq", PREREQ_UNASSIGNED),
			(call_script, "script_ce_store_troop_requirement_string_to_s31", ":prereq"),
			(str_store_string, s21, "@{s31}"),

			## OBJ - LABEL - SUB-INFO
			(try_begin),
				(this_or_next|eq, ":prereq", PREREQ_UNIQUE_LOCATION),
				(this_or_next|eq, ":prereq", PREREQ_UNIQUE_LOCATION_UPGRADE),
				(eq, ":prereq", PREREQ_OWNER_ONLY),
				(troop_get_slot, ":unique_center", ":troop_no", slot_troop_unique_location),
				(str_store_party_name, s22, ":unique_center"),
				(str_store_string, s21, "@{s21}  ({s22})"),
			(else_try),
				(eq, ":prereq", PREREQ_ELITE_MERCENARY),
				(str_store_string, s21, "@{s21}  (Requires Chapterhouse)"),
			(else_try),
				(eq, ":prereq", PREREQ_DISHONORABLE),
				(str_store_string, s21, "@{s21}  (Negative Player Honor)"),
			(else_try),
				(eq, ":prereq", PREREQ_FRIEND),
				(assign, reg21, troop_prereq_friend_relation),
				(str_store_string, s21, "@{s21}  ({reg21}+ Center Relation)"),
			(else_try),
				(eq, ":prereq", PREREQ_ALLY),
				(assign, reg21, troop_prereq_ally_relation),
				(str_store_string, s21, "@{s21}  ({reg21}+ Center Relation)"),
			(else_try),
				(eq, ":prereq", PREREQ_LIEGE_RELATION),
				(assign, reg21, troop_prereq_liege_relation),
				(str_store_string, s21, "@{s21}  ({reg21}+ Liege Relation)"),
			(else_try),
				(eq, ":prereq", PREREQ_DISREPUTABLE),
				(str_store_string, s21, "@{s21}  (Recruitment reduces honour)"),
			(else_try),
				(eq, ":prereq", PREREQ_EXPENSIVE),
				(str_store_string, s21, "@{s21}  (Double recruitment cost)"),
			(else_try),
				(eq, ":prereq", PREREQ_DOPPELSOLDNER),
				(str_store_string, s21, "@{s21}  (Double wage)"),
			(try_end), 
		
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
	]),
	
# script_trees_stamp_ability_info
# PURPOSE: Used in presentation "all_troops" to create a line of information about an ability in a slot.
# EXAMPLE: (call_script, "script_trees_stamp_ability_info", ":troop_no", ":slot_no", ":pos_x", ":pos_y"),
("trees_stamp_ability_info",
	[
		(store_script_param, ":troop_no", 1),
		(store_script_param, ":slot_no", 2),
		(store_script_param, ":pos_x", 3),
		(store_script_param, ":pos_y", 4),
		
		(store_add, ":pos_x_col_2", ":pos_x", 30),
		
		(store_sub, reg21, ":slot_no", slot_troop_ability_1),
		(val_add, reg21, 1),
		(str_store_string, s21, "@#{reg21}:"),
        (call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x", ":pos_y", 0, gpu_left),
		(call_script, "script_gpu_resize_object", 0, 75),
		(troop_get_slot, ":ability", ":troop_no", ":slot_no"),
		(try_begin),
			(neq, ":ability", BONUS_UNASSIGNED),
			(call_script, "script_ce_store_troop_ability_string_to_s31", ":troop_no", ":ability"),
			(str_store_string, s21, "@{s31}"),
			
			## OBJ - LABEL - SUB-INFO
			(try_begin),
				(eq, ":ability", BONUS_DISCIPLINED),
				(call_script, "script_get_troop_max_hp", ":troop_no"),
				(str_store_string, s21, "@{s21}  (+{reg1} Health)"),
			(else_try),
				(eq, ":ability", BONUS_SAVAGERY),
				# Get our wielded weapon's proficiency.
				(assign, ":fear_effect", 10),
				(assign, ":prof", 0),
				(store_proficiency_level, ":prof", ":troop_no", wpt_one_handed_weapon),
				(store_proficiency_level, ":prof_twohand", ":troop_no", wpt_two_handed_weapon),
				(try_begin),
					(ge, ":prof_twohand", ":prof"),
					(assign, ":prof", ":prof_twohand"),
				(try_end),
				(store_proficiency_level, ":prof_polearm", ":troop_no", wpt_polearm),
				(try_begin),
					(ge, ":prof_polearm", ":prof"),
					(assign, ":prof", ":prof_polearm"),
				(try_end),
				(val_div, ":prof", 10),
				(val_add, ":fear_effect", ":prof"),
				(assign, reg21, ":fear_effect"),
				(str_store_string, s21, "@{s21}  (+{reg1}% Fear Effect)"),
			(else_try),
				(eq, ":ability", BONUS_RALLYING_STRIKE),
				(store_skill_level, reg21, skl_leadership, ":troop_no"),
				(val_mul, reg21, 4),
				(val_add, reg21, 20),
				(str_store_string, s21, "@{s21}  (+{reg21}% Courage)"),
			(else_try),
				(eq, ":ability", BONUS_BERSERKER),
				(call_script, "script_get_troop_max_hp", ":troop_no"),
				(str_store_string, s21, "@{s21}  (+{reg1} Health)"),
			(else_try),
				(eq, ":ability", BONUS_CHEAP),
				(str_store_string, s21, "@{s21}  (-40% Hiring Price)"),
			(else_try),
				(eq, ":ability", BONUS_COMMANDING_PRESENCE),
				(store_skill_level, reg21, skl_leadership, ":troop_no"),
				(val_div, reg21, 2),
				(val_add, reg21, 2),
				(str_store_string, s21, "@{s21}  (+{reg21}% Heal - Troops)"),
			(else_try),
				(eq, ":ability", BONUS_BLADEMASTER),
				(store_skill_level, reg21, skl_weapon_master, ":troop_no"),
				(val_mul, reg21, 2),
				(str_store_string, s21, "@{s21}  (+{reg21}% Damage - Bladed Melee)"),
			(else_try),
				(eq, ":ability", BONUS_MASTER_BOWMAN),
				(store_skill_level, reg21, skl_weapon_master, ":troop_no"),
				(val_mul, reg21, 2),
				(val_add, reg21, 8),
				(str_store_string, s21, "@{s21}  (+{reg21}% Damage - Bows)"),
			(else_try),
				(eq, ":ability", BONUS_SHARPSHOOTER),
				(store_skill_level, reg21, skl_weapon_master, ":troop_no"),
				(val_mul, reg21, 4),
				(val_add, reg21, 20),
				(str_store_string, s21, "@{s21}  (+{reg21}% Accuracy)"),
			(else_try),
				(eq, ":ability", BONUS_HARDY),
				(store_skill_level, reg21, skl_ironflesh, ":troop_no"),
				(str_store_string, s21, "@{s21}  (+{reg21}% Health Regen)"),
			(else_try),
				(eq, ":ability", BONUS_INSPIRING),
				(str_store_string, s21, "@{s21}  (+2 to Party Morale)"),
			(else_try),
				(eq, ":ability", BONUS_TAX_COLLECTOR),
				(str_store_string, s21, "@{s21}  (-4% Tax Inefficiency)"),
			(else_try),
				(eq, ":ability", BONUS_DEVOTED),
				(str_store_string, s21, "@{s21}  (-50% Troop Wages)"),
			(else_try),
				(eq, ":ability", BONUS_LOYAL),
				(str_store_string, s21, "@{s21}  (+20 to Troop Morale)"),
			(else_try),
				(eq, ":ability", BONUS_SCAVENGER),
				(str_store_string, s21, "@{s21}  (Improves Looting)"),
			(else_try),
				(eq, ":ability", BONUS_RAPID_RELOAD),
				(store_proficiency_level, reg21, ":troop_no", wpt_crossbow),
				(val_div, reg21, 3),
				(str_store_string, s21, "@{s21}  (+{reg21}% Reload Speed)"),
			(else_try),
				(eq, ":ability", BONUS_TACTICIAN),
				(store_skill_level, reg21, skl_tactics, ":troop_no"),
				(val_mul, reg21, 3),
				(str_store_string, s21, "@{s21}  (+{reg21}% Nearby Troop Damage)"),
			(try_end),
			
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":pos_x_col_2", ":pos_y", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 75),
		(try_end),
	]),
]


from util_wrappers import *
from util_scripts import *

                
def modmerge_scripts(orig_scripts):
	# process script directives first
	# process_script_directives(orig_scripts, scripts_directives)
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
