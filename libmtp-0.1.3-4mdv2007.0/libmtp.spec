%define	name	libmtp
%define	version	0.1.3
%define release %mkrel 4
%define major	5
%define	libname	%mklibname mtp %major

Name:		%{name}
Summary:	Implementation of Microsoft's Media Transfer Protocol
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	LGPL
URL:		http://libmtp.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		archos.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	pkgconfig libusb-devel doxygen

%description
libmtp is an implementation of Microsoft's Media Transfer Protocol (MTP)
in the form of a library suitable primarily for POSIX compliant
operating systems. We implement MTP Basic, the stuff proposed for
standardization. MTP Enhanced is for Windows only, if we implement
it, well that depends...

It was initially based on (forked from) the great libptp2 library
by Mariusz Woloszyn but has since been moved over to follow Marcus
Meissners and Hubert Figuere's libgphoto2 fork of libptp2 (or is libptp2
 a fork of libgphoto?). The core implementation is identical to
libgphoto2, there is just a different API adapted to portable media
players.

%package -n	%{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n	%{libname}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q
%patch0 -p1

%build
%configure --enable-hotplugging --disable-static --program-prefix=mtp-
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
#rm -rf $RPM_BUILD_ROOT%{_docdir}
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING README
%{_bindir}/*
%{_libdir}/libmtp.so.%{major}
%{_libdir}/libmtp.so.%{major}.*
%{_datadir}/doc/*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}.la
%{_libdir}/pkgconfig/*


%changelog
* Sat Feb 10 2007 Kevin Deldycke <kev@coolcavemen.com> 0.1.3-4mdv2007.0
- Backport from cooker to Mandriva 2007

* Sun Feb 04 2007 Emmanuel Andry <eandry@mandriva.org> 0.1.3-3mdv2007.0
+ Revision: 116129
- add patch from sourceforge for various fixes

* Tue Jan 23 2007 Emmanuel Andry <eandry@mandriva.org> 0.1.3-2mdv2007.1
+ Revision: 112565
- configure with --program-prefix=mtp- (#bug 27710)
  disable static

* Mon Jan 22 2007 Emmanuel Andry <eandry@mandriva.org> 0.1.3-1mdv2007.1
+ Revision: 111646
- New version 0.1.3

* Sun Jan 14 2007 Emmanuel Andry <eandry@mandriva.org> 0.1.2-1mdv2007.1
+ Revision: 108785
- New release 0.1.2
  New major 5

* Tue Dec 26 2006 Emmanuel Andry <eandry@mandriva.org> 0.1.0-3mdv2007.1
+ Revision: 102088
- enable hotplugging
  include documentation

* Sun Dec 10 2006 Anssi Hannula <anssi@mandriva.org> 0.1.0-2mdv2007.1
+ Revision: 94547
- fix libname

* Sat Dec 09 2006 Emmanuel Andry <eandry@mandriva.org> 0.1.0-1mdv2007.1
+ Revision: 94179
- New version 0.1.0
  new major

* Sun Dec 03 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.21-2mdv2007.1
+ Revision: 90223
- buildrequires doxygen

* Sun Dec 03 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.21-1mdv2007.1
+ Revision: 90152
- New version 0.0.21
- Import libmtp



* Tue Aug 29 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.15-1mdv2007.0
- 0.0.15

* Wed Aug 23 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.12-1mdv2007.0
- initial Mandriva release
