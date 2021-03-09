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
import sys
import traceback
import jsonschema
from warwick.observatory.common import daemons, IP

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'pipeline_daemon', 'log_name', 'control_machines', 'usb_bus', 'usb_devnum',
        'arm', 'temperature_setpoint', 'output_path', 'output_prefix', 'expcount_path'
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
        'usb_devnum': {
            'type': 'number',
            'min': 1
        },
        'temperature_setpoint': {
            'type': 'number',
            'min': -20,
            'max': 30,
        },
        'arm': {
            'type': 'string',
        },
        'output_path': {
            'type': 'string',
        },
        'output_prefix': {
            'type': 'string',
        },
        'expcount_path': {
            'type': 'string',
        }
    }
}

class ConfigSchemaViolationError(Exception):
    """Exception used to report schema violations"""
    def __init__(self, errors):
        message = 'Invalid configuration:\n\t' + '\n\t'.join(errors)
        super(ConfigSchemaViolationError, self).__init__(message)


def __create_validator():
    """Returns a template validator that includes support for the
       custom schema tags used by the observation schedules:
            daemon_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.daemons address book
            machine_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.IP address book
    """
    validators = dict(jsonschema.Draft4Validator.VALIDATORS)

    # pylint: disable=unused-argument
    def daemon_name(validator, value, instance, schema):
        """Validate a string as a valid daemon name"""
        try:
            getattr(daemons, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid daemon name'.format(instance))

    def machine_name(validator, value, instance, schema):
        """Validate a string as a valid machine name"""
        try:
            getattr(IP, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid machine name'.format(instance))
    # pylint: enable=unused-argument

    validators['daemon_name'] = daemon_name
    validators['machine_name'] = machine_name
    return jsonschema.validators.create(meta_schema=jsonschema.Draft4Validator.META_SCHEMA,
                                        validators=validators)


def validate_config(config_json):
    """Tests whether a json object defines a valid environment config file
       Raises SchemaViolationError on error
    """
    errors = []
    try:
        validator = __create_validator()
        for error in sorted(validator(CONFIG_SCHEMA).iter_errors(config_json),
                            key=lambda e: e.path):
            if error.path:
                path = '->'.join([str(p) for p in error.path])
                message = path + ': ' + error.message
            else:
                message = error.message
            errors.append(message)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        errors = ['exception while validating']

    if errors:
        raise ConfigSchemaViolationError(errors)


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validate_config(config_json)

        self.daemon = getattr(daemons, config_json['daemon'])
        self.pipeline_daemon = getattr(daemons, config_json['pipeline_daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.usb_bus = config_json['usb_bus']
        self.usb_devnum = config_json['usb_devnum']
        self.arm = config_json['arm']
        self.output_path = config_json['output_path']
        self.output_prefix = config_json['output_prefix']
        self.expcount_path = config_json['expcount_path']
        self.temperature_setpoint = config_json['temperature_setpoint']