import sys
from java.util import Date
from java.text import SimpleDateFormat


def getOpt(base, option):
    if option.startswith(base):
        return option.split(base)[-1]
    return None

def getOptBoolean(base, option):
    return option.startswith(base)

def getVersion(fileName):
    fp = open(fileName)
    rl = fp.readline()
    fp.close()
    return rl

class Color:

    GREEN = '\033[1;32m'
    RED = '\033[1;31m'

    def _baseMsg(self, color, text):
        return "%s%s\033[1;m" % ( color, text)

    def green(self, msg):
        return self._baseMsg(self.GREEN, msg)

    def red(self, msg):
        return self._baseMsg(self.RED, msg)

class Log:

    def baseMessage(self, message, level):
        curDate = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS").format(Date())
        message = "%s - [%s] - %s" % ( Date().toString(), level, message)
        return message
    
    def write(self, message, level):
        """ must be overrided """
        pass

    def debug(self,message):
        self.write(message, 'DEBUG')

    def info(self,message):
        self.write(message, 'INFO')

    def warn(self,message):
        self.write(message, 'WARN')

    def error(self,message):
        self.write(message, 'ERROR')


class FileLogger(Log):
    def __init__(self, filename):
        self.fp = open(filename, 'w+')
        sys.stdout = self.fp

    def write(self,message, level):
        message = self.baseMessage(message, level)
        self.fp.write(message)
        self.fp.flush()

    def destroy(self):
        self.fp.close()

class StdoutLogger(Log):
    def __init__(self):
        pass

    def write(self, message, level):
        print self.baseMessage(message, level)
