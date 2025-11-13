import FreeSimpleGUI as sg
import threading
import clipboard as cb
import time

def update(window:sg.Window,list_to_update:list[str]):
    """
    Update a clipboard history list with the current saved clipboard entry, then reduce size of list to 30 items.
    
    Input the open window and the clipboard history list.

    The code writes the change into the event and value of the window.
    """
    while True:
        if not window["clipboard"].get() == cb.paste():
            list_to_update.insert(0,cb.paste())
            list_to_update.pop(30)
            window.write_event_value("clipboard",cb.paste())
        time.sleep(2)

clipboard_list:list[str] = [cb.paste()] + ["" for i in range(29)]

size=(30,30)

layout: list[list] = [
    [
        sg.T(text=cb.paste(),key="clipboard")
    ],[
        sg.HorizontalSeparator()
    ],[
        sg.Listbox(clipboard_list,key="listbox",size=size,enable_events=True)
    ]
]

window = sg.Window("Titel", layout=layout,finalize=True,grab_anywhere=True,keep_on_top=True)
threading.Thread(target=update,daemon=True,args=(window,clipboard_list)).start()

while True:
    event,val = window.read()
    # print(event,val)

    if event == "clipboard":
        window["clipboard"].update(value=cb.paste())
        window["listbox"].update(values=clipboard_list)

    if event == "listbox":
        cb.copy(*val["listbox"])

    if event is None:
        window.close()
        break
