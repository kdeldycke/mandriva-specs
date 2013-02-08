%define version 0.6
%define tarname televidilo-%{version}


Summary:    A GTK GUI to a bunch of french onlive TV video streams
Name:       Televidilo
Version:    %version
Release:    %mkrel 1
Source0:    http://download.gna.org/televidilo/%tarname.tar.bz2
License:    CeCILL version 2
Group:      Video
URL:        http://televidilo.bouil.org
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:   python, pygtk2.0, pygtk2.0-libglade, python-pyxml


%description
Application permettant de visualiser facilement les flux multimédias disponibles sur le web, et de les lancer dans le lecteur multimédia, éventuellement en plein écran, plutôt que dans une fenêtre web au format timbre poste.


%prep
%setup -c


%build


%install
%{__rm} -rf  %{buildroot}

%{__mkdir_p} %{buildroot}/usr/share/televidilo
%{__cp} -a Televidilo-%{version}/* %{buildroot}/usr/share/televidilo

%{__mkdir_p} %{buildroot}/%{_bindir}
cat > %{buildroot}/%{_bindir}/televidilo <<EOF
#!/bin/bash
cd /usr/share/televidilo/
./televidilo.py
EOF


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(755,root,root)
%{_bindir}/televidilo
/usr/share/televidilo/*

%changelog
* Mon May 14 2007 Kevin Deldycke <kev@coolcavemen.com> 0.6-1mdv2007.1
- initial package for Mandriva 2007.1