from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QUrl

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.webview = QWebEngineView()

        settings = self.webview.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        self.webview.page().profile().setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        )

        self.webview.setUrl(QUrl("Enter Address"))
        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)

        self.webview.page().fullScreenRequested.connect(self.handle_fullscreen)

    def navigate_to(self, url: str):
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.webview.setUrl(QUrl(url))

    def handle_fullscreen(self, request):
        request.accept()
        main_window = self.window()
        if request.toggleOn():
            main_window._enter_fullscreen()
        else:
            main_window._exit_fullscreen()
