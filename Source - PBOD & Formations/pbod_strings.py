## Prebattle Orders & Deployment by Caba'drin
## v0.96.3
## 29 March 2012

#-- Dunde's Key Config BEGIN
from module_constants import keys_list, all_keys_list
def get_key_strings():
   key_strings = []
   for i_key in xrange(len(all_keys_list)):
       key_strings.append(("key_"+str(i_key+1), all_keys_list[i_key][1]))    
   for i_key in xrange(len(keys_list)):
       key_strings.append(("key_no"+str(i_key+1), keys_list[i_key][2]))      
   return key_strings[:]  
#-- Dunde's Key Config END

strings = [
##PBOD
("real_deployment_start", "Place your troops before the battle starts by first selecting a division, then holding down '{s48}' and releasing the flag where you want the division. If you want the divison to begin in formation, first give the formation order, then place them with '{s48}'.^^Your Tactics Skill allows you {reg0} placements.^Hit '{s49}' to start the battle before they are all used."),
("real_deployment_end",   "Deployment Complete^^Prepare for battle!"),
("real_deployment_inprogress", "{!}{reg0} placement{reg1?s:} with '{s48}' remaining or hit '{s49}' to start the battle now."),
("order_wpt_ranged", "bows and missiles"),
("order_wpt_onehand", "side arms"),
("order_wpt_twohands", "two-handers"),
("order_wpt_polearm", "poelarms"),
("order_wpt_ready", "ready"),
("order_wpt_shields", "shields"),
("order_wpt_use_shield", "brandish"),
("order_wpt_no_shield", "doff your"),
("order_wpt_free_shield", "free"),
("order_skirmish_end", "stand and fight"),
("order_skirmish_start", "avoid melee"),
("order_volley_end", "end volley"),
("order_volley_start", "prepare to volley"),
("order_volley_rank_start", "fire by rank"),
("order_volley_platoon_start", "volley by platoons"),
("order_brace_end", "remove brace and fight"),
("order_brace_start", "brace for charge"),
("order_pavise_end", "recover shields"),
("order_pavise_start", "deploy pavise for cover"),
("order_crouch_end", "recover and stand"),
("order_crouch_start", "crouch and take cover"),
("order_firearrow_end", "extinguish flames"),
("order_firearrow_start", "ignite arrows"),
("order_num_ranks_add", "add another rank"),
("order_num_ranks_remove", "remove one rank"),
("s1_exclamation_point", "{s1}!"),
("everyone", "Everyone"),

##PBOD
] + get_key_strings()

from util_common import add_objects

# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "strings"
        orig_strings = var_set[var_name_1]
        add_objects(orig_strings, strings)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)

  # FOR REFERENCE, NATIVE 'BLANK' STRINGS
  # ("s0", "{!}{s0}"),
  # ("blank_s1", "{!} {s1}"),
  # ("reg1", "{!}{reg1}"),
  # ("s50_comma_s51", "{!}{s50}, {s51}"),
  # ("s50_and_s51", "{s50} and {s51}"),
  # ("s52_comma_s51", "{!}{s52}, {s51}"),
  # ("s52_and_s51", "{s52} and {s51}"),
  # ("reg0", "{!}{reg0}"),
  # ("s0_reg0", "{!}{s0} {reg0}"),
  # ("s0_s1", "{!}{s0} {s1}"),
  # ("reg0_dd_reg1reg2", "{!}{reg0}:{reg1}{reg2}"),
  # ("s0_dd_reg0", "{!}{s0}: {reg0}"),
  # ("s44_s41", "{!}{s44}, {s41}"),
