from emitter import EventEmitter

emitter = EventEmitter()

def test0():
    print("test0")

def test1():
    print("test1")

async def test2():
    print("test2")

def testOnce():
    print("testOnce")

def addListenerTest():
    print("==== addListenerTest ====")
    emitter.addListener("test", test0)
    emitter.addListener("test", test1)
    emitter.addListener("test", test2)
    emitter.emit("test")
    print("==== addListenerTest Done ====")

def removeListenerTest():
    print("==== removeListenerTest ====")
    emitter.removeListener("test", test0)
    emitter.emit("test")
    print("==== removeListenerTest Done ====")

def removeAllListenersTest():
    print("==== removeAllListenersTest ====")
    emitter.addListener("rl-test", test0)
    emitter.addListener("rl-test", test1)
    emitter.addListener("rl-test", test2)
    emitter.emit("rl-test")
    emitter.removeAllListeners("rl-test")
    emitter.emit("rl-test")
    print("==== removeAllListenersTest Done ====")


def onceTest():
    print("==== onceTest ====")
    emitter.once("test", testOnce)
    emitter.emit("test")
    emitter.emit("test")
    print("==== onceTest Done ====")

def emitTest():
    print("==== emitTest ====")
    emitter.emit("test")
    emitter.emit("not-exist-test")
    print("==== emitTest Done ====")
    

def run():
    addListenerTest()
    removeListenerTest()
    removeAllListenersTest()
    onceTest()
    emitTest()

run()