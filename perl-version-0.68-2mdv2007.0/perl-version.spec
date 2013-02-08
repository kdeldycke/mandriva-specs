%define module	version
%define name	perl-%{module}
%define	modprefix version

%define	realversion 0.68
%define version	0.68
%define release	%mkrel 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Perl extension for Version Objects
License:	GPL or Artistic
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/J/JP/JPEACOCK/%{module}-%{realversion}.tar.bz2
BuildRequires:	perl-devel
BuildRequires:	perl(ExtUtils::CBuilder)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Test::More)
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Overloaded version objects for all versions of Perl. This module implements
all of the features of version objects which will be part of Perl 5.10.0
except automatic version object creation.

%prep
%setup -q -n %{module}-%{realversion}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%check
./Build test

%clean
rm -rf %{buildroot}

%install
rm -rf %{buildroot}
./Build install destdir=%{buildroot}

%files
%defattr(-,root,root)
%doc Changes README
%{perl_vendorarch}/%{modprefix}*
%{perl_vendorarch}/auto/%{modprefix}
%{_mandir}/*/*



%changelog
* Sat Apr 07 2007 Kevin Deldycke <kev@coolcavemen.com> 0.68-2mdv2007.0
- Backported from cooker to Mandriva 2007.0

* Sun Dec 24 2006 Olivier Thauvin <nanardon@mandriva.org> 0.68-1mdv2007.0
+ Revision: 101959
- 0.68

* Mon Aug 28 2006 Scott Karns <scottk@mandriva.org> 0.67.01-1mdv2007.0
+ Revision: 58287
- Version 0.6701

* Thu Aug 17 2006 Scott Karns <scottk@mandriva.org> 0.67-3mdv2007.0
+ Revision: 56546
- Removed unnecessary BuildRequires gcc
- Added BuildRequires perl(ExtUtils::CBuilder)

* Thu Aug 17 2006 Scott Karns <scottk@mandriva.org> 0.67-2mdv2007.0
+ Revision: 56542
- Added BuildRequires gcc

* Sun Aug 13 2006 Scott Karns <scottk@mandriva.org> 0.67-1mdv2007.0
+ Revision: 55805
- Version 0.67
- Patched Build.PL for broken Module::Build-0.2805 (per CPAN
  maintainer of version)
- import perl-version-0.64-1mdv2007.0


* Fri Jun 16 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.64-1mdv2007.0
- new version
- revert to author's namespace for source URL, standard one doesn't seem to exist

* Thu Jun 08 2006 Guillaume Rousse <guillomovitch@mandriva.org> 0.63-1mdv2007.0
- New release 0.63
- no use for perl-devel, this one uses Module::Build

* Thu Apr 27 2006 Nicolas L�cureuil <neoclust@mandriva.org> 0.59-2mdk
- Fix SPEC Using perl Policies
	- BuildRequires

* Mon Apr 03 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.59-1mdk
- 0.59

* Mon Mar 06 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.57-1mdk
- 0.57

* Mon Jan 16 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.53-1mdk
- 0.53

* Fri Dec 16 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.50-1mdk
- 0.50

* Wed Oct 12 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.49-1mdk
- 0.49

* Fri Sep 30 2005 Nicolas L�cureuil <neoclust@mandriva.org> 0.48-2mdk
- Buildrequires fix

* Fri Sep 23 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.48-1mdk
- 0.48

* Wed Aug 24 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.47-1mdk
- 0.47

* Mon Aug 22 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.46-1mdk
- 0.46

* Mon Jul 25 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.44-1mdk
- 0.44
- Convert spec to build using Build.PL

* Sat May 07 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.42-2mdk
- drop patch, the pseudo-shellbang is actually used by perl

* Wed Apr 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.42-1mdk
- first mandriva release

