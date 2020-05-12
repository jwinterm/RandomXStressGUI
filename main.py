from tkinter import *
from PIL import ImageTk, Image
import subprocess
import threading
import queue
import os
import re
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
            #print(out.strip(), flush=True)
            q.put_nowait(out.strip())


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.started = False
        self.p = None
        self.q = queue.Queue()
        self.threads = 4
        self.imgStopped = ImageTk.PhotoImage(Image.open("notstress.jpg"))
        self.imgStarted = ImageTk.PhotoImage(Image.open("stress.jpg")) 
        self.checkbuttonvar = IntVar()
        self.init_window()


    def init_window(self):
        self.master.title("RandomX Stress Tester")
        self.pack(fill=BOTH, expand=1)

        self.titleLabel = Label(self, text="RandomX Stress Tester GUI", font=("Comic Sans MS", 16))

        self.statusLabel = Label(self, text="Current status:\nNot Stressed")
  
        self.statusImage = Label(image=self.imgStopped)
        self.statusImage.image = self.imgStopped

        self.hashrateLabel = Label(self, text="Hashrate: ")

        self.threadsLabel = Label(self, text="# of threads: ")
        self.threadsEntry = Entry(self, textvariable=self.threads, width=5)
        self.threadsEntry.insert(0, "4")

        self.hugepagesCheckbutton = Checkbutton(self, text="Use hugepages", variable=self.checkbuttonvar)

        self.hashrateLabel = Label(self, text="Hashrate: 0 h/s")
        self.hashrateLabel.after(2000, self.refresh_hashrate)
   
        self.startButton = Button(self, text="Start", background="green", command=self.startstop)
        self.quitButton = Button(self, text="Quit", command=self.client_exit)

        self.titleLabel.place(x=60, y=20)
        self.statusLabel.place(x=50, y=80)
        self.statusImage.place(x=140, y=80)
        self.threadsLabel.place(x=50, y=180)
        self.threadsEntry.place(x=125, y=180)
        self.hugepagesCheckbutton.place(x=220, y=180)
        self.hashrateLabel.place(x=50, y=220)
        self.startButton.place(x=50, y=270)
        self.quitButton.place(x=220, y=270)

    def startstop(self):
        if not self.started:
            try:
                self.threads = int(self.threadsEntry.get())
            except:
                self.threads = 2
            if self.threads > 16:  
                self.selection_handlethreads = 16
            self.threadsEntry.delete(0, 4)
            self.threadsEntry.insert(0, self.threads)
            if not self.checkbuttonvar.get():
                self.p = subprocess.Popen([r"randomx-stress.exe", "-t", str(self.threads)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            #shell=True,
                            encoding='utf-8',
                            errors='replace')
            elif self.checkbuttonvar.get():
                self.p = subprocess.Popen([r"randomx-stress.exe", "-t", str(self.threads), "-H"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
            self.t = threading.Thread(target=enqueue_output, args=(self.p, self.q))
            self.t.daemon = True
            self.t.start()
            self.started = True
            self.statusImage = Label(image=self.imgStarted)
            self.statusImage.image = self.imgStarted
            self.statusImage.place(x=140, y=80)
            self.statusLabel.config(text="Current status:\nStressed")
            self.startButton.config(text="Stop", background="red")
        elif self.started:
            system("taskkill /im randomx-stress.exe /f")
            self.p.kill()
            self.t.join()
            self.started = False
            self.statusImage = Label(image=self.imgStopped)
            self.statusImage.image = self.imgStopped
            self.statusImage.place(x=140, y=80)
            self.statusLabel.config(text="Current status:\nNot stressed")
            self.hashrateLabel.config(text="Hashrate: 0 h/s")
            self.startButton.config(text="Start", background="green")

    def refresh_hashrate(self):
        #print("checking hashrate if running")
        if not self.started:
            pass
        elif self.started:
            #print("its running")
            try:
                line = self.q.get_nowait()
                #newline = self.q.get(block=False)
                #newLine = newLine.decode('utf-8')
                print(line)
                try:
                    #hashrate = line.split(' ')[0]
                    hashrate = re.findall("\d+\.\d+", line)[0]
                    print(hashrate)
                    self.hashrateLabel.config(text="Hashrate: {0:.2f} h/s".format(float(hashrate)))
                except:
                    print("cant parse")
            except:
                print("error")
        self.hashrateLabel.after(2000, self.refresh_hashrate)

    def client_exit(self):
        exit()


root = Tk()
root.iconbitmap('./stress.ico')
root.geometry("400x300")

app = Window(root)
root.mainloop()

