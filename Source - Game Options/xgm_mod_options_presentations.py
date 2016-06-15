from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
import string

## xgm stuff
from xgm_mod_options_header import *
from xgm_mod_options import *


####################################################################################################################
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################

presentations = [
 ("mod_option", 0, mesh_load_window, [
	(ti_on_presentation_load,
       [
		## to be generated
	   ]),	
	(ti_on_presentation_event_state_change,
	   [
		(store_trigger_param_1, ":object"),
		(store_trigger_param_2, ":value"),
		## to be generated
	   ]),
	(ti_on_presentation_mouse_enter_leave, #Mouse-Over Pref-Tips
	   [
		(store_trigger_param_1, ":object"),
		(store_trigger_param_2, ":enter_leave"), #0 if mouse enters, 1 if mouse leaves
		## to be generated		
	   ]),
   ]),
] # presentations

from util_wrappers import *
from util_presentations import *

def generate_presentation_load_script(_mod_options = mod_options):
	opblock = OpBlockWrapper([])
	
	total_height = mod_options_get_total_height()
	if  total_height < xgm_mod_options_pane_height - xgm_mod_options_property_height/2:
		total_height = xgm_mod_options_pane_height - xgm_mod_options_property_height/2
	
	num_options = len(mod_options) #caba

	cur_posy = total_height
	cur_overlay_index = 0

	opblock.Append([
		(presentation_set_duration, 999999),
		(set_fixed_point_multiplier, 1000),

		(try_for_range, ":i", 0, num_options+1),
			(troop_set_slot, presobj_array, ":i", -1),
		(try_end),
		# (try_begin),
			# (party_slot_eq, "p_main_party", slot_party_pref_prefs_set, 0),
			# (call_script, "script_prebattle_set_default_prefs"),
			# (party_set_slot, "p_main_party", slot_party_pref_prefs_set, 1),
		# (try_end),
		
		(str_clear, s0),
		(create_text_overlay, overlay_var, s0, tf_scrollable),
		(position_set_x, pos1, xgm_mod_options_pane_posx),
		(position_set_y, pos1, xgm_mod_options_pane_posy),
		(overlay_set_position, overlay_var, pos1),
		(position_set_x, pos1, xgm_mod_options_pane_width),
		(position_set_y, pos1, xgm_mod_options_pane_height),
		(overlay_set_area_size, overlay_var, pos1),
		(set_container_overlay, overlay_var),
		(troop_set_slot, presobj_array, cur_overlay_index, overlay_var), #caba

		(position_set_x, pos1, xgm_mod_options_property_posx),    
	])
	
	cur_overlay_index += 1    

	for x in mod_options:
		aModOption = ModOptionWrapper(x)
		if aModOption.GetType() == xgm_ov_line:
			
			# Create line
			opblock.Append([
				(create_mesh_overlay, reg1, "mesh_white_plane"),
				(position_set_x, pos1, xgm_mod_options_line_width * 50),
				(position_set_y, pos1, xgm_mod_options_line_height * 50),
				(overlay_set_size, reg1, pos1),
				(position_set_x, pos1, xgm_mod_options_line_posx),
				(position_set_y, pos1, cur_posy + xgm_mod_options_line_offsety),
				(overlay_set_position, reg1, pos1),
				(overlay_set_color, reg1, 0x000000),
			])
		
		elif aModOption.GetType() in [xgm_ov_checkbox, xgm_ov_numberbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_slider, xgm_ov_title]:    
			# Create label
			labeltext = aModOption.GetTextLabel()

			if  (not labeltext is None) and ( labeltext <> "") and (aModOption.GetType() <> xgm_ov_title):	
				textflags = tf_vertical_align_center | aModOption.GetTextLabelFlags()                
				opblock.Append([
					(position_set_x, pos1, xgm_mod_options_property_label_posx),
					(create_text_overlay, reg0, "@%s" % aModOption.GetTextLabel(), textflags), #tf_vertical_align_center),
					(position_set_y, pos1, cur_posy),
					(overlay_set_position, reg0, pos1),
				])            
			# Create value           
			
			# Number box
			if( aModOption.GetType() == xgm_ov_numberbox ):
				opblock.Append([                       
					(position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_numberbox_offsetx),
					(create_number_box_overlay, overlay_var, aModOption.GetParameter(0), aModOption.GetParameter(1)),
					(position_set_y, pos1, cur_posy + xgm_ov_numberbox_offsety),
					(overlay_set_position, overlay_var, pos1),
					(position_set_x, pos1, xgm_ov_numberbox_scalex),
					(position_set_y, pos1, xgm_ov_numberbox_scaley),
					(overlay_set_size, overlay_var, pos1),
					(troop_set_slot, presobj_array, cur_overlay_index, overlay_var), #caba
				])            

				opblock.Append(aModOption.GetInitializeBlock()) # splice in initialize op block
				
				opblock.Append([                       
					(overlay_set_val, overlay_var, reg1),
				])                       
				cur_overlay_index += 1

			## WINDYPLAINS+ ## - Title Bar
			elif ( aModOption.GetType() == xgm_ov_title ):
				# textflags = tf_vertical_align_center | aModOption.GetTextLabelFlags() 
				opblock.Append([   
					(store_div, ":temp_offset", xgm_mod_options_line_offsety, 3),
					(val_mul, ":temp_offset", 2),
					(store_add, ":temp_y", cur_posy, ":temp_offset"),
					(store_sub, ":box_corner", cur_posy, ":temp_offset"),
					
					## Background Mesh
					(create_mesh_overlay, reg1, "mesh_white_plane"),
					(position_set_x, pos1, xgm_mod_options_line_width * 50),
					(position_set_y, pos1, 1600),
					(overlay_set_size, reg1, pos1),
					(position_set_x, pos1, xgm_mod_options_line_posx),
					(position_set_y, pos1, ":box_corner"),
					(overlay_set_position, reg1, pos1),
					(overlay_set_color, reg1, gpu_brown),
					
					## Top Line
					(create_mesh_overlay, reg1, "mesh_white_plane"),
					(position_set_x, pos1, xgm_mod_options_line_width * 50),
					(position_set_y, pos1, xgm_mod_options_line_height * 50),
					(overlay_set_size, reg1, pos1),
					(position_set_x, pos1, xgm_mod_options_line_posx),
					(position_set_y, pos1, ":temp_y"),
					(overlay_set_position, reg1, pos1),
					(overlay_set_color, reg1, 0x000000),
					
					## Title Text
					(position_set_x, pos1, xgm_mod_options_property_label_posx),
					(create_text_overlay, reg0, "@%s" % aModOption.GetTextLabel(), tf_vertical_align_center|tf_center_justify), #tf_vertical_align_center|tf_with_outline),
					(position_set_x, pos1, xgm_ov_titlebar_offsetx),
					(position_set_y, pos1, cur_posy),
					(overlay_set_position, reg0, pos1),
					(overlay_set_color, reg0, 0xFFFFFF),
					# Second copy to make it bold.
					(create_text_overlay, reg0, "@%s" % aModOption.GetTextLabel(), tf_vertical_align_center|tf_center_justify), #tf_vertical_align_center|tf_with_outline),
					(position_set_x, pos1, xgm_ov_titlebar_offsetx),
					(position_set_y, pos1, cur_posy),
					(overlay_set_position, reg0, pos1),
					(overlay_set_color, reg0, 0xFFFFFF),
					
					## Bottom Line
					(store_sub, ":temp_y", cur_posy, ":temp_offset"),
					(create_mesh_overlay, reg1, "mesh_white_plane"),
					(position_set_x, pos1, xgm_mod_options_line_width * 50),
					(position_set_y, pos1, xgm_mod_options_line_height * 50),
					(overlay_set_size, reg1, pos1),
					(position_set_x, pos1, xgm_mod_options_line_posx),
					(position_set_y, pos1, ":temp_y"),
					(overlay_set_position, reg1, pos1),
					(overlay_set_color, reg1, 0x000000),
				])    
				#cur_posy -= xgm_mod_options_property_height
			## WINDYPLAINS- ##
		
		# slider
			elif( aModOption.GetType() == xgm_ov_slider ):
				opblock.Append([                       
					(position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_slider_offsetx),
					(create_slider_overlay, overlay_var, aModOption.GetParameter(0), aModOption.GetParameter(1)),
					(position_set_y, pos1, cur_posy + xgm_ov_slider_offsety),
					(overlay_set_position, overlay_var, pos1),
					(position_set_x, pos1, xgm_ov_slider_scalex),
					(position_set_y, pos1, xgm_ov_slider_scaley),
					(overlay_set_size, overlay_var, pos1),
					(troop_set_slot, presobj_array, cur_overlay_index, overlay_var), #caba
				])            

				opblock.Append(aModOption.GetInitializeBlock()) # splice in initialize op block
				
				opblock.Append([                       
					(overlay_set_val, overlay_var, reg1),
				])                       
				cur_overlay_index += 1

			# Check box
			elif( aModOption.GetType() == xgm_ov_checkbox ):
				opblock.Append([                       
					(position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_checkbox_offsetx),
					(create_check_box_overlay, overlay_var, "mesh_checkbox_off", "mesh_checkbox_on"),
					(position_set_y, pos1, cur_posy + xgm_ov_checkbox_offsety),
					(overlay_set_position, overlay_var, pos1),
					(troop_set_slot, presobj_array, cur_overlay_index, overlay_var), #caba
				])            

				opblock.Append(aModOption.GetInitializeBlock()) # splice in initialize op block
				
				opblock.Append([                       
					(overlay_set_val, overlay_var, reg1),
					(position_set_x, pos1, xgm_ov_checkbox_scalex),
					(position_set_y, pos1, xgm_ov_checkbox_scaley),
					(overlay_set_size, overlay_var, pos1),
				])                       
				cur_overlay_index += 1
			
			
			elif( aModOption.GetType() == xgm_ov_combolabel ):
				opblock.Append([                       
					(position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_combolabel_offsetx),
					(create_combo_label_overlay, overlay_var),
					(position_set_y, pos1, cur_posy + xgm_ov_combolabel_offsety),
					(overlay_set_position,  overlay_var, pos1),
					(position_set_x, pos1, xgm_ov_combolabel_scalex),
					(position_set_y, pos1, xgm_ov_combolabel_scaley),
					(overlay_set_size, overlay_var, pos1),
					(troop_set_slot, presobj_array, cur_overlay_index, overlay_var), #caba
				])
				
				opblock.Append(aModOption.GetInitializeBlock()) # splice in initialize op block
				
				for aComboItem in aModOption.GetParameters():
					if (isinstance(aComboItem, str) and aComboItem.startswith("str_")) or (isinstance(aComboItem, int) and 0<=aComboItem<=67): #for strings "str_" and string regs sX
						opblock.Append([
							(overlay_add_item, overlay_var, aComboItem),
						]) ##Caba re-write
					else:
						opblock.Append([
							(overlay_add_item, overlay_var, "@%s" % aComboItem),
						])

				opblock.Append([                       
					(overlay_set_val, overlay_var, reg1),
				])                       
				cur_overlay_index += 1

			elif( aModOption.GetType() == xgm_ov_combobutton ):
				opblock.Append([                       
					(position_set_x, pos1, xgm_mod_options_property_value_posx + xgm_ov_combobutton_offsetx),
					(create_combo_button_overlay, overlay_var),
					(position_set_y, pos1, cur_posy + xgm_ov_combobutton_offsety),
					(overlay_set_position,  overlay_var, pos1),
					(position_set_x, pos1, xgm_ov_combobutton_scalex),
					(position_set_y, pos1, xgm_ov_combobutton_scaley),
					(overlay_set_size, overlay_var, pos1),
					(troop_set_slot, presobj_array, cur_overlay_index, overlay_var), #caba
				])
				
				opblock.Append(aModOption.GetInitializeBlock()) # splice in initialize op block
				
				params = aModOption.GetParameters()
				for aComboItem in params:
					if (isinstance(aComboItem, str) and aComboItem.startswith("str_")) or (isinstance(aComboItem, int) and 0<=aComboItem<=67): #for strings "str_" and string regs sX
						opblock.Append([
							(overlay_add_item, overlay_var, aComboItem),
						]) ##Caba re-write
					else:
						opblock.Append([
							(overlay_add_item, overlay_var, "@%s" % aComboItem),
						])

				opblock.Append([                       
					(overlay_set_val, overlay_var, reg1),
				])                       
				cur_overlay_index += 1			
			
			cur_posy -= xgm_mod_options_property_height

	opblock.Append([                       
		(set_container_overlay, -1),
		
		(create_text_overlay, overlay_var, "@Silverstag^Options", tf_center_justify),
		(position_set_x, pos1, 800),
		(position_set_y, pos1, 600),
		(overlay_set_position, overlay_var, pos1),
		(position_set_x, pos1, 2000),
		(position_set_y, pos1, 2000),
		(overlay_set_size, overlay_var, pos1),
		# Repeat for bold effect.
		(create_text_overlay, overlay_var, "@Silverstag^Options", tf_center_justify),
		(position_set_x, pos1, 800),
		(position_set_y, pos1, 600),
		(overlay_set_position, overlay_var, pos1),
		(position_set_x, pos1, 2000),
		(position_set_y, pos1, 2000),
		(overlay_set_size, overlay_var, pos1),
		
		(store_mul, ":mod_version", mod_version, 100),
		(val_add, ":mod_version", patch_version),
		
		(store_div, reg1, ":mod_version", 10000),
		(store_div, reg2, ":mod_version", 100),
		(store_mod, reg3, ":mod_version", 100),
		(try_begin),
			(lt, reg2, 10),
			(str_store_string, s2, "@0{reg2}"),
		(else_try),
			(str_store_string, s2, "@{reg2}"),
		(try_end),
		(try_begin),
			# (ge, BETA_TESTING_MODE, 1),
			(str_store_string, s2, "@{s2}.{reg3}"),
		(try_end),
		(str_store_string, s1, "@Version {reg1}.{s2}"),
		
		(create_text_overlay, overlay_var, s1, tf_center_justify),
		#(overlay_set_color, overlay_var, 0xFFFFFFFF),
		(position_set_x, pos1, 800),
		(position_set_y, pos1, 570),
		(overlay_set_position, overlay_var, pos1),
		(position_set_x, pos1, 900),
		(position_set_y, pos1, 900),
		(overlay_set_size, overlay_var, pos1),
		# Repeat for bold effect.
		(create_text_overlay, overlay_var, s1, tf_center_justify),
		#(overlay_set_color, overlay_var, 0xFFFFFFFF),
		(position_set_x, pos1, 800),
		(position_set_y, pos1, 570),
		(overlay_set_position, overlay_var, pos1),
		(position_set_x, pos1, 900),
		(position_set_y, pos1, 900),
		(overlay_set_size, overlay_var, pos1),
		
		## Mouse-over Tips	
		(str_store_string, s0, "@Mouse-over options for further information."),
		(create_text_overlay, mouse_over, s0, tf_double_space|tf_scrollable),
		(position_set_x, pos1, 650),
		(position_set_y, pos1, 200), # 350),
		(overlay_set_position, mouse_over, pos1),
		(position_set_x, pos1, 800),
		(position_set_y, pos1, 800),
		(overlay_set_size, mouse_over, pos1),
		(position_set_x, pos1, 300),
		(position_set_y, pos1, 350), # 200),
		(overlay_set_area_size, mouse_over, pos1),
			
		
		# This is for Done button
		(create_game_button_overlay, buttons_begin, "@Done"),
		(position_set_x, pos1, 900),
		(position_set_y, pos1, 25),
		(overlay_set_position, buttons_begin, pos1),
		
		(position_set_x, pos1, 740),
		(create_game_button_overlay, overlay_var, "@Restore Defaults", tf_center_justify),
		(overlay_set_position, overlay_var, pos1),	

		(position_set_x, pos1, 900),
		(position_set_y, pos1, 75),
		(create_game_button_overlay, overlay_var, "@Key Settings", tf_center_justify),
		(overlay_set_position, overlay_var, pos1),
		
	])    
	cur_overlay_index += 6  #was 1

	
	return opblock.Unwrap()
	
