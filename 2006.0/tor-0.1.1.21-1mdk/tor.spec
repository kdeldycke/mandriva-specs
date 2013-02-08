%define name tor
%define runuser toruser
%define version 0.1.1.21
%define release %mkrel 1

Name: %{name}
Version: %{version}
Release: %{release}
Summary: Anonymizing overlay network for TCP (The onion router)
URL: http://tor.eff.org/
Group: Networking/Other
License: BSD-like
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(postun):	rpm-helper
Requires: openssl >= 0.9.6
BuildRequires: openssl-devel >= 0.9.6 
BuildRequires: libevent-devel
BuildRequires: zlib-devel
BuildRequires: autoconf2.5
BuildRequires: transfig, tetex-latex
Source0: http://tor.eff.org/dist/%{name}-%{version}.tar.bz2
Source1: %{name}.logrotate
Source2: %{name}.init
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Tor is a connection-based low-latency anonymous communication system.

This package provides the "tor" program, which serves as both a client and
a relay node. Scripts will automatically create a "%{runuser}" user and
group, and set tor up to run as a daemon when the system is rebooted.

Applications connect to the local Tor proxy using the SOCKS
protocol. The local proxy chooses a path through a set of relays, in
which each relay knows its predecessor and successor, but no
others. Traffic flowing down the circuit is unwrapped by a symmetric
key at each relay, which reveals the downstream relay.

Warnings: Tor does no protocol cleaning.  That means there is a danger
that application protocols and associated programs can be induced to
reveal information about the initiator. Tor depends on Privoxy and
similar protocol cleaners to solve this problem. This is alpha code,
and is even more likely than released code to have anonymity-spoiling
bugs. The present network is very small -- this further reduces the
strength of the anonymity provided. Tor is not presently suitable
for high-stakes anonymity.

%prep
%setup -q 

%build
%configure2_5x
%make
make -C doc/design-paper tor-design.pdf

%install
%makeinstall

%define _logdir %{_var}/log

mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}
cat %{SOURCE2} > ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
chmod 0755 ${RPM_BUILD_ROOT}%{_initrddir}/%{name}

install -p -m 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/torrc.sample ${RPM_BUILD_ROOT}%{_sysconfdir}/%{name}/torrc

mkdir -p -m 755 ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
cat %{SOURCE1} > ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/%{name}

mkdir -p -m 700 ${RPM_BUILD_ROOT}%{_localstatedir}/%{name}
mkdir -p -m 755 ${RPM_BUILD_ROOT}%{_var}/run/%{name}
mkdir -p -m 755 ${RPM_BUILD_ROOT}%{_logdir}/%{name}

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && rm -rf ${RPM_BUILD_ROOT}

%pre
%_pre_useradd %{runuser} / /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}
rm -f ${_localstatedir}/%{name}/cached-directory
rm -f ${_localstatedir}/%{name}/bw_accounting
rm -f ${_localstatedir}/%{name}/control_auth_cookie
rm -f ${_localstatedir}/%{name}/router.desc
rm -f ${_localstatedir}/%{name}/fingerprint

%postun
%_postun_userdel %{runuser}
%_postun_groupdel %{runuser}

%files
%defattr(-,root,root)
%doc AUTHORS INSTALL LICENSE README ChangeLog doc/HACKING doc/TODO doc/design-paper/tor-design.pdf
%{_mandir}/man*/*
%{_bindir}/tor
%{_bindir}/torify
%{_bindir}/tor-resolve
%config(noreplace) %attr(0755,%{runuser},%{runuser}) %{_initrddir}/%{name}
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0755,root,%{runuser}) %{_sysconfdir}/%{name}/
%config(noreplace) %attr(0644,root,%{runuser}) %{_sysconfdir}/%{name}/*
%attr(0700,%{runuser},%{runuser}) %dir %{_localstatedir}/%{name}
%attr(0750,%{runuser},%{runuser}) %dir %{_var}/run/%{name}
%attr(0750,%{runuser},%{runuser}) %dir %{_logdir}/%{name}

%changelog
* Tue Jun 13 2006 Lenny Cartier <lenny@mandriva.com> 0.1.1.21-1mdv2007.0
- 0.1.1.21

* Thu May 25 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.1.20-1mdv2007.0
- New release 0.1.1.20
- use autoconf2.5
- buildrequires latex and transfig for the doc

* Sat Mar 11 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.0.17-1mdk
- New release 0.1.0.17

* Thu Jan 05 2006 Pascal Terjan <pterjan@mandriva.org> 0.1.0.16-1mdk
- 0.1.0.16

* Wed Nov 23 2005 Laurent MONTEL <lmontel@mandriva.com> 0.1.0.15-4
- Rebuild with new openssl

* Wed Oct 19 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.1.0.15-3mdk
- Fix BuildRequires

* Tue Sep 27 2005 Lev Givon <lev@columbia.edu> 0.1.0.15-2mdk
- Define %{_logdir} macro

* Sat Sep 24 2005 Pascal Terjan <pterjan@mandriva.org> 0.1.0.15-1mdk
- 0.1.0.15

* Tue Aug 16 2005 Pascal Terjan <pterjan@mandriva.org> 0.1.0.14-2mdk
- Add forgotten changelog

* Tue Aug 16 2005 Pascal Terjan <pterjan@mandriva.org> 0.1.0.14-1mdk
- 0.1.0.14 (security fix)

* Sun Aug 07 2005 Pascal Terjan <pterjan@zarb.org> 0.1.0.13-1mdk
- 0.1.0.13

* Sun Aug 07 2005 Pascal Terjan <pterjan@zarb.org> 0.1.0.12-1mdk
- first Mandriva version (partially based on the official rpm)
