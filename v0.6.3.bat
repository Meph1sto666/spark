@ECHO OFF
CD %~dp0
IF NOT EXIST data\refs ( MKDIR data\refs )
IF NOT EXIST data\saves ( MKDIR data\saves )
IF NOT EXIST data\targets (
	ECHO Please run setup.bat first
	PAUSE
	EXIT
)

py specter.py

PAUSE