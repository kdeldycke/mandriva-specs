%define name    dmg2img
%define version 1.6
%define release %mkrel 1


Name:          %{name}
Version:       %{version}
Release:       %{release}
Summary:       Converts dmg archives to HFS+ images
Group:         Productivity/File utilities
License:       GPLv2
URL:           http://vu1tur.eu.org/tools/
Source:        %{name}-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: libopenssl-devel, libbzip2-devel

%description
DMG2IMG is a tool which allows converting Apple compressed dmg archives to standard (hfsplus) image disk files.
This tool handles z-lib compressed dmg images.


%prep
%setup -q


%build
%{__make} CFLAGS="$RPM_OPT_FLAGS"


%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
install -m755 %{name} %{buildroot}%{_bindir}/
install -m755 vfdecrypt %{buildroot}%{_bindir}/
install -m644 vfdecrypt.1 %{buildroot}%{_mandir}/man1/


%files
%defattr(-,root,root,0755)
%{_bindir}/%{name}
%{_bindir}/vfdecrypt
%{_mandir}/man1/vfdecrypt.1*
%doc COPYING README


%clean
%{__rm} -rf %{buildroot}
%{__rm} -rf %{_builddir}/%{name}-%{version}-%{release}-buildroot


%changelog
* Sun Aug 01 2009 Kevin Deldycke <kevin@deldycke.com> 1.6-1mdv2009.1
- Clean up the legacy spec file
- Add missing libbzip2-devel build requirement
- Rebuild RPM for Mandriva 2009.1

* Thu Sep 25 2008 David Bolt <davjam@davjam.org>
- First spec and build for SUSE.
