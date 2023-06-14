import json
SETTINGS_FILE:str = "./userdata/settings.json"

def getSettingBool(setting:str) -> bool:
	return bool(json.load(open(SETTINGS_FILE))[setting])
def setSettingBool(setting:str, state:bool) -> None:
	json.load(open(SETTINGS_FILE))[setting] = bool(state)

def getSettingString(setting:str) -> str:
	return str(json.load(open(SETTINGS_FILE))[setting])
def setSettingString(setting:str, value:str) -> None:
	json.load(open(SETTINGS_FILE))[setting] = str(value)

def getSettingNum(setting:str) -> float:
	return float(json.load(open(SETTINGS_FILE))[setting])
def setSettingNum(setting:str, value:float) -> None:
	json.load(open(SETTINGS_FILE))[setting] = float(value)
