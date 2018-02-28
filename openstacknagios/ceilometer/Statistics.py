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
  Nagios/Icinga plugin to check ceilometer statistics.

  Returns the statistic of the chosen meter. This also returns the age of the 
  last sample used to aggregate. So this check can also be used to verify freshness
  of samples in the ceilometer DB. (or of course to check the value).

"""

import openstacknagios.openstacknagios as osnag

import ceilometerclient.v2.client as ceilclient

import datetime 
from pytz import timezone
import pytz

# Date format used by ceilometer for queries
date_format = "%Y-%m-%dT%H:%M:%S"
date_format_tz = "%Y-%m-%dT%H:%M:%S %Z"

class CeilometerStatistics(osnag.Resource):
    """
    """

    def __init__(self, args=None):
        self.meter     = args.meter
        self.tframe    = datetime.timedelta(minutes=int(args.tframe))
        self.tzone     = timezone(args.tzone)
        self.verbose   = args.verbose
        self.aggregate = args.aggregate
        self.openstack = self.get_openstack_vars(args=args)
        osnag.Resource.__init__(self)

    def probe(self):
        try:
           ceilometer = ceilclient.Client(
                                          session  = self.get_session(),
                                          cacert   = self.openstack['cacert'],
                                          insecure = self.openstack['insecure'])
        except Exception as e:
           self.exit_error('cannot start ceil ' + str(e))

        now=datetime.datetime.now(self.tzone)
   
        tstart=now - self.tframe
        query=[]
        query.append({'field': 'timestamp','op':'gt','value':tstart.strftime(date_format)})

        try:
           teste=ceilometer.statistics.list(self.meter, q=query)
           #print "meters = %s" % ceilometer.meters.list()
           #print "resources = %s" % ceilometer.resources.list()
           #print "alarms = %s" % ceilometer.alarms.list()
        except Exception as e:
           self.exit_error('cannot load: ' + str(e))

        for t in teste :
           period_end=self.tzone.localize(datetime.datetime.strptime(getattr(t,'period_end','')[:19],date_format))
           age = now - period_end
           yield osnag.Metric('count', getattr(t,'count',''),uom='samples')
           yield osnag.Metric('age', age.total_seconds()/60, uom='m' )
           yield osnag.Metric('value', getattr(t,self.aggregate,''),
                               min=getattr(t,'min',''),
                               max=getattr(t,'max',''),
                               uom=getattr(t,'unit',''))

           if self.verbose:
             print
             print 'now:            %s' % now.strftime(date_format_tz)
             print 'query start     %s' % tstart.strftime(date_format_tz)
             print 'duration_start: %s' % getattr(t,'duration_start','')
             print 'period_start:   %s' % getattr(t,'period_start','')
             print 'duration_end:   %s' % getattr(t,'duration_end','')
             print 'period_end:     %s' % period_end.strftime(date_format_tz)
             print 'age             %s minutes' % str(age.total_seconds()/60)
             print 'count:          %s samples' % getattr(t,'count','')
             print 'min:            %s ' % getattr(t,'min','') + getattr(t,'unit','')
             print 'max:            %s ' % getattr(t,'max','') + getattr(t,'unit','')
             print 'duration:       %s minutes' % (int(getattr(t,'duration',''))/60)
             print 'avg:            %s ' % getattr(t,'avg','') + getattr(t,'unit','')
             print 'sum:            %s ' % getattr(t,'sum','') + getattr(t,'unit','')
             print 

@osnag.guarded
def main():
    argp = osnag.ArgumentParser(description=__doc__)

    argp.add_argument('-m', '--meter', metavar='METER_NAME', required=True,
                      help='meter name (required)')
    argp.add_argument('-t', '--tframe', metavar='VALUE', type=int, default=60,
                      help='Time frame to look back in minutes')
    argp.add_argument('--tzone', metavar='TZONE', default='utc',
                      help='Timezone to use. Ceilometer does not store any timezone information with the samples.')

    argp.add_argument('-w', '--warn', metavar='RANGE', default='0:',
                      help='return warning if value is outside RANGE (default: 0:, never warn)')
    argp.add_argument('-c', '--critical', metavar='RANGE', default='0:',
                      help='return critical if value is outside RANGE (default 0:, never critical)')

    argp.add_argument('--warn_count', metavar='RANGE', default='0:',
                      help='return warning if the number of samples is outside RANGE (default: 0:, never warn')
    argp.add_argument('--critical_count', metavar='RANGE', default='0:',
                      help='return critical if the number of samples is outside RANGE (default: 0:, never critical')

    argp.add_argument('--warn_age', metavar='RANGE', default='0:',
                      help='return warning if the age in minutes of the last value is outside RANGE (default: 0:30, warn if older than 30 minutes')
    argp.add_argument('--critical_age', metavar='RANGE', default='0:',
                      help='return critical if the age in minutes of the last value is outside RANGE (default: 0:60, critical if older than 1 hour')

    argp.add_argument( '--aggregate', default='avg',
                      help='Aggregate function to use. Can be one of avg or sum (avg is the default)')

    args = argp.parse_args()

    check = osnag.Check(
        CeilometerStatistics(args=args),
        osnag.ScalarContext('age', args.warn_age, args.critical_age),
        osnag.ScalarContext('count', args.warn_count, args.critical_count),
        osnag.ScalarContext('value', args.warn, args.critical),
        osnag.Summary(show=['age','count','value'])
        )
    check.main(verbose=args.verbose, timeout=args.timeout)

if __name__ == '__main__':
    main()


