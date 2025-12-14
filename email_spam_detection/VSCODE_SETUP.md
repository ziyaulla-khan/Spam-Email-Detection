# VS Code Setup Guide

This guide will help you get started with the Email Spam Detection project in VS Code.

## Quick Start

### Option 1: Open Workspace (Recommended)
1. Open VS Code
2. Go to `File > Open Workspace from File...`
3. Select `email_spam_detection.code-workspace`
4. This will open the project with all recommended settings

### Option 2: Open Folder
1. Open VS Code
2. Go to `File > Open Folder...`
3. Navigate to and select the `email_spam_detection` folder

## Initial Setup

### 1. Install Python Extension
VS Code will prompt you to install the Python extension if not already installed. Click "Install" when prompted.

### 2. Install Dependencies
Open the terminal in VS Code (`Ctrl + ~` or `Terminal > New Terminal`) and run:

```bash
pip install -r requirements.txt
```

Or use the built-in task:
- Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on Mac)
- Type "Tasks: Run Task"
- Select "Install Dependencies"

### 3. Select Python Interpreter
- Press `Ctrl + Shift + P`
- Type "Python: Select Interpreter"
- Choose your Python interpreter (Python 3.8 or higher)

## Running the Application

### Method 1: Using Debug (Recommended)
1. Open `spam_detector.py`
2. Press `F5` or click the "Run and Debug" icon in the sidebar
3. Select "Python: Spam Detector" from the dropdown
4. Click the green play button or press `F5`

### Method 2: Using Terminal
1. Open the integrated terminal (`Ctrl + ~`)
2. Run: `python spam_detector.py`

### Method 3: Using Tasks
1. Press `Ctrl + Shift + P`
2. Type "Tasks: Run Task"
3. Select "Run Spam Detector"

## VS Code Features

### Debugging
- Set breakpoints by clicking left of line numbers
- Use the Debug panel (Ctrl + Shift + D) to start debugging
- Step through code with F10 (step over) and F11 (step into)

### IntelliSense
- Auto-completion for Python code
- Hover over code to see documentation
- Right-click for context menu options

### Integrated Terminal
- Access terminal with `Ctrl + ~`
- Multiple terminals can be opened
- Terminal automatically activates in project directory

## Project Structure

```
email_spam_detection/
├── .vscode/              # VS Code configuration
│   ├── settings.json     # Python and editor settings
│   ├── launch.json       # Debug configurations
│   ├── tasks.json        # Build and run tasks
│   └── extensions.json   # Recommended extensions
├── spam_detector.py      # Main application file
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore           # Git ignore rules
└── email_spam_detection.code-workspace  # Workspace file
```

## Troubleshooting

### Python Not Found
- Make sure Python is installed and in your PATH
- Use `python --version` in terminal to verify
- Install Python from [python.org](https://www.python.org/)

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using the correct Python interpreter
- Restart VS Code after installing packages

### Gradio Not Opening
- Check if port 7860 is already in use
- The URL will be displayed in the terminal output
- Try changing the port in `spam_detector.py` if needed

## Recommended VS Code Extensions

The following extensions are recommended (already configured):
- **Python** (ms-python.python) - Python language support
- **Pylance** (ms-python.vscode-pylance) - Fast Python language server
- **Black Formatter** (ms-python.black-formatter) - Code formatting
- **Jupyter** (ms-toolsai.jupyter) - Jupyter notebook support

These will be suggested automatically when you open the workspace.

## Keyboard Shortcuts

- `F5` - Start debugging
- `Ctrl + F5` - Run without debugging
- `F9` - Toggle breakpoint
- `F10` - Step over
- `F11` - Step into
- `Shift + F11` - Step out
- `Ctrl + ~` - Toggle terminal
- `Ctrl + Shift + P` - Command palette

## Next Steps

1. Open `spam_detector.py` to explore the code
2. Run the application using one of the methods above
3. Open the Gradio interface in your browser (URL shown in terminal)
4. Test the spam detection with sample emails

Happy coding! 🚀

