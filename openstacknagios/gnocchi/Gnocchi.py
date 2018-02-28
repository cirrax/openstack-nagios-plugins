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
from gnocchiclient import auth
from gnocchiclient.v1.client import Client


class Gnocchi(osnag.Resource):
    """
    Get gnocchi client
    """

    def __init__(self, args=None):
        self.openstack = self.get_openstack_vars(args=args)
        osnag.Resource.__init__(self)

    def get_client(self):

        try:
           client=Client( session  = self.get_session())
        except Exception as e:
           self.exit_error(str(e))

        return client

if __name__ == '__main__':
    main()

