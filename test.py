from lib.expose import exposeAll
import eel


eel.init("./src/") # type: ignore
exposeAll()
eel.start("index.html", mode="firefox") # type: ignore
# getPlayer("Emu", "awdasd")
