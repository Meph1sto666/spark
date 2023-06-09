import os
from lib.types.operator import *
from lib.types.misc import *
import colorama
from datetime import datetime as dt
colorama.init(True) # type: ignore
import pickle
from refdatmkr import *
# from PIL import Image

rfGen:RefDataCreator = pickle.load(open("./userdata/refs/0.srdta", "rb"))
print(rfGen.profRefData.toTuple(), rfGen.promRefData.toTuple())
allDeltas:list[float] = []
dmp = []
success:list[Operator] = []
for f in sorted(os.listdir("./userdata/targets/")[0:]):
	try:
		t0:dt = dt.now()
		o = Operator(f"./userdata/targets/{f}", rfGen.profRefData, rfGen.promRefData)
		allDeltas.append((dt.now()-t0).total_seconds())
		if allDeltas[-1] < .75: c: str = colorama.Fore.LIGHTCYAN_EX
		elif allDeltas[-1] < 1: c = colorama.Fore.GREEN
		elif allDeltas[-1] < 1.5: c = colorama.Fore.YELLOW
		else: c = colorama.Fore.RED
		print(o.IMAGE_PATH.ljust(40), f"[NAME: {o.name.ljust(31)}]", f"[E{o.promotion} LVL{str(o.level).rjust(2)}]".ljust(10), f"[POT {o.potential}]".ljust(7), f"[R {(o.skills.rank)} M {str([m.mastery if m != None else -1 for m in o.skills.masteries]).ljust(9)}]", f"M {o.module.type} S {o.module.stage}".ljust(16) if o.module.stage!=None else f"M None".ljust(16), f"[LOVED {str(o.loved).ljust(5)}]", f"{c}TIME: {allDeltas[-1]}")
		# Image.fromarray(bgraToRgba(o.drawAllBounds())).save(f"./final/{o.id}.png")
		success.append(o)
		dmp.append(o.toJson()) # type: ignore
		o.save("./userdata/saves/")
	except:
		raise
		print(f"{colorama.Fore.LIGHTBLUE_EX} {f}")

json.dump(dmp, open(f"./userdata/out/{dt.now().strftime('%Y-%m-%dT%H-%M')}.json", "w"))
print(f"Exported into [./userdata/out/{dt.now().strftime('%Y-%m-%dT%H-%M')}.json] enjoy")
print(str(len(success)/len(os.listdir("./userdata/targets/"))*100)+f"% in {sum(allDeltas)} [avg / {sum(allDeltas)/len(allDeltas)}]")