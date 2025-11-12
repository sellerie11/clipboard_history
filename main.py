import FreeSimpleGUI as sg
import threading
import clipboard as cb
import time

def update(window:sg.Window,list_to_update:list[str]):
    while True:
        if not window["clipboard"].get() == cb.paste():
            list_to_update.insert(0,cb.paste())
            list_to_update.pop(30)
            window.write_event_value("clipboard",cb.paste())
        time.sleep(2)

clipboard_list = [cb.paste()] + ["" for i in range(29)]

size=(30,30)

layout = [
    [
        sg.T(text=cb.paste(),key="clipboard")
    ],[
        sg.HorizontalSeparator()
    ],[
        sg.Listbox(clipboard_list,key="listbox",size=size,enable_events=True)
    ]
]

w = sg.Window("Titel", layout=layout,finalize=True,grab_anywhere=True,keep_on_top=True)
threading.Thread(target=update,daemon=True,args=(w,clipboard_list)).start()

while True:
    e,v = w.read()
    print(e,v)

    if e == "clipboard":
        w["clipboard"].update(value=cb.paste())
        w["listbox"].update(values=clipboard_list)

    if e == "listbox":
        cb.copy(*v["listbox"])

    if e is None:
        w.close()
        break
