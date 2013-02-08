%define realname	SVK
%define name		svk
%define version		2.0.0
%define release		%mkrel 5

Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
Summary:	Decentralized version control system based on Subversion
Source0:        http://search.cpan.org/CPAN/authors/id/C/CL/CLKAO/%{realname}-v%{version}.tar.bz2
Source1:	%{name}.bash-completion
Url:		http://svk.elixus.org/
Requires:	perl-SVK = %{version}
BuildRequires:	perl-Algorithm-Annotate
BuildRequires:	perl-Algorithm-Diff
BuildRequires:	perl-Class-Autouse
BuildRequires:	perl-Compress-Zlib
BuildRequires:	perl-File-BaseDir
BuildRequires:	perl-Data-Hierarchy
BuildRequires:	perl-File-MimeInfo
BuildRequires:	perl-File-Type
BuildRequires:	perl-FreezeThaw
BuildRequires:	perl-IO-Digest
BuildRequires:	perl-Locale-Maketext-Lexicon
BuildRequires:	perl-Locale-Maketext-Simple
BuildRequires:	perl-PerlIO-eol
BuildRequires:	perl-PerlIO-via-symlink
BuildRequires:	perl-Pod-Simple
BuildRequires:	perl-Regexp-Shellish
BuildRequires:	perl-Sort-Versions
BuildRequires:	perl-SVN-Mirror >= 0.66
BuildRequires:	perl-Text-Diff
BuildRequires:	perl-TimeDate
BuildRequires:	perl-YAML
BuildRequires:	perl-Clone
BuildRequires:	shared-mime-info
BuildRequires:  perl-devel
BuildRequires:  perl(YAML::Syck)
BuildRequires:  perl(App::CLI)
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(Class::Data::Inheritable)
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(UNIVERSAL::require)
BuildRequires:  perl-version
# For apxs2
BuildRequires:	apache2-devel
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
svk is a decentralized version control system written in Perl.
It uses the subversion filesystem but provides some other powerful features.

It allows you to work in a disconnected fashion with the possibility to merge
back your changes to the main repository.

%package -n perl-SVK
Summary:	Perl modules used by SVK
Group:		Development/Perl
# for some strange reason, not detected by our scripts
Requires:	perl-SVN-Mirror >= 0.66
Requires:	perl-File-Type
Requires:	perl-Class-Autouse
Requires:	perl-Term-ReadKey
Requires:	perl-Data-Hierarchy
Requires:	perl-Regexp-Shellish
Requires:	perl-Pod-Simple
Requires:	perl-IO-Digest
Requires:	perl-Clone
Requires:	perl-version
# not really needed, but I prefer to have more features enabled by defaut
Requires:	perl-File-MimeInfo
Requires:	perl-Locale-Maketext-Simple
# rpm doesn't find and generate this.
Provides:	perl(SVK::Version)

%description -n perl-SVK
This package provides the base modules needed by svk.

%prep
%setup -q -n %{realname}-v%{version}

%build
%{__perl} Makefile.PL --skip INSTALLDIRS=vendor
%make

