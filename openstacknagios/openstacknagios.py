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

from nagiosplugin import Resource      as NagiosResource
from nagiosplugin import Summary       as NagiosSummary
from nagiosplugin import Check
from nagiosplugin import Metric
from nagiosplugin import guarded
from nagiosplugin import ScalarContext

from keystoneauth1 import loading
from keystoneauth1 import session

from argparse import ArgumentParser    as ArgArgumentParser

from os import environ as env
import sys

import ConfigParser


class Resource(NagiosResource):
    """

    Openstack specific

    """

    def get_openstack_vars(self,args=None):

       os_vars = dict(username='', password='',tenant_name='',auth_url='', cacert='')

       if args.filename:
          config = ConfigParser.RawConfigParser()
          config.read(args.filename)
          try:
            for r in os_vars.keys():
               try:
                 os_vars[r]    = config.get('DEFAULT', r )
               except:
                 os_vars[r]    = None

          except Exception as e:
            self.exit_error(str(e) + ' Filename: ' + args.filename)
          
       else:
          try: 
            for r in os_vars.keys():
               os_vars[r]    = env['OS_' + r.upper()]
          except Exception as e:
            self.exit_error('missing environment variable ' + str(e))

       os_vars['insecure']=args.insecure
       return os_vars

    def get_session(self):
       loader = loading.get_plugin_loader('password')
       auth = loader.load_from_options(auth_url            = self.openstack['auth_url'],
                                       username            = self.openstack['username'],
                                       password            = self.openstack['password'],
                                       project_name        = self.openstack['tenant_name'],
                                       user_domain_name    = 'Default',
                                       project_domain_name = 'Default',
                                       )

       return  session.Session(auth   = auth,
                               verify = self.openstack['cacert'],
               )

    def exit_error(self, text):
       print 'UNKNOWN - ' + text
       sys.exit(3)



class Summary(NagiosSummary):
    """Create status line with info

    """
    def __init__(self, show):
        self.show = show
        NagiosSummary.__init__(self)


    def ok(self, results):
        return '[' + ' '.join(
            r + ':' + str(results[r].metric) for r in self.show) + ']'

    def problem(self, results):
        return str(results.first_significant) + '[' + ' '.join(
            r + ':' + str(results[r].metric) for r in self.show) + ']'


class ArgumentParser(ArgArgumentParser):

    def __init__(self,description, epilog=''):
        ArgArgumentParser.__init__(self,description=description, epilog=epilog)

        self.add_argument('--filename',
                      help='file to read openstack credentials from. If not set it take the environment variables' )
        self.add_argument('-v', '--verbose', action='count', default=0,
                      help='increase output verbosity (use up to 3 times)'
                           '(not everywhere implemented)')
        self.add_argument('--timeout', type=int, default=10,
                      help='amount of seconds until execution stops with unknown state (default 10 seconds)')
        self.add_argument('--insecure',
                      default=False,
                      action='store_true',
                      help="Explicitly allow client to perform \"insecure\" "
                           "SSL (https) requests. The server's certificate will "
                           "not be verified against any certificate authorities. "
                           "This option should be used with caution.")
        self.add_argument('--cacert',
                      help="Specify a CA bundle file to use in verifying a TLS"
                           "(https) server certificate.")
