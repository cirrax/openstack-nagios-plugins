#
#    Copyright (C) 2016  Jordan Tardif  http://github.com/jordant
#    Jordan Tardif <jordan@dreamhost.com>
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
   Nagios plugin to check router status. Router status is an extended feature
   provided to neutron via astara. https://github.com/openstack/astara . This
   plugin will **NOT** work for neutron servers without astara extensions.

   This corresponds to the output of 'neutron router-list -c id -c status'.
"""

import openstacknagios.openstacknagios as osnag

from neutronclient.neutron import client


class NeutronRouters(osnag.Resource):
    """
    Determines the number down/build/active routers

    """

    def __init__(self, args=None):
        self.openstack = self.get_openstack_vars(args=args)
        osnag.Resource.__init__(self)

    def probe(self):
        try:
            neutron = client.Client('2.0',
                                    session=self.get_session(),
                                    ca_cert=self.openstack['cacert'],
                                    insecure=self.openstack['insecure'])
        except Exception as e:
            self.exit_error('cannot load ' + str(e))

        try:
            result = neutron.list_routers()
        except Exception as e:
            self.exit_error(str(e))

        stati = dict(active=0, down=0, build=0)

        for router in result['routers']:
            if router['status'] == 'ACTIVE':
                stati['active'] += 1
            if router['status'] == 'DOWN':
                stati['down'] += 1
            if router['status'] == 'BUILD':
                stati['build'] += 1

        for r in stati.keys():
            yield osnag.Metric(r, stati[r], min=0)


@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('-w', '--warn', metavar='RANGE', default='0:',
                      help="""return warning if number of down routers is
                      greater than (default: 0)""")
    argp.add_argument('-c', '--critical', metavar='RANGE', default='10:',
                      help="""return critical if number of down routers is
                      greater than (default: 10) """)
    argp.add_argument('--warn_build', metavar='RANGE', default='0:',
                      help="""return warning if number of building routers is
                      greater than (default: 0)""")
    argp.add_argument('--critical_build', metavar='RANGE', default='10:',
                      help="""return critical if number of building routers
                      is greater than (default: 10) """)

    args = argp.parse_args()

    check = osnag.Check(
        NeutronRouters(args=args),
        osnag.ScalarContext('active'),
        osnag.ScalarContext('down', args.warn, args.critical),
        osnag.ScalarContext('build', args.warn_build, args.critical_build),
        osnag.Summary(show=['active', 'down', 'build'])
        )
    check.main(verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()

