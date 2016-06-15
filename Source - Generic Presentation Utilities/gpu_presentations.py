# Tournament Play Enhancements (1.4) by Windyplains

from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
from header_items import *   # Added for Show all Items presentation.
from module_items import *   # Added for Show all Items presentation.
import string

####################################################################################################################
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################

presentations = [

# script_gpu_create_checkbox     - pos_x, pos_y, label, storage_slot, value_slot
# script_gpu_create_mesh         - mesh_id, pos_x, pos_y, size_x, size_y
# script_gpu_create_portrait     - troop_id, pos_x, pos_y, size, storage_id
# script_gpu_create_button       - title, pos_x, pos_y, storage_id
# script_gpu_create_text_label   - title, pos_x, pos_y, storage_id, design
# script_gpu_resize_object       - storage_id, percent size
# script_gpu_draw_line           - x length, y length, pos_x, pos_y, color
# script_gpu_container_heading   - pos_x, pos_y, size_x, size_y, storage_id
# script_gpu_create_slider       - min, max, pos_x, pos_y, storage_id, value_id


("gpu_dialog", 0, 0, [
  (ti_on_presentation_load,
    [
		(set_fixed_point_multiplier, 1000),
		(assign, "$gpu_storage", "trp_tpe_presobj"),
		(assign, "$gpu_data",    "trp_tpe_presobj"),
		#(store_mission_timer_a, "$gpu_last_dialog_update"),
		
		(presentation_set_duration, 3000),
		
		(call_script, "script_gpu_display_troop_dialog", "trp_player", 1, "str_hub_note_shift_multiplies", 5),
		(call_script, "script_gpu_display_troop_dialog", NPC_Odval, 2, "str_hub_note_shift_multiplies", 5),
		
    ]),
	
    (ti_on_presentation_event_state_change,
    [
        #(store_trigger_param_1, ":object"),
        #(store_trigger_param_2, ":value"),
		
	]),
	
	(ti_on_presentation_run,
    [
        (store_trigger_param_1, ":timer"),
        
		## UPPER TIMER ##
		(try_begin),
			(troop_slot_eq, "$gpu_storage", dialog_obj_upper_status, 1),
			(troop_get_slot, ":dialog_time", "$gpu_storage", dialog_obj_upper_updated_time),
			(store_sub, reg21, ":timer", ":dialog_time"),
			(store_mod, reg22, reg21, 1000),
			(eq, reg22, 0),
			(val_div, reg21, 1000),
			(str_store_string, s21, "@{reg21} sec"),
			(troop_get_slot, ":obj_timer", "$gpu_storage", dialog_obj_upper_timer),
			(overlay_set_text, ":obj_timer", "@{s21}"),
		(try_end),
		
		## LOWER TIMER ##
		(try_begin),
			(troop_slot_eq, "$gpu_storage", dialog_obj_lower_status, 1),
			(troop_get_slot, ":dialog_time", "$gpu_storage", dialog_obj_lower_updated_time),
			(store_sub, reg21, ":timer", ":dialog_time"),
			(store_mod, reg22, reg21, 1000),
			(eq, reg22, 0),
			(val_div, reg21, 1000),
			(str_store_string, s21, "@{reg21} sec"),
			(troop_get_slot, ":obj_timer", "$gpu_storage", dialog_obj_lower_timer),
			(overlay_set_text, ":obj_timer", "@{s21}"),
		(try_end),
		
	]),
	
	
  ]),

 ]
	
def modmerge_presentations(orig_presentations, check_duplicates = False):
    if( not check_duplicates ):
        orig_presentations.extend(presentations) # Use this only if there are no replacements (i.e. no duplicated item names)
    else:
    # Use the following loop to replace existing entries with same id
        for i in range (0,len(presentations)-1):
          find_index = find_object(orig_presentations, presentations[i][0]); # find_object is from header_common.py
          if( find_index == -1 ):
            orig_presentations.append(presentations[i])
          else:
            orig_presentations[find_index] = presentations[i]

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "presentations"
        orig_presentations = var_set[var_name_1]
        modmerge_presentations(orig_presentations)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)