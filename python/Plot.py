
from OpenGL.GL import *
import math

def mymod (x, y):
    """
    (float, float) -> float
    """
    m = x % y
    if m < y - m:
        return m
    else:
        return m - y

def formatizeInt (n, zero):
    if n == 0:
        o = 0
    else:
        o = int (round (math.log (abs (n), 10), 6))
    if zero:
        return ("%0%d" % o)
    else:
        return ("%%d" % o)

class Line:
    def __init__ (self, line, color):
        """
        ('a, 'b) list -> Line
        """
        x, y = zip (*line)
        self.x = x
        self.y = y
        self.color = color

    def each (self):
        """
        () -> ('a, 'b) list
        """
        return zip (self.x, self.y)

    def maxmin_x (self):
        """
        () -> ('a, 'b)
        """
        return (max (self.x), min (self.x))

    def maxmin_y (self):
        """
        () -> ('a, 'b)
        """
        return (max (self.y), min (self.y))

class DrawGraph:
    def __init__ (self,
                  mi_x, ma_x, mi_y, ma_y,
                  limi_x, lima_x, limi_y, lima_y,
                  draw_func):
        """
        (DrawGraph,
         float, float, float, float,
         float, float, float, float,
         (Graph, float, float, float, float) -> ()
        ) -> ()
        """

        self.mi_x = mi_x
        self.ma_x = ma_x
        self.mi_y = mi_y
        self.ma_y = ma_y
        self.limi_x = limi_x
        self.lima_x = lima_x
        self.limi_y = limi_y
        self.lima_y = lima_y

        # max and min drawn
        def set_range (limit, m):
            return m if limit == None else limit

        self.drma_x = set_range (self.lima_x, self.ma_x)
        self.drmi_x = set_range (self.limi_x, self.mi_x)
        self.drma_y = set_range (self.lima_y, self.ma_y)
        self.drmi_y = set_range (self.limi_y, self.mi_y)

        self.rate_x = 1.0 / (self.drma_x - self.drmi_x)
        self.rate_y = 1.0 / (self.drma_y - self.drmi_y)

        self.draw_func = draw_func

    def drawGrid2 (self, step_x, step_y):
        """
        (DrawGraph, float, float) -> ()
        """

        glBegin (GL_LINE_STRIP)
        glVertex2f (-0.5, -0.5)
        glVertex2f ( 0.5, -0.5)
        glVertex2f ( 0.5,  0.5)
        glVertex2f (-0.5,  0.5)
        glVertex2f (-0.5, -0.5)
        glEnd ()

        glBegin (GL_LINES)

        rinv = self.rate_x
        t = mymod (self.drmi_x, step_x)
        for x in range (0, int (1.0 / (step_x * rinv)) + 1):
            glVertex2f ((x * step_x - t) * rinv - 0.5, -0.5)
            glVertex2f ((x * step_x - t) * rinv - 0.5,  0.5)

        rinv = self.rate_y
        t = mymod (self.drmi_y, step_y)
        for y in range (0, int (1.0 / (step_y * rinv))):
            glVertex2f (-0.5, 0.5 - (y * step_y - t) * rinv)
            glVertex2f ( 0.5, 0.5 - (y * step_y - t) * rinv)

        glEnd ()
            
    # end drawGrid2
    def drawAxis2 (self, chars, size, step_x, fmt_x, step_y, fmt_y):
        """
        (DrawGraph, String, float, string, float, string) -> ()
        """
        offset = - 0.5 - size
        scale = 1.0 / (1.0 + size)

        glScalef (scale, scale, 1.0)

        r = self.drma_x - self.drmi_x
        t = self.drmi_x - mymod (self.drmi_x, step_x)
        for x in range (0, int (r / step_x) + 1):
            v = t + x * step_x
            glPushMatrix ()
            glTranslatef ((v - self.drmi_x) / r - 0.5, offset, 0.0)
            glScalef (size, size, 1.0)
            chars.draw (fmt_x%v)
            glPopMatrix ()

        rinv = self.rate_y
        t = self.drmi_y - mymod (self.drmi_y, step_y)
        for y in range (0, int (1.0 / (step_y * rinv)) + 1):
            v = t + y * step_y
            glPushMatrix ()
            glTranslatef (offset, (v - self.drmi_y) * rinv - 0.5, 0.0)
            glScalef (size, size, 1.0)
            chars.draw (fmt_y%v)
            glPopMatrix ()
    # end drawAxis2
                
    def drawGrid (self, div_x, div_y):
        """
        (DrawGraph, int, int) -> ()
        """
        
        for x in range (0, div_x + 1):
            glBegin (GL_LINES)
            glVertex2f (1.0 * x / div_x - 0.5, -0.5)
            glVertex2f (1.0 * x / div_x - 0.5,  0.5)
            glEnd ()
        for y in range (0, div_y + 1):
            glBegin (GL_LINES)
            glVertex2f (-0.5, 1.0 * y / div_y - 0.5)
            glVertex2f ( 0.5, 1.0 * y / div_y - 0.5)
            glEnd ()
    # end def drawGrid


    def drawAxis (self, chars, size,
                  div_x, fmt_x,
                  div_y, fmt_y):
        """
        (DrawGraph, String, int, int, float) -> ()
        """
        offset = - 0.5 - size
        scale = 1.0 / (1.0 + size)
       
        glScalef (scale, scale, 1.0)

        for x in range (0, div_x + 1):
            v = self.drmi_x + 1.0 * x / div_x / self.rate_x
            glPushMatrix ()
            glTranslatef (1.0 * x / div_x - 0.5, offset, 0.0)
            glScalef (size, size, 1.0)
            chars.draw (fmt_x%v)
            glPopMatrix ()
        for y in range (0, div_y + 1):
            v = self.drmi_y + 1.0 * y / div_y / self.rate_y
            glPushMatrix ()
            glTranslatef (offset, 1.0 * y / div_y - 0.5, 0.0)
            glScalef (size, size, 1.0)
            chars.draw (fmt_y%v)
            glPopMatrix ()

    # end def drawAxis
    
    def drawLabel (self, chars, size, x, y):
        """
        (DrawGraph, String, string, string, float) -> ()
        """
        offset = -0.5 - size * 0.5
        scale = 1.0 / (1.0 + size * 2.0)
        
        glPushMatrix ()
        glTranslatef (0.0, offset, 0.0)
        glScalef (size, size, 1.0)
        chars.draw (x)
        glPopMatrix ()
        
        glPushMatrix ()
        glTranslatef (offset, 0.0, 0.0)
        glScalef (size, size, 1.0)
        glRotatef (90.0, 0.0, 0.0, 1.0)
        chars.draw (y)
        glPopMatrix ()
        
        glScalef (scale, scale, 1.0)
        
    # end def drawLabel

    def drawTitle (self, chars, title, size):
        """
        (DrawGraph, String, string, float, float) -> ()
        """
        offset = -0.5 - size * 0.5
        scale = 1.0 / (1.0 + size * 2.0)

        glPushMatrix ()
        glTranslatef (0.0, offset, 0.0)
        glScalef (size, size, 1.0)
        chars.draw (title)
        glPopMatrix ()

        glScalef (scale, scale, 1.0)
        
    # end def drawTitle

    def draw (self):
        self.draw_func (self.drmi_x, self.drma_x, self.rate_x,
                        self.drmi_y, self.drma_y, self.rate_y)
    
