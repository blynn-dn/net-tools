import netaddr
import dns.reversename
import dns.name
import dns.update
import dns.query
import dns.rcode

from app.models import CRUDActionEnum
from app.models.netbox import Event, ModelEnum, EventEnum
from app.provisioning import BaseProvisioning

IP6_ARPA = dns.name.from_text("ip6.arpa")


class DNSTools(BaseProvisioning):
    def __init__(self, event: Event):
        super().__init__(event)

        print(self._event.snapshots)
        print(self._event.snapshots.pre_change)
        print(self._event.snapshots.post_change)

        # helpers
        self._pre_ip_address = netaddr.IPNetwork(self._pre_change.address.split('/')[0]) if self._pre_change else None
        self._post_ip_address = netaddr.IPAddress(self._post_change.address.split('/')[0]) if self._post_change else None

    def process(self):
        """
        Process the IP Address change event.

        Notes:
            The logic might be simplified by using the pre_change and post_change data.  For example:
            - on deleted - only the pre_change data is populated and post_change is None
            - on created - only the post_change data is populated
            - on updated - both pre and post are populated, accordingly
            I used the `event_type` for determining the logic.

        """
        if self._event.model.value != ModelEnum.ipaddress:
            raise ValueError(f"{self._event.model.value} not supported")

        print(f"event_type: {self._event.event_type}")
        print(f"pre: {self._pre_change}")
        print(f"post: {self._post_change}")

        if self._event.event_type.value == EventEnum.deleted:
            # delete using the pre change data as the post change data is None
            self._update(CRUDActionEnum.delete, self._pre_ip_address, self._pre_change.dns_name or None)

        elif self._event.event_type.value == EventEnum.created:
            # add/create using the post change data as the pre change data is None
            self._update(CRUDActionEnum.create, self._post_ip_address, self._post_change.dns_name or None)

        elif self._event.event_type.value == EventEnum.updated:
            # remove the old and add the new
            self._update(CRUDActionEnum.delete, self._pre_ip_address, self._pre_change.dns_name)
            self._update(CRUDActionEnum.create, self._post_ip_address, self._post_change.dns_name)

        else:
            raise NotImplementedError(f"{self._event.event_type.value} not supported")

    def _update(self, action: CRUDActionEnum, ip_address, dns_name):
        """
        Performs the actual action -- Note that currently this method simply logs the intended action
        Args:
            action: (CRUDActionEnum) - create, update or delete action
            ip_address: (netaddr.IPAddress) - IP Address
            dns_name: (str) DNS Name

        """
        rev_name = dns.reversename.from_address(str(ip_address))
        rr_type = "AAAA" if rev_name.is_subdomain(IP6_ARPA) else "A"
        rr_name = dns.name.from_text(dns_name) if dns_name else ''

        print(f"performing {action.value}: {rev_name}:{rr_type}:{rr_name}")

        # add the actual acton here ---
