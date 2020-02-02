import eel

@eel.expose
def python_function(val):
    print(val + " from JavaScript")

eel.init("./")
eel.start("index.html")