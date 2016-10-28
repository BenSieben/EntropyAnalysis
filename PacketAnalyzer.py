import socket
import os
import struct
from ctypes import *
# Converts data into binary form
# and performs entropy analysis on packet data.

class PacketAnalyzer:
    def __init__(self):
        self.entropyResult = 0;
        
    # Converts a list of packet payloads into a list of binarys
    # Returns the binary form of the list
    def convertToBinary(self, packets):
        # Convert a character into it's ascii numeric value
        asciiValue = ord("A")
        # Convert decimal number into binary
        binary = format(asciiValue, '08b')
        
        print "binary of A is" + str(binary)
        print "Converting each packet into binary string\n"

    
    # Shannon's Entropoy algorithm
    def entropyAnalysis(self, binaryPacketData):
        print "Performing Entropy analysis\n"