%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

%define	soxlib	st
%define	major	0
%define	libname	%mklibname %{soxlib} %{major}

Summary:	A general purpose sound file conversion tool
Name:		sox
Version:	13.0.0
Release:	%mkrel 7
License: 	LGPL
Group:		Sound
Url:		http://sox.sourceforge.net/
Source0:	http://heanet.dl.sourceforge.net/sourceforge/sox/%{name}-%{version}.tar.bz2
#Patch0:		sox-13.0.0-fix-build-with-new-libflac.patch
#Patch1:		sox-13.0.0-flac-decoder-hack.patch
Patch2:		sox-13.0.0-new-flac.patch
BuildRequires:	oggvorbis-devel mad-devel gsm-devel libflac-devel libsndfile-devel
%if %build_plf
BuildRequires:	lame-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SoX (Sound eXchange) is a sound file format converter for Linux,
UNIX and DOS PCs. The self-described 'Swiss Army knife of sound
tools,' SoX can convert between many different digitized sound
formats and perform simple sound manipulation functions,
including sound effects.

Install the sox package if you'd like to convert sound file formats
or manipulate some sounds.

%if %build_plf
This package is in PLF as it was build with lame encoder support, which is in PLF.
%endif

%package -n	%{libname}
Summary:	Libraries for SoX
Group:		System/Libraries

%description -n	%{libname}
Libraries for SoX.

%package -n	%{libname}-devel
Summary:	Development headers and libraries for libst
Group:		Development/C
Provides:	lib%{soxlib}-devel = %{version}-%{release}
Provides:	%{soxlib}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
Development headers and libraries for libst.

%prep
%setup -q
#%patch0 -p1 -b .newflac
#%patch1 -p1 -b .flac_decoder_hack
%patch2 -p1 -b .newflac
autoconf

%build
CFLAGS="%{optflags} -DHAVE_SYS_SOUNDCARD_H=1 -D_FILE_OFFSET_BITS=64 -fPIC -DPIC" \
%configure2_5x
%make

%install
rm -rf %{buildroot}

%makeinstall_std

ln -sf play %{buildroot}%{_bindir}/rec

cat << EOF > %{buildroot}%{_bindir}/soxplay
#!/bin/sh

%{_bindir}/sox \$1 -t .au - > /dev/audio

EOF
chmod 755 %{buildroot}%{_bindir}/soxplay

ln -snf play %{buildroot}%{_bindir}/rec
ln -s play.1%{_extension} %{buildroot}%{_mandir}/man1/rec.1%{_extension}

