# Changes

## V0.3.0

* Major refactoring with widespread breaking changes.
* Added "controller extensions" to let controller retrieve data from additional endpoints.
* Added support for Skybell HD video doorbells (settings only, not video).
* Created testing framework and started building tests.

## v0.2.10 - 2022-04025

* Fixes crash when encountering unknown device type with missing permissions.
* Added more unsupported device types.
* Refactoring. Consolidated similar functions.

## v0.2.9 - 2022-04-22

* No longer tries to log back in when Timeout / Cancelled / ClientError exceptions encountered. Will bubble up and leave to caller to handle.

## v0.2.8 - 2022-04-16

* Converted major debug messages to errors.

## v0.2.7 - 2022-04-09

* Added debug data property for all entities.

## v0.2.6 - 2022-04-08

* Added support for lights that don't report state.
* Added previously unmapped device states.

## v0.2.5 - 2022-04-08

* Added read_only attribute to controllable devices.

## v0.2.4 - 2022-04-07

* Add freeze sensors.
* Fixed night arming.
* Started adding Alarm.com API reference data for future enhancements.

## v0.2.3 - 2022-04-06

* Fixed CLI asyncio error for Windows systems.

## v0.2.2 - 2022-04-05

* [BREAKING] Moved action functions from controller to individual devices.
* Added support for lights.
* Fixed OTP login workflow in CLI.
* Removed arming preferences (bypass - etc.) from controller. Now - preferences must be submitted on every arm request.

## v0.2 - v0.2.1

* (See release notes.)

## v0.1.13 - 2021-12-26

* Add detailed sensor attributes
* Add lock support

## v0.1.12 - 2021-12-13

* Adapt to sensorText rename in sensor endpoint json

## v0.1.11 - 2021-03-31

* Add armed night state

## v0.1.10 - 2020-12-22

* Fix login problem with refactor from 0.1.7

## v0.1.8 - 2020-12-15

* Add 2FA cookie

## v0.1.7 - 2020-12-13

* Add AlarmdotcomProtection1 and refactor classes
* Add Garage Doors status

## v0.1.6 - 2020-11-16

* Add thermostat status for ADT

## v0.1.5 - 2020-11-16

* Add thermostat status

## v0.1.4 - 2020-11-14

* Add AlarmdotcomADT for ADT portal login

## v0.1.3 - 2020-09-02

* Omit sending arming parameters if False. Only attempt relogin on HTTP 403 error.

## v0.1.2 - 2020-03-22

* Added option for silent arming
* Added different stay and away treatment for forcebypass/noentrydelay/silentarming
* Changed arming function name to use stay instead of home - sticking with ADC convention

## v0.1.1 - 2020-03-18

* Added sensor status

## v0.1.0 - 2020-03-18

* Initial release.