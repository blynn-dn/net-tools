"""
This is simple example of how to receive a webhook event from netbox
"""
import logging

from fastapi import APIRouter, Depends
from app.dependencies import get_x_hook_signature_header
import napalm

from nornir import InitNornir
from nornir.core.inventory import Host
from nornir_napalm.plugins.tasks import napalm_get

# init nornir
# nr = InitNornir(config_file="config/config.yaml")
nr = InitNornir(
    inventory={
        "plugin": "NetBoxInventory2",
        "options": {
            "nb_url": "http://localhost:8081",
            "nb_token": "d58c40cec78a309b9bbf2cb9251e19906bb23973",
            "ssl_verify": False,
        }
    }
)

logger = logging.getLogger(__name__)

# create /webhook API router endpoint
devices_ep = APIRouter(
    prefix='/devices',
    #d ependencies=[Depends(get_x_hook_signature_header)],
    tags=['devices'],
    responses={404: {'description': 'Not Found'}}
)

drivers = {}


def get_device(host: Host) -> napalm.base.base.NetworkDriver:
    optional_args = {}
    hostname = host.hostname

    port = host.data.get('custom_fields', {}).get('port', 443)

    if host.platform == 'eos':
        if host.data.get('device_type', {}).get('slug') == 'ceoslab':
            optional_args['port'] = port
            hostname = 'localhost'

        print(hostname, optional_args)

    if host.platform not in drivers:
        driver = napalm.get_network_driver(host.platform)
        drivers[host.platform] = driver
    else:
        driver = drivers.get(host.platform)

    return driver(hostname=hostname, optional_args=optional_args, username="arista", password="arista")


def call_napalm_function(hostname: str, function: str, **kwargs):
    try:
        host = nr.inventory.hosts.get(hostname)
        if not host:
            return {'success': False, 'error_message': f"host: {hostname} not found in inventory"}

        print(f"host: {host.hostname}, {host.data.get('device_type', {}).get('slug')}")
        device = get_device(host)
        print(device)
        device.open()

        method = getattr(device, function)
        if not method:
            return {'success': False, 'error_message': f"method: {function} is not supported"}

        print(f"calling: {method} with {kwargs}")
        return method(**kwargs)
    except Exception as ex:
        return {'success': False, 'error_message': ex}


@devices_ep.get('/devices/{hostname}/facts')
async def get_device_facts(hostname: str):
    return call_napalm_function(hostname, 'get_facts')


@devices_ep.get('/devices/{hostname}/interfaces')
async def get_device_interfaces(hostname: str):
    return call_napalm_function(hostname, 'get_interfaces')


@devices_ep.get('/devices/{hostname}/interfaces_counters')
async def get_device_interfaces_counters(hostname: str):
    return call_napalm_function(hostname, 'get_interfaces_counters')


@devices_ep.get('/devices/{hostname}/environment')
async def get_device_environment(hostname: str):
    return call_napalm_function(hostname, 'get_environment')


@devices_ep.get('/devices/{hostname}/bpg_config')
async def get_device_bgp_config(hostname: str, group: str = '', neighbor: str = ''):
    return call_napalm_function(hostname, 'get_bgp_config', **{'group': group, 'neighbor': neighbor})


@devices_ep.get('/devices/{hostname}/bpg_neighbors_detail')
async def get_device_bgp_neighbor_detail(hostname: str, neighbor: str = ''):
    return call_napalm_function(hostname, 'get_bgp_neighbors_detail', **{'neighbor_address': neighbor})


@devices_ep.get('/devices/{hostname}/optics')
async def get_device_optics(hostname: str):
    return call_napalm_function(hostname, 'get_optics')
