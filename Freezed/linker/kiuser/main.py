from kivy.app import App
from kivy.uix.label import Label
from plyer import gps

class GPSApp(App):

    def build(self):
        # 创建一个文本标签
        self.label = Label(text="Waiting for GPS data...")

        # 启动GPS服务
        gps.configure(on_location=self.on_location)

        return self.label

    def on_location(self, **kwargs):
        # 更新标签文本
        self.label.text = "Latitude: {lat}, Longitude: {lon}".format(
            lat=kwargs['lat'],
            lon=kwargs['lon']
        )

if __name__ == '__main__':
    GPSApp().run()