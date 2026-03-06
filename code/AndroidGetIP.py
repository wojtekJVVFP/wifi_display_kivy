'''
This module allows you to get the IP address of your Kivy/python-for-android app.
It was created by Ryan Marvin and is free to use.
Credit to Bruno Adele for the int_to_ip method
'''
#Required : ACCESS_WIFI_STATE permission, pyjnius

def int_to_ip(ipnum):
    oc1 = int(ipnum / 16777216) % 256
    oc2 = int(ipnum / 65536) % 256
    oc3 = int(ipnum / 256) % 256
    oc4 = int(ipnum) % 256
    # oc1 = 192
    # oc2 = 168
    # oc3 = 1
    # oc4 = 117

    return "{}.{}.{}.{}".format(oc4,oc3,oc2,oc1)
    
def getIP():
    from jnius import autoclass

    '''PythonActivity = autoclass('org.renpy.android.PythonActivity')
    SystemProperties = autoclass('android.os.SystemProperties')
    Context = autoclass('android.content.Context')
    wifi_manager = PythonActivity.mActivity.getSystemService(Context.WIFI_SERVICE)
    ip = wifi_manager.getConnectionInfo()
    ip = ip.getIpAddress()'''
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WifiManager = autoclass('android.net.wifi.WifiManager')

    activity = PythonActivity.mActivity
    wifi = activity.getSystemService(activity.WIFI_SERVICE)
    info = wifi.getConnectionInfo()

    ip = info.getIpAddress()

    ip = int_to_ip(int(ip))
    return ip
if __name__=="__main__":
    getIP()