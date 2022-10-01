from homeassistant.core import HomeAssistant
import petsafe
from . import SensorEntities
from .const import DOMAIN

from . import PetSafeCoordinator
from homeassistant.core import HomeAssistant


from datetime import timedelta

SCAN_INTERVAL = timedelta(seconds=60)


async def async_setup_entry(hass: HomeAssistant, config, add_entities):
    coordinator: PetSafeCoordinator = hass.data[DOMAIN]
    api: petsafe.PetSafeClient = coordinator.api

    feeders = await hass.async_add_executor_job(petsafe.devices.get_feeders, api)
    litterboxes = await hass.async_add_executor_job(
        petsafe.devices.get_litterboxes, api
    )

    entities = []
    for feeder in feeders:
        entities.append(
            SensorEntities.PetSafeFeederSensorEntity(
                hass=hass,
                name="Battery Level",
                device_class="battery",
                device_type="battery",
                device=feeder,
                coordinator=coordinator,
            )
        )
        entities.append(
            SensorEntities.PetSafeFeederSensorEntity(
                hass=hass,
                name="Last Feeding",
                device_type="last_feeding",
                device_class="timestamp",
                device=feeder,
                coordinator=coordinator,
            )
        )
        entities.append(
            SensorEntities.PetSafeFeederSensorEntity(
                hass=hass,
                name="Food Level",
                device_type="food_level",
                device=feeder,
                coordinator=coordinator,
                icon="mdi:bowl",
            )
        )
    for litterbox in litterboxes:
        entities.append(
            SensorEntities.PetSafeLitterboxSensorEntity(
                hass=hass,
                name="Rake Counter",
                device_type="rake_counter",
                device=litterbox,
                coordinator=coordinator,
                icon="mdi:rake",
            )
        )
    add_entities(entities)