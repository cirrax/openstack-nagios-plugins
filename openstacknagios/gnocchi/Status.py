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
    Nagios/Icinga plugin to check gnocchi status.

    This corresponds to the output of 'gnocchi status'.
"""

import openstacknagios.openstacknagios as osnag
import openstacknagios.gnocchi.Gnocchi as gnocchi

class GnocchiStatus(gnocchi.Gnocchi):
    """
    Determines the status of gnocchi.
    """

    def probe(self):
        client=self.get_client()

        try:
           result=client.status.get()['storage']['summary']
        except Exception as e:
           self.exit_error(str(e))

        #{u'storage': {u'summary': {u'metrics': 98, u'measures': 98}}}

        yield osnag.Metric('measures',result['measures'])
        yield osnag.Metric('metrics',result['metrics'])


@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('-w', '--warn', metavar='RANGE', default='0:100',
            help='return warning if number of measures to process range (default: 0:100)')
    argp.add_argument('-c', '--critical', metavar='range', default='0:200',
            help='return critical if number of measures to process range range (default 0:200)')

    argp.add_argument('--warn_metrics', metavar='RANGE', default='0:100',
                      help='return warning if number of metrics having measures to process outside RANGE (default: 0:100')
    argp.add_argument('--critical_metrics', metavar='RANGE', default='0:200',
                      help='return critical if number of metrics having measures to process is outside RANGE (default: 0:200')

    args = argp.parse_args()

    check = osnag.Check(
        GnocchiStatus(args=args),
        osnag.ScalarContext('measures', args.warn, args.critical),
        osnag.ScalarContext('metrics', args.warn_metrics, args.critical_metrics),
        osnag.Summary(show=['measures','metrics'])
        )
    check.main(verbose=args.verbose,  timeout=args.timeout)

if __name__ == '__main__':
    main()
