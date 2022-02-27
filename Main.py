import random
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,Clock
from kivy.graphics.vertex_instructions import Line,Quad
from kivy.core.window import Window
from kivy import platform
class MainWidget(Widget):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.perspectivePointX = NumericProperty(0)
        self.perspectivePointY = NumericProperty(0)
        self.verticalLines = []
        self.horizontalLines = []
        self.offsetY = 0
        self.offsetX = 0
        self.speedX = 0
        self.tiles = []
        self.tileCoordinates = []
        self.createVerticalLines()
        self.createHorizontalLines()
        self.createTiles()
        self.generateTileCoordinates()
        self.yLoop = 0
        if(platform in ("linux","win","macosx")):
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update,1/60)

    def keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def on_size(self,*args):
        # self.perspectivePointX = self.width/2
        # self.perspectivePointY = self.height * 0.75
        # self.updateVerticalLines()
        # self.updateHorizontalLines()
        pass

    def on_perspectivePointX(self,widget,value):
        pass

    def on_perspectivePointY(self,widget,value):
        pass

    def createVerticalLines(self):
        with self.canvas:
            for i in range(10): self.verticalLines.append(Line())

    def createHorizontalLines(self):
        with self.canvas:
            for i in range(8): self.horizontalLines.append(Line())

    def createTiles(self):
        with self.canvas:
            for i in range(8): 
                self.tiles.append(Quad())
                
    def generateTileCoordinates(self):
        lastY = 0
        lastX = 0
        for i in range(len(self.tileCoordinates)-1,-1,-1):
            if (self.tileCoordinates[i][1] < self.yLoop): del self.tileCoordinates[i]
        if(len(self.tileCoordinates) > 0): 
            lastX = self.tileCoordinates[-1][0]
            lastY = self.tileCoordinates[-1][1] +1
        for i in range(len(self.tileCoordinates),8): 
            r = random.randint(0,2)
            if( lastX <= -4): r = 1
            elif( lastX > 5): r = 2
            if(r == 0):
                self.tileCoordinates.append((lastX,lastY))
                self.tileCoordinates.append((lastX,lastY+1))
                self.tileCoordinates.append((lastX,lastY+2))
            elif(r == 1):
                self.tileCoordinates.append((lastX,lastY))
                self.tileCoordinates.append((lastX+1,lastY))
                self.tileCoordinates.append((lastX+1,lastY+1))
            else:
                self.tileCoordinates.append((lastX,lastY))
                self.tileCoordinates.append((lastX-1,lastY))
                self.tileCoordinates.append((lastX-1,lastY+1))
            
            lastY += 1
            
    
    def updateTiles(self):
        for i in range(8):
            xmin,ymin = self.getTileCoordinates(self.tileCoordinates[i][0],self.tileCoordinates[i][1])
            xmax,ymax = self.getTileCoordinates(self.tileCoordinates[i][0]+1,self.tileCoordinates[i][1]+1)
            x1,y1 = self.perspective(xmin,ymin)
            x2,y2 = self.perspective(xmin,ymax)
            x3,y3 = self.perspective(xmax,ymax)
            x4,y4 = self.perspective(xmax,ymin)
            self.tiles[i].points = [x1,y1,x2,y2,x3,y3,x4,y4]

    def getLineXfromIndex(self,index):
        center = self.perspectivePointX
        spacing = self.width * 0.25
        offset = index - 0.5
        lineX = center + spacing*offset + self.offsetX
        return lineX

    def getLineYfromIndex(self,index):
        y = index*0.1*self.height-self.offsetY
        return y

    def getTileCoordinates(self,ix,iy):
        x = self.getLineXfromIndex(ix)
        y = self.getLineYfromIndex(iy-self.yLoop)
        return x,y
    
    def updateHorizontalLines(self):
        minX = self.getLineXfromIndex(-4)
        maxX = self.getLineXfromIndex(5)
        for i in range(8): 
            y = self.getLineYfromIndex(i)
            x1,y1 = self.perspective(minX,y)
            x2,y2 = self.perspective(maxX,y)
            self.horizontalLines[i].points = [x1,y1,x2,y2]

    def updateVerticalLines(self):
        # spacing = self.width * 0.25
        # initX = self.width/2 - 4.5 * spacing 
        for i in range(-4,6): 
            x = self.getLineXfromIndex(i)
            x1,y1 = self.perspective(x,0)
            x2,y2 = self.perspective(x,self.height)
            self.verticalLines[i].points = [x1,y1,x2,y2]

    def dummy(self,x,y): return x,y
    
    def perspective(self,x,y):
        y =  y * self.perspectivePointY / self.height
        diffX = x - self.perspectivePointX
        diffY = self.perspectivePointY -y
        factorY = diffY/self.perspectivePointY
        factorY = pow(factorY,4)
        x = self.perspectivePointX + diffX * factorY
        y = self.perspectivePointY - self.perspectivePointY * factorY
        return int(x) ,int(y)
                
    def update(self,dt):
        self.updateVerticalLines()
        self.updateHorizontalLines()
        self.updateTiles()
        self.offsetY += 4 * dt * 60
        self.offsetX += self.speedX * dt * 60
        if(self.offsetY >= 0.1 * self.height): 
            self.offsetY -= 0.1 * self.height
            self.yLoop +=1
            self.generateTileCoordinates()

    def on_touch_down(self, touch):
        if(touch.x < self.width/2): self.speedX = 5
        else: self.speedX = -5

    def on_touch_up(self, touch): self.speedX = 0

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if (keycode[1] == 'left' or keycode[1] == 'a') : self.speedX = 5
        elif (keycode[1] == 'right' or keycode[1] == 'd'): self.speedX = -5
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.speedX = 0


class GalaxyApp(App):
    pass

GalaxyApp().run()