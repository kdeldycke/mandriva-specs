%define qemu_name	qemu
%define qemu_version	0.9.0
%define qemu_rel	6
#define qemu_release	%mkrel %{?qemu_snapshot:0.%{qemu_snapshot}.}%{qemu_rel}
%define qemu_release	%mkrel %{qemu_rel}
%define qemu_snapshot	20070214

# XXX add service
%define kqemu_name	kqemu
%define kqemu_version	1.3.0
%define kqemu_reldelta	3
%define kqemu_rel	%(echo $((%{qemu_rel} - %{kqemu_reldelta})))
%define kqemu_snapshot	pre11
%define kqemu_fullver	%{kqemu_version}%{?kqemu_snapshot:%{kqemu_snapshot}}
%define kqemu_dkmsver	%{kqemu_fullver}-%{kqemu_rel}
%define kqemu_release	%mkrel %{?kqemu_snapshot:0.%{kqemu_snapshot}.}%{kqemu_rel}
%define kqemu_arches	%{ix86} x86_64
%ifarch %{ix86}
%define kqemu_program	qemu
%endif
%ifarch x86_64
%define kqemu_program	qemu-system-x86_64
%endif

%define kvm_arches	%{ix86} x86_64

# Additionnal packaging notes
# XXX defined as macros so that to avoid extraneous empty lines
%ifarch %{kqemu_arches}
%define kqemu_note \
This QEMU package provides support for KQEMU, the QEMU Accelerator\
module.
%else
%define kqemu_note %{nil}
%endif
%ifarch %{kvm_arches}
%define kvm_note \
This QEMU package provides support for KVM (Kernel-based Virtual \
Machine), a full virtualization solution for Linux on x86 hardware \
containing virtualization extensions (AMD-v or Intel VT).
%else
%define kvm_note %{nil}
%endif

# Define targets to enable, allow redefinition from rpm build
%define all_targets i386-linux-user arm-linux-user armeb-linux-user arm-softmmu sparc-linux-user ppc-linux-user i386-softmmu ppc-softmmu sparc-softmmu x86_64-softmmu mips-softmmu
%{expand: %{!?targets: %%global targets %{all_targets}}}

%define __find_requires %{_builddir}/%{name}-%{version}/find_requires.sh

# QEMU doesn't build on x86 with gcc4 at this time
%if %{mdkversion} >= 200600
%ifarch %{ix86}
%define __cc	gcc-$(gcc3.3-version)
BuildRequires:	gcc3.3
%endif
%endif

Summary:	QEMU CPU Emulator
Name:		%{qemu_name}
Version:	%{qemu_version}
Release:	%{qemu_release}
Source0:	%{name}-%{version}%{?qemu_snapshot:-%{qemu_snapshot}}.tar.bz2
Source1:	kqemu-%{kqemu_fullver}.tar.bz2
Source2:	qemu.init
Patch1:		qemu-0.8.3-gcc4.patch
Patch2:		qemu-0.7.0-gcc4-dot-syms.patch
Patch3:		qemu-0.8.0-gcc4-hacks.patch
Patch4:		qemu-0.7.2-dyngen-check-stack-clobbers.patch
Patch5:		qemu-0.8.3-enforce-16byte-boundaries.patch
Patch6:		qemu-0.8.3-osx-intel-port.patch
Patch10:	qemu-0.7.0-cross64-mingw32-fixes.patch
Patch11:	qemu-0.9.0-kernel-option-vga.patch
Patch12:	qemu-0.7.2-no-nptl.patch
Patch13:	qemu-0.8.1-fix-errno-tls.patch
Patch14:	qemu-0.8.3-dont-strip.patch
Patch15:	qemu-0.8.3-x86_64-opts.patch
Patch16:	qemu-0.9.0-ppc.patch
Patch17:	qemu-0.9.0-fix-cpus-chaining.patch
Patch18:	qemu-0.9.0-migration.patch
Patch19:	qemu-0.9.0-not-rh-toolchain.patch
Patch20:	qemu-0.9.0-increase-initrd-load-addr.patch
Patch21:	qemu-0.9.0-fix-x86-fprem.patch
Patch200:	qemu-0.9.0-kvm.patch
Source201:	kvm_bios.bin
Patch201:	qemu-0.9.0-kvm-bios.patch
Patch202:	qemu-0.9.0-kvm-kqemu-window-caption.patch

