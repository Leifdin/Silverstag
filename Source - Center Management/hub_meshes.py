# Tournament Play Enhancements (1.6) by Windyplains

from header_meshes import *

####################################################################################################################
#  Each mesh record contains the following fields:
#  1) Mesh id: used for referencing meshes in other files. The prefix mesh_ is automatically added before each mesh id.
#  2) Mesh flags. See header_meshes.py for a list of available flags
#  3) Mesh resource name: Resource name of the mesh
#  4) Mesh translation on x axis: Will be done automatically when the mesh is loaded
#  5) Mesh translation on y axis: Will be done automatically when the mesh is loaded
#  6) Mesh translation on z axis: Will be done automatically when the mesh is loaded
#  7) Mesh rotation angle over x axis: Will be done automatically when the mesh is loaded
#  8) Mesh rotation angle over y axis: Will be done automatically when the mesh is loaded
#  9) Mesh rotation angle over z axis: Will be done automatically when the mesh is loaded
#  10) Mesh x scale: Will be done automatically when the mesh is loaded
#  11) Mesh y scale: Will be done automatically when the mesh is loaded
#  12) Mesh z scale: Will be done automatically when the mesh is loaded
####################################################################################################################

meshes = [
  # ("town_button", 0, "button_drop_child", 0, 0, 0, 0, 0, 0, 1.0, 0.5, 0.5),
  # ("town_button_highlight", 0, "button_drop_child_hl", 0, 0, 0, 0, 0, 0, 1.0, 0.5, 0.5),
  # ("town_button_selected", 0, "button_drop_child_clicked", 0, 0, 0, 0, 0, 0, 1.0, 0.5, 0.5),
  # ("data_background", 0, "mp_score_b", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
  # ("log_window", 0, "game_log_window", 0, 0, 0, 0, 0, 0, 1.0, 1.5, 0.5),
  ("marble_background", 0, "marble_background", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
  ("button_up", 0, "button4_up", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("button_down", 0, "button4_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("hub_golden_coins", 0, "mp_ico_gold", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
  
]

from util_common import *

def modmerge_meshes(orig_meshes):
    # add remaining meshes
    from util_common import add_objects
    num_appended, num_replaced, num_ignored = add_objects(orig_meshes, meshes)
    #print num_appended, num_replaced, num_ignored
	
	
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "meshes"
        orig_meshes = var_set[var_name_1]
        modmerge_meshes(orig_meshes)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)