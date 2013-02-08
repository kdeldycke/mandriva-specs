%define name libgpod
%define version 0.3.2
%define release %mkrel 1
%define major 0
%define libname %mklibname gpod %major

Summary: Library to access an iPod audio player
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/gtkpod/%{name}-%{version}.tar.bz2
License: LGPL
Group: System/Libraries
Url: http://www.gtkpod.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk+2-devel
BuildRequires: hal-devel
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

%package -n %libname-devel
Group: Development/C
Summary: Library to access an iPod audio player
Requires: %libname = %version
Provides: %name-devel = %version-%release

%description -n %libname-devel
libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.


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

%files -n %libname
%defattr(-,root,root)
%_libdir/lib*.so.%{major}*

%files -n %libname-devel
%defattr(-,root,root)
%_libdir/lib*.so
%attr(644,root,root)  %_libdir/lib*a
%_libdir/pkgconfig/*.pc
%_includedir/gpod-1.0/


%changelog
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
