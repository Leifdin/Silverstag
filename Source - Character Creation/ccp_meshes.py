# Character Creation Presentation (1.0.2)
# Created by Windyplains.  Inspired by Dunde's character creation presentation in Custom Commander.



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
####################################################################################################################################
# CCP 1.0
####################################################################################################################################
	("character_creator", 0, "character_creation", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
	("golden_coins", 0, "mp_ico_gold", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
	("weapon_bow", 0, "ico_bow", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
	("weapon_crossbow", 0, "ico_crossbow", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
	("weapon_onehand", 0, "ico_swordone", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
	("weapon_twohand", 0, "ico_swordtwo", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
	("weapon_thorwing", 0, "ico_knifethrow", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
	("weapon_polearm", 0, "ico_spear", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5),
	#("status_renown", 0, "he_nor_t1_crown", 0, 0, 0, 0, 0, 0, 1.0, 0.76, 0.5), # status_shield_100
	
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