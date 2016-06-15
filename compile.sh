#!/bin/bash
#make sure to modify build path in Main Source/module-info.py; note that the compiler will need absolute path in module_info.py
#you will probably need python 2.x(my is 2.7.8);

#switch module_info.py for my version

#cp ./'Main Source'/module_info.py ./'Main Source'/module_info.py.windy
#cp ./'Main Source'/module_info.py.leifdin ./'Main Source'/module_info.py
ls ./'Main Source'/module_info*

cp ./'Main Source'/*.py ./ >>Process_Log.txt
cp ./'Modmerger/'*.py ./ >>Process_Log.txt
cp ./'Source - Compiler'/*.py ./ >>Process_Log.txt
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


python compile.py tag %1 %2 %3 %4 %5 %6 %7 %8 %9

cp ID_*.py ./'Main Source'/ >>Process_Log.txt
rm *.py
rm Process_Log.txt

#move the old module_info.py back
#cp ./'Main Source'/module_info.py ./'Main Source'/module_info.py.leifdin
#cp ./'Main Source'/module_info.py.windy ./'Main Source'/module_info.py

echo done
