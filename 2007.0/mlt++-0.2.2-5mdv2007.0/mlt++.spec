%define name		mlt++
%define version		0.2.2
%define release		%mkrel 5
%define major		0.2.2

%define libname		%mklibname %name %major
%define libnamedev	%mklibname %name %major -d
%define libname_orig	lib%{name}

Summary: 	C++ bindings for MLT
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		%{name}-%{version}.tar.bz2
Group:		Video
Url:		http://mlt.sourceforge.net/
License:	LGPL
BuildRoot:	%{_tmppath}/%name-%{version}-root
BuildRequires:	mlt-devel

%description
MLT++ - C++ bindings to MLT


%package -n	%{libname}
Summary:	Main library for mlt++
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with mlt++.


%package -n     %{libnamedev}
Summary:        Headers for developing programs that will use mlt
Group:          Development/C
Requires:       %{libname} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}

%description -n %{libnamedev}
This package contains the headers that programmers will need to develop
applications which will use mlt++.


%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc AUTHORS CUSTOMISING HOWTO README
%{_includedir}/*
%{_libdir}/lib*.so


%changelog
* Sat Apr 07 2007 Kevin Deldycke <kev@coolcavemen.com> 0.2.2-5mdv2007.0
- Backported from cooker to Mandriva 2007.0

* Sun Mar 11 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.2.2-4mdv2007.1
+ Revision: 141366
- Rebuilt against latest mlt package.

* Tue Oct 31 2006 Anssi Hannula <anssi@mandriva.org> 0.2.2-3mdv2007.1
+ Revision: 73975
- rebuild
- commit on behalf of Giuseppe Ghib?\195?\178 to get package in sync with svn:
  * Fri Sep 15 2006 Giuseppe Ghib?\195?\178 <ghibo@mandriva.com> 0.2.2-2mdv2007.0
  - Reconstructed SPEC file because .src.rpm get lost.

  + Jerome Martin <jmartin@mandriva.org>
    - import mlt++-0.2.2-1mdv2007.0


* Tue Jun 20 2006 Jerome Martin <jmartin@mandriva.org> 0.2.2-1
- Initial version

