# Define a Python class for your lexer with members and methods
from src.generated.kern.kernLexer import kernLexer


class KernLexerWithSpines(kernLexer):
    textSpines = []  # Use a Python list to store the boolean values
    currentSpine = 0  # Initialize the current spine

    # Define a constructor for the lexer
    def __init__(self, input):
        super().__init__(input)

    # Define a method to check if you are in a text spine
    def inTextSpine(self):
        if self.currentSpine >= len(self.textSpines):
            return False
        else:
            return self.textSpines[self.currentSpine]

    # Define a method to increment the spine
    def incSpine(self):
        self.currentSpine += 1
        if self.inTextSpine():
            self.mode(self.FREE_TEXT)
        else:
            self.mode(0)

    # Define a method to split the spine
    def splitSpine(self):
        self.textSpines.insert(self.currentSpine, self.inTextSpine())

    # Define a method to join the spine
    def joinSpine(self):
        self.textSpines.pop(self.currentSpine)

    # Define a method to reset the mode
    def resetMode(self):
        self.mode(0)

    # Define a method to reset the spine and mode
    def resetSpineAndMode(self):
        self.resetMode()
        self.currentSpine = -1
        self.incSpine()

    # Define a method to add a music spine
    def addMusicSpine(self):
        self.textSpines.append(False)

    # Define a method to add a text spine
    def addTextSpine(self):
        self.textSpines.append(True)

    ## Revisar este comportamiento
    def terminateSpine(self):
        self.textSpines.pop(self.currentSpine)

    def addSpine(self):
        self.textSpines.append(False)

