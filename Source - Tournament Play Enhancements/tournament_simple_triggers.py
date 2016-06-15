# Tournament Play Enhancements (1.5) by Windyplains

from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
##diplomacy start+
# from header_terrain_types import *
# from module_factions import dplmc_factions_end
##diplomacy end+
from module_quests import *
from module_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################



simple_triggers = [
	
# QUEST: floris_active_tournament
# Determine if tournaments are active in a town.
#  - Deliver quest if tournament active and quest is not.  
#  - End quest if tournament is not active and quest is.
(12,
	[
		(map_free),
		(neg|is_currently_night),
		(eq, "$tpe_quests_active", 1),
		(assign, ":closest_town_no", -1),
		(assign, ":best_rated_town", -1),
		(try_for_range, ":center_no", towns_begin, towns_end),
			(party_get_slot, ":has_tournament", ":center_no", slot_town_has_tournament), # 0 = no, 1 = last day, 2+ = ongoing.
			(try_begin),
				##### ACQUIRE QUEST: Determine appropriate city #####
				# Make sure there is enough time to travel there.
				(ge, ":has_tournament", 3),
				# Check if the town is hostile to the player.
				(call_script, "script_tpe_store_town_faction_to_reg0", ":center_no"),
				(store_relation, ":relation", reg0, "fac_player_supporters_faction"),
				(assign, ":faction_no", reg0),
				(ge, ":relation", 0),
				(party_get_slot, ":troop_host", ":center_no", slot_town_lord),
				(ge, ":troop_host", 0), # Make sure someone actually controls the town.
				(neq, ":troop_host", "trp_player"), # Make sure the player isn't inviting himself.
				(troop_slot_eq, ":troop_host", slot_troop_prisoner_of_party, -1), # Ensure town lord isn't a prisoner somewhere.
				## TOWN QUALIFIES, NOW RATE IT ##
				(assign, ":rating_current", 0),
				# Improve rating based on it being the player's faction.
				(try_begin),
					(eq, ":faction_no", "$players_kingdom"),
					(val_add, ":rating_current", 100),
				(try_end),
				# Improve rating based on being closest to the player.
				(try_begin),
					(store_distance_to_party_from_party, ":distance", "p_main_party", ":center_no"),
					(store_sub, ":rating_distance", 100, ":distance"),
					(val_add, ":rating_current", ":rating_distance"),
				(try_end),
				# Improve rating based relation with host.
				(try_begin),
					(call_script, "script_troop_get_player_relation", ":troop_host"),
					(assign, ":host_relation", reg0),
					(val_add, ":rating_current", ":host_relation"),
				(try_end),
				## COMPARISON STAGE ##
				(this_or_next|ge, ":rating_current", ":best_rated_town"),
				(eq, ":best_rated_town", -1),
				(assign, ":best_rated_town", ":rating_current"),
				(assign, ":closest_town_no", ":center_no"),
				(ge, DEBUG_TPE_QUESTS, 1),
				(assign, reg31, ":has_tournament"),
				(str_store_party_name, s31, ":center_no"),
				(display_message, "@DEBUG (Quest Pack 1): {s31} has a tournament with {reg31} days left."),
			(else_try),
				##### FAIL QUEST: EXPIRED #####
				(le, ":has_tournament", 0),
				# Condition: Ensure quest IS active.
				(check_quest_active, "qst_floris_active_tournament"),
				(neg|quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_participated_in_tournament),
				(neg|quest_slot_eq, "qst_floris_active_tournament", slot_quest_current_state, qp1_tournament_refused_invitation),
				(quest_slot_eq, "qst_floris_active_tournament", slot_quest_target_center, ":center_no"),
				# Set quest to failed due to timeout.
				(call_script, "script_quest_floris_active_tournament", floris_quest_fail),
			(else_try),
				##### FAIL QUEST: HELD IN HOSTILE CITY ####
				(check_quest_active, "qst_floris_active_tournament"),
				(quest_slot_eq, "qst_floris_active_tournament", slot_quest_target_center, ":center_no"),
				(call_script, "script_tpe_store_town_faction_to_reg0", ":center_no"),
				(store_relation, ":relation", reg0, "fac_player_supporters_faction"),
				(lt, ":relation", 0),
				# Cancel quest to failed due to inability to attend.
				(call_script, "script_quest_floris_active_tournament", floris_quest_cancel),
			(try_end),
		(try_end),
		
		# Now assign a tournament to go to if there is a valid option and the quest isn't already active.
		(is_between, ":closest_town_no", towns_begin, towns_end),
		(neg|check_quest_active, "qst_floris_active_tournament"),
		(quest_slot_eq, "qst_floris_active_tournament", slot_quest_dont_give_again_remaining_days, 0),
				
		# Initialize some quest information.
		(quest_set_slot, "qst_floris_active_tournament", slot_quest_target_center, ":closest_town_no"),
		(call_script, "script_quest_floris_active_tournament", floris_quest_begin),
	]),

# QUEST: floris_active_tournament
# Determine if tournaments are active in a town.
#  - Deliver quest if tournament active and quest is not.  
#  - End quest if tournament is not active and quest is.
(12,
	[
		(map_free),
		(this_or_next|ge, DEBUG_TPE_general, 1),
		(ge, DEBUG_TPE_QUESTS, 1),
		(eq, "$g_wp_tpe_active", 1),
		(str_clear, s21),
		(display_message, "@List of Active Tournaments"),
		(try_for_range, ":center_no", towns_begin, towns_end),
			(party_get_slot, ":has_tournament", ":center_no", slot_town_has_tournament), # 0 = no, 1 = last day, 2+ = ongoing.
			(ge, ":has_tournament", 1),
			(assign, reg31, ":has_tournament"),
			(str_store_party_name, s31, ":center_no"),
			(display_message, "@{s31} has a tournament with {reg31} days left."),
		(try_end),
	]),
]


# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "simple_triggers"
        orig_simple_triggers = var_set[var_name_1]
        orig_simple_triggers.extend(simple_triggers)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)