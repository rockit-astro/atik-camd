Name:           python3-warwick-atik-camera
Version:        1.0.0
Release:        0
License:        GPL3
Summary:        Common backend code for the Atik camera daemon
Url:            https://github.com/warwick-one-metre/atik-camd
BuildArch:      noarch

%description
Part of the observatory software for the SuperWASP telescope.

python3-warwick-atik-camera holds the common camera code.

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
