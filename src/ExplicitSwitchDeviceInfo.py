from abc import ABC

from ham import DeviceInfo
from ham.switch import ExplicitSwitch
from ham.manager import __version__


class ExplicitSwitchDeviceInfo(ExplicitSwitch, ABC):
    location = None
    def device_info(self) -> DeviceInfo:

        return DeviceInfo(
            name=self.name,
            suggested_area=self.location,
            identifiers=[f"{self.name}"],
            sw_version=__version__,
            )