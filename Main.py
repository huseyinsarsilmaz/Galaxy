from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

class MainWidget(Widget):
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.perspectivePointX = NumericProperty(0)
        self.perspectivePointY = NumericProperty(0)
        

    def on_size(self,*args):
        # self.perspectivePointX = self.width/2
        # self.perspectivePointY = self.height * 0.75
        pass

    def on_perspectivePointX(self,widget,value):
        pass

    def on_perspectivePointY(self,widget,value):
        pass

class GalaxyApp(App):
    pass

GalaxyApp().run()