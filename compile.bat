@echo off
copy ".\Main Source\*.py" ".\" >>Process_Log.txt
copy ".\Modmerger\*.py" ".\" >>Process_Log.txt
copy ".\Source - Compiler\*.py" ".\" >>Process_Log.txt
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

python compile.py tag %1 %2 %3 %4 %5 %6 %7 %8 %9

copy ID_*.py ".\Main Source\" >>Process_Log.txt
@del *.py
@del Process_Log.txt
echo.
echo ______________________________
echo.
echo Script processing has ended.
echo Press any key to exit. . .
pause>nul


