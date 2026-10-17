from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, MIN_SCAN_INTERVAL

class TopTalkersCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: Any) -> None:
        self.client = client
        interval = max(MIN_SCAN_INTERVAL, int(entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)))
        super().__init__(hass, logger=__import__("logging").getLogger(__name__), name=DOMAIN, update_interval=timedelta(seconds=interval))

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            payload = await self.client._safe_dict_get("/api/diagnostics/traffic/top/lan,wan")
        except Exception as err:
            raise UpdateFailed(f"OPNsense Top-Talkers konnten nicht gelesen werden: {err}") from err
        result: dict[str, Any] = {}
        for interface in ("lan", "wan"):
            block = payload.get(interface, {}) if isinstance(payload, dict) else {}
            records = block.get("records", []) if isinstance(block, dict) else []
            safe = []
            for row in records[:20] if isinstance(records, list) else []:
                if not isinstance(row, dict):
                    continue
                safe.append({key: row.get(key) for key in (
                    "address", "rname", "rate_bits_in", "rate_bits_out", "rate_bits",
                    "rate_in", "rate_out", "rate", "cumulative_bytes_in",
                    "cumulative_bytes_out", "cumulative_in", "cumulative_out")})
            result[interface] = safe
        return result

