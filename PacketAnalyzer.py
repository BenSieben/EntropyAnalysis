import socket

import os

import struct

from ctypes import *

# Converts data into binary form

# and performs entropy analysis on packet data.



class PacketAnalyzer:

    def __init__(self):

        self.entropyResult = 0

    

    # Converts a list of filtered packet data into binary form

    # filteredPackets is a list of filtered packet data

    # Returns the binary form of the list

    def convertToBinary(self, filteredPackets):

        binaryPackets = []

        for packet in filteredPackets:  # examine each packet in the filtered packets list to convert each into binary

            binaryPacket = ''

            for packetChar in packet:

                packetCharValue = ord(packetChar)  # get ASCII value of each character

                packetCharValueBinary = self.convertNumberToBinary(packetCharValue, 8) # convert value into binary byte

                binaryPacket += packetCharValueBinary  # add binary byte value of character to binary packet string

            binaryPackets.append(binaryPacket)

        return binaryPackets



    # Converts a given (positive or zero) number into binary

    # num = number to convert to binary

    # numBits = how many bits to use to store the result

    # Note that if numBits cannot hold the value of num completely, the result will not be correct

    def convertNumberToBinary(self, num, numBits):

        byteString = ''  # start off byte string as all empty (the for loop below will build the bits)

        numRemaining = num

        for i in range(numBits, 0, -1): # go from numBits through 0 in steps of -1 (going backwards)

            if numRemaining >= 2 ** (i - 1):  # check if numRemaining >= 2^i (i.e., the value for this bit position

                byteString += '1'  # put 1 as bit if numRemaining was big enough to fill the bit

                numRemaining -= 2 ** (i - 1)  # decrement numReamining to subtract this filled bit's value

            else:

                byteString += '0'  # put 0 as bit if it numRemaining was too small

        return byteString



    # Shannon's Entropy algorithm

    def entropyAnalysis(self, binaryPacketData):

        print "Performing Entropy analysis\n"