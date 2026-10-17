# OPNsense Top Talkers for Home Assistant

Companion integration for `travisghansen/hass-opnsense`. It reuses the already-loaded OPNsense client and exposes LAN/WAN top-talker records as sensor attributes.

The OPNsense endpoint starts `iftop` internally. The integration enforces a 30-second minimum interval and defaults to 60 seconds to avoid the severe throughput impact reported for rapid polling.

Install as a HACS custom integration, restart Home Assistant, then add **OPNsense Top Talkers** and select the existing OPNsense entry.
