import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


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
