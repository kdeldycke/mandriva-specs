%define name    dmx_usb
%define version 20071111
%define release %mkrel 1


Name:     %{name}
Version:  %{version}
Release:  %{release}
Summary:  OpenDMX driver
Group:    Other
License:  GPL
URL:      http://www.erwinrol.com/index.php?opensource/dmxusb.php
Source0:  http://www.erwinrol.com/downloads/software/%{name}_module-%{version}.tgz
Source1:  %{name}_module-Makefile


%description
Open DMX USB is an open USB to DMX dongle hardware design developed by Enttec. The Open in Open DMX USB refers to the fact that everybody is free to use the design and produce its own USB DMX Dongle without paying any licenses. Since this fits the Linux philosophy I wrote a small Linux 2.6 kernel driver to make it possible to use the dongle under Linux. In the future I hope the DMX USB dongle will just be supported by DMX4Linux.


%package -n dkms-%{name}
Summary:  OpenDMX driver
Group:    System/Kernel and hardware
Requires: dkms
Requires: %{name} = %{version}
%description -n dkms-%{name}

Kernel drivers for the OpenDMX device


%prep
%setup -q -n %{name}_module
cp -f %{SOURCE1} ./Makefile

%build
make apps

%install
rm -rf %buildroot

mkdir -p %{buildroot}%{_bindir}
install -m 755 %{name}_test %{buildroot}%{_bindir}

mkdir -p %{buildroot}/usr/src/%{name}-%{version}-%{release}

cp  %{name}.* Makefile %{buildroot}/usr/src/%{name}-%{version}-%{release}/

cat > %{buildroot}/usr/src/%{name}-%{version}-%{release}/dkms.conf <<EOF
PACKAGE_VERSION="%{version}-%{release}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{name}"
BUILT_MODULE_NAME[0]="%{name}"
DEST_MODULE_LOCATION[0]="/kernel/drivers/usb/serial"

AUTOINSTALL=yes
EOF


%clean
rm -rf %buildroot

%post -n dkms-%{name}
dkms add -m	%{name} -v %{version}-%{release} --rpm_safe_upgrade
dkms build -m	%{name} -v %{version}-%{release} --rpm_safe_upgrade
dkms install -m	%{name} -v %{version}-%{release} --rpm_safe_upgrade --force

%preun -n dkms-%{name}
dkms remove -m	%{name} -v %{version}-%{release} --rpm_safe_upgrade --all


%files
%defattr(-,root,root,-)
%doc Changelog README
%{_bindir}/%{name}_test

%files -n dkms-%{name}
%defattr(-,root,root,-)
/usr/src/%{name}-%{version}-%{release}


%changelog
* Mon May 12 2008 Kevin Deldycke <kev@coolcavemen.com> 20071111-1mdv2008.1
- Ported from Fedora Core 8 ( http://rpms.netmindz.net/FC8/SRPMS.netmindz/dmx_usb-20071111-2.fc8.src.rpm ) to Mandriva 2008.1

* Sat Nov 10 2007 Will Tatam <will@netmindz.net>
- Fist Build
