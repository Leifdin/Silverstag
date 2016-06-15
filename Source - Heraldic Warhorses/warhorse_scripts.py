# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *
from module_items import items

from process_common import convert_to_identifier

def set_item_heraldic():
  item_heraldic = []
  for i_item in xrange(len(items)):
    type = items[i_item][3] & 0x000000ff
    if (type==itp_type_shield)|(type==itp_type_body_armor)|(type==itp_type_horse):
      if (len(items[i_item]))>8:
        if (len(items[i_item][8]))>0:
          item_heraldic.append((item_set_slot, i_item, slot_item_heraldic, 1))               
    if items[i_item][0].startswith("wse_"):
      native_id = items[i_item][0].replace("wse_","",1)
      j_item = find_object(items,convert_to_identifier(native_id))
      if (j_item > -1):
        item_heraldic.append((item_set_slot, i_item, slot_item_native_version,  j_item))        
        item_heraldic.append((item_set_slot, j_item, slot_item_wse_version, i_item))        
  return item_heraldic[:]

wse_warhorse_scripts = [

("init_heraldic_items", set_item_heraldic()),

("cf_troop_has_item",
 [(store_script_param_1, ":troop_no"),
  (store_script_param_2, ":item_no"),
  (assign, ":found", 0), 
  (try_begin),
     (neq, ":troop_no", "trp_player"),     
     (troop_get_inventory_capacity, ":inv_cap", ":troop_no"),
     (try_for_range, ":i_slot", 0, ":inv_cap"),
        (troop_get_inventory_slot, ":cur_item", ":troop_no", ":i_slot"),
        (eq, ":cur_item", ":item_no"),
        (assign, ":found", 1),
        (assign, ":inv_cap", 0),
     (try_end),      
  (else_try),
     (player_has_item, ":item_no"),
     (assign,":found", 1),   
  (try_end),   
  (eq, ":found", 1), ]),

("troop_remove_wse_items",
 [(store_script_param_1, ":troop_id"),
  (troop_sort_inventory, ":troop_id"),
  (troop_get_inventory_capacity, ":limit", ":troop_id"),
  (val_add, ":limit", 1),
  (try_for_range, ":inv_no", 0, ":limit"),
    (troop_get_inventory_slot, ":item_id", ":troop_id", ":inv_no"),
    (is_between, ":item_id", wse_only_begin, wse_only_end),
    (item_get_slot, ":native_version", ":item_id", slot_item_native_version),
    (gt, ":native_version", 0),
    (item_slot_eq, ":native_version", slot_item_wse_version, ":item_id"),
    (troop_set_inventory_slot, ":troop_id", ":inv_no", ":native_version"),
  (try_end),]), 
  
("troop_give_wse_items",
 [(store_script_param_1, ":troop_id"),
  (troop_sort_inventory, ":troop_id"),
  (troop_get_inventory_capacity, ":limit", ":troop_id"),
  (val_add, ":limit", 1),
  (try_for_range, ":inv_no", 0, ":limit"),
    (troop_get_inventory_slot, ":item_id", ":troop_id", ":inv_no"),
    (gt, ":item_id", 0),
    (item_get_slot, ":wse_version", ":item_id", slot_item_wse_version),
    (is_between, ":wse_version", wse_only_begin, wse_only_end),
    (item_slot_eq, ":wse_version", slot_item_native_version, ":item_id"),
    (troop_set_inventory_slot, ":troop_id", ":inv_no", ":wse_version"),
  (try_end),]),   

("check_wse_active_on_load",
 [(store_script_param_1, ":wse_disabled"),
  (try_begin),
    (this_or_next|eq, ":wse_disabled", 1),
    (is_vanilla_warband),
    (try_for_range, ":troop_id", kingdom_troops_begin,  kingdom_troops_end),    # Kingdom Soldiers
       (call_script, "script_troop_remove_wse_items", ":troop_id"),
    (try_end),
    (try_for_range, ":troop_id", mercenary_troops_begin,  mercenary_troops_end),    # Mercenaries Soldiers
       (call_script, "script_troop_remove_wse_items", ":troop_id"),
    (try_end), 
    (try_for_range, ":troop_id", armor_merchants_begin, village_elders_end),    # Merchants
       (call_script, "script_troop_remove_wse_items", ":troop_id"),
    (try_end),
    (try_for_range, ":troop_id", active_npcs_begin, active_npcs_end),           # NPCs
       (call_script, "script_troop_remove_wse_items", ":troop_id"),     
    (try_end), 
    (try_for_range, ":troop_id", quick_battle_troops_begin, quick_battle_troops_end),  
      (call_script, "script_troop_remove_wse_items", ":troop_id"),
    (try_end),
    (call_script, "script_troop_remove_wse_items", "trp_player"),
  (else_try),   
    (try_for_range, ":troop_id", kingdom_troops_begin,  kingdom_troops_end),    # Kingdom Soldiers
       (call_script, "script_troop_give_wse_items", ":troop_id"),
    (try_end),
    (try_for_range, ":troop_id", mercenary_troops_begin,  mercenary_troops_end),    # Mercenaries Soldiers
       (call_script, "script_troop_give_wse_items", ":troop_id"),
    (try_end),  
    (try_for_range, ":troop_id", armor_merchants_begin, village_elders_end),    # Merchants
       (call_script, "script_troop_give_wse_items", ":troop_id"),
    (try_end),
    (try_for_range, ":troop_id", active_npcs_begin, active_npcs_end),           # NPCs
       (call_script, "script_troop_give_wse_items", ":troop_id"),     
    (try_end), 
    (try_for_range, ":troop_id", quick_battle_troops_begin, quick_battle_troops_end),  
      (call_script, "script_troop_give_wse_items", ":troop_id"),
    (try_end),
    (call_script, "script_troop_give_wse_items", "trp_player"),
  (try_end), ]),

]

from util_wrappers import *
from util_scripts import *

scripts_directives = [
] # scripts_rename
                
def modmerge_scripts(orig_scripts):
	# process script directives first
	process_script_directives(orig_scripts, scripts_directives)
	# add remaining scripts
	add_scripts(orig_scripts, wse_warhorse_scripts, True)
	
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