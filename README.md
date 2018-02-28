openstack-nagios-plugins
========================

Nagios/icinga plugins to monitor an openstack installation.

Find also some information about these plugins in the talk
[Monitoring an Openstack Cluster with icinga/nagios](https://www.cirrax.com/downloads/2015_OpenstackMonitoring.pdf)
held at the 11th Swiss OpenStack User Group Meetup by [Cirrax](https://www.cirrax.com).


For all checks there are some common arguments:

```
  -h, --help            show help message and all arguments
  --filename FILENAME   File to read openstack credentials from. If not set it
                        takes the standard environment variables from openstack.
  -v, --verbose         increase output verbosity (use up to 3 times)(not
                        everywhere implemented)
  --cacert CACERT       Specify a CA bundle file to use in verifying a
                        TLS(https) server certificate.
  --insecure            Explicitly allow to perform "insecure" SSL
                        (https) requests. The server's certificate will not be
                        verified against any certificate authorities. This
                        option should be used with caution.
  --timeout TIMEOUT     amount of seconds until execution stops with unknow
                        state (default 10 seconds)
```

Currently the following checks are implemented:

check\_cinder-services
---------------------

Nagios/Icinga plugin to check running cinder agents/services.

This corresponds to the output of 'cinder service-list'.

optional arguments:
```
  -w RANGE, --warn RANGE
                        return warning if number of up agents is outside RANGE
                        (default: 0:, never warn)
  -c RANGE, --critical RANGE
                        return critical if number of up agents is outside
                        RANGE (default 1:, never critical)
  --warn_disabled RANGE
                        return warning if number of disabled agents is outside
                        RANGE (default: @1:, warn if any disabled agents
  --critical_disabled RANGE
                        return critical if number of disabled agents is
                        outside RANGE (default: 0:, never critical
  --warn_down RANGE     return warning if number of down agents is outside
                        RANGE (default: 0:, never warn)
  --critical_down RANGE
                        return critical if number of down agents is outside
                        RANGE (default: 0, always critical if any
  --binary BINARY       filter agent binary
  --host HOST           filter hostname
```

Admin rights are necessary to run this check.

check\_neutron-agents
--------------------
Nagios/Icinga plugin to check running neutron agents. 
This corresponds to the output of 'neutron agent-list'.

optional arguments:
```
  -w RANGE, --warn RANGE
                        return warning if number of up agents is outside RANGE
                        (default: 0:, never warn)
  -c RANGE, --critical RANGE
                        return critical if number of up agents is outside
                        RANGE (default 1:, never critical)
  --warn_disabled RANGE
                        return warning if number of disabled agents is outside
                        RANGE (default: @1:, warn if any disabled agents
  --critical_disabled RANGE
                        return critical if number of disabled agents is
                        outside RANGE (default: 0:, never critical
  --warn_down RANGE     return warning if number of down agents is outside
                        RANGE (default: 0:, never warn)
  --critical_down RANGE
                        return critical if number of down agents is outside
                        RANGE (default: 0, always critical if any
  --binary BINARY       filter agent binary
  --host HOST           filter hostname
```

Admin rights are necessary to run this check.


check\_neutron-floatingips
-------------------------

Nagios/Icinga plugin to check floating ip's.
Counts the assigned ip's (= used + unused). 

This corresponds to the output of 'neutron floatingip-list'.

optional arguments:
```
  -w RANGE, --warn RANGE
                        return warning if number of assigned floating ip's is
                        outside range (default: 0:200, warn if more than 200
                        are used)
  -c RANGE, --critical RANGE
                        return critical if number of assigned floating ip's is
                        outside RANGE (default 0:230, critical if more than
                        230 are used)
```

Admin rights are necessary to run this check.


check\_nova-services
-------------------

Nagios/Icinga plugin to check running nova services.

This corresponds to the output of 'nova service-list'.

optional arguments:
```
  -w RANGE, --warn RANGE
                        return warning if number of up agents is outside RANGE
                        (default: 0:, never warn)
  -c RANGE, --critical RANGE
                        return critical if number of up agents is outside
                        RANGE (default 1:, never critical)
  --warn_disabled RANGE
                        return warning if number of disabled agents is outside
                        RANGE (default: @1:, warn if any disabled agents
  --critical_disabled RANGE
                        return critical if number of disabled agents is
                        outside RANGE (default: 0:, never critical
  --warn_down RANGE     return warning if number of down agents is outside
                        RANGE (default: 0:, never warn)
  --critical_down RANGE
                        return critical if number of down agents is outside
                        RANGE (default: 0, always critical if any
  --binary BINARY       filter agent binary
  --host HOST           filter hostname
```

Admin rights are necessary to run this check.


check\_nova-hypervisors
----------------------

Nagios/Icinga plugin to check nova hypervisors.

This corresponds to the output of 'nova hypervisor-stats'

optional arguments:
```
  -H HOST, --host HOST  hostname where the hypervisor is running if not
                        defined (default), summary of all hosts is used
  -w RANGE, --warn RANGE
                        return warning if number of running vms is outside
                        RANGE (default: 0:, never warn)
  -c RANGE, --critical RANGE
                        return critical if number of running vms is outside
                        RANGE (default 0:, never critical)
  --warn_memory RANGE   return warning if number of disabled agents is outside
                        RANGE (default: 0:, never warn
  --critical_memory RANGE
                        return critical if number of disabled agents is
                        outside RANGE (default: 0:, never critical
  --warn_memory_percent RANGE
                        return warning if number of disabled agents is outside
                        percent RANGE (default: 0:90, warn if 90% of memory is
                        used
  --critical_memory_percent RANGE
                        return critical if number of disabled agents is
                        outside percent RANGE (default: 0:90, critical if 95%
                        of memory is used
  --warn_vcpus RANGE    return warning if number of down agents is outside
                        RANGE (default: 0:, never warn)
  --critical_vcpus RANGE
                        return critical if number of down agents is outside
                        RANGE (default: 0, always critical if any
  --warn_vcpus_percent RANGE
                        return warning if number of down agents is outside
                        RANGE (default: 0:90, warn if 90% of vcpus are used)
  --critical_vcpus_percent RANGE
                        return critical if number of down agents is outside
                        RANGE (default: 0:95, critical if 95% of vcpus are
                        used
```

Admin rights are necessary to run this check.

check\_ceilometer-statistics
---------------------------
Nagios/Icinga plugin to check ceilometer statistics. Returns the statistic of
the chosen meter. This also returns the age of the last sample used to
aggregate. So this check can also be used to verify freshness of samples in
the ceilometer DB. (or of course to check the value).


```
  -m METER_NAME, --meter METER_NAME
                        meter name (required)
  -t VALUE, --tframe VALUE
                        Time frame to look back in minutes
  --tzone TZONE         Timezone to use. Ceilometer does not store any
                        timezone information with the samples.
  -w RANGE, --warn RANGE
                        return warning if value is outside RANGE (default: 0:,
                        never warn)
  -c RANGE, --critical RANGE
                        return critical if value is outside RANGE (default 0:,
                        never critical)
  --warn_count RANGE    return warning if the number of samples is outside
                        RANGE (default: 0:, never warn
  --critical_count RANGE
                        return critical if the number of samples is outside
                        RANGE (default: 0:, never critical
  --warn_age RANGE      return warning if the age in minutes of the last value
                        is outside RANGE (default: 0:30, warn if older than 30
                        minutes
  --critical_age RANGE  return critical if the age in minutes of the last
                        value is outside RANGE (default: 0:60, critical if
                        older than 1 hour
  --aggregate AGGREGATE
                        Aggregate function to use. Can be one of avg or sum
                        (avg is the default)
```

check\_keystone-token
--------------------

Nagios/Icinga plugin to check keystone. The check will get a token and mesure the
time used.

```
  -w RANGE, --warn RANGE
                        return warning if number of up agents is outside RANGE
                        (default: 0:, never warn)
  -c RANGE, --critical RANGE
                        return critical if number of up agents is outside
                        RANGE (default 1:, never critical)
```

check\_rally-results
-------------------

Nagios/Icinga plugin to check rally results. Takes the outpup of 'rally task
results' as input on stdin. and calculates the sum of load- and full- duration
and the number of failed scenarios.

check_glance-images
-----------------

Lists glance images and gets timing

check_neutron-routers
---------------------

Determines the number down/build/active routers
