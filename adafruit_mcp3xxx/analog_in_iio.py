# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
:py:class:`~adafruit_mcp3xxx.analog_in_iio.AnalogIn`
======================================================
AnalogIn for single-ended and
differential iio ADC readings.

* Author(s): Brent Rubell

.. warning::
    The ADC chips supported by this library do not use negative numbers. If the resulting
    differential read is less than 0, then the returned integer value (and voltage value) is ``0``.
    If for some reason the voltage on a channel is greater than the reference voltage or
    less than 0, then the returned integer value is ``65535`` or ``0`` respectively.

"""
import os



class AnalogIn:
    """AnalogIn Mock Implementation for iio ADC Reads. Appropriate
    Device Tree Overlay must be applied.

    :param iio_device: iio device number of the mcp30xx.
    :param float ref_voltage: Voltage into (Vin) the ADC.
    :param int positive_pin: Required pin for single-ended.
    :param int negative_pin: Optional pin for differential reads.
    """

    def __init__(
        self, iio_device: int=1, ref_voltage: float=3.3, positive_pin: int=0, negative_pin:int=-1
    ) -> None:
        self._iio_device = iio_device
        self._ref_voltage = ref_voltage
        self._positive_pin = positive_pin
        self._negative_pin = negative_pin
        if self._negative_pin >= 0:
            self._iio_path = f"/sys/bus/iio/devices/iio:device{self._iio_device}/in_voltage{self._positive_pin}-voltage{self._negative_pin}_raw"
        else:
            self._iio_path = f"/sys/bus/iio/devices/iio:device{self._iio_device}/in_voltage{self._positive_pin}_raw"
        if not os.path.exists(self._iio_path):
            raise FileNotFoundError(
                self._iio_path 
                "is not a valid iio device."
                "Please Check Arguments and Device Tree Overlays."
            )
            

    @property
    def value(self) -> int:
        """Returns the value of an ADC pin as an integer. For conforimty purposes, the
        returned values range [0, 65535]."""
        return (int((self.value_raw / 1023.0) * 65535))

    @property
    def value_raw(self) -> int:
        """Returns the value of an ADC pin as an integer. Due to 10-bit accuracy of the chip, the
        returned values range [0, 1023]."""
        with open(self._iio_path, 'r') as file_:
            reading = file_.read()
        return(int(reading))

    @property
    def voltage(self) -> float:
        """Returns the voltage from the ADC pin as a floating point value. Due to the 10-bit
        accuracy of the chip, returned values range from 0 to ((``ref_voltage`` *
        1023) / 1023)"""
        return ((self.value_raw * self._ref_voltage) / 1023)
