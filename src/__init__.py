"""
This file registers the model with the Python SDK.
"""

import asyncio
from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.module.module import Module

from .dht22 import dht22

async def main():
    """Start the module"""
    Registry.register_resource_creator(
        Sensor.API,
        dht22.MODEL,
        ResourceCreatorRegistration(dht22.new, dht22.validate)
    )
    await Module.run_from_registry()

if __name__ == "__main__":
    asyncio.run(main())