License:	GPL
URL:		http://fabrice.bellard.free.fr/qemu/
Group:		Emulators
Requires:	qemu-img = %{version}-%{release}
BuildRequires:	libSDL-devel, tetex-texi2html
# XXXX: -luuid
BuildRequires:	e2fsprogs-devel
ExclusiveArch:	%{ix86} ppc x86_64 amd64 sparc
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%ifarch %{kqemu_arches}
# XXX: move up if some qemu-bridge is implemented for networking
Requires(post):   rpm-helper
Requires(preun):  rpm-helper
Requires:	  dkms-%{kqemu_name} >= %{kqemu_version}-%{kqemu_release}
%endif

%description
QEMU is a FAST! processor emulator. By using dynamic translation it
achieves a reasonnable speed while being easy to port on new host
CPUs. QEMU has two operating modes:

* User mode emulation. In this mode, QEMU can launch Linux processes
  compiled for one CPU on another CPU. Linux system calls are
  converted because of endianness and 32/64 bit mismatches. Wine
  (Windows emulation) and DOSEMU (DOS emulation) are the main targets
  for QEMU.

* Full system emulation. In this mode, QEMU emulates a full system,
  including a processor and various peripherials. Currently, it is
  only used to launch an x86 Linux kernel on an x86 Linux system. It
  enables easier testing and debugging of system code. It can also be
  used to provide virtual hosting of several virtual PC on a single
  server.
%kqemu_note
%kvm_note

%package -n dkms-%{kqemu_name}
Summary:	QEMU Accelerator Module
Group:		System/Kernel and hardware
Version:	%{kqemu_version}
Release:	%{kqemu_release}
Requires(post):	 dkms
Requires(preun): dkms

%description -n dkms-%{kqemu_name}
QEMU Accelerator (KQEMU) is a driver allowing the QEMU PC emulator to
run much faster when emulating a PC on an x86 host.

Full virtualization mode can also be enabled (with -kernel-kqemu) for
best performance. This mode only works with the following guest OSes:
Linux 2.4, Linux 2.6, Windows 2000 and Windows XP. WARNING: for
Windows 2000/XP, you cannot use it during installation.

Use "%{kqemu_program}" to benefit from the QEMU Accelerator Module.

%package img
Summary:	QEMU disk image utility
Group:		Emulators
Version:	%{qemu_version}
Release:	%{qemu_release}
Conflicts:	qemu < 0.9.0-%{mkrel 3}

%description img
This package contains the QEMU disk image utility that is used to
create, commit, convert and get information from a disk image.

%prep
%setup -q -a 1
%patch1 -p1 -b .gcc4
%patch2 -p1 -b .gcc4-dot-syms
%patch3 -p1 -b .gcc4-hacks
%patch4 -p1 -b .dyngen-check-stack-clobbers
%patch5 -p1 -b .enforce-16byte-boundaries
%patch6 -p1 -b .osx-intel-port
%patch10 -p1 -b .cross64-mingw32-fixes
%patch11 -p1 -b .kernel-option-vga
%if %{mdkversion} < 200700
%patch12 -p1 -b .no-nptl
%endif
%patch13 -p1 -b .fix-errno-tls
%patch14 -p1 -b .dont-strip
%patch15 -p1 -b .x86_64-opts
%patch16 -p1 -b .ppc
%patch17 -p1 -b .fix-cpus-chaining
%patch18 -p1 -b .migration
%patch19 -p1 -b .not-rh-toolchain
%patch20 -p1 -b .increase-initrd-load-addr
%patch21 -p1 -b .fix-x86-fprem

# kvm patches
%patch200 -p1 -b .kvm
cp %{SOURCE201} pc-bios/kvm_bios.bin
%patch201 -p1 -b .kvm-bios
%patch202 -p1 -b .kvm-kqemu-window-caption

# nuke explicit dependencies on GLIBC_PRIVATE
cat >find_requires.sh << EOF
#!/bin/sh
%{_prefix}/lib/rpm/find-requires %{buildroot} %{_target_cpu} | grep -v GLIBC_PRIVATE
EOF
chmod +x find_requires.sh

%build
# don't use -mtune=generic if it is not supported
if ! echo | %{__cc} -mtune=generic -xc -c - -o /dev/null 2> /dev/null; then
  CFLAGS=`echo "$RPM_OPT_FLAGS" | sed -e "s/-mtune=generic/-mtune=pentiumpro/g"`
fi
%configure2_5x --cc=%{__cc} --disable-gcc-check --target-list="%{targets}" --disable-gcc-check
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

# make sure to use the right accelerator-capable qemu binary on x86_64
cd $RPM_BUILD_ROOT%{_bindir}
mv qemu qemu-system-i386
%ifarch x86_64
ln -s qemu-system-x86_64 qemu
%else
ln -s qemu-system-i386 qemu
%endif
cd -

