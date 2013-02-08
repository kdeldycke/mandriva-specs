%define version 0.6
%define appname televidilo


Summary:    A GTK GUI to a bunch of french onlive TV video streams
Name:       %appname
Version:    %version
Release:    %mkrel 3
Source0:    http://download.gna.org/televidilo/%appname-%version.tar.bz2
License:    CeCILL 2
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

%{__mkdir_p} %{buildroot}/%{_datadir}/%appname
%{__cp} -a Televidilo-%{version}/* %{buildroot}/%{_datadir}/%appname

%{__mkdir_p} %{buildroot}/%{_bindir}
cat > %{buildroot}/%{_bindir}/%appname <<EOF
#!/bin/bash
cd %{_datadir}/%appname/
./televidilo.py
EOF


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(755,root,root)
%{_bindir}/%appname
%{_datadir}/%appname/*


%changelog
* Mon May 14 2007 Kevin Deldycke <kev@coolcavemen.com> 0.6-3mdv2008.0
- rebuild for Mandriva 2008.0

* Mon May 14 2007 Kevin Deldycke <kev@coolcavemen.com> 0.6-2mdv2007.1
- macro-ize everything

* Mon May 14 2007 Kevin Deldycke <kev@coolcavemen.com> 0.6-1mdv2007.1
- initial package for Mandriva 2007.1