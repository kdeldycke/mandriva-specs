%define name diva
%define version 0.0.2.svn20061111
%define release %mkrel 1

Summary: Video editing for the Gnome desktop
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://files.diva-project.org/releases/%{name}-%{version}.tar.bz2
License: MIT
Group: Video
Url: http://www.diva-project.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: scons gnome-sharp2
BuildRequires: libgstreamer-plugins-base-devel
BuildRequires: mono-devel
BuildRequires: gtk+2-devel
BuildRequires: desktop-file-utils
Requires: gstreamer0.10-plugins-good

%description
Diva is a project to build an easy to use, scalable, open-source video
editing software for the Gnome desktop. Our goal is to provide users
with a complete and tightly integrated set of tools that can be used
to import, edit, enhance and export digital video material. The aim of
the project is to chart the unexplored areas of video editing for the
open-source platform.

%prep
%setup -q

%build
#gw yes, this is needed for scons
mkdir -p $RPM_BUILD_ROOT
scons DESTDIR=%buildroot

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
scons DESTDIR=%buildroot install
desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Multimedia" \
  --remove-category="KDE" \
  --add-category="AudioVideoEditing" \
  --add-category="X-MandrivaLinux-Multimedia-Video" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS MOTD NEWS README RELEASE
%{_bindir}/%{name}
%{_bindir}/%{name}-inspector
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/*.dll
%{_prefix}/lib/%{name}/*.exe
%{_prefix}/lib/%{name}/*.so
%dir %{_prefix}/lib/%{name}/plugins
%{_prefix}/lib/%{name}/plugins/*.dll
%{_prefix}/lib/%{name}/plugins/*.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
/usr/share/locale/*


%changelog
* Sat Nov 11 2006 Kevin Deldycke <kev@coolcavemen.com> 0.0.2.svn20061111-1mdv2007.0
- new build based on 2006/11/11 SVN version (r315)
- add /usr/share/locale/* files

* Tue Jun 27 2006 Götz Waschk <waschk@mandriva.org> 0.0.2-2mdv2007.0
- add mandriva xdg menu
- fix build on x86_64
- fix buildrequires

* Mon Jun 26 2006 Olivier Blin <oblin@mandriva.com> 0.0.2-1mdv2007.0
- initial Mandriva release
