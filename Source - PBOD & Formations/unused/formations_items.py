# Formations AI by Motomataru
# rel. 08/31/2012

from header_items import *
from copy import deepcopy

def modmerge(var_set):
	try:
		from modmerger_options import module_sys_info
		version = module_sys_info["version"]
	except:
		version = 1153 # version not specified.  assume latest warband or wfas at this time

	try:
		var_name_1 = "items"
		orig_items = var_set[var_name_1]
		
		add_item = deepcopy(orig_items)
		for i_item in range(1,len(orig_items)):
			type = add_item[i_item][3] & 0x000000ff
			# if itp_type_one_handed_wpn <= type <= itp_type_polearm and add_item[i_item-1][3] & itp_next_item_as_melee == 0 and (get_thrust_damage(add_item[i_item][6]) % 256) > 0 and "tutorial" not in add_item[i_item][0] and "arena" not in add_item[i_item][0] and "practice" not in add_item[i_item][0] and "tpe" not in add_item[i_item][0]:
			if itp_type_one_handed_wpn <= type <= itp_type_polearm and (get_thrust_damage(add_item[i_item][6])&0xff) > 0 and "tutorial" not in add_item[i_item][0] and "arena" not in add_item[i_item][0] and "practice" not in add_item[i_item][0] and "tpe" not in add_item[i_item][0]:
				#Above checks that it is a weapon with thrust damage; also checks that it isn't a tournament-type weapon by checking the item ID (just to prevent not-used items)
				add_item[i_item][0] = 'noswing_'+add_item[i_item][0]                  #add noswing_ to the item's name
				add_item[i_item][6] = add_item[i_item][6] & ~(ibf_damage_mask << iwf_swing_damage_bits) #should set new item's swing damage to 0
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_overswing_polearm  #remove itcf_ capabilties to prevent swinging without damage  
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_slashright_polearm                     
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_slashleft_polearm
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_overswing_onehanded   
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_slashright_onehanded                     
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_slashleft_onehanded
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_overswing_twohanded
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_slashright_twohanded                     
				add_item[i_item][4] = add_item[i_item][4] & ~itcf_slashleft_twohanded
				if type == itp_type_polearm and add_item[i_item][3] & itp_two_handed == 0:
					add_item[i_item][4] = add_item[i_item][4] | itcf_thrust_onehanded  #so that the polearms use 'bent elbow' with shields, but normal without
				add_item[i_item][3] = add_item[i_item][3] & ~itp_merchandise
				# orig_items.insert((len(orig_items)-1), add_item[i_item])        #add right above itm_items_end
				orig_items.append(add_item[i_item])
		
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)