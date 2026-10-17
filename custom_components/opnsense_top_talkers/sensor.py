from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import TopTalkersCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: TopTalkersCoordinator = entry.runtime_data
    async_add_entities([TopTalkersSensor(coordinator, entry, "lan"), TopTalkersSensor(coordinator, entry, "wan")])

class TopTalkersSensor(CoordinatorEntity[TopTalkersCoordinator], SensorEntity):
    _attr_icon = "mdi:chart-bar"
    _attr_has_entity_name = True

    def __init__(self, coordinator: TopTalkersCoordinator, entry: ConfigEntry, interface: str) -> None:
        super().__init__(coordinator)
        self.interface = interface
        self._attr_unique_id = f"{entry.entry_id}_{interface}"
        self._attr_name = f"{interface.upper()} Top Talkers"

    @property
    def native_value(self) -> int:
        return len(self.coordinator.data.get(self.interface, []))

    @property
    def extra_state_attributes(self):
        return {"interface": self.interface, "records": self.coordinator.data.get(self.interface, [])}

