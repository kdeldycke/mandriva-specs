%define lib_major 2
%define lib_name %mklibname ofx %{lib_major}

Summary: LibOFX library provides support for OFX command responses
Name: libofx
Version: 0.8.0
Release: 2mdk
Source: http://download.sourceforge.net/libofx/%{name}-%{version}.tar.bz2
Patch0: libofx-0.7.0-c++fixes.patch.bz2
Group:	System/Libraries
License: GPL
URL: http://libofx.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: OpenSP-devel
BuildRequires: libcurl-devel

%description
This is the LibOFX library.  It is a API designed to allow applications to
very easily support OFX command responses, usually provided by financial
institutions.  See http://www.ofx.net/ofx/default.asp for details and
specification. LibOFX is based on the excellent OpenSP library written by
James Clark, and now part of the OpenJADE http://openjade.sourceforge.net/
project.  OpenSP by itself is not widely distributed.  OpenJADE 1.3.1 includes
a version on OpenSP that will link, however, it has some major problems with
LibOFX and isn't recommended.  Since LibOFX uses the generic interface to
OpenSP, it should be compatible with all recent versions of OpenSP (It has
been developed with OpenSP-1.5pre5).  LibOFX is written in C++, but provides a
C style interface usable transparently from both C and C++ using a single
include file.



%package -n %{lib_name}
Summary:        Libraries for libofx
Group:          System/Libraries
Requires: %{name} >= %{version}-%{release}

%description -n %{lib_name}
This package provides libraries to use libofx.

%package -n %{lib_name}-devel
Group:	Development/C
Summary: Libraries needed to develop for libofx
Requires: %{lib_name} = %{version}
Provides: libofx-devel = %{version}-%{release}
Requires: OpenSP-devel

%description -n %{lib_name}-devel
Libraries needed to develop for libofx.


%prep
%setup -q
%patch0 -p1 -b .c++fixes

%build
# FIXME: better make it lib64 aware in configure script
%configure2_5x --with-opensp-libs=%{_libdir}

%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

#remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/libofx

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README totest.txt doc/html 
%{_bindir}/*
%{_datadir}/libofx

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Mon Dec 05 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.8.0-2mdk
- add BuildRequires: libcurl-devel

* Fri Dec  2 2005 Götz Waschk <waschk@mandriva.org> 0.8.0-1mdk
- major 2
- New release 0.8.0

* Wed Aug 24 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.7.0-2mdk
- c++ fixes

* Mon Dec 13 2004 Götz Waschk <waschk@linux-mandrake.com> 0.7.0-1mdk
- major 1
- drop patch
- New release 0.7.0

* Wed Jun 16 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.6.6-2mdk
- Rebuild 

* Thu Jan 15 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.6.6-1mdk
- Release 0.6.6

* Thu Oct  2 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.5-2mdk
- lib64 fixes

* Fri Sep 12 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 0.6.5-1mdk
- Release 0.6.5

* Tue Apr 22 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 0.6.4-1mdk
- Release 0.6.4

* Thu Apr  3 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 0.6.3-1mdk
- Release 0.6.3

* Tue Feb  4 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 0.6.2-1mdk
- Initial mandrake package
