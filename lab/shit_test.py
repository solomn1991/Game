import asyncio

import tkinter

w = tkinter.Tk()


loop = asyncio.get_event_loop()
loop.run_forever()