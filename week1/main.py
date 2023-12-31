from pynput import mouse
from emitter import EventEmitter

emitter = EventEmitter()

@emitter.on("click", lambda x: x["pos_x"] < 500)
async def on_click_left(event):
    print("CLICK LEFT")

@emitter.on("click", lambda x: x["pos_x"] >= 500)
async def on_click_right(event):
    print("CLICK RIGHT")

def on_click(x, y, button, pressed):
    if (button == mouse.Button.right):
        print('Exiting...')
        return False
    if (pressed):
        emitter.emit("click", pos_x= x, pos_y= y)
    

with mouse.Listener(on_click=lambda x,y, button, pressed: on_click(x, y, button, pressed)) as listener:
    listener.join()






