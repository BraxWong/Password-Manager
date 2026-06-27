from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from Database.LoginDetailsDB import *
from Database.EmailSettings import TwoFactorAuthenticationSettingsDB
from EmailNotificationThread import EmailNotificationThread
from importPassword import ImportPassword
from exportPassword import ExportPassword
from passwordGeneration import *
from loginDetailsStorage import * 
from TwoFactorAuthentication import *
from decryptPasswordFiles import *
from WebsiteMonitor import *
from Util.UIUtil import *
from Util.SecurityModule import *
import threading

class Menu(Screen):
    def __init__(self, **kwargs):
        super(Menu,self).__init__(**kwargs)

        self.security_module = SecurityModule()

        self.two_factor_auth = TwoFactorAuthenticationSettingsDB()
        self.two_factor_auth_info = self.two_factor_auth.fetch_all_from_db()

        self.website_monitor = WebsiteMonitor()
        self.website_monitor_thread = threading.Thread(target=self.website_monitor.run, daemon=True)

        self.email_notification= EmailNotificationThread()
        self.email_notification_thread = threading.Thread(target=self.email_notification.run, daemon=True)

        self.layout = GridLayout(cols=1)
        self.cols=1
        self.layout.add_widget(Label(text='Password Manager',font_size='20sp'))

        self.search_password = Button(text='Find your password')
        self.search_password.bind(on_press=self.start_password_search)
        self.layout.add_widget(self.search_password)

        self.store_user_details = Button(text='Store Login Details')
        self.store_user_details.bind(on_press=self.store_login_details)
        self.layout.add_widget(self.store_user_details)

        self.generate_password = Button(text='Generate a password')
        self.generate_password.bind(on_press=self.start_password_generation)
        self.layout.add_widget(self.generate_password)

        self.send_email_notification = Button(text='2FA Settings')
        self.send_email_notification.bind(on_press=self.start_send_email_notification)
        self.layout.add_widget(self.send_email_notification)

        self.import_password = Button(text='Import password to system')
        self.import_password.bind(on_press=self.import_password_to_system)
        self.layout.add_widget(self.import_password)

        self.decrypt_password_file = Button(text='Decrypt password files')
        self.decrypt_password_file.bind(on_press=self.decrypt_password)
        self.layout.add_widget(self.decrypt_password_file)

        self.output_password = Button(text='Output password to file')
        self.output_password.bind(on_press=self.export_password_to_txt)
        self.layout.add_widget(self.output_password)

        self.output_password_email = Button(text='Output password to email')
        self.output_password_email.bind(on_press=self.export_password_to_email)
        self.layout.add_widget(self.output_password_email)

        self.start_stop_website_monitor = Button(text='Start website monitor')
        self.start_stop_website_monitor.bind(on_press=self.start_stop_monitor_thread)
        self.layout.add_widget(self.start_stop_website_monitor)

        self.user_audit = Button(text='User Audit')
        self.user_audit.bind(on_press=self.user_audit_screen)
        self.layout.add_widget(self.user_audit)

        self.add_widget(self.layout)

        self.start_send_email_notification_thread()


    def start_password_search(self,widget):
        self.manager.current = 'Password Search Screen'

    def start_password_generation(self,widget):
        self.manager.current = 'Password Generation Screen'

    def start_send_email_notification(self,widget):
        self.manager.current = '2FA Screen'

    def import_password_to_system(self,widget):
        self.import_password = ImportPassword(self.security_module)

    def export_password_to_txt(self,widget):
        self.exportPassword = ExportPassword(self.security_module)

    def decrypt_password(self,widget):
        self.decryptPassword = DecryptPasswordFiles(self.security_module)

    def export_password_to_email(self, widget):
        def send_credentials(result):
            if result:
                if not self.email_notification.running:
                    self.email_notification_thread = threading.Thread(target=self.emailNotification.sendLoginDetails, daemon=True)
                    self.email_notification_thread.start()                     
                    show_popup('Success',Label(text="Your user credentials have been sent to your email address."))
                    self.security_module.audit_action('EXPORT_EMAIL', 'User\'\s credentials have been export to their email address.')
                else:
                    self.email_notification.stop()
                    if self.email_notification_thread.is_alive():
                        self.email_notification_thread.join()  
            else:
                show_popup('Error',Label(text="The 2FA code you provided is incorrect.Please try again"))
                self.security_module.audit_action('2FA_AUTH', 'User has failed 2FA.')

        if not len(self.two_factor_auth_info) or not self.two_factor_auth_info[0][1]:
            send_credentials(True)
        else:
            create_2FA_popup_layout(send_credentials)

    def store_login_details(self,widget):
        self.manager.current = 'Login Details Storage Screen'

    def user_audit_screen(self, widget):
        self.manager.current = 'User Audit Screen'

    def start_send_email_notification_thread(self):
        if not self.email_notification.running:
            def initializeEmailNotificationThread(dt):
                self.email_notification_thread.start()
                self.email_notification_thread.run
            Clock.schedule_once(initializeEmailNotificationThread,0)
        else:
            self.email_notification.stop()
            self.email_notification_thread.join()

    #TODO: Kinda works but it does not allow the thread to restart. Have to think of a work around
    def start_stop_monitor_thread(self,widget):
        def run(result):
            if result:
                if self.website_monitor.driver is None:
                    def initializeMonitorThread(dt):
                        self.website_monitor_thread.start()
                        self.website_monitor_thread.run 
                    Clock.schedule_once(initializeMonitorThread,0)
                    self.start_stop_website_monitor.text = 'Stop website monitor'
                else:
                    self.website_monitor.stop()
                    self.website_monitor_thread.join(timeout=1)            
                    self.start_stop_website_monitor.text = 'Start website monitor'
            else:
                show_popup('Error',Label(text="The 2FA code you provided is incorrect.Please try again"))
        print(self.two_factor_auth_info)
        if isinstance(self.two_factor_auth_info, int) or not self.two_factor_auth_info[0][2]:
            run(True)
        else:
            create_2FA_popup_layout(run)

