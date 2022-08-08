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
  Nagios/Icinga plugin to check running cinder agents/services.

  This corresponds to the output of 'cinder service-list'.
"""

import openstacknagios.openstacknagios as osnag

from cinderclient.client import Client


class CinderServices(osnag.Resource):
    """
    Determines the status of the cinder agents/services.
    """

    def __init__(self, binary=None, host=None, args=None):
        self.binary = binary
        self.host   = host
        self.openstack = self.get_openstack_vars(args=args)
        osnag.Resource.__init__(self)

    def probe(self):

        try:
           cinder=Client( '3',
                          session  = self.get_session(),
                          insecure = self.openstack['insecure'],
                          cacert   = self.openstack['cacert'],
                        )
        except Exception as e:
           self.exit_error(str(e))

        try:
           result=cinder.services.list()
        except Exception as e:
           self.exit_error(str(e))

        stati=dict(up=0, disabled=0, down=0, total=0)

        for agent in result:
           if (self.host == None or self.host == agent.host) and (self.binary == None or self.binary == agent.binary):
                stati['total'] += 1
                if agent.status == 'enabled' and agent.state =='up':
                     stati['up'] += 1
                elif agent.status == 'disabled':
                     stati['disabled'] += 1
                else:
                     stati['down'] += 1

        for r in stati.keys():
           yield osnag.Metric(r, stati[r], min=0)

@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('-w', '--warn', metavar='RANGE', default='0:',
                      help='return warning if number of up agents is outside RANGE (default: 0:, never warn)')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='0:',
                      help='return critical if number of up agents is outside RANGE (default 1:, never critical)')

    argp.add_argument('--warn_disabled', metavar='RANGE', default='@1:',
                      help='return warning if number of disabled agents is outside RANGE (default: @1:, warn if any disabled agents')
    argp.add_argument('--critical_disabled', metavar='RANGE', default='0:',
                      help='return critical if number of disabled agents is outside RANGE (default: 0:, never critical')
    argp.add_argument( '--warn_down', metavar='RANGE', default='0:',
                      help='return warning if number of down agents is outside RANGE (default: 0:, never warn)')
    argp.add_argument( '--critical_down', metavar='RANGE', default='0',
                      help='return critical if number of down agents is outside RANGE (default: 0, always critical if any')

    argp.add_argument('--binary', 
                    dest='binary',
                    default=None,
                    help='filter agent binary')
    argp.add_argument('--host', 
                    dest='host',
                    default=None,
                    help='filter hostname')

    args = argp.parse_args()

    check = osnag.Check(
        CinderServices(args=args, host=args.host, binary=args.binary),
        osnag.ScalarContext('up', args.warn, args.critical),
        osnag.ScalarContext('disabled', args.warn_disabled, args.critical_disabled),
        osnag.ScalarContext('down', args.warn_down, args.critical_down),
        osnag.ScalarContext('total', '0:', '@0'),
        osnag.Summary(show=['up','disabled','down','total'])
        )
    check.main(verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()


