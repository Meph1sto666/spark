import json
ops = json.load(open("./operators.json"))
classes: dict[str, list[str]] = {
	"Guard": [],
	"Caster": [],
	"Vanguard": [],
	"Medic": [],
	"Specialist": [],
	"Sniper": [],
	"Supporter": [],
	"Defender": [],
}
# json.dump(dict([(ops[o].get("class"), ops[o].get("id")) for o in ops]), open("./class2op.json", "w"))
[classes[ops[o].get("class")].append(ops[o]) for o in ops]
json.dump(classes, open("./class2op.json", "w"), indent=4)