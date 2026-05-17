# ZugzwangSecure

Lock access to specified applications until a chess puzzle is solved.

## Setup

1. Install dependencies:
   ```bash
   pip install flask pywebview psutil

2. Configure target apps in main.py:
    Example: LOCKED_APPS = ["chrome.exe", "spotify.exe", "discord.exe"]

3. Run the application:
   ```bash
   python main.py

### Add database:
   - This project requires a chess puzzle database named `puzzles.db` in the root folder.
   - You can download the massive puzzle dataset from [Lichess Open Database](https://database.lichess.org/#puzzles).
   - *Note: The Lichess file is downloaded as a compressed `.bz2` file containing a `.csv`. You will need to extract it and import the data into an SQLite database named `puzzles.db` before running the application.*

#### Enable on Startup (Windows)

1. Build the executable using PyInstaller.

2. Press Win + R, type shell:startup, and press Enter.

3. Create a shortcut of your built .exe file and drop it into that folder.