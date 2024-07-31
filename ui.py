import logging
import re
import pyperclip
import json
from PyQt5.QtWidgets import (
    QLabel, QScrollArea, QVBoxLayout, QWidget, QAction, QMenuBar,
    QSlider, QHBoxLayout, QMenu, QApplication, QDialog, QLineEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QFont, QPainterPath, QRegion

from translator import Translator
from hotkey_listener import HotkeyListener

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(300, 300, 300, 250)  # Increased height for new widget
        self.layout = QVBoxLayout()

        self.appid_label = QLabel('App ID:')
        self.appid_input = QLineEdit()
        self.secret_key_label = QLabel('Secret Key:')
        self.secret_key_input = QLineEdit()

        self.service_label = QLabel('Translation Service:')
        self.service_combo = QComboBox()
        self.service_combo.addItems(['baidu', 'google'])

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_settings)

        self.layout.addWidget(self.appid_label)
        self.layout.addWidget(self.appid_input)
        self.layout.addWidget(self.secret_key_label)
        self.layout.addWidget(self.secret_key_input)
        self.layout.addWidget(self.service_label)
        self.layout.addWidget(self.service_combo)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)
    
    def save_settings(self):
        appid = self.appid_input.text()
        secret_key = self.secret_key_input.text()
        service = self.service_combo.currentText()
        if not appid or not secret_key:
            QMessageBox.warning(self, 'Input Error', 'Please enter both App ID and Secret Key.')
            return

        try:
            with open('config.json', 'w') as config_file:
                json.dump({'appid': appid, 'secret_key': secret_key, 'translation_service': service}, config_file)
            QMessageBox.information(self, 'Success', 'Settings saved successfully.')
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save settings: {e}')

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.config = self.load_config()
        self.translator = Translator(self.config['appid'], self.config['secret_key'], self.config['translation_service'])
        self.hotkey_listener = HotkeyListener(self.check_clipboard)
        self.hotkey_listener.start()
        self.oldPos = self.pos()

    def initUI(self):
        self.setWindowTitle('Translator')
        self.setGeometry(100, 100, 800, 540)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(400, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.result_label = QLabel("Double-press Ctrl+C to translate")
        self.result_label.setFont(QFont('Roboto', 14))
        self.result_label.setStyleSheet('''
            QLabel {
                background-color: #34495E;
                color: #FFFFFF;
                padding: 15px;
                border-radius: 10px;
            }
        ''')
        self.result_label.setWordWrap(True)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.result_label)
        scroll_area.setWidgetResizable(True)

        self.layout.addWidget(scroll_area)

        self.resize(self.result_label.sizeHint().width() + 20, self.result_label.sizeHint().height() + 50)
        
        # 菜单栏
        menubar = QMenuBar(self)
        settings_menu = QMenu('Settings', self)
        menubar.addMenu(settings_menu)

        # 添加设置菜单项
        settings_action = QAction('API Config', self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)
        
        # 添加退出菜单项
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        settings_menu.addAction(exit_action)

        # 添加透明度滑块
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(20, 100)  # 设置透明度范围
        self.slider.setValue(100)  # 默认值为100%不透明
        self.slider.valueChanged.connect(self.change_transparency)

        # 创建一个新的小部件来包含菜单栏和滑块
        menubar_layout = QHBoxLayout()
        menubar_layout.addWidget(menubar)
        menubar_layout.addWidget(self.slider)

        # 将新的小部件设置为主窗口的菜单栏
        self.layout.addLayout(menubar_layout)

        self.show()
        self.setWindowShape()  # 初始化时应用圆角形状

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.config = self.load_config()  # 重新加载配置
            self.translator = Translator(self.config['appid'], self.config['secret_key'])
    
    def load_config(self):
        try:
            with open('config.json', 'r') as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            config = {
                'appid': '',
                'secret_key': '',
                'translation_service': 'baidu'  # Default to Baidu if config is missing
            }
        except json.JSONDecodeError:
            logging.error('Failed to parse config file.')
            config = {
                'appid': '',
                'secret_key': '',
                'translation_service': 'baidu'  # Default to Baidu if config is corrupted
            }
        
        # Ensure all required keys are present
        if 'translation_service' not in config:
            config['translation_service'] = 'baidu'
        
        return config

    def setWindowShape(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, self.width(), self.height()), 20, 20)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        super().resizeEvent(event)  # 确保调用父类的实现
        self.setWindowShape()  # 在调整大小时更新窗口形状

    def change_transparency(self, value):
        self.setWindowOpacity(value / 100.0)

    def closeEvent(self, event):
        self.hotkey_listener.stop()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
            event.accept()

    def check_clipboard(self):
        clipboard_content = pyperclip.paste()
        text = re.sub(r' {3,}', ' ', clipboard_content)
        text = re.sub(r'\n+', ' ', text)
        formatted_content = text
        result = self.translator.baidu_translate(formatted_content, 'auto', 'zh')
        if result:
            translation = result.get('trans_result', [{}])[0].get('dst', 'No translation found.')
            self.result_label.setText(translation)
        else:
            self.result_label.setText("Error during translation.")
