"""GarageDoor websocket message handler."""

from __future__ import annotations

import logging

from pyalarmdotcomajax.devices.garage_door import GarageDoor
from pyalarmdotcomajax.websockets.const import EventType
from pyalarmdotcomajax.websockets.handler import BaseWebSocketHandler
from pyalarmdotcomajax.websockets.messages import (
    EventMessage,
    StatusChangeMessage,
    WebSocketMessage,
)

log = logging.getLogger(__name__)


class GarageDoorWebSocketHandler(BaseWebSocketHandler):
    """Base class for device-type-specific websocket message handler."""

    SUPPORTED_DEVICE_TYPE = GarageDoor

    EVENT_STATE_MAP = {
        EventType.Opened: GarageDoor.DeviceState.OPEN,
        EventType.Closed: GarageDoor.DeviceState.CLOSED,
    }

    async def process_message(self, message: WebSocketMessage) -> None:
        """Handle websocket message."""

        # www.alarm.com\web\system\assets\customer-ember\websockets\handlers\garage-doors.ts

        if type(message.device) != GarageDoor:
            return

        match message:
            case StatusChangeMessage():
                await message.device.handle_async_state_change_finished(message.new_state)

            case EventMessage():
                match message.event_type:
                    case EventType.Opened | EventType.Closed:
                        await message.device.handle_async_state_change_finished(
                            self.EVENT_STATE_MAP[message.event_type]
                        )
                    case _:
                        log.debug(
                            f"Support for event {message.event_type} ({message.event_type_id}) not yet implemented"
                            f" by {self.SUPPORTED_DEVICE_TYPE.__name__}."
                        )

            case _:
                log.debug(
                    f"Support for {type(message)} not yet implemented by {self.SUPPORTED_DEVICE_TYPE.__name__}."
                )
