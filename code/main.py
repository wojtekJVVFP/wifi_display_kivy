from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
import asyncio
import websockets
import json
import io
from PIL import Image as ImagePIL

from disp_no import DEVICE_NO, BASE_DISP  #number of current and base display
from websocket_devices import Ws_devices, devices

local_device = devices[DEVICE_NO]

class WifiServer(Widget):
    # button = ObjectProperty(None)
    label = ObjectProperty(None)
    button = ObjectProperty(None)
    image = ObjectProperty(None)

    test = 0

    #__init__

    def update(self, dt):
        pass
        #print('{}'.format(self.test))
        #self.label.text = str(self.test)

class WifiServerApp(App):
    def build(self):
        server = WifiServer()

        Clock.schedule_interval(server.update, 1.0/60.0)
        return server

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
            global image_pil

            print('Wiadomość odebrana: {}'.format(message[:30]))
            self.root.label.text = str(message)[:10]

            image_file_array = json.loads(message)
            image_file_bytes = bytes(image_file_array)

            image_bytesIO = io.BytesIO()
            image_bytesIO.write(image_file_bytes)

            image_base_pil = ImagePIL.open(image_bytesIO)

            image_bytesIO.seek(0)   #był niezbędny do prawidłowego zadziałania odczytu
            kivy_image = Image()
            kivy_image.texture = CoreImage(image_bytesIO, ext="jpg").texture    #gotowy obrazek do wyświetlenia w interfejsie

            self.root.image.texture = kivy_image.texture

            #Odbiór obrazka i zamiana na postać do wyświetlenia w widgecie image

            return_data_dict = {
                'data': 'dane',
                'width': 10,
                'height': 20,
                'window_width': 30,
                'window_height': 40
            }
            await websocket.send(json.dumps(return_data_dict))

    async def server_routine(self):
        try:
            async with websockets.serve(self.send1, local_device.ip, local_device.port_no, max_size=None):
                await asyncio.Future()  # run forever
        except asyncio.CancelledError as e:
            print('UI ended')
        finally:
            # when canceled, print that it finished
            print('Done')


if __name__ == '__main__':
    #WifiServerApp().run()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(WifiServerApp().app_func())
    loop.close()