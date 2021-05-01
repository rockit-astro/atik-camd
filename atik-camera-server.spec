Name:      atik-camera-server
Version:   20210501
Release:   0
Url:       https://github.com/warwick-one-metre/atik-camd
Summary:   Camera control server for the SuperWASP telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch
Requires:  python3, python3-Pyro4, python3-numpy, python3-astropy, python3-libusb1, python3-warwick-observatory-common, python3-warwick-atik-camera
Requires:  libatikcameras, observatory-log-client, %{?systemd_requires}

%description

Part of the observatory software for the SuperWASP telescope.

camd interfaces with and wraps modified Atik 11000M detectors and exposes them via Pyro.

%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/camd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/atik_camd.service %{buildroot}%{_unitdir}

%files
%defattr(0755,root,root,-)
%{_bindir}/camd
%defattr(0644,root,root,-)

%{_unitdir}/atik_camd.service

%changelog
