# Packet object, which stores packet data


class Packet:
    def __init__(self, sender, packetHead, packetBody, packetSize):
        self.sender = sender
        self.packetData = sender
        self.packetHead = packetHead
        self.packetBody = packetBody
        self.packetSize = packetSize

    def __str__(self):
        return "Packet Sender: " + self.sender + "; Packet Head: " + self.packetHead + "; Packet Body: " + self.packetBody + "; Packet Size: " + str(self.packetSize)
