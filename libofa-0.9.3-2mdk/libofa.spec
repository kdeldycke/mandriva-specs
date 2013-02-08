%define name	libofa
%define version 0.9.3
%define release %mkrel 2
%define summary	Open Fingerprint Architecture library

%define major	0
%define libname	%mklibname ofa %major

Summary:	%{summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://www.musicdns.org/themes/musicdns_org/downloads/%{name}-%{version}.tar.bz2
Patch0:		libofa-build-fix.patch
License:	GPL
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url:		http://www.musicdns.org
BuildRequires:	fftw3-devel
BuildRequires:	libcurl-devel
BuildRequires:	libexpat-devel


%description
Currently, MusicDNS and the Open Fingerprint Architecture are being used to:

    * identify duplicate tracks, even when the metadata is different, MusicIP identifies the master recording.
    * fix metadata
    * find out more about tracks by connecting to MusicBrainz- the worlds largest music metabase community

%package -n	%{libname}
Summary:        %{summary}
Group:          System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
Currently, MusicDNS and the Open Fingerprint Architecture are being used to:

    * identify duplicate tracks, even when the metadata is different, MusicIP identifies the master recording.
    * fix metadata
    * find out more about tracks by connecting to MusicBrainz- the worlds largest music metabase community

%package -n	%{libname}-devel
Summary:	Files needed for developing applications which use litunepimp
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-devel
The %{name}-devel package includes the header files and .so libraries
necessary for developing libofa enabled tagging applications.

If you are going to develop libofa enabled tagging 
applications you should install %{name}-devel. You'll also need 
to have the %name package installed.

%package -n	%{libname}-static-devel
Summary:        Static libraries for libtunepimp
Group:          Development/C
Provides:       %{name}-static-devel = %{version}-%{release}
Requires:       %{libname}-devel = %{version}-%{release}

%description -n	%{libname}-static-devel
The %{name}-devel package includes the static libraries
necessary for developing libofa enabled tagging
applications using the %{name} library.

If you are going to develop libofa enabled tagging applications,
you should install %{name}-devel.  You'll also need to have the %name
package installed.

%prep
%setup -q
%patch0 -p0

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean
rm -rf %buildroot

%post -p /sbin/ldconfig -n %{libname}
%postun -p /sbin/ldconfig -n %{libname}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS README COPYING
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/libofa.pc
%{_libdir}/*.so
%{_libdir}/*.la

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
* Mon Jul 31 2006 Helio Castro <helio@mandriva.com> 0.5.0-2mdv2007.0
- Put right requires for fftw3-devel

* Sat Jul 22 2006 Emmanuel Andry <eandry@mandriva.org> 0.5.0-1mdv2007.0
- Initial Mandriva release
