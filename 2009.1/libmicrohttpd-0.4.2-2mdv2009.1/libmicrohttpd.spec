%define major 5
%define shortname microhttpd
%define libname	%mklibname %shortname %major
%define develname %mklibname -d %shortname
%define sdevelname %mklibname -d -s %shortname

Name:		libmicrohttpd
Version:	0.4.2
Release:	%mkrel 2
URL:		http://gnunet.org/libmicrohttpd/
Source:		http://gnunet.org/libmicrohttpd/download/%{name}-%{version}.tar.gz
License:	GPLv2+
Summary:	Small C library to run an HTTP server
Group:		System/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libcurl-devel
%description
libmicrohttpd is a small C library that is supposed to make it easy to
run an HTTP server as part of another application. Key features that
distinguish libmicrohttpd from other projects are:

	* C library: fast and small
	* API is simple, expressive and fully reentrant
	* Implementation is (largely) http 1.1 compliant
	* HTTP server can listen on multiple ports
	* Support for IPv6
	* Creates binary of only 22k (for now)
	* Three different threading models

libmicrohttpd was started because the author needed an easy way to add
a concurrent HTTP server to other projects. Existing alternatives were
either non-free, not reentrant, standalone, of terrible code quality or
a combination thereof. Do not use libmicrohttpd if you are looking for
a standalone http server, there are many other projects out there that
provide that kind of functionality already. However, if you want to be
able to serve simple WWW pages from within your C or C++ application,
check it out.

%package -n %libname
Summary:	Small C library to run an HTTP server
Group:		System/Libraries

%description -n %libname
libmicrohttpd is a small C library that is supposed to make it easy to
run an HTTP server as part of another application. Key features that
distinguish libmicrohttpd from other projects are:

	* C library: fast and small
	* API is simple, expressive and fully reentrant
	* Implementation is (largely) http 1.1 compliant
	* HTTP server can listen on multiple ports
	* Support for IPv6
	* Creates binary of only 22k (for now)
	* Three different threading models

libmicrohttpd was started because the author needed an easy way to add
a concurrent HTTP server to other projects. Existing alternatives were
either non-free, not reentrant, standalone, of terrible code quality or
a combination thereof. Do not use libmicrohttpd if you are looking for
a standalone http server, there are many other projects out there that
provide that kind of functionality already. However, if you want to be
able to serve simple WWW pages from within your C or C++ application,
check it out.

%package -n %develname
Summary:	Development files for %libname
Group:		System/Libraries
Provides:	%name-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
%description -n %develname
Development files for %libname

%package -n %sdevelname
Summary:	Static libraries for %libname
Group:		System/Libraries
Provides:	%name-static-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{develname} = %{version}-%{release}
%description -n %sdevelname
Static libraries for %libname

%prep
%setup -q

%build
%configure2_5x
# makefile doesn't support running multiple jobs simultaneously
%{__make}

%install
%{__rm} -Rf %{buildroot}
%makeinstall_std

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%post -n %develname
%_install_info microhttpd.info

%preun -n %develname
%_remove_install_info microhttpd.info

%files -n %libname
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/%{name}.so.%{major}*
%{_mandir}/man3/%{name}.3.*

%files -n %develname
%{_includedir}/%{shortname}.h
%{_libdir}/%{name}.so
%{_libdir}/%{name}.la
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/info/*

%files -n %sdevelname
%{_libdir}/%{name}.a



%changelog
*  Fri May 29 2009 Kevin Deldycke <kevin@deldycke.com> 0.4.2-1mdv2009.1
- Upgrade to libmicrohttpd 0.4.2
- Increase major revision number
- Rebuild RPM for Mandriva 2009.1

* Fri Aug 08 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.3.1-2mdv2009.0
+ Revision: 267893
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed May 28 2008 Funda Wang <fundawang@mandriva.org> 0.3.1-1mdv2009.0
+ Revision: 212197
- New version 0.3.1

  + Thierry Vignaud <tvignaud@mandriva.com>
    - fix no-buildroot-tag

* Sun Feb 03 2008 Funda Wang <fundawang@mandriva.org> 0.2.1-1mdv2008.1
+ Revision: 161659
- update to new version 0.2.1

* Fri Dec 28 2007 Nicolas Vigier <nvigier@mandriva.com> 0.2.0-1mdv2008.1
+ Revision: 138879
- new version

* Tue Dec 18 2007 Nicolas Vigier <nvigier@mandriva.com> 0.1.2-1mdv2008.1
+ Revision: 132256
- new version

* Mon Aug 20 2007 Nicolas Vigier <nvigier@mandriva.com> 0.0.3-1mdv2008.0
+ Revision: 67318
- new version 0.0.3

* Tue Aug 14 2007 Nicolas Vigier <nvigier@mandriva.com> 0.0.1-1mdv2008.0
+ Revision: 63406
- Import libmicrohttpd

