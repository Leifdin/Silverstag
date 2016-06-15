#!/bin/bash
#make sure to modify build path in Main Source/module-info.py; note that the compiler will not accept ~ as shortcut to your home folder
#you will probably need python 2.x(my is 2.7.8);

#switch module_info.py for my version

#cp ./'Main Source'/module_info.py ./'Main Source'/module_info.py.windy
#cp ./'Main Source'/module_info.py.leifdin ./'Main Source'/module_info.py

cp ./'Main Source'/*.py ./ >>Process_Log.txt
cp ./'Modmerger/'*.py ./ >>Process_Log.txt
cp ./'Source - Tournament Play Enhancements'/*.py ./ >>Process_Log.txt
cp ./'Source - Generic Presentation Utilities'/*.py ./ >>Process_Log.txt
cp ./'Source - Character Creation'/*.py ./ >>Process_Log.txt
cp ./'Source - Combat Enhancements'/*.py ./ >>Process_Log.txt
cp ./'Source - Dynamic Damage'/*.py ./ >>Process_Log.txt
cp ./'Source - Game Options'/*.py ./ >>Process_Log.txt
cp ./'Source - Companion Management System'/*.py ./ >>Process_Log.txt
cp ./'Source - Dynamic Troop Trees'/*.py ./ >>Process_Log.txt
cp ./'Source - Quest Utilities'/*.py ./ >>Process_Log.txt
cp ./'Source - PBOD & Formations'/*.py ./ >>Process_Log.txt
cp ./'Source - Jrider Presentations'/*.py ./ >>Process_Log.txt
cp ./'Source - Heraldic Warhorses'/*.py ./ >>Process_Log.txt
cp ./'Source - Enhanced Diplomacy'/*.py ./ >>Process_Log.txt
cp ./'Source - Center Improvements'/*.py ./ >>Process_Log.txt
cp ./'Source - Kingdom Management Tools'/*.py ./ >>Process_Log.txt
cp ./'Source - Dynamic Arrays'/*.py ./ >>Process_Log.txt
cp ./'Source - Quest Utilities/Quest Pack 2 (Trade)'/*.py ./ >>Process_Log.txt
cp ./'Source - Quest Utilities/Quest Pack 3 (Nobility)'/*.py ./ >>Process_Log.txt
cp ./'Source - Quest Utilities/Quest Pack 4 (Companions)'/*.py ./ >>Process_Log.txt
cp ./'Source - Quest Utilities/Quest Pack 5 (Villages)'/*.py ./ >>Process_Log.txt
cp ./'Source - Quest Utilities/Quest Pack 6 (Tutorials)'/*.py ./ >>Process_Log.txt
cp ./'Source - Quest Utilities/Quest Pack 7 (Misc)'/*.py ./ >>Process_Log.txt
cp ./'Source - Center Management'/*.py ./ >>Process_Log.txt
cp ./'Source - Garrison Recruitment'/*.py ./ >>Process_Log.txt
cp ./'Source - Silverstag Emblems'/*.py ./ >>Process_Log.txt
cp ./'Source - Commissioned Items'/*.py ./ >>Process_Log.txt
cp ./'Source - Oathbound'/*.py ./ >>Process_Log.txt

python process_init.py
python process_global_variables.py
python process_strings.py
python process_skills.py
python process_music.py
python process_animations.py
python process_meshes.py
python process_sounds.py
python process_skins.py
python process_map_icons.py
python process_factions.py
python process_items.py
python process_scenes.py
python process_troops.py
python process_particle_sys.py
python process_scene_props.py
python process_tableau_materials.py
python process_presentations.py
python process_party_tmps.py
python process_parties.py
python process_quests.py
python process_info_pages.py
python process_scripts.py
python process_mission_tmps.py
python process_game_menus.py
python process_simple_triggers.py
python process_dialogs.py
python process_global_variables_unused.py
python process_postfx.py
cp ID_*.py ./'Main Source'/ >>Process_Log.txt
rm *.pyc
rm *.py

#move the old module_info.py back
#cp ./'Main Source'/module_info.py ./'Main Source'/module_info.py.leifdin
#cp ./'Main Source'/module_info.py.windy ./'Main Source'/module_info.py

echo done
