@ECHO OFF
CD %~dp0
IF NOT EXIST userdata\refs ( MKDIR userdata\refs )
IF NOT EXIST userdata\saves ( MKDIR userdata\saves )
IF NOT EXIST userdata\targets (
	ECHO Please run setup.bat first
	PAUSE
	EXIT
)

py specter.py

PAUSE