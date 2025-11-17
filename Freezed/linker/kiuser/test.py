from kivy.app import App

class application(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
if __name__ == '__main__':
    app = application()
    app.run()