from PySide6.QtWidgets import QMainWindow, QTabWidget, QToolBar, QLineEdit
from PySide6.QtGui import QAction, QPalette, QColor
from PySide6.QtCore import Qt
from tab import BrowserTab
from PySide6.QtWebEngineCore import QWebEngineScript


class Browser(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Orion Browser")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)

        self.setCentralWidget(self.tabs)

        self.navbar = QToolBar()
        self.addToolBar(self.navbar)
        self._create_navbar()

        self._was_maximized = False
        self.dark_mode = False
        self.add_new_tab()

    def _create_navbar(self):
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.navbar.addAction(QAction("⟨", self, triggered=lambda: self.current_webview().back()))
        self.navbar.addAction(QAction("⟩", self, triggered=lambda: self.current_webview().forward()))
        self.navbar.addAction(QAction("⟳", self, triggered=lambda: self.current_webview().reload()))
        self.navbar.addAction(QAction("+", self, triggered=self.add_new_tab))

        self.navbar.addWidget(self.url_bar)

        dark_mode_btn = QAction("🌙", self)
        dark_mode_btn.triggered.connect(self.toggle_dark_mode)
        self.navbar.addAction(dark_mode_btn)

    def current_webview(self):
        return self.tabs.currentWidget().webview

    def _enter_fullscreen(self):
        self._was_maximized = self.isMaximized()
        self.menuBar().setVisible(False)
        self.navbar.setVisible(False)
        self.tabs.tabBar().setVisible(False)
        self.showFullScreen()

    def _exit_fullscreen(self):
        self.menuBar().setVisible(True)
        self.navbar.setVisible(True)
        self.tabs.tabBar().setVisible(True)
        self.showMaximized() if self._was_maximized else self.showNormal()

    def navigate_to_url(self):
        self.tabs.currentWidget().navigate_to(self.url_bar.text())

    def update_url_bar(self, index):
        if index >= 0:
            current_url = self.current_webview().url().toString()
            self.url_bar.setText(current_url)

    def add_new_tab(self, url: str = "https://google.com"):
        new_tab = BrowserTab()
        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        new_tab.webview.titleChanged.connect(lambda title: self.tabs.setTabText(index, title))
        new_tab.navigate_to(url)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def toggle_dark_mode(self):
        if not self.dark_mode:
            self.app.setStyle("Fusion")
            dark_palette = QPalette()
            dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.WindowText, Qt.white)
            dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
            dark_palette.setColor(QPalette.ToolTipText, Qt.white)
            dark_palette.setColor(QPalette.Text, Qt.white)
            dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
            dark_palette.setColor(QPalette.ButtonText, Qt.white)
            dark_palette.setColor(QPalette.BrightText, Qt.red)
            dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.HighlightedText, Qt.black)
            self.app.setPalette(dark_palette)
            self.dark_mode = True
        else:
            self.app.setStyle("Fusion")
            self.app.setPalette(QPalette())
            self.dark_mode = False

    def inject_adblock_script(self):
        script = QWebEngineScript()
        script.setName("AdBlock")
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setSourceCode("""
            // Hide YouTube ads elements (not foolproof)
            const style = document.createElement('style');
            style.innerHTML = `
                .ytp-ad-module, .video-ads, .ytp-ad-overlay-container, .ytp-ad-player-overlay,
                .ytp-ad-skip-button-container, .ytp-ad-text, .ytp-ad-preview-container {
                    display: none !important;
                }
            `;
            document.head.appendChild(style);
        """)
        self.webview.page().scripts().insert(script)

