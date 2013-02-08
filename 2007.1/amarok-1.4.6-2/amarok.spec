%define __libtoolize /bin/true

%define libname_orig lib%{name}
%define libname %mklibname %{name} 0

%define name   amarok
%define version 1.4.6
%define release %mkrel 2

#Add MySQL support
%define build_mysql 1
%{?_with_mysql: %global build_mysql 1}

#Add PostgreSQL support
%define build_postgresql 1
%{?_with_postgresql: %global build_postgresql 1}

%define unstable 0
%{?_with_unstable: %global unstable 1}

%if %unstable
%define dont_strip 1
%endif

Summary:        A powerful media player for Kde
Name:           %{name}
Version:        %{version}
Release:        %{release}
Epoch:          1
License:        GPL
Url:            http://amarok.kde.org/
Group:          Sound
Source0:        %{name}-%{version}.tar.bz2
# fwang: add lyric script for Chinese songs
# http://www.kde-apps.org/content/show.php/Lyrics_CN?content=50120
Source1:	amarok-1.4.5-lyrics_cn.amarokscript.tar.gz
Patch0:         amarok-1.4.1-fix-initial-preference.patch
Patch1:         amarok-1.3-fix-default-config.patch
Patch2:         amarok-1.2-fix-config.patch
Patch3:         amarok-1.4-beta2-add-multimedia-shortcut.patch
#(nl): Disable for the moment as it had been reported that this patch is broken.
Patch4:         amarok-1.4.0-use-mandriva-directory.patch
Patch6:         amarok-add-radios.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  libtaglib-devel >= 1.4
BuildRequires:  kdemultimedia-devel
BuildRequires:  libxine-devel
BuildRequires:  libvisual-devel >= 0.4.0
BuildRequires:  libtunepimp-devel >= 1:0.4.2
BuildRequires:  kdebase-devel
BuildRequires:  libxml2-utils
#(nl) if k3b isn't installed before compilation, the entry on the menu will ALWAYS be grey'ed
#     so for the moment this is important to have this installed
#     http://www.sebruiz.net/?p=64
BuildRequires:  k3b-devel
BuildRequires:  libifp-devel
BuildRequires:  SDL-devel
BuildRequires:  libgpod-devel
BuildRequires:  libnjb-devel
BuildRequires:  sqlite3-devel
BuildRequires:  libmtp-devel
%if %build_mysql
BuildRequires:  mysql-devel
%endif
%if %build_postgresql
BuildRequires:  postgresql-devel
%endif
BuildRequires:  exscalibar-devel
BuildRequires:  mesaglut-devel
BuildRequires:  libgpod-devel
BuildRequires:  ruby-devel
BuildRequires:  gpm-devel

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires: amarok-engine
Requires: amarok-scripts
Requires: %{libname} = %epoch:%{version}
Requires: tunepimp-plugins

Requires:       exscalibar
Requires:       libvisual-plugins >= 0.4.0
# Allow to make smouth updates
Conflicts :     amarok-engine-arts
Conflicts :     amarok-engine-gstreamer
Conflicts :     amarok-engine-akode
#(nl) amarok-engine-gstreamer0.10 has been removed for amarok 1.4.0 as it is not
# ready for release but will be (perharps) back for amarok 1.4.3 or later
Conflicts :     amarok-engine-gstreamer0.10

Obsoletes:      amarok-engine-arts                 <= 1.4-0.beta1_rc1.10mdk
Obsoletes:      amarok-engine-gstreamer            <= 1.4-0.beta1_rc1.10mdk
Obsoletes:      amarok-engine-akode                <= 1.4-0.beta2.3mdk
Obsoletes:      amarok-engine-gstreamer0.10        <= 1.4-0.beta3.7mdk

%description
Feature Overview

* Music Collection:
You have a huge music library and want to locate tracks quickly? Let amaroK's
powerful Collection take care of that! It's a database powered music store,
which keeps track of your complete music library, allowing you to find any
title in a matter of seconds.

* Intuitive User Interface:
You will be amazed to see how easy amaroK is to use! Simply drag-and-drop files
into the playlist. No hassle with complicated  buttons or tangled menus.
Listening to music has never been easier!

