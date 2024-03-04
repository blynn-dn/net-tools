from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, RootModel, Field


# region common Model
class Status(BaseModel):
    value: str
    label: str
# endregion common Model


# region Device Model
class Manufacturer(BaseModel):
    id: int
    url: str
    display: str
    name: str
    slug: str


class DeviceType(BaseModel):
    id: int
    url: str
    display: str
    manufacturer: Manufacturer
    model: str
    slug: str


class Role(BaseModel):
    id: int
    url: str
    display: str
    name: str
    slug: str


class DeviceRole(BaseModel):
    id: int
    url: str
    display: str
    name: str
    slug: str


class Platform(BaseModel):
    id: int
    url: str
    display: str
    name: str
    slug: str


class Site(BaseModel):
    id: int
    url: str
    display: str
    name: str
    slug: str


class CustomFields(BaseModel):
    port: int


class DeviceData(BaseModel):
    id: int
    url: str
    display: str
    name: str
    device_type: DeviceType
    role: Role
    device_role: DeviceRole
    tenant: Any
    platform: Platform
    serial: str
    asset_tag: Any
    site: Site
    location: Any
    rack: Any
    position: Any
    face: Any
    latitude: Any
    longitude: Any
    parent_device: Any
    status: Status
    airflow: Any
    primary_ip: Any
    primary_ip4: Any
    primary_ip6: Any
    oob_ip: Any
    cluster: Any
    virtual_chassis: Any
    vc_position: Any
    vc_priority: Any
    description: str
    comments: str
    config_template: Any
    local_context_data: Any
    tags: List
    custom_fields: CustomFields
    created: str
    last_updated: str
    console_port_count: int
    console_server_port_count: int
    power_port_count: int
    power_outlet_count: int
    interface_count: int
    front_port_count: int
    rear_port_count: int
    device_bay_count: int
    module_bay_count: int
    inventory_item_count: int


class DevicePrechange(BaseModel):
    created: str
    description: str
    comments: str
    local_context_data: Any
    config_template: Any
    device_type: int
    role: int
    tenant: Any
    platform: int
    name: str
    serial: str
    asset_tag: Any
    site: int
    location: Any
    rack: Any
    position: Any
    face: str
    status: str
    airflow: str
    primary_ip4: Any
    primary_ip6: Any
    oob_ip: Any
    cluster: Any
    virtual_chassis: Any
    vc_position: Any
    vc_priority: Any
    latitude: Any
    longitude: Any
    console_port_count: int
    console_server_port_count: int
    power_port_count: int
    power_outlet_count: int
    interface_count: int
    front_port_count: int
    rear_port_count: int
    device_bay_count: int
    module_bay_count: int
    inventory_item_count: int
    custom_fields: CustomFields
    tags: List


class DevicePostchange(BaseModel):
    created: str
    last_updated: str
    description: str
    comments: str
    local_context_data: Any
    config_template: Any
    device_type: int
    role: int
    tenant: Any
    platform: int
    name: str
    serial: str
    asset_tag: Any
    site: int
    location: Any
    rack: Any
    position: Any
    face: str
    status: str
    airflow: str
    primary_ip4: Any
    primary_ip6: Any
    oob_ip: Any
    cluster: Any
    virtual_chassis: Any
    vc_position: Any
    vc_priority: Any
    latitude: Any
    longitude: Any
    console_port_count: int
    console_server_port_count: int
    power_port_count: int
    power_outlet_count: int
    interface_count: int
    front_port_count: int
    rear_port_count: int
    device_bay_count: int
    module_bay_count: int
    inventory_item_count: int
    custom_fields: CustomFields
    tags: List
# endregion Device Model


# region IP Address Model
class Family(BaseModel):
    value: int
    label: str


class IpAddressData(BaseModel):
    id: int
    url: str
    display: str
    family: Family
    address: str
    vrf: Any
    tenant: Any
    status: Status
    role: Any
    assigned_object_type: Any
    assigned_object_id: Any
    assigned_object: Any
    nat_inside: Any
    nat_outside: List
    dns_name: str
    description: str
    comments: str
    tags: List
    custom_fields: Dict[str, Any]
    created: str
    last_updated: str


class IpAddressChange(BaseModel):
    created: str
    description: str
    comments: str
    address: str
    vrf: Any
    tenant: Any
    status: str
    role: str
    assigned_object_type: Any
    assigned_object_id: Any
    nat_inside: Any
    dns_name: str
    custom_fields: Dict[str, Any]
    tags: List

# endregion IP Address Model


class Snapshots(BaseModel):
    # use an alias to support snake case
    pre_change: IpAddressChange | DevicePrechange | None = Field(alias='prechange') # noqa
    post_change: IpAddressChange | DevicePostchange | None = Field(alias='postchange') # noqa


class EventEnum(str, Enum):
    updated = 'updated'
    created = 'created'
    deleted = 'deleted'


class ModelEnum(str, Enum):
    device = 'device'
    ipaddress = 'ipaddress'


class Event(BaseModel):
    # use an alias to support a snake case and rename `event` to `event_type`
    event_type: EventEnum = Field(alias='event')
    timestamp: str
    model: ModelEnum
    username: str
    request_id: str
    data: IpAddressData | DeviceData
    snapshots: Snapshots


class EventRoot(RootModel):
    # The JSON payload is typically a root type -- which simply means the JSON is enclosed with {}
    # Pydantic's RootModel will simply apply a leaf with name 'root' to the payload
    root: Event
