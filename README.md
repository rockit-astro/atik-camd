## Atik camera daemon

`atik_camd` interfaces with and wraps modified Atik 11000M detectors and exposes them via Pyro.

`cam` is a commandline utility for controlling the cameras.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the observatory software architecture and instructions for developing and deploying the code.

### Configuration

Configuration is read from json files that are installed by default to `/etc/camd`.
A configuration file is specified when launching the camera server, and the `cam` frontend will search for files matching the specified camera id when launched.

The configuration options are:
```python
{
  "daemon": "localhost_test", # Run the camera server as this daemon. Daemon types are registered in `warwick.observatory.common.daemons`.
  "pipeline_daemon": "localhost_test2", # The daemon that should be notified to hand over newly saved frames for processing.
  "pipeline_handover_timeout": 10, # The maximum amount of time to wait for the pipeline daemon to accept a newly saved frame. The exposure sequence is aborted if this is exceeded.
  "log_name": "atik_camd@test", # The name to use when writing messages to the observatory log.
  "control_machines": ["LocalHost"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `warwick.observatory.common.IP`.
  "usb_bus": 1, # USB Bus that the camera is attached to. Can be found using `lsusb -t`
  "usb_port_numbers": [2], # USB Port tree that the camera is attached to. Can be found using `lsusb -t` and following the Port entries from the Bus to the device.
  "temperature_setpoint": -15, # Default temperature for the CMOS sensor.
  "temperature_query_delay": 1, # Amount of time in seconds to wait between querying the camera temperature and cooling status
  "camera_id": "TEST", # Value to use for the CAMERA fits header keyword.
  "output_path": "/var/tmp/", # Path to save temporary output frames before they are handed to the pipeline daemon. This should match the pipeline incoming_data_path setting.
  "output_prefix": "test", # Filename prefix to use for temporary output frames.
  "expcount_path": "/var/tmp/test-counter.json" # Path to the json file that is used to track the continuous frame number.
}
```

Note that the modified firmware in the cameras do not provide a stable serial number, so we must instead identify cameras
based on the physical USB port that they are connected to.

### Initial Installation (Raspberry Pi 4)

Note that this requires the 64 bit Raspbian to be installed. The arm32 atik library does not appear to work correctly.

Start by installing the atik SDK files from the [libatikcameras](https://github.com/warwick-one-metre/libatikcameras) repo.

Extract the zip file and copy:
* `lib/ARM/64/NoFlyCapture/libatikcameras.so` to `/usr/lib/libatikcameras.so`
* `lib/linux/atik.rules` to `/usr/lib/udev/rules.d/10-atikcameras.rules`

Install python deps using pip:
```
sudo pip3 install -r requirements.txt
```

Install the observatory software dependencies:
* [obslogd](https://github.com/warwick-one-metre/obslogd/) (copy `obslog` to `/usr/bin`)
* [warwick-observatory-common](https://github.com/warwick-one-metre/warwick-observatory-common/) (`sudo python3 setup.py install`)

Copy the camera server, client, and config files:
```
sudo cp cam atik_camd /usr/bin
sudo cp *.json /etc/camd
sudo cp atik_camd@.service /usr/lib/systemd/system
sudo cp completion/cam /etc/bash_completion.d/
```

Install the shared python code
```
sudo python3 setup.py install
```

Start the systemd services:
```
sudo systemctl daemon-reload
sudo systemctl enable atik_camd@<config>
sudo systemctl start atik_camd@<config>
```

where `config` is the name of the json file for each camera.

Finally, we need to set up NFS to mount the pipeline incoming data directory. Edit `/etc/fstab` and add

```
10.2.6.217:/data/wasp /mnt/wasp-data   nfs defaults,x-systemd.automount,x-systemd.after=network-online.target,_netdev 0 0
```

### Testing Locally

The camera server and client can be run directly from a git clone:
```
./atik_camd test.json
CAMD_CONFIG_ROOT=. ./cam test status
```
