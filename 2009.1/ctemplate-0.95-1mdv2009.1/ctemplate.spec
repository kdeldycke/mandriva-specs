%define	major 0
%define libname %mklibname ctemplate %{major}
%define develname %mklibname ctemplate -d

Summary:	Simple but powerful template language for C++
Name:		ctemplate
Version:	0.95
Release:	%mkrel 1
Group:		System/Libraries
License:	BSD
URL:		http://code.google.com/p/google-ctemplate/
Source:		http://google-ctemplate.googlecode.com/files/%{name}-%{version}.tar.gz
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	autoconf2.5
Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
The ctemplate package contains a library implementing a simple but
powerful template language for C++.  It emphasizes separating logic
from presentation: it is impossible to embed application logic in this
template language.  This limits the power of the template language
without limiting the power of the template *system*.  Indeed, Google's
"main" web search uses this system exclusively for formatting output.

%package -n	%{libname}
Summary:	Simple but powerful template language for C++
Group:          System/Libraries

%description -n	%{libname}
The ctemplate package contains a library implementing a simple but
powerful template language for C++.  It emphasizes separating logic
from presentation: it is impossible to embed application logic in this
template language.  This limits the power of the template language
without limiting the power of the template *system*.  Indeed, Google's
"main" web search uses this system exclusively for formatting output.

%package -n	%{develname}
Summary:	Development files for the %{name} library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname ctemplate 0 -d}

%description -n	%{develname}
The ctemplate-devel package contains static and debug libraries and header
files for developing applications that use the ctemplate package.

%prep

%setup -q

%build
export PTHREAD_LIBS="-lpthread"

%configure2_5x

%make

#%%check
#make check <- borked atm

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# cleanup
rm -rf %{buildroot}%{_docdir}/ctemplate-*

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL README doc/*
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_bindir}/diff_tpl_auto_escape
%{_bindir}/make_tpl_varnames_h
%{_bindir}/template-converter
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
/usr/include/ctemplate/*.h


%changelog
* Tue Aug 18 2009 Kevin Deldycke <kevin@deldycke.com> 0.95-1mdv2009.0
- Upgrade to ctemplate 0.95
- Fix broken file inclusion in devel package
- Rebuild RPM for Mandriva 2009.1

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0.94-1mdv2010.0
+ Revision: 376957
- 0.94

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0.90-1mdv2009.0
+ Revision: 200403
- 0.90

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Oct 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0.8-1mdv2008.1
+ Revision: 96986
- 0.8
- new devel naming

* Sun Jun 24 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-1mdv2008.0
+ Revision: 43639
- Import ctemplate



* Sun Jun 24 2007 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-1mdv2008.0
- 0.6.1

* Fri Jul 28 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2-1mdk
- 0.2

* Tue May 02 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1-1mdk
- initial Mandriva package
