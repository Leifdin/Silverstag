# jrider's updated presentations (1.2)

from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
from module_constants import *
from header_skills import *

import string

####################################################################################################################
#  Each presentation record contains the following fields:
#  1) Presentation id: used for referencing presentations in other files. The prefix prsnt_ is automatically added before each presentation id.
#  2) Presentation flags. See header_presentations.py for a list of available flags
#  3) Presentation background mesh: See module_meshes.py for a list of available background meshes
#  4) Triggers: Simple triggers that are associated with the presentation
####################################################################################################################

presentations = [

  # Jrider +
  # REPORTS PRESENTATIONS 1.2 :
  # Factions relations presentation report
  ("jrider_faction_relations_report", 0,
   mesh_load_window,
   [
     (ti_on_presentation_load,
      [
    (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        # Embed picture upper right
        (create_mesh_overlay, reg1, "mesh_pic_castledes"),
        (position_set_x, pos1, 180),
        (position_set_y, pos1, 180),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, 795),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),

        # Embed picture upper left
        (create_mesh_overlay, reg1, "mesh_pic_looted_village"),
        (position_set_x, pos1, 170),
        (position_set_y, pos1, 170),
        (overlay_set_size, reg1, pos1),
        (position_set_x, pos1, -15),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg1, pos1),

		# Presentation title, centered at the top
		(str_store_string, s21, "@_Faction Relations Report_"),
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 680, 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 150),
		# Doubled for bold effect.
		(call_script, "script_gpu_create_text_label", "str_hub_s21", 500, 680, 0, gpu_center),
		(call_script, "script_gpu_resize_object", 0, 150),
		
		(create_button_overlay, reg1, "@_Return_"),
		(position_set_x, pos1, 465),
		(position_set_y, pos1, 33),
		(overlay_set_position, reg1, pos1),
		(assign, "$g_jrider_faction_report_Return_to_menu", reg1),

		# Set Headlines
		#set column title
		(assign, ":x_poshl", 250),  
		(assign, ":y_pos", 620),
		(position_set_y, pos1, ":y_pos"),
		(try_for_range, ":faction", kingdoms_begin, kingdoms_end),
			(faction_slot_eq, ":faction", slot_faction_state, sfs_active), # continue if active
			(try_begin),
				(is_between, ":faction", npc_kingdoms_begin, npc_kingdoms_end),
				(store_sub, ":offset", ":faction", "fac_kingdom_1"),
				(val_add, ":offset", "str_swadians"),
				(str_store_string, s1, ":offset"),    
			(else_try),
				(str_store_string, s1, "@Your kingdom"),    
			(try_end),
			
			## OBJ - FACTION NAME - COLUMNS
			(str_store_string, s21, s1),
			(store_add, ":x_temp", ":x_poshl", 38),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_pos", 0, gpu_center),
			#(overlay_set_color, reg1, ":faction_color"),
			(call_script, "script_gpu_resize_object", 0, 80),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_hub_s21", ":x_temp", ":y_pos", 0, gpu_center),
			#(overlay_set_color, reg1, ":faction_color"),
			(call_script, "script_gpu_resize_object", 0, 80),
			
			
			(val_add, ":x_poshl", 90),
		(try_end),


		(assign, ":x_poshl", 215),
		(assign, ":y_pos", 597),
		(assign, ":headline_size", 0),
		(position_set_x, ":headline_size", 720),
		(position_set_y, ":headline_size", 775),

		(assign, ":hl_columnsep_size", 50),
		(position_set_x, ":hl_columnsep_size", 60),
		(position_set_y, ":hl_columnsep_size", 28000),

		(create_text_overlay, reg2, "@Player^Relation", tf_center_justify),
		(overlay_set_size, reg2, ":headline_size"),
		(position_set_x, pos1, ":x_poshl"),
		(position_set_y, pos1, ":y_pos"),
		(overlay_set_position, reg2, pos1),

        (val_add, ":x_poshl", 45),
		(try_for_range, ":count", 0, 7),
			# create a separator column
			(create_mesh_overlay, reg1, "mesh_white_plane"),
			(overlay_set_color, reg1, gpu_gray), # 0x000000),
			(overlay_set_size, reg1, ":hl_columnsep_size"),      
			(store_sub, ":line_x", ":x_poshl", 15), # set it 21 pix left of current column start
			(store_sub, ":y_pos2", ":y_pos", 500), # set it 21 pix left of current column start
			(position_set_x, pos2, ":line_x"),
			(position_set_y, pos2, ":y_pos2"),
			(overlay_set_position, reg1, pos2),
			(val_add, ":x_poshl", 90),

			(try_begin),
				(eq, "$cheat_mode", 1),
				(assign, reg20, ":count"),
				(display_message, "@{!}DEBUG - Drawing line {reg20}"),
			(try_end),
		(try_end),

		# clear the string globals that we'll use
		(str_clear, s9),
		(str_clear, s8),
		(str_clear, s3),
		(str_clear, s60),
		(str_clear, s61),
		(str_clear, s0),

        # Scrollable area (all the next overlay will be contained in this, s0 sets the scrollbar)
        (create_text_overlay, reg1, s0, tf_scrollable_style_2),
        (position_set_x, pos1, 50),
        (position_set_y, pos1, 70),
        (overlay_set_position, reg1, pos1),
        (position_set_x, pos1, 860),
        (position_set_y, pos1, 527),
        (overlay_set_area_size, reg1, pos1),
        (set_container_overlay, reg1),

        # set base position and size for lines
        (assign, ":line_size", 0),
        (assign, ":y_pos", 0),

		# set base color for line
		#(assign, ":line_color", 0x000000),

        # Line faction loop begins here - fetching corresponding informations and printing the line title
        (try_for_range_backwards, ":faction_line", kingdoms_begin, kingdoms_end),
            (faction_slot_eq, ":faction_line", slot_faction_state, sfs_active), # continue if active

            # Base position for subheaders
            (assign, ":x_posfhl", 220),

            # Loop other factions (columns)
            (try_for_range, ":faction_column", kingdoms_begin, kingdoms_end),
                (faction_slot_eq, ":faction_column", slot_faction_state, sfs_active), # continue if active

                (try_begin), # not same faction
					(neq, ":faction_column", ":faction_line"),

					(str_store_faction_name, s8, ":faction_column"),

					# sub-faction excluding current faction line
					(try_begin),
						# different from faction line, display status and relation with faction line
						(neq, ":faction_column", ":faction_line"),
						(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction_line", ":faction_column"),
						(assign, ":global_diplomatic_status", reg0),
						(assign, ":extended_diplomatic_status", reg1),

						(try_begin), # War
							(eq, ":global_diplomatic_status", -2),
							(str_store_string, s60, "@War"),
							(assign, reg60, 4980736), # Dark Red # 0xDD0000),
							(assign, reg59, 0),
						(else_try), # Border incident
							(eq, ":global_diplomatic_status", -1),
							(str_store_string, s60, "@Casus Belli"),
							(assign, reg60, 4980736), # Dark Red 0xDD8000),
							(assign, reg59, ":extended_diplomatic_status"),
						(else_try), # Peace
							(eq, ":global_diplomatic_status", 0),
							(str_store_string, s60, "@Peace"),
							(assign, reg60, 14336), # 0xFFFFFF), # Dark Green
							(assign, reg59, 0),
						(else_try), # Truce (non aggression)
							(eq, ":global_diplomatic_status", 1),
							(str_store_string, s60, "@Truce"),
							(assign, reg60, gpu_gray), # 0xDDDDDD),
							(assign, reg59, ":extended_diplomatic_status"),

							# for Diplomacy, comment if not using
							(try_begin),
								(ge, ":extended_diplomatic_status", 61),
								(str_store_string, s60, "@Alliance"),
								(assign, reg60, 0x00FF00),
								(store_sub, reg59, ":extended_diplomatic_status", 60),
							(else_try),
								(ge, ":extended_diplomatic_status", 41),
								(str_store_string, s60, "@Defense"),
								(assign, reg60, 0x00FFAA),
								(store_sub, reg59, ":extended_diplomatic_status", 40),
							(else_try),
								(ge, ":extended_diplomatic_status", 21),
								(str_store_string, s60, "@Trade"),
								(assign, reg60, gpu_gray), # 0x00FFCC),
								(store_sub, reg59, ":extended_diplomatic_status", 20),
							(try_end),
						(try_end),

						(val_add, ":x_poshl", 50),
  
						## OBJ - Diplomatic Status
						(str_store_string, s21, s60),
						(store_sub, ":line_x", ":x_posfhl", -18),
						(store_add, ":line_y", ":y_pos", 57),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":line_x", ":line_y", 0, gpu_center),
						(overlay_set_color, reg1, reg60),
						(call_script, "script_gpu_resize_object", 0, 75),
						# Doubled for bold effect.
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":line_x", ":line_y", 0, gpu_center),
						(overlay_set_color, reg1, reg60),
						(call_script, "script_gpu_resize_object", 0, 75),
						
						## OBJ - Days Remaining.
						(str_store_string, s21, "@{reg59?{reg59} days:}"),
						(store_sub, ":line_x", ":x_posfhl", -18),
						(store_add, ":line_y", ":y_pos", 38),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":line_x", ":line_y", 0, gpu_center),
						(call_script, "script_gpu_resize_object", 0, 75),
						
						## OBJ - Faction relation
						(store_relation, ":kingdom_relation", ":faction_line", ":faction_column"),
						(assign, reg61, ":kingdom_relation"),
						(str_store_string, s21, "@{reg61}"),
						(store_sub, ":line_x", ":x_posfhl", -18),
						(store_add, ":line_y", ":y_pos", 19),
						(call_script, "script_gpu_create_text_label", "str_hub_s21", ":line_x", ":line_y", 0, gpu_center),
						(call_script, "script_gpu_resize_object", 0, 75),
						
					(try_end), # end select alternate display
				(try_end),

                # increase column x position
                (val_add, ":x_posfhl", 90), # valid values 220, 385, 550, 715
            (try_end), # end of column faction loop

            # Faction line information, this is a 4 line block
            # reset x postion for next beginning column and decrease y position according to line count
            (assign, ":x_poshl", 165),

            (val_add, ":y_pos", 54), # linebreak

            # create a separator for faction line
            (create_mesh_overlay, reg1, "mesh_white_plane"),
            (overlay_set_color, reg1, gpu_gray), # 0x000000),
            (position_set_x, pos1, 42000),
            (position_set_y, pos1, 60),
            (overlay_set_size, reg1, pos1),
            (position_set_x, pos1, 17),
            (store_add, ":line_y", ":y_pos", 20), # set it 20 pix above current line
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg1, pos1),

            ## OBJ - FACTION NAME - ROW
            (str_store_faction_name, s21, ":faction_line"),
			(store_add, ":y_temp", ":y_pos", 11),
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 15, ":y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 80),
			# Doubled for bold effect.
			(call_script, "script_gpu_create_text_label", "str_hub_s21", 15, ":y_temp", 0, gpu_left),
			(call_script, "script_gpu_resize_object", 0, 80),
			
            # set position for columns
            (assign, ":x_poshl", 165),
            (assign, ":line_size", 0),
            (position_set_x, ":line_size", 700),
            (position_set_y, ":line_size", 800),

            ## Player relation (first column)
            (store_relation, reg1, "fac_player_supporters_faction", ":faction_line"),

            # no clean strings existing, doing it the same way it's done in game_menu
            (try_begin),
                (ge, reg1, 90),
                (str_store_string, s3, "@Loyal"),
            (else_try),
                (ge, reg1, 80),
                (str_store_string, s3, "@Devoted"),
            (else_try),
                (ge, reg1, 70),
                (str_store_string, s3, "@Fond"),
            (else_try),
                (ge, reg1, 60),
                (str_store_string, s3, "@Gracious"),
            (else_try),
                (ge, reg1, 50),
                (str_store_string, s3, "@Friendly"),
            (else_try),
                (ge, reg1, 40),
                (str_store_string, s3, "@Supportive"),
            (else_try),
                (ge, reg1, 30),
                (str_store_string, s3, "@Favorable"),
            (else_try),
                (ge, reg1, 20),
                (str_store_string, s3, "@Cooperative"),
            (else_try),
                (ge, reg1, 10),
                (str_store_string, s3, "@Accepting"),
            (else_try),
                (ge, reg1, 0),
                (str_store_string, s3, "@Indifferent"),
            (else_try),
                (ge, reg1, -10),
                (str_store_string, s3, "@Suspicious"),
            (else_try),
                (ge, reg1, -20),
                (str_store_string, s3, "@Grumbling"),
            (else_try),
                (ge, reg1, -30),
                (str_store_string, s3, "@Hostile"),
            (else_try),
                (ge, reg1, -40),
                (str_store_string, s3, "@Resentful"),
            (else_try),
                (ge, reg1, -50),
                (str_store_string, s3, "@Angry"),
            (else_try),
                (ge, reg1, -60),
                (str_store_string, s3, "@Hateful"),
            (else_try),
                (ge, reg1, -70),
                (str_store_string, s3, "@Revengeful"),
            (else_try),
                (str_store_string, s3, "@Vengeful"),
            (try_end),

            # Set relation to player numerical value (same line)
            (create_text_overlay, reg10, "@{reg1}", tf_right_align),
            (overlay_set_size, reg10, ":line_size"),
            (store_add, ":line_x", ":x_poshl", 20),
            (position_set_x, pos1, ":line_x"),
            (position_set_y, pos1, ":y_pos"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, gpu_gray), # ":line_color"),

            # Set relation to player string value (second line)
            (create_text_overlay, reg10, "@{s3}", tf_right_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, ":line_x"),
            (store_sub, ":line_y", ":y_pos", 20),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, gpu_gray), # ":line_color"),

            # Set Faction Coat of Arm for standard faction (left of relation string)
            (try_begin),
                (neq, ":faction_line", "fac_player_supporters_faction"),
                (store_sub, ":mesh_index", ":faction_line", kingdoms_begin),
                (val_add, ":mesh_index", "mesh_pic_recruits"),
                (create_mesh_overlay, reg10, ":mesh_index"),
                (position_set_x, pos1, 75),
                (position_set_y, pos1, 75),
                (overlay_set_size, reg10, pos1),
                (position_set_x, pos1, 165),
                (store_sub, ":line_y", ":y_pos", 37),
                (position_set_y, pos1, ":line_y"),
                (overlay_set_position, reg10, pos1),
            (try_end),

            # for current line_faction count lords and centers
            (assign, ":num_lords", 0),
            (assign, ":num_caravans", 0),
            (assign, ":num_centers", 0),
            (assign, ":unassigned_centers", 0),
            (try_for_parties, ":cur_party"),
                (store_faction_of_party, ":cur_faction", ":cur_party"),
                (eq, ":cur_faction", ":faction_line"),

                (try_begin),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_hero_party),
                    (val_add, ":num_lords", 1),
                (else_try),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_caravan),
                    (val_add, ":num_caravans", 1),
                (else_try),
                    (this_or_next|party_slot_eq, ":cur_party", slot_party_type, spt_town),
                    (this_or_next|party_slot_eq, ":cur_party", slot_party_type, spt_castle),
                    (party_slot_eq, ":cur_party", slot_party_type, spt_village),
                    (val_add, ":num_centers", 1),

                    (try_begin),
                        (party_slot_eq, ":cur_party", slot_town_lord, stl_unassigned),
                        (val_add, ":unassigned_centers", 1),
                    (try_end),
                (try_end),
            (try_end), # end of parties loop

            # Count prisoners
            (assign, ":prisoners", 0),
            (try_for_range, ":lord_id", active_npcs_begin, active_npcs_end),
                (troop_slot_eq, ":lord_id", slot_troop_occupation, slto_kingdom_hero),
                (troop_slot_ge, ":lord_id", slot_troop_prisoner_of_party, 0),
                (store_troop_faction, ":lord_faction", ":lord_id"),
                (eq, ":lord_faction", ":faction_line"),
                (val_add, ":prisoners", 1),
            (try_end),

            # add count to last line for faction line report (second, third and fourth line)
            (assign, reg61, ":num_centers"),
            (assign, reg58, ":unassigned_centers"),
            (create_text_overlay, reg10, "@{reg61} {reg58?({reg58} U) :}Centers", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (store_sub, ":line_y", ":y_pos", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, gpu_gray), # 0x000000),

            (assign, reg62, ":num_caravans"),
            (create_text_overlay, reg10, "@{reg62} Caravans", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (val_sub, ":line_y", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, gpu_gray), # 0x000000),

            (assign, reg60, ":num_lords"),
            (assign, reg59, ":prisoners"),
            (create_text_overlay, reg10, "@{reg60} {reg59?({reg59} P) :}Lords", tf_left_align),
            (overlay_set_size, reg10, ":line_size"),
            (position_set_x, pos1, 15),
            (val_sub, ":line_y", 17),
            (position_set_y, pos1, ":line_y"),
            (overlay_set_position, reg10, pos1),
            (overlay_set_color, reg10, gpu_gray), # 0x000000),

            # increase line for next faction block
            (val_add, ":y_pos", 18),#linebreak

        (try_end), # end of faction loop
        (set_container_overlay, -1),
   ]),
   ## END on load trigger

   ## Check for buttonpress
   (ti_on_presentation_event_state_change,
    [
        (store_trigger_param_1, ":button_pressed_id"),
        (try_begin),
             (eq, ":button_pressed_id", "$g_jrider_faction_report_Return_to_menu"), # pressed  (Return to menu)
        (presentation_set_duration, 0),
    (try_end),
    ]),
   ## END presentation event state change trigger

   ## Event to process when running the presentation
   (ti_on_presentation_run,
    [
        (try_begin),
      (this_or_next|key_clicked, key_escape),
      (key_clicked, key_right_mouse_button),
      (presentation_set_duration, 0),
      (jump_to_menu, "mnu_reports"),
        (try_end),

        ]),
   ]),
  # END presentation run trigger
  # END Faction relation presentation
  # Jrider -

  # Jrider +
  ##############################################################################
  # REPORT PRESENTATIONS v1.2 
  ## Character relations report
  ("jrider_character_relation_report", 0,
   mesh_message_window,
   [
     ## Load Presentation
     (ti_on_presentation_load,
      # generic_ti_on_load +
      [
    (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

        (str_clear, s0),
        (str_clear, s1),

        # Character presentation type variations
        (try_begin),
            ###############################
            ## Courtship Relations presentation
            (eq, "$g_character_presentation_type", 0),

            # Set presentation title string
            (str_store_string, s0, "@_Courtships in progress_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 160),
            (assign, ":base_scroll_size_y", 480),
            (assign, ":base_candidates_y", 0), # scrollable area size minus (one line size + 2) 430

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 1000),

            # presentation specific extra overlays
            (call_script, "script_generate_knonwn_poems_string"),

            # Extra text area for knowns poems (filling once so we use a register), filled from s1 generated in script call
            (create_text_overlay, reg1, s1, tf_left_align),
            (position_set_x, pos1, 590), # position
            (position_set_y, pos1, 55),
            (overlay_set_position, reg1, pos1),
            (position_set_x, pos1, 750), # size
            (position_set_y, pos1, 850),
            (overlay_set_size, reg1, pos1),
            (overlay_set_color, reg1, 0xFF66CC), # color
        (else_try),
            ###############################
            ## Lord Relations presentation
            (eq, "$g_character_presentation_type", 1),

            # Set presentation title string
            (str_store_string, s0, "@_Known Lords by Relation_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 110),
            (assign, ":base_scroll_size_y", 550), 
            (assign, ":base_candidates_y", 0), # scrollable area size minus 530

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 2000),
        (else_try),
            ###############################
            ## Player and Companions presentation
            (eq, "$g_character_presentation_type", 2),

            # Set presentation title string
            (str_store_string, s0, "@_Character & Companions_"),

            # Set size of listbox
            (assign, ":base_scroll_y", 110),
            (assign, ":base_scroll_size_y", 550),
            (assign, ":base_candidates_y", 0), # scrollable area size minus (one line size + 2) 530

            # Set storage index
            (assign, "$g_base_character_presentation_storage_index", 3000),

            # Extra area for equipment display
            (assign, ":inv_bar_size", 0),
            (position_set_x, ":inv_bar_size", 400),
            (position_set_y, ":inv_bar_size", 400),

            (create_mesh_overlay, reg1, "mesh_mp_inventory_left"),
            (position_set_x, pos1, 67),
            (position_set_y, pos1, 300),
            (overlay_set_position, reg1, pos1),
            (overlay_set_size, reg1, ":inv_bar_size"),

            (create_mesh_overlay, reg1, "mesh_mp_inventory_right"),
            (position_set_x, pos1, 450),
            (position_set_y, pos1, 330),
            (overlay_set_position, reg1, pos1),
            (overlay_set_size, reg1, ":inv_bar_size"),
        (try_end),
        # END of presentation type specific init and static overlay

        ###############################
        # Create common overlays
        # set foreground mesh overlay (has some transparency in it, so can't use it directly)
        (create_mesh_overlay, reg1, "mesh_face_gen_window"),
        (position_set_x, pos1, 0),
        (position_set_y, pos1, 0),
        (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1000),
        (position_set_y, pos1, 1000),
    (overlay_set_size, reg1, pos1),

    # Presentation title overlay, centered at the top of right pane (from s0, presentation type specific)
        (create_text_overlay, reg1, s0, tf_center_justify),
        (overlay_set_color, reg1, 0xDDDDDD),
    (position_set_x, pos1, 740), # Higher, means more toward the right
        (position_set_y, pos1, 680), # Higher, means more toward the top
        (overlay_set_position, reg1, pos1),
    (position_set_x, pos1, 1200),
        (position_set_y, pos1, 1200),
    (overlay_set_size, reg1, pos1),

    # Done button
        (create_game_button_overlay, "$g_jrider_character_report_Return_to_menu", "@_Done_"),
    (position_set_x, pos1, 290),
        (position_set_y, pos1, 10),
        (overlay_set_position, "$g_jrider_character_report_Return_to_menu", pos1),

        # Character Information text to fill when an entry is clicked in the list
        (create_text_overlay, "$g_jrider_character_information_text", "str_space", tf_left_align),
        (overlay_set_color, "$g_jrider_character_information_text", 0xFFFFFF),
        (position_set_x, pos1, 55), # Higher, means more toward the right
        (position_set_y, pos1, 60), # Higher, means more toward the top
        (overlay_set_position, "$g_jrider_character_information_text", pos1),
        (position_set_x, pos1, 700), # smaller means smaller font
        (position_set_y, pos1, 800),
        (overlay_set_size, "$g_jrider_character_information_text", pos1),

        # Character selection listbox overlay
        # use scrollable text area with global reference so objects can be put inside using overlay_set_container
        (create_text_overlay, "$g_jrider_character_relation_listbox", "str_empty_string", tf_scrollable_style_2),
        (position_set_x, pos1, 590),
        (position_set_y, pos1, ":base_scroll_y"),
        (overlay_set_position, "$g_jrider_character_relation_listbox", pos1),
        (position_set_x, pos1, 335),
        (position_set_y, pos1, ":base_scroll_size_y"),
        (overlay_set_area_size, "$g_jrider_character_relation_listbox", pos1),

        # Faction filter
        (create_combo_button_overlay, "$g_jrider_character_faction_filter", "str_empty_string",0),
        (position_set_x, pos1, 507),
        (position_set_y, pos1, 709),
        (overlay_set_position, "$g_jrider_character_faction_filter", pos1),
        (position_set_x, pos1, 550),
        (position_set_y, pos1, 650),
        (overlay_set_size, "$g_jrider_character_faction_filter", pos1),

        # add elements to filter button
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Your supporters"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Swadians"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Vaegirs"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Khergits"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Nords"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Rhodoks"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@Sarranids"),
        (overlay_add_item, "$g_jrider_character_faction_filter", "@All Factions"),

        # Set initial value for selection box
        (try_begin),
            (this_or_next|eq, "$g_jrider_pres_called_from_menu", 1),
            (eq, "$g_jrider_faction_filter", -1),

            (assign, "$g_jrider_faction_filter", -1),
            (overlay_set_val, "$g_jrider_character_faction_filter", 7),
        (else_try),
            (overlay_set_val, "$g_jrider_character_faction_filter", "$g_jrider_faction_filter"),
        (try_end),

        ###############################
        # Populate lists
        # Init presentation common global variables
        (assign, "$num_charinfo_candidates", 0),

        # Fill listbox (overlay_add_item and extra storage)
        (call_script, "script_fill_relation_canditate_list_for_presentation", "$g_character_presentation_type", ":base_candidates_y"),
        (assign, "$g_jrider_reset_selected_on_faction", 0),
        # stop if there's no candidate
        (gt, "$num_charinfo_candidates", 0),

        # get extra information from storage
        (store_add, ":current_storage_index", "$g_base_character_presentation_storage_index", "$g_latest_character_relation_entry"),
        (troop_get_slot, "$character_info_id", "trp_temp_array_c", ":current_storage_index"),

        # Fill text information for current entry and update text information overlay
        (call_script, "script_generate_extended_troop_relation_information_string", "$character_info_id"),
        (overlay_set_text, "$g_jrider_character_information_text", s1),

        # color selected entry
        (overlay_set_color, "$g_jrider_last_checked_indicator", 0xFF6666FF),
        (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0x44),

        # Begin common dynamic overlay
        # mesh Overlay for character portrait (global not needed)
        (create_image_button_overlay_with_tableau_material, "$g_jrider_character_portrait", -1, "tableau_troop_note_mesh", "$character_info_id"),
        (position_set_x, pos2, 100),
        (position_set_y, pos2, 280),
        (overlay_set_position, "$g_jrider_character_portrait", pos2),
        (position_set_x, pos2, 1100), #1150
        (position_set_y, pos2, 1100), #1150
        (overlay_set_size, "$g_jrider_character_portrait", pos2),

        # mesh Overlay for faction coat of arms
        (try_begin),
            (store_troop_faction, ":troop_faction", "$character_info_id"),
            (neq, ":troop_faction", "fac_player_supporters_faction"),
            (is_between, ":troop_faction", kingdoms_begin, kingdoms_end),
            (store_sub, ":faction_mesh_index", ":troop_faction", kingdoms_begin),
            (val_add, ":faction_mesh_index", "mesh_pic_recruits"),

            (create_mesh_overlay, "$g_jrider_faction_coat_of_arms", ":faction_mesh_index"),
            (position_set_x, pos3, 150),
            (position_set_y, pos3, 600),
            (overlay_set_position, "$g_jrider_faction_coat_of_arms", pos3),
            (position_set_x, pos3, 250),
            (position_set_y, pos3, 250),
            (overlay_set_size, "$g_jrider_faction_coat_of_arms", pos3),
        (try_end),

        # Begin presentation type specific dynamic overlay
        # equipement meshes for character/companions
        (try_begin),
            (eq, "$g_character_presentation_type", 2),

            (assign, ":base_inv_slot_x", 452),
            (assign, ":base_inv_slot_y", 536),

            (try_for_range, ":item_eq", 0, 9),
            # loop equipment slots
                (troop_get_inventory_slot, reg1, "$character_info_id", ":item_eq"),
        
                (try_begin),
                    (eq, ":item_eq", 4),
                    (assign, ":base_inv_slot_x", 68),
                    (assign, ":base_inv_slot_y", 557),
                (try_end),
                (try_begin),
                    (lt, reg1, 1),
                    # empty... assign default mesh
                   (try_begin),
                       (lt, ":item_eq", 4),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_equip"),
                   (else_try),
                       (eq, ":item_eq", 4),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_helmet"),
                   (else_try),
                       (eq, ":item_eq", 5),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_armor"),
                   (else_try),
                       (eq, ":item_eq", 6),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_boot"),
                   (else_try),
                       (eq, ":item_eq", 7),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_glove"),
                   (else_try),
                       (eq, ":item_eq", 8),
                       (assign, ":mesh_id", "mesh_mp_inventory_slot_horse"),
                   (try_end),
        
                   (create_mesh_overlay, reg11, ":mesh_id"),
                   (overlay_set_size, reg11, ":inv_bar_size"),

                   (position_set_x, pos1, ":base_inv_slot_x"),
                   (position_set_y, pos1, ":base_inv_slot_y"),
                   (overlay_set_position, reg11, pos1),
        
                   (troop_set_slot, "trp_temp_array_a", ":item_eq", -1),
                   (store_add, ":item_eq_id", ":item_eq", 10),
                   (troop_set_slot, "trp_temp_array_a", ":item_eq_id", -1),
                # end missing item
                (else_try),
                    (create_mesh_overlay_with_item_id, reg10, reg1),
                    (position_set_x, pos1, 450),
                    (position_set_y, pos1, 450),
                    (overlay_set_size, reg10, pos1),

                    (store_add, ":item_inv_slot_x", ":base_inv_slot_x", 25),
                    (store_add, ":item_inv_slot_y", ":base_inv_slot_y", 25),

                    (position_set_x, pos1, ":item_inv_slot_x"),
                    (position_set_y, pos1, ":item_inv_slot_y"),
                    (overlay_set_position, reg10, pos1),

                    # save id for reuse
                    (troop_set_slot, "trp_temp_array_a", ":item_eq", reg10),
                    (store_add, ":item_eq_id", ":item_eq", 10),
                    (troop_set_slot, "trp_temp_array_a", ":item_eq_id", reg1),
                # real items
                (try_end),
                (val_sub, ":base_inv_slot_y", 51),
            (try_end),
            # end loop equipments slots
        (try_end),

        # do an update if called from menu and reset init variable
        (try_begin),
            (eq, "$g_jrider_pres_called_from_menu", 1),
            (assign, "$g_jrider_pres_called_from_menu", 0),
        (try_end),
    ]),
    # end presentation load

    ## Mouse-over
    (ti_on_presentation_mouse_enter_leave,
      [
      (store_trigger_param_1, ":object"),
      (store_trigger_param_2, ":enter_leave"),

      (try_begin),
          (eq, "$g_character_presentation_type", 2),
          (try_begin),
              (eq, ":enter_leave", 0),
              (try_for_range, ":slot_no", 0, 9),
                  (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
                  (store_add, ":slot_no_eq", ":slot_no", 10),
                  (troop_get_slot, ":item_no", "trp_temp_array_a", ":slot_no_eq"),

                  (set_fixed_point_multiplier, 1000),

                  (position_set_x,pos0,740),
                  (position_set_y,pos0,235),
                  (show_item_details, ":item_no", pos0, 100),
              (try_end),
          (else_try),
              (try_for_range, ":slot_no", 0, 9),
                (troop_slot_eq, "trp_temp_array_a", ":slot_no", ":object"),
                (close_item_details),
              (try_end),
          (try_end),
      (try_end),
    ]),
    # end mouseover

    ## Check for buttonpress
    (ti_on_presentation_event_state_change,
     [
        (store_trigger_param_1, ":object"), # object
        (store_trigger_param_2, ":value"),  # value

        (try_begin),
            # pressed  (Return to menu)
            (eq, ":object", "$g_jrider_character_report_Return_to_menu"),

            (try_begin),
                (neq, "$num_charinfo_candidates", 0),
                (overlay_set_text, "$g_jrider_character_information_text", "str_empty_string"),
                (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0),
            (try_end),
            (presentation_set_duration, 0),

        (else_try),
            # Faction filter
            (eq, ":object", "$g_jrider_character_faction_filter"),
            (try_begin),
                (eq, ":value", 7),
                (assign, "$g_jrider_faction_filter", -1),
            (else_try),
                (assign, "$g_jrider_faction_filter", ":value"),
            (try_end),

            # reset selected to first
            (assign, "$g_jrider_reset_selected_on_faction", 1000),

            # restart presentation to take filters into account
            (start_presentation, "prsnt_jrider_character_relation_report"),

        (else_try),
            (neq, ":object", "$g_jrider_character_information_text"),
            (neq, ":object", "$g_jrider_character_portrait"),
            (neq, ":object", "$g_jrider_character_relation_listbox"),
            #(neq, ":object", "$g_jrider_faction_coat_of_arms"),
            # clicked on list entry
            # get storage index + base storage index
            (store_add, ":storage_button_id", ":object", "$g_base_character_presentation_storage_index"),
            (troop_get_slot, ":character_number", "trp_temp_array_b", ":storage_button_id"),

            (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0),
            (overlay_set_color, "$g_jrider_last_checked_indicator", 0xDDDDDD),

            # update last entry and check variables
            (assign, "$g_latest_character_relation_entry", ":character_number"),
            (assign, "$g_jrider_last_checked_indicator", ":object"),

            # color selected entry
            (overlay_set_color, "$g_jrider_last_checked_indicator", 0xFF6666FF),
            (overlay_set_alpha, "$g_jrider_last_checked_indicator", 0x44),

            # get troop information from storage to update text
            (val_add, ":character_number", "$g_base_character_presentation_storage_index"),
            (troop_get_slot, "$character_info_id", "trp_temp_array_c", ":character_number"),

            # restart presentation to update picture and text
            (start_presentation, "prsnt_jrider_character_relation_report"),
    (try_end),
     ] # + generic_ti_on_presentation_event_state_change
     ),
     # end event state change

    ## Event to process when running the presentation
    (ti_on_presentation_run,
     # generic_ti_on_presentation_run +
     [
        (try_begin),
      (this_or_next|key_clicked, key_escape),
      (key_clicked, key_right_mouse_button),
      (presentation_set_duration, 0),
      (jump_to_menu, "mnu_reports"),
        (try_end),

        ]),
     # end presentation run
     ]),
    ###################################
    # Character relation presentation end
# Jrider -

  
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