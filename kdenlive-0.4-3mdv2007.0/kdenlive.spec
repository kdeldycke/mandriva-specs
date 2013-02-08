
Name: 		kdenlive
Version: 	0.4
Release: 	%mkrel 3
License: 	GPL
Summary: 	A non-linear video editing application for KDE
Group:		Graphical desktop/KDE
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source: 	%name-%version.tar.bz2
BuildRequires:	kdelibs-devel
BuildRequires:	mlt-devel
BuildRequires:	mlt++-devel
BuildRequires:	libavc-devel
BuildRequires:	libiec61883-devel
Requires:	mlt >= 0.2.2
Requires: 	piave >= 0.2.2
Requires:	kdebase-progs >= 3.0.0
URL:		http://kdenlive.sourceforge.net/

%description
Kdenlive is a non-linear video editor for KDE. It relies on a separate
renderer, piave, to handle it's rendering. Kdenlive supports multitrack
editing.

%prep
%setup -q

%build
make -f admin/Makefile.common cvs

%ifarch %ix86
export CXXFLAGS="%optflags -fno-omit-frame-pointer"
%endif
%configure2_5x \
		--enable-shared \
		--disable-static \
		--disable-embedded \
		--disable-palmtop \
		--disable-rpath \
		--with-gnu-ld \
		--with-pic \
		--with-xinerama

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

install -d %buildroot/%_menudir/
kdedesktop2mdkmenu.pl kdenlive Multimedia/Video %buildroot/%_datadir/applications/kde/%{name}.desktop %buildroot/%_menudir/%{name}

perl -pi -e 's|^Icon=.*|Icon=%{name}|' %buildroot/%_datadir/applications/kde/kdenlive.desktop

%find_lang %name

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
%update_menus
%if %mdkversion > 200600
%{update_desktop_database}
%update_icon_cache hicolor
%endif

%postun
/sbin/ldconfig
%clean_menus
%if %mdkversion > 200600
%{clean_desktop_database}
%clean_icon_cache hicolor
%endif

%files -f %name.lang
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README TODO
%doc %{_docdir}/HTML
%_bindir/*
%_datadir/apps/%{name}
%_datadir/config.kcfg
%_datadir/applications/kde/%{name}.desktop
%_menudir/%{name}
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/actions/%{name}_*
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/piave.png
%_datadir/mimelnk/application/vnd.kde.kdenlive.desktop
%_datadir/mimelnk/application/vnd.kde.kdenlive.scenelist.desktop


%changelog
* Sat Apr 07 2007 Kevin Deldycke <kev@coolcavemen.com> 0.4-3mdv2007.0
- Backported from cooker to Mandriva 2007.0

* Wed Feb 07 2007 Laurent Montel <lmontel@mandriva.com> 0.4-2mdv2007.0
+ Revision: 117212
- Fix requires

* Wed Dec 13 2006 Anssi Hannula <anssi@mandriva.org> 0.4-1mdv2007.1
+ Revision: 96473
- from Jos?\195?\169 Jorge <jjorge@free.fr>
  o 0.4
  o drop no longer needed patch 0
  o action icons added to spec

* Sat Oct 28 2006 Anssi Hannula <anssi@mandriva.org> 0.3-1mdv2007.1
+ Revision: 73615
- 0.3
- clean spec
- drop no longer needed patches 1, 2, 3, 4
- patch0: fix autoconf detection
- add new buildrequires and requires
- use find_lang
- add clean_desktop_database
- Import kdenlive




* Tue Aug 29 2006 Nicolas L�cureuil <neoclust@mandriva.org> 0.2.4-4mdv2007.0
- Add Patch 4: Fix automake > 1.7 detection

* Fri Jun 30 2006 Nicolas L�cureuil <neoclust@mandriva.org> 0.2.43mdv2007.0
- Use macros for icons

* Sun Jan 22 2006 Nicolas L�cureuil <neoclust@mandriva.org> 0.2.4-2mdk
-  Add Patch 3 ( from qa.mandriva.com at vpanel.cjb.net) :
		- Fix ticket 15538
- Fix URL
- Use mkrel

* Mon Feb 21 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.4-1mdk
- 0.2.4

* Thu Dec 09 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.3-10mdk
- Fix spec file

* Mon Jun 14 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.3-9mdk
- Rebuild

* Sat May 22 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 0.2.3-8mdk
- grf, forgot the automake buildrequires

* Fri May 21 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 0.2.3-7mdk
- fix buildrequires
- do rm -rf $RPM_BUILD_ROOT in %%install, not %%prep
- fix path to qt (lib64 issue)
- added url
- fixed typo

* Wed Apr 07 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.3-6mdk
- Fix requires

* Wed Mar 31 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.3-5mdk
- use %%configure
- use mdkversion

* Mon Feb 23 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.3-4mdk
- Fix piave path

* Sun Feb 08 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.3-3mdk
- Rebuild

* Tue Jan 13 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.3-2mdk
- Add menu entry

* Mon Dec 15 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 0.2.3-1mdk
- first package
