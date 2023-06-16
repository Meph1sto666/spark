# import os
import pyautogui
from lib.settings import *
import typing
from lib.types.errors import EmulatorProcessNotFound
from lib.types import misc
import time
import cv2
import os

# class Assa:
# 	def __init__(self, emuId:str) -> None:
# 		self.emuId:str = emuId
# 		self.emuName:str = str(json.load(open("./data/emulators.json"))[emuId])

@misc.excParser
def getPlayer(emuId:str, emuName:str) -> typing.Any:
	windows:list[typing.Any] = pyautogui.getWindowsWithTitle(emuName) # type: ignore
	if len(windows) > 1: # type: ignore
		return windows[0] # type: ignore
	raise EmulatorProcessNotFound(emuId)

def capture(player:typing.Any, fName:str) -> None:
	pyautogui.screenshot(f"./userdata/targets/{fName}.png", (player.left, player.top, player.width, player.height)) # type: ignore

def scrollNext(player:typing.Any, duration:float=.25) -> None:
	pyautogui.mouseDown(player.left+player.width*.6,player.top+player.height/2) # type: ignore
	pyautogui.moveTo(player.left+player.width*.4,player.top+player.height/2,duration=duration) # type: ignore
	pyautogui.mouseUp()

def compareLastCaptures() -> float:
	files:list[str] = os.listdir("./userdata/targets/")
	if len(files) < 2: return 101 
	files = sorted(files, key=lambda x: int(x.split(".")[0]))
	print(files[-1],files[-2])
	return ((cv2.imread(f"./userdata/targets/{files[-1]}")-cv2.imread(f"./userdata/targets/{files[-2]}"))**2).mean() # type: ignore

if __name__ == "__main__":
	emu:str = getSettingString("assa_emulator")
	player:typing.Any = pyautogui.getWindowsWithTitle(emu)[0] # type: ignore
	player.activate() # type: ignore
	img:int = 0
	while True:
		time.sleep(.5)
		capture(player, str(img))
		scrollNext(player)
		sim = compareLastCaptures()
		print(sim, sim < 20) # type: ignore
		img+=1
		time.sleep(1)
		if sim < 20: break
	print("DONE")