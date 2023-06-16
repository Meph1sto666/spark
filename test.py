# from lib.expose import exposeAll
# import eel
from lib.asstaker import *

# eel.init("./src/") # type: ignore
# exposeAll()
# eel.start("index.html", mode="firefox") # type: ignore

emu:str = getSettingString("assa_emulator")
player:typing.Any = pyautogui.getWindowsWithTitle(emu)[0] # type: ignore
player.activate() # type: ignore
print(player)
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