%ifarch %{kqemu_arches}
# install kqemu sources
mkdir -p $RPM_BUILD_ROOT%{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver}
(cd kqemu-%{kqemu_fullver} && tar cf - .) | \
(cd $RPM_BUILD_ROOT%{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver} && tar xf -)
cat > $RPM_BUILD_ROOT%{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver}/dkms.conf << EOF
PACKAGE_NAME=%{kqemu_name}
PACKAGE_VERSION=%{kqemu_dkmsver}
MAKE[0]="./configure --kernel-path=/lib/modules/\${kernelver}/source && make"
DEST_MODULE_LOCATION[0]=/kernel/3rdparty/%{kqemu_name}
BUILT_MODULE_NAME[0]=%{kqemu_name}
AUTOINSTALL=yes
EOF

# install service
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/%{name}

# install udev rules
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/65-%{kqemu_name}.rules << EOF
KERNEL=="%{kqemu_name}", MODE="0666"
EOF
%endif

%ifarch %{kvm_arches}
# install udev rules
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
cat > $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/65-kvm.rules << EOF
KERNEL=="kvm", MODE="0666"
EOF
%endif

# remove unpackaged files
rm -rf $RPM_BUILD_ROOT%{_docdir}/qemu

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
if [ "$1" -ge "1" ]; then
  /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi

%post -n dkms-%{kqemu_name}
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m %{kqemu_name} -v %{kqemu_dkmsver}
/usr/sbin/dkms --rpm_safe_upgrade build -m %{kqemu_name} -v %{kqemu_dkmsver}
/usr/sbin/dkms --rpm_safe_upgrade install -m %{kqemu_name} -v %{kqemu_dkmsver}
/sbin/modprobe %{kqemu_name} >/dev/null 2>&1 || :

%preun -n dkms-%{kqemu_name}
# rmmod can fail
/sbin/rmmod %{kqemu_name} >/dev/null 2>&1
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m %{kqemu_name} -v %{kqemu_dkmsver} --all || :

