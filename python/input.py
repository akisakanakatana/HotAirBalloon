
class Input:
    def __init__ (self):
        self.head = []
        self.tail = []
        self.last_head = []
        self.last_tail = []

    def before (self):
        if self.head:
            self.tail = [self.head.pop ()] + self.tail

    def fore (self):
        if self.tail:
            self.head.append (self.tail.pop (0))

    def move (self, i):
        if i < 0:
            self.before ()
            self.move (i + 1)
        elif i > 0:
            self.fore ()
            self.move (i - 1)

    def clear (self):
        self.head = []
        self.tail = []

    def begin (self):
        self.tail = self.head + self.tail
        self.head = []

    def end (self):
        self.head = self.head + self.tail
        self.tail = []
        
    def insert (self, c):
        self.head.append (c)

    def delete (self):
        if self.tail:
            self.tail.pop (0)

    def backspace (self):
        if self.head:
            self.head.pop ()

    def kill (self):
        self.tail = []
        
    def position (self):
        return len (self.head)

    def readLine (self, string):
        self.head = self.head + [c for c in string]

    def submit (self):
        s = self.text ()
        self.last_head.append (self.head)
        self.clear ()
        return s

    def pre (self):
        if self.last_head:
            last = self.last_head.pop ()
            self.clear ()
            self.head = last
            self.last_tail.insert (0, last)

    def nex (self):
        if self.last_tail:
            last = self.last_tail.pop (0)
            self.clear ()
            self.head = last
            self.last_head.append (last)
        else:
            self.clear ()
        
    def text (self):
        return str.join ("", self.head) + str.join ("", self.tail)
    
    def __str__ (self):
        return str.join ("", self.head) + "|" + str.join ("", self.tail)
