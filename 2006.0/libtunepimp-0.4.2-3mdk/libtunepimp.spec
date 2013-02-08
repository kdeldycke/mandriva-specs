%define major	3
%define libname	%mklibname tunepimp %major

Name:	libtunepimp
Version:	0.4.2
Release:	%mkrel 3
Epoch: 1
Summary: A library for creating MusicBrainz enabled tagging applications
Source0:	ftp://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.gz
Patch0: libtunepimp-0.4.2-CVE-2006-3600.diff
License:	LGPL
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Url:		http://www.musicbrainz.org/products/tunepimp/
BuildRequires:	libflac-devel
BuildRequires:	readline-devel
BuildRequires:	libmad-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	libmusicbrainz-devel
BuildRequires:	libcurl-devel
BuildRequires:	libofa-devel
BuildRequires:	taglib-devel
BuildRequires:	libmpcdec-devel

%description
The TunePimp library (also referred to as libtunepimp) is
a development library geared towards developers who wish
to create MusicBrainz enabled tagging applications. 

#-----------------------------------------------------------

%package -n	tunepimp-utils
Summary:        A library for creating MusicBrainz enabled tagging applications
Group:          Sound
Obsoletes: %{_lib}tunepimp2-utils
Obsoletes: %{_lib}tunepimp5-utils

%description -n tunepimp-utils
This package contains %{name} tools

%files -n tunepimp-utils
%defattr(-,root,root)
%doc AUTHORS ChangeLog INSTALL README README.LGPL TODO
%{_bindir}/*

#-----------------------------------------------------------

%package -n	tunepimp-plugins
Summary: A library for creating MusicBrainz enabled tagging applications
Group: Sound
Obsoletes: %{_lib}tunepimp2-plugins
Obsoletes: %{_lib}tunepimp5-plugins

%description -n tunepimp-plugins
This package contains %{name} plugins

%files -n tunepimp-plugins
%defattr(-,root,root)
%{_libdir}/tunepimp/plugins/*.tpp

#-----------------------------------------------------------

%package -n	%{libname}
Summary:        A library for creating MusicBrainz enabled tagging applications
Group:          System/Libraries

%description -n	%{libname}
The TunePimp library (also referred to as libtunepimp) is
a development library geared towards developers who wish
to create MusicBrainz enabled tagging applications.

%post -p /sbin/ldconfig -n %{libname}
%postun -p /sbin/ldconfig -n %{libname}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

#-----------------------------------------------------------

%package -n	%{libname}-devel
Summary:	Files needed for developing applications which use litunepimp
Group:		Development/C
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Obsoletes: %{_lib}tunepimp2-devel
Obsoletes: %{_lib}tunepimp5-devel

%description -n	%{libname}-devel
The %{name}-devel package includes the header files and .so libraries
necessary for developing MusicBrainz enabled tagging applications.

If you are going to develop MusicBrainz enabled tagging 
applications you should install %{name}-devel. You'll also need 
to have the %name package installed.

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la

#-----------------------------------------------------------

%package -n	%{libname}-static-devel
Summary:        Static libraries for libtunepimp
Group:          Development/C
Provides:       %{name}-static-devel = %{version}-%{release}
Requires:       %{libname}-devel = %{epoch}:%{version}-%{release}

%description -n	%{libname}-static-devel
The %{name}-devel package includes the static libraries
necessary for developing MusicBrainz enabled tagging
applications using the %{name} library.

If you are going to develop MusicBrainz enabled tagging applications,
you should install %{name}-devel.  You'll also need to have the %name
package installed.

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/*.a

#-----------------------------------------------------------

%prep
%setup -q
%patch0 -p0

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
rm -rf examples/plugins/tta.tpp
%makeinstall_std


%clean
rm -rf %buildroot





%changelog
* Wed Aug 30 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-30 21:19:23 (58886)
- Raise release

* Wed Aug 30 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-30 21:17:45 (58885)
- Security update:
  http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-3600
  Referenced by http://bugs.musicbrainz.org/ticket/1764

* Tue Aug 08 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-08 23:08:26 (54629)
- Right obsoletes

* Thu Aug 03 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-03 16:13:34 (43320)
- Add missing source

* Thu Aug 03 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-03 16:13:07 (43319)
- Ok, enough with broken libraries. tunepimp 0.5 not work with *any* of included
  programs on distro, and the main one, Amarok, will not include upgrade sooner
  for this version. Reverting for most stable accepted, 0.4.2. In the future we
  need try to be carefull to no upgrade libraries without have sure that all
  affected programs will work.

* Thu Aug 03 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-08-03 15:22:13 (43295)
- import libtunepimp-0.5.0-3mdv2007.0

* Mon Jul 31 2006 Helio Chissini de Castro <helio@mandriva.com> 0.5.0-3mdv2007.0
- Soname is 5 now, no 2. Changing for smooth upgrade.

* Thu Jul 27 2006 Emmanuel Andry <eandry@mandriva.org> 0.5.0-2mdv2007.0
- fix buildrequires

* Tue Jul 25 2006 Emmanuel Andry <eandry@mandriva.org> 0.5.0-1mdv2007.0
- 0.5.0
- builrequires libcurl-devel libofa-devel (created package libofa for this) taglib-devel
- create plugins package

* Sat Nov 26 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.3.0-4mdk
- fix conflict with trm by renaming the example (#19019)

* Mon Apr 18 2005 Götz Waschk <waschk@mandriva.org> 0.3.0-3mdk
- rebuild for new flac

* Sat Jan 22 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.3.0-2mdk
- rebuild for new readline
- wipe out buildroot at the beginning of %%install
- don't ship the same documents with every package

* Mon Dec 13 2004 Laurent Culioli <laurent@mandrake.org> 0.3.0-1mdk
- initial release.

