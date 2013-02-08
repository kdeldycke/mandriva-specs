%define name    qlc
%define version 3.0.0.trunk.r1276
%define release %mkrel 1


Name:          %{name}
Version:       %{version}
Release:       %{release}
Summary:       Q Light Controller
Group:         Other
License:       GPL
URL:           http://qlc.sf.net
Source0:       %{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libqt4-devel >= 4.3, libalsa-devel, libusb-devel
Requires:      libqtcore4 >= 4.3, libalsa, libusb


%description
The Q Light Controller (QLC) is an X11/Linux application to control DMX or 0-10V lighting systems like dimmers, scanners and other lighting effects. Our goal is to replace expensive and rather limited hardware lighting desks with free software.


%prep
%setup -q -n %{name}-%{version}
# Do not compile FTDI DMX output folder: it seems broken on x86_64 machines
#sed -i -e 's,SUBDIRS\t\t\t+= ftdidmx,#SUBDIRS\t\t\t+= ftdidmx,g' libs/libs.pro
#%ifarch x86_64
#pushd  libs
#tar -xvzf %{SOURCE1}
#cp -f  libftd2xx0.4.16_x86_64/*.h                 ftdidmx/
#cp -f  libftd2xx0.4.16_x86_64/libftd2xx.so.0.4.16 ftdidmx/
#cp -f  libftd2xx0.4.16_x86_64/static_lib/*        ftdidmx/
#rm -rf libftd2xx0.4.16_x86_64
#popd
#%endif


%build
%qmake_qt4 INSTALL_ROOT=%buildroot
#lrelease qlc.pro
%make INSTALL_ROOT=%buildroot


%install
rm -rf %buildroot
#[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
#%makeinstall
#%makeinstall_std -C build
#%makeinstall_std DESTDIR=%buildroot
%makeinstall_std INSTALL_ROOT=%buildroot


%clean
rm -rf %buildroot


%files
%defattr(-, root, root)
/usr/bin/*
/usr/lib/libqlc*
/usr/lib/qlc/*
/usr/share/applications/*
/usr/share/pixmaps/*
/usr/share/qlc/fixtures/*
/usr/share/qlc/inputprofiles/*
%doc /usr/share/qlc/documents/gfx/*
%doc /usr/share/qlc/documents/html/*


%changelog
* Fri Aug 14 2009 Kevin Deldycke <kevin@deldycke.com> 3.0.0.trunk.r1276-1mdv2009.1
- Upgrade to latest SVN trunk revision r1276

* Sat Jun 20 2009 Kevin Deldycke <kevin@deldycke.com> 3.0.0.trunk.r1235-1mdv2009.1
- Upgrade to latest SVN trunk revision r1235
- Fix libs requirement

* Sun May 31 2009 Kevin Deldycke <kevin@deldycke.com> 3.0.0-1mdv2009.1
- Upgrade to QLC 3.0.0
- Remove old QLC/LLA patch
- Temporarily remove dependency on LLA
- Add patch to not compile FTDI DMX driver as it doesn't work on x86_64 arch
- Rebuild RPM for Mandriva 2009.1

* Mon May 12 2008 Kevin Deldycke <kev@coolcavemen.com> 2.6.1-1mdv2008.1
- Ported from Fedora Core 6 ( http://rpms.netmindz.net/FC6/SRPMS.netmindz/qlc-2.6.1-2.fc6.src.rpm ) to Mandriva 2008.1

* Sun Apr 29 2007 Will Tatam <will@netmindz.net> 2.6_1-2
- Added lla plugin to support :-
- ArtNet
- Strand Shownet
- Enttec ESP Net
- Sandnet
- Enttec USB Pro
- Enttec Open DMX USB

* Thu Nov 30 2006 Will Tatam <will@netmindz.net> 2.6_1-1
- first build
