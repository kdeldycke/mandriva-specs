%define name    lla
%define version 0.2.3.200710210908
%define release %mkrel 1


Name:    %{name}
Version: %{version}
Release: %{release}
Summary: Linux Lighting Architecture
Group:   Other
License: GPL
URL:     http://www.nomis52.net
Source0: http://www.nomis52.net/data/sources/%{name}/%{name}-%{version}.tar.gz


%description
The Linux Lighting Architecture (lla) consists of two parts, the daemon llad and the library, liblla.


%package -n liblla
Group:         Other
Summary:       Linux Lighting Architecture

%description -n liblla
The LLA library

%package -n liblla-devel
Group:         Other
Summary:       Linux Lighting Architecture

%description -n liblla-devel
The LLA library headers


%prep
%setup -q -n lla-0.2.3


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %buildroot
make install DESTDIR=%buildroot


%clean
rm -rf %buildroot


%files
%defattr(-,root,root,-)
/usr/bin/llad
/usr/bin/llad_test

%files -n liblla
%defattr(-,root,root,-)
%{_libdir}/liblla.so*
%{_libdir}/llad/*.so*
%{_libdir}/liblla*.so*

%files -n liblla-devel
%defattr(-,root,root,-)
/usr/include/
%{_libdir}/llad/liblla*.a
%{_libdir}/llad/liblla*.la
%{_libdir}/liblla*.a
%{_libdir}/liblla*.la
%{_libdir}/pkgconfig/liblla*.pc


%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO


%changelog
* Mon May 12 2008 Kevin Deldycke <kev@coolcavemen.com> 0.2.3.200710210908-1mdv2008.1
- Ported from Fedora Core 8 ( http://rpms.netmindz.net/FC8/SRPMS.netmindz/lla-0.2.3.200710210908-1.fc8.src.rpm ) to Mandriva 2008.1

* Sun Apr 29 2007 Will Tatam <will@netmindz.net> 0.1.3-1
- Fist Build
