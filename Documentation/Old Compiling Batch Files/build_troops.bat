@echo off
copy ".\Main Source\*.py" ".\" >>Process_Log.txt
copy ".\Main Source\ID_*.py" ".\" >>Process_Log.txt
python process_troops.py
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