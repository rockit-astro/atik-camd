Name:      python3-warwick-observatory-camera-atik
Version:   20210713
Release:   0
License:   GPL3
Summary:   Common code for the Atik camera daemon
Url:       https://github.com/warwick-one-metre/atik-camd
BuildArch: noarch

%description

%prep

rsync -av --exclude=build .. .

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
