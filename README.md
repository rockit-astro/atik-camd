## Atik camera daemon

Part of the observatory software for the SuperWASP telescope.

`camd` interfaces with and wraps modified Atik 11000M detectors and exposes them via Pyro.

`cam` is a commandline utility for controlling the cameras.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup

After installing `atik-camera-server`, the `camd` service must be enabled using:
```
sudo systemctl enable atik_camd.service@<config>
```

where `config` is TODO...

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start atik_camd@<config>
```

Finally, open ports in the firewall so that other machines on the network can access the daemons:
```
sudo firewall-cmd --zone=public --add-port=9037/tcp --permanent
sudo firewall-cmd --reload
```

### Hardware Setup

The modified cameras do not expose unique serial numbers, so are instead identified based on USB bus and device number as reported through `lsusb`.

