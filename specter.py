import os
from lib.types.operator import *
from lib.types.misc import *
import colorama
from datetime import datetime as dt
colorama.init(True) # type: ignore
import pickle
from refdatmkr import *

rfGen:RefDataCreator = pickle.load(open("./data/refs/0.srdta", "rb"))
print(rfGen.profRefData.toTuple(), rfGen.promRefData.toTuple())
allDeltas:list[float] = []
dmp = []
success:list[Operator] = []
for f in sorted(os.listdir("./data/targets/")[0:]):
	try:
		t0:dt = dt.now()
		o = Operator(f"./data/targets/{f}", rfGen.profRefData, rfGen.promRefData)
		allDeltas.append((dt.now()-t0).total_seconds())
		if allDeltas[-1] < .75: c: str = colorama.Fore.LIGHTCYAN_EX
		elif allDeltas[-1] < 1: c = colorama.Fore.GREEN
		elif allDeltas[-1] < 1.5: c = colorama.Fore.YELLOW
		else: c = colorama.Fore.RED
		o.save("./data/saves/")
		success.append(o)
		dmp.append(o.toJson()) # type: ignore
		print(o.IMAGE_PATH.ljust(40), f"[NAME: {o.name}]".ljust(26), f"[E{o.promotion} LVL{str(o.level).rjust(2)}]".ljust(11), f"[POT {o.potential}]".ljust(8), f"[R {(o.skills.rank)} M {[m.mastery if m != None else -1 for m in o.skills.masteries]}]".ljust(18), f"M {o.module.type} S {o.module.stage}".ljust(16) if o.module.stage!=None else f"M None".ljust(16), f"{c}TIME: {allDeltas[-1]}")
	except:
		print(f"{colorama.Fore.LIGHTBLUE_EX} {f}")

json.dump(dmp, open(f"./data/out/{dt.now().strftime('%Y-%m-%dT%H-%M')}.json", "w"))
print(f"Exported into [./data/out/{dt.now().strftime('%Y-%m-%dT%H-%M')}.json] enjoy")
print(str(len(success)/len(os.listdir("./data/targets/"))*100)+f"% in {sum(allDeltas)} [avg / {sum(allDeltas)/len(allDeltas)}]")