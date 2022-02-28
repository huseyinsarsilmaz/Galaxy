import random
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,Clock,ObjectProperty,StringProperty
from kivy.graphics.vertex_instructions import Line,Quad,Triangle
from kivy.graphics.context_instructions import Color
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy import platform
from kivy.lang import Builder
from kivy.core.audio import SoundLoader

Builder.load_file("menu.kv")
class MainWidget(RelativeLayout):
    menuTitle = StringProperty("G   A   L   A   X   Y")
    buttonTitle = StringProperty("START")
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
        self.yLoop = 0
        self.ship = None
        self.shipCoordinates = []
        self.stateGameOver = False
        self.StateGameStart = False
        self.soundBegin = SoundLoader.load("audio/begin.wav")
        self.soundgalaxy = SoundLoader.load("audio/galaxy.wav")
        self.soundImpact = SoundLoader.load("audio/gameover_impact.wav")
        self.soundVoice = SoundLoader.load("audio/gameover_voice.wav")
        self.soundMusic = SoundLoader.load("audio/music1.wav")
        self.soundRestart= SoundLoader.load("audio/restart.wav")

        self.soundBegin.volume = 1
        self.soundgalaxy.volume = .25
        self.soundImpact.volume = .6
        self.soundVoice.volume = .25
        self.soundMusic.volume = .25
        self.soundRestart.volume = .25
        
        self.menuWidget = ObjectProperty()
        self.createVerticalLines()
        self.createHorizontalLines()
        self.createTiles()
        self.createShip()
        for i in range(8): self.tileCoordinates.append((0,i))
        self.generateTileCoordinates()
        if(platform in ("linux","win","macosx")):
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update,1/60)
        self.soundgalaxy.play()

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

    def createShip(self):
        with self.canvas:
            Color(0,0,0)
            self.ship = Triangle()

    def updateShip(self):
        centerX = self.width/2
        baseY = self.height * 0.04
        shipWidth = self.width * 0.1 / 2
        x1,y1 = self.perspective(centerX - shipWidth,baseY)
        x2,y2 = self.perspective(centerX,baseY + self.height * 0.035) 
        x3,y3 = self.perspective(centerX + shipWidth,baseY)
        self.shipCoordinates.append((centerX - shipWidth,baseY))
        self.shipCoordinates.append((centerX,baseY + self.height * 0.035))
        self.shipCoordinates.append((centerX + shipWidth,baseY))
        self.ship.points = [x1,y1,x2,y2,x3,y3]     
    
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
            elif( lastX >= 4): r = 2
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
                
    def checkShipCollision(self):
        for i in range(0,len(self.tileCoordinates)):
            x,y = self.tileCoordinates[i]
            if(y > self.yLoop +1): return False
            if(self.checkShipCollisionTile(x,y)): return True
        return False
    
    def checkShipCollisionTile(self,x,y):
        minX,minY = self.getTileCoordinates(x,y)
        maxX,maxY = self.getTileCoordinates(x+1,y+1)
        for i in range(3):
            px,py = self.shipCoordinates[i]
            if( minX <= px <= maxX  and minY <= py <= maxY ): return True
        return False
    
    def update(self,dt):
        self.updateVerticalLines()
        self.updateHorizontalLines()
        self.updateTiles()
        self.updateShip()
        if(not self.stateGameOver and self.StateGameStart):
            self.offsetY += 0.5 * self.height * dt * 60 / 100
            self.offsetX += 0.45 * self.width * self.speedX * dt * 60 /100
            while(self.offsetY >= 0.1 * self.height): 
                self.offsetY -= 0.1 * self.height
                self.yLoop +=1
                self.generateTileCoordinates()
        if (not self.checkShipCollision() and not self.stateGameOver): 
            self.stateGameOver = True
            self.soundMusic.stop()
            self.soundImpact.play()
            Clock.schedule_once(self.gameOverSound,1)
            self.menuTitle = "G  A  M  E    O  V  E  R"
            self.buttonTitle = "RESTART"
            self.menuWidget.opacity = 1

    def gameOverSound(self,dt): self.soundVoice.play()
    
    def on_touch_down(self, touch):
        if(not self.stateGameOver and self.StateGameStart):
            if(touch.x < self.width/2): self.speedX = 5
            else: self.speedX = -5
        return super(MainWidget,self).on_touch_down(touch)

    def on_touch_up(self, touch): self.speedX = 0

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if (keycode[1] == 'left' or keycode[1] == 'a') : self.speedX = 5
        elif (keycode[1] == 'right' or keycode[1] == 'd'): self.speedX = -5
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.speedX = 0

    def onMenuButtonPressed(self): 
        if(self.stateGameOver): self.soundRestart.play()
        else: self.soundBegin.play()
        self.soundMusic.play()
        self.resetGame()
        self.StateGameStart = True
        self.menuWidget.opacity = 0
        

    def resetGame(self):
        self.offsetY = 0
        self.offsetX = 0
        self.speedX = 0
        self.yLoop = 0
        self.tileCoordinates = []
        for i in range(8): self.tileCoordinates.append((0,i))
        self.generateTileCoordinates()
        self.stateGameOver = False


class GalaxyApp(App):
    pass

GalaxyApp().run()