from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,Clock
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.perspectivePointX = NumericProperty(0)
        self.perspectivePointY = NumericProperty(0)
        self.verticalLines = []
        self.horizontalLines = []
        self.offset = 1
        self.createVerticalLines()
        self.createHorizontalLines()
        Clock.schedule_interval(self.update,1/60)
        

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
    
    def updateHorizontalLines(self):
        minX = self.width/2 - 4.5 * self.width * 0.25
        maxX = self.width/2 + 4.5 * self.width * 0.25
        for i in range(8): 
            y = i*0.1*self.height-self.offset
            x1,y1 = self.perspective(minX,y)
            x2,y2 = self.perspective(maxX,y)
            self.horizontalLines[i].points = [x1,y1,x2,y2]

    def updateVerticalLines(self):
        spacing = self.width * 0.25
        initX = self.width/2 - 4.5 * spacing
        for i in range(10): 
            x1,y1 = self.perspective(initX + i * spacing,0)
            x2,y2 = self.perspective(initX + i * spacing,self.height)
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
        self.offset += 1 * dt * 60
        if(self.offset >= 0.1 * self.height) : self.offset -= 0.1 * self.height


class GalaxyApp(App):
    pass

GalaxyApp().run()