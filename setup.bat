@ECHO OFF
CD %~dp0
IF NOT EXIST userdata ( MKDIR userdata )
IF NOT EXIST userdata\refs ( MKDIR userdata\refs )
IF NOT EXIST userdata\saves ( MKDIR userdata\saves )
IF NOT EXIST userdata\targets ( MKDIR userdata\targets )
IF NOT EXIST userdata\out ( MKDIR userdata\out )
dir /b %~dp0userdata\targets | findstr . > nul || (
	ECHO Need at least one image in .\userdata\targets folder.
	PAUSE
	EXIT
)
py refdatmkr.py
ECHO DONE
PAUSE