import socket
import os
import struct
from ctypes import *
# Filters raw packet captures, converts data into binary form,
# and performs entropy analysis on binary packet data.

class PacketAnalyzer:
    def __init__(self):
        self.entropyResult = 0;
    
    # Converts a list of raw packet captures into a filtered
    # list of packet captures.
    # rawPackets is a list of raw packet captures
    # Returns the filtered form of the list
    def filterPackets(self, rawPackets):
        print"Analyzing packets"
    
    # Converts a list of filtered packet data into binary
    # filteredPackets is a list of filtered packet data
    # Returns the binary form of the list
    def convertToBinary(self, filteredPackets):
        pass
    
    # Analyzes the binary form of the packet data using
    # Shannon's Entropoy algorithm
    def entropyAnalysis(self, binaryPacketData):
        pass