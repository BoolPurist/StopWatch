'''
Created on 07.04.2019

@author: Naumann
'''

import tkinter as tk
import threading as th
import time



class Window(tk.Tk):
    
    def __init__(self, title='App', geometry=None):
        tk.Tk.__init__(self)
        self.title(title)
        self.geometry(geometry)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        return
    
class MainFrame(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        return

class SubFrame(tk.Frame):
            
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.labels = []
        return

    def addlabel(self, labelText='Label', lrow=None, lcolumn=None, textvar=None, labelfamily='Times', labelsize=12): 
        if textvar != None:
            label = tk.Label(self, textvariable=textvar)
        else:    
            label = tk.Label(self, text=labelText)
        label.config(font=(labelfamily, labelsize))    
        if lrow == None or lcolumn == None:
            label.grid()
        else:                
            label.grid(row=lrow, column=lcolumn)
        self.labels.append(label)
        return
    
    
class StopWatch(th.Thread):
    
    def __init__(self):
        th.Thread.__init__(self)
        self.running = True
        self.currentTime = 0
        self.currentTimeString = ''
        self.sec = 0
        self.min = 0
        self.timeString = ['0', '0']
        self.startingtime = 0
        return
        
    def run(self):
        self.startingtime = time.time()
        time.sleep(1)
        while self.running:
            self.currentTime = time.time() - self.startingtime
            self.currentTime = int(self.currentTime)
            self.sec = self.currentTime % 60
            self.min = int(self.currentTime/60)
            self.timeString[0] = str(self.min)
            self.timeString[1] = str(self.sec)
            self.currentTimeString = '.'.join(self.timeString)
            time.sleep(1)
        return
    

    def stopRunning(self):
        self.running = False
        return

    def getTime(self):
        return self.currentTimeString
        
    
def updateLabel(window, frame, var):
    global currentThread
    if currentThread:
        var.set(currentThread.getTime())         
    window.after(1000, updateLabel, window, frame, var)
    return

def startThread(event, window, frame, var):
    global currentThread
    try:
        thread = StopWatch()
        thread.start()
        currentThread = thread
        window.after(1000, updateLabel, window, frame, var)
    except:
        pass       
    return

def stopThread(event):
    global currentThread
    try:
        currentThread.stopRunning()
        currentThread = None
    except:
        pass    
    return
    

if __name__ == '__main__':
    # Variables for configuration.
    
    keyForStart = 'space'
    keyForStop = 's'
    
    keyIntrotuction = 'Key to start Stopwatch: ' + keyForStart + '\nKey to stop Stopwatch: ' + keyForStop
    
    keyForStart = '<' + keyForStart + '>'
    keyForStop = '<' + keyForStop + '>'
    
    # Titel being displayed in window
    title = 'Stop Watch'
    
    currentThread = None
    main = Window(title=title)
    mframe = MainFrame(main)
    subframe = SubFrame(mframe)
    labelvar = tk.StringVar()
    labelvar.set('0.0')
    subframe.addlabel(labelText='Time past', labelsize=20)
    subframe.addlabel(textvar=labelvar, labelsize=40)
    subframe.addlabel(labelText=keyIntrotuction, labelsize=15)
    main.bind(keyForStart, lambda event, window=main, frame=subframe, var=labelvar: startThread(event, window, frame, var))
    main.bind(keyForStop, stopThread)
    main.mainloop()
