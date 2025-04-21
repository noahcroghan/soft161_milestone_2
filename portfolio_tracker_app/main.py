from kivy.app import App
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty


class PortfolioTrackerApp(App):
    crypto_price = StringProperty("")
    portfolio_value = StringProperty("")
    portfolio_value_change = StringProperty("")
    input_text = StringProperty("")

    def check_value(self, input_id, message_id):
        if input_id.text != '':
            message_id.text = ""
            self.crypto_price = "$#.##"
            self.portfolio_value = "$###.##"
            self.portfolio_value_change = "+ ##.##%"
        else:
            self.crypto_price = ""
            self.portfolio_value = ""
            self.portfolio_value_change = ""
            message_id.text = "Portfolio ID is Required"

    def go_to_home(self, message_id):
        self.crypto_price = ""
        self.portfolio_value = ""
        self.portfolio_value_change = ""
        self.input_text = " "
        self.input_text = ""
        message_id.text = ""

    def submit_data(self, message_id, id1, id2, id3, message_pass, message_fail):
        if id1.text != '' and id2.text != '' and id3.text != '':
            message_id.text = message_pass
            id1.text = ""
            id2.text = ""
            id3.text = ""
        else:
           message_id.text = message_fail

    def build(self):
        inspector.create_inspector(Window, self)


if __name__ == '__main__':
    Window.size = (420, 720)
    app = PortfolioTrackerApp()
    app.run()