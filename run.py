import multiprocessing
import time

def startJarvis():
    print("Proces 1")
    from main import start
    start()

def listenHotword():
    print("Process 2")
    from engine.features import hotword
    hotword()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=listenHotword)

    p1.start()
    p2.start()

    try:
        # Let processes run
        p1.join()
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        if p2.is_alive():
            p2.terminate()
            p2.join()
        print("System stop")
