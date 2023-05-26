from io import TextIOWrapper
import json
df:TextIOWrapper = open("operatornames.txt", "w", encoding="utf-8")
df.write("\n".join(o[1].get("name")for o in dict(json.load(open("./operators.json", encoding="utf-8"))).items()))