rm -rf %{buildroot}%{_libdir}/*.la

%post   -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog README NEWS AUTHORS
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libst.so.%{major}*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/libst-config
%{_libdir}/libst.a
%{_libdir}/libst.so
%{_includedir}/*.h


%changelog
* Sat Apr 07 2007 Kevin Deldycke <kev@coolcavemen.com> 13.0.0-7mdv2007.0
- Backported from cooker to Mandriva 2007.0

* Tue Mar 06 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 13.0.0-6mdv2007.0
+ Revision: 133639
- obsolete sox-devel (fixes #29197)

* Sun Feb 18 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 13.0.0-5mdv2007.1
+ Revision: 122478
- use flac patches from cvs (P2), obsoletes P0 & P1

* Fri Feb 16 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 13.0.0-4mdv2007.1
+ Revision: 122017
- flac decoding seems broken, might be due to my flac patch, work around
  for now (P1)
- remove commented out code that was forgotten..

* Fri Feb 16 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 13.0.0-3mdv2007.1
+ Revision: 121588
- fix build with new flac version (P0)
- drop useless dependencies
- fix libification
- revert some changes

* Tue Feb 13 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 13.0.0-2mdv2007.1
+ Revision: 120267
- add missing requires and provides
- move libst-config to the right place

* Tue Feb 13 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 13.0.0-1mdv2007.1
+ Revision: 120262
- new version
- fix buildrequires
- move libraries to its own package
- set %%multiarch on libst-config
- spec file clean

* Mon Dec 18 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 12.18.2-2mdv2007.1
+ Revision: 98466
- sync deps of sox-devel with the output of libst-config --libs

* Sun Dec 03 2006 Emmanuel Andry <eandry@mandriva.org> 12.18.2-1mdv2007.1
+ Revision: 90204
- New version 12.18.2
  drop patch0

* Sat Oct 28 2006 Anssi Hannula <anssi@mandriva.org> 12.18.1-3mdv2007.1
+ Revision: 73607
- fix configure parameters
- Import sox



* Wed Sep 12 2006 Giuseppe Ghib� <ghibo@mandriva.com> 12.18.1-2mdv2007.0
- Force -fPIC -DPIC in CFLAGS for X86-64 linkage.

* Mon May 08 2006 Olivier Thauvin <nanardon@mandriva.org> 12.18.1-1mdk
- 12.18.1

* Mon Dec 12 2005 Per Øyvind Karlsen <pkarlsen@mandriva.com> 12.17.9-1mdk
- New release 12.17.9
- drop P0 (fixed upstream)

* Tue Aug 23 2005 Oden Eriksson <oeriksson@mandriva.com> 12.17.8-1mdk
- 12.17.8 (Minor bugfixes)

* Wed Dec 22 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 12.17.7-1mdk
- 12.17.7

* Sun Nov 21 2004 Michael Scherer <misc@mandrake.org> 12.17.6-2mdk
- Add plf build

* Wed Nov 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 12.17.6-1mdk
- 12.17.6
- merge Oden's changes which went to the wrong place:
	o drop P1, the CAN-2004-0557 fix is included
	o reorder patches, rediffed P0, P1
	o added the scripts
	o use system gsm lib (P2)

* Mon Nov 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 12.17.4-5mdk
- fix license
- cosmetics

* Fri Oct 08 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 12.17.4-4mdk
- Patch1: security fix for CAN-2004-0557

* Wed Aug 25 2004 Götz Waschk <waschk@linux-mandrake.com> 12.17.4-3mdk
- fix docs list
- patch to fix alsa build

* Wed Jul  9 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 12.17.4-2mdk
- rebuild for new devel provides

* Thu May 15 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 12.17.4-1mdk
- new version

* Sun Jul 21 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 12.17.3-4mdk
- recompile against new vorbis stuff

* Tue Jun 25 2002 Todd Lyons <tlyons@mandrakesoft.com> 12.17.3-3mdk
- Add ability to build with oggvorbis capability.  Source detects
  it properly, just add BuildRequires and Requires.
- Geoff
  - fix it so it looks nicer ;)

* Sat Jun 15 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 12.17.3-2mdk
- Remove Alpha fix for the time being (can only verify it doesn't
  apply, will check later to see if a re-diff is necessary).
- Remove commented and obsolete bzip2 manpage / strip binary code.

* Mon Apr 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 12.17.3-1mdk
- New and shiny sox.

* Sat Mar 09 2002 Yves Duret <yduret@mandrakesoft.com> 12.17.1-3mdk
- spec clean up: macros, s#Copyright#License# ...

* Fri Aug 03 2001 Gregory Letoquart <gletoquart@mandrakesoft.com> 12.17.1-2mdk
- New Website & Rebuild after Six month.

* Fri Feb 02 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 12.17.1-1mdk
- new and shiny source.
- use of %%configure.

* Sat Dec 23 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 12.17-2mdk
- alpha fix.

* Mon Nov 13 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 12.17-1mdk
- new and shiny version.
 - fix the build.

* Wed Aug 30 2000 Enzo Maggi <enzo@mandrakesoft.com> 12.16-9mdk
- minor fix in the spec

* Tue Aug 29 2000 Enzo Maggi <enzo@mandrakesoft.com> 12.16-8mdk
- simplified the installation

* Mon Aug 28 2000 Enzo Maggi <enzo@mandrakesoft.com> 12.16-7mdk
- fixed installation directories

* Fri Apr 07 2000 Christopher Molnar <molnarc@mandrakesoft.com> 12.16-6mdk
- fixed groups

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix dangling symlinks (use rpmlint luke).

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- SMP check/build

* Sat Aug 07 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- -DHAVE_SYS_SOUNDCARD_H=1, cause configure is slightly broken

* Thu Jul 22 1999 Gregus <gregus@etudiant.net>
- fr locale

* Tue Jul 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- A new life for the spec file :).
- 12.16.
- Removed obsoletes patchs.

* Tue Jun 01 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Cleanup from Mandrake adaptions

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Wed Jan 20 1999 Bill Nottingham <notting@redhat.com>
- allow spaces in filenames for play/rec

* Wed Dec  9 1998 Bill Nottingham <notting@redhat.com>
- fix docs

* Mon Nov 23 1998 Bill Nottingham <notting@redhat.com>
- update to 12.15

* Sat Oct 10 1998 Michael Maher <mike@redhat.com>
- fixed broken spec file

* Mon Jul 13 1998 Michael Maher <mike@redhat.com>
- updated source from Chris Bagwell.

* Wed Jun 23 1998 Michael Maher <mike@redhat.com>
- made patch to fix the '-e' option. BUG 580
- added buildroot

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Nov 06 1997 Erik Troan <ewt@redhat.com>
- built against glibc
