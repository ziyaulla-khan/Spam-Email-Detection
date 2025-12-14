# 🚀 Quick Start Guide

## ✅ Project Successfully Deployed in VS Code!

Your Email Spam Detection project is now ready to use in VS Code.

## 📋 What's Included

- ✅ Deep Learning Model (CNN-based) for spam detection
- ✅ Gradio Web Interface
- ✅ VS Code Debug Configuration
- ✅ VS Code Tasks for easy running
- ✅ Python Settings & Extensions
- ✅ Setup Scripts

## 🎯 Next Steps (In VS Code)

### 1. Install Dependencies
Open the terminal in VS Code (`Ctrl + ~`) and run:
```bash
pip install -r requirements.txt
```

Or use the task:
- Press `Ctrl + Shift + P`
- Type: `Tasks: Run Task`
- Select: `Install Dependencies`

### 2. Run the Application

**Option A: Debug Mode (Recommended)**
- Press `F5` or click the Debug icon (▶️) in the sidebar
- Select "Python: Spam Detector"
- The app will start and open in your browser

**Option B: Terminal**
- Open terminal (`Ctrl + ~`)
- Run: `python spam_detector.py`

**Option C: Task**
- Press `Ctrl + Shift + P`
- Type: `Tasks: Run Task`
- Select: `Run Spam Detector`

### 3. Access the Interface

Once running, you'll see a URL in the terminal like:
```
Running on local URL:  http://127.0.0.1:7860
```

Open this URL in your browser to use the spam detection interface!

## 🎨 VS Code Features Available

| Feature | Shortcut | Description |
|---------|----------|-------------|
| **Debug** | `F5` | Start debugging the application |
| **Terminal** | `Ctrl + ~` | Open integrated terminal |
| **Command Palette** | `Ctrl + Shift + P` | Access all commands |
| **Run Task** | `Ctrl + Shift + P` → "Tasks: Run Task" | Run predefined tasks |
| **Breakpoints** | Click left of line number | Set breakpoints for debugging |

## 📁 Project Structure

```
email_spam_detection/
├── .vscode/                          # VS Code configuration
│   ├── settings.json                 # Python settings
│   ├── launch.json                   # Debug configs
│   ├── tasks.json                    # Build tasks
│   └── extensions.json               # Recommended extensions
├── spam_detector.py                  # Main application ⭐
├── requirements.txt                  # Dependencies
├── README.md                         # Full documentation
├── VSCODE_SETUP.md                   # Detailed VS Code guide
├── QUICK_START.md                    # This file
├── setup.bat                         # Windows setup script
├── run.bat                           # Windows run script
└── email_spam_detection.code-workspace  # Workspace file
```

## 🔧 Troubleshooting

### Python Not Found
- Make sure Python 3.8+ is installed
- Check: `python --version` in terminal
- Install from: https://www.python.org/

### Import Errors
- Install dependencies: `pip install -r requirements.txt`
- Restart VS Code after installing packages

### Port Already in Use
- Change port in `spam_detector.py` (line 250)
- Change `server_port=7860` to another port like `7861`

## 📚 More Information

- **Full Documentation**: See `README.md`
- **VS Code Setup**: See `VSCODE_SETUP.md`
- **Main Code**: See `spam_detector.py`

## 🎉 You're All Set!

The project is deployed and ready. Just install dependencies and press `F5` to start!

Happy coding! 🚀

