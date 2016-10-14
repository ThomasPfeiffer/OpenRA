@echo off
IF "%~1"=="" GOTO INPUT
set mapName=%1

:EXEC
C:\dev\OpenRA\OpenRA.Utility.exe ra --check-yaml "C:\dev\OpenRA\mods\ra\maps\%mapName%"
GOTO DONE

:INPUT
set /p mapName="Enter map name: "
GOTO EXEC

:DONE
if %errorlevel%==0 echo sucess
if not %errorlevel%==0 echo failure