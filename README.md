# CopyToTranslate

CopyToTranslate is a simple and efficient clipboard translator that allows users to double-press Ctrl+C to translate clipboard content using either Baidu or Google Translate API. The application is built with Python and PyQt5, providing a sleek and modern GUI.

## Features

- **Hotkey Listener**: Double-press Ctrl+C to trigger translation.
- **Translation Services**: Choose between Baidu and Google Translate API.
- **Configurable Settings**: Modify App ID, Secret Key, and translation service via a settings dialog.
- **Adjustable Transparency**: Use a slider to adjust the window's transparency.
- **Always on Top**: The application window stays on top of other windows.
- **Draggable Window**: Easily move the window by dragging it.

## Installation

- Clone the repository:

```bash
git clone https://github.com/yourusername/CopyToTranslate.git
cd CopyToTranslate
```

- Install the required dependencies:

```bash
pip install -r requirements.txt
```
## Usage
- Run the application:

```bash
python app.py
```
- Access the settings from the menu bar to configure the App ID, Secret Key, and translation service.
- Double-press Ctrl+C to translate the content of your clipboard.

## Configuration
- The application uses a config.json file to store the App ID, Secret Key, and selected translation service. The file should be located in the root directory of the project. The initial structure of the file is as follows:

```json
{
    "appid": "your_app_id",
    "secret_key": "your_secret_key",
    "translation_service": "baidu"  // Options: 'baidu' or 'google'
}
```
## Project Structure

```plaintext
CopyToTranslate/
├── .gitignore
├── app.py
├── config.json
├── hotkey_listener.py
├── translator.py
├── ui.py
└── requirements.txt
```