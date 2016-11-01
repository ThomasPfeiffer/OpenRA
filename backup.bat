set sourceFile="C:\dev\OpenRA\Scripts\balancing\fitness.db"
set backupFolder=C:\Users\Thomas\Google Drive\Uni\S11\Masterarbeit\DB_backup\
set backupFilename=backup-%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%.db
if exist %sourceFile% exit 0

copy %sourceFile% "%backupFolder%%backupFilename%"

if %errorlevel% neq 0 pause