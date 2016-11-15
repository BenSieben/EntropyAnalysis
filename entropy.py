from Tkinter import *
from PacketCapture import PacketCapture
from EntropyDataManager import EntropyDataManager
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
import socket
import threading

# Packet Capture Program
# This GUI uses our PacketCapture class


class GUIThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		print "Running"

class EntropyGUI:
    def __init__(self):
        
        self.pc = PacketCapture()        
        root = Tk()  # Create Window
        self.mt = GUIThread()
        self._running = True
        root.title("Packet Capture")

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

        Label(root, text="This program will capture a packet/s and display the raw data below").pack()

        Label(root, text="There needs to be network traffic so open a command prompt and execute a ping").pack()

        Label(root, text="Note that this program needs to be run with administrator privileges").pack()
        
        Label(root, text="").pack()  # Spacer 
        Label(root, text="Enter Host IP").pack()
        
        # Entrybox to get the host IP
        self.hostIP = StringVar()
        ip = socket.gethostbyname(socket.gethostname())        
        self.textEntry = Entry(root, textvariable = self.hostIP)
        self.textEntry.insert(END, ip) #enter host IP in text entry box
        self.textEntry.pack()
        
        # Enter number of packets to capture
        Label(root, text="Enter number of packets to capture").pack()
        self.numPackts = StringVar()
        self.numPacktsEntry = Entry(root, textvariable = self.numPackts)
        self.numPacktsEntry.pack()
        
        # Entropy Result
        Label(root, text="Entropy Result").pack()
        self.entropyResult = StringVar()
        self.entropyResultEntry = Entry(root, textvariable = self.entropyResult)
        self.entropyResultEntry.pack()

        
        # Button to trigger the packet capture
        button = Button(root)
        button.configure(text="Capture Packet")
        button.bind("<Button-1>", self.buttonClickCallback)
        button.pack()
        Label(root, text="").pack()  # Spacer   


        # Button to cancel the packet capture
        cancel = Button(root)
        cancel.configure(text="Cancel")
        cancel.bind("<Button-2>", self.cancelButtonClickCallback)
        cancel.pack()
        Label(root, text="").pack()  # Spacer      

        # include a Scrollbar to connect to the Text where all the packets get printed
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.textArea = Text(root)
        self.textArea.configure(width=150, height=40)
        self.textArea.pack()

        scrollbar.config(command=self.textArea.yview)

        root.mainloop() # main GUI  loop

    #Callback method activated when the left mouse key clicks the  "Capture
    # Packet" button
    def buttonClickCallback(self, event):
        host = self.hostIP.get()
        numPackets = self.numPackts.get()
        
        if numPackets == "":
            numPackets = "1" # default value
        
        # Make sure an IP address was entered
        # This validity check must be improved
        if host == "":
            self.textArea.insert(INSERT, "You must enter a valid IP address\n")
            return
        else:
        		
        		self.mt.start()
        		self.check_thread()
        		while self._running:
        			eResult = self.pc.capturePackets(host, int(numPackets))
        			self.entropyResultEntry.insert(0,eResult)
        			myList = self.pc.getPacketList()
        			for p in myList:
        				self.textArea.insert(END, p)

    def check_thread(self):
        # Still alive? Check again in half a second
        if self.mt.isAlive():
        		threading.Timer(500, self.check_thread)            
        else:
            print "Ended"
    def cancelButtonClickCallback(self, event):
    	self._running = False
    	self.mt.join()

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

EntropyGUI()  # Create the GUI


