import os
import sys
from pathlib import Path
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))
from PySide6.QtWidgets import QApplication
from main import MainWindow

app = QApplication([])
win = MainWindow()
print('initial tabs:', [win.tabs.tabText(i) for i in range(win.tabs.count())])
win.format_toggle.setChecked(True)
print('after check tabs:', [win.tabs.tabText(i) for i in range(win.tabs.count())])
print('current format:', win.current_format)
win.format_toggle.setChecked(False)
print('after uncheck tabs:', [win.tabs.tabText(i) for i in range(win.tabs.count())])
app.quit()
