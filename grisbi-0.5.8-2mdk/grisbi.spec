%define	name	grisbi
%define	version	0.5.8
%define	release	%mkrel 2


Summary:	Personnal finances manager
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Url:		http://www.grisbi.org/
Source0:	http://switch.dl.sourceforge.net/sourceforge/grisbi/%{name}-%{version}.tar.bz2
Source1:	grisbi-manuel-0.5.1.tar.bz2
Source11:	%{name}-16x16.png
Source12:	%{name}-32x32.png
Source13:	%{name}-48x48.png
# (fc) 0.5.8-2mdk fix browser name
Patch0:		grisbi-0.5.8-browser.patch.bz2
# (fc) 0.5.8-2mdk fix doc build
Patch1:		grisbi-0.5.8-fixbuild.patch.bz2

Group:		Office
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libgnomeui2-devel libgdk_pixbuf2.0-devel libgnomeprint-devel
BuildRequires:	ImageMagick gtk2-devel libofx-devel hevea
Requires: tetex-latex
Requires: tetex-dvips

%description
Grisbi helps you to manage your personnal finances with Linux.

%prep
%setup -q -a 1
%patch0 -p1 -b .browser
%patch1 -p1 -b .fixbuild

%build
%configure2_5x
%make

make -C grisbi-manuel-0.5.1/src html_img

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

cp -f -r grisbi-manuel-0.5.1/src/fr/* $RPM_BUILD_ROOT%{_datadir}/doc/grisbi/help/fr/

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

install -d $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}):\
command="%{name}"\
needs="x11" \
icon="%{name}.png"\
section="More Applications/Finances"\
title="Grisbi"\
icon="office_section.png"\
longtitle="Personnal Finances Manager"
EOF


%find_lang %{name}

%post
%{update_menus}


%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS NEWS README
%{_bindir}/*
%{_datadir}/doc/grisbi/help/C/
%{_datadir}/pixmaps/*
%{_mandir}/man1/*
#%_iconsdir/*.png
%{_datadir}/mime-info/*
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%lang(fr) %{_datadir}/doc/grisbi/help/fr
%lang(de) %{_datadir}/doc/grisbi/help/de

%changelog
* Thu Apr 06 2006 Frederic Crozat <fcrozat@mandriva.com> 0.5.8-2mdk
- Patch0: fix web browser name
- Patch1: fix doc build
- package french manual
- Add requires on latex, needed for printing
- fix buildrequires

* Thu Jan 19 2006 Lenny Cartier <lenny@mandriva.com> 0.5.8-1mdk
- 0.5.8

* Thu Nov 24 2005 Lenny Cartier <lenny@mandriva.com> 0.5.7-3mdk
- rebuild

* Mon Aug 08 2005 Per Ã˜yvind Karlsen <pkarlsen@mandriva.com> 0.5.7-2mdk
- %%mkrel
- get rid of bizarre stuff
- don't bzip2 icons
- cleanups!

* Thu Jun 09 2005 Lenny Cartier <lenny@mandriva.com> 0.5.7-1mdk
- 0.5.7

* Thu Jan 13 2005 Jerome Soyer <saispo@mandrake.org> 0.5.5-1mdk
- 0.5.5

* Mon Dec 20 2004 Götz Waschk <waschk@linux-mandrake.com> 0.5.3-2mdk
- rebuild for new ofx

* Thu Dec 02 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.5.3-1mdk
- 0.5.3

* Thu Oct 21 2004 Jerome Soyer <saispo@mandrake.org> 0.5.2-1mdk
- 0.5.2
- Update BuildRequires

* Sun Aug 29 2004 Jerome Soyer <saispo@mandrake.org> 0.5.1-3mdk
- fix buildrequires

* Sat Aug 21 2004 Jerome Soyer <saispo@mandrake.org> 0.5.1-2mdk
- fix menu entry

* Wed Aug 04 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.5.1-1mdk
- 0.5.1

* Mon Jul 19 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.5.0-1mdk
- from neoclust <n1c0l4s.l3@wanadoo.fr> : 
	- 0.5.0

* Fri Apr 23 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.4.5-1mdk
- 0.4.5
- merge with original grisbi spec

* Sun Jan 4 2004 Charles A Edwards <eslrahc@mandrake.org 0.4.3-1mdk
- 0.4.3

* Fri Dec 26 2003 Charles A Edwards <eslrahc@mandrake.org 0.4.2-1mdk
- 0.4.2
- drop icon sources and use ImageMagick
- buildrequires
- makeinstall_std

* Thu Jul 24 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.4.1-1mdk
- 0.4.1

* Wed Apr 30 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.4.0-2mdk
- buildrequires

* Mon Feb 17 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.4.0-1mdk
- 0.4.0

* Thu Jan 30 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.3.3-5mdk
- rebuild

* Mon Nov 04 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.3.3-4mdk
- rebuild

* Mon Oct 07 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.3.3-3mdk
- from Gerald Niel <gerald.niel@gegeweb.net> :
	- References to applet removed (for mdk 9.0)

* Sat Oct 5 2002 Gerald Niel <gerald.niel@gegeweb.net> 0.3.3-2gsb
  - Build against 0.3.3 CVS Sat Oct 5 2002
  - Requires dependencies removed
  - BuildRequires dependencies removed
  - New icons added

* Sat Sep 21 2002 Gerald Niel <gerald.niel@gegeweb.net> 0.3.3-1gsb
  - Build against 0.3.3 CVS Sat Sep 21 2002
  - Distribution Added

* Thu Sep 19 2002 Gerald Niel <gerald.niel@gegeweb.net> 0.3.2-5mdk
  - Build against 0.3.2-corr CVS Sun Sep 19 2002
  - Vendor and Packager Added

* Sun Sep 15 2002 Gerald Niel <gerald.niel@gegeweb.net> 0.3.2-4mdk
  - Build against 0.3.2-corr CVS Sun Sep 15 2002
  - Removed build macro
  - Requires dependencies Updated

* Sun Sep 08 2002 Gerald Niel <gerald.niel@gegeweb.net> 0.3.2-3mdk
  - Added build macro
  - Use automake and autoconf
  - Updated Group to Applications/Finances
  - Updated Requires dependencies

* Sat Sep 07 2002 Gerald Niel <gerald.niel@gegeweb.net> 0.3.2-2mdk
  - Added BuildRequires dependencies (Blaise Tramier)
  - Added Requires dependencies
  
* Wed Aug 21 2002 Gerald Niel <gerald.niel@gegeweb.net> 0.3.2-1mdk
  - Build against 0.3.2
  - Patch Makefile removed 
  
* Tue Jan 08 2002 Blaise Tramier <meles@linux-mandrake.com> 0.3.1-2mdk
  - Added menus entries.
  - Added icons.
  - Spec code cleaning (tryied at last).

* Sun Jan 06 2002 Blaise Tramier <meles@linux-mandrake.com> 0.3.1-1mdk
  - First Mandrake rpm.
  - Makefile patch.
