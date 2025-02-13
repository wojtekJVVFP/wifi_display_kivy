from disp_no import DEVICE_NO, BASE_DISP   #number of current and base display

class Disp_data():
    def __init__(self, resolution: tuple, dpi: int, margins: tuple):
        self.resolution = resolution
        self.dpi = dpi
        self.margins = margins
        self.calculated_margins = []

# converting mm to pixels according to given display data
def mm_to_pixel(disp: Disp_data, mm: float) -> int:
    dpi = disp.dpi #dots per inch, 1 inch = 25,4 mm
    pixels = mm * dpi / 25.4
    return int(pixels)

class Ws_devices():
    def __init__(self, ip, name, greet, isActive, resolution=(640,480), dpi = 500, margins = (0,0,0,0)):    #margins (left, upper, right, lower)
        self.ip = ip
        self.name = name
        self.greet = greet
        self.port_no = '8765' # można zmienić numer portu dla danego urządzenia jeśli jest inny
        self.isActive = isActive
        #self.resolution = resolution # tuple (szer, wys), szerokość mniejsza
        self.disp_data = Disp_data(resolution, dpi, margins)
    def calc_margins(self, base_disp: Disp_data):
        for i in self.disp_data.margins:
            self.disp_data.calculated_margins.append(mm_to_pixel(base_disp, i))
    def return_address(self):
        return 'ws://'+self.ip+':'+self.port_no


devices = []
devices.append(Ws_devices(ip='localhost', name='lokalne', greet='jestem lokalne', isActive = True, resolution = (1000, 1000), dpi = 127, margins = (8,10,8,0)))               #0
devices.append(Ws_devices(ip='192.168.1.117', name='samsung note 9', greet='jestem note 9', isActive = True, resolution = (1440, 2990), dpi = 514, margins = (3,9,3,6)))   #1
devices.append(Ws_devices(ip='192.168.1.107', name='samsung J5 #1', greet='jestem J5 mamy', isActive = False, resolution = (720, 1280)))    #2
devices.append(Ws_devices(ip='192.168.1.108', name='samsung xCover', greet='jestem xCover', isActive = False, resolution = (480, 764), dpi = 207, margins = (4,18,4,16)))     #3
devices.append(Ws_devices(ip='192.168.1.109', name='samsung J5 #2', greet='jestem J5 #2', isActive = False, resolution = (720, 1280)))    #4
devices.append(Ws_devices(ip='192.168.1.110', name='Xiaomi Redmi Szczep', greet='Redmi Szczep', isActive = False, resolution = (720, 1230)))    #5
devices.append(Ws_devices(ip='192.168.1.111', name='Xiaomi Redmi Bogd', greet='Redmi Bogd', isActive = False, resolution = (720, 1280), dpi = 294, margins = (3,13,3,15)))    #6
devices.append(Ws_devices(ip='192.168.1.103', name='Galaxy Tab S7', greet='Tab S7', isActive = False, resolution = (2800, 1752), dpi = 226))    #7
devices.append(Ws_devices(ip='192.168.1.115', name='LG G2 mini', greet='g2 mini', isActive = False, resolution = (540, 848), dpi = 234, margins = (3,12,3,14)))    #8

#calculating pixel margins according to base display
base_disp = devices[BASE_DISP].disp_data
for i in devices:
    i.calc_margins(base_disp)
    print(i.disp_data.calculated_margins)

if __name__ == '__main__':
    pass
    #print(devices[0].disp_data.calculated_margins)
