#
# This file is part of atik-camd.
#
# atik-camd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# atik-camd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with atik-camd.  If not, see <http://www.gnu.org/licenses/>.

"""Helper function to validate and parse the json config file"""

import json
from warwick.observatory.common import daemons, IP, validation

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'pipeline_daemon', 'pipeline_handover_timeout', 'log_name', 'control_machines', 'usb_bus',
        'usb_port_numbers', 'camera_id', 'temperature_setpoint', 'temperature_query_delay',
        'output_path', 'expcount_path'
    ],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'pipeline_daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'pipeline_handover_timeout': {
            'type': 'number',
            'min': 0
        },
        'log_name': {
            'type': 'string',
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        'usb_bus': {
            'type': 'number',
            'min': 1
        },
        'usb_port_numbers': {
            'type': 'array',
            'items': {
                'type': 'number',
                'min': 1,
                'minItems': 1,
                'maxItems': 7
            }
        },
        'temperature_setpoint': {
            'type': 'number',
            'min': -20,
            'max': 30,
        },
        'temperature_query_delay': {
            'type': 'number',
            'min': 0
        },
        'camera_id': {
            'type': 'string',
        },
        'output_path': {
            'type': 'string',
        },
        'expcount_path': {
            'type': 'string',
        }
    }
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validation.validate_config(config_json, CONFIG_SCHEMA, {
            'daemon_name': validation.daemon_name_validator,
            'machine_name': validation.machine_name_validator,
            'directory_path': validation.directory_path_validator,
        })

        self.daemon = getattr(daemons, config_json['daemon'])
        self.pipeline_daemon_name = config_json['pipeline_daemon']
        self.pipeline_handover_timeout = config_json['pipeline_handover_timeout']
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.usb_bus = config_json['usb_bus']
        self.usb_port_numbers = config_json['usb_port_numbers']
        self.camera_id = config_json['camera_id']
        self.output_path = config_json['output_path']
        self.expcount_path = config_json['expcount_path']
        self.temperature_setpoint = config_json['temperature_setpoint']
        self.temperature_query_delay = config_json['temperature_query_delay']
