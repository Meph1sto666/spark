# SpectArk (SpArk)

## Used librarys

- pyautogui &#x2022; screenshots and emulator automations
- cv2 &#x2022; image recognition
- pytesseract &#x2022; text recognition
- PySide6 &#x2022; GUI

## How to use the test version

1. Install the python librarys
2. Get some screenshots and put them into `./userdata/targets/`
3. Run `setup.bat`
4. Run `v0.6.6.bat`
5. Enjoy your export in `./userdata/out/`

## ToDo / feature list

### Operators

- [x] Profession recognition
- [x] Rarity recognition
- [x] Name recognition
- [x] Level recogntion
- [x] Promotion recogntion
- [x] Potential recogntion
- Skills
  - [x] Rank recognition
  - [x] Masteries recognition
  - [ ] [Selected skill recognition]
- Module
  - [x] Module stage recognition
  - [x] Module recognition
- [ ] [Skin recognition]
- [ ] [Loved recognition]

### Depot

- [ ] Item position detection
- [ ] Item type recognition
- [ ] Item amount recognition

### Profile

- [ ] Find anchor point for RefData
- [ ] Friendcode recognition
- [ ] Level recognition
- [ ] Hire date recognition
- [ ] [Note recognition]

### \[Supports\]

- [ ] Find support positions
- Operator recognition
  - [ ] Recognize potential (limiting operator selection)
  - [ ] Recognize level (limiting operator selection)
  - [ ] Recognize promotion (limiting operator selection)
  - [ ] Recognize operator by avatar

### GUI

- Do stuff

**NOTE: Features in [angular brackets] are non-compulsory and might not be implemented at any time.**

## Using the GUI

The GUI is built using [SvelteKit](https://kit.svelte.dev/), [Tailwind CSS](https://tailwindcss.com/) and [TypeScript](https://www.typescriptlang.org/).
It is all powered by [eel](https://github.com/python-eel/Eel), which allows us to use Python functions in the GUI.

The UI library used is [Skeleton](https://www.skeleton.dev/).

> **Note**
> The package manager used is [yarn](https://yarnpkg.com/).

### Development

During development, you need to run the SvelteKit development server and the GUI at the same time.
The GUI will then connect to the development server, enabling features like hot reloading while also getting eel's exposed functions.

1. Run `pip install -r requirements.txt` to install all the required Python packages
2. Run `yarn install` to install all the required packages
3. Run `yarn dev` to start the development server
4. Run `python main.py --dev` in another shell to start eel and connect to the development server

> **Note**
> You can use the `--mode` flag to change the browser mode used by eel. Defaults to `chrome`.

### Production

In production, all the files will be compiled in the `build` folder and the GUI will be started using the compiled files.

1. Compile the SvelteKit files using `yarn build`
2. Run `python main.py` to start the GUI using the compiled files

> **Note**
> Because this is a desktop app, the static adapter of SvelteKit is used. This means that every file needs to be able to be pre-rendered (see [the SvelteKit documentation](https://kit.svelte.dev/docs/page-options#prerender) for more information).
