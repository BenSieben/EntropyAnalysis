from Tkinter import *
from PacketCapture import PacketCapture

# Packet Capture Program
# This GUI uses our PacketCapture class


class EntropyGUI:
    def __init__(self):
        
        self.pc = PacketCapture()

        root = Tk()  # Create Window

        root.title("Packet Capture")

        Label(root, text="This program will capture a single packet and display the raw data below").pack()

        Label(root, text="There needs to be network traffic so open a command prompt and execute a ping").pack()

        Label(root, text="Note that this program needs to be run with administrator privileges").pack()
        
        Label(root, text="").pack()  # Spacer 
        Label(root, text="Enter Host IP").pack()
        
        # Entrybox to get the host IP
        self.ipAddr = StringVar()
        self.textEntry = Entry(root, textvariable = self.ipAddr)
        self.textEntry.pack()
        
        # Enter number of packets to capture
        Label(root, text="Enter number of packets to capture").pack()
        self.numPackts = StringVar()
        self.numPacktsEntry = Entry(root, textvariable = self.numPackts)
        self.numPacktsEntry.pack()
        
        # Button to trigger the packet capture
        button = Button(root)
        button.configure(text="Capture Packet")
        button.bind("<Button-1>", self.buttonClickCallback)
        button.pack()
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
        host = self.ipAddr.get()
        numPackets = self.numPackts.get()
        
        if numPackets == "":
            numPackets = "1" # default value
        
        # Make sure an IP address was entered
        # This validity check must be improved
        if host == "":
            self.textArea.insert(INSERT, "You must enter a valid IP address\n")
            return
        else:
            self.pc.capturePackets(host, int(numPackets))
            myList = self.pc.getPacketList()
            for p in myList:
                self.textArea.insert(END, p)       

EntropyGUI()  # Create the GUI
