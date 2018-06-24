##
#     Project: New in my net
# Description: Find new devices in my network
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2018 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

from collections import OrderedDict

from .constants import *
from .settings import Settings
from .dbhosts import DBHosts


class Application(object):
    def __init__(self):
        """Create the application object"""
        self.settings = Settings()
        self.dbhosts = DBHosts()

    def startup(self):
        """Configure the application during the startup"""
        self.networks = self.dbhosts.list_networks()

    def run(self, network_name):
        """Execute the application"""
        network = self.networks[network_name]
        for address in network.range():
            if network.check_ping:
                # Check the host using PING
                network.tool_ping.execute(address)
        # Start the tools threads
        network.tool_ping.start()
        # Awaits the tools to complete
        network.tool_ping.process()
        # Sort data and print results
        results = OrderedDict()
        for address in network.range():
            data = {}
            if network.check_ping:
                data['ping'] = network.tool_ping.results[address]
            results[address] = data
        for data in results:
            print(data, results[data])
        return results