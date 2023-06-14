# import os
import pyautogui
from lib.settings import *
import typing
from lib.types.errors import EmulatorProcessNotFound
from lib.types import misc

# emu:str = getSettingString("assa_emulator")
# player = pyautogui.getWindowsWithTitle(emu)[0] # type: ignore
# player.activate() # type: ignore
# img:int = 0
# while True:
# 	time.sleep(.5)
# 	pyautogui.screenshot(f"./userdata/targets/{img}.png", (player.left, player.top, player.width, player.height)) # type: ignore
# 	pyautogui.mouseDown(player.left+player.width*.6,player.top+player.height/2) # type: ignore
# 	pyautogui.moveTo(player.left+player.width*.4,player.top+player.height/2,duration=0.25) # type: ignore
# 	pyautogui.mouseUp()
# 	# files:list[str] = os.listdir("./userdata/targets/")
# 	sim:float = ((cv2.imread(f"./userdata/targets/{img}.png")-cv2.imread(f"./userdata/targets/{img-1}.png"))**2).mean() if img > 1 else 101 # type: ignore
# 	print(sim, sim < 20) # type: ignore
# 	img+=1
# 	time.sleep(1)
# 	if sim < 20: break
# print("DONE")

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
