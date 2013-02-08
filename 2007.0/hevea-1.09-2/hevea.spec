%define name hevea
%define version 1.09
%define release %mkrel 2

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Summary: 	A fast LaTeX to HTML translator
License: 	QPL
Group: 		Publishing
URL: 		http://para.inria.fr/~maranget/hevea
Source0: 	ftp://ftp.inria.fr/INRIA/moscova/hevea/%{name}-%{version}.tar.bz2
Source1: 	ftp://ftp.inria.fr/INRIA/moscova/hevea/%{name}-%{version}-manual.tar.bz2
BuildRequires:	ocaml >= 3.07
Requires:  tetex
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
HEVEA is a LaTeX to HTML translator.  The input language is a fairly
complete subset of LaTeX2e (old LaTeX style is also accepted) and
the output language is HTML that is (hopefully) correct with respect
to version 4.0 (transitional)
This package is a binary installation of the hevea system.
This software includes the Objective Caml run-time system, which is
copyright 1995--1999 INRIA.

%prep
%setup -q
%setup -q -a 1

%build
%make LIBDIR=%{_datadir}/%{name}

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -d -m 755 %{buildroot}%{_datadir}/texmf/tex/latex/%{name}
make \
	DESTDIR=%{buildroot} \
	PREFIX=%{_prefix} \
	LIBDIR=%{_datadir}/%{name} \
	LATEXLIBDIR=%{_datadir}/texmf/tex/latex \
	install

%clean
rm -rf %{buildroot}

%post -p %{_bindir}/mktexlsr

%postun -p %{_bindir}/mktexlsr


%files
%defattr(-,root,root)
%doc %{name}-%{version}-manual/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/texmf/tex/latex/%{name}.sty


%changelog
* Sun Dec 03 2006 Kevin Deldycke <kev@coolcavemen.com> 1.09-2mdv2007.0
- Backport from cooker to 2007.0

* Wed Nov 22 2006 Jérôme Soyer <saispo@mandriva.org> 1.09-2mdv2007.0
+ Revision: 86319
- Add Requires tetex
- Add BuildRequires Tetex

* Fri Nov 10 2006 Guillaume Rousse <guillomovitch@mandriva.org> 1.09-1mdv2007.0
+ Revision: 80682
- new version
- Import hevea

* Mon Sep 26 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.08-3mdk
- fix hevea.hva search

* Mon Jun 06 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.08-2mdk
- make clean first, upstream tarball sux

* Thu Jun 02 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.08-1mdk
- new release 1.08
- drop patch (merged upstream)

* Fri May 14 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.07-3mdk
- _really_ fix hevea.sty location (/me sux)

* Fri May 14 2004 Guillaume Rousse <guillomovitch@mandrake.org> 1.07-2mdk
- fix hevea.sty location
- rpmbuildupdate aware

* Thu Nov 06 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 1.07-1mdk
- new version
- arch-independant file in %{_datadir}/%{name}
- rm -rf %{buildroot} in %%install

* Fri Jan 17 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.06-3mdk
- rebuild

* Tue Dec 03 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.06-2mdk
- spec cleanup
- fixed forgotten binary

* Fri May 17 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.06-1mdk
- 1.06
- changed license tag

* Tue Jul 31 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.05-5mdk
- rebuild

* Thu Jan 11 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.05-4mdk
- rebuild

* Wed Oct 18 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.05-3mdk
- used srpm from Guillaume Rousse <g.rousse@linux-mandrake.com> :
	Tue Oct 17 2000 Guillaume Rousse <g.rousse@linux-mandrake.com>
	- changed license tag

* Tue Oct 17 2000 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.05-2mdk
- correct perm problem
- correct build problem

* Wed Aug 02 2000 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.05-1mdk
- first mandrake release
