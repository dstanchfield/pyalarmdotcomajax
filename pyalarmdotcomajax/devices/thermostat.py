"""Alarm.com thermostat."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import logging

from pyalarmdotcomajax.errors import UnexpectedDataStructure

from . import BaseDevice, DesiredStateMixin, DeviceType

log = logging.getLogger(__name__)


class Thermostat(DesiredStateMixin, BaseDevice):
    """Represent Alarm.com thermostat element."""

    # Fan duration of 0 is indefinite. otherwise value == hours.
    # TODO: desiredRts (remote temp sensor), desiredLocalDisplayLockingMode. Need user with remote sensors.
    # In identity info, check localizeTempUnitsToCelsius.

    @dataclass
    class ThermostatAttributes(BaseDevice.DeviceAttributes):
        """Thermostat attributes."""

        # Base
        temp_average: float | None  # Temperature from thermostat and all remote sensors, averaged.
        temp_at_tstat: float | None  # Temperature at thermostat only.
        setpoint_offset: float | None
        inferred_mode: Thermostat.DeviceState | None  # Indicates what thermostat is actually doing (cooling vs heating) if mode = auto.
        # Fan
        supports_fan_mode: bool | None
        supports_fan_indefinite: bool | None
        supports_fan_circulate_when_off: bool | None
        supported_fan_durations: list[int] | None
        fan_mode: Thermostat.FanMode | None
        # fan_duration: int | None # Fan duration is not updated in server response, even when fan is turned on for specific amount of time.
        # Temp
        supports_heat: bool | None
        supports_heat_aux: bool | None
        supports_cool: bool | None
        supports_auto: bool | None
        supports_setpoints: bool | None
        min_heat_setpoint: float | None
        max_heat_setpoint: float | None
        min_cool_setpoint: float | None
        max_cool_setpoint: float | None
        heat_setpoint: float | None
        cool_setpoint: float | None
        setpoint_buffer: float | None
        # Humidity
        supports_humidity: bool | None
        humidity: int | None
        # Schedules
        supports_schedules: bool | None
        supports_schedules_smart: bool | None
        schedule_mode: Thermostat.ScheduleMode | None

    class DeviceState(Enum):
        """Enum of thermostat states."""

        # https://www.alarm.com/web/system/assets/customer-ember/enums/ThermostatStatus.js

        UNKNOWN = 0
        OFF = 1
        HEAT = 2
        COOL = 3
        AUTO = 4
        AUX_HEAT = 5

    class FanMode(Enum):
        """Enum of thermostat fan modes."""

        # https://www.alarm.com/web/system/assets/customer-ember/enums/ThermostatFanMode.js

        AUTO = 0  # Technically AUTO_LOW
        ON = 1  # Technically ON_LOW
        CIRCULATE = 6

        # Not Used
        # AUTO_HIGH = 2
        # ON_HIGH = 3
        # AUTO_MEDIUM = 4
        # ON_MEDIUM = 5
        # HUMIDITY = 7

    class LockMode(Enum):
        """Enum of thermostat lock modes."""

        # https://www.alarm.com/web/system/assets/customer-ember/enums/ThermostatLock.js

        DISABLED = 0
        ENABLED = 1
        PARTIAL = 2

    class ScheduleMode(Enum):
        """Enum of thermostat programming modes."""

        # https://www.alarm.com/web/system/assets/customer-ember/enums/ThermostatProgrammingMode.js

        MANUAL = 0
        SCHEDULED = 1
        SMART_SCHEDULES = 2

    class SetpointType(Enum):
        """Enum of thermostat setpoint types."""

        FIXED = 0
        AWAY = 1
        HOME = 2
        SLEEP = 3

    class Command(Enum):
        """Commands for ADC lights."""

        SET_STATE = "setState"

    DEVICE_MODELS = {
        4293: {"manufacturer": "Honeywell", "model": "T6 Pro"},
        10023: {"manufacturer": "ecobee", "model": "ecobee3 lite"},
    }

    @property
    def available(self) -> bool:
        """Return whether the light can be manipulated."""
        return (
            self._attribs_raw.get("canReceiveCommands", False)
            and self._attribs_raw.get("remoteCommandsEnabled", False)
            and self._attribs_raw.get("hasPermissionToChangeState", False)
            and self.state is not self.DeviceState.UNKNOWN
        )

    @property
    def attributes(self) -> ThermostatAttributes | None:
        """Return thermostat attributes."""

        # Descriptions from https://www.alarm.com/web/system/assets/customer-ember/models/devices/thermostat.ts

        return self.ThermostatAttributes(
            temp_average=self._get_float(
                "forwardingAmbientTemp"
            ),  # The temperature text for the forwarding ambient temperature.
            temp_at_tstat=self._get_float(
                "ambientTemp"
            ),  # The current temperature including any additional temperature sensor averaging.
            inferred_mode=self._get_special(
                "inferredMode", self.DeviceState
            ),  # the indicated or inferred state in text form.
            setpoint_offset=(
                _setpoint_offset := self._get_float("setpointOffset")
            ),  # The amount to increment or decrement the setpoint by when changing it.
            supports_fan_mode=self._get_bool(
                "supportsFanMode"
            ),  # Whether the thermostat supports fan mode control.
            supports_fan_indefinite=self._get_bool(
                "supportsIndefiniteFanOn"
            ),  # Whether the thermostat supports running the fan indefinitely.
            supports_fan_circulate_when_off=self._get_bool(
                "supportsCirculateFanModeWhenOff"
            ),  # Whether the thermostat supports the circulate fan mode when in OFF mode.
            supported_fan_durations=self._get_list(
                "supportedFanDurations", int
            ),  # The fan mode durations that the thermostat supports
            fan_mode=self._get_special("fanMode", self.FanMode),
            supports_heat=self._get_bool(
                "supportsHeatMode"
            ),  # Whether the thermostat supports the heat temp mode.
            supports_heat_aux=self._get_bool(
                "supportsAuxHeatMode"
            ),  # Whether the thermostat supports the aux heat temp mode.
            supports_cool=self._get_bool(
                "supportsCoolMode"
            ),  # Whether the thermostat supports the cool temp mode.
            supports_auto=self._get_bool(
                "supportsAutoMode"
            ),  # Whether the thermostat supports the auto temp mode.
            supports_setpoints=self._get_bool(
                "supportsSetpoints"
            ),  # Whether the thermostat supports setpoints.
            setpoint_buffer=self._get_float(
                "autoSetpointBuffer"
            ),  # The minimum buffer between the heat and cool setpoints.
            min_heat_setpoint=self._get_float(
                "minHeatSetpoint"
            ),  # The min valid heat setpoint.
            min_cool_setpoint=self._get_float(
                "minCoolSetpoint"
            ),  # The min valid cool setpoint.
            max_heat_setpoint=self._get_float(
                "maxHeatSetpoint"
            ),  # The max valid heat setpoint.
            max_cool_setpoint=self._get_float(
                "maxCoolSetpoint"
            ),  # The max valid cool setpoint.
            heat_setpoint=(_heat_setpoint - (_setpoint_offset or 0))
            if ((_heat_setpoint := self._get_float("heatSetpoint")) is not None)
            else _heat_setpoint,  # The current heat setpoint. Needs to be offset by setpointOffset.
            cool_setpoint=(_cool_setpoint - (_setpoint_offset or 0))
            if ((_cool_setpoint := self._get_float("coolSetpoint")) is not None)
            else _cool_setpoint,  # The current cool setpoint. Needs to be offset by setpointOffset.
            supports_humidity=self._get_bool(
                "supportsHumidity"
            ),  # Whether the device supports humidity.
            humidity=self._get_int(
                "humidityLevel"
            ),  # The current humidity level reported by the device
            supports_schedules=self._get_bool(
                "supportsSchedules"
            ),  # Whether the thermostat supports schedules.
            supports_schedules_smart=self._get_bool(
                "supportsSmartSchedules"
            ),  # Whether the thermostat supports the Smart Schedule mode.
            schedule_mode=self._get_special(
                "scheduleMode", self.ScheduleMode
            ),  # The schedule mode.
        )

    async def async_set_attribute(
        self,
        state: DeviceState | None = None,
        fan: tuple[FanMode, int] | None = None,  # int = duration
        cool_setpoint: float | None = None,
        heat_setpoint: float | None = None,
        schedule_mode: ScheduleMode | None = None,
    ) -> None:
        """Send turn on command with optional brightness."""

        msg_body: dict[str, float | int] = {}

        # Make sure we're only being asked to set one attribute at a time.
        if (
            attrib_list := [state, fan, cool_setpoint, heat_setpoint, schedule_mode]
        ).count(None) < len(attrib_list) - 1:
            raise UnexpectedDataStructure

        # Build the request body.
        if state:
            msg_body = {"desiredState": state.value}
        elif fan:
            msg_body = {
                "desiredFanMode": self.FanMode(fan[0]).value,
                "desiredFanDuration": 0
                if self.FanMode(fan[0]) == self.FanMode.AUTO
                else fan[1],
            }
        elif cool_setpoint:
            msg_body = {"desiredCoolSetpoint": cool_setpoint}
        elif heat_setpoint:
            msg_body = {"desiredHeatSetpoint": heat_setpoint}
        elif schedule_mode:
            msg_body = {"desiredScheduleMode": schedule_mode.value}

        # Send
        await self._send_action_callback(
            device_type=DeviceType.THERMOSTAT,
            event=self.Command.SET_STATE,
            device_id=self.id_,
            msg_body=msg_body,
        )
