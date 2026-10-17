from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_OPNSENSE_ENTRY_ID, DOMAIN
from .coordinator import TopTalkersCoordinator

PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    source = hass.config_entries.async_get_entry(entry.data[CONF_OPNSENSE_ENTRY_ID])
    if source is None or source.state.value != "loaded" or source.runtime_data is None:
        return False
    client = source.runtime_data.opnsense_client
    coordinator = TopTalkersCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

