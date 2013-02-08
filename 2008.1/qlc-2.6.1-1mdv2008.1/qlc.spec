%define name    qlc
%define version 2.6.1
%define release %mkrel 1


Name:          %{name}
Version:       %{version}
Release:       %{release}
Summary:       Q Light Controller
Group:         Other
License:       GPL
URL:           http://qlc.sf.net
Source0:       %{name}-%{version}.tar.gz
Source1:       http://nomis52.net/data/artnet/qlc/qlc_lla.tar.gz
Patch1:        %{name}-lla.patch

BuildRequires: pkgconfig, libtool, autoconf, automake
%ifnarch x86_64
BuildRequires: libqt3-devel
%endif
%ifarch x86_64
BuildRequires: lib64qt3-devel
%endif
BuildRequires: liblla-devel >= 0.2.0, liblla >= 0.2.0
Requires:      liblla >= 0.2.0


%description
The Q Light Controller (QLC) is an X11/Linux application to control DMX or 0-10V lighting systems like dimmers, scanners and other lighting effects. Our goal is to replace expensive and rather limited hardware lighting desks with free software.


%prep
%setup -q -n %{name}2
pushd  libs/
tar zxf %{SOURCE1}
popd
%patch1 -p0
./bootstrap

%build
export QTDIR=%_prefix/lib/qt3
export PATH=$PATH:%_prefix/lib/qt3/bin


%configure
make %{?_smp_mflags}


%install
rm -rf %buildroot
make install DESTDIR=%buildroot


%clean
rm -rf %buildroot


%files
%defattr(-,root,root,-)
/usr/bin/qlc
/usr/bin/qlcfixtureeditor
%{_libdir}/libqlc*
%{_libdir}/qlc/*
/usr/share/applications/qlc.desktop
/usr/share/applications/qlc-fixtureeditor.desktop
/usr/share/doc/qlc/*
/usr/share/pixmaps/qlc/*
/usr/share/pixmaps/qlc*
/usr/share/fixtures


%changelog
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
