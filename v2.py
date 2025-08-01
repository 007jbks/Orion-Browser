from cefpython3 import cefpython as cef
import sys

def main():
    sys.excepthook = cef.ExceptHook  # To shutdown properly on error
    cef.Initialize()
    
    window_info = cef.WindowInfo()
    window_info.SetAsChild(0)  
    browser = cef.CreateBrowserSync(
        url="https://www.google.com",
        window_title="Orion Browser V2"
    )

    cef.MessageLoop()
    cef.Shutdown()

if __name__ == "__main__":
    main()
