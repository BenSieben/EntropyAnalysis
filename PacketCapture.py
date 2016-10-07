import socket
import os
import struct

# A Class to capture network packets
# Captured raw packets are stored as strings in the self.packets list

class PacketCapture:
    def __init__(self):
        self.packets = [""]
        self.ipAddr = ""
        self.numPackets = 0

    #Capture Packets and add to list    
    def capturePackets(self, ipAddr, numPackets):
        self.packets = [] # clear out the list
        self.ipAddr = ipAddr
        self.numPackets = numPackets

        # create a raw socket and bind it to the public interface
        if os.name == "nt":
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

        sniffer.bind((self.ipAddr, 0))

        # we want the IP headers included in the capture
        #sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # if we're on Windows we need to send an IOCTL
        # to setup promiscuous mode
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
            
        # read in a specified number of ethernet frames
        for i in range(self.numPackets):
            # Recieve packet
            rawPacket = sniffer.recvfrom(65565)
                        
            # add data part to list - data starts at byte 14 of ethernet frame
            self.packets.append(str(rawPacket[:14]) + "\n") #TODO - remove "\n"

        # if we're on Windows turn off promiscuous mode
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
                        
    def getPacketList(self):
        return self.packets
