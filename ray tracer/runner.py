from common import *
import app

W = 640
H = 480

if __name__ == "__main__":
    # Pass in desired width and height
    myApp = app.App(width=W, height=H)
    myApp.quit()