%files
%defattr(-,root,root)
%doc README qemu-doc.html qemu-tech.html
%{_bindir}/qemu
%{_bindir}/qemu-arm
%{_bindir}/qemu-armeb
%{_bindir}/qemu-i386
%{_bindir}/qemu-ppc
%{_bindir}/qemu-sparc
%{_bindir}/qemu-system-arm
%{_bindir}/qemu-system-ppc
%{_bindir}/qemu-system-mips
%{_bindir}/qemu-system-sparc
%{_bindir}/qemu-system-i386
%{_bindir}/qemu-system-x86_64
%{_mandir}/man1/qemu.1*
%dir %{_datadir}/qemu
%{_datadir}/qemu/*.bin
%{_datadir}/qemu/keymaps
%{_datadir}/qemu/video.x
%{_datadir}/qemu/openbios-sparc32
%config %{_initrddir}/%{name}
%ifarch %{kvm_arches}
%_sysconfdir/udev/rules.d/65-kvm.rules
%endif

%files img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_mandir}/man1/qemu-img.1*

%ifarch %{kqemu_arches}
%files -n dkms-%{kqemu_name}
%defattr(-,root,root)
%doc kqemu-%{kqemu_fullver}/README
%doc kqemu-%{kqemu_fullver}/kqemu-doc.html
%doc kqemu-%{kqemu_fullver}/kqemu-tech.html
%dir %{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver}
%{_usr}/src/%{kqemu_name}-%{kqemu_dkmsver}/*
%_sysconfdir/udev/rules.d/65-%{kqemu_name}.rules
%endif


%changelog
* Fri Mar 30 2007 Kevin Deldycke <kev@coolcavemen.com> 0.9.0-6mdv2007.0
- Backport from cooker to Mandriva 2007.0

* Tue Mar 27 2007 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.9.0-5mdv2007.1
+ Revision: 149237
- fix x86 fprem, aka fix konqueror in x86{,_64} guests (Julian Seward)
- propagate release to dkms config so that to handle upgrades gracefully
- don't try to load kvm module in xen0
- increase max -kernel size to 8 MB with -initrd (x86_64 guest, in particular)

* Thu Mar 15 2007 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.9.0-4mdv2007.1
+ Revision: 144294
- kqemu 1.3.0pre11 (no change)
- fix linux-user emulation on x86_64
- disable "no-nptl" patch for MDV >= 2007.0
- add should-start: dkms to initscript (blino)
- add conflicts to ensure upgrades from MDV < 2007.1

* Wed Mar 14 2007 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.9.0-3mdv2007.1
+ Revision: 143511
- split off qemu-img into another package
- make "qemu" the accelerator-capable binary on x86_64 too
- add KVM support (rev 4486)
- add live migration support (Anthony Liguori + KVM SVN)
- fix support for multi-threaded applications in linux-user

* Wed Feb 14 2007 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.9.0-2mdv2007.1
+ Revision: 120890
- add support for vga= option with -kernel (Pascal Terjan)
- updates from CVS (2007/02/14):
  * fix SYSLINUX hang (reset rombios32 area)
  * fix floating point to integer conversion in sparc emulation
  * serial console improvements
  * increase USB table poll interval
  * more linux-user syscalls: prctl, syslog

* Tue Feb 06 2007 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.9.0-1mdv2007.1
+ Revision: 116853
- 0.9.0
- integrate kqemu

* Sat Feb 03 2007 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.8.3-0.20070203.1mdv2007.1
+ Revision: 116057
- 64-bit fixes (preserve host registers)
- x86_64 host improvements (+15%% on nbench.flp)
- remove qvm86 accelerator (obsolete and unmaintained)
- updates from CVS (2007/02/03):
  * fix x86_64 syscalls, cwde and cdq
  * add sem*() and msg*() to linux-user emulation
  * add PIIX4 SMBus host support, EEPROM device emulation

* Tue Jan 30 2007 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.8.3-0.20070118.1mdv2007.1
+ Revision: 115559
- 0.8.3 snapshot (2007/01/18)



* Mon Jul 24 2006 trem <trem@mandriva.org> 0.8.2-1mdv2007.0
- 0.8.2

* Thu Jul 20 2006 trem <trem@mandriva.org> 0.8.1-2mdv2007.0
- add Patch20 which fix a compile error
- add arm-softmmu as target

* Fri May 04 2006 trem <trem@mandriva.org> 0.8.1-1mdk
- 0.8.1
- remove useless patch

* Mon Feb 13 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.8.0-4mdk
- fix gcc4 hacks for 0.8.0
- enforce 16-byte stack boundaries
- try to enforce only one exit point per synthetic opcode
- assorted fixes from cvs (2006/02/12):
  * fxsave/fxrstor fix
  * kqemu and SMP are currently not compatible
  * make target_mmap always return -1 on failure
  * correct DMA and transfer mode reporting (Jens Axboe)

* Sun Feb  5 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.8.0-3mdk
- add rtl8139 nic emulation (Igor Kovalenko)
- add support for nic card selection (-nic hw=ne2000|pcnet|rtl8139)
- fix but remove x86_64 softmmu asm opts as sizeof(CPUTLBEntry) is no
  longer of the form 2^n and thus requiring one more instruction that
  renders the optimization worthless

* Mon Jan 16 2006 trem <trem@mandriva.org> 0.8.0-2mdk
- Fix x86_64 compilation (disable patch x86_64-softmmu-asm)

* Tue Dec 20 2005 Pascal Terjan <pterjan@mandriva.org> 0.8.0-1mdk
- 0.8.0
- rediffed P8, P16
- merged P13 into P2
- dropped P12
- updated P11
- don't apply sheep-net patch for now, gb will do :)
- add patch by Paul Brook to speedup user-net (P19)

* Fri Oct 28 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.7.2-5mdk
- more gcc4 patches, disabled for now because of x86_64-softmmu

* Tue Oct 25 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.7.2-4mdk
- linux-user improvements:
  * add AT_PLATFORM & AT_HWCAP entries to auxiliary vector
  * forcibly disable use of NPTL for now since it's not emulated yet

* Tue Oct 11 2005 Pascal Terjan <pterjan@mandriva.org> 0.7.2-3mdk
- Enable building kqemu/qvm86 support (P12) :
  * don't require the sources of current kernel
  * as we don't know the kernel, enforce 2.6 build style

* Tue Oct 11 2005 Erwan Velu <erwan@seanodes.com> 0.7.2-2mdk
- Oops, 0.7.2-1mdk wasn't good :(
- importing newest kqemu.h
- qvm86 updates from CVS (2005/10/10)

* Mon Oct 10 2005 Erwan Velu <erwan@seanodes.com> 0.7.2-1mdk
- 0.7.2
- Rediffing to 0.7.2
- patch13 is merged upstream

* Thu Aug 11 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.7.1-3mdk
- IDE fix from CVS for FreeBSD/AMD64 support
- run-time detect qvm86/kqemu and enable specific features accordingly
- qvm86 updates from CVS (2005/08/01):
  * performance improvements
  * add support for pae enabled host kernels

* Mon Jul 25 2005 Pascal Terjan <pterjan@mandriva.org> 0.7.1-2mdk
- use new kqemu.h from kqemu
- enable kqemu support on x86_64 (P12)
- don't break x86_64 in P8 when kqemu is enabled

* Mon Jul 25 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.7.1-1mdk
- only use gcc3.3 in 2006+ and x86
- load initrd at a higher address in pc emulation
- 0.7.1:
  * fixes to sparc64 and ppc system emulation
  * add initial support for mips system emulation
  * fixes to i386 emulation: fscale, add overflow exceptions in divisions
  * fix 64-bit virtual addressing
  * allow more than 4 GB of physical memory
  * add IO-APIC support for Windows 64
  * add support for s390 hosts
  * linux-user improvements: more set/getsockopt values, [f]truncate64,

* Thu Jul 21 2005 Pascal Terjan <pterjan@mandriva.org> 0.7.0-8mdk
- add AMD pcnet patch (faster NIC, add -nic-pcnet to use it)
- fix qvm86 description (only runs on kernels without PAE)
- enforce using gcc3.3

* Sat Jun  4 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.7.0-7mdk
- minor optimizations to x86-64 host:
  * support direct jumps
  * assembly optimizations to softmmu mode

* Thu Jun  2 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.7.0-6mdk
- fix build with gcc4 (Paul Brook)
- fix build with gcc4 on x86_64 and local dot symbols
- fix x86-64 system emulation regression introduced from qvm86 patch

* Wed Jun  1 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.7.0-5mdk
- refactor buildrequires
- add support for -sheep-net network emulation

* Tue May 17 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.7.0-4mdk
- remove double free in slirp code
- 64-bit fixes to -user-net
- cross-compilation fixes to mingw32 from 64-bit host
- selected fixes from CVS (2005/05/17):
  * Windows 2000 install disk full hack (with -win2k-hack)
  * BMDMA interrupt fix (aka Solaris x86 IDE bug fix)
  * ne2000 reset fix (aka OS/2 Warp V4 fix)
  * handle the case where several PCI irqs share the same PIC irq
  * open fix in Linux/ARM user emulation
  * ARM saturating arithmetic fixes
  * ARM VFP dump fix
  * PPC dcbz fix

* Fri May 13 2005 Pascal Terjan <pterjan@mandriva.org> 0.7.0-3mdk
- Support qvm86 instead

* Wed May 11 2005 Pascal Terjan <pterjan@mandriva.org> 0.7.0-2mdk
- Enable kqemu support

* Fri Apr 29 2005 Pascal Terjan <pterjan@mandriva.org> 0.7.0-1mdk
- 0.7.0
- regenerate P1
- add new targets

* Sun Nov 14 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.6.1-1mdk
- 0.6.1
- build sparc target
- add initial sparc host cpu support
- drop P0, P2 & P3 (merged upstream)
- regenerate P1

* Wed Sep 29 2004 Michael Scherer <misc@mandrake.org> 0.6.0-2mdk
- fix memleak of userspace-net-stack, ( http://lists.gnu.org/archive/html/qemu-devel/2004-09/msg00244.html )

* Mon Sep  6 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.6.0-1mdk
- 0.6.0
- updates from CVS (2004/09/06):
  * fix x86 bound instruction
  * fix build on x86 with asm memory helpers
  * fix build on ppc

* Tue Mar 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.5.0-4mdk
- buildrequires

* Fri Nov  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.0-3mdk
- lib64 fixes
- update to current CVS:
  - float access fixes when using soft mmu
  - PC emulation support on PowerPC
  - A20 support

* Thu Nov  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.0-2mdk
- add initial AMD64 host cpu support

* Thu Nov  6 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.0-1mdk
- 0.5.0

* Fri Aug 01 2003 Michael Scherer <scherer.michael@free.fr> 0.4.1-2mdk
- BuildRequires ( glibc-static-devel )

* Mon Jul  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.4.1-1mdk
- 0.4.1

* Tue Jun  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.2-1mdk
- 0.2

* Sat Apr 12 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.6-1mdk
- 0.1.6

* Mon Mar 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.4-1mdk
- 0.1.4

* Thu Mar 27 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.1.2-1mdk
- First Mandrake Linux package
- Patch0: Fix x86 signal handler to retrieve pc from [REG_IP] slot
- Patch1: Add support for nanosecond resolution timestamps from glibc 2.3
- Patch2: Adjust ldscripts for glibc >= 2.3
- Patch3: Handle exit_group syscall as an exit
- Patch4: Add missing includes
