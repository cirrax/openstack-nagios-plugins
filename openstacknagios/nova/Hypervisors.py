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
    Nagios/Icinga plugin to check nova hypervisors.
    This corresponds to the output of 'nova hypervisor-stats'
"""

from novaclient.client import Client

import openstacknagios.openstacknagios as osnag

class NovaHypervisors(osnag.Resource):
    """
    Determines the status of the nova hypervisors.

    """

    def __init__(self, host=None, args=None):
        self.host   = host
        self.openstack = self.get_openstack_vars(args=args)

    def probe(self):
        try:
           nova=Client('2',
                       session  = self.get_session(),
                       cacert   = self.openstack['cacert'],
                       insecure = self.openstack['insecure'])

        except Exception as e:
           self.exit_error(str(e))

        try:
           if self.host:
              result=nova.hypervisors.get(nova.hypervisors.find(hypervisor_hostname=self.host))
           else:
              result=nova.hypervisors.statistics()
        except Exception as e:
           self.exit_error(str(e))

        yield osnag.Metric('vcpus_used',result.vcpus_used, min=0, max=result.vcpus )
        yield osnag.Metric('vcpus_percent',100*result.vcpus_used/result.vcpus, min=0, max=100 )
        yield osnag.Metric('memory_used',result.memory_mb_used, min=0, max=result.memory_mb )
        yield osnag.Metric('memory_percent',100*result.memory_mb_used/result.memory_mb, min=0, max=100 )
        yield osnag.Metric('running_vms',result.running_vms, min=0 )

@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('-H', '--host', default=None,
                      help='hostname where the hypervisor is running if not defined (default), summary of all hosts is used')

    argp.add_argument('-w', '--warn', metavar='RANGE', default='0:',
                      help='return warning if number of running vms is outside RANGE (default: 0:, never warn)')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='0:',
                      help='return critical if number of running vms is outside RANGE (default 0:, never critical)')

    argp.add_argument('--warn_memory', metavar='RANGE', default='0:',
                      help='return warning if number of disabled agents is outside RANGE (default: 0:, never warn')
    argp.add_argument('--critical_memory', metavar='RANGE', default='0:',
                      help='return critical if number of disabled agents is outside RANGE (default: 0:, never critical')

    argp.add_argument('--warn_memory_percent', metavar='RANGE', default='0:90',
                      help='return warning if number of disabled agents is outside percent RANGE (default: 0:90, warn if 90%% of memory is used')

    argp.add_argument('--critical_memory_percent', metavar='RANGE', default='0:95',
                      help='return critical if number of disabled agents is outside percent RANGE (default: 0:90, critical if 95%% of memory is used')

    argp.add_argument( '--warn_vcpus', metavar='RANGE', default='0:',
                      help='return warning if number of down agents is outside RANGE (default: 0:, never warn)')
    argp.add_argument( '--critical_vcpus', metavar='RANGE', default='0:',
                      help='return critical if number of down agents is outside RANGE (default: 0, always critical if any')

    argp.add_argument( '--warn_vcpus_percent', metavar='RANGE', default='0:90',
                      help='return warning if number of down agents is outside RANGE (default: 0:90, warn if 90%% of vcpus are used)')
    argp.add_argument( '--critical_vcpus_percent', metavar='RANGE', default='0:95',
                      help='return critical if number of down agents is outside RANGE (default: 0:95, critical if 95%% of vcpus are used')

    args = argp.parse_args()

    check = osnag.Check(
        NovaHypervisors(args=args, host=args.host),
        osnag.ScalarContext('running_vms', args.warn, args.critical),
        osnag.ScalarContext('vcpus_used', args.warn_vcpus, args.critical_vcpus),
        osnag.ScalarContext('vcpus_percent', args.warn_vcpus_percent, args.critical_vcpus_percent),
        osnag.ScalarContext('memory_used', args.warn_memory, args.critical_memory),
        osnag.ScalarContext('memory_percent', args.warn_memory_percent, args.critical_memory_percent),
        osnag.Summary(show=['memory_used','memory_percent', 'vcpus_used','vcpus_percent','running_vms'])
        )
    check.main(verbose=args.verbose,  timeout=args.timeout)

if __name__ == '__main__':
    main()

