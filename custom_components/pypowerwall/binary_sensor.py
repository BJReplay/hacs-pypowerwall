"""Binary sensor platform for pypowerwall."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PypowerwallConfigEntry
from .coordinator import PowerwallDataUpdateCoordinator
from .entity import PowerwallEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PypowerwallConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up pypowerwall binary sensors from a config entry."""
    coordinator = entry.runtime_data
    async_add_entities(
        [
            PowerwallGridConnectedBinarySensor(coordinator),
            PowerwallBatteryCalibrationBinarySensor(coordinator),
        ]
    )


class PowerwallGridConnectedBinarySensor(PowerwallEntity, BinarySensorEntity):
    """Whether the Powerwall gateway is currently connected to the grid."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_translation_key = "grid_connected"

    def __init__(self, coordinator: PowerwallDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._din}_grid_connected"

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.grid_connected


class PowerwallBatteryCalibrationBinarySensor(PowerwallEntity, BinarySensorEntity):
    """On while the gateway reports the BatteryCalibration alert.

    Disabled by default: the alert's exact meaning is undocumented upstream, so
    this only mirrors whether it is currently active.
    """

    _attr_translation_key = "battery_calibration"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(self, coordinator: PowerwallDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._din}_battery_calibration"

    @property
    def is_on(self) -> bool:
        return "BatteryCalibration" in self.coordinator.data.alerts
