# THIS PACKAGE IS HOSTED AT MANDRIVA SVN
# PLEASE DO NOT UPLOAD DIRECTLY BEFORE COMMIT

%define name libvisual
%define version 0.4.0
%define release %mkrel 1
%define major 0
%define libname %mklibname visual %major

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Audio visualisation framework
Source0: %{name}-%{version}.tar.bz2
License: LGPL
Group: System/Libraries
Url: http://localhost.nl/~synap/libvisual
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %mdkversion > 200600
BuildRequires:	X11-devel
%else
BuildRequires:	XFree86-devel
%endif

%description
Libvisual is a library that acts as a middle layer between
applications that want audio visualisation and audio visualisation
plugins.

Libvisual is aimed at developers who have a need for audio
visualisation and those who actually write the visualisation plugins.

#--------------------------------------------------------------------

%package -n %libname
Group: System/Libraries
Summary: Shared library of the audio visualisation framework 
Provides: %name = %version-%release
Obsoletes: libvisual-plugins < 0.4.0
Conflicts: gstreamer0.10-libvisual <= 0.10.7-1mdk

%description -n %libname
Libvisual is a library that acts as a middle layer between
applications that want audio visualisation and audio visualisation
plugins.

Libvisual is aimed at developers who have a need for audio
visualisation and those who actually write the visualisation plugins.

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root)
%doc README NEWS TODO ChangeLog AUTHORS
%_libdir/*.so.*
%_datadir/locale/*/*

#--------------------------------------------------------------------

%package -n %libname-devel
Group: Development/C
Summary: Header files of the audio visualisation framework 
Requires: %libname = %version
Provides: libvisual-devel = %version-%release

%description -n %libname-devel
Libvisual is a library that acts as a middle layer between
applications that want audio visualisation and audio visualisation
plugins.

Libvisual is aimed at developers who have a need for audio
visualisation and those who actually write the visualisation plugins.

%files -n %libname-devel
%defattr(-,root,root)
%_includedir/*
%_libdir/*.so
%_libdir/*.la
%_libdir/pkgconfig/*

#--------------------------------------------------------------------

%prep
%setup -q

%build
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




%changelog
* Tue May 30 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-05-30 19:43:56 (31733)
- New upstream version

* Tue May 30 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-05-30 18:57:29 (31729)
- import libvisual-0.2.0-5mdk

* Sun Apr 30 2006 Stefan van der Eijk <stefan@eijk.nu> 0.2.0-5mdk
- rebuild for sparc

* Mon Aug 22 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.2.0-4mdk
- reconstruct from cvs
- only build lv_video_mmx.c with -mmmx

* Mon Jun 20 2005 Götz Waschk <waschk@mandriva.org> 0.2.0-3mdk
- enable mmx

* Sat Feb 12 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.2.0-2mdk
- Patch1: fix ppc build

* Thu Feb 10 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.2.0-1mdk
- 0.2.0

* Tue Nov 23 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.7-3mdk
- fix provides

* Fri Oct 15 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.7-2mdk
- fix openGL build

* Fri Oct 15 2004 Goetz Waschk <waschk@linux-mandrake.com> 0.1.7-1mdk
- New release 0.1.7

* Sun Sep 12 2004 Goetz Waschk <waschk@linux-mandrake.com> 0.1.6-1mdk
- New release 0.1.6

* Wed Jun 30 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.5-1mdk
- fix installation
- New release 0.1.5

* Fri Jun 25 2004 Götz Waschk <waschk@linux-mandrake.com> 0.1.4-1mdk
- initial package

