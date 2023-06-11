import os
from lib.types.operator import *
from lib.types.misc import *
import colorama
from datetime import datetime as dt
colorama.init(True) # type: ignore
import pickle
from refdatmkr import *
from PIL import Image

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

		timeDat:dict[str|None, float] = o.tTracker.diff()
		inf:str = " ".join([
			o.IMAGE_PATH.ljust(40),
			f"{timeToColorPrec(timeDat['rarity'])}[RTY {o.rarity}]",
			f"{timeToColorPrec(timeDat['prof'])}[PRF {o.profession[:2]}]",
			f"{timeToColorPrec(timeDat['name'])}[NME {o.name.ljust(31)}]",
			f"{timeToColorPrec(timeDat['prom'])}[PRM {o.promotion} {timeToColorPrec(timeDat['level'])}LVL {str(o.level).rjust(2)}]".ljust(10),
			f"{timeToColorPrec(timeDat['pot'])}[POT {o.potential}]".ljust(7),
			f"{timeToColorPrec(timeDat['skills'])}[RNK {(o.skills.rank)} MRY {str([m.mastery if m != None else -1 for m in o.skills.masteries]).ljust(9)}]",
			f"{timeToColorPrec(timeDat['module'])}[{f'MOD {o.module.type} SGE {o.module.stage}'.ljust(15) if o.module.stage!=None else f'MOD None'.ljust(15)}]",
			f"{timeToColorPrec(timeDat['fav'])}[FAV {str(o.loved).ljust(5)}]",
			f"{timeToColor(allDeltas[-1])}TME: {allDeltas[-1]}"
		])
		print(inf)

		Image.fromarray(bgraToRgba(o.drawAllBounds())).save(f"./final/{o.id}.png") # type: ignore
		success.append(o)
		dmp.append(o.toJson()) # type: ignore
		o.save("./userdata/saves/")
	except:
		raise
		print(f"{colorama.Fore.LIGHTBLUE_EX} {f}")

json.dump(dmp, open(f"./userdata/out/{dt.now().strftime('%Y-%m-%dT%H-%M')}.json", "w"))
print(f"Exported into [./userdata/out/{dt.now().strftime('%Y-%m-%dT%H-%M')}.json] enjoy")
print(str(len(success)/len(os.listdir("./userdata/targets/"))*100)+f"% in {sum(allDeltas)} [avg / {sum(allDeltas)/len(allDeltas)}]")