%define name libgpod
%define version 0.6.0
%define release %mkrel 3
%define major 3
%define libname %mklibname gpod %major
%define libnamedev %mklibname -d gpod

Summary: Library to access an iPod audio player
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.gz
License: LGPL
Group: System/Libraries
Url: http://www.gtkpod.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk+2-devel
BuildRequires: hal-devel dbus-glib-devel
BuildRequires: libsgutils-devel
BuildRequires: taglib-devel
BuildRequires: eject
BuildRequires: perl-XML-Parser

%description
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n %libname
Group: System/Libraries
Summary: Library to access an iPod audio player
Requires: eject
Requires: %name >= %version

%description -n %libname
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n %libnamedev
Group: Development/C
Summary: Library to access an iPod audio player
Requires: %libname = %version
Provides: %name-devel = %version-%release
Obsoletes: %mklibname -d gpod 2

%description -n %libnamedev
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

%package -n python-gpod
Group: Development/Python
Summary: Python module for iPod access
BuildRequires: python-gobject-devel
BuildRequires: python-devel
BuildRequires: mutagen
BuildRequires: swig
Requires: mutagen

%description -n python-gpod
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This is a Python binding for libgpod.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std
%find_lang %name
%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%_libdir/hal/libgpod-callout
%_bindir/ipod-read-sysinfo-extended
%_datadir/hal/fdi/policy/20thirdparty/*

%files -n %libname
%defattr(-,root,root)
%_libdir/lib*.so.%{major}*

%files -n %libnamedev
%defattr(-,root,root)
%_libdir/lib*.so
%attr(644,root,root)  %_libdir/lib*a
%_libdir/pkgconfig/*.pc
%_includedir/gpod-1.0/
%_datadir/gtk-doc/html/*

%files -n python-gpod
%defattr(-,root,root)
%py_platsitedir/gpod/




%changelog
* Sat Jan 26 2008 Kevin Deldycke <kev@coolcavemen.com> 0.6.0-3mdv2008.0
- backport from cooker to Mandriva 2008.0

* Mon Nov 12 2007 Götz Waschk <waschk@mandriva.org> 0.6.0-2mdv2008.1
+ Revision: 108087
- fix devel name

* Sun Nov 11 2007 Götz Waschk <waschk@mandriva.org> 0.6.0-1mdv2008.1
+ Revision: 108024
- fix buildrequires
- new version
- new major
- add new hal callout

* Sat Jun 23 2007 Götz Waschk <waschk@mandriva.org> 0.5.2-1mdv2008.0
+ Revision: 43402
- new version

* Mon Jun 18 2007 Götz Waschk <waschk@mandriva.org> 0.5.0-1mdv2008.0
+ Revision: 40887
- new version
- new major
- new python-gpod dep on mutagen


* Mon Jan 15 2007 Götz Waschk <waschk@mandriva.org> 0.4.2-2mdv2007.0
+ Revision: 109259
- just increase the release tag
- fix python path
- new version
- new major

* Thu Dec 14 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.4.0-3mdv2007.1
+ Revision: 97036
- Rebuild against new Python

  + Götz Waschk <waschk@mandriva.org>
    - fix python package on x86_64 (Colin Guthrie)
    - Import libgpod

* Sat Oct 07 2006 Götz Waschk <waschk@mandriva.org> 0.4.0-1mdv2007.1
- add python bindings
- fix buildrequires
- update file list
- New version 0.4.0

* Wed Aug 02 2006 Götz Waschk <waschk@mandriva.org> 0.3.2-2mdv2007.0
- fix buildrequires

* Sun Mar 05 2006 Götz Waschk <waschk@mandriva.org> 0.3.2-1mdk
- New release 0.3.2

* Wed Jan 25 2006 Götz Waschk <waschk@mandriva.org> 0.3.0-2mdk
- rebuild for new dbus

* Sun Dec 11 2005 Götz Waschk <waschk@mandriva.org> 0.3.0-1mdk
- New release 0.3.0
- use mkrel

* Sat Dec 03 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.2.0-3mdk
- add BuildRequires: perl-XML-Parser

* Thu Dec 01 2005 Frederic Crozat <fcrozat@mandriva.com> 0.2.0-2mdk
- Remove pmount dependency, it isn't needed at all

* Mon Nov 28 2005 Götz Waschk <waschk@mandriva.org> 0.2.0-1mdk
- initial package

