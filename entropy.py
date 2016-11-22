import Tkinter
from Tkinter import *
import tkMessageBox
import time
import random
import Queue
from PacketCapture import PacketCapture
from EntropyDataManager import EntropyDataManager
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
import socket
import threading


# This program calculates Shannon's entropy on captured packets

class EntropyGUI:
    def __init__(self, root, queue, endCommand, threadClient):
        self.queue = queue
        self.tc = threadClient
        self.numPackets = ""
        self.host = ""
        
        root.title("Entropy Analysis")

        # Add drop down menu
        menubar = Menu(root)
        root.config(menu=menubar)

        # create a pulldown menu, and add it to the menu bar
        operationMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=operationMenu)
        operationMenu.add_command(label="Open",
                                  command=self.openFile)
        operationMenu.add_command(label="Save",
                                  command=self.saveFile)
        operationMenu.add_command(label='Exit', accelerator='Alt+F4', 
                                  command=self.exitProgram)
        
        # Add a frame to hold seperator
        frame0 = Frame(root) # Create and add a frame to window
        frame0.grid(row = 1, column = 1, sticky = W)
        
        # Add a frame to hold...
        frame1 = Frame(root) # Create and add a frame to window
        frame1.grid(row = 2, column = 1, sticky = W)
        
        # Add a frame to hold
        frame2 = Frame(root)
        frame2.grid(row = 3, column = 1, sticky = W)
        
        # Add a frame to hold padding row
        frame3 = Frame(root)
        frame3.grid(row = 4, column = 1, sticky = W)
        
        # Add a frame to hold textarea and scrollbar
        frame4 = Frame(root)
        frame4.grid(row = 5, column = 1, sticky = W)
        
        ##### Frame 0 Contents ####
        # Spacer
        Label(frame0, text=" ").grid(row=1, column=1, sticky=W)          
                
        ##### Frame 1 Contents ####
        Label(frame1, text="           ").grid(row=1, column=1, sticky=W)
        Label(frame1, text="Enter Host IP").grid(row=1, column=2)
        Label(frame1, text="                  ").grid(row=1, column=3, sticky=W)
        Label(frame1, text="Number of Packets").grid(row=1, column=4, sticky=W)
        
        #### Frame 2 Contents ####
        Label(frame2, text="            ").grid(row=1, column=1, sticky=W)
        # Entrybox to get the host IP
        self.hostIP = StringVar()
        ip = socket.gethostbyname(socket.gethostname())
        self.textEntry = Entry(frame2, textvariable = self.hostIP)
        self.textEntry.grid(row=1, column=2, sticky=W)
        self.textEntry.insert(END, ip) #enter host IP in text entry box
        
        # Spacer
        Label(frame2, text=" ").grid(row=1, column=3, sticky=W)        
        
        # Enter number of packets to capture
        self.numPackts = StringVar()
        self.numPacktsEntry = Entry(frame2, textvariable = self.numPackts)
        self.numPacktsEntry.grid(row=1, column=4, sticky=W)
        
        # Spacer
        Label(frame2, text=" ").grid(row=1, column=5, sticky=W)
        
        # Button to trigger the packet capture
        button = Button(frame2)
        button.configure(text="Capture Packets")
        button.bind("<Button-1>", self.buttonClickCallback)
        button.grid(row=1, column=6, sticky='w')
        Label(frame2, text=" ").grid(row=1, column=7, sticky=W)  # Spacer
        
        # Button to cancel the packet capture
        cancelButton = Button(frame2)
        cancelButton.configure(text="Cancel")
        cancelButton.bind("<Button-1>", self.cancelButtonEvent)
        cancelButton.grid(row=1, column=8, sticky=W)
        
        #### Frame 3 Contents ####
        # Spacer
        Label(frame3, text="   ").grid(row=1, column=1, sticky=W)
        
        #### Frame 4 Contents ####
        # include a Scrollbar to connect to the Text where all the packets get printed
        scrollbar = Scrollbar(frame4)
        scrollbar.pack(side = RIGHT, fill = Y)
        #scrollbar.pack(side=RIGHT, fill=Y)

        self.textArea = Text(frame4)
        self.textArea.configure(width=90, height=35, wrap = WORD, yscrollcommand = scrollbar.set)
        self.textArea.pack()
        scrollbar.config(command=self.textArea.yview)


    #Callback method activated when the left mouse key clicks the  "Capture
    # Packet" button
    def buttonClickCallback(self, event):
        self.host = self.textEntry.get()
        self.numPackets = self.numPackts.get()
        self.tc.getEntropyResult()
        
    def exitProgram(self, event=None):
        if tkMessageBox.askokcancel("Quit?", "Really quit?"):
            root.destroy()    
                
    def cancelButtonEvent(self, event):
        self.tc.killThread()

    def openFile(self):
        filenameforReading = askopenfilename()
        dataManager = EntropyDataManager(filenameforReading)
        newText = dataManager.openFile()
        # clear any current text and place loaded text
        self.textArea.delete(1.0, 'end')
        self.textArea.insert(1.0, newText)

    def saveFile(self):
        filenameforWriting = asksaveasfilename()
        dataManager = EntropyDataManager(filenameforWriting)
        saveText = self.textArea.get(1.0, 'end-1c')  # end-1c prevents final newline character from being saved to file
        dataManager.saveFile(saveText)
        
    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                self.textArea.insert(Tkinter.END, repr(msg) + "\n")
                print msg
            except Queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass
            
class ThreadedClient:
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master
        self.pc = PacketCapture()
        
        # Boolean to start/stop recieving entropy result
        self.inEntropyMode = False        

        # Create the queue
        self.queue = Queue.Queue(  )

        # Set up the GUI part
        self.gui = EntropyGUI(master, self.queue, self.endApplication, self)

        # Set up the thread to do asynchronous I/O
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )        
        
    def getEntropyResult(self):
        self.inEntropyMode = True
        print"My IP is " + str(self.gui.host) + " In getEntropyResult " + repr(self.inEntropyMode)
        
    # Kills thread when cancel button clicked in GUI
    # There's no way of killing thread from outside
    # Must create extended thread class that has the ability to
    # be terminated from outside the thread
    def killThread(self):
        pass
        
    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming(  )
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            self.master.destroy()
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            eResult = ""
            if self.inEntropyMode:
                ip = socket.gethostbyname(socket.gethostname())
                eResult = self.pc.capturePackets(ip, int(self.gui.numPackets))
            
            # yield control to GUI. May need to fine tune this pause
            time.sleep(rand.random(  ) * 1.5)
            
            if not eResult == "":
                self.queue.put("Entropy Result on " + self.gui.numPackets + " Packets: " + str(eResult))
                inEntropyMode = False

    def endApplication(self):
        self.running = 0
        self.inEntropyMode = False

rand = random.Random(  )
root = Tkinter.Tk(  )

client = ThreadedClient(root)
root.mainloop(  )
