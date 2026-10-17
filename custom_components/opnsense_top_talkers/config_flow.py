from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_OPNSENSE_ENTRY_ID, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, MIN_SCAN_INTERVAL

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        entries = self.hass.config_entries.async_entries("opnsense")
        choices = {entry.entry_id: entry.title for entry in entries}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_OPNSENSE_ENTRY_ID])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f"{choices[user_input[CONF_OPNSENSE_ENTRY_ID]]} Top Talkers", data=user_input)
        schema = vol.Schema({
            vol.Required(CONF_OPNSENSE_ENTRY_ID): vol.In(choices),
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL)),
        })
        return self.async_show_form(step_id="user", data_schema=schema)

