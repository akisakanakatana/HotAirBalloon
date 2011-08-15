
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

#  !"#$%&'()*+,-./0123456789:;<=>?@
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
# [\]^_`
# abcdefghijklmnopqrstuvwxyz{|}~
def makeAll ():
    a = range (32, 127) # 95 chars
    a = [chr (x) for x in a]
    return str.join ("", a)

class char:
    
    unit = 1.0 / 128
    
    def __init__ (self, disp, c):
        self.disp = disp
        
        start = (c - ord (" ")) * self.unit
        end = start + self.unit * 0.95

        glNewList (disp, GL_COMPILE)
        glBegin (GL_QUADS)
        
        glTexCoord2f (start, 0.0)
        glVertex3f (-0.25, -0.5, 0.0)
        glTexCoord2f (end, 0.0)
        glVertex3f ( 0.25, -0.5, 0.0)
        glTexCoord2f (end, 1.0)
        glVertex3f ( 0.25,  0.5, 0.0)
        glTexCoord2f (start, 1.0)
        glVertex3f (-0.25,  0.5, 0.0)
        
        glEnd ()
        glEndList ()

    def draw (self):
        glCallList (self.disp)

# end class char

class string:

    def __init__ (self, disp):
        if len (disp) != 95: raise Error
        disp_char = zip (disp, range (32, 127)) # " " - "~"+1
        self.chars = [char (d,c) for d,c in disp_char]

    def draw (self, string, **opt):
        glPushMatrix ()
        if not (opt.has_key ("fix") and opt["fix"]) :
            glTranslatef (-0.25 * (len (string) - 1), 0.0, 0.0)
        for c in string:
            self.chars[ord(c)-32].draw ()
            glTranslatef (0.5, 0.0, 0.0)
        glPopMatrix ()

    def drawLines (self, strings, **opt):
        glPushMatrix ()
        for s in strings:
            self.draw (s, **opt)
            glTranslatef (0.0, -1.0, 0.0)
        glPopMatrix ()
         
# end class string
