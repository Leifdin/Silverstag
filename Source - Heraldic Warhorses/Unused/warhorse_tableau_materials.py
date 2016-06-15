from header_common import *
from ID_animations import *
from header_mission_templates import *
from header_tableau_materials import *
from header_items import *
from module_constants import *

####################################################################################################################
#  Each tableau material contains the following fields:
#  1) Tableau id (string): used for referencing tableaux in other files. The prefix tab_ is automatically added before each tableau-id.
#  2) Tableau flags (int). See header_tableau_materials.py for a list of available flags
#  3) Tableau sample material name (string).
#  4) Tableau width (int).
#  5) Tableau height (int).
#  6) Tableau mesh min x (int): divided by 1000 and used when a mesh is auto-generated using the tableau material
#  7) Tableau mesh min y (int): divided by 1000 and used when a mesh is auto-generated using the tableau material
#  8) Tableau mesh max x (int): divided by 1000 and used when a mesh is auto-generated using the tableau material
#  9) Tableau mesh max y (int): divided by 1000 and used when a mesh is auto-generated using the tableau material
#  10) Operations block (list): A list of operations. See header_operations.py for reference.
#     The operations block is executed when the tableau is activated.
# 
####################################################################################################################

#banner height = 200, width = 85 with wood, 75 without wood

