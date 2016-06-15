## Prebattle Orders & Deployment by Caba'drin
## v0.96.2
## 25 March 2012

from header_operations import *
from header_triggers import *
#from module_constants import *

FireArrow_triggers = [
 (ti_on_init_missile, [
    (set_position_delta, 0, 100, 0), #change this to move the particle system's local position
    (particle_system_add_new, "psys_arrow_fire"),
    (particle_system_add_new, "psys_arrow_smoke"),
    (particle_system_add_new, "psys_arrow_fire_sparks"),
    (set_current_color,150, 130, 70),
    (add_point_light, 10, 30),
  ]),

  (ti_on_missile_hit, [
	(set_position_delta, 0, 100, -300), 
    (particle_system_burst,"psys_arrow_fire", 1, 20),
	(particle_system_burst,"psys_arrow_smoke", 1, 30),
	(particle_system_burst,"psys_arrow_fire_sparks", 1, 15),
	(set_current_color,150, 130, 70),
   ]),
]

from header_items import *
from util_wrappers import *
from copy import deepcopy
def modmerge(var_set):
	try:
		var_name_1 = "items"
		orig_items = var_set[var_name_1]
		
		# arrows_begin = 0
		add_item = deepcopy(orig_items)
		for i in range(1,len(orig_items)):
			itm_flags = add_item[i][3]
			type = itm_flags & 0x000000ff
			#type = orig_items[i][3] & 0x000000ff
			if type == itp_type_arrows and "tutorial" not in orig_items[i][0] and "practice" not in orig_items[i][0]: 
				mesh_list = ItemWrapper(add_item[i]).GetMeshList()
				for n in range(0, len(mesh_list)):
					if mesh_list[n][1] == ixmesh_flying_ammo: mesh_list[n] = ("fire_arrow_flying_missile", ixmesh_flying_ammo)
				# if arrows_begin == 0:
					# arrows_begin = i
				# arrows_end = i
				add_item[i][0] = add_item[i][0]+'_fire'
				add_item[i][3] = itm_flags & ~itp_merchandise & ~itp_default_ammo | itp_no_pick_up_from_ground		#disallow from merch list/default status, make not pickup-able
				dmg = get_thrust_damage(add_item[i][6]) % 256
				add_item[i][6] = add_item[i][6] & ~(ibf_damage_mask << iwf_thrust_damage_bits) #erase damage
				dmg += 8                                                                      #increase damage by 8 (5, 3 are taken away by 'bent' bow)
				add_item[i][6] = add_item[i][6] | thrust_damage(dmg, pierce)                   #write increase damage
				ItemWrapper(add_item[i]).GetTriggers().extend(FireArrow_triggers)
				#orig_items.insert((len(orig_items)-1), add_item[i])   ##do I really want them before 'end items' ?
				orig_items.append(add_item[i]) 
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)
	#return arrows_begin, arrows_end