# import os
import time
import cv2
import pyautogui


player = pyautogui.getWindowsWithTitle("BlueStacks App Player")[0]
player.activate()
img:int = 0
while True:
	# time.sleep(.25)
	pyautogui.screenshot(f"./data/targets/{img}.png", (player.left, player.top, player.width, player.height))
	pyautogui.mouseDown(player.left+player.width*.6,player.top+player.height/2)
	pyautogui.moveTo(player.left+player.width*.4,player.top+player.height/2,duration=0.25)
	pyautogui.mouseUp()
	# files:list[str] = os.listdir("./data/targets/")
	sim:float = ((cv2.imread(f"./data/targets/{img}.png")-cv2.imread(f"./data/targets/{img-1}.png"))**2).mean() if img > 1 else 101
	print(sim, sim < 20)
	img+=1
	time.sleep(1)
	if sim < 20: break
print("DONE")



"""
# tD: tuple[int, ...] = template.shape[::-1]
if len(loc[0]) > 0:
	# print(c, len(loc[0]))
	# for pt in zip(*loc[::-1]):
	# 	cv2.rectangle(target, pt, (pt[0]+tD[-2], pt[1]+tD[-1]), (255,0,255),2) # type: ignore
	# Image.fromarray(target,"L").show() # type: ignore
import os
from lib.types.operator import *
from lib.types.misc import *
import colorama
# from PIL import Image
from datetime import datetime as dt
colorama.init(True) # type: ignore

profRefDta:RefData = RefData(0.8907595872879028, 112, 26, 834)
promRefDta:RefData = RefData(0.9001659750938416, 126, 1148, 323)

# profRefDta:RefData = RefData(0.8677231669425964, 130, 29, 892)
# promRefDta:RefData = RefData(0.9216563701629639, 139, 1314, 300)

# profRefDta:RefData = getProfessionReferenceData(cv2.imread("./testdata/andreana.png"))
# print(profRefDta.toTuple())
# promRefDta:RefData = getPromotionReferenceData(cv2.imread("./testdata/andreana.png"))
# print(promRefDta.toTuple())


allDeltas:list[float] = []
dmp = []
success:list[Operator] = []
for f in sorted(os.listdir("./testdata/")[0:]):
	try:
		t0:dt = dt.now()
		o = Operator(f"./testdata/{f}", profRefDta, promRefDta)
		allDeltas.append((dt.now()-t0).total_seconds())
		if allDeltas[-1] < .75: c: str = colorama.Fore.LIGHTCYAN_EX
		elif allDeltas[-1] < 1: c = colorama.Fore.GREEN
		elif allDeltas[-1] < 1.5: c = colorama.Fore.YELLOW
		else: c = colorama.Fore.RED
		print(o.IMAGE_PATH.ljust(30), f"[NAME: {o.name}]".ljust(26), f"[E{o.promotion} LVL{str(o.level).rjust(2)}]".ljust(11), f"[POT {o.potential}]".ljust(8), f"[R {(o.skills.rank)}]".ljust(7), f"[M {[m.mastery if m != None else -1 for m in o.skills.masteries]}]".ljust(26), f"M {o.module.type} S {o.module.stage}".ljust(16), f"{c}TIME: {allDeltas[-1]}")
		o.save("./data/saves/")
		success.append(o)
		# Image.fromarray(bgraToRgba(o.drawAllBounds())).show()
		# dmp.append(o.toJson()) # type: ignore
	except:
		# print(f"{colorama.Fore.LIGHTBLUE_EX} {f}")
		raise

# checked = []
# chdata = json.load(open("./checkdata.json"))
# for co in dmp: # type: ignore
# 	# if co == list(filter(lambda x: co in x, dmp))[0]:
# 	if co in chdata: checked.append(co) # type: ignore
# 	else: print(co.get("id")) # type: ignore

json.dump(dmp, open("./dmp.json", "w"))
print(str(len(success)/len(os.listdir("./testdata/"))*100)+f"% in {sum(allDeltas)} [avg / {sum(allDeltas)/len(allDeltas)}]")"""