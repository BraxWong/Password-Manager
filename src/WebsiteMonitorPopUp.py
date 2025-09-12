from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard 
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from Database.LoginDetailsDB import LoginDetailsDB
import Util.UIUtil as UIUtil

class WebsiteMonitorPopup(object):
    _instance = None
    _popup_opened = False
    _popup = None
    _create_login_details_popup_opened = False
    _create_login_details_popup = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
    
    @classmethod
    def show_popup(cls,title,username,password):
        def create_popup(dt):
            if cls._popup_opened:
                cls._popup.dismiss()
                cls._popup_opened = False
            main_layout = BoxLayout(
                orientation='vertical',
                size_hint=(1,1),
                padding=0,
                spacing=50
            )
            main_layout.add_widget(Label(text=f'Username:{username}\nPassword:{password}'))
            button_box = MDBoxLayout(
                pos_hint={"center_x": 0.5},
                adaptive_size=True,
                padding="24dp",
                spacing="24dp",
            )

            copy_username_button = MDRaisedButton(text='Copy Username')
            copy_username_button.bind(on_release=lambda x:Clipboard.copy(username))
            copy_password_button = MDRaisedButton(text='Copy Password')
            copy_password_button.bind(on_release=lambda x:Clipboard.copy(password))
            button_box.add_widget(copy_username_button)
            button_box.add_widget(copy_password_button)
            main_layout.add_widget(button_box)
            cls._popup = Popup(title=title,
                            content=main_layout,
                            size_hint=(None,None),
                            size=(400,400))
            cls._popup.open()
        Clock.schedule_once(create_popup)

    @classmethod
    def show_create_login_details_popup(cls):
        def create_popup(dt):
            if cls._create_login_details_popup_opened:
                cls._create_login_details_popup.dismiss()
                cls._create_login_details_popup_opened = False
            
            info_map = UIUtil.createLoginDetailPopupLayout()
            button_box = MDBoxLayout(
                pos_hint={"center_x": 0.5},
                adaptive_size=True,
                padding="24dp",
                spacing="24dp",
            )

            confirm_button = MDRaisedButton(text='Confirm')
            cancel_button = MDRaisedButton(text='Cancel')
            button_box.add_widget(confirm_button)
            button_box.add_widget(cancel_button)
            info_map["Layout"].add_widget(button_box)
            cls._create_login_details_popup = Popup(title='Create Login Details',
                                            content=info_map["Layout"],
                                            size_hint=(None,None),
                                            size=(600,600))
            cancel_button.bind(on_release=cls._create_login_details_popup.dismiss)
            confirm_button.bind(on_release=lambda x:
                               cls.update_login_details_to_db(x,
                                                          cls._create_login_details_popup,
                                                          info_map["ApplicationName"].text,
                                                          info_map["Username"].text,
                                                          util.generate_password(info_map["SymbolEnabledCheckBox"].active,int(info_map["PasswordLength"].value))))

            cls._create_login_details_popup.open()
        Clock.schedule_once(create_popup)

    @classmethod
    def update_login_details_to_db(cls,instance,popup,application_name,username,password): 
        db = LoginDetailsDB()
        db.add_entry_to_db(application_name,username,password)
        popup.dismiss()
        popup = Popup(title='Success',
                            content=Label(text='Your details have been stored'),
                            size_hint=(None,None),
                            size=(600,600))
        popup.open()
