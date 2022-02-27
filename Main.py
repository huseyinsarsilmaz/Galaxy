from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Line

class MainWidget(Widget):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.perspectivePointX = NumericProperty(0)
        self.perspectivePointY = NumericProperty(0)
        self.lines = []
        self.createVerticalLines()
        

    def on_size(self,*args):
        # self.perspectivePointX = self.width/2
        # self.perspectivePointY = self.height * 0.75
        self.updateLines()
        pass

    def on_perspectivePointX(self,widget,value):
        pass

    def on_perspectivePointY(self,widget,value):
        pass

    def createVerticalLines(self):
        with self.canvas:
            for i in range(10): self.lines.append(Line())

    def updateLines(self):
        spacing = self.width * 0.1
        initX = self.width/2 - 4.5 * spacing
        for i in range(10): 
            x1,y1 = self.perspective(initX + i * spacing,0)
            x2,y2 = self.perspective(initX + i * spacing,self.height)
            self.lines[i].points = [x1,y1,x2,y2]

    def dummy(self,x,y): return x,y
    
    def perspective(self,x,y):
        y =  y * self.perspectivePointY / self.height
        diffX = x - self.perspectivePointX
        diffY = self.perspectivePointY -y
        proportionY = diffY/self.perspectivePointY
        x = self.perspectivePointX + diffX * proportionY
        return int(x) ,int(y)
                

class GalaxyApp(App):
    pass

GalaxyApp().run()