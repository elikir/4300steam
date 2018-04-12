

class MessageAPI(object):

    def sendMessage(self, fromUSer, toUser, content):
        return NotImplementedError("Not implemented")

    def getMessageContents(self, messageID):
        return NotImplementedError("Not implemented")

    def getMessageTo(self, messageID):
        return NotImplementedError("Not implemented")

    def getMessageFrom(self, messageID):
        return NotImplementedError("Not implemented")