__version__ = 0.1
# jak przechwycić wciśnięcie klawisza?

import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
import asyncio
from websockets.server import serve
import json
import io
from AndroidGetIP import getIP
from websocket_devices import Ws_devices

from disp_no import DEVICE_NO, BASE_DISP  #number of current and base display
from websocket_devices import Ws_devices, devices

local_device = Ws_devices(ip='localhost', name='lokalne', greet='jestem lokalne', isActive = True, resolution = (1000, 1000), dpi = 127, margins = (8,10,8,0))

from kivy.utils import platform
if platform == 'android':       #thanks to that we can run script also in windows
    from android.permissions import Permission, request_permissions, check_permission
    from jnius import autoclass


class ImageScr(Screen):
    image = ObjectProperty(None)

    test = 0

    def update(self, dt):
        pass
        #print('{}'.format(self.test))
        #self.label.text = str(self.test)


class SettingsScr(Screen):
    button = ObjectProperty(None)
    ip_address = ObjectProperty(None)
    display_res = ObjectProperty(None)
    display_dpi = ObjectProperty(None)

    def reposition(self, *args):
        pass

#Ws_devices(ip='localhost', name='lokalne', greet='jestem lokalne', isActive = True, resolution = (1000, 1000), dpi = 127, margins = (8,10,8,0))
    def get_device_data(self, ):  # mostly written with claude AI
        ip = getIP()
        if platform == 'android':  # python autoclass is only available in android builds
            self.ip_address.text = f"{ip}"

            PythonActivity = autoclass('org.kivy.android.PythonActivity')

            # getting phone display data
            activity = PythonActivity.mActivity
            metrics = activity.getResources().getDisplayMetrics()
            width_px = metrics.widthPixels  # width in px
            height_px = metrics.heightPixels  # height in px
            density = metrics.density  # scale coeficcient (1.0 = 160 dpi, 2.0 = 320 dpi...)
            dpi = metrics.densityDpi  # "logical" dpi (np. 240, 320, 420, 480)
            xdpi = metrics.xdpi  # physical dpi horizontal
            ydpi = metrics.ydpi  # physical dpi vertical

            # getting device name
            Build = autoclass('android.os.Build')
            Settings = autoclass('android.provider.Settings$Global')
            resolver = PythonActivity.mActivity.getContentResolver()
            name = Settings.getString(resolver, 'device_name')   # name of the phone working in android 7.1+
            if not name:  # if name is None - empty
                name = f'{Build.MANUFACTURER} {Build.MODEL}'.title()

            self.display_res.text = f"{width_px}, {height_px}"
            self.display_dpi.text = f"{xdpi}, {ydpi}"

            local_device.ip = ip
            local_device.name = name
            local_device.resolution = (width_px, height_px)
            local_device.dpi = int((xdpi + ydpi) / 2)  # average dpi of the screen

        if platform == 'win':  # thanks to that we can run script also in windows
            self.ip_address.text = f"{ip}"


class WifiServerApp(App):
    sm = ScreenManager()
    def build(self):
        Window.bind(on_keyboard=self.on_back_key)
        self.sm.add_widget(ImageScr(name='imageScreen'))
        self.sm.add_widget(SettingsScr(name='settingsScreen'))
        Clock.schedule_interval(self.sm.get_screen('imageScreen').update, 1.0/60.0)
        return self.sm

    def on_back_key(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            App().get_running_app().stop()
            return True
        return False
    def on_start(self):
        self.sm.get_screen('settingsScreen').get_device_data()  # getting device information
        if platform == 'android':  # with this we can run script also in windows
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")

                else:
                    print("Did not get all permissions")
            request_permissions([Permission.INTERNET, Permission.ACCESS_WIFI_STATE, Permission.ACCESS_NETWORK_STATE], callback)
            # request_permissions([Permission.INTERNET, Permission.ACCESS_WIFI_STATE])
        print("test on start")

    def app_func(self):
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        self.other_task = asyncio.ensure_future(self.server_routine())

        async def run_wrapper():
            # we don't actually need to set asyncio as the lib because it is
            # the default, but it doesn't hurt to be explicit
            await self.async_run(async_lib='asyncio')
            print('App done')
            self.other_task.cancel()

        return asyncio.gather(run_wrapper(), self.other_task)

    '''
    send1 - wysyłanie gotowej odpowiedzi na zapytanie od klienta

    '''
    async def send1(self, websocket):
        async for message in websocket:

            print('Wiadomość odebrana: {}'.format(message[:30]))

            # Odbiór obrazka i zamiana na postać do wyświetlenia w widgecie image
            image_file_array = json.loads(message)
            image_file_bytes = bytes(image_file_array)

            image_bytesIO = io.BytesIO()
            image_bytesIO.write(image_file_bytes)

            image_bytesIO.seek(0)   #był niezbędny do prawidłowego zadziałania odczytu
            kivy_image = Image()
            kivy_image.texture = CoreImage(image_bytesIO, ext="jpg").texture    #gotowy obrazek do wyświetlenia w interfejsie

            self.root.get_screen('imageScreen').image.texture = kivy_image.texture

            return_data_dict = {
                'name': local_device.name,
                'width_px': local_device.resolution[0],
                'height_px': local_device.resolution[1],
                'dpi': local_device.dpi,
                'ip_address': local_device.ip
            }
            await websocket.send(json.dumps(return_data_dict))

    async def server_routine(self):
        from AndroidGetIP import getIP

        print("test server start")
        try:
            # async with serve(self.send1, local_device.ip, local_device.port_no, max_size=None):
            #     await asyncio.Future()  # run forever
            if platform == 'android':  # thanks to that we can run script also in android
                server = await serve(self.send1, getIP(), local_device.port_no, max_size=None) #zamiast IP podanego jednoznacznie pobrano go
            if platform == 'win':  # thanks to that we can run script also in windows
                server = await serve(self.send1, 'localhost', local_device.port_no, max_size=None)  # dla windows adres ip podany jest bezpośrednio
            await server.serve_forever()
        except asyncio.CancelledError as e:
            print('UI ended')
        except OSError as e:
            print("incorrect IP address")
        finally:
            # when canceled, print that it finished
            print('Done')


if __name__ == '__main__':
    #WifiServerApp().run()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(WifiServerApp().app_func())
    loop.close()