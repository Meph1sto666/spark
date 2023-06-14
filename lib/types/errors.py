import typing
from types import TracebackType
import functools
import sys
import eel

def excParser(fn:typing.Callable[...,typing.Any]) -> typing.Callable[...,typing.Any]:
	@functools.wraps(fn)
	def wrapper(*args, **kwargs) -> typing.Any | None: # type: ignore
		try:
			res:typing.Any = fn(*args, **kwargs)
		except:
			inf:tuple[typing.Type[BaseException], BaseException, TracebackType] | tuple[None, None, None] = sys.exc_info()
			print(inf[0])
			if len(inf[1].args) > 0: # type: ignore
				eel.excHandler(list(inf[1].args)) # type: ignore
		else:
			return res
	return wrapper # type: ignore

# Operator
class OperatorProfessionConjectionFailed(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
class OperatorNameConjectionFailed(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
class OperatorRarityConjectionFailed(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
class OperatorLevelConjectionFailed(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
class OperatorPromotionConjectionFailed(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
class OperatorPotentialConjectionFailed(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
class SkillMasteryConjectionFailed(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
class SkillRankConjectionFailed(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
class OperatorNameNotFound(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__(*args)
# assa
class EmulatorProcessNotFound(BaseException):
	def __init__(self, *args: object) -> None:
		super().__init__("emu_not_found",*args)