%check
# should be corrected in new version, thanks for rgs for spotting this
export LC_ALL=C
APXS=/usr/sbin/apxs prove -b t/*.t

# don't leave non-writable directories
chmod -R +w t

%install
rm -rf %{buildroot}
%makeinstall_std

# bash completion
install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%clean
rm -rf %{buildroot}

%files -n perl-SVK
%defattr(-,root,root)
%doc README CHANGES COMMITTERS CHANGES-1.0
%{perl_vendorlib}/SVK
%{perl_vendorlib}/SVK.pm
%{_mandir}/man3/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Sat Apr 07 2007 Kevin Deldycke <kev@coolcavemen.com> 2.0.0-5mdv2007.0
- Backported from cooker to Mandriva 2007.0

* Sun Jan 14 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-4mdv2007.0
+ Revision: 108798
- real working bash completion update

* Fri Jan 12 2007 Guillaume Rousse <guillomovitch@mandriva.org> 2.0.0-3mdv2007.1
+ Revision: 108051
- fix bash completion installation
- update bash-completion
- decompress bash-completion file

* Wed Jan 03 2007 Michael Scherer <misc@mandriva.org> 2.0.0-2mdv2007.1
+ Revision: 103900
- add more doc
- add a Requires on perl-version, spotted by guillomovitch

* Wed Jan 03 2007 Michael Scherer <misc@mandriva.org> 2.0.0-1mdv2007.1
+ Revision: 103721
- fix BuildRequires
- version 2.0.0

* Fri Dec 22 2006 Michael Scherer <misc@mandriva.org> 1.99_90-1mdv2007.1
+ Revision: 101422
- update to 2.0 rc1

* Mon Dec 18 2006 Michael Scherer <misc@mandriva.org> 1.99_04-1mdv2007.1
+ Revision: 98386
- add missing BuildRequires
- fix rpmlint warning about bash completion file
- upgrade to 1.99_04
- Import svk



* Thu Jul 20 2006 Michael Scherer <misc@mandriva.org> 1.08-1mdv2007.0
- New version 1.08

* Thu Jul  6 2006 Olivier Blin <oblin@mandriva.com> 1.07-3mdv2007.0
- add explicit perl-Clone requires, since rpm's perl.req skips
  "require" statements that aren't flush against the left edge
  (for svk mkdir)
- buildrequires perl-Clone for tests
- Patch0: add missing "use Clone" in tests

* Thu Apr 27 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.07-2mdk
- Add perl-IO-Digest in dependencies (or else, svk merge crashes)

* Mon Feb 27 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.07-1mdk
- 1.07
- Drop patch 0
- Mark bash-completion file as config

* Wed Feb 01 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.06-2mdk
- Patch 0: silence warnings with perl 5.8.8

* Sun Dec 11 2005 Michael Scherer <misc@mandriva.org> 1.06-1mdk
- New release 1.06

* Sat Nov 26 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.05-3mdk
- bash-completion
- spec cleanup
- don't ship empty directories

* Thu Oct 06 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.05-2mdk
- Fix BuildRequires
- %%mkrel

* Thu Oct 06 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.05-1mdk
- 1.05
- Remove libsvn* from BuildRequires due to subversion package reorganisation

* Wed Aug 24 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.04-1mdk
- 1.04

* Fri Aug 19 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.03-1mdk
- 1.03

* Tue Aug 16 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.02-1mdk
- 1.02
- Fix requires (thanks to David Faure)
- Use prove instead of "make test", because tests are ok but not exit values,
  and "make test" isn't happy with that.

* Tue Jul 19 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.01-1mdk
- 1.01
- Fix apxs location

* Tue May 10 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.00-1mdk
- 1.00

* Sun May 01 2005 Michael Scherer <misc@mandriva.org> 0.994-1mdk
- New release 0.994

* Tue Apr 26 2005 Michael Scherer <misc@mandriva.org> 0.993-1mdk
- New release 0.993

* Fri Apr 22 2005 Michael Scherer <misc@mandriva.org> 0.992-2mdk
- fix my own bugreport #15295

* Tue Apr 19 2005 Michael Scherer <misc@mandrake.org> 0.992-1mdk
- New release 0.992
- use %%check

* Thu Mar 31 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.991-1mdk
- 0.991

* Tue Mar 15 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.30-2mdk
- Fix automatic dependencies of perl-SVK
- svk now requires perl-SVK of the same version

* Tue Mar 15 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.30-1mdk
- 0.30
- Requires File::Type manually

* Wed Feb 02 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.29-1mdk
- 0.29

* Tue Dec 21 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.27-1mdk
- New release
- Update descriptions
- Turn off the CPAN autoinstaller

* Fri Nov 12 2004 Stefan van der Eijk <stefan@mandrake.org> 0.26-2mdk
- BuildRequires
- Todo: somehow turn off the cpan autoinstaller for missing perl modules

* Fri Nov 12 2004 Michael Scherer <misc@mandrake.org> 0.26-1mdk
- New release 0.26

* Mon Oct 25 2004 Michael Scherer <misc@mandrake.org> 0.25-1mdk
- New release 0.25

* Sun Oct 24 2004 Michael Scherer <misc@mandrake.org> 0.23-1mdk
- New release 0.23

* Tue Oct  5 2004 Michael Scherer <misc@mandrake.org> 0.22-1mdk
- New release 0.22

* Fri Sep 24 2004 Michael Scherer <misc@mandrake.org> 0.21-1mdk
- New release 0.21

* Sat Sep  4 2004 Michael Scherer <misc@mandrake.org> 0.20-1mdk
- New release 0.20

* Tue Aug 31 2004 Michael Scherer <misc@mandrake.org> 0.19-2mdk
- BuildRequires

* Mon Aug 23 2004 Michael Scherer <misc@mandrake.org> 0.19-1mdk
- New release 0.19

* Sun Aug  8 2004 Stefan van der Eijk <stefan@eijk.nu> 0.18-3mdk
- still some more BuildRequires

* Sat Aug  7 2004 Stefan van der Eijk <stefan@eijk.nu> 0.18-2mdk
- BuildRequires to avoid endless looping

* Thu Aug  5 2004 Michael Scherer <misc@mandrake.org> 0.18-1mdk
- New release 0.18
- add missing BuildRequires

* Sun Jul 25 2004 Michael Scherer <misc@mandrake.org> 0.17-2mdk
- add a missing Requires

* Sun Jul 18 2004 Michael Scherer <misc@mandrake.org> 0.17-1mdk
- New release 0.17

* Wed Jun 30 2004 Michael Scherer <misc@mandrake.org> 0.16-1mdk
- New release 0.16
- reenable rpmbuildupdate

* Fri Jun 18 2004 Michael Scherer <misc@mandrake.org> 0.15-1mdk
- New release 0.15

* Wed Apr 28 2004 Michael Scherer <misc@mandrake.org> 0.14-1mdk
- 0.14

* Sun Apr 11 2004 Michael Scherer <misc@mandrake.org> 0.13-1mdk
- New release 0.13
- enable test

* Fri Apr 02 2004 Michael Scherer <misc@mandrake.org> 0.12-1mdk
- first Mandrakelinux package
