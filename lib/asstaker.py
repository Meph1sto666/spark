# # import os
# import time
# import cv2
# import pyautogui


# player = pyautogui.getWindowsWithTitle("BlueStacks App Player")[0] # type: ignore
# player.activate() # type: ignore
# img:int = 0
# while True:
# 	# time.sleep(.25)
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