%define name libvisual-plugins
%define version 0.4.0
%define release %mkrel 2

Summary: Visualisation plugins for applications based on libvisual
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: System/Libraries
Url: http://localhost.nl/~synap/libvisual/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes: libvisual-nebulus
Obsoletes: libvisual-gforce
Provides: libvisual-nebulus
Provides: libvisual-gforce
BuildRequires: libvisual-devel >= %version
BuildRequires: esound-devel
BuildRequires: bison
BuildRequires: chrpath
%if %mdkversion > 200600
BuildRequires:	X11-devel
%else
BuildRequires:	XFree86-devel
%endif

%description
Libvisual is a library that acts as a middle layer between
applications that want audio visualisation and audio visualisation
plugins.

This package contains the libvisual example plugins.
%prep
%setup -q

%build
%ifarch %ix86
export CFLAGS="-mmmx %optflags"
%endif
./configure \
   --prefix=%_prefix \
   --libdir=%_libdir \
   --mandir=%_mandir \
   --datadir=%_datadir 

%make

%install
rm -rf %buildroot

make DESTDIR=%buildroot install

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog NEWS
%_libdir/*
%_datadir/*



%changelog
* Fri Jun 30 2006 GÃ¶tz Waschk <waschk@mandriva.org>
+ 2006-06-30 15:01:46 (38239)
- fix buildrequires

* Tue May 30 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-05-30 20:08:21 (31737)
- New upstream version

* Tue May 30 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-05-30 19:47:07 (31734)
- import libvisual-plugins-0.2.0-4mdk

* Thu Feb 16 2006 Götz Waschk <waschk@mandriva.org> 0.2.0-4mdk
- enable mmx to make it build
- disable the infinite plugin
- use mkrel

* Tue Feb 15 2005 Götz Waschk <waschk@linux-mandrake.com> 0.2.0-3mdk
- fix buildrequires

* Fri Feb 11 2005 Götz Waschk <waschk@linux-mandrake.com> 0.2.0-2mdk
- remove rpaths
- obsoletes libvisual-nebulus and libvisual-gforce

* Thu Feb 10 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.2.0-1mdk
- 0.2.0

* Fri Oct 15 2004 Goetz Waschk <waschk@linux-mandrake.com> 0.1.7-1mdk
- New release 0.1.7

* Mon Sep 13 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.6-1mdk
- requires new libvisual
- New release 0.1.6

* Thu Jul 01 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.5-1mdk
- initial package

