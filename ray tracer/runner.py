from common import *
import app

W = 960
H = -1
USE_FXAA = True
# Set to False to disable FXAA

if __name__ == "__main__":
    # Pass in desired width, height, and FXAA setting
    myApp = app.App(width=W, height=H, use_fxaa=USE_FXAA)
    myApp.quit()