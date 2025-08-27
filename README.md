```markdown
# Multi-AI Assistant (GUI Python Application)

This is a **GUI Python application** that functions as a **Multi-AI Assistant**. Getting started is simple: you just need to create a Gemini API key and provide it in the application's settings section. Once configured, your Multi-AI Assistant will be ready to go!

## Features

*   **Graphical User Interface (GUI):** Easy-to-use visual interface.
*   **Multi-AI Assistant:** Powered by the Gemini API for diverse AI interactions.
*   **Simple Setup:** Quick configuration with your Gemini API key.

## Getting Started

### 1. Obtain Gemini API Key

You will need an API key from Google's Gemini platform.
*   Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to create your Gemini API key.

### 2. Configure API Key in Application

1.  **Launch the Application:**
    *   If running from source, execute your Python script.
    *   If using the Windows app, simply click on the `.exe` file.
2.  **Go to Settings:** Once the application starts, navigate to the **"Settings"** section.
3.  **Enter API Key:** Input your Gemini API key into the designated field.
4.  **Save:** Click the "Save" button to store your API key.

That's it! Your Multi-AI Assistant is now ready to use.

---

## Running as a Windows Application (.exe)

Follow these steps to convert your Python application into a standalone Windows executable.

1.  **Install PyInstaller:**
    Open your command prompt or terminal and run:
    ```bash
    pip install pyinstaller
    ```
2.  **Navigate to Python File Directory:**
    Change your current directory to where your main Python application file (`yourpython_file.py`) is located.
    ```bash
    cd C:\path\to\your\pythonfile\directory
    ```
3.  **Create Executable:**
    Execute PyInstaller, replacing `yourpython_file.py` with the actual name of your main script:
    ```bash
    pyinstaller --onefile yourpython_file.py
    ```
4.  **Wait for Completion:**
    The process will take a little bit of time to complete as it packages your application.
5.  **Locate `dist` Folder:**
    After completion, a `dist` folder will be created in your current directory.
6.  **Find the Executable:**
    Inside the `dist` folder, you will find your `.exe` (Windows application) file.
7.  **Launch the App:**
    Simply double-click on the `.exe` file to start your Multi-AI Assistant.
8.  **Initial API Key Setup (First Run):**
    *   After the application starts, go to the **"Settings"** section.
    *   Enter your **Gemini API key**.
    *   **Save** the API key.
9.  **Ready to Use:**
    You can now use your Multi-AI Assistant as a convenient Windows application!
```
