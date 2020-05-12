from tkinter import *
import subprocess
import threading
import queue
import os
from os import system
from re import sub
import sys

os.environ["PYTHONUNBUFFERED"] = "1"

def enqueue_output(p, q):
    while True:
        out = p.stdout.readline()
        if out == '' and p.poll() is not None:
            break
        if out:
            print("before queue" + out.strip(), flush=True)
            q.put_nowait(out.strip())


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.started = False
        self.p = None
        self.q = queue.Queue()
        self.threads = 1
        self.init_window()

    def init_window(self):
        self.master.title("RandomX Stress Tester")
        self.pack(fill=BOTH, expand=1)

        self.hashrateLabel = Label(self, text="Hashrate: ")
        self.hashrateLabel.after(2000, self.refresh_hashrate)
   
        self.startButton = Button(self, text="Start", background="green", command=self.startstop)
        self.quitButton = Button(self, text="Quit", command=self.client_exit)

        self.hashrateLabel.place(x=50, y=220)
        self.startButton.place(x=50, y=270)
        self.quitButton.place(x=220, y=270)

    def startstop(self):
        if not self.started:
            self.p = subprocess.Popen([r"randomx-stress.exe", "-t", str(self.threads)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        shell=True,
                        encoding='utf-8',
                        errors='replace')
            self.t = threading.Thread(target=enqueue_output, args=(self.p, self.q))
            self.t.daemon = True
            self.t.start()
            self.started = True
            self.startButton.config(text="Stop", background="red")
        elif self.started:
            system("taskkill /im randomx-stress.exe /f")
            self.p.kill()
            self.t.join()
            self.started = False
            self.startButton.config(text="Start", background="green")

    def refresh_hashrate(self):
        if not self.started:
            pass
        elif self.started:
            try:
                line = self.q.get_nowait()
                print("after queue" + line)
                if 'H/s' in line:
                    hashrate = line.split(' ')[0]
                    self.hashrateLabel.text = "Hashrate: {0:.2f} h/s".format(hashrate)
            except:
                print("error")
        self.hashrateLabel.after(2000, self.refresh_hashrate)

    def client_exit(self):
        exit()


root = Tk()
root.geometry("400x300")

app = Window(root)
root.mainloop()

