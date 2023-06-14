import argparse
import eel
from lib.types.operator import *
# from PIL import Image
from lib.expose import exposeAll

if __name__ == "__main__":
    # Parse arguments
    # Inspired from https://github.com/WiIIiamTang/create-sveltekit-eel-app/blob/main/templates/base/eelApp.py
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", default=False)
    parser.add_argument("--mode", type=str, default="chrome")
    args = parser.parse_args()

    # Initialize Eel
    eel.init("./src" if args.dev else "./build", [".tsx", ".ts", ".jsx", ".js", ".html", ".svelte"]) # type: ignore
    exposeAll()
    eel.start("" if not args.dev else {"port": 5173}, port=8888, mode=None if args.mode == "None" else args.mode) # type: ignore
