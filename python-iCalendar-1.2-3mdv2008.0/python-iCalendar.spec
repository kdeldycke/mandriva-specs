%define	module	iCalendar
%define	name	python-%{module}
%define	version	1.2
%define	rel	3
%define	release	%mkrel %{rel}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Parser/generator of iCalendar files package for Python
Group:		Development/Python
License:	LGPL
URL:		http://codespeak.net/icalendar/
Source0:	http://codespeak.net/icalendar/%{module}-%{version}.tar.bz2
Requires:	python >= 2.3
BuildRequires: python-devel >= 2.3
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The iCalendar package is a parser/generator of iCalendar files for use
with Python. It follows the RFC 2445 (iCalendar) specification.

%prep
%setup -q -n %{module}-%{version}

%build

%__python setup.py build

%install
%__rm -rf %{buildroot}
%__python setup.py install --root=%{buildroot} --record=INSTALLED_FILES

%clean
%__rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc CHANGES.txt CREDITS.txt doc/ HISTORY.txt INSTALL.txt LICENSE.txt README.txt TODO.txt version.txt

%changelog
* Sat Jan 26 2008 Kevin Deldycke <kev@coolcavemen.com> 1.2-3mdv2008.0
- rebuild for Mandriva 2008.0

* Sun Jul 01 2007 Kevin Deldycke <kev@coolcavemen.com> 1.2-2mdv2007.1
- rebuild for Mandriva 2007.1

* Sat Apr 07 2007 Kevin Deldycke <kev@coolcavemen.com> 1.2-1mdv2007.0
- inital release
