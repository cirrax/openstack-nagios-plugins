#
#    Copyright (C) 2014  Cirrax GmbH  http://www.cirrax.com
#    Benedikt Trefzer <benedikt.trefzer@cirrax.com>
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
   Nagios/Icinga plugin to check floating ip's.
   Counts the assigned ip's (= used + unused).

   This corresponds to the output of 'neutron floatingip-list'.
"""

import openstacknagios.openstacknagios as osnag

import json

from neutronclient.neutron import client



class NeutronFloatingips(osnag.Resource):
    """
    Determines the number of assigned (used and unused) floating ip's

    """

    def __init__(self, args=None):
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
           result=neutron.list_floatingips()
        except Exception as e:
           self.exit_error(str(e))

        stati=dict(assigned=0, used=0)

        for floatingip in result['floatingips']:
           stati['assigned'] += 1
           if floatingip['fixed_ip_address']:
             stati['used'] += 1

        for r in stati.keys():
           yield osnag.Metric(r, stati[r], min=0)


@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('-w', '--warn', metavar='RANGE', default='0:200',
                      help='return warning if number of assigned floating ip\'s is outside range (default: 0:200, warn if more than 200 are used)')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='0:230',
                      help='return critical if number of assigned floating ip\'s is outside RANGE (default 0:230, critical if more than 230 are used)')

    args = argp.parse_args()

    check = osnag.Check(
        NeutronFloatingips(args=args),
        osnag.ScalarContext('assigned', args.warn, args.critical),
        osnag.ScalarContext('used'),
        osnag.Summary(show=['assigned','used'])
        )
    check.main(verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()

