set sourceFile="C:\dev\OpenRA\workspace\fitness.db"
set backupFolder=C:\Users\Thomas\Google Drive\Uni\S11\Masterarbeit\DB_backup\
set backupFilename=backup-%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%.db

copy %sourceFile% "%backupFolder%%backupFilename%"

if %errorlevel% neq 0 pause

set sourceFolder2="C:\Users\Thomas\Google Drive\Uni\S11\Masterarbeit\*"
set backupFolder2="C:\Users\Thomas\sciebo\Masterarbeit"
xcopy /y /k /i /e %sourceFolder2% "%backupFolder2%"

if %errorlevel% neq 0 pause
