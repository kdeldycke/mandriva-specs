%define version 0.2.3
%define tarname Rugg-%{version}


Summary:        Flexible file system and hard drive crash testing
Name:           Rugg
Version:        %version
Release:        %mkrel 1
Source0:        http://prdownloads.sourceforge.net/rugg/%tarname.tar.bz2
License:        GPL
Group:          System/Kernel and hardware
URL:            http://rugg.sourceforge.net
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  python >= 2.4, slocate
Requires:       python >= 2.4, slocate

%description
Flexible file system and hard drive crash testing.

Rugg is a hard drive and filesystem harness tool that allows you to test and benchmark drives and filesystems, by writing simple to complex scenarios that can mimic the behaviour of real-world applications.

What makes Rugg special is that it can be easily customized to test specific usages of the filesystem. Initially, Rugg was made to test new database server harddrives intended to host a Postgres database. The goal was to enable to simulate the way the database used the hard drive.

Rugg sports a simple and expressive domain specific language designed from the start to be compact and versatile. Have a look at for more.

%prep
%setup -q -n %tarname

%build
%__python setup.py build

%install
%__rm -rf %buildroot
%__python setup.py install --root  %buildroot

%clean
%__rm -rf %buildroot

%files
%defattr(755,root,root)
%doc README LICENSE
%doc Documentation/*
%_bindir/rugg
%py_puresitedir/rugg/

%changelog
* Wed Dec 27 2006 Kevin Deldycke <kev@coolcavemen.com> 0.2.3-1mdk
- new build based on version 0.2.3

* Wed May 10 2006 Kevin Deldycke <kev@coolcavemen.com> 0.2.2-1mdk
- new build based on version 0.2.2

* Mon Apr 17 2006 Kevin Deldycke <kev@coolcavemen.com> 0.2.1-1mdk
- initial package for Mandriva 2006.0
