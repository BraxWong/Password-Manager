from kivy.uix.modalview import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard 
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from Database.LoginDetailsDB import *
from Database.VerifyUserDB import *
from Database.EmailSettings import *
from Util.two_factor_authentication import *
from LastActionTaken import LastActionTaken
import Util.Util as util
import Util.UIUtil as ui_util
import Util.passwordHasing as password_hashing
import Util.wordSearchAlgorithm as word_search

class PasswordSearch(Screen):
    def __init__(self, **kwargs):
        self.last_action_taken = LastActionTaken()
        self.paused_action = ""
        self.invalid_login_attempt = 0

        super(PasswordSearch,self).__init__(**kwargs)
        self.db = LoginDetailsDB() 
        self.verify_user_db = VerifyUserDB()
        self.two_factor_auth_db = TwoFactorAuthenticationSettingsDB()
        self.main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),  
            padding=0,
            spacing=50  
        )
        self.top_row_layout = BoxLayout(orientation='horizontal', 
                                      size_hint_y=None, 
                                      height=50, 
                                      padding=(10, 0))
        self.back_button = MDRaisedButton(text="Back", on_release=self.on_button_press)
        self.top_row_layout.add_widget(self.back_button)
        self.top_row_layout.add_widget(
            Label(
                text='Password Searching', 
                font_size='20sp', 
                halign='center',
                size_hint_x=0.8
            )
        )        
        self.main_layout.add_widget(self.top_row_layout)
        self.all_login_details = self.db.fetchAllFromDB()
        self.logged_in = False
        
        self.search_bar_layout = AnchorLayout(
            anchor_x='center',
            size_hint_y=None,
            height=50,
            padding=(10, 0)
        )

        self.search_bar = TextInput(
            text='', 
            multiline=False, 
            halign='center', 
            size_hint_x=None,  
            width=800,
            hint_text='Search Login Details By Website Name'
        )
        self.search_bar.bind(text=self.on_search)
        self.search_bar_layout.add_widget(self.search_bar)
        self.main_layout.add_widget(self.search_bar_layout)

        button_box = MDBoxLayout(
            pos_hint={"center_x": 0.5},
            adaptive_size=True,
            padding="24dp",
            spacing="24dp",
        )

        for button_text in ["Delete", "Update", "Reveal Password", "Hide Password", "Copy Username", "Copy Password"]:
            button_box.add_widget(
                MDRaisedButton(
                    text=button_text, on_release=self.on_button_press
                )
            )

        table_and_buttons = BoxLayout(orientation='vertical', size_hint=(None, None), width=800)
        self.row_checked = []
        self.data = []
        self.all_password = []
        self.table = MDDataTable(
            column_data = [
                ("Index",dp(30)),
                ("Password Safety",dp(30)),
                ("Application Name",dp(30)),
                ("Username",dp(30)),
                ("Password",dp(30)),
                ("Date Created",dp(30))
            ],
            row_data = self.data,
            size_hint = (None,None),
            width = 800,
            height = 400,
            background_color_cell="#451938",
            background_color_selected_cell="e4514f",
            check = True,
            use_pagination = True
        )
        self.table.bind(on_check_press=self.on_check_press)
        table_and_buttons.add_widget(self.table)
        table_and_buttons.add_widget(button_box)
        self.table_layout = AnchorLayout()
        self.table_layout.add_widget(table_and_buttons)
        self.main_layout.add_widget(Widget(size_hint_y=1))
        self.main_layout.add_widget(self.table_layout)
        self.add_widget(self.main_layout)

    def on_check_press(self, instance_table, current_row):
        if current_row[0] not in self.row_checked:
            self.row_checked.append(current_row[0])
        else:
            self.row_checked.remove(current_row[0])

    def on_button_press(self, instance_button: MDRaisedButton):
        try:
            {
                "Update": lambda:self.update_login_details(),
                "Delete": lambda:self.delete_login_details_confirmation(),
                "Back": lambda:self.return_to_menu(),
                "Reveal Password": lambda:self.password_censor(False),
                "Hide Password": lambda:self.password_censor(),
                "Copy Password": lambda:self.copy_password_or_username_to_clipboard(False),
                "Copy Username": lambda:self.copy_password_or_username_to_clipboard(True)
            }[instance_button.text]()
        except KeyError:
            pass

    def on_pre_enter(self, *args):
        if len(self.verify_user_db.getUserPasswordAndHint()) > 0 and not self.logged_in:
            self.two_factor_auth()
        elif len(self.verify_user_db.getUserPasswordAndHint()) == 0:
            self.create_password_and_hint()
        else:
            self.refresh_table_data()

    def refresh_table_data(self):
        self.all_login_details = self.db.fetchAllFromDB()
        self.data = []
        self.all_password = []
        if len(self.all_login_details) > 0:
            for i,password in enumerate(self.all_login_details):
                self.all_password.append(password[2])
                self.password = "*" * len(password[2])
                self.data.append((i,util.date_comparison(password[3]),password[0],password[1],self.password,password[3]))
        self.table.update_row_data(self.table.row_data, self.data)

    def on_search(self,instance,value):
        if len(value) == 0:
            self.refresh_table_data()
        elif len(self.all_login_details)>0:
            self.data = []
            self.all_password = []
            scores = word_search.search_website(self.all_login_details,value)
            table_index = 0
            for i in range(len(scores)):
                if scores[i]>=len(value)/2:
                    self.all_password.append(self.all_login_details[i][2])
                    self.data.append((table_index,util.date_comparison(self.all_login_details[i][3]),self.all_login_details[i][0],self.all_login_details[i][1],self.all_login_details[i][2],self.all_login_details[i][3]))
                    table_index+=1
            self.table.update_row_data(self.table.row_data,self.data)

    def two_factor_auth(self):
        self.two_factor_auth_info = self.two_factor_auth_db.fetchAllFromDB()
        if not len(self.two_factor_auth_info) or not self.two_factor_auth_info[0][1]:
            self.password_search_login(True)
        else:
            ui_util.create_2FA_popup_layout(self.password_search_login)
             
    def password_search_login(self, result):
        if result:
            main_layout = BoxLayout(orientation='vertical')

            password_layout = BoxLayout(orientation='horizontal')
            password_layout.add_widget(Label(text='Password',
                                                    font_size='15sp',
                                                    pos_hint={'x':0.2,'y':0})
                                                )
            password_text_input = TextInput(text='', 
                                        multiline=False,
                                        size_hint=(None,None), 
                                        height=30, 
                                        width=250,
                                        pos_hint={'x':0.5,'y':0.45})

            password_layout.add_widget(password_text_input)
            main_layout.add_widget(password_layout)


            hint_layout = BoxLayout(orientation='horizontal')
            hint_layout.add_widget(Label(text='Hint',
                                            font_size='15sp',
                                            pos_hint={'x':0.2,'y':0},))
            hint_text_input = TextInput(text='', 
                                    multiline=False,
                                    size_hint=(None,None), 
                                    height=30, 
                                    width=250,
                                    pos_hint={'x':0.5,'y':0.45})
            hint_layout.add_widget(hint_text_input)
            main_layout.add_widget(hint_layout)

            button_box = MDBoxLayout(
                pos_hint={"center_x": 0.5},
                adaptive_size=True,
                padding="24dp",
                spacing="24dp",
            )

            confirm_button = MDRaisedButton(text='Confirm')
            hint_button = MDRaisedButton(text='Hint')
            button_box.add_widget(confirm_button)
            button_box.add_widget(hint_button)
            main_layout.add_widget(button_box)
            popup = Popup(title='Password Search Login',
                            content=main_layout,
                            size_hint=(None,None),
                            size=(600,600))
            hint_button.bind(on_release=lambda x:self.show_hint(x,hint_text_input))
            confirm_button.bind(on_release=lambda x:self.verify_password_search_login(x,password_text_input.text,popup))
            popup.open()
        else:
            ui_util.show_incorrect_2FA_popup()
    
    def show_hint(self, instance, text_box):
        hint = self.verify_user_db.getUserPasswordAndHint()[0][1]
        text_box.text = hint

    def verify_password_search_login(self,instance,user_input_password, password_popup):
        password = self.verify_user_db.getUserPasswordAndHint()[0][0]
        if password_hashing.check_password(user_input_password,password):
            self.refresh_table_data()
            password_popup.dismiss()
            self.invalid_login_attempt = 0
            self.logged_in = True
            self.last_action_taken.update_time()
            self.resume_paused_action()
        else:
            self.invalid_login_attempt += 1
            incorrect_password_popup = Popup(title='Incorrect Password',
                                           content=Label(text='Incorrect Password'),
                                           size_hint=(None,None),
                                           size=(600,600))
            incorrect_password_popup.open()
            if self.invalid_login_attempt == 3:
                self.return_to_menu()
  
    def create_password_and_hint(self):
        main_layout = BoxLayout(orientation='vertical')
        password_layout = BoxLayout(orientation='horizontal')
        password_layout.add_widget(Label(text='Password',
                                                font_size='15sp',
                                                pos_hint={'x':0.2,'y':0})
                                            )
        password_text_input = TextInput(text='', 
                                      multiline=False,
                                      size_hint=(None,None), 
                                      height=30, 
                                      width=250,
                                      pos_hint={'x':0.5,'y':0.45})

        password_layout.add_widget(password_text_input)
        main_layout.add_widget(password_layout)

        hint_layout = BoxLayout(orientation='horizontal')
        hint_layout.add_widget(Label(text='Hint',
                                        font_size='15sp',
                                        pos_hint={'x':0.2,'y':0},))
        hint_text_input = TextInput(text='', 
                                  multiline=False,
                                  size_hint=(None,None), 
                                  height=30, 
                                  width=250,
                                  pos_hint={'x':0.5,'y':0.45})
        hint_layout.add_widget(hint_text_input)
        main_layout.add_widget(hint_layout)

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
        main_layout.add_widget(button_box)
        popup = Popup(title='Create password & hint',
                          content=main_layout,
                          size_hint=(None,None),
                          size=(600,600))
        cancel_button.bind(on_release=lambda x:self.cancel_password_and_hint(x,popup))
        confirm_button.bind(on_release=lambda x:self.create_password_search_password(x,password_text_input.text,hint_text_input.text,popup))
        popup.open()
        
    def create_password_search_password(self,instance,password,hint,popup):
        self.verify_user_db.addPasswordAndHint(password_hashing.encode_password(password),hint)
        popup.dismiss()
        self.refresh_table_data()

    def cancel_password_and_hint(self,instance,popup):
        popup.dismiss()
        self.return_to_menu()

    def return_to_menu(self):
        self.manager.current = 'Menu Screen'

    def update_login_details(self):
        self.paused_action = "update"
        if not self.check_timeout(): 
            if len(self.table.get_row_checks()) != 1:
                popUp = Popup(title='Error',
                            content=Label(text="Please select 1 row at a time when updating your login details"),
                            size_hint=(None,None),
                            size=(600,600))
                popUp.open()
            else:
                current_index = int(self.row_checked[0])
                info_map = ui_util.createLoginDetailPopupLayout() 

                button_box = MDBoxLayout(
                    pos_hint={"center_x": 0.5},
                    adaptive_size=True,
                    padding="24dp",
                    spacing="24dp",
                )
                info_map["Username"].text = self.table.row_data[current_index][3]
                confirm_button = MDRaisedButton(text='Confirm')
                cancel_button = MDRaisedButton(text='Cancel')
                button_box.add_widget(confirm_button)
                button_box.add_widget(cancel_button)
                info_map["Layout"].add_widget(button_box)
                editLoginDetailsPopup = Popup(title='Edit Login Details',
                                            content=info_map["Layout"],
                                            size_hint=(None,None),
                                            size=(600,600))

                cancel_button.bind(on_release=editLoginDetailsPopup.dismiss)
                confirm_button.bind(on_release=lambda x:self.update_login_details_to_db(x,editLoginDetailsPopup,info_map["ApplicationName"].text,info_map["Username"].text,util.generate_password(info_map["SymbolEnabledCheckBox"].active,int(info_map["PasswordLength"].value))))
                editLoginDetailsPopup.open()

    def update_login_details_to_db(self,instance,popup,application_name,username,password):
        self.db.updateEntryToDB(application_name,username,password)
        self.refresh_table_data()
        popup.dismiss()
        update_popup = Popup(title='Success',
                            content=Label(text='Your details have been updated'),
                            size_hint=(None,None),
                            size=(600,600))
        update_popup.open()

    def password_censor(self, hide_password = True):
        self.paused_action = "censor" if hide_password else "reveal"
        if not self.check_timeout():
            for row in self.row_checked: 
                current_index = int(row)
                new_row = list(self.table.row_data[current_index])
                new_row[4] = "*" * len(self.all_password[current_index])
                if not hide_password:
                    new_row[4] = self.all_password[current_index]
                self.table.update_row(self.table.row_data[current_index],new_row)

    def copy_password_or_username_to_clipboard(self, copy_username):
        self.paused_action = "copy username" if copy_username else "copy password"
        if not self.check_timeout():
            popup_text = "username" if copy_username else "password"
            if len(self.row_checked) != 1:
                popup = Popup(title="Error",
                            content=Label(text=f"Please select 1 {popup_text} to be copied to the clipboard."),
                            size_hint=(None,None),
                            size=(600,600))
                popup.open()
            else:
                content_to_copy = self.table.row_data[int(self.row_checked[0])][3] if copy_username else self.all_password[int(self.row_checked[0])]
                Clipboard.copy(content_to_copy)
                popup = Popup(title="Success",
                            content=Label(text=f"The {popup_text} has been copied to the clipboard."),
                            size_hint=(None,None),
                            size=(600,600))
                popup.open()

    def delete_login_details_confirmation(self):
        self.paused_action = "delete"
        if not self.check_timeout():
            if len(self.row_checked) >= 1:
                confirmation_layout = BoxLayout(orientation='vertical',
                                                    size_hint=(None,None),
                                                    width=500,
                                                    pos_hint={'center_x':0.5})
                button_box = MDBoxLayout(
                    pos_hint={"center_x": 0.5},
                    adaptive_size=True,
                    padding="24dp",
                    spacing="24dp",
                )

                confirm_button = MDRaisedButton(text='Confirm')
                cancel_button = MDRaisedButton(text='Cancel')
                confirmation_layout.add_widget(Label(text='Are you sure you want to remove these login details?'))
                button_box.add_widget(confirm_button)
                button_box.add_widget(cancel_button)
                confirmation_layout.add_widget(button_box)
                confirmation_popup = Popup(title='Confirmation',
                                        content=confirmation_layout,
                                        size_hint=(None,None),
                                        size=(600,200))

                cancel_button.bind(on_release=confirmation_popup.dismiss)
                confirm_button.bind(on_release=lambda x: self.delete_login_details(x,confirmation_popup))
                confirmation_popup.open()

    def delete_login_details(self, instance, popup_window):
        popup_window.dismiss()
        message = "The following website login details have been removed:"
        rows_to_delete = [] 
        for row in self.row_checked:
            rows_to_delete.append(self.table.row_data[int(row)])

        rows_to_delete.sort(key=lambda x: int(x[0]), reverse=True)

        for row in rows_to_delete:
            self.db.removeEntryFromDB(row[2])
            self.table.remove_row(self.table.row_data[int(row[0])])
            self.refresh_table_data()
            message += f"\n{row[2]}"

        popup = Popup(title='Success',
                      content=Label(text=message),
                      size_hint=(None,None),
                      size=(600,600))

        popup.open() 

    def check_timeout(self):
        if self.last_action_taken.check_login_required():
            self.password_search_login()
            return True
        else:
            self.last_action_taken.update_time()
            return False

    def resume_paused_action(self):
        match self.paused_action:
            case "update":
                self.update_login_details()
            case "delete":
                self.delete_login_details_confirmation()
            case "censor":
                self.password_censor()
            case "reveal":
                self.password_censor(False)
            case "copy username":
                self.copy_password_or_username_to_clipboard(True)
            case "copy password":
                self.copy_password_or_username_to_clipboard(False)
            case _:
                pass
        self.paused_action = ""
