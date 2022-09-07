import webview
import json
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

# Default setting param
DEFAULT_PROPERTIES_VALUE = {
                               "launch_webserver":True,
                               "title":"Web Executer Tools",
                               "url":"./index.html",
                               "html":"",
                               "width":1280,
                               "height":720,
                               "x":None,
                               "y":None,
                               "resizable":True,
                               "fullscreen":False,
                               "min_size_x":200,
                               "min_size_y":100,
                               "hidden":False,
                               "frameless":False,
                               "minimized":False,
                               "on_top":False,
                               "confirm_close":False,
                               "background_color":"#FFF",
                               "text_select":True,
                               "debug":False,
                               "cef_mode":False,
                               "use_webserver_of_webview":True
                          }

# Load properties
class Properties:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_file()

    def load_file(self):
        try:
            with open(self.file_path) as f:
              self.param = json.load(f)
        except FileNotFoundError:
            self.save_file(DEFAULT_PROPERTIES_VALUE)
            self.load_file()
        except json.decoder.JSONDecodeError:
            self.save_file(DEFAULT_PROPERTIES_VALUE)
            self.load_file()

    def save_file(self, param):
        with open(self.file_path, 'w') as f:
            json.dump(param, f, indent=4)

    def get_value(self, key, none_value=None):
        try:
            return self.param[key]
        except:
            if none_value != None:
                self.set_value(key, none_value)
            return none_value

    def set_value(self, key, value):
        try:    
            self.param[key] = value
        except:
            pass
print('[Info] Load properties from "./properties.json"')
prop = Properties("./properties.json")

if prop.get_value("launch_webserver",False) == True and prop.get_value("use_webserver_of_webview",True) == False:
    server = ThreadingHTTPServer(("localhost", 8000), SimpleHTTPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    prop.set_value("url","http://localhost:8000/")

# Setup webview
window = webview.create_window(
    title=prop.get_value("title",DEFAULT_PROPERTIES_VALUE["title"]),
    url=prop.get_value("url",DEFAULT_PROPERTIES_VALUE["url"]),
    html=prop.get_value("html",DEFAULT_PROPERTIES_VALUE["html"]),
    width=prop.get_value("width",DEFAULT_PROPERTIES_VALUE["width"]),
    height=prop.get_value("height",DEFAULT_PROPERTIES_VALUE["height"]),
    x=prop.get_value("x",DEFAULT_PROPERTIES_VALUE["x"]),
    y=prop.get_value("y",DEFAULT_PROPERTIES_VALUE["y"]),
    resizable=prop.get_value("resizable",DEFAULT_PROPERTIES_VALUE["resizable"]),
    fullscreen=prop.get_value("fullscreen",DEFAULT_PROPERTIES_VALUE["fullscreen"]),
    min_size=(prop.get_value("min_size_x",DEFAULT_PROPERTIES_VALUE["min_size_x"]), prop.get_value("min_size_y",DEFAULT_PROPERTIES_VALUE["min_size_y"])),
    hidden=prop.get_value("hidden",DEFAULT_PROPERTIES_VALUE["hidden"]),
    frameless=prop.get_value("frameless",DEFAULT_PROPERTIES_VALUE["frameless"]),
    minimized=prop.get_value("minimized",DEFAULT_PROPERTIES_VALUE["minimized"]),
    on_top=prop.get_value("on_top",DEFAULT_PROPERTIES_VALUE["on_top"]),
    confirm_close=prop.get_value("confirm_close",DEFAULT_PROPERTIES_VALUE["confirm_close"]),
    background_color=prop.get_value("background_color",DEFAULT_PROPERTIES_VALUE["background_color"]),
    text_select=prop.get_value("text_select",DEFAULT_PROPERTIES_VALUE["text_select"]),
)
print("[Info] Open webview")

# Console message separater
if prop.get_value("launch_webserver",False) == True:
    print("----------------------------------------------------------------------------")

# Start webview
if prop.get_value("cef_mode") != True:
    gui = None
else:
    gui = "cef"
if prop.get_value("launch_webserver",False) == True and prop.get_value("use_webserver_of_webview",True) == True:
    http_server = True
else:
    http_server = False
webview.start(gui=gui,http_server=http_server ,debug=prop.get_value("debug",DEFAULT_PROPERTIES_VALUE["debug"]))

# Console message separater
if prop.get_value("launch_webserver",False) == True:
    print("----------------------------------------------------------------------------")

print("[Info] Close webview")

if prop.get_value("launch_webserver",False) == True:
    print("[Info] Close webserver")