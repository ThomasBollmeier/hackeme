import os

class Output(object):
    
    def writeln(self, text):
        self.write(text + os.linesep)
        
    def write(self, text):
        print(text)