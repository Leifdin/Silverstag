@echo off
copy ".\Main Source\*.py" ".\" >>Process_Log.txt
copy ".\Modmerger\*.py" ".\" >>Process_Log.txt
copy ".\Source - Tournament Play Enhancements\*.py" ".\" >>Process_Log.txt
copy ".\Source - Generic Presentation Utilities\*.py" ".\" >>Process_Log.txt
copy ".\Source - Character Creation\*.py" ".\" >>Process_Log.txt
copy ".\Source - Combat Enhancements\*.py" ".\" >>Process_Log.txt
copy ".\Source - Dynamic Damage\*.py" ".\" >>Process_Log.txt
copy ".\Source - Game Options\*.py" ".\" >>Process_Log.txt
copy ".\Source - Companion Management System\*.py" ".\" >>Process_Log.txt
copy ".\Source - Dynamic Troop Trees\*.py" ".\" >>Process_Log.txt
copy ".\Source - Quest Utilities\*.py" ".\" >>Process_Log.txt
copy ".\Source - PBOD & Formations\*.py" ".\" >>Process_Log.txt
copy ".\Source - Jrider Presentations\*.py" ".\" >>Process_Log.txt
copy ".\Source - Heraldic Warhorses\*.py" ".\" >>Process_Log.txt
copy ".\Source - Enhanced Diplomacy\*.py" ".\" >>Process_Log.txt
copy ".\Source - Center Improvements\*.py" ".\" >>Process_Log.txt
copy ".\Source - Kingdom Management Tools\*.py" ".\" >>Process_Log.txt
copy ".\Source - Dynamic Arrays\*.py" ".\" >>Process_Log.txt
copy ".\Source - Quest Utilities\Quest Pack 2 (Trade)\*.py" ".\" >>Process_Log.txt
copy ".\Source - Quest Utilities\Quest Pack 3 (Nobility)\*.py" ".\" >>Process_Log.txt
copy ".\Source - Quest Utilities\Quest Pack 4 (Companions)\*.py" ".\" >>Process_Log.txt
copy ".\Source - Quest Utilities\Quest Pack 5 (Villages)\*.py" ".\" >>Process_Log.txt
copy ".\Source - Quest Utilities\Quest Pack 6 (Tutorials)\*.py" ".\" >>Process_Log.txt
copy ".\Source - Quest Utilities\Quest Pack 7 (Misc)\*.py" ".\" >>Process_Log.txt
copy ".\Source - Center Management\*.py" ".\" >>Process_Log.txt
copy ".\Source - Garrison Recruitment\*.py" ".\" >>Process_Log.txt
copy ".\Source - Silverstag Emblems\*.py" ".\" >>Process_Log.txt
copy ".\Source - Commissioned Items\*.py" ".\" >>Process_Log.txt

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
copy ID_*.py ".\Main Source\" >>Process_Log.txt
@del *.pyc
@del *.py
@del Process_Log.txt
echo.
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key to exit. . .
pause>nul
