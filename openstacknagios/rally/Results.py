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
  Nagios/Icinga plugin to check rally results.

  Takes the output of 'rally task results' as input on stdin.
  and calculates the sum of load- and full_duration and the number
  of failed scenarios.

"""

import openstacknagios.openstacknagios as osnag
import sys
import json

class RallyResults(osnag.Resource):
    """
    """

    def __init__(self, args=None):
        if args.resultfile:
            infile = open(args.resultfile, 'r')

            with infile:
                try:
                    self.results=json.load(infile)
                except ValueError:
                    raise SystemExit(sys.exc_info()[1])
        else:
            self.results=json.load(sys.stdin)

        osnag.Resource.__init__(self)

    def probe(self):
        full_duration=0
        load_duration=0
        total=0
        errors=0
        slafail=0
        for tres in self.results['tasks']:
           for stres in tres['subtasks']:
              for res in stres['workloads']:
                  total=total+res['total_iteration_count']
                  errors=errors+res['failed_iteration_count']
                  full_duration=full_duration + res['full_duration']
                  load_duration=load_duration + res['load_duration']
                  if 'sla_result' in res:
                      for sla in res['sla_results']['sla']:
                          if not sla['success']:
                              slafail=slafail+1

        yield osnag.Metric('total', total)
        yield osnag.Metric('errors', errors )
        yield osnag.Metric('slafail', slafail )
        yield osnag.Metric('fulldur', full_duration, uom='s' )
        yield osnag.Metric('loaddur', load_duration, uom='s' )

@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('--resultfile',
                      help='file to read results from (output of rally task results) if not specified, stdin is used.' )

    argp.add_argument('-w', '--warn', metavar='RANGE', default=':0',
                      help='return warning if error counter is outside RANGE (default: :0, warn if any errors)')
    argp.add_argument('-c', '--critical', metavar='RANGE', default=':0',
                      help='return critical if error counter is outside RANGE (default :0, critical if any errors)')

    argp.add_argument('--warn_total', metavar='RANGE', default='0:',
                      help='return warning if number of scenarios is outside RANGE (default: 0:, never warn)')
    argp.add_argument('--critical_total', metavar='RANGE', default='0:',
                      help='return critical if number of scenarios is outside RANGE (default: 0:, never critical)')

    argp.add_argument('--warn_slafail', metavar='RANGE', default=':0',
                      help='return warning if number of sla failures is outside RANGE (default: :0, warn if any failures)')
    argp.add_argument('--critical_slafail', metavar='RANGE', default=':0',
                      help='return critical if number of sla failures is outside RANGE (default: :0, critical if any failures)')

    argp.add_argument('--warn_fulldur', metavar='RANGE', default='0:',
                      help='return warning if full_duration is outside RANGE (default: 0:, never warn)')
    argp.add_argument('--critical_fulldur', metavar='RANGE', default='0:',
                      help='return critical if full_duration is outside RANGE (default: 0:, never critical)')

    argp.add_argument('--warn_loaddur', metavar='RANGE', default='0:',
                      help='return warning if load_duration is outside RANGE (default: 0:, never warn)')
    argp.add_argument('--critical_loaddur', metavar='RANGE', default='0:',
                      help='return critical if load_duration is outside RANGE (default: 0:, never critical)')

    args = argp.parse_args()

    check = osnag.Check(
        RallyResults(args=args),
        osnag.ScalarContext('errors', args.warn, args.critical),
        osnag.ScalarContext('total', args.warn_total, args.critical_total),
        osnag.ScalarContext('slafail', args.warn_slafail, args.critical_slafail),
        osnag.ScalarContext('fulldur', args.warn_fulldur, args.critical_fulldur),
        osnag.ScalarContext('loaddur', args.warn_loaddur, args.critical_loaddur),
        osnag.Summary(show=['errors','slafail'])
        )
    check.main(verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()


