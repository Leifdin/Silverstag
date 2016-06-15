from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
import string



####################################################################################################################
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################

wse_warhorse_presentations = [
("adjust_heraldic",0, mesh_load_window,
 [(ti_on_presentation_load,
   [(presentation_set_duration, 9999),
    (set_fixed_point_multiplier, 1000),
    # Title
    (position_set_y, pos1, title_pos_y), (position_set_x, pos1, title_pos_x),  # Title Position
    (position_set_x, pos2, title_size),  (position_set_y, pos2, title_size),   # Title Size
    (create_text_overlay, reg0, "str_banner_adjuster", tf_center_justify), (overlay_set_color, reg0, title_black),
    (overlay_set_position, reg0, pos1), (overlay_set_size, reg0, pos2),
    (position_set_y, pos1, title_pos_y-1),  (position_set_x, pos1, title_pos_x-1),  # Title Position
    (create_text_overlay, reg0, "str_banner_adjuster", tf_center_justify), (overlay_set_color, reg0, title_red),
    (overlay_set_position, reg0, pos1), (overlay_set_size, reg0, pos2),   
    # Create Static Texts
    (assign, ":cur_y", title_pos_y-50), (position_set_x, pos3, small_size), (position_set_y, pos3, small_size),
    (try_for_range, ":pointer", "str_param1", "str_banner_adjuster"),
       (store_sub, ":cur_y1", ":cur_y", 1),
       (create_text_overlay, reg0, ":pointer", tf_left_align), (overlay_set_color, reg0, title_black),
       (position_set_x, pos1,  35), (position_set_y, pos1, ":cur_y"),  (overlay_set_position, reg0, pos1), (overlay_set_size, reg0, pos3),   
       (create_text_overlay, reg0, ":pointer", tf_left_align), (overlay_set_color, reg0, title_yellow),
       (position_set_x, pos1,  34), (position_set_y, pos1, ":cur_y1"), (overlay_set_position, reg0, pos1), (overlay_set_size, reg0, pos3),   
       (val_sub, ":cur_y", 35),
    (try_end),
    # Create Objects
    (create_number_box_overlay,  "$g_presentation_obj_1", -500, 501),
    (create_number_box_overlay,  "$g_presentation_obj_2", -500, 501),
    (create_number_box_overlay,  "$g_presentation_obj_3", -500, 501),
    (create_number_box_overlay,  "$g_presentation_obj_4", -500, 501),
    (create_combo_label_overlay, "$g_presentation_obj_5"), #items
    (create_combo_label_overlay, "$g_presentation_obj_6"), #items
    (create_game_button_overlay, "$g_presentation_obj_20", "str_close", tf_center_justify),
    (try_begin),
       (eq, "$debug_heraldic", 0),
       (create_game_button_overlay, "$g_presentation_obj_21", "str_debug", tf_center_justify), 
    (else_try),
       (create_game_button_overlay, "$g_presentation_obj_21", "str_norm", tf_center_justify), 
    (try_end),
    # Rearrange Objects    
    (position_set_x, pos1, 290), (position_set_x, pos3, 600), (position_set_y, pos3, 600),
    (position_set_y, pos1, 595),      (overlay_set_position, "$g_presentation_obj_1",  pos1), (overlay_set_size, "$g_presentation_obj_1",  pos3),
    (position_set_y, pos1, 595-1*35), (overlay_set_position, "$g_presentation_obj_2",  pos1), (overlay_set_size, "$g_presentation_obj_2",  pos3),        
    (position_set_y, pos1, 595-2*35), (overlay_set_position, "$g_presentation_obj_3",  pos1), (overlay_set_size, "$g_presentation_obj_3",  pos3),
    (position_set_y, pos1, 595-3*35), (overlay_set_position, "$g_presentation_obj_4",  pos1), (overlay_set_size, "$g_presentation_obj_4",  pos3),
    (position_set_y, pos1, 595-6*35), (overlay_set_position, "$g_presentation_obj_5",  pos1), (overlay_set_size, "$g_presentation_obj_5",  pos3),
    (position_set_y, pos1, 595-5*35), (overlay_set_position, "$g_presentation_obj_6",  pos1), (overlay_set_size, "$g_presentation_obj_6",  pos3),
    # Rearrange Buttons
    (position_set_y, pos1, 25),  
    (position_set_x, pos1, 900),         (overlay_set_position, "$g_presentation_obj_20",  pos1),
    (position_set_x, pos1, 900 - 1*160), (overlay_set_position, "$g_presentation_obj_21",  pos1),
    # Values possible
    # Items
    (assign, ":heraldic_number", 0),
    (try_for_range, ":slot", 0, "itm_items_end"),
       (item_slot_eq, ":slot", slot_item_heraldic, 1),
       (val_add, ":heraldic_number", 1),
       (troop_set_slot, "trp_temp_array_a", ":heraldic_number", ":slot"),
    (try_end),
    (try_for_range, ":slot", wse_only_begin, wse_only_end),
       (val_add, ":heraldic_number", 1),
       (troop_set_slot, "trp_temp_array_a", ":heraldic_number", ":slot"),
    (try_end),    
    (troop_set_slot, "trp_temp_array_a", 0, ":heraldic_number"),
    (store_add, ":limit", ":heraldic_number", 1),
    (assign, ":active_slot", -1), 
    (try_for_range, ":slot", 1, ":limit"),
        (troop_get_slot, ":item", "trp_temp_array_a", ":slot"),
        (str_store_item_name, s0, ":item"),
        (overlay_add_item,  "$g_presentation_obj_5", s0),
        (eq, ":item", "$assigned_item"),
        (store_sub, ":active_slot", ":slot", 1),
    (try_end),
    (try_begin),
       (eq,  ":active_slot", -1), (assign, ":active_slot", 0),
       (troop_get_slot, "$assigned_item", "trp_temp_array_a", 1),
    (try_end),
    (overlay_set_val, "$g_presentation_obj_5", ":active_slot"), 
    # Troops
    (assign, ":heraldic_number", 0),
    (try_for_range, ":slot", kings_begin, lords_end),
       (val_add, ":heraldic_number", 1),
       (troop_set_slot, "trp_temp_array_b", ":heraldic_number", ":slot"),
    (try_end),
    (troop_set_slot, "trp_temp_array_b", 0, ":heraldic_number"),
    (store_add, ":limit", ":heraldic_number", 1),
    (assign, ":active_slot", -1), 
    (try_for_range, ":slot", 1, ":limit"),
        (troop_get_slot, ":item", "trp_temp_array_b", ":slot"),
        (str_store_troop_name, s0, ":item"),
        (overlay_add_item,  "$g_presentation_obj_6", s0),
        (eq, ":item", "$assigned_troop"),
        (store_sub, ":active_slot", ":slot", 1),
    (try_end),
    (try_begin),
       (eq,  ":active_slot", -1), (assign, ":active_slot", 0),
       (troop_get_slot, "$assigned_troop", "trp_temp_array_b", 1),
    (try_end),
    (overlay_set_val, "$g_presentation_obj_6", ":active_slot"),
        
    # Values
    (overlay_set_val, "$g_presentation_obj_1", "$heraldic_param1"), 
    (overlay_set_val, "$g_presentation_obj_2", "$heraldic_param2"), 
    (overlay_set_val, "$g_presentation_obj_3", "$heraldic_param3"), 
    (overlay_set_val, "$g_presentation_obj_4", "$heraldic_param4"), 
    # Pictures
    (try_begin),
      (gt,  "$assigned_item", 0),
      (create_mesh_overlay_with_item_id, reg0, "$assigned_item"),
      (position_set_x, pos1, 830), (position_set_y, pos1, 230), (position_set_x, pos3, 3000), (position_set_y, pos3, 3000),
      (overlay_set_position, reg0, pos1), (overlay_set_size, reg0, pos3),     
    (try_end), ]),    
    
  (ti_on_presentation_event_state_change, 
   [(store_trigger_param_1, ":object"),
    (store_trigger_param_2, ":value"),
    (set_fixed_point_multiplier, 1000),
    (assign, ":mul", 0),
    (assign, ":restart", 1),
    (try_begin),
       (key_is_down, key_left_shift),
       (assign, ":mul", 9),
    (try_end),
    (try_begin),
       (key_is_down, key_left_control),
       (val_add, ":mul", 99),
       (gt, ":mul", 100),
       (assign, ":mul", 999),
    (try_end),   
    (try_begin), 
       (eq, ":object",  "$g_presentation_obj_1"),
       (store_sub, ":diff", ":value", "$heraldic_param1"),
       (val_mul, ":diff", ":mul"),
       (val_add, ":value", ":diff"),
       (val_clamp, ":value", -500, 501),
       (assign, "$heraldic_param1", ":value"),
    (else_try),
      (eq, ":object",  "$g_presentation_obj_2"),
       (store_sub, ":diff", ":value", "$heraldic_param2"),
       (val_mul, ":diff", ":mul"),
       (val_add, ":value", ":diff"),
       (val_clamp, ":value", -500, 501),
       (assign, "$heraldic_param2", ":value"),
    (else_try),
       (eq, ":object",  "$g_presentation_obj_3"),
       (store_sub, ":diff", ":value", "$heraldic_param3"),
       (val_mul, ":diff", ":mul"),
       (val_add, ":value", ":diff"),
       (val_clamp, ":value", -500, 501),
       (assign, "$heraldic_param3", ":value"),
    (else_try),
       (eq, ":object",  "$g_presentation_obj_4"),
       (store_sub, ":diff", ":value", "$heraldic_param4"),
       (val_mul, ":diff", ":mul"),
       (val_add, ":value", ":diff"),
       (val_clamp, ":value", -500, 501),
       (assign, "$heraldic_param4", ":value"),
    (else_try),
      (eq, ":object",  "$g_presentation_obj_5"),
      (val_add, ":value", 1),
      (troop_get_slot, "$assigned_item", "trp_temp_array_a", ":value"),      
    (else_try),
      (eq, ":object",  "$g_presentation_obj_6"),
      (val_add, ":value", 1),
      (troop_get_slot, "$assigned_troop", "trp_temp_array_b", ":value"),
    (else_try),
       (eq, ":object",  "$g_presentation_obj_20"),
       (assign, ":restart", 0),
       (presentation_set_duration, 0),
    (else_try),
       (eq, ":object",  "$g_presentation_obj_21"),
       (store_sub, "$debug_heraldic", 1, "$debug_heraldic"),
    (else_try),    
       (assign, ":restart", 0),     
    (try_end),
    (eq, ":restart", 1),
    (start_presentation, "prsnt_adjust_heraldic"), ]),           
  ]),                

   ]
   
def modmerge_presentations(orig_presentations, check_duplicates = False):
    if( not check_duplicates ):
        orig_presentations.extend(wse_warhorse_presentations) # Use this only if there are no replacements (i.e. no duplicated item names)
    else:
    # Use the following loop to replace existing entries with same id
        for i in range (0,len(wse_warhorse_presentations)-1):
          find_index = find_object(orig_presentations, wse_warhorse_presentations[i][0]); # find_object is from header_common.py
          if( find_index == -1 ):
            orig_presentations.append(wse_warhorse_presentations[i])
          else:
            orig_presentations[find_index] = wse_warhorse_presentations[i]

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "presentations"
        orig_presentations = var_set[var_name_1]
        modmerge_presentations(orig_presentations)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)