##############################    
def generate_presentation_event_state_change_script(_mod_options = mod_options):
	opblock = OpBlockWrapper([]) # this will contain the main switch handling changes from overlay values
	# opblock2 = OpBlockWrapper([])  # This will refresh all overlay values using the initialize blocks
	
	cur_overlay_index = 1 # start from 1 since 0 is the base option object
	
	opblock.Append([
		#(store_trigger_param_1, ":object"),
		#(store_trigger_param_2, ":value"),

		(try_begin),
			(neq, 1, 1), # dummy
	])
	
	for x in mod_options:
		aModOption = ModOptionWrapper(x)
		if aModOption.GetType() == xgm_ov_line:
			# Create line
			pass # noop                        
		elif aModOption.GetType() in [xgm_ov_checkbox, xgm_ov_numberbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_slider]:
			# Number box

			if aModOption.GetType() in [xgm_ov_numberbox, xgm_ov_checkbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_slider]: # redundant condition. place holder for now

				opblock.Append([                       
					(else_try),                
						#(eq, ":object", overlay_var),
						(troop_slot_eq, presobj_array, cur_overlay_index, ":object"),
						(assign, reg1, ":value"), # placed here instead of at the top in case reg1 is unknowingly overwritten                    
				])            

				opblock.Append(aModOption.GetUpdateBlock()) # splice in update block
		
				# opblock2.Append(aModOption.GetInitializeBlock())                
				# opblock2.Append([                       
					# (troop_get_slot, overlay_var, presobj_array, cur_overlay_index),
					# (overlay_set_val, overlay_var, reg1),
				# ])                       

				cur_overlay_index += 1

	opblock.Append([                       
		(else_try),
			(eq, ":object", buttons_begin),
			(presentation_set_duration, 0),
			(try_begin),		  
				(eq, "$g_is_quick_battle", 1),
				(assign, "$g_is_quick_battle", 0),
				(start_presentation, "prsnt_game_custom_battle_designer"),
			(try_end),
		(else_try),
			(store_add, ":overlay", buttons_begin, 1),
			(eq, ":object", ":overlay"),
			(call_script, "script_initialize_default_settings"),	
			(try_begin),		  
				(eq, "$g_is_quick_battle", 1),
				(presentation_set_duration, 0),
			(try_end),
			(start_presentation, "prsnt_mod_option"),
		(else_try),
			(val_add, ":overlay", 1),
			(eq, ":object", ":overlay"),
			(try_begin),		  
				(eq, "$g_is_quick_battle", 1),
				(presentation_set_duration, 0),
			(try_end),
			(start_presentation, "prsnt_pbod_redefine_keys"),
		(try_end),
	])    
	cur_overlay_index += 1 #???? 

	
	return opblock.Unwrap()#+opblock2.Unwrap()
	