# end class DrawGraph
    
class DiscreteGraph:
    ma_x = None
    mi_x = None
    ma_y = None
    mi_y = None
  
    def __init__ (self, min_x, max_x, min_y, max_y):
        """
        (DiscreteGraph, 'a, 'a, 'b, 'b) -> DiscreteGraph
        """
        # graph max and min
        self.lima_x = max_x
        self.limi_x = min_x
        self.lima_y = max_y
        self.limi_y = min_y

        # data
        self.lines = []

    def append (self, line):
        """
        (DiscreteGraph, Line) -> ()
        """
        ma_x, mi_x = line.maxmin_x ()
        ma_y, mi_y = line.maxmin_y ()

        # max and min for each x and y
        if len (self.lines) == 0:
            self.ma_x = ma_x
            self.mi_x = mi_x
            self.ma_y = ma_y
            self.mi_y = mi_y
        else:
            if ma_x > self.ma_x: self.ma_x = ma_x
            if mi_x < self.mi_x: self.mi_x = mi_x
            if ma_y > self.ma_y: self.ma_y = ma_y
            if mi_y < self.mi_y: self.mi_y = mi_y

        self.lines.append (line)

    def make (self):
        """
        DiscreteGraph -> DrawGraph
        """
        return DrawGraph (
            self.mi_x, self.ma_x, self.mi_y, self.ma_y,
            self.limi_x, self.lima_x, self.limi_y, self.lima_y,
            self.draw
        )

    def draw (self, drmi_x, drma_x, rate_x, drmi_y, drma_y, rate_y):
        """
        (DiscreteGraph, String) -> ()
        """

        if len (self.lines) == 0:
            raise Error

        def rangize (points):
            def cross (p1, p2):
                x1, y1 = p1
                x2, y2 = p2
                mi_x, ma_x = (x1, x2) if x1 < x2 else (x2, x1)
                mi_y, ma_y = (y1, y2) if y1 < y2 else (y2, y1)
                mi_x = max (mi_x, drmi_x)
                ma_x = min (ma_x, drma_x)
                mi_y = max (mi_y, drmi_y)
                ma_y = min (ma_y, drma_y)
                
                def crossX (y):
                    if y1 == y2:
                        return None
                    else:
                        return ((x2-x1) * (y-y1) + (y2-y1) * x1) / (y2-y1)
                
                def crossY (x):
                    if x1 == x2:
                        return None
                    else:
                        return ((x2-x1) * y1 + (y2-y1) * (x-x1)) / (x2-x1)

                ux = crossX (drma_y)
                dx = crossX (drmi_y)
                ry = crossY (drma_x)
                ly = crossY (drmi_x)

                c = [(ux, drma_y) if ux and mi_x < ux < ma_x else None,
                     (dx, drmi_y) if dx and mi_x < dx < ma_x else None,
                     (drma_x, ry) if ry and mi_y < ry < ma_y else None,
                     (drmi_x, ly) if ly and mi_y < ly < ma_y else None]
                c = filter (lambda i:i, c)

                return c
            # end cross
            
            def f (lastin, p1, t):
                try:
                    p2 = t.pop (0)
                except: return []

                c = cross (p1, p2)

                if len (c) == 0:
                    if lastin: # in -> in
                        return [p2] + f (True, p2, t)
                    else: # out -> out
                        return f (False, p2, t)
                if len (c) == 1:
                    if lastin: # in -> out
                        return [c[0]] + f (False, p2, t)
                    else: # out -> in
                        return [c[0], p2] + f (True, p2, t)
                else: # out -> in -> out
                    x1, y1 = p1
                    def key (p):
                        x, y = p
                        return (x - x1) ** 2 + (y - y1) ** 2
                    c.sort (key=key)
                    return [c[0], c[1]] + f (False, p2, t)
                    
            try:
                p1 = points.pop (0)
                x1, y1 = p1
            except IndexError: return []
            if drmi_x <= x1 <= drma_x and drmi_y <= y1 <= drma_y:
                return [p1] + f (True, p1, points)
            else:
                return f (False, p1, points)
        # end rangize
        
        # draw lines
        for line in self.lines:
            glColor3f (*line.color)
            glBegin (GL_LINE_STRIP)
            for x, y in rangize (line.each ()):
                glVertex2f ((x - drmi_x) * rate_x - 0.5,
                            0.5 - (y - drmi_y) * rate_y)
            glEnd ()
    # end draw

# end class DiscreteGraph

