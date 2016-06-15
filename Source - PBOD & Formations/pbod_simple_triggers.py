## Prebattle Orders & Deployment by Caba'drin
## v0.96
## 13 March 2012
from header_troops import *
from header_common import *
from header_operations import *
from module_constants import *

pbod_version_trigger = (0, 
    [    
	 (try_begin),
		(party_slot_eq, "p_main_party", slot_party_pref_wp_prof_decrease, 2),
		(call_script, "script_weather_restore_proficiencies"),
		(party_set_slot, "p_main_party", slot_party_pref_wp_prof_decrease, 1),
	 (try_end),
	 # (try_begin),
		# (game_key_clicked, gk_view_orders),
		# (start_presentation, "prsnt_pbod_preferences"),
	 # (try_end),
	 
     (neg|party_slot_eq, "p_main_party", slot_party_pbod_mod_version, current_version),
	 #(call_script, "script_init_item_score"),
	 (call_script, "script_init_all_keys"),
	 (set_show_use_tooltip, tooltip_destructible_prop, 0),
	 (try_begin),
	    (this_or_next|party_slot_eq, "p_main_party", slot_party_pref_prefs_set, 0),
		(neg|party_slot_ge, "p_main_party", slot_party_pbod_mod_version, 960), #Preference Reset witih new 0.96 prefs
		(call_script, "script_prebattle_set_default_prefs"),
		(party_set_slot, "p_main_party", slot_party_pref_prefs_set, 1),
	 (try_end),	
	 (try_begin), 
		(neg|party_slot_eq, "p_main_party", slot_party_pbod_mod_version, 0), #PBOD previously installed
		(store_div, reg0, current_version, 10), #version number
		(store_mod, reg1, current_version, 10), #revision
		(try_begin),
			(eq, reg1, 0),
			(str_store_string, s1, "str_reg0"),
		(else_try),
			(str_store_string, s1, "@{reg0}.{reg1}"),
		(try_end),
		(game_key_get_key, reg0, gk_view_orders),
		(call_script, "script_str_store_key_name", s0, reg0),
        (display_message, "@PBOD Updated to version 0.{s1}^Mod Options and Mod Keys Reset. Press {s0} to access these preferences."),
     (try_end),	 
     (party_set_slot, "p_main_party", slot_party_pbod_mod_version, current_version),
    ])

from util_wrappers import *
# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
	try:
		var_name_1 = "simple_triggers"
		orig_simple_triggers = var_set[var_name_1]
		
		for i in range(len(orig_simple_triggers)):
			if( SimpleTriggerWrapper(orig_simple_triggers[i]).GetInterval() == 24 #for Native savegame compatiblity
				and SimpleTriggerWrapper(orig_simple_triggers[i]).GetOpBlock().GetLength() == 0 #find first 'blank' trigger
			   ): 
				orig_simple_triggers[i] = pbod_version_trigger #replace it
				break
		else: # no blank trigger found to replace (not Native/a Native compatible mod)
			orig_simple_triggers.extend([pbod_version_trigger,]) #tack onto end

	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)
