#
# This file is stored on the svn, dont forget to
# commit it if you do changes on it.
#

%define __libtoolize /bin/true

%define libname_orig lib%{name}
%define libname %mklibname %{name} 0

%define name    amarok
%define version 1.4.4
%define release %mkrel 1

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
Url:            http://amarok.sourceforge.net/
Group:          Sound
Source0:        %{name}-%{version}.tar.bz2
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
%if %mdkversion > 200600
BuildRequires:  exscalibar-devel
BuildRequires:  mesaglut-devel
BuildRequires:  libgpod-devel
%else
BuildRequires:  MesaGLU-devel
%endif
BuildRequires:  ruby-devel

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires: amarok-engine
Requires: amarok-scripts
Requires: %{libname} = %epoch:%{version}

%if %mdkversion > 200600
Requires:       exscalibar
Requires:       libvisual-plugins >= 0.4.0
%endif
# Permit to make smouth updates
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
%if %mdkversion > 200600
%{update_desktop_database}
%endif

%postun
%clean_menus
%if %mdkversion > 200600
%{clean_desktop_database}
%endif

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
%{_menudir}/amarok
%doc %_docdir/HTML/*/amarok/*
%exclude %_datadir/apps/amarok/scripts/
%exclude %_libdir/kde3/libamarok_xine-engine.*
%exclude %_datadir/services/amarok_xine-engine.desktop
%exclude %_datadir/config.kcfg/xinecfg.kcfg

#--------------------------------------------------------------------------

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


%package -n %{libname}-scripts
Summary:        library scripts for amarok
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


%post -n %{libname}-scripts -p /sbin/ldconfig
%postun -n %{libname}-scripts -p /sbin/ldconfig


%package -n %{libname}-devel-scripts
Summary:        library scripts for amarok
Group:          Graphical desktop/KDE
Requires:       %{libname}-scripts = %epoch:%{version}
URL:            http://amarok.kde.org/
Requires:       ruby

%description -n %{libname}-devel-scripts
This package includes devel for scripts for amarok.

%files -n %{libname}-devel-scripts
%defattr(-,root,root)
%_libdir/ruby_lib/*.so

#--------------------------------------------------------------------------

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

#--------------------------------------------------------------------------

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

#--------------------------------------------------------------------------

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

#--------------------------------------------------------------------------


%prep
%setup -q -n %name-%version
%patch0 -p1 -b .fix_amarok_initial_preference
%patch1 -p0 -b .fix_amarok_default_config_file
#reapply
#%patch2 -p1 -b .fix_default_config
%patch3 -p1 -b .fix_add_multimedia_shortcut
#%patch4 -p0 -b .use_mandriva_music_directory
%patch6 -p0 -b .add_some_radios

%build
export QTDIR=%_prefix/lib/qt3

# Libmtp detection was broken on 1.4.2 launch, so we need
# rebuild the buildsystem
make -f Makefile.cvs

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

mkdir -p %{buildroot}/%{_menudir}

kdedesktop2mdkmenu.pl %{name} "Multimedia/Sound" %buildroot%{_datadir}/applications/kde/%{name}.desktop %buildroot%{_menudir}/%{name} x11

%find_lang %{name}

#correct wrong script encoding file
perl -pi -e 's/\015$//' %{buildroot}/%{_datadir}/apps/%{name}/data/Cool-Streams.m3u
perl -pi -e 's/\015$//' %{buildroot}/%{_datadir}/apps/%{name}/scripts/playlist2html/README
perl -pi -e 's/\015$//' %{buildroot}/%{_datadir}/apps/%{name}/scripts/webcontrol/README

%clean
rm -rf %buildroot




%changelog
* Mon Oct 30 2006 Kevin Deldycke <kev@coolcavemen.com> 1.4.4-1mdv2007.0
- Backport from cooker to Mandriva 2007.0

* Mon Oct 30 2006 Laurent Montel <lmontel@mandriva.com> 1.4.4-1mdv2007.0
+ Revision: 73692
- ldconfig
- Add lib script package
- Remove it
- 1.4.4
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


* Mon Feb 20 2006 Nicolas L�ureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.9mdk
- Add Requires for the scripts subpackage
- Fix amarok URL

* Wed Feb 15 2006 Nicolas L�ureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.8mdk
- New subpackage engine-gstreamer0.10 ( libgstreamer0.10 was in contrib for
	mdv =< 2006 )

* Wed Feb 15 2006 Laurent MONTEL <lmontel@mandriva.com> 1.4-0.beta1_rc1.7
- Fix buildrequires

* Wed Feb 15 2006 Nicolas L�ureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.6mdk
- Fix aKode subpackage

* Wed Feb 15 2006 Laurent MONTEL <lmontel@mandriva.com> 1.4-0.beta1_rc1.5
- Fix macro

* Mon Feb 13 2006 Nicolas L�ureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.4mdk
- Real 1.4 Beta1
- Add ifp support
- Add iPod support
- Add buildRequires : libakode2-devel, SDL-devel, libgpod-devel
- Add a postgresql subpackage
- Fix Build akode on mdv2006

* Mon Feb 13 2006 Laurent MONTEL <lmontel@mandriva.com> 1.4-0.beta1_rc1.3
- Fix spec file
- Build akode on mdk2006 (libakode doesn't exist in mdk =< 2006 )

* Sat Feb 11 2006 Nicolas L�ureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.2mdk
- create akode engine, lib and devel packages

* Sat Feb 11 2006 Nicolas L�ureuil <neoclust@mandriva.org> 1.4-0.beta1_rc1.1mdk
- amaroK 1.4 beta1
- remove --disable-rpath

* Mon Jan 16 2006 Laurent MONTEL <lmontel@mandriva.com> 1.3.8-1
- 1.3.8

* Sat Jan 14 2006 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.8-0.Rc1.1mdk
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

* Tue Nov 08 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.6-1mdk
- New release 1.3.6
- Remove patch 20 : Merged upstream

* Mon Nov 07 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.5-5
- Add patch20: fix desktop file (bug found by Fred Crozat)

* Wed Nov 02 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.5-4mdk
- Add patch 19 : please give feedback to my patch

* Fri Oct 28 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.5-3mdk
- Fix Requires

* Tue Oct 25 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.5-2
- Remove unneccesary requires

* Tue Oct 25 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.5-1mdk
- New release 1.3.5

* Mon Oct 24 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.4-1mdk
- New release 1.3.4
- Drop patch 2 : Merged Upstream

* Fri Oct 21 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.3-4
- Add requires for gstreamer engine

* Tue Oct 18 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.3-3
- Allow to compile with debug

* Tue Oct 11 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.3-2mdk
- Fix BuildRequires ( add k3b)
- remove kdelibs-devel because already required by
	     kdebase-devel and kdemultimedia-devel

* Mon Oct 10 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.3-1mdk
- New release 1.3.3
- Drop Patch 6 : Merged Upstream

* Thu Sep 22 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.2-2mdk
- Use Amarok new icons ( betteeeeeeeeeeeeeeer :) )
- Drop patch 20 : uneeded now

* Thu Sep 22 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3.2-1mdk
- New release 1.3.2 ( bug fixes )

* Fri Sep 16 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.1-3
- Add patch6: disable lastfm config

* Fri Sep 09 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.1-2
- Rebuild

* Tue Sep 06 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3.1-1mdk
- Rebuild

* Tue Aug 30 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.3-2mdk
- remove obsolete lib64 fixes
- build without helix support (contribs)

* Mon Aug 15 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-1mdk
- 1.3

* Wed Aug 03 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta3.2mdk
- Make sure that it requires xine-lib

* Thu Jul 07 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta2.3mdk
- Rebuild with gcc4

* Mon Jun 27 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta2.2mdk
- Remove requires on xine-lib for the moment I can't rebuild xine-lib
on gcc-4.0 I create 3 patchs but there is again a error.
I will try to fix it after

* Mon Jun 27 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta2.1mdk
- 1.3 beta2

* Mon Jun 27 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta1.3mdk
- Split amarok as requested by Greg Meyer

* Wed Jun 08 2005 Nicolas L�ureuil <neoclust@mandriva.org> 1.3-0.beta1.2mdk
- Rediff Patch 3, 5

* Mon Jun 06 2005 Laurent MONTEL <lmontel@mandriva.com> 1.3-0.beta1.1mdk
- 1.3 beta1

* Wed May 25 2005 Sebastien Savarin <plouf@mandriva.org> 1.2.4-2mdk
- Drop Patch 0, 2, 15, 17 ( Merged Upstream )
- Minor rpmlint errors fix :
- Fix wrong script encoding line
- Fix strange-permission on amarok-1.2.4.tar.bz2

* Sun May 22 2005 Laurent MONTEL <lmontel@mandriva.com> 1.2.4-1mdk
- 1.2.4

* Mon May 02 2005 Laurent MONTEL <lmontel@mandriva.com> 1.2.3-2mdk
- Rebuild with new libflac

* Thu Apr 14 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.3-1mdk
- 1.2.3

* Mon Apr 04 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 1.2.2-4mdk
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

* Mon Oct 11 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1.1-1mdk
- 1.1.1

* Fri Oct 01 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.1-1mdk
- 1.1

* Fri Oct 01 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.2-5mdk
- Fix default config

* Wed Sep 29 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.2-4mdk
- Fix compile

* Wed Sep 08 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.2-3mdk
- Fix initial preference

* Mon Sep 06 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.2-2mdk
- Add initialpreference

* Fri Aug 06 2004 Laurent Culioli <laurent@mandrake.org> 1.0.2-1mdk
- 1.0.2
- regenerate patch0
- use libxine

* Mon Jun 28 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0.1-1mdk
- 1.0.1

* Fri Jun 18 2004 Laurent Culioli <laurent@mandrake.org> 1.0-2mdk
- Patch0: fix locales
- update description
- make rpmlint happy with menu

* Thu Jun 17 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-1mdk
- 1.0

* Fri Jun 04 2004 <lmontel@n2.mandrakesoft.com> 1.0-0.beta4.2mdk
- Rebuild

* Wed Jun 02 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-0.beta4.1mdk
- beta4

* Thu May 20 2004 Per �vind Karlsen <peroyvind@linux-mandrake.com> 1.0-0.beta3.3mdk
- fix buildrequires
- don't do rm -rf $RPM_BUILD_ROOT in %prep
[           1      -eq 1 ] || exit 0
[           1      -eq 1 ] || exit 0
[           1      -eq 1 ] || exit 0

* Mon May 17 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-0.beta3.2mdk
- Reapply patch1

* Wed May 12 2004 Bellegarde Cedric <cedric.bellegarde@wanadoo.fr> 1.0-0.beta3.1mdk
- Update to last version

* Fri May 07 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-0.beta2.3mdk
- Fix crash when xmms_plugins_path not found (bug found by Nicolas Chipaux)

* Sat Apr 24 2004 Bellegarde Cedric <cedric.bellegarde@wanadoo.fr> 1.0-0.beta2.2mdk
- Fix libxmms-devel missing build require
- Add libgstreamer support

* Sat Apr 24 2004 Bellegarde Cedric <cedric.bellegarde@wanadoo.fr> 1.0.beta2-1mdk
- update to last version

* Tue Apr 20 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 1.0-0.beta1.1mdk
- 1.0-beta1
- Fix spec file

* Wed Apr 07 2004 Laurent Culioli <laurent@mandrake.org> 0.9-2mdk
- reupload

* Sat Mar 06 2004 Bellegarde Cedric <cedric.bellegarde@wanadoo.fr> 0.9-1mdk
- Make a spec file