wse_warhorse_tableaus = [
# WSE horses BEGIN
  ("wse_charger", 0, "sample_wse_charger", 512, 512, 0, 0, 0, 0,
   [(store_script_param, ":banner_mesh", 1),

    (set_fixed_point_multiplier, 100),
    (try_begin), 
      (eq, "$debug_heraldic", 1),
      (call_script, "script_agent_troop_get_banner_mesh", -1, "$assigned_troop"),
      (assign, ":banner_mesh", reg0),
      (store_sub, ":background_slot", ":banner_mesh", arms_meshes_begin), #banner_meshes_begin),
      (troop_get_slot, ":background_color", "trp_banner_background_color_array", ":background_slot"),
      (cur_tableau_set_background_color, ":background_color"),
      (init_position, pos1),
      (cur_tableau_add_mesh_with_vertex_color, "mesh_heraldic_armor_bg", pos1, 200, 100, ":background_color"),
      (init_position, pos1),
      (position_set_z, pos1, "$heraldic_param1"),
      (position_set_x, pos1, "$heraldic_param2"),
      (position_set_y, pos1, "$heraldic_param3"),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, "$heraldic_param4", 0),
    (else_try),
      (store_sub, ":background_slot", ":banner_mesh", arms_meshes_begin), #banner_meshes_begin),
      (troop_get_slot, ":background_color", "trp_banner_background_color_array", ":background_slot"),
      (cur_tableau_set_background_color, ":background_color"),
      (init_position, pos1),
      (cur_tableau_add_mesh_with_vertex_color, "mesh_heraldic_armor_bg", pos1, 200, 100, ":background_color"),
      (init_position, pos1),
      (position_set_z, pos1, 50),
      (position_set_x, pos1, -60),
      (position_set_y, pos1, 88),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, 35, 0),  
      (position_set_x, pos1, 42),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, 35, 0),      
    (try_end),        
    (init_position, pos1),
    (position_set_z, pos1, 100),
    (cur_tableau_add_mesh,  "mesh_tableau_mesh_wse_charger", pos1, 0, 0),
    (cur_tableau_set_camera_parameters, 0, 200, 200, 0, 100000), ]),	  

  ("wse_warhorse_chain", 0, "sample_wse_warhorse_chain", 1024, 1024, 0, 0, 0, 0,
   [(store_script_param, ":banner_mesh", 1),

    (set_fixed_point_multiplier, 100),
    (try_begin), 
      (eq, "$debug_heraldic", 1),
      (call_script, "script_agent_troop_get_banner_mesh", -1, "$assigned_troop"),
      (assign, ":banner_mesh", reg0),
      (store_sub, ":background_slot", ":banner_mesh", arms_meshes_begin), #banner_meshes_begin),
      (troop_get_slot, ":background_color", "trp_banner_background_color_array", ":background_slot"),
      (cur_tableau_set_background_color, ":background_color"),
      (init_position, pos1),
      (cur_tableau_add_mesh_with_vertex_color, "mesh_heraldic_armor_bg", pos1, 200, 100, ":background_color"),
      (init_position, pos1),
      (position_set_z, pos1, "$heraldic_param1"),
      (position_set_x, pos1, "$heraldic_param2"),
      (position_set_y, pos1, "$heraldic_param3"),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, "$heraldic_param4", 0),
    (else_try),
      (store_sub, ":background_slot", ":banner_mesh", arms_meshes_begin), #banner_meshes_begin),
      (troop_get_slot, ":background_color", "trp_banner_background_color_array", ":background_slot"),
      (cur_tableau_set_background_color, ":background_color"),
      (init_position, pos1),
      (cur_tableau_add_mesh_with_vertex_color, "mesh_heraldic_armor_bg", pos1, 200, 100, ":background_color"),
      (init_position, pos1),
      (position_set_z, pos1, 50),
      (position_set_x, pos1, -19),
      (position_set_y, pos1, 84),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, 30, 0),       
    (try_end),        
    (init_position, pos1),
    (position_set_z, pos1, 100),
    (cur_tableau_add_mesh,  "mesh_tableau_mesh_wse_warhorse_chain", pos1, 0, 0),
    (cur_tableau_set_camera_parameters, 0, 200, 200, 0, 100000), ]),	  

  ("wse_warhorse_steppe", 0, "sample_wse_warhorse_steppe", 1024, 1024, 0, 0, 0, 0,
   [(store_script_param, ":banner_mesh", 1),

    (set_fixed_point_multiplier, 100),
    (try_begin), 
      (eq, "$debug_heraldic", 1),
      (call_script, "script_agent_troop_get_banner_mesh", -1, "$assigned_troop"),
      (assign, ":banner_mesh", reg0),
      (store_sub, ":background_slot", ":banner_mesh", arms_meshes_begin), #banner_meshes_begin),
      (troop_get_slot, ":background_color", "trp_banner_background_color_array", ":background_slot"),
      (cur_tableau_set_background_color, ":background_color"),
      (init_position, pos1),
      (cur_tableau_add_mesh_with_vertex_color, "mesh_heraldic_armor_bg", pos1, 200, 100, ":background_color"),
      (init_position, pos1),
      (position_set_z, pos1, "$heraldic_param1"),
      (position_set_x, pos1, "$heraldic_param2"),
      (position_set_y, pos1, "$heraldic_param3"),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, "$heraldic_param4", 0),
    (else_try),
      (store_sub, ":background_slot", ":banner_mesh", arms_meshes_begin), #banner_meshes_begin),
      (troop_get_slot, ":background_color", "trp_banner_background_color_array", ":background_slot"),
      (cur_tableau_set_background_color, ":background_color"),
      (init_position, pos1),
      (cur_tableau_add_mesh_with_vertex_color, "mesh_heraldic_armor_bg", pos1, 200, 100, ":background_color"),
      (init_position, pos1),
      (position_set_z, pos1, 50),
      (position_set_x, pos1, -19),
      (position_set_y, pos1, 52),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, 15, 0),       
    (try_end),        
    (init_position, pos1),
    (position_set_z, pos1, 100),
    (cur_tableau_add_mesh,  "mesh_tableau_mesh_wse_warhorse_steppe", pos1, 0, 0),
    (cur_tableau_set_camera_parameters, 0, 200, 200, 0, 100000), ]),	
       
  ("wse_warhorse_sarranid", 0, "sample_wse_warhorse_sarranid", 1024, 1024, 0, 0, 0, 0,
    [(store_script_param, ":banner_mesh", 1),

    (set_fixed_point_multiplier, 100),
    (try_begin), 
      (eq, "$debug_heraldic", 1),
      (call_script, "script_agent_troop_get_banner_mesh", -1, "$assigned_troop"),
      (assign, ":banner_mesh", reg0),
      (store_sub, ":background_slot", ":banner_mesh", arms_meshes_begin), #banner_meshes_begin),
      (troop_get_slot, ":background_color", "trp_banner_background_color_array", ":background_slot"),
      (cur_tableau_set_background_color, ":background_color"),
      (init_position, pos1),
      (cur_tableau_add_mesh_with_vertex_color, "mesh_heraldic_armor_bg", pos1, 200, 100, ":background_color"),
      (init_position, pos1),
      (position_set_z, pos1, "$heraldic_param1"),
      (position_set_x, pos1, "$heraldic_param2"),
      (position_set_y, pos1, "$heraldic_param3"),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, "$heraldic_param4", 0),
    (else_try),
      (store_sub, ":background_slot", ":banner_mesh", arms_meshes_begin), #banner_meshes_begin),
      (troop_get_slot, ":background_color", "trp_banner_background_color_array", ":background_slot"),
      (cur_tableau_set_background_color, ":background_color"),
      (init_position, pos1),
      (cur_tableau_add_mesh_with_vertex_color, "mesh_heraldic_armor_bg", pos1, 200, 100, ":background_color"),
      (init_position, pos1),
      (position_set_z, pos1, 50),
      (position_set_x, pos1, -19),
      (position_set_y, pos1, 84),
      (cur_tableau_add_mesh, ":banner_mesh", pos1, 30, 0),       
    (try_end),        
    (init_position, pos1),
    (position_set_z, pos1, 100),
    (cur_tableau_add_mesh,  "mesh_tableau_mesh_wse_warhorse_sarranid", pos1, 0, 0),
    (cur_tableau_set_camera_parameters, 0, 200, 200, 0, 100000), ]),	      
 #WSE horses END       
]

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "tableau_materials"
        orig_tableau_materials = var_set[var_name_1]
        orig_tableau_materials.extend(wse_warhorse_tableaus)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)