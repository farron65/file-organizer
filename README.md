# File Organizer

A small utility tool that watches your Downloads folder and automatically moves files to the correct directory based on keywords in the filename.

## How it works

When a file is created or moved into Downloads, the tool splits the filename into tokens and checks each token against a config file. If a match is found, the file is moved to the corresponding directory. All transfers are logged with a timestamp to `logs.txt`.

For example, a file named `Justice League Batman Lesson 19.pptx` would be moved to `D:/Justice League/Batman` because the token `batman` matches a key in the config.

## Setup

**1. Clone the repo and create a virtual environment**
```bash
  git clone https://github.com/farron65/file-organizer
  cd file-organizer
  python -m venv env
  env\Scripts\activate
  pip install -r requirements.txt
```

**2. Configure your directories**

Edit `config.json` to map keywords to destination folders:
```json
{
    "batman": "D:/Justice League/Batman",
    "spiderman": "D:/Justice League/Spidy",
    "flash": "D:/Justice League/Flash"
}
```

Keys are matched case-insensitively against tokens in the filename. Add as many as you need.

**3. Run manually**
```bash
python main.py
```

**4. Run on startup (Windows)**

To have the tool start automatically when you log in:

1. Open **Task Scheduler** and click **Create Basic Task**
2. Set the trigger to **When I log on**
3. For the action, select **Start a program**
4. In **Program/script**, enter the path to `pythonw.exe` inside your venv:
   ```
   D:\path\to your project\env\Scripts\pythonw.exe
   ```
5. In **Add arguments**, enter:
   ```
   main.py
   ```
6. In **Start in**, enter the project directory:
   ```
   D:\path\to your project\
   ```

Use `pythonw.exe` instead of `python.exe` to run the script silently without a console window. If you want to see the cmd use `python.exe` instead

## Logs

All file transfers are saved to `logs.txt` in the project directory with the format:
```
2026-03-07 21:04:48,935 Successfully moved the file 'example.pptx' to: 'D:/Justice League/Spidy' 🕸️
```

