from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
import Util.Util as util

class WebsiteMonitorPopup(object):
    _instance = None
    _popupOpened = False
    _popup = None
    _createLoginDetailsPopupOpened = False
    _createLoginDetailsPopup = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print("CREATING A NEW INSTANCE")
            cls._instance = cls.__new__(cls)
        return cls._instance
    
    @classmethod
    def showPopup(cls,title,content):
        if cls._popupOpened:
            cls._popup.dismiss()
            cls._popupOpened = False
        cls._popup = Popup(title=title,
                           content=Label(text=content),
                           size_hint=(None,None),
                           size=(400,400))
        cls._popup.open()

    @classmethod
    def showCreateLoginDetailsPopup(cls):
        if cls._createLoginDetailsPopupOpened:
            cls._createLoginDetailsPopup.dismiss()
            cls._createLoginDetailsPopupOpened = False
        mainLayout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),  
            padding=0,
            spacing=50 
        )
        applicationNameLayout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='50dp',
            spacing='10dp'
        )
        applicationNameLayout.add_widget(
            Label(
                text='Name of application/website',
                font_size='15sp',
                size_hint_x=0.4
            )
        )
        applicationNameTextInput = TextInput(
            text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        applicationNameLayout.add_widget(applicationNameTextInput)
        mainLayout.add_widget(applicationNameLayout)

                
        usernameLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        usernameLayout.add_widget(
            Label(text='Username', font_size='15sp', size_hint_x=0.4)
        )
        usernameTextInput = TextInput(
            text='', multiline=False, size_hint=(0.6, None), height='40dp'
        )
        usernameLayout.add_widget(usernameTextInput)
        mainLayout.add_widget(usernameLayout)

        passwordLengthLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp', spacing='10dp')
        passwordLengthLayout.add_widget(
            Label(text='Length of password', font_size='15sp', size_hint_x=0.4)
        )
        passwordSliderLayout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        passwordLengthLabel = Label(text='14', font_size='20sp', halign='center')
        passwordSliderLayout.add_widget(passwordLengthLabel)
        passwordLengthSlider = Slider(
            min=1, max=64, value=14, value_track=True, value_track_color=[1, 0, 0, 1]
        )
        passwordLengthSlider.bind(value=cls.onSliderValueChange)
        passwordSliderLayout.add_widget(passwordLengthSlider)
        passwordLengthLayout.add_widget(passwordSliderLayout)
        mainLayout.add_widget(passwordLengthLayout)

        symbolLayout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing='10dp')
        symbolLayout.add_widget(
            Label(text='Include special symbol', font_size='15sp', size_hint_x=0.135)
        )
        symbolEnabledCheckBox = CheckBox(size_hint_x=0.2)
        symbolLayout.add_widget(symbolEnabledCheckBox)
        mainLayout.add_widget(symbolLayout)

        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        confirmButton = MDRaisedButton(text='Confirm')
        cancelButton = MDRaisedButton(text='Cancel')
        button_box.add_widget(confirmButton)
        button_box.add_widget(cancelButton)
        mainLayout.add_widget(button_box)
        cls._createLoginDetailsPopup = Popup(title='Edit Login Details',
                                        content=mainLayout,
                                        size_hint=(None,None),
                                        size=(600,600))
        cancelButton.bind(on_release=cls._createLoginDetailsPopup.dismiss)
        confirmButton.bind(on_release=lambda x:cls.updateLoginDetailsToDB(x,cls._createLoginDetailsPopup,applicationNameTextInput.text,usernameTextInput.text,util.generatePassword(symbolEnabledCheckBox.active,int(passwordLengthSlider.value))))

        cls._createLoginDetailsPopup.open()

    @classmethod
    def onSliderValueChange(cls,widget,val):
        widget.text=str(int(val)) 

    @classmethod
    def updateLoginDetailsToDB(cls,db,instance,popup,applicationName,username,password): 
        db.addEntryToDB(applicationName,username,password)
        popup.dismiss()
        popup = Popup(title='Success',
                            content=Label(text='Your details have been stored'),
                            size_hint=(None,None),
                            size=(600,600))
        popup.open()