Name:      superwasp-atik-camera-data
Version:   20210713
Release:   0
Url:       https://github.com/warwick-one-metre/atik-camd
Summary:   Camera configuration for SuperWASP telescope.
License:   GPL-3.0
Group:     Unspecified
BuildArch: noarch

%description

%build
mkdir -p %{buildroot}%{_sysconfdir}/camd
%{__install} %{_sourcedir}/1.json %{buildroot}%{_sysconfdir}/camd
%{__install} %{_sourcedir}/2.json %{buildroot}%{_sysconfdir}/camd
%{__install} %{_sourcedir}/3.json %{buildroot}%{_sysconfdir}/camd
%{__install} %{_sourcedir}/4.json %{buildroot}%{_sysconfdir}/camd

%files
%defattr(0644,root,root,-)
%{_sysconfdir}/camd/1.json
%{_sysconfdir}/camd/2.json
%{_sysconfdir}/camd/3.json
%{_sysconfdir}/camd/4.json

%changelog