##############################    
def generate_presentation_mouse_enter_leave_script(_mod_options = mod_options): ##Caba addition
	opblock = OpBlockWrapper([]) # this will contain the main switch handling changes from overlay values
	
	cur_overlay_index = 1 # start from 1 since 0 is the base option object
	
	opblock.Append([
		#(store_trigger_param_1, ":object"),
		#(store_trigger_param_2, ":enter_leave"), #0 if mouse enters, 1 if mouse leaves
		(try_begin),
			(eq, ":enter_leave", 1),
			#Clear String...or do nothing?
		(else_try),
			(eq, ":enter_leave", 0),
			(try_begin),
				(neq, 1, 1), # dummy
	])
	
	for x in mod_options:
		aModOption = ModOptionWrapper(x)
		if aModOption.GetType() == xgm_ov_line:
			# Create line
			pass # noop                        
		elif aModOption.GetType() in [xgm_ov_checkbox, xgm_ov_numberbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_slider]:
			# Number box

			if aModOption.GetType() in [xgm_ov_numberbox, xgm_ov_checkbox, xgm_ov_combolabel, xgm_ov_combobutton, xgm_ov_slider]: # redundant condition. place holder for now
				opblock.Append([                       
					(else_try),    
						(troop_get_slot, overlay_var, presobj_array, cur_overlay_index),
						(val_sub, overlay_var, 1),
						(this_or_next|eq, ":object", overlay_var),
						(troop_slot_eq, presobj_array, cur_overlay_index, ":object"),                     
				])            

				if isinstance(aModOption.GetDescription(), str) and aModOption.GetDescription():
					opblock.Append([				
						(overlay_set_text, mouse_over, "@%s" % aModOption.GetDescription()),				
					]) 

				cur_overlay_index += 1

	opblock.Append([                       
			(else_try),
				(overlay_set_text, mouse_over, "@Mouse-over options for further information."),	
			(try_end),
		(try_end),
	])    
	cur_overlay_index += 1 #???? 

	
	return opblock.Unwrap()

