@ECHO OFF
CD %~dp0
IF NOT EXIST data\refs ( MKDIR data\refs )
IF NOT EXIST data\saves ( MKDIR data\saves )
IF NOT EXIST data\targets ( MKDIR data\targets )
IF NOT EXIST data\out ( MKDIR data\out )
dir /b %~dp0data\targets | findstr . > nul || (
	ECHO Need at least one image in .\data\targets folder.
	PAUSE
	EXIT
)
py refdatmkr.py
ECHO DONE
PAUSE