#skills: targetImg.crop((targetImg.width-650,500,targetImg.width,650))
#class: targetImg.crop((0,875,200,targetImg.height))
#elite: targetImg.crop((targetImg.width-625,300,targetImg.width-450,450))
"""
# tD: tuple[int, ...] = template.shape[::-1]
if len(loc[0]) > 0:
	# print(c, len(loc[0]))
	# for pt in zip(*loc[::-1]):
	# 	cv2.rectangle(target, pt, (pt[0]+tD[-2], pt[1]+tD[-1]), (255,0,255),2) # type: ignore
	# Image.fromarray(target,"L").show() # type: ignore
"""
import os
from lib.types.unit import *
from lib.types.misc import *
import colorama
from PIL import Image
from datetime import datetime as dt
colorama.init(True) # type: ignore


profRefDta:RefData = RefData(0.8907595872879028, 112, 26, 834)
# promRefDta:RefData = RefData(0.8907595872879028, 112, 26, 834)
promRefDta:RefData = RefData(0.9001659750938416, 126, 1148, 323)
success:list[Operator] = []

allDeltas:list[float] = []
# for f in os.listdir("./testdata/")[31:32]: # gg
for f in os.listdir("./testdata/")[0:]:
	t0:dt = dt.now()
	try:
		o = Operator(f"./testdata/{f}", profRefDta, promRefDta)
		allDeltas.append((dt.now()-t0).total_seconds())
		if allDeltas[-1] < .5: c = colorama.Fore.LIGHTCYAN_EX
		elif allDeltas[-1] < .75: c = colorama.Fore.GREEN
		elif allDeltas[-1] < 1: c = colorama.Fore.YELLOW
		else: c = colorama.Fore.RED
		print(o.IMAGE_PATH.ljust(30), f"NAME: {o.name}".ljust(20), f"E{o.promotion} LVL{o.level}".ljust(9), f"POT {o.potential}".ljust(6), f"{c}TIME: {allDeltas[-1]}")
		success.append(o)

		# Image.fromarray(bgraToRgba(o.skills.sb.crop(o.ORIGINAL))).show() # type: ignore
		# Image.fromarray(bgraToRgba(o.drawAllBounds())).show()
	except:
		raise
		print(f"{colorama.Fore.LIGHTBLUE_EX} {f}")
print(str(len(success)/len(os.listdir("./testdata/"))*100)+f"% in {sum(allDeltas)} [avg / {sum(allDeltas)/len(allDeltas)}]")