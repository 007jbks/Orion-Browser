import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineCore import QWebEngineProfile
from browser import Browser
import os
os.makedirs("web_profile_storage", exist_ok=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    profile = QWebEngineProfile.defaultProfile()
    profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
    profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
    profile.setPersistentStoragePath("web_profile_storage")

    window = Browser(app)
    window.show()
    sys.exit(app.exec())