##############################

from util_scripts import *

def generate_presentations():
	try:
		find_i = list_find_first_match_i( presentations, "mod_option" )
		prsnt_mod_option = PresentationWrapper(presentations[find_i])

		codeblock = prsnt_mod_option.FindTrigger(ti_on_presentation_load).GetOpBlock()
		codeblock.Append(
			generate_presentation_load_script()
		)
		

		codeblock = prsnt_mod_option.FindTrigger(ti_on_presentation_event_state_change).GetOpBlock()
		codeblock.Append(
			generate_presentation_event_state_change_script()
		)

		codeblock = prsnt_mod_option.FindTrigger(ti_on_presentation_mouse_enter_leave).GetOpBlock()
		codeblock.Append(
			generate_presentation_mouse_enter_leave_script()
		)

	except:
		import sys
		print "Injecton failed:", sys.exc_info()[1]
		raise

##############################    

generate_presentations() # call to generate stuff
	
def modmerge_presentations(orig_presentations):
	
	# add remaining presentations
	from util_common import add_objects
	num_appended, num_replaced, num_ignored = add_objects(orig_presentations, presentations)
	#print num_appended, num_replaced, num_ignored


# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
	try:
		var_name_1 = "presentations"
		orig_presentations = var_set[var_name_1]	
		
		# START do your own stuff to do merging
		
		modmerge_presentations(orig_presentations)

		# END do your own stuff
		
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)
	