#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
"""
   Nagios/Icinga plugin to check available ip's.

   This corresponds to the output of 'openstack ip availabilities show'.
"""

import openstacknagios.openstacknagios as osnag
import keystoneclient.v2_0.client as ksclient
from neutronclient.neutron import client

class NeutronNetworkipavailabilities(osnag.Resource):
    """
    Determines the number of total and used neutron network ip's

    """

    def __init__(self, args=None):
        self.network_uuid = args.network_uuid
        self.openstack = self.get_openstack_vars(args=args)
        osnag.Resource.__init__(self)

    def probe(self):
        try:
            neutron = client.Client('2.0',
                                    session  = self.get_session(),
                                    ca_cert  = self.openstack['cacert'],
                                    insecure = self.openstack['insecure'])
        except Exception as e:
            self.exit_error('cannot load ' + str(e))

        try:
            result=neutron.show_network_ip_availability(self.network_uuid)
        except Exception as e:
            self.exit_error(str(e))

        net_ip = result['network_ip_availability'] 

        stati=dict(total=0, used=0)
        stati['total'] = net_ip['total_ips']
        stati['used'] = net_ip['used_ips']

        for r in stati.keys():
            yield osnag.Metric(r, stati[r], min=0)

@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('-w', '--warn', metavar='RANGE', default='0:200',
                      help='return warning if number of used ip\'s is outside range (default: 0:200, warn if more than 200 are used)')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='0:230',
                      help='return critical if number of used ip\'s is outside RANGE (default 0:230, critical if more than 230 are used)')
    argp.add_argument('-n', '--network_uuid', required=True, help='network_uuid to check')
    args = argp.parse_args()

    check = osnag.Check(
        NeutronNetworkipavailabilities(args=args),
        osnag.ScalarContext('total'),
        osnag.ScalarContext('used', args.warn, args.critical),
        osnag.Summary(show=['total','used'])
        )
    check.main(verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()

