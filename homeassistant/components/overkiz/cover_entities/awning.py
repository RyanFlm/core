"""Support for Overkiz awnings."""
from __future__ import annotations

from typing import Any, cast

from pyoverkiz.enums import OverkizCommand, OverkizState

from homeassistant.components.cover import (
    ATTR_POSITION,
    CoverDeviceClass,
    CoverEntityFeature,
)

from .generic_cover import COMMANDS_STOP, OverkizGenericCover


class Awning(OverkizGenericCover):
    """Representation of an Overkiz awning."""

    _attr_device_class = CoverDeviceClass.AWNING

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        supported_features: int = super().supported_features

        if self.executor.has_command(OverkizCommand.SET_DEPLOYMENT):
            supported_features |= CoverEntityFeature.SET_POSITION

        if self.executor.has_command(OverkizCommand.DEPLOY):
            supported_features |= CoverEntityFeature.OPEN

            if self.executor.has_command(*COMMANDS_STOP):
                supported_features |= CoverEntityFeature.STOP

        if self.executor.has_command(OverkizCommand.UNDEPLOY):
            supported_features |= CoverEntityFeature.CLOSE

        return supported_features

    @property
    def current_cover_position(self) -> int | None:
        """
        Return current position of cover.

        None is unknown, 0 is closed, 100 is fully open.
        """
        current_position = self.executor.select_state(OverkizState.CORE_DEPLOYMENT)
        if current_position is not None:
            return cast(int, current_position)

        return None

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Move the cover to a specific position."""
        await self.executor.async_execute_command(
            OverkizCommand.SET_DEPLOYMENT, kwargs[ATTR_POSITION]
        )

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        await self.executor.async_execute_command(OverkizCommand.DEPLOY)

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        await self.executor.async_execute_command(OverkizCommand.UNDEPLOY)
