## Prebattle Orders & Deployment by Caba'drin
## v0.96
## 13 March 2012

from header_common import *
from header_scene_props import *
from header_operations import *
from header_triggers import *
from header_sounds import *
from module_constants import *
import string


pavise_init = (ti_on_init_scene_prop, 
   [
    (store_trigger_param_1, ":instance_no"),
	(assign, ":agent_no", reg5), #reg5 is caller agent, set before (spawn_scene_prop) in "cf_agent_deploy_pavise"
	(try_begin),
		(agent_is_active, ":agent_no"),
        (call_script, "script_agent_setup_pavise_prop", ":agent_no", ":instance_no"),
		(agent_get_troop_id, ":troop_no", ":agent_no"),
		(call_script, "script_agent_troop_get_banner_mesh", ":agent_no", ":troop_no"),
		(assign, ":mesh", reg0),
	(else_try),
		(scene_prop_set_hit_points, ":instance_no", 100),
		(scene_prop_set_slot, ":instance_no", slot_prop_pavise_spawn_agent, -1),
		(assign, ":mesh", "mesh_banners_default_b"),
	(try_end),
	(scene_prop_set_slot, ":instance_no", slot_prop_pavise_banner_mesh, ":mesh"),
	(assign, ":tableau", "tableau_pavise_shield_2"),
	(try_begin),			
		(prop_instance_get_scene_prop_kind, reg0, ":instance_no"),
		(eq, reg0, "spr_pavise_1"),
		(assign, ":tableau", "tableau_pavise_shield_1"),
	(try_end),	
	(cur_scene_prop_set_tableau_material, ":tableau", ":mesh"),
   ])

pavise_recover = (ti_on_scene_prop_use, ##JUNK
   [
    (store_trigger_param_1, ":agent_no"),
    (store_trigger_param_2, ":instance_no"),
	(display_message, "@On Use!"),
   
    (call_script, "script_cf_agent_recover_pavise", ":agent_no", ":instance_no"),
   ])
   
pavise_recover2 = ( ti_on_scene_prop_start_use, ##JUNK
    [
    (store_trigger_param_1, ":agent_no"),
    (store_trigger_param_2, ":instance_no"),
	(display_message, "@On Start-Use!"),
   
    (call_script, "script_cf_agent_recover_pavise", ":agent_no", ":instance_no"),
   ])
   
pavise_destroy = (ti_on_scene_prop_destroy, 
   [
    (store_trigger_param_1, ":instance_no"),      
    (store_trigger_param_2, ":attacker_agent_no"),

    (set_fixed_point_multiplier, 100),
    (prop_instance_get_position, pos1, ":instance_no"),
	(play_sound_at_position, "snd_dummy_destroyed", pos1),

	(assign, ":rotate_side", 86),
    (try_begin),
        (ge, ":attacker_agent_no", 0),
        (agent_get_position, pos2, ":attacker_agent_no"),
        (position_is_behind_position, pos2, pos1),
        (val_mul, ":rotate_side", -1),
    (try_end),
      
    (init_position, pos3),
    (try_begin),
        (ge, ":rotate_side", 0),
        (position_move_y, pos3, -100),
    (else_try),
        (position_move_y, pos3, 100),
    (try_end),
      
	(position_move_x, pos3, -50),
	(position_transform_position_to_parent, pos4, pos1, pos3),
	(position_move_z, pos4, 100),
	(position_get_distance_to_ground_level, ":height_to_terrain", pos4),
	(val_sub, ":height_to_terrain", 100),
	(assign, ":z_difference", ":height_to_terrain"),
	#(assign, reg0, ":z_difference"),
	#(display_message, "@{!}z dif : {reg0}"),
	(val_div, ":z_difference", 3),

	(try_begin),
		(ge, ":rotate_side", 0),
		(val_add, ":rotate_side", ":z_difference"),
	(else_try),
		(val_sub, ":rotate_side", ":z_difference"),
	(try_end),

    (position_rotate_x, pos1, ":rotate_side"),
    (prop_instance_animate_to_position, ":instance_no", pos1, 70), #animate to position 1 in 0.7 second
	
	(scene_prop_get_slot, ":spr_agent", ":instance_no", slot_prop_pavise_spawn_agent),
	(scene_prop_set_slot, ":instance_no", slot_prop_pavise_spawn_agent, -1),
	(agent_is_active, ":spr_agent"), 
	(agent_set_slot, ":spr_agent", slot_agent_deployed_pavise, 0),
    ])     
  
pavise_hit = (ti_on_scene_prop_hit, 
   [
    (store_trigger_param_1, ":instance_no"),       
    (store_trigger_param_2, ":damage"),
      
    (try_begin),
        (scene_prop_get_hit_points, ":hit_points", ":instance_no"),
        (val_sub, ":hit_points", ":damage"),
        (gt, ":hit_points", 0),
        (play_sound_at_position, "snd_dummy_hit", pos1),
    (else_try),
        (play_sound_at_position, "snd_dummy_destroyed", pos1),
    (try_end),

    (particle_system_burst, "psys_dummy_smoke", pos1, 3),
    (particle_system_burst, "psys_dummy_straw", pos1, 10),     
   ])

#pavise_triggers = [pavise_init, pavise_recover,pavise_recover2, pavise_hit, pavise_destroy]
pavise_triggers = [pavise_init, pavise_hit, pavise_destroy]
   
scene_props = [ #sokf_show_hit_point_bar|spr_use_time(0)
  ("pavise_1",sokf_moveable|sokf_destructible,"tableau_shield_pavise_prop_1","bo_tableau_shield_pavise_prop_1", pavise_triggers),
  ("pavise_2",sokf_moveable|sokf_destructible,"tableau_shield_pavise_prop_2","bo_tableau_shield_pavise_prop_2", pavise_triggers),
  ("pavise_3",sokf_moveable|sokf_destructible,"tableau_shield_pavise_prop_3","bo_tableau_shield_pavise_prop_3", pavise_triggers),
]

from util_common import add_objects
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "scene_props"
        orig_scene_props = var_set[var_name_1]
        add_objects(orig_scene_props, scene_props)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)