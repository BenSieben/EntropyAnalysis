import struct

# Filters raw packet captures, converts data into binary form,
# and performs entropy analysis on binary packet data.

class PacketAnalyzer:
    def __init__(self):
        pass
    
    # Converts a list of raw packet captures into a filtered
    # list of packet captures.
    # rawPackets is a list of raw packet captures
    # Returns the filitered form of the list
    def filterPackets(self, rawPackets):
        pass
    
    # Converts a list of filtered packet data into binary
    # filteredPackets is a list of filtered packet data
    # Returns the binary form of the list
    def convertToBinary(self, filterdPackets):
        pass
    
    # Analyzes the binary form of the packet data using
    # Shannon's Entropoy algorithm
    def entropyAnalysis(self, binaryPacketData):
        pass