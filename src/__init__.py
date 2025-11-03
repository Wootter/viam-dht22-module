"""
This file registers the model with the Python SDK.
"""

from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .dht22 import dht22

Registry.register_resource_creator(Sensor.SUBTYPE, dht22.MODEL, ResourceCreatorRegistration(dht22.new, dht22.validate))
