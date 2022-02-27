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
            for i in range(7): self.lines.append(Line())

    def updateLines(self):
        spacing = self.width * 0.1
        initX = self.width/2 - 3 * spacing
        for i in range(7): 
            x = int(initX + i * spacing)
            self.lines[i].points = [x,0,x,self.height]
                

class GalaxyApp(App):
    pass

GalaxyApp().run()