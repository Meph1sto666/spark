import typing
import eel
from lib.types.operator import *
from lib.settings import * 

functions:list[typing.Callable[..., typing.Any]] = [
	getPromotionReferenceData,
	getProfessionReferenceData,
	getBool,
	setBool,
	getString,
	setString,
	getNum,
	setNum
]
for f in functions:
	eel.expose(f) # type: ignore