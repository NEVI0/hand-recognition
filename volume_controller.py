import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

from constants import *


class VolumeController:
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_controller = cast(self.interface, POINTER(IAudioEndpointVolume))

        self.vol_range = self.volume_controller.GetVolumeRange()
        self.min_vol, self.max_vol = self.vol_range[0], self.vol_range[1]

    def set_volume(self, length):
        volume = np.interp(length, [50, 250], [self.min_vol, self.max_vol])
        self.volume_controller.SetMasterVolumeLevel(volume, None)

        return np.interp(length, [50, 250], [400, 100])

    @staticmethod
    def display_volume_bar(img, volume_bar):
        cv2.rectangle(img, (600, 100), (620, 400), BLACK_COLOR, 2)

        if volume_bar:
            cv2.rectangle(img, (600, int(volume_bar)), (620, 400), YELLOW_COLOR, cv2.FILLED)
