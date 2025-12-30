"""Config flow for hoboken_path."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_NAME

from .const import DOMAIN


class PathConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PATH trains."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            # Create a simple config entry
            # For now, monitor all stations
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, "PATH Trains"),
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default="PATH Trains"): str,
                }
            ),
        )
