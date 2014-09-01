openstack-nagios-plugins
========================

Nagios/icinga plugins to monitor an openstack installation.

For all checks there are some common arguments:

```
  -h, --help            show help message and all arguments
  --filename FILENAME   File to read openstack credentials from. If not set it
                        takes the standard environment variables from openstack.
  -v, --verbose         increase output verbosity (use up to 3 times)(not
                        everywhere implemented)
  --insecure            Explicitly allow to perform "insecure" SSL
                        (https) requests. The server's certificate will not be
                        verified against any certificate authorities. This
                        option should be used with caution.
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
