from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color,Rectangle


class BorderedLabel(Label):
    def __init__(self,**kwargs):
        super(BorderedLabel,self).__init__(**kwargs)
        with self.canvas.before:
            Color(1,0,0,1)
            self.rect=Rectangle(size=self.size,pos=self.pos)
        self.bind(pos=self.update_rect,size=self.update_rect)

    def update_rect(self,*args):
        self.rect.pos=self.pos
        self.rect.size=self.size

