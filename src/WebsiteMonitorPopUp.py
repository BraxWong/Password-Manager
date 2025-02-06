from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from Database.LoginDetailsDB import LoginDetailsDB
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
        def create_popup(dt):
            if cls._popupOpened:
                cls._popup.dismiss()
                cls._popupOpened = False
            #TODO: Enable users to copy both users and passwords to their clipboard when the popup is opened.
            cls._popup = Popup(title=title,
                            content=Label(text=content),
                            size_hint=(None,None),
                            size=(400,400))
            cls._popup.open()
        Clock.schedule_once(create_popup)

    @classmethod
    def showCreateLoginDetailsPopup(cls):
        def create_popup(dt):
            if cls._createLoginDetailsPopupOpened:
                cls._createLoginDetailsPopup.dismiss()
                cls._createLoginDetailsPopupOpened = False
            
            infoMap = util.createLoginDetailPopupLayout()
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
            infoMap["Layout"].add_widget(button_box)
            cls._createLoginDetailsPopup = Popup(title='Create Login Details',
                                            content=infoMap["Layout"],
                                            size_hint=(None,None),
                                            size=(600,600))
            cancelButton.bind(on_release=cls._createLoginDetailsPopup.dismiss)
            confirmButton.bind(on_release=lambda x:
                               cls.updateLoginDetailsToDB(x,
                                                          cls._createLoginDetailsPopup,
                                                          infoMap["ApplicationName"].text,
                                                          infoMap["Username"].text,
                                                          util.generatePassword(infoMap["SymbolEnabledCheckBox"].active,int(infoMap["PasswordLength"].value))))

            cls._createLoginDetailsPopup.open()
        Clock.schedule_once(create_popup)

    @classmethod
    def updateLoginDetailsToDB(cls,instance,popup,applicationName,username,password): 
        db = LoginDetailsDB()
        db.addEntryToDB(applicationName,username,password)
        popup.dismiss()
        popup = Popup(title='Success',
                            content=Label(text='Your details have been stored'),
                            size_hint=(None,None),
                            size=(600,600))
        popup.open()