* Streaming Radio:
Web streams take radio to the next level: Listen to thousands of great radio
stations on the internet, for free! amaroK provides excellent streaming
support, with advanced features, such as displaying titles of the currently
playing songs.

* Context Browser:
This tool provides useful information on the music you are currently listening
to, and can make listening suggestions, based on your personal music taste. An
innovate and unique feature.

* Visualizations:
amaroK is compatible with XMMS visualization plugins. Allows you to use the
great number of stunning visualizations available on the net. 3d visualizations
with OpenGL are a great way to enhance your music experience.

%post
%update_menus
%{update_desktop_database}

%postun
%clean_menus
%{clean_desktop_database}

%files -f %name.lang
%defattr(-,root,root)
%doc README AUTHORS COPYING ChangeLog
%{_bindir}/*
%{_libdir}/kde3/konqsidebar_universalamarok.*
%{_libdir}/kde3/libamarok_*
%{_datadir}/apps/konqueror/servicemenus/amarok_*
%{_datadir}/applications/kde/amarok.desktop
%{_datadir}/servicetypes/amarok_*
%{_datadir}/services/amarok*
%dir %{_datadir}/apps/amarok
%{_datadir}/apps/amarok/*
%{_datadir}/apps/profiles/amarok.profile.xml
%{_datadir}/config/amarokrc
%{_datadir}/config.kcfg/amarok.kcfg
%{_datadir}/apps/konqsidebartng/*
%{_miconsdir}/*
%{_iconsdir}/*
%{_liconsdir}/*
%doc %_docdir/HTML/*/amarok/*
%exclude %_datadir/apps/amarok/scripts/
%exclude %_libdir/kde3/libamarok_xine-engine.*
%exclude %_datadir/services/amarok_xine-engine.desktop
%exclude %_datadir/config.kcfg/xinecfg.kcfg

#--------------------------------------------------------------------

%package scripts
Summary:        Scripts for amarok
Group:          Graphical desktop/KDE
Requires:       %name = %epoch:%version-%release
URL:            http://amarok.kde.org/
Requires:       kjsembed
Requires:       ruby
Requires:       python
Requires:	%{libname}-scripts = %epoch:%version-%release


%description scripts
This package includes python scripts for amarok.

%files scripts
%defattr(-,root,root)
%dir %{_datadir}/apps/amarok/scripts/
%{_datadir}/apps/amarok/scripts/*

#--------------------------------------------------------------------

%package -n %{libname}-scripts
Summary:        Library scripts for amarok
Group:          Graphical desktop/KDE
Requires:       %name = %epoch:%version-%release
URL:            http://amarok.kde.org/
Requires:       ruby

%description -n %{libname}-scripts
This package includes library scripts for amarok.

%files -n %{libname}-scripts
%defattr(-,root,root)
%_libdir/ruby_lib/http11.rb
%_libdir/ruby_lib/*.la
%_libdir/ruby_lib/*.so.*

#--------------------------------------------------------------------
%post -n %{libname}-scripts -p /sbin/ldconfig
%postun -n %{libname}-scripts -p /sbin/ldconfig


%package -n %{libname}-devel-scripts
Summary:        Library scripts for amarok
Group:          Graphical desktop/KDE
Requires:       %{libname}-scripts = %epoch:%{version}
URL:            http://amarok.kde.org/
Requires:       ruby

%description -n %{libname}-devel-scripts
This package includes devel for scripts for amarok.

%files -n %{libname}-devel-scripts
%defattr(-,root,root)
%_libdir/ruby_lib/*.so

#--------------------------------------------------------------------

%package engine-xine
Summary:        Amarok xine engine
Group:          Graphical desktop/KDE
Provides:       amarok-engine
URL:            http://amarok.kde.org/
Requires:       xine-lib
Requires:       xine-plugins
Requires:       %name = %epoch:%version-%release

%description engine-xine
This package includes xine engine for amarok.

%files  engine-xine
%defattr(-,root,root)
%{_libdir}/kde3/libamarok_xine-engine.*
%{_datadir}/services/amarok_xine-engine.desktop
%{_datadir}/config.kcfg/xinecfg.kcfg

#--------------------------------------------------------------------

%package -n %{libname}
Summary:        Amarok  library
Group:          Graphical desktop/KDE
Provides:       %{libname_orig} = %epoch:%{version}-%{release}
Requires:       %name = %epoch:%version-%release

%description -n %{libname}
Library for Amarok

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libamarok.so.*

#--------------------------------------------------------------------

%package -n %{libname}-devel
Summary:        Headers of %name for development
Group:          Development/C
Requires:       %{libname} = %epoch:%{version}
Provides:       %{name}-devel = %epoch:%{version}-%{release}
Provides:       %{libname_orig}-devel = %epoch:%{version}-%{release}

%description -n %{libname}-devel
Headers of %{name} for development.

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libamarok.la
%{_libdir}/libamarok.so

#--------------------------------------------------------------------

%prep
%setup -q -n %name-%version -a 1
%patch0 -p1 -b .fix_amarok_initial_preference
%patch1 -p0 -b .fix_amarok_default_config_file
#reapply
#%patch2 -p1 -b .fix_default_config
%patch3 -p1 -b .fix_add_multimedia_shortcut
#%patch4 -p0 -b .use_mandriva_music_directory
%patch6 -p0 -b .add_some_radios

%build
export QTDIR=%_prefix/lib/qt3

%configure2_5x \
   --with-xine \
   --without-included-sqlite \
%if %mdkversion > 200600
   --with-libgpod \
%endif
   --without-helix \
   --without-xmms \
   --disable-rpath \
   --with-ifp \
   --disable-debug \
   --disable-warnings \
   --with-libmtp \
%if %build_mysql
   --enable-mysql \
%endif
%if %build_postgresql
   --enable-postgresql \
%endif

%make

%install
rm -rf %buildroot

%{makeinstall_std}

rm -rf %{buildroot}/%{_iconsdir}/*
install -m644 amarok/src/hi16-app-amarok.png -D %{buildroot}/%{_miconsdir}/%{name}.png
install -m644 amarok/src/hi32-app-amarok.png -D %{buildroot}/%{_iconsdir}/%{name}.png
install -m644 amarok/src/hi48-app-amarok.png -D %{buildroot}/%{_liconsdir}/%{name}.png

# install source1
mkdir -p %{buildroot}/%{_datadir}/apps/amarok/scripts/lyrics_cn
cd Lyrics_CN
install -m644 README COPYING Lyrics_CN.spec %{buildroot}/%{_datadir}/apps/amarok/scripts/lyrics_cn
install -m755 Lyrics_CN %{buildroot}/%{_datadir}/apps/amarok/scripts/lyrics_cn
cd -

%find_lang %{name} --with-html

#correct wrong script encoding file
perl -pi -e 's/\015$//' %{buildroot}/%{_datadir}/apps/%{name}/data/Cool-Streams.m3u
perl -pi -e 's/\015$//' %{buildroot}/%{_datadir}/apps/%{name}/scripts/playlist2html/README
perl -pi -e 's/\015$//' %{buildroot}/%{_datadir}/apps/%{name}/scripts/webcontrol/README

%clean
rm -rf %buildroot



%changelog
* Fri Jun 29 2007 Kevin Deldycke <kev@coolcavemen.com> 1.4.6-2mdv2007.1
- Enable MySQL and PostgreSQL support

* Wed Jun 20 2007 Nicolas Lécureuil <neoclust@mandriva.org> 1.4.6-1mdv2007.1
+ Revision: 41931
- Remove desktop-file-utils require as categories have been merged upstream
- New version 1.4.6
- Remove merged patches
- Bump release

  + Andreas Hasenack <andreas@mandriva.com>
    - branched cooker into 2007.1 (will have to revert some recent changes)


* Mon Mar 19 2007 Olivier Blin <oblin@mandriva.com> 1.4.5-8mdv2007.1
+ Revision: 146360
- tag lang on HTML doc

  + Michael Scherer <misc@mandriva.org>
    - disable debugging output, asked by neoclust

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - correctly set ipod model name, an "x" prefix is needed, code taken from
      gtkpod ( Patch20)
    - make the first rating star tri-state (Patch21)
    - Remove unused code (upstream BR: 141038)(Patch22)
    - fix regression  caused when mongrel had been updated , export correct
      symbols (Patch 23)
    - Fix regression: right-clicking on sound control would change volume
      (upstream BR: 141672)(Patch24)
    - Fix missing quoting for shell call. (upstream BR: 138499)(Patch25)
    - Support for colored stars *everywhere* (Patch26) see diff for a more
      important changelog
    - Fix stars refreshing ( Patch27)
    - Make stars more efficient ( Patch28)

* Fri Feb 23 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1:1.4.5-4mdv2007.1
+ Revision: 125145
- rebuild against new libgii

* Wed Feb 14 2007 Laurent Montel <lmontel@mandriva.com> 1:1.4.5-3mdv2007.1
+ Revision: 121153
- Fix magnatune

* Tue Feb 06 2007 Laurent Montel <lmontel@mandriva.com> 1:1.4.5-2mdv2007.1
+ Revision: 116584
- It was never a good idea to release a package before
  official release date
  => use last and official tarball (minor fix but official
  tarball)

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - New version 1.4.5
    - Remove merged upstream patches :  7,8,9,10,11,12

* Sat Jan 27 2007 Per Øyvind Karlsen <pkarlsen@mandriva.com> 1:1.4.4-7mdv2007.1
+ Revision: 114433
- fix release
- fix summary-not-capitalized
- fix build against new libmtp (P12)
- fix build on sparc (P11 from ubuntu)
- allow amarok to open external URLs (P10 from ubuntu)
- fix build against new libgpod (P9)

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Rebuild for new deps

  + Helio Chissini de Castro <helio@mandriva.com>
    - We don't need regenerate build system

* Mon Dec 11 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.4-6mdv2007.1
+ Revision: 94697
- Rebuidl against new libmtp

* Fri Dec 08 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.4-5mdv2007.1
+ Revision: 93602
-  Rebuild
- Add patch to fix amarok xine-lib 1.1.3  when playing Last.FM streams

* Sun Dec 03 2006 Emmanuel Andry <eandry@mandriva.org> 1:1.4.4-4mdv2007.1
+ Revision: 90224
- rebuild for new libmtp

* Thu Nov 09 2006 Laurent Montel <lmontel@mandriva.com> 1:1.4.4-3mdv2007.1
+ Revision: 79968
- Requires tunepimp-plugins (need for musicbrainz tags)

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Add a new webradio : Dogmazic ( ex: musique-libre.org)
         On this webradio, we can _ONLY_ listen free music :)

* Sat Nov 04 2006 Laurent Montel <lmontel@mandriva.com> 1:1.4.4-2mdv2007.0
+ Revision: 76543
- Remove debug

* Mon Oct 30 2006 Laurent Montel <lmontel@mandriva.com> 1:1.4.4-1mdv2007.1
+ Revision: 73692
- ldconfig
- Add lib script package
- Remove it
- 1.4.4

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - Add missing patch
    - amarok-1.4.3-6mdv2007.0
    - Better fix for encoding bug (from patchset1):
        * Fixed playlist encoding problem. This bug could also
             result in failure to restore the current playlist.
             (BR 133613)
             => amarok-1.4.3-playlist_encoding.diff
    - amarok-1.4.3-4mdv2007.0
    - Remove some radios as the links are dead
    - Fixed playlist encoding problems.
             (KDE BR 133613)
             (MDV BR  25493)
    - Fix macros for database (#25664)

* Thu Sep 07 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.3-2mdv2007.0
+ Revision: 60269
- amarok-1.4.3-2mdv2007.0
- Disable Moodbar
- Some podcasts would insert line breaks in author/title
     information and cause graphical errors. (BR 133591)
- Fix global shortcut conflicts

* Wed Sep 06 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.3-1mdv2007.0
+ Revision: 59945
- New release 1.4.3 (Lot lot of bugfixes)
- Remove patches 7,8,9,11 Merged upstream

* Sat Sep 02 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.2-6mdv2007.0
+ Revision: 59296
- Apply a forgotten patch
- amarok-1.4.2-6mdv2007.0
- PatchSet1:
  * Collection scanner would only restart a maximum of 2 times
      instead of 20.
      => amarok-1.4.2-scanner.diff
  * AudioCD playback would stutter and sometimes freeze Amarok.
      (BR 133015)
      => amarok-1.4.2-audiocd.diff
  * Fixed bug which prevented Amarok from creating the collection
      database in rare circumstances using SQLite. (BR 133072)
      => amarok-1.4.2-collection.diff

* Fri Sep 01 2006 Helio Chissini de Castro <helio@mandriva.com> 1:1.4.2-5mdv2007.0
+ Revision: 59076
- Added patch to fix libmtp compilation
- Fixed BuildRequires for mtp, sql
- For some reason cluster always add unstable as enabled, so amarok was compiling with debug everytime.
- Need match the correct tunepimp library for all archs
- rebuild to get rid of all tunepimp mess. We should now use libtunepimp and only this one

  + Nicolas Lécureuil <neoclust@mandriva.org>
    - amarok-1.4.2-4mdv2007.0
    - Add BuildRequire
    - Fix BuildRequires

* Sun Aug 27 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.2-2mdv2007.0
+ Revision: 58164
- amarok-1.4.2-2mdv2007.0
- Disable mandriva directory patch

* Sat Aug 12 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.2-1.beta1.4mdv2007.0
+ Revision: 55574
- 1.4.2-1.beta1.4mdv2007.0
- Fix rpmlint warnings

  + Helio Chissini de Castro <helio@mandriva.com>
    - Reenabled tunepimp

  + Laurent Montel <lmontel@mandriva.com>
    - Rebuild with new dbus (2006/08/02 1.4.2-beta1-3)

* Tue Aug 01 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.2-0.beta1.2mdv2007.0
+ Revision: 42865
- rebuild against new libtunepimp package

* Tue Aug 01 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.2-0.beta1.1mdv2007.0
+ Revision: 42842
- Remove musicbrainz support for the moment ( doesn't build)
- 1.4.2 Beta 1
- Remove patch 5: Merged Upstream
- Add --with-external-mad option to fix crash on 64bits ( ticket #24007)

* Mon Jul 31 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.1-5mdv2007.0
+ Revision: 42629
- Bump release
- Forget file
- Add some radios

* Fri Jul 21 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.1-4mdv2007.0
+ Revision: 41785
- Rebuild and upload to fix ticket #23852

  + Helio Chissini de Castro <helio@mandriva.com>
    - Removed gstreamer mentions. Amarok not ship any gstreamer as standard
    - Rearrange spec and reduced size
    - Added configure macro
    - enabled ipod module control using libgpod

* Wed Jul 05 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.1-2mdv2007.0
+ Revision: 38363
- ooops, forgot to commit the patch
- Increase release
- Fix conflicts with upstream lastfm (#23493) thanks Frederik Himpe

* Tue Jul 04 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.1-1mdv2007.0
+ Revision: 38287
- Fix File list
- 1.4.1 Final

* Fri Jun 23 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.4.1-0.6mdv2007.0
+ Revision: 37866
- Increase release
- Use macros (for mimetypes)
- Oooops forgot the source
- 1.4.1 Beta 1 (amaroK is now Amarok)
- Rediff Patch1
- Fix File list
- Increase release
- Fix epoch on requires
- Increase release
- Rebuild to generate category
- Add Epoch to allow upgrade from bundles as the rpm is epoched
- Add Requires ( close ticket #22896)
- Increase release
- New svn checkout
- Fix BuildRequires (thanks to Charles A Edwards)
- Increase release
- New svn checkout
- Fix File list
- increase requires on libvisual
- Use good tarball
- New svn checkout ( with many bugfixes)
- Fix File list
- increase release
- Fix File list
- 1.4.0 Final
- Obsolete gstreamer0.10 engine
- Fix MySQL build ( thanks delight for pointing this )
- Fix release
- Fix File list
- Increase release
- Remove gstreamer0.10 engine only xine is left
- remove patch 5
- 1.4.0 RC1
- Disable patch 7: merged upstream
- Fix File list
- Fix Patch 7
- Increase release
- Add Patch7: Fix Build for kde < 3.5
- New svn checkout
- add warning about the fact that amarok is on svn
- Fix file list
- increase release
- Readd gstreamer0.10 engine
- 1.4beta3-4mdk
- New svn checkout
- Fix Requires for mdv > 2006
- Rediff Patch6
- Fix File list
- increase release
- New svn snapshot
- Add Requires
- New svn checkout
- Change default shortcut ( Ticket #15163)
- New svn release ( ~ beta3 )
- Obsoletes aKode engine ( it doesn't exist anymore)
- revert previous commit
- Amarok 1.4.0 Rc2
- Fix patch4
- Add Exscalibar support
- increase release ( 0.beta2.3mdk)
- Readd previous patches ( close #21663)
- Remove xmms support
- Add versionned obsoletes

  + Andreas Hasenack <andreas@mandriva.com>
    - renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

  + Laurent Montel <lmontel@mandriva.com>
    - New release (critical fix)
      fix build against new xorg
    - Rebuild to generate category
    - Add patch from neoclust
      add conflict for smooth update
      remove arts and gstreamer subpackages (no more existant)
    - 1.4-beta2
      Reverse a part of previous changes.
      2006 support is important !
      Remove conflict with files
      Readd configure argument
      Add file at the end is better to read and not find
      file list into all spec file.
    - 1.4-beta2
      Reverse a part of previous changes.
      2006 support is important !
      Remove conflict with files
      Readd configure argument
      Add file at the end is better to read and not find
      file list into all spec file.

  + Helio Chissini de Castro <helio@mandriva.com>
    - Small spec refactoring
    - Fixed smoke dependency problem
    - Bring back amarok to svn

* Mon Feb 20 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.9mdk
- Add Requires for the scripts subpackage
- Fix amarok URL

* Wed Feb 15 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.8mdk
- New subpackage engine-gstreamer0.10 ( libgstreamer0.10 was in contrib for
	mdv =< 2006 )

* Wed Feb 15 2006 Laurent MONTEL <lmontel@mandriva.com> 1.4-0.beta1_rc1.7
- Fix buildrequires

* Wed Feb 15 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.6mdk
- Fix aKode subpackage

* Wed Feb 15 2006 Laurent MONTEL <lmontel@mandriva.com> 1.4-0.beta1_rc1.5
- Fix macro

* Mon Feb 13 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.4mdk
- Real 1.4 Beta1
- Add ifp support
- Add iPod support
- Add buildRequires : libakode2-devel, SDL-devel, libgpod-devel
- Add a postgresql subpackage
- Fix Build akode on mdv2006

* Mon Feb 13 2006 Laurent MONTEL <lmontel@mandriva.com> 1.4-0.beta1_rc1.3
- Fix spec file
- Build akode on mdk2006 (libakode doesn't exist in mdk =< 2006 )

* Sat Feb 11 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.2mdk
- create akode engine, lib and devel packages

* Sat Feb 11 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.1mdk
- amaroK 1.4 beta1
- remove --disable-rpath

* Mon Jan 16 2006 Laurent MONTEL <lmontel@mandriva.com> 1.3.8-1
- 1.3.8

* Sat Jan 14 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.8-0.Rc1.1mdk
- 1.3.8Rc1
- Remove Patch 7 : Merged Upstream

* Fri Jan 06 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-01-06 16:36:13 (1385)
- Added upstream lyrics patch on behalf of Eskild Hudtvedt ( Zero_Dogg )

* Fri Jan 06 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-01-06 16:28:24 (1384)
- Add sources and spec to svn

* Fri Jan 06 2006 Helio Chissini de Castro <helio@mandriva.com>
+ 2006-01-06 16:13:32 (1382)
- Current dir

* Fri Dec 16 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.7-4
- Rebuild because on x86_64 qt was not rebuild before new amarok rebuild: fix bug #20226

* Sat Dec 10 2005 Helio Chissini de Castro 1.3.7-3mdk
- Rebuild against new qt build

* Wed Dec 07 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.7-2
- qtdir is not define in spec file (found by Nicolas Chipaux)

* Wed Dec 07 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.7-1
- 1.3.7

* Tue Nov 08 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.6-1mdk
- New release 1.3.6
- Remove patch 20 : Merged upstream

* Mon Nov 07 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.5-5
- Add patch20: fix desktop file (bug found by Fred Crozat)

* Wed Nov 02 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.5-4mdk
- Add patch 19 : please give feedback to my patch

* Sat Oct 29 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.5-3mdk
- Fix Requires

* Wed Oct 26 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.5-2
- Remove unneccesary requires

* Wed Oct 26 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.5-1mdk
- New release 1.3.5

* Tue Oct 25 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.4-1mdk
- New release 1.3.4
- Drop patch 2 : Merged Upstream

* Sat Oct 22 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.3-4
- Add requires for gstreamer engine

* Wed Oct 19 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.3-3
- Allow to compile with debug

* Wed Oct 12 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.3-2mdk
- Fix BuildRequires ( add k3b)
- remove kdelibs-devel because already required by
	     kdebase-devel and kdemultimedia-devel

* Tue Oct 11 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.3-1mdk
- New release 1.3.3
- Drop Patch 6 : Merged Upstream

* Fri Sep 23 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.2-2mdk
- Use Amarok new icons ( betteeeeeeeeeeeeeeer :) )
- Drop patch 20 : uneeded now

* Fri Sep 23 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.2-1mdk
- New release 1.3.2 ( bug fixes )

* Sat Sep 17 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.1-3
- Add patch6: disable lastfm config

* Sat Sep 10 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.1-2
- Rebuild

* Wed Sep 07 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.1-1mdk
- Rebuild

* Wed Aug 31 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.3-2mdk
- remove obsolete lib64 fixes
- build without helix support (contribs)

* Tue Aug 16 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-1mdk
- 1.3

* Thu Aug 04 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta3.2mdk
- Make sure that it requires xine-lib

* Fri Jul 08 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta2.3mdk
- Rebuild with gcc4

* Tue Jun 28 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta2.2mdk
- Remove requires on xine-lib for the moment I can't rebuild xine-lib
on gcc-4.0 I create 3 patchs but there is again a error.
I will try to fix it after

* Tue Jun 28 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta2.1mdk
- 1.3 beta2

* Tue Jun 28 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta1.3mdk
- Split amarok as requested by Greg Meyer

* Thu Jun 09 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.3-0.beta1.2mdk
- Rediff Patch 3, 5

* Tue Jun 07 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta1.1mdk
- 1.3 beta1

* Thu May 26 2005 Sebastien Savarin <plouf@mandriva.org> 1.2.4-2mdk
- Drop Patch 0, 2, 15, 17 ( Merged Upstream )
- Minor rpmlint errors fix :
- Fix wrong script encoding line
- Fix strange-permission on amarok-1.2.4.tar.bz2

* Mon May 23 2005 Laurent MONTEL <lmontel@mandriva.com> 1.2.4-1mdk
- 1.2.4

* Tue May 03 2005 Laurent MONTEL <lmontel@mandriva.com> 1.2.3-2mdk
- Rebuild with new libflac

* Fri Apr 15 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.3-1mdk
- 1.2.3

* Tue Apr 05 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.2-4mdk
- Split amarok into amarok and amarok-script which requires PyQt
- Remove workaround to use gstreamer in x86_64 (asked by gb)

* Tue Mar 15 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.2-3mdk
- Fix buildrequires

* Tue Mar 15 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.2-2mdk
- Add patch18: fix kde bug #101496

* Tue Mar 15 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.2-1mdk
- 1.2.2

* Tue Mar 15 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.1-5mdk
- Add patch17: fix kde bug #101528

* Mon Mar 14 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.1-4mdk
- Add patch16: Fix signal/slot error

* Mon Mar 14 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.1-3mdk
- Fix shortcut, bug reported by Neoclust

* Mon Mar 14 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.1-2mdk
- Add patch15: fix kde bug #101276

* Mon Feb 28 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.1-1mdk
- 1.2.1

* Mon Feb 28 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-10mdk
- Add patch14: fix kde bug #100189
- Requires on kdemultimedia-common for "audiocd:/"

* Sun Feb 27 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-9mdk
- Add patch11: fix kde bug #100268
- Add patch12: fix kde bug #98415
- Add patch13: fix kde bug #100140

* Fri Feb 25 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-8mdk
- Add patch10: fix kde bug #100200

* Thu Feb 24 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-7mdk
- Add patch9: fix kde bug #100041

* Mon Feb 21 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-6mdk
- Fix shortcut, don't use Windows key as shortcut otherwise it opens
	K menu

* Fri Feb 18 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-5mdk
- Add patch8: fix "play media" allow to insert directory

* Wed Feb 16 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-4mdk
- Add patch7: fix cursor

* Tue Feb 15 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-3mdk
- Add patch3: reapply patch4
- Add other multimedia shortcut

* Mon Feb 14 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-2mdk
- Add patch6: fix amarok kde bug #90499

* Sun Feb 13 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-1mdk
- Amarok-1.2

* Mon Jan 31 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta4.2mdk
- Reapply patch1

* Mon Jan 31 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta4.1mdk
- beta4

* Mon Jan 10 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta3.1mdk
- beta3

* Sat Jan 01 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.2-0.beta2.3mdk
- add BuildRequires: kdebase-devel libxml2-utils
- list dangling "common" symlinks explicitly as the glob apparently doesn't
  work for them with up-to-date build env on ppc

* Mon Dec 13 2004 Laurent Culioli <laurent@mandrake.org> 1.2-0.beta2.2mdk
- rebuild with tunepimp ( autotagging support )

* Fri Dec 10 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta2.1mdk
- 1.2 beta2

* Thu Dec 02 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta1.5mdk
- Now libvisual is in main
- Add patch5: add multimedia shortcut

* Wed Dec 01 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta1.4mdk
- Add patch to compile conditional with mysql (patch from  Greg Meyer )

* Tue Nov 30 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta1.3mdk
- --enable-mysql

* Mon Nov 29 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta1.2mdk
- Reapply patch

* Mon Nov 29 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2-0.beta1.1mdk
- 1.2 beta1

* Fri Nov 26 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1.1-3mdk
- Add patch4: fix default config

* Tue Nov 09 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1.1-2mdk
- Reapply gb fixe

* Tue Oct 12 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1.1-1mdk
- 1.1.1

* Sat Oct 02 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1-1mdk
- 1.1

* Sat Oct 02 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.2-5mdk
- Fix default config

* Thu Sep 30 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.2-4mdk
- Fix compile

* Thu Sep 09 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.2-3mdk
- Fix initial preference

* Tue Sep 07 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.2-2mdk
- Add initialpreference

* Sat Aug 07 2004 Laurent Culioli <laurent@mandrake.org> 1.0.2-1mdk
- 1.0.2
- regenerate patch0
- use libxine

* Tue Jun 29 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.1-1mdk
- 1.0.1

* Sat Jun 19 2004 Laurent Culioli <laurent@mandrake.org> 1.0-2mdk
- Patch0: fix locales
- update description
- make rpmlint happy with menu

* Fri Jun 18 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-1mdk
- 1.0

* Sat Jun 05 2004 <lmontel@n2.mandrakesoft.com> 1.0-0.beta4.2mdk
- Rebuild

* Thu Jun 03 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-0.beta4.1mdk
- beta4

* Fri May 21 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.0-0.beta3.3mdk
- fix buildrequires
- don't do rm -rf $RPM_BUILD_ROOT in %%prep
[           1      -eq 1 ] || exit 0
[           1      -eq 1 ] || exit 0
[           1      -eq 1 ] || exit 0

[           1      -eq 1 ] || exit 0
[           1      -eq 1 ] || exit 0
[           1      -eq 1 ] || exit 0

* Tue May 18 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-0.beta3.2mdk
- Reapply patch1

* Thu May 13 2004 Bellegarde Cedric <cedric.bellegarde@wanadoo.fr> 1.0-0.beta3.1mdk
- Update to last version

* Sat May 08 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-0.beta2.3mdk
- Fix crash when xmms_plugins_path not found (bug found by Nicolas Chipaux)

* Sun Apr 25 2004 Bellegarde Cedric <cedric.bellegarde@wanadoo.fr> 1.0-0.beta2.2mdk
- Fix libxmms-devel missing build require
- Add libgstreamer support

* Sun Apr 25 2004 Bellegarde Cedric <cedric.bellegarde@wanadoo.fr> 1.0.beta2-1mdk
- update to last version

* Wed Apr 21 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-0.beta1.1mdk
- 1.0-beta1
- Fix spec file

* Thu Apr 08 2004 Laurent Culioli <laurent@mandrake.org> 0.9-2mdk
- reupload

