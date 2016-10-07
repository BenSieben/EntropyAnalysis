import socket
import os

# A Class to capture network packets
# Captured raw packets are stored as strings in the self.packets list
# Much of the packet capture code is from the book Black Hat Python by 
# Justin Seitz. We wrapped the code in a class to be used by our EntropytGUI
# class.

class PacketCapture:
    def __init__(self):
        self.packets = []
        self.ipAddr = ""
        
    def capturePackets(self, ipAddr):
        self.ipAddr = ipAddr

        # create a raw socket and bind it to the public interface
        if os.name == "nt":
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

        sniffer.bind((self.ipAddr, 0))

        # we want the IP headers included in the capture
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # if we're on Windows we need to send an IOCTL
        # to setup promiscuous mode
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        # read in a single packet
        rawPacket = sniffer.recvfrom(65565)
        
        # add packet to list
        self.packets.append(str(rawPacket))

        # if we're on Windows turn off promiscuous mode
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            
    def getPacketList(self):
        return self.packets
