%define name mlt
%define version 0.2.2
%define release %mkrel 10
%define major	0.2.2

%define libname		%mklibname %name %major
%define libnamedev	%mklibname %name %major -d
%define libname_orig	lib%{name}

%define use_mmx	0
%{?_with_mmx: %global use_mmx 1}
%{?_without_mmx: %global use_mmx 0}

Summary: Mutton Lettuce Tomato Nonlinear Video Editor
Name:		%{name}
Version:	%{version}
Release: 	%{release}
Source0:	%{name}-%{version}.tar.bz2
Patch1:		%{name}-%{version}-noO4.patch
Patch2:		mlt-0.2.2-linuxppc.patch
Patch3:		mlt-20070207.patch
Patch4:		mlt-0.2.2-sox13.patch
Patch5:		mlt-0.2.2-swscale.patch
License:	LGPL
Group:		Video
Url: 		http://mlt.sourceforge.net
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	pkgconfig
BuildRequires:	ffmpeg
BuildRequires:	ffmpeg-devel >= 0.4.9-3.pre1
BuildRequires:	glib2-devel
BuildRequires:	gtk2-devel
BuildRequires:	ladspa-devel
BuildRequires:	libdv-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	pango-devel
BuildRequires:	qt3-devel
BuildRequires:  quicktime-devel
BuildRequires:	SDL-devel
BuildRequires:	sox-devel >= 12.18.1-2mdv2007.0
BuildRequires:	ImageMagick
BuildRequires:	mad-devel
Requires: pango
Requires: gtk2
Requires: SDL
Requires: sox

%description
MLT is an open source multimedia framework, designed and developed for
television broadcasting.

It provides a toolkit for broadcasters, video editors, media players,
transcoders, web streamers and many more types of applications. The
functionality of the system is provided via an assortment of ready to
use tools, xml authoring components, and an extendible plug-in based
API.

%package -n     %{libname}
Summary:        Main library for mlt
Group:          System/Libraries
Provides:       %{libname_orig} = %{version}-%{release}

%description -n %{libname}
This package contains the libraries needed to run programs dynamically
linked with mlt.


%package -n     %{libnamedev}
Summary:        Headers for developing programs that will use mlt
Group:          Development/C
Requires:       %{libname} = %{version}
# mlt-config requires stuff from %{_datadir}/%{name}
Requires:	%{name} = %{version}
Provides:       %{name}-devel = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}

%description -n %{libnamedev}
This package contains the headers that programmers will need to develop
applications which will use mlt.


%prep
%setup -q
%patch1 -p1 -b .noO4
%patch2 -p1 -b .ppc
%patch3 -p1 -b .20070207
%patch4 -p1 -b .sox13
%patch5 -p1 -b .swscale
perl -pi -e 's,(QTLIBS=.+)/lib\b,\1/%{_lib},' src/modules/qimage/configure

%build
%configure2_5x \
	--disable-debug \
	--enable-gpl \
%if %use_mmx
	--enable-mmx \
%else
	--disable-mmx \
%endif
	--luma-compress \
	--enable-avformat \
	--avformat-shared=%{_prefix} \
	--enable-motion-est

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
%multiarch_binaries %{buildroot}%{_bindir}/mlt-config

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc docs COPYING README
%{_bindir}/albino
%{_bindir}/humperdink
%{_bindir}/inigo
%{_bindir}/miracle
%{_datadir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%multiarch %{multiarch_bindir}/mlt-config
%{_bindir}/mlt-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc



%changelog
* Sat Apr 07 2007 Kevin Deldycke <kev@coolcavemen.com> 0.2.2-10mdv2007.0
- Backported from cooker to Mandriva 2007.0

* Tue Mar 13 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.2.2-9mdv2007.1
+ Revision: 142397
- Rebuilt against latest ffmpeg.

* Mon Mar 12 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.2.2-8mdv2007.1
+ Revision: 141637
- Don't revert gb PPC patch.
- Better handling of avformat-swscale (for now disabled).

* Sun Mar 11 2007 Giuseppe Ghibò <ghibo@mandriva.com> 0.2.2-7mdv2007.1
+ Revision: 141361
- Unbzip2 patches.
- Added Patch3 from cvs (fix motion-est for x86_64).
- Added Patch4 to build with sox 13 (fix bug #29207).
- Added Patch5 (to enable --avformat-swscale).

  + Gwenole Beauchesne <gbeauchesne@mandriva.com>
    - lib{32,64} fixes

* Mon Dec 18 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.2.2-6mdv2007.1
+ Revision: 98492
- fix patch2: enable SSE optimizations for x86-64
- drop BuildRequires libavifile-devel (not used)
- patch2: fix build on ppc

* Mon Oct 30 2006 Anssi Hannula <anssi@mandriva.org> 0.2.2-5mdv2007.1
+ Revision: 73837
- buildrequires mad-devel
- buildrequires ImageMagick
- rebuild
- drop unused plf build switch
  fix invalid provides of libpackage
  fix requires of devel package

  + Andreas Hasenack <andreas@mandriva.com>
    - commit on behalf of Giuseppe Ghib?\195?\178 to get package in sync with svn:
      * Wed Sep 13 2006 Giuseppe Ghib?\195?\178 <ghibo@mandriva.com> 0.2.2-2mdv2007.0
      - Fix build for X86_64.
      - Fixed License.
      - Removed suffix in configure, so to let modules avformat built.

  + Jerome Martin <jmartin@mandriva.org>
    - import mlt-0.2.2-0.1.20060mdk


* Tue Jun 20 2006 Jerome Martin <jmartin@mandriva.org> 0.2.2-1
- Initial version

