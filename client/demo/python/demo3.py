import asyncio
import threading
import time

main_loop = asyncio.get_event_loop()




def test(main_loop):
    def hello_world():
        f = open("test", "w")
        f.close()

    time.sleep(1)
    main_loop.call_soon(hello_world,main_loop)

t = threading.Thread(target=test,args=(main_loop,))
t.start()


main_loop.run_forever()
